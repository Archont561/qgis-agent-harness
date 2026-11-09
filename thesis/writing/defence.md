---
id: writing/defence
title: "Defence theory: what has to be known and how to say it"
type: note
status: live
language: en
question: "What has to be known for the defence, and how should it be said?"
tasks: [TASK-14]
updated_date: '2026-11-07'
---

# Defence theory: what has to be known and how to say it

> A preparatory document, not part of the thesis. Four domains × the committee's questions, each with a 20-second answer, a deeper layer, and the trap it is easy to fall into.
> Assembled from the concepts actually used in this thesis (`design/experiment.md`, `analysis/statistics.md`, `design/arms-and-validation.md`, `concept-dictionary.md`).

---

## 0. One correction before anything else

**"The IMUP problem" — I assume this means MAUP** (*modifiable areal unit problem*), Openshaw's term from 1984. I know of no "IMUP" in statistics or geoinformation; if the committee said something else, ask for a clarification rather than guessing. MAUP is in §3.3 below, together with the neighbours it is confused with (the ecological fallacy, the class-break problem).

---

## 1. Statistics

### 1.1 What a statistical test is

**Answer (20 s):** it is a procedure that, assuming some model of the world is true (the null hypothesis), derives the distribution of a statistic and then checks whether the observation is typical or extreme in that distribution. The decision is binary, but **the inference is not proof**.

**Deeper:** four elements — (1) model and assumptions, (2) test statistic, (3) the distribution of that statistic **under H0**, (4) a decision rule. A test does not say how probable the hypothesis is; it says how probable the data are **if** the null were true.

**Trap:** "the test proved that…". A test does not prove; it rejects or fails to reject.

### 1.2 What *p* means and what α means

**Answer:** *p* is the probability of a result at least as extreme as the one obtained, **given H0**. α is the threshold we fix **before** the analysis, below which we call the result inconsistent with H0. Two different things: we choose α, we compute *p*.

**Deeper:** *p* is not the probability that H0 is true, nor a measure of effect size. That is why every *p* in this thesis stands beside an effect size and a confidence interval.

**Trap:** "p = 0.000" does not exist — *p* is never zero, only below the print threshold.

### 1.3 What a *particular* test tests (the most common committee question)

| Test | What it tests exactly | The assumption that gets forgotten |
|---|---|---|
| paired *t*-test | whether the **mean difference** in pairs is 0 | pairs independent of each other; differences roughly symmetric |
| Wilcoxon (paired) | whether the distribution of differences is **symmetric about zero** | not "the difference of medians", as it is colloquially put |
| one-way ANOVA | whether **group means** are equal; F = between-group ÷ within-group variance | homogeneity of variance, normality of residuals |
| repeated-measures ANOVA | the same, corrected for dependence of measurements within a unit | **sphericity** (hence the Greenhouse–Geisser ε) |
| χ² of independence | whether **two categorical variables are independent** | expected counts ≥ 5 per cell |
| McNemar | whether, in pairs, the count of **"A only" equals "B only"** | it uses **only discordant pairs** — hence it is weak when there are few of them |
| **TOST** | whether the difference lies **inside an equivalence margin** | the margin is set from practical meaning, **not from the data** |
| mixed logistic model | whether the odds of success differ between arms, **with a random task effect** | **conditional** estimand (for a given task) |
| GEE | the same, but with a **marginal** estimand (averaged over tasks) | a correlation structure has to be chosen |
| Holm correction | not a test — **control of the family-wise error rate** | the "family" has to be defined **before** the analysis |

**Trap:** the question "what does ANOVA test?" checks whether you distinguish a *test* from a *contrast*. ANOVA says "there is a difference somewhere"; a contrast says "between which levels, and by how much". This thesis's H3 needs a **contrast of differences of differences** — the condition × expressible-share interaction — and neither ANOVA nor pairwise comparisons gives it.

### 1.4 Type I and II errors, power, MDE

**Answer:** type I — rejecting a true H0 (controlled by α). Type II — failing to reject a false H0 (controlled by power = 1 − β). The **MDE** is the smallest difference the design detects with power 0.80; here **14.0 pp**.

**Deeper:** a non-significant result **is not** evidence of no difference — it is a lack of evidence of a difference. This design therefore does not run an equivalence test at all: where a difference is expected to be small or absent, the result is reported as **undecided below the MDE**, which is the honest formulation. TOST appears in the table above because the committee may ask about it, not because the thesis uses it.

**Trap:** "not significant, so the interfaces work equally well". If the difference is smaller than the MDE, the result is **unresolved** — and that is how the thesis writes it.

### 1.5 What pairing and a random task effect buy

**Answer:** pairing (the same task in the compared conditions) removes **task difficulty** from the comparison — it cancels in the difference. A random task effect does the same inside a model and **forces the degrees of freedom to be counted from tasks, not from runs**.

**Deeper:** 960 runs are **80 independent units**, and once the intraclass correlation (ICC 0.661, design effect 3.0) is accounted for, roughly **320 independent observations' worth** of information. Counting *df* from runs is **pseudoreplication** — *p* comes out artificially small and an examiner will catch it immediately.

### 1.6 Effect size, confidence interval, estimand

**Answer:** *p* says "whether", the effect size says "how much", the CI says "with what precision". In the thesis: a difference in **percentage points**, an **OR** from the model, CIs from a **cluster bootstrap over tasks**.

**Trap of the estimand (a hard question, here with illustrative numbers):** "why is the OR 2.05 in the mixed model and 1.83 in the GEE?" Because they are **different quantities**: the mixed model gives a **conditional** effect (for a given task), the GEE a **marginal** one (averaged over the population of tasks). The attenuation is an expected consequence, not an error.

### 1.7 Multiple comparisons

**Answer:** the more tests, the greater the chance that one is "significant" by accident. Hence **one confirmatory test** at α = 0.05 (H1), the two others in a family corrected with **Holm** (H2, H3), and everything else exploratory with CIs and no stars.

### 1.8 Five things from this list to know without stumbling

1. *p* ≠ the probability of the hypothesis.
2. Non-significance ≠ no difference.
3. MDE = 14.0 pp, and what that means for the conclusions.
4. Pairing removes task difficulty; *df* from tasks.
5. TOST is a test of **equivalence**, not of difference — and this design does not use one.

---

## 2. Classifying errors

### 2.1 Why classify errors at all

**Answer:** because two failures worth the same TSR can have completely different practical weight. An error that shouts ("no such tool") is repairable; an error that stays silent (wrong CRS, and the map looks fine) is dangerous.

### 2.2 What makes a taxonomy different from a list

**Answer:** it has to be **mutually exclusive and exhaustive** (MECE): every failure gets **exactly one** class, and the number of classes is finite. The thesis has **seven classes**, plus eight CRS sub-classes, with 20 % of runs coded **blind and twice**.

### 2.3 κ — what it measures and what it does not

**Answer:** κ measures **agreement between coders** after removing chance agreement. It does not measure validity: two coders can agree perfectly and both be wrong. Hence κ ≥ 0.6 is a condition of **admission** to the analysis of D2, not a proof of correctness.

### 2.4 Silent versus loud errors

**Answer:** silent — the result looks right and is wrong (an undetected CRS error, invalid geometry). Loud — visible and named (a wrong parameter, a missing tool). In the design's expectation the catalogue concentrates loud failures on tool and parameter choice, while the code condition errs silently on CRS, geometry and aggregation. That contrast is D2, and it is the practical core of the thesis.

**Deeper:** this is the practical value of the work — **the protocol turns part of the silent error into loud error**, because it validates schema and types before anything executes. It does not remove silent error, and the thesis never claims it does.

### 2.5 ISO 19157 — spatial data quality

**Answer:** the standard distinguishes quality elements: **completeness, logical consistency, positional accuracy, attribute accuracy, temporal accuracy**. My taxonomy is **derived from it but not identical** — it additionally covers *process* errors (the wrong tool, aggregation against intent), which the standard does not describe because they concern execution rather than the dataset.

**Trap:** do not say "I apply ISO 19157". Say: "I classify errors with reference to the quality elements of ISO 19157, extended by process errors".

### 2.6 Five committee questions from this part

1. What does it mean that the taxonomy is mutually exclusive?
2. Why κ and not percentage agreement?
3. How does an error differ from a failure of the harness (a refusal, a timeout)?
4. Which error is the most dangerous, and why the silent one?
5. Where do seven classes come from, rather than four or twenty?

---

## 3. Geoinformation

### 3.1 CRS, datum, reprojection

**Answer:** a CRS is a reference system: **geographic** (degrees on an ellipsoid) or **projected** (metres on a plane). The datum is the model of the Earth the system rests on. EPSG is the catalogue of identifiers. Reprojection is not a rescaling — it requires a **transformation between datums**, and omitting it gives an offset on the order of hundreds of metres with a map that looks perfectly correct.

**Trap:** EPSG:4326 has **axis order latitude–longitude**, not longitude–latitude. A classic source of silent error, including in model-generated code.

### 3.2 Extent, IoU, topological validity

**Answer:** *extent* is the rectangle bounding the data; **IoU** = intersection ÷ union (threshold ≥ 0.95 = "the same extent"). Topological validity: no self-intersections, closed rings, no holes where there should be none. The artefact is assessed by **predicates**, not by eye.

### 3.3 MAUP — the modifiable areal unit problem

**Answer (20 s):** a source of error in which the result of an analysis depends on **which spatial units** the data were aggregated to. Two components: the **scale effect** (the same boundaries, a different unit size) and the **zonation effect** (the same size, boundaries drawn differently). Described by Openshaw in 1984.

**Why this is geography and not statistics:** the units of aggregation are **arbitrary and modifiable** — they do not follow from the nature of the phenomenon but from human decisions (administrative boundaries, grids, catchments).

**How one defends against it:** a sensitivity analysis over several partitions, hierarchical (Bayesian) modelling, working on points rather than aggregates, and an explicit statement of the unit of reference.

**In this thesis:** MAUP is not the object of study, but it is a **threat to validity** in family C (cartography), where the result depends on the number of classes and the classification method. The distinction to remember:

| Concept | What exactly is modifiable |
|---|---|
| **MAUP** | the **units of aggregation** (grids, communes, sub-areas) |
| **the class-break problem** | the **class thresholds** within one unit (quantile vs equal interval vs Jenks) |
| **the ecological fallacy** | inferring about individuals from the aggregates that submerge them |

**Trap:** "MAUP is the same as the ecological fallacy". No: MAUP is about **making** aggregates, the ecological fallacy about **inferring from** them.

### 3.4 Vector, raster, missing values

**Answer:** vector = objects (points, lines, polygons); raster = a grid of values. Operations have different defaults: a raster has a **cell size and resampling rules**, a vector has **cleaning rules and tolerances**. Missing values (*null*) are not zero — and confusing them with zero is one of the most common silent errors in aggregation.

### 3.5 The OGC stack

**Answer:** service standards: **WMS/WFS** (images and vector data), **WPS** (processes, the predecessor), **OGC API** (the REST generation: Features, Processes). **OGC API – Processes** matters because it standardises the description of a process and the **asynchronous job cycle** (execute → status → result).

**Trap:** do not say you compare MCP with OGC API. The experiment has **no OGC arm**; the relation is discussed in chapter 2 as **layers**, not as competition.

### 3.6 What "the same geoprocessing" means in two interfaces

**Answer:** `qgis_process run native:buffer` and `processing.run("native:buffer", …)` reach **the same C++ implementation**. QGIS is the only mainstream GIS environment in which one can vary **the way of calling while holding the engine fixed** — which is why QGIS suffices and a second engine (ArcGIS, GRASS) would wreck identification.

### 3.7 Five questions from this part

1. How does a geographic CRS differ from a projected one?
2. What is MAUP and what are its two components?
3. What is IoU and why a threshold?
4. Why is the artefact, and not the code, the object of assessment?
5. How does OGC API – Processes differ from WPS?

---

## 4. Computing and language models

### 4.1 What an LLM is

**Answer (20 s):** a large language model is a **transformer** network trained to predict the next token; it therefore models the probability distribution of continuations. It has **no memory between sessions**, it has a **context window** (how much text it sees at once), and its answer comes from **sampling** that distribution — hence indeterminacy and "hallucinations".

**Deeper:** there is no fact base and no rule module inside it; there are patterns from training data. That is why **tools and validation are external to the model** — and that is the whole point of the interfaces under study.

**Trap:** "the model understands". Safer: "the model predicts a continuation and selects tool calls on the basis of the schemas in its context".

### 4.2 Protocol, API, library

**Answer:** a protocol is the **rules of communication** (who sends what, and in what order). An API is the **set of operations** a system exposes. A library is code you call **in-process**. MCP is a protocol (JSON-RPC), OGC API – Processes is an API over HTTP, PyQGIS is a library.

### 4.3 What MCP actually provides

**Answer:** three things: **tool discovery at run time** (`tools/list`), **capability negotiation** at connection, and a **common tool-schema format**. The transport (stdio, Streamable HTTP) is a detail **the model never sees**.

**Trap:** "MCP is faster / more accurate". That is not the object of the thesis — it measures **what the protocol contributes and at what cost**, not whether it is better in general.

### 4.4 Tool calling versus code generation

**Answer:** these are **two levels of the same decision**: the agent either selects an operation from a catalogue and supplies arguments, or writes code that performs it. A catalogue constrains the **action space** (fewer hallucinations, fewer possibilities); code gives **full expressiveness** (and full risk).

**Trap:** this is **not** a "legacy versus modern" comparison. Code is older and still often better — in cartography it wins.

### 4.5 Sandbox, reproducibility, pins

**Answer:** the agent's code runs in a **container** with limits; artefacts are stored with **SHA-256**; model, SDK and prompt versions are **pinned and logged**. Without that the experiment cannot be reproduced — and reproducibility is a condition, not a decoration.

### 4.6 Tokens as the unit of cost

**Answer:** a token is a unit of text the model processes; the cost of a task is **input + output tokens**. Repeating the context every turn makes cost grow with the number of steps rather than the number of operations.

### 4.7 Five questions from this part

1. What is a transformer and what does it predict?
2. Why does the model not "remember" previous tasks?
3. How does a protocol differ from an API?
4. What exactly does MCP standardise?
5. Where does the token cost of a multi-step task come from?

---

## 5. Geography as a discipline

### 5.1 GIS and GIScience

**Answer:** GIS is **technology and practice**; GIScience is **the study of the principles** behind the representation, analysis and visualisation of spatial information. This thesis sits on the GIScience side: it does not build a new QGIS function, it studies **how the way tools are exposed changes the outcome of a spatial analysis**.

### 5.2 Tobler's law and spatial autocorrelation

**Answer:** "everything is related to everything else, but near things are more related than distant things". Consequence: spatial observations are **not independent**, so the classical assumptions of statistics often fail. In this thesis the problem is handled differently — by **pairing and a random task effect**, because the unit of inference is the task, not the location.

### 5.3 The map as an argument

**Answer:** a map is not an illustration — it is a **claim**, because it makes choices (class breaks, palette, extent, generalisation) that change what is read from it. That is why cartographic assessment needs **declarative predicates**, not "it looks nice".

### 5.4 Scale

**Answer:** in geography "scale" has three meanings: **measurement scale** (nominal, ordinal, interval, ratio), **map scale** (1 : 50 000), and **analysis scale** (level of aggregation). The third is what MAUP is about — and the most frequent source of misunderstanding at a defence.

---

## 6. A map of the concepts used in the thesis

| Concept | Domain | Where in the thesis | The defence sentence |
|---|---|---|---|
| MCP | computing | ch. 2, §3.2 | a protocol for publishing tools to a model |
| tool catalogue / surface | computing | §3.2 | what the agent can do at all |
| code generation | computing | §3.2 | comparison arm: full expression, full risk |
| JSON schema / validation | computing | §4.4 | checking a call before execution |
| sandbox, SHA-256, pins | computing | §4.1 | the condition of reproducibility |
| token, context window | computing | §4.11 | the unit of cost and the limit of memory |
| TSR | statistics / methodology | §6.1 | the share of runs satisfying all predicates |
| PCI | methodology | §6.5 | the share of errors caught inside the loop |
| S3, S4/S4b, S5 | methodology | §6.3 | stability, guard quality, formalisation |
| predicate, oracle, negative control | methodology | §4.2 | what "correct" means |
| paired design | statistics | §3.3 | removes task difficulty from the comparison |
| random task effect | statistics | §6.2 | *df* from tasks, not from runs |
| pseudoreplication | statistics | §3.3 | the error being avoided |
| MDE, power, SESOI | statistics | §3.6 | the threshold of detectability and of meaning |
| Holm, α, test family | statistics | §3.6 | control of false discoveries |
| conditional vs marginal estimand | statistics | §6.2 | two different quantities from one dataset |
| κ, blind coding | statistics | §4.8 | the credibility of the taxonomy |
| silent / loud error | geoinformation + methodology | §6.5 | the most important practical result |
| ISO 19157 | geoinformation | §6.5 | the data-quality standard, a point of reference |
| CRS, datum, reprojection | geoinformation | §4.2 | the main source of silent error |
| extent, IoU, topology | geoinformation | §4.2 | spatial predicates |
| vector / raster, missing values | geoinformation | §3.1 | different defaults of operations |
| OGC API – Processes | geoinformation | ch. 2 | the standard layer beneath the protocol |
| **MAUP** | geography | §7.3 (limitations) | the units of aggregation are modifiable |
| Tobler's law | geography | ch. 2 | why spatial observations are not independent |
| scale (three meanings) | geography | §3.1 | measurement / map / analysis |
| GIScience vs GIS | geography | ch. 1 | studying principles, not building functions |

---

## 7. Five questions whose answer must take 15 seconds

1. **What exactly are you comparing?** — The way the same nine operations are exposed (a protocol catalogue versus code generation) on an **identical engine**, QGIS, on the same **80 tasks** and the same oracles.
2. **What is the measure?** — The artefact: an output file checked by predicates. Not the code, not the plan, not "a nice map".
3. **What does your main test test, and what came out?** — H1 is tested by paired McNemar at task level with a mixed logistic companion; the comparison is K against N4. The design's MDE is **14.0 pp**, so a difference below that is reported as undecided rather than as a finding.
4. **Where does your result stop holding?** — In cartography: there the advantage of the catalogue is small or absent, because the limit is the **surface of the catalogue**, not the way of calling. Add one engine, one model family, 80 tasks and an MDE of 14.0 pp.
5. **What is the contribution and what is repetition?** — Repetition: tool-calling benchmarks. Contribution: **assessing the protocol on spatial artefacts, with validation as a condition and with silent error separated from loud error**.

---

## 8. Four sentences not to say

1. "I proved that MCP is better." → *"I showed that in this setup the catalogue raises correctness, and I showed where that advantage disappears."*
2. "p = 0.000, so the hypothesis is true." → *"A p below the threshold means the data are unlikely under H0; a test says nothing about the truth of the hypothesis."*
3. "The result was not significant, so there is no difference." → *"The result is unresolved below the MDE; claiming equivalence would need a TOST, which this design does not run."*
4. "This solves the hallucination problem." → *"It turns part of the silent error into loud error; it does not remove hallucination, and that was not the aim."*
