"""Parser for legacy BeppeGrillo.it post pages.

The 2005-era template stores comments as:

    <div id="c194270">...</div>
    <p class="posted">Postato da: Name il 20.10.05 17:56</p>

This parser keeps raw author strings in a restricted field and provides a
salted hash for analysis use.
"""

from __future__ import annotations

import hashlib
import os
import re
from hashlib import sha1
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Comment, Tag


PARSER_VERSION = "parser_beppegrillo_legacy_v0.3"
COMMENT_ID_RE = re.compile(r"^c\d+$")
COMMENT_THREADED_ID_RE = re.compile(r"^comment-(?P<parent>\d+)-(?P<comment>\d+)-(?P<depth>\d+)$")
COMMENT_VOTE_ID_RE = re.compile(r"comment(?P<comment>\d+)")
COMMENT_META_RE = re.compile(
    r"^Postato\s+da:\s*(?P<author>.*?)\s+il\s+"
    r"(?P<date>\d{1,2}\.\d{1,2}\.\d{2,4})"
    r"(?:\s+(?P<time>\d{1,2}:\d{2}))?",
    flags=re.IGNORECASE,
)
COMMENT_META_ALT_RE = re.compile(
    r"^(?P<author>.*?)\s+"
    r"(?P<date>\d{1,2}\.\d{1,2}\.\d{2,4})"
    r"(?:\s+(?P<time>\d{1,2}:\d{2}))?",
    flags=re.IGNORECASE,
)
POST_META_RE = re.compile(
    r"Postato\s+da\s*(?P<author>.*?)\s+il\s+"
    r"(?P<date>\d{1,2}\.\d{1,2}\.\d{2,4})"
    r"(?:\s+(?P<time>\d{1,2}:\d{2}))?",
    flags=re.IGNORECASE,
)
ARCHIVE_COMMENT_COUNT_RE = re.compile(r"Commenti\s*\((?P<count>\d+)\)", flags=re.IGNORECASE)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def parse_italian_short_datetime(date_value: str, time_value: str | None = None) -> tuple[str, str]:
    day, month, year = [part.strip() for part in date_value.split(".")]
    if len(year) == 2:
        year_i = int(year)
        year = f"20{year_i:02d}" if year_i < 40 else f"19{year_i:02d}"
    time_value = time_value or "00:00"
    try:
        parsed = datetime.strptime(f"{day.zfill(2)}.{month.zfill(2)}.{year} {time_value}", "%d.%m.%Y %H:%M")
        confidence = "exact_timestamp" if time_value != "00:00" else "date_only"
        return parsed.isoformat(sep=" "), confidence
    except ValueError:
        return "", "unparsed"


def parse_iso_date(value: str) -> tuple[str, str]:
    try:
        parsed = datetime.strptime(value.strip(), "%Y-%m-%d")
        return parsed.isoformat(sep=" "), "date_only"
    except ValueError:
        return "", "unparsed"


def hash_author(author: str, salt: str | None = None) -> str:
    author_norm = clean_text(author).casefold()
    if not author_norm:
        return ""
    salt = salt if salt is not None else os.environ.get("COMMENT_HASH_SALT", "policy-update-feasibility-pilot")
    return hashlib.sha256(f"{salt}|{author_norm}".encode("utf-8")).hexdigest()


def soup_from_bytes(content: bytes) -> BeautifulSoup:
    return BeautifulSoup(content, "html.parser", from_encoding="iso-8859-1")


def post_title(soup: BeautifulSoup) -> str:
    comment_heading = None
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if clean_text(heading.get_text(" ", strip=True)).casefold() == "commenti":
            comment_heading = heading
            break
    if comment_heading:
        previous_h3 = comment_heading.find_previous("h3")
        if previous_h3:
            return clean_text(previous_h3.get_text(" ", strip=True))
    title = soup.find("title")
    return clean_text(title.get_text(" ", strip=True)) if title else ""


def first_posted_meta(soup: BeautifulSoup) -> Tag | None:
    for posted in soup.find_all("p", class_="posted"):
        text = clean_text(posted.get_text(" ", strip=True))
        if text.startswith("Postato da ") and not text.startswith("Postato da:"):
            return posted
    return None


def parse_post_meta(soup: BeautifulSoup) -> dict[str, Any]:
    posted = first_posted_meta(soup)
    title = post_title(soup)
    author = ""
    timestamp = ""
    date_confidence = ""
    category = ""
    if posted:
        text = clean_text(posted.get_text(" ", strip=True))
        match = POST_META_RE.search(text)
        if match:
            author = clean_text(match.group("author"))
            timestamp, date_confidence = parse_italian_short_datetime(match.group("date"), match.group("time"))
        links = posted.find_all("a")
        if links:
            category = clean_text(links[-1].get_text(" ", strip=True))
    if not timestamp:
        date_meta = soup.find("meta", attrs={"name": "date"})
        if date_meta and date_meta.get("content"):
            timestamp, date_confidence = parse_iso_date(str(date_meta.get("content")))
    body_text = ""
    if posted:
        chunks: list[str] = []
        cursor = posted.find_previous_sibling()
        while cursor:
            if isinstance(cursor, Tag) and cursor.name == "h3":
                break
            if isinstance(cursor, Tag):
                chunks.append(clean_text(cursor.get_text(" ", strip=True)))
            cursor = cursor.find_previous_sibling()
        body_text = "\n".join(reversed([chunk for chunk in chunks if chunk]))
    return {
        "title": title,
        "author": author,
        "date_published": timestamp,
        "date_confidence": date_confidence,
        "body_text": body_text,
        "category": category,
    }


def parse_comment_meta(text: str) -> tuple[str, str, str]:
    match = COMMENT_META_RE.match(clean_text(text))
    if not match:
        match = COMMENT_META_ALT_RE.match(clean_text(text))
    if not match:
        return "", "", "unparsed"
    timestamp, confidence = parse_italian_short_datetime(match.group("date"), match.group("time"))
    return clean_text(match.group("author")), timestamp, confidence


def parse_sotto_commenti_blocks(html: str, post_id: str, fetch_id: str, raw_path: str, start_order: int = 1) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    pattern = re.compile(
        r"<!--\s*inizio sotto commenti\s*-->(?P<body>.*?)<!--\s*fine sotto commenti\s*-->",
        flags=re.IGNORECASE | re.DOTALL,
    )
    for offset, match in enumerate(pattern.finditer(html), start=start_order):
        block_html = match.group("body")
        block = BeautifulSoup(block_html, "html.parser")
        posted_candidates = block.find_all("p", class_="posted")
        posted = posted_candidates[-1] if posted_candidates else None
        author = ""
        timestamp = ""
        confidence = "missing"
        links = []
        if posted:
            bold = posted.find("b")
            posted_text = clean_text(posted.get_text(" ", strip=True))
            author, timestamp, confidence = parse_comment_meta(posted_text)
            if bold and not author:
                author = clean_text(bold.get_text(" ", strip=True))
                date_match = re.search(r"(\d{1,2}\.\d{1,2}\.\d{2,4})(?:\s+(\d{1,2}:\d{2}))?", posted_text)
                if date_match:
                    timestamp, confidence = parse_italian_short_datetime(date_match.group(1), date_match.group(2))
            for link in posted.find_all("a", href=True):
                links.append(link.get("href", ""))
            posted.extract()
        body_text = clean_text(block.get_text("\n", strip=True))
        if not body_text and not author:
            continue
        source_hash = sha1(f"{post_id}|{offset}|{author}|{timestamp}|{body_text[:200]}".encode("utf-8")).hexdigest()[:16]
        comments.append(
            {
                "comment_id": f"{post_id}_sotto_{source_hash}",
                "comment_source_id": source_hash,
                "post_id": post_id,
                "fetch_id": fetch_id,
                "author_display_hash": hash_author(author),
                "author_raw_restricted": author,
                "comment_timestamp": timestamp,
                "comment_date_confidence": confidence,
                "comment_order": offset,
                "parent_comment_id": "",
                "body_text": body_text,
                "body_html_path": raw_path,
                "links": "|".join(links),
                "language": "it",
                "spam_score": "",
                "duplicate_score": "",
                "moderation_marker": "",
                "template_type": "legacy_2005_sotto_commenti",
                "parser_version": PARSER_VERSION,
                "parse_confidence": 0.90 if body_text and author and timestamp else 0.65,
                "parser_warnings": "" if posted else "missing_comment_posted_metadata",
                "restricted_raw_flag": True if author else False,
                "notes": "",
            }
        )
    return comments


def parse_comments(soup: BeautifulSoup, post_id: str, fetch_id: str, raw_path: str) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    for order, div in enumerate(soup.find_all(id=COMMENT_ID_RE), start=1):
        comment_source_id = str(div.get("id") or "")
        body_text = clean_text(div.get_text("\n", strip=True))
        posted = div.find_next_sibling("p", class_="posted")
        author = ""
        timestamp = ""
        confidence = "missing"
        if posted:
            author, timestamp, confidence = parse_comment_meta(posted.get_text(" ", strip=True))
        links = []
        for link in div.find_all("a", href=True):
            links.append(link.get("href", ""))
        comments.append(
            {
                "comment_id": f"{post_id}_{comment_source_id}" if comment_source_id else f"{post_id}_comment_{order}",
                "comment_source_id": comment_source_id,
                "post_id": post_id,
                "fetch_id": fetch_id,
                "author_display_hash": hash_author(author),
                "author_raw_restricted": author,
                "comment_timestamp": timestamp,
                "comment_date_confidence": confidence,
                "comment_order": order,
                "parent_comment_id": "",
                "body_text": body_text,
                "body_html_path": raw_path,
                "links": "|".join(links),
                "language": "it",
                "spam_score": "",
                "duplicate_score": "",
                "moderation_marker": "",
                "template_type": "legacy_2005_embedded_comments",
                "parser_version": PARSER_VERSION,
                "parse_confidence": 0.95 if body_text and posted else 0.60,
                "parser_warnings": "" if posted else "missing_comment_posted_metadata",
                "restricted_raw_flag": True if author else False,
                "notes": "",
            }
        )
    return comments


def parse_threaded_comments(soup: BeautifulSoup, post_id: str, fetch_id: str, raw_path: str, start_order: int = 1) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    order = start_order - 1
    for div in soup.find_all(id=COMMENT_THREADED_ID_RE):
        comment_source_id = str(div.get("id") or "")
        match = COMMENT_THREADED_ID_RE.match(comment_source_id)
        if not match:
            continue
        order += 1
        source_comment = match.group("comment")
        source_parent = match.group("parent")
        posted = div.find("p", class_="posted", recursive=False)
        author = ""
        timestamp = ""
        confidence = "missing"
        if posted:
            author, timestamp, confidence = parse_comment_meta(posted.get_text(" ", strip=True))
            if not author:
                bold = posted.find("b")
                author = clean_text(bold.get_text(" ", strip=True)) if bold else ""
                date_match = re.search(r"(\d{1,2}\.\d{1,2}\.\d{2,4})(?:\s+(\d{1,2}:\d{2}))?", posted.get_text(" ", strip=True))
                if date_match:
                    timestamp, confidence = parse_italian_short_datetime(date_match.group(1), date_match.group(2))

        chunks: list[str] = []
        links: list[str] = []
        for child in div.children:
            if isinstance(child, Tag) and child.name == "p" and "posted" in (child.get("class") or []):
                break
            if isinstance(child, Tag):
                chunks.append(clean_text(child.get_text("\n", strip=True)))
                for link in child.find_all("a", href=True):
                    links.append(link.get("href", ""))
            elif isinstance(child, str):
                chunks.append(clean_text(child))
        body_text = "\n".join(chunk for chunk in chunks if chunk)

        comments.append(
            {
                "comment_id": f"{post_id}_comment_{source_comment}",
                "comment_source_id": comment_source_id,
                "post_id": post_id,
                "fetch_id": fetch_id,
                "author_display_hash": hash_author(author),
                "author_raw_restricted": author,
                "comment_timestamp": timestamp,
                "comment_date_confidence": confidence,
                "comment_order": order,
                "parent_comment_id": "" if source_parent == "0" else f"{post_id}_comment_{source_parent}",
                "body_text": body_text,
                "body_html_path": raw_path,
                "links": "|".join(links),
                "language": "it",
                "spam_score": "",
                "duplicate_score": "",
                "moderation_marker": "",
                "template_type": "legacy_2006_threaded_comments",
                "parser_version": PARSER_VERSION,
                "parse_confidence": 0.93 if body_text and author and timestamp else 0.65,
                "parser_warnings": "" if posted else "missing_comment_posted_metadata",
                "restricted_raw_flag": True if author else False,
                "notes": "",
            }
        )
    return comments


def parse_comment_posted_div(posted: Tag) -> tuple[str, str, str, str]:
    author = ""
    bold = posted.find("b")
    if bold:
        author = clean_text(bold.get_text(" ", strip=True))
    text = clean_text(posted.get_text(" ", strip=True))
    date_match = re.search(r"(\d{1,2}\.\d{1,2}\.\d{2,4})(?:\s+(\d{1,2}:\d{2}))?", text)
    timestamp = ""
    confidence = "missing"
    if date_match:
        timestamp, confidence = parse_italian_short_datetime(date_match.group(1), date_match.group(2))
    source_id = ""
    for tag in posted.find_all(True):
        for attr in ("id", "onclick", "href"):
            value = tag.get(attr)
            if not value:
                continue
            match = COMMENT_VOTE_ID_RE.search(str(value))
            if match:
                source_id = match.group("comment")
                break
        if source_id:
            break
    return author, timestamp, confidence, source_id


def parse_comments_to_sort(soup: BeautifulSoup, post_id: str, fetch_id: str, raw_path: str, start_order: int = 1) -> list[dict[str, Any]]:
    container = soup.find(id="commentsToSort")
    if not isinstance(container, Tag):
        return []
    comments: list[dict[str, Any]] = []
    buffer: list[str] = []
    order = start_order - 1
    for child in container.children:
        if isinstance(child, Tag) and "comment-posted" in (child.get("class") or []):
            block_html = "".join(buffer)
            buffer = []
            block = BeautifulSoup(block_html, "html.parser")
            for node in block.find_all(string=lambda value: isinstance(value, Comment)):
                node.extract()
            body_text = clean_text(block.get_text("\n", strip=True))
            body_text = clean_text(re.sub(r"\bchiusura\s+div\s+commenti\b", " ", body_text, flags=re.IGNORECASE))
            author, timestamp, confidence, source_comment = parse_comment_posted_div(child)
            if not body_text and not author:
                continue
            order += 1
            links = [link.get("href", "") for link in block.find_all("a", href=True)]
            if not source_comment:
                source_comment = sha1(f"{post_id}|{order}|{author}|{timestamp}|{body_text[:200]}".encode("utf-8")).hexdigest()[:16]
            comments.append(
                {
                    "comment_id": f"{post_id}_comment_{source_comment}",
                    "comment_source_id": source_comment,
                    "post_id": post_id,
                    "fetch_id": fetch_id,
                    "author_display_hash": hash_author(author),
                    "author_raw_restricted": author,
                    "comment_timestamp": timestamp,
                    "comment_date_confidence": confidence,
                    "comment_order": order,
                    "parent_comment_id": "",
                    "body_text": body_text,
                    "body_html_path": raw_path,
                    "links": "|".join(links),
                    "language": "it",
                    "spam_score": "",
                    "duplicate_score": "",
                    "moderation_marker": "",
                    "template_type": "legacy_2008_comments_to_sort",
                    "parser_version": PARSER_VERSION,
                    "parse_confidence": 0.92 if body_text and author and timestamp else 0.65,
                    "parser_warnings": "" if author and timestamp else "missing_comment_posted_metadata",
                    "restricted_raw_flag": True if author else False,
                    "notes": "",
                }
            )
        else:
            buffer.append(str(child))
    return comments


def parse_post_page(content: bytes, post_id: str, fetch_id: str, raw_path: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    soup = soup_from_bytes(content)
    meta = parse_post_meta(soup)
    comments = parse_comments(soup, post_id, fetch_id, raw_path)
    threaded_comments = parse_threaded_comments(soup, post_id, fetch_id, raw_path, start_order=len(comments) + 1)
    if threaded_comments:
        existing_ids = {comment["comment_id"] for comment in comments}
        comments.extend(comment for comment in threaded_comments if comment["comment_id"] not in existing_ids)
    if not comments:
        comments = parse_comments_to_sort(soup, post_id, fetch_id, raw_path)
    if not comments:
        html = content.decode("iso-8859-1", errors="ignore")
        comments = parse_sotto_commenti_blocks(html, post_id, fetch_id, raw_path)
    warnings = []
    if not meta["title"]:
        warnings.append("missing_title")
    if not meta["date_published"]:
        warnings.append("missing_or_unparsed_post_date")
    if not comments:
        warnings.append("no_embedded_comments_found")
    post = {
        "post_id": post_id,
        "fetch_id": fetch_id,
        "title": meta["title"],
        "author": meta["author"],
        "date_published": meta["date_published"],
        "date_modified": "",
        "date_confidence": meta["date_confidence"],
        "body_text": meta["body_text"],
        "body_html_path": raw_path,
        "category": meta["category"],
        "tags": "",
        "visible_comment_count": "",
        "parsed_comment_count": len(comments),
        "language": "it",
        "template_type": comments[0]["template_type"] if comments else "legacy_2005_embedded_comments",
        "parser_version": PARSER_VERSION,
        "parse_confidence": 0.90 if meta["title"] and meta["date_published"] else 0.65,
        "parser_warnings": "|".join(warnings),
        "notes": "",
    }
    return post, comments


def parse_archive_comment_counts(content: bytes, base_url: str) -> list[dict[str, Any]]:
    soup = soup_from_bytes(content)
    rows: list[dict[str, Any]] = []
    for posted in soup.find_all("p", class_="posted"):
        text = clean_text(posted.get_text(" ", strip=True))
        count_match = ARCHIVE_COMMENT_COUNT_RE.search(text)
        if not count_match:
            continue
        post_link = None
        comment_link = None
        for link in posted.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".html") and not post_link:
                post_link = href
            if "#comments" in href:
                comment_link = href
        if not post_link and comment_link:
            post_link = comment_link.split("#", 1)[0]
        if not post_link:
            continue
        rows.append(
            {
                "post_url": urljoin(base_url, post_link),
                "post_path": urlsplit(urljoin(base_url, post_link)).path,
                "visible_comment_count": int(count_match.group("count")),
                "archive_posted_text": text,
            }
        )
    return rows


def read_raw(path: Path) -> bytes:
    return path.read_bytes()
