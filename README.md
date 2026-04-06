# AutoResearch

**AI-assisted manuscript writing pipeline for solo biomedical researchers.**

Drop your files in one folder. AutoResearch classifies them, determines where to start, and guides you through every step — from background knowledge to final proofreading — one checkpoint at a time.

---

## What This Is

AutoResearch is a **human-in-the-loop** manuscript writing assistant.  
It does not run autonomously. Every major decision requires your confirmation before the pipeline advances.

**You provide:**
- Any files in `input/[topic]/` — data, PDFs, analysis outputs, notes, drafts (anything)
- AutoResearch auto-classifies everything and determines the optimal entry point

**AutoResearch produces:**
- Complete manuscript draft (6 sections)
- Analysis code (Python / R)
- Publication-quality figure code + captions
- Reviewer response letter
- Revision change log + proofreading report

---

## Pipeline

```
[INPUT]  Drop everything into input/[topic]/  →  intake auto-classifies

Stage 1  Input Classification ─────────────────────────────────────── [CP 1]
         classify files · detect entry point · create session

Stage 2  Background Knowledge ─────────────────────────────────────── [CP 2]
         PubMed + Scholar search · thematic synthesis · evidence gap
         ↓ provides context for Stage 3

Stage 3  Data Analysis ─────────────────────────────────── [CP 3A] [CP 3B]
         literature-informed statistical plan · execute code · interpret results

Stage 4  Visualization ─────────────────────────────────────────────── [CP 4]
         figure type selection · generate code · render · captions

Stage 5  Paper Outline ─────────────────────────────────────────────── [CP 5]
         key message · narrative arc · section blueprints
         (uses Stage 2 + 3 + 4 simultaneously)

Stage 6  Paper Draft ───────────────────────────────── [CP 6-1 … CP 6-6]
         Methods → Results → Discussion → Conclusion → Introduction → Abstract

Stage 7  Peer Review ───────────────────────────────────────────────── [CP 7]
         Reviewer A (methods) ║ Reviewer B (clinical) ║ Reviewer C (writing)
         └─ Review Synthesis (auto)

Stage 8  Paper Revision ────────────────────────────────────────────── [CP 8]
         address reviewer checklist · change log · response letter

Stage 9  Proofreading ──────────────────────────────────────────────── [CP 9]
         8 systematic checks · flag only, you decide every fix

[OUTPUT] Manuscript · Analysis code · Figure code · Response letter
```

**15 checkpoints total.** At every checkpoint, the pipeline stops and waits for:
- `[OK]` — proceed to next step
- `[REVISE: ...]` — revise and re-present
- `[REDIRECT: ...]` — change direction entirely

---

## Quick Start

### 1. Install

```bash
git clone <this-repo>
cd PNUDH_AutoResearchClaw
pip install -e ".[autoresearch]"
```

### 2. Drop your files

```
input/
└── my_study/
    ├── patient_data.csv
    ├── smith2023.pdf
    ├── kim2022.pdf
    └── spss_output.txt
```

Any file type is accepted. AutoResearch classifies them automatically.

### 3. Start (in Claude Code)

Open Claude Code in this directory and say:

```
시작해줘
```

or

```
start
```

Claude loads the `intake` skill, classifies your files, detects the optimal entry point, and asks for your confirmation before creating a session.

Alternatively, preview the classification without starting:

```bash
autoresearch intake my_study
```

### 4. Approve checkpoints as you go

After each checkpoint, confirm progress:

```bash
autoresearch approve 3A --note "Approved Mann-Whitney approach"
autoresearch approve 3B
autoresearch status
```

### 5. Export

```bash
autoresearch export
```

Produces `sessions/<id>/final_output.md` with the full manuscript bundle.

---

## Skills

Each stage has a dedicated Claude Code skill. Load them by asking naturally:

| Stage | Skill | Example phrases |
|---|---|---|
| 1 | `intake` | "시작해줘", "내 파일 분류해줘", "start" |
| 2 | `literature` | "문헌 검색", "관련 논문 찾아줘", "literature" |
| 3 | `data-analysis` | "데이터 분석", "run the stats", "analyze" |
| 4 | `visualization` | "figure 만들어", "그래프", "visualize" |
| 5 | `story-writer` | "아웃라인", "narrative arc", "outline" |
| 6 | `section-writer` | "Methods 써줘", "write Results" |
| 7 | `reviewer-a/b/c` | "리뷰해줘", "peer review" |
| 8 | `revision` | "수정해줘", "revise", "address comments" |
| 9 | `proofreader` | "교정", "proofread", "final check" |
| — | `organize` | "archive 정리해줘", "sort files" |

You don't need exact trigger phrases — Claude infers intent from natural language.

---

## Automated Commands

```bash
# Classify files in input/ before starting
autoresearch intake [topic]

# After saving all 3 reviewer outputs to sessions/<id>/stage7/
autoresearch run synthesis

# After revision is complete
autoresearch run proofread

# PubMed search (Stage 2 support)
autoresearch run pubmed --query "SGLT-2 inhibitors heart failure" --max-results 30
```

---

## Session Management

```bash
autoresearch sessions                        # list all sessions
autoresearch status [SESSION_ID]             # show 15-checkpoint progress
autoresearch approve <CP> [--note "..."]     # mark checkpoint approved
autoresearch revoke <CP>                     # roll back to before a checkpoint
autoresearch export [SESSION_ID]             # assemble final output
```

---

## Workspace Layout

```
sessions/<session-id>/
├── session.json     — pipeline state (15 checkpoints, all stage summaries)
├── input/           — original user-provided files (never deleted)
├── archive/         — drop zone: ask "archive 정리해줘" to sort
├── stage1/          — intake manifest (intake_report.md)
├── stage2/          — background knowledge
│   ├── search_log.md
│   ├── included_papers.bib
│   └── synthesis.md
├── stage3/          — data analysis
│   ├── analysis_plan.md
│   ├── analysis_code.py
│   ├── analysis_results.txt
│   └── interpretation.md
├── stage4/          — visualization
│   ├── figure_plan.md
│   ├── fig1_*.py / fig1_*.pdf
│   └── captions.md
├── stage5/          — paper outline
│   ├── key_message.md
│   └── outline.md
├── stage6/          — manuscript draft
│   ├── methods.md / results.md / discussion.md
│   ├── conclusion.md / introduction.md / abstract.md
│   └── full_manuscript.md
├── stage7/          — peer review
│   ├── reviewer_a.md / reviewer_b.md / reviewer_c.md
│   └── synthesis.md
├── stage8/          — revision
│   ├── revision_checklist.md
│   ├── revised_manuscript.md
│   ├── change_log.md
│   └── response_letter.md
├── stage9/          — proofreading
│   └── proofread_report.md
└── final_output.md  — assembled export bundle
```

---

## Package Structure

```
autoresearch/
├── session.py       — ARSession: 15-checkpoint state, persistence
├── pipeline.py      — 9-stage checkpoint map, dependencies, progress
├── workspace.py     — stage1…stage9 directory I/O
├── cli.py           — CLI: intake / new / status / approve / run / export
└── stages/
    ├── data_analysis.py — Stage 3: CP 3A/3B formatting, code runner
    ├── visualization.py — Stage 4: CP 4 formatting, figure runner
    ├── literature.py    — Stage 2: PubMed search, synthesis, CP 2
    ├── writing.py       — Stage 5/6: outline (CP 5), section writer (CP 6-x)
    ├── review.py        — Stage 7: review parser, auto-synthesis, CP 7
    ├── revision.py      — Stage 8: change log, revision executor, CP 8
    └── proofreader.py   — Stage 9: 8-category checks, CP 9
```

---

## Requirements

- Python 3.11+
- Claude Code (CLI)
- Optional: R + Rscript (for R-based analysis and figures)
- Optional: `scholarly` (`pip install scholarly`) for Google Scholar search

```bash
pip install -e ".[autoresearch]"           # core + CLI
pip install -e ".[autoresearch,analysis]"  # + pandas, scipy, statsmodels
```

---

## Design Principles

1. **Researcher in control** — no step proceeds without explicit approval
2. **Literature-grounded analysis** — Stage 2 synthesis informs Stage 3 statistical approach
3. **Any input accepted** — drop any files; intake classifies and routes automatically
4. **Data-grounded** — analyses proposed from your actual data, not defaults
5. **No hypothesis fabrication** — topic is given; AutoResearch does not generate hypotheses
6. **Reproducible** — all analysis and figure code is saved and exported
7. **Transparent revision** — every change is logged with before/after and cascade effects
