#!/usr/bin/env python3
"""Append a skeleton paper entry to catalog/papers.yaml and a BibTeX entry to
bibliography/references.bib from a DOI or arXiv id (metadata via Crossref/arXiv).

    python scripts/add_paper.py --id koelbel1991compiling --doi 10.1109/71.97901
    python scripts/add_paper.py --id xu2021gspmd --arxiv 2105.04663

The entry is created with status `discovered`, verified: false, empty taxonomy
fields and a placeholder summary that the validator will flag; edit it by hand.
"""
import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_metadata import arxiv_by_id, crossref_by_doi  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "catalog" / "papers.yaml"
BIB = ROOT / "bibliography" / "references.bib"


def bib_entry(pid, m, arxiv=None):
    authors = " and ".join(m["authors"])
    if arxiv:
        return (f"@misc{{{pid},\n  title = {{{m['title']}}},\n  author = {{{authors}}},\n  year = {{{m['year']}}},\n"
                f"  eprint = {{{arxiv}}},\n  archiveprefix = {{arXiv}},\n  howpublished = {{arXiv:{arxiv}}},\n"
                f"  url = {{https://arxiv.org/abs/{arxiv}}},\n}}\n")
    etype = "article" if m.get("type") == "journal-article" else "inproceedings"
    venue_key = "journal" if etype == "article" else "booktitle"
    fields = [f"  title = {{{m['title']}}}", f"  author = {{{authors}}}", f"  {venue_key} = {{{m['venue']}}}", f"  year = {{{m['year']}}}"]
    for k in ("volume", "issue", "pages"):
        if m.get(k):
            fields.append(f"  {'number' if k == 'issue' else k} = {{{m[k]}}}")
    if m.get("publisher"):
        fields.append(f"  publisher = {{{m['publisher']}}}")
    fields.append(f"  doi = {{{m['doi']}}}")
    return f"@{etype}{{{pid},\n" + ",\n".join(fields) + ",\n}\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--doi")
    ap.add_argument("--arxiv")
    ap.add_argument("--era", default="era3")
    ap.add_argument("--tier", default="core")
    a = ap.parse_args()
    if not (a.doi or a.arxiv):
        sys.exit("need --doi or --arxiv")
    m = crossref_by_doi(a.doi) if a.doi else arxiv_by_id(a.arxiv)[0]
    doc = yaml.safe_load(open(PAPERS, encoding="utf-8"))
    if any(p["id"] == a.id for p in doc["papers"]):
        sys.exit(f"id {a.id} already exists")
    entry = {
        "id": a.id, "title": m["title"], "authors": m["authors"], "year": m["year"],
        "venue": m.get("venue") or "arXiv", "paper_type": "compiler-technique", "doi": m.get("doi"), "arxiv": a.arxiv,
        "official_url": f"https://doi.org/{m['doi']}" if m.get("doi") else f"https://arxiv.org/abs/{a.arxiv}",
        "pdf_url": f"https://arxiv.org/pdf/{a.arxiv}" if a.arxiv else None,
        "access_status": "open" if a.arxiv else "paywalled", "era": a.era, "relevance_tier": a.tier,
        "status": "discovered", "verified": False, "summary": "TODO: original summary", "why_read": None,
        "input_abstraction": [], "target_hardware": [], "data_decomposition": [], "computation_mapping": [],
        "communication_generation": [], "compiler_runtime_boundary": [], "compiler_architecture": [],
        "ir_representation": [], "optimization_objectives": [], "maturity": [], "predecessors": [], "successors": [],
        "taxonomy_tags": [], "readme_categories": [], "technique_lists": [],
        "evidence": [{"source": "Crossref metadata" if a.doi else "arXiv metadata", "section": "bibliographic record", "pages": None}],
        "metadata_sources": ["crossref" if a.doi else "arxiv"], "notes": None,
    }
    doc["papers"].append(entry)
    with open(PAPERS, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True, width=100)
    with open(BIB, "a", encoding="utf-8") as f:
        f.write("\n" + bib_entry(a.id, m, a.arxiv))
    print(f"added {a.id}: {m['title']} ({m['year']})")


if __name__ == "__main__":
    main()
