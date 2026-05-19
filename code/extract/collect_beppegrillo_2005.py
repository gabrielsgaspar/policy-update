"""Collect and parse BeppeGrillo.it yearly posts and embedded comments.

This is a bounded feasibility exercise. It downloads selected Wayback captures
for posts in a requested year, keeps raw HTML immutable, parses embedded comments, and
writes interim tables plus a source note report.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PARSER_PATH = ROOT / "code" / "parse" / "parser_beppegrillo_legacy.py"
PARSER_SPEC = importlib.util.spec_from_file_location("parser_beppegrillo_legacy", PARSER_PATH)
if PARSER_SPEC is None or PARSER_SPEC.loader is None:
    raise RuntimeError(f"Could not load parser from {PARSER_PATH}")
PARSER_MODULE = importlib.util.module_from_spec(PARSER_SPEC)
PARSER_SPEC.loader.exec_module(PARSER_MODULE)
parse_post_page = PARSER_MODULE.parse_post_page


USER_AGENT = "policy-update-beppegrillo-year-feasibility/0.1 (+research)"


@dataclass(frozen=True)
class CaptureCandidate:
    path: str
    original_url: str
    normalized_url: str
    timestamp: str
    cdx_digest: str
    cdx_length: int
    candidate_month: str
    candidate_slug: str


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def wayback_url(timestamp: str, original_url: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original_url}"


def canonical_post_id(path: str) -> str:
    cleaned = path.strip("/").replace("/", "_").replace(".", "_")
    return f"beppegrillo_{cleaned}"


def build_candidates(inventory_path: Path, max_attempts_per_post: int, year: int) -> dict[str, list[CaptureCandidate]]:
    inv = pd.read_parquet(inventory_path)
    posts = inv[
        (inv["query_group"] == "beppegrillo")
        & (inv["source_type"] == "blog_post_candidate")
        & (inv["candidate_year"].astype(str) == str(year))
    ].copy()
    posts["path"] = posts["normalized_url"].map(lambda value: urlsplit(str(value)).path)
    posts["timestamp"] = posts["wayback_timestamp"].astype(str)
    posts["cdx_length_int"] = pd.to_numeric(posts["cdx_length"], errors="coerce").fillna(0).astype(int)

    candidates: dict[str, list[CaptureCandidate]] = {}
    for path, group in posts.groupby("path"):
        group = group.drop_duplicates(subset=["timestamp", "cdx_digest"]).copy()
        old = group[group["timestamp"].str.slice(0, 4).astype(int).between(year, year + 2, inclusive="both")]
        picks = []
        if not old.empty:
            picks.extend(old.sort_values("timestamp").head(1).to_dict("records"))
            picks.extend(old.sort_values("cdx_length_int", ascending=False).head(1).to_dict("records"))
            picks.extend(old.sort_values("timestamp", ascending=False).head(1).to_dict("records"))
        if len(picks) < max_attempts_per_post:
            picks.extend(group.sort_values("timestamp").head(1).to_dict("records"))
            picks.extend(group.sort_values("cdx_length_int", ascending=False).head(1).to_dict("records"))
            picks.extend(group.sort_values("timestamp", ascending=False).head(1).to_dict("records"))
        if len(picks) < max_attempts_per_post:
            picks.extend(old.sort_values("cdx_length_int", ascending=False).head(max_attempts_per_post).to_dict("records"))
            picks.extend(group.sort_values("cdx_length_int", ascending=False).head(max_attempts_per_post).to_dict("records"))

        deduped = []
        seen = set()
        for row in picks:
            key = (str(row["timestamp"]), str(row["cdx_digest"]))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(row)
            if len(deduped) >= max_attempts_per_post:
                break

        candidates[path] = [
            CaptureCandidate(
                path=path,
                original_url=str(row["url"]),
                normalized_url=str(row["normalized_url"]),
                timestamp=str(row["timestamp"]),
                cdx_digest=str(row["cdx_digest"]),
                cdx_length=int(row["cdx_length_int"]),
                candidate_month=str(row["candidate_month"]).zfill(2),
                candidate_slug=str(row["candidate_slug"]),
            )
            for row in deduped
        ]
    return candidates


def raw_path_for(candidate: CaptureCandidate, content_hash: str, year: int) -> Path:
    return (
        Path(f"data/raw/wayback/html/beppegrillo_{year}")
        / candidate.candidate_month
        / f"{candidate.timestamp}_{content_hash}.html"
    )


def fetch_candidate(candidate: CaptureCandidate, timeout: int, retries: int, sleep: float, year: int) -> tuple[dict[str, object], bytes | None]:
    fetch_id = str(uuid.uuid4())
    fetch_url = wayback_url(candidate.timestamp, candidate.original_url)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    error = ""
    response = None
    for attempt in range(retries + 1):
        try:
            response = requests.get(fetch_url, timeout=(10, timeout), headers={"User-Agent": USER_AGENT})
            if response.status_code >= 500 and attempt < retries:
                time.sleep(sleep * (attempt + 1))
                continue
            break
        except Exception as exc:  # pragma: no cover - network/audit path
            error = repr(exc)
            if attempt < retries:
                time.sleep(sleep * (attempt + 1))

    if response is None:
        return (
            {
                "fetch_id": fetch_id,
                "post_path": candidate.path,
                "url": candidate.original_url,
                "normalized_url": candidate.normalized_url,
                "wayback_timestamp": candidate.timestamp,
                "retrieved_at": retrieved_at,
                "http_status": "",
                "mimetype": "",
                "content_hash": "",
                "raw_path": "",
                "cdx_digest": candidate.cdx_digest,
                "cdx_length": candidate.cdx_length,
                "fetch_method": "wayback_id",
                "retry_count": retries,
                "error_message": error or "No response",
            },
            None,
        )

    content = response.content
    content_hash = sha256_bytes(content)
    raw_path = raw_path_for(candidate, content_hash, year)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if not raw_path.exists():
        raw_path.write_bytes(content)
    return (
        {
            "fetch_id": fetch_id,
            "post_path": candidate.path,
            "url": candidate.original_url,
            "normalized_url": candidate.normalized_url,
            "wayback_timestamp": candidate.timestamp,
            "retrieved_at": retrieved_at,
            "http_status": response.status_code,
            "mimetype": response.headers.get("Content-Type", ""),
            "content_hash": content_hash,
            "raw_path": raw_path.as_posix(),
            "cdx_digest": candidate.cdx_digest,
            "cdx_length": candidate.cdx_length,
            "fetch_method": "wayback_id",
            "retry_count": 0,
            "error_message": "" if response.status_code < 400 else f"HTTP {response.status_code}",
        },
        content,
    )


def collect_one(path: str, candidates: list[CaptureCandidate], timeout: int, retries: int, sleep: float, year: int) -> dict[str, object]:
    attempts = []
    best_post = None
    best_comments = []
    best_fetch = None
    post_id = canonical_post_id(path)

    for candidate in candidates:
        fetch_meta, content = fetch_candidate(candidate, timeout, retries, sleep, year)
        attempts.append(fetch_meta)
        if content is None or fetch_meta.get("http_status") != 200:
            continue
        try:
            post, comments = parse_post_page(content, post_id, str(fetch_meta["fetch_id"]), str(fetch_meta["raw_path"]))
        except Exception as exc:  # pragma: no cover - parser audit path
            fetch_meta["error_message"] = f"{fetch_meta.get('error_message', '')}|parse_error:{exc!r}".strip("|")
            continue
        if best_post is None or len(comments) > len(best_comments):
            best_post = post
            best_comments = comments
            best_fetch = fetch_meta
        time.sleep(sleep)

    if best_post is None:
        best_post = {
            "post_id": post_id,
            "fetch_id": "",
            "url": candidates[0].original_url if candidates else "",
            "canonical_url": candidates[0].normalized_url if candidates else "",
            "title": "",
            "author": "",
            "date_published": "",
            "date_modified": "",
            "date_confidence": "missing",
            "body_text": "",
            "body_html_path": "",
            "category": "",
            "tags": "",
            "visible_comment_count": "",
            "parsed_comment_count": 0,
            "language": "it",
            "template_type": "",
            "parser_version": "",
            "parse_confidence": 0,
            "parser_warnings": "no_successful_capture",
            "notes": "",
        }
    else:
        best_post["url"] = best_fetch["url"] if best_fetch else ""
        best_post["canonical_url"] = best_fetch["normalized_url"] if best_fetch else ""
        best_post["wayback_timestamp"] = best_fetch["wayback_timestamp"] if best_fetch else ""
        best_post["selected_raw_path"] = best_fetch["raw_path"] if best_fetch else ""

    return {
        "post": best_post,
        "comments": best_comments,
        "attempts": attempts,
        "candidate_count": len(candidates),
    }


def write_table(frame: pd.DataFrame, csv_path: Path, parquet_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    safe_frame = frame.copy()
    for column in safe_frame.columns:
        if safe_frame[column].dtype == "object":
            safe_frame[column] = safe_frame[column].astype("string")
    safe_frame.to_csv(csv_path, index=False)
    safe_frame.to_parquet(parquet_path, index=False)


def read_existing_table(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size <= 2:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def flush_outputs(posts: list[dict[str, object]], comments: list[dict[str, object]], attempts: list[dict[str, object]], year: int) -> None:
    posts_frame = pd.DataFrame(posts)
    comments_frame = pd.DataFrame(comments)
    attempts_frame = pd.DataFrame(attempts)
    write_table(
        posts_frame,
        Path(f"data/interim/parsed_posts/beppegrillo_{year}_posts.csv"),
        Path(f"data/interim/parsed_posts/beppegrillo_{year}_posts.parquet"),
    )
    write_table(
        comments_frame,
        Path(f"data/interim/parsed_comments/beppegrillo_{year}_comments.csv"),
        Path(f"data/interim/parsed_comments/beppegrillo_{year}_comments.parquet"),
    )
    write_table(
        attempts_frame,
        Path(f"data/interim/fetches/beppegrillo_{year}_fetch_attempts.csv"),
        Path(f"data/interim/fetches/beppegrillo_{year}_fetch_attempts.parquet"),
    )


def load_existing(
    year: int,
    retry_failed: bool = False,
    retry_post_ids: set[str] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], set[str]]:
    posts_path = Path(f"data/interim/parsed_posts/beppegrillo_{year}_posts.csv")
    comments_path = Path(f"data/interim/parsed_comments/beppegrillo_{year}_comments.csv")
    attempts_path = Path(f"data/interim/fetches/beppegrillo_{year}_fetch_attempts.csv")
    posts_frame = read_existing_table(posts_path)
    retry_post_ids = retry_post_ids or set()
    if retry_failed and not posts_frame.empty and "parser_warnings" in posts_frame.columns:
        failed_mask = posts_frame["parser_warnings"].fillna("").str.contains("no_successful_capture|collection_error", regex=True)
        posts_frame = posts_frame[~failed_mask].copy()
    if retry_post_ids and not posts_frame.empty:
        posts_frame = posts_frame[~posts_frame["post_id"].astype(str).isin(retry_post_ids)].copy()
    posts = posts_frame.to_dict("records") if not posts_frame.empty else []
    comments_frame = read_existing_table(comments_path)
    if retry_post_ids and not comments_frame.empty and "post_id" in comments_frame.columns:
        comments_frame = comments_frame[~comments_frame["post_id"].astype(str).isin(retry_post_ids)].copy()
    comments = comments_frame.to_dict("records") if not comments_frame.empty else []
    attempts_frame = read_existing_table(attempts_path)
    attempts = attempts_frame.to_dict("records") if not attempts_frame.empty else []
    done = {str(row.get("post_id")) for row in posts if row.get("post_id")}
    return posts, comments, attempts, done


def archive_gap_retry_ids(path: Path, min_gap: int, max_posts: int | None, zero_only: bool) -> set[str]:
    if not path.exists():
        return set()
    frame = pd.read_csv(path)
    if "post_id" not in frame.columns or "gap" not in frame.columns:
        return set()
    frame["gap"] = pd.to_numeric(frame["gap"], errors="coerce").fillna(0).astype(int)
    if zero_only and "parsed" in frame.columns:
        frame["parsed"] = pd.to_numeric(frame["parsed"], errors="coerce").fillna(0).astype(int)
        frame = frame[frame["parsed"] == 0]
    frame = frame[frame["gap"] >= min_gap].sort_values("gap", ascending=False)
    if max_posts:
        frame = frame.head(max_posts)
    return set(frame["post_id"].dropna().astype(str))


def write_report(posts: pd.DataFrame, comments: pd.DataFrame, attempts: pd.DataFrame, output: Path, year: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    total_posts = len(posts)
    posts_with_comments = int((posts["parsed_comment_count"].fillna(0).astype(int) > 0).sum()) if total_posts else 0
    total_comments = len(comments)
    timestamped_comments = int(comments["comment_timestamp"].fillna("").ne("").sum()) if total_comments else 0
    authored_comments = int(comments["author_raw_restricted"].fillna("").ne("").sum()) if total_comments else 0
    successful_fetches = int(attempts["http_status"].astype(str).isin(["200", "200.0"]).sum()) if len(attempts) else 0
    failed_fetches = len(attempts) - successful_fetches
    top = posts.sort_values("parsed_comment_count", ascending=False).head(20)

    lines = [
        f"# BeppeGrillo.it {year} Posts And Comments Collection Report",
        "",
        f"Last updated: {date.today().isoformat()}",
        "",
        "## Scope",
        "",
        f"This is a bounded feasibility data collection exercise for posts dated {year} on BeppeGrillo.it and comments embedded in archived post pages. It uses Wayback `id_` captures and the observed legacy comment patterns.",
        "",
        "## Summary Counts",
        "",
        f"- Unique {year} post paths attempted: {total_posts:,}",
        f"- Posts with at least one parsed embedded comment: {posts_with_comments:,}",
        f"- Parsed comments: {total_comments:,}",
        f"- Comments with raw author string: {authored_comments:,}",
        f"- Comments with parsed timestamp: {timestamped_comments:,}",
        f"- Fetch attempts: {len(attempts):,}",
        f"- Successful fetch attempts: {successful_fetches:,}",
        f"- Failed fetch attempts: {failed_fetches:,}",
        "",
        "## Top Posts By Parsed Comment Count",
        "",
        "| Rank | Comments | Date | Title | URL |",
        "|---:|---:|---|---|---|",
    ]
    for rank, (_, row) in enumerate(top.iterrows(), start=1):
        title = str(row.get("title", "")).replace("|", "\\|")
        url = str(row.get("canonical_url", ""))
        published_date = str(row.get("date_published", ""))[:10]
        count = int(row.get("parsed_comment_count", 0))
        lines.append(f"| {rank} | {count:,} | {published_date} | {title} | `{url}` |")

    lines.extend(
        [
            "",
            "## Data Organization",
            "",
            f"- Raw HTML: `data/raw/wayback/html/beppegrillo_{year}/{{month}}/`",
            f"- Parsed posts CSV/Parquet: `data/interim/parsed_posts/beppegrillo_{year}_posts.*`",
            f"- Parsed comments CSV/Parquet: `data/interim/parsed_comments/beppegrillo_{year}_comments.*`",
            f"- Fetch attempts CSV/Parquet: `data/interim/fetches/beppegrillo_{year}_fetch_attempts.*`",
            "",
            "## Comment Fields",
            "",
            "Each parsed comment includes `comment_id`, `post_id`, `author_display_hash`, `author_raw_restricted`, `comment_timestamp`, `comment_date_confidence`, `comment_order`, `parent_comment_id`, `body_text`, `body_html_path`, `links`, `parser_version`, `parse_confidence`, and `parser_warnings`.",
            "",
            "Raw author strings are retained only in the restricted interim field `author_raw_restricted`; analysis should use `author_display_hash`.",
            "",
            "## Limitations",
            "",
            "- This parser recovers comments embedded directly in legacy post HTML. It does not yet follow external pagination or AJAX-style comment loaders.",
            "- For each post path, the collector tries a small set of candidate captures and keeps the capture with the most parsed embedded comments.",
            "- Comment order is page order. For this template, comments often appear reverse-chronologically, so timestamp fields should be used for temporal ordering when parsed.",
            f"- The CDX inventory was capped; additional {year} post URLs may exist outside the current capped inventory.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2005)
    parser.add_argument("--inventory", type=Path, default=Path("data/metadata/url_inventory.parquet"))
    parser.add_argument("--max-attempts-per-post", type=int, default=3)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--sleep", type=float, default=0.25)
    parser.add_argument("--limit-posts", type=int, default=None)
    parser.add_argument("--months", nargs="*", help="Optional two-digit month filter, e.g. --months 09 10 11 12.")
    parser.add_argument("--resume", action="store_true", help="Append to existing output tables and skip completed post IDs.")
    parser.add_argument("--retry-failed", action="store_true", help="When resuming, retry posts previously marked no_successful_capture or collection_error.")
    parser.add_argument("--retry-archive-gaps", action="store_true", help="When resuming, retry posts with archive-visible counts above parsed counts.")
    parser.add_argument("--archive-gap-file", type=Path, default=None)
    parser.add_argument("--min-gap", type=int, default=100)
    parser.add_argument("--max-gap-posts", type=int, default=None)
    parser.add_argument("--retry-zero-only", action="store_true", help="Only retry archive-gap posts whose current parsed comment count is zero.")
    parser.add_argument("--checkpoint-every", type=int, default=25)
    args = parser.parse_args()

    if args.archive_gap_file is None:
        args.archive_gap_file = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_archive_vs_parsed_comments.csv")

    candidates_by_path = build_candidates(args.inventory, args.max_attempts_per_post, args.year)
    paths = sorted(candidates_by_path)
    if args.months:
        wanted_months = {str(month).zfill(2) for month in args.months}
        paths = [path for path in paths if len(path.split("/")) > 2 and path.split("/")[2] in wanted_months]
    if args.limit_posts:
        paths = paths[: args.limit_posts]

    if args.resume:
        retry_post_ids = (
            archive_gap_retry_ids(args.archive_gap_file, args.min_gap, args.max_gap_posts, args.retry_zero_only)
            if args.retry_archive_gaps
            else set()
        )
        posts, comments, attempts, done_post_ids = load_existing(
            year=args.year,
            retry_failed=args.retry_failed,
            retry_post_ids=retry_post_ids,
        )
        paths = [path for path in paths if canonical_post_id(path) not in done_post_ids]
        if retry_post_ids:
            paths = [path for path in paths if canonical_post_id(path) in retry_post_ids or canonical_post_id(path) not in done_post_ids]
    else:
        posts = []
        comments = []
        attempts = []

    print(f"Collecting {len(paths)} unique {args.year} post paths", flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(collect_one, path, candidates_by_path[path], args.timeout, args.retries, args.sleep, args.year): path
            for path in paths
        }
        for index, future in enumerate(as_completed(futures), start=1):
            path = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # pragma: no cover - audit path
                post_id = canonical_post_id(path)
                posts.append({"post_id": post_id, "canonical_url": path, "parsed_comment_count": 0, "parser_warnings": f"collection_error:{exc!r}"})
                continue
            posts.append(result["post"])
            comments.extend(result["comments"])
            attempts.extend(result["attempts"])
            if index % 25 == 0 or index == len(paths):
                print(f"Completed {index}/{len(paths)} posts; comments so far: {len(comments)}", flush=True)
            if args.checkpoint_every and (index % args.checkpoint_every == 0):
                flush_outputs(posts, comments, attempts, args.year)

    posts_frame = pd.DataFrame(posts)
    comments_frame = pd.DataFrame(comments)
    attempts_frame = pd.DataFrame(attempts)

    flush_outputs(posts, comments, attempts, args.year)
    write_report(posts_frame, comments_frame, attempts_frame, Path(f"docs/source_notes/beppegrillo_{args.year}_collection_report.md"), args.year)
    print(f"Wrote parsed {args.year} posts/comments and collection report", flush=True)


if __name__ == "__main__":
    main()
