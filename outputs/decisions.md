# Design Decisions Log

Update this file whenever a design choice is made in conversation or implementation.

---

## D-001: No experiment generation, no science code
Input is given data and results. The system does not design or run experiments.
Claude Code sandbox is used only for data analysis and figure generation.

## D-002: Solo researcher as primary user
No role separation. One person makes all checkpoint decisions.

## D-003: Biomedical research domain
Reviewer personas and section structure calibrated for Bio/Med/Clinical papers.
Standard sections: Abstract, Introduction, Methods, Results, Discussion, Conclusion.

## D-004: Frequent checkpoints — every major decision
13 total checkpoints. The "wasted token" problem is solved by catching wrong
directions early, especially at narrative arc (CP 2B) and before execution (CP 1A).

## D-005: Abstract written last
Abstract is drafted after all other sections are confirmed. Ensures accuracy.

## D-006: Review synthesis before user sees raw reviews
Three reviewers → auto-synthesis → user sees organized output at CP 3.

## D-007: Skill file convention from AutoResearchClaw
`.claude/skills/{agent-name}/SKILL.md` structure.
Format: YAML frontmatter + numbered-list workflow. Short and actionable.

## D-008: Stage 0 renamed to Stage 1
Data & Visualization is now Stage 1. Writing is Stage 2.
Stages: 1 (Data+Viz) → 2 (Writing) → 3 (Review) → 4 (Revision).

## D-009: No GEO/TCGA auto-search
Comparison data must come from user-provided papers. Literature agent uses
PubMed and Google Scholar only.

## D-010: Visualization after all analysis complete
Phase 1-B starts only after CP 1B is cleared. 1-A and 1-B are strictly sequential.

## D-011: Visualization code — SciencePlots base, extend as needed
Start with SciencePlots + matplotlib/seaborn (Python) or ggplot2 (R).
Extend to specialized libraries (lifelines, PyComplexHeatmap, etc.) only when required.

## D-012: Figure type — AI proposes, user decides
Visualization agent reasons from data type + comparison structure + scientific question.
No hardcoded list. User makes final call at CP 1C.

## D-013: Data Analysis agent — design + execution + interpretation combined
Single agent handles explore → propose → execute → interpret.
Two checkpoints: CP 1A (before execution), CP 1B (after interpretation).

## D-014: Visualization — reasoning-based, not list-based
Agent reasons from data context. Excel chart list and biomedical special types
are reference knowledge, not a selection menu.

## D-015: Literature search is mandatory, not optional
Regardless of how many references the user provides, systematic search is always run.
Range: no default date cutoff — seminal papers from any era are included.

## D-016: Section writing order
Methods → Results → Discussion → Conclusion → Introduction → Abstract.
Introduction is second-to-last (written after content is confirmed).
Abstract is always last.

## D-017: Story Writer confirmed before Section Writer starts
Narrative arc and section outline must be approved at CP 2B before any prose is written.
Story Writer does not write prose — Section Writer does.

## D-018: Stage 2 depends on Stage 1 output
Story Writer and Section Writer reference confirmed figures and statistical
interpretation from Stage 1. Stage 2 cannot meaningfully begin without Stage 1 output.
