---
name: data-analysis
description: >
  Biomedical data analysis: explore data, check assumptions, propose and execute
  statistical tests, and interpret results. Use when the user provides raw data
  (CSV, Excel) or analysis results and needs statistical analysis before writing.
  Triggers on: "analyze data", "run statistics", "check significance", "what test",
  "Stage 1", or when raw data files are present at session start.
metadata:
  category: experiment
  trigger-keywords: "data,statistics,analysis,p-value,test,normality,effect size,ANOVA,regression,correlation,Stage 1"
  applicable-stages: "1"
  priority: "1"
  version: "1.0"
  author: autoresearch
  references: "adapted from statistical-reporting skill (AutoResearchClaw)"
---

# Data Analysis

Run Stage 1-A of the AutoResearch pipeline.
**Do not proceed to visualization until CP 1B is cleared.**

## Step 1 — Explore & Propose (no code yet)

1. Load and inspect data: shape, column types, group labels, sample sizes per group
2. Report missingness: count and pattern per variable
3. Describe distributions: mean, median, SD, range per group
4. Check statistical assumptions:
   - Normality: Shapiro-Wilk (n < 50) or describe Q-Q plot shape (n ≥ 50)
   - Variance homogeneity: Levene's test when comparing groups
   - Independence: confirm from study design
5. Map each comparison to the research hypothesis — do not propose analyses
   just because the data allows them
6. For each comparison, state: test name, rationale, expected output format

### ✓ CHECKPOINT 1A
Present the analysis plan. Wait for `[OK]` / `[REVISE: ...]` / `[REDIRECT: ...]`.
**Do not generate or run any code until confirmed.**

## Step 2 — Execute

1. Generate Python and/or R code:
   - Python: `pandas`, `scipy`, `statsmodels`, `pingouin`
   - R: base stats, `rstatix`, `car`
2. Run via Claude Code sandbox
3. Capture all outputs: summary tables, test statistics, raw results
4. If a test fails or produces unexpected results: report honestly, propose alternative,
   do not silently substitute

## Step 3 — Interpret

For every result, report ALL of the following:
1. Test used and why
2. Exact test statistic and degrees of freedom
3. Exact p-value (never "p < 0.05")
4. Effect size with 95% CI (Cohen's d / η² / OR / HR as appropriate)
5. Plain-language summary (1–2 sentences)
6. Explicitly state: statistical significance vs. biological/clinical significance

Flag explicitly:
- Assumption violations and their impact on interpretation
- Small sample size caveats
- Multiple comparisons (apply Bonferroni or FDR if applicable)
- What the analysis does NOT show
- Alternative explanations not ruled out by the data

End with **Summary for Story Writer**: 3–5 bullets rating each finding
as strong / moderate / weak / null, for use in narrative design.

### ✓ CHECKPOINT 1B
Present interpretation. Wait for `[OK]` / `[REVISE: ...]` / `[REDIRECT: ...]`.
Do not proceed to visualization until confirmed.

## Statistical Test Selection Reference

| Situation | Test |
|---|---|
| 2 independent groups, normal | Independent t-test |
| 2 independent groups, non-normal | Mann-Whitney U |
| 2 paired groups, normal | Paired t-test |
| 2 paired groups, non-normal | Wilcoxon signed-rank |
| 3+ independent groups, normal | One-way ANOVA + post-hoc |
| 3+ groups, non-normal | Kruskal-Wallis |
| Continuous association | Pearson or Spearman |
| Categorical outcomes | Chi-square or Fisher's exact |
| Binary outcome prediction | Logistic regression |
| Survival / time-to-event | Cox proportional hazards |

## APA Reporting Format

- t-test: `t(df) = X.XX, p = .XXX, d = X.XX [95% CI: X.XX, X.XX]`
- ANOVA: `F(df1, df2) = X.XX, p = .XXX, η² = .XX`
- Correlation: `r(df) = .XX, p = .XXX [95% CI: .XX, .XX]`
- Chi-square: `χ²(df, N = XXX) = X.XX, p = .XXX`

## Common Pitfalls

1. Never say "no effect" from a non-significant result — report power or CI instead
2. Never omit effect sizes — they are mandatory alongside p-values
3. Never round exact p-values to "p < 0.05"
4. Do not run code before CP 1A is cleared
5. Do not fetch comparison data from GEO, TCGA, or any database — user provides it
6. If pre-approved test fails, surface it before substituting
