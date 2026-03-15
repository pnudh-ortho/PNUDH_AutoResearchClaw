"""arXiv API client.

Uses stdlib ``urllib`` + ``xml.etree`` — zero extra dependencies.

Public API
----------
- ``search_arxiv(query, limit)`` → ``list[Paper]``

Rate limit: arXiv requests 3-second gaps between calls.  Retries up to
3 times with exponential back-off on transient failures.
"""

from __future__ import annotations

import logging
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from researchclaw.literature.models import Author, Paper

logger = logging.getLogger(__name__)

_BASE_URL = "https://export.arxiv.org/api/query"
_MAX_RESULTS = 50
_RATE_LIMIT_SEC = 3.1  # arXiv asks for ≥3 s between requests
_MAX_RETRIES = 3
_MAX_WAIT_SEC = 60
_TIMEOUT_SEC = 30

# Atom XML namespaces
_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def search_arxiv(
    query: str,
    *,
    limit: int = 20,
) -> list[Paper]:
    """Search arXiv for papers matching *query*.

    Parameters
    ----------
    query:
        Free-text search query (mapped to ``all:`` arXiv field).
    limit:
        Maximum number of results (capped at 50).

    Returns
    -------
    list[Paper]
        Parsed papers.  Empty list on network failure.
    """
    limit = min(limit, _MAX_RESULTS)
    params = {
        "search_query": f"all:{query}",
        "start": "0",
        "max_results": str(limit),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{_BASE_URL}?{urllib.parse.urlencode(params)}"

    xml_text = _fetch_with_retry(url)
    if xml_text is None:
        return []

    return _parse_atom_feed(xml_text)


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _fetch_with_retry(url: str) -> str | None:
    """GET *url* returning raw text, with retries."""
    for attempt in range(_MAX_RETRIES):
        try:
            req = urllib.request.Request(
                url, headers={"Accept": "application/atom+xml"}
            )
            with urllib.request.urlopen(req, timeout=_TIMEOUT_SEC) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, OSError) as exc:
            wait = min(_RATE_LIMIT_SEC * (2**attempt), _MAX_WAIT_SEC)
            jitter = random.uniform(0, wait * 0.2)
            logger.warning(
                "arXiv request failed (%s). Retry %d/%d in %.0fs …",
                exc,
                attempt + 1,
                _MAX_RETRIES,
                wait,
            )
            time.sleep(wait + jitter)
    logger.error("arXiv request exhausted retries for: %s", url)
    return None


def _parse_atom_feed(xml_text: str) -> list[Paper]:
    """Parse arXiv Atom XML feed into ``Paper`` objects."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        logger.error("Failed to parse arXiv Atom XML")
        return []

    papers: list[Paper] = []
    for entry in root.findall("atom:entry", _NS):
        try:
            papers.append(_parse_entry(entry))
        except Exception:  # noqa: BLE001
            logger.debug("Failed to parse arXiv entry")
    return papers


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return (element.text or "").strip()


def _parse_entry(entry: ET.Element) -> Paper:
    """Convert a single Atom <entry> to a ``Paper``."""
    title = re.sub(r"\s+", " ", _text(entry.find("atom:title", _NS)))
    abstract = re.sub(r"\s+", " ", _text(entry.find("atom:summary", _NS)))

    # Authors
    authors = tuple(
        Author(name=_text(a.find("atom:name", _NS)))
        for a in entry.findall("atom:author", _NS)
    )

    # arXiv ID from the <id> element (e.g. "http://arxiv.org/abs/2301.00001v2")
    raw_id = _text(entry.find("atom:id", _NS))
    arxiv_id = ""
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?$", raw_id)
    if m:
        arxiv_id = m.group(1)

    # Year from <published>
    published = _text(entry.find("atom:published", _NS))
    year = 0
    if published:
        ym = re.match(r"(\d{4})", published)
        if ym:
            year = int(ym.group(1))

    # DOI (may be absent)
    doi_el = entry.find("arxiv:doi", _NS)
    doi = _text(doi_el) if doi_el is not None else ""

    # Primary category
    primary = entry.find("arxiv:primary_category", _NS)
    venue = ""
    if primary is not None:
        venue = primary.get("term", "")

    # URL — prefer abs link
    url = ""
    for link in entry.findall("atom:link", _NS):
        if link.get("type") == "text/html":
            url = link.get("href", "")
            break
    if not url:
        url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else raw_id

    return Paper(
        paper_id=f"arxiv-{arxiv_id}" if arxiv_id else f"arxiv-{raw_id}",
        title=title,
        authors=authors,
        year=year,
        abstract=abstract,
        venue=venue,
        citation_count=0,  # arXiv doesn't provide citation counts
        doi=doi,
        arxiv_id=arxiv_id,
        url=url,
        source="arxiv",
    )
