"""Snapshot -> fine-tune -> eval on golden set -> promote. In AWS: a Step Functions state machine."""

from __future__ import annotations

from dataclasses import dataclass

from ..domain import EvalReport, LabelSource, Snapshot
from ..ports import ModelRegistry, SnapshotStore, TextStore, Trainer
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
                 models: ModelRegistry, evals: EvalService, policy: PromotionPolicy) -> None:
        self._store, self._snapshots, self._texts = store, snapshots, texts
        self._trainer, self._models, self._evals, self._policy = trainer, models, evals, policy

    def run(self, tenant_id: str, new_version: str, threshold: float,
            min_source: LabelSource = LabelSource.LLM_FALLBACK) -> TrainingResult:
        uri = self._store.build_snapshot(tenant_id, min_source)
        snap = self._snapshots.read(uri)
        current = self._models.current()
        cur_rep = self._evals.evaluate(current, threshold)

        candidate = self._trainer.fine_tune(current, snap, self._texts, new_version)
        if candidate is None:
            return TrainingResult(uri, snap, cur_rep, None, False, ["trainer exported data only"])

        cand_rep = self._evals.evaluate(candidate, threshold)
        ok, reasons = self._policy.decide(cur_rep, cand_rep)
        self._models.register(candidate, cand_rep, uri)
        if ok:
            self._models.promote(candidate.version)
        return TrainingResult(uri, snap, cur_rep, cand_rep, ok, reasons)
