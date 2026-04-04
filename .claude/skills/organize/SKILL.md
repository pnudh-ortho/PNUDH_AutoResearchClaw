# Skill: Archive Organizer

Organize files from a session's `archive/` folder into the correct stage directories.

## Trigger

This skill activates when the user says any of:
- "archive 정리해줘" / "정리해줘" / "파일 정리"
- "organize archive" / "sort files"
- "archive 폴더 정리"

---

## Step 1 — Locate the session and archive

Run `autoresearch status` to find the active session and its workspace path.

The archive directory is at:
```
sessions/<session-id>/archive/
```

List all files in archive/ (excluding README.md).  
If the archive is empty, tell the user and stop.

---

## Step 2 — Classify each file

For every file in archive/, determine the destination using these rules:

### By extension (automatic)

| Extension | Destination | Reason |
|---|---|---|
| `.csv`, `.tsv`, `.xlsx`, `.xls` | `input/` | Raw data |
| `.pdf` | `input/` | Reference paper |
| `.bib` | `stage2/literature/` | Bibliography |
| `.png`, `.jpg`, `.jpeg`, `.svg`, `.tiff`, `.tif` | `stage1/figures/` | Figure image |
| `.docx` | `input/` | Document (data or ref) |

### By extension + content inspection

**`.py` files** — read first 20 lines:
- Contains `matplotlib`, `seaborn`, `plt.`, `sns.`, `fig,`, `ax` → `stage1/figures/`
- Otherwise → `stage1/analysis/`

**`.R` files** — read first 20 lines:
- Contains `ggplot`, `plot(`, `hist(`, `barplot(` → `stage1/figures/`
- Otherwise → `stage1/analysis/`

**`.txt` files** — read first 30 lines:
- Contains `p =`, `p<`, `t(`, `F(`, `χ²`, `df =`, `CI`, `mean`, `SD`, `median` → `stage1/analysis/` (statistics output)
- Otherwise → `input/`

**`.json` files**:
- Contains `"figure"`, `"plot"`, `"chart"` keys → `stage1/figures/`
- Otherwise → `stage1/analysis/`

### By filename (for `.md` files)

Match the filename (case-insensitive) against these patterns:

| Filename pattern | Destination |
|---|---|
| `reviewer_a*`, `review_a*`, `*_a.md` | `stage3/reviewer_a.md` |
| `reviewer_b*`, `review_b*`, `*_b.md` | `stage3/reviewer_b.md` |
| `reviewer_c*`, `review_c*`, `*_c.md` | `stage3/reviewer_c.md` |
| `synthesis*` | `stage3/synthesis.md` |
| `methods*`, `method*` | `stage2/manuscript/methods.md` |
| `results*`, `result*` | `stage2/manuscript/results.md` |
| `discussion*` | `stage2/manuscript/discussion.md` |
| `conclusion*` | `stage2/manuscript/conclusion.md` |
| `introduction*`, `intro*` | `stage2/manuscript/introduction.md` |
| `abstract*` | `stage2/manuscript/abstract.md` |
| `outline*`, `story*`, `narrative*` | `stage2/story/` |
| `key_message*` | `stage2/story/key_message.md` |
| `literature*`, `search*` | `stage2/literature/` |
| `interpretation*` | `stage1/analysis/interpretation.md` |
| `analysis_plan*`, `plan*` | `stage1/analysis/analysis_plan.md` |
| `change_log*`, `changelog*` | `stage4/change_log.md` |
| `proofread*` | `stage4/proofread_report.md` |

---

## Step 3 — Handle ambiguous files

Files that don't match any rule above are **ambiguous**. For each one:
- Show the filename and first 3 lines of content (if text)
- List the possible destinations
- Ask the user which folder to use

Collect all ambiguous files first, then ask in one batch — don't ask one-by-one.

---

## Step 4 — Present the plan

Before moving anything, show a table:

```
파일 정리 계획
──────────────────────────────────────────────────────
  patient_data.csv       →  input/
  smith2023.pdf          →  input/
  fig1_boxplot.py        →  stage1/figures/
  analysis_code.py       →  stage1/analysis/
  results_output.txt     →  stage1/analysis/
  references.bib         →  stage2/literature/
  reviewer_a.md          →  stage3/reviewer_a.md
──────────────────────────────────────────────────────
총 7개 파일

이대로 이동할까요?  [OK] / [수정: ...]
```

Wait for `[OK]` before proceeding.

---

## Step 5 — Execute

For each file in the approved plan:
1. Check if destination file already exists
   - If yes: tell the user and ask whether to overwrite or skip
2. Move the file using `mv` (Bash tool):
   ```bash
   mv "sessions/<id>/archive/<filename>" "sessions/<id>/<destination>"
   ```
3. Track successes and any failures

---

## Step 6 — Report

After all moves are complete, print a summary:

```
✓ 정리 완료

이동됨 (7):
  ✓ patient_data.csv       →  input/
  ✓ smith2023.pdf          →  input/
  ✓ fig1_boxplot.py        →  stage1/figures/
  ...

건너뜀 (0):

archive/ 폴더가 비어 있습니다. 다음 단계로 진행하세요.
```

If any files remain in archive/ (skipped or failed), list them.

---

## Rules

- **Never delete** files from archive/ — always move (not copy-then-delete)
- **Never overwrite** without asking
- If a destination directory doesn't exist, create it before moving
- Do not move `README.md` from archive/
- After organizing, run `autoresearch status` and show the updated workspace
