---
name: story-writer
description: >
  Design the narrative architecture of a biomedical paper before any prose is written.
  Produces a key message, narrative arc, and section-by-section outline (blueprint).
  Does NOT write actual manuscript text. Use after literature (Stage 2-A) is confirmed.
  Triggers on: "story", "narrative", "outline", "key message", "Stage 2-B",
  or when CP 2A has been cleared.
metadata:
  category: writing
  trigger-keywords: "story,narrative,outline,key message,arc,structure,blueprint,Stage 2-B"
  applicable-stages: "2"
  priority: "2"
  version: "1.0"
  author: autoresearch
  references: "adapted from hypothesis-formulation skill (AutoResearchClaw)"
---

# Story Writer

Run Stage 2-B of the AutoResearch pipeline.
**Must reference Stage 1 output (confirmed figures + statistical interpretation).**
**Does NOT write prose — produces the blueprint Section Writer will follow.**

## Step 1 — Derive the Key Message

One sentence answering: "What did we find, and why does it matter?"

Requirements:
- Specific: names the finding, population, direction, and context
- Grounded: directly traceable to confirmed analysis results (Stage 1)
- Connected: addresses the gap identified in literature synthesis (Stage 2-A)
- Proportional: calibrated to what the data actually supports — no overclaiming

If the data does not support a strong key message, state this clearly at CP 2B.
Do not manufacture a key message that the analysis cannot sustain.

**Strong example:**
> "In patients with early-stage Disease Y (n=88), Treatment X reduced Biomarker Z
> by 34% (p=.008, d=0.71), suggesting a mechanistic role warranting validation
> in larger trials."

**Weak examples to avoid:**
> "Our study found differences in outcomes." (too vague)
> "Treatment X is effective for Disease Y." (overclaims a pilot study)

## Step 2 — Design the Narrative Arc

Map how each section contributes to the key message:

**Introduction funnel:** broad context → specific gap → our approach (do not reveal findings)
**Methods:** design justification → key methodological choices → statistical approach (reference Stage 1-A plan)
**Results:** primary finding first (highest effect size / most central claim) → supporting evidence in logical order → null findings reported honestly
**Discussion:** restate key finding (1 sentence) → literature context (confirm/contradict/extend) → mechanistic interpretation (label as interpretation, not fact) → limitations (specific, not generic) → implications (proportional to data)
**Conclusion:** key message restated + forward-looking statement
**Abstract:** last — synthesizes everything (written by Section Writer last)

## Step 3 — Section-by-Section Outline

For each section produce:
- **Purpose** (2–3 sentences): what this section must achieve
- **Key points** (bulleted): content that must appear, in order
- **Assigned figures/tables** (from Stage 1-B confirmed list)
- **Transition** (1 sentence): how this section leads into the next
- **Flags**: where data is weak, claims need softening, or gaps exist in the arc

Section order in outline:
Methods → Results → Discussion → Conclusion → Introduction → Abstract

Note: The outline is produced in this order even though Section Writer writes in the same order.
Abstract outline is a placeholder — Section Writer fills it last.

### ✓ CHECKPOINT 2B
Present: key message + narrative arc summary + section outlines.
Wait for `[OK]` / `[REVISE: ...]` / `[REDIRECT: ...]`.
**Section Writer does not begin until this is confirmed.**

## Common Pitfalls

1. Never start writing section prose — outline and bullet points only
2. Never place a figure in a section where it doesn't belong
3. Never overclaim in the key message — if data is exploratory, the arc must say so
4. Never leave a story gap unacknowledged — flag it at CP 2B
5. Never design an arc that contradicts the statistical interpretation from Stage 1
6. "Further research is needed" is not a limitation — require specific limitations
