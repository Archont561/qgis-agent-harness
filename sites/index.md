---
title: QGIS agent harness
description: A pre-registered comparison of MCP tool use against PyQGIS code generation, and the harness that runs it.
---

# QGIS agent harness

**Does exposing GIS operations as MCP tools change how often a fixed model produces correct QGIS
work, compared with generating PyQGIS code?** The comparison is pre-registered, run on one pinned
model, scored by spatial predicates rather than by a judging model, and reported as conditional on
data, surface and task class — never as "MCP beats codegen".

> Status: pre-registration open (milestone `m-0`, gate G1 not passed) — no number produced by
> `experiment/` counts until the measures are frozen.

## What the repository holds

| Path | What it is |
|---|---|
| `thesis/` | the thesis text: framing, design, analysis, the draft chapters and the sources |
| `experiment/` | the harness that runs the tasks, records the runs and scores them |
| `backlog/` | tasks, documents, decisions and milestones — the only place work is tracked |
| `docs/` | how this repository works: environments, tests, sandbox, commits, agents |

Nothing here is published: no package, no release, no version.

## How this site is built

The pages live in `sites/`; the text they publish stays in `thesis/` and is pulled in with
`{include}`. Two commands, in this order — the second names a stylesheet the first generates:

```sh
pixi run site-css          # uno.config.ts + the scanned content -> sites/assets/site.css
pixi run docs build --html # sites/ -> sites/_build/html
```

`assets/site.css` carries the design tokens as custom properties, so the utilities the pages use
follow the reader's light or dark theme without a second set of rules. What the reader is looking at
is the second command's output, published by `.github/workflows/pages.yml` on every push to `main`.
