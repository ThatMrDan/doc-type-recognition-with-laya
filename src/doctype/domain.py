"""Domain types. No I/O, no third-party imports."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum

# Option label -> description. Laya scores these descriptions directly, so the
# wording matters: describe what the document looks like, not what it is for.
CRITERIA: dict[str, str] = {
    "sov": "statement or schedule of values: property locations, premises, insured values, TIV, construction",
    "loss_run": "loss run or loss history: claims by year, incurred, paid, reserved, large losses",
    "acord": "ACORD standard form such as ACORD 125, 126 or 140 application sections",
    "broker_email": "broker or MGA email covering a submission: from, re, fwd, attached, regards",
    "other": "anything else: surveys, valuation reports, photos, plans, unrelated documents",
}
DOC_TYPES: tuple[str, ...] = tuple(CRITERIA)


class LabelSource(IntEnum):
    """Higher value = more trusted."""
    LLM_FALLBACK = 1
    DOWNSTREAM = 2      # another extractor's schema accepted the document
    HUMAN = 3


@dataclass(frozen=True)
class Document:
    doc_id: str
    tenant_id: str
    text: str                    # already cut to what Laya sees: first page, sheet headers, email body
    template_group: str          # broker/template key, used to stop near-duplicate leakage


@dataclass(frozen=True)
class Decision:
    decision_id: str
    tenant_id: str
    doc_id: str
    doc_hash: str
    template_group: str
    input_uri: str
    model_version: str
    probabilities: dict[str, float]
    threshold: float
    route: str                   # "auto" or "fallback"
    audited: bool
    created_at: datetime

    @property
    def predicted(self) -> str:
        return max(self.probabilities, key=self.probabilities.get)

    @property
    def confidence(self) -> float:
        return self.probabilities[self.predicted]


@dataclass(frozen=True)
class Label:
    label_id: str
    decision_id: str
    tenant_id: str
    doc_type: str
    source: LabelSource
    actor: str
    created_at: datetime
    note: str = ""


@dataclass(frozen=True)
class TrainingExample:
    decision_id: str
    input_uri: str
    doc_type: str
    source: LabelSource
    weight: float


@dataclass(frozen=True)
class Snapshot:
    snapshot_id: str
    tenant_id: str
    created_at: datetime
    golden_set_version: str
    min_source: LabelSource
    examples: tuple[TrainingExample, ...]
    excluded_golden: int
    excluded_template: int
    excluded_conflict: int
    excluded_below_floor: int


@dataclass(frozen=True)
class GoldenExample:
    text: str
    template_group: str
    doc_type: str


@dataclass(frozen=True)
class ExtractionResult:
    ok: bool
    doc_type: str
    fields: dict[str, str] = field(default_factory=dict)
    error: str = ""


@dataclass(frozen=True)
class IntakeOutcome:
    decision: Decision
    final_type: str | None
    extraction: ExtractionResult | None
    path: str                    # readable trace of what happened


@dataclass(frozen=True)
class EvalReport:
    model_version: str
    golden_version: str
    n: int
    accuracy: float
    recall: dict[str, float]
    precision: dict[str, float]
    ece: float                   # expected calibration error
    coverage: float              # share auto-routed at the threshold
    auto_error: float            # error rate on the auto-routed share
    threshold: float


def doc_hash(text: str) -> str:
    return hashlib.sha256(" ".join(text.lower().split()).encode()).hexdigest()


def now() -> datetime:
    return datetime.now(timezone.utc)


def normalise_distribution(probs: dict[str, float]) -> dict[str, float]:
    """Return a distribution over exactly DOC_TYPES that sums to 1."""
    clean = {t: max(0.0, float(probs.get(t, 0.0))) for t in DOC_TYPES}
    z = sum(clean.values())
    if z <= 0:
        return {t: 1.0 / len(DOC_TYPES) for t in DOC_TYPES}
    return {t: v / z for t, v in clean.items()}
