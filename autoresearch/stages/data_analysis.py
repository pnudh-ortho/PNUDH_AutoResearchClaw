"""
Stage 1-A: Data Analysis

Responsibilities:
  1. Load and inspect data files from the input/ directory
  2. Check statistical assumptions (normality, homogeneity, independence)
  3. Propose statistical tests aligned with the research topic  → CP 1A
  4. Execute approved analysis code in subprocess
  5. Capture and interpret results                          → CP 1B

This module provides:
  - run_code()         run Python/R code in a subprocess, capture output
  - explore_data()     inspect a CSV/Excel file, return summary dict
  - propose_tests()    format an analysis proposal for the researcher
  - format_results()   format raw execution output for interpretation
  - save_confirmed()   persist confirmed interpretation to the session
"""

from __future__ import annotations

import io
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession
    from autoresearch.workspace import WorkSpace


# ── constants ────────────────────────────────────────────────────────────────

ALLOWED_PYTHON_PACKAGES = {
    "pandas", "numpy", "scipy", "statsmodels", "pingouin",
    "sklearn", "matplotlib", "seaborn", "lifelines",
    "rpy2", "csv", "json", "math", "statistics",
}

STAT_TEST_TABLE = """\
| Situation | Recommended test |
|---|---|
| 2 independent groups, normal distribution | Independent t-test |
| 2 independent groups, non-normal / small n | Mann-Whitney U |
| 2 paired groups, normal | Paired t-test |
| 2 paired groups, non-normal | Wilcoxon signed-rank |
| 3+ independent groups, normal | One-way ANOVA + post-hoc (Tukey) |
| 3+ groups, non-normal | Kruskal-Wallis + Dunn |
| Continuous association | Pearson (normal) or Spearman (non-normal) |
| Categorical outcomes | Chi-square (n≥5/cell) or Fisher's exact |
| Binary outcome prediction | Logistic regression |
| Survival / time-to-event | Kaplan-Meier + log-rank; Cox PH for covariates |
| Multiple linear predictors | Multiple regression |
| Repeated measures | Repeated-measures ANOVA or mixed-effects |
"""

APA_FORMAT = """\
APA reporting format (required):
  t-test:      t(df) = X.XX, p = .XXX, d = X.XX [95% CI: X.XX, X.XX]
  ANOVA:       F(df1, df2) = X.XX, p = .XXX, η² = .XX
  Correlation: r(df) = .XX, p = .XXX [95% CI: .XX, .XX]
  Chi-square:  χ²(df, N = XXX) = X.XX, p = .XXX
  Mann-Whitney: U = XXX, p = .XXX, r = .XX (effect size)
"""


# ──────────────────────────────────────────────────────────────────────────────
# Code execution
# ──────────────────────────────────────────────────────────────────────────────

class CodeRunResult:
    """Result of running analysis code."""

    def __init__(self, stdout: str, stderr: str, returncode: int, code_path: Path):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.code_path = code_path
        self.success = returncode == 0

    @property
    def combined_output(self) -> str:
        parts = []
        if self.stdout.strip():
            parts.append(self.stdout)
        if self.stderr.strip():
            parts.append(f"[stderr]\n{self.stderr}")
        return "\n".join(parts) if parts else "(no output)"

    def __repr__(self) -> str:
        status = "OK" if self.success else f"ERROR (rc={self.returncode})"
        return f"CodeRunResult({status}, {len(self.stdout)} chars stdout)"


def run_python_code(code: str, data_dir: Path, output_dir: Path, timeout: int = 120) -> CodeRunResult:
    """
    Execute Python analysis code in a subprocess.

    The code is written to a temp file, run with the current Python interpreter,
    with cwd set to data_dir so relative file paths work.
    stdout/stderr are captured.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    code_path = output_dir / "analysis_code.py"
    code_path.write_text(code, encoding="utf-8")

    try:
        result = subprocess.run(
            [sys.executable, str(code_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(data_dir),
        )
        return CodeRunResult(result.stdout, result.stderr, result.returncode, code_path)
    except subprocess.TimeoutExpired:
        return CodeRunResult("", f"Timeout after {timeout}s", 1, code_path)
    except Exception as e:
        return CodeRunResult("", str(e), 1, code_path)


def run_r_code(code: str, data_dir: Path, output_dir: Path, timeout: int = 180) -> CodeRunResult:
    """
    Execute R analysis code via Rscript.
    Falls back gracefully if R is not installed.
    """
    import shutil
    rscript = shutil.which("Rscript")
    if rscript is None:
        return CodeRunResult(
            "", "Rscript not found — install R or use Python code.", 1,
            output_dir / "analysis_code.R"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    code_path = output_dir / "analysis_code.R"
    code_path.write_text(code, encoding="utf-8")

    try:
        result = subprocess.run(
            [rscript, str(code_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(data_dir),
        )
        return CodeRunResult(result.stdout, result.stderr, result.returncode, code_path)
    except subprocess.TimeoutExpired:
        return CodeRunResult("", f"Timeout after {timeout}s", 1, code_path)
    except Exception as e:
        return CodeRunResult("", str(e), 1, code_path)


# ──────────────────────────────────────────────────────────────────────────────
# Data exploration
# ──────────────────────────────────────────────────────────────────────────────

def explore_data_file(path: Path) -> dict:
    """
    Quick inspection of a CSV or Excel file.
    Returns a dict with shape, dtypes, missingness, per-column stats.
    Requires pandas; returns an error dict if not installed.
    """
    try:
        import pandas as pd
    except ImportError:
        return {"error": "pandas not installed — run: pip install pandas"}

    try:
        if path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
    except Exception as e:
        return {"error": f"Could not read {path.name}: {e}"}

    info: dict = {
        "file": path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing": {col: int(df[col].isna().sum()) for col in df.columns},
    }

    # Per-column basic stats
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        desc = df[numeric_cols].describe()
        info["numeric_summary"] = desc.round(4).to_dict()

    # Categorical summaries
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        info["categorical_summary"] = {
            col: df[col].value_counts().head(10).to_dict() for col in cat_cols
        }

    return info


def format_data_exploration(info: dict) -> str:
    """Format explore_data_file() output as a readable Markdown block."""
    if "error" in info:
        return f"**Error:** {info['error']}"

    lines = [
        f"**File:** {info['file']}",
        f"**Shape:** {info['rows']} rows × {info['columns']} columns",
        "",
        "**Columns:**",
    ]
    for col in info["column_names"]:
        dtype = info["dtypes"].get(col, "?")
        n_miss = info["missing"].get(col, 0)
        miss_str = f" ({n_miss} missing)" if n_miss > 0 else ""
        lines.append(f"  - `{col}` ({dtype}){miss_str}")

    if "numeric_summary" in info:
        lines.append("\n**Numeric summary (mean ± SD, min–max):**")
        for col, stats in info["numeric_summary"].items():
            mean = stats.get("mean", "?")
            std = stats.get("std", "?")
            mn = stats.get("min", "?")
            mx = stats.get("max", "?")
            lines.append(f"  - `{col}`: mean={mean}, SD={std}, range=[{mn}, {mx}]")

    if "categorical_summary" in info:
        lines.append("\n**Categorical value counts:**")
        for col, counts in info["categorical_summary"].items():
            top = ", ".join(f"{k}: {v}" for k, v in list(counts.items())[:5])
            lines.append(f"  - `{col}`: {top}")

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Assumption checking helpers
# ──────────────────────────────────────────────────────────────────────────────

def generate_assumption_check_code(df_var: str, group_col: str, value_col: str) -> str:
    """
    Generate Python code that checks normality (Shapiro-Wilk) and variance
    homogeneity (Levene's) for a two-group comparison.
    """
    # Build code as list of lines to avoid f-string/format brace conflicts
    lines = [
        "import pandas as pd",
        "from scipy import stats",
        "",
        "# Load your data — adjust path as needed",
        "# df = pd.read_csv('your_data.csv')",
        "",
        f"groups = {df_var}['{group_col}'].unique()",
        'print(f"Groups: {groups}")',
        "",
        f"group_data = [",
        f"    {df_var}.loc[{df_var}['{group_col}'] == g, '{value_col}'].dropna().values",
        "    for g in groups",
        "]",
        "",
        'print("\\n--- Normality (Shapiro-Wilk) ---")',
        "for g, data in zip(groups, group_data):",
        "    if len(data) < 3:",
        '        print(f"Group {g}: n={len(data)} — too small for Shapiro-Wilk")',
        "    else:",
        "        stat, p = stats.shapiro(data)",
        '        normal = "(normal)" if p > 0.05 else "(NON-NORMAL)"',
        '        print(f"Group {g}: W={stat:.4f}, p={p:.4f} {normal}")',
        "",
        'print("\\n--- Variance homogeneity (Levene\'s) ---")',
        "lev_stat, lev_p = stats.levene(*group_data)",
        "equal = '(equal variances)' if lev_p > 0.05 else '(UNEQUAL variances)'",
        'print(f"Levene: F={lev_stat:.4f}, p={lev_p:.4f} {equal}")',
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint 1A: analysis proposal formatting
# ──────────────────────────────────────────────────────────────────────────────

def format_cp1a_proposal(
    data_summary: str,
    comparisons: list[dict],
) -> str:
    """
    Format the CP 1A output that Claude presents to the researcher.

    comparisons: list of dicts with keys:
        comparison (str), test (str), rationale (str), expected_output (str)
    """
    lines = [
        "## Data Exploration Summary",
        "",
        data_summary,
        "",
        "## Proposed Statistical Plan",
        "",
        "The following analyses are proposed based on the data structure and research topic.",
        "Each comparison is grounded in the data — no exploratory analyses added without justification.",
        "",
    ]

    for i, comp in enumerate(comparisons, 1):
        lines += [
            f"### Comparison {i}: {comp.get('comparison', '')}",
            f"- **Test:** {comp.get('test', '')}",
            f"- **Rationale:** {comp.get('rationale', '')}",
            f"- **Expected output:** {comp.get('expected_output', '')}",
            "",
        ]

    lines += [
        "## Statistical Test Reference",
        "",
        STAT_TEST_TABLE,
        "",
        APA_FORMAT,
        "",
        "---",
        "✓ **CHECKPOINT 1A** — Approve statistical approach?",
        "`[OK]` to proceed with code generation  |  `[REVISE: ...]` to change approach  |  `[REDIRECT: ...]`",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint 1B: interpretation formatting
# ──────────────────────────────────────────────────────────────────────────────

def format_cp1b_interpretation(
    results_text: str,
    interpretation: str,
    story_writer_summary: list[str],
) -> str:
    """
    Format the CP 1B output: results + interpretation + summary for Story Writer.

    story_writer_summary: 3-5 bullets rating each finding
        e.g. ["Primary outcome (X vs Y): STRONG — p=.004, d=0.72",
               "Secondary outcome (A vs B): WEAK — p=.13, d=0.21"]
    """
    lines = [
        "## Statistical Results",
        "",
        results_text,
        "",
        "## Interpretation",
        "",
        interpretation,
        "",
        "## Summary for Story Writer",
        "",
        "Rating scale: STRONG (d>0.5, p<.05) | MODERATE (d=0.2–0.5, p<.05) | WEAK (p>.05 or d<0.2) | NULL",
        "",
    ]

    for bullet in story_writer_summary:
        lines.append(f"- {bullet}")

    lines += [
        "",
        "---",
        "✓ **CHECKPOINT 1B** — Approve results & interpretation?",
        "`[OK]` to proceed to visualization  |  `[REVISE: ...]`  |  `[REDIRECT: ...]`",
        "",
        "> Next step: Stage 1-B — Visualization (figure planning)",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Session integration
# ──────────────────────────────────────────────────────────────────────────────

def save_analysis_to_session(
    session: "ARSession",
    ws: "WorkSpace",
    *,
    plan_text: str = "",
    code: str = "",
    code_language: str = "python",
    run_result: "CodeRunResult | None" = None,
    interpretation_text: str = "",
    analysis_summary_bullets: list[str] | None = None,
) -> None:
    """
    Persist all Stage 1-A artifacts to the workspace and session.

    Call this after CP 1B is cleared.
    """
    if plan_text:
        ws.save_analysis_plan(plan_text)
    if code:
        ws.save_analysis_code(code, code_language)
    if run_result is not None:
        ws.save_analysis_results(run_result.combined_output)
    if interpretation_text:
        ws.save_interpretation(interpretation_text)
    if analysis_summary_bullets:
        session.analysis_summary = "\n".join(f"- {b}" for b in analysis_summary_bullets)
    session.save()
