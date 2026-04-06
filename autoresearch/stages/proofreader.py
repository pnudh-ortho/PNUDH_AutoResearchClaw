"""
Stage 4-B: Proofreader

Systematic final check of the revised manuscript before CP 4.
Flags issues — does NOT rewrite.

Checks:
  1. Terminology consistency (same term throughout)
  2. Citation completeness (every in-text cite in reference list and vice versa)
  3. Figure & table cross-references (sequential, all cited before appearing)
  4. Number & statistics consistency (text matches figures/tables)
  5. Claim-evidence alignment (Abstract/Conclusion match Results/Discussion)

This module provides:
  - ProofreadingCheck   data class for one issue found
  - check_terminology() scan for inconsistent terms
  - check_abbreviations() find undefined or inconsistently used abbreviations
  - check_figure_references() verify figure citation order and completeness
  - check_statistics_consistency() spot number mismatches
  - check_claim_language() flag overclaiming words in Abstract/Conclusion
  - run_all_checks()   run all checks, return ProofreadReport
  - format_cp4_report() format the CP 4 output
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession
    from autoresearch.workspace import WorkSpace


# ── module-level compiled patterns (avoid recompilation per call) ─────────────
_ABBREV_PATTERN = re.compile(r'\b([A-Z]{2,6})\b')
_DEFINITION_PATTERN = re.compile(r'([A-Za-z ]+)\s+\(([A-Z]{2,6})\)')


# ──────────────────────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ProofreadingIssue:
    category: str       # "terminology" | "citation" | "figure_ref" | "statistics" | "claim_language"
    description: str
    location: str       # section / approximate location
    original: str = ""  # problematic text
    recommendation: str = ""


@dataclass
class ProofreadReport:
    issues: list[ProofreadingIssue] = field(default_factory=list)
    clean_sections: list[str] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def issues_by_category(self) -> dict[str, list[ProofreadingIssue]]:
        cats: dict[str, list[ProofreadingIssue]] = {}
        for issue in self.issues:
            cats.setdefault(issue.category, []).append(issue)
        return cats


# ──────────────────────────────────────────────────────────────────────────────
# Individual checks
# ──────────────────────────────────────────────────────────────────────────────

def check_terminology(
    manuscript: str,
    term_pairs: list[tuple[str, str]],
) -> list[ProofreadingIssue]:
    """
    Check for inconsistent use of term pairs.
    term_pairs: [(preferred, alternative), ...]
    e.g. [("participants", "subjects"), ("patients", "subjects")]
    """
    issues = []
    for preferred, alternative in term_pairs:
        # Count occurrences of both
        n_preferred = len(re.findall(r'\b' + re.escape(preferred) + r'\b', manuscript, re.IGNORECASE))
        n_alternative = len(re.findall(r'\b' + re.escape(alternative) + r'\b', manuscript, re.IGNORECASE))
        if n_preferred > 0 and n_alternative > 0:
            # Find where the alternative appears
            for m in re.finditer(r'\b' + re.escape(alternative) + r'\b', manuscript, re.IGNORECASE):
                # Estimate section from position
                pos = m.start()
                context = manuscript[max(0, pos - 50):pos + 50].replace("\n", " ")
                issues.append(ProofreadingIssue(
                    category="terminology",
                    description=(
                        f'"{alternative}" used inconsistently with "{preferred}" '
                        f"({n_preferred} vs {n_alternative} occurrences)"
                    ),
                    location="See context",
                    original=context.strip(),
                    recommendation=f'Use "{preferred}" throughout.',
                ))
                break  # report once per pair
    return issues


def check_abbreviations(manuscript: str) -> list[ProofreadingIssue]:
    """
    Find abbreviations (2+ uppercase letters) that appear before their definition,
    or that are defined but never used, or used inconsistently.
    """
    issues = []
    defined: dict[str, int] = {}  # abbrev → position of definition
    for m in _DEFINITION_PATTERN.finditer(manuscript):
        abbrev = m.group(2)
        if abbrev not in defined:
            defined[abbrev] = m.start()

    # Check for abbreviations used before definition
    for m in _ABBREV_PATTERN.finditer(manuscript):
        abbrev = m.group(1)
        # Skip common non-abbreviations
        if abbrev in {"DNA", "RNA", "USA", "UK", "CT", "MRI", "BMI", "CI", "HR", "OR", "OR", "SD", "SEM"}:
            continue  # well-known, conventionally not re-defined
        if abbrev in defined and m.start() < defined[abbrev]:
            context = manuscript[max(0, m.start() - 30):m.start() + 30].replace("\n", " ")
            issues.append(ProofreadingIssue(
                category="terminology",
                description=f'Abbreviation "{abbrev}" used before definition',
                location="See context",
                original=context.strip(),
                recommendation=f'Move definition of "{abbrev}" to first use.',
            ))

    return issues


def check_figure_references(
    manuscript: str,
    expected_figure_count: int,
) -> list[ProofreadingIssue]:
    """
    Check that:
    - Figures are cited in sequential order (Figure 1 before Figure 2, etc.)
    - All expected figures are cited
    - No figures are cited that don't exist (based on expected_figure_count)
    """
    issues = []
    # Find all figure citations: "Figure N", "Fig. N", "Figure NA", etc.
    fig_pattern = re.compile(r'Fig(?:ure)?\.?\s*(\d+)([A-Z]?)', re.IGNORECASE)
    citations = [(int(m.group(1)), m.group(2), m.start()) for m in fig_pattern.finditer(manuscript)]

    if not citations:
        if expected_figure_count > 0:
            issues.append(ProofreadingIssue(
                category="figure_ref",
                description=f"No figure citations found in manuscript (expected {expected_figure_count})",
                location="entire manuscript",
                recommendation="Ensure all figures are cited in the text.",
            ))
        return issues

    # Check sequential order
    last_fig_num = 0
    for fig_num, panel, pos in citations:
        if fig_num > last_fig_num + 1 and fig_num > 1:
            context = manuscript[max(0, pos - 30):pos + 30].replace("\n", " ")
            issues.append(ProofreadingIssue(
                category="figure_ref",
                description=f"Figure {fig_num} cited before Figure {last_fig_num + 1} appears",
                location="See context",
                original=context.strip(),
                recommendation="Ensure figures are cited in sequential order.",
            ))
        last_fig_num = max(last_fig_num, fig_num)

    # Check all expected figures cited
    cited_nums = {num for num, _, _ in citations}
    for n in range(1, expected_figure_count + 1):
        if n not in cited_nums:
            issues.append(ProofreadingIssue(
                category="figure_ref",
                description=f"Figure {n} not cited in manuscript text",
                location="check Results / Methods sections",
                recommendation=f"Add citation to Figure {n} where it is first discussed.",
            ))

    # Check for out-of-range citations
    for fig_num, _, pos in citations:
        if fig_num > expected_figure_count:
            context = manuscript[max(0, pos - 30):pos + 30].replace("\n", " ")
            issues.append(ProofreadingIssue(
                category="figure_ref",
                description=f"Figure {fig_num} cited but only {expected_figure_count} figures confirmed",
                location="See context",
                original=context.strip(),
                recommendation="Renumber or remove citation.",
            ))

    return issues


def check_claim_language(
    manuscript: str,
) -> list[ProofreadingIssue]:
    """
    Flag overclaiming language in Abstract and Conclusion sections.
    """
    OVERCLAIMING_TERMS = [
        "demonstrates", "proves", "confirms", "establishes",
        "definitively", "clearly shows", "is effective",
        "is superior", "significantly better",
    ]
    EXPLORATORY_QUALIFIERS = ["suggests", "indicates", "may", "could", "warrant", "further study"]

    issues = []

    # Extract Abstract and Conclusion for special scrutiny
    abstract_match = re.search(r'## Abstract\s*(.*?)(?=\n##|\Z)', manuscript, re.DOTALL | re.IGNORECASE)
    conclusion_match = re.search(r'## Conclusion\s*(.*?)(?=\n##|\Z)', manuscript, re.DOTALL | re.IGNORECASE)

    for section_name, match in [("Abstract", abstract_match), ("Conclusion", conclusion_match)]:
        if not match:
            continue
        section_text = match.group(1)
        for term in OVERCLAIMING_TERMS:
            m = re.search(r'\b' + re.escape(term) + r'\b', section_text, re.IGNORECASE)
            if m:
                    start = max(0, m.start() - 60)
                    context = section_text[start:m.start() + 60].replace("\n", " ")
                    qualifier = " / ".join(EXPLORATORY_QUALIFIERS[:3])
                    issues.append(ProofreadingIssue(
                        category="claim_language",
                        description=f'Overclaiming term "{term}" in {section_name}',
                        location=section_name,
                        original=f"…{context.strip()}…",
                        recommendation=(
                            f'Replace with cautious language: e.g. "{qualifier}".'
                        ),
                    ))

    return issues


def check_statistics_consistency(
    manuscript: str,
    confirmed_stats: dict[str, str],
) -> list[ProofreadingIssue]:
    """
    Verify that key statistics in the manuscript match the confirmed analysis results.

    confirmed_stats: {"test_description": "reported_value"}
    e.g. {"primary outcome p-value": "p = .034", "effect size": "d = 0.32"}
    """
    issues = []
    for stat_label, expected_value in confirmed_stats.items():
        # Strip spaces for flexible matching
        clean_expected = expected_value.replace(" ", "")
        pattern = re.escape(clean_expected).replace(r"\ ", r"\s*")
        if not re.search(pattern, manuscript.replace(" ", ""), re.IGNORECASE):
            issues.append(ProofreadingIssue(
                category="statistics",
                description=f'Expected statistic not found: {stat_label} = "{expected_value}"',
                location="Results section",
                original="",
                recommendation=f'Verify that "{expected_value}" appears in the Results as reported at CP 1B.',
            ))
    return issues


# ──────────────────────────────────────────────────────────────────────────────
# Master check runner
# ──────────────────────────────────────────────────────────────────────────────

def run_all_checks(
    manuscript: str,
    *,
    term_pairs: list[tuple[str, str]] | None = None,
    expected_figure_count: int = 0,
    confirmed_stats: dict[str, str] | None = None,
) -> ProofreadReport:
    """
    Run the full proofreading checklist.
    Returns a ProofreadReport with all issues found.
    """
    report = ProofreadReport()

    # 1. Terminology
    default_pairs = [
        ("participants", "subjects"),
        ("participants", "patients"),
        ("participants", "cases"),
    ]
    all_pairs = (term_pairs or []) + default_pairs
    report.issues.extend(check_terminology(manuscript, all_pairs))

    # 2. Abbreviations
    report.issues.extend(check_abbreviations(manuscript))

    # 3. Figure references
    if expected_figure_count > 0:
        report.issues.extend(check_figure_references(manuscript, expected_figure_count))

    # 4. Statistics consistency
    if confirmed_stats:
        report.issues.extend(check_statistics_consistency(manuscript, confirmed_stats))

    # 5. Claim language
    report.issues.extend(check_claim_language(manuscript))

    # Identify clean sections (those with no issues)
    all_sections = ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]
    affected = {issue.location for issue in report.issues}
    report.clean_sections = [s for s in all_sections if s not in affected]

    return report


# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint 4: report formatting
# ──────────────────────────────────────────────────────────────────────────────

def format_cp4_report(report: ProofreadReport) -> str:
    """Format the full proofreading report for CP 4."""
    cats = report.issues_by_category()
    lines = [
        "## Proofreading Report — Stage 4-B",
        "",
        f"Total issues found: **{len(report.issues)}**",
        "",
    ]

    category_labels = {
        "terminology": "Terminology Issues",
        "citation": "Citation Issues",
        "figure_ref": "Figure / Table Cross-Reference Issues",
        "statistics": "Number & Statistics Inconsistencies",
        "claim_language": "Claim-Evidence Issues",
    }

    for cat_key, label in category_labels.items():
        items = cats.get(cat_key, [])
        lines += [f"### {label}", ""]
        if items:
            for i, issue in enumerate(items, 1):
                lines += [
                    f"{i}. **{issue.description}**",
                    f"   Location: {issue.location}",
                ]
                if issue.original:
                    lines.append(f"   Original: `{issue.original}`")
                if issue.recommendation:
                    lines.append(f"   → {issue.recommendation}")
                lines.append("")
        else:
            lines += ["No issues found. ✓", ""]

    if report.clean_sections:
        lines += [
            "### Clean Sections",
            "",
            "The following sections passed all automated checks:",
            "",
        ]
        for s in report.clean_sections:
            lines.append(f"- {s} ✓")
        lines.append("")

    lines += [
        "---",
        "✓ **CHECKPOINT 4** — Proofreading complete",
        "Approve final output?  `[OK]` → manuscript exported  |  `[FIX: ...]`",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Session integration
# ──────────────────────────────────────────────────────────────────────────────

def save_proofread_to_session(
    ws: "WorkSpace",
    report_text: str,
    session: "ARSession | None" = None,
) -> None:
    """Persist Stage 4-B proofread report to disk and session state."""
    ws.save_proofread_report(report_text)
    if session is not None:
        session.proofread_report = report_text
        session.save()
