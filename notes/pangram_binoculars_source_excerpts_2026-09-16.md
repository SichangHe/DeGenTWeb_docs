# Pangram and Binoculars source excerpts

(authored by agents unless marked 🧑)

This page preserves the exact source language cited by the comparison note.
The original paths identify artifacts in the parent DeGenTWeb repository; they
are plain text because that repository is not part of a standalone docs clone.

## Pangram analysis contract

Original path: `scripts/pangram_all_available_analysis.md`

> - site summary
>   - retains the first result when a text was checked repeatedly
>   - reports generated-site sensitivity evidence only
>   - does not estimate SVM accuracy without human-site Pangram percentages

## Full-corpus result packet

Original path:
`data/classify/full_corpus_svm_final_packet_20260915/final_result_packet.md`

> Prompts, reasoning settings, retained pages, and other generation conditions
> were not isolated, and this experiment does not measure model intelligence.
> Older whole-site results and the preliminary eight-Wix-site page-body run are
> not directly comparable.

## Bedrock experiment protocol

Original path: `codebase_index/bedrock_synth_site_eval.md`

> Purpose: generate 20-page synthetic sites from minimal prompts, wrap them in
> a fixed HTML shell, and run the DeGenTWeb extraction → Dolma → Binoculars
> → SVM path fully off-DB.

> Final controlled design: 5 site topics × 2 prompt styles per model-thinking
> config, with resumable JSONL artifacts at every stage.

The same protocol defines the prompt styles as `plain` and `quality` and records
the thinking controls for each condition.
