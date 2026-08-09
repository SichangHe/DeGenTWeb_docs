# Frozen candidate manifest

Candidate date: 2026-08-08, America/Los_Angeles.

Candidate state: **FRESH ADVERSARIAL PASS — AWAITING ONE-SHOT EVALUATOR**.
Review 3's earlier PASS is historical: the next evaluator showed that it did not
test catch-all semantics, and review 4 correctly rejected the first semantic
repair. Review 5 independently passed the fully frozen repair. This internal
review is not an evaluator PASS; no email delivery or lifecycle closure is
authorized.

## Scope and baseline

The owned candidate consists only of:

- `../dw1_detector_survey.md`;
- `../dw1_detector_survey_email.md`; and
- every file in this `dw1_detector_survey_sources/` directory.

The documentation baseline is commit
`f749a13a3529365bcb3d09d8ed72d2cdc7e08d76`. No DW1 implementation or
configuration file is in the candidate. A later parent-repository commit may
change only the `docs` gitlink to the pushed documentation commit.

## Repository content binding

`candidate_files.sha256` covers the two top-level documents and 43 source/evidence
files, 45 files total. It deliberately excludes itself and this explanatory
manifest; the final Git commit binds those two files. Its current SHA-256 is:

`2a265891dde4520857085019f44f5560fddee0a2d16b5f6308616e35b05ac0cf`

The ledger includes `adversarial_review.md`, every raw MELD stdout/stderr file,
the 8,022-row score CSV, interpreter/package/GPU manifests, model hashes, raw Atom
exports, Scholar TSV, row mapping, semantic-audit source/design/output/report/
environment, coverage dispositions, and mechanical email subject/body. Ledger
paths are relative to `docs/notes/`; the exact command, before commit and after
checkout of the final commit, is:

```text
cd /ssd1/sichangheagent/dw1/docs/notes
sha256sum --check dw1_detector_survey_sources/candidate_files.sha256
```

Files normally ignored by broad `*.txt`, `*.csv`, or `*.tsv` rules are explicitly
force-added. A staged-path comparison must show no candidate file absent from the
Git index. The raw score CSV uses CRLF bytes emitted by Python's CSV writer; it
was inserted in the index with Git content filters disabled so the committed blob
retains the exact recorded SHA-256 instead of silently normalizing line endings.

## External public evidence binding

Canonical path:

`/ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08`

The external `MANIFEST.sha256` covers 150 files and has SHA-256:

`1b92b652294562b6f1abbad3064c2c0f2b0fa2c49ff23e30b3937d5e9cdba67c`

`sha256sum --check MANIFEST.sha256` passed for all 150 files. The collection holds
the newly decisive PDFs, complete paper-era and current MELD snapshots, official
MRF and Exons source archives, public metadata, raw queries, and relevant HTTP
evidence. It also holds a primary PDF filename match for every one of the 71
distinct arXiv IDs linked in the explicit-disposition and targeted carry-forward
tables, plus immutable source archives for all three newly promoted papers that
link public repositories. DP-MGTD is explicitly preserved at public revision 1
because the frozen revision-2 PDF returned 404. No authenticated or persistent
browser/session state was used.

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
by submitted date descending. Deduplicating 2025–2026 identifiers yields 119.
`coverage_row_dispositions.tsv` maps each exactly once. The independent script
flags 106 rows for semantic performance triggers and requires either an
individual candidate disposition or documented false-positive reason. Its
kind-specific code-to-definition allowlists reject unknown, wrong-kind, and
catch-all codes. The generated audit has 68 explicit dispositions, 51
non-candidate classes, and PASS. EchoPrompt, Steer-to-Detect, and Hidden
Human-Like Nature are targeted carry-forwards, not silently counted in the 119.

The Google Scholar artifact is exactly one anonymous public first page and is not
called exhaustive. The historical robot challenge and fresh HTTP 200 observation
are both preserved; neither involved a bypass.

## Frozen corrective email and no-send state

- Human-readable email SHA-256:
  `a8b0d6e75483c7ede1733cc13f3c46ddb92c762bb78eac420c0c953c0ae8b5ca`.
- Mechanical subject SHA-256:
  `653b384e8e7218093a9d70386ebc745553c633ae2f02f7e502f15b431d7800b7`.
- Mechanical body SHA-256:
  `4604b9e408796d3e3c4d106ca8c1b7d742a18e0f9530643634ff00d90171a5dc`.

The mechanical copies exactly equal the subject and body of the human-readable
draft. Status is **NOT SENT**. `delivery_plan.md` forbids delivery unless a new
one-shot evaluator passes this exact pushed candidate and the manager then
authorizes the exact frozen subject/body. An internal reviewer PASS is not an
evaluator PASS.

## Independent review chain

`adversarial_review.md` preserves five distinct reviewer identities, exact
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

Review 4 inspected candidate-ledger SHA-256
`8e69fac73a24574f53424b4b13767970840335012ba88ef135c7ec38ba5ad580`
and external-ledger SHA-256
`f9b21e7a27383af474cc2b65a8fcdf8c33ca767e0d1d59ccddea41dd131e15b2`.
It returned **FAIL** because six high-scoring shared-task systems lacked
individual dispositions, arbitrary catch-all codes passed validation, and the
candidate-ledger command lacked its required working directory. Those findings
are durably preserved and resolved; a broader check additionally promoted
`2603.18750`.

Review 5, by the distinct reviewer `/root/semantic_repair_fresh_review`, inspected
candidate-ledger SHA-256
`cafc887f4811141bb067c33444813a65f466d64f413c84867cb1e44294c18839`
and the 150-entry external ledger. It replayed the row-level semantic audit and
its negative controls, checked the broader trigger surface, independently
challenged LM²otifs, NEULIF, and all seven later promotions, and rechecked every
previously accepted constraint, the bounded conclusion, exact correction, and
no-send gate. It returned **PASS — no P1, P2, or P3 findings**. Appending that
verdict changes only the durable review entry and its final candidate-ledger
binding; it does not change reviewed scientific or email content. Candidate
state remains pending a new one-shot evaluator and manager authorization.
