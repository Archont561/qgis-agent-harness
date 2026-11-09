---
id: draft/metaplan
title: "The metaplan: how it is, why it is so, how it should be, what to do"
type: note
status: live
language: en
question: "What is the argument of the thesis in four moves, and what has to happen for it to hold?"
tasks: [TASK-13]
updated_date: '2026-11-09'
---

# The metaplan: how it is, why it is so, how it should be, what to do

> A metaplan asks four questions of one object — *how it is*, *why it is so*, *how it should be*, *what to do about it* — and the answers only hold together if each column earns the next.
>
> Asked **twice** here, because the thesis has two objects. **Board A** is the argument: the state of agent-performed geoprocessing, its causes, the state it should be in, and the instrument that would get it there. That board is the drafting scaffold for §1.1–1.4 (`draft/structure.md` §1) and is kept as a whole for a poster. **Board B** is the work: where the thesis stands on 2026-11-09, why it stands there, where it has to be at the defence, and the actions that move it, each with the gate that says it is done (`writing/plan.md` §1).
>
> **Two rules the method imposes, and this document is held to.** A card is one idea, short enough to fit a card. And the fourth column is not a wish list: every action on Board B names the gate that closes it, so "what to do" cannot quietly become "what one hopes".

---

## Board A — the argument

### How it is

- **Catalogue, not text.** Agents reach geoprocessing through named operations with schemas — MCP now, WPS and OGC API – Processes before it.
- **Calls are scored.** The literature evaluates the call and the plan; the executed artefact is scored rarely.
- **Code wins in GIS.** Eleven systems, zero protocol comparisons: the discipline's consensus is code generation.
- **MCP-in-GIS exists.** As systems, and as one dataset-discovery benchmark. Not as analysis.
- **Structural validity is free.** In 2026 the decoder guarantees schema conformance, so it distinguishes no interface.
- **One empty cell.** Two paradigms, one engine, repeated — nobody occupies it.

### Why it is so

- **The type carries no meaning.** Metres and degrees are the same float; a schema cannot see a coordinate system.
- **Evaluation went where it was cheap.** Calls are loggable; meaning needs an oracle per task, and oracles cost days.
- **The protocol standardises the envelope, not the operation.** Schemas describe arguments, not spatial conditions.
- **Pass rates do not stack.** Different tasks, oracles and engines give two quantities with one name.
- **The canon stays home.** ISO 19157 supplies the vocabulary for correctness; the agent literature does not use it.
- **One identical engine is expensive,** and it has to be built before anything can be compared.

### How it should be

- **Conditions attached to operations.** The server checks them on every run, not when a model happens to write an assertion.
- **Georeference on every result.** CRS, lineage and provenance travel with the artefact, not with the conversation.
- **Artefacts scored, not calls.** Predicates and tolerances, one oracle per card, a negative control beside it.
- **Replication built in.** r = 4, so reliability is measured rather than averaged away.
- **Both paradigms on one engine.** Same tasks, same loop, same limits — the interface is the only variable.
- **Verdicts before data.** Three hypotheses with falsifiers, and a null result that still says something.

### What to do

- **One surface, three depths.** K, N1, N4: code, catalogue at the schema, and catalogue with invariants and contracts.
- **Nine operations, 80 cards** in three families — process, analysis, cartographic — with tolerances frozen before the first run.
- **A taxonomy frozen before measurement.** Seven failure classes and eight coordinate-system classes, plus the *detected-by* field that separates caught from unnoticed.
- **960 runs.** Three conditions × 80 tasks × r = 4, paired, seeded rotation, weekly blocks.
- **Power stated in advance.** MDE 14.0 pp, between-task variance from the pilot (ICC 0.661), Holm over the two secondary hypotheses.
- **Cost per success, not accuracy alone.** Tokens and turns are reported beside every correctness figure.

**Where each column comes from.** Column one: `framing/gap-and-literature.md` §§1–2, §5. Column two: `design/correctness.md` §§2–3. Column three: `framing/gap-and-literature.md` §3, `design/correctness.md` §4, `design/arms-and-validation.md` §2. Column four: `design/tool-surface.md`, `design/corpus.md`, `design/runs.md`, `writing/plan.md` §2.

---

## The four paragraphs the board becomes

`draft/structure.md` §1 rules that the board is not printed as a table in the thesis: printed, it reads as a form. It becomes four paragraphs in §1.1–1.4, **each closing with the sentence that opens the next**. Those sentences are the whole craft of the introduction, so they are written here rather than left to the drafting:

**§1.1 — how it is.** Agent access to geoprocessing is now organised as a catalogue of named operations: a server publishes nine operations with schemas, an agent chooses among them, and the call is what gets examined. The evaluation has followed the call, because the call is what can be logged and compared. So the literature can say how often an agent chose correctly, and how often its plan was executable, and very little about whether the layer it produced was right. **What the artefact does is what the field has stopped asking.**

**§1.2 — why it is so.** Three reasons, and none of them is carelessness. The type of a parameter does not encode its meaning — metres and degrees are the same float — so a schema can be satisfied by a value that is spatially wrong. Evaluation went where it was cheap: calls are loggable at no cost, while meaning needs an oracle per task, and oracles cost days. And the protocol standardises the envelope rather than the operation, which makes interfaces comparable in form and silent about what the operation enforces. **The result is a literature that can compare envelopes but not consequences.**

**§1.3 — what is missing.** The missing thing is a measurement, not a feature. Nobody has estimated how much of an interface's value is the enforcement it performs: schemas are free in 2026, so the difference between interfaces now lies in what the server checks against the data, and that has not been isolated as a factor anywhere — in GIS or outside it. **Answering it is a design question before it is an empirical one.**

**§1.4 — how it should be, and what to do.** The state the field should be in is one where conditions travel with operations, georeference travels with results, and scoring happens on the artefact. Reaching it needs an instrument: one engine, one loop, three depths of enforcement, one frozen corpus, and an oracle per card with a negative control beside it — which is what the rest of this thesis builds, runs, and accounts for. **The remaining sections state what that instrument may claim.**

---

## Board B — the work

### How it is (2026-11-09)

- **The design is closed.** Three conditions, 80 cards, 960 runs, one harness, one engine.
- **The harness runs.** Sixteen tests, 94 % coverage, a CLI that answers.
- **The gates hold.** 45 structure rules, 82 checker tests, no prose errors.
- **The title is decided.** T2, English as its translation; the College's answer is outstanding.
- **The corpus is not built.** Oracles are the bottleneck — roughly a day per card.
- **Chapter 6 is empty.** Six of seven chapters have draft material.

### Why it is so

- **The order is forced.** Freeze, then corpus and harness, then the sweep: a tolerance changed after the first run is a new study.
- **Oracles cost days and runs cost hours,** so the two blocks run in parallel; sequentially they do not fit in half a year.
- **Nothing in chapter 6 can be written before the sweep,** and everything else can — so the thesis waits on data, not on prose.
- **Administration has lead time.** The dean's office, the College and APD answer in weeks, not days.
- **Repetitions stop paying.** Between-task variance dominates, so more runs buy less resolution than more tasks.

### How it should be (at the defence)

- **A pre-registration dated before the first run,** with every later change marked.
- **Eighty oracles** that accept the reference solution and reject a deliberately wrong artefact.
- **A closed coverage matrix,** no run deleted, every artefact hashed.
- **Every number in chapter 6 traceable** to a chapter 4 table and a script.
- **One title** in APD, on the cover and in the competition entry, and the experimental status granted.
- **A subsection on the cartographic predicates,** without which one competition is unreachable.

### What to do

| Action | When | Gate that closes it |
|---|---|---|
| Ask the dean's office whether the topic needs re-approval, quoting both title changes at once | now | an answer on file, before the title is printed anywhere |
| Freeze the pre-registration: cards schema, predicates, tolerances, prompt, limits, analysis plan | B0, wk 1–2 | **G1** — dated and versioned; no later change unmarked |
| Build 80 cards with oracles and negative controls | B1, wk 3–8 | **G2** — every oracle accepts the reference and rejects a wrong artefact |
| Take the harness to a pilot | B2, wk 7–10 | **G3** — 60 runs, no crash, a complete log, the fake model reproducing its trajectory |
| Run the sweep | B3, wk 11–18 | **G4** — coverage matrix closed, SHA-256 per artefact |
| Analyse from scripts only | B4, wk 13–20 | **G5** — every number in chapter 6 comes from a script |
| Write chapters 1–7 | B5, wk 17–24 | **G6** — a full draft with the supervisor in week 24 |
| Format, abstract, poster, competitions | B6, wk 25–26 | **G7** — the §5 checklist ticked |

---

## What the four columns force, once they are read together

1. **The claim is conditional, not comparative.** Column one records that the prior favours code (`framing/gap-and-literature.md` §4). A metaplan that ended in "the catalogue is better" would contradict its own first column, so column three asks *when and why*, and the falsifiers are in place before the data.
2. **The cartographic family is an answer to column two, not decoration.** Where the operation cannot be expressed as a condition, conditions cannot help — so the corpus needs the case in which the catalogue loses by construction, and that case is the evidence, not a gap.
3. **Column four must survive a null.** If enforcement turns out inert, the instrument, the detection site and the cost accounting are still results. That is why the fourth column ends in outcomes and reproducibility rather than in a hoped-for effect.

**How to use it.** Four paragraphs for §1.1–1.4, as above. The whole board for the conference poster, where four columns are a legible form. And one sentence in a viva, if the argument has to be compressed: *the field measures the call because the call is cheap to measure; this thesis measures the artefact, and asks how much of the difference an interface makes is the correctness it enforces.*
