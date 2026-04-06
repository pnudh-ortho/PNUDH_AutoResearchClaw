"""
WorkSpace — directory structure and file I/O for one AutoResearch session.

Layout:
  {session_id}/
  ├── session.json
  ├── input/                   user-provided data files and reference PDFs
  ├── stage1/
  │   ├── data/                copies/links of input data
  │   ├── analysis/            generated analysis code + result outputs
  │   │   ├── analysis_plan.md     (CP 1A proposal)
  │   │   ├── analysis_code.py     (generated code)
  │   │   ├── analysis_results.txt (captured stdout/output)
  │   │   └── interpretation.md    (CP 1B confirmed interpretation)
  │   └── figures/             generated figure code + rendered images
  │       ├── figure_plan.md       (CP 1C proposal)
  │       ├── fig{N}_{name}.py     (figure script per finding)
  │       ├── fig{N}_{name}.pdf
  │       └── captions.md
  ├── stage2/
  │   ├── literature/          search results and synthesis
  │   │   ├── search_log.md        (databases queried, strings used)
  │   │   ├── included_papers.bib  (reference list)
  │   │   └── synthesis.md         (CP 2A confirmed synthesis)
  │   ├── story/               narrative blueprint
  │   │   ├── key_message.md
  │   │   └── outline.md           (CP 2B section-by-section outline)
  │   └── manuscript/          section drafts
  │       ├── methods.md
  │       ├── results.md
  │       ├── discussion.md
  │       ├── conclusion.md
  │       ├── introduction.md
  │       ├── abstract.md
  │       └── full_manuscript.md   (assembled after all sections confirmed)
  ├── stage3/
  │   ├── reviewer_a.md
  │   ├── reviewer_b.md
  │   ├── reviewer_c.md
  │   └── synthesis.md             (auto-generated, presented at CP 3)
  └── stage4/
      ├── revision_checklist.md    (from CP 3: which items to address)
      ├── revised_manuscript.md
      ├── change_log.md
      └── proofread_report.md      (CP 4)
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
    def stage1_dir(self) -> Path:
        return self.root / "stage1"

    @property
    def analysis_dir(self) -> Path:
        return self.root / "stage1" / "analysis"

    @property
    def figures_dir(self) -> Path:
        return self.root / "stage1" / "figures"

    @property
    def stage2_dir(self) -> Path:
        return self.root / "stage2"

    @property
    def literature_dir(self) -> Path:
        return self.root / "stage2" / "literature"

    @property
    def story_dir(self) -> Path:
        return self.root / "stage2" / "story"

    @property
    def manuscript_dir(self) -> Path:
        return self.root / "stage2" / "manuscript"

    @property
    def stage3_dir(self) -> Path:
        return self.root / "stage3"

    @property
    def stage4_dir(self) -> Path:
        return self.root / "stage4"

    @property
    def archive_dir(self) -> Path:
        return self.root / "archive"

    # ── scaffold ─────────────────────────────────────────────────────────

    def scaffold(self) -> None:
        """Create the full directory tree for a new session."""
        for d in [
            self.input_dir,
            self.analysis_dir,
            self.figures_dir,
            self.literature_dir,
            self.story_dir,
            self.manuscript_dir,
            self.stage3_dir,
            self.stage4_dir,
            self.archive_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)

        # Write README placeholders
        (self.input_dir / "README.md").write_text(
            "# Input files\n\nPlace raw data (CSV, Excel) and reference PDFs here.\n",
            encoding="utf-8",
        )
        (self.archive_dir / "README.md").write_text(
            "# Archive\n\n"
            "Drop any files here — data, PDFs, scripts, figures, notes.\n"
            "Then ask Claude: \"archive 정리해줘\" and it will sort them\n"
            "into the correct session folders automatically.\n",
            encoding="utf-8",
        )
        (self.stage4_dir / "change_log.md").write_text(
            "# Revision Change Log\n\n"
            "| # | Checklist item | Location | Change made | Cascade effects |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )

    # ── Stage 1-A helpers ─────────────────────────────────────────────────

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

    # ── Stage 1-B helpers ─────────────────────────────────────────────────

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

    # ── Stage 2-A helpers ─────────────────────────────────────────────────

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

    # ── Stage 2-B helpers ─────────────────────────────────────────────────

    def save_key_message(self, content: str) -> Path:
        p = self.story_dir / "key_message.md"
        p.write_text(content, encoding="utf-8")
        return p

    def save_narrative_outline(self, content: str) -> Path:
        p = self.story_dir / "outline.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_narrative_outline(self) -> str:
        p = self.story_dir / "outline.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ── Stage 2-C helpers ─────────────────────────────────────────────────

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

    # ── Stage 3 helpers ───────────────────────────────────────────────────

    def save_review(self, reviewer: str, content: str) -> Path:
        """reviewer: 'a', 'b', or 'c'"""
        p = self.stage3_dir / f"reviewer_{reviewer.lower()}.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_review(self, reviewer: str) -> str:
        p = self.stage3_dir / f"reviewer_{reviewer.lower()}.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def save_review_synthesis(self, content: str) -> Path:
        p = self.stage3_dir / "synthesis.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_review_synthesis(self) -> str:
        p = self.stage3_dir / "synthesis.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def all_reviews_present(self) -> bool:
        return all(
            (self.stage3_dir / f"reviewer_{x}.md").exists() for x in ("a", "b", "c")
        )

    # ── Stage 4 helpers ───────────────────────────────────────────────────

    def save_revision_checklist(self, content: str) -> Path:
        p = self.stage4_dir / "revision_checklist.md"
        p.write_text(content, encoding="utf-8")
        return p

    def read_revision_checklist(self) -> str:
        p = self.stage4_dir / "revision_checklist.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def save_revised_manuscript(self, content: str) -> Path:
        p = self.stage4_dir / "revised_manuscript.md"
        p.write_text(content, encoding="utf-8")
        return p

    def append_change_log_row(self, row: dict) -> None:
        """Append one row to the change_log.md table."""
        p = self.stage4_dir / "change_log.md"
        num = row.get("num", "?")
        item = row.get("item", "")
        location = row.get("location", "")
        change = row.get("change", "")
        cascade = row.get("cascade", "None")
        line = f"| {num} | {item} | {location} | {change} | {cascade} |\n"
        with p.open("a", encoding="utf-8") as f:
            f.write(line)

    def read_change_log(self) -> str:
        p = self.stage4_dir / "change_log.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def save_proofread_report(self, content: str) -> Path:
        p = self.stage4_dir / "proofread_report.md"
        p.write_text(content, encoding="utf-8")
        return p

    # ── generic helpers ───────────────────────────────────────────────────

    def list_input_files(self) -> list[Path]:
        return [p for p in self.input_dir.iterdir() if p.is_file() and p.name != "README.md"]

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

        # Extension fast-paths (no content inspection needed)
        FAST_PATH = {
            ".csv": "raw_data", ".tsv": "raw_data",
            ".sav": "raw_data", ".sas7bdat": "raw_data", ".dta": "raw_data",
            ".bib": "bibliography", ".ris": "bibliography", ".nbib": "bibliography",
            ".png": "figure_image", ".jpg": "figure_image", ".jpeg": "figure_image",
            ".tiff": "figure_image", ".svg": "figure_image",
        }

        # Statistical output keywords for text-based files
        _STAT_KEYWORDS = (
            "p =", "p<", "p =", "t(", "F(", "χ²", "U =", "H =", "df =",
            "95% CI", "Cohen", "OR =", "HR =", "AUC", "mean =", "SD =",
        )
        # Figure code keywords
        _FIG_PY = ("matplotlib", "seaborn", "plt.", "sns.", "subplots", "fig,", "ax =")
        _FIG_R  = ("ggplot", "plot(", "hist(", "barplot(", "geom_", "survplot")
        # Manuscript section headers
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

            # 1. Fast-path by extension
            if ext in FAST_PATH:
                categories[FAST_PATH[ext]].append(p)
                continue

            # 2. Content-dependent classification
            if ext in (".xlsx", ".xls"):
                head = _read_head(p, 3)
                stat_headers = ("p-value", "p_val", " or ", " hr ", " ci ", "coefficient",
                                "effect_size", "mean", "sd", "median", "beta", "β")
                cat = "analysis_output" if any(k in head for k in stat_headers) else "raw_data"
                categories[cat].append(p)

            elif ext == ".pdf":
                name_lower = p.stem.lower()
                # Filename heuristic: year + journal abbreviation pattern
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

        Entry stages: "Stage 1-A", "Stage 1-C", "Stage 2-A", "Stage 2-C", "Stage 3"
        """
        drafts     = classified.get("manuscript_draft", [])
        analysis   = classified.get("analysis_output", [])
        figures    = classified.get("figure_image", [])
        raw        = classified.get("raw_data", [])
        refs       = classified.get("reference_pdf", [])

        # Detect which manuscript sections are present from filenames / content
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
                "Stage 3",
                "All 5 required manuscript sections are present.",
                ["1A", "1B", "1C", "2A", "2B", "2C-1", "2C-2", "2C-3", "2C-4", "2C-5", "2C-6"],
            )

        if sections:
            writing_order = ["methods", "results", "discussion", "conclusion", "introduction"]
            missing = [s for s in writing_order if s not in sections]
            next_section = missing[0] if missing else "abstract"
            # Map section name to CP ID
            cp_map = {
                "methods": "2C-1", "results": "2C-2", "discussion": "2C-3",
                "conclusion": "2C-4", "introduction": "2C-5",
            }
            cleared_up_to = [cp_map[s] for s in writing_order if s in sections and s in cp_map]
            return (
                "Stage 2-C",
                f"Partial manuscript found ({len(sections)}/5 sections). Next section: {next_section}.",
                ["1A", "1B", "1C", "2A", "2B"] + cleared_up_to,
            )

        if analysis and figures:
            return (
                "Stage 2-A",
                "Analysis output and figures already present — skip to literature and writing.",
                ["1A", "1B", "1C"],
            )

        if analysis and not figures:
            return (
                "Stage 1-C",
                "Analysis output present but no figures — proceed to visualization.",
                ["1A", "1B"],
            )

        if refs and not raw and not analysis:
            return (
                "Stage 2-A",
                "Reference PDFs provided with no data — reference-only or review mode.",
                [],
            )

        # Default: raw data present, or nothing at all
        return (
            "Stage 1-A",
            "Raw data present — begin with full data analysis." if raw else "No materials found — empty start.",
            [],
        )

    def summary(self) -> str:
        """Quick text summary of what exists in the workspace."""
        lines = [f"Workspace: {self.root}"]
        for label, d in [
            ("Input files", self.input_dir),
            ("Analysis", self.analysis_dir),
            ("Figures", self.figures_dir),
            ("Literature", self.literature_dir),
            ("Story", self.story_dir),
            ("Manuscript", self.manuscript_dir),
            ("Reviews", self.stage3_dir),
            ("Revision", self.stage4_dir),
        ]:
            files = [p.name for p in d.iterdir() if p.is_file()] if d.exists() else []
            if files:
                lines.append(f"  {label}: {', '.join(files)}")
        return "\n".join(lines)
