"""Compare the current and fine-tuned Laya checkpoints on the golden set and a held-out batch.

    uv run python scripts/generate_production.py --data-dir <dir> --week holdout --n 150 --seed 99
    uv run python tools/compare_models.py <dir>/production/holdout.jsonl models/candidate-v2/checkpoint
"""
import json, sys
from collections import Counter
from doctype.adapters.laya_model import LayaModel
from doctype.adapters.storage import StaticGoldenSet
from doctype.domain import GoldenExample
from doctype.services import EvalService

holdout_path, cand_dir = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(holdout_path)]
sets = {
    "golden-v1 (10)": StaticGoldenSet.from_jsonl(__import__("pathlib").Path("data/golden/golden-v1.jsonl")),
    f"holdout ({len(rows)})": StaticGoldenSet("holdout", [GoldenExample(r["text"], r["template_group"], r["truth"]) for r in rows]),
    "holdout hard only": StaticGoldenSet("hard", [GoldenExample(r["text"], r["template_group"], r["truth"]) for r in rows if r.get("hard")]),
}
models = {"current": LayaModel("convaiinnovations/laya", "typed-decisions"),
          "fine-tuned": LayaModel(version="candidate-v2", local_dir=cand_dir)}
out = {}
for mname, m in models.items():
    for sname, gs in sets.items():
        ev = EvalService(gs)
        reps = {t: ev.evaluate(m, t) for t in (0.85, 0.6)}
        r = reps[0.85]
        out[(mname, sname)] = r
        print(f"{mname:<10} {sname:<18} acc={r.accuracy:.3f} ece={r.ece:.3f} "
              f"cov@0.85={r.coverage:.2f} err@0.85={r.auto_error:.2f} "
              f"cov@0.6={reps[0.6].coverage:.2f} err@0.6={reps[0.6].auto_error:.2f}")
        print(" " * 11, "recall:", " ".join(f"{k}={v:.2f}" for k, v in r.recall.items()))
    preds = [(m.predict(r["text"]), r["truth"]) for r in rows]
    conf = sorted(max(p.values()) for p, _ in preds)
    errs = Counter((y, max(p, key=p.get)) for p, y in preds if max(p, key=p.get) != y)
    print(f"{mname:<10} holdout confidence min {conf[0]:.2f} median {conf[len(conf)//2]:.2f} max {conf[-1]:.2f}; "
          f"confusions {dict(errs.most_common(5))}")
