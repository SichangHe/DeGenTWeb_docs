# DW1 detector survey source cards

## Reading rule

`S` marks a sourced fact from a primary paper, official implementation, or public
official artifact. `M` marks a direct local measurement. `E` marks arithmetic or
hardware estimation. `I` marks an inference. Quotes are short searchable anchors;
the adjacent locator holds the full context. Paper-reported results are not treated
as independent replications.

The primary PDFs are retained in the established external paper collection. Full
filenames and hashes are in `paper_artifacts.md`. Repository commits and search
routes are in `search_log.md`.

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
