# Frozen candidate manifest

Candidate date: 2026-08-08, America/Los_Angeles.

Candidate state: **PASS** after review-1 and review-2 preservation findings were
resolved and a third distinct reviewer inspected the repaired staged candidate.
No scientific evidence or email copy changed after that PASS; only the verdict
and its resulting integrity bindings were added.

## Scope and baseline

The owned candidate consists only of:

- `../dw1_detector_survey.md`;
- `../dw1_detector_survey_email.md`; and
- every file in this `dw1_detector_survey_sources/` directory.

The documentation baseline is commit
`fe98a1c552680e36f201a5340732c01cbac0739f`. No DW1 implementation or
configuration file is in the candidate. A later parent-repository commit may
change only the `docs` gitlink to the pushed documentation commit.

## Repository content binding

`candidate_files.sha256` covers the two top-level documents and 37 source/evidence
files, 39 files total. It deliberately excludes itself and this explanatory
manifest; the final Git commit binds those two files. Its current SHA-256 is:

`177d8f945741c89a1ccd4a0c18adf7240df0ea1199c617b35f5fbe962b7fadf9`

The ledger includes `adversarial_review.md`, every raw MELD stdout/stderr file,
the 8,022-row score CSV, interpreter/package/GPU manifests, model hashes, raw Atom
exports, Scholar TSV, coverage dispositions, and the mechanical email
subject/body. `sha256sum --check candidate_files.sha256` must pass before commit
and after checkout of the final commit.

Files normally ignored by broad `*.txt`, `*.csv`, or `*.tsv` rules are explicitly
force-added. A staged-path comparison must show no candidate file absent from the
Git index. The raw score CSV uses CRLF bytes emitted by Python's CSV writer; it
was inserted in the index with Git content filters disabled so the committed blob
retains the exact recorded SHA-256 instead of silently normalizing line endings.

## External public evidence binding

Canonical path:

`/ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08`

The external `MANIFEST.sha256` covers 105 files and has SHA-256:

`0afacad6dc7921c2f43e794f590604be49d9464ee2e9e7a8d3c91d227cd9c989`

`sha256sum --check MANIFEST.sha256` passed for all 105 files. The collection holds
the newly decisive PDFs, complete paper-era and current MELD snapshots, official
MRF and Exons source archives, public metadata, raw queries, and relevant HTTP
evidence. It also holds a primary PDF for every one of the 49 distinct arXiv IDs
linked in the plausible-result and targeted carry-forward tables. No
authenticated or persistent browser/session state was used.

## Benchmark anchors

- Current MELD revision:
  `453acf594d48f8c55c3a38bde396f9178516d817`.
- Paper-era preserved, not executed:
  `51f3ac2d4ce8de9f6f3a1eba9ca4276b077bb808`.
- Score CSV SHA-256:
  `7a37e7b7df84ab19fe915dfca5e07be7bb95ff3b44ad105cb0a5af1e1a924d63`.
- Score rows: 8,022 plus header.
- Independent CSV recomputation: direct and length-eligible AUROCs, calibration
  split counts, one/five-percent operating points, and shipped-threshold transfer
  rates all match `benchmark_meld_stdout.txt`.
- Static checks: the exact Python 3.13 target and isolated interpreter are recorded
  in `benchmark_meld_checks.txt`; ruff and basedpyright pass in that stated
  environment.

## Coverage anchors

The three raw exact-phrase exports contain 93, 40, and 71 rows and are each sorted
by submitted date descending. Deduplicating 2025–2026 identifiers yields 119;
all 119 appear in `coverage_dispositions.md`. EchoPrompt, Steer-to-Detect, and
Hidden Human-Like Nature are identified as targeted carry-forwards, not silently
counted in the 119.

The Google Scholar artifact is exactly one anonymous public first page and is not
called exhaustive. The historical robot challenge and fresh HTTP 200 observation
are both preserved; neither involved a bypass.

## Frozen corrective email and no-send state

- Human-readable email SHA-256:
  `3de69505a15116813823c38fe8c5435572f91b7a5bc9d34ee5d50e121f1b1f2e`.
- Mechanical subject SHA-256:
  `653b384e8e7218093a9d70386ebc745553c633ae2f02f7e502f15b431d7800b7`.
- Mechanical body SHA-256:
  `6b1e4791efb7217b238a7d0473fe9e7ac1866bab7df6bf03a2ef1214f250b9e9`.

The mechanical copies exactly equal the subject and body of the human-readable
draft. Status is **NOT SENT**. `delivery_plan.md` forbids delivery unless a new
one-shot evaluator passes this exact pushed candidate and the manager then
authorizes the exact frozen subject/body. An internal reviewer PASS is not an
evaluator PASS.

## Independent review chain

`adversarial_review.md` preserves three distinct reviewer identities, exact
scopes, verified facts, findings, resolutions, and unmodified final verdicts.
Review 1 caused this manifest, explicit force-addition, durable review record,
and explicit static-check environment. Review 2 found 13 disposition-table
papers missing from the external collection; all 13 PDFs are now preserved,
raising the verified external ledger from 92 to 105 files.

Review 3 inspected the fully staged repaired candidate and candidate ledger
SHA-256
`5bd694aa5fdfd7b7dc984412aeb15222199b7c6f97ded9038c25d0a50ee75eb8`
against recency, primary-artifact preservation, MELD provenance/comparability,
accuracy, exclusions, two-A6000 memory, near-Binoculars speed, conclusion, and
email gating. It returned **PASS** with no P1, P2, or P3 findings. Its verbatim
verdict was then appended to the review artifact, necessarily changing that one
entry and the final candidate-ledger hash shown above; no reviewed scientific or
email content changed.
