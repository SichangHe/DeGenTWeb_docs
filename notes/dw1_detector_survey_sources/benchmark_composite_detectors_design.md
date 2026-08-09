# Composite-source public-checkpoint screen

Run date: 2026-08-08, America/Los_Angeles.

## Scientific question

The generalized semantic repair found three previously hidden detector results
with complete, anonymous public checkpoints. This bounded screen asks whether the
exact public states fit two NVIDIA RTX A6000 GPUs, are plausibly near the fixed
DW1 Binoculars latency, and match or beat stored comparator discrimination on
identical available rows. It is triage evidence, not a new held-out benchmark.

The immutable candidates are:

- DetectRL-X X-Rob-Classifier, revision
  `76649a0257a812a81cf36b5de9cc5f2430aeaa7f`, XLM-RoBERTa, 512 tokens;
- Desklib AI text detector v1.01, revision
  `5fdea974cd4287c61674951ec78803aa274e2fb7`, custom DeBERTa classifier,
  768 tokens; and
- GeorgeDrayson ModernBERT AI detector, revision
  `08f218f1d05791ad99c26ede421f69c781a50360`, 2,048-token screen.

Different released length limits are reported rather than treated as a
like-for-like 2,048-token comparison. Each weight and all small model files are
hash-bound in `benchmark_composite_detector_model_files.sha256` and in the
external collection manifest.

## Fixed rows and splits

The harness reads, but does not modify, DW1's
`data/classify/cc10k/fdgpt_trial_all_df1`, SHA-256
`964cf196caacaee7cb28c106e0bc7b1177a2567478ab1058dd5ee5f8228aef46`.
Of 8,170 rows, 8,022 have local text. The continuity screen uses the same seed-42
500-human/500-generated selection as earlier controls. Its record-manifest hash
is `623afe670e7954fd2800dcc19486153fde1e7d9e6037cb9b03a6749f0fc7ece7`.

The main screen requires at least 100 whitespace-delimited words, leaving 4,907
rows. Seed 20260808 selects 1,000 human calibration rows; the disjoint evaluation
contains 2,315 human and 1,592 generated rows. Calibration and evaluation
manifest hashes are respectively
`ad8d52a4b91d918f3149b2ee0eff5d6bb71ce076a3fa536936991e5f9d82824b`
and `3b1259aa3415ee0a12e0769115b2aead25d89788e65471e0a88f9e597785ffa0`.
All candidates and stored comparators use the identical rows and split.

AUROC is computed from raw scores. Human-only calibration selects empirical
one- and five-percent-FPR thresholds; those thresholds are then applied once to
disjoint human and generated evaluation rows. Stored Binoculars is sign-normalized
and stored FastDetectGPT retains its existing orientation. These stored values
were not recomputed through current model processes and are labeled historical.

## Timing and memory boundary

Python 3.13.11, torch 2.9.1+cu126, transformers 4.57.3, and two 49,140 MiB
NVIDIA RTX A6000 cards were used. For each state, timing covers device-resident
token tensors entering model scoring through CPU detector scores leaving it.
Model load, tokenization, and host-to-device transfer are excluded. Five timed
repetitions follow one warm-up. Modes are one GPU batch 1, one GPU batch 8, and
two concurrent replicas with four documents per GPU. CUDA peak allocation is a
bounded model-path measurement, not total process memory or sustained load.

The fixed comparison is M1 DW1 Binoculars at 7.732507 seconds per two-card batch,
0.966563 seconds per document, 2,048 tokens, and 35,095 MiB peak allocated per
card. A candidate can pass feasibility without passing accuracy.

## Exact execution and independent verification

The preserved collection uses revision-bearing snapshot directory names, while
the frozen harness uses three short candidate keys. The non-destructive
`prepare_composite_model_layout.sh` verifies all 25 model files against
`benchmark_composite_detector_model_files.sha256`, refuses an existing target,
and creates only these deterministic symbolic links:

| Harness child | Frozen external snapshot |
| --- | --- |
| `detectrlx_xlm` | `snapshots/detectrlx-xlm-76649a0257a812a81cf36b5de9cc5f2430aeaa7f` |
| `desklib` | `snapshots/desklib-ai-text-detector-5fdea974cd4287c61674951ec78803aa274e2fb7` |
| `modernbert` | `snapshots/modernbert-ai-detection-08f218f1d05791ad99c26ede421f69c781a50360` |

The preserved-artifact replay setup and benchmark command are:

```text
cd /ssd1/sichangheagent/dw1/docs
sh notes/dw1_detector_survey_sources/prepare_composite_model_layout.sh /ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08 /tmp/dw1-rev3-models-replay
/tmp/dw1-meld-venv/bin/python notes/dw1_detector_survey_sources/benchmark_composite_detectors.py --model-root /tmp/dw1-rev3-models-replay --scores-out /tmp/benchmark_composite_detectors_scores-replay.csv
```

The layout-only replay is preserved in
`benchmark_composite_model_layout_check.txt`; it resolves each short name to the
expected immutable external directory after all model-file hashes pass.

The successful command was:

```text
cd /ssd1/sichangheagent/dw1/docs
/tmp/dw1-meld-venv/bin/python notes/dw1_detector_survey_sources/benchmark_composite_detectors.py --model-root /tmp/dw1-rev3-models --scores-out /tmp/benchmark_composite_detectors_scores.csv > /tmp/benchmark_composite_detectors_stdout.txt 2> /tmp/benchmark_composite_detectors_stderr.txt
```

The immutable model directories were copied into the external collection after
the run. The score CSV has 8,022 data rows and SHA-256
`c635d2b98583f9f9bcf3917f7ecb18469185550ab66d46ff60021a977195e786`.
`verify_composite_scores.py` independently reconstructs both seeded selections,
checks the frozen split column, and recomputes all five methods' direct/main
AUROCs and one/five-percent operating points. Its frozen run is in
`benchmark_composite_detectors_checks.txt`.

## Preserved failed attempt

The first full attempt completed DetectRL-X and Desklib, then failed when the
public ModernBERT config's `reference_compile=true` path encountered a
Transformers 4.57.3 FX/Dynamo concurrency error with two replicas. Its stdout and
stderr are preserved. The successful run changes only the in-memory ModernBERT
configuration flag to `reference_compile=false`; checkpoint weights, tokenizer,
forward mathematics, score semantics, and other candidates are unchanged. The
successful output records that execution note explicitly. This is an execution
compatibility correction, not a trained-state reconstruction.

## Results and limits

| Public state | Eval AUROC | Eval FPR/TPR at locally calibrated 1% FPR | Two-card batch seconds | Peak allocated MiB | Disposition |
| --- | ---: | ---: | ---: | ---: | --- |
| DetectRL-X X-Rob | 0.953253 | 0.00907 / 0.27136 | 0.028899 | 1,145.09 / 1,135.89 | Fast and runnable; accuracy and tail recall trail both stored comparators |
| Desklib v1.01 | 0.975080 | 0.00907 / 0.89636 | 0.285271 | 2,767.81 / 2,758.58 | Best new state in this screen; AUROC narrowly trails Binoculars, so watchlist only |
| ModernBERT | 0.833729 | 0.01037 / 0.00628 | 0.300674 | 977.07 / 967.42 | Fast and runnable; discrimination fails decisively |
| Stored Binoculars | 0.977899 | 0.01166 / 0.66080 | 7.732507 | 35,095.35 / 35,095.35 | Incumbent historical comparator |
| Stored FastDetectGPT | 0.968952 | 0.01037 / 0.75503 | not rerun | not rerun | Historical comparator |

Desklib's locally calibrated tail recall is materially higher than the stored
comparators on this convenience corpus, while its overall AUROC is 0.002819 below
Binoculars. Its training includes RAID and its 768-token path differs from DW1's
2,048-token limit. Those facts justify a runnable follow-up, not a replacement.
No screened state satisfies the fixed requirement to match or improve both
overall ranking quality and the selected low-FPR behavior on a frozen,
like-for-like evaluation.
