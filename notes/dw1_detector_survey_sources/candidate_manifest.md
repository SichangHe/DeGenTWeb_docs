# Frozen candidate manifest

Candidate date: 2026-08-09, America/Los_Angeles.

Candidate state: **FROZEN FOR DISTINCT FINAL-BYTE ADVERSARIAL REVIEW**. After
this manifest, the stable ledgers, and the review-subject ledger are created,
the only permitted candidate change is appending the read-only review verdict.
No internal review authorizes delivery. The corrective email remains **NOT
SENT**.

## Scope and accepted chain

The owned candidate consists only of:

- `../dw1_detector_survey.md`;
- `../dw1_detector_survey_email.md`; and
- every file in this `dw1_detector_survey_sources/` directory.

The direct predecessor documentation commit is
`c4246ad56aaf90461584de5b6afd0ae7c8104b44`, the pushed rev6 successor repair
evaluated by dw1eval8.
The accepted survey chain is preserved in Git: original survey `d5fb118`,
accuracy-first renewal `fe98a1c`, evaluator repair `f749a13`, rev2 semantic
repair `45191cb`, rev3 composite/E-card repair `1d2fc389`, rev4 full-text repair
`15acd6c`, eval6 successor `c9968e7`, and rev6 semantic-coverage repair
`c4246ad`. No DW1
implementation or configuration file is in the candidate. A later parent-
repository commit may change only the `docs` gitlink to the pushed documentation
commit.

## Repository content binding

`candidate_files.sha256` covers 76 stable scientific, audit, benchmark,
delivery, and evidence files. To avoid recursive or post-review invalidation it
excludes exactly four control artifacts: itself, this manifest,
`review_subject_files.sha256`, and `adversarial_review.md`. The final Git commit
binds all four exclusions. The separate review-subject ledger directly hashes
all 76 stable scientific, audit, benchmark, evidence, and exact-email files plus
the external README and manifest. It deliberately excludes both metadata
ledgers, this manifest, itself, and the review record, avoiding recursive or
obsolete indirect bindings; the final Git commit binds those control artifacts,
and the direct subject hashes remain reconstructable after the verdict is
appended. The candidate-ledger and review-subject-ledger SHA-256 values are:

`8217d71a51c9ed8430b006edc852e67c46435aa53403d5c92601331621b2e32a`

`1093ad9665835c6f546d4154fca9f99e13c0d320d43f26360ff1adead4608152`

The ledger includes the complete earlier MELD, benchmark, integrity, coverage,
and review evidence plus this repair's composite source/result mappings,
generated audits, primary-search record, public-checkpoint benchmark source,
both raw attempts, 8,022-row CSV, independent verifier, static checks, execution
environment, and model hashes. It also includes the full-text inventory generator,
independent table-discovery program, candidate/resolution/witness snapshots, 119-source PDF/text ledger,
immutable 987-account inventory and map, 724 primary-result dispositions, and
generated account audit. From `docs/notes/`, the exact
check is:

```text
sha256sum --check dw1_detector_survey_sources/candidate_files.sha256
```

Broad `*.txt`, `*.csv`, and `*.tsv` ignore rules apply in this repository. Every
owned ignored evidence file must therefore be force-added, and a staged-path
comparison must prove that every ledger path is present in the index. Raw CSV
bytes are bound by the ledger and must not be silently normalized. The owned
`.gitignore` explicitly unignores `__pycache__/` and `*.pyc`, so interpreter
caches cannot disappear from ordinary Git status; the frozen live scope contains
none, and all replay commands route caches to `/tmp`.

## External public evidence binding

Canonical path:

`/ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08`

The external `MANIFEST.sha256` covers 288 files and has SHA-256:

`e9ae35623cb3b808368cc9729d001bc33940b71148814199402c9d2b4149dd97`

`sha256sum --check MANIFEST.sha256` passed for all 288 entries. No file or
directory in the collection is writable. It preserves the earlier 150-file
collection, every composite parent PDF, Task 3 overview and six primary system
papers, Counter Turing primary papers, bounded primary-absence responses,
official source archives, and three complete immutable public checkpoint
snapshots. The collection contains only anonymous public evidence. No PB,
credential, authenticated endpoint, persistent browser/session state, cookie
reuse, robot-challenge bypass, or human-owned tmux session was used.

The final 14 additions are anonymously public arXiv PDFs needed to bind one
primary paper for every frozen export row. The external README identifies them;
`coverage_fulltext_sources.tsv` binds all 119 exact PDF and extracted-text
hashes. The external manifest path set exactly equals the live artifact set.

## Coverage anchors

The three immutable exact-phrase exports still contain 204 raw rows and 119
unique 2025–2026 publications. `coverage_row_dispositions.tsv` maps each exactly
once. The generated row audit flags 106 titles/abstracts, resolves 70 explicit
dispositions and 49 mechanically allowlisted non-candidate classes, and returns
PASS.

A second level selects 33 overview, benchmark, shared-task, evaluation,
comparative, survey, dataset, or training-study composite sources from frozen
title/class rules. All 33 have exact inspected scopes. Twenty-six expand to 263
individual named system/version rows; the other seven have source-specific
no-qualifier reasons. Every child binds a parent, metric and scope,
primary source or bounded-absence sentinel, artifact status, disposition, and
source card. The checker requires an independent, SHA-256-bound exact inventory
of all 263 result IDs and binds every expanded parent to its E-card. Task 3 and
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

The final content-derived layer does not use the composite selector. It binds all
119 primary PDFs and exact text extractions, then maps 987 expected accounts
one-to-one: 263 accepted embedded results and 724 primary-result dispositions,
with no parent-only account. Six sources have paper- and table-specific
no-qualifier reasons. Whole-file hashes and an immutable digest of every parent/
account pair prevent an omitted row from being hidden by lowering a mutable
count. Content anchors cover the earlier examples, the non-English and SenFlow
counterexamples, LM2otifs, NEULIF, all 13 TELL rows, all 15 LAPD-paper rows, all
nine late-stage stability rows, all 15 DNA-DetectLLM-paper rows, both DP-Net
states, and every no-account decision. A separate program scans all 119 PDFs
before account matching and freezes 4,812 high-metric table-row, grouped-method,
Roman-table, and figure-legend candidates plus 119 content-hash-bound source
summaries. Every candidate has an explicit resolution; content requirements
cover PAWN's fitted baseline, all four distribution-trained Vanilla states,
both ImBD training states, the evaluator-confirmed fitted additions, and the
final composite and primary comparison states. A distinct account-adjudication
phase then emits exactly one source-derived identity/metric witness for all 987
accounts without seeding or suppressing the raw candidate queue. The last repair directly requires
all 29 evaluator-confirmed Roman-table/Figure 4 accounts, exact source scope for
all 119 PDFs, and the six arXiv 2602.11871 scorer configurations whose Table 1
AUROC definition occurs only in Appendix K. The scanner normalizes mathematical
Unicode metric glyphs and spaced F1 labels; all three arXiv 2505.11550 Table 2
architectures now have direct raw candidates and witnesses. The five
distribution-shift shared-row states now bind their own Table 4 or Table 11
metric columns, while an audit-derived equation binds the external README to
4,812 result candidates plus 119 summaries. Fifty full-text controls join
the eleven accepted controls; all sixty-one pass. The exact
commands, inputs, output hashes, Poppler extraction version, and generated
987-row audit
are preserved.
The three audit/inventory programs and the two composite benchmark/verifier
programs pass Ruff 0.14.9 format and lint checks. The two composite
benchmark/verifier programs also pass the separately recorded basedpyright
1.36.0 check under the Python 3.13 target; no basedpyright-clean claim is made
for the expanded audit/inventory scripts.

The Leidos primary paper maps v1.0.4 to the unweighted multiclass DistilRoBERTa
state. The prior ensemble wording is removed from the result ledger and E1 card,
and a mutation control rejects its return.

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
all five methods' AUROCs and operating points. That score verifier passes the
recorded Ruff 0.14.9 and basedpyright 1.36.0 checks. The
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
  `82f31c0318dbc1d1f89edf78b18a094b3ff37abaff85b573580a978ea71b2e1a`.
- Mechanical subject SHA-256:
  `73540e80f5dafef3f3cb5168ad75475f755efade636b7135ea21ccaa4fc9abad`.
- Mechanical body SHA-256:
  `97cee6b3cdef877bf22b0334425853eb3d4e85213921122d93c83922f03915a0`.

The mechanical copies exactly equal the subject and body of the human-readable
draft. Status is **NOT SENT**. `delivery_plan.md` forbids delivery unless a new
one-shot evaluator passes the exact pushed candidate and the manager then
authorizes this exact frozen subject/body pair. An internal reviewer PASS is not
an evaluator PASS.

## Independent review chain

`adversarial_review.md` preserves twenty-one predecessor reviewer/evaluator verdicts.
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

Review 10 is the fresh dw1eval5 FAIL. It demonstrated that title/class selection
still omitted multi-configuration ordinary papers and corrected the Leidos
v1.0.4 mechanism. The 119-PDF/805-account repair and its thirteen full-text controls
are frozen for a new distinct adversarial reviewer. Review 10 remains a FAIL and
does not authorize delivery.

Review 11 is the first post-evaluator fresh-review FAIL. It caught the nine
Chinese encoder/LoRA states and eight SenFlow-related states that the initial
manual inventory missed. The repaired full-table pass also made the
2501.14288/LuxVeri rows and 17 weak-aggregate, high-narrow-cell TELL,
late-stage, ReMoDetect, and ImBD results explicit. Review 11 remains a FAIL and
does not authorize delivery.

Review 12 is the next distinct fresh-review FAIL. It caught eight baselines in
2509.15550 that falsely inherited DNA-DetectLLM's regeneration exclusion. The
repair gives every row its primary-paper mechanism, retains regeneration only
for actual DNA states, and adds a code-anchor mutation. The same systematic
check corrects training-only DP-Net noise from method-excluded to
evidence-rejected. Review 12 remains a FAIL and does not authorize delivery.

Review 13 is a different fresh review over the rev4 successor repair.
It independently reproduced all 119 sources, 805 accounts, 564 primary rows,
and 24 controls; checked the target primary PDFs, mixed-parent exclusions,
benchmarks, both integrity ledgers, conclusion, owned paths, and exact NOT-SENT
binding; and returned **PASS — no P1/P2 findings**. The eval6 one-shot verdict
then showed that Review 13 neither discovered all fitted states nor bound final
nonrecursive bytes, so it does not pass this repair or authorize delivery.

Review 14 is the distinct eval6 internal PASS. It reproduced the then-frozen
119-source/958-account/4,860-candidate state and all 31 controls. The fresh
dw1eval7 one-shot evaluator then proved that its scanner omitted Roman-numbered
tables, figure results, and 14 zero-yield sources; its environment bytes were
inconsistent; it did not directly hash this manifest; and ignored bytecode was
present. Review 14 therefore does not pass this repair or authorize delivery.

Review 15 is the dw1eval7 **FAIL** and is preserved with verdict SHA-256
`b90483ac670a29a0dde34a3e4420d0b5b7ee7fe1943b93395b9f72392882994f`.
Review 16 is the distinct read-only eval7 successor **FAIL**. It directly bound
the manifest and verified the 29 Roman/Figure accounts, but proved that arXiv
2602.11871 was still an account-bearing zero-yield source and that only 623 of
987 accounts had any candidate target. Review 17 is a different distinct
read-only **FAIL**. It proved that shared-task accounts were co-bound to the
wrong team row: Unibuc-NLP's qualifying Table 8 accuracy appeared only in prose,
while the raw candidate row belonged to AdvacheckEnglish. Review 18 is a further
distinct **FAIL** because an ignored, uncommitted legacy witness TSV remained in
the live owned directory; it was removed. Review 19 is another distinct **FAIL**:
it showed that mathematical Unicode `𝐹 1` suppressed all three qualifying Table
2 rows in arXiv 2505.11550, leaving inventory-driven witnesses with no raw
candidate. Every verdict remains non-authorizing. The repair now spans Unicode
metric normalization, off-page metric definitions, structured
same-PDF rank joins, table columns and vertical groups, text-extracted figure
series, hash-bound visual plot readings, and explicit below-threshold states,
with one source-derived witness for every account.

Review 20 is the distinct internal PASS over the failed rev6 bytes. Review 21,
the fresh dw1eval8 one-shot **FAIL**, then proved that Review 20 had not compared
the external README's advertised discovery total with raw replay and had
accepted five metrics owned by other arXiv 2607.03680 configurations. Both
records remain durable and non-authorizing. This successor derives the README
equation mechanically and gives those five states exact Table 4 or Table 11
row-and-column witnesses with wrong-row and wrong-column controls. Review 22,
the first distinct review of those bytes, then found that four reasoning-graph
accounts still inherited Longformer's Table 2 metric and that a rekeyed PAN12
witness could move to its neighboring F1 column. The final repair gives all
five accounts exact account-owned row/column joins, requires their candidate
targets, canonicalizes every supplied witness from the bound PDFs, and retains
Review 22 as a non-authorizing FAIL. Review 23 independently reproduced those
repairs and found only one stale capitalized `58` in the survey evidence note;
that note now says the mechanically derived 61, its ledgers are refreshed, and
Review 23 remains a non-authorizing FAIL.

The new distinct final reviewer must independently challenge all 119 source
summaries, the 4,812 result candidates, the 29 evaluator-confirmed accounts,
the six off-page-metric accounts, all 987 source-derived witnesses, Roman-table,
rank-join, column, vertical-group, and Figure 4 provenance, predecessor zero-yield sources,
the three Unicode-F1 Table 2 rows, the exact Python 3.13 replay, clean owned path
set, all 61 controls, and the unsent correction. It must directly record this final
`candidate_manifest.md` SHA-256 in addition to every hash in
`review_subject_files.sha256`. Its successor verdict will be appended without
changing any reviewed subject byte.

## Required final verification

Before commit and after checkout of the final commit:

1. replay the semantic audit and its sixty-one controls under the recorded
   Python 3.13 command;
2. replay the independent score verifier and static checks;
3. verify all 76 repository-ledger entries and 288 external-ledger entries;
4. prove the human email equals the mechanical subject/body and remains unsent;
5. prove every candidate-ledger path is staged and no unowned path is staged;
6. commit and push only owned documentation artifacts; and
7. verify the remote documentation commit and, if needed, update only the parent
   `docs` gitlink from an isolated clean worktree.
