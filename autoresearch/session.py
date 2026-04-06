"""
ARSession — AutoResearch pipeline session.

One session = one manuscript project.
Tracks which checkpoints have been cleared and persists state to disk.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autoresearch.pipeline import CHECKPOINT_SEQUENCE

# ── default session root ────────────────────────────────────────────────────
_DEFAULT_SESSIONS_ROOT = Path("sessions")

# ── config file search order ────────────────────────────────────────────────
_CONFIG_SEARCH = [
    Path("config.autoresearch.yaml"),
    Path("config.yaml"),
]


def load_ar_config(config_path: str | Path | None = None) -> dict:
    """
    Load an AutoResearch config file (YAML).
    Search order if config_path is None:
      1. config.autoresearch.yaml
      2. config.yaml
    Returns an empty dict if no file is found.
    """
    try:
        import yaml
    except ImportError:
        return {}

    candidates = [Path(config_path)] if config_path else _CONFIG_SEARCH
    for p in candidates:
        if p.exists():
            with p.open(encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    return {}


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ──────────────────────────────────────────────────────────────────────────────
# Session data model
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ARSession:
    """
    Persistent state for one AutoResearch pipeline run.

    Fields written to session.json; loaded on resume.
    """

    # ── identity ──────────────────────────────────────────────────────────
    session_id: str
    created_at: str
    updated_at: str

    # ── research context ─────────────────────────────────────────────────
    topic: str
    journal_target: str = ""          # optional target journal / style

    # ── workspace root ───────────────────────────────────────────────────
    workspace_dir: str = ""           # stored as str for JSON; cast to Path on load

    # ── pipeline state ───────────────────────────────────────────────────
    cleared_checkpoints: list[str] = field(default_factory=list)
    # Freeform notes per checkpoint, e.g. {"1A": "approved Mann-Whitney approach"}
    checkpoint_notes: dict[str, str] = field(default_factory=dict)
    # Key outputs confirmed at each checkpoint (paths relative to workspace_dir)
    checkpoint_artifacts: dict[str, list[str]] = field(default_factory=dict)

    # ── stage-level summaries (for downstream context) ───────────────────
    # Filled by stage runners; consumed by later stages
    analysis_summary: str = ""        # CP 1B output: 3-5 bullet summary for Story Writer
    figure_list: list[dict] = field(default_factory=list)  # confirmed figures from CP 1C
    literature_synthesis: str = ""    # CP 2A output: thematic synthesis
    key_message: str = ""             # CP 2B output: key message sentence
    narrative_arc: str = ""           # CP 2B output: arc description
    # Section drafts: section_name → content
    section_drafts: dict[str, str] = field(default_factory=dict)
    # Review outputs
    review_a: str = ""
    review_b: str = ""
    review_c: str = ""
    review_synthesis: str = ""        # CP 3 auto-synthesis
    # Revision
    change_log: list[dict] = field(default_factory=list)
    items_not_addressed: list[dict] = field(default_factory=list)
    # Stage 4-B
    proofread_report: str = ""

    # ── intake metadata ──────────────────────────────────────────────────
    # Set by the intake skill (Stage 0) so later sessions know their origin
    source_input_dir: str = ""      # e.g. "input/obesity_treatment"
    intake_entry_point: str = ""    # e.g. "Stage 1-A", "Stage 1-C", "Stage 2-A"

    # ──────────────────────────────────────────────────────────────────────
    # Construction
    # ──────────────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config_path: str | Path | None = None) -> "ARSession":
        """
        Create a new session by reading research.topic (and other fields)
        directly from a config file.

        Usage:
            session = ARSession.from_config("config.autoresearch.yaml")
        """
        cfg = load_ar_config(config_path)

        research = cfg.get("research", {})
        topic = str(research.get("topic", "")).strip()
        if not topic:
            raise ValueError("config must have research.topic set.")

        journal_target = str(research.get("journal_target", ""))
        pipeline_cfg = cfg.get("pipeline", {})
        sessions_dir = pipeline_cfg.get("sessions_dir", "sessions")
        sessions_root = Path(sessions_dir)

        session = cls.new(
            topic=topic,
            journal_target=journal_target,
            sessions_root=sessions_root,
        )
        # Attach raw config for downstream stage use
        session._config = cfg  # type: ignore[attr-defined]
        return session

    @classmethod
    def new(
        cls,
        topic: str,
        *,
        journal_target: str = "",
        sessions_root: Path | None = None,
    ) -> "ARSession":
        """Create a brand-new session and its workspace directory."""
        root = sessions_root or _DEFAULT_SESSIONS_ROOT
        sid = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        ws = root / sid
        ws.mkdir(parents=True, exist_ok=True)

        now = _utcnow()
        session = cls(
            session_id=sid,
            created_at=now,
            updated_at=now,
            topic=topic,
            journal_target=journal_target,
            workspace_dir=str(ws),
        )
        # Create subdirectory scaffold
        from autoresearch.workspace import WorkSpace
        WorkSpace(session).scaffold()

        session.save()
        return session

    @classmethod
    def _from_json_file(cls, path: Path) -> "ARSession":
        """Load a session from a session.json file path."""
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)

    @classmethod
    def load(cls, identifier: str | Path, sessions_root: Path | None = None) -> "ARSession":
        """
        Load a session by session_id string or by direct path to session.json
        (or the workspace directory).
        """
        path = Path(identifier)

        # Direct path to workspace dir or session.json
        if path.exists():
            if path.is_dir():
                path = path / "session.json"
            return cls._from_json_file(path)

        # Lookup by session_id string under sessions_root
        root = sessions_root or _DEFAULT_SESSIONS_ROOT
        candidate = root / str(identifier) / "session.json"
        if candidate.exists():
            return cls._from_json_file(candidate)

        raise FileNotFoundError(f"No session found for identifier: {identifier!r}")

    @classmethod
    def latest(cls, sessions_root: Path | None = None) -> "ARSession":
        """Load the most recently created session."""
        root = sessions_root or _DEFAULT_SESSIONS_ROOT
        candidates = sorted(
            (p for p in root.glob("*/session.json") if p.exists()),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            raise FileNotFoundError(f"No sessions found in {root}")
        return cls._from_json_file(candidates[0])

    @classmethod
    def list_all(cls, sessions_root: Path | None = None) -> list["ARSession"]:
        import sys as _sys
        root = sessions_root or _DEFAULT_SESSIONS_ROOT
        sessions = []
        for p in sorted(root.glob("*/session.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                sessions.append(cls._from_json_file(p))
            except Exception as e:
                print(f"Warning: skipped corrupted session at {p}: {e}", file=_sys.stderr)
        return sessions

    # ──────────────────────────────────────────────────────────────────────
    # Persistence
    # ──────────────────────────────────────────────────────────────────────

    @property
    def workspace(self) -> Path:
        return Path(self.workspace_dir)

    @property
    def _session_file(self) -> Path:
        return self.workspace / "session.json"

    def save(self) -> None:
        """Persist session state to session.json (atomic write)."""
        self.updated_at = _utcnow()
        data = asdict(self)
        tmp = self._session_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self._session_file)

    # ──────────────────────────────────────────────────────────────────────
    # Checkpoint management
    # ──────────────────────────────────────────────────────────────────────

    def is_cleared(self, cp_id: str) -> bool:
        return cp_id in self.cleared_checkpoints

    def clear_checkpoint(
        self,
        cp_id: str,
        note: str = "",
        artifacts: list[str] | None = None,
    ) -> None:
        """Mark a checkpoint as approved by the researcher."""
        if cp_id not in CHECKPOINT_SEQUENCE:
            raise ValueError(f"Unknown checkpoint: {cp_id!r}")
        if cp_id not in self.cleared_checkpoints:
            self.cleared_checkpoints.append(cp_id)
        if note:
            self.checkpoint_notes[cp_id] = note
        if artifacts:
            self.checkpoint_artifacts[cp_id] = artifacts
        self.save()

    def revoke_checkpoint(self, cp_id: str) -> None:
        """Un-clear a checkpoint (e.g., [REVISE] causes rollback)."""
        if cp_id in self.cleared_checkpoints:
            self.cleared_checkpoints.remove(cp_id)
        self.save()

    def revoke_from(self, cp_id: str) -> list[str]:
        """
        Revoke cp_id and all checkpoints that come after it.
        Returns list of revoked checkpoint IDs.
        """
        idx = CHECKPOINT_SEQUENCE.index(cp_id)
        to_revoke = CHECKPOINT_SEQUENCE[idx:]
        revoked = [cp for cp in to_revoke if cp in self.cleared_checkpoints]
        for cp in to_revoke:
            if cp in self.cleared_checkpoints:
                self.cleared_checkpoints.remove(cp)
        self.save()
        return revoked

    # ──────────────────────────────────────────────────────────────────────
    # Context helpers (consumed by skills at runtime)
    # ──────────────────────────────────────────────────────────────────────

    def stage1_context(self) -> str:
        """Compact context block injected into Stage 2 skills."""
        parts = [f"**Topic:** {self.topic}"]
        if self.analysis_summary:
            parts.append(f"\n**Analysis Summary (confirmed at CP 1B):**\n{self.analysis_summary}")
        if self.figure_list:
            fig_lines = "\n".join(
                f"  - Figure {i+1}: {f.get('type','?')} — {f.get('title','')}"
                for i, f in enumerate(self.figure_list)
            )
            parts.append(f"\n**Confirmed Figures (CP 1C):**\n{fig_lines}")
        return "\n".join(parts)

    def stage2_context(self) -> str:
        """Context block injected into Stage 3 skills."""
        parts = [self.stage1_context()]
        if self.literature_synthesis:
            parts.append(f"\n**Literature Synthesis (CP 2A):**\n{self.literature_synthesis[:1000]}…")
        if self.key_message:
            parts.append(f"\n**Key Message (CP 2B):** {self.key_message}")
        if self.narrative_arc:
            parts.append(f"\n**Narrative Arc (CP 2B):**\n{self.narrative_arc}")
        sections_done = list(self.section_drafts.keys())
        if sections_done:
            parts.append(f"\n**Sections confirmed:** {', '.join(sections_done)}")
        return "\n".join(parts)

    def full_manuscript(self) -> str:
        """Assemble confirmed section drafts in canonical reading order."""
        reading_order = ["abstract", "introduction", "methods", "results", "discussion", "conclusion"]
        parts = []
        for sec in reading_order:
            if sec in self.section_drafts:
                parts.append(f"## {sec.title()}\n\n{self.section_drafts[sec]}")
        return "\n\n---\n\n".join(parts)

    # ──────────────────────────────────────────────────────────────────────
    # Display helpers
    # ──────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        n_cleared = len(self.cleared_checkpoints)
        return (
            f"ARSession({self.session_id!r}, "
            f"topic={self.topic[:40]!r}, "
            f"checkpoints={n_cleared}/13)"
        )
