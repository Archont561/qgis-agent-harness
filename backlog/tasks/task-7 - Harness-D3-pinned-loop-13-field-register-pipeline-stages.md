---
id: TASK-7
title: 'Harness D3: pinned loop, 13-field register, pipeline stages'
status: To Do
assignee: []
created_date: '2026-11-07T19:46:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - experiment
milestone: m-1
dependencies:
  - TASK-5
  - TASK-6
references:
  - thesis/writing/key-concepts.md
documentation:
  - thesis/design/harness.md
  - backlog/docs/doc-4 - Specification-of-experiment-the-instrument-code.md
priority: high
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The harness is an instrument, not a product: it decides what reaches the register and what can no longer be reconstructed after the fact. The register must be complete before the first run, because a run without stop_reason cannot be rebuilt later.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The register stores 13 fields, including run_id, stop_reason, detected_by, artifact_hash
- [ ] #2 Two independent loop implementations yield the same artefact for the same seed
- [ ] #3 The 30-turn budget is enforced, and exceeding it ends the run as stop_reason = budget
- [ ] #4 Every task declared in experiment.yml passes a trial run
<!-- AC:END -->
