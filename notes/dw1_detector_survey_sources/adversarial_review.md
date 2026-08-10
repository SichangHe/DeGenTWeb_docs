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

## Review 10 — FAIL (fresh one-shot evaluator, dw1eval5)

- evaluator workspace: `/ssd1/sichangheagent/dw1eval5`
- evaluation date: `2026-08-09`, America/Los_Angeles
- verdict SHA-256:
  `83a0ae2d665fda4e549cbb573c4845db685b54fc6880b4004dbb9ae6c4102165`
- frozen next-evaluator prompt SHA-256:
  `ab0c2d2a7bddb41a7739012b18e48ce4aa2cbe6735b287c971045d3cbc30fd87`

### Findings

1. **P1 — content discovery still stopped at the composite selector.** The
   title/class rule could omit multiple high named configurations inside an
   ordinary primary detector paper. The evaluator proved this with three
   M-DAIGT systems in 2509.00623, nine classifier/feature states in 2503.22338,
   eight DeBERTa states in 2502.16857, and three Defactify systems in 2507.05157.
   Existing exact-ID controls only protected children after source selection.
2. **P2 — Leidos v1.0.4 had a false mechanism.** Its official system paper maps
   MC/v1.0.4 to an unweighted multiclass DistilRoBERTa classifier, not an
   ensemble.

### Resolution

The repair derives a content/table inventory from the primary PDF of every one
of the 119 frozen publications. It binds all PDF and exact extracted-text hashes,
then maps 537 accounts one-to-one: 241 accepted embedded results, 276 new
primary-configuration dispositions, and 20 parent dispositions. Twenty-eight
sources have paper-specific no-qualifier reasons. Immutable whole-file and exact
account-set hashes prevent a deleted row from being hidden by lowering a count.
Content anchors cover every evaluator example, and six new controls exercise the
ordinary-title omission, a non-anchor omission, artifact detachment, source-row
deletion, and Leidos contradiction. The Leidos result and E1 card now preserve
the official BC/BW/MC/MW mapping.

Review 10 remains a **FAIL** record. It does not authorize delivery, and the
correction remains **NOT SENT** pending a new one-shot evaluator and manager
authorization.

## Review 11 — FAIL

- reviewer identity: `/root/eval5_fulltext_fresh_review`, a distinct read-only
  reviewer
- timestamp recorded after receipt: `2026-08-09T04:20:02-07:00`
- scope: the first all-119-paper full-text repair, generator, exact ledgers,
  content controls, Leidos correction, integrity bindings, conclusion, and
  unsent correction

### Finding

1. **P1 — the curated full-text inventory still had a manual-list blind spot.**
   ArXiv 2509.00731 was incorrectly assigned zero accounts even though Table 1
   reports high RoBERTa, BERT, FastText, Qwen2.5-7B LoRA, and
   DeepSeek-R1-Distill-Qwen-7B LoRA results. ArXiv 2606.18946 was a second
   counterexample: its tables name POGER, SeqXGPT, SenDetEX, SenFlow, and four
   SenFlow ablations, including 0.924-0.940 macro F1. Hashing a hand-curated
   account list protected only already selected rows; it did not prove complete
   content discovery.

### Confirmed by reviewer 11

- The four dw1eval5 examples had separate complete rows and text anchors.
- Leidos v1.0.4 was correctly repaired to the unweighted multiclass
  DistilRoBERTa classifier.
- The then-current audit and generator were reproducible, both integrity
  ledgers passed, the accepted benchmark evidence was unchanged, and the exact
  correction remained **NOT SENT**.

### Resolution

The nine Chinese encoder/LoRA states and eight SenFlow-related states now have
individual table evidence, mechanisms, scope gates, artifact status, and
dispositions. Rechecking the former zero/parent partition added five
2501.14288 architecture stages and both LuxVeri ensembles. A final all-paper
table pass then caught 17 more narrow-cell rows that weak aggregates had hidden:
ten TELL comparators, five late-stage stability baselines, and ReMoDetect plus
ImBD in the LAPD paper. The repaired exact inventory has 805 accounts: all 241
accepted embedded results and 564 primary-paper configurations, with only six
source-specific table-derived zero-account decisions. Content anchors bind the
new per-paper ID sets to extracted table text, and lowered-count/content-
detachment controls cover both the non-English and narrow-domain omissions.

Reviewer 11 final verdict: **FAIL** until the expanded repair is frozen and a
different fresh reviewer passes. This FAIL remains preserved and is not
rewritten as a PASS.

## Review 12 — FAIL

- reviewer identity: `/root/eval5_final_fulltext_review3`, a different fresh
  read-only reviewer
- timestamp recorded after receipt: `2026-08-09T04:47:06-07:00`
- scope: the staged 119-paper/805-account repair, result-specific mechanisms,
  Leidos, audits and integrity bindings, accepted benchmark evidence,
  conclusion, and unsent correction

### Finding

1. **P1 — DNA-DetectLLM's parent exclusion leaked onto eight baselines.** All
   15 arXiv 2509.15550 rows carried `exclude_regeneration`, including BiScope,
   Entropy, Likelihood, LogRank, DetectGPT, FastDetectGPT, Binoculars, and
   Lastde++. The primary paper distinguishes those comparison mechanisms from
   DNA-DetectLLM's iterative token repair. A complete account with a false
   inherited mechanism is not a valid result-specific disposition.

### Confirmed by reviewer 12

- Isolated replay returned 119 sources, 805 accounts, 241 embedded results, 564
  primary results, and 23 passing controls.
- The generated ledgers reproduced exactly; Leidos v1.0.4 remained the
  unweighted multiclass DistilRoBERTa state; both integrity ledgers passed; and
  the exact correction remained **NOT SENT**.

### Resolution

The eight baselines now carry their actual supervised or score-based mechanisms.
BiScope, Entropy, Likelihood, LogRank, FastDetectGPT, Binoculars, and Lastde++
are evidence-rejected; DetectGPT keeps its separate multi-perturbation
exclusion. Only the seven actual DNA-DetectLLM repair/model-pair states retain
the regeneration exclusion. Exact Table 1/Table 2 evidence is separate for
every baseline and repair-order state, a hard-coded code anchor protects the
partition, and a mutation now rejects restoring the inherited regeneration
blocker.

The same systematic check corrected DP-Net arXiv 2504.21019: its uniform and
Gaussian embedding noise is training-only, so neither state is an inference
multi-perturbation pipeline. Their 85.48%/86.10% seven-domain average accuracy,
missing frozen state, missing low-FPR evidence, and missing fixed A6000 timing
leave both evidence-rejected without changing the conclusion.

Reviewer 12 final verdict: **FAIL** until these repairs are refrozen and a
different fresh reviewer passes. This FAIL remains preserved and is not
rewritten as a PASS. The reviewer made no edits and sent nothing.

## Review 13 — PASS

- reviewer identity: `/root/eval5_final_fulltext_review4`, a different fresh
  read-only reviewer
- timestamp recorded after receipt: `2026-08-09T05:09:19-07:00`
- scope: the fully staged eval5 successor repair, including every full-text
  account, result-specific exclusion, Leidos, all accepted benchmark and
  integrity evidence, conclusion, and unsent correction
- reviewed candidate-ledger SHA-256:
  `9982ac6c6dd85563f76b9dbaa8beff8a97d4a189f7294e69b114896e210a8720`
- reviewed external-manifest SHA-256:
  `ef79a70d6946056ae1fa6d92c2ef340d94e60f8218ecce31aa61e4fc8a89828a`

### Independent checks

- The reviewer regenerated 119 sources, 805 exact accounts, and 564 primary
  rows in isolation. All generated bytes matched the staged ledgers.
- The reviewer reran the audit in isolation. Its three generated audits matched
  byte-for-byte, and all eleven composite plus thirteen full-text controls
  passed.
- All 72 candidate-ledger entries and all 288 external-manifest entries, the
  external path set, and the read-only freeze passed.
- The primary PDFs supported the repaired DNA-DetectLLM baseline partition,
  DP-Net's training-only noise, Leidos v1.0.4's unweighted multiclass
  DistilRoBERTa mechanism, and the separate LM²otifs and NEULIF dispositions.
- The reviewer challenged the original eval5 omissions, Chinese encoder/LoRA
  states, SenFlow, TELL, late-stage stability, LAPD/ReMoDetect/ImBD, LuxVeri,
  mixed-mechanism parents, benchmark reconstruction, owned-path boundary, and
  conclusion. No reasonable P1/P2 finding remained.
- The human draft equalled the mechanical subject/body and remained **NOT
  SENT**. No file, commit, remote, mail, or external artifact was changed.

Reviewer 13 final verdict: **PASS — no P1/P2 findings**. P3: none. This internal
PASS freezes the candidate for a new one-shot evaluator; it neither substitutes
for that evaluator nor authorizes delivery.

## Review 14 — PASS

- reviewer identity: `/root/eval6_final_frozen_review14`, a new distinct
  read-only reviewer
- timestamp recorded after receipt: `2026-08-09T09:09:47-07:00`
- authoritative eval6 verdict SHA-256:
  `972eb1cc78ee5ee368b9ead9dc805a1787f1797b2f9de089cd57204fb44a2ed7`
- frozen next-evaluator prompt SHA-256:
  `67e3c2eccad5aca651d4af1218d94c82c1b551b9b2d6e8f5c3e49fe588f29d4e`
- scope: the fully staged eval6 successor repair, all 119 primary PDFs, the
  independent raw-table discovery and resolution ledger, every fitted-state
  repair, all accepted constraints and benchmarks, the direct nonrecursive
  byte bindings, conclusion, and exact unsent correction

### Direct reviewed hashes

- survey:
  `5e0d44d57060cb99e8ebfe2aad3b2d007d5fb41b47ac5370b12371bd4f3cc47c`
- human-readable email:
  `fb3bf756779ab210baf13162b2302d2bdeab02339b9dcc39f0a4d4894be1fc3b`
- inventory generator:
  `4646a3de8de101fbf6770ebf59bed1d0eda4bfaa7d27d1d49bb7d3462524392c`
- table scanner/resolver:
  `8170995d958fb3da46657db18e4f46557a6732e78c576a65996177d51f0faaee`
- audit program:
  `22d1f87cb0a52c6d48069c55cdea5c272c9a54a8da6b1cb7faa49cdc51d616b5`
- primary-result dispositions:
  `9bd6434060456233794f7d5d9b1b7e6c22d7bb9ea1689df3b7f3c7ddc00a0aec`
- table candidates and resolutions, respectively:
  `0460babd82a2aba738e83d53b978f464f0e546305037e92d03a565ab47e045dd`
  and `296a40b62dd17c828f9dc959a1667a5465803a333efd9d3bf03b086c24033a48`
- generated semantic, embedded-result, and full-text-account audits,
  respectively:
  `942f693a064e4a4302b410cb0c41cb4e3437ee8e9259674038cf4688a9e0db49`,
  `de74100cbd56d13cd0f2047af41557d1228d90648e066c5cc9cfb32e7369ebc8`,
  and `9c05a97c866e508349d2ccaba8d649a6f5e4be739e4ad4c80cf46a91b8808ce3`
- generated audit report and environment, respectively:
  `05781765f137bda48199f1465abdbfb1b494f256d7f95f82d918a8716d59954f`
  and `74f99fda8d74376db2c48bcc2df15856750c550a8e89d5a2363e0e9e7181e767`
- source cards:
  `c1a021fde1aa32e5fb7cc2b2b739cab3a1bda3e140ec289c4c5717e4e4beff91`
- mechanical delivery subject and body, respectively:
  `73540e80f5dafef3f3cb5168ad75475f755efade636b7135ea21ccaa4fc9abad`
  and `43fd5a9c4d35e0bd8edfc3ee3a100701579c2f84bacb1ab074f530b80c3df7a6`
- 74-file candidate ledger and 76-entry direct review-subject ledger,
  respectively:
  `cd3a03c28bcb492e1a9633d6b25584150eba5a9024cd799f3d72bf49a74e5b0a`
  and `af49e1af8f4a2fb188783fc206bc84ae9725a9246cb74af3919c8adc4052e243`
- external README and 288-entry manifest, respectively:
  `e44041d2fd53fe18784bc72bcfe7668f0edb46cd27a712ca797ff0edecf51c98`
  and `1d3537f1833a9463a9eb1399bd45f46ae2056cf8edef9423a67563254a8293b3`
- staged index tree before this review record was appended:
  `244f33c1bbbb433535c98fc0b97b452a105b1cb2`

### Independent checks

- The isolated generator reproduced 119 sources, 958 accounts, and 695 primary
  rows; all four generated inventories matched byte-for-byte.
- The independent PDF scanner reproduced 4,860 candidates with zero unresolved
  rows; both candidate and resolution snapshots matched byte-for-byte. The
  reviewer challenged grouped headings, aliases, duplicate operating points,
  false-positive reasons, and content-discovery edge cases rather than relying
  only on the required fixtures.
- The semantic audit reproduced all three generated audit files, its report and
  environment byte-for-byte. All eleven composite and twenty full-text controls
  passed.
- The reviewer directly checked PAWN's 34 accounts, including RADAR-FT and the
  five-epoch M4 RoBERTa state; all 21 distribution-shift accounts, including the
  four separately trained Vanilla states; and all 15 READER accounts, including
  distinct READ and target-adapted ImBD states. The eval5 fitted-state repairs,
  Task 3 and Leidos, Counter Turing, LM2otifs, NEULIF, MELD, mixed exclusion
  boundaries, generalized comparison tables, and no-account reasons also passed.
  No per-result disposition inherited an inapplicable parent exclusion.
- The score verifier reproduced all 8,022 rows and 20 benchmark checks. The
  scientific comparison remained bounded to keeping Binoculars while retaining
  Desklib as the only runnable follow-up.
- All 74 candidate-ledger files and the 76 direct review-subject entries passed.
  The latter is nonrecursive and remains valid when only this review record is
  appended. All 288 external entries and the exact live path set passed, with
  no writable file or directory.
- The staged scope contained 29 changed owned paths, no unstaged candidate
  bytes, no untracked file, and no diff-check error. The exact subject is
  `Correction: dw1_detector_survey.md evidence`; the human body matched the
  mechanical body, and the correction remained **NOT SENT**.

The reviewer reported one nonblocking P3: an expanded static-check scope would
reformat the three audit scripts and basedpyright reports four list-invariance
annotations in `audit_coverage.py`. Runtime replay, audit output, and scientific
content are unaffected. Reformatting or type-only refactoring was not added to
this minimal evaluator repair.

Reviewer 14 final verdict: **PASS — no P1/P2 findings**. This is an internal
review verdict only. It does not replace a fresh one-shot evaluator, authorize
delivery, or change the correction's **NOT SENT** state. The reviewer made no
edit and sent nothing.

## Review 15 — FAIL (fresh one-shot evaluator, dw1eval7)

- evaluator workspace: `/ssd1/sichangheagent/dw1eval7`
- evaluation date: `2026-08-09`, America/Los_Angeles
- evaluated documentation commit:
  `c9968e74eb0de03151e7c1d563f8145edb12505b`
- evaluator verdict SHA-256:
  `b90483ac670a29a0dde34a3e4420d0b5b7ee7fe1943b93395b9f72392882994f`
- frozen successor prompt SHA-256:
  `929e4ec96c33878916e44a8d2ca1a8875dd57ce0c1b2a6946ad4b520d5e09d0e`

The evaluator preserved the accepted scientific, benchmark, integrity, and
no-send work but found four remaining defects. First, the independent scanner
recognized only Arabic-numbered tables and covered only 105 sources; direct PDF
inspection proved 29 omitted accounts in Roman-caption tables or Figure 4 of
arXiv 2605.16107, 2604.02008, 2510.02319, and 2508.11933. Second, the recorded
Python 3.13 replay command contradicted an environment file produced by Python
3.10. Third, Review 14 did not directly hash `candidate_manifest.md`. Fourth,
four ignored bytecode-cache files made the live owned directory broader than
the committed candidate. The evaluator also recorded nonblocking Ruff-format
and basedpyright findings.

Review 15 remains a decisive **FAIL** and authorizes no delivery. Its repair is
limited to generalized Roman/figure/zero-yield discovery, exact replay
environment, direct final-manifest review binding, and a genuinely clean owned
scope. No email was sent.

## Review 16 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval7_final_manifest_review16`
- timestamp recorded after receipt: `2026-08-09T11:25:17-07:00`
- reviewed candidate-manifest SHA-256:
  `6f644af04ed77ca934c2760dd9efe42788d41ec2f4cfc110a48e8b527e3d01f1`
- 75-file candidate-ledger SHA-256:
  `ab3aa2d255a0ae2aa2d1515ec82fcd1d329f85c22a2db98fa1bd2b794090912b`
- 77-entry review-subject-ledger SHA-256:
  `d0d28c4b65a4f1df438f42022d241923475893b03052f99f159858a8c16f2349`
- 288-entry external-manifest SHA-256:
  `6c10a9aba91deddec49773068dadf825224fdbbaca2830bfd65ca4b6dc88b01e`
- frozen next-evaluator prompt SHA-256:
  `929e4ec96c33878916e44a8d2ca1a8875dd57ce0c1b2a6946ad4b520d5e09d0e`
- staged index tree before this review record was appended:
  `b894263ef615e1445a5a5737e5247b55a369b51a`

The reviewer verified both ledgers, the clean 79-file owned live scope, the
owned-only staged diff, the immutable 288-file external path set, exact unsent
subject/body bytes, the 8,022-row score verifier, Ruff and basedpyright, and an
isolated Python 3.13.11 replay. That replay reproduced 119 sources, 987
accounts, 724 primary rows, 5,010 discovery rows, and all 35 controls. The 29
Roman/Figure-4 repairs and every account in the fixed predecessor-zero-yield set
had direct evidence.

The reviewer nevertheless found a generalized P1. ArXiv 2602.11871 declared
six FastDetectGPT/Binoculars scorer accounts but its discovery scope contained
zero candidates. Table 1 reports qualifying AUROC values for the Llama,
Mistral, and Qwen configurations, while the AUROC definition appears only in
Appendix K; the scanner wrongly required a metric header on the same page.
Across the complete inventory, only 623 of 987 accounts appeared in any
candidate target, and validation required direct evidence only for a fixed
96-account predecessor subset. The reviewer required document-spanning metric
context, direct same-parent evidence for all qualifying accounts, and an
off-page-metric negative control.

Review 16 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or commit. The reviewer made no edit and sent nothing.

## Review 17 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval7_final_manifest_review17`
- timestamp recorded after receipt: `2026-08-09T11:54:12-07:00`
- reviewed candidate-manifest SHA-256:
  `284442f740eb7503b337fd42888209c82a44bc2bb949967c2e87f688a3a7b0b1`
- 75-file candidate-ledger SHA-256:
  `fd9c02d6a7b7878c59e3bb256f3701114e8b1d3c8fe7ec6e0ab998ff8d8f0e0a`
- 77-entry review-subject-ledger SHA-256:
  `b6133d1f25a4e322b6c453d2927d22cb7e3b61197a82c14ecf70875b88905ec8`
- 288-entry external-manifest SHA-256:
  `59d702dfb9ff1a8bebc1563bacc4b37f63dd02828d88068eed8712144e43474f`
- frozen next-evaluator prompt SHA-256:
  `929e4ec96c33878916e44a8d2ca1a8875dd57ce0c1b2a6946ad4b520d5e09d0e`
- staged index tree before this review record was appended:
  `d97f8e6e85606f8f0d735df0fbbaf7b3fe858a54`

The reviewer verified the clean owned scope, both ledgers, the immutable
external collection, and the exact unsent delivery bytes. It then found that
the generalized direct-evidence completion still allowed a false semantic
join. Candidate `2501.11012:f776877b6c242dd4` was an Advacheck English row,
yet it was made evidence for Unibuc-NLP and 30 unrelated English and
multilingual accounts. Unibuc-NLP's qualifying 94.1% PeerReview accuracy is
established only by joining its rank-two identity in English Table 4 to the
rank-two metric row in Table 8. Neither side of that join was represented or
validated by the chosen candidate; the desired qualifier appeared only in a
free-text reason.

The reviewer required structured per-account evidence for both sides of every
rank/configuration join and validation of parent, task track, rank or
configuration, account identity, and qualifying metric. It also required
negative controls that detach or mutate either side. The reviewer expressly
retracted a tentative working-directory concern after confirming the current
candidate-ledger command is correct; no P2 remained.

Review 17 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or commit. The reviewer made no edit and sent nothing.

## Review 18 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval7_final_witness_review18`
- timestamp recorded after receipt: `2026-08-09T14:57:15-07:00`
- reviewed candidate-manifest SHA-256:
  `3f91ca928a6a955723e76f9aee51254cb563b44e9cccaec07c50549e88cbea3a`
- 76-file candidate-ledger SHA-256:
  `37cda938250d985628e027d79beba1be164865484d74da640f6ebc746c07d82f`
- 78-entry review-subject-ledger SHA-256:
  `d5648ebc3898e16ec785b82e3afab9d4d4228e3bcb7217f3005ff5d3d2833f31`
- staged index tree before this review record was appended:
  `1b128173c4b566ba283c4abf5db9099bf7cbb129`

The reviewer replayed the 119-PDF extraction and semantic audit under CPython
3.13.11, reproducing 987 account witnesses and all 48 then-current controls.
The 8,022-row score verifier, 25-file layout verifier, 288-file read-only
external collection, direct manifest bindings, and exact NOT-SENT email bytes
also passed substantive inspection.

The reviewer nevertheless found a P2 owned-scope defect. The staged source
scope contained 78 files, while the live source directory contained an ignored,
uncommitted 697,266-byte legacy `coverage_account_content_witnesses.tsv`. Its
presence meant the frozen candidate did not equal the complete live owned scope.
The file was obsolete and was removed; no ignored or untracked replacement was
created. Review 18 final verdict: **FAIL**. It authorizes no delivery, email,
lifecycle closure, or commit. The reviewer made no edit and sent nothing.

## Review 19 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval7_final_clean_review19`
- timestamp recorded after receipt: `2026-08-09T14:57:15-07:00`
- reviewed candidate-manifest SHA-256:
  `3f91ca928a6a955723e76f9aee51254cb563b44e9cccaec07c50549e88cbea3a`
- 76-file candidate-ledger SHA-256:
  `37cda938250d985628e027d79beba1be164865484d74da640f6ebc746c07d82f`
- 78-entry review-subject-ledger SHA-256:
  `d5648ebc3898e16ec785b82e3afab9d4d4228e3bcb7217f3005ff5d3d2833f31`
- staged index tree before this review record was appended:
  `1b128173c4b566ba283c4abf5db9099bf7cbb129`

The reviewer confirmed a clean 78-file live/indexed scope, byte-identical
CPython 3.13.11 replay, 119 sources, 4,808 content candidates plus 119 scope
summaries, 987 account witnesses, all 48 controls, both repository ledgers, the
external collection, score and model-layout verifiers, accepted scientific
constraints, and the NOT-SENT correction. It found no other P1/P2.

The decisive P1 was a generalized Unicode-metric blind spot. ArXiv 2505.11550
reports three qualifying Table 2 architectures at F1 0.949, 0.994, and 0.974,
but its extracted metric label is mathematical Unicode `𝐹 1`. The scanner
recognized only ASCII `f1`, emitted zero raw candidates for the paper, and let
all three accounts survive only through inventory-driven text witnesses with
blank raw-candidate IDs. An unlisted configuration in the same format would
therefore remain invisible. The repair normalizes mathematical metric glyphs,
directly resolves all three rows, rejects unsupported account-bearing
zero-yield sources, and adds source-independent format controls plus a direct
witness-detachment control.

The reviewer also recorded a nonblocking static-analysis observation. The
candidate-manifest wording is now narrowed to the score verifier and its
recorded Ruff 0.14.9/basedpyright 1.36.0 checks; it no longer implies that the
expanded audit scripts pass a newer unpinned tool release. Review 19 final
verdict: **FAIL**. It authorizes no delivery, email, lifecycle closure, or
commit. The reviewer made no edit and sent nothing.

## Review 20 — PASS (distinct read-only reviewer)

- reviewer identity: `/root/eval7_final_unicode_review20`
- timestamp recorded after receipt: `2026-08-09T15:17:37-07:00`
- reviewed candidate-manifest SHA-256:
  `b2bad2b7fffdaad9ea43ffc65297e3eecd09fb7a52bcb86d06797095c3ea6ce3`
- 76-file candidate-ledger SHA-256:
  `5553cf03754a967459e89ff9a47bf95248caaa2f465da16a648ba2c37d06d348`
- 78-entry review-subject-ledger SHA-256:
  `a77ee6245431ac39364193bf0e1bd5d93e2e50ece4cbdcf069890969336a6bbc`
- 288-entry external-manifest SHA-256:
  `59d702dfb9ff1a8bebc1563bacc4b37f63dd02828d88068eed8712144e43474f`
- reviewed staged index tree before this review record was appended:
  `611a862d7c936f8778dc47071a689eec68d254f6`

The reviewer independently reconstructed the index-only candidate and replayed
the exact CPython 3.13.11 audit byte-for-byte: 119 sources, 4,812 content
candidates plus 119 summaries, 987 witnesses, and 51 controls. A novel
unregistered mathematical-Unicode F1 row was discovered without the account
inventory, while a matched non-metric mutation was rejected. The three arXiv
2505.11550 Table 2 architectures bound directly and individually to 0.949,
0.994, and 0.974; detaching their raw witness or required resolution failed.
The generalized zero-yield guard also rejected an account-bearing non-required
fixture, and the newly surfaced `Life Sciences 99` count retained its explicit
non-detector false-positive decision.

The reviewer also verified every accepted Roman-table, figure, off-page metric,
shared-task rank, column, vertical-group, weak-state, full-table, LM2otifs,
NEULIF, Leidos, DNA-DetectLLM, and DP-Net binding; all 76 repository-ledger and
78 review-subject entries; the exact 288-file read-only external path set; the
8,022-row score verifier and 25-file model-layout verifier; and the clean 78-file
live/indexed owned source scope. No ignored, untracked, bytecode, unstaged owned,
or unowned staged byte was present. The human-readable draft and mechanical
subject/body remained exact and **NOT SENT**.

Review 20 final verdict: **PASS — no P1/P2 findings**. The reviewer made no edit
and sent nothing. This internal PASS completes the required adversarial review
but does not authorize email delivery; the one-shot evaluator and manager gate
in `delivery_plan.md` remains binding.

## Review 21 — FAIL (fresh one-shot evaluator, dw1eval8)

- evaluator workspace: `/ssd1/sichangheagent/dw1eval8`
- evaluation SHA-256:
  `bcbcd8254d81ae795c72b9dd5e235aa02b77da2014194e5223be94c4e11e6076`
- frozen next-evaluator prompt SHA-256:
  `b590f3acc96008444d21ffb0efa483b9c5511d209c15e325e459df311886370a`
- evaluated documentation commit:
  `c4246ad56aaf90461584de5b6afd0ae7c8104b44`

The evaluator preserved all accepted scientific, coverage, benchmark,
integrity, environment, scope, conclusion, and no-send repairs, but found two
remaining P2 defects. The manifest-bound external README advertised 6,029
result candidates even though exact replay derived 4,812 result candidates plus
119 summaries, or 4,931 rows. Five arXiv 2607.03680 account witnesses also used
the unrelated Table 2 Anchor value 92.1 instead of their own Table 4 or Table 11
row and column: the two `Vanilla + extra` states at 91.5 and 88.2, and the three
held-out IntelLabs pooled states at 0.968, 0.970, and 0.997. Review 20 had not
challenged either contradiction, so it could not pass the evaluated candidate.

Review 21 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or repair outside the recorded successor scope. The evaluator changed
no candidate byte and sent nothing.

## Review 22 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval8_final_metric_review22`
- timestamp recorded after receipt: `2026-08-09T17:19:17-07:00`
- reviewed candidate-manifest SHA-256:
  `0f8bc08dd84569be55106be2e3d6acd9ee8fcbd2c36fe3691eaf452c08b1262a`
- 76-file candidate-ledger SHA-256:
  `e3970f319151166d95f59d3fd9a56b14708341b86fd698671ae611aec13496a3`
- 78-entry review-subject-ledger SHA-256:
  `161b2fabb90fcfb2a7857dc0080ed48919b94834ede18b7913bd677236acd6fc`
- 288-entry external-manifest SHA-256:
  `e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`
- reviewed staged index tree before this review record was appended:
  `55cd82d7542e10415cec08925d87efdb95bf12e1`

The reviewer independently reproduced the CPython 3.13.11 inventory,
discovery, audit, and all 58 then-current controls byte-for-byte: 119 sources,
987 accounts, 724 primary-result rows, and 4,812 result candidates plus 119
summaries. It confirmed the corrected external README equation, the five exact
arXiv 2607.03680 Table 4/Table 11 values, both repository ledgers, the 288-file
read-only external collection, and the exact **NOT SENT** correction.

The decisive P2 was a generalized non-direct witness ownership defect. The GCN,
GAT, Graph Transformer, and GPS accounts under arXiv 2607.14905 all cited the
Longformer Table 2 candidate and its 0.97 value, rather than an
architecture-owned row and column. The validator also accepted a rekeyed GCN
value changed from 0.97 to Longformer's neighboring 0.96 and a PAN12 recall
witness changed from 0.9602 to the neighboring 0.9041 F1 cell. Thus proximity,
locator, and digest checks did not prove semantic column ownership.

The repair gives the four graph architectures exact Table 2 row/configuration
and column witnesses, gives PAN12 an exact Table 1 recall-column witness,
requires their raw claim/result candidates to target the corresponding account,
and compares every supplied witness with a fresh canonical PDF derivation.
Three new negative controls preserve the reviewer's wrong-column and complete
wrong-row substitutions. The reviewer's nonblocking P3 also prompted removal
of the overbroad basedpyright-clean claim for the expanded audit scripts; the
recorded benchmark/verifier claim remains unchanged.

Review 22 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or commit. The reviewer made no edit and sent nothing.

## Review 23 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval8_final_metric_review23`
- timestamp recorded after receipt: `2026-08-09T17:42:44-07:00`
- reviewed candidate-manifest SHA-256:
  `82b75042c59903c54451a225879b8c9cf8a67d28f473efb34c5e2aeaaaa335ce`
- 76-file candidate-ledger SHA-256:
  `677d1053973806f310223790dd43763781f2a0295899dca5d9dd6abb025b91b1`
- 78-entry review-subject-ledger SHA-256:
  `c571f85db0b6915640d2c3db5fa56af47dcf653c872e9870b30a941740a214e7`
- 288-entry external-manifest SHA-256:
  `e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`
- reviewed staged index tree:
  `861dff7a775c87658e02608d25ceb1b8bdc81282`

The reviewer reconstructed the staged index and reproduced the complete build,
discovery, and audit byte-for-byte under CPython 3.13.11: 119 sources, 987
witnesses, 4,812 result candidates plus 119 summaries, and 61 controls. Direct
PDF inspection confirmed the five arXiv 2607.03680 Table 4/Table 11 cells, all
four arXiv 2607.14905 architecture-owned Table 2 cells, and PAN12's 0.9602
Recall column. Both repository ledgers, the 288-file read-only external path
set, scope, benchmark, exact-email, and no-send checks otherwise passed. No
other P1/P2 was found.

The sole P2 was stale survey prose: the evidence note still said 58 controls
although the generated audit, design, and manifest correctly reported 61. The
survey now says 61, and both direct ledgers were regenerated. The reviewer also
recorded a nonblocking P3: basedpyright with the successful benchmark Python
environment reports zero errors but 76 warnings, whereas the preserved raw
check used the separately recorded `--pythonversion 3.13` command and reported
zero warnings. The final manifest therefore continues to limit the clean
basedpyright claim to that exact recorded benchmark/verifier check and makes no
such claim for the audit scripts.

Review 23 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or commit. The reviewer made no edit and sent nothing.

## Review 24 — PASS (distinct read-only reviewer)

- reviewer identity: `/root/eval8_final_metric_review24`
- timestamp recorded after receipt: `2026-08-09T17:58:33-07:00`
- reviewed candidate-manifest SHA-256:
  `4fdacaabac3c3dd28fdd99d0a16b12f2f00f4bbd97a3b7d055471fa228c923b9`
- 76-file candidate-ledger SHA-256:
  `8217d71a51c9ed8430b006edc852e67c46435aa53403d5c92601331621b2e32a`
- 78-entry review-subject-ledger SHA-256:
  `1093ad9665835c6f546d4154fca9f99e13c0d320d43f26360ff1adead4608152`
- 288-entry external-manifest SHA-256:
  `e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`
- external README SHA-256:
  `314cb6da006c60b790ebbaee49c18ddab59e9bddcc83adf3bf4326d572bc49ac`
- reviewed staged index tree before this review record was appended:
  `0881839b96502cc157e1c48be27e17057a1960d0`

The reviewer independently reconstructed the frozen index and reproduced the
complete CPython 3.13 build, discovery, witness generation, and audit
byte-for-byte: 119 sources, 987 accounts and source-derived witnesses, 724
primary-result rows, 4,812 content candidates plus 119 source summaries, and
all 61 controls. Both repository ledgers verified. The external manifest
matched the exact 288-file read-only path set, and no ignored, untracked,
bytecode, unstaged owned, or unowned staged file was present.

Direct inspection of the bound PDFs confirmed the exact arXiv 2607.03680 Table
4 values 91.5 and 88.2 and Table 11 values 0.968, 0.970, and 0.997; the unrelated
Anchor 92.1 row cannot satisfy them. It also confirmed the four arXiv 2607.14905
architecture-owned Table 2 values 0.68, 0.75, 0.78, and 0.78 and the arXiv
2608.03859 PAN12 recall value 0.9602 rather than its neighboring 0.9041 F1
cell. Canonical regeneration and the wrong-value, column, complete-row,
candidate, locator, and identity controls proved exact metric ownership.

The reviewer additionally confirmed the mechanically derived external README
equation, `4,812 + 119 = 4,931`; the absence of stale control totals in the
final subject artifacts; the accepted scientific, benchmark, integrity,
environment, and delivery constraints; the exact correction subject/body; and
the binding **NOT SENT** gate. Its only observation was a nonblocking P3 that
the manifest correctly limits its clean basedpyright statement to the exact
recorded benchmark/verifier command.

Review 24 final verdict: **PASS — no P1/P2 findings**. The reviewer made no
edit, stage, commit, external-artifact change, email, or delivery attempt. This
internal PASS completes the required adversarial review but does not authorize
email delivery; the fresh one-shot evaluator and manager gate in
`delivery_plan.md` remains binding.

## Review 25 — FAIL (fresh one-shot evaluator, dw1eval10)

The fresh evaluator inspected documentation commit
`9a1b52ae76e20baeb54f0ea242108445e31cfb6f`, independently replayed the frozen
119-source audit and 61 controls, verified both repository ledgers and the
288-file external collection, and preserved every accepted scientific,
benchmark, integrity, public-access, and NOT-SENT finding. Its durable verdict
is `/ssd1/sichangheagent/dw1eval10/evaluation.md`, SHA-256
`09d22acbf56e4acbf57c94b568fdca5191e62514d90393bad573ac6dbd05c642`.

The decisive P2 was a generalized source-ownership failure in the predecessor
witness layer. All 225 `same_window` and 95 generic
`table_configuration_join` records were proximity or configuration joins that
did not prove that the named account owned the selected result row, numeric
column, and training state. The evaluator demonstrated concrete leakage from
fine-tuned DeBERTa into TF-IDF and zero-shot DeBERTa accounts and from base
ModernBERT into the MCGrad state. It specifically required exact Figure 4,
Table 4, Table 8, and Table 9 ownership and negative substitutions for a wrong
row, wrong result column, and wrong training state. The evaluator found no
independent P1. Its basedpyright and Poppler observations remained nonblocking
P3s.

Review 25 final verdict: **FAIL**. Review 24 therefore does not pass this repair
or authorize delivery. This successor preserves the complete prior chain and
replaces every affected predecessor witness with a source-owned account,
identity row, result row or figure, exact metric column, and method/training
state binding. A distinct read-only reviewer must independently challenge the
fully frozen successor before commit; neither that internal review nor this
repair authorizes email delivery.

## Review 26 — FAIL (distinct read-only reviewer)

- reviewer identity: `/root/eval10_final_ownership_review26`
- timestamp recorded after receipt: `2026-08-09T23:17:52-07:00`
- reviewed staged index tree: `509badabe9b678e786152706d57539ee38472da3`
- reviewed candidate-manifest SHA-256:
  `ad7ffe9bbc2cbc6e5f0569772f221c9dc9b4f2970bb4ec9a22c4c23ee1575850`
- 78-file candidate-ledger SHA-256:
  `f839a54cbd75f7224725a0c8451bd69908b6c298f8a063335fee93de05783713`
- 80-entry review-subject-ledger SHA-256:
  `c4b8b4e11df9012932cb5534ec9e84136d65cd8951d19e22b99630b7b616a914`
- 288-entry external-manifest SHA-256:
  `e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`

The reviewer independently replayed the 119-source CPython 3.13.11 audit and
all 67 then-current controls, checked the 82-path owned scope, external
collection, benchmark, exact correction bytes, and **NOT SENT** gate, and found
no independent P1. It confirmed that the named TF-IDF, zero-shot/fine-tuned
DeBERTa, and base/MCGrad ModernBERT repairs were correctly represented.

The decisive P2 was that the generalized ownership repair still accepted
non-result numbers and cross-model cells. The LAPD Llama2-7B account selected
the “7B” model-size numeral instead of its Table 6 result. The two J-Detector
ablations treated a 95 axis tick and a 5.3-point feature-ablation decrease as
absolute F1 results. The validator also accepted a T-Detect mutation that moved
the metric to an unrelated 3.9-percent row after the mutation moved the old
metric into the negative-donor fields. Broader inspection then confirmed a
GPT-J account borrowing RoBERTa-Large's row. Thus a checksum, account label, and
negative-value inequality did not prove semantic row ownership.

The successor re-audits all 321 ownership records. It rejects model-name
numerals, years, uncertainty cells, axis ticks, ranks, and sample counts;
requires exact result-row/column/state bindings; and derives every
wrong-column donor from a distinct result cell in the same source row. It also
corrects the LAPD, J-Detector, DetectAnyLLM, IRM, DetectGPT, base
Binoculars/ImBD, and DivEye counterexamples and requires each negative control
to fail for the intended semantic reason.

Review 26 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or commit. A different reviewer must inspect the final frozen repair.

## Review 27 — PASS (distinct final read-only reviewer)

- reviewer identity: `/root/eval10_final_ownership_review27`
- timestamp recorded after receipt: `2026-08-10T00:08:07-07:00`
- reviewed staged index tree: `9caf13f0b8035a25266a36682abb014e34a7ead2`
- reviewed candidate-manifest SHA-256:
  `65d74bb8453057b0ea54fb648357c0277bb6dbb384bcd12de9a60fd34b1fbc80`
- 78-file candidate-ledger SHA-256:
  `9999c82723f088584a14a70a95bd9a7f17f283e614d44df3e6d8cca137123399`
- 80-entry review-subject-ledger SHA-256:
  `3d6b6efb0c9452ca0fb8c7a08375b8c64d510eb44cb5296f05fe39e77e48a8c9`
- 288-entry external-manifest SHA-256:
  `e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`

The reviewer reconstructed the staged index in isolation. Its independent
CPython 3.13 replay reproduced the generated bytes and passed with 119 sources,
987 accounts and witnesses, 724 primary-result dispositions, 4,812 result
candidates plus 119 source summaries, all 321 ownership replacements, and all
70 controls. The ownership generator independently reproduced the exact
987-row final witness ledger.

A separate re-extraction of all 75 evidence sources used by the ownership
repair checked every one of the 321 rows. It found zero source-hash, page/line,
account/state, numeric-column, raw-candidate, or donor failures. The 298
wrong-column donors were distinct, deterministically derived result cells; the
remaining 23 state/row donors were valid. Direct checks confirmed TF-IDF,
zero-shot and fine-tuned DeBERTa, base and MCGrad ModernBERT, LAPD, both
J-Detector ablations, T-Detect, all three DetectAnyLLM states, IRM, DetectGPT,
base Binoculars and ImBD, all three DivEye states, and NEULIF.

The 78-file candidate ledger, 80-entry review-subject ledger, exact 82-file
owned live/index scope, absence of ignored bytecode, 288-file read-only external
collection, score verifier, model-layout verifier, conclusion, exact correction
subject/body, and **NOT SENT** gate all passed. Formatting and lint passed. The
only P3 was that a generic isolated Python environment lacks `sklearn`; the
recorded frozen Python 3.13 benchmark environment runs the verifier successfully.

Review 27 final verdict: **PASS — no P1/P2 findings**. The reviewer made no
edit, stage, commit, push, external-artifact change, email, or delivery attempt.
This internal PASS completes the required adversarial review but does not
authorize email delivery; the fresh evaluator and manager gate in
`delivery_plan.md` remains binding.

## Review 28 — FAIL (fresh dw1eval11 one-shot evaluator)

- evaluator workspace: `/ssd1/sichangheagent/dw1eval11`
- verdict recorded: `2026-08-10T04:26:53-07:00`
- evaluated documentation commit:
  `815e2f7c69151799f2b1b2f48ce5f5a7dd7cee5c`
- evaluated tree: `0baa83bc5269fe78cb03c2458e5eb8b48b55585a`
- evaluator-verdict SHA-256:
  `34768a3aff75af2fdb6099d18edde9f3f93cc7f8891f2014c8a4b7c8fc17a5a7`

The evaluator admitted the frozen candidate, independently reproduced its
119-source CPython 3.13 audit, all 70 then-current controls, the benchmark
verifiers, repository and 288-file external integrity, exact corrective-email
bytes, and **NOT SENT** gate. It found no new P1 and confirmed the accepted
scientific, MELD, LM2otifs/NEULIF, composite/full-text coverage, public-access,
two-A6000, conclusion, and delivery-boundary work.

The decisive P2 was a generalized wrong-column-donor defect. The predecessor
ownership ledger called two PAWN ensemble component counts (`1`, `1`), the
Exaone model version `3.5`, and Candace/TF-IDF `System 3`/`System 2` identifiers
different result cells. Their exact source rows instead contain PAWN result
cells 94.59/93.92/94.26/0.988 and 90.78/96.13/93.45/0.987, Exaone results
92.08/79.74/72.00/81.27, and eight result metrics after each System identifier.
Review 27's claimed exhaustive independent donor inspection was therefore
substantively false even though the owned positive metrics remained correct.

The successor schema freezes, for every one of the 298 wrong-column rows, the
source-derived semantic result-column start/end indexes, the complete set of
in-boundary result-cell indexes, and the selected alternate donor index. The
validator binds that inventory with an immutable digest and excludes
configuration labels, component counts, system identifiers, model/CUDA
versions, numeric model-name fragments, slash-delimited IDs, and text-length
parameters. Nine source-row mutations exercise the five reproduced failures
and four additional metadata classes. The exact Exaone Table 3 header is also
restored to extracted line 444 rather than self-labeling the result row.

Review 28 final verdict: **FAIL**. It authorizes no delivery, email, lifecycle
closure, or commit. A new distinct reviewer must inspect all 298 donor cells
against their source table/figure/prose semantics rather than merely replaying
the candidate parser, and must bind the fully frozen successor bytes.

## Review 29 — PASS (distinct final read-only reviewer)

- reviewer identity: `/root/eval11_final_semantic_donor_review29`
- timestamp recorded after receipt: `2026-08-10T05:06:01-07:00`
- reviewed staged index tree: `3caba735cec7e45f49a00a4f306248ab8ddd1277`
- reviewed candidate-manifest SHA-256:
  `56cb99259395830ca25d4d5cca0343648794677d37e638331870611db7cb0ced`
- 78-file candidate-ledger SHA-256:
  `f5b55b1255fa86500c94df75fdf78a48bb284f90949dedc91290051316cb8e04`
- 80-entry review-subject-ledger SHA-256:
  `9330c44b9efda81984ec50a467f5ebec39731c4e18fafae02a59d191658e4448`
- 321-row predecessor-ownership-ledger SHA-256:
  `8937292b89b527a5ebf8b618240389c633c0f3d7faff435531483b3129eeb112`
- 987-row final-witness-ledger SHA-256:
  `5058be16a7f15aa8f5e8c04e57ee80611ebe494ba2da0d8defadfe6f01a33641`
- 288-entry external-manifest SHA-256:
  `e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`

The reviewer reconstructed the staged tree in isolation and regenerated the
three audit TSVs byte-for-byte with the canonical CPython 3.13 command. The run
passed with 119 full-text sources, 987 accounts and witnesses, 724 primary
results, 4,812 result candidates plus 119 summaries, 298 semantic wrong-column
boundaries across 69 parents, and all 79 controls.

Crucially, the reviewer did not accept the candidate parser as proof. It made a
fresh `pdftotext -layout` extraction, independently implemented the logical-row
and index check, and source-checked all 298 wrong-column rows across the 69
bound PDFs. Its manual sweep of all 128 header/row groups found zero source,
record, index, value, or semantic discrepancies. Every donor is an actual table
result metric, including FPR, loss, or timing only when that quantity is a
declared result column; ranks, confidence intervals, uncertainties, model and
CUDA versions, component/count/token metadata, and identifiers are excluded.
It directly confirmed PAWN 94.26/93.45, Exaone 79.74 under the exact Table 3
header, Candace 99.60, and TF-IDF 97.91. It also confirmed that all nine mutated
metadata values lie outside their frozen semantic index sets.

The 78 stable files, 80 review subjects, exact 82-file owned scope, 288-file
read-only external collection, 8,022-row score verifier, 25-file model-layout
verifier, exact correction subject/body/plan, and **NOT SENT** gate all passed.
The reviewer generated and then removed three local bytecode cache files during
a static check; a final live/index comparison independently confirmed that no
cache, untracked, unstaged, ignored, or unowned byte remained.

Review 29 final verdict: **PASS — no P1/P2 findings**. The sole P3 is that the
validator uses the same conservative “not inside the derived semantic result
boundary” message for an in-boundary wrong alternate metric; this does not
weaken rejection or any ownership invariant. The reviewer made no candidate,
external-evidence, email, delivery, commit, or push change. This internal PASS
does not authorize email delivery; the fresh one-shot evaluator and manager
gate in `delivery_plan.md` remains binding.
