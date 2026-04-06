"""
Stage 2: Background Knowledge (Literature Search & Synthesis)

Responsibilities:
  1. Take user-provided references as the core set
  2. Expand via systematic search: PubMed (NCBI E-utilities) + Google Scholar
  3. Screen for relevance, flag user-provided papers that appear off-topic
  4. Synthesize by theme (not annotated list)
  5. Output knowledge summary that grounds Stage 3 analysis choices → CP 2

This module provides:
  - search_pubmed()        query NCBI PubMed (no API key required for basic use)
  - search_scholar()       query Google Scholar via scholarly (optional install)
  - format_search_results() human-readable result list
  - build_pico_queries()   derive Boolean queries from PICO structure
  - format_cp2a_synthesis() format the CP 2A checkpoint output
  - save_literature_to_session() persist artifacts
"""

from __future__ import annotations

import json
import time
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession
    from autoresearch.workspace import WorkSpace


# ──────────────────────────────────────────────────────────────────────────────
# NCBI PubMed (E-utilities, no API key needed for ≤3 req/s)
# ──────────────────────────────────────────────────────────────────────────────

_PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
_PUBMED_EFETCH  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
_PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def _get_url(url: str, timeout: int = 15) -> str:
    """Simple URL fetch with a user-agent header."""
    req = urllib.request.Request(url, headers={"User-Agent": "AutoResearch/1.0 (mailto:research@example.com)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def search_pubmed(query: str, max_results: int = 20) -> list[dict]:
    """
    Search PubMed using the NCBI E-utilities API.

    Returns list of dicts with keys:
        pmid, title, authors, journal, year, abstract (if available), doi
    """
    try:
        # Step 1: esearch to get PMIDs
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "usehistory": "y",
        })
        search_url = f"{_PUBMED_ESEARCH}?{params}"
        search_data = json.loads(_get_url(search_url))
        pmids = search_data.get("esearchresult", {}).get("idlist", [])

        if not pmids:
            return []

        time.sleep(0.4)  # respect rate limit: ≤3 req/s without API key

        # Step 2: esummary for metadata
        params2 = urllib.parse.urlencode({
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
        })
        summary_url = f"{_PUBMED_ESUMMARY}?{params2}"
        summary_data = json.loads(_get_url(summary_url))
        result_map = summary_data.get("result", {})

        papers = []
        for pmid in pmids:
            item = result_map.get(pmid, {})
            if not item or "title" not in item:
                continue
            authors_raw = item.get("authors", [])
            authors = [a.get("name", "") for a in authors_raw[:3]]
            if len(authors_raw) > 3:
                authors.append("et al.")
            papers.append({
                "pmid": pmid,
                "title": item.get("title", "").rstrip("."),
                "authors": ", ".join(authors),
                "journal": item.get("fulljournalname", item.get("source", "")),
                "year": item.get("pubdate", "")[:4],
                "doi": item.get("elocationid", "").replace("doi: ", ""),
                "abstract": "",  # filled below if needed
            })

        return papers

    except Exception as e:
        return [{"error": str(e), "query": query}]


def fetch_pubmed_abstracts(pmids: list[str]) -> dict[str, str]:
    """
    Fetch abstracts for a list of PMIDs via efetch.
    Returns dict: pmid → abstract text.
    """
    if not pmids:
        return {}
    try:
        time.sleep(0.4)
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "id": ",".join(pmids),
            "rettype": "abstract",
            "retmode": "xml",
        })
        xml_text = _get_url(f"{_PUBMED_EFETCH}?{params}")
        root = ET.fromstring(xml_text)
        abstracts: dict[str, str] = {}
        for article in root.iter("PubmedArticle"):
            pmid_el = article.find(".//PMID")
            abstract_el = article.find(".//AbstractText")
            if pmid_el is not None and abstract_el is not None:
                abstracts[pmid_el.text or ""] = abstract_el.text or ""
        return abstracts
    except Exception:
        return {}


def search_scholar(query: str, max_results: int = 10) -> list[dict]:
    """
    Search Google Scholar via the `scholarly` package (optional dependency).
    Falls back gracefully if not installed.
    """
    try:
        from scholarly import scholarly as _scholarly
    except ImportError:
        return [{"error": "scholarly not installed — run: pip install scholarly", "query": query}]

    results = []
    try:
        search_gen = _scholarly.search_pubs(query)
        for _ in range(max_results):
            try:
                pub = next(search_gen)
                bib = pub.get("bib", {})
                results.append({
                    "title": bib.get("title", ""),
                    "authors": ", ".join(bib.get("author", [])[:3]),
                    "journal": bib.get("venue", ""),
                    "year": str(bib.get("pub_year", "")),
                    "abstract": bib.get("abstract", ""),
                    "doi": pub.get("eprint_url", ""),
                    "citations": pub.get("num_citations", 0),
                    "source": "scholar",
                })
            except StopIteration:
                break
            time.sleep(1.0)  # Scholar rate-limit
    except Exception as e:
        results.append({"error": str(e), "query": query})

    return results


# ──────────────────────────────────────────────────────────────────────────────
# PICO query builder
# ──────────────────────────────────────────────────────────────────────────────

def build_pico_queries(
    population: str,
    intervention: str,
    comparison: str = "",
    outcome: str = "",
    synonyms: dict[str, list[str]] | None = None,
) -> list[str]:
    """
    Build Boolean PubMed search strings from PICO components.

    synonyms: {"population": ["alt1", "alt2"], "intervention": [...], ...}
    Returns 2-3 queries of increasing specificity.
    """
    syn = synonyms or {}

    def expand(base: str, key: str) -> str:
        terms = [base] + syn.get(key, [])
        return "(" + " OR ".join(f'"{t}"' for t in terms) + ")"

    p_str = expand(population, "population")
    i_str = expand(intervention, "intervention")
    c_str = expand(comparison, "comparison") if comparison else ""
    o_str = expand(outcome, "outcome") if outcome else ""

    queries = []
    # Most specific
    parts = [p_str, i_str]
    if c_str:
        parts.append(c_str)
    if o_str:
        parts.append(o_str)
    queries.append(" AND ".join(parts))

    # Drop comparison
    if c_str:
        queries.append(f"{p_str} AND {i_str} AND {o_str}" if o_str else f"{p_str} AND {i_str}")

    # Broadest: population + outcome only
    if o_str:
        queries.append(f"{p_str} AND {o_str}")

    return queries


# ──────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ──────────────────────────────────────────────────────────────────────────────

def format_search_results(results: list[dict], source: str = "PubMed") -> str:
    """Format a list of search-result dicts as readable Markdown."""
    if not results:
        return f"No results from {source}."

    lines = [f"### {source} results ({len(results)} papers)\n"]
    for i, r in enumerate(results, 1):
        if "error" in r:
            lines.append(f"{i}. **Error:** {r['error']}")
            continue
        pmid = r.get("pmid", "")
        pmid_str = f"PMID:{pmid}" if pmid else ""
        doi = r.get("doi", "")
        id_str = " | ".join(filter(None, [pmid_str, doi]))
        lines += [
            f"{i}. **{r.get('title', 'No title')}**",
            f"   {r.get('authors', '')} ({r.get('year', '')}). *{r.get('journal', '')}*. {id_str}",
        ]
        if r.get("abstract"):
            snippet = r["abstract"][:200].rstrip() + "…"
            lines.append(f"   > {snippet}")
        lines.append("")

    return "\n".join(lines)


def build_search_log(
    queries: list[str],
    databases: list[str],
    total_identified: int,
    total_screened: int,
    total_included: int,
    user_provided: int,
    search_date: str,
) -> str:
    """Build a PRISMA-style search documentation block."""
    return textwrap.dedent(f"""\
        ## Search Summary

        **Databases:** {', '.join(databases)}

        **Search strings:**
        {chr(10).join(f'  - `{q}`' for q in queries)}

        **Results:**
        - Identified: {total_identified}
        - After title/abstract screening: {total_screened}
        - Included in synthesis: {total_included}
        - User-provided papers: {user_provided} (reviewed separately)

        **Date range:** No restriction (last search: {search_date})
    """)


# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint 2A: synthesis formatting
# ──────────────────────────────────────────────────────────────────────────────

def format_cp2_synthesis(
    search_log: str,
    core_themes: list[dict],
    contradictions: str,
    gap_statement: str,
    how_current_study_addresses_gap: str,
    reference_list: str,
    flagged_user_papers: list[str] | None = None,
) -> str:
    """
    Format the full CP 2A output.

    core_themes: list of dicts:
        {"theme": str, "summary": str, "key_papers": list[str], "relevance": str}
    """
    lines = [
        "## Background Knowledge Synthesis — Stage 2",
        "",
        search_log,
        "",
        "---",
        "",
        "## Core Background Themes",
        "",
    ]

    for i, theme in enumerate(core_themes, 1):
        lines += [
            f"### Theme {i}: {theme.get('theme', '')}",
            "",
            theme.get("summary", ""),
            "",
        ]
        if theme.get("key_papers"):
            lines.append(f"Key papers: {', '.join(theme['key_papers'])}")
        if theme.get("relevance"):
            lines.append(f"Relevance to current study: {theme['relevance']}")
        lines.append("")

    lines += [
        "## Contradictions & Unresolved Debates",
        "",
        contradictions,
        "",
        "## Gap Statement",
        "",
        gap_statement,
        "",
        "## How the Current Study Addresses This Gap",
        "",
        how_current_study_addresses_gap,
        "",
        "## Reference List",
        "",
        reference_list,
    ]

    if flagged_user_papers:
        lines += [
            "",
            "## ⚠ Flagged User-Provided Papers (low relevance — please review)",
            "",
        ]
        for flag in flagged_user_papers:
            lines.append(f"- {flag}")

    lines += [
        "",
        "---",
        "✓ **CHECKPOINT 2** — Confirm background knowledge & key papers?",
        "`[OK]` to proceed to Stage 3 (Data Analysis)  |  `[ADD: paper/topic]`  |  `[REMOVE: ...]`  |  `[REDIRECT: ...]`",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Session integration
# ──────────────────────────────────────────────────────────────────────────────

def format_cp2a_synthesis(*args, **kwargs) -> str:
    """Legacy alias for format_cp2_synthesis."""
    return format_cp2_synthesis(*args, **kwargs)


def save_literature_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    *,
    search_log_text: str = "",
    bib_content: str = "",
    synthesis_text: str = "",
) -> None:
    """Persist Stage 2 artifacts after CP 2 is cleared."""
    if search_log_text:
        ws.save_search_log(search_log_text)
    if bib_content:
        ws.save_references_bib(bib_content)
    if synthesis_text:
        ws.save_literature_synthesis(synthesis_text)
        session.literature_synthesis = synthesis_text
    session.save()
