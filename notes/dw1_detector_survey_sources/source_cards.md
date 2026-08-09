# DW1 detector survey source cards

## Reading rule

`S` marks a sourced fact from a primary paper, official implementation, or public
official artifact. `M` marks a direct local measurement. `E` marks arithmetic or
hardware estimation. `I` marks an inference. Quotes are short searchable anchors;
the adjacent locator holds the full context. Paper-reported results are not treated
as independent replications.

Bracketed `E1` through `E19` references are document identifiers for the embedded-
result cards in `coverage_composite_dispositions.md`; they are not evidence-label
prefixes. Each such card distinguishes sourced claims from M8 measurements.

The primary PDFs and official snapshots are retained at the discoverable path
documented in `paper_artifacts.md`, with a complete SHA-256 ledger. Repository
commits and search routes are in `search_log.md`.

## 2026-08-08 accuracy-first follow-up

### N1 — LAPD

- Official sources: [arXiv 2604.16923](https://arxiv.org/abs/2604.16923) and
  [repository at inspected commit](https://github.com/creator-xi/LAPD/tree/1988eb68b70205d471c1924b6bbf1e199452662d).
- Preserved evidence: primary PDF, Table 13 and Appendix C.1; repository
  `method/core/compute.py`, `method/core/agg_strategy.py`,
  `method/lapd_multi_gpu.py`, and `method/scripts/time_efficiency.sh`.
- Sourced method: Log-likelihood Alignment Preference Discrepancy compares a base
  and aligned model, information-weights token discrepancies, and standardizes
  them with 10,000 independent categorical samples per token. The implementation
  samples from already-computed logits; it does not decode those samples or run
  another model forward. The paper nevertheless marks LAPD as a method that
  standardizes by “perturbing or generating auxiliary sequences.”
- Sourced accuracy: Table 13 uses the same Llama-2-7B base/instruct pair for every
  method. Binoculars/LAPD AUROC percentages are M4 87.27/88.02, DetectRL
  multi-LLM 93.11/97.17, DetectRL multi-domain 88.33/96.11, RAID 85.30/85.21,
  RealDet 94.56/95.32, and average 89.72/92.37.
- Sourced efficiency: Appendix C.1 caps input at 1,024 tokens and states two RTX
  3090 24 GB GPUs. Table 7 measures 300 texts, batch 1: LAPD 0.5792 seconds and
  Binoculars 0.6549.
- Exact anchor quote: “All methods use the Llama2-7B base/instruct pair”.
- Artifact boundary: code and datasets are public, but no license file or license
  declaration was found. The exact Llama artifacts require license acceptance.
  The cached release path reuses base logits when the sampling model equals the
  base, but the separate multi-GPU runner redundantly forwards that model again.
- Interpretation: the matched table is strong comparative evidence on those
  benchmarks, not evidence for DW1 or dynamic-quantized Falcon accuracy. The
  0.09-point RAID loss prevents a claim of universal dominance. Under the strict
  no-multi-perturbation constraint, the 10,000 auxiliary samples exclude LAPD
  unless the human explicitly permits them.

### N2 — IRM

- Official sources: [NeurIPS 2025 proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f50258b34f1c5080e43281e05050034e-Abstract-Conference.html),
  [official supplemental archive](https://proceedings.neurips.cc/paper_files/paper/2025/file/f50258b34f1c5080e43281e05050034e-Supplemental-Conference.zip),
  and [arXiv 2604.21223](https://arxiv.org/abs/2604.21223).
- Preserved evidence: primary paper Tables 1 and 5, implementation details, and
  the official supplemental archive, SHA-256
  `831062de6a10566594c072f43ea8b770dfdf73d1b1193dc32c3a4c76fb56c8fa`.
- Sourced method: the implicit reward score is the sequence log-likelihood under
  an instruction-tuned model minus the sequence log-likelihood under its base
  counterpart. The released command binds the instruction checkpoint to the
  implementation's misleading `base_model` variable. The implementation performs
  one forward per model.
- Sourced matched comparison: with the Llama-3.2-1B family, IRM/Binoculars AUROC
  percentages are 97.97/92.48 multi-domain, 97.24/92.08 multi-LLM,
  97.19/93.04 multi-attack, and 94.48/94.63 human writing. The reported 91.77
  aggregate mixes AUROC and F1 columns; it is not an aggregate AUROC.
- Sourced public-pair result: Qwen2-0.5B IRM gives 90.14, 89.43, and 90.47 AUROC
  on the same three task families; its mixed aggregate is 82.79.
- Sourced hardware: all experiments use two RTX 4090 24 GB GPUs.
- Exact anchor quote: “All experiments are conducted on two NVIDIA RTX 4090 GPUs”.
- Artifact boundary: code is complete, but the best Llama pair is gated behind
  license acceptance. The Qwen pair is anonymously downloadable.

### N3 — SV-Detect

- Official sources: [arXiv 2606.07313](https://arxiv.org/abs/2606.07313) and
  [repository at inspected commit](https://github.com/Atmyre/SV-Detect/tree/a25469ba6a1fa2adcf644338db6fef712511da66).
- Preserved evidence: primary paper Sections 3–4, Tables 1, 7, and 8, Appendix
  efficiency table; official repository training/evaluation source and data
  manifest.
- Sourced method: one frozen GPT-Neo-2.7B forward returns all hidden layers;
  mean-pooled representations are compared with learned steering directions and
  fed to logistic regression. Experiments use a 2,048-token maximum; the
  efficiency experiment separately caps at 512.
- Sourced accuracy boundary: in the in-domain DetectRL settings, reported
  SV-Detect AUROCs span 99.83–100. Training and test partitions come from the
  corresponding domain, source-model, or attack-family setting, and the attack
  setup uses 10,192 examples per class. Cross-source generalization is reported
  separately, without a matching Binoculars row.
- Sourced efficiency: one A100 40 GB, float16, 512 tokens; 25.71 milliseconds at
  batch 1, 74.3 texts per second at batch 16, 8,951 MB peak.
- Exact anchor quote: “only a single forward pass through the backbone”.
- Artifact boundary: repository code and data downloader are present, but no
  trained steering direction, logistic-regression state, release, checkpoint, or
  declared license was found.

### N4 — EchoPrompt

- Official source: [arXiv 2608.05741](https://arxiv.org/abs/2608.05741), submitted
  6 August 2026.
- Preserved evidence: primary manuscript, Tables 1–2, Figure 7, implementation
  details, and limitations.
- Sourced method: a fixed assistant-style prefix conditions base and aligned
  proxy likelihoods; no target text is rewritten and no auxiliary passage is
  decoded.
- Sourced result: with a Llama-3-8B proxy across DetectRL, RealDet, and RAID,
  EchoPrompt averages 95.56 AUROC and 91.98 F1 versus Binoculars at 90.07 and
  84.62. With Falcon, EchoPrompt/Binoculars average AUROC is 86.91/85.73, while
  F1 is 81.72/82.13.
- Sourced runtime boundary: Figure 7 plots 0.254 seconds per EchoPrompt text and
  0.157 for Binoculars. Experiments state a V100 32 GB and 1,024-token maximum,
  but the figure does not fully identify proxy, batch, or timing boundary.
- Exact anchor quote: “depends on the choice of proxy family”.
- Artifact boundary: no official repository or checkpoint was found in exact-title
  GitHub search on 8 August 2026. Results are manuscript claims, not a runnable
  reproduction.

### N5 — Steer-to-Detect

- Official source: [arXiv 2605.12890](https://arxiv.org/abs/2605.12890).
- Preserved evidence: primary manuscript, Table 8 and Appendix F.4.
- Sourced method: a frozen observer model is steered using a learned vector and
  scored in one forward. The efficiency comparison trains each trainable method
  on 512 mixed text pairs and uses Llama-3.1-8B as observer.
- Sourced same-run comparison: on one A100 80 GB, batch 1, the mixed test has
  average length about 267 tokens and 95 percent below 435. Steer-to-Detect reports
  98.90 AUROC, 97.75 TPR at 1 percent false-positive rate, 0.30 seconds, and
  39 GB peak. Binoculars reports 87.70, 74.70, 0.50 seconds, and 58 GB.
- Exact anchor quote: “All efficiency profiling is conducted on a single NVIDIA A100”.
- Artifact boundary: no official code, checkpoint, or detector state was found by
  exact-title GitHub search on 8 August 2026. A short-text batch-1 39 GB result
  does not prove batch-8, 2,048-token A6000 fit.

### N6 — RepreGuard

- Official sources: [arXiv 2508.13152](https://arxiv.org/abs/2508.13152) and
  [repository at inspected commit](https://github.com/NLP2CT/RepreGuard/tree/53677be4efc4a494d083b76f91dccc50d8bb4400).
- Preserved evidence: TACL 2025 manuscript Table 5; official training and
  evaluation source.
- Sourced result: one A100 80 GB, float32, batch 1; a 1,000-pair test across four
  generators after training on 512 Claude-Instant pairs. Phi-2 RepreGuard gives
  96.10 AUROC, 54.50 TPR at 0.01 percent false-positive rate, 16 GB, and 0.072
  seconds. Llama-3.1-8B gives 94.80, 77.10, 38 GB, and 0.359 seconds. Binoculars
  gives 81.90, 72.60, 58 GB, and 0.653 seconds.
- Exact anchor quote: “trained on the Claude-Instant dataset with 512”.
- Mismatch: inputs are capped at 256 tokens and generators are older than the
  current DW1 target. The repository ships code but no trained directions or
  checkpoint, has no declared license, and its dataset download identifier is
  malformed in the inspected README.

### N7 — Uncertainty and Uncertainty++

- Official sources: [arXiv 2606.02158](https://arxiv.org/abs/2606.02158) and
  [MIT-licensed repository at inspected commit](https://github.com/guoyikai2000/Uncertainty-AIGT/tree/2e06a3d91ed1121c25b3fd7e6380238e04517086).
- Preserved evidence: ICML 2026 manuscript main results and efficiency section;
  official source.
- Sourced result: with GPT-J on XSum, WritingPrompts, and Reddit, average AUROC is
  88.74 for Uncertainty and 93.24 for Uncertainty++, versus 85.64 FastDetectGPT
  and 91.51 Lastde++. A newer-generator table averages 94.79 for Uncertainty++.
- Sourced efficiency: on one A100 80 GB with GPT-J, throughput is 27.27 samples
  per second for Uncertainty and 18.75 for Uncertainty++, with 12.68 GB peak for
  the latter. Sequence length and batch are not sufficiently reported for a DW1
  comparison.
- Evidence gap: no like-for-like Binoculars result exists, so neither the strong
  AUROC nor the speed number establishes Binoculars parity.

### N8 — Newer methods rejected or excluded

- Primary manuscripts preserved: [DeBERTa-Sentinel](https://arxiv.org/abs/2608.01046),
  [DWT-Fusion](https://arxiv.org/abs/2607.22026),
  [GTCL](https://arxiv.org/abs/2607.14967),
  [strong RoBERTa baseline and distribution shift](https://arxiv.org/abs/2607.03680),
  [Triospect](https://arxiv.org/abs/2606.31074),
  [Multi-Level Contextual Detection](https://arxiv.org/abs/2605.16107),
  [Hidden Human-Like Nature](https://arxiv.org/abs/2605.23190),
  [GPTZero](https://arxiv.org/abs/2602.13042),
  [late-stage stability](https://arxiv.org/abs/2601.04833),
  [DEER](https://arxiv.org/abs/2511.01192),
  [PhantomHunter](https://arxiv.org/abs/2506.15683), and
  [DivScore](https://arxiv.org/abs/2506.06705).
- Artifact snapshots: DeBERTa-Sentinel commit
  `cd8b1a46cc98eb353ef2eb6e70bfc751f6eece16`; GTCL commit
  `c9094d66bd0f6a888d3490ac04b3b3c68d2d2b64`; Triospect commit
  `7599d456a667e3db0261ffe35da1c1bc37b641a9`; Multi-Level commit
  `c108289ea8595da780471ed1ce034773a571b364`.
- Accuracy rejection: DeBERTa-Sentinel's 99.53 ROC-AUC comes from one GLC random
  split and has no released checkpoint or credible cross-distribution comparator.
  DWT-Fusion's reported M4/MAGE results are below the leading candidates and it
  has no official detector release. Multi-Level exposes supplementary material,
  not runnable code. GPTZero is not an open detector artifact.
- Deployment rejection: PhantomHunter has several probability extractors, no
  released detector state, and insufficient speed evidence. DivScore targets
  specialized legal/medical domains through domain knowledge distillation, not a
  general DW1 drop-in. Late-stage stability lacks a like-for-like Binoculars row.
- Method exclusion: official GTCL inference uses k-nearest-neighbor classification
  over retained representations. Triospect generates summaries and simplified
  versions and aggregates multiple views. They violate retrieval or
  rewrite/regeneration constraints before ranking.

### N9 — MELD paper and two incompatible official artifact eras

- Official sources: [arXiv 2605.06903](https://arxiv.org/abs/2605.06903), the
  [paper-era Hugging Face revision](https://huggingface.co/anon-review-meld-2026/meld/tree/51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808),
  and the [current v5 revision](https://huggingface.co/anon-review-meld-2026/meld/tree/453acf594d48f8c55c3a38bde396f9178516d817).
- Preserved evidence: primary PDF; both complete immutable, anonymously
  downloadable, MIT-licensed Hugging Face snapshots; the official commit history;
  and the paper-era companion endpoint's anonymous HTTP 401 response. Exact files
  and hashes are in `paper_artifacts.md` and the external collection ledger.
- Sourced RAID comparison: the paper's public-leaderboard Table 1 gives MELD
  AUROC/TPR-at-5-percent-FPR/TPR-at-1-percent-FPR of 99.82/99.78/99.24 over all
  attacks and 99.85/99.76/99.40 on clean text. The clean Binoculars row is
  84.40/78.98/69.54. MELD's training mixture includes 1.85 million RAID rows,
  so this is a same-test comparison, not an equal-training-regime comparison.
- Sourced held-out comparison: Table 3 reports MELD AUROC of 99.7, 99.1, 78.0,
  100.0, 98.5, and 99.99 on HC3, MAGE, M4GT, Ghostbuster, DetectRL, and
  MELD-eval. The same rows are 79.4/60.7/57.3/75.4/64.8/45.2 for Binoculars and
  99.1/57.1/65.9/92.6/73.0/70.5 for Fast-DetectGPT. These are paper
  re-evaluations, not this study's measurements.
- Sourced low-FPR comparison: Table 4 gives overall MELD-eval TPR at one-percent
  FPR of 99.9, versus 95.5 for ModernBERT-Detect, 17.0 for Fast-DetectGPT, and
  0.6 for Binoculars. All are zero-shot with respect to four selected generators,
  but the pool reuses RAID-style English domains, human seeds, and attacks; each
  detector receives a pool-specific threshold. The paper explicitly denies that
  this demonstrates a single transferable deployment threshold.
- Paper architecture and cost boundary: the manuscript describes a 396-million-
  parameter Ettin encoder, one MLP main head, and discarded auxiliary heads;
  2,048-token training and overlapping 2,048-token evaluation chunks; and
  training on three H200 GPUs. It supplies no inference latency, batch-8 A6000
  memory, or end-to-end comparison with DW1 Binoculars.
- Paper-era artifact: revision
  `51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808` ships a 1,584,091,048-byte FP32
  weight file and describes 396 million parameters. Its model card requires the
  linked companion code. That endpoint returned HTTP 401 with
  `{"error":"not_connected"}` anonymously on 2026-08-08. Guessing the missing
  implementation would not be a faithful reproduction.
- Reconciliation gap: the paper says 6.60 million training rows and 1.85 million
  RAID rows, while the paper-era model card says 6.82 million and 1.91 million.
  The manuscript calls the main head an MLP; the current v5 state instead uses a
  token-style projection, human anchors, family prototypes, and top-fraction
  aggregation. The artifact history therefore reflects materially different
  states, not documentation drift that can safely be merged.
- Current artifact: v5 release commit
  `9b6379cdf62961a443d972fd27ff705ea9a07dd3` says it “replaces all earlier
  checkpoints”; subsequent commits culminate in immutable revision
  `453acf594d48f8c55c3a38bde396f9178516d817`. Its card says earlier revisions
  held different models and “scores are not comparable across them.” It is a
  self-contained 394,833,461-parameter FP32 detector that reads the first 2,048
  tokens and warns against inputs under 100 words. The shipped raw-score
  thresholds are 1.915662 at nominal one-percent FPR and -0.468027 at nominal
  five-percent FPR.
- Decision: the paper establishes that MELD is the most important recent
  scientific lead, and the current artifact is runnable, but v5 measurements
  cannot validate paper-era accuracy. Until the paper/checkpoint mapping and a
  frozen like-for-like accuracy evaluation are resolved, MELD is an explicit
  blocker rather than a recommendation.

### N10 — ICLR 2026 Markov-informed calibration

- Official sources: [ICLR 2026 paper, arXiv 2602.08031](https://arxiv.org/abs/2602.08031)
  and [official repository at commit](https://github.com/tmlr-group/MRF_Calibration/tree/a21add14e162943907c1af01ddbd299db8b7faf8).
- Sourced method: a supervised two-by-two Markov random-field layer calibrates
  token-level detector scores. The paper trains its weights on labeled text from
  a named generator and dataset, then tests other generators. It is a plug-in,
  not a new standalone detector.
- Sourced Binoculars rows: average AUROC changes from 94.85 to 94.91 on Essay,
  86.99 to 91.41 on Reuters, and 73.17 to 75.49 on DetectRL. These within-paper
  gains do not make Binoculars uniformly competitive with the strongest current
  detector rows.
- Artifact and cost boundary: the public source trains and saves a state per
  dataset; no trained state is shipped. The paper calls the sparse calibration
  overhead negligible, but does not give a 2,048-token two-A6000 whole-detector
  comparison with DW1 Binoculars. Its experiments use GPT-2-family proxies and
  1,024-token inputs.
- Decision: retained as a released calibration method, not a qualifying detector.
  A new supervised calibration state and a same-run base-detector benchmark would
  be required.

### N11 — Exons-Detect

- Official sources: [arXiv 2603.24981](https://arxiv.org/abs/2603.24981) and
  [official repository at commit](https://github.com/Xiaoweizhu57/Exons-Detect/tree/239862c0a9bb580b7cf883b5efdfab1570bb0e8f).
- Sourced matched comparison: Table 1 reports Exons-Detect AUROC of
  92.43/90.67/90.46/94.98 on M4, DetectRL multi-LLM, DetectRL multi-domain, and
  RealDet, averaging 92.14. Same-table Binoculars is
  90.00/83.21/77.45/93.64, averaging 86.08; Fast-DetectGPT averages 85.07.
- Method exclusion: the final score incorporates an “ideal AI sequence” built by
  choosing maximum-probability tokens under the proxy. The paper calls this the
  mutation-repair mechanism. Removing that term drops average AUROC from 92.14
  to 87.76. Constructing and scoring a generated replacement sequence is an
  essential regeneration stage, so the method is excluded before ranking.
- Artifact and cost boundary: the paper caps inputs at 1,024 tokens, uses one
  A100 80 GB in FP32, and reports sub-0.8-second latency around 300 tokens. The
  public repository is a cleaned scoring-math release; its README says its tests
  do not perform end-to-end model downloads, and it ships neither the paper's
  mutation-repair construction nor detector states or thresholds. It cannot
  reproduce the paper accuracy anonymously as released.
- Decision: high like-for-like paper accuracy is retained, but the method is
  excluded as regeneration and is not an A6000 accuracy or speed candidate.

### N12 — DACTYL/Vanguard released watchlist

- Official sources: [PAN 2026 notebook, arXiv 2607.17382](https://arxiv.org/abs/2607.17382),
  [Vanguard ModernBERT-large artifact](https://huggingface.co/ShantanuT01/vanguard-ai-text-detector/tree/82306100e5a8f1d31e495579d740ac7ff6f62336),
  and [Gradient DeBERTa artifact](https://huggingface.co/ShantanuT01/gradient-ai-text-detector/tree/c2e282cedc8d4ef8dd30d1cc1098d297b26ce258).
- Sourced accuracy: the paper's MCGrad-calibrated ModernBERT ranks second on PAN
  2026 with AUROC 0.993 and a 0.974 mean over five unlike metrics. Its released
  ModernBERT model card reports 0.9475 mean AUROC and 0.8493 macro F1 across its
  listed out-of-distribution sets. The composite 0.974 is not classification
  accuracy and cannot be compared numerically with DW1 AUROC.
- Artifact and deployment boundary: both official checkpoints are public and
  MIT-licensed; the ModernBERT weight is about 1.58 GB. Neither the paper nor
  card supplies a same-row Binoculars or FastDetectGPT comparison, low-FPR
  transfer result, 2,048-token batch-8 memory, or A6000 timing.
- Decision: retained as a genuinely released 2026 supervised watchlist item. It
  needs a frozen DW1 accuracy and operating-point run before feasibility testing
  can support promotion.

### N13 — LM²otifs

- Official source: [arXiv 2505.12507v2](https://arxiv.org/abs/2505.12507v2),
  updated 30 July 2026. The exact primary PDF is retained with SHA-256
  `b0a2bcc7f56ba0959563b7536f0bc9b6ee3e982865cfd91848805b60c2dfeb06`.
- Sourced mechanism: LM²otifs builds lexical token-co-occurrence and document
  graphs, inserts test-document nodes, and classifies them with a three-layer
  graph convolutional network. For out-of-vocabulary input it selects the
  “nearest semantic neighbor from the training set.” That inference-time lookup
  independently crosses the strict no-nearest-neighbor boundary.
- Sourced data and training: six datasets cover open question answering,
  medicine, finance, Reddit, arXiv, reviews, recipes, books, poetry, Yelp,
  essays, and creative writing. Generator rows include ChatGPT, DaVinci, Cohere,
  Dolly, BloomZ, Llama 2, GPT-4, MPT, Mistral, Claude 3, and Gemini 1.0 Pro.
  Individual graph experiments use up to 2,000 training, 200 validation, and 200
  test texts; the GCN trains for 5,000 epochs. The paper reports no document
  length distribution or 2,048-token batch basis.
- Sourced in-domain comparison: Table 1 reports average accuracy/AUC of
  0.98/1.00 for LM²otifs and 0.97/0.99 for same-table Binoculars over HC3, M4,
  and RAID ChatGPT rows. Table 2 reports average accuracy 0.95 versus 0.83 over
  eleven generator settings. These are supervised in-domain comparisons, not an
  equal-training regime, fixed low-FPR test, or transferable calibration.
- Sourced cross-domain control: Table 9 reports average accuracy 0.79 for
  LM²otifs versus 0.95 for Binoculars and 0.97 for FastDetectGPT. The paper says
  its “cross-domain generalization is constrained.” It reports no TPR at a fixed
  FPR, threshold-selection procedure, or independent calibration result.
- Sourced timing and hardware: Table 19 gives 0.0051–0.0091 seconds on four HC3
  domains and says the experiment was repeated ten times. It supplies no batch,
  input-length, per-document versus whole-set boundary, or Binoculars timing row.
  All experiments used “8 NVIDIA A100 GPUs,” each with 40 GB. Training graphs
  contain up to 8.6 million edges, but no peak memory or detector-state size is
  reported. The timing cannot establish near-Binoculars speed, and total A100
  capacity cannot establish a two-A6000 fit.
- Artifact boundary: the paper links no detector repository or checkpoint.
  Anonymous GitHub repository searches by method name, exact title, and arXiv
  identifier returned no match; anonymous Hugging Face model and Space searches
  by method name returned none. Raw responses are in the external collection.
  This is bounded negative evidence, not a universal absence claim.
- Reproducibility decision: no code, trained graph, vocabulary, GCN state, or
  threshold is public. A local A6000 reconstruction would test an invented
  implementation and cannot validate the tables or timing, so no screen was run.
  LM²otifs is excluded by its nearest-neighbor fallback and independently
  rejected for artifact, cross-domain, calibration, fit, and timing gaps despite
  the paper's “state-of-the-art performance” claim.

### N14 — NEULIF

- Official source: [arXiv 2511.21744v2](https://arxiv.org/abs/2511.21744v2),
  updated 8 January 2026. The exact primary PDF is retained with SHA-256
  `774057540585a0ce338a3456bc644b621949a8ee1f8af95d659c713a47208ab0`.
- Sourced mechanism: spaCy and TextDescriptives extract 68 stylometric,
  readability, syntactic, lexical, and cohesion features. A fitted scaler feeds
  either a one-dimensional CNN or a 100-tree random forest; the paper uses a
  nominal 0.5 CNN decision threshold. This is a single feature/classifier path,
  not retrieval, rewriting, regeneration, or multi-perturbation inference.
- Sourced data boundary: the authors randomly sample 20,000 balanced essays from
  a roughly 500,000-row Kaggle “AI Vs Human Text” corpus, drop missing features,
  and report 15,981 train, 1,993 validation, and 1,997 test rows. The paper does
  not identify the contributing generators, source domains, length distribution,
  or duplicate-control boundary. The matching public Kaggle listing says only
  that roughly 500,000 essays were combined from multiple sources; its anonymous
  metadata is retained. The exact dataset identity therefore remains an
  inference rather than paper-specified provenance.
- Sourced metrics: the CNN reports 97 percent accuracy, about 0.95–0.97 F1, and
  0.9951 ROC-AUC on that one random in-domain split; the random forest reports
  roughly 95 percent accuracy, 0.94 F1, and 0.9555 ROC-AUC. The paper explicitly
  says its “results are reported in-domain only.” Its cross-paper comparison
  mixes other datasets and metrics and contains no matched Binoculars row.
- Calibration and operating point: no held-out probability-calibration method,
  calibration curve, Brier score, or TPR at a fixed FPR is reported. The CNN
  confusion matrix has 28 false positives among 997 human test rows, an inferred
  2.81 percent FPR at the stated nominal threshold, not a one-percent operating
  point. Low log loss alone does not prove transferable calibration.
- Size and timing: the architecture table reports 2,205,185 trainable CNN
  parameters while an earlier prose claim says fewer than 10^5, an internal
  inconsistency. The serialized CNN and random forest are reported as about 25
  MB and 10.6 MB. The paper claims “typical inference times under 100
  milliseconds” for the complete CPU path but gives no CPU model, text length,
  batch, repetitions, distribution, raw timing, or matched Binoculars boundary.
  The claim is plausibly lightweight but does not demonstrate near-Binoculars
  speed under the fixed screen.
- Artifact boundary: the paper links no repository, model, scaler, feature
  schema, or checkpoint. Exact-name/title/identifier GitHub and method-name
  Hugging Face model/Space searches found no relevant release. The Kaggle corpus
  metadata is public, but data alone cannot reproduce the detector.
- Reproducibility decision: the tiny reported serialized sizes make two-A6000
  memory capacity plausible, yet the intended path is CPU-based and the trained
  classifier, scaler, precise features, split indices, and timing protocol are
  absent. Training a replacement would not reproduce the reported state, so no
  A6000 screen was scientifically meaningful. NEULIF is retained as an
  in-domain lightweight claim and rejected for provenance, generalization,
  artifact, low-FPR, and timing comparability gaps.

### N15 — High-claim rows promoted by semantic adversarial review

These seven rows are individual detector dispositions, not a shared-task
catch-all. Their primary PDFs and every paper-linked public repository are
preserved in the external collection.

- [Comparative neural detectors, 2603.18750](https://arxiv.org/abs/2603.18750):
  four supervised architectures are evaluated on 60-text tests. The strongest
  proposed model reaches 91.67 percent accuracy on the balanced English dtEN
  test and 98.3 percent on the thematic Italian ART&MH test; the Italian dtITA
  rows are single-class and cannot establish balanced discrimination. No
  Binoculars, fixed-FPR, hardware, or inference-time result is reported. The
  official repository at commit
  `a18a95ecb70e799b7b0ea02e9e43b1ae9929bddf` contains notebooks and data but no
  trained checkpoint. PDF SHA-256:
  `42106d2af0da94784fef3855471f0e5106e90c2beb0a2552295c4abece29d27f`;
  source-archive SHA-256:
  `c18030e7946007525740cc9ccdcf9c28f473f769b7193381cc7fe5225ee7ae2f`.
- [Multi-Strategy/M-DAIGT, 2509.00623](https://arxiv.org/abs/2509.00623):
  fine-tuned RoBERTa reports 99.99 percent accuracy/F1 on news and 100 percent
  on academic-abstract test sets after equally near-perfect development rows.
  The paper provides no generator-shift, cross-domain, calibration, fixed-FPR,
  hardware, or measured-latency result and links no trained state or source
  repository. Its 512-token method therefore cannot be assigned the shared-task
  scores outside that closed task split. PDF SHA-256:
  `6f564ed548359c3e73e97481dbfb9895fcd2b15c94839b8cf740d38956ea910c`.
- [Instruction fine-tuned detectors, 2507.05157](https://arxiv.org/abs/2507.05157):
  the Defactify Task-A test result is F1 0.9547. It comes from a fine-tuned,
  hosted GPT-4o-mini state; about 200 test calls were filtered, and the final
  submission combines that closed result with a BERT Task-B result. The paper
  links no detector release and supplies no low-FPR, matched comparator, or
  inference-time row. PDF SHA-256:
  `c5a4409f82ec509c78fd5df0243de5214d7fe6d4eef9200d0ab84b7dd0e9869e`.
- [mdok, 2506.01702](https://arxiv.org/abs/2506.01702): in-distribution
  validation AUROC is 0.9972 and the paper claims first rank, but the official
  binary test leaderboard reports AUROC 0.853 and F1 0.898. Its separate MIX2k
  validation AUROC is 0.6995 versus 0.6368 for same-table Binoculars. The
  detector uses a 14-billion-parameter Qwen model; the paper gives no inference
  timing or memory. The official repository at commit
  `3d87f716e895ac13df9c96c6c645f6b26c7eca3f` contains two training scripts and
  no checkpoint. PDF SHA-256:
  `c362ab8854b93bdeceeae9a6753b07c33ebf7041d03e3ecb08abc941c4a461e7`;
  source-archive SHA-256:
  `8ad6d7b5adbb15381f2c6a6a6fafc0b07fd0b49df8630ada98b5688d915e9b7b`.
- [Multifaceted Defactify detector, 2505.11550](https://arxiv.org/abs/2505.11550):
  the fifth-place Task-A system reports F1 0.994 on one shared-task test. It
  combines a RoBERTa detector, E5 embeddings, stylometric features, and a dense
  classifier. No public trained state, cross-distribution evaluation,
  fixed-FPR result, hardware, or latency is supplied. PDF SHA-256:
  `5ffd86b33dffeecef2cd3511ec33b219b810edf0b3713304ee94f347a0f03a02`.
- [SKDU/Defactify, 2503.22338](https://arxiv.org/abs/2503.22338): the permitted
  NELA-feature/XGBoost branch—not the lower-scoring seven-rewrite RAIDAR
  branch—reports Task-A test F1 0.9945. The official repository at commit
  `8ac8229b45fb826d309119927ead7e65924f7c64` contains two NELA feature scripts
  but no fitted classifier or frozen feature state. No cross-distribution,
  Binoculars, fixed-FPR, hardware, or timing result is reported. PDF SHA-256:
  `5d5c29599d4039d36bffca8a7f597adaf0e884dbe4b6c663ed74e6aaa214b986`;
  source-archive SHA-256:
  `29da14ce1cb119ccc4981a66370b63a51624387c05ed0e86869df60c48050303`.
- [Sarang/Defactify, 2502.16857](https://arxiv.org/abs/2502.16857): a
  DeBERTa-v3-small ensemble trained with input noise reports first-place Task-A
  F1 1.0 on one shared-task test, at a maximum length of 768. Training-time
  noising does not itself violate the inference method gate, but no public
  trained state, cross-distribution result, fixed-FPR calibration, hardware, or
  inference timing is supplied. PDF SHA-256:
  `2d4e556e73bc2397084180faa5822e7bc418f838be14488a445a1add565c2347`.

None received an A6000 screen: the three public repositories omit trained state,
the other four papers expose none, and rebuilding supervised systems would test
new states rather than the reported result. The missing fixed-state and timing
boundaries also prevent a near-Binoculars speed claim. All seven are retained as
high claims and individually rejected, leaving the recommendation unchanged.

### N16 — Linguistic-feature SVM, arXiv 2606.04177

- Official sources: [primary paper](https://arxiv.org/abs/2606.04177), PDF
  SHA-256 `454f87ecc87ad9c329018dd64c9a1b66bd35c9e13a8656ce9f833c17563e523a`,
  and the paper-linked [ELFEN feature repository](https://github.com/mmmaurer/elfen/tree/f404576157e15b403d893e7a1fadd7539c7caea3).
- Sourced mechanism and data: a class-weighted linear SVM consumes 284
  interpretable linguistic features over MAGE data from 27 generators in seven
  model families, ten original text domains, and four held-out GPT-4 domains.
  This is one parent detector rather than a benchmark inventory of independent
  proposed systems.
- Sourced metrics: Table 2 reports SVM AUROC of 0.987 for separate in-domain
  text/model-pair classifiers, 0.968 for one mixed in-domain classifier, 0.907
  on new text domains and GPT-4, and 0.945 for held-out text/model-domain pairs.
  The accompanying macro F1 values are 0.788, 0.827, 0.808, and 0.588. High
  threshold-free discrimination therefore coexists with unstable classification
  quality under the hardest shift.
- Artifact and deployment boundary: ELFEN is public feature-extraction source,
  but no fitted SVM, exact frozen feature state, calibration artifact, fixed-FPR
  result, document-length/timing protocol, or trained detector checkpoint is
  released. A local retraining would create a new state, so no A6000 screen was
  scientifically meaningful.
- Decision: individually retain/reject. The cross-domain rows merit preservation,
  but they do not establish a reproducible general detector, transferable
  low-FPR threshold, or near-Binoculars deployment result.

### N17 — Generalized composite-source semantic repair

- Durable source maps:
  [composite-source ledger](coverage_composite_sources.tsv),
  [result-level ledger](coverage_embedded_results.tsv),
  [independent exact-result inventory](coverage_expected_result_ids.tsv),
  [generated result audit](coverage_embedded_result_audit.tsv), and
  [embedded source cards](coverage_composite_dispositions.md).
- Sourced accounting: all 119 frozen export publications retain exactly one row
  disposition. In addition, 33 overview, benchmark, comparative, evaluation, or
  shared-task sources receive a second-level semantic inspection. Twenty-six
  sources expand to 241 qualifying named system/version results; the other seven
  record the inspected scope and a source-specific no-qualifier reason.
- Exact-ID control: an independently maintained 241-row inventory is bound by a
  checker-constant SHA-256 and must exactly match the actual child-ID set for
  every expanded source. The checker separately hard-codes the 20 Task 3 and
  eight Counter Turing identities as anchors. Missing a parent review, child,
  primary-source/absence field, artifact status, or explicit disposition is a
  hard failure, as is binding a child to the wrong E-card. The checker also
  parses and hash-binds the parent and exact result IDs from every real Markdown
  E-card marker.
- Accepted composite control: composite selection uses allowlisted source classes and
  publication-title semantics rather than a manually chosen identifier count.
  The audit validates exact child identities, counts, parents, and cards.
  Regression tests prove that the predecessor Task 3 omission, a missing CNLP
  row, deletion of the non-anchor mDeBERTa row plus a lowered declared count, a
  nonexistent source-card label, removal or parent/result misbinding of a parsed
  Markdown E-card, a synthetic count mismatch, reclassification of a known
  high-cell parent as no-qualifier, and a generic no-qualifier reason fail.
  Complete source-specific negative controls pass.
- Frozen result: 204 raw export rows deduplicate to 119 publications; 106 have
  title/abstract performance triggers, 70 have explicit parent dispositions, 49
  have mechanically allowlisted non-candidate classes, 33 require composite
  review, and 241 child results are individually dispositioned. All eleven
  regression/negative controls pass.
- Interpretation: a publication-row mapping is necessary but no longer
  sufficient. The child ledger prevents plausible high-score systems from being
  hidden within the selected “benchmark,” “overview,” “shared task,” and
  analogous composite classes. N18 removes that layer's remaining selection
  boundary across the complete corpus.

### N18 — Full-corpus, content-derived account repair

- Durable source maps:
  [119-paper source inventory](coverage_fulltext_sources.tsv),
  [805-account expectation inventory](coverage_fulltext_expected_accounts.tsv),
  [exact disposition map](coverage_fulltext_account_map.tsv),
  [564 primary-result dispositions](coverage_primary_results.tsv),
  [generated account audit](coverage_fulltext_account_audit.tsv), and
  [inventory generator](build_fulltext_inventory.py).
- Sourced accounting: every primary PDF and every main/appendix result table for
  all 119 frozen export publications was read. A separately named submitted,
  proposed, or fitted detector system, version, ensemble, training state, or
  configuration is an account when it carries a threshold metric at or above
  0.90 on any reported slice or an explicit high/best claim. Dataset and
  operating-point repetitions stay on one account; component-only hyperparameter
  sweeps do not become deployment accounts.
- Exact result: 805 accounts resolve one-to-one: all 241 accepted embedded
  results and 564 explicit primary-paper configurations. No parent-only account
  remains. Six papers have source-specific, table-derived full-text no-qualifier
  reasons. Each of the 119 source rows binds the preserved primary
  PDF hash and the hash of its exact `pdftotext -layout -enc UTF-8` extraction.
- Ordinary-title controls: arXiv 2509.00623 now has separate RoBERTa-base,
  TF-IDF plus linear support-vector machine, and Candace rows; 2503.22338 has all
  nine support-vector, random-forest, and XGBoost combinations over RAIDAR,
  NELA, and combined features; 2502.16857 has all eight original, noised,
  double-finetuned, and ensemble DeBERTa states; and 2507.05157 has separate
  GPT-4o-mini, BERT, and Llama-3-8B rows. Their high development, validation, or
  narrow test cells remain paired with weaker official, transfer, attack, and
  out-of-domain results.
- Full-corpus correction: a fresh mutation review showed that the first curated
  primary list still treated some inspected papers as account-free. The repair
  adds all nine encoder/LoRA states from 2509.00731, eight POGER/SeqXGPT/
  SenDetEX/SenFlow states from 2606.18946, five DeBERTa architecture stages from
  2501.14288, both LuxVeri inverse-perplexity ensembles from 2501.11914, and all
  other qualifying named rows found while rechecking the former zero/parent
  partition. Each now has its own primary-result target.
- Table-wide correction: a further all-paper table pass adds ten comparators in
  TELL arXiv 2605.27921 whose aggregate AUROCs are weak but whose domain cells
  reach 0.909-1.000; Likelihood, Log-Rank, FastDetectGPT, Lastde, and DivEye in
  arXiv 2601.04833, whose generator slices reach 90.28%-94.17%; and ReMoDetect
  and ImBD in the LAPD paper, whose RealDet AUROCs are 92.18% and 92.12% but
  five-benchmark averages are 80.82% and 83.27%. Each row preserves the weaker
  aggregate, artifact absence, method boundary, and timing gap rather than
  promoting a narrow cell. The LAPD paper's baselines, RAI, and S score do not
  inherit LAPD's auxiliary-sampling exclusion; DNA-DetectLLM keeps its separate
  regeneration exclusion, and only the actual LAPD pair states carry the
  10,000-sample blocker.
- Parent-exclusion correction: arXiv 2509.15550 now gives BiScope, Entropy,
  Likelihood, LogRank, DetectGPT, FastDetectGPT, Binoculars, and Lastde++ their
  own mechanisms and table evidence. DetectGPT is multi-perturbation-excluded;
  the other seven are evidence-rejected. Only the seven actual DNA-DetectLLM
  repair/order/model-pair states retain regeneration exclusion. ArXiv 2504.21019
  is corrected in the other direction: DP-Net's uniform/Gaussian embedding
  noise is applied during training, not inference. Its seven-domain average
  accuracy is 85.48%/86.10%, and no frozen state, low-FPR result, or fixed A6000
  timing supports promotion.
- Counterexample dispositions:
  - arXiv 2509.00731 now has RoBERTa, BERT, FastText, three Qwen2.5-7B LoRA
    ranks, and three DeepSeek-R1-Distill-Qwen-7B LoRA ranks. Qwen accuracies are
    0.9431/0.9376/0.9594; DeepSeek rank 8 qualifies through 0.9008 machine-class
    F1 despite 0.8898 accuracy. These Chinese-only fitted states expose no
    released checkpoint, cross-distribution/low-FPR result, or fixed timing. A
    7B LoRA path is plausible on two A6000s but has no scientifically equivalent
    public paper state to screen.
  - arXiv 2606.18946 now has POGER, SeqXGPT, SenDetEX, SenFlow, and four named
    SenFlow ablations. Reported macro F1 is 0.924 for SenDetEX, 0.940 for
    SenFlow, and 0.922-0.935 for the ablations. Every result labels sentences in
    hybrid documents rather than general documents; none supplies a qualifying
    frozen state, fixed calibration, or comparable A6000 timing.
  - arXiv 2501.14288 now has five separate DeBERTa/architecture-stage/ensemble
    rows with AUC 91.2%-94.7%. The earlier no-metric reason was false. All five
    remain evidence-rejected because the paper supplies no public trained state,
    cross-distribution result, low-FPR calibration, or fixed deployment timing.
  - arXiv 2501.11914 now has separate English and multilingual LuxVeri
    inverse-perplexity ensembles. They are explicitly the paper's best systems,
    but official macro F1 is only 0.7458/0.7513 and no released state establishes
    the fixed general-detector screen.
- Result-specific gates are not inherited blindly from a parent. The six
  RAIDAR-containing 2503.22338 configurations are excluded for seven target
  rewrites, while the three NELA-only classifiers are evidence-rejected. Eight
  direct classifiers in 2510.02319 are evidence-rejected, while only the PIFE
  target-canonicalization state inherits that paper's rewrite exclusion. Hosted
  GPT-4o-mini is separately marked closed.
- Leidos correction: the official Task 3 system paper maps MC/v1.0.4 to an
  unweighted multiclass DistilRoBERTa classifier. It is not an ensemble. The
  four submitted mappings are BC/v1.0.1 unweighted binary, BW/v1.0.3 weighted
  binary, MC/v1.0.4 unweighted multiclass, and MW/v1.0.2 weighted multiclass.
- Mechanical controls: the checker hash-binds all four full-text ledgers and the
  exact 805-pair set, reruns PDF extraction, and rejects missing or mis-targeted
  accounts. Thirteen full-text controls cover the ordinary-title selection fixture,
  Candace deletion with a lowered count, non-anchor PAWN deletion with a lowered
  count, deletion of a non-English Qwen LoRA state with a lowered count, content
  detachment for that state, deletion of the narrow-domain ChatGPT-D row with a
  lowered count, content detachment for that row and for a table-derived
  no-account decision, PDF/text detachment, the false Leidos ensemble
  description, false inheritance of parent method blockers by retained LAPD and
  DNA-DetectLLM-paper comparators, and removal of any one of the 119 source rows.
  Together with the eleven accepted composite controls, all twenty-four pass.
- Decision: the recovered configurations are individually visible but do not
  alter the accuracy-first conclusion. They are validation-only, narrow,
  shifted, unreleased, excluded-method, weaker on official/transfer evidence, or
  lack the matched low-FPR, two-A6000, and near-Binoculars timing basis required
  for promotion.

### M8 — Public states surfaced by composite sources

- Durable evidence: [benchmark source](benchmark_composite_detectors.py),
  [design](benchmark_composite_detectors_design.md), successful and failed raw
  stdout/stderr, 8,022-row [score CSV](benchmark_composite_detectors_scores.csv),
  [independent verifier](verify_composite_scores.py),
  [deterministic model layout](prepare_composite_model_layout.sh), layout check,
  interpreter, packages, GPUs, and exact model-file hashes. The layout maps the
  three short harness keys to revision-bearing external snapshot directories
  only after all 25 model files pass. The score CSV SHA-256 is
  `c635d2b98583f9f9bcf3917f7ecb18469185550ab66d46ff60021a977195e786`.
- Shared accuracy boundary: all three public states and stored comparators use
  the same 1,000 human calibration rows and disjoint 2,315-human/1,592-generated
  evaluation rows of at least 100 words. Stored comparators are historical, not
  recomputed in the candidate processes. Candidate released length limits differ
  and are explicit.
- DetectRL-X X-Rob at 512 tokens: evaluation AUROC 0.953253 and evaluation
  FPR/TPR 0.00907/0.27136 at a locally calibrated one-percent FPR. Its two-card
  four-plus-four median is 0.028899 seconds per batch with
  1,145.09/1,135.89 MiB peak allocated. It is extremely fast but trails stored
  Binoculars 0.977899 and FastDetectGPT 0.968952 in AUROC and tail recall.
- Desklib v1.01 at 768 tokens: evaluation AUROC 0.975080 and evaluation FPR/TPR
  0.00907/0.89636 at a locally calibrated one-percent FPR. Its two-card median is
  0.285271 seconds per batch with 2,767.81/2,758.58 MiB peak. It exceeds both
  stored comparators' local tail TPR but falls 0.002819 below Binoculars AUROC.
  RAID-aligned training, the convenience corpus, historical comparators, and
  shorter limit block replacement; it remains a runnable follow-up.
- ModernBERT at 2,048 tokens: evaluation AUROC 0.833729 and evaluation FPR/TPR
  0.01037/0.00628. Its two-card median is 0.300674 seconds per batch with
  977.07/967.42 MiB peak. It passes feasibility and fails discrimination.
- Execution note: the public ModernBERT config's compilation optimization failed
  with concurrent replicas under Transformers 4.57.3. The successful run disables
  only `reference_compile`; model weights, tokenizer, mathematical forward, and
  raw score semantics are unchanged. Both attempts are preserved.
- Decision: none matches or improves the incumbent across the fixed ranking and
  selected low-FPR requirements. Desklib is the only new public state from this
  repair that warrants a frozen follow-up; it is not a recommendation.

### M7 — Local MELD v5 feasibility and bounded accuracy screen

- Durable raw evidence: [benchmark_meld_stdout.txt](benchmark_meld_stdout.txt),
  [benchmark_meld_stderr.txt](benchmark_meld_stderr.txt),
  [score-level CSV](benchmark_meld_scores.csv), environment manifests, model-file
  hashes, and [benchmark source](benchmark_meld.py). The initial Python 3.14
  incompatibility is retained separately; the successful isolated Python 3.13
  environment is fully listed.
- Measured architecture: exact current revision
  `453acf594d48f8c55c3a38bde396f9178516d817`, 394,833,461 parameters, FP32,
  transformers 4.57.3, torch 2.9.1+cu126, and two 49,140 MiB RTX A6000 cards.
- Measured 2,048-token cost over five repetitions: one-GPU batch 8 was 1.200715
  seconds per batch, 0.150089 per document, and 2,682.95 MiB peak allocated.
  Two concurrent replicas, four documents per GPU, were 0.626530 seconds per
  batch, 0.078316 per document, and 2,107.07/2,098.52 MiB peak allocated. That
  two-card batch latency is 0.0810 of M1's fixed 7.732507-second DW1 Binoculars
  batch. Model load, tokenization, and input transfer are excluded from both
  timing boundaries.
- Direct historical screen: on the same seed-42 500-human/500-generated rows used
  for prior controls, MELD AUROC was 0.913200, versus stored Binoculars 0.959486
  and FastDetectGPT 0.953620. The sample includes 291 texts under the v5 card's
  100-word minimum and is retained for continuity, not as the main screen.
- Length-eligible screen: 4,907 available texts have at least 100 words. A fixed
  seed selects 1,000 human calibration texts; the disjoint evaluation has 2,315
  human and 1,592 generated texts. Evaluation AUROC is 0.955271 MELD, 0.977899
  stored Binoculars, and 0.968952 stored FastDetectGPT. At a locally calibrated
  one-percent human FPR, evaluation FPR/TPR is 0.00821/0.90201 for MELD,
  0.01166/0.66080 for Binoculars, and 0.01037/0.75503 for FastDetectGPT.
- Threshold-transfer failure: v5's shipped nominal one-percent threshold produces
  9.0-percent FPR on calibration human text and 8.60-percent FPR on evaluation
  human text. Its nominal five-percent threshold produces 24.1 and 23.46 percent.
  Locally selecting a threshold is therefore essential on this convenience
  corpus.
- Boundary: the corpus is available rather than stratified, generated rows are
  not a new held-out current-generator pool, and comparator scores are historical
  rather than new same-process forwards. The locally calibrated tail TPR is
  promising, but the lower AUROC, non-transferring shipped thresholds, and
  paper-era/v5 mismatch block a recommendation.

### M4 — Local IRM screen

- Durable output: [benchmark_irm_results.txt](benchmark_irm_results.txt).
- Measured: public Qwen2-0.5B pair, float32, two A6000s, batch 8, 2,048 tokens;
  1.833742 seconds per batch, 0.229218 per document, 30,383.789 MiB peak per card.
- Measured accuracy screen: fixed 500 human/500 generated rows, IRM raw AUROC
  0.943596 and orientation-free AUROC 0.943596; stored same-row Binoculars
  0.959486 and FastDetectGPT 0.953620. The base and instruction tokenizers were
  loaded separately and yielded identical token IDs for all selected texts.
- Reproducibility anchors: trial CSV SHA-256
  `964cf196caacaee7cb28c106e0bc7b1177a2567478ab1058dd5ee5f8228aef46`;
  selected-record manifest SHA-256
  `fbddb007a51a13de864711a10fddd1ac8d76f9698f75537ce405ea9a5bce782d`;
  selected path-and-text SHA-256
  `b4b189cbec454c96e752977a66d08bfa4eb7577c86cf3f680a39e910267ab1b9`.
- Boundary: public executable pair, but not the paper's best gated Llama pair;
  local corpus is unstratified and historical comparators may differ in software
  and truncation.

### M5 — Local SV-Detect feature-path screen

- Durable output: [benchmark_svdetect_results.txt](benchmark_svdetect_results.txt).
- Measured: an optimized reconstruction of the public GPT-Neo-2.7B feature
  mathematics, float16, two-A6000 data parallel, total batch 8, 2,048 tokens;
  1.247568 seconds per batch, 0.155946 per document, and at most 8,848.2 MiB peak
  per card.
- Boundary: the official extractor is one-text-at-a-time FP32 and records pooled
  activations to CPU. The harness batches four texts per card and projects inside
  GPU hooks. Deterministic unit directions preserve operation shapes, but this is
  not exact release or end-to-end detector throughput. No trained state was
  released, so no classification result was produced.

### M6 — Local LAPD cost screen

- Durable output: [benchmark_lapd_results.txt](benchmark_lapd_results.txt).
- Measured same-run comparison: DW1 dynamic Falcon pair, two A6000s, batch 8,
  2,048 tokens. LAPD median 7.764121 seconds per batch versus Binoculars 7.723376;
  ratio 1.005276. Both peaked at 35,095.347 MiB per GPU.
- Boundary: same hardware, models, token IDs, batch, documents, and timing boundary
  validate cost only. Paper accuracy from full-precision model pairs does not
  transfer to the dynamic DW1 checkpoints. The harness uses the official cached
  path's base-logit reuse, not the multi-GPU runner's redundant sampling forward.
  The same-process comparator ran in the preceding timing block, not interleaved.
  LAPD remains excluded by the strict auxiliary-sampling constraint.

## Canonical comparators

### C1 — Binoculars paper

- Official source: [ICML 2024 paper](https://proceedings.mlr.press/v235/hans24a.html).
- Preserved evidence: Binoculars paper Markdown, lines 103–105 and 484–492.
- Sourced facts: the main method uses Falcon-7B-Instruct for perplexity and the
  Falcon-7B/Falcon-7B-Instruct pair for cross-perplexity. It uses a 512-token prefix
  unless stated otherwise.
- Exact anchor quote: “For all datasets, we use prefix of 512 tokens”.
- Scope: the paper does not report a per-document runtime suitable for this speed
  screen.

### C2 — Binoculars official implementation

- Official source: [repository at inspected commit](https://github.com/ahans30/Binoculars/tree/c8ae2f90d50ee696418bc71d8d9e5020e5f9d7b8).
- Preserved evidence: `binoculars/detector.py`, lines 19–48 at that commit.
- Sourced facts: defaults are `tiiuae/falcon-7b` and
  `tiiuae/falcon-7b-instruct`, BF16, maximum 512 tokens, and two CUDA devices when
  available.
- Exact anchor quote: “selected using Falcon-7B and Falcon-7B-Instruct at bfloat16”.
- Scope: official fixed thresholds are coupled to that model pair and precision.

### C3 — DW1 operational comparator

- Source: `src/degentweb/classifying/__init__.py`, lines 42–49, and
  `src/degentweb/classifying/binoculars.py`, lines 39–46 and 55–140.
- Sourced facts: DW1 sets a 2,048-token maximum, uses the two
  `SichangHe/falcon-7b-*-FP8-Dynamic` repositories, maps one model to each available
  GPU, and runs the forward passes concurrently. The established trial batch is 8
  in `fdgpt_trial.py`, line 53.
- Exact anchor quote: “Run 2 LLMs with the same tokenizer”.
- Scope: the model objects reported BF16 as `model.dtype` in the local run; the
  repository names alone are not proof that all in-memory weights execute as FP8.

### C4 — FastDetectGPT paper

- Official source: [ICLR 2024 OpenReview](https://openreview.net/forum?id=Bpcgcr8E8Z).
- Preserved evidence: FastDetectGPT paper Markdown, lines 147–179 and 459–477.
- Sourced facts: the canonical black-box pair is GPT-J-6B for sampling/reference
  and GPT-Neo-2.7B for scoring. The paper generated 500 samples per dataset and
  timed XSum generations from five source models. FastDetectGPT took 233 seconds on
  a Tesla A100, excluding model initialization; batch size is not reported. The
  appendix identifies its A100 as 80 GB.
- Exact anchor quote: “excluding the time for initializing the model”.
- E: 233 seconds divided by 2,500 XSum documents is 93.2 milliseconds per document,
  assuming all five 500-document sets are included in the stated total. This is an
  explicit arithmetic inference, not a reported per-document measurement.

## Direct local evidence

### M1 — Controlled DW1 formula timing

- Evidence: `benchmark_dw1.py` and `benchmark_results.txt` in this directory.
- M: two A6000s, batch 8, eight documents each truncated to 2,048 tokens, one
  warm-up plus three timed repetitions, model load excluded.
- M: DW1 Binoculars median was 7.73251 seconds per batch, or 0.966563 seconds per
  document, with 35,095.35 MiB peak allocated on each GPU.
- M: the SpecDetect formula using one DW1 performer forward was 7.53812 seconds per
  batch and 35,095.60 MiB on one GPU; latency ratio to Binoculars was 0.97486.
- M: DetectLLM-LRR using one DW1 performer forward was 7.59651 seconds per batch and
  the same one-GPU peak; latency ratio to Binoculars was 0.98241.
- M: every method used device-resident token IDs as timed input and returned CPU
  detector scores; model load, tokenization, and input transfer were excluded.
- Scope: formula fidelity and runtime were measured, not candidate accuracy with
  that proxy, threshold calibration, model load, or sustained concurrency.

### M2 — WaveDetect public artifact timing and discrimination screen

- Evidence: `benchmark_wavedetect.py` and `benchmark_wavedetect_results.txt`.
- M: official public checkpoint, one A6000, batch 8. At 2,048 tokens, the median was
  0.310073 seconds per batch, 0.038759 seconds per document, and 15,412.90 MiB peak
  allocated. The measured per-document latency was 0.04010 of M1 Binoculars.
- M: on a seed-42 sample of 500 available human and 500 available generated DW1
  texts at the artifact's 1,024-token default, WaveDetect AUROC was 0.890558.
  Stored scores on the identical rows were 0.959486 for Binoculars and 0.953620 for
  FastDetectGPT, with score orientation normalized.
- Scope: this is a triage screen over an existing convenience corpus, not a held-out
  evaluation, low-FPR calibration, or production load test. The stored comparators
  may use different software versions and truncation limits from the WaveDetect
  run.

### M3 — Existing DW1 score corpus

- Evidence: `analyze_existing_scores.py` and `existing_score_results.txt`.
- M: all 8,170 stored rows comprise 6,216 human and 1,954 generated examples.
- M: orientation-free AUROC was 0.94670 Binoculars, 0.93860 FastDetectGPT, 0.79908
  LRR, 0.60777 OpenAI RoBERTa, and 0.67293 RADAR.
- Scope: descriptive reuse of a convenience trial, not a new held-out evaluation.

## Candidate source cards

### W1 — WaveDetect paper

- Official source: [Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.424/).
- Preserved evidence: WaveDetect PDF, sections 4.1, 7, and appendix F.
- Sourced facts: one Qwen2.5-0.5B-Base proxy produces token probabilities; a
  differentiable continuous wavelet transform and modified ResNet-18 classify the
  spectrum. The encoder has 11.7 million parameters. Training used batch 64 on four
  RTX 6000 Ada GPUs. The paper supplies theoretical cost, not measured inference
  latency.
- Exact anchor quote: “one forward pass of a lightweight 0.5B surrogate model and a CNN”.
- Sourced failure boundary: training is primarily RAID-based; the authors state its
  included LLMs are “relatively old or weak”.
- Fit implication: M2, rather than the theoretical table, establishes the two-A6000
  hardware and speed fit for DW1.

### W2 — WaveDetect public artifact

- Official source: [Hugging Face revision](https://huggingface.co/KaitongQin/WaveDetect/tree/c4d72102938842de531990b3e961d3b41aaa4f05).
- Preserved evidence: downloaded artifact hashes in `paper_artifacts.md`; immutable
  `wavedetect_hf.py`, lines 20–25, 75–124, and 126–148; immutable `README.md`,
  lines 1–38; and M2.
- Sourced facts: public, ungated, Apache-2.0 artifact with a roughly 1.01 GB
  checkpoint. The official loader uses BF16 on CUDA, 16 wavelet scales, a kernel of
  128, and a default 1,024-token maximum. Its convenience `predict` method accepts
  one text, while the underlying model accepts a batch.
- Exact anchor quote: “WaveDetect Inference”.
- Artifact result: the unmodified official example executed successfully on an
  A6000 before the direct batched screen.

### L1 — DetectLLM-LRR

- Official sources: [EMNLP Findings 2023](https://aclanthology.org/2023.findings-emnlp.827/) and
  [repository](https://github.com/mbzuai-nlp/DetectLLM/tree/1db7935ae8c6f68cb3ed36f97c207e14b622366d).
- Preserved evidence: DetectLLM paper Markdown, sections 6.1, 8, appendix A and E.
- Sourced facts: LRR divides log likelihood by log rank and needs one scoring-model
  forward. The paper's 10-rerun timing table reports 0.12 seconds for GPT2-XL,
  0.19 for Neo-2.7B, 0.08 for GPT-J, 0.10 for OPT-13B, and 1.20 for NeoX. Models up
  to GPT-J used one A100 40 GB; 13B models used three. The repository's generated
  sequence default is 200 tokens; the timing batch is unreported.
- Exact anchor quote: “averaged over 10 reruns”.
- Sourced failure boundary: the paper identifies unknown or unavailable source-model
  statistics and local LLM inference resources as limitations.
- Fit implication: M1 directly establishes speed and memory for the DW1 performer;
  M3 establishes that its existing discrimination is materially weaker than both
  comparators.

### S1 — SpecDetect and SpecDetect++ paper

- Official sources: [AAAI 2026 article](https://ojs.aaai.org/index.php/AAAI/article/view/40510) and
  [repository](https://github.com/luohaitong/SpecDetect/tree/4fadfad3d4c38590909f19adceac0ac9ecae9547).
- Preserved evidence: SpecDetect paper Markdown, sections 3 and 4.2; extracted
  Figure 4 image in the paper collection.
- Sourced facts: base SpecDetect applies DFT total energy to one proxy model's token
  log-probability sequence. SpecDetect++ adds an analytic sampling discrepancy
  derived from the same logits. In one GPT-4-Turbo/XSum run with GPT-J-6B on one
  H800, average milliseconds per sample were: SpecDetect 42.57, FastDetectGPT
  47.83, SpecDetect++ 47.29, Lastde 50.92, and Lastde++ 93.28. The exact inference
  batch is unreported; official data-generation code defaults to 200 tokens.
- Exact anchor quote: “All runtimes were measured on a single NVIDIA H800 GPU.”
- Fit implication: the paper gives a direct same-run comparison against
  FastDetectGPT, and M1 gives a direct 2,048-token comparison against DW1
  Binoculars. Both base formula comparisons satisfy the speed screen.

### S2 — SpecDetect artifact quality

- Source: official repository at the S1 commit, README and
  `py_scripts/baselines`.
- Exact repository locators: `README.md`, lines 1–13;
  `py_scripts/baselines/scoring_methods/based_scoring_baselines.py`, lines 91–111;
  and `py_scripts/baselines/specdetect_doubleplus.py`, lines 155–177.
- Sourced facts: README calls it an “initial version”; it points to a missing
  top-level `requirements.txt`. The base scorer applies NumPy mean directly to a
  CUDA tensor and then performs a second incompatible centering operation. The
  enhanced scorer computes NumPy arrays and calls `.cpu()` on the result. Those are
  concrete runtime blockers in the inspected paths.
- Exact anchor quote: “more complete implementations and detailed documentation in subsequent versions”.
- Artifact implication: the mathematical formula is easy to reproduce, but the
  official implementation is not deployable unchanged and no official checkpoint
  or calibrated DW1 threshold exists.

### A1 — Lastde and Lastde++

- Official sources: [ICLR 2025 OpenReview](https://openreview.net/forum?id=vo4AHjowKi) and
  [repository](https://github.com/TrustMedia-zju/Lastde_Detector/tree/ead6939e0e9382f9ce5aa1b33b936ee6c4e0605d).
- Preserved evidence: Lastde paper Markdown, sections 3.2, 4.1, and appendix B.2.
- Sourced facts: Lastde combines likelihood with multiscale diversity entropy over
  one proxy model's probability sequence. Lastde++ adds analytic sampling from the
  same model. Black-box experiments default to GPT-J-6B. The paper's setup was two
  RTX 3090 24 GB GPUs, and repository generation defaults to 200 tokens. The paper
  does not report detection latency.
- Exact anchor quote: “two RTX 3090 GPUs (2×24GB)”.
- Runtime boundary: S1's same-H800 comparison puts base Lastde at 50.92 ms versus
  47.83 for FastDetectGPT and Lastde++ at 93.28 ms. There is no direct 2,048-token,
  batch-8, A6000 comparison to Binoculars, so neither variant is called viable for
  DW1; that missing measurement is the exact blocker.

### P1 — PAWN

- Official sources: [arXiv 2501.03940](https://arxiv.org/abs/2501.03940) and
  [repository](https://github.com/pablomiralles22/ai-gen-detection/tree/675e6859fce24fd8e5dafd079c89770f2a4aea18).
- Preserved evidence: PAWN paper Markdown, sections 3.4.2–3.4.4 and 5.
- Sourced facts: one frozen GPT-2 or Llama-3.2-1B-Instruct forward supplies logits
  and hidden states to a trained attention head. Maximum length is 512. Training
  batches are 128 for MAGE, 32 for M4, and 128 for RAID. The head has 989 thousand
  or 1.6 million trainable parameters. All reported experiments used one RTX 3090
  24 GB. Training-cache and epoch times are reported, but inference time is not.
- Exact anchor quote: “All experiments were run on a single NVIDIA GeForce RTX 3090 GPU”.
- Artifact boundary: the official repository has training and benchmark code, but
  no release or standalone checkpoint; README reproduction commands depend on
  local paths and W&B run identifiers.
- Failure boundary: supervised calibration is required, paraphrasing reduces
  performance, and no traceable comparison against DW1 Binoculars speed exists.

### D1 — DetectAnyLLM

- Official sources: [ACM MM 2025 DOI](https://doi.org/10.1145/3746027.3754862),
  [repository](https://github.com/fjc2005/DetectAnyLLM/tree/ea82e853b23077474b1fb82b498ae888c8e69ada), and
  [public adapter](https://huggingface.co/JiachenFu/Qwen2-0.5B-detectanyllm-detector-en/tree/c1bcbefd92919ea27317ebf4e1868ab65bb40eda).
- Preserved evidence: DetectAnyLLM PDF, sections 3 and 5; repository README.
- Sourced facts: the paper builds on FastDetectGPT's one-pass analytic discrepancy
  and trains the scoring model with Direct Discrepancy Learning. Main tables use
  GPT-Neo-2.7B; repository evaluation defaults to batch 1. README reports about
  11 GB for training and 15 GB for evaluation. Section 3.3 and equations 11–13
  define Reference Clustering: retained machine and human reference sets are
  scored, their distances to the input are sorted, and a nearest window is used
  for the output ratio. No inference timing is reported.
- Exact anchor quote: “GPU memory cost: ~15G”.
- Retrieval anchor quote: “the value in M ∪ H that is kth closest”.
- Artifact boundary: the public artifact is a roughly 2.2 MB LoRA adapter over
  Qwen2-0.5B, a different smaller variant from the paper's main model. Its model
  card leaves use, evaluation, speed, hardware, and license details unfilled.
- Exclusion implication: its claimed memory fits one A6000, but Reference
  Clustering violates the fixed no-retrieval rule. Variant traceability,
  2,048-token behavior, and like-for-like speed would also remain unverified if
  retrieval were allowed.

### R1 — RADAR

- Official sources: [NeurIPS 2023 paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/30e15e5941ae0cdab7ef58cc8d59a4ca-Abstract-Conference.html),
  [repository](https://github.com/IBM/RADAR/tree/3a9acf6d3d9b1766f5c6497af96601dea1ead868), and
  [public checkpoint](https://huggingface.co/TrustSafeAI/RADAR-Vicuna-7B/tree/4ff1f23a69a36aa1df47b0933be6279f1b896c9b).
- Preserved evidence: RADAR paper Markdown, sections 3–4; repository README.
- Sourced facts: paraphrasing is used during adversarial training, not detector
  inference. The released detector is RoBERTa-large, takes at most 512 tokens, and
  has a 1,421,627,665-byte public weight file. Training used batch 32 on two V100
  32 GB GPUs. No paper inference runtime is reported.
- Exact anchor quote: “trained from the RoBERTa-large model”.
- Failure boundary: RAID reports clear model/domain bias and unusually poor movie
  review detection. M3 likewise gives only 0.67293 local AUROC, so RADAR is rejected
  for DW1 quality despite a clear hardware fit and fast historical local execution.

### R2 — RAID robustness control

- Official source: [ACL 2024](https://aclanthology.org/2024.acl-long.674/).
- Preserved evidence: RAID paper Markdown, findings 1–6 and conclusion.
- Sourced facts: RAID covers over six million generations across model, domain,
  decoding, and attack variations. It finds threshold, repetition penalty,
  generator, domain, and adversarial sensitivity. Binoculars was notably strong at
  low false-positive rates; RADAR showed training-distribution bias.
- Exact anchor quote: “calibrate detectors on in-domain data before using them”.
- Operational implication: AUROC screening cannot replace an in-domain low-FPR
  threshold and robustness study for any recommendation here.

## Screened but excluded lanes

### F1 — FourierGPT

- Official sources: [EMNLP 2024 paper](https://aclanthology.org/2024.emnlp-main.564/)
  and [repository at inspected commit](https://github.com/CLCS-SUSTech/FourierGPT/tree/ec84e8fad1767cf166210d6981d6bb4b1b2ede24).
- Preserved evidence: exact PDF and SHA-256 in `paper_artifacts.md`; paper sections
  3.1–3.3, 5.2, and 7; repository `README.md` procedure and classifier sections.
- Sourced facts: Mistral-7B, GPT-2-family, or a bigram estimator supplies token
  likelihoods with one forward, followed by normalization and a Fourier transform.
  The paper evaluates 50-, 100-, and 150-token cutoffs but reports no inference
  timing, hardware, batch size, or memory.
- Sourced operational boundary: the supervised path needs labeled fitting; the
  heuristic path only decides which member of a pair is machine-written and
  requires both texts to come from the same prompt. The repository exposes these
  supervised and pairwise experiment paths, not a calibrated single-text detector.
- Exact anchor quote: “the input pair must come from the same text prompt”.
- Fit implication: a 7B-or-smaller single forward is plausibly within A6000 memory,
  but that is only an inference. With no measured runtime and no deployable
  single-document classifier, FourierGPT is screened out rather than called viable.

### X1 — Ghostbuster

- Official source: [NAACL 2024](https://aclanthology.org/2024.naacl-long.95/).
- Sourced fact: probability features use a trigram model, unigram model, and the
  closed ada and davinci models. The official paper links a data repository rather
  than a runnable released detector.
- Exact anchor quote: “two early GPT-3 models (ada and davinci)”.
- Exclusion: it cannot be reproduced as a self-contained two-A6000 DW1 detector.

### X2 — Method-family exclusions

- DetectGPT and DetectNPR require many perturbed versions and repeated scoring.
- DNA-GPT truncates and rewrites/completes input prefixes.
- RAIDAR and TOCSIN derive detection signals from rewritten or regenerated text.
- DetectAnyLLM Reference Clustering searches retained human and generated reference
  sets for the nearest discrepancy window at detection time.
- Retrieval defenses, RAG detectors, k-nearest-neighbor proxy approaches, and
  example-retrieval prompting require retrieval at detection time.
- These were excluded by method, before hardware ranking; their reported accuracy
  cannot override the human's explicit latency and operational constraint.
