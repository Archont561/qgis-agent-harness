---
id: draft/thesis-draft-v0
title: "Evaluation of the MCP protocol as a way of exposing geoprocessing operations to LLM agents, compared with code generation on an identical QGIS runtime"
type: draft
status: live
language: en
tasks: [TASK-4, TASK-11, TASK-13]
updated_date: '2026-11-09'
---

# Evaluation of the MCP protocol as a way of exposing geoprocessing operations to LLM agents, compared with code generation on an identical QGIS runtime

## Working draft v0 — continuous text

> Minimal version, for the supervisor to read and correct. It does not contain results yet — chapter 6 gives **expected results together with interpretations written down in advance**. Terminology per `glossary-of-terms.md`; the numbers (power, run counts) were computed by script, not from memory.

---

# 1. Introduction

## 1.1. The problem

A language-model agent that has to perform a geoprocessing task — cut two layers, run a buffer, compute an area in metric units — needs two things: **access to operations** and **knowledge of when the result is correct**. The first is always given. The second is the subject of this thesis.

Access can be organised in at least two ways. In the first, the model is given a **catalogue of named tools** together with their signatures; a call is a message in an agreed format, and the result comes back as data with a known structure. In the second, the model **writes code**, which is then executed in a geoprocessing environment; the result comes back as the interpreter's output text.

The difference this thesis examines is not that one approach "can do more". In both cases the same algorithm of the same library is executed. The difference is **where correctness conditions can be placed and how often they are checked**. In the catalogue approach a condition can be written into the tool signature and into its terminal conditions — once, in one versioned implementation, active in every run. In the code approach the same condition has to be formulated by the model, anew in every run, and only when it judges that necessary.

## 1.2. Why geoinformation

In most fields an execution error ends with an exception: an undefined name, a mismatched type, a range violation. In geoinformation **a wrong result is a value of the right type and shape** — a valid array, valid geometry, a valid number; the contradiction lies not in the value but between the value and its meaning. A buffer with a radius of five metres instead of five kilometres is a valid operation; it produces a geometrically valid layer with a correctly declared coordinate reference system (CRS) and incorrect content — and if the result stays in memory and is never written, even that declaration disappears, because an array carries neither the system, nor the transformation, nor information about missing data. The same holds for units, missing data represented as zero, overlapping polygons counting an area twice, and a result clipped to an incomplete extent.

This property moves the criterion for evaluating an integration from "did the agent answer correctly" to **"is there anywhere for its mistake to be noticed"**. The thesis measures the latter, not only the former.

## 1.3. Aim of the thesis

The aim is **to establish whether, and to what extent** the way geoprocessing tools are exposed — a catalogue of named operations served over the MCP protocol versus generating PyQGIS code — affects the correctness of the resulting artefact, **and to identify the mechanism** of that effect: the role of correctness conditions enforced in the interface rather than in the model's reasoning.

The aim decomposes into five specific aims: **measurement** (estimate the difference in the share of correct artefacts, with a confidence interval and the smallest detectable difference), **mechanism** (establish the dependence of correctness on enforcement depth and on the task's expressible share), **diagnosis** (establish where errors are detected: by the language, by the model's own invariant, by the server in the loop, or only by the oracle), **instrument** (build and publish the instrument) and **practice** (formulate a rule for designing tool surfaces). The aim is decidable and is achieved **even with a zero or negative result** — the criterion is the readability of the partial results, not the sign of the difference.

The thesis does not aim at a verdict about the protocol in general, a comparison of protocols, an evaluation of models, an assessment of cartographic quality, or a ruling on transferability to other domains.

## 1.4. Thesis statement

> The way geoprocessing tools are exposed determines **where and how often** an error is caught, and consequently how often a correct artefact is produced. A tool interface allows correctness conditions to be written once and enforced in every run; code generation leaves their formulation to the model. **That is the position the thesis defends and the design tests:** it estimates whether the difference carries over into the correctness of GIS task execution, **through what** it works, and **where it stops working** — and it reports a difference below 14.0 pp as undecided rather than as absent.

## 1.5. Scope and boundaries

The thesis compares **two separate** ways of integrating: a tool catalogue served over the MCP protocol and code generation in PyQGIS, in an **identical environment** (the same interpreter, the same library versions, the same data). A variant combining both approaches — reconnaissance through the catalogue first, then generated code — is **not the subject of the study** and is named in chapter 7 as a direction for further work.

**Spatial scope:** tasks operate on reference data for the area of Poland, in **EPSG:2180** (PL-1992), with the unit of aggregation being the **gmina** (a unit of administrative division, the GUGiK reference layer); tasks involving a different target system require an explicit reprojection and are marked as such in the corpus. **Temporal scope:** input data come from one frozen snapshot (the state on the day preceding the run series), and the execution series takes five weeks; **the thesis does not study change over time** — it has no temporal variant and no comparison of epochs, because temporal variability would be a second factor and would weaken the contrast. **Subject scope:** exclusively the design dimension of the interface (what the agent may call and what is checked), not performance, not infrastructure cost, not the aesthetic quality of cartography.

The thesis does not compare protocols (MCP with REST or OGC API Processes), does not assess cartographic quality in the aesthetic sense, and does not rule on domains on the basis of ten tasks per domain. The assessment concerns the **design dimension** of the interface, not the protocol brand.

## 1.6. Contributions

1. **A vocabulary of failure**: a taxonomy of seven correctness gates and eight classes of coordinate-system errors, together with the place where each class can be detected.
2. **An instrument**: artefact assessment by spatial predicates, an in-loop catch rate, and a measure of the **expressible share** — the part of a task's requirements that the surface takes as a parameter and can check.
3. **A causal result**: the correctness curve as a function of enforcement depth (schema → invariants → terminal conditions).
4. **A descriptive measure for code generation**: the frequency and content of the checks the model writes by itself.
5. **Reproducible material**: eighty task cards with predicates, the oracle, the harness and a reproducibility package.

---

# 2. Literature review and the research gap

## 2.1. Four currents that never meet

**Action format.** Work on the agent–environment interface shows that the way an action is expressed changes effectiveness. The most cited result — CodeAct (Wang et al., 2024) — reports an advantage for actions expressed as code over function calls: 74.4 % versus 52.4 % on general tasks, with the advantage holding for 12 of 17 models tested. That result lies outside geoinformation and concerns tasks whose correctness is checkable by execution.

**The MCP protocol.** A standard created in 2024 for integrating language applications with external data sources and tools. In its current revision (2026-07-28) it is stateless: the protocol version and capabilities travel in the metadata of every request. The protocol normalises the **envelope** of a message — the format, method names, result shape and error channel — not the meaning of an operation. Input validation errors are to be returned as tool execution errors, so that the model can read them and repair; the protocol does not, however, define units, coordinate systems or the notion of a correct result.

**MCP versus code execution.** Comparative work exists and is not unanimous: reports of an advantage for an intermediate layer, of overhead costs, and of worse results when tool selection fails. Most of it measures **tool choice and call accuracy**, not the artefact.

**Geoinformation.** A separate literature concerns geoprocessing code generation and tool agents. The available benchmarks assess parameter accuracy, trajectory correctness or artefact agreement — but with a **fixed surface** and without a comparison arm.

## 2.2. Self-correction and feedback

The literature on model self-correction is decisive for this thesis. Huang et al. (2024) show that **internal** revision of one's own result without an external signal does not improve it but worsens it: on GSM8K, accuracy falls from 95.5 % to 89.0 % after two rounds, and among changed answers more go from correct to wrong (8.8 %) than the reverse (7.0 %). Kamoi et al. (2024) locate the cause: the bottleneck is **producing feedback**, not the correcting itself; self-correction works where a reliable external signal is available. Tyen et al. (2024) add that a model repairs an error when its location is pointed out, but does not find that location itself.

The conclusion for this thesis is twofold. First, the code-generation arm has feedback **defined by the programming language only** — an exception, a type, an undefined name. Domain information has to be produced by the model. Second, a fair comparison requires an **identical system prompt in both arms**: without it, what gets compared is instructions, not interfaces.

## 2.3. Silent error outside geoinformation

The phenomenon measured here is not a property of geoinformation. In chemistry, MolViBench (arXiv:2605.02351) describes a result that is *executable but chemically wrong*: the code runs without error while the model silently confuses stereochemistry, applies the wrong reaction template, or returns a molecule violating constraints. Work on the validity of molecular representations separates **syntactic** from **semantic** correctness — a representation can be parsable and violate valence — which corresponds to the P-I and P-II levels adopted here. Ready-made design patterns also exist: compiling ontology constraints into executable MCP tools (arXiv:2602.03439) gives the model feedback during operation. **This thesis therefore does not propose the idea of gates itself, but measures causally how much that idea yields relative to code generation.**

In medicine the stakes are highest, and the goal differs. Systems combining rules with pharmacological knowledge flag the majority of near-miss events (MEDIC, Nature Medicine 2024: 95.1 %), but the clinical decision support literature has struggled for decades with **alert fatigue** — a surplus of alerts leads to their being ignored. Hence in medicine a gate cannot be a filter alone; it must be able to **ask or escalate**, and the objective function is not the share of correct artefacts but the reduction of harm.

Geoinformation is chosen as the first proving ground because it combines three conditions needed for a causal measurement: the invariants are cheap and deterministic, the meaning is codified in a machine-readable registry (EPSG, `proj.db`), and the error is painful but not life-threatening — so the experiment can run on synthetic data.

## 2.4. The gap

| # | What is missing |
|---|---|
| L1 | Work in which **the interface is the variable**, while tasks, data and oracle stay fixed |
| L2 | Control of **catalogue curation** — the number and choice of primitive operations |
| L3 | Assessment of the **artefact** in the tool arm (existing assessment concerns calls) |
| L4 | Measurement of **silent spatial errors** as a separate outcome category |
| L5 | A **causal estimate** of the contribution of each validation level |
| L6 | Splitting the gain into "fewer errors" and "better repair" |
| L7 | A check of whether the mechanism is **local to geoinformation** or transferable (chemistry, medicine) |

---

# 3. Methods

## 3.1. The object of assessment

I decompose "integration method" into three components: the **surface** (the set of named operations), the **envelope** (the call and result format) and the **enforcement layer** (gates checking conditions). The variable in the experiment is the action channel and the enforcement depth; the envelope is a derivative of the channel.

I distinguish three levels of knowledge a tool may have about correctness:

| Level | What the tool knows | Example |
|---|---|---|
| **P-I — syntax** | whether the call matches the schema | the unit belongs to the set {m, km, ft} |
| **P-II — invariants** | whether the state after the operation is consistent with the data, without knowledge of the task | the CRS recorded in the file, valid geometry, the system's area of use consistent with the extent |
| **P-III — intent** | whether the result meets the task's requirement | "five kilometres", "in EPSG:2180" |

Level P-I is free in 2026 and does not differentiate interfaces: the decoding layer already provides it. The real value of gates lies in P-II, and P-III requires giving the tool an explicit task contract.

## 3.2. Conditions and contrasts

| Condition | Surface | Enforcement layer |
|---|---|---|
| **K** — code generation | one execution tool (`run_python`) | the interpreter only (language feedback) |
| **N1** — catalogue, basic level | named operations with signatures | input schema (P-I) |
| **N4** — catalogue, extended level | the same operations | invariants (P-II) and terminal conditions (P-III for the contract given in the prompt) |

Conditions N1 and N4 have **identical surfaces** — they differ only in the enforcement layer. This is a necessary condition for causal inference: if the surfaces differed, the effect of operation choice could not be separated from the effect of gates.

## 3.3. Equivalence assumptions

1. **A1 — oracle validity**: the predicates measure what the task is about.
2. **A2 — capability parity**: every operation available in the catalogue has a library equivalent in the code arm; the parity table is an appendix.
3. **A3 — information parity**: both arms receive the same task content and the same output contract.
4. **A4 — budget parity**: 25 model turns and 10 minutes of execution time.
5. **A5 — no drift**: the model, library versions and surface are frozen; runs are blocked by week.

Violating any of these does not invalidate the measurement but changes its interpretation; for each one it was written down in advance what it would mean (chapter 6.6).

## 3.4. Measures

| Measure | Definition | What it answers |
|---|---|---|
| **TSR** | share of artefacts satisfying all oracle predicates | correctness |
| **PCI** | share of errors caught **in the loop** (by the server or by language feedback) among all errors | catch rate |
| **S3** | error-class repeatability: share of tasks where the dominant class covers ≥ 75 % of failures | standardisation |
| **S4** | share of runs in the code arm whose script contains any check of the result | self-verification |
| **S4b** | among the checks in S4: share of **domain** checks versus language checks | content of verification |
| **S5** | completeness of the artefact's provenance record (inputs, version, parameters) | auditability |

The run register contains a `detected_by` column with four values: *language*, *own invariant*, *execution error*, *oracle*. Without that split, "the model wrote a check, but a language one" cannot be told apart from "the model wrote nothing".

**Methodological note.** Variance of outcomes is **not** a measure of determinism: the variance of a binary variable depends solely on its mean, so an increase in repeatability entails a drop in variance with no change in behaviour. Hence I measure standardisation by error-class repeatability, not by a variance test.

## 3.5. Taxonomies written down before measurement

Seven correctness gates: operation choice · names and types · values · preconditions · execution · result state · file contract. Eight classes of coordinate-system errors: non-existent code · existing but wrong code · false system in input metadata · missing transformation · omitted datum shift · units after transformation · system not written to the file · invalid geometry. Both taxonomies are closed before the run series and form an appendix. The class "system not written to the file" has two paths: the **file** one (an artefact written without a system declaration) and the **memory** one (a handle or array without accompanying georeferencing); the second is more dangerous, because an array carries neither the system, nor the transformation, nor the no-data value.

## 3.6. Analysis and power

The unit of analysis is the **task**, not the run. Contrasts are paired with McNemar's test; for simultaneous control of domain and repeatability, a mixed model with a random task effect. Confidence intervals by resampling. Reporting both in an intention-to-treat analysis (all tasks) and in a per-protocol analysis (tasks without a broken parity), with the reasons for exclusion stated explicitly.

With 80 tasks and four repetitions, **the smallest detectable difference is 14.0 percentage points** at an assumed between-task standard deviation of 10 points. This means that differences smaller than about 14 percentage points will be undecidable and will be described as such — not as "no difference".

## 3.7. The information-closure principle

A server gate may compare the result only with information the agent also has: I write that condition as `guard_information ⊆ agent_information`. If the task contract (target system, unit, expected extent) is given in the prompt, moving it into the tool signature **is not an oracle leak**. If, by contrast, the server compared the result with an expectation hidden from the agent, what would be measured is an oracle leak, not the action of the interface. Hidden expectations may only be a measurement gate on the harness side.

---

# 4. The research instrument

## 4.1. The corpus

Eighty task cards in eight domains of ten; thirteen cartographic cards whose artefact is a map or a composition. A card contains the task content, input files, the expected artefact, the oracle predicates with tolerances, a provenance record, and an indication of the trap the task is meant to trigger. Cards are in YAML; the register of rejected tasks is part of the appendix.

Every card is coded for its **expressible share**: seven requirement types (a value with a unit, the target system, the operation set, a spatial condition, the file contract, required result fields, a quality criterion), of which one counts the share of those that the surface takes as a parameter and can check. Coding is done by two coders on twenty cards, with agreement reported as kappa.

## 4.2. The surfaces

The catalogue covers primitive operations: describe a layer, buffer, clip, intersect, union, spatial join, zonal statistics, reproject, export. Every operation declares units, the required target system where that makes sense, and terminal conditions. Attached to the surface is a **parity table** — the mapping of every catalogue operation to a library function and version available in the code arm. Without that table the comparison could be undermined with one sentence.

## 4.3. The oracle

The oracle works on the artefact, not on the trajectory. Predicates: agreement of the coordinate system with the required one · presence of a system declaration in the file · geometric validity · extent coverage (IoU ≥ 0.95) · feature count · area within a percentage tolerance · presence of required attributes · integrity (input hashes, no writes outside the output directory). The oracle accepts two kinds of object: a file on disk and a handle returned by a tool. The predicate set includes `handle_carries_georeference` — the handle must carry the system, the transformation and information about missing data. The verdict is binary: an artefact is correct if and only if all predicates are satisfied.

## 4.4. The harness

The harness implements the agent loop, enforces the budget, runs both arms in the same container and records the run: number of turns, token usage, calls, artefact hashes, the result of every predicate and the `detected_by` column. The system prompt is **identical in both arms** and contains the same requirement to check the result before finishing.

---

# 5. How the experiment runs

The run series: three conditions × 80 tasks × 4 repetitions = **960 runs**, about five weeks of machine time, blocked by week to control drift.

The pilot covers 20 tasks in two conditions and four repetitions (160 runs) and serves only to estimate two quantities: the baseline error rate and the **share of error mass that is catchable** with the available information. Before the run series, three decision rules are written down:

| Rule | Condition | Decision |
|---|---|---|
| R1 | baseline TSR above 90 % or below 10 % | recalibrate corpus difficulty before the series, never after |
| R2 | catchable error mass below 25 % | the main claim moves from correctness to the structure of failure |
| R3 | capability parity broken for more than 10 % of operations | complete the surface or report it as a limitation |

Rule R2 is a safeguard against a situation in which the thesis "did not work out" only because the errors in the corpus turned out to be uncatchable. In that case the result is the structure of failure — not the absence of a result.

---

# 6. Expected results and their interpretations

## 6.1. The main axis

The basic contrast: TSR in condition N4 against condition K. Hypothesis H1: the difference is positive. Hypothesis H2: correctness rises with enforcement depth, with the expected shape **flat from N1 to N4 at the bottom and steep at the top** — the schema adds nothing over the decoder, terminal conditions add the most.

## 6.2. Six possible results and what follows from them

| Result | Difference | Depth curve | Catch rate | Permitted interpretation |
|---|---|---|---|---|
| **W1 — gate effect** | ≥ 14 pp | monotonic | higher in the catalogue | an interface with gates raises correctness, and the effect grows with enforcement depth; errors are caught before the artefact is written |
| **W2 — effect without mechanism** | ≥ 14 pp | flat | no difference | the difference exists but **does not come from gates**; another mechanism remains to be named (fewer turns, a smaller action space) |
| **W3 — mechanism without effect** | undecidable | monotonic | higher in the catalogue | gates **change the structure of failure, not its level**: errors are detected but not repaired |
| **W4 — zero** | undecidable | flat | no difference | standardisation of this kind yields nothing in this task class; the cause is uncatchable error mass or self-written checks in the code arm |
| **W5 — the other way** | negative, ≥ 14 pp | — | lower in the catalogue | the interface is a cost: fragmentation and turn count outweigh the gain from gates |
| **W6 — uninterpretable** | — | — | — | a ceiling or floor of correctness, broken parity, drift, or an unreliable oracle |

**W3 is the most instructive result for practice:** it shows that a gate alone, without a repair loop, buys auditability, not improvement. **W5 is not a failure of the thesis** — it agrees with the existing literature on the advantage of code execution and says that the boundary of the gain lies elsewhere than intuition suggests.

## 6.3. What remains in every scenario

Regardless of the main result, the thesis reports three claims: the size of the difference with a confidence interval and the value of the smallest detectable difference · the distribution of failures over error classes and gates · the frequency and content of checks in the code arm (S4 and S4b). The third is valuable even when the correctness difference turns out to be zero.

## 6.4. Moderator: the expressible share

Hypothesis H3: the difference grows with the task's expressible share. If it turns out flat across the whole range, the "gate" mechanism is false and another one must be sought. On cards with a low expressible share I predict a difference in catch rate but not in correctness — and that is a falsifiable prediction.

---

# 7. Discussion and conclusions

## 7.1. Answer to the title question

The answer will be phrased in three sentences, one each for: the size of the difference and its validity conditions; the mechanism through which the difference arises or does not; and what remains true regardless of the difference.

## 7.2. Implications for practice

For the integrator of a geoprocessing tool server the rule has three steps. Requirements that can be **expressed** in the signature — a unit, the target system, a clipping mask, the file contract — should be encoded as validated parameters. Requirements that cannot be expressed but are **checkable** on the result — geometric validity, a recorded system, consistency of area with extent — should be checked in the terminal conditions of every step. The rest, requiring a reference value, stay in a post-hoc control layer. An implementation in which all requirements land in the third group is not merely inexact but **unauditable** — and should not run without a human at the result.

## 7.3. Limitations

The corpus has no probabilistic representativeness: tasks are chosen deliberately to trigger specific error classes. One server, one model and one task class; replication on a second model may confirm or reverse the sign of the difference, but is not part of the design. No assessment of cartographic quality as an aesthetic judgement. Differences below the smallest detectable difference remain undecided.

## 7.4. Further work

A hybrid variant (reconnaissance through the catalogue, execution by code), moving the measurement to OGC API Processes as a **separate** arm, extending the corpus to tasks in which correctness is a matter of negotiation, and measuring surface drift across successive releases of the environment. The shortest route to checking whether the mechanism is not local is **moving the instrument into chemistry**, where domain checkers already exist (valence, mass balance, sanitisation); medicine needs a separate design, because it changes the objective from efficiency to harm and alert fatigue.

---

# Bibliography (key items; to be completed in the full version)

- Huang, J. et al. (2024). *Large Language Models Cannot Self-Correct Reasoning Yet*. ICLR 2024. arXiv:2310.01798.
- Kamoi, R. et al. (2024). *When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs*. TACL. arXiv:2406.01297.
- Wang, X. et al. (2024). *Executable Code Actions Elicit Better LLM Agents* (CodeAct). arXiv:2402.01030.
- Model Context Protocol, specification in revision 2026-07-28 (primary document: `modelcontextprotocol.io`).
- Comparative work on MCP versus code execution: CE-MCP (arXiv:2602.15945), MCP-Atlas (arXiv:2602.00933).
- Measurements of semantic error propagation in tool calls: AgentProp-Bench (arXiv:2604.16706).
- Geoinformation benchmarks: GeoAgentBench (arXiv:2604.13888), GeoNatureAgent (arXiv:2610.09112).
- Taxonomy of parameter errors: Findings of EMNLP 2025, aclanthology 2025.findings-emnlp.907.
- Tool-surface drift: MCPEvol-Bench (arXiv:2607.14642).

---

# Appendix A. Reference card A-01

```yaml
schema: 1
id: A-01
family: A
tier: T2
expressible: all
prompt: >
  Build a 5 km buffer around the roads from dane/drogi.gpkg and clip the result
  to the gmina boundaries from dane/gminy.gpkg. Save as wynik/bufor_gminy.gpkg
  in EPSG:2180.
inputs: [dane/drogi.gpkg, dane/gminy.gpkg]
expected_artifact: wynik/bufor_gminy.gpkg
oracle:
  reference: oracles/A-01.py
  seed: 42
  checks:
    - {type: crs_equal,     value: "EPSG:2180"}
    - {type: geom_valid}
    - {type: extent_iou,    value: 0.95}
    - {type: feature_count, value: 2481}
    - {type: attr_present,  value: [gmina_id]}
    - {type: scalar,        field: area_km2, value: 3912.4, tol_pct: 0.5}
negative_control:
  artifact: the same clip run on the unprojected input
  must_fail: [crs_equal]
pitfalls: [radius unit, clipping at the boundary]
```
