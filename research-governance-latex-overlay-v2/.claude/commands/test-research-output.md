---
description: Validate a research output, result, table, figure, or LaTeX draft against task acceptance criteria.
allowed-tools: Read, Grep, Glob, Bash
argument-hint: [task id or output path]
---

Validate the research output.

Target: $ARGUMENTS

Read `docs/TASKS.md`, `docs/RESULTS_LOG.md`, `docs/REPLICATION_CHECKLIST.md`, and relevant files. Check output exists, acceptance criteria, traceability to script/config/data, paper claims match output, LaTeX compiles if paper files changed, and limitations are logged. Return pass/fail, evidence, and required fixes.
