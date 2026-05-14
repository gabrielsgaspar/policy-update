# From Voice to Policy

Repository for the Beppe Grillo blog / Five Star Movement digital-party responsiveness project.

## Project

This project studies whether a party-owned digital platform helped the Five Star Movement (M5S) learn from supporter voice. The central question is whether grievances, issue priorities, local information, and policy proposals expressed in Beppe Grillo blog comments later shaped Grillo/M5S communication, campaign materials, programs, and parliamentary behavior.

The intended empirical setting is Italy, mainly 2005-2018, with the first feasibility pilot focused on 2005-2013.

The current stage is repository setup and research design. No data collection, parsing, modeling, or empirical analysis has been executed in this repo yet.

## Canonical Project Docs

- `PROJECT.md`: research question, hypotheses, contribution, empirical strategy, risks, and literature anchors.
- `DATA.md`: planned data sources, data architecture, schema, crawl strategy, privacy rules, and pilot sample design.
- `TASKS.md`: canonical project task tracker.
- `RESEARCH.md`: concise current source of truth for agents and collaborators.

## Repository Layout

```text
docs/       Durable research memory, source notes, codebooks, and governance logs.
data/       Data lifecycle directories. Raw data is immutable and not tracked by Git.
code/       Extraction, parsing, cleaning, build, ML, database, and analysis code.
outputs/    Generated tables, figures, logs, models, and validation reports.
paper/      Modular LaTeX manuscript scaffold.
.agents/    Codex skills from the research governance overlay.
.claude/    Claude Code agents and commands.
.cursor/    Cursor research-governance rules.
```

## Data Rules

Raw data must not be edited manually. Store original HTML, PDF, JSON, WARC, and API responses exactly as collected, with source URL, fetch timestamp, archive timestamp when relevant, content hash, parser version, and retrieval status.

Public comments are treated as ethically sensitive text from ordinary citizens. Analysis data should hash usernames, avoid deanonymization, and avoid publishing personally identifying metadata unless separately approved.

## First Milestone

The first milestone is a feasibility decision: can the project recover enough posts and comments, with usable dates or ordering, to measure whether comment issue attention and policy proposals predict later M5S communication or formal political outputs?

The immediate next tasks are listed in `TASKS.md`.
