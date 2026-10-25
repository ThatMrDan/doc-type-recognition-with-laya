"""Training adapters for a real Laya checkpoint.

Row format follows laya.train.items_from_rows (laya 0.4.15): each JSONL row is
    {"state": text, "questions": {...}, "gold": {qid: {"probabilities": {label: p}}}}
`expected` is the hard-label alternative. The reader has no per-row weight and
ignores unknown keys, so label trust is encoded as a soft gold target: a HUMAN
label puts all its mass on the label, an LLM_FALLBACK label spreads part of it
across the other options. Provenance rides along under "meta", which Laya ignores.

ExportTrainer writes train.jsonl and returns no candidate, for inspection or for
running `laya-train --data train.jsonl --base <alias> --out <dir>` yourself.
LayaTrainer calls laya.train.finetune(data, model_dir, output_dir, config, device).
Needs a GPU or Apple Silicon (device="mps") to finish in sensible time.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..domain import DOC_TYPES, Snapshot
from ..ports import DecisionModel, TextStore
from .laya_model import QUESTION_ID, QUESTIONS, LayaModel


def soft_target(doc_type: str, weight: float) -> dict[str, float]:
    """weight 1.0 -> one-hot; lower weight moves (1 - weight) evenly onto the other options."""
    rest = (1.0 - weight) / (len(DOC_TYPES) - 1)
    return {t: (weight if t == doc_type else rest) for t in DOC_TYPES}


def export_snapshot(snapshot: Snapshot, texts: TextStore, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for ex in snapshot.examples:
            row = {
                "state": texts.get(ex.input_uri),
                "questions": QUESTIONS,
                "gold": {QUESTION_ID: {"probabilities": soft_target(ex.doc_type, ex.weight)}},
                "meta": {"decision_id": ex.decision_id, "label": ex.doc_type, "source": ex.source.name,
                         "snapshot_id": snapshot.snapshot_id, "golden_excluded": snapshot.golden_set_version},
            }
            f.write(json.dumps(row) + "\n")
    return path


class ExportTrainer:
    def __init__(self, out_dir: str = "./models") -> None:
        self._out = Path(out_dir)

    def fine_tune(self, base: DecisionModel, snapshot: Snapshot, texts: TextStore,
                  new_version: str) -> DecisionModel | None:
        path = export_snapshot(snapshot, texts, self._out / new_version / "train.jsonl")
        print(f"  exported {len(snapshot.examples)} rows to {path}")
        return None


class LayaTrainer:
    def __init__(self, base: str = "english", out_dir: str = "./models", device: str = "auto") -> None:
        self._base, self._out, self._device = base, Path(out_dir), device

    def fine_tune(self, base: DecisionModel, snapshot: Snapshot, texts: TextStore,
                  new_version: str) -> DecisionModel | None:
        from laya.train import TrainConfig, finetune

        out = self._out / new_version
        train = export_snapshot(snapshot, texts, out / "train.jsonl")
        report = finetune(str(train), self._base, str(out / "checkpoint"),
                          TrainConfig(shuffle_options=("choice",)), device=self._device)
        print(f"  laya finetune: train_items={report.get('train_items')} skipped={report.get('skipped')} "
              f"temperature={report.get('temperature')}")
        return LayaModel(version=new_version, local_dir=str(out / "checkpoint"))
