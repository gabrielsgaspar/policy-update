#!/usr/bin/env python3
"""Lightweight structure check for the policy-update research repository."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md', 'PROJECT.md', 'DATA.md', 'TASKS.md', 'AGENTS.md', 'CLAUDE.md', 'RESEARCH.md',
    'docs/TASKS.md', 'docs/DECISIONS.md', 'docs/WHAT_WE_TRIED.md', 'docs/ASSUMPTIONS.md',
    'docs/IDENTIFICATION.md', 'docs/EMPIRICS.md', 'docs/DATA_SOURCES.md',
    'docs/DATA_EXTRACTION_PLAN.md', 'docs/RESULTS_LOG.md', 'docs/LITERATURE_MAP.md',
    'docs/WRITING_PLAN.md', 'docs/REPLICATION_CHECKLIST.md', 'docs/RESEARCH_CADENCE.md',
    'docs/LATEX_STRUCTURE.md', 'docs/OBSIDIAN_LITERATURE.md', 'docs/SEMINAR_FEEDBACK.md',
    'docs/INSTALL_RESEARCH_WORKFLOW.md', 'docs/REPO_ORGANIZATION_REPORT.md',
    'data/README.md', 'code/README.md', 'paper/main.tex', 'paper/Makefile',
    'paper/inputs/packages.tex', 'paper/inputs/settings.tex', 'paper/inputs/macros.tex',
    'paper/inputs/notation.tex', 'paper/frontmatter/title.tex', 'paper/frontmatter/abstract.tex',
    '.cursor/rules/00-research-governance.mdc', '.claude/agents/research-chief-of-staff.md',
    '.claude/commands/research-brief.md', '.agents/skills/research-brief/SKILL.md',
]
OPTIONAL_DIRS = [
    'data/raw', 'data/interim', 'data/clean', 'data/external', 'data/processed',
    'data/analysis', 'data/metadata', 'outputs/figures', 'outputs/tables',
    'outputs/logs', 'outputs/models', 'outputs/validation', 'code/extract',
    'code/parse', 'code/clean', 'code/build', 'code/analysis', 'code/ml',
    'code/db', 'code/utils', 'code/tests', 'code/notebooks',
]


def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        print('Missing required research workflow files:')
        for p in missing:
            print(f'  - {p}')
        return 1
    print('Research governance structure: OK')
    for d in OPTIONAL_DIRS:
        if not (ROOT / d).exists():
            print(f'Warning: optional directory missing: {d}')
    main_tex = (ROOT / 'paper/main.tex').read_text(encoding='utf-8')
    expected = [
        'frontmatter/abstract',
        'sections/01_introduction',
        'sections/06_empirical_strategy',
        'appendix/appendix_main',
        'references/references',
    ]
    missing_inputs = [x for x in expected if x not in main_tex]
    if missing_inputs:
        print('Warning: paper/main.tex may be missing expected inputs:')
        for item in missing_inputs:
            print(f'  - {item}')
    else:
        print('LaTeX main.tex structure: OK')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
