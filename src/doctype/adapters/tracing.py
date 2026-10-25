"""Tracers: OpenTelemetry spans written as one nested trace.json per run, or nothing at all."""

from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


class _NullSpan:
    def set(self, **attributes: object) -> None:
        pass

    def event(self, name: str, **attributes: object) -> None:
        pass


class NullTracer:
    @contextmanager
    def span(self, name: str, **attributes: object) -> Iterator[_NullSpan]:
        yield _NullSpan()

    def close(self) -> None:
        return None


def _flatten(attributes: dict[str, object], prefix: str = "") -> dict[str, object]:
    """OTel attributes are flat primitives, so {"p": {"sov": 0.4}} becomes {"p.sov": 0.4}."""
    out: dict[str, object] = {}
    for k, v in attributes.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(_flatten(v, f"{key}."))
        elif v is None:
            continue
        elif isinstance(v, (str, bool, int, float)):
            out[key] = v
        else:
            out[key] = str(v)
    return out


class _OtelSpan:
    def __init__(self, span) -> None:
        self._span = span

    def set(self, **attributes: object) -> None:
        self._span.set_attributes(_flatten(attributes))

    def event(self, name: str, **attributes: object) -> None:
        self._span.add_event(name, _flatten(attributes))


class OtelTracer:
    """Collects spans in memory and writes them as a time-ordered tree when closed."""

    def __init__(self, path: Path, service: str = "doctype") -> None:
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
        self._path = path
        self._exporter = InMemorySpanExporter()
        self._provider = TracerProvider(resource=Resource.create({"service.name": service}))
        self._provider.add_span_processor(SimpleSpanProcessor(self._exporter))
        self._tracer = self._provider.get_tracer("doctype")

    @contextmanager
    def span(self, name: str, **attributes: object) -> Iterator[_OtelSpan]:
        with self._tracer.start_as_current_span(name, attributes=_flatten(attributes)) as s:
            yield _OtelSpan(s)

    def close(self) -> str:
        spans = self._exporter.get_finished_spans()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(span_tree(spans), indent=2))
        self._provider.shutdown()
        return str(self._path)


def span_tree(spans) -> list[dict]:
    """Finished spans arrive child first; rebuild parent -> children, each level ordered by start."""
    nodes, children = {}, {}
    for s in spans:
        sid = s.context.span_id
        nodes[sid] = {
            "name": s.name,
            "trace_id": f"{s.context.trace_id:032x}",
            "span_id": f"{sid:016x}",
            "start": datetime.fromtimestamp(s.start_time / 1e9, timezone.utc).isoformat(),
            "_start_ns": s.start_time,
            "duration_ms": round((s.end_time - s.start_time) / 1e6, 3),
            "status": s.status.status_code.name,
            "attributes": dict(s.attributes or {}),
            "events": [{"name": e.name, "attributes": dict(e.attributes or {})} for e in s.events],
        }
        children.setdefault(s.parent.span_id if s.parent else None, []).append(sid)

    def build(sid: int) -> dict:
        node = nodes[sid]
        kids = sorted(children.get(sid, []), key=lambda k: nodes[k]["_start_ns"])
        node["children"] = [build(k) for k in kids]
        del node["_start_ns"]
        if node["status"] == "UNSET":
            del node["status"]
        if not node["events"]:
            del node["events"]
        return node

    roots = sorted((sid for sid in children.get(None, [])), key=lambda k: nodes[k]["_start_ns"])
    return [build(r) for r in roots]
