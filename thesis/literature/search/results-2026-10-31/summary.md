# Automated search run — 2026-10-31

arXiv window: 20241101 → 20261031; OpenAlex: publication_year>2022/2023 per query.
Scopus: **not run here** (no keyless endpoint) — use the strings in `queries.json`.

| Q | RQ | Concept | arXiv hits | OpenAlex hits |
|---|---|---|---|---|
| Q1 | PB1,PB7 | MCP x GIS (existence / core gap query) | 4 | 37 |
| Q1b | PB1 | bare-acronym recall guard (papers that only ever write 'MCP') | 5 | 36 |
| Q2 | PB1,PB2 | MCP vs CodeGen / function calling (the head-to-head the thesis claims is missing) | 111 | 172 |
| Q3 | PB1,PB3,PB4 | MCP evaluation / benchmark landscape | 401 | 1459 |
| Q4 | PB5 | MCP security / tool poisoning | 221 | 834 |
| Q5 | PB7 | tool-set size / tool retrieval / schema overhead | 328 | 835 |
| Q6 | PB4,PB6 | determinism / reproducibility of agentic tool use | 1048 | 2213 |
| Q7 | Ch. III.4 | cross-domain MCP evaluation (medical / legal / scientific) — the 'other domains did this, GIS did not' argument | 51 | 423 |
| Q8 | all | named-artifact sweep (known-item recall + derivatives) | 43 | 70 |
| Q9 | PB1,PB2 | domain-anchored paradigm comparison, protocol-agnostic (catches precedents that never say 'MCP') | 46 | 1539 |

## Known-item recall

| Work | arXiv ID | Retrievable by the protocol |
|---|---|---|
| GeoJSON Agents | 2509.08863 | YES |
| GeoAgentBench | 2604.13888 | YES |
| Hou et al. | 2503.23278 | YES |
| LiveMCPBench | 2508.01780 | YES |
| Help or Hurdle | 2508.12566 | YES |
| MCP landscape | 2610.05319 | YES |
| GeoNatureAgent | 2610.09112 | YES |
| Farinha | 2610.10659 | YES |
