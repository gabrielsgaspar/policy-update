---
description: Convert a PI-approved research decision into executable tasks with acceptance criteria.
allowed-tools: Read, Grep, Glob, Edit, Write
argument-hint: [PI-approved decision]
---

Convert the PI-approved decision into tasks.

Decision: $ARGUMENTS

Read `RESEARCH.md`, `docs/TASKS.md`, `docs/DECISIONS.md`, and relevant topical docs. Define task boundaries, owner, reviewer, outputs, acceptance criteria, validation, and dependencies. Update `docs/TASKS.md`; update `docs/DECISIONS.md` only for durable PI decisions. Stop before implementation unless PI explicitly approved execution.
