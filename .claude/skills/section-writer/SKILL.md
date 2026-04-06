---
name: section-writer
description: >
  Write one manuscript section at a time following the confirmed narrative arc.
  Produces publication-quality scientific prose for biomedical papers.
  Enforces cross-section consistency, word count targets, and mandatory statements.
  Use after Story Writer (CP 2B) is cleared. Writing order:
  Methods → Results → Discussion → Conclusion → Introduction → Abstract.
  Triggers on: "write [section]", "draft [section]", "Stage 2-C",
  or when CP 2B is cleared and the next section is specified.
metadata:
  category: writing
  trigger-keywords: "write,draft,section,methods,results,discussion,conclusion,introduction,abstract,manuscript,Stage 2-C,prose"
  applicable-stages: "2"
  priority: "2"
  version: "2.0"
  author: autoresearch
---

# Section Writer — Stage 2-C

**Write only the section you are called to write. Do not draft ahead.
Every factual claim must be traceable to this study's data, confirmed literature, or
explicitly labeled as interpretation. No padding. Every sentence earns its place.**

---

## Context to Load Before Starting Each Section

1. Run `autoresearch status` — confirm CP 2B is cleared; note which section is next.
2. Read `sessions/[id]/stage2/story/outline.md` — the confirmed section outline.
3. Read `sessions/[id]/stage1/analysis/interpretation.md` — for exact statistics.
4. Read `sessions/[id]/stage1/figures/captions.md` — for exact figure references.
5. Read `sessions/[id]/stage2/literature/synthesis.md` — for citation support.
6. **Read all previously approved sections** — extract consistency anchors (Step 1 below).

---

## Step 1 — Extract Consistency Anchors

Before writing any section, read all approved sections and record:

| Anchor | Value | Source section |
|---|---|---|
| Total N | e.g., n = 88 | Approved: Methods |
| Group A name | e.g., "Treatment group" | Approved: Methods |
| Group B name | e.g., "Control group" | Approved: Methods |
| Primary outcome name | e.g., "serum biomarker Z" | Approved: Methods |
| Primary statistic | e.g., "U = 234, p = .034, r = 0.42" | Approved: Results |
| Key figure reference | e.g., "Figure 1" | Approved: Results |

These anchors must be used verbatim in the new section. Any discrepancy is a error — flag it immediately.

For the first section (Methods): extract anchors from the confirmed figures and analysis output.

---

## Step 2 — Writing Order & Section-Specific Rules

### Section 1: Methods

**Tense:** Past tense throughout ("Patients were enrolled...", "Samples were analyzed...")
**Target word count:** 500–900 words (longer if complex multi-step procedures)
**Goal:** Sufficient detail for independent replication by a researcher in the same field.

**Required subsections** (in this order):
1. **Study design**: one sentence stating design type (RCT / cohort / case-control / cross-sectional / etc.) and study period
2. **Participants**: inclusion criteria, exclusion criteria, recruitment setting and procedure, total enrolled
3. **[Primary intervention or exposure]**: describe in sufficient technical detail for replication
4. **Measurements/outcomes**: define primary outcome first, then secondary outcomes; specify measurement units, timing, and instruments
5. **Statistical analysis**: list every approved test from CP 1A by name; state software and version; state multiple comparisons correction method; state significance threshold (α = .05 unless otherwise justified)
6. **Ethics statement**: IRB/ethics committee name, approval number, declaration of Helsinki compliance, consent procedure. If researcher has not provided this information, insert `[ETHICS STATEMENT REQUIRED]` and flag.

**Do NOT include results in Methods.**
**Do NOT justify methodological choices in Results or Discussion — do it here.**

### Section 2: Results

**Tense:** Past tense for findings; present tense for what figures show ("Figure 1 shows...")
**Target word count:** 700–1,100 words
**Goal:** Report what happened — not why it happened (that is Discussion).

**Structure:**
1. **Participant characteristics** paragraph: sample size, demographic/baseline table reference, any exclusions after enrollment with reason
2. **Primary outcome** paragraph: lead with the primary result; report complete statistics
3. **Secondary outcomes** (one paragraph each or combined if brief): in order of scientific priority
4. **Null results** (required if any tests were non-significant): report honestly; include power context

**Inline statistics format** — exact and complete every time:
```
t(48) = 2.18, p = .034, d = 0.32 [95% CI: 0.03, 0.61]
U = 234, p = .008, r = 0.42 [95% CI: 0.18, 0.62]
F(2, 87) = 5.34, p = .007, η² = .11 [95% CI: .02, .22]
OR = 2.41 [95% CI: 1.18, 4.93], p = .016
HR = 0.61 [95% CI: 0.41, 0.91], p = .015
```

**Figure citation rule:** cite each figure the first time the finding it displays is mentioned.
Correct: "Treatment A showed significantly lower biomarker Z levels (Figure 1A; U = 234, p = .008)."
Incorrect: "Biomarker Z levels are shown in Figure 1A." (uninformative — state the finding first)

**Do NOT interpret** — do not state mechanism, clinical implication, or comparison to prior studies.
**Do NOT omit** null or negative findings — they belong here, not buried in a supplementary.

### Section 3: Discussion

**Tense:** Mix — past tense for own findings; present tense for established facts; past tense for prior studies
**Target word count:** 900–1,400 words
**Goal:** Contextualize findings — confirm/contradict/extend prior work; interpret mechanism; acknowledge limitations; state implications.

**Required paragraph structure (follow exactly):**

**Paragraph 1 — Key finding restatement:**
- First sentence: restate the primary finding in plain language (no statistics)
- Do NOT re-report statistics here
- Example: "This study demonstrated that Treatment A was associated with significantly lower serum biomarker Z levels compared to controls, with a moderate effect size."

**Paragraphs 2–3 — Literature context:**
- Confirm/contradict/extend: "Consistent with Smith et al. [1]..." / "In contrast to Jones et al. [2]..."
- Reference the synthesis from Stage 2-A — cite papers by number
- If contradicting prior work: explain the discrepancy (different population, follow-up, measurement)

**Paragraph 4 — Mechanistic interpretation:**
- Propose plausible mechanism — MUST be labeled as interpretation: "One possible explanation is...", "These findings are consistent with the hypothesis that..."
- Do NOT present mechanism as established fact unless it is

**Paragraph 5 — Limitations:**
- Use the pre-identified limitations from Story Writer outline
- Each limitation: state what it is → why it exists → direction of potential bias → what was done to minimize it
- Do NOT begin with "This study has several limitations" — start with the first limitation directly

**Paragraph 6 — Implications:**
- Clinical or scientific implications — proportional to study design
- Pilot study: "These findings warrant confirmation in..." (not "These findings support immediate clinical use")
- If implications for practice: state what specific change is supported and for what population

**Do NOT introduce new results in Discussion.**
**Do NOT repeat statistics from Results** — refer to findings in plain language.

### Section 4: Conclusion

**Tense:** Present tense for implications; past tense for findings
**Target word count:** 150–250 words (maximum 3 paragraphs)
**Goal:** Final synthesis — key message restated + one forward-looking statement.

**Structure:**
- Paragraph 1: Restate key message (1–2 sentences, plain language, no statistics)
- Paragraph 2: One specific implication for practice or future research
- No new information not already in Discussion
- No new figures or citations

**Bad Conclusion:** "In conclusion, this study found significant results and further research is needed."
**Good Conclusion:** "This study provides evidence that Treatment A reduces serum biomarker Z in patients with early-stage Disease Y, with a moderate effect size suggesting clinical relevance pending larger-scale confirmation. These findings support the design of a multicenter RCT examining Treatment A in diverse populations with Disease Y, with cardiovascular events as the primary endpoint."

### Section 5: Introduction

**Tense:** Present tense for established facts; past tense for prior studies; present for the study aim
**Target word count:** 400–650 words
**Goal:** Funnel from broad context to specific gap to study objective.

**Required structure:**
- **Paragraph 1**: Broad clinical/epidemiological context — establish why the topic matters
- **Paragraph 2**: Current state of evidence — synthesize 2–4 key prior findings (use confirmed citations)
- **Paragraph 3**: The specific gap — name what is unknown (must match Story Writer's gap statement exactly)
- **Final sentence**: "Therefore, this study aimed to [objective]." — exact study aim, no results preview

**Do NOT preview findings** ("we found that...", "our results showed...")
**Do NOT include methods detail** in Introduction

### Section 6: Abstract *(always last)*

Written only after all other five sections are confirmed.
**Target word count:** 250 words or journal-specified limit (check config.autoresearch.yaml)
**Structure:** Background / Objective / Methods / Results / Conclusion (structured format)

**Rules:**
- Must accurately represent every section — re-read all confirmed sections before writing
- No information in Abstract that is not in the manuscript
- Primary outcome statistics must appear verbatim (same values as in Results)
- No citations in Abstract
- Results subsection: include primary outcome with complete statistics (p-value + effect size)
- Conclusion subsection: match the manuscript Conclusion — no additional claims

---

## Step 3 — General Writing Standards

1. **One main idea per paragraph** — state it in the topic sentence; support it in subsequent sentences; close it
2. **Active voice preferred:** "We measured..." not "Measurements were taken..."
3. **Define abbreviations on first use** in this section (even if defined in a prior section — readers may read sections independently)
4. **Sentence length:** average 15–25 words; vary rhythm; avoid run-ons
5. **Citations:** every factual claim about the external literature needs a citation number; every result from this study needs no citation
6. **Hedge precisely:** use one hedge, not stacked hedges
   - Bad: "It might possibly suggest that..."
   - Good: "These findings suggest that..." or "A possible explanation is..."
7. **"significant":** reserve for statistical significance only; use "substantial", "clinically meaningful", or "large" for practical importance

---

## Output Format Per Section

```
## [Section Name] Draft
[word count]

[Full section prose — no bullets, no headers within the section unless structured methods requires them]

---
Notes for Researcher:
- Claims added beyond the outline: [list each, or "None"]
- Citations added beyond the confirmed literature: [list each, or "None"]  
- Statistics used: [confirm they match Stage 1-B output exactly, or note discrepancy]
- Flags requiring researcher attention: [list, or "None"]

---
✓ CHECKPOINT 2C-[N] — [Section Name] complete ([word count] words)
Proceed to [next section]?  [OK] / [REVISE: ...] / [REDIRECT: ...]
```

---

## Self-Check Before Presenting

- [ ] Consistency anchors match all previously approved sections
- [ ] All assigned figures cited in text before they appear
- [ ] Statistics in text match Stage 1-B report exactly (same values, same format)
- [ ] No results in Methods; no interpretation in Results; no new results in Discussion
- [ ] All abbreviations defined on first use within this section
- [ ] Claims proportional to effect sizes (pilot study language for small n)
- [ ] Word count within target range
- [ ] Ethics/IRB statement present in Methods (or [PLACEHOLDER] flagged)
- [ ] Notes section lists any added claims, citations, or flags

---

## Hard Rules

1. **NEVER submit bullet points as manuscript text** — full prose required
2. **NEVER stack hedges**: "It might possibly suggest…" → choose one
3. **NEVER write "It is well known that…"** — cite it or remove it
4. **NEVER use "significant" for non-statistical emphasis** — use "substantial" or "notable"
5. **NEVER draft ahead** — one section at a time, one CP at a time
6. **NEVER omit null findings** — they must appear in Results
7. **NEVER add a citation not in the confirmed literature without flagging it in Notes**
8. **NEVER write the Abstract before all other sections are confirmed**
