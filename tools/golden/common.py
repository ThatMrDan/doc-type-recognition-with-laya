"""Shared helpers for building golden-v2. Deliberately imports nothing from scripts/ (the training generator)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROWS = ROOT / "tools" / "golden" / "rows"
OUT = ROOT / "tools" / "golden" / "out"
GUIDELINE = ROOT / "docs" / "golden" / "guideline-v1.md"
LABELS = ("sov", "loss_run", "acord", "broker_email", "other")

# Names that occur in training data. A golden row containing one shares a rare slot value with training.
BANNED = [
    "harbourline", "kestrel", "northgate", "ashby", "blackfriars", "saltmarsh", "redcliffe", "fenwick",
    "larkspur", "tamar", "wexcombe", "aldgate", "aon", "marsh", "willis", "lockton", "howden", "ajg", "bms",
    "brindle", "copperleaf", "merrow", "ostrander", "pellow", "quarry lane", "rowan", "tillery",
    "vance & hart", "wickham", "yardley", "ebury",
    "amy", "tom", "lee", "kim", "sam", "ana", "raj", "zoe", "ben", "eve", "ola", "max", "ivy", "noah",
]
_BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)


def banned_hits(text: str) -> list[str]:
    return sorted({m.group(1).lower() for m in _BANNED_RE.finditer(text)})


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def ollama_chat(model: str, system: str, user: str, schema: dict, *, temperature: float, seed: int,
                host: str = "http://localhost:11434", timeout: float = 300) -> dict:
    body = {"model": model, "stream": False, "think": False, "format": schema,
            "options": {"temperature": temperature, "seed": seed},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request(host + "/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read())
    return json.loads(payload["message"]["content"])


def _env(name: str) -> str | None:
    import os
    if os.environ.get(name):
        return os.environ[name]
    env = ROOT / ".env"
    for line in env.read_text().splitlines() if env.exists() else []:
        k, _, v = line.partition("=")
        if k.strip() == name and v.strip():
            return v.strip().strip('"').strip("'")
    return None


def _gemini_schema(schema: dict) -> dict:
    """Gemini takes an OpenAPI subset: upper-case types, nullable instead of type lists."""
    out = {}
    t = schema.get("type")
    if isinstance(t, list):
        out["nullable"] = "null" in t
        t = next(x for x in t if x != "null")
    if t:
        out["type"] = t.upper()
    if "enum" in schema:
        out["enum"] = schema["enum"]
    if "properties" in schema:
        out["properties"] = {k: _gemini_schema(v) for k, v in schema["properties"].items()}
    if "required" in schema:
        out["required"] = schema["required"]
    return out


def gemini_chat(model: str, system: str, user: str, schema: dict, *, temperature: float, seed: int,
                timeout: float = 120) -> dict:
    """Gemini generateContent with a JSON response schema. The key goes in a header, never the URL."""
    key = _env("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment or .env")
    body = {"systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": temperature, "seed": seed, "responseMimeType": "application/json",
                                 "responseSchema": _gemini_schema(schema)}}
    body["generationConfig"]["thinkingConfig"] = {"thinkingLevel": "low"}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(6):     # back off on rate limits (429), overload (503) and timeouts
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read())
            parts = payload["candidates"][0]["content"]["parts"]
            return json.loads("".join(p.get("text", "") for p in parts if not p.get("thought")))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 503) or attempt == 5:
                raise
            RATE_LIMITED.append(e.code)
        except TimeoutError:
            if attempt == 5:
                raise
        time.sleep(min(60, 2 ** attempt * 3))
    raise RuntimeError("unreachable")


RATE_LIMITED: list[int] = []


def gemini_models() -> list[str]:
    key = _env("GEMINI_API_KEY")
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200",
                                 headers={"x-goog-api-key": key or ""})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return [m["name"].removeprefix("models/") for m in json.loads(resp.read()).get("models", [])
                if "generateContent" in m.get("supportedGenerationMethods", [])]


_BEDROCK = {}


def bedrock_chat(model: str, system: str, user: str, schema: dict, *, temperature: float, seed: int) -> dict:
    """Bedrock Converse (any text model). No response schema there, so ask for JSON and parse the first object.
    Credentials come from the usual AWS chain (AWS_PROFILE, SSO, env vars); region from AWS_REGION."""
    import os
    if "client" not in _BEDROCK:
        import boto3
        from botocore.config import Config
        _BEDROCK["client"] = boto3.client("bedrock-runtime", region_name=_env("AWS_REGION") or os.environ.get("AWS_REGION", "eu-west-2"),
                                          config=Config(retries={"max_attempts": 8, "mode": "adaptive"}))
    keys = ", ".join(f"'{k}'" for k in schema.get("properties", {}))
    ask = f"{user}\n\nReply with one JSON object only, with the keys {keys}. No other text."
    resp = _BEDROCK["client"].converse(
        modelId=model, system=[{"text": system}], messages=[{"role": "user", "content": [{"text": ask}]}],
        inferenceConfig={"temperature": temperature, "maxTokens": 2048})
    text = "".join(p.get("text", "") for p in resp["output"]["message"]["content"])
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError(f"no JSON object in Bedrock reply: {text[:200]!r}")
    return json.loads(text[start:end + 1])


def chat(provider: str, model: str, system: str, user: str, schema: dict, *, temperature: float, seed: int) -> dict:
    fn = {"gemini": gemini_chat, "bedrock": bedrock_chat}.get(provider, ollama_chat)
    return fn(model, system, user, schema, temperature=temperature, seed=seed)


def normalise(text: str) -> str:
    """For similarity: lower case, digits masked, whitespace collapsed."""
    return " ".join(re.sub(r"\d", "0", text.lower()).split())


def char_shingles(text: str, n: int = 5) -> set[str]:
    t = normalise(text)
    return {t[i:i + n] for i in range(max(len(t) - n + 1, 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def word_ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    w = re.findall(r"[a-z0-9]+", normalise(text))
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}
