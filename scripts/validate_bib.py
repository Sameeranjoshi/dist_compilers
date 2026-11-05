#!/usr/bin/env python3
"""Validate bibliography/references.bib against catalog/papers.yaml.

  * every catalog paper id has a BibTeX entry with the same key;
  * every BibTeX key is a catalog id (no orphan references);
  * required fields per entry type are present;
  * DOI / year in the .bib agree with the catalog;
  * keys are valid BibTeX keys.
Exit 1 on error.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "misc": ["title", "year"],
    "book": ["author", "title", "publisher", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "incollection": ["author", "title", "booktitle", "year"],
}


def parse_bib(text):
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", text, re.S):
        etype, key, body = m.group(1).lower(), m.group(2), m.group(3)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\n]+)", body):
            fields[fm.group(1).lower()] = fm.group(2).strip().strip("{}\"").strip()
        entries[key] = (etype, fields)
    return entries


def main():
    bib_path = ROOT / "bibliography" / "references.bib"
    entries = parse_bib(bib_path.read_text(encoding="utf-8"))
    papers = {p["id"]: p for p in yaml.safe_load(open(ROOT / "catalog" / "papers.yaml", encoding="utf-8"))["papers"]}
    errors = []
    for pid in papers:
        if pid not in entries:
            errors.append(f"catalog paper '{pid}' has no BibTeX entry")
    for key, (etype, fields) in entries.items():
        if not re.fullmatch(r"[A-Za-z0-9:_-]+", key):
            errors.append(f"invalid BibTeX key '{key}'")
        if key not in papers:
            errors.append(f"BibTeX key '{key}' is not a catalog id")
            continue
        for f in REQUIRED.get(etype, ["title", "year"]):
            if f not in fields:
                errors.append(f"{key}: missing required field '{f}' for @{etype}")
        p = papers[key]
        if "year" in fields and str(p["year"]) != fields["year"]:
            errors.append(f"{key}: year {fields['year']} in .bib but {p['year']} in catalog")
        if p.get("doi") and fields.get("doi", "").lower() != p["doi"].lower():
            errors.append(f"{key}: doi mismatch (.bib '{fields.get('doi')}' vs catalog '{p['doi']}')")
    for e in errors:
        print("ERROR:", e)
    print(f"{len(entries)} bib entries, {len(papers)} catalog papers, {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
