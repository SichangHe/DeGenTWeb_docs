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
