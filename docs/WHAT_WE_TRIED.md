# What We Tried

Log failed, ambiguous, rejected, and successful-but-not-used attempts. Do not use this file for ordinary completed tasks; use `TASKS.md` and completion reports instead.

## Attempts

### A-2026-05-14-001: Inspect Internet Archive item `BeppeGrillo.it2005`

- Date: 2026-05-14
- Motivation: Test whether the Internet Archive item listed in project notes contains a parseable 2005 BeppeGrillo.it HTML/comment archive.
- Agent / owner: Research Chief of Staff / Data Manager
- Method / specification / draft approach: Retrieved item metadata from `https://archive.org/metadata/BeppeGrillo.it2005` and summarized file types.
- Data / sources used: Internet Archive item metadata only; no media files downloaded.
- Result: Metadata lists media/image derivatives and metadata files, not HTML, WARC, ARC, ZIP, TAR, or GZ website files.
- What worked: Metadata inspection quickly established file structure and likely parseability.
- What did not work: The item does not appear useful for direct post/comment recovery.
- Why it failed or was set aside: No parseable blog archive or comment files were visible in item metadata.
- What we learned: Wayback CDX/page captures remain the primary path for 2005 comment recovery.
- Should revisit? Only if manual inspection of the media item becomes substantively useful for historical context.
- Related files: `docs/source_notes/internet_archive_beppegrillo_2005.md`.

### A-2026-05-14-002: Query M5S PDF captures through Wayback CDX

- Date: 2026-05-14
- Motivation: Identify archived M5S official program/campaign PDFs in the 2005-2013 pilot window.
- Agent / owner: Research Chief of Staff / Data Manager
- Method / specification / draft approach: Queried Wayback CDX for `application/pdf` captures on M5S official domains.
- Data / sources used: Wayback CDX metadata.
- Result: Several domains returned zero PDF records; `movimento5stelle.it/*` and `portale.movimento5stelle.eu/*` returned 504 Gateway Timeout errors.
- What worked: Failures were captured in `data/raw/wayback/cdx/cdx_failures.jsonl`; HTML CDX inventory for M5S domains did complete.
- What did not work: Broad PDF CDX queries were not reliable for two domains.
- Why it failed or was set aside: Wayback CDX gateway timeouts on broad PDF queries.
- What we learned: Program/PDF recovery should use known official seed URLs, targeted URL patterns, and possibly official non-Wayback sources before broad PDF CDX sweeps.
- Should revisit? Yes, with narrower year/path patterns and known program URL seeds.
- Related files: `docs/source_notes/cdx_inventory_report.md`; `data/raw/wayback/cdx/cdx_failures.jsonl`.

### A-2026-05-15-001: Target remaining large 2005 BeppeGrillo.it archive comment gaps

- Date: 2026-05-15
- Motivation: Recover comments for 2005 posts where archived monthly listing pages showed substantially more comments than the parser had recovered.
- Agent / owner: Research Chief of Staff / Data Manager
- Method / specification / draft approach: Added parser support for the later threaded `comment-parent-id-depth` template, retried high-gap posts with larger Wayback capture candidate sets, and reparsed all already-downloaded raw HTML so transient Wayback failures could not overwrite better local captures.
- Data / sources used: Wayback `id_` captures from the current CDX-derived 2005 inventory; archived monthly listing pages with visible `Commenti (N)` counts.
- Result: Parsed comments increased from 190,529 before this pass to 270,151 after a final HTTPS Wayback retry recovered the last two failed post pages. The archive-visible positive gap across audited rows fell from 11,566 to 548. The remaining gap has no row above 500 comments and only two rows above 100 comments.
- What worked: The threaded-template parser and raw-cache reparse recovered many comments without expanding beyond the approved 2005 feasibility slice.
- What did not work: Additional slow retries did not improve the two largest remaining gaps: `Pedofilia mediatica` and `Io sono Valsusino!`.
- Why it failed or was set aside: Available successful captures for those posts still contain fewer parsed comments than the monthly archive listing counts, and additional Wayback attempts did not produce a better parseable capture.
- What we learned: 2005 comment recovery is strong enough for a feasibility-positive pilot slice, but archive completeness metrics and capture-level provenance must remain part of any analysis sample restriction.
- Should revisit? Yes, after implementing broader CDX pagination or if external archived bundles become available.
- Related files: `code/parse/parser_beppegrillo_legacy.py`; `code/extract/reparse_beppegrillo_2005_raw_cache.py`; `docs/source_notes/beppegrillo_2005_coverage_audit.md`.

### A-2026-05-15-002: Collect and audit 2006 BeppeGrillo.it posts/comments

- Date: 2026-05-15
- Motivation: Extend the approved early-period feasibility pilot from 2005 to 2006.
- Agent / owner: Research Chief of Staff / Data Manager
- Method / specification / draft approach: Parameterized the 2005 collector, archive-count collector, raw-cache reparser, and audit scripts by year; collected 2006 post captures from the current CDX-derived inventory; retried failed rows and top archive-gap rows with larger capture candidate sets.
- Data / sources used: Wayback `id_` captures for BeppeGrillo.it 2006 post candidates and archived monthly listing pages with visible `Commenti (N)` counts.
- Result: Recovered 468 candidate 2006 post paths, 439 successfully retrieved/parsed post pages, 365 posts with parsed comments, and 442,328 parsed comments after an additional largest-gap recovery pass. Twenty-nine 2006 post pages remain `no_successful_capture`. The 2006 archive-visible positive gap remains materially larger than 2005: 37,114 comments across audited rows after top-gap retries.
- What worked: Year-parameterized collection and parser support recovered a large 2006 comment corpus, including many high-comment posts.
- What did not work: Several older/larger Wayback captures repeatedly returned connection refusals; some monthly archive count rows map to URLs absent from the current post inventory or to captures where embedded comments remain incomplete.
- Why it failed or was set aside: Further retries were becoming rate-limited and time-expensive, and the remaining gaps should be handled as a structured coverage problem rather than open-ended scraping.
- What we learned: 2006 is feasible but less complete than 2005 under the current CDX inventory and retry strategy; coverage metrics must be used in sample restrictions and robustness checks.
- Should revisit? Yes, with broader CDX pagination, lower-rate targeted retries, and parser/pagination inspection for the largest residual gaps.
- Related files: `docs/source_notes/beppegrillo_2006_collection_report.md`; `docs/source_notes/beppegrillo_2006_coverage_audit.md`.

### A-2026-05-15-003: Collect and audit 2007 BeppeGrillo.it posts/comments

- Date: 2026-05-15 to 2026-05-16
- Motivation: Continue the approved early-period feasibility pilot after the requested 20-minute pause.
- Agent / owner: Research Chief of Staff / Data Manager
- Method / specification / draft approach: Ran the year-parameterized Wayback collector for 2007, resumed after timeout checkpoints, ran failed-row recovery passes, used a warmed-cache single-worker retry for October residual failures, ran a targeted archive-gap recovery pass, collected available monthly archive-visible comment counts, and generated the 2007 coverage audit.
- Data / sources used: Wayback `id_` captures for BeppeGrillo.it 2007 post candidates and available archived monthly listing pages with visible `Commenti (N)` counts.
- Result: Recovered 538 candidate 2007 post paths, 538 successfully retrieved/parsed post pages, 326 posts with parsed comments, and 273,625 parsed comments. No 2007 post pages remain `no_successful_capture` in the current CDX-derived inventory. The archive-count audit is sparse: 21 rows with 25,454 archive-visible comments and a 2,152 positive gap.
- What worked: The same parser recovered the main 2007 comment corpus, including Vaffanculo-Day period posts. A warmed-cache, single-worker retry recovered the ten residual October failures after earlier connection refusals/timeouts. A targeted archive-gap pass reduced large visible-count gaps and eliminated gaps of 500 or more among the parsed audit rows.
- What did not work: Archive-count coverage is much sparser than 2005-2006 because many monthly archive fetches failed or did not expose parseable `Commenti (N)` rows. Sixteen of the 21 audit rows still have a positive visible-count gap, likely reflecting capture timing, pagination/template limits, or archive-listing artifacts.
- Why it failed or was set aside: Further retrying would be rate-limited and should be handled through a lower-rate recovery job or broader CDX pagination rather than open-ended scraping.
- What we learned: 2007 is recoverable at useful scale in the current inventory, but archive-listing coverage remains weaker than 2005 and residual comment completeness needs a pagination/template audit.
- Should revisit? Yes, with targeted parser/pagination work for the remaining positive archive-visible comment gaps and with fuller CDX pagination before treating the inventory as exhaustive.
- Related files: `docs/source_notes/beppegrillo_2007_collection_report.md`; `docs/source_notes/beppegrillo_2007_coverage_audit.md`.

## Template

### A-YYYY-MM-DD-001: [Attempt]

- Date:
- Motivation:
- Agent / owner:
- Method / specification / draft approach:
- Data / sources used:
- Result:
- What worked:
- What did not work:
- Why it failed or was set aside:
- What we learned:
- Should revisit? yes/no/conditions
- Related files:
