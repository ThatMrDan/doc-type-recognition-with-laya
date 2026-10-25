# Label quality for a ~500-example golden set (5 document types, specialty insurance submissions)

Scope: how to make the golden set labels for `sov`, `loss_run`, `acord`, `broker_email`, `other` trustworthy enough to act as "the exam" (CLAUDE.md invariant 4), given that many labels come from a synthetic generator and need independent checking. Researched October 2026.

## How common are label errors in test sets, and how much do they distort rankings?

### Takeaway
Even famous, curated benchmarks carry a few percent of wrong test labels (mean at least 3.3%, up to about 10% per dataset), and only about 5 to 6 percentage points of extra test noise is enough to flip which of two models looks better. For a 500-item golden set, 3% is about 15 bad items, which is larger than the accuracy gaps a promotion gate is likely to judge.

### Cited Findings
- Northcutt, Athalye and Mueller (2021) found an average of at least 3.3% label errors across the test sets of 10 widely used vision, text and audio datasets; ImageNet validation errors are at least 6% (abstract) / 5.83% (Table 1). — [arXiv 2103.14749](https://arxiv.org/abs/2103.14749)
- Per-dataset estimated test error rates: MNIST 0.15%, CIFAR-10 0.54%, CIFAR-100 5.85%, Caltech-256 1.54%, ImageNet 5.83%, QuickDraw 10.12%, 20news 1.09%, IMDB 2.90%, Amazon Reviews 3.90%, AudioSet 1.35%. — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749)
- Method: candidates were flagged by confident learning, then each flagged example was shown to 5 Mechanical Turk workers; it counted as a validated error if fewer than 3 of 5 agreed the given label applied. On average 51% of flagged candidates were confirmed as errors (so about half of algorithmic flags were false alarms). — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749); [arXiv abstract](https://arxiv.org/abs/2103.14749)
- Validated errors were sorted into four outcomes: correctable (majority agree on the suggested label), multi-label (both labels apply), neither (neither label applies), non-agreement (no majority). This is a useful template for adjudication outcomes. — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749)
- Rankings: on the full ImageNet validation set, rankings of 34 pretrained models were largely unchanged after removing errors, but on the "correctable" subset they changed sharply (ResNet-18 rose from 34th to 1st; NASNet-large fell from 1st to 29th). ResNet-18 beats ResNet-50 if the prevalence of originally mislabelled test examples rises by about 6%; VGG-11 beats VGG-19 on CIFAR-10 at about 5%. — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749)
- Expert review suggested confident learning missed about 14% of ImageNet errors, so true error rates are likely higher than the reported figures. — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749)
- Authors' advice: correct test labels even if training labels stay noisy, and judge models on correctly labelled test data; higher-capacity models can look better on noisy test sets because they fit the noise. — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749)

### Inferences
- With 500 items, each item is 0.2 percentage points of accuracy. The promotion policy in this repo tolerates no accuracy loss and allows per-class recall drops up to 0.05; with about 100 items per class, 5 mislabelled items in one class is a 0.05 recall swing. Golden label errors therefore can directly cause wrong promote/reject decisions.
- Errors concentrate in hard, boundary items, which are the items where candidate models differ most, so the ranking distortion is worse than the raw error rate suggests (the "correctable subset" result).
- A synthetic generator's labels are "by construction" and may be systematically wrong in a correlated way (for example the generator labels every document by the template it used, even when the rendered content is ambiguous). Correlated errors are more dangerous than random ones because a model trained on similar synthetic data will agree with them.

### Gaps
- No published error rates were found for document-type classification test sets specifically (RVL-CDIP style) in this pass; the figures above are from general benchmarks.

## Writing annotation guidelines (decision rules, "other/ambiguous" policy, worked examples)

### Takeaway
The guideline must be fixed in writing before the reliability study, be exhaustive (every document gets exactly one label by a stated rule), and be tested on a sample covering every class and every known complication. Changing rules mid-study, or letting annotators confer, invalidates the agreement figures.

### Cited Findings
- Krippendorff's requirements for reproducible coding (as summarised by Artstein and Poesio): an exhaustively formulated, clear and usable coding scheme with step-by-step instructions; clearly specified criteria for choosing coders; and coders working independently. — [Artstein & Poesio 2008, Computational Linguistics 34(4), PDF](https://aclanthology.org/J08-4004.pdf)
- Practices that break these requirements: expanding instructions and adding rules while the data are generated; using long-term collaborators who agree because they know the project's intent rather than because they follow the written guide; discussing judgements or deciding by majority vote during the reliability exercise. Any of these "make the resulting data unusable for measuring reproducibility". — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- The reliability sample should contain examples of all category values, each category should occur often enough to yield at least five chance agreements, and the sample should cover every domain the instructions apply to, because "every domain displays different complications". — [Artstein & Poesio 2008, summarising Krippendorff 2004](https://aclanthology.org/J08-4004.pdf)
- Artstein and Poesio accept expert coders for computational linguistics (usefulness over pure replicability) but say expert-trained annotation is less replicable across sites, so agreement studies are still needed plus an independent evaluation of the downstream task. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)

### Inferences (proposed decision rules for this project; not from a source, for the writer to adapt)
- **Unit of annotation**: label the document as received by the intake step (one file or one email body), not the submission. If attachments are split into separate documents upstream, the email body is labelled on its own.
- **Primary-purpose rule**: label by what the document is for, not by what it mentions. An email whose body says "please find attached the SOV and loss runs" is `broker_email`; the attached spreadsheet is `sov`.
- **Container rule**: if an email body itself contains a pasted SOV table and little else, decide by the majority of content and the presence of the defining structure (location rows with TIV / building values). Write this threshold down with a worked example either way.
- **Title vs content rule**: a cover page titled "Loss Run" whose body is a schedule of locations is labelled by content (`sov`); titles are evidence, not the decision. Record "title_conflict" as a flag.
- **Multi-type bundles** (one PDF holding ACORD 125 plus a loss run): pick the type of the first substantive page or the dominant page count, but flag `multi_type=true` so these can be analysed or excluded; this mirrors the Northcutt "multi-label" outcome.
- **Explicit `other` vs ambiguous**: `other` is a real class (policy wordings, invoices, financial statements, photos). "I cannot tell" is not `other`; it is an `ambiguous` flag that sends the item to adjudication. Keep these separate in the schema so ambiguity does not inflate `other`.
- **Defining features per class** in the guide (for example ACORD: form number such as ACORD 125/126/140 and the standard layout; loss run: carrier, policy periods, claims with paid/reserved/incurred; SOV: one row per location with values; broker/MGA email: correspondence with sender, recipient and request).
- **Worked examples**: at least 2 clear positives per class plus at least 1 worked example for each boundary rule above, with the reasoning written out. Freeze as guideline v1.0 before the agreement study; any later change bumps the version and triggers re-checking of affected items.

### Gaps
- I did not retrieve a primary industry labelling guide (for example Google's or a vendor's) in this pass; the decision rules above are my synthesis, not sourced practice.

## Agreement metrics: computation, thresholds, how many items to double-annotate

### Takeaway
For two annotators use Cohen's kappa; for three or more, or missing labels, use Krippendorff's alpha (nominal); report percent agreement, a confidence interval and the full confusion matrix. Target alpha/kappa of at least 0.80 overall (0.67 to 0.80 is "tentative" only), and inspect per-class agreement because skewed classes hide problems.

### Cited Findings
- Coefficients: chance-corrected measures (kappa, pi, alpha) give a better indication of annotation quality than raw percent agreement, and the detailed calculation shows where disagreements sit. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Worked example in the paper: observed agreement 0.88 gives S = 0.82, pi about 0.7995, kappa about 0.8013 on the same data, showing that on nominal labels the coefficients are close but can straddle a threshold. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Bias and prevalence: kappa and pi diverge when coders have different label distributions (bias problem), and it is very hard to get high values when one category dominates (prevalence problem). Artstein and Poesio prefer pi-like K and alpha, which abstract away from individual coder bias, and note that the difference shrinks as the number of annotators grows; "increasing the number of annotators is the best strategy". — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- They recommend Krippendorff's alpha, which handles weighted distances (only needed when categories are not equally distinct; for 5 flat nominal classes, nominal alpha is equivalent in spirit to Fleiss-style K). — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Thresholds: Krippendorff/Carletta convention is K > 0.8 good, 0.67 to 0.8 "tentative conclusions"; the 0.67 boundary was "highly tentative and cautious" and Krippendorff later treats 0.8 as the absolute minimum ("Even a cutoff point of alpha = .800 ... is a pretty low standard", Krippendorff 2004 p. 242). Neuendorf (2002): 0.90 or above acceptable to all, 0.80 acceptable in most situations. Artstein and Poesio's own experience: only values above 0.8 ensured reasonable annotation quality, so "0.8 is a good value" if a threshold is needed. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Landis and Koch (1977) bands (slight/fair/moderate/substantial/almost perfect at 0.2 steps) are common in medicine but more lenient; Artstein and Poesio note CL researchers mostly follow the stricter Krippendorff conventions. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- McHugh (2012) argues the Cohen/Landis-Koch style bands are too lenient, proposes 0.60 to 0.79 moderate, 0.80 to 0.90 strong, above 0.90 almost perfect, concludes "any kappa below 0.60 indicates inadequate agreement", and notes many texts set 80% raw agreement as a minimum. — [McHugh 2012, Biochemia Medica (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3900052/)
- Significance: showing agreement beats chance is "trivial"; report a confidence interval instead. Kappa CIs can use the normal approximation for large samples; alpha CIs need bootstrapping (Hayes and Krippendorff 2007). — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Reporting: give number of coders, whether they worked independently, whether they relied only on the manual, and a confusion matrix so overall figures do not hide disagreement on rarer categories. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Sample size: Krippendorff's minimum-units formula (from Bloch and Kraemer 1989) is cited in Artstein and Poesio. A Sim and Wright (2005) style worked example targets an 80% CI of kappa plus or minus 0.1 and arrives at N = 165 items when no assumption about kappa is made. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf); [secondary excerpt, ime.usp.br (authorship unconfirmed)](https://www.ime.usp.br/~abe/lista/pdfGSoh9GPIQN); [Bujang & Baharum 2017 review citing Sim & Wright](https://riviste.unimi.it/index.php/ebph/article/view/29771)

### Inferences
- For 500 items and 5 classes, the cleanest design for a gold set is to double-annotate all 500 (it is small), with a third annotator on disagreements. If budget forces a subset, at least about 165 to 200 items, stratified so every class (and every boundary rule) is present, is the floor for a usable kappa CI of roughly plus or minus 0.1; this follows from the cited sample-size example, not from a source specific to this task.
- Gate: overall alpha (nominal) at least 0.80 with bootstrap 95% CI reported; per-class (one-vs-rest) kappa at least 0.70 as an internal warning level for each of the 5 classes; any class below that triggers a guideline revision before the set is frozen. The per-class number is my proposal.
- Compute with `krippendorff` (PyPI) or `statsmodels.stats.inter_rater` (`fleiss_kappa`) and `sklearn.metrics.cohen_kappa_score`; bootstrap over items for CIs. (Library names from general knowledge, not verified in this pass.)
- The generator's label should be treated as one "annotator" in the agreement table but not as one of the independent humans; its agreement with the human consensus is a direct measure of generator label quality.

### Gaps
- Could not retrieve Sim and Wright (2005) or Landis and Koch (1977) primaries; the Landis and Koch bands are quoted via Artstein and Poesio; the N = 165 figure is from a secondary excerpt whose authorship I could not confirm.
- Did not find a source giving an "acceptable agreement for a gold test set" that differs from the general 0.8 convention.

## Adjudication: majority vote vs expert, tracking disagreement, ambiguous items

### Takeaway
Measure agreement on independent labels first, then adjudicate; majority vote is fine for producing a label but must not be part of the reliability measurement, and genuinely ambiguous items should be kept with a flag and reported separately rather than forced into a class or silently dropped.

### Cited Findings
- Majority vote and discussion between coders break independence, so they must happen after, and separately from, agreement measurement. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Krippendorff's recommendation: three or more coders, chosen by stated criteria, working independently from a coding scheme fixed in advance. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- The Northcutt study used a 3-of-5 majority rule and kept four explicit outcome categories (correctable, multi-label, neither, non-agreement) instead of a binary keep/fix. — [arXiv HTML 2103.14749](https://arxiv.org/html/2103.14749)

### Inferences
- Proposed flow: (1) two independent human labels per item, blind to the generator label and to model predictions; (2) agree and match the generator: accept; (3) any disagreement (human vs human, or humans vs generator): an expert adjudicator (underwriting operations lead) decides using the guideline and records a rationale and the guideline rule cited; (4) outcomes follow the Northcutt-style categories: `accepted`, `corrected`, `multi_type`, `ambiguous` (non-agreement after adjudication).
- Expert adjudication beats plain majority vote here because there are only 2 to 3 annotators and the boundary rules are domain-specific; majority of two is undefined.
- Ambiguous items: keep them in a separate "hard/ambiguous" slice. Exclude them from the headline accuracy used by the promotion gate (invariant 6), but report model behaviour on them (ideally low confidence and routing to fallback, which is the system's intended behaviour). Removing them silently would overstate production accuracy; forcing a label adds noise.
- Track disagreement as data: a per-class confusion matrix between annotators, and a count of which guideline rule was invoked in adjudication. Rules that are invoked often are candidates for clarification in the next guideline version.

### Gaps
- No source found quantifying the accuracy of expert adjudication vs majority vote for document classification specifically.

## Automated label-error detection as triage (confident learning, cross-model disagreement, LLM annotators)

### Takeaway
Use cleanlab's `find_label_issues` with out-of-sample predicted probabilities, plus disagreement between Laya and an LLM, to rank which golden items humans should re-check first. Treat flags as a review queue, not as corrections: in the best-known study only about half of flagged items were real errors, and LLM annotators are inconsistent and task-dependent.

### Cited Findings
- `cleanlab.filter.find_label_issues(labels, pred_probs, *, return_indices_ranked_by=None, filter_by='prune_by_noise_rate', frac_noise=1.0, num_to_remove_per_class=None, min_examples_per_class=1, ...)`; returns a boolean mask, or indices ranked by `self_confidence`, `normalized_margin` or `confidence_weighted_entropy`. `labels` are integers 0..K-1, `pred_probs` shape (N, K). Results are most accurate with out-of-sample probabilities, for example from cross-validation. `filter_by` options include `prune_by_noise_rate`, `prune_by_class`, `both`, `confident_learning`, `predicted_neq_given`, `low_normalized_margin`, `low_self_confidence`. — [cleanlab filter docs](https://docs.cleanlab.ai/stable/cleanlab/filter.html)
- Confident learning flags in 10 benchmarks were confirmed by humans only 51% of the time on average, and still missed an estimated 14% of ImageNet errors. — [arXiv 2103.14749](https://arxiv.org/abs/2103.14749); [arXiv HTML](https://arxiv.org/html/2103.14749)
- Klie et al. reimplemented and compared 18 annotation error detection methods on 9 English datasets (text classification and token/span labelling) and released a common evaluation protocol and code. — [Klie et al. 2022, arXiv 2206.02280](https://arxiv.org/abs/2206.02280)
- LLM annotators, positive evidence: Gilardi, Alizadeh and Kubli (PNAS 2023), on 6,183 tweets and news articles across relevance, stance, topic and frame tasks, found zero-shot ChatGPT accuracy about 25 points above MTurk crowd workers on average, with higher intercoder agreement than crowd workers and trained annotators, at under $0.003 per annotation. — [arXiv 2303.15056](https://arxiv.org/abs/2303.15056); [PNAS via PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10372638)
- Törnberg (2023, preprint) reports GPT-4 had higher accuracy and reliability, and equal or lower bias, than experts and crowd workers when classifying US politicians' tweets by party in 2020. — [arXiv 2304.06588](https://arxiv.org/abs/2304.06588)
- Limits: Reiss (2023) found ChatGPT zero-shot labels (news vs not-news) changed with slight prompt rewording and across repeated identical runs, sometimes below scientific reliability standards; pooling repeated runs helped; "the unsupervised application of ChatGPT for text annotation and classification is not recommended". — [arXiv 2304.11085](https://arxiv.org/abs/2304.11085)
- Limits: Pangakis, Wolken and Fasching replicated 27 annotation tasks across 11 datasets with GPT-4 and found performance "highly contingent on both the dataset and the type of annotation task"; they recommend validating every task against human labels. A search snippet of the same paper reports accuracy about 19.4 points higher for items with a consistency score of 1.0 across repeated runs. — [arXiv 2306.00176](https://arxiv.org/abs/2306.00176) (consistency figure from search snippet, not verified in the abstract)
- Statistical test for replacing humans: Calderon, Reichart and Dror (ACL 2025) propose the Alternative Annotator Test, which uses a modest human-annotated subset (at least 3 independent human annotators) to justify LLM annotations; across 10 datasets, 6 LLMs and 4 prompting techniques, LLMs could sometimes replace humans, with closed models such as GPT-4o doing best. — [ACL Anthology 2025.acl-long.782](https://aclanthology.org/2025.acl-long.782); [arXiv 2501.10970](https://arxiv.org/abs/2501.10970v3)

### Inferences
- Getting `pred_probs` for the golden set without training on it (invariant 4): use a model trained only on non-golden data (Laya's current checkpoint and/or a cheap TF-IDF plus logistic regression baseline trained on production labels); these predictions are out-of-sample with respect to golden items by construction. Do not cross-validate by training on golden folds, as that breaks the "never trained on" rule even if the model is thrown away; a baseline trained only on non-golden data avoids the question.
- Triage queue order: (a) items where generator label is not equal to human label; (b) cleanlab flags ranked by `self_confidence`; (c) items where Laya and the LLM fallback agree with each other but disagree with the given label; (d) items where an LLM's label flips across 3 to 5 repeated runs or prompt paraphrases (the Reiss and Pangakis finding that inconsistency signals hard items). Every queued item gets a human decision; nothing is relabelled automatically.
- With only 500 items and 5 classes, cleanlab's noise-rate estimates per class rest on about 100 items each, so treat counts as rough; a simple `predicted_neq_given` plus low self-confidence list may be as useful.
- LLM as a third annotator: acceptable for triage and as a non-voting "annotator" column in the agreement table, but not as the gold source, because (i) the same LLM family is the system's fallback, so using it to define gold would make fallback agreement look artificially high (circularity), and (ii) the published evidence is on social-science text tasks, not insurance documents. If the team wants to rely on LLM labels for part of the set, run an alt-test style comparison against at least 3 human annotators first.
- Synthetic-specific check: the generator and any LLM may share blind spots (both "know" the template). Independence means at least one checker that never sees the generator's label or template id.

### Gaps
- No evidence found on LLM annotator reliability for insurance or commercial document types; the cited studies are on tweets, news and websites.
- Did not read Klie et al. results tables, so I cannot say which of the 18 methods performed best.

## Practical workflow and documentation (provenance, annotator ids, label version, dataset card)

### Takeaway
Store every label event, not just the final label: who (or what) labelled, under which guideline version, independently or in adjudication, and why. Publish a short dataset card with agreement statistics, the confusion matrix and the known-ambiguous slice.

### Cited Findings
- Reporting should include number of coders, independence, reliance on the manual, significance/CIs and a confusion matrix. — [Artstein & Poesio 2008](https://aclanthology.org/J08-4004.pdf)
- Datasheets for Datasets: every dataset should ship with a datasheet documenting "its motivation, composition, collection process, recommended uses". — [Gebru et al., arXiv 1803.09010](https://arxiv.org/abs/1803.09010)
- Northcutt et al. released their corrected labels publicly (labelerrors.com), an example of versioning corrections alongside the original labels rather than overwriting them. — [arXiv 2103.14749](https://arxiv.org/abs/2103.14749)

### Inferences (proposed schema and workflow for this repo)
- Per golden row: `doc_id`, `content_hash`, `template_group` (needed already for invariant 3), `source` (`synthetic_generator` / `real_anonymised`), `generator_version` and `generator_label` if synthetic, `labels[]` events each with `annotator_id`, `annotator_type` (`human_expert` / `human_ops` / `llm` / `generator`), `label`, `flags` (`ambiguous`, `multi_type`, `title_conflict`), `guideline_version`, `timestamp`, `independent` (bool), then `final_label`, `adjudicator_id`, `adjudication_rationale`, `adjudication_rule`, `outcome` (`accepted` / `corrected` / `multi_type` / `ambiguous`), and `golden_set_version`.
- Version the golden set as a whole (for example `golden-v1.2`), and record in each eval report which version was used, so a change in score can be attributed to model or to label fixes. Never edit labels in place.
- Workflow: write guideline v1.0 with worked examples; pilot on about 50 items with 2 annotators, revise guideline, discard pilot agreement figures; freeze guideline; independent double annotation of all ~500 (blind to generator label and model output); compute alpha/kappa with CI and per-class confusion; adjudicate disagreements; run automated triage (cleanlab, Laya vs LLM, LLM repeat-run instability) and send flags to human review; fix and log; publish dataset card; repeat the triage step whenever a new model is evaluated, since a new model's confident disagreements are fresh error candidates.
- Dataset card contents: class definitions and guideline version; source mix (synthetic vs real) per class; template-group counts; annotator pool description; agreement (overall and per class) with CIs; annotator confusion matrix; number and share of corrected, multi-type and ambiguous items; generator-vs-human agreement; known limitations (synthetic share, single tenant, English only).
- Spot audit: re-annotate a random 5 to 10% of the frozen set each release by a fresh annotator to estimate residual error; my proposal, not sourced.

### Gaps
- Did not retrieve the full Datasheets question list (only the abstract) or a Google/vendor labelling guide; the schema above is synthesis.
