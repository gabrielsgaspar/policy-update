# LaTeX Structure

The manuscript uses a modular LaTeX scaffold under `paper/`.

```text
paper/
  main.tex
  Makefile
  latexmkrc
  inputs/
    packages.tex
    settings.tex
    macros.tex
    notation.tex
  frontmatter/
    title.tex
    abstract.tex
  sections/
    01_introduction.tex
    02_literature.tex
    03_context.tex
    04_theory.tex
    05_data.tex
    06_empirical_strategy.tex
    07_results.tex
    08_robustness.tex
    09_conclusion.tex
  appendix/
    appendix_main.tex
    a_data_appendix.tex
    b_additional_results.tex
    c_robustness.tex
    d_proofs.tex
  references/
    references.bib
  figures/
  tables/
```

Substantive prose should live in section, appendix, or frontmatter files. Edit `paper/main.tex` only when changing structure.

Compile with:

```bash
make -C paper pdf
```

Do not add fake citations or results placeholders. Add verified BibTeX entries only.
