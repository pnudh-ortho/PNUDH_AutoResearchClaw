"""
WorkSpace — directory structure and file I/O for one AutoResearch session.

9-stage layout:
  {session_id}/
  ├── session.json
  ├── input/                   original user-provided files (never moved)
  ├── archive/                 drop zone: sort with organize skill
  ├── stage1/                  [Stage 1] intake manifest
  │   └── intake_report.md
  ├── stage2/                  [Stage 2] background knowledge
  │   ├── search_log.md
  │   ├── included_papers.bib
  │   └── synthesis.md             (CP 2 confirmed synthesis)
  ├── stage3/                  [Stage 3] data analysis
  │   ├── analysis_plan.md         (CP 3A proposal)
  │   ├── analysis_code.py         (generated code)
  │   ├── analysis_results.txt     (captured output)
  │   └── interpretation.md        (CP 3B confirmed interpretation)
  ├── stage4/                  [Stage 4] visualization
  │   ├── figure_plan.md           (CP 4 proposal)
  │   ├── fig{N}_{name}.py
  │   ├── fig{N}_{name}.pdf
  │   └── captions.md
  ├── stage5/                  [Stage 5] paper outline
  │   ├── key_message.md
  │   └── outline.md               (CP 5 section-by-section outline)
  ├── stage6/                  [Stage 6] manuscript draft
  │   ├── methods.md
  │   ├── results.md
  │   ├── discussion.md
  │   ├── conclusion.md
  │   ├── introduction.md
  │   ├── abstract.md
  │   └── full_manuscript.md       (assembled after all 6 sections confirmed)
  ├── stage7/                  [Stage 7] peer review
  │   ├── reviewer_a.md
  │   ├── reviewer_b.md
  │   ├── reviewer_c.md
  │   └── synthesis.md             (CP 7 auto-synthesis)
  ├── stage8/                  [Stage 8] revision
  │   ├── revision_checklist.md
  │   ├── revised_manuscript.md
  │   ├── change_log.md
  │   └── response_letter.md
  └── stage9/                  [Stage 9] proofreading
      └── proofread_report.md      (CP 9)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession


class WorkSpace:
    """File-system interface for a single AutoResearch session."""

    def __init__(self, session: "ARSession") -> None:
        self.root = Path(session.workspace_dir)

    # ── directory accessors ───────────────────────────────────────────────

    @property
    def input_dir(self) -> Path:
        return self.root / "input"

    @property
    def archive_dir(self) -> Path:
        return self.root / "archive"

    @property
    def intake_dir(self) -> Path:           # Stage 1
        return self.root / "stage1"

    @property
    def literature_dir(self) -> Path:       # Stage 2
        return self.root / "stage2"

    @property
    def analysis_dir(self) -> Path:         # Stage 3
        return self.root / "stage3"

    @property
    def figures_dir(self) -> Path:          # Stage 4
        return self.root / "stage4"

    @property
    def outline_dir(self) -> Path:          # Stage 5
        return self.root / "stage5"

    @property
    def manuscript_dir(self) -> Path:       # Stage 6
        return self.root / "stage6"

    @property
    def review_dir(self) -> Path:           # Stage 7
        return self.root / "stage7"

    @property
    def revision_dir(self) -> Path:         # Stage 8
        return self.root / "stage8"

    @property
    def proofread_dir(self) -> Path:        # Stage 9
        return self.root / "stage9"

    # ── legacy aliases (keep until all stage runners are updated) ─────────
    @property
    def stage3_dir(self) -> Path:
        """Legacy alias for review_dir (Stage 7)."""
        return self.review_dir

    @property
    def stage4_dir(self) -> Path:
        """Legacy alias for revision_dir (Stage 8)."""
        return self.revision_dir

    # ── scaffold ─────────────────────────────────────────────────────────

    def scaffold(self) -> None:
        """Create the full directory tree for a new session."""
        for d in [
            self.input_dir,
            self.archive_dir,
            self.intake_dir,
            self.literature_dir,
            self.analysis_dir,
            self.figures_dir,
            self.outline_dir,
            self.manuscript_dir,
            self.review_dir,
            self.revision_dir,
            self.proofread_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)

        # Write README placeholders
        (self.input_dir / "README.md").write_text(
            "# Input files\n\nOriginal user-provided files — never deleted.\n"
            "Drop additional files into archive/ and run 'organize'.\n",
            encoding="utf-8",
        )
        (self.archive_dir / "README.md").write_text(
            "# Archive\n\n"
            "Drop any files here at any point — data, PDFs, scripts, figures, notes.\n"
            "Then say 'organize' or 'archive 정리해줘' and Claude will sort them\n"
            "into the correct stage directories automatically.\n",
            encoding="utf-8",
        )
        # Initialize change log with header
        (self.revision_dir / "change_log.md").write_text(
            "# Revision Change Log — Stage 8\n\n"
            "| # | Checklist item | Location | Before | After | Cascade effects |\n"
            "|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )

    # ── Stage 1: Intake ────────────────────────────────────────────────────

    def save_intake_report(self, content: str) -> Path:
        p = self.intake_dir / "intake_report.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_intake_report(self) -> str:
        p = self.intake_dir / "intake_report.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── Stage 2: Background Knowledge ─────────────────────────────────────

    def save_search_log(self, content: str) -> Path:
        p = self.literature_dir / "search_log.md"
        p.write_text(content, encoding="utf-8")
        return p

    def save_references_bib(self, bib_content: str) -> Path:
        p = self.literature_dir / "included_papers.bib"
        p.write_text(bib_content, encoding="utf-8")
        return p

    def save_literature_synthesis(self, content: str) -> Path:
        p = self.literature_dir / "synthesis.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_literature_synthesis(self) -> str:
        p = self.literature_dir / "synthesis.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── Stage 3: Data Analysis ─────────────────────────────────────────────

    def save_analysis_plan(self, content: str) -> Path:
        p = self.analysis_dir / "analysis_plan.md"
        p.write_text(content, encoding="utf-8")
        return p

    def save_analysis_code(self, code: str, language: str = "python") -> Path:
        ext = "R" if language.lower() == "r" else "py"
        p = self.analysis_dir / f"analysis_code.{ext}"
        p.write_text(code, encoding="utf-8")
        return p

    def save_analysis_results(self, output: str) -> Path:
        p = self.analysis_dir / "analysis_results.txt"
        p.write_text(output, encoding="utf-8")
        return p

    def save_interpretation(self, content: str) -> Path:
        p = self.analysis_dir / "interpretation.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_analysis_results(self) -> str:
        p = self.analysis_dir / "analysis_results.txt"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def read_interpretation(self) -> str:
        p = self.analysis_dir / "interpretation.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── Stage 4: Visualization ─────────────────────────────────────────────

    def save_figure_plan(self, content: str) -> Path:
        p = self.figures_dir / "figure_plan.md"
        p.write_text(content, encoding="utf-8")
        return p

    def save_figure_code(self, index: int, name: str, code: str, language: str = "python") -> Path:
        ext = "R" if language.lower() == "r" else "py"
        safe_name = name.replace(" ", "_").lower()
        p = self.figures_dir / f"fig{index}_{safe_name}.{ext}"
        p.write_text(code, encoding="utf-8")
        return p

    def save_captions(self, content: str) -> Path:
        p = self.figures_dir / "captions.md"
        p.write_text(content, encoding="utf-8")
        return p

    def list_figure_scripts(self) -> list[Path]:
        return sorted(self.figures_dir.glob("fig*.py")) + sorted(self.figures_dir.glob("fig*.R"))

    # ── Stage 5: Paper Outline ─────────────────────────────────────────────

    def save_key_message(self, content: str) -> Path:
        p = self.outline_dir / "key_message.md"
        p.write_text(content, encoding="utf-8")
        return p

    def save_narrative_outline(self, content: str) -> Path:
        p = self.outline_dir / "outline.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_narrative_outline(self) -> str:
        p = self.outline_dir / "outline.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── Stage 6: Paper Draft ───────────────────────────────────────────────

    def save_section_draft(self, section_name: str, content: str) -> Path:
        safe = section_name.lower().replace(" ", "_")
        p = self.manuscript_dir / f"{safe}.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_section_draft(self, section_name: str) -> str:
        safe = section_name.lower().replace(" ", "_")
        p = self.manuscript_dir / f"{safe}.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def assemble_manuscript(self, session: "ARSession") -> Path:
        """Write full_manuscript.md from confirmed section drafts."""
        import sys as _sys
        required = {"abstract", "introduction", "methods", "results", "discussion", "conclusion"}
        missing = required - set(session.section_drafts.keys())
        if missing:
            print(
                f"Warning: assembling incomplete manuscript — missing sections: {', '.join(sorted(missing))}",
                file=_sys.stderr,
            )
        content = session.full_manuscript()
        p = self.manuscript_dir / "full_manuscript.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_full_manuscript(self) -> str:
        p = self.manuscript_dir / "full_manuscript.md"
        if p.exists():
            return p.read_text(encoding="utf-8")
        # Fall back to reading individual sections
        sections: list[str] = []
        for sec in ["abstract", "introduction", "methods", "results", "discussion", "conclusion"]:
            text = self.read_section_draft(sec)
            if text:
                sections.append(f"## {sec.title()}\n\n{text}")
        return "\n\n---\n\n".join(sections)

    # ── Stage 7: Peer Review ──────────────────────────────────────────────

    def save_review(self, reviewer: str, content: str) -> Path:
        """reviewer: 'a', 'b', or 'c'"""
        p = self.review_dir / f"reviewer_{reviewer.lower()}.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_review(self, reviewer: str) -> str:
        p = self.review_dir / f"reviewer_{reviewer.lower()}.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def save_review_synthesis(self, content: str) -> Path:
        p = self.review_dir / "synthesis.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_review_synthesis(self) -> str:
        p = self.review_dir / "synthesis.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def all_reviews_present(self) -> bool:
        return all(
            (self.review_dir / f"reviewer_{x}.md").exists() for x in ("a", "b", "c")
        )

    # ── Stage 8: Revision ─────────────────────────────────────────────────

    def save_revision_checklist(self, content: str) -> Path:
        p = self.revision_dir / "revision_checklist.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_revision_checklist(self) -> str:
        p = self.revision_dir / "revision_checklist.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def save_revised_manuscript(self, content: str) -> Path:
        p = self.revision_dir / "revised_manuscript.md"
        p.write_text(content, encoding="utf-8")
        return p

    def append_change_log_row(self, row: dict) -> None:
        """Append one row to the change_log.md table."""
        p = self.revision_dir / "change_log.md"
        num = row.get("num", "?")
        item = row.get("item", "")
        location = row.get("location", "")
        before = row.get("before", "")
        after = row.get("after", "")
        cascade = row.get("cascade", "None")
        line = f"| {num} | {item} | {location} | {before} | {after} | {cascade} |\n"
        with p.open("a", encoding="utf-8") as f:
            f.write(line)

    def read_change_log(self) -> str:
        p = self.revision_dir / "change_log.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def save_response_letter(self, content: str) -> Path:
        p = self.revision_dir / "response_letter.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_response_letter(self) -> str:
        p = self.revision_dir / "response_letter.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── Stage 9: Proofreading ─────────────────────────────────────────────

    def save_proofread_report(self, content: str) -> Path:
        p = self.proofread_dir / "proofread_report.md"
        p.write_text(content, encoding="utf-8")
        return p

    # ── generic helpers ───────────────────────────────────────────────────

    def list_input_files(self) -> list[Path]:
        return [p for p in self.input_dir.iterdir() if p.is_file() and p.name != "README.md"]

    def summary(self) -> str:
        """Quick text summary of what exists in the workspace."""
        STAGE_DIRS = [
            ("Input files",   self.input_dir),
            ("Stage 1 Intake", self.intake_dir),
            ("Stage 2 Literature", self.literature_dir),
            ("Stage 3 Analysis", self.analysis_dir),
            ("Stage 4 Figures", self.figures_dir),
            ("Stage 5 Outline", self.outline_dir),
            ("Stage 6 Manuscript", self.manuscript_dir),
            ("Stage 7 Review", self.review_dir),
            ("Stage 8 Revision", self.revision_dir),
            ("Stage 9 Proofread", self.proofread_dir),
        ]
        lines = [f"Workspace: {self.root}"]
        for label, d in STAGE_DIRS:
            files = [p.name for p in d.iterdir() if p.is_file()] if d.exists() else []
            if files:
                lines.append(f"  {label}: {', '.join(files)}")
        return "\n".join(lines)

    # ── intake helpers ────────────────────────────────────────────────────

    @staticmethod
    def classify_input_files(topic_dir: Path) -> dict[str, list[Path]]:
        """
        Classify all files in topic_dir into pipeline categories.

        Returns a dict with these keys (each value is a list of Paths):
          raw_data, analysis_output, figure_image, figure_code,
          analysis_code, reference_pdf, bibliography, manuscript_draft,
          protocol_doc, notes, unclear

        This mirrors the classification logic in .claude/skills/intake/SKILL.md.
        """
        categories: dict[str, list[Path]] = {
            "raw_data": [], "analysis_output": [], "figure_image": [],
            "figure_code": [], "analysis_code": [], "reference_pdf": [],
            "bibliography": [], "manuscript_draft": [], "protocol_doc": [],
            "notes": [], "unclear": [],
        }

        FAST_PATH = {
            ".csv": "raw_data", ".tsv": "raw_data",
            ".sav": "raw_data", ".sas7bdat": "raw_data", ".dta": "raw_data",
            ".bib": "bibliography", ".ris": "bibliography", ".nbib": "bibliography",
            ".png": "figure_image", ".jpg": "figure_image", ".jpeg": "figure_image",
            ".tiff": "figure_image", ".svg": "figure_image",
        }

        _STAT_KEYWORDS = (
            "p =", "p<", "t(", "f(", "χ²", "u =", "h =", "df =",
            "95% ci", "cohen", "or =", "hr =", "auc", "mean =", "sd =",
        )
        _FIG_PY = ("matplotlib", "seaborn", "plt.", "sns.", "subplots", "fig,", "ax =")
        _FIG_R  = ("ggplot", "plot(", "hist(", "barplot(", "geom_", "survplot")
        _MANUSCRIPT_HEADERS = (
            "## methods", "## results", "## discussion",
            "## conclusion", "## introduction", "## abstract",
        )
        _PROTOCOL_KEYWORDS = (
            "hypothesis", "study design", "inclusion criteria",
            "exclusion criteria", "protocol",
        )

        def _read_head(path: Path, lines: int = 50) -> str:
            try:
                with path.open(encoding="utf-8", errors="ignore") as f:
                    return "".join(f.readline() for _ in range(lines)).lower()
            except Exception:
                return ""

        all_files = [
            p for p in topic_dir.rglob("*")
            if p.is_file() and p.name != "README.md"
        ]

        for p in all_files:
            ext = p.suffix.lower()

            if ext in FAST_PATH:
                categories[FAST_PATH[ext]].append(p)
                continue

            if ext in (".xlsx", ".xls"):
                head = _read_head(p, 3)
                stat_headers = ("p-value", "p_val", " or ", " hr ", " ci ", "coefficient",
                                "effect_size", "mean", "sd", "median", "beta", "β")
                cat = "analysis_output" if any(k in head for k in stat_headers) else "raw_data"
                categories[cat].append(p)

            elif ext == ".pdf":
                name_lower = p.stem.lower()
                import re as _re
                if _re.search(r"\d{4}", name_lower):
                    categories["reference_pdf"].append(p)
                elif any(k in name_lower for k in ("fig", "figure")):
                    categories["figure_image"].append(p)
                else:
                    categories["reference_pdf"].append(p)

            elif ext == ".py":
                head = _read_head(p, 20)
                cat = "figure_code" if any(k in head for k in _FIG_PY) else "analysis_code"
                categories[cat].append(p)

            elif ext in (".r", ".rmd"):
                head = _read_head(p, 20)
                cat = "figure_code" if any(k in head for k in _FIG_R) else "analysis_code"
                categories[cat].append(p)

            elif ext in (".txt", ".log", ".html"):
                head = _read_head(p, 50)
                cat = "analysis_output" if any(k in head for k in _STAT_KEYWORDS) else "notes"
                categories[cat].append(p)

            elif ext in (".md", ".docx"):
                head = _read_head(p, 80)
                if any(k in head for k in _MANUSCRIPT_HEADERS):
                    categories["manuscript_draft"].append(p)
                elif any(k in head for k in _PROTOCOL_KEYWORDS):
                    categories["protocol_doc"].append(p)
                else:
                    categories["notes"].append(p)

            else:
                categories["unclear"].append(p)

        return categories

    @staticmethod
    def determine_entry_point(classified: dict[str, list[Path]]) -> tuple[str, str, list[str]]:
        """
        Apply the intake decision tree to classification results.

        Returns:
          (entry_stage, reason, auto_clear_checkpoints)

        Entry stages match the new 9-stage numbering:
          "Stage 3" (data analysis), "Stage 4" (visualization),
          "Stage 2" (literature), "Stage 6" (draft continue), "Stage 7" (review)
        """
        drafts   = classified.get("manuscript_draft", [])
        analysis = classified.get("analysis_output", [])
        figures  = classified.get("figure_image", [])
        raw      = classified.get("raw_data", [])
        refs     = classified.get("reference_pdf", [])

        SECTION_KEYS = {"methods", "results", "discussion", "conclusion", "introduction"}

        def _sections_in(paths: list[Path]) -> set[str]:
            found: set[str] = set()
            for p in paths:
                name = p.stem.lower()
                for sec in SECTION_KEYS:
                    if sec in name:
                        found.add(sec)
            return found

        sections = _sections_in(drafts)

        if len(sections) >= 5:
            return (
                "Stage 7",
                "All 5+ required manuscript sections present — proceed to peer review.",
                ["1", "2", "3A", "3B", "4", "5",
                 "6-1", "6-2", "6-3", "6-4", "6-5", "6-6"],
            )

        if sections:
            writing_order = ["methods", "results", "discussion", "conclusion", "introduction"]
            missing = [s for s in writing_order if s not in sections]
            next_section = missing[0] if missing else "abstract"
            cp_map = {
                "methods": "6-1", "results": "6-2", "discussion": "6-3",
                "conclusion": "6-4", "introduction": "6-5",
            }
            cleared_up_to = [cp_map[s] for s in writing_order if s in sections and s in cp_map]
            return (
                "Stage 6",
                f"Partial manuscript found ({len(sections)}/5 sections). Next section: {next_section}.",
                ["1", "2", "3A", "3B", "4", "5"] + cleared_up_to,
            )

        if analysis and figures:
            return (
                "Stage 5",
                "Analysis output and figures present — proceed to paper outline.",
                ["1", "2", "3A", "3B", "4"],
            )

        if analysis and not figures:
            return (
                "Stage 4",
                "Analysis output present but no figures — proceed to visualization.",
                ["1", "2", "3A", "3B"],
            )

        if refs and not raw and not analysis:
            return (
                "Stage 2",
                "Reference PDFs provided with no data — reference-only or review mode.",
                ["1"],
            )

        return (
            "Stage 3",
            "Raw data present — begin with data analysis." if raw else "Empty start.",
            ["1", "2"],
        )
