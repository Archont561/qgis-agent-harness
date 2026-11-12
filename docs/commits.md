# Commits, hooks and CI

The workspace is not a git repository yet (`backlog init --no-git`), so `convco`, `lefthook` and
`actionlint` are configured but idle until someone runs `git init`. Everything below is what happens
from that moment on.

**Conventional Commits** are enforced at three points — the `commit-msg` hook, the CI range check, and
`convco changelog` — all reading one config, [`.versionrc`](../.versionrc):

| Type | In changelog | Type | In changelog |
|---|---|---|---|
| `feat` `fix` `perf` `revert` | yes | `build` `ci` `chore` `style` | hidden, still valid |
| `docs` `test` `refactor` | yes | — | — |

`docs` and `test` are *visible* on purpose: thesis prose and the test suite are deliverables here, not
chores. Scopes are lowercase (`.versionrc:scopeRegex`), e.g. `feat(instalacja):`, `docs(thesis):`,
`chore(deps):`. Pre-1.0, a breaking change bumps `0.(x+1).0` (`preMajor: true`).

```bash
pixi run check-commits                  # lint everything since the last tag
pixi run check-commits HEAD~3..HEAD     # lint a range (what CI does)
pixi run convco-check-message <file>    # lint one message file (what the hook does)
pixi run changelog                      # print the unreleased changelog
```

**Hooks** ([`lefthook.yml`](../lefthook.yml)) run everything inside the pixi environment:

| Hook | What runs |
|---|---|
| `commit-msg` | `convco check --from-stdin` (skipped for merge/rebase messages) |
| `pre-commit` | `ruff check --fix` + `ruff format` on staged Python, `actionlint` on staged workflows, `alint` repo-wide, `tests-with-src` guard |
| `pre-push` | `pixi run test` — the same suite + coverage gate CI applies, resolved to the `test` env |

```bash
pixi run hooks      # lefthook install (needs .git)
```

Each command carries a one-line `#` note instead of a paragraph: `lefthook.yml` is held to the same
rule as the manifests (`config-comment-one-line`), so the reasoning behind a hook lives in this
table and in [tests.md](tests.md), not in the YAML.

Coverage gate and the two test workflows are described in [tests.md](tests.md); the sandbox publisher
belongs to [sandbox.md](sandbox.md). A third workflow publishes the MyST site to GitHub Pages on every
push to `main` — and builds it without publishing on every pull request that touches `sites/` — and is
described in [environments.md](environments.md) beside the site it publishes.
