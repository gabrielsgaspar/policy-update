# Assumptions

## Active Assumptions

### A-001: Historical comments can be recovered for a meaningful pilot

- Type: data
- Used in: source inventory, crawl strategy, pilot feasibility design
- Strength: medium
- Evidence: `DATA.md` lists multiple candidate sources, including current pages, Il Blog delle Stelle, Wayback CDX, and the Internet Archive item `BeppeGrillo.it2005`.
- Threats: comments may be deleted, paginated incompletely, absent from current pages, missing from Wayback captures, or duplicated across mirrors.
- Critical-agent concerns: archive completeness may be non-random by issue, year, popularity, or platform migration.
- How to test or justify: run source inventory, inspect the 2005 Internet Archive item, query CDX, and compute archive completeness metrics.
- Status: untested.

### A-002: Blog commenters are a meaningful supporter-input population

- Type: theoretical / measurement
- Used in: theory of supporter responsiveness and proposal adoption
- Strength: medium
- Evidence: `PROJECT.md` frames the blog as central to M5S identity, mobilization, agenda formation, and supporter relations.
- Threats: commenters are not representative voters; they may be unusually active supporters, opponents, trolls, spam, or coordinated actors.
- Critical-agent concerns: results should be framed as responsiveness to organized digital supporters, not to the electorate.
- How to test or justify: characterize commenters at the aggregate level, compare comment attention to broader public/media signals, and avoid individual-level claims.
- Status: active.

### A-003: Later M5S text can be temporally linked to prior supporter input

- Type: identification / data
- Used in: issue-week panels and proposal-level event history
- Strength: medium
- Evidence: `PROJECT.md` proposes lagged issue attention, proposal adoption, and institutional-output linkages.
- Threats: common shocks, original post topics, media agenda, and leader-driven agenda setting may jointly produce comment and output attention.
- Critical-agent concerns: comments are replies to posts, so apparent responsiveness may reflect continued attention to an issue already chosen by Grillo/M5S.
- How to test or justify: control for prior party attention, original post topic, media/public agenda, comparison-party outputs, and future-comment placebos.
- Status: design-stage.

### A-004: ML/LLM labels can be validated enough to support measurement

- Type: measurement / modeling
- Used in: issue classification, proposal extraction, stance, deliberative quality, semantic matching
- Strength: medium
- Evidence: `PROJECT.md` and `DATA.md` specify human-coded validation, prompt/model versioning, schema logging, and error audits.
- Threats: domain shift across years, unstable labels, invalid JSON, rhetorical changes, and measurement leakage.
- Critical-agent concerns: LLM measurement must not substitute for research design or unsupported causal claims.
- How to test or justify: build a stratified gold standard, report precision/recall/F1/calibration, validate by historical phase, and keep human review status.
- Status: planned.

## Template

### A-XXX: [Assumption]

- Type: theoretical / behavioral / institutional / data / identification / measurement / modeling / external validity
- Used in:
- Strength: low / medium / high
- Evidence:
- Threats:
- Critical-agent concerns:
- How to test or justify:
- Status:
