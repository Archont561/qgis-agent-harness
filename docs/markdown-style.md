# Markdown style

A README is read twice: once by a person deciding whether to look further, and once by a search engine
deciding what it is. Both reads reward the same thing — a stable shape — so the shape is checked rather
than remembered. The rule is `scripts/house_style.py`, and it is calibrated on the account's own
repositories rather than on taste.

```bash
python3 scripts/house_style.py invariants   README.md   # every repository
python3 scripts/house_style.py skeleton     README.md   # a repository that adopts the skeleton
python3 scripts/house_style.py contributing CONTRIBUTING.md
python3 scripts/house_style.py readme       README.md   # invariants + skeleton, for CI
```

## The calibration

Seven repositories were read before the rules were written — `skills`, `qgis-sdk`, `ODM-conda`,
`universe`, `pixi-sandbox`, `clifacet`, `playtest` — and the split between the modes follows what they
actually do, not what would be tidy:

| Mode | What it checks | Evidence |
|---|---|---|
| `invariants` | H1 on the first line (after front matter), no skipped heading levels, no punctuation at the end of a heading, no emoji, tagged fences from a known vocabulary, `alt` on every badge, an alignment row under every table header, `## License` last and spelled the American way | **7 of 7 repositories pass** |
| `skeleton` | a centred `<p align="center">` badge block, a bold tagline, a `> Status:` line above the first `##`, then `Try it` → `Develop` → `Documentation` → `License` | `qgis-sdk` and `skills`; `universe` and `pixi-sandbox` use other section names |
| `contributing` | H1 reading `# Contributing to <repository>`, then `Environment` → `Commands` → `Commits`, with a command table that gives every command a purpose | `universe/CONTRIBUTING.md` |

The split is the honest part. A rule that six of seven repositories fail is an opinion, so the
skeleton is **opt-in**: `invariants` is enforced here, and `skeleton` is used by repositories written
to that shape. Enforcing it everywhere would either be ignored or would rewrite seven READMEs to match
a convention they predate.

## Where it is enforced

| Rule | Paths | Mode |
|---|---|---|
| `readme-house-style` | `README.md` | `invariants` |
| `docs-house-style` | `docs/**/*.md` | `invariants` |

Both are `level: error`, so they fail `pixi run qa` rather than printing advice. The first run of the
rule found two real defects — an untagged pipeline fence and a missing `text` tag in
[`environments.md`](environments.md) — which is the whole argument for having it: nobody was going to
notice those in review.

## What is deliberately not checked

- **Prose.** Vale owns words; this owns shape. `backend`, `leverage` and the Oxford comma are
  [prose](prose.md)'s business.
- **Section content.** A `## Documentation` section with no useful link passes the rule, because the
  alternative is a linter that grades meaning and is wrong half the time.
- **Line length.** The repositories wrap at different widths, and a hard wrap rule fights every diff.
- **Typography that carries data.** A check mark in a table of required fields is data, not decoration,
  so a short allowlist of marks — `✓ ✔ ✗ ✘ ▲ ● ■ ★ →` and their relatives — passes, while a pictograph
  such as a green tick button fails. `experiment/tasks/README.md` is the reason the allowlist exists:
  its `Req.` column is check marks, and the alternative was pushing a real table into a ```text block to
  satisfy a linter.
- **The thesis notes and the literature.** `thesis/literature/fulltexts/` is verbatim source material and
  is never restyled; the argumentative notes under `thesis/` use question-headed sections by choice, and
  the invariant set was calibrated on repositories' READMEs, not on an argument. Applying it there would
  rewrite a voice rather than fix a defect, so the rule stops at `docs/`.

## Adopting it in a new repository

1. Copy `scripts/house_style.py` — it is stdlib-only, so it runs wherever `python3` does.
2. Copy the two rules from [`.alint.yml`](../.alint.yml) into the new repository's config, and add
   `readme-house-style` and `house-contributing-style` (mode `contributing`, paths
   `CONTRIBUTING.md`).
3. Run `pixi run alint`. A README written to the skeleton passes both modes on the first attempt.

`pymarkdown` is the complementary tool — it checks markdown syntax rather than this account's shape,
and it is what the `skills` repository runs through its two `.pymarkdown.*.json` configs. It is not
wired here because the syntax layer is already covered by the `markdown-paths-resolve` and
`markdown-fragments-resolve` rules; add it if a second consumer needs the same syntax gate.
