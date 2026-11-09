---
id: writing/plan
title: "The half-year plan: how to raise the bar without inflating the thesis"
type: note
status: live
language: en
question: "What has to happen in the next half year?"
tasks: [TASK-1]
updated_date: '2026-11-07'
---

# The half-year plan: how to raise the bar without inflating the thesis

> The 26-week operational plan, consistent with `framing/edge-of-scope.md` (what makes the work strong), `framing/aim-and-contributions.md` (what may not be claimed), `framing/scope-and-character.md` (the frozen scope), `design/corpus.md` (power), `competitions/competition-verification.md` and `competitions/historical-editions.md` (external criteria).
> **Assumption:** defence around June–September 2027, which means writing starts in November 2026. If the defence date is different (February 2027 = the winter semester), the plan has to be *cut* by block B3, not stretched — see §7.

## 0. The governing principle

**Raising the bar is not about adding. It is about making every artefact verifiable by a third person.**

An "ambitious" thesis adds hypotheses, layers and runs; a **strong** one has five things an examiner cannot undermine: a frozen pre-registration, oracles with negative controls, frozen tolerances, a published manifest, and a limitations section that tells the truth about power. All five cost **hours, not weeks** — and all five sit in the first two weeks of this plan, because once the sweep has started they can no longer be done.

## 1. The calendar in six blocks with gates

| Block | Wk | What is produced | **Gate** (without it you do not move on) |
|---|---|---|---|
| **B0 — freeze** | 1–2 | `pre-registration.md`: task-card schema, predicate vocabulary, **tolerance table**, the three conditions K / N1 / N4 with the nine operations and the exact list of what each enforces, system prompt, turn and token limit, manifest fields, analysis plan (α = 0.05 for H1, Holm over {H2, H3}), N = 80 with r = 4, error taxonomy | **G1**: a dated, versioned document; no number may change after G1 without an explicit "changed after a look at the data" entry |
| **B1 — corpus** | 3–8 | 80 tasks in three families, each with card + oracle + negative control; the first 8 end-to-end as a pilot | **G2**: all 80 oracles **accept** the reference solution and **reject** a deliberately wrong artefact (shifted CRS, missing field, wrong geometry type) |
| **B2 — harness** | 7–10 | the loop, `run_python`, the protocol server, the gate hook, scoring, `FakeModel`, `--resume` | **G3**: a 60-run pilot with no crashes; a complete log; `FakeModel` reproduces its trajectory exactly |
| **B3 — sweep** | 11–18 | **960 runs** (3 conditions × 80 tasks × 4 repetitions), with a weekly allocation | **G4**: the coverage matrix is closed (every task × condition × repetition cell), artefacts carry SHA-256 |
| **B4 — analysis** *(in parallel from wk 13)* | 13–20 | scoring, McNemar as the primary test, a mixed / GEE companion, the MDE arithmetic, error-signature plots, the expressible-share moderator | **G5**: every number in chapter 6 comes from a script, not from a hand |
| **B5 — writing** | 17–24 | chapters 1–7; **chapter 3 is written from the frozen specification, not from memory** | **G6**: a full draft with the supervisor in wk 24, internal review in wk 25 |
| **B6 — closing** | 25–26 | faculty formatting, abstract ≤ 4,000 characters, keywords, the 70 × 100 poster, the competition documents | **G7**: the checklist in §5 fully ticked |

**Why the corpus and the harness run in parallel (B1/B2):** oracles are the bottleneck (≈ 1 day of work per task), while the harness is code that can be written in the evenings. Sequentially the two blocks take 16 weeks and do not fit in half a year.

## 2. Corpus composition — the trade that saves the schedule

Measured with the live power arithmetic (`MDE ≈ 3.42 · √(τ² + 4950/r) / √N`, α = 0.05, τ = 10 pp, hierarchical testing):

| Variant | Runs (main part) | MDE | Comment |
|---|---:|---:|---|
| 48 tasks × 4 rep. | 576 | 18.0 pp | too coarse for an effect of the size the pilot suggests |
| **80 tasks × 4 rep.** | **960** | **14.0 pp** | **the design of record (decisions d-1, d-2)** |
| 80 tasks × 8 rep. | 1,920 | 10.3 pp | twice the engine time for 3.7 pp — not affordable |
| 80 tasks × 16 rep. | 3,840 | 7.7 pp | repetitions stop paying: between-task variance (ICC 0.661) dominates |
| 64 tasks × 5 rep. | 960 | 14.1 pp | same cost and same MDE for four fewer tasks of external validity |

**Recommendation: 80 tasks × 4 repetitions.** Four is the floor, not a preference: below it the between-task variance dominates and the extra repetitions buy nothing; above it the gain in MDE costs engine hours the schedule does not have. The 960 runs are ≈ 100 hours of engine time on 8–16 Slurm tasks, which fits inside B3.

Composition: **three families, 80 tasks**, with family C (cartography) at thirteen cards, because that family carries three obligations at once — the expressible share's `none` value, the moderator of H3, and the counter-case in chapter 6 where the catalogue loses by construction.

## 3. How to raise each external requirement

| Requirement | Where it is assessed | What maximises it | Cost |
|---|---|---|---|
| **the PTI review's six criteria** (topic, solution, independence, application, literature, editorial) | PTI §4.2 | a paragraph on "significance for the development of computing" in chapters 1 and 7; literature: ≥ 15 computing/AI items; alphabetical bibliography | 2 days |
| **40 points at the SGP**, including **5 for graphic design** | SGP §11 | every map with a **scale bar and a source line**; the expressible-share figure as a drawn figure; error plots rather than tables; consistent table typography | 3 days |
| **the Minister's Award criteria** (creative value, difficulty, originality, clarity of aim, practical value) | annex 1 §4.2 | the interface-choice rule table in chapter 5 + "harness released (repository, licence)" | 1 day |
| **the cartographic competition**: a 70 × 100 poster (motivation, aim, methods, results, discussion) | the 17th edition rules | a poster built **from the finished figures** of chapter 6, not from scratch | 0.5 day |
| **faculty format**: Times New Roman 12/1.5, 2.5 cm margins, headings 16/14, tables titled above, figures captioned below, source mandatory, maps with a scale | §V + annex 1 | the template set up **in week 1**, not week 25 | 2 h |
| **abstract ≤ 4,000 characters** + keywords | faculty rules | the version from `competitions/competition-verification.md` A1 — first sentence informative, second locational | 2 h |

The rule: **external requirements do not compete with the research** — each of the above is editorial work on content that already exists. They compete only if they land in week 25.

## 4. Five dimensions of strength → five artefacts

| Dimension (`framing/edge-of-scope.md`) | The artefact that maximises it | When |
|---|---|---|
| Identification | one loop, three tool sets, the same container — **described as a design decision, not as a detail** | B2 |
| Measurement validity | **the tolerance table and the predicate vocabulary frozen before the sweep**, oracles with negative controls | B0, B1 |
| Power | the test hierarchy (α = 0.05 for H1, Holm over {H2, H3}), the MDE pasted into chapter 3, a result smaller than the MDE named as unresolved | B0, B4 |
| Resilience to alternatives | a paragraph in chapter 1: three alternative explanations and why the three conditions separate them | B5 |
| Claims matched to evidence | the prohibition list from `framing/aim-and-contributions.md` §5 stuck to the monitor | B5 |

## 5. The "done" checklist (ticked in week 25)

- [ ] **Title of record** on the cover page, in APD and in the competition entry — the **T2** wording (`draft/titles.md` §0 and §11, applied 2026-11-09), set at **14 pt** so that it holds three lines, with the English line as its translation and the comparison wording confined to abstract and talk
- [ ] Pre-registration dated; every later change marked and justified
- [ ] Tolerance table and predicates identical to the code, with no divergence
- [ ] 80/80 oracles reject their negative control
- [ ] Every run's manifest: QGIS version, `mcp` version, protocol, model, seed, artefact SHA-256
- [ ] Coverage matrix with no holes; no run left "in progress"
- [ ] Every number in chapter 6 comes from a script under `experiment/`
- [ ] All maps with scale and source; tables titled above, figures captioned below
- [ ] Abstract ≤ 4,000 characters; first sentence informative, second locating the study by what it excludes (the combined condition), then gap, result, contribution — the first two fixed in `draft/titles.md` §4.1
- [ ] The limitations section names: the MDE, no commercial models, one engine, 80 tasks, no fourth condition
- [ ] The interface-choice rule table in chapter 5

## 6. What to cut when time runs short (in this order)

1. **The 48-run descriptive product appendix** — it is an illustration, not a claim.
2. **The corpus from 80 to 64 tasks**, repetitions held at 4 — 768 runs, MDE 15.6 pp: the external validity drops, the statistics do not break.
3. **The N4 condition reduced to its cheapest enforcement subset** (terminal conditions only, no invariants) — but then H3 is weakened and must be reported as moderated rather than confirmed.
4. **The expressible-share moderation** — moved to "further work", with the coding already done published as data.
5. **The competition documents** (poster, SGP application) — they cost days, not weeks, and none of them is a requirement of the degree.

What must **never** be cut: the pre-registration, the oracles' negative control, the test hierarchy, the limitations section. Those four are what a missing piece would cost the whole credibility, and together they take three days.

## 7. Risks with decision points

| Risk | Warning signal | Decision |
|---|---|---|
| Oracles too slow | wk 6: fewer than 32 tasks with a negative control | cut to 64 tasks × 4 repetitions, do not stretch the schedule |
| The sweep does not keep up | wk 12: fewer than 60 runs a week | the design stays 80 × 4 = 960 with three conditions; there is no return to a bigger corpus with fewer repetitions, because that variant is retired (`d-2`) |
| Writing started too late | wk 17: no draft of chapter 1 | freeze the analysis at what exists; results "in progress" do not enter the thesis |
| Defence moved to February | — | halve B3 (main part plus gating only), defer the moderator and the product appendix to a paper |
| The supervisor wants different hypotheses | wk 4 | fix one confirmatory claim and leave it alone; the rest is exploratory — that is consistent with §III.9 and needs no redesign |

## 8. The rhythm of the week (this is the plan, not a wish)

- **Mon–Wed**: production (tasks, harness, sweep) — 3 days
- **Thu**: analysis and plots — 1 day
- **Fri**: **write one section** + update the run log — 1 day
- **Sat/Sun**: 4 h of reading and correction, the rest free

Friday writing from week 1 (not week 17) is the one thing that reliably separates theses submitted on time from theses submitted in a panic. Chapter 3 can be written from the frozen specification **before** the results exist — and that is how it should be, because chapter 3 says what was done, not what came out.

## 9. One sentence that summarises the whole plan

**In the first two weeks you freeze everything that cannot be changed later; in the last two you tick the checklist; between the two, every week produces one task and one section.**
