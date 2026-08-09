# Semantic coverage audit design

## Frozen boundary and account rule

- The discovery boundary is every one of the 119 deduplicated 2025–2026 rows in
  the three immutable exact-phrase Atom exports. Title wording and the existing
  parent disposition never decide whether a paper receives full-text review.
- `coverage_fulltext_sources.tsv` binds each export row to one preserved primary
  PDF, its PDF SHA-256, and the SHA-256 of `pdftotext -layout -enc UTF-8`
  output. Every main and appendix result table was inspected.
- An account is a separately named submitted, proposed, or fitted detector
  system, version, architecture, ensemble, training state, or configuration
  with AUC/AUROC, accuracy, F1, precision, recall, or TPR at or above 0.90 on a
  reported evaluation, test, validation, dataset, generator, domain, language,
  length, prompt, attack, or class-specific slice, or with an explicit strong or
  best claim. Repeated datasets and operating points are evidence on one account;
  component-only hyperparameter sweeps are not deployment accounts.
- A high narrow cell remains an account even when its official test, mean,
  transfer, low-FPR, or attack result is weak. The weak result must remain in the
  same disposition. Validation-only evidence is labeled and cannot promote a
  method.

## Inputs and exact mappings

- `coverage_row_dispositions.tsv` maps all 119 export rows exactly once; the
  title/abstract trigger layer still flags 106 rows and requires an explicit
  disposition or documented false-positive reason.
- The accepted 33-source composite layer remains intact:
  `coverage_composite_sources.tsv`, the independent 263-ID
  `coverage_expected_result_ids.tsv`, 263 `coverage_embedded_results.tsv` rows,
  and the SHA-256-bound Markdown E-cards in
  `coverage_composite_dispositions.md`.
- `coverage_fulltext_expected_accounts.tsv` is the content-derived expected
  inventory. It contains 987 exact parent/account pairs: all 263 accepted
  embedded results and 724 explicit primary-paper configuration results. There
  are no parent-only accounts. Six papers have a documented, table-derived
  `no_qualifying_account` resolution.
- `coverage_fulltext_account_map.tsv` maps every expected account to exactly one
  embedded-result or primary-result disposition. `coverage_primary_results.tsv`
  records the mechanism, exact
  table scope and high evidence, weaker evidence, public artifact status,
  method-boundary status, feasibility evidence, and decision for every newly
  expanded configuration.
- The inventory generator is `build_fulltext_inventory.py`. Its curated
  full-text/table inventory is reproducible with:

  ```text
  uv run --isolated --no-project --python 3.13 python \
    build_fulltext_inventory.py \
    --external-root /ssd1/sichangheagent/dw1_detector_survey_public_artifacts/2026-08-08
  ```

  The output must remain 119 sources, 987 accounts, and 724 primary-result rows.
- `discover_table_accounts.py` is a separate PDF-content pass. It scans table
  and figure content in all 119 bound PDFs for threshold-metric rows without
  importing the curated inventory. It recognizes Arabic and Roman captions,
  grouped rows, compact figure legends, and tables whose metric is defined in
  surrounding or appendix prose rather than on the same page. It also emits one
  content-hash-bound scope summary for every PDF, including sources with no
  threshold candidate. Mathematical Unicode metric glyphs and spaced F1 labels
  are normalized before the content scan. `coverage_table_candidates.tsv`
  freezes 4,931 rows: 4,812 result candidates plus 119 scope summaries.
  `coverage_table_discovery.tsv`
  gives every candidate exactly one account, targeted carry-forward, duplicate,
  or content-specific non-candidate resolution. The main audit regenerates both
  snapshots byte-for-byte and rejects any unresolved, removed, mutated, or
  mis-targeted row. Content rules derived from the actual PAWN,
  distribution-shift, READER, NEULIF, DivEye, PhantomHunter, DivScore, and E13,
  E20, and E21 table labels require every repaired fitted or comparison state
  even if a curator lowers a source count. The same independent pass requires
  26 Roman-table accounts and the evaluator-confirmed figure accounts.
  Candidate extraction remains inventory-independent; the second phase makes
  the explicit candidate adjudication and cannot suppress unknown candidates.
  A grouped-row pass additionally finds
  method identities printed once above several generator rows, including the
  DeTeCtive M4 checkpoint in Table 14 of arXiv 2510.12476 and six
  FastDetectGPT/Binoculars scorer configurations in arXiv 2602.11871 whose
  Table 1 AUROC definition appears only in Appendix K.
- `coverage_account_witnesses.tsv` is a separate, exactly 987-row
  source-to-account witness ledger. Every declared account has exactly one
  hash-bound identity/metric witness derived from its own PDF. Ordinary rows use
  direct or same-window evidence; structured witnesses encode rank joins,
  column/configuration joins, Roman-caption tables, vertical groups, figure
  series, exact visual-plot readings, and individually disposed below-threshold
  states. The ledger is generated from PDF content after raw discovery, never
  used to seed or suppress the raw candidate queue, and is replayed and
  validated byte-for-byte.

## Validation flow

1. Parse and deduplicate the frozen exports; require exactly one allowlisted
   parent mapping for every identifier.
2. Preserve the accepted composite checks: exact 263-result set, real E-card
   parent/result binding, source-specific negative reasons, Task 3 and Counter
   Turing anchors, and all prior mutation controls.
3. Load the four full-text inventories and the account-witness ledger only if
   their whole-file SHA-256 values equal
   constants embedded in `audit_coverage.py`. Require the exact immutable digest
   of all 987 parent/account pairs.
4. Require the full-text source set to equal all 119 export identifiers. Rehash
   every primary PDF, rerun the exact text extraction, and compare both hashes.
   Reject missing, duplicate, reused, absolute, escaping, or unpreserved paths.
5. Require exact equality between expected account IDs and disposition-map IDs.
   An `embedded_result` target must be the accepted child under the same parent;
   a `primary_result` target must be an explicit row under the same parent.
6. Require the account count and mechanically derived resolution for each of all
   119 papers. A zero-account paper needs a source-specific full-text reason; no
   title-based catch-all or mutable count can suppress an expected account.
7. Independently regenerate 4,812 table-row, grouped-method, Roman-table, and
   figure-legend candidates plus 119 content-hash-bound source summaries from
   every one of the 119 PDFs and the final resolution ledger. Require every
   candidate to have one allowed resolution and require RADAR-FT and the five-epoch M4
   RoBERTa baseline from PAWN; all four IntelLabs/MAGE/FAID/MIRAGE-trained
   Vanilla states; and both READ-trained and target-adapted ImBD states. Then
   apply the earlier content anchors for all three M-DAIGT systems, all nine
   classifier-by-feature states in 2503.22338, all eight DeBERTa states in
   2502.16857, all three Defactify systems in 2507.05157, all nine Chinese
   encoder/LoRA states in 2509.00731, eight SenFlow-related states, five
   semantic-similarity DeBERTa stages, both LuxVeri ensembles, LM2otifs, NEULIF,
   all 13 TELL rows, all 15 LAPD-paper rows, all nine late-stage stability rows,
   all 15 predecessor DNA-DetectLLM-paper rows, both training-only DP-Net states,
   and all six
   table-derived no-account decisions. Their system names, values, or exclusion
   evidence must occur in the hash-bound extracted text. Separately require the
   eight unmodified 2605.16107 baselines from Roman Tables II-III, ten
   2604.02008 base/DALD/Glimpse states from Roman Tables III-V, four
   2510.02319 comparators from Roman Table VIII, and seven 2508.11933 Table I or
   Figure 4 states, plus the six arXiv 2602.11871 Table 1 scorer configurations
   bound to their off-page AUROC definition. Then regenerate exactly one
   source-derived witness for every one of the 987 accounts. The validator binds
   the printed identity, metric/configuration, page/locator, join semantics, raw
   candidate where applicable, and extracted-text hash; no account may pass on
   a cross-parent carry-forward or a mutable prose assertion alone.
8. Require Leidos v1.0.4 to be described as the official paper's unweighted
   multiclass DistilRoBERTa classifier and reject the false ensemble description.
9. Emit the 119-row semantic audit, 263-row accepted embedded-result audit,
   987-row full-text account audit, exact command, environment, hashes, counts,
   and `PASS` only after all validation and controls succeed.

## Controls and failure conditions

The eleven accepted composite controls remain unchanged. Forty full-text controls
add an ordinary-title positive fixture and reject: deleting Candace while
lowering its mutable count; deleting a non-anchor PAWN ensemble while lowering
its count; deleting a non-English Qwen LoRA state while lowering its count;
deleting the PDF-discovered five-epoch RoBERTa baseline while lowering its
count; collapsing the separately discovered MIRAGE-trained Vanilla state while
lowering its count; making the READ-trained ImBD baseline inherit READER's
generation exclusion;
detaching table content from that account set; deleting the narrow-domain
ChatGPT-D row while lowering its count; detaching its table content or a
table-derived no-account decision; detaching an extracted-text hash from its
PDF; giving retained LAPD- or DNA-DetectLLM-paper comparators their parent's
method-exclusion blocker; restoring the false Leidos ensemble mechanism; and
deleting any one of the 119 source audits. Four resolution-ledger controls also
reject a removed candidate decision, an unknown target, suppression of the
content-required grouped DeTeCtive state, and mutation of raw PDF-derived row
content without a corresponding resolution. Four source-form controls reject a
missing content-hash-bound source summary, normalization of required Roman-table
evidence to an Arabic locator, reclassification of required figure-legend
evidence as an ordinary table row, and loss of direct same-parent evidence for
an account in a predecessor zero-yield source. The generalized account-witness
controls remove a witness, detach its source hash, and mutate both sides of the
shared-task rank join, REACT shot column, CAMF and DEER figure series, M4 and
GREATER table columns, the Qwen vertical group, the visual plot value, and the
below-threshold state classification. The DMAP control separately detaches its
Table 1 scorer accounts from the off-page AUROC definition. Two source-independent
fixtures require mathematical-Unicode F1 row discovery while retaining the
metric-context guard, and a witness mutation detaches one such account from its
raw Table 2 candidate. Together with the eleven composite controls, all 51
controls must pass.

The run fails on any missing, duplicate, unknown, incomplete, mis-parented,
mis-targeted, count-mismatched, hash-mismatched, unpreserved, or unmapped source,
account, result, E-card, PDF, or extraction. It also fails if the independent
263-ID or 987-account inventories change without their immutable checker
bindings, if a content anchor is absent, or if an asserted no-qualifier source
lacks a paper-specific full-text resolution.
