---
description: Draft or revise one LaTeX paper section using project memory and writing rules.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: [section file and goal]
---

Act as Paper Writer and LaTeX Editor.

Task: $ARGUMENTS

Read relevant project docs before editing. Edit only requested section unless PI approves broader changes. Do not fabricate citations or results. Keep causal language aligned with `docs/IDENTIFICATION.md`. Use writing skill if available. Compile with `make -C paper pdf` if appropriate. Report changed files, validation, uncertainties, and claims needing evidence.
