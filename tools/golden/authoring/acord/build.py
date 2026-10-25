import json, re, sys
sys.path.insert(0, '.')
from core import CORE
from rest import BOUNDARY, CONTRAST
def length(t):
    n = len(t.split())
    return "short" if n <= 40 else "medium" if n <= 120 else "long", n
rows = []
def mk(i, slice_, key, label, rule, flags, attrs, text, parent=None, pair=None):
    L, n = length(text)
    cell = {"market": attrs.get("market", "US"), "format": "pdf_scan" if attrs.get("noise") == "ocr" else "pdf", "length": L}
    cell.update({k: v for k, v in attrs.items() if k not in cell})
    return {"id": f"A-acord-{i:03d}", "slice": slice_, "generator": "claude-opus-5.5", "generator_family": "A",
            "prompt_id": "a-acord-v1", "attribute_cell": cell, "template_group": f"gA:acord:{key}",
            "generator_label": label, "edge_rule": rule, "expected_flags": flags, "parent_id": parent,
            "pair_id": pair, "text": text}
i = 0
for key, attrs, text in CORE:
    i += 1; rows.append(mk(i, "core", key, "acord", None, [], attrs, text))
for key, label, rule, flags, attrs, text in BOUNDARY:
    i += 1; rows.append(mk(i, "boundary", key, label, rule, flags, attrs, text))
for n, (p, label, attrs, text) in enumerate(CONTRAST, 1):
    i += 1
    parent = rows[p - 1]
    a = dict(parent["attribute_cell"]); a.pop("length"); a.pop("format"); a.update(attrs)
    a["noise"] = parent["attribute_cell"].get("noise")
    r = mk(i, "contrast", parent["template_group"].split(":", 2)[2], label, None, [], a, text,
           parent=parent["id"], pair=f"P-acord-{n}")
    r["attribute_cell"].pop("number_position", None)
    if label == "broker_email": r["attribute_cell"]["format"] = "email"
    rows.append(r)
out = "/Users/dan/host-code/doc-type-recognition-with-laya/tools/golden/rows/a_acord.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows))
