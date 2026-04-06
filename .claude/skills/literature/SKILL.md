---
name: literature
description: >
  Systematic literature search and synthesis for AutoResearch Stage 2-A.
  Mandatory even when the researcher has provided references — always expands
  the knowledge base. Searches PubMed and Google Scholar, screens for relevance,
  synthesizes by theme (not as an annotated list), identifies the evidence gap,
  and connects it to the current study's contribution.
  Triggers on: "literature search", "find papers", "Stage 2-A", "knowledge base",
  "references", or when CP 1C has been cleared and writing is next.
metadata:
  category: literature
  trigger-keywords: "literature,search,PubMed,scholar,papers,references,citation,synthesis,background,gap,Stage 2-A"
  applicable-stages: "2"
  priority: "1"
  version: "2.0"
  author: autoresearch
---

# Literature — Stage 2-A

**Build the knowledge base that grounds the narrative.
Synthesize by theme — never produce an annotated list.
Never fabricate citations. Never restrict to recent years by default.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — confirm CP 1C (or 1B) is cleared.
2. Read `sessions/[id]/stage1/analysis/interpretation.md` — the confirmed findings.
3. List files in `sessions/[id]/input/` — identify any reference PDFs the researcher provided.
4. Read `sessions/[id]/input/README.md` or any notes files — note the stated research question.
5. If `sessions/[id]/stage2/literature/synthesis.md` exists, continue from where it was left.

---

## Step 1 — Anchor the Search

### 1.1 Identify Core Concepts

Decompose the research question into components using PICO when applicable:

| PICO element | Example |
|---|---|
| **P** — Population / Problem | "Adult patients with Type 2 diabetes (HbA1c > 7.5%)" |
| **I** — Intervention / Exposure | "SGLT-2 inhibitor therapy (empagliflozin)" |
| **C** — Comparison | "Placebo or standard care (metformin monotherapy)" |
| **O** — Outcome | "Cardiovascular mortality, HbA1c reduction at 12 months" |

If PICO does not fit (e.g., diagnostic study, basic science): use the study's key concepts directly.

### 1.2 Build Search Terms

For each PICO component, generate:
- Official MeSH term(s): `[MeSH]` tag for PubMed
- Common synonyms: e.g., "heart attack" AND "myocardial infarction"
- Abbreviations: e.g., "T2DM", "HbA1c", "SGLT-2"
- Narrow and broad variants for sensitivity/specificity tradeoff

**Example PubMed query structure:**
```
(Type 2 diabetes[MeSH] OR "type 2 diabetes mellitus" OR T2DM) AND
(SGLT-2 inhibitor[MeSH] OR empagliflozin OR dapagliflozin OR canagliflozin) AND
(cardiovascular mortality OR "CV death" OR MACE) AND
(randomized controlled trial[pt] OR clinical trial[pt] OR cohort study[tw])
```

### 1.3 Catalog User-Provided References

Before searching, review every PDF/citation the researcher provided:
- Extract: authors, title, journal, year, key finding
- Flag any that appear tangentially related — raise at CP 2A
- Do not discard any — but note if a paper does not fit the synthesis

---

## Step 2 — Execute Search

### 2.1 Databases

Search in this order:
1. **PubMed** — mandatory for biomedical topics
2. **Google Scholar** — mandatory (catches conference proceedings, preprints, and papers not in PubMed)
3. **Cochrane Library** — if meta-analyses or systematic reviews are sought
4. **Embase** — if pharmacological or clinical trial coverage is needed

Use `autoresearch run pubmed --query "[query]" --max-results 30` for PubMed automation.

### 2.2 No Date Restriction by Default

Include papers from any year when:
- Seminal foundational papers (e.g., original trial establishing the treatment)
- Defining methodology papers (e.g., original Cox regression paper)
- Papers frequently cited as establishing a concept

**However**, note publication year prominently — readers need temporal context.

Restrict to recent years (≤5) only if the research question is about current state-of-practice and older literature is genuinely superseded.

### 2.3 Inclusion Criteria

Include if:
- Directly addresses one or more PICO components
- Peer-reviewed (or a seminal preprint not yet formally published)
- Reports original data or systematic review/meta-analysis of relevant data

Exclude if:
- Addresses only tangentially related populations, interventions, or outcomes
- Superseded by a larger or more rigorous subsequent study (note the superseding paper)
- Case reports or small series (n < 5) unless the finding is unique and directly relevant

### 2.4 Document the Search

Record exactly:
```
## Search Documentation

Databases: PubMed, Google Scholar, [+ others]
Search date: [YYYY-MM-DD]
Queries used:
  PubMed:  [exact query string]
  Scholar: [exact query string]

Results:
  PubMed:  [N] identified → [N] screened → [N] included
  Scholar: [N] identified → [N] screened → [N] included
  User-provided: [N] (all reviewed; [N] included in synthesis)

Total included: [N] papers
```

---

## Step 3 — Synthesize by Theme

### 3.1 Evidence Hierarchy

When multiple paper types address the same question, weight evidence accordingly:

| Study type | Evidence level | Use in synthesis |
|---|---|---|
| Systematic review + meta-analysis | Highest | Lead with this; note heterogeneity |
| RCT (large, multicenter) | High | Primary support for efficacy claims |
| RCT (small, single center) | Moderate-high | Note sample size limitation |
| Prospective cohort | Moderate | Supports association; not causation |
| Retrospective cohort | Moderate-low | Note bias risk |
| Case-control | Low-moderate | Note recall and selection bias |
| Cross-sectional | Low | Prevalence only; no causation |
| Case series / case reports | Very low | Only for unique/rare findings |

When synthesizing contradictory evidence, state the evidence level of each source explicitly.

### 3.2 Theme Identification

Group papers by theme, not by author or year. Typical biomedical themes:
- Background biology / pathophysiology
- Epidemiology / prevalence
- Existing treatments and their limitations
- Mechanism of the study's intervention
- Prior clinical evidence (efficacy, safety)
- Contradictions or unresolved debates
- Gap that the current study addresses

### 3.3 Write the Synthesis

For each theme, write a synthesis paragraph — NOT an annotated list:

**Bad (annotated list):**
> "Smith et al. (2019) found that X reduces Y. Jones et al. (2021) reported that X has no effect on Y."

**Good (thematic synthesis):**
> "Evidence for the effect of X on Y is conflicting. Two RCTs in adult populations reported
> significant reductions in Y with X treatment (Smith et al., 2019, n=342; Brown et al., 2020,
> n=218), whereas a prospective cohort study (Jones et al., 2021, n=1,204) observed no
> association after adjustment for confounders. The discrepancy may reflect the shorter follow-up
> in the RCTs (12 weeks) vs. 2 years in Jones et al., or differing outcome definitions."

### 3.4 Required Synthesis Sections

Your synthesis output must include all five of these:

1. **Core background themes** (2–4 themes, each 3–6 sentences):
   - State the current evidence, including conflicting findings
   - Note sample sizes, study designs, and strength of evidence
   - Highlight methodological limitations of prior work

2. **Contradictions or unresolved debates** (if any):
   - Name the disagreement precisely
   - State which evidence is stronger and why
   - Note what would be needed to resolve it

3. **Gap statement** (2–3 sentences — must be specific):
   - Name the most recent relevant paper and state what it did NOT address
   - State the specific gap: not "little is known" but "no RCT has examined X in population Y with outcome Z"
   - Connect the gap to the current study's design

4. **How the current study addresses the gap** (2–3 sentences):
   - State explicitly how the study's design, population, or outcome fills the named gap
   - Be proportional: "This study provides preliminary evidence…" vs. "This study definitively establishes…"

5. **Full reference list** (all included papers):
   - Format: Vancouver by default (numbered, in citation order)
   - Include: all authors if ≤6, first 6 + "et al." if >6, journal, year, volume, pages/DOI

---

### ✓ CHECKPOINT 2A

Present the full synthesis including all five required sections and the search documentation.

```
## Literature Synthesis — CP 2A

### Search Documentation
[As specified in Step 2.4]

### Theme 1: [Theme Name]
[Synthesis paragraph]

### Theme 2: [Theme Name]
[Synthesis paragraph]

### [Additional themes as needed]

### Contradictions and Debates
[Section or "None identified — evidence is largely consistent"]

### Evidence Gap
[Specific gap statement]

### How This Study Addresses the Gap
[Connection to current study]

### Reference List
1. [Author(s). Title. Journal. Year;Volume:Pages. DOI]
...

---
✓ CHECKPOINT 2A — Confirm literature scope?
[OK] / [ADD: paper or topic] / [REMOVE: citation] / [REDIRECT: ...]
```

**STOP. Do not begin Story Writer until the researcher responds.**

---

## Self-Check Before Presenting

- [ ] At least 3 thematic sections (not annotated list)
- [ ] Evidence hierarchy respected — meta-analyses and RCTs weighted appropriately
- [ ] Gap statement is specific: names a paper, states what it didn't do
- [ ] "How this study addresses the gap" is proportional to the study design
- [ ] Search documentation is complete with exact query strings
- [ ] All user-provided references are accounted for
- [ ] No fabricated citations — every paper verifiably exists
- [ ] Contradictions explicitly addressed, not ignored

---

## Hard Rules

1. **NEVER fabricate references** — if a paper cannot be verified in PubMed or Scholar, do not cite it
2. **NEVER produce an annotated list** — theme synthesis is required
3. **NEVER restrict to 5 years by default** — foundational older papers are included when relevant
4. **NEVER write "little is known about X"** as the gap — always name the specific missing evidence
5. **NEVER search GEO, TCGA, or data repositories** — that is the researcher's domain
6. **NEVER begin Story Writer work during this phase**
7. If a user-provided paper appears low-relevance: flag it at CP 2A, do not silently exclude it

---

## Common Pitfalls

**Bad gap statement:** "The relationship between X and Y is not well understood."
**Good gap statement:** "While Johnson et al. (2022) demonstrated X in a small RCT (n=42),
no study has yet examined this relationship in patients with comorbid Z, which represents
approximately 40% of the clinical population [Smith 2021]."

**Bad synthesis:** "Several studies have found contradictory results for X."
**Good synthesis:** "The effect of X on Y remains contested. Three large cohort studies
(combined n > 5,000) report no significant association [1–3], whereas two RCTs (n=180, n=240)
show significant reductions [4,5]. The cohort studies adjusted for [confounders] not controlled
in the RCTs, suggesting the RCT findings may reflect confounding rather than a true effect."
