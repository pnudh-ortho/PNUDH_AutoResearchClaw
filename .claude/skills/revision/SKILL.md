---
name: revision
description: >
  Execute manuscript revision based on a confirmed review synthesis checklist.
  Makes only the changes the researcher approved at CP 7. Logs every change with location,
  what changed, and cascade effects. Generates a reviewer response letter after revision.
  Use after CP 7 (researcher has confirmed revision scope).
  Triggers on: "revise", "revision", "address comments", "Stage 8",
  or when CP 7 has been cleared with a revision scope decision.
metadata:
  category: revision
  trigger-keywords: "revise,revision,address,comments,checklist,Stage 8,response letter,rebuttal"
  applicable-stages: "8"
  priority: "8"
  version: "2.0"
  author: autoresearch
---

# Revision Agent — Stage 8

**Execute confirmed checklist items only. Do not make unrequested changes.
Log every single edit. Flag cascade effects immediately.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — confirm CP 7 is cleared.
2. Read `sessions/[id]/stage8/revision_checklist.md` — the confirmed checklist with researcher decisions (ADDRESS / DECLINE / OPTIONAL).
3. Read `sessions/[id]/stage7/synthesis.md` — the full review synthesis for context.
4. Read the most recent manuscript version:
   - `sessions/[id]/stage8/revised_manuscript.md` if it exists (prior revision pass)
   - Otherwise: assemble from `sessions/[id]/stage6/*.md`
5. Read `sessions/[id]/stage8/change_log.md` — to continue numbering from the last entry.

---

## Step 1 — Triage the Checklist

Group checklist items by type before starting:

| Status | Action |
|---|---|
| ADDRESS | Must revise — process in order of severity (Major first) |
| OPTIONAL | Revise only if confirmed at CP 7; skip otherwise |
| DECLINE | Do NOT revise; record rebuttal rationale in change log |

Within ADDRESS items: process Major concerns before Minor, to detect cascades early.

---

## Step 2 — Execute Each Change

For every ADDRESS item:

### 2.1 Locate the Exact Passage

Read the checklist item carefully:
- Location: "Results, paragraph 2" or "Discussion, sentence beginning 'Treatment A demonstrates...'"
- Find the exact text in the manuscript
- If location is ambiguous: flag the ambiguity before making any change (see Hard Rules)

### 2.2 Make the Minimum Necessary Change

Revision philosophy: **surgical, not structural**.
- Fix the specific problem identified — do not rewrite surrounding text unless the fix requires it
- If adding a missing statistic: insert it with exact formatting from Stage 3 (copy the exact value from analysis_results.txt)
- If softening an overclaim: change the specific word/phrase, not the whole sentence
- If adding a limitation: add it to the Limitations paragraph, not to a new location

**Example of minimum necessary change:**

Checklist item: "Reviewer A-02: Missing effect size for primary outcome in Results paragraph 2."
```
Before: "Treatment A showed significantly lower levels (p = .034)."
After:  "Treatment A showed significantly lower levels (U = 234, p = .034, r = 0.42
        [95% CI: 0.18, 0.62])."
```
Note: changed only what was missing. Did not rephrase the surrounding sentence.

### 2.3 Check for Cascade Effects

After every change, ask:
- Does this change affect a value, term, or claim that appears elsewhere in the manuscript?
- Does this change affect the Abstract?
- Does this change require a figure to be updated?
- Does this change create an inconsistency with any other section?

Cascade checklist (check after each change):
- [ ] Abstract references the same finding → same change needed there?
- [ ] Conclusion references this finding → same change needed there?
- [ ] Methods describes a procedure relevant to this fix → consistent?
- [ ] Figure caption references this value → consistent?

If cascade detected: make the cascading change and log it as a sub-entry under the primary change.

### 2.4 Log Every Change

Every change — including cascades — must be logged immediately.

**Change log entry format:**
```
| [#] | [Checklist ID] | [Location] | [Change made] | [Cascade effects] |
| 3   | RA-02          | Results, para 2, sentence 3 | Added effect size: "r = 0.42 [95% CI: 0.18, 0.62]" | Abstract Results sentence also updated (entry 4) |
| 4   | RA-02 (cascade)| Abstract, Results subsection | Added "r = 0.42 [95% CI: 0.18, 0.62]" to match Results | None |
```

---

## Step 3 — Handle Declined Items

For every DECLINE item:
- Do NOT make any change to the manuscript
- Record in the "Items Not Addressed" table with the researcher's stated rationale
- Ensure the rebuttal rationale is specific enough for a journal response letter

**Minimum acceptable rebuttal:**
```
| RB-01 | Reviewer B #1: generalizability concern | "Single-center recruitment is acknowledged in Limitations (para 5). The enrolled population represents the urban tertiary care context where this intervention is most commonly applied. We will acknowledge this in the response letter." |
```

---

## Step 4 — Generate Reviewer Response Letter

After all revisions are complete, draft the response letter. This is a mandatory output of Stage 8.

**Letter structure:**

```
Dear Editors and Reviewers,

We sincerely thank the reviewers for their thorough and constructive feedback.
The manuscript has been substantially improved as a result. Below, we address
each comment point by point.

All changes are highlighted in the revised manuscript (tracked changes or [brackets]).

---

## Response to Reviewer A

### Comment A-01: [Title from checklist]

**Reviewer's concern:**
"[Exact quote or close paraphrase of the reviewer's comment]"

**Our response:**
[How you addressed it — be specific. Reference the change made.]
[If addressed: "We have added the missing effect size (r = 0.42 [95% CI: 0.18, 0.62])
to Results paragraph 2 and the Abstract. The revised text reads: '...']"
[If declined: "We respectfully disagree with this concern because [specific reason].
We have added language to the Limitations section acknowledging [the underlying issue]."]

**Manuscript change:**
[Specific: "Results paragraph 2: added 'r = 0.42 [95% CI: 0.18, 0.62]'" | "No change — see rationale above"]

---

### Comment A-02: [Next comment]
[Same structure]

---

## Response to Reviewer B

### Comment B-01: [Title]
[Same structure]

---

## Response to Reviewer C

### Comment C-01: [Title]
[Same structure]

---

We believe these revisions substantially strengthen the manuscript and
address the reviewers' concerns comprehensively. We look forward to
your further consideration.

Sincerely,
[Author names — researcher fills in]
```

**Rules for the response letter:**
- Every reviewer comment gets a response — no comment is left unaddressed
- For addressed items: quote the change made with the exact new text
- For declined items: explain the scientific rationale, not just "we disagree"
- Tone: professional, not defensive; "we thank the reviewer" for concerns, not praise
- Never say "as we already stated" — restate the information clearly

---

## Step 5 — Final Output

Produce three files:

1. **`sessions/[id]/stage8/revised_manuscript.md`**:
   Full revised manuscript with all accepted changes incorporated.

2. **`sessions/[id]/stage8/change_log.md`** (appended):
   All changes with IDs, locations, before/after text, and cascade notes.
   Plus "Items Not Addressed" table with rebuttal rationales.

3. **`sessions/[id]/stage8/response_letter.md`** (new):
   Reviewer response letter ready for researcher to personalize and submit.

---

## Output Format for Change Log

```
## Revision Change Log — Stage 8

| # | Checklist item | Location | Before | After | Cascade effects |
|---|---|---|---|---|---|
| 1 | RA-02: Missing effect size | Results, para 2 | "...significantly lower (p = .034)." | "...significantly lower (U=234, p=.034, r=0.42 [95% CI: 0.18, 0.62])." | Abstract updated (entry 2) |
| 2 | RA-02 (cascade) | Abstract, Results | "...significantly lower (p=.034)." | "...significantly lower (p=.034, r=0.42)." | None |

## Items Not Addressed (Researcher Decision)

| # | Item | Reason not addressed | Rebuttal rationale |
|---|---|---|---|
| 1 | RB-01: Generalizability | Researcher decision: DECLINE | "Single-center design is acknowledged in Limitations para 5; population is appropriate for intervention context." |

## Additional Flags

[Any cases where the requested change created an inconsistency elsewhere that
the researcher should review. Any checklist items where the requested change was
ambiguous — state how the ambiguity was resolved.]
```

---

## Self-Check Before Presenting

- [ ] All ADDRESS items processed (Major before Minor)
- [ ] All DECLINE items logged with rebuttal rationale
- [ ] Every change (including cascades) has a log entry
- [ ] Abstract checked for cascade after every Results or Discussion change
- [ ] Revised manuscript is a single coherent document (sections assembled correctly)
- [ ] Response letter covers every reviewer comment without exception
- [ ] No unrequested changes made
- [ ] Additional flags section lists any noticed problems (do NOT silently fix them)

---

## Hard Rules

1. **NEVER make unrequested changes** — if a new problem is noticed while revising, add it to "Additional Flags" at the end of the log; do not silently fix it
2. **NEVER make a change without a log entry** — no undocumented edits
3. **Minimum necessary change** — do not rewrite a paragraph when a sentence change suffices
4. **If a checklist item is ambiguous**: state the ambiguity explicitly before acting — "Item RA-03 asks to 'clarify the statistical method' but does not specify where or how. I interpret this as [X]. Proceed? [OK] / [CLARIFY: ...]"
5. **Every cascade must be resolved** — a change in Results that leaves the Abstract inconsistent is an error
6. **Response letter is mandatory** — revisions without a response letter are incomplete deliverables
