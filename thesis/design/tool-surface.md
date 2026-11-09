---
id: design/tool-surface
title: "The tool surface: size, meta-tools, servers"
type: note
status: live
language: en
question: "How many tools, of what kind, on how many servers?"
tasks: [TASK-5, TASK-15]
sources: [tool-surface-design.md, meta-tools-without-code.md, two-mcp-servers-what-it-tests.md]
updated_date: '2026-11-07'
---

# The tool surface: size, meta-tools, servers

> How many tools, of what kind, on how many servers?
>
> Merged 2026-11-07 from `tool-surface-design.md`, `meta-tools-without-code.md`, `two-mcp-servers-what-it-tests.md`. Pruned and translated 2026-11-07; the cut log is §15. This document owns the **specification of the surface**: the nine operations, how the catalogue is defined and frozen, what the server may return, what it must never contain, and the two surface questions the design deliberately does not turn into conditions. The enforcement levels N1 and N4 are `design/arms-and-validation.md` §4.4; the gates those levels close are `design/correctness.md` §1.

---

## 0. Answer

**The surface is fixed, not varied.** All three conditions run against **the same nine named operations, described in the same words**, on the same QGIS engine behind the same container. What differs between N1 and N4 is what the server **checks**, and what differs between K and the catalogue conditions is whether the action channel is a **call with a schema** or **generated code**. That is the whole design, and it is why the surface is not a factor: an experiment that varies both the interface and the number of tools measures a bundle and can attribute the difference to neither part.

**The earlier version of this document proposed exactly that bundle** — a four-level size ladder (5 / 15 / 30 / 50 tools), an optional two-meta-tool arm, and a two-server topology arm. All three are retired, and §2 says what they would have bought and what they would have cost. What survives from that material is not the factor but the **guard**: the catalogue's composition is frozen, justified and reported, because a catalogue chosen by the author is a *sample of one* from a space of possible catalogues, and the honest response is to publish its composition rather than to randomise it in a design that cannot afford more cells.

**The two questions the title asks are answered as bounds, not as findings.** "How many tools" is answered by *nine, and the number is a constant*; "how many servers" by *one, because the second topology that would make the question interesting does not exist yet as a standard binding*. Both answers are limitations with a named cost, and both are cheaper to defend than a factor that cannot be powered.

---

## 1. The nine operations

The catalogue is the operation set of traditional geoprocessing, cut at a granularity a task card can name:

| # | Operation | Family | What it consumes and returns | What it does **not** express |
|---|---|---|---|---|
| 1 | `describe_layer` | P | a path or handle → CRS, extent, geometry type, feature count, attributes | anything about what the task wants |
| 2 | `reproject` | P | layer + target CRS → layer in that CRS | a datum-shift policy, unless declared as a parameter |
| 3 | `clip` | P | layer + mask layer → subset | a selection expression that needs a query language |
| 4 | `buffer` | A | layer + distance + unit → polygon layer | a variable buffer width from an attribute, unless declared |
| 5 | `intersect` | A | two layers → geometric intersection with attribute carry-over | overlay rule variations (identity, symmetric difference) |
| 6 | `union` | A | two layers → combined coverage with provenance attributes | topology repair policy |
| 7 | `spatial_join` | A | two layers + predicate → layer with joined attributes | arbitrary SQL predicates |
| 8 | `zonal_statistics` | A | raster + zones + statistic → table | weighted or custom statistics beyond the declared list |
| 9 | `export` | P | layer or handle + path + format → file | symbology, classification, layout |

Two properties of this list are load-bearing and both are design decisions rather than accidents.

**All nine are atomic.** No operation composes two others, and none takes a script or an expression language. The temptation to add a convenience tool — `reproject_then_buffer`, or a `buffer` that takes a list of distances — is exactly the temptation to smuggle the code arm's advantage into the catalogue arm, because composition is what the code arm is *for*. A catalogue whose tools compose internally is a code generator with a small vocabulary, and the comparison would then be between two ways of writing code rather than between a call and a generation.

**The ninth operation is an export, and it is not a formality.** The oracle reads a file or a handle (`design/correctness.md` §12), the code arm may never write anything if the task does not require it, and the export is itself a place where georeference is lost. Making the export an explicit operation makes it visible, countable and checkable.

---


### 1.1 The same task at the three conditions

One card — *"reproject to EPSG:2180 and buffer the communes by 5 km, then export"* — written in each condition, because this is where a reader sees that the manipulation is the action channel and nothing else.

| | The run looks like |
|---|---|
| **K** (code) | the model writes a script: read the GPKG, `to_crs(2180)`, `buffer(5000)`, write out — with whatever checks it decides to write, or none |
| **N1** (catalogue, basic) | three calls — `reproject(layer, target="EPSG:2180")`, `buffer(layer, distance=5000, unit="m")`, `export(handle, path="out.gpkg")` — each validated against its schema, nothing checked about the result |
| **N4** (catalogue, extended) | the same three calls with the same arguments; the server additionally refuses to return a layer whose CRS is not the requested one, whose extent falls outside the declared mask, or whose geometry is invalid, and returns a structured error naming the check |

The three calls in N4 are **character-identical** to the three in N1 apart from the values the model chose. That is the point of freezing the catalogue: if the N4 signature carried a `target_crs` the N1 signature lacked, the comparison would be between two interfaces, not between two depths of one interface — and the reader could not tell which difference produced which effect.

### 1.2 Near misses, enumerated per card

The near-miss property is what makes a card interesting (does the surface *confuse* or does it merely *fail*?), and it is decided at design time, never from the agent's behaviour:

| Card | Near-miss operation | Why it is a near miss |
|---|---|---|
| A-01 buffer + clip | `union` for `clip` | both reduce to a combined coverage; a union satisfies the extent predicate and violates the attribute predicate |
| A-04 spatial join | `intersect` for `spatial_join` | the geometry is right and the attributes are not carried |
| P-02 reproject | `reproject` with the neighbouring zone (2177 instead of 2180) | a legal call, a valid file, a wrong place |
| A-07 zonal statistics | `zonal_statistics` with the mean where the task says the sum | right table, wrong column |

Each card carries its near-miss operations as a list, and three metrics follow from it without any extra runs: the share of cards with at least one near miss, the mean number of near-miss candidates per card, and — from the record — the share of calls that chose the near miss. That last number is the operational form of the "density of close relatives" insight of §2, kept as a measurement because the factor it belonged to is gone.

## 2. Why the surface is not a variable

The retired proposal, stated so that it is recognisable if it comes back: a size ladder with geometric spacing —

```
L1 =  5 tools   minimal      L2 = 15 tools   moderate
L3 = 30 tools   the knee     L4 = 50 tools   "a GIS workstation"
M1 =  2 tools   meta-surface: search + run_processing_algorithm(id, params)      ← separate arm
```

— with a second ladder of *fixed core plus distractors*, an optional arm of K random catalogues from a frozen pool of a hundred tools (5 draws × 20 tasks × 3 repetitions = +300 runs), two variants of the middle level (balanced against near-miss-heavy, +120 runs), and a logarithmic {1, 2, 4, 8, 16, 32, 64, 100} exploratory ladder at 240 runs.

**It was a defensible thesis about a different question.** "Does the size and ambiguity of a tool surface change outcomes?" is worth answering — it is the question server authors actually face — and the old text answered *why not 1–100* correctly: cost, resolution (adjacent levels differ by less than the MDE, which was then 25 pp), and the bias–variance trade of many levels at a fixed budget. The problem is that it is a **second thesis**, and it competes with the first for the same 80 tasks, the same repetitions and the same MDE.

**What the arithmetic says now.** The live design has an MDE of **14.0 pp** at τ = 10 (`analysis/statistics.md` §6). A size ladder with four levels needs a monotone trend over four correlated points; at 80 tasks and r = 4 that is affordable only if the effect is large, and the literature that motivated the ladder reports differences of a few points. So the honest statement is not "the size question is uninteresting" but **"the size question cannot be decided inside this design, and pretending otherwise would spend the corpus on curves nobody can read"**.

**What survives from the retired material, and it is not nothing:**

1. **The insight that the number of tools is not the causal variable.** Adding a tool changes three things at once — **coverage** (it makes tasks feasible, raising the ceiling rather than the difficulty), **context load** (60–120 tokens per description, a cost that grows roughly log-linearly), and **near-miss density** (semantically adjacent candidates: `buffer` against `convex hull` against `dissolve`). Ten raster tools added to a vector task cost context and confuse nobody; three near-identical vector tools confuse immediately. That is now a **confound register entry** (`analysis/statistics.md` §11.4), not an independent variable.
2. **The catalogue as a sample of one.** Choosing a catalogue means choosing one point in a combinatorial space, and the result is conditional on that choice. The three escalating answers — freeze and justify; two variants at the critical level; K random catalogues — remain the right menu, and the design takes the first and names the other two with their cost (+120 and +300 runs) in the further-work list.
3. **The near-miss operationalisation**, which is a measurement, not a condition: a near-miss tool is one whose artefact satisfies **some** predicates and fails others, determined once per task at design time, never from the agent's behaviour. It rides in the corpus as a card property (`design/corpus.md` §6).

**And the cost of the retirement, stated plainly:** the thesis cannot say anything about surface size, ambiguity or the tool-explosion problem, and it cannot answer the practitioner's real question — *how many tools should my server expose?* — except by the negative result that the depth of enforcement on a fixed surface matters or does not. That is a narrower contribution, and §7 of `framing/edge-of-scope.md` lists it among the non-claims.

---

## 3. Why one server, and which question that leaves open

The retired second arm would have compared **one server exposing nine tools** against **two servers exposing the same nine, split by family** (five preparation/IO on one, four analysis on the other), on the hypothesis that routing between two catalogues is a different cognitive task from selecting inside one.

**The mechanism is real and the design cannot carry it.** Splitting the catalogue changes at least four things at once: the schema total in context (the same), the *number of `tools/list` calls*, the routing decision, and the failure mode when the model calls a tool that lives on the other server. With three conditions already fixed at 960 runs, a fourth costs **320 runs** and would be underpowered for the interaction it exists to detect. It is named as further work with that arithmetic rather than run.

**And one of the two topologies does not exist.** What `framing/what-we-study.md` §13 calls topology **D** — the standard MCP binding in which a client discovers remote servers and composes them without the author's intervention — is **not available as of November 2026**; the practical options are still "one server you launch yourself" and "a facade that fronts several back ends". So the two-server question would have been a question about a facade, not about the protocol, which is the second reason it is not an arm.

**What is left, and it belongs in the methods chapter as a bound:** the measurement is of **a single server exposing nine operations over the traditional-geoprocessing stratum**. Not "MCP", not "a production catalogue", not "the tool-explosion problem". Server replaceability — the property that the catalogue can be swapped without touching the loop — is still claimed, because the loop talks to `tools/list` and nothing else, and it is measured as S5 in the auditability group rather than as a contrast.

---

## 4. One definition, frozen and hashed

The catalogue is defined once, as data, and the data are hashed:

| What is defined | Where it lives | Why it must be frozen |
|---|---|---|
| operation names | `catalogue/operations.yaml` | the name is the model's only handle on the operation |
| description text | same file, one paragraph per operation | description wording is the treatment in N1 and N4 — *identical words*, or the enforcement contrast is confounded |
| parameter names, types, units, enums | same file, as the JSON Schema source | the schema is the surface seen by the decoder |
| return shape | same file, per operation | handles must carry georeference (§6) |
| the enforcement additions | `catalogue/checks.yaml`, applied only in N4 | this file is the whole difference between the two catalogue conditions |
| the canonical hash | `surface_sha`, in the manifest of every run | "the same surface" is a claim that needs a digest |

**The composition rules, to be pre-registered and then left alone:** every operation in the catalogue is used by at least three cards; no two operations share a name stem; no operation's description mentions a task, a family or a corpus identifier; every parameter that has units has a `unit` parameter beside it; and every operation appears in exactly one family (P or A) with the family used only for reporting, never for behaviour.

**Two guards against the author's own bias**, both cheap, neither a condition:

- **The parity table.** A table listing, for each operation, the PyQGIS call the server executes and the equivalent code-arm snippet, with the statement that both take the same path inside the container. This is what makes A2 (*capability parity*) a mechanical check rather than a promise — the execution-parity test of `design/harness.md` §7 is its operational form: the same script through both conditions must yield an **identical artefact hash**.
- **The anonymised-catalogue control.** Descriptions stripped of domain flavour (`buffer` described as "expands a geometry by a distance" without GIS vocabulary) and run on a small subsample; if the effect survives anonymisation, it is not an artefact of the author having written friendly descriptions. This is a control on **authoring bias**, not a fourth condition, and it is reported descriptively.

---


### 4.1 One catalogue entry, complete

The whole catalogue is this, nine times, plus the checks file. Written out because the details decide what is measurable:

```yaml
- name: buffer
  family: A
  description: >
    Expand every feature of a layer by a constant distance, with the distance
    given in the declared unit. Returns a polygon layer with the input attributes.
  parameters:
    layer:    {type: handle_or_path, required: true}
    distance: {type: number, exclusive_minimum: 0, required: true}
    unit:     {type: enum, values: [m, km, ft], required: true}
    dissolve: {type: boolean, default: false}
  returns: {handle: buffer_out}
  checks:                      # applied only in N4; see catalogue/checks.yaml
    precondition:  input_crs_declared and input_geometry_valid
    domain:        distance > 0 and unit_declared
    postcondition: output_crs == input_crs and extent_grew_at_least(distance)
    terminal:      geometry_valid(output) and feature_count(output) == feature_count(input)
```

Three things in that entry are decisions rather than conventions: **`unit` is required**, because a distance without a unit is not checkable; **`exclusive_minimum: 0`** sits in the schema, so a negative distance is rejected by the decoder before any gate runs (a *free* check, and the only kind N1 gets); and **the `checks` block is separate from the signature**, so that N1 and N4 differ by one file and the diff is publishable.

## 5. Parameter design is part of the instrument

The surface does not only decide *which* operations exist; it decides how much of the model's intent can be checked at all. Three rules follow from `design/correctness.md` §§5, 10 and are non-negotiable:

1. **Units are always declared.** `buffer(layer, distance, unit)` — never `buffer(layer, distance)` with an implicit metre. A parameter with an implicit unit cannot be validated (E6) and cannot be repaired, because after the transformation the model's "250" means something the model did not intend.
2. **CRS is a name or an enum, never a free integer.** `target: "EPSG:2180"` or an enum of the corpus's twenty systems; a free `int` makes E2 (a legal but wrong code) impossible to catch by any gate (`design/correctness.md` §10). This is the single most consequential line in the catalogue: it decides whether the most common silent spatial error is catchable at all, or only exposable by an echo.
3. **No default encodes an intent.** A default CRS, a default output path, a default NoData value: each is a decision the task should have made, and a default that happens to be right makes a wrong call succeed. Where a default is unavoidable it is written in the description and reported as a floor in the limitations.

**The corollary is an asymmetry the thesis must own:** tightening the surface buys catchability at the price of expressiveness. If every CRS is an enum of twenty, a task needing the twenty-first is inexpressible — which raises the expressible share for CRS classes and lowers coverage somewhere else. The design takes the enum because the corpus's cards are drawn from those twenty systems, and states the trade in the methods rather than in a footnote.

---

## 6. What the server returns

The return shape is where the enforcement layer either has something to check or has nothing (`design/correctness.md` §12). Four rules:

**Structured content, always.** A tool result carries `resultType`, `isError`, and a `structuredContent` object. The model needs the structure for repair; the harness needs it for the record; the oracle needs the handle.

**Handles carry georeference.** A handle returned by an operation carries CRS, transform, NoData, dtype and shape — or the operation declares explicitly that it transfers none. A handle without georeference **voids the enforcement layer**, because the next operation has nothing to compare against: this is the design rule that follows from P-II, not from the protocol.

**Errors are structured objects, not raises.** A rejection returns a code, the offending parameter, the constraint violated and a hint; the model can then repair, and the record can distinguish *caught* from *repaired*. Since the ability to reject and the ability to repair are statistically independent (`design/correctness.md` §2), one field each.

**The echo names what was resolved.** When the surface resolves a name to a code, the result says so: `{"resolved": "EPSG:2180", "name": "PUWG 1992/19", "area_of_use": "Poland"}`. This is not decoration: it is the only mechanism by which an intent error (E2) becomes visible to the *agent* rather than to the oracle, and §5's enum rule plus this echo are the two ways the surface can address the class that no gate can check.

**What changes between N1 and N4 is only whether these are checked** — the shapes are identical in both conditions, so a difference in outcome cannot be a difference in what the model was shown. `catalogue/checks.yaml` adds the preconditions and postconditions; it adds no parameters and changes no descriptions.

---

## 7. What the surface must never contain

Four prohibitions, each with the confound it prevents:

| Prohibited | Why |
|---|---|
| any expected value from the oracle — an extent, a feature count, a checksum | it breaks information closure (`guard_information ⊆ agent_information`, `design/correctness.md` §9) and measures oracle leakage instead of interface |
| a task identifier, family name or card number in a description, parameter name or return field | it lets the model condition on the design |
| a tool whose only purpose is to answer the task (`solve`, `check_my_result`) | it converts the comparison into "one arm has the answer" |
| a per-task branch inside an operation | it makes the surface a lookup table and the measurement meaningless |

The third deserves a note, because it is the most tempting to add. A `validate(inputs)` tool looks like a harmless convenience and is in fact a **different experimental object**: it moves the checking out of the operation and into a separate call the model must choose to make, which is precisely the property of the code arm (the model may write an assertion, or not) that the catalogue arm is supposed to remove. Checks belong **inside** the operation, on every call, unconditionally — that is the definition of the SPE.

---

## 8. The expressible share is a property of the surface

The nine operations cannot express every requirement in the corpus, and that is the moderator of H3 rather than an embarrassment. Each card is coded once, before the sweep, into one of four values describing how much of the task's requirement the surface can carry:

| Value | Meaning | Example |
|---|---|---|
| **all** | every requirement is a parameter, a domain rule or a postcondition the surface can state | buffer 5 km in 2180, clip to communes, export |
| **most** | the surface can carry the mechanical part; one requirement lives in prose | zonal statistics where the statistic is named but the class breaks are described |
| **part** | the surface can produce the artefact but cannot check the requirement | a reprojection whose target system is given only by a historical name |
| **none** | the requirement is outside the surface's vocabulary | symbology, classification, layout — the whole of family C |

**The coding is done blind to results and frozen in the pre-registration**, because it is the moderator of an interaction and a moderator chosen after the data is a moderator chosen to fit. The expected pattern is stated in advance: the difference between conditions should grow from `none` to `all`, and a **difference on `none` cards would refute the mechanism** rather than support it — if the catalogue arm wins where the surface cannot carry the requirement, the win is not about what the surface carries (`design/arms-and-validation.md` §2, H3).

This is also why "the surface is production-scale" is not claimed. Nine operations against hundreds of real MCP tools is a **tractable surface over the traditional-geoprocessing stratum** (`framing/gap-and-literature.md` §6), and its tractability is what makes the expressible share codable at all.

---


### 8.1 How the share is coded, and by whom

The four values are assigned by one coder with the codebook below, on 100 % of the cards, **before any run**; a second coder independently codes 25 % of the cards and Cohen's κ is reported beside the moderator. Below κ = 0.6 the moderator is redone, exactly as with the failure taxonomy — a moderator whose coding is unreliable turns H3 into a hypothesis about the coder.

| Code | Test applied to the card | Tie-breaking rule |
|---|---|---|
| `all` | every requirement is expressible as a parameter, a domain constraint or a postcondition the surface can state | — |
| `most` | one requirement survives only as prose the model must act on, and no check can be written for it | if two requirements are prose, take `part` |
| `part` | the artefact is producible, but a requirement cannot be checked by anything the surface knows | — |
| `none` | a required aspect lies outside the vocabulary — symbology, classification, layout, a custom statistic | — |

The rule that keeps this from becoming a post-hoc story: **the code is assigned to the *requirement*, not to the operation.** A card that uses `zonal_statistics` and asks for class breaks described in words is `most`, not `all`, because the surface can compute the statistic and cannot know the breaks. The codebook lives in the pre-registration, and the cards ship with the code in a column.

## 9. Inside the server: allowed, forbidden, bounded

The server executes QGIS through PyQGIS and, where the operation maps onto one, through `qgis_process`. What it may and may not do is part of the instrument:

| Allowed | Forbidden |
|---|---|
| call PyQGIS / GDAL directly for the nine operations | expose a generic runner, an `eval`, or a path from parameters into Python |
| normalise geometry types and reject invalid input | "fix" a wrong parameter silently and proceed |
| convert units when the unit is declared | infer the unit from the magnitude of the number |
| refuse with a structured error | return a success with a warning field the model will not read |
| cache within a run | reach the network |

**Determinism.** The same input must give the same output, and where it cannot, the tolerance is written down rather than hoped for: PROJ and GEOS can differ in the last digits through floating-point contraction and thread order, so artefacts are compared with tolerances and never by byte equality (`analysis/statistics.md` §11.1). The exception is the parity test, where the two conditions run the *same* library call in the *same* container, so there byte equality is the right criterion — and the fact that it holds is what makes A2 mechanical.

---


### 9.1 The operational envelope

The container is part of the surface's contract, because a limit is a behaviour: one container per run, headless QGIS 3.44, image digest in the manifest, **no network**, 8 CPUs, 32 GB, a ten-minute ceiling per call and a turn budget per run. Three consequences have to be stated rather than discovered:

- **A timeout is not a wrong answer.** It is an infrastructure exclusion only if the *host* failed; if the operation itself exceeds the ceiling, it is a property of the surface and is reported as such.
- **No network means no CRS downloads.** PROJ's grid files are baked into the image, which fixes the transformation pipeline and makes the datum-shift class (E5) reproducible instead of dependent on a download.
- **Headless means no map canvas.** Any operation whose semantics depend on rendering is outside the surface by construction — which is one of the reasons family C is `none` rather than `part`.

## 10. The meta-tool question, retired with its arithmetic

The most interesting engineering choice a server author faces is not how many tools to expose but whether to expose **one generic runner** — a `search` tool plus `run_processing_algorithm(id, params)` — over the whole `qgis_process` toolbox. The retired design turned this into an arm and it was, in the old text's own words, *the cleanest ablation the project could build*: both sides would have the same operation set and the same boundary (no `eval`), leaving exactly four measurable differences — schema size in context, actions per turn, **error-message granularity**, and **notation fluency** (the model knows Python from pretraining and knows an invented DSL not at all).

**Why it is still not run.** It changes the surface *and* the error granularity *and* the notation at once; it stops being a test of the protocol and becomes a test of DSL design, which is a different thesis with its own literature. And it cannot be bolted on: an arm comparing two meta-tools against nine named tools at 320 runs would be interpreted, correctly, as a bundle.

**What any fourth condition costs, in the live arithmetic.** Each condition is 80 tasks × 4 repetitions = **320 runs**, so a fourth condition is +33 % of the series (960 → 1,280) and buys **no improvement in the MDE of the existing contrasts** — the between-task variance is unchanged and the repetitions are the same. What it buys is one more contrast, which must then either spend α from a budget of one confirmatory test and a two-test Holm family, or be reported descriptively and thus cannot carry a claim. That is the arithmetic behind every "not run" in this document: it is not that the questions are uninteresting, it is that at this N a fourth cell produces one more underpowered comparison and one fewer repetition of the four already contracted.

**What survives is the prediction and the warning.** The prediction from the literature is that a generated DSL loses against code, because pretraining mass for Python is enormous and for an invented JSON grammar zero — and that prediction is worth one paragraph in chapter 7 as an expectation the thesis does not test. The warning is sharper: if a meta-tool is ever implemented, it must be an **explicit dictionary** `{operation_name: function}` with parameter validation, because an `eval`, an `exec` or a `getattr` on an arbitrary module silently recreates the escape hatch and returns the comparison to "code against code" without anyone noticing.

---

## 11. Risks, and what each one costs

| Risk | How it would show | Mitigation, and its cost |
|---|---|---|
| **the catalogue is a straw man** — nine operations chosen to be checkable | a reviewer asks why not thirty, or why not the toolbox | freeze, justify, publish the composition and the near-miss metrics; the K-random-catalogues study named at +300 runs |
| **the descriptions are too kind** | the effect disappears under anonymisation | the anonymised-catalogue control, reported descriptively |
| **near-miss density is uncontrolled** | a card's failure is about confusion, not enforcement | near-miss tools enumerated per card at design time |
| **the enforced checks leak the answer** | the N4 arm succeeds for the wrong reason | information closure tested mechanically: no check may reference anything not in the prompt, the data or a public registry |
| **the surface drifts between conditions** | a difference appears that is not the manipulation | `surface_sha` in every manifest; N1 and N4 share the file except `checks.yaml`, and the diff is an appendix |
| **one server is taken for MCP** | "your results are about your server" | the claim is bounded in the methods and §3; server replaceability is measured as S5, not claimed as a finding |

**The one risk with no mitigation is the honest one:** with nine operations and one server, the thesis cannot say what a larger or differently composed catalogue would do. That is not a gap that can be closed inside 960 runs, and it is better named in the limitations than partially addressed with an underpowered arm.

---

## 12. Five lines, and one sentence

1. **Nine atomic operations, identical in all conditions, described in identical words** — the surface is the instrument, not the variable.
2. **No composition inside a tool, no generic runner, no expression language** — because composition is the code arm's advantage and importing it would erase the comparison.
3. **The parameters decide what can be caught**: units always declared, CRS as a name or an enum, no default that encodes an intent.
4. **Handles carry georeference and errors are structured objects**, because a surface that returns opaque handles has no enforcement layer to speak of.
5. **Two questions are answered as bounds, not findings** — how many tools is a constant, how many servers is one, and both are named with their cost in the limitations.

**In one sentence.** The surface is a fixed, frozen, hashed catalogue of nine atomic geoprocessing operations with declared units and named reference systems, whose enforcement layer may check results but may never be told the answer, and whose limits — a constant size, a single server, a vocabulary that cannot express cartography — are the measurement of the expressible share rather than defects hidden from it.

---

## 13. What was cut, and why

| Cut | Source note | Reason |
|---|---|---|
| the four-level size ladder (5 / 15 / 30 / 50) with `L1 ⊂ L2 ⊂ L3 ⊂ L4` and the 50-tool "workstation" reference condition | `tool-surface-design.md` §§1–6 | a second thesis competing for the same 80 tasks and repetitions. A monotone trend over four correlated points at an MDE of 14.0 pp is unaffordable, and the size gap is retired (`framing/gap-and-literature.md`, G2 is enforcement depth) |
| the second ladder of fixed core plus distractors, the two middle-level variants (balanced against near-miss-heavy, +120 runs) | same, §5.1 | a randomisation of catalogue composition that the design answers with freeze-plus-justify; the variants are named in further work with their cost |
| the K-random-catalogues arm from a frozen pool of a hundred tools (+300 runs) | same, §5.1 | same reason; it answers "is my catalogue a straw man" by making composition a variance component, which needs more runs than the whole series |
| the logarithmic {1, 2, 4, 8, 16, 32, 64, 100} exploratory ladder at 240 runs | same, §5.2 | an exploratory study of curve shape, not a confirmatory one; the curve the design does test is depth of enforcement, not size |
| "MDE ≈ 20–25 pp", "adjacent levels differ by less than the MDE", "100 levels × 120 runs = 12 000 runs" | same, §§5.1–5.2 | retired arithmetic. Live: MDE 14.0 pp at τ = 10, 960 runs (`analysis/statistics.md` §6) |
| the meta-tool arm (`M1`: search + `run_processing_algorithm`) with its four-condition inference table and its A1/A2 granularity comparison | `meta-tools-without-code.md` §§0–8 | it changes surface, error granularity and notation together and becomes a thesis about DSL design; the prediction and the `eval` warning are kept, the arm is not run |
| the two-server arm and the four-condition matrix (single/double × basic/meta) with its inference table | `two-mcp-servers-what-it-tests.md` §§1–5 | a fourth condition at 320 runs, underpowered for the routing interaction it exists to detect; and topology D does not exist as a standard binding as of November 2026 |
| the four "sentences for the thesis" and the three "what this cannot show" lists, repeated across the two meta notes | both | the survivor is one paragraph in §10 and the bound in §12; the rest restated the same two conclusions in different vocabulary |
| the standalone "changes this forces on the artefacts" section | `tool-surface-design.md` §8 | it was a list of consequences for documents that have since been rewritten; the consequences live where they bite — in §5 (parameters), §6 (return shape) and `design/corpus.md` (near-miss coding) |

**Added while pruning**, because the cut had removed the only home of the claim: the nine operations as a table with an explicit "what it does not express" column (§1), the statement that composition inside a tool would import the code arm's advantage (§1, §3), the anonymised-catalogue control as a control rather than an arm (§4), the asymmetry between catchability and expressiveness that the enum rule creates (§5), the four prohibitions with the `validate(inputs)` case (§7), and the definite statement that a difference on `none` cards would refute H3 rather than support it (§8).

**Kept, because each is the only place in the repository where its claim is made:** the answer that the surface is fixed (§0), the nine operations and the atomicity rule (§1), the retirement of the size ladder with the surviving insight that tool count is not the causal variable and the catalogue is a sample of one (§2), the single-server bound with the missing topology D (§3), the frozen catalogue definition with `surface_sha` and the two bias guards (§4), the three parameter rules and their trade (§5), the four rules for what the server returns (§6), the prohibitions (§7), the expressible share as a surface property with its pre-registered pattern (§8), the allow/forbid table with the determinism rule (§9), the meta-tool prediction and the `eval` warning (§10), and the risk table with the one unmitigated risk named (§11).
