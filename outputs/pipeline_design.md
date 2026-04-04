# Pipeline Design — AutoResearch

---

## STAGE 1 — Data & Visualization

### Phase 1-A: Data Analysis

**Purpose:** Understand the data, propose and execute the right statistical approach,
and produce an interpretation that directly informs what the paper can claim.

**Inputs:**
- Raw data files (CSV, Excel, etc.) and/or pre-analyzed results
- Research hypothesis
- Comparison data from reference papers (user-provided only — no auto-fetch)

**Step 1 — Explore & Propose**
- Load and inspect: shape, column types, missingness, distributions per group
- Check statistical assumptions: normality (Shapiro-Wilk for n<50, Q-Q otherwise),
  variance homogeneity (Levene's), independence
- Map each comparison to the research hypothesis
- Propose: which test, why, what output will look like

**✓ CHECKPOINT 1A** — User approves statistical approach before any code runs.
`[OK]` / `[REVISE: ...]` / `[REDIRECT: ...]`

**Step 2 — Execute**
- Generate Python and/or R code for approved analysis
- Run via Claude Code sandbox
- Capture: summary statistics, test statistics, p-values, effect sizes, CIs

**Step 3 — Interpret**
- For every result: test used, exact statistic, exact p-value, effect size + 95% CI
- Explicitly distinguish statistical significance from biological/clinical significance
- Flag: assumption violations, small-n caveats, multiple comparisons, alternative explanations
- Produce "Summary for Story Writer" — 3–5 bullets on which findings are strong vs. weak

**✓ CHECKPOINT 1B** — User confirms interpretation before visualization begins.

**Hard rules:**
- Never run code before CP 1A is cleared
- Never report "p < 0.05" — always exact values
- Never omit effect sizes
- If a pre-approved test fails, surface it explicitly — do not silently substitute

---

### Phase 1-B: Visualization

**Purpose:** Translate confirmed analysis results into publication-quality figures.
Starts only after CP 1B is cleared.

**Inputs:** Confirmed analysis output from Phase 1-A

**Step 1 — Propose Figure Plan**

For each key finding, reason from the data (not from a fixed menu):
- Data type (continuous / categorical / survival / etc.)
- Comparison structure (two groups / multiple groups / correlation / over time / etc.)
- Scientific question (survival → KM; diagnostic → ROC; DEG → volcano; etc.)
- Readability: key finding must be visually obvious without reading the caption
- If n < 10 per group: always show individual data points

Propose 1–2 candidate figure types per finding with explicit rationale.

**✓ CHECKPOINT 1C** — AI proposes, user decides. Confirm figure plan before any code.

**Step 2 — Generate Code**

Base stack:
- Python: `SciencePlots` + `matplotlib` / `seaborn`
- R: `ggplot2` / `tidyverse` + `ggpubr`

Extend only when the figure type requires it:
| Figure type | Python | R |
|---|---|---|
| Kaplan-Meier | `lifelines` | `survival` + `survminer` |
| ROC | `sklearn.metrics` | `pROC` |
| Forest plot | `forestplot` | `forestploter` |
| Volcano | `matplotlib` custom | `EnhancedVolcano` |
| Complex heatmap | `PyComplexHeatmap` | `ComplexHeatmap` |
| OMICS multi-panel | `scanpy` | `Seurat` |
| Label adjustment | `adjustText` | `ggrepel` |

Code principles:
- One script per figure, modular and annotated
- Configuration variables at the top (colors, sizes, DPI)
- Export as PDF + PNG at 300 DPI minimum
- Colorblind-safe palettes by default

**Step 3 — Draft Captions**

Format: `Figure N. [Bold title]. [Methods note — n, test]. [Key finding sentence]. [(Panel labels if multi-panel)].`

---

## STAGE 2 — Writing

Stage 2 uses Stage 1 outputs as primary reference material.
Story Writer and Section Writer must have access to:
- Confirmed figure list and captions (from Phase 1-B)
- Statistical results and interpretation summary (from Phase 1-A)

### Phase 2-A: Literature

**Purpose:** Build the knowledge base that grounds the narrative.
Literature search is mandatory — not optional — regardless of how many
references the user provides.

**Search scope:** PubMed + Google Scholar. No date restriction by default
(seminal papers from any year are included). High-impact and directly relevant
papers are prioritized; recent papers (≤5 years) are noted but older foundational
work is equally included when relevant.

**Process:**
1. Start with user-provided references as the core set
2. Expand via systematic search: PICO-derived query, Boolean operators, 3+ databases
3. Screen for relevance; do not include papers merely to inflate reference count
4. Synthesize by theme — not an annotated list
5. Explicitly identify the gap that the current study addresses

**✓ CHECKPOINT 2A** — Confirm scope, add/remove papers, approve before Story Writer.

---

### Phase 2-B: Story Writer

**Purpose:** Design the narrative before a single word of the paper is written.
Story Writer does not write prose — it produces a blueprint.

**Inputs:** Literature synthesis (2-A) + confirmed figures + statistical interpretation (Stage 1)

**Step 1 — Key Message**

Derive one sentence answering: "What did we find, and why does it matter?"
Requirements: specific, grounded in confirmed results, connected to a literature gap,
proportional to what the data actually supports (no overclaiming).

**Step 2 — Narrative Arc**

Design how each section contributes to the key message:
- Introduction: background → gap → our approach
- Methods: design justification → key choices
- Results: primary finding first → supporting evidence in logical order
- Discussion: restate finding → literature context → mechanism → limitations → implications
- Conclusion: key message + forward-looking statement
- Abstract: last (synthesizes everything)

**Step 3 — Section-by-Section Outline**

For each section:
- Purpose (2–3 sentences)
- Key points (bullet list)
- Assigned figures/tables
- Transition note to next section
- Flags: where data is weak, where claims need softening

**✓ CHECKPOINT 2B** — Key message + arc confirmed before Section Writer begins.

---

### Phase 2-C: Section Writer

**Purpose:** Produce the manuscript one section at a time, strictly following the
confirmed narrative arc.

**Writing order:**
1. Methods
2. Results ← references confirmed figures and statistics from Stage 1
3. Discussion ← references Stage 1 interpretation + literature from Stage 2-A
4. Conclusion
5. Introduction
6. Abstract ← always last; synthesizes all confirmed sections

**Per-section rules:**
- Write only the assigned section — do not draft ahead
- Reference only confirmed figures, statistics, and literature
- Flag any new claims not in the outline at checkpoint (do not silently add)
- Self-check before presenting: figures referenced, stats match, no results in Methods,
  no interpretation in Results, claims proportional to effect sizes

**✓ CHECKPOINT 2C-1 through 2C-6** — One per section, in order.

---

## STAGE 3 — Review

Three reviewers run simultaneously and independently on the completed draft.
Each reads the full manuscript but focuses on their designated lens only.

### Reviewer A — Methodology & Statistical Rigor
Focus: study design, statistical test appropriateness, reproducibility,
sample size justification, effect size reporting, data integrity.
Does NOT comment on clinical relevance or writing quality.

### Reviewer B — Clinical Relevance & Translational Value
Focus: patient/clinical relevance, generalizability, clinical vs. statistical
significance, translational pathway, comparison to standard of care.
Does NOT comment on statistical methods or writing quality.

### Reviewer C — Scientific Writing & Logical Flow
Focus: narrative coherence, claim-data consistency, figure/table clarity,
abstract accuracy, language precision, citation appropriateness.
Does NOT comment on methodology or clinical relevance.

**Review Synthesis (auto-runs after all three reviews):**
- Aggregates comments by section
- Surfaces conflicts between reviewers
- Prioritizes: Major > Minor > Optional
- Produces unified revision checklist
- User sees synthesis, not raw reviews

**✓ CHECKPOINT 3** — User reviews synthesis, decides revision scope and priorities.

---

## STAGE 4 — Revision

### Phase 4-A: Revision Agent

Executes confirmed checklist items only.
Every change logged (what, where, why, cascade effects).
Items the researcher chose not to address are logged with rebuttal rationale.
No unrequested changes — additional problems noticed are flagged, not silently fixed.

### Phase 4-B: Proofreader

Systematic final check:
- Terminology consistency throughout
- Abbreviations: defined on first use, used consistently
- Citation completeness: every in-text citation in reference list and vice versa
- Figure/table cross-references: numbering, order, all cited before appearing
- Statistics consistency: text numbers match figures and tables
- Claim-evidence: Abstract and Conclusion match Results and Discussion
- Gene/protein formatting: italics for genes, regular for proteins

**✓ CHECKPOINT 4** — Final approval before output.

---

## Checkpoint Map

| ID | After | Gate question |
|----|-------|---------------|
| 1A | Data exploration + test proposal | Approve statistical approach? |
| 1B | Analysis execution + interpretation | Approve results & interpretation? |
| 1C | Figure plan proposal | Approve figure types & layout? |
| 2A | Literature synthesis | Confirm scope & key papers? |
| 2B | Story Writer outline | Approve key message & narrative arc? |
| 2C-1 | Methods draft | Proceed to Results? |
| 2C-2 | Results draft | Proceed to Discussion? |
| 2C-3 | Discussion draft | Proceed to Conclusion? |
| 2C-4 | Conclusion draft | Proceed to Introduction? |
| 2C-5 | Introduction draft | Proceed to Abstract? |
| 2C-6 | Abstract draft | All sections approved? |
| 3 | Review synthesis | Revision scope decided? |
| 4 | Proofreading complete | Approve final output? |
