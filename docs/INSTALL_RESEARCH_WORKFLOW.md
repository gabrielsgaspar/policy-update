# Installed Research Workflow

This repository has installed and adapted the research governance LaTeX overlay.

## Installed Components

- `.agents/skills/` for Codex-compatible research skills.
- `.claude/agents/` and `.claude/commands/` for Claude Code workflows.
- `.cursor/rules/` for Cursor workflows.
- `AGENTS.md`, `CLAUDE.md`, and `RESEARCH.md` at the repo root.
- `docs/` research memory files.
- `paper/` modular LaTeX scaffold.
- `scripts/research_doctor.py` structure check.

## Local Checks

Run:

```bash
python scripts/research_doctor.py
```

When TeX is available and paper files change, run:

```bash
make -C paper pdf
```

## Canonical Task Tracker

Root `TASKS.md` is canonical. `docs/TASKS.md` is a compatibility pointer for overlay tools.
