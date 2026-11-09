"""What `scripts/version_export.py` demands of a package that re-exports its version.

The four promises are checked one at a time: a manifest that declares a version, a `__version__`
that is read rather than typed, a module that names where the value comes from, and an `__all__`
that exports it.
"""

from __future__ import annotations

import pathlib

from conftest import Run, Write

MANIFEST = """[project]
name = "experiment"
version = "1.2.3"
"""

MODULE = '''"""Docstring naming pyproject.toml, so the reader knows where the version comes from."""

import pathlib
import tomllib

_MANIFEST = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"


def _read_version() -> str:
    with _MANIFEST.open("rb") as manifest:
        return tomllib.load(manifest)["project"]["version"]


__version__ = _read_version()

__all__ = ["__version__"]
'''


def _package(
    write: Write, root: pathlib.Path, module: str = MODULE, manifest: str | None = MANIFEST
) -> pathlib.Path:
    if manifest is not None:
        write(root, "experiment/pyproject.toml", manifest)
    write(root, "experiment/src/__init__.py", module)
    return root


def test_a_read_and_exported_version_passes(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    root = _package(write, tmp_path)
    done = run("version_export.py", cwd=root)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "exports __version__ = '1.2.3'" in done.stdout


def test_a_typed_version_is_refused(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    module = MODULE.replace("__version__ = _read_version()", '__version__ = "1.2.3"')
    root = _package(write, tmp_path, module=module)
    done = run("version_export.py", cwd=root)
    assert done.returncode == 1
    assert "is typed by hand" in done.stdout


def test_a_version_missing_from_all_is_refused(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    module = MODULE.replace('__all__ = ["__version__"]', "__all__ = []")
    root = _package(write, tmp_path, module=module)
    done = run("version_export.py", cwd=root)
    assert done.returncode == 1
    assert "the version is not exported" in done.stdout


def test_all_must_be_a_literal_to_be_checkable(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    module = MODULE.replace('__all__ = ["__version__"]', "__all__ = list()")
    root = _package(write, tmp_path, module=module)
    done = run("version_export.py", cwd=root)
    assert done.returncode == 1
    assert "the export cannot be checked" in done.stdout


def test_a_module_that_hides_its_source_is_refused(
    run: Run, write: Write, tmp_path: pathlib.Path
) -> None:
    module = MODULE.replace("pyproject.toml", "the manifest")
    root = _package(write, tmp_path, module=module)
    done = run("version_export.py", cwd=root)
    assert done.returncode == 1
    assert "does not name experiment/pyproject.toml" in done.stdout


def test_a_missing_manifest_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    root = _package(write, tmp_path, manifest=None)
    done = run("version_export.py", cwd=root)
    assert done.returncode == 1
    assert "there is nowhere for the version to come from" in done.stdout


def test_a_missing_module_is_reported(run: Run, write: Write, tmp_path: pathlib.Path) -> None:
    write(tmp_path, "experiment/pyproject.toml", MANIFEST)
    done = run("version_export.py", cwd=tmp_path)
    assert done.returncode == 1
    assert "experiment/src/__init__.py: missing" in done.stdout
