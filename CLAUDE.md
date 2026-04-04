# AutoResearch

AI-assisted research writing pipeline for a solo biomedical researcher.
Takes given data and references → produces a complete manuscript draft.

## What This Is Not
- Not AutoResearchClaw: no experiment generation, no code for science, no auto-search of GEO/TCGA
- Not fully autonomous: every major decision requires researcher confirmation

## Pipeline

```
[INPUT]  Topic · Hypothesis · Raw data / Analysis results · Reference papers (user-provided)

STAGE 1  Data Analysis ──────────────────────────────────────────────────── [CP 1A] [CP 1B]
         └─ Visualization (after all analysis confirmed) ──────────────────────────── [CP 1C]

STAGE 2  Literature ─────────────────────────────────────────────────────────────── [CP 2A]
         └─ Story Writer (references Stage 1 output) ────────────────────────────── [CP 2B]
            └─ Section Writer ×6 ──────────────────────────────── [CP 2C-1 … CP 2C-6]
               Order: Methods → Results → Discussion → Conclusion → Introduction → Abstract

STAGE 3  Review: Reviewer A ║ Reviewer B ║ Reviewer C  (parallel, independent)
         └─ Review Synthesis (auto) ────────────────────────────────────────────── [CP 3]

STAGE 4  Revision ──────────────────────────────────────────────────────────────── [CP 4]
         └─ Proofreader

[OUTPUT] Manuscript draft · Analysis code · Figure code · Figure captions
```

## Checkpoint Protocol

At every checkpoint the agent MUST:
1. Present output (or summary)
2. Explain decisions made
3. State next step with options
4. **STOP and wait** for: `[OK]` / `[REVISE: ...]` / `[REDIRECT: ...]`

Never auto-proceed past a checkpoint.

## Stage Dependencies

- Stage 2 cannot start until Stage 1 checkpoints (1A, 1B, 1C) are all cleared
- Story Writer reads confirmed figures + statistical interpretation from Stage 1
- Section Writer (Results) directly references confirmed figures and statistics
- Section Writer (Discussion) builds on Stage 1 interpretation
- Abstract is always written last

## Skills

```
.claude/skills/
├── data-analysis/      Stage 1-A: explore → propose → execute → interpret
├── visualization/      Stage 1-B: propose figure types → generate code → captions
├── literature/         Stage 2-A: search + synthesize knowledge base
├── story-writer/       Stage 2-B: key message → narrative arc → section outline
├── section-writer/     Stage 2-C: draft one section at a time
├── reviewer-a/         Stage 3:   methodology & statistical rigor
├── reviewer-b/         Stage 3:   clinical relevance & translation
├── reviewer-c/         Stage 3:   writing quality & logical flow
├── revision/           Stage 4-A: targeted revision per checklist
└── proofreader/        Stage 4-B: final consistency check
```

## Working Conventions

1. Read this file at the start of every session
2. Check `docs/pipeline_design.md` before making structural decisions
3. Load the relevant SKILL.md before starting any stage
4. One phase at a time — do not begin Stage 2 until Stage 1 is confirmed complete
5. Record design decisions in `docs/decisions.md` immediately

## Project Status

- [x] Pipeline structure (4 stages, 11 checkpoints)
- [x] Stage dependencies defined
- [x] Section writing order confirmed
- [x] Agent skills written (10 SKILL.md files)
- [x] Skills installed in `.claude/skills/` (all 10 active)
- [x] Stage 1 implementation (`autoresearch/stages/data_analysis.py`, `visualization.py`)
- [x] Stage 2 implementation (`autoresearch/stages/literature.py`, `writing.py`)
- [x] Stage 3 implementation (`autoresearch/stages/review.py`)
- [x] Stage 4 implementation (`autoresearch/stages/revision.py`, `proofreader.py`)

## AutoResearch Package

```
autoresearch/
├── __init__.py          — ARSession, ARPipeline, WorkSpace exports
├── session.py           — session state, checkpoint tracking, persistence
├── pipeline.py          — checkpoint map, stage deps, progress helpers
├── workspace.py         — file I/O for all session artifacts
├── cli.py               — CLI: new / status / approve / run / export
└── stages/
    ├── data_analysis.py — Stage 1-A: code runner, CP 1A/1B formatting
    ├── visualization.py — Stage 1-B: figure runner, CP 1C formatting
    ├── literature.py    — Stage 2-A: PubMed search, synthesis, CP 2A
    ├── writing.py       — Stage 2-B/C: story outline, section writer
    ├── review.py        — Stage 3: review parser, auto-synthesis, CP 3
    ├── revision.py      — Stage 4-A: change log, revision executor
    └── proofreader.py   — Stage 4-B: 5-category checks, CP 4
```

## CLI Quick Start

```bash
pip install -e ".[autoresearch]"

# Start a new session
autoresearch new --topic "..."

# Check status
autoresearch status

# Approve a checkpoint after Claude's output
autoresearch approve 1A --note "Approved Mann-Whitney approach"

# Auto-run review synthesis (after all 3 reviews saved to stage3/)
autoresearch run synthesis

# Auto-run proofreader
autoresearch run proofread

# Export final manuscript
autoresearch export
```
