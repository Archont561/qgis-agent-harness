---
id: TASK-20
title: Translate the remaining thesis notes into English
status: Done
assignee: []
created_date: '2026-11-07T20:10:00Z'
updated_date: '2026-11-09T00:00:00Z'
labels:
  - thesis
milestone: m-3
dependencies:
  - TASK-21
references:
  - thesis/README.md
documentation:
  - backlog/docs/doc-1 - Terminology-of-the-thesis.md
priority: high
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The apparatus (README, backlog, docs/) is English, and so is the draft; 66 working notes, the four konkursy conversions and the three analysis scripts are still Polish, which makes every quote in an English chapter a translation of a translation. Work proceeds by batches of 8-9k words, largest first, with only the glossary and the concept dictionary left in Polish on purpose.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Every file in the repo is in English except thesis/glossary-of-terms.md and thesis/concept-dictionary.md (Polish strings quoted as subject matter, e.g. the title candidates in thesis/draft/titles.md, stay)
- [x] #2 File names stay English; no --doc/--ref path changes during the translation
- [x] #3 Every batch ends with alint 27/27, qa clean and backlog doctor clean
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Progress 7 XI 2026 — the queue is empty; every thesis document outside the two registers is now English. This pass closed the last ten files, which the prune had left in Polish because they are not part of the seventeen: writing/key-concepts (2,041 -> 2,460), writing/plan (1,528 -> 1,931), writing/defence (3,008 -> 3,710), draft/draft-minimal (1,690 -> 2,125), competitions/README (469 -> 700), competitions/competition-verification (1,958 -> 2,378), competitions/historical-editions (1,828 -> 2,326), competitions/pti-kpm-rules (989 -> 1,203), competitions/sgp-kd-rules-2023 (2,024 -> 2,324), competitions/marpit-geoinformation-award-2020 (3,313 -> 3,144), and the Polish headnote of literature/search-review. Translation was not transcription: four of these documents were carrying a design generation that the pruned ones had already retired, and shipping them in English would have made the stale numbers look authoritative.

What was corrected in the same pass. writing/plan still ran on 40 tasks x 8 repetitions = 640 runs, a 1,300-1,500 run sweep, an L4 ladder, a 180-run model layer, H5 and the 2 x 2 diagram; it now runs on 80 x 4 = 960 with three conditions K / N1 / N4, an MDE of 14.0 pp, and a cut list that names the 48-run product appendix and 64 x 4 = 768 runs at 15.6 pp as the fallbacks. writing/defence quoted an MDE of 9.3 pp, 40 tasks, 640 runs, ED/RRR/T2V/CVS and H4b with its TOST; it now quotes 14.0 pp, 80 tasks, 960 runs, ICC 0.661 with the design effect turning 960 runs into roughly 320 independent units' worth of information, and the live ledger H1 / H2 / H3 with D1-D4 - TOST stays in the test table as a concept the committee may ask about, with an explicit line that this design runs no equivalence test and instead reports undecided results below the MDE. draft/draft-minimal carried L1 / L3 / L4, H1-H5 and a correction over four hypotheses; it now carries the same ledger as arms-and-validation. key-concepts and defence had 30-turn and 25-turn budgets against each other; both now say 25 turns, 10 minutes, one token budget, matching experiment.md A4 and runs.md. competition-verification said "diagram 2 x 2" and "300+ runs" for a REST arm; it now says the expressible-share figure and about 320 runs, and keeps the reason the REST arm is retired - a change of topic, not another arm.

Two editorial decisions recorded in the files themselves. (1) The three rulebook conversions and the competitions README are frozen records of external Polish regulations, so their translation is for reading: every § and annex number is unchanged, and each file now says in its headnote that anything quoted in the thesis, an application or a complaint is quoted from the Polish original. (2) The Minister's Award ordinance reproduced four application forms identical apart from their fields; they are now one translated template plus a table of the differences, stated in the headnote rather than silently dropped.

Kept in Polish on purpose: thesis/glossary-of-terms.md and thesis/concept-dictionary.md, both status frozen, because they are the English-Polish registers - translating a glossary into the language it translates from destroys it. Polish strings that survive inside English files are subject matter: the laureates' thesis titles in competitions/historical-editions (each with an English gloss in brackets), the addresses and institution names in the ordinance, and the Polish title candidates in thesis/draft/titles.md.

Verified: alint 28/28, qa clean, test 14 passed, backlog doctor clean, no Cyrillic homoglyphs outside the two registers, and no file under thesis/ carrying language: pl except the two registers.
<!-- SECTION:NOTES:END -->
