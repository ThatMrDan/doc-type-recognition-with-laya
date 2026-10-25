"""Schema-checked extractors. Each accepts a document only if its required fields are found.

These are regex stand-ins for the real SOV, loss run, ACORD and email extractors.
What matters for the label store is the contract: ok=False means "not my type".
"""

from __future__ import annotations

import re

from ..domain import Document, ExtractionResult
from ..ports import Extractor


class SchemaExtractor:
    def __init__(self, doc_type: str, required: dict[str, str]) -> None:
        self.doc_type = doc_type
        self._required = {k: re.compile(v, re.I) for k, v in required.items()}

    def extract(self, doc: Document) -> ExtractionResult:
        fields, missing = {}, []
        for name, pat in self._required.items():
            m = pat.search(doc.text)
            if m:
                fields[name] = m.group(1) if m.groups() else m.group(0)
            else:
                missing.append(name)
        if missing:
            return ExtractionResult(False, self.doc_type, error=f"missing {', '.join(missing)}")
        return ExtractionResult(True, self.doc_type, fields)


def default_extractors() -> list[Extractor]:
    return [
        SchemaExtractor("sov", {"tiv": r"tiv\s*[:=]?\s*([\d,.]+\s*[mk]?)", "locations": r"(\d+)\s+locations?"}),
        SchemaExtractor("loss_run", {"years": r"(\d+|one|two|three|four|five|six|seven|ten)\s*(?:yr|year)",
                                     "incurred": r"incurred\s*[:=]?\s*([\d,.]+\s*[mk]?)"}),
        SchemaExtractor("acord", {"form": r"acord\s*(\d{2,3})"}),
        SchemaExtractor("broker_email", {"sender": r"from:\s*(\S+)"}),
    ]
