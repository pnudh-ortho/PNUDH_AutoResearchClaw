"""
Pipeline state machine for AutoResearch.

Defines checkpoint ordering, stage dependencies, and the canonical
13-checkpoint sequence the researcher must navigate.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoresearch.session import ARSession

# ──────────────────────────────────────────────────────────────────────────────
# Checkpoint definitions
# ──────────────────────────────────────────────────────────────────────────────

CHECKPOINT_MAP: dict[str, dict] = {
    "1A": {
        "stage": 1,
        "phase": "data_analysis",
        "after": "data exploration + test proposal",
        "gate_question": "Approve statistical approach?",
        "skill": "data-analysis",
        "description": "Researcher approves the statistical plan before any code runs.",
    },
    "1B": {
        "stage": 1,
        "phase": "data_analysis",
        "after": "analysis execution + interpretation",
        "gate_question": "Approve results & interpretation?",
        "skill": "data-analysis",
        "description": "Researcher confirms statistical results and Story-Writer summary.",
    },
    "1C": {
        "stage": 1,
        "phase": "visualization",
        "after": "figure plan proposal",
        "gate_question": "Approve figure types & layout?",
        "skill": "visualization",
        "description": "Researcher selects figure types; code generation starts after.",
    },
    "2A": {
        "stage": 2,
        "phase": "literature",
        "after": "literature synthesis",
        "gate_question": "Confirm scope & key papers?",
        "skill": "literature",
        "description": "Researcher adds/removes papers; Story Writer uses this synthesis.",
    },
    "2B": {
        "stage": 2,
        "phase": "story",
        "after": "key message + narrative arc",
        "gate_question": "Approve key message & narrative arc?",
        "skill": "story-writer",
        "description": "Researcher approves the narrative blueprint; section writing begins.",
    },
    "2C-1": {
        "stage": 2,
        "phase": "writing",
        "section": "methods",
        "after": "Methods draft",
        "gate_question": "Proceed to Results?",
        "skill": "section-writer",
        "description": "Methods section approved.",
    },
    "2C-2": {
        "stage": 2,
        "phase": "writing",
        "section": "results",
        "after": "Results draft",
        "gate_question": "Proceed to Discussion?",
        "skill": "section-writer",
        "description": "Results section approved.",
    },
    "2C-3": {
        "stage": 2,
        "phase": "writing",
        "section": "discussion",
        "after": "Discussion draft",
        "gate_question": "Proceed to Conclusion?",
        "skill": "section-writer",
        "description": "Discussion section approved.",
    },
    "2C-4": {
        "stage": 2,
        "phase": "writing",
        "section": "conclusion",
        "after": "Conclusion draft",
        "gate_question": "Proceed to Introduction?",
        "skill": "section-writer",
        "description": "Conclusion section approved.",
    },
    "2C-5": {
        "stage": 2,
        "phase": "writing",
        "section": "introduction",
        "after": "Introduction draft",
        "gate_question": "Proceed to Abstract?",
        "skill": "section-writer",
        "description": "Introduction section approved.",
    },
    "2C-6": {
        "stage": 2,
        "phase": "writing",
        "section": "abstract",
        "after": "Abstract draft",
        "gate_question": "All sections approved?",
        "skill": "section-writer",
        "description": "Abstract (last section) approved — manuscript complete.",
    },
    "3": {
        "stage": 3,
        "phase": "review",
        "after": "review synthesis",
        "gate_question": "Revision scope decided?",
        "skill": "reviewer-a / reviewer-b / reviewer-c",
        "description": "Researcher reads synthesis, decides which items to address.",
    },
    "4": {
        "stage": 4,
        "phase": "revision",
        "after": "proofreading complete",
        "gate_question": "Approve final output?",
        "skill": "proofreader",
        "description": "Final manuscript approved for output.",
    },
}

# Ordered sequence of all checkpoints
CHECKPOINT_SEQUENCE: list[str] = [
    "1A", "1B", "1C",
    "2A", "2B",
    "2C-1", "2C-2", "2C-3", "2C-4", "2C-5", "2C-6",
    "3", "4",
]

# Which prior checkpoints must be cleared before this one can be reached
STAGE_DEPS: dict[str, list[str]] = {
    "1A": [],
    "1B": ["1A"],
    "1C": ["1B"],
    "2A": ["1A", "1B", "1C"],  # Stage 2 cannot start until all of Stage 1 is done
    "2B": ["2A"],
    "2C-1": ["2B"],
    "2C-2": ["2C-1"],
    "2C-3": ["2C-2"],
    "2C-4": ["2C-3"],
    "2C-5": ["2C-4"],
    "2C-6": ["2C-5"],
    "3":    ["2C-6"],
    "4":    ["3"],
}

# Section writing order (canonical)
SECTION_ORDER = ["methods", "results", "discussion", "conclusion", "introduction", "abstract"]

# Mapping: section name → checkpoint ID
SECTION_CHECKPOINT: dict[str, str] = {
    "methods":      "2C-1",
    "results":      "2C-2",
    "discussion":   "2C-3",
    "conclusion":   "2C-4",
    "introduction": "2C-5",
    "abstract":     "2C-6",
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
        for cp in CHECKPOINT_SEQUENCE:
            info = CHECKPOINT_MAP[cp]
            cleared = session.is_cleared(cp)
            icon = "✓" if cleared else "○"
            label = f"CP {cp:4s}  {icon}  {info['after']}"
            if not cleared:
                ok, missing = ARPipeline.can_proceed_to(cp, session)
                if not ok:
                    label += f"  [blocked: needs {', '.join(missing)}]"
            lines.append(label)
        return lines

    @staticmethod
    def stage_banner(stage_num: int) -> str:
        banners = {
            1: "STAGE 1 — Data Analysis & Visualization",
            2: "STAGE 2 — Literature & Writing",
            3: "STAGE 3 — Peer Review",
            4: "STAGE 4 — Revision & Proofreading",
        }
        return banners.get(stage_num, f"STAGE {stage_num}")

    @staticmethod
    def progress_summary(session: "ARSession") -> dict:
        total = len(CHECKPOINT_SEQUENCE)
        cleared = sum(1 for cp in CHECKPOINT_SEQUENCE if session.is_cleared(cp))
        next_cp = ARPipeline.next_checkpoint(session)
        current_stage = CHECKPOINT_MAP[next_cp]["stage"] if next_cp else 4
        return {
            "total": total,
            "cleared": cleared,
            "pct": round(cleared / total * 100),
            "next_checkpoint": next_cp,
            "current_stage": current_stage,
            "current_skill": ARPipeline.current_skill(session),
            "done": next_cp is None,
        }
