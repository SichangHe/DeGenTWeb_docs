# Recent WebConf papers to read with DeGenTWeb

## Recommendation

Read four papers together, in this order:

1. **Cheng et al., “Beyond Binary” (WebConf 2025).** This is the core read. It gives us the closest recent WebConf treatment of the difference between fully generated, extended, polished, and human text. Start with Sections 1 and 3, then read Sections 4.3–4.6 closely. [ACM DOI](https://doi.org/10.1145/3696410.3714770) · [author manuscript](https://arxiv.org/abs/2410.14259)
2. **Aljebreen, Meng, and Dragut, “Analysis and Detection of ‘Pink Slime’ Websites in Social Media Posts” (WebConf 2024).** This is the closest read on repeated observations, aggregation, and source dependence. Read Sections 3–4 for the units and sampling, Section 5.2 for post–article segmentation, and Sections 6.3–6.6 for outlet-grouped evaluation and URL-level majority voting. [ACM DOI](https://doi.org/10.1145/3589334.3645588) · [full manuscript](https://openreview.net/pdf?id=l60zHxOkcI)
3. **Park et al., “Adversarial Style Augmentation” (WebConf 2025).** Read this for its adaptive style-robustness test, not for its fake-news task. Focus on Sections 3.1–3.3, Tables 2–3 and 5–6, and the ethics discussion. [ACM DOI](https://doi.org/10.1145/3696410.3714569) · [author manuscript](https://arxiv.org/abs/2406.11260)
4. **Huang et al., “RU-AI” (WebConf 2025 Companion).** This is a short design-review paper. Its paired source records, generator inventory, data-flow figure, and noise variant are useful. Its benchmark scores are not. [ACM DOI](https://doi.org/10.1145/3701716.3715306) · [author manuscript](https://arxiv.org/abs/2406.04906)

This set came from a title-and-abstract sweep of the 2024–2026 WebConf proceedings, followed by full reads of the selected primary papers. **Industrialized Deception** is an optional fifth read, after the four above. It is lower priority than Pink Slime because it supplies framing and controlled-stimulus provenance, not an aggregation or web-measurement method. If time permits, read Sections 3.6 and 4, then the provenance paragraph in Section 5. [ACM DOI](https://doi.org/10.1145/3774905.3795471) · [author manuscript](https://arxiv.org/abs/2601.21963)

## What each paper contributes

### 1. Beyond Binary: define the target before tuning the detector

The paper separates role recognition from an involvement score. Its four roles are human author, LLM creator, LLM polisher, and LLM extender. That taxonomy fits the central ambiguity in “LLM-dominant” better than a single human/AI label. The paper’s best lesson is also its warning: “distinguishing between LLM-Polisher and Human-Author texts remains challenging” (p. 8, §4.6).

Its benchmark starts from 16,076 human news articles and creates three Llama-3 derivatives per article, for 64,304 records. Fine-tuned models score almost perfectly in-domain, but cross-domain performance drops sharply. The paper does not study webpages, extraction, natural base rates, site aggregation, low-FPR operation, or prevalence. Its random 7:2:1 split is not described at the source-family level, so related variants may cross splits. One pair of tables also disagrees on model-specific involvement-error values.

**Use it for:** a graded authorship target, explicit transfer tests, and separate evaluations for separate inferential tasks.

**Do not transfer:** its synthetic in-domain accuracy to live webpages, sites, or population estimates. Its Jaccard-based involvement label is a transformation proxy, not measured human effort.

### 2. Pink Slime: evaluate dependence and aggregation at the correct unit

The paper begins with known outlet lists: 1,313 Pink Slime outlets, 50 local outlets, and 25 national outlets. It collects posts linking to their articles, compares post text with the linked title and body, and predicts whether a post links to a Pink Slime outlet. Its five-fold evaluation groups posts by outlet, so an outlet does not supply posts to both train and test folds (p. 7, §6.3). This is a concrete precedent for splitting at a source-level dependency rather than randomly splitting records.

The aggregation experiment first predicts individual posts, groups posts that share an article URL, and assigns every post in a group the majority predicted label; ties are random (p. 8, §6.6). The prose reports that this collective label becomes perfect at around 100 posts per URL, but Figure 11's caption calls the horizontal unit the number of common URLs. That internally inconsistent unit makes the result useful as a question, not a transferable performance claim: when do repeated observations cancel independent errors, and when do shared source or template effects make the errors correlated?

The analogy to DeGenTWeb stops at the hierarchy. Pink Slime aggregates posts to one article URL; DeGenTWeb aggregates pages to a site. Pink Slime's label comes from a curated outlet list, not measured machine authorship. Its features include post structure, posting time and engagement, plus post–article copying patterns; it does not validate webpage extraction or a generated-text detector. Its closed, known-outlet experiments report accuracy and F1, not calibration, a low-FPR operating point, prevalence, or uncertainty for an open-web population. The random tie rule and the restricted equal-size URL groups also leave the aggregation result under-specified for deployment.

**Use it for:** source-grouped splits, an explicit record-to-entity hierarchy, and a direct experiment on how correlated errors change under aggregation.

**Do not transfer:** its Pink-Slime labels, post features, URL-level majority-vote accuracy, or known-outlet sampling frame to machine authorship, site labels, low-FPR performance, or web prevalence.

### 3. Adversarial Style Augmentation: test nuisance changes without changing the claim

AdStyle's order matters. In each round, an LLM first generates candidate style-conversion prompts from prior prompt–prediction-confusion-score pairs (the first round uses predefined prompts). Every candidate is then applied to a small subset of the training data and scored. The method jointly selects top-*k* prompts for adversarialness, coherency, and diversity, applies only those selected prompts to the full training data, and retrains the detector before the next round. The three criteria appear in Figure 1's caption on paper page 3; their selection procedure begins in §3.3 on paper page 4. This is a useful adaptive pattern for finding brittle style features. Its evaluation pairs clean and attacked results, includes low-data settings, tests a second rewrite model, and ablates the search loop.

But its label is veracity, not text origin. A style rewrite can preserve whether an article is true while changing whether its prose is machine-generated. Its balanced benchmarks and AUROC results say nothing about extreme web base rates or a chosen low-FPR threshold. Its 80/20 splits, generated attacks, and single-value tables do not establish open-web or temporal generalization.

**Use it for:** an adaptive held-out stress suite for tone, publisher-like register, structure, summarization, and paraphrase.

**Do not transfer:** fake/real labels, AUROC values, or robustness claims to generated-text attribution. Never rewrite a human negative with an LLM and retain a pure-human label.

### 4. RU-AI: make the data lineage auditable

RU-AI constructs aligned human and generated text, image, and voice records from public datasets and five generators per modality. The paper is unusually concrete about transformations and noise. For text, however, “Text is generated through rephrasing caption text” (p. 2, Fig. 1), and generated captions average roughly 17–27 words. That is far from heterogeneous extracted webpage prose.

The paper uses random 80/20 record splits. It reports no held-generator, held-domain, temporal, or source-grouped test; no calibration, uncertainty, or operational FPR; and no site aggregation. Counts and units are not fully consistent. Its prose calls 84.20 the best LanguageBind F1, while Table 4 places 84.20 under accuracy and precision. Noise effects also vary much more than its blanket summary suggests.

**Use it for:** a compact lineage diagram, paired records, explicit generator inventory, and versioned perturbation sets.

**Do not transfer:** its mid-80s balanced-benchmark metrics or character-noise results to webpage prose, web-scale robustness, or prevalence.

### 5. Industrialized Deception: optional framing, not a core precedent

The paper’s RogueGPT tool records prompts, model settings, style, and format for controlled news stimuli. JudgeGPT records graded judgments of origin and truthfulness along with response time and participant attributes. The paper states that “provenance proves origin, not truth” on paper page 5 in §3.6 and repeats it on paper page 6 under “Provenance and Authenticity Infrastructure,” an unnumbered subsection of §5. That boundary is the reason to keep this paper as optional framing.

This companion paper is mainly an update and synthesis. Its reported human-perception results point to companion studies and omit the sample and uncertainty details needed to reuse the numbers. It contains no web census, detector validation, aggregation study, or low-base-rate analysis.

**Use it for:** complete generation metadata, graded audit judgments, and the origin-versus-truth boundary.

**Do not transfer:** claims about misinformation, deceptive intent, coordination, trust erosion, or ecosystem harm to sites detected by DeGenTWeb.

## How I would rewrite the DeGenTWeb story

The paper should make one narrow claim well: **we estimate the share and characteristics of sites whose retained, extractable prose is mostly machine-generated within two defined web cohorts, using a transparent page-to-site pipeline evaluated at a deliberately low false-positive operating point.** Everything else should support or bound that claim.

1. **Define four levels of inference.** Show the path from extracted span, to page score, to site label, to cohort estimate. Give each level its own unit, denominator, error question, and limit. A single pipeline figure can make this legible.
2. **Name the authorship boundary early.** “LLM-dominant” excludes ordinary polishing and light assistance. Say what evidence can distinguish creator, extender, and polisher cases, and where the detector cannot.
3. **Make low FPR the evaluation spine.** Lead with FPR and recall at the frozen threshold, expected false positives per 10,000 or million sites, precision under plausible base rates, and uncertainty. AUROC and balanced accuracy can follow.
4. **Separate validation from measurement.** Ground-truth performance, historical negative controls, page-to-site aggregation, Common Crawl estimates, and Bing estimates answer different questions. Do not blend them into one accuracy narrative.
5. **Put the sampling boundary next to every prevalence number.** Use “retained Common Crawl sites” and “retained sites from WikiHow-style Bing queries,” with the qualifying-page rule and filtered-out share nearby.
6. **Label explanations as explanations.** If a result suggests SEO, monetization, common templates, or producer clustering, say what was observed and what would require a separate causal or network study.
7. **End with detector shelf life, not broad social harm.** Show exactly how performance changes by generator and editing condition, then state what must be recalibrated. Do not infer falsity or bad intent from likely machine origin.

## Research work that would most improve the paper

### Before submission

1. **Build graded, webpage-native ground truth.** Include dominant generation, extension, repeated polishing, light editing, and human-only controls. Preserve extraction artifacts, templates, quotations, and boilerplate. Report disagreement rather than forcing every ambiguous page into a binary label.
2. **Split by the real dependency unit.** Keep pages, variants, near-duplicates, and templates from the same source or site on one side of a split. State the split key. Add held-generator, held-prompt, held-domain, held-language, and forward-in-time tests.
3. **Audit the aggregation rule.** Measure page errors and then show how they propagate as the page count, affected-page fraction, page genre, and site threshold change. Report whether a few long pages or many weak signals drive a site verdict.
4. **Run a web-realistic robustness suite.** Include light human edits, LLM paraphrases, translation, publisher-style rewrites, copied passages, templated SEO prose, and extraction failures. Keep character noise as a secondary diagnostic. Freeze a held-out test set so adaptive prompt search cannot tune to it.
5. **Report deployment metrics.** Give threshold sensitivity, PR curves, calibration, absolute false-positive counts, and prevalence sensitivity under alternative plausible FPRs. Attach uncertainty to site shares and trends.
6. **Use hard negative controls.** Test pre-LLM archived prose, translated text, low-quality human writing, templated human sites, and difficult genres. Manually inspect false positives to see whether the model detects topic, fluency, translation, or templates rather than origin.
7. **Version the full measurement stack.** Record detector, tokenizer, extraction code, generator family, prompts, threshold, collection date, and cohort definition. That makes a later drift audit possible.

### Follow-up work, not required for the core claim

- Add image or metadata signals only if they improve site decisions at the required FPR. Multimodality is not automatically better.
- Study clusters or coordinated publishing only with independent network and behavioral evidence. Similar machine-generated prose alone does not establish common control.
- Study user trust or harm with a separate perception design. DeGenTWeb’s detector estimates likely origin, not truth or impact.
- Re-run the Pink Slime aggregation question at DeGenTWeb's actual hierarchy: estimate error correlation among pages from one site, compare several transparent page-to-site rules, and evaluate them on site-labeled ground truth without importing Pink Slime's reported accuracy.

## Questions for a joint reading meeting

1. Is “LLM-dominant” a binary site property, or should the paper report a graded dominant/extended/polished taxonomy?
2. Which source and site dependencies must be grouped before any train/test split?
3. What false-positive count would make the web estimates scientifically credible at the observed base rate?
4. Which perturbations preserve DeGenTWeb’s authorship label, and which create a new mixed-authorship label?
5. What part of the reported trend survives a plausible range of detector drift and site-level FPR?
6. Which ecosystem findings are direct measurements, and which should move to hypotheses or follow-up work?

## Bottom line

The four core papers and optional framing paper do not validate DeGenTWeb. Together they show how to define degrees of machine involvement, test dependence and aggregation, stress style and domain shifts, expose data lineage, and keep origin separate from truth or harm. DeGenTWeb’s contribution remains the part none of them supplies: transparent webpage processing, validated page-to-site aggregation, low-FPR evaluation, and bounded measurement of real web cohorts.
