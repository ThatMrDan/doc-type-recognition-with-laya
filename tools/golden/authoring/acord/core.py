# Core acord rows: (group_key, attrs, text)
CORE = [
# 1
("125-2016-03", {"market": "US", "state": "TX", "fill": "filled", "noise": "clean", "number_position": "footer_and_title"},
"""ACORD  COMMERCIAL INSURANCE APPLICATION   APPLICANT INFORMATION SECTION        DATE (MM/DD/YYYY) 03/14/2026
AGENCY: Corrigan Pike Insurance Agency, 4410 Gessner Rd Ste 210, Houston, TX 77041   CONTACT NAME: Marisol Ortega   PHONE (A/C, No, Ext): (713) 555-0148
CARRIER: Granite Shoals Mutual Ins Co   NAIC CODE: 30417   COMPANY POLICY OR PROGRAM NAME: Contractors Package
STATUS OF TRANSACTION: [X] QUOTE  [ ] ISSUE POLICY  [ ] BOUND (Give Date and/or Attach Copy)
LINES OF BUSINESS: [X] COMMERCIAL GENERAL LIABILITY  [X] BUSINESS AUTO  [X] UMBRELLA  [ ] PROPERTY
NAME (First Named Insured) AND MAILING ADDRESS: Delgado Brothers Concrete LLC, 1802 Aldine Bender Rd, Houston, TX 77032
GL CODE 91560   SIC 1771   NAICS 238110   FEIN 76-4410932   [X] LLC
PROPOSED EFF DATE 05/01/2026   PROPOSED EXP DATE 05/01/2027   BILLING PLAN: [X] AGENCY  PAYMENT PLAN: QUARTERLY
ACORD 125 (2016/03)                                    Page 1 of 4"""),
# 2
("125-2016-03", {"market": "US", "state": "OH", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 125 (2016/03) COMMERCIAL INSURANCE APPLICATION
DATE: 08/02/2026  AGENCY: Bluestem Risk Partners, Dayton OH
APPLICANT: Sable Creek Brewing Co   FEIN: ________   EFF DATE: 09/15/2026
LINES: [X] PROPERTY [X] GL [ ] AUTO"""),
# 3
("125-2016-03", {"market": "US", "state": "GA", "fill": "filled", "noise": "ocr", "number_position": "not_after_word"},
"""C0MMERCIAL lNSURANCE APPLlCATION     APPLICANT INF0RMATION SECTI0N
DATE (MM/DD/YYYY) 1O/06/2026   AGENCY Halvorsen & Dube Agency 2290 Peachtree Ind Blvd, Duluth GA 3OO96
CARRlER Prairie Lantern Casualty   NAlC C0DE 2 4 1 8 8   P0LICY NUMBER  pending
STATUS 0F TRANSACTI0N  [X] QU0TE   [ ] ISSUE P0LICY
NAME (First Named lnsured) Okafor Family Dental PLLC  MAlLING ADDRESS 515 Satellite Blvd NW Ste 4, Suwanee GA 30024
BUSlNESS PH0NE (678) 555-O277   WEBSITE okaforsmiles.example
SIC 8021  NAICS 621210  FEIN 58-339O114   [X] C0RP0RATION   [ ] PARTNERSHIP
NATURE 0F BUSINESS: [X] OFFICE   DESCRIPTI0N 0F 0PERATI0NS  General dentistry, 2 dentists, 9 staff
ACORD C0RP0RATION. All rights reserved.            FORM 125 (2016/03)     Pg 1 of 4"""),
# 4
("125-2014-12", {"market": "US", "state": "NJ", "fill": "filled", "noise": "caps", "number_position": "title_and_footer"},
"""ACORD 125 (2014/12)   COMMERCIAL INSURANCE APPLICATION
DATE 02/20/2026   AGENCY: TRI-COUNTY UNDERWRITING SERVICES INC, 77 ROUTE 17 N, PARAMUS NJ 07652   CONTACT: GERALD WHITCOMB   E-MAIL: GWHITCOMB@TRICOUNTYUW.EXAMPLE
CARRIER: IRONWOOD SPECIALTY INSURANCE CO   NAIC: 41092   UNDERWRITER: TERESA NAKAMURA
STATUS OF TRANSACTION: [X] QUOTE  [ ] BOUND
INDICATE SECTIONS ATTACHED: [X] COMMERCIAL GENERAL LIABILITY  [X] COMMERCIAL PROPERTY  [X] BUSINESS AUTO  [ ] CRIME  [ ] UMBRELLA
APPLICANT: HUTCHINS MECHANICAL INC   MAILING ADDRESS: 640 RIVER DR, GARFIELD NJ 07026   FEIN 22-3087745   SIC 1711   NAICS 238220   [X] CORPORATION
PREMISES INFORMATION: LOC 1 BLDG 1  640 RIVER DR, GARFIELD NJ 07026   [X] INSIDE CITY LIMITS   INTEREST: [X] OWNER   # FULL TIME EMPL 34   ANNUAL REVENUES $8,400,000   OCCUPIED AREA 18,000 SQ FT
NATURE OF BUSINESS: [X] CONTRACTOR   DESCRIPTION OF PRIMARY OPERATIONS: HVAC AND PLUMBING INSTALLATION AND SERVICE, COMMERCIAL 70% / RESIDENTIAL 30%
PRIOR CARRIER INFORMATION   YEAR 2025  CARRIER: COBALT RIDGE INDEMNITY  POLICY # CRG-GL-5521087  PREMIUM $41,220   YEAR 2024  SAME  PREMIUM $38,900
LOSS HISTORY (ENTER ALL CLAIMS OR LOSSES REGARDLESS OF FAULT FOR THE LAST 5 YEARS)  [ ] CHECK IF NONE
DATE OF OCCURRENCE 07/11/2024  LINE: GL  DESCRIPTION: WATER DAMAGE AT CLIENT SITE, FAILED FITTING   AMOUNT PAID $18,400   AMOUNT RESERVED $0   CLAIM STATUS: CLOSED
ACORD 125 (2014/12)                                                    PAGE 1 OF 4"""),
# 5
("125-2014-12", {"market": "US", "state": "WA", "fill": "partial", "noise": "clean", "number_position": "footer"},
"""COMMERCIAL INSURANCE APPLICATION — APPLICANT INFORMATION SECTION
Date 06/30/2026   Agency: Pinecrest Brokerage LLC, Tacoma WA   Contact: Hollis Brandt
Carrier: (to be determined)   Status of transaction: [X] Quote
Lines of business: [X] Commercial property  [X] Commercial general liability
First named insured: Lakeshore Pallet Recovery Inc, 3315 S Tacoma Way, Tacoma WA 98409
FEIN: 91-______   Entity: [X] Corporation   Proposed eff date: 08/01/2026
Contact information: Accounting  Name: Femi Adeyemi  Phone: (253) 555-0631
ACORD 125 (2014/12)   Page 1 of 4"""),
# 6
("125-2022-10", {"market": "US", "state": "CO", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 125 (2022/10) Commercial Insurance Application. Applicant: Ruiz Lumber & Truss Inc, Greeley CO. Eff 04/01/2026. Lines: CGL, Property, Auto. Agency: Front Range Mutual Agency. Prior carrier: none listed."""),
# 7
("125-2022-10", {"market": "US", "state": "FL", "fill": "filled", "noise": "clean", "number_position": "not_after_word"},
"""ACORD®
COMMERCIAL INSURANCE APPLICATION
DATE (MM/DD/YYYY) 11/03/2026
AGENCY  Gulfbreeze Commercial Insurance Group, 1200 W Platt St, Tampa, FL 33606   NAIC CODE —   AGENCY CUSTOMER ID 004417
CARRIER  Silver Fen Assurance Co    COMPANY POLICY OR PROGRAM NAME  Hospitality Select
STATUS OF TRANSACTION  [X] QUOTE  [ ] ISSUE POLICY  [ ] RENEW
LINES OF BUSINESS  [X] COMMERCIAL GENERAL LIABILITY  [X] LIQUOR LIABILITY  [X] COMMERCIAL PROPERTY
APPLICANT INFORMATION  Pelican Wharf Grill LLC, 88 Bayshore Dr, Clearwater, FL 33767   FEIN 59-2211804   SIC 5812   NAICS 722511   [X] LLC
PROPOSED EFF DATE 01/01/2027   PROPOSED EXP DATE 01/01/2028
Form 125 (2022/10)      Page 1 of 4"""),
# 8
("125-2007-10", {"market": "US", "state": "PA", "fill": "partial", "noise": "ocr", "number_position": "title"},
"""ACORD 125 (2007/10)  COMMERClAL lNSURANCE APPLlCATlON  APPLlCANT: Pemberton Farms Market, Lancaster PA  EFF: 03/01/2026  AGENCY: Conestoga Valley lns  [X] PROPERTY [X] GL  page 1 of 4"""),
# 9
("126-2016-09", {"market": "US", "state": "IL", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 126 (2016/09)   COMMERCIAL GENERAL LIABILITY SECTION      DATE 04/07/2026
AGENCY: Prairie Gate Insurance Services, Naperville IL   CARRIER: Cobalt Ridge Indemnity   NAIC 30881
APPLICANT: Kowalczyk Tool & Die Co   EFFECTIVE DATE 06/01/2026
COVERAGES   LIMITS   [X] COMMERCIAL GENERAL LIABILITY  [X] OCCURRENCE  [ ] CLAIMS MADE
GENERAL AGGREGATE $2,000,000   PRODUCTS & COMPLETED OPERATIONS AGGREGATE $2,000,000   EACH OCCURRENCE $1,000,000   PERSONAL & ADVERTISING INJURY $1,000,000   DAMAGE TO RENTED PREMISES $100,000   MEDICAL EXPENSE $5,000
DEDUCTIBLES: [X] PROPERTY DAMAGE $1,000  [ ] BODILY INJURY
SCHEDULE OF HAZARDS   LOC # 1  HAZ # 1  CLASSIFICATION: Metal goods mfg NOC   CLASS CODE 57001   PREMIUM BASIS (S) GROSS SALES   EXPOSURE $11,250,000   TERR 003
LOC # 1  HAZ # 2  CLASSIFICATION: Tool and die shops  CLASS CODE 59914   PREMIUM BASIS (P) PAYROLL   EXPOSURE $2,870,000
ACORD 126 (2016/09)    Page 1 of 4"""),
# 10
("126-2016-09", {"market": "US", "state": "MN", "fill": "partial", "noise": "caps", "number_position": "title"},
"""ACORD 126 (2016/09) COMMERCIAL GENERAL LIABILITY SECTION   APPLICANT: NORTHFORK COLD STORAGE INC, ST CLOUD MN   EACH OCCURRENCE $1,000,000   GEN AGG $2,000,000   HAZARDS: SEE ATTACHED"""),
# 11
("126-2016-09", {"market": "US", "state": "AZ", "fill": "filled", "noise": "ocr", "number_position": "title"},
"""ACORD 126 (2O16/O9)         C0MMERCIAL GENERAL LIABlLITY SECTI0N             DATE (MM/DD/YYYY) O5/19/2026
AGENCY  Saguaro Point lnsurance Brokers, 7th St & Camelback, Phoenix AZ 85014        CARRIER  Ironwood Specialty lns Co      NAIC C0DE 41O92
P0LICY NUMBER  (new)       APPLICANT  Desert Arc Welding & Fabrication LLC      EFFECTIVE DATE  O7/O1/2026
C0VERAGES          LlMITS
[X] C0MMERCIAL GENERAL LlABILITY          GENERAL AGGREGATE  $ 2,OOO,OOO
[ ] CLAIMS MADE  [X] 0CCURRENCE           PR0DUCTS & C0MPLETED 0PERATI0NS AGGREGATE  $ 2,OOO,OOO
[X] 0WNER'S & C0NTRACT0R'S PR0TECTIVE      PERS0NAL & ADVERTISING lNJURY  $ 1,OOO,OOO
                                           EACH 0CCURRENCE  $ 1,OOO,OOO
                                           DAMAGE T0 RENTED PREMISES (each occurrence)  $ 1OO,OOO
                                           MEDlCAL EXPENSE (Any one person)  $ 5,OOO
LlMIT APPLIES PER: [X] P0LICY  [ ] L0CATI0N  [ ] PR0JECT
SCHEDULE 0F HAZARDS
L0C #  HAZ #  CLASSIFICATI0N                       CLASS C0DE  PREMIUM BASIS  EXP0SURE     TERR
1      1      Welding or cutting NOC               99987       P              $1,14O,OOO   O14
1      2      Machine shops NOC                    97OO3       S              $3,6OO,OOO   O14
CLAlMS MADE: proposed retro date  N/A      EMPL0YEE BENEFITS LIABILITY: [ ] Y  [X] N
ACORD 126 (2O16/O9)                                        Page 1 of 4"""),
# 12
("126-2014-04", {"market": "US", "state": "NC", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 126 (2014/04)  COMMERCIAL GENERAL LIABILITY SECTION
Applicant: Blue Ridge Event Rentals LLC, 410 Hendersonville Rd, Asheville NC 28803   Effective date: 07/15/2026
Agency: Cardinal Trace Agency   Carrier: Prairie Lantern Casualty
Coverage: [X] Occurrence   Each occurrence $1,000,000   General aggregate $2,000,000   Products/completed ops agg $2,000,000
Schedule of hazards: Loc 1 Haz 1  Party equipment rental, class 16471, basis (S) gross sales $1,925,000
Contractors: Does applicant subcontract work? [X] N   Products: Does applicant install, service or demonstrate products? [X] Y
ACORD 126 (2014/04)   Page 1 of 4"""),
# 13
("126-2014-04", {"market": "US", "state": "VT", "fill": "partial", "noise": "clean", "number_position": "not_after_word"},
"""COMMERCIAL GENERAL LIABILITY SECTION. Applicant: Maple Hollow Sugarworks LLC, Montpelier VT. Each occurrence $1,000,000. Schedule of hazards: maple syrup processing, sales basis. ACORD — form 126 (2014/04), page 1 of 4."""),
# 14
("127-2015-12", {"market": "US", "state": "TN", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 127 (2015/12)  BUSINESS AUTO SECTION     DATE 01/22/2026
AGENCY: Volunteer Crossing Insurance, Knoxville TN   CARRIER: Granite Shoals Mutual   NAIC 30417
APPLICANT: Tennessee Valley Landscape Supply LLC   EFFECTIVE DATE 03/01/2026
DRIVER INFORMATION (attach ACORD 163 if more space needed)
#  NAME                 CITY        ST  DOB         LIC #        ST  YR LIC  % USE
1  Dwayne Kessler       Maryville   TN  03/11/1979  D104477218  TN  1995    60
2  Luis Arce            Knoxville   TN  09/02/1988  D220913340  TN  2006    40
GENERAL INFORMATION: Any vehicles owned but not scheduled? N   Any drivers not covered by WC? N   Any vehicles used by family members? N
ACORD 127 (2015/12)   Page 1 of 4"""),
# 15
("127-2015-12", {"market": "US", "state": "KY", "fill": "partial", "noise": "ocr", "number_position": "title"},
"""ACORD 127 (2O15/12) BUSlNESS AUT0 SECTI0N  APPLlCANT  Bluegrass Mobile Notary Svcs  DRIVER 1  Colleen Barrow  L0UISVILLE KY  % USE 1OO"""),
# 16
("127-2020-03", {"market": "US", "state": "MO", "fill": "filled", "noise": "clean", "number_position": "title_and_footer"},
"""ACORD 127 (2020/03)   BUSINESS AUTO SECTION                                         DATE (MM/DD/YYYY) 09/09/2026
AGENCY: Show-Me Commercial Risk LLC, 1100 Main St Ste 900, Kansas City, MO 64105            AGENCY CUSTOMER ID: 21-0098
CARRIER: Cobalt Ridge Indemnity     NAIC CODE: 30881     POLICY NUMBER: (new business)     EFFECTIVE DATE: 11/01/2026
APPLICANT: Heartland Mobile Shredding Inc
DRIVER INFORMATION
#  FIRST NAME  LAST NAME   CITY OF RESIDENCE  ST  DATE OF BIRTH  SEX  MAR STAT  LICENSE #     ST  YR LIC  % USE  VEH #
1  Margot      Hensley     Independence       MO  07/19/1983     F    M         M550311002   MO  2000    100    1
2  Curtis      Okonjo      Blue Springs       MO  12/02/1990     M    S         M619004417   MO  2008    100    2
3  Rafael      Benitez     Overland Park      KS  05/28/1976     M    M         K03-77-4410  KS  1993    100    3
GENERAL INFORMATION  (explain all "yes" responses)
1. Is applicant a subsidiary of another entity?  N
2. Any vehicles leased to others?  N
3. Any operations involve transporting hazardous material?  N
4. Any hold harmless agreements?  Y  (client service contracts, see remarks)
5. Is there a vehicle maintenance program in operation?  Y
6. Are MVRs obtained on all drivers?  Y, annually
ACORD 127 (2020/03)                                              Page 1 of 4"""),
# 17
("129-2014-04", {"market": "US", "state": "TX", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 129 (2014/04) VEHICLE SCHEDULE   Applicant: Delgado Brothers Concrete LLC   Eff 05/01/2026
VEH # | YEAR | MAKE | MODEL | BODY TYPE | V.I.N. | GVW | GARAGING ZIP | COST NEW | USE
1 | 2021 | Kenworth | T880 | Mixer | 1NKZX4TX4MJ411002 | 66,000 | 77032 | $214,500 | Commercial
2 | 2019 | Ford | F-350 | Pickup | 1FT8W3BT7KED30117 | 11,500 | 77032 | $58,900 | Service
3 | 2023 | Mack | Granite | Dump | 1M2GR4GC5PM028851 | 72,000 | 77032 | $189,000 | Commercial
Symbols: Liab 1  Comp 7  Coll 7   Radius: local under 50 mi
ACORD 129 (2014/04) Page 1 of 2"""),
# 18
("129-2014-04", {"market": "US", "state": "WI", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 129 (2014/04) VEHICLE SCHEDULE. Veh 1: 2020 Freightliner M2 box truck, VIN 3ALACWFC1LD300218, garaged Green Bay WI 54304, cost new $96,400. Veh 2: blank."""),
# 19
("129-2009-08", {"market": "US", "state": "OK", "fill": "filled", "noise": "caps", "number_position": "footer"},
"""VEHICLE SCHEDULE   APPLICANT: RED DIRT OILFIELD HOTSHOT LLC   AGENCY: CIMARRON LINE INSURANCE   EFFECTIVE 02/01/2026
VEH # 1  YR 2022  MAKE RAM  MODEL 5500  BODY FLATBED  VIN 3C7WRNFL4NG118804  GVW 19,500  COST NEW $81,200  GARAGE ZIP 73644  RADIUS 200 MI  USE COMMERCIAL
VEH # 2  YR 2018  MAKE CHEVROLET  MODEL 3500HD  BODY PICKUP  VIN 1GC4K0EY0JF201733  GVW 13,025  COST NEW $52,700  GARAGE ZIP 73644  RADIUS 200 MI
COVERAGES PER VEHICLE: LIAB [X]  MED PAY [ ]  PIP [ ]  UM [X]  COMP DED $1,000  COLL DED $1,000
ACORD 129 (2009/08)  PAGE 1 OF 2"""),
# 20
("130-2017-11", {"market": "US", "state": "CA", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 130 (2017/11)   WORKERS COMPENSATION APPLICATION        DATE 07/08/2026
AGENCY: Coastline Mesa Insurance Services, 2400 E Katella Ave, Anaheim CA 92806   PRODUCER: Priyanka Desai
COMPANY: Silver Fen Assurance Co   UNDERWRITER: (open)
STATUS OF SUBMISSION: [X] QUOTE  [ ] ISSUE POLICY   BILLING PLAN: [X] DIRECT  PAYMENT PLAN: [X] MONTHLY  AUDIT: [X] ANNUAL
APPLICANT NAME: Orange Grove Commissary Kitchens Inc   MAILING ADDRESS: 12850 Harbor Blvd, Garden Grove CA 92840
YRS IN BUS: 11   SIC 2099   NAICS 311991   FEDERAL EMPLOYER ID 33-0871562   [X] CORPORATION
PROPOSED EFF DATE 09/01/2026   NORMAL ANNIVERSARY RATING DATE 09/01
PART 1 WORKERS COMPENSATION (States): CA   PART 2 EMPLOYERS LIABILITY: $1,000,000 EACH ACCIDENT / $1,000,000 DISEASE POLICY LIMIT / $1,000,000 DISEASE EACH EMPLOYEE
STATE RATING WORKSHEET  LOC 1  CLASS CODE 2501  DESCR: Food preparation  # EMPL FT 42 PT 6  ESTIMATED ANNUAL REMUNERATION $2,310,000
ACORD 130 (2017/11)   Page 1 of 4"""),
# 21
("130-2017-11", {"market": "US", "state": "MA", "fill": "filled", "noise": "clean", "number_position": "title_and_footer"},
"""ACORD 130 (2017/11)                WORKERS COMPENSATION APPLICATION                 DATE (MM/DD/YYYY) 12/01/2026
AGENCY                                         COMPANY
Harborlight Insurance Agency Inc               Prairie Lantern Casualty
33 Washington St, Salem MA 01970               NAIC CODE 24188
PRODUCER NAME: Brendan Fitzhugh  CSR: Odile Marchand  PHONE (978) 555-0402
APPLICANT NAME: Merrimack Precision Plating Co      OFFICE PHONE (978) 555-0817
MAILING ADDRESS: 9 Industrial Way, Haverhill MA 01832      YRS IN BUS: 27      SIC 3471  NAICS 332813
[X] CORPORATION  [ ] PARTNERSHIP  [ ] LLC   FEDERAL EMPLOYER ID 04-2219087   NCCI RISK ID 220419875   RATING BUREAU ID —
STATUS OF SUBMISSION: [X] QUOTE  [ ] BOUND    BILLING PLAN [X] AGENCY BILL   PAYMENT PLAN [X] QUARTERLY   AUDIT [X] ANNUAL
LOCATIONS   # 1  9 Industrial Way, Haverhill MA 01832   # 2  14 Ward Hill Ave, Haverhill MA 01835
POLICY INFORMATION   PROPOSED EFF DATE 01/01/2027   PROPOSED EXP DATE 01/01/2028   NORMAL ANNIVERSARY RATING DATE 01/01
PARTICIPATING [ ]  NON-PARTICIPATING [X]   RETRO PLAN: none
PART 1 WORKERS COMPENSATION (States): MA    PART 2 EMPLOYER'S LIABILITY  $500,000 EACH ACCIDENT  $500,000 DISEASE-POLICY LIMIT  $500,000 DISEASE-EACH EMPLOYEE
PART 3 OTHER STATES INS: NH, ME     DEDUCTIBLES: none     OTHER COVERAGES: [X] U.S.L.&H. [ ] VOLUNTARY COMP
RATING INFORMATION   LOC 1  CLASS CODE 3372  DESCRIPTION Electroplating   FULL TIME 38  PART TIME 2   ESTIMATED ANNUAL REMUNERATION $2,145,000   RATE 4.11   EST ANNUAL MANUAL PREMIUM $88,160
LOC 2  CLASS CODE 8810  DESCRIPTION Clerical office employees NOC   FULL TIME 6  PART TIME 0   ESTIMATED ANNUAL REMUNERATION $412,000   RATE 0.09   EST ANNUAL MANUAL PREMIUM $371
ACORD 130 (2017/11)                                                                  Page 1 of 4"""),
# 22
("130-2013-09", {"market": "US", "state": "IN", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 130 (2013/09) WORKERS COMPENSATION APPLICATION. Applicant: Wabash Bend Millwork LLC, Terre Haute IN. Part 1 states: IN. Class 2802, payroll $640,000. Eff 10/01/2026."""),
# 23
("130-2013-09", {"market": "US", "state": "LA", "fill": "filled", "noise": "ocr", "number_position": "footer"},
"""W0RKERS C0MPENSATI0N APPLlCATI0N        DATE O3/O3/2026
AGENCY  Bayou Teche lnsurance Agency, Lafayette LA 7O5O3       C0MPANY  Cobalt Ridge lndemnity
APPLlCANT NAME  Atchafalaya Marine Electric lnc   MAlLING ADDRESS  2O8 Rue Jolie, Broussard LA 7O518
FEDERAL EMPL0YER lD  72-1188O45   NCCI RlSK lD  —   [X] C0RP0RATI0N
PART 1 W0RKERS C0MPENSATI0N (States)  LA     PART 2 EMPL0YERS LlABILITY  $1,OOO,OOO / $1,OOO,OOO / $1,OOO,OOO
0THER C0VERAGES  [X] U.S.L.&H.  [X] MARlTIME (Jones Act)   L0C 1  CLASS 6834  B0at building  EST ANNUAL REMUNERATl0N $1,22O,OOO
ACORD 130 (2O13/O9)  Page 1 of 4"""),
# 24
("131-2016-04", {"market": "US", "state": "NV", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 131 (2016/04)  UMBRELLA / EXCESS SECTION     DATE 02/11/2026
AGENCY: High Desert Risk Advisors, Henderson NV   CARRIER: Ironwood Specialty Insurance Co
APPLICANT: Silver State Hospitality Group LLC   EFFECTIVE DATE 04/01/2026
POLICY INFORMATION: [X] UMBRELLA  [ ] EXCESS   [X] OCCURRENCE   LIMIT OF LIABILITY EACH OCCURRENCE $10,000,000   AGGREGATE $10,000,000   SELF-INSURED RETENTION $10,000
EMPLOYEE BENEFITS: [ ] Y  [X] N
PRIMARY LOCATION AND SUBSIDIARIES: 1 - 4100 Paradise Rd, Las Vegas NV (hotel, 212 rooms)   2 - 31 Water St, Henderson NV (restaurant)
UNDERLYING INSURANCE: GL $1M/$2M Silver Fen Assurance; Auto CSL $1M Granite Shoals Mutual; EL $1M/$1M/$1M
ACORD 131 (2016/04)   Page 1 of 5"""),
# 25
("131-2016-04", {"market": "US", "state": "SC", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 131 (2016/04) Umbrella/Excess Section. Applicant: Lowcountry Roofing Co, Charleston SC. Requested limit $5,000,000 each occurrence, SIR $10,000. Underlying schedule: to follow."""),
# 26
("131-2009-10", {"market": "US", "state": "MI", "fill": "filled", "noise": "caps", "number_position": "footer"},
"""UMBRELLA / EXCESS SECTION   DATE 08/14/2026
AGENCY: GREAT LAKES LANTERN AGENCY, GRAND RAPIDS MI   CARRIER: SILVER FEN ASSURANCE CO
APPLICANT: KALAMAZOO RIVER PLASTICS INC   EFFECTIVE DATE 10/01/2026
POLICY INFORMATION: [ ] UMBRELLA  [X] EXCESS   LIMIT $5,000,000 EACH OCCURRENCE / $5,000,000 AGGREGATE   RETAINED LIMIT $0
UNDERLYING INSURANCE   AUTO: CSL $1,000,000   GL: $1,000,000 EACH OCC / $2,000,000 AGG / $2,000,000 PRODUCTS   EMPLOYERS LIABILITY: $500,000 / $500,000 / $500,000
ACORD 131 (2009/10)   PAGE 1 OF 5"""),
# 27
("137ca-2016-10", {"market": "US", "state": "CA", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 137 CA (2016/10)   COMMERCIAL AUTO   CALIFORNIA STATE SPECIFIC COVERAGES
Applicant: Central Valley Produce Haulers LLC, Fresno CA   Effective date 06/01/2026   Agency: San Joaquin Ridge Insurance
UNINSURED MOTORISTS: [X] Bodily injury limit $1,000,000 CSL   UM property damage: [X] Yes, limit $3,500
UNDERINSURED MOTORISTS: included with UM BI
MEDICAL PAYMENTS: $5,000 each person
Symbols: UM 2   Med pay 2
Rejection or selection of lower limits signed by named insured: [ ] Attached
ACORD 137 CA (2016/10)  Page 1 of 1"""),
# 28
("137ny-2016-10", {"market": "US", "state": "NY", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 137 NY (2016/10) COMMERCIAL AUTO - NEW YORK STATE SPECIFIC COVERAGES. Applicant: Hudson Rail Courier Inc. Basic PIP (no-fault) $50,000. Additional PIP: [ ]. SUM: $1,000,000."""),
# 29
("137tx-2017-06", {"market": "US", "state": "TX", "fill": "filled", "noise": "clean", "number_position": "not_after_word"},
"""ACORD
BUSINESS AUTO  TEXAS STATE SPECIFIC COVERAGES
APPLICANT: Delgado Brothers Concrete LLC      EFFECTIVE DATE 05/01/2026      AGENCY: Corrigan Pike Insurance Agency
PERSONAL INJURY PROTECTION: [X] Basic $2,500 each person   [ ] Rejected in writing
UNINSURED / UNDERINSURED MOTORISTS: [X] BI and PD  Limit $1,000,000 CSL   PD deductible $250
TOWING AND LABOR: [ ] Not applicable to heavy trucks
Symbols:  PIP 5   UM/UIM 6
Rejection forms attached for: none
Form 137 TX (2017/06)          Page 1 of 1"""),
# 30
("140-2014-12", {"market": "US", "state": "OR", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 140 (2014/12) PROPERTY SECTION   DATE 05/05/2026
AGENCY: Willamette Crest Insurance, Salem OR   CARRIER: Granite Shoals Mutual   APPLICANT: Cascade Foothill Veterinary Clinic PC   EFF 07/01/2026
PREMISES #: 1  STREET ADDRESS: 2275 Lancaster Dr NE, Salem OR 97305   BLDG #: 1
SUBJECT OF INSURANCE: Building   AMOUNT $1,850,000   COINS 90%   VALUATION RC   CAUSE OF LOSS: Special   DED $2,500
SUBJECT OF INSURANCE: Business personal property   AMOUNT $420,000   COINS 80%   VALUATION RC   CAUSE OF LOSS: Special
CONSTRUCTION TYPE: Joisted masonry   # STORIES 1   YEAR BUILT 1998   TOTAL AREA 7,600 SQ FT   PROTECTION CLASS 3   SPRINKLERED: N   BURGLAR ALARM: Central station
ACORD 140 (2014/12)   Page 1 of 3"""),
# 31
("140-2014-12", {"market": "US", "state": "CT", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 140 (2014/12) PROPERTY SECTION. Applicant: Quinnipiac Bindery LLC. Premises 1, 60 Hamilton St, New Haven CT. Building: not insured (tenant). BPP $275,000, special form, RC."""),
# 32
("140-2014-12", {"market": "US", "state": "MS", "fill": "filled", "noise": "ocr", "number_position": "footer"},
"""PR0PERTY SECTI0N        DATE (MM/DD/YYYY) O9/22/2026
AGENCY  Magnolia Delta lnsurance Group, Jackson MS        CARRlER  Prairie Lantern Casualty
APPLlCANT  Pearl River Seed & Feed lnc        EFFECTlVE DATE  11/O1/2026
PREMlSES # 1   STREET ADDRESS  4O1 Hwy 49 S, Florence MS 39O73     BLDG # 1
SUBJECT 0F INSURANCE  Building   AM0UNT $96O,OOO   C0INS % 8O   VALUATI0N  ACV   CAUSE 0F L0SS  Basic   DED $5,OOO
C0NSTRUCTI0N  Metal on steel frame (non-combustible)   YR BUlLT 1986   ST0RIES 1   AREA 14,2OO   PR0T CL 6   WlND/HAlL DED 2%
ACORD 140 (2014/12) Page 1 of 3"""),
# 33
("140-2016-03", {"market": "US", "state": "VA", "fill": "filled", "noise": "caps", "number_position": "title_and_footer"},
"""ACORD 140 (2016/03)                       PROPERTY SECTION                         DATE (MM/DD/YYYY) 03/27/2026
AGENCY: TIDEWATER BEACON INSURANCE AGENCY, NORFOLK VA          CARRIER: SILVER FEN ASSURANCE CO          NAIC 40155
APPLICANT: ELIZABETH RIVER MARINE SUPPLY INC          POLICY NUMBER: NEW          EFFECTIVE DATE: 06/01/2026
PREMISES #: 1   STREET ADDRESS: 1300 GRANBY ST, NORFOLK VA 23510   BLDG #: 1   BLDG DESCRIPTION: RETAIL STORE AND WAREHOUSE
SUBJECT OF INSURANCE: BUILDING   AMOUNT: $2,600,000   COINS %: 90   VALUATION: RC   CAUSES OF LOSS: SPECIAL   INFLATION GUARD %: 4   DED: $5,000   DED TYPE: $   BLANKET #: —   FORMS AND CONDITIONS TO APPLY: CP 00 10
SUBJECT OF INSURANCE: BUSINESS PERSONAL PROPERTY   AMOUNT: $1,150,000   COINS %: 80   VALUATION: RC   CAUSES OF LOSS: SPECIAL   DED: $5,000
SUBJECT OF INSURANCE: BUSINESS INCOME W/ EXTRA EXPENSE   AMOUNT: $600,000   COINS %: 50   CAUSES OF LOSS: SPECIAL
ADDITIONAL INFORMATION: BUSINESS INCOME / EXTRA EXPENSE: MONTHLY LIMIT 1/4   FLOOD ZONE: AE   EARTHQUAKE: NOT REQUESTED
CONSTRUCTION TYPE: MASONRY NON-COMBUSTIBLE   DISTANCE TO HYDRANT: 300 FT   FIRE STATION: 1.2 MI   FIRE DISTRICT: NORFOLK   PROT CL: 2   # OF STORIES: 2   # OF BASEMENTS: 0   YR BUILT: 1972   TOTAL AREA: 22,500 SQ FT
BUILDING IMPROVEMENTS: WIRING 2011   PLUMBING 2011   ROOFING 2019   HEATING 2015
WIND CLASS: [X] RESISTIVE   HEATING SOURCE: GAS FORCED AIR   SPRINKLER: [X] FULL  % 100   FIRE ALARM: [X] CENTRAL STATION
ACORD 140 (2016/03)                                                                    PAGE 1 OF 3"""),
# 34
("160-2014-12", {"market": "US", "state": "UT", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 160 (2014/12)  BUSINESS OWNERS SECTION     DATE 04/18/2026
AGENCY: Wasatch Keystone Insurance, Ogden UT   CARRIER: Granite Shoals Mutual   APPLICANT: Bonneville Cycle Works LLC
EFFECTIVE DATE 06/01/2026   POLICY TYPE: [X] SPECIAL  [ ] STANDARD
PREMISES 1: 2510 Washington Blvd, Ogden UT 84401   OCCUPANCY: Bicycle sales and repair   CLASS CODE 56211
BUILDING LIMIT: $0 (tenant)   BUSINESS PERSONAL PROPERTY $310,000   DEDUCTIBLE $1,000
LIABILITY: $1,000,000 each occurrence / $2,000,000 aggregate   MEDICAL EXPENSES $5,000
OPTIONAL COVERAGES: [X] Employee dishonesty $25,000  [X] Hired and non-owned auto
ACORD 160 (2014/12)   Page 1 of 4"""),
# 35
("160-2014-12", {"market": "US", "state": "NM", "fill": "partial", "noise": "caps", "number_position": "not_after_word"},
"""ACORD   BUSINESS OWNERS SECTION   APPLICANT: TURQUOISE MESA COFFEE ROASTERS LLC, SANTA FE NM   BPP $180,000   LIABILITY $1M/$2M   FORM 160 (2014/12) PAGE 1 OF 4"""),
# 36
("163-2010-05", {"market": "US", "state": "GA", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 163 (2010/05)  COMMERCIAL AUTO DRIVER INFORMATION SCHEDULE
Applicant: Chattahoochee Fixture Installers Inc   Agency: Halvorsen & Dube Agency   Eff date 02/15/2026
# | Driver name | DOB | Sex | Lic # | St | Date hired | Yrs exp | Accidents/violations (3 yrs)
4 | Terrence Paulk | 06/14/1985 | M | 058812274 | GA | 03/2019 | 17 | none
5 | Josefina Varga | 11/30/1992 | F | 061190033 | GA | 08/2022 | 10 | 1 minor speeding 2025
6 | Desmond Achebe | 01/07/1971 | M | 044716690 | GA | 01/2014 | 30 | none
ACORD 163 (2010/05)  Page 1 of 1"""),
# 37
("128-2011-08", {"market": "US", "state": "AL", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 128 (2011/08)  GARAGE AND DEALERS SECTION     DATE 10/12/2026
AGENCY: Iron Bowl Insurance Partners, Birmingham AL   CARRIER: Cobalt Ridge Indemnity
APPLICANT: Cahaba Auto Sales & Service LLC   EFFECTIVE DATE 12/01/2026
TYPE: [X] FRANCHISED DEALER  [ ] NON-FRANCHISED  [X] SERVICE / REPAIR
GARAGE LIABILITY: $1,000,000 each accident   GARAGEKEEPERS: [X] Legal liability  Limit $250,000 per location  Comp ded $500  Coll ded $500
DEALERS PHYSICAL DAMAGE: Locations 1  Maximum value $3,400,000   Reporting: [X] Monthly
Number of employees: Full time 22   Part time 3   Plates issued: 6
ACORD 128 (2011/08)   Page 1 of 4"""),
# 38
("101-2008-01", {"market": "US", "state": "MD", "fill": "filled", "noise": "clean", "number_position": "title"},
"""ACORD 101 (2008/01) ADDITIONAL REMARKS SCHEDULE. Agency: Chesapeake Lantern Ins. Named insured: Annapolis Sail Loft LLC. Form number: 125, form title: Commercial Insurance Application. Remarks: applicant also operates a seasonal rigging service at 2 marinas; see attached GL supplement."""),
# 39
("140-2016-03", {"market": "US", "state": "ID", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 140 (2016/03) Property Section — Applicant: Snake River Potato Packers Inc, Twin Falls ID. Premises 1 Bldg 1: building $4,200,000, RC, special form. Construction: tilt-up. Sprinklered: Y."""),
# 40
("127-2020-03", {"market": "US", "state": "NE", "fill": "partial", "noise": "clean", "number_position": "title"},
"""ACORD 127 (2020/03)  BUSINESS AUTO SECTION
Applicant: Platte Valley Grain Hauling Co, Kearney NE      Effective date: 01/01/2027
Driver information: 1  Hollis Brandt  Kearney NE  DOB 04/22/1969  Lic H11920334 NE  % use 100
General information: Any vehicles used to haul for others? Y (grain, intrastate)   Hazmat? N   Vehicles leased to others? N
Remarks: vehicle schedule on ACORD 129 attached
ACORD 127 (2020/03)   Page 1 of 4"""),
]
