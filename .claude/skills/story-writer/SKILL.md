---
name: story-writer
description: >
  Design the narrative architecture of a biomedical paper before any prose is written.
  Produces a key message, narrative arc, section-by-section outline, pre-identified
  limitations, and supplementary materials plan. Does NOT write manuscript prose.
  Use after CP 2A (literature) is confirmed.
  Triggers on: "story", "narrative", "outline", "key message", "Stage 2-B",
  or when CP 2A has been cleared.
metadata:
  category: writing
  trigger-keywords: "story,narrative,outline,key message,arc,structure,blueprint,Stage 2-B,plan,design"
  applicable-stages: "2"
  priority: "2"
  version: "2.0"
  author: autoresearch
---

# Story Writer — Stage 2-B

**Design the blueprint before a single word of prose is written.
Every architectural decision must be traceable to confirmed data.
Never overclaim. Never manufacture a story the data cannot sustain.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — confirm CP 2A is cleared.
2. Read `sessions/[id]/stage1/analysis/interpretation.md` — confirmed statistical findings.
3. Read `sessions/[id]/stage1/figures/figure_plan.md` — confirmed figure list and types.
4. Read `sessions/[id]/stage2/literature/synthesis.md` — confirmed literature synthesis.
5. Review the "Summary for Story Writer" table from Stage 1-B (finding strength ratings).
6. Note the target journal from config.autoresearch.yaml if specified.

---

## Step 1 — Derive the Key Message

One sentence answering: **"What did we find, and why does it matter to this field?"**

### 1.1 Requirements for the Key Message

- **Specific**: names the population, intervention/exposure, direction of effect, and magnitude
- **Grounded**: directly traceable to confirmed results (cite the finding and effect size)
- **Connected**: addresses the specific gap identified in the literature synthesis
- **Proportional**: calibrated to the study's design — pilot ≠ definitive, exploratory ≠ confirmatory

### 1.2 Evidence Calibration Scale

Match claim language to study strength:

| Finding strength | Appropriate claim language |
|---|---|
| Strong (p < .01, d ≥ 0.5, large RCT) | "demonstrates", "establishes", "shows" |
| Moderate (p < .05, d 0.2–0.5) | "suggests", "indicates", "is associated with" |
| Weak (p < .05, d < 0.2) | "may be associated with", "trend toward" |
| Null (non-significant) | "did not differ", "no significant association was observed" |
| Exploratory / pilot | "warrants further investigation", "provides preliminary evidence" |

### 1.3 Key Message Templates

**Strong finding:**
> "In [population] (n=[X]), [intervention/exposure] reduced [outcome] by [magnitude]
> ([test statistic], p=[value], d=[effect size]), suggesting [mechanism or implication]
> pending confirmation in [larger/multicenter/prospective] trials."

**Moderate finding:**
> "In [population] (n=[X]), [exposure] was significantly associated with [outcome]
> ([statistic], p=[value]), extending prior findings from [reference] to [new context/population]."

**Null finding (report honestly):**
> "In [population] (n=[X]), [intervention] did not significantly affect [outcome]
> (p=[value]); the study was underpowered to detect effects smaller than d=[threshold],
> and the observed effect (d=[observed]) warrants evaluation in adequately powered studies."

### 1.4 What to Do If Data Cannot Support a Strong Key Message

State this explicitly at CP 2B — do not manufacture a message the data cannot sustain.
Options:
- Reframe as exploratory: "This study generates hypotheses for future investigation..."
- Emphasize methodological contribution: "This study validates [method] in [population]..."
- Lead with the gap contribution: "This study provides the first [design] data on [topic]..."

---

## Step 2 — Design the Narrative Arc

Map how each section contributes to the key message. Every section must have a clear purpose.

### Introduction Arc
- **Paragraph 1**: Broad clinical/biological context — why does this topic matter?
- **Paragraph 2**: What is currently known — synthesize 2–3 main findings from literature
- **Paragraph 3**: What remains unknown — the specific gap (must match synthesis exactly)
- **Final sentence**: "Therefore, the aim of this study was to [objective]."
  — Do NOT preview results here. The aim is stated, not the outcome.

### Methods Arc
- **Study design**: state design type (RCT, cohort, case-control, cross-sectional) and justify
- **Population**: inclusion/exclusion criteria; representativeness
- **Key methodological choices**: decisions that affect interpretation (must reference CP 1A plan)
- **Statistical approach**: matches exactly what was approved at CP 1A (test names, correction strategy)
- **Ethics and approval**: IRB/ethics committee statement (flag if researcher has not provided)

### Results Arc
- **Lead with primary finding** — highest effect size / most central to key message
- **Supporting findings in order of scientific priority** — secondary, then exploratory
- **Null findings reported honestly** — do not bury or omit
- **Figures appear in the order they are first cited** — no figure jumps

### Discussion Arc
- **Sentence 1**: Restate the key finding (not the statistics — what it means)
- **Context block**: confirm / contradict / extend 2–4 prior studies (cite synthesis)
- **Mechanistic block**: plausible explanation — labeled as interpretation, not established fact
- **Limitations block**: pre-identified limitations (see Step 4)
- **Implications block**: what does this finding mean for practice or future research? Proportional.
- **Closing sentence**: forward-looking — one specific next step

### Conclusion Arc
- Restate key message in 1–2 sentences
- One forward-looking statement: what should happen next (specific, not generic)
- No new information not in Discussion

### Abstract Arc (placeholder — written last by Section Writer)
- Background / Objective / Methods / Results / Conclusion
- Will synthesize from confirmed sections

---

## Step 3 — Section-by-Section Outline

For each section, produce this exact structure:

```
### [Section Name]

**Purpose (2–3 sentences):** What must this section achieve?

**Key points (in order):**
1. [Content that must appear — specific, not vague]
2. [Next point]
...

**Assigned figures/tables:**
- Figure [N]: [brief description] — cited in paragraph [X]

**Transition to next section:**
[One sentence: how does this section set up the next?]

**Flags:**
- [Any weak data points, claims needing softening, or gaps in the arc]
```

Produce outlines in writing order: Methods → Results → Discussion → Conclusion → Introduction → Abstract.

---

## Step 4 — Pre-Identify Limitations *(mandatory)*

Before Section Writer begins, identify **at least 3 specific limitations**. Generic disclaimers ("small sample size", "further research is needed") are not acceptable.

Each limitation must answer:
1. **What** is the specific constraint?
2. **Why** does it exist (methodological reason)?
3. **Direction**: does this limitation over- or under-estimate the effect?
4. **Mitigation**: what did the study do to minimize it?
5. **Impact**: how does this limit interpretation?

**Bad limitation:** "Small sample size limits generalizability."

**Good limitation:**
> "Single-center recruitment (N=88) limits demographic diversity; all participants were
> recruited from an urban tertiary care center, and results may not generalize to rural
> or primary care populations where disease severity and comorbidity profiles differ.
> This is expected to bias results toward higher-acuity patients (overestimating effect
> in healthier populations)."

Pre-identified limitations must appear in the Discussion outline under the "Limitations block."

---

## Step 5 — Supplementary Materials Plan *(if applicable)*

Identify data that belongs in supplementary materials rather than the main manuscript:

| Content type | Main or Supplementary? |
|---|---|
| Primary outcome figure | Main |
| Secondary outcome figures (if many) | Supplementary |
| Sensitivity analyses | Supplementary |
| Extended methods detail | Supplementary |
| Complete statistical output tables | Supplementary |
| Additional exploratory analyses | Supplementary |

For each proposed supplementary item, state: what it contains and why it's supplementary (not just "to save space").

---

### ✓ CHECKPOINT 2B

Present:
1. Key message sentence with evidence calibration justification
2. Narrative arc summary (one sentence per section)
3. Full section-by-section outline (all 6 sections)
4. Pre-identified limitations (≥3, with full specification)
5. Supplementary materials plan (or "None required")

```
## Story Architecture — CP 2B

### Key Message
[One sentence]
Evidence calibration: [Strong/Moderate/Weak/Null/Exploratory] — [rationale]

### Narrative Arc Summary
Introduction:  [one sentence]
Methods:       [one sentence]
Results:       [one sentence]
Discussion:    [one sentence]
Conclusion:    [one sentence]
Abstract:      [written last — will synthesize confirmed sections]

### Section Outlines
[Full outline for each section — see Step 3 format]

### Pre-Identified Limitations
1. [Full specification]
2. [Full specification]
3. [Full specification]

### Supplementary Materials Plan
[List or "None required"]

---
✓ CHECKPOINT 2B — Approve narrative architecture?
[OK] / [REVISE: ...] / [REDIRECT: ...]
```

**STOP. Section Writer does not begin until researcher responds with [OK].**

---

## Self-Check Before Presenting

- [ ] Key message is traceable to specific confirmed statistics
- [ ] Claim language matches the evidence calibration scale
- [ ] Gap statement in Introduction arc matches the literature synthesis exactly
- [ ] Results arc leads with the primary finding
- [ ] Null findings are included in the outline (not omitted)
- [ ] Each section outline has Purpose, Key points, Assigned figures, Transition, Flags
- [ ] At least 3 specific limitations are pre-identified with full specification
- [ ] Limitations are specific — no "small sample size" without further elaboration
- [ ] Supplementary materials plan is present

---

## Hard Rules

1. **NEVER start writing prose** — outline and bullet points only
2. **NEVER place a figure in a section where it doesn't belong** (no Results figures in Introduction)
3. **NEVER overclaim** — if data is from a pilot study, the arc must reflect exploratory framing
4. **NEVER leave a story gap unacknowledged** — flag every weak point at CP 2B
5. **NEVER design an arc that contradicts Stage 1 statistical interpretation**
6. **"Further research is needed" is not a limitation** — require a specific, mechanistic limitation
7. **NEVER derive a key message that cannot be found in the actual data**
