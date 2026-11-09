---
id: TASK-18
title: 'Executor sandbox: run isolation, turn limit, seed determinism'
status: To Do
assignee: []
created_date: '2026-11-07T19:53:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - experiment
milestone: m-5
dependencies:
  - TASK-7
references:
  - thesis/design/harness.md
documentation:
  - thesis/design/harness.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Two runs of the same task must differ only in what is meant to differ. Without working-directory isolation and seed control, the difference between conditions may come from leftovers of the previous run.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every run starts in a clean working directory
- [ ] #2 The turn limit is enforced in the loop, not in the prompt
- [ ] #3 Two runs with the same seed yield an identical artefact hash
- [ ] #4 Exceeding the limit records stop_reason = budget
<!-- AC:END -->
