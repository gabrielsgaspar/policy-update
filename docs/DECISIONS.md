# Decisions

Record durable PI decisions only.

## Durable Decisions

### D-2026-05-14-001: Use the research governance overlay for this repository

- Date: 2026-05-14
- Decision maker: PI directive in repository setup prompt
- Context: The PI requested that the repository be organized using the research governance LaTeX overlay while preserving the project-specific contents of `PROJECT.md`, `DATA.md`, and `TASKS.md`.
- Options considered: keep only the three original project documents; install the full overlay without adaptation; install the overlay and adapt it to the M5S responsiveness project.
- Decision: Install the useful overlay infrastructure and adapt project memory files to the M5S project.
- Rationale: The project needs durable research memory, agent compatibility, a LaTeX scaffold, and a task system before data collection begins.
- Objections / risks: Generic scaffold text could obscure project-specific research content if copied without adaptation.
- Consequences: Root `TASKS.md` remains canonical; `RESEARCH.md` becomes the concise current source of truth; `docs/` stores durable research memory.
- Revisit date: TBD.
- Related tasks: P0-001.

### D-2026-05-14-002: Use `code/` as the primary implementation tree

- Date: 2026-05-14
- Decision maker: Repository organization decision under PI setup prompt
- Context: The original task list used `src/`, while the requested target structure used `code/`.
- Options considered: use only `src/`; use only `code/`; maintain both.
- Decision: Use `code/` as the primary implementation tree and update future task paths accordingly.
- Rationale: The requested target tree uses `code/`, and the pipeline is easier to read when organized by extraction, parsing, cleaning, build, analysis, ML, database, and utilities.
- Objections / risks: Existing task text referenced `src/`; those references should be updated consistently.
- Consequences: Future implementation tasks should write to `code/extract/`, `code/parse/`, `code/db/`, `code/ml/`, and related directories.
- Revisit date: TBD.
- Related tasks: P0-001.

### D-2026-05-14-003: Approve feasibility-only measurement-first identification-ready pilot

- Date: 2026-05-14
- Decision maker: PI
- Context: The research council recommended that the first data phase should test source recoverability, measurement validity, and identification readiness before full scraping, parsing, modeling, or empirical analysis.
- Options considered: proceed directly to full collection and analysis; run only a comment-recovery pilot; run a feasibility-only pilot that includes measurement and identification requirements from the start.
- Decision: Approve the feasibility-only, measurement-first, identification-ready pilot before any full scraping, parsing, modeling, or empirical analysis.
- Rationale: The project's viability depends on whether comments are recoverable at usable scale, whether timestamps/order and archive completeness are defensible, whether duplicate mirrors can be controlled, whether ethics rules are settled, and whether later issue/proposal measurement can be validated.
- Objections / risks: The pilot may reveal insufficient comment coverage, non-random archive gaps, weak timestamp information, unresolved source restrictions, or measurement error large enough to require pivoting the first paper.
- Consequences: Initial work should focus on ethics, source inventory, Wayback/CDX coverage, Internet Archive item inspection, URL inventory, provenance requirements, bounded pilot collection, quality checks, and a feasibility memo. Full collection, modeling, and empirical analysis remain gated by PI approval after the pilot report.
- Revisit date: After the pilot data report and feasibility memo.
- Related tasks: P0-004, P0-101, P0-102, P0-103, P1-104, P1-105, P1-106, P0-201, P0-202, P0-301, P0-307, P0-401, P0-402.

## Template

### D-YYYY-MM-DD-001: [Decision title]

- Date:
- Decision maker: PI
- Context:
- Options considered:
- Decision:
- Rationale:
- Objections / risks:
- Consequences:
- Revisit date:
- Related tasks:
