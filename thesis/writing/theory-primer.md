---
id: writing/theory-primer
title: "Theory primer: the terms the thesis runs on, explained from zero"
type: note
status: live
language: en
question: "What do LLM, agent, harness, geoprocessing, exposure, spatial correctness, agent evaluation and MDE actually mean here?"
tasks: [TASK-16]
updated_date: '2026-11-09'
---

# Theory primer: the terms the thesis runs on, explained from zero

> Three dictionaries exist for three different jobs, and this is the third of them. `concept-dictionary.md` is the **translation layer** (English → Polish → where the term is first used). `writing/key-concepts.md` is the **definitional layer** for §3.1, four fields per concept. This document is the **teaching layer** — the same vocabulary explained from nothing, in the order it has to be understood, each term answering *what it is*, *what it is not*, and *why this thesis cares*.
>
> Read it once, top to bottom. The order is a dependency chain, not alphabet: a model alone is not an agent; an agent without a harness is not a measurement; a harness without an oracle produces opinions. Every definition below is the one the thesis uses, which is sometimes narrower than the popular one — where it differs, the disagreement is named.

**Five documents, five jobs — none of them repeats another.**

| Document | Job | Read it when |
|---|---|---|
| this one | teaching layer: from zero, in dependency order | first, once |
| `key-concepts.md` | operational definitions for §3.1: definition, not to be confused with, how observed, example | writing chapter 3 |
| `concept-dictionary.md` | translation layer: English → Polish → first place of use | writing in Polish, or checking a term |
| `defence.md` | rehearsal layer: the committee's questions with 20-second answers, deeper layers and traps | the week before the defence |
| `docs/prose.md` | label layer: which letter means what | meeting `C4` or `F2` in a table |

Where a section below has a rehearsal twin, the pointer is given — they answer different questions ("what is it" against "how do I say it under pressure") and neither is a substitute for the other.

---

## 0. The chain, in one picture

```text
   datum / CRS ──▶ operation ──▶ engine (QGIS 3.44) ──▶ exposure method ──▶ agent (LLM + loop)
                                                                                    │
                    measure ◀── oracle ◀── artefact ◀── evaluation harness ◀────────┘
```

Read left to right it is the object of study: spatial data, operations on it, and the many ways of letting a language model reach them. Read right to left it is the measurement: what came out, was it right, and how do we know that the checking itself works. **The thesis lives on the two arrows in the middle** — the interface between engine and agent (exposure), and the interface between run and score (evaluation). Everything else is either substrate or instrument.

---

## 1. LLM — large language model

**What it is.** A function from text to text, trained to predict the next token. It takes a *context window* — a finite block of text, including the conversation so far and any system prompt — and returns a continuation. Around 10¹¹ parameters, fixed after training, no memory between calls unless something outside it stores the transcript.

**What it is not.** Not a database of facts (it interpolates), not deterministic (sampling and serving variance make the same prompt produce different continuations), not an agent, and not aware of anything beyond the context it is handed. It cannot run code, read a file or query a server; it can only *emit text that asks* for those things.

**Why this thesis cares.** Two consequences drive the whole design. First, because the model is a sampler, *one run tells you nothing about reliability* — hence repetitions. Second, because the model is the only component you cannot freeze, the experiment freezes everything around it: one model pinned by name, version and date, one prompt, one budget, and the same limits in every condition (`design/runs.md`).

**For the defence version of this section**, `defence.md` §4.1. **The word "model" versus the word "agent".** The title says *agents LLM*, and this is the distinction it leans on: the model is the function, the agent is the system that gives it tools, a loop, and a sandbox. The thesis studies the second; the first is a component it holds constant.

---

## 2. Agent — a model in a loop, with hands

**What it is.** Model + a loop + tools + a sandbox. One iteration is: the model emits an action (a tool call, or a block of code), the action is executed, the result returns into the context as an observation, and the model decides again — continue, repair, or stop. Repeat until the task is done, the turn limit is reached, or the clock runs out.

**What it is not.** Not a "framework" (in this thesis the loop is the *instrument*, named once and frozen — `design/harness.md`), not "autonomous AI" (the operational version is duller: *the agent completes the task without a human intervening mid-run*), and not a single model call. A ten-turn agent is ten model calls whose inputs depend on the outputs of the previous ones, which is why an early semantic error compounds instead of being averaged away.

**Why this thesis cares.** The loop is where an interface becomes measurable. A gate can only intercept an error if the error happens *inside* a loop that carries on afterwards — the model must be able to see the rejection and try again. And the loop is what makes repetition cheap to interpret: same task, same prompt, same tools, four times, and you learn something about variance that no single success can show.

---

## 3. Agent harness, and the evaluation harness

**What it is.** Two objects that are routinely confused, and the confusion is expensive.

| | **Agent harness** | **Evaluation harness** |
|---|---|---|
| What it is | the loop, the system prompt, the tools and the sandbox — **the thing under study** | the instrument that runs the tasks, resets the environment, records runs, calls the oracle and aggregates |
| Varies between conditions? | **no** — one, frozen (`d-4`) | **no** — identical in every condition, or the contrast is worthless |
| Polish | *stanowisko agenta* | *stanowisko pomiarowe* |

Both are "the harness" in ordinary speech, which is why the glossary splits them (`glossary-of-terms.md`). When the thesis says "the harness did X", it means the instrument; when it says "the harness was held constant", it means the studied object.

**What it is not.** Not a benchmark, not an application, not a product. The evaluation harness is the closest thing in the thesis to a laboratory instrument: it is described in a chapter so that someone else could rebuild it, and its own tests matter because a broken instrument produces confident nonsense.

**For the defence version**, `defence.md` §4.5 (sandbox, reproducibility, pins). **Why this thesis cares.** Every design decision that looks pedantic — pinned container digest, hashed task cards, `--resume`, never deleting a run — exists to make one sentence true: *the only thing that differed between the conditions was the interface*.

---

## 4. GIS geoprocessing — operations on spatial data

**What it is.** The class of operations that transform spatial data: reproject, clip, buffer, intersect, union, spatial join, zonal statistics, describe a layer, export. Each takes layers and parameters and returns new data. In this thesis they run on **QGIS 3.44 LTR**, through `processing.run` (PyQGIS) or `qgis_process` — the same engine either way, which is what makes the comparison controlled.

**What is special about spatial data.** Three things, and the thesis exists because of the third:

1. **Coordinates are meaningless without a CRS.** A coordinate reference system says which datum and which projection the numbers are in. The same pair `(1234.5, 567.8)` is a valid position in EPSG:2180 and a different valid position in EPSG:4326.
2. **The type does not carry the meaning.** A distance is a float. Five metres and five degrees are the same `5.0`. Nothing in a JSON schema can tell them apart, because both are numbers of the right type.
3. **A wrong result usually looks fine.** A layer reprojected into the wrong system still renders, still has geometry, still opens in QGIS. This is the **silent error**: a value of the right type, shape and plausibility, wrong in meaning.

**What it is not.** Not "GIS" as a subject — the thesis does not evaluate a GIS, it uses one as substrate — and not cartography, except for one family of tasks where the output is a map and its correctness is a property of the rendering.

**For the defence version**, `defence.md` §3.1–3.2 (CRS, IoU, validity) and §2.4 (silent against loud). **Why this thesis cares.** Silence is the phenomenon. If spatial errors were loud, every interface would look equal and the question would be boring. Because they are silent, the question becomes: *which interface can catch what, before the wrong layer reaches a user?*

---

## 5. Exposure methods — how a model is given the engine

**What it is.** The answer to one question: *what exactly does the model see of the engine, and in what form?* Two axes, and the thesis manipulates one per contrast.

**Axis 1 — the channel.**

| Channel | What the model emits | What the engine receives | Control arm |
|---|---|---|---|
| **Code** | text: a Python program using PyQGIS | a program, executed in the sandbox | **K** |
| **Catalogue** | a structured call: operation name plus arguments | a request routed to one operation | **N1**, **N4** |
| *(hybrid)* | both, alternating | both | **excluded** — it has no identifiable interface, and is named as further work |

**Axis 2 — the enforcement depth** inside the structured channel: how much the surface checks. The ladder is cumulative, and only two rungs are ever run as conditions:

| Rung | What the surface checks | What it can catch |
|---|---|---|
| L0 | nothing | — |
| **L1 / N1** | JSON Schema: types, enums, required fields | wrong names and types — which in 2026 the decoder already guarantees, so this rung buys ≈ 0 |
| L2 | domain constraints: the EPSG code exists, distance > 0, compatible geometry type | implausible values |
| L3 | preconditions: the input has a CRS, the layer is not empty, the field exists | errors that would otherwise fail late |
| **L4 / N4** | postconditions: output CRS as requested, units verified, extent not degenerate, count as expected — the server returns an **error instead of success** | the silent, spatially false artefact |
| (L5) | the artefact contract: the file exists, schema matches, the write is atomic | missing or half-written outputs |

Two things the ladder cannot do, and both are claims the thesis makes rather than hides. It cannot know **intent**: nothing inside the surface can tell that the task wanted a clip and the agent performed an intersection — that error belongs to the oracle. And depth costs the server author effort, which is why the interesting result is not "deeper is better" but *where on the curve the return starts*.

**What it is not.** *Exposure* is not *protocol*. The protocol (MCP) standardises the **envelope** — method names, argument encoding, result shape, error channel — and says nothing about which operations exist or what they check. That is why the thesis's finding is about enforcement, not about MCP: in 2026 every serious client can do the envelope, so the envelope distinguishes nothing.

**For the defence version**, `defence.md` §4.2–4.4 (protocol against API against library; what MCP provides; tool calling against code generation). **Why this thesis cares.** This is the manipulated variable. K against N1 asks whether the *channel* matters; N1 against N4 asks whether *enforcement* is what makes the structured channel worth having. Both contrasts run on one engine, one corpus, one loop.

---

## 6. Spatial correctness — what "right" means for an artefact

**What it is.** A property of the **artefact** — the file or handle the task names as its result — checked against a frozen set of **predicates**: target CRS, unit, extent overlapping the mask (IoU above a set tolerance), geometry validity, feature count, attribute values, and for map tasks the declared renderer, class count, classification field, and label field. Each predicate is a yes/no, each tolerance is a number fixed before the first run, and **all** predicates must pass for the run to count as a success.

**The seven gates** are the places where an error can die before it becomes an artefact: choice of operation, parameter names and types, parameter values, ordering and preconditions, execution, state of the output, file contract. Only some of them are reachable from inside an interface — which is precisely the space the ladder in §5 fills.

**The three knowledge levels** say how much a check could possibly know: **P-I** syntax and types, **P-II** domain invariants checkable from the data alone, **P-III** the task's intent as stated. A surface can reach P-I and P-II; P-III only insofar as the task card states the requirement in machine-checkable form. This is the honest ceiling on every claim in the thesis.

**What it is not.** Not "the code ran without an exception" (that is the loud failure, and counting only those inflates any score), not "the map looks right" (a rendered map can be plausible and wrong), and not the same as validity — a file can be formally valid and spatially false. Nor is it *accuracy*: the measure is task success rate (TSR), the share of runs where every predicate holds; partial credit (PCS) records how close a failure came, and call validity (CVS) separates "wrong answer" from "illegal move".

**For the defence version**, `defence.md` §2.1–2.4 and §1.3 (what a particular test tests). **Why this thesis cares.** It is the outcome variable, and it is where measurement validity is thinnest — hence the two defences: an **oracle** hidden and frozen before the sweep, and a **negative control** per card, a deliberately wrong artefact the oracle must reject. An oracle that never fails has not been shown to measure anything.

---

## 7. Agent evaluation — how anyone knows an agent worked

**What it is.** A choice of *what* to score and *how often*, and the two choices are independent.

**What to score.** Three options, in increasing strictness: the **call** (was the request well-formed and legal — CVS), the **plan** (was the sequence of operations sensible), the **artefact** (is the output correct — TSR over predicates). Text-matching and code-similarity scoring sit below all three: they compare the answer with a reference instead of checking the world. This thesis scores the artefact, because the artefact is the only object whose correctness matters to a user of a GIS.

**How often.** One attempt per task gives a **pass rate**: the fraction of tasks solved once. Repeating the same task gives **reliability**: how often the same task is solved, which is a different quantity, and the one that matches how these systems are actually used. A system that solves 60 % of tasks and solves each of them reliably is a different product from one that solves 60 % and is a coin flip on every task. The design here uses r = 4 repetitions on every task and reports per-task consistency, not just the mean (`analysis/statistics.md`).

**What it is not.** Not a leaderboard: this thesis publishes no ranking of models and no claim about "the best agent". Not pass@k (that is a coverage measure over k attempts: whether *at least one* works — useful for search, misleading for an assistant). And not a cost-free number: **cost per successful task** — tokens and turns divided by successes, not per call — is reported beside every correctness figure, because an interface that is more correct and three times more expensive has not obviously won.

**For the defence version**, `defence.md` §1.5–1.7 (pairing, effect size, multiple comparisons). **Why this thesis cares.** Because most of the field scores the cheap thing. Calls are loggable; meaning needs an oracle. The contribution is an instrument that scores the expensive thing properly — with tolerance tables, negative controls, blind double coding of failure classes, and a pre-registration that fixes the analysis before the data arrive.

---

## 8. MDE — the smallest difference the design can see

**What it is.** The **minimum detectable effect**: the smallest true difference a study can expect to detect at a given significance level (α = 0.05) and power (0.80). It is a property of the *design*, computed before any data exist, from three quantities: how many independent units you have (**80 tasks**), how many repetitions each gets (**r = 4**), and how much the tasks differ from each other.

**Why it is not "the effect size".** An effect size is what happened. The MDE is what *could* have been seen. If the true difference is 8 pp and the MDE is 14.0 pp, a flat result does not mean "no effect" — it means **undecided**, and the thesis has a word for exactly that verdict (§9). The two are often confused in drafts, and the confusion converts a limitation into a false finding.

**Why repetitions stop paying.** Because tasks differ from each other much more than runs of the same task do: the between-task share of variance here is **ICC 0.661**. Adding repetitions reduces the noise inside a task, which is already small; adding tasks reduces the noise *between* tasks, which is large. That is why the design is 80 × 4 = **960 runs** with an MDE of **14.0 pp**, and not 40 × 16, which would buy the same runs for less external validity.

**The supporting cast, in six lines.** **α** is the tolerated false-positive rate. **Power** is the chance of finding a real effect of the stated size. **ICC** is the share of variance explained by grouping (here, by task). **Holm** corrects the two secondary hypotheses for multiplicity, applied in a fixed order after the single confirmatory test. **κ** checks whether two blind coders assign the same failure class. **Intent-to-treat against per-protocol** decides whether crashed and abandoned runs count — here they do, because deleting them is how a sweep flatters itself.

**For the defence version**, `defence.md` §1.4. **Why this thesis cares.** The MDE is the sentence that makes the whole thing falsifiable: *an effect under 14.0 pp is not claimed.* It is also what turns a likely null into a result rather than a failure — the field's prior favours code (`framing/gap-and-literature.md` §4), so a small or absent effect is the expected shape, and a study that pre-commits to its resolution is the only kind that can report it honestly.

---

## 9. The vocabulary, in one table

| Term | Polish | Meaning in one line |
|---|---|---|
| LLM | model językowy | text-to-text function; sampled, not deterministic |
| agent | agent | model + loop + tools + sandbox |
| token, context window | token, okno kontekstu | the unit of text, and how much fits in one call |
| tool call | wywołanie narzędzia | one structured request to execute one named operation |
| MCP | MCP | protocol that standardises the *envelope* of tool calls |
| tool surface, catalogue | powierzchnia narzędzi, katalog | the set of operations offered, with descriptions and schemas |
| schema | schemat | machine description of an operation's parameters |
| envelope | koperta | message format: methods, encoding, result shape, error channel |
| exposure method | sposób udostępniania | how the model is given the engine: channel plus enforcement depth |
| enforcement layer | warstwa egzekwowania | every place where a condition is checked |
| gate (B1–B7) | bramka poprawności | a check at a defined point of the path from call to artefact |
| geoprocessing | geoprzetwarzanie | operations on spatial data: buffer, clip, join, reproject |
| CRS, EPSG | CRS, EPSG | the definition of coordinates and units; a silent-error factory |
| artefact | artefakt | the output object the task names as its result |
| oracle | wyrocznia | the program that scores an artefact against predicates |
| predicate, tolerance | predykat, tolerancja | one checkable condition, and the number that decides it |
| negative control | kontrola negatywna | a deliberately wrong artefact the oracle must reject |
| silent error | błąd cichy | right type and shape, wrong meaning, no exception |
| TSR, PCS, CVS | TSR, PCS, CVS | success rate, partial credit, call validity |
| cost per success | koszt zadania zakończonego sukcesem | tokens and turns divided by successes |
| run, turn, repetition, cell | przebieg, tura, powtórzenie, komórka | one attempt, one loop iteration, one repeat, one task × condition × repeat |
| agent harness | stanowisko agenta | the loop, prompt, tools and sandbox — the object of study |
| evaluation harness | stanowisko pomiarowe | the instrument that runs, records and scores |
| pre-registration, freeze | przedrejestracja, zamrożenie | the plan fixed in writing before the first run |
| MDE | minimalna wykrywalna różnica | the smallest difference the design can see |
| undecided | nierozstrzygnięte | a difference below the MDE: not "no difference" |
| expressible share | udział wyrażalny | the part of a task's requirements the surface can accept and check |
| P-I / P-II / P-III | poziomy wiedzy narzędzia | syntax · domain invariants · task intent |

---

## 10. Six sentences that would survive a viva

1. A language model is a sampler, so reliability has to be measured, not assumed — hence repetitions, not a single pass rate.
2. Spatial errors are mostly silent, because a float carries no units and a file carries no meaning; that is the phenomenon.
3. An interface differs from another in two ways: the channel the model speaks through, and how much it enforces — the thesis manipulates both, one contrast each.
4. Schema validation is free in 2026 and distinguishes nothing; what remains to be tested is what a server checks against the data.
5. Correctness is a property of the artefact, scored by frozen predicates with a negative control, because an oracle that cannot fail proves nothing.
6. The design resolves 14.0 pp; anything smaller is undecided, and a null with a mechanism is a better result than a comparison with a story.
