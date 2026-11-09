---
id: TASK-3
title: Eighty task cards as YAML
status: To Do
assignee: []
created_date: '2026-11-07T19:45:00Z'
updated_date: '2026-11-09T00:00:00Z'
labels:
  - thesis
milestone: m-0
dependencies: []
references:
  - thesis/design/corpus.md
documentation:
  - thesis/design/corpus.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
  - backlog/docs/doc-6 - Work-plan-and-schedule.md
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Cards are the unit of the corpus and the only place where expectations are written down. Without them the oracle has nothing to check and the expressible share has nothing to encode.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Eighty files carrying the canonical contract in `experiment/tasks/README.md`: `schema`, `id`, `family`, `tier`, `expressible`, `prompt`, `inputs`, `expected_artifact`, `pitfalls`, `licence`, `created`, `oracle`, `negative_control`
- [ ] #2 Every card has at least four `oracle.checks` spanning at least two predicates, and a `negative_control` naming the checks it must fail
- [ ] #3 `pixi run alint` rule `task-card-schema-cards` passes for all eighty files, and its `SLEEPING` entry in `scripts/repo_facts.py` is gone
- [ ] #4 The P/A/C family distribution matches the decision taken
<!-- AC:END -->
