---
id: TASK-21
title: Prune the 17 merged thesis documents
status: In Progress
assignee: []
created_date: '2026-11-07T20:55:00Z'
updated_date: '2026-11-09T00:00:00Z'
labels:
  - thesis
milestone: m-3
dependencies: []
priority: high
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The merge of 7 XI 2026 preserved text but did not reconcile it: two design generations sit inside the same documents (40 tasks / 1218 runs / H4a 2x2 TOST versus 80 tasks / 960 runs per decisions d-1 and d-2), and roughly 40 percent of every document restates an argument made two sections above. One reading pass per document, once, in size order.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Every merged document ends with a five-line summary that a chapter can lift verbatim
- [ ] #2 No section argues the retired generation (40 tasks, 1218 runs, H4a 2x2 TOST, 100 tools) except as a rejected option together with the reason it was rejected
- [ ] #3 Every deletion has its reason in doc-8; no provenance block is dropped while its content is still the only place a claim is made
- [ ] #4 6000-8000 words per document; a document still over 10000 words after pruning is split by sub-question and thesis/README.md updated
- [x] #5 corpus.md pruned: 13,379 -> 6,723 words, cuts registered in doc-8
- [x] #6 experiment.md pruned: 11,967 -> 4,219 words, rewritten against the live design, cuts in doc-8
- [x] #7 scope-and-character.md pruned: 9,541 -> 7,669 words, cuts in doc-8, ends with the five lines of section 8
- [x] #8 edge-of-scope.md pruned: 9,126 -> 7,551 words, cuts in doc-8, ends with the five lines of section 7
- [x] #9 alint 28/28, qa clean, test green, backlog doctor clean
- [x] #10 statistics.md pruned: 8,088 -> 6,662 words against the live design, cuts in doc-8
- [x] #11 arms-and-validation.md pruned: 7,530 -> 6,455 words, now the single owner of the claim ledger H1-H3 + D1-D4
- [x] #12 gap-and-literature.md pruned: 7,505 -> 6,063 words, RQs mapped onto the live ledger
- [x] #13 titles.md pruned: 7,482 -> 6,012 words, the S1-S8 alternative scopes removed
- [x] #14 what-we-study.md pruned: 7,413 -> 6,493 words, contrast ladder redrawn against K/N1/N4
- [x] #15 aim-and-contributions.md pruned: 7,207 -> 6,011 words, stale MDE/runs figures replaced
- [x] #16 correctness.md pruned: 6,858 -> 6,432 words, four-arm table and power tables retired
- [x] #17 harness.md pruned: 6,728 -> 6,406 words, front-end x model factor retired
- [x] #18 tool-surface.md pruned: 6,445 -> 6,091 words, size ladder and meta-tool/two-server arms retired
- [x] #19 structure.md reconciled: three competing tables of contents -> one, 5,875 -> 6,043 words, H1-H7 numbering retired
- [x] #20 runs.md rewritten for three conditions: 3,290 -> 6,046 words, two-arm vocabulary and L1/L3/L4 ablation retired
- [x] #21 requirements.md translated and restructured as a compliance checklist: 6,006 -> 6,025 words, the seven-chapter conflict corrected
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Progress 7 XI 2026, sixteen documents done: corpus 6,723; experiment 4,219; scope-and-character 7,669; edge-of-scope 7,551; statistics 6,662; arms-and-validation 6,455; gap-and-literature 6,063; titles 6,012; what-we-study 6,493; aim-and-contributions 6,011; correctness 6,432; harness 6,406; tool-surface 6,091; structure 6,043; runs 6,046; requirements 6,025. requirements.md is the only document in the queue that was NOT pruned. It is a transcript of three sources - the faculty's degree regulations, its qualification criteria, four competitions' rules - and a rule one must comply with is not an argument that can be tightened, so the word count was held at 6,006 +/- 20 by construction and the work went into form and into one contradiction. Form: English, fourteen sections, and every requirement carries a status (met / conditional / not met / will be met by an act of writing), which turns a transcript into something one can work through; the consolidated seventeen-row checklist at section 10 names, for each row, who can close it. Contradiction: the document asserted a structural CONFLICT - seven planned chapters against the frame's "five parts" - and had resolved it by merging methods, instrument and execution into one 26-30 page chapter. The frame does not say that. It puts two to four main-part chapters BETWEEN the third introductory chapter and the summary, so three introductory + three main-part (4 instrument, 5 execution, 6 results) + one summary = seven chapters with the main part at three, inside the permitted range. The earlier resolution looked like a compromise; in fact it dissolved C1 into procedure and left a 26-30 page chapter with nowhere to put the deviations register. The correction is recorded in section 5 with the arithmetic, and the merge of methods+instrument+execution is rejected there by argument rather than dropped. What the document now owns that nothing else does: the three decisions that are not mine and are therefore first (the reviewer must hold a habilitation if the supervisor is a doctor; the language of the thesis, where a foreign language needs a Vice-Dean application but leaves a Polish title, Polish figure captions and a Polish abstract; the grade that gates the SGP competition); the administrative rules that nonetheless bind the TEXT, including the distinction between a substantive and an editorial change of topic, which is exactly why the retired fourth condition (a REST arm) is not "just another arm" but a change of subject; the abstract as a deliverable of its own (<= 4,000 characters including spaces, two framings in two vocabularies, keywords, written last); appendices A-G numbered with every one cited, D as the proof of symmetry and G as the answer to "could it be your harness?"; the template decision (Markdown to DOCX through a reference template, built before chapter 4 is drafted, not after); the bibliography conversion as a script over 67 entries; the round of documents with its two purely administrative failure modes (a PDF over 30 MB because result figures were rasterised, and a statement plus four 4.5 x 6.5 cm photos seven working days before); the four sentences the defence must be able to say; and the correction that the thirteen family-C cards are not padding but one family carrying three obligations at once - an SGP qualification, the moderator of H3, and the counter-case in chapter 6 where the catalogue loses by construction. Also corrected: the frame's governing assumption that a specific AI faculty rule exists is false as far as the sources go - AI rules are missing from all three, so they must be obtained and quoted in the methods chapter, which is now a row of its own. Outside the queue: thesis/literature/literature.bib's header comment claimed 38 entries while the file holds 67 (grep -c "^@"); corrected. Sixteen of seventeen ticked, doc-8 now holds sixteen sections. NEXT: thesis/concept-dictionary.md, 3,299 words, status frozen - the last document and the only one that may be left alone: its retired rows are already marked as former terms with their successors, but its "gdzie" column still points at section numbers from before the merged seven-chapter structure, so the remaining work is a reconciliation pass over the references, not a rewrite. Done in the same pass, outside the seventeen: concept-dictionary.md (3,655 words, still frozen, still Polish) - the "gdzie" column had 110 cells pointing at section numbers from before the one table of contents. Reconciled by separating what is certain from what is temporary: the CHAPTER number is certain (1-7 identical in thesis/draft/thesis-draft-v0.md and thesis/draft/structure.md, so 3 = materials and methods, 4 = instrument, 6 = results) and is now the anchor of each entry; the subsection number survives in parentheses, marked provisional, to be set at writing time - better a verified anchor plus an admittedly provisional detail than a precise-looking number that is wrong. The header's claim that the dictionary becomes "appendix B" was also wrong: appendices A-G are fixed and none is a glossary, so the dictionary is now described as what it is - a writing aid that feeds definitions in chapter 2, the correctness vocabulary in chapter 3 and the predicate dictionary in chapter 4, and which only becomes an appendix if the thesis is written in Polish, a decision still open. Section 9 of the dictionary was rewritten from "how to paste it into the thesis" to those four destinations. thesis/README.md corrected in the same pass, because it claimed every frozen document carries no updated_date while this one now does.

Status 7 XI 2026: 17 of 21 criteria ticked and the prunes are finished, but the task stays open on the four repo-wide criteria, which are audits rather than documents. #4 is checked by arithmetic and holds: all sixteen pruned documents sit between 6,011 and 7,669 words, inside the 6,000-8,000 band, and none needed splitting. #2 is checked by the cut tables in doc-8. #3 holds for the sixteen documents with a section in doc-8. #1 does NOT hold literally: corpus, experiment, scope-and-character, edge-of-scope, statistics, arms-and-validation, gap-and-literature, titles, what-we-study and aim-and-contributions end with a five-line closing section, but correctness, harness, tool-surface, structure, runs and requirements end with their cut log's 'added while pruning' paragraph, which is a record of the edit rather than a summary a chapter can lift. Closing #1 means appending a five-line summary to those six - a small, well-defined pass, not a rewrite.
<!-- SECTION:NOTES:END -->
