#!/usr/bin/env python3
"""Figure 6: citation / influence map.

Edges are taken ONLY from `predecessors` / `successors` fields in
catalog/papers.yaml, which by policy must be stated by the paper itself or by a
cited survey (see docs/taxonomy.md, "Do not tag influence").  If fewer than
MIN_EDGES sourced edges exist the script writes a placeholder figure that says
so, so that the paper never shows an inferred influence graph.
"""
import graphviz

from _common import eras, papers, render_graph, short_authors

MIN_EDGES = 25

ps = {p["id"]: p for p in papers()}
edges = set()
for p in ps.values():
    for q in p.get("predecessors", []) or []:
        if q in ps:
            edges.add((q, p["id"]))
    for q in p.get("successors", []) or []:
        if q in ps:
            edges.add((p["id"], q))

g = graphviz.Digraph("citations", graph_attr={"rankdir": "LR", "fontname": "Helvetica", "bgcolor": "white",
                                              "nodesep": "0.1", "ranksep": "0.6"})
g.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="8", fillcolor="#f4f6fa",
       color="#4a5a7a", margin="0.08,0.04")
g.attr("edge", color="#4a5a7a", arrowsize="0.5")

if len(edges) < MIN_EDGES:
    g.node("placeholder", f"Citation / influence map withheld:\n{len(edges)} sourced edges in the catalog, "
           f"{MIN_EDGES} required.\nEdges are only drawn from predecessor/successor\nrelations stated in the papers themselves.",
           shape="note", fillcolor="#fff8e1")
else:
    era_of = {e["id"]: e for e in eras()}
    nodes = {a for e in edges for a in e}
    by_era = {}
    for n in nodes:
        by_era.setdefault(ps[n]["era"], []).append(n)
    for era, ns in sorted(by_era.items()):
        with g.subgraph(name=f"cluster_{era}") as c:
            c.attr(label=f"{era_of[era]['name']} ({era_of[era]['start']}-{era_of[era]['end']})",
                   style="rounded,dashed", color="#8a94a8", fontsize="9")
            for n in sorted(ns, key=lambda k: ps[k]["year"]):
                c.node(n, f"{short_authors(ps[n])} {ps[n]['year']}")
    for a, b in sorted(edges):
        g.edge(a, b)

render_graph(g, "citation-map")
