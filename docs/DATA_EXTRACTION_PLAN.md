# Data Extraction Plan

This file defines the first systematic extraction tasks. It is a plan only; no data extraction has been executed yet.

## Principles

- Raw files are immutable.
- Save raw API responses, HTML, PDFs, JSON, and WARC files exactly as collected.
- Deduplicate by content hash, not only by URL.
- Keep source provenance for every record.
- Measure missingness as a research object, not a nuisance.
- Respect rate limits, terms of service, and privacy/ethics constraints.

## Phase A: Source Inventory

### A1. Build seed URL table

Output: `data/metadata/seed_urls.csv`

Required fields:

```text
seed_id
url
normalized_url
domain
source_group
expected_content_type
priority
first_seen_source
notes
```

Initial sources are listed in `DATA.md` and `docs/DATA_SOURCES.md`.

### A2. Query Wayback CDX

Outputs:

- `data/raw/wayback/cdx/beppegrillo_cdx.jsonl`
- `data/raw/wayback/cdx/blogdellestelle_cdx.jsonl`
- `data/raw/wayback/cdx/movimento5stelle_cdx.jsonl`
- parsed Parquet inventories in `data/interim/`

Acceptance checks:

- counts by domain, year, mimetype, and status code;
- duplicate capture strategy documented;
- candidate post, comment, archive, PDF, and irrelevant URLs classified.

### A3. Inspect Internet Archive item `BeppeGrillo.it2005`

Output: `docs/source_notes/internet_archive_beppegrillo_2005.md`

Acceptance checks:

- file structure documented;
- comment presence assessed;
- parseability relative to Wayback snapshots assessed;
- license/access constraints recorded.

## Phase B: URL Inventory

Output: `data/metadata/url_inventory.parquet`

Required fields:

```text
url
normalized_url
domain
source_type
first_seen_source
first_seen_at
candidate_year
candidate_month
candidate_slug
wayback_timestamp
cdx_digest
priority
notes
```

## Phase C: Raw Download

Output locations:

```text
data/raw/live/{source}/{YYYY}/{MM}/{content_hash}.html
data/raw/wayback/html/{domain}/{YYYY}/{MM}/{wayback_timestamp}_{content_hash}.html
data/raw/live/{source}/pdf/{YYYY}/{content_hash}.pdf
```

Downloader requirements:

- rate limits for live sources;
- Wayback timestamp/original URL support;
- retries and permanent-failure logs;
- content hash storage;
- fetch metadata table;
- no manual edits to raw files.

## Phase D: Parsing

Initial parser targets:

- current Beppe Grillo pages;
- legacy Beppe Grillo / Wayback templates;
- Il Blog delle Stelle pages;
- M5S programs and PDFs;
- parliamentary outputs from Chamber/Senate/Openpolis samples.

Each parser should emit:

- parser version;
- parse confidence;
- structured warnings;
- template type where relevant;
- raw path and content hash;
- completeness flags.

## Phase E: Pilot Corpus

Pilot windows:

- 2005-2006: early blog formation;
- 2007-2008: V-Day/proto-movement period;
- 2012-2013: electoral breakthrough.

Pilot outputs:

- parser success rate;
- comments recovered per post;
- archive coverage score;
- spam/duplicate rate;
- timestamp/order availability;
- issue-label and proposal-extraction validation sample;
- first lead-lag feasibility table, only after PI approval for analysis execution.

## Immediate Extraction Task Order

1. Create seed URL list.
2. Query Wayback CDX for Beppe Grillo domains.
3. Query Wayback CDX for Il Blog delle Stelle.
4. Inspect `BeppeGrillo.it2005`.
5. Build initial URL inventory.
6. Implement raw downloader.
7. Download pilot raw pages.
8. Implement first parsers.
9. Compute archive completeness metrics.
10. Produce pilot data report.
