---
id: TASK-15
title: 'Task card loader: YAML into a card object with schema validation'
status: To Do
assignee: []
created_date: '2026-11-07T19:53:00Z'
updated_date: '2026-11-09T00:00:00Z'
labels:
  - experiment
milestone: m-5
dependencies:
  - TASK-3
references:
  - thesis/design/corpus.md
documentation:
  - thesis/design/tool-surface.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The cards do not exist yet: `experiment/tasks/cards/` is empty until `TASK-3` writes the eighty files. What does exist is the contract they will be written against - `experiment/tasks/README.md` (canonical schema 1) and `scripts/task_cards.py`, which the `task-card-*` alint rules run over every card and every documented example. The loader is the remaining half, and it is where a typo in a contract field has to stop before the run, not after it - otherwise the series counts tasks nobody meant to ask.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every card file loads into an object with the contract fields
- [ ] #2 A card that violates the schema is rejected with the field name and card number
- [ ] #3 Tests cover: missing field, wrong type, non-existent coordinate system
- [ ] #4 Loading eighty cards completes in under a second
<!-- AC:END -->
