
<!-- BACKLOG.MD GUIDELINES START -->
<!-- backlog.md-instructions-version: 1.55.3 -->
<CRITICAL_INSTRUCTION>

## Backlog.md Workflow

This project uses Backlog.md for task and project management.

**At the beginning of each conversation in this project, run `backlog instructions overview` before answering or taking action. Re-read it only if you have not read it yet in the current conversation.**

Use the overview to decide whether to search, read, create, or update Backlog tasks.

Before task lifecycle actions, read the matching detailed guide:
- `backlog instructions task-creation` before creating or splitting tasks
- `backlog instructions task-execution` before planning, changing status or assignee, adding a plan or implementation notes, or implementing task work
- `backlog instructions task-finalization` before checking acceptance criteria, writing final summaries, or moving tasks to terminal statuses

Use `backlog <command> --help` before running unfamiliar commands. Help shows options, fields, and examples.

Do not edit Backlog task, draft, document, decision, or milestone markdown files directly. Use the `backlog` CLI so metadata, relationships, and history stay consistent.

</CRITICAL_INSTRUCTION>
<!-- BACKLOG.MD GUIDELINES END -->

# AGENTS.md

> Guidance for AI coding agents working in this repo. Read this first.
> **Before building, changing, or debugging anything: verify live state** (read the actual code,
> config, and deployed branch). Do not act on stale assumptions.

<!-- agents-md:begin id=overview -->
## Overview

One MSc thesis and the instrument that measures it, in one repository: a harness that runs one
pinned model over the same GIS tasks twice — once with the operations exposed as MCP tools, once as
generated PyQGIS code — and scores both with spatial predicates rather than with a judging model.
The comparison is pre-registered, so no number produced by `experiment/` counts until the measures
are frozen.

| Where | What |
|---|---|
| `thesis/` | the text: framing, design, analysis, the six chapters, the bibliography |
| `experiment/` | the instrument: a Typer app in `src/`, its tests, its Gherkin `features/` |
| `backlog/` | the only place work is tracked — tasks, documents, decisions, milestones |
| `scripts/`, `.cluster/` | the checkers alint runs, and the scripts that provision the sweep host |
| `docs/` | how this repository works: environments, tests, sandbox, commits, agents |

Two runtimes, one entry point each: `pixi run <task>` for everything Python (features in
`pixi.toml`, locked in `pixi.lock`, restorable offline from the sandbox branch) and bun for the JS
tooling (`package.json`, `bun.lock`). A second toolchain is how a container and CI drift apart, so
the only two things that are not `pixi run` are the two generators: `readme-md-generator` and
`agents-md`, both reached through tasks.

Nothing here is published: no package, no release, no version.
<!-- agents-md:end id=overview -->

<!-- agents-md:begin id=commands -->
## Commands

Start every session with these two, in this order:

```bash
bash scripts/restore.sh     # the locked pixi environments, unpacked from the sandbox branch
pixi run hooks              # lefthook: commit-msg, pre-commit and pre-push
```

`restore.sh` reads `pixi-sandbox.toml`, unpacks the transport branch into `.pixi`, and leaves the
prefixes exactly as `pixi.lock` describes them. It is safe to repeat, and a host that already
carries the branch needs no network. Until lefthook is installed a commit skips `convco`, `ruff`,
`alint`, the `tests-with-src` guard and Vale, and a push skips the suite — the failure then arrives
from CI, later and further from the change. Without a `qa` environment yet,
`cp scripts/pre-push.sh .git/hooks/pre-push` is the same push gate.

| Command | Purpose |
|---|---|
| `pixi run qa` | every linter: `alint` (repo structure, 47 rules), `ruff check .`, `pixi run gherlint`, `pixi run prose` |
| `pixi run test` | pytest over the harness, the checkers and the sweep host, with the coverage gate CI applies |
| `pixi run test -k "<words>"` | one scenario or test, for the red-green loop |
| `pixi run prose <file>` | Vale on one file, when the gate reports something you did not mean to write |
| `pixi run shell <script>` | shellcheck for anything under `scripts/` |
| `pixi run render <command>` | maths and decks through the `archont561-render` skill, never a new script |
| `pixi run gherlint` | the feature files are linted, not just parsed |
| `pixi run sandbox-init` / `sandbox-check` | regenerate, or verify, the pixi-sandbox owned files |
| `pixi run bun x backlog task list` | the committed work |
| `pixi run readme` / `readme-check` | render `README.md` from `.readme/README.md.ejs`, or prove it is that render |
| `pixi run agents-md` | regenerate the marked sections of this file (see Notes) |
| `tox -e py312` | the suites on one interpreter: 3.12 (pinned), 3.13, 3.14 |

Every command resolves to the environment that owns it; `pixi run -e qa test` is an error that says
where the task does live. `pixi-sandbox` is a global CLI, not a project dependency.
<!-- agents-md:end id=commands -->

<!-- agents-md:begin id=testing -->
## Testing

**No production code without a failing test that demands it.** This is not a style preference: the
harness decides correctness of the thesis measurement, so a behaviour no test demanded is a
behaviour nobody checked.

| The change | Discipline | Artefact order |
|---|---|---|
| Anything a user or the exam protocol can observe: CLI output, design matrix, run counts, artefact predicates, exit codes | **BDD** | `.feature` (Gherkin) → failing step definition → implementation |
| Everything internal: parsers, scoring, aggregation, statistics, file layout, invariants | **TDD** | failing unit test → implementation |
| Numeric invariants, tolerances, thresholds (MDE, ICC, run arithmetic) | **TDD + hypothesis** | property test that fails on the current code |

A change that is observable *and* has internals needs both: the scenario states the promise, the
unit test pins the arithmetic.

The loop, and step 2 is the one that gets skipped:

1. **Red.** Write the smallest test that fails *for the reason the feature exists*, run it, read the
   failure. A test never seen failing proves nothing.
2. **Prove it is the right red.** A failure for an unrelated reason (import error, typo) is fixed
   first — otherwise the eventual green is meaningless.
3. **Green.** The least code that passes. No speculative parameters, no "while I'm here".
4. **Refactor** with the tests green, then re-run `pixi run test`.

Rules that follow:

- **A feature file without a step definition is not a test.** Every `experiment/features/` and
  `.cluster/features/` file must be referenced by a module under `experiment/tests/` or
  `.cluster/tests/`; `alint` enforces it with `bdd-feature-has-test`.
- **New step definitions ship with the scenario that needs them**, in the same commit.
- **Commit order is evidence:** a commit touching `experiment/src/**` without `experiment/tests/**`
  is rejected by the `tests-with-src` pre-commit hook. The escapes are visible in the shell history:
  `LEFTHOOK_EXCLUDE=tests-with-src` or `git commit --no-verify`.
- **A spike is allowed and then thrown away.** Keeping spike code is how untested code enters the
  harness.
- **Refactoring is a separate commit**, tests untouched and green before and after.
- **A bug fix starts from the test that reproduces the bug**: the failing test is the deliverable.
- Coverage is a floor, not a goal. A green suite with an untested branch that decides TSR is still a
  hole.
- **Interpreter coverage is `tox`, not pixi.** `tox.ini` runs the same suites on 3.12, 3.13 and 3.14
  without QGIS, which is a conda package; a missing interpreter fails rather than skips.
<!-- agents-md:end id=testing -->

<!-- agents-md:begin id=structure -->
## Project structure

```text
thesis/        the text: framing, design, analysis, draft chapters; index in thesis/README.md
experiment/    the instrument: src/ (package qgis_agent_harness), tests/, features/
backlog/       tasks, documents, decisions, milestones — managed by the backlog CLI
docs/          how the repository works (environments, tests, sandbox, commits, agents, backlog)
site/          the documentation site's pages; myst.yml at the root, text pulled from thesis/
scripts/       restore.sh, pre-push.sh, readme.sh and the checkers alint runs
.cluster/      the sweep host: setup.sh, sweep-ctl, their tests and their Gherkin features
.agents/       vendored agent skills, pinned by skills-lock.json
.readme/       README.md.ejs — the source README.md is rendered from
.github/       workflows and the pixi-sandbox owned ones
```

`experiment/src/` is a Typer app whose subcommands live in `src/commands/`; the import package is
`qgis_agent_harness` and the distribution is `qgis-agent-harness`. The layout is flat on purpose,
which is why the wheel is built from the tree and installed as a copy rather than editable.
<!-- agents-md:end id=structure -->

<!-- agents-md:begin id=conventions -->
## Code style & conventions

- **Python:** `ruff` (check and format, 100 columns). Type hints everywhere; `from __future__ import
  annotations` at the top of a module that needs it. Docstrings say what a module promises, not what
  a line does.
- **Pins are arguments, not habits.** `pytest-bdd==8.1.0` with `pytest 8` because 8.1.0 reads
  `FixtureManager._arg2fixturedefs`, which pytest 9 removes. Python is 3.12 in pixi because QGIS
  3.44 is a 3.12 build. A pin without its reason in a comment is a puzzle for the next person.
- **Markdown:** `scripts/house_style.py` over `README.md`, `docs/**` and `CONTRIBUTING.md` — one H1
  on line 1, no emoji, no skipped heading levels, tagged fences, `alt` on every badge, an alignment
  row under every table header, `## License` last.
- **Generated files are not edited.** `scripts/restore.sh`, `pixi-sandbox.toml`, the two
  pixi-sandbox workflows, `README.md`, the Backlog.md block at the top of this file, and everything
  inside `agents-md` markers: change the source, then run the task that renders it.
- **Gherkin:** a `Given` inside every scenario (gherlint C101) even when all scenarios share one;
  the R202 style suggestion is accepted on purpose and filtered in the `gherlint` task.
- **Prose:** no contractions, British punctuation, em dashes spaced on both sides, dense sentences.
  Rules that are off, and why, are in `docs/prose.md`; do not silence a rule to make a finding go
  away.
<!-- agents-md:end id=conventions -->

<!-- agents-md:begin id=git -->
## Git & PR workflow

Default branch `main`. Work happens on a branch; the branch is proposed as a pull request, and the
pull request is what CI answers.

Conventional Commits, checked by `convco` (`.versionrc`) in the `commit-msg` hook and in CI:
`<type>(<scope>): <description>`, lowercase scope, e.g. `feat(harness): add task card loader`.
Visible types: `feat fix perf revert docs test refactor`; hidden but valid: `build ci chore style`.
Pre-1.0, a breaking change bumps `0.(x+1).0`. `CHANGELOG.md`, when one appears, is generated by
`pixi run changelog` and is not hand-edited.

| CI job | What it insists on |
|---|---|
| `Scope of the change` | decides whether the range is prose only, which gates the suites |
| `Lint, lint-check, structure` | alint, ruff, actionlint, Vale |
| `Test, coverage` | the suites under pixi, with the coverage gate |
| `Python 3.12 / 3.13 / 3.14` | the same suites under tox, without QGIS |
| `Conventional commits` | every commit in the range |
| `lock guard` | `pixi.lock` still satisfies the manifests (with `relock` repairing it) |

A push cannot be greener than the pull request: `scripts/pre-push.sh` runs the suite before the push
and refuses with the remedy when neither pixi nor pytest is available.
<!-- agents-md:end id=git -->

<!-- agents-md:begin id=gotchas -->
## Gotchas & hard-won lessons

- **`pixi-sandbox` owns more than it looks like it owns.** It writes `pixi-sandbox.toml`,
  `scripts/restore.sh`, `.github/workflows/relock.yml` and `.github/workflows/publish-sandbox.yml`.
  Always pass `--script-path scripts/restore.sh`: the bare CLI regenerates a root `restore.sh` and
  rewrites the publisher workflow that embeds the launcher path.
- **A `package.json` or `pixi.toml` edit republishes the sandbox** — both are in `push_paths`, so
  the transport branch is repacked. That is why adding `repository` and `license` to `package.json`
  was not free.
- **`readme-md-generator` swallows its own git fallback.** Without a `repository` entry in
  `package.json` it hands a Buffer to a String method, throws inside its own `try`, and every URL
  renders empty. The `repository` field is the fix, not decoration.
- **`agents-md` rewrites what is inside its markers.** Anything written there by hand is replaced by
  what the tool detects, which for this repository is a stub for most sections.
- **A second `conftest.py` in another test tree shadows the first** — pytest imports both as the
  module `conftest`. `.cluster/tests` keeps none for that reason.
- **Backticks inside a single-quoted `echo` in a workflow `run:` block** are SC2016 to shellcheck,
  which actionlint runs over every `run:` body. A backtick in a workflow is a CI failure.
- **QGIS is headless here:** `QT_QPA_PLATFORM=offscreen`, set in the devcontainer, is what keeps a
  PyQGIS import from blocking on a display.
- **The sweep host has never been provisioned for real.** The `setup` job runs only on `main`, on a
  dispatch or on a schedule; `--probe` is the first thing it prints, so the first run on the box is
  what answers how much GPU there is.
<!-- agents-md:end id=gotchas -->

<!-- agents-md:begin id=security -->
## Security & secrets

No secret is in the tree, and `.env*` is ignored on purpose. The sweep host is reached with three
GitHub secrets — `SSH_TARGET`, `SSH_KEY` (ed25519) and `SSH_KNOWN_HOSTS` — and the job that uses
them writes the key to `$HOME/.ssh/id_ed25519`, compares the host key rather than accepting it, and
removes the key again in a step that runs `if: always()`. On the host,
`restrict,command="/opt/sweep-ctl"` in `authorized_keys` is what turns a leaked workflow key from a
shell into a menu of four verbs.

`CODECOV_TOKEN` is the fourth secret. Never print a secret's value in a log, a step summary or an
artefact — a summary is public on a public repository.
<!-- agents-md:end id=security -->

<!-- agents-md:begin id=boundaries -->
## Boundaries

- ✅ **Always**: restore the environments first; read the matching skill before that kind of work;
  write the failing test before the code; run `pixi run qa` and `pixi run test` before claiming
  done; keep commits conventional.
- ⚠️ **Ask first**: adding or moving a dependency in `pixi.toml` or `package.json` (both move a
  lock and republish the sandbox); changing the design matrix, the corpus or a pre-registered
  measure; moving a directory; force-pushing a branch; starting a real sweep against the host;
  re-running `pixi run agents-md` without a review of the diff.
- 🚫 **Never**: commit a key, a token or a real host name; edit `backlog/` files by hand instead of
  through the backlog CLI; edit a vendored skill in place; hand-edit a generated file; force-push
  `main`; commit `.pixi/`, `node_modules/` or `.tox/`.
<!-- agents-md:end id=boundaries -->

## Notes

<!-- Human-owned. Anything here is never touched by re-runs of agents-md. -->

Two blocks in this file are generated, and by different tools: the Backlog.md guidelines at the
very top (the `backlog` CLI, version 1.55.3) and the nine sections inside `agents-md:begin`/`end`
markers (`pixi run agents-md`). **Re-running that task regenerates everything inside the markers,
including content written by hand there** — the tool reads the repository, and what it cannot detect
(a pixi workspace, for one) it replaces with a stub. Review the diff of a refresh the way you would
review any other generated change: what is outside the markers, including this section, is never
touched.

---
<!-- Generated and maintained by agents-md (https://github.com/eugeniughelbur/agents-md).
     Content INSIDE agents-md:begin/end markers is regenerated on re-run.
     Everything OUTSIDE the markers (including ## Notes) is yours and is preserved. -->
