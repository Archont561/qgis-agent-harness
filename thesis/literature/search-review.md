---
id: literature/search-review
title: "Search review — GeoAIWorkbench KB + backlog"
type: note
status: live
language: en
updated_date: '2026-11-07'
---

# Search review — GeoAIWorkbench KB + backlog

> **Where this sits (2026-11-07):** moved here from `search/SEARCH-REVIEW.md`.
> Protocol: `literature/search/queries.json` · dumps from the 2026-10-31 run:
> `literature/search/results-2026-10-31/` (23 files) · replay script:
> `literature/search/run_search.py` · backlog task: `TASK-9`.
> The document describes the state of the **previous knowledge base** (GeoAIWorkbench), not of this tree — read it as
> a diagnosis of the search protocol, not as a description of `thesis/`.

**Review date:** 2026-10-31 · **Archive:** the GeoAIWorkbench knowledge-base snapshot of 29 X 2026, since deleted along with its unpacked copy; nothing here depends on it
**Scope of this document:** survey the knowledge base and backlog, state where the literature search actually stands, diagnose the current query protocol, and propose the replacement query set. The replacement set has already been executed against keyless sources — hit counts below are real, not placeholders.

---

## 1. What is in the archive

| Part | Contents | State |
|---|---|---|
| `.knowledge/` | 172 files in 16 directories, every file with YAML frontmatter (`id`, `status`, `authoritative`, `llm_hints`) | Mature; `README.md`, `INDEX.md`, `GLOSSARY.md`, `CHANGELOG.md` coherent |
| `.knowledge/01-literature/` | 33 per-paper notes, related-work map, gaps (13), citation-placement guide, **search-log.md** | The part under review |
| `.knowledge/02-research-design/` | 3-condition factorial design, PB1–PB7, hypotheses, DSRM | Consistent with the paper notes |
| `.knowledge/03-metrics`, `05-mcp-tools`, `09-testing`, `10-security` | 7-layer metric framework, tool specs, adversarial suite, threat taxonomy | Specified, not implemented |
| `backlog/` | 17 decisions, 5 milestones, **20 tasks** (2 Done, 1 In Progress, 17 To Do), 1 research doc | Backlog is the live layer; KB is the reference layer |

Two small bookkeeping drifts: `README.md` and `INDEX.md` claim *171 files across 13 directories*; there are **172 files across 16 directories**, and `INDEX.md` contradicts itself in its own body (*192 files*). Harmless, but the "LLM can reconstruct context" premise depends on those numbers being right.

## 2. Where the search actually stands

This is the bottleneck, and `task-18` says so honestly:

- **Scopus S1–S5: never executed.** No institutional access from the sandbox; the log's columns are all `—`.
- **arXiv A1–A5: executed 2026-10-15**, but through the *web* advanced-search UI, by decomposing every concept block into single-term AND pairs (A1a–A5e, 34 separate queries, 1,054 raw hits).
- **No exports, therefore no deduplication and no screening** — so the PRISMA numbers the thesis needs do not exist yet.
- **The gap claim in `research-gaps.md` is explicitly provisional** and leans on query S1–S5, which have not run. That is the one claim a defence committee will attack first.
- A one-off OR-chain (A5-odrzucone) returned **75,099 hits** and was discarded.

## 3. Six defects in the current protocol

**D1 — the acronym `MCP` is unguarded in Scopus.** S1, S3, S4, S5 all open with `TITLE-ABS-KEY("Model Context Protocol" OR "MCP")`. In Scopus, *MCP* is also membrane cofactor protein, monocyte chemoattractant protein, metacarpophalangeal, multi-chip package. In S3 (MCP × medical/clinical) this guarantees biomedical contamination at the top of the result list. Fix: spell the protocol out, add `"MCP server*"` / `"MCP tool*"`, and search bare `MCP` only in a separate query with a domain guard and a `NOT` block.

**D2 — boolean precedence bug in the arXiv queries.** The discarded A5 chain was
`abs:"Model Context Protocol" AND abs:security OR abs:attack OR abs:"prompt injection"` — the `OR`s bind looser than the `AND`, so this is `(MCP AND security) OR attack OR prompt injection`, i.e. every paper on attacks of any kind. That is the whole explanation for 75,099 hits. Verified today: the ungrouped form returns **203** hits, the correctly parenthesised `abs:"Model Context Protocol" AND (abs:security OR abs:attack OR abs:"prompt injection")` returns **3**. The per-term rewrite (A5a, A5c, A5d, A5e run separately) was a workaround for a syntax bug, not a methodological choice.

**D3 — single-AND decomposition destroyed the block structure.** A1d (`abs:"Model Context Protocol" AND abs:QGIS`) = 0 and A4d (`abs:"tool search"`) = 0 are reported as data points. They are not: they are artefacts of splitting a query that is meant to be `term AND (a OR b OR c)`. A zero tells you the vocabulary is wrong only if the query was well-formed.

**D4 — the anchor is wrong for the novelty claim (the serious one).** Every MCP-anchored query presupposes that the closest precedent names MCP. It does not. **GeoJSON Agents (arXiv 2509.08863)** — which `research-gaps.md` itself calls "the closest precedent, but multi-agent and GeoJSON-only" — **was returned by none of the nine MCP-anchored queries** I ran. It surfaced only after adding a *domain-anchored* query (Q9: GIS × function-calling/code-generation, no protocol term). A gap claim measured only on an intervention-anchored query will overstate the gap. Recall must be measured on the domain-anchored query; the MCP block is for differentiation, not for existence.

**D5 — vocabulary is missing whole constructs, one per RQ.** PB7 is about *tool count*, but S5 only has retrieval synonyms and forces a GIS term, which suppresses the general MCP tool-count literature that H7a–H7e rest on — `"toolset size"`, `"number of tools"`, `"tool description"`, `"tool overload"` are absent. PB4's execution determinism has **no query at all**. PB5 lacks the four Hou-et-al. threat classes (`attack surface`, `capability exposure`, `least privilege`, `confused deputy`). PB6's information fidelity has no query.

**D6 — no third source, no citation chasing.** arXiv + Scopus misses IJGIS/ISPRS/AGILE/SIGSPATIAL venues where the GIS-agent work actually lands, and OGSAgent (IJGIS, online 2026-08-17) — which the log itself flags as previously invisible — is only findable by snowballing.

**D7 (data integrity, fix before the defence).** In `search-log.md` §11 the Luo et al. row carries arXiv ID **2609.08863**, which resolves to *"Solvable groups defined by redundant cyclic presentations"* — a group-theory paper. The correct ID is **2509.08863**, the one the same row links to. Related: the OGSAgent row has a placeholder ID (`2609.112?`), and the GeoNatureAgent row says `2609.09112` in the ID column but `2610.09112` in its prose (the real one is **2610.09112**). Also, MCPacific's cited title is not the arXiv title. All eight arXiv IDs otherwise resolve correctly.

## 4. The proposed query set

**Grammar change:** one `AND` per *concept block*, arbitrary `OR` *inside* a block, parentheses explicit. Blocks: **P** = LLM/agent · **I** = protocol/tool integration · **D** = GIS/geospatial · **C** = construct (effectiveness, tool count, security, determinism, fidelity). Nine queries replace S1–S5 + A1–A5; each maps to an RQ so the screening can be stratified by RQ instead of by database.

| Q | Concept | Answers | Old equivalent |
|---|---|---|---|
| Q1 | MCP × GIS (existence) | PB1, PB7 | S1 / A1 |
| Q1b | bare-`MCP` recall guard (domain-guarded, `NOT` block) | PB1 | — |
| Q2 | MCP × code-gen/function-calling (head-to-head) | PB1, PB2 | — (decisive for the gap claim) |
| Q3 | MCP evaluation/benchmark landscape | PB1, PB3, PB4 | S3 / A3 |
| Q4 | MCP security / tool poisoning | PB5 | S4 / A5 |
| Q5 | tool-set size, retrieval, schema overhead | **PB7** | S5 / A4 |
| Q6 | determinism / reproducibility of agentic tool use | **PB4, PB6** | — (new) |
| Q7 | cross-domain MCP evaluation (Ch. III.4) | Ch. III.4 | (split out of S3) |
| Q8 | named-artifact sweep (known-item recall) | all | §8 checklist |
| Q9 | **domain-anchored** GIS × paradigm, protocol-agnostic | PB1, PB2 | S2 / A2 (re-roled as the anchor) |

### The three decisive Scopus strings

```
-- Q1  MCP x GIS
TITLE-ABS-KEY ( "model context protocol" OR "mcp server*" OR "mcp tool*" OR "mcp-based" )
AND TITLE-ABS-KEY ( gis OR "geographic information system*" OR geospatial OR geoprocessing
                    OR qgis OR arcgis OR postgis OR "spatial analysis" OR "spatial reasoning" )
AND PUBYEAR > 2023 AND PUBYEAR < 2027 AND LANGUAGE ( english ) AND DOCTYPE ( ar OR cp OR re )

-- Q2  MCP vs code generation  (this result set decides the novelty claim)
TITLE-ABS-KEY ( "model context protocol" OR "mcp server*" OR "mcp tool*" OR "mcp-based" )
AND TITLE-ABS-KEY ( "code generation" OR "function calling" OR "tool calling" OR "tool use"
                    OR pyqgis OR "code interpreter" OR "python code" )
AND PUBYEAR > 2023 AND PUBYEAR < 2027 AND LANGUAGE ( english )

-- Q9  domain-anchored comparison (the anchor for recall)
TITLE-ABS-KEY ( gis OR geospatial OR qgis OR arcgis OR postgis OR "geographic information system*"
                OR "spatial analysis" )
AND TITLE-ABS-KEY ( "function calling" OR "tool calling" OR "tool use" OR "code generation"
                    OR "tool-augmented" )
AND TITLE-ABS-KEY ( "large language model*" OR LLM* OR agent* )
AND PUBYEAR > 2022 AND PUBYEAR < 2027 AND LANGUAGE ( english )
```

### The corresponding arXiv forms (correctly parenthesised, date-bounded)

```
Q1 : (abs:"Model Context Protocol" OR abs:"MCP server" OR abs:"MCP tool")
     AND (abs:GIS OR abs:geospatial OR abs:"geographic information" OR abs:QGIS
          OR abs:"spatial analysis" OR abs:PostGIS)
Q4 : (abs:"Model Context Protocol" OR abs:"MCP server")
     AND (abs:security OR abs:attack OR abs:"prompt injection" OR abs:"tool poisoning"
          OR abs:"least privilege" OR abs:"attack surface")
Q9 : (abs:GIS OR abs:geospatial OR abs:QGIS OR abs:"spatial analysis")
     AND (abs:"function calling" OR abs:"tool calling" OR abs:"tool use" OR abs:"code generation")
-- append to every query:  AND submittedDate:[202411010000 TO <today>]
```

All ten queries, in three dialects (Scopus, arXiv, OpenAlex), with per-query rationale, are in **`queries.json`**. `run_search.py` executes the machine-runnable subset and writes the log table.

## 5. Run results (executed 2026-10-31, keyless sources)

| Q | RQ | arXiv hits | OpenAlex hits |
|---|---|---:|---:|
| Q1 | PB1, PB7 | 4 | 37 |
| Q1b | PB1 | 5 | 36 |
| Q2 | PB1, PB2 | 111 | 172 |
| Q3 | PB1, PB3, PB4 | 401 | 1,459 |
| Q4 | PB5 | 221 | 834 |
| Q5 | PB7 | 328 | 835 |
| Q6 | PB4, PB6 | 1,048 | 2,213 |
| Q7 | Ch. III.4 | 51 | 423 |
| Q8 | all | 43 | 70 |
| Q9 | PB1, PB2 | 46 | 1,539 |

**Known-item recall: 8 / 8.** GeoJSON Agents, GeoAgentBench, Hou et al., LiveMCPBench, Help-or-Hurdle, MCP-landscape, GeoNatureAgent and Farinha are all retrieved by the protocol — after Q9 was added. Before Q9 it was 7 / 8, with the closest precedent missing.

Caveats to carry into the log: OpenAlex hits are title+abstract substring matches and are noisier than Scopus `TITLE-ABS-KEY`; Q6 (1,048 / 2,213) is a *scoping* query and needs title screening before it is quoted; Scopus itself is still unexecuted because it has no keyless endpoint.

## 6. What the run turned up that the KB does not yet know

Q1 alone surfaces seven MCP-×-geospatial items absent from the 33 paper notes. Three matter for the thesis:

| Candidate | Identifier | Why it matters |
|---|---|---|
| **"Less Context, Better Plans: Evaluating Tool Exposure Strategies in an MCP Server for GNSS Data Acquisition"** (2026) | `10.5281/zenodo.22833797` | **Direct threat to Gap 11 / PB7 / principle P8.** This *is* a tool-exposure-strategy study inside a geospatial MCP server — the exact construct PB7 claims is untested in GIS. Mitigating: Zenodo deposit, i.e. grey literature, not peer-reviewed. Still must be cited and differentiated. |
| **"A Task-Based Benchmark for Model Context Protocol-Driven Geospatial Dataset Discovery: LLM Agents vs Human Search"** (2026) | `10.1109/ichms69701.2026.11602360` | MCP × geospatial benchmark, peer-reviewed (IEEE ICHMS). Undercuts the phrasing "no MCP benchmark for GIS"; overlaps Gap 2 (data discovery). |
| **OGSAgent** (confirmed live) plus **MapSmith** `10.5281/zenodo.22213091`, **MapHub** `10.1117/12.3091756`, **"Towards Automated Map JSON Style … Using MCP"** `10.5194/isprs-archives-l-4-w1-2026-297-2026` | see left | Evidence the MCP server ecosystem in GIS is broader than the log's "5 nearest works" suggests; strengthens Ch. III.4 but weakens any "first MCP GIS server" framing. |

From Q9 (domain-anchored), these are also missing from the paper notes and are closer than some works currently cited: **OpenEarthAgent** (arXiv 2602.17665, "unified framework for tool-augmented geospatial agents"), **TerraBench** (2606.13148), **TerraLogic** (2607.12497), **GeoNatureAgent *Benchmark*** (2606.12821 — a separate paper from the 2610.09112 entry), **MapAgent** (2509.05933), **GeoFlow** (2508.04719), **LifePlanner** (2608.25039).

**Consequence for the gap claim.** It survives, but only in a narrower form: the missing thing is not "MCP tool exposure in GIS is unstudied" (it is now studied, if thinly) but "**no controlled, replicated, multi-agent comparison of MCP tool calling against PyQGIS code generation on a fixed GIS task set, with spatial-output correctness and security as dependent variables**". Recommend re-phrasing `research-gaps.md` Gap 11 and the PB7 hypothesis framing accordingly, and citing the GNSS paper as the closest single-construct precedent.

## 7. Ordered next actions

1. **Fix §11 of the search log** (D7): `2609.08863` → `2509.08863`; resolve the OGSAgent placeholder ID; make GeoNatureAgent consistent at `2610.09112`. Cheap, and it is the kind of error a reviewer finds.
2. **Paste §5 into `search-log.md` §9** as the arXiv/OpenAlex rows with today's date, marking Scopus as still pending. This alone satisfies AC#1 partially and AC#2 fully (recall is now a measured 8/8 rather than a checklist).
3. **Screen Q1, Q1b, Q8, Q9 first** (≈130 arXiv records) — highest information per record; they contain the novelty threats. Then Q5 for PB7, then Q4.
4. **Run the Scopus strings on the host** (`pybliometrics` + institutional IP, or web export to CSV/RIS), and do dedup by DOI then by title for preprints. Only then revise the gap claim (AC#3).
5. **Snowball from five seeds** — 2509.08863, 2604.13888, 2610.09112, OGSAgent DOI, 2610.05319 — one hop forward and backward via OpenAlex. This is the only route to the IJGIS/ISPRS layer.
6. **Add the seven new candidates to `01-literature/papers/`** in the existing frontmatter format, and update `related-work-map.md` — the benchmark lineage there currently stops before TerraBench/TerraLogic/OpenEarthAgent.
7. Only after 3–5: touch `research-gaps.md` (Phases: Gap 11 wording, then the provisional gap claim).

---

**Files produced:** `queries.json` (canonical spec, 10 queries × 3 dialects) · `run_search.py` (executor + recall test) · `results/search-log.csv` (paste-ready log rows) · `results/<Q>_arxiv.json`, `results/<Q>_openalex.json` (top-200 records per query) · `results/summary.md` (auto-generated run report).
