#!/usr/bin/env python3
"""Figure 3: taxonomy as orthogonal axes (not a tree).

Reads catalog/taxonomy.yaml so the figure cannot drift from the catalog.
Only the six axes used in the paper's taxonomy figure are drawn; the others
are listed in the tables.
"""
import textwrap

import graphviz

from _common import render_graph, taxonomy

AXES = ["programming_abstraction", "data_decomposition", "computation_mapping",
        "communication_synthesis", "compilation_time", "target_memory_model"]
SHORT = {"programming_abstraction": "B. Source abstraction", "data_decomposition": "C. Data decomposition",
         "computation_mapping": "D. Computation mapping", "communication_synthesis": "E. Communication synthesis",
         "compilation_time": "F. Compiler / runtime boundary", "target_memory_model": "A. Target"}

tax = {a["key"]: a for a in taxonomy()["axes"]}
g = graphviz.Digraph("taxonomy", graph_attr={"rankdir": "TB", "nodesep": "0.25", "ranksep": "0.35",
                                             "fontname": "Helvetica", "bgcolor": "white"})
g.attr("node", shape="plaintext", fontname="Helvetica", fontsize="8")

g.node("center", '<<table border="0" cellborder="1" cellspacing="0" cellpadding="6"><tr><td bgcolor="#dfe9df"><b>A paper or system</b><br/>is placed on <i>every</i> axis</td></tr></table>>')
TOP, BOTTOM = AXES[:3], AXES[3:]
for key in AXES:
    rows = "".join(f'<tr><td align="left">{textwrap.shorten(v["name"], 30)}</td></tr>' for v in tax[key]["values"])
    label = f'<<table border="0" cellborder="1" cellspacing="0" cellpadding="2"><tr><td bgcolor="#e3ecf7"><b>{SHORT[key]}</b></td></tr>{rows}</table>>'
    g.node(key, label)
with g.subgraph() as s_top:
    s_top.attr(rank="same")
    for key in TOP:
        s_top.node(key)
with g.subgraph() as s_bot:
    s_bot.attr(rank="same")
    for key in BOTTOM:
        s_bot.node(key)
for key in TOP:
    g.edge(key, "center", color="#4a5a7a", arrowhead="none")
for key in BOTTOM:
    g.edge("center", key, color="#4a5a7a", arrowhead="none")

render_graph(g, "taxonomy")
