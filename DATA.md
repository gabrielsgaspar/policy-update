# DATA.md

Last updated: 2026-05-16

## Purpose

This document describes the data sources, collection strategy, storage architecture, and initial data model for the Beppe Grillo blog / Five Star Movement digital-party responsiveness project.

The goal is to build a longitudinal corpus linking:

1. Citizen input: comments on Beppe Grillo/M5S online spaces.
2. Party communication: Grillo/M5S posts, campaign messages, platform materials, and programs.
3. Formal political outputs: bills, parliamentary questions, motions, speeches, and local/national programs.
4. External controls: media agenda, election results, Google Trends/search interest, other parties' outputs, and political events.

## Data principles

1. **Raw data is immutable.** Save raw HTML/PDF/JSON exactly as collected.
2. **Every record has provenance.** Store source URL, fetch timestamp, Wayback timestamp if applicable, parser version, content hash, and retrieval status.
3. **Do not overwrite.** Use content hashes and source timestamps to version data.
4. **Separate raw, parsed, and analysis layers.** Raw files should never be manually edited.
5. **Respect privacy and ethics.** Blog comments may be public, but commenters are ordinary people. Hash usernames in analysis data, avoid doxxing, and do not publish personally identifying comment metadata unless legally and ethically cleared.
6. **Measure missingness.** Archive gaps, deleted comments, moderation, and page migrations are central to the research design.
7. **Preserve reproducibility.** All parsers, prompts, model versions, and transformations must be versioned.

## Data architecture

Use a bronze/silver/gold architecture.

```text
data/
  raw/
    live/
      beppegrillo/
      blogdellestelle/
      movimento5stelle/
      parliament/
      election_results/
      media/
    wayback/
      cdx/
      html/
      warc/
      metadata/
    third_party/
      manifesto_project/
      comparative_agendas/
      openpolis/
      gdelt/
  interim/
    parsed_posts/
    parsed_comments/
    parsed_outputs/
    text_cleaning/
    language_detection/
    spam_detection/
  processed/
    relational/
    features/
    embeddings/
    llm_labels/
    validation_sets/
  analysis/
    issue_week_panels/
    proposal_adoption_panels/
    event_studies/
    figures/
    tables/
  docs/
    source_notes/
    parser_notes/
    codebooks/
```

Recommended local stack:

- Files: raw HTML/PDF/JSON stored on disk.
- Tables: DuckDB for local analysis; Postgres if multiple collaborators need concurrent access.
- Columnar data: Parquet for analysis-ready files.
- Large text search: SQLite FTS, DuckDB full-text extensions, or OpenSearch if the corpus becomes large.
- Embeddings: vector store optional; keep embeddings in Parquet with stable document IDs.
- Versioning: Git for code/docs; DVC or git-annex for data manifests if raw data becomes too large.

## Core source groups

## 1. Beppe Grillo blog posts and comments

### Live/current sites

Primary live sources:

- Beppe Grillo official site: https://beppegrillo.it/
- Blog landing page: https://beppegrillo.it/blog/
- Current archive category: https://beppegrillo.it/category/archivio/
- 2005 archive example: https://beppegrillo.it/category/archivio/2005/

Historical domain patterns to inventory:

- https://www.beppegrillo.it/
- http://www.beppegrillo.it/
- https://beppegrillo.it/
- http://beppegrillo.it/
- https://www.beppegrillo.it/archives/
- http://www.beppegrillo.it/archives/

Potential issue: current Beppe Grillo pages may preserve post bodies but not all historical comment threads. We should treat current pages as one source, not the authoritative complete source for comments.

Current BeppeGrillo.it feasibility slices: Wayback-based collection has recovered 507 candidate 2005 post paths with 507 successfully retrieved/parsed pages, 445 posts with parsed comments, and 270,151 parsed comments. The 2006 pass has recovered 468 candidate post paths, 439 successfully retrieved/parsed pages, 365 posts with parsed comments, and 442,328 parsed comments; 29 2006 post pages remain `no_successful_capture` after targeted retries. The 2007 pass has recovered 538 candidate post paths, 538 successfully retrieved/parsed pages, 326 posts with parsed comments, and 273,625 parsed comments; no 2007 post pages remain `no_successful_capture` in the current CDX-derived inventory. Raw HTML is stored under `data/raw/wayback/html/beppegrillo_{year}/`; interim parsed posts/comments and coverage audits are stored under `data/interim/` and `docs/source_notes/`.

### Il Blog delle Stelle

Primary source:

- Il Blog delle Stelle: https://www.ilblogdellestelle.it/

Historical/legacy patterns to inventory:

- https://www.ilblogdellestelle.it/YYYY/MM/slug.html
- http://www.ilblogdellestelle.it/YYYY/MM/slug.html
- https://www.ilblogdellestelle.it/20YY/MM/post-slug.html

Example legacy-style seed URL from prior inspection:

- https://www.ilblogdellestelle.it/2005/12/le_buone_azioni.html

Il Blog delle Stelle may preserve comment threads for posts that current Beppe Grillo pages do not. It should be crawled and archived carefully.

### Internet Archive / Wayback Machine

Use Wayback both interactively and programmatically.

Calendar views:

- https://web.archive.org/web/*/https://www.beppegrillo.it/*
- https://web.archive.org/web/*/http://www.beppegrillo.it/*
- https://web.archive.org/web/*/https://beppegrillo.it/*
- https://web.archive.org/web/*/https://www.ilblogdellestelle.it/*
- https://web.archive.org/web/*/https://www.movimento5stelle.it/*
- https://web.archive.org/web/*/https://www.movimento5stelle.eu/*

CDX API documentation:

- Internet Archive Wayback API page: https://archive.org/help/wayback_api.php
- CDX server documentation: https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md

Example CDX queries:

```text
https://web.archive.org/cdx?url=www.beppegrillo.it/*&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200&filter=mimetype:text/html&collapse=digest

https://web.archive.org/cdx?url=beppegrillo.it/*&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200&filter=mimetype:text/html&collapse=digest

https://web.archive.org/cdx?url=www.ilblogdellestelle.it/*&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200&filter=mimetype:text/html&collapse=digest

https://web.archive.org/cdx?url=www.movimento5stelle.it/*&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200&filter=mimetype:text/html&collapse=digest
```

For each CDX record, store:

- `timestamp`
- `original`
- `statuscode`
- `mimetype`
- `digest`
- `length`
- `source_domain`
- `cdx_query`
- `retrieved_at`

Then download archived pages using:

```text
https://web.archive.org/web/{timestamp}id_/{original_url}
```

Use `id_` mode to reduce Wayback rewriting where possible.

### Internet Archive item: BeppeGrillo.it 2005

A specific Internet Archive item appears to contain a 2005 BeppeGrillo.it archive:

- https://archive.org/details/BeppeGrillo.it2005

This should be inspected separately because it may contain bundled files that are easier to parse than Wayback snapshots.

## 2. M5S party outputs

### Official M5S sites

Current and historical domains:

- https://www.movimento5stelle.it/
- https://www.movimento5stelle.eu/
- https://portale.movimento5stelle.eu/
- https://portale.movimento5stelle.eu/elezioni-trasparenti
- https://www.movimento5stelle.eu/tag/programma/

Wayback inventory should be run for both `.it` and `.eu` domains because site structure changed over time.

### Campaign programs and official party documents

Known seed:

- 2013 M5S program PDF hosted by the Italian Interior Ministry: https://www1.interno.gov.it/mininterno/export/sites/default/it/assets/files/25_elezioni/6_MOVIMENTO_5_STELLE.PDF

Other programs to collect:

- National election programs: 2013, 2018, 2022.
- European election programs: 2014, 2019, 2024.
- Regional and municipal programs where available.
- Candidate lists and transparency files from M5S official portals.
- Platform consultation results and participant-facing materials when archived.

Storage:

```text
data/raw/live/movimento5stelle/programs/
data/raw/wayback/html/movimento5stelle/
data/interim/parsed_outputs/programs/
```

For each document, store:

- document type
- election type
- election date
- jurisdiction
- party/list name
- source URL
- archival URL if applicable
- raw file hash
- extracted text
- OCR flag if OCR was required

## 3. Parliamentary outputs

### Chamber of Deputies

Official open-data portal:

- https://dati.camera.it/
- https://data.camera.it/

The Chamber open-data portal should be used for:

- deputies
- parliamentary groups
- bills
- acts of direction/control
- sitting records
- votes where available
- legislature metadata

### Senate

Official Senate sources:

- Parliamentary records overview: https://www.senato.it/en/parliamentary-business/senate-work/parliamentary-records-electronic-format
- Laws and documents: https://www.senato.it/leggi-e-documenti

Collect:

- bills
- non-legislative documents
- questions
- interpellations
- motions
- sitting reports
- speeches where available

### Openpolis / OpenParlamento

Useful third-party source for structured parliamentary monitoring:

- Openpolis activities overview: https://www.openpolis.it/openpolis-foundation/activities/
- OpenParlamento API example for legislature 19 bills: https://service.opdm.openpolis.io/api-openparlamento/v1/19/bills/
- OpenParlamento GitHub repository: https://github.com/openpolis/openparlamento

Openpolis can be used as a structured convenience layer, but official Chamber/Senate sources should remain the canonical sources for formal outputs.

## 4. Election results

### Italian Interior Ministry / Eligendo

Official historical election archive:

- https://elezionistorico.interno.gov.it/
- Open-data information page: https://elezionistorico.interno.gov.it/eligendo/info_opendata.php
- Current election portal: https://elezioni.interno.gov.it/
- Interior Ministry election data/open-data page: https://dait.interno.gov.it/elezioni/open-data
- Historical-election overview: https://www.interno.gov.it/it/temi/elezioni-e-referendum/dato-storico-elezioni

Collect:

- national election results by municipality where available
- European election results
- regional election results
- municipal election results
- turnout
- candidate/list information
- M5S vote shares over time

Use cases:

- link online responsiveness to later electoral performance
- measure local M5S strength
- build geographic controls
- compare comment/geography signals with vote geography if commenter locations can be extracted ethically and reliably

## 5. Comparison parties

Comparison parties should help distinguish M5S-specific responsiveness from national issue shocks.

Initial parties/lists:

- Partito Democratico (PD)
- Popolo della Liberta / Forza Italia
- Lega Nord / Lega
- Italia dei Valori
- Fratelli d'Italia for later periods
- Other relevant parties depending on the election/year

Sources:

- official party websites and Wayback captures
- official campaign programs deposited with electoral authorities
- Manifesto Project corpus where available
- parliamentary outputs by party group
- newspaper coverage and press releases

## 6. Media and public agenda controls

Purpose: distinguish party learning from common public/media shocks.

Candidate sources:

### Comparative Agendas Project / Italian Policy Agendas Project

- Main CAP site: https://www.comparativeagendas.net/
- Italy project page: https://www.comparativeagendas.info/page_id_62/

Potential uses:

- issue taxonomy
- coded policy activities
- parliamentary questions, laws, budgets, prime minister speeches, party manifestos where available

### Manifesto Project / MARPOR

- Manifesto Project: https://manifesto-project.wzb.eu/

Potential uses:

- party manifesto text and coding
- comparison-party issue attention
- standard issue coding
- cross-party and cross-election benchmarks

### GDELT

- GDELT API documentation: https://docs.gdeltcloud.com/api-reference/v2

Potential uses:

- media attention controls
- story/entity trends
- Italian news coverage over time, subject to coverage-quality checks

### Google Trends

Potential source for public attention. Use cautiously because APIs are unofficial and indexes are normalized.

- Google Trends website: https://trends.google.com/
- Pytrends package page: https://pypi.org/project/pytrends/
- Pytrends GitHub: https://github.com/GeneralMills/pytrends

Use cases:

- issue search interest
- national public attention proxies
- local/regional search interest where available

### AGCOM media monitoring

- AGCOM observatories: https://www.agcom.it/osservatori

Potential uses:

- media-system context
- political communication/media exposure controls if usable datasets are available

## 7. Event calendar

Create a manually curated event calendar to control for major political and news shocks.

Initial event types:

- M5S organizational milestones
- V-Day events
- local election dates
- national election dates
- European election dates
- parliamentary entry
- government entry/exit
- major corruption scandals
- major economic crises/policy reforms
- major environmental/infrastructure conflicts
- major platform changes or site migrations

Table fields:

```text
event_id
date_start
date_end
event_type
title
description
source_url
relevance_issues
m5s_specific_flag
national_shock_flag
notes
```

## Relational schema

Use stable IDs that are independent of URLs where possible.

### `sources`

```text
source_id
source_name
source_type
base_url
owner_or_institution
notes
```

### `fetches`

```text
fetch_id
source_id
url
canonical_url
wayback_timestamp
retrieved_at
http_status
mimetype
content_hash
raw_path
cdx_digest
cdx_length
fetch_method
error_message
```

### `posts`

```text
post_id
source_id
fetch_id
url
canonical_url
title
author
date_published
date_modified
body_text
body_html_path
category
tags
visible_comment_count
language
parser_version
parse_confidence
notes
```

### `comments`

```text
comment_id
post_id
fetch_id
author_display_hash
author_raw_restricted
comment_timestamp
comment_date_confidence
comment_order
parent_comment_id
body_text
body_html_path
links
language
spam_score
moderation_marker
parser_version
parse_confidence
notes
```

### `political_outputs`

```text
output_id
source_id
fetch_id
output_type
actor
party
institution
legislature
date_published
date_introduced
title
body_text
jurisdiction
url
raw_path
parser_version
notes
```

### `text_units`

A general table for machine-learning measurement. Unit can be post, comment, paragraph, sentence, proposal, or output.

```text
text_unit_id
parent_type
parent_id
unit_type
unit_order
text
char_start
char_end
language
created_at
```

### `llm_labels`

```text
label_id
text_unit_id
model_provider
model_name
model_version
prompt_version
schema_version
run_timestamp
input_hash
output_json
valid_json_flag
human_review_status
confidence
notes
```

### `issue_labels`

```text
text_unit_id
issue_scheme
issue_major
issue_minor
probability
label_source
validated_flag
```

### `proposals`

```text
proposal_id
text_unit_id
post_id
comment_id
proposal_summary
issue_major
issue_minor
policy_instrument
target_level
stance
specificity_score
uses_evidence
contains_local_information
contains_mobilization_request
novelty_score
confidence
validated_flag
```

### `proposal_matches`

```text
match_id
proposal_id
output_id
matched_text_unit_id
match_method
embedding_model
similarity_score
cross_encoder_score
human_validated_match
match_date
lag_days
notes
```

### `issue_week_panel`

```text
issue_id
week_start
comment_attention
comment_volume
comment_unique_author_hashes
post_attention
post_volume
m5s_output_attention
comparison_party_attention
media_attention
google_trends_index
election_period_flag
movement_phase
archive_coverage_score
```

## Archive completeness measures

For each post/thread, compute:

```text
post_id
expected_comment_count_visible
parsed_comment_count
comment_count_ratio
number_of_captures
first_capture_timestamp
last_capture_timestamp
capture_span_days
template_type
has_comment_pagination
pagination_complete_flag
archive_source_count
coverage_score_0_to_1
notes
```

This measure is analytically important. Archive completeness should be used in robustness tests and possibly as a weight or sample restriction.

## Comment privacy and restricted fields

Suggested practice:

- Store raw author strings only in a restricted raw table or encrypted file if necessary for deduplication.
- In analysis tables, use salted hashes of display names.
- Do not attempt to deanonymize commenters.
- Do not publish individual-level commenter histories unless cleared by ethics/legal review.
- When publishing examples in the paper, paraphrase ordinary citizen comments unless the comment is from a public figure or permission/legal basis is clear.

## Initial crawl strategy

### Step 1: build seed inventory

Sources:

- current Beppe Grillo archive pages
- current Il Blog delle Stelle pages
- current M5S pages
- Wayback CDX domain queries
- Internet Archive item `BeppeGrillo.it2005`
- existing sitemap files if available
- internal links found during crawl

Output:

```text
data/metadata/url_inventory.parquet
```

Fields:

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
priority
notes
```

### Step 2: classify URL types

URL types:

- blog post
- archive listing
- comment page
- comment pagination
- tag/category page
- media file
- PDF/program
- parliamentary document
- irrelevant

### Step 3: download raw files

- Respect robots, terms of service, and rate limits for live sources.
- Use Wayback CDX for archived sources.
- Keep retry logs.
- Deduplicate by content hash, not only URL.

### Step 4: parse posts/comments

Build source-specific parsers:

- `parser_beppegrillo_current`
- `parser_beppegrillo_legacy_wayback`
- `parser_blogdellestelle_current`
- `parser_blogdellestelle_legacy`
- `parser_movimento5stelle_programs`
- `parser_camera_outputs`
- `parser_senato_outputs`

Each parser should emit confidence scores and structured warnings.

### Step 5: text normalization

Keep both raw and normalized text. Normalization should include:

- HTML stripping
- whitespace normalization
- quote/comment markup removal where appropriate
- language detection
- duplicate detection
- spam detection
- boilerplate removal
- URL extraction

### Step 6: feature generation

Generate:

- issue labels
- proposal extractions
- embeddings
- sentiment/stance labels
- deliberative-quality labels
- named entities
- geographic entities
- author-hash activity metrics

### Step 7: analysis panels

Construct:

- issue-week panels
- proposal-adoption panels
- post-thread panels
- source-completeness panels
- comparison-party panels

## File naming conventions

Raw live pages:

```text
data/raw/live/{source}/{YYYY}/{MM}/{content_hash}.html
```

Raw Wayback pages:

```text
data/raw/wayback/html/{domain}/{YYYY}/{MM}/{wayback_timestamp}_{content_hash}.html
```

Raw PDFs:

```text
data/raw/live/{source}/pdf/{YYYY}/{content_hash}.pdf
```

Parsed tables:

```text
data/interim/parsed_posts/{source}_{parser_version}.parquet
data/interim/parsed_comments/{source}_{parser_version}.parquet
```

Analysis datasets:

```text
data/analysis/issue_week_panels/issue_week_{YYYYMMDD}.parquet
data/analysis/proposal_adoption_panels/proposal_adoption_{YYYYMMDD}.parquet
```

## Pilot sample design

The first pilot should not attempt full coverage. It should test feasibility and measurement validity.

Pilot windows:

1. 2005-2006: early blog formation.
2. 2007-2008: V-Day/proto-movement period.
3. 2012-2013: electoral breakthrough.

Pilot selection:

- 50 high-comment posts per window if available.
- 50 randomly selected posts per window.
- all comments for selected posts where recoverable.
- all subsequent posts within 30, 90, and 180 days.
- initial M5S program and parliamentary outputs around 2013.

Pilot outputs:

- parser success rate
- comments recovered per post
- archive coverage score
- spam rate
- proposal prevalence
- issue-label accuracy
- proposal-extraction accuracy
- first lead-lag correlation table

## Known uncertainties to resolve

1. Which historical pages preserve full comment threads?
2. Are comment timestamps available for all periods or only ordering?
3. Does comment pagination exist, and can it be recovered from Wayback?
4. Did site migrations alter URLs or remove comments?
5. Are there duplicate comment mirrors across BeppeGrillo.it and Il Blog delle Stelle?
6. Can we distinguish ordinary comments from staff responses, trackbacks, and automated spam?
7. Which official M5S outputs are archived with enough timestamp precision to test adoption?
8. How much of the parliamentary output can be reliably linked to M5S MPs and groups?
9. Which media control source has sufficient Italian coverage back to 2005?

## Data deliverables

Initial deliverables:

1. `url_inventory.parquet`: all candidate URLs and Wayback captures.
2. `posts.parquet`: parsed posts with metadata.
3. `comments.parquet`: parsed comments with hashed author identifiers.
4. `political_outputs.parquet`: programs and parliamentary outputs.
5. `archive_coverage.parquet`: source completeness and missingness metrics.
6. `issue_labels.parquet`: issue classifications with probabilities.
7. `proposals.parquet`: extracted policy proposals from comments.
8. `proposal_matches.parquet`: candidate links from comments to later outputs.
9. `issue_week_panel.parquet`: main panel for agenda responsiveness.
10. `validation_gold.parquet`: human-coded validation sample.

## Minimum viable dataset for first analysis

The minimum viable dataset should contain:

- at least 1,000 blog posts across 2005-2013
- comment threads for a meaningful subset of posts
- at least 50,000 parsed comments, if recoverable
- post/comment dates or reliable ordering
- issue labels for posts and comments
- proposal extraction for comments
- media controls for major issues
- M5S program and 2013 parliamentary outputs
- comparison-party or placebo text data

The exact sample size target should be revised after the first crawl.
