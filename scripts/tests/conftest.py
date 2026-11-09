"""Fixtures for the behavioural tests of the checkers in `scripts/`.

Each test runs a script the way alint runs it — a subprocess, its working directory set to a
throwaway tree, no imports of the script's internals — and asserts on the exit status and the words
it prints. Nothing here knows how a checker is written, only what it promises.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
from typing import Protocol

import pytest

REPO = pathlib.Path(__file__).resolve().parents[2]


class Run(Protocol):
    def __call__(
        self, script: str, *args: str, cwd: pathlib.Path
    ) -> subprocess.CompletedProcess[str]:
        """Run `scripts/<script>` with `args`, rooted at `cwd`."""


class Write(Protocol):
    def __call__(self, root: pathlib.Path, rel: str, text: str) -> pathlib.Path:
        """Write `text` to `root/rel`, creating parents; return the path."""


@pytest.fixture(name="run")
def run_fixture() -> Run:
    def run(script: str, *args: str, cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(REPO / "scripts" / script), *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    return run


@pytest.fixture(name="write")
def write_fixture() -> Write:
    def write(root: pathlib.Path, rel: str, text: str) -> pathlib.Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    return write
