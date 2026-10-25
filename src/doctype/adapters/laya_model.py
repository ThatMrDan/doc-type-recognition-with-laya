"""Real Laya decision model.

Uses the documented SDK surface from the laya package (0.4.x):
    agent = laya.load("convaiinnovations/laya", subfolder="typed-decisions")
    result = agent.predict(state, questions)
    result["answers"][qid] -> {"choice", "probabilities", "confidence", "answer_confidence", ...}

For a choice question, laya 0.4.15 returns "probabilities" as a dict keyed by
label (4 dp) and "answer_confidence" as max(p), the calibrated quantity to gate
on. _to_distribution also accepts a list or a bare choice, in case a later
release changes shape. `doctype probe` prints the raw answer.
"""

from __future__ import annotations

import os
from typing import Any

from ..domain import CRITERIA, DOC_TYPES, normalise_distribution

QUESTION_ID = "doc_type"
QUESTIONS: dict[str, Any] = {
    QUESTION_ID: {
        "type": "choice",
        "instructions": "Which type of insurance submission document is this?",
        "criteria": dict(CRITERIA),
    }
}


class LayaModel:
    def __init__(self, repo: str = "convaiinnovations/laya", subfolder: str | None = "typed-decisions",
                 version: str | None = None, local_dir: str | None = None) -> None:
        os.environ.setdefault("USE_TF", "0")   # the model card's fix for laya.load hanging
        import laya  # imported lazily so the rest of the project runs without it

        if local_dir:
            self._agent = laya.load(local_dir)
        elif subfolder:
            self._agent = laya.load(repo, subfolder=subfolder)
        else:
            self._agent = laya.load(repo)
        self.version = version or (local_dir or f"{repo}/{subfolder or 'english'}")

    def raw(self, text: str) -> dict[str, Any]:
        return self._agent.predict(text, QUESTIONS)

    def predict(self, text: str) -> dict[str, float]:
        return _to_distribution(self.raw(text)["answers"][QUESTION_ID])


def _to_distribution(answer: dict[str, Any]) -> dict[str, float]:
    probs = answer.get("probabilities")
    if isinstance(probs, dict):
        return normalise_distribution(probs)
    if isinstance(probs, (list, tuple)) and len(probs) == len(DOC_TYPES):
        if probs and isinstance(probs[0], (list, tuple)):          # [(label, p), ...]
            return normalise_distribution({str(k): float(v) for k, v in probs})
        return normalise_distribution(dict(zip(DOC_TYPES, map(float, probs))))
    # Fall back to the chosen label and its probability, spreading the rest evenly.
    choice = answer.get("choice")
    p = float(answer.get("answer_confidence", answer.get("confidence", 0.0)))
    if choice not in DOC_TYPES:
        raise ValueError(f"unexpected Laya answer shape: {answer!r}")
    rest = (1 - p) / (len(DOC_TYPES) - 1)
    return normalise_distribution({t: (p if t == choice else rest) for t in DOC_TYPES})
