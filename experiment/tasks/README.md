# `experiment/tasks/` — task cards, fixtures, oracles

The **canonical** card specification for the thesis sweep. If any other document describes the card
shape differently, this file wins; if any other document states how many cards there are, that
document owns the number and this one quotes it (`design/corpus.md` §1 is the owner: **80 cards**,
**r = 4 repetitions**, **960 runs**, `d-2`).

Status: **specification first, cards second.** The 80 cards are not written yet — what exists is the
40-card seed catalogue in `thesis/design/corpus.md` §4 that fixes the method, the family balance and
this schema. The loader lands with the first cards (`TASK-15`), the register with `TASK-16`.

```text
experiment/tasks/
├── README.md          ← this file (schema + vocabularies + oracle contract)
├── cards/             ← one YAML per card: P-01.yaml … A-01.yaml … C-01.yaml …
├── fixtures/          ← input data, content-pinned in fixtures/SHA256SUMS
├── oracles/           ← reference implementations, one per card: oracles/P-01.py
└── rejected.md        ← the register of rejected tasks and why (`design/corpus.md` §5)
```

**One name to settle.** `design/harness.md` §11 calls this directory `corpus/cards/` when it lists
the frozen bundle for Gate A; in the repository it is `experiment/tasks/cards/`. The checker accepts
cards under either path so that nothing is silently unchecked, but two names for one directory is a
question for `TASK-15`, not a state to leave standing.

**Why YAML and not TOML.** A prompt is multi-line prose and `oracle.checks` are records with
arguments; TOML's `'''` blocks push both into the margins. Cards are human-authored and frozen, never
machine-written, so the format's job is to be reviewable in a diff. The consequence to respect: `pyyaml` is declared in
`feature.harness` — the feature that holds the loader — and pinned `==6.0.3`, not inherited from a
neighbour. Inheriting it is exactly how the alint/PyYAML breakage happened in this repository.

---

## 1. Card schema

Every card is one YAML mapping. **Unknown keys are errors, not warnings**: a typo that silently drops
`expressible` invalidates the moderator, and nothing downstream would notice.

### 1.1 Top-level keys

| Key | Type | Req. | Allowed values / meaning |
|---|---|---|---|
| `schema` | int | ✔ | `1`. Bump only with a migration note in §6. |
| `id` | str | ✔ | `P-nn` · `A-nn` · `C-nn`; must equal the filename stem and agree with `family`. |
| `family` | str | ✔ | `P` preparation and IO · `A` analysis · `C` cartography — the **selection axis** (`d-3`) |
| `tier` | str | ✔ | `T1` single call · `T2` 2–4 steps · `T3` 6–10 steps · `T4` under-specified — the difficulty factor |
| `expressible` | str | ✔ | `all` · `most` · `part` · `none` — share of the task the **nine named operations** can carry; the **moderator** of H3 (`TASK-4`) |
| `prompt` | str | ✔ | The exact user turn, identical in all three conditions. Rules in §3. |
| `inputs` | list[str] | ✔ | Paths relative to `fixtures/`, e.g. `["drogi.gpkg", "gminy.gpkg"]`, pinned in `fixtures/SHA256SUMS` |
| `expected_artifact` | str \| list[str] | ✔ | The file or files the run must produce, as named in the prompt |
| `preconditions` | list[str] | | e.g. `["crs:EPSG:2180"]`, `["no network"]` — the precondition gate of `design/experiment.md` §8.1 |
| `pitfalls` | list[str] | ✔ | The **silent** errors the card is designed to provoke: CRS, unit, NoData, geometry type, boundary truncation |
| `licence` | str | ✔ | Licence of any reused material; `n/a` for original work |
| `created` | str | ✔ | `YYYY-MM-DD` |

### 1.2 `[oracle]` — always present

| Key | Type | Req. | Meaning |
|---|---|---|---|
| `reference` | str | ✔ | `oracles/<id>.py`, relative to `experiment/tasks/` |
| `seed` | int | ✔ | The seed the reference runs under; the reference artefact must be byte-stable for it |
| `checks` | list[map] | ✔ | Typed predicates with tolerances (§2.2). At least **four**, never a similarity score |

### 1.3 `[negative_control]` — always present

`design/experiment.md` §8.3 puts the negative control **in the card**, not in the analysis: a
tolerance nobody ever tried to break is a tolerance that has not been calibrated (`design/corpus.md`
§5 rule 3).

| Key | Type | Req. | Meaning |
|---|---|---|---|
| `artifact` | str | ✔ | The artefact that *looks* right and must be rejected, described in one line |
| `must_fail` | list[str] | ✔ | The `checks` types it must fail — non-empty, and drawn from the card's own `checks` |

### 1.4 `[provenance]` — for adapted material

| Key | Type | Meaning |
|---|---|---|
| `borrowed` | str | What exactly was taken (`task family`, `difficulty ladder`, `instruction style`) |
| `changed` | str | What was re-instantiated on our own fixtures |

Admission rule 5 requires `provenance` whenever the inspiration was a public question or a benchmark;
rule 7 (no answer on the web) is checked by searching the phrasing once it is written.

---

## 2. Controlled vocabularies

### 2.1 `family`, `tier`, `expressible`

| Axis | Values | Role |
|---|---|---|
| `family` | `P` · `A` · `C` | the selection axis (`d-3`); at least 13 tasks per family |
| `tier` | `T1` … `T4` | difficulty spread; at least 8 cards in the deep tier (T3–T4) |
| `expressible` | `all` · `most` · `part` · `none` | the moderator of H3; when the share is not `all`, name the missing operations in `notes` |

`family C` (cartography) is where the floor effect comes from: none of the nine operations touches
symbology, classification or layout, so a cartographic task is at best `part` and at worst `none`
(`design/corpus.md` §4).

### 2.2 `checks` — typed predicates, not similarity

`checks` is a list of mappings `{type: <predicate>, …arguments}`. The predicates compare the produced
artefact against the reference artefact; each carries its tolerance where a tolerance exists.

| Predicate | Arguments | Meaning |
|---|---|---|
| `crs_equal` | `value` | CRS of the output equals the reference's (`"EPSG:2180"`) |
| `geom_valid` | — | OGC-valid geometries, no self-intersections |
| `extent_iou` | `value` | IoU of bounding boxes against the reference, e.g. `0.95` |
| `feature_count` | `value` | Feature count equals the reference's |
| `attr_present` | `value` | Columns present (`[gmina_id]`) |
| `attr_exact` | `value` | Columns present **and** equal |
| `numeric` | `field`, `tol_pct` | Field within a relative tolerance of the reference value |
| `topology` | `value` | Pairwise predicate on the output layer, e.g. `no_overlap` |
| `scalar` | `tol` | Single value within an absolute tolerance |
| `refusal` | — | The agent must decline; any artefact fails |
| `handle_carries_georeference` | `value` | An in-memory handle still carries CRS and nodata (`design/experiment.md` §8.1) |
| `renderer_type` | `value` | Cartography: `graduated`, `categorised`, … |
| `class_count` | `value` | Cartography: number of classes |
| `class_method` | `value` | Cartography: `equal_interval`, `quantile`, … |
| `fields_used` | `value` | Cartography: the fields the styling reads |
| `image_not_empty` | — | Cartography: the raster is not blank |
| `dpi` | `value` | Cartography: export resolution |

Two rules on the set, both structural rather than stylistic:

1. **At least four checks**, including **always one that catches a silent error** — without it the
   card cannot produce the failure it was selected for.
2. Every task whose artefact is a layer carries at least one **geometric** and one **attribute**
   check; otherwise "wrong map, right table" scores as success.

### 2.3 Worked example

The smallest complete card — every key, nothing decorative. The three examples with real Polish
data are in `design/corpus.md` §6, and both sets are checked by the same rule.

```yaml
schema: 1
id: P-07
family: P
tier: T2
expressible: all
prompt: >
  For the layer dane/obszary.gpkg (EPSG:2180) compute each feature's area in
  square metres and write it to the field `area_m2`. Save wynik/bilans.gpkg.
inputs: [obszary.gpkg]
expected_artifact: wynik/bilans.gpkg
oracle:
  reference: oracles/P-07.py
  seed: 42
  checks:
    - {type: crs_equal,    value: "EPSG:2180"}
    - {type: geom_valid}
    - {type: attr_present, value: [area_m2]}
    - {type: numeric,      field: area_m2, tol_pct: 0.1}
negative_control:
  artifact: the area computed on the layer's degrees instead of its metres
  must_fail: [numeric]
pitfalls: [area in degrees instead of metres]
licence: n/a
created: 2026-11-07
```

---

## 3. Prompt rules

The prompt is the only thing shared verbatim across K, N1 and N4; if it leaks the paradigm the
comparison is dead.

1. No mention of tools, functions, MCP, servers, code, Python, QGIS or any API — the task is stated as
   an analyst's request (`"Buffer the roads by 5 km and clip them to the gminy"`, never
   `"call buffer() with …"`).
2. State the output contract: which file, which CRS, which unit, which columns.
3. Ambiguity is deliberate in `T4` cards but must be *decidable*: two competent analysts must reach
   the same answer, or the check cannot be defined.
4. Write it as a user would type it, including the vagueness. Do not pre-decompose into steps —
   decomposition is the dependent variable.
5. Keep it under ~60 words. Longer prompts measure prompt engineering rather than the protocol.

---

## 4. Oracle contract

An oracle is a plain script, no agent involved, that produces the reference artefact.

```bash
python experiment/tasks/oracles/P-01.py --fixtures experiment/tasks/fixtures --out out/P-01-ref
```

- Reads only the files named in `inputs`, writes only under `--out`.
- **No network.** Deterministic for `[oracle].seed`; a re-run must produce an identical artefact
  (strip timestamps, sort by a stable key, fixed float formatting).
- Prefers the plain library path (GeoPandas/Shapely) over QGIS, so the reference does not depend on
  the server implementation. Where the task must use a QGIS algorithm, say so in the card and pin
  QGIS 3.44 in the results chapter.
- Exit 0 on success; any other code means the card is broken, not that the agent failed.

---

## 5. The retired generation, and why it is not coming back

This file used to specify a **different** corpus, and the shape of that one is worth knowing only so
that it is not reintroduced by accident:

| Retired | Why it went | Where that is decided |
|---|---|---|
| 50 cards, `T001`…`T050` | the live design is **80 cards** in families P / A / C | `d-2`, `design/corpus.md` §1 |
| TOML card files | prompts and checks read badly in TOML (§ this file's header) | — |
| blocks `A`/`B`/`C`/`D` (anchored / custom / **adversarial** / transfer probe) | block `C` meant *adversarial*, while `family C` now means *cartography*; the collision alone is disqualifying | `design/experiment.md` §14 |
| `min_surface` + the `mcp5 ⊂ mcp15 ⊂ mcp30 ⊂ mcp50` ladder | the tool-count ladder is retired; the surface is fixed at nine operations | `design/tool-surface.md` §2, `design/runs.md` §"what changed" |
| `tools_required`, `tools_optional`, `distractors` | they only meant something against that ladder | `design/tool-surface.md` §2 |
| `expected_classes` | failure classes are coded from `checks.jsonl` by rule, not declared per card | `design/experiment.md` §8.2 |
| `[adversarial]` (`attack`, `target`, `success_if`) | adversarial cards are deliberately outside the design — "three cards would be a sample, not a test" | `design/experiment.md` §15 |
| `answer_form` | every artefact is a file; a scalar or a snippet is not admissible | `design/corpus.md` §5 rule 1 |
| `reference_steps` (PEA) | process efficiency is not among the six measures; cost is measured from `calls.jsonl` per successful task | `design/experiment.md` §7 |

The card carries its **family, tier and expressible share** instead of a surface size — that swap is
the whole difference between the two generations, and it follows from the design change that made the
surface a constant.
