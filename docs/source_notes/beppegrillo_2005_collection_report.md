# BeppeGrillo.it 2005 Posts And Comments Collection Report

Last updated: 2026-05-15

## Scope

This is a bounded feasibility data collection exercise for posts dated 2005 on BeppeGrillo.it and comments embedded in archived post pages. It uses Wayback `id_` captures and the legacy 2005 comment pattern.

## Summary Counts

- Unique 2005 post paths attempted: 507
- Posts with at least one parsed embedded comment: 445
- Parsed comments: 270,151
- Comments with raw author string: 262,714
- Comments with parsed timestamp: 262,716
- Fetch attempts: 1,655
- Successful fetch attempts: 1,006
- Failed fetch attempts: 649

## Top Posts By Parsed Comment Count

| Rank | Comments | Date | Title | URL |
|---:|---:|---|---|---|
| 1 | 3,691 | 2005-01-16 | Il muro del pianto | `http://www.beppegrillo.it/2005/01/il_muro_del_pia.html` |
| 2 | 3,672 | 2005-10-12 | Parlamento casinò | `http://www.beppegrillo.it/2005/10/parlamento_casi.html` |
| 3 | 2,791 | 2005-09-14 | I bari del potere | `http://www.beppegrillo.it/2005/09/i_bari_del_pote.html` |
| 4 | 2,431 | 2005-06-10 | 11° comandamento: non ti astenere | `http://www.beppegrillo.it/2005/06/11_comandamento.html` |
| 5 | 2,370 | 2005-10-06 | Are you lonesome tonight? | `http://www.beppegrillo.it/2005/10/non_sei_solo.html` |
| 6 | 2,313 | 2005-11-13 | La guerra ai poveri | `http://www.beppegrillo.it/2005/11/la_guerra_ai_po.html` |
| 7 | 2,255 | 2005-09-16 | La paga di Giuda | `http://www.beppegrillo.it/2005/09/la_paga_di_giud.html` |
| 8 | 2,175 | 2005-11-10 | Falluja, mon amour | `http://www.beppegrillo.it/2005/11/falluja_mon_amo.html` |
| 9 | 2,017 | 2005-12-06 | Io sono Valsusino! | `http://www.beppegrillo.it/2005/12/io_sono_valsusi.html` |
| 10 | 1,948 | 2005-08-25 | Appello del blog beppegrillo.it | `http://www.beppegrillo.it/2005/08/appello_del_blo.html` |
| 11 | 1,929 | 2005-11-20 | Fa che questo Papa... | `http://www.beppegrillo.it/2005/11/francescani_sot.html` |
| 12 | 1,919 | 2005-11-24 | Un Nobel per Milano | `http://beppegrillo.it/2005/11/un_nobel_per_mi_1.html` |
| 13 | 1,890 | 2005-10-13 | Un ponte da 3,88 miliardi di euro per risparmiare 20 minuti | `http://beppegrillo.it/2005/10/un_ponte_da_388.html` |
| 14 | 1,873 | 2005-10-20 | La figlia del Che | `http://www.beppegrillo.it/2005/10/la_figlia_del_c.html` |
| 15 | 1,854 | 2005-11-30 | TAV, no grazie! | `http://www.beppegrillo.it/2005/11/tav_no_grazie.html` |
| 16 | 1,837 | 2005-10-25 | Il dito medio del potere | `http://beppegrillo.it/2005/10/il_dito_medio_d.html` |
| 17 | 1,825 | 2005-07-30 | La caccia al mestolone | `http://www.beppegrillo.it/2005/07/la_caccia_al_me.html` |
| 18 | 1,816 | 2005-12-24 | Lettera di Natale | `http://www.beppegrillo.it/2005/12/lettera_di_nata.html` |
| 19 | 1,792 | 2005-11-07 | Liberté, egalité, fraternité | `http://www.beppegrillo.it/2005/11/liberte_egalite.html` |
| 20 | 1,785 | 2005-11-29 | Crimini elettorali | `http://www.beppegrillo.it/2005/11/crimini_elettor.html` |

## Data Organization

- Raw HTML: `data/raw/wayback/html/beppegrillo_2005/{month}/`
- Parsed posts CSV/Parquet: `data/interim/parsed_posts/beppegrillo_2005_posts.*`
- Parsed comments CSV/Parquet: `data/interim/parsed_comments/beppegrillo_2005_comments.*`
- Fetch attempts CSV/Parquet: `data/interim/fetches/beppegrillo_2005_fetch_attempts.*`

## Comment Fields

Each parsed comment includes `comment_id`, `post_id`, `author_display_hash`, `author_raw_restricted`, `comment_timestamp`, `comment_date_confidence`, `comment_order`, `body_text`, `body_html_path`, `links`, `parser_version`, `parse_confidence`, and `parser_warnings`.

Raw author strings are retained only in the restricted interim field `author_raw_restricted`; analysis should use `author_display_hash`.

## Limitations

- This parser recovers comments embedded directly in legacy post HTML. It does not yet follow external pagination or AJAX-style comment loaders.
- For each post path, the collector tries a small set of candidate captures and keeps the capture with the most parsed embedded comments.
- Comment order is page order. For this template, comments often appear reverse-chronologically, so timestamp fields should be used for temporal ordering when parsed.
- The CDX inventory was capped; additional 2005 post URLs may exist outside the current capped inventory.
