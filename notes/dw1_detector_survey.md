# DW1 accuracy-first survey of newest LLM-text detectors

Research update: 2026-08-09, America/Los_Angeles. This correction supersedes the
2026-08-07 conclusion and the already-sent incomplete summary. It changes only
the owned research artifacts; no DW1 implementation or configuration was changed.

## Answer

MELD, released in May 2026, remains the strongest actionable new scientific lead
and should have been in the earlier survey. Its paper reports dramatically better
like-for-like test-set numbers than Binoculars, and its current public checkpoint
is small, fast, and reproducible on the two NVIDIA A6000 GPUs. Those facts correct
the old claim that the bounded search found no such recent high-accuracy release.

They do **not** yet justify replacing DW1 Binoculars. The paper-era MELD checkpoint
and current runnable v5 checkpoint are materially different models, and the v5
card explicitly says their scores are incomparable. The paper-era companion code
is no longer anonymously available. On the available length-eligible DW1 screen,
v5 AUROC was 0.9553, below stored Binoculars at 0.9779 and FastDetectGPT at
0.9690. Its shipped nominal one-percent-FPR threshold produced 8.60 percent FPR
on disjoint local human rows. Local recalibration yielded promising tail recall,
but this convenience corpus and historical comparators are not a frozen
like-for-like evaluation. The artifact-version and comparability gap remains an
explicit blocker. [N9, M7]

A row-level semantic reaudit also found two plausible results previously hidden
in a mixed catch-all. LM²otifs reports stronger in-domain accuracy and AUC than
same-table Binoculars, but its cross-domain average accuracy is 0.79 versus 0.95,
its OOV path performs nearest-training-vocabulary lookup, and no runnable state or
comparable timing is public. NEULIF reports 0.9951 ROC-AUC for a 25 MB CNN, but
only on one random in-domain split of an under-specified Kaggle corpus, with no
matched Binoculars row or released model. Neither is a demonstrated qualifier.
[N13, N14]

Adversarial semantic review surfaced seven more detector papers whose strong or
superlative shared-task claims also require individual treatment. The public
mdok test AUROC is only 0.853 despite its first-place claim; four Defactify and
one M-DAIGT result are confined to their task splits without released trained
state; and the comparative neural paper's strongest rows use 60-text tests.
Three linked source repositories are preserved, but each omits a checkpoint.
None supplies matched low-FPR and timing evidence or changes the conclusion.
[N15]

A generalized second-level audit then found that publication-level dispositions
could still hide systems inside overviews, benchmarks, comparative studies, and
shared-task reports. A fresh adversarial pass then caught the same failure one
level deeper: weak means and official aggregates had suppressed named
per-dataset, generator, domain, prompt, and language cells as high as 1.00. The
final audit reviews 33 composite publications and maps 263 qualifying named
system/version results individually. The repaired Task 3 card
separates four Leidos versions, Pangram, USTC-BUPT, ALERT, and CNLP-NITS and
preserves four primary system papers plus USTC-BUPT's explicit primary-paper
absence. Three complete public checkpoints surfaced by this repair were screened.
DetectRL-X X-Rob and ModernBERT trail badly; Desklib v1.01 reaches 0.9751 AUROC
and 0.8964 TPR at a locally calibrated one-percent FPR, versus stored Binoculars
at 0.9779 and 0.6608. Desklib is fast and promising at the selected tail, but its
overall AUROC remains 0.0028 below the incumbent on a convenience corpus with
historical comparators. It is a runnable follow-up, not a replacement. [N17, M8]

A final content-derived pass removed the remaining title-selection blind spot.
It read the complete primary PDF and result tables for every one of the 119
frozen publications, not only papers already labeled as overviews or benchmarks.
The exact ledger now maps 987 reviewed detector accounts under the frozen
threshold-or-explicit-best rule: the accepted 263 embedded results and 724
separately named primary-paper configurations. No
parent-only account remains; the six papers with no qualifying result have
paper- and table-specific reasons. A fresh mutation pass caught and repaired
the first full-text inventory's remaining manual-list blind spot. In addition
to the earlier M-DAIGT, classifier-feature, DeBERTa, and Defactify recoveries,
the ledger now includes all nine Chinese encoder/LoRA states in 2509.00731,
eight SenFlow/baseline/ablation states, five semantic-similarity DeBERTa stages
in 2501.14288, both LuxVeri inverse-perplexity ensembles, ten narrow-domain TELL
comparators, five late-stage stability baselines, and the ReMoDetect and ImBD
rows in the LAPD paper. A separate PDF-table extraction then exposed the
remaining fitted-state blind spot: PAWN's RADAR-FT comparator and five-epoch M4
RoBERTa-base baseline; four distinct IntelLabs-, MAGE-, FAID-, and MIRAGE-
trained Vanilla states in the distribution-shift paper; and READ-trained versus
target-adapted ImBD states in READER. The final all-table repair also separates
the material language/training states in the Central-European benchmark, the
dataset-fitted RoBERTa, DeTeCtive, stylo, and mcgovern states in the cross-dataset
study, both M4 training-based states in the personalization benchmark, and named
comparison or ablation rows in NEULIF, DivEye, PhantomHunter, and DivScore.
The last independent-discovery repair recognizes Roman-numbered table captions,
figure legends, and every formerly zero-yield source. It adds eight unmodified
baselines from DNA-DetectLLM's Table III; ten base, DALD, and Glimpse alignment
states from the proxy-alignment paper; four zero-shot comparators from the PIFE
paper's Table VIII; and seven RAIDAR, hosted-prompt, and CAMF-backbone states
from CAMF's Table I and Figure 4. Those 29 states are now independently recovered
from the PDFs rather than seeded by the curated list. Their high narrow or
validation cells remain paired
with weak official, transfer, attack, or cross-domain evidence. Result-specific
gates now keep DNA-DetectLLM's regeneration blocker off its eight baselines and
treat DP-Net's embedding noise as training-only rather than an inference
perturbation. It also corrects Leidos v1.0.4: the primary system paper
defines it as an unweighted multiclass DistilRoBERTa classifier, not an ensemble.
The final reviewer exposed one more generalized audit gap: DMAP Table 1 put its
AUROC definition in Appendix K, so a same-page-header rule produced no candidate
for six FastDetectGPT/Binoculars scorer configurations, and only 623 of 987
accounts had a direct candidate target. The corrected scanner carries explicit
metric context across the document and resolves 4,812 independently extracted
content candidates plus 119 hash-bound source summaries. A separate 987-row
account-witness ledger then binds every account to its own PDF identity, metric,
configuration, locator, and extracted-text hash, including structured rank,
column, Roman-table, vertical-group, and figure joins. The witness ledger cannot
seed or suppress the independent unknown-row queue; both checks are required.
For arXiv 2607.03680, exact column joins now bind the two Table 4
`Vanilla + extra` states to 91.5% Unseen Domain accuracy and 88.2% Unseen
Domain+Generator accuracy, and the three Table 11 pooled states to held-out
IntelLabs AUROCs 0.968, 0.970, and 0.997. The unrelated Table 2 Anchor value
cannot satisfy any of those five accounts.
Mathematical Unicode metric labels are normalized before discovery, so Table 2
of arXiv 2505.11550 now yields direct rows for its 0.949, 0.994, and 0.974 F1
architectures instead of relying on the curated witness fallback.
None supplies the missing matched low-FPR, artifact, two-A6000, and
near-Binoculars evidence needed for promotion. [N18]

The corrected disposition is:

1. **Keep DW1 Binoculars.** No replacement has passed every fixed accuracy,
   low-false-positive, method, artifact, two-A6000 memory, and near-Binoculars
   speed gate on one frozen like-for-like evaluation.
2. **Make MELD the first candidate after provenance is resolved.** V5 passes the
   bounded memory and speed screen but not the accuracy/comparability gate. Its
   paper-era accuracy may not be attributed to v5. [N9, M7]
3. **Retain Desklib v1.01 as a runnable follow-up.** It fits and is fast on two
   A6000s, with strong locally calibrated tail recall, but narrowly misses the
   incumbent AUROC and uses a shorter 768-token path on non-frozen local data.
   [E9, M8]
4. **Retain DACTYL/Vanguard as a released supervised watchlist item.** Its PAN
   result and public ModernBERT checkpoint are credible, but it lacks a matching
   Binoculars/FastDetectGPT row, low-FPR transfer evidence, and the fixed A6000
   runtime basis. [N12]
5. **Reject LM²otifs and NEULIF individually.** Their headline values deserve
   preservation, but method, generalization, artifact, low-FPR, two-A6000, and
   timing evidence do not satisfy the fixed screen. [N13, N14]
6. **Keep every full-text detector account individually visible.** The 987-account
   ledger carries forward all 263 composite-source children and adds 724 primary-
   paper configurations. It covers all 119 papers without title, class, or
   parent-only grouping and keeps high narrow slices beside weak overall results.
   Missing state, scope, method, accuracy, or comparability blocks each
   non-control result except Desklib's follow-up status. [N15, N17, N18, E1–E26]
7. **Retain IRM as the runnable recent zero-shot control and SV-Detect as
   reconstruction-only evidence.** Their previously accepted evidence remains
   unchanged. [N2, N3, M4, M5]
8. **Keep LAPD, Exons-Detect, GTCL, and Triospect excluded.** Their attractive
   numbers cannot override the fixed multi-perturbation, regeneration, retrieval,
   and rewriting exclusions. [N1, N8, N11, M6]

This is a bounded, source-mapped conclusion—not a universal claim that no other
paper exists. The exact query exports, one mapping for every exported row, and a
semantic trigger audit are preserved in
[coverage_dispositions.md](dw1_detector_survey_sources/coverage_dispositions.md).

## Fixed deployment and comparison screen

The governing comparator is DW1's operational Binoculars: dynamic Falcon-7B and
Falcon-7B-Instruct checkpoints, one per NVIDIA RTX A6000, concurrent forwards,
batch 8, and a 2,048-token maximum. Its controlled result is 7.7325 seconds per
batch, 0.9666 seconds per document, and 35,095 MiB peak allocated on each card.
The cached revisions are `0ad33730b9d0911d6586670a661f04adaaf2c850` and
`40d43a5d6ac55026c5a471d908c9d3bf6623dbb1`. Candidate timing is accepted only
with the same scoring boundary and an explicit batch/length/hardware basis. [C3,
M1]

The canonical FastDetectGPT paper reports 233 seconds for five 500-document XSum
sets on one A100, excluding initialization. Dividing gives an inferred 0.0932
seconds per document, but the paper does not report batch size and uses different
models, hardware, data, and length. It is a scientific comparator, not a direct
DW1 speed threshold. Stored FastDetectGPT accuracy scores are used only on
identical local rows and are labeled historical. [C4, M7]

RAG, retrieval, nearest-neighbor lookup, target-text rewriting, regeneration, and
multi-perturbation pipelines remain excluded. Reported “accuracy” is never
silently substituted for AUROC, F1, or TPR at a selected FPR. Cross-paper numbers
are not ranked unless they share data, models, and protocol. Paper accuracy never
transfers merely because a different checkpoint fits the hardware.

Evidence labels are deliberate: **sourced** means a primary paper or official
artifact; **measured** means this machine; **inferred** means a bounded operational
judgment. Every bracketed ID resolves in
[source_cards.md](dw1_detector_survey_sources/source_cards.md). Raw outputs and
environment manifests sit beside the harnesses.

## MELD: strongest lead, unresolved blocker

### Paper-era accuracy

[MELD](https://arxiv.org/abs/2605.06903) is a supervised Ettin-400M encoder trained
with generator-family, attack, and domain auxiliary objectives; only its main
detector path is used at inference. On the public RAID leaderboard, the paper
reports AUROC, TPR at five-percent FPR, and TPR at one-percent FPR of
99.82/99.78/99.24 over attacks and 99.85/99.76/99.40 on clean text. The clean
Binoculars row is 84.40/78.98/69.54. MELD trains on 1.85 million RAID rows, so
this is a matching test set but not an equal training regime. [N9]

On the paper's held-out pools, MELD AUROC is 99.7/99.1/78.0/100.0/98.5/99.99
across HC3, MAGE, M4GT, Ghostbuster, DetectRL, and MELD-eval. The matching
Binoculars row is 79.4/60.7/57.3/75.4/64.8/45.2; FastDetectGPT is
99.1/57.1/65.9/92.6/73.0/70.5. On MELD-eval, overall TPR at one-percent FPR is
99.9 MELD, 95.5 ModernBERT-Detect, 17.0 FastDetectGPT, and 0.6 Binoculars. Those
four generators are held out, but the pool reuses RAID-style English domains,
human seeds, and attacks, and each detector receives a pool-specific threshold.
This is strong controlled evidence, not universal domain transfer or a fixed
deployment threshold. [N9]

### Paper-era versus current official state

The complete paper-era Hugging Face revision
`51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808` is public, ungated, MIT-licensed,
FP32, and about 1.58 GB. Its card describes a 396-million-parameter model, a
2,048-token window, and a main-head inference path, but requires companion code
at an official anonymous endpoint. That endpoint now returns HTTP 401 with
`{"error":"not_connected"}`; it was recorded and not bypassed. Reconstructing an
unpublished implementation would not be an independent reproduction. [N9]

The paper and paper-era card also disagree on 6.60 versus 6.82 million training
rows and 1.85 versus 1.91 million RAID rows. More importantly, the paper calls
the main head an MLP, while current v5 uses token-style coordinates, human
anchors, generator-family prototypes, and top-fraction aggregation. V5 release
commit `9b6379cdf62961a443d972fd27ff705ea9a07dd3` says it replaces all earlier
checkpoints. The latest immutable revision
`453acf594d48f8c55c3a38bde396f9178516d817` says plainly that earlier revisions
held different models and their scores are not comparable. [N9]

Consequently, the paper-era state is preserved but not guessed into execution;
the current state is executed but never used to validate the paper tables.

### Measured v5 feasibility

The exact self-contained v5 architecture and weights were run in FP32 under
Python 3.13, torch 2.9.1+cu126, and transformers 4.57.3. It has 394,833,461
parameters. At exactly 2,048 tokens over five repetitions:

| Mode | Median batch seconds | Seconds/document | Peak allocated MiB |
| --- | ---: | ---: | ---: |
| One GPU, batch 1 | 0.163666 | 0.163666 | 1,661.94 |
| One GPU, batch 8 | 1.200715 | 0.150089 | 2,682.95 |
| Two replicas, concurrent 4+4 | 0.626530 | 0.078316 | 2,107.07 / 2,098.52 |

The two-card batch latency is 0.0810 of the fixed 7.7325-second DW1 Binoculars
batch. Both timing blocks begin with device-resident token tensors and end with
CPU scores; model load, tokenization, and transfer are excluded. V5 therefore
comfortably passes the bounded two-A6000 memory and plausible near-Binoculars
speed screens. Its 0.0783-second measurement resembles the paper-derived
0.0932-second FastDetectGPT arithmetic estimate, but hardware, batch, length,
models, and data differ, so neither is declared faster. [M7, C4]

### Measured v5 accuracy and threshold transfer

The prior seed-42 500-human/500-generated continuity screen includes 291 texts
under v5's stated 100-word minimum. MELD AUROC is 0.9132, versus stored
Binoculars 0.9595 and FastDetectGPT 0.9536. It is retained for traceability, not
used as the main result. [M7]

The length-eligible screen uses all 4,907 available texts of at least 100 words.
One thousand human texts selected by a fixed seed form calibration only; the
disjoint evaluation contains 2,315 human and 1,592 generated texts:

| Method on identical evaluation rows | AUROC | Evaluation FPR/TPR at locally calibrated 1% FPR |
| --- | ---: | ---: |
| MELD v5 raw score | 0.955271 | 0.00821 / 0.90201 |
| Stored DW1 Binoculars, sign-normalized | 0.977899 | 0.01166 / 0.66080 |
| Stored DW1 FastDetectGPT | 0.968952 | 0.01037 / 0.75503 |

The locally selected MELD threshold has promising tail TPR, but v5 does not match
the stored comparators' overall AUROC. More seriously, v5's shipped nominal
one-percent threshold gives 9.0-percent FPR on calibration humans and 8.60 percent
on evaluation humans. Its nominal five-percent threshold gives 24.1 and 23.46
percent. Thresholds therefore do not transfer to this corpus. [M7]

The corpus is available rather than frozen and stratified, its generated examples
are not a new held-out current-generator pool, and comparator values were not
recomputed in the v5 process. These limits prevent either a positive or a final
negative deployment verdict. The defensible result is: fast and promising,
mandatory for the next evaluation, but blocked now.

## Other recent high-accuracy lanes

### Full-corpus accounts, composite sources, and public states

The generalized semantic audit treats 33 publications as composite sources in
addition to mapping all 119 export rows. Twenty-six sources contain 263
qualifying named results. Every child has a metric scope, primary source or
bounded absence sentinel, artifact status, and explicit disposition; the other
seven sources have a source-specific inspected scope and no-qualifier reason.
The machine audit binds an independent exact 263-ID inventory
and fails on a missing
child even when its mutable count is lowered, wrong parent or E-card, generic
catch-all, or missing evidence field. Its eleven regression controls include the
exact predecessor Task 3 omission, the generalized missing-result mutation, and
reclassification of a known high-cell parent as a no-qualifier, plus deletion
or misbinding of a real E-card. [N17]

That accepted composite layer is now a subset of a content-derived full-corpus
audit. Every one of the 119 primary PDFs is bound by both its PDF hash and the
hash of a reproducible full-text extraction. The resulting 987-account inventory
maps exactly to 263 accepted embedded-result dispositions and 724 primary-result
dispositions, with no parent-only target. It records six source-specific
no-qualifier outcomes. A separate full-document extractor regenerates 4,812
high-metric row-label, grouped-method, Roman-table, and figure-legend candidates
from all 119 PDFs, plus one content-hash-bound scope summary per paper, before
requiring one explicit account, carry-forward, duplicate, or content-specific
non-candidate decision for every candidate. It then regenerates exactly one
source-derived witness for every account without using those bindings to seed
the raw candidate queue. Fifty full-text controls reject ordinary-title,
non-anchor, non-English, and narrow-domain omissions even when a mutable count
is lowered; detach table content or a PDF/text hash; restore the false Leidos
mechanism; delete a fitted baseline or collapse a separately trained state while
lowering the mutable count; make an ImBD baseline inherit READER's generation
exclusion; remove any full-text source row; or remove, mutate, suppress, or
mis-target a PDF-derived candidate resolution; remove a source-scope summary;
erase the Roman or figure provenance of a required result; or leave an account
in a formerly zero-yield source without direct same-parent PDF evidence; detach
an off-page metric definition; remove any account witness; or mutate the
identity/metric sides of shared-task, column, figure, visual-plot,
below-threshold, or vertical-group joins; they also require source-independent
Unicode-F1 discovery and direct binding of the three recovered architecture
rows, derive the external README's 4,812-plus-119 total from the frozen queue,
and reject Anchor-row or neighboring-column substitutions for the five
distribution-shift accounts. They additionally require every supplied witness
to equal a fresh canonical PDF derivation, bind PAN12 recall to its declared
Table 1 column, and prevent GCN, GAT, Graph Transformer, or GPS from inheriting
Longformer's Table 2 values. Together with eleven composite controls, all
sixty-one pass. [N18]

Task 3 reports TPR at five-percent FPR on non-adversarial/adversarial RAID-derived
tests. The four Leidos rows are 99.4/97.2, 99.3/97.7, 99.2/97.6, and 99.1/95.7
percent: v1.0.3 leads the non-adversarial split, while v1.0.2 ties Pangram's
adversarial lead. Pangram is 99.3/97.7; USTC-BUPT 98.1/92.7; ALERT 91.8/82.6;
and CNLP 90.5/41.6. These are matched known-generator/domain results with
per-domain threshold searches, not DW1's frozen transferable calibration.
Leidos, Pangram, ALERT, and CNLP primary papers are preserved. The Leidos primary
paper maps v1.0.4 to MC, its unweighted multiclass DistilRoBERTa classifier; it is
not an ensemble.
USTC-BUPT has no separate paper or state after bounded public exact-team searches.
None exposes a frozen qualifying detector state. CNLP's attack-conditioned target
normalization/rewrite violates the method boundary; Pangram does not specify
whether its reported preprocessing transforms deployed inference targets, so it
is not misclassified as an inference rewrite. [E1]

The only scientifically meaningful new execution involved three complete public
checkpoints:

| State and released limit | Evaluation AUROC | Evaluation FPR/TPR at locally calibrated 1% FPR | Two-A6000 batch seconds | Decision |
| --- | ---: | ---: | ---: | --- |
| DetectRL-X X-Rob, 512 | 0.953253 | 0.00907 / 0.27136 | 0.028899 | Runnable, accuracy rejected |
| Desklib v1.01, 768 | 0.975080 | 0.00907 / 0.89636 | 0.285271 | Runnable follow-up; not a replacement |
| ModernBERT, 2,048 | 0.833729 | 0.01037 / 0.00628 | 0.300674 | Runnable, accuracy rejected |
| Stored Binoculars, historical comparator | 0.977899 | 0.01166 / 0.66080 | 7.732507 | Incumbent |
| Stored FastDetectGPT, historical comparator | 0.968952 | 0.01037 / 0.75503 | not rerun | Control |

All candidates fit comfortably on two A6000s and are plausibly near-Binoculars
speed. Their release limits differ, however, and the accuracy corpus is neither a
new frozen current-generator evaluation nor a same-process comparator run.
Desklib's strong calibrated tail recall warrants follow-up, but it does not pass
the fixed match-or-improve-over-Binoculars AUROC gate. [M8]

### Released watchlist: DACTYL/Vanguard

The PAN 2026 DACTYL system reports 0.993 AUROC and a 0.974 mean over AUROC, F1,
C@1, Brier score, and F0.5u; the latter is a composite, not accuracy. Its public
MIT-licensed ModernBERT checkpoint card reports mean AUROC 0.9475 and macro F1
0.8493 across listed out-of-distribution sets. The release is meaningful, but no
same-row Binoculars/FastDetectGPT result, low-FPR threshold transfer, 2,048-token
batch memory, or A6000 timing is available. It remains a watchlist item, not a
replacement. [N12]

### High in-domain graph result: LM²otifs

LM²otifs trains a three-layer graph convolutional network on lexical
co-occurrence/document graphs. Its supervised in-domain Table 1 reports average
accuracy/AUC of 0.98/1.00 versus 0.97/0.99 for same-table Binoculars; Table 2
reports 0.95 average accuracy versus 0.83 across eleven generator settings.
Those are genuine high claims. They do not transfer: cross-domain average
accuracy is 0.79 versus 0.95 for Binoculars and 0.97 for FastDetectGPT. [N13]

The published OOV path selects a nearest semantic neighbor from the training
vocabulary, crossing the strict no-nearest-neighbor gate. The paper used eight
40 GB A100 GPUs and gives neither input-length/batch memory nor detector-state
size. Its 0.0051–0.0091-second HC3 timing lacks a per-document versus whole-set
boundary, batch, length, and Binoculars row. No official code or checkpoint was
found. Reconstructing an unreleased graph, vocabulary, and state would not test
the paper, so no A6000 screen was run. LM²otifs is method-excluded and also fails
artifact, cross-domain, low-FPR, fit, and speed comparability. [N13]

### Lightweight in-domain claim: NEULIF

NEULIF extracts 68 spaCy/TextDescriptives features and applies a CNN or random
forest. On one random balanced split of 20,000 essays from a roughly 500,000-row
Kaggle corpus, the CNN reports 97 percent accuracy and 0.9951 ROC-AUC; the random
forest reports roughly 95 percent accuracy and 0.9555 ROC-AUC. The paper states
that these results are in-domain only. It does not identify generator families,
source domains, length distribution, or duplicate-control provenance, and its
cross-paper table has no matched Binoculars row. [N14]

The 25 MB/10.6 MB serialized-size claims make memory capacity plausible, not
reproducibility. No model, scaler, feature schema, split indices, or repository is
released. The claimed sub-100-millisecond CPU path lacks hardware, length, batch,
repetitions, and raw timing. Its nominal-threshold confusion matrix implies 2.81
percent FPR, not the fixed one-percent operating point. Training a substitute
would not validate the claim, so no A6000 screen was meaningful. [N14]

### Runnable control: IRM

IRM's best Llama-3.2-1B paper pair beats same-pair Binoculars on DetectRL
multi-domain, multi-model, and multi-attack AUROC: 97.97 versus 92.48, 97.24
versus 92.08, and 97.19 versus 93.04. It is slightly worse on human-writing
AUROC, 94.48 versus 94.63. Those Meta checkpoints require license acceptance and
were not accessed. [N2]

The strongest anonymous paper-listed family, Qwen2-0.5B, measured 1.834 seconds
per batch and 30,384 MiB per card at batch 8 and 2,048 tokens. Its fixed same-row
AUROC was 0.9436, below stored Binoculars 0.9595 and FastDetectGPT 0.9536. IRM
therefore remains a runnable control, not a demonstrated improvement. [M4]

### Reconstruction only: SV-Detect

SV-Detect reports 99.83–100 AUROC after training within corresponding
source/domain/attack settings. The public repository contains extraction and
training code but no trained steering directions or logistic-regression state.
An optimized FP16 feature reconstruction measured 1.248 seconds per batch at
2,048 tokens and under 8,849 MiB per card, but deterministic dummy directions
make its scores accuracy-free. That is cost reconstruction, not a released
end-to-end detector. [N3, M5]

### Method-excluded high numbers

LAPD's same-pair five-benchmark average is 92.37 AUROC versus 89.72 Binoculars,
and its adapted score cost was 1.0053 times the same-process Binoculars batch.
It remains excluded because standardization draws 10,000 categorical auxiliary
samples, which triggers the human's strict no-multi-perturbation boundary. [N1,
M6]

Exons-Detect reports 92.14 average AUROC versus same-table Binoculars 86.08 and
FastDetectGPT 85.07. Its essential “ideal AI sequence” mutation-repair term
constructs a replacement token sequence; removing it drops average AUROC to
87.76. It is excluded as regeneration. Its official cleaned repository also
omits the end-to-end construction and detector state. [N11]

GTCL uses k-nearest-neighbor classification over retained embeddings at
inference and is excluded as retrieval. Triospect generates summaries and
simplifications and aggregates multiple views; it is excluded as rewriting,
regeneration, and multi-view inference. Their evidence is preserved. [N8]

### Calibration and unreleased lanes

The ICLR 2026 Markov-informed layer is public code and improves within-paper
Binoculars average AUROC from 94.85 to 94.91 on Essay, 86.99 to 91.41 on Reuters,
and 73.17 to 75.49 on DetectRL. It learns a separate supervised state from labeled
generator/dataset text, ships no trained state, and has no whole-path 2,048-token
A6000 comparison. It is retained as calibration research, not a detector
replacement. [N10]

EchoPrompt reports 95.56 average AUROC versus 90.07 Binoculars with a Llama-3-8B
proxy; Steer-to-Detect reports 98.90 versus 87.70 and 0.30 versus 0.50 seconds on
one short-text A100 test. Neither released implementation or trained state was
found in the bounded public search. Their length, batch, and hardware evidence
does not prove the fixed A6000 screen. Both remain unreproduced watchlist claims.
[N4, N5]

## Normalized decision table

| Candidate | Best relevant evidence | Decisive mismatch | Disposition |
| --- | --- | --- | --- |
| MELD | Paper RAID clean 99.85 AUROC and 99.40 TPR at 1% FPR vs Binoculars 84.40/69.54; current v5 is released and fast | Paper/current states explicitly incomparable; v5 AUROC trails stored comparators; shipped thresholds fail local transfer | First blocker for a future frozen evaluation; not recommended |
| Desklib v1.01 | Public state; local 0.9751 AUROC and 0.8964 TPR at locally calibrated 1% FPR; 0.2853-second two-card batch | AUROC narrowly trails stored Binoculars 0.9779; 768-token RAID-trained path; convenience corpus and historical comparator | Runnable follow-up; not recommended |
| DetectRL-X X-Rob | Public state; 0.0289-second two-card batch | Local 0.9533 AUROC and only 0.2714 TPR at calibrated 1% FPR | Accuracy rejected |
| Model-collapse ModernBERT | Public state; 2,048-token 0.3007-second two-card batch | Local 0.8337 AUROC and 0.0063 TPR at calibrated 1% FPR | Accuracy rejected |
| DACTYL/Vanguard | Released ModernBERT; PAN AUROC 0.993 | Supervised challenge result; no matched Binoculars, low-FPR, length, memory, or speed row | Released watchlist |
| LM²otifs | In-domain 0.98 accuracy/1.00 AUC vs same-table Binoculars 0.97/0.99 | Cross-domain 0.79 vs 0.95; nearest-neighbor fallback; no state or comparable cost | Excluded/rejected |
| NEULIF | In-domain CNN 97% accuracy and 0.9951 ROC-AUC; reported 25 MB | One under-specified corpus split; no matched comparator, state, low-FPR, or reproducible timing | Unreleased in-domain claim |
| 987 full-text detector accounts | Up to 1.0 on reported F1, accuracy, precision, TPR, or AUROC slices; exact source/artifact disposition for 263 embedded results and 724 primary configurations | Narrow, validation-only, shifted, language-specific, closed, missing-state, excluded-method, or weaker mean/overall result except Desklib follow-up | Individually accounted across all 119 papers; no parent-only grouping or hidden promotion |
| IRM | Best paper pair beats matched Binoculars on three DetectRL AUROCs | Best pair gated; anonymous public pair trails stored Binoculars locally | Runnable control |
| SV-Detect | 99.83–100 matched-family reported AUROC | No trained detector state; supervised setting; local run is reconstruction only | Reconstruction evidence |
| LAPD | 92.37 average vs same-pair Binoculars 89.72; measured near-identical cost | 10,000 auxiliary categorical samples | Excluded by method |
| Exons-Detect | 92.14 average vs same-table Binoculars 86.08 | Essential generated ideal-sequence stage; incomplete cleaned release | Excluded by method |
| Markov calibration | Improves Binoculars on three within-paper datasets | Per-dataset supervised state not shipped; no whole-path fixed screen | Calibration research |
| EchoPrompt / Steer-to-Detect | Strong same-paper reported comparisons | No public implementation or state; incomplete deployment basis | Unreleased watchlist |

AUROC is threshold-free ranking quality, not classification accuracy. F1, raw
accuracy, TPR at one-percent FPR, TPR at 0.01-percent FPR, and composite challenge
scores are not interchangeable. The table preserves like-for-like comparisons
within each source and does not rank numbers across different rows.

## Coverage, preservation, and uncertainty

The frozen evidence includes three raw date-sorted arXiv query exports, a targeted
Markov export, 119 deduplicated 2025–2026 publication mappings, a generated
semantic audit, 33 accepted composite-source reviews, 263 generated child-result
audit rows, a complete 119-PDF full-text/table/figure review, 724 primary-configuration
dispositions, a 987-account exact mapping, and anonymous public
Google Scholar first-page evidence. The first layer
mechanically flagged 106 titles/abstracts for performance language or metrics;
every flag has an explicit disposition or documented false-positive reason. The
second layer rejects missing named results and generic composite-source reasons.
The final layer removes title/class selection entirely, rehashes every preserved
PDF and extracted text, requires a scope summary for every source, and requires
every expected account to resolve exactly once with a source-derived witness.
Sixty-one regression and negative controls cover selected composites,
ordinary-title primary papers, Roman-numbered tables, figure legends, former
zero-yield sources, Unicode metric labels, exact metric-column ownership,
mechanical external-README counts, and structured per-account joins.
A prior Scholar attempt returned a robot challenge and was not bypassed; fresh
narrow requests returned HTTP 200. The general web-search connector returned HTTP
404, so direct anonymous primary endpoints were used. No PB, authenticated state,
browser profile, persistent session, cookie reuse, robot bypass, or human-owned
tmux session was used.

All new papers, immutable MELD and composite-detector snapshots, official source
archives, public API metadata, raw HTTP evidence, and queries live in the
discoverable external collection documented by
[paper_artifacts.md](dw1_detector_survey_sources/paper_artifacts.md). Its full
integrity ledger is preserved. The repository keeps both benchmark sources, raw
successful and failed stdout/stderr, score-level CSVs, independent verifiers,
package/interpreter/GPU manifests, and exact model-file hashes.

Local timings remain bounded feasibility checks, not sustained production load.
CUDA peak allocation is not total process memory. Existing comparison scores come
from a convenience corpus and can differ in software/truncation. Paper benchmark
reuse, supervised training, and unknown pretraining overlap remain contamination
risks rather than assumed facts. These limitations are why MELD remains a blocker
instead of being promoted from attractive numbers.

## Future gate

Do not replace Binoculars yet. Resolve which runnable state produced the MELD
paper tables, then freeze a new stratified evaluation with current generators and
attacks, separate human calibration, and per-generator, domain, language, date,
and length-band results. Recompute MELD, Desklib, Binoculars, and FastDetectGPT in
the same software process and timing boundary.

A candidate advances only if it matches or improves Binoculars AUROC and the
chosen low-false-positive operating point on identical held-out rows, keeps the
two-A6000 2,048-token batch-8 fit, and remains plausibly near the fixed Binoculars
latency without entering an excluded method family. Until then, MELD is the
mandatory provenance blocker and Desklib is the strongest newly measured
secondary follow-up—not a deployable conclusion.
