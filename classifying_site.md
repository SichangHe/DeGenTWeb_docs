# Classifying Websites

## Binoculars optimizations

- quantize Falcon-7B and Falcon-7B-instruct to `fp8`:
    hardly change Binoculars score, but faster&smaller
- group batch by similar #tokens & decide batch size from max#tokens

## SVM website classifier

`classifying/site_svm.py`

- webpage filtering
    - filter by a URL path regex to rid index page, tag page, etc.
    - filter by `Content-Type: text/html`
    - filter by English & \#tokens \> 200, etc. (`filter_non_article.md`)
- compute 9 Binoculars score deciles among webpage for each website
    - also tried 101 percentiles, 11 deciles, 5 quartiles, 3 quartiles;
        little difference
- train linear SVM classifier on deciles as feature vector
    - train on company/personal website dataset (`baseline_sites.md`)
    - out-of-distribution test on personal/company/other website dataset
    - [perfect performance in every
        combination](https://github.com/SichangHe/DeGenTWeb/issues/18#issuecomment-2810937177)
        - optionally filter by beforeGPT
- still perform well and high SVM-sureness when sampling fewer pages/site
- Binoculars SVMs very confident on baseline data
- ⇒ aggregate Binoculars score analysis perform well regardless of
    the noise in data (e.g., boilerplate page)
    - generalize across different kinds of website

### Closed six-score comparison

Keep the paper's Binoculars-only classifier. A frozen comparison added
Fast-DetectGPT, log probability, likelihood log-rank ratio, log rank, and
entropy. Each score contributed the same nine site-level percentiles, so the
alternative used 54 features instead of nine and also standardized its inputs
using training data only.

Both methods trained on the same 112 websites and correctly classified the
same separate 20 websites: ten human and ten AI-generated. Neither produced a
false positive among the ten human sites. This tie shows no observed benefit
from the larger method, but it does not establish equal performance elsewhere:

- the 20 test sites are small and record each generated site as paired with a
  human source site, so independence across all outcomes is unverified
- 20/20 accuracy has a 95% Wilson interval of 83.9–100% if examples are treated
  as independent; 0/10 false positives has an interval of 0–27.8%
- the alternative changed both detector inputs and scaling, so this comparison
  cannot separate their effects
- 54 features from 112 training sites provide more opportunity to fit this
  dataset than nine features do; the sites-per-feature ratios, 2.07 and 12.44,
  indicate this risk but do not measure overfitting

Paper wording:

> The existing Binoculars-only method and a method adding five related detector
> scores each correctly classified all ten human and all ten AI-generated test
> websites. Because the dataset pairs every generated test website with a human
> source website in the same test set, and because the larger method also
> changed score scaling, this result does not show whether added scores improve
> performance on unrelated websites.

The experiment is closed. Do not run another comparison unless a later paper
decision proposes replacing Binoculars. Such a comparison should prespecify its
required accuracy improvement and maximum false-positive rate, use a larger
test without recorded source relationships, and distinguish unscaled
Binoculars, scaled Binoculars, and the scaled six-score method.

## Applying in the wild

- full SVM model: train SVM on all baseline website,
    w/ 9 deciles (`classifying/full_site_svm.py`)
- aim for 20page/site but allow at least 15page/site

## Other detectors

- keeping: Fast-DetectGPT `fast_detect_gpt`, mean log probability `log_p`,
    likelihood log-rank ratio (LRR) `lrr`, mean log rank `log_rank`, entropy
    - only Fast-DetectGPT perform perfectly on baseline;
        others have \>90% accuracies
- FastNPR, RoBERTa, RADAR, intrinsicPHD, max probability performs badly:
    \<0.5 Pearson correlation w/ `is_generated` on baseline

### Crawling websites for classification

`browser/bing_search.py`

- Sample 1000 WikiHow article how-to questions as queries by SHA256.
- Search Bing API for 20 results for each query.
- For each result link, extract subdomain.
- For each subdomain, fetch the sitemap.
    - If no sitemap, fetch last 2000 pages from Wayback Machine CDX.
- Randomly sample pages from the sitemap to crawl until 20 non-filtered.
    - respect robots.txt
    - give up on 3 error connecting, e.g., DNS resolution failure,
        connection timeout
