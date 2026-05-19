# Data Ethics Protocol

Last updated: 2026-05-14

## Scope

This protocol governs the feasibility pilot for public comments and related public political text from Beppe Grillo, Il Blog delle Stelle, M5S, parliamentary, media, and comparison-party sources.

The pilot is approved as feasibility-only, measurement-first, and identification-ready. It does not authorize full-scale scraping, modeling, or empirical analysis without a later PI decision.

## Core Rules

1. Public comments are treated as ethically sensitive even when visible online.
2. Raw data is immutable. Raw HTML, JSON, PDF, WARC, and API responses must be saved exactly as collected.
3. Ordinary commenters must not be deanonymized.
4. Analysis tables must use salted hashes for commenter display names or handles.
5. Raw author strings, if retained, must remain in restricted raw/interim fields and must not be exported to analysis datasets.
6. Do not publish ordinary-user comment text verbatim by default. Use paraphrases unless the PI approves a specific quotation rule and legal/ethics basis.
7. Do not collect private, login-gated, deleted-private, or non-public data.
8. Do not attempt to infer real identities from commenter names, links, writing style, email fragments, or external profiles.
9. Do not manually edit raw data.
10. Every record must preserve provenance sufficient to audit source, timing, parser, and retrieval status.

## Required Provenance

Every fetch must record:

- source name and source group;
- original URL;
- normalized URL;
- archival URL, if applicable;
- Wayback timestamp, if applicable;
- retrieval timestamp;
- HTTP status;
- MIME type;
- content hash;
- raw path;
- fetch method;
- retry count;
- error message, if any.

Every parsed post/comment/output must record:

- source and fetch ID;
- parser name and parser version;
- template type, where detectable;
- parse confidence;
- structured warnings;
- text extraction status;
- date or timestamp;
- date confidence;
- content hash or text hash;
- raw path or HTML fragment path.

## Commenter Identifiers

Analysis datasets may include:

- salted hash of display name;
- aggregate activity counts;
- source/thread-level identifiers;
- broad self-declared geography only if explicitly present in the public comment text and needed for approved analysis.

Analysis datasets must not include:

- raw usernames or display names;
- emails;
- IP addresses;
- profile URLs tied to ordinary commenters;
- any inferred identity.

If raw author strings are retained for deduplication, they must stay in restricted raw/interim storage and be excluded from shared processed/analysis files.

## Quotation Rule

Default publication rule: paraphrase ordinary-user comments.

Direct quotation requires PI approval and a documented reason, such as:

- comment is by a public political figure;
- comment was officially highlighted by M5S/Grillo or a public institution;
- legal/ethics review supports direct quotation;
- quotation is essential and cannot be replaced by paraphrase.

## Source Restrictions

For each source, record:

- access method;
- terms/license notes;
- robots/rate-limit notes for live websites;
- whether source is official, archival, third-party, or convenience layer;
- whether raw content can be redistributed or only derived features can be shared.

Official parliamentary and election sources should be treated as canonical where feasible. Third-party layers such as Openpolis can be used for discovery or convenience but must be marked as third-party.

## Pilot Gates

No comment-level data should enter processed analysis tables until:

- this protocol is in place;
- author identifiers are hashed or excluded;
- raw author strings are restricted;
- source restrictions are documented;
- parse warnings and coverage metrics are available.

No empirical modeling should begin until the PI approves the pilot feasibility memo.

