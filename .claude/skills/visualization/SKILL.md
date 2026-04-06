---
name: visualization
description: >
  Publication-quality scientific figure generation for AutoResearch Stage 1-C.
  Reasons from confirmed analysis results to propose figure types, generates
  complete annotated code (Python or R), executes scripts, and drafts captions.
  Starts only after CP 1B is cleared.
  Triggers on: "make figures", "plot", "visualize", "Stage 1-C", "figure plan",
  or when CP 1B has been cleared in the current session.
metadata:
  category: visualization
  trigger-keywords: "figure,plot,visualization,chart,graph,matplotlib,ggplot,publication,kaplan,ROC,volcano,heatmap,forest,boxplot,scatter"
  applicable-stages: "1"
  priority: "1"
  version: "2.0"
  author: autoresearch
---

# Visualization — Stage 1-C

**Translate confirmed statistical results into publication-quality figures.
Propose first, code after CP 1C approval. Every figure must make the key finding
visually obvious without reading the caption.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — confirm CP 1B is cleared.
2. Read `sessions/[id]/stage1/analysis/interpretation.md` — the confirmed findings.
3. Read `sessions/[id]/stage1/analysis/analysis_results.txt` — raw output for exact values.
4. Note the "Summary for Story Writer" table — it lists each finding and its strength rating.
5. Check `sessions/[id]/stage1/figures/` — note any existing figure files already present.

---

## Step 1 — Reason Through Figure Types

For each key finding from the analysis report, work through this decision tree:

### 1.1 Data Type Assessment

| Data type | Primary encoding |
|---|---|
| Continuous, 2 groups | Distribution comparison (box, violin, or individual points) |
| Continuous, 3+ groups | Multi-group distribution or faceted plot |
| Continuous × continuous | Scatter plot with regression line |
| Binary outcome × predictor | ROC curve, forest plot |
| Time-to-event | Kaplan-Meier curve |
| Proportions / counts | Bar chart (not pie) |
| Differential expression | Volcano plot |
| Expression patterns across samples | Heatmap |
| Effect sizes across subgroups | Forest plot |
| High-dimensional multi-omics | Composite multi-panel (UMAP, heatmap, violin) |

### 1.2 Sample Size Rule (non-negotiable)

**If n < 10 per group: individual data points are MANDATORY on every figure.**
- Use jittered strip plot, beeswarm, or overlaid dots on box/violin
- Bars alone are not acceptable for small samples
- Rationale: bars hide data distribution; n < 10 makes each point scientifically relevant

### 1.3 Figure Type Selection Guide

**Two independent groups, continuous outcome:**
- n ≥ 10 per group: Violin plot + box overlay + median line — shows full distribution
- n < 10 per group: Dot plot (individual points) + mean ± SD bar — shows every data point
- Add significance bar with exact p-value

**Three or more groups:**
- Grouped box plot (side-by-side, one color per group)
- Post-hoc significance: bracket annotations only for significant comparisons
- Color palette: one hue per group, colorblind-safe

**Correlation / two continuous variables:**
- Scatter plot + regression line + 95% confidence band
- Report r, p, and n in the figure or caption
- If n > 200: use density hexbin + marginal histograms

**Survival / time-to-event:**
- Kaplan-Meier curve — one curve per group, distinct colors
- Number-at-risk table below x-axis (mandatory for clinical data)
- Censoring marks: vertical tick marks on curves
- Log-rank p-value in plot area; HR [95% CI] in caption or legend

**Diagnostic accuracy:**
- ROC curve — AUC ± 95% CI labeled
- Reference diagonal (chance line) at y = x
- If comparing multiple classifiers: overlay on same axes

**Effect sizes across subgroups:**
- Horizontal forest plot
- Point estimate + 95% CI for each subgroup
- Vertical dashed line at null value (OR = 1, d = 0, etc.)
- Overall estimate at bottom, visually separated

**Differential expression:**
- Volcano plot: log₂(FC) on x, −log₁₀(p) on y
- Color: upregulated (red), downregulated (blue), non-significant (grey)
- Label top N hits by name (use `adjustText` / `ggrepel`)
- Threshold lines: significance cutoff and fold-change cutoff

**Expression patterns:**
- Heatmap with hierarchical clustering (rows = features, columns = samples)
- Row and column dendrograms
- Color: diverging palette (blue-white-red for expression; never rainbow)
- Annotate columns with clinical variables

### 1.4 Figure Combination Principle

- Maximum 4 panels per figure
- Panel labels: bold uppercase (A, B, C, D), top-left corner of each panel
- Logical grouping: panels in one figure should tell one coherent sub-story
- Do not combine unrelated analyses into one figure for space efficiency

---

### ✓ CHECKPOINT 1C

Present figure plan. For each proposed figure:

```
## Figure Plan — CP 1C

### Figure 1: [Key finding description]
- **Finding:** [One sentence from analysis results]
- **Data type:** [Continuous / Survival / Categorical / etc.]
- **n per group:** [X] — [individual points required / not required]
- **Proposed type (Option A):** [Figure type]
  Rationale: [Why this type best communicates the finding]
  Library: [Python: seaborn + matplotlib | R: ggplot2 + ggpubr]
- **Alternative (Option B):** [Alternative type, if any]
  Rationale: [When Option B would be preferable]

### Figure 2: ...

---
✓ CHECKPOINT 1C — Approve figure plan?
For each figure: [OK A] / [OK B] / [DIFFERENT TYPE: ...]
When all confirmed: [ALL OK] → code generation begins.
```

**STOP. Do not write any code until researcher responds.**

---

## Step 2 — Generate Code

### 2.1 Library Stack

**Always start with the base stack:**

Python:
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
import scienceplots  # pip install SciencePlots
plt.style.use(["science", "nature"])
```

R:
```r
library(ggplot2)
library(tidyverse)
library(ggpubr)
library(ggsci)       # journal color palettes
library(ggrepel)     # label placement
```

**Add specialist libraries only when the figure type requires:**

| Figure type | Python | R |
|---|---|---|
| Kaplan-Meier | `lifelines` | `survival` + `survminer` |
| ROC curve | `sklearn.metrics` | `pROC` |
| Forest plot | `forestplot` | `forestploter` / `meta` |
| Volcano plot | `matplotlib` (custom) | `EnhancedVolcano` |
| Complex heatmap | `PyComplexHeatmap` | `ComplexHeatmap` |
| OMICS multi-panel | `scanpy` + `anndata` | `Seurat` |
| Beeswarm / dot | `seaborn.stripplot` | `ggbeeswarm` |
| Label adjustment | `adjustText` | `ggrepel` |

### 2.2 Code Structure Requirements

Every figure script must follow this structure:

```python
"""
Figure [N]: [Description]
AutoResearch Session: [session_id]
CP 1C approved: [date]
"""

# ══════════════════════════════════════════════
# CONFIGURATION — modify these to adjust output
# ══════════════════════════════════════════════
COLORS = {
    "group_a": "#0077BB",   # colorblind-safe blue
    "group_b": "#EE7733",   # colorblind-safe orange
    "sig":     "#CC3311",   # significance annotation
    "ns":      "#AAAAAA",   # non-significant
}
FONT_SIZE_TITLE   = 10
FONT_SIZE_AXIS    = 9
FONT_SIZE_TICK    = 8
FONT_SIZE_ANNOT   = 8
FIG_W             = 3.5     # inches — single column (3.5) / 1.5-col (5.0) / full (7.0)
FIG_H             = 4.0
DPI               = 300

# ══════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════
import pandas as pd
df = pd.read_csv("../../input/patient_data.csv")

# ══════════════════════════════════════════════
# FIGURE
# ══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))

# ... plotting code ...

# ══════════════════════════════════════════════
# FORMATTING
# ══════════════════════════════════════════════
ax.set_xlabel("X Label (units)", fontsize=FONT_SIZE_AXIS)
ax.set_ylabel("Y Label (units)", fontsize=FONT_SIZE_AXIS)
ax.tick_params(labelsize=FONT_SIZE_TICK)
ax.spines[["top","right"]].set_visible(False)  # clean axes

# ══════════════════════════════════════════════
# EXPORT
# ══════════════════════════════════════════════
plt.tight_layout()
plt.savefig("fig[N]_[name].pdf", dpi=DPI, bbox_inches="tight")
plt.savefig("fig[N]_[name].png", dpi=DPI, bbox_inches="tight")
plt.close()
print("Figure saved.")
```

### 2.3 Color Palette Requirements

**Default: Okabe-Ito (fully colorblind-safe):**
```python
OKABE_ITO = {
    "orange":       "#E69F00",
    "sky_blue":     "#56B4E9",
    "green":        "#009E73",
    "yellow":       "#F0E442",
    "blue":         "#0072B2",
    "vermillion":   "#D55E00",
    "pink":         "#CC79A7",
    "black":        "#000000",
}
```

**Journal palettes (use ggsci in R, or manually in Python):**
- `nejm_pal()` — NEJM style (8 colors)
- `lancet_pal()` — Lancet style
- `jco_pal()` — Journal of Clinical Oncology

**Never use:** jet, rainbow, hsv, spectral — perceptually non-uniform and inaccessible.
**Never use:** red/green together as primary distinction — ~8% of males are red-green color blind.

### 2.4 Figure Sizing Standards

| Journal column | Width (inches) | Width (mm) |
|---|---|---|
| Single column | 3.3–3.5 | 85–89 |
| 1.5 column | 4.5–5.5 | 114–140 |
| Full width | 6.5–7.1 | 165–180 |
| Supplementary | up to 7.5 | 190 |

Default to single column unless figure complexity requires wider format.

### 2.5 Text Size Requirements

All text in a figure must be ≥ 8pt at the final print size. If using 3.5-inch single-column:
- Axis labels: 9–10pt
- Tick labels: 8–9pt
- Annotations: 8pt minimum
- Legend text: 8–9pt

### 2.6 Error Bars — Mandatory Specification

Always specify error bar type explicitly in code and caption:
- **SEM**: shows precision of the mean estimate (appropriate when comparing means)
- **SD**: shows spread of raw data (appropriate when describing population variability)
- **95% CI**: shows inference interval (preferred for between-group comparisons)

```python
# Example: 95% CI error bars
from scipy import stats
means = df.groupby("group")["outcome"].mean()
sems = df.groupby("group")["outcome"].sem()
ci95 = sems * stats.t.ppf(0.975, df.groupby("group")["outcome"].count() - 1)
ax.errorbar(x, means, yerr=ci95, fmt='none', color='black', capsize=4,
            label='95% CI')
```

### 2.7 Statistical Annotations

- Exact p-value when space allows: `p = .034`
- Use bracket + p-value for group comparisons
- "ns" only for non-significant results (p ≥ .05)
- Never use asterisk coding alone (*, **, ***) without defining in caption

---

## Step 3 — Execute Figure Scripts

```bash
cd sessions/[id]/stage1/figures
python fig1_[name].py
```

Report for each figure:
- Success / failure with stdout and stderr
- Output files generated (PDF, PNG paths)
- Any warnings (e.g., missing data points excluded)

---

## Step 4 — Draft Captions

**Caption format (strict):**

```
Figure [N]. [Bold title — describes WHAT is shown, not the finding].
[Methods note: sample sizes per group, statistical test, error bar type].
[Key finding sentence — states the result with statistics].
[(A) [panel description]. (B) [panel description].] [only if multi-panel]
[Abbreviations: list only those used in the figure itself.]
```

**Example (Good):**
```
Figure 2. Serum biomarker levels by treatment group.
Box plots show median (center line), IQR (box), and 1.5×IQR (whiskers) for
Treatment A (n=45) and Control (n=43). Individual data points overlaid.
Mann-Whitney U test. Treatment A showed significantly lower biomarker Z
(median 12.3 vs. 18.7 ng/mL, U = 623, p = .008, r = 0.42 [95% CI: 0.18, 0.62]).
Abbreviations: IQR, interquartile range.
```

**Example (Bad — do not do this):**
```
Figure 2. Results of biomarker analysis.
The figure shows that treatment is better.
```

---

## Self-Check Before Presenting

- [ ] Every figure has been executed and produces output files
- [ ] All text is ≥ 8pt at final print size
- [ ] Colorblind-safe palette used throughout
- [ ] n < 10 groups have individual data points
- [ ] Error bars are specified (type stated in code and caption)
- [ ] Statistical annotations use exact p-values or "ns"
- [ ] Panel labels (A, B, C) are present and bold
- [ ] Both PDF (vector) and PNG (raster) files exported
- [ ] Caption follows the required format
- [ ] Figures saved to `sessions/[id]/stage1/figures/`

---

## Hard Rules

1. **NEVER generate code before CP 1C is cleared**
2. **NEVER use pie charts** for group comparisons — use bar or box
3. **NEVER use 3D charts** — they distort data
4. **NEVER use rainbow/jet colormaps** — use perceptually uniform alternatives
5. **NEVER use bars alone for n < 10** — individual points are mandatory
6. **NEVER omit error bars** when a distribution or uncertainty exists
7. **NEVER omit significance annotation** when a statistical comparison was made
8. **Code must run as-is** — no placeholder values, no "replace with your data" stubs
