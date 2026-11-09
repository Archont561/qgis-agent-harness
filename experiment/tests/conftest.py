"""Point ``import qgis_agent_harness`` at ``src/`` instead of the installed copy.

The harness is installed as a *copy* (pixi path dependency; a flat ``src/`` layout
cannot be installed editable), so without this shim the tests would exercise
``site-packages/qgis_agent_harness`` and coverage would report 0 % against the real source
files. Loading ``src/__init__.py`` under the name ``qgis_agent_harness`` — with ``src`` as its
search path — makes ``qgis_agent_harness.__main__`` resolve there too, which also means
``pixi run test`` no longer needs ``pixi run sync`` first.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"

if "qgis_agent_harness" not in sys.modules and (SRC / "__init__.py").is_file():
    spec = importlib.util.spec_from_file_location(
        "qgis_agent_harness",
        SRC / "__init__.py",
        submodule_search_locations=[str(SRC)],
    )
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["qgis_agent_harness"] = module
        spec.loader.exec_module(module)
