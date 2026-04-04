"""
Stage 2-B + 2-C: Story Writer & Section Writer

Stage 2-B — Story Writer:
  1. Derive the key message sentence (one sentence, specific + grounded)
  2. Design the narrative arc (how each section contributes)
  3. Produce section-by-section outline                           → CP 2B

Stage 2-C — Section Writer:
  Write one section at a time in this order:
  Methods → Results → Discussion → Conclusion → Introduction → Abstract
  Each section has its own checkpoint (CP 2C-1 through CP 2C-6).

This module provides:
  - format_cp2b_outline()       format Story Writer output for CP 2B
  - section_header()            return per-section writing rules reminder
  - format_section_checkpoint() format per-section output with checkpoint block
  - assemble_manuscript()       assemble confirmed sections into full_manuscript.md
  - save_story_to_session()     persist 2-B artifacts
  - save_section_to_session()   persist one confirmed section draft
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession
    from autoresearch.workspace import WorkSpace

from autoresearch.pipeline import SECTION_ORDER, SECTION_CHECKPOINT


# ──────────────────────────────────────────────────────────────────────────────
# Stage 2-B: Story Writer
# ──────────────────────────────────────────────────────────────────────────────

KEY_MESSAGE_TEMPLATE = """\
Key message format: "[Population] (n=X), [Intervention] [direction] [Outcome]
by [magnitude] ([stat]), suggesting [mechanism/implication] [warranting/pending] [next step]."

✓ Requirements:
  - Specific: names finding, population, direction, context
  - Grounded: traceable to confirmed analysis results (Stage 1-B)
  - Connected: addresses the gap from literature synthesis (Stage 2-A)
  - Proportional: calibrated to what the data actually supports
"""

NARRATIVE_ARC_GUIDE = """\
## Narrative Arc Design

Map how each section contributes to the key message:

**Introduction:** broad context → specific gap → our approach
  (Do NOT reveal findings here)

**Methods:** design justification → key methodological choices → statistical approach
  (Reference the CP 1A confirmed plan exactly)

**Results:** primary finding first (largest effect / most central to hypothesis)
  → supporting evidence in logical order → null findings reported honestly

**Discussion:** restate key finding (1 sentence, no stats) → literature context
  (confirm / contradict / extend) → mechanistic interpretation (labelled as interpretation)
  → specific limitations (not generic) → proportional implications

**Conclusion:** key message restated + forward-looking statement (1–3 paragraphs)

**Abstract:** last — accurate synthesis, no overclaiming, 250 words default
"""

SECTION_RULES: dict[str, str] = {
    "methods": """\
**Methods writing rules:**
- Past tense throughout
- Sufficient detail for independent replication
- Statistical methods: match exactly what was confirmed at CP 1A
- Ethics/approval statement if applicable
- Do NOT include results""",

    "results": """\
**Results writing rules:**
- Past tense for findings; present tense for what figures show ("Figure 1 shows…")
- Lead with the primary finding (as established by Story Writer arc)
- Reference figures inline: (Figure 1A)
- Inline statistics: `t(48) = 2.18, p = .034, d = 0.32 [95% CI: 0.03, 0.61]`
- Do NOT interpret — mechanism/implications go in Discussion
- Report null and negative findings honestly""",

    "discussion": """\
**Discussion writing rules:**
- First sentence only: restate key finding (no statistics in sentence 1)
- Contextualize: confirm / contradict / extend prior work
- Mechanistic interpretation: label as interpretation, not established fact
- Limitations: specific to this study's design and data (not generic disclaimers)
- Implications: proportional to what the data actually shows
- Do NOT introduce new results""",

    "conclusion": """\
**Conclusion writing rules:**
- 1–3 paragraphs maximum
- No new information not already in Discussion
- Key message restated + forward-looking statement""",

    "introduction": """\
**Introduction writing rules:**
- Funnel structure: broad context → specific gap → our approach
- Present tense for established facts; past tense for prior studies
- End with clear statement of study objective (not a preview of results)
- Do NOT preview findings""",

    "abstract": """\
**Abstract writing rules:**
- Written LAST — after all other sections are confirmed
- Structure: Background / Objective / Methods / Results / Conclusion
- Must accurately reflect the paper (no overclaiming, no new information)
- Default word limit: 250 words unless journal specifies otherwise
- Include primary outcome statistics""",
}

SELF_CHECK = """\
Self-check before presenting:
- [ ] All assigned figures/tables referenced in text
- [ ] Statistics match Stage 1-A report exactly
- [ ] No references outside confirmed list (without flagging)
- [ ] Abbreviations defined on first use in this section
- [ ] No results in Methods; no interpretation in Results
- [ ] Claims proportional to effect sizes
- [ ] Terminology consistent with previously approved sections
"""


def format_cp2b_outline(
    stage1_context: str,
    literature_synthesis_snippet: str,
    key_message: str,
    narrative_arc: str,
    section_outlines: list[dict],
) -> str:
    """
    Format the full CP 2B output.

    section_outlines: list of dicts (one per section, in writing order):
        {"section": str,
         "purpose": str,
         "key_points": list[str],
         "assigned_figures": list[str],
         "transition": str,
         "flags": list[str]}
    """
    lines = [
        "## Story Writer — Stage 2-B",
        "",
        "### Stage 1 Context (confirmed)",
        "",
        stage1_context,
        "",
        "### Literature Gap (from CP 2A)",
        "",
        literature_synthesis_snippet,
        "",
        "---",
        "",
        "## Key Message",
        "",
        f"> {key_message}",
        "",
        KEY_MESSAGE_TEMPLATE,
        "",
        "---",
        "",
        "## Narrative Arc",
        "",
        NARRATIVE_ARC_GUIDE,
        "",
        narrative_arc,
        "",
        "---",
        "",
        "## Section-by-Section Outline",
        "(Writing order: Methods → Results → Discussion → Conclusion → Introduction → Abstract)",
        "",
    ]

    for outline in section_outlines:
        section = outline.get("section", "").title()
        purpose = outline.get("purpose", "")
        key_points = outline.get("key_points", [])
        figs = outline.get("assigned_figures", [])
        transition = outline.get("transition", "")
        flags = outline.get("flags", [])

        lines += [f"### {section}", "", f"**Purpose:** {purpose}", ""]
        if key_points:
            lines.append("**Key points:**")
            for pt in key_points:
                lines.append(f"  - {pt}")
            lines.append("")
        if figs:
            lines.append(f"**Assigned figures/tables:** {', '.join(figs)}")
        if transition:
            lines.append(f"**Transition:** {transition}")
        if flags:
            lines.append("\n**⚠ Flags:**")
            for flag in flags:
                lines.append(f"  - ⚠ {flag}")
        lines.append("")

    lines += [
        "---",
        "✓ **CHECKPOINT 2B** — Approve key message & narrative arc?",
        "`[OK]` to begin section writing  |  `[REVISE: ...]`  |  `[REDIRECT: ...]`",
        "",
        "> Next: Section Writer — Methods (CP 2C-1)",
    ]

    return "\n".join(lines)


def save_story_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    *,
    key_message: str = "",
    narrative_arc: str = "",
    outline_text: str = "",
) -> None:
    """Persist Stage 2-B artifacts after CP 2B is cleared."""
    if key_message:
        ws.save_key_message(key_message)
        session.key_message = key_message
    if narrative_arc:
        session.narrative_arc = narrative_arc
    if outline_text:
        ws.save_narrative_outline(outline_text)
    session.save()


# ──────────────────────────────────────────────────────────────────────────────
# Stage 2-C: Section Writer
# ──────────────────────────────────────────────────────────────────────────────

def section_context_preamble(section_name: str, session: "ARSession") -> str:
    """
    Build context block injected at the top of each section-writing prompt.
    Provides confirmed Stage 1 + 2 outputs for reference.
    """
    lines = [
        f"## Section Writer — {section_name.title()}",
        "",
        "### Confirmed context from earlier stages",
        "",
        session.stage1_context(),
        "",
    ]

    if session.key_message:
        lines += [f"**Key Message (CP 2B):** {session.key_message}", ""]
    if session.narrative_arc:
        lines += ["**Narrative Arc (CP 2B):**", session.narrative_arc, ""]

    # Show already-confirmed sections
    done_sections = [s for s in SECTION_ORDER if s in session.section_drafts]
    if done_sections:
        lines += [f"**Confirmed sections:** {', '.join(done_sections)}", ""]

    return "\n".join(lines)


def format_section_checkpoint(
    section_name: str,
    draft_text: str,
    new_claims: list[str],
    extra_references: list[str],
    flags: list[str],
    word_count: int,
) -> str:
    """
    Wrap a section draft with the standard output block.

    Appends:
      - Notes for Researcher (new claims, extra refs, flags, word count)
      - Checkpoint block
    """
    cp_id = SECTION_CHECKPOINT.get(section_name.lower(), "2C-?")
    cp_num = cp_id.split("-")[-1] if "-" in cp_id else "?"

    # Next section in order
    order = SECTION_ORDER
    try:
        idx = order.index(section_name.lower())
        next_section = order[idx + 1].title() if idx + 1 < len(order) else "Abstract (all done)"
    except ValueError:
        next_section = "next section"

    sections = [
        f"## {section_name.title()} Draft",
        "",
        draft_text,
        "",
        "---",
        "**Notes for Researcher:**",
        f"- New claims not in outline: {', '.join(new_claims) if new_claims else 'none'}",
        f"- References added beyond confirmed list: {', '.join(extra_references) if extra_references else 'none'}",
    ]

    if flags:
        sections.append("- Flags requiring attention:")
        for flag in flags:
            sections.append(f"  - ⚠ {flag}")

    sections += [
        f"- Word count: {word_count}",
        "",
        SELF_CHECK,
        "",
        "---",
        f"✓ **CHECKPOINT {cp_id}** — {section_name.title()} complete",
        f"Proceed to {next_section}?  `[OK]`  |  `[REVISE: ...]`  |  `[REDIRECT: ...]`",
    ]

    return "\n".join(sections)


def save_section_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    section_name: str,
    draft_text: str,
) -> None:
    """Persist one confirmed section draft after its checkpoint is cleared."""
    ws.save_section_draft(section_name, draft_text)
    session.section_drafts[section_name.lower()] = draft_text
    session.save()


# ──────────────────────────────────────────────────────────────────────────────
# Manuscript assembly
# ──────────────────────────────────────────────────────────────────────────────

def assemble_full_manuscript(session: "ARSession", ws: "WorkSpace") -> Path:
    """
    Assemble all confirmed section drafts into full_manuscript.md.
    Called automatically after CP 2C-6 is cleared.
    """
    return ws.assemble_manuscript(session)


def next_section_to_write(session: "ARSession") -> str | None:
    """Return the name of the next section to write, or None if all done."""
    for section in SECTION_ORDER:
        if section not in session.section_drafts:
            return section
    return None


def sections_status(session: "ARSession") -> list[tuple[str, bool]]:
    """Return list of (section_name, confirmed) for all 6 sections."""
    return [(sec, sec in session.section_drafts) for sec in SECTION_ORDER]
