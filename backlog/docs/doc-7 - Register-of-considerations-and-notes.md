---
id: doc-7
title: Register of considerations and notes
type: guide
created_date: '2026-11-07T19:53:00Z'
updated_date: '2026-11-07T20:56:00Z'
---
Notes in `thesis/` are not chapters. They are working material: decisions, doubts, other people's positions, sketches. This document says where to look for what, so that nobody has to read eighty files in order.

## Four directories, one document per question (map: `thesis/README.md`)

Since 7 XI 2026 the 84 flat notes are merged into 17 documents; each still carries a `<!-- from ... -->` comment naming the note a section came from, so an old reference can be resolved inside the new file.

| Directory | Contents | Documents |
|---|---|---|
| `thesis/framing/` | aim, gap, what is studied, scope, the edge of the scope | 5 |
| `thesis/design/` | experiment, one run, arms and validation, correctness, tool surface, corpus, harness | 7 |
| `thesis/analysis/` | from runs to claims: hypotheses, power, analysis | 1 |
| `thesis/writing/` | requirements, key concepts, plan, critique, defence | 5 |
| `thesis/draft/` | the thesis text, its structure and its titles | 4 |
| `thesis/competitions/` | rulebooks as faithful conversions | 6 |

Pruning (`TASK-21`) is what turns these documents from everything-written-down into something a chapter can lift; translation (`TASK-20`) follows it, not the other way round.

## Three kinds of notes and what they are for

- **Considerations and objections** - possible counter-arguments ("MCP is just a wrapper", "code wins because the tasks are code-like") and the answers to them. They go into chapter 5; candidates for the defence.
- **Other people's positions** - who claims what and what they did not check; raw material for chapter 2, not for citing without verification.
- **Decisions** - what was chosen, what was rejected and at what cost. Also recorded in the backlog (`backlog decisions`), so that they do not get lost in prose.

## Bibliographic apparatus

`thesis/literature/literature.bib` (67 items) · `thesis/literature/index.md` (map of items) · `thesis/literature/fulltexts/` (30 transcripts, the source of quotations) · `thesis/literature/search-review.md` (how the set was built) · `thesis/external-sources.md` (external documents without a full text).

The rule: a quotation comes only from `fulltexts/` or from a document named in `external-sources.md`. A summary of somebody's work is not a source for a quotation.

## Further reading

`thesis/README.md` (tree map, folder by chapter) · `thesis/writing/defence.md` · `thesis/literature/index.md`
