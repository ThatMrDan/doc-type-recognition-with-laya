"""Golden set evaluation and the promotion gate."""

from __future__ import annotations

from dataclasses import dataclass

from ..domain import DOC_TYPES, EvalReport
from ..ports import DecisionModel, GoldenSetRegistry


class EvalService:
    def __init__(self, golden: GoldenSetRegistry, bins: int = 10) -> None:
        self._golden, self._bins = golden, bins

    def evaluate(self, model: DecisionModel, threshold: float) -> EvalReport:
        rows = [(model.predict(g.text), g.doc_type) for g in self._golden.examples()]
        preds = [(max(p, key=p.get), max(p.values()), y) for p, y in rows]
        n = len(preds)
        correct = [pred == y for pred, _, y in preds]

        recall, precision = {}, {}
        for t in DOC_TYPES:
            actual = [c for (_, _, y), c in zip(preds, correct) if y == t]
            predicted = [c for (pred, _, _), c in zip(preds, correct) if pred == t]
            if actual:
                recall[t] = sum(actual) / len(actual)
            if predicted:
                precision[t] = sum(predicted) / len(predicted)

        ece = 0.0
        for b in range(self._bins):
            lo, hi = b / self._bins, (b + 1) / self._bins
            idx = [i for i, (_, conf, _) in enumerate(preds) if lo < conf <= hi]
            if idx:
                acc = sum(correct[i] for i in idx) / len(idx)
                conf = sum(preds[i][1] for i in idx) / len(idx)
                ece += len(idx) / n * abs(acc - conf)

        auto = [c for (_, conf, _), c in zip(preds, correct) if conf >= threshold]
        return EvalReport(
            model_version=model.version, golden_version=self._golden.version(), n=n,
            accuracy=sum(correct) / n, recall=recall, precision=precision, ece=ece,
            coverage=len(auto) / n, auto_error=(1 - sum(auto) / len(auto)) if auto else 0.0,
            threshold=threshold,
        )


@dataclass(frozen=True)
class PromotionPolicy:
    max_recall_drop: float = 0.05
    max_ece_increase: float = 0.02

    def decide(self, current: EvalReport, candidate: EvalReport) -> tuple[bool, list[str]]:
        reasons = []
        if candidate.accuracy < current.accuracy:
            reasons.append(f"accuracy {candidate.accuracy:.2f} < {current.accuracy:.2f}")
        for t, r in current.recall.items():
            cr = candidate.recall.get(t, 0.0)
            if r - cr > self.max_recall_drop:
                reasons.append(f"{t} recall dropped {r:.2f} -> {cr:.2f}")
        if candidate.ece - current.ece > self.max_ece_increase:
            reasons.append(f"ECE worsened {current.ece:.3f} -> {candidate.ece:.3f}")
        return not reasons, reasons
