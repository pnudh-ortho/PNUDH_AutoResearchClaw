---
name: data-analysis
description: >
  Biomedical data analysis for AutoResearch Stage 1-A and 1-B.
  Explores raw data, checks statistical assumptions, proposes the appropriate
  test battery, executes approved analysis code, runs post-hoc power analysis,
  and produces a structured interpretation summary for the Story Writer.
  Triggers on: "analyze data", "run statistics", "Stage 1", "what test should I use",
  "check significance", "explore my data", or when raw data files are present in the session.
metadata:
  category: analysis
  trigger-keywords: "data,statistics,analysis,p-value,normality,test,ANOVA,regression,correlation,effect size,Stage 1,explore"
  applicable-stages: "1"
  priority: "1"
  version: "2.0"
  author: autoresearch
---

# Data Analysis — Stage 1-A / 1-B

**Produce rigorous, reproducible statistical analysis grounded in the data actually provided.
Never run code before CP 1A is cleared. Never report "p < 0.05" — always exact values.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — note current session ID and workspace path.
2. List files in `sessions/[id]/input/` — identify all data files.
3. Read `sessions/[id]/input/README.md` if present — note researcher's study description.
4. If `sessions/[id]/stage1/analysis/analysis_results.txt` already exists, skip to Step 3 (Interpret).

---

## Step 1 — Explore & Propose  *(no code runs until CP 1A)*

### 1.1 Load and Inspect

For each data file found in input/:

```python
import pandas as pd
df = pd.read_csv("path/to/file.csv")  # or read_excel for .xlsx

print(df.shape)          # (rows, columns)
print(df.dtypes)         # column types
print(df.head())         # first 5 rows
print(df.describe())     # basic statistics
print(df.isnull().sum()) # missing values per column
```

Report:
- Dataset dimensions (rows × columns)
- Variable names and types (continuous, categorical, ordinal, binary, time-to-event)
- Group variable(s) and sample sizes per group
- Missing data: count and percentage per variable; note if missingness is systematic

### 1.2 Describe Distributions

For every numeric variable, per group:
- Mean ± SD (if approximately normal)
- Median [IQR] (if skewed or non-normal)
- Min–Max range
- Visual description: "right-skewed", "approximately symmetric", "bimodal"

### 1.3 Check Statistical Assumptions

**Normality** (required before any parametric test):
- n < 50 per group: Shapiro-Wilk test (`scipy.stats.shapiro` or `shapiro.test()` in R)
  - W statistic and exact p-value required
  - p < .05 indicates departure from normality
- n ≥ 50 per group: describe Q-Q plot pattern; Shapiro-Wilk loses power at large n

**Variance Homogeneity** (required for independent group comparisons):
- Levene's test (`scipy.stats.levene` or `car::leveneTest()` in R)
- Report: F statistic, df, exact p-value
- p < .05 indicates heterogeneous variances → use Welch correction or non-parametric

**Independence**:
- Confirm from study design (not tested statistically)
- State explicitly: "Observations are independent based on [study design feature]"
- If repeated measures / matched pairs: identify paired structure

### 1.4 Designate Primary vs. Secondary Outcomes

At this stage, before any code runs:
- **Primary outcome**: the single main research question. All power calculations reference this.
- **Secondary outcomes**: list in order of scientific priority.
- **Exploratory analyses**: clearly labeled as hypothesis-generating, not confirmatory.

If the researcher has not specified, ask: "Which variable is the primary outcome for this study?"
Do not proceed without this designation — it determines the multiple comparisons correction strategy.

### 1.5 Multiple Comparisons Planning

If ≥ 2 statistical tests will be run:
- State the correction method upfront, before seeing results.
- Options: Bonferroni (conservative), Benjamini-Hochberg FDR (less conservative for exploratory), none with explicit justification.
- Rule: if primary outcome is pre-specified and tests are independent, Bonferroni on secondary outcomes only is acceptable. State the rationale.

### 1.6 Test Selection

For each comparison, map to the appropriate test using this matrix:

| Data structure | Distribution | Recommended test |
|---|---|---|
| 2 independent groups | Normal, equal variance | Independent-samples t-test |
| 2 independent groups | Normal, unequal variance | Welch's t-test |
| 2 independent groups | Non-normal or small n | Mann-Whitney U |
| 2 paired/matched groups | Normal | Paired t-test |
| 2 paired/matched groups | Non-normal | Wilcoxon signed-rank |
| 3+ independent groups | Normal, equal variance | One-way ANOVA + Tukey HSD post-hoc |
| 3+ independent groups | Non-normal | Kruskal-Wallis + Dunn post-hoc (Bonferroni-adjusted) |
| 3+ repeated measures | Normal | Repeated-measures ANOVA + Bonferroni |
| 3+ repeated measures | Non-normal | Friedman test |
| 2 continuous variables | Linear association | Pearson r |
| 2 continuous variables | Monotonic, non-normal | Spearman ρ |
| Binary outcome, independent predictor | — | Logistic regression |
| Time-to-event | — | Kaplan-Meier + log-rank; Cox proportional hazards for multivariate |
| Categorical × categorical | Expected cell count ≥ 5 | Chi-square (χ²) |
| Categorical × categorical | Expected cell count < 5 | Fisher's exact |
| Diagnostic accuracy | — | AUC-ROC, sensitivity, specificity, PPV, NPV with 95% CI |

**Important**: Do not propose a test just because the data allows it. Every proposed test must be justified by the research question.

---

### ✓ CHECKPOINT 1A

Present the full analysis plan:
1. Dataset summary (shape, variables, missing data)
2. Distribution and assumption findings
3. Primary outcome designation
4. Full list of proposed tests with rationale
5. Multiple comparisons correction strategy

**Format:**
```
## Analysis Plan — CP 1A

**Dataset:** [N] observations, [K] variables
**Groups:** [Group A] (n=[X]), [Group B] (n=[Y])
**Primary outcome:** [variable name]

**Assumption check results:**
- Normality (Shapiro-Wilk): [Group A] W=[X.XX], p=[.XXX]; [Group B] W=[X.XX], p=[.XXX]
- Variance homogeneity (Levene's): F([df1],[df2])=[X.XX], p=[.XXX]

**Proposed tests:**
1. [Primary outcome] — [Test name] — Rationale: [one sentence]
2. [Secondary outcome 1] — [Test name] — Rationale: [one sentence]

**Multiple comparisons:** [method + justification]

---
✓ CHECKPOINT 1A — Approve statistical approach?
[OK] / [REVISE: ...] / [REDIRECT: ...]
```

**STOP. Do not generate or run any code until the researcher responds with [OK].**

---

## Step 2 — Execute

### 2.1 Generate Code

After CP 1A approval, write analysis code with these requirements:
- One script total: `analysis_code.py` or `analysis_code.R`
- Header comment block: analysis date, session ID, approved tests, data file path
- Import section at top; no in-line imports
- Each test in its own clearly labeled block with the test name as a comment
- All outputs printed with explicit labels (not bare numbers)
- Save outputs to file: `print()` statements redirect to `analysis_results.txt`

**Python template:**
```python
"""
AutoResearch Stage 1-A Analysis
Session: [session_id]
CP 1A approved: [date]
Tests: [list of approved tests]
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import pingouin as pg

# ── Data loading ──────────────────────────────────────────────────────────
df = pd.read_csv("../input/patient_data.csv")

# ── Descriptive statistics ────────────────────────────────────────────────
print("=== DESCRIPTIVE STATISTICS ===")
print(df.groupby("group")["outcome"].agg(["mean","std","median",
    lambda x: x.quantile(0.25), lambda x: x.quantile(0.75), "count"]))

# ── Primary analysis: Mann-Whitney U ──────────────────────────────────────
print("\n=== PRIMARY ANALYSIS: Mann-Whitney U ===")
group_a = df[df["group"]=="A"]["outcome"]
group_b = df[df["group"]=="B"]["outcome"]
stat, pval = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
print(f"U = {stat:.4f}, p = {pval:.4f}")

# Effect size: rank-biserial correlation
r = 1 - (2 * stat) / (len(group_a) * len(group_b))
print(f"Effect size (r) = {r:.4f}")
```

### 2.2 Execute

Run via Claude Code sandbox:
```bash
cd sessions/[id]
python stage1/analysis/analysis_code.py > stage1/analysis/analysis_results.txt 2>&1
```

Capture all output: test statistics, p-values, descriptive tables, any warnings.

### 2.3 Handle Failures

If a test fails or produces unexpected results:
- Report the error exactly — do not silently substitute another test
- Propose one specific alternative with rationale
- Raise at CP 1B: "The approved test [X] failed because [Y]. I propose [Z] instead. Do you approve?"
- Do not proceed without researcher confirmation of the substitute

---

## Step 2.5 — Power Analysis

Run for every statistical test. **This is mandatory, not optional.**

### For significant results (post-hoc observed power):

```python
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower, NormalIndPower

# Example: independent t-test
analysis = TTestIndPower()
power = analysis.power(effect_size=cohen_d, nobs1=n_a, ratio=n_b/n_a, alpha=0.05)
print(f"Observed power: {power:.3f}")
```

Report: "Achieved power = [X]% to detect the observed effect (d = [Y]) at α = .05, n = [Z] per group."

If power < .80: flag explicitly — "This study is underpowered. The observed effect should be interpreted cautiously and confirmed in a larger sample."

### For non-significant results:

Calculate the minimum detectable effect at 80% power given the actual sample size:

```python
analysis = TTestIndPower()
min_detectable = analysis.solve_power(nobs1=n_a, ratio=n_b/n_a, alpha=0.05, power=0.80)
print(f"Minimum detectable effect at 80% power: d = {min_detectable:.3f}")
```

Report: "At n=[X] per group, this study had 80% power to detect effects of d ≥ [Y]. The observed effect (d = [Z]) falls below this threshold. The non-significant result should not be interpreted as evidence of no effect."

### A priori power:

If the researcher provided a sample size calculation: verify adequacy.
If no a priori calculation exists: note as a study limitation.

---

## Step 3 — Interpret

### 3.1 Report Every Result With All Required Components

For **every** statistical test, report ALL of the following — no exceptions:

| Component | Required format |
|---|---|
| Test used and why | "Mann-Whitney U was used because..." |
| Exact test statistic | U = 234.0, t(48) = 2.18, F(2,87) = 5.34, χ²(1, N=90) = 6.41 |
| Degrees of freedom | Always include when applicable |
| Exact p-value | p = .034 (never "p < .05"; never "p = 0.03") |
| Effect size | Cohen's d, r, η², ω², OR, RR, HR as appropriate |
| 95% CI on effect size | [X.XX, X.XX] — use bootstrap CI for non-parametric tests |
| Plain-language summary | 1–2 sentences stating what the result means |

**APA 7th Edition Reporting Formats:**

```
t-test:         t(df) = X.XX, p = .XXX, d = X.XX [95% CI: X.XX, X.XX]
Mann-Whitney:   U = XXX, p = .XXX, r = X.XX [95% CI: X.XX, X.XX]
ANOVA:          F(df1, df2) = X.XX, p = .XXX, η² = .XX [95% CI: .XX, .XX]
Kruskal-Wallis: H(df) = X.XX, p = .XXX, η²_H = .XX
Pearson r:      r(df) = .XX, p = .XXX [95% CI: .XX, .XX]
Spearman ρ:     ρ(df) = .XX, p = .XXX
Chi-square:     χ²(df, N = XXX) = X.XX, p = .XXX, φ = .XX
Logistic reg:   OR = X.XX [95% CI: X.XX, X.XX], p = .XXX
Cox hazards:    HR = X.XX [95% CI: X.XX, X.XX], p = .XXX
```

### 3.2 Statistical vs. Clinical Significance

For every significant result, explicitly state:
- **Statistical significance**: "The difference is statistically significant (p = .034)."
- **Clinical/biological significance**: assess the effect size against established benchmarks:
  - Cohen's d: small=0.2, medium=0.5, large=0.8
  - η²: small=.01, medium=.06, large=.14
  - OR/HR: discuss clinical relevance in the study context

Example of required distinction:
> "The group difference reached statistical significance (p = .034), however the effect size
> is small (d = 0.32 [95% CI: 0.03, 0.61]), suggesting the clinical magnitude of this
> difference warrants further consideration of practical relevance."

### 3.3 Flag All Caveats Explicitly

The following must be flagged when applicable — never omit:

- **Assumption violations**: "Normality was violated (Shapiro-Wilk p = .018). Mann-Whitney U was used, which is valid but has lower power under these conditions."
- **Small n**: "With n = [X] per group, confidence intervals are wide. Replication in a larger sample is warranted."
- **Multiple comparisons**: "X comparisons were made. After [correction method], the adjusted α = [Y]. Results significant only at the unadjusted level are marked with †."
- **What the analysis does NOT show**: state explicitly what cannot be concluded.
- **Alternative explanations**: list at least one plausible alternative interpretation not ruled out by the data.

### 3.4 Summary for Story Writer

End every CP 1B report with this exact block:

```
## Summary for Story Writer

| Finding | Direction | Effect size | Strength | Notes |
|---|---|---|---|---|
| [Primary outcome] | [↑/↓/~] | d=[X] | Strong/Moderate/Weak/Null | [key caveat] |
| [Secondary 1]     | [↑/↓/~] | r=[X]  | Moderate | [caveat] |

Strength key:
  Strong   = p < .01 AND d ≥ 0.5 (or η² ≥ .06)
  Moderate = p < .05 AND d ≥ 0.2
  Weak     = p < .05 AND d < 0.2 (statistically significant but small effect)
  Null     = p ≥ .05 (report with power context)
```

---

### ✓ CHECKPOINT 1B

Present full interpretation report including:
1. All test results with complete reporting (Step 3.1 format)
2. Statistical vs. clinical significance distinction (Step 3.2)
3. All flagged caveats (Step 3.3)
4. Power analysis results (Step 2.5)
5. Summary for Story Writer (Step 3.4)

**STOP. Do not proceed to visualization until the researcher responds with [OK].**

---

## Self-Check Before Presenting at CP 1B

- [ ] Every result has: test statistic, df, exact p-value, effect size, 95% CI
- [ ] No result reports "p < .05" — all p-values are exact
- [ ] Statistical and clinical significance are distinguished for every significant result
- [ ] All assumption violations are flagged
- [ ] Multiple comparisons correction is applied and reported
- [ ] Power analysis is present for every test
- [ ] Non-significant results have minimum-detectable-effect calculation
- [ ] Summary for Story Writer is complete with strength ratings
- [ ] No interpretation of mechanism (save for Discussion section)

---

## Hard Rules

1. **NEVER run code before CP 1A is cleared** — not even "just to check"
2. **NEVER report "p < .05"** — always exact p-values to 3 decimal places
3. **NEVER omit effect sizes** — they are mandatory alongside every p-value
4. **NEVER say "no effect" from a non-significant result** — report power and minimum detectable effect instead
5. **NEVER substitute a failed test silently** — surface it explicitly and seek approval
6. **NEVER fetch external data** (GEO, TCGA, databases) — the researcher provides all data
7. **NEVER propose analyses not tied to the research question** — more tests ≠ better science
8. **NEVER round p-values to 0** — if p < .001, report as "p < .001" (not p = 0.000)

---

## Common Pitfalls

**Bad:** "The t-test showed a significant difference (p < .05)."
**Good:** "Groups differed significantly on the primary outcome (t(48) = 2.18, p = .034, d = 0.32 [95% CI: 0.03, 0.61])."

**Bad:** "There was no significant difference, so X has no effect on Y."
**Good:** "The difference did not reach statistical significance (U = 234, p = .187). At n = 25 per group, the study had 80% power to detect effects of d ≥ 0.57. The observed effect (d = 0.28) falls below this threshold; the study may be underpowered to detect small-to-medium effects."

**Bad:** Running 12 comparisons without correction and reporting all as significant.
**Good:** Pre-specify primary outcome, apply Bonferroni to secondary outcomes, report adjusted α.
