# LaTeX Structure

The default paper scaffold follows the organization used in the uploaded examples:

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

For existing papers with non-numbered section names, keep the existing names and update `paper/main.tex` accordingly. The workflow cares about modularity, not exact section filenames.
