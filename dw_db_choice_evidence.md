# Database-choice measurement transcript
(authored by agents unless marked 🧑)

```text
Collected October 5, 2026, around 01:25–01:30 PDT.
Read-only catalog queries and EXPLAIN without ANALYZE; no corpus query executed.
Planner counts are estimates. Statistics counters do not establish full historical activity.

=== catalog ===
BEGIN
SET
SET
                                                              version                                                              
-----------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 17.5 (Ubuntu 17.5-1.pgdg20.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0, 64-bit
(1 row)

              name               | setting  | unit |       source       
---------------------------------+----------+------+--------------------
 checkpoint_timeout              | 1800     | s    | configuration file
 effective_cache_size            | 2097152  | 8kB  | configuration file
 maintenance_work_mem            | 8388608  | kB   | configuration file
 max_connections                 | 256      |      | configuration file
 max_parallel_workers            | 128      |      | configuration file
 max_parallel_workers_per_gather | 64       |      | configuration file
 max_wal_size                    | 65536    | MB   | configuration file
 random_page_cost                | 1.1      |      | configuration file
 shared_buffers                  | 2097152  | 8kB  | configuration file
 synchronous_commit              | off      |      | configuration file
 temp_file_limit                 | 20971520 | kB   | configuration file
 temp_tablespaces                |          |      | default
 wal_compression                 | pglz     |      | configuration file
 work_mem                        | 262144   | kB   | configuration file
(14 rows)

                  relname                  | estimated_rows | table_size | indexes_size | total_size |    tablespace    
-------------------------------------------+----------------+------------+--------------+------------+------------------
 htmls                                     |       68171024 | 3274 GB    | 1490 MB      | 3275 GB    | database_default
 common_crawl_index_generation_records     |      885913216 | 234 GB     | 88 GB        | 323 GB     | ts_ssd1
 extractions                               |       93378256 | 161 GB     | 4036 MB      | 165 GB     | database_default
 cc_idx_records                            |      884648576 | 95 GB      | 34 GB        | 129 GB     | database_default
 crawls                                    |      111025872 | 7801 MB    | 26 GB        | 34 GB      | ts_ssd1
 site_pages                                |          96738 | 29 GB      | 7248 kB      | 29 GB      | database_default
 pages                                     |      106140448 | 13 GB      | 15 GB        | 28 GB      | ts_ssd1
 classifications                           |      104003824 | 9974 MB    | 9332 MB      | 19 GB      | ts_ssd1
 clasf_crawls                              |      102366080 | 5937 MB    | 10112 MB     | 16 GB      | ts_ssd1
 dolma_cleaned_metrics                     |       93404432 | 11 GB      | 2086 MB      | 13 GB      | ts_ssd1
 dolma_cleaned                             |       91088680 | 6082 MB    | 6864 MB      | 13 GB      | ts_ssd1
 subdomains                                |       19666808 | 1629 MB    | 5785 MB      | 7414 MB    | ts_ssd1
 detector_score_sets                       |       24679928 | 2375 MB    | 1000 MB      | 3375 MB    | ts_ssd1
 ads_counts                                |       37824596 | 1706 MB    | 1645 MB      | 3351 MB    | ts_ssd1
 detector_score_archive_results            |        2668471 | 2562 MB    | 770 MB       | 3332 MB    | database_default
 detector_score_archive_bindings           |        2236126 | 2269 MB    | 947 MB       | 3216 MB    | database_default
 page_dates                                |       37584404 | 1829 MB    | 858 MB       | 2687 MB    | ts_ssd1
 warc_paths                                |        4630958 | 711 MB     | 1583 MB      | 2294 MB    | ts_ssd1
 subdomain_categorizations                 |          59221 | 1913 MB    | 5112 kB      | 1918 MB    | ts_ssd1
 subdomain_categorization_prompt_pages     |         287306 | 1320 MB    | 9120 kB      | 1329 MB    | ts_ssd1
 given_up_sites                            |        2983390 | 1096 MB    | 156 MB       | 1252 MB    | ts_ssd1
 old_cc_idx_records                        |        8380340 | 784 MB     | 391 MB       | 1175 MB    | database_default
 links                                     |        4038311 | 204 MB     | 392 MB       | 595 MB     | ts_ssd1
 blacklists_ut1_domains                    |        5340265 | 228 MB     | 163 MB       | 390 MB     | ts_ssd1
 subdomain_categorization_request_evidence |          12434 | 380 MB     | 568 kB       | 380 MB     | database_default
(25 rows)

  datname  | temp_files | temp_bytes | blks_read |  blks_hit  | stats_reset 
-----------+------------+------------+-----------+------------+-------------
 degentweb |          2 |  439125420 |  37747867 | 2719962604 | 
(1 row)

               tablename               |                    indexname                     |                                                                                     indexdef                                                                                      
---------------------------------------+--------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 cc_idx_records                        | cc_idx_records_pkey                              | CREATE UNIQUE INDEX cc_idx_records_pkey ON public.cc_idx_records USING btree (subdomain_id, record64blake3)
 common_crawl_index_generation_records | common_crawl_index_generation_records_pkey       | CREATE UNIQUE INDEX common_crawl_index_generation_records_pkey ON public.common_crawl_index_generation_records USING btree (generation_id, canonical_subdomain, record64blake3)
 common_crawl_index_generation_records | common_crawl_index_generation_records_site_order | CREATE INDEX common_crawl_index_generation_records_site_order ON public.common_crawl_index_generation_records USING btree (generation_id, subdomain64blake3, canonical_subdomain)
 crawls                                | idx_crawls_page_crawled_at_desc                  | CREATE INDEX idx_crawls_page_crawled_at_desc ON public.crawls USING btree (page_id, crawled_at DESC) INCLUDE (crawl_id, crawl_ok, w_browser)
 crawls                                | idx_crawls_ok_browser                            | CREATE INDEX idx_crawls_ok_browser ON public.crawls USING btree (crawl_id) WHERE (crawl_ok AND w_browser)
 crawls                                | idx_crawls_src_page_crawled_at_desc              | CREATE INDEX idx_crawls_src_page_crawled_at_desc ON public.crawls USING btree (crawl_src_id, page_id, crawled_at DESC) INCLUDE (crawl_id, crawl_ok, w_browser)
 crawls                                | crawls_pkey                                      | CREATE UNIQUE INDEX crawls_pkey ON public.crawls USING btree (crawl_id)
 crawls                                | crawls_page_id_crawled_at_key                    | CREATE UNIQUE INDEX crawls_page_id_crawled_at_key ON public.crawls USING btree (page_id, crawled_at)
 crawls                                | idx_crawls_page_id                               | CREATE INDEX idx_crawls_page_id ON public.crawls USING btree (page_id)
 crawls                                | idx_crawls_crawled_at                            | CREATE INDEX idx_crawls_crawled_at ON public.crawls USING btree (crawled_at)
 crawls                                | idx_crawls_ok                                    | CREATE INDEX idx_crawls_ok ON public.crawls USING btree (crawl_ok)
 crawls                                | idx_crawls_w_browser                             | CREATE INDEX idx_crawls_w_browser ON public.crawls USING btree (w_browser)
 pages                                 | idx_pages_subdomain_page_id                      | CREATE INDEX idx_pages_subdomain_page_id ON public.pages USING btree (subdomain_id, page_id)
 pages                                 | pages_pkey                                       | CREATE UNIQUE INDEX pages_pkey ON public.pages USING btree (page_id)
 pages                                 | idx_pages_subdomain_id                           | CREATE INDEX idx_pages_subdomain_id ON public.pages USING btree (subdomain_id)
 pages                                 | idx_pages_page_url                               | CREATE UNIQUE INDEX idx_pages_page_url ON public.pages USING btree (md5(page_url))
(16 rows)

ROLLBACK

=== plans ===
BEGIN
SET
SET
           name           | setting | unit 
--------------------------+---------+------
 effective_io_concurrency | 256     | 
 hash_mem_multiplier      | 2       | 
(2 rows)

  spcname   | pg_tablespace_location 
------------+------------------------
 pg_default | 
 pg_global  | 
 ts_ssd1    | /ssd1/postgresql17main
(3 rows)

                relname                | n_live_tup | n_dead_tup | last_analyze | last_autoanalyze 
---------------------------------------+------------+------------+--------------+------------------
 cc_idx_records                        |          0 |          0 |              | 
 crawls                                |      96225 |          0 |              | 
 site_pages                            |          0 |          0 |              | 
 common_crawl_index_generation_records |   13049720 |    6523952 |              | 
(4 rows)

                                                              QUERY PLAN                                                              
--------------------------------------------------------------------------------------------------------------------------------------
 Unique  (cost=2.98..1099043.67 rows=11126230 width=24)
   InitPlan 1
     ->  Index Scan using crawl_sources_crawl_src_name_key on crawl_sources  (cost=0.14..2.35 rows=1 width=2)
           Index Cond: (crawl_src_name = 'common_crawl2'::text)
   ->  Incremental Sort  (cost=0.62..1059508.64 rows=15813070 width=24)
         Sort Key: crawls.page_id, crawls.crawled_at DESC, crawls.crawl_id DESC
         Presorted Key: crawls.page_id, crawls.crawled_at
         ->  Index Only Scan using idx_crawls_src_page_crawled_at_desc on crawls  (cost=0.57..511959.89 rows=15813070 width=24)
               Index Cond: ((crawl_src_id = (InitPlan 1).col1) AND (crawled_at < '2026-08-01 00:00:00'::timestamp without time zone))
(9 rows)

                                                             QUERY PLAN                                                              
-------------------------------------------------------------------------------------------------------------------------------------
 Finalize GroupAggregate  (cost=32365730.67..32413676.90 rows=36587 width=27)
   Group Key: canonical_subdomain
   ->  Gather Merge  (cost=32365730.67..32411481.68 rows=365870 width=27)
         Workers Planned: 10
         ->  Sort  (cost=32364730.48..32364821.95 rows=36587 width=27)
               Sort Key: canonical_subdomain
               ->  Partial HashAggregate  (cost=32361591.49..32361957.36 rows=36587 width=27)
                     Group Key: canonical_subdomain
                     ->  Parallel Seq Scan on common_crawl_index_generation_records  (cost=0.00..31888080.49 rows=94702200 width=27)
                           Filter: (generation_id = 1)
(10 rows)

ROLLBACK

=== generations ===
BEGIN
SET
 generation_id | expected_shard_count | max_records_per_subdomain | manifest_sealed 
---------------+----------------------+---------------------------+-----------------
             1 |                  580 |                      2000 | t
(1 row)

 generation_id | record_count | site_count | completed_shard_count 
---------------+--------------+------------+-----------------------
(0 rows)

 selection_run_id | generation_id | selected_site_count 
------------------+---------------+---------------------
(0 rows)

                     relname                      | size  | tablespace 
--------------------------------------------------+-------+------------
 cc_idx_records_pkey                              | 34 GB | ts_ssd1
 common_crawl_index_generation_records_pkey       | 76 GB | ts_ssd1
 common_crawl_index_generation_records_site_order | 12 GB | ts_ssd1
(3 rows)

ROLLBACK

=== analytics_plan ===
BEGIN
SET
                                                                                         QUERY PLAN                                                                                         
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Left Join  (cost=33231254.20..38833480.97 rows=1413636 width=216)
   Hash Cond: (crawls.crawl_id = page_dates.crawl_id)
   ->  Nested Loop  (cost=31874264.84..37192475.82 rows=1413636 width=208)
         ->  Nested Loop  (cost=31874264.27..36732806.21 rows=1413636 width=178)
               ->  Hash Left Join  (cost=31874263.70..34071933.49 rows=1413636 width=100)
                     Hash Cond: (crawls.crawl_id = ads_counts.crawl_id)
                     ->  Nested Loop  (cost=30597422.53..32561210.53 rows=1413636 width=96)
                           Join Filter: basic_dw_filter(dolma_cleaned.n_tokens, classifications.pcent_relative_dupe)
                           ->  Hash Right Join  (cost=30597421.95..31343310.81 rows=4428706 width=72)
                                 Hash Cond: (detector_score_sets.score_set_id = dolma_cleaned.score_set_id)
                                 ->  Seq Scan on detector_score_sets  (cost=0.00..550671.28 rows=24679928 width=32)
                                 ->  Hash  (cost=30542063.13..30542063.13 rows=4428706 width=56)
                                       ->  Nested Loop  (cost=1926889.82..30542063.13 rows=4428706 width=56)
                                             ->  Nested Loop  (cost=1926889.24..30289719.22 rows=10093534 width=32)
                                                   ->  Unique  (cost=1926888.68..1977356.35 rows=10093534 width=24)
                                                         ->  Sort  (cost=1926888.68..1952122.51 rows=10093534 width=24)
                                                               Sort Key: crawls.page_id, crawls.crawled_at DESC
                                                               ->  Nested Loop  (cost=0.70..631419.93 rows=10093534 width=24)
                                                                     ->  Index Scan using crawl_sources_crawl_src_name_key on crawl_sources  (cost=0.14..2.35 rows=1 width=2)
                                                                           Index Cond: (crawl_src_name = 'common_crawl2'::text)
                                                                     ->  Index Only Scan using idx_crawls_src_page_crawled_at_desc on crawls  (cost=0.57..472804.90 rows=15861268 width=26)
                                                                           Index Cond: (crawl_src_id = crawl_sources.crawl_src_id)
                                                   ->  Limit  (cost=0.57..2.79 rows=1 width=8)
                                                         ->  Index Only Scan using idx_clasf_crawls_crawl_id_desc on clasf_crawls  (cost=0.57..2.79 rows=1 width=8)
                                                               Index Cond: (crawl_id = crawls.crawl_id)
                                             ->  Memoize  (cost=0.57..2.79 rows=1 width=24)
                                                   Cache Key: clasf_crawls.clasf_id
                                                   Cache Mode: logical
                                                   ->  Index Only Scan using idx_dolma_cleaned_passes_true on dolma_cleaned  (cost=0.56..2.78 rows=1 width=24)
                                                         Index Cond: (clasf_id = clasf_crawls.clasf_id)
                           ->  Memoize  (cost=0.58..2.79 rows=1 width=40)
                                 Cache Key: clasf_crawls.clasf_id
                                 Cache Mode: logical
                                 ->  Index Scan using idx_classifications_clasf_cover on classifications  (cost=0.57..2.79 rows=1 width=40)
                                       Index Cond: (clasf_id = clasf_crawls.clasf_id)
                     ->  Hash  (cost=604875.52..604875.52 rows=38656852 width=12)
                           ->  Seq Scan on ads_counts  (cost=0.00..604875.52 rows=38656852 width=12)
               ->  Index Scan using pages_pkey on pages  (cost=0.57..1.88 rows=1 width=86)
                     Index Cond: (page_id = crawls.page_id)
         ->  Memoize  (cost=0.57..1.83 rows=1 width=34)
               Cache Key: pages.subdomain_id
               Cache Mode: logical
               ->  Index Scan using subdomains_pkey on subdomains  (cost=0.56..1.82 rows=1 width=34)
                     Index Cond: (subdomain_id = pages.subdomain_id)
   ->  Hash  (cost=644154.16..644154.16 rows=41008016 width=16)
         ->  Seq Scan on page_dates  (cost=0.00..644154.16 rows=41008016 width=16)
(46 rows)

ROLLBACK


=== host snapshot, approximately 01:35 PDT ===
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1    3.5T  2.1T  1.2T  64% /ssd1
/dev/sda         15T  9.7T  4.1T  71% /hdd1
               total        used        free      shared  buff/cache   available
Mem:           251Gi        39Gi        13Gi        17Gi       198Gi       192Gi
Swap:          2.0Gi       2.0Gi       0.0Ki

```
