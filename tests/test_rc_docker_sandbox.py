"""Tests for DockerSandbox — all mocked, no real Docker needed."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from researchclaw.config import DockerSandboxConfig, ExperimentConfig
from researchclaw.experiment.docker_sandbox import DockerSandbox
from researchclaw.experiment.factory import create_sandbox
from researchclaw.experiment.sandbox import SandboxResult


# ── SandboxResult contract ─────────────────────────────────────────────


def test_sandbox_result_fields():
    r = SandboxResult(
        returncode=0,
        stdout="primary_metric: 0.95\n",
        stderr="",
        elapsed_sec=1.2,
        metrics={"primary_metric": 0.95},
        timed_out=False,
    )
    assert r.returncode == 0
    assert r.metrics["primary_metric"] == 0.95
    assert r.timed_out is False


# ── DockerSandbox command building ─────────────────────────────────────


def test_build_run_command_default(tmp_path: Path):
    cfg = DockerSandboxConfig()
    sandbox = DockerSandbox(cfg, tmp_path / "work")
    cmd = sandbox._build_run_command(
        tmp_path / "staging",
        entry_point="main.py",
        container_name="rc-test-1",
        network_disabled=True,
    )
    assert "docker" in cmd
    assert "--gpus" in cmd
    assert "--network" in cmd
    assert "none" in cmd
    assert "--memory=8192m" in cmd
    assert "--shm-size=2048m" in cmd
    assert cmd[-1] == "/workspace/main.py"
    # Should NOT contain container_python (ENTRYPOINT handles it)
    assert "/usr/bin/python3" not in cmd


def test_build_run_command_no_gpu(tmp_path: Path):
    cfg = DockerSandboxConfig(gpu_enabled=False)
    sandbox = DockerSandbox(cfg, tmp_path / "work")
    cmd = sandbox._build_run_command(
        tmp_path / "staging",
        entry_point="main.py",
        container_name="rc-test-2",
        network_disabled=False,
    )
    assert "--gpus" not in cmd
    assert "--network" not in cmd


def test_build_run_command_specific_gpus(tmp_path: Path):
    cfg = DockerSandboxConfig(gpu_device_ids=(0, 2))
    sandbox = DockerSandbox(cfg, tmp_path / "work")
    cmd = sandbox._build_run_command(
        tmp_path / "staging",
        entry_point="main.py",
        container_name="rc-test-3",
        network_disabled=True,
    )
    assert "--gpus" in cmd
    gpu_idx = cmd.index("--gpus")
    assert "0,2" in cmd[gpu_idx + 1]


# ── Harness injection ─────────────────────────────────────────────────


def test_harness_injection(tmp_path: Path):
    harness_src = Path(__file__).parent.parent / "researchclaw" / "experiment" / "harness_template.py"
    if not harness_src.exists():
        pytest.skip("harness_template.py not found")

    target = tmp_path / "project"
    target.mkdir()
    DockerSandbox._inject_harness(target)
    assert (target / "experiment_harness.py").exists()


# ── Factory ────────────────────────────────────────────────────────────


def test_factory_returns_experiment_sandbox(tmp_path: Path):
    from researchclaw.experiment.sandbox import ExperimentSandbox

    config = ExperimentConfig(mode="sandbox")
    sandbox = create_sandbox(config, tmp_path / "work")
    assert isinstance(sandbox, ExperimentSandbox)


@patch("researchclaw.experiment.docker_sandbox.DockerSandbox.ensure_image", return_value=True)
@patch("researchclaw.experiment.docker_sandbox.DockerSandbox.check_docker_available", return_value=True)
def test_factory_returns_docker_sandbox(mock_avail, mock_image, tmp_path: Path):
    config = ExperimentConfig(mode="docker")
    sandbox = create_sandbox(config, tmp_path / "work")
    assert isinstance(sandbox, DockerSandbox)


@patch("researchclaw.experiment.docker_sandbox.DockerSandbox.check_docker_available", return_value=False)
def test_factory_raises_when_docker_unavailable(mock_avail, tmp_path: Path):
    config = ExperimentConfig(mode="docker")
    with pytest.raises(RuntimeError, match="Docker daemon"):
        create_sandbox(config, tmp_path / "work")


@patch("researchclaw.experiment.docker_sandbox.DockerSandbox.ensure_image", return_value=False)
@patch("researchclaw.experiment.docker_sandbox.DockerSandbox.check_docker_available", return_value=True)
def test_factory_raises_when_image_missing(mock_avail, mock_image, tmp_path: Path):
    config = ExperimentConfig(mode="docker")
    with pytest.raises(RuntimeError, match="not found locally"):
        create_sandbox(config, tmp_path / "work")


# ── run() with mocked subprocess ──────────────────────────────────────


@patch("subprocess.run")
def test_docker_run_success(mock_run, tmp_path: Path):
    mock_run.return_value = subprocess.CompletedProcess(
        args=["docker", "run"],
        returncode=0,
        stdout="primary_metric: 0.85\n",
        stderr="",
    )
    cfg = DockerSandboxConfig()
    sandbox = DockerSandbox(cfg, tmp_path / "work")
    result = sandbox.run("print('hello')", timeout_sec=60)

    assert result.returncode == 0
    assert result.metrics.get("primary_metric") == 0.85
    assert result.timed_out is False


@patch("subprocess.run")
def test_docker_run_timeout(mock_run, tmp_path: Path):
    mock_run.side_effect = subprocess.TimeoutExpired(cmd="docker run", timeout=10)
    cfg = DockerSandboxConfig()
    sandbox = DockerSandbox(cfg, tmp_path / "work")
    result = sandbox.run("import time; time.sleep(999)", timeout_sec=10)

    assert result.timed_out is True
    assert result.returncode == -1


# ── Dep detection ─────────────────────────────────────────────────────


def test_detect_pip_packages(tmp_path: Path):
    (tmp_path / "main.py").write_text(
        "import torchdiffeq\nimport numpy\nfrom PIL import Image\n"
    )
    detected = DockerSandbox._detect_pip_packages(tmp_path)
    # torchdiffeq is in the base image → skipped, PIL → Pillow
    assert "Pillow" in detected
    # numpy and torchdiffeq should be skipped (builtin)
    assert "numpy" not in detected
    assert "torchdiffeq" not in detected


# ── Static checks (mocked) ────────────────────────────────────────────


@patch("subprocess.run")
def test_check_docker_available_true(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
    assert DockerSandbox.check_docker_available() is True


@patch("subprocess.run")
def test_check_docker_available_false(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1)
    assert DockerSandbox.check_docker_available() is False


@patch("subprocess.run", side_effect=FileNotFoundError)
def test_check_docker_available_no_binary(mock_run):
    assert DockerSandbox.check_docker_available() is False


@patch("subprocess.run")
def test_ensure_image_true(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
    assert DockerSandbox.ensure_image("researchclaw/experiment:latest") is True


@patch("subprocess.run")
def test_ensure_image_false(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1)
    assert DockerSandbox.ensure_image("nonexistent:latest") is False
