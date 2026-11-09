# Prose

`vale` lints the writing the way `ruff` lints the Python: over `thesis/` and `docs/`, against one
base style (Microsoft, committed under `.vale/styles/`), with every disagreement between that style
and the way these documents are actually written recorded in `.vale.ini` next to its reason.

```bash
pixi run prose                      # the whole prose tree — what `pixi run qa` and CI run
pixi run vale docs/prose.md         # exactly the files you name …
pixi run vale --output=JSON thesis  # … with any other vale flag (JSON, --minAlertLevel, --glob)
pixi run prose-sync                 # move to a newer rule set; review and commit the diff
```

**Only errors fail.** Vale exits non-zero on error-level findings and on nothing else, so the
suggestions below report without blocking a commit, a push, or CI.

## What counts as prose

| Path | Linted | Why |
|---|---|---|
| `thesis/{framing,design,writing,draft,analysis}/**`, `thesis/README.md` | **yes** | the live thesis text: notes, drafts, registers of what was decided |
| `thesis/competitions/` | **yes** | our own assessment of the rulebooks |
| `thesis/competitions/` | no | faithful conversions of the rulebooks — quoted § numbering, not our sentences |
| `thesis/literature/**` | no | machine-extracted transcripts and raw API dumps (the same trees `.alint.yml` ignores) |
| `thesis/` | no | the two Polish registers — English rules on Polish prose produce noise only, and Vale cannot read the frontmatter to find that out |
| `docs/**`, `README.md`, `AGENTS.md`, `experiment/**/*.md` | **yes** | prose that binds a person or an agent |
| `backlog/` | no | written through the Backlog.md CLI |
| `.agents/skills/` | no | vendored, pinned by `skills-lock.json` |
| `*.py`, `*.feature` | n/a | `ruff` and `gherlint` own those |

An exclusion is an empty `BasedOnStyles =` section in `.vale.ini`: Vale still walks the file when a
whole directory is passed, and matches no style, so it says nothing. The exclusions live in the
config rather than in the task's argument list so that a hand-run `pixi run vale thesis/` skips the
same files the gate does.

## One base style, and the rules switched off

Microsoft is the base because it is the only maintained package that reads like a style guide rather
than a spell-checker. It is also written for product documentation, so a fair number of its rules
argue with a thesis. Every rule switched off in `.vale.ini` is off for a reason that would survive
someone disagreeing — never because the finding was inconvenient to fix.

| Rules | Level | Why they are off |
|---|---|---|
| `Contractions`, `Passive`, `We`, `FirstPerson` | — | academic register: no contractions, methods reported in the passive, argument carried by "we" |
| `Dashes`, `Quotes` | — | spaced em dashes and logical (British) punctuation are the house style |
| `Semicolon` | — | clauses are joined in one breath, and a §-reference mid-sentence makes splitting it worse; the rule's only advice is "simplify", 1 143 times |
| `HeadingColons`, `HeadingPunctuation` | — | the colon says what a document answers and the question mark says it is a question |
| `Foreign` | — | `e.g.` and `i.e.` are scholarly Latin, not slang |
| `DateFormat`, `DateOrder` | — | dates are day-month-year (`7 November 2026`, `7 XI 2026`) |
| `SentenceLength` | — | 30 words is a product-doc threshold; 681 findings would not all be improvements |
| `Adverbs` | — | every `-ly` word is a finding, including to `only` and `explicitly` |
| `QuestionMarks` | — | the documents are question-driven: one question per file, restated in the heading |
| `Acronyms`, `HeadingAcronyms`, `Uppercase` | — | MCP, GIS, OGC API, GRASS GIS are the subject matter, defined once in `thesis/glossary-of-terms.md` |
| `Vocab`, `Terms` | — | Microsoft's A–Z list prefers "personal digital assistant" over "agent" |
| `Hyphens` | — | all 13 findings were compound labels (`family-C`, `locally-valid`), not hyphenable word pairs |
| `Accessibility` | — | "disabled" here names a control state, not a person |
| `Headings`, `Auto`, `Militaristic` | — | sentences are already sentence-case, `auto-commit` is the step's name, and "blast radius" is sharper than the suggested "impact" |
| `Avoid` | **warning**, not off | its word list bans `backend`, which is the term of art for one of this repo's layers |

`Microsoft.OxfordComma`, `Microsoft.Wordiness`, `Microsoft.Jargon`, `Microsoft.UIVerbs`,
`Microsoft.Suspended` and `Microsoft.GeneralURL` stay as they are.

Current state, `pixi run prose`: **82 findings, 0 errors** — 59 `OxfordComma`, 13 `Wordiness`, 4
`Avoid` (warning), 6 across `Jargon`, `UIVerbs`, `Suspended` and `GeneralURL`. The Oxford-comma
backlog is a real inconsistency, not a rule debating the register: the tree already writes the
serial comma 594 times, so those 59 are the places where it was not noticed. They do not fail the
gate, and fixing them is a separate pass over the thesis, not a by-product of setting this up.

## Before adding or silencing a rule

Run it on the tree first and read what it matched (`pixi run vale --output=JSON thesis/` keeps the
matched string). A rule earns a line in the table above only if every finding it produced was wrong
for these documents; a rule that is merely inconvenient stays on and gets the prose fixed.

## Frontmatter is not prose

Vale lints YAML frontmatter as prose: each top-level string becomes its own block, scoped
`text.frontmatter.<key>`, and **that pass honours nothing but `IgnoredScopes`** — `BlockIgnores` and
`TokenIgnores`, the two workarounds every blog post suggests, never reach it. Bare `frontmatter` in
`IgnoredScopes` drops the whole header. Our frontmatter is metadata, checked by `.alint.yml`'s
schema rule, and its `question:` field is a question on purpose. `tt, code, kbd` are repeated beside
it because setting `IgnoredScopes` replaces Vale's own default for inline HTML.

## Rules are committed, not synced

`.vale/styles/Microsoft/` (48 files, 193 KB) is versioned. Vale's advice is the opposite — gitignore
the styles and let `vale sync` rebuild them — but this repository has to lint prose in an airlocked
sandbox (`scripts/restore.sh` restores environments, not the network), and a gate that cannot run
offline is not a gate. `pixi run prose-sync` re-downloads the package when you want a newer rule
set; the diff it leaves is the review, and `Packages = Microsoft` in `.vale.ini` is the source of
truth for where it came from.

## What is still worth adding

**Spelling.** `Vale.Spelling` with a `Vocab` is the one check that would catch a typo no rule above
sees, and it is off because it needs a curated accept list: with no vocabulary it produces about
19 000 findings on this tree — technical nouns to the last one (QGIS, WMS, Mann-Whitney, OMML …). The way
in is `thesis/glossary-of-terms.md`, which already holds the vocabulary that has to be spelled the
same way twice; seed `styles/config/vocabularies/Thesis/accept.txt` from it, add
`Vocab = Thesis` and `Vale.Spelling = YES` to `.vale.ini`, and judge the remainder by hand instead
of accepting whatever the first run prints.

**House terms.** A small custom style under `.vale/styles/Thesis/` (say `Thesis/Terms.yml`) is where
a rule that is genuinely ours belongs — "the harness", not "the tool"; "task", not "prompt" — if the
glossary ever settles enough to be machine-checkable.

## Labels: one letter, one meaning

Prose rules govern words; labels are the shorthand a reader meets in a table and has to resolve without
help. Three families of them once shared the letter N — the enforcement ladder, the ranked contributions
and the currents of chapter 1 — so the same two characters could mean a rung, a contribution or a
current, sometimes in one paragraph. The collision was renamed away: the families are disjoint, and
`scripts/terminology.py` holds the line as the alint rule `terminology-labels`.

| Family | Labels | What they name | Owner |
|---|---|---|---|
| conditions | **K · N1 · N4** | the three arms: code, catalogue at the schema, catalogue with invariants and contract | `design/arms-and-validation.md` §3.1 |
| ladder rungs | **L0–L5** | enforcement depth inside one surface; only `L1 / N1` and `L4 / N4` carry a condition | `design/correctness.md` §5 |
| contributions | **C1–C6** | the ranked contributions, by durability | `framing/aim-and-contributions.md` §6 |
| currents | **F1–F6** | the six field currents the thesis positions itself inside | `framing/scope-and-character.md` §6.1 |
| hypotheses | **H1–H3** | the confirmatory claims; `D1–D4` are descriptive, `W1–W6` the interpretations of an outcome | `analysis/statistics.md` §5 |
| failure classes | **E1–E8** | coordinate-system error classes; `B1–B7` are the gates that could catch them | `design/correctness.md` §1, §7 |
| sub-questions | **SQ1–SQ5** | the research questions, kept numbered so they cannot be read as a second hypothesis list | `framing/gap-and-literature.md` §6 |
| gaps | **G1–G5** | the literature gaps, one of them marked closed | `framing/gap-and-literature.md` §3 |
| rules of interpretation | **R1–R3** | the decision rules fixed before the sweep | `thesis/design/runs.md` |

The checker enforces the three that collided. It allows a quoted old label on a line that names the
retirement, under a heading that does, or in a file whose front matter freezes it — which is how the
pruning records keep the history without keeping the ambiguity.

## Where it runs

```bash
pixi run qa              # alint + ruff + gherlint + prose — the whole toolchain, in the qa env
pixi run prose           # this linter alone; same environment, since vale is a qa dependency
```

- **Lefthook**, `pre-commit`: `pixi run vale {staged_files}` on staged `*.md`. Errors block a commit;
  suggestions do not. `vale`, `ruff` and `alint` are all in `qa`, so the hook runs in one environment
  from the first command to the last.
- **CI**, `.github/workflows/ci.yml`, job `Lint`: `pixi run prose` beside `ruff` and `alint` in the
  `qa` environment — the same env the hook uses, so a finding cannot appear in one and not the other.
  No network needed beyond the environment itself: the rules are committed.
