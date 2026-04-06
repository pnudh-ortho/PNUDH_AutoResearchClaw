---
name: proofreader
description: >
  Final systematic proofreading of a biomedical manuscript after Stage 4-A revision.
  Checks terminology consistency, abbreviations, citation completeness, figure cross-references,
  number and statistics consistency, claim-evidence alignment, gene/protein formatting,
  and mandatory statement completeness. Flags issues only — does not rewrite.
  Triggers on: "proofread", "final check", "Stage 4-B",
  or when revision (Stage 4-A) is complete and final output is next.
metadata:
  category: proofreader
  trigger-keywords: "proofread,final check,consistency,citation,abbreviation,figures,statistics,Stage 4-B,gene,formatting"
  applicable-stages: "4"
  priority: "4"
  version: "2.0"
  author: autoresearch
---

# Proofreader — Stage 4-B

**Final systematic pass. Flag and specify — do not rewrite. The researcher decides on every issue.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — confirm Stage 4-A is complete.
2. Read the revised manuscript: `sessions/[id]/stage4/revised_manuscript.md`
   or assemble from `sessions/[id]/stage2/manuscript/` if no revision was run.
3. Read `sessions/[id]/stage1/analysis/analysis_results.txt` — for statistics consistency check.
4. Note the session's figure count from `sessions/[id]/stage1/figures/` (count fig*.py or fig*.R files).
5. Check `config.autoresearch.yaml` for `stage2.writing.word_limits` (if set).

---

## Check 1: Terminology Consistency

Scan the full manuscript for inconsistent use of synonymous terms.

**Common biomedical term conflicts to check:**
- "participants" vs. "patients" vs. "subjects" vs. "cases" vs. "individuals"
- "controls" vs. "control group" vs. "comparison group"
- Study design terms: "randomized" vs. "randomly assigned" (use one)
- Drug/compound: generic name vs. brand name (one throughout; generic preferred)
- Gene/variant: use the same notation throughout

**Process:**
1. Identify all terms used for each core concept (use search)
2. Count occurrences of each variant
3. Recommend the preferred term (most frequent or most precise)
4. Report each instance of the non-preferred term with its location

**Report format:**
```
Terminology Issue 1: "participants" (n=14) vs. "patients" (n=3) vs. "subjects" (n=2)
  Preferred: "participants" (most frequent)
  Non-preferred instances:
    - "patients": Methods para 3 ("patients were excluded if..."); Results para 1 ("patients showed...")
    - "subjects": Methods para 2 ("subjects were recruited..."); Discussion para 4 ("subjects in this study...")
  → Replace all non-preferred instances with "participants"
```

---

## Check 2: Abbreviations

**Rule**: every abbreviation must be defined on first use in each section independently (Abstract and body text are separate documents for this purpose).

**Process:**
1. List all abbreviations appearing in the manuscript
2. For each, find the first occurrence in: (a) Abstract, (b) main text
3. Verify the definition appears at that first occurrence
4. Check that the abbreviation is used consistently (same form throughout)
5. Flag abbreviations used fewer than 3 times in the main text (should be spelled out instead)

**Report format:**
```
Abbreviation Issue 1: "SGLT-2" used in Introduction paragraph 2 before first definition.
  First definition found: Methods paragraph 1. 
  → Move "sodium-glucose cotransporter-2 (SGLT-2)" to Introduction paragraph 2.

Abbreviation Issue 2: "IRB" defined in Methods, but not defined in Abstract where it appears.
  → Add "institutional review board (IRB)" on first use in Abstract.

Abbreviation Issue 3: "GFR" used only once in Discussion ("glomerular filtration rate (GFR) was noted").
  → Spell out fully; remove abbreviation (used only once).
```

---

## Check 3: Figure and Table Cross-References

**Rule**: every figure and table must be cited in the text before it appears; citations must be in sequential order.

**Process:**
1. Extract all figure citations from the text: `Figure 1`, `Fig. 1`, `Figure 1A`, etc.
2. Record the text location (section, paragraph) of each citation
3. Verify: figures are cited in order (Figure 1 before Figure 2, etc.)
4. Verify: every expected figure is cited at least once
5. Verify: no figure is cited that does not exist

**Report format:**
```
Figure Reference Issue 1: Figure 3 is cited in Results paragraph 2, but Figure 2 is not cited until Results paragraph 4.
  → Figures must be cited in sequential order. Check: is Figure 2 missing from the text, or is the citation out of order?

Figure Reference Issue 2: Figure 4 expected (4 figure scripts found in stage1/figures/) but not cited anywhere in the manuscript.
  → Either add a citation for Figure 4 or remove the figure if unused.

Table Reference Issue 1: Table 2 cited in Methods but Table 1 is not cited until Discussion.
  → Verify table numbering and citation order.
```

---

## Check 4: Number and Statistics Consistency

Compare every quantitative value in the text against its source.

**Step 4.1 — Sample sizes:**
- Total N stated in Methods → consistent in Results, Abstract, and figures?
- n per group stated in Methods → consistent in Results and figure legends?
- List any discrepancy with exact locations of all occurrences

**Step 4.2 — Statistics:**
Compare manuscript text against `analysis_results.txt`:
- Every p-value, test statistic, effect size, and CI must match exactly
- Units must be consistent: mg/dL throughout (not mixed with mg/dl or mmol/L)
- Decimal places: consistent per metric type (p-values to 3 decimal places; measurements to appropriate significant figures)

**Step 4.3 — Percentages:**
- Percentages must sum to ~100% where they describe a complete distribution
- Calculated percentages must match the reported n values: "34% of 88 = 29.9 ≈ 30 patients" — verify

**Report format:**
```
Statistics Issue 1: Results paragraph 2 reports "p = .038" but analysis_results.txt shows "p = 0.034".
  → Verify: transcription error or rounding. Correct to match the actual analysis output.

Statistics Issue 2: Methods states "n = 88 total" but Table 1 column totals sum to 86.
  → Identify the discrepancy: were 2 patients excluded before table construction? If so, explain in Methods.

Statistics Issue 3: "SD" used for error bars in Figure 1 legend but text says "SEM" for the same data.
  → Confirm which is correct; update the inconsistent location.
```

---

## Check 5: Claim-Evidence Alignment

Verify that Abstract and Conclusion match the Results and Discussion of the manuscript.

**Abstract claims → Results evidence:**
- Every quantitative claim in Abstract must appear in Results with matching values
- "Significant" in Abstract: verify p-value is < .05 in Results
- Any claim of direction ("reduced", "increased", "no difference") must match Results direction

**Conclusion claims → Discussion support:**
- Every recommendation or implication in Conclusion must be argued in Discussion
- No new results or claims in Conclusion
- No stronger language in Conclusion than Discussion ("Treatment A is recommended" if Discussion says "warrants further study")

**Overclaiming terms — flag every occurrence in Abstract and Conclusion:**
| Term | Problem | Suggested replacement |
|---|---|---|
| "demonstrates" | Too strong for observational/pilot | "suggests", "indicates" |
| "proves" | Never appropriate in empirical research | "provides evidence that" |
| "confirms" | Implies definitive replication | "is consistent with", "supports" |
| "shows that X causes Y" | Causation from observational data | "is associated with", "may contribute to" |
| "clearly" | Rhetorical, not scientific | Remove or replace with specific evidence |
| "obviously" | Same | Remove |

**Report format:**
```
Claim Issue 1: Abstract Conclusion states "Treatment A is effective for Disease Y."
  Evidence in Results: p = .034, d = 0.32 (small-to-medium effect), n = 88 (single center, pilot).
  → Replace with: "Treatment A was associated with significantly lower [outcome] in this pilot study, warranting evaluation in larger trials."

Claim Issue 2: Conclusion introduces "This finding has immediate clinical implications" — not argued in Discussion.
  → Either add a Discussion paragraph arguing this, or remove from Conclusion.
```

---

## Check 6: Gene, Protein, and Nomenclature Formatting

**Gene symbols — italicized, species-specific case:**
| Species | Format | Example |
|---|---|---|
| Human | Uppercase italic | *BRCA1*, *TP53*, *VEGFA* |
| Mouse | First letter uppercase, rest lowercase italic | *Brca1*, *Tp53*, *Vegfa* |
| Rat | Same as mouse | *Brca1* |
| Drosophila | Lowercase italic | *brca1* |

**Protein names — NOT italicized, species-independent:**
- Human protein: BRCA1, TP53, VEGF-A
- Mouse protein: BRCA1 (same as human — not italicized)

**Common errors to check:**
- Gene name not italicized: `BRCA1` → `*BRCA1*`
- Protein name italicized: `*p53*` → `p53`
- Inconsistent case: `VEGF` vs. `VEGFA` vs. `VEGF-A` (pick one and use throughout)
- Drug names: generic name in lowercase (empagliflozin, not Empagliflozin, except at sentence start)

**Report format:**
```
Gene Formatting Issue 1: "BRCA1" (not italicized) appears in Methods paragraph 2 and Results paragraph 1.
  → Italicize: *BRCA1* in both locations.

Gene Formatting Issue 2: "p53" (protein) is italicized in Discussion paragraph 3.
  → Remove italics from protein name: p53.
```

---

## Check 7: Mandatory Statements

Verify the following required statements are present in the manuscript:

| Statement | Required location | Present? |
|---|---|---|
| Ethics / IRB approval | Methods | [ ] |
| Declaration of Helsinki compliance | Methods (or Ethics subsection) | [ ] |
| Informed consent statement | Methods | [ ] |
| Conflict of interest disclosure | Dedicated section or Methods | [ ] |
| Funding acknowledgment | Acknowledgments or Methods | [ ] |
| Data availability statement | Dedicated section or end of Methods | [ ] |
| Author contributions (CRediT taxonomy) | Dedicated section | [ ] (if journal requires) |

**Report format:**
```
Mandatory Statement Issue 1: No data availability statement found.
  → Add to end of Methods or as a separate section: "The dataset analyzed in this study is available from the corresponding author upon reasonable request." (or specify the repository).

Mandatory Statement Issue 2: Conflict of interest statement absent.
  → Add before References: "The authors declare no conflicts of interest." (or specify actual COI).
```

---

## Check 8: Word Count Verification

Check section word counts against targets (from config.autoresearch.yaml or defaults):

| Section | Default target | Actual count | Status |
|---|---|---|---|
| Abstract | ≤ 250 words | [count] | [OK / Over / Under] |
| Methods | 500–900 | [count] | [OK / Over / Under] |
| Results | 700–1,100 | [count] | [OK / Over / Under] |
| Discussion | 900–1,400 | [count] | [OK / Over / Under] |
| Introduction | 400–650 | [count] | [OK / Over / Under] |
| Conclusion | 150–250 | [count] | [OK / Over / Under] |

Flag sections significantly over/under target. Note: these are guidelines, not hard limits.

---

## Output Format

```
## Proofreading Report — Stage 4-B
Total issues: [N] ([major count] requiring researcher review)

### Check 1: Terminology Consistency
[Issues, or "No issues found. ✓"]

### Check 2: Abbreviations
[Issues, or "All abbreviations properly defined. ✓"]

### Check 3: Figure & Table Cross-References
[Issues, or "All figures and tables cited in order. ✓"]

### Check 4: Number & Statistics Consistency
[Issues, or "All values consistent with analysis output. ✓"]

### Check 5: Claim-Evidence Alignment
[Issues, or "Abstract and Conclusion consistent with manuscript body. ✓"]

### Check 6: Gene / Protein Formatting
[Issues, or "No gene or protein names found / All correctly formatted. ✓"]

### Check 7: Mandatory Statements
[Missing statements, or "All required statements present. ✓"]

### Check 8: Word Count
[Table with counts per section]

### Clean Sections
The following passed all checks without any flagged issues:
- [Section name] ✓

---
✓ CHECKPOINT 4 — Proofreading complete
Approve final output?  [OK] → export  |  [FIX: ...]
```

---

## Hard Rules

1. **Flag and specify — do not rewrite** — the researcher makes every correction decision
2. **Quote exact locations** — "Methods paragraph 2, sentence 3" not "somewhere in Methods"
3. **Be exhaustive on figure references** — a missed figure number causes desk rejection
4. **Report clean sections explicitly** — researchers need to know what is verified, not just what is wrong
5. **Flag all overclaiming** in Abstract and Conclusion — editors read these first
6. **Every check must be run** — skipping any check produces an incomplete proofread
