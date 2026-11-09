---
id: TASK-2
title: 'Oracle: predicates with tolerances and tests for the oracle'
status: To Do
assignee: []
created_date: '2026-11-07T19:45:00Z'
updated_date: '2026-11-09T00:00:00Z'
labels:
  - experiment
milestone: m-0
dependencies: []
documentation:
  - backlog/docs/doc-6 - Work-plan-and-schedule.md
  - thesis/draft/thesis-draft-v0.md
priority: high
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The whole thesis judges artefact correctness, so the oracle is a measuring instrument, not a helper script. An oracle that returns different verdicts for the same (artefact, card) pair invalidates TSR no matter what the model does.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The same (artefact, card) pair returns the same verdict in two runs
- [ ] #2 Every predicate that measures a quantity carries an explicit tolerance (`numeric`, `extent_iou`, `scalar`); the set-valued ones (`crs_equal`, `geom_valid`, `attr_present`) are exact by construction
- [ ] #3 Tests cover artefacts broken on purpose: wrong CRS, missing field, NaN instead of NoData
- [ ] #4 The oracle verdict is stored per predicate, not as a single flag
<!-- AC:END -->
