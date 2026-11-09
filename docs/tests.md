# Tests

Both disciplines are mandatory; the rule text lives in `AGENTS.md` → *"Tests come first"*. In short:
**observable behaviour starts as a Gherkin scenario in `experiment/features/`, everything internal
starts as a failing unit test**, and no `experiment/src/**` change travels without a test.

| Layer | Artefact | Tooling |
|---|---|---|
| Observable behaviour (CLI output, design matrix, run counts, artefact predicates) | `experiment/features/` + step definitions in `experiment/tests/` | `pytest-bdd`, `gherlint` |
| Internal logic (scoring, aggregation, statistics) | `experiment/tests/test_*.py` | `pytest`, `hypothesis` |
| The checkers in `scripts/` (card schema, counts, retired vocabulary, backlog ids, rule coverage, version export, house markdown style) | `scripts/tests/test_*.py` | `pytest`, each checker run as a subprocess |

Enforcement, so the rule is not merely advisory:

```bash
pixi run alint                     # rule bdd-feature-has-test: every .feature must be wired into a test module
pixi run test -k "design matrix"   # fast red/green loop on one scenario
pixi run test-scripts              # only the checkers' behavioural suite (82 tests)
pixi run test                      # both suites + coverage gate (what CI applies)
```

The `tests-with-src` pre-commit hook rejects a commit that stages `experiment/src/**` without any
`experiment/tests/**` change; the escape hatches are `LEFTHOOK_EXCLUDE=tests-with-src` or
`git commit --no-verify`, both visible in the shell history rather than hidden in config.

## Coverage

Measured by `pixi run test` (`pytest-cov` → `coverage.xml`, gitignored) and gated by
[`codecov.yml`](../codecov.yml) at **90 %** for both the project and any patch — a 960-run sweep
should not merge an untested branch path. Config lives in
[`experiment/pyproject.toml`](../experiment/pyproject.toml) (`[tool.coverage.*]`); tests import
`experiment/src` directly via `experiment/tests/conftest.py`, so the numbers point at source files
rather than at the installed copy in `site-packages`.

```bash
pixi run test              # both suites + coverage table + coverage.xml   (94 %, 16 + 82 tests)
pixi run cov-upload        # codecovcli upload — CI only
```

## The checkers' suite

A checker in `scripts/` is proved the way alint runs it: `pytest` starts
`python scripts/<checker>.py <mode>` as a subprocess, with the working directory set to a throwaway
tree, and asserts on the exit status and the words printed. No test imports a checker, so the tests
survive a rewrite of one and fail when its promise changes — which is also the only way to test a
script whose whole job is to exit non-zero.

| Suite | Checker | Cases |
|---|---|---|
| `test_task_cards.py` (13) | card schema, corpus arithmetic, retired keys | a valid card passes; unknown keys, wrong predicate arity, four checks of one predicate, family/filename mismatches, and a retired key outside the retirement section all fail |
| `test_repo_facts.py` (23) | counts, retired vocabulary, backlog ids, rule coverage, backlog records | a drifted count fails while a dated history row passes; `1 218 runs` fails unmarked and passes marked, under a pruning heading, in a frozen file, or under `backlog/`; a dangling id fails and an archived one needs the word "completed"; a rule that lints nothing, a sleeping rule that woke, and a document no rule covers all fail; a sound task record passes while a dangling dependency, an undeclared label, a missing milestone, a vanished documentation path and a path promised in the body all fail |
| `test_version_export.py` (7) | the version export | a read-and-exported version passes; a typed one, a missing `__all__` entry, a non-literal `__all__`, a module that hides its source, a missing manifest and a missing module all fail |
| `test_terminology.py` (16) | the label vocabulary: conditions, ladder rungs, contributions, currents | a clean document passes; an unknown N label, a rung bound to the wrong condition, a `C7` and an `F7` all fail; a line that names the retirement may quote the old label, so may a row under a pruning heading, a frozen file and a label inside a fence; a missing path exits 2 |
| `test_house_style.py` (23) | house markdown style, in three modes (`invariants`, `skeleton`, `contributing`) | a conforming README passes, with or without front matter; a missing H1, a badge without `alt`, a table header without an alignment row, an untagged or unknown fence, emoji outside a fence, a heading that ends in punctuation, a skipped heading level, a section after `## License`, `## Licence`, a missing skeleton section and out-of-order sections all fail; a plain README passes `invariants` and fails `skeleton`, which is the point of the split |

Fixtures are written per test, so a case states its whole world — a card, a corpus table, a tree of
backlog files — and nothing is inherited from the repository it runs in.

## Workflows

[`ci.yml`](../.github/workflows/ci.yml) lints, tests and uploads coverage on every push — with one
exception, decided by a `scope` job every other test gate reads: when the whole range touches nothing
but prose, `Test, coverage` is **skipped** rather than run. Prose means markdown wherever it stands,
`docs/`, `thesis/`, `backlog/`, `LICENSE` and the Vale config; a file the list does not recognise
counts as code, and so does a range that cannot be read, which is the direction a gate should fail
in. Lint, structure, prose and commit messages always run — they are what a docs change answers for.

[`experiment.yml`](../.github/workflows/experiment.yml) is the runner workflow — plumbing only until
the harness has commands; its stage names come from the pre-registration (`TASK-1`). It already
carries its own `paths:` filter (`experiment/**`), so a docs pull request does not start a sweep
either.

## The sweep host

The series does not run on GitHub's runners: they have no GPU, and `thesis/design/harness.md` §8
froze the host as pinned local weights on a university machine. Actions therefore only *drives* the
sweep, and `experiment.yml` prepares the machine before it asks anything of it:

| Job | What it does |
|---|---|
| `plumbing` | every pull request: cards, matrix and a dry run, no model calls |
| `setup` | every push, schedule and dispatch: is the host provisioned, and provision it if not |
| `cards`, `sweep`, `merge`, `analyse` | the pre-registration gate, the shards, the tidy tables, the statistics |

`setup` sends [`setup.sh`](../.cluster/setup.sh) over ssh and runs it with
`bash -s`, so the copy that provisions the host is the one reviewed in this repository and the host
needs nothing installed first but bash. Its defaults are a configuration block at the top of the
script, each one a `${VAR:-default}` that the environment overrides, because a script arriving on
stdin cannot read a file beside itself. The script has four modes and is safe to re-run:

| Mode | What it does |
|---|---|
| `--probe` | reports cores, memory, disk, GPU and VRAM, and the engine those facts imply |
| `--plan` | prints the steps, resolved against the probe |
| `--check` | compares the host against the configuration at the top of `setup.sh`: `0` ready, `10` nothing provisioned, `11` drifted, `12` a sweep is running, `13` the host lacks something |
| `provision` | pixi, the checkout at a named commit, `pixi install --frozen`, the harness wheel, headless QGIS, the engine, the weights, a health check, and a marker |

The engine is the one decision the script makes from the machine: vLLM when the probe finds a CUDA
GPU at or above `MIN_VRAM_MIB`, Ollama otherwise, because §8 keeps Ollama as the development mirror
and not as a sweep engine. Weights are pinned through `MODEL_ID`/`MODEL_REVISION`, since `run_id` is
derived from `model_digest` and an unpinned model is a sweep whose rows cannot be compared. A host
provisioned without a GPU is marked `cpu_only=1` and refuses to serve a measurement unless
`--allow-cpu` says the run is plumbing only.

Three secrets drive it — `SSH_TARGET` (`user@host`), `SSH_KEY` (ed25519) and `SSH_KNOWN_HOSTS` — and
the job does nothing but report when they are absent. The host key is compared rather than accepted,
and the key file is removed again in a step that runs `if: always()`. To keep a leaked workflow key
from becoming a shell on a machine that is reachable from the internet, install
[`sweep-ctl`](../.cluster/sweep-ctl) on the host and pin it in
`authorized_keys` as `restrict,command="/opt/sweep-ctl"`: it accepts four verbs and two flags and
refuses everything else. Host-specific overrides that should not live in git go next to it as
`environment="MODEL_ID=…"`.

## The harness package

`experiment/src/` is a Typer app whose subcommands live in `experiment/src/commands/`; the import package is `qgis_agent_harness` and the distribution is `qgis-agent-harness`. Layout and the
"drop a module in" rule: [`experiment/README.md`](../experiment/README.md).

```bash
pixi run harness             # help, with the commands currently registered
pixi run harness -v          # which command modules were discovered
pixi run sync                 # rebuild the wheel after editing experiment/src/
```

Layout: `src/cli.py` builds the app and imports whatever sits in `src/commands/`; `src/__main__.py`
only re-exports and runs it. The rebuild adds one module per command (`matrix`, `run`, `score`).

`features/` is empty on purpose (`.gitkeep`): scenarios appear with the first command, and
`pixi run gherlint` is a no-op until then. The commands follow `backlog/docs/doc-4` and
`TASK-15`…`TASK-18`.
