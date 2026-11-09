---
id: framing/scope-and-character
title: "Scope and character of the thesis"
type: note
status: live
language: en
question: "How large is the thesis, what kind of study is it, and what may it claim?"
tasks: [TASK-1, TASK-4, TASK-14]
sources: [scope-decision.md, is-this-needed.md, degree-fit.md, thesis-character.md, what-to-focus-on.md, geoai-trend.md, explain-like-im-ten.md]
updated_date: '2026-11-07'
---

# Scope and character of the thesis

> How large is the thesis, what kind of study is it, and what may it claim?
>
> Merged 2026-11-07 from `scope-decision.md`, `is-this-needed.md`, `degree-fit.md`, `thesis-character.md`, `what-to-focus-on.md`, `geoai-trend.md`, `explain-like-im-ten.md`. **Pruned and translated the same day** (`TASK-21`): 9,541 → 7,669 words. The five sections below are the five questions a committee asks in the first ten minutes, in the order it asks them.

**Everything here is written against the live configuration** (`d-1`–`d-5`): three conditions K/N1/N4, 80 task cards, r = 4, **960 runs**, one model, one harness, MDE 14.0 pp, families P/A/C as the selection axis.

---

## 1. Scope: is the thesis too large?

**It was — roughly twice over, in the generation that preceded the current design. The cut was made on the right axis: arms and contrasts, not tasks.** Task count is what buys statistical power; contrasts and models are what make a study unbuildable. Cutting tasks to save time is the mistake that looks like progress.

### 1.1 The arithmetic that decides it

| Cost driver | Scales with | Currency |
|---|---|---|
| oracles and fixtures | the number of **tasks** | person-weeks, not compute |
| the sweep | the number of **runs** = tasks × conditions × repetitions | hours of machine time, cheap on HPC |
| analysis and writing | the number of **contrasts**, each needing a section, a table and a defence | person-weeks |

The binding constraint is therefore **cards and contrasts**; runs are nearly free. That single observation decides the design: keep the tasks, drop the arms. Halving the corpus from 80 to 40 would halve the card work and destroy the power the MDE calculation shows the thesis can barely afford (14.0 → 19.8 pp at r = 4, and the floor rises from 3.8 to 5.4 pp).

### 1.2 What is in, and what is out

| **In** | Why it stays |
|---|---|
| 80 task cards, families P/A/C, four tiers | power, the family contrast, and the corpus is contribution C4 |
| the nine-operation catalogue, one surface | it is the manipulated variable, not a product |
| conditions **N1 and N4** | the *only* pair that turns a ranking into a mechanism |
| one model, one harness, pinned | scope decision; capability and harness become stated limitations |
| the expressible share, coded per card | the moderator that makes H3 falsifiable |
| `detected_by`, S3, S4/S4b, cost per success | free — computed from runs that already exist |
| κ double-coding on 20 % of runs | one week, and it converts a rubric into a measurement |

| **Out** (named as future work) | What is lost | Why the loss is affordable |
|---|---|---|
| a second model | the capability gradient | the claim becomes conditional on model and version; a capability axis is the first extension |
| a second front-end / harness | the "one CLI" objection in factor form | one pinned harness (`d-4`); the objection is answered in the limitations, not with a doubled series |
| a tool-count ladder (5/15/30/50) | the "how many tools" dose–response | with nine fixed operations the ladder is replaced by **enforcement depth**; surface size returns as future work |
| a separate gating 2 × 2 | a crossed experiment on validation | **folded into the arms**: N1 (schema) vs N4 (invariants + terminal conditions) *is* the gating contrast, at zero extra runs |
| a hybrid condition (catalogue, then code) | what practitioners actually do | one paragraph in chapter 7 admitting it, and the top future-work item |
| a second server, an interoperability swap | MCP's strongest practical claim | a design proposal in chapter 7 |
| adversarial cards as a study | security breadth | three cards as a qualitative probe, not a test |
| a transfer probe, a fidelity bound | cross-agent transfer | both already flagged in the literature as unsolved |

The honest totals: the retired generation committed to **~2,800 runs, two models, two harnesses and nine contrasts**, which serialises to 9–12 months of work. The live design commits to **960 runs, one model, three contrasts** — a master's thesis's worth — while keeping every task, which is what keeps the instrument intact.

### 1.3 The test: what the abstract must still be able to say

> We built an artefact-scored instrument for agent-performed geoprocessing (C4) and used it to compare three ways of exposing the same nine GIS operations on an identical engine (C1); correctness rises with enforcement depth, the difference grows with the task's expressible share, and giving generated code the same terminal conditions narrows the gap to a point that can be stated with an interval (C2, C3).

If every clause survives the cut, the scope is right. Notice what is **not** there: a second model, a hybrid condition, a second server, a capability gradient. Those are sentences the retired design was paying months for.

### 1.4 If a supervisor insists, add back in this order

1. **A second model on a subset** (+120 runs, +2 weeks) — restores the capability gradient as a sign replication.
2. **A random-catalogue control** (+320 runs) — answers "you authored a convenient surface".
3. **A hybrid condition** (+240 runs) — closes the "why choose?" hole.
4. **A second server** (+2 weeks of server work) — the interoperability claim.
5. Everything else is genuinely future work.

The rule that keeps this list from growing a third time: anything outside §1.2 is **conditional** — added only *after* the main sweep is accounted for and the H1/H2 analysis is closed, never "if there is time".

### 1.5 The one thing not to cut

Do not merge N1 and N4 into a single catalogue condition to save 320 runs. That pair is the only part of the study that produces a **mechanism** rather than a ranking, it is what makes C2 and C3 exist, and it is what still says something interesting if the main comparison comes back undecided. Everything else on the cut list is breadth; this is the thesis.

### 1.6 The future-work paragraph, in the shape it should be written

> Three extensions follow directly. A second GIS substrate (PostGIS or GRASS) would test whether the interface effect is engine-specific; a hybrid condition — catalogue discovery followed by generated code — would model what practitioners actually do; and scaling the catalogue towards production size would test whether the effect of a surface saturates. Each is a re-run of the same instrument with a changed configuration, which is the practical argument for treating the instrument as a first-class contribution rather than a by-product.

---

## 2. Is the research needed?

The harder version of the scope question: *will anyone care, and will the answer still be true when it lands?*

**Short answer: the question is needed, but not the one in the working title — and the fix is to rescope the *claim*, not the work.** Keep the instrument and the comparison; move the centre of gravity from "which interface wins" (fashionable, contestable, possibly answered by industry, dies on a null) to **"when an agent does spatial work, how do we know the result is right — and how much of the interface's value is that guarantee?"** The second question is needed regardless of which protocol is in vogue, and it is the one place where a GIS department has an advantage no AI lab has.

### 2.1 What is genuinely needed

| Needed | Why it survives the fashion cycle |
|---|---|
| **A correctness-first instrument for agent-performed spatial work** | the domain's own literature says evaluation is weak and irreproducible (`yu2026geoagentbench`, `nust2018`, `konkol2019`); a frozen, oracle-scored harness is wanted whoever builds the agents |
| **A measured answer about interface choice in the domain where wrongness is silent** | a wrong map raises no error (`monmonier2018`, `maceachren1992`, `iso19157`); general benchmarks score answers and calls, not CRS, topology and extent |
| **The validation-boundary measurement** | nobody has measured, in any domain, whether the benefit of a protocol surface is the protocol or the **guaranteed check before execution** — a mechanism claim, not a ranking, and currently untested |

### 2.2 What is not needed, and should stop being defended

| Not needed | Why |
|---|---|
| "the first evaluation of MCP in GIS" | MapHub, OGSAgent and `ichms2026_mcp_geodata` exist; the claim is false and unnecessary |
| a headline ranking of MCP against code generation | two competitors will publish rankings with more models, and `song2025helpor` shows the direction is not guaranteed; the value is not the ranking |
| "MCP is the future of GIS–AI integration" | not a research claim, and it dates the thesis to a spec version |

### 2.3 The obsolescence risk, honestly

The real threat is not that somebody answers the question; it is that **the field routes around it**. The direction of travel in agent tooling is retrieval and compression — dynamic tool search, coarse tools with composite parameters, "write code that calls the tools" hybrids — because everyone has noticed that huge catalogues cost context and degrade selection. If that becomes standard, a result of the form "50 tools is worse than 15" becomes historical trivia.

Three mitigations, all already in the design: **frame results as a mechanism, not a number** ("coverage rises and selection degrades with surface size; the net is a knee", which stays true when the knee moves) · **never tie the claim to a spec version** ("a protocol-mediated tool surface", cite the snapshot, note the mechanism is protocol-agnostic) · **keep the enforcement contrast as the headline**, because a validation guarantee is not a fashion.

### 2.4 The decision test

| Question | The honest answer |
|---|---|
| Does anyone's decision change if the answer is X rather than Y? | **Yes** — an author of a GIS tool server deciding how much to validate, and an analyst deciding whether to let an agent touch their project |
| Will the **claim** still be true in two years? | the mechanism and the instrument: yes; the specific percentages: probably not. So claim the former |
| Can it be finished in the time available? | only at this scope: 960 runs, 80 cards, one model |
| Would a null result still teach something? | **yes** — the instrument, the failure taxonomy, the repeatability result and the catch-rate distribution all survive a tie |

### 2.5 Pivot and kill criteria, fixed now

- **Pivot to instrument-first** if, after the pilot, qualification fails twice (strong model below the 20 % TSR floor on tasks the catalogue covers) — the interfaces cannot be compared yet, and the instrument becomes the thesis.
- **Pivot to the mechanism-only thesis** if N1 and N4 are indistinguishable in the pilot while the K-versus-N4 contrast is large: the depth claim has no signal, and the runs belong to the comparison.
- **Stop and re-plan** if, before the sweep, a paper appears with an executed, replicated, cross-paradigm GIS comparison. *Status 2026-11-01:* GISAgentBench closes the "artefact scoring" half and GeoContra half of the gating argument; neither compares interfaces, so the criterion has not fired — but it came close, and it must be re-checked before the pilot. If it fires, the differentiator is the **spatial oracle vocabulary plus the enforcement measurement**, i.e. replication-plus-mechanism, which is a respectable thesis with a different chapter 1.

### 2.6 The paragraph to say out loud

> Spatial analysis is being handed to agents, and the field is choosing between interface styles on the strength of demos. In GIS an incorrect result usually looks correct — no exception is raised, the map is simply wrong — so the choice has to be measured on executed spatial outputs, not on plans or code similarity, and it has to be measured repeatedly, because reliability is the property a practitioner depends on. This thesis builds that instrument, uses it to compare protocol-mediated tool exposure against code generation on an identical engine, and tests the mechanism behind any difference: whether the value lies in the protocol or in the validation boundary it imposes. The instrument and the mechanism outlast whichever interface is fashionable.

---

## 3. Is it a proper Geoinformatics MSc topic?

**Yes — but as first framed it read as "an AI-systems evaluation that happens to use GIS", and a Geoinformatics committee will say so.** The fix is not to change the topic: it is to reframe it in geoinformatics vocabulary, to add the GIScience canon the design silently relies on, and to make sure a third of the corpus is *spatial analysis* rather than toolbox primitives.

### 3.1 The three objections, and the answers that work

| Objection | Fair? | Answer |
|---|---|---|
| "this is testing AI tools, not GIS — you could swap QGIS for Blender and the study would still run" | **partly**: the *design* is engine-agnostic, the *measurement* is not | the outcome variables are spatial — CRS agreement, geometric validity, topological relations, extent IoU, attribute preservation, cartographic properties; ground truth here is a **spatial predicate**, and designing that vocabulary is geoinformatics method |
| "where is the geoinformatic contribution?" | fair if the answer is "we compared two interfaces" | three: a spatial correctness vocabulary for executed artefacts; a **spatial error taxonomy** (silent CRS error, invalid geometry, topological near-miss, attribute misalignment, plausible-but-wrong classification); and a measured comparison of two **geoprocessing interface styles** — the question OGC has asked since WPS |
| "this needs no cartography or geodesy knowledge" | fixable, and currently thin | the cartographic family (classification, symbolisation, layout, export) plus CRS and accuracy predicates make cartographic competence visible — and it is the family where the expressible-share argument gets its sharpest evidence |

### 3.2 What is genuinely geoinformatic here

| Anchor | Where it lives | Why a GIScience committee recognises it |
|---|---|---|
| spatial predicates as correctness | oracle vocabulary, chapter 4 | ISO 19157 territory — positional, thematic and logical-consistency quality — applied to machine outputs |
| a spatial failure taxonomy | chapters 4 and 6 | error propagation and "plausible but wrong" outputs are canonical GIScience concerns |
| a domain model of geoprocessing | the nine-operation catalogue | curating operations by workflow family is applied geoprocessing knowledge, not prompt engineering |
| interoperability of geoprocessing interfaces | chapter 2 | MCP against OGC API – Processes is a standards question, and standards are core geoinformatics |
| cartographic output assessed | family C | classification method, symbolisation and layout completeness are cartography, measured objectively |
| an applied artefact | harness and corpus | Polish MSc theses expect a working thing; the instrument is the working thing |

### 3.3 The reframing that fixes the degree fit

The thesis currently sits in *AI evaluation*. Move it one shelf, into **geoprocessing interoperability and quality assessment**, where geoinformatics already has a mature evaluation culture (OGC compliance testing, SDI assessment, geoprocessing service quality). One sentence does it:

> Web geoprocessing has standardised how spatial processes are described and invoked (WPS, then OGC API – Processes), and those standards assume a human or scripted client that knows what to ask for. Agentic clients do not: they discover capability from a machine-readable catalogue and compose calls on the fly. This thesis evaluates the interface that makes geoprocessing agent-accessible — protocol-mediated exposure of QGIS operations versus generated PyQGIS — holding the engine constant and scoring what lands on disk.

That makes MCP a participant in an existing geoinformatics conversation rather than a new hobby. It costs one subsection of chapter 2 and one paragraph of chapter 1, and it changes how the committee hears the whole thesis.

**Two titles in geoinformatics vocabulary** (both keep the novelty; the chosen one is in `draft/titles.md`):

- *Protocol-mediated geoprocessing: a controlled, replicated evaluation of agent access to GIS operations via MCP versus generated code on an identical QGIS runtime*
- *Evaluating geoprocessing interfaces for AI agents: spatial correctness, reliability and cost of MCP tool exposure versus PyQGIS code generation*

### 3.4 Three additions the degree requires

1. **At least a third of the corpus must be composite spatial analysis, not single operations.** A corpus of buffer/reproject/clip reads as a toolbox test; site selection, zoning, accessibility analysis, suitability modelling and multi-criteria overlay read as GIScience. Tiers should mean *analytical depth*, not call count.
2. **Cite the GIScience canon the design leans on**: ISO 19157 (data quality), ISO 19115 (metadata), positional accuracy and error propagation, uncertainty visualisation, map communication and classification-method choice (equal-interval vs quantile vs Jenks), and VGI quality if OSM appears in fixtures. Ten references, one afternoon, and chapter 2 stops looking like it was written by a computer scientist.
3. **Make the cartographic family real.** Not decoration: classification method, class count, colour ramp, label placement, layout completeness and export resolution, checked against what the request asked for. It is the only place where the thesis demonstrates cartographic judgement.

### 3.5 Scorecard against typical MSc Geoinformatics criteria

| Criterion | Score | Comment |
|---|---|---|
| clearly defined spatial problem | 4 | strong once §3.3 lands |
| geoinformatic method development | 4 | spatial predicate vocabulary and failure taxonomy |
| cartographic competence demonstrated | **2 → 3** | only through family C; needs the properties checklist |
| spatial data handling, CRS, topology | 4 | fixtures, EPSG:2180, predicates |
| literature grounded in GIScience | **2** | currently AI-heavy; see §3.4 |
| applied artefact of professional standard | 5 | harness, corpus, frozen manifests |
| evaluation rigour | 5 | better than most GIScience MSc work |
| balance — not a CS thesis in disguise | **3** | fixed by §3.3 and §3.4 |

The two 2s are the answer: the topic is proper, the *grounding* is one-sided.

### 3.6 Four practical matters

1. **Supervisor fit matters more than committee fit.** An agent thesis in a geoinformatics programme needs a GIS-side supervisor comfortable with LLM agents, or a co-supervision pair. A remote-sensing specialist with no agent interest will drift the topic towards something safer and less interesting.
2. **Prepare one slide titled "what is geoinformatic here?"** — §3.2 compressed. It will be asked, and a confident 40 seconds ends the line of questioning.
3. **Lead the appendix with a composite task.** If the first three examples are "reproject a layer", "count features", "buffer 500 m", the committee pattern-matches the thesis to a software test suite.
4. **Keep the design-science framing explicit** (`peffers2007design`): geoinformatics programmes accept DSRM readily, and it gives the harness the status of a research artefact rather than an engineering side-product.

---

## 4. What character must the thesis have?

One sentence: **a research thesis, and in the sense of §III.9 of the faculty rules, an experimental one** — testing a hypothesis, manipulating specified factors, establishing causal relations. Not a review, not a design thesis — although it contains a review component (chapter 2) and a design component (the instrument, chapter 4).

### 4.1 What the rules say

| Paragraph | Content | Application |
|---|---|---|
| §III.8 | a thesis may be a **review**, a **research** or a **design** thesis | choose one as dominant |
| §III.10a | on second-cycle *general-academic* programmes all three are admissible | no obligation to be a design thesis |
| §III.9 | a research thesis is **experimental** if it is aimed at **testing a research hypothesis**, studying the course/variability of phenomena **under specified factors**, and establishes **causal relations** | this is the definition of the work, point by point |
| §III.12 | a master's thesis is **in-depth**, settles questions of advanced specialist knowledge using **specialist methods and tools** | 960 runs, mixed models, typed oracles — met with room to spare |
| §II.6 | for research theses requiring experiments, the supervisor submits, **with the topic**, a short description of the planned experiment indicating its conditions; the **status of an experimental thesis** is granted by the College on the programme team's motion | see §4.4 — two different things |

### 4.2 Point-by-point fit with §III.9

| Requirement | What satisfies it |
|---|---|
| **testing a research hypothesis** | H1 (enforcement changes correctness), H2 (correctness rises with enforcement depth), H3 (the difference grows with the expressible share) — written down, falsifiable, each with a named test |
| **phenomena under specified factors** | the manipulated factors are the **enforcement layer** (K, N1, N4), with task family and the expressible share as the moderators |
| **causal relations** | not a correlation over observations: the same tasks, the same engine, the same model, the same harness, the same prompt — only the interface differs, four repetitions per cell |

All three conditions are met not "generally" but **in the exact form the rules name**, which is rare and worth stating in the introduction: the thesis does not "have a research character because something was studied", it satisfies the experimental criterion of §III.9.

### 4.3 Why not the other two characters

| Character | Definition (§III.8) | Why it is not this thesis |
|---|---|---|
| **review** | collecting, analysing, ordering and critically discussing the literature | that is chapter 2 only; the argument does not end with a conclusion from the literature but with a measurement |
| **design** | realising an **applied goal**, joining theory to practical application, comprehensive documentation of a solution | a tool is built, but **the tool is not the goal**; if it were, the thesis would have user documentation instead of hypotheses |

**The one real risk of misclassification:** the committee reads "the student built a research environment" and calls it a design thesis. The answer is one sentence (§4.7).

### 4.4 Two things that sound alike

| | **Experimental character** (§III.9) | **Status of an experimental thesis** (§II.6) |
|---|---|---|
| what it is | a methodological property | a formal decision of the College |
| who decides | it follows from the method; the supervisor and reviewer assess it | the College, on the programme team's opinion |
| condition | hypothesis, factors, causality | "**laboratory experiments**" and an indication of the **conditions** |
| consequence | how the thesis is assessed | organisational |

Honestly: this experiment is **computational, not laboratory**, so the §II.6 status does not follow directly from the text. But the experiment does require **specified conditions** (GPU, model server, container image, pinned versions), which is precisely what the rule asks to be indicated, the description is cheap to prepare, and the status is sometimes needed organisationally. **Recommendation: prepare the description (§4.6) and ask the supervisor whether to apply. Do not decide alone.**

### 4.5 What this means for structure and writing

1. **The hypotheses must be in the text**, not only in the notes: a section "research questions and hypotheses", each with an operational definition and a test. Without it a reviewer has no way to read the thesis as experimental.
2. **The instrument is the method, not the goal.** Title chapter 4 "Materials and methods — the measuring instrument" (or keep it inside chapter 3), never "the tool we built". Wording: "an oracle was constructed in order to **measure**…", not "an application was built that…".
3. **The factor must be called a factor**, with its levels and its within/between type — that is the evidence of §III.9, not decoration.
4. **The review chapter stays** as a component (the rules recommend it), but its conclusion leads to hypotheses, not to a summary of the literature.
5. **Design elements** (harness, catalogue, containers) are described as **conditions of measurement reproducibility**, not as engineering output. The repository and CI are evidence, not content.

### 4.6 The ready experiment description

> **Description of the planned experiment (per §II.6 of the WNoZiGP UMCS diploma rules 2025/2026)**
>
> **Aim and hypotheses.** The aim is to establish whether the way geoprocessing capability is exposed to an AI agent — the MCP protocol versus code generation — changes the **correctness, repeatability and cost** of spatial tasks on an **identical engine**, and whether any observed effect comes from the protocol itself or from the validation enforced before and after execution.
>
> **Factors.** The principal factor is the **enforcement layer**, at three levels: code generation with interpreter feedback only; a named-operation catalogue with input schema validation; the same catalogue with invariants and terminal conditions. Moderators: task family (preparation, analysis, cartography) and the task's expressible share. Dependent variables: artefact correctness (all oracle predicates satisfied), in-loop catch rate, error-class repeatability, self-verification content, provenance completeness and cost per successful task.
>
> **Material.** 80 frozen task cards with typed predicates and negative controls, spatial reference data for Poland in EPSG:2180 with checksums, a nine-operation catalogue with declared units and terminal conditions, and a parity table mapping every operation to its library equivalent.
>
> **Conditions.** QGIS in headless mode inside a container pinned by digest; one language model served locally with pinned digest, quantisation and sampling parameters; a fresh container per run with the cache disabled; limits of 25 turns, 10 minutes and one token budget, identical in every condition; the run order drawn in permuted blocks with a recorded seed.
>
> **Scale.** Three conditions × 80 tasks × 4 repetitions = **960 runs**, with an estimated 100 h of engine time on 8–16 parallel Slurm tasks. Every run, failed ones included, is archived and accounted for.
>
> **Quality control.** Oracles and tolerances frozen before the sweep; blind double-coding of the error taxonomy on 20 % of runs with kappa reported; ten tasks repeated after the sweep as a drift check.
>
> **Ethics and safety.** No human participants; the security probe concerns only the author's own local tool servers — no third-party systems are tested.

### 4.7 The sentence for the defence

> The thesis has a research character and satisfies the experimental criterion of §III.9: it tests hypotheses stated in advance, manipulates specified factors (enforcement layer, with family and expressible share as moderators) and establishes causal relations because everything outside the factor is held identical — the same engine, tasks, model and harness. The instrument is a **condition of measurement**, not the goal: its value is that it can settle the hypotheses, not the completeness of its documentation.

### 4.8 This week

1. Paste §4.6 into the form and **ask the supervisor** whether to apply for the §II.6 status.
2. Add to chapter 3 a subsection "research questions and hypotheses" — H1, H2, H3, each with its test and its falsification criterion.
3. Rename the working chapter titles: "instrument" becomes part of **materials and methods**.
4. Write into the pre-registration: "the thesis has a research character, experimental in the sense of §III.9" — so the classification is not renegotiated at assessment.

---

## 5. What to focus on, what can be claimed, and whether it holds

### 5.1 The focus in one sentence

**Hold the GIS engine constant and vary only how the agent is allowed to touch it — a catalogue of named operations versus generated code, and within the catalogue only how much is checked — score what actually lands on disk, repeat every task four times, and manipulate the one thing that might explain any difference: the enforcement boundary.**

Everything that is not that sentence is support (instrument, corpus, catalogue) or consequence (failure taxonomy, cost, guidance). Anything that competes with it for months of work is a scope error.

### 5.2 The point

People are already handing spatial analysis to agents, and the choice of *interface* is being made on demo videos. In GIS that choice is unusually consequential because **wrongness is silent**: a CRS mistake produces a valid, beautiful, wrong map with no error anywhere. So the question is not "can an agent do GIS work" — partly yes — but **"which interface, at what cost in correctness, reliability and money, and why?"** The "why" is what makes it a thesis rather than a benchmark: if the advantage is the *check before execution* rather than the protocol, that changes what anyone should build next.

### 5.3 The claim ledger

Renumbered to the live hypotheses; the retired V1–V7 list is in §7.

| # | Claim | Operational test | Falsified if |
|---|---|---|---|
| **H1** | the interfaces differ in artefact correctness | TSR in N4 versus K, paired at task level, mixed logistic with a random task effect | the interval contains zero at an MDE of 14 pp (undecided), or the difference is negative and ≥ 14 pp (refuted, W5) |
| **H2** | correctness rises with enforcement depth | N1 versus N4 on identical surfaces; a trend contrast, not a pair of tests | a flat or non-monotonic depth curve with a flat catch rate — the gates would be inert |
| **H3** | the difference grows with the task's expressible share | interaction between condition and the coded share | a flat interaction across the whole range, or a correctness difference on cards whose share is *none* |
| **D1** | the interfaces differ in **repeatability**, not only in the mean | S3 error-class repeatability, plus predicate-level agreement across the four repetitions | both equally deterministic, with identical error-class distributions |
| **D2** | the interfaces have **distinct failure signatures** | `detected_by` and the double-coded taxonomy, kappa reported | the distributions are indistinguishable |
| **D3** | cost per **success** can invert the ranking | token, call and time logs divided by successes | one condition dominates on both quality and cost everywhere |
| **D4** | the instrument itself is constructible and stable | frozen cards and oracles; agreement across repetitions; kappa against a second coder | oracles disagree between runs, or the pilot cannot clear the instrument floor |

`D` claims are descriptive: they do not become confirmatory by being interesting.

**Cannot be claimed, do not try:** aesthetic quality · generalisation beyond QGIS · production-scale surfaces · security in general (three cards is a probe) · "MCP improves GIS agents" · anything below the MDE.

### 5.4 What is new, precisely

| Contribution | Precisely what is new | What it is *not* |
|---|---|---|
| **the comparison** | the first controlled, executed, replicated head-to-head of protocol-mediated exposure and generated code on an *identical* engine | not "first MCP work in GIS" (MapHub, OGSAgent exist); not "first artefact scoring" (GISAgentBench) |
| **the enforcement measurement (H2)** | whether a validation boundary makes generated code **reach parity with** a protocol surface — the question GeoContra leaves open (it shows contracts help code; it never compares to a tool surface) | not "validation improves correctness" — already published |
| **reliability as an outcome (D1)** | repetition, determinism and recovery reported in GIS agent evaluation | not a new metric — `strickland2026pareto` proposed the idea |
| **the expressible share (H3)** | a coded moderator that predicts *where* the interface difference should appear | not a new covariate concept; the coding is |
| **a spatial failure taxonomy (D2)** | silent CRS, invalid geometry, topological near-miss and aggregation error mapped to observable symptoms | not a security taxonomy (`zhang2025msb` has that) |
| **the instrument (C4)** | adapted, frozen, reusable; adds the expressible-share coding and typed terminal conditions | **not** invented from scratch — cite GISAgentBench for the scoring logic |

Ranked by durability: **H2 > D1 > H3 > D2 > the comparison > the instrument.** The top two are mechanism and reliability claims, which is exactly why they survive a tie in the headline.

### 5.5 Can it withstand critique?

| Attack | Holds? | What must be done for it to hold |
|---|---|---|
| "GISAgentBench already scores real output files" | **yes**, if instrument novelty is not claimed | cite it, adopt its tolerance logic, claim *adaptation plus the interface factor* |
| "GeoContra already proves validation helps" | **yes, only if** substitution is tested | keep N1 and N4 distinct; frame as parity, not improvement |
| "your effect is one harness's quirk" | **weakest leg** | instrument qualification, a pinned harness, a scoped claim, and the limitation stated |
| "your nine-operation catalogue is a strawman you wrote" | **weakest leg #2** | anchor operations to documented workflows, freeze, family-balance, report the token tax, and name the random-catalogue control as the check that was not run |
| "80 tasks cannot resolve modest effects" | **yes** | state the MDE (14.0 pp), phrase claims as ≥ MDE, task-level analysis, never single-run tests |
| "the dichotomy is false — real agents do both" | **yes** | admit it in chapter 7 and name the hybrid condition as the first extension |
| "it will be obsolete in two years" | **partly** | mechanism framing, no spec version in the title, and the enforcement contrast as the durable claim |

**Net assessment:** the thesis withstands critique **if and only if** every claim is written at the strength the design can carry. It fails if the original framing is kept (benchmark + ranking + first instrument) — that framing is what the 2026 papers already took away. The narrowed version is smaller, duller in the abstract, and much harder to knock down.

### 5.6 The order of work that follows

1. Analysis hierarchy and MDE into the pre-registration (one primary, Holm for the rest).
2. The catalogue design note: nine operations, atomic, documented, frozen, with the parity table.
3. **Ten cards end-to-end**, one per family × tier, with oracles and negative controls — then the pilot.
4. Build **N4** before scaling the corpus; the enforcement layer is the thesis.
5. Eighty cards, then the sweep; the failure taxonomy double-coded while runs are landing.
6. Write chapters 3 and 4 **now**, not after the data.

---

## 6. Where it sits in the GeoAI current

> Positioning for chapters 1 and 2. State of the field checked 2026-11-01. The conclusion: the thesis lands in the **intersection of two currents that stopped being a vision in 2026 and became infrastructure** — standardisation/interoperability, and trustworthiness/validation — and **not** in agent-building or benchmarking, where the competition is densest.

### 6.1 Six currents

| Current | What defines it | Evidence |
|---|---|---|
| **F1 — the "autonomous GIS" agenda** | GIS not as a tool but as an artificial geospatial analyst; the programme is institutionalising | *GIScience in the Era of AI: A Research Agenda Towards Autonomous GIS* (Annals of GIS); Kazazi and Li, *From Tool to Collaborator…* (preprint, III 2026) with the **ARE** model and a layered validation stack |
| **F2 — standardisation and infrastructure** | agents are to be attached through standards, not wrapper upon wrapper | Esri UC VII 2026 (ArcGIS positioned as a spatial layer reachable **through MCP**); FGDC adopting autonomous-GIS goals into SDI modernisation 2026–2027; the **GAS** framework (V 2026) |
| **F3 — trustworthiness and validation** | from "check the result" to "validate the episode": provenance, repeatability, code verification, geospatial sanity checks, uncertainty-bounded claims | the ARE validation stack; *Toward Governance-Aware Autonomous GIS* (IX 2026), which states that "field-tested evaluations of governance controls remain limited" |
| **F4 — benchmarks and evaluation** | from text matching to executable artefacts; growing task sets | GeoAgentBench, GeoAnalystBench, GeoBenchX, GISAgentBench, GeoContra; a dedicated AAG session on benchmarking and reliability |
| **F5 — system building** | agent architectures, often multi-agent; gains on one- and two-tool tasks, losses on long ones | GIS Copilot, GISclaw, GeoAgent, GeoAIAgent |
| **F6 — domain applications and multimodality** | urban planning, crises, health; agents reading maps and imagery | Earth Copilot, GeoAgentic-RAG |

### 6.2 Where this work stands

| Current | Relation | Why |
|---|---|---|
| **F2 — standardisation** | **core** | "protocol versus code" is a question about the **shape of the geoprocessing interface** — the same question OGC has asked since WPS |
| **F3 — trustworthiness** | **core** | the terminal conditions are one layer of the validation stack operationalised; error-class repeatability is reliability |
| F4 — benchmarks | neighbour, deliberately **not** a competitor | the thesis compares, it does not rank; it adds no leaderboard |
| F1 — agenda | dependent neighbour | the agenda **postulates** validation; this thesis **measures what it is worth** |
| F5 — systems | outside | the conditions are deliberately minimal, because the system is an instrument, not the contribution |
| F6 — applications | outside | the domain is controlled (QGIS), not studied |

Sentence for chapter 1: "The thesis concerns the layer that the autonomous-GIS agenda names as the condition of deployment — validation of results — and measures it where the architectural decision is actually made: at the agent–engine boundary."

### 6.3 Three nearest neighbours, and the sentence that separates each

| Neighbour | What it does | Separating sentence |
|---|---|---|
| Kazazi and Li (2026), ARE and the validation stack | proposes a frame and **postulates** episode validation | "They propose a validation layer; this thesis measures **what one of those layers is worth** — whether it substitutes for a bounded interface or merely supplements it." |
| GeoContra (2026) | contracts plus a repair loop raise generated-code correctness by 26.6 pp | "They show that contracts **help code**; this thesis asks whether, with contracts, code **catches up with** a protocol surface — the question they leave open." |
| GISAgentBench / GeoAnalystBench | task sets with executable artefact scoring; model rankings | "They rank models; this thesis **isolates the interface** and reports repeatability and cost per success, not a position in a table." |

The rule: **every neighbour is named in chapter 2 and every one gets a separating sentence.** A thesis that does not name its neighbours looks unaware of the field; one that names them and separates itself looks mature.

### 6.4 Four dating risks, and how each is defused

**R1 — MCP becomes the default** (Esri, VII 2026). If the dominant vendor connects ArcGIS to agents through MCP, "should we use MCP" stops being a question. *Defused by* never framing the thesis as "MCP or code", but as **"what does the protocol contribute, and what does it cost"** — which becomes *more* important under adoption, because it is a question about the price of the default.

**R2 — validation becomes a commodity.** If the validation stack and the contract approach land in platforms, the terminal conditions stop being something one builds. *Defused by* treating the enforcement layer as a **manipulated variable**, not as a contribution: what is contributed is the measurement of its substitutive value.

**R3 — benchmarks saturate.** Another GIS task set stops being news. *Defused by* keeping the mechanism claim as the headline and the instrument as its condition.

**R4 — models improve, and this is the real threat to the result.** If both conditions saturate at high capability the difference vanishes — not because the interface does not matter, but because it stopped mattering *at that capability*. A single-model result ages in a month.

*Defused by* phrasing the claim as a **shape**, not a number: "the gap between interfaces narrows and closes at capability level X" is a statement about the form of the dependence, and it does not age with the models. This is where the current and the scope decision disagree, and the disagreement is resolved in favour of scope: the capability axis is **not** in this thesis (`d-2`, one model), so the defence is (a) report the effect as explicitly conditional on this model, version and date, (b) name the capability gradient as the first extension, and (c) treat a saturation observed at one capability as W6 (uninterpretable), never as evidence that interfaces do not matter.

### 6.5 What to write, and where

| Place | Content | Length |
|---|---|---|
| §1, paragraph 1 | market and institutional motivation: Esri (MCP for ArcGIS, VII 2026), FGDC (SDI-AI, 2026–2027) — **adoption outpacing evidence** | 3 sentences |
| §1, paragraph 2 | the gap: nobody has measured how much of the protocol's value is validation | 3 sentences |
| §2.1 | N1: the autonomous-GIS agenda and the ARE model | 1 page |
| §2.2 | F2: from WPS through OGC API – Processes to MCP — the same problem, a new client | 2 pages |
| §2.3 | F3–F4: the validation stack, GeoContra, the benchmarks — and what they do not measure | 2 pages |
| §2.4 | the neighbour table from §6.3, four columns: work, contribution, what it does not measure, separating sentence | 1 table |
| §7 | the contributions from `framing/aim-and-contributions.md` plus the limitation: one engine, one model, 80 tasks | 3 pages |

### 6.6 Bibliography additions (metadata verified 2026-11-01; DOIs to confirm)

| Item | Metadata | For |
|---|---|---|
| agenda, autonomous GIS | *GIScience in the Era of Artificial Intelligence: A Research Agenda Towards Autonomous GIS*, **Annals of GIS** | F1, motivation |
| Kazazi and Li, ARE | *From Tool to Collaborator: Rethinking GIScience as GIS Becomes Agentic and Autonomous*, SSRN preprint, III 2026 | F3, nearest neighbour |
| governance review | Subramanian and Jain, *Toward Governance-Aware Autonomous GIS…*, arXiv **2609.16232**, IX 2026 | F3, the "field-tested evaluations remain limited" gap |
| GAS | *Geospatial Agentic Services*, V 2026 | F2, standardisation of agentic services |
| GeoAgent (IJGIS) | Lin, Xu, Wu, Du, *GeoAgent: a hierarchical LLM-based multi-agent architecture for autonomous spatial analysis*, **IJGIS**, II 2026 | F5, the systems neighbourhood |

**Methodological note:** with preprints proliferating in this current, **never cite a version summarised by an aggregator** — confirm metadata and claims on `arxiv.org/abs` or in the journal version. Same rule as in `framing/gap-and-literature.md`.

### 6.7 What not to do in order to "fit the current"

1. **Do not add a multi-agent layer.** The current has it and praises it; this thesis compares interfaces, not agent architectures.
2. **Do not position the work as a framework.** Frameworks are N1; this is a measurement, and a framework without a measurement is exactly what the current already has in excess.
3. **Do not chase terminology.** "Agentic", "autonomous", "GeoFM" — once in §1, not in every paragraph.
4. **Do not announce that the thesis "answers the agenda".** It answers **one question from the agenda**, and saying so narrowly is what keeps the claim credible.

---

## 7. What was pruned, and why

| Cut | Came from | Reason |
|---|---|---|
| the item-by-item cut of the 2,800-run design (arms S1/S2/S3, meta-tool, hybrid, two models, two front-ends, 12 anchored reproductions) | `scope-decision` | that design no longer exists; the surviving content is the **rule** (cut arms, not tasks) and the arithmetic behind it, kept in §1.1–§1.2 |
| the "six decisions grew the plan to 3,566 runs" audit and its three budget paths A/B/C | `scope-decision` | it audited a design that the next round of decisions replaced wholesale; the freeze rule survives as one sentence in §1.4 |
| V1–V7 claim ledger | `what-to-focus-on` | renumbered onto the live hypotheses H1–H3 plus four descriptive claims; a second numbering of the same claims is how two systems of reference end up in one thesis |
| "four possible theses" A/B/C/D table | `is-this-needed` | the choice has been made and is recorded (`d-1`, `d-2`); the pivot criteria survive in §2.5 |
| the "make the model an axis" recommendation (§R4 in the source) | `geoai-trend` | it contradicts the scope decision (`d-2`, one model). Kept as a **recorded disagreement** in §6.4 with the three-part defence that replaces it |
| the plain-language version as a separate section | `explain-like-im-ten` | its content is now the opening paragraphs of §1, §2.2 and §5.2; a second telling of the whole thesis in the same document invites the two to drift |
| the "eight domains of ten" phrasing carried over from the draft | several | contradicts `d-3`: family is the selection axis, domain is a descriptive label (`design/corpus.md` §3) |

---

## 8. Five lines, and one sentence

1. **Question.** Does the interface through which geoprocessing is exposed to an agent change the correctness of the artefacts it produces, and how much of any such difference is the validation boundary rather than the protocol?
2. **Design.** Three conditions on one pinned harness — code execution (K), narrow tools (N1), composed tools with schemas and preconditions (N4) — 80 tasks, 4 repetitions, 960 runs, nine operations over the traditional-geoprocessing stratum.
3. **Measure.** Task success from the spatial predicates (a wrong result of correct type still fails), plus precision at completeness, the four wrong-result signatures, and cost per successful run; McNemar on paired tasks, task as the unit of analysis.
4. **Decision rules.** R1 the direction is the interface's if N1 and N4 differ and K sits outside the pair; R2 the difference grows with the expressible share of the operation (H3); R3 the thesis fails its own comparison if N4 ≤ N1.
5. **Contribution.** A repeatable instrument that outlives the answer, the measured interaction between interface and validation boundary, a failure-signature vocabulary, and a cost-per-success curve — positioned where OGC's interoperability question meets the autonomous-GIS agenda's demand for trustworthy results.

**And in one sentence.** **The thesis is a scope-cut, correctly-classified experimental study of one question — whether the way geoprocessing is exposed to an agent changes the correctness of what lands on disk, and how much of that is the validation boundary rather than the protocol — carried by an instrument that outlives the answer, positioned in geoinformatics at the point where OGC's interoperability question meets the autonomous-GIS agenda's demand for trustworthy results.**
