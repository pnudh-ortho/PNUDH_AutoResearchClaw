---
name: proofreader
description: >
  Final systematic proofreading of a biomedical manuscript after revision.
  Checks terminology consistency, citation completeness, figure cross-references,
  number consistency, and claim-evidence alignment. Use after Stage 4-A (revision)
  is complete, before final output.
  Triggers on: "proofread", "final check", "proofreader", "Stage 4-B",
  or when revision is complete and final approval is next.
metadata:
  category: writing
  trigger-keywords: "proofread,final check,consistency,citation,abbreviation,Stage 4-B"
  applicable-stages: "4"
  priority: "4"
  version: "1.0"
  author: autoresearch
---

# Proofreader

Run Stage 4-B of the AutoResearch pipeline.
**Final pass before CP 4. Flag issues — do not rewrite.**

## Checklist

### 1. Terminology Consistency
- Same term used throughout (e.g., "participants" not mixed with "patients" / "subjects")
- Abbreviations: defined on first use, used consistently thereafter
- Gene names: italicized (e.g., *BRCA1*); protein names: regular (e.g., BRCA1)
- Drug/compound names: consistent (generic vs. brand — one throughout)

### 2. Citation Completeness
- Every in-text citation appears in the reference list
- Every reference list entry is cited in the text (no orphans)
- Citation format consistent throughout
- Every factual claim has a citation or is from this study's own data

### 3. Figure & Table Cross-References
- Every figure cited in text before it appears: "Figure 1", "Figure 2A"
- Figure numbers are sequential and match the order of appearance
- Every table cited in text
- No orphaned figures or tables (cited but missing, or present but uncited)
- Multi-panel labels (A, B, C…) referenced consistently in text and captions

### 4. Number & Statistics Consistency
- Statistics in text match figures and tables exactly
- n per group consistent throughout all sections
- Percentages sum correctly where applicable
- Units consistent (e.g., mg/dL not mixed with mg/dl)
- Decimal places consistent per metric type

### 5. Claim-Evidence Alignment
- Abstract claims supported by Results
- Conclusion claims supported by Discussion
- No new statistics appear in Introduction or Conclusion
- No overclaiming in Abstract (flag "demonstrates" / "proves" / "shows" for pilot studies)

## Output Format

```
## Proofreading Report

### Terminology Issues
1. [Term] — inconsistent: "[usage A]" (Methods, para 2) vs. "[usage B]" (Results, para 1)
   → Recommend: use "[preferred term]" throughout

### Citation Issues
1. [Claim location] — uncited claim. Needs reference or attribution to study data.

### Figure/Table Cross-Reference Issues
1. "Figure 4" cited in Results para 3 — figure sequence shows this is Figure 3.
   Verify figure order and renumber.

### Number/Statistics Inconsistencies
1. Results text: "n=45 per group" — Table 1 shows n=44 in Group A. Verify source.

### Claim-Evidence Issues
1. Abstract: "demonstrates efficacy" — Results report p=.034, d=0.32 from a pilot study.
   Suggest: "suggests potential efficacy pending larger validation."

### Clean Sections
[Sections and elements that passed all checks — listed explicitly]

---
✓ CHECKPOINT 4 — Proofreading complete
Approve final output? [OK] / [FIX: ...]
```

## Hard Rules

1. Flag and specify — do not rewrite; the researcher decides
2. Be exhaustive on cross-references — missed figure numbers cause desk rejection
3. Flag overclaiming in Abstract and Conclusion — editors read these first
4. Report clean sections explicitly — helps the researcher know what is verified
