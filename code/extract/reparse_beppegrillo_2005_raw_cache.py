"""Reparse downloaded yearly raw HTML and keep the best capture per post.

Wayback can be intermittent during targeted retries. This script makes the
interim parsed tables stable by using all previously downloaded raw HTML listed
in the fetch-attempt log, then selecting the capture with the largest parsed
comment count for each post.
"""

from __future__ import annotations

import importlib.util
import argparse
import sys
from datetime import date
from pathlib import Path

import pandas as pd


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


def canonical_post_id(path: str) -> str:
    cleaned = path.strip("/").replace("/", "_").replace(".", "_")
    return f"beppegrillo_{cleaned}"


def write_table(frame: pd.DataFrame, csv_path: Path, parquet_path: Path) -> None:
    safe = frame.copy()
    for column in safe.columns:
        if safe[column].dtype == "object":
            safe[column] = safe[column].astype("string")
    safe.to_csv(csv_path, index=False)
    safe.to_parquet(parquet_path, index=False)


def write_report(posts: pd.DataFrame, comments: pd.DataFrame, attempts: pd.DataFrame, year: int, report_path: Path) -> None:
    total_posts = len(posts)
    posts_with_comments = int((pd.to_numeric(posts["parsed_comment_count"], errors="coerce").fillna(0) > 0).sum())
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
            "- The parser recovers comments embedded directly in archived post HTML across the 2005 legacy templates observed so far.",
            "- For each post path, the retained parsed record is the already-downloaded capture with the most parsed embedded comments.",
            "- Comment order is page order. Timestamp fields should be used for temporal ordering when parsed.",
            "- The CDX inventory was capped; additional 2005 post URLs may exist outside the current capped inventory.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2005)
    args = parser.parse_args()

    posts_csv = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_posts.csv")
    posts_parquet = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_posts.parquet")
    comments_csv = Path(f"data/interim/parsed_comments/beppegrillo_{args.year}_comments.csv")
    comments_parquet = Path(f"data/interim/parsed_comments/beppegrillo_{args.year}_comments.parquet")
    attempts_csv = Path(f"data/interim/fetches/beppegrillo_{args.year}_fetch_attempts.csv")
    report_path = Path(f"docs/source_notes/beppegrillo_{args.year}_collection_report.md")

    posts = pd.read_csv(posts_csv)
    comments = pd.read_csv(comments_csv, low_memory=False)
    attempts = pd.read_csv(attempts_csv)

    current_counts = comments.groupby("post_id").size().to_dict()
    best_by_post: dict[str, tuple[dict[str, object], list[dict[str, object]], int]] = {}
    successes = attempts[attempts["http_status"].astype(str).isin(["200", "200.0"])].copy()
    successes = successes.dropna(subset=["post_path", "raw_path"]).drop_duplicates(subset=["post_path", "raw_path"])

    for index, (_, attempt) in enumerate(successes.iterrows(), start=1):
        raw_path = Path(str(attempt["raw_path"]))
        if not raw_path.exists():
            continue
        post_id = canonical_post_id(str(attempt["post_path"]))
        try:
            post, parsed_comments = parse_post_page(raw_path.read_bytes(), post_id, str(attempt["fetch_id"]), raw_path.as_posix())
        except Exception as exc:
            print(f"parse_error {raw_path}: {exc!r}")
            continue
        post["url"] = attempt.get("url", "")
        post["canonical_url"] = attempt.get("normalized_url", "")
        post["wayback_timestamp"] = attempt.get("wayback_timestamp", "")
        post["selected_raw_path"] = raw_path.as_posix()
        post["candidate_count"] = ""
        count = len(parsed_comments)
        best = best_by_post.get(post_id)
        if best is None or count > best[2]:
            best_by_post[post_id] = (post, parsed_comments, count)
        if index % 100 == 0:
            print(f"Reparsed {index}/{len(successes)} successful raw captures")

    replace_ids = {
        post_id
        for post_id, (_, _, count) in best_by_post.items()
        if count > int(current_counts.get(post_id, 0))
    }
    existing_ids = set(posts["post_id"].astype(str))
    replace_ids.update(post_id for post_id in best_by_post if post_id not in existing_ids)
    failed_mask = posts["parser_warnings"].fillna("").str.contains("no_successful_capture|collection_error", regex=True)
    failed_ids = set(posts.loc[failed_mask, "post_id"].astype(str))
    replace_ids.update(post_id for post_id in failed_ids if post_id in best_by_post)

    if not replace_ids:
        print("No parsed records improved from raw cache")
        return

    retained_posts = posts[~posts["post_id"].astype(str).isin(replace_ids)].copy()
    retained_comments = comments[~comments["post_id"].astype(str).isin(replace_ids)].copy()
    replacement_posts = []
    replacement_comments = []
    for post_id in sorted(replace_ids):
        post, parsed_comments, _ = best_by_post[post_id]
        replacement_posts.append(post)
        replacement_comments.extend(parsed_comments)

    posts_out = pd.concat([retained_posts, pd.DataFrame(replacement_posts)], ignore_index=True, sort=False)
    comments_out = pd.concat([retained_comments, pd.DataFrame(replacement_comments)], ignore_index=True, sort=False)
    posts_out["parsed_comment_count"] = pd.to_numeric(posts_out["parsed_comment_count"], errors="coerce").fillna(0).astype(int)
    posts_out = posts_out.sort_values(["date_published", "post_id"], na_position="last").reset_index(drop=True)
    comments_out = comments_out.sort_values(["post_id", "comment_order"], na_position="last").reset_index(drop=True)

    write_table(posts_out, posts_csv, posts_parquet)
    write_table(comments_out, comments_csv, comments_parquet)
    write_report(posts_out, comments_out, attempts, args.year, report_path)
    print(f"Improved {len(replace_ids)} post records from raw cache")


if __name__ == "__main__":
    main()
