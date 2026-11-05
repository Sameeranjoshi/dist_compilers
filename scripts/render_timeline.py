#!/usr/bin/env python3
"""Figure 1: historical timeline 1950-2026 with parallel lanes.

Events come from catalog/timeline.yaml (each tied to a catalog paper or a
named source); era bands come from catalog/eras.yaml.  The figure is produced
at two sizes: the README SVG is wide, the LaTeX PDF fits a figure* environment.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

from _common import CATALOG, eras, papers, save_fig  # noqa: E402

LANES = ["hardware", "abstraction", "representation", "distribution", "systems"]
LANE_LABEL = {"hardware": "Hardware", "abstraction": "Programming\nabstraction",
              "representation": "Compiler\nrepresentation", "distribution": "Distribution\nmechanism",
              "systems": "Representative\nsystems / papers"}
ERA_COLORS = ["#f2f2f2", "#e8eef7", "#f2f2f2", "#e8eef7", "#f2f2f2", "#e8eef7", "#f2f2f2"]

events = yaml.safe_load(open(CATALOG / "timeline.yaml", encoding="utf-8"))["events"]
pids = {p["id"] for p in papers()}
for e in events:
    if e.get("paper") and e["paper"] not in pids:
        raise SystemExit(f"timeline.yaml: unknown paper id {e['paper']}")


def draw(width, height, fontsize):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(1950, 2027)
    ax.set_ylim(-0.75, len(LANES) - 0.25)
    ax.set_yticks(range(len(LANES)))
    ax.set_yticklabels([LANE_LABEL[l] for l in LANES], fontsize=fontsize)
    ax.invert_yaxis()
    ax.set_xticks(range(1950, 2030, 10))
    ax.tick_params(axis="x", labelsize=fontsize)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    for i, e in enumerate(eras()):
        ax.axvspan(e["start"], e["end"] + 1, color=ERA_COLORS[i % len(ERA_COLORS)], lw=0, zorder=0)
        ax.text((e["start"] + e["end"] + 1) / 2, len(LANES) - 0.45, f"Era {i}", ha="center", va="top",
                fontsize=fontsize - 1, color="#555", style="italic")
    for y in range(len(LANES)):
        ax.axhline(y, color="#bbb", lw=0.6, zorder=1)
    # stagger labels within a lane on four levels (above near, below near, above far, below far)
    offsets = [(0, 9, "bottom"), (0, -9, "top"), (0, 20, "bottom"), (0, -20, "top")]
    counter = {l: 0 for l in LANES}
    last_x = {l: -1e9 for l in LANES}
    for ev in sorted(events, key=lambda e: e["year"]):
        lane = LANES.index(ev["lane"])
        x = ev["year"]
        if x - last_x[ev["lane"]] > 14:
            counter[ev["lane"]] = 0
        dx, dy, va = offsets[counter[ev["lane"]] % 4]
        counter[ev["lane"]] += 1
        last_x[ev["lane"]] = x
        call = ev.get("callout")
        ax.plot(x, lane, marker="D" if call else "o", ms=5 if call else 3.5,
                color="#c0392b" if call else "#4a5a7a", zorder=3)
        ax.annotate(ev["label"], (x, lane), xytext=(dx, dy), textcoords="offset points",
                    ha="center", va=va, fontsize=fontsize - 1.5, fontweight="bold" if call else "normal",
                    arrowprops=dict(arrowstyle="-", color="#999", lw=0.4) if abs(dy) > 12 else None,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="#c0392b" if call else "#ccc", lw=0.5, alpha=0.95))
    ax.set_xlabel("year", fontsize=fontsize)
    return fig


save_fig(draw(18, 6.5, 8), "timeline")
fig = draw(7.16, 4.6, 5.0)   # IEEE double-column width
fig.savefig(CATALOG.parent / "paper" / "figures" / "timeline.pdf", bbox_inches="tight", metadata={"CreationDate": None})
print("wrote paper/figures/timeline.pdf (two-column size)")
