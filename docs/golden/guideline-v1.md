# Golden set labelling guideline, version 1.0

This guideline decides the label for every golden-v2 row. Annotators, the judge model and the
row generators all work from it. It is frozen at 1.0 for golden-v2; any change makes a new version
and a new golden version. Rationale and sources: `reports/Golden set for document typing.md`.

## What you are labelling

Each row is the text the typer sees: the first page of a PDF, the header rows and first data rows
of a spreadsheet (cells separated by ` | `), or an email's headers and body. Label the document's
type, which decides the extractor that runs next. Read the whole text before deciding.

## The five classes

| Label | The document is | Typical signals |
|---|---|---|
| `sov` | An insurance statement or schedule of values: a per-location or per-building schedule of property attributes and insured values | Location or building rows; address, occupancy, construction (ISO 1 to 6 or words), year built, area, sprinklers, protection class; building, contents, BI and total insured values (TIV); a valuation basis |
| `loss_run` | Loss history for an insured: a carrier or TPA loss run, a broker loss summary, or a no-known-loss letter | Policy periods, a valuation date; claim number, date of loss, description, paid, reserve or outstanding, incurred, open or closed; totals by year |
| `acord` | A standard ACORD application form or section used to apply for cover | "ACORD" with a form number (125, 126, 127, 129, 130, 131, 137, 140 and others) and application fields: applicant, premises, prior carrier, hazards |
| `broker_email` | Correspondence from a broker, MGA or agent covering a submission | From, to, subject; greeting; coverage requested, effective date, deadlines; attachment mentions; signature or disclaimer |
| `other` | Anything else in a submission | Surveys, valuations, supplemental questionnaires, quotes, binders, MRC slips, presentations, financials, invoices, KYC, certificates, plans, photos |

## How to decide

1. Decide by content and purpose, not by the title or file name. A title is evidence; the body decides.
2. A mention of a type is not an instance of it. "SOV attached" in an email does not make the email an SOV.
3. If a document contains several documents, label the first substantive one and set the `multi_type` flag.
4. If the title contradicts the content, label by content and set the `title_conflict` flag.
5. If you cannot tell after reading, do not use `other`. Pick your best label and set the `ambiguous`
   flag; the row goes to adjudication. `other` is a real class, not a "don't know".
6. Label independently. Do not look at another annotator's label, the generator's intended label,
   the judge's vote or any model output.

## Edge-case rules

| # | Case | Label | Flag |
|---|---|---|---|
| 1 | Email body that only lists attachments ("SOV and 5 yr loss runs attached") | `broker_email` | |
| 2 | Email body with a short inline loss summary (a sentence or a few figures) | `broker_email` | |
| 3 | Email whose body is mostly a pasted SOV or loss table: more than half the text is the table and the table has its defining columns | The table's class (`sov` or `loss_run`) | |
| 4 | Forwarded chain, top line "pls see below", the retail agent's submission beneath | `broker_email` | |
| 5 | Combined document, for example ACORD 125 then ACORD 126 then loss runs | The first substantive document's class | `multi_type` |
| 6 | ACORD 139 Statement of Values | `sov` | |
| 7 | ACORD 140 property section, even with location and value blocks | `acord` | |
| 8 | ACORD certificates and evidence of insurance (24, 25, 27, 28): "issued as a matter of information only" | `other` | |
| 9 | Supplemental application or questionnaire (Y/N questions, carrier or MGA branded) | `other` | |
| 10 | Valuation or appraisal report, even with a building schedule appendix | `other` | |
| 11 | Broker market presentation, even with a values summary and a claims table | `other` | |
| 12 | Carrier quote or indication, even with premium by location | `other` | |
| 13 | No-known-loss letter signed by the insured | `loss_run` | |
| 14 | Broker multi-carrier loss summary spreadsheet | `loss_run` | |
| 15 | Construction contract "schedule of values" (pay application budget by trade) | `other` | |
| 16 | London market variants: MRC slip is `other`; "Schedule of Insured Values" is `sov`; "Claims Experience" is `loss_run`; an email quoting a UMR is `broker_email` | as stated | |
| 17 | Title contradicts content, for example a "Loss Run" cover over a location schedule | By content | `title_conflict` |
| 18 | Still cannot tell after reading | Best guess | `ambiguous` |

## Worked examples

- `From: priya@ostlerhart.co.uk | Subject: Fwd: Calder Mills renewal | Hi team, SOV and 5 yr loss runs attached, target 1 Dec. Thanks` is `broker_email` (rule 1).
- `Loc | Address | Occ | Constr | Bldg | Contents | TIV` followed by location rows is `sov`.
- `ACORD 25 CERTIFICATE OF LIABILITY INSURANCE ... THIS CERTIFICATE IS ISSUED AS A MATTER OF INFORMATION ONLY` is `other` (rule 8).
- `To whom it may concern, we confirm there have been no known losses for the period 01/01/2021 to date. Signed, director` is `loss_run` (rule 13).
- `LOSS RUN` as a title over rows of `Bldg # | Street | Construction | Building value` is `sov` with `title_conflict` (rule 17).

## Where this differs from the model's `CRITERIA`

`CRITERIA` in `src/doctype/domain.py` is what Laya scores. It does not yet mention ACORD 139 (rule 6),
certificates (rule 8) or no-known-loss letters (rule 13). It is left unchanged for golden-v2 so the
current and fine-tuned checkpoints are compared on the descriptions they were trained with. Align it
in a later model version and record the change against the golden version.

## What an annotator records

For each row: `label`, any `flags` (`multi_type`, `title_conflict`, `ambiguous`), annotator id,
guideline version (`1.0`) and, if the label relied on a rule, the rule number.
