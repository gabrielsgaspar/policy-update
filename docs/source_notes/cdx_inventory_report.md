# Wayback CDX Inventory Report

Last updated: 2026-05-14

## Scope

This report summarizes the first approved feasibility-only Wayback CDX inventory. It collects archive metadata only: no archived HTML pages, PDFs, or comment bodies were downloaded.

## Scripts

- `code/extract/build_seed_urls.py`
- `code/extract/query_wayback_cdx.py`
- `code/extract/build_url_inventory.py`

## Generated Metadata Outputs

- `data/metadata/seed_urls.csv`
- `data/raw/wayback/cdx/beppegrillo_cdx.jsonl`
- `data/raw/wayback/cdx/blogdellestelle_cdx.jsonl`
- `data/raw/wayback/cdx/movimento5stelle_cdx.jsonl`
- `data/raw/wayback/cdx/movimento5stelle_pdf_cdx.jsonl`
- `data/raw/wayback/cdx/cdx_failures.jsonl`
- `data/interim/cdx/*_cdx.csv`
- `data/interim/cdx/*_cdx.parquet`
- `data/metadata/cdx_inventory_summary.csv`
- `data/metadata/url_inventory.parquet`
- `data/metadata/url_inventory_sample.csv`
- `data/metadata/url_inventory_type_summary.csv`

Raw/interim data files are generated artifacts and are intentionally excluded from Git where applicable.

## Main Findings

### BeppeGrillo.it

For the pilot window `2005-2013`, both `www.beppegrillo.it/*` and `beppegrillo.it/*` hit the per-query cap of 50,000 CDX records. After URL/digest deduplication, the initial URL inventory classifies Beppe Grillo records as:

- `blog_post_candidate`: 24,786
- `unclassified_html_candidate`: 22,615
- `archive_listing_candidate`: 1,216
- `homepage_candidate`: 1,337
- `comment_page_candidate`: 42

Interpretation: BeppeGrillo.it has substantial Wayback coverage in the target period, enough to support a pilot sampling strategy. Because the query hit the cap, a full inventory should later use pagination/resume keys or narrower year/month URL queries.

### Il Blog delle Stelle

The CDX metadata currently available in raw inventory includes 279,693 records across all years, with sparse coverage in the first-paper pilot period:

- 2012: 47 records
- 2013: 39 records

The URL inventory classifies Il Blog delle Stelle records as:

- `blog_post_candidate`: 186,052
- `pagination_candidate`: 13,738
- `comment_page_candidate`: 9,635
- `archive_listing_candidate`: 2,635
- `unclassified_html_candidate`: 66,886

Interpretation: Il Blog delle Stelle is unlikely to be central for 2005-2013 input recovery, but it appears important for later-period platform/migration checks and may help diagnose duplicate mirrors or post-2013 comment structures.

### M5S Official Domains

For `2005-2013`, M5S official HTML CDX coverage is modest:

- `movimento5stelle.it`: 71 records
- `www.movimento5stelle.it`: 71 records
- `movimento5stelle.eu`: 15 records
- `www.movimento5stelle.eu`: 15 records
- `portale.movimento5stelle.eu`: 0 records

After deduplication, the URL inventory classifies M5S records as:

- `homepage_candidate`: 64
- `m5s_page_candidate`: 22

PDF CDX checks returned zero records for several domains and timed out for `movimento5stelle.it/*` and `portale.movimento5stelle.eu/*`; failures are logged in `data/raw/wayback/cdx/cdx_failures.jsonl`.

Interpretation: for the 2013 output spine, official program PDFs and parliamentary/official sources outside Wayback will likely be more useful than M5S domain CDX alone.

## Duplicate Strategy

The initial URL inventory normalizes URLs by:

- lowercasing scheme/domain;
- removing default ports `:80` and `:443`;
- stripping trailing slashes except root;
- sorting query parameters;
- removing fragments;
- grouping by `normalized_url` and CDX digest.

This is a first-pass deduplication only. Later pilot parsing should add title/date/slug matching, body-text hashes, and near-duplicate text checks to identify BeppeGrillo.it and Il Blog delle Stelle mirrors.

## Quality Flags

- Beppe Grillo CDX queries hit the 50,000-record cap for both domain variants.
- Il Blog delle Stelle raw metadata includes post-2013 records because an initial unbounded metadata-only query completed before the bounded pilot query. This is not page scraping, but later summaries should filter explicitly to the analysis window.
- Two M5S PDF CDX requests timed out with 504 errors and need targeted retries.
- CDX metadata alone does not prove comment recoverability; archived page download and parser audits are still required.

## Next Implementation Step

Use `url_inventory.parquet` to sample candidate Beppe Grillo blog posts/comment pages in the three approved pilot windows, then implement the raw downloader and parser fixtures. Do not begin empirical analysis until comment recoverability, timing/order, source restrictions, and measurement validation are assessed.

