# Database choice for DeGenTWeb
(authored by agents unless marked 🧑)

## Recommendation

🧑 “Or is it that we are using Postgres wrong?”

I would keep PostgreSQL but change its role. PostgreSQL fits the mutable relational work: crawl identities, job claims, annotations, provenance, and publishing a selected cohort atomically. I would move the bulk Common Crawl index, immutable page bodies, and repeated corpus analysis out of its main workload.

The code reveals avoidable work, but I have not measured whether it dominates ingestion or analysis time. The current code repeatedly maintains indexed records and prunes them while ingesting; the analysis reconstructs latest-page state across large tables before DuckDB receives the result. Disk placement and query resource settings compound those costs. Replacing PostgreSQL while preserving this design would preserve these sources of I/O.

🧑 “Basically, if we redo this project from scratch, what should we have chosen and how should we have designed around the DBs?”

My default would be **PostgreSQL on SSD + immutable Parquet datasets queried with DuckDB + compressed body files on HDD or object storage**. Parquet is a column-oriented file format, not another database service. Add ClickHouse only if concurrent, repeatedly refreshed corpus queries need a shared analytics server. I cannot establish that requirement from the code or the measurements here. This is a design recommendation, not a measured winner.

This assumes batch research on one main machine, with only chosen sites needing active crawl state. The code supports selecting sites before crawling, but I do not know the eventual working-set size. If all 100 million pages need active operational queries, PostgreSQL needs a correspondingly large hot metadata store.

The additional file pipeline buys independent analytics, immutable research inputs, and separation of bodies from database maintenance. It also adds file publication, retrieval, backup, and restore code. If that cost exceeds the value of independent snapshots, PostgreSQL COPY staging, one batch reduction, and reusable PostgreSQL snapshot tables are a reasonable simpler design to benchmark.

For the existing project, I would first reuse the existing DuckDB caches and publish shareable narrow snapshots, then set explicit scratch and worker budgets. I have not established how often caches are rebuilt. Separate bodies and redesign the next index generation after that.

## What I measured

Measured October 5, 2026, around 01:25–01:30 PDT, using read-only catalog queries and EXPLAIN without ANALYZE. No corpus query ran. Full original output is in [the measurement transcript](dw_db_choice_evidence.md). Sizes below use PostgreSQL's binary units. Row counts are planner estimates from `pg_class.reltuples`, not exact counts.

The original catalog output includes `htmls ... 3274 GB`, `common_crawl_index_generation_records ... 234 GB ... 88 GB`, and `crawls ... 7801 MB ... 26 GB`. Bodies dominate capacity: HTML occupies about 3.2 TiB. The retained candidate index has an estimated 886 million rows and occupies 323 GiB including indexes. These are allocated sizes, not useful payload or removable bloat. The legacy index is another 129 GiB; similar row estimates do not prove duplicate contents.

The generation table and both indexes are on `ts_ssd1`, whose location is `/ssd1/postgresql17main`. Its primary index alone is 76 GB; its site-order index is 12 GB. `crawls`, `pages`, classifications, and several feature tables are also on SSD. HTML, extractions, and the legacy index heap use the database default tablespace; the manager states: “the PostgreSQL data directory is on a hard drive, `/hdd1`” (task delegation in this conversation). The legacy index's 34 GB primary index is on SSD. Thus “the database is on HDD” conceals a mixed layout.

The host reported 251 GiB RAM, about 192 GiB available, 1.2 TiB free on SSD, and 4.1 TiB free on HDD. Those values are transient. Moving all 3.2 TiB of HTML to this SSD is not currently possible without changing capacity or retention.

The settings returned `work_mem = 262144 kB`, `hash_mem_multiplier = 2`, `max_parallel_workers_per_gather = 64`, `temp_file_limit = 20971520 kB`, and an empty `temp_tablespaces`. These mean 256 MiB per sort operation, potentially 512 MiB per hash operation, up to 64 workers per gather, and 20 GiB of temporary files per process. Spill still uses the default tablespace. Multiple operations, workers, and queries multiply resource use.

The failure account says “no `temp_file_limit`”; today's limit is different. PostgreSQL documents that the limit is for “a given PostgreSQL process.” It does not give one query a 20 GiB budget. [PostgreSQL 17 resource documentation](https://www.postgresql.org/docs/17/runtime-config-resource.html). Full settings and relation measurements are in the linked transcript.

The small generation metadata tables returned `expected_shard_count = 580` and `max_records_per_subdomain = 2000`. There was no generation seal or selection-run row at measurement time. The table estimate therefore does not establish the size of a completed, sealed July population. Recent activity statistics have missing analyze timestamps and implausibly small live counts relative to allocated tables. I would not use those activity counters to estimate corpus cardinality or infer today's maintenance history. The database temp counters also do not reconstruct the earlier incident.

## Where the design spends disk work

**Ingestion maintains the final relational representation before selection.** In [generation_ingest.rs](../src/generation_ingest.rs), the batch size is bounded by `MAX_GENERATION_QUERY_PARAMS / 9`, about 7,281 rows. It runs `INSERT ... ON CONFLICT ... DO UPDATE`, then prunes touched sites with `row_number() OVER (PARTITION BY canonical_subdomain ORDER BY record64blake3)` and `DELETE`. A generation-wide `pg_advisory_xact_lock` spans each shard's transaction. These statements maintain two large indexes, check lineage constraints, and revisit retained records after every shard. The lock serializes database persistence for that generation even if downloading or parsing overlaps. These are source facts; I have not measured their individual runtime shares.

This keeps up to 2,000 records per site across the whole candidate population before choosing the final sites. It stores and maintains candidates that may never enter the final crawl; the avoidable fraction is unmeasured. The current selection rule uses valid canonical sites present in the generation and an inclusive site-hash boundary, not an uncapped page-count threshold. The SQL says `GROUP BY canonical_subdomain, subdomain64blake3`; the builder skips a site when `candidate.subdomain64blake3 > config.inclusive_boundary_hash` ([common_crawl_selection.sql](../src/degentweb/sql/queries/common_crawl_selection.sql), lines 158–163; [rebuild_selection.py](../src/degentweb/common_crawl/rebuild_selection.py), lines 415–425). A redesign can apply that fixed hash boundary earlier to payload retention while preserving the full candidate-site inventory and required audit counts.

**DuckDB currently receives an expensive PostgreSQL result.** The analysis script executes `CREATE TABLE df_all_source AS FROM postgres_query(...)`; its referenced SQL first chooses latest crawls, chooses latest classifications, and joins classifications, cleaning, scores, ads, pages, sites, and dates. See [cc_dolma_data_analysis.py](../src/degentweb/common_crawl/cc_dolma_data_analysis.py), lines 207–227, and [classifying.sql](../src/degentweb/sql/queries/classifying.sql), lines 678–787.

EXPLAIN of that actual dataset query returned these original plan fragments:

```text
Sort ... rows=10093534
  Sort Key: crawls.page_id, crawls.crawled_at DESC
Seq Scan on detector_score_sets ... rows=24679928
Seq Scan on ads_counts ... rows=38656852
Seq Scan on page_dates ... rows=41008016
```

The plan also has millions of estimated per-crawl latest-classification lookups. Estimates are not actual reads or timings. The cache is built only after this PostgreSQL query finishes, so it cannot remove the first extraction's join work. Useful composite indexes already exist; “add an index” alone is not a sufficient diagnosis.

A separate EXPLAIN of the unbounded latest-capture operation estimated 15.8 million index entries feeding an incremental sort and uniqueness step. A generation-wide site aggregation planned a parallel sequential scan with 10 workers. Neither plan was executed. The current backlog query now includes `page_id = ANY($1::BIGINT [])`; it should not be described as still running the incident's unbounded query.

**Resource controls do not match the shared disks.** The incident document records “about 8 million temporary files” and cleanup “at about 300 files per second.” Its reported failure was prolonged disk saturation and ext4 journal failure, not evidence that PostgreSQL lost committed table data. See [the incident account](pg_temp_file_disk_failure_2026-10-03.md). SSD table placement does not redirect spill files when `temp_tablespaces` remains default. The cost settings are global despite mixed SSD/HDD storage. `effective_cache_size` is a planner estimate, not reserved memory; its 16 GiB value merits comparison with actual cache residency. I would not prescribe a replacement number from `free` alone.

Longer checkpoints can reduce repeated writes during ingestion, but cannot eliminate index maintenance, pruning, global joins, or HDD spill cleanup. `synchronous_commit = off` trades recent-commit crash durability for latency; it is not a substitute for efficient bulk loading.

## From-scratch design

The data flow would be: decode and merge index shards → choose eligible sites → load their working records into PostgreSQL → crawl, store bodies, and record extraction/scoring results → publish reusable research snapshots for DuckDB.

1. **Store bodies separately.** Write compressed HTML and extracted text into immutable packs sized for the review/scoring read workload, with a manifest mapping capture/content IDs to pack offsets and lengths. Keep checksums, sizes, provenance, and pointers in PostgreSQL. Pack files avoid millions of filesystem objects; retain an index for bounded random reads used by review and scoring. Use HDD/object storage for cold packs and SSD for active packs. Existing WARC references can substitute for a copy only when retrieval availability and reproducibility meet the project's needs. This removes large payloads from database maintenance, but adds a separate body backup/restore responsibility and application-managed retrieval. It does not reduce the bytes needed to read them.

2. **Make Common Crawl ingestion a batch reduction.** Decode each selected source shard once, canonicalize and hash exactly as today, and write immutable Parquet fragments with source-shard identity and checksum. Deduplicate by the existing key and tie-break rule, then merge per-site bounded record sets across all releases. The downloader already keeps shard-local smallest sets: its comment says “preserving only the `MAX_RECORDS_PER_SUBDOMAIN` records with the lowest hashes” ([idx_file_downloading.rs](../src/idx_file_downloading.rs), lines 7–8). Merge those sets to obtain the global smallest 2,000 distinct hashes, retaining the current duplicate tie-break, without maintaining a globally mutable indexed table during each shard load. Partition by a bounded number of site-hash buckets so a site's records meet in one reduction; avoid one file per site. Keep a compact site inventory with each site's distinct retained-record count, capped at 2,000. This reproduces counts over the retained index; it is not an uncapped distinct-page count. The current site-selection rule needs presence and site hash, not that uncapped count. Choose the final cohort only after full-period eligibility and deterministic selection are established. PostgreSQL receives the selected working records and compact generation/shard/selection metadata, rather than the entire candidate index. Keep the globally reduced candidate index, at most 2,000 retained hashes per site, queryable as Parquet. By default, discard intermediate shard fragments after verifying the final dataset and retaining source manifests/checksums; retaining all decoded candidates would be a separate storage choice.

3. **Preserve the existing publication guarantees.** Keep canonicalization, exact shard manifests, checksums, completion receipts, generation sealing, and atomic active-selection changes. Finish immutable files first, verify their manifest, then commit one PostgreSQL manifest pointer. A failed transaction leaves unreferenced files, not a partially published population. Each run records and keeps using the same file manifest and generation ID. Deterministic replay and file cleanup replace the current giant shard transaction's crash recovery role.

4. **Separate operational state from research snapshots.** PostgreSQL owns active jobs, current crawl/classification pointers, labels, and selected-page metadata. For this default design, PostgreSQL retains the selected working population's crawl/classification history and foreign-key references; Parquet is the published research copy, not a reason to delete referenced database rows. Bodies and the full candidate index have their authoritative copies in files. Archiving operational history out of PostgreSQL would require a separate reference/retention design. “Latest” must name its policy: source, cutoff, successful versus any capture, and tie-break. A current pointer cannot answer an arbitrary historical cutoff. Produce versioned capture/feature/score Parquet tables and a joined narrow table for common analyses. Score records include detector/model version, text checksum, and preprocessing version. Publish cohort membership and exact capture/classification IDs alongside each research snapshot.

5. **Run analysis directly on snapshots.** DuckDB reads local Parquet or materializes the hot subset into its own database. PostgreSQL supplies bounded IDs or changed rows, rather than repeatedly rebuilding the corpus through joins. DuckDB's documentation says “only the columns required for the query are read” for Parquet; partitioning and sorting also enable skipping irrelevant portions. [Parquet documentation](https://duckdb.org/docs/stable/data/parquet/overview.html). Use SSD scratch space with explicit memory, thread, and spill budgets. DuckDB still spills, and its documentation warns: “If multiple blocking operators appear in the same query, DuckDB may still throw an out-of-memory exception”. [Workload tuning](https://duckdb.org/docs/stable/guides/performance/how_to_tune_workloads.html).

6. **Budget the shared machine.** Give ingestion, analysis, and backups explicit concurrency and disk-space budgets. Isolate analytics scratch from PostgreSQL's data/WAL and reserve free space for recovery. Set PostgreSQL limits by role/workload; bound aggregate worker usage, not just each process. Review actual plans before corpus jobs. Start with fewer workers and increase only when measured throughput improves without starving other work.

## Other choices and what would change my answer

I would add **ClickHouse** for several simultaneous analytics users or continuously refreshed shared queries over full history. Load append-only, versioned facts in batches, choose sorting keys from measured filters, and build explicit cohort/latest snapshots. Keep transactionally authoritative labels and job state in PostgreSQL. The ClickHouse documentation cautions that “sending too many insert queries per second can lead to situations where the background merging can't keep up”. Switching engines still requires batch ingestion and an I/O budget. [ClickHouse insert guidance](https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/_snippets/_bulk_inserts.md).

I would not introduce Scylla for the observed join-heavy research workload. SQLite or Turso could serve a much smaller embedded application, but they do not address the measured full-population reduction and joins. I see no measured requirement for distributed key-value serving or database sync. Those are workload-based recommendations, not benchmark results comparing these engines.

## What remains unknown

I do not know how much of the days-long ingestion was download, decoding, index writes, pruning, checkpoints, or waiting. Nor did I measure HDD latency, cache residency, bloat, or alternative-engine speed. The report supports an architectural recommendation, not a promised speedup.

Before committing to a migration, compare an isolated representative multi-release, overlapping-site sample under (a) the current loader, (b) PostgreSQL COPY staging followed by set-based reduction and final index construction, and (c) Parquet/DuckDB reduction. Preserve identical selected records and provenance, including canonicalization, signed hash ordering, deduplication, tie-breaks, and eligibility/count semantics. Measure elapsed time, bytes written including WAL/spill, peak memory, final bytes, restart behavior, and interference with operational queries. Compare cold and warm snapshot queries as well. Only these measurements can tell whether improving PostgreSQL alone is enough and whether ClickHouse earns its additional service.

The missing operational evidence is per-stage ingestion timing and per-job read/write/spill accounting. Recording those during normal runs would make future database decisions much less speculative.
