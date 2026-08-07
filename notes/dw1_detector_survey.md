# DW1 alternative LLM-text detector survey

Research date: 2026-08-07. This is a read-only research study; no DW1
implementation, configuration, credentials, or browser state was changed.

## Decision

WaveDetect is the only newly found method I would advance immediately to a
bounded DW1 evaluation. Its official public checkpoint ran on one NVIDIA RTX
A6000 at batch 8 and 2,048 tokens, used 15,413 MiB, or about 15.1 GiB, of peak
allocated memory, and took
0.0388 seconds of scoring time per document. The controlled DW1 Binoculars comparator used both
A6000s, 35,095 MiB, or about 34.3 GiB, on each, and took 0.967 seconds per
document. WaveDetect was
therefore measured faster, without defining an arbitrary tolerance for “not much
slower.” On a fixed 1,000-document DW1 triage screen, WaveDetect at 1,024 tokens
had 0.891 AUROC; stored historical Binoculars and FastDetectGPT scores on those
rows had 0.959 and 0.954, but their software and truncation basis may differ. It is
a viable pilot, not an accuracy-equivalent replacement. [M1, M2, W1, W2]

DetectLLM-LRR is also speed- and hardware-qualified, and it is already calculated
in DW1. With the DW1 performer alone it measured 0.950 seconds per document
versus 0.967 for Binoculars. Its existing 8,170-row AUROC is only 0.799 versus
0.947 for Binoculars and 0.939 for FastDetectGPT, so it is useful as a cheap
baseline or ensemble feature, not as the primary replacement. [M1, M3, L1]

Base SpecDetect is the strongest next formula to investigate: it measured 0.942
seconds per document with one DW1 performer and its paper reports a direct
same-H800 speed win over FastDetectGPT. I do not call it deployably viable because
the inspected official release contains concrete runtime defects and no DW1
accuracy or threshold evidence. [M1, S1, S2]

Lastde and PAWN fit the two-A6000 memory envelope on their reported setups, but
neither has a traceable like-for-like runtime against 2,048-token DW1 Binoculars.
Their exact blocker is unverified speed, compounded by artifact or calibration
gaps. DetectAnyLLM was excluded because its Reference Clustering stage performs
nearest-reference lookup. RADAR and OpenAI RoBERTa are fast and fit, but their
existing DW1 AUROCs are too weak to recommend. [A1, P1, D1, R1, M3]

## What “viable” means here

The fixed hardware limit is two NVIDIA RTX A6000 GPUs, each reporting 49,140 MiB.
The fixed speed requirement is “not much slower than Binoculars.” No percentage or
multiplier was invented. A method receives a speed-qualified label only when a
traceable same-input local comparison shows that it is no slower than DW1
Binoculars, or when a primary source reports a same-run comparison against the
canonical comparator. Hardware estimates alone do not establish viability.

RAG, retrieval, nearest-neighbor retrieval, text rewriting, regeneration, and
multi-perturbation approaches are outside scope. Analytic conditional sampling
from already computed logits, as used by FastDetectGPT-style methods, is not text
generation and remains in scope. [X2]

Labels used below are explicit. `Sourced` is a primary paper or official artifact
fact. `Measured` is a direct local observation. `Estimated` is arithmetic or a
capacity calculation. `Inferred` is an operational judgment. The evidence IDs
resolve in
[source_cards.md](dw1_detector_survey_sources/source_cards.md); exact commands and
outputs are beside the benchmark harnesses.

## Comparator normalization

Canonical Binoculars uses BF16 Falcon-7B and Falcon-7B-Instruct over 512-token
prefixes, with the models placed on separate devices in the official release.
DW1 instead uses its two `SichangHe` Falcon-7B dynamic-model repositories, batch 8,
a 2,048-token limit, one model per A6000, and concurrent forwards. This operational
DW1 version is the governing speed comparator. [C1, C2, C3]

Canonical black-box FastDetectGPT uses GPT-J-6B for reference sampling and
GPT-Neo-2.7B for scoring. Its paper reports 233 seconds for five 500-document XSum
sets on one Tesla A100, excluding initialization. Dividing the stated total by
2,500 yields an estimated 93.2 milliseconds per document; sequence and batch
bases are not reported well enough to compare that number directly with the DW1
2,048-token batch-8 run. The DW1 FastDetectGPT score instead reuses the same two
Falcon logits as Binoculars, so its forward-pass resource envelope is operationally
coupled to the DW1 Binoculars pair. [C4, C3]

The controlled local comparator used the eight longest stored trial documents,
all truncated to 2,048 tokens, one warm-up, and three timed repetitions. Every
method used the same timing boundary: device-resident token IDs entered the timed
operation and CPU detector scores left it. Model loading, tokenization, and input
transfer were excluded. The successful harness copied the token encoding before
moving it to each GPU, matching the established trial path. Calling the current
`Binoculars.compute_score` path directly first failed because the installed
Transformers version mutates `BatchEncoding.to`, leaving both references on the
second GPU. This reproducibility incident did not change DW1 code. [M1]

## Candidate one: WaveDetect — viable bounded pilot

Method and model. Sourced: WaveDetect runs Qwen2.5-0.5B-Base once, applies a
differentiable continuous wavelet transform to the token-probability signal, and
classifies the spectrum with a modified ResNet-18 of 11.7 million parameters. It
does not retrieve or rewrite text. The official public artifact is ungated,
Apache-2.0, and includes a roughly 1.01 GB checkpoint and loader. [W1, W2]

Length, batch, and mapping. Sourced: the official helper defaults to 1,024 tokens
and accepts one string, while the underlying model accepts a batch. Measured: the
screen used batch 8 on GPU 0 only at both 1,024 and 2,048 tokens; the second A6000
was unused. The 2,048-token extension used the checkpoint's underlying model,
because the helper exposes its maximum as a constructor option. [W2, M2]

Memory. Measured: 8,195 MiB peak allocated at 1,024 tokens and 15,413 MiB at 2,048
tokens on one A6000. That is a direct fit, not a parameter-size estimate. [M2]

Runtime. Measured: the 1,024-token median was 0.16612 seconds per batch. The
2,048-token runs were 0.31117, 0.30803, and 0.31007 seconds per batch, with a
0.31007 median. That is 0.03876 seconds per document and a 0.04010 latency ratio
to the separately measured DW1 Binoculars run. The paper itself reports theoretical
complexity but no measured latency, so the local measurement is the runtime basis.
[M2, W1]

Direct comparator result. Against Binoculars, the same hardware, batch, documents,
and 2,048-token cap establish a clear speed pass and much lower memory use. Against
FastDetectGPT, the local accuracy screen uses identical rows, but no like-for-like
isolated FastDetectGPT latency was produced; the canonical paper number uses a
different GPU, model pair, sequence basis, and unreported batch. WaveDetect is not
claimed faster than canonical FastDetectGPT from those incomparable numbers.
[M1, M2, C4]

Effectiveness and failures. Measured: fixed seed-42, 500 human and 500 generated
available local texts, batch 8, maximum 1,024 tokens. WaveDetect AUROC was 0.89056;
the stored comparators on the same rows were Binoculars 0.95949 and FastDetectGPT
0.95362, although those historical scores may use different software and truncation
bases. Sourced: WaveDetect was trained primarily on RAID, and its authors warn that
those generators are relatively old or weak. Inferred: the checkpoint offers useful
independent signal and a large speed reserve, but distribution shift, default-length
truncation, score threshold, low-FPR behavior, and recent-generator coverage must be
validated before replacement use. [M2, W1, R2]

## Candidate two: DetectLLM-LRR — viable fast baseline, weak replacement

Method and model. Sourced: LRR uses one proxy model forward and divides mean log
likelihood by mean log rank. It does not retrieve or rewrite. The primary paper
tests GPT2-XL through NeoX-20B; the official repository is public. DW1 already
computes the score from its performer logits. [L1, C3]

Length, batch, and mapping. Sourced: the repository's generation default is 200
tokens and the paper timing batch is unreported. Measured: the controlled DW1
formula run used the performer on GPU 1, batch 8, and 2,048 tokens; GPU 0 remained
effectively unused. [L1, M1]

Memory and runtime. Measured: 35,095 MiB peak allocated on the performer A6000.
Median batch latency was 7.59651 seconds, or 0.94956 seconds per document, a
0.98241 ratio to DW1 Binoculars. Sourced comparison: the paper's A100-40GB table
reports 0.08 seconds for GPT-J and 0.19 for Neo-2.7B, averaged over ten reruns,
but that short, unbatched-or-unspecified basis is not substituted for the local
measurement. [M1, L1]

Direct comparator result. Against Binoculars, LRR passes the hardware and speed
screen, but concurrent two-GPU Binoculars means dropping one Falcon forward saves
little wall time. Against FastDetectGPT, LRR avoids the second proxy model but is
far weaker on the existing DW1 score corpus: 0.79908 AUROC versus 0.93860, with
Binoculars at 0.94670. [M1, M3]

Failures. Sourced: the method depends on proxy/source statistics and is sensitive
to generation temperature and decoding. Measured: its local separation is much
weaker. Inferred: retain it as a baseline or ensemble feature; do not promote it to
primary detector. [L1, M3]

## Candidate three: SpecDetect — speed-qualified formula, artifact blocked

Method and model. Sourced: base SpecDetect takes one proxy model's token log
probabilities, removes their mean, applies a discrete Fourier transform, and uses
total spectral energy. SpecDetect++ adds analytic independent samples from the
same logits. Neither variant rewrites or retrieves text. Black-box experiments use
GPT-J-6B. [S1]

Length, batch, and mapping. Sourced: official generation code defaults to 200
tokens; the paper's inference batch is unreported. Measured: the base formula used
the DW1 performer on GPU 1, batch 8, and 2,048 tokens. [S1, M1]

Memory and runtime. Measured: the base formula used 35,095 MiB on one A6000 and
0.94227 seconds per document, a 0.97486 ratio to DW1 Binoculars. Sourced: in one
same-H800 GPT-4-Turbo/XSum experiment with GPT-J-6B, milliseconds per sample were
42.57 SpecDetect, 47.83 FastDetectGPT, 47.29 SpecDetect++, 50.92 Lastde, and 93.28
Lastde++. Those are direct within-run comparisons, but the sequence and batch bases
are not reported. [M1, S1]

Direct comparator result. Base SpecDetect passes both the local Binoculars speed
screen and the paper's same-run FastDetectGPT comparison. Accuracy is not yet
known on DW1: M1 validates only its formula cost, not its classification behavior.
The paper reports average black-box AUC 0.8875 for base SpecDetect and 0.8791 for
FastDetectGPT on its own three-dataset, twelve-source setup, which cannot be
transferred to DW1. [M1, S1]

Artifact blocker. Sourced: the repository calls itself an initial release, omits
the referenced requirements file, applies NumPy directly to a CUDA tensor in the
base path, and calls `.cpu()` on a NumPy result in the enhanced path. Inferred:
the formula is a good controlled ablation because it can reuse existing logits,
but the official artifact is not deployable unchanged and has no threshold. It is
therefore a candidate, not an end-to-end viable recommendation. [S2]

## Candidate four: Lastde and Lastde++ — hardware fit, speed unverified

Method and model. Sourced: base Lastde combines likelihood with multiscale
diversity entropy over one proxy model's token-probability sequence. Lastde++ adds
analytic same-logit sampling. Black-box tests use GPT-J-6B. Neither rewrites or
retrieves. [A1]

Length, batch, mapping, and memory. Sourced: official generations default to 200
tokens. The paper reports an overall setup of two RTX 3090 24 GB GPUs and FP16 for
GPT-J, but not a detection batch or per-model mapping. Estimated: two A6000s have
twice the per-GPU memory and therefore meet the reported hardware envelope, but
this is capacity evidence, not a DW1 runtime measurement. [A1]

Runtime and comparison. The Lastde paper provides no detector timing. SpecDetect's
same-H800 run measures base Lastde at 50.92 ms versus FastDetectGPT at 47.83, and
Lastde++ at 93.28. That comparison says base Lastde is close to FastDetectGPT in
one short-text setup and Lastde++ is slower there, but neither is directly compared
with 2,048-token DW1 Binoculars. Because “not much slower” has no invented numeric
threshold, the exact blocker is a missing A6000, batch-8, 2,048-token measurement.
[A1, S1]

Operational fit and failures. Sourced: Lastde has sensitive time-series
hyperparameters and proxy choice; Lastde++ adds computation over sampled token
statistics. Inferred: do not prioritize either ahead of WaveDetect or base
SpecDetect until the missing direct timing and DW1 discrimination checks exist.

## Candidate five: PAWN — small supervised method, artifact and speed blocked

Method and model. Sourced: PAWN makes one frozen GPT-2 or Llama-3.2-1B-Instruct
forward, then a trained attention head weights token-distribution metrics using
hidden states and positions. The head has roughly 989 thousand or 1.6 million
trainable parameters. It does not retrieve or rewrite at inference. [P1]

Length, batch, mapping, and memory. Sourced: maximum length is 512. Reported
training batches are 128, 32, and 128 across its three benchmarks. Every experiment
ran on one RTX 3090 24 GB. Estimated: either published backbone should fit easily
on one 48 GB A6000, leaving the second free. [P1]

Runtime and comparison. The paper reports cache-building and training-epoch time,
not inference latency. The repository contains a benchmark script but no official
result. There is no traceable like-for-like speed comparison to Binoculars or
FastDetectGPT, so the speed requirement is unverified. [P1]

Artifact and failure blockers. The public repository contains training code but no
released standalone checkpoint or GitHub release; reproduction commands reference
local W&B runs and paths. Supervised DW1 training and threshold calibration would
be required. The paper reports paraphrase susceptibility. Inferred: PAWN remains a
research candidate, not a viable immediate alternative. [P1]

## Screened exclusion: DetectAnyLLM — reference retrieval disallowed

Method and model. Sourced: DetectAnyLLM trains a scoring model using Direct
Discrepancy Learning, then uses a FastDetectGPT-like analytic discrepancy and
Reference Clustering. At inference, Reference Clustering compares the input's
discrepancy against retained human and generated reference sets, sorts distance,
and selects a nearest reference window. That is reference retrieval under this
study's fixed exclusion, regardless of its compute cost. The paper's main tables
use GPT-Neo-2.7B. [D1]

Length, batch, mapping, and memory. Sourced: official evaluation defaults to batch
1. README reports about 15 GB evaluation memory, which fits one A6000. The public
artifact is instead a roughly 2.2 MB LoRA adapter for Qwen2-0.5B; it is public and
ungated, but the card does not document length, hardware, use, evaluation, or
license. [D1]

Runtime and comparison. No paper or artifact inference timing exists. The paper
compares favorably with FastDetectGPT under its own model/data setup, but it does
not supply a speed comparison. The smaller public adapter is not the paper's main
GPT-Neo-2.7B configuration. Even if retrieval were allowed, exact blockers would
remain variant traceability, a documented loader/evaluation path, 2,048-token
behavior, and like-for-like A6000 timing. [D1]

Operational failures. As a trained scoring model, it can inherit training-set and
threshold shift. It is excluded rather than ranked, and is not called viable.

## Candidate six: RADAR — hardware fit, rejected for DW1 quality

Method and model. Sourced: RADAR uses a paraphraser only during adversarial
training. Inference is a released RoBERTa-large classifier, maximum 512 tokens,
with a 1.42 GB public weight file. Training used batch 32 on two V100 32 GB GPUs.
It therefore does not violate the no-rewrite inference constraint. [R1]

Runtime and hardware. Measured historical DW1 code successfully ran the checkpoint
on local GPU hardware and recorded 8,170 batch-1 documents in 159.42 seconds, but
the Binoculars trace covers only 3,108 documents and different work. That is not a
like-for-like speed ratio. The small encoder and successful run establish practical
hardware fit; no strict speed-qualified label is needed because accuracy rejects it.
[C3, R1]

Direct comparator result and failures. Measured across all stored DW1 rows, RADAR
AUROC is 0.67293 versus 0.94670 Binoculars and 0.93860 FastDetectGPT. Sourced: RAID
found RADAR unusually poor on movie reviews and showed bias toward seen domains and
models. Inferred: reject it for DW1 despite low operational cost. [M3, R1, R2]

## Control: OpenAI RoBERTa — rejected

DW1 already measured the public RoBERTa detector. Its stored AUROC is 0.60777,
far below both comparators. It is fast and fits easily, but supervised distribution
shift dominates its operational value. RAID independently documents analogous
domain/model sensitivity in neural detectors. Reject. [M3, R2]

## Exclusions

DetectGPT and DetectNPR were excluded because they generate many perturbations and
score repeated model calls. DNA-GPT was excluded because it truncates and rewrites
or completes the text. RAIDAR and TOCSIN were excluded because rewriting or
regeneration is part of their detection signal. DetectAnyLLM was excluded because
its Reference Clustering searches retained reference sets at detection time.
Retrieval defenses, RAG, nearest-neighbor proxy methods, and example-retrieval
prompting were excluded before ranking. Ghostbuster was separately rejected
because its defining released method depends on closed ada and davinci
probabilities and lacks an official runnable detector artifact. FourierGPT was
screened independently, but has no reported inference runtime; its released
supervised path needs labeled fitting, while its heuristic path requires a
prompt-matched human/generated pair rather than classifying one DW1 document. [D1,
F1, X1, X2]

## Recommended bounded next step

First, evaluate the unchanged public WaveDetect checkpoint on a genuinely held-out,
stratified DW1 set, preserving generator, domain, language, date, and length. Report
AUROC only as a secondary diagnostic; select and report a low false-positive
operating point from separate in-domain human calibration data. Include recent
generators, repetition penalties, paraphrases, homoglyphs, whitespace, and mixed
human/machine documents. Measure service throughput with the intended worker
concurrency at both 1,024 and 2,048 tokens. [W1, R2, M2]

Second, use base SpecDetect only as a formula-level ablation on already available
DW1 logits, then decide whether accuracy justifies repairing or independently
implementing it. Keep LRR as the zero-cost comparison. Do not spend implementation
time on Lastde++, PAWN, RADAR, or RoBERTa until their stated blockers change;
DetectAnyLLM remains excluded by method.

No implementation work is part of this recommendation, and none was performed.

## Uncertainty and limits

The Google Scholar query was stopped at its HTTP 403 robot challenge and not
bypassed. The discovery corpus therefore comes from public primary papers, official
venue metadata, repositories, and artifacts, not complete Scholar results. The
exact attempt and public search route are in
[search_log.md](dw1_detector_survey_sources/search_log.md).

The direct timings are narrow feasibility tests: one machine, one software state,
one warm-up, three repetitions, longest available documents, and no sustained
load. Allocated CUDA memory is not total process or reserved memory. The accuracy
screens reuse an existing convenience corpus, are not threshold-calibrated, and do
not establish a safe low-FPR deployment. The 148 historical rows whose text files
were absent were excluded from the fixed WaveDetect sample pool. [M1, M2, M3]

## Adversarial review record

Reviewer identity: `/root/adversarial_detector_review`, a distinct read-only
reviewer. Scope: infer the intended goal from the survey, memo, archived source
cards and harnesses, DW1 comparator code, and official artifacts; challenge
hardware/runtime claims, comparator normalization, exclusions, source mapping,
and listenable-email fidelity.

First-pass verdict: fail pending material fixes. The reviewer found that the first
M1 run included tokenization and input transfer for Binoculars but not for the two
candidate formulas; DetectAnyLLM's nearest-reference stage contradicted the
retrieval exclusion; FourierGPT had been dismissed with an unsupported
“superseded” claim; the email needed the mixed-basis accuracy caveat and descriptive
links; the WaveDetect environment record omitted software, driver, and GPU-1
details; and the paper manifest promised filenames but listed only hashes. A
preliminary MiB/GiB concern was withdrawn after the reviewer re-read the corrected
15.1 and 34.3 GiB values.

Resolution: M1 was rerun with one explicit boundary for all methods—device-resident
token IDs in and CPU scores out—and all dependent timings and ratios were replaced.
DetectAnyLLM moved to the excluded lane. FourierGPT received an independent primary-
source card and preserved paper, without a supersession claim. The email now states
the 1,024-token versus historical-score accuracy limitation and uses descriptive
links. M2 now records Python, Torch, Transformers, CUDA build, NVIDIA driver, both
GPU identities, and memory. The artifact manifest now gives exact filenames and
hashes, and repository assertions have immutable file/line locators.

Second-pass verdict: all substantive fixes verified, with no further material
finding. The reviewer identified one remaining audit-record placeholder that still
said the repeat review was pending. That bookkeeping defect is resolved in this
paragraph. Final confirmation pass: PASS, with no remaining material issue.
