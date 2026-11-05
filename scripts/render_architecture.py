#!/usr/bin/env python3
"""Figure 2: the common architecture of a distributed-memory compiler.

Original to this survey (it is analogous in purpose to the common-design figure
of the DL compiler survey by Li et al., but the stages are the ones that recur
across the systems in the catalog: see paper/sections/04-compiler-architecture.tex).
"""
import graphviz

from _common import render_graph

g = graphviz.Digraph("arch", graph_attr={
    "rankdir": "TB", "nodesep": "0.25", "ranksep": "0.35", "fontname": "Helvetica",
    "bgcolor": "white", "pad": "0.1", "dpi": "96"})
g.attr("node", shape="box", style="rounded,filled", fontname="Helvetica", fontsize="11",
       fillcolor="#f4f6fa", color="#4a5a7a", penwidth="1.2", margin="0.15,0.08")
g.attr("edge", color="#4a5a7a", arrowsize="0.7", penwidth="1.1", fontname="Helvetica", fontsize="9")

with g.subgraph(name="cluster_in") as c:
    c.attr(label="Inputs", style="rounded,dashed", color="#8a94a8", fontname="Helvetica", fontsize="11", labeljust="l")
    c.node("src", "Source program\n(sequential code, array language,\nDSL, tensor graph)")
    c.node("mach", "Machine model\n(topology, memory hierarchy,\ndevice mesh)")
    c.node("hint", "Distribution hints\n(ALIGN/DISTRIBUTE, sharding\nannotations, mapper, inferred ownership)")

g.node("ir", "High-level compiler IR\n(dependence graph, polyhedral sets, array statements,\nlogical regions, graph IR, MLIR dialects)", fillcolor="#e3ecf7")
g.node("decomp", "Data decomposition + computation mapping\n(ownership, owner-computes, partition propagation,\niteration/operator/pipeline partitioning)", fillcolor="#e3ecf7")
g.node("comm", "Communication synthesis + redistribution\n(communication sets, collectives, halo exchange,\nimport/export schedules, resharding)", fillcolor="#e3ecf7")
g.node("local", "Local code generation + compiler-integrated runtime\n(global-to-local addressing, inspector-executor,\nschedulers, collective libraries)", fillcolor="#e3ecf7")
g.node("target", "Distributed target\n(multicomputer / MPP, cluster, multi-GPU,\naccelerator mesh, wafer-scale fabric)", fillcolor="#dfe9df")

for s in ("src", "mach", "hint"):
    g.edge(s, "ir")
g.edge("ir", "decomp")
g.edge("decomp", "comm")
g.edge("comm", "local")
g.edge("local", "target")
# feedback loops that distinguish the compiler/runtime boundary (RQ5)
g.edge("local", "decomp", label=" runtime inspection,\n profiling, autotuning", style="dashed", constraint="false")
g.edge("mach", "comm", label=" cost model", style="dashed", constraint="false")

render_graph(g, "compiler-architecture")
