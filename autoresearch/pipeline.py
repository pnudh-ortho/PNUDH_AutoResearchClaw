"""
Pipeline state machine for AutoResearch.

9-Stage pipeline:
  Stage 1  INPUT 분류      — classify inputs, determine entry point
  Stage 2  BACKGROUND      — systematic literature review and synthesis
  Stage 3  DATA ANALYSIS   — statistical analysis with literature context
  Stage 4  VISUALIZATION   — publication-quality figures
  Stage 5  PAPER OUTLINE   — key message, narrative arc, section blueprints
  Stage 6  PAPER DRAFT     — section writing (Methods→Results→…→Abstract)
  Stage 7  PEER REVIEW     — parallel review by 3 independent reviewers
  Stage 8  PAPER REVISION  — targeted revision + reviewer response letter
  Stage 9  PROOFREADING    — final scientific proofreading

15 checkpoints total.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession

# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint definitions
# ──────────────────────────────────────────────────────────────────────────────

CHECKPOINT_MAP: dict[str, dict] = {
    # ── Stage 1: Input Classification ─────────────────────────────────────
    "1": {
        "stage": 1,
        "phase": "intake",
        "after": "input classified, entry point confirmed",
        "gate_question": "Approve file classification & entry point?",
        "skill": "intake",
        "description": "Researcher approves classified input files and pipeline entry point.",
    },
    # ── Stage 2: Background Knowledge ─────────────────────────────────────
    "2": {
        "stage": 2,
        "phase": "literature",
        "after": "background knowledge synthesis confirmed",
        "gate_question": "Confirm literature scope & key papers?",
        "skill": "literature",
        "description": "Literature synthesis confirmed; knowledge base grounds Stage 3 analysis.",
    },
    # ── Stage 3: Data Analysis ─────────────────────────────────────────────
    "3A": {
        "stage": 3,
        "phase": "data_analysis",
        "after": "statistical analysis plan approved",
        "gate_question": "Approve statistical approach?",
        "skill": "data-analysis",
        "description": "Researcher approves statistical plan before any code runs.",
    },
    "3B": {
        "stage": 3,
        "phase": "data_analysis",
        "after": "analysis results & interpretation confirmed",
        "gate_question": "Approve results & interpretation?",
        "skill": "data-analysis",
        "description": "Researcher confirms results, interpretation, and Story-Writer summary.",
    },
    # ── Stage 4: Visualization ─────────────────────────────────────────────
    "4": {
        "stage": 4,
        "phase": "visualization",
        "after": "figures confirmed",
        "gate_question": "Approve figure types & layout?",
        "skill": "visualization",
        "description": "Researcher selects figure types; code generation starts after.",
    },
    # ── Stage 5: Paper Outline ─────────────────────────────────────────────
    "5": {
        "stage": 5,
        "phase": "outline",
        "after": "paper outline approved",
        "gate_question": "Approve key message & paper outline?",
        "skill": "story-writer",
        "description": "Researcher approves narrative blueprint; section writing begins.",
    },
    # ── Stage 6: Paper Draft ───────────────────────────────────────────────
    "6-1": {
        "stage": 6,
        "phase": "writing",
        "section": "methods",
        "after": "Methods section approved",
        "gate_question": "Proceed to Results?",
        "skill": "section-writer",
        "description": "Methods section approved.",
    },
    "6-2": {
        "stage": 6,
        "phase": "writing",
        "section": "results",
        "after": "Results section approved",
        "gate_question": "Proceed to Discussion?",
        "skill": "section-writer",
        "description": "Results section approved.",
    },
    "6-3": {
        "stage": 6,
        "phase": "writing",
        "section": "discussion",
        "after": "Discussion section approved",
        "gate_question": "Proceed to Conclusion?",
        "skill": "section-writer",
        "description": "Discussion section approved.",
    },
    "6-4": {
        "stage": 6,
        "phase": "writing",
        "section": "conclusion",
        "after": "Conclusion section approved",
        "gate_question": "Proceed to Introduction?",
        "skill": "section-writer",
        "description": "Conclusion section approved.",
    },
    "6-5": {
        "stage": 6,
        "phase": "writing",
        "section": "introduction",
        "after": "Introduction section approved",
        "gate_question": "Proceed to Abstract?",
        "skill": "section-writer",
        "description": "Introduction section approved.",
    },
    "6-6": {
        "stage": 6,
        "phase": "writing",
        "section": "abstract",
        "after": "Abstract approved — full draft complete",
        "gate_question": "All 6 sections complete?",
        "skill": "section-writer",
        "description": "Abstract (final section) approved — manuscript complete.",
    },
    # ── Stage 7: Peer Review ──────────────────────────────────────────────
    "7": {
        "stage": 7,
        "phase": "review",
        "after": "peer review synthesis + revision scope decided",
        "gate_question": "Revision scope decided?",
        "skill": "reviewer-a / reviewer-b / reviewer-c",
        "description": "Researcher reads synthesis, decides which items to address.",
    },
    # ── Stage 8: Paper Revision ───────────────────────────────────────────
    "8": {
        "stage": 8,
        "phase": "revision",
        "after": "revision complete, response letter drafted",
        "gate_question": "Approve revised manuscript & response letter?",
        "skill": "revision",
        "description": "Researcher approves revised manuscript and reviewer response letter.",
    },
    # ── Stage 9: Proofreading ──────────────────────────────────────────────
    "9": {
        "stage": 9,
        "phase": "proofread",
        "after": "proofreading complete",
        "gate_question": "Approve final output for submission?",
        "skill": "proofreader",
        "description": "Final manuscript approved for submission.",
    },
}

# Ordered sequence of all 15 checkpoints
CHECKPOINT_SEQUENCE: list[str] = [
    "1",
    "2",
    "3A", "3B",
    "4",
    "5",
    "6-1", "6-2", "6-3", "6-4", "6-5", "6-6",
    "7",
    "8",
    "9",
]

# Which prior checkpoints must be cleared before this one can be reached
STAGE_DEPS: dict[str, list[str]] = {
    "1":   [],
    "2":   ["1"],
    "3A":  ["2"],              # analysis after background knowledge
    "3B":  ["3A"],
    "4":   ["3B"],             # visualization after analysis confirmed
    "5":   ["2", "3B", "4"],   # outline needs literature + analysis + figures
    "6-1": ["5"],
    "6-2": ["6-1"],
    "6-3": ["6-2"],
    "6-4": ["6-3"],
    "6-5": ["6-4"],
    "6-6": ["6-5"],
    "7":   ["6-6"],
    "8":   ["7"],
    "9":   ["8"],
}

# Section writing order (canonical)
SECTION_ORDER = ["methods", "results", "discussion", "conclusion", "introduction", "abstract"]

# Mapping: section name → checkpoint ID
SECTION_CHECKPOINT: dict[str, str] = {
    "methods":      "6-1",
    "results":      "6-2",
    "discussion":   "6-3",
    "conclusion":   "6-4",
    "introduction": "6-5",
    "abstract":     "6-6",
}


# ──────────────────────────────────────────────────────────────────────────────
# Pipeline controller
# ──────────────────────────────────────────────────────────────────────────────

class ARPipeline:
    """
    Stateless helper that answers dependency and status questions
    given an ARSession's cleared checkpoint list.
    """

    # ── dependency checks ──────────────────────────────────────────────────

    @staticmethod
    def can_proceed_to(cp_id: str, session: "ARSession") -> tuple[bool, list[str]]:
        """
        Return (ok, missing_deps).
        ok=True means all prerequisite checkpoints are cleared.
        """
        missing = [dep for dep in STAGE_DEPS.get(cp_id, []) if not session.is_cleared(dep)]
        return len(missing) == 0, missing

    @staticmethod
    def next_checkpoint(session: "ARSession") -> str | None:
        """Return the first uncleared checkpoint in sequence, or None if all done."""
        for cp in CHECKPOINT_SEQUENCE:
            if not session.is_cleared(cp):
                return cp
        return None

    @staticmethod
    def current_skill(session: "ARSession") -> str | None:
        cp = ARPipeline.next_checkpoint(session)
        if cp is None:
            return None
        return CHECKPOINT_MAP[cp]["skill"]

    # ── status display ────────────────────────────────────────────────────

    @staticmethod
    def status_lines(session: "ARSession") -> list[str]:
        """Return a human-readable list of checkpoint statuses."""
        lines: list[str] = []
        current_stage = -1
        for cp in CHECKPOINT_SEQUENCE:
            info = CHECKPOINT_MAP[cp]
            stage = info["stage"]

            # Stage header
            if stage != current_stage:
                current_stage = stage
                lines.append(f"\n  {ARPipeline.stage_banner(stage)}")

            cleared = session.is_cleared(cp)
            icon = "✓" if cleared else "○"
            label = f"    CP {cp:<4}  {icon}  {info['after']}"
            if not cleared:
                ok, missing = ARPipeline.can_proceed_to(cp, session)
                if not ok:
                    label += f"  [blocked: needs {', '.join(missing)}]"
            lines.append(label)
        return lines

    @staticmethod
    def stage_banner(stage_num: int) -> str:
        banners = {
            1: "STAGE 1 — Input Classification",
            2: "STAGE 2 — Background Knowledge",
            3: "STAGE 3 — Data Analysis",
            4: "STAGE 4 — Visualization",
            5: "STAGE 5 — Paper Outline",
            6: "STAGE 6 — Paper Draft",
            7: "STAGE 7 — Peer Review",
            8: "STAGE 8 — Paper Revision",
            9: "STAGE 9 — Proofreading",
        }
        return banners.get(stage_num, f"STAGE {stage_num}")

    @staticmethod
    def progress_summary(session: "ARSession") -> dict:
        total = len(CHECKPOINT_SEQUENCE)
        cleared = sum(1 for cp in CHECKPOINT_SEQUENCE if session.is_cleared(cp))
        next_cp = ARPipeline.next_checkpoint(session)
        current_stage = CHECKPOINT_MAP[next_cp]["stage"] if next_cp else 9
        return {
            "total": total,
            "cleared": cleared,
            "pct": round(cleared / total * 100),
            "next_checkpoint": next_cp,
            "current_stage": current_stage,
            "current_skill": ARPipeline.current_skill(session),
            "done": next_cp is None,
        }
