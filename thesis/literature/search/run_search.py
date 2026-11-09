#!/usr/bin/env python3
"""
run_search.py — execute the revised GeoAIWorkbench search protocol against the
keyless sources (arXiv API, OpenAlex). Scopus has no keyless path: the Scopus
strings in queries.json are for a host run (pybliometrics / web export).

    python3 run_search.py                 # all queries, counts only
    python3 run_search.py --fetch         # also store top-N records per query
    python3 run_search.py --recall        # known-item recall test only

Archived run (2026-10-31) lives in ./wyniki-2026-10-31/; a fresh run writes to ./results/.
The script is reproduction tooling, not harness code: it has no tests and is not imported anywhere.

Outputs (in ./results/):
    <ID>_arxiv.json / <ID>_openalex.json
    search-log.csv        — the table to paste into .knowledge/01-literature/search-log.md §9
    summary.md            — human-readable run report
"""

import argparse
import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
EMAIL = os.environ.get("SCHOLAR_EMAIL", "geoaiworkbench@example.invalid")
UA = {"User-Agent": f"geoaiworkbench-search/1.0 (mailto:{EMAIL})"}
START, END = "202411010000", date.today().strftime("%Y%m%d") + "0000"
MAXREC = 200
os.makedirs(RES, exist_ok=True)

QSPEC = json.load(open(os.path.join(HERE, "queries.json")))["queries"]


def fetch(url, tries=4):
    for a in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=60
            ).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and a < tries - 1:
                time.sleep(3 * (a + 1))
                continue
            raise


# ---------------------------------------------------------------- arXiv
def arxiv_run(q, maxrec=MAXREC):
    sq = f"({q}) AND submittedDate:[{START} TO {END}]"
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": sq, "max_results": maxrec, "sortBy": "relevance"}
    )
    xml = fetch(url).decode()
    total = int(re.search(r"<opensearch:totalResults[^>]*>(\d+)<", xml).group(1))
    recs = []
    for e in re.split(r"<entry>", xml)[1:]:
        recs.append(
            {
                "id": re.search(r"<id>.*?/abs/(.*?)</id>", e).group(1),
                "title": " ".join(re.search(r"<title>(.*?)</title>", e, re.S).group(1).split()),
                "published": re.search(r"<published>(.*?)</published>", e).group(1)[:10],
            }
        )
    return total, recs


# ---------------------------------------------------------------- OpenAlex
def oa_run(params, maxrec=MAXREC):
    p = dict(params)
    p.update({"per-page": min(maxrec, 200), "mailto": EMAIL})
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(p)
    d = json.loads(fetch(url))
    return d["meta"]["count"], [
        {
            "id": w["id"].split("/")[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "title": w.get("display_name"),
            "year": w.get("publication_year"),
            "cites": w.get("cited_by_count"),
        }
        for w in d["results"]
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--recall", action="store_true")
    a = ap.parse_args()

    rows, seen_arxiv = [], {}
    for q in QSPEC:
        row = {
            "id": q["id"],
            "rq": ",".join(q["rq"]),
            "concept": q["concept"],
            "date": str(date.today()),
        }
        if not a.recall and q.get("arxiv"):
            try:
                total, recs = arxiv_run(q["arxiv"])
                row["arxiv_hits"] = total
                if a.fetch:
                    json.dump(recs, open(f"{RES}/{q['id']}_arxiv.json", "w"), indent=1)
                for r in recs:
                    seen_arxiv.setdefault(r["id"].split("v")[0], r["title"])
                print(f"{q['id']:4s} arXiv   {total:6d}  {q['concept'][:62]}")
            except Exception as e:
                row["arxiv_hits"] = f"ERR {e}"
                print(f"{q['id']:4s} arXiv   ERROR {e}")
            time.sleep(3)  # arXiv etiquette
        if not a.recall and q.get("openalex"):
            try:
                total, recs = oa_run(q["openalex"])
                row["openalex_hits"] = total
                if a.fetch:
                    json.dump(recs, open(f"{RES}/{q['id']}_openalex.json", "w"), indent=1)
                print(f"{q['id']:4s} OpenAlex {total:6d}")
            except Exception as e:
                row["openalex_hits"] = f"ERR {e}"
                print(f"{q['id']:4s} OpenAlex ERROR {e}")
        rows.append(row)

    # ---------------------------------------------------------- recall test
    spec = json.load(open(os.path.join(HERE, "queries.json")))
    expected = {
        k.split(" (")[0]: re.search(r"\(([\d.]+)\)", k).group(1)
        for k in spec["known_items_recall_test"]["yields"]
    }
    recall = []
    for name, aid in expected.items():
        base = aid.split("v")[0]
        hit = base in seen_arxiv
        recall.append({"work": name, "arxiv_id": aid, "found_by_any_query": "YES" if hit else "NO"})
        print(f"recall  {name:32s} {aid:12s} {'OK' if hit else 'MISSING'}")

    with open(f"{RES}/search-log.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["id", "rq", "concept", "date", "arxiv_hits", "openalex_hits"]
        )
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "—") for k in w.fieldnames})
    json.dump(
        {"rows": rows, "recall": recall}, open(f"{RES}/run-{date.today()}.json", "w"), indent=1
    )

    with open(f"{RES}/summary.md", "w") as f:
        f.write(
            f"# Automated search run — {date.today()}\n\n"
            f"arXiv window: {START[:8]} → {END[:8]}; "
            f"OpenAlex: publication_year>2022/2023 per query.\n"
            "Scopus: **not run here** (no keyless endpoint) — "
            "use the strings in `queries.json`.\n\n"
        )
        f.write("| Q | RQ | Concept | arXiv hits | OpenAlex hits |\n|---|---|---|---|---|\n")
        for r in rows:
            f.write(
                f"| {r['id']} | {r['rq']} | {r['concept']} | {r.get('arxiv_hits', '—')} "
                f"| {r.get('openalex_hits', '—')} |\n"
            )
        f.write(
            "\n## Known-item recall\n\n"
            "| Work | arXiv ID | Retrievable by the protocol |\n|---|---|---|\n"
        )
        for r in recall:
            f.write(f"| {r['work']} | {r['arxiv_id']} | {r['found_by_any_query']} |\n")
    print(f"\nwrote {RES}/search-log.csv, summary.md, run-{date.today()}.json")


if __name__ == "__main__":
    main()
