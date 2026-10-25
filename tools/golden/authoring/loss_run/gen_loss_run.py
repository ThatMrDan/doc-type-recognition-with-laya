"""Hand-authored loss_run golden rows (generator family A). Figures computed so paid + reserve = incurred."""
import json
import sys

OUT = sys.argv[1]
rows = []


def usd(x):
    return f"${x:,.2f}"


def usd0(x):
    return f"${x:,.0f}"


def gbp(x):
    return f"£{x:,.0f}"


def gbp2(x):
    return f"£{x:,.2f}"


def add(slice_, cell, group, label, text, edge_rule=None, flags=None, parent=None, pair=None):
    n = len(rows) + 1
    rows.append({
        "id": f"A-loss_run-{n:03d}",
        "slice": slice_,
        "generator": "claude-opus-5.5",
        "generator_family": "A",
        "prompt_id": "a-loss_run-v1",
        "attribute_cell": cell,
        "template_group": group,
        "generator_label": label,
        "edge_rule": edge_rule,
        "expected_flags": flags or [],
        "parent_id": parent,
        "pair_id": pair,
        "text": text.strip(),
    })
    return rows[-1]["id"]


def cell(market, source, line, layout, length, years, drift=None, ocr=False, incurred_word=True):
    return {"market": market, "source": source, "line": line, "layout": layout, "length": length,
            "years": years, "label_drift": drift or [], "ocr_noise": ocr, "incurred_word": incurred_word}


def claim_lines(claims, fmt, sep=" | "):
    out = []
    for c in claims:
        no, dol, desc, paid, res, status = c
        out.append(sep.join([no, dol, desc, fmt(paid), fmt(res), fmt(paid + res), status]))
    return out


def tot(claims):
    p = sum(c[3] for c in claims)
    r = sum(c[4] for c in claims)
    return p, r, p + r


CORE = {}

# ---------------- CORE ----------------

# 1 Granitebridge ClaimTrak, US property, medium
c1 = [
    ("GB-P-22-00417", "02/14/2022", "Frozen pipe burst, 2nd floor office", 38420.00, 0.00, "Closed"),
    ("GB-P-23-01188", "07/09/2023", "Wind damage to roof membrane", 61750.00, 12500.00, "Open"),
    ("GB-P-24-00342", "04/22/2024", "Sprinkler head leak, warehouse bay 3", 9875.40, 0.00, "Closed"),
]
p, r, i = tot(c1)
t = f"""GRANITEBRIDGE MUTUAL INSURANCE COMPANY
ClaimTrak Loss Run Report    Run Date: 10/02/2026    Valuation Date: 09/30/2026
Named Insured: Coldwater Ridge Distribution LLC
Policy No: CPP 7740312-05   Line: Commercial Property
Policy Periods: 10/01/2021 - 10/01/2026
Claim No | Date of Loss | Cause / Description | Paid | Reserve | Incurred | Status
""" + "\n".join(claim_lines(c1, usd)) + f"""
TOTALS (3 claims) | | | {usd(p)} | {usd(r)} | {usd(i)} |
Policy year 10/01/2021-22 and 10/01/2025-26: no claims reported."""
CORE[1] = add("core", cell("US", "carrier loss run printout", "property", "header + claim rows", "medium", 5),
              "gA:loss_run:granitebridge-claimtrak", "loss_run", t)

# 2 Granitebridge ClaimTrak, US property, long, per-year sections with no-claims years
c2a = [("GB-P-19-00911", "08/03/2019", "Hail, rooftop HVAC units and skylights", 112400.00, 0.00, "Closed")]
c2b = [("GB-P-21-00102", "01/18/2021", "Vandalism, broken storefront glass", 4210.00, 0.00, "Closed"),
       ("GB-P-21-00655", "05/27/2021", "Fire in tenant kitchen, smoke damage units 4-6", 287900.00, 41200.00, "Open")]
c2c = [("GB-P-23-00230", "03/11/2023", "Water intrusion, failed window seals", 18640.00, 2500.00, "Open")]
pa, ra, ia = tot(c2a); pb, rb, ib = tot(c2b); pc, rc, ic = tot(c2c)
P, R, I = pa + pb + pc, ra + rb + rc, ia + ib + ic
t = f"""GRANITEBRIDGE MUTUAL INSURANCE COMPANY          ClaimTrak v6.2          Page 1 of 1
LOSS RUN - ALL CLAIMS - PROPERTY
Insured: Oakhurst Plaza Partners LP       Producer: Tallis Grove Insurance Agency
Policy Number: CPP 6618904 (renewals -01 to -05)
Policy Term Covered: 06/01/2019 to 06/01/2024     Valuation Date: 08/31/2026
Report Basis: Gross of deductible, ground-up, includes expense

POLICY PERIOD 06/01/2019 - 06/01/2020
Claim No | DOL | Description | Paid | Reserve | Incurred | Status
""" + "\n".join(claim_lines(c2a, usd)) + f"""
Period Total: {usd(pa)} | {usd(ra)} | {usd(ia)}

POLICY PERIOD 06/01/2020 - 06/01/2021
""" + "\n".join(claim_lines(c2b, usd)) + f"""
Period Total: {usd(pb)} | {usd(rb)} | {usd(ib)}

POLICY PERIOD 06/01/2021 - 06/01/2022
*** NO CLAIMS THIS PERIOD ***

POLICY PERIOD 06/01/2022 - 06/01/2023
""" + "\n".join(claim_lines(c2c, usd)) + f"""
Period Total: {usd(pc)} | {usd(rc)} | {usd(ic)}

POLICY PERIOD 06/01/2023 - 06/01/2024
*** NO CLAIMS THIS PERIOD ***

GRAND TOTAL ALL PERIODS (4 claims, 2 open): Paid {usd(P)}  Reserve {usd(R)}  Incurred {usd(I)}
This report reflects information in the ClaimTrak system as of the valuation date and is subject to change."""
CORE[2] = add("core", cell("US", "carrier loss run printout", "property", "per-period sections, no-claims rows", "long", 5),
              "gA:loss_run:granitebridge-claimtrak", "loss_run", t)

# 3 Pinecrest LossView, US GL, medium, Total Inc.
c3 = [
    ("PC-GL-0318872", "03/02/2024", "Customer slip and fall, wet floor at entrance", 6200.00, 12200.00, "Open"),
    ("PC-GL-0302291", "11/15/2023", "Property damage, delivery truck struck neighbour fence", 3480.00, 0.00, "Closed"),
    ("PC-GL-0276650", "06/30/2022", "Bodily injury, patron tripped on display platform", 22500.00, 0.00, "Closed"),
]
p, r, i = tot(c3)
t = f"""PINECREST CASUALTY COMPANY - LossView
Loss History by Claim    as of 09/15/2026
Insured: Bellmont Home & Garden Centers Inc.   Pol #: GL 20-448812
Eff 01/01/2022 thru 01/01/2026 (4 terms)   Coverage: General Liability (Occurrence)
Clm # | Loss Dt | Description | Pd Loss | Reserve | Total Inc. | Sts
""" + "\n".join(claim_lines(c3, usd)) + f"""
Total: 3 clms | {usd(p)} | {usd(r)} | {usd(i)}
Term 01/01/2025-26: No losses reported."""
CORE[3] = add("core", cell("US", "carrier loss run printout", "GL", "header + claim rows", "medium", 4, ["Total Inc."]),
              "gA:loss_run:pinecrest-lossview", "loss_run", t)

# 4 Pinecrest LossView, US GL, short, totals by policy year only
t = """PINECREST CASUALTY - LossView Summary. Insured: Delgado Brothers Roofing. GL 20-512094. Valued 09/30/2026.
Pol Yr | Clms | Paid | Reserve | Total Inc.
2023-24 | 1 | $8,150 | $0 | $8,150
2024-25 | 0 | $0 | $0 | $0
2025-26 | 2 | $3,900 | $27,000 | $30,900"""
CORE[4] = add("core", cell("US", "carrier loss run printout", "GL", "totals by policy year only", "short", 3, ["Total Inc."]),
              "gA:loss_run:pinecrest-lossview", "loss_run", t)

# 5 Ironvale RiskPoint, US auto, medium, faxed OCR
t = """FAX  10/06/2026 14:22  FROM: IRONVALE INS CO   PG 01/02
IRONVALE INSURANCE C0MPANY  RiskPoint Loss Run
lnsured: Sutter Creek Aggregates Inc      Policy: BA 3307715
Policy Period: O7/01/2022 - 07/01/2025    Valuation: 09/30/2026
Claim#      DOL         Description                      Paid        Reserve    Incurred   Status
A2201876  11/04/2022  Rear-end collision, unit 14 dump   $14,220.00  $0.00      $14,220.00  CL
A2300412  02/19/2023  Windshield, flying stone, unit 9   $   640.00  $0.00      $   640.00  CL
A2402233  05/08/2024  Backing accident, client gate      $ 2,915.5O  $1,500.00  $ 4,415.50  OP
TOTAL                                                    $17,775.50  $1,500.00  $19,275.50
3 CLAIMS   1 OPEN"""
CORE[5] = add("core", cell("US", "carrier loss run printout", "auto", "header + claim rows", "medium", 3, ocr=True),
              "gA:loss_run:ironvale-riskpoint", "loss_run", t)

# 6 Ironvale RiskPoint, US auto, long, with BI/PD split
c6 = [
    ("A2100533", "03/12/2021", "Intersection collision, BI claimant, unit 3", 48500.00, 0.00, "Closed"),
    ("A2101987", "09/27/2021", "Parked unit struck, PD only", 2310.00, 0.00, "Closed"),
    ("A2200414", "01/06/2022", "Jackknife on ice, I-80, cargo spill", 96400.00, 35000.00, "Open"),
    ("A2203351", "10/18/2022", "Mirror strike, opposing vehicle", 880.00, 0.00, "Closed"),
    ("A2300920", "04/02/2023", "Rollover at quarry exit, driver injured", 31275.00, 60000.00, "Open"),
]
p, r, i = tot(c6)
t = f"""IRONVALE INSURANCE COMPANY
RiskPoint Commercial Lines - Detailed Loss Run
Report Requested By: Hartwell & Pryce Insurance Services   Report ID: RP-LR-882091
Named Insured: Mesa Verde Freight Lines Inc.
Policy Number: BA 2981140   Line of Business: Commercial Auto (Liability + Physical Damage)
Policy Periods Included: 02/01/2021 - 02/01/2024 (3 annual terms)
Valuation Date: 09/30/2026   Currency: USD   Deductible: $2,500 PD
Claim No | Date of Loss | Accident Description | Paid | Reserve | Incurred | Status
""" + "\n".join(claim_lines(c6, usd)) + f"""
Totals: 5 claims | Paid {usd(p)} | Reserve {usd(r)} | Incurred {usd(i)}
Open claims: 2   Closed claims: 3   Subrogation recovered: $0.00
Losses include allocated loss adjustment expense. Figures are not a guarantee of future experience.
Policy term 02/01/2024 - 02/01/2025 written by another carrier; contact prior carrier for loss information."""
CORE[6] = add("core", cell("US", "carrier loss run printout", "auto", "header + claim rows", "long", 3),
              "gA:loss_run:ironvale-riskpoint", "loss_run", t)

# 7 Corvane CCS Online TPA, US WC, medium, indemnity/medical/expense
t = """CORVANE CLAIMS SERVICES  |  CCS Online  |  Workers' Compensation Loss Run
Client: Ridgeline Senior Living Group   Carrier: Bluestem Indemnity Co.   Policy: WC 55-0091273
Policy Period: 04/01/2023 - 04/01/2026   Valuation Date: 09/30/2026
Claim # | DOI | Injury / Cause | Indemnity Paid | Medical Paid | Expense | O/S | Total Incurred | Status
CC-23-40118 | 06/12/2023 | Lifting resident, lumbar strain | $9,840 | $14,310 | $1,250 | $0 | $25,400 | Closed
CC-24-10552 | 01/30/2024 | Slip on wet floor, wrist fracture | $4,100 | $8,775 | $640 | $6,000 | $19,515 | Open
CC-25-02219 | 08/14/2025 | Needle stick, med only | $0 | $1,180 | $0 | $0 | $1,180 | Closed
Totals | | | $13,940 | $24,265 | $1,890 | $6,000 | $46,095 |"""
CORE[7] = add("core", cell("US", "TPA report", "workers comp", "header + claim rows", "medium", 3, ["Indemnity Paid", "Expense", "O/S"]),
              "gA:loss_run:corvane-ccsonline", "loss_run", t)

# 8 Corvane, US WC, short, no claims this period
t = """CORVANE CLAIMS SERVICES - CCS Online Loss Run. Client: Pruitt Landscaping Co. WC 55-0104418. Period 07/01/2023 - 07/01/2026. Valued 09/30/2026. NO CLAIMS THIS PERIOD. Total Paid $0.00 | O/S $0.00."""
CORE[8] = add("core", cell("US", "TPA report", "workers comp", "no claims this period", "short", 3, ["O/S"], incurred_word=False),
              "gA:loss_run:corvane-ccsonline", "loss_run", t)

# 9 Corvane, US WC, long, 10 years totals by year
yrs = [(2016, 3, 41200, 0), (2017, 1, 6850, 0), (2018, 0, 0, 0), (2019, 4, 77320, 0), (2020, 2, 15100, 0),
       (2021, 5, 102480, 3500), (2022, 2, 22600, 8000), (2023, 3, 18950, 21500), (2024, 1, 2400, 4600),
       (2025, 2, 3150, 38000)]
lines = []
for y, n, pd, os_ in yrs:
    lines.append(f"{y}-{y+1 - 2000:02d} | {n} | {usd0(pd)} | {usd0(os_)} | {usd0(pd + os_)}" if n else f"{y}-{y+1 - 2000:02d} | 0 | no claims this period | | ")
P = sum(y[2] for y in yrs); R = sum(y[3] for y in yrs); N = sum(y[1] for y in yrs)
t = f"""CORVANE CLAIMS SERVICES
CCS Online - Ten Year Loss Summary by Policy Year
Client: Tri-County Municipal Services Authority
Program: Self-Insured Workers' Compensation with excess (SIR $500,000)
Excess Carrier: Bluestem Indemnity Co.   Policy Years: 07/01/2016 - 07/01/2026
Valuation Date: 09/30/2026   Prepared for renewal marketing, figures ground-up within SIR
Policy Year | Claim Count | Total Paid | Outstanding | Total Incurred
""" + "\n".join(lines) + f"""
10-Year Total | {N} | {usd0(P)} | {usd0(R)} | {usd0(P + R)}
Open claims at valuation: 6. Largest single claim: 2021-22, police officer knee injury, {usd0(64000)} incurred.
No claim in the period has pierced the self-insured retention. Detailed claim listing available on request.
Reported claims only; IBNR not included. Prepared by Corvane Claims Services account management."""
CORE[9] = add("core", cell("US", "TPA report", "workers comp", "totals by policy year only, no-claims row", "long", 10),
              "gA:loss_run:corvane-ccsonline", "loss_run", t)

# 10 Meridale Marine, UK marine, medium, no incurred word
t = """MERIDALE MARINE UNDERWRITERS LTD
Claims Experience Statement - Marine Cargo
Assured: Penhallow Seafoods Ltd     Policy: MMU/CG/22/04417
Period: 01/04/2021 to 31/03/2026     Prepared: 30/09/2026     Currency: GBP
Claim Ref | Date of Loss | Voyage / Circumstances | Paid | Outstanding | Total | Status
MC21-0381 | 14/08/2021 | Reefer failure, Vigo to Felixstowe, frozen product | £42,180 | £0 | £42,180 | Settled
MC23-0107 | 02/02/2023 | Container wet damage, Aberdeen transhipment | £6,940 | £0 | £6,940 | Settled
MC25-0219 | 19/07/2025 | Temperature deviation, Rotterdam, survey awaited | £0 | £18,500 | £18,500 | Open
Totals | | | £49,120 | £18,500 | £67,620 |
Years 2022/23 and 2024/25: nil claims."""
CORE[10] = add("core", cell("UK", "insurer claims experience statement", "marine", "header + claim rows", "medium", 5, ["Outstanding"], incurred_word=False),
               "gA:loss_run:meridale-marine-ces", "loss_run", t)

# 11 Meridale, UK marine, short
t = """MERIDALE MARINE UNDERWRITERS - Claims Experience. Assured: Tregenna Boatyard Ltd. Hull & Machinery, 3 years to 31/03/2026. 1 claim: 11/11/2024 grounding, Fal estuary, paid £23,600, O/S £4,000, total £27,600, open. Valued 30/09/2026."""
CORE[11] = add("core", cell("UK", "insurer claims experience statement", "marine", "header + claim rows", "short", 3, ["O/S"], incurred_word=False),
               "gA:loss_run:meridale-marine-ces", "loss_run", t)

# 12 Thistlewood, UK property, medium
t = """THISTLEWOOD INSURANCE PLC
Commercial Property - Claims Experience
Policyholder: Ardgowan Textiles Ltd   Policy No: TW/CP/0058831
Policy Years: 01/03/2021 - 28/02/2026   Data as at: 30/09/2026
Claim No | Date of Loss | Peril / Description | Paid | O/S Reserve | Incurred | Open/Closed
TCP-21-6602 | 17/12/2021 | Escape of water, dye house mezzanine | £27,450 | £0 | £27,450 | Closed
TCP-23-1185 | 05/06/2023 | Theft of copper cabling, yard | £3,120 | £0 | £3,120 | Closed
TCP-24-0973 | 28/10/2024 | Storm, roof sheets lifted, stock wetted | £58,300 | £21,700 | £80,000 | Open
Total 3 claims | | | £88,870 | £21,700 | £110,570 |"""
CORE[12] = add("core", cell("UK", "insurer claims experience statement", "property", "header + claim rows", "medium", 5, ["O/S"]),
               "gA:loss_run:thistlewood-claims-exp", "loss_run", t)

# 13 Thistlewood, UK property, long, scanned OCR
t = """THlSTLEWOOD INSURANCE PLC                                   CLAIMS EXPERIENCE
Policyholder : Kilbarchan Cold Store Ltd          Policy No : TW/CP/0047120
Address : Unit 7, Linwood Road Trading Estate, Paisley
Period of review : 01/09/2019 - 31/08/2025 (6 years)       Valued as at : 3O/09/2026
Basis : Material damage and business interruption combined, gross of excess (£2,500)

Claim No     D.O.L.       Description                                 Paid       O/S       Incurred   Status
TCP-19-4410  22/11/2019   Ammonia leak, plant room, stock spoiled     £64,800    £0        £64,800    C
TCP-20-0911  09/04/2020   Forklift impact, racking collapse aisle 4   £12,350    £0        £12,350    C
             2020/21 & 2021/22   NO CLAIMS
TCP-22-7728  30/08/2022   Power outage, refrigeration failure, BI     £118,200   £0        £118,200   C
TCP-24-3302  14/01/2024   Roof leak over loading dock                 £4,060     £1,940    £6,000     O
TCP-25-0156  03/03/2025   Malicious damage, gatehouse windows         £1,275     £0        £1,275     C

TOTAL (5 claims)                                                    £200,685   £1,940    £202,625
Largest loss 2022 power outage: recovery from distribution network operator under review, not reflected above.
Th1s statement is provided for underwriting purposes only and is accurate as at the date shown.
Prepared by Claims Information Unit, Thistlewood Insurance plc, Glasgow office."""
CORE[13] = add("core", cell("UK", "insurer claims experience statement", "property", "header + claim rows, no-claims row", "long", 6, ["O/S"], ocr=True),
               "gA:loss_run:thistlewood-claims-exp", "loss_run", t)

# 14 Cobalt Shore, US product liability, medium
t = """COBALT SHORE SPECIALTY INSURANCE CO.  -  PL Register Loss Run
Insured: Vantor Kitchen Appliances Corp.    Policy: PL 04-7781209
Coverage: Products / Completed Operations   Policy Periods: 05/15/2021 - 05/15/2026
Valuation Date: 09/30/2026
Claim No | Date of Loss | Product / Allegation | Paid (Ind) | Expense Paid | Reserve | Incurred | Status
PL21-0044 | 12/02/2021 | Pressure cooker lid failure, burn injury | $72,500 | $18,300 | $0 | $90,800 | Closed
PL23-0170 | 07/21/2023 | Toaster oven fire, kitchen damage, subrogated claim | $0 | $6,200 | $41,000 | $47,200 | Open
PL24-0091 | 03/09/2024 | Blender blade detachment, laceration | $15,000 | $4,450 | $0 | $19,450 | Closed
Totals | | | $87,500 | $28,950 | $41,000 | $157,450 |"""
CORE[14] = add("core", cell("US", "carrier loss run printout", "product liability", "header + claim rows", "medium", 5, ["Expense"]),
               "gA:loss_run:cobaltshore-plregister", "loss_run", t)

# 15 Cobalt Shore, short, no claims
t = """COBALT SHORE SPECIALTY - PL Register. Insured: Glenrock Outdoor Gear LLC. PL 04-8013377. 08/01/2022-08/01/2026. Valuation 09/30/2026. No claims reported for the periods shown. Total incurred: $0."""
CORE[15] = add("core", cell("US", "carrier loss run printout", "product liability", "no claims this period", "short", 4),
               "gA:loss_run:cobaltshore-plregister", "loss_run", t)

# 16 Elmstead ClaimsHub, UK GL (public liability), medium
t = """ELMSTEAD ASSURANCE UK LIMITED   ClaimsHub Report
Insured: Brockley Hythe Leisure Ltd t/a Riverside Lido   Policy: EA/PL/7716045
Cover: Public & Products Liability   Policy Periods: 01/05/2022 - 30/04/2026
Valuation Date: 30/09/2026
Claim Ref | Loss Date | Circumstances | Paid | Outstanding | Incurred | Status
EA-PL-22-3381 | 13/08/2022 | Member slipped on poolside, fractured ankle | £14,200 | £0 | £14,200 | Closed
EA-PL-24-0428 | 26/05/2024 | Child injured on changing room door | £2,750 | £9,250 | £12,000 | Open
EA-PL-25-1103 | 02/07/2025 | Lost property claim, jewellery from locker | £480 | £0 | £480 | Closed
Total | | | £17,430 | £9,250 | £26,680 |
2023/24 policy year: no claims notified."""
CORE[16] = add("core", cell("UK", "carrier loss run printout", "GL", "header + claim rows, no-claims row", "medium", 4, ["Outstanding"]),
               "gA:loss_run:elmstead-claimshub", "loss_run", t)

# 17 Elmstead, UK, short, totals only, no incurred word
t = """ELMSTEAD ASSURANCE - ClaimsHub summary, Corrie Lane Joinery Ltd, EA/PL/7720981, at 30/09/2026
Year | No. | Paid | O/S | Total
2022/23 | 0 | £0 | £0 | £0
2023/24 | 1 | £6,300 | £0 | £6,300
2024/25 | 1 | £0 | £15,000 | £15,000"""
CORE[17] = add("core", cell("UK", "carrier loss run printout", "GL", "totals by policy year only", "short", 3, ["O/S"], incurred_word=False),
               "gA:loss_run:elmstead-claimshub", "loss_run", t)

# 18 Quillon Q-Report TPA, UK EL, medium
t = """QUILLON RISK SERVICES LTD  (TPA)  Q-Report: Claims Listing
Client: Morwick Precision Engineering Ltd    Insurer: Sedgemoor General Insurance plc
Policy: Employers' Liability SGI/EL/330719    Periods: 01/01/2021 - 31/12/2025
Data valued at 30/09/2026
Claim | Date of Incident | Injury / Cause | Indemnity Paid | Costs Paid | O/S | Total Inc. | Status
QRS-EL-21-0090 | 16/03/2021 | Hand caught in press brake, partial amputation | £68,000 | £21,400 | £0 | £89,400 | Closed
QRS-EL-23-0412 | 04/09/2023 | Noise induced hearing loss, 22 yr exposure | £0 | £3,800 | £26,200 | £30,000 | Open
QRS-EL-24-0217 | 21/02/2024 | Manual handling, shoulder strain | £4,500 | £1,900 | £0 | £6,400 | Closed
Totals | | | £72,500 | £27,100 | £26,200 | £125,800 |"""
CORE[18] = add("core", cell("UK", "TPA report", "workers comp", "header + claim rows", "medium", 5, ["Indemnity Paid", "O/S", "Total Inc."]),
               "gA:loss_run:quillon-qreport", "loss_run", t)

# 19 Quillon, UK motor fleet, long
c19 = [
    ("QRS-MF-21-1102", "07/06/2021", "TP rear-ended at lights, A38, TP injury", 18450, 0, "Closed"),
    ("QRS-MF-21-1730", "29/10/2021", "Own damage, van reversed into bollard", 2140, 0, "Closed"),
    ("QRS-MF-22-0388", "11/03/2022", "Windscreen replacement", 395, 0, "Closed"),
    ("QRS-MF-23-0914", "19/05/2023", "Multi-vehicle collision M5 J25, TP credit hire", 37800, 22000, "Open"),
    ("QRS-MF-24-0051", "08/01/2024", "Theft of tools from locked van, overnight", 3600, 0, "Closed"),
    ("QRS-MF-25-0677", "15/04/2025", "TP alleges side-swipe, liability disputed", 0, 8500, "Open"),
]
p, r, i = tot(c19)
t = f"""QUILLON RISK SERVICES LTD
Q-Report  |  Motor Fleet Claims Experience  |  Report generated 01/10/2026
Client: Hembury Facilities Management Ltd     Fleet size: 64 vehicles (LCVs and cars)
Insurer: Sedgemoor General Insurance plc      Policy: SGI/MF/118842
Periods: 01/06/2020 - 31/05/2026 (6 years)    Valued as at 30/09/2026
Excess: £500 own damage, £250 windscreen
Claim Ref | Date of Loss | Circumstances | Paid | O/S | Incurred | Status
""" + "\n".join(claim_lines(c19, gbp)) + f"""
Totals | 6 claims | | {gbp(p)} | {gbp(r)} | {gbp(i)} |
Period 01/06/2020 - 31/05/2021: no claims.
Frequency: 1.0 claims per year. Average incurred per claim {gbp(i / 6)}.
Credit hire exposure on QRS-MF-23-0914 reserved at insurer's estimate; figures subject to development.
Quillon Risk Services acts as claims handler on behalf of the insurer and accepts no liability for decisions based on this report."""
CORE[19] = add("core", cell("UK", "TPA report", "auto", "header + claim rows, no-claims row", "long", 6, ["O/S"]),
               "gA:loss_run:quillon-qreport", "loss_run", t)

# 20 Delacourt broker loss summary, US GL, medium
t = """DELACOURT RISK PARTNERS
Loss Summary prepared for renewal marketing
Client: Hollis & Crane Event Staffing Inc.   Carrier: Pinewick National Insurance Co.
Line: Commercial General Liability   Policy: CGL 7092215   Valued: 09/30/2026 (per carrier runs)
Policy Year | Claim # | DOL | Description | Paid | Reserve | Incurred | Open/Closed
2021-22 | 71-00992 | 10/09/2021 | Guest assaulted by attendee, negligent security alleged | $40,000 | $0 | $40,000 | Closed
2022-23 | none | | | | | |
2023-24 | 71-02218 | 06/17/2023 | Staff member dropped tray, guest burn | $5,600 | $0 | $5,600 | Closed
2024-25 | 71-03307 | 04/28/2025 | Stage barrier collapse, 3 claimants | $12,900 | $85,000 | $97,900 | Open
Total | | | | $58,500 | $85,000 | $143,500 |
Source: carrier loss runs dated 09/30/2026. Delacourt has not audited carrier data."""
CORE[20] = add("core", cell("US", "broker loss summary", "GL", "header + claim rows by year, no-claims row", "medium", 4),
               "gA:loss_run:delacourt-broker-summary", "loss_run", t)

# 21 Delacourt, US property, short
t = """Delacourt Risk Partners - Loss Summary | Ferro Valley Machine Works | Property | Valued 08/31/2026
PY | # | Paid | Reserve | Incurred
2022 | 1 | $22,400 | $0 | $22,400
2023 | 0 | - | - | -
2024 | 1 | $3,750 | $1,250 | $5,000"""
CORE[21] = add("core", cell("US", "broker loss summary", "property", "totals by policy year only", "short", 3),
               "gA:loss_run:delacourt-broker-summary", "loss_run", t)

# 22 Fernhollow broker summary UK property, medium, no incurred
t = """FERNHOLLOW INSURANCE BROKERS LTD
Claims Summary for: Lowther Street Bakeries Ltd
Insurer: Thistlewood Insurance plc   Cover: Commercial Combined (Property section)
Period: 5 years to 24/06/2026        Source: insurer claims data at 31/08/2026
Date of Loss | Description | Paid | Outstanding | Total loss | Status
03/02/2022 | Oven fire, production line 2 | £31,600 | £0 | £31,600 | Settled
19/08/2023 | Flood, basement stores | £9,450 | £2,050 | £11,500 | Open
24/12/2024 | Break-in, safe and till damage | £1,880 | £0 | £1,880 | Settled
Total | | £42,930 | £2,050 | £44,980 |
No other claims notified in the period."""
CORE[22] = add("core", cell("UK", "broker loss summary", "property", "header + claim rows", "medium", 5, ["Outstanding", "Total loss"], incurred_word=False),
               "gA:loss_run:fernhollow-broker-summary", "loss_run", t)

# 23 Fernhollow, UK motor short
t = """Fernhollow Insurance Brokers - claims summary, Carrick Taxis Ltd, motor fleet, 3 yrs to 31/07/2026: 2 claims. 14/03/2024 TP collision, paid £7,200, O/S £0. 02/05/2025 own damage, paid £2,950, O/S £1,000. Total £11,150."""
CORE[23] = add("core", cell("UK", "broker loss summary", "auto", "inline claim rows", "short", 3, ["O/S"], incurred_word=False),
               "gA:loss_run:fernhollow-broker-summary", "loss_run", t)

# 24 Sabledown FleetLoss, US auto, medium, O/S
t = """SABLEDOWN GENERAL INSURANCE CO.   FleetLoss Report
Insured: Arroyo Linen & Uniform Service   Policy #: CA 66-310442
Term(s): 03/01/2023 - 03/01/2026   Val Dt: 09/30/2026
Claim No | DOL | Veh | Description | Paid | O/S | Incurred | Stat
FL-23-88120 | 08/21/2023 | 2019 Isuzu NPR | Struck pedestrian in lot, minor injury | $11,300 | $0 | $11,300 | C
FL-24-90815 | 12/03/2024 | 2021 Ford Transit | Sideswipe, PD to third party | $4,725 | $0 | $4,725 | C
FL-25-01177 | 01/14/2025 | 2020 Isuzu NPR | Rear-end, claimant attorney rep | $2,100 | $32,900 | $35,000 | O
Totals | | | | $18,125 | $32,900 | $51,025 |"""
CORE[24] = add("core", cell("US", "carrier loss run printout", "auto", "header + claim rows", "medium", 3, ["O/S"]),
               "gA:loss_run:sabledown-fleetloss", "loss_run", t)

# 25 Sabledown, short faxed
t = """SABLEDOWN GEN INS  FLEETLOSS   lnsd: QUIK-HAUL MOVERS LLC  CA 66-298O51  VAL 09/30/2026
FL-24-77310  06/06/2024  BACKED INTO CARPORT  PD $3,410  O/S $0  INC $3,410  CLSD
NO OTHER CLAIMS 03/01/2022-03/01/2026"""
CORE[25] = add("core", cell("US", "carrier loss run printout", "auto", "header + claim rows", "short", 4, ["O/S", "INC"], ocr=True, incurred_word=False),
               "gA:loss_run:sabledown-fleetloss", "loss_run", t)

# 26 Westmarch Comp Ledger, US WC, medium, 4 years
t = """WESTMARCH INDEMNITY COMPANY - Comp Ledger Loss Run
Employer: Calderon Framing & Drywall Inc.   FEIN on file   Policy: WCX 4410278
State: AZ   Policy Periods: 01/01/2022 - 01/01/2026   Valued As Of: 09/30/2026
Claim # | Inj Date | Body Part / Nature | Med Paid | Ind Paid | Reserve | Total Incurred | Status
CL22-00315 | 04/11/2022 | Fall from ladder, wrist | $6,820 | $3,300 | $0 | $10,120 | Closed
CL23-01142 | 09/05/2023 | Nail gun puncture, hand | $2,140 | $0 | $0 | $2,140 | Closed
CL24-00287 | 02/26/2024 | Back strain carrying sheet rock | $9,410 | $11,600 | $18,000 | $39,010 | Open
CL25-00913 | 07/30/2025 | Eye, debris | $1,050 | $0 | $0 | $1,050 | Closed
Totals | | | $19,420 | $14,900 | $18,000 | $52,320 |"""
CORE[26] = add("core", cell("US", "carrier loss run printout", "workers comp", "header + claim rows", "medium", 4, ["Ind Paid"]),
               "gA:loss_run:westmarch-compledger", "loss_run", t)

# 27 Westmarch, long, WC multi-state, by policy year with claims and lost time
c27 = [
    ("2020-21", "CL20-00410", "05/02/2020", "Lost time, knee, slipped on loading ramp", 28400, 0, "Closed"),
    ("2020-21", "CL20-01007", "11/19/2020", "Medical only, laceration, box cutter", 920, 0, "Closed"),
    ("2021-22", "CL21-00655", "08/08/2021", "Lost time, rotator cuff, repetitive lifting", 51300, 0, "Closed"),
    ("2022-23", "CL22-01290", "03/14/2023", "Medical only, sprained ankle", 1480, 0, "Closed"),
    ("2023-24", "CL23-00118", "02/02/2024", "Lost time, forklift tip-over, crush injury", 88700, 145000, "Open"),
    ("2024-25", "CL24-00942", "12/09/2024", "Medical only, heat exhaustion", 2210, 0, "Closed"),
]
lines = [f"{py} | {no} | {d} | {ds} | {usd0(pd)} | {usd0(rs)} | {usd0(pd + rs)} | {st}" for py, no, d, ds, pd, rs, st in c27]
P = sum(c[4] for c in c27); R = sum(c[5] for c in c27)
t = f"""WESTMARCH INDEMNITY COMPANY
Comp Ledger - Workers' Compensation Loss Run, All Claims, All States
Employer: Sorrento Valley Produce Distributors Inc.
Policy: WCX 3907716 (renewal series)   States: CA, NV
Policy Periods: 01/01/2020 - 01/01/2026 (6 years)   Valued As Of: 09/30/2026
Experience Mod (current): 1.08   Payroll basis on file with underwriting
Pol Yr | Claim # | DOI | Type / Description | Total Paid | Reserve | Total Incurred | Status
""" + "\n".join(lines) + f"""
2025-26 | - | - | No claims this period | $0 | $0 | $0 |
Totals | 6 claims (3 lost time, 3 medical only) | | | {usd0(P)} | {usd0(R)} | {usd0(P + R)} |
Open claim CL23-00118 is in litigation; reserve reviewed 09/2026.
Medical-only claims under $2,500 are reported at 30% for experience rating purposes in CA.
This loss run is confidential and furnished at the request of the insured's agent of record."""
CORE[27] = add("core", cell("US", "carrier loss run printout", "workers comp", "header + claim rows by year, no-claims row", "long", 6),
               "gA:loss_run:westmarch-compledger", "loss_run", t)

# 28 Orrin Bay Claimsight TPA, US GL, medium
t = """ORRIN BAY CLAIMS ADMINISTRATORS  -  Claimsight
Loss Run for: Lakeview Property Management Co.  |  Carrier: Halcourt Specialty Insurance Co.
Policy: HSI-GL-210887   GL Occurrence   Periods: 09/01/2022 - 09/01/2026   As of 09/30/2026
Claim No. | Date of Loss | Loss Description | Indemnity Paid | Expense | Outstanding | Total Incurred | Status
OB-22-5130 | 12/27/2022 | Tenant fall on icy walkway, Bldg C | $21,000 | $7,850 | $0 | $28,850 | Closed
OB-24-2091 | 05/15/2024 | Dog bite in common area, guest | $0 | $2,400 | $17,600 | $20,000 | Open
OB-25-0716 | 03/03/2025 | Mold exposure allegation, unit 14B | $0 | $5,100 | $44,900 | $50,000 | Open
Totals | | | $21,000 | $15,350 | $62,500 | $98,850 |
Policy year 09/01/2023-24: no reported claims."""
CORE[28] = add("core", cell("US", "TPA report", "GL", "header + claim rows, no-claims row", "medium", 4, ["Indemnity Paid", "Expense", "Outstanding"]),
               "gA:loss_run:orrinbay-claimsight", "loss_run", t)

# 29 Orrin Bay, US product liability, short
t = """Orrin Bay Claimsight | Insured: Tavish Toy Imports | Products Liability | 2023-2026 | As of 09/30/2026
OB-24-3318 | 10/30/2024 | Choking hazard, small part | Pd $0 | Exp $1,850 | O/S $25,000 | Inc $26,850 | Open"""
CORE[29] = add("core", cell("US", "TPA report", "product liability", "header + claim rows", "short", 3, ["O/S", "Inc", "Expense"], incurred_word=False),
               "gA:loss_run:orrinbay-claimsight", "loss_run", t)

# 30 Calloway Marine, UK marine cargo, long, 7 years, no incurred
c30 = [
    ("CMG/C/19/112", "21/05/2019", "Theft from container, Felixstowe port", 12300, 0, "Settled"),
    ("CMG/C/20/045", "09/03/2020", "Rough handling, machinery parts damaged", 7840, 0, "Settled"),
    ("CMG/C/21/301", "30/11/2021", "General average contribution, MV fire at sea", 26900, 0, "Settled"),
    ("CMG/C/23/077", "17/04/2023", "Water ingress, flat rack, steel coils rusted", 15600, 0, "Settled"),
    ("CMG/C/24/190", "06/09/2024", "Container lost overboard, North Sea", 0, 61000, "Outstanding"),
]
lines = [f"{no} | {d} | {ds} | {gbp(pd)} | {gbp(os_)} | {gbp(pd + os_)} | {st}" for no, d, ds, pd, os_, st in c30]
P = sum(c[3] for c in c30); R = sum(c[4] for c in c30)
t = f"""CALLOWAY MARINE & GENERAL INSURANCE COMPANY LIMITED
CLAIMS EXPERIENCE - MARINE CARGO OPEN COVER
Assured: Brennock Engineering Exports Ltd       Open Cover No: CMG/OC/0912
Declaration basis: all shipments, UK exports and imports, institute cargo clauses (A)
Period under review: 01/01/2019 - 31/12/2025 (7 underwriting years)
Statement date: 30/09/2026       Currency: GBP (USD claims converted at settlement rate)
Claim No | Date of Loss | Circumstances | Paid | Outstanding | Total | Status
""" + "\n".join(lines) + f"""
2022 and 2025 underwriting years: NIL claims
Totals 7 years | 5 claims | | {gbp(P)} | {gbp(R)} | {gbp(P + R)} |
Recoveries from carriers under Hague-Visby rules: £4,100 received (2019 theft), not netted above.
The outstanding figure for CMG/C/24/190 is an estimate pending salvage report.
Issued by Calloway Marine & General claims department for the attention of the assured's broker."""
CORE[30] = add("core", cell("UK", "insurer claims experience statement", "marine", "header + claim rows, nil-claims row", "long", 7, ["Outstanding"], incurred_word=False),
               "gA:loss_run:calloway-marine-ces", "loss_run", t)

# 31 Calloway, UK hull short
t = """CALLOWAY MARINE & GENERAL - Claims Experience, Hull. Assured: Skerray Fishing Co Ltd, MFV Aurora Bay. 01/01/2023-31/12/2025. Nil claims all years. Paid £0, Outstanding £0. Statement 30/09/2026."""
CORE[31] = add("core", cell("UK", "insurer claims experience statement", "marine", "no claims this period", "short", 3, ["Outstanding"], incurred_word=False),
               "gA:loss_run:calloway-marine-ces", "loss_run", t)

# 32 Ambergate AMBER claims, UK motor, medium
t = """AMBERGATE INSURANCE LTD  -  AMBER Claims Experience Report
Policyholder: Quayside Couriers (Bristol) Ltd   Policy: AMB-MF-0440917
Motor Fleet, 22 vehicles   Periods: 01/02/2022 - 31/01/2026   Valuation date: 30/09/2026
Claim No. | Incident Date | Reg | Description | Paid | Reserve | Incurred | Status
AMB-22-71104 | 18/05/2022 | WX19 KDF | Hit parked car, Gloucester Rd | £3,240 | £0 | £3,240 | Closed
AMB-23-64400 | 01/12/2023 | WR21 PLA | Cyclist collision, injury claim | £9,800 | £14,200 | £24,000 | Open
AMB-24-10928 | 27/03/2024 | WX19 KDF | Windscreen | £310 | £0 | £310 | Closed
AMB-25-55017 | 09/09/2025 | WU22 HTE | Stolen from depot, recovered damaged | £6,450 | £0 | £6,450 | Closed
Total | | | | £19,800 | £14,200 | £34,000 |"""
CORE[32] = add("core", cell("UK", "carrier loss run printout", "auto", "header + claim rows", "medium", 4),
               "gA:loss_run:ambergate-amber", "loss_run", t)

# 33 Ambergate short, no claims
t = """AMBERGATE INSURANCE - AMBER claims report. Policyholder: Ferncastle Florists Ltd. Motor, 4 vehicles. 01/02/2023 - 31/01/2026. NO CLAIMS THIS PERIOD. Incurred £0. Valued 30/09/2026."""
CORE[33] = add("core", cell("UK", "carrier loss run printout", "auto", "no claims this period", "short", 3),
               "gA:loss_run:ambergate-amber", "loss_run", t)

# 34 Hollinsworth legacy, US property, faxed OCR, all caps, medium
t = """HOLLINSWORTH MUTUAL FIRE INS CO     LOSS HISTORY - LEGACY SYSTEM     PAGE 1
INSURED: ST. BRENDAN PARISH & SCHOOL CORP        POLICY: HMF-CP-00918822
POLICY PERIOD: 07/01/2020 TO 07/01/2025          VALUATION DATE: O9/30/2026
CLAIM NO    DATE LOSS   CAUSE                          PAID         RESERVE    INCURRED     ST
2O-114092   08/14/2020  LIGHTNING, BELL TOWER           $ 46,300.00  $     0.00 $ 46,300.00  C
21-120117   02/16/2021  FROZEN PIPES, SCHOOL GYM        $ 88,915.00  $     0.00 $ 88,915.00  C
23-131560   06/30/2023  HAIL, SLATE ROOF RECTORY        $ 19,400.00  $ 7,600.00 $ 27,000.00  O
** TOTAL **                                             $154,615.00  $ 7,600.00 $162,215.00
P0LICY YEAR 2021-22, 2022-23, 2024-25 NO LOSSES"""
CORE[34] = add("core", cell("US", "carrier loss run printout", "property", "header + claim rows, no-claims row", "medium", 5, ocr=True),
               "gA:loss_run:hollinsworth-legacy", "loss_run", t)

# 35 Hollinsworth short
t = """HOLLINSWORTH MUTUAL FIRE - LOSS HISTORY. INSD: CEDAR KNOLL APARTMENTS. HMF-CP-01022410. 2023-2026. CLM 24-140771 03/03/2024 KITCHEN FIRE UNIT 2B PAID $31,200 RES $0 INCURRED $31,200 CLOSED. VAL 09/30/2026."""
CORE[35] = add("core", cell("US", "carrier loss run printout", "property", "header + claim rows", "short", 3),
               "gA:loss_run:hollinsworth-legacy", "loss_run", t)

# 36 Verdant Plains WCNet, US WC, short
t = """Verdant Plains Insurance Co. WCNet Loss Run | Employer: Bluff City Bakery Inc | WC 81-447210 | 10/01/2023-10/01/2026 | Val 09/30/2026
VP-24-2210 | 01/11/2024 | Burn, oven door | Med $3,450 | Ind $0 | Res $0 | Inc $3,450 | Closed
VP-25-0981 | 06/20/2025 | Slip, back strain | Med $5,200 | Ind $2,800 | Res $4,000 | Inc $12,000 | Open"""
CORE[36] = add("core", cell("US", "carrier loss run printout", "workers comp", "header + claim rows", "medium", 3, ["Inc"], incurred_word=False),
               "gA:loss_run:verdantplains-wcnet", "loss_run", t)

# 37 Crestmoor UWA, UK GL claims experience, medium
t = """CRESTMOOR UNDERWRITING AGENCY LIMITED
On behalf of participating insurers
CLAIMS EXPERIENCE  -  Liability (Employers' & Public)
Insured: Pennard Scaffolding Services Ltd    Agreement ref: CUA/LIA/2210/88
Years: 2021 - 2025    As at 30/09/2026    Currency GBP
Year | Claim | Date | Section | Description | Paid | Reserve | Incurred | Status
2021 | CUA-L-4410 | 12/07/2021 | PL | Falling fitting struck pedestrian | £18,600 | £0 | £18,600 | Closed
2022 | NIL | | | | | | |
2023 | CUA-L-5102 | 22/02/2023 | EL | Operative fell from lift, fractured pelvis | £42,000 | £38,000 | £80,000 | Open
2024 | CUA-L-5560 | 03/10/2024 | PL | Vehicle damaged by tube, Swansea High St | £1,940 | £0 | £1,940 | Closed
2025 | NIL | | | | | | |
Total | 3 claims | | | | £62,540 | £38,000 | £100,540 |"""
CORE[37] = add("core", cell("UK", "insurer claims experience statement", "GL", "header + claim rows by year, nil rows", "medium", 5),
               "gA:loss_run:crestmoor-uwa-ces", "loss_run", t)

# 38 Halvard PL register, US product liability, long
c38 = [
    ("HS-PL-17-0081", "02/03/2017", "E-bike battery thermal runaway, garage fire", 0, 0, 215000, "Closed"),
    ("HS-PL-18-0207", "09/12/2018", "Folding frame hinge failure, rider fall", 0, 0, 42500, "Closed"),
    ("HS-PL-20-0033", "01/25/2020", "Brake lever fracture, collision", 0, 0, 18750, "Closed"),
    ("HS-PL-22-0142", "07/04/2022", "Charger overheating, apartment smoke damage", 0, 26000, 11200, "Open"),
    ("HS-PL-24-0019", "03/18/2024", "Class action notice, battery recall (precautionary)", 0, 150000, 34500, "Open"),
]
# fields: no, dol, desc, _, reserve, paid
lines = [f"{no} | {d} | {ds} | {usd0(pd)} | {usd0(rs)} | {usd0(pd + rs)} | {st}" for no, d, ds, _, rs, pd, st in c38]
P = sum(c[5] for c in c38); R = sum(c[4] for c in c38)
t = f"""HALVARD SPECIALTY INSURANCE COMPANY
Product Liability Loss Register - Insured Copy
Named Insured: Velocane Micromobility Inc. (and subsidiaries)
Policy Series: HSPL-5520-xx   Coverage: Products-Completed Operations, Claims-Made, Retro Date 01/01/2015
Policy Periods Reported: 01/01/2016 - 01/01/2026 (10 years)
Valuation Date: 09/30/2026   Self-Insured Retention: $25,000 per claim (included below)
Claim No | Date of Loss | Product / Allegation | Paid (Loss + ALAE) | Reserve | Incurred | Status
""" + "\n".join(lines) + f"""
Policy years 2016, 2019, 2021, 2023 and 2025: no claims reported.
Totals 10 years | 5 claims | | {usd0(P)} | {usd0(R)} | {usd0(P + R)} |
The 2024 recall matter is reserved at the defense estimate only; indemnity exposure not yet evaluated.
Claim counts include incidents reported but not yet asserted as claims. Values are gross of SIR.
Issued by Halvard Specialty claims operations at the request of the named insured."""
CORE[38] = add("core", cell("US", "carrier loss run printout", "product liability", "header + claim rows, no-claims row", "long", 10),
               "gA:loss_run:halvard-plregister", "loss_run", t)

# 39 Kellbrook LossNet, US GL, medium, no incurred, Total Loss
t = """KELLBROOK CASUALTY INSURANCE CO.
LossNet Claim Detail     Valuation: 09/30/2026
Insured: Northfork Brewing Cooperative     Policy No.: KCG 118-30447
Line: General Liability incl. Liquor Liability     Terms: 11/01/2022 - 11/01/2025
Claim | Loss Date | Description | Paid to Date | Outstanding | Total Loss | Status
KC-23-00411 | 02/11/2023 | Over-served patron, single vehicle accident, dram shop claim | $95,000 | $0 | $95,000 | Closed
KC-24-01790 | 08/23/2024 | Taproom patron cut by broken glass | $3,300 | $1,700 | $5,000 | Open
Total | | | $98,300 | $1,700 | $100,000 |
Term 11/01/2023 - 11/01/2024: no claims reported."""
CORE[39] = add("core", cell("US", "carrier loss run printout", "GL", "header + claim rows, no-claims row", "medium", 3, ["Outstanding", "Total Loss"], incurred_word=False),
               "gA:loss_run:kellbrook-lossnet", "loss_run", t)

# 40 Kellbrook, US inland marine short
t = """KELLBROOK CASUALTY - LossNet | Insured: Rio Seco Equipment Rental | Inland Marine / Contractors Equipment | IMK 220-0871 | 2022-2025 | Val 09/30/2026
KC-24-02215 | 05/19/2024 | Theft of skid steer from jobsite | Paid $41,500 | Reserve $0 | Incurred $41,500 | Closed"""
CORE[40] = add("core", cell("US", "carrier loss run printout", "marine", "header + claim rows", "short", 3),
               "gA:loss_run:kellbrook-lossnet", "loss_run", t)

# 41 Ravensworth TPA, US auto, medium
t = """RAVENSWORTH CLAIMS MANAGEMENT, INC. (Third Party Administrator)
Program: Brazos Valley School Transportation Pool   Member: Pecan Hollow ISD
Coverage: Auto Liability and Physical Damage   Fund Years: 09/01/2022 - 09/01/2026
Report Date: 10/01/2026   Valuation: 09/30/2026
Claim No | DOL | Unit | Description | Paid | Reserve | Incurred | Status
RCM-AL-22-1180 | 10/12/2022 | Bus 21 | Bus clipped parked vehicle at stop | $2,860 | $0 | $2,860 | Closed
RCM-AL-23-0702 | 04/04/2023 | Bus 08 | Student injured, sudden stop | $6,500 | $0 | $6,500 | Closed
RCM-PD-24-0331 | 01/22/2024 | Van 3 | Hail damage, district lot | $14,180 | $0 | $14,180 | Closed
RCM-AL-25-0904 | 11/07/2025 | Bus 15 | Rear-ended by pickup, subrogation pending | $1,950 | $3,050 | $5,000 | Open
Total | | | | $25,490 | $3,050 | $28,540 |"""
CORE[41] = add("core", cell("US", "TPA report", "auto", "header + claim rows", "medium", 4),
               "gA:loss_run:ravensworth-tpa", "loss_run", t)

# 42 Ravensworth TPA, US property, medium, totals by year only
t = """RAVENSWORTH CLAIMS MANAGEMENT, INC.
Property Fund Loss Summary by Fund Year (no claim detail)
Member: City of Arden Springs   Pool: Brazos Valley Municipal Property Pool
Valuation: 09/30/2026
Fund Year | Claims | Paid | Reserve | Incurred | Largest Loss
2020-21 | 4 | $63,210 | $0 | $63,210 | Winter storm, water plant
2021-22 | 2 | $8,900 | $0 | $8,900 | Lightning, traffic signals
2022-23 | 0 | $0 | $0 | $0 | -
2023-24 | 3 | $129,450 | $18,000 | $147,450 | Tornado, parks maintenance barn
2024-25 | 1 | $2,300 | $1,700 | $4,000 | Vandalism, library
Total | 10 | $203,860 | $19,700 | $223,560 |"""
CORE[42] = add("core", cell("US", "TPA report", "property", "totals by policy year only", "medium", 5),
               "gA:loss_run:ravensworth-tpa", "loss_run", t)

# 43 Brackenfield Syndicate, UK marine claims experience, medium
t = """BRACKENFIELD MARINE SYNDICATE MANAGEMENT
Claims Experience - Marine Liability (Port and Terminal Operators)
Assured: Kingsferry Terminal Services Ltd     Policy ref: BKM/TOL/23/0619
Years of account: 2021 - 2025     Figures at 30/09/2026     Currency: USD
YOA | Claim | Date of Loss | Description | Paid | O/S | Incurred
2021 | BKM-2021-0332 | 06/09/2021 | Crane dropped container, cargo damage | $84,200 | $0 | $84,200
2022 | - | - | Nil | $0 | $0 | $0
2023 | BKM-2023-0127 | 28/03/2023 | Stevedore injury on quay | $12,500 | $47,500 | $60,000
2024 | BKM-2024-0405 | 17/11/2024 | Reefer plug failure, perishables | $9,300 | $0 | $9,300
2025 | - | - | Nil | $0 | $0 | $0
Total | | | | $106,000 | $47,500 | $153,500"""
CORE[43] = add("core", cell("UK", "insurer claims experience statement", "marine", "header + claim rows by year, nil rows", "medium", 5, ["O/S"]),
               "gA:loss_run:brackenfield-syndicate-ces", "loss_run", t)

# 44 Dunmore carrier loss run UK property short
t = """DUNMORE GENERAL INSURANCE - LOSS LISTING | Insured: Gwaun Valley Holiday Cottages | Policy DGI/PR/55107 | 01/04/2023 - 31/03/2026 | Valued 30/09/2026
DG-24-1180 | 11/02/2024 | Storm damage to slate roof, cottage 3 | Paid £7,850 | O/S £650 | Incurred £8,500 | Open"""
CORE[44] = add("core", cell("UK", "carrier loss run printout", "property", "header + claim rows", "short", 3, ["O/S"]),
               "gA:loss_run:dunmore-losslisting", "loss_run", t)

assert len(rows) == 44

# ---------------- BOUNDARY ----------------
# Rule 13: no-known-loss letters signed by the insured
add("boundary", {"market": "US", "source": "no-known-loss letter", "line": "GL", "length": "medium", "signed_by": "insured officer"},
    "gA:loss_run:nkl-insured-letterhead", "loss_run", """
SPRINGWATER ORCHARDS LLC
4410 County Road 12, Hood Glen, OR 97031

September 22, 2026

To: Halcourt Specialty Insurance Co., c/o Tallis Grove Insurance Agency
Re: Statement of No Known Losses - Commercial General Liability

The undersigned, being an officer of Springwater Orchards LLC, hereby states that after inquiry there
have been no losses, claims, accidents or occurrences, reported or unreported, that may give rise to a
claim under the general liability coverage for the period 09/01/2021 through the date of this letter.

Signed: Marguerite Olafsen, Managing Member      Date: 09/22/2026
""", edge_rule=13)

add("boundary", {"market": "US", "source": "no-known-loss letter", "line": "property", "length": "short", "signed_by": "insured owner"},
    "gA:loss_run:nkl-insured-short", "loss_run", """
No Known Loss Letter. Insured: Lattimer Auto Glass Inc. I certify there have been no known property losses or claims from 01/01/2023 to 10/01/2026. Signed: Desmond Lattimer, President, 10/01/2026.
""", edge_rule=13)

add("boundary", {"market": "UK", "source": "no-known-loss letter", "line": "property", "length": "medium", "signed_by": "insured director"},
    "gA:loss_run:nkl-insured-uk-director", "loss_run", """
Calderbrook Joinery Limited
Unit 4, Mossbank Works, Hebden Royd HX7 5QT

15 October 2026

Dear Sirs,

Declaration of Claims Experience: Nil

We confirm that Calderbrook Joinery Limited has made no claims and is not aware of any incident,
loss or circumstance likely to give rise to a claim under its property, business interruption or
liability insurances for the five years from 1 November 2021 to the date of this letter. Our previous
insurer was Dunmore General Insurance. This declaration is given for the purpose of obtaining cover.

Yours faithfully,
Hamish Pargeter
Director, for and on behalf of Calderbrook Joinery Limited
""", edge_rule=13)

add("boundary", {"market": "UK", "source": "no-known-loss letter", "line": "workers comp", "length": "short", "signed_by": "insured company secretary", "ocr_noise": True},
    "gA:loss_run:nkl-insured-uk-scanned", "loss_run", """
NO KNOWN L0SS DECLARATION - Employers Liability. Insured: Ystrad Mill Care Homes Ltd. We declare no claims or known incidents 01/04/2022 to date. Signed: P. Gwilliam, Company Secretary. Dated 07/10/2026.
""", edge_rule=13)

# Rule 14: broker multi-carrier loss summary spreadsheets
add("boundary", {"market": "US", "source": "broker multi-carrier loss summary spreadsheet", "line": "GL", "length": "medium", "format": "sheet"},
    "gA:loss_run:mc-sheet-delacourt", "loss_run", """
DELACOURT RISK PARTNERS | Multi-Carrier Loss Summary | Client: Ponderosa Ridge Hospitality Group | Valued 09/30/2026
Policy Year | Carrier | Line | # Claims | Paid | Reserve | Incurred | Open
2021-22 | Pinewick National | GL | 2 | $18,400 | $0 | $18,400 | 0
2022-23 | Pinewick National | GL | 1 | $6,100 | $0 | $6,100 | 0
2023-24 | Halcourt Specialty | GL | 3 | $22,750 | $41,000 | $63,750 | 2
2024-25 | Halcourt Specialty | GL | 0 | $0 | $0 | $0 | 0
2025-26 | Kellbrook Casualty | GL | 1 | $1,200 | $8,800 | $10,000 | 1
Total | | | 7 | $48,450 | $49,800 | $98,250 | 3
""", edge_rule=14)

add("boundary", {"market": "US", "source": "broker multi-carrier loss summary spreadsheet", "line": "auto", "length": "medium", "format": "sheet"},
    "gA:loss_run:mc-sheet-tallisgrove", "loss_run", """
Tallis Grove Insurance Agency ; 5 Yr Loss Summary - All Carriers ; Insured: Cimarron Pipe & Supply
PY | Carrier | Pol # | Line | Clms | Pd | O/S | Tot Inc | Val Dt
2021 | Ironvale Ins Co | BA 2210045 | Auto | 3 | $27,300 | $0 | $27,300 | 09/30/26
2022 | Ironvale Ins Co | BA 2210045-1 | Auto | 2 | $9,880 | $0 | $9,880 | 09/30/26
2023 | Sabledown General | CA 66-330017 | Auto | 4 | $51,200 | $12,500 | $63,700 | 09/30/26
2024 | Sabledown General | CA 66-330017-1 | Auto | 1 | $3,400 | $16,600 | $20,000 | 09/30/26
2025 | Sabledown General | CA 66-330017-2 | Auto | 0 | $0 | $0 | $0 | 09/30/26
TOTAL | | | | 10 | $91,780 | $29,100 | $120,880 |
""", edge_rule=14)

add("boundary", {"market": "UK", "source": "broker multi-carrier loss summary spreadsheet", "line": "property", "length": "medium", "format": "sheet"},
    "gA:loss_run:mc-sheet-fernhollow", "loss_run", """
Fernhollow Insurance Brokers Ltd | Claims Summary (all insurers) | Client: Allanbank Retail Parks Ltd | Data to 30/09/2026
Year | Insurer | Section | Claims | Paid | Outstanding | Total | Notes
2021/22 | Thistlewood Insurance plc | Property Damage | 2 | £14,600 | £0 | £14,600 | EoW, glass
2022/23 | Thistlewood Insurance plc | Property Damage | 0 | £0 | £0 | £0 | nil
2023/24 | Dunmore General | Property Damage | 1 | £72,000 | £0 | £72,000 | Fire, unit 9
2024/25 | Dunmore General | Business Interruption | 1 | £18,250 | £11,750 | £30,000 | Fire, unit 9 BI
2025/26 | Elmstead Assurance UK | Property Damage | 1 | £2,100 | £0 | £2,100 | Vandalism
Total | | | 5 | £106,950 | £11,750 | £118,700 |
""", edge_rule=14)

add("boundary", {"market": "US", "source": "broker multi-carrier loss summary spreadsheet", "line": "workers comp", "length": "long", "format": "sheet", "multi_line": True},
    "gA:loss_run:mc-sheet-hartwellpryce", "loss_run", """
HARTWELL & PRYCE INSURANCE SERVICES | LOSS SUMMARY BY CARRIER AND LINE | Account: Granger Hill Nursery & Landscape Inc. | Prepared 10/05/2026 from carrier runs valued 09/30/2026
Line | Policy Year | Carrier | Policy No | Claim Count | Paid | Reserve | Incurred | Largest Claim
WC | 2021-22 | Westmarch Indemnity | WCX 3301872 | 4 | $33,900 | $0 | $33,900 | $21,000 back strain
WC | 2022-23 | Westmarch Indemnity | WCX 3301872-1 | 2 | $8,450 | $0 | $8,450 | $6,100 laceration
WC | 2023-24 | Verdant Plains Ins | WC 81-402266 | 5 | $47,800 | $26,000 | $73,800 | $52,000 fall from truck
WC | 2024-25 | Verdant Plains Ins | WC 81-402266-1 | 1 | $1,900 | $0 | $1,900 | $1,900 med only
AUTO | 2021-22 | Ironvale Ins Co | BA 3040128 | 1 | $4,200 | $0 | $4,200 | $4,200 PD
AUTO | 2022-25 | Ironvale Ins Co | BA 3040128-1/-3 | 0 | $0 | $0 | $0 | -
GL | 2021-25 | Pinewick National | CGL 7185520 | 1 | $0 | $15,000 | $15,000 | $15,000 irrigation trench fall
Totals | | | | 14 | $96,250 | $41,000 | $137,250 |
Notes: WC carrier change at 2023 renewal. All figures from carrier loss runs; Hartwell & Pryce has not verified reserves. Open claims: 3.
""", edge_rule=14)

# Rule 16: London "Claims Experience"
add("boundary", {"market": "UK", "source": "London market claims experience", "line": "property", "length": "medium"},
    "gA:loss_run:london-ce-binder", "loss_run", """
CLAIMS EXPERIENCE
Assured: Monkswell Hotels Group Ltd     UMR: B1427MWH2025
Class: Property Damage and Business Interruption     Lead: Brackenfield Syndicate 3318
Years of account 2020 - 2025, figures 100% of risk, as at 30/09/2026, GBP
YOA | Date of Loss | Location | Cause | Paid | Outstanding | Total | Status
2020 | 03/12/2020 | Harrowfield Lodge | EoW from tank | £41,700 | £0 | £41,700 | Settled
2021 | Nil | | | | | |
2022 | 19/07/2022 | Crosshaven Hotel | Kitchen fire, BI 6 weeks | £310,500 | £0 | £310,500 | Settled
2023 | Nil | | | | | |
2024 | 22/01/2024 | Monkswell Spa | Storm Isha roof damage | £27,900 | £8,100 | £36,000 | Open
2025 | Nil | | | | | |
""", edge_rule=16)

add("boundary", {"market": "UK", "source": "London market claims experience", "line": "marine", "length": "short"},
    "gA:loss_run:london-ce-short", "loss_run", """
Claims Experience, Cargo, 5 YOA to 2025, Assured Tidewell Commodities Ltd, at 30/09/2026 (USD, 100%): 2021 $14,000 settled; 2022 nil; 2023 $62,500 o/s; 2024 nil; 2025 nil.
""", edge_rule=16)

add("boundary", {"market": "UK", "source": "London market claims experience", "line": "GL", "length": "long"},
    "gA:loss_run:london-ce-casualty", "loss_run", """
CLAIMS EXPERIENCE - CASUALTY
Insured: Rothwell Ferris Event Structures Ltd and subsidiaries
Unique Market Reference: B0991RFE2026     Lines: Public and Products Liability, Employers' Liability
Period: five years of account 2021 - 2025     Prepared 01/10/2026 from insurer bordereaux, as at 30/09/2026
Figures are 100% of the risk in GBP, ground up, including costs

Year of Account | Section | Claims | Paid | Outstanding | Total | Comments
2021 | PL | 2 | £8,400 | £0 | £8,400 | Spectator trip hazards
2021 | EL | 1 | £36,500 | £0 | £36,500 | Rigger fall, settled 2023
2022 | PL | 0 | £0 | £0 | £0 | Nil
2022 | EL | 0 | £0 | £0 | £0 | Nil
2023 | PL | 1 | £5,000 | £70,000 | £75,000 | Grandstand step collapse, 4 claimants
2023 | EL | 1 | £2,250 | £0 | £2,250 | Hand injury
2024 | PL | 0 | £0 | £0 | £0 | Nil
2024 | EL | 1 | £0 | £18,000 | £18,000 | Noise induced hearing loss notification
2025 | PL / EL | 0 | £0 | £0 | £0 | Nil to date
Total | | 6 | £52,150 | £88,000 | £140,150 |
No claims have been declined. The 2023 grandstand matter is the subject of a contribution claim against the venue operator.
""", edge_rule=16)

# Rule 17: SOV / Statement of Values title over claims listing
add("boundary", {"market": "US", "source": "carrier loss run printout", "line": "property", "length": "medium", "title": "Schedule of Values"},
    "gA:loss_run:title-conflict-sov-cover", "loss_run", """
SCHEDULE OF VALUES - Juniper Flats Self Storage LLC (renewal 2027)
Claim No | Date of Loss | Location | Cause | Paid | Reserve | Incurred | Status
GB-P-22-01804 | 05/06/2022 | 1180 Ocotillo Rd | Hail, roll-up doors | $28,600 | $0 | $28,600 | Closed
GB-P-24-00977 | 09/14/2024 | 22 Mesquite Way | Monsoon wind, roof panels | $15,350 | $9,650 | $25,000 | Open
Totals | | | | $43,950 | $9,650 | $53,600 |
Carrier: Granitebridge Mutual. Policy CPP 7801455. Valuation 09/30/2026.
""", edge_rule=17, flags=["title_conflict"])

add("boundary", {"market": "UK", "source": "insurer claims experience statement", "line": "property", "length": "medium", "title": "Statement of Values"},
    "gA:loss_run:title-conflict-statement-of-values", "loss_run", """
STATEMENT OF VALUES
Policyholder: Glenmorie Distillery Co Ltd     Insurer: Thistlewood Insurance plc     As at 30/09/2026
Claim No | Date of Loss | Description | Paid | O/S | Incurred | Status
TCP-22-2071 | 08/05/2022 | Cask warehouse roof collapse under snow load | £96,400 | £0 | £96,400 | Closed
TCP-25-0332 | 21/03/2025 | Still house flood, burn in spate | £12,800 | £22,200 | £35,000 | Open
Total 2 claims, 2021/22 - 2025/26 | | | £109,200 | £22,200 | £131,400 |
""", edge_rule=17, flags=["title_conflict"])

# ---------------- CONTRAST ----------------
by_id = {r["id"]: r for r in rows}


def contrast(parent_num, new_label, text, cell_extra, n):
    pid = CORE[parent_num]
    parent = by_id[pid]
    c = dict(parent["attribute_cell"])
    c.update(cell_extra)
    add("contrast", c, parent["template_group"], new_label, text, parent=pid, pair=f"P-loss_run-{n}")


# P1: parent 3 -> broker_email (table shrinks to one line)
contrast(3, "broker_email", """
From: Corinne Atwater <catwater@tallisgrove-ins.com>
To: submissions@halcourtspecialty.com
Subject: Bellmont Home & Garden Centers Inc. - GL renewal 01/01/2027
Hi team,
Insured: Bellmont Home & Garden Centers Inc.   Pol #: GL 20-448812
Eff 01/01/2022 thru 01/01/2026 (4 terms)   Coverage: General Liability (Occurrence)
Losses as of 09/15/2026: 3 claims, $44,380 total incurred, one slip and fall still open. Full carrier runs attached.
Can you quote by 12/01? Thanks,
Corinne Atwater, Tallis Grove Insurance Agency
""", {"edit": "claim table reduced to one line inside broker email"}, 1)

# P2: parent 7 -> broker_email
contrast(7, "broker_email", """
From: Desmond Ruelas <druelas@hartwellpryce.com>
To: wc.submissions@bluestemindemnity.com
Subject: Ridgeline Senior Living Group - WC renewal, Policy WC 55-0091273
Hello,
Client: Ridgeline Senior Living Group   Carrier: Bluestem Indemnity Co.   Policy: WC 55-0091273
Policy Period: 04/01/2023 - 04/01/2026   Valuation Date: 09/30/2026
Per the CCS Online loss run attached: 3 claims, $46,095 total incurred, 1 open. Please confirm renewal terms by 02/15.
Regards, Desmond Ruelas, Hartwell & Pryce Insurance Services
""", {"edit": "claim table reduced to one line inside broker email"}, 2)

# P3: parent 16 -> broker_email (UK)
contrast(16, "broker_email", """
From: Felicity Marrable <f.marrable@fernhollowbrokers.co.uk>
To: liability.uw@elmsteadassurance.co.uk
Subject: Brockley Hythe Leisure Ltd t/a Riverside Lido - PL renewal 01/05/2027
Dear Underwriter,
Insured: Brockley Hythe Leisure Ltd t/a Riverside Lido   Policy: EA/PL/7716045
Cover: Public & Products Liability   Policy Periods: 01/05/2022 - 30/04/2026
Claims as at 30/09/2026 total £26,680 across 3 claims, one open (child injured on changing room door). ClaimsHub report attached.
Kind regards, Felicity Marrable, Fernhollow Insurance Brokers Ltd
""", {"edit": "claim table reduced to one line inside broker email"}, 3)

# P4: parent 24 -> other (carrier quote referencing losses)
contrast(24, "other", """
SABLEDOWN GENERAL INSURANCE CO.   Commercial Auto QUOTATION
Insured: Arroyo Linen & Uniform Service   Proposed Policy #: CA 66-310442-3
Proposed Term: 03/01/2027 - 03/01/2028   Quote valid until 01/31/2027
Coverage | Limit | Deductible | Premium
Auto Liability CSL | $1,000,000 | - | $38,420
Physical Damage (Comp/Coll) | ACV, 9 units | $1,000 | $12,960
Total Annual Premium | | | $51,380
Rating note: loss experience 03/01/2023 - 03/01/2026 (3 claims, $51,025 incurred, 1 open) reviewed; experience debit 10% applied.
Subject to: MVRs for all drivers, signed application.
""", {"edit": "claims table replaced by premium table and one-line loss reference; now a carrier quote (rule 12)"}, 4)

# P5: parent 12 -> other (risk survey referencing losses)
contrast(12, "other", """
THISTLEWOOD INSURANCE PLC
Risk Survey Report - Commercial Property
Policyholder: Ardgowan Textiles Ltd   Policy No: TW/CP/0058831
Surveyed: 22/09/2026   Surveyor: R. Coulthard, Risk Engineering
Construction: steel frame, brick and profiled sheet clad, built 1968, 4,200 m2. Fire protection: no sprinklers, intruder alarm to EN 50131 grade 3.
Loss history reviewed: 3 claims since 2021 including storm roof damage £80,000 (open); see claims experience held by underwriting.
Recommendations: R1 replace fragile roof sheets over dye house; R2 thermographic survey of distribution boards; R3 remove combustible waste from yard.
Risk grade: Average.
""", {"edit": "claim table replaced by survey content with one-line loss reference"}, 5)

# P6: parent 20 -> other (broker market presentation, rule 11)
contrast(20, "other", """
DELACOURT RISK PARTNERS
Renewal Market Presentation - Section 4 of 7: Loss Experience
Client: Hollis & Crane Event Staffing Inc.   Incumbent: Pinewick National Insurance Co.
Line: Commercial General Liability   Policy: CGL 7092215   Valued: 09/30/2026 (per carrier runs)
Policy Year | Claim # | DOL | Description | Paid | Reserve | Incurred | Open/Closed
2021-22 | 71-00992 | 10/09/2021 | Guest assaulted by attendee, negligent security alleged | $40,000 | $0 | $40,000 | Closed
2024-25 | 71-03307 | 04/28/2025 | Stage barrier collapse, 3 claimants | $12,900 | $85,000 | $97,900 | Open
Our story to markets: barrier vendor contract now requires certified installation and additional insured status.
Section 5: Marketing strategy and target premium. Section 6: Coverage enhancements. Section 7: Service team.
""", {"edit": "retitled as a section of a broker market presentation with narrative around a shortened table (rule 11)"}, 6)

# P7: parent 26 -> acord (ACORD 130 with loss history section)
contrast(26, "acord", """
ACORD 130 (2017/05)   WORKERS COMPENSATION APPLICATION
APPLICANT: Calderon Framing & Drywall Inc.   FEIN on file   PROPOSED EFF DATE: 01/01/2027
STATE: AZ   AGENCY: Tallis Grove Insurance Agency   PRIOR CARRIER: Westmarch Indemnity Company, Policy WCX 4410278
RATING INFORMATION: Class 5645 Carpentry - Residential | Est. Annual Payroll $1,840,000
LOSS HISTORY (ENTER ALL CLAIMS, PAST 4 YEARS)  Valued As Of: 09/30/2026
Year | # Claims | Amount Paid | Reserve | Open/Closed
2022 | 1 | $10,120 | $0 | Closed
2023 | 1 | $2,140 | $0 | Closed
2024 | 1 | $21,010 | $18,000 | Open
2025 | 1 | $1,050 | $0 | Closed
GENERAL INFORMATION: 1. Does applicant own, operate or lease aircraft/watercraft? N   2. Any work performed underground or above 15 feet? Y
""", {"edit": "header changed to ACORD 130 application with rating and general information sections; claims condensed into the form's loss history block"}, 7)

# P8: parent 37 -> other (MGA quotation referencing claims experience)
contrast(37, "other", """
CRESTMOOR UNDERWRITING AGENCY LIMITED
On behalf of participating insurers
QUOTATION  -  Liability (Employers' & Public)
Insured: Pennard Scaffolding Services Ltd    Agreement ref: CUA/LIA/2210/88
Period: 01/01/2027 - 31/12/2027    Currency GBP
Section | Limit | Excess | Premium
EL | £10,000,000 | Nil | £21,450
PL | £5,000,000 | £1,000 | £9,870
Total premium excluding IPT | | | £31,320
Claims experience 2021 - 2025 (3 claims, £100,540 incurred, one open EL claim) has been taken into account.
Subject to: height safety risk improvement within 60 days. Quotation valid 30 days.
""", {"edit": "claims table replaced by premium table and one-line reference; now an MGA quotation (rule 12)"}, 8)

with open(OUT, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows))
