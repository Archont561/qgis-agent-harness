"""Entry point: ``python -m qgis_agent_harness`` (and ``pixi run harness``).

The app itself lives in :mod:`qgis_agent_harness.cli` so that subcommands can be imported
without importing the entry point.
"""

from __future__ import annotations

from qgis_agent_harness.cli import app, main

__all__ = ["app", "main"]

if __name__ == "__main__":
    app()
