# Classifying Websites

## SVM website classifier

`classifying/site_svm.py`

- webpage filtering
    - filter by a URL path regex to rid index page, tag page, etc.
    - filter by `Content-Type: text/html`
    - filter by English & \#tokens \> 200 (`filter_non_article.md`)
- compute 11 Binoculars score deciles among webpage for each website
    - also tried 101 percentiles, 9 deciles, 5 quartiles, 3 quartiles;
        little difference
- train linear SVM classifier on deciles as feature vector
    - train on company/personal website dataset (`baseline_sites.md`)
    - out-of-distribution test on personal/company/other website dataset
    - filter by beforeGPT for training?
    - [perfect performance in every
        combination](https://github.com/SichangHe/DeGenTWeb/issues/18#issuecomment-2810937177)
- ⇒ aggregate Binoculars score analysis perform well regardless of
    the noise in data (e.g., boilerplate page)
    - generalize across different kinds of website

## Applying in the wild

- full SVM model: train SVM on
    all baseline website (`classifying/full_site_svm.py`)

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
