"""Experiment harness: MCP tool exposure vs. code generation for GIS agents.

Package layout note: this directory *is* the ``qgis_agent_harness`` package (see the
``package-dir`` mapping in ``../pyproject.toml``), so ``python -m qgis_agent_harness``
resolves to ``src/__main__.py``.

The version is written once, in ``../pyproject.toml``, and re-exported here so that
``qgis_agent_harness.__version__`` cannot drift from the version pip and pixi record. The
installed copy is a plain copy of ``src/`` and carries no manifest, so it falls back to the
distribution metadata — which setuptools generated from that same file.
"""

from __future__ import annotations

import pathlib
import tomllib
from importlib.metadata import version as _distribution_version

_MANIFEST = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"


def _read_version() -> str:
    """``[project] version`` from the manifest next door, or the metadata of the installed copy."""
    if _MANIFEST.is_file():
        with _MANIFEST.open("rb") as manifest:
            return tomllib.load(manifest)["project"]["version"]
    return _distribution_version("qgis-agent-harness")


__version__ = _read_version()

__all__ = ["__version__"]
