"""Generate synthetic production documents for a demo week.

    uv run python scripts/generate_production.py              # week1, 120 generated rows
    uv run python scripts/generate_production.py --n 60 --week week2

Hand-written rows in data/production/<week>.jsonl are kept as they are. Rows this script wrote
before carry "source": "generated" and are replaced, so re-running is safe. Seeded, so the same
arguments always give the same file.

The text is what Laya sees: the first lines of a sheet, form or email body. Brokers, people and
addresses are invented. About one row in six is a deliberate hard case: wording the regex
extractors miss, emails that mention other document types, or a cover title that disagrees with
the content. Template groups never reuse a golden-set group.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

BROKERS = ["harbourline", "kestrel", "northgate", "ashby", "blackfriars", "saltmarsh", "redcliffe",
           "fenwick", "larkspur", "tamar", "wexcombe", "aldgate"]
PEOPLE = ["amy", "tom", "lee", "kim", "sam", "ana", "raj", "zoe", "ben", "eve", "ola", "max", "ivy", "noah"]
TLDS = ["co.uk", "com", "uk", "ie"]
OCCUPANCY = ["warehousing", "light manufacturing", "retail units", "offices", "cold storage", "food processing",
             "hotel", "logistics hub", "student accommodation", "data centre"]
CONSTRUCTION = ["frame construction", "steel frame", "masonry non-combustible", "timber frame", "concrete frame"]
INSUREDS = ["Brindle Foods Ltd", "Copperleaf Logistics", "Merrow Hotels plc", "Ostrander Plastics",
            "Pellow Cold Store", "Quarry Lane Estates", "Rowan Data Centres", "Tillery Marine", "Vance & Hart Ltd",
            "Wickham Retail Group", "Yardley Engineering", "Ebury Student Living"]
CLASSES = ["property", "general liability", "marine cargo", "product liability", "property damage and BI"]


def money(r: random.Random, lo: float, hi: float) -> str:
    v = r.uniform(lo, hi)
    style = r.random()
    if style < 0.5:
        return f"{v:.1f}m" if v < 100 else f"{v:.0f}m"
    if style < 0.8:
        return f"{v * 1_000_000:,.0f}"
    return f"{v * 1000:.0f}k"


def sov(r: random.Random, broker: str) -> tuple[str, str, bool]:
    n = r.randint(2, 60)
    tiv = money(r, 2, 400)
    head = r.choice(["Schedule of values", "Statement of values", "Statement of exposures", "Property schedule",
                     "Insured values by location", "Location schedule", "Premises register"])
    if r.random() < 0.15:   # hard: no "TIV" token, or a currency sign the extractor does not expect
        alt = r.choice([f"total sum insured {tiv}", f"TIV £{tiv}", f"buildings and contents declared {tiv}"])
        text = f"{head}, {n} locations, {alt}. Occupancy {r.choice(OCCUPANCY)}, {r.choice(CONSTRUCTION)}."
        return text, f"{broker}-sov", True
    extras = r.sample([f"occupancy {r.choice(OCCUPANCY)}", r.choice(CONSTRUCTION), "sprinklered",
                       f"year built {r.randint(1960, 2022)}", "BI 12 months indemnity", "flood zone 2 at 1 site"], 2)
    text = f"{head} {n} locations, TIV {tiv}, {extras[0]}, {extras[1]}"
    return text, f"{broker}-sov", False


def loss_run(r: random.Random, broker: str) -> tuple[str, str, bool]:
    yrs = r.choice(["3 yr", "5 years", "five year", "4 yr", "10 years", "6 year"])
    inc = money(r, 0.05, 6)
    head = r.choice(["Loss run", "Loss history", "Carrier loss summary", "Claims experience", "Loss report",
                     "Five year loss summary"])
    if r.random() < 0.15:   # hard: paid and reserved but never the word "incurred"
        text = (f"{head} {yrs}: paid {money(r, 0.05, 3)}, outstanding reserves {money(r, 0.01, 1)}, "
                f"{r.randint(1, 30)} claims, {r.randint(0, 3)} open")
        return text, f"{broker}-loss", True
    tail = r.choice([f"claims {r.randint(1, 40)}", "large losses listed", f"{r.randint(0, 4)} open claims",
                     "valued as at 30 Sept 2026", f"largest single loss {money(r, 0.01, 1)}"])
    return f"{head} {yrs} incurred {inc}, {tail}", f"{broker}-loss", False


def acord(r: random.Random, broker: str) -> tuple[str, str, bool]:
    form, title = r.choice([("125", "commercial insurance application"), ("126", "general liability section"),
                            ("140", "property section"), ("131", "umbrella / excess section"),
                            ("130", "workers compensation application"), ("137", "commercial auto section")])
    tail = r.choice(["applicant information", "named insured and mailing address", "premises information",
                     "prior carrier information", "schedule of hazards", "additional premises"])
    return f"ACORD {form} {title}, {tail}, insured {r.choice(INSUREDS)}", f"acord-{form}", False


def broker_email(r: random.Random, broker: str) -> tuple[str, str, bool]:
    who = r.choice(PEOPLE)
    sender = f"{who}@{broker}.{r.choice(TLDS)}"
    subj = r.choice(["Fwd: new submission", "Re: renewal pack attached", "Re: quote request",
                     "Fwd: updated exposures", "Re: subjectivities", "Submission for your review"])
    if r.random() < 0.2:    # hard: the email talks about the other document types
        body = r.choice([f"please find the ACORD {r.choice(['125', '140'])} and SOV attached",
                         "loss runs for five years attached, incurred figures to follow",
                         "schedule of values to follow, TIV circa 40m, please indicate"])
        return f"From: {sender} {subj}. Dear underwriter, {body}. Kind regards, {who.title()}", \
            f"broker-{who}", True
    body = r.choice(["please see attached pack", f"{r.choice(CLASSES)} renewal, terms by Friday please",
                     "attaching the full submission", "client keen to bind by month end",
                     "updated information attached as requested"])
    sign = r.choice(["regards", "kind regards", "thanks", "best"])
    return f"From: {sender} {subj}. {body.capitalize()}, {sign}", f"broker-{who}", False


def other(r: random.Random, broker: str) -> tuple[str, str, bool]:
    text, group = r.choice([
        ("Risk survey report, fire protection recommendations and site photos", "surveyor-a"),
        ("Valuation report for warehouse, reinstatement cost and floor plan", "valuer-b"),
        ("Binder agreement, delegated authority schedule and limits", "binder"),
        ("Premium invoice and payment terms, due 30 days", "invoice"),
        ("Engineering inspection certificate, lifting equipment", "engineer"),
        ("Terms of business agreement between broker and insurer", "tob"),
        ("Fire risk assessment, means of escape and alarm testing", "fra"),
        ("Market presentation, client overview and placement strategy", f"{broker}-presentation"),
        ("Sanctions screening and KYC confirmation for the insured", "kyc"),
        ("Site plan and aerial photography, building footprint", "plans"),
    ])
    return f"{text}, {r.choice(INSUREDS)}", group, False


def mislabelled(r: random.Random, broker: str) -> tuple[str, str, str]:
    """A cover title that disagrees with the content: the extractor router has to recover the type."""
    return (f"Schedule of values tiv summary sheet, loss history {r.choice(['5 years', '3 yr'])} "
            f"incurred {money(r, 0.1, 3)}", f"{broker}-mixed", "loss_run")


MIX = [("sov", sov, 30), ("loss_run", loss_run, 24), ("acord", acord, 18), ("broker_email", broker_email, 28),
       ("other", other, 14)]


def generate(n: int, seed: int) -> list[dict]:
    r = random.Random(seed)
    makers = [(t, f) for t, f, w in MIX for _ in range(w)]
    rows = []
    for i in range(n):
        broker = r.choice(BROKERS)
        if r.random() < 0.03:
            text, group, truth = mislabelled(r, broker)
            hard = True
        else:
            truth, maker = r.choice(makers)
            text, group, hard = maker(r, broker)
        rows.append({"text": text, "template_group": group, "truth": truth, "source": "generated",
                     **({"hard": True} if hard else {})})
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--week", default="week1")
    p.add_argument("--n", type=int, default=120)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--data-dir", default="data")
    args = p.parse_args()

    path = Path(args.data_dir) / "production" / f"{args.week}.jsonl"
    golden = Path(args.data_dir) / "golden" / "golden-v1.jsonl"
    golden_groups = {json.loads(l)["template_group"] for l in golden.read_text().splitlines() if l.strip()}
    kept = [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []
    kept = [row for row in kept if row.get("source") != "generated"]
    new = generate(args.n, args.seed)
    assert not {row["template_group"] for row in new} & golden_groups, "generated rows reuse a golden group"
    path.write_text("".join(json.dumps(row) + "\n" for row in kept + new))
    print(f"{path}: {len(kept)} hand-written + {len(new)} generated = {len(kept) + len(new)} rows")


if __name__ == "__main__":
    main()
