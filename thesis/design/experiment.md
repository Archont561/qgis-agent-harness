---
id: design/experiment
title: "The experiment: design and shape"
type: note
status: live
language: en
question: "What is measured, on what, and what comes out of one series?"
tasks: [TASK-1, TASK-8, TASK-11, TASK-12, TASK-21]
sources: [experiment.md, experiment-shape.md, experiment-full.md, research-design.md, evaluation-design.md]
updated_date: '2026-11-07'
---

# The experiment: design and shape

> What is measured, on what, and what comes out of one series?
>
> Merged 2026-11-07 from `experiment.md`, `experiment-shape.md`, `experiment-full.md`, `research-design.md`, `evaluation-design.md`. **Pruned and translated the same day** (`TASK-21`): 11,967 → 4,219 words. The pruned generation is listed in §14 with its reason; the two documents it overlapped with are `design/corpus.md` (which tasks) and `design/arms-and-validation.md` (which hypotheses).

**This document is written against the live design only.** Where the five source notes disagreed, the draft (`draft/thesis-draft-v0.md` §3–§5) and decisions `d-1`–`d-5` win; the contradictions that remain open are listed in §16 rather than smoothed over.

| Quantity | Value |
|---|---|
| Conditions | **K** (code generation), **N1** (catalogue, schema only), **N4** (same catalogue, invariants + terminal conditions) |
| Tasks | **80** cards (`design/corpus.md`) |
| Repetitions | **r = 4** per (task × condition) |
| Runs in the series | 3 × 80 × 4 = **960**, about five weeks of machine time, blocked by week |
| Pilot | 20 tasks × 2 conditions × 4 repetitions = **160 runs** |
| Unit of inference | the **task** |
| Smallest detectable difference | **14.0 pp** at τ = 10 pp between tasks (`design/corpus.md` §7.2) |
| Primary test | paired McNemar on the task level, one confirmatory comparison at α = 0.05 |

---

## 1. What the series must decide

One contrast carries the thesis, the rest are support:

| Question | What is manipulated | Where it is answered |
|---|---|---|
| Does the **way the same nine operations are exposed** change artefact correctness? | K versus N4 | **H1 — the confirmatory test** |
| Does correctness rise with **enforcement depth**? | N1 versus N4, same surface, different gates | H2, the depth curve |
| Does the difference **grow with the expressible share** of the task? | the moderator, coded per card | H3 |
| Are the interfaces **repeatable**, not merely different on average? | r = 4 per cell | S3, error-class repeatability |
| Do they differ in **where a mistake is caught**? | `detected_by` | PCI and the failure distribution |
| What does it cost **per successful task**? | token and turn logs | the cost claim, descriptive |

The hypothesis list, its falsification conditions and the inference table live in `design/arms-and-validation.md`; this document is the machinery that produces the numbers those hypotheses are tested on.

**Three claims survive whatever the main result** (`design/arms-and-validation.md`): the size of the difference with an interval and an explicit MDE · the distribution of failures over error classes and over the gates that did or did not catch them · the frequency and content of checks the model wrote for itself in the code condition (S4, S4b). The third is worth reporting even when the difference is zero.

## 2. The design in one table

| Factor | Levels | Type |
|---|---|---|
| **Condition** | K · N1 · N4 | within task (the same task runs in all three) |
| **Task family** | P · A · C | between tasks, the selection axis (`d-3`) |
| **Tier** | T1 · T2 · T3 · T4 | between tasks, descriptive |
| **Expressible share** | all · most · part · none | between tasks, the moderator of H3 |
| **Repetitions** | 4 | within cell |
| **Model** | one, pinned by name, version and date | **held fixed, not manipulated** |
| **Harness** | one, pinned | held fixed (`d-4`) |

The model and the harness are deliberately *not* factors: the thesis measures an interface difference, and a crossed model × harness design would need a series several times larger to say anything about either. This is a scope decision, and it is also the first item in the list of things further work would add (§15).

## 3. The three conditions

| Condition | What the agent gets | Enforcement layer |
|---|---|---|
| **K** — code generation | one execution tool (`run_python`) and the environment; it writes and runs a program | the interpreter only (language feedback) |
| **N1** — catalogue, basic | nine named operations with signatures and JSON schemas | **P-I**: is the call well-formed |
| **N4** — catalogue, extended | **the same nine operations, the same descriptions, the same schemas** | **P-II** invariants (is the state consistent with the data) and **P-III** terminal conditions (does the result meet the contract stated in the prompt) |

N1 and N4 have **identical surfaces** and differ only in the enforcement layer. That is a necessary condition for causal inference: if the surfaces differed, the effect of choosing named operations could not be separated from the effect of gates. It is also the reason this document keeps the operation list unchanged between the two catalogue conditions, down to the wording of the descriptions.

**The information-closure principle** (draft §3.7) constrains what a gate may do: `guard_information ⊆ agent_information`. If the task contract — target system, unit, expected extent — is stated in the prompt, then moving it into a tool signature **is not an oracle leak**. If a server compared the result against an expectation hidden from the agent, what would be measured is a leak, not the action of the interface. Hidden expectations may only be a measurement gate on the harness side.

### 3.1 Equivalence assumptions

| Assumption | Content | Written-down consequence if broken |
|---|---|---|
| **A1 — oracle validity** | the predicates measure what the task is about | the measurement changes meaning; the oracle audit (§8.4) is the evidence that it holds |
| **A2 — capability parity** | every catalogue operation has a library equivalent in the code condition; the parity table is an appendix | a gap above 10 % of operations is completed or reported as a limitation (rule R-3, §10) |
| **A3 — information parity** | both conditions get the same task content and the same output contract | the contrast becomes "same task, more information", which is a different thesis |
| **A4 — budget parity** | 25 model turns, 10 minutes of execution, the same token budget | an asymmetric budget is a confound, and the run is flagged, not discarded |
| **A5 — no drift** | model, library versions and surface frozen; runs blocked by week; a drift patch repeated at the end | the series is split at the drift point and reported as two blocks |

Violating one of these does not invalidate the measurement, it **changes its interpretation** — which is why each line has its consequence written down before the series, and why chapter 6 reports which assumptions held.

## 4. The instrument

**Corpus.** 80 cards; content, provenance, traps, predicates and the expressible share are specified in `design/corpus.md`, with the seed catalogue of 40 already written and the remaining 40 to follow under the same admission rules (`TASK-3`, `TASK-4`).

**The surface.** Nine primitive operations — describe a layer, buffer, clip, intersect, union, spatial join, zonal statistics, reproject, export — each declaring units, the required target system where that makes sense, and terminal conditions (`TASK-5`). Attached to the surface is a **parity table**: every operation mapped to a library function and version available in the code condition. Without that table, one sentence at the defence undermines the comparison.

**The oracle.** It works on the **artefact**, never on the trajectory. Predicates: coordinate system equal to the required one · presence of a system declaration in the file · geometric validity · extent coverage (IoU ≥ 0.95) · feature count · area within a percentage tolerance · presence of the required attributes · integrity (input hashes unchanged, no writes outside the output directory). The oracle accepts two kinds of object — a file on disk and a **handle** returned by a tool — and the predicate set includes `handle_carries_georeference`: the handle must carry the system, the transformation and the no-data information. The verdict is binary: an artefact is correct if and only if every predicate is satisfied.

Tolerances are **frozen before the sweep** and justified numerically (instrument precision, data resolution), never fitted to observed outcomes. `TASK-2` is the oracle; every card carries a negative control (§8.3).

**The harness.** It implements the agent loop, enforces the budget, runs all three conditions in the same container and records the run: turns, tokens, calls, artefact hashes, the result of every predicate and the `detected_by` value (`d-4`). The **system prompt is identical across conditions** and contains the same instruction to check the result before finishing. This is not a courtesy: if the code condition were told to self-check and the catalogue conditions were not, the comparison would measure the prompt.

## 5. One run, twelve steps

1. **Assignment.** The order of (task × condition × repetition) is drawn with a recorded seed in permuted blocks, so that no condition always runs first for a task.
2. **Fresh container** per run: images pinned by digest, empty working directory, cache off. The manifest records the QGIS version, `qgis_process --version`, the image digest, the model digest, quantisation and sampling parameters.
3. **Task load.** The prompt is the card's text, identical in every condition, with no hint about the *way* to solve it. Inputs are read-only; the output directory is named in the prompt.
4. **Agent run with limits**: 25 turns, 10 minutes, one token budget — identical in all three conditions. Exceeding a limit is a failure of class `timeout`, not a discarded run.
5. **(N4 only)** pre-execution validation of the call against invariants; a rejected call returns a message to the agent and one repair is allowed.
6. **Execution** in the engine; the artefact is written to disk.
7. **(N4 only)** post-execution validation of the result against the terminal conditions; one repair iteration.
8. **Close the run**: `prompt.txt`, `transcript.jsonl`, `calls.jsonl`, `artefact/` and **`result.json` written last** — its presence is what marks a run complete.
9. **Score**: the oracle runs on the artefact and writes `checks.jsonl` (predicate → expected → received → tolerance → pass/fail).
10. **Classify the failure** from `checks.jsonl` by rule, with ambiguous cases queued for manual coding (§8.4).
11. **Merge** into the analysis tables plus `manifest.json`. **No run is ever deleted**; failures stay in the data.
12. **Check**: `merge --check` compares the number of runs against the expected 960. A shortfall stops the pipeline; it is never "quietly topped up".

Steps 5 and 7 are the *only* difference between N1 and N4, and the code condition performs neither — the asymmetry is the manipulation, and the parity of everything else is what makes it interpretable.

## 6. What is logged

| Artefact | Content |
|---|---|
| `manifest.json` | QGIS and Processing versions, image digest, model digest, quantisation, sampling parameters, harness version, seed, limits, dates, block |
| `calls.jsonl` | every call: tool name or code block, arguments, time, input and output tokens, result (ok / error) |
| `transcript.jsonl` | the whole conversation, for qualitative analysis and the taxonomy |
| `checks.jsonl` | predicate → expected → received → tolerance → pass/fail |
| `artefact/` | output files plus checksums |
| `result.json` | status, error class, `detected_by`, aggregated measures |

The run register has **thirteen fields** (`TASK-16`) and includes `detected_by` with four values: **language**, **own invariant**, **execution error**, **oracle**. Without that split, "the model wrote a check — but a language check" cannot be told apart from "the model wrote nothing", and the thesis loses its most interesting diagnostic.

## 7. Measures

| Measure | Definition | What it answers |
|---|---|---|
| **TSR** | share of artefacts satisfying **all** oracle predicates | correctness |
| **PCI** | share of errors caught **in the loop** (server gate or language feedback) among all errors | catch rate |
| **S3** | error-class repeatability: share of tasks whose dominant error class covers ≥ 75 % of their failures | standardisation |
| **S4** | share of code-condition runs whose script contains **any** check of the result | self-verification |
| **S4b** | among the checks counted by S4: share of **domain** checks versus language checks | content of verification |
| **S5** | completeness of the artefact's provenance record (inputs, version, parameters) | auditability |
| cost | tokens, calls, seconds — **per successful task**, never per call | the practical claim |

**A methodological note that has to be in chapter 3.** The variance of a binary outcome is a function of its mean alone, so an increase in repeatability *entails* a drop in variance with no change in behaviour. A variance test would therefore "detect" standardisation it did not measure. Standardisation is measured by **error-class repeatability (S3)**, and repeatability of the artefact is reported through the predicate-level comparison of the four repetitions (identical / equivalent / divergent).

## 8. Scoring, taxonomy and the negative control

### 8.1 Gates and error classes, closed before the series

**Seven correctness gates:** operation choice · names and types · values · preconditions · execution · result state · file contract.

**Eight classes of coordinate-system error:** non-existent code · existing but wrong code · false system in the input metadata · missing transformation · omitted datum shift · units after transformation · system not written to the file · invalid geometry. The class "system not written to the file" has two paths — the **file** path (an artefact written without a system declaration) and the **memory** path (a handle or array without accompanying georeferencing). The second is more dangerous, because an array carries neither the system, the transformation, nor the no-data value, and it is exactly what `handle_carries_georeference` exists to catch.

Both taxonomies are frozen before the run series and belong in an appendix.

### 8.2 The failure taxonomy used for classification

Wrong layer or data · no validation → silent CRS error · invalid geometry · near-miss in topology · wrong parameter or wrong tool · aggregation that misses the intent · refusal or timeout. Classification is rule-driven from `checks.jsonl`; ambiguous cases go to manual coding.

### 8.3 The negative control is part of the card, not of the analysis

Every card must admit an artefact that **looks right and must be rejected** (`design/corpus.md` §5, rule 3). Without it, a predicate set is a wish: a tolerance nobody ever tried to break is a tolerance that has not been calibrated.

### 8.4 Agreement

**20 % of runs are coded blind by a second coder** (without knowing the condition), and kappa is reported. A second, cheaper audit: ten cards' predicates and tolerances are checked by an independent implementation. Both are reported even when agreement is poor — especially then, because that is an oracle defect, not a reviewer's opinion.

## 9. The analysis plan, frozen in the pre-registration

1. **One confirmatory comparison at α = 0.05**: TSR in N4 against TSR in K, on the task level, with a mixed logistic model carrying a random task effect; paired differences per task reported alongside.
2. **Everything else through Holm** within its hypothesis family; the remainder is exploratory, with intervals and no stars.
3. **The depth curve** is a **trend** (a linear contrast N1 → N4 plus a plateau fit), not a pair of tests — the question is the shape, not which of two cells wins.
4. **H3** is an interaction between condition and expressible share, reported with the predicted pattern stated in advance: a growing difference where the surface can carry the requirement, a difference in catch rate but **not** in correctness where it cannot.
5. **Intervals by resampling over tasks**, never over runs.
6. **MDE stated up front** — 14.0 pp at τ = 10 pp — and an insignificant result reported as **undecided**, never as "no difference".
7. **Degrees of freedom are counted from tasks**, not from runs. With r = 4 the design-effect inflation is ≈ 3, so 960 rows are worth roughly 320 independent rows, and the claim is about 80 tasks.
8. **Both an intention-to-treat and a per-protocol analysis**, with the reasons for exclusion stated. If the two disagree, that disagreement is a finding about parity or about the corpus, and it is reported rather than resolved silently.

## 10. The pilot and the three decision rules

The pilot is 20 tasks × 2 conditions × 4 repetitions = 160 runs. It produces exactly two quantities: the baseline error rate, and the **share of the error mass that is catchable** with the information the agent actually has. Three rules are written down **before** the pilot and are not revisited after it:

| Rule | Condition | Decision |
|---|---|---|
| **R-1** | baseline TSR above 90 % or below 10 % | recalibrate corpus difficulty **before** the series, never after |
| **R-2** | catchable error mass below 25 % | the main claim moves from correctness to the **structure of failure** |
| **R-3** | capability parity broken for more than 10 % of operations | complete the surface, or report the gap as a limitation |

R-2 is a safeguard against a thesis that "does not work out" only because the corpus's errors turned out to be uncatchable. In that case the result is the structure of failure — not the absence of a result.

## 11. Six outcomes, written before the measurement

| Result | Difference | Depth curve | Catch rate | Permitted interpretation |
|---|---|---|---|---|
| **W1 — gate effect** | ≥ 14 pp | monotonic | higher in the catalogue | an interface with gates raises correctness, and the effect grows with enforcement depth; errors are caught before the artefact is written |
| **W2 — effect without mechanism** | ≥ 14 pp | flat | no difference | the difference is real but **does not come from gates**; another mechanism has to be named (fewer turns, a smaller action space) |
| **W3 — mechanism without effect** | undecidable | monotonic | higher in the catalogue | gates **change the structure of failure, not its level**: errors are detected but not repaired |
| **W4 — zero** | undecidable | flat | no difference | standardisation of this kind yields nothing in this task class; the cause lies in the uncatchable error mass or in the checks the code condition writes for itself |
| **W5 — the other way** | negative, ≥ 14 pp | — | lower in the catalogue | the interface is a cost: fragmentation and turn count outweigh the gain from gates |
| **W6 — uninterpretable** | — | — | — | a ceiling or floor effect, broken parity, drift, or an unreliable oracle |

**W3 is the most instructive outcome for practice:** a gate without a repair loop buys auditability, not improvement. **W5 is not a failed thesis** — it agrees with the existing literature on executable code and says the boundary of the gain lies elsewhere than intuition suggests. **W6 is the one outcome that cannot be reported as a result**, which is why the floor effect is predicted in advance for family C (`design/corpus.md` §4).

## 12. What would kill each claim

| Claim | What would falsify it |
|---|---|
| H1 — N4 differs from K | an interval containing zero at an MDE of 14 pp (undecided, not refuted) or a negative difference ≥ 14 pp (refuted, W5) |
| H2 — correctness rises with enforcement depth | a flat or non-monotonic depth curve with the catch rate also flat — the gates would then be inert |
| H3 — the difference grows with the expressible share | a flat interaction across the whole range; or a correctness difference on cards whose expressible share is *none* — which would mean the difference is not about what the surface can carry |
| The mechanism is catching, not repairing | a higher catch rate with an unchanged TSR (which is W3, not a refutation of the measurement but of the mechanism) |
| Repeatability differs | identical error-class distributions across conditions, with S3 equal and the predicate-level repetitions identical |
| The interface is a cost | W5 itself |

## 13. Threats and controls

| Threat | Control |
|---|---|
| order or warm-up effects | rotation of conditions per task, fresh container per run, cache off and reported |
| tolerance tuning towards the result | tolerances inside the cards, justified numerically, hashed and frozen **before** the sweep |
| authoring the surface to fit the tasks | the catalogue written against documented workflows, a parity table, and the anonymised-catalogue control (`design/corpus.md` §10) |
| "one CLI effect" | one harness, pinned, identical system prompt; the harness is not a factor and the limitation says so |
| model or service drift | model and image digests in the manifest; the drift patch repeated at the end, ≤ 2 tasks differing between the start and the end of the series |
| pseudo-replication | inference at the task level; df from tasks; the run count never called a sample size |
| vanishing runs | `merge --check` against the expected 960; a shortfall stops the pipeline |
| a ceiling or floor | rules R-1 and R-2 before the series; the floor predicted for family C; W6 as the interpretation if it happens anyway |

## 14. What was pruned, and why

| Cut | Came from | Reason |
|---|---|---|
| arms A1–A9 (tool ladder L1–L4, `codegen+gate`, `surface+gate`, adversarial, meta) | `experiment` | the live design has **three** conditions in an **enforcement** ladder, not nine in a tool-count ladder; the tool-count ladder is retired with `min_surface` (`design/corpus.md` §11) |
| claims V2–V7 | `experiment` | superseded by H1–H3 plus the three claims that survive any result; the hypothesis list has one owner (`design/arms-and-validation.md`) |
| two front-ends (`opencode`, `goose`) as a crossed factor | `experiment` | one pinned harness (`d-4`); crossing it would multiply the series for a claim the thesis does not make |
| the 50-task corpus, 1 416 and 4 768-run matrices | `experiment`, `experiment-full` | 80 tasks, 960 runs (`d-2`) |
| simulated chapter-6 results, hypothesis by hypothesis (H1–H7), five seeds | `experiment-full` | the simulation and its artefacts were removed on 7 XI 2026; writing chapter 6 in advance has been replaced by W1–W6, which fix the *interpretations* without inventing numbers |
| "it is not an experiment without these six things" as a separate section | `experiment-shape` | folded into §5 (procedure), §6 (logging) and §13 (threats) — the list was a summary of things already stated |
| the operational-definition essay on evaluating a protocol | `evaluation-design` | kept only as §7 and §9; the argument itself lives in `framing/gap-and-literature.md` and `design/arms-and-validation.md` |
| the bibliography stub of §7 | `evaluation-design` | one bibliography, in `literature/literature.bib`; a second list in a note is a second list to keep in step |
| `PIPELINE.md`, `runs.csv`, `simulated_results.json`, `scripts/*` | several | removed on 7 XI 2026 by instruction: they described a pipeline that measured nothing. The stage names and the register contract survive in §5, §6 and `TASK-16` |

What deliberately survived all five notes: the twelve-step procedure, the run-directory contract with `result.json` last, the "never drop a run" rule, the thirteen-field register with `detected_by`, the metric definitions, both taxonomies, the kappa audit, the inequality `guard_information ⊆ agent_information`, the equivalence assumptions with their consequences, the pilot rules R-1–R-3, the six outcomes, and the threats table.

## 15. What the series does not model

Deliberately outside: map aesthetics as a judgement · security in general (three adversarial cards would be a sample, not a test) · production scale (catalogues of hundreds of operations) · engines other than QGIS · a second model, a hybrid condition (reconnaissance through the catalogue, execution by code) and an OGC API — Processes arm, all named as further work in chapter 7.

The limits that must be stated in chapter 7, whatever the result: one model, one server, one task class, a corpus without probabilistic representativeness, and differences below the MDE left undecided.

## 16. Open items before G1

1. **The corpus composition sentence in the draft contradicts `d-3`.** `draft/thesis-draft-v0.md` §4.1 still says "eighty task cards in eight domains of ten", while `d-3` makes the P/A/C family the selection axis and the domain a descriptive label (`design/corpus.md` §3). The draft sentence has to change; the decision does not.
2. **The parity table** (operation → library function and version) must exist as an appendix before the pilot, or A2 is an assertion.
3. **Freeze and publish** the tolerances, the seven gates, the eight CRS classes and the failure taxonomy, with hashes, before the first pilot run.
4. **Close the numbers** — `TASK-1`: the pilot's two estimates feed the final MDE statement, and the 14.0 pp figure must be restated with the τ actually estimated rather than assumed.

## 17. One sentence

**Three conditions expose the same nine operations with a different amount of enforcement, 80 tasks run four times each for 960 runs with the task as the unit of inference, the artefact is scored by typed predicates rather than by a judge, one confirmatory paired comparison at an MDE of 14 pp decides the thesis, and the six possible outcomes have their permitted interpretations written down before the first run.**
