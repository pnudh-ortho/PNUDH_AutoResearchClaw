"""
AutoResearch — AI-assisted manuscript writing pipeline for solo biomedical researchers.

Input:  topic · raw data · reference papers (user-provided)
Output: complete manuscript draft · analysis code · figure code · figure captions

Stages:
  Stage 1  Data Analysis (CP 1A, 1B) + Visualization (CP 1C)
  Stage 2  Literature (CP 2A) + Story Writer (CP 2B) + Section Writer ×6 (CP 2C-1…6)
  Stage 3  Review A ∥ Review B ∥ Review C → Synthesis (CP 3)
  Stage 4  Revision (CP 4) + Proofreader

Usage:
  autoresearch new --topic "..."
  autoresearch status
  autoresearch approve 1A
  autoresearch run --stage 2A
"""

__version__ = "1.0.0"

from autoresearch.session import ARSession
from autoresearch.pipeline import ARPipeline, CHECKPOINT_MAP, STAGE_DEPS
from autoresearch.workspace import WorkSpace

__all__ = ["ARSession", "ARPipeline", "WorkSpace", "CHECKPOINT_MAP", "STAGE_DEPS"]
