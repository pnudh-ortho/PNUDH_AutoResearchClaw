"""
Stage 3: Parallel Review + Auto-Synthesis

Three reviewers run independently and simultaneously on the completed draft.
Each evaluates only their designated domain; they do not communicate.

  Reviewer A — Methodology & Statistical Rigor
  Reviewer B — Clinical Relevance & Translational Value
  Reviewer C — Scientific Writing & Logical Flow

After all three reviews exist, auto-synthesis:
  1. Aggregates comments by manuscript section
  2. Surfaces conflicts between reviewers
  3. Prioritizes: Major > Minor > Optional
  4. Produces unified revision checklist               → CP 3

This module provides:
  - run_all_reviews()       run all three reviewers sequentially (or collect existing)
  - parse_review_sections() extract Major/Minor/Optional/Strengths from raw review text
  - synthesize_reviews()    combine three parsed reviews into a unified checklist
  - format_cp3_synthesis()  format the CP 3 output for the researcher
  - save_reviews_to_session() persist all review artifacts
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession
    from autoresearch.workspace import WorkSpace


# ──────────────────────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ReviewComment:
    """One comment from a reviewer."""
    reviewer: str              # "A", "B", or "C"
    severity: str              # "major", "minor", "optional", "strength"
    title: str
    location: str              # section / figure / table
    problem: str
    suggestion: str


@dataclass
class ParsedReview:
    reviewer: str
    recommendation: str        # "Accept" / "Minor revision" / etc.
    rationale: str
    major: list[ReviewComment] = field(default_factory=list)
    minor: list[ReviewComment] = field(default_factory=list)
    optional: list[ReviewComment] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    raw_text: str = ""


# ──────────────────────────────────────────────────────────────────────────────
# Review parsing
# ──────────────────────────────────────────────────────────────────────────────

MAX_STRENGTHS_IN_REPORT = 10  # cap strengths list for readability

_SEVERITY_PATTERNS = {
    "major":    re.compile(r"###\s*Major\s+Concerns?", re.IGNORECASE),
    "minor":    re.compile(r"###\s*Minor\s+Concerns?", re.IGNORECASE),
    "optional": re.compile(r"###\s*Optional|###\s*Suggestion", re.IGNORECASE),
    "strength": re.compile(r"###\s*Strength", re.IGNORECASE),
}

_RECOMMENDATION_PATTERN = re.compile(
    r"###\s*Summary\s+Recommendation.*?\n+(.*?)\n",
    re.IGNORECASE | re.DOTALL,
)

_ITEM_PATTERN = re.compile(
    r"(\d+)\.\s+\*?\*?([^\n]+)\*?\*?\s*\n"          # numbered title
    r"(?:\s+Location:\s+([^\n]+)\n)?"                # optional location
    r"(?:\s+Problem:\s+([^\n]+(?:\n(?!\s+\w+:)[^\n]+)*))?",  # optional problem (multiline)
    re.MULTILINE,
)


def parse_review(reviewer_id: str, text: str) -> ParsedReview:
    """
    Parse structured review output into a ParsedReview.
    Handles the standard format produced by reviewer-a/b/c skills.
    """
    review = ParsedReview(reviewer=reviewer_id, recommendation="", rationale="", raw_text=text)

    # Extract recommendation
    rec_match = _RECOMMENDATION_PATTERN.search(text)
    if rec_match:
        first_line = rec_match.group(1).strip().splitlines()[0].strip("- *")
        review.recommendation = first_line

    # Split into sections by severity
    sections = re.split(r"(?=###\s)", text)
    current_severity: str | None = None

    for section in sections:
        if not section.strip():
            continue

        for sev_name, pattern in _SEVERITY_PATTERNS.items():
            if pattern.match(section):
                current_severity = sev_name
                break
        else:
            if "rationale" in section.lower() and rec_match:
                rationale_lines = section.strip().splitlines()[1:]
                review.rationale = " ".join(l.strip() for l in rationale_lines if l.strip())
            continue

        if current_severity == "strength":
            bullet_lines = re.findall(r"[-*]\s+(.+)", section)
            review.strengths.extend(bullet_lines)
            continue

        # Parse numbered items in this severity section
        for m in _ITEM_PATTERN.finditer(section):
            comment = ReviewComment(
                reviewer=reviewer_id,
                severity=current_severity or "minor",
                title=m.group(2).strip() if m.group(2) else "",
                location=m.group(3).strip() if m.group(3) else "",
                problem=m.group(4).strip() if m.group(4) else "",
                suggestion="",  # will be filled from "Suggestion:" line
            )
            # Try to extract Suggestion
            sug_match = re.search(
                rf"{re.escape(m.group(2) or '')}" + r".*?Suggestion:\s*([^\n]+)",
                section, re.IGNORECASE | re.DOTALL
            )
            if sug_match:
                comment.suggestion = sug_match.group(1).strip()
            getattr(review, current_severity).append(comment)

    return review


# ──────────────────────────────────────────────────────────────────────────────
# Review synthesis
# ──────────────────────────────────────────────────────────────────────────────

def synthesize_reviews(
    review_a: ParsedReview,
    review_b: ParsedReview,
    review_c: ParsedReview,
) -> dict:
    """
    Combine three parsed reviews into a unified synthesis dict.

    Returns:
        {
          "checklist": [{"id": str, "severity": str, "reviewer": str,
                          "title": str, "location": str, "problem": str, "suggestion": str}],
          "conflicts": [str],
          "strengths": [str],
          "recommendations": {"A": str, "B": str, "C": str},
          "overall_recommendation": str,
        }
    """
    checklist = []
    item_id = 1

    for severity in ("major", "minor", "optional"):
        for review in (review_a, review_b, review_c):
            for comment in getattr(review, severity):
                checklist.append({
                    "id": f"R{review.reviewer}-{item_id:02d}",
                    "severity": severity.upper(),
                    "reviewer": f"Reviewer {review.reviewer}",
                    "title": comment.title,
                    "location": comment.location,
                    "problem": comment.problem,
                    "suggestion": comment.suggestion,
                    "addressed": False,
                })
                item_id += 1

    # Detect conflicts: same section, opposite severity or contradictory advice
    conflicts: list[str] = []
    # Simple heuristic: look for same location with opposing language
    location_comments: dict[str, list[dict]] = {}
    for item in checklist:
        loc = item["location"].lower()
        location_comments.setdefault(loc, []).append(item)

    for loc, items in location_comments.items():
        if len(items) >= 2:
            reviewers = [i["reviewer"] for i in items]
            if len(set(reviewers)) >= 2:
                # Check for "too much" vs "not enough" contradiction
                texts = [i["problem"].lower() for i in items]
                if any("too much" in t or "too long" in t or "excessive" in t for t in texts) and \
                   any("not enough" in t or "too short" in t or "insufficient" in t for t in texts):
                    conflicts.append(
                        f"Conflict at [{loc}]: "
                        + " vs ".join(f"{i['reviewer']}: {i['title']}" for i in items[:2])
                    )

    # Aggregate strengths
    all_strengths = review_a.strengths + review_b.strengths + review_c.strengths

    # Overall recommendation (most conservative)
    priority_order = ["Reject", "Major revision", "Minor revision", "Accept"]
    recs = [review_a.recommendation, review_b.recommendation, review_c.recommendation]
    overall = "Unknown"
    for rec in priority_order:
        if any(rec.lower() in r.lower() for r in recs if r):
            overall = rec
            break

    return {
        "checklist": checklist,
        "conflicts": conflicts,
        "strengths": all_strengths,
        "recommendations": {
            "A": review_a.recommendation,
            "B": review_b.recommendation,
            "C": review_c.recommendation,
        },
        "overall_recommendation": overall,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint 3: synthesis formatting
# ──────────────────────────────────────────────────────────────────────────────

def format_cp3_synthesis(synthesis: dict) -> str:
    """
    Format the unified review synthesis for CP 3.
    The researcher sees this instead of three raw review documents.
    """
    checklist = synthesis["checklist"]
    conflicts = synthesis["conflicts"]
    strengths = synthesis["strengths"]
    recs = synthesis["recommendations"]
    overall = synthesis["overall_recommendation"]

    major = [i for i in checklist if i["severity"] == "MAJOR"]
    minor = [i for i in checklist if i["severity"] == "MINOR"]
    optional = [i for i in checklist if i["severity"] == "OPTIONAL"]

    lines = [
        "## Review Synthesis — Stage 3",
        "",
        "Three independent reviewers have evaluated the manuscript.",
        "This synthesis aggregates their findings; you do NOT need to read the raw reviews.",
        "",
        "### Reviewer Recommendations",
        f"- Reviewer A (Methodology): **{recs.get('A', 'N/A')}**",
        f"- Reviewer B (Clinical): **{recs.get('B', 'N/A')}**",
        f"- Reviewer C (Writing): **{recs.get('C', 'N/A')}**",
        f"- **Overall (most conservative): {overall}**",
        "",
    ]

    if conflicts:
        lines += ["### ⚠ Reviewer Conflicts (require researcher decision)", ""]
        for c in conflicts:
            lines.append(f"- {c}")
        lines.append("")

    # Major concerns
    lines += ["---", "", f"### Major Concerns ({len(major)}) — MUST address before submission", ""]
    if major:
        for item in major:
            lines += [
                f"**{item['id']}** — {item['title']}",
                f"  - Source: {item['reviewer']} | Location: {item['location']}",
                f"  - Problem: {item['problem']}",
                f"  - Suggestion: {item['suggestion']}" if item['suggestion'] else "",
                "",
            ]
    else:
        lines += ["No major concerns. ✓", ""]

    # Minor concerns
    lines += ["---", "", f"### Minor Concerns ({len(minor)}) — should address", ""]
    if minor:
        for item in minor:
            lines += [
                f"**{item['id']}** — {item['title']}",
                f"  - Source: {item['reviewer']} | Location: {item['location']}",
                f"  - Problem: {item['problem']}",
                f"  - Suggestion: {item['suggestion']}" if item['suggestion'] else "",
                "",
            ]
    else:
        lines += ["No minor concerns. ✓", ""]

    # Optional
    lines += ["---", "", f"### Optional Improvements ({len(optional)})", ""]
    if optional:
        for item in optional:
            lines += [
                f"**{item['id']}** — {item['title']} ({item['reviewer']})",
                f"  {item['problem']}",
                "",
            ]

    # Strengths
    if strengths:
        lines += ["---", "", "### Strengths Noted by Reviewers", ""]
        for s in strengths[:MAX_STRENGTHS_IN_REPORT]:
            lines.append(f"- {s}")
        lines.append("")

    lines += [
        "---",
        "✓ **CHECKPOINT 3** — Revision scope decided?",
        "",
        "For each item, decide:",
        "  `[ADDRESS: R{ID}]` — will fix this",
        "  `[DECLINE: R{ID} — reason]` — will not fix; provide rebuttal rationale",
        "  `[OPTIONAL: R{ID}]` — will address if time allows",
        "",
        "When scope is decided: `[OK: scope confirmed]` → Revision Agent begins.",
    ]

    return "\n".join(l for l in lines)


def build_revision_checklist(synthesis: dict, researcher_decisions: dict) -> str:
    """
    Build the revision_checklist.md from synthesis + researcher decisions at CP 3.

    researcher_decisions: {"R{ID}": "address" | "decline: reason" | "optional"}
    """
    lines = [
        "# Revision Checklist",
        "",
        "| ID | Severity | Title | Location | Decision | Notes |",
        "|---|---|---|---|---|---|",
    ]

    for item in synthesis["checklist"]:
        iid = item["id"]
        decision_raw = researcher_decisions.get(iid, "address" if item["severity"] == "MAJOR" else "pending")
        if decision_raw.startswith("decline:"):
            decision = "DECLINE"
            note = decision_raw[8:].strip()
        elif decision_raw == "optional":
            decision = "OPTIONAL"
            note = ""
        else:
            decision = "ADDRESS"
            note = ""

        lines.append(
            f"| {iid} | {item['severity']} | {item['title']} | "
            f"{item['location']} | {decision} | {note} |"
        )

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Session integration
# ──────────────────────────────────────────────────────────────────────────────

def save_reviews_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    *,
    review_a_text: str = "",
    review_b_text: str = "",
    review_c_text: str = "",
    synthesis_text: str = "",
) -> None:
    """Persist Stage 3 review artifacts."""
    if review_a_text:
        ws.save_review("a", review_a_text)
        session.review_a = review_a_text
    if review_b_text:
        ws.save_review("b", review_b_text)
        session.review_b = review_b_text
    if review_c_text:
        ws.save_review("c", review_c_text)
        session.review_c = review_c_text
    if synthesis_text:
        ws.save_review_synthesis(synthesis_text)
        session.review_synthesis = synthesis_text
    session.save()


def auto_synthesize_if_ready(session: "ARSession", ws: "WorkSpace") -> str | None:
    """
    If all three reviews exist in the workspace, auto-run synthesis.
    Returns the formatted synthesis text if generated, or None.
    """
    if not ws.all_reviews_present():
        return None

    review_a_text = ws.read_review("a") or session.review_a
    review_b_text = ws.read_review("b") or session.review_b
    review_c_text = ws.read_review("c") or session.review_c

    if not (review_a_text and review_b_text and review_c_text):
        return None

    parsed_a = parse_review("A", review_a_text)
    parsed_b = parse_review("B", review_b_text)
    parsed_c = parse_review("C", review_c_text)

    synthesis_dict = synthesize_reviews(parsed_a, parsed_b, parsed_c)
    synthesis_text = format_cp3_synthesis(synthesis_dict)

    save_reviews_to_session(session, ws, synthesis_text=synthesis_text)
    return synthesis_text
