---
id: TASK-19
title: Moving the thesis notes into six directories (phase 2)
status: To Do
assignee: []
created_date: '2026-11-07T19:57:00Z'
updated_date: '2026-11-07T20:10:00Z'
labels:
  - thesis
milestone: m-4
dependencies:
  - TASK-13
references:
  - thesis/README.md
documentation:
  - backlog/docs/doc-7 - Register-of-considerations-and-notes.md
priority: medium
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The notes lie flat, while chapters refer to them in prose and through --doc. While the draft is being rewritten (TASK-13), moving them means doing the same work twice and one more path bug; once the draft is closed it is a mechanical operation with a countable cost. The order is part of the task: --doc first, then mv, then prose, and the README last.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Six directories: praca 2, zakres-i-decyzje 20, metodyka 29, literatura-i-luki 20, formalnosci 10, obrona 2 - 83 files, each in exactly one
- [ ] #2 Every --doc/--ref fixed through backlog task edit, never by hand; backlog doctor reports no dead paths
- [ ] #3 Zero references from thesis/<file>.md to files that moved
- [ ] #4 alint 27/27, qa 0, test 9 passed after the move
<!-- AC:END -->
