"""Command line entry point.

    doctype demo       full end-to-end run: week 1 intake, review, calibration, training, week 2
    doctype classify   one text through the model and the gate
    doctype eval       current model against the golden set
    doctype probe      raw Laya output for one text, to confirm the answer shape
"""

from __future__ import annotations

import argparse
import dataclasses
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from .config import Settings
from .container import App, build_app, build_model
from .domain import Document, EvalReport, LabelSource
from .services import CalibratedModel, fit_temperature, tune_threshold

MIN_AUDIT_SAMPLE = 30


def _fmt(r: EvalReport) -> str:
    rec = " ".join(f"{t}={v:.2f}" for t, v in r.recall.items())
    return (f"{r.model_version}\n      acc={r.accuracy:.2f} ece={r.ece:.3f} "
            f"coverage@{r.threshold:.2f}={r.coverage:.2f} auto_error={r.auto_error:.2f}\n      recall: {rec}")


def _load_batch(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def _run_week(app: App, name: str, rows: list[dict], truth: dict[str, str]) -> None:
    model = app.models.current()
    print(f"\n== {name}: {model.version}, threshold {app.intake.threshold:.2f}")
    with app.tracer.span("week", week=name, model_version=model.version, threshold=app.intake.threshold,
                         documents=len(rows)) as span:
        auto = 0
        for i, row in enumerate(rows):
            doc = Document(f"{name}-{i}", app.settings.tenant, row["text"], row["template_group"])
            out = app.intake.process(doc)
            truth[out.decision.decision_id] = row["truth"]
            auto += out.decision.route == "auto"
            print(f"  {row['text'][:46]:<46}  {out.path}")
        print(f"  auto-routed {auto}/{len(rows)}")
        span.set(auto_routed=auto)
        with app.tracer.span("ops.review", actor="ops:reviewer") as review:
            items = app.review.drain()
            for d, reason in items:   # simulated ops reviewer, using the ground truth in the sample file
                app.store.add_label(d.decision_id, truth[d.decision_id], LabelSource.HUMAN, "ops:reviewer", reason)
                review.event("label", decision_id=d.decision_id, reason=reason, source=LabelSource.HUMAN.name,
                             doc_type=truth[d.decision_id])
            review.set(items=len(items))
        print(f"  ops reviewed {len(items)}: {dict(Counter(r for _, r in items))}")


def cmd_demo(s: Settings) -> None:
    run_dir = Path(s.var_dir) / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    app = build_app(s, run_dir)
    data = Path(s.data_dir) / "production"
    truth: dict[str, str] = {}
    print(f"model={s.model} fallback={s.fallback} trainer={s.trainer} run={run_dir}")
    try:
        with app.tracer.span("demo", model=s.model, fallback=s.fallback, trainer=s.trainer, tenant=s.tenant,
                             run_dir=str(run_dir)):
            _demo_steps(app, s, run_dir, data, truth)
    finally:
        if trace := app.tracer.close():
            print(f"trace {trace}")


def _demo_steps(app: App, s: Settings, run_dir: Path, data: Path, truth: dict[str, str]) -> None:
    _run_week(app, "week1", _load_batch(data / "week1.jsonl"), truth)

    with app.tracer.span("calibration", min_audit_sample=MIN_AUDIT_SAMPLE) as span:
        audited = app.store.human_labelled(s.tenant, audited_only=True)
        span.set(audited=len(audited))
        print(f"\n== calibration: {len(audited)} audited decisions")
        if len(audited) >= MIN_AUDIT_SAMPLE:
            t = fit_temperature(audited)
            tuned = tune_threshold(audited, max_auto_error=0.05)
            span.set(fitted=True, temperature=t, threshold=tuned)
            print(f"  temperature={t:.2f} threshold={tuned}")
            if tuned is not None:
                app.intake.threshold = tuned
        else:
            span.set(fitted=False, threshold=app.intake.threshold)
            print(f"  fewer than {MIN_AUDIT_SAMPLE}; keeping temperature 1.0 and threshold {app.intake.threshold:.2f}")

    print("\n== training run")
    result = app.pipeline.run(s.tenant, "candidate-v2", app.intake.threshold)
    snap = result.snapshot
    print(f"  manifest {result.snapshot_uri}")
    print(f"  examples {len(snap.examples)} by source {dict(Counter(e.source.name for e in snap.examples))}")
    print(f"  excluded golden={snap.excluded_golden} template={snap.excluded_template} "
          f"conflict={snap.excluded_conflict} below_floor={snap.excluded_below_floor}")
    print(f"  eval on {app.golden.version()} ({app.golden.examples().__len__()} examples)")
    print("    current  ", _fmt(result.current))
    if result.candidate:
        print("    candidate", _fmt(result.candidate))
    print(f"  promoted: {result.promoted}" + (f"  ({'; '.join(result.reasons)})" if result.reasons else ""))
    (run_dir / "eval.json").write_text(json.dumps(
        {"current": dataclasses.asdict(result.current),
         "candidate": dataclasses.asdict(result.candidate) if result.candidate else None,
         "promoted": result.promoted, "reasons": result.reasons}, indent=2))

    _run_week(app, "week2", _load_batch(data / "week2.jsonl"), truth)
    print(f"\nrun artefacts in {run_dir}")


def cmd_classify(s: Settings, text: str) -> None:
    probs = build_model(s).predict(text)
    best = max(probs, key=probs.get)
    route = "auto" if probs[best] >= s.threshold else "fallback"
    for t, p in sorted(probs.items(), key=lambda kv: -kv[1]):
        print(f"  {t:<13} {p:.3f}")
    print(f"-> {best} ({route} at threshold {s.threshold:.2f})")


def cmd_eval(s: Settings, temperature: float) -> None:
    app = build_app(s, Path(s.var_dir) / "eval")
    model = app.models.current()
    if temperature != 1.0:
        model = CalibratedModel(model, temperature)
    with app.tracer.span("eval", model_version=model.version, threshold=s.threshold) as span:
        r = app.evals.evaluate(model, s.threshold)
        span.set(accuracy=r.accuracy, ece=r.ece, coverage=r.coverage, recall=r.recall)
    print(_fmt(r))
    if trace := app.tracer.close():
        print(f"trace {trace}")


def cmd_probe(s: Settings, text: str) -> None:
    from .adapters.laya_model import LayaModel
    m = LayaModel(s.laya_repo, s.laya_subfolder or None)
    print(json.dumps(m.raw(text), indent=2, default=str))


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="doctype")
    p.add_argument("--model", choices=["simulated", "laya"])
    p.add_argument("--fallback", choices=["simulated", "ollama", "bedrock"])
    p.add_argument("--trainer", choices=["simulated", "export", "laya"])
    p.add_argument("--threshold", type=float)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    c = sub.add_parser("classify")
    c.add_argument("text")
    e = sub.add_parser("eval")
    e.add_argument("--temperature", type=float, default=1.0)
    pr = sub.add_parser("probe")
    pr.add_argument("text")
    args = p.parse_args(argv)

    s = Settings.from_env()
    overrides = {k: v for k, v in {"model": args.model, "fallback": args.fallback,
                                   "trainer": args.trainer, "threshold": args.threshold}.items() if v is not None}
    if args.model == "laya" and args.trainer is None and s.trainer == "simulated":
        overrides["trainer"] = "export"
    s = dataclasses.replace(s, **overrides)

    if args.cmd == "demo":
        cmd_demo(s)
    elif args.cmd == "classify":
        cmd_classify(s, args.text)
    elif args.cmd == "eval":
        cmd_eval(s, args.temperature)
    elif args.cmd == "probe":
        cmd_probe(s, args.text)


if __name__ == "__main__":
    main()
