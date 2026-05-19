"""Audit parsed yearly comments against archive-visible comment counts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def canonical_post_id(path: str) -> str:
    cleaned = path.strip("/").replace("/", "_").replace(".", "_")
    return f"beppegrillo_{cleaned}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2005)
    args = parser.parse_args()

    posts_path = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_posts.csv")
    comments_path = Path(f"data/interim/parsed_comments/beppegrillo_{args.year}_comments.csv")
    archive_counts_path = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_archive_comment_counts.csv")
    out_csv = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_archive_vs_parsed_comments.csv")
    out_parquet = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_archive_vs_parsed_comments.parquet")
    summary_path = Path(f"docs/source_notes/beppegrillo_{args.year}_coverage_audit.md")

    posts = pd.read_csv(posts_path)
    comments = pd.read_csv(comments_path, low_memory=False)
    try:
        archive = pd.read_csv(archive_counts_path)
    except pd.errors.EmptyDataError:
        archive = pd.DataFrame(
            columns=[
                "post_url",
                "post_path",
                "visible_comment_count",
                "archive_month",
                "archive_wayback_timestamp",
            ]
        )

    if archive.empty:
        archive_counts = pd.DataFrame(
            columns=["post_id", "post_path", "post_url", "visible_comment_count", "archive_month", "archive_wayback_timestamp"]
        )
    else:
        archive["post_id"] = archive["post_path"].map(canonical_post_id)
        archive_counts = (
            archive.sort_values("visible_comment_count", ascending=False)
            .drop_duplicates(subset=["post_id"])
            .loc[:, ["post_id", "post_path", "post_url", "visible_comment_count", "archive_month", "archive_wayback_timestamp"]]
            .copy()
        )
    parsed_counts = (
        comments.groupby("post_id", dropna=False)
        .size()
        .rename("parsed")
        .reset_index()
    )
    post_lookup = posts.loc[:, ["post_id", "title", "date_published", "canonical_url", "parser_warnings"]].copy()
    audit = archive_counts.merge(parsed_counts, on="post_id", how="left").merge(post_lookup, on="post_id", how="left")
    if audit.empty:
        audit = pd.DataFrame(
            columns=[
                "post_id",
                "post_path",
                "post_url",
                "visible_comment_count",
                "archive_month",
                "archive_wayback_timestamp",
                "parsed",
                "title",
                "date_published",
                "canonical_url",
                "parser_warnings",
                "gap",
            ]
        )
    else:
        audit["parsed"] = audit["parsed"].fillna(0).astype(int)
        audit["visible_comment_count"] = pd.to_numeric(audit["visible_comment_count"], errors="coerce").fillna(0).astype(int)
        audit["gap"] = (audit["visible_comment_count"] - audit["parsed"]).clip(lower=0).astype(int)
    audit = audit.sort_values(["gap", "visible_comment_count"], ascending=[False, False])

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(out_csv, index=False)
    audit.to_parquet(out_parquet, index=False)

    total_posts = len(posts)
    failed_posts = int(posts["parser_warnings"].fillna("").str.contains("no_successful_capture|collection_error", regex=True).sum())
    posts_with_comments = int((pd.to_numeric(posts["parsed_comment_count"], errors="coerce").fillna(0) > 0).sum())
    total_comments = len(comments)
    authored_comments = int(comments["author_raw_restricted"].fillna("").ne("").sum())
    timestamped_comments = int(comments["comment_timestamp"].fillna("").ne("").sum())
    nonempty_comments = int(comments["body_text"].fillna("").str.strip().ne("").sum())
    positive_gap = audit[audit["gap"] > 0]
    top_posts = (
        posts.sort_values("parsed_comment_count", ascending=False)
        .loc[:, ["parsed_comment_count", "date_published", "title", "canonical_url"]]
        .head(20)
    )

    lines = [
        f"# BeppeGrillo.it {args.year} Coverage Audit",
        "",
        "## Current Counts",
        "",
        f"- Identified {args.year} post paths in current CDX-derived inventory: {total_posts:,}",
        f"- Successful parsed/retrieved post pages: {total_posts - failed_posts:,}",
        f"- Failed post pages: {failed_posts:,}",
        f"- Posts with parsed embedded comments: {posts_with_comments:,}",
        f"- Parsed comments: {total_comments:,}",
        f"- Comments with raw restricted author: {authored_comments:,}",
        f"- Comments with parsed timestamp: {timestamped_comments:,}",
        f"- Comments with nonempty text: {nonempty_comments:,}",
        "",
        "## Archive Count Cross-Check",
        "",
        f"- Archive-visible count rows: {len(audit):,}",
        f"- Archive-visible comments on those rows: {int(audit['visible_comment_count'].sum()):,}",
        f"- Parsed comments on those rows: {int(audit['parsed'].sum()):,}",
        f"- Positive archive gap sum: {int(positive_gap['gap'].sum()):,}",
        f"- Rows with any positive gap: {len(positive_gap):,}",
        f"- Rows with gap at least 100: {int((audit['gap'] >= 100).sum()):,}",
        f"- Rows with gap at least 500: {int((audit['gap'] >= 500).sum()):,}",
        "",
        "## Top Posts By Parsed Comment Count",
        "",
        "| Rank | Comments | Date | Title | URL |",
        "|---:|---:|---|---|---|",
    ]
    for rank, (_, row) in enumerate(top_posts.iterrows(), start=1):
        title = str(row["title"]).replace("|", "\\|")
        date = str(row["date_published"])[:10]
        lines.append(f"| {rank} | {int(row['parsed_comment_count']):,} | {date} | {title} | `{row['canonical_url']}` |")

    lines.extend(
        [
            "",
            "## Largest Remaining Archive Gaps",
            "",
            "| Gap | Visible | Parsed | Title | URL |",
            "|---:|---:|---:|---|---|",
        ]
    )
    for _, row in positive_gap.head(20).iterrows():
        title = str(row.get("title", "")).replace("|", "\\|")
        url = str(row.get("canonical_url") or row.get("post_url") or "")
        lines.append(f"| {int(row['gap']):,} | {int(row['visible_comment_count']):,} | {int(row['parsed']):,} | {title} | `{url}` |")

    lines.extend(
        [
            "",
            "## Notes",
            "",
        "- The audit compares parsed comments to comment counts displayed on archived monthly listing pages when those counts can be parsed. Listing counts are a useful coverage check but are themselves archived page artifacts.",
        f"- Archive-visible count rows are zero for {args.year} if the downloaded archive listings do not expose parseable `Commenti (N)` rows or if archive-listing fetches failed.",
            "- Positive gaps may reflect missing comments, different captures at different dates, source pages that are archive/listing pages rather than individual posts, or templates not yet parsed.",
            f"- Raw HTML remains in `data/raw/wayback/html/beppegrillo_{args.year}/`; parsed outputs are in `data/interim/`.",
            "",
        ]
    )
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_csv} and {summary_path}")


if __name__ == "__main__":
    main()
