---
id: concept-dictionary
title: "Słownik pojęć: angielski — polski — co znaczy"
type: dictionary
status: frozen
language: pl
updated_date: '2026-11-07'
---

# Słownik pojęć: angielski — polski — co znaczy

> Dokument roboczy do pisania rozdziałów: definicje z §2.1 (definicje) i 4.2 (słownik predykatów) biorą się z tej tabeli, a nie odwrotnie. **Nie jest załącznikiem pracy** — załączniki A–G są ustalone w `draft/structure.md` §3 i żaden z nich nie jest słownikiem; jeśli praca powstanie po polsku, słownik może dojść jako dodatkowy załącznik, ale to zależy od decyzji o języku, która nie jest podjęta (`writing/requirements.md` §13).
> Kryterium doboru: pojęcie występuje w pracy **i** ma albo angielski źródłowy termin, albo polski odpowiednik, który bywa mylony. Kolumna „gdzie" wskazuje pierwsze miejsce użycia — tam definicja musi się pojawić, nie w słowniku.
>
> **Uwaga o numeracji (7 XI 2026, uzgodnione):** kolumna „gdzie" była rozjechana z jednym spisem treści. Rozdzielono to, co pewne, od tego, co tymczasowe: **numer rozdziału jest pewny** (1 wstęp, 2 przegląd literatury, 3 materiały i metody, 4 instrument, 5 wykonanie, 6 wyniki, 7 wnioski — zgodne i z `draft/thesis-draft-v0.md`, i z `draft/structure.md` §3) i to on jest teraz kotwicą hasła; **numer podrozdziału w nawiasie jest tymczasowy** — pochodzi z planu v0 i zostanie ustawiony przy pisaniu rozdziału, więc nie wolno się na nim opierać przy odwołaniach. Hasła dotyczące wycofanych pojęć (ED, RRR, T2V, REF, TOST) są oznaczone i wskazują następcę, a nie usunięte — słownik ma pokazywać, co wypadło, a nie udawać, że tego nigdy nie było.

---

## 0. Trzy zasady stosowania

1. **Pierwsze użycie w tekście:** *termin angielski* (polski odpowiednik) — jednorazowo, dalej tylko jeden z nich, konsekwentnie w całej pracy.
2. **Skróty zostają angielskie i nie są tłumaczone:** MCP, TSR, PCS, CVS, S3, S4, S4b, S5, MDE, ICC, DEFF, CRS, EPSG, GIS, QGIS, PyQGIS, OGC, WPS, IoU, JSON-RPC, API, κ. Rozwinięcie raz, w nawiasie, przy pierwszym użyciu.
3. **Nie tłumaczy się:** *token*, *manifest*, *artefakt*, *predykat*, *wyrocznia*, *ramię*, *przebieg*, *bootstrap*, *Holm*. Tłumaczenie ich na polski „na siłę" (np. „żeton", „parsowanie") pogarsza tekst.

---

## 1. Protokół i warstwa agentowa

| English | Polski | Co znaczy | Gdzie |
|---|---|---|---|
| Model Context Protocol (MCP) | Protokół kontekstu modelu | Otwarty protokół, w którym serwer publikuje modelowi językowemu katalog narzędzi wraz ze schematami parametrów, a model wywołuje je przez klienta | rozdz. 2 (1) |
| tool surface | powierzchnia narzędzi | Zbiór operacji udostępnionych agentowi wraz z opisami i schematami — to, co agent może zrobić *w ogóle* | rozdz. 3 (2) |
| tool catalog | katalog narzędzi | Konkretna, policzalna postać powierzchni: lista narzędzi opublikowana przez serwer (`tools/list`) | rozdz. 3 (2) |
| tool schema | schemat narzędzia | Maszynowy opis parametrów narzędzia (JSON Schema): nazwy, typy, zakresy, wymagalność | rozdz. 4 (3) |
| envelope | koperta | Format komunikatu: nazwy metod, kodowanie argumentów, kształt wyniku, kanał błędu — warstwa standaryzowana przez protokół, semantycznie pusta | rozdz. 3 (1) |
| enforcement layer | warstwa egzekwowania | Ogół miejsc, w których sprawdzane są warunki: parametry, warunek wstępny, warunek końcowy, artefakt | rozdz. 3 (1) |
| task contract | kontrakt zadania | Jawny, maszynowy zapis wymagań zadania (układ, jednostka, maska, ścieżka wyjścia, pola wyniku) | rozdz. 3 (1) |
| handle | uchwyt | Odniesienie do wyniku pośredniego wraz z metadanymi (układ, transformacja, braki danych, typ); przeciwieństwo „gołej" tablicy | rozdz. 3 (1) |
| tool call | wywołanie narzędzia | Jedno żądanie agenta wykonania jednej operacji z katalogu, z argumentami | rozdz. 4 (6) |
| tool discovery | odkrywanie narzędzi | Odczytanie katalogu przez agenta w czasie działania, bez zakodowania go w promptcie | rozdz. 2 (3) |
| capability negotiation | negocjacja zdolności | Ustalenie przy połączeniu, jakie funkcje protokołu obsługują obie strony | rozdz. 2 (3) |
| transport | warstwa transportowa | Sposób przesyłania komunikatów (stdio, Streamable HTTP) — **niewidoczny dla modelu**, gdy oba ramiona podają te same schematy | rozdz. 2 (4) |
| JSON-RPC | JSON-RPC | Format komunikatów żądanie/odpowiedź używany przez MCP | rozdz. 2 (3) |
| code generation | generowanie kodu | Ramię kontrolne: agent pisze i uruchamia kod w środowisku Python/PyQGIS zamiast wywoływać narzędzia | rozdz. 3 (2) |
| agent loop | pętla agenta | Oprogramowanie wykonujące cykl: model → akcja → obserwacja → decyzja o zakończeniu | rozdz. 4 (1) |
| agent harness | stanowisko agenta | Pętla, polecenie, narzędzia i piaskownica — system poddany badaniu; w tej pracy jeden, zamrożony, identyczny w obu warunkach poza czynnikiem, który je definiuje | rozdz. 4 (1) |
| evaluation harness | stanowisko pomiarowe | Przyrząd: uruchamia zadania, resetuje środowisko, zapisuje przebiegi i wywołania, uruchamia wyrocznię i agreguje wyniki | rozdz. 4 (1) |
| harness (zbiorczo) | stanowisko badawcze (harness) | Termin nadrzędny nad oboma powyżej; używać tylko tam, gdzie rozdział nie zmienia sensu zdania | rozdz. 3 (1) |
| front-end | aplikacja agentowa (front-end) | Warstwa interfejsu użytkownika i orkiestracji nad pętlą; w tej pracy **wycinek kontrolny**, nie czynnik | rozdz. 6 (9) |
| context window | okno kontekstu | Maksymalna objętość tekstu, jaką model przyjmuje w jednym żądaniu | rozdz. 4 (7) |
| truncation | przycinanie kontekstu | Ucinanie historii rozmowy przez wykonawcę po przekroczeniu okna — mierzone jako `stop_reason = length` | rozdz. 6 (11) |
| token | token | Jednostka tekstu rozliczana przez model; podstawa metryki kosztu | rozdz. 6 (8) |
| structured output | wynik strukturalny | Odpowiedź w formacie maszynowym (JSON, schemat), a nie w swobodnym tekście | rozdz. 2 (3) |
| OGC API – Processes | OGC API – Processes | Standard wystawiania procesów geoprzetwarzania przez HTTP, z opisem procesu i cyklem zadań asynchronicznych | rozdz. 2 (4) |
| Web Processing Service (WPS) | WPS | Poprzednik OGC API – Processes; kontekst historyczny | rozdz. 2 (4) |

---

## 2. GIS, dane i artefakty

| English | Polski | Co znaczy | Gdzie |
|---|---|---|---|
| geoprocessing | przetwarzanie geoprzestrzenne (geoprzetwarzanie) | Operacje na danych przestrzennych: reprojekcja, przycięcie, nakładka, bufor, agregacja | rozdz. 3 (1) |
| spatial predicate | predykat przestrzenny | Sprawdzenie warunku na danych przestrzennych (CRS, poprawność geometrii, zasięg, liczba klas) | rozdz. 4 (2) |
| coordinate reference system (CRS) | układ współrzędnych odniesienia (CRS) | Definicja odwzorowania i jednostek; najczęstsze źródło **cichych** błędów w ramieniu kodu | rozdz. 4 (2) |
| extent | zasięg | Prostokąt obejmujący dane; porównywany przez IoU | rozdz. 4 (2) |
| intersection over union (IoU) | IoU | Miara pokrycia dwóch zasięgów: część wspólna ÷ suma; próg tolerancji, np. ≥ 0,95 | rozdz. 4 (2) |
| geometry validity | poprawność geometrii | Czy geometria spełnia reguły topologiczne (brak samoprzecięć, zamknięte pierścienie) | rozdz. 4 (2) |
| tolerance table | tabela tolerancji | Zamrożone progi liczbowe predykatów; zmieniana **wyłącznie** w analizie wrażliwości | rozdz. 4 (2) |
| vector / raster | dane wektorowe / rastrowe | Dwa podstawowe modele danych przestrzennych | rozdz. 3 (1) |
| symbology | symbologia | Sposób przedstawienia danych na mapie: kolory, rozmiary, przezroczystość | rozdz. 3 (1) |
| classification | klasyfikacja kartograficzna | Podział wartości na klasy (np. quantile, equal interval) wraz z liczbą klas | rozdz. 3 (1) |
| map composition / layout | kompozycja mapy | Ramka, legenda, skala, podziałka, tytuł — elementy arkusza mapy | rozdz. 3 (1) |
| null value (GIS) | wartość pusta (null) | Brak danych w atrybucie lub rastrze. **Nie mylić z hipotezą zerową (null hypothesis)** | rozdz. 4 (2) |
| PyQGIS | PyQGIS | Pythonowe API QGIS: `qgis.core`, `processing.run` | rozdz. 4 (1) |
| `qgis_process` | `qgis_process` | Wiersz poleceń QGIS wywołujący te same algorytmy co `processing.run` — podstawa twierdzenia o stałym silniku | rozdz. 3 (3) |
| native algorithm | algorytm natywny | Algorytm dostarczany przez QGIS (`native:buffer`), a nie przez wtyczkę zewnętrzną | rozdz. 3 (3) |
| reference solution | rozwiązanie referencyjne | Sprawdzone rozwiązanie zadania, od którego mierzy się trudność i waliduje wyrocznię | rozdz. 4 (2) |

---
| silent error | cichy błąd | Błąd, który nie kończy się wyjątkiem: wynik jest poprawną wartością o poprawnym typie i kształcie, a niepoprawny znaczeniowo | rozdz. 3 (1) |
| expressible share | udział wyrażalny | Część wymagań zadania, którą powierzchnia przyjmuje jako parametr i umie sprawdzić, podzielona przez wszystkie wymagania | rozdz. 3 (1) |
| knowledge level P-I/P-II/P-III | poziom wiedzy narzędzia | Ile narzędzie może wiedzieć: P-I składnia, P-II niezmienniki dziedzinowe, P-III intencja zadania — inny wymiar niż głębokość egzekwowania | rozdz. 3 (1) |

## 3. Projekt eksperymentu

| English | Polski | Co znaczy | Gdzie |
|---|---|---|---|
| condition / experimental arm | warunek / ramię | Jedna konfiguracja czynników, w której zadanie jest rozwiązywane (np. `katalog+gate`) | rozdz. 3 (2) |
| factor | czynnik | Zmienna manipulowana przez badacza (interfejs, walidacja, poziom drabinki) | rozdz. 3 (2) |
| level | poziom czynnika | Konkretna wartość czynnika (interfejs: katalog / kod; drabinka: 5 / 15 / 30) | rozdz. 3 (2) |
| paired design | projekt parowany | To samo zadanie, dane i wyrocznia w każdym warunku; różnice liczone w obrębie zadania | rozdz. 4 (7) |
| blocking | blokowanie | Grupowanie przebiegów tak, by zmienność bloku nie wchodziła do porównania (blok = zadanie) | rozdz. 4 (7) |
| randomisation | randomizacja | Losowa kolejność przebiegów w obrębie bloku, z zapisanym ziarnem | rozdz. 4 (7) |
| counterbalancing | równoważenie kolejności | Zapewnienie, że żaden warunek nie jest systematycznie pierwszy (dryf, zmęczenie, cache) | rozdz. 4 (7) |
| run | przebieg | Jedno uruchomienie agenta na jednym zadaniu w jednym warunku | rozdz. 4 (1) |
| repetition | powtórzenie | Kolejny przebieg tej samej pary (zadanie × warunek) | rozdz. 4 (1) |
| cell | komórka macierzy | Pojedyncze przecięcie zadanie × warunek × powtórzenie | rozdz. 5 (2) |
| coverage matrix | macierz pokrycia | Tabela domknięcia wszystkich komórek; bramka G4 wymaga zera pustych | rozdz. 5 (2) |
| manifest | manifest | Zbiór rekordów opisujących wszystkie przebiegi; jedno źródło wszystkich liczb w rozdziale 6 | rozdz. 4 (6) |
| pre-registration | pre-rejestracja | Dokument z hipotezami, regułami decyzyjnymi i progami, złożony **przed** pierwszym przebiegiem | rozdz. 3 (5) |
| freeze | zamrożenie | Moment, po którym żadna liczba ani reguła nie zmienia się bez wpisu „zmiana po podglądzie" | rozdz. 3 (5) |
| validation boundary (`gate`) | granica walidacji | Trzy elementy naraz: walidacja przed wykonaniem, sprawdzenie artefaktu po wykonaniu, jedna iteracja naprawy. **Nie mylić z bramką projektu (G1–G7)** | rozdz. 4 (4) |
| milestone gate (G1–G7) | bramka projektu | Punkt kontrolny harmonogramu, bez którego nie przechodzi się do następnego bloku | rozdz. 5 (1) |
| negative control | kontrola negatywna | Celowo zepsuty artefakt, który wyrocznia **musi** odrzucić — dowód, że mierzy, a nie zalicza | rozdz. 4 (2) |
| oracle | wyrocznia | Program sprawdzający artefakt predykatami; tajna i zamrożona przed sweepem | rozdz. 4 (2) |
| ground truth | prawda odniesienia | Rozwiązanie uznane za poprawne, od którego porównuje się artefakty agenta | rozdz. 4 (2) |
| adversarial probe | sonda adwersaryjna | Zadania z celowo zwodniczymi opisami/CRS; raportowana **opisowo**, bez testu | rozdz. 6 (10) |
| control slice | wycinek kontrolny | Mała warstwa sprawdzająca, czy wynik nie jest własnością jednej aplikacji agentowej | rozdz. 6 (9) |
| portability slice | wycinek przenośności | Mała warstwa sprawdzająca powtarzalność wyniku poza środowiskiem autora | rozdz. 6 (9) |
| throttle / rate limit | limit zapytań | Ograniczenie dostawcy modelu; źródło anomalii instrumentu, nie wyniku | rozdz. 6 (11) |

---

## 4. Miary i wyniki

| English | Polski | Co znaczy | Gdzie |
|---|---|---|---|
| task success rate (TSR) | współczynnik sukcesu zadań | Odsetek przebiegów, w których **wszystkie** wymagane predykaty są spełnione | rozdz. 4 (5) |
| partial credit (OQS/PCS) | wynik częściowy | Ważony udział spełnionych predykatów; mówi *jak blisko* był przebieg | rozdz. 4 (5) |
| repeatability (D1; dawne ED) | powtarzalność | Czy powtórzenia dają **ten sam artefakt** (identyczne / równoważne / rozbieżne) i czy klasa błędu jest ta sama — mierzone jako S3 i klasy na poziomie predykatów | rozdz. 6 (6) |
| repair (dawne RRR) | naprawa | Wycofane jako osobna miara; w rejestrze zostaje `repair_iterations`, a o naprawie rozstrzyga licznik przy bramce | rozdz. 4 (8) |
| turns to a correct artefact (dawne T2V) | liczba tur do poprawnego artefaktu | Miara drugorzędna, z cenzurowaniem przy braku sukcesu | rozdz. 4 (8) |
| silent error | błąd cichy | Wynik o poprawnym typie i kształcie, fałszywy w sensie — klasa, dla której cała ta praca istnieje | rozdz. 4 (10) |
| call validity score (CVS) | wskaźnik legalności wywołań | Udział wywołań zgodnych ze schematem i dozwolonymi modułami; rozdziela „złą odpowiedź" od „niedozwolonego ruchu" | rozdz. 4 (5) |
| cost per success | koszt zadania zakończonego sukcesem | Tokeny (czas, wywołania) ÷ liczba sukcesów — **nie** koszt pojedynczcego wywołania | rozdz. 6 (8) |
| effect size | wielkość efektu | Liczbowa miara różnicy (w p.p., OR), niezależna od istotności | rozdz. 6 (1) |
| odds ratio (OR) | iloraz szans | Stosunek szans sukcesu w jednym ramieniu do szans w drugim; OR 1,64 ≈ +10 p.p. przy TSR ~48 % | rozdz. 6 (1) |
| interaction | interakcja | Sytuacja, w której efekt jednego czynnika zależy od poziomu drugiego (np. przewaga katalogu zależy od rodziny) | rozdz. 6 (2) |
| dominance | dominacja | Jeden warunek jest lepszy **jednocześnie** pod względem skuteczności i kosztu | rozdz. 6 (8) |
| ranking reversal | odwrócenie rankingu | Warunek wygrywa na skuteczności, a przegrywa na koszcie (lub odwrotnie) | rozdz. 6 (8) |

---

## 5. Statystyka i wnioskowanie

| English | Polski | Co znaczy | Gdzie |
|---|---|---|---|
| null hypothesis | hipoteza zerowa | Założenie braku różnicy, które test odrzuca lub nie | rozdz. 3 (4) |
| falsification criterion | kryterium falsyfikacji | Z góry opisany wynik, który **obala** hipotezę | rozdz. 3 (4) |
| confirmatory test | test potwierdzający | Jedyny test w pracy, dla którego ustalono α = 0,05 i który rozstrzyga H1 | rozdz. 3 (6) |
| exploratory analysis | analiza eksploracyjna | Analiza bez progu istotności; raportowana z CI i wielkością efektu, bez gwiazdek | rozdz. 6 (2) |
| significance level (α) | poziom istotności | Dopuszczalne ryzyko błędu I rodzaju; tu 0,05 dla H1 | rozdz. 3 (4) |
| statistical power | moc testu | Prawdopodobieństwo wykrycia efektu o zadanej wielkości, gdy istnieje; tu 0,80 | rozdz. 3 (4) |
| minimum detectable effect (MDE) | minimalna wykrywalna różnica | Najmniejsza różnica, którą projekt wykryje z mocą 0,80; tu **9,3 p.p.** dla 40 × 16 | rozdz. 3 (4) |
| smallest effect size of interest (SESOI) | najmniejsza różnica mająca znaczenie | Najmniejszy efekt, który zmieniłby wniosek praktyczny — dobierany **razem** z MDE | rozdz. 3 (4) |
| undecided (verdict) | nierozstrzygnięte | Trzecia wartość osądu: różnica mniejsza niż MDE. Czwartej kategorii („równoważność wykazana") nie ma, bo projekt nie zawiera testu równoważności | rozdz. 6 (1) |
| equivalence margin | margines równoważności | Dopuszczalna różnica uznawana za równoważną; tu ±20 p.p. | rozdz. 6 (4) |
| Holm correction | korekta Holma | Sekwencyjna korekta wielu porównań w obrębie rodziny hipotez (silniejsza od Bonferroniego) | rozdz. 3 (4) |
| multiplicity | wielokrotność porównań | Liczba testów w rodzinie; bez korekty zawyża odsetek fałszywych odkryć | rozdz. 3 (4) |
| mixed-effects logistic model | mieszany model logistyczny | Model regresji logistycznej z losowym efektem zadania — uwzględnia zagnieżdżenie przebiegów w zadaniach | rozdz. 6 (1) |
| random intercept | losowy efekt zadania (random intercept) | Przesunięcie modelu różne dla każdego zadania; wchłania jego trudność | rozdz. 6 (1) |
| pseudoreplication | pseudoreplikacja | Liczenie *df* od przebiegów zamiast od zadań — zaniża *p* i jest błędem | rozdz. 4 (7) |
| cluster bootstrap | bootstrap klastrowy | Losowanie **zadań** ze zwracaniem do wyznaczenia CI; jedyna poprawna metoda dla kosztu/sukces | rozdz. 6 (8) |
| confidence interval (CI) | przedział ufności | Zakres wartości zgodnych z danymi na zadanym poziomie ufności (95 %) | rozdz. 6 (1) |
| intraclass correlation (ICC) | korelacja wewnątrzklasowa | Udział wariancji wyjaśniany przez zgrupowanie (zadanie) | rozdz. 6 (11) |
| inconclusive | nierozstrzygnięty | Wynik, którego projekt nie potrafi rozstrzygnąć (różnica < MDE) — **nie** to samo co „brak różnicy" | rozdz. 6 (3) |
| reproducibility vs replicability | odtwarzalność vs powtarzalność | Odtwarzalność: te same dane + ta sama analiza → ten sam wynik. Powtarzalność: nowe dane → ten sam wniosek | rozdz. 4 (8) |
| threat to validity | zagrożenie trafności | Systematyczne źródło błędu wnioskowania (np. jeden silnik, jeden model) | rozdz. 7 (3) |
| measurement validity | trafność pomiaru | Czy miernik mierzy to, co nazywa — tu najsłabsze ogniwo; dlatego kontrola negatywna i κ | rozdz. 4 (7) |

---

## 6. Błędy i ich taksonomia

| English | Polski | Co znaczy | Gdzie |
|---|---|---|---|
| silent error | błąd cichy | Wynik wygląda poprawnie, ale jest zły (np. niewykryty błąd CRS) — najgroźniejsza klasa w ramieniu kodu | rozdz. 6 (5) |
| loud error | błąd głośny | Błąd widoczny i nazwany (zły parametr, nieistniejące narzędzie) — dominuje w ramieniu katalogu | rozdz. 6 (5) |
| error signature | sygnatura błędów | Charakterystyczny rozkład klas błędów dla danego interfejsu | rozdz. 6 (5) |
| failure taxonomy | taksonomia błędów | Zamknięty słownik 7 klas używany do kodowania porażek | rozdz. 4 (6) |
| near miss | bliskie nietrafienie | Artefakt podobny do poprawnego, ale niespełniający predykatu (np. convex hull zamiast bufora) | rozdz. 4 (2) |
| distractor | dystraktor | Narzędzie obecne w katalogu, ale niepotrzebne; utrudnia selekcję | rozdz. 4 (3) |
| close relative | bliski krewny | Dystraktor, którego wynik spełnia **część** predykatów zadania | rozdz. 4 (3) |
| gate rejection | odrzucenie przez granicę walidacji | Wywołanie odrzucone przed wykonaniem z powodu naruszenia kontraktu | rozdz. 4 (4) |
| inter-rater agreement (κ) | zgodność między kodującymi | Czy dwie osoby kodują ten sam błąd tak samo; próg κ ≥ 0,6 | rozdz. 4 (6) |
| blind coding | kodowanie w ciemno | Kodowanie bez informacji o warunku — warunek wiarygodności D2 | rozdz. 4 (9) |

---

## 7. Pułapki tłumaczeniowe i terminy zakazane

| Nie pisz | Pisz | Dlaczego |
|---|---|---|
| „istotny" (= significant) | **„istotny statystycznie"** | Po polsku „istotny" znaczy „ważny"; bez przymiotnika zdanie jest dwuznaczne |
| „znaczący" (= significant) | **„istotny statystycznie"** | Kalka; „znaczący" = „duży", a to inna informacja |
| „MCP kontra REST" | **„MCP a generowanie kodu"** | W eksperymencie **nie ma** ramienia REST; takie zdanie opisuje inne badanie |
| „brak różnicy" | **„wynik nierozstrzygnięty"** lub **„równoważność wykazana"** | Rozróżnienie rozstrzyga, czy wniosek jest mocny czy pusty |
| „protokół zastępuje walidację" | **„kod z walidacją osiąga równoważność z katalogiem w P i A, ale nie w C"** | Twierdzenie bezwarunkowe jest szersze niż dane |
| „framework agentowy" | **„pętla agenta" / „stanowisko eksperymentalne"** | Pętla jest instrumentem, nie tematem pracy |
| „agent AI" | **„agent oparty na modelu językowym"** | Precyzja: badamy zachowanie modelu z narzędziami, nie „AI" |
| „benchmark" | **„zadanie / korpus zadań"** | Praca nie jest benchmarkiem; nie publikuje rankingu modeli |
| „wydajność" bez miary | **„skuteczność (TSR)" / „koszt tokenowy" / „czas"** | „Wydajność" miesza trzy różne metryki |
| „wrapper MCP" | **„warstwa pośrednia MCP"** | „Wrapper" sugeruje trywialność; w pracy to przedmiot oceny |
| „żeton", „parsowanie" | **„token", „parsowanie" (lub „analiza składniowa")** | Spolszczenia psują tekst techniczny |
| „agent działa autonomicznie" | **„agent wykonuje zadanie bez interwencji człowieka w trakcie przebiegu"** | „Autonomicznie" jest niedefiniowalne operacyjnie |
| „null" w GIS i „null" w statystyce | **„wartość pusta" vs „hipoteza zerowa"** | Ten sam napis, dwie różne rzeczy |

---

## 8. Indeks skrótów

| Skrót | Rozwinięcie | Polski |
|---|---|---|
| **MCP** | Model Context Protocol | Protokół kontekstu modelu |
| **TSR** | task success rate | współczynnik sukcesu zadań |
| **OQS / PCS** | output quality score / process claim score | wynik częściowy |
| **S3** | repeatability share | udział powtarzalności |
| **S4 / S4b** | check present / domain check | sprawdzenie obecne / sprawdzenie dziedzinowe |
| **S5** | auditability | audytowalność |
| **ICC / DEFF** | intraclass correlation / design effect | korelacja wewnątrzklasowa / efekt projektu |
| **CVS** | call validity score | wskaźnik legalności wywołań |
| **MDE** | minimum detectable effect | minimalna wykrywalna różnica |
| **SESOI** | smallest effect size of interest | najmniejsza różnica mająca znaczenie |
| **D1–D4** | descriptive and precondition claims | twierdzenia opisowe i warunek wstępny |
| **CI** | confidence interval | przedział ufności |
| **OR** | odds ratio | iloraz szans |
| **ICC** | intraclass correlation | korelacja wewnątrzklasowa |
| **CRS** | coordinate reference system | układ współrzędnych odniesienia |
| **IoU** | intersection over union | miara pokrycia zasięgów |
| **κ** | Cohen's kappa | zgodność między kodującymi |
| **G1–G7** | milestone gates | bramki projektu |

---

## 9. Jak to wstawić do pracy

Cztery miejsca w pracy, żadne w załącznikach:

1. **Rozdział 2 (przegląd literatury)** — cztery lub pięć pojęć protokołu, których recenzent nie zna: MCP, powierzchnia i katalog narzędzi, wywołanie narzędzia. Bez nich rozdział 4 czyta się jak instrukcja do nieistniejącego urządzenia.
2. **Rozdział 3 (materiały i metody), podrozdział o przedmiocie oceny** — tabela z §2 tego dokumentu (GIS i predykaty); to jest miejsce, gdzie „co znaczy poprawne" musi być jednoznaczne.
3. **Rozdział 4 (instrument)** — pełny słownik predykatów, bo tam recenzent sprawdza, co jest manipulowane; to jest zarazem źródło załącznika C.
4. **§7 tego dokumentu** — nie do pracy, ale **do własnej kontroli przed oddaniem**: przejrzyj tekst pod kątem zakazanych zwrotów, zwłaszcza „istotny" bez „statystycznie" i „brak różnicy".
