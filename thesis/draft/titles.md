---
id: draft/titles
title: "Titles: candidates, revisions and assessment"
type: note
status: live
language: en
question: "What is the thesis called, and why that and not the alternatives?"
tasks: [TASK-14]
sources: [title.md, title-revisions.md, alternative-titles-and-scopes.md, scientific-evaluation-of-titles-and-scopes.md]
updated_date: '2026-11-09'
---

# Titles: candidates, revisions and assessment

> What is the thesis called, and why that and not the alternatives?
>
> The approved title is fixed in shape, and the question is what in it is wrong and what it costs to fix. §1 gives the five tests; §2 diagnoses the approved wording and finds one critical defect and three sharpenings; §3 gives four repair variants and the one applied first; §4 is the request to the supervisor, the procedure question, and the five mitigations if the title cannot change; §5 is what not to touch; §6 is titles for the abstract and for talks, where the rules are different; §7 is the formal classification question the department actually asks; §11 is the second decision of 2026-11-09 — the object repaired — and the candidates it beat.
>
> Pruned and translated 2026-11-07 (`TASK-21`): 7,482 → 5,975 words, four source notes → eleven sections, twelve once §11 was added. The eight alternative *scopes* (S1–S8) and the 0–10 scoring of them are gone: they proposed other theses, and the scope is decided (`d-1`–`d-5`).

---

## 0. Decided — and frozen

**Title of record, 2026-11-09, second decision (§11).** Two changes were made to the approved title the same day, and both are recorded rather than one absorbed into the other: **W2** repaired the verb (*w połączeniu z* → *w porównaniu z*, §2), and **T2** repaired the object (*jako metody integracji … z narzędziami GIS* → *jako sposobu udostępniania operacji geoprzetwarzania agentom LLM*). The title of record is:

> **Ocena protokołu MCP jako sposobu udostępniania operacji geoprzetwarzania agentom LLM w porównaniu z generowaniem kodu na identycznym środowisku QGIS**

> *Evaluation of the MCP protocol as a way of exposing geoprocessing operations to LLM agents, compared with code generation on an identical QGIS runtime*

W2 survives verbatim in §3 as the variant that would be restored if the College refuses a second wording change (§11.6).

The English line is a **translation of that title**, not a second title (§4.1 item 4), and the two are defined here together so that no other document has to invent a third. The comparison wording — *Comparing protocol-mediated tool exposure and code generation for GIS agents* — survives as a **talk and abstract title only** (§6); it may not appear on a cover page, in APD, or in a competition entry, because an English line that improves on the Polish one is the defect §4.1 exists to prevent.

Applying W2 invoked §5 rule 5, and **the rule was reopened once, deliberately, the same day** (§11). That exception is now spent: rule 5 is re-armed and there is no third decision in this document. Variants W0–W4 in §3 and T1–T4 in §11.3 stay as the record of why this wording and not the others, not as options still open. What remains open is only what a title cannot settle — the College re-approval question (§4) and the §8 items that depend on the cover page, on APD, and on the competition entry.

---

## 1. The five tests

A title for an MSc in geoinformatics has to pass five, and the last two are the ones that eliminate most candidates:

1. **Names the object** — geoprocessing, GIS operations, not "AI agents" in the abstract.
2. **Names the comparison** — a title with one thing in it is a report, not a study.
3. **States the rigour** — one word (*controlled*, *replicated*, *artefact-scored*) is what separates this from a demonstration paper.
4. **Survives a null** — if the comparison ties, the title must still be true. Any ranking title ("MCP improves X") fails here.
5. **Is falsifiable** — "Evaluation of MCP for GIS–AI integration" cannot fail, and therefore says nothing.

A title is a compression of the gap, so the four open gaps each demand something of it (`framing/gap-and-literature.md` §3):

| | Gap | Nearest prior art | What it demands of a title |
|---|---|---|---|
| **G1** | No cross-paradigm control: tool exposure and code generation have never run on the *same* engine, on the same tasks | `luo2026geojson` | name *both* sides of the comparison **and** the shared engine |
| **G2** | Enforcement depth untested in GIS; validation treated as present or absent | `strickland2026pareto`, `geocontra2026` | make the enforcement layer visible as the manipulated variable |
| **G3** | *(closed)* artefact scoring was under-operationalised before `gisagentbench2026` | `gisagentbench2026` | nothing as a gap — but the outcome should still read as *spatial correctness on executed artefacts* |
| **G4** | Reliability reported as a mean from a single attempt | `fan2026infofidelity` | one word: *replicated* — or its content in the subtitle |
| **G5** | The attack surface has not been probed in a spatial toolchain | `zhang2025msb` | **nothing** — three adversarial cards are a probe, not a claim. A title containing "security" promises a chapter that is not being written |

### 1.1 The approved title against the five tests

| Test | Verdict | Why |
|---|---|---|
| names the object | **partly** | *narzędzia GIS* is a domain word, but the object of the study is geoprocessing in **QGIS**, and the two are not the same claim. Observation 4 in §2 fixes it for free — and **T2 is that fix** (§11), which is the one verdict this table changes |
| names the comparison | **yes** | two arms are in the title; this is the title's strongest feature |
| states the rigour | **no** | nothing in it separates a controlled study from a demonstration. W2 supplies *na identycznym środowisku QGIS* — which is a condition, not an adjective, so it does the work of a rigour word without sounding like a claim |
| survives a null | **yes** | it describes a study, not a result; no outcome can embarrass it. This is why the title is repaired rather than replaced |
| falsifiable | **yes, once repaired** | as written it can be read as an announcement that a protocol was evaluated; with *w porównaniu z* it names a contrast that can fail |

Four of five, with the fifth recoverable by one word — which is an unusually good position to be in, and the reason §2 argues for repair rather than for a new title. **That repair was applied on 2026-11-09** (§0): against the W2 wording all five pass, *states the rigour* through *na identycznym środowisku QGIS* and *falsifiable* through *w porównaniu z*.

T2 changes none of the five and moves the first from *partly* to *yes* (§11.4). The verdicts above are left as W2 earned them, because that is what they were when the repair was applied.

---

## 2. The approved title, and the one critical defect

> **Ocena protokołu MCP jako metody integracji agentów LLM z narzędziami GIS w połączeniu z generowaniem kodu**

**Status 2026-11-09: repaired.** The wording below is the *approved* one, kept because the diagnosis is what justified the change; the title of record is in §0.

The *"Ocena X jako metody integracji …"* shape is a classic Polish diploma formula and a committee accepts it instantly. It must therefore be **corrected, not replaced** — the whole repair strategy rests on that, because the cost of the negotiation is then one sentence of justification rather than a new topic.

**What it gets right.** Both arms are named, so G1 is in the title. *"Jako metody integracji"* is the integration-methods frame of `framing/scope-and-character.md` §3 and the best phrase in the title. MCP is spelled out, so the thesis is findable. And it describes a study rather than a result, so no outcome embarrasses it.

**The one critical defect sits in four words: *"w połączeniu z generowaniem kodu"*.** In Polish *w połączeniu z* means *together with, in combination with* — so the natural reading is a **hybrid condition**: first discover through MCP, then let generated code do the work. The thesis compares **two separate interfaces** and deliberately excludes the hybrid (it is named as further work). The title therefore promises a condition that does not exist.

Three readings a reviewer can take, and only the first is charitable:

| Reading | What the reviewer then looks for | What they find |
|---|---|---|
| **A. "MCP compared with code"** ← intended | a comparison of two conditions | consistent |
| **B. "MCP together with code"** ← the more natural Polish | a hybrid condition | **absent → the title does not match the content** |
| **C. "an evaluation of the MCP protocol itself"** | a comparison against REST or OpenAPI | **absent → the protocol was not tested, the exposure method was** |

B and C are live readings; A requires goodwill. **A title cannot run on goodwill.**

### 2.1 The hybrid condition the title promises

It is worth knowing exactly what is being disclaimed, because the mitigation in §4.1 item 3 depends on describing it well.

A **hybrid** is: the agent discovers capability through the tool surface, then executes the awkward part by writing code — reprojection chains, loops over layers, anything the nine operation schemas do not carry. It is what production systems actually do, what several papers describe as practice, and what an honest engineer would build. It is *not* in the design for two reasons, and neither is a matter of taste:

1. **It destroys the contrast.** A condition that may use both channels has no identifiable interface: on every task it could succeed through either, and any difference from K or N4 would be unattributable. The isolation of the interface is the whole identification of the thesis (`framing/edge-of-scope.md` §3.1).
2. **It doubles the corpus before it says anything.** A fourth condition crossed with 80 tasks at r = 4 is 320 further runs, about two more weeks of machine time, at the same 14.0 pp resolution — and the interesting question about a hybrid is not whether it beats either arm but *which part of a task it hands to which channel*, which is a different study with a different unit of analysis.

So the title's promise is not a small overreach; it is a different thesis. That is what makes it the one critical defect and everything else in §2 cosmetic. **And it is why the disclaiming sentence in §4.1 item 1 is written the way it is**: it does not apologise for the absence, it states the exclusion, which is what a scope section is for.

**The other six observations, none of them fatal:**

| # | Element | Problem | Fix |
|---|---|---|---|
| 1 | *w połączeniu z* | means "together with", not "compared with" | **→ *w porównaniu z*** — a one-word change |
| 2 | no mention of **control** | the strongest methodological asset (identical engine, one loop) is invisible | add *na identycznym środowisku QGIS* |
| 3 | *Ocena protokołu MCP* | the object is the **exposure of the operations**, not the specification | **T2** (§11): *jako sposobu udostępniania operacji geoprzetwarzania agentom LLM* — with §1.6 still explaining it |
| 4 | *narzędziami GIS* | what was measured is geoprocessing in QGIS, not "GIS" as such | **T2** (§11), which drops the phrase rather than widening it to *narzędziami geoprzetwarzania QGIS* |
| 5 | *agentów LLM* | a genitive acronym: readable, imprecise (an agent is not a model) | keep in the title, unpack in the abstract's first sentence |
| 6 | no title/subtitle split | fifteen words in one run with two conjunctions | split with a colon |

And the seventh, which is the argument that wins the conversation: **the English title on the cover page already says something different and better** — *"Comparing protocol-mediated tool exposure and code generation for GIS agents: a controlled study on an identical QGIS runtime"*. Two titles on one cover is a visible defect, so the Polish fix is not modernisation; it is **restoring agreement with the English version that has to be there anyway**.

---

## 3. Four repair variants

**These labels are historical.** *W* is the outcome family elsewhere in the thesis (`docs/prose.md`: W1–W6 are interpretations of a result, and `analysis/statistics.md` uses them that way), so the repairs in §11 are labelled T and the collision is not extended. W0–W4 stay as written, because they are what §2's diagnosis was read against and because W2 is still the fallback (§11.6).

**W0 — today's title.** Reads as a hybrid (§2).

**W1 — one word changed (the cheapest negotiation).**

> **Ocena protokołu MCP jako metody integracji agentów LLM z narzędziami GIS w porównaniu z generowaniem kodu**

*Evaluation of the MCP protocol as a method of integrating LLM agents with GIS tools, compared with code generation.*

Buys: removes reading B, the dangerous one. Does not buy: still no mention of control, still "an evaluation of the protocol".

**W2 — recommended (one word changed, seven added).**

> **Ocena protokołu MCP jako metody integracji agentów LLM z narzędziami GIS w porównaniu z generowaniem kodu na identycznym środowisku QGIS**

*Evaluation of the MCP protocol as a method of integrating LLM agents with GIS tools, compared with code generation on an identical QGIS runtime.*

Buys: B is gone; the **control** is visible in the title, which is the one thing no other work on the list has (identical engine, same tasks, same data, same loop); and the title stops describing an activity and starts describing a **controlled study**. Does not buy: "an evaluation of the protocol" still invites the REST question, which §1.6 has to answer.

**W3 — restructured with a subtitle (if more is allowed).**

> **Udostępnianie narzędzi GIS agentom opartym na modelach językowych: porównanie protokołu MCP i generowania kodu na identycznym środowisku QGIS**

*Exposing GIS tools to language-model agents: a comparison of the MCP protocol and code generation on an identical QGIS runtime.*

Buys: the object becomes tool exposure rather than protocol evaluation; comparison and control are explicit; it matches the English title one-to-one. Costs: it abandons the supervisor's formula — which is why it is third and not first.

**W4 — with the mechanism in the title (deliberately risky).**

> **Ocena protokołu MCP jako metody integracji agentów LLM z narzędziami GIS w porównaniu z generowaniem kodu — rola walidacji wyników**

Buys: the main contribution (the validation boundary) is advertised, and the title survives a null. Risk: three concepts in one title, and *rola walidacji* reads as a thesis the supervisor did not approve. **Not recommended** — but worth knowing that if the result turns out null, this is the strongest variant.

| | Removes reading B | Shows the control | Agrees with the English title | Keeps the supervisor's formula | Cost of negotiation |
|---|---|---|---|---|---|
| W0 | — | — | no | yes | — |
| **W1** | yes | no | partly | yes | **one word** |
| **W2** | yes | **yes** | **yes** | yes | one sentence |
| W3 | yes | yes | yes | **no** | a new title |
| W4 | yes | no | no | yes | a new title and a new thesis |

**And the subtitle**, which is where anything the main line drops gets restored:

> *Tool-surface size, enforcement depth, spatial correctness, run-to-run reliability and cost per successful task*
>
> *Liczebność zestawu narzędzi, głębokość egzekwowania, poprawność przestrzenna, powtarzalność i koszt zadania zakończonego powodzeniem*

### 3.1 Translation notes, so the two titles say the same thing

The Polish and English titles must be semantically identical, and five decisions have to be made the same way twice:

| Polish | Use | Do not use | Why |
|---|---|---|---|
| *udostępnianie narzędzi* | yes | *ekspozycja narzędzi* | *ekspozycja* is a marketing calque and reads as advertising; *udostępnianie* is the term used in the OGC and FOSS-GIS literature for publishing a capability |
| *środowisko uruchomieniowe* | yes | *czas działania* | the second is a literal calque of *runtime* that means "running time"; it will be read as a performance metric |
| *identycznym* | yes | *podobnym*, *tym samym* | *identyczny* is the claim; *podobny* would weaken the control the thesis actually has |
| **QGIS**, **GIS**, **MCP**, **PyQGIS** | untranslated | *system informacji geograficznej* | acronyms and product names are the searchable keywords; expanding them in the title costs length and buys nothing |
| *w porównaniu z* + instrumental | yes | *w porównaniu do* | the second is tolerated in speech, marked as an error by a picky reviewer, and this is a cover page |

One more rule that has already been broken once: **do not introduce "MCP" in the Polish title if the English one does not contain it**, and vice versa. A title pair that differs in its keywords is a pair that will be cited under two different names.

### 3.2 What the chosen title trades away — and what chapter 1 must therefore carry

| | A title built from the gaps (*Same engine…*, W3-like) | The approved title (W2) | Consequence |
|---|---|---|---|
| rigour word | *replicated* | *controlled* (in the identical-runtime clause) | reliability is no longer advertised — so *powtarzalność* must be in the subtitle, or D1 loses its billing |
| manipulated variable | *enforcement depth* | *(absent)* | G2 is not visible; H2 has to be carried by chapter 1 and the abstract |
| protocol named | *MCP* | *MCP* | unchanged — the keyword survives |
| domain object | *geoprocessing on QGIS* | *narzędzia GIS* | the flavour drifts from geoinformatics towards AI systems; the subtitle restores *geoprzetwarzanie* |
| claim type | comparison **and** mechanism | plain comparison | safest to defend, sells least; the enforcement mechanism disappears from the title |
| gaps advertised | G1, G2, G4 | **G1 only** | chapter 1 must carry G2 and G4 explicitly even though the title does not |

The verdict is not "the approved title is worse". It is that **the title is now a plain comparison, so the thesis has to do in chapter 1 and the abstract the work the title no longer does**: state that enforcement depth is manipulated, that reliability is an outcome, and that the comparison is controlled. Three sentences, in the places a reader actually looks first — which is cheaper than a negotiation over a cover page.

---

## 4. How to ask for it — and what to do if the answer is no

**The recommendation is W2.** It keeps the formula, removes the critical defect, and puts in the title the one thing no other work has.

**Three sentences to the supervisor, in this order:**

> I would like to propose **one correction to the title**: *"w połączeniu z generowaniem kodu"* → *"w porównaniu z generowaniem kodu na identycznym środowisku QGIS"*.
> The reason is substantive, not aesthetic: *w połączeniu z* reads as a **hybrid condition** (MCP first, then code), and there is no such condition in the thesis — the scope covers two separate interfaces, so a reviewer would have grounds to say the title does not match the content.
> Adding *na identycznym środowisku QGIS* widens nothing — it describes a condition that is in the methodology anyway — and it shows at once that the comparison is controlled; the English version already says this, so the correction restores agreement between the two titles.

**The same three sentences in Polish**, because the conversation will not be in English:

> Chciałbym zaproponować **jedną poprawkę w tytule**: „w połączeniu z generowaniem kodu" na „w porównaniu z generowaniem kodu na identycznym środowisku QGIS".
> Powód jest merytoryczny, nie estetyczny: „w połączeniu z" czyta się jako **wariant hybrydowy** (najpierw MCP, potem kod), a takiego wariantu w pracy nie ma — zakres obejmuje dwa osobne interfejsy, więc recenzent miałby podstawy zarzucić niezgodność tytułu z treścią.
> Dodanie „na identycznym środowisku QGIS" niczego nie rozszerza — to opis warunku, który i tak jest w metodyce — a od razu pokazuje, że porównanie jest kontrolowane; wersja angielska już to mówi, więc poprawka przywraca zgodność między tytułem polskim i angielskim.

**Three situations, three answers.** If the supervisor agrees: take W2, log the decision in `writing/plan.md`, and apply the consistency checklist in §8 the same week. If the supervisor prefers W3 because it matches the English title one-to-one: take W3 and accept the loss of the formula — it is a cleaner title and the only cost is one more negotiation with the College. If the topic is frozen at the College level: do not spend the capital. Apply the five mitigations in §4.1 instead, and use the W3 wording in the abstract, the conference talk and every spin-off paper, where an abstract is legitimately not a title.

**The procedural question is not "will the supervisor agree".** The topic is approved by the College under §II.3–4 of the diploma rules, so the question is whether a change of wording **requires re-approval of the topic**. That belongs in the dean's office, and it belongs there now: changing the content of an approved topic late is usually harder than changing it early.

### 4.1 If the title is frozen — five mitigations

The title stays, and the defect is neutralised in five places instead of one:

1. **The abstract, first two sentences, fixed here** (2026-11-09, so that the abstract cannot grow a sixth statement of what the thesis is). **First:** *"The thesis compares two ways of exposing the same geoprocessing operations to an LLM agent on an identical QGIS runtime, and measures the **correctness of the produced artefact** — because the interface's value, if any, lies in where the condition about spatial meaning is enforced."* **Second:** *"A condition combining the two is not the subject of the study."* The first sentence satisfies the §8 item — comparison, identical runtime, and now also the measured object, not only the comparison; the second closes reading B before the reviewer formulates it.
2. **§1.6 (scope and boundaries):** a paragraph titled *how I read the title*, defining *w połączeniu z* as *in juxtaposition, not in combination*. It sounds formalistic, and in a thesis with an inherited title that is the standard move.
3. **§2.8 (nearest neighbours):** say in the table that the hybrid exists in the literature and in practice and is outside this scope, with a pointer to further work. That turns an omission into **a decision**.
4. **The English title as a faithful translation**, not a better description — so that the cover page carries two titles that are imperfect in the same way. Two titles that disagree is a worse defect than one weak title.
5. **The abstract and the talks** use the W3 wording, because an abstract is not a title and nobody can charge it with inconsistency.

---

## 5. What not to touch

1. **Do not swap *Ocena* for *Analiza*.** *Ocena* is in the supervisor's formula and implies valuation against criteria; *analiza* only describes.
2. **Do not put *walidacja* in the title (W4)** before the supervisor knows the result: a title may not announce a thesis that was not approved, and with a null result W4 becomes a promise unkept.
3. **Do not exceed two lines** on the cover page. Fifteen to twenty words is the limit beyond which a title stops being citable.
4. **Do not remove "MCP"** — it is the keyword by which the thesis will be found.
5. **Do not change the title a second time.** One decision, now, and then finished: every later change is another version of the cover page and another reason for someone to cite the thesis under the wrong title. **Invoked 2026-11-09** — W2 applied, title frozen. **Reopened once, the same day**, by explicit author decision, for the single repair in §11: the exception is spent, the rule stands, and a third change is a new decision with a new section rather than a continuation of this one.

---

## 6. Titles for the abstract and for talks — where the rules differ

An abstract, a conference talk and a paper are not the thesis, and the title that is *safest* for a diploma is not the title that is *strongest* for a talk. Four alternates worth keeping for that purpose:

| # | Title | Use when | Cost |
|---|---|---|---|
| **A** | *Standardised enforcement, not standardised tools: what a schema-carrying interface actually contributes to agent-performed geoprocessing* | leading with the finding that is durable whatever H1 does | a claim in the title, fine for a paper, not for the diploma |
| **B** | *A replicated, artefact-scored comparison of two ways to expose one GIS engine to an agent* | the instrument is the contribution and the comparison is the demonstration | reads as a methods paper |
| **C** | *When the map looks right but isn't: measuring spatial correctness, reliability and cost of agent-performed geoprocessing under two integration interfaces* | the GIScience framing should dominate and a metaphor is acceptable | too long for a cover page, strong for a talk |
| **D** | *Silent spatial errors in agent-performed GIS work: taxonomy and measurement* | the phenomenon, not the protocol, is the subject — the strongest article title and **never** a diploma title here, because it leaves geoinformatics for computer science (§7.1) | loses the degree fit |
| **E** | *Evaluation of the Model Context Protocol for integrating AI agents with QGIS geoprocessing* | last resort: conventional and instantly readable to a conservative committee | unfalsifiable, dates the thesis to one protocol, and hides the mechanism — the title §1 test 5 exists to reject |

**Words to keep:** *geoprocessing*, *spatial*, *QGIS* (the three terms that make this geoinformatics rather than AI-systems work); *replicated* or *controlled* (the rigour claim, impossible to fake later); *tool surface* or *tool catalogue* (the manipulated variable); *correctness*, *reliability*, *cost* (a trade-off study, not a scoreboard).

**Words to lose:** *"Evaluation of …"* as the opening (unfalsifiable, reads as a report); *revolutionise*, *next-generation*, *autonomous GIS* (marketing, and no agent is being built here); *"MCP vs code"* alone (no domain, no rigour, and it invites "you moved a Blender study"); any year or version number (guaranteed to look stale at submission).

**Two practical rules.** Do not finalise the title before the pilot: the pilot tells you whether the honest word is *replicated evaluation* or *controlled comparison*. And read the title as a claim — "Exposing geoprocessing to agents: a comparison of …" describes what was done; "MCP improves GIS agents" would be a finding, and this thesis has no finding in hand at the moment of writing the cover.

**And the keyword line, which is the title's second half in every system that indexes it.** Six terms, in this order: *Model Context Protocol*, *geoprocessing*, *LLM agents*, *QGIS*, *spatial correctness*, *reproducibility*. Six, not twelve — a keyword list that includes everything distinguishes nothing, and the first two are the ones a search will actually use. In Polish, the same six with *geoprzetwarzanie*, *poprawność przestrzenna*, *powtarzalność*, and the acronyms left untranslated.

---

## 7. The formal question: how the department classifies the work

### 7.1 Classify, do not score

**The faculty does not score "scientific quality". It classifies the thesis.** Three characters under §III.8–10 — review, research, project — plus a separate status, **experimental work** (§III.9), granted by the College on the supervisor's application, which must include a short description of the planned experiment **together with the conditions under which it will be conducted**.

The §III.9 definition is narrow and has to be quoted exactly: a thesis "aimed at testing a research hypothesis, studying the course or variability of phenomena under specified factors, and establishing cause-and-effect relationships".

**Three elements must therefore be visible:** a hypothesis, a **manipulated factor**, and an inference about causation. Anything measured on a 0–10 scale of "scientific level / difficulty / novelty" is the SGP+GGK competition's scale, not the faculty's — mixing the two orders is the commonest error in documents like this one.

**How the live design answers the question, in one table:**

| Element §III.9 requires | Where it is in this thesis |
|---|---|
| hypothesis | H1–H3 with falsifiers (`design/arms-and-validation.md` §2) |
| **a manipulated factor, ideally with a gradient** | condition with **three levels** — K, N1, N4 — i.e. exposure *and* enforcement depth. Two conditions would have been "on the borderline" here: hypothesis and factor present, gradient absent. The third level is what moves the thesis from a comparison of two tools to a study of the effect of enforcement depth |
| causal inference | identical engine, identical prompt, identical limits, paired tasks, random task effect; A1–A5 written down with their consequences (`design/experiment.md` §3.1) |
| the conditions of the experiment | the pinned-stack list in §7.3 below — this *is* the document the College asks for |

**One risk to note for the record.** A title without "GIS" (alternate D) would move the thesis from geoinformatics to computer science under §II.3–4, which ties the topic to the supervisor's field and output. That is the single formal reason the domain word must never leave the title, in Polish or English.

### 7.2 Two classification risks that the title creates, and one it cannot fix

**Risk one — "ocena protokołu" invites a protocol test.** If the title says the *protocol* is being evaluated, a reviewer is entitled to ask where the comparison against REST or OpenAPI is. The thesis does not have one and does not need one: it evaluates **a way of exposing geoprocessing**, and the protocol is the vehicle. Two places have to say so: §1.6, in a paragraph that names the object precisely, and the abstract's second sentence. This is a writing fix, not a design fix — but it is only cheap if it is done once, early.

**Risk two — "narzędzia GIS" invites a broader domain claim.** What was measured is geoprocessing in QGIS 3.44 over one stratum of tasks. A reviewer who reads *narzędzia GIS* and then finds QGIS has a legitimate objection only if the text overclaims; the title is fine, the limitations paragraph is what has to be exact (`framing/edge-of-scope.md` §3.6).

**What the title cannot fix, and no wording will.** The department's §III.9 test is about the *design*: hypothesis, manipulated factor with a gradient, causal inference. A better title can make that visible; it cannot make it true. The fourth condition that would strengthen the causal story — gated code generation — is not in the design (`framing/edge-of-scope.md` §4.2), and no phrase on a cover page substitutes for a condition that was not run. That is why the honest move is W2 plus a scope section, not W4.

### 7.3 The document the College asks for

§II.6 wants a short description of the experiment and the conditions. The conditions are already enumerated, which is rare enough to be worth saying: one model pinned by name, version and date; one harness pinned, with an identical system prompt in all three conditions; one engine (QGIS 3.44) pinned by container digest; 80 frozen task cards with predicates and tolerances hashed before the first run; 25 turns, 10 minutes and one token budget in every condition; one oracle, hidden, with a negative control per card; seeded rotation of the order; 960 runs in permuted blocks by week; and every run kept, none deleted. **That list is the application**, and it should be produced as a one-page annex rather than assembled at the last minute.

### 7.4 The competition scales, and the one condition they impose

Two external audiences score rather than classify, and their criteria are public, which is why they can be prepared for rather than hoped for:

| Audience | What it scores | What that demands of this thesis |
|---|---|---|
| **PTI** (Polish Information Processing Society) | weight for computer science, practical potential | the interface question stated as a systems question: what a schema-carrying surface provides that a text channel does not, and at what cost. The mechanism section (`design/arms-and-validation.md` §4) is what answers it |
| **SGP + GGK**, with the cartography competition | scientific level, difficulty, novelty, cartographic bearing | an oracle with negative controls, a stated MDE, and a **separate subsection on cartographic predicates** — the C family is the cartographic bearing, and it cannot be claimed without it |
| **the Minister's award** | potential and rigour, judged from the abstract alone | the abstract must state the comparison, the control and the artefact-scoring in its first three sentences, in the W3 wording (§6) |

Their scales differ and their weights differ, but they share one structural demand, and it is a *design* demand rather than a writing one:

> **The cartography family is a qualification condition, not a decoration.**

The corpus carries 13 cartographic cards in the 40-card seed. If chapter 4 contains **no separate subsection on the cartographic predicates** and no table of *task → predicate → result in each condition*, then the cartographic bearing collapses and one of the competitions becomes unreachable — regardless of how good the main result is. With that subsection, one corpus works for both audiences: the P and A families answer "does the interface change correctness", and the C family answers "can the correctness of a map be checked without a judge".

Two consequences to carry into chapter 4: the C-family predicates are **declarative property checks** (renderer type, class count, classification field, palette, label field, composition elements, DPI, non-empty raster) and never an aesthetic judgement; and the tolerance table for them has to be justified numerically like every other tolerance, because "the style was applied" is exactly the claim a reviewer will probe.

**The honest note about scores.** The spread between the candidate scopes was small — a few points out of sixty — which means no scope was ever doomed and no scope was ever safe. **What moves the assessment is rigour of execution, not the topic**: pre-registration, the MDE, the oracle with its negative controls, the register of exclusions. That is fortunate, because those are the things already built.

---

## 8. Consistency check — to be ticked once

- [ ] The Polish title on the cover page = the title in APD = the title in the competition entry — now the **T2** string (§11.6)
- [x] The English title is a **faithful translation**, not a separate description — both strings are fixed together in §0 (2026-11-09); ticked here for the wording, not for the cover page
- [x] Every document that quotes a title quotes the **T2 pair** — `requirements.md`, `plan.md`, and the draft's front matter and H1 all moved on 2026-11-09 (§11.6)
- [ ] The cover page sets the title at **14 pt**, the largest size at which the T2 line holds three lines (§11.3)
- [x] The abstract's first sentence fixes the comparison, the identical runtime **and the measured object** — written out verbatim in §4.1 item 1 (2026-11-09); ticked for the sentence, not for the abstract, which does not exist yet
- [ ] MCP is expanded at its first use in the abstract, not only in chapter 2
- [ ] §1.6 contains the paragraph "how I read the title"
- [ ] The hybrid condition is named as out of scope in §2.8, with a pointer to further work
- [ ] The subtitle carries the enforcement depth, the correctness, the reliability and the cost
- [ ] The College's one-page experiment description exists as an annex (§7.3), not as an intention

---

## 9. What was pruned, and why

| Cut | From | Reason |
|---|---|---|
| titles *T0–T4* as a numbered candidate set, and the "your original title, assessed" section | `title.md`, `alternative-titles-and-scopes` | the topic is approved, so the choice is no longer between titles but between **repairs of one title**. The original-title assessment survived as the diagnosis in §2, where its six observations are the six that still need doing |
| the recommended *"Same engine, different interface…"* title and its Polish rendering | `title.md` | it was built for two arms and a tool-surface-size ladder, neither of which exists; its content survives as variant W3 and as the abstract wording in §6 |
| **eight alternative *scopes* S1–S8** with their run counts, MDEs and week estimates | `alternative-titles-and-scopes` | they were eight *other theses*. The scope is decided (`d-1`–`d-5`) and one of them (the S1 enforcement ablation) was **absorbed into the live design** as N1 against N4 — which is the point: what was a spin-off proposal is now the third condition |
| the "spin-off in this order" recommendation and the "same 80 cards, same oracle" rule | `alternative-titles-and-scopes` | a publication plan, not a title question; the rule itself survives as `design/corpus.md` §10 |
| the 0–10 scoring table across six competition criteria for ten scopes | `scientific-evaluation` | it scored scopes that no longer exist, and three of the six columns would have to be re-scored for the live design. What survives is the structural finding — family C is a qualification condition — and the observation that the spread was small, so execution decides |
| the classification audit rows for T1–T4 and S1–S8 | `scientific-evaluation` | replaced by one table that maps the §III.9 elements onto the live design, which is the only version a reader can check |
| the five "things to change in the plan after this assessment" | `scientific-evaluation` | four of the five have since **been done** — the third condition supplies the gradient, the identical checking instruction is frozen in the prompt, S2/S3-style instrument work is a subsection rather than a title claim, and family C is treated as a condition. The fifth, the College document, survives as §7.3 |
| the duplicated "words to keep / words to lose" and "practical checks" lists | `title.md` | one copy each, in §6 |
| the Polish translation notes (*ekspozycja* vs *udostępnianie*, *środowisko uruchomieniowe* vs *czas działania*) | `title.md` | two of them survive as parenthetical warnings where the Polish title appears; the rest is a translation decision already made |

Kept, because each is the only place in the repository where its claim is made: the five tests and the gap-to-title table with G5 deliberately absent (§1), the diagnosis of the approved title and the three readings (§2), variants W0–W4 with the buys-matrix and the recommendation (§3), the three sentences to the supervisor and the re-approval question, the five mitigations for a frozen title (§4.1), the five prohibitions (§5), the alternates and word lists for abstracts and talks (§6), the classify-do-not-score distinction with the §III.9 element map and the College annex (§7.1, §7.3), and family C as a qualification condition (§7.4).

---

## 10. Five lines, and one sentence

1. **The title was fixed and one word in it was wrong.** *W połączeniu z* promises a hybrid condition the thesis explicitly excludes — that was the only *critical* defect, and it cost one word plus seven to repair. An elective repair of the object followed the same day (§11).
2. **The title of record is T2** (2026-11-09, §11): *…jako sposobu udostępniania operacji geoprzetwarzania agentom LLM w porównaniu z generowaniem kodu na identycznym środowisku QGIS*. W2 supplied the verb and the control, T2 the object: nineteen words, three lines at 14 pt, and the supervisor's *Ocena* intact.
3. **The procedural question is not the supervisor's agreement but whether the College must re-approve the topic.** Ask the dean's office now, not later; if the answer is no, five mitigations neutralise the damage in the abstract, §1.6 and §2.8.
4. **The department classifies, it does not score.** §III.9 needs a hypothesis, a manipulated factor with a gradient and a causal inference — which is why the third condition (N1 against N4) is a formal requirement and not an enrichment.
5. **The cartography family is a qualification condition.** Without a subsection on cartographic predicates, one competition is unreachable and the "correctness of a map" claim has no evidence behind it.

**And in one sentence.** The approved title needed its verb changed — *w połączeniu z* to *w porównaniu z*, plus the identical-runtime clause — because as written it promised a hybrid condition the thesis deliberately excludes, and the same day its object was narrowed from *narzędzia GIS* to *operacje geoprzetwarzania* exposed to an agent; both decisions were applied on 2026-11-09 (§0, §11), and everything else about the title, the abstract wording and the formal classification follows from them.

---

## 11. Second decision, 2026-11-09: the object repaired (T2)

**What was decided, and by whom.** The author reopened the title once, on the day W2 was applied, after reading §3's buys-matrix against §2's observations. W2 repaired the verb and put the control in the title; what it left untouched was the *object*, still phrased as *metody integracji … z narzędziami GIS*. T2 replaces that phrase and nothing else. The decision is the author's, not the supervisor's, and §11.6 states what that costs.

> **Ocena protokołu MCP jako sposobu udostępniania operacji geoprzetwarzania agentom LLM w porównaniu z generowaniem kodu na identycznym środowisku QGIS**

> *Evaluation of the MCP protocol as a way of exposing geoprocessing operations to LLM agents, compared with code generation on an identical QGIS runtime.*

Nineteen words against twenty, one phrase substituted, nothing else moved.

**The labels here are T, not W.** *W* belongs to the outcome family (`docs/prose.md`: W1–W6 are interpretations of a result, and `analysis/statistics.md` uses them that way in five places), so the repairs of a title are labelled T and the collision that §3 carries is not extended. T names nothing outside this document, on the same footing as the A–E alternates in §6.

### 11.1 The two observations one phrase fixes

| # | From §2 | In W2 | In T2 |
|---|---|---|---|
| 3 | *Ocena protokołu MCP* — the object is the **exposure of the operations**, not the specification | unchanged: a reviewer may still ask where the REST arm is (§7.2 risk one) | the thing evaluated is a *sposób udostępniania operacji*; the protocol is the vehicle. Risk one is answered by the title instead of by §1.6 alone |
| 4 | *narzędziami GIS* — what was measured is geoprocessing in QGIS, not "GIS" as such | unchanged; §7.2 risk two stays open | *operacji geoprzetwarzania* and *QGIS*: the domain claim is narrower, and the geoinformatics anchor is stronger, which is what §7.1 asks of the domain word |

Both are cosmetic by §2's own ranking: the critical defect was the verb, and W2 fixed it. T2 does not repair a second defect; it repairs the two sharpenings that a second reading showed to be cheap, because they sit in one noun phrase. **The distinction matters** — a change described as necessary when it is elective is how §5 rule 5 loses its authority, so this section says elective.

### 11.2 The word *integracja*, which T2 gives up

`framing/scope-and-character.md` §3 frames the thesis as an **integration-methods** question, and §2 called *jako metody integracji* the best phrase in the title. T2 spends it. Three consequences, all of them writing tasks and none of them design:

- **§1.6, first paragraph** uses *integracja* and defines it — the interface between a model and a geoinformatics engine — so the frame is stated in the text rather than inferred from the cover.
- **The abstract's second sentence** keeps *a method of integrating* in the position it already holds; an abstract is not a title (§4.1 item 5).
- **Chapter 2's taxonomy** carries the frame already; nothing changes there.

In exchange, the title no longer invites the question it could not answer: *ocena protokołu MCP* reads as a protocol test, and this thesis runs no comparison against REST or OpenAPI (§7.2 risk one).

### 11.3 The candidates, measured

All five are repairs of one title, not five titles: *Ocena*, *MCP* and the comparison survive in four of them. Word and character counts are exact. Line counts are measured in the widest serif available — DejaVu Serif Bold, A4, 2.5 cm margins, a 160 mm measure — which makes them a **conservative upper bound**: the faculty template's Times New Roman is narrower, so the real count is never higher.

| | Polish | Words | Chars | EN words | Three lines up to |
|---|---|---|---|---|---|
| **T0** | W2, the incumbent (§3) | 20 | 136 | 24 | 14.9 pt |
| **T1** | W2 with *narzędziami geoprzetwarzania QGIS* | 21 | 154 | 25 | 14.1 pt |
| **T2** | **the object swapped: *jako sposobu udostępniania operacji geoprzetwarzania agentom LLM*** | **19** | **148** | **24** | **14.4 pt** |
| **T3** | T2 plus the mechanism in a subtitle | 27 | 214 | 31 | 10.2 pt |
| **T4** | outcome first: *Poprawność wyników geoprzetwarzania w QGIS: protokół MCP a generowanie kodu …* | 17 | 140 | 20 | 15.1 pt |

**The two-line rule (§5 rule 3) is unattainable and always was.** T0 needs to fall to 10.8 pt to fit two lines and T2 to 9.6 pt; 10 pt is smaller than body text. The operative limit is **three lines**. At that limit T0 and T2 are 3 % apart — at the faculty's 14 pt both set to three lines, at 16 pt both to four, at 18 pt T2 goes to five where T0 stays at four. **So the cover page sets the title at 14 pt**, and that is now a checklist item (§8) rather than an assumption.

| | Buys | Costs |
|---|---|---|
| **T1** | fixes observation 4 alone | one word longer, and *QGIS* twice — *narzędziami geoprzetwarzania QGIS … środowisku QGIS* stutters |
| **T2** | fixes observations 3 and 4 in one phrase, and is a word shorter than the incumbent | loses *jako metody integracji* (§11.2) |
| **T3** | the mechanism (G2) and the outcome are both in the title | 27 words, five lines at 14 pt: past citable length and past the cover |
| **T4** | every gap in the title — outcome, mechanism, comparison, control | a new title rather than a repair: *Ocena* and the supervisor's formula go, so the College re-approves a topic instead of a wording (§4) |

T4 stays in the table because it is the variant to take **if the formula is ever reopened for other reasons**; it is not a candidate today. T5 — the mechanism as the headline, *rola warunków poprawności egzekwowanych w interfejsie* — is refused until the sweep exists, on §5 rule 2's ground: a title may not announce a result that has not been measured.

### 11.4 Against the five tests

| Test | T0 (W2) | T2 |
|---|---|---|
| names the object | partly — *narzędzia GIS* | **yes** — *operacje geoprzetwarzania*, in QGIS |
| names the comparison | yes | yes |
| states the rigour | yes — *na identycznym środowisku QGIS* | yes, unchanged |
| survives a null | yes | yes |
| falsifiable | yes | yes |

One verdict changes, and it is the test §1 lists first. G2 — enforcement depth — is still absent from the title under either variant, so §3.2 stands as written: chapter 1 and the abstract carry the mechanism, and the subtitle keeps *powtarzalność* and *koszt zadania zakończonego powodzeniem*.

### 11.5 Translation, term by term

The English line translates the Polish one; the five decisions of §3.1 are all still honoured — *udostępnianie* and not *ekspozycja*, *identyczny* and not *podobny*, the acronyms untranslated, *w porównaniu z* with the instrumental. Phrase by phrase:

| Polish | English | Why this and not the alternative |
|---|---|---|
| *Ocena* | Evaluation | unchanged; not *Analysis* (§5 rule 1) |
| *protokołu MCP* | of the MCP protocol | the keyword stays (§5 rule 4) |
| *jako sposobu* | as a way of | *sposób* is a way, not a method; *method* would restore the phrase T2 removed and split the pair |
| *udostępniania operacji geoprzetwarzania* | exposing geoprocessing operations | *exposing* is English for *udostępnianie*, and it is the verb W3 already uses, so §6 and §0 agree |
| *agentom LLM* | to LLM agents | dative in Polish, prepositional in English; the plural must stay plural wherever the abstract repeats it |
| *w porównaniu z generowaniem kodu* | compared with code generation | unchanged |
| *na identycznym środowisku QGIS* | on an identical QGIS runtime | unchanged; *runtime* is the accepted English here (§3.1) |

Both lines carry 24 words in English against 19 in Polish, and neither introduces a keyword the other lacks — the rule §3.1 records as having been broken once already.

### 11.6 What this decision changes, and what it costs

**Changed in this repository, 2026-11-09**, in every place that quotes a title:

| Place | From | To |
|---|---|---|
| §0 of this document | the W2 pair | the T2 pair, with W2 kept as the fallback |
| `writing/requirements.md` §1 | commitments read in W2 | read in T2; Z2 now defines *exposure* rather than *integration* |
| `writing/plan.md` | "the W2 wording" on the cover-page item | the T2 wording, and the 14 pt setting |
| `draft/thesis-draft-v0.md` | the English W2 line, front matter and H1 | the English T2 line, both places |
| §1.1, §2, §5, §8, §10 here | W2 verdicts | T2 verdicts, with W2 kept wherever it is the history |

**Still outside it:** APD, the cover page and the competition entry — the three that follow every wording change, now quoting the T2 line, set at 14 pt.

**What it costs, plainly.**

1. **A second negotiation.** §4's procedural question does not disappear; it is asked twice. If both changes were applied in one sitting, ask it **once, about the pair**: *W2 and T2 were applied together on 2026-11-09; does the topic need re-approval?* One answer covers both.
2. **Rule 5 spent.** The document said one change and there were two, so §5 rule 5 is re-armed rather than reinterpreted: a third change is a new decision with a new section, not a continuation of this one.
3. **A title already in the wild.** If the W2 line has left the desk — an abstract, a form, a competition entry — then two strings exist and one is wrong. Check before propagating, and propagate backwards as well as forwards.

**What would reverse it.** If the College treats a second wording change as a new topic, restore W2 and stop: it is §3 verbatim, it passes four of five tests, and §4.1's five mitigations cover the rest. The reversal costs one substitution in one file, which is exactly what T2 itself costs.
