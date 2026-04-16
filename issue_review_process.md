# Periodic GitHub issue review process

Use this when refreshing `docs/issue_reviews.md`.

## Goal

Record only still-useful analysis takeaways and unresolved analysis questions from GitHub issues. Skip paper-writing, pure infra/tooling, and stale directions.

## Incremental workflow

1. Read the `Last full issue+comment review` timestamp in `docs/issue_reviews.md`.
2. List only changed issues since then:

   ```sh
   gh issue list --state all --search 'updated:>2026-04-16T02:37:02Z' --limit 200 --json number,title,state,updatedAt,url
   ```

   `updatedAt` already moves when comments are added, so this usually captures new issue replies too.
3. Skip obvious non-analysis threads by title first: paper-writing, figure polish, infra, refactors, migrations, one-off bug fixes.
4. For each remaining issue, inspect the full thread:

   ```sh
   gh issue view <number> --comments
   ```

5. Keep only:
   - analysis results that still affect current understanding;
   - methodology decisions that changed interpretation of results;
   - unresolved analysis questions worth revisiting.
6. Do **not** keep:
   - stale directions that later comments effectively abandoned;
   - coordination chatter;
   - implementation details that did not change analysis conclusions.
7. Update `docs/issue_reviews.md` with:
   - a new dated section;
   - concise grouped takeaways;
   - a brief unresolved-issues list with issue links;
   - the new `Last full issue+comment review` timestamp.

## Heuristic for this repo

Usually include issues about baseline results, search-result analysis, Common Crawl/Webis experiments, filtering/dedup effects, detector trustworthiness, live-fetch measurements, dates/ads/blacklists, and monetization evidence. Usually skip paper-outline issues and most infra/tooling threads.
