# One query took down `/hdd1` and PostgreSQL (2026-10-03)

(authored by agents unless marked 🧑)

🧑 "document this horror story concisely in relevant dw docs and make sure any
agent who wants to run similar queries will see it"

## What happened

- 2026-10-02 21:40 PDT: an agent ran
  `scripts/dw_writeup_scoring_backlog.py --timeout-seconds 1800`, one count
  over the latest Common Crawl capture per page
  (`SELECT DISTINCT ON(page_id) ... FROM crawls ... ORDER BY page_id, crawled_at DESC`,
  joined to classifications and extractions).
- The plan spilled to disk with many parallel workers
  (`max_parallel_workers_per_gather = 64`, `work_mem = 256MB`, no
  `temp_file_limit`) and created about 8 million temporary files in
  `base/pgsql_tmp` on the single hard disk `/hdd1`.
- 22:10: the statement timeout cancelled it. `pg_cancel_backend` and
  `pg_terminate_backend` at 22:38 returned true. The backend kept running
  anyway: it had to delete its temporary files first, at about 300 files per
  second, which is about 7 hours.
- That deletion, a backup, and agents' whole-disk file scans saturated the
  disk. 2026-10-03 04:36:24: ten writes waited past the kernel's 30 s limit and
  were dropped, ext4 aborted its journal, and `/hdd1` refused all writes.
- PostgreSQL was down from 04:36 to 13:04. Recovery needed root: unmount,
  `e2fsck`, restart. No table data was lost; the write-ahead log is on `/ssd1`.

## Why the usual safety nets failed

- A statement timeout bounds how long the query runs, not how long its
  clean-up runs. Cancelling or terminating the backend does not skip the
  clean-up.
- The server does not log successful or running statements, and `agent_dw`
  cannot list temporary files (`pg_ls_tmpdir`) or set `temp_file_limit`.

## Rule

🧑 "understand exactly what your query will do and how much they scan before
you execute them"

Largest tables: `htmls`, `common_crawl_index_generation_records`,
`extractions`, `cc_idx_records`, `crawls`, `pages`, `classifications`,
`clasf_crawls`, `dolma_cleaned`.
