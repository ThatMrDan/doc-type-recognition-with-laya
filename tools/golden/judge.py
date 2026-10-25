"""Blind judge: three runs per row with the guideline as the system prompt.

    uv run python tools/golden/judge.py --provider gemini --model <gemini model> --families A
    uv run python tools/golden/judge.py --provider ollama --model llama3.1:8b

A judge only labels rows from generator families it did not write (--families), so no model grades
its own text. It never sees the generator's label. Writes out/judge_<provider>_<model>.jsonl and is
resumable (skips ids already judged).
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from common import GUIDELINE, LABELS, OUT, RATE_LIMITED, ROWS, chat, read_jsonl

SCHEMA = {"type": "object", "properties": {
    "label": {"type": "string", "enum": list(LABELS)},
    "rule": {"type": ["integer", "null"]},
    "cue": {"type": "string"}}, "required": ["label", "rule", "cue"]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--provider", choices=["ollama", "gemini", "bedrock"], default="ollama")
    p.add_argument("--model", default="llama3.1:8b")
    p.add_argument("--families", nargs="*", default=["A", "B"])
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--workers", type=int, default=1)
    args = p.parse_args()
    system = ("You label insurance submission documents for a test set. Apply this guideline exactly.\n\n"
              + GUIDELINE.read_text()
              + "\n\nReturn JSON: 'label' (one of the five labels), 'rule' (the edge-case rule number you relied "
                "on, or null) and 'cue' (the few words in the text that decided it).")
    rows = [row for path in sorted(ROWS.glob("*.jsonl")) for row in read_jsonl(path)
            if row["generator_family"] in args.families]
    path = OUT / f"judge_{args.provider}_{re.sub(r'[^a-z0-9.]+', '-', args.model.lower())}.jsonl"
    done = {r["id"] for r in read_jsonl(path) if all(v["label"] for v in r["judge_votes"])}   # re-judge rows with failed calls
    OUT.mkdir(parents=True, exist_ok=True)
    todo = [row for row in rows if row["id"] not in done]
    lock = threading.Lock()

    def judge_row(row: dict) -> None:
        votes = []
        for run in range(args.runs):
            order = list(LABELS)
            random.Random(f"{row['id']}-{run}").shuffle(order)
            user = f"Labels in no particular order: {', '.join(order)}.\n\nDocument:\n{row['text']}"
            try:
                v = chat(args.provider, args.model, system, user, SCHEMA, temperature=0.7, seed=1000 + run)
            except Exception as e:     # a failed call is recorded, not retried silently
                v = {"label": None, "rule": None, "cue": f"error: {e}"}
            votes.append(v)
        labels = Counter(v["label"] for v in votes if v["label"])
        top, k = labels.most_common(1)[0] if labels else (None, 0)
        rec = {"id": row["id"], "judge_model": f"{args.provider}:{args.model}", "judge_votes": votes,
               "judge_label": top, "judge_stable": k == args.runs}
        with lock:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print(f"{row['id']} -> {top} ({k}/{args.runs})", file=sys.stderr, flush=True)

    with path.open("a") as f, ThreadPoolExecutor(args.workers) as ex:
        list(ex.map(judge_row, todo))
    print(f"judged {len(todo)} rows; rate-limit or overload retries: {len(RATE_LIMITED)}", flush=True)

if __name__ == "__main__":
    main()
