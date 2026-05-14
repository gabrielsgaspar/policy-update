# Paper

This is a modular LaTeX paper scaffold.

Compile:

```bash
make -C paper pdf
```

Main entry point: `paper/main.tex`.

Substantive prose lives in:

- `paper/frontmatter/`
- `paper/sections/`
- `paper/appendix/`

Keep tables and figures either generated into `outputs/` and copied/symlinked into `paper/`, or generated directly into `paper/tables/` and `paper/figures/` if that is your convention.
