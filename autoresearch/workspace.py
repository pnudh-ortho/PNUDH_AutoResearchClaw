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
