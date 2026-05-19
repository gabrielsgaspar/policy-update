# BeppeGrillo.it 2007 Posts And Comments Collection Report

Last updated: 2026-05-16

## Scope

This is a bounded feasibility data collection exercise for posts dated 2007 on BeppeGrillo.it and comments embedded in archived post pages. It uses Wayback `id_` captures and the observed legacy comment patterns.

## Summary Counts

- Unique 2007 post paths attempted: 538
- Posts with at least one parsed embedded comment: 326
- Parsed comments: 273,625
- Comments with raw author string: 202,956
- Comments with parsed timestamp: 202,956
- Fetch attempts: 2,496
- Successful fetch attempts: 1,058
- Failed fetch attempts: 1,438

## Top Posts By Parsed Comment Count

| Rank | Comments | Date | Title | URL |
|---:|---:|---|---|---|
| 1 | 2,677 | 2007-05-16 | Crimen Sollicitationis | `http://www.beppegrillo.it/2007/05/crimen_sollicit.html` |
| 2 | 2,654 | 2007-02-26 | Istigazione al suicidio | `http://www.beppegrillo.it/2007/02/istigazione_al_suicidio.html` |
| 3 | 2,551 | 2007-03-02 | Lo sciopero dei sacramenti | `http://www.beppegrillo.it/2007/03/lo_sciopero_dei.html` |
| 4 | 2,309 | 2007-09-09 | Piazza Maggiore, Bologna, otto settembre 2007 | `http://www.beppegrillo.it/2007/09/piazza_maggiore.html` |
| 5 | 2,269 | 2007-06-14 | Vaffanculo-Day | `http://www.beppegrillo.it/2007/06/vaffanculoday.html` |
| 6 | 2,257 | 2007-03-13 | Voglio fare l'editore | `http://www.beppegrillo.it/2007/03/voglio_fare_led.html` |
| 7 | 2,241 | 2007-01-16 | Un Paese a sovranità limitata | `http://beppegrillo.it/2007/01/un_paese_a_sovr.html` |
| 8 | 2,065 | 2007-02-18 | Brigate CGIL | `http://www.beppegrillo.it/2007/02/brigate_cgil.html` |
| 9 | 2,026 | 2007-09-14 | L' Herald Tribune e il V-day | `http://www.beppegrillo.it/2007/09/l_herald_tribun.html` |
| 10 | 1,941 | 2007-01-13 | Una lettera dal Vaticano | `http://www.beppegrillo.it/2007/01/una_lettera_dal_vaticano.html` |
| 11 | 1,920 | 2007-04-12 | Le bandiere rosse di via Paolo Sarpi | `http://www.beppegrillo.it/2007/04/le_bandiere_ros.html` |
| 12 | 1,859 | 2007-02-20 | I marchesi del Grillo | `http://www.beppegrillo.it/2007/02/i_marchesi_del_grillo.html` |
| 13 | 1,849 | 2007-05-14 | Garibaldi addio | `http://www.beppegrillo.it/2007/05/garibaldi_addio.html` |
| 14 | 1,836 | 2007-06-11 | Per chi suona la sirena | `http://www.beppegrillo.it/2007/06/per_chi_suona_l.html` |
| 15 | 1,754 | 2007-05-12 | Avignone non può attendere | `http://www.beppegrillo.it/2007/05/avignone_non_pu.html` |
| 16 | 1,735 | 2007-01-08 | Grazie Gianluigi | `http://www.beppegrillo.it/2007/01/grazie_gianluigi.html` |
| 17 | 1,703 | 2007-05-08 | Razzismo all'italiana | `http://www.beppegrillo.it/2007/05/razzismo_allita.html` |
| 18 | 1,695 | 2007-06-10 | Il nuovo terrorismo | `http://www.beppegrillo.it/2007/06/il_nuovo_terrorismo.html` |
| 19 | 1,680 | 2007-07-05 | Berluscagate | `http://beppegrillo.it/2007/07/berluscagate.html` |
| 20 | 1,640 | 2007-05-21 | La notte della Repubblica | `http://www.beppegrillo.it/2007/05/la_notte_della.html` |

## Data Organization

- Raw HTML: `data/raw/wayback/html/beppegrillo_2007/{month}/`
- Parsed posts CSV/Parquet: `data/interim/parsed_posts/beppegrillo_2007_posts.*`
- Parsed comments CSV/Parquet: `data/interim/parsed_comments/beppegrillo_2007_comments.*`
- Fetch attempts CSV/Parquet: `data/interim/fetches/beppegrillo_2007_fetch_attempts.*`

## Comment Fields

Each parsed comment includes `comment_id`, `post_id`, `author_display_hash`, `author_raw_restricted`, `comment_timestamp`, `comment_date_confidence`, `comment_order`, `parent_comment_id`, `body_text`, `body_html_path`, `links`, `parser_version`, `parse_confidence`, and `parser_warnings`.

Raw author strings are retained only in the restricted interim field `author_raw_restricted`; analysis should use `author_display_hash`.

## Limitations

- This parser recovers comments embedded directly in legacy post HTML. It does not yet follow external pagination or AJAX-style comment loaders.
- For each post path, the collector tries a small set of candidate captures and keeps the capture with the most parsed embedded comments.
- Comment order is page order. For this template, comments often appear reverse-chronologically, so timestamp fields should be used for temporal ordering when parsed.
- The CDX inventory was capped; additional 2007 post URLs may exist outside the current capped inventory.
