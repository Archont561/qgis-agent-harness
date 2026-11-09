#!/usr/bin/env python3
"""Check that the package version is read from `pyproject.toml` and re-exported.

Four promises, in the order a reader asks them:

  1. `experiment/pyproject.toml` declares a static `[project] version`;
  2. `src/__init__.py` assigns a module-level `__version__`, and does not *type* it — a literal is
     a second source of truth, which is exactly the drift this check exists to prevent;
  3. the module names `pyproject.toml`, so a reader can see where the value comes from even on the
     branch that falls back to the installed metadata;
  4. `__all__` lists `__version__`, so the export exists for `import *` and for the package rather
     than only for the metadata.

Usage: python3 scripts/version_export.py [PATH]

`PATH` defaults to `experiment/src/__init__.py`; alint passes `{path}`. Exit 0 when all four
promises hold, 1 with one line per broken one.
"""

from __future__ import annotations

import ast
import pathlib
import sys
import tomllib

ROOT = pathlib.Path.cwd()
DEFAULT_MODULE = "experiment/src/__init__.py"
MANIFEST = "experiment/pyproject.toml"


def _declared_version() -> tuple[str | None, str | None]:
    path = ROOT / MANIFEST
    if not path.is_file():
        return None, f"{MANIFEST}: missing — there is nowhere for the version to come from"
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        return None, f"{MANIFEST}: does not parse ({error})"
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        return None, f"{MANIFEST}: [project] declares no static version"
    return version, None


def _module_problems(rel: str, source: str, tree: ast.Module) -> list[str]:
    problems: list[str] = []
    assigned: dict[str, ast.expr | None] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned[target.id] = node.value

    version_node = assigned.get("__version__")
    if "__version__" not in assigned:
        problems.append(f"{rel}: no module-level __version__ — nothing is exported")
    elif isinstance(version_node, ast.Constant) and isinstance(version_node.value, str):
        problems.append(
            f"{rel}: __version__ = {version_node.value!r} is typed by hand "
            f"— read it from {MANIFEST}"
        )

    exports = assigned.get("__all__")
    names: set[str] = set()
    if isinstance(exports, (ast.List, ast.Tuple, ast.Set)):
        names = {
            element.value
            for element in exports.elts
            if isinstance(element, ast.Constant) and isinstance(element.value, str)
        }
    else:
        problems.append(f"{rel}: __all__ is not a literal list — the export cannot be checked")
    if "__version__" not in names and not any("__all__ is not" in p for p in problems):
        problems.append(f'{rel}: __all__ does not list "__version__" — the version is not exported')

    if "pyproject.toml" not in source:
        problems.append(f"{rel}: does not name {MANIFEST} — say where the version comes from")
    return problems


def main(argv: list[str]) -> int:
    rel = argv[1] if len(argv) > 1 else DEFAULT_MODULE
    problems: list[str] = []

    version, problem = _declared_version()
    if problem:
        problems.append(problem)

    path = ROOT / rel
    if not path.is_file():
        problems.append(f"{rel}: missing")
    else:
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source, filename=rel)
        except SyntaxError as error:
            problems.append(f"{rel}: does not parse ({error})")
        else:
            problems.extend(_module_problems(rel, source, tree))

    for line in problems:
        print(line)
    if problems:
        print(f"{len(problems)} problem(s) in the version export", file=sys.stderr)
    elif version is not None:
        print(f"{rel} exports __version__ = {version!r} from {MANIFEST}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
