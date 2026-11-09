---
id: writing/critique
title: "Critique review: design and thesis plan"
type: note
status: live
language: en
question: "What is still wrong with the design, in order of severity?"
updated_date: '2026-11-07'
---

# Critique review: design and thesis plan

Reviewer-style assessment of the design in [`design/experiment.md`](../design/experiment.md). Three
questions answered first (task families, task count, why measure tool count), then a severity-ranked
review with fixes, a rubric, and a two-week action list.

Verdict up front: **the design is sound in kind and under-specified in degree.** Nothing here is
fatal; four things must be fixed before the first real run, and one is a scope decision that will
otherwise eat the timeline.

---

## 1. Should presentation tasks be graded differently from analysis tasks?

**Yes — and more strongly: they should not be pooled into the same outcome.**

Styling a map and running an analysis have different *success constructs*:

| Family | What "correct" means | Can it be verified objectively? |
|---|---|---|
| **P — preparation / IO** (load, reproject, clip, join, export) | the data on disk is right | yes — geometry/attribute predicates |
| **A — analysis** (buffer, overlay, aggregate, network, statistics) | the numbers and geometries are right | yes — same predicates, plus numeric tolerance |
| **C — cartography / presentation** (symbols, classification, labels, layout, export) | the *requested style properties* were applied and the map renders | partly — properties yes, aesthetics no |

A response that produces a correct result with an ugly map is a success on P/A and a failure on C. A
beautiful map over wrong data is a failure on both. If you average them into one TSR, a paradigm that
happens to be good at the *easy-to-verify* presentation tasks can look better while being worse at
analysis — and the headline number becomes uninterpretable. Two acceptable organisations:

1. **Family as a blocking factor** (recommended): report TSR per family, use family as a fixed factor,
   and pre-register which families form the *primary* outcome (P+A) and which are secondary (C).
2. **Presentation as a separate exploratory block**, excluded from the confirmatory tests.

For family C, verify **declarative properties of the project/output**, not pixels:

| Check | Reads |
|---|---|
| `layer_count`, `layer_names` | project state |
| `crs_equal` | layer CRS |
| `style_type:categorized\|graduated` | renderer class |
| `class_count`, `class_field` | renderer categories |
| `colour_ramp_present` | renderer ramp |
| `label_field`, `label_placement` | labelling config |
| `layout_elements:title,legend,scalebar` | layout objects |
| `export_exists`, `export_dpi`, `export_extent_iou` | the rendered artefact |
| `raster_non_blank` | rendered image is not empty |

These are objective and cheap. Do **not** add an LLM judge for "does it look nice" — that reintroduces
exactly the weakness the rest of the design avoids.

There is a second, better reason to keep family C in the design: **it is the sharpest test of the
catalogue's coverage limit.** QGIS styling is an enormous, deeply nested API; a curated 15-tool MCP
surface will cover it badly, while code generation handles it in a few PyQGIS lines. The
family × paradigm interaction is therefore a direct, GIS-specific instance of the
"opaque vs transparent composition" argument in `strickland2026pareto`, and where code generation
*should* win. A thesis in which MCP wins on analysis and loses on cartography is far more credible —
and far more useful — than one where it wins everything.

---

## 2. Is 5 tasks too little? Should it be 50?

Two different numbers are being conflated, and both matter:

- **5 → 15 is the number of *tools*** in the surface arms (`mcp-5`, `mcp-15`), not the number of tasks.
- **50 is the number of *tasks***, and it is not obviously enough — see §3.1 for the power arithmetic.

On task count specifically:

| Purpose | Tasks needed | Why |
|---|---|---|
| Plumbing / smoke test | 3–5 | prove the harness runs end to end |
| Calibration pilot (`--stage pilot`) | 10 | choose the wide surface, screen (CLI, model) pairs |
| Pooled confirmatory claim (PB1) | ≥ 50 | 50 is adequate **only** for effects ≥ 25 pp at α = 0.0083, or ≥ 20 pp at α = 0.05 |
| Family-level claim (P vs A vs C) | ≥ 12 per family | 3 tasks per cell is anecdote, not evidence |
| Tier-level claim (PB2) | ≥ 12 per tier for the tiers you claim | otherwise report the interaction descriptively |

So: 5 is a fine **starting** number to build end-to-end, 50 is the **minimum** for the pooled claim,
and if you keep both families and tiers you are really looking at **60–100 cards** (e.g. 3 families ×
20, each spanning the four tiers, plus 5 adversarial). The runs scale linearly; the *cards* are the
long pole (§4, P0-4).

---

## 3. Why measure the number of tools at all?

Because surface size is the one knob a practitioner actually holds when they build an MCP server, and
because it is the only contrast in your design that stays meaningful even if the main hypothesis dies.

1. **It is a design decision, not a feature of nature.** Anyone shipping a GeoMCP server chooses
   between a 5-tool minimal surface and a 50-tool kitchen sink. Your result tells them which.
2. **The literature says the effect is real but was never tested with execution.**
   `tool_exposure_gnss_2026` moves tool-selection F1 from **0.635 to 0.849** purely by changing how
   the catalogue is exposed, while scoring generated plans and never running them. MCP-Atlas mixes a
   mean **11.1 distractor tools** per task; MCP-Bench attaches **10 distractor servers**. The
   distractor effect is established; the *GIS execution* consequence is not.
3. **It is a within-paradigm contrast.** Even a null in MCP-vs-codegen leaves PB7 interpretable, which
   protects the thesis against its worst-case outcome.
4. **It tests a mechanism claim**: "opaque vs transparent composition" predicts that a bigger surface
   helps coverage and hurts selection, and that the balance shifts with task complexity — an
   interaction, not a main effect. That is a theory-relevant test, not a tuning exercise.
5. **A null is actionable.** If 5 ≈ 15, the guidance is "do not build a large server" — cheap,
   publishable, and immediately useful.

Caveat that must stay in the thesis: 5 and 15 are both small against production MCP (100–500 tools),
so the claim is about *catalogue ambiguity at tractable scale*, not production-scale realism
(`design/experiment.md` §9).

---

## 4. Review findings, ranked

Severity: **P0** = fix before the first real run; **P1** = fix before writing results; **P2** = nice to
have.

### P0-1 — The confirmatory tests are probably underpowered

I simulated the planned paired comparison (assumptions: latent task
difficulty N(0, 0.55), constant paradigm shift, 3 reps per task, paired t-test on task-level
proportions, 1,200–2,000 simulated studies):

| Tasks | Δ (success-rate difference) | Power at α = 0.0083 | Power at α = 0.05 |
|---|---|---|---|
| 50 | 10 pp | 0.12 | 0.33 |
| 50 | 15 pp | 0.32 | 0.62 |
| 50 | **20 pp** | **0.62** | 0.83 |
| 50 | 25 pp | 0.83 | 0.96 |
| 50 | 30 pp | 0.94 | 0.99 |
| 100 | 20 pp | 0.95 | 0.99 |

And if the analysis degrades to a **single-run-per-task McNemar** (i.e. it ignores the 3 reps), power
at 50 tasks collapses: 0.02 / 0.05 / 0.10 / 0.19 / 0.32 for Δ = 10…30 pp. **The replication is the
power** — an analysis that treats one run per task as the datum throws away most of the design.

Fixes, cheapest first:

1. **Pre-register the hierarchy**: one primary confirmatory test (PB1, TSR) at α = 0.05; the other
   five are secondary, reported with CIs and labelled exploratory. Holm–Bonferroni across the family
   is the compromise (uniformly more powerful than Bonferroni at the same FWER). Six tests at
   0.0083 is defensible, but only if you accept "≥ 25 pp or nothing".
2. **Analyse at task level, exploiting reps** (paired t / Wilcoxon on task means, or a mixed model
   with task random intercept and rep as a repeated measure) — never a single-run-per-task test.
3. **Compute and state the MDE** in the methods chapter (`power_mde.py` is committed for exactly
   this), and treat a non-significant result as *inconclusive*, not as "no difference".
4. If you need to detect ~15–20 pp at the corrected α, **go to 100 tasks** or restrict the primary
   claim to one paradigm contrast on 100 tasks (mcp-15 vs codegen, one model = 1,800 runs, same as
   the current full factorial).

### P0-2 — Pseudo-replication is the reviewer's first bullet

1,800 runs are not 1,800 independent observations: three reps of one task are correlated, and 50 tasks
are the real sampling unit for generalisation. The mixed model handles this, but the *claim* must be
phrased at task level ("across 50 tasks…"), the degrees of freedom must come from tasks, and Figure 1
should show per-task paired differences, not only pooled means. Say it explicitly, or a statistical
reviewer will.

### P0-3 — Task-family heterogeneity is unaddressed (see §1)

Mixing presentation and analysis tasks into one TSR makes the headline uninterpretable and inflates
variance. Fix: family as a factor, primary outcome = preparation + analysis, presentation reported
separately, family-specific check vocabularies.

### P0-4 — The oracle/fixture work is the real schedule risk, not the runs

65 cards ≈ 65 oracle scripts + fixtures + tolerances. At a realistic 1–2 days each that is 3–5 months
of work, dwarfing a 2,400-run sweep. Mitigations:

- build **10 cards end-to-end first** (one per family × tier), freeze the card format, then batch;
- generate variants **programmatically from one fixture pack** (same city, parametrised operations)
  rather than hand-authoring each task's data;
- reuse published fixtures where licences allow (GeoBenchX, GIS Copilot data) instead of inventing
  new geometries;
- cap the corpus at what you can verify: **60 well-verified cards beat 100 rushed ones**, and the
  power you lose is recoverable, the credibility you lose is not.

### P0-5 — Tolerance tuning can manufacture the result

If the oracle's tolerances are adjusted until both arms behave as hypothesised, the study measures the
author, not the paradigms. Freeze tolerances in the cards *before* seeing results (they are already
part of the card hash), derive them from numerical reasoning (projection accuracy, floating-point
accumulation) rather than from observed output, and have a second person code a random 20 % of runs
blind for the failure taxonomy (report κ).

### P1-1 — The paradigm bundle is still an undeclared confound

MCP-5/MCP-15/codegen differ on representation, surface size, discovery and execution locus
simultaneously. The 2 × 2 (representation × validation) in `framing/edge-of-scope.md` fixes the gating half;
the surface half needs the `mcp-5` vs `mcp-15` contrast to be run at *fixed required capability*
(distractors as the manipulation), not by making some tasks unsolvable in the small arm — otherwise you
are comparing "narrow" with "impossible".

### P1-2 — The adversarial block cannot carry a hypothesis test

Five tasks × proportions will not clear any corrected α. Reframe as a **qualitative security probe**
with an explicit detection criterion ("the poisoned description caused a call that would otherwise not
have been made, observed in the transcript"), reported as counts with exact CIs, and keep the claim
narrow: "the spatial blast radius is plausible-looking wrong output, not an error".

### P1-3 — ED resolution with 3 reps is coarse

Three runs give three pairwise comparisons; the classes identical/equivalent/divergent are honest but
blunt. Either add 2 reps on a 10-task subsample to check whether ED is stable at n = 5, or state the
coarseness as a limitation and report the raw artefact hashes.

### P1-4 — The MCP catalogue is itself a treatment, and it is undocumented

Which 5 and which 15 tools, at what granularity (atomic vs task-level), with what schema richness
(does `reproject` declare CRS domains? do tools declare units?) determines both the coverage and the
gate's power. This needs its own short design document and must be frozen with `cards.lock`, or the
whole "surface size" factor is a post-hoc artefact.

### P1-5 — A hybrid arm is missing, and it is what practitioners actually do

Real agents discover capability through MCP and then write code to fill gaps. Without a
**hybrid** condition (MCP discovery + code execution with the same sandbox), the thesis answers "A or
B" while practice does "A then B". Cheapest form: one exploratory arm, 2 agents × 50 tasks × 3 reps =
300 runs. If you drop it, say why in the limitations — a reviewer will ask.

### P1-6 — No qualitative validation of the tasks

Three to five GIS analysts reviewing 10 cards for realism and ambiguity is half a day of work and buys
ecological validity that no statistic can. `strickland2026pareto` used 18 expert interviews; you need
far fewer, but not zero.

### P2 — Smaller items

- **Scope inflation**: PB1–PB5, PB7, PB8, PB9, gating, surfaces, adversarial, transfer probe. Cut PB6
  (ITS), cut the transfer probe, keep 3 of the 5 adversarial cards, and the thesis gets deeper.
- **Domain coverage**: vector only, one city's fixtures, no raster/remote sensing, no temporal or
  network analysis. Either add one raster family or state the boundary in the title of the results
  chapter.
- **Token accounting is CLI-dependent**: CLIs count tokens differently (and some hide them). Cross
  check with server-side usage from vLLM logs, or cost comparisons across front-ends are noise.
- **Failure taxonomy needs two coders** — one coder is a rubric, not a measurement.
- **Report per-task paired differences and the cost–reliability frontier** as figures; pooled bars
  hide exactly the heterogeneity you claim to explain.

---

## 5. Rubric

| Dimension | Score (1–5) | Comment |
|---|---|---|
| Novelty / gap definition | 4 | measurement gap, well argued, correctly disclaimed against MapHub/OGSAgent |
| Construct validity | 3 | spatial artefacts + replication are strong; paradigm bundle and family mixing are the holes |
| Internal validity | 3 → 4 | same-engine control is good; catalogue and tolerance freedoms are live risks |
| Statistical adequacy | 2 | 50 tasks at α = 0.0083 detects only ~25 pp; fixable with hierarchy/MDE/100 tasks |
| Feasibility / timeline | 2 | oracle+fixture authoring, not compute, is the binding constraint |
| Practical significance | 4 | surface guidance, cost frontier, failure taxonomy are all usable |
| Reproducibility | 4 | frozen cards, manifest, pinned stack — better than most of the corpus |

**Overall: major revision of the design before the sweep — not before the writing.** The thesis is
publishable as designed; it is the *claims* that need tightening to match the power that exists.

---

## 6. Two-week action list (in order)

1. Adopt the analysis hierarchy (one primary at α = 0.05, Holm for the rest) and paste the MDE table
   into the pre-registration. *(1 day)*
2. Split the corpus into families; rewrite the card schema to require `family` and family-specific
   check sets (`experiment/tasks/README.md`). *(1 day)*
3. Write the catalogue design note: the 5 and the 15, with granularity and schema richness, and freeze
   it. *(2 days)*
4. Build 10 cards end-to-end (one per family × tier) with oracles; run the pilot on them; measure
   turns/tokens/wall-time for the HPC case. *(5 days)*
5. Decide the hybrid arm, PB6, transfer probe: keep or cut — and write the decision down. *(1 day)*
6. Only then scale the corpus to 50–60 and start the real sweep.
