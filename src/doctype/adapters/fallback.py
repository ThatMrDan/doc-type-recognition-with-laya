"""LLM fallback classifiers for low-confidence documents.

OllamaFallback   local, free, offline. Uses Ollama's JSON-schema structured output.
BedrockFallback  production path. Uses the Converse API so any Bedrock text model works.

Both return one of DOC_TYPES and degrade to "other" on unparseable output, so a
bad answer goes to human review rather than to the wrong extractor.
"""

from __future__ import annotations

import json
import re
import urllib.request

from ..domain import CRITERIA, DOC_TYPES

SYSTEM_PROMPT = (
    "You classify documents from specialty insurance submissions. "
    "Choose exactly one type:\n"
    + "\n".join(f"- {k}: {v}" for k, v in CRITERIA.items())
    + '\nReply with JSON only, for example {"doc_type": "sov"}.'
)

SCHEMA = {
    "type": "object",
    "properties": {"doc_type": {"type": "string", "enum": list(DOC_TYPES)}},
    "required": ["doc_type"],
}


def parse_doc_type(raw: str) -> str:
    match = re.search(r"\{.*?\}", raw, re.S)
    if match:
        try:
            value = json.loads(match.group(0)).get("doc_type")
            if value in DOC_TYPES:
                return value
        except json.JSONDecodeError:
            pass
    return "other"


class OllamaFallback:
    def __init__(self, model: str = "qwen3:4b", host: str = "http://localhost:11434", timeout: float = 60) -> None:
        self.actor = f"ollama:{model}"
        self._model, self._url, self._timeout = model, host.rstrip("/") + "/api/chat", timeout

    def classify(self, text: str) -> str:
        body = {
            "model": self._model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}],
            "format": SCHEMA,
            "stream": False,
            "think": False,
            "options": {"temperature": 0},
        }
        req = urllib.request.Request(self._url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:
            payload = json.loads(resp.read())
        return parse_doc_type(payload.get("message", {}).get("content", ""))


class BedrockFallback:
    def __init__(self, model_id: str = "amazon.nova-micro-v1:0", region: str = "eu-west-2") -> None:
        import boto3

        self.actor = f"bedrock:{model_id}"
        self._model_id = model_id
        self._client = boto3.client("bedrock-runtime", region_name=region)

    def classify(self, text: str) -> str:
        resp = self._client.converse(
            modelId=self._model_id,
            system=[{"text": SYSTEM_PROMPT}],
            messages=[{"role": "user", "content": [{"text": text}]}],
            inferenceConfig={"temperature": 0, "maxTokens": 50},
        )
        parts = resp["output"]["message"]["content"]
        return parse_doc_type("".join(p.get("text", "") for p in parts))
