# Boundary rows: (key, rule, label, attrs, text)
BOUNDARY = []

def add(key, rule, label, attrs, text):
    BOUNDARY.append((key, rule, label, attrs, text.strip("\n")))

# ---- rule 1: body only lists attachments
add("ferrier_lowe", 1, "broker_email", dict(market="UK", sender_type="retail_broker", purpose="renewal", header_style="outlook", tone="terse", length="short"), """
From: Nadia Okwuosa <n.okwuosa@ferrierlowe.co.uk>
Sent: 03 November 2026 07:58
To: Care Sector Team <care@cobaltline-specialty.co.uk>
Subject: Fwd: Thistledown Care Homes - renewal 01/01/27

Hi team, SOV, 5 yr loss runs and the ACORD 125 attached for Thistledown. Thanks
""")

add("elmstead_wholesale", 1, "broker_email", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="neutral", length="short"), """
From: Darius Fenn <dfenn@elmsteadwholesale.com>
To: Property Submissions <property@halberdcasualty.com>
Sent: Fri 10/23/2026 3:14 PM
Subject: New - Coldwater Creek Apartments - 1/1/27

Attached for your review:
- SOV (4 buildings)
- Loss runs, 5 years, currently valued
- ACORD 125 and ACORD 140
- Photos

Regards,
Darius
""")

add("juniper_coast_agency", 1, "broker_email", dict(market="US", sender_type="retail_agent", purpose="new_business", header_style="gmail", tone="terse", length="short", avoids_cue_words=True), """
Inez Calderwood <inez@junipercoast.com>
Oct 27, 2026, 11:36 AM
to me

Seabright Seafood Processors, eff 12/1.

SOV.xlsx
LossRuns_2021-2026.pdf
ACORD125_signed.pdf
ACORD140.pdf

Inez
""")

add("whitlock_brokers", 1, "broker_email", dict(market="UK", sender_type="retail_broker", purpose="new_business", header_style="none", tone="formal", length="short", no_from_line=True), """
Subject: Quarterhouse Printworks Ltd - new enquiry

Dear Sir or Madam,

Please find enclosed in respect of the above: schedule of values (SOV), loss runs from the current insurer for five years, and a completed ACORD 125 commercial application.

Yours faithfully,
Edwin Marchbank
Whitlock Insurance Brokers Ltd, Norwich
""")

# ---- rule 2: short inline loss summary
add("brackenridge_insurance", 2, "broker_email", dict(market="US", sender_type="retail_agent", purpose="new_business", header_style="outlook", tone="neutral", length="medium"), """
From: Corinne Abara <cabara@brackenridgeins.com>
Sent: Tuesday, October 6, 2026 10:50 AM
To: Package Underwriting <package@westvaleins.com>
Subject: New business - Driftwood Coffee Roasters - BOP - 11/15/2026

Hi,

Driftwood Coffee Roasters, Bend, Oregon. Leased 6,800 sq ft unit, roasting plus a small cafe, revenue $1.7M. BPP $380k, equipment $510k (two drum roasters with afterburners). Looking for a BOP with equipment breakdown and spoilage.

Losses: 2022 $14,200 water damage (closed), 2024 $3,150 theft (closed). Otherwise clean.

Target is $9k. Effective 11/15.

Corinne Abara
Brackenridge Insurance | Bend, OR
""")

add("harlow_penrose", 2, "broker_email", dict(market="UK", sender_type="retail_broker", purpose="renewal", header_style="outlook", tone="neutral", length="medium"), """
From: Alastair Penrose <a.penrose@harlowpenrose.co.uk>
Sent: 09 November 2026 13:02
To: Rachel Odum <rachel.odum@stonecrop-europe.co.uk>
Subject: Renewal terms please - Fellside Outdoor Centre - 01/01/2027

Hi Rachel,

Fellside Outdoor Centre renews on 1 January. Activities unchanged (climbing wall, gorge walking, kayaking), 46,000 visitor days last year, turnover GBP 1.9m. Buildings sum insured GBP 2.6m.

Claims: three in five years totalling GBP 27,400 paid, none open, all minor injury claims under the public liability section.

Client would like to keep the GBP 500 excess. Could you let me have terms by 4 December.

Thanks,
Alastair
Harlow Penrose Insurance Brokers, Kendal
""")

add("mesa_verde_risk", 2, "broker_email", dict(market="US", sender_type="mga", purpose="chasing_quote", header_style="on_wrote_reply", tone="neutral", length="medium"), """
Subject: Re: Saguaro Ridge Shopping Center - GL quote

Paolo,

Following up on the quote. To answer your question from last week: one GL slip-and-fall in 2023 at the food court, $48,500 incurred ($40,000 paid, $8,500 reserve), still open; nothing else in five years.

We need terms by Thursday, the retailer presents Monday.

Lorna Vickery
Mesa Verde Risk Underwriters | Scottsdale, AZ

On Wed, Oct 21, 2026 at 2:44 PM Paolo Brenner <pbrenner@ferrousindemnity.com> wrote:
> Lorna, any claims I should know about before I price this?
""")

add("caskwell_dane", 2, "broker_email", dict(market="UK", sender_type="retail_broker", purpose="new_business", header_style="none", tone="terse", length="short", no_from_line=True, avoids_cue_words=True), """
Afternoon Nkechi,

New one for you: Brockhurst Garden Centre, Hampshire, materials damage GBP 3.2m, BI GBP 900k, start 01/02/27. Claims 21/22 nil, 22/23 GBP 4,100, 23/24 nil, 24/25 GBP 11,800 (escape of water), 25/26 nil. Terms by 15/01 please.

Gareth Lyle-Ames
Caskwell & Dane
""")

# ---- rule 3: body is mostly a pasted table with defining columns
add("orchard_lane_agency", 3, "sov", dict(market="US", sender_type="retail_agent", purpose="new_business", header_style="gmail", tone="terse", length="medium", table="sov"), """
From: Bram Kessler <bram@orchardlaneagency.com>
To: submissions@sundialbrokerage.com
Subject: Hollowell Self Storage - values

Clare, client could not send the spreadsheet so I pasted it:

Loc # | Address | City | ST | Occupancy | Construction | Yr Built | Sq Ft | Sprinklered | Bldg Value | Contents | BI | TIV
1 | 4100 Gulf Breeze Pkwy | Gulf Breeze | FL | Self storage | Masonry non-comb | 2004 | 58,200 | N | 4,350,000 | 25,000 | 310,000 | 4,685,000
2 | 22 Industrial Blvd | Crestview | FL | Self storage | Metal (non-comb) | 2011 | 41,000 | N | 2,900,000 | 15,000 | 220,000 | 3,135,000
3 | 7810 Hwy 98 | Navarre | FL | Self storage + office | JM | 1999 | 36,400 | N | 2,150,000 | 40,000 | 175,000 | 2,365,000
4 | 515 Main St | Milton | FL | Self storage | Masonry non-comb | 2017 | 63,900 | Y | 5,600,000 | 30,000 | 400,000 | 6,030,000
TOTAL | | | | | | | 199,500 | | 15,000,000 | 110,000 | 1,105,000 | 16,215,000

Bram
""")

add("holloway_thorne", 3, "sov", dict(market="UK", sender_type="london_broker", purpose="renewal", header_style="outlook", tone="neutral", length="long", table="sov"), """
From: Saskia Holloway <s.holloway@hollowaythorne.co.uk>
Sent: 12 October 2026 15:30
To: Arran Doig <a.doig@halberdmanaging.co.uk>
Subject: Renewal values - Greyling Estates Ltd

Arran, schedule for 2027 below as requested.

SCHEDULE OF INSURED VALUES - GREYLING ESTATES LTD - Valuation basis: reinstatement, day one
Site | Address | Postcode | Occupancy | Construction | Storeys | Year | Floor area m2 | Sprinklers | Buildings GBP | Contents GBP | Loss of rent GBP | Total GBP
01 | 4 Wellgate | DD1 2DW | Retail ground, offices over | Sandstone, slate roof | 4 | 1890 | 1,840 | No | 3,950,000 | 120,000 | 410,000 | 4,480,000
02 | 17-21 Mercer Row | NE1 4AP | Offices | Steel frame, glazed curtain wall | 6 | 2007 | 5,210 | Yes | 14,800,000 | 350,000 | 1,320,000 | 16,470,000
03 | Unit 3 Kelvin Park | G20 0QQ | Warehouse / trade counter | Steel portal, comp. panel | 1 | 1998 | 3,900 | No | 3,100,000 | 60,000 | 290,000 | 3,450,000
04 | 88 Bridge St | CH1 1NQ | Retail | Brick, timber floors | 3 | 1912 | 960 | No | 2,250,000 | 45,000 | 215,000 | 2,510,000
05 | The Maltings | YO1 9WR | Residential (24 flats) | Brick, concrete floors | 5 | 2015 | 2,700 | Yes | 6,900,000 | 30,000 | 560,000 | 7,490,000
Totals | | | | | | | 14,610 | | 31,000,000 | 605,000 | 2,795,000 | 34,400,000

Saskia
""")

add("pinecrest_wholesale", 3, "sov", dict(market="US", sender_type="wholesale_broker", purpose="endorsement", header_style="outlook", tone="terse", length="medium", table="sov", mess="ocr_and_caps"), """
From: R. Abernathy-Cole <rac@pinecrestwholesale.com>
To: Ferrous Indemnity Policy Svcs
Subject: FW: updated schedule - Tri-County Church Fellowship

pls update policy to the schedule below eff 3/1

LOC | BLDG | ADDRESS | OCCUP | CONST (ISO) | YR BLT | SQ FT | PROT CL | SPRK | BLDG $ | BPP $ | TIV
1 | 1 | 300 Old Mill Rd, Lexington KY | House of worship | 2 - JM | 1972 | 18,400 | 4 | N | 3,800,000 | 450,000 | 4,250,000
1 | 2 | 300 Old Mill Rd, Lexington KY | Fellowship hall / kitchen | 1 - Frame | 1985 | 6,200 | 4 | N | 1,150,000 | 120,000 | 1,270,000
2 | 1 | 41 Church St, Paris KY | House of worship | 4 - MNC | 2003 | 11,000 | 5 | Y | 2,600,000 | 300,000 | 2,9OO,000
3 | 1 | 1201 Bypass Rd, Winchester KY | Daycare / classrooms | 3 - Non-comb | 2010 | 7,800 | 6 | N | 1,400,000 | 180,000 | 1,580,000
TOTAL | | | | | | 43,400 | | | 8,950,000 | 1,050,000 | 10,000,000
""")

add("abernethy_risk", 3, "loss_run", dict(market="UK", sender_type="retail_broker", purpose="new_business", header_style="outlook", tone="neutral", length="medium", table="loss_run"), """
From: Morag Fairlie <morag@abernethyrisk.co.uk>
Sent: 20 October 2026 09:12
To: Kirsty Baird <k.baird@cobaltline-specialty.co.uk>
Subject: Claims for Lochside Haulage Ltd

Kirsty, insurer's claims listing pasted below, valued 30/09/2026.

Policy year | Claim ref | Date of loss | Description | Paid GBP | Outstanding GBP | Incurred GBP | Status
2021/22 | LHL-0417 | 14/03/2022 | Vehicle fire, depot yard | 38,200 | 0 | 38,200 | Closed
2022/23 | LHL-0533 | 02/11/2022 | Theft of goods in transit | 12,650 | 0 | 12,650 | Closed
2023/24 | LHL-0609 | 21/07/2023 | Roof damage, storm | 7,480 | 0 | 7,480 | Closed
2024/25 | LHL-0718 | 09/01/2025 | Employee injury, loading bay | 4,000 | 21,000 | 25,000 | Open
2025/26 | - | - | No claims | 0 | 0 | 0 | -
Total | | | | 62,330 | 21,000 | 83,330 |
""")

add("lakemont_brokerage", 3, "loss_run", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="terse", length="long", table="loss_run"), """
From: Jonah Whitley <jwhitley@lakemontbrokerage.com>
Sent: Monday, November 2, 2026 9:47 AM
To: Casualty UW <casualty@oldweirus.com>
Subject: Bayline Restaurants Group - GL loss history

Carrier loss runs below, pasted from the portal since the PDF will not export.

COMMERCIAL GENERAL LIABILITY LOSS RUN - Insured: Bayline Restaurants Group Inc - Valued as of 10/15/2026
Policy Period | Claim No | Date of Loss | Claimant / Description | Paid Indemnity | Paid Expense | Reserve | Total Incurred | Status
11/01/21-22 | GL21-88412 | 02/19/2022 | Patron slip on wet floor | 18,500 | 4,200 | 0 | 22,700 | C
11/01/21-22 | GL21-89030 | 06/03/2022 | Foodborne illness allegation | 0 | 2,950 | 0 | 2,950 | C
11/01/22-23 | GL22-90155 | 12/10/2022 | Burn from hot plate | 9,800 | 1,600 | 0 | 11,400 | C
11/01/23-24 | GL23-91877 | 08/27/2024 | Parking lot trip and fall | 30,000 | 8,400 | 26,600 | 65,000 | O
11/01/24-25 | - | - | No losses reported | 0 | 0 | 0 | 0 | -
11/01/25-26 | GL25-93301 | 04/12/2026 | Broken chair, back injury | 0 | 1,250 | 13,750 | 15,000 | O
Totals | 3 closed / 2 open | | | 58,300 | 18,400 | 40,350 | 117,050 |

Jonah
""")

# ---- rule 4: forwarded chain with "pls see below"
add("ironbridge_wholesale", 4, "broker_email", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="forwarded_original_message", tone="terse", length="medium"), """
From: Teresa Lindqvist <tlindqvist@ironbridgewholesale.com>
Sent: Tuesday, November 10, 2026 8:03 AM
To: Inland Marine UW <im@halberdcasualty.com>
Subject: FW: Contractor's equipment - Delgado Earthworks

pls see below

-----Original Message-----
From: Ruben Salcido <ruben@pecanhollowins.com>
Sent: Monday, November 9, 2026 5:40 PM
To: Teresa Lindqvist
Subject: Contractor's equipment - Delgado Earthworks

Teresa, looking for a home for Delgado Earthworks' equipment floater. 31 scheduled units, total $4.9M, largest is a 2022 excavator at $610k. Effective 12/15. Current carrier is raising the deductible to $25k and they want $5k. Equipment schedule and 5 years of losses enclosed. Thanks, Ruben
""")

add("silverlake_es", 4, "broker_email", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="forwarded_gmail", tone="terse", length="medium"), """
pls see below - vacant building, need a market quick

---------- Forwarded message ---------
From: Annika Strand <astrand@bayfogins.com>
Date: Thu, Oct 29, 2026 at 4:12 PM
Subject: Vacant warehouse Oakland
To: Nadia Farouk <nfarouk@silverlake-es.com>

Hi Nadia, client owns a vacant 40,000 sq ft tilt-up warehouse at 2900 Peralta St, Oakland. Building value $5.8M, vacant since August, tenant search ongoing. Needs property and GL from 11/15. Fenced, monitored alarm, weekly inspections. Photos and SOV attached.

Annika Strand
Bayfog Insurance Services
""")

add("calloway_excess", 4, "broker_email", dict(market="US", sender_type="wholesale_broker", purpose="renewal", header_style="forwarded_original_message", tone="neutral", length="long"), """
From: Ethan Okonkwo <eokonkwo@callowayexcess.com>
Sent: Wednesday, September 9, 2026 10:30 AM
To: Hugo Pellegrini <hpellegrini@oldweirus.com>
Subject: FW: Renewal - Blue Ridge Timber Products

Hugo, pls see below. Same structure as last year, want to give you first look.

-----Original Message-----
From: Wendy Haverford <whaverford@yadkinbendins.com>
Sent: Tuesday, September 8, 2026 4:55 PM
To: Ethan Okonkwo <eokonkwo@callowayexcess.com>
Subject: Renewal - Blue Ridge Timber Products

Ethan,

Blue Ridge Timber Products renews 11/1. Sawmill and planing mill in Wilkesboro NC, plus a dry kiln building added in May (steel, non-comb, $1.9M). Total values now $16.3M including BI.

They spent $240k on a spark detection and extinguishing system for the dust collectors this spring, which I hope helps with pricing. One small kiln fire in 2025, about $22k, closed.

Expiring premium $298,000. Owner would like options with a $50k deductible as well as the current $25k.

Updated SOV, loss runs and the spark detection invoice are enclosed. If you can have terms back by 10/9 that gives us time to review with them.

Thanks,
Wendy Haverford
Yadkin Bend Insurance Associates
""")

add("halcyon_ridge_brokers", 4, "broker_email", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="forwarded_gmail", tone="terse", length="short", avoids_cue_words=True), """
From: Yusuf Demir <ydemir@halcyonridge.com>
To: Hugo Pellegrini
Subject: FW: mixed use bldg Queens

pls see below

> From: Lionel Batista <lbatista@ditmarsagency.com>
> Sent: Monday, November 16, 2026
> Mixed use, 4 stories, 2 retail + 12 apts, Astoria NY, TIV $7.1M, eff 1/1. Need property and GL. Apps to follow.
""")

# ---- rule 16: London email quoting a UMR
add("penhallow_risk_partners", 16, "broker_email", dict(market="UK", sender_type="london_broker", purpose="endorsement", header_style="outlook", tone="formal", length="medium"), """
From: Declan Moss <d.moss@penhallowrisk.co.uk>
Sent: 18 January 2027 10:14
To: Property Open Market <property.submissions@cobaltline-specialty.co.uk>
Subject: UMR B0742PRP2611903 - Pellinore Cold Storage Ltd - additional location

Dear Underwriter,

Under UMR B0742PRP2611903 we request an endorsement to add the insured's newly acquired site at Unit 4, Fenland Way, Wisbech PE13 2RQ with effect from 1 February 2027. Declared values: buildings GBP 3.4m, stock GBP 1.1m. The site is sprinklered and monitored.

Please confirm your agreement and the additional premium. A revised schedule is enclosed.

Kind regards,
Declan Moss
Penhallow Risk Partners Ltd
""")

add("pemberton_lyle", 16, "broker_email", dict(market="UK", sender_type="london_broker", purpose="bind_request", header_style="outlook", tone="formal", length="short"), """
From: Imogen Thrale
Sent: 22 December 2026 14:06
To: Felix Danvers
Subject: Sorrel Agri-Foods - firm order - UMR B1188PL26SAF001

Felix, we have firm order from the client. Please stamp your 30% line on the slip under UMR B1188PL26SAF001 at the agreed terms, inception 31/12/2026.

Imogen Thrale | Pemberton Lyle Ltd
""")

add("varga_hollins", 16, "broker_email", dict(market="UK", sender_type="london_broker", purpose="chasing_quote", header_style="on_wrote_reply", tone="neutral", length="medium"), """
Subject: RE: UMR B0612VH2601MMC - Meridale Mining - EQ sublimit

Dolores,

Thank you for the quote. Before we take it to the client, could you confirm whether your terms for the USD 100m earthquake sublimit under UMR B0612VH2601MMC assume the old or the revised seismic study? The leader has indicated a 10% reduction on the EQ rate on the revised study.

We need to revert to the client by 20 November.

Arjun Mehta
Varga Hollins LLP

On 12 Nov 2026, at 09:30, Dolores Kwan <d.kwan@cobaltline-specialty.co.uk> wrote:
> Arjun, terms enclosed for our 12.5% line.
""")
