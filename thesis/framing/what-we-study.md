---
id: framing/what-we-study
title: "What exactly is studied"
type: note
status: live
language: en
question: "Which question is measured, which is argued, and which is out of reach?"
sources: [what-exactly-we-study.md, comparison-basis-codegen-mcp.md, mcp-rest-ogc-codegen.md, mcp-ogc-facade.md, mcp-protocol-shape.md]
updated_date: '2026-11-07'
---

# What exactly is studied

> Which question is measured, which is argued, and which is out of reach?
>
> The estimand document. §1 separates three levels of the question and says which one the experiment touches; §2–§4 fix the basis of comparison (one principle, five assumptions, four limits); §5–§6 say what is measured and what is *not* in the contrast ladder; §7–§9 are the run record, the arithmetic and one worked example; §10 lists what this basis cannot compare; §11–§13 handle the two things a reviewer will raise before the results — *why not OGC API – Processes* and *do you know what MCP actually is*.
>
> Pruned and translated 2026-11-07 (`TASK-21`): 7,413 → 6,493 words, five source notes → fifteen sections, rewritten against the live design (K · N1 · N4, 80 tasks, r = 4, 960 runs).

---

## 1. Three levels of the question, and one correction

**The correction first, because the wrong version of the sentence is the commonest way this thesis gets misread: MCP is not REST.** MCP is JSON-RPC 2.0 over `stdio` or Streamable HTTP — no resources, no HTTP verbs, no status codes. "REST" in the sentence *"I study how much of MCP is REST plus validation"* is mental shorthand for three different things:

| What intuition calls "REST" | What it really is | Where it sits in the thesis |
|---|---|---|
| "a described interface called remotely" | a catalogue of tools with **schemas** plus a structural call (`tools/call`) | the catalogue conditions |
| "a wrapper over somebody's API" | function calling over one's own API (FastAPI plus OpenAPI) | **not in the experiment** |
| "a protocol" | JSON-RPC, version negotiation, discovery | the catalogue conditions, but as a *vehicle*, not a factor |

**The second arm of the experiment is not REST. It is code generation.** A comparison of "MCP against REST as a tool wrapper" would probably come out close to zero — a good sentence for chapter 2, and not the thesis statement, because that condition does not exist and will not exist inside the run budget.

The question then splits into three levels, of which the experiment touches two:

| Level | Question | Status in the thesis |
|---|---|---|
| **P1 — transport and protocol** | does JSON-RPC plus discovery add anything over REST/OpenAPI plus function calling? | **not tested.** Chapter 2 argues it from the literature and from the architecture, and the honest conclusion is *nothing for a single call* — the difference would appear when the server is swapped and reused, which is the substitution slice R1 and not a condition |
| **P2 — representation** | does exposing operations as named, described tools change what the agent produces, against writing code on the same engine? | **the core of the experiment**: H1 |
| **P3 — the enforcement boundary** | how much of any P2 difference is the *validation* rather than the representation? | **partly measured**: H2 grades enforcement *inside* the tool surface; the comparison that would isolate it fully — gated code — is not in the design (`framing/edge-of-scope.md` §4.2) |

So the sentence *"I study how much of MCP is REST plus validation"* jumps from P1 to P3 and skips what is measured. The correct version:

> **The thesis studies how much of the difference between a described tool surface and generated code follows from the enforcement boundary rather than from the representation — on an identical engine, with the surface held constant between the two catalogue conditions.**

The difference is not cosmetic: the first version promises a comparison with REST that does not exist, and a reviewer will ask where it is.

### 1.1 "Whether it pays off" is a vector, not a number

Operationalised, the value of an interface splits into four quantities, each with its own claim and its own unit:

| Component | Measure | Claim | Note |
|---|---|---|---|
| **effectiveness** | TSR — binary artefact correctness | **H1** | the only confirmatory test; an effect below the MDE is *undecided* |
| **enforcement gain** | TSR at N1 against TSR at N4, same surface and same words | **H2** | the depth curve as a trend |
| **repeatability** | error-class repeatability (S3) and predicate-level classes across the four repetitions | **D1** | rarely reported, cheap, and robust under a null |
| **cost** | tokens, calls and seconds **per successful task** | **D3** | the ranking can invert; this is not TSR |
| **coverage** | the share of a task's requirements the surface can carry (the expressible share) | **H3** | a catalogue can be faultless and useless at once |

The practical product of the thesis is therefore a decision table rather than a verdict — and it is the answer to "does it pay off":

| Situation | Choice | What licenses it |
|---|---|---|
| repeated tasks, several clients, an audit trail required | the **catalogue** | structural call record, gates, server replaceability (D2, S5) |
| declarative cartography and style | the **code channel**, or a surface that carries the style properties | family C: the corpus records where a surface cannot express the requirement (H3) |
| one-off, unusual spatial analysis | **code** | no surface to invest in, no coverage to gain |
| token cost is the bottleneck | depends on D3 | the cost ranking may invert the TSR ranking |
| "what exactly ran" must be shown | the **catalogue** | a call record against the text of a script |

**Without that table "pays off" remains an opinion** — and the table cannot be filled in before the series.

---

## 2. The basis of comparison, in one paragraph

The comparison stands on one sentence: **the same input material, the same output contract, the same oracle — only the route by which the file is produced differs.** Prompt, input data, model, harness budget and predicates are pinned and hashed; the variable is the **action channel**: a tool call through the server, or a program written and executed in the sandbox. What is studied is therefore **the conditional probability of producing a correct artefact, given the task and given the interface** — not "a file", not "a protocol", not "a model". The file is an **instrument of observation**, not the object of study; the predicates are the **definition of correctness**, not a measure of code quality.

That is the only basis on which two different action channels can be compared: **the artefact is their only common denominator.** Every metric attached to calls or trajectories is one-sided by construction — the tool conditions have tool calls and the code condition does not.

### 2.1 Ceteris paribus, item by item

| Element | K (code) | N1 / N4 (catalogue) | How it is held |
|---|---|---|---|
| task content | identical | identical | one card file, `prompt_hash` in the register |
| input data | the same files | the same files | input hash recorded on the card |
| model, version, sampling, seed | the same | the same | recorded in the manifest |
| runtime | the same container, the same library versions | the same container | the server is a **thin wrapper over the same functions** (A2) |
| budget | 25 turns, 10 min, one token budget | identical | the same harness limits and the same stop rules |
| output contract | `out.gpkg` at the given path | identical | the same output-schema validator |
| oracle | predicates and tolerances | identical | one scorer, one `oracle.yml` per task |
| **action channel** | **program → sandbox → execution** | **tool call → server → execution** | **the only thing that differs** |
| **error channel** | interpreter traceback | server response: error code plus message, or a typed rejection | **differs — and that is the manipulation, not a flaw** |

The last two rows are not an oversight: two ways of driving an agent are being compared, and the error channel is one of the mechanisms by which one may be better. It must be **measured** (repair iterations, error class, `detected_by`), never "equalised".

---

## 3. Five equivalence assumptions, and what is measured if each breaks

This is the table the defence will go through line by line.

| # | Assumption | Content | If it breaks, what is measured instead |
|---|---|---|---|
| **A1** | **oracle validity** | the predicate set carries the intent of the task | **your predicate set**, not the quality of the solution — the commonest failure of GIS benchmarks |
| **A2** | **capability parity** | every catalogue operation has a library equivalent in the code condition; the surface is a thin wrapper, not a simplified API | **tool capability**, not the interface — the classic "code wins because it has geopandas and the server has nine functions" |
| **A3** | **information parity** | the prompt carries the same knowledge about the task; only the description of the surface differs | **prompt engineering**, not the interface |
| **A4** | **budget parity** | the same turn, time and token ceilings | **the harness ceiling** — if the limit truncates one condition, the limit is being measured |
| **A5** | **no drift** | model and surface versions do not change during the series | **drift over time** — the literature measures 13–14 pp across one server-version change |

**The practical consequence of A2** is one artefact: before comparing, prove the surface is a thin wrapper, with a **parity table** — *operation → library function → version*. Without that table the whole comparison falls to one sentence at the defence, which is why `design/experiment.md` §16 lists it as an open item before the pilot.

A3 and A4 are the two that can be broken by accident and in good faith. A3 breaks if the catalogue's descriptions happen to mention something the prompt does not; A4 breaks if 25 turns is generous for one channel and tight for the other. Neither is detectable after the fact, so both are **declared and hashed before** the first run.

---

## 4. Why the artefact and the predicates are the right basis — and its four limits

**The advantages, each following from the construction rather than from convenience:**

1. **Neutrality with respect to the interface.** The oracle does not know how the file was produced, and that is a **condition of comparability**, not merely a virtue. Call metrics, trajectory metrics and code-similarity metrics (TAO/TIO/PEA, CodeBLEU) are one-sided by definition: they exist in only one condition.
2. **Agreement with the best practice of the field.** `gisagentbench2026` established that GIS agents are scored on a ground-truth file with tolerances; the basis is therefore recognisable and reviewable rather than idiosyncratic.
3. **No judge.** No LLM-as-judge and no VLM judge, so there is no style bias and no irreproducibility — the charge levelled at several MCP benchmarks.
4. **The predicates are auditable.** They can be shown, attacked and hashed before the measurement, which cannot be done with "map quality".

**The limits, which have to be stated rather than discovered by a reviewer:**

1. **The oracle defines the construct.** If the predicates do not cover units, NoData and CRS, what is measured is "whether the file looks right". Hence the **silent spatial error needs its own predicate**; otherwise one of the most interesting differences between the interfaces is invisible.
2. **A binary outcome throws away the gradient.** `oracle_pass` is all-or-nothing. Report the **share of satisfied predicates** alongside — a continuous measure, free, because the data already exist — as secondary, never instead of the primary.
3. **No information about the process.** The file does not say whether a hit was luck. The trace (turns, calls, tokens) is therefore **recorded but not scored**; scoring it would bring the one-sided metrics back in.
4. **Lucky hits and quiet repairs.** A solution can pass every predicate while the agent did something inadmissible — overwriting an input, writing outside the output directory. So the predicate set includes an **integrity predicate**: input hashes unchanged, no writes outside the output directory. Without it, "correct" is partly a matter of luck.

---

## 5. The three layers: effect, mechanism, boundary

| Layer | Question | Estimand or measure | Where |
|---|---|---|---|
| **effect** | does the route by which the file is produced change the chance of a correct file? | difference in share of passed tasks, **paired by task**: `D_i = 1[pass_i^catalogue] − 1[pass_i^code]`, estimand `E[D]` | H1; McNemar plus a mixed model |
| **mechanism** | through what? | which predicate fails first, how many repair iterations, which error class, `detected_by`, tokens and turns; TSR at N1 against N4 | H2, D1, D2 |
| **boundary** | when does the effect disappear? | the interaction between the condition difference and the **expressible share** of the card | H3 |

The three layers correspond to the three sentences the thesis can say: **"by how much"**, **"why"**, **"until when"**. The first without the second is an anecdote; the second without the third is not transferable; the third without the first has no magnitude.

The live design says something specific about the middle layer that earlier versions could not: because N1 and N4 have **identical surfaces and identical descriptions**, the N1 → N4 contrast is a **pure enforcement** contrast. The mechanism claim therefore does not rest on comparing a curated catalogue with unbounded code — it rests on two conditions in which every word the model sees is the same.

---

## 6. The contrast ladder, honestly drawn

A bare A/B measures a **package**, not an interface: the two conditions differ in representation, in surface and in enforcement all at once. The earlier plan answered that with a four-contrast ladder (K1–K4) built around a randomised catalogue and a whitelisted code condition. **Those contrasts are not in the live design**, and the honest version of the ladder is this:

| Contrast | Conditions | What it answers | Status |
|---|---|---|---|
| **across the interface** | K against N4 | what an analyst gets when choosing a tool surface or code *as both are used today* | **in the design — H1, confirmatory** |
| **within the surface** | N1 against N4, identical surface | does enforcement itself raise correctness? | **in the design — H2, the depth curve** |
| **moderated by the task** | the difference against the expressible share | where does the surface help, and where can it not? | **in the design — H3** |
| form at equal surface | code **with a whitelisted function list** against the catalogue | is the difference the protocol and the naming, given that both conditions are bounded? | **not in the design.** Would need a static checker or a forced-API harness; it is the nearest cheap addition and it is named as further work |
| gated code | code **with pre-execution and post-execution validation** against the catalogue | how much of the effect is validation *rather than* representation? | **not in the design.** This is the missing cell that bounds the causal claim (`framing/edge-of-scope.md` §4.2) |
| catalogue curation | the hand-curated surface against a mechanically generated one | how much of any advantage is a well-chosen surface? | **partly in the design** — the anonymised-catalogue control (`design/corpus.md` §10), which is the cheap version of the same worry |

**What that means for wording.** The across-interface contrast and the within-surface contrast are both needed: the first says what happens in practice, the second says whether enforcement is behind it. If the first shows an advantage and the second does not, the honest sentence is: *"the advantage comes from the representation and the bounded action space, not from enforcement"* — which is a result, and a practically useful one. If both are flat while the catch rate differs, the result is outcome W3: gates change the structure of failure, not its level.

---

## 7. What one run leaves behind

| Group | Fields | What it is for |
|---|---|---|
| **identity** | `run_id`, `task_id`, `condition`, `model`, `model_version`, `prompt_hash`, `seed`, surface version | reproducibility; the tests of A3 and A5 |
| **outcome** | the predicate vector → `oracle_pass`, the share of satisfied predicates | the estimand, and the continuous secondary measure |
| **process** | `turns`, calls (legal and total), `gate_rejections`, `repair_iterations`, `error_class`, `detected_by`, `stop_reason` | the mechanism, A4, and the mediation report |
| **cost** | `tokens_in`, `tokens_out`, `wall_clock_s` | efficiency, and cost per success |
| **artefact** | `artefact_path`, `artefact_sha256`, the checksum of the container image | rescoring without rerunning; integrity |

Three fields make the comparison auditable, and all three are hashes: **`artefact_sha256`**, **`prompt_hash`** and the **surface version**. Without them nothing shows that both conditions received the same task, or that the file was not substituted. `result.json` is written last, and its presence is what marks a run complete (`design/experiment.md` §5). The register has **thirteen fields** and `detected_by` takes four values, because "the model wrote a check, but a language check" must be distinguishable from "the model wrote nothing".

---

## 8. How it is computed

The full argument is in `analysis/statistics.md`; four points belong here because they are properties of the *basis*, not of the analysis:

1. **The unit is the task, not the run.** The same task runs in all three conditions, so task difficulty cancels in the difference. With ICC = 0.661 and r = 4 the design effect is 3.0: 960 runs are worth about 320 independent rows, and the claim is about 80 tasks.
2. **The primary test is McNemar on the discordant pairs** of `oracle_pass`, with a mixed logistic model carrying a random task effect as the companion; for the share of satisfied predicates, a paired test or the same mixed model.
3. **The MDE is written down first: 14.0 pp at τ = 10 pp.** Anything smaller is reported as *undecided*, never as "no difference".
4. **ITT and per-protocol side by side.** ITT — all tasks, with infeasible ones counted as failures — speaks to practice; PP — only tasks feasible on this surface — speaks to the interface and the agent.

One free by-product: the same analysis estimates **ICC and τ**, i.e. how much of the variance is between tasks, and that feeds the power of every later claim.

---

## 9. One task, three conditions

Task A-07: buffer, reproject, export. Six predicates.

| | K — code | N1 — schema only | N4 — invariants and terminal conditions |
|---|---|---|---|
| prompt | identical (`prompt_hash` equal) | identical | identical |
| what happens | writes `gdf = gpd.read_file(...)`, `to_crs(2180)`, `buffer(250)`, `to_file(...)` | calls `reproject(layer, 2180)` → `buffer(layer, 250)` → `write(layer, path)` | the same three calls |
| error channel | `pyproj.exceptions.CRSError: …` | a typed rejection: `CRS mismatch: layer carries 4326, expected 2180` | the same, plus a post-execution check on the written file |
| repair iterations | 1, after the traceback | 1, after the rejection | 1 |
| predicates | `crs_equal(2180)` ✗, the rest ✓ | all ✓ after the repair | all ✓ on the first attempt |
| result | `oracle_pass = False`, share 5/6 | `oracle_pass = True` | `oracle_pass = True` |

**What is the observation:** the pair (0, 1) for K against the catalogue conditions on this task. **What is the mechanism:** the same CRS error, three different routes of detection — after the fact by the oracle, before execution by the surface, before execution plus after execution by the deeper surface. **What is the by-product:** the repair count is equal here, so on this task the surface did not help *repair*, it helped *avoid*. Distinctions of exactly this kind are what the basis is designed to produce, and they are why `detected_by` has four values rather than a boolean.

---

## 10. What this basis does not compare

An honest list, and it belongs in chapter 7:

1. **Not the protocol in general** — this protocol, this surface, this model, this stratum of tasks. A general statement would need replication on other surfaces.
2. **Not "efficiency" in a fully fair sense.** The code condition has an unbounded library, so its lower token cost may be a consequence of a larger action space rather than of a better representation. Hence cost is reported **beside** correctness, never instead of it.
3. **Nothing below 14.0 pp.**
4. **Not cartographic quality** — aesthetics and legend legibility. The predicates check the presence and agreement of elements, not their quality. That is stated outright instead of pretending a VLM judge would settle it.
5. **Nothing that is not in the predicates.** Oracle quality is assumption A1, not a finding.
6. **Not the effect of the model or the harness** — both frozen, both named as further work.

---

## 11. Why there is no third arm: MCP, OGC API – Processes, code generation

This is the question a geoinformatics committee asks first, so the answer has to be a section rather than a footnote. **The literature justifies the comparison in chapter 2 and does not justify a third arm.**

The key observation is that **for an agent, OGC API – Processes does not exist apart from one of two forms:**

| Form | What the model sees | What it collapses into |
|---|---|---|
| **(a) wrapped as tools** (as in the 52°North bridge) | the same schemas as the MCP condition, called as a tool | **the difference is transport only** — JSON-RPC over `stdio` against HTTP — and the model does not see transport |
| **(b) called from code** (the agent writes HTTP requests) | code text with a URL and JSON | the **code** condition, aimed at a different target |

In form (a) the two conditions differ in something the model cannot observe, and the expected effect is zero — which the industry numbers, weak as they are, point at (differences of a tenth of a percentage point). A third arm would cost roughly three weeks and 320 runs to measure something that is designed not to exist.

**One difference is not trivial**, and it is worth naming so that it is not mistaken for an oversight: OGC API – Processes standardises (1) a machine-readable process description and (2) an asynchronous job cycle — `execute` → `/jobs/{id}` → status → results. MCP has only an experimental Tasks extension in that place. That is an architectural difference, not a transport one, and it would matter for tasks requiring **long-running operations** (minutes, not seconds). The corpus contains no such task: every card is designed to be scored inside container limits. The difference is real and **outside the corpus**.

| Variant | What is done | Cost | What it buys |
|---|---|---|---|
| **V0 — chapter 2 only** *(recommended)* | §2.2 "from WPS through OGC API – Processes to MCP": the comparison table, the 52°North bridge, the finding that call style is a factor, and one sentence that the model does not see transport | 2 days | the theoretical justification and the positioning, with no risk |
| **V1 — a descriptive appendix** | 8 tasks, 2 conditions (MCP against OGC API through a service), 3 repetitions = 48 runs, reported as description with no hypothesis test | about 2 weeks | an empirical answer to "does transport matter" — expected zero, but **documented** |
| **V2 — a full third arm** | 80 tasks × r = 4 × 3 conditions | +320 runs, three weeks, and reopening a frozen scope | measures a difference there is no reason to expect |

**V0 is recommended, V1 is defensible, V2 is not.** The answer to a reviewer pressing for OGC is: *transport is invisible to the model, so a third arm would measure noise; instead MCP is positioned against OGC API – Processes in chapter 2, and the bridge that already exists is cited as evidence that the mapping is trivial.*

**A novelty risk worth knowing.** Because the OGC → MCP bridge was built and described in 2026, a thesis whose main contribution were "wrap OGC API in MCP and compare" would read as a repetition of a student project. The advantage here lies where that project has nothing: a **frozen surface, scoring on spatial artefacts, repetitions and an enforcement condition**. A third arm does not increase that advantage; it dilutes it.

**What not to cite.** Industry "MCP vs REST" benchmarks (vendor blogs, numbers with no protocol and no replication) — not as evidence. They may be mentioned in one sentence as reports from practice, with the caveat that they are not reproducible. The 52°North bridge is cited as an engineering project with a date, not as a scientific source.

---

## 12. What MCP actually is — and the two facts that matter for this thesis

A reviewer will ask whether the candidate knows what is being evaluated. One paragraph, then the parts that carry weight.

**MCP is an envelope layer.** It standardises the *form* of the message between an LLM application and a server — JSON-RPC 2.0, method names, result shape, error channel, version negotiation — and **does not standardise the meaning** of an operation. Three roles: **host** (the application: here, the harness with its loop, budget and trace), **client** (one connection, one server), **server** (the geoprocessing tools). The design is borrowed from the Language Server Protocol: it standardises how to connect, not what is connected.

**Version and transport, which have to be pinned in three places.** Revisions are dated: `2024-11-05` → `2025-03-26` → `2025-06-18` → `2025-11-25` → **`2026-07-28` (Current)**. The current revision is **stateless**: no `initialize`, no session header — protocol version and capabilities travel in the metadata of *each request*, and the server must implement `server/discover`. Transports: **stdio** for local use (`stderr` for logs; `stdout` must not be polluted) and **Streamable HTTP** for remote. So the thesis pins **the protocol revision, the SDK version and the transport**, and reports all three — otherwise the result is attributable to no particular state of the standard.

### 12.1 The two facts that carry the thesis

**Fact one — the protocol gives two and a half of the seven correctness gates.**

| Gate (from `design/correctness.md`) | Does the protocol provide it? | Note |
|---|---|---|
| B1 choice of tool | partly | `tools/list` provides the catalogue; choosing well is the model's job |
| B2 names and types | **yes** | `inputSchema` is JSON Schema (default dialect 2020-12) |
| B3 values (range, enum) | **yes, if the author declares them** | `enum` in the schema |
| B4 preconditions | **no** | the server; it may use `input_required` |
| B5 execution | **no** | the server |
| B6 result state (CRS, geometry) | **no** | the server; the protocol only relays the check |
| B7 file contract | **no** | the server |
| error channel | **yes** | `isError` plus a tool-error payload with content — **the precondition for repair in the loop** |

That number — **two and a half** — is what the thesis says, instead of "MCP standardises validation". It is also the whole reason the enforcement layer is a property of the *server* and therefore a thing the thesis can manipulate.

**Fact two — the protocol deliberately supplies a feedback channel, and it does not supply the content.** Since revision `2025-11-25` (SEP-1303), **input-validation errors must be returned as tool-execution errors, not as protocol errors**, precisely so the model can read them and correct itself. The error is *data*: `isError: true` with a readable payload, alongside `structuredContent` on success. That is exactly the feedback that the self-correction literature identifies as the bottleneck (`design/arms-and-validation.md` §5.1). What the protocol will not do is decide **what** counts as an error — the server's author must.

Two further details that are easy to get wrong and matter for comparability:

- **`annotations`** (`readOnly`, `destructive`, `idempotent`, `openWorld`) are **hints, and the specification instructs clients to treat them as untrusted**. If a surface's safety rests on annotations, that is not a gate, and counting it as one would inflate the enforcement layer.
- **`tools/list` order and caching** are set deliberately (deterministic order, pagination, `ttlMs`/`cacheScope`), because otherwise the catalogue condition receives a different prompt cache from the code condition and the cost comparison stops being comparable.

**MRTR — the gate that asks instead of blocking.** `resultType: "input_required"` with `inputRequests` lets a server **suspend a call** and ask for what is missing; the client retries with `inputResponses` and a new `id`. For the error taxonomy this is a **third response to class E2** ("the code exists but is the wrong one"): the server can neither guess nor guess silently, but *ask*. It is a different strategy from a blocking gate and must be **declared in the surface design**, because a gate that asks and a gate that blocks produce different catch rates.

### 12.2 Five methodological decisions that follow

1. **Pin three versions and state them in chapter 3**: the protocol revision (`2026-07-28`), the SDK version, and the transport (stdio, local QGIS). Without them the result is attributable to no particular state of the standard.
2. **`detected_by` must separate protocol errors from execution errors** as well as from own invariants and from the oracle. Splitting the first pair is new and free, and it shows whether the server uses the channel the protocol gave it.
3. **MRTR is either enabled or deliberately disabled**, and recorded as a property of the surface. If the server may ask, the catch rate measures something different than if it may only block.
4. **Deterministic tool order and cache policy** are fixed, or the cost comparison is between two prompt caches rather than two interfaces.
5. **Annotations do not count as validation** — see above.

And the standing risk: five revisions in twenty months, the last one stateless and therefore breaking servers written for the previous one. A thirteen-week series will cross at least one release. **Which is why the variable is not "MCP" but "MCP at revision X, through SDK Y, over transport Z"** — and why the durable claim is about the *necessity of checking the result*, a design dimension, rather than about a named protocol.

---

## 13. The facade question, and the one control it suggests

*Is OGC API a REST API? Is MCP based on REST? Can MCP not be a facade for OGC?* Short answers: **OGC API – Processes is REST** (resource-oriented, JSON, OpenAPI-described; the successor to WPS 2.0, which was RPC). **MCP is not REST** — it is JSON-RPC 2.0. And **yes, MCP can be a facade for OGC — it already is**: MapHub aggregates and queries OGC services through an MCP server.

The interesting sentence for chapter 2: **web GIS moved from RPC (WPS) to REST (OGC API) over fifteen years, and MCP brings RPC back** — not from nostalgia, but because LLM tool calling *is* RPC: the model chooses a capability name and arguments, not a resource and an HTTP verb. A second sentence follows: OGC API – Processes is already "a catalogue of geoprocessing capabilities with typed descriptions", so the difference from MCP is not discoverability but **who the client is** — a browser or a program, against a language model.

**Four facade topologies, of which two matter:**

| Topology | What the facade does | Where validation sits | Risk |
|---|---|---|---|
| **A. pass-through** | exposes `/processes` 1:1 | stays in OGC; the facade only translates | loses the semantics OGC's JSON Schema does not express (CRS, units) |
| **B. translating** | maps OGC descriptions into MCP tool schemas, adds constraints | in two places, partly duplicated | **two descriptions of one process drifting apart** |
| **C. re-implementing** | the facade has its own curated tools and calls OGC in the background | only in the facade | loses OGC capabilities that were not selected |
| **D. a standard binding** | OGC defines an MCP binding for API – Processes | one truth, standard validation | **does not exist as of November 2026 — an open standardisation niche** |

"MCP as a facade for OGC" is B or C in practice, and that is why it is scientifically interesting: **the facade is where the validation boundary becomes visible**, because a second, often automatically generated, description of the same capability is introduced.

**The control it suggests, and the one thing to avoid.** Topology B gives a natural experiment: removing validation from the facade while keeping it in OGC yields a *gated/ungated* pair for the same tool — a cheaper version of the missing 2 × 2 if time ever appears. And because OGC API and the QGIS Processing catalogue both publish **machine-readable descriptions**, a surface can in principle be **generated mechanically** rather than curated by hand. That is a direct answer to the weakest leg of the thesis — "your catalogue is your own straw man" — and the cheap version of it is the **anonymised-catalogue control** already in `design/corpus.md` §10. What must not be done: **do not expand the thesis into OGC facades.** The local engine is the condition of the "same engine" control, and it is the most important thing in the project.

---

## 14. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| the "four measurable quantities" table with H1/H2/H5/H6 numbering | `what-exactly-we-study` | it mapped onto a retired hypothesis list. The content survives in §1.1, re-expressed against the live ledger (H1, H2, H3, D1, D3) |
| the thesis statement built on "a 2 × 2 comparison and an equivalence test" | `what-exactly-we-study` | the 2 × 2 with gated code and its TOST are not in the design. §1 states what P3 can and cannot claim instead, which is a weaker and true sentence |
| the **K1–K4 contrast ladder** with the whitelisted code condition, the five random catalogues and the curation interaction | `comparison-basis-codegen-mcp` | three of its four contrasts are not conditions in the live design. §6 redraws the ladder against K · N1 · N4 and **marks the two missing contrasts as missing**, with the anonymised-catalogue control as the cheap stand-in for one of them |
| the eight-step "how it is computed" list with `df = 39`, "MDE 8.6 pp at r = 32", and the 40-task arithmetic | `comparison-basis-codegen-mcp` | belongs to the retired 40 × 8 generation and to `analysis/statistics.md`, which owns the arithmetic. §8 keeps the four points that are properties of the basis, with the live numbers (ICC 0.661, DEFF 3.0, 80 tasks, 14.0 pp) |
| the 40-line JSON-RPC and tool-description examples, the message-type catalogue and the primitive table in full | `mcp-protocol-shape` | a design note is not the specification. What a thesis needs is the **two facts** that carry the argument, the version pinning, and the five decisions — all kept; the wire examples are cut and will be a figure or an appendix if needed |
| the sixteen-row mapping of protocol features onto gates | `mcp-protocol-shape` | compressed to the seven-gate table and the number "two and a half", which is the claim. The rest was the table's own arithmetic |
| the full "risk forecast" and version chronology essay | `mcp-protocol-shape` | the chronology is four dates in one sentence; the consequence is one standing risk paragraph in §12.2 |
| the 52°North novelty discussion as a *risk to the thesis* | `mcp-rest-ogc-codegen` | it is a two-line paragraph in §11, not a section: the bridge existing does not threaten a thesis whose contribution is the frozen surface and artefact scoring |
| the three "levels of literature" (mechanistic, empirical, practical) with eleven citations | `mcp-rest-ogc-codegen` | it is literature review material and belongs to `framing/gap-and-literature.md`; two citations survive here because they are load-bearing for the no-third-arm argument |
| the industry benchmark numbers (99.84 % / 99.71 % / 99.52 %) | `mcp-rest-ogc-codegen` | not evidence, by their own admission; the *fact that the question circulates* survives as one clause |
| the "facade topologies" detail beyond the four rows, and the "what not to do" list as prose | `mcp-ogc-facade` | four rows plus three rules; the list became the last paragraph of §13 |

Kept, because each is the only place in the repository where its claim is made: the three-level decomposition and the "MCP is not REST" correction (§1), the four-component answer to "does it pay off" with the decision table (§1.1), the one-paragraph basis with the ceteris paribus table and the error-channel note (§2, §2.1), A1–A5 with their consequences (§3), the four advantages and four limits of artefact scoring (§4), the three layers (§5), the honest contrast ladder marking what is missing (§6), the run record and the three auditability hashes (§7), the four computation properties (§8), the worked A-07 example across three conditions (§9), the six limits (§10), the no-third-arm argument with V0/V1/V2 and the async difference (§11), the two protocol facts, MRTR and the five decisions (§12), and the facade topologies with the generated-catalogue control (§13).

---

## 15. Five lines, and one sentence

1. **Three levels, two measured.** Transport is invisible to the model and is argued in chapter 2; representation and enforcement are measured, the second only inside the surface.
2. **The file is the instrument, not the object.** Same prompt, same data, same budget, same oracle, one thing different: the action channel. That is the only basis on which two channels can be compared at all.
3. **Five assumptions, each with its consequence written down.** The dangerous two are information parity and budget parity, because both can break in good faith after the fact.
4. **The arithmetic is 80 tasks at r = 4, ICC 0.661, DEFF 3.0 and an MDE of 14.0 pp** — so 960 runs are worth about 320 independent rows, and nothing below 14 pp is decided.
5. **No third arm, and no fourth condition.** Transport is invisible and gated code is absent; both absences are named with their cost, which is what makes the rest of the comparison credible.

**And in one sentence.** Two of the three ways the question can be posed are measured — the representation of geoprocessing as named tools against generated code, and the depth of enforcement on an identical surface — with everything else pinned and hashed, the artefact scored by spatial predicates rather than by a judge, and the claim bounded in advance by an MDE of 14 pp and by two contrasts the design deliberately does not contain.
