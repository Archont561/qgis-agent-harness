---
id: design/corpus
title: "The corpus: how many tasks, which ones, and why"
type: note
status: live
language: en
question: "How large must the task set be, and how is it chosen without begging the question?"
tasks: [TASK-3, TASK-4, TASK-21]
sources: [tasks-40.md, tasks-per-domain.md, representativeness-and-task-count.md, task-count-decision.md, mvp-what-task-and-tool-counts-measure.md, paired-templates.md, selection-objection-how-to-answer.md]
updated_date: '2026-11-07'
---

# The corpus: how many tasks, which ones, and why

> How large must the task set be, and how is it chosen without begging the question?
>
> Merged 2026-11-07 from `tasks-40.md`, `tasks-per-domain.md`, `representativeness-and-task-count.md`, `task-count-decision.md`, `mvp-what-task-and-tool-counts-measure.md`, `paired-templates.md`, `selection-objection-how-to-answer.md`. **Pruned and translated the same day** (`TASK-21`): 13,379 → ~7,600 words. What was cut, and why, is listed in §11 — the rejected generation is kept there as one line each, not as three sections.

**The configuration this document is written against** (decisions `d-1`, `d-2`, `d-3`):

| Quantity | Value | Source |
|---|---|---|
| Arms | **K** (code, `run_python`), **N1** (nine named operations + JSON schemas), **N4** (the same nine + invariants + terminal conditions) | `d-1`, `design/arms-and-validation.md` |
| Task cards | **80** | `d-2`, `TASK-3` |
| Repetitions | **r = 4** | `d-2` |
| Runs | 80 × 4 × 3 = **960** | `design/experiment.md` |
| Smallest detectable difference | **14.0 pp** at τ = 10 pp | `d-2`, §7 |
| Unit of inference | the **task**, never the run | §7 |
| Axis of task selection | family **P / A / C**; domain is a descriptive label | `d-3` |
| Moderator | the **expressible share** of the nine operations, coded on the card | `TASK-4`, §3 |

---

## 1. Where the tasks come from

**From practice, not from benchmarks — but the scoring pattern is taken from benchmarks.** Three sources, in this order:

| Source | What it gives | Share |
|---|---|---|
| **GIS practice** (what an analyst actually does: preparing data, analysing it, making maps) | realism and coverage of the P/A/C families | ~70 % |
| **Practitioners' questions** (GIS Stack Exchange — used as a *pattern*, never copied) | the phrasings that really cause trouble: CRS, units, NoData, boundaries | ~20 % |
| **Method literature** (GeoContra, GeoTool-GPT, the `zhang2025msb` error taxonomy) | the classes of error a task is meant to provoke | ~10 % |

**The rule:** every task is **recast onto our own data and our own geography**. No task text, dataset or reference solution is copied — for the same reason GISAgentBench recasts its tasks onto new areas: so that a published answer does not exist on the web. Each card carries a filled `provenance` field; without it, forty tasks from one desk and forty tasks from three sources are indistinguishable.

## 2. What the benchmarks give, and what they leave

| Benchmark | Tasks | Where the tasks come from | Environment | How it scores | What it does **not** give |
|---|---|---:|---|---|---|
| **GeoAnalystBench** (Zhang et al., *Transactions in GIS* 2025) | 50 | tutorials and papers | **ArcPy** code generation | CodeBLEU + workflow-length deviation + validity | **no artefact** — it scores similarity to an expert solution, three answers per prompt |
| **GeoAgentBench** | 53 | handbooks | 117 tools | trajectory match + a **VLM judge looking at the map** | no hard ground truth; a VLM judge is a proxy signal |
| **GISAgentBench** (arXiv 2608.01645, VIII 2026) | **349** | **GIS Stack Exchange** | 128 APIs over QGIS / GeoPandas / Rasterio / Shapely | **exact truth file + tolerance matching**; best agent **32.7 %** | no cartographic family (announced as future work), one environment, no interface manipulation |
| ComplexMCP · MCPToolBench++ · Live API-Bench | 120–300+ | sandboxes, live APIs | general | execution + argument correctness | **not GIS** — they do not transfer to spatial predicates |

**The conclusion to have ready for the defence:** GISAgentBench **confirms** the design of this thesis (artefact truth, tolerances, tasks taken from practitioners) but **does not make it redundant** — it measures **one** interface, it does not compare two, and it has **no cartography**, which is the third family here. It is also the **novelty risk**: since August 2026 the proximity is high, so the thesis has to cut itself away from it in one sentence:

> "GISAgentBench (2026) established that GIS agents must be scored on **truth files with tolerances**, and that approach is adopted here. The difference is the **manipulation, not the metric**: there, one interface is measured on 349 tasks from the analytical families; here, **three ways of exposing the same nine operations** are compared on 80 tasks, including **cartographic tasks** that the other corpus deliberately does not contain."

## 3. The class of tasks the corpus describes

The corpus is not a sample from a defined population (§7.3); it is a **stratified purposive selection** with a written frame. The frame is three axes, and only the first two select:

| Axis | Values | Role |
|---|---|---|
| **Family** | **P** preparation and IO · **A** analysis · **C** cartography | **the selection axis** (`d-3`) |
| **Tier** | T1 single call · T2 2–4 steps · T3 6–10 steps · T4 under-specified | selection, to keep the difficulty spread |
| **Domain** | business, visibility, ecology, spatial planning, geology, geomorphology, data management and formats, geovisualisation | **a label only**, reported descriptively (§8) |
| **Expressible share** | the fraction of the task that the nine named operations can carry: *all · most · part · none* | the **moderator** of C2 (`TASK-4`) |

The expressible share replaces the `min_surface` column of the retired tool-count ladder (§11). It matters because it is what makes the second research question answerable: `d-3` and turn-of-design reasoning say the difference between the interfaces should **grow** with the expressible share, and be **absent or negative** where the nine operations cannot express the task at all — which is the expected fate of much of family C, and the reason W6 (floor effect) is written down before the sweep.

**Claims are about this class, not about "GIS tasks".** The sentence belongs verbatim in §3 of the thesis:

> "The corpus is a stratified purposive selection with a documented frame (family × tier), written admission rules and a register of rejected tasks. It is not a random sample, because the population of GIS tasks has no register; results are therefore stated for the class of tasks defined in §4.2, not for GIS tasks in general."

This is not a weakness relative to the benchmarks — it is **the same standard**, said honestly: GISAgentBench draws 349 tasks from one forum (availability selection), GeoAnalystBench 50 from tutorials, GeoAgentBench 53 from handbooks. None is a random sample and none claims to be.

## 4. The seed catalogue: 40 cards, and how the 80 are built from them

The 80 cards of `TASK-3` are not yet written. What exists is a **40-card seed catalogue** that fixes the method, the family balance and the card schema; the remaining 40 extend it under the same admission rules (§5), keeping at least 13 tasks per family and at least 8 in the deep tier (T3–T4), where the seed has only 2 in T4.

Legend: **T** = tier · **P** = number of predicates in the oracle.

### Family P — preparation and IO (14)

| ID | Task | T | P | The trap it provokes |
|---|---|---:|---:|---|
| P-01 | Load `drogi.gpkg`, reproject from EPSG:4326 to 2180, save | T1 | 4 | **silent CRS error** |
| P-02 | Clip a polygon layer to a voivodeship boundary | T1 | 4 | extent / geometry truncation |
| P-03 | Convert SHP→GPKG preserving Polish characters in attributes | T1 | 5 | encoding, field length |
| P-04 | Merge two point layers and drop duplicates by `id` | T2 | 5 | feature count after the merge |
| P-05 | Join a CSV to a layer by key, keeping numeric types | T2 | 6 | data type, key matching |
| P-06 | Repair invalid geometries and report how many were repaired | T2 | 5 | **invalid geometry** |
| P-07 | Extract polygon centroids with selected attributes | T1 | 4 | feature count, point-in-polygon |
| P-08 | Drop features with an empty `ludnosc` value | T1 | 4 | **null ≠ 0** |
| P-09 | Export to GeoJSON in 4326 with coordinate precision to 6 places | T2 | 5 | axis order, precision |
| P-10 | Split a layer into points / lines / polygons | T2 | 5 | geometry type |
| P-11 | Compute **area in metres** for a layer in 2180 | T2 | 4 | **area in degrees instead of metres** |
| P-12 | Clip a DEM raster to a vector extent, keeping resolution | T2 | 5 | cell size, NoData |
| P-13 | Mosaic three raster tiles, preserving NoData | T3 | 6 | empty values, tile edges |
| P-14 | Reorder and rename fields to a target schema | T2 | 5 | schema, attribute loss |

### Family A — analysis (13)

| ID | Task | T | P | The trap it provokes |
|---|---|---:|---:|---|
| A-01 | 5 km buffer around roads, intersected with gmina boundaries | T2 | 5 | radius unit (m vs km) |
| A-02 | Variable-distance buffer from the `szer_m` field | T3 | 5 | field instead of a constant |
| A-03 | Assign points to polygons and count points per unit | T3 | 6 | assignment on the boundary |
| A-04 | Total protected-area surface per gmina | T3 | 6 | overlapping polygons → double counting |
| A-05 | Intersect two layers and take the area of the common part | T2 | 5 | topology of the result |
| A-06 | Dissolve by attribute and count multipart parts | T2 | 5 | parts, not features |
| A-07 | Road-network length inside a 2 km buffer | T3 | 6 | line truncation at the boundary |
| A-08 | Zonal statistics: mean raster value inside polygons | T3 | 6 | cells partly inside the polygon |
| A-09 | For each point, the nearest feature and its distance | T2 | 5 | metric CRS vs degrees |
| A-10 | Union of two classifications and a cross table of classes | T3 | 6 | class mapping |
| A-11 | Select sites: ≥300 m from roads, ≤500 m from rivers, within boundaries | T4 | 6 | three conditions at once, thresholds |
| A-12 | Feature density per km² on a 1 km grid | T3 | 6 | grid unit, features on the edge |
| A-13 | Compare the area of the same layer in 2180 and in 3857 | T3 | 4 | **projection distortion** |

### Family C — cartography (13)

| ID | Task | T | P | The trap it provokes |
|---|---|---:|---:|---|
| C-01 | Five-class quantile classification, sequential palette | T2 | 6 | class count, method, palette |
| C-02 | Labels from the `nazwa` field, 9 pt, white halo | T2 | 5 | label field, size |
| C-03 | 300 DPI PNG export with title, legend and scale bar | T2 | 7 | DPI, layout elements |
| C-04 | Categorical symbology on `typ`, four categories, qualitative palette | T2 | 6 | category count, renderer type |
| C-05 | Seven equal-interval classes **and** seven quantile classes — two artefacts | T3 | 6 | classification method |
| C-06 | Two layers: background at 50 % opacity plus a theme | T2 | 5 | layer order, opacity |
| C-07 | Labels only for the five largest units | T3 | 6 | filtering by expression |
| C-08 | A4 landscape layout with a coordinate grid and scale bar | T3 | 7 | layout, elements, format |
| C-09 | Jenks classification with a legend describing the classes | T2 | 6 | method, descriptions |
| C-10 | Line width by attribute plus a dashed pattern | T3 | 6 | multi-level symbol |
| C-11 | Atlas: two pages, one unit per page | T4 | 6 | atlas coverage, page count |
| C-12 | Point heat map with a 300 m radius | T2 | 5 | radius, unit |
| C-13 | Map with missing data shown (NoData in its own colour) | T3 | 6 | **null ≠ zero**, legend |

**Counted from the tables, not from memory:** families **P 14 · A 13 · C 13**; tiers **T1 5 · T2 19 · T3 14 · T4 2**.

Family C is where the floor effect comes from: the catalogue holds nine primitive operations — **describe a layer, buffer, clip, intersect, union, spatial join, zonal statistics, reproject, export** (`draft/thesis-draft-v0.md`; `TASK-5`) — and none of them touches symbology, classification or layout, so a cartographic task is at best *partly* expressible (`TASK-4`), and at worst not at all. That is not a defect of the corpus — it is the **expected cause of W6**, and the reason the expressible share is coded per card before the sweep.

## 5. Admission rules

A task enters the corpus only if all seven hold:

1. **The artefact is a file** — not an "answer", not a code snippet.
2. **At least four predicates**, including **always one that catches a silent error** (CRS, unit, NoData, geometry type).
3. **A negative control exists**: it is possible to build an artefact that *looks* right and **must** be rejected.
4. **Executable in every arm** — each task has a counterpart in the catalogue of nine operations and can be written in PyQGIS. Where it cannot be expressed by the nine operations, the card says so through its expressible share, and the task stays in the corpus on purpose.
5. **`provenance` filled in**, whenever the inspiration was a public question or a benchmark.
6. **The expressible share is coded**, with the operations that are missing, when any are.
7. **No answer on the web** — after the task is phrased, search the phrasing and check that it does not copy a published solution.

Rejected tasks are **registered with their reason**. That register is part of the evidence of coverage: it is the only artefact that separates purposive selection from convenient selection.

## 6. Three cards in full

The **canonical** schema is `experiment/tasks/README.md` (§1 keys, §2 vocabularies, §4 oracle
contract); these three show the shape and are checked against it — `task-card-schema-docs` in
`.alint.yml` parses exactly these blocks, so an example that drifts from the schema fails
`pixi run qa`. Two details are load-bearing: `oracle.checks` are typed predicates with tolerances
(never a similarity score), and `pitfalls` plus `negative_control` are what stop the predicate set
from being a wish.

```yaml
schema: 1
id: P-01
family: P
tier: T1
expressible: all            # the nine operations carry the whole task
prompt: >
  Load dane/drogi.gpkg, reproject it from EPSG:4326 to EPSG:2180 and
  save it as wynik/drogi_2180.gpkg.
inputs: [drogi.gpkg]
expected_artifact: wynik/drogi_2180.gpkg
oracle:
  reference: oracles/P-01.py
  seed: 42
  checks:
    - {type: crs_equal,     value: "EPSG:2180"}
    - {type: geom_valid}
    - {type: feature_count, value: 8421}
    - {type: extent_iou,    value: 0.99}
negative_control:
  artifact: the layer saved in EPSG:4326 with the attribute table intact
  must_fail: [crs_equal]
pitfalls: [silent CRS error, system not written to the file]
licence: n/a
created: 2026-11-07
```

```yaml
schema: 1
id: A-01
family: A
tier: T2
expressible: all
prompt: >
  Buffer the roads in dane/drogi.gpkg by 5 km and clip the result to the gmina
  boundaries in dane/gminy.gpkg. Save wynik/bufor_gminy.gpkg in EPSG:2180.
inputs: [drogi.gpkg, gminy.gpkg]
expected_artifact: wynik/bufor_gminy.gpkg
oracle:
  reference: oracles/A-01.py
  seed: 42
  checks:
    - {type: crs_equal,     value: "EPSG:2180"}
    - {type: geom_valid}
    - {type: extent_iou,    value: 0.95}
    - {type: feature_count, value: 2481}
    - {type: numeric,       field: area_km2, tol_pct: 0.5}
    - {type: attr_present,  value: [gmina_id]}
negative_control:
  artifact: the buffer computed with the radius read as degrees
  must_fail: [numeric, extent_iou]
pitfalls: [radius unit, boundary truncation]
provenance:
  borrowed: instruction style of GIS Stack Exchange questions
  changed: recast on Polish road and gmina layers; nothing quoted
licence: n/a
created: 2026-11-07
```

```yaml
schema: 1
id: C-05
family: C
tier: T3
expressible: none           # no classification call among the nine operations
prompt: >
  Make two maps of population by gmina: (a) seven equal-interval classes,
  (b) seven quantile classes. Same sequential palette, same legend with the
  same number of classes. Save wynik/klasy_eq.png and wynik/klasy_q.png (300 DPI).
inputs: [gminy.gpkg]
expected_artifact: [wynik/klasy_eq.png, wynik/klasy_q.png]
oracle:
  reference: oracles/C-05.py
  seed: 42
  checks:
    - {type: renderer_type,   value: graduated}
    - {type: class_count,     value: 7}
    - {type: class_method,    value: [equal_interval, quantile]}   # per artefact
    - {type: fields_used,     value: [ludnosc]}
    - {type: image_not_empty}
    - {type: dpi,             value: 300}
negative_control:
  artifact: both panels drawn with the same classification method
  must_fail: [class_method]
pitfalls: [classification method, legend/class mismatch]
provenance:
  borrowed: cartographic predicate set
  changed: written against `design/correctness.md`; no benchmark task reused
licence: n/a
created: 2026-11-07
```

## 7. How many tasks: what tasks buy, and what repetitions cannot

### 7.1 Three quantities that get conflated

| Concept | What it is | What raises it | Does the corpus have it? |
|---|---|---|---|
| **number of units** | independent units in the analysis | more **tasks** (not runs, not twins) | 80 → df = 79 |
| **precision** | narrowness of the interval around the contrast | repetitions (up to the floor), a binary predicate outcome, pairing | yes, r = 4 on 80 tasks |
| **coverage** | how many cells of the design space hold at least one task | tasks in thin cells | 6 of 6 in the 3 × 2 arrangement (family × depth), T4 thin |
| **representativeness** | whether the sample reproduces the **distribution of a trait in a population** | the **selection procedure**: stratified drawing or an explicit frame plus a register of rejects | **no** — and not attainable by counting tasks |

The first three are numbers; the fourth is a **property of a procedure**. That is why "is 80 a lot?" has no answer without "a lot **relative to what** and **with respect to which trait**". Representativeness is a three-place relation — sample *S*, population *P*, trait *X* — and here *P* (GIS tasks phrased in natural language) has no register from which anything could be drawn.

### 7.2 Tasks buy reach, repetitions buy precision, and nothing buys representativeness

| Lever | Cost | What it changes |
|---|---|---|
| more **tasks** | ~1 day of authoring each (oracle, card, tolerance calibration, validation) | lowers the **floor** of the MDE, widens the class the claim covers |
| more **repetitions** | runs only | reduces binomial noise, **only down to the floor** |
| a **better estimator** (paired contrast, mixed model, binary outcome) | 0 runs | removes the between-task component from the standard error of a paired contrast |
| a **selection procedure** | 0 runs | the only thing that buys representativeness, and only relative to a stated population |

The power model used throughout, with τ the between-task standard deviation of the interface effect, N the number of task cards and r the repetitions:

```
MDE ≈ 3.42 · sqrt(tau² + 4950 / r) / sqrt(N)      [percentage points]
```

The constant 4950 is the binomial term at p = 0.5, the worst case; on the corpus distribution actually measured (mean TSR 0.51, SD 0.22) it is ≈ 0.40, so the table is slightly conservative.

At the live configuration (τ = 10 pp):

| N \ r | 4 | 8 | 16 | 32 | floor (r → ∞) |
|---:|---:|---:|---:|---:|---:|
| **40** | 19.8 | 14.5 | 10.9 | 8.6 | 5.4 |
| **80** | **14.0** | 10.3 | 7.7 | 6.1 | **3.8** |
| **160** | 9.9 | 7.2 | 5.5 | 4.3 | 2.7 |

Two readings, both of which belong in chapter 3:

1. **`d-2` is exactly the bold cell.** 80 tasks × 4 repetitions gives 14.0 pp. Going down to 7.7 pp would take **16 repetitions on 80 tasks — 3,840 runs at three arms**, four times the series. That is the arithmetic behind the decision, and it should be quoted as arithmetic rather than as preference.
2. **The floor moves only with N.** At τ = 10 pp no number of repetitions goes below 5.4 pp on 40 tasks, 3.8 pp on 80, 2.7 pp on 160. At τ = 0 the horizon would be unlimited — but τ = 0 means "both interfaces help exactly the same tasks by exactly the same amount", which is the negation of the hypothesis under test.

### 7.3 The same budget spent on tasks instead of repetitions

At τ = 10 pp, compare two moves of **+640 runs each** (three arms): r 4 → 8 on 80 tasks falls from 14.0 to 10.3 pp; N 40 → 80 at r = 4 falls from 19.8 to 14.0 pp **and lowers the floor from 5.4 to 3.8 pp**. The second move buys more and buys it permanently, which is why the corpus is the first thing to grow and repetitions are not.

The honest limit is authoring cost, not compute: a task costs about a day (oracle, card, tolerance calibration, qualitative validation), so twelve tasks are two to three weeks of afternoons. **Every task added to raise power is a week traded for a few points that a free estimator change already gives; a task added to cover a thin cell or a family is worth its price.**

### 7.4 Grouping: why the run count is not the sample size

With ICC(1,1) = 0.661 measured on the pilot distribution, the design-effect inflation is `DEFF = 1 + (r − 1) · ICC`:

| repetitions r | 4 | 8 | 16 | 32 | 60 |
|---|---:|---:|---:|---:|---:|
| DEFF | 3.0 | 5.6 | 10.9 | 21.5 | 40.0 |

Reading 960 runs "by rows" believes in 960 observations; at r = 4 it actually has **~320 rows worth independent units**, and for statements about a *level* (not a difference) the between-task variance eats the sample down towards 80. But **not for the primary contrast**: the same task runs in all three arms, so the task's difficulty term cancels exactly and does not enter the standard error of the paired difference. What is left in that denominator is τ — the heterogeneity of the interface effect itself — plus binomial noise. This distinction is the whole reason repetitions are worth buying, and the whole reason they do not replace tasks.

The thesis says: "**80 tasks, four repetitions per task and arm; the unit of inference is the task**" — never "960 observations".

### 7.5 Cells: where the corpus becomes thin

MDE for a **single cell** holding n_c tasks, at r = 4, τ = 10 pp:

| n_c | 5 | 10 | 13 (one family) | 20 | 40 |
|---|---:|---:|---:|---:|---:|
| MDE | **55.9 pp** | 39.5 pp | 34.7 pp | 28.0 pp | 19.8 pp |

To say anything about a *cell* at 15 pp would take ~140 tasks in that cell. Therefore:

- inference is **pooled only** (one paired contrast over 80 tasks);
- the 3 families × 2 depths (shallow T1–T2 / deep T3–T4) split is **descriptive** — reported with intervals and an explicit caveat, not tested;
- if tasks are ever added "for more coverage", they go **first into T4, where there are 2**, not into T2, where there are 19 and the information gain is smallest.

### 7.6 Five moves that really raise coverage

In order of gain per price, not counting authoring days:

1. **Fill the thin cells.** T4 = 2 → 8 is +6 tasks and the cheapest reach available: today every claim about the deepest tasks stands on two units.
2. **Qualitative variety, not variants.** A new trap, a new surface shape, a new error class — not a second version of the same template. A twin is **not a new unit** (§9).
3. **Variety of origin.** 70 / 20 / 10 (§1), written into `provenance`. Without it nobody can tell forty tasks from one desk from forty tasks from three sources.
4. **A register of rejects** (§5). "What I rejected" is part of the evidence of coverage.
5. **Report stratified, not one average.** A single pooled TSR is dragged by the easiest cells; with 5 tasks in T1 and 19 in T2 the average mostly describes T2.

A sixth, not about counting: **saturation**. When a new card adds no new error class and no new trap, selection is saturated — a substantive argument, stronger than any count, and worth computing ("after 40 cards, new cards introduced no new error class in 9 of 10 cases").

### 7.7 Three traps

1. **Adding tasks after seeing results** is a change of the stopping rule, not a larger sample. N, tolerances and predicates are frozen before the sweep.
2. **Counting twins as N.** 60 instances over 40 templates are 40 units; counting 60 understates the MDE by √(60/40) = 1.22× and reintroduces pseudo-replication one level up.
3. **Writing "960 observations" in §3.** A methodology reviewer will compute the degrees of freedom in a minute.

## 8. Domains: descriptive, measured, weighted

`d-3` says domains are not a variable. This section is why that is not a dodge but the only defensible position — and it is backed by two measurements made on 1 XI 2026.

### 8.1 What practitioners actually stop on — GIS Stack Exchange

Question counts for the tags assigned to each domain (Stack Exchange API, `site=gis`, the 397 most frequent tags; the tag → domain mapping is **my judgement** and is printed in full so it can be challenged):

| Domain | Tags (question sum) | Share of the 38,558 total |
|---|---|---:|
| **Data management and formats** | coordinate-system 8,645 · shapefile 5,698 · convert 1,474 · csv 1,458 · file-geodatabase 1,056 · geopackage 693 | **49.3 %** |
| **Geovisualisation and cartography** | labeling 2,456 · symbology 2,390 · style 1,371 · legend 989 · cartography 867 · classification 735 · color-ramp 190 | **23.3 %** |
| Analysis and spatial statistics | buffer 1,533 · raster-calculator 1,296 · interpolation 931 · spatial-statistics 673 · kriging 277 | 12.2 % |
| Geomorphology and terrain | dem 2,115 · lidar 946 · slope 404 · hydrology 372 · terrain 247 · watershed 240 | 11.2 % |
| Remote sensing / ecology | ndvi 799 (the tags "ecology", "habitat", "conservation", "species-distribution" **do not exist**) | 2.1 % |
| Visibility | viewshed 261 | 0.7 % |
| Business analysis | network-analysis 98 · business 36 · demography 32 | 0.4 % |
| Geology | geology 96 · soil 47 | 0.4 % |
| Spatial planning | land-use 133 (the tags "urban-planning", "zoning" **do not exist**) | 0.3 % |

**Two of the eight domains have no tag of their own on the largest forum of GIS practitioners**, and five of the rest sit between 0.3 % and 0.7 % of the volume. Geomorphology is the exception: no tag under its name, but strong proxies in elevation data. This does not mean nobody does these things; it means they are not where practitioners get stuck.

### 8.2 What the discipline is made of — GIS&T Body of Knowledge

The canonical taxonomy (UCGIS 2024: **10 Knowledge Areas, 96 Units, 306 Topics**) has at its top level *Analytics and Modeling*, *Cartography and Visualization*, *Data Capture*, **Data Management**, *Computing Platforms*, *Programming and Development*, *Foundational Concepts*, *Knowledge Economy*, *GIS&T and Society* and **Domain Applications**. And the decisive point:

> **Geology, ecology, planning, business and geomorphology are not separate pillars in that taxonomy — they are subcategories of a single Knowledge Area, *Domain Applications*, holding 43 of ~306–331 topics, about 14 % of the discipline.**

Both measurements say the same thing although they measure different things (tags: difficulty and frequency of questions; BoK: structure of knowledge): **subject-matter domains are a narrow slice of GIS work, not its skeleton.** Eight equal pillars is the structure of an encyclopaedia, not of an analyst's day.

The caveat has to be stated with both: tags overlap (a question often has three or four), so the shares are not a time budget; and question volume measures **difficulty and confusion**, not hours worked. BoK is an educational taxonomy, not a description of job roles. These are **proxies** — good enough to establish an order of magnitude, not to rule on percentages. But all three available proxies (tags, BoK, reports that data preparation dominates the working day) point the same way.

### 8.3 Proportional allocation destroys coverage

Allocating tasks **in proportion to the shares in §8.1** gives, at 40 tasks:

| Domain | share | tasks out of 40 | out of 80 |
|---|---:|---:|---:|
| Data management and formats | 49.3 % | **20** | 39 |
| Geovisualisation and cartography | 23.3 % | **9** | 19 |
| Analysis and spatial statistics | 12.2 % | 5 | 10 |
| Geomorphology and terrain | 11.2 % | 4 | 9 |
| Remote sensing / ecology | 2.1 % | 1 | 2 |
| Visibility | 0.7 % | **0** | 1 |
| Business analysis | 0.4 % | **0** | 0 |
| Geology | 0.4 % | **0** | 0 |
| Spatial planning | 0.3 % | **0** | 0 |

At 40 tasks four domains get nothing; at 80, still three. (Sums do not close because of rounding.) That is the answer to the intuition "I will build a corpus proportional to an analyst's work": **proportionality and coverage are opposite requirements.** Hence **balance in the design, weights in the analysis** (§8.4) — never proportionality in the selection.

### 8.4 How to "reflect an analyst's work": weights, not allocation

```
TSR_weighted = Σ_d (w_d · TSR_d)      where w_d = domain d's share of an analyst's work, Σ w_d = 1
```

Three rules without which this is decoration:

1. **The weights come from an external measurement, not from the corpus** — e.g. the frozen GIS SE tag snapshot of §8.1 (with its freeze date) or the BoK Knowledge-Area distribution. Written into the pre-registration **before** the sweep.
2. **Report two numbers: unweighted and weighted.** Unweighted answers "does the phenomenon exist", which is the confirmatory claim because it does not depend on a proxy; weighted answers "what will a typical analyst meet", and is descriptive.
3. **Never mix them.** Do not test a hypothesis on the weighted number while the weights are a judgement: the test result would then depend on the judgement, not on the data.

### 8.5 Four traps

1. **Choosing domains by how easy the oracle is.** Visibility and geovisualisation have sharp predicates; planning and "business analysis" are fuzzy and invite an oracle that judges taste. If a domain enters the corpus it needs a **written oracle with tolerances** — otherwise only the measurable part enters, and the corpus quietly tilts towards what is convenient.
2. **A domain as a label without `provenance`.** "Geology" with one invented task is a name, not geology.
3. **Changing the structure after seeing results.** Moving from three families to eight domains after the pilot is a change of design, not a cosmetic one; it must be recorded before the sweep, like N and the tolerances.
4. **Confusing coverage with representativeness.** Eight domains with five tasks each give **coverage** of eight cells. They do not license "the corpus reflects GIS analysis" — that sentence needs weights (§8.4) and a measurement (§8.1), not a task count.

## 9. Twin templates: what they buy, and what they do not

A **template** is one task described by a card. A **twin** is a second variant of the same template: the same intent and the same predicates *in substance*, with the **surface** changed — field names, CRS, file format, the phrasing of the output path. What stays common is the logic of a correct solution; what changes is the layer the agent reacts to.

**A twin does not lower the standard error, and the earlier note that said it does was wrong.** Tasks are already paired across arms, so the task-difficulty term cancels exactly in the paired difference and there is nothing to "lower". A twin adds a second observation about the *same template*, not an observation about an easier or harder task; the variance of the difference is unchanged. What sits in the denominator is the heterogeneity of the interface effect (τ) plus binomial noise — the first is beyond control, the second depends on r.

| templates (units) | instances | MDE at r = 4, τ = 10 | extra authoring days |
|---:|---:|---:|---:|
| 80 | 80 | **14.0** | 0 |
| 80 + 20 twins | 100 | **14.0** *(unchanged — 80 units)* | +5 |
| 100 different templates | 100 | 12.5 | +20 |

Twins share the template-level effect: if the agent trips over a field-naming convention, **both** variants fail. So they are not independent units, and counting them as such understates the MDE by √(instances/templates) and brings pseudo-replication back one level up. Even a nested model cannot recover them as full units.

What they *do* buy, and it is worth having:

| Purpose | Mechanism | Value |
|---|---|---|
| a **surface-sensitivity test** | the same template with a different field name, CRS, format or phrasing: does the result depend on the surface or on the content? | answers "80 anecdotes from your own corpus" |
| a **contamination and paraphrase probe** | the twin is a paraphrase of the card: does the agent recognise the intent or match a pattern? | material for the limitations chapter |
| **cheap extension** | one parameterised oracle, two sets of expected values: ~2 h instead of ~1 day per variant | 20 twins for ~5 days |

**Decision:** twins stay out of N. The unit of inference remains the **template**. Twelve to twenty twins may be built later as a **sensitivity analysis**, never as power — and if τ turns out large, the only road to a lower MDE is more *different templates*, never more repetitions or more variants of the same template.

## 10. "You picked the wrong tools, tasks and model"

The objection is not one objection but five, and four of them are answered cheaply and concretely.

| Objection | The control that answers it | Runs |
|---|---|---:|
| "you picked convenient tools" | **anonymised catalogue**: the same functions, named `tool_01…tool_09`, functional descriptions only | 72 |
| "you picked a convenient catalogue" | **random catalogues** drawn from the pool of available operations, reported as between-catalogue spread | 320 |
| "one odd task carries the result" | **leave-one-out + bootstrap over tasks** (an analysis, not runs) | **0** |
| "one model, so it is the model's idiosyncrasy" | **a second model on a subset** — a test of sign, not of size | 120 |
| "the interface will change under you" | **drift patch**: 8 tasks after a version bump | 16 |

The count comes from the retired 960-run arithmetic and has to be re-stated against the live series before G1; the *controls* are what matters here, not their price.

**One of the objections is false in its premise.** "MCP as such" is not a causal object: MCP is a message format. What decides the outcome is the **design of the surface** — bounded, named, curated operations versus synthesis of a program. Moving the claim from a brand to a **design dimension** takes half the force out of "it is only this one situation", because the dimension is manipulated, not chosen once. Hence three layers of claim:

| Claim | Question | What supports it | What it requires |
|---|---|---|---|
| **T1 — existence and direction** | does the phenomenon occur at all | one corpus suffices: a single instance is evidence that a difference exists | nothing more — but it licenses only "it occurs here" |
| **T2 — size** | how large, here and now | paired contrast + interval + MDE written before measurement | 80 tasks, r = 4, unit = task |
| **T3 — transfer** | does the result travel | a held-out prediction, a second model, the drift patch, the expressible-share gradient | the controls above |

Never claim T3 from one cell — and the thesis need not: T3 can be stated as conditional and partially checked, which is more honest than pretending one configuration says everything.

Two analyses cost nothing and change the weight of evidence:

- **held-out prediction.** Split the 80 tasks into 60 + 20. Fit `outcome ~ task features (expressible share, predicate count, tier, silent-error risk, domain) + arm + interaction` and check whether it predicts the held-out 20. The claim then stops being about *these 80 tasks* and becomes about the **relation between task features and interface** — the objection "wrong tasks" turns into "what is your feature distribution", for which there is a table.
- **oracle audit by a second coder.** 10 tasks checked by an independent implementation or person; agreement is reported. This closes the objection stronger than selection: "your oracle measures something else".

And what cannot be defended, which belongs in the limitations chapter verbatim:

1. **Probabilistic representativeness.** No register, no sampling frame, no claim of "reflecting GIS tasks".
2. **Generality of the protocol.** One server, one implementation; the claim concerns a dimension, not a brand.
3. **Generality across models.** One model plus a sign replication on a second.
4. **Cartographic quality as aesthetics.** The predicates check presence and agreement, not beauty.
5. **Differences below the MDE.** A result smaller than the MDE is reported as **undecided**, not as "no difference".

## 11. What was pruned, and why

Every cut below existed in one of the seven source notes; each is listed with its reason, and the full record goes to `backlog/docs/doc-8`.

| Cut | Where it came from | Why |
|---|---|---|
| the 40-task count as the corpus size | `tasks-40` | superseded by `d-2` (80 cards); the 40 survive as the **seed catalogue** (§4), which is why the tables are still here |
| the `min_surface` column (5 / 15 / 30 tools) | `tasks-40`, `mvp-what-…` | the tool-count ladder is retired; the nine operations are fixed and the successor variable is the **expressible share** (`TASK-4`) |
| ITT versus PP analysis, random catalogues, the whitelist ablation, packages M0–M3 | `mvp-what-…` | all of it is **tool-surface** material, and it already lives in `design/tool-surface.md`; keeping a second copy here is how a reviewer finds two different ladders |
| α = 0.0083 and the Bonferroni/6 tables | `task-count-decision` | the live design uses one confirmatory test at 0.05 with Holm for the rest; the retired tables re-derived a decision that is now three lines in §7.2 |
| the 1,218-run budget variants A/B/C and the 50-task main series | `task-count-decision` | the series is 960 runs on 80 tasks (`d-2`); the surviving argument is the **shape** of the trade-off, kept as §7.3 |
| "two arms, MCP versus code" framing | `selection-objection`, `mvp-…` | three arms (K, N1, N4); the objection answer is now written against the arms that exist |
| the twin-template power arithmetic at N = 40, r = 8 | `paired-templates` | recomputed at the live configuration (§9); the *mechanism* (twins share the template effect) is what had to survive |
| hypotheses H3/H4a/H4b and the L1–L4 mapping of the corpus | several | the hypothesis list is `design/arms-and-validation.md`; one owner per list |

What deliberately survived all seven notes: the sourcing rule and the 70/20/10 split, the benchmark table, the admission rules, the seed catalogue, the two domain measurements, the τ-floor argument, the unit-of-inference rule, the twins caveat, and the five objection–control pairs.

## 12. Open items before G1

1. **Re-run the power table** at N = 80, r = 4 and the τ estimated from the pilot, and paste the result into §7.2 and into §3 of the draft. The closed form above reproduces the numbers the retired simulation produced at N = 40, r = 8; the live cell has to be checked the same way when the instrument has its analysis stage. `TASK-1` is where that is closed.
2. **Write the 40 remaining cards**, keeping ≥13 per family and raising T4 from 2 to ≥8.
3. **Code the expressible share** for all 80 and check that family C lands where the floor effect (W6) predicts.
4. **Freeze the weights** (the GIS SE snapshot with its date) and the two-number reporting rule, before the sweep.

## 13. One sentence

**Tasks buy reach, repetitions buy precision, and representativeness is bought only by the selection procedure — so the corpus grows to 80 cards at four repetitions on three arms, is balanced by family rather than by domain, reports domains descriptively with weights beside the unweighted result, and states its claims about the class of tasks it actually describes.**
