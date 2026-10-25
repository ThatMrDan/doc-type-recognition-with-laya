import json

import pytest

from doctype.domain import Document

pytest.importorskip("opentelemetry.sdk")
from doctype.adapters.tracing import OtelTracer  # noqa: E402


def test_spans_nest_in_start_order_with_flat_attributes(tmp_path):
    tracer = OtelTracer(tmp_path / "trace.json")
    with tracer.span("run", tenant="t1"):
        with tracer.span("first", probabilities={"sov": 0.7, "other": 0.3}) as s:
            s.event("label", source="HUMAN")
        with tracer.span("second", missing=None):
            pass
    [root] = json.loads(open(tracer.close()).read())
    assert root["name"] == "run" and root["attributes"] == {"tenant": "t1"}
    assert [c["name"] for c in root["children"]] == ["first", "second"]
    first = root["children"][0]
    assert first["attributes"] == {"probabilities.sov": 0.7, "probabilities.other": 0.3}
    assert first["events"] == [{"name": "label", "attributes": {"source": "HUMAN"}}]
    assert root["children"][1]["attributes"] == {}


def test_failed_step_is_marked_as_error(tmp_path):
    tracer = OtelTracer(tmp_path / "trace.json")
    with pytest.raises(RuntimeError):
        with tracer.span("boom"):
            raise RuntimeError("ollama down")
    [root] = json.loads(open(tracer.close()).read())
    assert root["status"] == "ERROR"
    assert root["events"][0]["name"] == "exception"


def test_intake_trace_shows_each_step_of_a_fallback_document(tmp_path):
    from conftest import Wired
    tracer = OtelTracer(tmp_path / "trace.json")
    w = Wired(audit_rate=1.0, tracer=tracer)
    w.intake.process(Document("1", "t1", "ACORD 125 application commercial", "acord-125"))
    [doc] = json.loads(open(tracer.close()).read())
    assert doc["name"] == "intake.document"
    assert [c["name"] for c in doc["children"]] == [
        "model.predict", "gate", "review.queue", "fallback.classify", "extract"]
    gate = doc["children"][1]["attributes"]
    assert gate["route"] == "fallback" and gate["audited"] is True
    assert doc["children"][3]["attributes"]["doc_type"] == "acord"
    assert doc["attributes"]["final_type"] == "acord"
