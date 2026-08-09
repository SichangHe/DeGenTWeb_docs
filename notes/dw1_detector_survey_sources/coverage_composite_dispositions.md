# Embedded-result source cards for composite publications

Frozen review date: 2026-08-08, America/Los_Angeles.

## Reading and accounting rule

Overview, benchmark, comparative, and shared-task publications are composite
sources: one publication row can contain many independently qualifying detector
results. `coverage_embedded_results.tsv` is the canonical result-level ledger.
Each of its 241 rows records one system/version, the exact qualifying metric and
scope, a primary source or the bounded-search absence sentinel, artifact status,
and an explicit disposition. `coverage_composite_sources.tsv` records the exact
scope inspected for all 33 composite sources, including source-specific reasons
for the seven sources with no independently qualifying child result.
`coverage_embedded_result_audit.tsv` is generated, not hand
edited, and binds every child to exactly one parent and source card. A separate
hand-reviewed `coverage_expected_result_ids.tsv`, immutably bound by a checker
hash, enumerates the exact 241 parent/result pairs so changing a count and deleting
a child cannot recreate a semantic catch-all. Twenty-six sources have explicit
child inventories; the two former parent-only rows now expand separately named
comparison systems while retaining the proposed parent method's disposition.
Each expanded heading carries a machine-readable HTML comment that binds its
E-card label and parent identifier to the complete result-ID set. The audit
parses those comments, checks them against both ledgers, and binds this Markdown
file by SHA-256; deleting or misassociating a real card is therefore a failure.

The cards below summarize mechanism and comparability at the publication level;
they do not replace the individual result rows. Paper-reported values are sourced
claims rather than local replications. A high cell is retained even when its
dataset, language, training regime, metric, or artifact state prevents promotion.

## E1 — GenAI Detection Task 3 overview, arXiv 2501.08913

<!-- coverage-card E1 parent=2501.08913 results=2501.08913:leidos-v1.0.3;2501.08913:leidos-v1.0.2;2501.08913:leidos-v1.0.4;2501.08913:leidos-v1.0.1;2501.08913:pangram;2501.08913:ustc-bupt-r-l-focal-loss;2501.08913:alert-v1.1;2501.08913:cnlp-nits-distilbert;2501.08913:alert-v1.2;2501.08913:lux-rb-roai;2501.08913:lux-roai-bert;2501.08913:lux-finetuned-rb;2501.08913:lux-radar-r-l;2501.08913:cnlp-adv-submission-3;2501.08913:cnlp-adv-new-detector;2501.08913:ustc-roberta-dataaug;2501.08913:binoculars;2501.08913:mosaic-5;2501.08913:gltr;2501.08913:openai-roberta-large -->

- Primary overview: [GenAI Detection Task 3](https://arxiv.org/abs/2501.08913),
  preserved PDF SHA-256
  `7ff2de1560787f5859f7a3bbac20a104bb30a51f0843299a945757685e6db4af`.
  The official train and test distributions contain the same 11 generators,
  eight domains, and four decoding strategies; the adversarial task applies 11
  attacks, and no generator or domain is held out. The non-adversarial
  generation table reports 323.4 mean tokens overall, with generator means from
  185.6 to 404.4 tokens; none of the eight qualifying results is broken out by
  text length. Tables 4 and 5 report domain-adjusted TPR at five-percent FPR on
  the non-adversarial and adversarial RAID-derived tests. The evaluator searches
  a separate threshold for each detector and domain to within 0.0005 FPR, but
  neither the overview nor the system releases preserve those thresholds or
  identify a reusable independent calibration split. These matched, per-domain
operating points therefore are not directly comparable with DW1's single
frozen calibration and transfer screen. Every submitted version or baseline
reaching 90 percent on any official aggregate, domain, or attack cell is
expanded below; a weak aggregate never suppresses a high slice.
- **Leidos v1.0.3, v1.0.2, v1.0.4, and v1.0.1:** the four score rows are
  respectively 99.4/97.2, 99.3/97.7, 99.2/97.6, and 99.1/95.7 percent. The
  [primary system paper](https://aclanthology.org/2025.genaidetect-1.39/), PDF
  SHA-256 `9f25944491038204c8799cd691bacb192b342a75b7665779f43908e0e4bd53fc`,
  describes DistilRoBERTa binary and multiclass submissions, each with and
  without static class weighting. Training randomly partitions RAID, reserving
  50,000 validation and 400,000 internal-test examples, and evaluates the best
  model separately on Task-1-derived generators; the paper does not report a
  maximum input length, batch size, optimizer, learning rate, or epoch count.
  v1.0.3 is the non-adversarial winner at 99.4 percent, while class-weighted
  multiclass v1.0.2, not v1.0.3, reaches the 97.7-percent adversarial lead. No
  official trained state, detector repository, frozen threshold vector, or
  inference timing was found. Each version is therefore separately
  retained/rejected rather than treating one split winner as a universal best.
- **Pangram:** 99.3/97.7 percent. The
  [primary paper](https://aclanthology.org/2025.genaidetect-1.40/), PDF SHA-256
  `7d95eeb40f45b2d04ca3916a7ee5c2f57c552435ec3bfdc567f0ec22ea43a3a4`,
  describes a closed Mistral-Nemo-12B LoRA detector. Its first stage mirrors
  pre-2022 human text from reviews, news, web, email, essays, creative writing,
  Q&A, scientific/medical papers, books, and Wikipedia with GPT-3.5/4, Claude,
  Llama, Mistral, and Gemini families; its second stage retrains on the 50,000
  highest-error RAID generations and paired human examples. It crops to 512
  tokens and reports two one-epoch training stages, initially on eight A100s
  with effective batch 24, AdamW, linear decay, and weighted cross entropy.
  Header removal and Unicode normalization occur before tokenization in the
  described data pipeline, but the paper does not say whether deployed inference
  transforms targets, so that ambiguity is not used as a method exclusion. The
  service state, domain thresholds, independent transfer operating point, and
  comparable timing are not public; the result is retained/rejected rather than
  screened.
- **USTC-BUPT R-L Focal Loss:** 98.1/92.7 percent. The overview supplies only a
  RoBERTa-large system trained on RAID with focal-loss alpha 0.65 and gamma 2.5,
  four synonym-replaced samples per human example, and AI downsampling to a 2:1
  AI/human ratio. The overview gives no input-length limit, remaining optimizer
  or schedule details, or released threshold. Its bibliography has no primary
  system paper, and bounded exact team/system searches of public OpenAlex, DBLP,
  and GitHub found no paper, repository, or trained state. The explicit
  result-level disposition is `primary_absent`; the summary cannot establish
  reproducibility, independent calibration, two-A6000 fit, or speed.
- **ALERT v1.1:** 91.8/82.6 percent. The
  [primary paper](https://aclanthology.org/2025.genaidetect-1.42/), PDF SHA-256
  `2fedcda2c27feee5d7783ba9990c1b7dae6b4a8d0867ff5090c9564e343e8988`,
  describes Qwen2-1.5B and E5-Mistral-7B authorship-style encoders and a two-layer
  classifier. It splits RAID 60/20/20 with generator, domain, and attack balance;
  trains the encoders about five epochs with AdamW, learning rate 5e-5, and
  effective batch 2,048; and trains the classifier three to five epochs with a
  validation-selected checkpoint. Long documents are segmented into paragraphs,
  but no numeric maximum evaluated length is reported. Training used four RTX
  A6000 GPUs. The paper releases neither trained classifier state nor official
  thresholds and gives no comparable inference timing; four-card training
  hardware does not establish the fixed two-A6000 deployment screen. It is
  individually retained/rejected, with its sub-0.90 adversarial score explicit.
- **CNLP-NITS-PP DistilBERT:** 90.5/41.6 percent. The
  [primary paper](https://aclanthology.org/2025.genaidetect-1.38/), PDF SHA-256
  `353b54f5b72f5fcb8dfe9b4e290ac482764d25c31b1a89368f2aca2f5369e03a`,
  samples 40 percent of RAID adversarial training IDs and fine-tunes DistilBERT
  at maximum sequence length 128, batch 16, learning rate 2e-5, three epochs,
  AdamW, and cross entropy on a Quadro P2000. Its pipeline first predicts an
  attack and then normalizes or rewrites every target before classification. It
  has no trained public state, released calibration, or timing and collapses on
  the adversarial aggregate. The target transformation independently crosses
  the fixed no-rewriting boundary.

- **Twelve additional high-slice rows:** ALERT v1.2; four LuxVeri variants;
  CNLP Adv.-submission-3 and Adv.-New-Detector; USTC-BUPT Roberta_dataaug;
  Binoculars; MOSAIC-5; GLTR; and OpenAI RoBERTa-large all cross 90 percent on
  at least one domain or attack while their official aggregates range from
  89.3 down to 30.8 percent non-adversarial and from 80.1 down to 27.6 percent
  adversarial. LuxVeri and MOSAIC primary PDFs are preserved alongside the
  existing ALERT/CNLP papers; USTC's second version has an explicit bounded
  primary-absence result. Binoculars, GLTR, and OpenAI Detector remain older
  controls. The CNLP versions inherit the documented conditional target
  normalization/rewriting exclusion. Each row records its exact high cell and
  weak aggregate, so none can masquerade as general accuracy.

These twenty result rows are immutable checker expectations. The independent
exact-result inventory also binds all other expanded publications; omitting any
one of the 241 expected result IDs, lowering a mutable count, or substituting a
nonexistent source-card label makes the coverage audit fail.

## E2 — Counter Turing Test Task A overview, arXiv 2605.20761

<!-- coverage-card E2 parent=2605.20761 results=2605.20761:sarang;2605.20761:dakiet;2605.20761:tesla;2605.20761:skdu;2605.20761:drocks;2605.20761:llama-mamba;2605.20761:ai-blues;2605.20761:nlp-great -->

The weighted-F1 leaderboard has eight qualifying systems, each represented by a
separate ledger row: Sarang 1.0000, Dakiet 0.9999, Tesla 0.9962, SKDU 0.9945,
Drocks 0.9941, Llama_Mamba 0.9880, AI_Blues 0.9547, and NLP_great 0.9157.
Primary papers are preserved for Sarang, Dakiet, SKDU, Drocks, and AI_Blues.
The bounded exact searches in `coverage_primary_search_log.md` found no public
primary paper, repository, or checkpoint for Tesla, Llama_Mamba, or NLP_great;
their rows therefore use the explicit primary-absence sentinel. The paper-backed
systems also release no frozen trained detector state. Task-specific weighted F1
does not establish cross-distribution AUROC, a low-FPR operating point, or
near-Binoculars timing, so none is promoted.

## E3 — DetectRL-X benchmark, arXiv 2605.15518

<!-- coverage-card E3 parent=2605.15518 results=2605.15518:x-rob-classifier;2605.15518:mdeberta-classifier;2605.15518:gecscore;2605.15518:biscope -->

X-Rob-Classifier reports 95.58 percent best F1 and 91.31 percent F1 at one-percent
FPR; mDeBERTa-Classifier reports 95.48 and 93.20 percent. Both are trained on the
benchmark's binary setting and degrade in its ternary setting. The official
release contains an immutable XLM-RoBERTa classifier state for X-Rob but no
equivalent frozen mDeBERTa state. The released X-Rob state is included in the
bounded A6000 screen; its final local disposition is recorded in M8 and the
result-level ledger. Reconstructing mDeBERTa would create a new state, so that
row remains reconstruction-only. GECScore and BiScope also reach 91.36 and
92.85 percent respectively on one binary-language best-F1 cell, despite weak
70.10/57.36 and 80.06/63.62 percent multilingual best/low-FPR averages. Both
now have individual result rows; the former lacks an immutable fitted state and
the latter's exact benchmark fit/calibration is not released.

## E4 — AITDNA mixed-authorship benchmark, arXiv 2606.04906

<!-- coverage-card E4 parent=2606.04906 results=2606.04906:pangram;2606.04906:gptzero -->

Pangram reports 0.932 F1 with 0.155 FPR and GPTZero reports 0.908 with 0.115 on
the paper's new document-level mixed-authorship definition. Both are closed
commercial services whose tested versions cannot be frozen. The metric notion,
high false-positive rates, unavailable state, and absent fixed A6000 timing make
both explicit commercial-closed dispositions rather than reusable candidates.

## E5 — C-ReD Chinese-domain benchmark, arXiv 2604.11796

<!-- coverage-card E5 parent=2604.11796 results=2604.11796:lapd;2604.11796:remodetect;2604.11796:roberta-base;2604.11796:roberta-large;2604.11796:imbd;2604.11796:log-likelihood;2604.11796:entropy;2604.11796:log-rank;2604.11796:lrr;2604.11796:fastdetectgpt;2604.11796:lastde-plus-plus;2604.11796:dna-detectllm -->

Twelve named rows qualify. In addition to LAPD, ReMoDetect-DeBERTa, and the
three C-ReD-trained RoBERTa/ImBD families, Log-Likelihood, Entropy, Log-Rank,
LRR, FastDetectGPT, Lastde++, and DNA-DetectLLM each exceed 0.90 on a domain or
generator cell. Their weaker five-domain means remain explicit: several peak
only on Q&A, while others have no domain mean above 0.90 despite near-perfect
generator cells. LAPD and Lastde++ violate the multi-perturbation boundary;
DNA-DetectLLM iteratively constructs an ideal replacement sequence and violates
the regeneration boundary. The older token-statistic methods remain controls,
and the four trained/comparison states remain Chinese/domain-specific without
released frozen detector states, a fixed English low-FPR comparison, or
like-for-like timing. Official C-ReD source commit
`b90072cd218b6ebdbd1d1478ce6e439677f18192` is preserved, but source does not
substitute for the missing trained states.

## E6 — EnsemJudge shared-task system, arXiv 2603.27949

<!-- coverage-card E6 parent=2603.27949 results=2603.27949:qwen-lora;2603.27949:qwen-lora-extreme-short;2603.27949:qwen-lora-short;2603.27949:ensemjudge;2603.27949:fastdetectgpt-qwen;2603.27949:fastdetectgpt-analytical-qwen;2603.27949:fastdetectgpt-analytical-glm;2603.27949:binoculars-qwen;2603.27949:chinese-roberta;2603.27949:chinese-roberta-extreme-short;2603.27949:glm-lora;2603.27949:hybrid-feature-roberta;2603.27949:hybrid-feature-roberta-extreme-short -->

Thirteen configurations qualify. Three Qwen2.5-7B-Instruct LoRA submissions
report overall macro F1 of 0.9409, 0.9057, and 0.9572, while EnsemJudge reports
0.9922. Three FastDetectGPT proxy variants, Binoculars, two ChineseRoBERTa
variants, GLM-4-9B-Chat LoRA, and two HybridFeatureRoBERTa variants also cross
0.90 on normal, attack, or 256/512-token cells while overall macro F1 can be as
low as 0.7701. Every configuration is individually visible with its aggregate.
The baseline methods remain controls; trained states are Chinese-task-specific
and unfrozen, while the ensemble also multiplies deployment cost. No public
submitted state, cross-distribution low-FPR evidence, or comparable timing
supports promotion.

## E7 — English/Italian comparative neural study, arXiv 2603.18750

<!-- coverage-card E7 parent=2603.18750 results=2603.18750:mobilenet-cnn;2603.18750:gptzero-dten;2603.18750:cnn1d-artmh;2603.18750:mlp-artmh;2603.18750:zerogpt-artmh;2603.18750:gptzero-artmh;2603.18750:quillbot-artmh;2603.18750:originality-artmh;2603.18750:sapling-artmh;2603.18750:isgen-artmh;2603.18750:transformer-dten;2603.18750:rephrase;2603.18750:writer -->

Thirteen rows cover all twelve unique named detectors with any overall or
class-specific value at or above 90 percent; GPTZero retains separate dtEN and
ART&MH results. In addition to the prior MobileNet, CNN1D, MLP, GPTZero,
ZeroGPT, QuillBot, Originality.ai, Sapling, and IsGen rows, Transformer,
Rephrase, and Writer are explicit. Several qualify only because one class is
predicted almost universally—for example Writer has perfect GenAI detection
but zero human detection—so weak balanced accuracy stays in the row. Proposed
classifiers are retained/rejected because the tiny tests and checkpoint-free
official notebooks cannot establish generalization. Closed service versions
cannot be frozen. The official notebook archive contains no trained checkpoint.

## E8 — Bengali benchmark, arXiv 2512.21709

<!-- coverage-card E8 parent=2512.21709 results=2512.21709:xlm-roberta-large;2512.21709:mdeberta-v3-base;2512.21709:banglabert-base;2512.21709:multilingual-bert;2512.21709:zeroshot-banglabert;2512.21709:zeroshot-indicbert;2512.21709:zeroshot-multilingualbert -->

Four fine-tuned rows report AUROC from 0.9453 to 0.9687 on a Bengali
ChatGPT-paraphrase split; three also exceed 0.90 macro F1. Three separate
zero-shot variants—BanglaBERT, IndicBERT, and MultilingualBERT—reach
92.47–99.70 percent recall while accuracy stays at 50.04–50.34 percent and F1
at 65.04–66.70 percent. All seven are explicit, preventing a recall-only high
cell from appearing to be balanced accuracy. Each is rejected on language/data
scope. Only base models are public: no paper fine-tune, general English
transfer, fixed-FPR operating point, or deployment timing is released.

## E9 — detector-bias comparison, arXiv 2512.09292

<!-- coverage-card E9 parent=2512.09292 results=2512.09292:glimpse;2512.09292:binoculars;2512.09292:desklib -->

Glimpse reports 0.948 AUROC, Binoculars 0.907, and Desklib v1.01 0.994 on the
bias-study aggregate. Glimpse remains an unfrozen white-box score and Binoculars
is the existing control. Desklib supplies an immutable public custom DeBERTa
classifier at revision `5fdea974cd4287c61674951ec78803aa274e2fb7`; it is
therefore included in the bounded screen rather than promoted from the table.
M8 and the result ledger record the final measured disposition.

## E10 — MINT white-box benchmark, arXiv 2510.19492

<!-- coverage-card E10 parent=2510.19492 results=2510.19492:loss;2510.19492:logrank;2510.19492:min-k;2510.19492:min-k-plus-plus;2510.19492:fastdetectgpt;2510.19492:binoculars;2510.19492:detectllm;2510.19492:lastde-plus-plus;2510.19492:rank;2510.19492:entropy;2510.19492:reference;2510.19492:zlib;2510.19492:neighborhood;2510.19492:recall;2510.19492:dc-pdd;2510.19492:detectgpt -->

All sixteen Table 3-4 methods are explicit. The eight high white-box averages
remain Loss, LogRank, Min-K percent, Min-K-percent-plus-plus, FastDetectGPT,
Binoculars, DetectLLM, and Lastde++. Rank, Entropy, Reference, Zlib,
Neighborhood, ReCaLL, DC-PDD, and DetectGPT have weaker averages but each
reaches 0.90–1.00 on at least one domain/generator cell, so all eight receive
rows too. Neighborhood and DetectGPT perturb targets repeatedly; ReCaLL
retrieves ten held-out human prefixes per domain; Lastde++ uses sampled
perturbation normalization. Those paths remain method-excluded. Other scores
require matched/surrogate likelihoods or static reference corpora and exhibit
severe black-box variance. High cells do not become a generator-agnostic
public detector result.

## E11 — Urdu case study, arXiv 2510.16573

<!-- coverage-card E11 parent=2510.16573 results=2510.16573:mdeberta-v3-base;2510.16573:distilbert-multilingual;2510.16573:xlm-roberta-base -->

All three fine-tuned multilingual transformers are explicit. mDeBERTa-v3-base
reports 0.9126 test accuracy and 0.9129 F1. DistilBERT has sub-0.90 test
accuracy/F1 but 0.9016 precision. XLM-RoBERTa reaches 0.9087/0.9089
accuracy/F1 during training and 0.9033 test precision, while test accuracy/F1
are 0.8905/0.8907. The dataset contains 3,600 original Urdu documents from
literature, news, and encyclopedic sources, augmented by GPT-4o-mini, Gemini,
and Kimi rephrasings, then chunked into 6,133/767/767 train/validation/test rows.
No trained Urdu state, exact split artifact, low-FPR calibration, or timing is
released. All three are separately rejected on language/data scope; training or
precision-only crossings are labeled rather than suppressed.

## E12 — ALHD Arabic benchmark, arXiv 2510.03502

<!-- coverage-card E12 parent=2510.03502 results=2510.03502:arabertv2-large;2510.03502:araelectra;2510.03502:arabertv2-base;2510.03502:xlm-r-large;2510.03502:asafaya-bert-large;2510.03502:xlm-r-base;2510.03502:marbert;2510.03502:asafaya-bert-base;2510.03502:arberv2;2510.03502:google-mbert;2510.03502:linearsvc;2510.03502:logistic-regression;2510.03502:random-forest -->

Thirteen rows exceed 0.90 ROC-AUC: ten BERT-family models plus LinearSVC,
LogisticRegression, and RandomForest. The exact accuracy, macro-F1, ROC-AUC,
artifact status, and separate scope disposition for every row are preserved in
the result ledger. The official ALHD source commit
`f7b8450fe0ffbafb3d580e5791b2e010b76a83a5` is preserved, but no fitted
classifier is released. Arabic-only evaluation, weak F1 for several high-AUROC
rows, absent fixed-FPR evidence, and missing timings prevent promotion.

## E13 — Central-European benchmark, arXiv 2509.26051

<!-- coverage-card E13 parent=2509.26051 results=2509.26051:llama-3.2-3b;2509.26051:mdeberta-v3-base;2509.26051:gemma-2-2b;2509.26051:xlm-roberta-base;2509.26051:fastdetectgpt;2509.26051:binoculars;2509.26051:llm-deviation -->

Llama-3.2-3B, mDeBERTa-v3-base, Gemma-2-2B, and XLM-RoBERTa-base report mean
AUROC of 0.9758, 0.9739, 0.9660, and 0.9621 across eight Central European
languages. FastDetectGPT and Binoculars additionally reach 0.9667 and 0.9555
on Llama-2 generations despite means near 0.78/0.76, and LLM-Deviation reaches
0.9025–0.9083 only on selected regional-news languages despite a 0.7060 news
mean. All seven rows are separate. No new trained checkpoint or calibration is
released; language/benchmark scope and missing general-English low-FPR and
timing evidence prevent promotion.

## E14 — LLMTrace benchmark, arXiv 2509.21269

<!-- coverage-card E14 parent=2509.21269 results=2509.21269:english-only;2509.21269:russian-only;2509.21269:bilingual -->

English-only, Russian-only, and bilingual Mistral-7B classifiers report roughly
98.4 percent mean accuracy and 97.8–98.0 percent TPR at one-percent FPR on the
constructed LLMTrace test sets. The fixed-FPR claims are retained individually,
but no trained classifier state, external transfer result, or inference-time
basis is public. The Russian row is language-scope-rejected; English and
bilingual rows are retained/rejected as unfrozen benchmark-aligned claims.

## E15 — SHIELD style benchmark, arXiv 2507.15286

<!-- coverage-card E15 parent=2507.15286 results=2507.15286:binoculars;2507.15286:fastdetectgpt;2507.15286:radar -->

Binoculars and FastDetectGPT each exceed 0.90 AUROC in three style aggregates and
remain existing controls. RADAR reaches 0.917 in one RMM/Gemma cell while its
URSS is only 0.311; that isolated cell receives its own retain/reject row rather
than being hidden or promoted. Weak weighted robustness metrics govern the
benchmark interpretation.

## E16 — OpenTuringBench, arXiv 2504.11369

<!-- coverage-card E16 parent=2504.11369 results=2504.11369:log-l;2504.11369:log-r;2504.11369:gltr;2504.11369:lrr;2504.11369:lm-d;2504.11369:detective;2504.11369:otbdetector;2504.11369:rank;2504.11369:entropy;2504.11369:fastdetectgpt;2504.11369:openai-detector;2504.11369:chatgpt-detector -->

All twelve Table 10 systems cross 0.90 on at least one reported precision,
recall, or F1 cell. Seven have strong paired F1: Log-Likelihood, Log-Rank,
GLTR, LRR, LM-D, DeTeCtive, and OTBDetector. Rank, Entropy, and FastDetectGPT
are high only on the easier OOD-text F1 column; OpenAI Detector and ChatGPT
Detector qualify on precision while F1 remains below 0.90. The paper fine-tunes
model-based comparisons for ten epochs but releases none of those exact states.
Every method is explicit; controls remain controls, and unfrozen states remain
reconstruction-only or retained/rejected. Exact high and weak values are in the
result ledger.

## E17 — SPADE dialogue-domain study, arXiv 2503.15044

<!-- coverage-card E17 parent=2503.15044 results=2503.15044:roberta;2503.15044:mlp;2503.15044:xgboost;2503.15044:logistic-regression;2503.15044:svm;2503.15044:random-forest -->

RoBERTa, MLP, XGBoost, Logistic Regression, SVM, and Random Forest report mean
macro F1 from 0.9196 to 0.9734 across four dialogue tasks. Every model has a
separate row. Cross-dataset transfer and specialist dialogue-domain limits,
unreleased trained states, and absent fixed-FPR/timing evidence make all six
scope rejections.

## E18 — model-collapse detector study, arXiv 2502.15654

<!-- coverage-card E18 parent=2502.15654 results=2502.15654:roberta;2502.15654:deberta-v3;2502.15654:modernbert;2502.15654:mage-longformer -->

RoBERTa reports 0.982 in-distribution and 0.846 out-of-distribution AUC;
DeBERTa-v3 0.971/0.817; ModernBERT 0.986/0.943; and the cited MAGE Longformer
0.99/0.94. The first two are explicitly retained/rejected for transfer failure,
and MAGE is an existing control. Only ModernBERT has an official public detector
state, revision `08f218f1d05791ad99c26ede421f69c781a50360`, preserved with the
official model-collapse source commit
`feb8511479a2e2dc868e1caf3f63cb99f1fcc746`. The checkpoint is included in M8's
bounded screen; the paper table alone does not promote it.

## E19 — author-role bias benchmark, arXiv 2502.12611

<!-- coverage-card E19 parent=2502.12611 results=2502.12611:binoculars;2502.12611:fastdetectgpt;2502.12611:detectgpt;2502.12611:gltr;2502.12611:chatgpt-roberta;2502.12611:radar;2502.12611:xgb-classifier;2502.12611:extra-trees;2502.12611:mlp-classifier;2502.12611:linear-svc;2502.12611:random-forest;2502.12611:linear-discriminant-analysis;2502.12611:logistic-regression;2502.12611:bagging-classifier;2502.12611:voting-classifier;2502.12611:decision-tree;2502.12611:gradient-boosting;2502.12611:adaboost;2502.12611:extra-tree;2502.12611:bernoulli-nb -->

Six public detectors cross 0.90 TPR at five-percent FPR on an overall,
generator, or CEFR subgroup cell: Binoculars, FastDetectGPT, DetectGPT, GLTR,
HC3 ChatGPT-RoBERTa, and RADAR. Their overall means are respectively 0.927,
0.894, 0.784, 0.783, 0.745, and 0.690, which remain beside the high cells.
Binoculars, FastDetectGPT, and RADAR are controls; DetectGPT is
multi-perturbation-excluded; GLTR and ChatGPT-RoBERTa are older narrow methods
without new deployment evidence.

Appendix Figure 42 also reports HC3 in-domain accuracy at or above 0.90 for 14
study-fitted lexical classifiers: XGBoost, Extra Trees, MLP, LinearSVC, Random
Forest, Linear Discriminant Analysis, Logistic Regression, Bagging, Voting,
Decision Tree, Gradient Boosting, AdaBoost, Extra Tree, and Bernoulli Naive
Bayes. Figure 43 exposes their out-of-domain ICNALE-plus-LLM aggregate accuracy
from 0.432 to 0.770. Official code/data are public, but no fitted classifier,
feature-pipeline bundle, threshold, or timing is released. All 14 therefore have
reconstruction-only rows; trivial two-A6000 fit would not make a speed screen
meaningful after the documented transfer collapse. This card has 20 children in
total and no longer uses aggregate-only or subgroup exceptions.

## E20 — cross-dataset detector evaluation, arXiv 2604.16607

<!-- coverage-card E20 parent=2604.16607 results=2604.16607:binoculars;2604.16607:fdg-gpt-neo;2604.16607:fdg-gpt-j;2604.16607:fdg-falcon-7b;2604.16607:zippy-lzma;2604.16607:zippy-ensemble;2604.16607:biscope-arxiv;2604.16607:biscope-yelp;2604.16607:biscope-essay;2604.16607:biscope-creative;2604.16607:detective-mage;2604.16607:detective-m4gt -->

Table 2 reports the best, worst, and mean AUROC for 15 public detector variants
on seven class-balanced test sets derived from MAGE/MAGE-OOD, M4GT, H3C+, and
RAID. The evaluator selected 10,000 examples per dataset; the paper emphasizes
wide domain, generator, style, and length variation, including a 26-word mean
for one short informal-human set and errors that vary substantially below and
above 400 words. It uses default 0.5 labels for threshold metrics and AUROC for
Table 2, not an independently frozen DW1 calibration. No per-method threshold
bundle is released.

Twelve named variants have a best-dataset AUROC from 0.92 to 1.00 and therefore
receive rows even though every one has a worst value at or below 0.60 and means
are only 0.66–0.80: Binoculars; three FastDetectGPT proxy variants; two Zippy
compression variants; four separately trained BiScope domain variants; and two
DeTeCtive dataset variants. Binoculars and FastDetectGPT remain existing
controls. Zippy retains LLM-generated seed dictionaries and is excluded by the
retrieval boundary. The public BiScope release supplies code/data but no single
best fitted state; the evaluation authors trained the four variants, so they are
reconstruction-only. DeTeCtive publishes dataset checkpoints but performs KNN
against a retained embedded training database, which also violates retrieval.
The paper used one 48-GB L40S for GPU experiments but reports no per-method
latency or memory. Capacity is plausible for several variants on two A6000s,
but the method exclusions, missing exact states, and weak cross-dataset means
make a new bounded speed screen scientifically unnecessary.

Primary identities are explicit: Binoculars arXiv 2401.12070; FastDetectGPT
arXiv 2310.05130; BiScope DOI 10.52202/079017-3307 and official repository;
DeTeCtive arXiv 2410.20964 and official repository/checkpoints; and Zippy's
official repository. A high cell is no longer suppressed because a mean is low.

## E21 — personalization feature-inversion benchmark, arXiv 2510.12476

<!-- coverage-card E21 parent=2510.12476 results=2510.12476:lastde;2510.12476:lastde-plus-plus;2510.12476:log-likelihood;2510.12476:logrank;2510.12476:detect-lrr;2510.12476:fastdetectgpt -->

Table 2 compares seven GPT-J-6B-proxy scores on M4-general Cohere, ChatGPT,
Davinci, and BLOOMZ generations and on personalized Stylo-Blog and
Stylo-Literary generations from seven authors and eight newer LLMs. Samples are
at most 512 tokens. Six methods exceed 0.90 AUROC on at least one generator
aggregate: Lastde, Lastde++, Log-Likelihood, LogRank, Detect-LRR, and
FastDetectGPT. Their Cohere/ChatGPT values span 0.9312–0.9899, but personalized
cells fall as low as 0.0667–0.3978. Each row preserves both sides of that
feature-inversion boundary.

Lastde and Lastde++ generate and aggregate multiple perturbations and remain
method-excluded. Log-Likelihood is an unfrozen proxy-likelihood score. LogRank
and Detect-LRR map to the preserved DetectLLM primary paper arXiv 2306.05540;
FastDetectGPT maps to 2310.05130. These are controls rather than newer states.
The shared GPT-J proxy is plausibly within two A6000s, but no fixed calibration,
memory, throughput, or like-for-like latency is reported, and the decisive
personalized collapse makes a local speed-only screen uninformative.

## E22 — linguistic DPO attack study, arXiv 2505.24523

<!-- coverage-card E22 parent=2505.24523 results=2505.24523:mage;2505.24523:radar;2505.24523:binoculars;2505.24523:svm;2505.24523:roberta -->

Table 1 evaluates six detector columns on 45,000-document XSUM and 8,000-document
arXiv-abstract balanced tests across Llama-3.1-8B, Gemma-2-2B, and four DPO
attack variants; generation prompts allow up to 500 words. Table 2 separately
reports supervised-detector TPR at one- and five-percent FPR. Five systems cross
0.90 on at least one original or fixed-FPR slice: MAGE, RADAR, Binoculars, and
study-fitted linear-SVM and RoBERTa detectors. LLM-DetectAIve is inspected but
peaks below 0.90, so it is the explicit nonqualifying sixth column rather than a
hidden child.

MAGE's 0.997 TPR occurs only at five-percent FPR; it is 0.054 at one percent.
RADAR reaches 0.94 macro F1 and 0.932/0.995 TPR at one/five percent, then falls
to 0.324/0.571 after linguistic DPO. Binoculars reaches 0.99 only on original
XSUM/Llama and is 0.79 on original arXiv/Llama. The fitted SVM and RoBERTa reach
0.97 and 1.00 respectively on aligned cells, but the official source release
contains reconstruction code/splits rather than their immutable fitted detector
states or thresholds. The three older methods remain controls; the two custom
states are reconstruction-only. No detector timing or memory is reported. The
public study repository and parent PDF are preserved, but attack-generator LoRA
training is not confused with a detector release or with two-A6000 inference
evidence; no new screen is meaningful.

## E23 — GenAI Detection Task 1 overview, arXiv 2501.11012

<!-- coverage-card E23 parent=2501.11012 results=2501.11012:english-advacheck;2501.11012:english-unibuc-nlp;2501.11012:english-fraunhofer-sit;2501.11012:english-grape;2501.11012:english-techexperts-ipn;2501.11012:english-turquaz;2501.11012:english-szegedai;2501.11012:english-aaig;2501.11012:english-dcbu;2501.11012:english-alfa;2501.11012:english-l3i-plus-plus;2501.11012:english-luxveri;2501.11012:english-azlearning;2501.11012:english-honghanhh;2501.11012:english-baseline;2501.11012:english-vx1291;2501.11012:english-rockstart;2501.11012:multilingual-grape;2501.11012:multilingual-rockstart;2501.11012:multilingual-nota-ai;2501.11012:multilingual-luxveri;2501.11012:multilingual-baseline;2501.11012:multilingual-techexperts-ipn;2501.11012:multilingual-azlearning;2501.11012:multilingual-nampfiev1995;2501.11012:multilingual-starlight1;2501.11012:multilingual-abit7431;2501.11012:multilingual-fraunhofer-sit;2501.11012:multilingual-mail6djj;2501.11012:multilingual-saehyunma;2501.11012:multilingual-seven;2501.11012:multilingual-jojoc;2501.11012:multilingual-yaoxy;2501.11012:multilingual-bennben;2501.11012:multilingual-fangsifan;2501.11012:multilingual-yuwert777;2501.11012:multilingual-honghanhh;2501.11012:multilingual-tmarchitan;2501.11012:multilingual-sohailwaleed2 -->

Official aggregate macro F1 peaks at 0.8307 for English and 0.7916 for
multilingual detection, but Tables 8–11 expose many high domain, prompt-group,
and language cells. The repaired rule therefore expands 17 English submission
states that reach at least 0.90 on PeerReview and 22 multilingual states that
reach at least 0.90 on a domain, prompt group, or language. These are 39
track-specific rows, including both task baselines; no team is compressed into
an overview-only disposition. The rows record the corresponding official
aggregate so a 0.99–1.00 slice cannot masquerade as general accuracy.

The English analysis covers MixSet, CUDRT, IELTS, and PeerReview; the high cells
are concentrated in training-aligned PeerReview. The multilingual test has
151,425 examples across eight domains and 15 languages. Several apparent
perfect scores occur on the 1,325-example Tweet slice, while aggregate macro F1
can be close to chance. Tables 10–11 further separate original/fill-gap prompts
and seen/unseen languages. Accuracy on these unequal slices is not comparable
to a broad AUROC or a fixed low-FPR operating point. The overview describes the
RoBERTa/XLM-R baselines (2e-5 learning rate, batch 16, three epochs) but releases
neither trained baselines nor thresholds, and it supplies no universal text
limit or per-submission calibration/timing.

Official ACL primary papers are preserved for DCBU, L3i++, TechExperts,
SzegedAI, Unibuc/tmarchitan, Fraunhofer SIT, Nota AI, LuxVeri, Grape, AAIG,
TurQUaz, and Advacheck. For the remaining named submissions, the overview's
footnote explicitly says systems without descriptions did not submit a
manuscript or short description; their rows use the bounded primary-absence
sentinel and enumerate the absent checkpoint, threshold, hardware, and timing.
No paper-backed submission releases its exact trained task state with a
reusable calibration package and like-for-like latency. Some compact backbones
are plausibly within two A6000s, but absent states plus weak aggregate results
make reconstruction and a speed-only benchmark scientifically unjustified.

## E24 — Unibuc Task 1 system paper, arXiv 2501.09813

<!-- coverage-card E24 parent=2501.09813 results=2501.09813:qwen2.5-0.5b -->

The Qwen2.5-0.5B English classifier freezes all but the final layer and head,
trains about 14.9 million parameters for at most three epochs with 2,048-token
inputs, and reports validation macro F1 rising to 0.966. It also approaches 100
percent accuracy on named NLPeer test sources, but the authors warn that small
source sizes can inflate those cells; official English test macro F1 is 0.8301
and multilingual macro F1 is 0.66. The public GitHub release contains training
code/configuration rather than submitted weights or a threshold artifact.

The 0.5B capacity makes two-A6000 fit and near-Binoculars speed plausible, not
verified. With no frozen state, no independent low-FPR calibration, no broad
transfer result, and no timing, reconstructing a new state solely to reproduce
training validation would not be a scientifically meaningful bounded screen.
The primary ACL paper and public source identity remain preserved.

## E25 — linguistic-feature detector analysis, arXiv 2603.23146

<!-- coverage-card E25 parent=2603.23146 results=2603.23146:mdok-kinit;2603.23146:optimized-svc;2603.23146:optimized-xgboost;2603.23146:optimized-random-forest;2603.23146:optimized-logistic-regression;2603.23146:baseline-tfidf-svm;2603.23146:ensemble-pan;2603.23146:ensemble-coling -->

The parent disposition covers the paper's proposed linguistic-feature approach,
but its tables contain eight independently named qualifying results. Four
paper-fitted classifiers—SVC, XGBoost, Random Forest, and Logistic
Regression—report 94.09–97.97 percent accuracy, precision, recall, or F1 on the
PAN-aligned test, then fall to 67.23–76.59 percent F1 under cross-dataset
transfer. Ens-PAN averages 94.61 percent on Ghostbuster; Ens-COL averages only
87.13 percent but reaches 90.98/92.64 percent on Reuters/Essay. None of those
six exact fitted states or ensemble bundles is released.

The comparison table also names mdok of KInIT at 98.90 percent leaderboard F1
and a TF-IDF SVM baseline at 90.40 percent. mdok maps to its preserved primary
paper, arXiv 2506.01702, whose official test AUROC/F1 are only 0.853/0.898 and
whose trained 14B state is absent; this is a targeted carry-forward, not a new
promotion. The cited overview supplies no separate fitted TF-IDF baseline, so
that row records explicit primary-state absence. All eight rows preserve weak
transfer, artifact status, calibration absence, two-A6000 feasibility, and
missing timing rather than letting the parent paper stand in for them.

## E26 — linguistic-feature systematic analysis, arXiv 2606.04177

<!-- coverage-card E26 parent=2606.04177 results=2606.04177:mage-longformer -->

The explicit parent disposition covers the single proposed linear-SVM method
across its 270 fixed-domain/model fits and the TB1–TB8 testbed variants; those
are configurations of one method rather than separately named external
systems. The aggregate comparison table also names MAGE Longformer at 0.990
in-domain and 0.940 unseen-domain/model AUROC. That independently named
baseline now has its own child row mapped to the preserved MAGE primary paper
and public artifact. It remains a pre-window control and adds no new state,
calibration, or near-Binoculars timing. FastText and GLTR peak below 0.90 in
the same comparison and are documented nonqualifiers rather than hidden rows.

## Sources with no qualifying independent child

The remaining seven composite-source rows are not catch-alls. For each,
`coverage_composite_sources.tsv` records the table/section scope inspected and a
source-specific reason: reported detector-use percentages without a labeled
evaluation; maxima below 0.90 on every evaluation slice; or surveys whose high
percentages concern prior literature or a different authorship task. Low means
or official leaderboards can no longer erase a named high
domain/generator/language/length/class result. The audit rejects generic
“reviewed/no candidate” language, count-only accounting, and reclassification of
an exact-inventory parent as a no-qualifier.
