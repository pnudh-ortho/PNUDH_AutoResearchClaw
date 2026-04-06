---
name: intake
description: >
  Smart input intake for AutoResearch — Stage 1.
  Scans input/[topic]/ at the project root, classifies every file by type and
  pipeline relevance, determines the optimal pipeline entry point (which checkpoints
  are pre-satisfied by existing materials), creates a session, moves files into the
  session workspace, and hands off to the appropriate stage skill.
  Triggers on: "시작해줘", "start", "내 파일 봐줘", "intake", "분석 시작",
  or whenever input/ contains an unprocessed topic folder.
metadata:
  category: pipeline
  trigger-keywords: "시작,start,begin,intake,파일,files,input,topic,classify,분류,새 연구,new study"
  applicable-stages: "1"
  priority: "0"
  version: "2.0"
  author: autoresearch
---

# Intake — Stage 1

**The researcher drops all files into input/[topic]/ and says "start."
This skill handles everything else: classification, entry point detection,
session creation, file placement, and pipeline handoff.**

---

## Step 1 — Locate the Topic Folder

```bash
ls input/
```

**If no subdirectories exist:**
```
No topic folder found in input/.
Please create a folder: input/[your-study-name]/
Then place all your files there (data, PDFs, notes, previous results — everything).
When ready, say "시작해줘" or "start".
```
Stop.

**If exactly one subdirectory exists**: use it as the topic. Proceed.

**If multiple subdirectories exist**: list them and ask:
```
Multiple study folders found in input/:
  1. obesity_treatment/    (12 files)
  2. cardiac_biomarkers/   ( 4 files)
  3. pilot_rct_2025/       ( 7 files)

Which study would you like to work on?
```
Wait for researcher selection. Proceed with selected folder.

Topic folder path: `input/[topic]/`

---

## Step 2 — Classify All Files

List every file in `input/[topic]/` (including subdirectories, recursively).
For each file, apply the classification rules below.

### Classification Categories

| Category | Description | Pipeline implication |
|---|---|---|
| `raw_data` | Unprocessed tabular data | Stage 3: data analysis needed |
| `analysis_output` | Statistics output from prior analysis | Stage 3 can be skipped or partially skipped |
| `figure_image` | Rendered figure files | Stage 4 may be partially satisfied |
| `figure_code` | Python/R scripts that generate figures | Stage 4 context available |
| `analysis_code` | Python/R scripts for data analysis | Stage 3 code context available |
| `reference_pdf` | Peer-reviewed papers for citation | Stage 2 accelerated |
| `bibliography` | .bib / .ris reference files | Stage 2 ready |
| `manuscript_draft` | Written manuscript sections | Stages already complete |
| `protocol_doc` | Study protocol or design document | CP 3A context |
| `notes` | Researcher notes, hypotheses, context | General context for all stages |

### Classification Rules (apply in order)

**Step 2.1 — Extension-based fast path:**

| Extension | Category | No inspection needed |
|---|---|---|
| `.csv`, `.tsv`, `.sav`, `.sas7bdat`, `.dta` | `raw_data` | ✓ |
| `.bib`, `.ris`, `.nbib` | `bibliography` | ✓ |
| `.png`, `.jpg`, `.jpeg`, `.tiff`, `.svg` | `figure_image` | ✓ |

**Step 2.2 — Extension + content inspection:**

**.xlsx / .xls** — read column headers (first row):
- Headers include `p`, `p-value`, `p_val`, `OR`, `HR`, `CI`, `β`, `coefficient`, `effect_size`, `mean`, `SD`, `median` → `analysis_output`
- Otherwise → `raw_data`

**.pdf** — read first 200 characters or filename:
- Filename contains author names, year, journal abbreviation pattern (e.g., `Smith2023_NEJM.pdf`) → `reference_pdf`
- Text contains: DOI, "Abstract", journal name → `reference_pdf`
- Filename suggests figure (`fig1_`, `Figure_`) → `figure_image`
- Otherwise → `reference_pdf` (most PDFs in a research context are papers; flag as UNCLEAR only if truly ambiguous)

**.py** — read first 20 lines:
- Contains `matplotlib`, `seaborn`, `plt.`, `sns.`, `subplots`, `fig,`, `ax =` → `figure_code`
- Otherwise → `analysis_code`

**.R / .Rmd** — read first 20 lines:
- Contains `ggplot`, `plot(`, `hist(`, `barplot(`, `geom_`, `survplot` → `figure_code`
- Otherwise → `analysis_code`

**.txt / .log / .html** — read first 50 lines:
- Contains `t(`, `F(`, `p =`, `p<`, `χ²`, `U =`, `H =`, `df =`, `95% CI`, `Cohen`, `OR =`, `HR =`, `AUC` → `analysis_output`
- Otherwise → `notes`

**.md / .docx** — scan for section headers:
- Contains `## Methods`, `## Results`, `## Discussion`, `## Conclusion`, `## Introduction`, `## Abstract` (case-insensitive) → `manuscript_draft`; record which sections are present
- Contains `hypothesis`, `study design`, `inclusion criteria`, `exclusion criteria`, `protocol` → `protocol_doc`
- Otherwise → `notes`

**Unrecognized or ambiguous**: mark `UNCLEAR` — ask in Step 3.

---

## Step 3 — Handle Unclear Files

Collect all UNCLEAR files. Ask in one batch before proceeding:

```
Some files could not be auto-classified. Please help:

1. study_notes.txt
   Content preview: "Hypothesis: Treatment A reduces inflammation via..."
   Options: (A) notes   (B) protocol_doc
   
2. results_final_v3.xlsx
   Content preview: [column headers not clearly statistical]
   Options: (A) raw_data   (B) analysis_output
   
Your choice for each? (enter: 1A 2B, or specify custom path)
```

Wait for researcher response. Proceed with confirmed classifications.

---

## Step 4 — Determine Pipeline Entry Point

Apply this decision tree to the classification results:

```
All required manuscript sections present?
  (Methods + Results + Discussion + Conclusion + Introduction = 5 sections)
  → YES: Entry point = Stage 7 (Review)
         Auto-clear: CP 3A, 3B, 4, 2, 5, 6-1 through 6-6

Some manuscript sections present (but not all 5)?
  → YES: Entry point = Stage 6 (continue writing)
         Find first missing section in writing order: Methods → Results → Discussion → Conclusion → Introduction
         Auto-clear: stages completed up to the first missing section

analysis_output AND figure_image both present?
  → YES: Entry point = Stage 2 (Background Knowledge / Literature)
         Auto-clear: CP 3A, 3B, 4
         Note: analysis results and figures already exist; proceed to narrative and writing

analysis_output present (but no figures)?
  → YES: Entry point = Stage 4 (Visualization)
         Auto-clear: CP 3A, 3B
         Note: analysis already done; propose figures based on existing results

reference_pdf only (no raw_data, no analysis_output)?
  → YES: Entry point = Stage 2 (Background Knowledge, reference-only mode)
         Note: no data analysis; this may be a review article or data-free study

raw_data present (standard case)?
  → YES: Entry point = Stage 3 (Data Analysis — normal start)
         Auto-clear: none

Nothing found?
  → Entry point = Stage 3 (empty start)
```

---

## Step 5 — CP 1: Intake Report

Present the intake report and wait for researcher confirmation.

```
## Intake Report — input/[topic]/

### Files Found ([N] total)

  Raw data        ([N]): patient_data.csv, lab_results.xlsx
  Reference PDFs  ([N]): smith2023.pdf, kim2022.pdf, jones2021.pdf
  Analysis output ([N]): spss_output.txt
  Figure images   ([N]): fig1_km_curve.png
  Analysis code   ([N]): analysis_code.R
  Notes/context   ([N]): hypothesis.txt, study_design.md
  Unclear         ([N]): [resolved in Step 3 or still open]

### Recommended Entry Point

→ **Stage 4 (Visualization)** — CP 4

Reason: Analysis output (spss_output.txt) is present, suggesting data analysis
is already complete. No figures yet — Stage 4 will propose figure types based
on the existing results and generate code.

### Checkpoints to Auto-Clear (pending your approval)

  CP 3A (statistical approach approval)  — analysis_output present; assumes analysis was performed externally
  CP 3B (results interpretation)         — requires researcher review of spss_output.txt before clearing

### File Placement Plan

  patient_data.csv            →  sessions/[id]/input/
  lab_results.xlsx            →  sessions/[id]/input/
  smith2023.pdf               →  sessions/[id]/input/
  kim2022.pdf                 →  sessions/[id]/input/
  jones2021.pdf               →  sessions/[id]/input/
  spss_output.txt             →  sessions/[id]/stage3/analysis_results.txt
  fig1_km_curve.png           →  sessions/[id]/stage4/figures/
  analysis_code.R             →  sessions/[id]/stage3/
  hypothesis.txt              →  sessions/[id]/input/
  study_design.md             →  sessions/[id]/input/

---
✓ CHECKPOINT 1 — Intake complete
Entry point: Stage 4 (Visualization)

Options:
  [OK]                         — proceed with this entry point
  [ENTRY: Stage 3]             — restart from full data analysis
  [ENTRY: Stage 2]             — skip analysis, go straight to background knowledge
  [ENTRY: Stage 7]             — all analysis and writing done; just need review
  [ADD FILES]                  — add more files to input/[topic]/ first
```

**STOP. Do not create session or move files until researcher responds.**

---

## Step 6 — Create Session and Move Files

After `[OK]` or `[ENTRY: ...]`:

**6.1 Create session:**
```bash
# If config.autoresearch.yaml exists with research.topic set:
autoresearch new --config config.autoresearch.yaml

# Otherwise, use the topic folder name:
autoresearch new --topic "[topic folder name formatted as sentence]"
```

Get the session ID and workspace path from `autoresearch status`.

**6.2 Move files per the placement plan:**
```bash
# Raw data and references → input/
mv "input/[topic]/patient_data.csv" "sessions/[id]/input/"
mv "input/[topic]/smith2023.pdf"    "sessions/[id]/input/"

# Analysis output → stage3/ with standard filename
mv "input/[topic]/spss_output.txt"  "sessions/[id]/stage3/analysis_results.txt"

# Figures → stage4/figures/
mv "input/[topic]/fig1_km_curve.png" "sessions/[id]/stage4/figures/"

# Code → appropriate stage
mv "input/[topic]/analysis_code.R"  "sessions/[id]/stage3/"

# Notes stay in input/ for context
mv "input/[topic]/hypothesis.txt"   "sessions/[id]/input/"
mv "input/[topic]/study_design.md"  "sessions/[id]/input/"

# Manuscript drafts → stage6/[section].md
mv "input/[topic]/methods_draft.md" "sessions/[id]/stage6/methods.md"
```

**6.3 Keep input/[topic]/ folder intact** (may still contain the original files as backup).

---

## Step 7 — Pre-Clear Approved Checkpoints

For each checkpoint the researcher approved to auto-clear:
```bash
autoresearch approve 3A --note "Intake: analysis output provided by researcher (spss_output.txt)"
```

**Only clear what was explicitly approved at CP 0.** Do not silently clear checkpoints.

---

## Step 8 — Hand Off to Appropriate Skill

State the handoff clearly and load the relevant skill:

| Entry point | Announcement | Skill to load |
|---|---|---|
| Stage 3 | "Starting data analysis. Let's explore the data files." | data-analysis |
| Stage 4 | "Analysis results are present. Let's design the figures." | visualization |
| Stage 2 | "Moving to background knowledge search. [N] reference PDFs will be the starting set." | literature |
| Stage 6 | "Continuing manuscript writing. Next section: [section name]." | section-writer |
| Stage 7 | "Complete draft found. Starting parallel peer review." | reviewer-a/b/c |

---

## Rules

- **Never move files before CP 0 is approved** — always show plan first
- **Never delete original files** from `input/[topic]/` — always move (mv), treat as backup
- **Never silently pre-clear checkpoints** — only clear what researcher explicitly approved at CP 0
- **Never fabricate a topic name** — use the folder name or ask the researcher if unclear
- **notes files are always preserved** in input/ — they provide context for every stage
- **If a config.autoresearch.yaml is present** with a matching topic: use it for session creation
