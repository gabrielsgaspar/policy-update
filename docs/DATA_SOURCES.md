# Data Sources

This file summarizes project data sources. `DATA.md` remains the detailed source-of-truth memo for data architecture, schemas, privacy rules, and collection strategy.

## Data Lifecycle Rules

- Do not overwrite raw data.
- Keep raw, interim, clean, processed, analysis, and external data separate.
- Every clean or processed dataset should trace to raw sources and scripts.
- Store source URL, fetch timestamp, Wayback timestamp if applicable, parser version, content hash, and retrieval status.
- Document merge keys, merge losses, coverage gaps, and source restrictions.
- Treat public comments as ethically sensitive. Hash usernames in analysis data and do not deanonymize commenters.

## Source Groups

### Beppe Grillo blog posts and comments

- Current Beppe Grillo site: `https://beppegrillo.it/`
- Blog landing page: `https://beppegrillo.it/blog/`
- Current archive category: `https://beppegrillo.it/category/archivio/`
- Historical domain variants: `www.beppegrillo.it`, `beppegrillo.it`, `http`, `https`, archive paths.
- Primary concern: current pages may preserve post bodies but not all historical comment threads.

### Il Blog delle Stelle

- Main source: `https://www.ilblogdellestelle.it/`
- Candidate legacy pattern: `https://www.ilblogdellestelle.it/YYYY/MM/slug.html`
- Possible use: recover comments or mirrored posts missing from current Beppe Grillo pages.

### Internet Archive / Wayback Machine

- Use CDX queries for Beppe Grillo, Il Blog delle Stelle, and M5S domains.
- Store raw CDX responses and parsed inventories.
- Download archived pages with `id_` mode where possible.
- Measure capture counts, template changes, pagination completeness, and missingness.

### Internet Archive item `BeppeGrillo.it2005`

- Source: `https://archive.org/details/BeppeGrillo.it2005`
- Task: inspect file structure, comments, parseability, and license/access constraints.

### M5S official outputs

- Current and historical domains: `movimento5stelle.it`, `movimento5stelle.eu`, and `portale.movimento5stelle.eu`.
- Document types: programs, campaign materials, platform materials, candidate lists, transparency files, consultation results.
- Known seed: 2013 M5S program PDF hosted by the Italian Interior Ministry.

### Parliamentary outputs

- Chamber of Deputies: `https://dati.camera.it/` and `https://data.camera.it/`.
- Senate: `https://www.senato.it/leggi-e-documenti`.
- Openpolis/OpenParlamento as a structured convenience layer, with official sources treated as canonical when possible.

### Election results

- Interior Ministry historical archive and Eligendo open data.
- Use cases: local M5S strength, electoral timing, geography controls, and possible extensions.

### Comparison parties

Initial comparison parties include PD, PDL/Forza Italia, Lega, Italia dei Valori, Fratelli d'Italia for later periods, and other relevant parties depending on year and election.

### Media and public agenda controls

Candidate controls include Comparative Agendas Project / Italian Policy Agendas, Manifesto Project, GDELT, Google Trends, and AGCOM media monitoring. Feasibility is TBD.

### Event calendar

Manual event calendar for M5S milestones, elections, V-Day, parliamentary entry, government entry/exit, platform changes, major scandals, crises, and national shocks.

## Dataset Template

### Dataset: [Name]

- Source:
- URL / path:
- Access date:
- Raw location:
- Interim location:
- Clean / processed location:
- Unit of observation:
- Time coverage:
- Geographic coverage:
- Key variables:
- Merge keys:
- Known issues:
- Cleaning scripts:
- License / access restrictions:
- Used in:
- Last updated:
