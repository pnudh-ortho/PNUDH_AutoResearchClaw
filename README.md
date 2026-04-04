# AutoResearch

**AI-assisted manuscript writing pipeline for solo biomedical researchers.**

Provide your data and references. AutoResearch guides you through analysis, visualization, literature synthesis, section writing, peer review, and final revision — one checkpoint at a time.

---

## What This Is

AutoResearch is a **human-in-the-loop** manuscript writing assistant.  
It does not run autonomously. Every major decision requires your confirmation before the pipeline advances.

**You provide:**
- Raw data (CSV, Excel) or pre-computed analysis results
- Reference papers (PDFs or citations)
- Research topic and target journal (optional)

**AutoResearch produces:**
- Complete manuscript draft (6 sections)
- Analysis code (Python / R)
- Publication-quality figure code
- Figure captions
- Revision change log
- Proofreading report

---

## Pipeline

```
[INPUT]  Topic · Raw data · Reference papers

Stage 1  Data Analysis ─────────────────────────────────────── [CP 1A] [CP 1B]
         └─ Visualization ────────────────────────────────────────────── [CP 1C]

Stage 2  Literature ──────────────────────────────────────────────────── [CP 2A]
         └─ Story Writer ──────────────────────────────────────────────── [CP 2B]
            └─ Section Writer ×6 ─────────────────── [CP 2C-1 … CP 2C-6]
               Methods → Results → Discussion → Conclusion → Introduction → Abstract

Stage 3  Reviewer A ║ Reviewer B ║ Reviewer C  (parallel, independent)
         └─ Review Synthesis (auto) ─────────────────────────────────── [CP 3]

Stage 4  Revision ────────────────────────────────────────────────────── [CP 4]
         └─ Proofreader

[OUTPUT] Manuscript · Analysis code · Figure code · Figure captions
```

**13 checkpoints total.** At every checkpoint, the pipeline stops and waits for:
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

### 2. Configure

Edit `config.autoresearch.yaml`:

```yaml
research:
  topic: >
    Your research topic. Include background, context, and data characteristics
    so Stage 2 (Literature, Story Writer) works accurately.
  journal_target: "PLOS ONE"   # optional

input:
  data_files:
    - "input/patient_data.csv"
  reference_papers:
    - "input/refs/smith2023.pdf"
```

### 3. Create a session

```bash
autoresearch new --config config.autoresearch.yaml
# or
autoresearch new --topic "Effect of X on Y in Z population"
```

Place your data files in `sessions/<session-id>/input/`.

### 4. Run the pipeline (in Claude Code)

Open Claude Code in this directory and ask:

```
Stage 1 데이터 분석을 시작해 주세요.
```

Claude loads the `data-analysis` skill and guides you through CP 1A → CP 1B.  
After each checkpoint, record the approval:

```bash
autoresearch approve 1A --note "Approved Mann-Whitney approach"
autoresearch approve 1B
```

Continue through all stages. Check progress at any time:

```bash
autoresearch status
```

### 5. Export

```bash
autoresearch export
```

Produces `sessions/<id>/final_output.md` with the full manuscript bundle.

---

## Skills

Each stage has a dedicated Claude Code skill. Load them by asking Claude:

| Stage | Skill | Trigger phrase |
|---|---|---|
| 1-A | `data-analysis` | "데이터 분석 시작", "analyze my data" |
| 1-B | `visualization` | "figure 만들어줘", "visualize results" |
| 2-A | `literature` | "문헌 검색", "literature search" |
| 2-B | `story-writer` | "narrative 설계", "story writer" |
| 2-C | `section-writer` | "Methods 작성", "write Results" |
| 3 | `reviewer-a/b/c` | "peer review", "리뷰해줘" |
| 4-A | `revision` | "수정 시작", "revise manuscript" |
| 4-B | `proofreader` | "교정", "proofread" |
| — | `organize` | "archive 정리해줘", "파일 정리" |

---

## Automated Commands

```bash
# After saving all 3 reviewer outputs to sessions/<id>/stage3/
autoresearch run synthesis

# After revision is complete
autoresearch run proofread

# Search PubMed (Stage 2-A support)
autoresearch run pubmed --query "your search terms" --max-results 30
```

---

## Session Management

```bash
autoresearch sessions              # list all sessions
autoresearch status [SESSION_ID]   # show checkpoint progress
autoresearch approve <CP> [--note "..."]
autoresearch revoke <CP>           # roll back to before a checkpoint
autoresearch export [SESSION_ID]
```

---

## Workspace Layout

```
sessions/<session-id>/
├── session.json          — pipeline state (checkpoints cleared, summaries)
├── archive/              — drop files here; ask Claude "archive 정리해줘"
├── input/                — your data files and reference PDFs
├── stage1/
│   ├── analysis/         — analysis_code.py, results.txt, interpretation.md
│   └── figures/          — figure scripts, rendered PNGs/PDFs, captions.md
├── stage2/
│   ├── literature/       — search_log.md, included_papers.bib, synthesis.md
│   ├── story/            — story_outline.md
│   └── manuscript/       — one .md file per section
├── stage3/
│   ├── reviewer_a.md
│   ├── reviewer_b.md
│   ├── reviewer_c.md
│   └── synthesis.md
├── stage4/
│   ├── revised_manuscript.md
│   ├── change_log.md
│   └── proofread_report.md
└── final_output.md       — assembled export bundle
```

### Archive Organizer

Drop any files into `archive/` without worrying about naming or placement.  
Then ask Claude:

```
archive 정리해줘
```

Claude inspects each file's extension and content, proposes a move plan, waits for your confirmation, then executes. Ambiguous files are collected and asked about in one batch before anything is moved.

---

## Package Structure

```
autoresearch/
├── session.py           — ARSession: state, checkpoint tracking, persistence
├── pipeline.py          — CHECKPOINT_MAP, stage dependencies, progress helpers
├── workspace.py         — file I/O for all session artifacts
├── cli.py               — CLI entry point
└── stages/
    ├── data_analysis.py — Stage 1-A: code runner, CP 1A/1B formatting
    ├── visualization.py — Stage 1-B: figure runner, CP 1C formatting
    ├── literature.py    — Stage 2-A: PubMed search, synthesis, CP 2A
    ├── writing.py       — Stage 2-B/C: story outline, section writer
    ├── review.py        — Stage 3: review parser, auto-synthesis, CP 3
    ├── revision.py      — Stage 4-A: change log, revision executor
    └── proofreader.py   — Stage 4-B: 5-category checks, CP 4
```

---

## Requirements

- Python 3.11+
- Claude Code (CLI)
- Optional: R + Rscript (for R-based analysis)
- Optional: `scholarly` (`pip install scholarly`) for Google Scholar search

```bash
pip install -e ".[autoresearch]"          # core + CLI
pip install -e ".[autoresearch,analysis]" # + pandas, scipy, statsmodels
```

---

## Design Principles

1. **Researcher in control** — no step proceeds without explicit approval
2. **Data-grounded** — analyses proposed from your actual data, not defaults
3. **No hypothesis fabrication** — topic is given; AutoResearch does not generate or infer hypotheses
4. **Reproducible** — all analysis and figure code is saved and exported
5. **Transparent revision** — every change is logged in `change_log.md`
