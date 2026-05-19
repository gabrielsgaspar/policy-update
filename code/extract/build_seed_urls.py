"""Build the approved feasibility-pilot seed URL table.

This script writes a small, hand-curated source inventory used as the starting
point for Wayback/CDX discovery and later pilot collection. It does not scrape
page contents.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class SeedUrl:
    seed_id: str
    url: str
    normalized_url: str
    domain: str
    source_group: str
    expected_content_type: str
    priority: str
    first_seen_source: str
    notes: str


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, parts.query, ""))


def domain(url: str) -> str:
    return urlsplit(url).netloc.lower()


def row(
    seed_id: str,
    url: str,
    source_group: str,
    expected_content_type: str,
    priority: str,
    first_seen_source: str,
    notes: str,
) -> SeedUrl:
    normalized = normalize_url(url)
    return SeedUrl(
        seed_id=seed_id,
        url=url,
        normalized_url=normalized,
        domain=domain(normalized),
        source_group=source_group,
        expected_content_type=expected_content_type,
        priority=priority,
        first_seen_source=first_seen_source,
        notes=notes,
    )


def build_seeds() -> list[SeedUrl]:
    seeds = [
        row("BG-LIVE-001", "https://beppegrillo.it/", "beppegrillo_live", "html", "P0", "DATA.md", "Current Beppe Grillo official site."),
        row("BG-LIVE-002", "https://beppegrillo.it/blog/", "beppegrillo_live", "html", "P0", "DATA.md", "Current blog landing page."),
        row("BG-LIVE-003", "https://beppegrillo.it/category/archivio/", "beppegrillo_live", "html", "P0", "DATA.md", "Current archive category landing page."),
        row("BG-LIVE-004", "https://beppegrillo.it/category/archivio/2005/", "beppegrillo_live", "html", "P0", "DATA.md", "Current 2005 archive entry point."),
        row("BG-HIST-001", "http://www.beppegrillo.it/", "beppegrillo_wayback", "html", "P0", "DATA.md", "Historical www/http domain variant."),
        row("BG-HIST-002", "https://www.beppegrillo.it/", "beppegrillo_wayback", "html", "P0", "DATA.md", "Historical www/https domain variant."),
        row("BG-HIST-003", "http://beppegrillo.it/", "beppegrillo_wayback", "html", "P0", "DATA.md", "Historical non-www/http domain variant."),
        row("BG-HIST-004", "https://beppegrillo.it/", "beppegrillo_wayback", "html", "P0", "DATA.md", "Historical non-www/https domain variant."),
        row("BG-HIST-005", "http://www.beppegrillo.it/archives/", "beppegrillo_wayback", "html", "P0", "DATA.md", "Legacy archive path."),
        row("BG-HIST-006", "https://www.beppegrillo.it/archives/", "beppegrillo_wayback", "html", "P0", "DATA.md", "Legacy archive path over https."),
        row("BDS-LIVE-001", "https://www.ilblogdellestelle.it/", "blogdellestelle_live", "html", "P0", "DATA.md", "Il Blog delle Stelle current site."),
        row("BDS-HIST-001", "http://www.ilblogdellestelle.it/", "blogdellestelle_wayback", "html", "P0", "DATA.md", "Historical http domain variant."),
        row("BDS-HIST-002", "https://www.ilblogdellestelle.it/2005/12/le_buone_azioni.html", "blogdellestelle_wayback", "html", "P0", "DATA.md", "Legacy-style seed URL from project notes."),
        row("M5S-LIVE-001", "https://www.movimento5stelle.it/", "m5s_live", "html", "P1", "DATA.md", "Current M5S official .it site."),
        row("M5S-LIVE-002", "https://www.movimento5stelle.eu/", "m5s_live", "html", "P1", "DATA.md", "Current/historical M5S .eu site."),
        row("M5S-LIVE-003", "https://portale.movimento5stelle.eu/", "m5s_live", "html", "P1", "DATA.md", "M5S portal."),
        row("M5S-LIVE-004", "https://portale.movimento5stelle.eu/elezioni-trasparenti", "m5s_live", "html", "P1", "DATA.md", "Candidate/election transparency portal seed."),
        row("M5S-LIVE-005", "https://www.movimento5stelle.eu/tag/programma/", "m5s_live", "html", "P1", "DATA.md", "Program-tag discovery seed."),
        row("M5S-PROG-001", "https://www1.interno.gov.it/mininterno/export/sites/default/it/assets/files/25_elezioni/6_MOVIMENTO_5_STELLE.PDF", "m5s_programs", "pdf", "P1", "DATA.md", "2013 M5S program PDF hosted by Interior Ministry."),
        row("IA-ITEM-001", "https://archive.org/details/BeppeGrillo.it2005", "internet_archive_item", "metadata/html", "P1", "DATA.md", "Internet Archive item to inspect for 2005 files and comments."),
        row("CAMERA-001", "https://dati.camera.it/", "parliament_camera", "rdf/html/api", "P1", "DATA.md", "Official Chamber open data portal."),
        row("CAMERA-002", "https://data.camera.it/", "parliament_camera", "rdf/html/api", "P1", "DATA.md", "Alternate official Chamber data domain."),
        row("SENATO-001", "https://www.senato.it/leggi-e-documenti", "parliament_senate", "html/api", "P1", "DATA.md", "Official Senate laws/documents entry point."),
        row("OPENPOLIS-001", "https://service.opdm.openpolis.io/docs/", "parliament_openpolis", "api_docs", "P1", "DATA.md", "Openpolis/OpenParlamento API documentation."),
        row("OPENPOLIS-002", "https://service.opdm.openpolis.io/api-openparlamento/v1/19/bills/", "parliament_openpolis", "json", "P1", "DATA.md", "OpenParlamento bills API example."),
        row("ELIGENDO-001", "https://elezionistorico.interno.gov.it/", "election_results", "html/csv", "P2", "DATA.md", "Interior Ministry historical election archive."),
        row("ELIGENDO-002", "https://elezionistorico.interno.gov.it/eligendo/info_opendata.php", "election_results", "html/csv", "P2", "DATA.md", "Eligendo open-data information page."),
        row("ELIGENDO-003", "https://dait.interno.gov.it/elezioni/open-data", "election_results", "html/csv", "P2", "DATA.md", "Interior Ministry election open-data page."),
        row("CAP-001", "https://www.comparativeagendas.net/project/italy", "media_public_controls", "html/csv", "P1", "DATA.md", "Italian Policy Agendas / Comparative Agendas project."),
        row("CAP-002", "https://www.comparativeagendas.net/", "media_public_controls", "html/csv", "P1", "DATA.md", "Comparative Agendas project root."),
        row("MANIFESTO-001", "https://manifesto-project.wzb.eu/", "comparison_party_controls", "html/api/corpus", "P1", "DATA.md", "Manifesto Project data and corpus root."),
        row("GDELT-001", "https://docs.gdeltcloud.com/api-reference/v2", "media_public_controls", "api_docs", "P1", "DATA.md", "GDELT Cloud API documentation."),
        row("TRENDS-001", "https://trends.google.com/", "media_public_controls", "web", "P2", "DATA.md", "Google Trends public attention proxy."),
        row("AGCOM-001", "https://www.agcom.it/osservatori", "media_public_controls", "html", "P2", "DATA.md", "AGCOM observatories seed."),
    ]
    return seeds


def write_csv(seeds: list[SeedUrl], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(seeds[0]).keys())
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(seed) for seed in seeds)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/metadata/seed_urls.csv"),
        help="Path for the seed URL CSV.",
    )
    args = parser.parse_args()
    seeds = build_seeds()
    write_csv(seeds, args.output)
    print(f"Wrote {len(seeds)} seed URLs to {args.output}")


if __name__ == "__main__":
    main()

