# Semantic coverage audit design

- focus
  - frozen 2025–2026 rows from the three exact-phrase Atom exports
  - title-and-abstract claims that require individual review
- inputs
  - immutable Atom exports
  - one reviewed TSV mapping per deduplicated arXiv identifier
- control flow
  - parse and deduplicate identical export metadata
  - flag SOTA, best/first-rank/most-performant, comparative-improvement,
    high/robust/remarkable/near-perfect, accuracy-claim, named-metric, and
    high-percentage text
  - require exactly one mapping for every exported identifier
  - require an individual disposition or documented false-positive resolution for every flag
  - require every disposition code to appear in the script's kind-specific
    code-to-definition allowlist; emit that definition beside every generated row
  - emit a complete generated TSV, environment, hashes, counts, command, and PASS only after validation
- assumptions
  - arXiv identifier is the stable row key
  - the frozen title and abstract are discovery evidence, not promotion evidence
  - primary-paper review remains necessary for plausible candidates
- failure conditions
  - missing, duplicate, unknown, conflicting, incomplete, or unresolved mappings
  - unknown, catch-all, or wrong-kind disposition codes
  - generated output that does not bind the exact exports and reviewed mapping by SHA-256
