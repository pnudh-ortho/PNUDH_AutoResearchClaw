"""
AutoResearch Web UI — FastAPI backend
Run via: autoresearch web
"""
from __future__ import annotations

import asyncio
import fcntl
import os
import re
import select
import socket
import subprocess
import time
from pathlib import Path

import yaml
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

PROJECT_DIR  = Path(__file__).parent.parent.parent
STATIC_DIR   = Path(__file__).parent / "static"
DEFAULT_CFG  = PROJECT_DIR / "config.autoresearch.yaml"

app = FastAPI(title="AutoResearch Web UI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _save_yaml(data: dict, p: Path) -> None:
    with p.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def _slug(name: str) -> str:
    return re.sub(r"[^\w\-]", "_", name).strip("_") or "project"


def _win_path(p: Path) -> str:
    try:
        r = subprocess.run(["wslpath", "-w", str(p)], capture_output=True, text=True, timeout=3)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:
        pass
    return r"\\wsl$\Ubuntu" + str(p)


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        out[k] = _deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


# ── root ──────────────────────────────────────────────────────────────────────

@app.get("/")
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


# ── config ────────────────────────────────────────────────────────────────────

@app.get("/api/config/default")
async def config_default():
    return _load_yaml(DEFAULT_CFG)


@app.get("/api/config/{name}")
async def config_load(name: str):
    p = PROJECT_DIR / f"config.{_slug(name)}.yaml"
    if not p.exists():
        return _load_yaml(DEFAULT_CFG)
    return _deep_merge(_load_yaml(DEFAULT_CFG), _load_yaml(p))


@app.post("/api/config")
async def config_save(data: dict):
    name = (data.get("project", {}).get("name") or "").strip()
    if not name:
        raise HTTPException(400, "project.name required")
    slug = _slug(name)
    if slug != name:
        data.setdefault("project", {})["name"] = slug
    _save_yaml(data, PROJECT_DIR / f"config.{slug}.yaml")
    return {"slug": slug}


@app.get("/api/projects")
async def projects_list():
    out = []
    for p in sorted(PROJECT_DIR.glob("config.*.yaml")):
        if p.name == "config.autoresearch.yaml":
            continue
        slug = p.stem.removeprefix("config.")
        d = _load_yaml(p)
        out.append({
            "slug": slug,
            "name": d.get("project", {}).get("name", slug),
            "topic": (d.get("research", {}).get("topic") or "")[:80],
        })
    return out


# ── backgrounds ───────────────────────────────────────────────────────────────

@app.post("/api/folder/create")
async def folder_create(data: dict):
    name = _slug(data.get("name", ""))
    if not name:
        raise HTTPException(400, "name required")
    folder = PROJECT_DIR / "input" / name
    folder.mkdir(parents=True, exist_ok=True)
    return {"path": str(folder)}


@app.post("/api/folder/open")
async def folder_open(data: dict):
    name = _slug(data.get("name", ""))
    folder = PROJECT_DIR / "input" / name
    folder.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.Popen(["explorer.exe", _win_path(folder)])
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/folder/files/{name}")
async def folder_files(name: str):
    folder = PROJECT_DIR / "input" / _slug(name)
    if not folder.exists():
        return {"exists": False, "files": []}
    files = sorted(
        ({"name": f.name, "size_kb": round(f.stat().st_size / 1024, 1)}
         for f in folder.rglob("*") if f.is_file()),
        key=lambda x: x["name"],
    )
    return {"exists": True, "files": files}


@app.post("/api/vscode/open")
async def vscode_open(data: dict):
    rel = data.get("path", "")
    if not rel:
        raise HTTPException(400, "path required")
    try:
        subprocess.Popen(["code", str(PROJECT_DIR / rel)], cwd=str(PROJECT_DIR))
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── pipeline ──────────────────────────────────────────────────────────────────

def _latest_session():
    from autoresearch.session import ARSession
    return ARSession.latest()


@app.get("/api/pipeline/status")
async def pipeline_status(session_id: str | None = None):
    try:
        from autoresearch.session import ARSession
        from autoresearch.pipeline import ARPipeline, CHECKPOINT_MAP, CHECKPOINT_SEQUENCE
        s = ARSession.load(session_id) if session_id else _latest_session()
        prog = ARPipeline.progress_summary(s)
        checkpoints = []
        for cp in CHECKPOINT_SEQUENCE:
            info = CHECKPOINT_MAP[cp]
            ok, missing = ARPipeline.can_proceed_to(cp, s)
            checkpoints.append({
                "id": cp,
                "stage": info["stage"],
                "phase": info["phase"],
                "description": info["after"],
                "skill": info["skill"],
                "cleared": s.is_cleared(cp),
                "note": s.checkpoint_notes.get(cp, ""),
                "can_approve": ok and not s.is_cleared(cp),
                "blocked_by": missing,
            })
        return {
            "session_id": s.session_id,
            "topic": s.topic,
            "progress": prog,
            "checkpoints": checkpoints,
        }
    except FileNotFoundError:
        return {"error": "no_session"}


@app.get("/api/pipeline/sessions")
async def pipeline_sessions():
    try:
        from autoresearch.session import ARSession
        from autoresearch.pipeline import ARPipeline
        sessions = ARSession.list_all()
        out = []
        for s in sessions:
            prog = ARPipeline.progress_summary(s)
            out.append({
                "session_id": s.session_id,
                "topic": s.topic[:60],
                "cleared": prog["cleared"],
                "total": prog["total"],
                "pct": prog["pct"],
            })
        return out
    except Exception:
        return []


@app.post("/api/pipeline/new")
async def pipeline_new(data: dict):
    config_name = data.get("config_slug", "")
    try:
        from autoresearch.session import ARSession
        if config_name:
            p = PROJECT_DIR / f"config.{config_name}.yaml"
            s = ARSession.from_config(str(p))
        else:
            topic = data.get("topic", "").strip()
            if not topic:
                raise HTTPException(400, "topic or config_slug required")
            s = ARSession.new(topic=topic)
        return {"session_id": s.session_id, "topic": s.topic}
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/api/pipeline/approve")
async def pipeline_approve(data: dict):
    cp_id = data.get("cp_id", "").upper()
    note  = data.get("note", "")
    session_id = data.get("session_id")
    try:
        from autoresearch.session import ARSession
        from autoresearch.pipeline import ARPipeline, CHECKPOINT_MAP
        s = ARSession.load(session_id) if session_id else _latest_session()
        if cp_id not in CHECKPOINT_MAP:
            raise HTTPException(400, f"Unknown checkpoint: {cp_id}")
        ok, missing = ARPipeline.can_proceed_to(cp_id, s)
        if not ok:
            raise HTTPException(400, f"Missing: {missing}")
        s.clear_checkpoint(cp_id, note=note)
        return {"approved": cp_id}
    except FileNotFoundError:
        raise HTTPException(404, "No session")


@app.post("/api/pipeline/revoke")
async def pipeline_revoke(data: dict):
    cp_id = data.get("cp_id", "").upper()
    session_id = data.get("session_id")
    try:
        from autoresearch.session import ARSession
        s = ARSession.load(session_id) if session_id else _latest_session()
        revoked = s.revoke_from(cp_id)
        return {"revoked": revoked}
    except FileNotFoundError:
        raise HTTPException(404, "No session")


@app.post("/api/pipeline/run")
async def pipeline_run(data: dict):
    component = data.get("component", "").lower()
    session_id = data.get("session_id")
    try:
        from autoresearch.session import ARSession
        s = ARSession.load(session_id) if session_id else _latest_session()
    except FileNotFoundError:
        raise HTTPException(404, "No session")

    from autoresearch.workspace import WorkSpace
    ws = WorkSpace(s)

    if component == "synthesis":
        from autoresearch.stages.review import auto_synthesize_if_ready
        if not ws.all_reviews_present():
            raise HTTPException(400, "Missing reviewer files (reviewer_a/b/c.md)")
        result = auto_synthesize_if_ready(s, ws)
        return {"output": result or "Synthesis failed"}

    elif component == "proofread":
        from autoresearch.stages.proofreader import run_all_checks, format_cp4_report, save_proofread_to_session
        manuscript = ws.read_full_manuscript()
        if not manuscript:
            raise HTTPException(400, "No manuscript found. Complete Stage 6 first.")
        report = run_all_checks(manuscript, expected_figure_count=len(s.figure_list or []))
        text = format_cp4_report(report)
        save_proofread_to_session(ws, text, session=s)
        return {"output": text, "issues": len(report.issues)}

    elif component == "pubmed":
        from autoresearch.stages.literature import search_pubmed, format_search_results, save_literature_to_session
        query = data.get("query") or s.topic
        max_r = int(data.get("max_results", 20))
        results = search_pubmed(query, max_results=max_r)
        formatted = format_search_results(results, source="PubMed")
        ws.save_search_log(formatted)
        return {"output": formatted, "count": len([r for r in results if "error" not in r])}

    elif component == "intake":
        topic_dir = PROJECT_DIR / "input" / _slug(data.get("topic", ""))
        if not topic_dir.exists():
            raise HTTPException(400, f"Folder not found: {topic_dir}")
        classified = WorkSpace.classify_input_files(topic_dir)
        entry, reason, auto_clear = WorkSpace.determine_entry_point(classified)
        total = sum(len(v) for v in classified.values())

        # Build markdown report and persist to session workspace
        lines = [f"# Intake Report\n\n**Topic dir:** `{topic_dir}`\n"]
        lines.append(f"**Entry point:** {entry}  \n**Reason:** {reason}\n")
        lines.append(f"**Total files:** {total}\n")
        if classified:
            lines.append("\n## Classified Files\n")
            for cat, files in classified.items():
                if files:
                    lines.append(f"\n### {cat}\n")
                    for f in files:
                        lines.append(f"- {f.name}")
        report_md = "\n".join(lines)

        ws.save_intake_report(report_md)
        s.intake_report = report_md
        s.intake_entry_point = entry
        s.source_input_dir = str(topic_dir)
        s.save()

        return {
            "total": total,
            "classified": {k: [p.name for p in v] for k, v in classified.items() if v},
            "entry_point": entry,
            "reason": reason,
            "auto_clear": auto_clear,
            "report": report_md,
        }

    raise HTTPException(400, f"Unknown component: {component}")


@app.post("/api/pipeline/export")
async def pipeline_export(data: dict):
    session_id = data.get("session_id")
    try:
        from autoresearch.session import ARSession
        from autoresearch.workspace import WorkSpace
        s = ARSession.load(session_id) if session_id else _latest_session()
        ws = WorkSpace(s)
        revised = ws.revision_dir / "revised_manuscript.md"
        final = revised if revised.exists() else ws.assemble_manuscript(s)
        bundle = ws.root / "final_output.md"
        sections = [f"# {s.topic}\n\n*Generated by AutoResearch*\n", final.read_text(encoding="utf-8")]
        bundle.write_text("\n\n".join(sections), encoding="utf-8")
        return {"path": str(bundle.relative_to(PROJECT_DIR))}
    except FileNotFoundError:
        raise HTTPException(404, "No session")


# ── acpx / Claude Code WebSocket ──────────────────────────────────────────────

import shutil

_DONE_RE   = re.compile(r"^\[done\]")
_CLIENT_RE = re.compile(r"^\[client\]")
_ACPX_RE   = re.compile(r"^\[acpx\]")
_TOOL_RE   = re.compile(r"^\[tool\]")


def _find_acpx() -> str | None:
    found = shutil.which("acpx")
    if found:
        return found
    bundled = os.path.expanduser("~/.openclaw/extensions/acpx/node_modules/.bin/acpx")
    if os.path.isfile(bundled) and os.access(bundled, os.X_OK):
        return bundled
    return None


def _is_metadata(line: str) -> bool:
    return bool(
        _DONE_RE.match(line) or _CLIENT_RE.match(line) or
        _ACPX_RE.match(line) or _TOOL_RE.match(line)
    )


@app.websocket("/ws/claude/{session_name}")
async def ws_claude(websocket: WebSocket, session_name: str):
    """Stream Claude Code responses via acpx named sessions."""
    await websocket.accept()

    acpx = _find_acpx()
    if not acpx:
        await websocket.send_json({
            "type": "error",
            "text": "acpx를 찾을 수 없습니다.\n  npm install -g acpx  으로 설치하세요."
        })
        await websocket.close()
        return

    # Ensure acpx session exists (run from PROJECT_DIR so acpx finds/creates session there)
    try:
        r = await asyncio.create_subprocess_exec(
            acpx, "claude", "sessions", "new", "--name", session_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(PROJECT_DIR),
        )
        await r.wait()
    except Exception:
        pass  # session may already exist; ignore

    await websocket.send_json({"type": "ready", "text": f"세션 '{session_name}' 준비됨"})

    _proc: asyncio.subprocess.Process | None = None

    try:
        while True:
            msg = await websocket.receive_json()
            msg_type = msg.get("type", "send")

            if msg_type == "kill":
                if _proc is not None and _proc.returncode is None:
                    _proc.kill()
                break

            if msg_type != "send":
                continue

            prompt = msg.get("text", "").strip()
            if not prompt:
                continue

            await websocket.send_json({"type": "thinking"})

            cmd = [
                acpx, "--approve-all", "--ttl", "0",
                "--cwd", str(PROJECT_DIR),
                "claude", "-s", session_name, prompt,
            ]

            try:
                _proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(PROJECT_DIR),
                )
            except FileNotFoundError as e:
                await websocket.send_json({"type": "error", "text": str(e)})
                _proc = None
                continue

            in_tool_block = False
            response_lines: list[str] = []
            stderr_lines: list[str] = []

            # Collect stderr concurrently to prevent buffer deadlock
            async def _collect_stderr():
                async for raw in _proc.stderr:
                    stderr_lines.append(raw.decode("utf-8", errors="replace").rstrip("\n"))

            stderr_task = asyncio.create_task(_collect_stderr())

            # Keepalive: send a ping every 20 s while the process runs
            last_ping = asyncio.get_event_loop().time()

            async for raw in _proc.stdout:
                now = asyncio.get_event_loop().time()
                if now - last_ping >= 20:
                    await websocket.send_json({"type": "heartbeat"})
                    last_ping = now

                line = raw.decode("utf-8", errors="replace").rstrip("\n")

                # Filter acpx metadata
                if _DONE_RE.match(line) or _CLIENT_RE.match(line) or _ACPX_RE.match(line):
                    in_tool_block = False
                    continue
                if _TOOL_RE.match(line):
                    in_tool_block = True
                    continue
                if in_tool_block:
                    if line.startswith("  ") or not line.strip():
                        continue
                    in_tool_block = False

                response_lines.append(line)
                await websocket.send_json({"type": "stream", "text": line + "\n"})

            await _proc.wait()
            await stderr_task

            full = "\n".join(response_lines).strip()

            # If no output, surface stderr and exit code for diagnosis
            if not full:
                stderr_text = "\n".join(stderr_lines).strip()
                exit_code = _proc.returncode
                diag = f"[acpx exited {exit_code}, no output]"
                if stderr_text:
                    diag += f"\nstderr:\n{stderr_text}"
                await websocket.send_json({"type": "error", "text": diag})

            await websocket.send_json({"type": "done", "full": full})
            _proc = None

    except WebSocketDisconnect:
        if _proc is not None and _proc.returncode is None:
            _proc.kill()


# ── server entry ──────────────────────────────────────────────────────────────

def serve(port: int = 8080, open_browser: bool = True) -> None:
    import uvicorn

    for p in range(port, port + 10):
        with socket.socket() as s:
            if s.connect_ex(("localhost", p)) != 0:
                port = p
                break

    url = f"http://localhost:{port}"
    print(f"\n  AutoResearch Web UI → {url}\n")

    if open_browser:
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", url])
        except Exception:
            pass

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
