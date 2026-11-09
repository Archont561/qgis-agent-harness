---
id: writing/design-answers
title: "Six questions about the design, answered"
type: note
status: live
language: en
question: "Why nine operations, why eighty tasks, what is a card, what limits each arm, why these predicates, and what is actually measured?"
tasks: [TASK-2, TASK-3, TASK-4, TASK-5, TASK-6]
sources: []
updated_date: '2026-11-09'
---

# Six questions about the design, answered

> The six questions that come back every time the design is explained — from a supervisor, from a
> reviewer, from a colleague in the corridor — with the answer in the shape a chapter can lift.
>
> **No number here is new.** Every one is owned by a design document, quoted, and the owner is named
> in the section. Where this page and its owner disagree, the owner wins and this page is the bug.

| # | The question | The answer in one line | Owner |
|---:|---|---|---|
| 1 | Why nine operations? | Because the surface is frozen, not varied — nine atomic operations are the granularity a card can name | [`design/tool-surface.md`](../design/tool-surface.md) §1 |
| 2 | Why eighty tasks? | Because 80 × 4 × 3 is the configuration whose MDE (14.0 pp) is small enough to change a recommendation and cheap enough to author | [`design/corpus.md`](../design/corpus.md) §7 |
| 3 | What is the structure of a task, and of an operation? | A card is thirteen keys, two blocks and a reference implementation; an operation is one atomic call with a JSON schema and a written list of what it cannot express | [`experiment/tasks/README.md`](../../experiment/tasks/README.md) §1 |
| 4 | How are the operations limited for MCP and for code generation? | Nothing is withheld from the code arm; what differs is where the domain invariant lives, and that is the variable | [`design/arms-and-validation.md`](../design/arms-and-validation.md) §3.1, §5 |
| 5 | Why this many spatial predicates? | Because one predicate is not one check: five CRS error classes hide inside `crs_equal`, and a card with fewer than four checks cannot produce the failure it was selected for | [`design/correctness.md`](../design/correctness.md) §11 |
| 6 | What effect is measured, and why does it matter? | The difference in task success rate between conditions, paired at task level, with an MDE declared in advance — because the decision it informs is where the check lives, not whether a protocol is fashionable | [`analysis/statistics.md`](../analysis/statistics.md) §5–6 |

---

## 1. Why nine operations

**The number is a constant, not a variable.** Every condition runs against the same nine named
operations, described in the same words, on the same engine: `describe_layer`, `reproject`, `clip`,
`buffer`, `intersect`, `union`, `spatial_join`, `zonal_statistics`, `export`. If the catalogue changed
between conditions, the comparison would measure a bundle of interface differences and could attribute
the result to none of them — which is exactly why the earlier size ladder was retired rather than run.

**Nine is the granularity a card can name.** Smaller than an operation is a library call; larger is a
workflow, and a workflow operation is a small code generator wearing a schema — it would smuggle the
code arm's advantage into the catalogue arm. So all nine are atomic: none composes another, none takes
an expression language, none takes a script. Composition stays where it belongs, in the arm whose whole
premise is that the model writes it.

**The ninth is an export, and it is not bookkeeping.** The oracle reads a file or a handle, and export
is where georeference is most often lost — the CRS is written, or silently not written, at that moment.
Making export explicit makes the loss visible, countable and checkable.

*If pressed — "why not ninety?"* Because coverage is not the binding constraint: the corpus needs tasks
the nine **cannot** carry, and it gets them. The `expressible` code (`all` · `most` · `part` · `none`)
records what the surface can reach, family C is where it reaches least, and that is the moderator of
H3 rather than a defect of the catalogue.

*The limit.* The result is conditional on this catalogue, which is a sample of one from a combinatorial
space. That is stated as a limitation, and the ladder that would have randomised it is further work at
+300 runs.

---

## 2. Why eighty tasks

**Because the arithmetic picks eighty, and the arithmetic is a table.** The smallest difference this
design detects is

```text
MDE ≈ 3.42 · sqrt(τ² + 4950 / r) / sqrt(N)
```

with τ the between-task spread of the effect, r the repetitions per cell and N the number of cards. At
τ = 10 pp and r = 4, N = 40 gives 19.8 pp, **N = 80 gives 14.0 pp**, N = 160 gives 9.9 pp. Eighty is
the point where a difference in task success rate is large enough to change a sentence in chapter 7:
at a TSR near 45 against 55, one interface stops "half working" and the other does not.

**Tasks buy reach; repetitions buy precision only down to a floor, and the floor moves only with N.**
At τ = 10 pp the floor is 5.4 pp on 40 tasks, 3.8 pp on 80, 2.7 pp on 160. Doubling repetitions from
4 to 8 on 80 tasks buys about four points and does nothing to the floor; doubling the corpus does both,
which is why the corpus is the first thing to grow and repetitions are not.

**The binding cost is authoring, not compute.** A card is roughly a day: the prompt, the oracle, the
tolerance calibration, the negative control, the qualitative validation. That is what stops the corpus
at eighty rather than at a hundred and sixty, not the 960 runs — those are five weeks of machine time.

*If pressed — "so why not 5 pp?"* Because 5 pp needs about r = 60 at N = 80, which is 14 400 runs, and
because **no sentence in chapter 7 changes at 5 pp**. A statistically significant five-point difference
would be reported as "significant, practically unremarkable" — the weakest sentence available.

*The limit.* Eighty is not a sample; the corpus is a stratified purposive selection with a written
frame, admission rules and a register of rejects. Claims are about the class the corpus defines, and
the deep tier (T3–T4) is thin — 16 cards in the seed of which 2 are T4 — so tier-level claims are
description, not test.

---

## 3. The structure of a task and of an operation

**A card is a frozen record, not a prompt in a folder.** One YAML file per card, thirteen top-level
keys, unknown keys are errors rather than warnings — a typo that drops `expressible` would invalidate
the moderator and nothing downstream would notice.

| Part | What it fixes |
|---|---|
| `id`, `family`, `tier`, `expressible` | the four coding decisions: identity, selection axis, depth, and what the surface can carry |
| `prompt` | the only text shared verbatim by K, N1 and N4 — it names the request and the output contract, never a tool, a function or a language |
| `inputs`, `expected_artifact`, `preconditions` | what the run starts from, what it must produce, and what must be true before it starts |
| `pitfalls` | the silent errors the card was selected to provoke |
| `oracle` | a reference implementation, a seed, and at least four typed checks |
| `negative_control` | an artefact that looks right and must be rejected, plus which checks must reject it |
| `provenance`, `licence`, `created` | where borrowed material came from, and when the card was frozen |

**An operation is one call with a schema and an honest list of omissions.** Each of the nine has a
signature, a JSON schema, and a column in the catalogue table stating what it does **not** express:
`clip` has no selection expression, `buffer` has no attribute-driven width, `intersect` has no identity
or symmetric-difference variant, `export` has no symbology. The omissions are the design, because they
are what `expressible: part` refers to.

**The two structures meet in the tier.** T1 is a single expression, T2 is two to four dependent steps in
one family, T3 is six to ten steps crossing families, T4 is under-specified and has no canonical
sequence. Tier is measured from the reference solution, never counted from the number of calls the model
made — otherwise a wasteful run would look like a hard task.

*If pressed — "who writes the oracle?"* The reference implementation is written per card and pinned by
seed; the checks are declared on the card; the negative control proves at least one tolerance is not
vacuous. A tolerance nobody ever tried to break is a tolerance that has not been calibrated.

---

## 4. How the operations are limited for MCP and for code generation

**Read the question as "what is held equal", because the answer is almost everything.**

| Held identical | Value |
|---|---|
| system prompt | the same text in all three conditions, including the same instruction to verify the result before finishing |
| engine and data | QGIS 3.44 pinned by digest; the same fixtures, content-pinned by SHA-256 |
| budget | 25 turns, 10 minutes, one token budget — a run that exceeds one is flagged, not discarded |
| model and harness | one model, one agent loop, both pinned by name and version |
| prompting | the prompt never mentions tools, functions, MCP, servers, code, Python or QGIS |

**What differs is the action channel, and inside it the enforcement layer.**

- **K — code generation.** One execution tool (`run_python`) and the environment. Nothing is withheld:
  it may import `pyproj`, `shapely` or `QgsGeometryValidator`, and it may write whatever checks it
  decides to write. Whether it does is a measured quantity, not an assumption — S4 is the share of runs
  containing any check, S4b the share of those that are domain checks rather than language checks.
- **N1 — catalogue, basic.** Nine named operations with schemas. Enforcement level P-I: is the call
  well-formed. Nothing about the result is checked.
- **N4 — catalogue, extended.** The same nine operations, the same descriptions, the same schemas,
  character-identically. Adds P-II invariants (CRS, unit, geometry validity, extent) and P-III contract
  conditions, and returns a structured error naming the check that failed.

**The gate is not the oracle.** The gate is visible and checks form against declared expectations; the
oracle is hidden and checks the artefact against ground truth. If the gate could see the oracle, every
gated run would pass trivially and H2 would measure nothing.

*If pressed — "so the catalogue arm cannot write code and the code arm cannot call tools?"* Correct, and
that is the manipulation, not a confound: the arms are two ways of asking an engine to do the same
geoprocessing. The confound the design does carry is named: without a **gated code generation** cell,
the difference cannot be split into validation and representation.

*The limit.* A rejection is not a repair. A gate that refuses the only viable plan converts a wrong
answer into no answer, which is why the refusal predicate and the fuzzy tier exist and why catch rate is
reported beside correctness rather than instead of it.

---

## 5. Why this many spatial predicates

**Because "the CRS is right" is five different claims.** One `crs_equal` predicate collapses them, so
the check is split into four, each with a different place of detection:

| Predicate | What it catches | Where it is decided |
|---|---|---|
| `crs_equal(expected)` | the wrong system — the intention was wrong | after the fact, on the artefact |
| `crs_declared` | the right coordinates with no metadata written into the file or the handle | after the fact, on the artefact |
| `extent_iou ≥ 0.95`, or coordinates within tolerance | the right label on coordinates that were never recomputed | after the fact, on the geometry |
| `area_of_use` consistent with the extent | a system whose area of use cannot contain the data | **before** execution |

**Four checks per card is a floor, and two of the four must be of different kinds.** Every card carries
at least four checks, at least one of which catches a **silent** error — without it the card cannot
produce the failure it was selected for — and every card whose artefact is a layer carries at least one
geometric and one attribute check, or "wrong map, right table" scores as a success. The vocabulary is
seventeen typed predicates with arguments and tolerances; a similarity score appears nowhere, because a
score cannot be argued with in a defence and cannot be mapped to an error class.

**The count is chosen by the taxonomy, not by thoroughness.** Each predicate exists because there is an
error class that only it can see, and the seven failure classes and eight CRS classes of the register
are only recoverable if the predicates distinguish them. Compare classes, not sums: "CRS errors fell by
X" is weaker than "one class fell while another was unchanged", and with three arms and one model the
per-class profile is the only place the mechanism becomes visible.

*If pressed — "why not average the predicates into a score?"* Because a binary verdict is what a task
contract means: an artefact is correct if and only if every predicate is satisfied. The predicate-level
share is kept as a *secondary* continuous measure — it costs zero runs and carries more information than
all-or-nothing — but it never replaces the verdict.

---

## 6. What effect is measured and why it matters

**The primary quantity is the difference in task success rate between conditions, paired at task level.**
A task succeeds when its artefact satisfies every predicate on the card. The unit of inference is the
task, not the run: 960 runs are 80 tasks × 4 repetitions × 3 conditions, and with ICC(1,1) = 0.661 that
is about 320 rows' worth of independent units — never "960 observations". Because the same task runs in
every condition, its difficulty cancels exactly, and the pairing is where the power is.

| Claim | What it measures | Why the result matters either way |
|---|---|---|
| **H1** | TSR difference, K against the catalogue conditions | If it clears the MDE, "keep the domain invariant in a versioned component" is advice with a number attached; if it does not, that too is a finding about the protocol's reach |
| **H2** | the trend from N1 to N4 on an identical surface | A flat curve says the surface, not the gates, is the active ingredient — the informative null |
| **H3** | interaction with `expressible` | The difference should grow where the surface can carry the requirement and be absent where it cannot; the predicted pattern is written before the sweep |
| **D1–D4** | repeatability, failure signatures, cost per success, instrument stability | Failure signatures are a deliverable in their own right; cost per success can reverse the ranking, because a correctness win bought with three times the tokens is not a win |

**The decision threshold is declared, not discovered.** Δ ≥ MDE with *p* < 0.05 confirms; |Δ| < MDE is
**undecided**, which is reported as undecided and not as "no difference"; Δ ≤ −MDE refutes. At
τ = 10 pp, r = 4 and N = 80 that threshold is 14.0 pp, and it was written into the pre-registration
before a single run — an MDE computed afterwards is an excuse.

**Why this matters more than "does MCP help".** The claim was never that a protocol is good. It is that
in geoinformatics the failure modes are *silent* — a layer in the wrong system looks perfect — and that
the difference between the interfaces is **where the domain invariant is kept**: in the model's context,
rebuilt at every attempt, or in a versioned component written once by a human and executed identically
every time. That sentence is testable, falsifiable, and useful to whoever has to decide where to put the
check in their own harness.

*If pressed — "what if the difference is nil?"* Then the honest conclusion is that standardising calls
does not translate into execution correctness in this task class, and that the value of the surface is
engineering and audit: provenance completeness, surface versioning, portability across clients. That
outcome was written down before the measurement so that it cannot be reinterpreted afterwards.

*The limit.* One model, one engine, one server, one agent loop. The claim is about this configuration;
the missing cells — a cross-model interaction, a gated code generation arm, a randomised catalogue — are
named in [`framing/edge-of-scope.md`](../framing/edge-of-scope.md) with what their absence costs.
