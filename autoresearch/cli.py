"""
AutoResearch CLI

Usage:
  autoresearch new --topic "..."
  autoresearch status [SESSION_ID]
  autoresearch approve <CP_ID> [SESSION_ID] [--note "..."]
  autoresearch revoke  <CP_ID> [SESSION_ID]
  autoresearch run     <CP_ID> [SESSION_ID]
  autoresearch sessions
  autoresearch export  [SESSION_ID]

SESSION_ID defaults to the most recently created session.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _get_session(session_id: str | None):
    from autoresearch.session import ARSession
    if session_id:
        return ARSession.load(session_id)
    return ARSession.latest()


def _print_status(session) -> None:
    from autoresearch.pipeline import ARPipeline
    prog = ARPipeline.progress_summary(session)

    print(f"\n{'='*60}")
    print(f"Session:    {session.session_id}")
    print(f"Topic:      {session.topic}")
    print(f"Progress:   {prog['cleared']}/{prog['total']} checkpoints ({prog['pct']}%)")
    if prog["done"]:
        print("Status:     ✓ COMPLETE — ready for final export")
    else:
        cp = prog["next_checkpoint"]
        print(f"Next:       CP {cp} — load skill: {prog['current_skill']}")
    print(f"{'='*60}")
    print()

    for line in ARPipeline.status_lines(session):
        print(" ", line)
    print()


def _print_workspace(session) -> None:
    from autoresearch.workspace import WorkSpace
    ws = WorkSpace(session)
    print(ws.summary())


# ──────────────────────────────────────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────────────────────────────────────

def cmd_new(args) -> None:
    from autoresearch.session import ARSession, load_ar_config

    config_path = getattr(args, "config", None)

    # Config-file mode: topic comes from the YAML
    if config_path or (not getattr(args, "topic", None)):
        try:
            session = ARSession.from_config(config_path)
        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)
            print("  Either fix the config file or use --topic flag.", file=sys.stderr)
            sys.exit(1)
    else:
        session = ARSession.new(
            topic=args.topic,
            journal_target=getattr(args, "journal", ""),
        )

    print(f"\n✓ Session created: {session.session_id}")
    print(f"  Workspace: {session.workspace_dir}")
    print(f"\n  Next step: place files in input/[topic]/ then run: autoresearch intake [topic]")
    print(f"  Or load the intake skill in Claude and say 'start'.\n")
    _print_status(session)


def cmd_status(args) -> None:
    try:
        session = _get_session(getattr(args, "session_id", None))
        _print_status(session)
        _print_workspace(session)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_approve(args) -> None:
    from autoresearch.pipeline import ARPipeline, CHECKPOINT_MAP
    try:
        session = _get_session(getattr(args, "session_id", None))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cp_id = args.cp_id.upper()
    if cp_id not in CHECKPOINT_MAP:
        print(f"Error: Unknown checkpoint '{cp_id}'", file=sys.stderr)
        sys.exit(1)

    ok, missing = ARPipeline.can_proceed_to(cp_id, session)
    if not ok:
        print(f"Error: Cannot approve CP {cp_id} — missing: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    note = getattr(args, "note", "") or ""
    session.clear_checkpoint(cp_id, note=note)

    print(f"\n✓ Checkpoint {cp_id} approved.")
    if note:
        print(f"  Note: {note}")

    prog = ARPipeline.progress_summary(session)
    if prog["done"]:
        print("\n🎉 All 13 checkpoints cleared. Manuscript pipeline complete!")
        print(f"   Run `autoresearch export` to assemble the final output.")
    else:
        next_cp = prog["next_checkpoint"]
        skill = prog["current_skill"]
        print(f"\n  Next: CP {next_cp} — load skill: {skill}")
    print()


def cmd_revoke(args) -> None:
    from autoresearch.pipeline import CHECKPOINT_MAP
    try:
        session = _get_session(getattr(args, "session_id", None))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cp_id = args.cp_id.upper()
    revoked = session.revoke_from(cp_id)
    if revoked:
        print(f"\n✓ Revoked checkpoints: {', '.join(revoked)}")
        print(f"  Pipeline rolled back to before CP {cp_id}.\n")
    else:
        print(f"  CP {cp_id} was not cleared — nothing to revoke.\n")


def cmd_run(args) -> None:
    """
    Run an automated stage component (where automation is possible).
    Currently supports:
      - 3-synthesis  : auto-synthesize reviews if all three exist
      - 4-proofread  : run automated proofreading checks
    """
    from autoresearch.pipeline import CHECKPOINT_MAP
    try:
        session = _get_session(getattr(args, "session_id", None))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cmd = args.component.lower()

    if cmd in ("3-synthesis", "review-synthesis", "synthesis"):
        _run_review_synthesis(session)
    elif cmd in ("4-proofread", "proofread"):
        _run_proofread(session)
    elif cmd in ("pubmed",):
        _run_pubmed_search(session, args)
    else:
        print(f"Unknown component: {cmd!r}", file=sys.stderr)
        print("Available: synthesis | proofread | pubmed", file=sys.stderr)
        sys.exit(1)


def _run_review_synthesis(session) -> None:
    from autoresearch.workspace import WorkSpace
    from autoresearch.stages.review import auto_synthesize_if_ready

    ws = WorkSpace(session)
    if not ws.all_reviews_present():
        missing = [r for r in ("a", "b", "c") if not (ws.review_dir / f"reviewer_{r}.md").exists()]
        print(f"Error: Missing reviews: {', '.join(f'reviewer_{r}.md' for r in missing)}", file=sys.stderr)
        print("  Save each reviewer's output to stage3/ and re-run.", file=sys.stderr)
        sys.exit(1)

    synthesis = auto_synthesize_if_ready(session, ws)
    if synthesis:
        print(f"\n✓ Review synthesis generated: {ws.review_dir / 'synthesis.md'}")
        print("\n" + synthesis)
    else:
        print("Error: Could not generate synthesis.", file=sys.stderr)
        sys.exit(1)


def _run_proofread(session) -> None:
    from autoresearch.workspace import WorkSpace
    from autoresearch.stages.proofreader import run_all_checks, format_cp4_report, save_proofread_to_session

    ws = WorkSpace(session)
    manuscript = ws.read_full_manuscript()
    if not manuscript:
        print("Error: No manuscript found. Complete Stage 2-C first.", file=sys.stderr)
        sys.exit(1)

    n_figures = len(session.figure_list) if session.figure_list else 0
    report = run_all_checks(
        manuscript,
        expected_figure_count=n_figures,
    )
    report_text = format_cp4_report(report)
    save_proofread_to_session(ws, report_text, session=session)

    print(f"\n✓ Proofreading complete: {len(report.issues)} issues found.")
    print(f"  Report: {ws.proofread_dir / 'proofread_report.md'}")
    print()
    print(report_text)


def _run_pubmed_search(session, args) -> None:
    from autoresearch.workspace import WorkSpace
    from autoresearch.stages.literature import search_pubmed, format_search_results, save_literature_to_session

    query = getattr(args, "query", session.topic)
    max_results = getattr(args, "max_results", 20)

    print(f"\nSearching PubMed: {query!r} (max {max_results})…")
    results = search_pubmed(query, max_results=max_results)
    formatted = format_search_results(results, source="PubMed")

    ws = WorkSpace(session)
    ws.save_search_log(formatted)
    print(f"✓ {len([r for r in results if 'error' not in r])} papers found.")
    print(f"  Saved to: {ws.literature_dir / 'search_log.md'}")
    print()
    print(formatted)


def cmd_intake(args) -> None:
    """
    Scan input/[topic]/ and print the intake classification report.
    Does NOT create a session or move files — that is done interactively
    by the intake skill in Claude. This command is a helper for that skill.
    """
    from autoresearch.workspace import WorkSpace

    input_root = Path("input")
    if not input_root.exists():
        print("Error: No 'input/' directory found at project root.", file=sys.stderr)
        print("  Create: input/[your-study-name]/ and drop your files there.", file=sys.stderr)
        sys.exit(1)

    # Determine which topic folder to use
    topic_name = getattr(args, "topic", None)
    if topic_name:
        topic_dir = input_root / topic_name
        if not topic_dir.exists():
            print(f"Error: input/{topic_name}/ not found.", file=sys.stderr)
            sys.exit(1)
    else:
        subdirs = [d for d in input_root.iterdir() if d.is_dir()]
        if not subdirs:
            print("No topic folders found in input/.", file=sys.stderr)
            print("  Create a folder: input/[your-study-name]/", file=sys.stderr)
            sys.exit(1)
        if len(subdirs) > 1:
            print("Multiple topic folders found in input/:")
            for d in sorted(subdirs):
                files = list(d.rglob("*"))
                n = sum(1 for f in files if f.is_file())
                print(f"  {d.name}/  ({n} files)")
            print("\nSpecify one: autoresearch intake [topic-name]")
            sys.exit(0)
        topic_dir = subdirs[0]

    # Classify
    classified = WorkSpace.classify_input_files(topic_dir)
    entry_stage, reason, auto_clear = WorkSpace.determine_entry_point(classified)

    LABELS = {
        "raw_data":       "Raw data",
        "analysis_output":"Analysis output",
        "figure_image":   "Figure images",
        "figure_code":    "Figure code",
        "analysis_code":  "Analysis code",
        "reference_pdf":  "Reference PDFs",
        "bibliography":   "Bibliography",
        "manuscript_draft":"Manuscript drafts",
        "protocol_doc":   "Protocol/design docs",
        "notes":          "Notes/context",
        "unclear":        "Unclear (needs review)",
    }

    total = sum(len(v) for v in classified.values())
    print(f"\n{'='*60}")
    print(f"Intake Report — input/{topic_dir.name}/")
    print(f"{'='*60}\n")
    print(f"Files found: {total}\n")

    for key, label in LABELS.items():
        files = classified.get(key, [])
        if files:
            names = ", ".join(p.name for p in files)
            print(f"  {label:<22} ({len(files)}): {names}")

    print(f"\n{'─'*60}")
    print(f"Recommended entry point: {entry_stage}")
    print(f"Reason: {reason}")
    if auto_clear:
        print(f"\nCheckpoints to auto-clear (with researcher approval):")
        for cp in auto_clear:
            print(f"  CP {cp}")
    print(f"{'─'*60}")
    print(f"\nNext: load the intake skill in Claude and say 'start'")
    print(f"      or run: autoresearch new --topic \"{topic_dir.name.replace('_', ' ').title()}\"\n")


def cmd_sessions(args) -> None:
    from autoresearch.session import ARSession
    sessions = ARSession.list_all()
    if not sessions:
        print("No sessions found. Run `autoresearch new` to start.")
        return
    print(f"\n{'ID':<30} {'Topic':<40} {'CPs':>4}")
    print("-" * 76)
    for s in sessions:
        cps = f"{len(s.cleared_checkpoints)}/13"
        print(f"{s.session_id:<30} {s.topic[:40]:<40} {cps:>4}")
    print()


def cmd_export(args) -> None:
    """Assemble and export the final manuscript."""
    from autoresearch.workspace import WorkSpace
    try:
        session = _get_session(getattr(args, "session_id", None))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    ws = WorkSpace(session)

    # Use revised manuscript if it exists, otherwise assemble from sections
    revised = ws.revision_dir / "revised_manuscript.md"
    if revised.exists():
        final_path = revised
        print(f"\n✓ Using revised manuscript: {revised}")
    else:
        final_path = ws.assemble_manuscript(session)
        print(f"\n✓ Assembled manuscript: {final_path}")

    # Also write a combined output bundle
    bundle = ws.root / "final_output.md"
    sections = [
        f"# {session.topic}\n\n*Generated by AutoResearch*\n",
        final_path.read_text(encoding="utf-8"),
    ]
    if (ws.figures_dir / "captions.md").exists():
        sections.append("\n---\n\n## Figure Captions\n\n" + (ws.figures_dir / "captions.md").read_text(encoding="utf-8"))
    if (ws.revision_dir / "change_log.md").exists():
        sections.append("\n---\n\n" + (ws.revision_dir / "change_log.md").read_text(encoding="utf-8"))
    bundle.write_text("\n\n".join(sections), encoding="utf-8")

    print(f"✓ Final bundle: {bundle}")
    print(f"\n  Figure scripts: {ws.figures_dir}")
    print(f"  Analysis code:  {ws.analysis_dir}")
    print(f"  References:     {ws.literature_dir / 'included_papers.bib'}\n")


# ──────────────────────────────────────────────────────────────────────────────
# Argument parser
# ──────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autoresearch",
        description="AutoResearch — AI-assisted manuscript writing pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # new
    p_new = sub.add_parser("new", help="Start a new research session")
    p_new.add_argument("--config", default=None,
                       help="Path to config.autoresearch.yaml (default: auto-detect)")
    p_new.add_argument("--topic", default=None, help="Research topic (overrides config)")
    p_new.add_argument("--journal", default="", help="Target journal (optional)")

    # status
    p_status = sub.add_parser("status", help="Show pipeline status")
    p_status.add_argument("session_id", nargs="?", default=None)

    # approve
    p_approve = sub.add_parser("approve", help="Mark a checkpoint as approved")
    p_approve.add_argument("cp_id", help="Checkpoint ID (e.g. 1A, 2B, 2C-1)")
    p_approve.add_argument("session_id", nargs="?", default=None)
    p_approve.add_argument("--note", default="", help="Optional approval note")

    # revoke
    p_revoke = sub.add_parser("revoke", help="Roll back to before a checkpoint")
    p_revoke.add_argument("cp_id", help="Checkpoint ID to revoke from")
    p_revoke.add_argument("session_id", nargs="?", default=None)

    # run
    p_run = sub.add_parser("run", help="Run an automated stage component")
    p_run.add_argument("component", choices=["synthesis", "proofread", "pubmed"],
                       help="synthesis=review synthesis; proofread=automated checks; pubmed=PubMed search")
    p_run.add_argument("session_id", nargs="?", default=None)
    p_run.add_argument("--query", default="", help="Search query for pubmed")
    p_run.add_argument("--max-results", type=int, default=20)

    # intake
    p_intake = sub.add_parser(
        "intake",
        help="Scan input/[topic]/ and print the classification report (no files moved)",
    )
    p_intake.add_argument(
        "topic", nargs="?", default=None,
        help="Topic folder name under input/ (auto-detected if only one exists)",
    )

    # sessions
    sub.add_parser("sessions", help="List all sessions")

    # export
    p_export = sub.add_parser("export", help="Assemble and export the final manuscript")
    p_export.add_argument("session_id", nargs="?", default=None)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "new":      cmd_new,
        "status":   cmd_status,
        "approve":  cmd_approve,
        "revoke":   cmd_revoke,
        "run":      cmd_run,
        "intake":   cmd_intake,
        "sessions": cmd_sessions,
        "export":   cmd_export,
    }

    fn = dispatch.get(args.command)
    if fn is None:
        parser.print_help()
        sys.exit(1)
    fn(args)


if __name__ == "__main__":
    main()
