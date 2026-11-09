---
id: framing/aim-and-contributions
title: "Aim and contributions"
type: note
status: live
language: en
question: "What does the thesis establish, and what is new about it?"
tasks: [TASK-4]
sources: [thesis-aim.md, novelty-and-contributions.md, scientific-contribution.md, implications.md, impact-on-ai-gis-integration.md]
updated_date: '2026-11-07'
---

# Aim and contributions

> What does the thesis establish, and what is new about it?
>
> Two halves that must agree. §1–§5 fix the **aim** so that it is decidable — a reviewer is entitled to ask *how will I know it has been achieved* — and §6–§8 fix the **contribution**, ranked by durability rather than by ambition. §9–§11 say what follows for practice and for the discipline, each thesis with its condition attached; §12 is the list of sentences that must not appear anywhere.
>
> Pruned and translated 2026-11-07 (`TASK-21`): 7,207 → 6,011 words, five source notes → fourteen sections. Rewritten against the live design (K · N1 · N4, 80 tasks, 960 runs, MDE 14.0 pp) and against the claim ledger in `design/arms-and-validation.md` §2.

---

## 1. The aim, in one sentence

> **The aim of the thesis is to establish whether, and to what extent, the way geoprocessing operations are exposed to an agent — a catalogue of named operations with declared constraints, or generated PyQGIS code — changes the correctness of the artefact that lands on disk, and to identify the mechanism of that change: the role of correctness conditions enforced in the interface rather than in the model's reasoning.**

Three components, each measurable:

| Component | Question | Where it is answered |
|---|---|---|
| **whether** | does the difference exist at all? | H1 — N4 against K, one confirmatory test |
| **to what extent** | for which kinds of task does it hold, and where does it vanish? | H3 — the difference against the **expressible share** of the card |
| **through what** | is it enforcement, or representation? | H2 — the depth curve between **N1 and N4 on an identical surface**, plus D2's `detected_by` |

The third component is the one that changed, and the change makes the aim *more* decidable rather than less: the earlier version wanted to isolate enforcement by comparing gated code with a tool surface, which the design does not contain; the live version isolates it by comparing **two catalogue conditions that expose the same nine operations in the same words** and differ only in what is checked. A pure enforcement contrast, at the price of not knowing what gated code would do — stated as such in `framing/edge-of-scope.md` §4.2.

---

## 2. Specific aims

| # | Aim | Measure | Chapter |
|---|---|---|---|
| **A1 — measurement** | estimate the difference in the share of correct artefacts between conditions, with an interval and an explicitly stated smallest detectable difference | TSR, Δ, **MDE 14.0 pp at τ = 10** | 6.1 |
| **A2 — mechanism** | establish how correctness changes with **enforcement depth** (schema → invariants and terminal conditions) and whether the difference grows with the task's **expressible share** | the depth contrast plus the pre-registered interaction | 6.2, 6.4 |
| **A3 — diagnosis** | establish **where** errors are detected: by the language, by the model's own invariant, by an execution error, or only by the oracle after the fact | the four-valued `detected_by`, the in-loop catch rate, error-class repeatability | 6.3 |
| **A4 — instrument** | build and publish the instrument: 80 task cards with predicates and negative controls, the artefact oracle, the harness, two taxonomies frozen before the measurement | availability and reproducibility of the package | 4, appendices |
| **A5 — practice** | formulate a rule for designing tool surfaces: what to encode in the signature, what to check after every step, what to leave to post-hoc control | a three-step rule derived from the data, not from opinion | 7.2 |

**A5 is an aim, not decoration.** Without it the thesis is a measurement with no application — and the competitions score "practical potential" explicitly (`draft/titles.md` §7.4).

**What the aim is not:**

1. A verdict about **MCP as a protocol** — what is studied is a design dimension of the interface, on one server and one model.
2. A comparison of **protocols** (MCP against REST or OGC API – Processes) — argued in chapter 2, named as further work (`framing/what-we-study.md` §11).
3. An evaluation of **language models** — the model is a condition of repeatability, not an object of assessment.
4. A judgement of **cartographic quality as aesthetics** — the predicates check agreement, not beauty.
5. A ruling about **domains** — 13 cards in one family is not power to say anything about a domain, and transfer to chemistry or medicine is further work (`framing/edge-of-scope.md` §2).
6. **A product**: the harness is an instrument, and the server is a treatment, not a deliverable.

### 2.1 Three kinds of aim — the layout the diploma requires

| Kind | Content |
|---|---|
| **cognitive** | explain where, in the process of exposing geoprocessing to an agent, a silent error arises and what stops it; decide whether enforcing conditions in the interface carries over into artefact correctness |
| **methodological** | provide the measuring instrument: artefact scoring instead of trajectory scoring, an in-loop catch rate, the expressible share as a moderator, a register of **where** an error was detected |
| **practical** | give integrators a decision rule — which requirements to encode in the signature, which to check on the result of every step, which to leave to post-hoc control — and show when an interface is a cost rather than a gain |

---

## 3. How to recognise that the aim has been achieved

The aim is achieved when each of the following is **directly readable** in the thesis:

- [ ] **A1** — the difference is given with an interval **and** with the MDE, and "undecided" is distinguished from "absent" in words, not in a footnote;
- [ ] **A2** — the depth contrast is estimated **and** so is the dependence of the difference on the expressible share, each with its falsifier;
- [ ] **A3** — failures are distributed over **places of detection** (language / own invariant / execution error / oracle), not reduced to one percentage;
- [ ] **A4** — the corpus, the oracle, the harness and both taxonomies are available and reproducible by a third party;
- [ ] **A5** — the rule in §7.2 is derived from the results rather than from the literature.

**The aim is achieved even with a zero or negative result**, provided A1–A4 are readable — and then A5 says when the interface does not help. That is not a loophole: it is a criterion written down in advance, and it is why the thesis does not depend on the sign of the difference.

---

## 4. Aim, statement, hypotheses, title

| Element | Role |
|---|---|
| **aim** (this document) | what is to be established — decidable |
| **thesis statement** (`draft/thesis-draft-v0.md` §1.3) | what the thesis claims about the world — refutable |
| **claims H1–H3, D1–D4** (`design/arms-and-validation.md` §2) | how the statement is tested — each with a falsifier |
| **title** | "an assessment" — that is, an aim, not a statement assumed in advance |

Consistency: the title says *assessment*, the aim says *to establish*, the statement says *I expect that*, the claims say *I will measure it like this*. Four levels of one intention, and none of them prejudges the result.

---

## 5. The comparison alone is not the contribution

This is the section that has to be read before anything is written into chapter 1.

**"Code generation versus MCP in GIS" is the hook, not the novelty.** It is the framing a supervisor and a committee grasp in ten seconds, and it belongs in the title and the introduction. As a *claim* it is the most copyable and most attackable thing in the thesis.

| Attack a reviewer will make | Is it fair? | What answers it |
|---|---|---|
| "function calling against code generation in GIS is already published" (`luo2026geojson`) | partly: they compare two architectures inside one system and score task accuracy | the control: same engine, same tasks, a fixed surface, executed artefacts, repetitions |
| "the MCP benchmark space is crowded" (MCP-Atlas, MCP-Universe, LiveMCPBench, MCP-Bench) | fair, but none is GIS and none has a code condition | say it in the introduction; do not hide it |
| "two conditions is an ablation, not a thesis" | fair if the comparison is all there is | the depth contrast, the failure taxonomy, repeatability, cost |
| "the dichotomy is false — real agents discover through a server and then write code" | **fair, and dangerous** | admit the omission in the scope section, and name it as further work (`framing/what-we-study.md` §6) |
| "you measured your harness's tool calling, not the integration method" | fair | one harness pinned (`d-4`), the "one CLI" objection answered in the limitations, and the harness's capability table checked in the pilot |

**Three tests decide whether a candidate is a contribution at all:** can a competitor copy it in a week? does it survive a null result? is it a claim, or only a setting? *"I compared MCP with code generation"* fails all three: copyable in a week, dead if the effect is null, and it asserts nothing by itself.

---

## 6. The four candidates, ranked by durability

| # | Candidate | Copyable in a week? | Survives a null? | Verdict |
|---|---|---|---|---|
| **C1** | **the instrument** — 80 frozen cards, an artefact oracle with negative controls, a four-valued detection register | **partly** — `gisagentbench2026` already publishes 349 tasks with ground-truth files and tolerance-aware structural checks | yes | still the most reusable piece, but it is **an instrument and a protocol**, not an instrument from scratch. Never claim "the first" |
| **C2** | **the enforcement mechanism** — does correctness rise with what the surface *checks*, on an identical surface? | no — it needs two conditions with identical surfaces and descriptions, and a reason to believe the second layer matters | yes — a flat curve with a flat catch rate is informative (outcome W2) | **the strongest conceptual claim**, and nobody has measured it in any domain, let alone GIS |
| **C3** | **where errors are caught, and how repeatably** — `detected_by`, the in-loop catch rate, error-class repeatability | no — it needs the four-valued register and four repetitions | yes | the most distinctive empirical result, and the one most likely to survive whatever H1 does |
| **C4** | **the paradigm comparison itself** | **yes** | only if significant | the hook, and the framing of chapters 1–2 |
| C5 | cost per success in a spatial toolchain | medium | yes | a good supporting section, not a headline |
| C6 | the substitution slice (same agent × other server, same server × other client) — R1 | medium | yes | **currently missing and underrated**: it tests the value the protocol claims for itself |

What C1–C3 have in common: they are contributions **about how to know**, not about who won. That is also why they survive the most likely empirical outcome — the literature already hints the effect may be small or negative (`song2025helpor`, `mastouri2025automcp`).

**C6 deserves a note, because it is the cheapest contribution in the whole list and it is not in the design.** The substitution slice — the same agent against a different server, and the same server against a different client, about 90 runs — measures **substitutability**, which is the one value MCP claims for itself and nobody has measured: that a server can be replaced, or a client changed, without touching the agent. It survives a null trivially (a low substitutability would be a finding about the ecosystem, not about this thesis) and it cannot be copied in a week, because it needs a second server and a second client that are actually comparable. If time appears after the main series, this is the first thing to run; if it does not, it is named in chapter 7 as the measurement that would complete the argument, which is a stronger position than leaving it unmentioned.

**A downgrade that has to be absorbed.** An earlier round ranked the validation boundary first on the strength of a 2 × 2 that would have given *generated code* an equivalent gate, with an equivalence test to show the gap closing. That cell is not in the design. The claim is therefore narrower and still novel: **enforcement is graded inside one surface, and its effect is measured causally.** What is lost is the sentence "a protocol advantage is largely a validation advantage" — that now becomes the *interpretation* offered for H2's result, explicitly conditional on the missing cell, not a measured finding.

---

## 7. The contribution statement, in three claims

Three claims, in this order. Chapter 1 states them; chapters 5–7 discharge them.

**C1 — instrumental (methodological).**
*A reproducible instrument for comparing two ways of exposing one GIS engine to an agent: frozen task cards with oracle artefacts and per-card negative controls, a spatial predicate vocabulary adapted from the current best practice in artefact scoring, and protocol-level measures — in-loop catch rate, error-class repeatability, four-valued detection site, cost per successful task — with run-to-run repeatability as a first-class outcome rather than an assumption.*

Note, because it is the part most likely to be overclaimed: artefact-scored GIS evaluation is **no longer novel** — `gisagentbench2026` publishes ground-truth-file matching and `geocontra2026` publishes contract verification. C1 must therefore claim **replication, the interface factor, the enforcement contrast and repeatability**, and never "the first instrument that checks real outputs". The editorial formula for chapter 3: *"an instrument that adapts and combines the current best practice of artefact scoring"*.

**C2 — empirical.**
*On an identical QGIS runtime, a catalogue of named operations and free-form code generation differ in artefact correctness — by an amount given with an interval against a stated MDE — and they differ in where their errors are caught, in how repeatably they fail, and in cost per successful task; the correctness difference is tested as a function of the task's expressible share.*

**C3 — mechanistic (conditional).**
*Within an identical surface, correctness rises with the depth of enforcement: with what the interface checks on the state before and after an operation, and not only on the shape of the call. The interpretation offered — that a large part of what looks like the value of a protocol is the value of a standardised validation boundary — is a hypothesis this design can support but not isolate, because the cell in which generated code receives the same boundary is not run.*

C3 is the sentence a committee remembers, and it is the one that stays true if C2 comes back null.

**Two things C1–C3 must never say**, and both are easy to write by accident:

1. **"We compared integration methods between GIS and AI."** Two of many; plugins, `qgis_process` wrappers, GUI automation and bespoke REST APIs are not in it. Say: *"the two methods that scale"*.
2. **"MCP is better/worse."** The claim is about two interfaces on one engine, at one revision, with one model.

### 7.1 Where "integration methods between GIS and AI" is the right frame, and where it is a trap

As a *frame* it is excellent: it places the tool surface and generated code as two points in a space that also contains QGIS plugins, `qgis_process` wrappers, function calling over a bespoke API, agent frameworks and GUI automation. A reader immediately sees why the choice matters, and the title keeps the phrase *"jako metody integracji"* for exactly that reason (`draft/titles.md` §2).

As a *claim* it over-reaches: two of those methods are tested, one of them twice. The scoped sentence is therefore:

> "…compares two integration methods — a described tool surface and free-form code generation — on an identical GIS engine."

The broader frame belongs in **chapter 2** as a positioning taxonomy, not in chapter 1 as a contribution. Five dimensions do the work, and they cost a week of reading rather than a chapter of experiments:

| Dimension | What it separates |
|---|---|
| **coupling** | in-process library · external server · GUI automation |
| **contract** | implicit (library API) · declared (schema) · none (vision) |
| **validation point** | pre-execution · at runtime · post-hoc |
| **coverage** | closed catalogue · open code · whatever the UI allows |
| **provenance** | a validated plan object · the text of a script · a screen recording |

That table gives C1–C3 their vocabulary, and it lets the thesis say honestly: *"these two methods are the two that scale, and here is how to choose between them"* — instead of "we compared the integration methods", which is not true.

---

## 8. Where each contribution is discharged

| Chapter | What it establishes | What must be visible |
|---|---|---|
| 1. Introduction | C3 as the research question, C1 as the instrument | the three conditions drawn as a figure with the enumeration difference marked, not described in prose |
| 2. Literature review | positioning, never contribution | the taxonomy table: coupling · contract · validation point · coverage · provenance |
| 3. Materials and methods | C1 | the instrument-qualification table, the version pins, the 960-run budget and its justification |
| 4. Results | C2 | the depth contrast, the interaction with the expressible share, intervals and the MDE beside every comparison, per-family and per-tier splits, cost per success |
| 5. Summary and conclusions | C3 | the enforcement sentence with its condition, and the limitations: one model, one engine, one task stratum, nothing below 14 pp |
| 7. Practice and further work | A5, C6 | the interface-choice rule, the substitution slice, and the missing gated-code cell as the first item of further work |

---

## 9. Implications are a vector: outcome × audience × action

**An implication without an audience and an action is a comment.** Each thesis below is therefore written as: *who*, *what they stop doing or start doing*, *on the strength of which result*. And because the result is unknown, the implications are **branched** — not as a hedge, but because in every branch something specific follows.

| Question | Who asks it | What the thesis gives | Claim |
|---|---|---|---|
| "which interface should I expose to an agent over my GIS?" | an engineer building a GIS assistant | a rule: coverage (code) against control and repeatability (catalogue), depending on the task family | H1, D1 |
| "does validation in the interface actually buy correctness?" | the same, plus an architect | the depth contrast, with the price in turns and tokens | H2, D3 |
| "are agent errors in GIS loud or silent?" | an analyst, a quality auditor | signatures: the catalogue errs on tool or parameter choice, code errs silently on CRS and geometry | D2 |
| "can I reproduce the agent's result next month?" | anyone signing off a deliverable | error-class repeatability and the share of runs that repeat identically | D1 |
| "is the interface choice about effectiveness or about cost?" | a decision-maker, a client | cost per success, which can invert the correctness ranking | D3 |
| "which requirements can I actually enforce?" | the same architect | the expressible share of a task, coded before the measurement | H3 |
| "what should a GIS agent benchmark report?" | a methodologist, a reviewer | the proposal: validation state and repetitions as part of the protocol, not as a footnote | follows from D1, D2 |

### 9.1 The six outcomes, and what each one means

The design pre-registers six outcomes (`design/experiment.md` §11). Each has a different practical and a different disciplinary implication — which is the strongest argument that the experiment is worth 960 runs.

| Outcome | For the practitioner | For GIScience |
|---|---|---|
| **W1 — gain, with a monotone depth curve** | build the surface, and make it enforce: the gain is not in naming the operations but in checking their results | a measured return on encoded domain invariants — the first dose–response for validation in GIS |
| **W2 — gain, flat depth curve** | a bounded, named surface helps even without gates; the mechanism is the action space, not validation | the representation of operations matters independently of enforcement — a claim about tool design, not about protocols |
| **W3 — mechanism without gain** | gates buy auditability, not correctness: keep them for the trace, do not expect fewer errors | the boundary changes the **structure** of failure, not its level — the honest and probably most useful result |
| **W4 — nothing anywhere** | do not decide architecture on this; decide on cost and maintenance | the interface is not the lever in this task class; look at description quality, prompt, model |
| **W5 — the other way** | the surface costs more than it saves: fragmentation and turn count | agrees with the code-first literature and locates the boundary elsewhere than intuition suggests |
| **W6 — uninterpretable** | nothing: a ceiling, a floor, broken parity or drift | a reported failure of the instrument, which is itself a contribution to anyone building one |

---

### 9.2 Three questions at the defence, and the answers to have ready

1. **"Isn't this just a benchmark paper?"**
   No: benchmarks rank models, and this isolates an interface. The deliverables that outlive any ranking are the instrument (C1) and the detection-site result (C3), and the enforcement claim is testable independently of which condition wins.

2. **"Why should I care about the tool surface if generated code is just as good?"**
   Because the surface gives for free what code generation must be given by hand: a validated call boundary, a machine-checkable record of what ran, and the ability to swap the server without touching the agent. That is the honest answer to "what does the interface buy" — and if H2 comes back flat, the answer narrows to the record and the swap, which is still a reason and is stated as such rather than as a rescue.

3. **"You tested one model, one harness and one engine."**
   Correct, and all three are pinned and reported rather than treated as nuisance: the claim is scoped to a capability-controlled stack, the limitation is stated before it is asked, and the model × interface interaction is the first item of further work. An interaction the design cannot see is not a gap in the argument; it is a boundary of the claim, and the difference between those two is the whole of §10.

## 10. What the thesis does not settle

The list has to be in chapter 7 explicitly, because it is what separates a mature thesis from an ambitious one:

- whether an agent writes **better maps than a person** — no human comparison is run;
- what follows for **throughput and production scale** — time and tokens are measured, not production capacity;
- whether any of it **transfers to ArcGIS, GRASS or PostGIS** — one engine, one granularity (portability shown on five GRASS tasks, `framing/edge-of-scope.md` §3.5);
- whether it **transfers to multimodal agents** reading maps from screenshots — a different paradigm, outside;
- whether an agent can **plan a whole multi-stage study** — tiers T3–T4 are six to ten steps, not projects;
- whether the value is **universal** — value depends on the recipient's bottleneck (`framing/what-we-study.md` §1.1);
- whether **MCP beats REST or OpenAPI** — that condition does not exist and will not;
- whether **model capability** changes the picture — the model is frozen, and the interaction is the first item of further work;
- what **gated code generation** would do — the missing cell, named everywhere it matters.

---

## 11. Four theses for GIS in the age of agents — each with its condition

Not futurology: each is a consequence of a measured quantity, and each is false if its condition fails.

### T1 — the bottleneck is the contract, not the model

Models can write PyQGIS. What they cannot do is **guarantee that the result is spatially correct**, and a better model does not fix that, because it is not a prediction problem but a validation problem. If H1 shows a difference and H2 shows a depth effect, the thesis is strong: **the maturity of a GIS agent depends on the quality of the invariant, not on the quality of the generator.** If both are flat, the thesis is weaker and more interesting: the bottleneck is elsewhere.

Institutional consequence, conditional on W1 or W2: investment in "AI for GIS" should go into **predicate vocabularies and quality control**, not into further model deployments.

### T2 — the scarce resource becomes correctness control, not code

When a machine writes the code, code stops being scarce. What is scarce is what distinguishes a correct map from one that merely looks right: axis order, geometry type, NoData, attribute completeness, style predicates. This thesis is the **operationalisation of that resource** — 80 cards with oracles are not "a test set" but **formalised domain knowledge about what "correct" means in geoprocessing** (and note the MAUP hazard: the cards aggregate to communes, and the partitioning is part of the answer).

Consequence: whoever builds a shared, citable vocabulary of correctness for GIS operations decides what agents can do — regardless of whose protocol they use.

### T3 — standardisation moves toward validation, not toward tools

GIS has a tradition of standardising the **description and invocation** of spatial operations: WPS, then OGC API – Processes. Those standards assume a client that knows what it is asking for. A language model does not — and that is why it needs a machine-checkable contract, not only a description.

Conditional on H2: the next standard contribution for GIS is not another invocation protocol but a **validation vocabulary for spatial operations** — exactly what MCP does not define and what OGC could.

### T4 — automation moves error from visible to invisible

The most GIS-specific thesis, and the one rooted in the discipline's own history: the most dangerous cartographic error has never been the one that shouts, but the **credible and wrong map**. If D2 shows that the code condition fails silently (a shifted CRS, a nearly valid geometry) while the catalogue fails loudly (no such tool, wrong parameter), the conclusion is a warning: **agentic GIS raises the share of errors nobody sees.**

Consequence: with an agent in the process, **post-execution validation is mandatory**, not optional. Without an agent, checking the inputs was often enough; with an agent the error arises during execution, after the inputs were fine.

---

### 11.1 What integration does to expertise

One consequence deserves its own paragraph because it is the one that is easiest to get wrong in the conclusions: **integration does not automate expertise, it relocates it.** The domain knowledge does not disappear when an agent performs the operation; it moves from the analyst's judgment into whatever the interface encodes — the declared unit, the required CRS, the terminal condition, the predicate. Where nobody encodes it, it does not move anywhere: it is simply absent, and the availability of the agent then means **silent errors at scale** rather than fewer errors.

That reframing is what makes the work's topic a geoinformatics topic rather than a software-engineering one, and it is why the object of study is the *placement* of the invariant (in the model's context, rebuilt every run, or in a versioned component written once) rather than the quality of any model.
## 12. The integration policy rule — three rows, one alarm

For every requirement of a task, the decision is one of three, and it depends on two measurable things: the **expressible share** and whether the requirement is **checkable at all**.

| | When | What you do | Cost |
|---|---|---|---|
| **encode** | the requirement is expressible and checkable | a parameter plus a gate in the server | one-off, and somebody's |
| **check in the loop** | the requirement is checkable but not expressible in a signature | an invariant after the operation, with the verdict returned to the agent | one-off, cheaper |
| **check after the fact** | the requirement needs a reference value | an oracle or QA on the artefact, with an explicit threshold | recurring, and outside the loop |

**The practical rule, and the alarm:** if **every** requirement in your implementation lands in the third row, you have an agent that cannot be supervised, only audited afterwards. That is the definition of an implementation that must not run without a human at the result. And the good news, which is testable in days rather than years: most of these invariants **already exist in the data** — the CRS registry with areas of use, the Processing algorithm metadata, geometry-validity rules, unit declarations in files. The invariant layer is **derivable**, not inventable.

### 12.1 Three levels of integration, and the one that is not integration

| Level | What is exposed | Who checks the requirements | Effect |
|---|---|---|---|
| **I. wrapper** | `run_gdal(args)` / `pyqgis(code)` | nobody | the same silence as in code generation |
| **II. named operation** | `buffer(layer, distance, unit)` plus a description | the schema, and part of the invariants | a type and unit error becomes **loud** |
| **III. contract-bound operation** | the same, plus a target CRS, a mask, an expected extent | the server checks the **intent stated in the prompt** | a semantic error becomes **loud** |

**"We wrapped GDAL, GRASS and QGIS in a server" is level I** — a change of transport, not an integration. Real integration is levels II–III, and it requires domain work: naming the operations, declaring the units, defining the conditions. Which is precisely why the enforcement layer here is a **treatment** and has to be documented like the task cards.

---

## 13. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| the 2 × 2 with gated code, and the equivalence test (±20 pp margin) as the *main* contribution | `novelty-and-contributions`, `scientific-contribution` | the cell is not in the design. The enforcement claim is narrowed to the N1 → N4 contrast (§6, §7) and the missing cell is named everywhere it bounds an interpretation |
| **"MDE ≈ 20–25 pp at 50 tasks, α = 0.0083"**, repeated in three sections | `scientific-contribution`, `thesis-aim` | three generations stale. The live figures are **80 tasks, r = 4, MDE 14.0 pp at τ = 10, one confirmatory test at α = 0.05** with Holm over a family of two (`analysis/statistics.md` §6) |
| "1 218 runs", "two models, one host", "3–5 repetitions", "50 tasks" | several | retired design generation; 960 runs, one model, one harness, r = 4 (`design/experiment.md` §0) |
| the L1–L4 ladder as the surface-size manipulation ("5 ≈ 15 is a result") | `novelty-and-contributions`, `scientific-contribution` | the tool-count ladder is retired with `min_surface`; the manipulation is enforcement depth on a fixed surface |
| the hypothesis-by-hypothesis table mapping H1–H7 onto contributions | `scientific-contribution` | a second numbering of the claim ledger; §9.1 uses the six pre-registered **outcomes** instead, which is what a reader can actually follow |
| the "four cells of the 2 × 2, four different conclusions" table | `implications` | replaced by the six outcomes, which are the design's own vocabulary and are already pre-registered |
| the "two front-end and model factor" defence answer | `novelty-and-contributions` | there is one harness and one model (`d-2`, `d-4`); the answer is now the pinned-stack limitation, and pretending otherwise would be the one place a reviewer could catch the thesis overclaiming |
| the six-row "positioning taxonomy" as a *contribution* | `novelty-and-contributions` | it is chapter 2 material and is listed as such in §8; as a contribution it would be an unmeasured table |
| the title options section | `novelty-and-contributions` | titles have an owner (`draft/titles.md`); the only survivor is the subtitle wording, which lives there |
| the four "institutional" and forecasting paragraphs of the impact note, kept as four theses | `impact-on-ai-gis-integration` | eleven paragraphs of prose became §11 plus four numbered predictions in §13.1 below; a thesis does not need two essays on the same three ideas |

### 13.1 Four predictions, marked as predictions

Testable within a year, tested by nobody in this thesis: (1) geoinformatics servers will be assessed by **gate coverage** rather than by tool count, with a "validation depth" field as they now have an API version; (2) agent benchmarks will gain an **artefact-oracle column** beside call scoring, because call scoring cannot distinguish "called correctly, computed wrongly"; (3) the **silent error** will become a standard evaluation axis in GIS agent tests, as unit tests once became in code; (4) an **invariant registry** will emerge, starting with CRS and units because the data already exist.

Added while pruning, because the cut had removed the only home of the claim: §7.1 (the "integration methods" frame as a frame and not as a claim, with the five-dimension positioning taxonomy), §9.2 (three defence questions with their answers), §11.1 (integration relocates expertise rather than automating it) and the note on C6, the substitution slice.

Kept, because each is the only place in the repository where its claim is made: the one-sentence aim with its three measurable components (§1), the five specific aims with live measures and the six non-aims (§2), the three kinds of aim (§2.1), the achievement checklist (§3), the aim-statement-claim-title distinction (§4), the three contribution tests with the reviewer attacks (§5), the four candidates ranked by durability with the absorbed downgrade (§6), C1–C3 with the anti-overclaim formula (§7), the chapter map (§8), the implication vector with the six outcomes (§9), the list of what is not settled (§10), the four theses with their conditions (§11), the policy rule with its alarm and the three levels of integration (§12), and the predictions marked as such (§13.1).

---

## 14. Five lines, and one sentence

1. **The aim is decidable and survives a null.** Whether, to what extent, through what — three components, each with a measure, and the achievement criterion is the readability of A1–A5, not the sign of the difference.
2. **The comparison is the hook; the contribution is how to know.** The instrument, the enforcement contrast and the detection-site distribution are what cannot be copied in a week and what stay true if the effect is zero.
3. **The main claim is narrower than it was, and honest.** Enforcement is graded *inside one surface*, causally; the gated-code cell that would let the thesis say "a protocol's advantage is a validation advantage" is not run, and that sentence appears only as a conditional interpretation.
4. **Every implication carries an audience and a condition.** Six pre-registered outcomes, six different practical consequences — which is what makes the experiment worth 960 runs rather than a report of who won.
5. **The rule for practice is three rows with an alarm.** Encode, check in the loop, check after the fact — and if everything lands in the third row, the implementation must not run without a human at the result.

**And in one sentence.** The thesis establishes, with an interval and a stated MDE, whether exposing geoprocessing as a constrained tool surface rather than as generated code changes what lands on disk, grades that change by how much the surface enforces and by how much of the task the surface can carry, reports where the errors were caught and how repeatably, and delivers an instrument and a three-row rule that remain useful whichever way the comparison comes out.
