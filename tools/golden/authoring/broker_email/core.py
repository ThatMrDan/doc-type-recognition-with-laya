# Core broker_email rows: (key, attrs, text)
CORE = []

def add(key, attrs, text):
    CORE.append((key, attrs, text.strip("\n")))

# 1
add("penhallow_risk_partners", dict(market="UK", sender_type="london_broker", purpose="new_business", header_style="outlook", tone="formal", length="medium"), """
From: Harriet Okafor <h.okafor@penhallowrisk.co.uk>
Sent: 14 October 2026 09:42
To: Property Open Market <property.submissions@cobaltline-specialty.co.uk>
Cc: Declan Moss <d.moss@penhallowrisk.co.uk>
Subject: New business - Pellinore Cold Storage Ltd - PD/BI - 01/12/2026

Dear Underwriter,

We are pleased to present Pellinore Cold Storage Ltd for property damage and business interruption, inception 1 December 2026 for 12 months.

The insured operates five temperature-controlled warehouses across the East Midlands. Combined declared values are GBP 48.6m (buildings GBP 31.2m, stock and machinery GBP 11.9m, gross profit GBP 5.5m, 18 month indemnity period). All sites are sprinklered and alarmed to a central station.

Expiring premium is GBP 61,250 plus IPT with a composite market that is withdrawing from cold store risks. We are looking for a lead line at or around expiring.

Enclosed you will find the schedule of values, five years of claims experience and the 2025 risk survey. An indication by 6 November would be appreciated.

Kind regards,

Harriet Okafor
Account Executive, Property
Penhallow Risk Partners Ltd
4th Floor, 22 Mincing Row, London EC3R 7AW
T +44 20 7946 0318

Penhallow Risk Partners Ltd is authorised and regulated by the Financial Conduct Authority. This email and any attachments are confidential and intended solely for the addressee.
""")

# 2
add("penhallow_risk_partners", dict(market="UK", sender_type="london_broker", purpose="renewal", header_style="none", tone="terse", length="short", no_from_line=True, avoids_cue_words=True), """
Morning both,

Pellinore renewal. Values up 4% on index, no change to locations, same deductible. Pls can you hold the line at expiring. Need terms by 20 Nov.

Declan Moss
Penhallow Risk Partners
+44 20 7946 0322
""")

# 3
add("strathmore_quill", dict(market="UK", sender_type="london_broker", purpose="endorsement", header_style="on_wrote_reply", tone="formal", length="medium"), """
Subject: RE: Harrowgate Marine Logistics - mid-term adjustment

Hi Moira,

Thanks for confirming the cover note. The insured has now signed the lease on an additional unit at Unit 9, Tilbury Riverside Park, RM18 7HX, used for bonded storage of packaged spirits. Declared value GBP 2,400,000 stock, building is the landlord's responsibility.

Could you please endorse the policy to add the location from 1 November 2026 and let me have the additional premium pro rata.

Many thanks,
Callum Reid
Strathmore & Quill (Insurance Brokers) LLP

On Tue, 13 Oct 2026 at 16:05, Moira Lennox <m.lennox@oldweir.co.uk> wrote:
> Callum, cover note attached for your records. Shout if anything else is needed.
""")

# 4
add("strathmore_quill", dict(market="UK", sender_type="london_broker", purpose="bind_request", header_style="outlook", tone="formal", length="short"), """
From: Callum Reid
To: Moira Lennox
Subject: Harrowgate Marine Logistics - firm order

Moira, client instructs us to bind as quoted 21 October, GBP 38,400 plus IPT, inception 1 November 2026. Please confirm.

Callum Reid | Strathmore & Quill
""")

# 5
add("corvid_specialty_brokerage", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="neutral", length="medium"), """
From: Marisol Vega <mvega@corvidspecialty.com>
Sent: Wednesday, October 14, 2026 2:31 PM
To: E&S Property Submissions <esproperty@stonecropspecialty.com>
Subject: NEW SUBMISSION // Delacroix Hospitality Group // eff 12/15/2026

Good afternoon,

Submitting Delacroix Hospitality Group on behalf of our retail agent in Baton Rouge. Three limited-service hotels in Louisiana, all frame and joisted masonry, built 1998 to 2006. TIV $27,850,000. Named storm is required; insured will accept a 5% wind deductible.

Effective 12/15/2026. Target premium $410,000 all in. Incumbent is non-renewing on wind.

Included: SOV, 5 yr loss runs, ACORD 125/140, and the most recent roof inspection reports.

Need indication by 11/20 please.

Marisol Vega
Senior Property Broker | Corvid Specialty Brokerage
Direct 504-555-0187
""")

# 6
add("corvid_specialty_brokerage", dict(market="US", sender_type="wholesale_broker", purpose="chasing_quote", header_style="gmail", tone="terse", length="short"), """
Marisol Vega <mvega@corvidspecialty.com>
to esproperty
Nov 18, 2026, 9:04 AM

Any update on Delacroix? Retailer meeting the client Fri. Even a range would help.
""")

# 7
add("corvid_specialty_brokerage", dict(market="US", sender_type="wholesale_broker", purpose="answering_subjectivities", header_style="outlook", tone="neutral", length="medium"), """
From: Gideon Platt <gplatt@corvidspecialty.com>
To: Hannah Pruett <hpruett@stonecropspecialty.com>
Sent: Mon 12/7/2026 10:12 AM
Subject: RE: Delacroix Hospitality - bind subjectivities

Hannah,

Responses to the open items from your quote:

1. Signed and dated SOV - enclosed, signed by the CFO 12/4.
2. Confirmation of central station fire alarm at all three locations - certificates from the monitoring company included.
3. Roof age at Loc 2 - replaced 2019, invoice enclosed.
4. Surplus lines filing info - we are the filing agent, LA license 774512.

That should clear everything for the 12/15 inception. Let me know if you need anything else.

Gideon Platt
Corvid Specialty Brokerage
""")

# 8
add("bellwether_underwriting_managers", dict(market="US", sender_type="mga", purpose="bind_request", header_style="outlook", tone="formal", length="medium"), """
From: Wendell Haynes <whaynes@bellwetherum.com>
Sent: Thursday, October 22, 2026 4:48 PM
To: Binding Desk <binding@ferrousindemnity.com>
Cc: Lucia Brandt <lbrandt@bellwetherum.com>
Subject: Request to bind - Quillon Self Storage Partners LP - Policy BWM-PR-2611042

Dear Binding Desk,

Please bind coverage for Quillon Self Storage Partners LP under our property facility, effective November 1, 2026, per the attached quote and the terms below:

Limit: $18,500,000 blanket, building and business income
AOP deductible: $25,000; wind/hail 2% per building, $100,000 minimum
Premium: $96,750 plus fees and surplus lines tax

All subjectivities have been received and are on file. The insured has 14 storage facilities in Texas and Oklahoma.

Sincerely,

Wendell Haynes
Program Underwriter
Bellwether Underwriting Managers, LLC
1200 Commerce Street, Suite 800, Dallas, TX 75202
""")

# 9
add("bellwether_underwriting_managers", dict(market="US", sender_type="mga", purpose="endorsement", header_style="outlook", tone="formal", length="long"), """
From: Lucia Brandt <lbrandt@bellwetherum.com>
Sent: Tuesday, March 9, 2027 9:15 AM
To: Policy Services <policyservices@ferrousindemnity.com>
Subject: Endorsement request - Quillon Self Storage Partners LP - BWM-PR-2611042 - add 2 locations, delete 1

Good morning,

On behalf of the insured we are requesting the following changes to the above policy, effective March 15, 2027:

Add Location 15: 4410 Ranch Road 620, Austin, TX 78732. Non-combustible single story storage, built 2021, 61,000 sq ft, building value $5,200,000, business income $380,000.

Add Location 16: 902 N Classen Blvd, Oklahoma City, OK 73106. Masonry non-combustible, built 2015, 48,500 sq ft, building value $3,950,000, business income $290,000.

Delete Location 6: 17 Industrial Loop, Lawton, OK. Sold to an unrelated party, closing date March 12, 2027.

Revised blanket limit would be $24,890,000. Please advise the additional premium and issue the endorsement. Both new sites have monitored burglar alarms and gated access; neither is sprinklered, which is consistent with the rest of the schedule.

The updated statement of values and closing statement for Lawton are enclosed for your file.

Thank you,

Lucia Brandt
Account Manager
Bellwether Underwriting Managers, LLC
T 214-555-0143

CONFIDENTIALITY NOTICE: This e-mail message, including any attachments, is for the sole use of the intended recipient(s) and may contain confidential and privileged information. Any unauthorized review, use, disclosure or distribution is prohibited. If you are not the intended recipient, please contact the sender by reply e-mail and destroy all copies of the original message.
""")

# 10
add("dunmore_coverholder_services", dict(market="UK", sender_type="coverholder", purpose="new_business", header_style="outlook", tone="formal", length="medium"), """
From: Siobhan Keane <skeane@dunmorecs.co.uk>
Sent: 19 October 2026 14:20
To: Referrals - Syndicate 6218 <referrals6218@halberdmanaging.co.uk>
Subject: Referral outside authority - Kittiwake Leisure Parks Ltd

Good afternoon,

We would like to refer the following risk, which sits outside our binding authority on sum insured.

Insured: Kittiwake Leisure Parks Ltd
Business: Holiday park operator, 3 sites in Cornwall and Devon
Sum insured: GBP 14.3m buildings and contents, plus GBP 2.1m loss of revenue
Inception: 1 January 2027
Claims: two escape of water claims in the last five years, total GBP 41k

Our proposed rate is 0.165% giving a premium of GBP 27,060. Proposal form and site schedule enclosed.

Agreement by 30 November please.

Best wishes,
Siobhan Keane
Senior Underwriter, Dunmore Coverholder Services Ltd
""")

# 11
add("dunmore_coverholder_services", dict(market="UK", sender_type="coverholder", purpose="chasing_quote", header_style="none", tone="terse", length="short", no_from_line=True, avoids_cue_words=True), """
Hi, just nudging on the Kittiwake referral sent 19/10. Broker is pushing us for a decision this week.

Siobhan
Dunmore CS
""")

# 12
add("tidewater_agency_group", dict(market="US", sender_type="retail_agent", purpose="new_business", header_style="gmail", tone="casual", length="medium"), """
From: Owen Tregarthen <owen@tidewateragency.com>
Date: Mon, Oct 12, 2026 at 3:47 PM
Subject: New biz - Brightwater Marina & Boatyard
To: Teresa Lindqvist <tlindqvist@ironbridgewholesale.com>

Hi Teresa,

Got a good one for you. Brightwater Marina & Boatyard in Hampton, VA. Owner has been with the same carrier 11 years and they just non-renewed for coastal exposure. Two buildings plus dry stack storage, about $6.4M TIV. They also want GL and marina operators legal liability.

Eff date 1/1/27. Client is currently paying around $88k and would love to stay under $110k.

SOV and loss runs attached, ACORD 125 and 140 to follow tomorrow.

Thanks!
Owen

Owen Tregarthen, CIC
Tidewater Agency Group | Hampton, VA
757-555-0164
""")

# 13
add("tidewater_agency_group", dict(market="US", sender_type="retail_agent", purpose="chasing_quote", header_style="gmail", tone="terse", length="short"), """
Owen Tregarthen <owen@tidewateragency.com>
Wed, Dec 2, 2026, 8:12 AM
to Teresa

Teresa - where are we on Brightwater? Client asked again yesterday. 1/1 is close.
""")

# 14
add("hollis_mercer_insurance", dict(market="US", sender_type="retail_agent", purpose="renewal", header_style="outlook", tone="formal", length="long"), """
From: Desmond Liu <dliu@hollismercer.com>
Sent: Friday, September 25, 2026 11:03 AM
To: Clare Whitford <cwhitford@sundialbrokerage.com>
Cc: Kofi Mensah <kmensah@hollismercer.com>
Subject: Renewal submission - Arkwright Precision Castings, Inc. - Property & GL - 12/1/2026

Clare,

Please find the renewal submission for Arkwright Precision Castings, Inc., Dayton, Ohio. They have been our client since 2014 and have had excellent experience with the current program.

Account summary:
- Operations: investment casting of aerospace and medical components, two plants
- Plant 1: 2250 Webster St, Dayton OH, 112,000 sq ft, masonry non-combustible, fully sprinklered, built 1987
- Plant 2: 61 Progress Dr, Miamisburg OH, 54,000 sq ft, non-combustible, sprinklered, built 2009
- Property TIV: $41,700,000 (building, contents, business income with extra expense)
- Revenue: $68M, payroll $21.4M, 240 employees

Coverage requested: property all risk with equipment breakdown, $10M flood sublimit; GL $1M/$2M with products-completed operations.

Expiring premium $214,600 property, $47,900 GL. The client would like to see options at $10k and $25k AOP deductibles. One furnace breakdown claim in 2024 ($62,000, closed); otherwise clean.

Our marketing deadline is October 30 so that we can present by November 10.

Thank you for your help on this one.

Desmond Liu, CPCU
Vice President, Commercial Lines
Hollis Mercer Insurance Agency
400 E Third Street, Dayton, OH 45402
Phone 937-555-0110

The information contained in this message is confidential and may be legally privileged. It is intended only for the use of the recipient named above. If you have received this message in error, please notify the sender immediately and delete it. Hollis Mercer Insurance Agency cannot bind or alter coverage by e-mail without written confirmation from an authorized representative.
""")

# 15
add("hollis_mercer_insurance", dict(market="US", sender_type="retail_agent", purpose="answering_subjectivities", header_style="outlook", tone="neutral", length="short"), """
From: Kofi Mensah
To: Clare Whitford
Subject: RE: Arkwright - quote conditions

Clare, signed no-flood-loss warranty and the sprinkler inspection report for Plant 2 are enclosed. Still waiting on the boiler cert, should have it Monday.

Kofi
""")

# 16
add("ironbridge_wholesale", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="neutral", length="long"), """
From: Teresa Lindqvist <tlindqvist@ironbridgewholesale.com>
Sent: Thursday, October 15, 2026 10:26 AM
To: Coastal Property <coastal.uw@halberdcasualty.com>
Subject: Submission: Brightwater Marina & Boatyard LLC, Hampton VA | Property + GL + MOLL | 01/01/2027

Hi team,

Sending over a coastal marina we like. Brightwater Marina & Boatyard LLC, owner operated since 2009.

Exposures
- Main building: 2 story office, ship store and restaurant, JM, built 1994, roof replaced 2020
- Service building: steel frame, 9,600 sq ft, used for hull and engine repair (no fiberglass layup)
- Dry stack: 180 racks, enclosed metal building, foam suppression system installed 2022
- Wet slips: 142, floating docks, concrete pilings
- TIV $6,385,000; wind is required, insured will take 5% named storm

Liability: GL $1M/$2M; marina operators legal liability $1M, customers' boats in care, custody or control, largest vessel valued at $750k (vessel list included).

Loss history: 2023 wind claim, $38,200, closed; 2025 slip customer fall, $12,500 paid, closed. Nothing open.

Current premium is about $88k across property and GL with a carrier exiting the coast. Retail agent believes the client will pay up to $110k for a well structured program.

Effective 1/1/2027. We'd like quotes by December 1 so the retailer has time to present.

Documents included: SOV, carrier loss runs (5 yrs, valued 9/30/26), ACORD 125, 126 and 140, vessel list, dry stack fire suppression certificate.

Thanks,
Teresa

Teresa Lindqvist
Vice President | Ironbridge Wholesale Insurance Services
Houston, TX | 713-555-0129
""")

# 17
add("ironbridge_wholesale", dict(market="US", sender_type="wholesale_broker", purpose="bind_request", header_style="gmail", tone="terse", length="short"), """
Teresa Lindqvist <tlindqvist@ironbridgewholesale.com>
Dec 18, 2026, 4:51 PM
to coastal.uw

Bind Brightwater per your quote 12/10, option B ($104,250). Eff 1/1/27. Signed app and SL forms to follow.
""")

# 18
add("glenarm_specialty", dict(market="US", sender_type="mga", purpose="endorsement", header_style="forwarded_original_message", tone="neutral", length="medium"), """
From: Rosalind Achebe <rachebe@glenarmspecialty.com>
Sent: Wednesday, February 3, 2027 1:40 PM
To: Underwriting Ops <uwops@glenarmspecialty.com>
Subject: FW: Fairhaven Dental Group - add new office

Ops, can you process this one, the AP is $1,140 per the rater. Effective 2/15.

-----Original Message-----
From: Jasper Nkemelu <jasper@granitepeakagency.com>
Sent: Wednesday, February 3, 2027 11:02 AM
To: Rosalind Achebe <rachebe@glenarmspecialty.com>
Subject: Fairhaven Dental Group - add new office

Rosalind,

Fairhaven Dental is opening a fifth office at 1880 S Colorado Blvd, Denver CO 80222 on February 15. Tenant improvements and equipment come to $640,000, business personal property only, leased space in a masonry building with sprinklers. Please endorse and send me the added premium.

Jasper Nkemelu
Granite Peak Agency
""")

# 19
add("glenarm_specialty", dict(market="US", sender_type="mga", purpose="renewal", header_style="none", tone="neutral", length="medium", no_from_line=True, avoids_cue_words=True), """
Jasper,

The Fairhaven Dental Group renewal is coming up on 5/1/2027. To get terms out in time we need the following from you by March 31:

- updated property schedule with the five offices and current BPP values
- current-year revenue and number of dentists and hygienists
- carrier loss history valued within 90 days
- confirmation that no offices have moved or closed

Rate change is likely to be flat to +5% if the experience stays clean. Happy to jump on a call if easier.

Rosalind Achebe
Senior Underwriter
Glenarm Specialty Underwriters | Professional & Package
303-555-0172
""")

# 20
add("pemberton_lyle", dict(market="UK", sender_type="london_broker", purpose="new_business", header_style="outlook", tone="formal", length="long"), """
From: Imogen Thrale <imogen.thrale@pembertonlyle.co.uk>
Sent: 07 October 2026 10:05
To: Felix Danvers <felix.danvers@syndicate3390.co.uk>
Cc: Property Team <property@pembertonlyle.co.uk>
Subject: Open market submission | Sorrel Agri-Foods Group plc | Property Damage & BI | 31/12/2026

Dear Felix,

We have been appointed to market the property programme of Sorrel Agri-Foods Group plc with effect from 31 December 2026 and would welcome your consideration as leader.

The group processes and packs fresh produce at seven sites in Lincolnshire, Kent and the Netherlands. Total declared values are GBP 212m, of which GBP 64m is gross profit on a 24 month indemnity period. The largest single site, Spalding, carries GBP 71m. Six of the seven sites have full sprinkler protection to LPC rules; the Dutch packhouse is protected by detection only and a sprinkler installation is budgeted for Q2 2027.

The programme is currently placed on a subscription basis with an aggregate premium of GBP 486,000. The client is seeking to increase the BI indemnity period and to add a cold-chain spoilage extension at GBP 5m. We would like your view on both, and on capacity for a 25% to 40% line.

The enclosed pack comprises the schedule of insured values by site, ten years of claims experience, engineering surveys for the four largest sites, and the client's business continuity plan.

We would be grateful for an indication by Friday 6 November, ahead of client meetings in the week of 16 November.

With best regards,

Imogen Thrale
Divisional Director, Property & Casualty
Pemberton Lyle Ltd, Lloyd's Broker
1 Leadenwell Street, London EC3V 4AB
Direct +44 20 7946 0451

Pemberton Lyle Ltd is authorised and regulated by the Financial Conduct Authority (FRN 612345). This message is confidential and may be privileged; if received in error please notify the sender and delete it.
""")

# 21
add("pemberton_lyle", dict(market="UK", sender_type="london_broker", purpose="chasing_quote", header_style="outlook", tone="formal", length="short"), """
From: Imogen Thrale
Sent: 04 November 2026 16:20
To: Felix Danvers
Subject: RE: Sorrel Agri-Foods - indication

Felix, a reminder that we are hoping for your indication by Friday. Happy to set up a call on the Dutch site.

Imogen
""")

# 22
add("cardew_ross_brokers", dict(market="UK", sender_type="retail_broker", purpose="renewal", header_style="outlook", tone="neutral", length="medium"), """
From: Rhys Carrow <rhys.carrow@cardewross.co.uk>
Sent: 02 November 2026 08:55
To: Northern Commercial Underwriting <nc.uw@cobaltline-specialty.co.uk>
Subject: Renewal - Wharfedale Joinery & Shopfitting Ltd - Policy CL/889214 - due 01/01/27

Hi all,

Renewal information for Wharfedale Joinery & Shopfitting Ltd, Otley. No change to trade or premises. Turnover for the year ending June 2026 was GBP 3.84m (prior GBP 3.51m), wageroll GBP 1.22m.

One theft claim during the year, GBP 6,800 tools from a site van, settled. Please can we have terms by 10 December. Client would accept a higher property excess if it holds the premium near this year's GBP 14,920.

Cheers,
Rhys Carrow
Account Handler, Cardew Ross Insurance Brokers, Leeds
0113 496 0275
""")

# 23
add("cardew_ross_brokers", dict(market="UK", sender_type="retail_broker", purpose="endorsement", header_style="none", tone="terse", length="short", no_from_line=True), """
Subject: CL/889214 Wharfedale - add vehicle store

Please add the detached vehicle store at the rear of the premises, buildings sum GBP 85,000, from today. Brick and steel clad, alarmed. Let me know the AP.

Rhys - Cardew Ross
""")

# 24
add("silverlake_es", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="neutral", length="medium"), """
From: Nadia Farouk <nfarouk@silverlake-es.com>
Sent: Tuesday, October 20, 2026 5:12 PM
To: DIC Submissions <dic@cobaltline-us.com>
Subject: DIC/EQ submission - Mirador Office Partners - 3 bldgs San Jose - 1/15/27

Hello,

Looking for earthquake and flood DIC on Mirador Office Partners. Three Class A office buildings in San Jose, steel moment frame, built 1999, 2001 and 2016. Total TIV $186,000,000. Requesting $25M primary EQ limit, 5% deductible, with flood included.

Incumbent DIC premium is $1.12M and the client wants to compare with a $50M limit. Seismic reports with PML figures are part of the package along with the SOV.

Effective 1/15/2027. Quotes needed by 12/18.

Nadia Farouk
Silverlake Excess & Surplus Brokers | San Francisco
CA License 0K48211
""")

# 25
add("silverlake_es", dict(market="US", sender_type="wholesale_broker", purpose="answering_subjectivities", header_style="on_wrote_reply", tone="neutral", length="medium"), """
Subject: Re: Mirador Office Partners - DIC quote open items

Hi Victor,

Answers below in blue:

- Year of seismic retrofit for Bldg A: no retrofit required, built to 1997 UBC
- Confirm no soft-story construction: confirmed by the structural engineer's letter dated 11/2
- Tenant list for Bldg C: largest tenant is a software company at 38% of rentable area, lease through 2031

I think that closes everything. Please send the binder request form when you are ready.

Nadia

On Mon, Jan 4, 2027 at 9:21 AM Victor Amari <vamari@cobaltline-us.com> wrote:
> Nadia, before we can bind we need the three items below. Thanks, Victor
""")

# 26
add("prairie_beacon_insurance", dict(market="US", sender_type="retail_agent", purpose="new_business", header_style="gmail", tone="casual", length="short"), """
From: Grace Ellery <grace@prairiebeacon.com>
To: submissions@bluestempm.com
Subject: Grain elevator - new account

New grain elevator account in Hutchinson KS, 2 locations, $9.2M TIV. Eff 12/1. Apps, SOV and loss runs attached. Can you take a look? Thanks, Grace
""")

# 27
add("prairie_beacon_insurance", dict(market="US", sender_type="retail_agent", purpose="renewal", header_style="outlook", tone="neutral", length="medium"), """
From: Grace Ellery <grace@prairiebeacon.com>
Sent: Monday, August 31, 2026 1:18 PM
To: Ethan Szabo <eszabo@bluestempm.com>
Subject: Cottonwood Feed & Seed Co-op - renewal 11/1

Ethan,

Cottonwood Feed & Seed is up for renewal 11/1. A few changes this year:

The co-op bought a fertilizer blending plant in Newton. They also replaced the conveyor at the main elevator and installed bearing temperature sensors and hazard monitoring on both legs.

Updated values come to about $14.6M across 4 sites. Payroll is $2.9M, sales $41M.

Expiring premium was $132,400. They'd like to keep it under $150k if you can get there.

Need your renewal quote by October 9 please, the board meets the 15th.

Grace Ellery
Prairie Beacon Insurance | Hutchinson, KS
620-555-0136
""")

# 28
add("ardent_gate_underwriting", dict(market="UK", sender_type="mga", purpose="bind_request", header_style="outlook", tone="formal", length="medium"), """
From: Tabitha Crane <t.crane@ardentgate.co.uk>
Sent: 16 December 2026 15:34
To: Delegated Authority Desk <da@stonecrop-europe.co.uk>
Subject: Bind confirmation required - Larch Court Residents Management Co Ltd - ref AGU/PO/40177

Dear colleagues,

Following our referral of 9 December and your agreement in principle, we are now instructed to incept the above residential block policy from 1 January 2027.

Buildings sum insured GBP 22,750,000 (reinstatement, day one basis), 112 flats over two blocks, built 2008, concrete frame with brick facade, no combustible cladding per the EWS1 form held on file. Property owners liability GBP 10m. Premium GBP 18,245 plus IPT.

Please confirm we may bind and we will issue documentation under our authority.

Yours faithfully,

Tabitha Crane
Underwriting Manager
Ardent Gate Underwriting Ltd
""")

# 29
add("halcyon_ridge_brokers", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="formal", length="long"), """
From: Constance Reilly <creilly@halcyonridge.com>
Sent: Monday, October 26, 2026 8:40 AM
To: Hugo Pellegrini <hpellegrini@oldweirus.com>
Cc: Yusuf Demir <ydemir@halcyonridge.com>
Subject: New Submission - Lantern Street Residential Portfolio (NYC habitational) - Property & Umbrella - eff 01/01/2027

Hugo,

Hope you are well. We are marketing a New York habitational portfolio for a long-standing retail client and would very much like your participation on the primary property layer.

Insured: Lantern Street Residential LLC and affiliated single-purpose entities
Schedule: 23 buildings, 611 units, Manhattan and Brooklyn, mostly pre-war masonry walk-ups, 6 elevator buildings
Total insured value: $318,400,000 (building, rents, equipment breakdown)
Program structure: $25M primary with layered excess to $100M; umbrella $25M
Deductible: $50,000 AOP, water damage $100,000
Expiring property premium: $1,487,000; client budget $1.6M for the property tower

Risk improvements since last year: boilers converted to dual fuel at 14 buildings, leak detection with auto shutoff installed in 9 buildings, and gas line inspections (LL152) completed for all sites with no open violations.

Loss experience: average annual incurred of about $410,000 over five years, mostly water damage. One 2024 fire at a Brooklyn walk-up, $1.9M incurred, cause was a tenant's space heater.

Enclosed: SOV with COPE details, five year loss runs valued 9/30/2026, building inspection reports, LL152 certificates, ACORD 125/140.

We need indications by November 23 and firm quotes by December 10. Thank you for looking at this.

Best,

Constance Reilly
Executive Vice President, Property
Halcyon Ridge Brokers, Inc.
590 Madison Avenue, 21st Floor, New York, NY 10022
O 212-555-0181 | M 917-555-0102
""")

# 30
add("halcyon_ridge_brokers", dict(market="US", sender_type="wholesale_broker", purpose="chasing_quote", header_style="gmail", tone="terse", length="short", avoids_cue_words=True), """
Yusuf Demir <ydemir@halcyonridge.com>
Nov 24, 2026, 6:02 PM
to Hugo

Hugo - checking in on Lantern Street. We had your indication pencilled in for yesterday. Can you give us a date?

YD
""")

# 31
add("tolland_insurance_agency", dict(market="US", sender_type="retail_agent", purpose="endorsement", header_style="outlook", tone="neutral", length="short"), """
From: Nell Garvey <ngarvey@tollandagency.com>
To: service@westvaleins.com
Sent: 4/6/2027 10:44 AM
Subject: Change request - Bristow Hill Orchards - add mortgagee

Please add Hartland Valley Farm Credit ACA as mortgagee on the barn at 210 Bristow Hill Rd, Glastonbury CT, loan # 4471-0098. Effective today. Send me the updated dec page when done.

Thanks,
Nell
Tolland Insurance Agency
""")

# 32
add("crestwater_specialty", dict(market="UK", sender_type="london_broker", purpose="renewal", header_style="outlook", tone="formal", length="medium"), """
From: Pieter Van Dam <p.vandam@crestwater.co.uk>
Sent: 05 October 2026 12:11
To: Beatriz Coelho <beatriz.coelho@halberdmanaging.co.uk>
Subject: Renewal 2027 | Ostra Hotels SA | Portugal property | expiring 31/12/2026

Dear Beatriz,

Ahead of the 1 January renewal of Ostra Hotels SA, the client has made the following changes: a fourth hotel in Faro opened in June (EUR 38m declared).

Total declared values for 2027 are EUR 154m including 12 months loss of rents. The client is happy with the current deductible of EUR 100,000 and would like to retain the existing 30% line with you.

Expiring premium for your line was EUR 92,700. Could we have renewal terms by 13 November?

Yours sincerely,
Pieter Van Dam
Crestwater Re & Specialty Ltd
""")

# 33
add("oakmere_commercial", dict(market="UK", sender_type="retail_broker", purpose="new_business", header_style="none", tone="neutral", length="medium", no_from_line=True, avoids_cue_words=True), """
Good morning Ethan,

I have a new manufacturing risk I think fits your appetite. Bramwell Packaging Solutions Ltd, Trafford Park, makes corrugated board for the food sector.

Single site, steel portal frame building of 9,200 m2, built 2012, full sprinklers and a monitored fire alarm. Buildings GBP 6.1m, plant GBP 4.4m, stock GBP 1.3m, gross profit GBP 3.8m with a 24 month period.

Start date 1 February 2027. They are paying GBP 31,400 with their current insurer and have had one small fire in a baler in 2024, GBP 18k.

Terms by mid-January would be ideal.

Speak soon,
Joanna Whitcombe
Commercial Account Executive
Oakmere Commercial Insurance Brokers | Manchester
0161 496 0438
""")

# 34
add("bluestem_program_managers", dict(market="US", sender_type="mga", purpose="answering_subjectivities", header_style="outlook", tone="neutral", length="medium"), """
From: Ethan Szabo <eszabo@bluestempm.com>
Sent: Friday, November 13, 2026 3:05 PM
To: Agribusiness UW <agri@halberdcasualty.com>
Subject: Cottonwood Feed & Seed Co-op - subjectivity response

Hi team,

On the Cottonwood renewal, here is where we stand on your quote conditions:

- Dust collection maintenance logs for both elevators: received, enclosed
- Hot work permit program: insured uses a written permit system, a blank copy is enclosed
- Updated values for the Newton plant: $2,350,000 building, $1,100,000 equipment, confirmed by the co-op manager
- Loss control visit: scheduled for December 8

Please confirm these satisfy the pre-binding items so we can issue the binder for 11/1. The loss control visit would be post-binding.

Ethan Szabo
Program Manager, Agribusiness
Bluestem Program Managers
""")

# 35
add("quayside_risk", dict(market="UK", sender_type="coverholder", purpose="endorsement", header_style="outlook", tone="terse", length="short"), """
From: Owain Pryddy
To: Lloyd's Desk
Date: 11/02/2027
Subject: QRL/HH/2207 - change of address

Insured has moved. New risk address 14 Mill Bank, Ludlow SY8 1AB, same contents sum. Please note on cover from 08/02/27.
""")

# 36
add("sundial_brokerage_partners", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="neutral", length="medium"), """
From: Clare Whitford <cwhitford@sundialbrokerage.com>
Sent: Thursday, October 1, 2026 2:00 PM
To: Florida Property <flprop@stonecropspecialty.com>
Subject: Submission - Pelican Shores Condominium Assn - Naples FL - wind incl - 12/31/26

Hi Hannah,

Pelican Shores Condominium Association, Naples. One 9 story building, 84 units, built 2003, reinforced concrete, impact glass throughout, roof replaced 2021. Milestone inspection completed in 2025 with no structural repairs required.

TIV $47,300,000. Looking for a layered or shared program including named storm with a 3% deductible, or 5% if that helps the price.

Expiring premium $612,000. Board budget is $650,000.

Effective 12/31/2026. Please quote by 12/4. Wind mitigation form, SOV, milestone report and loss runs are in the package.

Clare Whitford
Sundial Brokerage Partners | Tampa, FL
""")

# 37
add("sundial_brokerage_partners", dict(market="US", sender_type="wholesale_broker", purpose="bind_request", header_style="on_wrote_reply", tone="terse", length="short"), """
Hannah - please bind Pelican Shores, 3% option, $638,500 total. Eff 12/31.

Clare

On Tue, Dec 22, 2026 at 10:15 AM Hannah Pruett <hpruett@stonecropspecialty.com> wrote:
> Clare, quote revised as requested. Valid until 12/29.
""")

# 38
add("linden_pryce", dict(market="US", sender_type="retail_agent", purpose="new_business", header_style="outlook", tone="neutral", length="medium"), """
From: Marcus Delaney <mdelaney@lindenpryce.com>
Sent: Wednesday, September 16, 2026 9:30 AM
To: Corvid Specialty Brokerage <submissions@corvidspecialty.com>
Subject: Peachtree Pallet Recycling - property & GL - need a market

Hello,

I have a pallet recycling operation in Macon, GA that admitted carriers will not touch. 3 acres, one 22,000 sq ft metal building (non-combustible, not sprinklered), outdoor pallet storage with 50 ft separation from the building. TIV $2.1M. GL exposure is $4.6M in sales.

Requested effective date 11/1/2026. Premium last year $47,800 package.

We have ACORD 125, 126 and 140 completed and loss runs from the current carrier (one fire, 2022, outdoor stock only).

Marcus Delaney
Linden & Pryce Insurance | Macon, GA
478-555-0158
""")

# 39
add("varga_hollins", dict(market="UK", sender_type="london_broker", purpose="renewal", header_style="outlook", tone="formal", length="long"), """
From: Bettina Sorensen <bettina.sorensen@vargahollins.com>
Sent: 30 September 2026 17:48
To: Gwilym Hart-Davies <g.hartdavies@syndicate5527.co.uk>; Dolores Kwan <d.kwan@cobaltline-specialty.co.uk>
Cc: Arjun Mehta <arjun.mehta@vargahollins.com>
Subject: 1/1 renewal - Meridale Mining Corporation - Construction & Operational Property - Chile & Peru

Dear Gwilym and Dolores,

As the 1 January renewal approaches, we write with the renewal information for Meridale Mining Corporation's operational property programme.

Summary of changes for 2027:
- The Quebrada Alta concentrator expansion reached mechanical completion in July and moves from the construction section into operational cover. Replacement value USD 410m.
- The Peruvian tailings facility has been independently reviewed against GISTM; the consultant's report is included in the renewal pack.
- Total insured values increase from USD 2.31bn to USD 2.74bn, with BI at USD 860m on a 24 month indemnity period.

The client is seeking renewal of the existing programme structure: USD 500m loss limit, USD 10m PD deductible and 60 days BI waiting period, with a USD 100m earthquake sublimit. We would like to discuss the pricing of the earthquake sublimit in light of the improved seismic study.

Expiring premium for the 100% order is USD 9.84m. Your current lines are 15% and 12.5% respectively, and we would welcome confirmation that you are able to renew at the same shares.

Claims experience is clean for the last three years following the 2023 conveyor fire, which is now closed at USD 14.2m.

We would be grateful for your quotes by 6 November.

Yours sincerely,

Bettina Sorensen
Partner, Mining & Natural Resources
Varga Hollins LLP, Lloyd's Broker
20 Gracechurch Lane, London EC3V 0BG

This email is confidential and is intended for the addressee only. Varga Hollins LLP is authorised and regulated by the Financial Conduct Authority.
""")

# 40
add("granite_peak_agency", dict(market="US", sender_type="retail_agent", purpose="chasing_quote", header_style="gmail", tone="terse", length="short"), """
From: Jasper Nkemelu <jasper@granitepeakagency.com>
Subject: Re: Alpine Ridge Lodge quote?
Date: Thu, 15 Oct 2026 16:40:11 -0600

Following up again. Lodge owner signs with someone else Monday if I don't have a number. Please advise.

JN
""")

# 41
add("thornbury_specialty", dict(market="UK", sender_type="mga", purpose="answering_subjectivities", header_style="outlook", tone="neutral", length="medium"), """
From: Felicity Draycott <f.draycott@thornburyspecialty.co.uk>
Sent: 23 November 2026 10:27
To: Rhys Carrow <rhys.carrow@cardewross.co.uk>
Subject: RE: Holmfirth Textile Mills - quotation conditions

Hi Rhys,

Thanks for the information. Taking each point:

1. Electrical inspection (EICR) - received, dated 3 October 2026, satisfactory. Condition cleared.
2. Thermographic survey - the insured has booked this for 12 January. We can bind subject to receipt within 60 days of inception.
3. Waste removal - we need written confirmation that combustible waste is removed from the building at the end of each shift. Please ask the insured to put this in an email or letter.

Once item 3 arrives I can release the policy wording.

Kind regards,
Felicity Draycott
Senior Underwriter, Thornbury Specialty Underwriting
""")

# 42
add("calloway_excess", dict(market="US", sender_type="wholesale_broker", purpose="new_business", header_style="outlook", tone="neutral", length="medium"), """
From: Ethan Okonkwo <eokonkwo@callowayexcess.com>
Sent: Tuesday, November 3, 2026 11:19 AM
To: Builders Risk Desk <br@ferrousindemnity.com>
Subject: Builders risk - The Ledger Lofts, Richmond VA - 14 mo term

Team,

New ground-up builders risk: The Ledger Lofts, 5 story podium, 4 floors wood frame over 1 floor concrete, 96 units plus retail. Hard costs $28.4M, soft costs $3.1M. Term 14 months starting 1/4/2027.

GC is a regional firm with 30 years in business. Site security: fencing, cameras with remote monitoring, a night guard from framing onwards. Water damage and theft deductibles are flexible.

Seeking a quote by 12/11. Construction schedule, site plan and the GC's qualifications are in the package.

Ethan Okonkwo
Calloway Excess & Surplus | Charlotte, NC
""")

# 43
add("kingsferry_underwriting", dict(market="UK", sender_type="coverholder", purpose="bind_request", header_style="none", tone="terse", length="short", no_from_line=True, avoids_cue_words=True), """
To: Lloyd's Desk
Subject: KFU/0471 Moorfoot Kennels - incept please

Broker confirms client happy with terms. Please incept from 01/12/2026, GBP 2,140 incl IPT.

Kingsferry Underwriting Ltd
""")

# 44
add("westvale_insurance_services", dict(market="US", sender_type="retail_agent", purpose="renewal", header_style="outlook", tone="neutral", length="medium"), """
From: Celia Okoro <cokoro@westvaleins.com>
Sent: Monday, August 17, 2026 2:22 PM
To: Underwriting <uw@glenarmspecialty.com>
Subject: Renewal - Sable Creek Veterinary Clinic - BOP - 10/1/2026

Hi,

Sable Creek Veterinary Clinic is renewing 10/1. No changes to the building or operations. Two vets, four techs, revenue $2.3M. Building value $1.45M, BPP $420k.

The owner tells us they have had no losses in the past five years, and she has agreed to sign a no-known-loss statement for the file.

Renewal premium last year was $6,870. Please send renewal terms by 9/10.

Thank you,
Celia Okoro
Westvale Insurance Services | Sacramento, CA
""")
