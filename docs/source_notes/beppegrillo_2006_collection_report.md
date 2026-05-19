# BeppeGrillo.it 2006 Posts And Comments Collection Report

Last updated: 2026-05-15

## Scope

This is a bounded feasibility data collection exercise for posts dated 2006 on BeppeGrillo.it and comments embedded in archived post pages. It uses Wayback `id_` captures and the observed legacy comment patterns.

## Summary Counts

- Unique 2006 post paths attempted: 468
- Posts with at least one parsed embedded comment: 365
- Parsed comments: 442,328
- Comments with raw author string: 344,171
- Comments with parsed timestamp: 344,171
- Fetch attempts: 3,726
- Successful fetch attempts: 1,464
- Failed fetch attempts: 2,262

## Top Posts By Parsed Comment Count

| Rank | Comments | Date | Title | URL |
|---:|---:|---|---|---|
| 1 | 4,803 | 2006-06-11 | Forza Ghana!!! | `http://www.beppegrillo.it/2006/06/forza_ghana.html` |
| 2 | 4,130 | 2006-04-11 | C'è chi | `http://beppegrillo.it/2006/04/ce_chi.html` |
| 3 | 3,862 | 2006-07-23 | Una lettera del ministro Di Pietro | `http://www.beppegrillo.it/2006/07/una_lettera_del.html` |
| 4 | 3,838 | 2006-04-10 | Pedalare Prodi, pedalare... | `http://www.beppegrillo.it/2006/04/pedalare_prodi.html` |
| 5 | 3,718 | 2006-04-05 | Scatenati coglione! | `http://www.beppegrillo.it/2006/04/scatenati_cogli.html` |
| 6 | 3,598 | 2006-07-12 | Fantozzi è vivo e lotta con noi | `http://www.beppegrillo.it/2006/07/fantozzi_e_vivo_1.html` |
| 7 | 3,438 | 2006-04-13 | Lettera a George Bush | `http://beppegrillo.it/2006/04/lettera_a_georg_1.html` |
| 8 | 3,306 | 2006-04-07 | Basta? Basta! | `http://www.beppegrillo.it/2006/04/basta.html` |
| 9 | 3,083 | 2006-10-23 | RESET | `http://beppegrillo.it/2006/10/reset.html` |
| 10 | 2,920 | 2006-04-04 | Primarie dei cittadini: informazione | `http://www.beppegrillo.it/2006/04/primarie_dei_ci_8.html` |
| 11 | 2,891 | 2006-03-28 | De profundis | `http://www.beppegrillo.it/2006/03/de_profundis.html` |
| 12 | 2,887 | 2006-08-01 | Adolf Gibson | `http://beppegrillo.it/2006/08/adolf_gibson.html` |
| 13 | 2,680 | 2006-12-03 | Il sabato delle salme | `http://beppegrillo.it/2006/12/il_sabato_delle.html` |
| 14 | 2,668 | 2006-05-03 | Telecom al servizio del Paese | `http://www.beppegrillo.it/2006/05/post_17.html` |
| 15 | 2,624 | 2006-04-03 | ...e poi, non ne rimase nessuno | `http://www.beppegrillo.it/2006/04/e_poi_non_ne_ri.html` |
| 16 | 2,622 | 2006-02-05 | Vergogne d'Italia | `http://beppegrillo.it/2006/02/vergogne_ditali.html` |
| 17 | 2,592 | 2006-11-05 | Australia | `http://beppegrillo.it/2006/11/australia.html` |
| 18 | 2,559 | 2006-10-21 | Un Paese sull'orlo di una crisi di nervi | `http://www.beppegrillo.it/2006/10/un_paese_sullor.html` |
| 19 | 2,463 | 2006-07-27 | Litaliano medio ruba le tartarughe. | `http://beppegrillo.it/2006/07/litaliano_medio_1.html` |
| 20 | 2,446 | 2006-03-13 | La ricerca imbavagliata | `http://www.beppegrillo.it/2006/03/la_ricerca_imba.html` |

## Data Organization

- Raw HTML: `data/raw/wayback/html/beppegrillo_2006/{month}/`
- Parsed posts CSV/Parquet: `data/interim/parsed_posts/beppegrillo_2006_posts.*`
- Parsed comments CSV/Parquet: `data/interim/parsed_comments/beppegrillo_2006_comments.*`
- Fetch attempts CSV/Parquet: `data/interim/fetches/beppegrillo_2006_fetch_attempts.*`

## Comment Fields

Each parsed comment includes `comment_id`, `post_id`, `author_display_hash`, `author_raw_restricted`, `comment_timestamp`, `comment_date_confidence`, `comment_order`, `parent_comment_id`, `body_text`, `body_html_path`, `links`, `parser_version`, `parse_confidence`, and `parser_warnings`.

Raw author strings are retained only in the restricted interim field `author_raw_restricted`; analysis should use `author_display_hash`.

## Limitations

- This parser recovers comments embedded directly in legacy post HTML. It does not yet follow external pagination or AJAX-style comment loaders.
- For each post path, the collector tries a small set of candidate captures and keeps the capture with the most parsed embedded comments.
- Comment order is page order. For this template, comments often appear reverse-chronologically, so timestamp fields should be used for temporal ordering when parsed.
- The CDX inventory was capped; additional 2006 post URLs may exist outside the current capped inventory.
