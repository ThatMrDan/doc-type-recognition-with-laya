# Generator A authoring brief (shared by all classes)

You are generator family A for golden-v2: hand-authored synthetic documents written by Claude.

Read first:
- docs/golden/guideline-v1.md (the labelling rules; your rows must follow them exactly)
- reports/Golden set for document typing.md, section "Most confusions come from documents that
  contain or describe another class" (what real documents contain)

Do NOT open scripts/, data/production/ or models/: the golden set must not echo the training
generator. Do not use any of these names anywhere in your text (they appear in training data):
harbourline, kestrel, northgate, ashby, blackfriars, saltmarsh, redcliffe, fenwick, larkspur, tamar,
wexcombe, aldgate, aon, marsh, willis, lockton, howden, ajg, bms, Brindle, Copperleaf, Merrow,
Ostrander, Pellow, Quarry Lane, Rowan, Tillery, Vance & Hart, Wickham, Yardley, Ebury,
and first names amy, tom, lee, kim, sam, ana, raj, zoe, ben, eve, ola, max, ivy, noah.
Invent all other brokers, carriers, insureds, people, addresses and policy numbers. They are fictional:
never use a real company's name.

What a row's text is: what the typer sees. A spreadsheet is serialised as its header rows and first
data rows, cells separated by " | " and rows by " ; " or new lines. A PDF is its first page of text.
An email is its headers then its body. Vary length: about a third short (10 to 40 words), half medium
(40 to 120), the rest long (120 to 300). Keep figures internally consistent (incurred = paid + reserve,
TIV = sum of values). Mix US and UK market conventions (dates, currency, vocabulary). Include some
realistic mess: merged or abbreviated headers, odd spacing, a stray OCR error, all caps.

Output: one JSON object per line, UTF-8, to the file named in your task, with exactly these keys:
  id              "A-<class>-<nnn>" (zero-padded, unique in your file)
  slice           "core", "boundary" or "contrast"
  generator       "claude-opus-5.5"
  generator_family "A"
  prompt_id       "a-<class>-v1"
  attribute_cell  object with the grid attributes you chose, e.g. {"market": "UK", "format": "sheet", "length": "medium", ...}
  template_group  "gA:<class>:<key>" where key names the source style (broker firm, carrier system,
                  form number and edition, etc). At least 20 distinct groups among your core rows,
                  at most 5 rows per group.
  generator_label the label the guideline gives this text (one of sov, loss_run, acord, broker_email, other)
  edge_rule       guideline rule number for boundary rows, else null
  expected_flags  list, e.g. ["title_conflict"], else []
  parent_id       for contrast rows, the id of the core row you edited, else null
  pair_id         for contrast rows "P-<class>-<n>", else null
  text            the document text

Contrast rows: copy one of your own core rows and make the smallest edit that changes the correct
label to a different class under the guideline (for example turn a loss run's claim table into a
one-line mention inside an email, or retitle and restructure an SOV header so it becomes a
construction pay application). The edit must be minimal: most of the text stays the same.

When done, check the file: every line parses as JSON, keys exactly as above, ids unique, counts as
asked, no banned names (case-insensitive search). Report counts by slice and label, group count,
and anything you were unsure about.
