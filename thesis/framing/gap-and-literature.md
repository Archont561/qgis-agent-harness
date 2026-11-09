---
id: framing/gap-and-literature
title: "The gap and what the literature leaves open"
type: note
status: live
language: en
question: "What is not known yet, and which of it does this thesis answer?"
tasks: [TASK-9, TASK-10]
sources: [gap-and-rqs.md, literature-brief.md, literature-mcp-vs-code.md, origin-of-terms.md]
updated_date: '2026-11-07'
---

# The gap and what the literature leaves open

> What is not known yet, and which of it does this thesis answer?
>
> The literature half of the framing: what six streams establish (§1), the one cell they leave empty (§2), the gap in five pieces with one of them honestly closed by someone else (§3), and — the section that matters most for calibration — **the evidence that points against this thesis** (§4). Then the nearest neighbours (§5), the research questions mapped onto the claim ledger (§6), what may not be claimed (§7), the provenance of every term (§8), and the citation hygiene that has to happen before chapter 2 (§9).
>
> Pruned and translated 2026-11-07 (`TASK-21`): 7,505 → 6,050 words, four source notes → eleven sections. Rewritten against the live design (K · N1 · N4, 80 tasks, r = 4, 960 runs) and against the single claim ledger in `design/arms-and-validation.md` §2.

---

## 1. What is known, in six streams

| Stream | What it establishes | Strongest citations | What it leaves open |
|---|---|---|---|
| **A. Protocol and foundations** | MCP is a JSON-RPC contract for tools, resources and prompts; servers are largely mechanical wraps of REST surfaces; distortion along tool chains is bounded, not explosive; descriptions are an attack surface | `anthropicMCP`, `mastouri2025automcp`, `fan2026infofidelity`, `maloyan2026breaking`, `zhang2025msb` | nothing about a *domain*; fidelity is analysed, never measured in spatial work |
| **B. General MCP tool-use benchmarks** | agents cope poorly-to-unevenly with large catalogues; **MCP is not automatically better than non-MCP baselines**; catalogue context costs tokens | `song2025helpor`, `wang2025mcpbench`, `bandi2026mcpatlas`, `luo2025mcpuniverse`, `mo2025livemcpbench`, `fan2025mcptoolbench` | no spatial semantics; no code-generation arm; one attempt per task |
| **C. Autonomous GIS agents** | GIS agents are overwhelmingly **code-generating** (PyQGIS/Python); multi-agent architectures are the norm; the field is systems-first | `li2023autonomous`, `li2025autonomous`, `akinboyewa2025giscopilot`, `han2026gisclaw`, `luo2026geojson` | no controlled comparison of interfaces; success is demonstrated, not measured |
| **D. GIS benchmarks** | static text and code matching is inadequate; **execution-grounded scoring is the emerging standard**; complexity tiers matter | `yu2026geoagentbench`, `krechetova2025geobenchx`, `zhang2025geoanalystbench`, `gisagentbench2026` | one paradigm per benchmark; pass rates from one attempt; spatial predicates thin or coarse |
| **E. MCP × GIS systems** | MCP-in-GIS **exists** — as systems, and as one dataset-discovery benchmark | `gis-mcp-server-cluster-2026` (MapHub), `ogsagent2026`, `ichms2026_mcp_geodata` | discovery, not analysis; nobody evaluates the protocol as a factor |
| **F. GIScience canon** (27 entries) | the discipline's own vocabulary for correctness, error, aggregation, symbolisation, interoperability, reproducibility | `iso19157`, `ogcApiProcesses`, `harrowerBrewer2003`, `konkol2019` | says nothing about agents; it supplies the **criteria** by which an agent study is judged |
| (method) | design science as the process frame; the determinism-versus-flexibility trade-off; schema gating as a concept | `peffers2007design`, `strickland2026pareto` | no GIS instantiation of any of it |

**Two asymmetries are the whole argument:** the GIS-agent literature is *code-generation first* (eleven systems, zero protocol comparisons), and the MCP literature is *domain-general* (eight benchmarks, none with spatial-output semantics). `ichms2026_mcp_geodata` is the only crossing, and it scores dataset *discovery*.

### 1.1 What the canon licenses, item by item

The F stream is not decoration: each entry is the reason a predicate, a manifest field or a failure class exists.

| Canon | Keys | Where the thesis uses it |
|---|---|---|
| data-quality elements (completeness, logical consistency, positional, thematic, temporal) | `iso19157` | the oracle's check vocabulary is an executable instantiation of these elements (ch. 4.5) |
| metadata, lineage, CRS, spatial representation | `iso19115` | the run manifest's provenance fields (ch. 4.9) |
| geometry and topology schema | `iso19107`, `egenhofer1991` | validity and topological-relation predicates (ch. 4.5) |
| error and uncertainty in spatial data; propagation | `goodchildGopal1989`, `heuvelink1998`, `zhangGoodchild2002` | why a multi-step analytical failure is not "the last call failed" (ch. 4.7, 6.5) |
| aggregation and zonation hazard | `openshaw1984maup` | a named failure mode: fluent re-aggregation to a convenient unit (ch. 4.7) |
| uncertainty communication | `maceachren1992`, `monmonier2018` | the "plausible-looking wrong map" blast radius (ch. 6.9, 7.4) |
| cartographic correctness (classification, colour, layout) | `jenks1971`, `harrowerBrewer2003`, `slocum2009` | the presentation family's property checks (ch. 4.5) |
| semantics of spatial terms; core spatial concepts | `kuhn2005`, `kuhn2012` | why the catalogue's descriptions are a design artefact, and why the families are conceptual rather than arbitrary (ch. 4.4) |
| geoprocessing interfaces on the web | `ogcWps2`, `ogcApiProcesses` | the positioning reframe: MCP sits beside WPS and OGC API – Processes (ch. 1.1, 2.1) |
| data quality of non-authoritative producers | `haklay2010`, `goodchildLi2012`, `goodchild2007citizens` | the analyst's trust problem when an agent produces the layer (ch. 7.5) |
| FOSS-GIS landscape and workflow anchoring | `steinigerBocher2009`, `steinigerHay2009` | the substrate argument and the anchoring method for the surface (ch. 2.1, 4.4) |
| reproducibility norms in GIScience | `nust2018`, `konkol2019` | the frozen-card, manifest and never-drop-a-run design (ch. 4.1, 4.9) |
| evaluation of interfaces as a GIScience genre | `nivala2008` | the disciplinary precedent for evaluating an interface rather than a model (ch. 2.2) |

---

## 2. The empty cell

Crossing the two relevant axes leaves one quadrant unoccupied:

|  | **Code or architecture compared** | **Protocol interface as the variable** |
|---|---|---|
| **Plans, text or code scored** | `luo2026geojson` (function calling vs code inside one system), `tool_exposure_gnss_2026` (seven exposure modes, 250 tasks, **plans only**) | `wang2025mcpbench`, `bandi2026mcpatlas`, `mo2025livemcpbench` (domain-general, one interface) |
| **Executed artefacts scored** | `gisagentbench2026` (349 tasks, exact ground-truth files — **one tool paradigm, single attempt**), `geocontra2026` (contract-verified code only), `yu2026geoagentbench` | **← still empty: two paradigms, one engine, repeated. This thesis.** |

That cell is not empty by oversight. It needs an **identical engine** (so the interface is the only thing that varies), a **replicated** design (so reliability is measurable), and an **oracle per task** (so executed artefacts can be scored). QGIS supplies the first (`framing/edge-of-scope.md` §3); the harness supplies the rest; `design/corpus.md` supplies the third.

**Why the two ecosystems cannot simply be stacked.** The obvious shortcut — put the existing code-generation benchmarks next to the existing tool-agent benchmarks and compare pass rates — does not work, and it is worth saying why before a reviewer says it: they use **different tasks, different oracles and different environments**. A pass rate computed by CodeBLEU against a reference script (`zhang2025geoanalystbench`) and a pass rate computed by structural comparison against a ground-truth file (`gisagentbench2026`) are not two measurements of one quantity; they are two different quantities with the same name. Any comparison of interfaces has to be *built*: one task set, one oracle, one engine, both interfaces. That is the whole reason this thesis is an experiment rather than a survey.

The corollary is a constraint on ambition: because the cell is empty for structural reasons, filling it once does not fill it generally. One engine, one surface, one stratum of tasks. Widening any of the three is a new study, which is what chapter 7 says rather than what chapter 6 implies.

---

## 3. The gap, in five pieces

| | Claim | Nearest prior art | Why it does not close the gap |
|---|---|---|---|
| **G1** | **No cross-paradigm control**: MCP tool calls and code generation have never run against the *same backend* on the *same tasks*, scored on the same artefact oracle | `luo2026geojson` | compares two *agent architectures* inside one system, so the protocol is not isolated. Still open after `gisagentbench2026` (one 128-API harness, no code arm) and `geocontra2026` (code only, no protocol arm). **This is the thesis's main claim** |
| **G2** | **Enforcement depth is untested in GIS, on any surface.** The literature treats validation as present or absent (guardrails, contracts, gates); nobody has varied *how much* an identical surface enforces | `strickland2026pareto` (concept: schema-described vs schema-gated), `geocontra2026` (contracts around *generated code*) | the concept exists without an implementation; the one measurement puts contracts around code, not inside a tool surface, and does not compare against an ungated version of the same surface. **H2 is the empirical claim for this gap** |
| **G3** | *(Closed.)* Output correctness was under-operationalised | `gisagentbench2026` | **largely closed in August 2026**: 349 practitioner tasks with exact ground-truth files, tolerance-aware structural checks (CRS, geometry type, raster dimensions, NoData, columns) and entity F1 at IoU ≥ 0.5. What remains open is not *artefact scoring* but artefact scoring **under an interface manipulation, with repetitions**. **Do not claim this gap** — it is cited as the method's foundation, not as a hole in the literature |
| **G4** | **Reliability is reported as a mean from a single attempt** | `fan2026infofidelity` (a theoretical bound on distortion), `strickland2026pareto` (the trade-off) | distortion is bounded theoretically; no GIS study reports run-to-run determinism, error-class repeatability, or recovery after a rejection |
| **G5** | **The MCP attack surface has not been probed in a spatial toolchain** | `zhang2025msb`, `maloyan2026breaking` | injectability is established generally; in GIS the blast radius is a *plausible-looking wrong map*, not an error. **Not closed by this thesis** — the three adversarial cards are a probe, not coverage, and chapter 7 says so |

**The gap in three sentences, thesis-ready:**

> GIS agent research has converged on code generation and evaluates one paradigm at a time; MCP research has produced strong benchmarks that are domain-general and score plans or tool calls rather than executed spatial artefacts. Nobody has held the engine constant and varied the *interface* — protocol-mediated tool exposure against generated code — while scoring what lands on disk, repeatedly enough to separate capability from luck. This thesis does that, and it adds the manipulation the gap implies: on an identical surface, how much the interface *enforces*.

### 3.1 Two open questions this thesis does not turn into hypotheses

Both are measurable from the register, both are genuinely open in the literature, and neither gets a hypothesis — because a hypothesis would need a manipulation the design does not have, and a descriptive answer is better than an underpowered test.

**Repair as a mediator.** CodeAct attributes its gain to self-debugging from tracebacks, and MCPEvol shows that planning errors grow when an interface changes. Nobody has asked how much of any interface difference is *first-try success* and how much is *recovery after a rejection*. The register carries `repair_iterations` and a four-valued `detected_by`, so the decomposition is available: report the share of successful runs that were successful on the first attempt, per condition, with an interval. If the difference is concentrated in recovered runs, the mechanism is feedback; if it is concentrated in first attempts, the mechanism is the action space — and those are two different theses about why an interface matters. It stays descriptive, and it is one of the few places where this design gets a mechanism *for free*.

**The context cost of long schemas.** GIS tool schemas are long: EPSG code lists, tolerance parameters, format enums. The general stacks measure catalogue overhead in the thousands of tokens; nobody has measured what a geoprocessing surface costs to carry, or whether the cost curve bends faster there than in domains without topology. D3 already reports tokens per successful task, so the number will exist. What will not exist is the comparison across domains, and chapter 7 says so in one sentence rather than extrapolating.

---

## 4. The evidence that points the other way

This section exists because a thesis that only cites its friends is not calibrated. **Outside GIS, the literature mostly favours executable code over structured tool calls**, and that has to be stated before the result is known, or the result will look like motivated design.

| Work | Finding | Numbers |
|---|---|---|
| **CodeAct** (Wang et al., ICML 2024, arXiv 2402.01030) | executable Python actions beat JSON or text actions, and the gain **grows with task complexity** | up to **+20.7 pp** and ≈ 2.1 fewer turns on M³ToolEval; best format for 12 of 17 models. But on *atomic* calls JSON wins for closed models (GPT-4-1106: 76.7 % code against 82.7 % JSON on API-Bank), so the advantage is conditional on structure, not universal |
| **CE-MCP** (arXiv 2602.15945) | executing code *inside* MCP reduces tokens and latency at comparable quality; the differences come from the call-graph's dependency structure, not from the model; and it opens a new failure class — **syntactically valid, substantively false** | qualitative plus token and latency counts |
| **Help or Hurdle?** (`song2025helpor`, arXiv 2508.12566) | MCP *hurts* on average | **−9.5 %** accuracy overall, **−17.0 %** in code generation, at 3.25–236.5× the input tokens. **Serious methodological caveat:** the "with MCP" condition is computed only over instances where the model actually called a tool — a selection artefact. A paired design removes it by construction, which is one reason the design here is paired |
| **MCP-Atlas** (arXiv 2602.00933) | benchmarks are not saturated, but call mechanics no longer explain the outcome | **63.3 %** of diagnosed failures are *cognitive*, not tool-related; the commonest single error is "no tool called at all"; the front-runners sit at 78–82 % |
| **MCPEvol-Bench** (arXiv 2607.14642) | interface evolution degrades performance | **−13.7 pp** and **−14.4 pp** when server versions change, mostly through planning errors and redundant calls |

**What follows, and it is not comfortable.** The prior is on the side of code. So the thesis cannot claim "tools are better"; it can only claim a *conditional and mechanistic* statement: **when and why a curated, bounded, enforcing surface wins on spatial tasks — and where it stops winning.** Three consequences:

1. **A negative or null result is the likely outcome, and it is publishable.** With `mastouri2025automcp` (MCP is a thin wrap) and `fan2026infofidelity` (errors do not snowball), a null on correctness combined with a difference in *where* errors are caught is the most probable shape of the result — and it is what D1–D3 are built to record.
2. **The mechanism has to be named, not assumed.** "Tools help" is an anecdote; "enforcement catches errors before the artefact is written, and the gain scales with the expressible share" is a mechanism with a falsifier (H2, H3).
3. **The drift finding is a limitation with a number in it.** If a server-version change costs 14 pp (`mcpevol`), then a bibliography that argues for standardisation has to concede that standardisation's benefit is partly consumed by its own churn — and the thesis says so in chapter 7.

---

## 5. The six nearest neighbours, and the one sentence that separates each

1. **`diazireland2026geonatureagent` (GeoNatureAgent)** — a fixed 16-tool MCP surface, 103 tasks, nine models, a deterministic scorer, published October 2026. *They hold the interface fixed so that the model is the only variable; this thesis inverts the role of the variable.* This is the single most important boundary in the literature chapter, and it needs a paragraph, not a clause.
2. **`gisagentbench2026`** — 349 practitioner tasks, exact ground-truth outputs, tolerance-aware matching, best agent 32.7 %. *One tool paradigm, one attempt per task, no code arm; the scoring logic is adopted unchanged, the interface factor and the repetitions are added.*
3. **`geocontra2026`** — executable spatial contracts around generated code, **+26.6 pp** spatial correctness over eleven open models. *They show contracts improve code; they do not test whether contracts make code match a tool surface — and their design has no ungated control on the same surface, which is exactly H2's manipulation.*
4. **`tool_exposure_gnss_2026`** — seven exposure modes, 250 Portuguese tasks, selection F1 0.635 → 0.849. *They deliberately skip execution to isolate exposure from execution; execution is where this thesis measures.*
5. **`luo2026geojson`** — function calling against code generation inside one GeoJSON multi-agent system. *They vary the agent architecture inside a system; this thesis varies the integration method on an identical runtime and scores executed artefacts.*
6. **CodeAct and CE-MCP** — the format-versus-protocol distinction and the code-in-MCP result. *Both compare action formats outside GIS, on tasks without spatial output semantics; neither holds an engine constant, and neither scores an artefact on disk.*

**What each neighbour would predict about this result**, which is the reason the list is worth keeping: GeoNatureAgent predicts that model capability dominates and interface is a second-order effect; `geocontra2026` predicts that contracts help *code*, and therefore that N4 > N1 while K stays behind; CodeAct predicts the opposite ordering, with K ahead on every multi-step tier; `tool_exposure_gnss_2026` predicts that less surface means better selection, not better execution, and therefore no correctness difference at all; `gisagentbench2026` predicts a ceiling somewhere near a third of tasks, which is the floor-and-ceiling risk rule R-1 exists for. **Four of the five predict that H1 fails.** That asymmetry is not a reason to change the design; it is the reason the design pre-registers its interpretation rules, so that a failure of H1 is read as a result about where the value of the interface sits rather than as a broken experiment.

---

## 6. The research questions, mapped onto the ledger

The design fixes the vocabulary: **K** (code generation), **N1** (catalogue, schema only), **N4** (the same catalogue with invariants and terminal conditions) × **80 tasks** × **4 repetitions** = **960 runs**, one model, one harness, task as the unit of inference (`design/experiment.md` §0). The questions below exist so that chapter 1 asks what chapter 6 answers — nothing here is a second hypothesis list, and if this section and `design/arms-and-validation.md` §2 ever disagree, that document wins.

**Main question (RQ0).** *Does the way the same nine geoprocessing operations are exposed to an agent change the correctness, the repeatability and the cost of the artefacts it produces on an identical engine — and is any such change attributable to the enforcement boundary rather than to the protocol?*

| # | Question | Maps to | Variables | What answers it |
|---|---|---|---|---|
| **SQ1** | Does artefact correctness differ between the catalogue and code conditions? | **H1** | condition (K vs N4) → TSR | the one confirmatory test, α = 0.05 |
| **SQ2** | Within an identical surface, does correctness rise when the interface enforces invariants and terminal conditions? | **H2** | enforcement depth (N1 vs N4) → TSR | the depth curve as a trend |
| **SQ3** | Does the difference grow with the share of the task's requirements the surface can carry? | **H3** | ΔTSR × expressible share | the pre-registered interaction |
| **SQ4** | Do the conditions differ in *how* they fail and how stably they succeed? | **D1, D2** | error classes, S3, `detected_by` | distributions, κ |
| **SQ5** | What does each condition cost per successful task? | **D3** | tokens, calls, seconds ÷ successes | ratio estimator, task bootstrap |

**What is deliberately not a research question.** A sixth question — *does the protocol widen the attack surface* — is interesting and is **not answered here**: three adversarial cards are a probe, not a test, and the honest place for it is chapter 7. Nor is there a question about model capability, about agent architecture, or about a second engine: each is a factor the design freezes, and freezing is why the design can afford 80 tasks.

**Four framing rules, kept from the last round because they were right.**

1. **Every question is non-directional.** "Differs", never "improves". The direction is a prediction from the literature (§4), recorded separately, so a sign reversal is a finding and not an embarrassment.
2. **One dependent variable per question**, and where two are tempting, name the primary. SQ1 carries TSR; the predicate-level share is secondary and supporting.
3. **Pre-register the mapping** from card to family, tier and expressible share, and freeze the failure taxonomy before the first run. The taxonomy is the easiest place in the whole thesis to rationalise after the fact.
4. **State the MDE and the unit of inference inside the question's own paragraph.** A question that cannot say what would count as an answer is not a question, it is a hope.

---

## 7. What the literature does not let you claim

| Tempting claim | Why not | Say instead |
|---|---|---|
| "the first MCP work in GIS" | MapHub, OGSAgent and `ichms2026_mcp_geodata` exist; `diazireland2026geonatureagent` is a full MCP substrate | "the first controlled evaluation of the *interface* as a factor in GIS" |
| "MCP improves GIS agent performance" | `song2025helpor` (MCP can hurt), CodeAct (code wins on complex tasks); the direction is the thing under test | "we test whether it changes success, in which direction, and by how much" |
| "results generalise to Esri, PostGIS or web GIS" | one substrate, one engine, one granularity | "scoped to QGIS 3.44; the harness is substrate-agnostic and portability is shown on five GRASS tasks" |
| "our surface is production-scale" | nine operations against hundreds of real MCP tools | "a tractable surface over the traditional-geoprocessing stratum" |
| "the maps look right" | there is no aesthetic judge, by design | "the requested style properties were applied; aesthetics are out of scope" |
| "state of the art in tool use" | one model, one harness | "a capability-controlled stack, with model and harness frozen and reported" |
| "we close the GIS agent gap" | one gap, one manipulation, 80 tasks | "one of the two manipulations the gap implies" |
| "the corpus is representative of GIS work" | it is a purposive sample over one stratum, not a probability sample of anything | "a purposive, auditable corpus; the claim is about these 80 cards and the stratum they come from" |
| "the difference we find will hold next year" | `mcpevol` measures a 13–14 pp drop across a server-version change | "measured on pinned versions; drift is a stated limitation, and the mechanism is the durable claim" |

---

## 8. Where every term comes from

The point of this section is to separate **terms of my own** (which need a definition, a justification and, where the construct is hand-coded, a reliability check) from **terms borrowed from the literature** (which need a citation, and sometimes a note saying that my meaning is narrower) from **terms that are simply the vocabulary of a field** (which need one first use).

Classes: **W** — own and working · **L** — from the literature · **D** — a field's common concept (CS, GIS, geography, statistics) · **R** — the regulation's own wording.

### 8.1 Own terms (W) — six, and each one is an attack surface

| Term | What is mine | Nearest thing in the literature | Reviewer risk | What has to be added |
|---|---|---|---|---|
| **expressible share** | the **quotient construction**: requirements the surface accepts and can check ÷ all requirements of the task; seven requirement types coded per card | "constraint coverage", "interface expressiveness" — near terms, no task-level operationalisation | **highest** — a hand-coded construct invites the charge of arbitrariness | two coders on 20 % of cards, **κ ≥ 0.70**, the codebook in an appendix (`design/arms-and-validation.md` §3.4) |
| **enforcement depth** | a **graded** independent variable — the same surface at P-I, then at P-II/P-III — where the literature treats validation as present or absent | "validation levels", "defence in depth" | high — two adjacent levels can be hard to separate empirically | an explicit criterion for what separates the levels, and a written statement that **a missing difference between them is a result**, not an instrument failure |
| **gate** (a check attached to an operation) | the engineering notion moved into an **MCP operation catalogue** as a design unit | "validation gate", "CI gate", "guardrail" | medium — a reader may hear "gate" as a project stage | keep the names apart: *gate* (the check) against *decision rule* (R1–R3) and against *milestone* |
| **PCI** (in-loop catch rate) | a measure of the **ratio of detection sites**; the literature has "catch rate" for a filter, not for an interface | "interception rate", "detection rate" | medium — it depends on the error definition, so it must be computed **against the oracle** | the formula in the open, and PCI plotted against TSR in one figure |
| **`detected_by`** | a typology of **four sites**: language · own invariant · execution error · oracle. The literature has "error source" (cause), not "error location" | "error attribution" | low — it is a register field, not a theory | show on three examples that **location ≠ class** |
| **information closure** | `guard_information ⊆ agent_information` as a **condition of validity**, not an ethical posture | "information asymmetry", "privileged information" | low–medium — easily mistaken for hiding the oracle | one table: what may move from the prompt into a signature, and what may not |

**Labels, not theories** (one definition each, no defence needed): the condition names **K / N1 / N4**, the levels **P-I / P-II / P-III**, **task card**, **parity table**, **research stand** (the pinned stack).

### 8.2 Borrowed terms (L) — three of them are shifted on purpose

| Term | Source | Does it mean the same here? |
|---|---|---|
| **silent error** | software engineering ("silent failure", "silent data corruption"); chemistry, with the syntax/semantics split (arXiv 2509.23099) and *runnable but chemically wrong* (MolViBench) | **yes, sharpened**: here it is additionally *a value of the correct type and shape* — and that has to be said in the sentence that introduces it |
| **tool surface** | the agent and MCP literature | yes |
| **agent loop**, **self-correction**, **external feedback** | Huang et al. (ICLR 2024), Kamoi et al. (TACL 2024), Tyen et al. (2024) | yes — and this is the mechanism behind H2 (`design/arms-and-validation.md` §5.1) |
| **benchmark**, **dataset**, **baseline** | the agent-benchmark literature | yes |
| **TSR** | the agent literature | **no** — in the literature "success" is often judged on the trajectory; here it is judged **only on the artefact**. A footnote is required at first use |
| **artefact** | software engineering (build artefact) | **partly** — here it is "the object named in the contract on which the oracle rules"; the shift is noted |
| **contract** | design by contract (Meyer) | **yes in spirit, not in formalism** — a task contract is a checkable structure, with no claim of provability |
| **alert fatigue**, **automation bias** | medicine, decision support | yes — used as background for domain profile B (`framing/edge-of-scope.md` §2.3) |
| **pre-registration** | empirical methodology | yes |

The conclusion of the table: **three terms need a terminological footnote** — TSR, artefact, silent error — because their meaning here is narrower or wider than at source. That is the most common place where a reviewer writes "the author uses a concept inconsistently with the literature".

### 8.3 Field vocabulary (D) and regulation wording (R)

| Class | Terms used | Obligation in the text |
|---|---|---|
| **D-CS** | message envelope, schema validation, client/server, handle, hash, random seed, sandbox, JSONL register, API, JSON Schema, request–response protocol | nothing — first use, untranslated |
| **D-GIS** | CRS, EPSG, reprojection, buffer, clip, mask, union, zonal statistics, NoData, geometry validity, extent, raster/vector, layer, attribute | one sentence for zonal statistics, which is often confused with aggregation |
| **D-GEOG** | spatial unit, scale, spatial aggregation, **MAUP** | MAUP **must** appear in the limitations, because the tasks aggregate to communes and the result depends on the partitioning |
| **D-STAT** | confidence interval, power, **MDE**, ICC, McNemar, bootstrap, Holm, effect size | one sentence that ICC justifies the paired design; nothing else |
| **R** | chain of reasoning, hierarchical layout, abstract ≤ 4 000 characters, keywords, cognitive / methodological / practical contribution | use the regulation's wording verbatim — the reviewer compares against the list |

**Balance.** Six own terms and five labels; about thirteen borrowed terms, three of them shifted; roughly forty field terms; five regulation terms. **The three-question test** for every W and L term: can a source be pointed at (if not, it is mine and must say so); is my meaning identical to the source's (if not, a footnote with one example of the difference); could someone measure it the way I do (if not, what is missing is an operationalisation, not a definition).

**Three sentences for the introduction.** The term **silent error** is taken from the agent literature and sharpened here; **expressible share** and **enforcement depth** are mine, which is why their coding is checked by two coders; **TSR** is computed on the artefact only, unlike in most benchmarks, and that is said at its first use.

---

## 9. Citation hygiene before chapter 2

Two obligations, both cheap, both fatal if skipped.

**Nine works are argued from but not yet in `thesis/literature/literature.bib`.** One of them — `huang2024`, `kamoi`, `tyen` — supplies the *mechanism* for H2; `codeact`, `cemcp`, `mcp_atlas`, `mcpevol` supply the evidence *against* the thesis (§4); the rest support the "MCP benchmarks are domain-specific everywhere except GIS" argument. `TASK-10` owns the additions. A sentence in the text that cites a key absent from the bibliography is not a citation.

| Item | Status | Note |
|---|---|---|
| CodeAct, arXiv 2402.01030, ICML 2024 | peer-reviewed | safe; numbers 20.7 pp / 2.1 turns / 12 of 17 models |
| Huang et al., arXiv 2310.01798, ICLR 2024 | peer-reviewed | the self-correction numbers quoted in `arms-and-validation.md` §5.1 |
| Kamoi et al., arXiv 2406.01297, TACL 2024 | peer-reviewed | categorical conclusion; use as such |
| Tyen et al. 2024 | peer-reviewed (findings) | the localisation result |
| Help or Hurdle?, arXiv 2508.12566 | open-review preprint | **cite with the selection-artefact caveat** — it strengthens the method |
| CE-MCP, arXiv 2602.15945 | preprint (Feb 2026) | key to "the trade-off is dissolving"; label as a preprint |
| MCP-Atlas 2602.00933 · MCPEvol 2607.14642 · MCPToolBench++ 2508.07575 · LiveMCPBench 2508.01780 | preprints | numbers usable, label as preprints |
| **GeoNatureAgent 2610.09112** | GeoIndustry '26 (ACM SIGSPATIAL workshop), DOI 10.1145/3849727.3856786 | **the most important new entry** — verify the DOI and whether it is the extended version of 2606.12821 |
| GeoAgentBench 2604.13888 | preprint | 117 tools / 53 tasks / 6 domains; TAO, TIO, TEM, PEA, VLM judge |
| GeoKTools + GeoExpertQueries, arXiv 2610.15750 | preprint (Google Research, 11 Oct 2026) | check whether the scorer is public; **do not cite results from blogs** |
| GISAgentBench 2608.01645 · GeoAnalystBench (TIG 2025, 2509.05881) · GeoBenchX 2503.18129 · ThinkGeo · UnivEARTH | mixed | UnivEARTH (33 % accuracy, 58 % code failures) is known **second-hand** from a related-work section — verify at source or drop the number |
| blog posts comparing "QGIS MCP vs plugin" | **do not cite** | marketing material; the fact that it circulates may be noted without citation |

**The checklist for chapter 2.** Every work in the §1 table carries: task count, tool count, whether the interface is **fixed or variable**, and how it is scored (calls / trajectory / artefact / judge). The sentence nobody else has written — *interface as the variable, tasks and model held constant* — appears with a pointer to the works that do the opposite. GeoNatureAgent is separated by a paragraph, not a clause. The prior in favour of code gets its own paragraph and its own consequence for interpretation. No number comes from a blog or a press release.

---

## 10. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| the PB1–PB9 question table with its own DVs (TSR, OQS, PCS, PEA, ITS, ED, ADV) | `gap-and-rqs` | it was written for a four-agent, 1,800-run, Bonferroni-corrected design. The questions now map one-to-one onto the live ledger H1–H3 + D1–D3 and are numbered SQ1–SQ5 so they cannot be mistaken for a second hypothesis list |
| "38 references" as the corpus count, with the per-cluster `n` column | `gap-and-rqs`, `literature-brief` | counts change with every addition and the per-cluster figures were already stale (67 and 65 appeared in two different paragraphs). The bibliography is the count |
| the six-layer gap list plus the six "truly undecided" items (numbered 1–8 in the source note) | `gap-and-rqs`, `literature-mcp-vs-code` | two lists of the same gap, one in Polish and one in English, with different numbering. Merged into G1–G5, with G3 marked closed and G5 marked out of scope |
| the tool-*size* gap (5 vs 15 vs 30 vs 50 tools) | `gap-and-rqs`, `literature-brief` | the tool-count ladder is retired (`design/corpus.md` §11). What replaced it as the manipulation is **enforcement depth**, and G2 was rewritten to say so rather than to keep a gap the design no longer fills |
| the two "housekeeping items" that described the design as "2 front-ends × 2 models" and "a three-level surface ladder S1/S2/S3" | `literature-brief` | they recorded a design generation that no longer exists, and the instruction to "update the RQ wording when the design freezes" is discharged by §6 |
| the three sharpened title candidates | `gap-and-rqs` | titles belong in `draft/titles.md`, which is the owner of that question |
| the Polish "seven things in three layers" programme (§5 of `literature-mcp-vs-code`) | `literature-mcp-vs-code` | it was a seven-item redesign proposal, of which five items are now the design (paired oracle, interface as factor, silent-error column, cost, ITT/PP) and two are not (a second model, random catalogues). The five are stated where they live; the two are named as further work |
| the "two models of different capability" requirement, repeated in three places | several | `d-2` fixes one model; the model × interface interaction is named as the first item of further work in `design/experiment.md` §15 |
| the `origin-of-terms` class boilerplate and the D-class inventory expanded to 40 named concepts | `origin-of-terms` | the classes are stated in one line each and the D list is now a vocabulary by field rather than a 40-row table; nothing is gained by listing `raster` and `layer` separately |
| the "bibliography is now 38 → 65 → 67" narrative | `literature-brief` | three incompatible counts in one document. One line: the bibliography is the count, and §9 says what is still missing from it |

Kept, because each is the only place in the repository where its claim is made: the six-stream map with the two asymmetries (§1), the canon-to-use table (§1.1), the empty-cell quadrant (§2), G1–G5 with G3 closed and G5 disclaimed (§3), **the evidence against the thesis with its numbers and its three consequences** (§4), the six neighbours with the separating sentence (§5), RQ0 and SQ1–SQ5 mapped to the ledger with the four framing rules (§6), the claims the literature forbids (§7), the full term provenance with the three shifted meanings and the three-question test (§8), and the citation-hygiene obligations (§9).

---

## 11. Five lines, and one sentence

1. **The literature splits in two and never crosses.** GIS agent research is code-first; MCP research is domain-general; the only crossing scores dataset discovery.
2. **One cell is empty and this thesis occupies it**: two paradigms, one engine, executed artefacts, repetitions.
3. **The enforcement-depth gap is real; the artefact-scoring gap is closed** — `gisagentbench2026` already did it, so it is cited as a foundation and never claimed as a hole.
4. **The prior favours code** (CodeAct +20.7 pp, CE-MCP cheaper inside MCP, Help or Hurdle −9.5 %), which is why the claim is conditional and mechanistic, and why a null is a publishable result rather than a failure.
5. **Two terms are mine and two meanings are shifted on purpose.** Expressible share and enforcement depth need a codebook and κ; TSR, artefact and silent error need a footnote at first use.

**And in one sentence.** GIS benchmarks evaluate one interface at a time and MCP benchmarks ignore spatial semantics, so nobody has held the engine constant and varied how geoprocessing is exposed — and because the literature outside GIS mostly favours generated code, this thesis claims not that tools are better but a conditional, mechanistic statement about when enforcement on a bounded surface changes what lands on disk, with the direction, the size and the boundary stated in advance.
