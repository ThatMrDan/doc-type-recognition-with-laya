# Boundary rows: (group_key, label, rule, flags, attrs, text)
BOUNDARY = [
# rule 5: combined packs
("pack-125-2016-03-126-2016-09-lr", "acord", 5, ["multi_type"], {"market": "US", "state": "OH", "fill": "filled", "noise": "clean", "pack": "125+126+loss_run"},
"""ACORD 125 (2016/03)  COMMERCIAL INSURANCE APPLICATION   DATE 01/12/2026
AGENCY: Buckeye Ledger Insurance Group, Columbus OH   CARRIER: Cobalt Ridge Indemnity
APPLICANT: Scioto Valley Precast LLC, 2900 Alum Creek Dr, Columbus OH 43207   FEIN 31-1774020   [X] LLC   EFF 03/01/2026
LINES OF BUSINESS: [X] CGL  [X] PROPERTY  [X] AUTO
ACORD 125 (2016/03)  Page 1 of 4
--- page 5 ---
ACORD 126 (2016/09)  COMMERCIAL GENERAL LIABILITY SECTION
APPLICANT: Scioto Valley Precast LLC   EACH OCCURRENCE $1,000,000   GENERAL AGGREGATE $2,000,000
SCHEDULE OF HAZARDS: LOC 1 HAZ 1  Concrete products mfg  CLASS 51221  BASIS (S)  $6,700,000
--- page 9 ---
COBALT RIDGE INDEMNITY  LOSS RUN  VALUED 12/31/2025   INSURED: SCIOTO VALLEY PRECAST LLC   POLICY CRG-GL-4410883
CLAIM # | DOL | DESCRIPTION | PAID | RESERVE | INCURRED | STATUS
GL-24-0091 | 05/14/2024 | Delivery truck struck customer gate | $6,200 | $0 | $6,200 | Closed"""),
("pack-125-2014-12-126-2014-04-lr", "acord", 5, ["multi_type"], {"market": "US", "state": "PA", "fill": "filled", "noise": "caps", "pack": "125+126+loss_run"},
"""COMMERCIAL INSURANCE APPLICATION   APPLICANT: ALLEGHENY RIVET & FASTENER CO, PITTSBURGH PA   AGENCY: THREE RIVERS UNDERWRITING   STATUS: QUOTE   EFF 05/01/2026   ACORD 125 (2014/12) PAGE 1 OF 4
COMMERCIAL GENERAL LIABILITY SECTION   EACH OCC $1,000,000   GEN AGG $2,000,000   HAZARD: BOLT, NUT, RIVET MFG  CLASS 51896  BASIS (S) $14,300,000   ACORD 126 (2014/04) PAGE 1 OF 4
PRAIRIE LANTERN CASUALTY   CLAIMS LISTING AS OF 03/31/2026
POLICY YEAR 2023-24: CLAIM PL0044172  DOL 11/02/2023  PRODUCT LIABILITY, FAILED RIVET  PAID $41,000  RESERVE $22,500  INCURRED $63,500  OPEN
POLICY YEAR 2024-25: NO CLAIMS
POLICY YEAR 2025-26: NO CLAIMS"""),
("pack-125-2022-10-126-2016-09-lr", "acord", 5, ["multi_type"], {"market": "US", "state": "WA", "fill": "partial", "noise": "ocr", "pack": "125+126+loss_run"},
"""ACORD 125 (2022/10)  C0MMERCIAL lNSURANCE APPLlCATI0N
APPLlCANT  Puget Ferry Galley Services lnc   AGENCY  Sound Harbor Brokerage   EFF O6/O1/2026
LlNES  [X] GL  [ ] PR0PERTY
Page 1 of 4
ACORD 126 (2O16/O9)  C0MMERCIAL GENERAL LlABILITY SECTI0N   EACH 0CC $1,OOO,OOO   AGG $2,OOO,OOO
L0SS RUN  Silver Fen Assurance  valuation date O4/3O/2026
Claim  DOL  Desc  Paid  Reserve  lncurred  Status
SF-23-11O4  O8/19/2O23  Slip and fall, galley  $12,3OO  $O  $12,3OO  Closed
SF-25-O227  O2/O3/2O25  Customer illness claim  $1,8OO  $4,2OO  $6,OOO  Open"""),
("pack-125-2016-03-126-2014-04-lr-uk", "acord", 5, ["multi_type"], {"market": "UK", "state": "NY", "fill": "filled", "noise": "clean", "pack": "125+126+loss_run", "note": "US risk placed via London coverholder, UK dates in loss run"},
"""ACORD 125 (2016/03)  COMMERCIAL INSURANCE APPLICATION
Applicant: Finger Lakes Cider House LLC, Geneva NY 14456   Agency: Seneca Shore Insurance   Proposed eff 07/01/2026   Lines: CGL, Liquor, Property   Entity: LLC
Nature of business: cidery with tasting room, 14 FT employees
ACORD 125 (2016/03)  Page 1 of 4

ACORD 126 (2014/04)  COMMERCIAL GENERAL LIABILITY SECTION
Each occurrence $1,000,000   General aggregate $2,000,000   Hazard 1: wineries/cideries, class 16911, basis (S) $2,480,000

Claims experience supplied by coverholder, figures in USD, as at 30/04/2026
Year of account | Claims | Paid | Outstanding | Incurred
2023 | 0 | 0 | 0 | 0
2024 | 1 | 3,400 | 0 | 3,400
2025 | 0 | 0 | 0 | 0"""),
# rule 6: ACORD 139
("139-2004-03", "sov", 6, [], {"market": "US", "state": "TX", "fill": "filled", "noise": "clean"},
"""ACORD 139 (2004/03) STATEMENT OF VALUES
Named insured: Lone Oak Self Storage LP   Agency: Corrigan Pike Insurance Agency   Valuation: Replacement cost   Date 02/02/2026
Loc # | Bldg # | Address | Construction | Occupancy | Yr built | Sq ft | Sprk | Building | BPP | BI/EE | Total
1 | 1 | 9100 FM 1960 Rd W, Houston TX | Masonry non-combustible | Self storage | 2004 | 48,000 | N | $3,900,000 | $25,000 | $310,000 | $4,235,000
2 | 1 | 2211 N Frazier St, Conroe TX | Non-combustible | Self storage | 2011 | 36,500 | N | $2,950,000 | $15,000 | $240,000 | $3,205,000
Total insured values: $7,440,000"""),
("139-2004-03", "sov", 6, [], {"market": "US", "state": "IL", "fill": "partial", "noise": "caps"},
"""ACORD 139 STATEMENT OF VALUES   INSURED: MIDWAY BAKERY DISTRIBUTORS INC
LOC | ADDRESS | CONSTR | YR | BLDG VALUE | CONTENTS | TIV
1 | 4500 S PULASKI RD, CHICAGO IL | JM | 1958 | $2,100,000 | $760,000 | $2,860,000"""),
("139-2015-12", "sov", 6, [], {"market": "US", "state": "FL", "fill": "filled", "noise": "ocr"},
"""STATEMENT 0F VALUES        ACORD 139 (2015/12)
NAMED lNSURED  Coquina Key Condominium Assn lnc      AGENCY  Gulfbreeze Commercial lnsurance Group      VALUATI0N BASlS  RC
L0C | BLDG | ADDRESS | C0NST | 0CC | YR BLT | ST0RIES | SQ FT | PR0T CL | BUILDlNG | C0NTENTS | 0THER | T0TAL
1 | 1 | 6OO Gulf Blvd, lndian Rocks Beach FL | Fire resistive | Condo | 1981 | 6 | 61,OOO | 3 | $14,2OO,OOO | $15O,OOO | $0 | $14,35O,OOO
1 | 2 | 6OO Gulf Blvd (garage) | Non-comb | Parking | 1981 | 1 | 2O,OOO | 3 | $1,1OO,OOO | $O | $O | $1,1OO,OOO
T0TAL $15,45O,OOO"""),
("139-2015-12", "sov", 6, [], {"market": "US", "state": "MN", "fill": "filled", "noise": "clean"},
"""ACORD 139 (2015/12)  Statement of Values  page 1 of 2
Insured: Northfork Cold Storage Inc   Policy period 01/01/2027 to 01/01/2028   Basis: replacement cost, 90% coinsurance
Loc | Bldg | Street | City/State | Description | Construction | Yr | Area | Sprinklered | Bldg | Contents | BI | Total
1 | 1 | 3800 County Rd 8 | St Cloud MN | Freezer warehouse | Insulated metal panel | 2009 | 92,000 | Y | $11,500,000 | $6,800,000 | $2,000,000 | $20,300,000
1 | 2 | 3800 County Rd 8 | St Cloud MN | Office | Frame | 2009 | 4,000 | Y | $640,000 | $90,000 | $0 | $730,000
2 | 1 | 120 Industrial Dr | Sauk Rapids MN | Dry storage | Tilt-up concrete | 2016 | 40,000 | Y | $4,100,000 | $1,200,000 | $500,000 | $5,800,000
Totals | | | | | | | | | $16,240,000 | $8,090,000 | $2,500,000 | $26,830,000"""),
# rule 7: ACORD 140 with location and value blocks
("140-2014-12-multi", "acord", 7, [], {"market": "US", "state": "OH", "fill": "filled", "noise": "clean", "blocks": 3},
"""ACORD 140 (2014/12)  PROPERTY SECTION   DATE 01/12/2026   APPLICANT: Scioto Valley Precast LLC   CARRIER: Cobalt Ridge Indemnity
PREMISES # 1  BLDG # 1  2900 Alum Creek Dr, Columbus OH 43207
  SUBJECT: Building  AMOUNT $3,400,000  COINS 90%  VAL RC  CAUSE: Special  DED $10,000
  SUBJECT: BPP  AMOUNT $1,250,000  COINS 80%  VAL RC  CAUSE: Special  DED $10,000
  SUBJECT: Business income  AMOUNT $900,000  COINS 50%
  CONSTRUCTION: Non-combustible  YR BUILT 1994  STORIES 1  AREA 54,000  PROT CL 2  SPRINKLERED 100%
PREMISES # 2  BLDG # 1  415 Frank Rd, Columbus OH 43223
  SUBJECT: Building  AMOUNT $1,100,000  COINS 90%  VAL RC  CAUSE: Special  DED $10,000
  SUBJECT: BPP  AMOUNT $380,000  COINS 80%  VAL RC
  CONSTRUCTION: Joisted masonry  YR BUILT 1967  STORIES 1  AREA 18,500  PROT CL 3  SPRINKLERED N
BLANKET SUMMARY: Blanket # 1  Building and BPP all premises  $6,130,000
ACORD 140 (2014/12)  Page 1 of 3"""),
("140-2016-03-multi", "acord", 7, [], {"market": "US", "state": "GA", "fill": "filled", "noise": "caps", "blocks": 2},
"""ACORD 140 (2016/03) PROPERTY SECTION   APPLICANT: CHATTAHOOCHEE FIXTURE INSTALLERS INC   EFF 02/15/2026
PREMISES 1 BLDG 1: 1750 OAKBROOK DR, NORCROSS GA 30093   BUILDING $2,250,000 RC 90% SPECIAL   BPP $640,000 RC 80% SPECIAL   CONSTR: MASONRY NC   YR 2001   AREA 31,000   PC 3   SPRK Y
PREMISES 2 BLDG 1: 88 ENTERPRISE CT, LAWRENCEVILLE GA 30046   BUILDING $1,180,000 RC 90% SPECIAL   BPP $210,000 RC 80% SPECIAL   CONSTR: TILT-UP   YR 2013   AREA 16,000   PC 4   SPRK N
TOTAL BUILDING $3,430,000   TOTAL BPP $850,000   PAGE 1 OF 3"""),
("140-2014-12-multi-ocr", "acord", 7, [], {"market": "US", "state": "LA", "fill": "filled", "noise": "ocr", "blocks": 2},
"""PR0PERTY SECTI0N        ACORD 140 (2014/12)
APPLlCANT  Atchafalaya Marine Electric lnc      EFFECTIVE DATE  O4/O1/2026
PREMlSES # 1  BLDG # 1   2O8 Rue Jolie, Broussard LA
SUBJECT 0F lNSURANCE  Building  AM0UNT $1,45O,OOO  C0INS 8O%  VALUATI0N RC  CAUSE 0F L0SS Special  DED $5,OOO  WlND DED 5%
SUBJECT 0F lNSURANCE  BPP  AM0UNT $9OO,OOO  C0INS 8O%  VALUATl0N RC
C0NSTRUCTI0N  Metal bldg  YR BUlLT 2OO7  AREA 12,OOO  PR0T CL 4  FL00D Z0NE  X
PREMlSES # 2  BLDG # 1   Port of lberia, Slip 14, New lberia LA
SUBJECT 0F lNSURANCE  BPP (tools and inventory)  AM0UNT $31O,OOO  C0INS 8O%  VALUATl0N ACV
Page 1 of 3"""),
("140-2016-03-multi-short", "acord", 7, [], {"market": "US", "state": "CO", "fill": "partial", "noise": "clean", "blocks": 2},
"""ACORD 140 (2016/03) Property Section. Applicant: Ruiz Lumber & Truss Inc. Prem 1: 900 6th St, Greeley CO, building $2,800,000, stock $1,600,000. Prem 2: 14 Kodak Rd, Windsor CO, building $950,000, stock $400,000. Special form, RC."""),
# rule 8: certificates
("cert-25-2016-03", "other", 8, [], {"market": "US", "state": "TX", "form": "25", "noise": "clean"},
"""ACORD 25 (2016/03)   CERTIFICATE OF LIABILITY INSURANCE   DATE 05/02/2026
THIS CERTIFICATE IS ISSUED AS A MATTER OF INFORMATION ONLY AND CONFERS NO RIGHTS UPON THE CERTIFICATE HOLDER.
PRODUCER: Corrigan Pike Insurance Agency, Houston TX   INSURED: Delgado Brothers Concrete LLC, 1802 Aldine Bender Rd, Houston TX 77032
INSURER A: Granite Shoals Mutual Ins Co  NAIC 30417
COVERAGES: A  COMMERCIAL GENERAL LIABILITY  OCCUR  POLICY GSM-CPP-2210448  05/01/2026 - 05/01/2027  EACH OCCURRENCE $1,000,000  GENERAL AGGREGATE $2,000,000
A  AUTOMOBILE LIABILITY  ANY AUTO  GSM-BA-2210449  COMBINED SINGLE LIMIT $1,000,000
DESCRIPTION OF OPERATIONS: Certificate holder is additional insured on GL where required by written contract.
CERTIFICATE HOLDER: Gulf Coast Paving Partners, 500 Post Oak Blvd, Houston TX 77027
AUTHORIZED REPRESENTATIVE: M. Ortega"""),
("cert-24-2016-03", "other", 8, [], {"market": "US", "state": "OR", "form": "24", "noise": "clean"},
"""ACORD 24 (2016/03) CERTIFICATE OF PROPERTY INSURANCE. Issued as a matter of information only; it does not amend, extend or alter the coverage afforded by the policies below. Insured: Cascade Foothill Veterinary Clinic PC. Location: 2275 Lancaster Dr NE, Salem OR. Building $1,850,000, special form. Holder: Mid-Valley Community Bank, mortgagee."""),
("cert-27-2016-03", "other", 8, [], {"market": "US", "state": "VA", "form": "27", "noise": "caps"},
"""EVIDENCE OF PROPERTY INSURANCE   ACORD 27 (2016/03)   DATE 06/01/2026
THIS IS EVIDENCE THAT INSURANCE AS IDENTIFIED BELOW HAS BEEN ISSUED, IS IN FORCE, AND CONVEYS ALL THE RIGHTS AND PRIVILEGES AFFORDED UNDER THE POLICY.
AGENCY: TIDEWATER BEACON INSURANCE AGENCY   COMPANY: SILVER FEN ASSURANCE CO   POLICY # SFA-CP-7700213   EFF 06/01/2026  EXP 06/01/2027
INSURED: ELIZABETH RIVER MARINE SUPPLY INC   PROPERTY: 1300 GRANBY ST, NORFOLK VA 23510
COVERAGE: BUILDING $2,600,000  SPECIAL FORM  DED $5,000
ADDITIONAL INTEREST: [X] MORTGAGEE  [ ] LENDER'S LOSS PAYABLE   NAME: HAMPTON ROADS SAVINGS BANK"""),
("cert-28-2016-03", "other", 8, [], {"market": "US", "state": "IL", "form": "28", "noise": "ocr"},
"""EVlDENCE 0F C0MMERCIAL PR0PERTY lNSURANCE   ACORD 28 (2O16/O3)
This evidence of property insurance is issued as a matter of inf0rmation only and confers no rights up0n the additional interest named bel0w.
lNSURED  Kowalczyk Tool & Die Co   C0MPANY  Cobalt Ridge lndemnity   P0LICY  CRl-CP-551O22   O6/O1/2026 to O6/O1/2027
L0CATI0N  1880 W Diehl Rd, Naperville lL   BUlLDING $5,2OO,OOO  BPP $3,1OO,OOO  Bl $1,OOO,OOO
ADDITI0NAL lNTEREST  DuPage Equipment Finance LLC, loss payee"""),
("cert-25-2014-01", "other", 8, [], {"market": "US", "state": "NV", "form": "25", "noise": "clean"},
"""ACORD 25 (2014/01) CERTIFICATE OF LIABILITY INSURANCE. This certificate is issued as a matter of information only. Insured: Silver State Hospitality Group LLC. Umbrella liab, occurrence, each occurrence $10,000,000. Holder: Paradise Rd Events LLC."""),
]

# Contrast rows: (parent_index (1-based core row), new_label, attrs, text)
CONTRAST = [
(2, "other", {"edit": "acord_marks_removed_carrier_supplemental"},
"""GRANITE SHOALS MUTUAL  BREWERY AND CRAFT SPIRITS SUPPLEMENTAL QUESTIONNAIRE
DATE: 08/02/2026  AGENCY: Bluestem Risk Partners, Dayton OH
APPLICANT: Sable Creek Brewing Co   EFF DATE: 09/15/2026
Tasting room on premises? [X] Y [ ] N   Self-distribution? [ ] Y [X] N"""),
(10, "other", {"edit": "acord_126_to_mga_gl_supplemental"},
"""TRI-STAR UNDERWRITING MANAGERS  GENERAL LIABILITY SUPPLEMENTAL APPLICATION - COLD STORAGE   APPLICANT: NORTHFORK COLD STORAGE INC, ST CLOUD MN   AMMONIA REFRIGERATION? Y/N   THIRD-PARTY GOODS STORED? Y/N   HAZARDS: SEE ATTACHED"""),
(22, "other", {"edit": "acord_130_to_carrier_indication"},
"""COBALT RIDGE INDEMNITY WORKERS COMPENSATION INDICATION. Applicant: Wabash Bend Millwork LLC, Terre Haute IN. State: IN. Class 2802, payroll $640,000, rate 3.92, est premium $25,088. Eff 10/01/2026. Subject to loss runs."""),
(31, "sov", {"edit": "acord_140_to_acord_139_schedule"},
"""ACORD 139 (2015/12) STATEMENT OF VALUES. Insured: Quinnipiac Bindery LLC. Loc | Address | Constr | Bldg | BPP | TIV ; 1 | 60 Hamilton St, New Haven CT | Masonry | $0 (tenant) | $275,000 | $275,000. Valuation RC."""),
(6, "broker_email", {"edit": "acord_125_fields_to_cover_email"},
"""From: Front Range Mutual Agency <submissions@frontrangemutual.example>
Subject: New submission - Ruiz Lumber & Truss Inc, Greeley CO
Hi, ACORD 125 attached for Ruiz Lumber & Truss Inc, Greeley CO. Eff 04/01/2026. Lines: CGL, Property, Auto. Prior carrier: none. Thanks"""),
(25, "other", {"edit": "acord_131_to_acord_25_certificate"},
"""ACORD 25 (2016/03) Certificate of Liability Insurance, issued as a matter of information only. Insured: Lowcountry Roofing Co, Charleston SC. Umbrella liab, occurrence, $5,000,000 each occurrence, retention $10,000. Holder: Harbor View HOA."""),
(15, "loss_run", {"edit": "acord_127_driver_line_to_auto_loss_run"},
"""BUSlNESS AUT0 L0SS RUN valued O6/3O/2026  lNSURED  Bluegrass Mobile Notary Svcs  CLAlM BA-25-O118  D0L O1/O9/2O25  DRIVER  Colleen Barrow  rear-end, L0UISVILLE KY  PAlD $4,1OO  RESERVE $O  lNCURRED $4,1OO  CL0SED"""),
(35, "other", {"edit": "acord_160_to_carrier_bop_quote"},
"""GRANITE SHOALS MUTUAL   BUSINESS OWNERS QUOTE   APPLICANT: TURQUOISE MESA COFFEE ROASTERS LLC, SANTA FE NM   BPP $180,000   LIABILITY $1M/$2M   ANNUAL PREMIUM $2,140   QUOTE VALID 30 DAYS"""),
]
