-- DuckDB schema for the Beppe Grillo / M5S feasibility pilot.
-- Raw files remain immutable on disk; these tables store provenance,
-- parsed records, measurement labels, and later analysis linkages.

CREATE TABLE IF NOT EXISTS sources (
    source_id VARCHAR PRIMARY KEY,
    source_name VARCHAR NOT NULL,
    source_type VARCHAR NOT NULL,
    base_url VARCHAR,
    owner_or_institution VARCHAR,
    canonicality VARCHAR,
    access_notes VARCHAR,
    license_notes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS fetches (
    fetch_id VARCHAR PRIMARY KEY,
    source_id VARCHAR,
    url VARCHAR NOT NULL,
    normalized_url VARCHAR,
    canonical_url VARCHAR,
    wayback_timestamp VARCHAR,
    retrieved_at TIMESTAMP NOT NULL,
    http_status INTEGER,
    mimetype VARCHAR,
    content_hash VARCHAR,
    raw_path VARCHAR,
    cdx_digest VARCHAR,
    cdx_length BIGINT,
    fetch_method VARCHAR,
    retry_count INTEGER DEFAULT 0,
    error_message VARCHAR,
    restricted_raw_flag BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS posts (
    post_id VARCHAR PRIMARY KEY,
    source_id VARCHAR,
    fetch_id VARCHAR,
    url VARCHAR,
    canonical_url VARCHAR,
    title VARCHAR,
    author VARCHAR,
    date_published TIMESTAMP,
    date_modified TIMESTAMP,
    date_confidence VARCHAR,
    body_text VARCHAR,
    body_html_path VARCHAR,
    category VARCHAR,
    tags VARCHAR,
    visible_comment_count INTEGER,
    parsed_comment_count INTEGER,
    language VARCHAR,
    template_type VARCHAR,
    parser_version VARCHAR,
    parse_confidence DOUBLE,
    parser_warnings VARCHAR,
    notes VARCHAR,
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    FOREIGN KEY (fetch_id) REFERENCES fetches(fetch_id)
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id VARCHAR PRIMARY KEY,
    post_id VARCHAR,
    fetch_id VARCHAR,
    author_display_hash VARCHAR,
    author_raw_restricted VARCHAR,
    comment_timestamp TIMESTAMP,
    comment_date_confidence VARCHAR,
    comment_order INTEGER,
    parent_comment_id VARCHAR,
    body_text VARCHAR,
    body_html_path VARCHAR,
    links VARCHAR,
    language VARCHAR,
    spam_score DOUBLE,
    duplicate_score DOUBLE,
    moderation_marker VARCHAR,
    template_type VARCHAR,
    parser_version VARCHAR,
    parse_confidence DOUBLE,
    parser_warnings VARCHAR,
    restricted_raw_flag BOOLEAN DEFAULT FALSE,
    notes VARCHAR,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (fetch_id) REFERENCES fetches(fetch_id)
);

CREATE TABLE IF NOT EXISTS political_outputs (
    output_id VARCHAR PRIMARY KEY,
    source_id VARCHAR,
    fetch_id VARCHAR,
    output_type VARCHAR,
    actor VARCHAR,
    party VARCHAR,
    institution VARCHAR,
    legislature VARCHAR,
    date_published TIMESTAMP,
    date_introduced TIMESTAMP,
    date_confidence VARCHAR,
    title VARCHAR,
    body_text VARCHAR,
    jurisdiction VARCHAR,
    url VARCHAR,
    raw_path VARCHAR,
    parser_version VARCHAR,
    parse_confidence DOUBLE,
    parser_warnings VARCHAR,
    notes VARCHAR,
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    FOREIGN KEY (fetch_id) REFERENCES fetches(fetch_id)
);

CREATE TABLE IF NOT EXISTS text_units (
    text_unit_id VARCHAR PRIMARY KEY,
    parent_type VARCHAR NOT NULL,
    parent_id VARCHAR NOT NULL,
    unit_type VARCHAR NOT NULL,
    unit_order INTEGER,
    text VARCHAR NOT NULL,
    char_start INTEGER,
    char_end INTEGER,
    language VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS llm_labels (
    label_id VARCHAR PRIMARY KEY,
    text_unit_id VARCHAR,
    model_provider VARCHAR,
    model_name VARCHAR,
    model_version VARCHAR,
    prompt_version VARCHAR,
    schema_version VARCHAR,
    temperature DOUBLE,
    seed INTEGER,
    top_p DOUBLE,
    run_timestamp TIMESTAMP,
    input_hash VARCHAR,
    output_json VARCHAR,
    valid_json_flag BOOLEAN,
    retry_count INTEGER DEFAULT 0,
    human_review_status VARCHAR,
    confidence DOUBLE,
    notes VARCHAR,
    FOREIGN KEY (text_unit_id) REFERENCES text_units(text_unit_id)
);

CREATE TABLE IF NOT EXISTS issue_labels (
    issue_label_id VARCHAR PRIMARY KEY,
    text_unit_id VARCHAR,
    issue_scheme VARCHAR,
    issue_major VARCHAR,
    issue_minor VARCHAR,
    probability DOUBLE,
    label_source VARCHAR,
    validated_flag BOOLEAN DEFAULT FALSE,
    notes VARCHAR,
    FOREIGN KEY (text_unit_id) REFERENCES text_units(text_unit_id)
);

CREATE TABLE IF NOT EXISTS proposals (
    proposal_id VARCHAR PRIMARY KEY,
    text_unit_id VARCHAR,
    post_id VARCHAR,
    comment_id VARCHAR,
    proposal_text_span VARCHAR,
    proposal_summary VARCHAR,
    issue_major VARCHAR,
    issue_minor VARCHAR,
    policy_instrument VARCHAR,
    target_level VARCHAR,
    stance VARCHAR,
    specificity_score DOUBLE,
    uses_evidence BOOLEAN,
    contains_local_information BOOLEAN,
    contains_mobilization_request BOOLEAN,
    novelty_score DOUBLE,
    confidence DOUBLE,
    validated_flag BOOLEAN DEFAULT FALSE,
    human_review_status VARCHAR,
    notes VARCHAR,
    FOREIGN KEY (text_unit_id) REFERENCES text_units(text_unit_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
);

CREATE TABLE IF NOT EXISTS proposal_matches (
    match_id VARCHAR PRIMARY KEY,
    proposal_id VARCHAR,
    output_id VARCHAR,
    matched_text_unit_id VARCHAR,
    match_method VARCHAR,
    embedding_model VARCHAR,
    similarity_score DOUBLE,
    cross_encoder_score DOUBLE,
    human_validated_match BOOLEAN,
    match_date TIMESTAMP,
    lag_days INTEGER,
    notes VARCHAR,
    FOREIGN KEY (proposal_id) REFERENCES proposals(proposal_id),
    FOREIGN KEY (output_id) REFERENCES political_outputs(output_id),
    FOREIGN KEY (matched_text_unit_id) REFERENCES text_units(text_unit_id)
);

CREATE TABLE IF NOT EXISTS archive_coverage (
    coverage_id VARCHAR PRIMARY KEY,
    post_id VARCHAR,
    normalized_url VARCHAR,
    expected_comment_count_visible INTEGER,
    parsed_comment_count INTEGER,
    comment_count_ratio DOUBLE,
    number_of_captures INTEGER,
    first_capture_timestamp VARCHAR,
    last_capture_timestamp VARCHAR,
    capture_span_days INTEGER,
    template_type VARCHAR,
    has_comment_pagination BOOLEAN,
    pagination_complete_flag BOOLEAN,
    archive_source_count INTEGER,
    coverage_score_0_to_1 DOUBLE,
    notes VARCHAR,
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS source_events (
    event_id VARCHAR PRIMARY KEY,
    date_start DATE NOT NULL,
    date_end DATE,
    event_type VARCHAR,
    title VARCHAR,
    description VARCHAR,
    source_url VARCHAR,
    relevance_issues VARCHAR,
    m5s_specific_flag BOOLEAN,
    national_shock_flag BOOLEAN,
    notes VARCHAR
);

