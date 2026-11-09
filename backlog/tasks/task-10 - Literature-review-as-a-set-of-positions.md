---
id: TASK-10
title: Literature review as a set of positions
status: To Do
assignee: []
created_date: '2026-11-07T19:46:00Z'
updated_date: '2026-11-09T00:00:00Z'
labels:
  - thesis
  - literature
milestone: m-1
dependencies:
  - TASK-9
documentation:
  - backlog/docs/doc-7 - Register-of-considerations-and-notes.md
  - thesis/draft/thesis-draft-v0.md
priority: medium
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The faculty rules require a set of positions, and the draft has an inventory of four currents. This is the only §V requirement that a checklist cannot replace - a position needs a thesis and a counter-argument.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every position has a thesis and a counter-argument answer
- [ ] #2 The axis of the dispute is named in one sentence in the chapter introduction
- [ ] #3 Every claim carries a citation per Appendix 4
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Bibliography gap found while pruning thesis/framing/gap-and-literature.md (7 XI 2026). The text argues from nine works that are not in thesis/literature/literature.bib: huang2024 (arXiv 2310.01798, ICLR 2024), kamoi (2406.01297, TACL 2024), tyen (2024), codeact (2402.01030, ICML 2024), cemcp (2602.15945), mcp_atlas (2602.00933), mcpevol (2607.14642); plus the domain-specific MCP benchmarks named in the previous run (MedMCP-Calc, DynamicMCPBench, MCPAgentBench, ComplexMCP, FinMCP-Bench). Three of them carry the mechanism for H2, four carry the evidence against the thesis. Verify each DOI/venue before adding; the citation-hygiene table in gap-and-literature.md section 9 says which are preprints and which are peer-reviewed, and GeoNatureAgent (2610.09112) needs its DOI checked.
<!-- SECTION:NOTES:END -->
