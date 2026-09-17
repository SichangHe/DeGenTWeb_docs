# AI website-builder quirks

(authored by agents unless marked 🧑)

This tree is the single source for operational quirks of the four builders named
in the September 15, 2026 “Other website builders” request. Each provider file
contains the restrictions established by its cited provider material and marks
verified evidence gaps as unknown.

- [Durable](durable.md)
- [10Web](10web.md)
- [Framer](framer.md)
- [Hostinger](hostinger.md)

Evidence was rechecked against the linked provider pages on September 15, 2026.
Prices exclude tax unless the source says otherwise. Recheck mutable prices,
product limits, and terms before use.

## Experiment artifact hygiene

- Put durable builder captures and lifecycle evidence under
  `data/source1931-builder-experiments/`, grouped by provider and by sealed or
  live state. Every migrated capture must have provenance recording its source,
  byte length, digest, and byte-for-byte verification.
- Put reusable automation in the repository's `scripts/` or `src/` tree and
  keep provider notes in this documentation tree.
- Do not place new experiment evidence or reports in an ad-hoc `.runtime`
  subtree. Runtime directories are only for ephemeral process state. Before
  removing legacy runtime evidence, first copy it into `data`, repoint and test
  every active reader, and preserve immutable consumed lifecycle files rather
  than rewriting them.
