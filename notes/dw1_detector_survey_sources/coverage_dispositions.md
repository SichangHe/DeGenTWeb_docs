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
| 2026-06-01 | [Uncertainty++, 2606.02158](https://arxiv.org/abs/2606.02158) | Retain/reject: public code and strong AUROC exist, but no like-for-like Binoculars row or complete length/batch speed basis establishes parity. [N7] |
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
| 2026-03-05 | [NOTAI.AI, 2603.05617](https://arxiv.org/abs/2603.05617) | Retain/reject: a FastDetectGPT-derived explanatory ensemble, but no public frozen state and like-for-like DW1 low-FPR/speed evidence were found in the bounded check. |
| 2026-02-08 | [Markov-informed calibration, 2602.08031](https://arxiv.org/abs/2602.08031) | Retain released calibration: official code exists, but per-dataset supervised states are not shipped and its Binoculars gains do not establish a qualifying detector or whole-path speed. [N10] |
| 2026-02-01 | [Prototype-based proxy routing, 2602.01240](https://arxiv.org/abs/2602.01240) | Retain/reject: routing among proxies adds artifact/training requirements and lacks a released fixed DW1 parity and two-A6000 result. |
| 2026-01-27 | [Variation/VaryBalance, 2602.13226](https://arxiv.org/abs/2602.13226) | Exclude: the claimed gain over Binoculars depends on LLM rewrites of the target text. |
| 2026-01-08 | [Late-stage stability, 2601.04833](https://arxiv.org/abs/2601.04833) | Retain/reject: no like-for-like Binoculars accuracy and fixed A6000 speed evidence supports promotion. [N8] |
| 2025-11-03 | [DEER, 2511.01192](https://arxiv.org/abs/2511.01192) | Retain/reject: supervised mixture-of-experts claims generalization, but no released deployment state and fixed comparator evidence establish DW1 parity. [N8] |
| 2025-10-14 | [StyleDecipher, 2510.12608](https://arxiv.org/abs/2510.12608) | Retain/reject: supervised stylistic performance lacks a runnable frozen state and like-for-like low-FPR/A6000 evidence. |
| 2025-09-26 | [Mixture of Detectors, 2509.22147](https://arxiv.org/abs/2509.22147) | Retain/reject: ensemble claims do not provide the fixed public state, comparator, and latency basis required here. |
| 2025-09-23 | [Diversity Boosts Detection, 2509.18880](https://arxiv.org/abs/2509.18880) | Retain/reject: training-data diversity gains do not establish a released detector that beats Binoculars on the same held-out rows. |
| 2025-09-15 | [DetectAnyLLM, 2509.14268](https://arxiv.org/abs/2509.14268) | Exclude: Reference Clustering performs nearest-reference lookup over retained human/generated sets. [X2] |
| 2025-09-02 | [MoSEs, 2509.02499](https://arxiv.org/abs/2509.02499) | Exclude: inference activates examples from a Stylistics Reference Repository for conditional thresholds, crossing the no-retrieval gate. |
| 2025-08-19 | [MGT-Prism, 2508.13768](https://arxiv.org/abs/2508.13768) | Retain/reject: supervised spectral-alignment results lack a public frozen state and same-row low-FPR, length, and speed comparison. |
| 2025-08-15 | [SpecDetect, 2508.11343](https://arxiv.org/abs/2508.11343) | Retain/reject: formula is fast but the public artifact is incomplete and published accuracy does not establish Binoculars parity under DW1. [S1, S2] |
| 2025-08-03 | [Temporal Tomography, 2508.01754](https://arxiv.org/abs/2508.01754) | Retain/reject: theoretical temporal signal lacks a released qualifying state and matched low-FPR/A6000 comparison. |
| 2025-07-31 | [T-Detect, 2507.23577](https://arxiv.org/abs/2507.23577) | Retain/reject: tail normalization targets attacks but has no released fixed state or complete like-for-like Binoculars and A6000 result. |
| 2025-06-18 | [PhantomHunter, 2506.15683](https://arxiv.org/abs/2506.15683) | Retain/reject: several probability extractors, no released detector state, and insufficient speed evidence. [N8] |
| 2025-06-07 | [DivScore, 2506.06705](https://arxiv.org/abs/2506.06705) | Reject for scope: specialized legal/medical domain distillation is not a general DW1 replacement. [N8] |
| 2025-05-21 | [AGENT-X, 2505.15261](https://arxiv.org/abs/2505.15261) | Retain/reject: multiple reasoning LLM agents provide no plausible near-Binoculars latency or fixed public deployment artifact. |
| 2025-05-20 | [FAID, 2505.14271](https://arxiv.org/abs/2505.14271) | Reject for scope: fine-grained multilingual academic/hybrid attribution is not the fixed binary general-document task. |
| 2025-05-20 | [Domain Gating Ensemble, 2505.13855](https://arxiv.org/abs/2505.13855) | Retain/reject: supervised ensemble results lack a released state and like-for-like operating-point/speed evidence. |
| 2025-05-08 | [Multiscaled Conformal Prediction, 2505.05084](https://arxiv.org/abs/2505.05084) | Retain calibration watchlist: controls FPR on RealDet calibration, but does not ship a DW1 calibration state or establish a whole-detector A6000 comparison. |
| 2025-04-22 | [Dynamic perturbations, 2504.21019](https://arxiv.org/abs/2504.21019) | Exclude: target-text dynamic perturbations violate the fixed multi-perturbation constraint. |
| 2025-04-01 | [Short-PHD, 2504.02873](https://arxiv.org/abs/2504.02873) | Exclude: the detector inserts off-topic content into the target, violating the no-rewriting/perturbation gate. |
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

## Accounting for the other export rows

The remaining deduplicated rows did not meet the declared plausible-general-
detector rule. They were still inspected at title and abstract level and assigned
one of these source-mapped dispositions:

- **Different task or unit:** 2608.03859 (source plagiarism/reranking),
  2607.23805 (survey-fraud study), 2607.14905 (reasoning authorship attribution),
  2606.18946 (sentence-level hybrid documents), 2605.03723 (change-point hybrid
  segmentation), 2604.21365 (generated code), 2604.21300 (authorship attribution),
  2604.04932 (creator/editor attribution), 2510.00890 (scientific span detection),
  2509.25154 (generated judgments), 2509.21269 (corpus/localization), 2508.18715
  (dialogue-specific detection), and 2506.02959 (human-AI coauthoring).
- **Language- or benchmark-specific rather than a general English replacement:**
  2604.11796, 2603.27949, 2512.21709, 2510.20610, 2510.16573, 2510.03502,
  2509.26051, 2509.00731, 2508.06913, 2507.05157, 2503.00032, 2502.12064,
  2501.11914, 2501.09813, 2501.11012, and 2501.08913.
- **Dataset, evaluation, attack, analysis, privacy, or survey—not a new qualifying
  detector:** 2606.04906, 2606.04177, 2605.20761, 2605.15518, 2605.14240,
  2604.19768, 2604.16607, 2603.23146, 2603.18750, 2602.11871, 2601.20006, 2601.04641,
  2512.09292, 2510.22874, 2510.19492, 2510.12476, 2507.15286, 2505.24523,
  2505.15422, 2504.11369, 2503.23622, 2502.15654, 2502.12611, and 2501.18998.
- **Narrow system paper, augmentation/training recipe, or no high-accuracy claim
  sufficient to enter the priority table:** 2605.02712, 2602.15514,
  2601.03812, 2511.21744, 2511.17402, 2511.00988, 2510.16549, 2509.00623,
  2508.11933, 2506.01702, 2505.12507, 2505.11550, 2503.22338, 2503.15044,
  2502.16857, 2502.12734, and 2501.14288.
- **Excluded method family not already in the priority table:** 2606.00402
  (rewrite-based), 2510.02319 (adversarial perturbation modeling), 2509.15550
  (mutation-repair), and 2504.21019 (dynamic perturbations).

The raw exports, rather than this human-readable grouping, remain the canonical
result inventory.

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
