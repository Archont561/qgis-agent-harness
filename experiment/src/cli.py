"""The harness CLI: one Typer app that discovers its subcommands in ``commands/``.

The harness is rebuilt command by command (`TASK-17`: ``matrix`` / ``run`` / ``score``), and a
CLI that lists its own commands cannot drift from the modules that implement them: dropping a
file into ``src/commands/`` is the whole registration step.

A command module is picked up when it exposes either

* ``app: typer.Typer`` — added as a sub-app under the app's name (or the module's), or
* ``COMMAND: Callable`` — added as a single command named after the module.

Every command receives ``typer.Context``; shared state (version, loaded module names) lives in
``ctx.obj`` as an :class:`AppContext`.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

import typer
from qgis_agent_harness import __version__
from qgis_agent_harness import commands as commands_package

HELP = (
    "Harness for the thesis: MCP tool exposure vs. PyQGIS code generation for GIS agents. "
    "Commands are discovered in `experiment/src/commands/` and listed below."
)

EPILOG = (
    "add a command: drop a module into experiment/src/commands/ exposing `app: typer.Typer` "
    "or `COMMAND: Callable`; it is imported and registered on the next run."
)


@dataclass
class AppContext:
    """State shared by every command through ``ctx.obj``."""

    version: str = __version__
    loaded: list[str] = field(default_factory=list)


def discover_commands() -> Iterable[tuple[str, Any]]:
    """Yield ``(name, module)`` for every importable module in ``src/commands``."""
    for info in pkgutil.iter_modules(commands_package.__path__):
        if info.name.startswith("_"):
            continue
        yield info.name, importlib.import_module(f"{commands_package.__name__}.{info.name}")


def register(app: typer.Typer, found: Iterable[tuple[str, Any]]) -> list[str]:
    """Attach every discovered module to ``app``; return the names that were registered."""
    registered: list[str] = []
    for name, module in found:
        sub = getattr(module, "app", None)
        if isinstance(sub, typer.Typer):
            # typer.Typer keeps its declared name in `info.name` (there is no `.name`), and a
            # sub-app may be unnamed — then the module name is the command name.
            app.add_typer(sub, name=getattr(sub.info, "name", None) or name)
            registered.append(name)
            continue
        command = getattr(module, "COMMAND", None)
        if callable(command):
            app.command(name=name)(command)
            registered.append(name)
    return registered


def build_app() -> typer.Typer:
    """Build the app: help text, discovery, and the callback that fills ``ctx.obj``."""
    app = typer.Typer(
        name="qgis-agent-harness",
        help=HELP,
        epilog=EPILOG,
        add_completion=False,
        no_args_is_help=False,
        context_settings={"help_option_names": ["-h", "--help"]},
    )
    loaded = register(app, discover_commands())

    @app.callback(invoke_without_command=True)
    def main_callback(
        ctx: typer.Context,
        verbose: bool = typer.Option(
            False, "--verbose", "-v", help="Show which command modules were discovered."
        ),
    ) -> None:
        """Run a harness command; with no command, print the help."""
        ctx.obj = AppContext(loaded=loaded)
        if verbose:
            typer.echo(f"commands: {', '.join(loaded) or '(none yet)'}")
        if ctx.invoked_subcommand is None:
            typer.echo(ctx.get_help())

    return app


app = build_app()


def main() -> None:
    """Console-script entry point (``[project.scripts] qgis-agent-harness``)."""
    app()


if __name__ == "__main__":
    app()
