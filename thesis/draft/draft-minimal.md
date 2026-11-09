---
id: draft/draft-minimal
title: "The minimalist thesis draft — what it checks, how, what can come out, and what follows"
type: draft
status: live
language: en
tasks: [TASK-8]
updated_date: '2026-11-07'
---

# The minimalist thesis draft — what it checks, how, what can come out, and what follows

> The **minimal but defensible** version: the smallest design that satisfies §III.9 of the faculty's degree rules (a hypothesis, a manipulated factor, causal inference), fits the schedule, and leaves material for two papers.
> Every number (MDE, runs, weeks) comes from the formula used in the other documents (τ = 10 pp), not from memory.
> Depends on: `writing/requirements.md` (the full structure), `design/runs.md` (what one run looks like), `design/arms-and-validation.md` (the claim ledger), `draft/structure.md` (chapters and pages).

---

## 1. What the thesis checks

**In one sentence:** whether the way geoprocessing tools are exposed (a tool catalogue through a protocol, versus code generation) changes **artefact correctness**, and whether any difference comes from **enforcing correctness conditions** rather than from the mere use of a protocol.

**Four questions, in order of importance:**

| # | Question | The answer we are looking for |
|---|---|---|
| **P1** | Are artefacts from the catalogue condition more often correct than from the code condition? | a difference **Δ** in the share of correct artefacts (TSR) |
| **P2** | Does Δ grow with **enforcement depth** (schema → invariants → terminal conditions)? | the slope of the N1 → N4 curve |
| **P3** | Are errors **caught inside the loop** (by the server) or only after the fact (by the oracle)? | the `detected_by` distribution and PCI |
| **P4** | In the code condition, does the model **write its own checks** — and of what kind (linguistic or domain)? | S4, S4b |

**The claims (written down before measurement, each with a falsification condition):**

- **H1:** Δ > 0 — higher correctness in the catalogue condition (K versus N4), tested by paired McNemar at task level with a mixed logistic as a companion. One confirmatory test, α = 0.05.
- **H2:** correctness rises **with enforcement depth** (N1 → N4 on an identical surface); the predicted shape is a **trend**, not a pair of tests. Corrected within the family by Holm.
- **H3:** the difference **grows with the expressible share** of the task — the condition × share interaction, with the pattern stated in advance.
- **D1–D3** (descriptive, intervals and no stars): the conditions differ in **repeatability** (S3), in **failure signature** (the seven failure classes, `detected_by`), and in **cost per successful task**.
- **D4** is a precondition, not a finding: the oracle repeats and the artefact verdicts agree across repetitions. A "significant" D4 would mean the meter is broken.

**Unit of analysis:** the task (not the run). **Primary criterion:** an artefact that satisfies every oracle predicate. **Not** an assessment of the trajectory, **not** an LLM judge.

---

## 2. How it does it — the minimal version

| Element | Value |
|---|---|
| **Conditions** | three: **K** (one tool, `run_python`, executing code) · **N1** (the nine-operation catalogue, schema validation only) · **N4** (the same catalogue, invariants plus terminal conditions). A fourth condition gains no MDE for +320 runs, and is retired (`d-2`) |
| **Corpus** | 80 tasks in three families, of which **13 cartographic cards** (family C — the SGP qualification condition) |
| **Repetitions** | r = 4 (seed and temperature recorded in the manifest) |
| **Runs** | 3 × 80 × 4 = **960 ≈ 5.1 weeks** of engine time across 8–16 Slurm tasks |
| **MDE** | **14.0 pp** (N = 80, r = 4, τ = 10); at r = 8 → 10.3 pp, for twice the cost |
| **Held fixed** | the same instruction, data, model and seed, container, library versions, budget (**25 turns / 10 minutes** / one token budget), output contract, oracle, and **the identical paragraph about checking the result** |
| **Varied** | the action channel; then enforcement depth as the second factor |
| **Oracle** | predicates on the artefact: CRS equal, valid geometry, extent IoU ≥ 0.95, object count, area within tolerance, required attributes present, integrity (input hashes, no writes outside the run directory) |
| **Log** | `detected_by ∈ {language, own_invariant, execution_error, oracle}`, turns, tokens, artefact hashes |
| **Analysis** | McNemar as the primary test, a mixed logistic on the unit "task", GEE as the marginal companion; ITT **and** PP; Holm over {H2, H3} |
| **Pilot** | 20 tasks × 2 conditions × r = 4 = **160 runs** — solely to measure the **baseline error rate** and the **share of the error mass that is catchable** |

**Three decision rules written down BEFORE the series of runs:**

| Rule | Condition | Decision |
|---|---|---|
| **R1** | baseline TSR > 90 % or < 10 % | recalibrate corpus difficulty (before the series, never after) |
| **R2** | catchable share of the error mass < 25 % | the main claim moves from "correctness" to **"the structure of failure"** (PCI, S3) — stated in advance, not after the result |
| **R3** | capability parity breaks for more than 10 % of operations | complete the surface, or report it as a limitation and analyse ITT |

---

## 3. What the thesis looks like

| Chapter | Pages | What it must contain |
|---|--:|---|
| 1. Introduction | 7 | the problem, three audiences, the thesis sentence, the contributions, **what the thesis does not claim** |
| 2. Literature review | 14 | four currents (action format / MCP / MCP versus code / GIS), the comparison table, the gap, **self-correction and external feedback** |
| 3. Materials and methods | 15 | the object of assessment (surface / envelope / enforcement), the equivalence assumptions A1–A5, the contrasts, **the measures S3, S4/S4b, S5**, the taxonomies B1–B7 and E1–E8 written down before measurement, power and the MDE, ITT/PP, information closure |
| 4. The instrument | 14 | the corpus of 80 cards, the three surfaces (one catalogue in two enforcement configurations) plus **the parity table**, the oracle, the harness, the identical instruction, the reproducibility package |
| 5. Execution | 6 | schedule, blocking, the pilot and rules R1–R3, handling failures, the deviations register |
| 6. Results | 18 | §6.1 TSR (H1) · §6.2 the depth curve N1 → N4 (H2) · §6.3 PCI and `detected_by` (D1, D2) · §6.4 the moderator: expressible share (H3) · §6.5 S4/S4b in the code condition · §6.6 families (descriptive) · §6.7 robustness |
| 7. Conclusions | 8 | the answer to the title in three sentences, **recommendations for integrators**, limitations, further work |
| Appendices | — | A–G: the 80 cards, the predicates, the parity table, the pre-registration, the statistical tables, the container build, the harness defence |

**The minimum set of artefacts without which there is no thesis:** 80 YAML cards · an oracle with four CRS predicates and a negative control · one catalogue in two enforcement configurations plus the parity table · a code condition in the same container · a `detected_by` column · a pre-registration carrying the MDE · the reproducibility package. **The minimal version trims pages, never these.**

---

## 4. The possible results — six scenarios

The main axis is **Δ (H1)**. The mechanism axes are **the slope of the depth curve (H2)** and **PCI (D1/D2)**.

| # | Scenario | Δ | Depth curve | PCI | What produces it |
|---|---|:--:|:--:|:--:|---|
| **W1** | **the gate effect** | ≥ MDE | monotone | higher in N4 | catchable mass ≥ 50 %, the server enforces invariants and terminal conditions |
| **W2** | **an effect without the mechanism** | ≥ MDE | **flat** | no difference | Δ from something else: fewer turns, a different attention structure, a smaller action space |
| **W3** | **the mechanism without the effect** | ≈ 0 | monotone | **higher in N4** | gates catch errors, but repair does not turn into correctness (the repair bottleneck) |
| **W4** | **zero** | ≈ 0 | flat | no difference | the error mass is uncatchable; or the code condition writes its own domain checks |
| **W5** | **the other way** | < 0 | — | lower in N4 | the cost of fragmentation: more turns, more opportunities, a chain of dependencies |
| **W6** | **uninterpretable** | — | — | — | ceiling or floor effects, broken parity, drift, an untrustworthy oracle |

---

## 5. Every interpretation — what may be claimed in each scenario

| Scenario | The admissible claim | What has to be added | For practice | The title |
|---|---|---|---|---|
| **W1** | "an interface with gates raises correctness by Δ, the effect grows with enforcement depth, and errors are caught before the artefact is written" | nothing — this is the target result | encode invariants and terminal conditions; the schema alone is not enough | the title holds in full |
| **W2** | "the difference exists, but **does not come from the gates**" | exploratory analysis: turns, tokens and calls as mediators; an honest admission that H2 is refuted | do not overpay for validation if only the result matters | the title holds, but the mechanism claim does not |
| **W3** | "gates **change the structure of failure**, not its level: errors are detected but not repaired" | mediation analysis of repair; the split between "fewer errors" and "better repair" | a gate without a repair loop is an audit, not an improvement — **the most interesting result for practice** | a "detectability" title fares better than a "correctness" one |
| **W4** | "standardisation of this kind **achieves nothing** in this class of task" | proof that the error mass was uncatchable (R2), or that the code condition writes its own checks (S4b) | do not invest in gates; invest in model knowledge or in post-hoc QA | the detectability title survives; the correctness title only conditionally |
| **W5** | "the catalogue interface is **expensive**: fragmentation and turn count outweigh the gain from gates" | the cost distribution: turns, tokens, latency; a comparison with the literature on code agents | for this class of task choose code; gates only for high-risk tasks | the title holds, **but it must promise an assessment, not an advantage** |
| **W6** | "unresolved at an MDE of 14.0 pp" | diagnostics: why (ceiling, parity, drift) | nothing follows — and that is what must be written | none; it is a methodological result |

**Always, whatever the scenario — three claims that remain:**
(a) the size of Δ with its CI and the MDE · (b) the distribution of failure by class · (c) the frequency and content of the checks the code condition writes (S4/S4b).

---

## 6. What follows

**For research:** in every scenario what remains is **the vocabulary** (B1–B7, E1–E8, P-I/II/III, `detected_by`), **the instrument** (the artefact oracle, PCI, the expressible share) and **a result** — including a negative one. That is exactly the combination that does not age with the next model release.

**For practice (the shortest version, for §7.2):**
- **W1/W3** → encode invariants and terminal conditions; a gate without a repair loop buys auditability, not correctness.
- **W2** → do not buy validation "just in case"; measure what actually makes the difference.
- **W4/W5** → in this class of task the interface can be a cost; choose it for high-risk tasks (CRS, units, areas), not for speed.

**For the competitions:** scenario **W3** is the best for the PTI award ("significance for computing" — a mechanism, not an application), **W1** for the Minister's Award and the cartographic competition, and **W5** is the hardest to sell — which is why family C must be in the corpus whatever the result.

**The calendar:** pilot (0.8 week) → **decision on R1/R2** → the series of 960 runs (5.1 weeks) → analysis (2 weeks) → writing (6 weeks) → formatting and competitions (1 week) ≈ **15 weeks**, with slack for one stumble.

---

## 7. In one sentence

**The minimal version is three conditions (code, catalogue with schema, catalogue with invariants and terminal conditions) × 80 cards × 4 repetitions = 960 runs at an MDE of 14.0 pp: it checks whether the action channel changes artefact correctness, whether the effect grows with enforcement depth, and whether errors are caught inside the loop — and the six possible results have six different interpretations written down in advance, none of which ends in "the study failed", because in every scenario the same vocabulary, the same instrument and an honestly named result remain.**
