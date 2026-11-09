"""Behaviour of the harness CLI: help, command discovery, context."""

from __future__ import annotations

import types

import pytest
import typer
from qgis_agent_harness import cli
from qgis_agent_harness.cli import AppContext, build_app
from typer.testing import CliRunner

runner = CliRunner()


# ── baseline behaviour ────────────────────────────────────────────────────────


def test_no_arguments_prints_help():
    result = runner.invoke(cli.app, [])
    assert result.exit_code == 0
    assert "Usage" in result.stdout
    assert "Commands" in result.stdout


def test_help_is_available_and_documents_discovery():
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    assert "experiment/src/commands" in result.stdout
    assert cli.EPILOG.split(";")[0][:30] in result.stdout


def test_short_help_flag_works_too():
    assert runner.invoke(cli.app, ["-h"]).exit_code == 0


def test_unknown_command_fails():
    assert runner.invoke(cli.app, ["nonsense"]).exit_code != 0


def test_entry_point_reexports_the_app():
    from qgis_agent_harness import __main__

    assert __main__.app is cli.app
    assert callable(__main__.main)


# ── discovery ─────────────────────────────────────────────────────────────────


def _module(name: str, **attributes) -> types.ModuleType:
    module = types.ModuleType(name)
    for key, value in attributes.items():
        setattr(module, key, value)
    return module


def test_commands_package_is_empty_on_purpose():
    assert list(cli.discover_commands()) == []


def test_discovered_command_function_is_registered(monkeypatch):
    def greet(ctx: typer.Context, name: str = "world") -> None:
        """Say hi to one name."""
        typer.echo(f"{ctx.obj.version}: {name}")

    discovered = [("greet", _module("greet", COMMAND=greet))]
    monkeypatch.setattr(cli, "discover_commands", lambda: discovered)
    result = runner.invoke(build_app(), ["greet", "--name", "Ada"])
    assert result.exit_code == 0
    assert result.stdout.strip() == f"{cli.__version__}: Ada"


def test_discovered_sub_app_is_registered(monkeypatch):
    sub = typer.Typer(name="matrix", help="Print the design matrix.")

    @sub.command("show")
    def show(ctx: typer.Context) -> None:
        """Show a placeholder matrix."""
        typer.echo(f"matrix placeholder ({ctx.obj.version})")

    discovered = [("matrix", _module("matrix", app=sub))]
    monkeypatch.setattr(cli, "discover_commands", lambda: discovered)
    result = runner.invoke(build_app(), ["matrix", "show"])
    assert result.exit_code == 0
    assert result.stdout.startswith("matrix placeholder")


def test_context_carries_the_loaded_module_names(monkeypatch):
    def dump(ctx: typer.Context) -> None:
        """Dump the context."""
        assert isinstance(ctx.obj, AppContext)
        typer.echo(",".join(ctx.obj.loaded))

    discovered = [("dump", _module("dump", COMMAND=dump))]
    monkeypatch.setattr(cli, "discover_commands", lambda: discovered)
    result = runner.invoke(build_app(), ["dump"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "dump"


def test_verbose_lists_the_discovered_modules(monkeypatch):
    monkeypatch.setattr(cli, "discover_commands", lambda: [])
    result = runner.invoke(build_app(), ["--verbose"])
    assert result.exit_code == 0
    assert "commands: (none yet)" in result.stdout


def test_modules_without_a_registration_surface_are_skipped(monkeypatch):
    monkeypatch.setattr(cli, "discover_commands", lambda: [("noop", _module("noop"))])
    app = build_app()
    assert runner.invoke(app, ["noop"]).exit_code != 0
    assert "Usage" in runner.invoke(app, []).stdout


def test_private_modules_are_not_discovered(tmp_path, monkeypatch):
    (tmp_path / "_hidden.py").write_text("COMMAND = None\n", encoding="utf-8")
    (tmp_path / "visible.py").write_text("x = 1\n", encoding="utf-8")
    monkeypatch.setattr(cli.commands_package, "__path__", [str(tmp_path)], raising=False)
    assert [name for name, _ in cli.discover_commands()] == ["visible"]


@pytest.mark.parametrize("flag", ["-v", "--verbose"])
def test_verbose_flags_are_equivalent(flag):
    assert runner.invoke(cli.app, [flag]).exit_code == 0
