"""Intake: Laya decision, confidence gate, fallback, extraction and label capture."""

from __future__ import annotations

from ..domain import Decision, Document, ExtractionResult, IntakeOutcome, LabelSource
from ..ports import Extractor, FallbackClassifier, ModelRegistry, ReviewQueue, TextStore, Tracer
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
                 texts: TextStore, store: LabelStoreService, review: ReviewQueue, threshold: float,
                 tracer: Tracer) -> None:
        self._models, self._fallback, self._router = models, fallback, router
        self._texts, self._store, self._review = texts, store, review
        self.threshold = threshold
        self._tracer = tracer

    def process(self, doc: Document) -> IntakeOutcome:
        with self._tracer.span("intake.document", doc_id=doc.doc_id, tenant_id=doc.tenant_id,
                               template_group=doc.template_group) as span:
            out = self._process(doc)
            span.set(decision_id=out.decision.decision_id, final_type=out.final_type or "none", path=out.path)
            return out

    def _process(self, doc: Document) -> IntakeOutcome:
        model = self._models.current()
        with self._tracer.span("model.predict", model_version=model.version) as span:
            probs = model.predict(doc.text)
            span.set(probabilities=probs)
        uri = self._texts.put(doc.tenant_id, doc.text)
        with self._tracer.span("gate", threshold=self.threshold) as span:
            d = self._store.record_decision(doc=doc, input_uri=uri, model_version=model.version,
                                            probabilities=probs, threshold=self.threshold)
            span.set(decision_id=d.decision_id, doc_hash=d.doc_hash, predicted=d.predicted,
                     confidence=d.confidence, route=d.route, audited=d.audited)
        trace = [f"{d.predicted} {d.confidence:.2f}"]
        if d.audited:
            self._push_review(d, "audit sample")
            trace.append("audit queued")

        if d.route == "auto":
            doc_type = d.predicted
            trace.append("auto")
        else:
            with self._tracer.span("fallback.classify", actor=self._fallback.actor) as span:
                doc_type = self._fallback.classify(doc.text)
                self._store.add_label(d.decision_id, doc_type, LabelSource.LLM_FALLBACK, self._fallback.actor)
                span.set(doc_type=doc_type, agrees_with_model=doc_type == d.predicted)
                span.event("label", source=LabelSource.LLM_FALLBACK.name, doc_type=doc_type)
            trace.append(f"fallback -> {doc_type}")

        if doc_type == "other":
            self._push_review(d, "typed as other")
            trace.append("review: other")
            return IntakeOutcome(d, None, None, " | ".join(trace))

        with self._tracer.span("extract", doc_type=doc_type) as span:
            first, recovered = self._router.extract(doc, doc_type)
            span.set(ok=first is not None and first.ok, error=first.error if first else "no extractor",
                     recovered_type=recovered.doc_type if recovered else None)
            if recovered is not None:
                span.event("label", source=LabelSource.DOWNSTREAM.name, doc_type=recovered.doc_type)
        if first is not None and first.ok:
            trace.append(f"extract {doc_type} ok")
            return IntakeOutcome(d, doc_type, first, " | ".join(trace))
        if recovered is not None:
            self._store.add_label(d.decision_id, recovered.doc_type, LabelSource.DOWNSTREAM,
                                  f"{recovered.doc_type}-extractor", f"{doc_type} schema failed")
            trace.append(f"{doc_type} schema failed, {recovered.doc_type} accepted")
            return IntakeOutcome(d, recovered.doc_type, recovered, " | ".join(trace))
        self._push_review(d, "no extractor accepted")
        trace.append("review: no extractor accepted")
        return IntakeOutcome(d, None, first, " | ".join(trace))

    def _push_review(self, d: Decision, reason: str) -> None:
        with self._tracer.span("review.queue", decision_id=d.decision_id, reason=reason):
            self._review.push(d, reason)
