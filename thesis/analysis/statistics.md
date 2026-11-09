---
id: analysis/statistics
title: "From runs to claims: hypotheses, power, analysis"
type: note
status: live
language: en
question: "Which test decides what, with what power, and what may not be claimed afterwards?"
tasks: [TASK-1, TASK-12]
sources: [hypothesis-testing.md, what-is-mde.md, sample-size.md, pingouin.md, analysis-automation.md, confounders.md]
updated_date: '2026-11-07'
---

# From runs to claims: hypotheses, power, analysis

> Which test decides what, with what power, and what may not be claimed afterwards?
>
> The bridge between the series and the sentences of chapter 6. It is written against the **live design only** — three conditions, 80 tasks, r = 4, 960 runs (`design/experiment.md` §0) — and every number below is either computed for that design or carries the source it came from. Where an older generation of the plan said something else, §12 records the cut and the reason.
>
> Pruned and translated 2026-11-07 (`TASK-21`): 8,088 → 6,662 words, six source notes → thirteen sections.

---

## 1. The short answer: five levels

Testing here is not one test. It is five levels, and the first is not a test of a hypothesis at all:

| Level | What is settled there | Where in the thesis |
|---|---|---|
| **0. Instrument qualification** | is there anything to measure with | §4, gate G2 |
| **1. Unit of inference** | how many independent observations exist | §4.7 |
| **2. Test hierarchy** | how much type-I error may be spent | §3.4, the pre-registration |
| **3. The test for each claim** | which model, which decision rule | §6.1–6.8 |
| **4. The three-valued verdict** | confirmed / refuted / **undecided** | §6.11 and §7 |

The feature that decides whether the chapter is defensible: **an insignificant result is not a zero result.** It is either *undecided* (when |Δ| is below the MDE) or *unresolvable in principle* (when the design has no contrast that could answer the question). There is no third category called "no difference", and the phrase does not appear in the thesis except inside a rejected sentence quoted as such.

---

## 2. Level 0 — before any test: is the oracle an instrument?

A hypothesis test on a broken meter is not a test. Before the series, gate **G2** requires:

1. **Every card's reference artefact passes** — all predicates satisfied, so the oracle measures what it says it measures.
2. **Every card's deliberately broken artefact fails** — a shifted CRS, a missing attribute, the wrong geometry type, an array without a system declaration.

The first half alone is a trap: an oracle that always returns *pass* passes it too. The second is the negative control, and without it chapter 6 is worthless — the more so because the artefacts this thesis scores are exactly the kind that *look* right.

Three further admission conditions, all reported in §4:

- **Oracle repeatability** — the same artefact scored twice gives the same verdict; the check is cheap and it catches state leaking into scoring.
- **κ ≥ 0.6** on the failure taxonomy, double-coded blind on **20 % of runs** (`design/experiment.md` §8.4). Below that the taxonomy is a hypothesis, not a measurement, and D2 cannot be tested at all.
- **Baseline TSR ≥ 10 %** on the cards the surface covers, per rule R-1. At zero success there is no variance to explain and nothing to test; at either extreme the design is at a floor or a ceiling and the outcome is W6.

A fourth quantity is estimated before the series and is not a pass/fail at all: **the between-task variance τ**. It sets the MDE (§6), so it is estimated in the pilot and the 14.0 pp figure is restated with the observed τ rather than the assumed one (`design/experiment.md` §16, item 4).

---

## 3. Level 1 — the unit of inference is the task, not the run

This is the most common error in work of this kind and the easiest objection for a reviewer to make. With 80 tasks × 3 conditions × 4 repetitions there are 960 runs — and **80 independent units**.

The arithmetic of the correction, since it must appear in chapter 3 rather than in an appendix:

- The **intraclass correlation** of correctness across repetitions of the same task is **ICC = 0.661** (`design/corpus.md` §7.2).
- The design effect is `1 + (r − 1)·ICC`: at r = 4 it is **3.0**, at r = 16 it would be **10.9**.
- So 960 rows are worth roughly **320 independent rows** — and the claim is about 80 tasks, not about 960 anything.

Consequences, all of which are decisions and not preferences:

- **Primary model**: a mixed logistic model on the binary predicate outcome, with a **random task effect** and condition as a fixed effect. Degrees of freedom come from the number of tasks.
- **Primary confirmatory test**: **McNemar on the paired task-level outcome**, which uses the pairing directly and needs no distributional assumption about the between-task variance. The mixed model is the covariate-carrying companion and the second opinion, not a substitute.
- **Repetitions do not buy power in the sense of *n*.** Four repetitions buy *precision* on the secondary measures (error-class repeatability, `PCI`, cost) and insurance against single-run noise. Said plainly in §4.7, because at first hearing it sounds like a contradiction: more runs, no more independent observations.
- **Never call the run count a sample size.** "960 runs" describes the work; "80 tasks" describes the inference. The two numbers appear in different sentences.

There is a second-order version of the same trap, which the pairing makes tempting: with paired tasks, one can compute a difference for each task and then test 80 differences. That is correct, and it is *still* 80 units — the temptation is to weight those differences by their four repetitions as if they were 320. They are not; the repetition average is one number per task, which is exactly why McNemar on the majority outcome and the mixed model on all four can disagree slightly and why the disagreement must be reported rather than resolved by choosing the friendlier one.

---

## 4. Level 2 — the hierarchy, and how much error may be spent

| Role | Claims | α |
|---|---|---|
| **one confirmatory test** | **H1** — the way the nine operations are exposed changes artefact correctness (N4 against K) | **0.05** |
| **Holm within the family** | **H2** (depth curve), **H3** (interaction with expressible share) | 0.05, corrected |
| **descriptive, no stars** | D1 repeatability (S3, predicate-level classes), D2 failure signatures, D3 cost per success, S4/S4b, S5 | intervals only |
| **not tested at all** | the three adversarial cards, the plateau point as advice, the platform slice | reported as numbers |

**Why the hierarchy is not alpha-laundering.** The alternative — four hypotheses at α = 0.05/4 = 0.0125 each — buys a smaller per-test error at the price of an MDE roughly 12 % larger for everything, including the one comparison the thesis is about. The hierarchy instead spends the error where the claim is: one test at 0.05, and everything else demoted *in wording* as well as in arithmetic. What makes that legitimate is the last column of §5: each demoted claim has a written-down interpretation and a written-down falsifier, so nothing is being tested quietly.

Two rules that come from `design/arms-and-validation.md` and are cheap to obey:

1. **State the direction separately from the hypothesis.** H1 is two-sided on purpose, and the direction (N4 > K) is a prediction from the literature recorded next to it. An opposite result is then a result, not an embarrassment, and there is no temptation to rephrase after seeing the sign.
2. **Count the tests before the series.** Two confirmatory-family tests (H2, H3) plus one confirmatory test plus five descriptive measures plus two sensitivity analyses is the whole budget. A chapter 6 with eleven starred p-values means either the pre-registration was ignored or the family was defined after the fact.

---

## 5. Level 3 — the test for each claim

| Claim | DV | Test or model | Decision rule | An opposite result is also a result, because… |
|---|---|---|---|---|
| **H1** — exposure changes correctness | TSR, binary per task | paired McNemar at task level (primary) + mixed logistic with random task effect (companion); difference in pp with a task-bootstrap CI | Δ ≥ MDE **and** *p* < 0.05 → confirmed; \|Δ\| < MDE → **undecided**; Δ ≤ −MDE → refuted (W5) | the prediction was weak and two-sided: the literature reports MCP sometimes hurting |
| **H2** — correctness rises with enforcement depth | TSR at N1 and N4, same surface | **linear contrast N1 → N4 plus a plateau fit**, as a *trend*, not a pair of tests | monotone rise with a CI excluding zero → depth matters; flat → gates inert (W2/W4) | a flat curve is the informative case: it says the surface, not the gates, is the active ingredient |
| **H3** — the difference grows with the expressible share | TSR difference per card, moderator coded per card (all / most / part / none) | condition × share interaction, with the predicted *pattern* stated in advance | growing difference where the surface can carry the requirement; difference in catch rate but **not** in correctness where it cannot | a flat interaction across the range, or a correctness difference on `none` cards, falsifies the mechanism rather than the measurement |
| **D1** — repeatability | error-class distribution, S3 (share of tasks whose dominant class ≥ 75 % of their failures), predicate-level identical/equivalent/divergent over the four repetitions | contingency over classes + S3 as a proportion with a task-bootstrap CI | different distributions → the interfaces differ in *stability*, not only in level | equal distributions mean the interfaces differ only in the mean, which is a cleaner claim than the alternative |
| **D2** — failure signatures | seven failure classes, eight CRS classes, `detected_by` (four values) | distributions + **κ** on the 20 % blind double coding | different signatures (silent CRS vs a loud wrong tool choice) | the taxonomy is the deliverable either way; uniform signatures mean the interface does not change *where* things go wrong |
| **D3** — cost per success | tokens, calls, seconds **per successful task** | **ratio estimator + task-level bootstrap** | the cost ranking reverses the TSR ranking in ≥ 1 family | no reversal means one interface dominates, which is also a result |
| **D4** — the instrument is stable | predicate verdicts, artefact hashes, manifest fields | agreement across repetitions and across blocks; digest comparison | stability is a precondition: failure stops the series | D4 is reported as a condition, never as a finding |

Three subtleties that have to be defensible at the defence:

- **D3 is not a difference of means.** Cost per success is a ratio of two random variables, and the delta method lies about its variance at moderate n; intervals come from the task-level bootstrap. When a condition has zero successes the value is `NaN`, not zero, and the condition leaves the ranking.
- **`detected_by` is the most diagnostic field in the register.** With four values — language, own invariant, execution error, oracle — "the model wrote a check, but a language check" is distinguishable from "the model wrote nothing". Collapsing that column into a boolean destroys the thesis's most interesting secondary result.
- **Standardisation cannot be measured as variance.** The variance of a binary outcome is a function of its mean, so higher repeatability *entails* lower variance with no behavioural change; a variance test would "detect" standardisation it never measured. That is why D1 is `S3` and the predicate-level classes, and why a variance test appears nowhere in this document.

---

## 6. Level 4 — the MDE, and when "no difference" may be said

**Definition.** The MDE is the smallest difference the design has ~80 % chance of detecting as significant at the stated α. Three properties that matter more than the definition:

1. **It is a property of the design, not of the world.** The same 10 pp effect is significant with 300 tasks and undecided with 30.
2. **It is declared before the measurement.** An MDE written into the pre-registration is a commitment; an MDE computed afterwards is an excuse.
3. **It is a decision threshold, not a truth threshold.** Below it, the honest sentence is "this design does not resolve differences this small", never "there is no difference".

**The closed form for this design** (`design/corpus.md` §7.2):

```
MDE ≈ 3.42 · sqrt( τ² + 4950 / r ) / sqrt(N)
```

where `τ` is the between-task standard deviation of the difference in pp, `r` the repetitions per cell and `N` the number of tasks. The constant 4950 is `p(1−p)·2·10 000` at p = 0.45 — the binomial part — and the `τ²` term is what pairing does *not* remove: the task × condition interaction.

**Live numbers.** With τ = 10 pp, r = 4, N = 80: **MDE = 14.0 pp** at 80 % power. The sensitivity that must be shown next to it, because τ is estimated and not known:

| τ (pp) | MDE at N = 80, r = 4 | MDE at N = 80, r = 8 | MDE at N = 80, r = 16 |
|---:|---:|---:|---:|
| 5 | 12.2 | 10.3 | 9.5 |
| **10** | **14.0** | 11.8 | 10.9 |
| 15 | 14.7 | 12.4 | 11.4 |
| 25 | 17.9 | 15.1 | 13.9 |

Two things the table says at once: **the MDE is insensitive to τ at r = 4** — most of it is the binomial part, not the task interaction — and **repetitions are a weak lever** once the design is at r = 4 with 80 tasks: doubling them buys about 2 pp. That is the opposite of the intuition "add runs", and it is the reason the run count is not the number to argue about.

**The per-cell trap.** The MDE above is for the whole corpus. The temptation is to read a per-family or per-tier difference off the same table, and the resolution collapses with the cell:

| Tasks in the cell | MDE at r = 4 |
|---:|---:|
| 5 | **55.9 pp** |
| 13 | **34.7 pp** |
| 40 | **19.8 pp** |
| 80 | **14.0 pp** |

So the family P/A/C split (14 / 13 / 13 of the 40-card seed) cannot carry a correctness claim at all; tiers T1–T4 with 5, 19, 14 and 2 cards can carry one only at T2. This is why H2 and H3 are stated as *trends and interactions over the whole corpus* and why the family split enters chapter 6 as description rather than as test.

**Why the target is not 5 pp.** The algebra says 5 pp is reachable without a single new task: at N = 80 it needs ≈ r = 60, i.e. 14 400 runs. Three things break before the arithmetic does:

1. **Throughput.** The series is about five weeks of machine time at 960 runs; 14 400 would be most of the remaining project, sweep and analysis together.
2. **Drift.** A sweep stretched that far measures different models in the first block and the last; repetitions from week 1 and week 20 are not exchangeable, and the whole power calculation assumes they are.
3. **The pseudo-replication temptation.** At 60 repetitions it becomes almost irresistible to count degrees of freedom from runs — the exact error §3 exists to prevent, and one that would *manufacture* significance at any MDE one likes.

And the substantive argument, which settles it: **there is no sentence in chapter 7 that would change at 5 pp.** At a TSR near 45 % versus 55 %, neither interface stops "half working", no recommendation reverses, and no claim about the mechanism changes form. The goal of H1 was never "is there any difference" but "how large, and for whom" — and 14 pp is the resolution at which the answer changes a recommendation. A 5 pp result would be reported as "statistically significant, practically unremarkable", which is the weakest sentence available to chapter 6.

**Four levers cheaper than runs.** Before paying in repetitions:

| Lever | Effect | Cost |
|---|---|---|
| **McNemar on the paired task outcome** instead of a two-sample comparison of proportions | uses the pairing at the level where the inference is made — a real power gain for zero runs | 0 runs, one line in the pre-registration |
| **The predicate-level outcome** (share of satisfied predicates) as a secondary continuous measure | carries more information than all-or-nothing; the data are already in `checks.jsonl` | 0 runs |
| **A pre-registered subgroup** (family C, tiers T2–T3) declared as exploratory | an MDE computed where the effect is larger by construction | 0 runs, but it must be written **before** the sweep |
| **Task templates with two instances per unit** — 80 units, 100 instances | lowers within-cell heterogeneity, so it lowers τ, so it lowers the MDE without adding units | corpus design, not runs |

The first three are free and are the honest answer to "can the conclusions be stronger": yes, through a better estimator, not through more runs.

---

## 7. Level 5 — what else has to hold for a sentence to survive

Chapter 6.11 is not decoration; it is the durability condition for every sentence in 6.1–6.8. Five analyses, each of which can kill a specific claim:

| Sensitivity analysis | What it would invalidate |
|---|---|
| moving the tolerance table within the bounds declared before the sweep | a result that depends on the choice of threshold (`extent_iou ≥ 0.95`, area tolerance) |
| excluding runs whose instrument integrity is violated (input hashes changed, writes outside the output directory) | harness failures dressed up as an interface effect |
| **intention-to-treat against per-protocol** (`design/experiment.md` §9.8) | a difference produced by the exclusion rule rather than by the conditions; if the two disagree, the disagreement is a finding about parity |
| splitting the series at a drift point | a series measuring two model versions as if they were one |
| weighted against unweighted TSR over families | an artefact of the corpus composition, since P / A / C are not equally sized |

The fourth is the one to plan for rather than hope against: the runs are blocked by week precisely so that the split, if it is needed, has a clean boundary.

---

## 8. What is not tested, and why it is not a gap

- **The three adversarial cards** — reported as numbers with exact intervals, not tested. At that n every test would be theatre, and `design/correctness.md` states the security surface as future work.
- **The plateau point of the depth curve** — reported as practical advice ("beyond N1 the marginal gain is small"), not as a causal claim. Two points do not identify a plateau; the plateau *fit* is a description of the same two points.
- **The platform slice** — a limitation, not a hypothesis (§11.1).
- **D4, the stability of the instrument** — a precondition of measurement. It belongs in §4, not in the table of claims, and a "significant" D4 would mean the meter is broken.
- **Model ranking, harness ranking, a second engine, gated code generation** — all outside the design, all named as further work. This is the boundary drawn in `framing/edge-of-scope.md` §4; a test of a cell the design does not contain would be a test of nothing.

---

## 9. The software: what computes what

The division of labour was checked by running it, not by reading documentation, on a run manifest of 4 769 synthetic rows before the pre-results scaffolding was removed on 7 XI 2026. What survives is the split, the trap, and the dependency decision.

| Layer | Tool | Why |
|---|---|---|
| load, filter, aggregate, the coverage matrix `task × condition × repetition` | **pandas** | trivial in `groupby`/`pivot_table`; deterministic given a seed |
| artefact scoring (predicates, hashes, tolerances) | own scorer | it is the layer *before* statistics and the one the thesis is about |
| **paired tests, McNemar, Wilcoxon as a robustness check** | **`pingouin`** | `pg.ttest(paired=True)`, `pg.chi2_mcnemar`; McNemar checked against `b = 1, c = 7` → asymptotic *p* ≈ 0.034, exact 0.070 |
| **Holm** | `pg.multicomp` | identical to a hand-written Holm on the same p-values |
| **ICC / share of task variance** | `pg.intraclass_corr` | this is where ICC = 0.661 and the design effect of 3.0 come from |
| effect sizes and Bayes factors | `pg.compute_effsize`, `pg.bayesfactor_ttest` | cheap to report next to *p*, and BF₁₀ is a better answer to "is this undecided or zero" |
| **the confirmatory model with a random task effect** | `statsmodels` — **GEE with the task as cluster**, family binomial | three lines instead of forty; see the estimand note below |
| **the contrast that answers H2 and H3, cost per success, error classes, κ, cluster bootstrap** | own code | `pingouin` has no contrast-of-contrasts, no ratio estimator and no bootstrap |

**The trap, stated once and remembered.** For a two-level condition `pg.pairwise_tests` returns one contrast, and it happens to be the right one. The moment a third level exists it returns three, all of which can be significant while the question of interest — is the *increment* shrinking — is undecided. A worked case from the synthetic manifest: pairwise tests gave *p* = 0.0018, ≈ 0 and 0.0061 for three pairs, while the difference of differences was **+4.4 pp, CI [−7.7, 16.6], undecided**. Both statements are true and only one answers the hypothesis. The pre-registration therefore fixes **the shape of the contrast**, not the name of the test — otherwise a correct analysis of the wrong question passes every check.

**The estimand has to be named.** GEE gives a **marginal** effect (averaged over the population of tasks); a mixed model gives a **conditional** one (for a given task). On the same synthetic data: β = 0.603, OR = 1.83 (GEE) against β = 0.717, OR = 2.05 (Gauss–Hermite quadrature). The attenuation factor 1.19 is the expected one for a between-task σ of 0.93, so the difference is not an error — it is a different estimand. Chapter 6 says which is reported; the conclusion is the same either way.

**Dependencies: conda-forge, not PyPI.** `pingouin` is on conda-forge, and `pixi.toml` reserves `pypi-dependencies` for what is not (`alint`, `codecov-cli`, the local `experiment` wheel). Beyond consistency there is a reason specific to this environment: the wheel ships its own BLAS, and in a container that also holds QGIS 3.44 and geopandas, a second `libopenblas`/`libstdc++` is a classic source of import failures in Qt plugins — a fault that appears at a random point and costs hours. Same version either way (0.7.0), so the risk buys nothing. A useful side effect: `pingouin` pulls `statsmodels`, which is what makes the GEE route available at all.

Two remaining rigour items: pin the version (`>=0.7.0,<0.8`), and record it in the manifest's `analysis_env` field, because `BF₁₀` is version-dependent while `pg.tost` and `pg.multicomp` are not. And note the installation route: `pixi run python -m pip install` does not work in this environment — there is no pip — so the only path is a `pixi.toml` edit and a re-solve. Anyone who skips that has the package locally and not in CI.

---

## 10. How much of the analysis can be automatic

Three levels, and the boundary between them is the boundary between arithmetic and authorship:

| Level | Content | Automation |
|---|---|---|
| **A — numbers** | aggregation, coverage matrix, TSR, cost per success, contingency tables, bootstrap, contrasts, Holm | **100 %** — pandas and scipy, deterministic for a given seed |
| **B — verdicts** | confirmed / refuted / undecided | **100 %**, but only because the rules were frozen in the pre-registration. The script does not judge; it applies |
| **C — interpretation** | what the result means for the thesis, whether a chapter-7 sentence may stand unqualified | **none** — and this is structural, not technical |

Sentences in a generated report can be automatic in exactly one sense: they are **templates parameterised by computed numbers and branched on the result**. That is not "AI interprets the results"; it is `if/else` over an interval. The distinction matters because the first would be irreproducible and indefensible.

**Cases the analysis must recognise, or admit it does not.** A case not on this list is not handled, and the report says so:

| Case | Detection | Behaviour | Automatic? |
|---|---|---|---|
| duplicate `run_id` | `duplicated` | exclude, with the rule and the reason recorded | yes |
| missing artefact / dry run | `status` | exclude; `result.json` absent means incomplete | yes |
| **empty cell in the coverage matrix** | coverage ≠ expected | **provisional verdict** plus a warning; nothing is imputed | yes (the decision is "run it") |
| exclusions above 5 % in a condition | share per condition | escalate; the report is marked as at risk | yes |
| context truncation | `stop_reason == "length"` | **not** excluded — enters the sensitivity analysis | yes |
| no successes in a condition | `succ == 0` | cost per success = `NaN`, not 0; the condition leaves the ranking | yes |
| low agreement | `kappa < 0.6` | D2 "without basis"; the coding is repeated | yes |
| a difference within 25 % of the MDE | \|Δ\| < 1.25 × MDE | flagged "borderline", with a prescribed cautious wording | yes |
| a borderline result after Holm | 0.01 ≤ p_adj ≤ 0.06 | "borderline after correction", no categorical sentence | yes |
| a changed model or library version inside the series | distribution of `model_version` | split into blocks — **needs an author decision** | partly |
| the family-C interval covering zero | a test on the subset | **switches** the chapter-7 sentence to its "boundary of the claim" version | yes |

Four things turn a report into an instrument, in order of importance: **schema validation of the manifest** (otherwise a missing column is silently counted as `NaN`), **tests on dummy manifests covering every case in the table above** (a demonstration that the handling works, not that it happened to work), **a hash of the report output** (same manifest plus seed gives the same file), and **the rules in one versioned file** (`rules.yml`: MDE, α, margins) so that a post-hoc change to a rule shows up in a diff.

**What the automation cannot do**, and why the boundary is where it is: it cannot decide whether a claim may be unconditional (it can only select between two prepared sentences); it cannot add a condition or a task after a look at the results, because that is a decision requiring a log entry and the log is a document, not a side effect; and it cannot judge whether a result matters to anyone who writes an MCP server — that is literature and practice, not a confidence interval. The recognition rule is one line: **a number that can be recomputed from the manifest is automatic and must be reproducible; a sentence about meaning is the author's comment and must be marked as such.**

---

## 11. Confounders: what is frozen, what is varied, what is blocked

One governing principle: **what you do not study, you freeze and report; what is theoretically interesting you turn into a factor; what can be neither frozen nor studied you treat as a variance component, not as a blemish.**

| Strategy | When | What it buys |
|---|---|---|
| **freeze** | factors with no theoretical role in this question, expensive to vary | removes variance, **narrows the claim** to one environment |
| **vary** | factors about which something is to be said | variance becomes a result; costs runs |
| **block or randomise** | factors known but not tied to a condition | variance enters the error, not the bias |

In a comparative design, 90 % of the trouble disappears through one habit: **inside a block, everything is identical except the condition** — the same task, the same data, the same model, the same harness, the same limits, the same order drawn at random.

### 11.1 Platform

The platform does influence the result, but not where one expects: through **tool availability** (much agent tooling assumes a POSIX shell), **filesystem semantics** (case-insensitivity, `MAX_PATH`, file locking, and the `-wal`/`-shm` behaviour of GeoPackage under concurrent access), **numerics** (GEOS and PROJ can produce coordinates that differ slightly through FMA and thread order — hence tolerances, never byte equality), **error text** (paths and messages differ, so the agent repairs differently — a real platform effect, not noise), and **speed** (affects the time metric, not correctness).

**Decision: frozen** — one Linux image pinned by digest, headless QGIS 3.44, one container per run. **What may be claimed:** "in a Linux container", with the invariance check named as the cheapest way to widen it (about 60 runs on a second platform, reported as agreement of verdicts, not as a study). If it is not run, the limitation says so in one sentence.

### 11.2 Model

The largest of the three influences, and the one that hits the weakest leg of the project ("this is a property of one model"). **Decision: fixed** (`d-2`) — one model, pinned by name, version and date, with the digest in the manifest. Three consequences are written down rather than argued away:

1. The claim is "under a model capable of the task" — the weakest available claim, and an honest one. It is enforced by the qualification rule: baseline TSR must clear 10 % on the covered cards, or the measurement is of the model's incompetence, not of the interface.
2. **A model × interface interaction is the most interesting absent result** in this project, and it is exactly what a reviewer will ask about. It is named as the first item of further work, with the arithmetic that makes it expensive (a second model doubles the series before it says anything about the interaction).
3. **Drift is treated as a threat, not as a factor**: blocking by week, digests in the manifest, a drift patch repeated at the end with at most two tasks differing between the first and last block.

### 11.3 Harness

The most "hidden" factor: two agents with the same model and the same server behave differently because of things invisible in a publication — the system prompt, the call loop, the retry policy, context compression, how tool schemas are rendered, how tool results are truncated, the token budget, the sandbox policy.

**Decision: one pinned harness** (`d-4`). Crossing it would multiply the series for a claim the thesis does not make, and it is also the reason the "one CLI" objection is answered in the limitations rather than with a doubled design. What the harness must nonetheless satisfy — as an **admission criterion checked in the pilot**, because a harness that cannot run all three conditions makes the sweep invalid:

| Capability | Why it is critical |
|---|---|
| code execution / shell access | without it the K condition does not exist |
| writing files to a named directory | without it no artefact exists to score |
| MCP transport (`stdio` or HTTP) | without it N1 and N4 do not exist |
| configurable turn, time and token limits | without it budgets cannot be equal across conditions |
| a single system prompt, editable but identical | without it the comparison measures the prompt (turn 86) |

Three alignment duties: the same prompt template, the same schema text, the same limits, the same output directory, the same sandbox, with extras disabled (auto-retry, planning modes, memory, reflection); **report what cannot be aligned**; and **measure the context actually delivered, not the assumed one** — log `tokens_in_system` per request, because a surface that one harness truncates is no longer the manipulation it claims to be.

### 11.4 The factor register, for chapter 3

| Factor | Influence | Decision | What may be claimed |
|---|---|---|---|
| Platform | medium (numerics, paths, tool availability) | **frozen**: Linux + container | "in a Linux container"; invariance check named |
| Model | **large** | **fixed** + qualification rule | "under one model capable of the task"; interaction named as further work |
| Harness | **large** | **fixed**, one, pinned; capability table checked in the pilot | "with one pinned harness"; the "one CLI" objection answered in the limitations |
| Surface composition | **large** | the treatment itself: same nine operations in N1 and N4, down to the wording | "for this surface"; the anonymised-catalogue control guards authoring bias |
| Order, cache, warm-up | small–medium | **blocked**: rotation of conditions per task, a fresh container, cache off | no order effect |
| Library versions (QGIS, GDAL, GEOS, PROJ) | small but silent | **frozen** by digest; tolerances instead of byte equality | reproducibility; D4 measures the rest |
| Turn / time / token limits | medium | **frozen and equal** across conditions (A4) | comparability of budgets |

### 11.5 Thirty seconds at the defence

> The platform is frozen, because a cross-platform replication would cost the whole budget and the thing I am studying is the interface, not the operating system — but the invariance check is named and costs sixty runs. The model is fixed in the main comparison, because doubling it would double the sweep before it said anything about an interaction; instead the claim is scoped to a model capable of the task, and the interaction is the first item of further work. The harness is fixed and pinned, and I align everything that can be aligned — the prompt, the budgets, the limits — and report what cannot. The condition is the only thing that moves between the arms of a block.

---

## 12. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| the 40 × 8 design, its 640 runs, its MDE table (0.574 … 0.880) and its recommendation to move to 40 × 16 or 40 × 60 | `hypothesis-testing`, `what-is-mde`, `sample-size` | the live design is 80 tasks at r = 4, 960 runs, MDE 14.0 pp at τ = 10. Every number computed for 40 × 8 was replaced rather than carried |
| the "MDE 20–25 pp at 50 tasks" figure and the α = 0.0083 (Bonferroni/6) discussion | `hypothesis-testing`, `sample-size` | both belong to a retired generation; the live hierarchy spends 0.05 once and Holm on a two-test family |
| **TOST, the ±20 pp margin and its sample-size table** | `hypothesis-testing`, `sample-size` | the equivalence claim existed to rescue the 2 × 2 with a gated-code cell, and that cell is not in the design (`framing/edge-of-scope.md` §4.2). A test with no corresponding contrast is a rule without a subject |
| the 2 × 2 interaction cost analysis ("~140 tasks for a 20 pp interaction") | `sample-size` | same reason: there is no interaction contrast in the live design, only the depth curve and the expressible-share moderator |
| **the tool ladder L1–L4 and the randomised catalogue of 100 tools in K = 5 draws** | `sample-size` | the tool-count ladder is retired with `min_surface`; the surviving control is the anonymised catalogue (`design/corpus.md` §10), which tests the same worry in one arm rather than five |
| the hypothesis list H1–H7 with its per-hypothesis DVs | `hypothesis-testing` | the live claims are H1–H3 plus D1–D4, and they have one owner (`design/arms-and-validation.md`). Two numberings of the same claim ends in two reference systems |
| the sample-size tables of "tasks needed for 80 % power" at α = 0.0083 | `sample-size` | superseded by the closed form with τ, which is what the design actually uses; the tables answered a different design's question |
| **the model sensitivity control (3 models × 15 tasks, +180 runs) and the platform invariance control (+60 runs)** as plan items | `confounders` | neither is in the 960-run series; both survive as one-sentence limitations with their cost named, which is honest and cheaper than pretending they are scheduled |
| two front-ends as a crossed factor, and the front-end affordance table as a *comparison* | `confounders` | one pinned harness (`d-4`); the affordance table survives as an **admission criterion** for that one harness |
| the six-subsection `pixi add` versus `pixi add --pypi` investigation (download sizes per package, ABI provenance) | `pingouin` | one paragraph survives: conda-forge, because of the BLAS duplication in a QGIS container. The byte-level argument is a decision already recorded in `pixi.toml` |
| the "4 769-run manifest" evidence, the generated-report excerpts and the exclusion-list artefacts | `pingouin`, `analysis-automation` | the pre-results scaffolding was removed on 7 XI 2026; what remains is the contract for `TASK-12` and `TASK-16`, and no text may point at a file that no longer exists |
| "eight repetitions" wherever it survived as the design's r | `hypothesis-testing` | r = 4 in the live design; the ICC and the design effect were recomputed for r = 4 |

Kept, because each is the only place in the repository where its claim is made: the five levels and the three-valued verdict (§1), the G2 admission conditions including the negative control (§2), the DEFF arithmetic and the unit-of-inference rules (§3), the hierarchy and the test budget (§4), the per-claim table with its falsifiers and the three subtleties (§5), the closed-form MDE, the τ sensitivity, the per-cell resolution table, the argument against 5 pp and the four free levers (§6), the five sensitivity analyses (§7), what is deliberately not tested (§8), the software split with the contrast trap and the estimand note (§9), the automation boundary with the case catalogue (§10), and the confounder strategy with the register and the defence paragraph (§11).

---

## 13. Five lines, and one sentence

1. **The run is not the observation.** 960 runs are worth about 320 independent rows at ICC = 0.661 and r = 4; the inference is about 80 tasks, and the degrees of freedom come from tasks.
2. **One confirmatory test at α = 0.05, Holm on a family of two, everything else descriptive.** The error is spent where the claim is, and every demoted claim still carries its falsifier.
3. **The MDE is 14.0 pp at τ = 10, and it is declared first.** Below it the verdict is *undecided*; there is no verdict called "no difference", and it is not written anywhere in the thesis.
4. **The granularity of the test is a decision, not a default.** The contrast that answers the hypothesis must be pre-registered by shape, because a library will happily return three significant pairwise results to a question nobody asked.
5. **Most of the analysis is automatic; the verdicts are automatic only because the rules were frozen; the interpretation never is.** A number recomputable from the manifest must be reproducible, and a sentence about meaning must be marked as the author's.

**And in one sentence.** Artefacts are scored by typed predicates, correctness is compared across conditions on the task level with McNemar and a mixed logistic model, the depth curve is tested as a trend and the mechanism as an interaction with the expressible share, one comparison at α = 0.05 carries the confirmatory weight while the rest are corrected or descriptive, and any difference below 14.0 pp is reported as undecided rather than as absent.
