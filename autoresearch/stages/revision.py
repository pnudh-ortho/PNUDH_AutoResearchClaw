"""
Stage 4-A: Revision Agent

Executes confirmed checklist items ONLY.
Every change is logged (what, where, why, cascade effects).
Items the researcher chose not to address are logged with rebuttal rationale.
No unrequested changes.

This module provides:
  - parse_revision_checklist()   read checklist and classify items by decision
  - apply_text_change()          minimal in-text substitution utility
  - build_change_log_table()     format a Markdown change log
  - format_revision_output()     wrap revised manuscript + change log
  - save_revision_to_session()   persist artifacts
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
class ChecklistItem:
    item_id: str            # e.g. "RA-01"
    severity: str           # MAJOR / MINOR / OPTIONAL
    title: str
    location: str
    problem: str
    suggestion: str
    decision: str           # "ADDRESS" / "DECLINE" / "OPTIONAL"
    rebuttal: str = ""      # filled if decision == "DECLINE"


@dataclass
class ChangeRecord:
    num: int
    item_id: str
    title: str
    location: str
    change_made: str
    cascade_effects: str = "None"


# ──────────────────────────────────────────────────────────────────────────────
# Checklist parsing
# ──────────────────────────────────────────────────────────────────────────────

def parse_revision_checklist(checklist_text: str) -> list[ChecklistItem]:
    """
    Parse a revision_checklist.md produced by build_revision_checklist().

    Table format:
    | ID | Severity | Title | Location | Decision | Notes |
    """
    items: list[ChecklistItem] = []
    for line in checklist_text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| ID") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        item_id, severity, title, location, decision = cells[:5]
        rebuttal = cells[5] if len(cells) > 5 else ""
        items.append(ChecklistItem(
            item_id=item_id,
            severity=severity,
            title=title,
            location=location,
            problem="",
            suggestion="",
            decision=decision.upper().strip(),
            rebuttal=rebuttal,
        ))
    return items


def items_to_address(checklist: list[ChecklistItem]) -> list[ChecklistItem]:
    return [i for i in checklist if i.decision in ("ADDRESS", "OPTIONAL")]


def items_declined(checklist: list[ChecklistItem]) -> list[ChecklistItem]:
    return [i for i in checklist if i.decision == "DECLINE"]


# ──────────────────────────────────────────────────────────────────────────────
# Text revision utilities
# ──────────────────────────────────────────────────────────────────────────────

def apply_text_substitution(
    text: str,
    old_phrase: str,
    new_phrase: str,
    *,
    count: int = 1,
) -> tuple[str, int]:
    """
    Replace old_phrase with new_phrase in text.
    Returns (new_text, n_replacements).
    Uses case-sensitive exact match.
    """
    n = text.count(old_phrase)
    if n == 0:
        return text, 0
    replacements = min(count, n)
    new_text = text.replace(old_phrase, new_phrase, replacements)
    return new_text, replacements


def apply_regex_substitution(
    text: str,
    pattern: str,
    replacement: str,
    flags: int = 0,
) -> tuple[str, int]:
    """
    Replace using a regex pattern.
    Returns (new_text, n_replacements).
    """
    new_text, n = re.subn(pattern, replacement, text, flags=flags)
    return new_text, n


# ──────────────────────────────────────────────────────────────────────────────
# Change log
# ──────────────────────────────────────────────────────────────────────────────

def build_change_log_table(records: list[ChangeRecord]) -> str:
    lines = [
        "## Change Log",
        "",
        "| # | Item ID | Title | Location | Change made | Cascade effects |",
        "|---|---|---|---|---|---|",
    ]
    for r in records:
        lines.append(
            f"| {r.num} | {r.item_id} | {r.title} | "
            f"{r.location} | {r.change_made} | {r.cascade_effects} |"
        )
    return "\n".join(lines)


def build_declined_table(items: list[ChecklistItem]) -> str:
    if not items:
        return ""
    lines = [
        "",
        "## Items Not Addressed (Researcher Decision)",
        "",
        "| # | Item ID | Title | Rebuttal rationale |",
        "|---|---|---|---|",
    ]
    for i, item in enumerate(items, 1):
        lines.append(f"| {i} | {item.item_id} | {item.title} | {item.rebuttal} |")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Revision output formatter
# ──────────────────────────────────────────────────────────────────────────────

def format_revision_output(
    revised_manuscript: str,
    change_records: list[ChangeRecord],
    declined_items: list[ChecklistItem],
    additional_flags: list[str] | None = None,
) -> str:
    """
    Wrap the revised manuscript with the standard change log block.
    """
    lines = [
        "## Revised Manuscript",
        "",
        revised_manuscript,
        "",
        "---",
        "",
        build_change_log_table(change_records),
    ]

    if declined_items:
        lines.append(build_declined_table(declined_items))

    if additional_flags:
        lines += ["", "## Additional Flags (noticed but not in checklist)", ""]
        for flag in additional_flags:
            lines.append(f"- ⚠ {flag}")

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Session integration
# ──────────────────────────────────────────────────────────────────────────────

def save_revision_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    *,
    revised_manuscript: str = "",
    change_records: list[ChangeRecord] | None = None,
    declined_items: list[ChecklistItem] | None = None,
) -> None:
    """Persist Stage 4-A artifacts."""
    if revised_manuscript:
        ws.save_revised_manuscript(revised_manuscript)

    if change_records:
        for record in change_records:
            session.change_log.append({
                "num": record.num,
                "item_id": record.item_id,
                "title": record.title,
                "location": record.location,
                "change_made": record.change_made,
                "cascade_effects": record.cascade_effects,
            })
            ws.append_change_log_row({
                "num": record.num,
                "item": f"{record.item_id}: {record.title}",
                "location": record.location,
                "change": record.change_made,
                "cascade": record.cascade_effects,
            })

    if declined_items:
        for item in declined_items:
            session.items_not_addressed.append({
                "item_id": item.item_id,
                "title": item.title,
                "rebuttal": item.rebuttal,
            })

    session.save()
