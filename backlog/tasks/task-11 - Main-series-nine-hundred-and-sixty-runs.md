---
id: TASK-11
title: 'Main series: nine hundred and sixty runs'
status: To Do
assignee: []
created_date: '2026-11-07T19:46:00Z'
updated_date: '2026-11-07T20:11:00Z'
labels:
  - thesis
milestone: m-2
dependencies:
  - TASK-8
references:
  - thesis/writing/plan.md
  - thesis/draft/thesis-draft-v0.md
documentation:
  - backlog/docs/doc-6 - Work-plan-and-schedule.md
  - thesis/draft/thesis-draft-v0.md
priority: high
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The main series is the only source of numbers for chapter 4. Its value depends on register completeness: a run without stop_reason is void, not zero, and zeroing gaps understates TSR.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 960 register rows, 80 tasks in each of three conditions and four repetitions
- [ ] #2 Zero runs without stop_reason
- [ ] #3 Technical incidents and retries are in the quality report, not in TSR
- [ ] #4 Seeds are stored and reproducible
<!-- AC:END -->
