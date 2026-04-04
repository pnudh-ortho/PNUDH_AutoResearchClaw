---
name: visualization
description: >
  Publication-quality scientific figure generation for biomedical research.
  Proposes figure types by reasoning from the data, then generates annotated
  Python or R code. Use after data analysis (Stage 1-A) is confirmed complete.
  Triggers on: "make figures", "plot", "visualization", "Stage 1-B",
  or when CP 1B has been cleared in the current session.
metadata:
  category: writing
  trigger-keywords: "figure,plot,visualization,chart,graph,matplotlib,ggplot,publication,kaplan,ROC,volcano,heatmap"
  applicable-stages: "1"
  priority: "1"
  version: "1.0"
  author: autoresearch
  references: "adapted from scientific-visualization skill (AutoResearchClaw)"
---

# Visualization

Run Stage 1-B of the AutoResearch pipeline.
**Start only after CP 1B (data analysis interpretation) is cleared.**

## Step 1 — Reason & Propose

For each key finding from the analysis report, reason through:

1. **Data type**: continuous / categorical / ordinal / survival / expression
2. **Comparison structure**:
   - 2 groups → box/violin + individual points + significance bar
   - 3+ groups → grouped or faceted
   - Correlation → scatter + regression line
   - Over time → line plot
   - Survival → Kaplan-Meier
   - Diagnostic performance → ROC
   - Effect across subgroups → Forest plot
   - Differential expression → Volcano plot
   - Expression patterns → Heatmap
   - Multi-dimensional OMICS → composite multi-panel
3. **Sample size**: if n < 10 per group, individual data points are mandatory
4. **Reader priority**: the key finding must be visually obvious without reading the caption

Propose 1–2 candidate figure types per finding with explicit rationale.
Note which specialized library (if any) is required.

### ✓ CHECKPOINT 1C
Present figure plan. AI proposes, user decides.
Wait for `[OK]` / `[REVISE: ...]` / `[DIFFERENT TYPE: ...]` per figure.
Do not generate code until confirmed.

## Step 2 — Generate Code

**Base stack (always start here):**
```
Python: scienceplots + matplotlib + seaborn + pandas + numpy
R:      ggplot2 + tidyverse + ggpubr + ggsci
```

**Extend only when required:**
| Figure type | Python lib | R lib |
|---|---|---|
| Kaplan-Meier | `lifelines` | `survival` + `survminer` |
| ROC curve | `sklearn.metrics` | `pROC` |
| Forest plot | `forestplot` | `forestploter` / `meta` |
| Volcano plot | `matplotlib` custom | `EnhancedVolcano` |
| Complex heatmap | `PyComplexHeatmap` | `ComplexHeatmap` |
| OMICS multi-panel | `scanpy` + `anndata` | `Seurat` |
| Label adjustment | `adjustText` | `ggrepel` |

**Code principles:**
1. One script per figure (or combined notebook if preferred)
2. Configuration block at top: colors, font sizes, figure dimensions, DPI
3. Use colorblind-safe palettes (ColorBrewer, Okabe-Ito, viridis, ggsci journal palettes)
4. Export: PDF/SVG (vector) + PNG at 300 DPI minimum
5. Panel labels (A, B, C…) in bold, top-left corner, handled automatically
6. All text ≥ 8pt at final print size
7. Error bars: specify type explicitly (SEM / SD / 95% CI) in both code and caption
8. Significance annotations: exact p-values when space allows; NS for non-significant

**Journal figure sizing:**
- Single column: 3.3–3.5 inches (85–89 mm) wide
- 1.5 column: 4.5–5.5 inches (114–140 mm)
- Full width: 6.5–7.1 inches (165–180 mm)

## Step 3 — Draft Captions

Format:
```
Figure N. [Bold title — what the figure shows, not the finding].
[Methods note: n per group, statistical test used, error bar type].
[Key finding sentence]. [(A) panel description. (B) panel description.]
Abbreviations: [if any].
```

Example:
```
Figure 2. Survival outcomes by treatment group.
Kaplan-Meier curves for Treatment A (n=45) vs. Control (n=43). Log-rank test.
Shaded areas = 95% CI. Treatment A showed significantly improved overall survival
(median OS 18.3 vs. 11.2 months, HR = 0.61 [95% CI: 0.41–0.91], p = .015).
```

## Common Pitfalls

1. Never use pie charts for group comparisons — use bar or box instead
2. Never use 3D charts — they distort data perception
3. Never use rainbow colormaps (jet, rainbow) — use perceptually uniform alternatives
4. Never use bar charts for n < 10 per group without individual points
5. Always show uncertainty — error bars, confidence bands, or individual points
6. Never omit significance annotation when a statistical comparison was made
7. Code must run as-is — no placeholder values, no "replace with your data" stubs
