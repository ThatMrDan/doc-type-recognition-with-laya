import json, sys
sys.path.insert(0, sys.argv[1])
from core import CORE
from boundary import BOUNDARY

OUT = sys.argv[2]
CLS = "broker_email"

def row(n, slice_, key, attrs, label, rule=None, parent=None, pair=None, text=""):
    w = len([t for t in text.split() if t != "|"])
    attrs = dict(attrs, length="short" if w <= 40 else "medium" if w <= 120 else "long")
    return {
        "id": f"A-{CLS}-{n:03d}", "slice": slice_, "generator": "claude-opus-5.5",
        "generator_family": "A", "prompt_id": f"a-{CLS}-v1", "attribute_cell": attrs,
        "template_group": f"gA:{CLS}:{key}", "generator_label": label, "edge_rule": rule,
        "expected_flags": [], "parent_id": parent, "pair_id": pair, "text": text,
    }

rows = []
n = 0
for key, attrs, text in CORE:
    n += 1
    rows.append(row(n, "core", key, attrs, CLS, text=text))
for key, rule, label, attrs, text in BOUNDARY:
    n += 1
    rows.append(row(n, "boundary", key, attrs, label, rule=rule, text=text))

def sub(text, pairs):
    for a, b in pairs:
        assert a in text, a
        text = text.replace(a, b)
    return text

# contrast edits: (core index 1-based, new label, edit description, replacements)
C = []
C.append((26, "sov", "attachment mention replaced by pasted SOV", [
 ("Apps, SOV and loss runs attached. Can you take a look?",
  "Apps and loss runs attached, SOV pasted below:\n\n"
  "Loc | Bldg | Address | Occupancy | Construction | Yr Built | Sq Ft | Sprinkler | Bldg Value | Contents/Stock | BI | TIV\n"
  "1 | 1 | 1400 E 4th Ave, Hutchinson KS | Concrete grain elevator | Fire resistive | 1962 | 18,000 | N | 3,100,000 | 1,200,000 | 250,000 | 4,550,000\n"
  "1 | 2 | 1400 E 4th Ave, Hutchinson KS | Office / scale house | Frame | 1978 | 1,600 | N | 240,000 | 35,000 | 0 | 275,000\n"
  "2 | 1 | 88 Elevator Rd, Partridge KS | Steel bin storage | Non-comb | 2008 | 14,500 | N | 2,450,000 | 1,400,000 | 180,000 | 4,030,000\n"
  "2 | 2 | 88 Elevator Rd, Partridge KS | Grain dryer / leg | Non-comb | 2015 | 900 | N | 300,000 | 0 | 45,000 | 345,000\n"
  "TOTAL | | | | | | 35,000 | | 6,090,000 | 2,635,000 | 475,000 | 9,200,000\n\n"), (" Thanks, Grace", "Thanks, Grace")]))
C.append((31, "sov", "mortgagee request replaced by pasted building schedule", [
 ("Subject: Change request - Bristow Hill Orchards - add mortgagee", "Subject: Change request - Bristow Hill Orchards - updated schedule"),
 ("Please add Hartland Valley Farm Credit ACA as mortgagee on the barn at 210 Bristow Hill Rd, Glastonbury CT, loan # 4471-0098. Effective today.",
  "Updated property schedule below, replacement cost, effective today.\n\n"
  "Bldg | Address | Occupancy | Construction | Yr Built | Sq Ft | Prot Class | Bldg Value | Contents | TIV\n"
  "1 | 210 Bristow Hill Rd, Glastonbury CT | Dwelling (farmhouse) | Frame | 1924 | 2,800 | 5 | 620,000 | 150,000 | 770,000\n"
  "2 | 210 Bristow Hill Rd, Glastonbury CT | Barn / equipment storage | Frame | 1951 | 6,400 | 5 | 410,000 | 285,000 | 695,000\n"
  "3 | 210 Bristow Hill Rd, Glastonbury CT | Cold storage / packing | Metal non-comb | 2012 | 9,000 | 5 | 1,150,000 | 340,000 | 1,490,000\n"
  "4 | 214 Bristow Hill Rd, Glastonbury CT | Farm stand / retail | Frame | 1998 | 1,200 | 5 | 180,000 | 40,000 | 220,000\n"
  "Total | | | | | 19,400 | | 2,360,000 | 815,000 | 3,175,000\n")]))
C.append((23, "sov", "single added building replaced by pasted revised schedule", [
 ("Wharfedale - add vehicle store", "Wharfedale - revised schedule"),
 ("Please add the detached vehicle store at the rear of the premises, buildings sum GBP 85,000, from today. Brick and steel clad, alarmed. Let me know the AP.",
  "Please amend to the revised schedule below from today, basis reinstatement. Let me know the AP.\n\n"
  "Item | Building | Address | Use | Construction | Year | Floor area m2 | Sprinklers | Buildings GBP | Contents GBP | Stock GBP | Total GBP\n"
  "1 | Main workshop | Ilkley Rd, Otley LS21 3JP | Joinery manufacture | Steel portal, brick/clad | 1986 | 1,450 | No | 1,250,000 | 410,000 | 95,000 | 1,755,000\n"
  "2 | Office & showroom | Ilkley Rd, Otley LS21 3JP | Office / showroom | Brick, slate roof | 1932 | 320 | No | 480,000 | 60,000 | 15,000 | 555,000\n"
  "3 | Timber store | Ilkley Rd, Otley LS21 3JP | Storage | Steel frame, open sided | 2004 | 600 | No | 140,000 | 0 | 120,000 | 260,000\n"
  "4 | Vehicle store | Ilkley Rd, Otley LS21 3JP (rear) | Vehicle storage | Brick and steel clad | 2019 | 180 | No | 85,000 | 10,000 | 0 | 95,000\n"
  "Total | | | | | | 2,550 | | 1,955,000 | 480,000 | 230,000 | 2,665,000")]))
C.append((40, "sov", "chaser replaced by pasted location schedule", [
 ("Subject: Re: Alpine Ridge Lodge quote?", "Subject: Re: Alpine Ridge Lodge values"),
 ("Following up again. Lodge owner signs with someone else Monday if I don't have a number. Please advise.",
  "Values you asked for below.\n\n"
  "Loc | Bldg | Address | Occupancy | Constr | Yr | Stories | Sq Ft | Sprinkler | Building | Contents | BI | TIV\n"
  "1 | 1 | 7700 Hwy 9, Breckenridge CO | Lodge, 38 rooms | Heavy timber | 1979 | 3 | 31,000 | Y | 8,400,000 | 900,000 | 1,600,000 | 10,900,000\n"
  "1 | 2 | 7700 Hwy 9, Breckenridge CO | Restaurant / bar | Frame | 1985 | 1 | 4,800 | Y | 1,350,000 | 280,000 | 450,000 | 2,080,000\n"
  "1 | 3 | 7700 Hwy 9, Breckenridge CO | Staff housing | Frame | 1996 | 2 | 6,200 | N | 1,100,000 | 90,000 | 0 | 1,190,000\n"
  "1 | 4 | 7700 Hwy 9, Breckenridge CO | Maintenance garage | Metal | 2008 | 1 | 3,000 | N | 310,000 | 220,000 | 0 | 530,000\n"
  "TOTAL | | | | | | | 45,000 | | 11,160,000 | 1,490,000 | 2,050,000 | 14,700,000")]))
C.append((2, "loss_run", "renewal note replaced by pasted claims experience table", [
 ("Values up 4% on index, no change to locations, same deductible. Pls can you hold the line at expiring. Need terms by 20 Nov.",
  "Claims experience below, valued 30/09/2026.\n\n"
  "Year | Date of loss | Site | Cause | Paid GBP | Reserve GBP | Incurred GBP | Status\n"
  "2021/22 | 08/02/2022 | Corby | Refrigeration plant breakdown, stock spoilage | 142,600 | 0 | 142,600 | Closed\n"
  "2022/23 | - | - | No claims | 0 | 0 | 0 | -\n"
  "2023/24 | 17/08/2023 | Kettering | Storm damage to roof | 23,900 | 0 | 23,900 | Closed\n"
  "2024/25 | 03/12/2024 | Corby | Forklift impact, racking collapse | 61,000 | 14,500 | 75,500 | Open\n"
  "2025/26 | 22/06/2026 | Daventry | Escape of ammonia, partial evacuation | 9,750 | 30,250 | 40,000 | Open\n"
  "Total | | | | 237,250 | 44,750 | 282,000 |\n\n"
  "Need terms by 20 Nov.")]))
C.append((15, "loss_run", "subjectivity reply replaced by pasted carrier loss run", [
 ("Subject: RE: Arkwright - quote conditions", "Subject: RE: Arkwright - loss history"),
 ("Clare, signed no-flood-loss warranty and the sprinkler inspection report for Plant 2 are enclosed. Still waiting on the boiler cert, should have it Monday.",
  "Clare, carrier loss run pasted below as you asked. Still waiting on the boiler cert, should have it Monday.\n\n"
  "PROPERTY & GL LOSS RUN - Arkwright Precision Castings, Inc. - Valued as of 10/31/2026\n"
  "Policy Term | Line | Claim # | DOL | Description | Paid | Reserve | Incurred | Status\n"
  "12/1/21-22 | ALL | - | - | No losses | 0 | 0 | 0 | -\n"
  "12/1/22-23 | GL | 22-GL-3108 | 05/16/2023 | Damage to customer property during delivery | 7,400 | 0 | 7,400 | Closed\n"
  "12/1/23-24 | PROP | 23-PR-1194 | 03/02/2024 | Induction furnace breakdown | 62,000 | 0 | 62,000 | Closed\n"
  "12/1/24-25 | ALL | - | - | No losses | 0 | 0 | 0 | -\n"
  "12/1/25-26 | GL | 25-GL-4410 | 07/21/2026 | Product defect allegation | 0 | 18,000 | 18,000 | Open\n"
  "Totals | | | | | 69,400 | 18,000 | 87,400 |")]))
C.append((44, "loss_run", "renewal email rewritten as no-known-loss letter signed by the insured", [
 ("From: Celia Okoro <cokoro@westvaleins.com>\nSent: Monday, August 17, 2026 2:22 PM\nTo: Underwriting <uw@glenarmspecialty.com>\nSubject: Renewal - Sable Creek Veterinary Clinic - BOP - 10/1/2026\n\nHi,",
  "To: Westvale Insurance Services, Sacramento, CA\nRe: Sable Creek Veterinary Clinic - BOP - 10/1/2026\n\nTo whom it may concern,"),
 ("The owner tells us they have had no losses in the past five years, and she has agreed to sign a no-known-loss statement for the file.\n\nRenewal premium last year was $6,870. Please send renewal terms by 9/10.\n\nThank you,\nCelia Okoro\nWestvale Insurance Services | Sacramento, CA",
  "I confirm that the clinic has had no losses in the past five years, and I am not aware of any incident or circumstance that may give rise to a claim.\n\nSigned: Helena Marwick, DVM, Owner\nSable Creek Veterinary Clinic\nDate: August 24, 2026")]))
C.append((13, "loss_run", "chaser replaced by pasted loss history", [
 ("Teresa - where are we on Brightwater? Client asked again yesterday. 1/1 is close.",
  "Teresa - Brightwater loss runs from the expiring carrier, pasted since the PDF is a scan. 1/1 is close.\n\n"
  "LOSS HISTORY - Brightwater Marina & Boatyard LLC - valued 09/30/2026\n"
  "Pol Yr | Cov | Claim No | DOL | Desc | Paid | O/S Reserve | Incurred | Open/Closed\n"
  "01/01/21-22 | ALL | - | - | No claims | 0 | 0 | 0 | -\n"
  "01/01/22-23 | ALL | - | - | No claims | 0 | 0 | 0 | -\n"
  "01/01/23-24 | Prop | BW-23-0071 | 09/23/2023 | Wind, dock and roof damage | 38,200 | 0 | 38,200 | C\n"
  "01/01/24-25 | ALL | - | - | No claims | 0 | 0 | 0 | -\n"
  "01/01/25-26 | GL | BW-25-0112 | 05/30/2025 | Customer fall on dock | 12,500 | 0 | 12,500 | C\n"
  "01/01/26-27 | ALL | - | - | No claims to date | 0 | 0 | 0 | -\n"
  "Total | | | | | 50,700 | 0 | 50,700 |")]))

for i, (idx, label, desc, pairs) in enumerate(C, 1):
    parent = rows[idx - 1]
    assert parent["slice"] == "core"
    n += 1
    attrs = dict(parent["attribute_cell"])
    attrs["contrast_edit"] = desc
    rows.append(row(n, "contrast", parent["template_group"].split(":", 2)[2], attrs, label,
                    parent=parent["id"], pair=f"P-{CLS}-{i}", text=sub(parent["text"], pairs)))

with open(OUT, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows))
