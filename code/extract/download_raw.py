"""Rate-limited raw downloader for live and Wayback URLs.

The downloader stores raw bytes by content hash and writes fetch metadata. It
does not parse, clean, or overwrite raw files. Use it only after the PI-approved
pilot sample has been selected.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd
import requests


USER_AGENT = "policy-update-feasibility-pilot/0.1 (+research; contact PI)"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def source_slug(url: str) -> str:
    domain = urlsplit(url).netloc.lower().replace(":", "_")
    return domain or "unknown"


def year_month_from_timestamp(timestamp: str | float | int | None) -> tuple[str, str]:
    value = "" if pd.isna(timestamp) else str(timestamp)
    if len(value) >= 6 and value[:6].isdigit():
        return value[:4], value[4:6]
    return "unknown", "unknown"


def raw_path_for(
    root: Path,
    source: str,
    content_hash: str,
    extension: str,
    wayback_timestamp: str | None,
) -> Path:
    year, month = year_month_from_timestamp(wayback_timestamp)
    if wayback_timestamp:
        return root / "wayback" / "html" / source / year / month / f"{wayback_timestamp}_{content_hash}{extension}"
    return root / "live" / source / year / month / f"{content_hash}{extension}"


def extension_from_mimetype(mimetype: str | None, url: str) -> str:
    path_suffix = Path(urlsplit(url).path).suffix.lower()
    if path_suffix in {".html", ".htm", ".pdf", ".json", ".xml", ".txt"}:
        return path_suffix
    mt = (mimetype or "").split(";")[0].strip().lower()
    if mt == "application/pdf":
        return ".pdf"
    if mt in {"application/json", "text/json"}:
        return ".json"
    if mt in {"text/xml", "application/xml"}:
        return ".xml"
    if mt.startswith("text/") or mt == "text/html":
        return ".html"
    return ".bin"


def wayback_url(timestamp: str, original_url: str) -> str:
    return f"https://web.archive.org/web/{timestamp}id_/{original_url}"


def fetch_once(url: str, timeout: int) -> requests.Response:
    return requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})


def download_row(
    row: pd.Series,
    raw_root: Path,
    timeout: int,
    retries: int,
    sleep_seconds: float,
) -> dict[str, object]:
    original_url = str(row.get("url") or row.get("original") or row.get("normalized_url"))
    normalized_url = str(row.get("normalized_url") or original_url)
    wayback_timestamp = str(row.get("wayback_timestamp") or "")
    wayback_timestamp = "" if wayback_timestamp.lower() in {"nan", "none"} else wayback_timestamp
    fetch_method = "wayback_id" if wayback_timestamp else "live"
    fetch_url = wayback_url(wayback_timestamp, original_url) if wayback_timestamp else original_url
    source = source_slug(normalized_url)

    retrieved_at = datetime.now(timezone.utc).isoformat()
    response: requests.Response | None = None
    error_message = ""
    retry_count = 0

    for attempt in range(retries + 1):
        retry_count = attempt
        try:
            response = fetch_once(fetch_url, timeout)
            if response.status_code >= 500 and attempt < retries:
                time.sleep(sleep_seconds * (attempt + 1))
                continue
            break
        except Exception as exc:  # pragma: no cover - network/audit path
            error_message = repr(exc)
            if attempt < retries:
                time.sleep(sleep_seconds * (attempt + 1))

    if response is None:
        return {
            "fetch_id": str(uuid.uuid4()),
            "source_id": str(row.get("query_group") or source),
            "url": original_url,
            "normalized_url": normalized_url,
            "canonical_url": "",
            "wayback_timestamp": wayback_timestamp,
            "retrieved_at": retrieved_at,
            "http_status": "",
            "mimetype": "",
            "content_hash": "",
            "raw_path": "",
            "cdx_digest": str(row.get("cdx_digest") or ""),
            "cdx_length": str(row.get("cdx_length") or ""),
            "fetch_method": fetch_method,
            "retry_count": retry_count,
            "error_message": error_message or "No response",
        }

    mimetype = response.headers.get("Content-Type", "")
    content_hash = sha256_bytes(response.content)
    extension = extension_from_mimetype(mimetype, original_url)
    raw_path = raw_path_for(raw_root, source, content_hash, extension, wayback_timestamp or None)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if not raw_path.exists():
        raw_path.write_bytes(response.content)

    if response.status_code >= 400:
        error_message = f"HTTP {response.status_code}"

    return {
        "fetch_id": str(uuid.uuid4()),
        "source_id": str(row.get("query_group") or source),
        "url": original_url,
        "normalized_url": normalized_url,
        "canonical_url": "",
        "wayback_timestamp": wayback_timestamp,
        "retrieved_at": retrieved_at,
        "http_status": response.status_code,
        "mimetype": mimetype,
        "content_hash": content_hash,
        "raw_path": raw_path.as_posix(),
        "cdx_digest": str(row.get("cdx_digest") or ""),
        "cdx_length": str(row.get("cdx_length") or ""),
        "fetch_method": fetch_method,
        "retry_count": retry_count,
        "error_message": error_message,
    }


def read_input(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def write_metadata(records: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return
    fieldnames = list(records[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="CSV/Parquet sample with url/normalized_url/wayback_timestamp fields.")
    parser.add_argument("--output", type=Path, default=Path("data/interim/fetches/fetches.csv"))
    parser.add_argument("--raw-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=2.0)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()

    frame = read_input(args.input)
    if args.limit is not None:
        frame = frame.head(args.limit)

    records: list[dict[str, object]] = []
    for _, row in frame.iterrows():
        records.append(download_row(row, args.raw_root, args.timeout, args.retries, args.sleep))
        time.sleep(args.sleep)

    write_metadata(records, args.output)
    print(f"Wrote {len(records)} fetch metadata rows to {args.output}")


if __name__ == "__main__":
    main()

