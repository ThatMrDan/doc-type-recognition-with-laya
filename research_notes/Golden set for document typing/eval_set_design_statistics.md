# Designing a golden evaluation set for a 5-class document classifier: statistics, sizing, versioning

Case: 5 classes (`sov`, `loss_run`, `acord`, `broker_email`, `other`), about 500 golden examples, and promotion gates that reject a candidate if any per-class recall drops by more than 0.05 or ECE rises by more than 0.02.

Where a number below is marked "own calculation", I computed it in Python for these notes (Wilson and Clopper-Pearson via scipy, McNemar power via the standard normal approximation, ECE noise via Monte Carlo simulation). The formulas are cited. The numbers can be reproduced from the formulas given.

## 1. How many examples per class to estimate per-class recall within a given margin?

### Takeaway
With 100 examples per class, a recall near 0.90 has a 95% Wilson half-width of about ±0.06, and near 0.95 about ±0.045. Getting ±0.05 at recall 0.80 needs roughly 250 per class, and at 0.90 roughly 140. So 500 examples (100 per class) measure each class's recall to about ±0.05, not much better. That is too coarse to tell from one measurement whether a 0.05 drop is real, unless the comparison is paired (section 2).

### Cited Findings
- **Wilson score interval** for x successes in n trials, with p̂ = x/n and z = 1.96: centre = (p̂ + z²/2n)/(1 + z²/n); half-width = z·sqrt(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n). It inverts the score test, so it never goes outside [0,1] and does not collapse to width 0 when p̂ = 0 or 1. — [Wilson 1927, JASA](https://doi.org/10.1080/01621459.1927.10502953)
- **Agresti-Coull ("add two successes and two failures")**: ñ = n + z², p̃ = (x + z²/2)/ñ, then apply the Wald formula with p̃ and ñ. Agresti and Coull report that this has better coverage than the exact Clopper-Pearson interval for interval estimation. — [Agresti & Coull 1998, The American Statistician](https://doi.org/10.1080/00031305.1998.10480550)
- Brown, Cai and DasGupta show that the Wald interval p̂ ± z·sqrt(p̂(1−p̂)/n) has erratic and poor coverage, even at large n and especially near 0 or 1. They recommend Wilson or Jeffreys for small n and Wilson, Jeffreys or Agresti-Coull for larger n, and call Clopper-Pearson "wastefully conservative". — [Brown, Cai & DasGupta 2001, Statistical Science](https://doi.org/10.1214/ss/1009213286). Caveat: the full text did not load during this research. This summary comes from the widely cited conclusions of the paper, not from a re-read.
- Planning sample size with the normal approximation: n = z²·p(1−p)/E² for margin E. — standard result, same sources as above.
- **Worked numbers (own calculation, 95%, Wilson; Clopper-Pearson in brackets):**

| n per class | observed recall | Wilson 95% CI | half-width | Clopper-Pearson |
|---|---|---|---|---|
| 50 | 0.80 (40/50) | 0.670 to 0.888 | 0.109 | 0.663 to 0.900 |
| 50 | 0.90 (45/50) | 0.786 to 0.957 | 0.085 | 0.782 to 0.967 |
| 50 | 0.96 (48/50) | 0.865 to 0.989 | 0.062 | 0.863 to 0.995 |
| 50 | 1.00 (50/50) | 0.929 to 1.000 | 0.036 | 0.929 to 1.000 |
| 100 | 0.80 | 0.711 to 0.867 | 0.078 | 0.708 to 0.873 |
| 100 | 0.90 | 0.826 to 0.945 | 0.060 | 0.824 to 0.951 |
| 100 | 0.95 | 0.888 to 0.978 | 0.045 | 0.887 to 0.984 |
| 100 | 0.98 | 0.930 to 0.994 | 0.032 | 0.930 to 0.998 |
| 100 | 1.00 | 0.963 to 1.000 | 0.018 | 0.964 to 1.000 |
| 150 | 0.80 | 0.729 to 0.856 | 0.064 | 0.727 to 0.861 |
| 150 | 0.90 | 0.842 to 0.938 | 0.048 | 0.840 to 0.943 |
| 150 | 0.947 | 0.898 to 0.973 | 0.037 | 0.898 to 0.977 |
| 150 | 0.98 | 0.943 to 0.993 | 0.025 | 0.943 to 0.996 |

- **n per class needed for a ±0.05 margin (normal approximation, own calculation):** 385 at p = 0.5, 246 at p = 0.8, 139 at p = 0.9, 73 at p = 0.95. **For ±0.03:** 683 at 0.8, 385 at 0.9, 203 at 0.95.
- **Zero errors observed ("rule of three"):** with 0 misses in n, the one-sided 95% upper bound on the miss rate is about 3/n. That is 0.06 at n = 50, 0.03 at n = 100 and 0.02 at n = 150 (exact values 1 − 0.05^(1/n) = 0.058, 0.030, 0.020; own calculation). — [Hanley & Lippman-Hand 1983, JAMA](https://doi.org/10.1001/jama.1983.03330370053031)
- Per-class precision has a random denominator: the number of predictions of that class, not the number of true examples. Its interval is a Wilson interval on that count, so it widens when a class is rarely predicted. — follows directly from the binomial setup above.

### Inferences
- With 100 per class, report each class's recall with a Wilson interval (about ±0.045 to ±0.06 for recalls of 0.90 to 0.95). Do not report it as a bare point estimate.
- If any class is expected to have recall around 0.8 (`other` is the likely candidate, because it is heterogeneous), it needs about 250 examples to reach ±0.05. A practical split of 500 might give `other` about 150 and the other four classes about 90 each. Weigh that against the precision needed for the four structured classes.
- Use Wilson, or Jeffreys, everywhere. Never use Wald: at p̂ = 1.0 it gives a width of 0, which happens often for easy classes such as `acord`.

### Gaps
- None of the sources gives a sizing rule specific to document classification. The arithmetic above is generic binomial.

## 2. Comparing two models on the same eval set: paired tests, bootstrap, detectable differences

### Takeaway
Always compare the candidate and the incumbent paired, on the same items. Use the McNemar test (exact or mid-p) on the items where they disagree, or a paired bootstrap of the difference. The detectable difference depends on the discordance rate ψ, the share of items where exactly one model is right, not on the overall accuracy. With N = 500 and ψ = 5 to 10%, the minimum detectable accuracy difference (80% power, α = 0.05) is about 0.03 to 0.04. An unpaired comparison would only detect about 0.05. For per-class recall with about 100 items per class, the detectable change is about 0.04 to 0.10, depending on ψ.

### Cited Findings
- Dietterich compared five tests. A two-proportions test and a paired t-test over repeated random splits had high Type I error and "should not be used". McNemar's test had low Type I error. For algorithms that can be run only once (our case: one candidate checkpoint against one incumbent on a fixed golden set), McNemar's test is the only test with acceptable Type I error. The 5×2cv t-test is recommended when an algorithm can be retrained 10 times. — [Dietterich 1998, Neural Computation (abstract)](https://mlanthology.org/neco/1998/dietterich1998neco-approximate/); [preprint](https://web.engr.oregonstate.edu/~tgd/publications/dietterich-approximate-statistical-tests-nc1998.pdf)
- **McNemar setup:** b = items the incumbent got right and the candidate got wrong, c = the reverse. Under H0, b ~ Binomial(b + c, 0.5). The asymptotic statistic is (b − c)²/(b + c) ~ χ²₁. The continuity-corrected version is (|b − c| − 1)²/(b + c). — [Dietterich 1998](https://mlanthology.org/neco/1998/dietterich1998neco-approximate/)
- Fagerland, Lydersen and Laake recommend the **McNemar mid-p test**: compute the exact one-sided conditional binomial p-value, subtract half the probability of the observed count, and double the result. It did not exceed the nominal level in any of 9,595 scenarios. The exact conditional test and the continuity-corrected asymptotic test "did not perform well" (too conservative). The uncorrected asymptotic test is acceptable if small violations of the nominal level are tolerable. — [Fagerland et al. 2013, BMC Med Res Methodol (PubMed)](https://pubmed.ncbi.nlm.nih.gov/23848987/); [supplementary calculation note](https://www.springermedizin.de/resource/supplementary/12874_2013_967_MOESM1_ESM.pdf/9433268)
- Card et al. found that many NLP comparisons are underpowered because test sets are small. For example, typical machine translation test sets of 2,000 sentences have about 75% power to detect a 1 BLEU difference. They recommend running a power analysis before relying on an evaluation set, and released notebooks for doing it. — [Card et al. 2020, EMNLP](https://arxiv.org/abs/2010.06595)
- **Sample size for a paired proportion difference** (Connor-style normal approximation): N = [z_{α/2}·√ψ + z_β·√(ψ − Δ²)]² / Δ², where Δ = the difference in accuracy and ψ = the discordant proportion. This is the standard formula for McNemar power; the numbers below are my own calculation.
- **Minimum detectable difference, own calculation (two-sided α = 0.05, power 80%):**

| N | discordant ψ = 2% | 5% | 10% | 15% |
|---|---|---|---|---|
| 100 (one class) | ~0.02* | ~0.05* | 0.088 | 0.107 |
| 500 (whole set) | 0.018* | 0.028 | 0.040 | 0.048 |

  *When Δ ≈ ψ, almost every disagreement has to go one way. In practice, the detectable difference at low discordance is set by ψ itself.
  For comparison, an unpaired two-proportion test at accuracy 0.9 detects only about 0.119 with n = 100 and about 0.053 with n = 500 per arm (own calculation).
- **Per-class recall, own calculation (n_c items of one class, discordance ψ within that class):** n_c = 50 detects 0.04 to 0.12, about equal to ψ. n_c = 100 detects 0.04, 0.078 and 0.096 at ψ = 4%, 8% and 12%. n_c = 150 detects 0.04, 0.064 and 0.079.
- **False-trip rate of the "drop > 0.05" point gate when there is no true change (own Monte Carlo, 20,000 runs; disagreements split 50/50):**

| n per class | ψ = 4% | ψ = 8% | ψ = 12% |
|---|---|---|---|
| 50 | 3.8% | 10.1% | 14.7% |
| 100 | 0.4% | 2.8% | 5.2% |
| 150 | 0.2% | 1.4% | 3.7% |

  With five classes, these rates compound. For example, at n_c = 100 and ψ = 8%, 1 − (1 − 0.028)^5 ≈ 13% of promotions of an equally good model would be wrongly blocked.
- **Paired bootstrap:** resample item indices with replacement, B ≥ 2,000 times, and recompute metric(candidate) − metric(incumbent) on each resample. Report a percentile or BCa interval. Resampling items, not each model separately, keeps the pairing. This works for any metric, including ECE, macro-F1 and per-class recall. — [Efron & Tibshirani 1993, An Introduction to the Bootstrap](https://doi.org/10.1201/9780429246593) (standard method); also covered in [Raschka 2018, model evaluation review](https://arxiv.org/abs/1811.12808)

### Inferences
- Change the promotion rule from "point drop > 0.05" to a statistical rule. Options: block if the upper limit of the 95% paired-bootstrap (or Newcombe paired) interval for recall_cand − recall_inc is below −0.05 (a non-inferiority framing). Or block if the point drop exceeds 0.05 and the mid-p McNemar on that class is significant. Either way, log b and c for every class.
- At about 100 per class, the gate can detect drops of about 0.05 only when the models disagree on fewer than about 5 to 8% of a class's items. That is typical of an incremental fine-tune, but not of a new base model.
- Treat the five per-class tests as a family. Either use Holm correction, or accept the higher false-block rate on purpose, because a false block costs less than a false promotion.

### Gaps
- I did not fetch Newcombe's paired-difference interval paper (1998, Statistics in Medicine). It is the standard closed-form CI for a paired difference of proportions, if the team prefers it to the bootstrap.

## 3. Production prior or balanced/stratified eval set? How to report both

### Takeaway
Build the golden set stratified (enough examples per class for per-class recall, as in section 1). Then report headline accuracy and precision reweighted to the production prior. Recall is conditional on the true class, so it does not depend on the prior. Precision, accuracy and ECE do depend on the class mix, and must be reweighted or computed on a separate random, prior-matching sample. Balanced sampling costs little in headline-accuracy precision.

### Cited Findings
- Google's Rules of ML recommend evaluating on data gathered after the training window (Rule #33: train on data up to January 5th, test on January 6th). They recommend labelling a small random sample of live traffic as an unbiased held-out set (Rule #34: "Ten thousand examples is enough to estimate performance quite accurately"). Rule #30: don't drop sampled data arbitrarily; use importance weights. — [Google, Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
- Label-shift adjustment: when class-conditional distributions are stable and only priors change, posteriors can be corrected to new priors. The ratio π_new/π_train is the importance weight per class. — [Saerens, Latinne & Decaestecker 2002, Neural Computation](https://doi.org/10.1162/089976602753284446)
- **Reweighting formulas** (follow from Bayes' rule and stratified sampling theory, [Cochran 1977, Sampling Techniques](https://www.wiley.com/en-us/Sampling+Techniques%2C+3rd+Edition-p-9780471162407)). Let C[j,k] = P(pred k | true j) be the row-normalised confusion matrix from the stratified set, and π the production prior.
  - Accuracy_prod = Σ_k π_k·recall_k; Var ≈ Σ_k π_k²·r_k(1 − r_k)/n_k.
  - Precision_prod(k) = π_k·C[k,k] / Σ_j π_j·C[j,k].
  - Neyman-optimal allocation for estimating one prior-weighted metric: n_k ∝ π_k·sqrt(r_k(1 − r_k)).
- **Worked example (own calculation, illustrative prior** π = broker_email 0.40, other 0.25, sov 0.15, loss_run 0.12, acord 0.08, **not a measured prior**; all recalls 0.95). With a balanced split of 100 per class, the prior-weighted accuracy has SE 0.0112 (95% ± 0.022). A proportional random sample of 500 gives SE 0.0097 (± 0.019). Balanced sampling costs only about 15% wider headline intervals, and it gives `acord` 100 examples instead of 40.

### Inferences
- Store each golden item's stratum, and store the production prior used for weighting (estimated from the decision log's routed volume, refreshed and versioned). Report three numbers: macro (unweighted per-class mean), prior-weighted, and per class.
- Small-class precision is the metric most distorted by a balanced set. A balanced set overstates the true mixing rate of a rare class's false positives, or understates it, depending on direction. Always reweight precision before quoting it to underwriters.
- ECE computed on a balanced set measures calibration under the balanced mix, which is not the production mix. Compute it with per-item weights π_k/(n_k/N), or on the random audit sample. Note that CLAUDE.md invariant 5 already reserves the audit sample for fitting, not for evaluation, so a separate prior-matching slice would be needed.

### Gaps
- No primary source gives a recommended balanced-versus-prior split for multi-class document typing. The recommendation above is derived from sampling theory.

## 4. Calibration evaluation: sample needs, binned-ECE bias, binning, alternatives

### Takeaway
At n = 500, binned ECE is too noisy and too biased for a ±0.02 gate to be reliable. Roelofs et al. find that detecting 2% miscalibration needs more than 10,000 samples, and that with fewer than 500 samples only miscalibration above about 10% is reliably detected. In my simulation, a perfectly calibrated model still shows ECE ≈ 0.026 (15 equal-width bins) at n = 500. Gate on a paired bootstrap difference of a lower-bias estimator (debiased ECE or ECE-sweep) together with a proper scoring rule (Brier or log loss), and show reliability diagrams with consistency bands.

### Cited Findings
- **Guo et al. 2017** popularised ECE = Σ_b (|B_b|/n)·|acc(B_b) − conf(B_b)| with 15 equal-width bins on the top-label confidence, along with temperature scaling. They showed that modern deep networks are over-confident. — [Guo et al. 2017, ICML](https://arxiv.org/abs/1706.04599)
- **Nixon et al. 2019** list the flaws of ECE. It uses only the max probability and does not condition on class. Fixed bins on sharp models are dominated by "typically one or two" bins. The bin count trades bias against variance. Over- and under-confidence cancel within a bin. The L1 norm distorts comparisons, and implementations are ambiguous. They propose:
  - SCE = (1/K) Σ_k Σ_b (n_bk/N)·|acc(b,k) − conf(b,k)| (classwise, static bins).
  - ACE: the same idea with equal-mass ranges, (1/(KR)) Σ_k Σ_r |acc(r,k) − conf(r,k)|.
  - TACE: ACE restricted to predictions above a threshold ε, for example 0.01.

  They recommend class-conditional measurement, adaptive bins (more stable rank order across bin counts) and the L2 norm. The choice of metric "drastically" changes the rank order of recalibration methods. — [Nixon et al. 2019, CVPR-W](https://arxiv.org/html/1904.01685)
- **Kumar et al. 2019:** binned calibration error underestimates true calibration error in the limit. Histogram binning needs O(B/ε²) samples; scaling methods need O(1/ε²). A debiased estimator from meteorology estimates calibration error with O(√B) samples instead of O(B), and gives more accurate estimates than plugin estimators. — [Kumar, Liang & Ma 2019, NeurIPS](https://arxiv.org/abs/1909.10155)
- **Roelofs et al. 2022:**
  - ECE_bin is systematically biased, and "paradoxically the bias is most severe for perfectly calibrated models". At n = 200 with 15 equal-width bins, a perfectly calibrated model shows large ECE.
  - Equal-mass binning has lower bias than equal-width.
  - There is an optimal bin count for each n, and it grows with n.
  - ECE_debias (the jackknife per-bin bias correction of Ferro & Fricker 2012 and Bröcker 2012) is better for well-calibrated models. ECE_sweep (equal-mass bins, choosing the largest bin count for which bin accuracies stay monotonic) is better for miscalibrated models.
  - "To detect a miscalibration of 2%, over 10,000 samples are needed; and if one has under 500 samples, the miscalibration must be greater than 10% to be detected reliably" (Beta(1,1) confidence simulation, α = 0.05).

  — [Roelofs, Cain, Shlens & Mozer 2022, AISTATS](https://arxiv.org/abs/2012.08668)
- **Own simulation** (perfectly calibrated model, confidence ~ Beta(9,1), mean 0.9, 500 replicates, 15 bins). Mean ECE at a true value of 0:

| n | equal-width mean | sd | equal-mass mean | sd |
|---|---|---|---|---|
| 100 | 0.057 | 0.017 | 0.079 | 0.017 |
| 500 | 0.026 | 0.008 | 0.037 | 0.008 |
| 2,000 | 0.014 | 0.004 | 0.018 | 0.004 |
| 10,000 | 0.006 | 0.002 | 0.008 | 0.002 |

  For this confidence distribution, equal-mass bins showed more bias than equal-width at a true value of 0. This differs from Roelofs' finding across realistic and miscalibrated settings: the outcome depends on the confidence distribution and bin count, which is exactly Roelofs' point about choosing bins adaptively.
- **Own simulation of the ECE gate:** two models with identical true calibration, correlated predictions, 500 shared items. ECE(candidate) − ECE(incumbent) had sd ≈ 0.009, and the "+0.02" gate tripped 1.4% of the time with no real change. At n = 2,000 the sd was ≈ 0.005. The gate catches only fairly large real changes: a true +0.02 change would be seen as anywhere from about 0.00 to 0.04.
- **Classwise ECE** (Kull et al.): the average over classes of the binned calibration error of each class's one-vs-rest probability. — [Kull et al. 2019, NeurIPS (Dirichlet calibration)](https://arxiv.org/abs/1910.12656)
- **Proper scoring rules:** the Brier score and log loss are strictly proper. They need no binning, and their per-item scores can be paired-bootstrapped. — [Gneiting & Raftery 2007, JASA](https://doi.org/10.1198/016214506000001437). Murphy's decomposition splits Brier into reliability, resolution and uncertainty. — [Murphy 1973, J. Applied Meteorology](https://doi.org/10.1175/1520-0450(1973)012%3C0595:ANVPOT%3E2.0.CO;2)
- **Reliability diagrams with consistency bars:** resample outcomes from the predicted probabilities, assuming the model is calibrated, to draw the range an observed bin frequency could take by chance. — [Bröcker & Smith 2007, Weather and Forecasting](https://doi.org/10.1175/WAF993.1). The CORP method uses isotonic (PAV) regression in place of ad hoc binning, adds consistency and confidence bands, and gives a CORP decomposition of a score into miscalibration, discrimination and uncertainty. — [Dimitriadis, Gneiting & Jordan 2021, PNAS](https://doi.org/10.1073/pnas.2016191118). The page returned 403 during this research; the summary is from the paper's known content.

### Inferences
- For a 5-class top-label confidence at n = 500, change the gate to: the paired bootstrap 95% interval of ΔECE_debias (or Δ ECE_sweep), with the gate on its lower bound > 0.02. Also gate on Brier or log loss non-inferiority, which is less noisy and needs no binning.
- Report classwise calibration only descriptively. With 100 items per class it is far too noisy to gate on.
- Fix the ECE implementation in the golden-set version: number of bins, equal-width or equal-mass, norm, and top-label or classwise. Bias depends on all of these, so a candidate and the incumbent must be scored with an identical estimator.
- CLAUDE.md invariant 5 forbids fitting temperature on the golden set. That is consistent with this literature: fitting on the same items being scored would bias ECE downwards.

### Gaps
- I did not find a closed-form sample-size formula for ECE at a given margin. The available evidence is simulation-based (Roelofs, plus my own).

## 5. Selective classification / coverage-risk at a confidence threshold

### Takeaway
At a threshold, report coverage (the share auto-routed) and selective risk (the error rate among auto-routed items), each with a Wilson interval. The effective sample for risk is N × coverage, not N. At a low target risk, the interval is wide relative to the risk: at 80% coverage of 500 (400 accepted) and 2% observed risk, the 95% CI is 1.0 to 3.9%. AURC or E-AURC summarises the ranking quality of confidence over all thresholds.

### Cited Findings
- **Definitions** (Geifman, Uziel & El-Yaniv):
  - Coverage φ = E[g(x)], estimated as (1/m)·Σ g(x_i).
  - Selective risk R = E[ℓ·g]/φ.
  - The risk-coverage curve plots risk against coverage as the threshold varies.
  - AURC = (1/n)·Σ_θ r̂(f, g_θ) over thresholds at each observed confidence.
  - The optimal AURC* (all errors ranked below all correct items) ≈ r̂ + (1 − r̂)·ln(1 − r̂).
  - E-AURC = AURC − AURC*, which removes the dependence on the base error rate. It is computed on an independent labelled set, not the training set.

  — [Geifman, Uziel & El-Yaniv 2019, ICLR "Bias-reduced uncertainty estimation"](https://arxiv.org/html/1805.08206v4)
- **Selection with Guaranteed Risk (SGR):** choose the threshold on a labelled set so that, with probability 1 − δ, true selective risk ≤ r*, using a binomial tail bound with a union bound over the thresholds tried. — [Geifman & El-Yaniv 2017, NeurIPS "Selective classification for deep neural networks"](https://arxiv.org/abs/1705.08500)
- **Own calculation (Wilson 95%):**
  - 8 errors out of 400 accepted → risk 0.020, CI 0.010 to 0.039.
  - 4 out of 400 → 0.010, CI 0.004 to 0.025.
  - 5 out of 250 → 0.020, CI 0.009 to 0.046.
  - AURC* at a 10% base error rate ≈ 0.0052.

### Inferences
- To show auto-route risk ≤ 2% with 95% confidence, roughly 400 or more accepted items with ≤ 3 to 4 errors are needed (rule of three: zero errors in 150 gives an upper bound ≈ 2%). A 500-item golden set can evaluate this threshold, but not tightly.
- The threshold is chosen on the audit sample (invariant 5). The golden set should only report the resulting coverage and risk. Using the golden set to choose among thresholds would turn it into a tuning set. If a guarantee is wanted, use SGR-style binomial bounds on the audit sample.
- Compare candidate and incumbent risk at matched coverage, not at the same raw threshold, because their confidence scales differ. Use a paired bootstrap of the risk difference at coverage c.

### Gaps
- No source found gives power calculations specifically for AURC differences. The paired bootstrap is the practical route.

## 6. Versioning and freezing golden sets; test-set reuse

### Takeaway
Treat the golden set as an immutable, content-hashed, versioned artefact with a datasheet. Freeze the metric code and the label guidelines alongside it. Never use it for tuning (thresholds, temperature, prompt or feature choices). Limit and log how often it is queried. Refresh it on a schedule with a new version, rather than editing it in place. Adaptive reuse can overfit a holdout. Recht et al. found that most of the drop on fresh test sets came from distribution shift, not adaptive overfitting, which argues for periodically drawing fresh in-distribution data as well.

### Cited Findings
- **Dwork et al.:** "Reusing a holdout set adaptively multiple times can easily lead to overfitting to the holdout set itself." They give a reusable-holdout mechanism (Thresholdout) based on differential privacy and description length, which can validate many adaptively chosen hypotheses. — [Dwork et al. 2015, Science / arXiv](https://arxiv.org/abs/1506.02629)
- **Blum & Hardt's Ladder:** leaderboard participants who evaluate repeatedly overfit the holdout. The Ladder reports a new score only when a submission beats the previous best by a margin, which gives guarantees in a fully adaptive setting. Common fixes such as limiting answer precision or the number of submissions are poorly understood heuristics. — [Blum & Hardt 2015, ICML](https://arxiv.org/abs/1502.04585)
- **Recht et al.:** on newly collected CIFAR-10 and ImageNet test sets built with the original protocol, accuracy dropped by 3 to 15% and 11 to 14%. The ranking of models was largely preserved. The authors attribute the drops to failure to generalise to slightly "harder" images, not to adaptive overfitting from test-set reuse. — [Recht et al. 2019, ICML](https://arxiv.org/abs/1902.10811)
- **Datasheets for Datasets** propose standard documentation covering motivation, composition, collection process, recommended uses and more, to improve transparency and accountability. The full question list also covers preprocessing and labelling, distribution and maintenance (including versioning and errata). — [Gebru et al. 2018/2021](https://arxiv.org/abs/1803.09010). Only the abstract was fetched; the section list is from the paper's known structure.
- **Model Cards** report evaluation results disaggregated by relevant factors, with the evaluation data described. — [Mitchell et al. 2019, FAT*](https://arxiv.org/abs/1810.03993)
- **Rules of ML:** test on data from after the training window (Rule #33). Check held-out performance before export (Rule #9). Measure skew between training, holdout, next-day and live data (Rule #37). "The only easy launch decisions are when all metrics get better (or at least do not get worse)" (Rule #39). — [Google, Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml)

### Inferences (practices for this repo)
- **Version identifier:** `golden/vN` with a manifest of item SHA-256 hashes, template-group IDs, labels, label source and adjudication notes, stratum, and collection date. Also store the hash of the metric code and its configuration (ECE bins, norm), so two runs are comparable only when both hashes match. This extends CLAUDE.md invariant 3, which already excludes training documents by hash and template group.
- **Labels:** double-label with adjudication. Record inter-annotator agreement (for example Cohen's κ) in the datasheet. Label noise in the golden set puts a ceiling on measurable accuracy, and adds variance that the binomial maths above ignores.
- **Freezing:** corrections to labels create v(N+1) with an errata entry. Re-score the incumbent on v(N+1) before comparing, and never mix versions in one comparison.
- **Reuse budget:** log every golden evaluation (who, which model, result). Show only gate pass or fail plus coarse metrics to people iterating on models, in the spirit of the Ladder. Keep a small "sequestered" slice (for example 100 items) that is scored only at release, to check for drift from repeated use of the main set.
- **Refresh cadence:** no primary source gives a fixed cadence. A reasonable rule is to add a new time-sliced tranche each quarter, or when the decision-log class prior or template mix shifts measurably. Retire the oldest tranche into the training pool only after it is no longer used for comparisons, and run the leakage check again.

### Gaps
- I found no primary industry source prescribing a refresh interval or a numeric reuse budget for internal golden sets. The cadence above is a recommendation, not a sourced fact.
- Tooling for dataset versioning (DVC, lakeFS, Iceberg snapshot tags) was not researched here.

## 7. Hard and edge cases: a separate challenge slice

### Takeaway
Keep a "representative" slice (random within strata, which drives the headline metrics and gates) and a labelled "challenge" slice (curated hard, ambiguous, adversarial or rare cases), and report them separately. Gate on the challenge slice only for regressions on specific known failure modes. Never pool it into the headline numbers, because curated hard cases inflate error rates by an amount that depends on how many were added.

### Cited Findings
- **Contrast sets:** small, expert-made perturbations near the decision boundary expose failures that i.i.d. test sets hide. Models scored much lower on contrast sets than on the original test sets. They are presented as a complement to the standard test set, not a replacement. — [Gardner et al. 2020, Findings of EMNLP](https://arxiv.org/abs/2004.02709)
- **CheckList:** behavioural test suites (minimum functionality, invariance, directional tests) report failure rates per capability, separately from held-out accuracy. — [Ribeiro et al. 2020, ACL](https://arxiv.org/abs/2005.04118)
- **Hidden stratification:** aggregate metrics can hide poor performance on clinically important subclasses. Measure and report the important subsets explicitly. — [Oakden-Rayner et al. 2020, ACM CHIL](https://arxiv.org/abs/1909.12475)
- Recht et al. show that a "slightly harder" distribution can lower accuracy by many points while leaving model rankings largely unchanged. Mixing harder items into a headline set therefore changes the level, not necessarily the ranking. — [Recht et al. 2019](https://arxiv.org/abs/1902.10811)

### Inferences
- For this domain, plausible challenge strata are:
  - SOV spreadsheets embedded in an email body
  - loss runs with an ACORD-like layout
  - scanned or OCR-noisy ACORD forms
  - multi-document PDFs
  - broker emails that quote loss figures
  - non-English documents
  - near-empty attachments
- Tag every challenge item with its stratum. Report each stratum's pass rate with a Wilson CI. With 20 to 30 items per stratum, intervals are about ±0.15 to ±0.2, so use these slices for "did this specific case regress" checks, for example a McNemar test on the slice, not for precise rates.
- Template-group exclusion (invariant 3) applies equally to the challenge slice. Hard cases are often template families, and a family partly in training leaks easily.

### Gaps
- No primary source found gives a recommended ratio of challenge items to representative items.
