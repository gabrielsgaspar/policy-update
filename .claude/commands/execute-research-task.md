---
description: Execute exactly one approved research task, validate it, and report results.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: [task id]
---

Execute exactly one approved task.

Task ID: $ARGUMENTS

Read `docs/TASKS.md`, confirm the task exists, identify owner and reviewer, restate scope and affected files, execute only this task, validate output, apply critic/reviewer perspective, update durable docs, and report using the AGENTS.md completion format. Do not expand scope.
