"""Generator family B (Google: gemma3 via Ollama, or Gemini via the API), one call per attribute-grid cell.

    uv run python tools/golden/gen_b.py [--model gemma3:12b]
    uv run python tools/golden/gen_b.py --provider gemini --model <gemini model> --only acord broker_email other

Writes tools/golden/rows/b_<class>.jsonl. Seeded: the same grid and seeds give the same calls.
"""

from __future__ import annotations

import argparse
import itertools
import random
import re
import sys

from common import BANNED, ROWS, banned_hits, chat, read_jsonl, write_jsonl

DEFINITIONS = {
    "sov": "an insurance statement or schedule of values: a per-location or per-building schedule of property "
           "attributes (address, occupancy, construction, year built, area, sprinklers, protection) and insured "
           "values (building, contents, business interruption, total)",
    "loss_run": "a loss run or loss history for an insured: carrier or TPA claims listing with policy periods, "
                "valuation date, claim numbers, dates of loss, causes, paid, reserve or outstanding, incurred, status",
    "acord": "a standard ACORD application form or section (for example 125, 126, 127, 130, 131, 137, 140) "
             "with filled application fields: applicant, premises, prior carrier, hazards",
    "broker_email": "an email from an insurance broker, MGA or agent covering a submission: headers, greeting, "
                    "what cover is wanted, dates, what is attached, signature",
    "other": "a document found in an insurance submission that is none of: schedule of values, loss run, ACORD "
             "application, broker email. For example a survey, valuation report, supplemental questionnaire, quote, "
             "binder, MRC slip, presentation, financial statement, invoice, KYC check, certificate of insurance",
}

GRID = {
    "sov": {"market": ["US", "UK"], "format": ["spreadsheet header and first rows", "carrier PDF form", "cover sheet with schedule"],
            "size": ["1 location", "6 locations", "40 locations", "250 locations"],
            "occupancy": ["warehousing", "manufacturing", "retail", "hotel", "healthcare", "school", "mixed use"]},
    "loss_run": {"market": ["US", "UK"], "source": ["carrier printout", "TPA report", "broker summary"],
                 "line": ["property", "general liability", "commercial auto", "workers compensation", "marine cargo"],
                 "history": ["3 years", "5 years", "10 years", "nil claims most years"]},
    "acord": {"form": ["125", "126", "127", "130", "131", "137", "140", "160"],
              "state": ["filled", "partly filled", "scanned with OCR noise"], "market": ["US"]},
    "broker_email": {"market": ["US", "UK"], "sender": ["retail agent", "wholesale broker", "MGA", "London broker"],
                     "purpose": ["new submission", "renewal", "chasing a quote", "answering subjectivities", "bind request"],
                     "style": ["terse", "formal", "forwarded chain"]},
    "other": {"kind": ["risk survey report", "valuation report", "cyber supplemental questionnaire", "carrier quote",
                       "binding authority schedule", "MRC slip", "broker market presentation", "management accounts",
                       "premium invoice", "KYC confirmation", "certificate of insurance", "fire risk assessment",
                       "policy endorsement", "loss control recommendations letter", "site photo log"],
              "market": ["US", "UK"]},
}
COUNTS = {"sov": 37, "loss_run": 37, "acord": 35, "broker_email": 37, "other": 45}
LENGTHS = [("short", "20 to 40"), ("medium", "50 to 110"), ("long", "130 to 220")]

SYSTEM = ("You write realistic but entirely fictional documents for testing an insurance document classifier. "
          "Output only JSON. Never use real company names. Invent every person, firm, carrier, insured, "
          "address and policy number.")

SCHEMA = {"type": "object", "properties": {"source_key": {"type": "string"}, "text": {"type": "string"}},
          "required": ["source_key", "text"]}


def prompt(label: str, cell: dict, words: str) -> str:
    attrs = "; ".join(f"{k}: {v}" for k, v in cell.items() if k != "length")
    return (f"Write the text a document classifier would see for {DEFINITIONS[label]}.\n"
            f"Attributes: {attrs}.\n"
            f"Length: {words} words.\n"
            "If it is a spreadsheet, give the header row and the first data rows with cells separated by ' | '. "
            "If it is a PDF, give the first page text. If it is an email, give the headers then the body.\n"
            "Make the figures realistic and consistent. Do not explain anything; do not add a title like "
            "'Example'.\n"
            f"Do not use any of these names: {', '.join(BANNED)}.\n"
            "Return JSON with 'source_key' (a short name for the fictional firm, carrier system or form edition "
            "that produced it) and 'text'.")


def cells(label: str, n: int, rng: random.Random) -> list[dict]:
    keys = list(GRID[label])
    combos = [dict(zip(keys, c)) for c in itertools.product(*(GRID[label][k] for k in keys))]
    rng.shuffle(combos)
    picked = (combos * (n // len(combos) + 1))[:n]
    for c in picked:
        c["length"] = rng.choice(LENGTHS)[0]
    return picked


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--provider", choices=["ollama", "gemini", "bedrock"], default="ollama")
    p.add_argument("--model", default="gemma3:12b")
    p.add_argument("--seed", type=int, default=4242)
    p.add_argument("--only", nargs="*", choices=list(COUNTS))
    args = p.parse_args()
    rng = random.Random(args.seed)
    for label, n in COUNTS.items():
        if args.only and label not in args.only:
            continue
        path = ROWS / f"b_{label}.jsonl"
        rows = read_jsonl(path)          # resume: keep rows already written, generate the rest
        have = {r["id"] for r in rows}
        for i, cell in enumerate(cells(label, n, rng)):
            if f"B-{label}-{i + 1:03d}" in have:
                continue
            words = dict(LENGTHS)[cell["length"]]
            seed = args.seed * 1000 + i
            for attempt in range(3):
                out = chat(args.provider, args.model, SYSTEM, prompt(label, cell, words), SCHEMA,
                           temperature=0.9, seed=seed + attempt * 7919)
                text = out.get("text", "").strip()
                if text and not banned_hits(text):
                    break
            key = re.sub(r"[^a-z0-9]+", "-", out.get("source_key", "unknown").lower()).strip("-")[:40] or "unknown"
            rows.append({
                "id": f"B-{label}-{i + 1:03d}", "slice": "core", "generator": f"{args.provider}:{args.model}",
                "generator_family": "B", "prompt_id": "b-v1", "seed": seed, "attribute_cell": cell,
                "template_group": f"gB:{label}:{key}", "generator_label": label, "edge_rule": None,
                "expected_flags": [], "parent_id": None, "pair_id": None, "text": text,
            })
            write_jsonl(path, rows)
            print(f"{label} {i + 1}/{n} {len(text.split())} words  {key}", file=sys.stderr, flush=True)
        print(f"wrote {len(rows)} {label} rows", flush=True)


if __name__ == "__main__":
    main()
