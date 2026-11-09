---
id: design/runs
title: "One run, start to finish"
type: note
status: live
language: en
question: "What physically happens between the prompt and the scored artefact?"
tasks: [TASK-17]
sources: [experiment-architecture.md, run-in-both-arms-a-01.md]
updated_date: '2026-11-07'
---

# One run, start to finish

> What physically happens between the prompt and the scored artefact?
>
> Merged 2026-11-07 from `experiment-architecture.md`, `run-in-both-arms-a-01.md`. Pruned and translated 2026-11-07; the cut log is §17. This document owns the **execution anatomy**: the loop, the channels, the run directory, the observation points, the error taxonomy and the resume rules — and one card worked through all three conditions. The stack and the host are `design/harness.md`; the surface specification `design/tool-surface.md`; the gates `design/correctness.md` §1; the conditions and the ledger `design/arms-and-validation.md` §§2, 4.4.

---

## 0. Answer

**One agent loop, three action channels.** The same client, the same system prompt, the same turn and time budget, the same truncation policy and the same register run in every condition; what differs is **what the model is allowed to do**: write code (**K**), call nine operations whose calls are validated against their schemas (**N1**), or call the same nine operations whose *results* are also checked against invariants and the card's terminal conditions (**N4**).

**The catalogue conditions go through a real MCP server**, with `initialize`, `tools/list` and `tools/call` over `stdio` — not through a list of schemas pasted into the prompt. That is not a detail: pasting the schemas would remove discovery, remove the protocol's error channel, and leave a comparison of two prompts rather than two interfaces.

**One run leaves a directory, not a log line.** `request.jsonl`, `calls.jsonl`, `stdout.log`, `artefacts/` and — written last — `result.json`; its presence is what marks a run complete and what makes `--resume` idempotent. Everything else in this document is detail about what goes into that directory and in what order.

---

## 1. The one decision: one loop, three channels

If the code condition were a single one-shot generation while the catalogue conditions were agents with twenty-five turns, the comparison would be of **interface plus agency** — and no result could be distinguished from a difference in the iteration budget. Both sides are therefore the same loop, and the only difference is the tool set:

| | **K** — generated code | **N1** — catalogue, schema only | **N4** — catalogue, with checks |
|---|---|---|---|
| Tools the model sees | `run_python(code)`, `finish()` | nine GIS operations, `finish()` | the **same nine**, `finish()` |
| What the model does | writes PyQGIS, sees stdout/stderr, repairs | chooses an operation and its parameters | chooses the same operation and parameters |
| Engine | the same QGIS container | the same container, through the server | the same container, through the server |
| What is checked | nothing but the interpreter | the call against its schema (P-I) | the call (P-I) **and** the result (P-II/P-III) |
| Budget | turns / 10 min / tokens | identical | identical |

**What must be identical and is easy to break by accident:** the system prompt, the turn limit, the wall-clock limit, the token budget, the truncation length of tool results, the rule that errors come back verbatim, the way a run ends (`finish` or the budget), and the output contract. Each of these is a line in the manifest, not a promise — a difference in any of them is a difference in the treatment.

**What must differ and is the treatment:** the tool set and, inside the catalogue conditions, whether `checks.yaml` is applied. Nothing else.

---

## 2. One agent loop, not "agents versus plain LLMs"

| Question | Answer | Why |
|---|---|---|
| Build an agent loop? | **yes — one, controlled** | the loop is part of the interface and must be constant across conditions |
| Compare against a one-shot "plain" LLM? | **not in the main comparison** | one-shot generation measures whether the model got it right first time, not which interface it worked through |
| Require native tool calling? | **yes** | without it the catalogue condition does not exist; this is a model *qualification* rule, checked before the series |

The cheap variant worth one sentence and not an arm: setting the turn limit to one in the code condition measures the value of *iteration* rather than the value of the *interface*. It is a legitimate side result and it is not in the design, because at 80 tasks and r = 4 it would spend runs that the depth contrast needs.

---

## 3. The components

```
                    ┌──────────────────────────────┐
                    │  model server (vLLM)         │
                    │  OpenAI-compatible API       │
                    │  digest + quantisation PIN   │
                    └──────────────▲───────────────┘
                                   │ chat/completions (logged)
                    ┌──────────────┴───────────────┐
                    │  HARNESS (own, Python)       │
                    │  • one loop, one parser      │
                    │  • turn / time / token budget│
                    │  • N4 check hooks            │
                    │  • writes the run directory  │
                    └───┬──────────────────────┬───┘
                        │ MCP (stdio)          │ code execution (K only)
              ┌─────────▼─────────┐   ┌────────▼─────────────┐
              │ MCP SERVER        │   │ QGIS 3.44 CONTAINER  │
              │ (`mcp`, Python)   │──▶│ headless, no network │
              │ tools/list,       │   │ `qgis_process` /     │
              │ tools/call        │   │ `processing.run`     │
              └───────────────────┘   └────────┬─────────────┘
                                               │ artefact on disk
                                      ┌────────▼─────────────┐
                                      │ ORACLE (harness side)│
                                      │ predicates → verdict │
                                      └──────────────────────┘
```

The load-bearing line in the diagram: **the MCP server and `run_python` call the same engine inside the same container image.** If they did not, a difference between conditions would be a difference of implementation, not of interface — which is the confounder the parity test (§14) exists to exclude. And the oracle sits **outside** the loop, on the **evaluation-harness** side (`design/harness.md` §0.1), because it knows the answer and the loop must not.

---

## 4. The loop, with the observation points marked

```python
for turn in range(max_turns):
    req = build_request(system, history, tools)      # log tokens_in_system, prompt_hash
    resp = model.chat(req)                           # log tokens_out, stop_reason, latency
    if resp.tool_call is None:
        history.append(resp.text); continue          # "thinking" without action: allowed, counted

    match resp.tool_call.name:
        case "finish":
            break
        case "run_python" if condition == "K":
            res = sandbox.exec(call.args["code"])    # stdout / stderr / exit, 10-minute ceiling
        case tool if condition in ("N1", "N4"):
            res = mcp.call_tool(tool, call.args)     # log args, result, error, duration
            if CHECKS:                               # N4 only
                res = validate_result(tool, call.args, res)
    history.append(truncate(res))                    # identical truncation in all conditions
else:
    status = "budget_exhausted"
```

Three things about that loop are worth naming because they are where a harness silently stops being an instrument.

**`truncate` is the same function in all conditions.** Long tool results are cut to the same length, by the same rule, whether the result is stdout from Python or a JSON object from the server. A different cut is a different interface.

**The N4 check runs on the result, inside the loop, before the model sees it** — that is the whole of the enforcement contrast. In N1 the same `call_tool` returns the result unchecked, so the model sees exactly what an N4 run would show when nothing is wrong.

**A turn without a tool call is allowed and counted.** Models think in text; forbidding it would change the interface, and counting it lets the cost analysis see the difference between reasoning and acting.

---

## 5. How the code condition "returns code", which the harness executes

Three variants existed; the first is the design.

| Variant | Mechanism | Assessment |
|---|---|---|
| **A. One tool `run_python(code)`** ← chosen | the model calls a tool whose argument is code; the harness executes it in the container and returns stdout/stderr/exit | simplest to analyse; the code is a **call argument**, so it sits in `calls.jsonl` like any other call and the comparison with the catalogue is nearly symmetric |
| B. Code blocks in the text | the model emits ```` ```python ```` and the harness extracts and runs it | needs a parser and text cleanup, and comparing it with tool calls is harder |
| C. A file plus a command | the model writes `script.py` and calls `run` | an extra layer of intermediate artefacts and more places to go wrong |

With A, the code condition has **exactly two "tools"**, and a single call in either condition is a comparable unit: name, arguments, result, duration.

**Execution safety and determinism:** a fresh container per run, no network, empty `tmp`, CPU/memory/time limits, code executed in a subprocess with `cwd` set to the run directory, artefacts writable only under the path the task names, and a SHA-256 dump of the output files at the end of every run — including failed ones.

---

## 6. What "using MCP" means, concretely

| MCP element | Where it happens | What is logged |
|---|---|---|
| `initialize` | handshake between client and server (name, version, capabilities) | the **negotiated protocol version** and the server version |
| `tools/list` | **discovery** at run time | the server's full response, before any conversion to a provider format |
| schema → tool-calling translation | in the client | the **effective token count** of the schemas actually sent |
| `tools/call` | the call, with arguments | arguments, result, error, duration |
| server-side validation | rejection inside the server | the error code and its text |

**Transport: `stdio`**, one process per run — simplest and fully deterministic; Streamable HTTP is closer to production and adds network variability for no measurement gain. In the Python SDK the shape is a server with decorated functions and a client session over `stdio`, and **the module names must be checked against the pinned version** and recorded in the manifest.

**Where the surface lives.** The nine operations are registered **on the server**, and what the model sees is whatever `tools/list` publishes. That is how a real deployment works, and it is why the surface can be hashed (`surface_sha`) and compared across conditions: it is a property of the server, not of the prompt text. The hash is computed over the **canonical** form of the response — keys sorted, descriptions included verbatim, `additionalProperties` and `enum` preserved — so that "the same surface" is a digest rather than a claim, and so that a difference in wording between two runs is caught before the sweep rather than in the results.

---

## 7. The run directory, file by file

One directory per run, and its layout is a contract, because a rescoring pass years later depends on it:

| File | Written | Contents |
|---|---|---|
| `request.jsonl` | at every turn, append-only | the request as sent: system hash, message roles and lengths, tool list hash, parameters |
| `response.jsonl` | at every turn | raw responses, stop reasons, token counts, latency |
| `calls.jsonl` | at every call | tool name, arguments, result or error, duration, and for K the captured script |
| `stdout.log` | for K | the interpreter's stdout, stderr and exit code, untruncated |
| `artefacts/` | whenever written | every file the run produced, plus a `SHA256SUMS` |
| `gate.jsonl` | N4 only | each check, its inputs, its verdict and the `repair_iterations` counter |
| `result.json` | **last** | the record of `framing/what-we-study.md` §7 plus `protocol_version`, `surface_sha`, `image_digest` |

**The ordering rule is not cosmetic.** `result.json` written last means its presence is a completion marker, which is what makes resume safe (§11) and what makes a half-written run visible rather than plausible. A run whose directory exists but whose `result.json` does not is **unfinished**, never "empty result".

---

### 7.1 What the layout buys: rescoring and the archive

Two properties are worth the discipline of the layout, and both matter more than they look at design time.

**Rescoring without re-running.** A predicate can be recomputed from `artefacts/` alone, because the oracle reads files and the files are kept with their hashes. If a tolerance turns out to be wrong, or a predicate's implementation has a bug, the series is re-scored in minutes rather than re-run in a week — and the sensitivity analysis on tolerances (`design/harness.md` §15) is only affordable because of this.

**A defensible archive.** A run's directory is a few megabytes, dominated by artefacts; 960 of them, with the container image and the weights referenced rather than copied, fit in a repository's side-storage without negotiation. What is archived is `request.jsonl`, `calls.jsonl`, `gate.jsonl`, `result.json` and `SHA256SUMS`; the raw `stdout.log` can be dropped once `calls.jsonl` has the exit code, and the artefacts of failed runs can be dropped only if their hashes and oracle verdicts stay — because the failures are the data.

## 8. Context, truncation, and the thing that must not differ

The interface includes how much of the world the model sees between turns. Four rules, all identical across conditions:

1. **A fixed result-length ceiling**, in characters, applied to every tool result and to stdout/stderr alike. Exceeding it appends an explicit marker, so truncation is observable in the record rather than inferred.
2. **No summarisation of history.** The harness never rewrites earlier turns; if the model hits the cap, the run ends with `stop_reason = "length"`, which is an *instrument anomaly* reported in the results chapter, not an exclusion. Production harnesses do the opposite — they **compact**, summarising and offloading earlier context so a long run continues (`anthropic2026evals`). The divergence is deliberate: compaction makes the prompt a function of the agent's own past, and that quantity is counted in tokens by D3. It is named as an external-validity limitation, because a deployment that compacts may behave differently at the context limit than this series does.
3. **Errors are passed verbatim** — the server's structured object or the interpreter's stderr, unedited. Repair quality is a measured quantity, so the message must be the one the condition actually produces.
4. **The schema block is counted, not estimated.** `tokens_in_system` includes the schemas as sent, because the surface's context cost is part of what the catalogue condition pays and part of what D3 measures.

The temptation this section resists is "helping" one condition with a tidier result format. A tidier format is an interface change, and the design has exactly one such change in it: the presence or absence of the N4 checks.

---

## 9. Observation points, and what each field feeds

| Layer | What is logged | What it is for |
|---|---|---|
| model | every request and response, `tokens_in` / `tokens_out`, `stop_reason`, latency, seed | cost (D3); detecting context clipping |
| **effective context** | `tokens_in_system`, the number and size of tool definitions **actually sent** | the effective surface; without it you do not know what was manipulated |
| harness | each turn: text, call, `finish` decision, stop reason | reconstructing the trajectory, the failure taxonomy |
| MCP | `initialize`, the full `tools/list`, every `tools/call` | proof that the protocol was used; analysis of tool-choice errors |
| sandbox | stdout / stderr / exit code, time, memory | D2 (silent errors in code), D1 (repeatability) |
| `gate` | what was rejected, why, and how many repair iterations it cost | H2 (enforcement depth) and the mediation report |
| artefact | paths, SHA-256, size | D1 and the detection of unlogged substitution |
| oracle | predicate → expected → observed → tolerance → pass | every dependent variable |
| `detected_by` | one of **four** values | the in-loop catch rate, and the difference between "refused" and "caught afterwards" |

---

## 10. Errors at the harness level, and how they map onto exclusions

Not every failure is a result, and not every non-result may be thrown away. The taxonomy, with the exclusion rule it maps onto (`design/harness.md` §11):

| Kind | Example | Counted as | Excluded? |
|---|---|---|---|
| **model/task failure** | wrong artefact, silent CRS error | a task failure, with its error class | no — this is the datum |
| **surface rejection** | N4 refuses a call or a result | a rejection, plus a repair iteration | no — this is the treatment working |
| **protocol/transport** | `stdio` process died, malformed JSON-RPC | an infrastructure anomaly | only if the host failed, per rule 2 |
| **container/host limit** | image failed to start, host timeout | infrastructure | yes, rule 2 |
| **oracle fault** | a predicate raises, artefact unreadable | an instrument fault | yes, rule 1 or 3, and escalated |
| **duplicate or dry run** | the same `run_id` twice, `FakeModel` output | not a run | yes, rules 4–5 |

**The rule that keeps this honest:** a *rejection* is never an exclusion. If N4 rejects a call and the model repairs, that is the mechanism working; if it rejects and the model gives up, that is a failure of the task, and the repair counter is what tells the two apart.

---

## 11. Resume, run identity and idempotency

A series of 960 runs will be interrupted; the design assumes it.

- **A `run_id` is derived, not invented:** `sha256(condition | task_id | repetition | surface_sha | model_digest)[:16]`. Two runs with the same id are the same run, and a re-execution overwrites rather than duplicates.
- **`--resume` skips any run directory with a `result.json`.** An interrupted run leaves a directory without one, so it is redone from the start — a partial trajectory is not a datum.
- **Re-running a *finished* run requires an explicit flag**, and the flag writes a line into the deviations register. Silent re-runs are how a sweep acquires a bias nobody can see.
- **`FakeModel` runs share the layout** and are distinguishable by one field, so the pipeline can be exercised end to end at no cost and so that a dry run can never be mistaken for a datum (exclusion rule 5).

---

### 11.1 The volume arithmetic

960 runs × (three conditions × 80 tasks × four repetitions), each with a directory of a few megabytes, is a working set on the order of tens of gigabytes at peak and a few after pruning. That is small enough to keep the whole series in one place, and large enough that the pruning rule must be written down before the sweep rather than invented during it:

| Kept for ever | Kept until scoring | Dropped after scoring |
|---|---|---|
| `result.json`, `calls.jsonl`, `gate.jsonl`, `SHA256SUMS`, `request.jsonl` | `stdout.log`, intermediate artefacts of successful runs | nothing from a failed run except its hashes and verdicts |

The rule that keeps the archive honest: **a failed run's record is never cheaper to drop than a successful one's.** Failures are the dependent variable in D2 and the source of the error-class distribution; a sweep that archived successes and discarded failures would produce a thesis in which nothing ever went wrong.

## 12. One card through all three conditions

The card, from the corpus, is the one that makes the abstract argument concrete:

```yaml
id: A-01     tier: T2     family: A
prompt: >
  Buffer the roads in dane/drogi.gpkg by 5 km and clip the result to the
  commune boundaries in dane/gminy.gpkg. Write it to wynik/bufor_gminy.gpkg
  in EPSG:2180.
inputs: [dane/drogi.gpkg, dane/gminy.gpkg]        # both in EPSG:2180
oracle: crs_equal 2180 · geom_valid · extent_iou >= 0.95
        feature_count 2481 · area 3912.4 km2 +-0.5 % · attr_present [gmina_id]
pitfall: the unit of the radius (m vs km) · clipping at the boundary
```

**Common to all three conditions:** the identical prompt text, the same inputs, the same model version and seed, the same container with the same library versions, the same turn/time budget, the same output contract (`wynik/bufor_gminy.gpkg` plus the run record), the same oracle, and the same register.

### 12.1 K — prompt → generated code → execution

One tool: `run_python(code)`. No operation catalogue; the model has the prompt and an interpreter.

```
TURN 1  [model → tool call]
run_python(code="""
  from qgis.core import QgsVectorLayer
  import processing
  drogi = QgsVectorLayer("dane/drogi.gpkg|layername=drogi", "drogi", "ogr")
  gminy = QgsVectorLayer("dane/gminy.gpkg|layername=gminy", "gminy", "ogr")
  buf = processing.run("native:buffer", {
      "INPUT": drogi, "DISTANCE": 5, "SEGMENTS": 5,
      "DISSOLVE": False, "OUTPUT": "memory:"})["OUTPUT"]
  out = processing.run("native:clip", {
      "INPUT": buf, "OVERLAY": gminy, "OUTPUT": "memory:"})["OUTPUT"]
  processing.run("native:savefeatures", {
      "INPUT": out, "OUTPUT": "wynik/bufor_gminy.gpkg"})
""")

TURN 2  [tool → model]        ← OBSERVATION: free text
  "Process completed. no output
   Warning 1: Field 'gmina_id' of feature 0 not found"

TURN 3  [assistant → final text]
  "The 5 km buffer was computed and clipped to the commune boundaries;
   the result is saved in wynik/bufor_gminy.gpkg in EPSG:2180."
```

**What just happened, and why it is the subject of the thesis.** `DISTANCE: 5` in a metric layer means **5 metres**, not 5 kilometres. No exception is raised; execution "succeeded". The interpreter returned **free text** — no CRS, no units, no feature count, no area. The model declares success in turn 3, and it is right about what it did and has no way to see that it was wrong unless it writes a check itself (which is what measure **S4** counts).

**What the oracle sees:**

| Check | Observed | Verdict |
|---|---|---|
| `crs_equal 2180` | EPSG:2180 | ✓ |
| `geom_valid` | valid | ✓ |
| `feature_count 2481` | 2481 | ✓ |
| `attr_present [gmina_id]` | present | ✓ |
| `extent_iou >= 0.95` | **0.34** | ✗ |
| `area 3912.4 km2 +-0.5 %` | **4.6 km2** | ✗ |
| **TSR** | | **0** |

**Four of six checks pass.** The artefact is technically correct and substantively useless. `detected_by = oracle` — after the fact, outside the loop, with no chance of repair. This is a **silent spatial error**, not "the model made a mistake". The whole run cost **three turns**: short and cheap, which is exactly the advantage the literature attributes to code generation.

### 12.2 N1 — the same task through the catalogue, schema only

The surface is the server's: `describe_layer`, `buffer`, `clip`, `export`. Every call is validated against its schema and **nothing about the result is checked**.

```
TURN 1  [model → tool call]
describe_layer(path="dane/drogi.gpkg")

TURN 1' [tool → model]        ← OBSERVATION: structure
  {"layer":"drogi","crs":"EPSG:2180","crs_name":"PUWG 1992/19",
   "area_of_use":"Poland","units":"metre","feature_count":2481}

TURN 2  [model → tool call]   ← the mistake, made legally
buffer(input="dane/drogi.gpkg", distance=5, unit="m", segments=5, dissolve=false)

TURN 2' [tool → model]
  {"handle":"r1","distance_used":5.0,"unit_used":"m","crs":"EPSG:2180","extent_grew":true}
        ↑ the call is valid, the echo is honest, and nobody has compared anything to the task

TURN 3  clip(input="r1", mask="dane/gminy.gpkg")
TURN 3' {"handle":"r2","feature_count":2481,"crs":"EPSG:2180"}

TURN 4  export(handle="r2", path="wynik/bufor_gminy.gpkg", target="EPSG:2180")
TURN 4' {"ok":true,"path":"wynik/bufor_gminy.gpkg","crs_written":"EPSG:2180"}
```

**The outcome on this card is the same as in K: TSR 0, `detected_by = oracle`.** That is the point of having N1 in the design and it is worth stating plainly, because it is the opposite of what a paper about "MCP validation" would want: **schema validation does not prevent this error.** What the surface has done is make the mistake *declarable* — `unit` is a required enum, so the model cannot silently forget the unit — but declaring `5 m` is as wrong as writing `DISTANCE: 5`, and no schema can tell.

N1 is therefore the control that makes H2 interpretable: it holds the surface, the descriptions, the prompt and the model constant and removes only the checks. If the difference between conditions were produced by *the catalogue being a catalogue*, N1 would already show it.

### 12.3 N4 — the same surface, with the checks on

The calls are character-identical to N1's; the arguments are the model's. What is added is `checks.yaml`: preconditions on the input, invariants on the result, and the card's terminal conditions.

```
TURN 1  describe_layer("dane/drogi.gpkg")        → as above
TURN 2  buffer(distance=5, unit="m", ...)
TURN 2' {"handle":"r1", "distance_used":5.0, "unit_used":"m"}     ✓ precondition: CRS present, geometry valid
TURN 3  clip(input="r1", mask="dane/gminy.gpkg")
TURN 3' ✗ {"isError": true, "code": "EXTENT_NOT_COVERING_MASK",
           "detail": "output extent covers 0.34 of the mask extent",
           "constraint": "terminal condition of the card: the result must cover the communes",
           "hint": "the buffer radius is 5 m; the task asks for 5 km"}
        ↑ caught INSIDE the loop, on the result, before the artefact is written
TURN 4  buffer(distance=5000, unit="m", ...)       ← repair
TURN 5  clip(...)                                   ✓ 0.97
TURN 6  export(...)                                 ✓ crs_written, geom_valid
```

**What caught it, exactly** — and this part has to be stated with precision, because it is the whole thesis in one transcript: not the schema (N1 had the same schema), not the enum (the model declared its unit correctly), but a **terminal condition derived from the card's own words**: *clip to the communes*. The surface knows the mask because the task named it, and it can therefore compare the result against it. That is P-III made machine-checkable by the card, and it is why the expressible share is the moderator of H3 rather than a footnote.

**Cost:** six model turns against three, and several times the tokens on this card. That price is a result, not a nuisance to be normalised away.

### 12.4 The same card in K, when the model does write the check

The interesting comparison is not K against N4 on a bad day; it is K on a **good** day, because that is what the S4 measure is counting. The same task, one turn longer:

```
TURN 1  run_python(code="""
  ...
  buf = processing.run("native:buffer", {"INPUT": drogi, "DISTANCE": 5000, ...})
  ...
  layers = QgsProject.instance().mapLayersByName("bufor")
  assert layer.extent().width() > 1000, f"extent too small: {layer.extent()}"
""")
```

Three things can happen, and all three are recorded:

- **the guard is right** — the extent check catches the metre/kilometre error before the clip, and the run repairs; `guard_present_in_code = true`, `detected_by = model`. This is the good case, and S4 measures how often it occurs.
- **the guard is wrong** — the model asserts something plausible and false (a width above 1 000 map units "must be right"), the assertion passes on a wrong artefact, and the run fails identically to §12.1 while *looking* careful. Nothing in the interpreter distinguishes a check from a decoration.
- **the guard is written after the failure** — the model sees a suspicious number, adds a check that encodes the same mistake, and the hint it writes for itself is not evidence.

This is why **S4 is not a quality measure**: it counts whether *any* check exists, and **S4b** separates domain checks (CRS equality, extent, area, feature count) from language checks (`try`, `if x is None`, a print). A code condition that writes many language checks and no domain checks is not verifying anything — and that pattern, not a single transcript, is what the thesis reports.

### 12.5 The transcript's honest caveats

1. **The advantage on this card comes from a design decision, not from "using the protocol".** A naive server — `buffer(input, distance)` with no unit and no terminal condition — behaves like K and the difference vanishes. That is why the depth contrast N1 → N4 exists: without it, the measurement would be of the author's server, not of the interface.
2. **Turns and tokens differ structurally.** They are reported as secondary results and never "balanced" away; integrating through a catalogue costs more steps, and that is part of what is being measured.
3. **The oracle does not know which channel produced the artefact.** Both conditions have the *same output contract*, not "a script versus calls" — which is what makes the oracle indifferent to the treatment.
4. **Rejection is not success.** If N4's checks were strict enough to reject correct artefacts, TSR would fall and the falsifier of H2 (a flat curve *with* a flat catch rate) would appear as a different pattern. The catch rate and the repair counter are what separate a working gate from an obstructive one.

---

## 13. One card where the catalogue loses

A fair document needs the counter-case, and family C supplies it. The requirement is *"a 300 DPI PNG with a title, a legend and a scale bar"*. The nine operations do not touch symbology, classification or layout, so:

| | K | N1 / N4 |
|---|---|---|
| What happens | the model writes three lines of `QgsPrintLayout` code and produces the image | the surface cannot express it; the model ends with `finish` and no artefact, or with an attributed failure |
| Error class | none, if the code is right | a task failure by construction |
| Who is responsible | the model | the surface |

This is the `none` value of the expressible share, and it is **the reason H3 is a claim at all**. If the catalogue arm also "won" here, the mechanism would be something other than what the surface can carry — which is why a difference on `none` cards refutes H3 instead of supporting it. It is also the honest answer to "why not just add tools": every added tool changes coverage, context cost and near-miss density at once (`design/tool-surface.md` §2), and a surface that could express everything would stop being a treatment.

---

## 14. The parity test, and how the code arm's guards are extracted

**Parity, at run level.** One script, pushed through both channels, must produce the **same artefact hash**: run it as `run_python(code)` in K and as the equivalent server calls in N4, then compare `SHA256SUMS`. Where the hashes differ, the difference must be attributable to the library call and not to a wrapper — a differing hash with identical inputs is a technical handicap of one condition, and it stops the series before the sweep (a gate-B failure, `design/harness.md` §12).

**Guard extraction, for S4 and S4b.** The code condition's scripts are captured as `calls.jsonl` arguments, and each is classified blind:

| Code | Test | Feeds |
|---|---|---|
| **S4** | does the script contain **any** check of the result — an assertion, a comparison, a conditional raise | "how often does the model even try" |
| **S4b** | among those, is the check **domain** (CRS equality, extent, area, feature count) or **language** (a `try`, an `if x is None`, a print) | the direct answer to "at most a syntax or a type error" |

Both are descriptive and **independent of the main result**, which is what makes them the insurance policy against a null: if the model writes a guard in 5 % of runs, that fact alone justifies a layer that does it always, whatever the TSR contrast shows.

The coding follows the same discipline as the failure taxonomy: 20 % of the captured scripts are classified blind by a second coder on transcripts without the `condition` column, κ is reported for both S4 and S4b, and κ below 0.6 sends the coding back rather than into a table. The scripts are archived in `calls.jsonl`, so a later re-coding needs no rerun — which matters, because S4b is the measure most likely to be re-examined by a reviewer who disagrees with what counts as a domain check.

---

## 15. Build order, and what to pin

| Step | Module | Indicative size |
|---|---|---|
| 1 | `sandbox.py` — container start, `exec(code)`, limits, artefact dump | ~150 lines |
| 2 | `mcp_server/` — the nine operations over `qgis_process` / `processing.run`, `tools/list` | ~300 lines |
| 3 | `loop.py` — one loop, three channels, budgets, logging | ~250 lines |
| 4 | `oracles/` — predicates for the pilot cards | ~30 lines per card |
| 5 | `checks/` — preconditions, invariants, terminal conditions; the repair counter | ~150 lines |
| 6 | `score.py`, `merge.py` — predicates to tables, with `--check` | ~200 lines |

Roughly **1,100–1,300 lines for the whole experiment**, and `FakeModel` plus the JSONL writing come **first**, before `loop.py`, so the loop is written against a test rather than against hope (`design/harness.md` §4). A ready-made CLI is thousands of lines nobody in this project controls.

**To pin in the manifest, or the result is not repeatable:** MCP protocol version, `mcp` SDK version, server version, harness commit; container digest with QGIS/GDAL/GEOS/PROJ versions; model digest, quantisation, chat template, temperature, `top_p`, `max_tokens`, seed; the surface hash; the truncation length; turn, time and token limits.

---

## 16. Five lines, and one sentence

1. **One loop, three channels** — the same client, prompt, budget and register, differing only in what the model may do and in whether results are checked.
2. **The catalogue conditions use a real MCP server** with `initialize`, `tools/list` and `tools/call`, because a schema pasted into a prompt measures a prompt.
3. **Schema validation does not prevent a silent spatial error** — on card A-01 the N1 condition fails exactly as the code condition fails, which is what makes the N1 → N4 contrast informative.
4. **What catches it is a terminal condition derived from the card's own words**, applied to the result inside the loop before the artefact is written — at a visible cost in turns and tokens.
5. **Every run leaves a directory whose last file marks completion**, which is what makes resume safe, rescoring possible and a half-written run visible.

**In one sentence.** A run is one loop over three channels in which the prompt, the budgets, the truncation and the register are identical and only the action channel differs, and on the card that matters the difference is not that the catalogue "validates parameters" but that a result can be compared against the task's own stated requirement before the file exists — which the same card shows failing identically at the schema and succeeding at the checks.

---

## 17. What was cut, and why

| Cut | Source note | Reason |
|---|---|---|
| the two-arm vocabulary throughout ("arm A / arm B"), with the tool table written for two | both notes | the design has three conditions; a two-arm transcript cannot show that N1 and N4 are the contrast, and it invites the reading that schema validation is the treatment |
| `min_surface: 1` in the card and the sentence "this card needs one operation" | `run-in-both-arms-a-01.md` §0 | the tool-size ladder is retired (`design/tool-surface.md` §2); the card carries its family, tier and expressible share instead |
| the surface ladder 5 / 15 / 30 / 50 and "the level chooses what the server publishes in `tools/list`" | `experiment-architecture.md` §6 | retired with the ladder; what survives is the true and useful part — the surface is a property of the server's registration, not of the prompt |
| the L1 / L3 / L4 ablation as the answer to "that is your server, not the protocol" | `run-in-both-arms-a-01.md` §3 | retired levels; the same defence is now carried by the N1 → N4 contrast with the catch rate as its falsifier |
| the "control slice: 15 tasks with opencode and goose" | `experiment-architecture.md` §1 | the front-end factor is retired (`d-2`, `d-4`); the descriptive product appendix is 48 runs and lives in `framing/what-we-study.md` §11 |
| the 25-turn figure as a design constant | `experiment-architecture.md` §4 | a budget, not a finding: it is now "the turn budget", pinned in the manifest, with the 10-minute ceiling as the only fixed number |
| the `turns_limit = 1` side condition | `experiment-architecture.md` §2 | one sentence of it survives in §2; at 80 tasks it would spend runs the depth contrast needs |
| three of the five "sentences for the thesis" | `run-in-both-arms-a-01.md` §5 | the transcript itself now does that work; one defence sentence survives, compressed into §12.5 |
| the "what this shows for measurement" table repeated from `design/arms-and-validation.md` | same §4 | it duplicated the `detected_by` and metric definitions owned elsewhere; the fields that matter are listed once, in §9 |
| the module-by-module line counts as a commitment | `experiment-architecture.md` §8 | kept as *indicative* and marked so; a promise of 1,000 lines in a design note is a number nobody can be held to |

**Added while pruning**, because the cut had removed the only home of the claim: the run directory as a contract with `result.json` written last (§7), the truncation and context rules with the reason each must be identical (§8), the error taxonomy mapped onto the five exclusion rules (§10), run identity and resume as idempotency (§11), the full three-condition transcript of card A-01 with the honest statement that **N1 fails exactly as K fails** (§12), the counter-case from family C (§13), and the parity test plus the guard extraction that produces S4 and S4b (§14).

**Kept, because each is the only place in the repository where its claim is made:** the one-loop/three-channels decision with the list of what must be identical (§1), the agent-versus-LLM answer and the native-tool-calling qualification (§2), the component diagram with the shared-engine line (§3), the loop with its observation points (§4), the `run_python` variant choice with its safety rules (§5), what "using MCP" concretely means and where the surface lives (§6), the observation table and what each field feeds (§9), the build order with `FakeModel` first (§15), and the manifest pin list (§15).
