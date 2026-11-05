#!/usr/bin/env python3
"""Regenerate the generated blocks of README.md from the catalog.

README.md contains hand-written prose plus blocks delimited by
  <!-- BEGIN:<name> -->  ...  <!-- END:<name> -->
Everything between the markers is replaced; everything else is kept.
Blocks: status, start-here, categories, eras, techniques, systems-table.
"""
import re
from collections import Counter, defaultdict

from _common import ROOT, eras, paper_link, papers, short_authors, systems, taxonomy

README = ROOT / "README.md"

CATEGORY_ORDER = [
    ("foundations", "Foundations (pre-1980 compiler, dependence, vector/array/dataflow machines)"),
    ("global-arrays", "Global arrays and pre-HPF systems"),
    ("fortran-d-hpf", "Fortran D / HPF"),
    ("mpi-generated", "MPI and generated message passing"),
    ("irregular", "Irregular computation / inspector-executor"),
    ("pgas-languages", "PGAS and language systems"),
    ("polyhedral", "Polyhedral and affine distributed compilation"),
    ("task-region", "Task / region compiler systems"),
    ("ml-compilers", "Multi-GPU and ML compilers"),
    ("spatial-wafer", "Spatial / wafer-scale compilers"),
    ("performance-models", "Performance and cost modeling"),
    ("surveys", "Surveys and taxonomies"),
]
TECHNIQUE_ORDER = [
    ("data-distribution", "Data distribution"),
    ("owner-computes", "Owner-computes"),
    ("communication-generation", "Communication generation"),
    ("redistribution", "Redistribution / resharding"),
    ("irregular-ownership", "Irregular ownership"),
    ("automatic-mpi", "Automatic MPI / message-passing generation"),
    ("mesh-sharding", "Mesh / tensor sharding"),
    ("compiler-runtime-codesign", "Compiler/runtime co-design"),
]
START_HERE_GROUPS = [
    (1, 2, "Foundational map"), (3, 5, "Global arrays and owner-computes"), (6, 8, "Automatic distribution"),
    (9, 9, "Irregular computation"), (10, 11, "MPI generation"), (12, 16, "Modern distributed tensors"),
]


def entry(p, reason=True):
    link = paper_link(p)
    title = f"[{p['title']}]({link})" if link else p["title"]
    tags = " ".join(f"`{t}`" for t in (p.get("taxonomy_tags") or [])[:5])
    status = "" if p["verified"] else " *(metadata-verified; summary pending full read)*" if p["status"] in ("discovered", "screened") else ""
    why = p.get("why_read") or p["summary"]
    line = f"- **{short_authors(p)} ({p['year']})** — {title} — *{p['paper_type']}*.{status}"
    if reason:
        line += f"  \n  {why}"
    if tags:
        line += f"  \n  {tags}"
    return line


def block_status(P, S):
    c = Counter(p["status"] for p in P)
    v = sum(1 for p in P if p["verified"])
    tiers = Counter(p["relevance_tier"] for p in P)
    lines = [f"| papers in catalog | {len(P)} |", f"| systems | {len(S)} |",
             f"| metadata-verified against Crossref/arXiv | {sum(1 for p in P if 'crossref' in ' '.join(p.get('metadata_sources') or []).lower() or 'arxiv' in ' '.join(p.get('metadata_sources') or []).lower())} |",
             f"| status `verified` (primary source read) | {v} |",
             f"| status `read` | {c.get('read', 0)} |", f"| status `screened` / `discovered` | {c.get('screened', 0) + c.get('discovered', 0)} |",
             f"| tier core / bridge / foundation / adjacent | {tiers.get('core', 0)} / {tiers.get('bridge', 0)} / {tiers.get('foundation', 0)} / {tiers.get('adjacent', 0)} |",
             f"| paper cards | {len(list((ROOT / 'notes' / 'paper-cards').glob('*.md')) ) - 1} |"]
    return "| metric | value |\n|---|---|\n" + "\n".join(lines)


def block_start_here(P):
    sh = sorted([p for p in P if p.get("start_here")], key=lambda p: p["start_here"])
    out = []
    for lo, hi, name in START_HERE_GROUPS:
        items = [p for p in sh if lo <= p["start_here"] <= hi]
        if not items:
            continue
        out.append(f"**{name}**\n")
        for p in items:
            link = paper_link(p)
            out.append(f"{p['start_here']}. [{p['title']}]({link}) — {short_authors(p)}, {p['year']}.  \n   *Learn:* {p.get('why_read') or p['summary']}")
        out.append("")
    return "\n".join(out)


def block_categories(P):
    out = []
    for key, name in CATEGORY_ORDER:
        items = sorted([p for p in P if key in (p.get("readme_categories") or [])], key=lambda p: p["year"])
        out.append(f"### {name}\n")
        if not items:
            out.append("_No verified entries yet — see ROADMAP.md._\n")
            continue
        out += [entry(p) for p in items]
        out.append("")
    return "\n".join(out)


def block_eras(P, E):
    out = []
    for i, e in enumerate(E):
        items = sorted([p for p in P if p["era"] == e["id"]], key=lambda p: (p["year"], p["id"]))
        out.append(f"### Era {i}: {e['name']} ({e['start']}–{e['end']})\n")
        out.append(f"*Machine driver:* {e['machine_driver']}.  \n*Limitation that motivated the next era:* {e['limitation']}.\n")
        out += [entry(p, reason=False) for p in items] or ["_No entries yet._"]
        out.append("")
    return "\n".join(out)


def block_techniques(P):
    out = []
    for key, name in TECHNIQUE_ORDER:
        items = sorted([p for p in P if key in (p.get("technique_lists") or [])], key=lambda p: p["year"])
        out.append(f"### {name}\n")
        out += [entry(p, reason=False) for p in items] or ["_No entries yet._"]
        out.append("")
    return "\n".join(out)


def block_systems(S, P):
    pm = {p["id"]: p for p in P}
    cols = ["System", "Years", "Input", "Distribution", "Work mapping", "Communication", "Runtime", "Targets", "Artifact", "Papers"]
    rows = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for s in sorted(S, key=lambda s: s["active_years"]):
        b = s.get("table_b") or {}
        refs = ", ".join(f"[{pm[i]['year']}]({paper_link(pm[i])})" for i in s["papers"] if i in pm and paper_link(pm[i]))
        rows.append("| " + " | ".join(str(x).replace("|", "/") for x in [
            s["name"], s["active_years"], b.get("input", "?"), b.get("distribution", "?"), b.get("work_mapping", "?"),
            b.get("communication", "?"), b.get("runtime", s["runtime"]), b.get("targets", ", ".join(s["targets"])),
            b.get("artifact", s["open_source_status"]), refs]) + " |")
    return "\n".join(rows) + "\n\n`?` = not yet filled from a primary source."


def replace_block(text, name, body):
    pat = re.compile(rf"(<!-- BEGIN:{name} -->\n).*?(<!-- END:{name} -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"README.md lacks block {name}")
    return pat.sub(lambda m: m.group(1) + body.rstrip() + "\n" + m.group(2), text)


def main():
    P, S, E = papers(), systems(), eras()
    text = README.read_text(encoding="utf-8")
    for name, body in (("status", block_status(P, S)), ("start-here", block_start_here(P)), ("categories", block_categories(P)),
                       ("eras", block_eras(P, E)), ("techniques", block_techniques(P)), ("systems-table", block_systems(S, P))):
        text = replace_block(text, name, body)
    README.write_text(text, encoding="utf-8")
    print("README.md regenerated")


if __name__ == "__main__":
    main()
