---
id: TASK-1
title: Close and freeze the numbers before gate G1
status: To Do
assignee: []
created_date: '2026-11-07T19:45:00Z'
updated_date: '2026-11-07T20:31:00Z'
labels:
  - thesis
milestone: m-0
dependencies: []
references:
  - thesis/writing/plan.md
documentation:
  - thesis/analysis/statistics.md
  - backlog/docs/doc-6 - Work-plan-and-schedule.md
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Chapters 3 and 4 of the draft currently give different ladders, different repetition counts and different MDEs, and the pre-registration is meant to close those numbers for good. Until they agree, every run computed against one version is void against the other.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The four inconsistencies in §8 are closed
- [ ] #2 The ladder is 5/15/30, not 5/15/30/50
- [ ] #3 H5 computes ED from 8 repetitions
- [ ] #4 The MDE is stated as 13-14 pp at 40 x 8, alpha = 0.05
- [ ] #5 The run total agrees with the number in the main part
- [ ] #6 The pre-registration document carries a date and a version
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
The harness was reset on 7 XI 2026: `experiment/` is a Typer app that prints hello world, the old 4 x 3 x 50 x 3 = 1,800 matrix is gone, `reports/` and `features/cli.feature` are deleted. This task therefore has to *write* the matrix (conditions x tasks x repetitions), not inherit one from the scaffold.
<!-- SECTION:NOTES:END -->
