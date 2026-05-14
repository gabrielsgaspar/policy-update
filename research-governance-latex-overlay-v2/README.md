# Research Governance LaTeX Overlay

This is a drop-in workflow overlay for PI-led research papers written in LaTeX.

It is designed for:

- Claude Code: `.claude/agents/` and `.claude/commands/`
- Cursor: `AGENTS.md` and `.cursor/rules/`
- Codex: `AGENTS.md` and `.agents/skills/`

The user is the Principal Investigator (PI). Agents can advise, plan, execute bounded tasks, criticize, validate, and update project memory, but they must not make final PI decisions.

## Install

For a new research project, copy everything into the repo root.

For an existing paper repo, merge carefully:

1. Copy `.claude/`, `.cursor/`, `.agents/skills/`, `CLAUDE.md`, and `docs/INSTALL_RESEARCH_WORKFLOW.md` first.
2. Merge `AGENTS.md` rather than blindly replacing your existing instructions.
3. Merge `paper/` only if you want the scaffold; do not overwrite existing LaTeX content.
4. Run:

```bash
python scripts/research_doctor.py
```

5. Compile the paper with:

```bash
make -C paper pdf
```

## Core loop

```text
PI asks question
  -> Research Chief of Staff frames it
  -> Builder agents construct best case
  -> Critical agents attack it
  -> Chief of Staff synthesizes options
  -> PI decides
  -> task is planned
  -> one bounded task is executed
  -> critic/reviewer validates
  -> durable docs are updated
```
