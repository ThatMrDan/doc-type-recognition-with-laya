"""Calibration and threshold tuning, both fitted on the random human audit sample.

Laya's checkpoints ship over-confident (per ConvAI's model card), so refit a
temperature on your own labelled data before trusting the gate. Never fit
either of these on the golden set: it is the exam, not the textbook.
"""

from __future__ import annotations

import math

from ..domain import Decision, normalise_distribution
from ..ports import DecisionModel


class CalibratedModel:
    """Wraps any DecisionModel with temperature scaling: p_i ∝ p_i ** (1 / T)."""

    def __init__(self, inner: DecisionModel, temperature: float) -> None:
        self._inner, self.temperature = inner, temperature
        self.version = f"{inner.version}+T{temperature:.2f}"

    def predict(self, text: str) -> dict[str, float]:
        return apply_temperature(self._inner.predict(text), self.temperature)


def apply_temperature(probs: dict[str, float], t: float) -> dict[str, float]:
    eps = 1e-9
    return normalise_distribution({k: math.exp(math.log(max(v, eps)) / t) for k, v in probs.items()})


def fit_temperature(labelled: list[tuple[Decision, str]],
                    grid: tuple[float, ...] = tuple(round(0.5 + 0.1 * i, 2) for i in range(36))) -> float:
    """Temperature minimising negative log-likelihood on human-labelled decisions."""
    if not labelled:
        return 1.0

    def nll(t: float) -> float:
        return -sum(math.log(max(apply_temperature(d.probabilities, t).get(y, 0.0), 1e-9))
                    for d, y in labelled) / len(labelled)

    return min(grid, key=nll)


def tune_threshold(audited: list[tuple[Decision, str]], max_auto_error: float,
                   grid: tuple[float, ...] = (0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95)) -> float | None:
    """Lowest threshold whose auto-path error stays within budget on the audit sample."""
    for t in sorted(grid):
        auto = [(d, y) for d, y in audited if d.confidence >= t]
        if auto and sum(d.predicted != y for d, y in auto) / len(auto) <= max_auto_error:
            return t
    return None
