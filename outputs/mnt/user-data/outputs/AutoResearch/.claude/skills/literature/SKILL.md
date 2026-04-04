---
name: literature
description: >
  Systematic literature search and synthesis for biomedical research papers.
  Mandatory stage — runs even when the user has provided references.
  Expands the knowledge base via PubMed and Google Scholar with no date cutoff.
  Use at the start of Stage 2, before Story Writer begins.
  Triggers on: "literature", "search papers", "knowledge base", "Stage 2-A",
  or when narrative arc design is next in the pipeline.
metadata:
  category: experiment
  trigger-keywords: "literature,review,PubMed,search,citation,reference,background,knowledge base,Stage 2"
  applicable-stages: "2"
  priority: "1"
  version: "1.0"
  author: autoresearch
  references: "adapted from literature-search skill (AutoResearchClaw)"
---

# Literature

Run Stage 2-A of the AutoResearch pipeline.
**Must complete before Story Writer begins.**

## Search Strategy

1. Start with user-provided references as the core set — do not discard or replace them
2. Identify 2–4 core concepts from the research question using PICO when applicable
   (Population, Intervention/Exposure, Comparison, Outcome)
3. List synonyms, abbreviations, and MeSH terms for each concept
4. Combine with Boolean operators: AND between concepts, OR within synonyms
5. Run searches on: PubMed, Google Scholar (minimum); add Scopus or Web of Science
   if the topic warrants it
6. **No date restriction by default** — seminal foundational papers from any era are
   included if directly relevant; note publication year prominently
7. Document exact search strings for reproducibility

## Screening

1. Title/abstract screen against relevance to the research question
2. Full-text review for borderline papers
3. Include: peer-reviewed articles, relevant preprints if seminal
4. Do not inflate reference count with tangentially related papers
5. Flag any user-provided references that appear low-relevance — raise at CP 2A

## Synthesis

Organize findings by **theme**, not as an annotated list. Per theme:
- Summarize state of evidence in 2–4 sentences
- Note: sample sizes, methodologies, strength of evidence
- Highlight: contradictions, debates, limitations of prior work
- Connect to the current study's findings (supports / contradicts / extends)

Required sections in synthesis output:
1. **Core background themes** (2–4 themes, each 2–4 sentences)
2. **Contradictions or unresolved debates** in the literature
3. **Gap statement**: what the current literature lacks, in 1–2 sentences
4. **How the current study addresses that gap**
5. **Full reference list** (all included papers, citation format consistent)

### ✓ CHECKPOINT 2A
Present synthesis. Wait for `[OK]` / `[ADD: paper/topic]` / `[REMOVE: ...]` / `[REDIRECT: ...]`.
Do not proceed to Story Writer until confirmed.

## Search Documentation Block (include in output)

```
## Search Summary
Databases: PubMed, Google Scholar [+ others if used]
Search terms: [list per concept]
Results: [n] identified → [n] screened → [n] included
Date range: No restriction (last search: [date])
User-provided papers: [n] (listed separately)
```

## Common Pitfalls

1. Never fabricate references — if existence cannot be verified, do not include
2. Never produce an annotated list — synthesis by theme is required
3. Never restrict to 5 years by default — foundational older papers are explicitly included
4. Do not search GEO, TCGA, or data repositories — that is the user's domain
5. Flag conflicts between user-provided papers and search results at CP 2A
6. Do not begin Story Writer work during this phase
