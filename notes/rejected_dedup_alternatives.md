# Rejected Deduplication Alternatives

This decision note records alternatives considered in August 2026. It does not
change the current site-local CDC rule, production behavior, stored data, or
scores.

## Similarity-heavy methods

The discussed “mean hash” method is **MinHash**, not a mean of hashes. Lee et
al. combine two corpus-global methods: a suffix array removes repeated spans of
at least 50 BPE tokens, while 5-gram MinHash finds candidate document pairs for
Jaccard and edit-similarity checks. Their selected near-duplicate rule requires
Jaccard and edit similarity above 0.8. The paper reports a 9,000-value MinHash
signature per document and substantial suffix-array resources: its 350 GB C4
run used about 1,000 CPU-hours and a 1.5 TB suffix array
([Lee et al., ACL 2022](https://aclanthology.org/2022.acl-long.577/)).

Newer semantic approaches are heavier still. SemDeDup embeds every document
with a pretrained model, clusters the embeddings with k-means, then performs
pairwise cosine-similarity comparisons within clusters
([Abbas et al., 2023](https://arxiv.org/abs/2303.09540)).

We are not adopting either family now. Applying Lee et al. faithfully would
require corpus-wide tokenization, indexes, candidate generation, and similarity
rescoring. Span removal would also change detector input and require detector
rescoring. An embedding adaptation would add model inference, clustering,
similarity computation, and a new semantic threshold. Those costs and policy
changes are excessive for this workflow. These are properties of the published
methods; a site-local adaptation would be a new project method, not “Lee et al.”
or “SemDeDup.”

## BFF-style Bloom filtering

DataComp-LM's modified Big Friendly Filter (BFF) tokenizes documents, checks
n-grams against a Bloom filter, and can remove paragraphs or documents when the
fraction already present exceeds a configurable threshold. Its documented
configuration uses a threshold of 0.8
([DataComp-LM, Appendix L](https://arxiv.org/abs/2406.11794),
[implementation](https://github.com/mlfoundations/dclm/blob/main/dedup/bff/src/my_main.rs#L97)).
The threshold is a DCLM/BFF configuration choice, not an inherent requirement
of Bloom filters or every BFF use.

We reject that 0.8-style gate for this project because it is too lenient: a
document with 79% already-seen n-grams would pass even though it is highly
similar to prior documents. Lowering the threshold or changing its scope could
address that example, but would be a project-specific adaptation requiring new
validation rather than adoption of the evaluated DCLM policy.

Decision: retain the current CDC rule. No implementation, rescore, data change,
or experiment follows from this note.
