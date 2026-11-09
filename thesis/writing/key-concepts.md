---
id: writing/key-concepts
title: "Key concepts — operational definitions for §3.1"
type: note
status: live
language: en
question: "What are the operational definitions used in the thesis?"
tasks: [TASK-16]
updated_date: '2026-11-07'
---

# Key concepts — operational definitions for §3.1

> The answer to one question: **what do the terms the thesis uses actually mean** — operation catalogue, envelope, gate, artefact and the rest.
> This document is the **definitional layer** (for §3.1 of the thesis). The translation layer (English → Polish → where it is first used) stays in `concept-dictionary.md`, and the layer of statistical concepts stays in `analysis/statistics.md`.
> Every concept carries four fields: **definition · not to be confused with · how it is observed · example**. That is the examiner's requirement: a term without an operationalisation is decoration.

---

## A. The interface

| Concept | Definition | Not to be confused with | How it is observed | Example |
|---|---|---|---|---|
| **operation catalogue** (tool surface) | the **countable set of named operations** offered to the agent with signatures and descriptions — what the agent can do *at all* | "protocol": the protocol is the means of transfer, the catalogue is the content; "number of tools": the catalogue has structure (primitive, composite, meta) | the number of entries in the response to a tool listing; the operation table in §4.2 | nine primitive operations: describe layer, buffer, clip, intersect, union, spatial join, zonal statistics, reproject, export |
| **envelope** | the **message format**: method names, argument encoding, result shape, error channel. Standardised by the protocol | "catalogue": the envelope says nothing about *which* operations exist; "semantics": the envelope is semantically empty | comparing two messages that describe the same action in both arms (`design/runs.md`) | a call as a message `tool call {name, arguments}` versus a code string handed to the executor |
| **enforcement layer** | **all the places where conditions are checked** — in parameters, before execution, after execution, on the artefact | "schema validation": the schema is only the shallowest of those places | the number and kind of gates active in a given condition (N1 vs N4) | condition N4: argument validation + invariants + terminal conditions + a check that the file was written |
| **gate** | a **single check attached to an operation**, executed at a defined point and returning an explicit outcome (pass / error with content) | "test": a gate runs on every run, a test on request; "project gate (G1–G7)": those are decision points in the research plan, not checks in code — **a name collision to be removed in §3.1** | the number of errors ending in `isError` inside the loop; the share of `detected_by = server` | a required `unit` parameter (parameter gate); a check that "the CRS was written to the file" (artefact gate) |
| **task contract** | the **explicit, machine-readable statement of requirements**: target CRS, unit, mask, output path, required fields | "instruction": the instruction is text for the model, the contract is a checkable structure | the presence and completeness of the contract fields in the task card | `{target_crs: EPSG:2180, unit: km, mask: gminy, out: wynik/bufor_gminy.gpkg}` |
| **handle** | a **reference to an intermediate result together with its metadata** (CRS, transformation, missing data, type) | "file path": a handle needs no file on disk; "array": a handle carries metadata, an array does not | the presence of metadata fields in the structured result of every operation | `{handle: r1, crs: EPSG:2180, transform: [...], nodata: -9999, shape: [1200, 1500]}` |

---

## B. Correctness

| Concept | Definition | Not to be confused with | How it is observed | Example |
|---|---|---|---|---|
| **artefact** | the **output object of a task** on which the oracle rules: a result file or a handle. Not "whatever happened to be produced", but what the task names as its result | "intermediate result": the artefact is named in the contract; "the model's answer": an answer is not an artefact | artefact hash + the predicate set | `wynik/bufor_gminy.gpkg` |
| **silent error** | an **error that does not end in an exception**: the result is a valid value of the right type and shape, and wrong in meaning | "omission error": a silent error *was performed*, not skipped | an oracle failure at zero exceptions in the run | a 5 m buffer instead of 5 km: execution without error, four of six predicates satisfied |
| **invariant** | a **property of the result checkable from the data alone**, without knowing the task's intent | "task requirement": "5 km" is intent (P-III); "the CRS was written" is an invariant (P-II) | the list of invariants in the gate table of §3.5 | valid geometry; result extent inside the mask; area consistent with the number of objects |
| **tool-knowledge levels** P-I / P-II / P-III | **how much the tool can know**: P-I syntax and types · P-II domain invariants · P-III the task's intent | "enforcement depth": N is the configuration of a condition, P is the kind of knowledge — **two different dimensions** | the error classes detectable at each level (the table in §3.1) | P-I: `unit` belongs to the set; P-II: the CRS in the file matches the declaration; P-III: the distance is 5 km |
| **expressible share** | **the part of a task's requirements that the surface accepts as a parameter and can check**, divided by all requirements | "gate coverage": coverage says how many gates exist, the expressible share says how many of *this task's* requirements they cover | coding seven requirement types on the card (W1–W7), reported as a fraction | A-01: 6/6 = 1.00; an atlas card: ≈ 0.50 |

---

## C. Measurement

| Concept | Definition | Not to be confused with | How it is observed | Example |
|---|---|---|---|---|
| **run** | **one execution of one task in one condition and one repetition**, from the first instruction to the closing of the artefact (or exhaustion of the budget). A self-contained, accountable unit: it has a `run_id`, its own log and its own oracle verdict | "task": the task is the **unit of analysis** (one, repeated), the run the **unit of execution**; "repetition": a repetition is the index of a run within a task and condition; "repair": repair happens **inside** a run and does not create a new one | a log row + a run directory named by `run_id` holding the artefact, the event log and the oracle verdict | `K/A-01/r3` — task A-01, condition K (code), repetition 3, finished after 11 turns |
| **task card** | the **unit of the corpus**: instruction, inputs, expected artefact, predicates with tolerances, provenance, trap | "instruction": the instruction is one field of the card | a YAML file in the appendix | card A-01 (`draft/thesis-draft-v0.md`, appendix A) |
| **condition** (arm) | the **configuration of factors** in which all tasks are solved | "level": conditions N1 and N4 share one surface and differ in their level of enforcement | the column name in the log | K (code) · N1 (catalogue, schema) · N4 (catalogue, invariants + terminal conditions) |
| **oracle** | the **set of predicates that decide on the artefact's correctness**, written down before measurement | "model judge": the oracle is deterministic; "unit test": the predicates carry domain tolerances | the outcome of every predicate in the log | four CRS predicates + geometry validity + extent coverage + area |
| **predicate** | **one check of the artefact with an explicit tolerance** | "gate": a gate acts inside the loop, a predicate after the fact | the value and threshold in the oracle table | `extent_iou ≥ 0.95`; `area 3912.4 km² ± 0.5 %` |
| **harness** | the **instrumentation**: loop, executor, budget, log, oracle invocation | "agent": the harness makes no substantive decisions | the code, the version and the parity test results in the appendix | loop + protocol client + container + JSONL log |
| **TSR** | the **share of correct artefacts** among the runs of a given condition | "share of successful calls" — a different measure, and usually a higher one | the "correct" row over all rows in the results table | 0.62 vs 0.36 |
| **PCI** | the **share of errors caught inside the loop** (by the server or by the language) among all errors | TSR: PCI does not say how many artefacts are correct, only where an error was noticed | the distribution of `detected_by` | 0.71 against 0.24 |
| **`detected_by`** | the **log field recording where an error was caught** — language · own invariant · tool execution error · oracle | "cause of the error": where it was caught is not its class (one class can be caught in several places) | a column in the log, cross-tabulated with the class | a unit error caught by the server, or only by the oracle |

---

## C.1 The anatomy of a run

Because "960 runs" is the number the whole time budget rests on, a run has to be defined **at its boundaries**, not only descriptively.

**When it starts:** at the moment the task instruction is handed to the model with an empty task context. Waiting for resources does not count — only turns.

**When it ends** — one of four reasons, recorded in `stop_reason`:

| `stop_reason` | Meaning | Does it count towards TSR |
|---|---|---|
| `artifact` | the agent declared completion and named the artefact | yes |
| `budget` | the turn limit (25) or the token budget was exhausted | yes (the artefact is scored if one exists) |
| `error` | the harness stopped the run (executor failure, no response) | **no** — the run is repeated and the incident logged |
| `refused` | the agent refused to perform the task | yes, as a failure |

**What one run's log contains** (13 fields — this is also the specification of the result file):

`run_id` · `task_id` · `condition` · `repetition` · `seed` · `stop_reason` · `turns` · `tokens_in/out` · `tool_calls` · `detected_by` · `error_class` · `tsr_pass` · `artifact_hash`

**Three things that must not be confused:**

| Concept | What it is | Effect on the number of runs |
|---|---|---|
| **repetition** | an independent execution of the same task in the same condition with a different seed — **it estimates variability** | multiplies: 80 × 3 × 4 = 960 |
| **repair iteration** | a further attempt **inside** a run, after an error message from a gate or from the language | does **not** multiply — it is an event in the run's log |
| **retry** | a run voided for technical reasons (`stop_reason = error`) and executed again from scratch | does not increase the analysis N; the incident goes into the quality report |

**Consequence for power:** four repetitions give an MDE of 14.0 pp at 80 tasks; eight give 10.3 pp; sixteen give 7.7 pp. Increasing repetitions **below** the threshold of 4 makes no sense, because between-task variability (ICC 0.661) dominates the within-task one — repetitions buy precision only until task variance stops being the binding factor.

**Recording rule:** a run without an artefact and without a `stop_reason` in the log is **void**, not "zero". Zero-filling gaps deflates TSR and is the most common error in reporting series of this kind.

## D. Inference

| Concept | Definition | Not to be confused with | How it is observed | Example |
|---|---|---|---|---|
| **MDE** | the **smallest detectable difference** at a given number of tasks, repetitions and between-task variability | "effect size": the MDE is the resolution limit of the measurement, not a result | stated beside every "no difference" | 14.0 pp at 80 tasks and 4 repetitions |
| **equivalence assumptions** A1–A5 | the **conditions under which the comparison makes sense**: oracle validity, capability parity, information parity, budget parity, absence of drift | "limitations": these are not caveats but validity conditions — violating one changes the interpretation | the parity test table in the appendix | the same script → the same artefact hash in both arms |
| **parity table** | the **mapping of every catalogue operation onto a library function and version** in the code arm | "tool list": parity concerns capability, not count | appendix + parity test | `buffer` ↔ `processing.run("native:buffer")`, QGIS 3.x |
| **information closure** | the **rule `guard_information ⊆ agent_information`**: a gate may not compare the result with something the agent does not know | "hiding the oracle": hidden expectations are admissible only on the harness side | an audit of the contract fields against the instruction text | a contract taken from the instruction may go into a signature; an expectation from the oracle file may not |
| **pre-registration** | the **record of hypotheses, measures, decision rules and the MDE before the series of runs** | "work plan": pre-registration binds the analytical decisions | the dated pre-registration file in the appendix | rule R2: if the catchable mass is below 25 %, the claim moves to the structure of failure |

---

## E. Terms to separate before §3.1 is written

Three name collisions that occur in the present notes and **cannot** enter the thesis unresolved:

| Collision | Resolution |
|---|---|
| **gate** — a check in code *vs* "gate G1–G7" from the research plan | in the thesis: a **gate** is a check in the interface; the plan's stages are called **decision points** |
| **level** — enforcement depth (N1/N4) *vs* tool-knowledge level (P-I/P-II/P-III) *vs* task difficulty (T1–T4) | three different words: **enforcement depth** · **knowledge level** · **task difficulty** |
| **condition** — experimental arm *vs* correctness condition (invariant) | **condition** = arm; **correctness condition** = an invariant or a requirement |
| **run** — execution *vs* repetition *vs* repair *vs* retry | **run** = one execution; a **repetition** multiplies N; a **repair** is an event inside a run; a **retry** is a run voided for technical reasons |

---

## F. In one sentence

**The operation catalogue is the content, the envelope is the form, the enforcement layer is the place where form meets meaning; a gate is a single check at that place, the artefact the object of evaluation, the handle the carrier of metadata along the chain of operations, and the oracle the set of predicates that rule after the fact — and each of these concepts has not only a definition in the thesis but also a stated "not to be confused with" and a way of being observed, because a term without an operationalisation is decoration, not method.**
