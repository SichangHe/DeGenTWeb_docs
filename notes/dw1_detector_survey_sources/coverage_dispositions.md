# Bounded 2025–2026 coverage and result dispositions

Search frozen: 2026-08-08, America/Los_Angeles.

## Reproducible search boundary

Three anonymous arXiv API queries requested 100 results each, sorted by submitted
date descending:

- `all:"AI-generated text detection"`: 93 results;
- `all:"LLM-generated text detection"`: 40 results; and
- `all:"machine-generated text detection"`: 71 results.

The raw Atom responses are preserved as
`coverage_query_ai_generated.atom`, `coverage_query_llm_generated.atom`, and
`coverage_query_machine_generated.atom`. Their SHA-256 values are respectively
`0b9dead4e200076f560eee47422a2d24c0a338e7c95d6e92503050e1d5e9d3e9`,
`dbc0e01e6f859b7b59b40c982ed1f8667b98e6f387c8d4f93c8ccc6a692cb8dc`, and
`6da5b39f5ff7bac05c1c2ecee0bb982a4b7928c23e1850a5c0019328a6787e7d`.
Deduplicating arXiv identifiers and retaining submission years 2025–2026 yields
119 rows. A targeted Markov query is also preserved because the evaluator named
that omission.

“Plausible high-accuracy result” means a 2025–2026 work proposing a reusable
general document detector or calibration layer whose public title, abstract, or
paper claims strong/SOTA performance, an improvement over major baselines, or a
metric of at least 0.90. Special-language, code-only, span-only, hybrid-authorship,
dataset-only, attack-only, survey, and source-plagiarism work is not silently
dropped: those rows are accounted for after the priority table. This is a bounded
screen of these exact exports, not a claim that all possible papers were found.

## Every plausible high-accuracy result returned

This table is date-sorted. “Retain” means preserve the evidence, not recommend the
method. Each reason maps to the linked primary paper; artifact-specific claims map
to `source_cards.md` and `paper_artifacts.md`.

| Date | Result | One-line disposition |
| --- | --- | --- |
| 2026-08-02 | [DeBERTa-Sentinel, 2608.01046](https://arxiv.org/abs/2608.01046) | Retain/reject: 99.53 ROC-AUC is one GLC random split; official source has no released checkpoint or cross-distribution Binoculars comparison. [N8] |
| 2026-07-24 | [DWT-Fusion, 2607.22026](https://arxiv.org/abs/2607.22026) | Retain/reject: training-free but its M4/MAGE rows trail stronger candidates, with no official detector state or two-A6000 comparison. [N8] |
| 2026-07-19 | [DACTYL/Vanguard, 2607.17382](https://arxiv.org/abs/2607.17382) | Retain watchlist: a public ModernBERT checkpoint and 0.993 PAN AUROC are real, but there is no same-row Binoculars, low-FPR transfer, 2,048-token memory, or A6000 timing. [N12] |
| 2026-07-16 | [Latent Trajectory/GTCL, 2607.14967](https://arxiv.org/abs/2607.14967) | Exclude: official inference is k-nearest-neighbor classification over retained representations, violating the no-retrieval gate. [N8] |
| 2026-07-04 | [Strong baseline under shift, 2607.03680](https://arxiv.org/abs/2607.03680) | Retain/reject: important evidence that a RoBERTa baseline can look strong in distribution, but it does not establish released low-FPR parity under the fixed DW1 screen. [N8] |
| 2026-06-30 | [Triospect, 2606.31074](https://arxiv.org/abs/2606.31074) | Exclude: it generates summaries and simplifications and aggregates multiple transformed views, violating rewrite/regeneration and multi-view constraints. [N8] |
| 2026-06-22 | [WaveDetect, 2606.23336](https://arxiv.org/abs/2606.23336) | Retain/reject: the released checkpoint is fast, but measured same-row AUROC 0.8906 trails Binoculars 0.9595. [M2] |
| 2026-06-05 | [SV-Detect, 2606.07313](https://arxiv.org/abs/2606.07313) | Retain reconstruction only: near-perfect matched-family rows are supervised and the release omits trained steering directions and classifier state. [N3, M5] |
| 2026-06-02 | [Linguistic-feature SVM, 2606.04177](https://arxiv.org/abs/2606.04177) | Retain/reject: AUROC is 0.968 in-domain and 0.907–0.945 on held-out settings, but macro F1 ranges from 0.588 to 0.827 and no fitted state, fixed-FPR result, or comparable timing is public. [N16] |
| 2026-06-01 | [Uncertainty++, 2606.02158](https://arxiv.org/abs/2606.02158) | Retain/reject: public code and strong AUROC exist, but no like-for-like Binoculars row or complete length/batch speed basis establishes parity. [N7] |
| 2026-05-29 | [Distribution-free rewrite calibration, 2606.00402](https://arxiv.org/abs/2606.00402) | Exclude: it expressly converts rewrite-based detectors, outside the fixed no-rewriting boundary. |
| 2026-05-27 | [Show, Don't TELL, 2605.27921](https://arxiv.org/abs/2605.27921) | Retain/reject: supervised explanation-generating detector reports 0.927 AUROC, below the requested accuracy lead and without the fixed speed evidence. |
| 2026-05-24 | [READER, 2605.25281](https://arxiv.org/abs/2605.25281) | Exclude: its 1.5B model autoregressively reasons before detection, making generation part of inference; no fixed DW1 comparator is supplied. |
| 2026-05-15 | [Multi-Level Contextual Detection, 2605.16107](https://arxiv.org/abs/2605.16107) | Retain/reject: only supplementary material was released; no runnable detector state supports the reported gains. [N8] |
| 2026-05-07 | [MELD, 2605.06903](https://arxiv.org/abs/2605.06903) | Advance as blocker, not recommendation: strongest paper claims and runnable v5 are preserved and tested, but the paper-era and v5 models are incomparable, v5 trails stored comparators in AUROC, and shipped thresholds fail to transfer. [N9, M7] |
| 2026-05-04 | [Fight Poison with Poison, 2605.02374](https://arxiv.org/abs/2605.02374) | Retain/reject: few-shot adversarial training is not a released general detector with a like-for-like Binoculars and two-A6000 result. |
| 2026-04-28 | [Luminol-AIDetect, 2604.25860](https://arxiv.org/abs/2604.25860) | Exclude: detection depends on randomized target-text shuffling and ensemble features, crossing the strict multi-perturbation boundary. |
| 2026-04-23 | [IRM, 2604.21223](https://arxiv.org/abs/2604.21223) | Retain runnable control: best paper pair is gated; the strongest anonymous pair measured 0.9436 AUROC versus stored Binoculars 0.9595. [N2, M4] |
| 2026-04-18 | [LAPD, 2604.16923](https://arxiv.org/abs/2604.16923) | Exclude: strong matched zero-shot comparison and near-Binoculars measured cost are preserved, but 10,000 categorical auxiliary samples trigger the strict multi-perturbation gate. [N1, M6] |
| 2026-04-13 | [AEyeDE, 2606.00016](https://arxiv.org/abs/2606.00016) | Retain/reject: attention attribution claims do not include a released state or fixed low-FPR, 2,048-token A6000 comparison. |
| 2026-04-02 | [kNNProxy, 2604.02008](https://arxiv.org/abs/2604.02008) | Exclude: the defining proxy alignment uses k-nearest-neighbor lookup, violating retrieval. |
| 2026-03-26 | [Exons-Detect, 2603.24981](https://arxiv.org/abs/2603.24981) | Exclude: its 92.14 average AUROC beats same-table Binoculars 86.08, but an essential generated ideal-sequence mutation-repair term violates regeneration; the release is not end-to-end. [N11] |
| 2026-03-24 | [Explainable linguistic-feature detector, 2603.23146](https://arxiv.org/abs/2603.23146) | Retain/reject: 0.9734 in-domain F1 degrades under cross-domain and cross-generator shift; no fixed Binoculars, low-FPR, or A6000 result establishes parity. |
| 2026-03-19 | [Comparative neural detectors, 2603.18750](https://arxiv.org/abs/2603.18750) | Retain/reject: the strongest proposed-model rows are 91.67 percent on a 60-text English test and 98.3 percent on a 60-text thematic test; public notebooks ship no checkpoint, and no matched low-FPR or timing evidence establishes parity. [N15] |
| 2026-03-05 | [NOTAI.AI, 2603.05617](https://arxiv.org/abs/2603.05617) | Retain/reject: a FastDetectGPT-derived explanatory ensemble, but no public frozen state and like-for-like DW1 low-FPR/speed evidence were found in the bounded check. |
| 2026-02-17 | [DependencyAI, 2602.15514](https://arxiv.org/abs/2602.15514) | Retain/reject: competitive syntactic results include cross-domain overprediction and expose no fixed metric, public detector state, or A6000 comparator in the export. |
| 2026-02-08 | [Markov-informed calibration, 2602.08031](https://arxiv.org/abs/2602.08031) | Retain released calibration: official code exists, but per-dataset supervised states are not shipped and its Binoculars gains do not establish a qualifying detector or whole-path speed. [N10] |
| 2026-02-01 | [Prototype-based proxy routing, 2602.01240](https://arxiv.org/abs/2602.01240) | Retain/reject: routing among proxies adds artifact/training requirements and lacks a released fixed DW1 parity and two-A6000 result. |
| 2026-01-27 | [Variation/VaryBalance, 2602.13226](https://arxiv.org/abs/2602.13226) | Exclude: the claimed gain over Binoculars depends on LLM rewrites of the target text. |
| 2026-01-27 | [LLM-specific fine-tuning, 2601.20006](https://arxiv.org/abs/2601.20006) | Retain/reject: 99.6 percent is token-level accuracy on the authors' benchmark, not document AUROC or low-FPR parity; no fixed deployment state is established. |
| 2026-01-08 | [Late-stage stability, 2601.04833](https://arxiv.org/abs/2601.04833) | Retain/reject: no like-for-like Binoculars accuracy and fixed A6000 speed evidence supports promotion. [N8] |
| 2026-01-08 | [DP-MGTD, 2601.04641](https://arxiv.org/abs/2601.04641) | Exclude: near-perfect accuracy follows differentially private entity sanitization of the target text, outside the no-perturbation screen. |
| 2026-01-07 | [AI Generated Text Detection, 2601.03812](https://arxiv.org/abs/2601.03812) | Retain/reject: DistilBERT reports 0.96 ROC-AUC but 88.11 percent accuracy and no released state, low-FPR row, or fixed speed result. |
| 2025-11-22 | [NEULIF, 2511.21744](https://arxiv.org/abs/2511.21744) | Retain/reject: 0.9951 ROC-AUC is one balanced in-domain Kaggle split; no matched Binoculars row, frozen model, cross-domain test, or comparable timing artifact exists. [N14] |
| 2025-11-03 | [DEER, 2511.01192](https://arxiv.org/abs/2511.01192) | Retain/reject: supervised mixture-of-experts claims generalization, but no released deployment state and fixed comparator evidence establish DW1 parity. [N8] |
| 2025-11-02 | [Easy-to-hard supervision, 2511.00988](https://arxiv.org/abs/2511.00988) | Retain/reject: broad effectiveness is claimed without a threshold metric, fixed released state, or like-for-like Binoculars and A6000 comparison in the export. |
| 2025-10-14 | [StyleDecipher, 2510.12608](https://arxiv.org/abs/2510.12608) | Retain/reject: supervised stylistic performance lacks a runnable frozen state and like-for-like low-FPR/A6000 evidence. |
| 2025-09-26 | [Mixture of Detectors, 2509.22147](https://arxiv.org/abs/2509.22147) | Retain/reject: ensemble claims do not provide the fixed public state, comparator, and latency basis required here. |
| 2025-09-23 | [Diversity Boosts Detection, 2509.18880](https://arxiv.org/abs/2509.18880) | Retain/reject: training-data diversity gains do not establish a released detector that beats Binoculars on the same held-out rows. |
| 2025-09-22 | [PIFE, 2510.02319](https://arxiv.org/abs/2510.02319) | Exclude: inference transforms the target through multi-stage normalization and scores the rewrite discrepancy. |
| 2025-09-19 | [DNA-DetectLLM, 2509.15550](https://arxiv.org/abs/2509.15550) | Exclude: SOTA gains require iterative construction of an ideal AI sequence, violating no regeneration. |
| 2025-09-15 | [DetectAnyLLM, 2509.14268](https://arxiv.org/abs/2509.14268) | Exclude: Reference Clustering performs nearest-reference lookup over retained human/generated sets. [X2] |
| 2025-09-02 | [MoSEs, 2509.02499](https://arxiv.org/abs/2509.02499) | Exclude: inference activates examples from a Stylistics Reference Repository for conditional thresholds, crossing the no-retrieval gate. |
| 2025-08-30 | [Multi-Strategy/M-DAIGT, 2509.00623](https://arxiv.org/abs/2509.00623) | Retain/reject: near-perfect RoBERTa scores are confined to news and academic-abstract task sets; no public trained state, cross-distribution result, low-FPR evidence, or fixed deployment basis is released. [N15] |
| 2025-08-19 | [MGT-Prism, 2508.13768](https://arxiv.org/abs/2508.13768) | Retain/reject: supervised spectral-alignment results lack a public frozen state and same-row low-FPR, length, and speed comparison. |
| 2025-08-16 | [CAMF, 2508.11933](https://arxiv.org/abs/2508.11933) | Retain/reject: a multi-LLM-agent inference pipeline has no public fixed state or plausible near-Binoculars timing basis. |
| 2025-08-15 | [SpecDetect, 2508.11343](https://arxiv.org/abs/2508.11343) | Retain/reject: formula is fast but the public artifact is incomplete and published accuracy does not establish Binoculars parity under DW1. [S1, S2] |
| 2025-08-09 | [SentiDetect, 2508.06913](https://arxiv.org/abs/2508.06913) | Exclude: reported F1 gains depend on sentiment-altering and semantic-preserving target transformations, violating the multi-perturbation screen. |
| 2025-08-03 | [Temporal Tomography, 2508.01754](https://arxiv.org/abs/2508.01754) | Retain/reject: theoretical temporal signal lacks a released qualifying state and matched low-FPR/A6000 comparison. |
| 2025-07-31 | [T-Detect, 2507.23577](https://arxiv.org/abs/2507.23577) | Retain/reject: tail normalization targets attacks but has no released fixed state or complete like-for-like Binoculars and A6000 result. |
| 2025-07-07 | [Instruction fine-tuned detectors, 2507.05157](https://arxiv.org/abs/2507.05157) | Retain/reject: the 0.9547 Task-A result is one Defactify fine-tune, including a closed hosted GPT-4o-mini state, with no public detector, low-FPR result, or fixed deployment comparison. [N15] |
| 2025-06-18 | [PhantomHunter, 2506.15683](https://arxiv.org/abs/2506.15683) | Retain/reject: several probability extractors, no released detector state, and insufficient speed evidence. [N8] |
| 2025-06-07 | [DivScore, 2506.06705](https://arxiv.org/abs/2506.06705) | Reject for scope: specialized legal/medical domain distillation is not a general DW1 replacement. [N8] |
| 2025-06-02 | [mdok, 2506.01702](https://arxiv.org/abs/2506.01702) | Retain/reject: despite first place, official test AUROC/F1 are 0.853/0.898; public source ships no trained 14B state, inference timing, low-FPR row, or fixed A6000 comparison. [N15] |
| 2025-05-21 | [AGENT-X, 2505.15261](https://arxiv.org/abs/2505.15261) | Retain/reject: multiple reasoning LLM agents provide no plausible near-Binoculars latency or fixed public deployment artifact. |
| 2025-05-20 | [FAID, 2505.14271](https://arxiv.org/abs/2505.14271) | Reject for scope: fine-grained multilingual academic/hybrid attribution is not the fixed binary general-document task. |
| 2025-05-20 | [Domain Gating Ensemble, 2505.13855](https://arxiv.org/abs/2505.13855) | Retain/reject: supervised ensemble results lack a released state and like-for-like operating-point/speed evidence. |
| 2025-05-18 | [LM²otifs, 2505.12507](https://arxiv.org/abs/2505.12507) | Exclude/reject: in-domain rows beat same-table Binoculars, but cross-domain accuracy trails it; a nearest-training-vocabulary lookup violates the strict method gate, and no released state, comparable timing, or two-A6000 basis exists. [N13] |
| 2025-05-15 | [Multifaceted Defactify detector, 2505.11550](https://arxiv.org/abs/2505.11550) | Retain/reject: 0.994 F1 is fifth place on one binary task; the multi-encoder system has no public trained state, cross-distribution, low-FPR, or speed basis. [N15] |
| 2025-05-08 | [Multiscaled Conformal Prediction, 2505.05084](https://arxiv.org/abs/2505.05084) | Retain calibration watchlist: controls FPR on RealDet calibration, but does not ship a DW1 calibration state or establish a whole-detector A6000 comparison. |
| 2025-04-22 | [Dynamic perturbations, 2504.21019](https://arxiv.org/abs/2504.21019) | Exclude: target-text dynamic perturbations violate the fixed multi-perturbation constraint. |
| 2025-04-15 | [OpenTuringBench/OTBDetector, 2504.11369](https://arxiv.org/abs/2504.11369) | Retain/reject: seven systems exceed 0.90 F1 on both designated unseen-model columns, but their individual rows expose no new frozen state with a broad low-FPR and fixed deployment comparison. [E16] |
| 2025-04-01 | [Short-PHD, 2504.02873](https://arxiv.org/abs/2504.02873) | Exclude: the detector inserts off-topic content into the target, violating the no-rewriting/perturbation gate. |
| 2025-03-28 | [SKDU/Defactify, 2503.22338](https://arxiv.org/abs/2503.22338) | Retain/reject: the allowed NELA-XGBoost branch reports 0.9945 Task-A F1, but public feature code ships no trained state and no cross-distribution, low-FPR, Binoculars, or timing comparison. [N15] |
| 2025-02-24 | [Sarang/Defactify, 2502.16857](https://arxiv.org/abs/2502.16857) | Retain/reject: perfect Task-A F1 comes from one shared-task split and a DeBERTa ensemble, without a public trained state, cross-distribution, low-FPR, or fixed deployment result. [N15] |
| 2025-02-18 | [GREATER, 2502.12734](https://arxiv.org/abs/2502.12734) | Retain/reject: 0.67 percent is attack-success reduction, not absolute accuracy; no fixed Binoculars, released state, or A6000 result is supplied. |
| 2025-02-17 | [ExaGPT, 2502.11336](https://arxiv.org/abs/2502.11336) | Exclude: example-based inference is a retrieval lane. |
| 2025-02-06 | [Group-adaptive thresholds, 2502.04528](https://arxiv.org/abs/2502.04528) | Retain/reject: a threshold-optimization study, not a released detector demonstrating fixed DW1 accuracy and speed. |
| 2025-01-07 | [PAWN, 2501.03940](https://arxiv.org/abs/2501.03940) | Retain/reject: released supervised detector remains below the accuracy-first qualifying evidence and lacks the fixed full deployment comparison. [P1] |

### Plausible targeted carry-forward outside the three exact-phrase exports

Exact-title and citation-following checks from the accepted earlier search are
kept alongside the export-derived set. Three plausible high-accuracy papers were
not members of the 119-row exact-phrase union:

| Date | Result | One-line disposition |
| --- | --- | --- |
| 2026-08-06 | [EchoPrompt, 2608.05741](https://arxiv.org/abs/2608.05741) | Retain unreleased watchlist: paper reports 95.56 average AUROC versus same-proxy Binoculars 90.07, but no public code/state and no complete batch/length/hardware timing basis were found. [N4] |
| 2026-05-22 | [Hidden Human-Like Nature, 2605.23190](https://arxiv.org/abs/2605.23190) | Retain/reject: targeted citation-following evidence lacks a released, frozen detector state and a complete same-run A6000/Binoculars basis. [N8] |
| 2026-05-13 | [Steer-to-Detect, 2605.12890](https://arxiv.org/abs/2605.12890) | Retain unreleased watchlist: paper reports 98.90 AUROC versus Binoculars 87.70 on one short-text A100 test, but no public state and no 2,048-token batch-8 A6000 fit. [N5] |

## Composite-source result expansion

Publication-level accounting is not sufficient for an overview, benchmark,
comparative study, evaluation, or shared-task paper. The generalized audit marks
33 such frozen export rows. Twenty-six contain 263 qualifying named system/version
results; every result now has its own metric scope, primary source or bounded
absence sentinel, artifact status, and explicit disposition in
`coverage_embedded_results.tsv`. The other seven composite sources record the exact
tables or sections inspected and a source-specific no-qualifier
reason in `coverage_composite_sources.tsv`. Full evidence cards are in
`coverage_composite_dispositions.md` [N17].

The Task 3 overview at arXiv 2501.08913 is no longer a benchmark catch-all.
Twenty rows separate every qualifying submitted version and official baseline.
Primary system PDFs are preserved for Leidos, Pangram, ALERT, CNLP, LuxVeri,
and MOSAIC. USTC-BUPT's rows document the bounded absence of a separate primary
paper or public state. Pangram is retained/rejected as closed because its
preprocessing section does not specify the deployed inference path; CNLP remains
excluded because its inference pipeline rewrites or normalizes the target. The Counter Turing
overview likewise expands all eight qualifying Task-A systems, including three
explicit primary-paper absences. [E1, E2]

Three complete public states exposed by composite sources received the same
bounded screen. DetectRL-X X-Rob measured 0.9533 evaluation AUROC and 0.2714 TPR
at a locally calibrated one-percent FPR. ModernBERT measured 0.8337 and 0.0063.
Desklib measured 0.9751 and 0.8964, versus stored Binoculars 0.9779 and 0.6608;
its overall AUROC remains 0.0028 lower. All three easily fit two A6000s and are
much faster than the fixed Binoculars batch, but no state passes every accuracy
and comparability gate. Desklib remains a runnable follow-up, not a replacement.
[E3, E9, E18, M8]

## Full-corpus account expansion

The final audit removes the composite selector from discovery. It reads the
complete primary PDF and every main/appendix result table for all 119 export
publications. `coverage_fulltext_sources.tsv` binds each paper's PDF hash and the
hash of its exact `pdftotext -layout -enc UTF-8` extraction.

`coverage_fulltext_expected_accounts.tsv` contains 987 exact detector accounts:
the accepted 263 embedded results and 724 separately named primary-paper
configurations. No parent-only account remains. Each maps exactly once in
`coverage_fulltext_account_map.tsv`; the 724 configuration dispositions are in
`coverage_primary_results.tsv`. Six papers have source-specific, table-derived
full-text no-qualifier reasons. The generated 987-row resolution is
`coverage_fulltext_account_audit.tsv`. [N18]

This content pass recovers all three M-DAIGT systems from 2509.00623, all nine
classifier-by-feature states in 2503.22338, all eight original/noised/double/
ensemble DeBERTa states in 2502.16857, and all three Defactify systems in
2507.05157. Content anchors require both their exact IDs and their names/high
values in the hash-bound extraction. Six new controls reject an ordinary-title
omission with a lowered count, an analogous non-anchor omission, PDF/text
detachment, the former false Leidos mechanism, and removal of any one of the 119
source reviews. None of the recovered configurations passes the full accuracy,
low-FPR, artifact, two-A6000, and near-Binoculars gate.

The final fitted-state pass separates PAWN's RADAR-FT comparator and the
authors' five-epoch M4 RoBERTa-base baseline; four IntelLabs-, MAGE-, FAID-, and
MIRAGE-trained Vanilla states in 2607.03680; and READ-trained versus
target-adapted ImBD in READER. A separate PDF-content extractor freezes 4,812
high-metric row-label, grouped-method, Roman-table, and figure-legend candidates
from all 119 papers, plus one hash-bound source-scope summary per paper, before
matching them to the curated inventory. It separately emits exactly one
source-derived account witness for all 987 accounts; these bindings do not seed
or suppress the independent raw-candidate queue. Its content-derived controls reject deletion of the M4
baseline, collapse of a trained Vanilla state, and false inheritance of
READER's generation exclusion by ImBD. These eight explicit states add seven
net accounts and none passes the complete deployment screen. Mathematical
Unicode metric labels are normalized before extraction; arXiv 2505.11550's
three Table 2 architectures therefore have direct row candidates and witnesses
rather than inventory-only fallback evidence. [N18]
For arXiv 2607.03680, Table 4 now binds `Vanilla + extra` separately to 91.5%
Unseen Domain and 88.2% Unseen Domain+Generator accuracy; Table 11 binds the
three held-out IntelLabs pooled configurations to 0.968/0.970/0.997 AUROC.
Structured controls reject the unrelated Anchor/Table 2 metric and neighboring
column substitutions. The external README total is also derived from the frozen
4,812 candidates plus 119 summaries rather than copied by hand. [N18]

A fresh full-corpus mutation review then found that the first primary list still
left some inspected non-candidate papers at zero. The exact repair adds all nine
Chinese encoder/LoRA states in 2509.00731, eight SenFlow-related states, five
semantic-similarity DeBERTa stages in 2501.14288, both LuxVeri ensembles, and
every other qualifying row recovered from the former zero/parent partition.
The final table pass also adds ten narrow-domain TELL comparators, five
late-stage stability baselines, and ReMoDetect and ImBD from the LAPD comparison.
The LAPD-paper rows are mechanism-specific: its baselines, RAI, and S score are
evidence-rejected, DNA-DetectLLM is regeneration-excluded, and only the actual
LAPD pair states inherit the auxiliary-sampling exclusion.
The 2509.15550 rows now apply regeneration only to actual DNA-DetectLLM states;
DetectGPT is separately multi-perturbation-excluded and the other seven
baselines are evidence-rejected. DP-Net 2504.21019 is also evidence-rejected
because its noise is training-only, not an inference perturbation.
The first twenty full-text controls include non-English and narrow-domain
lowered-count omissions and content detachment from both positive inventories
and a table-derived zero decision, fitted-baseline deletion, collapsed training
state, plus three false-inheritance controls for parent method blockers.

The final discovery repair adds 29 evaluator-confirmed states that were hidden
behind Roman-numbered table captions or Figure 4: eight unmodified baselines in
2605.16107, ten base/DALD/Glimpse alignment states in 2604.02008, four zero-shot
comparators in 2510.02319, and seven RAIDAR/hosted-prompt/CAMF states in
2508.11933. Each has exact strong and weak evidence, mechanism, artifact,
method-boundary, two-A6000, and timing treatment. The scanner also requires a
scope summary for all 119 PDFs and direct same-parent evidence for every account
under each predecessor zero-yield source. Four added mutations exercise those
source, Roman-caption, figure-legend, and direct-evidence requirements. The
generalized 987-row witness ledger then binds every account to one same-parent
identity/metric witness, including rank, column, figure, visual-plot,
below-threshold, and vertical-group joins; mutation controls reject removal or
misbinding of each new evidence form.

## Accounting for every export row

The former catch-all buckets are superseded. `coverage_row_dispositions.tsv`
contains exactly one reviewed source-mapped row for each of the 119 deduplicated
export identifiers. `audit_coverage.py` independently parses the three immutable
exports, rejects conflicting or duplicate mappings, and flags title or abstract
text containing SOTA, best, comparative or high-performance claims, named
metrics, or explicit percentages of at least 90.

The generated `coverage_semantic_audit.tsv` preserves the title, contributing
exports, every matched text fragment, mapping kind, allowlisted class definition,
resolution, reason, and primary arXiv URL for every row. The frozen run found 106
semantic flags. All 70 plausible or method-excluded publication rows have
explicit dispositions; the other 49 rows have mechanically allowlisted
non-candidate classes and specific reasons. Every flag in those 49 rows is
resolved as a documented false positive, such as a metric belonging to a
source-plagiarism task, an attack, a dataset-only contribution, or a
special-language task outside the fixed deployment scope.

The second audit layer validates all 33 composite reviews and all 263 embedded
results: 26 sources expand and seven have result-specific no-qualifier reasons.
It rejects a missing child, wrong parent, count mismatch, absent primary
source/absence sentinel, absent artifact status, unknown disposition, or generic
no-qualifier explanation. Eleven regression and negative controls include the
predecessor Task 3 omission, a one-child CNLP omission, and removal or parent/
result misbinding of a real Markdown E-card. Unknown, wrong-kind, and catch-all
codes fail validation at both levels.

The final audit layer validates all 119 full-text source records and all 987
accounts, independent of title or parent class. It requires the immutable exact
account set, one disposition target per account, all 119 PDF and text hashes,
one source-scope record per PDF, and one same-parent source-derived witness per
account, with content-derived anchors for evaluator counterexamples and
no-account decisions. Together the two result-level layers run sixty-one
regression and negative controls; no
identifier-only or publication-only group remains.

`coverage_semantic_audit_report.txt` preserves the exact project-neutral command,
input/output hashes, raw and deduplicated counts, mapping counts, and PASS.
`coverage_embedded_result_audit.tsv` preserves the generated child mapping, and
`coverage_fulltext_account_audit.tsv` preserves the complete account mapping.
`coverage_semantic_audit_environment.txt` preserves the Python and platform
environment; `coverage_semantic_audit_design.md` fixes the control flow and
failure conditions. The raw Atom exports remain the canonical publication data,
while the reviewed mappings and generated audits make both levels of semantic
accounting testable.

## Public Google Scholar check

One fresh anonymous request queried the first date-sorted page for
`"AI-generated text detection"`, years 2025–2026. It returned HTTP 200 without a
robot challenge. No cookie was stored or sent, no second page was requested, and
no challenge was bypassed. The raw body and sanitized headers are in the external
collection; `coverage_query_google_scholar.tsv` preserves the ten visible results.

The page yielded: a Springer linguistic-signature chapter (metadata only; no
public detector artifact/comparator), DeBERTa-Sentinel (priority table), two
listings for a software-survey fraud study (different task), GigaCheck (span
localization, different task), a BERT multi-source classification article (no
public fixed artifact/comparator in this bounded check), a reinforcement-guided
perturbation method (excluded family), a dialectical analysis paper (not a
detector release), a corpus study of academic language (not a detector release),
and DACTYL (priority table). Scholar is a supplemental first-page check, not an
exhaustive coverage claim.
