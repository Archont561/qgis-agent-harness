---
id: glossary-of-terms
title: "Glosariusz polonizacji — anglicyzmy → terminologia polska"
type: glossary
status: frozen
language: pl
updated_date: '2026-11-07'
---

# Glosariusz polonizacji — anglicyzmy → terminologia polska

> Słownik stosowany w dokumentach `thesis/`. Zasada: **zamieniamy pojęcia, zachowujemy nazwy własne i identyfikatory.**
> Zastosowanie: **ręczne**, według tabeli §1 — od tej wersji tabela jest listą kontrolną, nie słownikiem dla skryptu (polonizator usunięty 7 XI 2026).
> **Harness rozdzielony (31 X 2026):** *agent harness* → **stanowisko agenta** (obiekt badania), *evaluation harness* → **stanowisko pomiarowe** (przyrząd). Powód i konsekwencje: `design/harness.md` §0.1.
> Nie podmienia się: bloków kodu, fragmentów w `odwrotnych apostrofach`, odnośników i nazw własnych; pliki-słowniki (`concept-dictionary.md`, ten plik) mają angielski termin w kolumnie źródłowej, więc są wyłączone z każdej korekty.
> Stan: **6 dokumentów rdzenia przetworzonych i sprawdzonych ręcznie** (§4); pozostałe ~64 czekają na przegląd zdanie po zdaniu.

---

## 1. Podmiany podstawowe

| Anglicyzm | Termin polski | Uwaga |
|---|---|---|
| prompt, system prompt | **polecenie, polecenie systemowe** | rzeczownik nijaki → poprawki zgodności: *to samo polecenie*, *identyczne polecenie* |
| prompt zadaniowy | polecenie zadaniowe | |
| feedback (zewnętrzny / dziedzinowy / językowy) | **informacja zwrotna** (zewnętrzna / dziedzinowa / językowa) | rodzaj żeński → *wiarygodna*, *definiowana*, *językowa* |
| harness (agent harness) | **stanowisko agenta** | pętla, polecenie, narzędzia i piaskownica — **obiekt badania**; w tej pracy jedno i zamrożone (`d-4`) |
| evaluation harness | **stanowisko pomiarowe** | uruchamia zadania, zapisuje przebiegi i wywołania, uruchamia wyrocznię, agreguje wyniki — **przyrząd**; to samo w obu warunkach |
| harness (zbiorczo) | **stanowisko badawcze** | termin nadrzędny nad oboma; używać tylko tam, gdzie rozdział nie ma znaczenia dla zdania |
| benchmark | **test porównawczy** | |
| sweep | **seria przebiegów** | |
| coverage, guard coverage | **pokrycie, pokrycie bramkami** | |
| pipeline | **potok przetwarzania** | |
| workflow | **przepływ pracy** | |
| wrapper | **opakowanie** | |
| trade-off | **kompromis** | |
| sandbox | **piaskownica** | |
| seed | **ziarno losowania** | |
| checklist | **lista kontrolna** | |
| dataset | **zbiór danych** | |
| baseline | **poziom odniesienia** | |
| endpoint | **punkt końcowy** | |
| ground truth | **wartość odniesienia** | |
| codebook | **kodeks kodowania** | |
| insight | **wniosek** | |
| best practice | **dobra praktyka** | |
| state of the art | **stan wiedzy** | |
| edge case | **przypadek skrajny** | |
| unit test | **test jednostkowy** | |
| audit | **audyt** | |
| pre-registration | **przedrejestracja** | albo opisowo: *zapisane przed pomiarem* |
| design eksperymentu / design 2 × 2 | **plan eksperymentu / układ 2 × 2** | |
| handle (w prozie) | **uchwyt** | identyfikator `handle` w kodzie zostaje |
| [assistant → tool_call], [tool → assistant] | **[model → wywołanie narzędzia]**, **[narzędzie → model]** | dotyczy zapisów przebiegu |

---

## 2. Co zostaje po angielsku — i dlaczego

| Kategoria | Przykłady | Uzasadnienie |
|---|---|---|
| **Nazwy własne protokołów i formatów** | MCP, JSON-RPC, Streamable HTTP, stdio, OAuth, JSON Schema | nazwy specyfikacji — nie tłumaczy się ich w pracach |
| **Nazwy metod protokołu** | `tools/list`, `tools/call`, `server/discover`, `notifications/...` | identyfikatory techniczne, cytowane dosłownie |
| **Nazwy narzędzi i bibliotek** | QGIS, PyQGIS, GDAL, GRASS, PROJ, `proj.db`, `pyproj`, `shapely`, `run_python` | nazwy produktów i funkcji |
| **Skróty dziedzinowe** | CRS, EPSG, WKT, NoData, DPI, TSR, PCI, MDE, ITT, PP, SE, IoU | skróty powszechnie używane w polskiej literaturze; przy pierwszym użyciu rozwijane po polsku (np. *CRS — układ odniesienia współrzędnych*) |
| **Zapożyczenia utrwalone** | agent, serwer, klient, protokół, artefakt, skrypt, token, model, kontener, walidacja, scenariusz, klasa błędu | funkcjonują w polskim obiegu naukowym bez tłumaczenia; tłumaczenie ich byłoby sztuczne („żeton" zamiast „token") |
| **Identyfikatory w kodzie** | `detected_by`, `guard_information`, `agent_information`, `crs_oracle`, klucze JSON | cytaty kodu — nie wolno ich zmieniać |
| **Tytuły prac obcojęzycznych** | *Large Language Models Cannot Self-Correct Reasoning Yet* | bibliografia w wersji oryginalnej |

**Uwaga o „tokenie":** to jedyny częsty termin bez dobrego polskiego odpowiednika w kontekście modeli językowych („żeton" jest błędem znaczeniowym). Jeśli promotor zażąda, warianty to *jednostka tekstowa* lub *jednostka tokenizacji* — ale wtedy trzeba to zrobić konsekwentnie w całej pracy, razem z rozwinięciem skrótu przy pierwszym użyciu.

---

## 3. Jak to czytać w tekście — trzy przykłady przed i po

| Przed | Po |
|---|---|
| „bez system promptu, który każe sprawdzić wynik" | „bez polecenia systemowego, które każe sprawdzić wynik" |
| „interfejs z walidacją vs kod bez feedbacku" | „interfejs z walidacją wobec kodu bez informacji zwrotnej" |
| „po sweepie 960 runs, harness zapisuje detected_by" | „po serii przebiegów (960) stanowisko pomiarowe zapisuje `detected_by`" |

---

## 4. Stan wykonania

**Przetworzone i sprawdzone ręcznie (6):**
`draft/draft-minimal.md` · `writing/requirements.md` · `design/arms-and-validation.md` · `design/arms-and-validation.md` · `design/runs.md` · `design/correctness.md`

**Do przetworzenia (~64 pliki):** m.in. `design/correctness.md`, `design/correctness.md`, `design/arms-and-validation.md`, `framing/what-we-study.md`, `framing/aim-and-contributions.md`, `draft/titles.md`, `draft/titles.md`, `design/corpus.md`, `concept-dictionary.md` i pozostałe.

**Wyłączone z korekty (świadomie):** `concept-dictionary.md` i ten glosariusz — angielski termin jest w nich **kolumną źródłową**, więc podmiana zniszczyłaby słownik. Tak samo `literature/index.md` (tytuły prac) i `literature/search-review.md` (zapytania).

**Dlaczego nie hurtem:** automatyczna podmiana rzeczowników zmienia rodzaj gramatyczny (*prompt* → *polecenie*, *feedback* → *informacja zwrotna*), więc każdy plik wymaga przeglądu zdań ze zmianą — inaczej w pracy zostają konstrukcje typu „*informacja zwrotna był bogatszy*". Przetworzone pliki mają ten przegląd zrobiony; pozostałe wymagają tego samego, po jednym pliku.

**Kontrola po każdym pliku (dwa polecenia, bez skryptu):**

```
grep -nE "(informacj[a-ząę]* zwrotn[a-ząę]*|poleceni[a-ząę]*).{0,40}(był|jest|identyczn|zewnętrzn|definiowan)" thesis/PLIK.md
grep -niE "\b(prompt|feedback|harness|benchmark|sweep|coverage|pipeline|workflow|wrapper|sandbox|seed|checklist|dataset|baseline)\b" thesis/PLIK.md
```

Drugie polecenie ma dać **zero trafień poza blokami kodu i nazwami w odwrotnych apostrofach** — sprawdzasz to okiem, bo skryptu już nie ma.

---

## 5. Jednym zdaniem

**Słownik jest gotowy i sprawdzony na sześciu dokumentach rdzenia: polecenie zamiast promptu, informacja zwrotna zamiast feedbacku, stanowisko agenta i stanowisko pomiarowe zamiast jednego „harnessu", test porównawczy zamiast benchmarku — a nazwy własne protokołów, identyfikatory kodu i utrwalone zapożyczenia (agent, artefakt, token) zostają, bo ich tłumaczenie byłoby sztuczne, nie polskie.**
