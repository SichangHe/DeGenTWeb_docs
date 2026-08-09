# MELD v5 benchmark design and result boundary

Run date: 2026-08-08, America/Los_Angeles.

## Question and version boundary

The benchmark asks whether the current, anonymously runnable MELD v5 artifact
fits exactly two NVIDIA RTX A6000 GPUs, remains plausibly near the fixed DW1
Binoculars batch latency at 2,048 tokens, and shows enough discrimination on the
available DW1 convenience corpus to justify a later frozen evaluation.

It does not test the paper-era model. The paper-era immutable revision
`51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808` requires companion code whose public
endpoint returned HTTP 401. The current v5 model card says earlier revisions are
different models and their scores are incomparable. The harness therefore loads
only current immutable revision
`453acf594d48f8c55c3a38bde396f9178516d817`, validates both preserved weight
hashes, and labels every result v5.

## Inputs and hypotheses

The source corpus is the read-only DW1 trial CSV at
`data/classify/cc10k/fdgpt_trial_all_df1`; its SHA-256 is
`964cf196caacaee7cb28c106e0bc7b1177a2567478ab1058dd5ee5f8228aef46`.
Of 8,170 rows, 8,022 referenced text files were locally available.

The bounded hypotheses were:

1. A single 395-million-parameter FP32 encoder will fit one A6000 at batch 8 and
   2,048 tokens.
2. Two replicas processing four documents per card will have lower batch latency
   than the fixed 7.732507-second DW1 Binoculars batch-8 result.
3. The current artifact will not be promoted unless it matches or improves the
   stored same-row Binoculars AUROC and has defensible low-FPR threshold behavior.

## Timing design

The eight longest available texts were tokenized to exactly 2,048 tokens. After
warm-up, five repetitions measured:

- one GPU, batch 1;
- one GPU, batch 8; and
- two model replicas concurrently processing four documents per GPU.

The timed boundary begins with device-resident token tensors entering the exact
model-card scoring computation and ends when detector scores reach CPU. It
excludes model loading, tokenization, and host-to-device input transfer, matching
the fixed comparator's scoring-only boundary. CUDA peak allocated and reserved
memory are reset and synchronized around each timing block. The batch-latency
ratio uses the fixed DW1 Binoculars batch latency, never a batch-1-to-batch-8
ratio.

## Accuracy design

The historical continuity screen reproduces the prior seed-42 selection of 500
human and 500 generated rows and records record-manifest and text hashes. It is
reported separately because 291 selected texts are below the v5 card's stated
100-word minimum.

The length-eligible screen includes all 4,907 available texts with at least 100
words. A deterministic seed of 20,260,808 selects 1,000 human-only calibration
rows. The disjoint evaluation set contains the remaining 2,315 human and 1,592
generated rows. AUROC is computed on the evaluation set. Thresholds targeting
one-percent and five-percent calibration-human FPR are selected without looking
at evaluation labels, then applied unchanged to evaluation. The shipped v5
thresholds are also applied unchanged to both human partitions.

Stored DW1 Binoculars and FastDetectGPT values are evaluated on identical rows,
with the documented Binoculars sign normalization. They are historical scores,
not new same-process forwards, so software and truncation may differ. The corpus
is a convenience corpus, not a frozen stratified current-generator benchmark.

## Exact run and environment

The successful run used an isolated Python 3.13 environment because the first
Python 3.14 attempt hit a documented third-party `torch.compile` incompatibility.
Both attempts' raw stdout and stderr are preserved. The successful invocation
was equivalent to:

```text
CUDA_VISIBLE_DEVICES=0,1 uv run --python 3.13 benchmark_meld.py \
  --artifact-root /ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08 \
  --scores-out benchmark_meld_scores.csv
```

`benchmark_meld_python.txt`, `benchmark_meld_packages.txt`,
`benchmark_meld_gpus.txt`, and `benchmark_meld_model_files.sha256` pin the
interpreter, packages, GPUs/driver, and every model file. Static validation is
recorded in `benchmark_meld_checks.txt`: ruff 0.14.9 passed check and format, and
basedpyright 1.36.0 reported zero errors/warnings when explicitly pointed at the
successful Python 3.13.11 environment with a Python 3.13 target. A host-default
type check is not treated as equivalent. The benchmark made no DW1 implementation
or configuration change.

## Results and decision

The two-replica 2,048-token batch-8 median was 0.626530 seconds, or 0.078316 per
document, with 2,107.07 and 2,098.52 MiB peak allocated. It fits and is 0.0810 of
the fixed Binoculars batch latency. The one-GPU batch-8 median was 1.200715
seconds with 2,682.95 MiB peak allocated.

On the length-eligible evaluation, AUROC was 0.955271 for MELD, 0.977899 for
stored Binoculars, and 0.968952 for stored FastDetectGPT. With a locally selected
one-percent-FPR threshold, MELD evaluation FPR/TPR was 0.00821/0.90201. The
shipped nominal one-percent threshold instead produced 0.090 calibration FPR and
0.08596 evaluation FPR; the shipped nominal five-percent threshold produced
0.241 and 0.23456.

V5 therefore passes the bounded two-A6000 fit and near-Binoculars speed screens,
but fails the current recommendation gate. Its AUROC is lower on the available
same-row screen, its shipped thresholds do not transfer, and it is not the model
whose paper-era accuracy was reported. The result justifies a future frozen,
stratified, same-run evaluation after version provenance is resolved; it does not
justify deployment.
