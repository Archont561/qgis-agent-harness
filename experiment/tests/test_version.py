"""The version is declared once, in ``pyproject.toml``, and exported from the package.

The alint rule `version-exported` checks the *shape* of that arrangement statically; these two
assert the arrangement's *result*, which needs the package imported.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import qgis_agent_harness

MANIFEST = Path(__file__).resolve().parents[1] / "pyproject.toml"


def test_version_is_the_declared_one() -> None:
    declared = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))["project"]["version"]
    assert qgis_agent_harness.__version__ == declared


def test_version_is_exported() -> None:
    assert "__version__" in qgis_agent_harness.__all__
