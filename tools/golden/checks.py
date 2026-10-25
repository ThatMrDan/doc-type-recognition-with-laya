"""Rule validators, the train-versus-golden contamination report, near-duplicate components and a
diversity and discriminator panel.

    uv run python tools/golden/checks.py

Training corpus: every data/production/*.jsonl row (what snapshots are built from). Writes
out/checks.jsonl (per row) and out/checks_summary.json. Thresholds follow the research report:
hard fail on an exact match, a shared 8-word n-gram, any of three 50-character substrings, character
5-gram Jaccard >= 0.8 or a training-data name; review for Jaccard 0.5 to 0.8.
"""

from __future__ import annotations

import gzip
import json
import math
import random
import re
from collections import Counter, defaultdict

from common import (LABELS, OUT, ROOT, ROWS, banned_hits, char_shingles, jaccard, normalise, read_jsonl,
                    word_ngrams)

CUES = {
    "sov": r"locat|premis|building|address|\btiv\b|insured value|sum insured|occupan|construct|values",
    "loss_run": r"claim|loss|paid|reserve|outstanding|incurred|no known",
    "acord": r"acord",
    "broker_email": r"from:|subject:|\bdear\b|\bhi\b|regards|thanks|sent:|wrote:|cheers",
}


def token_counter():
    try:
        from laya.train import resolve_checkpoint_dir
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(resolve_checkpoint_dir("typed-decisions") + "/tokenizer")
        return lambda t: len(tok(t)["input_ids"])
    except Exception:          # without the laya extra, fall back to a rough estimate and say so
        return lambda t: -int(len(t.split()) * 1.3)


def validate(row: dict, count) -> dict:
    text, label = row["text"], row["generator_label"]
    fails, warns = [], []
    if len(text.split()) < 8:
        fails.append("too_short")
    if hits := banned_hits(text):
        fails.append("training_name:" + ",".join(hits))
    if label in CUES and not re.search(CUES[label], text, re.I):
        warns.append(f"no_{label}_cue")
    if label != "acord" and re.search(r"\bacord\s*\d{2,3}\b", text, re.I) and row["slice"] == "core":
        warns.append("mentions_acord_form")
    return {"validator_fails": fails, "validator_warns": warns, "token_count": count(text)}


def contamination(rows: list[dict], train: list[str]) -> dict[str, dict]:
    tr_norm = [normalise(t) for t in train]
    tr_sh = [char_shingles(t) for t in train]
    tr_ng = set().union(*(word_ngrams(t) for t in train))
    r = random.Random(50)
    out = {}
    for row in rows:
        n = normalise(row["text"])
        sh = char_shingles(row["text"])
        sims = [jaccard(sh, s) for s in tr_sh]
        best = max(range(len(sims)), key=sims.__getitem__)
        subs = [n[i:i + 50] for i in (r.randrange(max(len(n) - 50, 1)) for _ in range(3))] if len(n) > 60 else []
        flags = []
        if n in tr_norm:
            flags.append("exact")
        if word_ngrams(row["text"]) & tr_ng:
            flags.append("shared_8gram")
        if any(s in t for s in subs for t in tr_norm):
            flags.append("verbatim_50")
        if sims[best] >= 0.8:
            flags.append("char5_ge_0.8")
        review = 0.5 <= sims[best] < 0.8
        out[row["id"]] = {"nearest_train_index": best, "max_char5_sim": round(sims[best], 3),
                          "leak_flags": flags, "leak_review": review}
    return out


def components(rows: list[dict], threshold: float = 0.5) -> dict[str, str]:
    """Union rows whose texts are near-duplicates (excluding a contrast or noise row and its own parent)."""
    parent = {r["id"]: r["id"] for r in rows}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    sh = {r["id"]: char_shingles(r["text"]) for r in rows}
    linked = {r["id"]: r.get("parent_id") for r in rows}
    ids = [r["id"] for r in rows]
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            if linked[a] == b or linked[b] == a or (linked[a] and linked[a] == linked[b]):
                continue
            if jaccard(sh[a], sh[b]) >= threshold:
                parent[find(a)] = find(b)
    return {i: find(i) for i in ids}


def diversity(texts: list[str]) -> dict:
    words = [w for t in texts for w in normalise(t).split()]
    bigrams = list(zip(words, words[1:]))
    blob = "\n".join(texts).encode()
    return {"n": len(texts), "distinct_2": round(len(set(bigrams)) / max(len(bigrams), 1), 3),
            "compression_ratio": round(len(blob) / max(len(gzip.compress(blob)), 1), 2)}


def discriminator(a: list[str], b: list[str], folds: int = 5) -> float | None:
    """Cross-validated accuracy of a character 3-gram naive Bayes telling golden from training text."""
    if len(a) < folds or len(b) < folds:
        return None
    data = [(t, 0) for t in a] + [(t, 1) for t in b]
    random.Random(3).shuffle(data)
    grams = lambda t: Counter(normalise(t)[i:i + 3] for i in range(len(normalise(t)) - 2))
    correct = 0
    for k in range(folds):
        test = data[k::folds]
        train = [d for i, d in enumerate(data) if i % folds != k]
        counts, totals, prior = [Counter(), Counter()], [0, 0], [0, 0]
        for t, y in train:
            g = grams(t); counts[y].update(g); totals[y] += sum(g.values()); prior[y] += 1
        vocab = len(set(counts[0]) | set(counts[1])) + 1
        for t, y in test:
            g = grams(t)
            score = [math.log(prior[c] / len(train)) + sum(n * math.log((counts[c][x] + 1) / (totals[c] + vocab))
                                                           for x, n in g.items()) for c in (0, 1)]
            correct += (score[1] > score[0]) == (y == 1)
    return round(correct / len(data), 3)


def main() -> None:
    rows = [row for path in sorted(ROWS.glob("*.jsonl")) for row in read_jsonl(path)]
    train = [json.loads(l)["text"] for p in sorted((ROOT / "data" / "production").glob("*.jsonl"))
             for l in p.read_text().splitlines() if l.strip()]
    count = token_counter()
    cont = contamination(rows, train)
    comp = components(rows)
    per_row = []
    for row in rows:
        rec = {"id": row["id"], **validate(row, count), **cont[row["id"]], "group_component": comp[row["id"]]}
        per_row.append(rec)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.jsonl").write_text("".join(json.dumps(r) + "\n" for r in per_row))

    by_fam = defaultdict(list)
    for row in rows:
        if row["slice"] == "core":
            by_fam[row["generator_family"]].append(row["text"])
    core = by_fam["A"] + by_fam["B"]
    multi = Counter(comp[r["id"]] for r in rows)
    summary = {
        "rows": len(rows), "by_file": Counter(r["id"].split("-")[0] + ":" + r["slice"] for r in rows),
        "validator_fails": Counter(f.split(":")[0] for r in per_row for f in r["validator_fails"]),
        "validator_warns": Counter(w for r in per_row for w in r["validator_warns"]),
        "leak_hard": Counter(f for r in per_row for f in r["leak_flags"]),
        "leak_review": sum(r["leak_review"] for r in per_row),
        "max_char5_sim": max(r["max_char5_sim"] for r in per_row),
        "over_512_tokens": sum(abs(r["token_count"]) > 512 for r in per_row),
        "near_dup_components_with_2_plus": sum(1 for c, k in multi.items() if k > 1),
        "diversity": {"A": diversity(by_fam["A"]), "B": diversity(by_fam["B"]), "training": diversity(train)},
        "discriminator_golden_core_vs_training": discriminator(core, train),
        "discriminator_A_vs_B": discriminator(by_fam["A"], by_fam["B"]),
    }
    (OUT / "checks_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
