# Semantic coverage audit design

- focus
  - frozen 2025–2026 rows from the three exact-phrase Atom exports
  - title-and-abstract claims that require individual review
- inputs
  - immutable Atom exports
  - one reviewed TSV mapping per deduplicated arXiv identifier
  - one reviewed composite-source row for every overview, benchmark, shared-task,
    evaluation, dataset, survey, comparative, and training-study source selected
    by the frozen title/class rule
  - one reviewed embedded-result row for every unique named detector system or
    submitted version at or above the frozen 0.90 threshold on any reported
    evaluation/test aggregate, dataset, generator, domain, prompt group,
    language, text-length bucket, attack, class-specific, or fixed-threshold
    slice on AUC/AUROC, accuracy, F1, precision, recall, or TPR, or carrying an
    explicit strong/best claim
  - one separately maintained, SHA-256-bound exact-result inventory listing the
    immutable parent/result ID pair for every expanded publication
  - the SHA-256-bound Markdown E-card file, whose machine-readable heading
    markers bind each real card label and parent to its complete result-ID set
- control flow
  - parse and deduplicate identical export metadata
  - flag SOTA, best/first-rank/most-performant, comparative-improvement,
    high/robust/remarkable/near-perfect, accuracy-claim, named-metric, and
    high-percentage text
  - require exactly one mapping for every exported identifier
  - require an individual disposition or documented false-positive resolution
    for every flag
  - require every disposition code to appear in the script's kind-specific
    code-to-definition allowlist; emit that definition beside every generated row
  - select composite sources from allowlisted publication classes and title
    patterns, then require exactly one source-level resolution
  - require every expanded source's actual result-ID set to equal the independent
    exact-result inventory, not merely a mutable count; parse the real Markdown
    E-cards and require their parent/result sets to match both ledgers; bind every
    embedded row to its parent-specific E-card, version, claim, metric scope,
    qualifying basis, primary source or bounded-absence marker, artifact status,
    and disposition
  - additionally hard-code all twenty Task 3 and eight Counter Turing result
    sets as anchor checks against the independent inventory
  - treat per-domain, per-language, per-generator, per-length, per-attack, and
    class-specific high cells as qualifying discovery evidence; preserve the
    weak overall/cross-slice result in the same disposition instead of using it
    to erase the named high result; precision-only or recall-only crossings must
    retain the corresponding accuracy/F1 so class collapse is visible
  - replay predecessor, missing-anchor-result, lowered-count plus missing
    non-anchor result, formerly hidden high-cell parent, nonexistent-card label,
    removed real card, wrong real-card parent, wrong real-card result set,
    analogous count-mismatch, weak-negative, and complete-negative controls on
    every run
  - emit a complete generated TSV, environment, hashes, counts, command, and PASS
    only after validation
- assumptions
  - arXiv identifier is the stable row key
  - the frozen title and abstract are discovery evidence, not promotion evidence
  - primary-paper review remains necessary for plausible candidates
  - training-only validation scores are retained when a source presents them as
    detector performance, but the disposition must label them as validation and
    preserve the official held-out result; no validation score can promote a method
- failure conditions
  - missing, duplicate, unknown, conflicting, incomplete, or unresolved mappings
  - unknown, catch-all, or wrong-kind disposition codes
  - a selected composite source without an inspected table/page scope and a
    result-specific expansion, parent disposition, or documented no-qualifier reason
  - missing, duplicate, unversioned, unaudited-parent, count-mismatched,
    exact-inventory-mismatched, source-card-mismatched, real-card-missing,
    real-card-parent-mismatched, or real-card-result-mismatched embedded results
  - known Leidos-version, Task 3 team, or Counter Turing system omissions
  - an asserted no-qualifier class with empty or generic inspection evidence
  - an asserted no-qualifier or parent-only class for a parent present in the
    immutable exact-result inventory, including a formerly hidden high-cell source
  - an altered independent expectation inventory whose SHA-256 no longer matches
    the checker constant
  - generated output that does not bind the exact exports, reviewed mapping,
    exact expectation inventory, and real Markdown E-card file by SHA-256
