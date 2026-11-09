# experiment/

Harness for the thesis protocol: **MCP tool exposure vs. code generation for GIS agents**.

```
experiment/
├── pyproject.toml     # package metadata; src/ is mapped onto the `qgis_agent_harness` package
├── src/
│   ├── __init__.py    # __version__ only
│   ├── cli.py         # Typer app: discovers commands/, fills ctx.obj, owns the help text
│   ├── __main__.py    # `from qgis_agent_harness.cli import app` and run — nothing else
│   └── commands/      # placeholder package: one module per subcommand, found automatically
├── tests/             # test_cli.py — behaviour of the app (CliRunner)
├── features/          # empty on purpose (.gitkeep); scenarios come with the first command
└── tasks/             # the canonical card schema: tasks/README.md
```

The analysis probes and their synthetic inputs (`analyse.py`, `power_mde.py`, `simulate_results.py`,
`PIPELINE.md`, `runs.csv`, `simulated_results.json`) were removed on 7 XI 2026: they measured nothing
and pre-dated the instrument. The pipeline stages they assumed are now in
[`thesis/design/runs.md`](../thesis/design/runs.md) and the run register in `TASK-16`.

## Run it

```bash
pixi run harness              # help, with the commands currently registered
pixi run harness -v           # → "commands: (none yet)" (nothing is registered yet)
pixi run test                 # pytest + coverage (16 tests), no QGIS
```

## Adding a command

Drop a module into `experiment/src/commands/`, expose either surface, and it is imported and
registered on the next run — no import list to keep in sync:

```python
# experiment/src/commands/matrix.py
import typer

def show(ctx: typer.Context) -> None:
    """Print the design matrix."""
    typer.echo(ctx.obj.version)

COMMAND = show          # or: app = typer.Typer(...) to add a whole sub-app
```

`experiment/src/cli.py` decides: a module exposing `app: typer.Typer` becomes a sub-app, one exposing
`COMMAND: Callable` becomes a command named after the module. Every command receives
`typer.Context`, and shared state (greeting, version, the list of loaded modules) is in
`ctx.obj` — an `AppContext` instance built by the callback. Modules whose name starts with `_`
are skipped.

`pixi run harness` forwards every argument to `python -m qgis_agent_harness` inside the pixi
environment. The `qgis-agent-harness` console script is the same entry point
(`[project.scripts] qgis-agent-harness = "qgis_agent_harness.__main__:main"`).

## Editing the code

The harness is installed into the pixi env as a **wheel**, not editable — setuptools' editable
finder cannot map a flat `src/` layout (it looks for `src/qgis_agent_harness/__init__.py`, which this
layout deliberately does not have). So after editing anything under `src/`:

```bash
pixi run sync   # = pixi reinstall -e experiment qgis-agent-harness, ~2 s
```

Tests import `src/` directly through `tests/conftest.py`, so they do not need `sync`; the installed
copy is what `pixi run harness` executes.

## What comes next

The contract is `backlog/docs/doc-4` (modules: cards, register, CLI, sandbox, MCP server, code arm,
harness, oracle) plus these tasks: `TASK-15` (card loader), `TASK-16`
(run register), `TASK-17` (`matrix` / `run` / `score`), `TASK-18` (sandbox). Per `AGENTS.md`,
every observable behaviour starts as a `.feature` in `features/` and every internal one as a
failing unit test.
