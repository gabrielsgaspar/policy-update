"""Query Wayback CDX metadata for feasibility-pilot source groups.

This script collects archive metadata only. It does not download archived page
contents. Raw CDX responses are written as JSONL and parsed inventories are
written as CSV/Parquet for audit and later URL inventory construction.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests


CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
FIELDS = ["timestamp", "original", "statuscode", "mimetype", "digest", "length"]


@dataclass(frozen=True)
class QuerySpec:
    group: str
    domain: str
    url_pattern: str
    mimetype: str
    priority: str


QUERY_SPECS = [
    QuerySpec("beppegrillo", "www.beppegrillo.it", "www.beppegrillo.it/*", "text/html", "P0"),
    QuerySpec("beppegrillo", "beppegrillo.it", "beppegrillo.it/*", "text/html", "P0"),
    QuerySpec("blogdellestelle", "www.ilblogdellestelle.it", "www.ilblogdellestelle.it/*", "text/html", "P0"),
    QuerySpec("movimento5stelle", "www.movimento5stelle.it", "www.movimento5stelle.it/*", "text/html", "P1"),
    QuerySpec("movimento5stelle", "movimento5stelle.it", "movimento5stelle.it/*", "text/html", "P1"),
    QuerySpec("movimento5stelle", "www.movimento5stelle.eu", "www.movimento5stelle.eu/*", "text/html", "P1"),
    QuerySpec("movimento5stelle", "movimento5stelle.eu", "movimento5stelle.eu/*", "text/html", "P1"),
    QuerySpec("movimento5stelle", "portale.movimento5stelle.eu", "portale.movimento5stelle.eu/*", "text/html", "P1"),
    QuerySpec("movimento5stelle_pdf", "www.movimento5stelle.it", "www.movimento5stelle.it/*", "application/pdf", "P1"),
    QuerySpec("movimento5stelle_pdf", "movimento5stelle.it", "movimento5stelle.it/*", "application/pdf", "P1"),
    QuerySpec("movimento5stelle_pdf", "www.movimento5stelle.eu", "www.movimento5stelle.eu/*", "application/pdf", "P1"),
    QuerySpec("movimento5stelle_pdf", "movimento5stelle.eu", "movimento5stelle.eu/*", "application/pdf", "P1"),
    QuerySpec("movimento5stelle_pdf", "portale.movimento5stelle.eu", "portale.movimento5stelle.eu/*", "application/pdf", "P1"),
]


def selected_specs(groups: set[str] | None) -> list[QuerySpec]:
    if not groups:
        return QUERY_SPECS
    return [spec for spec in QUERY_SPECS if spec.group in groups]


def query_cdx(
    spec: QuerySpec,
    timeout: int,
    from_timestamp: str | None,
    to_timestamp: str | None,
    limit: int | None,
    retries: int,
) -> list[dict[str, str]]:
    params = {
        "url": spec.url_pattern,
        "output": "json",
        "fl": ",".join(FIELDS),
        "filter": [f"statuscode:200", f"mimetype:{spec.mimetype}"],
        "collapse": "digest",
        "gzip": "false",
    }
    if from_timestamp:
        params["from"] = from_timestamp
    if to_timestamp:
        params["to"] = to_timestamp
    if limit:
        params["limit"] = str(limit)

    last_error: Exception | None = None
    response: requests.Response | None = None
    for attempt in range(retries + 1):
        try:
            response = requests.get(CDX_ENDPOINT, params=params, timeout=timeout)
            response.raise_for_status()
            break
        except Exception as exc:  # pragma: no cover - network/audit path
            last_error = exc
            if attempt >= retries:
                raise
            time.sleep(5 * (attempt + 1))
    if response is None:
        raise RuntimeError(f"CDX request failed: {last_error!r}")
    payload = response.json()
    if not payload:
        return []
    header = payload[0]
    records = []
    for values in payload[1:]:
        record = dict(zip(header, values, strict=False))
        record.update(
            {
                "query_group": spec.group,
                "query_domain": spec.domain,
                "query_url_pattern": spec.url_pattern,
                "query_mimetype": spec.mimetype,
                "query_priority": spec.priority,
                "query_from": from_timestamp or "",
                "query_to": to_timestamp or "",
                "query_limit": str(limit or ""),
                "cdx_endpoint": response.url,
            }
        )
        records.append(record)
    return records


def write_jsonl(records: Iterable[dict[str, str]], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def write_summary(all_records: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "query_group",
        "query_domain",
        "query_mimetype",
        "records",
        "first_capture",
        "last_capture",
        "unique_original_urls",
        "unique_digests",
    ]
    if not all_records:
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
        return

    frame = pd.DataFrame(all_records)
    grouped = (
        frame.groupby(["query_group", "query_domain", "query_mimetype"], dropna=False)
        .agg(
            records=("timestamp", "size"),
            first_capture=("timestamp", "min"),
            last_capture=("timestamp", "max"),
            unique_original_urls=("original", "nunique"),
            unique_digests=("digest", "nunique"),
        )
        .reset_index()
        .sort_values(["query_group", "query_domain", "query_mimetype"])
    )
    grouped.to_csv(output_path, index=False)


def add_year_month(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    frame = frame.copy()
    frame["capture_year"] = frame["timestamp"].str.slice(0, 4)
    frame["capture_month"] = frame["timestamp"].str.slice(0, 6)
    return frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--groups", nargs="*", help="Optional query groups to run.")
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw/wayback/cdx"))
    parser.add_argument("--interim-dir", type=Path, default=Path("data/interim/cdx"))
    parser.add_argument("--summary", type=Path, default=Path("data/metadata/cdx_inventory_summary.csv"))
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds to sleep between requests.")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--from-timestamp", default=None, help="Inclusive Wayback timestamp lower bound, e.g. 2005.")
    parser.add_argument("--to-timestamp", default=None, help="Inclusive Wayback timestamp upper bound, e.g. 2013.")
    parser.add_argument("--limit", type=int, default=None, help="Optional per-query record limit.")
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()

    specs = selected_specs(set(args.groups) if args.groups else None)
    by_group: dict[str, list[dict[str, str]]] = {}
    all_records: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    for spec in specs:
        try:
            records = query_cdx(
                spec,
                args.timeout,
                args.from_timestamp,
                args.to_timestamp,
                args.limit,
                args.retries,
            )
            by_group.setdefault(spec.group, []).extend(records)
            all_records.extend(records)
            print(f"{spec.group} {spec.domain} {spec.mimetype}: {len(records)} records", flush=True)
        except Exception as exc:  # pragma: no cover - network/audit path
            failure = {
                "query_group": spec.group,
                "query_domain": spec.domain,
                "query_mimetype": spec.mimetype,
                "query_url_pattern": spec.url_pattern,
                "query_from": args.from_timestamp or "",
                "query_to": args.to_timestamp or "",
                "query_limit": str(args.limit or ""),
                "error": repr(exc),
            }
            failures.append(failure)
            print(f"FAILED {spec.group} {spec.domain} {spec.mimetype}: {exc}", flush=True)
        time.sleep(args.sleep)

    for group, records in by_group.items():
        write_jsonl(records, args.raw_dir / f"{group}_cdx.jsonl")
        frame = add_year_month(pd.DataFrame(records))
        args.interim_dir.mkdir(parents=True, exist_ok=True)
        frame.to_csv(args.interim_dir / f"{group}_cdx.csv", index=False)
        frame.to_parquet(args.interim_dir / f"{group}_cdx.parquet", index=False)

    if failures:
        write_jsonl(failures, args.raw_dir / "cdx_failures.jsonl")

    write_summary(all_records, args.summary)
    print(f"Wrote summary to {args.summary}")


if __name__ == "__main__":
    main()
