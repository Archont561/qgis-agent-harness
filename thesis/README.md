---
id: README
title: "thesis/"
type: index
status: live
language: en
updated_date: '2026-11-09'
---

# thesis/

One question this index answers: **which file is thesis text, which is a source, and which is a note.** The tree is **eight directories** — `framing/`, `design/`, `analysis/` and `writing/` hold the thesis itself (20 files); `draft/`, `competitions/`, `img/` and `literature/` hold the assembled text, the rule sources and the sources. The merge of 7 XI 2026 turned 84 flat notes into 17 documents across those four directories and `draft/` (`titles.md`, `structure.md`) — the set `TASK-21` prunes — so the four count 18 files, not 17.

## The five sentences that say what the thesis is

One question this section answers: **where the thesis's identity is fixed**, so that a sixth statement of it is an edit to one of these five rather than a new paragraph somewhere else.

| # | Sentence | Fixed in | What it is for |
|---|---|---|---|
| 1 | the title pair, Polish and English | `draft/titles.md` §0 | what is approved — **binds the other four** |
| 2 | the abstract's first two sentences | `draft/titles.md` §4.1 | what a reader meets first: the comparison, the identical runtime, the measured object, and the excluded hybrid |
| 3 | the aim | `framing/aim-and-contributions.md` §1 | what is to be established, decomposed into *whether · to what extent · through what* |
| 4 | the thesis statement | `draft/thesis-draft-v0.md` §1.4 | the position defended, marked as a position under test |
| 5 | the contribution statement C1–C3 | `framing/aim-and-contributions.md` §7 | what chapter 7 claims |

**The rule that keeps them reconcilable:** none of the five may name a comparison, a factor, an engine, an outcome or a condition the others do not have. If two disagree, the approved title binds the rest and the aim binds every claim downstream; the abstract's version is the *narrower* of the first two, because it is read by people who will never see the design.

## Thesis text — `draft/`

- `draft/thesis-draft-v0.md` — continuous draft in English, §1–§7 + appendix A; rebuild into six chapters: `TASK-13`
- `draft/draft-minimal.md` — minimal version: what it checks, how, and what may come out
- `draft/structure.md` — structure, proportions, TOC and the IMRAD metaplan
- `draft/titles.md` — the title, its revisions, the alternatives and their assessment
- `draft/metaplan.md` — the four-question scaffold behind §1.1–1.4, and the poster version of it
- `img/` — figures (`experiment-schemat.svg`)

## Sources

- `literature/` — `literature.bib` (69 items), `index.md` (key → DOI → transcript), `fulltexts/` (30 transcripts), `search-review.md`, `search/` (queries + raw 2026-10-31 dumps)
- `competitions/` — the rulebooks as faithful conversions: `pti-kpm-rules.md`, `sgp-kd-rules-2023.md`, `marpit-geoinformation-award-2020.md`, plus `historical-editions.md` and `competition-verification.md`
- `external-sources.md` — external documents that have no full text (the UMCS rules, SGP+GGK 2023, an archival MRiT act)

The rule: **a quotation comes only from `literature/fulltexts/` or from a document named in `external-sources.md`.** A summary of somebody's work is not a source for a quotation.

## Notes — four directories, one document per question

Every file below is a merged document: its sections came from separate notes and each section still begins with a `<!-- from … -->` comment naming the note it came from.

| Directory | Feeds | Documents |
|---|---|---|
| `framing/` | ch. 1, ch. 2, abstract, keywords | the questions and the justification |
| `design/` | ch. 3 (method), ch. 4 (instrument) | what is measured, with what, on what corpus |
| `analysis/` | ch. 4 (measures), ch. 6 (results) | from numbers to claims |
| `writing/` | formalities, appendix, defence | rules and rehearsal, not content |

### `framing/`

| File | Question it answers |
|---|---|
| `aim-and-contributions.md` | what does the thesis establish, and what is new about it |
| `gap-and-literature.md` | what is not known yet, and which of it this thesis answers |
| `what-we-study.md` | which question is measured, which is argued, which is out of reach |
| `scope-and-character.md` | how large is the thesis, and what kind of study is it |
| `edge-of-scope.md` | what this thesis does not claim, and where the claim stops holding |

### `design/`

| File | Question it answers |
|---|---|
| `experiment.md` | what is measured, on what, and what comes out of one series |
| `runs.md` | what physically happens between the prompt and the scored artefact |
| `arms-and-validation.md` | what is manipulated, what is held fixed, where validation sits |
| `correctness.md` | what makes an artefact correct, and where a wrong one can be caught |
| `tool-surface.md` | how many tools, of what kind, on how many servers |
| `corpus.md` | how large the task set must be, and how it is chosen without begging the question |
| `harness.md` | own instrument or a ready agent, and what that costs to run |

### `analysis/`

| File | Question it answers |
|---|---|
| `statistics.md` | which test decides what, with what power, and what may not be claimed afterwards |

### `writing/`

| File | Question it answers |
|---|---|
| `requirements.md` | which faculty and competition requirements bind the text |
| `key-concepts.md` | operational definitions for §3.1 |
| `theory-primer.md` | the same vocabulary from zero: what an LLM, an agent, a harness, exposure, spatial correctness and an MDE are |
| `plan.md` | the half-year plan |
| `critique.md` | the standing critique review of the design |
| `defence.md` | defence theory: what has to be known and how to say it |
| `design-answers.md` | the six questions about the design — nine operations, eighty tasks, the card, the arms, the predicates, the effect |

## Frontmatter — one schema, checked by `alint`

Every file in this tree opens with YAML frontmatter, the same shape as a backlog task: an `id`, a `title`, a `type`, a `status`. Two fields are specific to this tree — `language`, which is what `TASK-20` counts, and `sources`, which records the notes a merged document was built from (`TASK-21`).

```yaml
---
id: design/corpus                                   # path under thesis/, without .md
title: "The corpus: how many tasks, which ones, and why"   # identical to the H1
type: note                  # note | draft | index | glossary | dictionary | register | rulebook | fulltext
status: live                # live | frozen
language: en                # en | pl — the only two allowed, and the whole of TASK-20
question: "How large must the task set be, and how is it chosen without begging the question?"
tasks: [TASK-3, TASK-4, TASK-21]                    # backlog tasks that own this file
sources: [tasks-40.md, tasks-per-domain.md, ...]     # only on merged documents
updated_date: '2026-11-07'  # omitted when status is frozen
---
```

Three rules keep it honest:

- **`status: frozen`** marks what is not ours to edit: `glossary-of-terms.md`, `concept-dictionary.md`, the four competition conversions and the 30 transcripts. Those carry no `updated_date`, because there is no such date — with one exception, `concept-dictionary.md`, whose `updated_date` is the 7 November 2026 reconciliation of its "gdzie" column against the one table of contents (chapter numbers confirmed, subsection numbers marked provisional).
- **`language` is a claim about the file, not about the project.** A document that is still Polish says `pl`; when it is translated the field flips in the same commit as the text.
- **The transcripts carry a bibliography record** — `key`, `resource`, `description`, `page`, `venue`, `authors`, `year` — in the same block, above `id`. One frontmatter, two dialects: the bib fields serve `literature/index.md`, the common fields serve the linter.

`alint` rule `thesis-frontmatter` enforces the five universal keys, the `updated_date`-unless-frozen rule, and that `id` matches the path — so a document cannot be moved or renamed without its metadata following:

```bash
pixi run alint        # 48 rules, one of which is this schema
```

## Rules

- **Terminology correction is manual**, following the table in `glossary-of-terms.md` (no script since 7 November 2026). Polish on purpose: `glossary-of-terms.md`, `concept-dictionary.md`. Do not touch: `literature/index.md`, `literature/search-review.md`, `fulltexts/`, `search/` — the English there is source content.
- **Do not add a new note.** If a question is already a document above, extend that document; a new file needs a question that none of the 17 answers, and then it gets its own row here.
- **The backlog links these files through `--doc`/`--ref`.** Renaming a file requires `backlog task edit --remove-doc … --add-doc …`; backlog files are never edited by hand.
- **Bibliography for APD:** the list in the thesis must be converted to the format of Appendix 5 (no DOI in parentheses) — `literature.bib` serves the pipeline, it is not the list.
- **One source of truth for decisions:** a design decision written in prose must have its counterpart in `backlog decisions` (1–7), otherwise it is lost when the text is rebuilt.

## Tree history

| When | What | Where | Trace |
|---|---|---|---|
| 7 Nov 2026 | **YAML frontmatter on all 64 files** (`id`, `title`, `type`, `status`, `language`, `question`, `tasks`, `sources`, `updated_date`) | every file in this tree | new `alint` rule `thesis-frontmatter`, 27 → 28 rules |
| 7 Nov 2026 | **84 flat notes → 17 documents** in `framing/`, `design/`, `analysis/`, `writing/`; `draft/` for the text | this tree | 63 files rewritten references, `--doc`/`--ref` fixed in 18 tasks, plan kept in `TASK-21` |
| 7 Nov 2026 | `konkursy/` → `competitions/`, `literatura/` → `literature/` | English directory names | 2 prose references, 1 line in `.alint.yml` |
| 7 Nov 2026 | `literature/` (bib + index + 30 transcripts) | `thesis/literature/`, `fulltext/` → `fulltexts/` | 12 prose references, 30 links in `index.md` |
| 7 Nov 2026 | `search/` (review + `queries.json` + `run_search.py` + 23 JSON) | `literature/search-review.md`, `literature/search/` | `TASK-9 --ref` |
| 7 Nov 2026 | `uploads/` (3 PDFs) | deleted; provenance in `external-sources.md` | no references |
| 7 Nov 2026 | `backlog-triage.md`, `restrukturyzacja-thesis.md` | knowledge: `backlog/docs/doc-8`, this file, `TASK-19` (completed, now in `backlog/archive/`) | files removed from the root |
| 7 Nov 2026 | all Polish file names in `thesis/`, `konkursy/`, `literatura/` | English names | references rewritten in 30+ files, `--doc` unchanged by the move |

There is no git in `research/`, so every such operation is irreversible: copy `thesis/` to a directory outside the repository before starting one.

## What is still owed on this tree

1. **Pruning (`TASK-21`).** The merge preserved text; it did not reconcile it. Two design generations coexist inside the merged documents (40 tasks / 1 218 runs / H4a 2×2 TOST vs 80 tasks / 960 runs, decisions `d-1`–`d-2`), so each document has to be read once and the retired half removed. Target: 6,000–8,000 words per document.
2. **Translation (`TASK-20`).** Every file here is still Polish except the draft, the glossaries and the documents translated on 7 XI 2026.

## Why the notes no longer lie flat: the discarded Phase 2 map

Before this restructure the plan was to split the flat notes into six directories and leave them as 83 files. That map is void — it would have produced 84 → 83. It is recorded in the history row of 7 Nov 2026 above and in `TASK-21`, because its cost table (14 `--doc` paths, 3 README places, the `doc-1…8` bodies, the move order) was accurate and was reused verbatim.
