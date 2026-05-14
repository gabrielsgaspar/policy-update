# Code Directory

This is the primary implementation tree for the project.

## Layout

```text
code/extract/    Source inventories, CDX queries, downloaders, and raw fetch metadata.
code/parse/      Source-specific parsers for posts, comments, programs, and political outputs.
code/clean/      Text normalization, deduplication, language detection, and spam flags.
code/build/      Dataset construction and panel-building scripts.
code/analysis/   Empirical analysis scripts.
code/ml/         Issue labels, proposal extraction, embeddings, validation, and matching.
code/db/         DuckDB schema and database utilities.
code/utils/      Shared helpers.
code/tests/      Unit tests and parser fixtures.
code/notebooks/  Exploratory notebooks, only when scripts are not yet appropriate.
```

Future code should keep raw-data writes, parsing, cleaning, and analysis in separate modules.
