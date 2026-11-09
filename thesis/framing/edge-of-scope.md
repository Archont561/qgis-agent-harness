---
id: framing/edge-of-scope
title: "The edge of the scope"
type: note
status: live
language: en
question: "What does this thesis not claim, and where would the claim stop holding?"
sources: [geoinformation-only.md, substrate-choice.md, environment-generalisability.md, thesis-strength.md, schema-gating.md, ai-mcp-gis-guide.md]
updated_date: '2026-11-07'
---

# The edge of the scope

> What does this thesis not claim, and where would the claim stop holding?
>
> The negative half of the scope. Everything else under `framing/` says what the work **is**; this says where it **stops** — first as a list of sentences the thesis refuses to write (§1), then as three boundaries that generate those refusals: the domain (§2), the substrate (§3), the comparison itself (§4). §5 is the hierarchy that decides whether the result is worth having, §6 the cut log, §7 five lines and a sentence.
>
> Pruned and translated 2026-11-07 (`TASK-21`): 9,126 → 7,551 words, six source notes → seven sections.

---

## 1. What the thesis does not claim

| # | The claim it refuses | Why | Where the honest version lives |
|---|---|---|---|
| 1 | "MCP is better than code generation" | the comparison is three conditions on one harness and one engine; a general ranking is not what was measured | §5, and `design/experiment.md` §8 |
| 2 | "Interfaces matter for AI agents" | a claim about the world, not about this measurement; it is too wide to fail | H1–H3 in `scope-and-character.md` §5.3 |
| 3 | "We contribute a framework / an MCP server" | the artefact is an **instrument**; a server without a measurement adds to the pile the field already has | `design/arms-and-validation.md` |
| 4 | "This is how GIS analysis is done" | analysts click buttons; all three conditions are headless. The unit is the **operation**, not the interaction | §3.6, threat 4 |
| 5 | "Geoprocessing with agents, in general" | the corpus is the traditional-geoprocessing stratum only — no remote sensing, no geostatistics, no network analysis | `design/corpus.md` §3 |
| 6 | "Agents are becoming autonomous" | agent architecture is held constant by design (`K` has the same loop); this is not a study of autonomy | `design/experiment.md` §5 |
| 7 | "Model X is better than model Y" | one model (`d-2`); the model is a nuisance parameter, not a factor | `backlog/decisions` `d-2` |
| 8 | "Validation boundaries are a new idea" | they are standard practice in software and were specified for tool use before this thesis | `design/correctness.md`; the gates are **measured**, not proposed |
| 9 | "Gating is what makes MCP better" | the live design cannot separate gating from representation; §4 says exactly how much of the claim survives | §4.3 below |
| 10 | An effect smaller than 14.0 pp | 14.0 pp is the resolution floor at τ = 10; anything below it is **unresolved**, not zero | `analysis/statistics.md` §2 |

The rule that generates all ten rows is one line: **claim ⊂ evidence.** The reviewer does not ask whether the work is good; they ask whether every sentence is covered by what was measured. Three editorial rules follow, and they cost no compute:

1. **Narrow the noun.** QGIS 3.44 was measured, so the text says "QGIS 3.44", not "GIS". Eighty tasks in one stratum were measured, so it says that, not "geoprocessing practice".
2. **Absence of significance is not absence of difference**, outside a designed equivalence test. Below the MDE the correct word is *unresolved*.
3. **Every non-zero result carries its limitation in the same paragraph**, not in a closing "Limitations" section — nobody returns to a closing section.

A useful read-aloud test before submission: take any sentence from the discussion, then point at the row of the results table that licenses it. Sentences with no row are the ones that cost marks, and they are found faster this way than by rereading the whole chapter.

---

## 2. Boundary 1 — the domain

**The question.** Is the silent error a property of geoinformation, or of any field in which the artefact has a correct type and a meaningless sense? Medicine and chemistry also depend on domain knowledge without which a well-typed result is nonsense.

**In three sentences.** (1) No — it is a property of every domain in which **the result is a value of the right type whose meaning depends on knowledge outside the language**. (2) Geoinformatics is a good *first* proving ground because its invariants are cheap and deterministic and its register of meaning (EPSG, `proj.db`) is machine-readable, so gates can be built and measured. (3) The differences between domains are not cosmetic: they change the **ceiling of gate coverage** and the **objective function**.

### 2.1 Seven properties that produce a silent error

| # | Property | Geoinformation | Chemistry | Medicine | Plain code |
|---|---|:--:|:--:|:--:|:--:|
| 1 | **operations are total** — any argument yields a result | ✓ buffer, clip, reclassify | ✓ a reaction "runs" for any template | ✓ any dose is a number | ✗ the compiler rejects it |
| 2 | **the type does not encode meaning** | `float` metres vs degrees | mass vs concentration vs moles | mg vs µg vs mg/kg | usually encoded |
| 3 | **metadata is separated from the payload** | CRS and transformation outside the array | reaction conditions, standard state | lab units, patient context | no metadata |
| 4 | **meaning depends on order and state** | topology, overlay, NoData | stoichiometry, stereochemistry, template match | interactions, renal failure | partly |
| 5 | **the error is costly but not trivial** | expensive, rarely dangerous | expensive, wastes a synthesis | **harm to a patient** | usually cheap |
| 6 | **cheap domain checkers exist** | extent, area, geometry validity | valence, mass balance, sanitisation | only partly (dose, interaction databases) | complete |
| 7 | **judgement needs a human** | rarely | rarely | **often** | no |

Geoinformation has 6 of 7 properties, chemistry 6 of 7, medicine 7 of 7 — but in medicine property 6 is weak and property 7 strong. That changes **what can be built**, not **what the problem is**.

### 2.2 Evidence from other fields — this is not an analogy of ours

**Chemistry, near-identical formulation.** MolViBench (`arXiv 2605.02351`) describes exactly this: code can **run without error and return a chemically wrong result** — the model calls RDKit correctly and silently confuses stereochemistry, applies the wrong reaction template, or returns a molecule that violates constraints. The authors call it *runnable but chemically wrong* and propose layered evaluation: type-aware comparison of outputs plus semantic analysis of the API calls.

**Chemistry, the level distinction ready-made.** Work on molecular-string correctness (`arXiv 2509.23099`) separates **syntactic** from **semantic** correctness: `C#C=C` parses and is chemically wrong, because the middle carbon exceeds valence 4. That is the P-I / P-II distinction of this thesis, stated earlier and more sharply.

**The design pattern already exists — under MCP.** Work on compiling ontologies into tools (`arXiv 2602.03439`) turns formal ontology constraints into **executable MCP tools**, so the model gets feedback during the call rather than after it; one example is a tool that checks a unit of measure against the ontology's permitted values. That is the same concept as the P-II gates here. The difference — and this is the contribution — is that there a design is *shown*, whereas here the question is **how much it buys, causally, against generated code**.

**Medicine — checking works, but the objective is different.** MEDIC (*Nature Medicine*, 2024) combines rules with pharmacological knowledge and flagged **95.1 %** of previously reported "near-miss" events for correction. At the same time, the clinical decision support literature has fought **alert fatigue** for decades: knowledge-based rules fire on alerts irrelevant to the patient, and the excess teaches staff to ignore them. Add the known failure modes: **unit conversion errors**, dependence on local forms, and **automation bias** once the tool is trusted.

### 2.3 Three domain profiles, three design consequences

| Profile | When | What the gate is | What the objective is |
|---|---|---|---|
| **A — invariant gates** | invariants cheap and deterministic (geoinformation, chemistry) | conditions on the operation's output | raise the share of correct artefacts |
| **B — reference gates** | a knowledge base is needed (medicine: doses, interactions; chemistry: compound registries) | comparison against the base plus rules | **reduce harm without alert fatigue** |
| **C — escalation** | judgement requires a human | a question to the human, a refusal, a marked uncertainty | do not mislead |

**The most important transfer:** in profile C the gate stops being a filter and becomes a **question**. That is precisely the capability MCP provides through `resultType: "input_required"` — one of three strategies used here for class E2, and **the default strategy in medicine**, because a gate that guesses is worse than a gate that asks.

### 2.4 What transfers from this work, and what does not

| Element | Transfers? | Note |
|---|:--:|---|
| **The phenomenon and its definition** (right type, wrong sense) | **yes** | MolViBench confirms it independently in chemistry |
| **The level distinction** P-I syntax / P-II invariants / P-III intent | **yes** | in chemistry it is the syntax / semantics / task-conditions split |
| **The instrument** (artefact oracle, in-loop capture, `detected_by`) | **yes**, with a modification | medicine: the artefact is sometimes a recommendation, so adjudication is needed as well |
| **The design rule** (constraints attached to the operation, not the artefact; the handle carries the georeference) | **yes** | in chemistry the handle carries conditions and conventions |
| **The information-closure principle** (a gate may not know more than the agent) | **yes** | universal |
| **The effect size (ΔTSR) and the ceiling of gate coverage** | **no** | both depend on the expressible share, which is a property of the (task, domain) pair — and is exactly what H3 makes a variable |
| **The objective function** | **no** | geoinformation: correctness; medicine: harm and alert fatigue |

### 2.5 Why geoinformatics is a good first proving ground

1. **Invariants are cheap and deterministic** — extent, area, geometry validity, CRS presence. The check can be computed, not adjudicated.
2. **Meaning is machine-coded** — the EPSG registry and `proj.db` provide an "area of use" per CRS, i.e. domain knowledge already in checkable form.
3. **Operations are total** — any argument yields a result, so silence is the rule rather than the exception.
4. **The error is costly but not dangerous** — synthetic data, no ethics approval, no patient risk.
5. **A reference implementation exists** — QGIS and PROJ let one ask whether a failing gate is a gate bug.

What medicine lacks as a *first* ground is point 4 entirely and point 1 partly. It is therefore the **next** step, and the hypothesis there is not "do gates raise correctness" but **"does a gate with escalation reduce harm without alert fatigue"** — a different hypothesis, a different measure, and a research project of its own.

### 2.6 Two sentences to place

**For §2 (contribution, not limitations):**

> The phenomenon this work measures is not a property of geoinformation: in chemistry it is called *runnable but chemically wrong*, in medicine it is bound up with unit conversion and alert fatigue. Geoinformation was chosen because it alone combines the three conditions a causal measurement needs — invariants that are cheap and deterministic, meaning codified in a machine-readable registry, and an error that is costly without being dangerous.

**For §7.4 (future work):** moving the instrument to chemistry, where the checkers already exist (valence, mass balance, sanitisation), is the **shortest** route to testing whether the mechanism is local; medicine requires a separate design because it changes the objective function.

---

## 3. Boundary 2 — the substrate

Answering: *"I chose QGIS because it provides the common GIS tools for an end-to-end analyst workflow, and because it is open source — is that right?"* The choice is right. **The two stated reasons are not the ones that survive a viva**, and one of them invites a one-line rebuttal.

### 3.1 The reason that actually carries the thesis

Not "open source", not "common tools": **QGIS is the only mainstream substrate where the same operation is reachable both as a declared call and as generated code, on an identical runtime.**

| Requirement of the design | Why only QGIS satisfies it |
|---|---|
| same-engine control | `qgis_process run native:buffer` and `processing.run(...)` reach the same C++ implementation; the MCP tool and the generated script execute the *same* algorithm |
| bounded vs unbounded coverage as the treatment | the Processing toolbox is an enumerable catalogue (bounded); PyQGIS is the whole API (unbounded) — both in one install |
| headless, pinned, containerised | `QgsApplication` + `qgis_process` under a pinned QGIS 3.44 image; no licence server, no GUI |
| artefact-on-disk scoring | GeoPackage / GeoJSON / GeoTIFF / PNG are written deterministically, so the oracle predicates have something to read |
| an executable, not an invented, catalogue | `qgis_process list` enumerates algorithms with types and defaults, so the S1 ⊂ S2 ⊂ S3 ladder is *mechanically* validatable |
| existing MCP servers to compare against practice | MapHub, GeoMCP, GIS Copilot, `qgis_mcp` all wrap QGIS — the substrate the field actually wraps is the one being tested |

That is a **methodological necessity, not a preference**: without it, "nested tools versus code" cannot be separated from "engine A versus engine B", and that separation is the whole identification of this thesis.

### 3.2 Grading the alternatives

| Substrate | Same-engine call + code | Headless / pinnable | Enumerable typed catalogue | Real MCP servers | Licence | Verdict |
|---|---|---|---|---|---|---|
| **QGIS 3.44** | ✔ Processing + PyQGIS | ✔ container, no licence | ✔ `qgis_process list` | ✔ several | GPL-2, free | **chosen** |
| GRASS GIS | ✔ modules + scripts | ✔ | ✔ | ✘ rarely wrapped | GPL, free | strong on rigour, weak on practice |
| ArcGIS Pro / ArcPy | partly (arcpy ≈ GUI operations) | ✘ licence, Windows | ✘ proprietary | ✘ | ✘ | impossible for a 960-run sweep |
| PostGIS | ✔ SQL vs SQL | ✔ | ~ | few | GPL, free | a database, not an analyst workflow |
| GDAL/OGR only | ✔ | ✔ | ✔ | some | permissive | too low-level: no analyst operations |
| GeoServer / OGC services | ✘ no equal code path | ✔ | ✘ | few | free | service integration, not desktop GIS |

The row that gets asked about is ArcGIS, and the answer is one sentence: **ArcGIS was rejected because a repeatable, licence-free execution environment cannot be guaranteed for it, not because of its availability.** Three blockers, the first sufficient: the licence and Windows platform make a reviewer's rerun impossible; Esri's terms restrict publishing comparative benchmarks without consent, which would void the comparative point of the work; and in ArcGIS both conditions would collapse into `arcpy`, since no mature MCP server for Pro tools is known to exist.

### 3.3 The two stated reasons, graded

**"Common GIS tools for an end-to-end analyst workflow"** — true of the substrate, not yet true of the design.

- The Processing toolbox is roughly 1 000 algorithms over native, GDAL, GRASS and SAGA providers, which comfortably covers the analyst core: load, reproject, clip, join, buffer, overlay, dissolve, raster algebra, zonal statistics, layout export.
- But "end-to-end" is a claim about the **card corpus**, not about QGIS's feature list. It holds only once each tool in the surface is **anchored to a documented workflow** — QGIS training manual chapters, the PyQGIS developer cookbook, the task sets of GIS Copilot / GeoBenchX / MapHub — rather than to whatever one personally reaches for. One day of work: the anchor goes next to each tool in the catalogue.
- The honest boundaries: **network analysis** (needs GRASS or pgRouting), **geostatistics** (GeoDa, R), **cartographic generalisation**, **3D and temporal animation**, **field collection**, **imagery pipelines beyond raster algebra**. Declare them; do not let "end-to-end" be read as "every GIS workflow".

**"Open source"** — an enabler, not the differentiator.

As a headline it invites *"GRASS and GDAL are open source too — why QGIS?"*, and there is no answer, because openness does not distinguish. What openness actually buys, in one clause rather than a paragraph: **reproducible pinning** (a versioned container anyone can rebuild), **redistributable fixtures and artefacts** (a replication package that survives review), **auditable ground truth** (the oracle re-derivable from the same open implementation), and **no licence barrier to replication**. So: *open source is what makes the comparison reproducible, not what makes it interesting.*

### 3.4 Which layer of the QGIS stack is "the GIS"?

This matters more than the product choice and is easy to leave implicit.

| Layer | Size | Fits | Problem |
|---|---|---|---|
| **Processing algorithms** (`qgis_process`) | ~1 000, typed, documented | the K/N1/N4 ladder, mechanical nesting validation | **cartography is not here** |
| **Raw PyQGIS API** | unbounded | what the code condition writes | not enumerable, so it cannot be a bounded surface |
| **Plugins / GUI** | unbounded | not headless | unusable in a sweep |

**The decision to record:** the tool surface = Processing algorithms **plus a small set of hand-written PyQGIS wrappers for styling, labelling, layout and export** — because in QGIS cartography lives in the PyQGIS API and only partly in Processing. Two consequences. First, the N4 catalogue is family-balanced (~15 cartography tools) and the schemas matter most there, because those wrappers are *ours*: their descriptions and constraints are a **treatment** that must be documented and frozen like the cards. Second, several Processing algorithms are thin wrappers over GDAL, GRASS or SAGA, so "QGIS tools" is shorthand for "the QGIS Processing interface to a stack of providers". Name the provider per tool in the catalogue: it is free provenance, and it turns "your tools are just GDAL" from a criticism into a disclosed fact.

### 3.5 Why not a second engine — and the cheaper ladder

The thesis is about the **interface** with the engine held constant. Adding an engine adds a **third factor** and a `engine × interface` interaction question. To answer it one needs tasks **within each engine**, i.e. a corpus twice the size — roughly 80 more tasks and 80 more days of oracle work, more than the total budget. Treating the engine as a **replication** instead is not generalisation either: it is one extra point that either agrees or not, and nothing follows from one point.

**GRASS** is open, headless and containerisable, so it does not fail technically. It fails on two design grounds: its **module granularity** differs from QGIS Processing, so the 5/15/30 ladder cannot be carried over — a new catalogue would have to be designed, and then H3 is not replicated but studied afresh; and its **default semantics** differ (computational region and resolution, vector cleaning, NoData handling), so all 40 oracles would have to be **re-validated** against different defaults. That is not a conversion, it is a new tolerance calibration, the most expensive part of the instrument. Cost: 6–8 weeks, the whole corpus block of the plan.

The objection — *"is the result not a property of QGIS?"* — has five cheaper answers:

| # | Move | What it tests | Cost | Verdict |
|---|---|---|---|---|
| **R1** | **Substitution slice** (same agent × other server, same server × other client) — ~90 runs | **substitutability**, the value the protocol claims for itself | already in budget | **do** — the most on-target answer, because it is about the thesis, not the engine |
| **R2** | **Two API depths in QGIS**: `qgis_process` (CLI) vs `processing.run` vs `qgis.core` | whether "code" as a condition is an artefact of one API | ~1 week, **0 new oracles** (the checks read artefacts from disk) | **do** |
| **R3** | **The raster family** (1–2 tasks in family A) | whether the result is a property of vector data | ~2 weeks | **consider** if time is left |
| **R4** | **GRASS, 5 tasks, 2 conditions × 3 repetitions = 30 runs** — reported as **feasibility**, not as a result | that the harness is portable through an adapter, empirically rather than by promise | ~3 days | **do** — kills the "single substrate" objection with evidence |
| **R5** | GRASS as a full replication (80 tasks) | the `engine × interface` interaction | 6–8 weeks | **no** — that is a different thesis |

**R4 is the most important row.** A reviewer asking *"is this not a property of QGIS?"* is not waiting for a second full experiment; they are waiting to learn whether the instrument is portable **by construction**. Five GRASS tasks reported as feasibility, a 40-line adapter in an appendix, and one sentence in the limitations is a complete answer. A promise sounds like an excuse; a demonstration on five tasks sounds like a decision.

### 3.6 Threats to validity that this choice creates

| Threat | Mitigation |
|---|---|
| **Version drift** — algorithm IDs and parameters change between releases | pin QGIS 3.44; record `qgis_process --version` in every run manifest |
| **Catalogue authorship bias** — the tools, their names and descriptions are ours | anchor to documented workflows; write in QGIS terminology; review blind to the tasks; freeze with the cards lock |
| **Expressiveness asymmetry** — code gets all of PyQGIS, the surface gets a catalogue | that asymmetry **is** the treatment; state it, and make coverage loss measurable via the `expressible` share each card records |
| **Desktop reality** — analysts click buttons, all three conditions are headless | scope the claim to *operations*, not interaction; say so in the limitations |
| **Single substrate and single grain** — nothing follows for Esri, PostGIS, web-GIS, or a different module granularity | R1, R2, R4 above; full replication named as a separate study rather than an extension |
| **Determinism assumptions** — QGIS and GDAL have threaded and floating-point nondeterminism | that is what D1 measures; never assume byte-identical output, test it |

### 3.7 The sentences for the methods chapter

> QGIS 3.44 was chosen because it is the only mainstream GIS in which a given operation is reachable both through a declarative, schema-described interface (`qgis_process` / Processing) and through generated code (PyQGIS) on an identical runtime, which lets the integration method be varied while the engine is held constant; it is also headless, pinnable in a container and freely redistributable, which is what makes a 960-run sweep reproducible. The tool surface is a curated subset of the Processing catalogue plus hand-written PyQGIS wrappers for cartography, since map styling is not exposed through Processing.

And in the limitations, one sentence: the result concerns one engine and one tool granularity; the instrument is portable through an adapter, shown on five GRASS tasks, but **the comparison has not been run on a second engine**.

Three reviewer questions, three one-sentence answers:

| Question | Answer |
|---|---|
| "Why not ArcGIS?" | "Because a repeatable, licence-free execution environment cannot be guaranteed for it, and without one the sweep is not reproducible." |
| "Is this not a property of QGIS?" | "The interface is variable at constant engine only because QGIS allows it; instrument portability is shown on five GRASS tasks, and a full replication is a separate study of the engine × interface interaction." |
| "Why not GRASS, if it is more rigorous?" | "Because the 5/15/30 ladder is defined against QGIS Processing granularity; on GRASS a new catalogue and a full oracle re-calibration would be needed — that is a different thesis, not a wider one." |

---

## 4. Boundary 3 — what the comparison can prove

The third boundary is the comparison itself, and it is the one most easily overstated. It is also where the design changed most: the two-by-two that an earlier round proposed is **not** what is being run, and saying so precisely is what makes the claim defensible.

### 4.1 Three regimes, not three points on an axis

The literature distinguishes **schema-described** from **schema-gated** systems: one uses schemas to describe tool interfaces but permits unvalidated actions; the other makes the schema the sole path to execution. The three live conditions sit in different places:

| | **K — code** | **N1 — narrow tools** | **N4 — composed tools** |
|---|---|---|---|
| Where the contract lives | library API surface, implicit in docs and type hints | JSON Schema per tool (`inputSchema`), server-enforced | JSON Schema **plus** preconditions across steps: data-flow types, dependency order, parameter compatibility |
| When validation happens | at execution: the interpreter raises, or GDAL/QGIS raises, or nothing raises | at call time, before that one call runs | before a step runs, over the composed plan |
| What a violation looks like | `TypeError`, `KeyError`, a GDAL error, or a valid-looking wrong map | typed protocol error the model can read and repair | typed rejection naming the violated cross-step constraint, before side effects |
| Failure class produced | `argument_semantics`, `spatial_reasoning`, **silent wrongness** | `contract` (recoverable), then semantics | `contract` at plan level, or refusal |
| Expressiveness | open world: any Python, any library | closed world: the catalogue | closed world, smaller still |
| Instrumentation on the wire | none — must be built (import whitelist, helper catalogue, AST checks) | `args_schema_valid`, `in_catalogue`, error types, free | same, plus pre-execution rejection events |

The distinction that matters is in the validation rows, not the representation row. MCP already gates *each call*; that is mainstream. What almost no GIS benchmark tests is that **tool-level validity does not imply plan validity**: each invocation is locally valid and the composed plan is unsound. The worked example in the literature is scientific (train on columns the previous step never produced); the GIS equivalents are immediate:

- buffer in metres after a silent reprojection failure — every call well-typed, every distance wrong;
- join on a field the previous step renamed — locally valid, composed unsound;
- overlay two layers in different CRSs, where QGIS reprojects on the fly and produces a plausible map;
- aggregate before filtering — again well-typed at every step.

Code generation cannot express a *pre-execution* check of any of these, because its "schema" is a Python library: validation is the interpreter running it. That is the whole asymmetry, and it is what H2 makes measurable as **enforcement depth** (N1 → N4).

### 4.2 The confound to name: gating is orthogonal to the protocol

**Schema gating is not a property of MCP.** MCP can be run ungated; generated code can be gated by a static checker. So "gated tools versus plain code" confounds two things — the representation (a JSON call versus program text) and the validation boundary. The clean design is a 2 × 2: `{tool call, code} × {ungated, gated}`, in which the within-representation contrast gives the value of the boundary, the within-gating contrast gives the value of the representation, and the interaction cell decides what the headline claim can be.

**The live design does not contain that 2 × 2, and that is a decision, not an oversight.** Three conditions, 960 runs, 80 tasks and one model are what the budget buys at a resolution of 14.0 pp; a fourth cell would halve that resolution or double the corpus, and the corpus — not the arms — is what the power rests on. What the design does instead:

- the **representation** contrast is `K` against the tool conditions;
- the **enforcement-depth** contrast is `N1` against `N4`, which is a gating gradient *inside* the tool representation;
- the missing cell — **gated code** — is named in the limitations, and §4.3 states exactly which readings of the result it leaves open.

That is a materially weaker instrument than the 2 × 2 and a materially stronger thesis than a four-arm design run at unresolvable resolution. The honest sentence for the discussion: *"the thesis measures whether enforcement depth helps within a tool surface, and whether a tool surface helps against code; it does not measure whether gated code closes the gap, and therefore cannot attribute the whole of any difference to validation."*

### 4.3 What each outcome would prove

Pre-registered now, because these are the interpretation rules and they are what protects against post-hoc storytelling.

| Outcome | Reading | Strength of claim |
|---|---|---|
| N4 > N1 on TSR at modest cost | early structured feedback is the active ingredient within the surface | mechanistic claim about *why* tools help — strong |
| N4 ≈ N1, both > K | the advantage is the representation and the catalogue, not the boundary | claim moves from gating to structured interface; still publishable |
| N4 ≈ K | the boundary, not the protocol, carries the effect | the honest and probably most valuable result; reframes MCP as an engineering standard |
| N4 > N1 on strict tasks, more refusals on `fuzzy` ones | the determinism/flexibility trade-off reproduced at task level | scope condition: gating buys reliability at the price of flexibility |
| The N1–N4 difference appears only in tiers 3–4 (multi-step) and not on single-tool tasks | plan-level failure is exactly what composition introduces | supports the locally-valid / composed-unsound mechanism directly |
| No effect anywhere | enforcement depth is not where the value lies — consistent with MCP as a thin wrap, and with findings that MCP can hurt | a null that still answers the comparison question |

The last row deserves emphasis: a well-run null is a **finding**, because the field currently assumes gating helps and reports almost no test of it.

### 4.4 How to measure it without defining the outcome into existence

In a gated condition nothing executes unless it validates, so "conformance of executed calls" is 1.0 by construction. Any metric defined as executed-calls-that-are-valid hands the win to the gate trivially — which is why **TSR and the artefact signatures, not conformance, are the primary measure**, and why the intercept rates below are the secondary ones:

| Metric | Definition | Why it survives the trap |
|---|---|---|
| **IRR** — interception rate | attempts rejected by the gate ÷ all attempts | counts what the boundary caught; comparable with the *invalid* calls of the ungated condition |
| **RRR** — repair success | P(success \| ≥ 1 rejection of class c) | the real question: after a rejection, does the agent recover? |
| **T2V** — turns to a valid plan | turns and tokens spent before the first fully valid plan | the cost half of the trade-off |
| **REF** — refusal rate | tasks answered "the surface does not support this" ÷ unsupported tasks | a gate should make correct refusal *possible*; `fuzzy` tasks test over-refusal |
| **Cost per success** | tokens, calls, wall time per success | the boundary should show up here first |

Two implementation notes. **Type the rejections** — the error must name the violated constraint (`CRS mismatch: layer A EPSG:4326 vs layer B EPSG:2180`); a generic "invalid arguments" gives the model nothing to repair and turns the gated condition into a noisier ungated one, which is exactly what the `contract` class in the failure taxonomy exists to count. And **bound the repair loop** — two retries, then fail — otherwise enforcement becomes a compute subsidy and the comparison is between budgets rather than mechanisms.

### 4.5 What this comparison cannot prove

- **Not "tools beat code generation" in general.** Only for this catalogue, this engine, these 80 tasks, this model. The interaction terms are the honest deliverable.
- **Not that gating is necessary.** A type-checked Python pipeline with a strict helper API could match it; that is the `codegen-gated` cell, and if a later study finds it matches, the claim moves to standardisation and adoption cost.
- **Enforcement trades failure for refusal.** A gate that rejects the only viable plan converts a wrong answer into no answer. TSR alone cannot see that; `REF` and the `fuzzy` tier can.
- **Plan-level validation is only as good as the schema.** If the N4 schemas do not encode CRS, units or geometry type as constraints, the gate cannot catch the GIS-specific silent errors. The schema design is therefore part of the treatment and must be frozen and documented like the task cards.

---

## 5. Strength — why the weakest link decides

This section answers a general question but settles it on this thesis, because a general answer without an application is useless. It completes the rubric in `writing/critique.md` §5; several items marked weak there have since been resolved.

**One sentence:** strength is the **product** of four things — identification, measurement validity, inferential power, and resistance to alternative explanations — so the weakest link decides; and one editorial factor, **whether the claim is narrower than the evidence**, removes marks more often than any of the four.

A distinction to make immediately: **strength ≠ importance.** A study can be strong and interesting to nobody (a well-measured irrelevant effect), or weak and important (a good question answered badly). Strength is judged by the methodologist, importance by the audience. A master's thesis is graded primarily on strength, because importance cannot be defended in twenty minutes.

### 5.1 The four factors, and the diagnostic question for each

| Factor | The question | State here | Cheapest improvement |
|---|---|---|---|
| **Identification** — does it follow that A affects B | can the difference be attributed **solely** to the declared factor? | **strong**: one loop, one engine, two tool sets; `K` differs in neither prompt, turn limit, container nor model | describe it in §3 as an *identification device*, not an implementation detail |
| **Measurement validity** — is what is claimed what was measured | does TSR mean "did the task correctly" or "produced a file of the right name"? | **medium, and the priority**: tolerances (IoU ≥ 0.5, permitted CRS deviation) and predicates written after seeing results measure our own decision | **freeze tolerances and predicates before the sweep** and publish them in the manifest — one editorial decision, not more runs |
| **Power** — can signal be told from noise | what is the smallest effect this work **can** detect? | **deliberately limited**: 14.0 pp at τ = 10; everything below is unresolved, not absent | paste the MDE into §3 and call sub-MDE results *unresolved*; keep the unit of inference at **task**, not run, or it is pseudo-replication |
| **Resistance to alternatives** | what is the most likely other explanation, and was it excluded in the text or only in the author's head? | **strong construction, weak description** | one paragraph in §1: the three alternatives and why the design discriminates |

Three threats to measurement validity deserve naming, because each is one careless afternoon away: tolerances set **after** seeing results; oracles written **around a known solution**, so the predicate tests an implementation rather than correctness; and cartographic predicates that check QML syntax instead of visual effect, so the file format is what is measured.

The alternative explanations, in the order a reviewer will think of them: (a) the tool catalogue is simply *better written* than the code prompt; (b) models know tool schemas better than they know PyQGIS from memory; (c) the advantage of the catalogue **is** argument validation. **(c) is also the main hypothesis** — which is why this work is strong here rather than vulnerable: instead of hiding the alternative it becomes the moderator (H3). That is rare enough to be stated explicitly in §1.

### 5.2 Why a product, not a sum

| Situation | Perfect | Failing | Result |
|---|---|---|---|
| 10 000 runs, two variables at once | power | identification | **zero** — nobody knows what acted |
| perfect control, TSR from file names | identification | measurement validity | **zero** — something else was measured |
| everything correct, 8 tasks | identification, validity | power | **unresolved** — not zero, but nothing is claimed |
| everything correct, claim wider than evidence | — | claim fit | **marks deducted**, despite good work |

The practical consequence: **a weak link cannot be repaired by strengthening a strong one.** More runs do not fix blurred identification, and better plots do not fix a bad measure. Invest where it is weakest — here, **frozen tolerances and predicates**, not the run count.

### 5.3 What does not decide (though it looks as if it does)

| Belief | Reality |
|---|---|
| **Novelty of the topic** | a new topic without identification is worse than an old one with it; "the first comparison" is not a result |
| **The number of runs** | runs do not buy power if the unit of inference is the run; the number of **tasks** does |
| **Sophistication of the tooling** | LangGraph or a hand-written loop does not change the strength of the conclusion; it changes whether the conclusion can be repeated and logged |
| **Volume** | 120 pages without a hypothesis hierarchy lose to 60 pages with one confirmatory hypothesis |
| **The number of hypotheses** | seven hypotheses without a multiplicity correction are seven chances at a chance result; one confirmatory plus exploratory rest is stronger |
| **Elegance of the narrative** | helps reception, not assessment; a methodologist reads §3 and the results table |

### 5.4 The one question that settles it

**"What result would convince me that I am wrong — and would I believe it?"** If the answer is "none", this is a demonstration, not a study. If it is "such a result, but I would attack it methodologically", the work is testing its method rather than its hypothesis.

Here the answer is good and two-sided: the null — code with gating equivalent to the tool surface — is a **predicted** result, not a failure, because the main hypothesis says the advantage of a protocol is largely an advantage of validation. That belongs in §1 as a **risk taken deliberately**, not hidden as a possible embarrassment. The private auxiliary question: *"could I repeat this from memory, without notes?"* If not, neither can the reviewer.

### 5.5 Scorecard, after the scope was frozen

| Dimension | State | Cheapest improvement |
|---|---|---|
| Identification (shared loop, shared engine) | **strong** | describe it in §3 as an identification device |
| Measurement validity (predicates, tolerances) | **medium — priority** | freeze them before the sweep; publish in the manifest |
| Inferential power | **deliberately limited** | MDE into §3; sub-MDE results named unresolved |
| Resistance to alternatives | **strong construction, weak description** | one paragraph in §1: three alternatives, and why the design discriminates |
| Unit of inference | **correct** (task) | one sentence on pseudo-replication, the first thing a reviewer raises |
| Claim-to-evidence fit | **to police in §5** | the prohibition list from `scope-and-character.md` §5, open while writing |
| Repeatability | **strong** | version pin, manifest, container digest (planned) |
| Importance and usefulness | **strong** | the interface-choice rule table in §5 |

**The largest gain in strength per hour:** not additional runs, but **freezing the evaluation criteria before the sweep** and **calling unresolved results unresolved**. The first buys measurement validity, the second credibility.

### 5.6 Three sentences worth remembering

**At the defence, on why this work is credible:**

> Because identification is single — one loop, one engine, two tool sets — and the evaluation criteria were frozen before measurement; and because any result below the detection threshold I call unresolved, not zero.

**On what strength does not buy:**

> A well-designed experiment that settles something irrelevant is still irrelevant — which is why the work has to end in a decision rule, not only a table of results.

**On the hierarchy:**

> The strength of a study is a product, not a sum: reinforcing the strong link does not repair the weak one.

---

## 6. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| the whole "AI–MCP–GIS primer" (one-paragraph overview, MCP in five sentences, landscape table, glossary of twelve pairs, reading order) | `ai-mcp-gis-guide.md` | every part of it already exists where it is maintained: the MCP vocabulary in `thesis/glossary-of-terms.md`, the landscape and the G1–G5 gaps in `framing/gap-and-literature.md`, the OGC API – Processes positioning in `scope-and-character.md` §3.3 and §6. A beginner's primer is not a document about the edge of scope, and a second copy of a glossary is how two glossaries disagree |
| the "what is known / what is not known" list as a separate section | `ai-mcp-gis-guide.md` | a subset of the gap table in `framing/gap-and-literature.md`, and the one gap it added (the mechanistic question) is now §4 of this document |
| the 2 × 2 factorial with a fourth arm, its 600-run and 2,400-run arithmetic, and `mcp-15-gated` as a design change | `schema-gating.md` | the live design is three conditions and 960 runs; the arithmetic described a design that does not exist. The **reasoning** survives as §4.2 — the confound is real, the missing cell is named, and the claim is narrowed accordingly |
| the six-metric table of the gated arm | `schema-gating.md` | cut to the four metrics that the live conditions can actually populate; T2V and REF survive because the N4 preconditions produce rejection events |
| "why this strengthens the MCP evaluation rather than just adding an arm" (five points) | `schema-gating.md` | a defence of an arm that is not being run; the two points that still apply are folded into §4.3 |
| the security (G5) extension — ADV-01…05 under two gating levels | `schema-gating.md` | not in the live design; the security surface is future work and is stated as such in `design/correctness.md` |
| the second copy of the QGIS justification, "§3.1 in two sentences" and "§3 six paragraphs" | `substrate-choice.md` + `environment-generalisability.md` | the same paragraph appeared in both sources and again in `scope-and-character.md` §3.3; kept once, in §3.7 |
| the R5 row's cost estimate as a plan item | `environment-generalisability.md` | 6–8 weeks is not a plan item in a six-month thesis; it survives only as the "why not" column |
| "two things to do this week" (anchor the tool list, snapshot the toolbox) | `substrate-choice.md` | week-scale to-do lists do not belong in a framing document; the two actions are recorded in `writing/plan.md` |
| the Polish glossary table and the reading order | `ai-mcp-gis-guide.md` | term pairs are maintained in `thesis/glossary-of-terms.md`, which is allowed to stay Polish; a reading list belongs in `literature/index.md` |
| "four agents" and the 50-task arithmetic wherever it survived | `schema-gating.md`, `thesis-strength.md` | the live design is one model and 80 tasks (`d-2`, `d-3`); every stale number was replaced, not carried |

Kept, because each is the only place in the repository where its claim is made: the ten non-claims and the claim ⊂ evidence rule (§1); the seven-property table, the three domain profiles, and the transfer ledger (§2); the six requirements on the substrate, the alternative-scoring table, the layer decision, the cheaper ladder R1/R2/R4, the threat table and the reviewer answers (§3); the three regimes, the orthogonality argument, the interpretation rules, the tautology trap and its metrics, and the four limits (§4); the product-not-sum argument, the four factors with their diagnostic questions, the scorecard, and the three memorable sentences (§5).

---

## 7. Five lines, and one sentence

1. **The phenomenon is general; the proof is local.** A right-typed, wrong-sensed result occurs wherever the type does not encode meaning — geoinformatics is the cleanest ground, not the exception.
2. **One substrate, deliberately.** QGIS 3.44 is the only mainstream substrate where the same operation is a declared call and generated code on one runtime; a second engine would change the research question, so portability is shown on five GRASS tasks instead of promised.
3. **The comparison has a nameable confound.** Gating is orthogonal to the protocol; the design measures enforcement depth within the tool surface and the surface against code, and does **not** measure gated code — which bounds the claim to what validation-plus-representation jointly buys.
4. **Below 14.0 pp nothing is decided.** Power is knowingly limited; an effect under the detection threshold is called unresolved, and the unit of inference is the task, not the run.
5. **Strength is a product.** The weakest of identification, measurement validity, power and resistance to alternatives decides the outcome, and the cheapest improvement is to freeze the evaluation criteria before the first run.

**And in one sentence.** The thesis claims a measured, narrowly-bounded difference in artefact correctness between three ways of exposing one GIS engine to one agent, together with the failure signatures and the cost per success that come with it — and it claims nothing about other engines, other domains' effect sizes, model ranking, autonomy, or the novelty of validation itself.
