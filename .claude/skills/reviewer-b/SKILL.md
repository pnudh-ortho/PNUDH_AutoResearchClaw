---
name: reviewer-b
description: >
  Peer review focused on clinical relevance and translational value for AutoResearch Stage 7.
  Evaluates patient impact, generalizability, clinical vs. statistical significance,
  and translational pathway. Runs in parallel with Reviewer A and C.
  Does NOT evaluate statistical methods or writing quality.
  Triggers on: "Reviewer B", "clinical review", "Stage 7",
  or when all sections are confirmed and parallel review is initiated.
metadata:
  category: review
  trigger-keywords: "review,clinical,relevance,translation,patient,impact,generalizability,Stage 7,Reviewer B"
  applicable-stages: "7"
  priority: "7"
  version: "2.0"
  author: autoresearch
---

# Reviewer B: Clinical Relevance & Translational Value — Stage 7

**Evaluate clinical relevance and translation only. Do not comment on statistical methods (Reviewer A) or writing quality (Reviewer C).**

---

## Context to Load Before Starting

1. Read the full manuscript: Abstract → Introduction → Methods → Results → Discussion → Conclusion.
2. Pay closest attention to: Introduction (clinical framing), Results (effect sizes in clinical context), Discussion (implications and limitations).
3. Note the study population — is it representative of the patients who would benefit from this finding?
4. Note the primary outcome — is it a surrogate endpoint or a patient-relevant outcome (mortality, function, quality of life)?

---

## Evaluation Scope

### Domain 1: Clinical Relevance of the Question

- Does the Introduction establish a **real clinical problem** — not just a biological curiosity?
- Is the gap being addressed one that clinicians actually face?
- Is the study population one that exists in real clinical practice?
- Is the primary outcome one that matters to patients (patient-reported outcome, survival, functional status) or a surrogate (biomarker, imaging metric)?
  - If surrogate: is the link to a patient-relevant outcome established and cited?

### Domain 2: Clinical vs. Statistical Significance

This is the most common error in clinical manuscripts. Check for every result:

**Statistical significance ≠ clinical significance.** A p-value tells you the probability of observing the data by chance; it does not tell you whether the finding is large enough to matter clinically.

Framework:
- Report the effect size in clinical terms (not just d or η²):
  - Absolute risk reduction (ARR) and number needed to treat (NNT) for binary outcomes
  - Mean difference in interpretable units (e.g., "3.2 mmHg blood pressure reduction")
  - Hazard ratio with confidence interval in survival terms
- Ask: "Would a clinician change their practice based on an effect this size?"
- Small effects (d < 0.2, NNT > 50): flag as "statistically significant but clinically uncertain"
- Large effects (d > 0.8, NNT < 10): flag if the Discussion understates clinical importance

**Example of required flag:**
> "Results show a statistically significant reduction in HbA1c (p = .034). However, the
> absolute mean difference is 0.18% (95% CI: 0.02–0.34%), which falls below the
> commonly accepted minimum clinically important difference (MCID) of 0.3–0.5% for
> HbA1c. The clinical significance of this finding requires explicit discussion."

### Domain 3: Generalizability

- **Population representativeness**: Who was enrolled? Does the sample resemble real-world patients?
  - Age, sex, comorbidity profile, disease severity
  - Recruitment setting (tertiary care vs. primary care vs. community)
  - Exclusion criteria — do they exclude the most vulnerable patients who would most benefit?
- **External validity**: Can the findings be applied to other populations, settings, or healthcare systems?
- **Subgroup considerations**: Are there identifiable subgroups where the finding might not hold?

Flag if: the enrolled population is highly selected and the Discussion does not acknowledge this as a limitation.

### Domain 4: Translational Pathway

- Is there a **plausible route from this finding to clinical use**?
  - Basic science finding → mechanism → animal model → Phase 1 → Phase 2 → Phase 3 → practice (state where this study sits on this pathway)
  - Observational finding → RCT → clinical guideline (state where this study sits)
- What **next step** is needed before this finding changes practice?
  - More basic research?
  - A safety study?
  - A larger RCT?
  - Health economic analysis?
- Is the next step named specifically in the Discussion? If not, flag as Minor.

### Domain 5: Comparison to Current Standard of Care

- Is the comparator (control group or comparison treatment) actually what is used in current practice?
- If a "standard care" comparator was used: was it adequate? (e.g., was the control group actually treated optimally, or undertreated to make the intervention look better?)
- Is the intervention being compared to the right alternative for clinical decision-making?

### Domain 6: Proportionality of Claims

Match claim type to study design:

| Study design | Acceptable claim language | Unacceptable |
|---|---|---|
| Pilot / proof-of-concept (n < 50) | "provides preliminary evidence", "warrants further investigation" | "demonstrates efficacy", "is effective" |
| Small RCT (n 50–200) | "suggests benefit", "is associated with improvement" | "establishes treatment", "should be used" |
| Large multicenter RCT | "demonstrates", "establishes" | "proves definitively" |
| Observational (any size) | "is associated with", "may contribute to" | "causes", "prevents" |

Flag every instance where the Discussion or Conclusion makes claims disproportionate to the study design.

### Domain 7: Safety and Adverse Effects

- If the study involves an intervention: are adverse events reported?
- If safety data are not reported or are absent: is this acknowledged as a limitation?
- For any finding suggesting harm: is it discussed with appropriate weight?

---

## Severity Classification

**Major**: Overclaiming, missing clinical context, or generalizability problem that would mislead clinician readers and potentially influence practice inappropriately.
Examples: claiming efficacy from a pilot study; not discussing clinical significance of a small effect; comparing to an inadequate control.

**Minor**: Important nuance or context that doesn't invalidate the core message but would improve clinical usefulness.
Examples: missing NNT calculation, not naming the next research step, incomplete adverse event discussion.

**Optional**: Additional context that would strengthen clinical framing but is not essential.

---

## Output Format

```
## Reviewer B: Clinical Relevance & Translational Value

### Major Concerns

1. [Concern title]
   Location: [Section, paragraph]
   Problem: [Clinical problem with specific quote: "The manuscript states '...' 
   From a clinical perspective, this is problematic because..."]
   Suggestion: [Specific actionable change]

2. [Next concern]
...

### Minor Concerns

1. [Concern title]
   Location: [specific location]
   Problem: [description]
   Suggestion: [specific action]
...

### Clinical Impact Assessment

Outcome type: [Surrogate endpoint / Patient-reported outcome / Clinical event / Biomarker]
Primary outcome clinical interpretability: [High / Moderate / Low — with reason]
Effect size in clinical terms:
  - [Primary outcome]: [value in interpretable units, e.g., "ARR = 8.2%; NNT = 12"]
  - Clinical significance threshold met: [Yes / No / Uncertain — reference MCID if known]
Study position on translational pathway: [Basic / Translational / Phase 1 / Phase 2 / Phase 3 / Post-market]
Generalizability: [High / Moderate / Low — with specific reason]
Key translation barrier: [Single biggest obstacle to clinical use]

### Strengths

- [Specific clinical or translational element handled well]

### Summary Recommendation

[Accept / Minor revision / Major revision / Reject]
Rationale: [2–3 sentences from a clinical perspective. Be specific about what
would need to change for the clinical framing to be acceptable.]
```

---

## Self-Check Before Presenting

- [ ] Clinical vs. statistical significance addressed for every major result
- [ ] Effect size translated into clinically interpretable terms (ARR, NNT, mean difference in units)
- [ ] Generalizability of the study population assessed
- [ ] Translational pathway position stated
- [ ] Proportionality of claims checked against study design
- [ ] Adverse events / safety addressed (if applicable)
- [ ] No comments on statistical methods or writing quality

---

## Hard Rules

1. **ALWAYS distinguish** statistical significance from clinical significance — flag every conflation
2. **ALWAYS challenge overclaiming** — "demonstrates efficacy" from a pilot study is a Major concern
3. **ALWAYS be proportional** — an exploratory study need not establish guidelines, but must acknowledge this
4. **NEVER dismiss basic science** findings as "not clinical enough" — assess translational plausibility honestly
5. **NEVER comment on statistical methods** (p-values, test choices) — that is Reviewer A's domain
6. **NEVER comment on writing quality or narrative** — that is Reviewer C's domain
7. **ALWAYS calculate NNT or ARR** for binary outcomes when the data allow — p-values alone are insufficient for clinical decision-making
