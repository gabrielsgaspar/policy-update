#!/usr/bin/env python3
"""Lightweight structure check for the research governance overlay."""
from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'AGENTS.md','RESEARCH.md','docs/TASKS.md','docs/DECISIONS.md','docs/WHAT_WE_TRIED.md',
    'docs/IDENTIFICATION.md','docs/DATA_SOURCES.md','docs/RESULTS_LOG.md','docs/LITERATURE_MAP.md',
    'docs/WRITING_PLAN.md','paper/main.tex','paper/Makefile','paper/inputs/packages.tex',
    'paper/inputs/settings.tex','paper/inputs/macros.tex','paper/inputs/notation.tex',
    'paper/frontmatter/title.tex','paper/frontmatter/abstract.tex',
    '.cursor/rules/00-research-governance.mdc','.claude/agents/research-chief-of-staff.md',
    '.claude/commands/research-brief.md','.agents/skills/research-brief/SKILL.md'
]
OPTIONAL_DIRS = ['data/raw','data/interim','data/clean','outputs/figures','outputs/tables','code/scripts','code/notebooks','code/regressions']

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
    expected = ['frontmatter/abstract','sections/01_introduction','sections/06_empirical_strategy','appendix/appendix_main','references/references']
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
