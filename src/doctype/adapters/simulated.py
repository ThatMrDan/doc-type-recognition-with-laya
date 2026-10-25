"""Deterministic stand-ins so the whole flow runs offline with no model weights.

SimulatedLaya     keyword scores + learned token weights, softmaxed
SimulatedTrainer  "fine-tunes" by learning token weights from the snapshot
SimulatedFallback rule-based stand-in for an LLM, right most of the time
"""

from __future__ import annotations

import math
import re
from collections import defaultdict

from ..domain import DOC_TYPES, Snapshot
from ..ports import DecisionModel, TextStore

_TOKEN = re.compile(r"[a-z0-9:]+")


def tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class SimulatedLaya:
    BASE = {
        "sov": {"schedule": 1.2, "values": 1.2, "tiv": 1.6, "location": 0.8},
        "loss_run": {"loss": 1.4, "claims": 1.0, "incurred": 1.4},
        "acord": {"acord": 2.2, "form": 0.6},
        "broker_email": {"fwd:": 1.4, "re:": 1.2, "attached": 0.8, "regards": 0.8},
        "other": {},
    }

    def __init__(self, version: str = "simulated-v1", learned: dict[str, dict[str, float]] | None = None,
                 temperature: float = 0.9) -> None:
        self.version = version
        self.learned = learned or {}
        self._temp = temperature

    def predict(self, text: str) -> dict[str, float]:
        toks = tokens(text)
        scores = {}
        for t in DOC_TYPES:
            s = 0.3 if t == "other" else 0.0
            s += sum(self.BASE[t].get(tok, 0.0) for tok in toks)
            s += sum(self.learned.get(tok, {}).get(t, 0.0) for tok in toks)
            scores[t] = s / self._temp
        m = max(scores.values())
        exp = {t: math.exp(v - m) for t, v in scores.items()}
        z = sum(exp.values())
        return {t: v / z for t, v in exp.items()}


class SimulatedTrainer:
    """Reads only what the snapshot manifest lists."""

    def __init__(self, lr: float = 0.9) -> None:
        self._lr = lr

    def fine_tune(self, base: DecisionModel, snapshot: Snapshot, texts: TextStore,
                  new_version: str) -> DecisionModel | None:
        learned: dict[str, dict[str, float]] = defaultdict(dict)
        for tok, per_type in getattr(base, "learned", {}).items():
            learned[tok].update(per_type)
        for ex in snapshot.examples:
            for tok in set(tokens(texts.get(ex.input_uri))):
                if tok in SimulatedLaya.BASE.get(ex.doc_type, {}):
                    continue
                learned[tok][ex.doc_type] = learned[tok].get(ex.doc_type, 0.0) + self._lr * ex.weight
        return SimulatedLaya(new_version, dict(learned))


class SimulatedFallback:
    actor = "simulated-llm"
    RULES = (("acord", "acord"), ("tiv", "sov"), ("schedule of values", "sov"), ("sov", "sov"),
             ("loss run", "loss_run"), ("losses", "loss_run"), ("claims", "loss_run"),
             ("fwd:", "broker_email"), ("re:", "broker_email"), ("dear", "broker_email"))

    def classify(self, text: str) -> str:
        low = text.lower()
        for needle, t in self.RULES:
            if needle in low:
                return t
        return "other"
