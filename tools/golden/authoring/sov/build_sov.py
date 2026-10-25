"""Build tools/golden/rows/a_sov.jsonl (generator family A, class sov)."""
import json, re, sys

OUT = sys.argv[1]

# ---------- formatting helpers ----------
def us(v): return f"{v:,}"
def usd(v): return f"${v:,}"
def gbp(v): return f"£{v:,}"
def eur(v): return f"€{v:,}"
def eu(v): return f"{v:,}".replace(",", ".")
def plain(v): return str(v)
def k(v): return f"{v // 1000:,}"

def table(cols, data, fmt, total_label="Total", total_col=True, sep=" ; ", cols2=None):
    """data: list of (cells, vals). Appends a row sum if total_col and a totals row if total_label."""
    lines = []
    if cols2:
        lines.append(" | ".join(cols2))
    lines.append(" | ".join(cols))
    sums = None
    for cells, vals in data:
        out = list(cells) + [fmt(v) for v in vals]
        if total_col:
            out.append(fmt(sum(vals)))
        lines.append(" | ".join(out))
        row = list(vals) + ([sum(vals)] if total_col else [])
        sums = row if sums is None else [a + b for a, b in zip(sums, row)]
    if total_label:
        ncells = len(data[0][0])
        lines.append(" | ".join([total_label] + [""] * (ncells - 1) + [fmt(s) for s in sums]))
    return sep.join(lines), sums

ROWS = []
def add(slice_, cell, group, label, text, edge_rule=None, flags=None, parent=None, pair=None):
    ROWS.append(dict(slice=slice_, attribute_cell=cell, template_group=group, generator_label=label,
                     edge_rule=edge_rule, expected_flags=flags or [], parent_id=parent, pair_id=pair,
                     text=text.strip()))
    return len(ROWS)  # 1-based index -> id

def C(market, fmt, size, columns, valuation, occupancy, construction, currency, **extra):
    d = dict(market=market, format=fmt, size=size, columns=columns, valuation=valuation,
             occupancy=occupancy, construction=construction, currency=currency)
    d.update(extra)
    return d

TEXT = {}  # id index -> text, for contrast editing

# =====================================================================
# CORE ROWS
# =====================================================================

# --- 1 Corvane Partners, pipe header with full COPE
t, s = table(
    ["Loc #", "Bldg #", "Address", "City", "ST", "Zip", "Occupancy", "ISO Const", "Yr Built", "Sq Ft", "Stories", "Sprinklered", "PC", "Building", "Contents", "BI/EE", "TIV"],
    [(["1", "1", "4410 Industrial Pkwy", "Fresno", "CA", "93725", "Warehouse - dry goods", "3", "1998", "182,000", "1", "Y - ESFR", "3"], [14_200_000, 6_500_000, 1_800_000]),
     (["2", "1", "88 Lockwood Rd", "Reno", "NV", "89502", "Warehouse - cross dock", "4", "2011", "126,500", "1", "Y - ESFR", "2"], [11_900_000, 4_100_000, 1_200_000]),
     (["3", "1", "2105 E Commerce Way", "Boise", "ID", "83716", "Warehouse / light assembly", "3", "1986", "71,250", "1", "Partial", "4"], [5_350_000, 2_275_000, 650_000])],
    usd, total_label="TOTALS", sep="\n")
r1 = add("core", C("US", "sheet", "2-10", "full_cope", "replacement_cost", "warehouse", "iso_number", "USD"),
         "gA:sov:corvane-partners-pipe-cope", "sov",
         "CORVANE PARTNERS LLC - STATEMENT OF VALUES\nInsured: Redwater Distribution Co. | Policy Term: 07/01/2027 - 07/01/2028 | Valuation: Replacement Cost\n" + t)

# --- 2 Corvane, manufacturing, 18 locations, first rows
t, s = table(
    ["Loc #", "Bldg #", "Address", "City", "ST", "Occupancy", "ISO Const", "Yr Built", "Sq Ft", "Stories", "Sprinklered", "PC", "Building", "Contents", "Stock", "BI/EE", "TIV"],
    [(["1", "1", "1200 Furnace St", "Toledo", "OH", "Metal stamping", "4", "1974", "214,000", "1", "Y", "2"], [18_400_000, 9_750_000, 2_100_000, 6_000_000]),
     (["1", "2", "1200 Furnace St", "Toledo", "OH", "Paint line / finishing", "3", "1991", "48,000", "1", "Y", "2"], [4_200_000, 3_900_000, 450_000, 0]),
     (["2", "1", "77 Riverbend Dr", "Muncie", "IN", "Injection moulding", "3", "2003", "96,500", "1", "Y", "3"], [8_100_000, 7_250_000, 1_300_000, 3_400_000])],
    usd, total_label=None, sep="\n")
r2 = add("core", C("US", "sheet", "11-100", "full_cope", "replacement_cost", "manufacturing", "iso_number", "USD", rows_shown="first 3 rows (2 of 18 locations)"),
         "gA:sov:corvane-partners-pipe-cope", "sov",
         "CORVANE PARTNERS LLC | SCHEDULE OF VALUES | Hollins Precision Components Inc. and subsidiaries\n"
         "Valuation basis: RC (Bldg, Contents), Stock at selling price less discounts, BI 12 mos ALS | 18 locations | Total Insured Value $227,450,000 | Prepared 09/14/2027 rev 2\n" + t)

# --- 3 Corvane, single church, values only, ACV, no TIV
r3 = add("core", C("US", "sheet", "1", "values_only", "acv", "church", "none", "USD", no_tiv=True),
         "gA:sov:corvane-partners-pipe-cope", "sov",
         "Corvane Partners LLC - Statement of Values (ACV)\nLoc | Address | Occupancy | Building | Contents | Total Values\n"
         "1 | 300 N Chapel St, Ottumwa IA 52501 | Church & fellowship hall | $2,450,000 | $310,000 | $2,760,000")

# --- 4 Halsted Grey, merged two-row headers, retail, words
t, s = table(
    ["No.", "Street", "City/St", "Occ", "Constr", "Yr", "Sq Ft", "Spr", "Bldg", "BPP", "BI", "TIV"],
    [(["1", "2210 Mesa Blvd", "Tucson AZ", "Retail - furniture", "Masonry non-comb", "1999", "41,000", "Y"], [3_900_000, 2_600_000, 900_000]),
     (["2", "15 Saguaro Plz", "Mesa AZ", "Retail - furniture", "Masonry non-comb", "2006", "38,400", "Y"], [3_650_000, 2_450_000, 850_000]),
     (["3", "8801 N 7th Ave", "Phoenix AZ", "Retail outlet + whse", "Tilt-up concrete", "2014", "62,750", "Y"], [5_800_000, 3_900_000, 1_100_000]),
     (["4", "460 Copper Ln", "Flagstaff AZ", "Retail - furniture", "Joisted masonry", "1983", "22,000", "N"], [1_750_000, 1_200_000, 400_000])],
    us, total_label="TOT", sep=" ; ",
    cols2=["LOCATION", "", "", "BUILDING INFO", "", "", "", "", "VALUES ($)", "", "", ""])
r4 = add("core", C("US", "sheet", "2-10", "messy_merged", "replacement_cost", "retail", "words", "USD"),
         "gA:sov:halsted-grey-merged-2row", "sov",
         "HALSTED GREY INSURANCE SERVICES ; Desert Hearth Home Furnishings LLC - SOV eff 3/1/28 - RC ; " + t)

# --- 5 Halsted Grey, offices, free text construction, 11-100, no TIV
t, s = table(
    ["#", "Address", "City/St", "Occupancy", "Construction (as reported)", "Yr Blt / Updates", "Sq Ft", "Fl", "Spklr", "Bldg", "Contents", "EDP", "Bus Inc", "Total Insured Value"],
    [(["1", "100 Commerce Sq", "Hartford CT", "Office - multi-tenant", "steel frame, curtain wall", "1987 / roof 2019", "212,000", "14", "Full"], [48_500_000, 2_200_000, 900_000, 3_500_000]),
     (["2", "41 Asylum Ave", "Hartford CT", "Office", "brick bearing wall, wood floors", "1921 / elec 2010", "36,500", "5", "Full"], [9_800_000, 450_000, 150_000, 700_000]),
     (["3", "2290 Post Rd", "Warwick RI", "Office - medical tenants", "JM/frame w mansard", "1968 / HVAC 2016", "18,200", "2", "Partial"], [2_750_000, 150_000, 0, 300_000])],

    usd, total_label=None, sep="\n",
    cols2=["LOCATION DETAIL", "", "", "COPE", "", "", "", "", "", "VALUES - REPLACEMENT COST", "", "", "", ""])
r5 = add("core", C("US", "sheet", "11-100", "messy_merged", "replacement_cost", "office", "free_text", "USD", no_tiv=True, rows_shown="first 3 of 23"),
         "gA:sov:halsted-grey-merged-2row", "sov",
         "HALSTED GREY INSURANCE SERVICES\nNamed Insured: Tidewater Commons REIT LP et al | 23 locs | Renewal 01/01/2028\n"
         "NOTE: construction per property managers, not verified.\n" + t +
         "\n(continued on tab 'Locs 4-23')")

# --- 6 Halsted Grey, schools ACV
r6_text = ("HALSTED GREY | ISU - Prairie Lakes Community School District | SOV - ACV per member schedule ; "
           "LOCATION | | | BUILDING | | | VALUES | | ; "
           "No. | Campus / Address | Occ | Constr | Yr | Sq Ft | Bldg | Contents | TIV ; "
           "1 | Elm Creek Elem, 18 Pond Rd Ames IA | School K-5 | Masonry | 1959 | 43,000 | 5,600,000 | 650,000 | 6,250,000 ; "
           "2 | Prairie Lakes MS, 600 Main St Nevada IA | School 6-8 | Masonry/steel | 1972 | 71,500 | 9,100,000 | 1,050,000 | 10,150,000 ; "
           "3 | PLHS + gym, 610 Main St Nevada IA | School 9-12 | Masonry/steel | 1998 | 128,000 | 17,400,000 | 2,300,000 | 19,700,000 ; "
           "4 | Bus barn, 12 County Rd E | Garage | Metal | 2004 | 9,800 | 640,000 | 410,000 | 1,050,000 ; "
           "TOT | | | | | | 32,740,000 | 4,410,000 | 37,150,000")
r6 = add("core", C("US", "sheet", "2-10", "messy_merged", "acv", "school", "words", "USD"),
         "gA:sov:halsted-grey-merged-2row", "sov", r6_text)

# --- 7 Pinebrook values only, mixed-use, short, no TIV
r7_text = ("Pinebrook Risk Advisors - Values Schedule - Lanternfield Holdings LLC\n"
           "Loc | Address | Occupancy | Building | Contents | Rents | Total\n"
           "1 | 212 Main St, Bozeman MT | Mixed-use: retail ground, 6 apts above | 2,850,000 | 120,000 | 210,000 | 3,180,000\n"
           "2 | 18 Willson Ave, Bozeman MT | Mixed-use: cafe + offices | 1,640,000 | 95,000 | 130,000 | 1,865,000\n"
           "Total | | | 4,490,000 | 215,000 | 340,000 | 5,045,000")
r7 = add("core", C("US", "sheet", "2-10", "values_only", "replacement_cost", "mixed_use", "none", "USD", no_tiv=True),
         "gA:sov:pinebrook-values-only", "sov", r7_text)

# --- 8 Pinebrook retail ACV, 11-100 values only
t, s = table(["Store", "Address", "City", "ST", "Bldg (ACV)", "Contents (ACV)", "Stock", "TIV"],
             [(["101", "1450 Hwy 30 W", "Twin Falls", "ID"], [0, 380_000, 1_150_000]),
              (["102", "220 N Main", "Pocatello", "ID"], [1_200_000, 340_000, 980_000])],

             us, total_label=None)
r8 = add("core", C("US", "sheet", "11-100", "values_only", "acv", "retail", "none", "USD", rows_shown="first 2 of 34"),
         "gA:sov:pinebrook-values-only", "sov",
         "PINEBROOK ; Gem State Farm Supply - ACV ; " + t)

# --- 9 Ferrisford Mutual carrier SOV form, healthcare, long
r9 = add("core", C("US", "pdf_form", "2-10", "full_cope", "replacement_cost", "healthcare", "words", "USD", carrier_branded=True),
         "gA:sov:ferrisford-mutual-fm-sv-14-0322", "sov", """
FERRISFORD MUTUAL INSURANCE COMPANY
PROPERTY STATEMENT OF VALUES                                         FM-SV-14 (03/22)    Page 1 of 3
Named Insured: St. Brannock Health Partners, Inc.          Agency: Cobbleway Agency Group   Agency Code: 44-1902
Policy Period: 04/15/2028 to 04/15/2029                    Valuation:  [X] Replacement Cost  [ ] Actual Cash Value  [ ] Agreed Value
Coinsurance: 90%   Margin clause: [X] 110%
Loc  Bldg  Street Address / City / State / Zip          Occupancy                    Construction        Yr Built  Stories  Area (sq ft)  Sprinklered %  Alarm  Prot Class
1    1     1880 Larchmont Rd, Lexington KY 40503     Acute care hospital         Fire resistive      1979      6        248,000       100            CS     2
1    2     1880 Larchmont Rd, Lexington KY 40503     Parking structure           Fire resistive      2005      4        190,000       0              None   2
2    1     41 Bluegrass Pkwy, Georgetown KY 40324   Outpatient surgery center   Masonry non-comb.   2012      1        26,400        100            CS     3
3    1     705 Elm St, Richmond KY 40475           Medical office building     Joisted masonry     1964      2        19,750        40             Local  4
Loc  Bldg  Building Value     Contents / Equipment   Business Income / Extra Expense   Total Insured Value
1    1     $96,400,000        $38,200,000           $22,000,000                       $156,600,000
1    2     $14,750,000        $150,000              $0                                $14,900,000
2    1     $8,300,000         $6,900,000            $2,400,000                        $17,600,000
3    1     $3,450,000         $1,120,000            $380,000                          $4,950,000
TOTAL      $122,900,000       $46,370,000           $24,780,000                       $194,050,000
Values reported are as of 01/31/2028. I certify the above values are true and complete to the best of my knowledge.
Signature of Applicant ______________________   Title ____________   Date ________
""")

# --- 10 Ferrisford, single hotel
r10 = add("core", C("US", "pdf_form", "1", "full_cope", "replacement_cost", "hotel", "words", "USD", carrier_branded=True),
          "gA:sov:ferrisford-mutual-fm-sv-14-0322", "sov", """
FERRISFORD MUTUAL INSURANCE COMPANY   PROPERTY STATEMENT OF VALUES   FM-SV-14 (03/22)
Named Insured: Gullwing Hospitality LLC dba Harborlight Inn & Suites   Policy Period: 06/01/2028-06/01/2029
Valuation: [X] Replacement Cost
Loc 1 Bldg 1 | 9 Ocean View Dr, Myrtle Beach SC 29577 | Hotel - 142 keys, restaurant, outdoor pool
Construction: Masonry non-combustible | Yr Built 1996 (renov 2021) | Stories 7 | Area 118,000 sq ft | Sprinklered 100% | Prot Class 3 | Dist. to coast 400 ft
Building $31,500,000 | Contents/FF&E $4,250,000 | BI incl. Rents 12 mos $6,800,000 | Total Insured Value $42,550,000
""")

# --- 11 Granite Ridge Specialty SOV form, cold storage, ACV
r11 = add("core", C("US", "pdf_form", "2-10", "full_cope", "acv", "cold_storage", "iso_number", "USD", carrier_branded=True),
          "gA:sov:granite-ridge-specialty-gr-sov-2-0119", "sov", """
GRANITE RIDGE SPECIALTY INSURANCE CO.      STATEMENT OF VALUES      GR-SOV-2 (01/19)
Applicant: Frostmere Cold Chain LLC        Producer: Delacroix Wholesale Brokerage, Atlanta GA
Valuation Basis: ACTUAL CASH VALUE         Stock Valuation: Selling Price
LOC | ADDRESS | OCCUPANCY | ISO CLASS | YR | SQ FT | SPRINK | PPC | BLDG | CONTENTS/STOCK | SPOILAGE | TIV
1 | 300 Peachtree Industrial Blvd, Suwanee GA | Cold storage -10F freezer | 3 | 2001 | 165,000 | Y (dry pipe) | 3 | 11,200,000 | 14,800,000 | 2,500,000 | 28,500,000
2 | 18 Ag Center Rd, Tifton GA | Cold storage / produce cooler | 4 | 2017 | 92,000 | Y | 5 | 9,750,000 | 6,300,000 | 1,000,000 | 17,050,000
3 | 7700 Port Access Rd, Savannah GA | Blast freeze + dry whse | 3 | 1993 | 128,400 | Y | 2 | 7,900,000 | 11,650,000 | 1,750,000 | 21,300,000
TOTALS | | | | | | | | 28,850,000 | 32,750,000 | 5,250,000 | 66,850,000
""")

# --- 12 Granite Ridge, warehouses, 11-100, no TIV
r12 = add("core", C("US", "pdf_form", "11-100", "full_cope", "replacement_cost", "warehouse", "iso_number", "USD", carrier_branded=True, no_tiv=True, rows_shown="first 3 of 27"),
          "gA:sov:granite-ridge-specialty-gr-sov-2-0119", "sov", """
GRANITE RIDGE SPECIALTY INSURANCE CO.      STATEMENT OF VALUES      GR-SOV-2 (01/19)       Page 1 of 4
Applicant: Bellcourt Logistics Partners LP        Producer: Delacroix Wholesale Brokerage
Valuation Basis: REPLACEMENT COST     Number of Locations: 27     Total Insured Values (all pages): $412,960,000
LOC | ADDRESS | OCCUPANCY | ISO CLASS | YR | SQ FT | SPRINK | PPC | BLDG | CONTENTS | BI | TOTAL
1 | 4000 Airport Rd, Charlotte NC | Distribution whse | 4 | 2016 | 512,000 | ESFR | 2 | 38,400,000 | 9,600,000 | 4,000,000 | 52,000,000
2 | 125 Logistics Dr, Greer SC | Distribution whse | 4 | 2019 | 404,800 | ESFR | 3 | 31,100,000 | 7,200,000 | 3,200,000 | 41,500,000
3 | 9 Rail Spur Ln, Spartanburg SC | Whse - tires (high piled) | 3 | 2008 | 286,000 | ESFR | 3 | 17,900,000 | 22,400,000 | 2,100,000 | 42,400,000
""")

# --- 13 Thistledown Brokers UK offices
t, s = table(["Ref", "Property", "Postcode", "Use", "Construction (walls/roof)", "Built", "Floor Area m2", "Sprinklers", "Intruder Alarm", "Buildings", "Contents", "Loss of Rent (3 yrs)", "TIV"],
             [(["01", "Kingsmede House, 14 Albion Street, Leeds", "LS1 6HX", "Offices", "Brick / slate pitched", "1890 (Grade II)", "2,140", "No", "Redcare"], [6_850_000, 420_000, 1_350_000]),
              (["02", "Unit 4 Canalside Court, Wakefield", "WF1 5PR", "Offices", "Steel frame, composite panel (LPCB)", "2009", "1,310", "No", "Bells only"], [2_450_000, 180_000, 540_000]),
              (["03", "The Mint Building, 2 Cheapside, Bradford", "BD1 4JA", "Offices + ground floor retail", "Reinforced concrete / flat felt", "1968", "3,600", "Yes", "Redcare"], [8_900_000, 310_000, 2_100_000])],
             gbp, total_label="Total", sep="\n")
r13 = add("core", C("UK", "sheet", "2-10", "full_cope", "reinstatement", "office", "words", "GBP"),
          "gA:sov:thistledown-brokers-uk-schedule", "sov",
          "Thistledown Brokers Ltd - Property Schedule\nClient: Pennine Arches Estates Ltd | Renewal 01/04/2028 | Basis: Reinstatement, Day One uplift 15%\n" + t)

# --- 14 Thistledown mixed-use, 11-100, no TIV, long
t, s = table(["Ref", "Address", "Postcode", "Occupancy", "Construction", "Year", "Storeys", "Listed", "Flood Zone", "Buildings SI", "Contents SI", "Loss of Rent SI", "Total Sum Insured"],
             [(["001", "1-7 Market Place, Ripon", "HG4 1BP", "Shops with flats over", "Stone / slate", "c.1820", "3", "Gr II", "1"], [3_200_000, 0, 410_000]),
              (["002", "22 High Street, Harrogate", "HG1 1RT", "Restaurant ground, offices over", "Brick / slate", "1905", "4", "No", "1"], [2_150_000, 60_000, 290_000]),
              (["003", "Wharf Mill, Mill Lane, Knaresborough", "HG5 8AB", "Residential flats (14)", "Stone, timber floors / slate", "1840 conv 2004", "4", "Gr II", "3a"], [5_600_000, 85_000, 720_000]),
              (["004", "Units 1-3 Station Parade, Skipton", "BD23 1ND", "Shops, gym first floor", "Steel frame, brick clad / flat", "1972", "2", "No", "2"], [1_980_000, 0, 260_000]),
              (["005", "The Old Exchange, 9 Bond End, Otley", "LS21 3AD", "Bar + 3 flats over", "Brick / slate", "1888", "3", "No", "1"], [1_450_000, 30_000, 175_000]),
              (["006", "Abbey Yard, Selby", "YO8 4PT", "Mixed: dental surgery, 6 flats", "Timber frame, brick skin / tile", "2011", "3", "No", "3a"], [2_750_000, 40_000, 330_000])],
             gbp, total_label=None, sep="\n")
r14 = add("core", C("UK", "sheet", "11-100", "full_cope", "reinstatement", "mixed_use", "words", "GBP", no_tiv=True, rows_shown="first 6 of 41"),
          "gA:sov:thistledown-brokers-uk-schedule", "sov",
          "THISTLEDOWN BROKERS LTD\nSCHEDULE OF PROPERTIES - Dalesway Property Holdings Ltd and associated companies\n"
          "Renewal date 25/03/2028. Sums insured on a Reinstatement basis, declared values; Day One uplift 20% applies. Loss of Rent 3 years.\n"
          "41 properties. Grand total sum insured £58,412,500 (see summary tab).\n" + t +
          "\nNotes: flood zone per EA mapping. Ref 003 subject to unoccupancy condition until refurbishment completes.")

# --- 15 Thistledown single retail, short, no TIV
r15 = add("core", C("UK", "sheet", "1", "values_only", "reinstatement", "retail", "none", "GBP", no_tiv=True),
          "gA:sov:thistledown-brokers-uk-schedule", "sov",
          "Thistledown Brokers - Schedule ; Ref | Premises | Buildings | Contents | Stock | Sum Insured ; "
          "1 | 48 Fore Street, Hexham NE46 1NA (shop) | £780,000 | £65,000 | £140,000 | £985,000 ; Basis: reinstatement")

# --- 16 Calloway Prentice, messy merged, manufacturing, free text
r16 = add("core", C("UK", "sheet", "2-10", "messy_merged", "reinstatement", "manufacturing", "free_text", "GBP"),
          "gA:sov:calloway-prentice-merged", "sov", """
CALLOWAY PRENTICE INSURANCE BROKERS          ASSET SCHEDULE - MATERIAL DAMAGE & BI
Insured: Severnside Plastics Group Ltd       Period: 01/10/2027 - 30/09/2028
SITE DETAILS |  |  | CONSTRUCTION & PROTECTION |  |  | SUMS INSURED (£) - REINSTATEMENT |  |  |  |
Site | Address | Activity | Construction | Sprinklers | Fire alarm | Buildings | Plant & Mach | Stock | GP (24m) | TIV
1 | Unit 7, Westgate Ind Est, Gloucester GL2 5HR | Extrusion | steel portal, part EPS panel (pre-1995) remainder rockwool | none | L2 | 4,200,000 | 6,800,000 | 1,100,000 | 9,500,000 | 21,600,000
2 | Brookfield Works, Stroud GL5 3QD | Moulding + tool room | old mill, brick/timber floors, newer steel annex | part (annex only) | L3 | 2,650,000 | 3,350,000 | 600,000 | 4,100,000 | 10,700,000
3 | Plot 12 Quedgeley Park GL2 4NB | Warehouse | steel/clad, LPCB 1181 panels | ESFR | L2 | 3,100,000 | 150,000 | 2,250,000 | 0 | 5,500,000
TOTAL |  |  |  |  |  | 9,950,000 | 10,300,000 | 3,950,000 | 13,600,000 | 37,800,000
""")

# --- 17 Calloway Prentice, 100+ high street retail, values only
r17 = add("core", C("UK", "sheet", "100+", "values_only", "reinstatement", "retail", "none", "GBP", rows_shown="first 2 of 186"),
          "gA:sov:calloway-prentice-merged", "sov",
          "CALLOWAY PRENTICE | Brackenhurst Opticians plc - 186 branches | Reinstatement ; "
          "Br | Town | Postcode | Tenure | Buildings | Shopfit & Equipment | Stock | TIV ; "
          "001 | Taunton | TA1 1SA | Leasehold | 0 | 185,000 | 42,000 | 227,000 ; "
          "002 | Yeovil | BA20 1EG | Leasehold | 0 | 160,000 | 38,500 | 198,500")


# --- 18 Dunmere prose cover sheet + schedule, schools, no TIV
r18 = add("core", C("UK", "prose_cover", "2-10", "full_cope", "reinstatement", "school", "words", "GBP", no_tiv=True),
          "gA:sov:dunmere-prose-cover", "sov", """
DUNMERE INSURANCE BROKERS LIMITED
Statement of Values - Holloway Fields Academy Trust - renewal 1 September 2028

This schedule sets out the buildings and contents sums insured for the Trust's four schools. Buildings figures are reinstatement costs taken from the 2026 desktop rebuild exercise, index-linked by 4.5%; contents are the Trust's own declared values. Blocks with CLASP system build are shown separately because insurers rate them differently. All sites have intruder alarms monitored to a central station; none are sprinklered except the new science block at Site 2.

Site | School / block | Address | Construction | Built | GIFA m2 | Buildings £ | Contents £ | Total £
1 | Holloway Fields Primary - main | Fennel Road, Northampton NN3 2LP | Brick, pitched tile roof | 1964 | 2,310 | 6,120,000 | 410,000 | 6,530,000
1 | Holloway Fields Primary - CLASP block | as above | CLASP steel frame, flat felt | 1971 | 880 | 2,050,000 | 140,000 | 2,190,000
2 | Weston Brook Secondary | Barrack Lane, Wellingborough NN8 4EZ | Brick/block, part flat roof | 1988 | 9,450 | 24,900,000 | 1,650,000 | 26,550,000
2 | Weston Brook - science block (sprinklered) | as above | Steel frame, rainscreen cladding | 2023 | 1,620 | 5,400,000 | 720,000 | 6,120,000
3 | Ashfield Lane Infants | Ashfield Lane, Kettering NN15 7JQ | Brick, pitched slate | 1902 | 1,140 | 3,350,000 | 175,000 | 3,525,000
Total |  |  |  |  |  | 41,820,000 | 3,095,000 | 44,915,000
""")

# --- 19 Dunmere prose cover, single church, no TIV
r19 = add("core", C("UK", "prose_cover", "1", "full_cope", "reinstatement", "church", "words", "GBP", no_tiv=True),
          "gA:sov:dunmere-prose-cover", "sov", """
DUNMERE INSURANCE BROKERS LIMITED - Schedule of Values
The Parochial Church Council of St Wendreda, Fenholme. Sums insured are on a reinstatement basis using like-for-like traditional materials, as the church is Grade I listed.
Building | Address | Construction | Built | Buildings | Contents (incl. organ, bells) | Total Sum Insured
Church | Church Lane, Fenholme PE15 0RT | Coursed limestone, lead and slate roofs | 13th c., tower 1480 | £6,400,000 | £385,000 | £6,785,000
""")

# --- 20 Albright & Coyle UK MGA form, hotels, long
r20 = add("core", C("UK", "pdf_form", "2-10", "full_cope", "reinstatement", "hotel", "words", "GBP", carrier_branded=True),
          "gA:sov:albright-coyle-mga-pf3-2024", "sov", """
ALBRIGHT & COYLE UNDERWRITING LTD   (Coverholder)
PROPERTY SCHEDULE OF VALUES - FORM PF3 (2024)                                    Page 1/2
Proposer: Lowmoor Inns & Hotels Ltd          Broker: Pellbridge Harris LLP         Inception: 14/02/2028
Basis of cover: Reinstatement (Buildings), Replacement as new (Contents), Gross Profit 24 month indemnity period
SECTION A - PREMISES
No. | Address & postcode | Trade | Rooms | Walls | Roof | Year built | Listed | Fire detection | Sprinklers
1 | The Drovers Arms, Market Sq, Kendal LA9 4TN | Hotel + bar | 22 | Stone | Slate | 1760 | Grade II | L1 automatic | No
2 | Lakeside Lodge, Bowness-on-Windermere LA23 3HQ | Hotel + spa | 48 | Brick/render | Slate & flat felt (spa) | 1910 / 2015 ext | No | L1 automatic | Spa only
3 | Fellgate Hotel, Penrith CA11 7YR | Hotel | 31 | Stone | Slate | 1880 | No | L2 | No
SECTION B - SUMS INSURED (GBP)
No. | Buildings | Contents & Stock | Gross Profit | TIV
1 | 3,900,000 | 420,000 | 1,100,000 | 5,420,000
2 | 9,750,000 | 1,280,000 | 3,600,000 | 14,630,000
3 | 5,200,000 | 560,000 | 1,450,000 | 7,210,000
Totals | 18,850,000 | 2,260,000 | 6,150,000 | 27,260,000
Declaration: values provided by proposer. Flood: Loc 2 lakeside, EA zone 3. Thatch: none.
""")

# --- 21 Albright & Coyle single care home short, no TIV
r21 = add("core", C("UK", "pdf_form", "1", "values_only", "reinstatement", "healthcare", "none", "GBP", carrier_branded=True, no_tiv=True),
          "gA:sov:albright-coyle-mga-pf3-2024", "sov",
          "ALBRIGHT & COYLE UNDERWRITING LTD  PROPERTY SCHEDULE OF VALUES - FORM PF3 (2024)\n"
          "Proposer: Meadowsweet Care Ltd | No. 1 | Elmhurst Care Home, 4 Vicarage Rd, Hereford HR1 2QB | 46 beds\n"
          "Buildings £5,850,000 | Contents £640,000 | Gross Profit £1,900,000 | Total £8,390,000")

# --- 22 Kettering Vale carrier property schedule form, warehouses UK
r22 = add("core", C("UK", "pdf_form", "11-100", "full_cope", "reinstatement", "warehouse", "words", "GBP", carrier_branded=True, rows_shown="first 4 of 14"),
          "gA:sov:kettering-vale-plc-ps10-2023", "sov", """
KETTERING VALE INSURANCE PLC                SCHEDULE OF PROPERTIES AND VALUES      PS10 (rev. 06/2023)
Policyholder: Thornfield Freight Services Ltd     Policy No: KV/CP/2283117     Basis: Reinstatement
Loc | Address | Use | Construction | Built | Area m2 | Sprinklers | Buildings | Contents | Stock | TIV
1 | Unit A Magna Park, Lutterworth LE17 4XW | Distribution | Steel frame, LPCB panels | 2007 | 28,400 | ESFR | 22,500,000 | 3,100,000 | 9,800,000 | 35,400,000
2 | Unit 9 Daventry Intl Rail Freight Terminal NN6 7GX | Distribution | Steel frame, LPCB panels | 2015 | 19,750 | ESFR | 16,900,000 | 2,400,000 | 7,250,000 | 26,550,000
3 | Bridge Rd, Corby NN17 5XR | Warehouse + workshop | Steel frame, part EPS panel | 1989 | 6,300 | None | 4,150,000 | 650,000 | 1,900,000 | 6,700,000
4 | 12 Swan Valley Way, Northampton NN4 9BD | Cross dock | Steel frame, brick/clad | 1997 | 8,900 | None | 5,600,000 | 820,000 | 300,000 | 6,720,000
""")

# --- 23 Lindqvist Brokerage, EUR, UK market, manufacturing
r23 = add("core", C("UK", "sheet", "2-10", "full_cope", "reinstatement", "manufacturing", "words", "EUR", number_format="continental"),
          "gA:sov:lindqvist-brokerage-eur", "sov",
          "Lindqvist Brokerage B.V. obo London placement - Location Schedule - Veldhaven Food Machinery Group - values in EUR, reinstatement / new replacement value\n"
          "Loc | Address | Country | Activity | Construction | Year | m2 | Sprinkler | Buildings | Machinery | Stock | BI 18m | TIV\n"
          "1 | Industrieweg 14, 5683 Best | NL | Machining + assembly | Concrete frame, steel deck roof | 1994 | 18.500 | Yes (VdS) | 21.400.000 | 18.750.000 | 4.200.000 | 12.600.000 | 56.950.000\n"
          "2 | Am Hafen 7, 47119 Duisburg | DE | Welding, paint shop | Steel frame, sandwich panel PIR | 2006 | 9.800 | No | 8.900.000 | 7.300.000 | 1.650.000 | 5.100.000 | 22.950.000\n"
          "3 | Rue de l'Industrie 31, 7700 Mouscron | BE | Spares warehouse | Steel frame, mineral wool panel | 2019 | 6.400 | Yes | 4.750.000 | 350.000 | 3.900.000 | 0 | 9.000.000\n"
          "Total | | | | | | | | 35.050.000 | 26.400.000 | 9.750.000 | 17.700.000 | 88.900.000")

# --- 24 Lindqvist, US market, data centres EUR + USD values only
r24 = add("core", C("US", "sheet", "1", "values_only", "replacement_cost", "data_centre", "none", "EUR", fx="USD equivalent shown"),
          "gA:sov:lindqvist-brokerage-eur", "sov",
          "LINDQVIST BROKERAGE | Arcwell Compute Inc. - EU site, US master program | RC | 1 EUR = 1.08 USD ; "
          "Site | City | Building EUR | Equipment EUR | BI EUR | TIV EUR | TIV USD ; "
          "AMS-2 | Amsterdam | 34,000,000 | 61,000,000 | 15,000,000 | 110,000,000 | 118,800,000")


# --- 25 Sabledown prose cover, mixed-use US, long
r25 = add("core", C("US", "prose_cover", "2-10", "full_cope", "replacement_cost", "mixed_use", "iso_number", "USD"),
          "gA:sov:sabledown-cover-narrative", "sov", """
SABLEDOWN & ROYCE INSURANCE BROKERS
STATEMENT OF VALUES - COVER SHEET
Insured: Calder Street Partners LLC (and as per schedule of named insureds)
Effective: 05/01/2028       Valuation: Replacement Cost, no coinsurance (agreed amount endorsement requested)

The insured owns five urban mixed-use buildings in Pittsburgh and Cleveland. Ground floors are let to retail and restaurant tenants; upper floors are residential apartments, 112 units in total. Values below were updated by the insured's asset manager in February 2028 using a cost-per-square-foot trend of 7% over expiring. Loc 4 is undergoing a facade repair and has scaffolding until August. Restaurant cooking at Locs 1, 3 and 5 has UL 300 hood suppression.

Loc | Address | Occupancy | ISO | Yr Built | Sq Ft | Stories | Spr | PC | Building | Contents | Rents | TIV
1 | 1405 Penn Ave, Pittsburgh PA | Restaurant / 18 apts | 2 | 1912 | 24,600 | 4 | Y | 1 | 6,150,000 | 50,000 | 780,000 | 6,980,000
2 | 3720 Butler St, Pittsburgh PA | Retail / 22 apts | 2 | 1925 | 29,000 | 4 | N | 1 | 7,250,000 | 40,000 | 910,000 | 8,200,000
3 | 2150 E 4th St, Cleveland OH | Restaurant, bar / 30 apts | 5 | 2009 | 41,800 | 6 | Y | 2 | 12,300,000 | 75,000 | 1,420,000 | 13,795,000
4 | 1830 Superior Ave, Cleveland OH | Retail / 26 apts | 2 | 1931 | 33,500 | 5 | Partial | 2 | 8,400,000 | 30,000 | 1,050,000 | 9,480,000
5 | 701 W 25th St, Cleveland OH | Brewpub / 16 apts | 1 | 1898 | 19,200 | 3 | N | 2 | 4,350,000 | 120,000 | 560,000 | 5,030,000
Total |  |  |  |  |  |  |  |  | 38,450,000 | 315,000 | 4,720,000 | 43,485,000
""")

# --- 26 Sabledown prose cover, churches ACV, values only, no TIV
r26 = add("core", C("US", "prose_cover", "11-100", "values_only", "acv", "church", "none", "USD", no_tiv=True, rows_shown="first 6 of 38"),
          "gA:sov:sabledown-cover-narrative", "sov", """
Sabledown & Royce - Statement of Values cover sheet. Insured: Missionary Diocese of the Upper Cumberland and its 38 parishes. At the Diocese's request values are on an Actual Cash Value basis for buildings over 75 years old and Replacement Cost for the rest; the basis column shows which. Combined values for all parishes: $96,240,000.
Parish | City, ST | Basis | Building | Contents | Total Values
St. Ambrose | Cookeville TN | RC | 4,100,000 | 380,000 | 4,480,000
Holy Cross | Crossville TN | ACV | 1,850,000 | 210,000 | 2,060,000
St. Brendan | Somerset KY | ACV | 2,300,000 | 190,000 | 2,490,000
Christ the King | Knoxville TN | RC | 7,650,000 | 640,000 | 8,290,000
St. Clare | Jamestown TN | ACV | 980,000 | 95,000 | 1,075,000
Our Lady of the Hills | London KY | RC | 3,200,000 | 260,000 | 3,460,000
""")

# --- 27 Ironhollow Wholesale, 100+, full COPE, retail, long
r27 = add("core", C("US", "sheet", "100+", "full_cope", "replacement_cost", "retail", "iso_number", "USD", rows_shown="first 3 of 212"),
          "gA:sov:ironhollow-wholesale-export", "sov",
          "IRONHOLLOW WHOLESALE INSURANCE SERVICES - SOV EXPORT - Palmetto Ridge Fuel & Convenience Holdings - 212 locs - RC - TIV $318,604,000\n"
          "LocID | Store # | Address | City | ST | Zip | County | Occ Desc | Const (ISO) | YrBlt | SqFt | Canopy | Sprk | PPC | Bldg | Canopy Val | Contents | Fuel Sys | BI | TIV\n"
          "1 | 1004 | 1601 US-27 S | Avon Park | FL | 33825 | Highlands | C-store w/ fuel | 3 | 2004 | 4,200 | Y | N | 4 | 1,050,000 | 210,000 | 280,000 | 340,000 | 160,000 | 2,040,000\n"
          "2 | 1006 | 820 W Main St | Wauchula | FL | 33873 | Hardee | C-store w/ fuel | 2 | 1991 | 2,950 | Y | N | 5 | 690,000 | 175,000 | 240,000 | 310,000 | 120,000 | 1,535,000\n"
          "3 | 1011 | 3311 Lakeland Hills Blvd | Lakeland | FL | 33805 | Polk | C-store w/ fuel + QSR | 3 | 2016 | 5,600 | Y | N | 2 | 1,640,000 | 260,000 | 410,000 | 395,000 | 290,000 | 2,995,000")


# --- 28 Ironhollow, 100+, values only, short-ish
r28 = add("core", C("US", "sheet", "100+", "values_only", "replacement_cost", "warehouse", "none", "USD", rows_shown="first 3 of 140"),
          "gA:sov:ironhollow-wholesale-export", "sov",
          "IRONHOLLOW SOV EXPORT | Tri-County Self Storage LLC | 140 facilities | RC\n"
          "LocID | City | ST | Bldg | Contents | BI | TIV\n"
          "1 | Lubbock | TX | 3,400,000 | 25,000 | 410,000 | 3,835,000\n"
          "2 | Amarillo | TX | 2,950,000 | 20,000 | 360,000 | 3,330,000\n"
          "3 | Midland | TX | 4,100,000 | 30,000 | 520,000 | 4,650,000")

# --- 29 Quillfeather hotels, free text construction
r29 = add("core", C("US", "sheet", "2-10", "full_cope", "replacement_cost", "hotel", "free_text", "USD"),
          "gA:sov:quillfeather-risk-hospitality", "sov",
          "Quillfeather Risk Services - Hospitality SOV - Brightmoor Hotel Group LLC - RC - 2028/29\n"
          "Loc | Property | Address | Keys | Constr | YOC | Stories | Sq Ft | Sprk | PC | Bldg | FF&E | BI (12m) | TIV\n"
          "1 | Brightmoor Inn Savannah Historic | 22 Bay St, Savannah GA | 64 | JM/frame w mansard | 1884 / gut reno 2012 | 4 | 46,000 | Y | 2 | 14,800,000 | 2,100,000 | 3,900,000 | 20,800,000\n"
          "2 | Brightmoor Suites Airport | 1470 Airways Ave, Charleston SC | 118 | wood frame 4 over 1 podium | 2017 | 5 | 78,500 | Y (13R) | 3 | 19,600,000 | 3,300,000 | 5,200,000 | 28,100,000\n"
          "3 | Brightmoor Beach | 302 S Ocean Blvd, Myrtle Beach SC | 96 | masonry nc, hip roof | 1989 | 8 | 71,000 | Y | 3 | 17,250,000 | 2,650,000 | 4,700,000 | 24,600,000\n"
          "Totals | | | 278 | | | | | | | 51,650,000 | 8,050,000 | 13,800,000 | 73,500,000")

# --- 30 Quillfeather, merged headers, 11-100, long, no TIV
r30 = add("core", C("US", "sheet", "11-100", "messy_merged", "replacement_cost", "hotel", "free_text", "USD", no_tiv=True, rows_shown="first 6 of 16"),
          "gA:sov:quillfeather-risk-hospitality", "sov", """
QUILLFEATHER RISK SERVICES          HOSPITALITY STATEMENT OF VALUES          Wayfarer Lodging Trust (16 hotels)
Valuation: Replacement Cost | BI 18 months | Values per owner 2/2028 | Grand Total Insured Value $402,900,000
PROPERTY |  |  |  | C O P E |  |  |  |  | V A L U E S |  |  |
Hotel | Flag | City, ST | Keys | Construction | YOC | Flrs | Sprk | Dist to coast | Building | FF&E / Contents | BI/EE | Total
Wayfarer Galveston | upscale select | Galveston TX | 152 | conc frame, EIFS | 2006 | 9 | 100% | 0.1 mi | 31,400,000 | 4,600,000 | 8,100,000 | 44,100,000
Wayfarer Corpus Christi Bayfront | full svc | Corpus Christi TX | 210 | steel/conc, curtain wall | 1984 rnv 2018 | 12 | 100% | 0.2 mi | 46,800,000 | 7,200,000 | 12,500,000 | 66,500,000
Wayfarer Austin Domain | select | Austin TX | 128 | wd frame 4 story over conc podium | 2019 | 5 | 100% | n/a | 24,300,000 | 3,800,000 | 6,400,000 | 34,500,000
Wayfarer San Marcos | ext stay | San Marcos TX | 96 | wood frame, brick veneer | 2001 | 3 | 100% | n/a | 11,600,000 | 1,700,000 | 2,900,000 | 16,200,000
Wayfarer Lake Charles | select | Lake Charles LA | 104 | masonry nc | 1996 rnv 2022 | 4 | 100% | 28 mi | 15,900,000 | 2,300,000 | 3,600,000 | 21,800,000
Wayfarer Biloxi | full svc | Biloxi MS | 188 | conc frame | 2008 | 11 | 100% | 0.05 mi | 39,750,000 | 6,050,000 | 9,700,000 | 55,500,000
Subtotal TX/LA/MS coastal tier 1 (Galveston, CC, Biloxi): 166,100,000
""")

# --- 31 Bramblecote churches UK 11-100
r31 = add("core", C("UK", "sheet", "11-100", "full_cope", "reinstatement", "church", "words", "GBP", rows_shown="first 6 of 22"),
          "gA:sov:bramblecote-faith-schedule", "sov",
          "BRAMBLECOTE BROKERS - Schedule of Values - Ravensmoor Methodist Circuit (22 chapels) - Reinstatement\n"
          "No | Chapel | Address | Postcode | Walls/Roof | Built | Listed | Alarm | Buildings | Contents | TIV\n"
          "1 | Bethesda | High St, Holmfirth | HD9 3HE | Stone / slate | 1857 | Gr II | Yes | 2,350,000 | 85,000 | 2,435,000\n"
          "2 | Zion | Towngate, Marsden | HD7 6DD | Stone / slate | 1872 | Gr II* | Yes | 3,100,000 | 110,000 | 3,210,000\n"
          "3 | Ebenezer | Chapel Hill, Slaithwaite | HD7 5AB | Stone / slate | 1830 | No | No | 1,450,000 | 40,000 | 1,490,000\n"
          "4 | Wesley Hall | Station Rd, Honley | HD9 6BU | Brick / tile | 1961 | No | Yes | 980,000 | 60,000 | 1,040,000\n"
          "5 | Providence | Moor Lane, Meltham | HD9 5JZ | Stone / slate, flat felt hall ext | 1868 / 1974 | No | No | 1,720,000 | 55,000 | 1,775,000\n"
          "6 | Salem | Lockwood Rd, Huddersfield | HD1 3QR | Brick / slate | 1899 | Gr II | Yes | 2,050,000 | 70,000 | 2,120,000")

# --- 32 Bramblecote churches short values only no TIV
r32 = add("core", C("UK", "sheet", "2-10", "values_only", "reinstatement", "church", "none", "GBP", no_tiv=True),
          "gA:sov:bramblecote-faith-schedule", "sov",
          "Bramblecote Brokers ; St Oswin's PCC ; Building | Buildings £ | Contents £ | Sum Insured £ ; "
          "Church | 4,850,000 | 260,000 | 5,110,000 ; Church hall | 690,000 | 35,000 | 725,000 ; Total | 5,540,000 | 295,000 | 5,835,000")

# --- 33 Marchetti Dunn healthcare ISO
r33 = add("core", C("US", "sheet", "2-10", "full_cope", "replacement_cost", "healthcare", "iso_number", "USD"),
          "gA:sov:marchetti-dunn-healthcare", "sov",
          "MARCHETTI DUNN INSURANCE BROKERS | SOV | Bayou Teche Senior Living Inc | RC\n"
          "Loc | Facility | Address | Occ | ISO Cl | Yr | SqFt | Beds | Sprk | Gen | PPC | Bldg | Contents | BI | TIV\n"
          "1 | Teche Gardens SNF | 400 Main St, New Iberia LA | Skilled nursing | 4 | 1997 | 52,000 | 120 | Y | Y | 3 | 11,700,000 | 1,850,000 | 3,200,000 | 16,750,000\n"
          "2 | Teche Gardens AL | 402 Main St, New Iberia LA | Assisted living | 1 | 2014 | 38,500 | 64 | Y | Y | 3 | 7,900,000 | 900,000 | 1,600,000 | 10,400,000\n"
          "3 | Cypress Bend Memory Care | 15 Levee Rd, Breaux Bridge LA | Memory care | 2 | 2005 | 21,000 | 36 | Y | N | 5 | 4,250,000 | 520,000 | 880,000 | 5,650,000\n"
          "TOTAL | | | | | | | 220 | | | | 23,850,000 | 3,270,000 | 5,680,000 | 32,800,000")

# --- 34 Marchetti Dunn clinics merged, 11-100, no TIV, long
r34 = add("core", C("US", "sheet", "11-100", "messy_merged", "replacement_cost", "healthcare", "free_text", "USD", no_tiv=True, rows_shown="first 7 of 19"),
          "gA:sov:marchetti-dunn-healthcare", "sov", """
MARCHETTI DUNN INSURANCE BROKERS - SCHEDULE OF LOCATIONS & VALUES
Gulfside Family Medicine Associates PA  |  19 clinics  |  Replacement Cost  |  Combined Total Values $41,385,000
  LOCATION        |                     |  BUILDING                          |           |  VALUES (USD)                      |
Clinic | Address | Owned/Lsd | Constr | Yr | SqFt | Sprk | Bldg | Med Equip | Contents | EDP | BI | Total
Pensacola Main | 4500 Bayou Blvd, Pensacola FL | Owned | brick veneer on CMU, metal roof | 2003 | 14,200 | Y | 3,350,000 | 1,900,000 | 420,000 | 260,000 | 1,100,000 | 7,030,000
Navarre | 8740 Navarre Pkwy, Navarre FL | Leased | strip ctr unit, tilt-up | 2011 | 4,100 | N | 0 | 650,000 | 120,000 | 80,000 | 310,000 | 1,160,000
Milton | 6086 Stewart St, Milton FL | Owned | wood frm, stucco, shingle (roof 2019) | 1985 | 3,600 | N | 690,000 | 380,000 | 85,000 | 45,000 | 240,000 | 1,440,000
Gulf Breeze | 1159 Gulf Breeze Pkwy | Leased | JM, flat roof w/ parapet | 1978 | 5,200 | N | 0 | 720,000 | 140,000 | 90,000 | 350,000 | 1,300,000
Crestview | 2290 S Ferdon Blvd, Crestview FL | Owned | pre-eng mtl bldg | 2016 | 6,800 | Y | 1,250,000 | 880,000 | 160,000 | 110,000 | 420,000 | 2,820,000
Fort Walton Bch | 1 Hollywood Blvd NE | Leased | med office bldg, conc/steel (MNC?) | 1999 | 7,400 | Y | 0 | 1,050,000 | 190,000 | 140,000 | 610,000 | 1,990,000
Destin Urgent Care | 34 Mattie M Kelly Blvd, Destin FL | Owned | CMU, impact glass, hip roof | 2020 | 5,900 | Y | 1,780,000 | 1,320,000 | 150,000 | 120,000 | 840,000 | 4,210,000
""")

# --- 35 Polar Vault insured-prepared, cold storage, OCR error
r35 = add("core", C("US", "sheet", "2-10", "full_cope", "replacement_cost", "cold_storage", "words_and_iso", "USD", noise="ocr_error"),
          "gA:sov:insured-prepared-polarvault", "sov",
          "POLAR VAULT REFRIGERATED WAREHOUSING INC - LOCATION & VALUE SCHEDULE (prepared by Finance, 10/2027)\n"
          "Site | Address | Use | Construction | ISO | Built | Sq Ft | Temp | Sprinkler | Bldg | Equip/Refrig | Stock (cust. goods, legal liab) | Spoilage | TIV\n"
          "Omaha 1 | 3900 S 60th St, Omaha NE | Freezer whse | Tilt-up conc, IMP walls | 4 | 2010 | 210,000 | -10F | Dry pipe ESFR | 19,500,000 | 8,400,000 | 22,000,000 | 1,500,000 | 51,400,000\n"
          "Omaha 2 | 11 Dock Rd, Council Bluffs IA | Cooler + freezer | Steel frarne, EPS panels | 3 | 1992 | 96,000 | 34F/-5F | Wet (cooler only) | 7,800,000 | 4,100,000 | 9,500,000 | 750,000 | 22,150,000\n"
          "Sioux City | 700 Port Neal Rd, Sergeant Bluff IA | Blast freezer | Steel frame, PIR panels | 3 | 2019 | 74,500 | -20F | Dry pipe | 8,900,000 | 6,200,000 | 7,400,000 | 600,000 | 23,100,000\n"
          "TOTAL | | | | | | 380,500 | | | 36,200,000 | 18,700,000 | 38,900,000 | 2,850,000 | 96,650,000")

# --- 36 Polar Vault single loc short ACV
r36 = add("core", C("US", "sheet", "1", "values_only", "acv", "cold_storage", "none", "USD"),
          "gA:sov:insured-prepared-polarvault", "sov",
          "Polar Vault - Grand Island NE cold store - ACV ; Bldg | Refrig Equip | Stock | TIV ; 6,100,000 | 2,750,000 | 5,300,000 | 14,150,000")

# --- 37 Westerly Ashgrove data centres, long
r37 = add("core", C("US", "sheet", "2-10", "full_cope", "replacement_cost", "data_centre", "iso_number", "USD"),
          "gA:sov:westerly-ashgrove-tech", "sov",
          "WESTERLY ASHGROVE RISK PARTNERS\nStatement of Values: Halcyon Data Infrastructure LLC | Valuation RC | BI/EE 24 months, waiting period 24h | Effective 08/01/2028\n"
          "Site | Address | Occupancy | ISO Const | Yr Built | Gross Sq Ft | Raised floor sq ft | MW (IT) | Suppression | Gen backup | PPC | Building | Mech/Elec Infrastructure | Tenant IT Equip (CCC) | BI/EE | TIV\n"
          "ASH-1 | 21700 Filigree Ct, Ashburn VA | Data center - colo | 6 | 2014 | 186,000 | 92,000 | 24 | Pre-action + VESDA | 2N diesel, 48h fuel | 1 | 62,000,000 | 118,000,000 | 40,000,000 | 55,000,000 | 275,000,000\n"
          "ASH-2 | 21720 Filigree Ct, Ashburn VA | Data center - colo | 5 | 2020 | 240,000 | 128,000 | 36 | Pre-action + VESDA | 2N diesel, 48h | 1 | 81,000,000 | 164,000,000 | 25,000,000 | 72,000,000 | 342,000,000\n"
          "PHX-1 | 615 N 48th St, Phoenix AZ | Data center - enterprise | 4 | 2009 | 98,000 | 41,000 | 9 | Clean agent + wet | N+1 | 2 | 28,500,000 | 46,000,000 | 12,500,000 | 18,000,000 | 105,000,000\n"
          "HQ | 1100 Wilson Blvd Ste 1400, Arlington VA | Office (leased) | 6 | 1989 | 22,000 | 0 | 0 | Wet | none | 1 | 0 | 0 | 1,400,000 | 600,000 | 2,000,000\n"
          "Totals | | | | | 546,000 | 261,000 | 69 | | | | 171,500,000 | 328,000,000 | 79,000,000 | 145,600,000 | 724,100,000\n"
          "Notes: Tenant IT equipment shown is care, custody and control only, as required by MSA. Utility service interruption sublimit requested at $25M.")

# --- 38 Westerly Ashgrove short values only no TIV
r38 = add("core", C("US", "sheet", "2-10", "values_only", "replacement_cost", "data_centre", "none", "USD", no_tiv=True),
          "gA:sov:westerly-ashgrove-tech", "sov",
          "Westerly Ashgrove - values - Northpine Edge Compute Inc ; Site | Building | Equipment | BI | Total Insured Value ; "
          "DEN-1 | 14,500,000 | 38,000,000 | 9,000,000 | 61,500,000 ; SLC-1 | 11,000,000 | 27,500,000 | 6,500,000 | 45,000,000")

# --- 39 Penhallow schools UK long
r39 = add("core", C("UK", "sheet", "11-100", "full_cope", "reinstatement", "school", "words", "GBP", rows_shown="first 7 of 15"),
          "gA:sov:penhallow-associates-education", "sov",
          "PENHALLOW ASSOCIATES LTD - EDUCATION PRACTICE\nProperty Schedule - Kernow Coast Learning Trust (15 academies) - Reinstatement inc. professional fees and debris removal - Renewal 01/09/2028\n"
          "Ref | Academy | Address | Postcode | Phase | Construction | Year | GIFA m2 | Pupils | Fire alarm | Sprinklers | Buildings £ | Contents £ | ICT £ | TIV £\n"
          "KC01 | Porthmorna Academy | Trevenson Rd, Camborne | TR14 8RX | Secondary | Brick/block, flat & pitched roofs | 1958 / 2004 | 11,200 | 1,140 | L2 | No | 29,500,000 | 1,600,000 | 650,000 | 31,750,000\n"
          "KC02 | Penwartha Primary | Chapel St, Redruth | TR15 2BY | Primary | Granite / slate | 1889 | 1,350 | 210 | L3 | No | 4,100,000 | 160,000 | 70,000 | 4,330,000\n"
          "KC03 | Carn View Primary | Agar Rd, Illogan | TR16 4EB | Primary | Timber frame (modular), metal roof | 2016 | 1,900 | 315 | L2 | Yes | 5,750,000 | 210,000 | 95,000 | 6,055,000\n"
          "KC04 | St Ia Academy | Higher Tregenna Rd, St Ives | TR26 2DE | Secondary | System build (SCOLA), flat roof | 1972 | 7,800 | 760 | L2 | No | 20,400,000 | 1,050,000 | 420,000 | 21,870,000\n"
          "KC05 | Hayle Sands Primary | Foundry Sq, Hayle | TR27 4HH | Primary | Brick / tile | 1995 | 1,600 | 260 | L3 | No | 4,650,000 | 175,000 | 80,000 | 4,905,000\n"
          "KC06 | Marazion Infants | Turnpike Hill, Marazion | TR17 0DS | Infant | Granite / slate | 1902 | 640 | 95 | L3 | No | 2,050,000 | 70,000 | 30,000 | 2,150,000\n"
          "KC07 | Lizard Point Academy | Clodgey Lane, Helston | TR13 8PJ | Secondary | Steel frame, curtain walling (RAAC survey: none found) | 1979 | 8,450 | 820 | L1 | No | 22,800,000 | 1,180,000 | 470,000 | 24,450,000")

# --- 40 Penhallow 100+ values only short no TIV
r40 = add("core", C("UK", "sheet", "100+", "values_only", "reinstatement", "school", "none", "GBP", no_tiv=True, rows_shown="first 3 of 104"),
          "gA:sov:penhallow-associates-education", "sov",
          "Penhallow Associates | Wessex Downs Diocesan Schools (104 sites) | Ref | Site | Buildings | Contents | Total Sum Insured ; "
          "W001 | Amesbury CE Primary | 3,950,000 | 140,000 | 4,090,000 ; W002 | Tisbury St John's | 2,600,000 | 95,000 | 2,695,000 ; W003 | Downton CE Primary | 3,300,000 | 120,000 | 3,420,000")

# --- 41 Trevanion & Lusk, merged mixed-use UK
r41 = add("core", C("UK", "sheet", "2-10", "messy_merged", "reinstatement", "mixed_use", "free_text", "GBP"),
          "gA:sov:trevanion-lusk-merged", "sov",
          "TREVANION & LUSK  -  SCHEDULE OF VALUES  -  Quayside Lofts Management Co Ltd  -  Reinstatement (rebuild est. 2027)\n"
          "PROPERTY        |               |         | CONSTRUCTION / RISK        |          |        | SUMS INSURED £            |            |         |\n"
          "Block | Address | Use | Construction | Storeys | EWS1 | Buildings | Comm. contents | Loss of rent | TIV\n"
          "A | 1-24 Wharf Rd, Gloucester GL1 2EH | 24 flats over 3 shops | former warehouse, brick + timber floors, mansard added 2006 | 6 | B1 | 9,600,000 | 45,000 | 620,000 | 10,265,000\n"
          "B | 25-40 Wharf Rd | 16 flats, gym | concrete frame, render on EPS (remediation 2025) | 5 | A1 | 6,900,000 | 30,000 | 410,000 | 7,340,000\n"
          "C | Wharf Rd car park + bike store | parking | steel/open sided | 1 | n/a | 450,000 | 0 | 0 | 450,000\n"
          "TOTAL |  |  |  |  |  | 16,950,000 | 75,000 | 1,030,000 | 18,055,000")

# --- 42 Brightlowe Programs 100+ habitational/mixed, long
r42 = add("core", C("US", "sheet", "100+", "full_cope", "replacement_cost", "mixed_use", "iso_number", "USD", rows_shown="first 3 of 131"),
          "gA:sov:brightlowe-programs-mga", "sov",
          "BRIGHTLOWE PROGRAMS (MGA) - PROPERTY PROGRAM SOV TEMPLATE v4.2\n"
          "Account: Piedmont Main Street Realty Fund III | 131 bldgs | Val: RC | Account TIV $289,775,000\n"
          "LOC_NO | BLDG_NO | STREET | CITY | STATE | ZIP | OCC_CODE | OCC_DESC | CONST_CODE | YEAR_BUILT | NUM_STORIES | SQFT | SPRINKLER_PCT | ROOF_TYPE | ROOF_YR | PPC | BLDG_VAL | CONT_VAL | BI_VAL | TIV\n"
          "1 | 1 | 1201 Main St | Columbia | SC | 29201 | 412 | Retail / Apt over | 2 | 1915 | 3 | 18,400 | 0 | Mod bit | 2018 | 2 | 3,450,000 | 40,000 | 410,000 | 3,900,000\n"
          "1 | 2 | 1205 Main St | Columbia | SC | 29201 | 412 | Retail / Apt over | 2 | 1915 | 3 | 12,900 | 0 | Mod bit | 2018 | 2 | 2,420,000 | 25,000 | 290,000 | 2,735,000\n"
          "2 | 1 | 85 E Broad St | Athens | GA | 30601 | 420 | Restaurant / Office | 2 | 1902 | 2 | 9,600 | 100 | TPO | 2021 | 3 | 1,980,000 | 60,000 | 240,000 | 2,280,000")


# --- 43 Okonkwo Hale 100+ merged ACV retail no TIV
r43 = add("core", C("US", "sheet", "100+", "messy_merged", "acv", "retail", "words", "USD", no_tiv=True, rows_shown="first 2 of 260"),
          "gA:sov:okonkwo-hale-merged", "sov",
          "OKONKWO HALE ; THRIFTMORE DISCOUNT STORES - 260 STORES - ACV ; "
          "STORE INFO | | | | CONST/PROT | | VALUES ACV | | | ; "
          "STORE | ADDRESS | CITY | ST | CONST | SPRK | BLDG | FIXT/EQUIP | STOCK | TOTAL ; "
          "0001 | 1880 HWY 49 S | FLORENCE | MS | MASONRY | N | 0 | 145,000 | 310,000 | 455,000 ; "
          "0002 | 501 E PASS RD | GULFPORT | MS | METAL BLDG | N | 0 | 160,000 | 335,000 | 495,000")


# --- 44 SPX carrier system export, offices
r44 = add("core", C("US", "sheet", "11-100", "full_cope", "replacement_cost", "office", "iso_number", "USD", carrier_system=True, rows_shown="first 1 of 12"),
          "gA:sov:summit-plains-spx-extract", "sov",
          "SUMMIT PLAINS SPX EXTRACT - SPP-0091744 - Lenape Valley Engineering PC\n"
          "LOC|BLD|ADDR|OCC|CONST|YR|SQFT|SPR|PPC|BLDG_LMT|BPP_LMT|BI_LMT|TIV\n"
          "001|01|300 Market St, Wilmington DE|Office|5|1994|42,000|Y|2|9,100,000|1,450,000|1,200,000|11,750,000")


N_CORE = len(ROWS)

# =====================================================================
# BOUNDARY ROWS
# =====================================================================

# ---- Rule 15: construction schedule of values / pay application (other) x4
add("boundary", C("US", "sheet", "n/a", "construction_sov", "n/a", "construction_project", "n/a", "USD"),
    "gA:sov:b15-gc-continuation-sheet", "other", """
CONTINUATION SHEET - SCHEDULE OF VALUES          Application No.: 6     Period To: 09/30/2027
Project: Cedar Hollow Medical Office Building, 2400 Hartwell Rd, Columbus OH     Contractor: Tallis Ridge Builders Inc.     Retainage: 10%
Item | Description of Work | Scheduled Value | From Previous Application | This Period | Materials Presently Stored | Total Completed & Stored | % | Balance to Finish | Retainage
01 | General Conditions | 412,000 | 220,000 | 41,000 | 0 | 261,000 | 63% | 151,000 | 26,100
02 | Sitework & Utilities | 538,000 | 538,000 | 0 | 0 | 538,000 | 100% | 0 | 53,800
03 | Concrete | 760,000 | 690,000 | 70,000 | 0 | 760,000 | 100% | 0 | 76,000
05 | Structural Steel | 925,000 | 610,000 | 240,000 | 45,000 | 895,000 | 97% | 30,000 | 89,500
07 | Roofing & Waterproofing | 318,000 | 0 | 96,000 | 62,000 | 158,000 | 50% | 160,000 | 15,800
22 | Plumbing | 455,000 | 80,000 | 115,000 | 0 | 195,000 | 43% | 260,000 | 19,500
26 | Electrical | 690,000 | 110,000 | 150,000 | 38,000 | 298,000 | 43% | 392,000 | 29,800
GRAND TOTAL | | 4,098,000 | 2,248,000 | 712,000 | 145,000 | 3,105,000 | 76% | 993,000 | 310,500
""", edge_rule=15)

add("boundary", C("US", "pdf_form", "n/a", "construction_sov", "n/a", "construction_project", "n/a", "USD"),
    "gA:sov:b15-sub-pay-app", "other", """
SUBCONTRACTOR PAY APPLICATION #3 - SCHEDULE OF VALUES
To: Brennock Construction Group (GC)   From: Ventry Mechanical LLC   Job: Riverside Lofts Phase II, 900 Water St, Richmond VA   Period ending 03/31/2028
Line | Trade / Cost Code | Scheduled Value | Previously Billed | This Period | Stored | Total to Date | Balance | Retainage 5%
1 | HVAC equipment | 610,000 | 240,000 | 180,000 | 90,000 | 510,000 | 100,000 | 25,500
2 | Ductwork | 285,000 | 60,000 | 75,000 | 0 | 135,000 | 150,000 | 6,750
3 | Controls | 120,000 | 0 | 20,000 | 0 | 20,000 | 100,000 | 1,000
Total | | 1,015,000 | 300,000 | 275,000 | 90,000 | 665,000 | 350,000 | 33,250
Amount due this application (less retainage and previous payments): $346,750. Lien waiver attached. Notarised.
""", edge_rule=15)

add("boundary", C("UK", "sheet", "n/a", "construction_sov", "n/a", "construction_project", "n/a", "GBP"),
    "gA:sov:b15-uk-interim-valuation", "other",
    "Schedule of Values - Interim Valuation No. 9 - Holmwood Primary School extension, Leicester LE4 - Contractor: Ashcombe Bray Construction Ltd - Valuation date 28/02/2028\n"
    "Ref | Element / trade package | Contract sum £ | Previous valuations £ | This valuation £ | Cumulative £ | % complete | Retention 3% £\n"
    "1 | Preliminaries | 180,000 | 120,000 | 15,000 | 135,000 | 75% | 4,050\n"
    "2 | Substructure | 240,000 | 240,000 | 0 | 240,000 | 100% | 7,200\n"
    "3 | Frame & upper floors | 310,000 | 255,000 | 55,000 | 310,000 | 100% | 9,300\n"
    "4 | Roof | 145,000 | 30,000 | 70,000 | 100,000 | 69% | 3,000\n"
    "5 | M&E services | 420,000 | 60,000 | 95,000 | 155,000 | 37% | 4,650\n"
    "Total | | 1,295,000 | 705,000 | 235,000 | 940,000 | 73% | 28,200", edge_rule=15)

add("boundary", C("US", "sheet", "n/a", "construction_sov", "n/a", "construction_project", "n/a", "USD", tempting="building names and values"),
    "gA:sov:b15-owner-draw-budget", "other",
    "SCHEDULE OF VALUES (Owner draw request #11) | Lender: Fairhaven Community Bank | Project: Oakmere Commons, Bldgs A-C, Durham NC | Borrower: Oakmere Commons Owner LLC ; "
    "Bldg | Line item | Budget | Drawn to date | This draw | Remaining ; "
    "A | Framing | 1,240,000 | 1,240,000 | 0 | 0 ; A | Drywall | 410,000 | 205,000 | 120,000 | 85,000 ; "
    "B | Framing | 1,180,000 | 900,000 | 280,000 | 0 ; B | MEP rough-in | 760,000 | 150,000 | 300,000 | 310,000 ; "
    "C | Foundations | 395,000 | 395,000 | 0 | 0 ; Totals | | 3,985,000 | 2,890,000 | 700,000 | 395,000 ; Inspector sign-off required before release.",
    edge_rule=15)

# ---- Rule 16: London "Schedule of Insured Values" (sov) x3
add("boundary", C("UK", "pdf_form", "2-10", "full_cope", "reinstatement", "warehouse", "words", "GBP", london_market=True),
    "gA:sov:b16-london-siv-slip-appendix", "sov", """
SCHEDULE OF INSURED VALUES
Unique Market Reference: B0917QX28PR0044          Assured: Crossmoor Freight Holdings Ltd          Period: 12 months at 01/06/2028
Basis of Settlement: Reinstatement (Buildings), Replacement (Stock at cost)          Currency: GBP
Location | Address | Occupancy | Construction | Sprinklered | Buildings | Stock | Gross Profit (12m) | Total Sum Insured
1 | Felixstowe Rd, Ipswich IP3 9SJ | Bonded warehouse | Steel portal, LPCB panels | Yes | 14,200,000 | 21,500,000 | 3,300,000 | 39,000,000
2 | Haven Exchange, Felixstowe IP11 3QY | Container freight station | Steel portal, metal clad | No | 6,800,000 | 4,100,000 | 1,600,000 | 12,500,000
3 | Purfleet By-pass, Purfleet RM19 1RP | Distribution | Concrete frame, brick/clad | Yes | 11,950,000 | 9,700,000 | 2,850,000 | 24,500,000
Total |  |  |  |  | 32,950,000 | 35,300,000 | 7,750,000 | 76,000,000
""", edge_rule=16)

add("boundary", C("UK", "sheet", "11-100", "values_only", "reinstatement", "office", "none", "USD", london_market=True, no_tiv=True),
    "gA:sov:b16-london-siv-open-market", "sov",
    "Schedule of Insured Values (USD) - Declarations to Binding Authority B6411BAW2027 - Assured: Harrowgate Lane Capital LLC - Section: Property Damage & BI\n"
    "Loc | Address | State | Building | Contents | BI | Total Insured Values\n"
    "1 | 600 Brickell Ave, Miami | FL | 41,000,000 | 2,500,000 | 6,500,000 | 50,000,000\n"
    "2 | 1 Alhambra Plz, Coral Gables | FL | 18,750,000 | 1,250,000 | 3,000,000 | 23,000,000\n"
    "3 | 2400 E Commercial Blvd, Fort Lauderdale | FL | 12,300,000 | 900,000 | 1,800,000 | 15,000,000\n"
    "... 9 further locations on page 2", edge_rule=16)

add("boundary", C("UK", "sheet", "2-10", "full_cope", "reinstatement", "manufacturing", "words", "EUR", london_market=True),
    "gA:sov:b16-london-siv-facility", "sov",
    "SCHEDULE OF INSURED VALUES ; Facility ref: lineslip LS-2028-117 ; Assured: Brenncastle Chemie GmbH ; values EUR, reinstatement ; "
    "Site | Location | Activity | Construction | Year | Buildings | Machinery & Equipment | Stock | BI (18m) | TSI ; "
    "1 | Ludwigshafen-Rheingoenheim | Speciality coatings | RC frame, steel truss roof | 1978 | 18,400,000 | 31,600,000 | 6,200,000 | 22,800,000 | 79,000,000 ; "
    "2 | Ghent, Port Area | Resin blending | Steel frame, PIR panels | 2011 | 9,900,000 | 14,350,000 | 3,750,000 | 9,000,000 | 37,000,000 ; "
    "Total | | | | | 28,300,000 | 45,950,000 | 9,950,000 | 31,800,000 | 116,000,000", edge_rule=16)

# ---- Rule 17: title says Loss Run / Claims Summary over a location schedule (sov, title_conflict) x4
add("boundary", C("US", "sheet", "2-10", "full_cope", "replacement_cost", "office", "iso_number", "USD", title="LOSS RUN"),
    "gA:sov:b17-misfiled-lossrun-tab", "sov",
    "LOSS RUN\nWestbury Glen Properties LLC\nBldg # | Street | City | Construction | Yr Built | Sq Ft | Building Value | Contents | TIV\n"
    "1 | 4100 Lakeview Pkwy | Rowlett TX | 5 | 2001 | 64,000 | 11,200,000 | 600,000 | 11,800,000\n"
    "2 | 22 Founders Sq | Garland TX | 2 | 1977 | 18,000 | 2,650,000 | 150,000 | 2,800,000\n"
    "3 | 900 N Central Expy | Plano TX | 6 | 2015 | 120,000 | 26,400,000 | 1,100,000 | 27,500,000\n"
    "Total | | | | | | 40,250,000 | 1,850,000 | 42,100,000", edge_rule=17, flags=["title_conflict"])

add("boundary", C("UK", "sheet", "2-10", "full_cope", "reinstatement", "retail", "words", "GBP", title="Claims Summary", no_tiv=True),
    "gA:sov:b17-claims-summary-cover", "sov",
    "CLAIMS SUMMARY - 5 YEARS - Fernleigh Garden Centres Ltd ; "
    "Site | Address | Use | Construction | Buildings £ | Glasshouses £ | Stock £ | Sum Insured £ ; "
    "1 | Pickmere Lane, Knutsford WA16 0JF | Garden centre + cafe | Steel frame, glazed / brick | 2,900,000 | 640,000 | 780,000 | 4,320,000 ; "
    "2 | Wrenbury Rd, Nantwich CW5 7AE | Garden centre | Timber frame, glazed | 1,450,000 | 380,000 | 520,000 | 2,350,000 ; "
    "Total | | | | 4,350,000 | 1,020,000 | 1,300,000 | 6,670,000", edge_rule=17, flags=["title_conflict"])

add("boundary", C("US", "pdf_form", "11-100", "full_cope", "acv", "warehouse", "words", "USD", title="Loss Run Report", rows_shown="first 4 of 13"),
    "gA:sov:b17-carrier-style-header", "sov", """
LOSS RUN REPORT                                     Run Date: 10/02/2027     Page 1 of 2
Insured: Ozark Ridge Feed & Grain Cooperative
Policy: CPP 4410-882-03     Valuation: ACV
Loc | Bldg | Address | Description | Construction | Yr | Sq Ft | Sprinkler | Building | Contents | Stock | TIV
1 | 1 | 100 Elevator Rd, Joplin MO | Grain elevator | Concrete silos | 1958 | 22,000 | No | 2,800,000 | 150,000 | 1,900,000 | 4,850,000
1 | 2 | 100 Elevator Rd, Joplin MO | Feed mill | Steel frame, metal clad | 1985 | 36,000 | No | 3,400,000 | 2,100,000 | 650,000 | 6,150,000
2 | 1 | 4 Depot St, Carthage MO | Farm store | Masonry | 1972 | 12,500 | No | 980,000 | 140,000 | 420,000 | 1,540,000
3 | 1 | 2210 Hwy 71, Neosho MO | Seed warehouse | Pole barn / frame | 1996 | 18,000 | No | 610,000 | 40,000 | 900,000 | 1,550,000
""", edge_rule=17, flags=["title_conflict"])

add("boundary", C("UK", "sheet", "2-10", "values_only", "reinstatement", "hotel", "none", "GBP", title="filename loss runs", no_tiv=True),
    "gA:sov:b17-filename-loss-runs", "sov",
    "File: Loss_Runs_2023-2028_FINAL.xlsx | Sheet: Loss Run\n"
    "Property | Town | Buildings | Contents | BI (24m) | Total Sum Insured\n"
    "The Marlow Arms | Shrewsbury | 3,250,000 | 290,000 | 850,000 | 4,390,000\n"
    "Linden Court Hotel | Ludlow | 5,400,000 | 520,000 | 1,600,000 | 7,520,000\n"
    "Total | | 8,650,000 | 810,000 | 2,450,000 | 11,910,000", edge_rule=17, flags=["title_conflict"])

# =====================================================================
# CONTRAST ROWS (minimal edits of core rows)
# =====================================================================
def core_text(i): return ROWS[i - 1]["text"]
def core_cell(i): return dict(ROWS[i - 1]["attribute_cell"])
def core_group(i): return ROWS[i - 1]["template_group"]
def cid(i): return f"A-sov-{i:03d}"

# P1: row 7 -> broker email mentioning the schedule
add("contrast", dict(core_cell(r7), format="email", edit="table to attachment mention"), core_group(r7), "broker_email",
    "From: Lise Marchand <lmarchand@pinebrookrisk.com>\nTo: property.submissions@caldersgate-us.com\nSubject: Lanternfield Holdings LLC - Values Schedule\n"
    "Hi all, Pinebrook Risk Advisors - Values Schedule for Lanternfield Holdings LLC attached: 2 mixed-use buildings at 212 Main St and 18 Willson Ave, Bozeman MT, "
    "Building, Contents and Rents, Total 5,045,000. Looking for terms by 11/15.\nThanks, Lise",
    parent=cid(r7), pair="P-sov-1")

# P2: row 4 -> construction pay application (retitle and restructure header)
add("contrast", dict(core_cell(r4), format="sheet", edit="retitled to pay application, trades for occupancy"), core_group(r4), "other",
    "HALSTED GREY CONSTRUCTION SERVICES ; Desert Hearth Home Furnishings LLC - store fit-out - Schedule of Values / Pay App #2 - period to 3/1/28 ; "
    "LINE | | | WORK | | | | | BILLING ($) | | | ; "
    "No. | Street | City/St | Trade | Scope | Yr | Sq Ft | Spr | Scheduled Value | Previous | This Period | Total to Date ; "
    "1 | 2210 Mesa Blvd | Tucson AZ | Millwork | Retail fixtures | 2028 | 41,000 | Y | 390,000 | 260,000 | 90,000 | 350,000 ; "
    "2 | 15 Saguaro Plz | Mesa AZ | Electrical | Lighting upgrade | 2028 | 38,400 | Y | 365,000 | 245,000 | 85,000 | 330,000 ; "
    "3 | 8801 N 7th Ave | Phoenix AZ | Flooring | Polished concrete | 2028 | 62,750 | Y | 580,000 | 390,000 | 110,000 | 500,000 ; "
    "4 | 460 Copper Ln | Flagstaff AZ | Sprinkler | New wet system | 2028 | 22,000 | N | 175,000 | 120,000 | 40,000 | 160,000 ; "
    "TOT | | | | | | | | 1,510,000 | 1,015,000 | 325,000 | 1,340,000 ; Retainage 10% withheld",
    parent=cid(r4), pair="P-sov-2")

# P3: row 13 -> valuation report extract (rule 10)
add("contrast", dict(core_cell(r13), format="pdf_report", edit="framed as reinstatement cost assessment report"), core_group(r13), "other",
    "Thistledown Surveyors LLP - Reinstatement Cost Assessment Report\nClient: Pennine Arches Estates Ltd | Inspection dates 12-14/01/2028 | Basis: Reinstatement, Day One uplift 15%\n"
    "1.0 Instructions. We were instructed to assess the reinstatement cost of the properties below for insurance purposes. Our assessed figures, inclusive of professional fees and debris removal, are summarised here; the full building descriptions and our assumptions follow in Sections 2 to 5.\n"
    + "\n".join(core_text(r13).split("\n")[2:]),
    parent=cid(r13), pair="P-sov-3")

# P4: row 1 -> loss run (value columns become claim columns)
add("contrast", dict(core_cell(r1), edit="value columns replaced by claim columns"), core_group(r1), "loss_run",
    "CORVANE PARTNERS LLC - LOSS RUN SUMMARY valued 09/30/2027\nInsured: Redwater Distribution Co. | Policy Term: 07/01/2026 - 07/01/2027 | Property\n"
    "Loc # | Bldg # | Address | City | ST | Zip | Claim # | Date of Loss | Cause | Status | Paid | Reserve | Incurred\n"
    "1 | 1 | 4410 Industrial Pkwy | Fresno | CA | 93725 | RW-26-0114 | 08/19/2026 | Roof leak - stock damage | Closed | $86,400 | $0 | $86,400\n"
    "1 | 2 | 4410 Industrial Pkwy | Fresno | CA | 93725 | RW-26-0187 | 11/02/2026 | Burglary | Closed | $12,750 | $0 | $12,750\n"
    "2 | 1 | 88 Lockwood Rd | Reno | NV | 89502 | RW-27-0021 | 02/11/2027 | Sprinkler leakage | Open | $140,000 | $95,000 | $235,000\n"
    "3 | 1 | 2105 E Commerce Way | Boise | ID | 83716 | RW-27-0060 | 05/28/2027 | Forklift impact, racking | Open | $8,200 | $14,000 | $22,200\n"
    "TOTALS | | | | | | | | | | $247,350 | $109,000 | $356,350",
    parent=cid(r1), pair="P-sov-4")

# P5: row 33 -> carrier indication with premium by location (rule 12)
add("contrast", dict(core_cell(r33), edit="framed as carrier indication with rate and premium"), core_group(r33), "other",
    "GRANITE RIDGE SPECIALTY - PROPERTY INDICATION (not a binder) | Bayou Teche Senior Living Inc | via Marchetti Dunn | RC | valid 30 days\n"
    "Loc | Facility | Address | Occ | ISO Cl | Yr | Sprk | TIV | Rate | Premium\n"
    "1 | Teche Gardens SNF | 400 Main St, New Iberia LA | Skilled nursing | 4 | 1997 | Y | 16,750,000 | 0.210 | 35,175\n"
    "2 | Teche Gardens AL | 402 Main St, New Iberia LA | Assisted living | 1 | 2014 | Y | 10,400,000 | 0.265 | 27,560\n"
    "3 | Cypress Bend Memory Care | 15 Levee Rd, Breaux Bridge LA | Memory care | 2 | 2005 | Y | 5,650,000 | 0.240 | 13,560\n"
    "TOTAL | | | | | | | 32,800,000 | | 76,295\n"
    "Deductibles: $25,000 AOP; 3% named storm. Subjects: signed SOV, 5 yr loss runs, roof survey Loc 1. Terms subject to underwriting review.",
    parent=cid(r33), pair="P-sov-5")

# P6: row 19 -> broker email (prose kept, schedule becomes attachment mention)
add("contrast", dict(core_cell(r19), format="email", edit="cover sheet turned into email, schedule removed"), core_group(r19), "broker_email",
    "From: Hettie Crane <hettie.crane@dunmere-brokers.co.uk>\nTo: churches@wrenfold-underwriting.co.uk\nSubject: St Wendreda, Fenholme - schedule of values\n"
    "Dear Wrenfold team, please find attached the schedule of values for the Parochial Church Council of St Wendreda, Fenholme. Sums insured are on a reinstatement basis using like-for-like traditional materials, as the church is Grade I listed; total sum insured £6,785,000. Renewal is 1 January.\n"
    "Kind regards, Hettie Crane, Dunmere Insurance Brokers Limited",
    parent=cid(r19), pair="P-sov-6")

# P7: row 10 -> ACORD 140 property section (rule 7)
add("contrast", dict(core_cell(r10), format="acord_form", edit="carrier SOV form header and fields recast as ACORD 140"), core_group(r10), "acord",
    "ACORD 140 (2016/03) PROPERTY SECTION\nAPPLICANT: Gullwing Hospitality LLC dba Harborlight Inn & Suites   EFFECTIVE DATE: 06/01/2028\n"
    "PREMISES #: 1  BLDG #: 1  STREET ADDRESS: 9 Ocean View Dr, Myrtle Beach SC 29577  BLDG DESCRIPTION: Hotel - 142 keys, restaurant, outdoor pool\n"
    "SUBJECT OF INSURANCE: Building  AMOUNT: $31,500,000  COINS %: 90  VALUATION: RC  CAUSES OF LOSS: Special  DED: $25,000\n"
    "SUBJECT OF INSURANCE: Business Personal Property  AMOUNT: $4,250,000  VALUATION: RC\nSUBJECT OF INSURANCE: Business Income incl. Rents  AMOUNT: $6,800,000\n"
    "CONSTRUCTION TYPE: Masonry non-combustible  YR BUILT: 1996  # STORIES: 7  TOTAL AREA: 118,000  PROTECTION CLASS: 3  SPRINKLERED: 100%\n"
    "BUILDING IMPROVEMENTS: renov 2021   DISTANCE TO TIDAL WATER: 400 ft   ADDITIONAL INTEREST: [ ] MORTGAGEE",
    parent=cid(r10), pair="P-sov-7")

# P8: row 41 -> UK interim valuation for remediation works (rule 15)
add("contrast", dict(core_cell(r41), format="sheet", edit="sums insured columns replaced by contract and valuation columns"), core_group(r41), "other",
    "TREVANION & LUSK CONTRACTORS  -  SCHEDULE OF VALUES / INTERIM VALUATION No. 4  -  Quayside Lofts Management Co Ltd  -  cladding remediation contract\n"
    "PROPERTY        |               |         | WORKS PACKAGE        |          |        | VALUATION £            |            |         |\n"
    "Block | Address | Use | Package | Storeys | EWS1 | Contract sum | Previous | This valuation | Cumulative\n"
    "A | 1-24 Wharf Rd, Gloucester GL1 2EH | 24 flats over 3 shops | scaffold + mansard fire breaks | 6 | B1 | 420,000 | 210,000 | 95,000 | 305,000\n"
    "B | 25-40 Wharf Rd | 16 flats, gym | strip EPS render, install mineral wool system | 5 | A1 | 1,150,000 | 640,000 | 260,000 | 900,000\n"
    "C | Wharf Rd car park + bike store | parking | site compound | 1 | n/a | 35,000 | 35,000 | 0 | 35,000\n"
    "TOTAL |  |  |  |  |  | 1,605,000 | 885,000 | 355,000 | 1,240,000\nRetention 5%. Payment due 14 days from certificate.",
    parent=cid(r41), pair="P-sov-8")

# =====================================================================
def words(t): return len(re.findall(r"[A-Za-z0-9£$€][^\s|;]*", t))
def length_band(w): return "short" if w <= 40 else ("medium" if w <= 120 else "long")

with open(OUT, "w", encoding="utf-8") as f:
    for i, r in enumerate(ROWS, 1):
        w = words(r["text"])
        cell = dict(r["attribute_cell"])
        cell["length"] = length_band(w)
        cell["tiv_token"] = "TIV" in r["text"]
        cell.pop("no_tiv", None)
        obj = {
            "id": f"A-sov-{i:03d}",
            "slice": r["slice"],
            "generator": "claude-opus-5.5",
            "generator_family": "A",
            "prompt_id": "a-sov-v1",
            "attribute_cell": cell,
            "template_group": r["template_group"],
            "generator_label": r["generator_label"],
            "edge_rule": r["edge_rule"],
            "expected_flags": r["expected_flags"],
            "parent_id": r["parent_id"],
            "pair_id": r["pair_id"],
            "text": r["text"],
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
print(len(ROWS), "rows;", N_CORE, "core")
