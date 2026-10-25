# Anatomy of commercial and specialty insurance submission documents

Scope: what the five intake classes (sov, loss_run, acord, broker_email, other) really look like, so a synthetic golden set can mimic content, layout, vocabulary and confusions. Researched October 2026. Most accessible web sources are vendor blogs and insurer or broker help pages; ACORD.org and Lloyd's/LMG primary pages were partly unreachable (HTTP 403, or compressed PDFs with no extractable text), which is noted under Gaps. Items under "Inferences" that are not tied to a citation are practitioner background knowledge and should be checked against real documents before being relied on.

## SOV: columns, header wording, opening lines, units and formats

### Takeaway
An SOV is a per-location (and often per-building) table of COPE attributes (construction, occupancy, protection, exposure) and insured values by coverage, usually an Excel workbook, often messy (merged headers, mid-table subtotals, free-text construction). Insurer-issued SOV forms are titled "Statement of Values" and ask for separate values per separately rated building on a stated valuation basis.

### Cited Findings
- Insurer SOV forms are organised by location number, occupancy and value columns for building, contents and stock; values stated on replacement cost or actual cash value; separate values are required for each separately rated building and its contents. The Intact form adds columns for property of others and customers' goods. — [Markel property SOV form (via search summary)](https://content.markel.com/api/public/content/property-statement-of-values); [Intact SOV form 70048](https://portal.intactinsurance.com/system/files/mydocuments/70048%20%2806-2016%29%20W7777.pdf)
- The Markel form's PDF title field is "STATEMENT OF VALUES"; page 1 is landscape (wide table) and page 2 portrait, with many fillable fields. — [Markel SOV PDF metadata](https://content.markel.com/api/public/content/property-statement-of-values)
- A broker-style SOV guide lists fields: address, city, state, zip, construction type, year built, square footage, number of stories, building value ($), business personal property value ($), equipment, primary use, fire suppression system, fire alarms and detectors, security system; building value defined as estimated replacement cost, not market value. — [Rikor, Understanding the SOV schedule](https://rikor.helpjuice.com/en_US/franchise-insurance-101/insurance-101-how-do-i-complete-a-statement-of-values-sov-form)
- Construction class definitions used on SOVs: Class 1 Frame (combustible walls, floors, roof); Class 2 Joisted Masonry (masonry walls, combustible interior framing); Class 3 Non-Combustible (metal or concrete); Class 4 Masonry Non-Combustible; Class 5 Modified Fire Resistive (rating at least 1 hour but under 2); Class 6 Fire Resistive (rating at least 2 hours, e.g. reinforced concrete or protected steel). Codes run 1 (least) to 6 (most fire-resistive); classes 7 to 9 are variations not directly tied to fire. — [Rikor](https://rikor.helpjuice.com/en_US/franchise-insurance-101/insurance-101-how-do-i-complete-a-statement-of-values-sov-form); [IRMI, Modified fire resistive](https://www.irmi.com/term/insurance-definitions/modified-fire-resistive-construction-iso); [Troxell, ISO construction types](https://www.troxellins.com/Blog/Posts/92/Business-Insurance/2025/12/ISO-Construction-Types-How-They-Impact-Your-Insurance/blog-post/); [AmTrust ISO construction classes training doc](https://careers.alexanderschmidt.com/ASFieldAlerts/AmTrust/AmTrust%20Library/Trainingdocs/ISO%20Construction%20Classes.pdf)
- Public Protection Classification (PPC) values are 1 to 10 with split classes such as "4/8B"; ISO revised 8B to a "Y" suffix (4/8B becomes 4/4Y) and split 9 to "X" (4/9 becomes 4/4X); 10W is a newer class for properties 5 to 7 road miles from a station but within 1,000 feet of a creditable water source. Effective date given as 1 July 2014 by ISO; one carrier reported receiving X/Y values from December 2016; not applicable in Texas. — [Verisk, New PPC classes](https://www.verisk.com/blog/new-ppc-fire-protection-classes-to-benefit-insurers-communities/); [ISO PPC announcement brochure](https://isomitigation.com/images/articles/PPC-Announcement-Brochure.pdf); [Encova coding note](https://www.encova.com/the-loop/wmic/2016/11/motorists-insurance-group-invests-in-discovery-district2/); [Santa Cruz County ISO rating](https://www.countyfire.santacruzcountyca.gov/Portals/36/sccfire/FireResources/ISO_RATING.pdf)
- Cat-model exposure schemas treat occupancy, year built, construction type and number of stories as the core per-location characteristics, with example values like "Wood frame" and "General residential"; dominant occupancy is computed on TIV. — [Verisk Touchstone, most frequently observed value](https://docs.risksolutions.verisk.com/Touchstone/11.0/ts-tsre_all/help_ts_data-quality_most-frequently-observed-value.html)
- Real SOV quirks: merged header row (a 41-location SOV in a worked example), merged body cells, a subtotal mid-rows, construction in free text such as "JM/frame w mansard", protection class typed into the wrong column. — [CallSphere practitioner write-up](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md)
- SOVs often arrive as multi-tab spreadsheets with inconsistent headers and embedded notes; extraction tools map synonyms such as "replacement cost" and "insured value" to one field. — [Nomad Data, submission backlog](https://www.nomad-data.com/doc-chat/clearing-the-submission-backlog-ai-transformation-for-underwriting-assistants-in-property-homeowners-commercial-auto-and-general-liability-construction-d6c76); [V7 Labs, best AI tools for commercial lines](https://www.v7labs.com/blog/best-ai-tools-commercial-lines-underwriting)
- A typical packet pairs a typed ACORD PDF with an Excel SOV. — [V7 Labs, submission triage](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)
- ACORD also publishes a Statement of Values form (ACORD 139), separate from ACORD 140 Property Section; one carrier table appears to misalign this. — [Instafill ACORD forms category](https://instafill.ai/category/acord-forms); [Amerisafe supported ACORD forms](https://geaux.amerisafe.com/umhelp/AgentHelp/topics/submissions/r_supported_acord_forms.html)
- Beware the homonym: "schedule of values" in construction contracting (AIA G703, Oracle Unifier) is a payment-application line-item budget, not an insurance SOV. — [Archdesk SOV template](https://archdesk.com/blog/schedule-of-values-template-construction); [Oracle Unifier, Add SOV columns](https://docs.oracle.com/cd/F74772_01/English/unifier_modules/74605.htm)

### Inferences
- For synthetic SOVs, the first lines typically read as a title row ("Statement of Values", "Schedule of Values", "Property Schedule", "Location Schedule", UK: "Schedule of Insured Values" / "Asset Register") plus insured name and policy period, then one header row (sometimes two-tier merged, e.g. "VALUES" spanning Building / Contents / BI / Total TIV). Common header variants (practitioner knowledge, unverified here): Loc #, Bldg #, Street Address, City, State/Province, Zip/Postcode, County, Occupancy / Use / Description, Construction (code or text: Frame, JM, Non-Comb, MNC, MFR, FR), Yr Built, Yr Roof/Updates, # Stories, Sq Ft (UK: m2 / sq m), Sprinklered (Y/N/%), PPC / Prot Class, Building (RC), Contents/BPP, Stock, EDP, BI/BE/Rental Income (often 12 months), TIV / Total Insured Value, Flood zone, Lat/Long.
- Currency formats: US "$1,250,000" or "1,250,000"; UK/London "GBP 1,250,000", "£1.25m", schedules in multiple currencies with a "Currency" column and FX note; totals row "TOTAL" or "Grand Total" at bottom; values sometimes in thousands ("USD 000s").
- When text-serialised for a classifier, an SOV is mostly numbers and short codes with a repeating row structure; this is its strongest signal and also why valuation reports with embedded schedules and ACORD 140 location blocks are its main confusions.
- ISO construction codes on SOVs may appear as numbers (1 to 6), as abbreviations, or in free text; PPC appears as integers, split classes (e.g. "3/9", "4/4X") or blank.

### Gaps
- Could not extract text from the Markel or Intact PDFs (compressed streams), so exact header wording from insurer forms is not verified.
- No primary source found for UK/London market SOV conventions (e.g. Lloyd's property schedule headers, sums insured on reinstatement basis, declared value) in this pass.
- No public specification of ACORD 139 columns was retrieved.

## Loss runs: layout, wording variants, no-loss letters, broker summaries

### Takeaway
Loss runs are carrier (or TPA) system printouts per policy and policy period, stamped with a valuation ("as of") date, listing claims with claim number, date of loss, cause/description, paid, reserve/outstanding, incurred and open/closed status, with per-period totals. Layouts and labels vary by carrier; they frequently arrive as scans or photos; three to five years is standard.

### Cited Findings
- Valuation date is the cutoff through which claim transactions are included; summary loss runs are "as of" a date and show paid losses, expenses and claim counts by year. Paid plus case reserve equals incurred (also "reported"). — [CAS CLRS 2013 handout](https://www.casact.org/sites/default/files/presentation/clrs_2013_handouts_paper_2482_handout_1315_0.pdf); [Milliman, Beginner's guide to casualty actuarial language](https://www.milliman.com/ja-JP/insight/A-beginners-guide-to-the-casualty-actuarial-language)
- Claim-level fields: claim number, date of loss, line of coverage, short loss description, amount paid (indemnity), LAE, reserves, open/closed status; some runs include a summary loss ratio; no industry-standard format; "amount paid" on one carrier is "indemnity paid" on another. — [V7 Labs, AI loss run analysis](https://www.v7labs.com/blog/ai-loss-run-analysis-automate-data-extraction)
- Label drift: "incurred" vs "total loss" vs "Total Inc." — [Nomad Data, loss run analysis](https://www.nomad-data.com/doc-chat/supercharging-loss-run-analysis-for-complex-submissions-in-commercial-auto-gl-construction-and-property-with-doc-chat-for-broker-submission-specialists); [CallSphere](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md)
- Formats: PDF, scans, phone photos, spreadsheets, or pasted email text; multi-year histories usually 3 to 5 years, sometimes 5 to 7; each carrier only covers its own policies, so multi-carrier history means several runs; underwriters want runs dated within about 12 months. — [V7 Labs, AI loss run analysis](https://www.v7labs.com/blog/ai-loss-run-analysis-automate-data-extraction)
- Example: a five-year loss run faxed then photographed, valuation date in the header, handwritten margin note ("claim reopened, reserve now 118k") changing incurred from $34,000 to $152,000; repeated photocopying blurs figures. — [CallSphere](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md)
- A US workers' comp carrier requires four years of prior-carrier loss runs valued within 100 days of inception, total premium and payroll per year, TPA runs on TPA letterhead, and a written explanation if runs cannot be supplied. — [State Fund California, loss run information](https://www.statefundca.com/broker/how-to-submit-a-quote/loss-run-information/)
- No known loss letters / statements: the named insured (or authorised representative, after diligent inquiry) certifies no known losses, accidents or circumstances that could give rise to a claim for a stated period; carriers use them for reinstatements and moratoria; forms carry fraud warnings and say inaccuracy may void coverage. — [Admiral, No known loss statement](https://admiralins.com/no-known-loss-statement); [Admiral NKL letter PL](https://admiralins.com/wp-content/uploads/dlm_uploads/2023/06/No-Known-Loss-Letter-PL.pdf); [OSCIS Representation of No Known Loss](https://www.oscis.com/wp-content/uploads/2025/09/Representation-of-No-Known-Loss-v2.pdf); [Hawaii No Known Loss Affidavit](https://cca.hawaii.gov/ins/files/2025/06/No-Known-Loss-Affidavit.pdf); [Kin, statement of no loss](https://www.kin.com/blog/statement-of-no-loss/)
- Vendor tools separately flag catastrophe years and compute five-year incurred. — [Nomad Data](https://www.nomad-data.com/doc-chat/supercharging-loss-run-analysis-for-complex-submissions-in-commercial-auto-gl-construction-and-property-with-doc-chat-for-broker-submission-specialists)

### Inferences
- Realistic synthetic loss-run header block (practitioner background): carrier name/logo, "Loss Run" / "Loss History Report" / "Claims Experience Report" / "Policy Loss Detail" / UK "Claims Experience" or "Loss Record", insured name, policy number, line (GL, Auto, WC, Property), policy period (MM/DD/YYYY to MM/DD/YYYY), "Valued as of" / "Evaluation date" / "Run date", page x of y. Body: Claim # | DOL | Date Reported | Claimant | Cause / Description | Status (O/C, Open/Closed/Reopened) | Paid (Indemnity, Medical, Expense) | Reserve / Outstanding | Recovery / Subrogation | Total Incurred. Footer: totals per policy year, claim counts, "No claims reported for this period" lines for clean years.
- A "no known losses" letter is short prose on the insured's letterhead, signed and dated; it is likely to be labelled loss_run by a business but reads lexically like "other" correspondence, so the taxonomy decision should be explicit.
- London market: claims experience is commonly presented as a broker-prepared table inside a presentation or as a "5 year claims summary", with GBP/USD and "outstanding" rather than "reserve"; "incurred" and "paid" still used. Not verified from a primary UK source here.
- Broker loss summaries (one table across carriers and years with loss ratio) are loss_run in content even if embedded in an email or presentation.

### Gaps
- No primary carrier loss-run template was retrieved (TotalCSR guide returned 403).
- No UK/Lloyd's source on claims-experience presentation was found.

## ACORD forms: what each is, page-one text, certificates vs applications

### Takeaway
ACORD 125 is the master commercial application; line sections (126 GL, 127 business auto with 129 vehicle schedule and 137 auto coverages, 130 WC, 131 umbrella/excess, 140 property, 139 SOV) attach to it. Certificates and evidence forms (24, 25, 27, 28) are post-bind proof-of-coverage documents issued by agents, carry a "matter of information only" disclaimer, and are a natural confusion with "other".

### Cited Findings
- ACORD 125 starts most commercial submissions: applicant details, operations, prior carrier data and loss history; 126 GL covers liability exposures, limits and additional interests; 130 WC; 131 umbrella/excess; 140 commercial property including building information, coverages and protection systems; current editions cited as 2024/11 (verify). — [Semsee, ACORD 125](https://semsee.com/blog/acord-125); [Infrrd, ACORD 125](https://www.infrrd.ai/blog/acord-125); [Eduyush, ACORD 125](https://eduyush.com/en-us/blogs/insurance/acord-125-form); [Matil, ACORD 125](https://matil.ai/en/blog/acord-form-125)
- Auto: ACORD 127 Business Auto Section (with 129 Vehicle Schedule), ACORD 137 Commercial Auto Coverages/Limits Section in state-specific versions (137 AL, 137 CA, 137 NJ); sources disagree on whether 127 or 137 is "the" auto form. — [Merchants Group New Business Solutions Center](https://www.merchantsgroup.com/?p=30139); [Amerisafe supported ACORD forms](https://geaux.amerisafe.com/umhelp/AgentHelp/topics/submissions/r_supported_acord_forms.html); [Applied Epic ACORD form list](https://help.appliedsystems.com/Help/Epic/2023.2en-US/Accounts/Policies/ACORD_form_List.htm)
- ACORD 131 Umbrella/Excess section contains liability details and provides for extended coverage and high deductibles; ACORD 140 Property Section (2014/12 edition in one vendor list). — [UiPath ACORD131 ML package](https://docs.uipath.com/de/document-understanding/automation-cloud/latest/user-guide/acord131-ml-package); [Amerisafe](https://geaux.amerisafe.com/umhelp/AgentHelp/topics/submissions/r_supported_acord_forms.html)
- ACORD 35 is a cancellation request / policy release. — [search summary of vendor form lists incl. Docsumo](https://www.docsumo.com/blog/acord-form-processing)
- Certificates: ACORD 24 Certificate of Property Insurance, 25 Certificate of Liability Insurance, 27 Evidence of Property Insurance, 28 Evidence of Commercial Property Insurance. ACORD 25 states it is issued as a matter of information only, confers no rights on the holder, and does not amend, extend or alter coverage; if the holder is an additional insured the policy must be endorsed. 27/28 confer no rights on the additional interest named. ACORD supplies forms; agents/brokers complete and issue them. — [ACORD Certificates FAQ](https://acord.org/docs/default-source/forms/acordcertificatesfaq) (403 on fetch, content via search summary)
- Applications may be scanned with handwritten applicant sections; ACORD forms are "the easy part" of a packet to read. — [CallSphere](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md); [V7 Labs, submission triage](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)
- Appian's underwriting product auto-creates a submission from a broker email only when it contains an ACORD 125 Applicant Information section and no Submission ID in the subject. — [Appian, Create new submission](https://docs.appian.com/suite/help/26.6/cu-26.2.1.8/cu-create-new-submission.html)
- Extraction from ACORD covers named insured, addresses, class codes, limits, deductibles, effective dates. — [V7 Labs, submission triage](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)

### Inferences
- Page-one signals for synthetic ACORDs (practitioner background, summarised, not form text): "ACORD" wordmark and form number with edition date in a footer (e.g. "ACORD 125 (2016/03)" style) and "The ACORD name and logo are registered marks of ACORD"; title such as "COMMERCIAL INSURANCE APPLICATION" with "APPLICANT INFORMATION SECTION"; boxes for Agency, Carrier, NAIC code, Policy number, Underwriter; checkbox grid of lines of business requested (Commercial General Liability, Commercial Property, Business Auto, Umbrella, etc.) with premium columns; date, status of transaction (Quote / Issue / Bound / Change / Cancel). Text-serialised ACORDs are dense with short uppercase field labels, checkbox words ("Y/N", "X"), and NAIC/FEIN/SIC/NAICS codes.
- Certificates read differently from applications: single page, "CERTIFICATE OF LIABILITY INSURANCE", producer, insured, "INSURER(S) AFFORDING COVERAGE" with letters A-F and NAIC, table of policy types with policy numbers, effective/expiry dates and limits (each occurrence, damage to rented premises, med exp, general aggregate), "Certificate Holder" and "Cancellation" boxes, authorised representative signature. Whether a certificate is "acord" or "other" is a taxonomy decision: same branding, very different purpose (post-bind evidence, not submission data). Recommend labelling explicitly and including certificates in the golden set as hard cases.
- UK/London market has no ACORD application equivalent in common use; proposal forms are insurer- or MGA-specific (these belong in "other" or a supplemental class). ACORD's London presence is mainly data standards (e.g. messaging), not paper forms (not verified here).

### Gaps
- ACORD.org form catalogue pages were not reachable; edition dates and exact titles should be checked there.
- No information found on ACORD 146 or the full list of property-related forms (e.g. 141 to 149 range).

## Broker and MGA submission emails

### Takeaway
The cover email is a short narrative wrapper: account name, lines and limits sought, effective date, incumbent and expiring premium/target, a sentence on operations and losses, a list of attachments by colloquial name, and a quote-by date, followed by signature and legal disclaimers. Underwriters value summaries and specific facts in it, and the body itself may carry key data.

### Cited Findings
- A typical packet arrives as a broker email with attachments in mixed formats (typed ACORD PDF, Excel SOV, scanned loss run) and plain-text body content; body may carry key context; submissions also arrive via portals, SFTP and APIs. — [V7 Labs, submission triage](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)
- Example of a real-world shaped submission: an 8:02 a.m. email with four attachments (scanned ACORD 125, ACORD 126, five-year loss run, 41-location SOV). — [CallSphere](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md)
- Underwriters prefer submissions with specific facts, answers to likely questions and summaries; a cover letter should summarise what the underwriter will find and flag key items; brokers should say what information is still being gathered. — [Insurance Thought Leadership, How to catch the underwriter's attention](https://www.insurancethoughtleadership.com/how-to-catch-the-underwriters-attention)
- Thin submissions lead underwriters to assume the worst (higher rates, larger deductibles, more restrictions). — [Insurance Business AU, What brokers get wrong](https://www.insurancebusinessmag.com/au/news/breaking-news/what-brokers-get-wrong-in-submissions-to-underwriters-546561.aspx)
- Broker guidance from a Canadian carrier on successful quote submissions exists (content not retrieved). — [Sovereign Insurance](https://sovereigninsurance.ca/advice-and-tools/broker-resources/how-brokers-can-be-successful-with-quote-submissions)
- Intake systems must also handle duplicate submissions and broker-of-record conflicts (same account from two agencies). — [V7 Labs](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing); [CallSphere](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md)

### Inferences
- Synthetic email structure (practitioner background): headers From/To/Cc/Date/Subject; subjects like "New Submission - Acme Logistics LLC - Eff 01/01/2027 - Property/GL", "RE: FW: Renewal - ...", "Submission: [Insured] | Excess Casualty xs $5M", UK "New risk: [Insured] - Property Damage & BI - inception 1 Jan 2027"; greeting ("Hi team", "Good morning [UW]"); account summary paragraph (operations, years in business, revenue, locations); "Coverage requested" bullets with limits/deductibles/attachment points; incumbent carrier and expiring premium, "target" or "need to beat"; loss commentary ("clean 5 years", "one large GL claim 2023 now closed"); "Attached please find: ACORD 125/126/140, SOV, 5 yr currently valued loss runs, supplemental, prior year quote"; deadline ("quotes needed by 12/1"); signature block with agency, licence numbers, phone; confidentiality/E&O disclaimers; often a forwarded chain with the retail agent's original below the wholesaler's note.
- London market: emails from Lloyd's brokers often attach a "market presentation" / "submission pack" and a draft MRC slip, quote "UMR" references, and use "inception", "renewal", "lead", "following market", "line", "order" vocabulary.
- An email that merely names attachments ("SOV attached", "loss runs to follow") is broker_email, not sov/loss_run; the classifier must learn that mentions of a type are not instances of it.

### Gaps
- No primary source with a canonical broker submission email template or vocabulary frequency study was found; structure above is inferred.
- No source found on MGA-specific submission email conventions.

## Other documents: common types and opening text, including London market

### Takeaway
"Other" is a heterogeneous bucket: supplemental applications, financial statements, risk engineering/survey reports, valuation/appraisal reports, quotes and binders, certificates, MRC slips, broker presentations, invoices, KYC/sanctions material. Several contain SOV-like tables or loss tables, making them the main source of confusion.

### Cited Findings
- Commercial packets include supplemental applications (class-specific; the example packet has three) and financials alongside ACORD, SOV and loss runs. — [V7 Labs, submission triage](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)
- Appraisals can conflict with the application (e.g. location marked unsprinklered on the form but 100% sprinklered in an appraisal), so appraisals/valuations travel with submissions. — [Nomad Data](https://www.nomad-data.com/doc-chat/clearing-the-submission-backlog-ai-transformation-for-underwriting-assistants-in-property-homeowners-commercial-auto-and-general-liability-construction-d6c76)
- MRC (Market Reform Contract) is divided into six sections: Risk Details, Information, Security Details, Subscription Agreement, Fiscal and Regulatory, Broker Remuneration; underwriters subscribe by writing their line; the MRC is the source for the UMR and security block; current version described as MRC v3 with a digital iMRC (vendor source, unconfirmed against LMG). — [Buckhill key concepts](https://cdn.buckhill.co.uk/help/article/key-concepts)
- Earlier London Market Principles slips included a unique market reference, risk details, subscription agreement, information supporting the risk assessment, and fiscal/regulatory details. — [Insurance News, slips out a new principle](https://insurancenews.com.au/international/-and-slips-out-a-new-principle); [Insurance Insider, London embraces LMP slip](https://www.insuranceinsider.com/article/2876iu98zf5y778k4n2f4/london-embraces-lmp-slip)
- LMA guidance (v1.5, 2018) added Subscription Agreement headings for line slip operation (section leaders, delegation to leader). — [LMA bulletin LMA18-006](https://lmalloyds.com/LMA_Bulletins/LMA18_006_AC.aspx)
- Slip mechanics: broker presents risk on a slip; lead underwriter's line draws followers; lines are "signed down" proportionately when over-subscribed. — [Low & Partners, Maritime insurance law part 4](https://www.lowpartners.com/maritime-insurance-law-part-4/)
- Binders in the London market are delegated-authority contracts; coverholders submit bordereaux listing bound risks. — [Buckhill](https://cdn.buckhill.co.uk/help/article/key-concepts); [Lloyd's Y4991 Lineslips](https://assets.lloyds.com/assets/y4991-lineslips/1/Y4991%20-%20Lineslips.pdf)
- Reinsurance/specialty submissions often carry limited data, leading to conservative pricing (actuarial working party). — [IFoA paper B04](https://vle.actuaries.org.uk/pluginfile.php/143817/mod_resource/content/1/b04-analyzing-disconnect-between-reinsurance-submission-and-global-underwriters-needs.pdf)
- Underwriting data rooms list typical documents for complex risks. — [Fast.io, insurance underwriting data room](https://www.fast.io/resources/insurance-underwriting-data-room.md)

### Inferences
- Opening text cues for synthetic "other" docs (practitioner background, unverified):
  - Supplemental application / questionnaire: carrier or MGA logo, "[Class] Supplemental Application" or "Contractors Supplemental Questionnaire", numbered yes/no questions, fraud warning, signature block. UK: "Proposal Form".
  - Quote / quote letter / indication: "Quotation", "Terms are as follows", premium, taxes/fees, subjectivities, "valid for 30 days".
  - US binder: "Binder" / "Evidence of binding", binder number, effective time.
  - MRC slip: "UNIQUE MARKET REFERENCE: B0XXX...", "RISK DETAILS", headings TYPE, INSURED, PERIOD, INTEREST, LIMIT OF LIABILITY, DEDUCTIBLE, PREMIUM, CONDITIONS, CHOICE OF LAW AND JURISDICTION, then SECURITY DETAILS with "Insurer's Signed/Written Line" and stamps. (Headings not confirmed by a primary source in this pass.)
  - Broker market presentation: cover page with broker brand, "Property Renewal 2027 Market Presentation", contents (Executive summary, Business overview, Locations/values summary, Claims experience, Risk management, Coverage structure/tower diagram). Contains SOV summaries and loss tables, making it a prime confusion.
  - Risk engineering / survey report: "Risk Survey Report" / "Loss Prevention Survey", surveyor, date of visit, COPE narrative, recommendations numbered with priority, estimated maximum loss (EML/PML/MFL) scenarios.
  - Valuation / appraisal report: "Insurance Valuation Report" / "Reinstatement Cost Assessment" (UK, RICS), "Replacement cost new", appendix schedules by building that look like an SOV.
  - Financial statements: "Balance Sheet", "Statement of Income", auditor's report, "Notes to the financial statements".
  - Invoices / premium notices: "Invoice", "Debit Note" (UK), amount due, IPT (UK Insurance Premium Tax) or surplus lines tax.
  - KYC / sanctions: client due diligence forms, beneficial ownership, sanctions screening results; UK Lloyd's brokers use these heavily.
  - Certificates (if not mapped to acord), endorsements, policy wordings, expiring policy declarations pages.

### Gaps
- Could not reach LMG/Lloyd's primary MRC guidance; MRC v3 status and exact headings unverified.
- No primary source retrieved on risk survey or RICS reinstatement valuation report structure.

## Common classification confusions and edge cases

### Takeaway
Most errors in practice come from documents that contain or describe another class: emails that list or summarise attachments, combined PDFs, SOV-like schedules inside valuations, ACORD 140 location blocks, presentations with loss tables, certificates bearing ACORD branding, and supplementals that look like applications.

### Cited Findings
- Recognising each document type inside a mixed packet is the first hard step ("multimodal problem"); formats vary within a packet and across brokers. — [V7 Labs, submission triage](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)
- Loss data also arrives as pasted email text, not just attachments. — [V7 Labs, AI loss run analysis](https://www.v7labs.com/blog/ai-loss-run-analysis-automate-data-extraction)
- Handwritten annotations, fax artefacts, merged cells, free-text construction and misplaced columns degrade both classification and extraction; low-confidence readings should go to a person. — [CallSphere](https://callsphere.ai/blog/the-loss-run-arrives-as-a-scanned-fax-with-a-handwritten-note-in-the-m.md)
- Appraisal vs application conflicts on sprinklers show valuation reports carry SOV-type attributes. — [Nomad Data](https://www.nomad-data.com/doc-chat/clearing-the-submission-backlog-ai-transformation-for-underwriting-assistants-in-property-homeowners-commercial-auto-and-general-liability-construction-d6c76)
- ACORD 139 is itself a Statement of Values, so an SOV can be an ACORD form. — [Instafill](https://instafill.ai/category/acord-forms)
- ACORD 125 contains a prior carrier and loss history section, so an application page can look like a loss summary. — [Semsee, ACORD 125](https://semsee.com/blog/acord-125)
- "Schedule of values" also names construction pay applications. — [Archdesk](https://archdesk.com/blog/schedule-of-values-template-construction)

### Inferences
- Edge cases to include in the golden set, each with an explicit labelling rule:
  1. Email body with an inline loss table ("losses: 2022 $0, 2023 one claim $12k closed") -> broker_email (dominant purpose) unless policy says otherwise.
  2. Email body that only lists attachments -> broker_email.
  3. Forwarded chain where the top message is one line ("pls see below") and the payload is a retail agent's submission -> broker_email.
  4. Combined PDF (ACORD 125 + 126 + loss runs) -> needs page-level splitting; if typed whole, label by first/majority document and record as a known limitation.
  5. ACORD 139 SOV -> decide sov vs acord (recommend sov, since content and extractor are SOV).
  6. ACORD 140 with location/building blocks and values -> acord.
  7. ACORD 25/24/27/28 certificates -> decide acord vs other (recommend other or a dedicated certificate label, since they are post-bind and not submission data; at minimum test both).
  8. Supplemental application with carrier logo and Y/N questions -> other, despite application-like layout.
  9. Valuation/appraisal report with building schedule appendix -> other.
  10. Broker presentation with location summary and claims table -> other.
  11. Carrier quote with premium breakdown by location -> other.
  12. No known loss letter -> loss_run (content is loss history) but lexically letter-like.
  13. Broker-prepared multi-carrier loss summary spreadsheet -> loss_run, though spreadsheet-shaped like an SOV.
  14. Construction contract schedule of values -> other.
  15. Scanned/OCR-noisy versions of each class.
  16. UK variants: MRC slip (other), "Schedule of Insured Values" (sov), "Claims Experience" (loss_run), Lloyd's broker email with UMR (broker_email).

### Gaps
- No quantitative data found on which confusions are most frequent in production intake systems.

## Public datasets and published work on submission document classification

### Takeaway
I found no public dataset or peer-reviewed benchmark for commercial insurance submission document typing. The space is dominated by vendor products whose implicit taxonomies converge on ACORD / SOV / loss run / email / supplemental / financials / other.

### Cited Findings
- Intellect AI Magic Submission: ingestion, extraction, enrichment, triage and routing of ACORDs, SOVs, emails and loss runs. — [Intellect AI Magic Submission](https://www.intellectai.com/magic-submission/)
- Deloitte multi-agent framework on AWS Marketplace with Supervisor, SOV, Loss Run and ACORD agents, validated against business rules. — [AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-mtfsi3ii2jfos)
- Roots.ai submissions intake: monitors inboxes, classifies and routes, extracts, populates rating systems. — [Roots.ai](https://www.roots.ai/platform/ai-agent/insurance/submissions-intake)
- Pibit.ai vision APIs classify submission documents into categories for routing (loss-run focus). — [G2, Pibit.ai](https://www.g2.com/sellers/pibit-ai)
- V7 Labs: packet taxonomy ACORD (125/126/130/140), loss runs, SOV, supplemental applications, financials, broker email; triage outputs appetite, new/renewal, completeness, priority. — [V7 Labs](https://www.v7labs.com/blog/ai-insurance-submission-triage-processing)
- Appian commercial underwriting: manual upload with a "Document Type" dropdown; email auto-creation keyed on ACORD 125. — [Appian](https://docs.appian.com/suite/help/26.6/cu-26.2.1.8/cu-create-new-submission.html)
- UiPath Document Understanding ships an ACORD 131 ML extraction package (ACORD-form-specific models). — [UiPath ACORD131](https://docs.uipath.com/de/document-understanding/automation-cloud/latest/user-guide/acord131-ml-package)
- ACORD extraction APIs/vendors: Base64.ai, Docsumo, Instafill. — [Base64.ai ACORD](https://Base64.Ai/features/data-extraction-api/acord); [Docsumo](https://www.docsumo.com/blog/acord-form-processing)

### Inferences
- The five-class taxonomy in `src/doctype/domain.py` matches the vendor consensus; the main divergence across vendors is whether supplemental applications, financials and certificates get their own classes. A future split of "other" into supplemental, quote/binder, certificate, survey/valuation, financials, slip/presentation would align with vendor practice.
- Without public data, realistic evaluation depends on anonymised real documents; synthetic sets should deliberately encode the edge cases above.

### Gaps
- No academic papers, public datasets (e.g. on Kaggle/Hugging Face) or published accuracy benchmarks for submission document classification were found; all claims of accuracy are vendor marketing and were excluded.
- Vendors named in the brief (e.g. Cytora, Sixfold, Federato, hx) were not individually researched in this pass.
