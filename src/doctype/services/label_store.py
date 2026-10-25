"""Decision log, labels with provenance, and versioned training snapshots."""

from __future__ import annotations

import random
import uuid

from ..domain import (
    DOC_TYPES, Decision, Document, Label, LabelSource, Snapshot, TrainingExample, doc_hash, now,
)
from ..ports import DecisionLog, GoldenSetRegistry, LabelRepository, SnapshotStore

SOURCE_WEIGHTS = {LabelSource.HUMAN: 1.0, LabelSource.DOWNSTREAM: 0.7, LabelSource.LLM_FALLBACK: 0.4}


class LabelStoreService:
    def __init__(self, decisions: DecisionLog, labels: LabelRepository, golden: GoldenSetRegistry,
                 snapshots: SnapshotStore, audit_rate: float = 0.02, rng: random.Random | None = None) -> None:
        self._decisions, self._labels, self._golden, self._snapshots = decisions, labels, golden, snapshots
        self._audit_rate = audit_rate
        self._rng = rng or random.Random()

    # 1. every Laya call
    def record_decision(self, *, doc: Document, input_uri: str, model_version: str,
                        probabilities: dict[str, float], threshold: float) -> Decision:
        route = "auto" if max(probabilities.values()) >= threshold else "fallback"
        decision = Decision(
            decision_id=str(uuid.uuid4()), tenant_id=doc.tenant_id, doc_id=doc.doc_id,
            doc_hash=doc_hash(doc.text), template_group=doc.template_group, input_uri=input_uri,
            model_version=model_version, probabilities=dict(probabilities), threshold=threshold,
            route=route, audited=route == "auto" and self._rng.random() < self._audit_rate, created_at=now(),
        )
        self._decisions.append(decision)
        return decision

    # 2-4. labels from fallback, extractors and humans
    def add_label(self, decision_id: str, doc_type: str, source: LabelSource, actor: str, note: str = "") -> Label:
        if doc_type not in DOC_TYPES:
            raise ValueError(f"unknown doc_type {doc_type!r}")
        d = self._decisions.get(decision_id)
        label = Label(str(uuid.uuid4()), decision_id, d.tenant_id, doc_type, source, actor, now(), note)
        self._labels.add(label)
        return label

    def resolve(self, decision_id: str, min_source: LabelSource) -> Label | None:
        """Highest trust wins; latest wins within a tier; disagreement below HUMAN returns None."""
        candidates = [l for l in self._labels.for_decision(decision_id) if l.source >= min_source]
        if not candidates:
            return None
        top = max(l.source for l in candidates)
        tier = [l for l in candidates if l.source == top]
        if top != LabelSource.HUMAN and len({l.doc_type for l in tier}) > 1:
            return None
        return max(tier, key=lambda l: l.created_at)

    def human_labelled(self, tenant_id: str, audited_only: bool = False) -> list[tuple[Decision, str]]:
        out = []
        for d in self._decisions.all_for_tenant(tenant_id):
            if audited_only and not d.audited:
                continue
            humans = [l for l in self._labels.for_decision(d.decision_id) if l.source == LabelSource.HUMAN]
            if humans:
                out.append((d, max(humans, key=lambda l: l.created_at).doc_type))
        return out

    # 6. training job entry point
    def build_snapshot(self, tenant_id: str, min_source: LabelSource = LabelSource.LLM_FALLBACK) -> str:
        golden_hashes, golden_groups = self._golden.doc_hashes(), self._golden.template_groups()
        examples: list[TrainingExample] = []
        seen: set[str] = set()
        ex_golden = ex_template = ex_conflict = ex_floor = 0
        for d in self._decisions.all_for_tenant(tenant_id):
            if d.doc_hash in golden_hashes:
                ex_golden += 1
                continue
            if d.template_group in golden_groups:
                ex_template += 1
                continue
            if d.doc_hash in seen:
                continue
            labels = self._labels.for_decision(d.decision_id)
            if not labels:
                continue
            if not any(l.source >= min_source for l in labels):
                ex_floor += 1
                continue
            label = self.resolve(d.decision_id, min_source)
            if label is None:
                ex_conflict += 1
                continue
            seen.add(d.doc_hash)
            examples.append(TrainingExample(d.decision_id, d.input_uri, label.doc_type, label.source,
                                            SOURCE_WEIGHTS[label.source]))
        snap = Snapshot(str(uuid.uuid4()), tenant_id, now(), self._golden.version(), min_source,
                        tuple(examples), ex_golden, ex_template, ex_conflict, ex_floor)
        return self._snapshots.write(snap)
