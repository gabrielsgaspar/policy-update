# BeppeGrillo.it 2008 Posts And Comments Collection Report

Last updated: 2026-05-16

## Scope

This is a bounded feasibility data collection exercise for posts dated 2008 on BeppeGrillo.it and comments embedded in archived post pages. It uses Wayback `id_` captures and the observed legacy comment patterns.

## Summary Counts

- Unique 2008 post paths attempted: 484
- Posts with at least one parsed embedded comment: 219
- Parsed comments: 55,780
- Comments with raw author string: 55,780
- Comments with parsed timestamp: 55,780
- Fetch attempts: 1,928
- Successful fetch attempts: 787
- Failed fetch attempts: 1,141

## Top Posts By Parsed Comment Count

| Rank | Comments | Date | Title | URL |
|---:|---:|---|---|---|
| 1 | 374 | 2008-07-21 | Blog di Beppe Grillo - Lezione di legalita' dall'Albania | `http://www.beppegrillo.it/2008/07/lezione_di_legalita_dallalbania.html` |
| 2 | 374 | 2008-08-18 | Blog di Beppe Grillo - La Dora al cromo esavalente | `http://www.beppegrillo.it/2008/08/la_dora_al_crom.html` |
| 3 | 374 | 2008-09-28 | Comuni, stiamo arrivando... | `http://www.beppegrillo.it/2008/09/comunistiamo_arrivando.html` |
| 4 | 374 | 2008-12-07 | I primi della classe | `http://www.beppegrillo.it/2008/12/i_primi_della_c.html` |
| 5 | 373 | 2008-06-26 | Blog di Beppe Grillo - Silvio Horror Picture Show | `http://www.beppegrillo.it/2008/06/silvio_horror_p.html` |
| 6 | 373 | 2008-09-20 | Blog di Beppe Grillo - Squali d'Italia | `http://www.beppegrillo.it/2008/09/squali_ditalia.html` |
| 7 | 370 | 2008-10-31 | Blog di Beppe Grillo - Le due Italie | `http://www.beppegrillo.it/2008/10/le_due_italie.html` |
| 8 | 368 | 2008-08-26 | Una tranquilla Italia da paura | `http://www.beppegrillo.it/2008/08/una_tranquilla.html` |
| 9 | 365 | 2008-10-01 | Sei anche tu un intercettato? | `http://www.beppegrillo.it/2008/10/sei_anche_tu_un.html` |
| 10 | 363 | 2008-07-31 | Blog di Beppe Grillo - In morte di Riccardo Rasman | `http://www.beppegrillo.it/2008/07/in_morte_di_ric.html` |
| 11 | 362 | 2008-05-09 | Blog di Beppe Grillo - Zappiamo Forbice | `http://www.beppegrillo.it/2008/05/zappiamo_forbic.html` |
| 12 | 362 | 2008-11-11 | Blog di Beppe Grillo - La versione dei piloti Alitalia | `http://www.beppegrillo.it/2008/11/la_versione_dei.html` |
| 13 | 361 | 2008-11-24 | D'Alema, il piu' uguale degli altri | `http://www.beppegrillo.it/2008/11/passaparola_lun_4.html` |
| 14 | 361 | 2008-07-12 | Blog di Beppe Grillo - Lettera a una Lega mai nata | `http://www.beppegrillo.it/2008/07/lettera_a_una_l.html` |
| 15 | 359 | 2008-10-08 | Le banche e la politica cialtrona | `http://www.beppegrillo.it/2008/10/le_banche_e_la_politica_cialtrona.html` |
| 16 | 359 | 2008-08-19 | Eleições Limpas | `http://www.beppegrillo.it/2008/08/eleicoes_limpas.html` |
| 17 | 358 | 2008-12-05 | La patata bollente da 98 miliardi | `http://www.beppegrillo.it/2008/12/98_miliardi.html` |
| 18 | 357 | 2008-12-19 | Blog di Beppe Grillo - Rosa (Russo Iervolino) sei rimasta sola... | `http://www.beppegrillo.it/2008/12/rosa_russo_ierv.html` |
| 19 | 357 | 2008-12-01 | Mediaset Uber Alles | `http://www.beppegrillo.it/2008/12/passaparola_lun_7.html` |
| 20 | 356 | 2008-06-21 | Blog di Beppe Grillo - Le foglie morte | `http://www.beppegrillo.it/2008/06/come_dautunno.html` |

## Data Organization

- Raw HTML: `data/raw/wayback/html/beppegrillo_2008/{month}/`
- Parsed posts CSV/Parquet: `data/interim/parsed_posts/beppegrillo_2008_posts.*`
- Parsed comments CSV/Parquet: `data/interim/parsed_comments/beppegrillo_2008_comments.*`
- Fetch attempts CSV/Parquet: `data/interim/fetches/beppegrillo_2008_fetch_attempts.*`

## Comment Fields

Each parsed comment includes `comment_id`, `post_id`, `author_display_hash`, `author_raw_restricted`, `comment_timestamp`, `comment_date_confidence`, `comment_order`, `parent_comment_id`, `body_text`, `body_html_path`, `links`, `parser_version`, `parse_confidence`, and `parser_warnings`.

Raw author strings are retained only in the restricted interim field `author_raw_restricted`; analysis should use `author_display_hash`.

## Limitations

- This parser recovers comments embedded directly in legacy post HTML. It does not yet follow external pagination or AJAX-style comment loaders.
- For each post path, the collector tries a small set of candidate captures and keeps the capture with the most parsed embedded comments.
- Comment order is page order. For this template, comments often appear reverse-chronologically, so timestamp fields should be used for temporal ordering when parsed.
- The CDX inventory was capped; additional 2008 post URLs may exist outside the current capped inventory.
