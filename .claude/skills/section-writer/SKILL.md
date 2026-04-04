---
name: section-writer
description: >
  Write one manuscript section at a time following the confirmed narrative arc.
  Produces scientific prose for biomedical papers. Use after Story Writer (CP 2B)
  is cleared. Called once per section in this order:
  Methods → Results → Discussion → Conclusion → Introduction → Abstract.
  Triggers on: "write [section name]", "draft methods", "write results",
  "Stage 2-C", or when CP 2B has been cleared and a section name is specified.
metadata:
  category: writing
  trigger-keywords: "write,draft,section,methods,results,discussion,conclusion,introduction,abstract,manuscript,Stage 2-C"
  applicable-stages: "2"
  priority: "2"
  version: "1.0"
  author: autoresearch
  references: "adapted from scientific-writing skill (AutoResearchClaw)"
---

# Section Writer

Run Stage 2-C of the AutoResearch pipeline.
**Write only the section you are called to write. Do not draft ahead.**
**Reference confirmed figures, statistics, and literature only.**

## Before Writing Each Section

1. Read the section outline from Story Writer
2. Identify all figures/tables assigned to this section
3. Check previously approved sections for terminology and claim consistency
4. Note any flags raised by Story Writer for this section

## Writing Order & Section-Specific Rules

### 1. Methods
- Past tense throughout
- Sufficient detail for independent replication
- Statistical methods: match exactly what was confirmed at CP 1A
- Ethics and approval statement if applicable
- Do NOT include results

### 2. Results
- Past tense for findings; present tense for what figures show ("Figure 1 shows...")
- Lead with the primary finding (as established by Story Writer arc)
- Reference figures inline as they appear: (Figure 1A)
- Report statistics inline: `t(48) = 2.18, p = .034, d = 0.32 [95% CI: 0.03, 0.61]`
- Do NOT interpret — mechanism and implications belong in Discussion
- Report null and negative findings honestly — do not omit

### 3. Discussion
- First sentence only: restate key finding (do not re-report statistics)
- Contextualize in literature: confirm / contradict / extend prior work
- Mechanistic interpretation: label as interpretation, not established fact
- Limitations: specific to this study's design and data — not generic disclaimers
- Implications: proportional to what the data actually shows
- Do NOT introduce new results

### 4. Conclusion
- 1–3 paragraphs maximum
- No new information not already in Discussion
- Key message restated + forward-looking statement

### 5. Introduction
- Funnel structure: broad context → specific gap → our approach
- Present tense for established facts; past tense for prior studies
- End with clear statement of study objective (not a preview of results)
- Do NOT preview findings

### 6. Abstract (always last)
- Written after all other sections are confirmed
- Structure: Background / Objective / Methods / Results / Conclusion
- Must accurately reflect the paper — no overclaiming
- Default word limit: 250 words unless journal specifies otherwise
- Include primary outcome statistics

## General Writing Rules

1. Each paragraph conveys ONE main idea
2. Active voice preferred: "We measured…" not "Measurements were taken…"
3. Define abbreviations on first use; use consistently thereafter
4. Vary sentence length; aim for average 15–25 words
5. Every factual claim must be: from the study's own data, cited from confirmed literature,
   or explicitly labelled as interpretation
6. Do not pad — every sentence earns its place

## Output Format Per Section

```
## [Section Name] Draft

[Full section prose]

---
Notes for Researcher:
- New claims not in outline: [list or "none"]
- References added beyond confirmed list: [list or "none"]
- Flags: [anything requiring researcher attention]
- Word count: [n]

---
✓ CHECKPOINT 2C-[N] — [Section Name] complete
Proceed to [next section]? [OK] / [REVISE: ...] / [REDIRECT: ...]
```

## Self-Check Before Presenting

- [ ] All assigned figures/tables referenced
- [ ] Statistics match Stage 1-A report exactly
- [ ] No references outside confirmed list (without flagging)
- [ ] Abbreviations defined on first use in this section
- [ ] No results in Methods; no interpretation in Results
- [ ] Claims proportional to effect sizes
- [ ] Terminology consistent with approved sections

## Common Pitfalls (from scientific-writing best practice)

1. Never submit bullet points as manuscript text — write in full prose
2. Avoid hedge-stacking: "It might possibly suggest…" — choose one hedge
3. Do not start sentences with "It is well known that…" — cite or remove
4. Distinguish "significant" (statistical) from "substantial" (practical)
5. Ensure figures/tables are cited in text before they appear
6. Keep abbreviations to a minimum — define each on first use
