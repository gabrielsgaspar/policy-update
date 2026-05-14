# TASKS.md

Last updated: 2026-05-14

## Purpose

This document is the canonical live task tracker for the Beppe Grillo blog / M5S digital-party responsiveness project. Tasks are grouped by phase and include concrete outputs and acceptance criteria.

Priority codes:

- **P0:** Required for the project to exist.
- **P1:** Required for the first serious pilot.
- **P2:** Important for the full paper but can wait until the pilot is viable.
- **P3:** Extension or polish.

Status codes:

- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[?]` blocked or uncertain

Governance rules:

1. The PI makes final research decisions.
2. Do not execute data collection, scraping, parsing, modeling, or empirical analysis unless the PI asks for that specific task.
3. Do not modify raw data.
4. If an output path is unclear, write `TBD` and add a task to resolve it.
5. Use `code/` as the primary implementation tree.
6. Keep `PROJECT.md`, `DATA.md`, `RESEARCH.md`, and `docs/*.md` aligned when tasks change the project memory.

## Current queue

### Completed setup

- `[x]` P0-001: Create project repository and governance structure.

### Recommended next tasks

1. `[ ]` P0-002: Freeze the first research design memo.
2. `[ ]` P0-004: Decide data ethics rules.
3. `[ ]` P0-101: Build seed URL list for core domains.
4. `[ ]` P0-102: Query Wayback CDX for Beppe Grillo domains.
5. `[ ]` P0-103: Query Wayback CDX for Il Blog delle Stelle.
6. `[ ]` P1-105: Inspect Internet Archive item `BeppeGrillo.it2005`.

## Phase 0: Research design and repository setup

### P0-001: Create project repository

- Status: `[x]`
- Output: Git repository with folders for `code/`, `data/`, `docs/`, `paper/`, `outputs/`, `.agents/`, `.claude/`, and `.cursor/`.
- Acceptance criteria:
  - Repository structure exists.
  - README explains project purpose, current stage, layout, data rules, and first milestone.
  - `.gitignore` excludes raw data, credentials, caches, derived data, and model outputs.
  - Research governance scaffold is available for Codex, Claude Code, and Cursor.
  - Project-specific content from `PROJECT.md`, `DATA.md`, and `TASKS.md` is preserved.
  - No research data collection or analysis is executed.

### P0-002: Freeze the first research design memo

- Status: `[ ]`
- Output: 2-4 page memo summarizing research question, hypotheses, data, empirical strategy, and risks.
- Acceptance criteria:
  - Defines the main outcome variables.
  - Defines the first pilot period.
  - Lists the first comparison groups.
  - Identifies the minimum viable dataset.

### P0-003: Build citation library

- Status: `[ ]`
- Output: Zotero/BibTeX library with must-cite papers.
- Acceptance criteria:
  - Includes representation/party responsiveness literature.
  - Includes political economy of media/internet literature.
  - Includes online feedback and agenda-setting literature.
  - Includes M5S/digital-party literature.
  - Includes text-as-data and LLM validation literature.

### P0-004: Decide data ethics rules

- Status: `[ ]`
- Output: Short ethics/data-handling protocol.
- Acceptance criteria:
  - Defines how commenter names are stored and hashed.
  - Defines what can be quoted in papers/presentations.
  - Defines whether raw comment data can be shared.
  - Defines restricted/raw data access rules.

## Phase 1: Source inventory

### P0-101: Build seed URL list for core domains

- Status: `[ ]`
- Output: `data/metadata/seed_urls.csv`
- Sources:
  - https://beppegrillo.it/
  - https://beppegrillo.it/blog/
  - https://beppegrillo.it/category/archivio/
  - https://beppegrillo.it/category/archivio/2005/
  - https://www.ilblogdellestelle.it/
  - https://www.movimento5stelle.it/
  - https://www.movimento5stelle.eu/
  - https://portale.movimento5stelle.eu/elezioni-trasparenti
- Acceptance criteria:
  - Each seed has source type, priority, notes, and expected content type.
  - Includes historical domain variants with `http`/`https` and `www`/non-`www`.

### P0-102: Query Wayback CDX for Beppe Grillo domains

- Status: `[ ]`
- Output: `data/raw/wayback/cdx/beppegrillo_cdx.jsonl` and parsed Parquet.
- Example query:
  - `https://web.archive.org/cdx?url=www.beppegrillo.it/*&output=json&fl=timestamp,original,statuscode,mimetype,digest,length&filter=statuscode:200&filter=mimetype:text/html&collapse=digest`
- Acceptance criteria:
  - CDX records stored raw and parsed.
  - Counts by year, mimetype, and domain variant reported.
  - Duplicate capture strategy documented.

### P0-103: Query Wayback CDX for Il Blog delle Stelle

- Status: `[ ]`
- Output: `data/raw/wayback/cdx/blogdellestelle_cdx.jsonl` and parsed Parquet.
- Acceptance criteria:
  - CDX records stored raw and parsed.
  - Counts by year and URL pattern reported.
  - Candidate legacy post URLs identified.

### P1-104: Query Wayback CDX for M5S official domains

- Status: `[ ]`
- Output: `data/raw/wayback/cdx/movimento5stelle_cdx.jsonl` and parsed Parquet.
- Domains:
  - `www.movimento5stelle.it`
  - `movimento5stelle.it`
  - `www.movimento5stelle.eu`
  - `movimento5stelle.eu`
  - `portale.movimento5stelle.eu`
- Acceptance criteria:
  - Program/campaign/platform pages are identified.
  - PDF and HTML outputs are separated.

### P1-105: Inspect Internet Archive item `BeppeGrillo.it2005`

- Status: `[ ]`
- Source: https://archive.org/details/BeppeGrillo.it2005
- Output: source note in `docs/source_notes/internet_archive_beppegrillo_2005.md`
- Acceptance criteria:
  - Determine file structure.
  - Determine whether comments are included.
  - Determine whether files are easier to parse than Wayback snapshots.
  - Record license/access constraints.

### P1-106: Build initial URL inventory table

- Status: `[ ]`
- Output: `data/metadata/url_inventory.parquet`
- Acceptance criteria:
  - Every candidate URL has normalized URL, domain, source type, first-seen source, date guess, priority, and notes.
  - Includes Wayback timestamp for archived records.
  - Deduplicates by normalized URL and content digest where available.

## Phase 2: Raw collection

### P0-201: Implement raw downloader

- Status: `[ ]`
- Output: `code/extract/download_raw.py`
- Acceptance criteria:
  - Downloads live URLs with rate limiting.
  - Downloads Wayback URLs using timestamp and original URL.
  - Stores raw files by source and content hash.
  - Writes fetch metadata to `fetches` table.
  - Retries transient failures and logs permanent failures.

### P0-202: Download pilot raw pages

- Status: `[ ]`
- Output: raw HTML for pilot windows.
- Pilot windows:
  - 2005-2006
  - 2007-2008
  - 2012-2013
- Acceptance criteria:
  - At least 300 candidate post pages downloaded if available.
  - At least 100 candidate pages with visible or recoverable comments identified if available.
  - Fetch success rate reported.

### P1-203: Download initial M5S programs

- Status: `[ ]`
- Output: raw program PDFs/HTML.
- Initial source:
  - 2013 M5S program PDF: https://www1.interno.gov.it/mininterno/export/sites/default/it/assets/files/25_elezioni/6_MOVIMENTO_5_STELLE.PDF
- Acceptance criteria:
  - 2013 program downloaded and text extracted.
  - Other program URLs inventoried for 2014, 2018, 2019, 2022, 2024.

### P1-204: Download initial parliamentary-output samples

- Status: `[ ]`
- Sources:
  - https://dati.camera.it/
  - https://www.senato.it/leggi-e-documenti
  - https://service.opdm.openpolis.io/api-openparlamento/v1/19/bills/
- Output: sample M5S-related bills/questions/motions.
- Acceptance criteria:
  - Identify how to filter by M5S group/MP.
  - Extract text for at least 100 parliamentary outputs.
  - Document official versus third-party source mapping.

## Phase 3: Parsing and database construction

### P0-301: Define database schema

- Status: `[ ]`
- Output: `code/db/schema.sql`
- Tables:
  - `sources`
  - `fetches`
  - `posts`
  - `comments`
  - `political_outputs`
  - `text_units`
  - `llm_labels`
  - `issue_labels`
  - `proposals`
  - `proposal_matches`
- Acceptance criteria:
  - Schema runs in DuckDB.
  - Primary keys and foreign keys are defined where practical.
  - Date/time fields are standardized.

### P0-302: Implement current Beppe Grillo parser

- Status: `[ ]`
- Output: `code/parse/parser_beppegrillo_current.py`
- Acceptance criteria:
  - Extracts title, date, author if present, body, category/tags, visible comment count if present.
  - Emits parser confidence and warnings.
  - Includes unit tests on saved HTML fixtures.

### P0-303: Implement legacy Beppe Grillo/Wayback parser

- Status: `[ ]`
- Output: `code/parse/parser_beppegrillo_legacy.py`
- Acceptance criteria:
  - Handles at least two historical templates.
  - Extracts comments where present.
  - Handles comment pagination if present.
  - Emits template type and completeness flags.

### P1-304: Implement Il Blog delle Stelle parser

- Status: `[ ]`
- Output: `code/parse/parser_blogdellestelle.py`
- Acceptance criteria:
  - Extracts post body and metadata.
  - Extracts comment threads if visible.
  - Links duplicate/mirrored posts to Beppe Grillo canonical URLs where possible.

### P1-305: Implement program/PDF parser

- Status: `[ ]`
- Output: `code/parse/parser_programs.py`
- Acceptance criteria:
  - Extracts text from PDFs.
  - Flags OCR-required documents.
  - Stores page-level text and document-level text.
  - Preserves raw PDF path and hash.

### P1-306: Implement parliamentary-output parser

- Status: `[ ]`
- Output: `code/parse/parser_parliament.py`
- Acceptance criteria:
  - Parses sample Chamber/Senate/Openpolis outputs.
  - Stores output type, actor, date, title, body, institution, legislature, and URL.
  - Can filter or tag M5S outputs.

### P0-307: Create archive completeness metrics

- Status: `[ ]`
- Output: `data/processed/archive_coverage.parquet`
- Acceptance criteria:
  - Counts captures per URL/post.
  - Estimates comment recovery ratio where visible comment counts exist.
  - Flags incomplete pagination.
  - Produces coverage score by post/thread.

## Phase 4: Pilot corpus and descriptive analysis

### P0-401: Build pilot corpus

- Status: `[ ]`
- Output: `data/processed/pilot_corpus.parquet`
- Acceptance criteria:
  - Includes posts, comments, and metadata for pilot windows.
  - Deduplicates mirrored or repeated archived pages.
  - Reports number of posts, comments, authors hashed, and source coverage by year.

### P0-402: Produce pilot data report

- Status: `[ ]`
- Output: `docs/source_notes/pilot_data_report.md`
- Acceptance criteria:
  - Reports post/comment recovery by year.
  - Reports parser success/failure by template.
  - Reports timestamp availability.
  - Reports spam/duplicate rates.
  - Identifies the best years and source types for scaling.

### P1-403: Create event calendar v0

- Status: `[ ]`
- Output: `data/metadata/event_calendar.csv`
- Acceptance criteria:
  - Includes M5S launch, V-Day events, national elections, 2013 parliamentary entry, 2018 government entry, and major site/platform changes.
  - Each event has source URL and issue tags.

### P1-404: Build preliminary media/public agenda controls

- Status: `[ ]`
- Output: `data/interim/media_controls_sample.parquet`
- Candidate sources:
  - Comparative Agendas Project: https://www.comparativeagendas.net/
  - Italian Policy Agendas Project page: https://www.comparativeagendas.info/page_id_62/
  - GDELT API: https://docs.gdeltcloud.com/api-reference/v2
  - Google Trends: https://trends.google.com/
- Acceptance criteria:
  - At least one feasible media/public attention control is selected for pilot issues.
  - Limitations are documented.

## Phase 5: Human coding and ML/LLM measurement

### P0-501: Define issue taxonomy

- Status: `[ ]`
- Output: `docs/codebooks/issue_taxonomy.md`
- Acceptance criteria:
  - Maps Comparative Agendas Project categories to M5S-specific issue categories.
  - Includes examples and decision rules.
  - Includes residual/unclear category.

### P0-502: Define proposal coding schema

- Status: `[ ]`
- Output: `docs/codebooks/proposal_schema.md`
- Acceptance criteria:
  - Defines what counts as a policy proposal.
  - Defines issue, target level, instrument, stance, specificity, evidence, local information, mobilization request.
  - Includes positive and negative examples.

### P0-503: Create human-coded gold standard v0

- Status: `[ ]`
- Output: `data/processed/validation_sets/gold_v0.parquet`
- Acceptance criteria:
  - At least 1,000 comments and 200 posts coded if feasible.
  - Stratified by year, issue, source, and comment volume.
  - Includes double-coding for a subset to measure human agreement.

### P0-504: Build LLM issue/proposal extraction pipeline

- Status: `[ ]`
- Output: `code/ml/llm_extract.py`
- Acceptance criteria:
  - Accepts text units and outputs valid JSON under a fixed schema.
  - Logs model, prompt, schema, date, and input hash.
  - Retries or flags invalid JSON.
  - Produces confidence fields.

### P1-505: Validate LLM labels

- Status: `[ ]`
- Output: `outputs/validation/llm_validation_v0.md`
- Acceptance criteria:
  - Reports precision, recall, F1 for issue labels and proposal detection.
  - Reports errors by year and issue.
  - Compares at least two model/prompt settings if feasible.
  - Identifies labels that require human review.

### P1-506: Generate embeddings

- Status: `[ ]`
- Output: `data/processed/embeddings/pilot_embeddings.parquet`
- Acceptance criteria:
  - Embeddings generated for posts, comments/proposals, and political outputs.
  - Model name/version recorded.
  - Similarity search can retrieve candidate matches from comments to outputs.

### P1-507: Build spam and duplicate filter

- Status: `[ ]`
- Output: `code/ml/filter_spam_duplicates.py`
- Acceptance criteria:
  - Flags obvious spam comments, link farms, duplicate text, and boilerplate.
  - Does not drop records permanently; stores flags and scores.
  - Reports sensitivity of pilot results to filtering.

## Phase 6: Empirical pilot

### P0-601: Build issue-week panel v0

- Status: `[ ]`
- Output: `data/analysis/issue_week_panels/issue_week_v0.parquet`
- Acceptance criteria:
  - Contains comment attention, post attention, and controls for pilot period.
  - Includes archive coverage score.
  - Includes movement phase indicators.

### P0-602: Estimate lead-lag agenda models

- Status: `[ ]`
- Output: `code/notebooks/lead_lag_pilot.ipynb` or `code/analysis/lead_lag_pilot.py` plus table.
- Acceptance criteria:
  - Tests whether comment issue attention predicts future post issue attention.
  - Includes lags of party attention.
  - Includes issue and time fixed effects where sample permits.
  - Includes future-comment placebo.

### P1-603: Build proposal-adoption panel v0

- Status: `[ ]`
- Output: `data/analysis/proposal_adoption_panels/proposal_adoption_v0.parquet`
- Acceptance criteria:
  - Extracts proposals from comments.
  - Searches for semantically similar later posts/outputs.
  - Hand-validates a sample of candidate matches.

### P1-604: Estimate proposal adoption model v0

- Status: `[ ]`
- Output: first adoption table and matched examples.
- Acceptance criteria:
  - Outcome is candidate/human-validated adoption in later M5S text.
  - Predictors include support volume, specificity, issue, local information, and phase.
  - Includes false-positive audit.

### P1-605: Run common-shock placebo tests

- Status: `[ ]`
- Output: placebo/robustness table.
- Acceptance criteria:
  - Compare M5S comments predicting M5S outputs versus comparison-party outputs.
  - Include simple media attention controls for pilot issues.
  - Include unrelated issue placebo.

## Phase 7: Scaling up

### P1-701: Scale crawler to full 2005-2013 corpus

- Status: `[ ]`
- Output: full pre-2013 corpus.
- Acceptance criteria:
  - Post/comment counts by year are reported.
  - Parser failure rate is below agreed threshold or failures are triaged.
  - Archive completeness metrics are computed.

### P2-702: Extend to 2013-2018 parliamentary period

- Status: `[ ]`
- Output: integrated corpus with parliamentary outputs.
- Acceptance criteria:
  - M5S parliamentary outputs are linked to MPs/groups.
  - Proposal matching works across comments, posts, programs, and parliamentary outputs.
  - Institutionalization break around 2013 can be estimated.

### P2-703: Build comparison-party corpus

- Status: `[ ]`
- Output: comparison-party text corpus.
- Acceptance criteria:
  - Includes programs and/or parliamentary outputs for PD, PDL/Forza Italia, Lega, Italia dei Valori, and other relevant parties.
  - Issue classification uses same taxonomy as M5S corpus.
  - Used in placebo/comparison models.

### P2-704: Add election/geography extension

- Status: `[ ]`
- Sources:
  - https://elezionistorico.interno.gov.it/
  - https://elezionistorico.interno.gov.it/eligendo/info_opendata.php
  - https://dait.interno.gov.it/elezioni/open-data
- Output: municipality-level M5S electoral dataset.
- Acceptance criteria:
  - Election results are merged to municipality identifiers.
  - M5S vote shares and turnout are available for relevant elections.
  - Geographic extension is feasible without deanonymizing commenters.

## Phase 8: Paper production

### P1-801: Write extended outline

- Status: `[ ]`
- Output: `paper/outline.md`
- Acceptance criteria:
  - Includes introduction, theory, data, measurement, empirical strategy, results, robustness, conclusion.
  - Identifies required figures and tables.
  - Identifies remaining evidence gaps.

### P2-802: Draft data/methods section

- Status: `[ ]`
- Output: `paper/sections/05_data.tex`
- Acceptance criteria:
  - Explains sources and archive missingness.
  - Explains LLM/ML validation.
  - Includes enough detail for replication.

### P2-803: Draft theory section

- Status: `[ ]`
- Output: `paper/sections/04_theory.tex`
- Acceptance criteria:
  - Defines digital parties as learning organizations versus mobilization machines.
  - Connects to representation, party responsiveness, and political economy literatures.
  - Generates testable hypotheses.

### P2-804: Create first results deck

- Status: `[ ]`
- Output: `presentations/pilot_results.pdf` or slides.
- Acceptance criteria:
  - Describes data recovery.
  - Shows validation performance.
  - Shows first lead-lag/proposal adoption evidence.
  - Lists next decisions.

## Immediate next 10 tasks

These are the tasks to do first, in order.

1. `[x]` Create repository and folder structure. `P0-001`
2. `[ ]` Freeze the first research design memo. `P0-002`
3. `[ ]` Decide data ethics rules. `P0-004`
4. `[ ]` Create seed URL list. `P0-101`
5. `[ ]` Query Wayback CDX for Beppe Grillo domains. `P0-102`
6. `[ ]` Query Wayback CDX for Il Blog delle Stelle. `P0-103`
7. `[ ]` Inspect `BeppeGrillo.it2005` Internet Archive item. `P1-105`
8. `[ ]` Build initial URL inventory table. `P1-106`
9. `[ ]` Implement raw downloader. `P0-201`
10. `[ ]` Define database schema. `P0-301`

## First milestone: feasibility decision

Target output: a short feasibility memo answering:

1. Can we recover comments at scale?
2. Which source has the best comment coverage?
3. Are comment dates/order reliable enough?
4. What share of comments contain policy-relevant content?
5. Can LLMs extract issues/proposals with acceptable precision?
6. Is there preliminary evidence that comment signals predict later party text?
7. What is the best first-paper sample: 2005-2013 only, or 2005-2018?

Decision rule:

- **Proceed to full paper:** comments are recoverable, timestamps/order are usable, and there is meaningful issue/proposal variation.
- **Pivot but continue:** comments are incomplete, but enough text exists to study participation rhetoric, platform governance, or the gap between participatory claims and observed responsiveness.
- **Stop or redesign:** comments are too sparse, timestamps are unusable, and no reliable output linkage can be built.
