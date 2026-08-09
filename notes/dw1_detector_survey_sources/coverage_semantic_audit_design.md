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
  `coverage_composite_sources.tsv`, the independent 241-ID
  `coverage_expected_result_ids.tsv`, 241 `coverage_embedded_results.tsv` rows,
  and the SHA-256-bound Markdown E-cards in
  `coverage_composite_dispositions.md`.
- `coverage_fulltext_expected_accounts.tsv` is the content-derived expected
  inventory. It contains 805 exact parent/account pairs: all 241 accepted
  embedded results and 564 explicit primary-paper configuration results. There
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

  The output must remain 119 sources, 805 accounts, and 564 primary-result rows.

## Validation flow

1. Parse and deduplicate the frozen exports; require exactly one allowlisted
   parent mapping for every identifier.
2. Preserve the accepted composite checks: exact 241-result set, real E-card
   parent/result binding, source-specific negative reasons, Task 3 and Counter
   Turing anchors, and all prior mutation controls.
3. Load all four full-text ledgers only if their whole-file SHA-256 values equal
   constants embedded in `audit_coverage.py`. Require the exact immutable digest
   of all 805 parent/account pairs.
4. Require the full-text source set to equal all 119 export identifiers. Rehash
   every primary PDF, rerun the exact text extraction, and compare both hashes.
   Reject missing, duplicate, reused, absolute, escaping, or unpreserved paths.
5. Require exact equality between expected account IDs and disposition-map IDs.
   An `embedded_result` target must be the accepted child under the same parent;
   a `primary_result` target must be an explicit row under the same parent.
6. Require the account count and mechanically derived resolution for each of all
   119 papers. A zero-account paper needs a source-specific full-text reason; no
   title-based catch-all or mutable count can suppress an expected account.
7. Content anchors independently require all three M-DAIGT systems, all nine
   classifier-by-feature states in 2503.22338, all eight DeBERTa states in
   2502.16857, all three Defactify systems in 2507.05157, all nine Chinese
   encoder/LoRA states in 2509.00731, eight SenFlow-related states, five
   semantic-similarity DeBERTa stages, both LuxVeri ensembles, LM2otifs, NEULIF,
   all 13 TELL rows, all 15 LAPD-paper rows, all nine late-stage stability rows,
   all 15 DNA-DetectLLM-paper rows, both training-only DP-Net states, and all six
   table-derived no-account decisions. Their system names, values, or exclusion
   evidence must occur in the hash-bound extracted text.
8. Require Leidos v1.0.4 to be described as the official paper's unweighted
   multiclass DistilRoBERTa classifier and reject the false ensemble description.
9. Emit the 119-row semantic audit, 241-row accepted embedded-result audit,
   805-row full-text account audit, exact command, environment, hashes, counts,
   and `PASS` only after all validation and controls succeed.

## Controls and failure conditions

The eleven accepted composite controls remain unchanged. Thirteen full-text controls
add an ordinary-title positive fixture and reject: deleting Candace while
lowering its mutable count; deleting a non-anchor PAWN ensemble while lowering
its count; deleting a non-English Qwen LoRA state while lowering its count;
detaching table content from that account set; deleting the narrow-domain
ChatGPT-D row while lowering its count; detaching its table content or a
table-derived no-account decision; detaching an extracted-text hash from its
PDF; giving retained LAPD- or DNA-DetectLLM-paper comparators their parent's
method-exclusion blocker; restoring the false Leidos ensemble mechanism; and
deleting any one of the 119 source audits.

The run fails on any missing, duplicate, unknown, incomplete, mis-parented,
mis-targeted, count-mismatched, hash-mismatched, unpreserved, or unmapped source,
account, result, E-card, PDF, or extraction. It also fails if the independent
241-ID or 805-account inventories change without their immutable checker
bindings, if a content anchor is absent, or if an asserted no-qualifier source
lacks a paper-specific full-text resolution.
