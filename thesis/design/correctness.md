---
id: design/correctness
title: "Correctness, and who is able to notice a mistake"
type: note
status: live
language: en
question: "What makes an artefact correct, and where can a wrong one be caught?"
tasks: [TASK-2, TASK-6]
sources: [correctness-what-ensures-it.md, error-does-not-end-with-exception.md, crs-error-or-wrong-parameter.md, what-i-can-claim-about-mcp-vs-codegen.md]
updated_date: '2026-11-07'
---

# Correctness, and who is able to notice a mistake

> What makes an artefact correct, and where can a wrong one be caught?
>
> Merged 2026-11-07 from `correctness-what-ensures-it.md`, `error-does-not-end-with-exception.md`, `crs-error-or-wrong-parameter.md`, `what-i-can-claim-about-mcp-vs-codegen.md`. Pruned and translated 2026-11-07; the cut log is §17. This document owns the vocabulary of correctness — the seven gates, the eight CRS error classes, the four predicates and the correction that an error need not end in a file. The claim ledger itself lives in `design/arms-and-validation.md`; the three levels **P-I / P-II / P-III**, the *honest recount* of how many classes a gate can catch, and the information-closure argument are owned there (§4.4–4.6) and are only referred to here.

---

## 0. Answer

1. **Execution correctness is not one thing but seven gates** through which an error can escape: choice of operation → names and types → **values** → ordering and preconditions → execution → **state of the output** → file contract. Any interface may intercept an error at any of them. **What decides correctness is how many gates are instrumented, not whether the interface is called MCP.**
2. **Schema validation of parameters — what people usually mean by "MCP validates parameters" — buys almost nothing in 2026.** The decoder already guarantees it: *strict tool use* modes and constrained decoding make a schema-violating call **impossible to emit**, not merely unlikely.
3. **The real error is semantic, not syntactic.** The best-measured number in the literature: a parameter error that **passes schema validation** (right type, right value in form, wrong in content) leads to a wrong answer with probability ≈ **0.62**, and this is independent of the model (13 models, `AgentProp-Bench`).
4. **What provides correctness is the pair nobody has measured:** **precondition guards** (the input has a CRS, units are declared, the layer is not empty) and **postcondition guards** (the server checks the result before returning success, preferring an error to a silently wrong file). The one place where a server can do **structurally** what code cannot: in the code arm the model writes the assertions, every time afresh, and nobody tests them.
5. **The gap is exact and closing it is cheap:** nobody has estimated the **causal** contribution of enforcement depth to task correctness on one surface. Taxonomies and correlations exist; the same nine operations at N1 against N4 does not. That contrast is in the design (`d-1`, `d-2`) and is the strongest contribution available.

---

## 1. Correctness as seven gates

Rather than say "correctness", decompose the path of an error. Each gate is a place where the interface **may** intercept one before it becomes an artefact:

| # | Gate | Typical error | Who can catch it |
|---|---|---|---|
| **B1** | choice of operation | the agent does something other than what is needed | only the oracle (after the fact) |
| **B2** | parameter names and types | wrong field name, incompatible type | **the decoder** (strict tool use) / the schema |
| **B3** | **parameter values** | 2180 vs 2177, "250" metres vs feet, wrong attribute | **domain validation only** |
| **B4** | ordering and preconditions | buffer before reprojection, no CRS in the input | **precondition guards** |
| **B5** | execution | library exception, out of memory | the runtime |
| **B6** | **state of the output** | a file formally valid and **spatially false** | **postcondition guards only** |
| **B7** | file contract | no file, wrong path, partial write | the artefact validator |

The sentence that follows, and that is this work's thesis in one line: **an interface is not better because it is a protocol, but because it lets the programmer write gates B3–B4 and B6–B7 once and have them enforced on every run.** In the code arm those gates are written by the model — ad hoc, untested, anew at each iteration.

Two remarks keep the table honest. **B1 is not a gate** in this sense: nothing inside the surface can know that the task asked for a clip rather than an intersection, which is why that error is visible only to the oracle and counted as a task failure rather than a caught error. And **B5 flatters the code arm**: an exception is loud, and loud failures are the ones that get repaired, so counting only exceptions as failures is the classic way to inflate a score — which the run record is designed to prevent (`framing/what-we-study.md` §11).

The gates are what the *detected-by* field enumerates — *gate, oracle, nowhere, unknown* — because "the oracle caught it afterwards" and "the server refused" are different quantities, and collapsing them makes the H2 contrast unmeasurable (`design/arms-and-validation.md` §5.3).

---

## 2. What the literature settles (five findings)

1. **Structural validation is solved and has stopped being an advantage.** *Strict tool use* modes and constrained decoding (OpenAI, Anthropic, vLLM/SGLang, Outlines/XGrammar/llguidance) guarantee that arguments **always** match the schema, at the price of token masking. The 2026 engineering consensus is that *"structural correctness is not semantic correctness"* and that the guarantee **moves failure from visible to invisible**. Practitioners report a benchmark on which constrained generation did **worse** than free generation with parsing afterwards (91.4 % vs 93.6 %) — a blog number, but in the same direction.
2. **Parameter errors dominate tool-choice errors.** Academic taxonomies (EMNLP 2025 Findings, *failed parameter filling in tool agents*) split them into five classes: missing information, superfluous information, **name hallucination**, deviation from the task, non-compliance with the specification. The authors conclude that **name hallucination comes from model limitations** while the other classes come from input sources — an under-specified question, poor documentation, a non-standard return format.
3. **A schema-valid, semantically wrong error propagates with probability ≈ 0.62.** `AgentProp-Bench` injects a *semantically wrong but schema-valid* parameter value before the first call and measures how often it ends in a wrong answer: **0.62 across 13 models**, with the **ability to reject** and the **ability to repair** **statistically independent** (ρ = 0.041). The only number in the literature saying how much survives schema validation.
4. **Silent, persistent errors are the worst class.** `ToolMaze` decomposes tool failures as explicit/hidden × transient/persistent: under **hidden and persistent** failures plan recovery falls **below 20 %** while the loop rate exceeds **70 %** — "structurally valid but semantically incorrect results severely disrupt planning".
5. **The quality of the error message is a separate mechanism.** The EMNLP authors state that *insufficient feedback from a tool failure prevents the model from correcting effectively* and recommend standardising the return format; practice adds **a structured error object (code + details + hint) instead of a raise**. Since rejection and repair are independent (finding 3), a better message improves **only one** — hence *caught* and *repaired* are separate fields.

---

## 3. The inversion: the argument that loses

**If the main criterion is correctness, then "MCP validates parameters" is a weak argument, and the literature confirms it.** In 2026 schema validation is free and universal (the decoder does it), so it does not differentiate interfaces. What differentiates them is **domain validation and state guards** — and of those **nobody has measured** the causal contribution.

That reverses how the work is worth justifying: not "tools have schemas, therefore they are safer", but **"a server can enforce spatial conditions that no decoder will check, and do it on every run rather than only when the model happens to write an assertion"**.

The inversion has a cost worth stating plainly: the strongest remaining argument is about **P-II**, and P-II is *not* checking a parameter value — it checks **properties of the result against the data**, which makes the argument depend on the server having the result and on the data carrying enough metadata to check against. In a domain without registries and metadata conventions there would be nothing to fill a P-II gate with; that GIS has them belongs in the argument, not in a footnote (`design/arms-and-validation.md` §4.2).

---

## 4. The gap, as one item with four parts

`framing/gap-and-literature.md` carries the gap register G1–G5; the validation gap *is* **G2** (enforcement depth). Its four unclosed parts:

| # | Part | What exists | What is missing |
|---|---|---|---|
| **V1** | **the causal contribution of enforcement depth** | error taxonomies (EMNLP 2025, `AgentAtlas`, `AgentPlanningBench`), correlations and error injection (`AgentProp-Bench`) | **the ablation: the same surface at N1 against N4** — nobody has estimated how much correctness each level buys |
| **V2** | **postcondition validation in GIS** | the artefact oracle as **evaluation** (GISAgentBench), parameter accuracy (GABench), eight checks per call (GNA) | **gates**: no GIS server checks the result before returning success, and nobody has measured whether converting "silent error → explicit error + repair" raises correctness |
| **V3** | **domain validation in GIS** | the EPSG registry, geometry types, NoData policies, CRS units — all checkable **before** execution | a measurement of whether these checks catch the errors of finding 3 (the 62 %) |
| **V4** | **validation ↔ repair as a mediator** | repair counters in benchmarks (TEM in GABench, "Recover" in `AgentAtlas`) | the decomposition: how much of the gain from validation is *fewer errors* and how much is *better repair* |

**Why this is attractive:** V1–V4 are the **only area in which MCP has a structural advantage over code** — gates written once, enforced always — and the literature has not touched it because every existing MCP benchmark measures **tool choice**, not **guarantees**. V1 is contracted, not merely wanted: it is the N1 → N4 contrast of H2 with its falsifier. V2 and V3 are by-products of the same 960 rows, and V4 is mediation, worth running only if H2 shows a gain.

---

## 5. The enforcement ladder inside one surface

Depth is one dimension and the levels are cumulative. Each row gives the level, what it checks, the gate it closes and the predicted contribution:

| Level | What it checks | Closes gate | Predicted contribution |
|---|---|---|---|
| **L0** | nothing (free parameters) | — | the baseline |
| **L1 / N1** | JSON Schema: types, enums, required fields | B2 | **≈ 0 in 2026** — the decoder already guarantees it |
| **L2** | **domain constraints**: the EPSG code exists in the registry, distance > 0, geometry type compatible with the operation, units declared | B3 | small to medium, but **cheap** |
| **L3** | **state preconditions**: the input has a CRS, the layer is not empty, the field exists, the extent is plausible, NoData is declared | B4 | **medium — and here the difference between interfaces begins** |
| **L4 / N4** | **postconditions**: output CRS as requested, units verified, extent not degenerate, feature count as expected → **the server returns an error instead of success** | B6 | **the largest**, because it addresses the class with propagation probability 0.62 |
| **(L5)** | the artefact contract: the file exists, the schema matches, the write is atomic, the input hash is unchanged | B7 | medium; mainly eliminates "lucky hits" |

Two design decisions must not be quietly reopened. **L5 is not a separate surface**: the contract-bound surface proposed earlier *is* the extended catalogue condition N4, and it entered the design rather than the future-work list (`design/arms-and-validation.md` §4.4). And **only N1 and N4 are arms** — the intermediate levels are *predictions about the shape of the curve*, not cells: with 80 tasks and r = 4 the MDE is 14.0 pp at τ = 10 (`analysis/statistics.md` §5), so intermediate cells would be underpowered for anything but a sign.

**The prediction, written down before measuring:** the curve of correctness against enforcement depth is **flat from L0 to L1**, **slightly rising through L2–L3**, and **steepest from N1 to N4**. If so, the result is stronger than "MCP vs code": it is **an indication of where to invest in a server** — the advice anyone building a GIS MCP server today is looking for. If the curve is flat *and* the catch rate flat, the gates were inert, which is outcome **W2** and is reported as such.

One asymmetry bounds the whole claim: **the deepest available level still cannot catch an intent error.** N4 compares the result with the *contract as stated*, so it catches what P-III makes explicit — "write in EPSG:2180", "5 km" — and not a wrong-but-legal code chosen when the request carried no expectation. The ladder buys P-II, and P-III only insofar as the card states the requirement in machine-checkable form (§8, §9).

---

## 6. The asymmetry that has to be named

> **In the MCP arm the gates are written once by the programmer; in the code arm the assertions are written by the model, each time afresh, and nobody tests them.**

That is the mechanism of reliability and at once the source of **determinism**: the server executes the same tested code on every run, while the code arm reinvents the implementation at every attempt. Between-repetition variance should therefore be **smaller** in the MCP arm, which is testable without new tasks — the within-task variance of `oracle_pass` across repetitions, in both arms: D1 in the ledger. The name for this in the design is the **SPE**, defined and enumerated in `design/arms-and-validation.md` §4.2.

The mechanism states its own limit: what is standardised is **the place of enforcement, not the content of the condition**. If correctness rises only from N1 to N4, the protocol supplied the frame and the author the content — a result, not an objection, and the sentence that keeps the thesis from claiming a protocol knows what a valid polygon is.

---

## 7. Eight classes of CRS error in one tool

The case that makes the abstraction decidable. Signature: `reproject(layer ← path | handle, epsg: int) → layer`.

| # | Class | What happens | Does parameter validation catch it? | Where it can be caught |
|---|---|---|---|---|
| **E1** | **non-existent code** (99999) | the library raises | **yes** (registry / enum) | L2 — and it is free |
| **E2** | **existing code, the wrong one** (2177 instead of 2180) | the transformation succeeds, the result is in the wrong system | **NO — the code is legal** | only an **external expectation** (§9) or a design that removes the choice (§10) |
| **E3** | **the input carries a false CRS in its metadata** (declares 4326, geometry is in 2180) | the tool "processes" garbage | **NO** — the parameter was correct | L3: extent against the CRS **area of use** |
| **E4** | **no transformation at all** (the input layer is returned) | success, CRS unchanged | **NO** | L4: output CRS ≠ requested |
| **E5** | **an omitted datum shift** | the result is "almost" right, off by metres | **NO** | L4: coordinate tolerance against a reference |
| **E6** | **units after transformation** (degrees → metres) break the next step | the reprojection is fine, the buffer's "250" is 250 degrees | **NO** — the error is in the *next* parameter | L3: the CRS unit declared before the operation |
| **E7** | **georeference does not reach the artefact** — the **file** route (a file without CRS declaration) or the **memory** route (a handle or array without CRS or transform) | no declaration at all; an array carries nothing domain-specific | **NO** | L5: `crs_declared` on the file, `handle_carries_georeference` on the handle |
| **E8** | **invalid geometry after transformation** | success, invalid polygons | **NO** | L4/L5: `geom_valid` |

**The arithmetic that matters:** of eight classes, **parameter validation catches one** (E1). That is precisely the "schema validation" which is free in 2026 because the decoder guarantees it — and therefore **does not differentiate interfaces**. One of eight is a measurement of the size of the free part, not of the contribution of the protocol.

Two classes deserve a second sentence, because a reviewer will press on them. **E6 is not a CRS error in the strict sense** — the reprojection is correct and the failure lands two operations later — so the record classifies it by the operation at which the failing artefact appears, not the one that produced the suspicious value. And **E4 is what makes the naive postcondition look sufficient**: "output CRS = requested CRS" does catch E4, and someone with only E4 in mind concludes that a postcondition solves the problem (§8 shows why it does not).

---

## 8. Why "the output has the requested CRS" is not enough

This is the most common misunderstanding and the example defuses it in three lines:

```
reproject(layer, epsg=2177)   →   layer in 2177
postcondition: layer.crs == epsg   →   ✓ CONSISTENT
```

The postcondition compares the result with **the request**, not with **the intention**. If the model supplied the wrong code, the tool did exactly what it was asked — and has no way of knowing otherwise. **Internal consistency is not correctness.** The postcondition catches E4, E7 and E8, because there the request and the intention agree and the result departs from the request; **E2 passes through every such gate untouched.**

That is the class the literature measures as "schema-valid, semantically wrong", with a propagation probability of ≈ 0.62 (`AgentProp-Bench`). A wrong but existing EPSG code is its textbook example, and it is the reason the thesis cannot rest on postconditions alone.

The same argument applies to the whole family of results that are "reproducible" — the same wrong answer, twice, with identical provenance. Determinism without a second source of expectation gives you a reliable instrument for producing a wrong map, and that is precisely the failure mode `design/tool-surface.md` calls a *pipeline that is auditable and wrong*.

---

## 9. Where the expectation comes from — and the rule that protects the experiment

An expectation can come from **four** places. Each has a different price and different methodological consequences:

| Source | Example | Who sees it | Role |
|---|---|---|---|
| **task contract** (explicit in the prompt) | "write in **EPSG:2180**" — as in card A-01 | **agent and gate** | **correct** — the agent has the information, the server may enforce it |
| **task contract** (hidden in the oracle) | `crs_equal("EPSG:2180")` in `oracle.yml` | **the oracle only** | a **measurement gate**, never a server guard |
| **the data** | the layer extent inside the CRS area of use (EPSG carries this metadata) | the agent, if the tool returns it | an L3 guard — catches E3 without knowing the intention |
| **a registry or a name** | "PUWG 1992" → 2180, resolved on the server | the agent | an L2 guard — **turns E2 into E1** |

**The rule without which the experiment breaks — information closure:**

> **The information available to a server gate must be a subset of the information available to the agent.**
> `guard_information ⊆ agent_information`

If the server compares the result with a **hidden** oracle expectation, the agent gets the answer for free and what is measured is oracle leakage, not the interface. So **a hidden expectation may be a measurement gate only, never a server guard**; a guard may use the request, the data and public registries, and nothing else (the argument is in `design/arms-and-validation.md` §4.6).

The cost is visible and should be stated: the rule forbids the strongest possible server — one that knows the answer key — and caps N4 at the share of failures that the request plus the data make checkable. That cap *is* the expressible share, the moderator of H3; closure is what makes the moderator measurable rather than a confession after the fact.

---

## 10. Three moves that turn a semantic error into a syntactic one

The practical answer to the objection "if a bad code cannot be *checked*, then nothing can be done": **take away the freedom to choose it.**

| Move | What it looks like | What happens to E2 |
|---|---|---|
| **1. Enum instead of a number** | `target: enum["EPSG:2180","EPSG:2177","EPSG:4326",…]` (the 20 systems in the corpus) | the free `int` disappears → **the wrong code becomes impossible to emit** |
| **2. Name resolution** | `target: "PUWG 1992"` → the server returns `2180` | the model does not choose a code, it copies a **name from the prompt** → the error shifts to name recognition, which is explicit in the text |
| **3. Echo and confirmation** | the result contains `{"resolved": "EPSG:2180", "name": "PUWG 1992/19", "extent": [...], "area_of_use": "Poland"}` | the agent **sees** what was chosen and can compare it with the prompt **before** exporting |

This is a stronger version of standardisation than validation: not "check the value" but **"design the parameter so that the error is impossible or immediately visible"**. And it is testable: the same surface, the variant `epsg: int` against the variant `target: enum`, the same task text — the difference in the share of E2 is a direct measurement of the value of interface design.

**Two boundary conditions, because the argument could overreach here.** An enum of twenty systems is **a different surface** from `int`, so the comparison is of two interfaces, not two models, and must be named as such. And the third move does not prevent the error — it *exposes* it, and exposure helps only an agent that looks: in the code arm the echo is a printed statement the model may or may not read. The measured quantity is therefore not "does the echo prevent E2" but "does the share of E2 reaching the artefact fall", which is why the class profile is reported per arm.

---

## 11. Four predicates instead of one

One `crs_equal` is not enough, because five different classes live inside it. Split it:

| Predicate | Catches | Kind |
|---|---|---|
| **P1** `crs_equal(expected)` | **E2**, **E4** | intention: the output in the system the contract names |
| **P2** `crs_declared` | **E7** | metadata written into the file or carried by the handle |
| **P3** `coords_within_tolerance(reference, tol)` or `extent_iou ≥ 0.95` | **E3**, **E5** | geometry actually recomputed |
| **P4** `area_of_use_consistent` (extent inside the CRS area of use) | **E3** | consistency of data with metadata — **checkable before execution** |

**The working definition for chapter 3:** *a CRS error is a discrepancy between the CRS of the artefact and the CRS the task contract requires, on a call that returned success* (P1) — and **state errors** (P3, P4) are reported separately, because they are not parameter errors and have a different place of detection. That separation is what distinguishes this taxonomy from "a wrong parameter".

One consequence for the analysis, stated before any data arrive: **compare classes, not sums.** "CRS errors fell by X pp" is weaker than "E2 fell from a to b while E1 was unchanged", because the second shows **which move worked** — with three arms and one model, the per-class profile is the only place the mechanism is visible. It is also why the taxonomy is frozen in the pre-registration: a class defined after the data is a class chosen to fit an outcome.

---

## 12. In memory is quieter than in a file

An earlier formulation of this document said that in geoinformation an error ends in a file. The objection that follows from raster practice is right about the wording and wrong about the phenomenon: a raster can live in a numpy array, be reclassified in memory and never written. "File" was shorthand, and **an in-memory array makes the error quieter, not louder**.

| Carrier | What it carries about georeference | What can be checked without extra information |
|---|---|---|
| **GeoTIFF** | reference system, affine transform, NoData, cell type | whether the file has a system; whether the extent is plausible; the resolution |
| **numpy array** | **shape and element type** | **nothing domain-specific** — `float32 (1000, 1000)` is a valid array whether the cell is 5 metres or 5 kilometres |

Which reverses the intuition: **converting to memory removes the one place where the check could have stood.** In a file the system is written down and can be compared; in an array it has to be remembered alongside — the kind of knowledge the code-arm model holds nowhere but its own context.

**Three routes lose georeference and one loses meaning:** `.values` / `ReadAsArray()`, which pulls the numbers out of a layer whose system and transform stay behind in the object; writing an array without a transform, producing a file that "exists", looks right and is displaced; recomputing resolution or axes in memory, by axis order or a `reshape` without an updated transform. And meaning goes without georeference going when NoData is masked to zero (`nan → 0`) or `float32` is cast to `int`: the system is intact and the content no longer means the same thing.

**This is the same class as E7 in the taxonomy, with two routes:**

| Route | Description | Predicate |
|---|---|---|
| **E7a — file** | a file written without a declaration of its system | `crs_declared` on the file |
| **E7b — memory** | a handle or an array without accompanying georeference | `handle_carries_georeference` on the handle |

The number of classes does not change (eight); what changes is the **number of routes**, and that the predicate must work on a handle and not only on a file.

**What this changes in the oracle:** it must accept **two kinds of object**, a file on disk *and* a handle returned by a tool; the output contract must **require an export**, since otherwise the code arm may never write the result and the oracle has nothing to evaluate — the export is part of the task, and itself a place where georeference is lost; a **new predicate** `handle_carries_georeference` is needed, requiring the handle to carry system, transform and NoData, or the operation to declare that it does not; and where the task speaks of an area or a count, the artefact must have the matching type, because a cast destroys content without changing the system.

**And in the tool surface** — the gain from the objection. The run record uses handles as intermediate results, so **a handle must carry georeference in the structured content**:

```json
{"resultType": "complete", "isError": false,
 "structuredContent": {"handle": "r1", "crs": "EPSG:2180",
                       "transform": [10.0, 0, 500000, 0, -10.0, 600000],
                       "nodata": -9999, "dtype": "float32",
                       "shape": [1200, 1500]}}
```

A server that does not return this **invalidates its own enforcement layer**: the next operations have nothing to check against. A design rule following from P-II, not from the protocol.

**A test follows:** the raster card "reclassify and compute the area of each class", executed entirely in memory with the export only at the end, tests whether the surface carries georeference through a chain of handles — the one thing a code arm cannot be forced to do, having no surface to carry it.

**The effect on the thesis is a sharpening.** "An error ends in a file" suggested the silence could be caught on the way out; the truth is stronger — **the silence arises in the value**, and in memory there are not even metadata for a check to rest on, so correctness conditions must be **attached to the operation**, not to the artefact.

**The formulation to use instead, in the draft's §1.2 and §10 of the summary:** *in geoinformation a wrong result is a value of the right type and shape — a valid array, a valid geometry, a valid number; the contradiction is not in the value but between the value and its meaning* — and where a valid layer with a correctly declared system and incorrect content is produced, *if the result stays in memory even that declaration disappears*.

---

## 13. What may be claimed on one server and one model

The question that follows from "parameter validation catches one class in eight": *may anything at all be claimed about MCP against code generation?* Yes — three things, and one thing may not be said.

**First, the correction to the arithmetic.** The 1-in-8 figure was computed for a **bare** tool, not for MCP. A bare tool with a schema catches E1. A **bound** server catches 7 of 8. A server **without** a contract catches **3 fully (E3, E7, E8) and one partly (E4)** — the honest recount is in `design/arms-and-validation.md` §4.5, and the earlier "7 of 8" silently assumed a server that knows the task. So 1-in-8 measures the size of the free part, and 3–4-in-8 measures what the protocol's own layer delivers without a contract.

Under the closure rule of §9 only the bound figure belongs to N4 as designed: the contract is in the card, so the server may use it.

**Second, what may be said**, in the ledger's own labels rather than a new numbering. **H1**: exposure changes correctness by δ (CI) in this task class, for this model and surface — the paired contrast over 80 tasks with the MDE fixed in advance, and **always conditional** on model, data and surface. **H3**: the difference **is not spread evenly** — it concentrates in the classes a server gate can intercept **before** the artefact is written, and the arms are indistinguishable where the information is unavailable; this needs the **taxonomy frozen before measurement**, and its moderator is the expressible share. **D2**: the failure signature differs — the surviving classes are not the same and are more repeatable across repetitions in the tool arm, with κ < 0.6 on the coding invalidating the measure and being reported as invalidation. **S4 / S4b**: in code generation the model checks spatial conditions in **q** % of runs, and the share of *domain* checks among those is **q_b** — descriptive and **independent of the main result**.

**Third, the claim that may not be made:** "MCP is better than code generation as a way of integrating" — one server, one model, one task class.

S4/S4b deserve separate mention as the insurance policy against a null: if the model writes a guard in 5 % of runs, that fact alone justifies a layer that does it always, whatever the TSR difference turns out to be. A thesis resting only on H1 is hostage to a result; one that also carries S4/S4b, D1 and D2 is not.

**Four substitutions keep the wording honest:** "MCP validates parameters, therefore it is better" → **"a server can enforce gates nobody in code is there to write every time"**; "MCP is better than codegen" → **"on this surface and this model δ = …, concentrated in classes X, Y, Z"**; "inconclusive, so no difference" → **"inconclusive at MDE = X pp for N = 80"**; "our server represents MCP" → **"the measurement concerns a surface with a declared depth, version and catalogue"**.

---

## 14. The mechanistic model, and what the pilot decides

```
ΔTSR ≈ base_error × catchable_share × gate_effectiveness
```

Three factors, each measurable on its own: **base_error**, the code arm's TSR from the pilot; **catchable_share**, the share of failures in classes for which a gate *can* exist given the available information, from the E1–E8 taxonomy on the same runs; **gate_effectiveness**, the share of those errors a gate converts into an explicit one, from the N1 → N4 contrast. The full dose model, with the `1[expressible]` indicator and the repair term, is owned by `design/arms-and-validation.md` §3.4; this is its three-factor reading, and the two must not diverge.

**Why it beats one difference of means:** it is a **refutable prediction**. A large Δ with a small catchable share refutes it; a Δ rising exactly where the gates rise confirms it. That is what survives "it is only one server".

**What the pilot decides, in four branches.** A high catchable share with Δ well above the MDE: the design stands, the main claim is H1 plus H3. A middling share with Δ near the MDE: narrow the corpus to catchable classes — **written down before the run series** — or raise N (`analysis/statistics.md` §5). A small share with Δ below the MDE: **the main claim changes**, from "MCP improves correctness" to "MCP changes the **structure** of failure — catch rate, repeatability of the error class, auditability — not its level". A large Δ with a small catchable share: the mechanism fails and another must be sought, such as fewer turns meaning fewer opportunities for error.

**No branch ends in "the work failed".** Risk lives in the **content** of the claim, not in its existence — the sense in which the aim is null-proof (`framing/aim-and-contributions.md` §3), with W1–W6 as the vocabulary in which the branches are reported.

## 15. Citation hygiene, and three things not to claim

**Cite (verify the identifiers before pasting):**

- `AgentProp-Bench`, arXiv **2604.16706** — injection of semantically wrong, schema-valid parameter values; **p ≈ 0.62**; independence of rejection and repair (ρ = 0.041).
- `ToolMaze`, arXiv **2606.05806** — the 2 × 2 failure taxonomy; hidden persistent: recovery < 20 %, loops > 70 %.
- EMNLP 2025 Findings, *A Comprehensive Analysis of Failed Parameter Filling in Tool Agents* (`aclanthology.org/2025.findings-emnlp.907`) — five classes of parameter error; the conclusion about insufficient feedback.
- `AgentPlanningBench`, arXiv **2606.04874** — the E1–E6 taxonomy, including E5 "tool use error" as a parameter error.
- `AgentAtlas`, arXiv **2605.20530** — the decision taxonomy (Act/Ask/Refuse/Stop/Confirm/Recover) and the coverage audit of 15 benchmarks.
- BFCL — AST evaluation, i.e. "does the call parse into the expected signature" (the structural layer, not the semantic one).

**Do not cite as evidence:** blogs about constrained decoding (the 91.4 % vs 93.6 % and "60–75 % of errors are parameters" come from practitioners — they may be given as an *observation of practice*, not as literature), vendors and aggregators.

**Three things not to claim:** that schema validation makes MCP better (false in 2026); that guards guarantee correctness (they guarantee **detectability**, not correctness); that the result transfers to other servers (see `design/corpus.md` §11 on the surface being the unit of the claim).

---

## 16. Five lines a chapter can lift

1. **Execution correctness is not one property but seven gates**, and what an interface buys is the number of gates it instruments, not its name.
2. **Schema validation is free in 2026** — the decoder guarantees it — and catches **one** of the eight CRS error classes, so it differentiates no interface.
3. **A schema-valid, semantically wrong value propagates to a wrong result with probability ≈ 0.62**, and no postcondition comparing result with request can catch it.
4. **What remains is enforcement depth**: preconditions on the state and postconditions on the result, written once by the programmer instead of once per run by the model — the contrast N1 → N4 on one surface, and the causal estimate the literature does not have.
5. **Enforcement is bounded by information**: `guard_information ⊆ agent_information`, the ladder buys P-II and P-III only where the card states the requirement, and correctness conditions therefore attach to the operation — because in memory there is not even a file to be quietly wrong in.

**In one sentence.** Correctness is not provided by a protocol or by schema validation but by gates on parameter values, preconditions and the state of the output, written once by the programmer and enforced on every run — and the literature has exactly one number about how much survives schema validation (0.62) and no measurement of what each further gate buys, which is the place where this work can contribute something nobody has.

---

## 17. What was cut, and why

| Cut | Source note | Reason |
|---|---|---|
| the four-arm table A–D (L1 / L3 / L4 / code) with 1,280 runs and "≈ 6.7 weeks" | `correctness-what-ensures-it.md` §7 | a retired design generation. The ablation is N1 → N4 inside three arms K / N1 / N4, 80 tasks, r = 4, 960 runs (`d-1`, `d-2`) |
| the two power tables (N at r = 8 / r = 16 for seven values of Δ; the base-error × catchable-share grid) | `what-i-can-claim-about-mcp-vs-codegen.md` §4 | a retired formula and r = 8 / 16. Live: MDE 14.0 pp at τ = 10 (`analysis/statistics.md` §5); the arithmetic must not exist twice with two answers |
| the four-branch pilot tree in tabular form; the labels G1–G4 for the four validation gaps; the three claims under local labels C-a / C-b / C-c | `what-i-can-claim…` §§3, 5; `correctness-what-ensures-it.md` §4 | three second numberings — of the outcomes (now W1–W6, prose in §14), of the gap register (G1–G5 lives in `framing/gap-and-literature.md`, so these became V1–V4 under G2) and of the ledger (now H1 / H3 / D2 / S4) |
| the second "who catches what" table | `what-i-can-claim…` §1 | duplicated the E1–E8 × level matrix owned by `design/arms-and-validation.md` §4.5; the corrected figure is quoted once, in §13 |
| eleven "on defence, when someone says…" paragraphs | all four notes | three defences survive, compressed into §10, §13 and §14; the rest restated the argument |
| the L0–L5 ladder as five *conditions* | `correctness-what-ensures-it.md` §5 | L2 and L3 are not arms, L5 is absorbed into N4 (`design/arms-and-validation.md` §4.4); the ladder survives as the predicted curve in §5 |
| the "PCI ceiling" arithmetic and the "3 of 8 without a contract" derivation, repeated three times | `crs-error-or-wrong-parameter.md` §6, `what-i-can-claim…` §1 | one statement of each, with the owners cited |
| the three JSON examples | `error-does-not-end-with-exception.md` §4 | one kept: the rule it states — a handle carries georeference or it voids the enforcement layer — is the whole point of §12 |

**Added while pruning**, because the cut had removed the only home of the claim: the four-valued *detected-by* note (§1), the boundary conditions on the three moves (§10), the honest recount set against the closure rule (§13), and the remark that the deepest level cannot catch intent (§5).

**Kept, each being the only place in the repository where its claim is made:** §§1–15, in particular B1–B7 and the one-line thesis, the five numbered findings, V1–V4, the predicted depth curve, the eight classes with the 1-in-8 arithmetic, why a postcondition cannot catch E2, information closure, enum / name / echo, the four predicates and the working definition of a CRS error, the E7a/E7b correction with the handle contract, the three claims with the four substitutions, the mechanistic model and its branches, and the citation prohibitions.
