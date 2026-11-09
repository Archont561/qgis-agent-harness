
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
## Agent skills

Repository skills live in `.agents/skills/<name>/SKILL.md` and are pinned in `skills-lock.json`.
Read the matching skill before the kind of work it covers — `backlog` (task lifecycle), `bdd` and
`tdd` (tests first), `refactor` and `clean-code-principles` (code changes), `audit` (review),
`skill-creator` (new skills), `writing-for-agents` (agent-facing prose), `playwright-cli` (browser
automation), `typst` (typesetting maths and pages to PDF, LaTeX → typst) and `pptx` (decks, and why
an equation slide can be blank everywhere but PowerPoint). Do not edit a vendored skill in place: change it upstream or via `skill-creator`, then
`pixi run bun x skills update <name>` so `skills-lock.json` records the new hash.

## Quality gates before claiming work is done

Run `pixi run qa` — it chains `alint` (repo structure, 45 rules), `ruff check .`,
`pixi run gherlint` (Gherkin over `experiment/features`) and `pixi run prose` (Vale over `thesis/`
and `docs/`) — all four in the `qa` environment. Beyond that:

- `pixi run test` — pytest + coverage gate that CI applies; a push cannot be greener than the PR.
  It resolves to the `test` environment, which is the only one providing the command.
- `pixi run prose <file>` — Vale on one file, when the gate reports something you did not mean to
  write. Rules that are off, and why, are in `docs/prose.md`; do not silence a rule there to make a
  finding go away, fix the prose (see "Before adding or silencing a rule").
- `pixi run shell <script>` — shellcheck for anything under `scripts/`.
- Rendering goes through `pixi run render <command>` (`.agents/skills/archont561-render`): a
  formula becomes a deck, a document or a picture there, not through a new script in `scripts/`.
- Feature files must keep a `Given` inside every scenario (gherlint C101), even when all scenarios
  share one; the R202 style suggestion is accepted on purpose and filtered in the `gherlint` task.
- `pixi-sandbox` (global CLI, not a project dependency) owns `pixi-sandbox.toml`,
  `scripts/restore.sh` and the two workflows under `.github/workflows/`. Never hand-edit them: change
  config, then `pixi run sandbox-init`, and verify with `pixi run sandbox-check`. Both tasks pass the
  non-default `--script-path scripts/restore.sh`; running the bare CLI would regenerate a root
  `restore.sh` and rewrite the publisher workflow that embeds the launcher path.

## Tests come first: TDD and BDD (mandatory)

**No production code without a failing test that demands it.** This is not a style preference here:
the harness decides correctness of the thesis measurement, so a behaviour that no test demanded is a
behaviour nobody has checked.

### Which one, when

| The change | Discipline | Artefact order |
|---|---|---|
| Anything a user or the exam protocol can observe: CLI output, design matrix, run counts, artefact predicates, exit codes | **BDD** | `.feature` (Gherkin) → failing step definition → implementation |
| Everything internal: parsers, scoring, aggregation, statistics, file layout, invariants | **TDD** | failing unit test → implementation |
| Numeric invariants, tolerances, thresholds (MDE, ICC, run arithmetic) | **TDD + hypothesis** | property test that fails on the current code |

If a change is observable *and* has internals, it needs **both**: the scenario states the promise, the
unit test pins the arithmetic.

### The loop (do not skip step 2)

1. **Red.** Write the smallest test/scenario that fails *for the reason the feature exists*, run it, and
   read the failure. A test that has never been seen failing proves nothing.
2. **Prove it is the right red.** If it fails for an unrelated reason (import error, typo), fix that
   first — otherwise the eventual green is meaningless.
3. **Green.** Write the least code that passes. No speculative parameters, no "while I'm here".
4. **Refactor** with the test green, then re-run `pixi run test`.

Commands to see each state:

```bash
pixi run test -k "design matrix"   # one scenario/test, fast loop
pixi run test                      # full suite + coverage gate (what CI applies)
pixi run gherlint                    # the feature file is linted, not just parsed
```

### Rules that follow from this

- **A feature file without a step definition is not a test.** Every `experiment/features/` must
  be referenced by a module under `experiment/tests/` (`scenarios("../features/<name>.feature")`);
  `alint` enforces this with the `bdd-feature-has-test` rule.
- **New step definitions ship with the scenario that needs them**, in the same commit — never a step
  defined "for later".
- **Commit order is evidence:** a commit that adds `experiment/src/**` without touching
  `experiment/tests/**` is rejected by the `tests-with-src` pre-commit hook. The only escape hatches are
  explicit and visible in the shell history: `LEFTHOOK_EXCLUDE=tests-with-src` (rename, docstring,
  comment-only change) or `git commit --no-verify`.
- **A spike is allowed and then thrown away.** Explore freely, then delete it and redo the change
  test-first; keeping spike code is how untested code enters the harness.
- **Refactoring is a separate commit** with tests untouched and green before and after.
- **Bug fixes start from a test that reproduces the bug** — the failing test is the deliverable, the fix
  is the consequence.
- Coverage is a floor, not a goal: `pixi run test` gates on the number from `experiment/pyproject.toml`,
  but a green suite with an untested branch that decides TSR is still a hole.

## Commits

Conventional Commits, checked by `convco` (`.versionrc`) in the `commit-msg` hook and in CI:
`<type>(<scope>): <description>`, lowercase scope, e.g. `feat(harness): add task card loader`.
Visible types: `feat fix perf revert docs test refactor`; hidden but valid: `build ci chore style`.
Pre-1.0, breaking changes bump `0.(x+1).0`. Do not hand-edit `CHANGELOG.md` if one appears — it is
generated by `pixi run changelog`.
