# Durable adversarial review record

Review target: renewed DW1 detector survey candidate, 2026-08-08.

This record preserves every independent adversarial verdict in order. A later
PASS does not erase an earlier FAIL; each reasonable finding must have a concrete
resolution. Reviewer agents were read-only and did not author the candidate.

## Review 1 — FAIL

- Reviewer identity: canonical task `/root/adversarial_survey_review_1` (distinct
  read-only `reviewer` subagent).
- Review timestamp: 2026-08-08T17:04:18-07:00.
- Exact scope: complete evaluator verdict; owned survey, email, and source
  directory changes including ignored raw files; external public collection and
  `MANIFEST.sha256`; MELD v5 benchmark method and outputs.
- Inferred intended change: correct the missed recent high-accuracy MELD lead,
  preserve paper-era/current-version separation, add bounded recency
  dispositions, preserve raw evidence, and gate an unsent corrective email.

### Findings

1. **P1 — candidate not yet frozen.** `candidate_manifest.md` did not exist even
   though the delivery and preservation notes referenced it. MELD raw
   stdout/stderr, score CSV, environment manifests, Scholar TSV, and mechanical
   email files were ignored and untracked. Required resolution: force-add every
   required raw file and add a manifest binding the exact documents, raw
   evidence, external manifest, email subject/body, and reviewer artifact; then
   commit the complete set.
2. **P1 — no durable adversarial-review artifact.** Required resolution: preserve
   this FAIL with identity, scope, findings, resolutions, and verdict, then obtain
   a fresh PASS from a different reviewer after the freeze repair. The first
   reviewer must not be reused for the PASS.
3. **P3 — static-check environment ambiguity.** A host-default basedpyright run
   reports missing machine-learning dependencies and an older target. This does
   not invalidate the recorded Python 3.13 execution, but the candidate must name
   the static-check interpreter/target or make no host-level type-check claim.

### Verified by reviewer 1

- The external integrity ledger passed for all 92 files.
- All 119 deduplicated 2025–2026 arXiv-export identifiers were accounted for;
  targeted carry-forwards were explicit.
- Current MELD v5 source matched the official model-card algorithm; immutable
  hashes, 2,048-token batch/concurrency design, raw scores, AUROCs, and operating
  points recomputed.
- Paper-era/v5 incompatibility, historical-comparator limitations,
  threshold-transfer failure, exclusions, two-A6000 memory, and speed boundaries
  were honest.
- Corrective email prose was listenable, mechanical copies matched, and the fresh
  evaluator PASS plus manager-authorization no-send gate was adequate.

### Resolutions

- Finding 1: resolved by force-adding the ignored raw artifacts and creating
  `candidate_files.sha256` plus `candidate_manifest.md`; the final docs commit
  binds both. Exact staged-path and ledger checks are recorded in the manifest.
- Finding 2: this file preserves review 1. A fresh distinct reviewer is required
  below before candidate PASS.
- Finding 3: `benchmark_meld_checks.txt` now records ruff 0.14.9 and basedpyright
  1.36.0, with basedpyright explicitly pointed to the successful Python 3.13.11
  isolated interpreter and Python 3.13 target. `benchmark_meld_design.md` states
  that a host-default check is not equivalent.

Review 1 final verdict: **FAIL** until the two P1 preservation/review artifacts
are completed and a distinct fresh reviewer passes.

## Review 2 — FAIL

- Reviewer identity: canonical task `/root/adversarial_survey_review_2` (different
  distinct read-only `reviewer` subagent).
- Review timestamp: 2026-08-08T17:14:10-07:00.
- Exact scope: complete evaluator verdict; all staged candidate changes; candidate
  and external integrity ledgers; MELD benchmark source, design, raw stdout, CSV,
  and manifests; coverage exports/dispositions; preservation records; delivery
  plan and email.
- Reviewed anchors: staged survey blob
  `083a89fbdfcccedf9b2c4e46d196c457a601cc6e`; staged email blob
  `56f1c079ac756df9731c7475aa5accee7e2167a7`; staged candidate-ledger blob
  `56e144d2cd45b65104c93cd49a4527b8e959abda`; then-current external manifest
  SHA-256
  `5c6e343d1927d64e3ffe071e382147e80b0b42b27afbff789c557a1663bef0c6`.
- Inferred intended change: correct the missed MELD lead, retain paper-era/v5
  incompatibility as a blocker, provide bounded recent-result coverage, preserve
  reproducible evidence, and freeze an unsent corrective email.

### Finding

1. **P1 — newly cited coverage papers not preserved.** The disposition table
   assigned substantive decisions to 13 new primary papers, but the external
   collection held neither their PDFs nor official snapshots: `2502.04528`,
   `2502.11336`, `2504.02873`, `2504.21019`, `2505.13855`, `2508.01754`,
   `2508.13768`, `2509.22147`, `2510.12608`, `2602.01240`, `2603.05617`,
   `2604.02008`, and `2606.00016`. Raw Atom metadata and links were not enough to
   satisfy the explicit primary-artifact preservation requirement.

### Verified by reviewer 2

- Reviewer 1's index, raw-file, durable-review, and static-check remedies passed.
- Candidate ledger passed against working-tree and staged bytes, including the
  exact CRLF score CSV.
- MELD implementation, score recomputation, provenance/comparability blockers,
  two-A6000 cost, speed language, exclusions, conclusion, and no-send email gate
  were sound.
- All 119 export identifiers were dispositioned, but the then-current external
  92-file ledger was incomplete only by the 13 papers above.

### Resolution

All 13 exact public arXiv PDFs are now retained under identifier filenames.
`paper_artifacts.md` records every hash. A mechanical audit finds a retained PDF
for all 49 distinct arXiv identifiers linked by the plausible-result and targeted
carry-forward tables. The rebuilt external ledger covers 105 files and has
SHA-256
`0afacad6dc7921c2f43e794f590604be49d9464ee2e9e7a8d3c91d227cd9c989`;
all 105 entries pass. The repository candidate ledger is rebuilt after this
resolution.

Review 2 final verdict: **FAIL** until all 13 artifacts are preserved, both
manifests are refreshed, and a third distinct fresh reviewer passes. This FAIL is
not promoted or rewritten as a PASS.

## Review 3 — PASS

- reviewer identity: `/root/adversarial_survey_review_3`, distinct read-only reviewer
- timestamp: `2026-08-08T17:24:37-07:00`
- scope: complete evaluator verdict; all staged owned survey/email/source artifacts; MELD source, raw outputs, CSV, manifests, coverage exports/dispositions, delivery gate, candidate ledger, and external public collection
- reviewed candidate ledger SHA-256: `5bd694aa5fdfd7b7dc984412aeb15222199b7c6f97ded9038c25d0a50ee75eb8`
- external ledger: 105 entries, SHA-256 `0afacad6dc7921c2f43e794f590604be49d9464ee2e9e7a8d3c91d227cd9c989`

Inferred goal: repair the missed 2025–2026 accuracy-first detector screen, preserve public primary evidence and raw MELD reproduction outputs, retain MELD’s version/comparability blocker, and freeze an unsent corrective email.

Findings:

- P1: none
- P2: none
- P3: none

Verified facts:

- candidate ledger passed against working and staged bytes for all 39 entries; the staged CRLF score CSV exactly hashes to `7a37e7b7df84ab19fe915dfca5e07be7bb95ff3b44ad105cb0a5af1e1a924d63`
- external ledger passed for all 105 files, including reviewer 2’s 13 formerly missing PDFs
- all 119 exact-export 2025–2026 identifiers have dispositions; EchoPrompt, Hidden Human-Like Nature, and Steer-to-Detect are correctly explicit targeted carry-forwards
- all 49 distinct linked arXiv identifiers have a retained primary PDF, including canonical PAWN, SpecDetect, DetectAnyLLM, and WaveDetect mappings
- MELD’s paper-era/current-v5 incompatibility, paper accuracy limitations, local AUROC/threshold-transfer results, two-A6000 2,048-token batch/concurrency memory, and non-direct FastDetectGPT speed comparison are accurately bounded
- the CSV independently reproduces the recorded MELD AUROC `0.9552706839`, local one-percent-FPR operating point `0.0082073/0.9020101`, and shipped-threshold transfer failures
- retrieval, rewriting/regeneration, and multi-perturbation exclusions remain enforced
- the conclusion keeps Binoculars, makes MELD the next blocked experiment, and does not claim universal literature absence
- the listenable email is corrected and frozen; delivery requires both a fresh one-shot evaluator PASS and explicit manager authorization, with no send attempted

Required resolution: none. Append this review verbatim to the durable review record, refresh the two candidate bindings, then commit the frozen candidate.

Final verdict: **PASS**

## Review 4 — FAIL

- reviewer identity: `/root/semantic_repair_adversarial_review`, a fresh distinct
  read-only reviewer
- recorded timestamp: `2026-08-08T18:52:40-07:00`
- scope: complete evaluator verdict; fully staged owned semantic repair; all 119
  row mappings and generated audit; LM²otifs/NEULIF primary evidence; previously
  accepted method, accuracy, MELD, A6000, speed, integrity, conclusion, and
  no-send constraints; candidate and external ledgers
- reviewed candidate-ledger SHA-256:
  `8e69fac73a24574f53424b4b13767970840335012ba88ef135c7ec38ba5ad580`
- reviewed external ledger: 134 entries, SHA-256
  `f9b21e7a27383af474cc2b65a8fcdf8c33ca767e0d1d59ccddea41dd131e15b2`

### Findings

1. **P1 — semantic coverage still hid plausible high-score detectors.** The
   trigger expressions omitted “first rank,” “most performant,” and
   “near-perfect results.” Rows `2509.00623` and `2506.01702` were consequently
   unflagged and lacked individual primary-source review. Four already flagged
   high metric claims—`2507.05157`, `2505.11550`, `2503.22338`, and
   `2502.16857`—were wrongly called false positives: their missing artifact,
   low-FPR, or deployment evidence were rejection criteria, not reasons that the
   high detector claims were false positives.
2. **P2 — arbitrary catch-all codes passed.** The script checked only mapping
   kind, resolution, and nonempty text; an unknown `catch_all` disposition code
   would have validated. It needed kind-specific allowlists bound to documented
   class semantics.
3. **P2 — candidate-ledger command lacked its working directory.** Ledger paths
   are relative to `docs/notes/`, so the command printed beside the ledger failed
   when run from the source directory.

### Verified by reviewer 4

- all 45 candidate-ledger entries matched staged and working bytes when checked
  from `notes/`;
- all 134 external-ledger entries matched;
- LM²otifs and NEULIF PDFs, source cards, artifact blockers, metric boundaries,
  two-A6000 decisions, and no-run decisions were sound;
- MELD and prior accepted constraints remained intact; and
- email subject/body matched and remained **NOT SENT**, with staged paths limited
  to owned survey artifacts.

### Resolution

The six named shared-task rows now have individual dispositions, primary PDFs,
and artifact checks. A broader trigger stress test also found general detector
paper `2603.18750`; it too is individually reviewed and preserved. Three linked
official source repositories are archived at immutable commits, while their lack
of checkpoints is explicit. The trigger set now covers first-rank,
most-performant, robust/remarkable/near-perfect, accuracy-claim, broader metric,
and comparative-improvement language. The generated audit emits a
kind-specific allowlisted class definition; unknown, wrong-kind, and catch-all
codes fail. The candidate manifest gives the exact notes-relative ledger command.

Reviewer 4 final verdict: **FAIL** until these defects are repaired and a
different fresh reviewer passes. This FAIL is preserved and is not rewritten as
a PASS.

## Review 5 — PASS

- reviewer identity: `/root/semantic_repair_fresh_review`, a different fresh
  read-only reviewer
- timestamp: `2026-08-08T19:05:39-07:00`
- scope: complete evaluator verdict; fully staged owned semantic repair; all 119
  row mappings and generated audit; LM²otifs/NEULIF and all seven later-promoted
  systems; previously accepted method, accuracy, MELD, A6000, speed, integrity,
  conclusion, and no-send constraints; candidate and external ledgers
- reviewed candidate-ledger SHA-256:
  `cafc887f4811141bb067c33444813a65f466d64f413c84867cb1e44294c18839`
- reviewed external ledger: 150 entries, SHA-256
  `1b92b652294562b6f1abbad3064c2c0f2b0fa2c49ff23e30b3937d5e9cdba67c`

Inferred goal: close every P1/P2 semantic-coverage defect without disturbing
the cleared MELD benchmark, integrity, conclusion, review-chain, or unsent-email
work, and freeze the smallest public-evidence-backed candidate suitable for a
new one-shot evaluator.

Findings:

- P1: none
- P2: none
- P3: none

Verified facts:

- all 45 candidate-ledger entries matched both staged and working bytes when
  checked from `docs/notes/`, including the exact CRLF score CSV, and the staged
  candidate equalled the working candidate;
- all 150 external-ledger entries matched, and every one of the 71 distinct
  explicit or targeted arXiv identifiers had a retained primary PDF;
- the semantic audit replayed to 204 raw rows, 119 unique rows, 106 flagged
  rows, 68 explicit dispositions, 51 mechanically defined non-candidate rows,
  and PASS, with every frozen export row mapped exactly once;
- missing, duplicate, unknown catch-all, and wrong-kind mappings failed; a
  broader independent performance-language check found no unflagged high-claim
  row;
- LM²otifs and NEULIF each had a separate primary-source-backed disposition,
  artifact search, comparability analysis, two-A6000 assessment, speed
  assessment, and scientifically justified no-run decision;
- all seven systems promoted after review 4 had individual primary-source and
  artifact review, disposition, and justified no-run decision;
- the cleared MELD evidence, benchmark outputs, method exclusions, bounded
  conclusion, and external/public-access integrity remained intact;
- the human-readable email and mechanical delivery body matched exactly and
  remained **NOT SENT**, gated on a new one-shot evaluator PASS and manager
  authorization; and
- the staged paths were confined to the owned survey artifacts and contained no
  DW1 implementation or configuration change.

Required resolution: none. Append this review to the durable record and refresh
the candidate bindings; those bookkeeping changes do not alter reviewed
scientific or email content.

Final verdict: **PASS — no P1, P2, or P3 findings.**

## Review 6 — FAIL

- reviewer identity: `/root/composite_semantic_adversarial_review`, a fresh
  distinct read-only reviewer
- timestamp recorded after receipt: `2026-08-08T21:48:53-07:00`
- scope: the fully staged generalized composite repair; exact result ledgers and
  checker; composite source cards; Task 3 primary evidence; benchmark source,
  model files, execution records, and replay path; external collection;
  previously accepted constraints, conclusion, and unsent correction
- reviewed then-current candidate-ledger SHA-256:
  `90e9e65ca199f0bfd5cb21abf87f1b7be1cfe2e8c8792c77c58c1c89a9940b22`

### Findings

1. **P1 — generalized hidden-result omissions still passed.** Only Task 3 and
   Counter Turing had immutable required result IDs; the other 80 rows were
   protected only by mutable counts. The reviewer removed
   `2605.15518:mdeberta-classifier`, changed its expected count from two to one,
   and proved that `validate_composites` still passed. Every expanded source
   needed an exact result-ID set and this mutation needed a regression control.
2. **P1 — external evidence was not frozen or fully manifest-bound.** The ledger
   had 246 entries but omitted live `papers/2505.24523.pdf` and
   `papers/canonical_detectllm_2306.05540.pdf`; the former was a required
   composite parent. The collection root, `papers/`, the added PDF, and the
   manifest were writable.
3. **P1 — two primary-paper identities were wrong.** The two FastDetectGPT child
   rows cited unrelated arXiv 2305.16783 instead of 2310.05130. DetectLLM result
   URLs used correct 2306.05540, but inherited artifact names identified
   unrelated 2306.05594 bytes as DetectLLM.
4. **P1 — the benchmark was not replayable from preserved paths.** The harness
   expected `detectrlx_xlm`, `desklib`, and `modernbert` below a transient model
   root, while the collection stored only long revision-bearing directories and
   documented no deterministic mapping.
5. **P2 — source-card labels were not bound.** Any nonempty string, including
   `does-not-exist`, passed because no parent-to-card mapping was validated.
6. **P2 — Task 3 comparability was compressed.** E1 needed explicit present or
   absent text length, generators/domains, training and calibration details, and
   the split distinction that Leidos v1.0.3 leads non-adversarial results while
   v1.0.2 leads adversarial results.

### Verified by reviewer 6

- the then-current candidate ledger validated from `docs/notes/`;
- the score verifier passed all 20 metric and operating-point checks;
- the staged diff had no whitespace errors; and
- the email mechanical subject/body equality passed and delivery remained
  **NOT SENT**.

### Resolutions

- Finding 1: `coverage_expected_result_ids.tsv` independently enumerates all 96
  exact parent/result pairs and is immutably bound by a checker-constant SHA-256.
  Every one of the 19 expanded parents must match its exact set. A regression now
  deletes mDeBERTa and lowers the mutable count; it fails as required.
- Finding 2: the external manifest now covers 248 files, including both missing
  PDFs, at SHA-256
  `65275647408127937e27e2869ba6b6e0e3872ee83bfe8bd03d040ec6380f4967`.
  All entries pass and a permission audit finds zero writable files or
  directories.
- Finding 3: both FastDetectGPT rows cite 2310.05130. Correct DetectLLM
  2306.05540 is retained under its own filename and hash; the two inherited
  2306.05594 files remain only for ledger continuity and are explicitly marked
  unrelated and excluded from evidence.
- Finding 4: `prepare_composite_model_layout.sh` verifies all 25 exact model
  files, refuses an existing target, and creates the three deterministic links.
  Its successful layout replay and the full benchmark replay command are
  durable.
- Finding 5: a hard-coded map binds every expanded parent to exactly one E-card;
  the `does-not-exist` mutation is a regression failure.
- Finding 6: E1 now records the common RAID generator/domain/length/calibration
  boundary and per-system training, length, artifact, and timing evidence or
  absence. The two Leidos split winners are explicit.

Reviewer 6 final verdict: **FAIL** until these defects are repaired, the candidate
and external ledgers are refreshed, and a different fresh reviewer passes. This
FAIL remains preserved and is not rewritten as a PASS.

## Review 7 — FAIL

- reviewer identity: `/root/composite_semantic_fresh_review`, a different fresh
  read-only reviewer
- timestamp recorded after receipt: `2026-08-08T22:22:55-07:00`
- scope: the fully staged generalized composite repair, its exact 96-result
  inventory and checker, all no-qualifier composite classes, source cards,
  accepted constraints, and unsent correction

### Finding

1. **P1 — the composite selection rule still hid named high-score results.**
   Cross-dataset evaluation `2604.16607` was classified as having zero
   qualifying children because all means were below 0.90, even though Table 2
   names twelve variants with a best-dataset AUROC from 0.92 to 1.00, including
   Binoculars, three FastDetectGPT proxies, two Zippy variants, four BiScope
   variants, and two DeTeCtive variants. Personalization benchmark `2510.12476`
   likewise had zero children even though Table 2 reports six named methods at
   0.9312–0.9899 AUROC on Cohere or ChatGPT aggregates. The aggregate-only
   exception contradicted the stated rule and recreated the semantic blind spot
   before the exact-ID checker: that checker was sound only for parents already
   selected for expansion.

### Required resolution

Expand every named high cell into an individual source-mapped disposition, or
give a result-specific false-positive reason; remove the aggregate-only escape
hatch; bind the new exact IDs; add a regression for reclassifying a known
high-cell parent as a no-qualifier; refresh all generated/integrity artifacts;
and obtain another fresh review.

### Resolution

The rule now treats every named detector/submission version with a reported
evaluation/test metric at or above 0.90 on any aggregate, dataset, generator,
domain, prompt group, language, or fixed-threshold slice as qualifying discovery
evidence. It preserves the weak mean/overall/cross-slice result in that same row
instead of suppressing the child. In addition to the reviewer-named 18 rows,
the renewed audit expands five high-cell attack-study detectors, 39 English and
multilingual shared-task submission states, and one high-validation/system-source
state. A final cross-source consistency pass also expands training/precision and
author-role bias rows; the independent inventory now binds all 180 exact IDs,
and a negative
control reclassifies `2604.16607` as a no-qualifier while deleting its children;
that mutation must fail.

That 180-row state was not treated as final. A closing table-by-table pass over
all 33 sources found 61 more qualifying configurations, including additional
Task 3 versions and controls, high length/attack/domain/language slices, older
score baselines, and author-role-bias fitted models. The exact inventory now
binds 241 result IDs from 26 expanded parents; the other seven parents retain
source-specific inspected-scope reasons. LuxVeri, MOSAIC, GLTR, HC3, DetectGPT,
Neighborhood, ReCaLL, DC-PDD, and LLM-Deviation primary evidence is preserved.
The source check also rejected two provisional identifiers that resolved to
unrelated algebraic-geometry and radar papers before the external collection was
refrozen at 274 manifest entries.

Reviewer 7 final verdict: **FAIL** until these defects are repaired and a
different fresh reviewer passes. This FAIL remains preserved and is not
rewritten as a PASS.

## Review 8 — FAIL

- reviewer identity: `/root/final_semantic_coverage_adversarial_review`, a new
  read-only reviewer
- timestamp recorded after receipt: `2026-08-08T23:31:40-07:00`
- scope: the staged 241-result repair, all 33 composite sources, exact ledgers,
  actual E-card evidence, prior scientific/integrity constraints, and frozen
  correction

### Findings

1. **P1 — the required filename was absent from the correction subject.** The
   human and mechanical subjects said `Correction: newest DW1 detector evidence`
   instead of containing the required literal `dw1_detector_survey.md`.
2. **P2 — the E-card check bound only a TSV label.** The checker compared each
   result's `source_card` string to a hard-coded label but never read
   `coverage_composite_dispositions.md`. Deleting or misassociating the actual
   card evidence could therefore pass.

### Verified by reviewer 8

- both the 66-entry candidate ledger and 274-entry external ledger validated;
- the audit deterministically regenerated 119 publication rows, 33 composite
  reviews, and 241 embedded results;
- independent sampling of all seven no-qualifier PDFs and Task 3 Tables 4–5
  supported the documented 20-result Task 3 set; and
- no file was edited and no correction was sent.

### Resolutions

- The human-readable and mechanical subjects now say
  `Correction: dw1_detector_survey.md evidence`; the body and NOT-SENT gate are
  unchanged.
- Every expanded Markdown heading now contains a machine-readable marker with
  its E-card label, parent, and exact result IDs. The audit parses and SHA-256-
  binds that file, requires its 26 cards and 241 IDs to match both ledgers, and
  rejects absent-card, wrong-parent, wrong-result-set, and wrong-label mutations.
  The audit now passes eleven regression and negative controls.

Reviewer 8 final verdict: **FAIL** until these repairs are refrozen and a
different fresh reviewer passes. This FAIL remains preserved and is not
rewritten as a PASS.

## Review 9 — PASS

- reviewer identity: `/root/final_card_bound_semantic_review`, a different
  fresh read-only reviewer
- timestamp recorded after receipt: `2026-08-08T23:44:08-07:00`
- scope: the fully staged 241-result repair, all 33 composite sources, the
  actual Markdown E-card bindings and eleven controls, the correction subject,
  every accepted scientific/integrity constraint, and the no-send gate

### Independent verification

- The exact audit replay was byte-identical: 119 publications, 33 composite
  sources, 241 child results, and eleven passing regression/negative controls.
  The checker reads and SHA-256-binds the actual Markdown E-card file, parses
  its parent and exact result-ID markers, and rejects removed, mis-parented,
  wrong-set, and wrong-label cards.
- The reviewer independently checked the 20 Task 3 rows, eight Counter Turing
  rows, all seven no-qualifier source scopes, the exact inventory, primary-paper
  mappings, and the FastDetectGPT/DetectLLM identities. No hidden qualifying
  system or unsupported primary mapping produced a P1 or P2 finding.
- The 66-entry candidate ledger and 274-entry external ledger validated. The
  external collection had no missing, extra, or writable path; every staged
  path was owned and its index bytes matched the working bytes.
- The accepted MELD reconciliation, two-A6000 evidence, three-model benchmark
  and replay mapping, metric checks, public-only boundary, feasibility/speed
  constraints, bounded conclusion, and review chain remained intact.
- The subject is exactly `Correction: dw1_detector_survey.md evidence`; its
  human and mechanical subject/body copies and bound hashes agree. The draft
  remains **NOT SENT**.

The reviewer noted only an optional P3 wording nit: E1's phrase “eight
qualifying results” could be read ambiguously beside its broader 20-result
inventory, but the surrounding text defines the two scopes and the accounting
is exact. No change was required.

Reviewer 9 final verdict: **PASS — no P1/P2 findings**. This is an internal
review verdict only, not the required new one-shot evaluator verdict and not
delivery authorization. The reviewer made no edits and sent nothing.
