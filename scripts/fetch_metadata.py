#!/usr/bin/env python3
"""Look up bibliographic metadata for papers from public, non-paywalled indexes.

Sources (in this order): Crossref (DOI + venue), DBLP (venue/year cross-check),
arXiv API (for preprints).  Nothing is scraped from publisher full-text pages.

Usage:
    python scripts/fetch_metadata.py --title "Compiling Fortran D for MIMD" [--author Tseng] [--year 1992]
    python scripts/fetch_metadata.py --doi 10.1145/143095.143108
    python scripts/fetch_metadata.py --arxiv 2105.04663
    python scripts/fetch_metadata.py --batch queries.json --out results.json

The output is JSON; it is meant to be *reviewed by a human* before being
copied into catalog/papers.yaml (see docs/methodology.md, "Verification").
"""
import argparse
import json
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET

import requests

UA = "dist-compilers-survey/0.1 (https://github.com/Sameeranjoshi/dist_compilers)"
HEADERS = {"User-Agent": UA}
SKIP_DBLP = False
TIMEOUT = 30.0  # set by --no-dblp (DBLP sits behind a bot check for some networks)


def crossref_by_title(title, author=None, year=None, rows=3):
    params = {"query.bibliographic": title, "rows": rows}
    if author:
        params["query.author"] = author
    if year:
        params["filter"] = f"from-pub-date:{int(year)-1},until-pub-date:{int(year)+1}"
    r = requests.get("https://api.crossref.org/works", params=params, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return [_cr_item(i) for i in r.json()["message"]["items"]]


def crossref_by_doi(doi):
    r = requests.get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}", headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return _cr_item(r.json()["message"])


def _cr_item(i):
    date = i.get("issued", {}).get("date-parts", [[None]])[0]
    return {
        "source": "crossref",
        "doi": i.get("DOI"),
        "title": (i.get("title") or [""])[0],
        "authors": [f"{a.get('given','')} {a.get('family','')}".strip() for a in i.get("author", [])],
        "year": date[0] if date else None,
        "venue": (i.get("container-title") or i.get("event", {}).get("name") or [""])[0]
        if isinstance(i.get("container-title") or [""], list) else i.get("container-title"),
        "publisher": i.get("publisher"),
        "type": i.get("type"),
        "url": i.get("URL"),
        "volume": i.get("volume"),
        "issue": i.get("issue"),
        "pages": i.get("page"),
    }


def dblp_by_title(title, rows=3):
    r = requests.get("https://dblp.org/search/publ/api", params={"q": title, "format": "json", "h": rows},
                     headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    hits = r.json().get("result", {}).get("hits", {}).get("hit", []) or []
    out = []
    for h in hits:
        info = h["info"]
        authors = info.get("authors", {}).get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        out.append({
            "source": "dblp",
            "title": info.get("title", "").rstrip("."),
            "authors": [a["text"] for a in authors],
            "year": int(info["year"]) if info.get("year") else None,
            "venue": info.get("venue"),
            "doi": info.get("doi"),
            "url": info.get("ee"),
            "dblp_key": info.get("key"),
            "type": info.get("type"),
        })
    return out


def arxiv_by_id(arxiv_id):
    r = requests.get("https://export.arxiv.org/api/query", params={"id_list": arxiv_id}, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(r.text)
    out = []
    for e in root.findall("a:entry", ns):
        out.append({
            "source": "arxiv",
            "arxiv": e.find("a:id", ns).text.split("/abs/")[-1],
            "title": " ".join(e.find("a:title", ns).text.split()),
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "year": int(e.find("a:published", ns).text[:4]),
            "doi": (e.find("{http://arxiv.org/schemas/atom}doi") is not None
                    and e.find("{http://arxiv.org/schemas/atom}doi").text) or None,
        })
    return out


def arxiv_by_title(title, rows=3):
    r = requests.get("https://export.arxiv.org/api/query",
                     params={"search_query": f'ti:"{title}"', "max_results": rows}, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(r.text)
    return [{
        "source": "arxiv",
        "arxiv": e.find("a:id", ns).text.split("/abs/")[-1],
        "title": " ".join(e.find("a:title", ns).text.split()),
        "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
        "year": int(e.find("a:published", ns).text[:4]),
    } for e in root.findall("a:entry", ns)]


def lookup(q):
    res = {"query": q, "crossref": [], "dblp": [], "arxiv": []}
    try:
        if q.get("doi"):
            res["crossref"] = [crossref_by_doi(q["doi"])]
        elif q.get("title"):
            res["crossref"] = crossref_by_title(q["title"], q.get("author"), q.get("year"))
    except Exception as e:  # noqa: BLE001
        res["crossref_error"] = str(e)
    if not SKIP_DBLP:
        try:
            if q.get("title"):
                res["dblp"] = dblp_by_title(q["title"])
        except Exception as e:  # noqa: BLE001
            res["dblp_error"] = str(e)
    try:
        if q.get("arxiv"):
            res["arxiv"] = arxiv_by_id(q["arxiv"])
        elif q.get("title") and (q.get("year") or 0) >= 2010:
            res["arxiv"] = arxiv_by_title(q["title"])
    except Exception as e:  # noqa: BLE001
        res["arxiv_error"] = str(e)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title")
    ap.add_argument("--author")
    ap.add_argument("--year", type=int)
    ap.add_argument("--doi")
    ap.add_argument("--arxiv")
    ap.add_argument("--batch", help="JSON list of query objects {id,title,author,year,doi,arxiv}")
    ap.add_argument("--out", help="write JSON results here (default stdout)")
    ap.add_argument("--sleep", type=float, default=1.0, help="pause between batch queries (politeness)")
    ap.add_argument("--no-dblp", action="store_true", help="skip DBLP (it may be bot-gated)")
    ap.add_argument("--timeout", type=float, default=30.0, help="per-request timeout in seconds")
    a = ap.parse_args()
    global SKIP_DBLP, TIMEOUT
    SKIP_DBLP = a.no_dblp
    TIMEOUT = a.timeout
    if a.batch:
        queries = json.load(open(a.batch))
    else:
        queries = [{k: v for k, v in dict(title=a.title, author=a.author, year=a.year, doi=a.doi, arxiv=a.arxiv).items() if v}]
    results = []
    for i, q in enumerate(queries):
        print(f"[{i+1}/{len(queries)}] {q.get('id') or q.get('title') or q.get('doi')}", file=sys.stderr)
        results.append(lookup(q))
        if a.out:
            open(a.out, "w").write(json.dumps(results, indent=2, ensure_ascii=False))
        if a.batch:
            time.sleep(a.sleep)
    text = json.dumps(results, indent=2, ensure_ascii=False)
    if a.out:
        open(a.out, "w").write(text)
    else:
        print(text)


if __name__ == "__main__":
    main()
