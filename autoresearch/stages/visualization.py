"""
Stage 1-B: Visualization

Responsibilities:
  1. Reason from confirmed analysis to propose figure types        → CP 1C
  2. Generate annotated Python/R code for each approved figure
  3. Execute figure scripts, capture rendered outputs
  4. Draft figure captions in the standard format

This module provides:
  - run_figure_script()   execute a figure script, capture output/errors
  - propose_figures()     format figure-plan proposal for CP 1C
  - caption_template()    return the standard caption format string
  - render_all()          run all figure scripts in the workspace
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession
    from autoresearch.workspace import WorkSpace


# ── figure type reasoning guide ────────────────────────────────────────────

FIGURE_TYPE_GUIDE = """\
## Figure Type Selection (reason through data, not from a fixed menu)

For each key finding, consider:
1. **Data type**: continuous / categorical / ordinal / survival / expression
2. **Comparison structure**:
   - 2 groups → box/violin + jitter + significance bar
   - 3+ groups → grouped box or faceted violin
   - Correlation → scatter + regression line + CI band
   - Change over time → line plot with error bars
   - Survival / time-to-event → Kaplan-Meier curve
   - Diagnostic test performance → ROC curve
   - Effect across subgroups → Forest plot
   - Differential expression → Volcano plot
   - Expression patterns across samples → Heatmap
   - Multi-omics / high-dimensional → composite multi-panel
3. **Sample size**: if n < 10 per group, individual data points are MANDATORY
4. **Readability**: the key finding must be visually obvious without reading the caption

**Libraries by figure type:**
| Figure | Python | R |
|---|---|---|
| Box/violin/bar | `matplotlib` + `seaborn` + `scienceplots` | `ggplot2` + `ggpubr` |
| Kaplan-Meier | `lifelines` | `survival` + `survminer` |
| ROC | `sklearn.metrics` | `pROC` |
| Forest plot | `forestplot` | `forestploter` / `meta` |
| Volcano | `matplotlib` custom | `EnhancedVolcano` |
| Complex heatmap | `PyComplexHeatmap` | `ComplexHeatmap` |
| OMICS multi-panel | `scanpy` + `anndata` | `Seurat` |
| Label adjustment | `adjustText` | `ggrepel` |

**Base stack always first:**
- Python: `scienceplots` + `matplotlib` + `seaborn` + `pandas` + `numpy`
- R: `ggplot2` + `tidyverse` + `ggpubr` + `ggsci`
"""

CAPTION_FORMAT = """\
Figure {n}. {title}.
{methods_note}
{key_finding}
"""

CODE_PRINCIPLES = """\
Code principles (enforce in every figure script):
1. Configuration block at top: COLORS, FONT_SIZE, FIG_W, FIG_H, DPI
2. Colorblind-safe palette by default (Okabe-Ito, viridis, ggsci journal palettes)
3. Export: PDF/SVG (vector) + PNG at ≥300 DPI
4. Panel labels (A, B, C…) bold, top-left corner
5. All text ≥ 8pt at final print size
6. Error bars: type specified explicitly (SEM / SD / 95% CI) in code + caption
7. Significance: exact p-value when space allows, NS otherwise
8. Journal widths: single 3.3–3.5 in | 1.5-col 4.5–5.5 in | full 6.5–7.1 in
9. One script per figure; code must run as-is on the session data
"""


# ──────────────────────────────────────────────────────────────────────────────
# Figure script execution
# ──────────────────────────────────────────────────────────────────────────────

class FigureRunResult:
    def __init__(self, stdout: str, stderr: str, returncode: int, script_path: Path):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.script_path = script_path
        self.success = returncode == 0

    def __repr__(self) -> str:
        status = "OK" if self.success else f"FAIL(rc={self.returncode})"
        return f"FigureRunResult({self.script_path.name}, {status})"


def run_figure_script(
    script_path: Path,
    data_dir: Path,
    output_dir: Path,
    language: str = "python",
    timeout: int = 180,
) -> FigureRunResult:
    """
    Execute a figure-generation script.
    cwd is set to data_dir so relative paths work.
    Generated files (PDF, PNG) land wherever the script writes them;
    conventionally they should use output_dir.
    """
    import shutil

    if language.lower() == "r":
        exe = shutil.which("Rscript")
        if exe is None:
            return FigureRunResult("", "Rscript not found", 1, script_path)
        cmd = [exe, str(script_path)]
    else:
        cmd = [sys.executable, str(script_path)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(data_dir),
            env={**os.environ, "MPLBACKEND": "Agg"},  # headless matplotlib
        )
        return FigureRunResult(result.stdout, result.stderr, result.returncode, script_path)
    except subprocess.TimeoutExpired:
        return FigureRunResult("", f"Timeout after {timeout}s", 1, script_path)
    except Exception as e:
        return FigureRunResult("", str(e), 1, script_path)


def render_all_figures(ws: "WorkSpace", data_dir: Path) -> list[FigureRunResult]:
    """Run all figure scripts in the workspace figures directory."""
    results = []
    for script in ws.list_figure_scripts():
        lang = "r" if script.suffix.upper() == ".R" else "python"
        result = run_figure_script(script, data_dir, ws.figures_dir, language=lang)
        results.append(result)
    return results


# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint 1C: figure plan proposal
# ──────────────────────────────────────────────────────────────────────────────

def format_cp1c_proposal(
    analysis_summary: str,
    figure_proposals: list[dict],
) -> str:
    """
    Format the CP 1C output.

    figure_proposals: list of dicts with keys:
        finding (str)        — what finding this figure shows
        data_type (str)      — continuous / survival / etc.
        candidate_a (dict)   — {type, rationale, library}
        candidate_b (dict)   — optional second candidate
        n_per_group (int)    — for n<10 individual points check
    """
    lines = [
        "## Confirmed Analysis (reference for figure planning)",
        "",
        analysis_summary,
        "",
        FIGURE_TYPE_GUIDE,
        "",
        "## Proposed Figure Plan",
        "",
        "One or two candidate figure types are proposed per finding.",
        "**User decides the final type at CP 1C.**",
        "",
    ]

    for i, prop in enumerate(figure_proposals, 1):
        n = prop.get("n_per_group", 0)
        n_note = f"  ⚠ n={n} per group — individual data points mandatory." if 0 < n < 10 else ""

        lines += [
            f"### Figure {i}: {prop.get('finding', '')}",
            f"- **Data type:** {prop.get('data_type', '')}",
            n_note,
            "",
            f"**Option A — {prop['candidate_a']['type']}**",
            f"  Rationale: {prop['candidate_a']['rationale']}",
            f"  Library: {prop['candidate_a']['library']}",
        ]
        if "candidate_b" in prop and prop["candidate_b"]:
            lines += [
                "",
                f"**Option B — {prop['candidate_b']['type']}**",
                f"  Rationale: {prop['candidate_b']['rationale']}",
                f"  Library: {prop['candidate_b']['library']}",
            ]
        lines.append("")

    lines += [
        CODE_PRINCIPLES,
        "",
        "---",
        "✓ **CHECKPOINT 1C** — Approve figure types & layout?",
        "For each figure: `[OK A]` / `[OK B]` / `[DIFFERENT TYPE: ...]`",
        "When all confirmed: `[ALL OK]` → code generation begins.",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Caption builder
# ──────────────────────────────────────────────────────────────────────────────

def build_caption(
    n: int,
    title: str,
    methods_note: str,
    key_finding: str,
    panel_labels: list[str] | None = None,
    abbreviations: str = "",
) -> str:
    """
    Build a standard figure caption.

    Example:
        Figure 2. Survival outcomes by treatment group.
        Kaplan-Meier curves for Treatment A (n=45) vs. Control (n=43). Log-rank test.
        Shaded areas = 95% CI. Treatment A showed significantly improved overall survival
        (median OS 18.3 vs. 11.2 months, HR = 0.61 [95% CI: 0.41–0.91], p = .015).
    """
    parts = [f"Figure {n}. **{title}.**", methods_note, key_finding]
    if panel_labels:
        parts.append(" ".join(f"({lbl})" for lbl in panel_labels))
    if abbreviations:
        parts.append(f"Abbreviations: {abbreviations}.")
    return " ".join(p.strip() for p in parts if p.strip())


def format_captions_block(captions: list[str]) -> str:
    return "\n\n".join(captions)


# ──────────────────────────────────────────────────────────────────────────────
# Session integration
# ──────────────────────────────────────────────────────────────────────────────

def save_figures_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    *,
    figure_plan_text: str = "",
    confirmed_figures: list[dict] | None = None,
    captions_text: str = "",
) -> None:
    """
    Persist Stage 1-B artifacts after CP 1C is cleared.

    confirmed_figures: list of dicts like
        [{"index": 1, "type": "KM curve", "title": "Overall survival", "library": "lifelines"}, ...]
    """
    if figure_plan_text:
        ws.save_figure_plan(figure_plan_text)
    if captions_text:
        ws.save_captions(captions_text)
    if confirmed_figures:
        session.figure_list = confirmed_figures
    session.save()
