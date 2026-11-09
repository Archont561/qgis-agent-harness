---
id: doc-8
title: 'Backlog pruning: cut tests K1-K6 and what was cut'
type: guide
created_date: '2026-11-07T19:57:00Z'
updated_date: '2026-11-07T22:31:00Z'
---
---
id: doc-8
title: 'Backlog pruning: cut tests K1-K6 and what was cut'
type: guide
created_date: '2026-11-07T19:57:00Z'
updated_date: '2026-11-07T21:07:00Z'
---
A task list that nobody pruned stops being a task list and becomes a table of contents. This document keeps the cut tests and the full register of what is **deliberately absent** from the backlog - so that a cut item does not come back in two weeks as a "missing task".

## Six tests, in this order

| # | Test | Control question |
|--:|---|---|
| K1 | Is this work, or is it already written down? | if a file in `thesis/` already settles the matter, a backlog entry only duplicates it |
| K2 | Can it be closed now? | an item waiting for results will rot for months and teach you to ignore the board |
| K3 | Does it have an AC that cannot be faked? | "write a chapter" is not an AC; "every figure has a scale" is |
| K4 | Is it part of another item? | two tasks about the same document = the same status twice |
| K5 | Does it depend on something that does not exist? | a second coder, institutional access - those are conditions, not tasks |
| K6 | Is it about this repository? | fixing files in another project's archive is not work on this thesis |

## What was cut and why (register)

| Cut | Test | Reason |
|---|:--:|---|
| "Freeze N and the analysis plan" | K4 | same document and same act of freezing as closing the numbers -> absorbed as the fifth AC |
| "Implement the `experiment.yml` stages" | K4 | pipeline stages are part of the harness (TASK-7) -> absorbed as AC |
| "Fix ID errors and snowballing" | K6 | wrong arXiv IDs sit in **another project's** archive; the rest reduces to one AC in the literature review |
| "Check Scopus access" | K5 | a condition, not work: either access exists, or it becomes a sentence in the limitations |
| "Abstract of at most 4000 characters" | K2 | cannot be written honestly before the results; returns after the main series |
| "Editorial audit: scales, quotations" | K2, K3 | there is nothing to audit yet; it is already a checklist in `writing/requirements.md` §2 |
| "70 x 100 poster" | K2 | half a day of work after the defence, today it hangs without content |
| decision "Title T0" | K1 | the title is approved externally and described in `draft/titles.md` with a rationale |
| decision "Terminology correction" | K1 | the rule lives in `glossary-of-terms.md` and in `doc-1`; a decision enforced by a document needs no entry |
| decision "No competition version" | K1 | a preference derivable from `competitions/competition-verification.md` §3.C |
| document: `design/harness.md` | K4 | an SOP for a single task -> `--doc` on TASK-12 |
| document: `writing/defence.md` | K1 | material for the diploma exam, not project work |

**Kept despite doubts:** coding the expressible share (kappa needs a second coder - that is, a human; the risk is recorded in the AC as a 20 % audit by the supervisor) and the literature review as a set of positions (the only §V requirement a checklist cannot replace).

## Three rules: what never enters the backlog

1. **Prose** stays in `thesis/` in place and is only linked (`--doc`/`--ref`) - see decision-7.
2. **Raw material** (`.bib`, transcripts, JSON dumps, PDFs) never enters `backlog/`; it is material, not work.
3. **Generated files** (offline transport, `pixi.lock`, CI artefacts) enter nowhere - they have their own `init --check`.

## A limitation worth knowing

`backlog decision create` accepts a title and a status only - there is no field for content. So a decision's rationale goes into the title after the word "because", and a `decision-N` -> `thesis/*.md` mapping does not exist as a file. If decisions are to be citable in the thesis, they have to be woven into chapter 5 (`TASK-13`) rather than referenced from the backlog.

## Register of pruned thesis text (TASK-21)

The merge of 7 XI 2026 turned 84 flat notes into 17 documents; pruning them removes text that two design generations had put side by side. Per document, the cuts go here, so that a deleted paragraph does not come back as a "missing consideration".

### `thesis/design/corpus.md` (13,379 -> 6,723 words, 7 sources)

| Cut | Source note | Reason |
|---|---|---|
| the 40-task count as the corpus size | `tasks-40` | superseded by `d-2` (80 cards); the 40 survive as the seed catalogue with its tables intact |
| the `min_surface` column (5/15/30 tools) | `tasks-40`, `mvp-what-task-and-tool-counts-measure` | the tool-count ladder is retired; the nine operations are fixed and the successor moderator is the expressible share (`TASK-4`) |
| ITT versus PP, random catalogues, whitelist ablation, packages M0-M3 | `mvp-what-task-and-tool-counts-measure` | all of it is tool-surface material and already lives in `design/tool-surface.md`; a second copy is how two different ladders end up in one thesis |
| alpha = 0.0083 and the Bonferroni/6 tables | `task-count-decision` | the live design has one confirmatory test at 0.05 with Holm for the rest |
| the 1,218-run budget variants A/B/C and the 50-task main series | `task-count-decision` | the series is 960 runs on 80 tasks; what survived is the shape of the trade-off, not its old arithmetic |
| "two arms, MCP versus code" framing | `selection-objection-how-to-answer`, `mvp-what-...` | three arms K/N1/N4; the objection answer is now written against the arms that exist |
| twin-template power arithmetic at N = 40, r = 8 | `paired-templates` | recomputed at the live cell (N = 80, r = 4, tau = 10 pp -> 14.0 pp); the mechanism survived, the numbers did not |
| hypotheses H3/H4a/H4b and the L1-L4 mapping | several | one owner per list: `design/arms-and-validation.md` |

Kept through all seven notes: the sourcing rule and the 70/20/10 split, the benchmark table, the admission rules, the seed catalogue, the two domain measurements (GIS SE tags, GIS&T BoK), the tau-floor argument, the unit-of-inference rule, the twins caveat and the five objection-control pairs.

### `thesis/design/experiment.md` (11,967 -> 4,219 words, 5 sources)

| Cut | Source note | Reason |
|---|---|---|
| arms A1-A9 (tool ladder L1-L4, codegen+gate, surface+gate, adversarial, meta) | `experiment` | the live design has three conditions in an **enforcement** ladder, not nine in a tool-count ladder; the tool-count ladder retired together with `min_surface` |
| claims V2-V7 | `experiment` | superseded by H1-H3 plus the three claims that survive any result; one owner for hypotheses (`design/arms-and-validation.md`) |
| two front-ends (opencode, goose) as a crossed factor | `experiment` | one pinned harness per decision-4; crossing it multiplies the series for a claim the thesis does not make |
| the 50-task corpus and the 1,416 / 4,768-run matrices | `experiment`, `experiment-full` | 80 tasks and 960 runs per decision-2 |
| simulated chapter-6 results, hypothesis by hypothesis (H1-H7), five seeds | `experiment-full` | the simulation and its artefacts were removed on 7 XI 2026; W1-W6 fix the interpretations without inventing numbers |
| "six things without which it is not an experiment" as its own section | `experiment-shape` | it was a summary of §5, §6 and §13 |
| the protocol-evaluation essay and its bibliography stub | `evaluation-design` | the argument belongs to `framing/gap-and-literature.md`; one bibliography in `literature/literature.bib` |

Kept: the twelve-step procedure, `result.json` written last, "never drop a run", the thirteen-field register with `detected_by`, the metric definitions, both taxonomies, the kappa audit, `guard_information subset agent_information`, the equivalence assumptions with their consequences, pilot rules R1-R3, W1-W6, and the threats table.

### Files removed by instruction (7 XI 2026)

`experiment/PIPELINE.md`, `experiment/runs.csv`, `experiment/simulated_results.json`, `experiment/scripts/` (analyse, check_pingouin, power_mde, simulate_results). Nothing measured had been produced by them; the pipeline stages moved into `thesis/design/runs.md` and `thesis/design/experiment.md` section 5, the register contract into `TASK-16`, and the power model closed form into `thesis/design/corpus.md` section 7.2. References were rewritten in 13 files: `docs/tests.md`, `.github/workflows/experiment.yml`, `ruff.toml` (three per-file ignores dropped), `experiment/pyproject.toml`, `docs/environments.md`, `experiment/tasks/README.md`, `experiment/README.md`, and seven thesis documents.
### `thesis/framing/scope-and-character.md` (9,541 -> 7,669 words, 7 sources)

| Cut | Source note | Reason |
|---|---|---|
| the item-by-item cut of the 2,800-run design (arms S1/S2/S3, meta-tool, hybrid, two models, two front-ends, 12 anchored reproductions) | `scope-decision` | that design does not exist any more; the rule survived (cut arms, not tasks) together with the arithmetic behind it |
| the "six decisions grew the plan to 3,566 runs" audit and its three budget paths A/B/C | `scope-decision` | it audited a design the next round of decisions replaced wholesale; the freeze rule survives as one sentence |
| the V1-V7 claim ledger | `what-to-focus-on` | renumbered onto H1-H3 plus four descriptive claims; two numberings of the same claim is how one thesis ends up with two reference systems |
| the "four possible theses" A/B/C/D table | `is-this-needed` | the choice is recorded in d-1 and d-2; the pivot criteria survive |
| the "make the model an axis" recommendation | `geoai-trend` | contradicts the scope decision (one model); kept as a recorded disagreement with the three-part defence that replaces it |
| the plain-language telling as its own section | `explain-like-im-ten` | its content became the openings of sections 1, 2.2 and 5.2; a second whole-thesis telling in one document invites the two to drift |
| "eight domains of ten", carried over from the draft | several | contradicts d-3: family is the selection axis, domain a descriptive label |

Kept: the cost arithmetic, the in/out ledger, the abstract test, the add-back order, "do not merge N1 and N4", the needed/not-needed split, the obsolescence risks, the decision test, the pivot criteria, the degree-fit objections and answers, the reframing sentence, the three degree additions, the scorecard, the whole of the thesis-character section (regulation paragraphs, point-by-point fit, the ready experiment description, the defence sentence), the claim ledger with falsification conditions, the novelty table, the critique table, and the GeoAI positioning.
### `thesis/framing/edge-of-scope.md` (9,126 -> 7,551 words, 6 sources)

| Cut | Source note | Reason |
|---|---|---|
| the whole AI-MCP-GIS primer (overview, MCP in five sentences, landscape table, Polish glossary, reading order) | `ai-mcp-gis-guide.md` | every part already exists where it is maintained: vocabulary in `thesis/glossary-of-terms.md`, landscape and G1-G5 in `framing/gap-and-literature.md`, OGC API - Processes positioning in `scope-and-character.md`. Two copies of a glossary is how two glossaries disagree |
| the "what is known / not known" list as its own section | `ai-mcp-gis-guide.md` | a subset of the gap table in `gap-and-literature.md`; the one gap it added is now section 4 of the document |
| the 2x2 factorial, its fourth arm, the 600- and 2,400-run arithmetic | `schema-gating.md` | the live design is three conditions and 960 runs; the arithmetic described a design that does not exist. The reasoning survives: the confound is named and the claim is narrowed |
| the security (G5) extension, ADV-01..05 under two gating levels | `schema-gating.md` | not in the live design; named as future work instead |
| the same QGIS justification copied three times | `substrate-choice.md`, `environment-generalisability.md` | one paragraph, one place |
| "two things to do this week" | `substrate-choice.md` | week-scale to-dos belong in `writing/plan.md` |
| stale arithmetic (four agents, 50 tasks, 1,218 runs) | several | contradicts d-2/d-3 and the live design; replaced, not carried |

Kept: the ten non-claims and the claim-is-subset-of-evidence rule, the seven-property table, the three domain profiles, the transfer ledger, the substrate requirements, the alternative-scoring table, the layer decision, the cheaper ladder R1/R2/R4/R5, the threat table, the reviewer answers, the three regimes, the orthogonality argument, the interpretation rules, the tautology trap and its metrics, the four limits, the product-not-sum argument, the four factors and scorecard, the three memorable sentences.
### `thesis/analysis/statistics.md` (8,088 -> 6,662 words, 6 sources)

| Cut | Source note | Reason |
|---|---|---|
| the 40 x 8 design, its 640 runs, the MDE table 0.574-0.880 and the 40 x 16 / 40 x 60 recommendations | `hypothesis-testing`, `what-is-mde`, `sample-size` | the live design is 80 tasks at r = 4, 960 runs, MDE 14.0 pp at tau = 10; every number was recomputed, not carried |
| the "MDE 20-25 pp at 50 tasks" figure and the alpha = 0.0083 (Bonferroni/6) discussion | `hypothesis-testing`, `sample-size` | retired generation; the live hierarchy spends 0.05 once and Holm on a family of two |
| TOST, the +/-20 pp margin and its sample-size table | `hypothesis-testing`, `sample-size` | the equivalence claim existed to rescue the 2x2 with a gated-code cell, and that cell is not in the design; a test with no corresponding contrast is a rule without a subject |
| the 2x2 interaction cost analysis ("~140 tasks for a 20 pp interaction") | `sample-size` | no interaction contrast in the live design, only the depth curve and the expressible-share moderator |
| the tool ladder L1-L4 and 5 random 100-tool catalogues | `sample-size` | retired with `min_surface`; the surviving control is the anonymised catalogue in `corpus.md` |
| the H1-H7 hypothesis list with per-hypothesis DVs | `hypothesis-testing` | live claims are H1-H3 + D1-D4 with one owner (`arms-and-validation.md`); two numberings end in two reference systems |
| "tasks needed for 80 % power" tables at alpha = 0.0083 | `sample-size` | superseded by the closed form with tau, which is what the design uses |
| the model sensitivity control (+180) and platform invariance control (+60) as plan items | `confounders` | neither is in the 960-run series; both survive as one-sentence limitations with their cost named |
| two front-ends as a crossed factor and the affordance table as a comparison | `confounders` | one pinned harness (d-4); the table survives as an admission criterion for that harness |
| the six-subsection `pixi add` vs `--pypi` investigation | `pingouin` | one paragraph survives (conda-forge, BLAS duplication in a QGIS container); the rest is recorded in `pixi.toml` |
| the 4 769-run manifest evidence, report excerpts, exclusion artefacts | `pingouin`, `analysis-automation` | the pre-results scaffolding was removed on 7 XI 2026; what remains is the contract for TASK-12 and TASK-16 |

Kept: the five levels, G2 with its negative control, the DEFF arithmetic (ICC 0.661, r = 4 -> 3.0), the hierarchy and test budget, the per-claim table with falsifiers, the closed-form MDE with the tau sensitivity and per-cell resolution table, the argument against 5 pp and the four free levers, the five sensitivity analyses, the software split with the contrast trap and estimand note, the automation boundary with the case catalogue, and the confounder register.

Stale numbers fixed outside this file when their documents were pruned - all three now done: `framing/aim-and-contributions.md` (MDE 20-25 pp, 50 tasks, alpha 0.0083 -> 14.0 pp, 80 tasks, alpha 0.05), `design/tool-surface.md` (~20-25 pp -> 14.0 pp at tau = 10), `writing/plan.md` (the "back to 40 x 8" fallback -> the series stays at 80 x 4).
### `thesis/design/arms-and-validation.md` (7,530 -> 6,455 words, 4 sources)

Now the single owner of the claim ledger: H1, H2, H3 with inferential weight, D1-D3 descriptive, D4 a precondition.

| Cut | Source note | Reason |
|---|---|---|
| the H1-H7 hypothesis table with per-hypothesis DVs | `hypotheses-and-factors` | live ledger is H1-H3 + D1-D4; H4a/H4b (2x2, TOST), H5 (ED classes), H6 (cost), H7 (signatures) were re-expressed as D1-D3, not deleted, because a descriptive claim needs no alpha; two numberings end in two reference systems |
| the L1-L4 tool ladder and `min_surface` as a factor | `hypotheses-and-factors` | retired with `min_surface` (`corpus.md` §11); replaced by enforcement depth on a fixed surface |
| the `gate` factor with `none`/`gate` levels and the 2x2 with `codegen-gated` | `hypotheses-and-factors`, `validation-in-the-code-arm` | the live design is three conditions in a depth ladder, not a factorial; the reasoning survives in `edge-of-scope.md` §4.2 with its cost to the claim |
| conditions C0 (no checking instruction) and C2 (no reference values) | `validation-in-the-code-arm` | C1, the identical checking instruction, IS the design and was adopted; C0 is the straw man the design avoids by construction, so running it measures the straw man; C2 violates A3 information parity and changes the thesis into a question about the model's domain knowledge |
| the four-condition arithmetic (1 280 runs, MDE 10.3 / 14 pp, r = 8) | `validation-standardisation`, `what-a-tool-can-validate` | describes a series not being run: 960 runs, three conditions, r = 4 |
| the fourth surface `L5` as a separate arm | `what-a-tool-can-validate` | it became N4; a contract-bound surface is not an extra arm but the extended catalogue condition, and arm-ifying it would have duplicated the design |
| the simulated variance evidence (0.2114/0.2121/0.2118) and the class-repeatability table (0.65 vs 0.37) | `validation-standardisation` | the argument survives as one sentence (variance of a binary outcome is a function of its mean); the numbers came from the pre-results scaffolding removed 7 XI 2026 and are not reproducible from the repository |
| the nine-entry glossary (distractor, min_surface, T2V, REF, ED) | `hypotheses-and-factors` | terms are defined where used; a second glossary drifts from `glossary-of-terms.md` |
| the duplicate "how it lands in the thesis" list | `hypotheses-and-factors` | one map, in section 8 |

Kept: the no-direction + one-falsifier rule, the durability order, the three condition definitions with the three distinctions that keep them apart (gate is not the oracle; N1 already validates; a rejection is not a repair), the family and tier operationalisations, the expressible-share codebook with its coding procedure and dose model, the frozen-factor table and the two designs not run, the SPE with its four properties, the three-error example, P-I/P-II/P-III, the honest recount of 3-4 of 8 CRS classes, the contract-bound surface with the information-closure argument, what remains when nothing is expressible, the self-correction literature with numbers and caveat, S4/S4b and four-valued `detected_by`, the falsification condition, and the three counterarguments.

Also fixed: `design/runs.md` referenced H4a/H4b, H6 and H7 in its logging table; the cross-references now point at H2, D1, D2 and D3.
### `thesis/framing/gap-and-literature.md` (7,505 -> 6,063 words, 4 sources)

| Cut | Source note | Reason |
|---|---|---|
| the PB1-PB9 question table with its own DVs (TSR, OQS, PCS, PEA, ITS, ED, ADV) | `gap-and-rqs` | written for a four-agent, 1,800-run design; questions now map one-to-one onto the live ledger as SQ1-SQ5, so they cannot be mistaken for a second hypothesis list |
| "38 references" as a corpus count and the per-cluster `n` column | `gap-and-rqs`, `literature-brief` | counts were already inconsistent in three places (38 / 65 / 67); the bibliography is the count |
| the six-layer gap list plus the six "truly undecided" items N1-N8 | `gap-and-rqs`, `literature-mcp-vs-code` | two lists of the same gap in two languages with two numberings; merged into G1-G5 with G3 marked closed and G5 marked out of scope |
| the tool-*size* gap (5/15/30/50) | both | the tool-count ladder is retired; the manipulation is enforcement depth, and G2 was rewritten to say so rather than to keep a gap the design no longer fills |
| the two housekeeping items describing "2 front-ends x 2 models" and the S1/S2/S3 ladder | `literature-brief` | recorded a design generation that no longer exists; the instruction to update the RQ wording is discharged by section 6 |
| the three sharpened title candidates | `gap-and-rqs` | titles belong in `draft/titles.md`, the owner of that question |
| the Polish seven-item redesign programme | `literature-mcp-vs-code` | five of the seven items are now the design and are stated where they live; two (second model, random catalogues) are further work |
| the "two models of different capability" requirement, stated three times | several | d-2 fixes one model; the model x interface interaction is the first item of further work |
| the origin-of-terms class boilerplate and the 40-concept D inventory | `origin-of-terms` | classes in one line each; the D list is a vocabulary by field rather than a 40-row table |
| the "38 -> 65 -> 67 entries" narrative | `literature-brief` | three incompatible counts in one document; one line now, plus what is still missing |

Added while pruning, because the cut had removed a claim's only home: section 3.1 (repair as mediator, the context cost of long GIS schemas) and the paragraph on why the two ecosystems cannot be stacked, plus the "what each neighbour would predict" list in section 5 and two rows in section 7.

Kept: the six-stream map with the two asymmetries, the canon-to-use table, the empty-cell quadrant, G1-G5, the evidence against the thesis with its numbers and three consequences, the six neighbours with separating sentences, RQ0 and SQ1-SQ5 mapped to the ledger with four framing rules, the claims the literature forbids, the full term provenance with three shifted meanings, and the citation-hygiene obligations.

Open, and recorded in section 9: nine works argued from but absent from `literature.bib` (huang2024, kamoi, tyen, codeact, cemcp, mcp_atlas, mcpevol, plus the domain-specific MCP benchmarks). TASK-10 owns the additions.
### `thesis/draft/titles.md` (7,482 -> 6,012 words, 4 sources)

| Cut | Source note | Reason |
|---|---|---|
| titles T0-T4 as a numbered candidate set and the "your original title, assessed" section | `title`, `alternative-titles-and-scopes` | the topic is approved, so the choice is between repairs of one title, not between titles; the six observations of the original assessment survive as the diagnosis |
| the recommended "Same engine, different interface..." title and its Polish version | `title` | built for two arms and a tool-surface-size ladder, neither of which exists; content survives as variant W3 and as the abstract wording |
| eight alternative *scopes* S1-S8 with run counts, MDEs and week estimates | `alternative-titles-and-scopes` | eight other theses; the scope is decided, and the S1 enforcement ablation was absorbed into the live design as N1 vs N4 |
| the "spin-off in this order" publication plan | `alternative-titles-and-scopes` | a publication plan, not a title question; the same-cards-same-oracle rule survives in `corpus.md` §10 |
| the 0-10 scoring table across six criteria for ten scopes | `scientific-evaluation` | scored scopes that no longer exist; the structural finding (family C is a qualification condition) and the small-spread observation survive |
| the classification audit rows for T1-T4 and S1-S8 | `scientific-evaluation` | replaced by one table mapping the §III.9 elements onto the live design |
| the five "things to change in the plan" | `scientific-evaluation` | four have been done (third condition supplies the gradient, identical checking instruction frozen, instrument work is a subsection not a title, family C is a condition); the fifth survives as the College annex |
| duplicate word-keep/lose and practical-check lists | `title` | one copy each |

Added while pruning, because the cut removed the place where the claim lived: section 1.1 (the approved title against the five tests), 2.1 (what the hybrid condition is and why excluding it is a scope decision rather than an apology), 3.1 (translation decisions for the PL/EN pair), 3.2 (what the chosen title trades away and what chapter 1 must therefore carry), the Polish version of the three sentences to the supervisor with three situations and three answers, 7.2 (two classification risks the title creates and one it cannot fix), the competition-audience table, and the keyword line.

Kept: the five tests with the gap-to-title table (G5 deliberately absent), the diagnosis of the approved title and its three readings, W0-W4 with the buys-matrix, the recommendation and the re-approval question, the five mitigations for a frozen title, the five prohibitions, the alternates and word lists for abstracts and talks, the classify-do-not-score distinction with the §III.9 element map, the College annex list, and family C as a qualification condition.
### `thesis/framing/what-we-study.md` (7,413 -> 6,493 words, 5 sources)

| Cut | Source note | Reason |
|---|---|---|
| the "four measurable quantities" table with H1/H2/H5/H6 numbering | `what-exactly-we-study` | mapped onto a retired hypothesis list; content survives re-expressed against the live ledger |
| the thesis statement built on "a 2x2 comparison and an equivalence test" | `what-exactly-we-study` | the 2x2 with gated code and its TOST are not in the design; replaced by a weaker and true sentence about what P3 can claim |
| the K1-K4 contrast ladder (whitelisted code condition, five random catalogues, curation interaction) | `comparison-basis-codegen-mcp` | three of four contrasts are not conditions in the live design; the ladder is redrawn against K/N1/N4 and the two missing contrasts are marked as missing |
| the eight-step computation list with df = 39, "MDE 8.6 pp at r = 32" and 40-task arithmetic | `comparison-basis-codegen-mcp` | retired 40 x 8 generation; `statistics.md` owns the arithmetic. Four points that are properties of the basis remain, with live numbers |
| the 40-line JSON-RPC and tool-description examples, the message-type catalogue, the full primitive table | `mcp-protocol-shape` | a design note is not the specification; the two facts that carry the argument, the version pinning and five decisions are kept |
| the sixteen-row mapping of protocol features onto gates | `mcp-protocol-shape` | compressed to the seven-gate table and the claim "two and a half of seven" |
| the version chronology essay and risk forecast in full | `mcp-protocol-shape` | four dates in one sentence; the consequence is one paragraph |
| the 52North novelty discussion as a risk | `mcp-rest-ogc-codegen` | two lines, not a section: the bridge existing does not threaten a thesis built on a frozen surface and artefact scoring |
| the three "levels of literature" with eleven citations | `mcp-rest-ogc-codegen` | literature-review material; belongs to `gap-and-literature.md`. Two citations survive because they are load-bearing for the no-third-arm argument |
| the industry benchmark numbers (99.84 / 99.71 / 99.52 %) | `mcp-rest-ogc-codegen` | not evidence by their own admission |
| the facade section beyond four rows, and "what not to do" as prose | `mcp-ogc-facade` | four rows plus three rules |

Kept: the three-level decomposition with the "MCP is not REST" correction, the four-component answer to "does it pay off" with the decision table, the one-paragraph basis with ceteris paribus and the error-channel note, A1-A5 with consequences, four advantages and four limits of artefact scoring, the three layers, the honest contrast ladder, the run record with three auditability hashes, four computation properties, the worked A-07 example across three conditions, six limits, the no-third-arm argument with V0/V1/V2 and the async difference, the two protocol facts with MRTR and five decisions, and the facade topologies with the generated-catalogue control.
### `thesis/framing/aim-and-contributions.md` (7,207 -> 6,011 words, 5 sources)

| Cut | Source note | Reason |
|---|---|---|
| the 2x2 with gated code and the equivalence test as the *main* contribution | `novelty-and-contributions`, `scientific-contribution` | the cell is not in the design; the enforcement claim is narrowed to the N1 -> N4 contrast and the missing cell is named wherever it bounds an interpretation |
| "MDE 20-25 pp at 50 tasks, alpha = 0.0083", repeated in three sections | `scientific-contribution`, `thesis-aim` | three generations stale. Live: 80 tasks, r = 4, MDE 14.0 pp at tau = 10, one confirmatory test at alpha = 0.05 with Holm over a family of two |
| "1 218 runs", "two models, one host", "3-5 repetitions", "50 tasks" | several | retired design generation; 960 runs, one model, one harness, r = 4 |
| the L1-L4 ladder as the surface-size manipulation | `novelty-and-contributions`, `scientific-contribution` | retired with `min_surface`; the manipulation is enforcement depth on a fixed surface |
| the hypothesis-by-hypothesis table mapping H1-H7 onto contributions | `scientific-contribution` | a second numbering of the ledger; the six pre-registered outcomes serve the same purpose and are followable |
| the "four cells of the 2x2, four conclusions" table | `implications` | replaced by the six outcomes, the design's own vocabulary |
| the "two front-ends and two models as a factor" defence answer | `novelty-and-contributions` | one harness, one model (d-2, d-4); pretending otherwise is the one place a reviewer could catch an overclaim |
| the positioning taxonomy as a *contribution* | `novelty-and-contributions` | chapter 2 material; as a contribution it is an unmeasured table |
| the title options section | `novelty-and-contributions` | titles have an owner (`draft/titles.md`) |
| eleven paragraphs of impact prose | `impact-on-ai-gis-integration` | became four numbered theses with conditions plus four predictions marked as predictions |

Added while pruning: 7.1 (frame vs claim with the five-dimension taxonomy), 9.2 (three defence questions), 11.1 (integration relocates expertise), and the note on N6, the substitution slice.

Kept: the one-sentence aim with three measurable components, five specific aims with live measures and six non-aims, three kinds of aim, the achievement checklist, aim-statement-claim-title, the three contribution tests with reviewer attacks, four candidates ranked by durability with the absorbed downgrade, C1-C3 with the anti-overclaim formula, the chapter map, the implication vector with six outcomes, what is not settled, four theses with conditions, the policy rule with its alarm and three integration levels, and the predictions.

### `thesis/design/correctness.md` (6,858 -> 6,432 words, 4 sources)

The smallest cut of the seventeen, and the reason is worth recording: the four source notes asked four different questions (what provides correctness; whether an error ends in a file; whether a bad CRS is a bad parameter; what may be claimed), so the merged document restated almost nothing across sections. What it did carry was retired design and two competing numberings.

| Cut | Source note | Reason |
|---|---|---|
| the four-arm table A-D (L1 / L3 / L4 / code) with "1,280 runs, ~6.7 weeks" | `correctness-what-ensures-it.md` 7 | retired design generation; the ablation is N1 -> N4 inside K / N1 / N4, 80 tasks, r = 4, 960 runs (d-1, d-2) |
| two power tables (N at r = 8 / r = 16 for seven values of delta; the base-error x catchable-share grid) | `what-i-can-claim-about-mcp-vs-codegen.md` 4 | a retired formula and repetitions the design does not use; live MDE 14.0 pp at tau = 10 lives in `analysis/statistics.md` 5, and the arithmetic must not exist twice with two answers |
| the four-branch pilot tree as a table, the local labels C-a / C-b / C-c, and G1-G4 for the four validation gaps | same 3, 5; `correctness-what-ensures-it.md` 4 | three second numberings - of the outcomes (now W1-W6, prose), of the gap register (G1-G5 lives in `gap-and-literature.md`, so the four validation gaps became V1-V4 under G2) and of the ledger (now H1 / H3 / D2 / S4) |
| the second "who catches what" table per class | `what-i-can-claim...` 1 | duplicated the E1-E8 x level matrix owned by `arms-and-validation.md` 4.5; the honest recount of 3 fully + 1 partly is quoted once, in 13 |
| the L0-L5 ladder as five *conditions* | `correctness-what-ensures-it.md` 5 | L2 and L3 are not arms and L5 is absorbed into N4; the ladder survives as the predicted shape of the depth curve |
| eleven "on defence, when someone says..." paragraphs | all four notes | three defences survive, compressed into the enum boundary, the arithmetic correction and the pilot branches |
| the three JSON variants of the handle example and the full six-row carrier comparison | `error-does-not-end-with-exception.md` 4 | one example kept, because the rule it states is the point: a handle that does not carry georeference voids the server's own enforcement layer |
| the "PCI ceiling" arithmetic and the "3 of 8 without a contract" derivation, each repeated three times | `crs-error-or-wrong-parameter.md` 6, `what-i-can-claim...` 1 | one statement of each, with the owner cited |

Added while pruning, because the cut had removed the only home of the claim: the four-valued `detected_by` note, the boundary conditions on the enum / name / echo moves (a different surface, and an echo exposes rather than prevents), the honest recount set against the information-closure rule, and the remark that even the deepest level cannot catch an intent error.

Kept, each being the only place in the repository where its claim is made: the seven gates B1-B7 with the one-line thesis, the five numbered findings from the literature, the inversion (schema validation is free in 2026) with its cost, V1-V4 as parts of G2, the predicted shape of the depth curve, the asymmetry and the SPE's own limit, the eight CRS classes with the 1-in-8 arithmetic, why a postcondition cannot catch E2, the four sources of expectation and information closure, enum / name / echo, the four predicates and the working definition of a CRS error, the memory-versus-file correction (E7a / E7b) with the handle contract and the replacement wording, the three claims with their four substitutions, the mechanistic model and its four branches, and the citation hygiene with the three prohibitions.

### `thesis/design/harness.md` (6,728 -> 6,406 words, 4 sources)

Third of the three shallow cuts, and for the same reason: four notes on four different questions (which libraries; own station or ready product; local weights on a cluster; the analyst's procedure) and almost no restatement between them. What the document carried instead was a whole retired *factor design* - a front-end x model study - which is now denied in one line and in the cut log.

| Cut | Source note | Reason |
|---|---|---|
| the hypothesis table H2-H7 with the 2 x 2 gated interaction, the TOST at +/-20 pp, H5 on artefact identity, H6 cost, H7 error classes | `analyst-procedure.md` 5, 12 | a retired numbering and a condition set that is not run; the ledger is H1 / H2 (N1 -> N4) / H3 (expressible share) plus D1-D4 |
| `ladder_level` 1-3, `min_surface`, and the L1-L3 contrasts in the manifest and the tables | same, 2.1, 5.2, 7 | the tool-size ladder is retired; the manifest carries `condition` (K / N1 / N4) |
| "40 tasks x 16 repetitions, MDE 9.3 pp", the 160-run pilot, the 90-run calibration pilot | same 5.1; `own-harness-or-ready-agent.md` 6 | three generations of arithmetic; live is 80 tasks, r = 4, 960 runs, MDE 14.0 pp at tau = 10 |
| the front-end x model factor (2 CLIs x 2 models x 3 paradigms = 1,800 runs, 2,400 with a gated arm) and the 60-shard Slurm array | `hpc-local-models.md` 3-4 | `d-2` fixes one model and `d-4` one harness; a second model doubles the series before it can speak about an interaction, so it is further work rather than a factor |
| "PB3 / PB4", `mcp-15-gated`, `codegen`, `runs.parquet`, the GitHub matrix | same; `technical-stack.md` 5 | retired vocabulary and deleted artefacts; conditions are K / N1 / N4 and the record is `runs/<run_id>/result.json` |
| "ED" as a named metric with its own class table | `analyst-procedure.md` 4 | the construct survives as D1 (S3 plus predicate-level classes) and a variance test is explicitly banned; the old class table had drifted toward a variance measure |
| three separate schedules (17 weeks, the HPC phase plan, the implementation order) | all four notes | one phase plan plus the planning figure in `framing/scope-and-character.md`; a second schedule is a second answer |

Added while pruning, because the cut had removed the only home of the claim: the qualification rule stated as one number in one place (baseline TSR >= 10 %, matching `R-1` and `analysis/statistics.md` 2), the note that a ready-product appendix turns the client-compatibility matrix into a qualification note rather than a results table, the five sensitivity analyses including epochs and tier, and the manifest field `detected_by` beside `protocol_version` and `image_digest`.

Kept, each being the only place in the repository where its claim is made: the measurement argument against agent frameworks, the append-only log with resume, the three SDK traps (schema canonicalisation, logging the wire, pinning the protocol), the stack table with `FakeModel` as its most important row, the prohibition table, D1 / D2 / D3 with D3 chosen, the eight things that must be frozen with the three parity measures, the host as a frozen factor with the capability floor, the serving layer and the wall-clock arithmetic, the Slurm shape with sharding by design cell and the phase plan, the analyst's limits and the blindness rule, Gate A and Gate B, the scoring definitions with their three prohibitions, the per-claim reporting table with the three-valued verdict, the five sensitivity analyses, the output package with ten prohibitions and the change log, and the five lines.

### `thesis/design/tool-surface.md` (6,445 -> 6,091 words, 3 sources)

The one document whose word count hides what happened to it: about 1,500 words of retired factor design came out and about 1,150 words of specification went in, so the net cut is 5 per cent and the real change is a change of subject. It used to be a note about how to vary the surface; it is now the specification of a surface that does not vary.

| Cut | Source note | Reason |
|---|---|---|
| the four-level size ladder (5 / 15 / 30 / 50) with `L1 subset L2 subset L3 subset L4` and the 50-tool "workstation" reference condition | `tool-surface-design.md` 1-6 | a second thesis competing for the same 80 tasks and repetitions; a monotone trend over four correlated points at an MDE of 14.0 pp is unaffordable, and the size gap is retired (G2 is enforcement depth) |
| the second ladder (fixed core plus distractors), the two middle-level variants (+120 runs) and the K-random-catalogues arm from a pool of a hundred tools (+300 runs) | same, 5.1 | randomising catalogue composition is answered by freeze-plus-justify; both variants are named in further work with their cost |
| the logarithmic {1,2,4,8,16,32,64,100} exploratory ladder at 240 runs | same, 5.2 | an exploratory study of curve shape; the curve the design tests is depth of enforcement, not size |
| "MDE ~20-25 pp", "adjacent levels differ by less than the MDE", "100 levels x 120 runs = 12 000 runs" | same, 5.1-5.2 | retired arithmetic; live is MDE 14.0 pp at tau = 10, 960 runs |
| the meta-tool arm (`M1`: search + `run_processing_algorithm`) with its four-condition inference table and the A1/A2 error-granularity comparison | `meta-tools-without-code.md` 0-8 | it changes surface, error granularity and notation together and becomes a thesis about DSL design; the prediction and the `eval` warning are kept, the arm is not run |
| the two-server arm and the four-condition matrix (single/double x basic/meta) with its inference table | `two-mcp-servers-what-it-tests.md` 1-5 | a fourth condition at 320 runs, underpowered for the routing interaction it exists to detect; and topology D does not exist as a standard binding as of XI 2026 |
| the four "sentences for the thesis" and the three "what this cannot show" lists, repeated across the two meta notes | both | one paragraph in the meta-tool section and one bound in the closing lines survive; the rest restated two conclusions in different vocabulary |
| the standalone "changes this forces on the artefacts" section | `tool-surface-design.md` 8 | a list of consequences for documents since rewritten; the consequences live where they bite - in the parameter rules, the return shape and the corpus's near-miss coding |

Added, because the cut had removed the only home of the claim: the nine operations as a table with an explicit "what it does not express" column; the same task written at all three conditions, to show that N1 and N4 calls are character-identical apart from the model's own values; the near-miss enumeration per card with the three metrics that follow from it at no extra cost; one complete catalogue entry in YAML, including the `checks` block that is the whole difference between N1 and N4; the expressible-share codebook with its tie-breaking rule and its kappa; the operational envelope (no network, baked PROJ grids, ten-minute ceiling, headless); and the arithmetic of any fourth condition (+320 runs, +33 per cent of the series, no improvement in the MDE of the existing contrasts).

Kept, each being the only place in the repository where its claim is made: the answer that the surface is fixed, the nine atomic operations and the argument that composition inside a tool would import the code arm's advantage, the retirement of the size ladder with the surviving insight that tool count is not the causal variable and that a catalogue is a sample of one, the single-server bound with the missing topology D, the frozen catalogue definition with `surface_sha` and the two bias guards (parity table and anonymised-catalogue control), the three parameter rules with the catchability-expressiveness trade, the four rules for what the server returns, the four prohibitions with the `validate(inputs)` case, the expressible share as a surface property with the pre-registered pattern and the refutation condition on `none` cards, the allow/forbid table with determinism and tolerances, the meta-tool prediction, and the risk table with its one unmitigated risk.

### `thesis/draft/structure.md` (5,875 -> 6,043 words, 3 sources - the only document that grew)

The only one of the seventeen that ends up longer, and the reason is on the record rather than hidden: the merge had left THREE tables of contents inside one file (seven chapters under the faculty frame, eight chapters of design science, six chapters of IMRAD), each with its own page budget and its own retired design. Reconciling them to one structure removes about 1,100 words of duplicate schedule; adding the production furniture a single structure needs (compliance table, artefact list, appendices as preconditions, the writing-time split, the examiner's route) adds about 1,250. The file was also below the 6,000-word band floor of AC #4 at 5,875, so the net +168 is what brings it into the band rather than an expansion of argument.

| Cut | Source note | Reason |
|---|---|---|
| the eight-chapter design-science contents page, its 90-page budget and its chapter-to-draft map | `toc-blueprint.md` | contradicted the faculty frame, which needs "Materials and methods" and "Summary and conclusions", and its content was built on retired design: 2 front-ends x 2 models x {S1, S2, S3, codegen}, 1,800 runs, a 50-tool surface. Design science survives as the narrative of 3.1, the budget is unified at 82 pp |
| the six-chapter IMRAD structure that merged methods, instrument and execution into one 26-30 pp chapter | `metaplan-and-imrad.md` B.2 | at that length the instrument - which is C1 - disappears into procedure and the deviations register has nowhere to live; the IMRAD logic is kept as a must/must-not table, the numbering follows the faculty |
| the seven-chapter contents page as it stood | `table-of-contents.md` 3 | its sections still carried 40 tasks, the 5 / 15 / 30 ladder, `min_surface`, the 2 x 2 with TOST, H1-H7, a capability axis with three levels, ED and RRR as headline metrics, a 90-run control slice |
| the H1-H7 numbering throughout, with its hypothesis-to-section map | `table-of-contents.md` 4, `toc-blueprint.md` 3 and 6 | the ledger is H1 / H2 (N1 -> N4) / H3 (expressible share) plus D1-D4; a contents page that schedules the wrong hypotheses schedules the wrong chapters |
| the ladder section (6.3) and the 2 x 2 "validation boundary" section (6.4) as separate results | `table-of-contents.md` 6 | one is retired, the other is absent from the design; 6.2 and 6.4 now carry the depth contrast and the detection sites |
| the capability-axis section (6.6) and its place in 3.2 | both notes | `d-2` fixes one model; a section reporting a capability effect would report a comparison that was not run |
| the "interoperability swap" section (same server x agents) | `toc-blueprint.md` 6.8 | retired with the front-end factor; auditability and server replaceability survive as a descriptive section |
| two page budgets (82 and 90/91) and two writing orders | all three notes | one budget and one order; a second order is a second answer |
| the appendix list promising "the S3 catalogue with 50 tools and the nesting proof" | both notes | the surface does not nest; appendix B lists nine operations with the parity table and the `checks` file |
| the metaplan printed as a table | `metaplan-and-imrad.md` A.2 | in an introduction it reads as a form; it becomes four paragraphs whose connecting sentences are named |

Added, because the cut had removed the only home of the claim: the statement that three structures were merged and one had to win, with the argument for a separate execution chapter as the place reliability is demonstrated; the compliance table mapping each element of the faculty frame to a chapter; the artefact list (nine generated result tables, four hand-written instrument tables, three figures) so that no chapter is written from memory; two hand-written tables that can exist before the sweep; the examiner's route through the thesis; appendices as preconditions of chapters (appendix D as the proof of symmetry, appendix G as the answer to "could it be your harness"); the split of writing into specification, frame, generation and reliability jobs with their different inputs; the three-row integration rule and the further-work list with a cost for every item scheduled into chapter 7; and the honest chapter-by-draft map which says the thesis is waiting on data, not on writing.

Also this turn, outside the queue: `thesis/concept-dictionary.md` was carrying the retired vocabulary in its glossary rows (ED, RRR, T2V, REF, TOST, and H7 as the condition for blind coding). The rows are not deleted - a glossary should show what fell out - but each is marked as former and points at its successor (D1, `repair_iterations`, the censored secondary measure, the silent-error entry, and the three-valued verdict), the abbreviation list now names live acronyms only, and a header note says the "where" column predates the merged structure and will be remapped when the chapters are written. That note is the honest alternative to a fake remap of 130 section numbers.

### `thesis/design/runs.md` (3,290 -> 6,046 words, 2 sources)

The second document that grew, and for a different reason than `structure.md`: the merge was two notes (the architecture, and one card worked in both arms) totalling 3,290 words, well under the band floor, and pruning the retired half of them left about 2,300. The three-condition rewrite and the pipeline material the document should have carried bring it to 6,046. Nothing in the growth is argument repeated from elsewhere; every section added is about what physically happens between a prompt and a scored artefact, which is this document's declared subject and no other document's.

| Cut | Source note | Reason |
|---|---|---|
| the two-arm vocabulary ("arm A / arm B") with the tool table written for two | both notes | the design has three conditions; a two-arm transcript cannot show that N1 and N4 are the contrast, and it invites exactly the reading the thesis has to refute - that schema validation is the treatment |
| `min_surface: 1` in the card and "this card needs one operation" | `run-in-both-arms-a-01.md` 0 | the tool-size ladder is retired; the card carries family, tier and expressible share |
| the surface ladder 5 / 15 / 30 / 50 and "the level chooses what the server publishes in tools/list" | `experiment-architecture.md` 6 | retired with the ladder; the true and useful part survives - the surface is a property of the server's registration, not of the prompt |
| the L1 / L3 / L4 ablation as the answer to "that is your server, not the protocol" | `run-in-both-arms-a-01.md` 3 | retired levels; the defence is now the N1 -> N4 contrast with the catch rate as its falsifier |
| the "control slice: 15 tasks with opencode and goose" | `experiment-architecture.md` 1 | front-end factor retired (d-2, d-4); the descriptive product appendix is 48 runs and lives in `what-we-study.md` 11 |
| the 25-turn figure as a design constant | `experiment-architecture.md` 4 | a budget, not a finding; it is now "the turn budget", pinned in the manifest, with the 10-minute ceiling the only fixed number |
| the `turns_limit = 1` side condition | `experiment-architecture.md` 2 | one sentence survives; at 80 tasks it would spend runs the depth contrast needs |
| three of the five "sentences for the thesis", and the "what this shows for measurement" table | `run-in-both-arms-a-01.md` 4, 5 | the transcript now does the work; the fields that matter are listed once in the observation table |
| the module line counts as a commitment | `experiment-architecture.md` 8 | kept as indicative and marked so |

Added, because the cut had removed the only home of the claim: the run directory as a contract with `result.json` written last; what that layout buys in rescoring and in a defensible archive, including the rule that a failed run's record is never cheaper to drop than a successful one's; the truncation and context rules with the reason each must be identical; the harness-level error taxonomy mapped onto the five exclusion rules, with the rule that a rejection is never an exclusion; run identity, resume and idempotency; the volume arithmetic and the pruning rule written down before the sweep; the full three-condition transcript of card A-01 with the statement that N1 fails exactly as K fails; the good-day transcript in the code condition, with three ways a self-written guard can go wrong and why that is what S4 and S4b measure; the coding discipline for S4 and S4b with kappa; the counter-case from family C; and the parity test plus `surface_sha` over a canonical `tools/list`.

Kept, each being the only place in the repository where its claim is made: the one-loop/three-channels decision with the list of what must be identical and what must differ, the agent-versus-LLM answer with the native-tool-calling qualification, the component diagram with the shared-engine line, the loop with its observation points, the `run_python` variant choice with its safety and determinism rules, what "using MCP" concretely means, the observation table and what each field feeds, the build order with `FakeModel` first, and the manifest pin list.

### `thesis/writing/requirements.md` (6,006 -> 6,025 words, 3 sources) - a rulebook, not an argument

Deliberately treated differently from the rest of the queue: this is a transcript of the faculty's degree regulations and four competitions' rules, so nothing in it may be pruned on grounds of style or redundancy - a rule one must comply with is not an argument that can be tightened. What changed is the FORM: translated to English, reorganised as a checklist with a status per requirement (met / conditional / not met / will be met by an act of writing), and corrected where it contradicted the design.

The correction is the reason this document was worth rewriting. It reported a structural CONFLICT - seven planned chapters against "five parts" - and resolved it by merging methods, instrument and execution into one 26-30 page chapter. That was a misreading: the frame already contains a main part of two to four chapters *between* the third chapter and the summary, so three introductory + three main-part + one summary = seven chapters with the main part at three, inside the permitted range. The earlier resolution was not merely inelegant; it cost the instrument its own chapter, which is exactly what makes C1 disappear into procedure, and it left a 26-30 page chapter with nowhere to put the deviations register. `draft/structure.md` and this document now agree, and this one records which of them changed its mind and why.

| Cut or changed | Source note | Reason |
|---|---|---|
| the "delta against the existing table of contents" section and the six-chapter renumbering that followed from it | `thesis-requirements.md` 3-4, `umcs-criteria-and-competitions.md` 1.3 | resolved a conflict that did not exist; the arithmetic and the cost are recorded in the rewritten 5 |
| the per-chapter "what each chapter must contain" map | `thesis-requirements.md` 2 | duplicated `draft/structure.md` 3, which owns chapter contents; this document owns requirements and their status |
| the "H1-H5 / three conditions / 8 domains x 10 tasks / ladder L1-L5 / measures S1-S5" preamble | `thesis-requirements.md` preamble | a retired design generation; the ledger is H1 / H2 / H3 with D1-D4, 80 tasks in three families, depth axis N1 -> N4 |
| "TOST" quoted as evidence of master's-level sophistication | `umcs-criteria-and-competitions.md` 1.2 | the equivalence test is retired; the depth argument now rests on McNemar, the mixed/GEE estimand distinction, Holm and S3 |
| the C1-C5 list | `thesis-requirements.md` 1 | contributions are C1-C3 |
| the "six things to do" list with completion marks | `umcs-criteria-and-competitions.md` 2 | two of the six dissolved with the structural correction; the rest became rows with statuses inside the checklists |
| the narrative summary of administrative rules (supervisor selection, document circulation, the diploma fee) | `umcs-regulations-2025-26.md` 1, 2, 8 | compressed; what binds the TEXT is kept, the rest is one paragraph plus the round of documents |
| the editorial remarks about the regulations document itself | `umcs-regulations-2025-26.md` 11 | one row: do not quote the extraction |
| the competitions' calendar by T-0 and eleven "notes for the defence" paragraphs | `umcs-criteria-and-competitions.md` 3; all three notes | the calendar belongs to `competition-verification.md`; the defence script belongs to `writing/defence.md` |

Added, because the compression had removed material the document alone can carry: the status vocabulary and the methodological warning that a draft can only be judged as design; the reviewer's degree as the narrowest bottleneck, because it is decided by other people on their own timetable; the ordered skeleton of the ten elements of V as a table; the administrative rules that nonetheless bind the text, including the distinction between a substantive and an editorial change of topic - which is why the retired REST arm is not "just another arm"; the one-page experiment description the College needs for the experimental status; the abstract as a deliverable of its own, with the two-vocabulary framing and the reason to write it last; appendix numbering plus the rule that every appendix is cited, with D as the proof of symmetry and G as the answer to "could it be your harness?"; the template decision (Markdown to DOCX through a reference template, built before chapter 4); the bibliography conversion as a script over 67 entries rather than by hand; the round of documents and its two administrative failure modes; a consolidated seventeen-row checklist with who can close each row; the three blocked-on-other-people rows as the argument for doing them first; the four sentences the defence must be able to produce; and the thirteen family-C cards as one family carrying three separate obligations (an SGP qualification, the moderator of H3, and the counter-case in chapter 6).

Also fixed outside the queue: `thesis/literature/literature.bib`'s header claimed 38 entries while the file holds 67.
