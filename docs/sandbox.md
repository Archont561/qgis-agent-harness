# Offline sandbox

The environment can be packed into a **Git-orphan-branch transport** and restored on a host without
network access. `pixi-sandbox` (v0.9.0) is installed **globally** — it is deliberately *not* a project
dependency, and `init` leaves `pixi.toml` and `pixi.lock` byte-identical:

```bash
pixi global install --channel https://prefix.dev/archont561/archont561 --channel conda-forge pixi-sandbox
pixi run sandbox-init          # writes the four files it owns (launcher in scripts/)
pixi run sandbox-check         # verify they match a fresh render (exit 1 names drift)
pixi run sandbox-plan          # validated publish matrix
pixi-sandbox plan --config pixi-sandbox.toml --json  # the same matrix as a GH Actions object
```

Files owned by the generator (never hand-edit — `init --check` reports drift):

| Path | Role |
|---|---|
| `pixi-sandbox.toml` | reviewed bundle plan: `branch_prefix`, bundles, platforms, budgets |
| `.github/workflows/publish-sandbox.yml` | publisher: install → `pack` → `doctor --verify` → `publish` |
| `.github/workflows/relock.yml` | lockfile-refresh bot for the connected side |
| `scripts/restore.sh` | airlock-side entrypoint (`bash scripts/restore.sh`), no network calls |

Current plan: **1 target** — bundle `developer`, envs `qa` `js`, `linux-64`, runner
`ubuntu-latest`, branch **`sandbox/developer-linux-64`**, `cargo_vendor = false` (no Rust workspace
here — the starter's old default of vendoring would be wrong).

Two environments, not the four this document used to name. `pack` refuses a PyPI entry that the lock
does not record as a wheel, and the harness is a path dependency that `pixi.lock` records as
`pypi: ./experiment`; `experiment` and `test` both carry it, so the instrument stays out of the
transport until it ships as a wheel. `renderers` was never bundled and still is not, and the empty
`default` is not worth a blob.

## What triggers a publish

As generated, the publisher answered `on: push: branches: [main]` with no filter, so every merge to
`main` repacked both environments and force-pushed the transport branch — a README typo cost a full
republish. The `[workflow]` table in `pixi-sandbox.toml` narrows the two generated triggers to the
files the transport is actually built from:

| Field | Renders as | Entries |
|---|---|---|
| `push_paths` | `on.push.paths` in the publisher | `bun.lock`, `experiment/**`, `package.json`, `pixi-sandbox.toml`, `pixi.lock`, `pixi.toml` |
| `relock_paths` | `on.pull_request.paths` in the lock guard | the same manifests and locks, with `experiment/pyproject.toml` instead of the whole tree |

Leaving a field unset derives the same manifests and locks and stops there: the generator cannot see
that the harness is a path dependency, packed into `experiment` and `test` as a wheel built from that
tree, so the publisher has to be told about `experiment/` and the guard about the manifest the solve
reads. A docs-only merge now triggers neither workflow. The Monday schedule and a manual dispatch
still publish whenever a fresh transport is wanted.

Adding the table also switches `setup-pixi`'s `cache:` to `false`, the default the table selects
(ADR-18): a cache keyed on the consumer manifest can restore a solve the publisher's own native
`pixi install` will not reuse. Both workflows stay generated — `pixi run sandbox-init` writes them,
`pixi run sandbox-check` is what proves a hand-applied config change matches a fresh render.

## Restoring on an airlocked host

Carry the project **and** the sandbox branch (`git bundle create project-airlock.bundle main
sandbox/developer-linux-64`), then `bash scripts/restore.sh`, then prove it with
`pixi install --frozen --offline`, which must be a no-op. The launcher finds the project root via
`git rev-parse --show-toplevel`, so living one directory down changes nothing.

**The launcher path is not a default.** `init` defaults to `restore.sh` at the project root, so the
non-default location is passed explicitly on every run — `--script-path scripts/restore.sh` — which is
why the two pixi tasks exist instead of calling the CLI bare. Calling `pixi-sandbox init` without the
flag would regenerate a root `restore.sh` and rewrite `publish-sandbox.yml` (it embeds the launcher
path), and `init --check` would then report drift.

## Three caveats found on this tree

- `shellcheck scripts/restore.sh` reports **SC1087** on the generated line that greps `platforms`
  entries (`$PLATFORM["']` looks like an array index). It is a false positive in generated code; the
  file must stay byte-identical to the template, so the warning is documented rather than patched away.
- `pack` refuses a PyPI dependency that `pixi.lock` does not record as a wheel. The harness is a path
  dependency, so the two environments carrying it — `experiment` and `test` — cannot be packed until
  it is published as a wheel, or until `pixi-sandbox` carries a local path source. The first publish
  of this tree stopped on it: run `42639796286`, red at `Pack, verify, and publish`, with the
  annotation `publish pipeline failed during pack (exit 1)`.
- `pixi run lint` (actionlint) refuses to run because `.github/workflows` is not inside a Git
  repository — it looks for `.git` upwards from the working directory. It becomes usable once the
  project is a Git checkout.
