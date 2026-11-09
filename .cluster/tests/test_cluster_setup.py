"""What `.cluster/setup.sh` promises about a host it has never seen.

The script is a shell entry point, so it runs under `bash` rather than the `run` fixture, with a
PATH whose `nvidia-smi` is a stub: the promise under test is the *decision* the script makes from
what it finds — which engine, how many workers, and whether the host matches `host.env` — not the
installs themselves, which need a real GPU and a real network.

Exit codes pinned here are part of the contract the workflow branches on: 0 ready, 10 nothing
provisioned, 11 drifted, 12 a sweep is running, 13 the host is missing something.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
from typing import Protocol

import pytest

REPO = pathlib.Path(__file__).resolve().parents[2]
SETUP = REPO / ".cluster" / "setup.sh"


class Write(Protocol):
    def __call__(self, root: pathlib.Path, rel: str, text: str) -> pathlib.Path:
        """Write `text` to `root/rel`, creating parents; return the path."""


@pytest.fixture(name="write")
def write_fixture() -> Write:
    """Local on purpose: a second `conftest.py` in another test tree shadows this one under the
    module name `conftest`, so a tree whose tests need nothing shared keeps none."""

    def write(root: pathlib.Path, rel: str, text: str) -> pathlib.Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    return write


# A bare `command -v` probe: every verb needs these two present before it does anything else.
STUBS = {
    "git": "#!/bin/sh\nexit 0\n",
    "curl": "#!/bin/sh\nexit 0\n",
}


def _bin(
    root: pathlib.Path, vram_mib: int | None, extra: dict[str, str] | None = None
) -> pathlib.Path:
    """A PATH directory holding stubs; `vram_mib=None` means a host with no NVIDIA driver."""
    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    for name, body in {**STUBS, **(extra or {})}.items():
        path = bin_dir / name
        path.write_text(body, encoding="utf-8")
        path.chmod(0o755)
    if vram_mib is None:
        (bin_dir / "nvidia-smi").unlink(missing_ok=True)
    else:
        gpu = bin_dir / "nvidia-smi"
        gpu.write_text(
            f'#!/bin/sh\ncase "$*" in\n*name*) echo "Stub GPU {vram_mib}MiB" ;;\n'
            f"*) echo {vram_mib} ;;\nesac\n",
            encoding="utf-8",
        )
        gpu.chmod(0o755)
    return bin_dir


def _env(root: pathlib.Path, vram_mib: int | None, **overrides: str) -> dict[str, str]:
    bin_dir = _bin(root, vram_mib)
    env = {
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "HOME": str(root / "home"),
        "HOST_DIR": str(root / "home" / "research"),
        "SWEEP_HOME": str(root / "home" / "state"),
        **overrides,
    }
    (root / "home").mkdir(parents=True, exist_ok=True)
    return env


def _setup(env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SETUP), *args],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _fact(out: str, key: str) -> str:
    for line in out.splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1]
    raise AssertionError(f"{key} missing in:\n{out}")


def test_probe_reports_a_gpu_less_host_as_cpu_only(tmp_path: pathlib.Path) -> None:
    # A host without a driver is a plumbing box: Ollama runs there, a measurement may not.
    result = _setup(_env(tmp_path, None), "--probe")
    assert result.returncode == 0, result.stderr
    assert _fact(result.stdout, "cpu_only") == "1"
    assert _fact(result.stdout, "vram_mib") == "0"
    assert _fact(result.stdout, "engine") == "ollama"


def test_probe_picks_vllm_and_shards_by_vram(tmp_path: pathlib.Path) -> None:
    # 24 GiB is the design's floor for serving the series; one shard per 12 GB, capped at four.
    result = _setup(_env(tmp_path, 24576), "--probe")
    assert result.returncode == 0, result.stderr
    assert _fact(result.stdout, "engine") == "vllm"
    assert _fact(result.stdout, "workers") == "2"
    assert _fact(result.stdout, "cpu_only") == "0"


def test_probe_caps_workers_at_four(tmp_path: pathlib.Path) -> None:
    result = _setup(_env(tmp_path, 98304), "--probe")
    assert _fact(result.stdout, "workers") == "4"


def test_plan_names_the_engine_and_the_frozen_install(tmp_path: pathlib.Path) -> None:
    result = _setup(_env(tmp_path, 24576, MODEL_ID="qwen3-8b"), "--plan")
    assert result.returncode == 0, result.stderr
    assert "pixi install --frozen -e experiment" in result.stdout
    assert "vllm" in result.stdout
    assert "qwen3-8b" in result.stdout


def test_plan_says_so_when_no_model_is_pinned(tmp_path: pathlib.Path) -> None:
    # An unpinned model cannot produce comparable run ids, so the plan has to say it out loud.
    result = _setup(_env(tmp_path, None), "--plan")
    assert "cannot measure" in result.stdout


def test_check_reports_nothing_provisioned(tmp_path: pathlib.Path) -> None:
    result = _setup(_env(tmp_path, None), "--check")
    assert result.returncode == 10
    assert "nothing provisioned" in result.stderr


def test_check_accepts_a_matching_host(tmp_path: pathlib.Path, write: Write) -> None:
    env = _env(tmp_path, None)
    write(
        tmp_path,
        "home/state/provisioned.env",
        "\n".join(
            [
                "schema=1",
                f"host_dir={env['HOST_DIR']}",
                "pixi_version=0.81.0",
                "experiment_env=experiment",
                "engine=ollama",
                "engine_version=",
                "model=",
                "model_revision=",
                "quantization=",
                "engine_host=127.0.0.1",
                "engine_port=8000",
            ]
        ),
    )
    result = _setup(env, "--check")
    assert result.returncode == 0, result.stderr


def test_check_refuses_to_reconfigure_under_a_live_sweep(
    tmp_path: pathlib.Path, write: Write
) -> None:
    # The sweep writes its own lock; provisioning underneath it would pull the server out from under
    # running runs.
    env = _env(tmp_path, None)
    write(tmp_path, "home/research/runs/.sweep/sweep-id", "20260101T0000Z-abc1234\n")
    write(tmp_path, "home/state/provisioned.env", "schema=1\n")
    result = _setup(env, "--check")
    assert result.returncode == 12
    assert "a sweep is running" in result.stderr


def test_check_reports_drift(tmp_path: pathlib.Path) -> None:
    env = _env(tmp_path, None)
    (pathlib.Path(env["SWEEP_HOME"])).mkdir(parents=True, exist_ok=True)
    (pathlib.Path(env["SWEEP_HOME"]) / "provisioned.env").write_text(
        "schema=1\npixi_version=0.0.1\n", encoding="utf-8"
    )
    result = _setup(env, "--check")
    assert result.returncode == 11
    assert "drifted" in result.stderr


def test_provision_refuses_a_gpu_less_host_unless_forced(tmp_path: pathlib.Path) -> None:
    # The series on CPU would take months; the refusal is what stops somebody trying it by accident.
    env = _env(tmp_path, None)
    refused = _setup(env, "provision")
    assert refused.returncode == 13
    assert "no GPU found" in refused.stderr
    # --allow-cpu is the deliberate way past it, for plumbing only.
    assert "no GPU found" not in _setup(env, "provision", "--allow-cpu").stderr


def test_usage_rejects_an_unknown_flag(tmp_path: pathlib.Path) -> None:
    result = _setup(_env(tmp_path, None), "--nonsense")
    assert result.returncode == 64
    assert "unknown argument" in result.stderr


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__]))
