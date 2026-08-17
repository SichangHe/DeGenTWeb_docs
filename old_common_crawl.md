# Resumable 2014 Common Crawl ingest

`comcrawl-db --old-cc-2014-42` reads the deterministic 1/32 sample of
`CC-MAIN-2014-42` index files. It stores records separately from the current
Common Crawl cohort:

- records: `old_cc_idx_records`
- completed index files: `old_cc_idx_files`

The records and completion marker for one index file commit in the same
transaction. A crash before commit leaves the file incomplete, so a restart
retries it. A committed marker makes subsequent runs skip the file before
download. Run only one ingest process at a time.

## Deliberate production run

1. apply migration `v15.sql` through the normal PostgreSQL setup path
2. verify database version 15 and inspect aggregate state with the read-only
   query below
3. build and run from the production checkout in its designated non-human tmux
   session:

```sh
cargo run --release --features comcrawl-db --bin comcrawl-db -- --old-cc-2014-42
```

Restart with the same command. Do not add `--dbg` to the production run.

## Aggregate state

This query exposes no record content or credentials:

```sql
SELECT
    (SELECT count(*) FROM old_cc_idx_files) AS completed_index_files,
    (SELECT count(*) FROM old_cc_idx_records) AS records,
    (SELECT count(DISTINCT subdomain_id) FROM old_cc_idx_records) AS subdomains;
```
