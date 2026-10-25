"""Select rows to the golden-v2 counts and write the draft, manifest and labelling kit.

    uv run python tools/golden/assemble.py

Selection never uses the judge's or any model's opinion (that would bias the set towards easy rows).
It drops only hard failures (validator fails, leak flags), keeps every contrast parent, caps each
near-duplicate component and template group at 5 core rows, and fills class quotas alternating
generator families. Labels stay provisional (generator label) until two annotators and an
adjudicator have labelled every row.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict

from common import LABELS, OUT, ROOT, ROWS, read_jsonl

sys.path.insert(0, str(ROOT / "src"))
from doctype.domain import doc_hash  # noqa: E402

VERSION = "golden-v2-draft"
CORE = {"sov": 70, "loss_run": 70, "acord": 65, "broker_email": 70, "other": 85}
BOUNDARY, CONTRAST, INVARIANCE = 64, 40, 36
GROUP_CAP = 5
KIT = ROOT / "docs" / "golden" / "kit"


def merge_judges() -> dict[str, dict]:
    """Pool every judge's votes per row; each judge file only covers families that judge did not write."""
    pooled: dict[str, dict] = {}
    for path in sorted(OUT.glob("judge_*.jsonl")):
        for j in read_jsonl(path):
            rec = pooled.setdefault(j["id"], {"judge_models": [], "judge_votes": []})
            rec["judge_models"].append(j["judge_model"])
            rec["judge_votes"] += [dict(v, judge_model=j["judge_model"]) for v in j["judge_votes"]]
    for rec in pooled.values():
        labels = Counter(v["label"] for v in rec["judge_votes"] if v.get("label"))
        top, k = labels.most_common(1)[0] if labels else (None, 0)
        rec["judge_label"], rec["judge_stable"] = top, bool(labels) and k == sum(labels.values())
    return pooled


def main() -> None:
    r = random.Random(500)
    rows = {row["id"]: row for p in sorted(ROWS.glob("*.jsonl")) for row in read_jsonl(p)}
    checks = {c["id"]: c for c in read_jsonl(OUT / "checks.jsonl")}
    judge = merge_judges()
    ok = {i: row for i, row in rows.items()
          if not checks[i]["validator_fails"] and not checks[i]["leak_flags"]}
    dropped = sorted(set(rows) - set(ok))

    # core: contrast parents first, then alternate families, capped per group and component
    contrast = [row for row in ok.values() if row["slice"] == "contrast" and row["parent_id"] in ok]
    contrast = contrast[:CONTRAST]
    must = {row["parent_id"] for row in contrast}
    per_group, per_comp, core = Counter(), Counter(), []

    def take(row) -> bool:
        g, c = row["template_group"], checks[row["id"]]["group_component"]
        if per_group[g] >= GROUP_CAP or per_comp[c] >= GROUP_CAP:
            return False
        per_group[g] += 1; per_comp[c] += 1; core.append(row)
        return True

    for i in sorted(must):
        take(ok[i])
    for label, quota in CORE.items():
        fams = {f: [row for row in ok.values() if row["slice"] == "core" and row["generator_label"] == label
                    and row["generator_family"] == f and row["id"] not in must] for f in "AB"}
        for f in fams:
            r.shuffle(fams[f])
        have = sum(row["generator_label"] == label for row in core)
        turn = "AB"
        while have < quota and (fams["A"] or fams["B"]):
            for f in turn:
                if fams[f] and have < quota:
                    if take(fams[f].pop()):
                        have += 1
    core_ids = {row["id"] for row in core}

    boundary = [row for row in ok.values() if row["slice"] == "boundary"]
    by_rule = defaultdict(list)
    for row in boundary:
        by_rule[row["edge_rule"]].append(row)
    picked_b = []
    while len(picked_b) < BOUNDARY and any(by_rule.values()):
        for rule in sorted(by_rule, key=lambda x: (x is None, x)):
            if by_rule[rule] and len(picked_b) < BOUNDARY:
                picked_b.append(by_rule[rule].pop(0))
    invariance = [row for row in ok.values() if row["slice"] == "invariance" and row["parent_id"] in core_ids]
    invariance = invariance[:INVARIANCE]
    final = core + picked_b + contrast + invariance

    out = []
    for n, row in enumerate(final, 1):
        c, j = checks[row["id"]], judge.get(row["id"], {})
        out.append({
            "doc_id": f"G2-{n:04d}", "source_row": row["id"], "golden_version": VERSION,
            "content_hash": doc_hash(row["text"]), "text": row["text"], "token_count": c["token_count"],
            "final_label": None, "outcome": "pending", "provisional_label": row["generator_label"],
            "slice": row["slice"], "stratum": row["generator_label"], "edge_rule": row.get("edge_rule"),
            "expected_flags": row.get("expected_flags", []),
            "template_group": row["template_group"], "group_component": c["group_component"],
            "source": "synthetic_llm", "generator": row["generator"], "generator_family": row["generator_family"],
            "prompt_id": row["prompt_id"], "seed": row.get("seed"), "attribute_cell": row.get("attribute_cell", {}),
            "parent_id": row.get("parent_id"), "pair_id": row.get("pair_id"), "noise_ops": row.get("noise_ops", []),
            "generator_label": row["generator_label"],
            "validator_results": {"warns": c["validator_warns"]},
            "judge_model": j.get("judge_models", []), "judge_votes": j.get("judge_votes", []),
            "judge_label": j.get("judge_label"), "judge_stable": j.get("judge_stable"),
            "labels": [], "adjudicator_id": None, "adjudication_rule": None, "adjudication_rationale": None,
            "max_char5_sim": c["max_char5_sim"], "leak_flags": c["leak_flags"], "leak_review": c["leak_review"],
        })
    # parent ids point at source rows; map them to doc ids
    to_doc = {o["source_row"]: o["doc_id"] for o in out}
    for o in out:
        if o["parent_id"]:
            o["parent_id"] = to_doc.get(o["parent_id"], o["parent_id"])

    draft = ROOT / "data" / "golden" / f"{VERSION}.jsonl"
    draft.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out))
    sha = hashlib.sha256(draft.read_bytes()).hexdigest()
    summary = {
        "golden_version": VERSION, "file": str(draft.relative_to(ROOT)), "sha256": sha, "rows": len(out),
        "guideline": "docs/golden/guideline-v1.md (1.0)", "status": "draft: provisional labels, not for promotion",
        "by_slice": Counter(o["slice"] for o in out),
        "core_by_class": Counter(o["stratum"] for o in out if o["slice"] == "core"),
        "core_by_family": Counter(o["generator_family"] for o in out if o["slice"] == "core"),
        "core_groups_by_class": {l: len({o["template_group"] for o in out if o["slice"] == "core" and o["stratum"] == l})
                                 for l in LABELS},
        "boundary_by_rule": Counter(str(o["edge_rule"]) for o in out if o["slice"] == "boundary"),
        "judge_agrees_with_generator": sum(o["judge_label"] == o["generator_label"] for o in out),
        "judge_unstable": sum(o["judge_stable"] is False for o in out),
        "dropped_hard_fail": dropped, "candidates": len(rows),
        "shortfalls": {l: q - sum(o["stratum"] == l for o in out if o["slice"] == "core") for l, q in CORE.items()},
    }
    (ROOT / "data" / "golden" / f"{VERSION}.manifest.json").write_text(json.dumps(summary, indent=2))

    # labelling kit: blind (no labels, no generator or judge output), a different order per annotator
    KIT.mkdir(parents=True, exist_ok=True)
    for a, seed in (("annotator_1", 11), ("annotator_2", 22)):
        order = out[:]
        random.Random(seed).shuffle(order)
        with (KIT / f"{a}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["doc_id", "text", "label", "flags", "rule", "notes"])
            for o in order:
                w.writerow([o["doc_id"], o["text"], "", "", "", ""])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
