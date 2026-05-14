# Empirical Plan

## Main Empirical Table / Figure Plan

Planned outputs, conditional on data recovery:

- source inventory counts by domain, year, source type, and archive status;
- post/comment recovery table by year and template;
- archive completeness figure by source and period;
- issue attention time series for comments, posts, M5S outputs, media/public controls, and comparison parties;
- lead-lag agenda responsiveness table;
- proposal extraction validation table;
- proposal adoption candidate-match table;
- placebo and robustness table;
- institutionalization heterogeneity figure around 2009, 2013, and 2018.

No empirical outputs have been generated yet.

## Main Specification

See `docs/IDENTIFICATION.md`.

## Secondary Specifications

- proposal-level event history;
- semantic responsiveness using within-issue embeddings;
- explicit acknowledgement detection;
- comparison-party placebo models;
- archive-completeness weighted or restricted models.

## Heterogeneity

Candidate heterogeneity dimensions:

- movement phase: 2005-2007, 2007-2009, 2009-2012, 2013-2017, 2018-2021;
- issue area: anti-corruption, transparency, public services, environment, infrastructure, digital democracy, media criticism, local governance, and other categories TBD;
- proposal features: specificity, local information, evidence use, repetition, novelty, stance, and deliberative quality;
- source type: BeppeGrillo.it, Il Blog delle Stelle, Wayback, Internet Archive item, M5S official sources.

## Mechanisms

Candidate mechanisms:

- attention discovery: comments reveal issue priorities;
- proposal discovery: comments surface concrete policy instruments;
- local information: supporters provide geographically specific knowledge;
- mobilization filtering: repeated/high-energy comments are elevated;
- institutional constraint: responsiveness changes as M5S enters electoral and governing institutions.

## Robustness Checks

See `docs/IDENTIFICATION.md`.

## Placebo Tests

See `docs/IDENTIFICATION.md`.

## Regression Task Queue

| Task | Skill | Output | Status |
|---|---|---|---|
| Build issue-week panel v0 | reg-fe, after data construction | `data/analysis/issue_week_panels/issue_week_v0.parquet` and first table | backlog |
| Estimate lead-lag agenda models | reg-fe, after panel construction | first lead-lag table and future-comment placebo | backlog |
| Estimate proposal adoption model v0 | reg-fe or event-history model, TBD | proposal adoption table and audit sample | backlog |

## Current Empirical Bottlenecks

- Historical comment recovery.
- Timestamp/order reliability.
- Archive-completeness measurement.
- Feasible media/public agenda controls back to 2005.
- Human validation design for issue labels and proposal extraction.
