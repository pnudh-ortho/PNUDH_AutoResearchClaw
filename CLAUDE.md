# AutoResearch

AI-assisted research writing pipeline for a solo biomedical researcher.
Takes given data and references → produces a complete manuscript draft.

## What This Is Not
- Not AutoResearchClaw: no experiment generation, no code for science, no auto-search of GEO/TCGA
- Not fully autonomous: every major decision requires researcher confirmation

## Pipeline

```
[INPUT]  Any files in input/[topic]/  →  intake skill auto-classifies everything

STAGE 1  Input Classification ───────────────────────────────────────────────────── [CP 1]
         (classify files, detect entry point, create session, move files)

STAGE 2  Background Knowledge ───────────────────────────────────────────────────── [CP 2]
         (systematic literature search → thematic synthesis → evidence gap)

STAGE 3  Data Analysis ──────────────────────────────────────── [CP 3A] ── [CP 3B]
         (literature-informed statistical plan → execute code → interpret results)

STAGE 4  Visualization ──────────────────────────────────────────────────────────── [CP 4]
         (figure type selection → generate code → render → captions)

STAGE 5  Paper Outline ──────────────────────────────────────────────────────────── [CP 5]
         (key message → narrative arc → section-by-section blueprints)
         Uses: Stage 2 synthesis + Stage 3 analysis + Stage 4 figures

STAGE 6  Paper Draft ──────────────────────────────── [CP 6-1 … CP 6-6]
         Methods → Results → Discussion → Conclusion → Introduction → Abstract

STAGE 7  Peer Review ────────────────────────────────────────────────────────────── [CP 7]
         Reviewer A (methods) ║ Reviewer B (clinical) ║ Reviewer C (writing)
         └─ Review Synthesis (auto)

STAGE 8  Paper Revision ─────────────────────────────────────────────────────────── [CP 8]
         (address reviewer checklist → change log → response letter)

STAGE 9  Proofreading ───────────────────────────────────────────────────────────── [CP 9]
         (8 systematic checks → flag only, researcher decides every fix)

[OUTPUT] Manuscript · Analysis code · Figure code · Figure captions · Response letter
```

## Stage Dependencies

- Stage 3 (Data Analysis) cannot start until Stage 2 (Literature) is complete
  → Literature context informs statistical approach and interpretation
- Stage 5 (Paper Outline) requires Stages 2 + 3 + 4 all complete
  → Outline is informed by background, data, AND figures simultaneously
- Stages proceed sequentially thereafter: 6 → 7 → 8 → 9

## Checkpoint Protocol

At every checkpoint the agent MUST:
1. Present output (or summary)
2. Explain decisions made
3. State next step with options
4. **STOP and wait** for: `[OK]` / `[REVISE: ...]` / `[REDIRECT: ...]`

Never auto-proceed past a checkpoint.

## Skills

```
.claude/skills/
├── intake/             Stage 1:   scan input/, classify files, detect entry point  [CP 1]
├── organize/           Any:       sort files from archive/ into correct stage dirs
├── literature/         Stage 2:   systematic search + knowledge synthesis          [CP 2]
├── data-analysis/      Stage 3:   literature-informed analysis → interpret          [CP 3A/3B]
├── visualization/      Stage 4:   figure type reasoning → code → captions          [CP 4]
├── story-writer/       Stage 5:   key message → narrative arc → section outlines   [CP 5]
├── section-writer/     Stage 6:   draft one section at a time                      [CP 6-1…6-6]
├── reviewer-a/         Stage 7:   methodology & statistical rigor
├── reviewer-b/         Stage 7:   clinical relevance & translation
├── reviewer-c/         Stage 7:   writing quality & logical flow                   [CP 7]
├── revision/           Stage 8:   targeted revision + response letter              [CP 8]
└── proofreader/        Stage 9:   8-category final proofread                       [CP 9]
```

## Working Conventions

1. Read this file at the start of every session
2. Run `autoresearch status` at the start of every session to learn the current pipeline state
3. Check `docs/pipeline_design.md` before making structural decisions
4. Load the relevant SKILL.md before starting any stage
5. One phase at a time — do not begin Stage 2 until Stage 1 is confirmed complete
6. Record design decisions in `docs/decisions.md` immediately

## Session Continuity

At the start of every conversation:
1. Run `autoresearch status` to check pipeline progress
2. If a session exists and has cleared checkpoints: state the current stage and ask "Shall we continue from [stage]?"
3. If no session exists and `input/` has files: offer to run intake — "I see files in input/[topic]/. Shall I classify them and start the pipeline?"
4. If no session and no input files: greet the researcher and explain how to start

Do not ask the researcher to re-explain context that is already recorded in the session.

## Natural Language Intent Routing

Map researcher language to pipeline actions. Do not require exact trigger phrases.

| Researcher says (examples) | Intent | Action |
|---|---|---|
| "시작해줘", "start", "let's go", "파일 있어", "내 데이터 봐줘" | Begin pipeline | Load intake skill |
| "정리해줘", "archive 정리", "sort files", "파일 분류" | Organize files | Load organize skill |
| "데이터 분석", "analyze the data", "run the stats" | Stage 1-A | Load data-analysis skill |
| "figure 만들어", "그래프", "visualization", "plot" | Stage 1-C | Load visualization skill |
| "논문 찾아줘", "literature", "references", "관련 논문" | Stage 2-A | Load literature skill |
| "스토리", "어떻게 쓸지", "outline", "narrative arc" | Stage 2-B | Load story-writer skill |
| "methods 써줘", "results 작성", "write the [section]" | Stage 2-C | Load section-writer skill |
| "리뷰해줘", "peer review", "검토", "비평" | Stage 3 | Load reviewer-a/b/c skills |
| "수정해줘", "revise", "revision", "address comments" | Stage 4-A | Load revision skill |
| "교정", "proofread", "final check", "마지막 확인" | Stage 4-B | Load proofreader skill |

When intent is ambiguous, name the most likely skill and confirm: "It sounds like you want to [X]. Shall I load the [skill] skill?"

## Project Status

- [x] Pipeline structure (4 stages, 13 checkpoints)
- [x] Stage dependencies defined
- [x] Section writing order confirmed
- [x] Agent skills written (12 SKILL.md files, English, v2.0)
- [x] Skills installed in `.claude/skills/` (all 12 active)
- [x] Stage 0: intake skill + `autoresearch intake` CLI command
- [x] Stage 1 implementation (`autoresearch/stages/data_analysis.py`, `visualization.py`)
- [x] Stage 2 implementation (`autoresearch/stages/literature.py`, `writing.py`)
- [x] Stage 3 implementation (`autoresearch/stages/review.py`)
- [x] Stage 4 implementation (`autoresearch/stages/revision.py`, `proofreader.py`)
- [x] Natural language intent routing (see above)
- [x] Session continuity protocol (auto-check status at session start)

## AutoResearch Package

```
autoresearch/
├── __init__.py          — ARSession, ARPipeline, WorkSpace exports
├── session.py           — session state, 15-checkpoint tracking, persistence
├── pipeline.py          — 9-stage checkpoint map, deps, progress helpers
├── workspace.py         — stage1…stage9 directory I/O
├── cli.py               — CLI: intake / new / status / approve / run / export
└── stages/
    ├── data_analysis.py — Stage 3: code runner, CP 3A/3B formatting
    ├── visualization.py — Stage 4: figure runner, CP 4 formatting
    ├── literature.py    — Stage 2: PubMed search, synthesis, CP 2
    ├── writing.py       — Stage 5/6: outline, section writer, CP 5 / CP 6-x
    ├── review.py        — Stage 7: review parser, auto-synthesis, CP 7
    ├── revision.py      — Stage 8: change log, revision executor, CP 8
    └── proofreader.py   — Stage 9: 8-category checks, CP 9
```

## CLI Quick Start

```bash
pip install -e ".[autoresearch]"

# --- Intake (Stage 0) ---
# Place all files in input/[topic]/ then scan + classify them
autoresearch intake [topic]        # prints report; no files moved yet

# Start a new session (done by intake skill after CP 0 approval)
autoresearch new --topic "..."
autoresearch new --config config.autoresearch.yaml

# --- Pipeline control ---
# Check status (run at start of every conversation)
autoresearch status

# Approve a checkpoint after Claude's output
autoresearch approve 1A --note "Approved Mann-Whitney approach"

# Roll back a checkpoint
autoresearch revoke 1B

# --- Automated stage components ---
# Auto-run review synthesis (after all 3 reviews saved to stage3/)
autoresearch run synthesis

# Auto-run proofreader
autoresearch run proofread

# PubMed search
autoresearch run pubmed --query "SGLT-2 inhibitors heart failure" --max-results 30

# --- Output ---
# List all sessions
autoresearch sessions

# Export final manuscript
autoresearch export
```
