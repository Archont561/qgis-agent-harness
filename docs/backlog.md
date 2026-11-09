# Backlog

Committed work is tracked with Backlog.md (`pixi run backlog …`, config in `backlog/config.yml`,
`filesystem_only: true`). Read `pixi run backlog instructions overview` before touching it, and
**never edit metadata by hand** — `id`, `status`, `labels`, `milestone`, `dependencies`,
`references`, `documentation` and the dates belong to the CLI, which keeps the relationships
consistent. Prose is text and may be edited where it lives: descriptions, acceptance criteria and
implementation notes, which is how the reconciliations of 9 XI 2026 were recorded.

Both halves are checked, so "consistent" is not a promise: `pixi run backlog doctor` for duplicate
ids, cycles and dead links, and `pixi run alint` rule `backlog-records-resolve` for everything a
record points at — id against filename, status and labels against `backlog/config.yml`, milestone and
dependencies against the files, and a Done task that still has an unticked criterion.

| Bucket | Contents |
|---|---|
| `tasks/` 20 | labels: `thesis` (12), `experiment` (8), `literature` (2, on top of `thesis`); milestones `m-0`…`m-5` |
| `backlog/docs/doc-1` | terminology: three layers, correction rule, order of work |
| `backlog/docs/doc-2` | compliance with UMCS rules and the four competitions |
| `backlog/docs/doc-3` | thesis structure: metaplan and IMRAD |
| `backlog/docs/doc-4` | specification of the `experiment/` code: modules, contracts frozen at G1, constraints |
| `backlog/docs/doc-5` | specification of the thesis: six chapters of §V, what sits outside them, editorial traps |
| `backlog/docs/doc-6` | work plan: six stages ↔ milestones, dates that drive everything, ordering rules |
| `backlog/docs/doc-7` | register of working notes: six note categories, three note kinds, bibliographic apparatus |
| `backlog/docs/doc-8` | backlog pruning: cut tests K1–K6, register of what was deliberately not created |
| `decisions/` 1…7 | scope, sample size, domain axis, harness choice, silent error, novelty, knowledge-location |

`doc-4`…`doc-8` are **pointers, not copies**: the text stays in `thesis/`, the backlog holds the
contract. Same rule as decision-7, and the reason `doc-8` exists at all — prose stays in `thesis/`,
raw material (`.bib`, transcripts, JSON dumps) never enters `backlog/`, generated files enter nowhere.

The document that answers "where does this belong, and why is that item *not* here" is
`doc-8`.

## Everyday commands

```bash
pixi run backlog task list                 # the board
pixi run backlog task create '…' -m m-5 --priority High --dep TASK-15 -l experiment \
  --doc thesis/design/runs.md --ac '…'
pixi run backlog task edit TASK-9 --add-doc <path> --remove-doc <path>
pixi run backlog doc update doc-4 --content "$(cat page.md)"
pixi run backlog doctor                    # duplicate IDs, dependency cycles, dead links
pixi run backlog browser                   # web UI on port 6420
```

`task create` takes `-l/--labels` (not `--add-label`); `task edit` takes `--add-doc`, `--remove-doc`,
`--add-label`, `--clear-labels`. `decision create` and `decision edit` accept **title and status
only** — the rationale goes into the title after "bo", and a decision that must be citable in the
thesis belongs in chapter five, not only in the backlog.

## Settings chosen at init

- project name `research`, task prefix `task`, ids not zero-padded
- git integration **off** (`--no-git`: not a git repo), filesystem-only mode, no auto-commit
- `AGENTS.md` written, no shell completions
- web UI auto-open off (headless box); port 6420 when you run `pixi run backlog browser`

## Known failure

If `pixi run backlog` dies with `EACCES … node_modules/backlog.md-linux-x64/backlog`, the binary lost
its exec bit after a snapshot restore: `chmod +x node_modules/backlog.md-linux-x64/backlog` (or
`pixi run install`). Reinstalling the whole tree is unnecessary — `pixi.lock` and `bun.lock` are fine.
