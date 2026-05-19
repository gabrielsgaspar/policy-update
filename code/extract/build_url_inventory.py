"""Build an initial URL inventory from seed URLs and Wayback CDX metadata."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import pandas as pd


ASSET_EXTENSIONS = {
    ".bmp",
    ".css",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".m4v",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".ogv",
    ".png",
    ".rss",
    ".svg",
    ".swf",
    ".txt",
    ".webp",
    ".xml",
}


POST_PATTERNS = [
    re.compile(r"/archives/(?P<year>20\d{2}|19\d{2})/(?P<month>\d{2})/(?P<slug>[^/?#]+)\.html?$"),
    re.compile(r"/(?P<year>20\d{2}|19\d{2})/(?P<month>\d{2})/(?P<slug>[^/?#]+)\.html?$"),
]

ARCHIVE_PATTERNS = [
    re.compile(r"/archives/?$"),
    re.compile(r"/archives/(?P<year>20\d{2}|19\d{2})/?$"),
    re.compile(r"/archives/(?P<year>20\d{2}|19\d{2})/(?P<month>\d{2})/?$"),
    re.compile(r"/category/archivio"),
    re.compile(r"/(?P<year>20\d{2}|19\d{2})/?$"),
    re.compile(r"/(?P<year>20\d{2}|19\d{2})/(?P<month>\d{2})/?$"),
]


def iter_jsonl(paths: list[Path]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for path in paths:
        if path.stat().st_size == 0:
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                records.append(json.loads(line))
    return records


def normalize_url(url: str) -> str:
    parts = urlsplit(str(url).strip())
    scheme = (parts.scheme or "http").lower()
    netloc = parts.netloc.lower()
    if netloc.endswith(":80") and scheme == "http":
        netloc = netloc[:-3]
    if netloc.endswith(":443") and scheme == "https":
        netloc = netloc[:-4]
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((scheme, netloc, path, query, ""))


def file_extension(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return suffix


def extract_date_parts(path: str) -> tuple[str, str, str]:
    for pattern in POST_PATTERNS + ARCHIVE_PATTERNS:
        match = pattern.search(path)
        if match:
            return (
                match.groupdict().get("year", "") or "",
                match.groupdict().get("month", "") or "",
                match.groupdict().get("slug", "") or "",
            )
    return "", "", ""


def classify_url(row: pd.Series) -> str:
    url = str(row.get("normalized_url", ""))
    parts = urlsplit(url)
    path = parts.path.lower()
    query = parts.query.lower()
    mimetype = str(row.get("mimetype", "")).lower()
    group = str(row.get("query_group", "")).lower()

    if "comment" in path or "comment" in query or "commenti" in path or "commenti" in query:
        return "comment_page_candidate"
    if any(token in query for token in ["page=", "paged=", "cpage=", "cp=", "p="]) or "/page/" in path:
        return "pagination_candidate"
    if mimetype == "application/pdf" or path.endswith(".pdf"):
        return "pdf_or_program_candidate"
    if file_extension(path) in ASSET_EXTENSIONS:
        return "asset_or_feed"
    if any(pattern.search(path) for pattern in POST_PATTERNS):
        if "movimento5stelle" in group:
            return "m5s_post_or_output_candidate"
        return "blog_post_candidate"
    if any(pattern.search(path) for pattern in ARCHIVE_PATTERNS):
        return "archive_listing_candidate"
    if path in {"", "/"}:
        return "homepage_candidate"
    if "movimento5stelle" in group:
        return "m5s_page_candidate"
    return "unclassified_html_candidate"


def source_priority(group: str) -> str:
    if group in {"beppegrillo", "blogdellestelle"}:
        return "P0"
    if group.startswith("movimento5stelle"):
        return "P1"
    return "TBD"


def build_inventory(cdx_frame: pd.DataFrame, seed_frame: pd.DataFrame) -> pd.DataFrame:
    cdx = cdx_frame.copy()
    if cdx.empty:
        return cdx
    cdx["normalized_url"] = cdx["original"].map(normalize_url)
    cdx["domain"] = cdx["normalized_url"].map(lambda value: urlsplit(value).netloc)
    cdx["path"] = cdx["normalized_url"].map(lambda value: urlsplit(value).path)
    cdx["source_type"] = cdx.apply(classify_url, axis=1)
    date_parts = cdx["path"].map(extract_date_parts)
    cdx["candidate_year"] = [part[0] for part in date_parts]
    cdx["candidate_month"] = [part[1] for part in date_parts]
    cdx["candidate_slug"] = [part[2] for part in date_parts]
    cdx["candidate_year"] = cdx["candidate_year"].where(cdx["candidate_year"] != "", cdx["timestamp"].str.slice(0, 4))
    cdx["candidate_month"] = cdx["candidate_month"].where(cdx["candidate_month"] != "", cdx["timestamp"].str.slice(4, 6))
    cdx["first_seen_source"] = "wayback_cdx"
    cdx["first_seen_at"] = cdx["timestamp"]
    cdx["wayback_timestamp"] = cdx["timestamp"]
    cdx["cdx_digest"] = cdx["digest"]
    cdx["priority"] = cdx["query_group"].map(source_priority)
    cdx["notes"] = ""

    grouped = (
        cdx.sort_values("timestamp")
        .groupby(["normalized_url", "cdx_digest"], dropna=False)
        .agg(
            url=("original", "first"),
            domain=("domain", "first"),
            source_type=("source_type", "first"),
            first_seen_source=("first_seen_source", "first"),
            first_seen_at=("first_seen_at", "first"),
            candidate_year=("candidate_year", "first"),
            candidate_month=("candidate_month", "first"),
            candidate_slug=("candidate_slug", "first"),
            wayback_timestamp=("wayback_timestamp", "first"),
            first_capture_timestamp=("timestamp", "min"),
            last_capture_timestamp=("timestamp", "max"),
            capture_count=("timestamp", "size"),
            cdx_length=("length", "first"),
            mimetype=("mimetype", "first"),
            query_group=("query_group", "first"),
            query_domain=("query_domain", "first"),
            priority=("priority", "first"),
            notes=("notes", "first"),
        )
        .reset_index()
    )

    seed_rows = seed_frame.copy()
    seed_rows["url"] = seed_rows["url"].astype(str)
    seed_rows["normalized_url"] = seed_rows["normalized_url"].astype(str)
    seed_rows["source_type"] = "seed_url"
    seed_rows["first_seen_at"] = ""
    seed_rows["candidate_year"] = ""
    seed_rows["candidate_month"] = ""
    seed_rows["candidate_slug"] = ""
    seed_rows["wayback_timestamp"] = ""
    seed_rows["first_capture_timestamp"] = ""
    seed_rows["last_capture_timestamp"] = ""
    seed_rows["capture_count"] = 0
    seed_rows["cdx_digest"] = ""
    seed_rows["cdx_length"] = ""
    seed_rows["mimetype"] = seed_rows["expected_content_type"]
    seed_rows["query_group"] = seed_rows["source_group"]
    seed_rows["query_domain"] = seed_rows["domain"]

    keep_columns = [
        "url",
        "normalized_url",
        "domain",
        "source_type",
        "first_seen_source",
        "first_seen_at",
        "candidate_year",
        "candidate_month",
        "candidate_slug",
        "wayback_timestamp",
        "first_capture_timestamp",
        "last_capture_timestamp",
        "capture_count",
        "cdx_digest",
        "cdx_length",
        "mimetype",
        "query_group",
        "query_domain",
        "priority",
        "notes",
    ]
    return pd.concat([seed_rows[keep_columns], grouped[keep_columns]], ignore_index=True)


def write_cdx_summary(frame: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if frame.empty:
        pd.DataFrame().to_csv(output_path, index=False)
        return
    frame = frame.copy()
    frame["capture_year"] = frame["timestamp"].str.slice(0, 4)
    summary = (
        frame.groupby(["query_group", "query_domain", "mimetype", "capture_year"], dropna=False)
        .agg(
            records=("timestamp", "size"),
            first_capture=("timestamp", "min"),
            last_capture=("timestamp", "max"),
            unique_original_urls=("original", "nunique"),
            unique_digests=("digest", "nunique"),
        )
        .reset_index()
        .sort_values(["query_group", "query_domain", "mimetype", "capture_year"])
    )
    summary.to_csv(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-csv", type=Path, default=Path("data/metadata/seed_urls.csv"))
    parser.add_argument("--cdx-dir", type=Path, default=Path("data/raw/wayback/cdx"))
    parser.add_argument("--output-parquet", type=Path, default=Path("data/metadata/url_inventory.parquet"))
    parser.add_argument("--output-csv", type=Path, default=Path("data/metadata/url_inventory_sample.csv"))
    parser.add_argument("--summary", type=Path, default=Path("data/metadata/cdx_inventory_summary.csv"))
    parser.add_argument("--type-summary", type=Path, default=Path("data/metadata/url_inventory_type_summary.csv"))
    args = parser.parse_args()

    seed_frame = pd.read_csv(args.seed_csv)
    cdx_paths = sorted(path for path in args.cdx_dir.glob("*_cdx.jsonl") if path.name != "cdx_failures.jsonl")
    cdx_records = iter_jsonl(cdx_paths)
    cdx_frame = pd.DataFrame(cdx_records)
    if not cdx_frame.empty:
        cdx_frame["timestamp"] = cdx_frame["timestamp"].astype(str)
    inventory = build_inventory(cdx_frame, seed_frame)

    args.output_parquet.parent.mkdir(parents=True, exist_ok=True)
    inventory.to_parquet(args.output_parquet, index=False)
    inventory.head(1000).to_csv(args.output_csv, index=False)
    write_cdx_summary(cdx_frame, args.summary)
    (
        inventory.groupby(["query_group", "source_type"], dropna=False)
        .size()
        .reset_index(name="records")
        .sort_values(["query_group", "source_type"])
        .to_csv(args.type_summary, index=False)
    )
    print(f"Wrote {len(inventory):,} inventory rows to {args.output_parquet}")
    print(f"Wrote sample CSV to {args.output_csv}")
    print(f"Wrote CDX summary to {args.summary}")


if __name__ == "__main__":
    main()

