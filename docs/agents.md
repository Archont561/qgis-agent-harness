# Agent skills and runtime notes

Reusable agent skills live in `.agents/skills/` (vendored, plain files — no `node_modules`), and
every one is pinned in `skills-lock.json` (schema `version: 1`: `source`, `sourceType`, `skillPath`,
`computedHash`). Both are tracked by git on purpose: the skills shape how agents work in this repo,
so they are reviewable like code and reproducible like a lockfile.

Nine skills, copied from the author's own repositories and checked in:

| Skill | Source | Used for |
|---|---|---|
| `backlog` | `Archont561/qgis-sdk` | creating/splitting/closing tasks through the Backlog.md CLI |
| `bdd` | `Archont561/universe` | Gherkin features → pytest-bdd scenarios |
| `tdd` | `Archont561/qgis-sdk` | red-green-refactor for `experiment/` |
| `refactor` | `Archont561/qgis-sdk` | behaviour-preserving refactors |
| `clean-code-principles` | `Archont561/qgis-sdk` | SOLID/DRY review ruleset |
| `audit` | `Archont561/qgis-sdk` | evidence-based code-quality audits |
| `skill-creator` | `Archont561/qgis-sdk` | authoring/revising further skills |
| `writing-for-agents` | `Archont561/universe` | prose for agent-facing docs |
| `playwright-cli` | `Archont561/bun-test-utils` | driving a real browser from the CLI |

Deliberately **not** copied: `qgis-sdk`, `arena`, `session`, `odm-packaging`, `release-review`,
`cep-channel`, `regain-direction`, `arena-agent` — they are bound to their own repository's
workflow (QGIS-SDK package layout, Arena sandbox conventions, conda/Photoshop packaging) and would
be misleading here.

```bash
pixi run bun x skills list          # what is installed, and where each one came from
pixi run bun x skills add Archont561/<repo> -l        # list what a repo offers
pixi run bun x skills add Archont561/<repo> -s <name> -a universal --copy -y
```

`computedHash` is sha256 over the skill directory's files — each file's relative path followed by
its bytes, files ordered with `localeCompare` — which is what `skills` computes on install, so the
pin can be re-derived, not just trusted.

**Recovery is `git`, not the registry.** `.agents/skills/` is committed, so a fresh clone already
has the files; `skills-lock.json` records provenance + integrity. `skills experimental_install`
restores only a skill that its pinned repo exposes *as its own* — several of these are themselves
vendored into `Archont561/*` from other repositories (`backlog`, `refactor`, `tdd` and
`skill-creator` come from a private `Archont561/qgis-rust`, `clean-code-principles` from
`AsyrafHussin/agent-skills`, `playwright-cli` from `microsoft/playwright-cli`, …), and the CLI
correctly declines to attribute them to the middle repo. Verified: of the nine, only `audit`
re-installs from `Archont561/qgis-sdk`; the other eight report "No matching skills found". Re-vendor
those from their upstream source by hand if they ever need updating.

## AGENTS.md is generated in zones

`AGENTS.md` is written by hand and refreshed by
[agents-md](https://github.com/eugeniughelbur/agents-md) (npm), which owns only what sits between
its markers:

```bash
pixi run agents-md-check        # what a refresh would change, without writing it
pixi run agents-md              # rewrite the nine marked sections
```

| Zone | Owner |
|---|---|
| Backlog.md guidelines, at the top of the file | the `backlog` CLI, v1.55.3 |
| the nine `agents-md:begin` / `end` sections | `pixi run agents-md` |
| `## Notes`, and anything else outside the markers | us — neither tool touches it |

**A refresh replaces everything inside the markers**, including prose written there by hand. The tool
reads the repository and leaves a `_TBD_` stub for what it cannot detect, which here is most of it:
it sees `package.json` and reports "stack: node", when the Python is pixi's and the JS is bun's. So
the marked sections are filled deliberately, and the diff of a refresh is reviewed the way any
generated change is. The `## Notes` section says so in the file itself, because it is the part that
survives.

`--no-symlink` is deliberate: the tool also offers to point `CLAUDE.md` at `AGENTS.md`, and that is a
second file to keep in step for a tool nobody here has asked for yet.

## Runtime notes

**bun** — comes from the `js` feature of `pixi.toml` (v1.4.x), reached as `pixi run bun …`; the
sandbox's global Node 20 is *not* on the script path. Verified: `pixi run bun install` resolved all
deps, `pixi run bun run backlog --version` → 1.55.3.

**`skills` needs bun's runtime (or Node ≥ 22.20.0).** The package imports `glob` from `fs/promises`,
which Node only exposes from v22.20; this box has Node 20.20.2, so `npx skills` and `bunx skills`
both fail — the bin shim's shebang sends it to Node either way. Bun 1.4.4 implements that export, so
the `skills` script in `package.json` calls the CLI directly on bun:

```bash
bun run skills --help          # works → resolves to `bunx --bun skills`
```

`backlog.md` runs fine on either runtime.

**Nothing outside the workspace persists.** `node_modules`, the global bun install and the npm cache
all live outside the snapshot, so a later session needs `sudo npm i -g bun` (or
`curl -fsSL https://bun.sh/install | bash`) plus `bun install` again. `package.json` + `bun.lock` are
what persist.
