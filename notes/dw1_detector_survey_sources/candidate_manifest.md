# Frozen candidate manifest

Candidate date: 2026-08-08, America/Los_Angeles.

Candidate state: **FROZEN FOR DISTINCT ADVERSARIAL REVIEW — AWAITING A NEW
ONE-SHOT EVALUATOR**. No internal review authorizes delivery. The corrective
email remains **NOT SENT**.

## Scope and accepted chain

The owned candidate consists only of:

- `../dw1_detector_survey.md`;
- `../dw1_detector_survey_email.md`; and
- every file in this `dw1_detector_survey_sources/` directory.

The starting documentation commit is
`45191cb40963a137192795cba0dc7d10ada2f598`, the pushed rev2 semantic repair.
The accepted survey chain is preserved in Git: original survey
`d5fb118`, accuracy-first renewal `fe98a1c`, evaluator repair `f749a13`, and rev2
semantic repair `45191cb`. No DW1 implementation or configuration file is in the
candidate. A later parent-repository commit may change only the `docs` gitlink to
the pushed documentation commit.

## Repository content binding

`candidate_files.sha256` covers the two top-level documents and 64 source/evidence
files, 66 files total. It excludes itself and this explanatory manifest; the
final Git commit binds those two files. Its current frozen SHA-256 is:

`4bb11271b477f0c9d66752b2b2b895dda0ddf8309c798e59988d374e03e58136`

The ledger includes the complete earlier MELD, benchmark, integrity, coverage,
and review evidence plus this repair's composite source/result mappings,
generated audits, primary-search record, public-checkpoint benchmark source,
both raw attempts, 8,022-row CSV, independent verifier, static checks, execution
environment, and model hashes. From `docs/notes/`, the exact check is:

```text
sha256sum --check dw1_detector_survey_sources/candidate_files.sha256
```

Broad `*.txt`, `*.csv`, and `*.tsv` ignore rules apply in this repository. Every
owned ignored evidence file must therefore be force-added, and a staged-path
comparison must prove that every ledger path is present in the index. Raw CSV
bytes are bound by the ledger and must not be silently normalized.

## External public evidence binding

Canonical path:

`/ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08`

The external `MANIFEST.sha256` covers 274 files and has SHA-256:

`6aeb1d786e1c91eb6c7e3f0723d129a6a562586c57024227c7082bbbdf5f4529`

`sha256sum --check MANIFEST.sha256` passed for all 274 entries. No file or
directory in the collection is writable. It preserves the earlier 150-file
collection, every composite parent PDF, Task 3 overview and six primary system
papers, Counter Turing primary papers, bounded primary-absence responses,
official source archives, and three complete immutable public checkpoint
snapshots. The collection contains only anonymous public evidence. No PB,
credential, authenticated endpoint, persistent browser/session state, cookie
reuse, robot-challenge bypass, or human-owned tmux session was used.

## Coverage anchors

The three immutable exact-phrase exports still contain 204 raw rows and 119
unique 2025–2026 publications. `coverage_row_dispositions.tsv` maps each exactly
once. The generated row audit flags 106 titles/abstracts, resolves 69 explicit
dispositions and 50 mechanically allowlisted non-candidate classes, and returns
PASS.

A second level selects 33 overview, benchmark, shared-task, evaluation,
comparative, survey, dataset, or training-study composite sources from frozen
title/class rules. All 33 have exact inspected scopes. Twenty-six expand to 241
individual named system/version rows; the other seven have source-specific
no-qualifier reasons. Every child binds a parent, metric and scope,
primary source or bounded-absence sentinel, artifact status, disposition, and
source card. The checker requires an independent, SHA-256-bound exact inventory
of all 241 result IDs and binds every expanded parent to its E-card. Task 3 and
Counter Turing retain separate hard-coded anchor sets. It also parses and hash-
binds the machine marker under every real E-card heading to the same parent and
exact result-ID set. Eleven regression/negative controls pass, including
deletion of a non-anchor row plus a lowered mutable count, removal of a real
E-card, and wrong label, parent, or result-ID card bindings. The current audit
hashes and command are in `coverage_semantic_audit_report.txt`.

The Task 3 primary evidence separately resolves 20 qualifying submitted versions
and baselines, including Leidos, Pangram, USTC-BUPT, ALERT, CNLP-NITS, LuxVeri,
MOSAIC, Binoculars, GLTR, and OpenAI RoBERTa-large. USTC-BUPT has an explicit
bounded absence rather than an invented primary paper. Pangram is not method-
excluded from a training-data preprocessing description; CNLP is excluded for
inference-stage target normalization/rewrite.

## Benchmark anchors

The accepted MELD evidence and exact paper-era/current incompatibility are
unchanged. Current v5 remains a provenance blocker: measured evaluation AUROC
0.955271 trails stored Binoculars 0.977899, and shipped thresholds do not
transfer, despite the strong two-A6000 feasibility result.

The generalized repair executes only three complete public states:

- DetectRL-X revision `76649a0257a812a81cf36b5de9cc5f2430aeaa7f`:
  evaluation AUROC 0.953253, calibrated-one-percent-FPR evaluation TPR 0.271357,
  and 0.028899-second two-card batch;
- Desklib revision `5fdea974cd4287c61674951ec78803aa274e2fb7`:
  evaluation AUROC 0.975080, calibrated-one-percent-FPR evaluation TPR 0.896357,
  and 0.285271-second two-card batch; and
- ModernBERT revision `08f218f1d05791ad99c26ede421f69c781a50360`:
  evaluation AUROC 0.833729, calibrated-one-percent-FPR evaluation TPR 0.006281,
  and 0.300674-second two-card batch.

The score CSV has 8,022 data rows and SHA-256
`c635d2b98583f9f9bcf3917f7ecb18469185550ab66d46ff60021a977195e786`.
`verify_composite_scores.py` independently reconstructs both seeded splits and
all five methods' AUROCs and operating points. Ruff and basedpyright pass. The
first ModernBERT compilation-optimization failure is preserved; the successful
run changes only `reference_compile`, not weights or mathematical scoring. The
non-destructive layout helper verifies 25 model files and deterministically maps
the three revision-bearing external snapshots to the harness keys; the replay
command and successful layout check are preserved.

None of the three replaces Binoculars. Desklib is the only new runnable follow-up:
its local tail recall is strong, but its AUROC is 0.002819 lower, it uses a
768-token RAID-trained path, and this is a convenience corpus with historical
comparators rather than a frozen like-for-like evaluation.

## Frozen correction and no-send state

- Human-readable email SHA-256:
  `5b8ec279d73fb5da5100719c53678b4d2965652bd7f95db516a3c217425d6021`.
- Mechanical subject SHA-256:
  `73540e80f5dafef3f3cb5168ad75475f755efade636b7135ea21ccaa4fc9abad`.
- Mechanical body SHA-256:
  `a7d276ccd281f50ed68d581824612a08f829442ec2a5b5c908c2275882d9bcb5`.

The mechanical copies exactly equal the subject and body of the human-readable
draft. Status is **NOT SENT**. `delivery_plan.md` forbids delivery unless a new
one-shot evaluator passes the exact pushed candidate and the manager then
authorizes this exact frozen subject/body pair. An internal reviewer PASS is not
an evaluator PASS.

## Independent review chain

`adversarial_review.md` preserves nine distinct reviewer verdicts verbatim.
Reviews 1, 2, 4, 6, 7, and 8 remain FAIL records with their resolved findings;
reviews 3 and 5 are historical PASS records for predecessor candidate states.
The dw1eval4 verdict proves that review 5 did not test publication-internal
semantic coverage and therefore does not pass this repair. Review 6 found the
mutable-count blind spot, unbound card labels, missing manifest entries, primary-
paper identity errors, undocumented model layout, and compressed Task 3
comparability; each repair is preserved.
Review 8 found the missing filename in the subject and a label-only E-card
check. Review 9, a different fresh reviewer, independently replayed the repaired
119-publication/33-source/241-result audit and all eleven controls, challenged
the Task 3 and Counter Turing expansions and all seven no-qualifier scopes,
verified the actual E-card bindings, both integrity ledgers, benchmark evidence,
bounded conclusion, exact correction, and no-send gate, and returned **PASS —
no P1/P2 findings**. That internal PASS does not substitute for the required new
one-shot evaluator and does not authorize delivery.

## Required final verification

Before commit and after checkout of the final commit:

1. replay the semantic audit and its eleven controls;
2. replay the independent score verifier and static checks;
3. verify all 66 repository-ledger entries and 274 external-ledger entries;
4. prove the human email equals the mechanical subject/body and remains unsent;
5. prove every candidate-ledger path is staged and no unowned path is staged;
6. commit and push only owned documentation artifacts; and
7. verify the remote documentation commit and, if needed, update only the parent
   `docs` gitlink from an isolated clean worktree.
