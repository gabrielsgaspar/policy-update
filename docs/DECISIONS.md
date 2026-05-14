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
