---
id: TASK-6
title: Code arm in PyQGIS and the parity table
status: To Do
assignee: []
created_date: '2026-11-07T19:45:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - experiment
milestone: m-1
dependencies:
  - TASK-2
documentation:
  - thesis/framing/what-we-study.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The code arm is the reference point, so its capabilities must be identical to the catalogue. The parity table is the document that removes the objection that the comparison measures a difference in capability rather than a difference in interface.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every catalogue operation has a library equivalent, with its version
- [ ] #2 The same script run in both arms yields an identical artefact hash
- [ ] #3 Capability differences are listed explicitly or removed
<!-- AC:END -->
