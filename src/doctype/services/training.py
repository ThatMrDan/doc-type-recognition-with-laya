"""Snapshot -> fine-tune -> eval on golden set -> promote. In AWS: a Step Functions state machine."""

from __future__ import annotations

from dataclasses import dataclass

from ..domain import EvalReport, LabelSource, Snapshot
from ..ports import DecisionModel, ModelRegistry, SnapshotStore, TextStore, Tracer, Trainer
from .evaluation import EvalService, PromotionPolicy
from .label_store import LabelStoreService


@dataclass(frozen=True)
class TrainingResult:
    snapshot_uri: str
    snapshot: Snapshot
    current: EvalReport
    candidate: EvalReport | None
    promoted: bool
    reasons: list[str]


class TrainingPipeline:
    def __init__(self, store: LabelStoreService, snapshots: SnapshotStore, texts: TextStore, trainer: Trainer,
                 models: ModelRegistry, evals: EvalService, policy: PromotionPolicy, tracer: Tracer) -> None:
        self._store, self._snapshots, self._texts = store, snapshots, texts
        self._trainer, self._models, self._evals, self._policy = trainer, models, evals, policy
        self._tracer = tracer

    def run(self, tenant_id: str, new_version: str, threshold: float,
            min_source: LabelSource = LabelSource.LLM_FALLBACK) -> TrainingResult:
        with self._tracer.span("training.run", tenant_id=tenant_id, new_version=new_version,
                               threshold=threshold, min_source=min_source.name) as span:
            result = self._run(tenant_id, new_version, threshold, min_source)
            span.set(promoted=result.promoted, reasons="; ".join(result.reasons))
            return result

    def _run(self, tenant_id: str, new_version: str, threshold: float, min_source: LabelSource) -> TrainingResult:
        with self._tracer.span("snapshot.build") as span:
            uri = self._store.build_snapshot(tenant_id, min_source)
            snap = self._snapshots.read(uri)
            span.set(uri=uri, snapshot_id=snap.snapshot_id, examples=len(snap.examples),
                     excluded={"golden": snap.excluded_golden, "template": snap.excluded_template,
                               "conflict": snap.excluded_conflict, "below_floor": snap.excluded_below_floor})
        current = self._models.current()
        cur_rep = self._evaluate("eval.current", current, threshold)

        with self._tracer.span("trainer.fine_tune", base=current.version, trainer=type(self._trainer).__name__) as span:
            candidate = self._trainer.fine_tune(current, snap, self._texts, new_version)
            span.set(candidate=candidate.version if candidate else "none (exported data only)")
        if candidate is None:
            return TrainingResult(uri, snap, cur_rep, None, False, ["trainer exported data only"])

        cand_rep = self._evaluate("eval.candidate", candidate, threshold)
        with self._tracer.span("promotion.decide", current=current.version, candidate=candidate.version) as span:
            ok, reasons = self._policy.decide(cur_rep, cand_rep)
            self._models.register(candidate, cand_rep, uri)
            if ok:
                self._models.promote(candidate.version)
            span.set(promoted=ok, reasons="; ".join(reasons))
        return TrainingResult(uri, snap, cur_rep, cand_rep, ok, reasons)

    def _evaluate(self, name: str, model: DecisionModel, threshold: float) -> EvalReport:
        with self._tracer.span(name, model_version=model.version) as span:
            r = self._evals.evaluate(model, threshold)
            span.set(golden_version=r.golden_version, n=r.n, accuracy=r.accuracy, ece=r.ece,
                     coverage=r.coverage, auto_error=r.auto_error, recall=r.recall)
            return r
