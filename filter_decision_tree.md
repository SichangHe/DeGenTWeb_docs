# Filter Decision Tree Workflow

This document records the workflow for training the decision tree that
approximates the `DW_FILTER` predicate using baseline pages.

## Default workflow

Use the CLI helper that lives in the codebase:

```bash
uv run python -m degentweb.classifying.build_filter_tree
```

The command will:

- fetch up to 400 pages per subdomain (Russell 2000 ∪ IndieWeb ∪ Wix ∪ B12),
- train a decision tree with max depth 4 and minimum 20 samples per leaf, and
- print the tree structure, accuracy, confusion matrix, and
    classification report.

The defaults were chosen to mirror the existing `DW_FILTER` thresholds while
remaining simple enough to audit.
Running the script against the current Postgres snapshot typically yields
accuracy > 0.99.

## Custom hyperparameters

All key hyperparameters are exposed as flags:

```bash
uv run python -m degentweb.classifying.build_filter_tree \
  --sample-size 600 \
  --max-depth 5 \
  --min-samples-leaf 30
```

- `--sample-size` controls the maximum number of pages sampled per subdomain.
    The default is 400; values below 200 tend to reduce stability.
- `--max-depth` sets the tree depth cap (default 4).
- `--min-samples-leaf` enforces the minimum number of samples in
    a leaf (default 20).

## Persisting outputs

Two optional flags allow writing the results to disk:

- `--output-text path/to/summary.txt`
    writes the textual tree representation along with
    the chosen hyperparameters and metrics.
- `--output-json path/to/metrics.json`
    writes a machine-readable summary containing the description, accuracy,
    confusion matrix, classification report (`classification_report(...,
    output_dict=True)`), feature column names, and the list of
    baseline subdomains included in the run.

Example:

```bash
uv run python -m degentweb.classifying.build_filter_tree \
  --output-text data/filter_tree.txt \
  --output-json data/filter_tree.json
```

## Interpreting the results

- The textual tree highlights the thresholds that best mimic the `DW_FILTER`
    predicate; the defaults reinforce the existing heuristics:
    - `% large block > 75` remains a dominant split,
    - `n_tokens > 200`, `% list/table`, and `% relative dupe` continue to
        act as guard rails.
- The JSON payload is suitable for regression checks or
    future automation (e.g. comparing tree structure across datasets).

Whenever the script is re-run, review the produced metrics; if
accuracy drops or splits deviate significantly from expectations,
repeat the run with a larger sample size or
revisit the engineered features before updating production thresholds.
