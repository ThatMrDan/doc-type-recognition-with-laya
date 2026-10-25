# Preventing leakage between training data and a held-out golden set for document typing

Scope: group-aware splitting and near-duplicate detection for a five-class document typer (sov, loss_run, acord, broker_email, other) on short texts of roughly 10 to 60 words. The repo already excludes golden documents from training snapshots by exact hash and by `template_group` (`src/doctype/services/label_store.py`, around line 70). The team plans a synthetic golden set of about 500 examples, made by a process similar to the one that makes training data.

Note on sourcing: everything under "Cited Findings" was checked against the source in this session (October 2026). Anything not verified is listed under "Gaps". Recommendations and thresholds that I derived rather than read are under "Inferences".

## 1. What leakage is, which forms matter here, and documented cases where it inflated results

### Takeaway
Leakage means the evaluation measures memorisation of something the model saw in training rather than generalisation to new documents. The well documented cases show inflation of roughly 8 to 13 F1 points from overlap in NLP, and claims that collapse entirely in other fields. For this project the forms that matter most are exact and near duplicates, same-template leakage (including standard forms such as ACORD shared across brokers), temporal leakage on production data, and generator leakage where golden and training data come from the same synthetic process.

### Cited Findings
- Kapoor and Narayanan found data leakage errors in 17 fields, affecting 329 papers, and gave a taxonomy of 8 leakage types "ranging from textbook errors to open research problems". [arXiv 2207.07048](https://arxiv.org/abs/2207.07048)
- The authors' companion site, updated May 2024, lists 41 papers from 30 fields that found errors, collectively affecting 648 papers. This is a later count, not a contradiction of the 17 fields / 329 papers in the paper. [Princeton reproducibility site](https://reproducible.cs.princeton.edu/)
- The site groups leakage into three broad kinds: no clean separation of training and test sets (test data available during pre-processing, modelling or evaluation), illegitimate features (proxies for the outcome), and a test set not drawn from the distribution of interest. [Princeton reproducibility site](https://reproducible.cs.princeton.edu/)
- Civil war prediction case: every paper claiming complex ML beat logistic regression failed to reproduce because of leakage. After correction, complex models did not do substantively better than decades-old logistic regression. Causes included imputing training and test data together, reusing an imputed dataset, and using proxies for the target. [arXiv 2207.07048](https://arxiv.org/abs/2207.07048); [Princeton reproducibility site](https://reproducible.cs.princeton.edu/)
- The site's table lists a law review (Medvedeva et al. 2023) where 156 of 171 papers had pitfalls, including temporal leakage and non-independence between training and test sets. [Princeton reproducibility site](https://reproducible.cs.princeton.edu/)
- Kaufman, Rosset and Perlich (KDD 2011, extended in ACM TKDD 6(4) 2012) define leakage as information about the target that should not legitimately be available to the model. They propose avoiding it through careful data management plus "learn-predict separation", and give ways to detect it when the modeller does not control data collection. They name KDD Cup 2008 as suffering severe leakage, and KDD Cup 2007 and the IJCNN 2011 Social Network Challenge as affected by leakage from external sources. [ACM DOI 10.1145/2382577.2382579](https://www.doi.org/10.1145/2382577.2382579); [Paper Digest summary](https://www.paperdigest.org/certificate/78717d808eb6b31c)
- Elangovan, He and Verspoor (EACL 2021): random splits can lead "to inflated results, inadvertently evaluating the model's ability to memorize and interpreting it as the ability to generalize". In text classification, document-level similarity of inputs causes train/test leakage. [ACL Anthology 2021.eacl-main.113](https://aclanthology.org/2021.eacl-main.113)
- Same paper, AIMed relation extraction: with random 10-fold splits, mean best-match train/test unigram cosine similarity was 96.95 (trigram 73.15). With folds split by source document ID it was 67.14 (trigram 20.77). F1 fell for all three models: BiLSTM 71.7 to 58.7, ConvRes 69.9 to 56.1, BioBERT 77.9 to 64.4. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Same paper: SST2 (sentiment) mean best-match unigram similarity between test and train was 46.06. BC2GM: 2,308 of 6,331 test gene names had exact matches in train. On ChEMU NER, F1 dropped from 96.7 on the most train-similar test interval to 85.6 on a less similar one, and on BC2GM from 82.4 to 74.5. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Elangovan et al. cite Lewis et al. (2020): 58 to 71% of test answers in three open-domain QA sets also appear in training data, and 28 to 34% of questions have paraphrases in training. They also cite Min (2020): splitting questions into paraphrase "templates" and keeping each template in one split only made models perform "significantly worse". This is the closest published analogue to our `template_group` split. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Lee et al. (2022), "Deduplicating Training Data Makes Language Models Better": train/test overlap affects "over 4% of the validation set of standard datasets". By NearDup, the share of validation examples with a near duplicate in train was C4 4.60%, RealNews 14.35%, LM1B 4.92%, Wiki-40B 0.72%. [arXiv 2107.06499](https://arxiv.org/abs/2107.06499); [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2107.06499)
- The GPT-3 paper built "clean" versions of benchmarks by removing any example with a 13-gram overlap with the pretraining set, then compared clean and full scores. Secondary sources report that over 90% of QuAC, SQuADv2 and DROP examples were flagged. [GPT-3 supplemental, NeurIPS 2020](https://proceedings.nips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Supplemental.pdf); [contamination survey arXiv 2404.00699](https://arxiv.org/pdf/2404.00699)
- Later work found that simple changes such as paraphrase or translation get past n-gram decontamination. [Contamination survey arXiv 2404.00699](https://arxiv.org/pdf/2404.00699); [arXiv 2311.04850](https://arxiv.org/pdf/2311.04850v1)
- Generator leakage, nearest published evidence: RoSE (arXiv 2510.06143) assumes synthetic data carries its generator's signature. It picks generators by training on one LLM's synthetic data and testing on synthetic test sets from other LLMs (round-robin), not on the same generator's output. [RoSE arXiv 2510.06143](https://arxiv.org/pdf/2510.06143)
- Li et al. (EMNLP 2023): BERT trained on GPT-3.5-generated data and tested on real data did close to real-data training on low-subjectivity tasks (news topic, spam) but lost an average 27.4% Macro-F1 on the six most subjective tasks. A same-generator test set would not reveal that gap. [Li et al. 2023, arXiv 2310.07849](https://arxiv.org/pdf/2310.07849v2)
- Temporal structure: scikit-learn warns that for time-ordered data, KFold and ShuffleSplit "would result in unreasonable correlation between training and testing instances", and offers `TimeSeriesSplit`, whose training sets only precede the test fold. [scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html)

### Inferences
- Forms of leakage ranked for this project:
  1. **Generator leakage (highest risk for the 500-example synthetic golden set).** If golden and training data come from the same LLM, prompt family, slot-value lists (insured names, addresses, perils, carriers) and rendering code, the golden set measures how well Laya learned that generator's style. Exact-hash and `template_group` exclusion do not catch this, because the shared factor is the generator, not a template key.
  2. **Template / standard-form leakage.** ACORD forms (125, 126, 140 and so on) are industry standard, so two "different" brokers can submit near-identical ACORD text. A broker-only `template_group` would put near-duplicate ACORD pages on both sides of the split. The grouping key for `acord` should include form number and edition, not just broker.
  3. **Near duplicates across groups.** The same loss-run layout from one carrier system (for example, a carrier's standard loss-run export) appears under many brokers. Group exclusion by broker misses it; similarity-based exclusion catches it.
  4. **Temporal leakage** on production data: training on documents labelled after the golden set was drawn, or on later re-submissions of the same account, leaks the same insured's documents into training.
  5. **Fitting leakage**, already covered by repo invariants 4 and 5 (no fitting of temperature or threshold on golden).
  6. **Label leakage through features** (for example, a filename or email subject containing "SOV" or "loss run") is the "illegitimate feature" case. It matters if metadata is ever added to Laya's state.
- The AIMed result (about 13 F1 points lost when moving from random to source-document-disjoint folds) is the best quantitative guide to how much a near-duplicate-heavy, template-driven corpus can overstate accuracy. Templated broker documents look structurally more like AIMed than like SST2.

### Gaps
- I could not get the full Kaufman et al. text (the hosting servers refused the connection), so the KDD Cup 2008 mechanism (patient-ID leakage, as commonly described) is not verified here.
- I found no published study that directly measures how much accuracy inflates when a classifier is evaluated on a test set from its own synthetic generator. RoSE and Li et al. are indirect evidence.
- I did not retrieve the names of all 8 types in Kapoor and Narayanan's taxonomy (the abstract does not list them). The full paper at arXiv 2207.07048 has them.

## 2. Group-aware splitting: GroupKFold, grouped holdout, source- or template-disjoint evaluation, and choosing the grouping key

### Takeaway
Use group-aware splitters so that no group appears on both sides. Choose the grouping key as the coarsest unit that a new production document could share with a training document (broker, carrier system, standard form edition, generator prompt family), and merge groups linked by near-duplicate edges. The repo's template exclusion is the right idea; the improvements are a better key and similarity-based linking.

### Cited Findings
- scikit-learn: "The i.i.d. assumption is broken if the underlying generative process yields groups of dependent samples." To test generalisation to unseen groups, "all the samples in the validation fold [must] come from groups that are not represented at all in the paired training fold." The `groups` parameter carries the group ID. [scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html)
- `GroupKFold` "ensures that the same group is not represented in both testing and training sets". Fold sizes can differ when groups are unbalanced. With `shuffle=False` it balances sample counts across folds; with `shuffle=True` it balances the number of distinct groups, ignoring group size. [scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html)
- `StratifiedGroupKFold` keeps each group in one split while trying to preserve class balance. It assigns groups greedily and "might produce imbalanced splits even if perfect stratification is possible". If class distributions are similar across groups, the docs suggest plain `GroupKFold`. [scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html)
- `LeaveOneGroupOut` holds out one group per split; `LeavePGroupsOut` holds out P groups, with overlapping test sets for P>1. `GroupShuffleSplit` gives random group-disjoint splits and is the cheap substitute for `LeavePGroupsOut`. `train_test_split` "cannot account for groups", so a grouped holdout should use `GroupShuffleSplit` indices. [scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html)
- The docs suggest `LeaveOneGroupOut` for time-based splits where "the groups could be the year of collection". [scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html)
- Elangovan et al. split AIMed folds so each source document ID appears in one fold only (AIMed (U)), which cut train/test trigram similarity from 73.15 to 20.77 and lowered F1 by over 10 points. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Min (2020), as summarised by Elangovan et al., grouped paraphrase "templates" and kept each in one split; models performed significantly worse under the strict split. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Cleanlab's docs warn that "it is questionable to include examples in a test dataset which are (nearly) duplicated" in training data. [cleanlab issue type guide](https://docs.cleanlab.ai/stable/cleanlab/datalab/guide/issue_type_description.html)

### Inferences
- **Grouping key recommendation (composite, hierarchical):**
  - `sov`: broker plus spreadsheet template (column header signature, for example a hash of the normalised header row).
  - `loss_run`: carrier or loss-run system (the producer of the layout), not the broker forwarding it.
  - `acord`: ACORD form number plus edition date. Treat all brokers' copies of the same form edition as one group.
  - `broker_email`: broker firm (and sender, if one sender writes many emails).
  - `other`: source or template where known; otherwise fall back to near-duplicate clusters.
  - Synthetic data: add the generator identity (model, prompt template ID, slot-list version) to the key. See section 3 and the generator recommendations below.
- **Merge groups linked by similarity.** Build a graph whose nodes are documents, with edges for exact hash match, same `template_group`, or near-duplicate similarity above threshold (section 3). Take connected components (union-find) as the final groups, then split on components. This catches cross-broker ACORD and carrier loss-run duplicates that a declared key misses.
- **Golden set as a grouped holdout.** Pick golden groups first (for example with `GroupShuffleSplit` or by hand to cover each class), then exclude every training row in those components. This extends invariant 3 in CLAUDE.md from "hash and template group" to "hash, template group and near-duplicate component".
- **Model selection during development:** use `StratifiedGroupKFold` (5 folds) on non-golden data so that tuning never sees the golden groups. With five classes of different sizes, stratification matters; check per-fold class counts because the greedy assignment can be lopsided.
- **Temporal guard for production-derived data:** golden or audit samples drawn from production should be dated, and training snapshots should use only documents labelled before the golden cut-off, or be grouped by account so one insured's re-submissions cannot cross.
- Choosing group size: groups should be small enough that the holdout covers many groups (for the per-class confidence intervals to mean anything) but large enough to swallow all variants of a template. As a rule of thumb, aim for at least 20 to 30 distinct groups per class in the golden set; with 500 examples and 5 classes that is about 3 to 5 examples per group.

### Gaps
- I found no published guidance specific to choosing a grouping key for business-document classification. The recommendations above are derived from the general principle in the scikit-learn docs and the template-split evidence.
- I did not verify which scikit-learn release first added `shuffle` to `GroupKFold`. The page fetched was the current stable guide (it reported version 1.9.1).

## 3. Near-duplicate detection methods with concrete settings, and trade-offs on short texts (10 to 60 words)

### Takeaway
Use cheap exact normalisation plus character-shingle MinHash/LSH with an exact Jaccard check as the main filter, and embedding cosine similarity as a second, semantic net for paraphrases. Published defaults (word 5-grams, Jaccard 0.8, 13-gram overlap) were designed for long web documents and are too coarse for 10 to 60 word texts, so thresholds must be calibrated on our own data.

### Cited Findings
- **MinHash/LSH at scale (Lee et al. 2022, NearDup):** space-tokenised 5-grams, hashed; 9,000 hash functions arranged as 450 buckets of 20 hashes; candidates confirmed if Jaccard > 0.8 and then edit similarity > 0.8. An alternative tested setting used 0.9 thresholds with 800 hashes (40 buckets of 20). [ar5iv full text of arXiv 2107.06499](https://ar5iv.labs.arxiv.org/html/2107.06499)
- **Exact substring (Lee et al., ExactSubstr):** threshold of 50 BPE tokens, chosen conservatively after finding a knee near 10 tokens. [ar5iv 2107.06499](https://ar5iv.labs.arxiv.org/html/2107.06499)
- **LSH maths (datasketch):** with b bands of r rows, retrieval probability is P(s) = 1 - (1 - s^r)^b. `MinHashLSH(threshold, num_perm, weights=(fp_weight, fn_weight))` chooses b and r; `params=(b, r)` fixes them. For threshold 0.5 and 128 permutations, weights (0.1, 0.9) give b=32, r=4 (higher recall) and (0.9, 0.1) give b=16, r=8 (higher precision). Results are approximate and unranked, so verify candidates with `MinHash.jaccard` if the threshold must hold exactly. Benchmarks showed precision and recall of 0.92 to 1.0 on a near-duplicate corpus but about 0.69 to 0.84 where many pairs sit near the threshold. Accuracy did not rise steadily with `num_perm`. [datasketch LSH docs](https://ekzhu.com/datasketch/lsh.html)
- **datasketch containment:** for "high intersection with the query" rather than high Jaccard, the docs point to LSH Ensemble. [datasketch LSH docs](https://ekzhu.com/datasketch/lsh.html)
- **SimHash (Manku, Jain and Das Sarma, WWW 2007):** applied Charikar's fingerprinting at web scale; for 8 billion pages, 64-bit fingerprints with Hamming distance k = 3 were suitable. The paper also gives an algorithm to find fingerprints within k bits quickly. [Search summary of the WWW 2007 paper](https://archives.iw3c2.org/www2007/paper215.php.html); [DOI 10.1145/1242572.1242592](http://doi.acm.org/10.1145/1242572.1242592)
- **text-dedup example configs:** MinHash `ngram_size=5`, `num_perm=240`, `threshold=0.7`, `check_false_positive=true`; SimHash `hash_bits=64`, `ngram_size=3`, `bit_diff=3`; suffix array `length_threshold=100`; Bloom filter `error_rate=1e-5`. These are sample configs, not stated defaults. [text-dedup GitHub](https://github.com/ChenghaoMou/text-dedup)
- **13-gram overlap (GPT-3):** remove examples sharing any 13-gram with the training set; examples shorter than 13 grams were matched on their whole text. [GPT-3 supplemental](https://proceedings.nips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Supplemental.pdf); [contamination survey](https://arxiv.org/pdf/2404.00699)
- **Character-substring check (GPT-4 technical report, Appendix C):** strip spaces and symbols from both sets, keeping only characters and digits; sample three 50-character substrings from each eval example (or use the whole example if under 50 characters); call it contaminated if any substring appears in a processed training example. OpenAI notes this gives false negatives on small edits and false positives too. [GPT-4 technical report, arXiv 2303.08774](https://arxiv.org/pdf/2303.08774)
- **Bag-of-words cosine (Elangovan et al.):** for each test item, take the max cosine similarity to any training item over unigram, bigram or trigram count vectors (stopwords removed); report the mean, and bin test items into [0, 0.25), [0.25, 0.5), [0.5, 0.75), [0.75, 1.0]. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- **Embedding-based (cleanlab Datalab):** flags an example as a near duplicate when its distance to its nearest neighbour is below c times D, where D is the median nearest-neighbour distance across the dataset and 0 < c < 1. Exact duplicates score 0. It needs `features` (for example sentence-transformer embeddings) or a `knn_graph`, and returns `near_duplicate_sets` and `distance_to_nearest_neighbor`. [cleanlab issue types](https://docs.cleanlab.ai/stable/cleanlab/datalab/guide/issue_type_description.html); [cleanlab text tutorial](https://docs.cleanlab.ai/stable/tutorials/datalab/text.html)
- **Embedding-based (SemDeDup in NVIDIA NeMo Curator):** embed, k-means cluster, compute pairwise cosine within clusters, and drop pairs above a threshold. Example `eps` values vary by docs version (0.01, 0.07, 0.001) and work as distance-style cut-offs. [NeMo Curator SemDeDup docs](https://docs.nvidia.com/nemo/curator/latest/curate-text/process-data/deduplication/semdedup.html)
- n-gram decontamination is bypassed by paraphrase or translation. [arXiv 2311.04850](https://arxiv.org/pdf/2311.04850v1)

### Inferences
Short-text trade-offs (10 to 60 words):
- **Word 5-gram MinHash is fragile here.** A 10-word text has only 6 word 5-grams; one changed word (an insured's name, a date, a policy number) removes up to 5 of them, so Jaccard falls from 1.0 to around 0.1 to 0.3 after a single slot substitution. Templated documents with different slot values would look unrelated. Use **character 5-grams** on normalised text (lower-case, collapse whitespace, replace digits with `0`, optionally mask emails and amounts) or **word 3-grams**. Character shingles degrade gracefully under slot substitution.
- **13-gram overlap is too blunt** for this length: most 10 to 20 word texts would fall back to whole-text matching, which is just exact match. Use an 8-word n-gram or the GPT-4-style 50-character substring check as a cheap verbatim-copy test, not as the main near-duplicate filter.
- **SimHash at 64 bits / k=3** was tuned for web pages with hundreds of features. With few features, fingerprints are noisy and k=3 behaves unpredictably. Use it only if scale demands; at our scale (thousands to low hundreds of thousands of documents) MinHash with exact Jaccard verification, or even brute-force pairwise comparison, is affordable.
- **Brute force is feasible.** 500 golden examples against 100,000 training rows is 50 million pairs: trivial for TF-IDF char n-gram cosine with a sparse matrix product, or for normalised embeddings in a dot product. Exact computation removes LSH approximation error entirely. Use LSH only once the training pool is in the millions.
- **Embeddings catch what shingles miss** (paraphrased broker emails, the same SOV described with different wording, generator rewrites). They also flag pairs that are merely the same class ("Please find attached the loss runs for..."), so an embedding threshold set too low will exclude most of a class. Calibrate rather than adopt a published number.

Recommended starting settings (calibrate before fixing):

| Check | Settings | Treat as duplicate / leak | Send to review |
|---|---|---|---|
| Exact | SHA-256 of normalised text (lower-case, whitespace collapsed, digits to 0, punctuation stripped) | any match | n/a |
| Verbatim span | GPT-4 style: three 50-char substrings per golden item, or any shared 8-word n-gram | any match | n/a |
| Lexical near-dup | character 5-gram shingles; datasketch `MinHash(num_perm=256)`, `MinHashLSH(threshold=0.5, weights=(0.2, 0.8))` for candidates, then exact Jaccard | Jaccard >= 0.8 (Lee et al. level) | 0.5 to 0.8 |
| Lexical, BoW | Elangovan-style max cosine over word unigram/bigram counts | >= 0.75 (top Elangovan bin) | 0.5 to 0.75 |
| Semantic | sentence-transformer embeddings, cosine to nearest training item | calibrated cut-off (see below) | calibrated band |

Calibrating the semantic threshold: take pairs known to share a template (same `template_group`, different slot values) and pairs known to be independent but same-class (different groups, same `doc_type`). Plot the two nearest-neighbour cosine distributions and set the duplicate cut-off where same-template pairs dominate (for example, the 5th percentile of same-template similarity, if that sits above the 99th percentile of independent same-class similarity). If the two distributions overlap heavily, rely on lexical checks plus group keys and use embeddings only for review flags.

Generator-leakage-specific checks for the synthetic golden set:
- Compare golden against training on the slot values themselves (insured names, addresses, carriers, policy numbers). Any shared, non-generic value (not "USA", not "Property") is a leak signal even when text similarity is low.
- Generate golden with a different LLM and different prompt templates and slot lists from training, and record generator identity in the group key. Run a RoSE-style cross-check: score the model on golden-from-generator-B after training on generator-A data, and compare with a same-generator test split. A large gap measures generator leakage directly.
- Keep a real, anonymised slice (even 50 to 100 documents) as the final check, following Li et al.'s finding that synthetic-trained models can lose a lot on real test data.

### Gaps
- I did not retrieve Broder (1997) itself, so the original shingle size and resemblance thresholds are not cited here.
- I found no published, sourced cosine-similarity threshold for "near duplicate" with sentence-transformer embeddings. The NeMo `eps` values are configuration examples, not validated thresholds, and depend on the embedding model.
- I did not confirm cleanlab's default `threshold` value for near duplicates (the docs page did not state it); check the installed version's `NearDuplicateIssueManager` signature.
- I found no study that measures MinHash or SimHash accuracy specifically on 10 to 60 word texts. The short-text arguments above are arithmetic on shingle counts, not empirical results.

## 4. Tooling and how to run a train-versus-golden contamination report

### Takeaway
Everything needed is available in standard Python libraries: datasketch (MinHash/LSH), scikit-learn (TF-IDF cosine and group splitters), sentence-transformers plus cleanlab or a plain nearest-neighbour search (semantic), and text-dedup for large-scale batch dedup. The report should, for each golden item, record its nearest training neighbour under each check, then summarise flagged counts and accuracy by similarity bin.

### Cited Findings
- datasketch `MinHash` / `MinHashLSH`: `insert(key, minhash)`, `query(minhash)` returns unranked candidates; `merge` combines indexes; Redis/Cassandra storage with `insertion_session()` for bulk insert; MinHash LSH Forest for top-k; LSH Ensemble for containment. [datasketch docs](https://ekzhu.com/datasketch/lsh.html)
- text-dedup provides MinHash+LSH, SimHash (64 or 128 bit), suffix array (exact substring) and Bloom filter (exact) modules, run as `python -m text_dedup.minhash` with a `config.toml`; Apache-2.0, Python 3.12+; no tagged releases on GitHub. [text-dedup GitHub](https://github.com/ChenghaoMou/text-dedup)
- cleanlab Datalab: `lab.find_issues(pred_probs=..., features=text_embeddings)` then `lab.get_issues("near_duplicate")`, with `near_duplicate_score`, `near_duplicate_sets`, `distance_to_nearest_neighbor`. The tutorial uses sentence-transformers embeddings. [cleanlab text tutorial](https://docs.cleanlab.ai/stable/tutorials/datalab/text.html)
- Elangovan et al. Algorithm 1: for each test item, best-match similarity against all training items; average across the test set as the overlap indicator; then evaluate the model per similarity interval and per similarity quartile. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- GPT-3 and GPT-4 both report scores on the full benchmark and on the "clean" (decontaminated) subset and compare them. [GPT-3 supplemental](https://proceedings.nips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Supplemental.pdf); [GPT-4 technical report](https://arxiv.org/pdf/2303.08774)

### Inferences
Proposed contamination report (a new service behind a port, so it fits the hexagonal layout; run on every snapshot build and fail the build on any hard leak):

1. **Normalise** golden and snapshot texts identically (function shared with `doc_hash`).
2. **Exact:** hash join. Hard fail on any hit (already enforced; keep the test).
3. **Group:** set intersection of golden and training group keys (already enforced) plus the new composite key and near-duplicate components.
4. **Verbatim:** 50-character substring sampling and 8-word n-gram set intersection. Hard fail.
5. **Lexical:** char 5-gram TF-IDF cosine (scikit-learn `TfidfVectorizer(analyzer="char_wb", ngram_range=(5,5))`, then `linear_kernel`) or datasketch MinHash with exact Jaccard. Record max similarity and nearest training ID for each golden item. Hard fail at >= 0.8; review list for 0.5 to 0.8.
6. **Semantic:** sentence-transformers embeddings (normalised), max cosine per golden item via matrix product; or cleanlab Datalab on the union of golden and training with a `split` column, keeping only flagged sets that cross the split.
7. **Slot overlap** (synthetic only): shared rare entities between golden and training.
8. **Output** a JSON or Markdown table in `var/runs/<ts>/`: per golden item `{id, doc_type, group, max_jaccard, max_bow_cosine, max_embed_cosine, nearest_train_id, flags}`; summary counts per class and per check; histogram of max similarity; and model accuracy per Elangovan similarity bin ([0, 0.25), [0.25, 0.5), [0.5, 0.75), [0.75, 1.0]). Accuracy that rises sharply with similarity shows the headline number is leaning on memorisation.
9. **Wire to promotion:** the promotion gate should refuse a candidate whose snapshot has any hard-fail contamination, and the eval report should show the clean-subset score next to the full score, as the GPT-3/GPT-4 reports do.

Library choice: at the current scale, scikit-learn TF-IDF plus sentence-transformers brute force is simpler and exact. Add datasketch LSH (or text-dedup) only when the training pool grows to millions of rows or moves to the Iceberg store.

### Gaps
- I did not check current (October 2026) release versions of datasketch, cleanlab or sentence-transformers, or which sentence-transformer model works best on insurance text. Pin and test whatever is installed.
- cleanlab's docs do not describe a built-in "train versus test" mode; the cross-split filter above is my construction.

## 5. Evaluating generalisation to unseen sources (out-of-distribution slice) versus in-distribution, and reporting both

### Takeaway
Report at least two numbers: in-distribution (held-out documents from groups also seen in training, deduplicated) and out-of-distribution (wholly unseen groups, plus unseen generator and real documents). The gap between them is itself a key metric. Published evidence shows that gap can be 10 or more F1 points for template-heavy data.

### Cited Findings
- scikit-learn frames group splitting as asking whether "a model trained on a particular set of groups generalizes well to the unseen groups". [scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html)
- AIMed: BioBERT F1 77.9 on random folds versus 64.4 on source-document-disjoint folds; similar 13 to 14 point drops for BiLSTM and ConvRes. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Elangovan et al. evaluate per similarity interval and per similarity quartile; both views show performance falling as test items get less similar to training (ChEMU 96.7 to 85.6; BC2GM 82.4 to 74.5). [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Template-disjoint splits (Min 2020) made models perform significantly worse than random splits. [Elangovan et al. 2021](https://aclanthology.org/2021.eacl-main.113.pdf)
- Kapoor and Narayanan list "test set not drawn from the distribution of interest" as a leakage type in its own right. [Princeton reproducibility site](https://reproducible.cs.princeton.edu/)
- Training on synthetic data can transfer poorly to real data (27.4% Macro-F1 average drop on subjective tasks), and generator-crossed evaluation is proposed when human test sets are missing. [Li et al. 2023](https://arxiv.org/pdf/2310.07849v2); [RoSE](https://arxiv.org/pdf/2510.06143)

### Inferences
Suggested structure for the ~500-example golden set and its report:
- **Slices (tag every golden row):**
  - `id_template`: groups that also exist in training, but the documents themselves pass all near-duplicate checks (about 30%). Measures in-template generalisation to new slot values. Note: this deliberately relaxes the current "exclude by template group" rule for this slice only, so it needs a separate flag; otherwise keep invariant 3 as is for the main exam.
  - `ood_template`: groups absent from training (about 50%, the main exam score and the one the promotion gate should use).
  - `ood_generator`: produced by a different LLM and prompt family from any training generator (about 20%, can overlap with `ood_template`).
  - `real`: anonymised real broker documents, as many as can be obtained, reported separately even when small.
- **Report per slice:** accuracy, macro-F1, per-class recall, ECE and the auto-route rate at the current threshold, each with a 95% confidence interval (bootstrap over groups, not over documents, since documents in a group are correlated). With 500 examples spread over slices and five classes, per-class per-slice counts will be small; show counts next to every metric.
- **Headline gap metric:** `ood_template accuracy - id_template accuracy`. A large gap means the model leans on template memory; track it across model versions.
- **Promotion gate:** extend `PromotionPolicy` to require no regression on the `ood_template` slice specifically, not only overall, so a candidate cannot buy in-distribution gains with out-of-distribution losses.
- **Leave-one-group-out diagnostic:** on training data (never golden), run `LeaveOneGroupOut` or `GroupKFold` by broker or carrier to see which sources the model fails on when unseen; this guides what to add to golden and training.

### Gaps
- I found no source giving recommended slice proportions for an in-distribution versus out-of-distribution golden set; the 30/50/20 split is a judgement call.
- I did not find published guidance on minimum per-group sample counts for a grouped bootstrap; with few groups per class the intervals will be wide and should be reported as such.
