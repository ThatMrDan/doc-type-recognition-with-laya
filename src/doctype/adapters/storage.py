"""Storage adapters.

In-memory versions back the demo and tests. The Jsonl* and File* versions
persist each run under var/ so you can inspect the decision log, labels and
snapshot manifests afterwards. In production these become Iceberg tables in the
tenant's lakehouse, a versioned S3 prefix for the golden set, and S3 manifests.
"""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from enum import Enum
from pathlib import Path

from ..domain import Decision, EvalReport, GoldenExample, Label, Snapshot, doc_hash
from ..ports import DecisionModel


def _jsonable(obj):
    if dataclasses.is_dataclass(obj):
        return {k: _jsonable(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.name
    return obj


def to_json(obj) -> str:
    return json.dumps(_jsonable(obj))


class InMemoryTextStore:
    def __init__(self) -> None:
        self._rows: dict[str, str] = {}

    def put(self, tenant_id: str, text: str) -> str:
        uri = f"s3://{tenant_id}-laya-inputs/{doc_hash(text)[:16]}.txt"
        self._rows[uri] = text
        return uri

    def get(self, uri: str) -> str:
        return self._rows[uri]


class InMemoryDecisionLog:
    def __init__(self) -> None:
        self._rows: dict[str, Decision] = {}

    def append(self, decision: Decision) -> None:
        if decision.decision_id in self._rows:
            raise ValueError("decision log is append-only")
        self._rows[decision.decision_id] = decision

    def get(self, decision_id: str) -> Decision:
        return self._rows[decision_id]

    def all_for_tenant(self, tenant_id: str) -> list[Decision]:
        return [d for d in self._rows.values() if d.tenant_id == tenant_id]


class JsonlDecisionLog(InMemoryDecisionLog):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, decision: Decision) -> None:
        super().append(decision)
        with self._path.open("a") as f:
            f.write(to_json(decision) + "\n")


class InMemoryLabelRepository:
    def __init__(self) -> None:
        self._rows: list[Label] = []

    def add(self, label: Label) -> None:
        self._rows.append(label)

    def for_decision(self, decision_id: str) -> list[Label]:
        return [l for l in self._rows if l.decision_id == decision_id]


class JsonlLabelRepository(InMemoryLabelRepository):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, label: Label) -> None:
        super().add(label)
        with self._path.open("a") as f:
            f.write(to_json(label) + "\n")


class StaticGoldenSet:
    def __init__(self, version: str, examples: list[GoldenExample]) -> None:
        self._version, self._examples = version, tuple(examples)
        self._hashes = frozenset(doc_hash(e.text) for e in examples)
        self._groups = frozenset(e.template_group for e in examples)

    @classmethod
    def from_jsonl(cls, path: Path) -> "StaticGoldenSet":
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        return cls(path.stem, [GoldenExample(r["text"], r["template_group"], r["doc_type"]) for r in rows])

    def version(self) -> str:
        return self._version

    def examples(self) -> tuple[GoldenExample, ...]:
        return self._examples

    def doc_hashes(self) -> frozenset[str]:
        return self._hashes

    def template_groups(self) -> frozenset[str]:
        return self._groups


class InMemorySnapshotStore:
    def __init__(self) -> None:
        self._rows: dict[str, Snapshot] = {}

    def write(self, snapshot: Snapshot) -> str:
        uri = f"s3://{snapshot.tenant_id}-label-store/snapshots/{snapshot.snapshot_id}/manifest.json"
        self._rows[uri] = snapshot
        return uri

    def read(self, uri: str) -> Snapshot:
        return self._rows[uri]


class FileSnapshotStore(InMemorySnapshotStore):
    def __init__(self, root: Path) -> None:
        super().__init__()
        self._root = root

    def write(self, snapshot: Snapshot) -> str:
        path = self._root / snapshot.tenant_id / "snapshots" / snapshot.snapshot_id / "manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_jsonable(snapshot), indent=2))
        uri = str(path)
        self._rows[uri] = snapshot
        return uri


class InMemoryModelRegistry:
    def __init__(self, initial: DecisionModel) -> None:
        self._models = {initial.version: initial}
        self._current = initial.version
        self.history: list[tuple[str, EvalReport, str]] = []

    def current(self) -> DecisionModel:
        return self._models[self._current]

    def register(self, model: DecisionModel, report: EvalReport, snapshot_uri: str) -> None:
        self._models[model.version] = model
        self.history.append((model.version, report, snapshot_uri))

    def promote(self, version: str) -> None:
        self._current = version


class InMemoryReviewQueue:
    def __init__(self) -> None:
        self._items: list[tuple[Decision, str]] = []

    def push(self, decision: Decision, reason: str) -> None:
        self._items.append((decision, reason))

    def drain(self) -> list[tuple[Decision, str]]:
        items, self._items = self._items, []
        return items
