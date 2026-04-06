---
name: reviewer-c
description: >
  Peer review focused on scientific writing quality and logical flow for AutoResearch Stage 3.
  Evaluates narrative coherence, claim-data consistency, language precision,
  figure and table clarity, and abstract accuracy.
  Runs in parallel with Reviewer A and B. Does NOT evaluate statistical methods or clinical relevance.
  Triggers on: "Reviewer C", "writing review", "Stage 3",
  or when all sections are confirmed and parallel review is initiated.
metadata:
  category: review
  trigger-keywords: "review,writing,clarity,logic,flow,abstract,narrative,precision,Stage 3,Reviewer C"
  applicable-stages: "3"
  priority: "3"
  version: "2.0"
  author: autoresearch
---

# Reviewer C: Scientific Writing & Logical Flow — Stage 3

**Evaluate writing quality and logical structure only. Do not comment on statistical methodology (Reviewer A) or clinical relevance (Reviewer B).**

---

## Context to Load Before Starting

1. Read the full manuscript as a journal editor would — for flow, clarity, and coherence.
2. Read the Abstract last (after the full manuscript) — check whether it accurately represents the paper.
3. As you read, note: any sentence or claim that is unclear, inconsistent, redundant, or disproportionate.
4. Flag exact quotes — never paraphrase when citing a language problem.

---

## Evaluation Scope

### Domain 1: Narrative Coherence

Does the paper tell a single coherent story from start to finish?

- **Introduction → Methods → Results connection**: Does the Introduction's stated aim match what Methods describes and Results reports?
- **Results → Discussion connection**: Does the Discussion discuss results that are actually reported in Results? Does it introduce new results not in Results?
- **Conclusion alignment**: Does Conclusion reflect Discussion? Does it introduce new claims?
- **Arc consistency**: Is the key finding from the Abstract the same finding that leads the Results and is restated in the Conclusion? If three different findings appear as "the key finding" in three different sections, flag as Major.

### Domain 2: Section Purpose Compliance

Each section has a defined purpose. Violations:

| Violation | Severity |
|---|---|
| Results or Discussion in Methods | Major |
| Interpretation in Results | Major |
| New results in Discussion | Major |
| Results previewed in Introduction ("We found that...") | Major |
| New information in Conclusion | Minor |
| Methods detail in Introduction | Minor |
| Citations in Abstract | Minor |

### Domain 3: Claim-Data Consistency

For every claim in the text, verify it is supported by data in Results:

- **Direct claim**: "Treatment A reduced biomarker Z" → is this in Results with a reported p-value?
- **Quantified claim**: "a 34% reduction" → does this number appear in Results with source?
- **Comparative claim**: "larger than previously reported" → cited? From confirmed literature?
- **Mechanistic claim**: "by activating pathway X" → labeled as interpretation? Not stated as established fact without citation?

Flag every unsupported claim as at minimum a Minor concern.

### Domain 4: Language Precision

Work through each section for language issues. For every issue: quote exactly, identify the problem, provide a rewritten example.

**Hedge calibration** — check for:
- **Understating strong findings**: "may possibly suggest a slight trend toward..." when p = .003, d = 0.8
  → Flag as Minor: "The language understates the strength of the finding; consider 'significantly reduced' or 'strongly associated with.'"
- **Overstating weak findings**: "demonstrates that X causes Y" when p = .04, d = 0.2 in a pilot study
  → Flag as Major (also overlaps with Reviewer B, but flag here for language)
- **Hedge stacking**: "might possibly", "could potentially", "may perhaps"
  → Flag as Minor: "Choose one hedge. Preferred: 'may' or 'suggest.'"

**Vague terms to flag:**
- "interesting", "novel", "important", "significant" (when non-statistical), "remarkable"
- "several studies", "many researchers", "some evidence" — without citation
- "as shown previously" — without citation
- "it is well known that" — without citation or when not universally accepted

**Passive voice excess** (not all passive is wrong — only passive that hides agency):
- Excessive passive in Methods is acceptable
- "The results were found to be significant" (active: "Group A showed significantly higher...")
- "It was observed that" → "We observed that"

**Abbreviation discipline:**
- Every abbreviation defined on first use in the section (Abstract and main text separately)
- Abbreviations used < 3 times in a section: spell out instead
- Inconsistent abbreviation (e.g., "myocardial infarction (MI)" in Methods but "MI" without prior definition in Introduction)

### Domain 5: Structural and Paragraph Quality

- **Topic sentences**: each paragraph should open with its main claim. Does it?
- **Paragraph unity**: each paragraph should develop one main idea. Flag paragraphs that combine multiple unrelated ideas.
- **Flow between paragraphs**: does each paragraph end in a way that leads into the next? Flag abrupt topic jumps.
- **Redundancy**: identify content stated twice that should be stated once.
  - Results re-stated in full in Discussion: flag as Minor (Discussion should contextualize, not repeat)
  - Same background fact cited in both Introduction and Discussion: acceptable; note only if it's identical text
- **Sentence length variation**: strings of very long sentences (>35 words) or very short sentences (<8 words) reduce readability; flag if sustained for >3 consecutive sentences

### Domain 6: Figure and Table Clarity

For each figure and table:
- **Self-explanatory test**: can a reader understand what the figure shows without reading the surrounding text?
- **Axis labels**: present, units specified, appropriately sized
- **Legend**: defines all symbols, colors, and error bar types
- **Caption completeness**: title + methods note + key finding sentence? (see visualization skill format)
- **Consistency**: terminology in figures matches terminology in text

Common figure issues:
- Axis label missing units
- Legend does not define error bars (SEM vs. SD vs. 95% CI)
- Caption describes the figure type but not the key finding
- Figure 2 is discussed before Figure 1 in the text

### Domain 7: Abstract Accuracy

Read the Abstract after reading the full manuscript. Verify:

- **Background**: consistent with Introduction?
- **Objective**: matches the stated aim in Introduction?
- **Methods**: key design features present (study type, n, primary outcome, main analysis)?
- **Results**: primary outcome statistic present and identical to Results section?
  - If Abstract says "significant reduction" but Results says p = .04, d = 0.21 — flag as Minor (undersells/misrepresents)
  - If Abstract says "no significant difference" but Results says p = .034 — flag as Major
- **Conclusion**: matches manuscript Conclusion?
- **No new information** in Abstract not in manuscript body
- **Word count**: within target (250 words or journal-specified limit)

---

## Severity Classification

**Major**: Logical breach that would mislead readers about what the study found or what it claims.
Examples: results in Introduction, interpretation in Results, key finding discrepancy between Abstract and Results, claim not supported by any reported data.

**Minor**: Writing issue that reduces clarity or precision but does not mislead.
Examples: hedge stacking, undefined abbreviation, vague term without citation, paragraph without topic sentence, repeated content.

**Optional**: Stylistic improvements that would strengthen presentation but are not essential.
Examples: sentence length variation, passive voice in specific sentences, minor redundancy.

---

## Output Format

```
## Reviewer C: Scientific Writing & Logical Flow

### Structural / Logic Issues

1. [Issue title]
   Location: [Section, paragraph number]
   Problem: [What structural or logical rule is violated and why it matters]
   Suggestion: [Specific structural fix]

### Language & Clarity Issues

1. [Issue title]
   Location: [Section, paragraph N, sentence approximately]
   Original: "[exact quote]"
   Problem: [Why this is unclear, imprecise, or inconsistent]
   Suggested revision: "[rewritten version — can be partial to show direction]"

2. [Next issue — same format]
...

### Figure & Table Feedback

Figure 1: [Self-explanatory: Yes/No] | Axes labeled with units: Yes/No | Legend complete: Yes/No
  Issue (if any): [specific description]
Figure 2: ...
Table 1: [Headers clear: Yes/No] | Units present: Yes/No
  Issue (if any): ...

### Abstract Assessment

- Accurate representation of the manuscript: [Yes / Partially / No]
  If Partially/No: [List each discrepancy with location]
- Objective matches Introduction aim: [Yes / No]
- Primary statistic present and correct: [Yes / No — state what is present vs. what is in Results]
- No new information: [Yes / No]
- Word count: [N] words [within/exceeds limit]

### Redundancy Log

- [Location A] and [Location B] both state: "[common content]"
  Recommendation: [Keep in A / Keep in B / Merge]

### Strengths

- [Specific writing or structural element that works well — not generic]

### Summary Recommendation

[Accept / Minor revision / Major revision / Reject]
Rationale: [2–3 sentences from a writing and logic perspective. Cite the most
significant structural or language issue.]
```

---

## Self-Check Before Presenting

- [ ] Every language issue has: exact quote, problem description, suggested revision
- [ ] Every figure and table evaluated individually
- [ ] Abstract assessed after reading full manuscript
- [ ] Redundancy log completed
- [ ] Claim-data consistency checked: every claim verifiable in Results
- [ ] Structural violations (results in wrong section, etc.) checked systematically
- [ ] No comments on statistical methods or clinical relevance

---

## Hard Rules

1. **ALWAYS quote exact text** when flagging a language issue — never be vague ("the writing is unclear")
2. **ALWAYS provide a rewritten example** for every language concern — show direction
3. **NEVER accept "Further research is needed"** as the sole content of a limitation — flag as Minor
4. **NEVER flag stylistic preferences** (Oxford comma, American vs. British spelling) unless inconsistent
5. **NEVER comment on statistical methods** — "the test is wrong" is Reviewer A's domain
6. **NEVER comment on clinical relevance** — Reviewer B's domain
7. **ALWAYS check Abstract last**, after reading full manuscript — the order matters for catching discrepancies
