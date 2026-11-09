---
id: writing/requirements
title: "What the thesis must contain"
type: note
status: live
language: en
question: "Which faculty and competition requirements bind the text?"
tasks: [TASK-14]
sources: [thesis-requirements.md, umcs-regulations-2025-26.md, umcs-criteria-and-competitions.md]
updated_date: '2026-11-07'
---

# What the thesis must contain

> Which faculty and competition requirements bind the text?
>
> Merged 2026-11-07 from `thesis-requirements.md`, `umcs-regulations-2025-26.md`, `umcs-criteria-and-competitions.md`. Pruned, translated and turned into a checklist 2026-11-07; the cut log is §14. **This document is a transcript of rules, not an argument**: the regulations of the Faculty of Earth Sciences and Spatial Management, UMCS, 2025/2026, plus the four competitions' rules, reduced to what binds the text, with a status per requirement. The chapter plan that satisfies it is `draft/structure.md`; the title is `draft/titles.md`; the competitions' own analysis is `competitions/competition-verification.md`.

---

## 1. What the title commits the text to

The title of record contains **three commitments** and **two things it does not claim**. Two repairs were applied on 2026-11-09 (`draft/titles.md` §0 and §11): **W2** gave the verb and the control — *…w porównaniu z generowaniem kodu na identycznym środowisku QGIS* — and **T2** gave the object — *…jako sposobu udostępniania operacji geoprzetwarzania agentom LLM*. That pair is what the examiner measures the text against, so the commitments below are read in it, not in the earlier *w połączeniu z* form. **Z2 therefore reads *exposure* where it used to read *integration***, which is a writing obligation on §1.6 and not a change of scope.

| | Commitment | What must therefore exist |
|---|---|---|
| **Z1** | *evaluation* | an explicit object, a criterion, a measure, an oracle and a reference point — not "a description of behaviour" |
| **Z2** | *as a way of exposing geoprocessing operations to LLM agents* | a defined scope: what exactly counts as **exposure** (the tool surface, the call envelope, the enforcement layer), for which class of tasks, and in which geoinformatics environment. *Integracja* remains the frame and must be defined in §1.6 (`draft/titles.md` §11.2) |
| **Z3** | *compared with code generation* | **the code condition must exist** — without it the title is false, not merely imprecise |
| ¬Z1 | ~~evaluating the MCP protocol in general~~ | one server, one model, one task class: the claim is about a **design dimension**, not about a brand |
| ¬Z2 | ~~a hybrid MCP + code variant~~ | "compared with" is not "in combination with" — the defect of the previously approved wording, repaired 2026-11-09, see `draft/titles.md` §0 and §2. The T2 repair changed the object, not this disclaimer, and the two are disclaimed in the same sentence of the abstract |

**The thesis in one sentence, which chapter 1 must carry:** *the position defended* is that the way geoprocessing operations are exposed determines **where and how often an error is caught**, and therefore the correctness of the artefact — a tool interface lets the programmer write the conditions of correctness once and enforce them on every run, while code generation leaves their formulation to the model, anew each time; *the work tests that position*, estimating whether the difference translates into task correctness, **through what**, and **where it stops**.

**Two forms of the same claim, and this is the second.** The reader-facing form is the abstract's first sentence, fixed verbatim in `draft/titles.md` §4.1: it says what is compared, on which runtime, and what is measured. The sentence above says what is *defended*, and it is the one chapter 1 carries. They must never drift into two different theses — the reader-facing one is the narrower.

**Three sub-claims, each with its evidence chapter** — and the numbering here is the ledger's (`design/arms-and-validation.md` §2), not an older H1–H7: **H1** the exposure changes correctness (chapter 6.1), **H2** correctness rises with enforcement depth on one surface (6.2), **H3** the difference grows with the expressible share (6.3); D1–D4 are descriptive and D4 is a precondition of the whole series.

---

## 2. How to read the statuses

| Mark | Meaning |
|---|---|
| ✅ | satisfied by material that exists |
| 🟡 | satisfied conditionally — a specific action is needed, named in the row |
| ⛔ | not satisfied; something must change |
| ⏳ | will be satisfied by an act of writing or generation — **not** the same as satisfied |

**The methodological note, because it protects the verdicts:** the work is at the stage of draft and plan, so substantive criteria can only be checked **as design**, not as achievement. This document separates the two, and a reviewer will too.

---

## 3. Qualification criteria (§III.2–6)

| Criterion | Requirement | Status | Note |
|---|---|---|---|
| Type of thesis | master's (second cycle) | ✅ | a research thesis with an engineering artefact |
| Supervisor | at least a doctorate | ✅ | — |
| **Reviewer** | a doctorate; **for a master's thesis supervised by a doctor — a habilitated doctor or professor** | 🟡 | an organisational condition to settle **now**; this is the narrowest bottleneck in the whole list, because the reviewer must also be competent in LLM/agent work |
| Character | review / research / project — any on a general-academic programme | ✅ | **research with a project element**: the instrument is a designed artefact |
| Language | Polish on a Polish-language programme; another language on application to the Vice-Dean, with the supervisor's and reviewer's consent | ⛔ **decision pending** | see §13; this is the one requirement that needs an application rather than a document |
| Title | Polish, **with an English version on the title page** | ✅ | both exist; the PL repair is in `draft/titles.md` |

---

### 3.1 Administrative obligations that nonetheless bind the text

Not every rule is about prose, but three of these decide what the prose may say.

| Element | Rule | Consequence for this work |
|---|---|---|
| supervisor's responsibility | correctness **substantive, methodological and formal** | the instrument and the statistics are the supervisor's reading as much as the author's; the design notes must be readable by someone who will not run the code |
| topic | chosen with the supervisor, consistent with the field of study, the specialisation **and the supervisor's own research or professional experience** | the title pair must be defended once, at approval; it is not a working label |
| approval | topics are assessed by programme teams and approved by the College; **an experimental thesis additionally needs a short description of the planned experiment and its conditions** | the one-page description in §4 |
| change of topic | **substantive** — supervisor **and** College, on the student's application; **editorial** — the Vice-Dean for students | a change of the *title's wording* is editorial; a change of *what is compared* is substantive and reopens approval, which is why the retired fourth condition (a REST arm) is not "just another arm" |
| change of supervisor | possible in justified cases, approved by the College | — |

## 4. Substantive criteria (§III.8–12)

| Criterion | What it demands | Status | Evidence, or what is missing |
|---|---|---|---|
| §III.9 — **experimental work** | testing a research hypothesis, studying how a phenomenon varies **under specified factors**, establishing cause and effect | ✅ | one manipulated factor (the action channel, and inside it the depth of enforcement), the effect measured on the artefact, five equivalence assumptions with their consequences. **Must be said in one sentence** that the manipulation is in the interface and the design is not a correlation study |
| §III.12 — master's depth | advanced specialist knowledge, **specialist methods and tools** | ✅ | paired design, ICC 0.661 and DEFF 3.0 (task as the unit of inference), MDE 14.0 pp at τ = 10, McNemar with a mixed-logistic companion, GEE as the estimand-carrying model, Holm over a two-test family, S3 as the repeatability measure. These are not first-cycle methods |
| §III.9 — **status of an experimental thesis** | the supervisor submits **a short description of the planned experiment with the conditions** in which it will run; the College grants the status | ⏳ | one page: aim, factors, 960 runs (3 conditions × 80 tasks × 4 repetitions), QGIS 3.44 in a container on pinned weights, one model, oracle and tolerances. Material is ready in `design/experiment.md` and `design/harness.md`; the page itself is unwritten |
| §III.11 — **hierarchical layout** | chapter → subsection → point | ✅ | the seven-chapter plan is three levels deep at most |
| §III.11 — **chain of inference** | every part continues the previous one and underpins the next | ✅ | six connecting sentences in `draft/structure.md` §7 plus its numerical control (every number in §7 has a table in §6, every table in §6 a measure in §4.8) |

---

## 5. The structural requirement (§V), and a conflict that did not exist

The regulations fix this order: title page · table of contents · abstract · **1 Introduction · 2 Literature review · 3 Materials and methods · the main part, in two to four chapters · Summary and conclusions** · lists · appendices.

Earlier versions of this document reported a **conflict** here — seven planned chapters against "five parts" — and resolved it by merging methods, instrument and execution into a single 26–30 page chapter. **That was a misreading, and the correction matters because the merged version cost something real.**

The frame already contains a main part of **two to four chapters** between the third and the summary. So the arithmetic is:

> three introductory chapters (1–3) + **three** main-part chapters (4 instrument, 5 execution, 6 results) + one summary chapter (7) = **seven chapters, with the main part at three, inside the permitted two to four.**

| Requirement | Status | Note |
|---|---|---|
| main part in 2–4 chapters | ✅ | three: 4, 5, 6 |
| a separate Summary and conclusions | ✅ | chapter 7 |
| Materials and methods before the main part | ✅ | chapter 3 |

**Why the correction is worth more than a footnote.** The earlier resolution was not wrong because seven chapters are prettier; it was wrong because fusing the instrument into the methods chapter is exactly what makes contribution C1 disappear into procedure, and because a 26–30 page chapter has nowhere to put the deviations register on which the reliability of the whole series rests (`draft/structure.md` §1). The two documents now agree, and this one records which of them changed its mind.

---

### 5.1 The skeleton as the regulations order it

| # | Element | Status | Where it is satisfied |
|--:|---|---|---|
| 1 | title page, normalised (annex 1): university, faculty, field, specialisation, name, album number, **title in Polish and English**, supervisor, **chair** in which the work was written, place and year | ⏳ | generated at submission; the PL/EN pair from `draft/titles.md` |
| 2 | table of contents (annex 2) | ⏳ | generated from headings |
| 3 | **abstract, ≤ 4 000 characters** plus keywords | ⏳ | see §6.1 |
| 4 | **1 Introduction** | 🟡 | §6 below; the temporal and spatial scope is the gap |
| 5 | **2 Literature review** (recommended for a master's thesis by name) | 🟡 | §6; needs positions, not an inventory |
| 6 | **3 Materials and methods** | ✅ | conditions, assumptions, measures, taxonomies, corpus, oracle, procedure |
| 7 | **main part in 2–4 chapters** | ✅ | chapters 4 (instrument), 5 (execution), 6 (results) |
| 8 | **Summary and conclusions** | 🟡 | chapter 7; own judgements must be explicit |
| 9 | lists of literature, tables, figures, photographs, appendices | ⏳ | generated |
| 10 | appendices, Arabic numbering top right | ⏳ | A–G in `draft/structure.md` §3 |

## 6. What each part of §V must contain, and where it is satisfied

| Part | Must contain | Status | Where |
|---|---|---|---|
| 1 Introduction | justification of the topic; **aim** (problem and tasks); **temporal and spatial scope**; explanation of superordinate terms | 🟡 | aim ✅ (`framing/aim-and-contributions.md`), tasks ✅ (A1–A5), terms ✅ (`writing/key-concepts.md`), scope ✅ (`framing/scope-and-character.md`); **the temporal and spatial scope must be stated explicitly in prose** — one paragraph naming the state of the protocol stack as of November 2026, QGIS 3.44, Polish EPSG:2180 datasets, and the vector plus raster stratum. This is the one substantive gap in a part that is otherwise written |
| 2 Literature review | the scholarly output around the problem; **a comparison of positions**, cited | 🟡 | four streams and the gap exist (`framing/gap-and-literature.md`); they must be presented as **positions and a dispute** — "stream A holds…, stream B replies…" — not as an inventory |
| 3 Materials and methods | the character and kind of sources; **the methods used to carry out the tasks** | ✅ | conditions, assumptions, measures, taxonomies, corpus, oracle, procedure — `design/arms-and-validation.md`, `analysis/statistics.md`, `design/corpus.md` |
| main part, 4–6 | chapters as self-contained wholes; illustrations with captions and sources; separate numbering for tables, figures, photographs | ⏳ | the instrument, the execution and the results; the numbering discipline is a generation rule |
| 7 Summary and conclusions | assessment of whether the aim was met; general regularities and conclusions; **own judgements and opinions**; proposed solutions | 🟡 | claims with three-valued verdicts, contributions C1–C3, theses T1–T4 with conditions, and the three-row rule for integrators; **one sentence must state explicitly** "I consider the aim achieved because…", and the opinions must be opinions, not a summary of §6 |
| Lists | literature, tables, figures, photographs, appendices | ⏳ | generated at submission |
| Appendices | Arabic numbering, top right | ⏳ | A–G in `draft/structure.md` §3 |

---

### 6.1 The abstract, as a deliverable of its own

The 4 000-character limit is not the 250-word abstract of a blueprint; it is a hard limit checked at entry into APD, and the abstract is the only part of the thesis every competition reads twice.

| Requirement | Consequence |
|---|---|
| ≤ 4 000 characters **including spaces**, plus keywords | roughly 600 words; write it to 3 000 and leave room for a late revision |
| one sentence per element: gap, method, headline result, contribution | the four-sentence spine |
| **two framings, two vocabularies** | the same work described once in computing terms (an evaluation of an integration method) and once in geoinformation terms (an evaluation of geoprocessing correctness), because the PTI reads one and the SGP the other; both must be true |
| keywords | from the approved line: Model Context Protocol, geoprocessing, LLM agents, QGIS, spatial correctness, reproducibility |
| PL and EN | a thesis in a foreign language still needs a Polish abstract and a Polish title |

**When to write it:** last, after chapter 7, with the limit in hand and the four verdicts already phrased. An abstract written first is a promise the results may not keep.

### 6.2 Appendices: what must be numbered and what must be referenced

The regulations want appendices numbered in Arabic in the top right corner, and every appendix must be **called out in the text** — an appendix nobody cites is a document the reviewer will assume was padded. The mapping is fixed by `draft/structure.md` §3: A cards, B the nine operations with the parity table and the `checks` file, C predicates and the oracle's reference implementation, D prompt templates, E the manifest with one real run, F statistical tables, G reproduction. Two of them carry argument rather than evidence: **D is the proof that the conditions differ only in the action channel**, and **G is the answer to "could it be your harness?"**.

## 7. Formatting (§V, "Editing the thesis")

Binding, and cheapest to satisfy **once**, in a template, before writing rather than after:

| Element | Requirement |
|---|---|
| paper and printing | A4, **single-sided** |
| editor | Word, OpenOffice Writer or LibreOffice Writer |
| body text | **Times New Roman 12 pt, 1.5 line spacing** (≈30 lines × ≈70 characters) |
| margins | **all 2.5 cm** |
| chapter titles | new page, separated by two blank lines; bold TNR, e.g. **16 pt** |
| subsection titles | 1.5 lines above, one line below; e.g. **14 pt bold** |
| paragraphs | several developed sentences, **at most half a page**, first-line indent **1.25 cm** |
| page numbers | bottom, centre or right; **no number on the title page** |
| grammatical form | one throughout: **impersonal (recommended)** or third person |
| tables | title **above** (TNR 10 pt bold), source **below** (TNR 10 pt italic), content 10–11 pt, single spacing, **no empty cells** |
| figures and photographs | title **below** (TNR 10 pt bold), source beneath it (10 pt italic) |
| **maps** | must carry a **linear scale bar or a numerical scale** |
| formulae | equation editor, TNR 12 pt italic, inside an invisible table, numbered "(chapter.number)" in a 2 cm column |

**The one item with scientific consequences:** the scale rule. Every result figure showing communes or a study area needs a scale — plan it in the figure template, because a map without a scale is a formatting defect *and* a cartographic one, and the competition that reads this work as geoinformation will notice.

---

### 7.1 Where the template comes from, and when

The repository is plain Markdown; the regulations require Word, OpenOffice or LibreOffice Writer. Between them sits one decision worth making once:

| Option | Cost | Risk |
|---|---|---|
| **Markdown → DOCX through a reference template** ← recommended | half a day to build a reference document with styles named for TNR 12/1.5, the 16 pt and 14 pt headings, 10–11 pt table text, the 2.5 cm margins and the 1.25 cm indent | pandoc's table and figure handling needs checking once, then it is stable |
| write directly in the word processor | nothing now | §7 is re-checked by hand on every revision, and the last revision is always the one made at midnight before the deadline |
| LaTeX | a template that satisfies Word-formatting rules approximately | the faculty format is specified in terms of a word processor, and a LaTeX PDF that *looks* compliant still has to be submitted as a PDF whose fonts and margins match |

The template is built **before chapter 4 is written**, because the first chapter written sets the habit and the habit is what survives a deadline.

## 8. Citation and bibliography (§V, annexes 4 and 5)

| Rule | Detail |
|---|---|
| direct quotation | in quotation marks + author + year + **page number**, **maximum 50 words** |
| indirect (paraphrase) | author + year, no page |
| two authors | both names; **three or more** — first name + "et al." (all names in the bibliography) |
| edited volume | editor's name + [ed.] + year |
| several authors for one claim | all, **in chronological order** |
| same author, same year | 1999a, 1999b |
| second-hand citation | "(Hart 1995, after: Parnicki 2006)" |
| internet sources | in text, the **first five elements** of the address; in the bibliography, the full address + access date |
| bibliography | **alphabetical by surname**; online sources separate |
| entry format | `Author, year. Title. Publisher, Place.`; article: `Author, year. Title. Journal, volume, issue, pages.`; chapter: `Author, year. Chapter title. In: Ed. (ed.), Volume title. Publisher, Place: pages.` |
| **artificial intelligence** | "a student may use AI tools during the preparation of the thesis **under the rules in force at the Faculty**" — the regulation defers to separate faculty rules **that are not in this document** |

**Two consequences worth acting on.** The bibliography pipeline (`thesis/literature/literature.bib`, 67 entries) feeds the text, but the printed list must be **converted** to the annex-5 format — plain fields, no DOIs in brackets, all authors spelled out. And because the AI clause points at rules that do not exist in the material at hand, **the faculty's own AI policy must be obtained and quoted in the methods section**; describing how AI tools were used in building the instrument is both a compliance act and, in this thesis, a substantive one.

---

### 8.1 The bibliography conversion, concretely

The database has 67 entries; a draft citing nine of them is a draft that has not yet used its own library. Two rules follow, and they are different rules:

- **the printed list contains every work cited in the text and nothing else** — a bibliography padded with unread entries is visible to a reviewer in one glance at the section that cites none of them;
- **every entry is converted** from the pipeline format to `Author, year. Title. Publisher, Place.` (articles and chapters per §8), with all authors spelled out and no bracketed DOIs.

The conversion is mechanical and should be done by script from `literature.bib`, not by hand, because a hand-converted list of 67 entries will contain at least one inconsistent year and the inconsistency will be in the most-cited paper.

## 9. Submission, deadlines and the examination

| Event | Deadline |
|---|---|
| entry into APD (the thesis is entered by **30 September** for a second-cycle summer completion) | see the table in the regulations; the operative date for this work is **30 September** |
| supervisor's review | within **7 days** of approval in APD |
| reviewer's review | within **7 days** of the supervisor's review's approval |
| statement of independent authorship + **four photographs 4.5 × 6.5 cm** | at least **7 working days** before the examination |
| defence | **no later than 4 weeks** after entry into APD |

**What the student submits into APD:** the PDF (≤ **30 MB**), the **abstract (≤ 4 000 characters)**, keywords, the language of the thesis, and the appendices (compressed ≤ 10 MB; anything larger is described by its place of deposit rather than uploaded).

**The examination (§IV).** Oral, closed by default, before a committee of chair, supervisor and reviewer. Admission requires all credits, the thesis in APD with appendices, an accepted anti-plagiarism report, and a positive assessment. **For a master's degree: four questions, two of them about the thesis.** The grade for the thesis is the mean of supervisor and reviewer; the examination is passed at a mean of at least 3.0 with at most one negative mark; a failure or an unjustified absence leads to a second sitting within a month, which is final.

**Anti-plagiarism matters here in a specific way.** Long passages reused from this repository's own notes are the realistic risk: the notes are not the thesis, and quoting them without marking is exactly what the system is built to catch.

---

### 9.1 The round of documents, and who can stop it

| Actor | Act | Time |
|---|---|---|
| student | enters PDF (≤ 30 MB), abstract, keywords, language, appendices into APD | before 30 September |
| supervisor | checks completeness of the description → approves → **anti-plagiarism control** → review | review within 7 days |
| reviewer | review in APD | within 7 days of the supervisor's review being approved |
| dean's office | data into APD, completeness check, prints the reviews, prepares the examination file | within 3 working days |
| student | statement of independent authorship + four photographs | at least 7 working days before the examination |

**Two failure modes that are entirely administrative and entirely avoidable:** a PDF over 30 MB because result figures were rasterised at print resolution rather than exported as vector plots, and a missing statement or set of photographs inside the seven-working-day window. Both are discovered at the worst possible moment unless they are on a checklist, which is what §10.1 is.

## 10. Verdict on the faculty criteria

| Group | Verdict |
|---|---|
| qualification (§III.2–6) | ✅ except the **reviewer's degree** and the **language decision** (§13) |
| character (§III.8–9) | ✅ research and experimental: one manipulated factor, cause-and-effect established under five written assumptions |
| depth (§III.12) | ✅ paired design, ICC/DEFF, MDE, McNemar with a mixed model, Holm, a repeatability measure — specialist methods, not first-cycle |
| structure (§V) | ✅ **no conflict**: three introductory + three main-part + one summary chapter, main part inside the permitted two to four |
| editorial (§V, annexes 4–5) | 🟡 one gap (map scales) and one conversion (the bibliography into the annex format) |
| deadlines | ⏳ APD 30 September; a defence by mid-September keeps **all four** competitions open, a defence in October closes two |

---

### 10.1 The consolidated checklist

Every requirement in this document, in the order a reader would work through them, with who can close it. This table is the document's real product: the rest is evidence for these rows.

| # | Requirement | Status | Closed by |
|--:|---|---|---|
| 1 | reviewer with habilitation if the supervisor is a doctor | 🟡 | a conversation, now |
| 2 | decision on the language of the thesis (and the application if foreign) | ⛔ | the author and the Vice-Dean |
| 3 | one-page description of the experiment for the College | ⏳ | the author, from `design/experiment.md` |
| 4 | title pair PL/EN with the W2 repair applied | 🟡 | `draft/titles.md`, then College approval |
| 5 | temporal and spatial scope in §1 | 🟡 | one paragraph, after the language decision |
| 6 | literature review as positions and a dispute | 🟡 | rewriting §2 of the thesis text |
| 7 | seven chapters, main part of three | ✅ | `draft/structure.md` |
| 8 | own judgements and proposed solutions in chapter 7 | 🟡 | written after the results |
| 9 | scale bar or numerical scale on every map | 🟡 | the figure template |
| 10 | bibliography converted to the annex-5 format, all authors spelled out | 🟡 | a conversion pass over 67 entries |
| 11 | faculty AI rules obtained and quoted in the methods | ⏳ | the faculty office |
| 12 | abstract ≤ 4 000 characters, in two framings, PL and EN | ⏳ | after chapter 7 |
| 13 | appendices A–G, numbered, each cited in the text | ⏳ | at submission |
| 14 | PDF ≤ 30 MB, vector figures | ⏳ | the export settings |
| 15 | statement + four photographs, 7 working days before | ⏳ | calendar |
| 16 | grade settled for the SGP competition | 🟡 | the supervisor |
| 17 | defence by mid-September to keep all four competitions open | ⏳ | the calendar |

**Reading the table:** three of seventeen rows are blocked on decisions rather than work (language, reviewer, grade), and all three are decided by other people on their own timetable. That is the argument for doing them first.

## 11. Competitions, and the three dependencies that are not scientific

| Competition | Qualification | Status | What decides |
|---|---|---|---|
| **Minister's Award (geoinformation)** | a master's thesis in geoinformation, defended within two years; **the university submits the application** | ✅ substantively, 🟡 organisationally | the faculty's willingness, not the author's; confirm the current edition, since the legal acts have changed |
| **PTI — master's theses** | "the thesis **concerns computer science**"; criteria: importance for IT, problem solved, independence, **practical application**, literature, editorial level | 🟡 conditional | the abstract framed in computing terms; the bibliography audit is favourable — a majority of the 67 entries are computing by title, which satisfies the literature criterion with margin |
| **SGP + Head Office of Geodesy** | a graduate of geodesy and cartography **or a related field**; "a study within a specialisation in geodesy and cartography"; **a very good grade** | 🟡 doubtful | three conditions: the field on the diploma, the grade, and a text that says in so many words that the work concerns cartographic artefacts. The **thirteen family-C cards** are what make that argument possible rather than rhetorical |
| **XVII Competition (cartography, geomatics, geoinformation)** | a thesis in geoinformation; a **70 × 100 cm poster**; entry through the supervisor | ✅ thematically, ⏳ poster | the poster is half a day's work after the defence; the entry date (~25 September) forces an early defence |

**Three dependencies that quality cannot fix:** the **framing in the abstract** (two sentences, two vocabularies — one for computing, one for geoinformation), the **grade** (for the SGP a grade other than very good is disqualifying, without exception), and the **defence date** (by about 15 September keeps all four open).

**Why the cartographic family is a qualification condition rather than a nicety.** The SGP competition requires a study "within a specialisation in geodesy and cartography", and the honest way to satisfy that is to demonstrate cartographic work, not to relabel an evaluation study. The corpus already contains it: **thirteen family-C cards** — symbology, classification, layout, a 300 DPI export with title, legend and scale bar — which the nine-operation surface cannot express. That is the same family that supplies the `none` value of the expressible share and the counter-case in chapter 6 (where the catalogue loses by construction). One family of cards therefore carries three separate obligations: a competition's qualification, the moderator of H3, and the fairness of the results chapter. If the corpus were trimmed for tidiness, all three would go with it.

**What not to do for a competition:** do not add a REST/OpenAPI arm (+300 runs, and it would change a frozen scope); do not change the title for a competition (it is approved by the College); do not write a "competition version"; do not claim geodetic competence the work does not demonstrate.

---

## 12. What would disqualify the work

| Scenario | Consequence | Protection |
|---|---|---|
| the sweep does not happen and the thesis stays a plan | loses §III.9 and every competition except PTI | the 960-run series precedes the writing of chapters 6 and 7 |
| a grade other than very good | SGP excluded without exception | settle the grade question with the supervisor **now**, not after the review |
| a defence after 25 September | PTI (10 October) and the XVII competition (25 September) fall away | aim for mid-September |
| a title without the geoprocessing word | the SGP and the Minister's Award read the work as AI systems rather than geoinformation | the title already contains it — do not touch it |
| a run count different from the pre-registration | the accusation of fitting hypotheses after the fact | pre-registration before the series; every change dated and justified |
| a reviewer without habilitation, with a doctoral supervisor | the thesis cannot proceed | resolve in §3 |

---

### 12.1 The four sentences the defence must be able to produce

Whatever else happens, the compliance work succeeds only if four sentences can be said without notes — and they are compliance sentences as much as scientific ones:

1. **"The work is experimental: one factor was manipulated — the action channel, and within it the depth of enforcement — with the task as the unit of inference."**
2. **"The structure is the frame of §V: three introductory chapters, three in the main part, one of conclusions."**
3. **"The contribution is C1 the instrument, C2 the measured difference with its detection sites and its cost, C3 enforcement inside a single surface — stated with the condition under which each holds."**
4. **"The aim was met in the sense declared before the measurement, and the result is reported as confirmed, refuted or undecided against an MDE of 14.0 pp."**

Each is one line in a table in this document; that is the point of reducing rules to a checklist. A requirement that cannot be said in a sentence at the defence is a requirement that was satisfied on paper only.

## 13. What the regulations do not settle

| Open item | Why it matters | What to do |
|---|---|---|
| **the language of the thesis** | a Polish-language programme; a foreign language requires an application to the Vice-Dean with the supervisor's and reviewer's consent, and for a language other than English the College gives an opinion | decide **before** chapter 1 is written, because the decision changes the title pair, the abstracts and every caption. A thesis written in English must still carry a Polish title, Polish captions and a Polish abstract |
| **the faculty's AI rules** | the citation annex defers to rules that are not in the material available | obtain them and quote them in the methods section; the thesis uses AI as an object of study, which makes this more than a formality |
| the original PDF of the regulations | removed after conversion; the extracted text is the working copy | cite the regulations by their section numbers; do not cite the extraction |
| extraction artefacts | the extracted text has joined words and a duplicated point number, and one paragraph about figures says "below the table" | none affect obligations; do not quote the extraction verbatim in the thesis |

---

## 14. What was cut, and why

| Cut | Source note | Reason |
|---|---|---|
| the "delta against the existing table of contents" section, and the six-chapter renumbering that followed from it | `thesis-requirements.md` §§3–4, `umcs-criteria-and-competitions.md` §1.3 | it resolved a conflict that did not exist: §V's main part is 2–4 chapters *between* the third chapter and the summary, so seven chapters is compliant. The correction and its cost are recorded in §5 |
| the per-chapter "what each chapter must contain" map duplicating `draft/structure.md` §3 | `thesis-requirements.md` §2 | the structure document owns the chapter contents; this one owns the *requirements* and their status |
| the "H1–H5 / three conditions / scope 8 domains × 10 tasks / ladder L1–L5 / measures S1–S5" framing in the header | `thesis-requirements.md` preamble | a retired design generation; the ledger is H1 / H2 / H3 with D1–D4, 80 tasks in three families, and the depth axis N1 → N4 |
| "TOST" quoted as evidence of master's-level sophistication | `umcs-criteria-and-competitions.md` §1.2 | the equivalence test is retired; the depth argument now rests on McNemar, the mixed/GEE estimand distinction, Holm and S3 |
| the C1–C5 list in the introduction table | `thesis-requirements.md` §1 | the contributions are C1–C3 |
| the "six things to do" list with completion marks | `umcs-criteria-and-competitions.md` §2 | two of its six items were resolved by correcting the structural reading and one is superseded by the structure document; the remaining actions are now rows with statuses in §§6, 10 and 13 rather than a separate list |
| the full narrative summary of the regulations (supervisor selection, change of topic, document circulation, the fee for the diploma) | `umcs-regulations-2025-26.md` §§1, 2, 8 | obligations that are administrative rather than textual; what binds the *text* is kept, the rest is one paragraph in §9 |
| the editorial remarks about the regulations document itself | `umcs-regulations-2025-26.md` §11 | compressed to one row in §13, because the only actionable part is "do not quote the extraction" |
| the competitions' calendars by T‑0 | `umcs-criteria-and-competitions.md` §3 | the calendar is `competitions/competition-verification.md` §4's subject; the three non-scientific dependencies survive here because they are decisions, not dates |
| eleven "notes for the defence" paragraphs | all three notes | the defence script is `writing/defence.md` |

**Added while pruning**, because the cut had removed the only home of the claim: the correction of the structural conflict with its arithmetic (§5), the status vocabulary and the methodological warning that a draft can only be judged as design (§2), the reviewer's degree as the narrowest bottleneck (§3), the one-page experiment description the College needs for the experimental status (§4), the AI-tools clause and the missing faculty rules as an open item (§8, §13), the language decision as the only requirement that needs an application rather than a document (§13), and the scale rule as the one formatting requirement with scientific consequences (§7).

**Kept, because each is the only place in the repository where its claim is made:** the three title commitments and the two non-claims (§1), the qualification and substantive criteria with their statuses and evidence (§3–4), what each part of §V must contain and where it is satisfied (§6), the formatting table (§7), the citation rules including the AI clause (§8), the submission and examination rules (§9), the verdict table (§10), the four competitions with the three non-scientific dependencies (§11), and the disqualification scenarios (§12).
