"""Inspect Internet Archive item metadata for the feasibility pilot."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import requests


def suffix_for(name: str) -> str:
    path = Path(name)
    return path.suffix.lower() or "(none)"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--identifier", default="BeppeGrillo.it2005")
    parser.add_argument("--output", type=Path, default=Path("docs/source_notes/internet_archive_beppegrillo_2005.md"))
    parser.add_argument("--raw-output", type=Path, default=Path("data/raw/third_party/internet_archive/BeppeGrillo.it2005_metadata.json"))
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    url = f"https://archive.org/metadata/{args.identifier}"
    response = requests.get(url, timeout=args.timeout)
    response.raise_for_status()
    metadata = response.json()

    args.raw_output.parent.mkdir(parents=True, exist_ok=True)
    args.raw_output.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    files = metadata.get("files", [])
    suffix_counts = Counter(suffix_for(item.get("name", "")) for item in files)
    formats = Counter(item.get("format", "(missing)") for item in files)
    names = [item.get("name", "") for item in files]
    comment_like = [name for name in names if "comment" in name.lower() or "commenti" in name.lower()]
    html_like = [name for name in names if suffix_for(name) in {".html", ".htm", ".xhtml"}]
    archive_like = [name for name in names if suffix_for(name) in {".zip", ".tar", ".gz", ".warc", ".arc"}]

    title = metadata.get("metadata", {}).get("title", args.identifier)
    description = metadata.get("metadata", {}).get("description", "")
    publicdate = metadata.get("metadata", {}).get("publicdate", "TBD")
    licenseurl = metadata.get("metadata", {}).get("licenseurl", "TBD")

    lines = [
        "# Internet Archive Source Note: BeppeGrillo.it2005",
        "",
        "Last updated: 2026-05-14",
        "",
        "## Source",
        "",
        f"- Identifier: `{args.identifier}`",
        f"- Metadata URL: `{url}`",
        f"- Title: {title}",
        f"- Public date: {publicdate}",
        f"- License URL: {licenseurl}",
        f"- Raw metadata saved to: `{args.raw_output.as_posix()}`",
        "",
        "## Metadata Summary",
        "",
        f"- File count: {len(files)}",
        f"- HTML-like file count: {len(html_like)}",
        f"- Archive-like file count: {len(archive_like)}",
        f"- Comment-name file count: {len(comment_like)}",
        "",
        "## File Suffix Counts",
        "",
    ]
    for suffix, count in sorted(suffix_counts.items()):
        lines.append(f"- `{suffix}`: {count}")
    lines.extend(["", "## Format Counts", ""])
    for fmt, count in sorted(formats.items()):
        lines.append(f"- `{fmt}`: {count}")

    lines.extend(["", "## Initial Comment Recoverability Assessment", ""])
    if comment_like:
        lines.append("Filenames containing `comment` or `commenti` were found. Inspect these files before treating the item as post-only.")
        lines.append("")
        for name in comment_like[:25]:
            lines.append(f"- `{name}`")
    else:
        lines.append("No filenames explicitly containing `comment` or `commenti` were found in item metadata. This does not rule out comments embedded inside HTML or bundled archives.")

    lines.extend(
        [
            "",
            "## Parseability Assessment",
            "",
            "TBD after inspecting the listed HTML/archive files. The next check should determine whether files contain complete post pages, comment sections, pagination, stable dates, and original URL structure.",
            "",
            "## Access / License Notes",
            "",
            "TBD. Metadata was retrieved for inspection only. Any downloading or reuse of bundled files should record item-level rights metadata and Internet Archive access constraints.",
            "",
            "## Description Snippet",
            "",
            str(description)[:1000] if description else "TBD",
            "",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote source note to {args.output}")


if __name__ == "__main__":
    main()

