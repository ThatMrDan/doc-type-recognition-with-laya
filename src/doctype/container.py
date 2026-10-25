"""Composition root: builds services from settings. The only place adapters are chosen."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

from .adapters.extractors import default_extractors
from .adapters.simulated import SimulatedFallback, SimulatedLaya, SimulatedTrainer
from .adapters.storage import (
    FileSnapshotStore, InMemoryModelRegistry, InMemoryReviewQueue, InMemoryTextStore,
    JsonlDecisionLog, JsonlLabelRepository, StaticGoldenSet,
)
from .config import Settings
from .adapters.tracing import NullTracer
from .ports import DecisionModel, FallbackClassifier, Trainer, Tracer
from .services import (
    EvalService, ExtractionRouter, IntakeService, LabelStoreService, PromotionPolicy, TrainingPipeline,
)


def build_model(s: Settings) -> DecisionModel:
    if s.model == "laya":
        from .adapters.laya_model import LayaModel
        return LayaModel(s.laya_repo, s.laya_subfolder or None)
    if s.model == "simulated":
        return SimulatedLaya("simulated-v1")
    raise ValueError(f"unknown model {s.model!r}")


def build_fallback(s: Settings) -> FallbackClassifier:
    if s.fallback == "ollama":
        from .adapters.fallback import OllamaFallback
        return OllamaFallback(s.ollama_model, s.ollama_host)
    if s.fallback == "bedrock":
        from .adapters.fallback import BedrockFallback
        return BedrockFallback(s.bedrock_model_id, s.aws_region)
    if s.fallback == "simulated":
        return SimulatedFallback()
    raise ValueError(f"unknown fallback {s.fallback!r}")


def build_trainer(s: Settings) -> Trainer:
    if s.trainer == "simulated":
        if s.model != "simulated":
            raise ValueError("the simulated trainer only fine-tunes the simulated model; use export or laya")
        return SimulatedTrainer()
    from .adapters.laya_trainer import ExportTrainer, LayaTrainer
    if s.trainer == "export":
        return ExportTrainer(s.laya_output_dir)
    if s.trainer == "laya":
        return LayaTrainer(s.laya_base, s.laya_output_dir, s.laya_device)
    raise ValueError(f"unknown trainer {s.trainer!r}")


def build_tracer(s: Settings, run_dir: Path) -> Tracer:
    if s.trace == "otel":
        try:
            from .adapters.tracing import OtelTracer
            return OtelTracer(run_dir / "trace.json")
        except ImportError as e:
            raise RuntimeError("tracing needs the trace extra: uv sync --extra trace, or set DOCTYPE_TRACE=off") from e
    if s.trace == "off":
        return NullTracer()
    raise ValueError(f"unknown trace {s.trace!r}")


@dataclass
class App:
    settings: Settings
    run_dir: Path
    golden: StaticGoldenSet
    texts: InMemoryTextStore
    models: InMemoryModelRegistry
    review: InMemoryReviewQueue
    store: LabelStoreService
    intake: IntakeService
    evals: EvalService
    pipeline: TrainingPipeline
    tracer: Tracer


def build_app(s: Settings, run_dir: Path, seed: int = 7) -> App:
    tracer = build_tracer(s, run_dir)
    golden = StaticGoldenSet.from_jsonl(Path(s.data_dir) / "golden" / "golden-v1.jsonl")
    texts = InMemoryTextStore()
    snapshots = FileSnapshotStore(run_dir)
    models = InMemoryModelRegistry(build_model(s))
    review = InMemoryReviewQueue()
    store = LabelStoreService(JsonlDecisionLog(run_dir / "decisions.jsonl"),
                              JsonlLabelRepository(run_dir / "labels.jsonl"),
                              golden, snapshots, audit_rate=s.audit_rate, rng=random.Random(seed))
    intake = IntakeService(models, build_fallback(s), ExtractionRouter(default_extractors()),
                           texts, store, review, s.threshold, tracer)
    evals = EvalService(golden)
    pipeline = TrainingPipeline(store, snapshots, texts, build_trainer(s), models, evals, PromotionPolicy(), tracer)
    return App(s, run_dir, golden, texts, models, review, store, intake, evals, pipeline, tracer)
