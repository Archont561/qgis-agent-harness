# Environments

`pixi.toml` declares every dependency once, inside a **feature**; **environments** then pick
features. One environment per feature, and **every command is bound to exactly one environment** —
`pixi run test` runs in `test`, `pixi run prose` in `prose`, and neither needs `-e`.

| Env | Features | Provides | Size |
|---|---|---|---|
| `experiment` | `py` `geo` `harness` `experiment` | QGIS 3.44.14, geopandas, scipy, matplotlib, pingouin, the harness CLI | 3.5 GB |
| `test` | `py` `harness` `test` | Python 3.12, pytest/pytest-bdd/hypothesis/pytest-cov, the harness, codecov-cli — **no QGIS** | 258 MB |
| `qa` | `py` `qa` | ruff, actionlint, shellcheck, alint, gherlint, convco, lefthook, vale — **the whole linter and formatter toolchain, in one env** | 332 MB |
| `js` | `js` | bun 1.4.2 **only** — no node, no Python | 120 MB |
| `renderers` | `py` `renderers` | manim 0.22.1, typst 0.15.1, pandoc 3.13, easypptx 0.11.0, pypdfium2 5.15.1 | 1.3 GB |
| `default` | — | nothing, on purpose | 164 KB |

The `default` environment is empty. pixi always has one, so instead of letting it accumulate features
(which is how the old 3.8 GB `default` happened) it holds nothing: a bare `pixi run <command>` goes
straight to the single environment that owns the command. `pixi install -a` builds everything;
`pixi install` alone builds the empty `default`, which is a no-op on purpose.

Nothing is installed twice for convenience. What keeps commands single-owner is that the features
holding **no** commands may be shared:

| Feature | Dependencies | Why it may appear in several envs |
|---|---|---|
| `py` | `python 3.12` | declared once, so no two envs can drift to different interpreters |
| `harness` | `experiment` (path dependency) + `typer` + `pyyaml` | the tests import it and the experiment runs it — a library, not a command; the card loader parses YAML, so the parser ships with the library |
| `geo` | `qgis 3.44.*`, `geopandas`, `scipy`, `matplotlib`, `pingouin` | the measurement needs QGIS; only one env measures |
| `qa` | `ruff`, `actionlint`, `shellcheck`, `alint` + `gherlint` (pypi), `convco`, `lefthook`, `vale`, `pyyaml` | one env — every linter, formatter and hook of the repo |
| `test` | `pytest`, `pytest-bdd`, `hypothesis`, `pytest-cov` + `codecov-cli` (pypi) | one env |
| `experiment` | **no dependency at all** — only the `experiment` and `sync` commands | a command feature, so exactly one env |
| `js` | `bun 1.4.*` | one env |
| `renderers` | `manim 0.22.*`, `typst 0.15.*`, `pandoc 3.*` + `easypptx`, `pypdfium2` (pypi) | one env |

`experiment` holds commands and nothing else because the harness *package* lives in `harness`: the
`test` env needs the package to import without inheriting the commands, and if both features were one
the `experiment` command would exist in two environments — which is exactly the ambiguity the split
is for. `sync` therefore names its environment (`pixi reinstall -e experiment experiment`): a rebuild
builds a wheel for one env, and "whichever env is implicit" is how you rebuild the wrong one.

Solve groups: `experiment` and `test` share one, so the harness is the same wheel in the env that
runs it and the env that tests it — a green test has to be a statement about the code that measures.
`qa`, `prose` and `js` share another, and `renderers` keeps its own so numpy 2.x never reaches the
QGIS solve.

QGIS is pinned to **3.44.x** (resolved 3.44.14-Solothurn) to match the thesis protocol; conda-forge
also ships 4.2.3 if you ever want it. `alint` and `gherlint` are not on conda-forge, so they come
from pypi (`[feature.qa.pypi-dependencies]`).

**No dependency is a bare `*`.** Twelve of them used to be, and a `*` is not a version: it asks the
next solve to pick whatever conda-forge published that morning, so two machines can disagree while
both manifests are byte-identical. Each now names the version the lock already held, in `==` form:
`geopandas 1.2.0`, `scipy 1.18.1`, `matplotlib 3.11.2`, `codecov-cli 11.3.2`, `pytest-bdd 8.1.0`,
`hypothesis 6.170.15`, `actionlint 1.7.12`, `shellcheck 0.11.0`, `lefthook 2.2.2`, `ruff 0.17.4`,
`pyyaml 6.0.3`, `pypdfium2 5.15.1`. The pin changes how an upgrade happens, not whether one can:
`pixi update` will not move a package past its `==`, so a bump is an edit to `pixi.toml` followed by
`pixi lock` — deliberate, reviewable, and visible in the diff.

What stays a range stays a range on purpose: `python 3.12.*`, `qgis 3.44.*`, `pytest 8.*` (pytest-bdd
8.1.0 reads a fixture-manager attribute pytest 9 removed), `pytest-cov 7.*`, `convco 0.7.*`,
`bun 1.4.*`, `manim 0.22.*`, `typst 0.15.*`, `pandoc 3.*`, and the compatibility windows
`vale >=3.26,<4`, `gherlint >=0.5,<0.6`, `typer >=0.12,<1`, `pingouin >=0.7,<0.8`,
`easypptx >=0.11,<1`, `latex2mathml >=3.81.1,<4`, `mathml2omml >=0.0.2,<0.0.3`. Those windows say
something a single version cannot — that the code is written against an API rather than a build.

**What the binding does not promise.** Dependencies still travel transitively: `qa` carries pytest
9.0.3 because a pypi dependency of `alint` pulls it in, and no rule about features prevents that. The
guarantee is about *commands* — the `test` task exists in `test` and nowhere else — which is the part
that decides whether `pixi run test` is a statement about the runtime you meant.

**Where the envs live:** `~/.cache/rattler/cache/envs` (symlinked from `.pixi/envs`), because
detached environments are switched on in pixi's own global configuration. Nothing heavy lands in this
repo; `pixi install -a` builds them all from `pixi.lock` — seconds for `prose` and `js` on a warm
cache, a couple of minutes for `experiment`, whose 3.5 GB is QGIS and its geospatial stack.

## qa — lint, structure, hooks

```bash
pixi run qa                          # alint + ruff (tree + our skill) + gherlint + prose, all in this env
pixi run lint-py                     # ruff check .
pixi run fmt                         # ruff format .
pixi run ruff check path/to/file.py  # ruff passthrough
pixi run lint                        # actionlint
pixi run shell path/to/script.sh     # shellcheck
pixi run alint                       # repo-structure linter (.alint.yml)
pixi run gherlint                    # Gherkin lint (feature files), fails on unaccepted findings
pixi run gherlint-stats              # Gherkin metrics (scenarios, steps, tags)
pixi run prose                       # prose lint (Vale) over thesis/ and docs/ — docs/prose.md
pixi run vale docs/prose.md          # vale passthrough: exactly the files you name
pixi run prose-sync                  # re-download the style package in .vale.ini (rarely)
pixi run hooks                       # lefthook install
```

Everything that reads or rewrites the repository's text lives here — the code linters, the prose
linter, the commit-message linter and the hook runner — so `pixi run qa` is one command in one
environment, and a `pre-commit` hook never switches envs between `ruff` and `vale`.

Two dependencies are not obviously linters and are here anyway, each with its reason:

- `pyyaml` is for `.alint.yml`, whose `thesis-frontmatter` rule runs `python3 -c "import yaml"`.
- `codecov-cli` is *not* here: `cov-upload` is a task of the `test` env, so the uploader lives with
  the tests. A task and its binary always share a feature, which is what keeps the binding true.

## experiment — the measurement

```bash
pixi run harness --help                                # the harness CLI
pixi run harness matrix                                # design matrix, run arithmetic
pixi run sync                                          # rebuild the harness wheel after editing src/
pixi run -e experiment python -c "import qgis.core; print(qgis.core.Qgis.QGIS_VERSION)"
pixi run -e experiment qgis_process --version          # headless QGIS, no display needed
```

The `experiment` and `sync` commands resolve here without `-e`; raw binaries inside the environment
(`python`, `qgis_process`) do need it, because there is no `default` environment to fall back on.

## test — pytest, no GIS

```bash
pixi run test                              # both pytest suites + coverage + coverage.xml
pixi run test-scripts                      # only the checkers in scripts/ (behavioural)
pixi run test -k "design matrix"           # one scenario
pixi run cov-upload                        # codecovcli upload — CI only
```

`test` is the measurement environment minus QGIS: same harness wheel (one solve group), 243 MB, which
is what CI's test job and the `pre-push` hook use.

## js, renderers

```bash
pixi run bun install           # bun 1.4.2; also `pixi run backlog task list`, `pixi run skills`
pixi run manim -ql scene.py Scene
pixi run typst compile figure.typ figure.pdf
```

## Asking for a specific environment

`-e` is only needed when you want a *different* environment than the one the command belongs to, or
for a raw binary. Where a command exists in one environment, asking for another is an error that says
where it does live:

```console
$ pixi run -e qa test
Error:   × the task 'test' is not available in environment 'qa'
  help: The task is defined in environment(s): test.

        Run it there with:

        	pixi run --environment test test
```

## Linting

| Tool | Scope | Config |
|---|---|---|
| `ruff` 0.17.4 | Python lint + format | `ruff.toml` |
| `actionlint` | GitHub Actions workflows | `actionlint.yaml` if you add one |
| `shellcheck` | shell scripts | none |
| `alint` 0.21.2 | repo structure, naming, file content | `.alint.yml` |
| `gherlint` 0.5.0 | Gherkin feature files (`experiment/features`) | `gherlint.toml` |
| `vale` 3.26.0 | prose in `thesis/` and `docs/` — [docs/prose.md](prose.md) | `.vale.ini` |
| `lefthook` | git hooks | `lefthook.yml` |

`.alint.yml` extends three bundled rulesets (`oss-baseline`, `python`, `node`), ignores generated
trees (`node_modules`, `.pixi`, `thesis/literature/fulltexts`, `thesis/literature/search`,
`backlog`) and switches off the four OSS-governance rules that do not fit a solo thesis —
SECURITY.md, CODEOWNERS, a code of conduct and a dependency-update bot — plus `.nvmrc`, because bun
is the runtime here and pinning a Node version would be a second one. The licence is real: the
workspace is MIT, `oss-license-exists` is left on, and `experiment/pyproject.toml` says so too.
Current state: **46 rules pass, 0 violations**.

Eighteen rules are configured here rather than inherited, and they are the ones a bundled ruleset
cannot know on its own:

| Rule | Enforces |
|---|---|
| `bdd-feature-has-test` | every `.feature` is pulled in by a module under `experiment/tests` — an unwired feature is documentation, not a test |
| `thesis-frontmatter` | the `id`/`title`/`type`/`status`/`language` schema, and that `id` equals the path |
| `gherlint-config-exists`, `vale-config-exists` | the config that makes `pixi run gherlint` and `pixi run prose` mean anything |
| `sandbox-config-exists` | the reviewed bundle plan and the launcher survive |
| `task-card-schema-docs` | every ```yaml card example in `experiment/tasks/README.md` and `thesis/design/corpus.md` parses against the canonical schema — keys, enums, predicates, negative control |
| `task-card-schema-cards` | the same parser over `experiment/tasks/cards/` (no cards yet: the rule wakes up with `TASK-15`) — unknown keys are errors, `id` must match the filename |
| `task-card-numbers` | the card/repetition/run arithmetic and the retired-generation keys: `80 × 4 × 3 = 960` must hold, and `min_surface`-era keys may appear only in the section that retires them |
| `config-comment-one-line` | a comment in `pixi.toml`, `experiment/pyproject.toml`, `gherlint.toml` or `lefthook.yml` is one line: no stacked `#` blocks, so a remark either survives compression or moves into these docs |
| `markdown-links-resolve` | a relative Markdown link points at a file that exists — its first run found one wrong relative path and four links into the two trees `ignore:` hides (`backlog/`, `.agents/skills/`), which became inline code, because a link the linter cannot see behind `ignore:` is a link nobody checks |
| `markdown-paths-resolve` | a backticked path with a prefix in `thesis/`, `docs/`, `experiment/` or `scripts/` resolves — its first run reported 30: paths left behind by the move to `experiment/src/`, backlog ids that read as repository paths, globs and brace expansions, and references into the trees `ignore:` hides |
| `markdown-fragments-resolve` | a `#fragment` in a local link names a heading in its target |
| `repo-counts` | a number the index documents quote about this tree (`20 tasks`, `69 references`, `39 rules`, `8 directories`) is the number the filesystem holds — scripts/repo_facts.py re-counts |
| `repo-retired-values` | `1 218 runs`, `mcp-5`, `H4a`, `TOST`, `min_surface`, `T00n` may appear only in a sentence that marks them as retired, or under such a heading; the registers in `backlog/`, `thesis/writing/` and frozen files are exempt |
| `repo-backlog-ids` | every `TASK-n`, `d-n`, `doc-n`, `m-n` in prose names a file in `backlog/` or `backlog/archive/` — and an id that only resolves in the archive must be called completed on its line |
| `backlog-records-resolve` | every task record holds together: `id` matches its filename, `status` and `labels` are the ones `backlog/config.yml` declares, `milestone` names a file, `dependencies` name tasks (here or in the archive), `references`/`documentation` and any repository path the body promises resolve, and a task marked Done has no unticked acceptance criterion |
| `version-exported` | `experiment/src/__init__.py` reads its version from `experiment/pyproject.toml`, names that file, and exports `__version__` through `__all__` — a literal version is a second source of truth, and the rule refuses one |
| `repo-rule-coverage` | no rule selects an empty file set: a rule whose `paths` match nothing passes silently, so it must first be declared sleeping, with a reason, in `SLEEPING` — and the entry is an error once it wakes up. It also holds the markdown rules to every document: add a directory without adding it to their `paths` and the file is reported as unlinted |

Every caveat in that table is paid one of three ways: **a check**, **a named register**, or **a
sentence here**. The registers are visible in `scripts/repo_facts.py` — `EXEMPT` (trees that are
historical by construction, each with its reason), `SLEEPING` (rules allowed to match nothing for
now, each with the condition that wakes it, and the entry becomes an error once the rule matches)
and `COUNTS` (the claims that are checked at all). What is left is accepted rather than fixed, and
this paragraph is where it is written down: a number nobody registered is not checked, so quoting a
new noun means adding a line to `COUNTS`; the trees under `ignore:` are invisible to the markdown
rules, so a reference into `backlog/` or `.agents/skills/` is inline code by convention, not by
check; `repo-retired-values` enforces that a stale value is *acknowledged*, not that the
acknowledgement is true; and Vale's eight warnings are triaged on reading, not silenced.

```bash
pixi run alint                  # lint  → "✓ All 45 rule(s) passed."
pixi run alint list             # active rules
pixi run alint explain <rule>   # why a rule exists, what it checks
pixi run alint validate-config  # check the YAML
```

`gherlint` lints `experiment/features/` and, unlike alint, **exits 0 even when it reports
findings** — so the `gherlint` task pipes its output through `awk` (one line in `pixi.toml`, no
wrapper script): any line ending in a rule name is printed and turns into a non-zero exit, except
`(consider-using-background)`. That one is accepted on purpose: rule R202 cannot coexist with
`(missing-given-step)` (C101) when all scenarios repeat one shared `Given`, because C101 does not
count a `Background`'s `Given`, and completeness beats style here.

```bash
pixi run gherlint                        # lint experiment/features; exit 1 on any new finding
pixi run gherlint-stats                  # scenarios / steps / background / tags as a table
gherlint lint experiment/features        # raw binary — always exits 0, not CI-safe
```

Tag conventions live in `gherlint.toml` (`[convention]`): scenario tags must name a thesis card
(`@P-01`, `@A-01`, `@C-01`), feature tags must name the surface under test (`@katalog`, `@kod`,
`@obydwa`). Enforced only when a tag is present.

## js environment (isolated)

```bash
pixi run bun install
pixi run skills list
pixi run backlog task list
```

Package scripts are one-liners that need no `node_modules` paths:

| Script | Body | Result |
|---|---|---|
| `backlog` | `bunx --bun backlog` | backlog CLI (1.55.3) |
| `board` / `browser` | `bunx --bun backlog board` / `… browser` | kanban / web UI |
| `skills` | `bunx --bun skills` | skills CLI (1.7.4) |

**Why there is no nodejs in the env.** `bun x <pkg>` normally executes a package's bin through its
shebang — `#!/usr/bin/env node` — which would need Node on PATH (and `skills` needs ≥ 22.20, so
the sandbox's Node 20 would fail anyway). Passing `--bun` makes bun intercept that shebang and run
the script itself, so the `js` feature is one binary. `bun` is a passthrough task whose command is
`bun --bun`: everything after it is forwarded verbatim.

Note `bunfig.toml`'s `[run] bun = true` does **not** cover `bun x` (tested: it only affects
`bun run <script>`), hence the flag in the tasks themselves.

## renderers environment (isolated)

```bash
pixi run typst compile figure.typ figure.pdf
pixi run manim -ql scene.py Scene                      # -qh before it goes in the thesis
pixi run render omml '\frac{a}{b}'                     # maths, via the archont561 skill (below)
pixi run render list                                   # every command that skill dispatches
pixi run -e renderers python -c "import easypptx"     # slides for the defence (raw binary, so -e)
```

| Binary | Version | Why it is here |
|---|---|---|
| `typst` | 0.15.1 | typesetting a document without hand-laying it out; the conda-forge **compiler**, not the pypi bindings |
| `manim` | 0.22.1 | animations of the run loop and of the expressible-share argument for the results chapter and the defence |
| `easypptx` | 0.11.0 | the defence slides and the 70 × 100 poster, generated from the same numbers as chapter 6 rather than typed |
| `pandoc` | 3.13 | the single converter behind both halves of a formula on a slide: LaTeX → typst maths for the picture, LaTeX → DOCX/OMML for the editable equation. Handles `align`, matrices, `\bar`/`\vec`. A 161 MB Haskell binary — the price of not needing TeX, and it retired two pypi converters |
| `pypdfium2` | 5.15.1 | rasterises the formula PDF at any resolution, with transparency, from inside the env — so the picture route needs no poppler and no LibreOffice |

**Why its own feature and its own solve group.** `manim` pulls `numpy >= 2.1`, `scipy >= 1.13`,
`pycairo`, `manimpango`, `moderngl` and `ffmpeg` (9.0.2 arrives with it). Those are not the QGIS
env's business: `default` pins `qgis 3.44.*` and `pingouin 0.7.*`, and a shared solve group would let
a renderer's numpy floor move the geo solve. The separate group also means `pixi lock` failing in
one group cannot take the other down.

**What is deliberately not in it.** No QGIS and no `geo` feature — `import qgis` fails here on
purpose, so a renderer script cannot quietly grow into an analysis script. No TeX distribution:
`MathTex` needs a LaTeX install and is not available; `Tex`/`MathTex`-free scenes (`Text`, shapes,
plots) work, and for formulas the honest route is `typst` or a vector export from matplotlib.

### Rendering is a skill command

The maths code used to be four loose scripts in `scripts/`. It now lives in
`.agents/skills/archont561-render/commands/`, and it is
invoked through the **`archont561` runtime**, installed as a skill from
[`Archont561/skills`](https://github.com/Archont561/skills) and pinned in `skills-lock.json`:

```bash
pixi run render list                                   # the four commands, self-documented
pixi run render omml '\sqrt{x}' --format docx          # 1 of 4; trailing args are forwarded
```

How the dispatch works, because it is small enough to hold in your head:

- The runtime scans the skills root (`.agents/skills/`) for `archont561*` directories — a
  `skills-lock.json` *in that directory* would take over as an explicit manifest, but prefix scan is
  the mode here, so a new command provider needs no bookkeeping.
- Each `commands/<name>.py` becomes a command, with underscores turned into dashes
  (`omml_slide.py` → `omml-slide`). The module must define `def command(ctx, argv) -> int`, and the
  first line of its docstring is the summary `pixi run render list` prints.
- `commands/` is not on `sys.path` — modules are imported by file path — so the two that need a
  sibling (`omml_slide.py` → `omml`, `omml` → `mathml_omml`) put their own directory on the path.
  Shared code stays in a module beside them; a file prefixed with `_` is skipped by the scanner.

Adding a rendering route is therefore a file drop, not a wiring exercise.

The runtime is a dependency like any other, and `pixi run skills update` moves it: the pin is the
`computedHash` recorded in `skills-lock.json`, so an update is a reviewed diff rather than a
background drift, and nothing here schedules one.

`.agents/skills` is excluded from the tree-wide `ruff` run, because most of that tree is vendored
code nobody here wrote. These four modules are first-party, so `qa` names the directory explicitly —
`ruff check .agents/skills/archont561-render`, which ruff honours even though the tree is excluded
(a path passed on the command line bypasses `exclude`; only the `.` walk honours it). That is what
keeps the render code linted without also linting eleven vendored skills.

### Math on a slide — what actually works

`easypptx` 0.11.0 has **no math support of its own** (its only `math` import is the standard library, in
`textfit.py` and `slide.py`), and a PPTX cannot carry MathML: PowerPoint stores equations as **OMML**
(Office Math Markup Language). So neither package makes `add_text('$x^2$')` work by itself; they are
two steps of a chain that ends in a shape's text frame:

```text
LaTeX --pandoc--> DOCX/OMML --extract m:oMath--> OMML --<a14:m><m:oMathPara>--> PPTX
```

**The route that produces a live, editable equation** — the `omml-slide` command, which wraps the
OMML the way PowerPoint itself wraps it (`a14:m` from the DrawingML-2010 namespace around
`m:oMathPara`):

```bash
pixi run render omml-slide '\mathrm{MDE} = 3.42\sqrt{\tau^2 + 4950/r}'
pixi run render omml-slide '\frac{a}{b}' -o eq.pptx --title "Ratio"
```

#### The function, without a slide

The `omml` command is the converter on its own: a LaTeX string in, OMML out, no deck, no document,
no Office and no TeX.

```python
from omml import latex_to_omml            # '<m:oMath>…</m:oMath>'
from omml import add_equation             # appends to a python-pptx OR python-docx paragraph

omml = latex_to_omml(r"\frac{a}{b}")      # plain string, cached per formula in the process
add_equation(doc.add_paragraph(), r"E = mc^2")                  # Word: bare oMathPara
add_equation(shape.text_frame.paragraphs[0], r"E = mc^2")       # PowerPoint: a14:m wrapper
add_equation(p, r"\Delta = 1", display=False)                   # inline instead of displayed
```

`pptx_equation` / `docx_equation` return the wrapper each host wants; `add_equation` detects the
host from the paragraph's own tag, so the call site does not have to care. Caching is by string, the
returned elements are fresh, and `pixi run render omml '<latex>' --format pptx|docx|raw` prints what
you would be inserting. It is importable for callers running inside the renderers env — `commands/`
puts itself on `sys.path` — and it lives in the skill rather than in the `experiment` package
because it needs pandoc and the Office libraries, which only that env has.

Verified in both hosts by rendering the results: a python-docx manuscript (`omml-function-in-word.png`)
and a PPTX (below).

**Which readers draw a DOCX equation.** The file is right in all three cases; the reader is what
differs, and the difference decides what to ship:

| What the paragraph holds | Word | LibreOffice Writer | a docx→HTML preview (mammoth) |
|---|---|---|---|
| `m:oMathPara` / `m:oMath` (what `add_equation` writes) | drawn | drawn | **dropped silently** — prose survives, equation gone |
| `mc:AlternateContent` with the equation as `Choice` and a picture as `Fallback` | drawn (choice) | **nothing at all** | drawn (fallback picture) |
| a picture from `equation_picture` | drawn | drawn | drawn |

So the PPTX trick does **not** transfer: Impress resolves `mc:AlternateContent` and takes the
fallback, Writer does not resolve it at all and drops the whole construct. In a DOCX there are two
honest options and no third — the equation (editable, invisible in previews) or a picture of it
(visible everywhere, uneditable). `equation_picture(latex, workdir)` renders the PNG; insert it with
`run.add_picture(path)`.

**The route that is both** — `omml-slide` with its default `mc:AlternateContent` wrap. This
is the shape PowerPoint itself writes when it saves a slide carrying an equation: the same formula is
stored twice, once as the live equation and once as a picture, and the reader picks.

```xml
<mc:AlternateContent>
  <mc:Choice Requires="a14"> <p:sp> … <a14:m><m:oMathPara> … </p:sp> </mc:Choice>
  <mc:Fallback>              <p:pic> … the formula as a PNG …                </mc:Fallback>
</mc:AlternateContent>
```

PowerPoint reads the choice and hands back an editable equation; every reader without an OMML import
falls through to the fallback and draws the picture. `--no-fallback` writes the bare `a14:m` deck
instead (no `ppt/media` part, invisible outside PowerPoint).

**The route that is a picture only** — `math-slide`, when there is no equation to edit and the deck
only has to look right: LaTeX is typeset to a PDF and a
crop of that page is placed as a picture. The PDF is kept next to the deck, so the same formula can be
dropped into the thesis or the poster at vector quality.

```bash
pixi run render math-slide '\mathrm{MDE} = 3.42\sqrt{\tau^2 + 4950/r}' \
    -o slide.pptx --title "Precision of the design"
pixi run render math-slide '\Delta = \mathrm{TSR}_{N4} - \mathrm{TSR}_{K}' \
    --deck defence.pptx                       # append to a deck that already exists
```

```text
LaTeX --pandoc--> typst math --typst--> PDF --pypdfium2 (900 ppi, transparent)--> PNG --add_picture--> PPTX
```

`--mode vector` instead goes PDF → SVG → EMF through LibreOffice, which keeps the formula sharp at any
zoom, but write such a deck once: python-pptx 1.0.2 stores the EMF part as `image/x-wmf` and then
cannot reopen its own file (PIL has no metafile reader), so it can be added to and never edited
again. The raster has no such caveat.

Four defects met on the way, all now handled inside the script — worth knowing before trusting a
hand-rolled version of the same pipeline:

| Defect | Fix |
|---|---|
| `typst --format png` drops the radical's vinculum and mis-measures the page height | export the **PDF** and rasterise that with PDFium |
| `#set page(height: auto)` clips the denominator of a built-up fraction; a 1–2 pt margin clips the numerator and the vinculum, which the page top cuts off | fixed 5 cm page, **12 pt** margin, then crop to the ink (`Image.getbbox`) with a 4 px pad |
| a 900 ppi PNG still carries a white box unless the alpha channel is asked for | `fill_color=(255, 255, 255, 0)` — a non-opaque fill is what makes PDFium render into an alpha bitmap |
| `\begin{vmatrix}` / `\begin{Vmatrix}`: pandoc writes `mat(delim: "||")`, and typst's `delim:` takes exactly one character, so the compile fails | map `"||"` → `"‖"` (U+2016), which is what a determinant's bars are |

What the test runs established, so they do not have to be rediscovered:

| Attempt | Result |
|---|---|
| LaTeX → MathML → OMML → `a14:m` injection | **works** — the saved deck carries `<m:rad>`, `<m:sSup>` and `<m:r>` runs, no `ppt/media` part, and reopens in python-pptx |
| `\mathrm{...}` inside the formula | honoured: upright `<m:sty m:val="p"/>` for the label, italic for the variables |
| `typst --format png --ppi 300` → `add_image` | **works** — 300 ppi raster, lands as `ppt/media/image1.png` |
| `typst --format svg` → `add_image` | **fails**: `UnidentifiedImageError` — python-pptx goes through PIL, which has no SVG reader |
| `MathTex` in manim | needs a TeX distribution, which this env deliberately does not have |

**What rendering the output taught us** (LibreOffice 25.2 + poppler, installed ad hoc for the check):

| Test | Result |
|---|---|
| OMML **inside a DOCX**, converted by LibreOffice Writer | **renders** — so Writer is a usable proving ground for the markup |
| the first version of the script, same route | `√` with an empty placeholder and the radicand gone: the converter omitted the required `m:deg`, and the missing degree swallowed the content |
| after inserting `<m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/>` | `MDE = 3.42√(τ² + 4950/r)`, correct — this is what `omml-slide` now does |
| OMML **inside a PPTX**, `a14:m > m:oMathPara` (what PowerPoint writes) | **nothing drawn** — LibreOffice Impress drops it |
| OMML **inside a PPTX**, bare `m:oMath` in the paragraph | **nothing drawn** either |
| OMML in `mc:Choice Requires="a14"` + a picture in `mc:Fallback` | **renders** — Impress takes the fallback and draws the picture |
| same, with a red rectangle in place of the picture | the rectangle appears and the equation does not: the control that proves Impress never reads the `mc:Choice` branch |

So LibreOffice Impress has no OMML import at all, in either wrapper; that is a reader limitation, not a
defect in the file, but it is the reader used by most previewers — including the preview pane in this
workspace. **The fix is not a different renderer, it is a second representation in the same file**: the
`mc:AlternateContent` wrap above keeps the equation editable in PowerPoint *and* visible everywhere
else, at the cost of one 50 kB PNG per formula. Only when the fallback is not wanted is there a
choice to make — a picture cannot be re-typeset, renumbered or restyled, an OMML equation can and is
then invisible outside PowerPoint.

**Neither route needs LibreOffice.** The fallback picture is typeset by typst and rasterised by
PDFium, both inside the renderers env; proven by running the whole pipeline with `PATH` cut down to
the env's `bin`, where `shutil.which("soffice")` and `shutil.which("pdftocairo")` are both `None` and
the deck comes out byte-for-byte the same size class. LibreOffice is only the tool used to *look* at
the result — and `--mode vector` in `math_slide.py` is the one option that really does call it.

**One converter, not three.** The OMML used to come from `latex2mathml` → `mathml2omml` 0.0.2, two
pypi packages with two defects: the `m:deg` a square root needs was omitted (the radicand vanished and
the root drew as "√⍰"), and `\bar`/`\vec` produced markup that does not close. pandoc's DOCX writer
emits what Word itself consumes — `m:deg` present, `\bar` as `m:acc` with `m:chr val="‾"`, matrices as
`m:d` + `m:m` — and it was already in the env for the typst side, so both packages were dropped.
`omml-slide` keeps the guard they earned: `normalise_omml` still inserts a missing degree
and `REQUIRED_CHILDREN` still refuses to write a malformed equation. A page of `align` environments is
still pandoc's DOCX writer's job, not the script's.

**Write maths both branches agree on.** The two halves of a hybrid slide are typeset by different
engines, so the LaTeX has to mean the same thing to both: `4950/r` is a slash in each (pandoc escapes
it to `\/` on the typst side on purpose), and a stacked fraction needs `\frac{4950}{r}`. For a label,
`\text{MDE}` gives one upright run; `\mathrm{MDE}` gives a run per letter and reads as "M D E".

**How much LaTeX survives.** Two probes — 64 realistic formulas, then 88 single commands — through
`latex_to_typst()` and `typst compile`: **118 of 152 compiled**. Every failure was the same failure:
pandoc does not know the macro, so it hands the LaTeX back as **plain text** — nothing raises, and the
slide shows a monospace `\textcolor{blue}{x}` where the maths should be. That is worse than an error,
which is why the guard belongs in `latex_to_typst()` (reject output that does not start with `$`)
rather than in a reviewer's eye.

| Class | Commands |
|---|---|
| **falls back to raw LaTeX text** (19) | `\textcolor`, `\fbox`, `\cancelto`, `\hphantom`, `\vphantom`, `\vspace`, `\eqref`, `\intertext`, `\emph`, `\mbox`, `\hbox`, `\mathchoice`, `\leftroot`/`\uproot`, `\dbinom`, `\cfrac`, mathtools' `dcases`/`rcases`, a bare `\hline` |
| **silently degraded** | `\color` and `\tag` vanish; `\label` becomes a typst label outside the maths; `array`, `matrix`, `smallmatrix` lose the column gap (pandoc writes a bare `&`, which typst reads as an alignment point); `\hline` inside an array is dropped; `\setminus` comes out as a doubled backslash |
| **survives** | fractions (incl. nested), every root, `\sum`/`\int`/`\prod`/`\oint` with limits, `\lim`/`\limsup`/`\liminf`, `\binom`, `cases`, `aligned`/`align`/`align*`/`gather*`, all five matrix variants, `\overset`/`\underset`/`\stackrel`, `\operatorname*`, `\substack`, the accent and font alphabets, `\overbrace`/`\underbrace`, `\boxed`, `\phantom`, `\hspace`, `\cancel`, sized and `\middle` delimiters, `\colon`, `\%` |

**The same OMML without pandoc.** `mathml-omml` is a second backend for the editable
equation — `latex2mathml` → `mathml2omml`, both pure-python, no 161 MB binary and no subprocess.
`latex_to_omml(latex, backend="mathml")` reaches it; `backend="pandoc"` stays the default. Seven
repairs are needed before either package is usable, and each one has a formula that regressed
without it — recorded per repair in `commands/mathml_omml.py`. The two upstream packages carry
their own test suites; this repository keeps the list of repairs it depends on rather than a second
copy of a suite it did not write:

| Repair | What broke |
|---|---|
| a bare `&` is not well-formed XML | `latex2mathml` writes `<mi>&</mi>` for the alignment marker, so `aligned` kills every consumer with a SAX error |
| ASCII accents are invisible | `\hat` arrives as `^` (U+005E) and comes out as two runs, `y` then `^`; it needs the modifier letter and `stretchy` |
| `</m:groupChrPr>` is written as `</m:groupChr>` | the package's `MOver` branch emits markup that cannot be parsed |
| `<msqrt>` has neither `m:deg` nor `m:degHide` | Word draws "√⍰" and loses the radicand |
| an accent arrives as `m:groupChr` | it is a group character, not an accent; Word writes `m:acc` |
| `\lim` arrives as `m:sSub` | LibreOffice draws that form with a red "¿"; `m:limLow` is drawn correctly |
| `m:box` around every `mrow`, no `subHide`/`supHide` | the boxes misplace an indexed radical's degree in LibreOffice; without the flags a sum's limits stay at the side |

Measured against the pandoc backend on 30 formulas: **30/30 produce schema-valid OMML**, 21/30 are
glyph-for-glyph identical, and the nine differences are spacing characters, Unicode styled letters
(`ℝ` where pandoc writes `m:scr`) and one relation codepoint (`⪯` vs `≼`). Rendered through
LibreOffice the two documents are visually the same, with the shim ahead on `\mathbb`, `\mathbf`
and the determinant bars. Where the shim loses is coverage, not fidelity: anything pandoc's LaTeX
reader knows and `latex2mathml` does not — mathtools environments, macros, `\intertext`, `\eqref`.

**Sandbox.** `pixi-sandbox.toml` bundles `default` only, so this environment stays out of the
offline transport: the 1.4 GB of renderers would travel for nothing, and a thesis is not rendered
in the field. Restore a sandbox copy on a network host when figures have to be re-rendered.
