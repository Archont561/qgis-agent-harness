---
id: external-sources
title: "External sources — what used to sit in `uploads/` and where the knowledge from it lives"
type: register
status: live
language: en
updated_date: '2026-11-07'
---

# External sources — what used to sit in `uploads/` and where the knowledge from it lives

> The `uploads/` directory (3 PDFs, 2.7 MB) was **deleted on 2026-11-07**. This file is the provenance trace: which document, in which version, what follows from it, and in which `thesis/` file that knowledge now sits.
> The rule: **a conversion or a summary enters the tree, never a scan.** All three documents are public and re-obtainable, and binaries submit to neither searching, nor terminology correction, nor linting.

| Document | Version / issuing body | What follows from it | Where the knowledge lives | Status |
|---|---|---|---|---|
| **UMCS WNoZiGP diploma rules** | 2025/2026, 23 pages | thesis type, eligibility, APD and exam deadlines, structure per §V, formatting, citation | `writing/requirements.md` (summary with consequences) + `umcs-regulations-2025-26.txt` (full text, `===== PAGE n =====` markers) | **in force** |
| **SGP + GGK competition rules** ("KD") | 2023, 8 pages | eligibility conditions, scoring 0–10 / 0–5 / 0–5, appendices 2–3 | `competitions/sgp-kd-rules-2023.md` (faithful conversion, § numbering preserved) | in force until the edition changes |
| **Order no. 3 of the MRiT** — Minister's Award (geoinformation) | 4 Dec 2020, 22 pages, MRiT Official Journal item 6 | application procedure through the university body, appendices, deadlines | `competitions/marpit-geoinformation-award-2020.md` (faithful conversion) | **archival** — the fifth edition already ran on Order no. 33 of 10 Aug 2022; fetch the current one before applying |

## What is **not** here, and why

- **The PDFs.** The conversions are faithful (§ and appendix numbering preserved), so a PDF adds nothing the Markdown lacks, weighs 2.7 MB, and cannot be cited in a search.
- **URLs to the PDFs.** Two of the three were local files with no durable address; the only verifiable address is the PTI page (`https://kpm.pti.org.pl/terms`, retrieved 2026-11-01), recorded in `competitions/pti-kpm-rules.md`.
- **Page snapshots.** Their place is taken by the conversion with the retrieval date in the file header.

## The rule going forward

A new external document enters `thesis/` **only as a conversion or a summary with a date and a version**, recorded in the table above. If a conversion is impossible (a scan without a text layer, a paywalled document), the file stays outside the tree and the table entry says where to look for it and what is missing from it.
