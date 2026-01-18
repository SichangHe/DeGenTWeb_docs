# Development

## Setup

- clone w/ `--recurse-submodules` and remember to update submodules on pull
    - automatically do these w/
        [these Git
        config](https://sichanghe.github.io/notes/programming/git.html#config)
- use [UV](https://docs.astral.sh/uv/) to manage Python dependencies
    (`uv sync --all-packages`, `uv add`)
    - note: some dependency like `nvidia-cuda-runtime-cu12` version for
        Binoculars are unfortunately hardcoded for Exxact; need to change if
        used on other machine
- install `ruff` and `maturin[patchelf]`:

    ```sh
    uv tool install ruff
    uv tool install maturin[patchelf]
    ```

- [install Rust](https://www.rust-lang.org/tools/install)
- register [Pre-commit Hook](https://pre-commit.com/) to run linters and
    formatters automatically before Git commit:

    ```sh
    . .venv/bin/activate
    pre-commit install
    ```

- copy the content of `../conf_template/` to `../` and modify they as
    appropriate.

## Pull request

- run `. static_checks.sh` before making pull request

## Coordination

- to pause scoring tasks, run:
    ```sh
    sh pause_bino_server.sh
    ```
- after done using the GPU, please allow the tasks to resume:
    ```sh
    sh /ssd1/sichanghe/DeGenTWeb/resume_bino_server.sh
    ```

## Restoring PostgreSQL database

- install PostgreSQL 17
- see
    [PgBackRest
    docs](https://pgbackrest.org/user-guide.html#quickstart/perform-restore)

### Record of Postgres tablespace creation

Properly restoring backup may require creating tablespaces using this info.

We have small tables & indices on SSD, rest on HDD, set up using:

```sql
CREATE TABLESPACE ts_ssd1 LOCATION 'replace w/ SSD data path';

-- Command used to create the alter table statements:
SELECT format(
         'ALTER TABLE %I.%I SET TABLESPACE ts_ssd1;',
         n.nspname, c.relname
       ) AS ddl
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog','information_schema')
  AND pg_total_relation_size(c.oid) < 10737418240  -- < 10GiB
ORDER BY pg_total_relation_size(c.oid) DESC;
-- Alter table statements generated:
ALTER TABLE public.crawls SET TABLESPACE ts_ssd1;
ALTER TABLE public.pages SET TABLESPACE ts_ssd1;
ALTER TABLE public.subdomains SET TABLESPACE ts_ssd1;
ALTER TABLE public.classifications SET TABLESPACE ts_ssd1;
ALTER TABLE public.dolma_cleaned SET TABLESPACE ts_ssd1;
ALTER TABLE public.clasf_crawls SET TABLESPACE ts_ssd1;
ALTER TABLE public.dolma_cleaned_metrics SET TABLESPACE ts_ssd1;
ALTER TABLE public.warc_paths SET TABLESPACE ts_ssd1;
ALTER TABLE public.ads_counts SET TABLESPACE ts_ssd1;
ALTER TABLE public.page_dates SET TABLESPACE ts_ssd1;
ALTER TABLE public.blacklists_ut1_domains SET TABLESPACE ts_ssd1;
ALTER TABLE public.given_up_sites SET TABLESPACE ts_ssd1;
ALTER TABLE public.detector_score_sets SET TABLESPACE ts_ssd1;
ALTER TABLE public.links SET TABLESPACE ts_ssd1;
ALTER TABLE public.redirections SET TABLESPACE ts_ssd1;
ALTER TABLE public.search_query_hashes SET TABLESPACE ts_ssd1;
ALTER TABLE public.wikihow_articles SET TABLESPACE ts_ssd1;
ALTER TABLE public.search_results SET TABLESPACE ts_ssd1;
ALTER TABLE public.cc_idx_files SET TABLESPACE ts_ssd1;
ALTER TABLE public.reviews SET TABLESPACE ts_ssd1;
ALTER TABLE public.search_engines SET TABLESPACE ts_ssd1;
ALTER TABLE public.crawl_sources SET TABLESPACE ts_ssd1;
ALTER TABLE public.blacklists_ut1_catalog SET TABLESPACE ts_ssd1;
ALTER TABLE public.site_tags SET TABLESPACE ts_ssd1;
ALTER TABLE public.tags SET TABLESPACE ts_ssd1;
ALTER TABLE public.version_n_timestamps SET TABLESPACE ts_ssd1;
ALTER TABLE public.baseline_sites SET TABLESPACE ts_ssd1;
ALTER TABLE public.baseline_correspondences SET TABLESPACE ts_ssd1;
ALTER TABLE public.seed_versions SET TABLESPACE ts_ssd1;

-- Command used to create the alter index statements:
SELECT format(
         'ALTER INDEX %I.%I SET TABLESPACE ts_ssd1;',
         ns.nspname, i.relname
       ) AS ddl
FROM pg_class t
JOIN pg_namespace ns ON ns.oid = t.relnamespace
JOIN pg_index ix ON ix.indrelid = t.oid
JOIN pg_class i ON i.oid = ix.indexrelid
WHERE t.relkind = 'r'
  AND ns.nspname NOT IN ('pg_catalog','information_schema')
  AND pg_relation_size(i.oid) < 10737418240  -- < 10GiB
ORDER BY pg_relation_size(i.oid) DESC;
-- Alter index statements generated:
ALTER INDEX public.idx_pages_page_url SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_src_page_crawled_at_desc SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_page_crawled_at_desc SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_subdomains_subdomain64blake3_subdomain_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_classifications_clasf_cover SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_pages_subdomain_page_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.subdomains_subdomain_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_subdomains_subdomain SET TABLESPACE ts_ssd1;
ALTER INDEX public.crawls_page_id_crawled_at_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_clasf_crawls_crawl_id_desc SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_crawled_at SET TABLESPACE ts_ssd1;
ALTER INDEX public.crawls_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.dolma_cleaned_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_htmls_crawl_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_dolma_cleaned_clasf_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_page_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.warc_paths_warc_path_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_warc_paths_warc_path SET TABLESPACE ts_ssd1;
ALTER INDEX public.clasf_crawls_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_classifications_clasf_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.pages_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.subdomains_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_clasf_crawls_crawl_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_subdomains_subdomain64blake3 SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_classifications_eng_tokens_dupe SET TABLESPACE ts_ssd1;
ALTER INDEX public.dolma_cleaned_metrics_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.page_dates_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.ads_counts_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_dolma_cleaned_passes_true SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_clasf_crawls_timestamp SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_extractions_clasf_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_ads_counts_low SET TABLESPACE ts_ssd1;
ALTER INDEX public.extractions_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_pages_subdomain_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_ok SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_w_browser SET TABLESPACE ts_ssd1;
ALTER INDEX public.blacklists_ut1_domains_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.detector_score_sets_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.warc_paths_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_crawls_ok_browser SET TABLESPACE ts_ssd1;
ALTER INDEX public.given_up_sites_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.links_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_links_search_result_id_page_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.redirections_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.search_query_hashes_index SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_site_pages_subdomain_timestamp_desc SET TABLESPACE ts_ssd1;
ALTER INDEX public.search_query_hashes_search_query_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.wikihow_articles_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_site_pages_subdomain_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.search_query_hashes_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_search_results_query_engine_result SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_search_results_query_id_engine_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.search_results_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_cc_idx_files_cc_idx_file_url SET TABLESPACE ts_ssd1;
ALTER INDEX public.cc_idx_files_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.baseline_correspondences_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.search_engines_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.search_engines_search_engine_name_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.blacklists_ut1_catalog_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_search_engines_name SET TABLESPACE ts_ssd1;
ALTER INDEX public.reviews_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.reviews_clasf_id_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.idx_reviews_clasf_id SET TABLESPACE ts_ssd1;
ALTER INDEX public.tags_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.site_tags_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.crawl_sources_crawl_src_name_key SET TABLESPACE ts_ssd1;
ALTER INDEX public.crawl_sources_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.version_n_timestamps_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.baseline_sites_pkey SET TABLESPACE ts_ssd1;
ALTER INDEX public.seed_versions_pkey SET TABLESPACE ts_ssd1;
```
