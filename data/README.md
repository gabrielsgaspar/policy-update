# Data Directory

Raw data is immutable and should not be tracked by Git.

## Layout

```text
data/raw/        Original HTML, PDF, JSON, WARC, API responses, and CDX records.
data/interim/    Parsed or intermediate files produced during extraction and cleaning.
data/clean/      Analysis-ready datasets when a clean layer is useful.
data/processed/  Relational tables, features, embeddings, labels, and validation sets.
data/analysis/   Issue-week panels, proposal-adoption panels, event-study panels, tables, and figures.
data/external/   External public datasets or manually downloaded reference data.
data/metadata/   Seed URLs, URL inventories, event calendars, and other small metadata tables.
data/docs/       Data-adjacent source notes, parser notes, and codebooks when they belong with data outputs.
```

## Rules

- Do not edit files under `data/raw/`.
- Store provenance for every fetched record.
- Use content hashes and source timestamps to version raw files.
- Keep restricted commenter metadata out of analysis tables.
- Prefer Parquet for analysis tables and DuckDB for local relational work.
- Document all source groups in `docs/DATA_SOURCES.md`.
