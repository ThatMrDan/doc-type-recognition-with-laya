import random

import pytest

from doctype.adapters.extractors import default_extractors
from doctype.adapters.simulated import SimulatedFallback, SimulatedLaya, SimulatedTrainer
from doctype.adapters.storage import (
    InMemoryDecisionLog, InMemoryLabelRepository, InMemoryModelRegistry, InMemoryReviewQueue,
    InMemorySnapshotStore, InMemoryTextStore, StaticGoldenSet,
)
from doctype.adapters.tracing import NullTracer
from doctype.domain import GoldenExample
from doctype.services import (
    EvalService, ExtractionRouter, IntakeService, LabelStoreService, PromotionPolicy, TrainingPipeline,
)

GOLDEN = [
    GoldenExample("Statement of values: 14 locations, total TIV 82.4m", "g-sov", "sov"),
    GoldenExample("Loss history 3 yr incurred 410k", "g-loss", "loss_run"),
    GoldenExample("ACORD 125 commercial application", "g-acord", "acord"),
    GoldenExample("From: a@b.com Fwd: renewal, regards", "g-email", "broker_email"),
    GoldenExample("Engineering survey photos", "g-other", "other"),
]


class Wired:
    def __init__(self, audit_rate: float = 0.0, threshold: float = 0.85, tracer=None):
        self.tracer = tracer or NullTracer()
        self.texts = InMemoryTextStore()
        self.golden = StaticGoldenSet("golden-test", GOLDEN)
        self.snapshots = InMemorySnapshotStore()
        self.models = InMemoryModelRegistry(SimulatedLaya("sim-v1"))
        self.review = InMemoryReviewQueue()
        self.store = LabelStoreService(InMemoryDecisionLog(), InMemoryLabelRepository(), self.golden,
                                       self.snapshots, audit_rate=audit_rate, rng=random.Random(1))
        self.intake = IntakeService(self.models, SimulatedFallback(), ExtractionRouter(default_extractors()),
                                    self.texts, self.store, self.review, threshold, self.tracer)
        self.evals = EvalService(self.golden)
        self.pipeline = TrainingPipeline(self.store, self.snapshots, self.texts, SimulatedTrainer(),
                                         self.models, self.evals, PromotionPolicy(), self.tracer)


@pytest.fixture
def wired():
    return Wired()


@pytest.fixture
def audit_everything():
    return Wired(audit_rate=1.0)
