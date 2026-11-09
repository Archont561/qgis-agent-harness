---
id: draft/structure
title: "Structure and proportions of the thesis"
type: note
status: live
language: en
question: "Which chapters exist, how long is each, and what goes in them?"
tasks: [TASK-13]
updated_date: '2026-11-07'
---

# Structure and proportions of the thesis

> Which chapters exist, how long is each, and what goes in them?
>
> Merged 2026-11-07 from `table-of-contents.md`, `toc-blueprint.md`, `metaplan-and-imrad.md`. Pruned, reconciled and translated 2026-11-07; the cut log is §14. The merge preserved **three competing tables of contents** — a seven-chapter one under the faculty frame, an eight-chapter design-science blueprint, and a six-chapter IMRAD map — each with its own page budget and its own retired design. This document now carries **one** structure. The claims it schedules are owned by `design/arms-and-validation.md` §2; the aim and contributions by `framing/aim-and-contributions.md`; the title by `draft/titles.md`.

---

## 1. One structure, and which one

**Seven chapters, in the frame the faculty imposes.** The programme's regulations (§V of the degree rules) fix the outer skeleton: title page (PL and EN) · table of contents · abstract · 1 Introduction · 2 Literature review · 3 Materials and methods · **the main part, in two to four chapters** · Summary and conclusions · lists · appendices. All the freedom sits inside the main part, and the choice made here is **three** chapters there — the instrument, the execution, the results.

| Was | Now | Why |
|---|---|---|
| eight chapters with DSRM as chapter 3 | **seven**, with DSRM as the framing of §3.1 | the faculty frame requires an explicit "Materials and methods" chapter and a separate "Summary and conclusions"; an eight-chapter design-science order collides with both |
| six chapters that folded methods, instrument and execution into one 26–30 pp chapter | seven, with the instrument and the execution separated | at 26–30 pp inside one chapter the instrument — which is contribution C1 — disappears into procedure, and a six-month schedule with its deviations loses the place where reliability is demonstrated |
| a separate Discussion chapter | **no separate discussion**; interpretation lives in §7 | with one confirmatory test and three named claims, a discussion chapter restates §6 and §7 and gives a reviewer two places to attack instead of one |
| both "Theoretical introduction" and "Literature review"; a "Tools and technologies" chapter | neither | the first duplicates §2; the second is a list of libraries, and versions belong to the manifest and to appendix E |

**Two of the three framings survive inside the seven.** IMRAD is not a layout but an order of inference — *what was asked → how → what came out → what follows* — and it maps onto the seven as I = §1–2, M = §3–5, R = §6, D = §7. Design science survives as the narrative of §3.1 (problem → objectives → design → demonstration → evaluation), which is how the chapter explains why the instrument looks the way it does.

---

### 1.1 The frame, element by element

Written out because a missing element is discovered at submission, not at defence:

| Element the regulations require | Where it is satisfied | Risk if forgotten |
|---|---|---|
| title page in PL and EN | front matter | formal rejection; the PL title comes from `draft/titles.md`, and the approved wording needs its repair applied |
| abstract ≤ 4 000 characters with keywords | front matter (PL), plus a ~250-word EN abstract | the limit is a *character* limit; an abstract written to a page and then cut loses its second sentence, the locational one |
| 1 Introduction | §1 | — |
| 2 Literature review | §2 | a merged "introduction and literature" chapter is not the required skeleton |
| 3 Materials and methods | §3 | — |
| **main part in 2–4 chapters** | §4, §5, §6 | three chapters is the choice; two would force the execution into §3 and four would need a discussion chapter |
| Summary and conclusions, with **own judgements and proposals** | §7 | a §7 that only summarises §6 fails the requirement even if every number is right |
| lists of figures, tables, abbreviations; bibliography | after §7 | — |
| appendices | A–G | — |
| hierarchical layout and a chain of inference (§III.11) | §2 and §7 of this document | checked as a checklist, not as an intention |

The regulation text itself, with the phrase-level requirements, is `writing/requirements.md`; this table only says **which chapter answers which requirement**, because that is a scheduling question rather than a reading of the rules.

## 2. Formal rules for the table of contents

The contents page is not decoration; a reviewer uses it to decide three things in ten seconds: whether the chapters **follow from each other**, whether there is a chapter with an **instrument** and a chapter with a **result**, and whether anything obvious is **missing** (validity, power, limitations).

| Rule | Reason |
|---|---|
| at most **three levels** (1 / 1.1 / 1.1.1) | a fourth level does not fit the page and signals that the hierarchy was never decided |
| a heading is a promise: a section with one paragraph is **demoted** | sixty entries at eighty pages reads like a list of notes, not a thesis |
| every chapter opens with **one or two sentences** before its first subsection | the reader has to know why the chapter exists before reading it |
| continuous Arabic numbering; lists of figures, tables and abbreviations **outside** the numbering | the faculty's requirement |
| the contents page is **generated** from headings, never typed | a hand-typed contents page breaks at the first correction |

---

## 3. The table of contents

Budget: **~82 pages of body**, excluding title page, lists and appendices. Abstract: **≤ 4 000 characters** with keywords, first sentence informative, second locational.

### Front matter

| Element | Content | Length |
|---|---|---|
| Title page (faculty template) | university, faculty, field, specialisation, name, title in PL and EN, supervisor, place and year — **the title itself comes from `draft/titles.md`** | 1 p. |
| Table of contents | this structure | 2 pp. |
| Abstract (PL) | ≤ 4 000 characters, keywords; five sentences, in this order: **the comparison and the object measured**, **the excluded hybrid**, **the gap**, **the headline result**, **the contribution** — the first two fixed verbatim in `draft/titles.md` §4.1 | 1 p. |
| Abstract (EN) | ~250 words, same four sentences | 1 p. |
| Statement of contributions | C1–C3 in one paragraph each, taken verbatim from `framing/aim-and-contributions.md` §7 — **placed up front so the examiner knows what to look for** | ½ p. |

### 1. Introduction — 7 pp

| § | Content | Served by |
|---|---|---|
| 1.1 | **State, in the order of the metaplan**: what is the case — agent access to geoprocessing is organised as a catalogue of named operations, and what is evaluated is the accuracy of calls and the course of action, not the sense of the artefact | `framing/gap-and-literature.md` §2 |
| 1.2 | **Why it is so**: three reasons — the type does not encode meaning (metres and degrees are the same float), evaluation went where it was cheap (calls are loggable, meaning needs an oracle), and the protocol standardises the envelope rather than the operation | `design/correctness.md` §§2–3 |
| 1.3 | **What is missing**: the gap in three sentences, as a *measurement* gap — nobody has estimated how much of the protocol's value is validation | `framing/gap-and-literature.md` §3 |
| 1.4 | **What should be the case, and what to do**: conditions attached to operations, georeference carried by every result, evaluation by artefact; and the instrument that would show it | same §4 |
| 1.5 | Aim and claims, named and not developed: H1, H2, H3, and D1–D4 | `design/arms-and-validation.md` §2 |
| 1.6 | Contributions C1–C3, one sentence each | `framing/aim-and-contributions.md` §7 |
| 1.7 | Scope and boundaries stated **before** the claims: one engine, one model, one harness, nine operations, eight CRS error classes, vector and raster but not cartography | `framing/edge-of-scope.md` §2, §7 |
| 1.8 | Structure of the thesis, one paragraph per chapter | — |

**The metaplan, and how much of it to print.** The four columns — *how it is / why it is so / how it should be / what to do about it* — are a drafting scaffold, not a table for the thesis: printed as a table they read as a form. They become **four paragraphs** in §1.1–1.4, each closing with the sentence that opens the next. The desired state then feeds §1.5–1.6, and the whole table is kept for a conference poster. **The board itself, filled, with the four linking sentences written out and the same four questions put to the work rather than to the argument, is `draft/metaplan.md`.**

### 2. Literature review — 14 pp

| § | Content |
|---|---|
| 2.1 | The autonomous-GIS agenda and what the stream postulates |
| 2.2 | **A positioning taxonomy of integration methods** — coupling, contract, validation point, coverage, provenance. A *frame*, not a contribution |
| 2.3 | Standardising geoprocessing: from WPS through OGC API – Processes to MCP — the same problem, a new client |
| 2.4 | MCP as a contract: schemas, discovery, and the security surface |
| 2.5 | The empirics of the protocol: wrapping, information fidelity, and the results where tool access hurts |
| 2.6 | MCP benchmarks: what they optimise and what they do not see |
| 2.7 | GIS agents: the consensus around code generation |
| 2.8 | GIS benchmarks: from text matching to the evaluation of executed artefacts |
| 2.9 | **The empty cell**, with the nearest-neighbour table and one separating sentence for each |
| 2.10 | What the literature licenses and what it forbids you to claim |

**Two traps.** Do not claim novelty for the taxonomy here — §2.2 is positioning, and novelty lives in §1.6 and §7.2. And do not let §2.5 become a survey of *what MCP is*; the reader needs the two or three measurements that bound this thesis, not a description of the protocol.

### 3. Materials and methods — 15 pp

| § | Content |
|---|---|
| 3.1 | DSRM framing: problem → objectives → design → demonstration → evaluation, and why the design is an artefact rather than a survey |
| 3.2 | **The three conditions**: K (generated code), N1 (nine operations at the schema), N4 (the same nine, plus invariants and terminal conditions). One table, not prose |
| 3.3 | What is **frozen** and what is varied: one model, one harness, one platform, one corpus, one oracle. A factor register with a decision for each |
| 3.4 | **The estimand and the unit of inference**: the task, not the run; ICC 0.661 and DEFF 3.0, so 960 runs are worth about 320 independent rows |
| 3.5 | **The five equivalence assumptions** A1–A5 (oracle validity, capability parity, information parity, budget parity, no drift), each with the consequence of its failure |
| 3.6 | Claims and tests: H1 as the single confirmatory test at α = 0.05; Holm over {H2, H3}; D1–D4 descriptive; D4 as a precondition rather than a finding |
| 3.7 | **Power and the MDE**: 14.0 pp at τ = 10, the closed-form relation, and the rule that a difference below the MDE is *undecided*, not absent |
| 3.8 | Validity — construct, internal, external, conclusion — with the specific threat and its mitigation for each |
| 3.9 | Pre-registration: what was frozen, when, and which changes are admissible at all |
| 3.10 | Ethics and safety: no human subjects; adversarial probing confined to the author's own servers; disclosure |

### 4. The instrument — 14 pp ← **C1 lives here**

| § | Content |
|---|---|
| 4.1 | Architecture: one agent loop, three action channels, a run directory, and the rule that no run is ever dropped silently |
| 4.2 | **The corpus**: 80 cards in families P (preparation/IO), A (analysis) and C (cartography), tiers T1–T4, and the **expressible share** coded per card |
| 4.3 | The card schema: every key and why it exists, including the near-miss operations and the expected error classes |
| 4.4 | **The catalogue**: nine atomic operations, frozen and hashed (`surface_sha`), the parity table, the anonymised-catalogue control |
| 4.5 | Oracles and the predicate vocabulary: CRS with axis order, geometry, rasters, attributes, cartographic predicates — with the four CRS predicates P1–P4 |
| 4.6 | **Tolerances**: how they are derived, why never byte equality, and the freeze |
| 4.7 | The oracle's negative control: every oracle must reject a deliberately broken artefact, 40 of 40 |
| 4.8 | **Metric definitions**, each defined once with its unit: TSR, the share of satisfied predicates, S3, S4 and S4b, S5, CVS, cost per success |
| 4.9 | The failure taxonomy — seven failure classes and eight CRS classes — and the blind double coding with κ |
| 4.10 | `detected_by`: the four values, and why "the oracle caught it afterwards" and "the server refused" must never be merged |
| 4.11 | Provenance: the manifest, the digests, the negotiated protocol version, the abstract hashes |
| 4.12 | **Instrument qualification**: the 10 % floor, the negative control, oracle repeatability, κ — and what happens when one of them fails |

> This is the chapter that outlives the thesis. Write it as if it will be cited by someone who never reads the results.

### 5. Execution of the experiment — 6 pp

| § | Content |
|---|---|
| 5.1 | Plan and blocks: 3 conditions × 80 tasks × 4 repetitions = **960 runs**, sharded by design cell |
| 5.2 | Pilot and qualification: what the pilot decides and what it may not decide |
| 5.3 | Accounting: planned, executed, excluded — with the closed list of five exclusion rules |
| 5.4 | **The deviations register**: everything changed after pre-registration, each with its impact on which table |
| 5.5 | Reproduction: the three commands a reader types |

### 6. Results — 18 pp

Order: the primary comparison first, then the mechanism, then everything else. Every section opens with the question it answers and closes with one sentence a reader could quote.

| § | Content | Answers |
|---|---|---|
| 6.1 | **The main comparison** K against N4: TSR with confidence intervals, per-task paired differences, effect size, **and the MDE printed beside them** | H1 |
| 6.2 | **Depth on one surface** N1 → N4: the contrast, the plateau, **and the in-loop catch rate** | H2 |
| 6.3 | **The moderator**: difference against expressible share, including the `none` cards where a difference would refute rather than support | H3 |
| 6.4 | **Where errors are caught**: the `detected_by` distribution, four values across three conditions | C3, the money figure |
| 6.5 | Failure signatures: seven failure classes and eight CRS classes by condition, with κ; silent CRS against loud wrong tool choice | D2 |
| 6.6 | Repeatability: S3 and the predicate-level classes across the four repetitions | D1 |
| 6.7 | Cost per success, and whether the cost ranking reverses the correctness ranking in any family | D3 |
| 6.8 | Auditability (S5) and server replaceability — descriptive, with the caveat that both are properties of the instrument | — |
| 6.9 | **Sensitivity**: tolerances, exclusions, family weighting, tier, epochs — each with "does the conclusion change" | reliability |
| 6.10 | What the instrument did not produce: failed qualification checks, exclusion rates, truncation, anomalies reported rather than removed | D4 |

### 7. Summary and conclusions — 8 pp

| § | Content |
|---|---|
| 7.1 | Answers claim by claim — H1, H2, H3, D1–D4 — each with its evidence pointer and a three-valued verdict: **confirmed / refuted / undecided** |
| 7.2 | Contributions: C1 the instrument, C2 the empirical difference with its detection sites and its cost, C3 enforcement inside one surface — with the anti-overclaim formula: *adapts and combines*, never *first* |
| 7.3 | What this means for GIS in the age of AI: theses T1–T4, each with its condition attached |
| 7.4 | **The three-row rule for integrators**: encode it / check it in the loop / check it after the fact — and the alarm that an implementation whose requirements all land in the third row can be audited but not supervised |
| 7.5 | Limitations, ordered by how much they threaten the conclusion rather than by convenience |
| 7.6 | Further work, each item with its cost: the substitution slice (~90 runs), the descriptive product appendix (48 runs), a third arm (+320 runs), random catalogues (+300), a second model (doubling), the meta-tool arm, gated code generation |

> The faculty's rules require **own judgements and proposed solutions** in this chapter, and forbid reducing it to a summary of §6. §7.2–7.4 are where that requirement is met.

### Lists and appendices

| Element | Content |
|---|---|
| Lists of figures, tables, abbreviations | generated; the abbreviation list will be long — TSR, MDE, ICC, DEFF, CRS, EPSG, MCP, PyQGIS, PCS, CVS — and that is fine |
| Bibliography | alphabetical, one style throughout |
| **A** | the card schema plus three example cards, one per family |
| **B** | the nine operations in full, the parity table (server call against code-arm snippet), and the `checks` file |
| **C** | the predicate vocabulary and the oracle's reference implementation |
| **D** | prompt templates — identical apart from the interface, which is the proof of symmetry |
| **E** | the manifest schema, one real manifest, and the hashes |
| **F** | statistical tables: model outputs, the power arithmetic, the sensitivity analyses |
| **G** | reproduction: container build, commands, hardware |

---

## 4. At a glance: chapter → contribution → claim → external criterion

| Chapter | pp | Contribution | Claims | Whom it serves |
|---|--:|---|---|---|
| 1 Introduction | 7 | the frame of the problem | — | the examiner's first question: is the topic weighty and justified |
| 2 Literature | 14 | positioning | — | the choice of literature; knowledge of the field |
| 3 Methods | 15 | rigour of inference | H1–H3, D1–D4, the test plan | independence of method; a methodologist reviewer |
| 4 **The instrument** | 14 | **C1** | instrument qualification (D4) | the creative element; the chapter cited by others |
| 5 Execution | 6 | reliability | — | reproducibility; experimental status |
| 6 **Results** | 18 | **C2** | H1, H2, H3, D1–D3 | the scientific level of the work |
| 7 Conclusions | 8 | **C3** + T1–T4 | verdicts | applicability; the practical contribution |

**The test of the table:** a chapter with an empty cell on the right has no audience and must be shortened or cut. A chapter with no claim in the middle is a chapter that does not advance the argument — which is why §5 is the shortest one and why it is allowed to be.

---

### 4.1 The tables and figures each chapter must produce

The structure is also a production plan: a chapter without a named artefact is a chapter that will be written from memory. The fixed list, so that §6's prose is generated from files rather than typed (° marks a generated table):

| Artefact | Belongs to | Produced by |
|---|---|---|
| ° t6_1 — TSR, CI, paired differences, MDE | §6.1 | the scoring pipeline |
| ° t6_2 — depth contrast N1 → N4, plateau, catch rate | §6.2 | same |
| ° t6_3 — difference against expressible share | §6.3 | same, joined to the card codes |
| ° t6_4 — `detected_by` × condition, four values | §6.4 | same |
| ° t6_5 — failure classes, CRS classes, κ | §6.5 | same, plus the coding sheet |
| ° t6_6 — S3 and predicate-level repeatability classes | §6.6 | same |
| ° t6_7 — cost per success and the rankings | §6.7 | same |
| ° t6_8 — auditability (S5), replaceability | §6.8 | manifest fields |
| ° t6_9 — the five sensitivity analyses | §6.9 | same pipeline, five variants |
| t4_1 — the nine operations, parameters, checks | §4.4 | the catalogue file |
| t4_2 — the parity table, server call against code snippet | §4.4 | written by hand, once |
| t4_3 — the predicate vocabulary and tolerances | §4.5–4.6 | the oracle files |
| t4_4 — metric definitions with units | §4.8 | written by hand, once |
| t3_1 — conditions × factors, the register | §3.2–3.3 | written by hand, once |
| t3_2 — MDE against τ and N | §3.7 | the closed form |
| t2_1 — the nearest-neighbour table with separations | §2.9 | the literature notes |
| f6_1 — TSR by condition with intervals; f6_2 — depth curve; f6_3 — share interaction | §6.1–6.3 | the same tables, plotted |

Both hand-written tables (t4_2, t4_4) are the ones a reviewer photographs, and both can exist before the sweep — which is another reason §4 is written first.

## 5. Order of writing, which is not the order of chapters

1. **§4 The instrument** — writing it exposes holes in the design and needs no results.
2. **§3 Methods** — once the instrument is fixed the factors and the tests are knowable.
3. **§6 Results** — section by section as the analyses land, generated from the tables rather than typed.
4. **§2 Literature** — written last it is a review, not a summary of a study that has not been run.
5. **§7 and then §1** — conclusions first, introduction after: an introduction written after the conclusions knows what it promised.
6. **The abstract**, at the very end, with the 4 000-character limit in hand.

---

## 6. What is deliberately absent from the contents

| Absent | Why that is right |
|---|---|
| a chapter "Tools and technologies" | a list of libraries is not content; versions and pins live in §4.11 and appendix E |
| "Theoretical introduction" beside "Literature review" | the same thing twice |
| a separate Discussion chapter | with one confirmatory test, interpretation belongs in §7 and does not need its own chapter |
| a chapter about the agent framework | the loop is the instrument, not the subject; described in §4.1 |
| "Partial conclusions" after every chapter | it repeats §7 and gives a reviewer three places to attack instead of one |
| a chapter on surface size, meta-tools or two servers | retired as designs (`design/tool-surface.md` §2), so a chapter about them would report studies that were not run |

---

### 6.1 The examiner's route through the thesis

A defence is not a reading; it is a set of questions. The structure should let each be answered by pointing at a page:

| If the question is… | Send them to | Then to |
|---|---|---|
| "what is actually new here?" | §1.6, then §7.2 | §2.9 for what is not new |
| "is the comparison fair?" | §3.3–3.5 (frozen factors, equivalence assumptions) | §4.4 (parity table), appendix B |
| "how do you know a wrong artefact is wrong?" | §4.5–4.7 (predicates, tolerances, negative control) | appendix C |
| "what did you measure, exactly?" | §4.8 (metrics, each defined once) | §6.1 |
| "is it powered to say that?" | §3.7 (MDE) | §6.1's MDE column, §6.9 |
| "where does the effect come from?" | §6.2 (depth) and §6.4 (detection sites) | §6.3 (the moderator) |
| "could it be your harness?" | §4.1, §5.4 (deviations), §6.10 (anomalies) | appendix G |
| "what does it *not* show?" | §1.7, §7.5, and the before/after lists in §7.6 | — |

Written as a route rather than as a defence script, because the route is a property of the structure and the script is a property of the day.

## 7. The inference chain, as a checklist

Each chapter must end with the sentence that follows from it and opens the next. Written out, because this is the test the faculty's §III.11 actually describes:

- [ ] end of §1 → "…so two interfaces have to be compared with everything else pinned" → opens §2, what is already known
- [ ] end of §2 → "…and that frame does not exist, so it has to be built" → opens §3, the methods
- [ ] end of §3 → "…these conditions are realised by the instrument described next" → opens §4
- [ ] end of §4 → "…this instrument was run according to the procedure of §5" → opens §5
- [ ] end of §5 → "…960 runs were collected, whose results §6 reports" → opens §6
- [ ] end of §6 → "…these results answer the question the title poses" → opens §7

**The numerical check that goes with it:** every number in §7 has a source in a table of §6; every table of §6 has a counterpart among the measures of §4.8; every measure of §4.8 is computable from the artefacts and the manifest. Where that chain breaks is exactly where a reviewer will ask the question.

---

### 7.1 What must exist before a chapter can be written

The appendices are not an afterthought appended to a finished text; several of them are the *condition* of a chapter existing:

| Before writing | There must exist | Appendix |
|---|---|---|
| §4 | the nine operations, the parity table, the `checks` file | B |
| §4 | the predicate vocabulary, the tolerance derivation, the negative-control results | C |
| §4 | the prompt templates, proved identical apart from the interface | D |
| §5 | the manifest schema and one real manifest | E |
| §6 | the statistical tables and the power arithmetic | F |
| §5, §6 | the container build, the commands, the hardware record | G |
| §2 | the bibliography, complete and consistently styled | — |

Two consequences. **Appendix D is the proof of symmetry** — without it, the claim that the two conditions differ only in the action channel is an assertion. And **appendix G is the answer to "could it be your harness?"**, which is the first question an examiner asks of any measurement made with a self-built instrument.

## 8. What each IMRAD element must and must not do

| Element | Must | Must not |
|---|---|---|
| **I** (§1–2) | problem, aim, thesis, scope, contributions, the gap in the literature | promise a result; choose the literature to fit the thesis |
| **M** (§3–5) | the criterion of correctness, the conditions, the equivalence assumptions, the measures, the power, the taxonomies **before** the measurement | report results; justify the number of tasks after seeing them |
| **R** (§6) | numbers with uncertainty, distributions, negative results, the MDE beside every "no difference" | interpret, explain, or cite literature |
| **D** (§7) | the answer to the title, the mechanism, the bounds, the practice, further work | introduce new results or new tables |

---

## 9. Page budget, and what it implies about the writing

| Ch | 1 | 2 | 3 | 4 | 5 | 6 | 7 | total |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| pp | 7 | 14 | 15 | 14 | 6 | 18 | 8 | **82** |

Two consequences worth stating before writing starts. **§6 is the largest chapter and the last to be written**, so the schedule must not treat it as a writing task but as a generation task — its tables exist before its prose does. And **§4 is the second largest and the first to be written**, which is the correct order for a thesis whose contribution is an instrument: the chapter that outlives the work is the one written first.

---

### 9.1 What can be written before the sweep, during it, and after

The schedule is not "write 82 pages in eight weeks"; it is three different jobs whose inputs arrive at different times:

| Job | Chapters | Depends on | Can start |
|---|---|---|---|
| **specification writing** — the instrument and the methods, written as if cited by someone who never reads the results | §4, §3 | nothing but the design being frozen | now |
| **frame writing** — literature, gap, positioning, scope | §2, §1 (except 1.5's numbers) | the reading being finished | after §4, so that the review is not a summary of a study not yet run |
| **generation** — results, then conclusions, then the abstract | §6, §7, abstract | the sweep and the scoring | after §5's accounting is final |
| **reliability writing** — the deviations register and the run accounting | §5 | the series | during and immediately after it |

The reason this matters for the structure rather than for the planner: **§5 cannot be written before the series runs**, and it is the smallest chapter. A plan that reserves writing time for it in week 3 is a plan that will produce a chapter of intentions.

## 10. Chapter → draft material, honestly

| Chapter | Already drafted in | State |
|---|---|---|
| 1 | `framing/gap-and-literature.md`, `framing/aim-and-contributions.md` | solid; needs the metaplan reordering |
| 2 | `framing/gap-and-literature.md` §§1–4, `framing/edge-of-scope.md` §2 | solid; the positioning taxonomy needs the five dimensions |
| 3 | `analysis/statistics.md`, `design/arms-and-validation.md` §§2–3 | solid; the equivalence assumptions need their consequences beside them |
| 4 | `design/tool-surface.md`, `design/correctness.md`, `design/corpus.md` | solid; the metric section must be assembled from four documents |
| 5 | `design/harness.md` §§9, 16 | thin — the deviations register cannot exist before the series |
| 6 | **empty** | nothing to write until the sweep runs |
| 7 | `framing/aim-and-contributions.md` §§8–12, `framing/edge-of-scope.md` §7 | the skeleton exists; the verdicts require §6 |

**The honest reading of that column:** six of seven chapters have draft material, and the thesis is therefore waiting on **data**, not on writing. The one chapter that cannot be drafted is the one whose every sentence is a number.

---

## 11. The PhD adaptation, kept as a contingency

If the thesis is continued at doctoral level: keep §1–5 and §7, split §6 into two — the main comparison, and the mechanism with the surface — and add two study chapters: a **substrate replication** (the same harness against PostGIS or GRASS) and a **gate implementation** chapter, in which the validating boundary is not merely tested but built and evaluated. That converts C3 from a finding into an artefact, which is the difference between a master's and a doctoral contribution here.

---

## 12. Five lines, and one sentence

1. **Seven chapters in the faculty's frame**, with three of them in the main part — instrument, execution, results — because the instrument is the contribution and cannot hide inside procedure.
2. **IMRAD survives as an order of inference** (I = §1–2, M = §3–5, R = §6, D = §7) and design science as the narrative of §3.1; neither needs a chapter of its own.
3. **82 pages of body**, of which §6 has 18 and §4 has 14 — and §4 is written first while §6 is generated rather than written.
4. **Six of the seven chapters already have draft material**; the one that does not is the one whose every sentence is a number, and that is the schedule's real constraint.
5. **No chapter on tools, on the framework, on partial conclusions or on surface size** — each would either duplicate another chapter or report a study that was not run.

**In one sentence.** The thesis is seven chapters inside the faculty's frame, ordered by IMRAD's chain of inference, budgeted at 82 pages with the instrument first and the results last, and its contents page is designed so that an examiner can see in ten seconds where the instrument is, where the result is, and what the work deliberately does not claim.

---

## 13. Cut log

| Cut | Source note | Reason |
|---|---|---|
| the eight-chapter design-science table of contents, its 90-page budget and its chapter→draft map | `toc-blueprint.md` | a second structure that contradicted the faculty frame (which needs "Materials and methods" and "Summary and conclusions"), and its content was built on retired design: 2 front-ends × 2 models × {S1, S2, S3, codegen}, 1,800 runs, a 50-tool surface. Design science survives as §3.1, the budget is unified at 82 pp |
| the six-chapter IMRAD structure that merged methods, instrument and execution into one 26–30 pp chapter | `metaplan-and-imrad.md` B.2 | at that length the instrument disappears into procedure and the deviations register has nowhere to live; the IMRAD *logic* is kept in §8 and the numbering follows the faculty |
| the seven-chapter table of contents as it stood | `table-of-contents.md` §3 | its sections still carried the retired design: 40 tasks, the 5 / 15 / 30 ladder, `min_surface`, the 2 × 2 with TOST, H1–H7, a capability axis with three levels, ED and RRR as headline metrics, a 90-run control slice |
| the H1–H7 numbering throughout, with the hypothesis-to-section map | `table-of-contents.md` §4, `toc-blueprint.md` §§3, 6 | the ledger is H1 / H2 (N1 → N4) / H3 (expressible share) plus D1–D4; a table of contents that schedules the wrong hypotheses schedules the wrong chapters |
| the "aim of ~5-15-30" ladder sections (§6.3) and the 2 × 2 "validation boundary" section (§6.4) as separate results | `table-of-contents.md` §6 | one is retired, the other is absent from the design; §6.2 and §6.4 now carry the depth contrast and the detection sites instead |
| the capability axis as a chapter-6 section (§6.6) and §3.2 | both notes | `d-2` fixes one model; a section reporting a capability effect would report a comparison that was not run |
| the "interoperability swap" section (same server × agents) | `toc-blueprint.md` §6.8 | retired with the front-end factor; auditability and server replaceability survive as a descriptive section (§6.8) |
| two page budgets (82 and 90/91) and two writing orders | all three notes | one budget (§9) and one order (§5); a second order is a second answer |
| the appendix list that included "the S3 catalogue with 50 tools and the nesting proof" | both notes | the surface does not nest; appendix B lists nine operations with the parity table and the `checks` file |
| the metaplan printed as a table | `metaplan-and-imrad.md` A.2 | a table of four columns in an introduction reads as a form; it becomes four paragraphs (§3, ch. 1) |

**Added while pruning**, because the cut had removed the only home of the claim: the statement that the merge preserved three structures and that one of them had to win (§1), the argument for a separate execution chapter as the place where reliability is demonstrated (§1), the three-row integration rule scheduled into §7.4, the further-work list with a cost for every item (§7.6), and the honest chapter-by-draft map that says the thesis is waiting on data rather than on writing (§10).

**Kept, because each is the only place in the repository where its claim is made:** the formal rules for a contents page (§2), the single table of contents with its page budget (§3), the chapter → contribution → claim → audience table with its empty-cell test (§4), the writing order (§5), the list of deliberate absences (§6), the inference-chain checklist with its numerical control (§7), the IMRAD must/must-not table (§8), the budget table with its two consequences (§9), the draft map (§10), the PhD adaptation (§11), and the five lines (§12).
