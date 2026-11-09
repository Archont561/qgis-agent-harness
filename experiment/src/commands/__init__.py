"""Placeholder for harness subcommands — empty on purpose (rebuild starts here).

Drop a module into this directory and ``qgis_agent_harness.cli`` finds it on the next run:

* expose ``app: typer.Typer``      -> registered as a Typer sub-app,
* expose ``COMMAND: Callable``     -> registered as a command named after the module.

Either way the command receives ``typer.Context``; shared state sits in
``ctx.obj`` (``qgis_agent_harness.cli.AppContext``).
"""
