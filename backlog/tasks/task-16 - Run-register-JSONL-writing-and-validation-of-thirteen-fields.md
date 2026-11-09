---
id: TASK-16
title: 'Run register: JSONL writing and validation of thirteen fields'
status: To Do
assignee: []
created_date: '2026-11-07T19:53:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - experiment
milestone: m-5
dependencies:
  - TASK-7
documentation:
  - thesis/writing/key-concepts.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The register is the only evidence that a run happened. A run without stop_reason is void, not zero, so field validation must be enforced at write time, not at analysis time.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every run appends one JSONL row with thirteen fields
- [ ] #2 Writing rejects a row without stop_reason or without artifact_hash
- [ ] #3 The validator detects a duplicate run_id
- [ ] #4 Tests cover the four stop_reason values
<!-- AC:END -->
