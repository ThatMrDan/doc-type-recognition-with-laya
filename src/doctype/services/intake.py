"""Intake: Laya decision, confidence gate, fallback, extraction and label capture."""

from __future__ import annotations

from ..domain import Document, ExtractionResult, IntakeOutcome, LabelSource
from ..ports import Extractor, FallbackClassifier, ModelRegistry, ReviewQueue, TextStore
from .label_store import LabelStoreService


class ExtractionRouter:
    """Runs the typed extractor; on schema failure tries the others to find the real type."""

    def __init__(self, extractors: list[Extractor]) -> None:
        self._by_type = {e.doc_type: e for e in extractors}

    def extract(self, doc: Document, doc_type: str) -> tuple[ExtractionResult | None, ExtractionResult | None]:
        """Returns (first attempt, recovered result if a different extractor accepted it)."""
        primary = self._by_type.get(doc_type)
        if primary is None:
            return None, None
        first = primary.extract(doc)
        if first.ok:
            return first, None
        for t, ext in self._by_type.items():
            if t != doc_type:
                alt = ext.extract(doc)
                if alt.ok:
                    return first, alt
        return first, None


class IntakeService:
    def __init__(self, models: ModelRegistry, fallback: FallbackClassifier, router: ExtractionRouter,
                 texts: TextStore, store: LabelStoreService, review: ReviewQueue, threshold: float) -> None:
        self._models, self._fallback, self._router = models, fallback, router
        self._texts, self._store, self._review = texts, store, review
        self.threshold = threshold

    def process(self, doc: Document) -> IntakeOutcome:
        model = self._models.current()
        probs = model.predict(doc.text)
        uri = self._texts.put(doc.tenant_id, doc.text)
        d = self._store.record_decision(doc=doc, input_uri=uri, model_version=model.version,
                                        probabilities=probs, threshold=self.threshold)
        trace = [f"{d.predicted} {d.confidence:.2f}"]

        if d.route == "auto":
            doc_type = d.predicted
            trace.append("auto")
            if d.audited:
                self._review.push(d, "audit sample")
                trace.append("audit queued")
        else:
            doc_type = self._fallback.classify(doc.text)
            self._store.add_label(d.decision_id, doc_type, LabelSource.LLM_FALLBACK, self._fallback.actor)
            trace.append(f"fallback -> {doc_type}")

        if doc_type == "other":
            self._review.push(d, "typed as other")
            trace.append("review: other")
            return IntakeOutcome(d, None, None, " | ".join(trace))

        first, recovered = self._router.extract(doc, doc_type)
        if first is not None and first.ok:
            trace.append(f"extract {doc_type} ok")
            return IntakeOutcome(d, doc_type, first, " | ".join(trace))
        if recovered is not None:
            self._store.add_label(d.decision_id, recovered.doc_type, LabelSource.DOWNSTREAM,
                                  f"{recovered.doc_type}-extractor", f"{doc_type} schema failed")
            trace.append(f"{doc_type} schema failed, {recovered.doc_type} accepted")
            return IntakeOutcome(d, recovered.doc_type, recovered, " | ".join(trace))
        self._review.push(d, "no extractor accepted")
        trace.append("review: no extractor accepted")
        return IntakeOutcome(d, None, first, " | ".join(trace))
