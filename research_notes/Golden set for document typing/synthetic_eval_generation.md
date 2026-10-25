# Generating a synthetic held-out evaluation set for document typing: methods and risks

Context: about 500 examples over 5 classes (`sov`, `loss_run`, `acord`, `broker_email`, `other`). The classifier is a small encoder-style decision model (Laya), trained so far on a seeded template generator. The golden set must not mirror that generator.

Research scope: about 15 tool calls (searches and fetches of abstracts and some full texts), October 2026. Where only an abstract was read, the notes say so.

## Approaches: templates vs LLM generation vs perturbing real seeds, and how to get diversity

### Takeaway
LLM-generated data is consistently less diverse than real data and lags it most on subjective or fuzzy tasks. Grounding generation in real seed examples (few-shot or perturbation) narrows the gap far more than zero-shot prompting does, and so do an explicit attribute taxonomy and a discriminator filter. For a golden set, use a generator that is structurally independent of the training templates: LLM generation grounded in real anonymised seeds and conditioned on an attribute grid, plus controlled noise. Keep a slice of hand-edited real-derived documents.

### Cited Findings
- Li et al. (EMNLP 2023) trained BERT and RoBERTa on synthetic data and tested them on real held-out data. Zero-shot synthetic data cost an average of 16.9 macro-F1 points (RoBERTa). Few-shot synthetic data, generated with real examples in the prompt, cost 6.7. Few-shot beat zero-shot by about 10.3 to 10.6 macro-F1 points. — [Li et al. 2023, Synthetic Data Generation with LLMs for Text Classification: Potential and Limitations](https://arxiv.org/html/2310.07849v2)
- In the same study, low-subjectivity tasks (AG News topics, relation, IMDB, SMS spam) lost only about 3 to 6 points with zero-shot data. The six most subjective tasks lost an average of 27.4 macro-F1 points (BERT). Topic-like tasks such as AG News (95.3 real vs 89.3 zero-shot vs 91.5 few-shot) are the closest analogue to document typing. — [Li et al. 2023](https://arxiv.org/html/2310.07849v2)
- Diversity ranking in that study: real data was more diverse than few-shot synthetic data, which was more diverse than zero-shot synthetic data. Diversity was measured with Remote Clique (mean pairwise embedding distance) and Chamfer distance (mean nearest-neighbour distance). The zero-shot diversity drop was significantly larger on subjective tasks (p < 0.01). Models trained on synthetic data converged faster and overfitted more. — [Li et al. 2023](https://arxiv.org/html/2310.07849v2)
- Veselovsky et al. tested three ways to make LLM synthetic data more faithful to real data: grounding (real examples in the prompt), filtering (a discriminator removes samples that look unrealistic) and taxonomy-based generation (a taxonomy in the prompt for diversity). All three improved downstream performance on real data, and grounding helped most on their sarcasm task. — [Veselovsky et al. 2023, Generating Faithful Synthetic Data with LLMs](https://arxiv.org/pdf/2305.15041)
- Persona conditioning: Persona Hub (Tencent AI Lab) curates about 1 billion web-derived personas. Each persona is put in the prompt to steer the generator towards a different perspective and diversify the output, and the set was deduplicated with MinHash and embeddings (the deduplication detail comes from a secondary review). — [Ge et al., Scaling Synthetic Data Creation with 1,000,000,000 Personas](https://arxiv.org/html/2406.20094v1)
- CheckList generates many test cases from templates with fill-in lexicons and perturbation functions, organised as a matrix of capabilities by test type (abstract level). Templates are cheap and give precise control, but they produce exactly the narrow, regular text that a template-trained model will find easy. — [Ribeiro et al. 2020, CheckList](https://arxiv.org/abs/2005.04118)
- Real OCR engines produce noisy text that pre-trained text classifiers are not robust to. Simulating OCR-like noise from clean text, combined with hard-example mining, recovered much of the robustness. — [Xu et al. 2021, Robust Learning for Text Classification with Multi-source Noise Simulation](https://arxiv.org/abs/2107.07113v1)
- One preprint injected synthetic OCR-style substitutions, deletions and insertions into text to stress a classifier. Its authors say the corruption model does not perfectly replicate real PDF parsers, so treat simulated OCR noise as an approximation. — [arXiv 2608.28595](https://arxiv.org/pdf/2608.28595)
- Anthropic's eval guidance: mirror the real task distribution and include edge cases, specifically irrelevant or missing input, overly long input, and ambiguous cases where humans would disagree. Prefer many automatically graded cases over a few hand-graded ones. — [Anthropic, Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

### Inferences
- Document typing is a low-subjectivity, topic-like task, so on Li et al.'s evidence LLM-generated documents should be usable as eval data. The real danger is not subjectivity but structural sameness: the generator's idea of what a loss run looks like will be cleaner and more prototypical than real broker output.
- Recommended mix of generation sources for the 500 rows, with each source recorded per row:
  - Grounded LLM generation, prompted with anonymised real seeds where available.
  - Hand or LLM perturbation of real seeds.
  - A small number of CheckList-style template cases, only for targeted functionality tests and never with the training generator's templates or vocabulary.
- Attribute grid to condition on, one cell per generation call. Example axes:
  - Line of business (property, casualty, marine, cyber).
  - Sender persona (wholesale broker, MGA underwriter, retail agent, insured's risk manager).
  - Source system (carrier loss-run export, broker spreadsheet, ACORD 125/126/140 form-fill).
  - Length (one line to multi-page) and format (table-heavy, prose, mixed).
  - Extraction path (native text, OCR'd scan, email body with quoted thread, spreadsheet flattened to CSV-like text).
  - Language register.
  - Noise level (none, typos, OCR substitutions, truncation at 512 tokens, header or footer stripped).
- Truncation needs its own grid axis because the English Laya root is 512 tokens (repo CLAUDE.md). A document whose class-defining header falls beyond the window is a realistic hard case.
- Apply noise as a separate, seeded post-processing step after generation and labelling, so the clean original and the noised variant share a label. They then form a natural invariance pair.

### Gaps
- I found no study of synthetic test sets for insurance or business document classification specifically.
- Exact diversity scores from Li et al. are only in figures and were not extracted.
- I found no quantitative comparison of template-generated and LLM-generated test sets for the same classifier.

## Known risks of synthetic eval sets

### Takeaway
Synthetic benchmarks track real performance reasonably well on simple classification tasks such as intent detection, but less well on complex ones. They carry a same-generator bias (small models score higher on data they generated themselves) and an easiness bias from low diversity. Test-label errors of even a few per cent can reorder models. The sharpest risk here is template echo: evaluating a template-trained model on text with the same structure inflates accuracy, just as real-data models fail on counterfactual distributions they never saw.

### Cited Findings
- Maheshwari et al. found that LLM-generated synthetic data captures the relative performance of methods well on simpler tasks such as intent classification, but less well on complex tasks such as NER. — [Maheshwari, Ivanov, El Haddad 2024, Efficacy of Synthetic Data as a Benchmark (arXiv preprint)](https://arxiv.org/abs/2409.11968)
- The same paper defines a "bias factor" for the case where one LLM both generates the benchmark and performs the task. Smaller LLMs did better on their own generated data, larger ones showed no significant bias. The authors recommend averaging over data from several larger generator models. — [Maheshwari et al. 2024](https://arxiv.org/abs/2409.11968)
- Ko et al. (ICML 2023 workshop) built steerable synthetic sentence-classification datasets as proxy benchmarks. They report high correlation with real downstream performance and position synthetic sets as a way to avoid test-data leakage. — [Ko et al. 2023, On Robustness-Accuracy Characterization of LLMs Using Synthetic Datasets](https://icml.cc/virtual/2023/26894)
- Generated data is less diverse than real data and models trained on it overfit more (diversity ranking real > few-shot > zero-shot). — [Li et al. 2023](https://arxiv.org/html/2310.07849v2)
- Linguistic diversity (lexical, semantic and syntactic) declines when models are trained recursively on synthetic text, and few works measure diversity beyond the lexical level. — [Guo et al. 2023, The Curious Decline of Linguistic Diversity](https://arxiv.org/pdf/2311.09807)
- Classifiers trained only on original data fail on counterfactually revised data and the reverse also holds, while training on both reduces reliance on spurious features (abstract level). This is evidence that a test distribution differing in surface features can expose large hidden gaps. — [Kaushik, Hovy, Lipton 2020, Learning the Difference that Makes a Difference with Counterfactually-Augmented Data](https://arxiv.org/abs/1909.12434)
- Northcutt et al. estimated at least 3.3% label errors on average across the test sets of 10 widely used benchmarks (about 6% on the ImageNet validation set). On corrected CIFAR-10 labels, a smaller model overtook a larger one once mislabelled test examples rose by only 5%. — [Northcutt, Athalye, Mueller 2021, Pervasive Label Errors in Test Sets](https://arxiv.org/abs/2103.14749)
- Standard test sets can overstate capability because models learn shortcut decision rules that also work on the test set. Small expert edits dropped accuracy by up to 25%. — [Gardner et al. 2020, Evaluating Models' Local Decision Boundaries via Contrast Sets](https://arxiv.org/abs/2004.02709v2)

### Inferences
- Treat golden-set accuracy as an upper bound on production accuracy until it has been compared against a real anonymised sample. Report both numbers side by side as they arrive.
- Same-generator optimism takes two forms in this repo:
  1. The training template generator and the golden set share structure (a template echo).
  2. The fallback LLM (Ollama qwen or Bedrock) generates or judges golden rows and is then compared against them.
  Mitigate (1) by keeping the generator code and lexicons for the golden set separate from `scripts/` training generators, and by running a near-duplicate check (embedding cosine and MinHash) between the golden set and training snapshots. The near-duplicate check extends invariant 3 (exclusion by hash and template group). Mitigate (2) by never letting the fallback model family generate golden rows.
- Use at least two generator model families and report accuracy per generator. A large spread between generators is a sign that the set measures generator style rather than document type.
- LLM text tends to be cleaner and more prototypical than real submissions, so a purely synthetic set will probably be easier than production. That is why the hard and noisy slices below matter.

### Gaps
- No bias-factor numbers were extracted (only the abstract was read).
- I found no study measuring whether LLM-generated test documents are systematically easier or harder than real ones for encoder classifiers. The easiness claim above is an inference from the diversity results.

## Hard, adversarial and boundary cases

### Takeaway
Build a separate, labelled hard slice (roughly 20 to 30% of the set) from three test types: contrast or counterfactual edits that minimally flip the class, CheckList invariance tests where noise or format changes should not change the class, and directional tests. Report the hard slice separately from the in-distribution slice, never only blended.

### Cited Findings
- Contrast sets: dataset authors hand-perturb test instances in small but meaningful ways that usually change the gold label, which probes the model's local decision boundary. Across 10 datasets, model performance was significantly lower than on the original test sets, by up to 25%, even though the edits were not adversarial. — [Gardner et al. 2020](https://arxiv.org/abs/2004.02709v2)
- CheckList: a capability by test-type matrix with three test types:
  - Minimum Functionality Tests (MFT): simple cases the model must get right.
  - Invariance tests (INV): label-preserving perturbations that should not change the prediction.
  - Directional expectation tests (DIR): perturbations with a known expected effect on the prediction.

  Practitioners using CheckList wrote about twice as many tests and found nearly three times as many bugs, and a commercial team found new, actionable bugs in an extensively tested model. (Test types are from the paper's well-known content; the fetched abstract confirms the matrix and the user-study results.) — [Ribeiro et al. 2020](https://arxiv.org/abs/2005.04118)
- Counterfactual revision protocol: edit the document so it matches a counterfactual target label, stays coherent and avoids unnecessary changes. — [Kaushik et al. 2020](https://arxiv.org/abs/1909.12434)
- Anthropic recommends including ambiguous cases where even humans would struggle to agree, alongside irrelevant and overly long inputs. — [Anthropic develop-tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

### Inferences
- Concrete hard cases for this taxonomy:
  - **Contrast pairs:**
    - A broker email that only says "SOV attached" (`broker_email`) vs the attached SOV body (`sov`).
    - A loss run vs a premium or exposure history table with the same columns but no claims (`other`).
    - An ACORD 125 form-fill vs a broker's free-text summary of the same fields (`broker_email` or `other`).
    - A schedule of vehicles or equipment vs a property SOV.
    - A carrier "no known losses" letter (decide and document whether this is `loss_run`).
    - An email with an inline pasted loss table.
  - **INV tests:** OCR substitutions (0/O, 1/l, rn/m), typos, dropped headers, column reordering, currency and date-format changes (UK vs US), truncation beyond the class cue, and forwarded-thread wrappers around a document.
  - **MFT:** canonical, textbook examples of each class.
  - **DIR:** adding a valuation column header such as "TIV" should raise the `sov` probability.
- Keep each contrast pair linked by a `pair_id` and score pair consistency (both members correct), as Gardner et al. do. Pair consistency is much stricter than accuracy.
- Suggested split of the 500 rows:
  - About 350 in-distribution rows (70 per class, varied over the attribute grid).
  - About 100 contrast and boundary rows (50 pairs).
  - About 50 noise and invariance variants derived from in-distribution rows.

  Report accuracy, macro-F1, per-class recall and ECE for each slice. Because the promotion gate (`PromotionPolicy`) uses per-class recall, compute it on the in-distribution slice, and treat a hard-slice regression as a warning or a separate gate.
- `other` needs deliberate breadth: the generator will otherwise produce a few stock "other" documents, and real submissions contain many types (financials, inspection reports, engineering surveys, policy wordings, invoices).

### Gaps
- I found no published guidance giving an optimal share of hard cases. The 20 to 30% above is a judgement call, chosen so that hard cases cannot dominate the headline number.

## Validating synthetic labels

### Takeaway
A generated document's intended label is not ground truth. Validate it with layered checks: rule-based validators, an independent LLM judge from a different model family to the generator, multi-sample self-consistency, and a stratified human review sized by binomial statistics. Route disagreements to human adjudication rather than dropping them silently.

### Cited Findings
- Li et al. did not verify that generated texts actually matched their target labels. This is a common gap in synthetic-data work. — [Li et al. 2023](https://arxiv.org/html/2310.07849v2)
- Anthropic recommends grading with a different model from the one that generated the output. Constrain the grader's output format (for example "Output only 'yes' or 'no'"), validate the response, and define scale endpoints explicitly. — [Anthropic develop-tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- Self-preference bias: GPT-4 showed significant self-preference as a judge. LLM judges rated low-perplexity (familiar) text higher than humans did, whoever wrote it, which suggests familiarity is the mechanism. — [Wataoka, Takahashi, Ri 2024, Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819)
- A preprint on multimodal judges reports self-preference and also bias towards models of the same family (unreviewed). — [MLLM-as-a-Judge Exhibits Self-Preference Bias](https://projectpage-1sg1y.kinsta.page/)
- Zheng et al. identify position, verbosity and self-enhancement biases and limited reasoning in LLM judges, and propose mitigations. — [Zheng et al. 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena, NeurIPS D&B](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract.html)
- Survey: using an LLM as judge does not by itself guarantee accurate evaluations aligned with established standards. Reliability needs dedicated work on consistency and bias mitigation. — [Gu et al., A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594)
- Test-set label errors are pervasive (at least 3.3% on average across 10 benchmarks). Confident-learning flags were confirmed as real errors by humans only about half the time (51% or 54%, depending on the version), so automated flags need human confirmation. — [Northcutt et al. 2021](https://arxiv.org/abs/2103.14749)

### Inferences
- Pipeline per row:
  1. Generate with the intended label and the attribute-grid cell recorded.
  2. Run rule validators, for example: `acord` must contain an ACORD form number or its field layout; `loss_run` needs claim, date-of-loss and paid/reserve style fields; `sov` needs a location list with values. Also run negative rules, for example `broker_email` must have email headers or a salutation.
  3. Ask a judge from a different family to both the generator and the fallback model to classify the document blind, from the `CRITERIA` descriptions, 3 to 5 times at temperature above 0. Accept only if the majority matches the intended label and the agreement rate is high.
  4. Round-trip check: ask the judge to explain the class-defining cue and confirm the cue is present in the text, not only in the generation prompt.
  5. Send anything that fails to human adjudication, keeping the disagreement as metadata, because it is often a genuine boundary case worth keeping.
- Do not use Laya itself, or any model under evaluation, as a label validator. Filtering by the evaluated model's agreement turns the golden set into a set of "examples the model already gets right".
- Human spot-check size (standard binomial statistics, worked here rather than sourced):
  - With zero errors found in n reviewed rows, the 95% upper bound on the error rate is about 3/n (the "rule of three"). Reviewing 100 clean rows bounds error below about 3%, and 300 below about 1%.
  - To estimate the error rate to within plus or minus 3% at 95% confidence, n is about 1.96² · p(1−p) / 0.03². That is about 200 if the error rate is near 5%, and about 1,067 in the worst case (p = 0.5).
  - Practical choice for 500 rows: review 100% of the hard and contrast slice (about 150 rows, where errors concentrate and the labels are the point) plus a stratified random 100 of the in-distribution slice (20 per class). If that 100 has 0 or 1 errors, the slice error rate is plausibly below 3 to 5%. Track the estimate per class, because a 20-row class sample alone gives only a loose bound of about 14%.
- Record judge agreement and the human verdict per row. Label errors above about 2 to 3% matter here because the promotion gate tolerates only a 0.05 per-class recall drop.

### Gaps
- The MT-Bench human-agreement figure (often quoted as above 80%) was not verified in this session.
- I found no study that quantifies how well an LLM judge verifies labels for document-type data specifically.

## Diversity and quality metrics for generated sets

### Takeaway
Report a small panel of low-correlated metrics, because no single diversity score is adequate:
- Lexical: distinct-n at a fixed sample size, Self-BLEU, compression ratio.
- Semantic: mean pairwise embedding distance (Remote Clique) and nearest-neighbour distance (Chamfer).
- Coverage: the fill rate of the attribute grid.
- Distance to the training data, which is the measure most specific to this project.

### Cited Findings
- Distinct-n is the proportion of unique n-grams among all n-grams. It depends on text length, so report it at fixed sizes. Self-BLEU scores each sample against the others (higher means less diverse) and is purely lexical. Average pairwise BERTScore serves as a homogenisation index. — [Shaib et al. 2024, Standardizing the Measurement of Text Diversity](https://arxiv.org/html/2403.00553v3)
- Shaib et al. recommend reporting compression ratio, self-repetition of long n-grams and Self-BLEU together, because the three correlate weakly with each other. Fast compression captures much the same signal as slow n-gram homogeneity scores. — [Shaib et al. 2024](https://arxiv.org/pdf/2403.00553)
- N-gram metrics capture only surface form, missing semantics and style. Diversity methods fall into n-gram-based, reference-based (MAUVE- or FID-style) and transformation-based families. — [Measuring Diversity in Synthetic Datasets (arXiv 2502.08512)](https://arxiv.org/html/2502.08512v1)
- Remote Clique and Chamfer distance over embeddings both showed real data to be more diverse than synthetic data. — [Li et al. 2023](https://arxiv.org/html/2310.07849v2)
- Diversity should be measured at lexical, semantic and syntactic levels. — [Guo et al. 2023](https://arxiv.org/pdf/2311.09807)

### Inferences
- Metrics to implement (cheap, deterministic, testable in the repo):
  - Per class: distinct-2 and distinct-3 on a fixed 50-document sample, Self-BLEU, and gzip compression ratio.
  - Embedding Remote Clique and Chamfer, using an embedding model that is not Laya's encoder.
  - Attribute-grid coverage: fraction of cells with at least k rows, and the entropy of the cell distribution.
  - Length and token-count histograms against the 512-token window.
- Leakage and echo metrics:
  - Maximum and mean cosine similarity from each golden row to its nearest training-snapshot row.
  - MinHash Jaccard similarity to the nearest training row, with a threshold that flags near-duplicates.
  - A classifier two-sample test: train a quick discriminator to tell golden rows from training rows. If it is near chance, the golden set is a template echo. If it is near perfect, check the golden set against real data as well.
- Once real anonymised samples exist, compute the same metrics on them, plus MAUVE or an embedding-distribution distance from the synthetic set to the real set, to quantify distribution shift.

### Gaps
- I found no accepted thresholds for "diverse enough". Metrics are only meaningful relative to a real reference sample or across versions.

## Mixing synthetic with real anonymised data, and documenting provenance

### Takeaway
Treat real anonymised documents as the anchor and synthetic rows as coverage and stress material. Report metrics by source, add real rows as they become available, and carry per-row provenance (source, generator model and version, prompt or template id, seed, attribute cell, noise ops, validation results, reviewer) so that slices can be recomputed and contamination traced.

### Cited Findings
- Grounding synthetic generation in real examples gave the largest faithfulness gains. — [Veselovsky et al. 2023](https://arxiv.org/pdf/2305.15041); [Li et al. 2023](https://arxiv.org/html/2310.07849v2)
- In an education-domain study, a human-coded test set was kept as the validity check for LLM-generated data. The best classifier results came from training on 80% synthetic and 20% human-coded data, and higher generation temperatures increased variance in performance estimates. This was a training mix; the test set stayed human-coded. — [Borchers et al. 2025 (arXiv 2501.09126)](https://arxiv.org/abs/2501.09126v1)
- Synthetic benchmarks are most trustworthy when pooled across several generator models. — [Maheshwari et al. 2024](https://arxiv.org/abs/2409.11968)
- Evals should mirror the real-world task distribution. — [Anthropic develop-tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)

### Inferences
- Suggested per-row schema for the golden JSONL:
  - `id`, `text`, `label`
  - `source`: one of `synthetic_llm`, `synthetic_template`, `real_perturbed`, `real_anonymised`
  - `generator` (model id and version), `prompt_id`, `seed`, `attribute_cell` (dict)
  - `noise_ops` (list), `parent_id` (for perturbed or noised variants), `pair_id` (for contrast pairs)
  - `slice`: one of `in_dist`, `contrast`, `invariance`, `mft`
  - `template_group`, which is needed for invariant 3's group exclusion
  - `validator_results`, `judge_model`, `judge_votes`, `human_reviewer`, `human_verdict`, `created_at`, `content_hash`
- Report accuracy and macro-F1 by `source` and by `slice`. Weight decisions towards the real anonymised slice once it reaches about 30 or more rows per class.
- Golden synthetic rows must never be used as training seeds, and their generator prompts must not be reused by the training generator. Add this as an explicit exclusion check alongside the hash and template-group checks.
- Freeze and version the golden set (a hash of the file). Any change to the generator, judge or noise ops produces a new version, so promotion comparisons always run on the same exam.

### Gaps
- I found no primary-source guidance (from OpenAI, Google or Hugging Face) on synthetic-to-real ratios for held-out sets specifically. Those vendor guides were not fetched in this session.
- I found no insurance-specific public corpus of anonymised submissions to use as a real reference.
