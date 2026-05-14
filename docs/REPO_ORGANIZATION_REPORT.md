# Repository Organization Report

Date: 2026-05-14

## Summary

The repository has been organized for the Beppe Grillo blog / M5S digital-party responsiveness project. This pass installed the research governance scaffold, created a project-specific directory structure, wrote durable research memory files, updated the README and task tracker, and prepared a modular LaTeX manuscript scaffold.

No data collection, scraping, parsing, modeling, or empirical analysis was executed.

## Validation

- `python scripts/research_doctor.py`: passed.
- `make -C paper pdf`: not run successfully because `make` is not installed in the current PowerShell environment.

## Files Modified

- `.gitignore`
- `README.md`
- `TASKS.md`
- `scripts/research_doctor.py`

## Files Created Or Copied

### Root governance files

- `AGENTS.md`
- `CLAUDE.md`
- `RESEARCH.md`

### Codex skills

- `.agents/skills/identification-review/SKILL.md`
- `.agents/skills/latex-paper-workflow/SKILL.md`
- `.agents/skills/literature-map/SKILL.md`
- `.agents/skills/research-brief/SKILL.md`
- `.agents/skills/research-council-review/SKILL.md`
- `.agents/skills/research-execute-task/SKILL.md`
- `.agents/skills/research-plan-execution/SKILL.md`
- `.agents/skills/research-session-close/SKILL.md`

### Claude Code agents

- `.claude/agents/data-critic.md`
- `.claude/agents/data-manager.md`
- `.claude/agents/econometrics-builder.md`
- `.claude/agents/econometrics-critic.md`
- `.claude/agents/latex-editor.md`
- `.claude/agents/literature-critic.md`
- `.claude/agents/literature-mapper.md`
- `.claude/agents/paper-writer.md`
- `.claude/agents/research-chief-of-staff.md`
- `.claude/agents/robustness-lead.md`
- `.claude/agents/skeptical-replicator.md`
- `.claude/agents/stats-ml-builder.md`
- `.claude/agents/stats-ml-critic.md`
- `.claude/agents/theory-builder.md`
- `.claude/agents/theory-critic.md`
- `.claude/agents/writing-critic.md`

### Claude Code commands

- `.claude/commands/council-review.md`
- `.claude/commands/end-research-session.md`
- `.claude/commands/execute-research-task.md`
- `.claude/commands/identification-review.md`
- `.claude/commands/latex-write.md`
- `.claude/commands/literature-map.md`
- `.claude/commands/plan-research-task.md`
- `.claude/commands/referee-2.md`
- `.claude/commands/research-brief.md`
- `.claude/commands/results-review.md`
- `.claude/commands/test-research-output.md`
- `.claude/commands/weekly-research-retro.md`

### Cursor rules

- `.cursor/rules/00-research-governance.mdc`
- `.cursor/rules/10-latex-paper.mdc`
- `.cursor/rules/20-research-memory.mdc`
- `.cursor/rules/30-empirical-methods.mdc`

### Research memory docs

- `docs/ASSUMPTIONS.md`
- `docs/DATA_EXTRACTION_PLAN.md`
- `docs/DATA_SOURCES.md`
- `docs/DECISIONS.md`
- `docs/EMPIRICS.md`
- `docs/IDENTIFICATION.md`
- `docs/INSTALL_RESEARCH_WORKFLOW.md`
- `docs/LATEX_STRUCTURE.md`
- `docs/LITERATURE_MAP.md`
- `docs/OBSIDIAN_LITERATURE.md`
- `docs/REPLICATION_CHECKLIST.md`
- `docs/RESEARCH_CADENCE.md`
- `docs/REPO_ORGANIZATION_REPORT.md`
- `docs/RESULTS_LOG.md`
- `docs/SEMINAR_FEEDBACK.md`
- `docs/TASKS.md`
- `docs/WHAT_WE_TRIED.md`
- `docs/WRITING_PLAN.md`
- `docs/codebooks/.gitkeep`
- `docs/codebooks/README.md`
- `docs/parser_notes/.gitkeep`
- `docs/parser_notes/README.md`
- `docs/source_notes/.gitkeep`
- `docs/source_notes/README.md`

### Data structure files

- `data/README.md`
- `data/analysis/.gitkeep`
- `data/clean/.gitkeep`
- `data/external/.gitkeep`
- `data/interim/.gitkeep`
- `data/metadata/.gitkeep`
- `data/processed/.gitkeep`
- `data/raw/.gitkeep`

### Code structure files

- `code/README.md`
- `code/analysis/.gitkeep`
- `code/build/.gitkeep`
- `code/clean/.gitkeep`
- `code/db/.gitkeep`
- `code/extract/.gitkeep`
- `code/ml/.gitkeep`
- `code/notebooks/.gitkeep`
- `code/parse/.gitkeep`
- `code/tests/.gitkeep`
- `code/utils/.gitkeep`

### Outputs structure files

- `outputs/figures/.gitkeep`
- `outputs/logs/.gitkeep`
- `outputs/models/.gitkeep`
- `outputs/tables/.gitkeep`
- `outputs/validation/.gitkeep`

### Paper scaffold

- `paper/.gitignore`
- `paper/Makefile`
- `paper/README.md`
- `paper/appendix/a_data_appendix.tex`
- `paper/appendix/appendix_main.tex`
- `paper/appendix/b_additional_results.tex`
- `paper/appendix/c_robustness.tex`
- `paper/appendix/d_proofs.tex`
- `paper/figures/.gitkeep`
- `paper/figures/README.md`
- `paper/frontmatter/abstract.tex`
- `paper/frontmatter/title.tex`
- `paper/inputs/macros.tex`
- `paper/inputs/notation.tex`
- `paper/inputs/packages.tex`
- `paper/inputs/settings.tex`
- `paper/latexmkrc`
- `paper/main.tex`
- `paper/references/references.bib`
- `paper/sections/01_introduction.tex`
- `paper/sections/02_literature.tex`
- `paper/sections/03_context.tex`
- `paper/sections/04_theory.tex`
- `paper/sections/05_data.tex`
- `paper/sections/06_empirical_strategy.tex`
- `paper/sections/07_results.tex`
- `paper/sections/08_robustness.tex`
- `paper/sections/09_conclusion.tex`
- `paper/tables/.gitkeep`
- `paper/tables/README.md`

## Directories Created

- `docs/source_notes/`
- `docs/parser_notes/`
- `docs/codebooks/`
- `data/raw/live/beppegrillo/`
- `data/raw/live/blogdellestelle/`
- `data/raw/live/movimento5stelle/`
- `data/raw/live/parliament/`
- `data/raw/live/election_results/`
- `data/raw/live/media/`
- `data/raw/wayback/cdx/`
- `data/raw/wayback/html/`
- `data/raw/wayback/warc/`
- `data/raw/wayback/metadata/`
- `data/raw/third_party/`
- `data/interim/parsed_posts/`
- `data/interim/parsed_comments/`
- `data/interim/parsed_outputs/`
- `data/interim/text_cleaning/`
- `data/interim/language_detection/`
- `data/interim/spam_detection/`
- `data/processed/relational/`
- `data/processed/features/`
- `data/processed/embeddings/`
- `data/processed/llm_labels/`
- `data/processed/validation_sets/`
- `data/analysis/issue_week_panels/`
- `data/analysis/proposal_adoption_panels/`
- `data/analysis/event_studies/`
- `data/analysis/figures/`
- `data/analysis/tables/`
- `data/docs/source_notes/`
- `data/docs/parser_notes/`
- `data/docs/codebooks/`

## Files Left Untouched

- `PROJECT.md`
- `DATA.md`
- `LICENSE`
- `research-governance-latex-overlay-v2/`
