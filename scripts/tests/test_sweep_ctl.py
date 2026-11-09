"""What `scripts/cluster/sweep-ctl` promises to a host that is reachable from the internet.

`restrict,command="/opt/sweep-ctl"` in `authorized_keys` decides which *program* an ssh key runs; it
says nothing about what that program is told, because the client still controls
`$SSH_ORIGINAL_COMMAND` in full. So the wrapper's promise is the security boundary: four verbs, two
flags, and a refusal for everything else — including `rm -rf /` and a `--sha` that is not a commit.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[2]
SWEEP_CTL = REPO / "scripts" / "cluster" / "sweep-ctl"
SETUP = REPO / "scripts" / "cluster" / "setup.sh"


def _ctl(tmp_path: pathlib.Path, request: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SWEEP_CTL)],
        env={
            "PATH": os.environ["PATH"],
            "HOME": str(tmp_path / "home"),
            "HOST_DIR": str(tmp_path / "home" / "research"),
            "SWEEP_HOME": str(tmp_path / "home" / "state"),
            # Pointing at the repository copy stands in for the /opt fallback a virgin host needs,
            # before there is a checkout to take the script from.
            "SWEEP_CTL_FALLBACK": str(SETUP),
            "SSH_ORIGINAL_COMMAND": request,
        },
        capture_output=True,
        text=True,
        check=False,
    )


def test_an_allowlisted_verb_reaches_the_provisioner(tmp_path: pathlib.Path) -> None:
    # exit 10 is setup.sh's "nothing provisioned": the wrapper ran it, so the plumbing works.
    result = _ctl(tmp_path, "check")
    assert result.returncode == 10
    assert "nothing provisioned" in result.stderr


def test_probe_and_plan_reach_it_too(tmp_path: pathlib.Path) -> None:
    assert _ctl(tmp_path, "probe").returncode == 0
    assert _ctl(tmp_path, "plan").returncode == 0


def test_a_verb_that_is_not_on_the_menu_is_refused(tmp_path: pathlib.Path) -> None:
    result = _ctl(tmp_path, "rm -rf /")
    assert result.returncode == 64
    assert "unknown verb" in result.stderr
    assert "probe" in result.stderr  # the menu, so the caller knows what is allowed


def test_a_sha_that_is_not_a_commit_is_refused(tmp_path: pathlib.Path) -> None:
    # A path or a `; curl …` would arrive in the same place and be rejected the same way.
    for sha in ("nope", "../../etc/passwd", "$(id)", "abc; rm -rf /"):
        result = _ctl(tmp_path, f"setup --sha {sha}")
        assert result.returncode == 64
        assert "--sha needs a commit sha" in result.stderr


def test_an_unlisted_flag_is_refused(tmp_path: pathlib.Path) -> None:
    result = _ctl(tmp_path, "setup --engine vllm")
    assert result.returncode == 64
    assert "not allowed" in result.stderr


def test_no_request_at_all_is_refused(tmp_path: pathlib.Path) -> None:
    result = _ctl(tmp_path, "")
    assert result.returncode == 64
    assert "no command" in result.stderr


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__]))
