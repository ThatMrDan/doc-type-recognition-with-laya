import json, sys

OUT = sys.argv[1]
rows = []  # (key, slice, group, label, rule, flags, parent_key, attrs, text)


def add(key, slice_, group, attrs, text, label="other", rule=None, flags=None, parent=None):
    rows.append(dict(key=key, slice=slice_, group=group, label=label, rule=rule,
                     flags=flags or [], parent=parent, attrs=attrs, text=text.strip("\n")))


def core(key, group, attrs, text, **kw):
    add(key, "core", group, attrs, text, **kw)


def bnd(key, group, attrs, text, rule, label="other", flags=None):
    add(key, "boundary", group, attrs, text, label=label, rule=rule, flags=flags)


def con(key, parent, label, attrs, text):
    add(key, "contrast", None, attrs, text, label=label, parent=parent)


def A(market, fmt, kind, noise="clean"):
    return {"market": market, "format": fmt, "doc_kind": kind, "noise": noise}

# ---------------------------------------------------------------- core
core("C1", "risk-survey-halberd", A("UK", "pdf", "risk engineering report"), """
HALBERD UNDERWRITING LIMITED - RISK ENGINEERING REPORT
Insured: Penhallow Textiles Ltd | Site: Unit 4, Carrow Road Industrial Estate, Norwich NR1 2QT | Survey date: 14 August 2026 | Surveyor: Gareth Iles BEng MIFireE | Report ref: HU-RE-26-0817
1. Executive summary
The site is a single-storey steel portal frame weaving and dyeing works of approximately 6,400 m2, built 1987 with a 2009 extension. Walls are part brick, part insulated composite panel (PIR core, unapproved). The building is not sprinklered. Fire detection is an L2 automatic system monitored by an ARC. Housekeeping in the dye house was poor at the time of visit, with lint accumulation on overhead ductwork.
2. Risk grading
Fire: Below average. Theft: Average. Business interruption: Below average (single site, long lead time on replacement Jacquard looms).
3. Loss history (as reported by the insured)
The insured reported a small fire in the drying range in 2023, put out by staff with extinguishers; no claim was made.
4. Recommendations
26/01 Remove lint from extract ductwork on a monthly schedule.
26/02 Replace PIR panels adjoining the boiler house with LPCB-approved panels.
26/03 Introduce a written hot work permit system.
Please confirm acceptance of the recommendations within 30 days.
""")

core("C2", "risk-survey-halberd", A("UK", "pdf", "risk improvement follow-up", "ocr"), """
HALBERD UNDERWRITING LTD   RISK IMPROVEMENT FOLLOW-UP
Insured : Calloway Foods Ltd     Locati0n : Bay 7, Fenland Way, Wisbech PE13 2RT
Visit date: 03/09/2026   Ref: HU-RE-25-1142/FU
Rec No.   Recommendation                          Status
25/01     Thermographic survey of main LV board   Complete - report seen
25/02     Segregate pallet store from bldg        Outstanding
25/03     Fit fire doors to cold store corridor   In progress, target Nov 26
Overall gradlng unchanged: Average.  Next survey due Q3 2027.
""")

core("C3", "risk-survey-halberd", A("UK", "pdf", "desktop survey note"), """
Halberd Underwriting | Risk Engineering | Desktop survey note | Insured: Upton Vale Hotels plc, 3 sites | No visit required; review of photographs and FRA supplied. Grading: Average. No recommendations.
""")

core("C4", "loss-control-survey-granite", A("US", "pdf", "loss control survey"), """
GRANITE RIDGE CASUALTY COMPANY
LOSS CONTROL SURVEY REPORT
Account: Ridgeback Plastics Inc.   Policy No.: GRC-CPP-3318842   Survey Date: 09/16/2026
Consultant: Wendell Okafor, CSP   Location surveyed: 2210 Industrial Pkwy, Dayton, OH 45414
OPERATIONS: Injection molding of polypropylene housings, 3 shifts, 84 employees. 22 molding machines, a regrind area and a 40,000 sq ft warehouse with rack storage to 18 ft.
CONSTRUCTION / PROTECTION: Joisted masonry, built 1974, wet pipe sprinklers throughout; warehouse design density is not adequate for Group A plastics at the current storage height. Public protection class 3. Hydrant 200 ft.
LOSS HISTORY DISCUSSED: Management described a 2022 hydraulic oil fire at Press 14 (approx. $180,000 property damage) and two forklift injuries in 2024. Loss runs were not reviewed as part of this visit.
RECOMMENDATIONS:
26-1 Limit storage of expanded plastics to 12 ft or upgrade in-rack sprinklers.
26-2 Install fire-resistant hydraulic fluid on presses over 500 tons.
26-3 Implement a written forklift operator certification program.
OVERALL RATING: Fair. Account acceptable subject to completion of 26-1 within 90 days.
""")

core("C5", "loss-control-survey-granite", A("US", "pdf", "survey scheduling notice"), """
GRANITE RIDGE CASUALTY - LOSS CONTROL - Survey request confirmation. Account: Sorrel Creek Apartments LLC, 4 bldgs, Tulsa OK. Inspection scheduled 10/29/2026 9:00 AM with the property manager on site.
""")

core("C6", "fra-ardent", A("UK", "pdf", "fire risk assessment"), """
FIRE RISK ASSESSMENT
Regulatory Reform (Fire Safety) Order 2005
Premises: The Granary, 12-14 Mill Lane, Ludlow SY8 1BB
Responsible person: Upton Vale Hotels plc
Assessor: Ardent Fire Consultancy (Fiona Marchetti, IFE Member)
Date of assessment: 22 July 2026     Review date: July 2027
Description of premises: Grade II listed three-storey hotel of timber frame and brick construction, 28 bedrooms, ground floor restaurant and bar with commercial kitchen. Sleeping risk. Peak occupancy approximately 70 persons.
Fire alarm: Category L1 to BS 5839-6 grade A, tested weekly.
Emergency lighting: BS 5266, monthly function tests recorded.
Significant findings:
1. Kitchen extract ductwork not cleaned in the last 12 months. Priority: High.
2. Self-closer missing to second floor bedroom 21. Priority: Medium.
3. Staff fire training records incomplete for agency staff. Priority: Medium.
Overall risk rating: Moderate. Action plan attached.
""")

core("C7", "fra-ardent", A("UK", "pdf", "FRA action plan close-out"), """
ARDENT FIRE CONSULTANCY | FRA action plan close-out | Premises: Penhallow Textiles, Norwich | Items 1-6 closed, item 7 (dye house fire stopping) open, due 31/12/2026.
""")

core("C8", "valuation-cairnfield", A("UK", "pdf", "reinstatement cost assessment"), """
CAIRNFIELD SURVEYORS LLP - Reinstatement Cost Assessment for Insurance Purposes
Client: Dunmore Cold Storage Ltd   Property: Dunmore Park, Selby YO8 4ER   Date of inspection: 11 June 2026
We have assessed the cost of reinstating the buildings on a day one basis, including demolition and site clearance, professional fees at 12% and local authority charges, excluding VAT. In our opinion the declared value should be GBP 18,450,000. This assessment is provided for insurance purposes only and is not a market valuation. Building schedule at Appendix B.
""")

core("C9", "valuation-cairnfield", A("UK", "pdf", "insurance reinstatement valuation"), """
CAIRNFIELD SURVEYORS LLP
Insurance Reinstatement Valuation  |  Ref CS/26/3391  |  Valuation date 30 September 2026
Client: Upton Vale Hotels plc
Basis: reinstatement cost, day one, excluding VAT, fees at 12.5%, debris removal included.
Our assessment is based on an external and internal inspection carried out on 18 September 2026 by Imogen Thackeray MRICS. Floor areas are gross internal areas measured on site.
Building | Address | Construction | Year built | GIA m2 | Reinstatement £
1 | The Granary, 12-14 Mill Lane, Ludlow SY8 1BB | Timber frame / brick, slate roof | c.1780 | 2,140 | 6,420,000
2 | Coach House, 12 Mill Lane, Ludlow SY8 1BB | Brick, slate roof | c.1820 | 380 | 1,045,000
3 | Riverside Lodge, Teme Road, Ludlow SY8 1PQ | Brick and block, tiled roof | 2004 | 960 | 2,115,000
Total | | | | 3,480 | 9,580,000
The listed status of building 1 increases reinstatement cost owing to specialist materials and conservation officer requirements. We recommend the sums insured are reviewed annually by index and a full revaluation is undertaken every three years.
""")

core("C10", "appraisal-stonebridge", A("US", "pdf", "insurable value appraisal"), """
STONEBRIDGE VALUATION GROUP, INC.
Insurable Value Appraisal  -  Sorrel Creek Apartments LLC
Effective date of value: 08/01/2026
Scope: Replacement cost new (RCN) and insurable value of 4 garden-style apartment buildings at 7700 E 61st St, Tulsa, OK 74133, using the cost approach and a commercial cost estimating service.
Bldg | Units | Construction | Yr Built | Sq Ft | RCN
A | 24 | Frame | 1998 | 22,800 | $3,420,000
B | 24 | Frame | 1998 | 22,800 | $3,420,000
C | 16 | Frame | 1999 | 15,200 | $2,280,000
D | 16 | Frame | 1999 | 15,200 | $2,280,000
Total | 80 | | | 76,000 | $11,400,000
Certification: I certify that, to the best of my knowledge and belief, the statements of fact contained in this report are true and correct. Desmond Achebe, ASA
""")

core("C11", "appraisal-stonebridge", A("US", "letter", "appraisal engagement letter", "ocr"), """
STONEBRIDGE VALUATlON GROUP   Engagement letter - insurable value appraisal, Ridgeback Plastics Inc., Dayton OH. Fee $4,850. Site inspection week of 11/09/2026.
""")

core("C12", "supp-cyber-corvid", A("US", "pdf", "cyber supplemental application"), """
CORVID MUTUAL INSURANCE COMPANY
CYBER AND PRIVACY LIABILITY SUPPLEMENTAL APPLICATION  (CM-CY-SUP 07/25)
This supplemental must be completed in addition to ACORD 125. Please attach ACORD 125 and the most recent financial statements.
Applicant name: Ridgeback Plastics Inc.
1. Do you enforce multi-factor authentication for all remote access to your network?  Y / N
2. Do you keep offline or immutable backups, tested at least quarterly?  Y / N
3. Annual revenue: $________
4. Number of records containing PII held:  ________
5. In the past 3 years, have you suffered a ransomware incident or data breach?  Y / N   If yes, describe.
""")

core("C13", "supp-cyber-corvid", A("US", "pdf", "cyber supplemental page"), """
Corvid Mutual - Cyber supplemental, page 2 of 4.  6. Do you filter inbound email for malicious attachments? Y/N  7. Is EDR deployed on all endpoints? Y/N  8. Who is your MSP? ______
""")

core("C14", "supp-recall-brightwater", A("US", "pdf", "product recall questionnaire"), """
BRIGHTWATER SPECIALTY INSURANCE CO.
Product Contamination & Recall Questionnaire
Named insured: Calloway Foods Inc. (US subsidiary)   Products: chilled ready meals, sauces
a) Gross sales by product line, last 3 years (attach breakdown)
b) Do you hold a current SQF or BRCGS certificate?  Yes [ ] No [ ]  Grade: ____
c) Has the company conducted a mock recall in the last 12 months?  Yes [ ] No [ ]
d) Describe traceability: lot coding at ingredient and finished goods level?
e) Any recalls, withdrawals or FDA warning letters in the past 5 years?  Yes [ ] No [ ]  If yes, give dates, products and cost.
""")

core("C15", "supp-recall-brightwater", A("US", "pdf", "questionnaire signature page"), """
Brightwater Specialty - Recall questionnaire - signature page. I declare the answers are true and complete. Signed: Nadia Osei, CFO, Calloway Foods Inc.  Date 10/02/2026
""")

core("C16", "supp-dno-meridale", A("UK", "pdf", "D&O proposal form"), """
MERIDALE SYNDICATE 8871 AT LLOYD'S
Directors' and Officers' Liability Proposal Form - Private Companies
Proposer: Penhallow Textiles Ltd    Companies House no. 04418273
1. Has the company or any subsidiary breached any loan covenant in the last 3 years?  Yes / No
2. Is any director aware of any circumstance which may give rise to a claim?  Yes / No
3. Has any director been disqualified or subject to an HMRC investigation?  Yes / No
4. Please enclose the latest audited accounts and, if more than 6 months old, management accounts.
Important: failure to disclose material facts may entitle insurers to avoid the policy.
""")

core("C17", "supp-dno-meridale", A("UK", "pdf", "D&O proposal financial section"), """
MERIDALE 8871 - D&O proposal - Section 5 Financial information: Total assets £_____  Net assets £_____  Turnover £_____  Has net worth fallen by more than 25% year on year? Y/N
""")

core("C18", "supp-contractors-granite", A("US", "pdf", "contractors supplemental"), """
GRANITE RIDGE CASUALTY COMPANY
CONTRACTORS SUPPLEMENTAL QUESTIONNAIRE   GRC-CON-02 (03/24)
Attach to ACORD 125 and ACORD 126.
Applicant: Bellweather Roofing & Sheet Metal LLC
1. Percentage of work:  Residential __%  Commercial __%  New construction __%  Remodel __%
2. Do you subcontract work?  Y / N   If yes, do you require certificates of insurance from all subs?  Y / N
3. Do you perform any work above 3 stories?  Y / N
4. Do you use torch-down or hot tar applications?  Y / N
5. Any work in New York State in the past 5 years?  Y / N
""")

core("C19", "supp-contractors-granite", A("US", "pdf", "contractors supplemental page", "ocr"), """
GRC-CON-02  pg 2   6. Annual payroll by class: ______   7. Largest job in past 3 yrs: $______   8. Written safety program? Y / N   9. Use of cranes? Y / N
""")

core("C20", "quote-halberd", A("UK", "pdf", "carrier quotation"), """
HALBERD UNDERWRITING LIMITED
QUOTATION - Commercial Combined
Insured: Calloway Foods Ltd    Quote ref: HU-Q-26-55102    Valid until: 30 November 2026
Period: 01/12/2026 to 30/11/2027
Premises: 1. Bay 7, Fenland Way, Wisbech PE13 2RT   2. Unit 3, Saxon Road, King's Lynn PE30 4LT
Material Damage sum insured £14,200,000; Business Interruption (gross profit, 18 months) £6,000,000; Employers' Liability £10,000,000; Public/Products Liability £5,000,000
Total premium £86,450 plus IPT at 12%
Subjectivities: completion of risk recommendation 25/02 within 60 days; satisfactory electrical inspection certificate.
""")

core("C21", "quote-halberd", A("UK", "pdf", "quote summary"), """
Halberd UW - Quote HU-Q-26-55188 - Upton Vale Hotels plc - Property Owners - Premium £41,200 + IPT - terms per attached schedule - NTU if not bound by 15/11/26
""")

core("C22", "indication-brightwater", A("US", "pdf", "non-binding indication"), """
BRIGHTWATER SPECIALTY INSURANCE CO.
NON-BINDING INDICATION - COMMERCIAL PROPERTY
Named Insured: Sorrel Creek Apartments LLC
Producer: Pelham Strand Partners, Chicago IL
Proposed Effective: 12/01/2026    Expiration: 12/01/2027
Premises: 7700 E 61st St, Tulsa, OK 74133 - 4 buildings, frame, garden apartments
Coverage: Special form, replacement cost, $11,400,000 blanket building limit; $250,000 business income with rents
Deductible: $25,000 AOP; 2% wind/hail
Indicated premium: $68,400 plus surplus lines taxes and fees
This indication is subject to receipt of a completed application, a currently valued 5 year loss run and a satisfactory inspection.
""")

core("C23", "indication-brightwater", A("US", "pdf", "declination notice"), """
Brightwater Specialty - Indication declined. Ridgeback Plastics Inc. Reason: Group A plastics storage outside appetite. No terms offered.
""")

core("C24", "binder-corvid", A("US", "pdf", "binder"), """
CORVID MUTUAL INSURANCE COMPANY
BINDER OF INSURANCE    Binder No. CMB-26-00914
Date: 10/21/2026    Effective 12:01 AM 11/01/2026    Expires 12:01 AM 12/01/2026 (30 days)
Named insured: Bellweather Roofing & Sheet Metal LLC, 1450 Commerce Dr, Lansing MI 48906
Coverage bound: Commercial General Liability, occurrence form; $1,000,000 each occurrence / $2,000,000 general aggregate
Premium: $38,720 (deposit, auditable)
Conditions: Binder subject to receipt of signed contractors supplemental and confirmation of no torch-down work.
This binder may be cancelled by the insured by surrender of this binder or by written notice to the company.
""")

core("C25", "binder-corvid", A("US", "pdf", "binder extension"), """
BINDER CMB-26-00977 - extension to 12/15/2026 - all other terms unchanged - Corvid Mutual, authorized representative Luis Ferreira
""")

core("C26", "ba-schedule-thistledown", A("UK", "pdf", "binding authority schedule"), """
BINDING AUTHORITY AGREEMENT - SCHEDULE
UMR: B1874TD26BA012    Coverholder: Thistledown Underwriting Agency Ltd
Period: 01/01/2026 to 31/12/2026
Class of business: UK Commercial Property and Liability for SME risks
Territorial limits: Great Britain, Northern Ireland, Isle of Man and Channel Islands
Gross premium income limit: £4,500,000
Any one risk limit: £5,000,000 Material Damage and BI combined
Commission: 27.5%
Bordereaux: risk and premium monthly within 15 days of month end; claims monthly.
Security: Meridale Syndicate 8871 (60%), Halberd Underwriting Ltd (40%)
""")

core("C27", "ba-schedule-thistledown", A("UK", "pdf", "binding authority endorsement"), """
THISTLEDOWN UW AGENCY - Binding Authority B1874TD26BA012 - Endorsement 3: add Excluded Risks item 14 (waste and recycling plants). All other terms unchanged. Effective 01/07/2026.
""")

core("C28", "mrc-slip-meridale", A("UK", "pdf", "MRC slip"), """
RISK DETAILS
UNIQUE MARKET REFERENCE: B1874PSP2611206
TYPE: Property Damage and Business Interruption
INSURED: Dunmore Cold Storage Ltd and subsidiary companies
PERIOD: From 01 December 2026 to 30 November 2027, both days inclusive, local standard time at the address of the Insured
INTEREST: All real and personal property of every description, and business interruption, as more fully defined in the wording
SUM INSURED: GBP 18,450,000 PD; GBP 9,000,000 BI (24 months indemnity period)
LIMIT: GBP 27,450,000 any one occurrence
EXCESS: GBP 50,000 each and every loss
SITUATION: Dunmore Park, Selby YO8 4ER, United Kingdom
CONDITIONS: Ammonia Refrigeration Warranty; Sanctions Limitation and Exclusion Clause; Cyber Property Exclusion
SUBJECTIVITIES: Satisfactory survey within 60 days of inception
CHOICE OF LAW AND JURISDICTION: England and Wales
PREMIUM: GBP 112,500 (100%)
TAXES PAYABLE BY INSURED: UK IPT 12%
SECURITY DETAILS: Meridale Syndicate 8871 written line 35%
""")

core("C29", "mrc-slip-meridale", A("UK", "pdf", "MRC endorsement"), """
MRC - ENDORSEMENT No. 2 - UMR B1874PSP2611206 - Insured: Dunmore Cold Storage Ltd - Additional premium GBP 4,250 for inclusion of Unit 9. Agreed: Meridale 8871 (slip leader).
""")

core("C30", "presentation-pelham", A("US", "pdf", "broker marketing submission"), """
PELHAM STRAND PARTNERS
2027 RENEWAL MARKETING SUBMISSION
Ridgeback Plastics Inc.
Contents: 1 Executive Summary - 2 Operations - 3 Property Exposures - 4 Casualty Exposures - 5 Loss History - 6 Coverage Requests
1. EXECUTIVE SUMMARY
Ridgeback Plastics is a family-owned custom injection molder founded in 1974 and headquartered in Dayton, Ohio. The company serves appliance and automotive OEMs from a single 120,000 sq ft plant. Since the 2022 press fire the insured has invested $1.2M in fire-resistant hydraulic fluid, in-rack sprinklers and a new hot work program, and its loss control rating has improved from Poor to Fair.
We are approaching a select panel of markets for a 12/1/2026 effective date, seeking a primary property program with a $30M blanket limit and a guaranteed-cost casualty program. Detailed values are in the enclosed SOV and five years of currently valued loss runs are included in Section 5.
Key marketing points: management commitment to risk improvement; no losses above $25,000 since 2022 other than one open water damage claim; long tenure of key customers.
""")

core("C31", "presentation-pelham", A("US", "pdf", "market summary page"), """
PELHAM STRAND PARTNERS | Sorrel Creek Apartments LLC | Renewal Submission 2026-27
Section 3 - Market Summary
Incumbent: Brightwater Specialty (expiring premium $61,900)
Markets approached: 9 | Declined: 4 | Quoted: 3 | Pending: 2
Recommendation: proceed with Brightwater at $68,400 subject to inspection; alternative Corvid Mutual at $72,150 with a lower wind/hail deductible.
Prepared by Rhiannon Duvall, Senior Vice President
""")

core("C32", "financials-audited-penhallow", A("UK", "pdf", "audited financial statements"), """
PENHALLOW TEXTILES LIMITED
Annual Report and Financial Statements for the year ended 31 March 2026
Company registration number 04418273
Independent auditor's report to the members of Penhallow Textiles Limited
Opinion: We have audited the financial statements of Penhallow Textiles Limited for the year ended 31 March 2026, which comprise the statement of comprehensive income, the statement of financial position, the statement of changes in equity and notes to the financial statements, including significant accounting policies. In our opinion the financial statements give a true and fair view of the state of the company's affairs as at 31 March 2026 and of its profit for the year then ended, and have been properly prepared in accordance with FRS 102 and the Companies Act 2006.
Statement of comprehensive income        2026 £000    2025 £000
Turnover                                   21,480       19,935
Cost of sales                             (15,610)     (14,720)
Gross profit                                5,870        5,215
Administrative expenses                    (3,940)      (3,610)
Operating profit                            1,930        1,605
Harrowgate & Pyne LLP, Statutory Auditor, Norwich
""")

core("C33", "financials-audited-keelson", A("US", "pdf", "audited balance sheet"), """
RIDGEBACK PLASTICS, INC.
BALANCE SHEETS
December 31, 2025 and 2024
                                   2025           2024
Cash                         $ 1,842,310    $ 1,205,770
Accounts receivable, net       6,118,904      5,772,018
Inventories                    4,330,512      4,018,660
Total current assets          12,291,726     10,996,448
See accompanying notes and independent auditor's report.  Keelson Ward CPAs, PLLC
""")

core("C34", "mgmt-accounts-calloway", A("UK", "sheet", "management accounts", "ocr"), """
CALLOWAY FOODS LTD - MANAGEMENT ACCOUNTS - PERIOD 6 (SEPT 2026)
 | Month | YTD | Budget YTD
Sales £k | 2,412 | 13,870 | 13,500
Gross margin % | 24.1% | 23.6% | 24.0%
Overheads £k | (388) | (2,301) | (2,280)
EBITDA £k | 193 | 972 | 960
Comment: YTD sales ahead of budget, driven by new multiple retailer contract. Insurance renewal 1/12 inc1uded in Q3 forecast.
""")

core("C35", "debit-note-orrin", A("UK", "pdf", "broker debit note"), """
ORRIN & GALE INSURANCE BROKERS LTD
DEBIT NOTE    No. DN-2611-0482    Date: 02/11/2026
Client: Dunmore Cold Storage Ltd, Dunmore Park, Selby YO8 4ER
UMR: B1874PSP2611206    Insurer: Meridale Syndicate 8871 and others
Class: Property Damage and Business Interruption    Period: 01/12/2026 to 30/11/2027
Premium                   £112,500.00
Insurance Premium Tax      £13,500.00
Total due                 £126,000.00
Payment terms: 30 days from inception. Bank details on remittance advice.
Orrin & Gale is authorised and regulated by the Financial Conduct Authority.
""")

core("C36", "debit-note-orrin", A("UK", "pdf", "broker credit note"), """
ORRIN & GALE - CREDIT NOTE CN-2611-0031 - Penhallow Textiles Ltd - Return premium following deletion of vehicle from fleet schedule - £-412.80 incl. IPT
""")

core("C37", "invoice-castellan", A("US", "pdf", "premium invoice"), """
CASTELLAN SURPLUS LINES BROKERAGE, LLC
INVOICE #44718    10/24/2026
Bill to: Sorrel Creek Apartments LLC c/o Pelham Strand Partners
Policy: BSI-PR-0099315   Brightwater Specialty Insurance Co.   12/01/2026-12/01/2027
Premium $68,400.00 | Policy fee $250.00 | SL tax (OK 6%) $4,119.00 | Stamping fee $68.65 | TOTAL $72,837.65
""")

core("C38", "kyc-castlemere", A("UK", "letter", "KYC and sanctions confirmation"), """
CASTLEMERE RISK PARTNERS LTD
Client due diligence and sanctions confirmation
Client: Penhallow Textiles Ltd (Companies House 04418273)
We confirm that:
1. The client, its directors and beneficial owners holding more than 25% were screened against the HM Treasury consolidated list, the OFAC SDN list and EU lists on 20/10/2026 with no matches.
2. The identity of each director was verified by electronic check.
3. No politically exposed persons were identified.
Signed: Harriet Quayle, Compliance Officer    Date: 20/10/2026
""")

core("C39", "sanctions-letter-insured", A("UK", "letter", "insured sanctions confirmation"), """
To whom it may concern,
We confirm that Quenby Bakeries Ltd and its directors were screened against UK, EU and OFAC sanctions lists on 14/10/2026 and no matches were found.
Signed: Owen Pritchard, Director, Quenby Bakeries Ltd
""")

core("C40", "toba-castlemere", A("UK", "pdf", "terms of business agreement"), """
CASTLEMERE RISK PARTNERS LTD - TERMS OF BUSINESS AGREEMENT
Between Castlemere Risk Partners Ltd ("the Broker") and Meridale Syndicate 8871, managed by Corran Managing Agency Ltd ("the Insurer")
Effective date: 1 January 2026
1. Scope. This agreement governs the placing of non-life business by the Broker with the Insurer, including open market, line slips and binding authorities.
2. Premium handling. Risk transfer applies: premium received by the Broker is held as agent of the Insurer. Settlement within 60 days of inception unless otherwise agreed on the slip.
3. Claims money. Claims money received by the Broker is held as agent of the insured.
4. Data protection. Each party is a controller in its own right under UK GDPR.
5. Financial crime. Both parties keep anti-bribery and sanctions controls; the Broker shall not place business that would breach applicable sanctions.
6. Termination. Either party may terminate on 90 days' written notice.
7. Governing law. England and Wales.
Signed for the Broker: Callum Rees, Director      Signed for the Insurer: Petra Lindqvist, Active Underwriter
""")

core("C41", "site-plan-cairnfield", A("UK", "pdf", "site plan legend"), """
SITE PLAN - NOT TO SCALE    Dunmore Park, Selby
[A] Cold store 1 (insulated panel, ammonia plant room on north wall)
[B] Cold store 2
[C] Despatch canopy / 14 loading docks
[D] Offices, 2 storey brick
[E] Sprinkler pump house and 750 m3 tank
[F] Trailer park, 60 bays
Separation A-B: 3 m (no fire wall).  Hydrants: H1-H4 on ring main.  North arrow top left.
Drawn by Cairnfield Surveyors from site measurements, Sept 2026.
""")

core("C42", "photo-log-granite", A("US", "pdf", "photo log"), """
PHOTO LOG - Granite Ridge Casualty Loss Control
Account: Bellweather Roofing & Sheet Metal LLC    Date: 10/07/2026
Photo 1: Shop exterior, metal building, east elevation.
Photo 2: Propane cylinder storage cage, unlocked - see Rec 26-2.
Photo 3: Torch kit in truck #4 (insured states no longer used).
Photo 4: Flammable liquids cabinet, self-closing doors functional.
Photo 5: Ladder rack and fall protection harnesses, inspection tags current.
""")

core("C43", "loler-cert-sentinel", A("UK", "pdf", "thorough examination report"), """
REPORT OF THOROUGH EXAMINATION - Lifting Operations and Lifting Equipment Regulations 1998
Employer: Calloway Foods Ltd, Bay 7, Fenland Way, Wisbech PE13 2RT
Equipment: Counterbalance forklift truck, Serial No. FL-77310-K, SWL 2,500 kg
Date of examination: 15/09/2026    Next examination due: 15/03/2027 (6 months)
Defects involving existing or imminent danger: None
Defects requiring remedy within a specified time: Mast chain wear at 2.1%, re-examine at next visit
Examined by: Kofi Mensah, Engineer Surveyor, Sentinel Plant Inspection Ltd
""")

core("C44", "boiler-cert-us", A("US", "pdf", "boiler inspection certificate", "ocr"), """
JURISDICTIONAL INSPECTION CERTIFICATE - BOILER AND PRESSURE VESSEL. Owner: Ridgeback Plastics lnc. Object: Hot water boiler, Nat'l Bd No. 48812. Expires 09/30/2027. lnspected by: J. Varga, Commissioned Inspector.
""")

core("C45", "endorsement-corvid", A("US", "pdf", "policy endorsement"), """
CORVID MUTUAL INSURANCE COMPANY
THIS ENDORSEMENT CHANGES THE POLICY. PLEASE READ IT CAREFULLY.
EXCLUSION - ROOFING OPERATIONS INVOLVING OPEN FLAME    CM-GL 41 07 (01/25)
This endorsement modifies insurance provided under the following: COMMERCIAL GENERAL LIABILITY COVERAGE PART
The following exclusion is added to Paragraph 2. Exclusions of Section I - Coverage A:
This insurance does not apply to "bodily injury" or "property damage" arising out of any roofing operations performed by you or on your behalf involving the use of a torch, open flame or hot tar kettle.
Policy No. CM-GL-2611408    Named insured: Bellweather Roofing & Sheet Metal LLC
""")

core("C46", "wording-halberd", A("UK", "pdf", "policy wording extract"), """
Halberd Commercial Combined wording HCC 01/26 - Section 3 Business Interruption - Definitions: "Gross Profit" means the amount by which the Turnover and the Closing Stock exceed the Opening Stock and Specified Working Expenses.
""")

core("C47", "claims-email-ironvale", A("US", "email", "adjuster claim update"), """
From: Marisol Grant <mgrant@ironvaleclaims.com>
To: Rhiannon Duvall <rduvall@pelhamstrand.com>
Subject: Claim GRC-26-118842 - Ridgeback Plastics - water damage 08/14/2026
Rhiannon,
Following our inspection on 8/20, we have issued a first interim payment of $42,500 for mitigation and drying. The current reserve is $96,000 for building repairs pending the contractor's estimate. Coverage is confirmed under the policy subject to the $25,000 deductible. Please ask the insured to send invoices for the temporary chiller rental.
Regards,
Marisol Grant, Senior Property Adjuster, Ironvale Claims Services
""")

core("C48", "claims-letter-fairholme", A("UK", "letter", "loss adjuster settlement letter"), """
Fairholme Loss Adjusters Ltd
Our ref: FLA/26/7731    Your ref: HU-CL-26-0402
Date: 7 October 2026
Private and confidential
Upton Vale Hotels plc, The Granary, 12-14 Mill Lane, Ludlow SY8 1BB
Dear Mr Brereton,
Escape of water - Room 21, The Granary - date of loss 2 September 2026
We write further to our visit on 9 September. Drying is now complete and the moisture readings taken on 30 September are within normal limits. We have agreed the reinstatement scope with your contractor in the sum of £18,640, and loss of revenue for two rooms out of service for 26 nights at an average rate of £145, being £7,540. After the policy excess of £1,000, the agreed settlement is £25,180. Insurers' payment will follow on receipt of the signed discharge form enclosed.
Yours sincerely,
Declan Furness ACII, Senior Adjuster
""")

core("C49", "lc-recs-granite", A("US", "letter", "loss control recommendations letter"), """
GRANITE RIDGE CASUALTY COMPANY - Loss Control Department
October 2, 2026
Sorrel Creek Apartments LLC, Attn: Property Manager, 7700 E 61st St, Tulsa OK 74133
RE: Loss Control Recommendations, Policy GRC-HAB-552019
Thank you for your cooperation during our recent survey. Please address the following and return the enclosed response form within 45 days:
26-01 Replace aluminum branch wiring or install approved copper pigtail connectors in Buildings A and B.
26-02 Clean dryer vents on an annual schedule.
26-03 Repair trip hazards on the pool deck.
Failure to comply may affect renewal terms.
""")

core("C50", "lc-requirement-halberd", A("UK", "letter", "risk requirement letter"), """
Halberd Underwriting - Risk Requirement letter - Dunmore Cold Storage Ltd - Requirement 26/R1: ammonia detection to be linked to the ARC within 30 days, failing which cover for ammonia release will be suspended.
""")

core("C51", "acord25-cert", A("US", "pdf", "certificate of liability insurance"), """
ACORD 25 (2016/03)   CERTIFICATE OF LIABILITY INSURANCE    DATE (MM/DD/YYYY) 10/22/2026
THIS CERTIFICATE IS ISSUED AS A MATTER OF INFORMATION ONLY AND CONFERS NO RIGHTS UPON THE CERTIFICATE HOLDER.
PRODUCER: Pelham Strand Partners, 4410 N Ravenswood Ave, Chicago IL 60640
INSURED: Bellweather Roofing & Sheet Metal LLC, 1450 Commerce Dr, Lansing MI 48906
INSURER A: Corvid Mutual Insurance Company   NAIC # 99817
COMMERCIAL GENERAL LIABILITY   Policy CM-GL-2611408   11/01/2026   11/01/2027   EACH OCCURRENCE $1,000,000   GENERAL AGGREGATE $2,000,000
CERTIFICATE HOLDER: Lakeshore Medical Partners, 900 N Pine St, Lansing MI 48933
""")

core("C52", "payapp-continuation", A("US", "sheet", "construction pay application"), """
CONTINUATION SHEET - APPLICATION AND CERTIFICATE FOR PAYMENT
Project: Sorrel Creek Clubhouse Renovation    Application No. 6    Period to: 09/30/2026
Item | Description of Work | Scheduled Value | Work Completed Previous | This Period | % | Balance to Finish
1 | General conditions | $84,000 | $56,000 | $7,000 | 75% | $21,000
2 | Demolition | $22,500 | $22,500 | $0 | 100% | $0
3 | Roofing | $61,200 | $0 | $30,600 | 50% | $30,600
4 | Electrical | $48,300 | $19,320 | $9,660 | 60% | $19,320
""")

core("C53", "premium-finance-quillfeather", A("US", "pdf", "premium finance agreement"), """
PREMIUM FINANCE AGREEMENT - Quillfeather Premium Funding Co. - Insured: Bellweather Roofing & Sheet Metal LLC - Total premiums $38,720 - Down payment $9,680 - Amount financed $29,040 - 9 monthly installments of $3,359.16 - APR 9.75%
""")

# ---------------------------------------------------------------- boundary
# rule 9: supplementals
bnd("B1", "supp-wind-tidewater", A("US", "pdf", "habitational wind supplemental"), """
TIDEWATER COASTAL UNDERWRITERS (MGA)
Habitational Wind Supplemental - Florida & Gulf
Insured: Sorrel Creek Holdings LLC - Location: 1180 Gulf Breeze Pkwy, Pensacola FL 32507 (one building, 3 stories, 36 units)
1. Roof covering replaced within last 15 years?  Y / N   Year: ____
2. Roof-to-wall attachment:  Toe nails / Clips / Single wraps / Double wraps
3. Opening protection on all glazed openings?  Y / N
4. Secondary water resistance?  Y / N
5. Distance to coast (miles): ____
6. Any wind or flood loss in last 5 years?  Y / N   If yes, attach loss runs.
""", rule=9)

bnd("B2", "supp-panel-thistledown", A("UK", "pdf", "composite panel questionnaire"), """
THISTLEDOWN UNDERWRITING AGENCY
Composite Panel Supplementary Questionnaire (TUA-CP 2026)
Proposer: Dunmore Cold Storage Ltd    Premises: Dunmore Park, Selby YO8 4ER
Q1 Are any external walls or internal partitions of composite panel construction?  YES / NO
Q2 If yes, what % of total wall area?  ____%
Q3 Core type:  PIR / PUR / EPS / Mineral fibre / Unknown
Q4 Are panels LPCB LPS 1181 or FM 4880 approved?  YES / NO
Q5 Is hot work prohibited within 10 m of panels without a permit?  YES / NO
Q6 Are panel penetrations fire-stopped?  YES / NO
Declaration: I declare that the above statements are true and that I have not withheld any material fact.
""", rule=9)

bnd("B3", "supp-liquor-corvid", A("US", "pdf", "liquor liability supplement", "ocr"), """
CORVlD MUTUAL - LIQUOR LIABILITY SUPPLEMENT   Applicant: Upton Tavern Group LLC   1. Liquor receipts as % of total sales: ___   2. Are all servers certified in responsible alcohol service? Y/N   3. Live entertainment? Y/N   4. Open past 1 AM? Y/N
""", rule=9)

bnd("B4", "supp-epl-granite", A("US", "pdf", "EPL supplemental application"), """
GRANITE RIDGE CASUALTY COMPANY
EMPLOYMENT PRACTICES LIABILITY SUPPLEMENTAL APPLICATION    GRC-EPL-SUP (05/25)
THIS IS AN APPLICATION FOR A CLAIMS MADE POLICY. Complete in full and attach to ACORD 125.
Applicant: Ridgeback Plastics Inc.    Address: 2210 Industrial Pkwy, Dayton, OH 45414
Employees:  Full-time ___  Part-time ___  Seasonal ___  Independent contractors ___
Employees by state:  OH ___  IN ___  KY ___  Other ___
1. Does the applicant have a written employee handbook reviewed by counsel in the last 2 years?  Y / N
2. Is there a formal anti-harassment policy with annual training?  Y / N
3. Has the applicant had a reduction in force exceeding 10% in the last 24 months, or is one planned?  Y / N
4. Does the applicant use an outside HR consultant or PEO?  Y / N
5. Within the past 5 years, has any EEOC charge, state agency complaint or lawsuit been filed by a current or former employee?  Y / N
   If yes, complete the table:  Date | Allegation | Status | Paid | Reserve
6. Is any person proposed for this insurance aware of any fact, circumstance or situation that might reasonably give rise to a claim?  Y / N
FRAUD WARNING: Any person who knowingly and with intent to defraud any insurance company files an application containing any materially false information commits a fraudulent insurance act.
""", rule=9)

# rule 10: valuations with building schedule
bnd("B5", "valuation-ledbury", A("UK", "pdf", "insurance valuation report with schedule"), """
LEDBURY GRANGE CHARTERED SURVEYORS
Insurance Valuation Report - Calloway Foods Ltd
Prepared for: Calloway Foods Ltd and Orrin & Gale Insurance Brokers Ltd
Valuation date: 1 October 2026    Inspected: 24 September 2026
1. Instructions. We were instructed to provide reinstatement cost assessments of the freehold buildings for insurance purposes.
2. Basis. Reinstatement on a like for like basis using modern materials, including demolition, site clearance and professional fees of 13%, excluding VAT and loss of rent.
3. Summary of opinion. Total declared value for the portfolio: £14,200,000.
4. Limitations. No structural survey was undertaken. Areas are taken from drawings supplied and checked on site.
Appendix A - Building schedule
Ref | Site | Description | Construction | Storeys | GIA m2 | Reinstatement £
A1 | Bay 7, Fenland Way, Wisbech PE13 2RT | Production hall | Steel portal, composite panel | 1 | 5,200 | 7,280,000
A2 | Bay 7, Fenland Way, Wisbech PE13 2RT | Offices | Brick and block | 2 | 820 | 1,640,000
A3 | Unit 3, Saxon Road, King's Lynn PE30 4LT | Chilled distribution | Steel portal, composite panel | 1 | 3,900 | 5,280,000
Total | | | | | 9,920 | 14,200,000
""", rule=10)

bnd("B6", "appraisal-stonebridge", A("US", "pdf", "desktop appraisal update with exhibit"), """
STONEBRIDGE VALUATION GROUP, INC. - Insurable Value Update (Desktop) - Ridgeback Plastics Inc.
Purpose: trend the prior appraisal (2023) to current replacement cost for insurance placement. No site inspection.
Trend factor applied: 1.148 (cost index, 2023 Q3 to 2026 Q3).
Exhibit 1 - Building summary
Bldg | Description | Constr | Yr | Sq Ft | 2023 RCN | 2026 RCN
1 | Molding plant | JM | 1974 | 80,000 | $9,500,000 | $10,906,000
2 | Warehouse | JM | 1974 | 40,000 | $3,800,000 | $4,362,400
Total | | | | 120,000 | $13,300,000 | $15,268,400
""", rule=10)

bnd("B7", "valuation-cairnfield", A("UK", "pdf", "desktop RCA update", "ocr"), """
CAIRNFIELD SURVEYORS LLP   Desktop RCA update - Penhallow Textiles Ltd.  Index applied +4.2% (build cost index).  Appendix: Bldg 1 Weaving shed 4,100m2 £6,150,000 -> £6,408,300 | Bldg 2 Dye house 2,300m2 £3,220,000 -> £3,355,240.  Opinion valid 12 months.
""", rule=10)

bnd("B8", "appraisal-hollins", A("US", "pdf", "summary appraisal report with schedule"), """
HOLLINS & DRAKE APPRAISAL SERVICES
SUMMARY APPRAISAL REPORT - INSURABLE REPLACEMENT COST
Client: Bellweather Roofing & Sheet Metal LLC
Intended use: establishing property insurance limits. Intended users: the client and its insurance producer, Pelham Strand Partners.
Date of inspection: 09/12/2026    Effective date: 09/15/2026
The subject consists of a single-story pre-engineered metal building used as a roofing contractor's shop and office, with a detached storage shed. Replacement cost new was estimated by the segregated cost method and adjusted by local multipliers; exclusions (foundations below grade, site work, underground piping) have been deducted to arrive at insurable value.
SCHEDULE A - IMPROVEMENTS
Item | Address | Construction | Yr Built | Sq Ft | Sprinklered | RCN | Exclusions | Insurable Value
1 | 1450 Commerce Dr, Lansing MI 48906 | Non-combustible (ISO 3) | 2001 | 12,000 | N | $1,560,000 | $140,000 | $1,420,000
2 | 1450 Commerce Dr, Lansing MI 48906 | Frame (ISO 1) | 2011 | 1,800 | N | $162,000 | $12,000 | $150,000
Total | | | | 13,800 | | $1,722,000 | $152,000 | $1,570,000
Contents and equipment were not appraised.
""", rule=10)

# rule 11: presentations
bnd("B9", "presentation-pelham", A("US", "pdf", "marketing submission with values and loss table"), """
PELHAM STRAND PARTNERS - RIDGEBACK PLASTICS INC. - 2026-27 PROPERTY & CASUALTY MARKETING SUBMISSION
Section 3: Property Exposures
Ridgeback operates from one owned plant at 2210 Industrial Pkwy, Dayton OH. Values below are as reported by the insured and supported by a 2026 desktop appraisal.
Values summary: Building $15,268,400 | Machinery & equipment $11,400,000 | Stock $3,100,000 | Business income (12 mo) $8,500,000 | Total insured value $38,268,400
Section 5: Loss History (carrier loss runs valued 09/30/2026, enclosed)
Policy Yr | Claims | Paid | Reserve | Incurred
2021-22 | 1 | $12,400 | $0 | $12,400
2022-23 | 2 | $181,900 | $0 | $181,900
2023-24 | 0 | $0 | $0 | $0
2024-25 | 2 | $21,350 | $3,000 | $24,350
2025-26 | 1 | $42,500 | $96,000 | $138,500
Commentary: The 2022-23 year includes the Press 14 hydraulic fire. The open 2025-26 claim is a water damage loss from a failed chiller line; repairs are underway and the line has been replaced with stainless steel.
""", rule=11)

bnd("B10", "presentation-castlemere", A("UK", "pdf", "market presentation with claims experience"), """
CASTLEMERE RISK PARTNERS - Market Presentation - Upton Vale Hotels plc - Renewal 1 January 2027
Values summary (declared): Buildings £9,580,000 | Contents £1,350,000 | Loss of revenue (24 months) £4,200,000 | Total £15,130,000
Claims experience (5 years, insurer data to 30/09/2026):
Year | No. | Paid £ | Outstanding £ | Total £
2022 | 0 | 0 | 0 | 0
2023 | 1 | 3,480 | 0 | 3,480
2024 | 0 | 0 | 0 | 0
2025 | 1 | 11,200 | 0 | 11,200
2026 | 1 | 25,180 | 0 | 25,180
Our view: a well-run, low-frequency account; we are seeking a 5% reduction and removal of the flood excess at The Granary.
""", rule=11)

bnd("B11", "presentation-castlemere", A("UK", "pdf", "presentation page", "ocr"), """
CASTLEMERE RlSK PARTNERS  Market Presentation  p.4 of 22  Dunmore Cold Storage Ltd  TIV £27,450,000 (PD £18.45m, BI £9m)  Claims: 2 in 5 yrs, total incurred £61,300  see Appendix C for full loss listing
""", rule=11)

bnd("B12", "presentation-ferrousbay", A("US", "pdf", "habitational program submission"), """
FERROUS BAY INSURANCE SERVICES | Habitational Program Submission | Sorrel Creek Holdings LLC
Account overview: 2 garden-style communities, 116 units, owned since 2015; professional management by an affiliated company.
Schedule summary: Tulsa OK 80 units $11,400,000 | Pensacola FL 36 units $6,850,000 | Total TIV $18,250,000
Five year loss summary: 7 claims, $214,600 incurred, largest $88,000 (2024 wind, Pensacola). No liability losses over $10,000.
Requested: property $18.25M blanket, named storm sublimit $5M, GL $1M/$2M.
""", rule=11)

# rule 12: quotes with premium by location
bnd("B13", "quote-corvid", A("US", "pdf", "property quotation by location"), """
CORVID MUTUAL INSURANCE COMPANY - COMMERCIAL PROPERTY QUOTATION
Quote No. CMQ-26-30418    Named Insured: Sorrel Creek Holdings LLC    Term: 12/01/2026 - 12/01/2027
Loc | Address | Bldg Limit | BI Limit | Rate | Premium
1 | 7700 E 61st St, Tulsa OK 74133 | $11,400,000 | $250,000 | 0.520 | $60,580
2 | 1180 Gulf Breeze Pkwy, Pensacola FL 32507 | $6,850,000 | $150,000 | 1.940 | $135,800
Total premium $196,380. Wind deductible 5% at Loc 2. Terms valid 30 days; subject to wind mitigation inspection report for Loc 2.
""", rule=12)

bnd("B14", "quote-halberd", A("UK", "pdf", "quotation schedule by location"), """
HALBERD UNDERWRITING LIMITED
QUOTATION SCHEDULE - Property Owners - Quote ref HU-Q-26-55188
Insured: Upton Vale Hotels plc    Broker: Castlemere Risk Partners Ltd
Proposed period: 01/01/2027 to 31/12/2027
Premium by location
Loc | Premises | Buildings SI £ | Contents SI £ | LoR SI £ | Premium £
1 | The Granary, 12-14 Mill Lane, Ludlow | 6,420,000 | 900,000 | 2,800,000 | 24,960
2 | Coach House, 12 Mill Lane, Ludlow | 1,045,000 | 150,000 | 400,000 | 4,140
3 | Riverside Lodge, Teme Road, Ludlow | 2,115,000 | 300,000 | 1,000,000 | 12,100
Total | | 9,580,000 | 1,350,000 | 4,200,000 | 41,200
Excesses: £1,000 each and every loss; £10,000 flood at Loc 1 and 3.
IPT at 12% in addition. Commission 17.5%.
Subjectivities: 1. Completion of FRA action items at The Granary within 60 days. 2. Confirmation of annual kitchen extract cleaning.
This quotation is valid for 30 days and is subject to no material change in risk and no claims arising prior to inception.
""", rule=12)

bnd("B15", "indication-brightwater", A("US", "pdf", "inland marine quote", "ocr"), """
BRIGHTWATER SPECIALTY - QUOTE BSQ-77120 - Bellweather Roofing - Contractors Equipment.  Loc 1 Lansing yard $480,000 prem $3,360 | Loc 2 Grand Rapids yard $210,000 prem $1,470 | TOTAL $4,830
""", rule=12)

bnd("B16", "lead-quote-meridale", A("UK", "pdf", "lead quote by section and location"), """
MERIDALE 8871 - LEAD QUOTE - Dunmore Cold Storage Ltd
Section | Location | Sum insured GBP | Rate % | Premium GBP
PD | Dunmore Park, Selby | 18,450,000 | 0.400 | 73,800
BI | Dunmore Park, Selby | 9,000,000 | 0.430 | 38,700
Total 100% premium GBP 112,500. Line offered 35%. Quote valid until 15/11/2026. Ammonia refrigeration warranty applies.
""", rule=12)

# rule 16: MRC slips
bnd("B17", "mrc-slip-castlemere", A("UK", "pdf", "MRC slip excess liability"), """
MARKET REFORM CONTRACT
UMR: B2290CRP2600417
RISK DETAILS
TYPE: Excess Liability
INSURED: Ridgeback Plastics Inc., 2210 Industrial Pkwy, Dayton, OH 45414, USA
PERIOD: 1 December 2026 to 1 December 2027, both days at 12.01 a.m. Local Standard Time at the address of the Insured
INTEREST: Legal liability in excess of underlying insurances as scheduled
LIMIT OF LIABILITY: USD 10,000,000 each occurrence and in the aggregate, excess of USD 5,000,000
CONDITIONS: Follow form underlying; Nuclear Incident Exclusion; Sanctions clause
SUBJECTIVITIES: Copy of underlying policies within 30 days
INFORMATION: Per broker presentation dated 15 October 2026
PREMIUM: USD 54,000 (100%) annual
SECURITY DETAILS
INSURERS' LIABILITY: several not joint
Meridale Syndicate 8871   written line 25%   ref MS-EXL-2614
""", rule=16)

bnd("B18", "mrc-slip-meridale", A("UK", "pdf", "MRC slip fragment", "ocr"), """
UMR: B1874PSP2611206   RlSK DETAILS   TYPE: PD/BI   INSURED: Dunmore Cold Storage Ltd   PERIOD: 01/12/2026-30/11/2027   LIMIT: GBP 27,450,000 AOO   SUBJECTIVITIES: survey within 60 days
""", rule=16)

bnd("B19", "mrc-slip-orrin", A("UK", "pdf", "MRC slip commercial combined"), """
RISK DETAILS
UMR: B1874OGB2601893
TYPE: Commercial Combined (Material Damage, Business Interruption, Employers' and Public Liability)
INSURED: Calloway Foods Ltd
PERIOD: 01/12/2026 to 30/11/2027
INTEREST: Buildings, plant, stock and gross profit at the situations
SITUATION: 1. Bay 7, Fenland Way, Wisbech PE13 2RT; 2. Unit 3, Saxon Road, King's Lynn PE30 4LT
SUM INSURED: MD GBP 14,200,000; BI GBP 6,000,000; EL GBP 10,000,000; PL GBP 5,000,000
EXCESS: GBP 2,500 MD each and every loss
CONDITIONS: Composite Panel Condition; Electrical Inspection Condition
SUBJECTIVITIES: Completion of Halberd risk recommendation 25/02 within 60 days
""", rule=16)

# rule 18: ambiguous
bnd("B20", "ambig-values-premium-sheet", A("UK", "sheet", "values sheet with indicative premium"), """
Site | Address | Constr | Bldgs £ | Stock £ | GP £ | Total £ | Indic. prem £
Wisbech | Bay 7, Fenland Way, PE13 2RT | Steel/panel | 8,920,000 | 1,600,000 | 4,000,000 | 14,520,000 | 65,340
King's Lynn | Unit 3, Saxon Road, PE30 4LT | Steel/panel | 5,280,000 | 700,000 | 2,000,000 | 7,980,000 | 35,910
Totals | | | 14,200,000 | 2,300,000 | 6,000,000 | 22,500,000 | 101,250
Indicative premiums at 0.45%, not a quotation.
""", rule=18, label="sov", flags=["ambiguous"])

bnd("B21", "ambig-claims-page", A("UK", "pdf", "claims table page of unknown source"), """
Upton Vale Hotels plc - renewal 2027 - 7
Yr | No. claims | Incurred £ | Largest £
2022 | 0 | 0 | -
2023 | 1 | 3,480 | 3,480
2024 | 0 | 0 | -
2025 | 1 | 11,200 | 11,200
2026 | 1 | 25,180 | 25,180
Source: insurer data.
""", rule=18, label="loss_run", flags=["ambiguous"])

bnd("B22", "ambig-carrier-application-wrenfield", A("US", "pdf", "carrier application in ACORD field order"), """
WRENFIELD CASUALTY COMPANY - GENERAL APPLICATION WF-APP-1 (follows ACORD 125 field order; ACORD forms accepted in lieu)
APPLICANT: Bellweather Roofing & Sheet Metal LLC    FEIN: 38-4471920    SIC: 1761
MAILING ADDRESS: 1450 Commerce Dr, Lansing MI 48906
LINES REQUESTED: [X] General liability  [ ] Property  [X] Inland marine  [ ] Umbrella
PREMISES #1: 1450 Commerce Dr, Lansing MI - owned - 12,000 sq ft - 22 FT employees
PRIOR CARRIER (last 3 yrs): Corvid Mutual 2025-26, $36,900; Corvid Mutual 2024-25, $34,110
LOSS HISTORY: any claims in last 5 yrs?  Y / N    If yes, attach loss runs.
NATURE OF BUSINESS: commercial roofing and sheet metal; 70% commercial reroof, 30% new construction.
""", rule=18, label="acord", flags=["ambiguous"])

bnd("B23", "ambig-mga-bound-email", A("US", "email", "MGA binding confirmation email"), """
From: Ines Haldane <ihaldane@tidewatercoastal.com>
To: Rhiannon Duvall <rduvall@pelhamstrand.com>
Subject: RE: Sorrel Creek Holdings - Pensacola - BOUND
Rhiannon, confirmed we have bound coverage effective 12/01/2026 per our quote TCQ-4418: $6,850,000 building, 5% named storm deductible, premium $131,400. Formal binder to follow by end of day; please send the signed wind mitigation form and the updated SOV when you have them.
Thanks, Ines
""", rule=18, label="broker_email", flags=["ambiguous"])

# ---------------------------------------------------------------- contrast
con("P1", "C9", "sov", A("UK", "sheet", "schedule of insured values"), """
UPTON VALE HOTELS PLC
Schedule of Insured Values  |  Ref CS/26/3391  |  Valuation date 30 September 2026
Basis: reinstatement cost, day one, excluding VAT, fees at 12.5%, debris removal included.
Building | Address | Construction | Year built | GIA m2 | Reinstatement £
1 | The Granary, 12-14 Mill Lane, Ludlow SY8 1BB | Timber frame / brick, slate roof | c.1780 | 2,140 | 6,420,000
2 | Coach House, 12 Mill Lane, Ludlow SY8 1BB | Brick, slate roof | c.1820 | 380 | 1,045,000
3 | Riverside Lodge, Teme Road, Ludlow SY8 1PQ | Brick and block, tiled roof | 2004 | 960 | 2,115,000
Total | | | | 3,480 | 9,580,000
""")

con("P2", "C22", "acord", A("US", "pdf", "ACORD 140 property section"), """
ACORD 140 (2016/03)   PROPERTY SECTION
Applicant: Sorrel Creek Apartments LLC
Agency: Pelham Strand Partners, Chicago IL
Proposed Effective: 12/01/2026    Expiration: 12/01/2027
Premises #1: 7700 E 61st St, Tulsa, OK 74133 - 4 buildings, frame, garden apartments
Subject of insurance: Building $11,400,000 blanket; Business income with rents $250,000
Valuation: replacement cost    Causes of loss: special
Deductible: $25,000 AOP; 2% wind/hail
Construction type: ____  Year built: ____  Protection class: ____  Sprinklered: Y / N
""")

con("P3", "C47", "broker_email", A("US", "email", "broker submission email"), """
From: Rhiannon Duvall <rduvall@pelhamstrand.com>
To: Arjun Mehta <amehta@brightwaterspecialty.com>
Subject: Ridgeback Plastics - 12/1 renewal submission
Arjun,
Attached are the SOV, ACORD 125/140 and currently valued loss runs for Ridgeback's 12/1 renewal; we need terms by 11/10. One open claim to flag: water damage 08/14/2026 (GRC-26-118842). The adjuster has issued a first interim payment of $42,500 for mitigation and drying, and the current reserve is $96,000 for building repairs pending the contractor's estimate.
Regards,
Rhiannon Duvall, Senior Vice President, Pelham Strand Partners
""")

con("P4", "C18", "acord", A("US", "pdf", "ACORD 126 contractors section"), """
ACORD 126 (2016/09)   COMMERCIAL GENERAL LIABILITY SECTION
CONTRACTORS
Applicant: Bellweather Roofing & Sheet Metal LLC
1. Percentage of work:  Residential __%  Commercial __%  New construction __%  Remodel __%
2. Do you subcontract work?  Y / N   If yes, do you require certificates of insurance from all subs?  Y / N
3. Do you perform any work above 3 stories?  Y / N
4. Do you use torch-down or hot tar applications?  Y / N
5. Any work in New York State in the past 5 years?  Y / N
""")

con("P5", "C39", "loss_run", A("UK", "letter", "no known loss letter"), """
To whom it may concern,
We confirm that Quenby Bakeries Ltd has had no known losses or claims for the period 01/01/2021 to 14/10/2026.
Signed: Owen Pritchard, Director, Quenby Bakeries Ltd
""")

con("P6", "C29", "broker_email", A("UK", "email", "broker email quoting UMR"), """
From: Hugo Penrose <hpenrose@orringale.co.uk>
To: Petra Lindqvist <plindqvist@meridale8871.co.uk>
Subject: MRC ENDORSEMENT No. 2 - UMR B1874PSP2611206 - Dunmore Cold Storage Ltd
Petra, please agree additional premium GBP 4,250 for inclusion of Unit 9; revised schedule attached. Thanks, Hugo
""")

con("P7", "C51", "acord", A("US", "pdf", "ACORD 125 applicant section"), """
ACORD 125 (2016/03)   COMMERCIAL INSURANCE APPLICATION    DATE (MM/DD/YYYY) 10/22/2026
APPLICANT INFORMATION SECTION
AGENCY: Pelham Strand Partners, 4410 N Ravenswood Ave, Chicago IL 60640
APPLICANT: Bellweather Roofing & Sheet Metal LLC, 1450 Commerce Dr, Lansing MI 48906
CARRIER: Corvid Mutual Insurance Company   NAIC # 99817
LINES OF BUSINESS: COMMERCIAL GENERAL LIABILITY   PROPOSED EFF 11/01/2026   PROPOSED EXP 11/01/2027   EACH OCCURRENCE $1,000,000   GENERAL AGGREGATE $2,000,000
PREMISES INFORMATION: LOC 1   1450 Commerce Dr, Lansing MI 48906
""")

con("P8", "C10", "sov", A("US", "sheet", "statement of values"), """
SORREL CREEK APARTMENTS LLC
Statement of Values  -  Valuation basis: replacement cost new
Values as of: 08/01/2026
Location: 7700 E 61st St, Tulsa, OK 74133 - 4 garden-style apartment buildings
Bldg | Units | Construction | Yr Built | Sq Ft | RCN
A | 24 | Frame | 1998 | 22,800 | $3,420,000
B | 24 | Frame | 1998 | 22,800 | $3,420,000
C | 16 | Frame | 1999 | 15,200 | $2,280,000
D | 16 | Frame | 1999 | 15,200 | $2,280,000
Total | 80 | | | 76,000 | $11,400,000
""")

# ---------------------------------------------------------------- emit
ids = {}
n = 0
pair = 0
out = []
for r in rows:
    n += 1
    rid = f"A-other-{n:03d}"
    ids[r["key"]] = rid
for r in rows:
    words = len(r["text"].split())
    length = "short" if words <= 40 else ("medium" if words <= 120 else "long")
    attrs = dict(r["attrs"]); attrs["length"] = length
    if r["slice"] == "contrast":
        pair += 1
        group = next(x["group"] for x in rows if x["key"] == r["parent"])
    else:
        group = r["group"]
    out.append({
        "id": ids[r["key"]],
        "slice": r["slice"],
        "generator": "claude-opus-5.5",
        "generator_family": "A",
        "prompt_id": "a-other-v1",
        "attribute_cell": attrs,
        "template_group": f"gA:other:{group}",
        "generator_label": r["label"],
        "edge_rule": r["rule"],
        "expected_flags": r["flags"],
        "parent_id": ids[r["parent"]] if r["parent"] else None,
        "pair_id": f"P-other-{pair}" if r["slice"] == "contrast" else None,
        "text": r["text"],
    })
with open(OUT, "w", encoding="utf-8") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
print(len(out))
