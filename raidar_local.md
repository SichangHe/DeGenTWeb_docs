# Local single-rewrite RAIDAR variant

- scope
  - ports a single-rewrite subset of RAIDAR's detector-side features
  - fuzzy scores reproduce fuzzywuzzy 0.18.0 pure-Python 0--100 behavior
  - fits logistic regression only on an explicit site-disjoint training split
  - evaluates only an explicit test split
- rewrite boundary
  - caller supplies the rewrite function or immutable precomputed rewrites
  - every rewrite binds original hash, rewrite hash, model identity, and prompt
  - mixed model or prompt identities fail closed
  - duplicate IDs and any cross-role original/rewrite hash reuse fail closed
  - no API, model download, database write, or implicit provider fallback exists
- old-baseline run
  - freeze the old baseline page manifest and site-level train/test split
  - choose and record one local rewrite model revision and one prompt
  - pass non-default model comparisons with matching `--model-id` and
    `--model-revision`; the snapshot directory name must equal that revision
  - exclude empty bodies before calling `rewrite_examples`
  - call `evaluate_raidar` on the resulting `RaidarRewrite` records
  - report its page metrics and mean-page-probability site metrics
  - or serialize those exact records as JSONL and run
    `python scripts/evaluate_raidar_offline.py rewrites.jsonl manifest.jsonl result.json`
  - the independent manifest binds each label, split, site, and original hash
  - the runner requires the imported detector to resolve to the hashed repository source
  - it binds the runner, detector, `pyproject.toml`, and `uv.lock` hashes
  - it binds Python, NumPy, SciPy, and scikit-learn runtime versions
  - source/config/lock drift during evaluation fails closed
  - it publishes with exclusive creation and cannot replace an existing artifact
- GPU handoff
  - wait until no other user's GPU job is running
  - run `sh pause_bino_server.sh`
  - verify the model server has released both GPUs
  - run the bounded RAIDAR rewrite job
  - whether it succeeds or fails, run `sh resume_bino_server.sh`
  - verify one model server owns the GPUs and regular scoring is running again
  - larger-model comparisons use `scripts/raidar_model_size_fence.py`
    - accepts only reviewed Qwen2 1.5B and 7B revisions
    - requires a matching immutable local snapshot inventory
    - preserves the historical 0.5B fence unchanged
    - each checkpointed window uses the same pause/resume handoff
- interpretation
  - this is a local single-rewrite variant, not exact parity with RAIDAR's
    upstream multi-rewrite feature layout or obsolete GPT-3.5 setup
  - an old-baseline result is blocked until a local rewrite model revision and
    prompt are approved, frozen, and used to produce immutable rewrites
  - L2D remains gated by its Gemma-2-9B-IT checkpoint and available GPU memory
