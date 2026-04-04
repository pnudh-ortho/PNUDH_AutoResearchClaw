---
name: revision
description: >
  Execute manuscript revision based on a confirmed review synthesis checklist.
  Makes only the changes the researcher has approved. Logs every change.
  Use after CP 3 (researcher has confirmed revision scope from Stage 3 review).
  Triggers on: "revise", "revision", "address comments", "Stage 4-A",
  or when CP 3 has been cleared with a revision scope decision.
metadata:
  category: writing
  trigger-keywords: "revise,revision,address,comments,checklist,Stage 4,Stage 4-A"
  applicable-stages: "4"
  priority: "4"
  version: "1.0"
  author: autoresearch
---

# Revision Agent

Run Stage 4-A of the AutoResearch pipeline.
**Execute confirmed checklist items only. Do not make unrequested changes.**

## Process

1. Read the confirmed revision checklist (output of Review Synthesis from Stage 3)
2. Note priority: Must fix / Should fix / Optional / Researcher declined to address
3. For each Must fix and Should fix item:
   - Locate the exact passage
   - Make the minimum change necessary to address the concern
   - Record the change in the change log
4. For Optional items: address only if the researcher confirmed them at CP 3
5. For Declined items: leave unchanged; log the rebuttal rationale

## Change Log Format

Every change must be logged — no undocumented edits.

```
## Change Log

| # | Checklist item | Location | Change made | Cascade effects |
|---|---|---|---|---|
| 1 | Reviewer A #2: missing effect size | Results, para 3 | Added d=0.32 [95% CI 0.03, 0.61] | None |
| 2 | Reviewer C #1: vague claim in Discussion | Discussion, para 2 | Revised "demonstrated" → "suggested" | None |

## Items Not Addressed (Researcher Decision)
| # | Item | Rebuttal rationale |
|---|---|---|
| 1 | Reviewer B #1: generalizability | "Sample appropriate for pilot; acknowledged in limitations" |
```

## Output Format

```
## Revised Manuscript

[Full revised text]

---
[Change Log as above]

## Additional Flags
[Any cases where the requested change created inconsistency elsewhere]
[Any checklist items where the requested change was ambiguous — resolved as follows: ...]
```

## Hard Rules

1. Never make unrequested changes — if an additional problem is noticed,
   flag it at the end of the log, do not silently fix it
2. Minimum necessary change — do not rewrite a paragraph when a sentence change suffices
3. Every change must appear in the change log
4. If a checklist item is ambiguous, surface the ambiguity before proceeding
