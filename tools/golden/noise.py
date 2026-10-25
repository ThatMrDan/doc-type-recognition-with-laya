"""Invariance slice: seeded noise variants of core rows. The label follows the parent.

    uv run python tools/golden/noise.py

Reads every rows/*.jsonl core row, writes rows/n_invariance.jsonl.
"""

from __future__ import annotations

import random
import re

from common import LABELS, ROWS, read_jsonl, write_jsonl

PER_CLASS = {"sov": 8, "loss_run": 8, "acord": 6, "broker_email": 7, "other": 7}
OCR = {"O": "0", "0": "O", "l": "1", "I": "l", "S": "5", "rn": "m", "e": "c", "B": "8"}


def ocr(text: str, r: random.Random) -> str:
    out, i = [], 0
    while i < len(text):
        two = text[i:i + 2]
        if two in OCR and r.random() < 0.15:
            out.append(OCR[two]); i += 2; continue
        ch = text[i]
        out.append(OCR[ch] if ch in OCR and r.random() < 0.05 else ch); i += 1
    return "".join(out)


def past_window(text: str, r: random.Random) -> str:
    """Grow the document past Laya's context window by repeating its own body, as later pages would."""
    parts = re.split(r"(?<=[;\n.])\s+", text)
    body = parts[len(parts) // 3:] or parts
    out = text
    while len(out.split()) < 900:
        out += " " + " ".join(r.sample(body, min(len(body), 4)))
    return out


def uk_format(text: str, r: random.Random) -> str:
    text = re.sub(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b", r"\2/\1/\3", text)
    return text.replace("$", "£").replace("USD", "GBP")


def drop_header(text: str, r: random.Random) -> str:
    for sep in ("\n", " ; ", ". "):
        if sep in text:
            head, rest = text.split(sep, 1)
            if len(rest.split()) >= 8:
                return rest
    return text


def caps(text: str, r: random.Random) -> str:
    return text.upper()


def fwd(text: str, r: random.Random) -> str:
    return ("FW: see below\n\n-----Original Message-----\n" + text)


OPS = {"ocr": ocr, "past_window": past_window, "uk_format": uk_format, "drop_header": drop_header, "caps": caps}


def main() -> None:
    r = random.Random(36)
    core = [row for p in sorted(ROWS.glob("[ab]_*.jsonl")) for row in read_jsonl(p) if row["slice"] == "core"]
    out = []
    for label in LABELS:
        pool = [row for row in core if row["generator_label"] == label]
        r.shuffle(pool)
        ops = list(OPS) + (["fwd"] if label == "broker_email" else [])
        for k, parent in enumerate(pool[:PER_CLASS[label]]):
            op = ops[k % len(ops)]
            fn = fwd if op == "fwd" else OPS[op]
            text = fn(parent["text"], r)
            if text == parent["text"]:
                op, text = "ocr", ocr(parent["text"], r)
            out.append({**{k2: parent[k2] for k2 in ("generator", "generator_family", "prompt_id", "attribute_cell",
                                                     "template_group", "generator_label")},
                        "id": f"N-{label}-{k + 1:03d}", "slice": "invariance", "edge_rule": None,
                        "expected_flags": [], "parent_id": parent["id"], "pair_id": None,
                        "noise_ops": [op], "text": text})
    write_jsonl(ROWS / "n_invariance.jsonl", out)
    print(f"wrote {len(out)} invariance rows")


if __name__ == "__main__":
    main()
