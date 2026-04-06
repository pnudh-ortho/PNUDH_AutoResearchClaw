---
name: organize
description: >
  Classify and move files from a session's archive/ folder into the correct stage directories.
  Also handles files dropped directly into input/[topic]/ at the project root (secondary intake).
  After organizing, reports what was found and suggests the next pipeline action.
  Triggers on: "정리해줘", "파일 정리", "organize", "sort files", "archive 정리",
  or when new files appear in archive/ during an active session.
metadata:
  category: pipeline
  trigger-keywords: "organize,sort,archive,정리,files,move,classify,stage,intake"
  applicable-stages: "any"
  priority: "0"
  version: "2.0"
  author: autoresearch
---

# Organize — Archive File Sorter

**Classify and move files from archive/ into the correct session stage directories.
Show the plan first. Move only after [OK]. Never delete. Never overwrite without asking.**

---

## Context to Load Before Starting

1. Run `autoresearch status` — find the active session ID and workspace path.
2. The archive directory is at: `sessions/[id]/archive/`
3. List all files in archive/ excluding README.md.
4. If archive/ is empty: "Archive is empty. No files to organize." — stop.

---

## Step 1 — Classify Each File

For every file in archive/, determine the correct destination using the rules below.

### By Extension (automatic)

| Extension | Default destination | Reason |
|---|---|---|
| `.csv`, `.tsv` | `input/` | Raw tabular data |
| `.xlsx`, `.xls` | Inspect (see below) | Could be raw data or analysis output |
| `.pdf` | Inspect (see below) | Could be reference paper or figure |
| `.bib`, `.ris`, `.nbib` | `stage2/literature/included_papers.bib` | Bibliography |
| `.png`, `.jpg`, `.jpeg`, `.tiff`, `.svg` | `stage1/figures/` | Figure image |
| `.docx`, `.doc` | Inspect (see below) | Could be manuscript draft or protocol |
| `.py` | Inspect (see below) | Analysis code or figure code |
| `.R`, `.r`, `.Rmd` | Inspect (see below) | Analysis code or figure code |
| `.txt`, `.log`, `.html` | Inspect (see below) | Analysis output or notes |
| `.sav`, `.sas7bdat`, `.dta` | `input/` | SPSS / SAS / Stata raw data |
| `.json` | Inspect (see below) | Analysis output or config |

### Content Inspection Rules (read first 30–50 lines)

**`.xlsx` / `.xls`**:
- If column headers include `p`, `p-value`, `p_val`, `OR`, `HR`, `CI`, `coefficient`, `β`, `mean ± SD`, `effect` → `stage1/analysis/analysis_results.txt` equivalent — save as `stage1/analysis/[filename]`
- Otherwise → `input/` (raw data)

**`.pdf`**:
- If first page contains: author names, journal name, DOI, year in citation format → `input/` (reference paper)
- If filename suggests figure (e.g., `fig1_`, `figure_`, `Figure_`) → `stage1/figures/`
- Otherwise → `input/` (unknown — flag as UNCLEAR)

**`.py`**:
- If contains `matplotlib`, `seaborn`, `plt.`, `sns.`, `fig,`, `ax =`, `subplots` → `stage1/figures/`
- Otherwise → `stage1/analysis/`

**`.R` / `.Rmd`**:
- If contains `ggplot`, `plot(`, `hist(`, `barplot(`, `geom_` → `stage1/figures/`
- Otherwise → `stage1/analysis/`

**`.txt` / `.log`**:
- If contains `p =`, `p<`, `t(`, `F(`, `χ²`, `U =`, `df =`, `95% CI`, `mean =`, `SD =`, `OR =`, `HR =` → `stage1/analysis/analysis_results.txt` (append or save as named file)
- Otherwise → `input/` (notes / context)

**`.docx` / `.doc`**:
- If contains section headers matching `## Methods`, `## Results`, `# Introduction`, `## Discussion`, `## Conclusion`, `## Abstract` → classify each matching section (see .md rules below)
- Otherwise → `input/` (protocol, notes, or other context)

**`.json`**:
- If contains `"figure"`, `"plot"`, `"chart"`, `"axes"` keys → `stage1/figures/`
- Otherwise → `stage1/analysis/`

**`.md` files** — match filename (case-insensitive):

| Filename pattern | Destination |
|---|---|
| `reviewer_a*`, `review_a*`, `*_a.md` | `stage3/reviewer_a.md` |
| `reviewer_b*`, `review_b*`, `*_b.md` | `stage3/reviewer_b.md` |
| `reviewer_c*`, `review_c*`, `*_c.md` | `stage3/reviewer_c.md` |
| `synthesis*`, `review_synthesis*` | `stage3/synthesis.md` |
| `methods*`, `method*` | `stage2/manuscript/methods.md` |
| `results*`, `result*` | `stage2/manuscript/results.md` |
| `discussion*` | `stage2/manuscript/discussion.md` |
| `conclusion*` | `stage2/manuscript/conclusion.md` |
| `introduction*`, `intro*` | `stage2/manuscript/introduction.md` |
| `abstract*` | `stage2/manuscript/abstract.md` |
| `outline*`, `story*`, `narrative*`, `arc*` | `stage2/story/outline.md` |
| `key_message*` | `stage2/story/key_message.md` |
| `literature*`, `synthesis*`, `search*` | `stage2/literature/` |
| `interpretation*` | `stage1/analysis/interpretation.md` |
| `analysis_plan*`, `plan*` | `stage1/analysis/analysis_plan.md` |
| `change_log*`, `changelog*` | `stage4/change_log.md` |
| `revision_checklist*` | `stage4/revision_checklist.md` |
| `revised_manuscript*` | `stage4/revised_manuscript.md` |
| `proofread*`, `proofreading*` | `stage4/proofread_report.md` |
| `response_letter*`, `rebuttal*` | `stage4/response_letter.md` |

---

## Step 2 — Handle Ambiguous Files

Files matching no rule above are **UNCLEAR**. For each:
- Show the filename
- Show the first 3 lines of content (if text file)
- List the 2–3 most likely destinations
- Do NOT guess — ask the researcher

Collect ALL ambiguous files before asking. Ask in one batch:

```
Ambiguous files — please specify destination for each:

1. study_notes.docx
   Content preview: "Patient selection criteria: aged 18-65, diagnosed with..."
   Options: (A) input/ — protocol/context   (B) stage2/manuscript/methods.md
   Your choice for each? [A/B/other path]
```

---

## Step 3 — Present the Plan

Show a formatted plan before moving anything:

```
File Organization Plan
──────────────────────────────────────────────────────────
  patient_data.csv            →  input/
  lab_results.xlsx            →  input/
  smith2023.pdf               →  input/
  spss_output.txt             →  stage1/analysis/analysis_results.txt
  fig1_boxplot.py             →  stage1/figures/
  reviewer_a.md               →  stage3/reviewer_a.md
  references.bib              →  stage2/literature/included_papers.bib
──────────────────────────────────────────────────────────
  7 files to move
  0 ambiguous (resolved above)

Conflicts detected (file already exists at destination):
  ⚠ stage3/reviewer_a.md already exists — overwrite or skip?

Proceed?  [OK] / [EDIT: filename → new destination] / [SKIP: filename]
```

Wait for `[OK]` before proceeding.

---

## Step 4 — Execute

For each file in the approved plan:

1. **Check if destination file already exists**:
   - If yes and user did not approve overwrite: skip and report
   - If yes and user approved overwrite: back up existing file as `[filename].bak` first, then overwrite
2. **Create destination directory if needed**: `mkdir -p path/to/dir`
3. **Move the file**: `mv "sessions/[id]/archive/[file]" "sessions/[id]/[destination]"`
4. Track results

---

## Step 5 — Report and Next Action

After completing all moves:

```
✓ Organization complete

Moved (7):
  ✓ patient_data.csv        →  input/
  ✓ smith2023.pdf           →  input/
  ✓ spss_output.txt         →  stage1/analysis/analysis_results.txt
  ✓ fig1_boxplot.py         →  stage1/figures/
  ✓ reviewer_a.md           →  stage3/reviewer_a.md
  ✓ references.bib          →  stage2/literature/included_papers.bib

Skipped (1):
  ✗ fig2_scatter.py         →  [already exists at destination, not overwritten]

Remaining in archive/ (0): —
```

**Next action suggestion** — based on what was just organized and current session state:

```
Suggested next steps based on what was organized:

1. reviewer_a.md added to stage3/ → check if all 3 reviews are now present:
   run `autoresearch run synthesis` if reviewer_b.md and reviewer_c.md also exist.

2. analysis_results.txt moved → Stage 1-B can now be completed:
   Load data-analysis skill to interpret the results.
```

Show 1–3 concrete suggestions. Do not prescribe — the researcher decides.

---

## Rules

- **Never delete** files from archive/ — always move (not copy-then-delete)
- **Never overwrite** without explicit per-file confirmation
- **Never move README.md** from archive/
- **If destination directory doesn't exist**: create it before moving
- **After organizing**: always run `autoresearch status` and show updated workspace summary
- **One batch of ambiguous questions** — do not ask file-by-file
