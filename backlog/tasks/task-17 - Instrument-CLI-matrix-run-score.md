---
id: TASK-17
title: 'Instrument CLI: matrix / run / score'
status: To Do
assignee: []
created_date: '2026-11-07T19:53:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - experiment
milestone: m-5
dependencies:
  - TASK-15
  - TASK-16
references:
  - experiment/README.md
documentation:
  - thesis/design/runs.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Without a single entry point the three stages (compute the matrix, execute a run, score the artefact) get launched from memory, and every argument mistake looks like a result. The CLI is also where the budget and the seed are enforced, not merely declared.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 matrix prints the matrix of tasks, conditions and repetitions without starting the model
- [ ] #2 run takes a seed and a turn budget, and their absence is an error, not a default
- [ ] #3 score runs the oracle on an artefact and returns a verdict per predicate
- [ ] #4 Every command has a BDD-style scenario test
<!-- AC:END -->
