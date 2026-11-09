---
id: TASK-5
title: 'MCP server: nine operations, gates N1/N4, handle with georeferencing'
status: To Do
assignee: []
created_date: '2026-11-07T19:45:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - experiment
milestone: m-1
dependencies:
  - TASK-2
references:
  - thesis/writing/key-concepts.md
documentation:
  - thesis/design/tool-surface.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Without a surface there is nothing to compare. Condition N1 is the schema alone, N4 adds invariants and terminal conditions - the difference between them is the content of the measurement, so both configurations must come from one codebase, not two servers.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Each of the nine operations has a schema and declared gates
- [ ] #2 The structural result of every operation carries a handle with crs, transform, nodata, dtype, shape
- [ ] #3 A bad parameter returns as isError with content that allows repair
- [ ] #4 Conditions N1 and N4 differ only in gates, not in the operation set
<!-- AC:END -->
