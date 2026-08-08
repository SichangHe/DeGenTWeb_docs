# DW1 accuracy-first survey of recent LLM-text detectors

Research update: 2026-08-08, America/Los_Angeles. This update supersedes the
2026-08-07 WaveDetect-first recommendation. It changes research artifacts only;
no DW1 implementation or configuration was changed.

## Answer

No 2025–2026 detector is yet demonstrated to be a drop-in replacement for DW1
Binoculars under all of the requested conditions. The strongest recent paper
results either lack a released detector state, use supervised in-distribution
training, use incomparable data or lengths, or have not reproduced Binoculars-level
accuracy on DW1. High reported numbers without those qualifications are not
treated as deployment accuracy.

The evidence screen is substantially stronger than the old WaveDetect survey,
but it does not yield an improved qualifying shortlist:

1. **IRM is the only recent, fully executable, in-scope public control.** The
   NeurIPS 2025 paper's Llama-3.2-1B pair beats same-pair Binoculars on DetectRL
   multi-domain, multi-model, and multi-attack AUROC: 97.97 versus 92.48, 97.24
   versus 92.08, and 97.19 versus 93.04. It is slightly worse on human-writing
   AUROC, 94.48 versus 94.63. Those exact Meta checkpoints are license-gated. The
   strongest anonymously downloadable family from the paper, Qwen2-0.5B, ran
   locally at 0.230 seconds per document, batch 8 and 2,048 tokens, using 30,384
   MiB per card. Its fixed 1,000-row orientation-free AUROC was 0.9436, below
   stored Binoculars at 0.9595 and FastDetectGPT at 0.9536. It is therefore a
   control, not an improved recommendation. [N2, M4]
2. **SV-Detect is reconstruction-only evidence.** Its paper reports near-perfect
   DetectRL results after training on matched source/domain/attack families. A
   local optimized FP16 feature reconstruction fit easily and was fast, but the
   authors did not release trained steering directions or logistic-regression
   state. The published accuracy is not runnable as shipped, and the adapted cost
   screen is not end-to-end detector throughput. [N3, M5]
3. **LAPD has the strongest matched zero-shot paper result but is excluded.** Its
   average AUROC is 92.37 versus 89.72 for same-pair Binoculars, and its local
   adapted score cost was within 0.53 percent of same-process Binoculars. However,
   LAPD standardizes with 10,000 categorical auxiliary samples, and its own paper
   groups it with methods that perturb or generate auxiliary sequences. Under the
   strict no-multi-perturbation constraint, it cannot be advanced without an
   explicit exception. [N1, M6]

WaveDetect is also not a recommendation: its local AUROC was 0.8906 on the same
convenience screen. Speed alone does not answer the corrected accuracy-first
request. [M2]

## Fixed deployment screen

The governing comparator is DW1's operational Binoculars: dynamic Falcon-7B and
Falcon-7B-Instruct checkpoints, one per NVIDIA RTX A6000, concurrent forwards,
batch 8, and a 2,048-token maximum. Its controlled 2026-08-07 result was 7.733
seconds per batch, 0.967 seconds per document, and 35,095 MiB peak allocated on
each card. The cached checkpoint revisions were `0ad33730b9d0911d6586670a661f04adaaf2c850`
and `40d43a5d6ac55026c5a471d908c9d3bf6623dbb1`; the result file records the
software stack and timing boundary. Candidate timing is accepted only with a
traceable same-run comparison or a conservative local screen at this batch and
length. [C3, M1]

RAG, retrieval, nearest-neighbor lookup, target-text rewriting, regeneration, and
multi-perturbation pipelines remain excluded. LAPD draws 10,000 independent token
alternatives from already-computed categorical logits, but does not decode them
into text and does not re-forward or rescore auxiliary passages. The paper marks
this family as using perturbed or generated auxiliary sequences. The conservative
decision is to apply the human's strict constraint and exclude LAPD. Its accuracy
and timing evidence is retained only to show why it would otherwise have been the
leading candidate. [N1]

Evidence labels are deliberate: **sourced** means a primary manuscript or
official artifact; **measured** means this machine; **inferred** means a bounded
operational judgment. Every evidence ID resolves in
[source_cards.md](dw1_detector_survey_sources/source_cards.md). Exact local
outputs sit beside the harnesses.

## Accuracy claims normalized

| Candidate | Strongest reported comparison | Material mismatch or failure | Result here |
| --- | --- | --- | --- |
| LAPD | Matched Llama-2 pair, five benchmark columns: 92.37 average AUROC versus 89.72 Binoculars | Average hides a 0.09-point RAID loss; paper data are not DW1; 10,000 auxiliary categorical samples violate the conservative no-multi-perturbation reading | Excluded by method |
| IRM | Matched Llama-3.2-1B family on DetectRL: 97.97/97.24/97.19 AUROC versus 92.48/92.08/93.04 Binoculars | The paper's 91.77 “average” mixes AUROC and F1 and is not itself AUROC; exact model pair is gated; public Qwen local AUROC trails Binoculars | Runnable control, not a demonstrated replacement |
| SV-Detect | In-domain DetectRL AUROCs from 99.83 to 100 in the reported source/domain/attack settings | Supervised on corresponding source/domain/attack-family data, sometimes with 10,192 examples per class; no trained detector state; local timing is an optimized reconstruction | Reconstruction-only evidence |
| EchoPrompt | Llama-3-8B proxy across DetectRL, RealDet, and RAID: 95.56 AUROC versus 90.07 Binoculars | Manuscript only; no code/checkpoint; V100, 1,024-token cap, unspecified batch; reported 0.254 seconds versus 0.157 for Binoculars lacks a complete runtime basis | Watchlist, claimed accuracy rejected as unreproduced |
| Steer-to-Detect | Same A100-80GB mixed test: 98.90 AUROC versus 87.70 Binoculars; 0.30 versus 0.50 seconds | Trained on 512 mixed pairs; average text 267 tokens and 95 percent below 435; batch 1; 39 GB at short length; no code/checkpoint | Watchlist; 2,048-token A6000 fit unproved |
| RepreGuard | Same A100-80GB test: Phi-2 96.10 and Llama-3.1-8B 94.80 AUROC versus 81.90 Binoculars | Trained on 512 Claude pairs; tests four older generators; maximum 256 tokens; no trained directions/checkpoint | Older fallback, superseded by SV-Detect |
| Uncertainty++ | Up to 93.24 average AUROC on its GPT-J black-box set and 94.79 on a newer-generator set | No like-for-like Binoculars row; length and batch are incomplete in the efficiency report | Not evidence of Binoculars parity |

The table compares only like-for-like rows within each paper. Numbers across rows
must not be ranked against each other because datasets, generation models,
domains, text lengths, contamination risks, training regimes, metrics, and
hardware differ. In particular, supervised random or matched-family splits can
produce very high AUROC without proving unseen-generator or unseen-domain
performance.

AUROC is retained because it is the most consistently reported threshold-free
metric; it is not classification accuracy. F1, raw accuracy, TPR at 1 percent
false-positive rate, and TPR at 0.01 percent false-positive rate are not
interchangeable. No paper threshold is transferred to DW1.

Contamination remains unresolved rather than assumed away. LAPD and IRM reuse
public benchmarks and do not provide an independent audit of overlap with proxy
pretraining or generator tuning. SV-Detect, Steer-to-Detect, and RepreGuard train
on related corpus or generator families, so their high in-distribution rows are
especially vulnerable to split and source cues. EchoPrompt supplies only the
manuscript evaluation. None of those facts proves contamination occurred; each is
an evidence gap that prevents treating the reported number as DW1 accuracy.

## Excluded accuracy benchmark: LAPD

### Sourced result

[LAPD](https://arxiv.org/abs/2604.16923), released in April 2026, contrasts a base
model with its aligned counterpart and information-weights the per-token
preference discrepancy. The official repository was inspected at commit
`1988eb68b70205d471c1924b6bbf1e199452662d`. Its matched Table 13 gives:

| Benchmark | Binoculars AUROC | LAPD AUROC |
| --- | ---: | ---: |
| M4 | 87.27 | 88.02 |
| DetectRL multi-LLM | 93.11 | 97.17 |
| DetectRL multi-domain | 88.33 | 96.11 |
| RAID | 85.30 | 85.21 |
| RealDet | 94.56 | 95.32 |
| Average | 89.72 | 92.37 |

All rows use the Llama-2-7B base/instruct pair, so the average improvement is a
real method comparison on those data. It is not a universal win: RAID is slightly
worse. Main experiments cap input at 1,024 tokens and use two RTX 3090 24 GB
cards. At batch 1 over 300 instances, the paper reports 0.5792 seconds per LAPD
text and 0.6549 for Binoculars. [N1]

### Measured feasibility

The local harness used DW1's two dynamic Falcon checkpoints, eight fixed documents
of exactly 2,048 tokens, one warm-up, and three runs. It executes the released
10,000-sample statistic after the same concurrent model forwards as Binoculars.
Median LAPD time was 7.7641 seconds per batch, or 0.9705 per document, versus
7.7234 and 0.9654 for the preceding same-process comparator block. Both peaked at
35,095 MiB on each A6000. The official cache-building path reuses base logits
when the base is also the sampling model, while the release's separate multi-GPU
runner forwards that model redundantly. The harness uses the cache-path behavior and is therefore
a transparent executable adaptation, not an unchanged CLI timing. [N1, M6]

### Decision boundary

The bounded cost screen supports near-Binoculars feasibility, but it is only three
repetitions and uses an adapted cache path. More importantly, the 10,000 auxiliary
categorical samples trigger the strict method exclusion. The timing checkpoints
also differ in precision and family from the paper's strongest Llama pair, so
dynamic-Falcon cost does not transfer paper AUROC. The repository has no declared
license. LAPD is not advanced or recommended.

## Reconstruction-only evidence: SV-Detect

### Sourced result

[SV-Detect](https://arxiv.org/abs/2606.07313), released in June 2026, runs a frozen
GPT-Neo-2.7B once, mean-pools each hidden layer, compares those vectors with
learned steering directions, and applies logistic regression. The official
[repository](https://github.com/Atmyre/SV-Detect) was inspected at commit
`a25469ba6a1fa2adcf644338db6fef712511da66`. Its DetectRL in-domain table reports
AUROCs between 99.83 and 100 across the selected multi-domain, multi-LLM, and
multi-attack settings. Those are trained tests, not zero-shot comparisons:
training uses the corresponding setting and can reach 10,192 examples per class.
Cross-source results are reported separately, without a like-for-like Binoculars
row. [N3]

On one A100 40 GB, float16, 512 tokens, the paper reports 25.71 milliseconds at
batch 1, 74.3 texts per second at batch 16, and 8,951 MB peak. That establishes a
small model path, but not DW1 length or comparator parity. [N3]

### Measured feasibility

The public GPT-Neo-2.7B revision was reconstructed at 2,048 tokens. One-card batch
1 measured 0.304 seconds and 6,114 MiB peak. Two-card data parallel batch 8
measured 1.248 seconds per batch, 0.156 per document, and under 8,849 MiB per
card. Unlike the release's one-text-at-a-time FP32 activation extraction to CPU,
the local harness uses FP16, batches four documents per card, and projects inside
GPU hooks. It is an optimized mathematical feature-cost adaptation, not the exact
released path or end-to-end detector throughput. Deterministic dummy directions
were required because the repository ships neither trained steering directions
nor logistic-regression state; the resulting scores have no accuracy meaning.
[M5]

### Decision boundary

SV-Detect has a large reconstructed cost margin and the highest recent reported
numbers, but no runnable released detector. It is not a qualifying candidate. A
future reconstruction would require separately partitioned labels with
generator/date/domain holdouts; random or matched-family validation would repeat
the paper-comparability problem.

## Runnable in-scope control: IRM

### Sourced result

[IRM's official NeurIPS 2025 paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f50258b34f1c5080e43281e05050034e-Abstract-Conference.html)
scores instruction-model sequence log-likelihood minus base-model sequence
log-likelihood. The official supplemental archive contains runnable code. Its
matched Llama-3.2-1B DetectRL rows show clear AUROC gains over Binoculars for
multi-domain, multi-LLM, and multi-attack data, while its human-writing row is
0.15 points worse. The paper's single 91.77 aggregate combines AUROC and F1
columns, so it is not reported here as AUROC. Experiments use two RTX 4090 24 GB
cards. [N2]

### Measured feasibility and accuracy screen

The Llama checkpoints required authenticated license acceptance, which was not
bypassed. The anonymously downloadable Qwen2-0.5B base/instruct pair is explicitly
evaluated in the paper: 90.14, 89.43, and 90.47 AUROC on its multi-domain,
multi-LLM, and multi-attack tasks. At float32, batch 8 and 2,048 tokens, the pair
measured 1.834 seconds per batch, 0.229 per document, and 30,384 MiB peak on each
A6000. [N2, M4]

On a fixed local screen of 500 human and 500 generated rows, IRM reached 0.9436
orientation-free AUROC. Stored scores on the same rows were 0.9595 for Binoculars
and 0.9536 for FastDetectGPT. Stored comparators may differ in software and
truncation, and the sample is not stratified, so this is triage—not a calibrated
accuracy verdict. It is nonetheless sufficient to reject a claim that the public
Qwen variant has already beaten Binoculars on DW1. The base and instruction
tokenizers were loaded separately and matched on all selected texts; the trial,
selection-manifest, and selected-text hashes are preserved with the result. [M4]

## Unreleased high-accuracy watchlist

**EchoPrompt**, dated 6 August 2026, prepends a fixed assistant context before
base/instruct likelihood scoring. It reports 95.56 average AUROC versus 90.07 for
Binoculars with a Llama-3-8B proxy across DetectRL, RealDet, and RAID. Its figure
reports 0.254 seconds per text versus 0.157 for Binoculars, but the timing proxy,
batch, and complete hardware basis are not given; experiments otherwise mention
a V100 32 GB and a 1,024-token cap. No official code or checkpoint was found.
The prompt is not target rewriting, but the method remains unreproducible. [N4]

**Steer-to-Detect**, dated May 2026, reports the strongest direct accuracy/runtime
row: 98.90 AUROC and 0.30 seconds versus Binoculars at 87.70 and 0.50 on the same
A100 80 GB mixed test. It is supervised on 512 mixed pairs. Text averages 267
tokens, 95 percent is shorter than 435, batch is 1, and peak inference allocation
is 39 GB. No official implementation or trained state was found. A 39 GB short-text
batch-1 result cannot establish batch-8, 2,048-token A6000 fit. [N5]

Neither claim is called reproducible accuracy. Release and exact A6000 evidence
would be required before promotion.

## Other recent methods screened

- RepreGuard is a credible TACL 2025 predecessor, but its high same-run result is
  trained on 512 Claude pairs, tested on four older generators, capped at 256
  tokens, and not shipped with learned detector state. [N6]
- Uncertainty and Uncertainty++ have official MIT-licensed code and strong 2026
  results, but no same-benchmark Binoculars comparison and incomplete efficiency
  length/batch reporting. They cannot establish the requested parity. [N7]
- DeBERTa-Sentinel reports 99.53 ROC-AUC on one GLC random split, but releases no
  checkpoint and provides no credible cross-generator or cross-domain parity
  evidence. DWT-Fusion similarly has no released detector and weaker reported
  M4/MAGE results. Multi-Level Contextual Detection releases only supplementary
  material. GPTZero is commercial rather than a reproducible released method.
  [N8]
- DivScore is specialized-domain work with a domain-distillation pipeline rather
  than a general DW1 replacement. PhantomHunter requires several probability
  extractors and supplies neither a detector checkpoint nor useful speed evidence.
  Late-stage stability methods do not supply a like-for-like Binoculars result.
  [N8]

## Method exclusions

GTCL uses k-nearest-neighbor classification over retained embeddings at inference
and is excluded as retrieval. Triospect creates summaries, simplifications, and
multiple derived views and is excluded as rewriting/regeneration and a
multi-view pipeline. LAPD is excluded under the strict multi-perturbation boundary
because it uses 10,000 auxiliary categorical samples. DetectGPT, DetectNPR,
DNA-GPT, RAIDAR, TOCSIN, DetectAnyLLM
Reference Clustering, and other RAG/retrieval/rewrite/multi-perturbation families
remain excluded before accuracy ranking. Their high numbers cannot override the
deployment constraint. [N8, X2]

## Disposition and future gate

Do not replace Binoculars, and do not present a recent detector shortlist as
qualified. IRM is the reproducible zero-shot control; its public variant trailed
the stored local Binoculars score in the bounded screen. SV-Detect is only a
possible supervised reconstruction if that future scope and label budget are
explicitly approved. LAPD stays excluded unless the human explicitly permits its 10,000
auxiliary categorical samples. EchoPrompt and Steer-to-Detect need released
artifacts before any A6000 accuracy claim can be reproduced.

Any future candidate must be evaluated on a frozen, stratified DW1 set, with
per-generator, per-domain, per-language, per-date, and length-band results. It must
include current generators and attacks, select low-false-positive thresholds only
on separate human calibration data, and preserve Binoculars as a same-run
comparator.

A method advances beyond pilot only if it matches or improves Binoculars AUROC
and the chosen low-false-positive operating point on the same held-out rows,
while retaining the measured A6000 speed boundary. Paper averages alone are not
an acceptance criterion.

## Coverage and uncertainty

The update prioritized 19 public 2025–2026 manuscripts and eight official
repositories. Primary PDFs, hashes, revisions, and artifact gaps are preserved in
[paper_artifacts.md](dw1_detector_survey_sources/paper_artifacts.md); discovery
and robot-gate handling are in
[search_log.md](dw1_detector_survey_sources/search_log.md).

Google Scholar returned an HTTP 403 robot challenge and OpenReview challenged the
IRM page. Neither was bypassed. The official NeurIPS proceedings, public arXiv
API/PDFs, GitHub, and public Hugging Face APIs were used instead. Therefore this
is a bounded primary-source study, not a claim of exhaustive Scholar coverage.

Local timings are narrow feasibility screens: one machine, one software state,
one warm-up, three repetitions, and no sustained worker contention. CUDA peak
allocation is not total process memory. The IRM local AUROC uses a convenience
corpus, not a production test. LAPD and SV-Detect local runs establish adapted
cost only. These limitations support the plain conclusion: no qualifying recent
method has demonstrated every requirement at once.
