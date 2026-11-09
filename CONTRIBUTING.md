# Contributing to qgis-agent-harness

The harness that scores GIS-agent artefacts: one QGIS runtime, nine geoprocessing operations, three
ways of exposing them, one oracle. This page is the short way in. The binding rules — tests before
code, one pixi environment per concern, conventional commits — are in [AGENTS.md](AGENTS.md), and
the work itself is tracked in `backlog/` through the Backlog.md CLI.

## Environment

Everything runs inside a pixi environment; nothing goes into a system Python. Two commands open a
session, and the second needs the first:

```bash
bash scripts/restore.sh   # the locked environments, unpacked from the sandbox branch
pixi run hooks            # lefthook: commit-msg, pre-commit and pre-push
```

Six environments, one per concern ([docs/environments.md](docs/environments.md)): `qa` holds every
linter, `test` runs the suites, `experiment` carries QGIS, `js` carries bun, `renderers` carries
manim and typst, and `default` is empty on purpose. QGIS is never needed to lint or to test. Where
lefthook cannot be installed yet, `cp scripts/pre-push.sh .git/hooks/pre-push` gives you the push
gate on its own.

## Commands

| Command | Purpose |
|---|---|
| `bash scripts/restore.sh` | unpack the locked environments; offline once the sandbox branch is fetched |
| `pixi run hooks` | install the git hooks, so the gates run here rather than in CI |
| `pixi run qa` | alint, ruff, gherlint and Vale — everything that reads repo text |
| `pixi run test` | both suites and the coverage gate, exactly as CI runs them |
| `pixi run harness --help` | the instrument; commands are discovered in `experiment/src/commands/` |
| `pixi run backlog task list` | the work; task files are never edited by hand |
| `pixi run sandbox-plan` | the publish matrix the offline transport is built from |

## Commits

Conventional Commits, checked by `convco` in the `commit-msg` hook, in CI, and by
`pixi run changelog`: `<type>(<scope>): <description>`, lowercase scope, as in
`feat(harness): add task card loader`. Visible types are `feat`, `fix`, `perf`, `revert`, `docs`,
`test` and `refactor`; `build`, `ci`, `chore` and `style` are valid and stay out of the changelog.
The whole ladder, with the reasoning, is in [docs/commits.md](docs/commits.md).

Tests come first. A commit that adds `experiment/src/` without `experiment/tests/` is refused by the
`tests-with-src` hook, and a push that has not run the suite is refused by `scripts/pre-push.sh`. A
feature file that no test module references is documentation, not a test — `alint` says so too.
