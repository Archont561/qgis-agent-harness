---
id: design/arms-and-validation
title: "Arms, factors and the validation boundary"
type: note
status: live
language: en
question: "What is manipulated, what is held fixed, and where does validation sit?"
tasks: [TASK-1, TASK-5]
sources: [hypotheses-and-factors.md, validation-standardisation.md, validation-in-the-code-arm.md, what-a-tool-can-validate.md]
updated_date: '2026-11-07'
---

# Arms, factors and the validation boundary

> What is manipulated, what is held fixed, and where does validation sit?
>
> The **owner of the claim ledger**. If any other document disagrees with §2 below about what the thesis claims, this section wins. The rest of the document defines the factors operationally (§3) and then argues the one thing the design is really about: **where the invariant lives** (§4), and why the code condition is not a straw man (§5).
>
> Written against the live design only — K · N1 · N4, 80 tasks, r = 4, 960 runs (`design/experiment.md` §0). Pruned and translated 2026-11-07 (`TASK-21`): 7,530 → 6,455 words, four source notes → ten sections.

---

## 1. One thing that is not a hypothesis

**D4 — "the comparison can be built and it is stable" — is not a claim about the world.** It is a *condition of the instrument*: oracles that repeat, κ on the failure taxonomy, a baseline TSR above the floor, a predicate set that rejects the broken artefact. It is checked in the pilot; if it fails there is nothing to test, and the thesis reports the failure rather than the comparison.

It is listed in §2 with the other claims because a reader needs to see it, and it is marked there as a precondition: **a "significant" D4 would mean the meter is broken.** The same sentence applies to A1–A5 in `design/experiment.md` §3.1 — assumptions, not results.

---

## 2. The claim ledger

Two rules of composition, both learned the hard way:

1. **A claim is written without a direction.** The hypothesis says *differs*; the expected direction is recorded separately as a *prediction from the literature*. Otherwise an unexpected sign reads as a failure and invites rephrasing after the fact.
2. **Each claim has one falsifier.** Not a list of things that would be interesting, but the single observable pattern that would make the claim false. If that pattern cannot be written down, the claim is not a claim.

| # | Claim (no direction) | Prediction from the literature | Variables | Test | Falsifier |
|---|---|---|---|---|---|
| **H1** | The way the same nine operations are exposed **changes** artefact correctness on an identical engine | weak and two-sided: the MCP literature reports cases where tool access *hurts*, the practice literature expects the catalogue to win | factor: condition (K vs N4); DV: TSR per task | paired McNemar at task level + mixed logistic with a random task effect — **the one confirmatory test, α = 0.05** | a difference below the MDE (undecided, not refuted) or a negative difference ≥ MDE (refuted) |
| **H2** | Correctness **rises with enforcement depth**: N4 against N1 on an identical surface | `geocontra2026` (spatial contracts raise code correctness by ≈ 26 pp); `strickland2026pareto` (locally valid, composed unsound) | factor: enforcement layer (P-I vs P-II/P-III); DV: TSR | **trend**: linear contrast N1 → N4 plus a plateau fit, not a pair of tests | a flat curve **with** a flat catch rate — the gates would then be inert (outcome W2) |
| **H3** | The difference **grows with the expressible share** of the task | the mechanism predicts it: where the requirement can be carried by the surface, a gate can act; where it cannot, it cannot | DV: ΔTSR per card; moderator: expressible share (all / most / part / none) | condition × share interaction, with the **pattern** stated in advance | a flat interaction across the whole range, **or** a correctness difference on `none` cards — that would mean the difference is not about what the surface can carry |
| **D1** | The conditions differ in **repeatability**, not only in the mean | `strickland2026pareto` (determinism against flexibility), `fan2026infofidelity` | error-class distribution; S3 = share of tasks whose dominant error class covers ≥ 75 % of their failures; predicate-level identical/equivalent/divergent across the four repetitions | distributions + S3 as a proportion with a task-bootstrap CI | indistinguishable distributions and equal S3 |
| **D2** | They produce **different failure signatures**: the catalogue errs on tool or parameter choice, code errs silently on CRS, geometry and aggregation | `zhang2025msb`, the GIS literature on silent error (`iso19157`, `monmonier2018`) | seven failure classes, eight CRS classes, `detected_by` | distributions + κ on 20 % blind double coding | indistinguishable class distributions — and κ < 0.6 first invalidates the measurement rather than the claim |
| **D3** | **Cost per successful task** differs, and reverses the TSR ranking in at least one family | `song2025helpor` (overhead), MapHub/OGSAgent (claims without measurement) | tokens, calls, seconds ÷ successes, per task | ratio estimator + task-level bootstrap | one condition dominates on both correctness and cost in every family |
| **D4** | *Precondition:* the comparison is stable — the oracle repeats, the artefact verdicts agree across repetitions and blocks | — | predicate verdicts, artefact hashes, manifest fields | agreement + digests | instability, which stops the series rather than refuting a hypothesis |

**D1 has a reporting companion, not a second test.** The four repetitions per cell also give
*pass⁴* — the share of tasks on which **all four** runs succeed — which is the consistency number a
practitioner asks for (`yao2024taubench` introduced it as pass^k). It is reported as a descriptive
beside the ICC, never as a hypothesis: the pre-registration is frozen, and at ICC = 0.661 with a
modest TSR the estimate sits near the floor, so its task-bootstrap interval will be wide. ICC remains
the better estimator of the same property; pass⁴ is there because it is the number a reader can
interpret without a variance decomposition.

**Hierarchy and test budget.**

| Role | Claims | α |
|---|---|---|
| one confirmatory test | **H1** | 0.05 |
| Holm within the family | **H2**, **H3** | 0.05, corrected over two tests |
| descriptive, intervals and no stars | D1, D2, D3, and S4/S4b/S5 | — |
| precondition, reported in chapter 4 | D4 | — |

Three tests carry inferential weight and the rest are description. That is the whole budget, and it is the reason `analysis/statistics.md` §4 says *count the tests before the series*: a chapter 6 with eleven starred p-values means this table was rewritten after the fact.

**Durability order**, in case the thesis has to be defended on partial results: H2 > D1 > H3 > D2 > H1 > the instrument. The depth curve and the repeatability contrast survive a failed main comparison, which is why the corpus and the register are built to produce them even if H1 comes out undecided.

**What is not on this list**, and why it is not an omission: the three adversarial cards (a number with an exact interval, not a test), the plateau point of the depth curve (practical advice, not a causal claim), the platform slice (a limitation), model or harness ranking (outside the design), and gated code generation (`framing/edge-of-scope.md` §4.2).

---

## 3. The factors, operationally

### 3.1 Condition — three levels

| Level | What the agent gets | Enforcement layer | What the enforcement can know |
|---|---|---|---|
| **K** — code generation | one execution tool (`run_python`) and the environment; it writes and runs a program | the interpreter only | syntax, names, types, exceptions — the language |
| **N1** — catalogue, basic | nine named operations with signatures and JSON schemas | **P-I**: is the call well-formed | the signature |
| **N4** — catalogue, extended | **the same nine operations, the same descriptions, the same schemas** | **P-II** invariants + **P-III** terminal conditions | the data, the domain rules, and the task contract as stated in the prompt |

N1 and N4 have **identical surfaces** and differ *only* in the enforcement layer. That is the necessary condition for H2 to be a causal statement: if the surfaces differed, "named operations" and "gates" would be inseparable. It is also why the wording of the nine descriptions is frozen down to the comma, and part of the reason the treatment is documented like the task cards rather than like plumbing.

Three definitions that are easy to blur and must not be:

- **The gate is not the oracle.** The oracle checks **correctness against ground truth** and is hidden. The gate checks **form and declared expectations** and is visible to the agent. If the gate could see the oracle, every gated run would pass trivially and H2 would measure nothing.
- **N1 already validates.** The protocol enforces types and schema. What N4 adds is the part that is *not* in the schema: CRS and unit invariants, the state of the result, and a repair loop. H2 therefore asks whether the **second** layer adds anything over the first, not whether "MCP validates and code does not".
- **A rejection is not a repair.** A gate that refuses the only viable plan converts a wrong answer into no answer; that is what `REF` and the `fuzzy` tier are for (`analysis/statistics.md` §5).

### 3.2 Task family — three levels

**Family = the kind of GIS work, defined by *what is checked as correct*** — not by how many tools it needs and not by difficulty:

| Family | Operations | What "correct" means | How it is checked |
|---|---|---|---|
| **P — preparation / IO** | load, reproject, clip, table join, export | the data on disk are right | geometry, CRS, attribute and feature-count predicates |
| **A — analysis** | buffer, overlay, aggregate, statistics, spatial relations | the numbers and geometries are right | predicates plus numeric tolerances |
| **C — cartography / presentation** | classification, symbology, labels, composition, map export | **the requested style features were applied** and the map renders | declarative predicates: renderer type, class count, classification field, palette, label field, composition elements, DPI, non-empty raster |

Family is the **selection axis** (`d-3`) and a blocking factor: each card belongs to exactly one family, and cards from different families have *different predicate vocabularies*, so they may never be averaged into a single TSR without the split being shown.

> Terminological note: **task family** ≠ **tool group in the catalogue**. The catalogue is also divided (analysis / cartography / IO / metadata), and that division is *surface composition*, not the family factor.

### 3.3 Tier — four levels

**Tier = the analytical depth of the task**, not the number of calls. All four are measured from the reference solution and recorded on the card:

| Tier | Definition | Indicators |
|---|---|---|
| **T1** | one call, one expression | 1 operation, 1 family, no decision |
| **T2** | 2–4 dependent steps in one family | 2–4 operations, 1 family, no method choice |
| **T3** | 6–10 steps, **crossing families** (prepare → analyse → style) | ≥ 2 families, a dependent sequence |
| **T4** | a **fuzzy** task: interpretation required, no canonical sequence (e.g. "the best location" with soft criteria) | no unique solution; scored by threshold predicates |

What a tier is not: not the number of tools in the catalogue, not the number of distractors, and not the family. **Tier is "how deep"; family is "what is checked".** The 40-card seed contains 5 / 19 / 14 / 2 cards across T1–T4, which is itself a finding about corpus design: T4 is where the interesting failures are and where the corpus is thinnest.

### 3.4 Expressible share — the moderator of H3

**Definition.** For task *t* and surface *S*:

```
expressible_share(t, S) = |{requirements of t that S takes as a parameter and can check}|
                        / |{requirements of t}|
```

A requirement codebook, seven types, each coded on the card:

| # | Requirement type | Can the surface take it and check it |
|---|---|---|
| W1 | a numeric value **with a unit** | `distance` + a required `unit` → yes |
| W2 | the target CRS | `target_crs` → yes |
| W3 | the required set of operations | tool count and order → partly |
| W4 | a spatial condition (inside / at least x away) | mask, predicate → yes |
| W5 | the file contract (path, format, number of artefacts) | `write_vector(path, format)` → yes |
| W6 | required output fields | `attr_present` → yes |
| W7 | a quality criterion (quantile, 300 DPI, 5 classes) | symbology / classification → yes for a closed list, no for "nice" |

Two extreme cards from the corpus and two middling ones:

| Card | Requirements | Expressible | Share |
|---|---|---|---|
| **A-01** buffer + intersect | 5 km · 2180 · buffer + clip · inside the communes · path · `gmina_id` | W1 W2 W3 W4 W5 W6 = 6/6 | **1.00** |
| **A-13** area comparison, 2180 vs 3857 | two CRSs · same layer · comparison · result | W2 W3 W5 = 3/4 | **0.75** |
| **C-11** two-page atlas | two pages · one unit per page · atlas extent · page format · title… | W3 W5 + part of W7 ≈ 2.5/5 | **≈ 0.50** |
| **C-09** Jenks classification with class labels | method · class count · labels · palette | W7 (closed list) + W6 = 2/4 | **≈ 0.50** |

The expressible share is **not a property of MCP** — it is a property of the **(task, surface) pair**. That is the whole point: the comparison is run on the same tasks in every condition, and what is predicted to grow is the *difference*, as a function of that share.

**Coding procedure.** 80 cards × 7 requirement types = 560 decisions. Two coders on 20 cards, κ reported; the remainder is coded by one person. That is one day of work, and it is the cheapest way to turn the strongest objection to the thesis into a variable — which is what H3 is for.

**The dose model** that makes the prediction falsifiable:

```
ΔTSR(t) ≈ Σ_(w in requirements of t)  P(model errs on w) × 1[w expressible in S] × P(gate blocks) × P(repair succeeds)
```

- `1[w expressible]` is zero for cards with a low share: **there the predicted difference is zero**, and a difference there is evidence against the mechanism.
- `P(model errs on w)` comes from the pilot, per requirement type — units and CRS are confused often, paths rarely.
- The third and fourth factors are what N4 against N1 isolates, with the repair loop bounded at two attempts so that enforcement does not become a compute subsidy.

### 3.5 What is frozen, and the factors that could have been and are not

| Held fixed | Value | Why it is not a factor |
|---|---|---|
| engine | QGIS 3.44, pinned by digest | a second engine changes the research question (`framing/edge-of-scope.md` §3.5) |
| model | one, pinned by name, version, date | `d-2`; a model × condition interaction doubles the series before it says anything |
| agent harness | one, pinned; identical system prompt (the *evaluation* harness — `design/harness.md` §0.1 — is the instrument) | `d-4`; the "one CLI" objection is answered in the limitations |
| limits | 25 turns, 10 minutes, one token budget | A4: an asymmetric budget is a confound, and the run is flagged, not discarded |
| tasks and data | 80 cards, four repetitions | the corpus is the source of power, not the arms |
| versions | QGIS / GDAL / GEOS / PROJ by digest | tolerances instead of byte equality; D4 measures the rest |

**Two designs that were considered and are not being run**, recorded so that nobody reinvents them: a **crossed model** factor (the most interesting absent interaction, and the first item of further work) and **gated code generation** (the cell that would separate validation from representation; `framing/edge-of-scope.md` §4.2 states what its absence costs the claim).

---

## 4. The validation boundary: what MCP standardises, and what it cannot

### 4.1 The claim, narrowed to what survives

MCP standardises the **envelope and the syntactic contract** of a call: the input schema, the message format, the result envelope, error signalling, tool discovery, transport. It does **not** standardise semantics — what "250" means, whether it is metres, in which CRS.

So the claim is not "validation is standardised". The claim is: **the place where validation happens is standardised.**

| Element | Standardised by MCP? | Consequence for validation |
|---|---|---|
| tool input schema (`inputSchema`) | **yes** | type, required-field and enum validation, uniformly, server-side |
| call message format | **yes** | one place to parse and one place to reject |
| result envelope (`content`, `isError`) | **yes** | an error is **data**, not an exception — the model can read it and repair |
| tool discovery (`tools/list`) | **yes** | the surface is declared machine-readably, so it can be versioned and hashed |
| transport | **yes** | the same surface works in any client |
| **parameter semantics** | **no** | "250" — metres or feet? The server decides, not the protocol |
| **preconditions of state** | **no** | does the input carry a CRS? Implemented by the server, if at all |
| **terminal conditions** | **no** | is the result in the requested system? Implemented by the server, if at all |
| **validation policy** (what to reject, what to repair) | **no** | a decision of the server's author |

### 4.2 The standard enforcement point

> **SPE — one versioned place in the system where a correctness condition is checked and enforced on every run, regardless of what the model thought of.**

Four properties that code generation lacks **structurally**, though it can imitate them by convention:

| Property | In MCP | In code generation |
|---|---|---|
| one implementation across all runs | yes — server code | no — an assertion in the script is new every run |
| testable and versioned | yes — the server module has tests and a version | no — a model-written assertion has no test |
| auditable after the fact | yes — the call log plus the validation result | partly — the sandbox has to be instrumented by hand |
| composable across servers | yes — the envelope is shared | no — every script invents its own conventions |

The consequence that decides the measurement: **standardisation does not raise the ceiling of capability, it lowers variance and makes failures diagnosable.** That is why it cannot be measured by TSR alone, and why D1–D3 exist.

### 4.3 One task, three errors

Task: reproject to EPSG:2180 and buffer by 250 m. Three errors can occur.

| Error | Where a gated catalogue catches it | Where code catches it |
|---|---|---|
| `2177` given instead of `2180` | **P-I/P-II gate**: the code does not exist in the registry, or does not match the declared target | nowhere — a valid file in the wrong system is produced |
| the input carries no CRS | **P-II**: precondition on the state | `pyproj` raises — sometimes, depending on the path taken |
| the buffer computed in feet | **P-II/P-III**: the output extent falls outside tolerance, or violates the stated contract | nowhere — the file passes, and the oracle rejects it after the fact |

In two of three cases **code has nowhere to catch it**: there is no layer in which such a condition could stand. That is the entire structural difference, in one sentence: **a tool surface makes room for a gate; a script makes room for an incident.**

### 4.4 What a tool can know: three levels

| Level | What the tool knows | Source | Example | Who has it |
|---|---|---|---|---|
| **P-I syntax** | whether the call matches the schema | the signature | `unit ∈ {m, km, ft}`, `distance > 0` | both conditions after decoder validation — **does not discriminate** |
| **P-II invariants** | whether the state of the world after the operation is consistent | **data + domain rules, without knowledge of the task** | CRS present · area of use consistent with the extent · valid geometry · CRS **written into the file** · raster size consistent with cells · no writes outside the output directory | **only the server** |
| **P-III intent** | whether the result satisfies the **requirement of the task** | the task text or an explicit contract | "5 km", "clip to the communes", "write in 2180" | neither server nor code by default — the oracle, **or** a tool to which the contract was given |

The distinction that earlier drafts of this work got wrong: P-I is free in 2026 and discriminates nothing, but most of the real value of gates sits in **P-II**, and P-II is not "checking a parameter value" — it is checking **properties of the result against the data**, and the result is available to a server in a way it is not available to the action channel of a code condition.

### 4.5 The honest recount: what a gate catches without knowing the task

| Class | Level needed | Catchable without intent? | Note |
|---|---|:--:|---|
| **E1** non-existent code | P-I | ✓ | but so does the decoder and `pyproj` — **does not discriminate** |
| **E2** existing code, wrong one | P-III | **✗** | needs the expectation; only an enum from the prompt, a name, or an echo |
| **E3** false CRS in the metadata | **P-II** | **✓** | area of use against the data extent — a **real gate** |
| **E4** missing transformation | P-III (request) + P-II | partly | output ≠ input is checkable; "≠ requested" needs the request |
| **E5** omitted datum shift | P-III (reference) | **✗** | nothing to compare against without a reference |
| **E6** units that break the next step | P-III | **✗** | the server can only force a declaration and convert itself |
| **E7** CRS not written into the file | **P-II** | **✓** | cheap, certain, task-independent |
| **E8** invalid geometry | **P-II** | **✓** | as above |

**The honest balance: three classes fully (E3, E7, E8), one partly (E4), four not at all** — and of those four, E1 is trivial. An earlier version of this note claimed "a well-designed server catches 7 of 8", which was a number from a table that had quietly assumed the server **knows the task**. It does not. **Corrected: 3–4 of 8 without a contract, 7–8 of 8 with the contract made explicit.**

That is not a reason to abandon the comparison. It is a reason to change its basis, which is what H3 does.

### 4.6 The contract-bound surface — and why it is N4

If a task has an explicit, machine-readable contract — and the cards do — the contract can be **given to the tool**: `buffer(input, distance, unit, contract: {target_crs: "EPSG:2180", expect_extent_within: "data/communes.gpkg"})`. The server then checks **P-III**, not only P-II, and that is the only way a tool can know that "5 m" is wrong.

Two things must be said about it honestly:

1. **It is not an oracle leak.** The information-closure principle holds: `guard_information ⊆ agent_information`, because the contract **is in the prompt** — the tool receives nothing the model does not have. Moving it into a signature is therefore legal. A hidden expectation may only be a measurement gate on the harness side.
2. **It is the work of a designer, not "the action of the protocol".** Someone has to turn the requirements into constraints — once, in a versioned component. What is being compared is therefore a **one-off cost** against a **cost incurred again in every run**. That is the fair version of "a guarantee that is written once against a guarantee that is improvised", without hiding who pays.

**This is what N4 is.** What an earlier round proposed as a fourth surface `L5` — the surface bound by contract — is the extended catalogue condition, and it entered the design rather than the future-work list. The remaining difference is only that N4 carries P-II invariants *and* the P-III terminal conditions stated in the card, and that the four-level tool ladder it was meant to sit on has been retired (`design/corpus.md` §11).

### 4.7 What remains when nothing can be expressed

On cards with a low expressible share (C-11, C-09, much of T4) the server has nothing to check — and then only the measures that are *not* correctness do any work:

| Measure | What it shows | Why it works without intent |
|---|---|---|
| `PCI` | the error was **noticed in the loop** | the observation is structural: the chosen `unit`, `target_crs`, feature count are visible |
| S3 | the error is **attributable** — same class, not "something went wrong" | the classes are named in the result |
| S4 / S4b | whether the code condition **has a place** for a check at all | independent of the main result |
| composition | the step chain needs no intermediate writes | a handle instead of a path |

That is the entire content of "the interface changes the structure of failure, not its level" — and the reason it has to be available in reserve, because the objection in §4.5 is the one most certain to be raised.

---

## 5. The code condition is not a straw man

The single easiest way to ruin this thesis: give the code condition a prompt without an instruction to check the result, and gate the catalogue. Then the comparison measures two different instructions, and the reviewer's answer — *"add one sentence and the difference disappears"* — is correct.

**The design closes that hole by construction**: the system prompt is **identical** in all three conditions and contains the **same** instruction to verify the result against the task before finishing. The code condition is therefore given the same discipline the catalogue has built in, and the contrast becomes: *with the same instruction, only one condition has something to check against.*

### 5.1 The literature that makes it a mechanism rather than a metaphor

| Work | Finding | Numbers |
|---|---|---|
| **Huang et al., ICLR 2024**, *LLMs cannot self-correct reasoning yet* (arXiv 2310.01798) | **internal** self-correction without external signal does not improve the result — it degrades it; earlier "successes" used oracle labels to stop the loop, which is oracle filtering, not self-correction | GPT-4 GSM8K: 95.5 → 91.5 → 89.0 over two rounds; of the changed answers **8.8 % correct → wrong** against 7.0 % wrong → correct; Llama-2 down to −25.5 pp |
| **Kamoi et al., TACL 2024**, *When can LLMs actually correct their own mistakes?* (arXiv 2406.01297) | no earlier work demonstrates reliable self-correction from model-generated feedback in general tasks; it works where **reliable external feedback exists** (an interpreter, a solver); **the bottleneck is generating feedback, not acting on it** | critical review; categorical conclusion |
| **Tyen et al. 2024** | a model **repairs** an error when its location is pointed out, but does not find the location itself | — |
| **Self-Refine ablation** (in Huang et al.) | the gain came from the feedback prompt carrying **richer content** than the initial prompt, not from self-correction | no gain once the content is moved into the first prompt |

In the language of this literature, **the tool condition is a feedback generator** — and what distinguishes a server from "ask the model to check" is that it supplies **the location and the content of the error**, which is exactly what Tyen et al. identify as missing.

**One caveat that must be stated, not glossed:** the code condition *does* have external feedback — the interpreter. It is feedback **defined by the language**, not by the domain. So the code condition is not "unvalidated"; it is validated with **the wrong content for GIS**. That sentence is the honest form of the claim, and it is stronger than the version it replaces, because it cannot be dismissed by pointing at a traceback.

### 5.2 Three sources of checking, and who has them

| Source | Code condition | Catalogue condition |
|---|---|---|
| **S1. Language** — syntax, types, exceptions, undefined names | ✓ automatically (the interpreter) | ✓ automatically (decoder / schema) |
| **S2. Domain invariant** — CRS present, geometry valid, unit declared, area consistent with extent, CRS **written into the file** | **only if the model writes it** — probability *q*; it may import `pyproj`, `shapely`, `QgsGeometryValidator`, but that is its decision in every run | ✓ **always**, because it lives in the server, not in the model's context |
| **S3. Reference value** — "what should come out" | only from the prompt or the oracle | the same, or from the contract stated explicitly (§4.6) |

The sentence this yields, and it is the thesis in one line: **the difference is not that one condition validates and the other does not — it is where the domain invariant is kept: in the model's context, rebuilt every run, or in a versioned component written once by a human.**

### 5.3 What is measured instead of assumed

Because the claim turns on probability *q*, *q* has to be measured, not presumed:

| Measure | Definition | Why it matters |
|---|---|---|
| **S4** | share of code-condition runs whose script contains **any** check of the result | shows how often the model even tries |
| **S4b** | among those, the share of **domain** checks against language checks | the direct answer to "at most a syntax or type error" — and it is measurable |
| **`detected_by`** with four values: `language`, `own invariant`, `execution error`, `oracle` | where the error was caught | without four values, "the model wrote a check, but a language check" is indistinguishable from "the model wrote nothing" — and that distinction is the thesis |

**The falsification condition, written before the measurement** so that a null cannot be reinterpreted as a failure:

> If TSR, the in-loop catch rate and error-class repeatability turn out **indistinguishable** between conditions, the conclusion is: **standardising calls does not translate into execution correctness in this task class**, and the value of the SPE is engineering and audit — provenance completeness, surface versioning, portability across clients. If the code condition systematically writes **domain** checks (S4b high), the claim is refuted. Both are legitimate, publishable results and will be reported as such.

---

## 6. Why this weighs more in geoinformatics than elsewhere

| Property of GIS | Why it strengthens the SPE argument |
|---|---|
| **errors are silent** | CRS, units and NoData raise no exception; the only place to catch them is a gate written by the server's author |
| **outputs feed decisions and publications** | a map in the wrong system is worse than no map; auditability is a requirement, not decoration |
| **the domain has registries** | EPSG, OGC, ISO 19115, GML — **ready-made sources of constraints** for P-II gates; in domains without registries an SPE would have nothing to fill itself with |
| **reproducibility is a procedural requirement** | the same conclusion, the same result, the same record — exactly what one implementation across runs provides |
| **the artefact is verifiable** | spatial predicates exist, so a failure is visible — **but only after the fact**, unless there is a gate |

The sentence for chapter 3: **in GIS, standardisation does not mainly improve the mean — it makes failure early and repeatable.** That is a different and stronger promise than "how many percentage points better", and it is the one D1 measures.

---

## 7. Three counterarguments, and the answers

**K1. "Semantics are not standardised, so there is nothing to standardise."**
> The **place** of enforcement is standardised, not the content of the condition. And that is measured directly: the same surface at P-I and at P-II/P-III. If correctness rises only with the second layer, the protocol supplies the frame and the author supplies the content. That is a result, not an objection.

**K2. "Code can be standardised too — with a library, a validator, a linter."**
> Yes, **by convention**. So the question is not "can it" but "does it". That is measurable: the share of runs in which the model wrote any checking condition at all (S4) and what kind (S4b). If domain checks are rare, the advantage of the SPE is empirical, not merely theoretical.

**K3. "This is a study of your server, not of the protocol."**
> Agreed, and that is the point: in MCP the guarantee **lives in the server and is shared by every run and every client**. To show it is not one implementation, the enforcement depth is itself the variable (N1 against N4) and the catalogue is authored against documented workflows, with the anonymised-catalogue control (`design/corpus.md` §10). The protocol contributes exactly as much as shared enforcement contributes — and that is what is being measured.

---

## 8. Where this lands in the thesis

| Section | From this document |
|---|---|
| §3.2 | the factor table from §3 (levels, within/between, what is frozen) |
| §3.4 (pre-registration) | the claim ledger from §2 with its falsifiers and hierarchy |
| §3.3 and §4 | the three levels P-I/P-II/P-III, the `gate ≠ oracle` distinction, the information-closure principle, the expressible-share definition and its coding |
| §4 (materials and methods) | the predicate glossary, the four-valued `detected_by`, S4/S4b |
| §5 | the declaration that the work is research, experimental in the sense of §III.9 (`scope-and-character.md` §4) |

---

## 9. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| the hypothesis table H1–H7 with per-hypothesis DVs | `hypotheses-and-factors.md` | the live ledger is H1–H3 plus D1–D4; H4a/H4b (the 2 × 2 and its TOST), H5 (ED classes), H6 (cost) and H7 (signatures) were re-expressed as D1–D3 rather than deleted, because a descriptive claim needs no α. A second numbering of the same claims ends in two systems of reference |
| the four-level tool ladder L1–L4 and `min_surface` as a factor | `hypotheses-and-factors.md` | the tool-count ladder is retired with `min_surface` (`design/corpus.md` §11); what replaced it is enforcement depth on a fixed surface |
| the `gate` factor with levels `none` / `gate` and its 2 × 2 with `codegen-gated` | `hypotheses-and-factors.md`, `validation-in-the-code-arm.md` | the live design has three conditions in a depth ladder, not a factorial over representation and gating. The reasoning survives in `framing/edge-of-scope.md` §4.2, with the cost to the claim stated |
| **condition C0** (a prompt without the checking instruction) and **C2** (a prompt without reference values) | `validation-in-the-code-arm.md` | C1 — the identical checking instruction — **is** the design, and it was adopted; C0 is the straw man the design avoids by construction, so running it would have measured the straw man; C2 violates A3, information parity, and would have changed the thesis into "how much domain knowledge does the model have" |
| the design arithmetic for that proposal (four conditions, 1 280 runs, MDE 10.3 and 14 pp) | `validation-standardisation.md`, `what-a-tool-can-validate.md` | it describes a series that is not being run: two conditions at r = 8, then four at r = 4. The live series is 960 runs at r = 4 with three conditions |
| **the fourth surface `L5`** as a separate arm | `what-a-tool-can-validate.md` | it became N4 (§4.6): a contract-bound surface is not an extra arm, it is the extended catalogue condition, and treating it as a separate surface would have duplicated the design |
| the simulation evidence for the variance argument (0.2114 / 0.2121 / 0.2118) and the class-repeatability table (0.65 vs 0.37) | `validation-standardisation.md` | the *argument* survives and is stated once: variance of a binary outcome is a function of its mean, so standardisation cannot be measured as variance. The simulated numbers belonged to the pre-results scaffolding removed on 7 XI 2026 and are not reproducible from anything in the repository |
| the nine-entry glossary of `dystractor`, `min_surface`, `T2V`, `REF`, `ED` and kin | `hypotheses-and-factors.md` | the terms that survive are defined where they are used; a glossary in a design note duplicates `thesis/glossary-of-terms.md` and drifts from it |
| the "how it lands in the thesis" list of four chapter items, second copy | `hypotheses-and-factors.md` | one map, in §8 |

Kept, because each is the only place in the repository where its claim is made: the rule that a claim carries no direction and one falsifier (§2), the durability order, the three condition definitions with the three distinctions that keep them apart (§3.1), the family and tier operationalisations (§3.2–3.3), the expressible-share codebook, coding procedure and dose model (§3.4), the list of frozen factors and the two designs not run (§3.5), the SPE and its four properties (§4.2), the three-error example (§4.3), P-I/P-II/P-III (§4.4), the honest recount of 3–4 of 8 (§4.5), the contract-bound surface and the information-closure argument (§4.6), what remains when nothing is expressible (§4.7), the self-correction literature with its numbers and its caveat (§5.1), S4/S4b and the four-valued `detected_by` (§5.3), and the three counterarguments (§7).

---

## 10. Five lines, and one sentence

1. **Six claims, three with inferential weight.** H1 (the exposure changes correctness), H2 (it rises with enforcement depth), H3 (the difference grows with the expressible share) carry tests; D1–D3 are description; D4 is a precondition, not a finding.
2. **The manipulation is enforcement, not the surface.** N1 and N4 expose the same nine operations with the same words and differ only in whether invariants and terminal conditions are checked.
3. **What MCP standardises is the place of enforcement, not the content of the condition.** That is the SPE, and it is why the claim is about diagnosability and repeatability as much as about the mean.
4. **A gate knows less than intuition says: three or four of the eight CRS error classes without a contract.** That is why the basis of comparison is the expressible share of each task, coded before the measurement.
5. **The code condition is not a straw man, and the literature says why it cannot easily repair itself.** With an identical checking instruction, only one condition has the domain invariant stored outside the model's context — and *q*, the probability that the model writes its own check, is measured rather than assumed.

**And in one sentence.** Three conditions expose the same nine operations with growing enforcement depth, and the thesis claims that the way geoprocessing is exposed changes the correctness of the artefact and, more certainly, changes *where and how reproducibly* the mistakes are caught — with the size of any correctness difference predicted to grow with the share of the task's requirements that the surface can carry, and with a null reported as a result about auditability rather than as a failure.
