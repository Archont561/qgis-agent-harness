---
title: Placeholder pages
description: Scaffolding — three pages that exist so the build, the stylesheet and the navigation can be checked before any real content is written.
---

# Placeholder pages

These pages are scaffolding. They carry no thesis content: they exist so that the build, the design
tokens and the navigation can be proved end to end before a single real page is written. Delete the
directory when the site has content of its own.

| Page | What it proves |
|---|---|
| [Design tokens](./tokens.md) | that `assets/site.css` reaches a rendered page, and follows the theme |
| [Numbers](./numbers.md) | that the tables of results will line up in columns |

Both pages are held to the same shape as everything else in `site/`: `alint` runs
`scripts/house_style.py invariants` over them.
