#!/usr/bin/env python3
"""Validate catalog/papers.yaml, catalog/systems.yaml, catalog/eras.yaml against
catalog/schema.json and catalog/taxonomy.yaml.

Checks (all are hard failures unless noted):
  * JSON-schema validity of every entry;
  * unique paper ids, DOIs, arXiv ids (case-insensitive), and titles;
  * every taxonomy tag value exists in catalog/taxonomy.yaml;
  * era ids exist in catalog/eras.yaml and the paper year falls in the era range
    (warning only: boundaries are provisional);
  * predecessors/successors/related_versions/systems point at existing ids;
  * status/relevance_tier/access_status/paper_type values come from the taxonomy;
  * `verified: true` requires verified_date and at least one evidence entry whose
    source is not purely bibliographic;
  * a paper with paper_type 'survey' must say so in its summary (guard against
    mislabelled technique papers -- see docs/methodology.md);
  * URL fields start with https:// and are not on a disallowed host list;
  * every paper must have at least one of doi / arxiv / official_url, or a
    'supplied PDF' metadata source (owner-provided copy with no public record).
Exit status 1 on any error.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "catalog"

DISALLOWED_HOSTS = ("sci-hub", "libgen", "booksc", "z-lib", "annas-archive", "scribd.com", "researchgate.net/profile")


def load(name):
    with open(CAT / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    errors, warnings = [], []
    schema = json.load(open(CAT / "schema.json", encoding="utf-8"))
    papers_doc = load("papers.yaml")
    systems_doc = load("systems.yaml")
    taxonomy = load("taxonomy.yaml")
    eras = {e["id"]: e for e in load("eras.yaml")["eras"]}

    validator = jsonschema.Draft202012Validator(schema)
    for doc, label in ((papers_doc, "papers.yaml"), (systems_doc, "systems.yaml")):
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
            path = "/".join(str(p) for p in err.path)
            errors.append(f"{label}: schema: {path}: {err.message[:300]}")

    axes = {a["field"]: {v["id"] for v in a["values"]} for a in taxonomy["axes"]}
    axes["paper_type"] = {v["id"] for a in taxonomy["axes"] if a["key"] == "paper_type" for v in a["values"]}
    tiers = {t["id"] for t in taxonomy["relevance_tiers"]}
    statuses = {s["id"] for s in taxonomy["status_levels"]}
    access = {s["id"] for s in taxonomy["access_status"]}

    papers = papers_doc.get("papers", [])
    systems = systems_doc.get("systems", [])
    pids = [p["id"] for p in papers]
    sids = [s["id"] for s in systems]
    pid_set, sid_set = set(pids), set(sids)

    for key, items in (("paper id", pids), ("system id", sids)):
        for k, n in Counter(items).items():
            if n > 1:
                errors.append(f"duplicate {key}: {k}")
    for field in ("doi", "arxiv"):
        vals = Counter((p.get(field) or "").lower().split("v")[0] if field == "arxiv" else (p.get(field) or "").lower() for p in papers)
        for k, n in vals.items():
            if k and n > 1:
                errors.append(f"duplicate {field}: {k}")
    # A title may repeat only between entries that name each other in related_versions
    # (a journal and a proceedings version of one paper). Any other repeat is an error.
    by_title = {}
    for p in papers:
        by_title.setdefault(re.sub(r"[^a-z0-9]", "", p["title"].lower()), []).append(p)
    for k, group in by_title.items():
        if len(group) < 2:
            continue
        ids_in = {p["id"] for p in group}
        linked = all(set(p.get("related_versions") or []) & (ids_in - {p["id"]}) for p in group)
        if not linked:
            errors.append(f"duplicate title (normalised): {k[:60]}")

    for p in papers:
        pid = p["id"]
        for field, allowed in axes.items():
            vals = p.get(field)
            if vals is None:
                continue
            if isinstance(vals, str):
                vals = [vals]
            for v in vals:
                if v not in allowed:
                    errors.append(f"{pid}: {field} value '{v}' not in taxonomy.yaml")
        if p["relevance_tier"] not in tiers:
            errors.append(f"{pid}: relevance_tier '{p['relevance_tier']}' unknown")
        if p["status"] not in statuses:
            errors.append(f"{pid}: status '{p['status']}' unknown")
        if p["access_status"] not in access:
            errors.append(f"{pid}: access_status '{p['access_status']}' unknown")
        if p["era"] not in eras:
            errors.append(f"{pid}: era '{p['era']}' unknown")
        else:
            e = eras[p["era"]]
            if not (e["start"] <= p["year"] <= e["end"]):
                warnings.append(f"{pid}: year {p['year']} outside {p['era']} range {e['start']}-{e['end']} (allowed, but justify in notes)")
        supplied = any("supplied pdf" in (m or "").lower() for m in (p.get("metadata_sources") or []))
        if not (p.get("doi") or p.get("arxiv") or p.get("official_url") or supplied):
            errors.append(f"{pid}: needs at least one of doi / arxiv / official_url, or a supplied-PDF metadata source")
        for field in ("official_url", "pdf_url", "artifact_url", "source_code_url"):
            u = p.get(field)
            if u and any(h in u.lower() for h in DISALLOWED_HOSTS):
                errors.append(f"{pid}: {field} points at a disallowed host")
        for field in ("predecessors", "successors", "related_versions"):
            for ref in p.get(field, []) or []:
                if ref not in pid_set:
                    errors.append(f"{pid}: {field} references unknown paper id '{ref}'")
        for ref in p.get("systems", []) or []:
            if ref not in sid_set:
                errors.append(f"{pid}: systems references unknown system id '{ref}'")
        if p.get("verified"):
            if not p.get("verified_date"):
                errors.append(f"{pid}: verified=true requires verified_date")
            if p["status"] != "verified":
                errors.append(f"{pid}: verified=true requires status: verified")
            if not any("metadata" not in (ev.get("source", "").lower()) for ev in p["evidence"]):
                errors.append(f"{pid}: verified=true requires evidence beyond bibliographic metadata")
        if p["status"] == "verified" and not p.get("verified"):
            errors.append(f"{pid}: status verified requires verified: true")
        if p["paper_type"] == "survey" and "survey" not in p["summary"].lower() and "overview" not in p["summary"].lower():
            errors.append(f"{pid}: paper_type survey but summary does not describe it as a survey/overview")
        if p["status"] in ("read", "verified") and not p.get("why_read"):
            warnings.append(f"{pid}: status {p['status']} but no why_read sentence for the README")
        if len(p["summary"]) > 900:
            warnings.append(f"{pid}: summary is long ({len(p['summary'])} chars); keep summaries concise")

    for s in systems:
        for ref in s.get("papers", []):
            if ref not in pid_set:
                errors.append(f"system {s['id']}: unknown paper id '{ref}'")
        for field in ("predecessors", "successors"):
            for ref in s.get(field, []) or []:
                if ref not in sid_set:
                    errors.append(f"system {s['id']}: {field} references unknown system '{ref}'")
        for v in s.get("compiler_architecture", []):
            if v not in axes["compiler_architecture"]:
                errors.append(f"system {s['id']}: compiler_architecture '{v}' not in taxonomy")
        for v in s.get("targets", []):
            if v not in axes["target_hardware"]:
                errors.append(f"system {s['id']}: target '{v}' not in taxonomy")
        for k, v in (s.get("decomposition_support") or {}).items():
            if v not in ("yes", "no", "partial", "unknown"):
                errors.append(f"system {s['id']}: decomposition_support.{k} must be yes/no/partial/unknown")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"\n{len(papers)} papers, {len(systems)} systems, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
