---
id: design/harness
title: "The harness and who operates it"
type: note
status: live
language: en
question: "Own instrument or a ready agent, and what does that cost to run?"
tasks: [TASK-7, TASK-18]
sources: [technical-stack.md, own-harness-or-ready-agent.md, hpc-local-models.md, analyst-procedure.md]
updated_date: '2026-11-07'
---

# The harness and who operates it

> Own instrument or a ready agent, and what does that cost to run?
>
> Merged 2026-11-07 from `technical-stack.md`, `own-harness-or-ready-agent.md`, `hpc-local-models.md`, `analyst-procedure.md`. Pruned and translated 2026-11-07; the cut log is §18. This document owns the **runner**: the stack, the pinned open loop, where the sweep executes, and the procedure an analyst follows from frozen pre-registration to the output package. The claim ledger it serves is `design/arms-and-validation.md`; the test hierarchy and the MDE are `analysis/statistics.md`; the run record's fields are `framing/what-we-study.md` §7.

---

## 0. Answer

**A framework is refused, the protocol SDK is used, and the loop is pinned rather than written from scratch.** The agent frameworks are refused not because they are heavy but because the three things they automate — message and state assembly, tool-schema translation, retry semantics — are **dependent variables** here: token accounting, effective surface, and the difference between *an error*, *a retry* and *a repair*. The MCP Python SDK is used strictly as **instrument**: `FastMCP` for the server, `ClientSession` over `stdio` for the client, raw JSON-RPC responses for the record. The loop is a pinned open loop of a few hundred lines (`d-4`), because the prompt, the seed, the budget and the register must be ours.

**The sweep runs on pinned weights and frozen code.** Whether the host is a university cluster or an API is a **frozen factor**, decided once and written down, not a factor in the comparison (`analysis/statistics.md` §11.1–11.3). A cluster buys the two things that are hard to argue away — the model cannot change mid-series, and the artefact is a repo plus digests an examiner could re-run — at the price of a real capability floor, which is handled as instrument qualification rather than as a result.

**And the analysis is a procedure, not a judgement.** An analyst applies frozen rules; every decision taken after seeing a result goes into a change log and is marked *post hoc*. Ten prohibitions, four escalation triggers stated as numbers, and a definition of done that ends with *every number has a file and a row*.

---
## 0.1 Two harnesses, one word

"Harness" names two different things in the agent-evaluation literature, and the difference is the
internal-validity argument of this thesis, so the vocabulary is fixed here and used consistently in
chapters 3 and 4 (`thesis/glossary-of-terms.md`, `thesis/concept-dictionary.md`):

| Term | What it is | In this design |
|---|---|---|
| **agent harness** | the loop, the prompt, the tools and the sandbox that turn a model into an agent — the thing **under test** | one, pinned (`d-4`); identical across conditions except the single factor that defines them |
| **evaluation harness** | what runs the tasks, resets the environment, records the trial, invokes the oracle and aggregates the scores — the **instrument** | also one; the reason a difference can be attributed to the interface at all |

The practice literature keeps the two apart for the same reason: a grader that shares the agent's
context inherits its assumptions, and a rig that shares the agent's loop cannot measure it
(`yao2024taubench`; `anthropic2026evals` — task, trial, transcript, outcome, grader). Two
consequences for the writing: name the **agent harness** when describing the conditions, name the
**evaluation harness** when describing the instrument, and avoid "harness" unqualified in both. Where
it survives it means the pair — as in `design/runs.md` §4, where the oracle sits "outside the loop,
on the harness side": that sentence is about the evaluation harness, and says so.

## 1. No framework, and not because it is large

LangGraph 1.x (MIT, 2026) is mature and stable; the objection is **measurement**, not quality. Three of the things it does for you are dependent variables here:

| What a framework automates | Why that breaks the measurement |
|---|---|
| message and state assembly (`TypedDict` + reducers) | `tokens_in` must count the **actual** prompt; reducers add and rewrite content between turns in a way the log does not show — D3 stands on token cost |
| conversion of tools into call schemas (`langchain-core`) | the number of **effective** tools and schemas in context is the independent variable of the depth conditions; an unlogged intermediary is a confounder |
| its own retry semantics (`retryPolicy`, `errorHandler`) | "tool error", "retry" and "repair through a gate" are **three different categories** in the record — D2 depends on telling them apart, and a framework collapses them into one event stream |
| checkpointing to SQLite/Postgres | the one feature worth wanting — see §2 |
| MCP integration (`langchain.mcp`) | adds a **second** MCP → tool-calling translation beside the SDK's, so whether the schema reached the model unchanged becomes unverifiable |

There is also the argument from the programme's own rules: the work is **experimental** and the instrument is the harness. If the loop is a framework, a reviewer may fairly ask what was measured — the interface, or the framework's behaviour. "Both arms ran on the same framework" is true and does not answer the question about **mechanism**, which is the whole content of H2.

---

## 2. The one thing worth taking, and its cheap replacement

What is genuinely valuable is **durability of execution**: 960 runs of several minutes each are days of machine time, and an interrupted sweep must not restart from zero. This needs no state graph — an append-only log plus skipping finished `run_id`s is enough:

```python
def pending(runs: list[Run], log_path: Path) -> list[Run]:
    done = set()
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            rec = json.loads(line)
            if rec.get("event") == "run_finished":
                done.add(rec["run_id"])
    return [r for r in runs if r.run_id not in done]
```

A dozen lines, the same effect, and the log is simultaneously **material for chapter 4** rather than a state database nobody wants to read while writing a table.

A graph runtime would return to the table only if a **multi-agent** variant (planner + executor + critic) entered after the main sweep, which `framing/scope-and-character.md` keeps as a conditional extension. In that case it also needs a **separate control arm**: the same variant on the own loop, so that "the effect of a multi-agent architecture" is separated from "the effect of LangGraph".

---

## 3. The MCP SDK as instrument, not as control

`mcp` (MIT) is used for the two things one does not want to write: the **server** (`FastMCP` with `@mcp.tool()` on PyQGIS functions, `stdio` transport) and the **client** (`ClientSession` giving `initialize`, `list_tools()`, `call_tool()` and raw JSON-RPC responses — exactly the observation layer the record needs). It does **not** choose tools, run a loop or build a prompt. The decision layer is the own loop, common to all conditions, which is the only way the difference stays a difference of interface.

**Three traps, concretely.**

- **Schema determinism.** `FastMCP` generates JSON Schema from type hints and docstrings. Canonicalise before counting tokens and before writing the manifest, or the same server yields different SHA-256 sums between runs and the surface hash loses its meaning:

  ```python
  canonical = json.dumps(tools_schema, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
  schema_sha = hashlib.sha256(canonical.encode()).hexdigest()
  ```

- **Log the wire, not the object.** `tools/list` is written **before** any conversion to a provider format — it is both the proof of run-time discovery and the input to the token accounting.
- **The protocol surface moves.** The SDK dropped Python 3.10 in X 2026, ships per-version types privately (`mcp_types._v*`) and negotiates `protocolVersion` on `initialize`. Hence: **pin `mcp`**, require Python ≥ 3.11, and record the **negotiated protocol version** in the manifest beside the QGIS version. "Used MCP version X, protocol Y" is citable; "used MCP" is not.

---

## 4. The target stack

The selection rule: **every dependency is either a measuring instrument or an artefact check.** A library that only "helps" is a cost, because it hides.

| Layer | Package | What for, concretely | Rejected alternative |
|---|---|---|---|
| Inference | `openai`-compatible client (vLLM/Ollama) or `anthropic` | native tool calling; one code path for local and hosted models | a framework's chat model — adds its own message format |
| MCP | `mcp` (server + client) | geoprocessing server, raw `tools/list`, `tools/call` | a second package of the same name, framework adapters |
| Contracts | `pydantic` v2, `jsonschema` | the gate: types, CRS domain, geometry type, units, required fields | hand-written `if`s (undocumentable) |
| Container | Docker SDK; **Apptainer** on the cluster | headless QGIS 3.44, no network, CPU/RAM/10-minute limits | bare `subprocess`, or a namespace jail for complexity nobody needs |
| CRS and geometry | `pyproj`, `shapely` 2.x | CRS identity and **axis order** (the silent errors of E5/E6), IoU, `equals_exact` with tolerance | string comparison of EPSG codes — misses 4326 with swapped axes |
| Vectors | `pyogrio` (+ `geopandas` for analysis) | GPKG/Shapefile read, required columns, feature counts, topology | slower readers in retirement |
| Rasters | `rasterio` / `rioxarray` | dimensions, CRS, NoData, resolution, value range | direct GDAL bindings |
| Cartography (family C) | `lxml` | declarative QML predicates: symbol, classes, labels | rendering to PNG and comparing pixels — not reproducible across QGIS versions |
| Statistics | `statsmodels`, `pingouin`; GEE as primary, `bambi`/`lme4` as the conditional companion | descriptive work, McNemar, Holm, and the estimand distinction of `analysis/statistics.md` §9 | one unexplained model |
| Tests | `pytest`, `pytest-bdd`, **`FakeModel`**, `vcrpy` | the harness tested without paying for tokens and without non-determinism | tests against a live API |
| Log | stdlib `json` → JSONL, `--resume` by `run_id` | the source of every table in chapter 6 | SaaS trackers — the table must come from JSONL, not from a UI |
| Reproduction | `pixi` + `pixi.lock` | versions in one file; the lock hash into the manifest | unpinned requirement lists |

**`FakeModel` is the most important row.** The harness must be testable **without model calls**: a scripted trajectory (two tool calls, one failing, then `finish`) behind the same interface. That makes the gate, the scoring and the log verifiable in a second instead of ten minutes, and it is what makes TDD possible at all — every "does my scoring work" question becomes free, and the variance it would otherwise introduce never exists.

---

## 5. What is not added

| Candidate | Decision | Reason, as it will appear in §3 of the thesis |
|---|---|---|
| LangChain, agent frameworks | no | the loop and the message format are the object of measurement |
| multi-agent frameworks | no | multi-agent behaviour is a conditional extension, not the instrument |
| experiment trackers (MLflow, W&B, LangSmith) | not on the critical path | the tables come from JSONL; a SaaS cannot be replayed years later |
| workflow engines (Snakemake, Airflow, DVC) | no | `pixi run harness` plus `--resume` suffices; another layer to describe |
| config frameworks (Hydra) | no | `pydantic-settings` and YAML are enough |
| vector store / RAG | no | the tasks need no corpus retrieval; the QGIS documentation is in the versioned system prompt |
| Kubernetes | no | one host, 960 runs, a sequential queue |

**One marginal note:** the SDK has announced extensions (MCP Apps, Skills). They are not needed and must **not** be enabled — every extension changes the protocol surface, which is an independent variable. The manifest records that they were off.

---

## 6. Own station, ready product, or a pinned open loop

| | **D1. Own station from scratch** | **D2. Ready agent, two configurations** | **D3. Pinned open loop** ← chosen (`d-4`) |
|---|---|---|---|
| What is written | loop + MCP client + code executor + register | only configurations and the oracle | loop configuration + register + oracle |
| Control of the prompt | full | **none** | full |
| Control of the seed and temperature | full | none | full |
| Build cost | 3–4 weeks | days | **1–2 weeks** |
| Likely objection | "your loop is worse than a commercial agent" | "you compared two products, not two interfaces" | small, if the loop is pinned and described |
| Causal inference | yes | no | **yes** |

**D3 is not a compromise but the correct choice.** An agent loop is a few hundred lines; writing it from scratch buys nothing beyond **pinning** an existing open implementation, because what matters is that *we* fix the prompt, the surface, the budget and the register — not who typed the loop. The one thing D3 must accept is that the loop is part of the instrument, and therefore has to be tested, versioned and attached: *the station is part of the apparatus, not its background; its code, version and parity-test results are an appendix.*

---

## 7. What must be frozen, and what a product will not freeze

| Element | Why it must be fixed | In a ready-made product |
|---|---|---|
| **system prompt** | the thesis compares interfaces, not instructions | **unavailable** — internal, and it changes between versions |
| **the same instruction to check the result in both conditions** | without it the code condition is a straw man (`design/arms-and-validation.md` §3) | addable only as a user message or a config file — **not in the same place** |
| **tool surface** | the experimental variable | partly: built-ins can be disabled, but the loop has **its own** (file edit, read, shell) |
| **turn and time budget** | assumption A4 | limits exist, but **not the same** in both modes |
| **seed and temperature** | D1 needs repetitions to be comparable | usually not exposed |
| **`detected_by` register** | without it there is no in-loop catch rate | absent; the product has its own log at a different granularity |
| **version freeze** | a series that spans weeks | the product updates **during** the series |
| **output: one artefact + the run record** | the oracle reads a file | the product does many things "on the way" |

**Conclusion:** with a ready-made product two *configurations* can be compared, but it cannot be claimed that the difference comes from the interface, because the prompt, the loop and the repair policy change as well.

**The objection to pre-empt — "your station is weaker" — is closed by three measures before the series:** **execution parity**, where the same PyQGIS script pushed through both conditions must produce an **identical artefact hash**, or the code condition is technically handicapped; **calibration**, where the code condition's share of correct artefacts on the pilot must land inside the expected range — zero means a station fault, not a property of the model (§12); and **a second implementation of the loop**, the pilot repeated on an independent one, where agreement of sign is what rules out a result being an artefact of a single implementation.

---

## 8. Where it runs: a frozen factor, not a study

Pinned local weights on a university cluster are a strict upgrade for **validity**; this section is written to double as the justification of an allocation request.

| Threat in an API-only design | With pinned local weights |
|---|---|
| the provider silently updates the model mid-series; a multi-week sweep spans two model versions | weights are a digest you record; nothing changes unless you change it |
| rate limits and outages make the schedule unpredictable and leave shards unbalanced | scheduler-driven, fully under control |
| per-token cost forces run-count compromises | marginal cost is GPU-hours; 960 runs stop being a budget question |
| "your results are about one vendor's model in a given month, not about the protocol" | the stack is a repo plus pinned digests — closer to an artefact an examiner could re-run |
| task data and draft text leaving campus | everything stays on-premises |

The determinism point matters most here: **D1 is a claim about run-to-run stability**, and the cleanest possible confound removal is "the model could not have changed between repetition 1 and repetition 4". That sentence belongs in the methods chapter.

**What gets harder — four things to plan around.**

**Capability floor, the largest design risk.** Open-weight models at the size a shared cluster can serve are weaker at structured tool calling than frontier models. Too weak a model and **every condition collapses to ~0 % TSR**: no variance, nothing to explain, and a null that is about capability rather than about the protocol. The answer is a pre-registered qualification rule, not a hopeful choice: a (model, harness) pair enters the design only if **baseline TSR ≥ 10 %** on the cards the surface covers, the same rule as `analysis/statistics.md` §2 and `R-1`. A pair that fails is reported as *harness does not qualify* and excluded, exactly like a failed instrument — the table of who qualified is a legitimate results section, not a confession.

**Ollama is a development server, not a sweep engine**: it serialises per model, offers no tensor parallelism and is single-node — fine for a two-hour smoke test, painful for a thousand runs. The serving layer is **vLLM** (or SGLang/TGI): OpenAI-compatible `/v1`, continuous batching, tensor parallelism, a pinned `--revision`. Ollama stays as the laptop mirror, where the pilot asserts *comparable behaviour* rather than equivalence, because chat templates differ.

**The harness is not the only thing that can swallow a call.** For the *ready-product* appendix (V1, 48 runs) the compatibility matrix matters, because a tool call the CLI mangles is not a model error:

| Client | Local OpenAI-compatible endpoint | Risk |
|---|---|---|
| `opencode` | yes, custom provider | low; configuration only |
| `goose` | yes, provider override | low to medium; verify the tool-call format |
| `claude-code` | no; needs a translating proxy | high; tool-use fidelity through a shim is not something to build a claim on |

For the main series this is not a results table, because the loop is ours: it becomes a **qualification note** — tool-call parse success, parallel-call support, streaming deltas, maximum context used — recorded before the series and cited if anyone asks whether the harness swallowed the call.

**Wall clock may get worse, not better.** Local inference on shared GPUs is often 20–60 tok/s per request; a ten-turn run of 2–4 k tokens per turn is minutes of pure generation plus the QGIS work. The estimate is not guessed but computed in phase 0 and put into the allocation request:

```
GPU-hours ≈ runs × (turns/run × output_tokens/turn) / throughput_tokens_per_sec / 3600
            + runs × spatial_work_seconds / 3600
```

The pilot records `tokens_in`, `tokens_out`, `turns` and `wall_ms`, so the arithmetic is mechanical. Independent of that measurement, the planning figure stands: **960 runs are on the order of 100 hours of engine time on 8–16 parallel Slurm tasks** (`framing/scope-and-character.md` §10).

**Quantisation is a treatment you cannot vary.** Q4, FP8 and BF16 change tool-calling reliability materially. One level across the whole design, stated in the methods, recorded in the manifest, and no comparison with papers that used another.

**Bit-level determinism is not guaranteed** even locally — batching and non-deterministic kernels see to that. D1 measures *behavioural* stability, and the methods chapter says so rather than claiming perfect reproducibility.

---

## 9. Slurm shape against the design cells

Shard by **design cell**, never by "the first N runs", so that a partially completed array is still a balanced subset:

```bash
#!/bin/bash
#SBATCH --job-name=exp-sweep
#SBATCH --array=0-15                     # task blocks; each block covers all three conditions
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=06:00:00
#SBATCH --output=logs/%x-%A_%a.out
#SBATCH --requeue                        # resume semantics: a run dir with result.json is skipped

set -euo pipefail
export QT_QPA_PLATFORM=offscreen
export PIXI_CACHE_DIR="$SCRATCH/pixi"
source "$SCRATCH/research/.pixi/envs/experiment/bin/activate" 2>/dev/null || pixi install --frozen

read -r BLOCK <<<"$(pixi run harness shard --index "$SLURM_ARRAY_TASK_ID")"
pixi run harness run --sweep-id "$SWEEP_ID" --tasks "$BLOCK" --resume
pixi run harness score --sweep-id "$SWEEP_ID"
```

Two serving patterns, one of them preferred: a **dedicated server job** allocating N GPUs and exposing an OpenAI-compatible endpoint that the array tasks point at (best throughput; the server must outlive the array), or **one server per array task** on a single GPU (simpler, but pays model load time per task). Prefer the first.

Operational notes for the request: install on the login node with `--frozen` and let compute nodes run offline; write to `$SCRATCH`, then archive and pull back `runs/`; keep only `data/` and `results/` in the repository. Weights come from a gated repository — check the licence terms and whether the cluster mirrors them, otherwise the download is part of the request.

**Phase plan, each phase producing the input for the next:**

| Phase | Where | Scope | What it produces |
|---|---|---|---|
| 0 | 1 GPU node | smoke: a handful of tasks, one condition, one repetition | tokens/turn, turns/run, wall time/run → the numbers for the allocation |
| 1 | 1 GPU node, vLLM | the calibration set, the candidate model | the floor screen: does the pair qualify (10 %) |
| 2 | cluster, small array | the pilot | τ, the in-loop catch rate, variance estimates → the power check |
| 3 | cluster, full array | 960 runs across the design cells | `runs/` with `result.json` per run |
| 4 | login node or laptop | `score → merge → analyse` | the tables, the figures, the thesis numbers |

---

## 10. The analyst: role and limits

The procedure is operational, not a chapter; it can enter the appendix as *analysis reproduction*. It binds from the freeze of the pre-registration to the handover of the output package. **Overriding rule: the analyst applies frozen rules and does not invent them.** Any decision not in the pre-registration or in this document requires a change-log entry and the author's agreement.

| The analyst **may** | **may not** |
|---|---|
| reject a run by the closed list of rules (§12) | reject a run "because it looks odd" |
| report a suspected oracle fault | fix the oracle after seeing data |
| report a result as undecided | call a non-significant result "no difference" |
| propose an additional analysis | add an extra analysis **to the confirmatory table** |
| see every column | see condition **labels while coding failures** (§14) |

**Separation of roles.** The person coding failures receives transcripts with the `condition` column removed and a random `run_alias`; unblinding happens after the coding is frozen. The quantitative analysis may be unblinded from the start — labels are in the manifest anyway and the rules are frozen.

---

## 11. Gate A — integrity audit

**Inputs, and the check on each:**

| File or directory | What it holds | Check |
|---|---|---|
| `pre-registration.md` | version, date, cards, tolerances, analysis plan, MDE | SHA-256 in `SHA256SUMS` |
| `runs/<run_id>/result.json` | one run: condition, turns, tokens, time, artefacts, predicates | completeness 1:1 with the coverage matrix |
| `oracles/` + `tolerance-table.csv` | predicates and thresholds | frozen before the first run |
| `corpus/cards/*.yaml` | the 80 task cards, `family`, `tier`, expressible share | 80 files |
| `SHA256SUMS` | the sums of all of the above | verified before scoring |

**The first command of every session:**

```
sha256sum -c SHA256SUMS && git -C . rev-parse HEAD
```

A hash mismatch is a **stop**. The data are not what was frozen, and everything downstream is meaningless.

**The manifest.** Every `result.json` carries the record of `framing/what-we-study.md` §7 — identity, outcome, process, cost and artefact groups, with `detected_by` taking four values — plus `protocol_version`, `surface_sha` and `image_digest`, without which the surface cannot be said to be the same surface. A missing required field sends the run to the list of gaps, not to the analysis.

**Coverage matrix.** Build `task × condition × repetition` and count empty cells. **Criterion: zero empty cells.** Empty cells are reported with a list, never "filled in with the mean".

**Homogeneity in time.** Plot the distribution of `model_version` and `prompt_hash` against run order. A change mid-series means **the data are split into epochs** and reported separately; epochs are never mixed in one test, because that is not one experiment.

**The closed exclusion list — these five, and no others:**

1. the artefact is unreadable **and** the oracle could not evaluate it (not: "the artefact is bad");
2. an **infrastructure** limit was exceeded (container, host timeout) — not an agent limit;
3. no oracle entry while an artefact exists;
4. a duplicated `run_id`;
5. a run produced by `FakeModel` or a dry run.

Output: `exclusions.csv` (`run_id`, rule 1–5, justification) plus the count and share **per condition**. If exclusions exceed **5 %** in any condition, escalation (§16).

**Instrument anomalies are reported, not excluded:** `stop_reason == "length"` (context truncation), rate-limit errors, timeouts, a missing output file, turns equal to the limit. These are **data about agent behaviour** and belong in the results chapter.

**Gate A output:** `audit.md`, `exclusions.csv`, a GO/NO-GO decision.

---

## 12. Gate B — instrument qualification

Without these four numbers there is no analysis, only reporting of noise:

| Condition | Threshold | Source |
|---|---|---|
| oracle negative control | **40/40** deliberately broken artefacts rejected | `oracles/tests/` |
| oracle repeatability | two scorings of the same artefact give an identical verdict | double run |
| failure coding agreement | **κ ≥ 0.6** on 20 % of runs coded blind and double | `coding/` |
| capability floor | **baseline TSR ≥ 10 %** on the cards the surface covers | pilot runs, rule `R-1` |

If any threshold fails: **stop and escalate**. Not "analyse with caution" — there is nothing to measure with. The negative control deserves its own sentence, because the first three conditions alone are passed by an oracle that always returns *pass*, and the artefacts this thesis scores are exactly the kind that *look* right.

---

## 13. Scoring — the only permitted implementation

```
for each run:
    art = artefacts            # list of files with SHA-256
    for each predicate p in oracle[task_id]:
        pass[p] = eval(p, art) # tolerances from tolerance-table.csv, NOT from code
    TSR_run   = all(pass)
    PCS_run   = sum(w_p * pass[p]) / sum(w_p)      # partial credit
    CVS_run   = legal_calls / all_calls
    cost_run  = tokens_in + tokens_out              # time and call count reported separately
```

| Metric | Definition | Edge case |
|---|---|---|
| **TSR** | share of runs in which **all** required predicates passed | no required predicate → configuration error, not 0 |
| **PCS** | weighted share of satisfied predicates | weights from the pre-registration, not from the data |
| **S3** | share of a task's failures covered by its dominant error class ≥ 75 % | the D1 measure; **not** a variance test |
| **repeatability class** | predicate verdict across the four repetitions: identical / equivalent / divergent | no success → `no_success`, not "divergent" |
| **CVS** | share of calls matching the schema and the allowed modules | empty code → 0 |
| **cost per success** | Σ tokens ÷ number of successes, **at task level** | zero successes → `NaN`, not a division by zero |
| **turns to first correct artefact** | secondary, reported with censoring | no success → censored at the turn limit |

**Three scoring prohibitions.**

1. **Repeatability is computed on the predicate vector and the artefact hash, not on a pass pattern** — a pattern measure gives "divergent" for most tasks and the test loses its meaning. And a **variance** test is banned outright: the variance of a binary outcome is a function of its mean, so higher repeatability would be "detected" with no behavioural change (`analysis/statistics.md` §5).
2. **Cost is computed per success, not per call** — otherwise it measures a different quantity, and D3 is about the cost of *effectiveness*.
3. **TSR is never averaged across families into one headline without the breakdown** — the families carry different predicate vocabularies and the average hides H3.

**Output:** `scored/runs.parquet`, `scored/tasks.parquet` (aggregate per task × condition), `scoring_report.md` with the numbers and the edge cases.

---

## 14. What is tested, and what verdict looks like

The claims are the ledger's (`design/arms-and-validation.md` §2) and are not restated here; what a procedure has to fix is the **order** and the **sentence**.

| Claim | Analysis | What has to be on the page |
|---|---|---|
| **H1** — the way the operations are exposed changes correctness | paired McNemar at task level (primary) + mixed logistic with a random task effect (companion) | β, SE, OR, *p*, σ, and the difference in pp with a task-bootstrap CI; the MDE printed beside it |
| **H2** — correctness rises with enforcement depth, N1 → N4 | linear contrast across depth plus a plateau fit, not two pairwise tests | the contrast, its CI, the plateau point, **and the catch rate** — the falsifier is a flat curve *with* a flat catch rate |
| **H3** — the difference grows with the expressible share | condition × share interaction, with the pattern stated in advance | the interaction and a per-share breakdown, including the `none` cards, where a difference would refute rather than support |
| **D1** | S3 and the predicate-level classes | distributions, S3 with a task-bootstrap CI |
| **D2** | failure classes × condition; κ on the blind subsample | counts, shares, Cramér's V, κ |
| **D3** | cost per success, task-level bootstrap | median and mean, CI, and the TSR ranking against the cost ranking per family |
| **D4** | oracle repeatability, artefact hashes, manifest completeness | agreement; instability stops the series instead of refuting a hypothesis |

**Order of work.** Compute **all** *p*-values of the family first, then apply **Holm** to {H2, H3}, and record both raw and corrected values. H1 stands alone at α = 0.05 and does not enter Holm.

**The verdict is always three-valued:** *confirmed* / *refuted* / **undecided**. Rule: a difference smaller than the MDE is **undecided**, whatever *p* says; a difference of at least the MDE in the opposite direction is refuted (outcome W5). There is no fourth "equivalence shown" category, because the design contains no equivalence test — equivalence was part of a condition set that is not being run.

**Failure coding happens before unblinding.** Classes: wrong layer or data · silent CRS error · invalid geometry · near miss · wrong parameter or tool · inconsistent aggregation · refusal or timeout. **20 %** of runs are coded blind and double on transcripts without `condition`; κ is computed only on that subsample, and κ < 0.6 means *code again*, not *interpret*.

---

## 15. Windows onto the result

Five sensitivity analyses, all mandatory, each answered as a yes/no against the main conclusion:

| Analysis | What is recomputed | The question it answers |
|---|---|---|
| **Tolerances** | TSR at the lower and upper bound of the tolerance table | does the conclusion depend on the threshold |
| **Exclusions** | the analysis with and without `exclusions.csv` | do the rejections change the result |
| **Family weighting** | TSR weighted equally across families against the raw figure | does one family's advantage produce the average |
| **Tier** | the contrast within `tier` | is the effect an artefact of difficulty |
| **Epochs** | the contrast within each time epoch | is the effect an artefact of one stretch of the series |

The output is a table `analysis | main value | variant | does the conclusion change (yes/no)`. A conclusion that flips at ±0.02 on `extent_iou` is not fit for a sentence in chapter 7.

---

## 16. The output package, ten prohibitions, and the change log

Chapter 6 is **generated, not rewritten**. File names are fixed, so that each section of the results cites one file:

| File | Content | Thesis section |
|---|---|---|
| `tables/t6_1_tsr.csv` | TSR, CI, paired differences | 6.1 |
| `tables/t6_2_families.csv` | family × condition × tier | 6.2 |
| `tables/t6_3_depth.csv` | N1 → N4 contrast, plateau, catch rate | 6.3 |
| `tables/t6_4_share.csv` | condition × expressible share | 6.4 |
| `tables/t6_5_failures.csv` | failure classes, CRS classes, V, κ | 6.5 |
| `tables/t6_6_repeatability.csv` | S3, predicate-level classes | 6.6 |
| `tables/t6_7_cost.csv` | cost per success, rankings | 6.7 |
| `tables/t6_8_audit.csv` | auditability S5, gate log | 6.8 |
| `tables/t6_9_sensitivity.csv` | the five analyses | 6.9 |
| `figures/` | plots from the same data | 6.1–6.9 |
| `audit.md`, `exclusions.csv`, `scoring_report.md`, `analysis_log.md` | the reproduction trail | appendix |

**The criterion:** every number in chapter 6 has a source file and a row. A hand-typed number is a missing gate.

**Ten prohibitions.**

1. Do not look at condition labels before the exclusion rules and the coding are frozen.
2. Do not change the tolerance table after the first look.
3. Do not add cards to the corpus after a look, not even "to balance it".
4. Do not report *p* without an effect size and a CI.
5. Do not compute degrees of freedom from runs.
6. Do not call a non-significant result "no difference" — that phrase is available only against the MDE.
7. Do not average families without the breakdown.
8. Do not drop the adversarial sample because "it did not work out".
9. Do not compute cost per call when the claim is cost per success.
10. Do not change a hypothesis after seeing a result; a new one may be added, marked *post hoc*.

**Escalation triggers, as numbers, not feelings:**

| Trigger | Action |
|---|---|
| exclusions > 5 % in any condition | halt scoring, report to the author |
| κ < 0.6 | repeat the coding; do not interpret |
| an empty cell in the matrix | the test is not computed; the missing runs are added **before** the analysis |
| `model_version` or `protocol_version` changed mid-series | split into epochs, report separately |
| baseline TSR < 10 % on the pilot | stop — no variance to explain (outcome W6) |
| > 10 % of runs with `stop_reason == "length"` | an instrument problem, not a result |

**The change log, mandatory format, for every decision taken after seeing any result:**

```
### Z-04  (2027-02-11)
What: family C was added to the H1 analysis after checking TSR.
Why: <substantive reason>
Impact: <which tables change>
Status: post hoc — does NOT enter the confirmatory test
```

**Definition of done**, all of it true: the checksum passes and the log is complete; the matrix is closed and exclusions stay under 5 % per condition; the four gate-B numbers are met and quoted; scoring comes from one implementation with its edge cases computed; H1 carries β, OR, the difference in pp, CI, *p* and the MDE; H2 carries the depth contrast, the plateau **and** the catch rate; H3 carries the per-share breakdown including the `none` cards; Holm has raw **and** corrected values in the table; the five sensitivity analyses carry a "does the conclusion change" column; every number has a file and a row; every verdict is three-valued.

---

## 17. Five lines, and one sentence

1. **No framework, one protocol SDK, one pinned open loop** — because the loop, the prompt and the schema translation are measured, not used.
2. **The station is part of the apparatus**: parity of the artefact hash, calibration in the expected range, and a second implementation of the loop are what stop "your harness is weaker" from being an alternative explanation.
3. **The host is frozen, not varied** — pinned weights and digests remove model drift, and the capability floor is handled as qualification (10 %), not as a finding.
4. **An analyst applies frozen rules**: Gate A on integrity, Gate B on the four qualification numbers, one scoring implementation, and five sensitivity analyses that must be able to say "the conclusion changes".
5. **Every number has a file and a row**, every verdict is three-valued, and everything decided after a look is in the change log marked *post hoc*.

**In one sentence.** The instrument is a pinned open loop around the official protocol SDK, run on frozen weights in a pinned container, carried by an append-only log that survives interruption and doubles as chapter 4 material, and handed to an analyst who may apply frozen rules but may not invent them — which is what makes the difference in chapter 6 a difference of interface rather than a difference of station.

---

## 18. What was cut, and why

| Cut | Source note | Reason |
|---|---|---|
| the hypothesis table H2–H7 with the 2 × 2 gated interaction, the TOST at ±20 pp, H5 on artefact identity, H6 cost, H7 error classes | `analyst-procedure.md` §§5, 12 | a retired numbering and a condition set that is not run. The ledger is H1 / H2 (N1 → N4) / H3 (expressible share) plus D1–D4, owned by `design/arms-and-validation.md` §2 |
| `ladder_level` (1–3), `min_surface`, and the L1–L3 contrasts in the manifest and the tables | same, §§2.1, 5.2, 7 | the tool-size ladder is retired; the manifest carries `condition` (K / N1 / N4) |
| "40 tasks × 16 repetitions, MDE 9.3 pp", the 160-run pilot, the 90-run calibration pilot | same, §5.1; `own-harness-or-ready-agent.md` §6 | three generations of arithmetic. Live: 80 tasks, r = 4, 960 runs, MDE 14.0 pp at τ = 10 (`analysis/statistics.md` §6) |
| the front-end × model factor (2 CLIs × 2 models × 3 paradigms = 1,800 runs, 2,400 with the gated arm) and the 60-shard array | `hpc-local-models.md` §§3–4 | `d-2` fixes one model and `d-4` one harness; a second model doubles the series before it can speak about an interaction, so it is further work rather than a factor |
| "PB3 / PB4", `mcp-15-gated`, `codegen`, `runs.parquet`, the GitHub matrix | same; `technical-stack.md` §5 | retired vocabulary and deleted artefacts; conditions are K / N1 / N4 and the record is `runs/<run_id>/result.json` |
| "ED" as a named metric with its own class table | `analyst-procedure.md` §4 | the construct survives as D1 (S3 plus predicate-level classes) and a variance test is explicitly banned; the old class table drifted toward a variance measure |
| three separate schedules (17 weeks, the HPC phase plan, the implementation order) | all four notes | one phase plan (§9) plus the planning figure in `framing/scope-and-character.md`; a second schedule is a second answer |

**Added while pruning**, because the cut had removed the only home of the claim: the qualification rule as one number in one place (10 %, §8 and §12), the note that a ready-product appendix turns the client-compatibility matrix into a qualification note rather than a results table, the five sensitivity analyses including epochs and tier, and the manifest field `detected_by` with its four values beside `protocol_version` and `image_digest`.

**Kept, each being the only place in the repository where its claim is made:** the measurement argument against frameworks, the append-only log with resume, the three SDK traps, the stack table with `FakeModel`, the prohibition table, D1/D2/D3, the eight things that must be frozen with the three parity measures, the host as a frozen factor with the capability floor and wall-clock arithmetic, the Slurm shape and phase plan, the analyst's limits and the blindness rule, Gate A and Gate B, the scoring definitions with their three prohibitions, the per-claim reporting table with the three-valued verdict, the five sensitivity analyses, the output package with ten prohibitions and the change log, and the five lines — §§1–17.
