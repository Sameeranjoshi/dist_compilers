#!/usr/bin/env python3
"""Figure 5: historical rediscovery map.

Pairs an older concept (left) with its modern descendant (right).  Each edge is
annotated with the catalog ids that document the older and newer form; the
*pairing itself* is a survey hypothesis (see docs/historical-claims.md), not a
claim that the newer system cites the older one.
"""
import graphviz

from _common import render_graph

PAIRS = [
    ("Processor grid\n(HPF PROCESSORS)", "Device mesh\n(Mesh-TensorFlow, GSPMD, Shardy)", "loveman1993hpf", "xu2021gspmd"),
    ("ALIGN / DISTRIBUTE\n(Fortran D, HPF)", "Tensor sharding annotations\n(GSPMD, PartIR, MLIR shard)", "hiranandani1992compiling", "alabed2025partir"),
    ("Owner-computes rule\n(Kali, Fortran D)", "SPMD partition propagation\n(GSPMD, Shardy)", "koelbel1991compiling", "xu2021gspmd"),
    ("Communication-set generation\n(Koelbel; Chatterjee et al.)", "Collective insertion\n(XLA SPMD, PartIR)", "chatterjee1993generating", "alabed2025partir"),
    ("Array redistribution\n(HPF REDISTRIBUTE, PARADIGM)", "Resharding\n(GSPMD, Alpa cross-mesh)", "ramaswamy1996redistribution", "zheng2022alpa"),
    ("Inspector-executor\n(PARTI, CHAOS)", "Dynamic sparse communication planning\n(SpDISTAL, MLIR sparse distribution)", "saltz1991runtime", "yadav2022spdistal"),
    ("Global arrays\n(SUPERB, Vienna Fortran)", "Distributed tensor values\n(DISTAL, Legion/Regent regions)", "zima1988superb", "yadav2022distal"),
    ("PARTI import/export schedules", "Sparse tensor slice exchange\n(SpDISTAL)", "das1994communication", "yadav2022spdistal"),
    ("Hierarchical machine mappings\n(Sequoia, PARADIGM)", "Inter-/intra-operator parallelism\n(Alpa)", "fatahalian2006sequoia", "zheng2022alpa"),
]

g = graphviz.Digraph("rediscovery", graph_attr={
    "rankdir": "LR", "nodesep": "0.18", "ranksep": "1.4", "fontname": "Helvetica", "bgcolor": "white", "splines": "true"})
g.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="10", penwidth="1.0", margin="0.12,0.06")
g.attr("edge", fontname="Helvetica", fontsize="8", color="#4a5a7a", arrowsize="0.6")

with g.subgraph(name="cluster_old") as c:
    c.attr(label="1988-2006 concept", style="rounded,dashed", color="#8a94a8", fontname="Helvetica", fontsize="11")
    for i, (old, _, _, _) in enumerate(PAIRS):
        c.node(f"o{i}", old, fillcolor="#fbf1dc", color="#b08a3a")
with g.subgraph(name="cluster_new") as c:
    c.attr(label="2018-2025 descendant", style="rounded,dashed", color="#8a94a8", fontname="Helvetica", fontsize="11")
    for i, (_, new, _, _) in enumerate(PAIRS):
        c.node(f"n{i}", new, fillcolor="#e3ecf7", color="#4a5a7a")
for i, (_, _, a, b) in enumerate(PAIRS):
    g.edge(f"o{i}", f"n{i}", label=f"{a} -> {b}")

render_graph(g, "rediscovery-map")
