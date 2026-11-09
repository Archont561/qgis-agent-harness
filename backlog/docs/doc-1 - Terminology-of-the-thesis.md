---
id: doc-1
title: 'Terminology of the thesis'
type: guide
created_date: '2026-11-07T19:45:00Z'
updated_date: '2026-11-07T20:09:00Z'
---
A pointer, not a copy. Three layers of terminology live in `thesis/` and change there; this document only says where to look and what the rule is.

| Layer | File | Used for |
|---|---|---|
| operational definitions (definition, "do not confuse with", observation, example) | `thesis/writing/key-concepts.md` | §3.1 of the thesis |
| mapping English -> Polish -> first-use location | `thesis/concept-dictionary.md` | appendix B |
| correction glossary: anglicism -> Polish term, exception list | `thesis/glossary-of-terms.md` | editing |

## The rule

The first use in the text gives the English term once, afterwards only one form; identifiers and proper names (MCP, PyQGIS, EPSG, `detected_by`) stay untranslated.

The correction is applied **by hand using the table in `glossary-of-terms.md`** - there has been no automation since 7 November 2026. The reason: substitution changes grammatical gender (*prompt* -> *polecenie*, *feedback* -> *informacja zwrotna*), so every sentence needs review, and the script hid how many sentences had not been reviewed. About 415 unresolved occurrences remain in the corpus - that is editorial debt, not a fault.

Dictionary files (`concept-dictionary.md`, `glossary-of-terms.md`), `literature/index.md` and `literature/search-review.md` are **excluded from the correction**: the English term there is the source column or a paper title.

## Order of work

Core document (chapters 3 and 5) -> chapters 1, 2, 6 -> working notes. Chapters 4 and 6 are written only after the results exist (`TASK-12`), so correcting the main text makes sense only after `TASK-13`.
