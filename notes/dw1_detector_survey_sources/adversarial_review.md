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
