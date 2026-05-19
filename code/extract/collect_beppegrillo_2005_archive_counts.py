"""Collect yearly monthly archive visible comment counts.

Monthly archive pages often list post links with `Commenti (N)`. This script
downloads the earliest available archive capture for each month in a requested year and uses
those counts as a recovery audit against parsed embedded comments.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
import time
import uuid
from datetime import datetime, timezone
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
parse_archive_comment_counts = PARSER_MODULE.parse_archive_comment_counts


USER_AGENT = "policy-update-beppegrillo-year-archive-counts/0.1 (+research)"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def wayback_url(timestamp: str, original_url: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original_url}"


def select_monthly_archive_captures(inventory_path: Path, year: int) -> pd.DataFrame:
    inv = pd.read_parquet(inventory_path)
    arch = inv[
        (inv["query_group"] == "beppegrillo")
        & (inv["source_type"] == "archive_listing_candidate")
        & (inv["candidate_year"].astype(str) == str(year))
    ].copy()
    arch = arch[arch["domain"].astype(str).eq("www.beppegrillo.it")].copy()
    arch["timestamp"] = arch["wayback_timestamp"].astype(str)
    arch["timestamp_year"] = arch["timestamp"].str.slice(0, 4).astype(int)
    old = arch[arch["timestamp_year"].between(year, year + 2, inclusive="both")].copy()
    if old.empty:
        old = arch
    old = old.sort_values(["candidate_month", "timestamp"])
    return old.groupby("candidate_month", as_index=False).head(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2005)
    parser.add_argument("--inventory", type=Path, default=Path("data/metadata/url_inventory.parquet"))
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()

    captures = select_monthly_archive_captures(args.inventory, args.year)
    rows = []
    fetches = []
    for _, capture in captures.iterrows():
        original_url = str(capture["url"])
        timestamp = str(capture["wayback_timestamp"])
        url = wayback_url(timestamp, original_url)
        retrieved_at = datetime.now(timezone.utc).isoformat()
        fetch_id = str(uuid.uuid4())
        try:
            response = requests.get(url, timeout=(10, args.timeout), headers={"User-Agent": USER_AGENT})
            content = response.content
            content_hash = sha256_bytes(content)
            raw_path = (
                Path(f"data/raw/wayback/html/beppegrillo_{args.year}_archive")
                / str(capture["candidate_month"]).zfill(2)
                / f"{timestamp}_{content_hash}.html"
            )
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            if not raw_path.exists():
                raw_path.write_bytes(content)
            if response.status_code == 200:
                parsed_rows = parse_archive_comment_counts(content, original_url)
                for row in parsed_rows:
                    row.update(
                        {
                            "archive_fetch_id": fetch_id,
                            "archive_month": str(capture["candidate_month"]).zfill(2),
                            "archive_wayback_timestamp": timestamp,
                            "archive_raw_path": raw_path.as_posix(),
                        }
                    )
                    rows.append(row)
            error_message = "" if response.status_code < 400 else f"HTTP {response.status_code}"
            http_status = response.status_code
            mimetype = response.headers.get("Content-Type", "")
        except Exception as exc:  # pragma: no cover - network/audit path
            content_hash = ""
            raw_path = Path("")
            error_message = repr(exc)
            http_status = ""
            mimetype = ""
        fetches.append(
            {
                "fetch_id": fetch_id,
                "url": original_url,
                "wayback_timestamp": timestamp,
                "retrieved_at": retrieved_at,
                "http_status": http_status,
                "mimetype": mimetype,
                "content_hash": content_hash,
                "raw_path": raw_path.as_posix() if raw_path.as_posix() != "." else "",
                "error_message": error_message,
            }
        )
        time.sleep(args.sleep)

    count_columns = [
        "post_url",
        "post_path",
        "visible_comment_count",
        "archive_posted_text",
        "archive_fetch_id",
        "archive_month",
        "archive_wayback_timestamp",
        "archive_raw_path",
    ]
    counts = pd.DataFrame(rows, columns=count_columns)
    fetch_frame = pd.DataFrame(fetches)
    out_csv = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_archive_comment_counts.csv")
    out_parquet = Path(f"data/interim/parsed_posts/beppegrillo_{args.year}_archive_comment_counts.parquet")
    fetch_csv = Path(f"data/interim/fetches/beppegrillo_{args.year}_archive_fetches.csv")
    fetch_parquet = Path(f"data/interim/fetches/beppegrillo_{args.year}_archive_fetches.parquet")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fetch_csv.parent.mkdir(parents=True, exist_ok=True)
    for frame, csv_path, parquet_path in [
        (counts, out_csv, out_parquet),
        (fetch_frame, fetch_csv, fetch_parquet),
    ]:
        safe_frame = frame.copy()
        for column in safe_frame.columns:
            if safe_frame[column].dtype == "object":
                safe_frame[column] = safe_frame[column].astype("string")
        safe_frame.to_csv(csv_path, index=False)
        safe_frame.to_parquet(parquet_path, index=False)
    print(f"Wrote {len(counts)} archive comment-count rows")


if __name__ == "__main__":
    main()
