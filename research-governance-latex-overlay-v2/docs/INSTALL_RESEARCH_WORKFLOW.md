# Install the Research Workflow

## New repo

Copy the overlay into the repo root and run:

```bash
python scripts/research_doctor.py
make -C paper pdf
```

## Existing paper repo

Do not blindly overwrite existing paper files.

Recommended merge order:

1. `.claude/`
2. `.cursor/`
3. `.agents/skills/`
4. `CLAUDE.md`
5. `AGENTS.md` merged with your existing project instructions
6. `docs/*.md` templates only where missing
7. `paper/` scaffold only for missing files

## Claude Code workflow

From repo root:

```bash
claude
```

Then:

```text
/research-brief
/council-review What are the next three highest-leverage steps for this paper?
```

After you decide:

```text
/plan-research-task PI approves [decision]. Create bounded tasks and acceptance criteria. Do not implement.
```

Then execute exactly one task:

```text
/execute-research-task R-001
```

For writing:

```text
/latex-write paper/sections/01_introduction.tex -- revise the introduction around the current contribution without inventing results or citations.
```

For review:

```text
/referee-2 paper/main.tex
```

## Cursor workflow

Use Cursor with `AGENTS.md` and `.cursor/rules/`.

Example prompt:

```text
Act as Research Chief of Staff. Read AGENTS.md, RESEARCH.md, and docs/*.md. Prepare a PI brief. Do not edit files.
```

Then:

```text
Run a research council review on the next research step. Use builder and critic perspectives. Do not edit files.
```

## Codex workflow

Use `AGENTS.md` plus `.agents/skills/`.

Example prompts:

```text
Use $research-brief.
```

```text
Use $research-council-review on: What are the next three steps for this paper?
```

```text
Use $latex-paper-workflow to revise paper/sections/06_empirical_strategy.tex.
```
