---
id: competitions/historical-editions
title: "Historical editions — what the committees have rewarded"
type: note
status: live
language: en
question: "What have the competition committees rewarded so far?"
tasks: [TASK-14]
updated_date: '2026-11-07'
---

# Historical editions — what the committees have rewarded

> An analysis of the laureates' profiles in four competitions, based on the result lists of the editions named in §1. The aim is not to check "does the thesis meet the conditions" (that is `competitions/competition-verification.md`) but **what type of thesis wins** — and whether this type of thesis has already won anywhere.
> The most important finding: **yes, it has — but not where one expects it.** See §6.

## 1. What I reviewed and what I did not

| Competition | Editions | Source |
|---|---|---|
| PTI KPM | XXIX–XLII (2013–2025), with lists of laureates and distinctions | the archive `kpm.pti.org.pl/archive/winners`, the announcements on `pti.org.pl` |
| SGP + the Surveyor General | 2016/17, 2023/24, 2024/25 (full lists of places and distinctions) | `konkurs.sgp.geodezja.org.pl`, `gov.pl/web/gugik`, `gik.pw.edu.pl` |
| Cartography / Geomatics / Geoinformation (the Polish Geographical Society's cartographic branch + the Military University of Technology) | V, VII, XI–XVI (2013–2025) | `kartografia.org`, `geoinformatics.uw.edu.pl` |
| the Minister's Award (geoinformation) | III–VI (2020–2023) | `gov.pl/web/rozwoj-technologia`, `gisplay.pl`, faculty pages |

**What I did not verify:** the full lists of all *submitted* theses (the PTI publishes them under `kpm.pti.org.pl/archive/applications` — the only place where one can check whether a GIS/geoprocessing thesis has already competed and how it fared), and SGP editions older than 2016/17. Statements about "no precedent" are therefore phrased only as "in the editions reviewed".

---

## 2. PTI — a competition that changed its subject in three years

This is the most important finding of the whole analysis, because it **overturns the conclusion of `competitions/competition-verification.md`**.

| Edition | Year | First place | Character of the thesis |
|---|---|---|---|
| XXIX | 2013 | *Relational cache analysis…* | theory / formal |
| XXXIII | 2016 | *Routing-Layer Failure Detection…* | systems / networks |
| XXXVI | 2019 | *Incremental learning … embedding of temporal graphs* | ML |
| XXXVII | 2020 | *D'Wave 2000Q … Job Scheduling* | quantum computing |
| XXXVIII | 2021 | *Optimisation of job scheduling … burst buffers* | HPC |
| XXXIX | 2022 | *Nash equilibria … in quantum games* | algorithms |
| **XL** | **2023** | **"Fine-tuning large language models for long context utilization"** | **LLM** |
| XLI | 2024 | *Metody wykrywania fałszywych obrazów generowanych przez SI* ["Methods of detecting fake AI-generated images"] (ex aequo) | ML |
| XLII | 2025 | *Cybersecurity of decentralized applications* | security |

Until 2022 the winners are dominated by algorithms, formal methods, systems and HPC. **From 2023 the first place goes to a thesis on large language models**, and the two following editions to work on generative AI (deepfakes, diffusion, explainability). Three further observations, each of which matters here:

1. **A domain thesis wins if the method is general.** XLII, third place: *"Domain-Aware Machine Learning Architectures for Hyperspectral Remote Sensing"* (Poznań University of Technology, Artificial Intelligence programme). Hyperspectral remote sensing is a cousin of geoinformation — and it reached the podium. The conclusion: **a domain does not disqualify, provided the thesis is about a method and the domain is a case of use.**
2. **A comparative thesis is an accepted genre.** XLII, a distinction: *"AI-generated vs human-authored texts: **comparative analysis** of datasets and NLP methods"*. Earlier: *Pomiar jakości kodu w Javie…* ["Measuring code quality in Java"] (2020, second place), *Porównanie systemów analizy danych … e-nosów* ["Comparing data-analysis systems … electronic noses"] (2013, second place), *Odkrywanie charakterystyk UDF* ["Discovering UDF characteristics"] (2021, distinction). **Comparison plus measurement is a rewarded genre** — provided the object of measurement is a computational artefact and not a convenient abstraction.
3. **The scale of the competition:** 160 theses submitted and 106 accepted in XLI (2023/24); 78 accepted from 21 universities in XLII (2024/25). Prizes: 12 500 PLN (first), 10 500 (second), 7 000 (distinctions) in XLII — earlier 5 000 / 4 000 / 2 500.

**What follows:** a thesis about an LLM agent's interface to a GIS system is **closer to the centre of gravity of the PTI in 2023–2025 than ever before**. My earlier assessment ("meets conditionally") was based on the 2013–2022 profile and is too cautious. Realistically: **qualification likely, a podium unlikely** (the competition consists of work from the Warsaw, Wrocław, Kraków and Warsaw-university groups on generative AI).

---

## 3. SGP + the Surveyor General — a geodetic measurement plus a method, never "an interface"

| Edition | First place (master's theses) | Pattern |
|---|---|---|
| 2024/25 | *Predykcja i wykrywanie anomalii przemieszczeń w szeregach czasowych InSAR z zastosowaniem metod sztucznej inteligencji* ["Predicting and detecting displacement anomalies in InSAR time series using AI methods"] | a measurement problem + AI |
| 2024/25 (second, ex aequo) | *Symulacje dokładności i niezawodności pozycjonowania … na powierzchni Księżyca (ESA Moonlight)* ["Simulations of positioning accuracy and reliability … on the lunar surface"] | PNT + simulation |
| 2024/25 (second, ex aequo) | *Detekcja zwierząt na zobrazowaniach termalnych … uczenie maszynowe* ["Animal detection in thermal imagery … machine learning"] | remote sensing + ML |
| 2023/24 | InSAR, GNSS (bridge vibration), LiDAR/photogrammetry, BIM of underground infrastructure, ML for deformation from point clouds | measurement + ML + engineering |
| 2016/17 | GOCE gradiometry, a rolling-shutter image block, a 3D city model from ALS | physical geodesy / photogrammetry |

The pattern is very stable across a decade: **a measured geodetic problem + a method (increasingly ML) + a quantitative assessment of accuracy.** AI appears only as a *method of measurement*, never as the *object of study*. In the editions reviewed there is **no thesis about cartographic software, interfaces or agents**.

The closest is an engineering thesis, *"Algorytmizacja procedury kalibracji systemu pozycjonowania USBL z wykorzystaniem języka Python"* ["Algorithmising the calibration procedure of a USBL positioning system with Python"] (third place, 2024/25) — that is, **software as an instrument of measurement**, not as a subject.

**What follows:** the SGP remains the weakest fit and no amount of editing will change that. The thesis is not "a study within a geodetic specialisation". If one applies at all, only through family C and through the language of **assessing the quality of automated cartographic production** (see §6), in full awareness that this is an exception to the profile.

---

## 4. Cartography / Geomatics / Geoinformation — two genres, both close to this thesis

The competition of the Polish Geographical Society's cartographic branch (the host of the final is the university whose graduate won the previous edition). In the editions reviewed, **two** genres dominate:

**Genre A — an experiment in map perception and usability**
- *Wpływ redundancji na percepcję użytkownika mapy* ["The effect of redundancy on the map user's perception"] (XVI, second place)
- *Wpływ sposobu cieniowania na iluzję inwersji rzeźby terenu* ["The effect of the shading method on the relief-inversion illusion"] (XVI, second place)
- *Empiryczna ewaluacja sposobów kartograficznej prezentacji zmian klimatu z wykorzystaniem eye trackingu* ["An empirical evaluation of cartographic presentations of climate change using eye tracking"] (XIV, finalist)
- *Ocena empiryczna sugestywności wybranych metod manipulacji i zniekształceń informacji na mapach tematycznych* ["An empirical assessment of the suggestiveness of selected manipulation and distortion methods in thematic maps"] (XV, finalist)

**Genre B — automating cartographic generalisation with an assessment of effectiveness**
- *Wykorzystanie drzew decyzyjnych (DT) do automatyzacji selekcji rzek na mapach ogólnogeograficznych* ["Using decision trees to automate river selection on general geographic maps"] (XIII, finalist)
- *Automatyzacja procesu generalizacji wybranych warstw BDOO…* ["Automating the generalisation of selected BDOO layers"] (XIV, second place)
- *Wykorzystanie technik eksploracji danych do automatyzacji selekcji dróg na mapach ogólnogeograficznych* ["Using data-mining techniques to automate road selection on general geographic maps"] (XII, distinction)
- *Przegląd metod automatycznego pozyskiwania geometrii sieci drogowej…* ["A review of methods for automatically acquiring road-network geometry"] (XVI, finalist)

And a third place (XII, 2020): **Marcin Pałka, UMCS, the Geoinformation programme** — *Metodyczne problemy odtworzenia i zobrazowania 3D obiektu topograficznego* ["Methodological problems of reconstructing and visualising a topographic object in 3D"]. That is: **UMCS has already won here, with a thesis from the geoinformation programme.** It is also the only hard evidence in the whole set that "geoinformation" is not a handicap in this competition.

**What follows:** this is the competition whose **research culture is closest to this thesis** — both genres are controlled comparisons with a measured result and plots. Genre A is an empirical experiment; genre B is an assessment of the effectiveness of automation. This thesis combines both: it compares two ways of automating and measures effectiveness against cartographic predicates.

---

## 5. The Minister's Award — here, applications won

Master's theses, editions III–VI:

| Edition | Thesis | Character |
|---|---|---|
| III (2020) | *Wykonanie **aplikacji mobilnej** służącej do aktualizacji informacji o bazie punktów państwowej osnowy wysokościowej* ["A **mobile application** for updating information on the national height control network"] | **an artefact thesis** |
| IV (2021) | an assessment of GNSS residuals; tropospheric delay modelling; an assessment of CLC classification effectiveness; ALS quality | measurement + method assessment |
| V (2022) | **drzewa decyzyjne do automatyzacji selekcji rzek na mapach ogólnogeograficznych** ["decision trees for automating river selection on general geographic maps"]; Sentinel-1/TerraSAR-X integration; land-parcel attractiveness | automation + assessment |
| VI (2023) | — | (the edition was announced; I did not verify the laureate lists) |

Two things worth remembering:

1. **An artefact thesis won** (a mobile application, a statuette). The claim that "the harness is a contribution" has full precedent here — in this category, *building something that works and assessing it* is rewarded, not suspected.
2. **Iga Ajdacka won two competitions with the same type of thesis:** decision trees for automating river selection were a finalist in the cartographic competition (2022) and a laureate of the Minister's Award (the fifth edition). It is the only case in the whole set of **one thesis hitting twice** — and it is exactly the genre discussed in §6.

---

## 6. The main finding: the right language for this thesis has already won

The thesis compares **two ways for an agent to perform a geoprocessing task** and measures **effectiveness on artefacts, including cartographic ones**. In the language of the competitions this is not "testing AI tools". It is:

> **an assessment of the effectiveness of automating cartographic production — separating how much of that effectiveness comes from validating the result and how much from the way the task is performed.**

This genre has laureates in two competitions at once (Ajdacka: decision trees → river selection), and its methodology is identical to this thesis's: define a criterion of correctness, compare methods, compute effectiveness, show where they fail. There is one difference and it has to be named honestly: **Ajdacka assessed a classification method; this thesis assesses an interface of execution.** That is a shift one level up, not a change of genre.

**The editorial consequence (the cheapest and most effective change in the whole set):** in chapters 1 and 7 add one sentence and one table that place the thesis in this genre:

- **the sentence:** "The thesis belongs to the current of assessing the effectiveness of automated cartographic production, with the difference that the object of assessment is the way of execution (the agent's interface) rather than the classification method."
- **the table:** family C laid out as *cartographic task → predicate of correctness → result in both arms* — exactly what this competition's jury recognises as a result.

It changes not a single run and not a single conclusion. It changes only whether the jury recognises its own field.

---

## 7. The updated verdict after the history

| Competition | The laureates' profile | This thesis against the profile | Verdict (revised) |
|---|---|---|---|
| **PTI** | 2023–2025: LLM, generative AI, ML; domain and comparative theses admitted | close to the centre of gravity; the comparative genre is recognised | **qualification likely**, a podium unrealistic — **an upward revision** against `competitions/competition-verification.md` |
| **the Minister's Award** | measurement + assessment; **artefact theses** | artefact + assessment = full precedent | **meets**, a university application needed |
| **Cartography / Geomatics / Geoinformation** | empirical experiment + automation with an assessment of effectiveness; UMCS has won | the genre fits; needs the poster and the "assessment of effectiveness" language | **the best fit** |
| **SGP** | geodetic measurement + ML; no theses about software | an exception to the profile for a decade | **remains doubtful**, unchanged |

**One sentence of summary:** the history shows that this thesis is not "odd" — it is a **comparative-evaluative thesis**, and that genre has won in two of the four competitions; it loses only where the jury expects a geodetic measurement (the SGP).

---

## 8. What not to conclude from the history

1. **Do not copy the laureates' titles.** Titles of the *"Predykcja i wykrywanie anomalii… z zastosowaniem metod sztucznej inteligencji"* kind are descriptive and work at the SGP, but the PTI rewards a short English title. One title, approved by the College — the room for adjustment is in the abstract, not in the title.
2. **Do not add "using artificial intelligence"** to the title or the abstract if that is not the object of the thesis. At the PTI it does not help (AI is the default there), and at the SGP it suggests a method of measurement the thesis does not propose.
3. **Do not infer chances from a single edition.** Laureate lists are short and decided by individual votes; one edition is too little to predict anything from.
4. **Do not enter the SGP "just in case".** Submitting a thesis about interfaces to a geodetic competition costs credibility if the Commission disqualifies it (§9) — and it is the same year in which you compete elsewhere.
