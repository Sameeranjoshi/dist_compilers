#!/usr/bin/env python3
"""Figure 4: data-decomposition taxonomy, drawn as small example grids.

Each panel shows a 1-D or 2-D array of elements coloured by owning place.
Panels are grouped as in the taxonomy: rectilinear, structured non-rectilinear,
irregular.  No data from the catalog is needed; the figure illustrates axis C.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from _common import save_fig  # noqa: E402

PAL = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#b07aa1", "#76b7b2"]
N = 8  # elements per side


def grid(ax, owner, title, hatch=None, ghost=None, subtile=False):
    """owner: NxN int array of place ids (-1 = empty); ghost: NxN bool for ghost cells."""
    n = owner.shape[0]
    for i in range(n):
        for j in range(n):
            o = owner[i, j]
            if o < 0:
                continue
            face = PAL[o % len(PAL)]
            alpha = 0.35 if (ghost is not None and ghost[i, j]) else 0.9
            if subtile and ((i // 2) + (j // 2)) % 2:
                alpha = 0.55
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, facecolor=face, alpha=alpha,
                                   edgecolor="white", linewidth=0.8,
                                   hatch="///" if (ghost is not None and ghost[i, j]) else None))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor("#888")
    ax.set_title(title, fontsize=7, pad=2)


def rect_block_1d():
    return np.repeat(np.arange(4), 2)[None, :].repeat(N, 0)


def rect_block_2d():
    o = np.zeros((N, N), int)
    o[N // 2:, :] += 2
    o[:, N // 2:] += 1
    return o


def uneven_block():
    bounds = [0, 1, 4, 5, 8]
    o = np.zeros((N, N), int)
    for k in range(4):
        o[:, bounds[k]:bounds[k + 1]] = k
    return o


def tiled():
    o = np.zeros((N, N), int)
    for i in range(N):
        for j in range(N):
            o[i, j] = ((i // 4) * 2 + (j // 4))  # node level
    return o


def replicated():
    return np.zeros((N, N), int)


def halo():
    o = rect_block_2d()
    ghost = np.zeros((N, N), bool)
    # mark the cells adjacent to the block boundary of place 0 as ghosts it holds
    g = np.full((N, N), -1)
    g[:N // 2 + 1, :N // 2 + 1] = 0
    ghost[N // 2, :N // 2 + 1] = True
    ghost[:N // 2 + 1, N // 2] = True
    return g, ghost


def cyclic():
    return (np.arange(N) % 4)[None, :].repeat(N, 0)


def block_cyclic():
    return ((np.arange(N) // 2) % 2 + 2 * ((np.arange(N) // 4) % 2))[None, :].repeat(N, 0) % 4


def skewed():
    o = np.zeros((N, N), int)
    for i in range(N):
        for j in range(N):
            o[i, j] = ((i + j) // 4) % 4
    return o


def graph_partition():
    rng = np.random.default_rng(3)
    o = np.zeros((N, N), int)
    seeds = [(1, 1), (6, 2), (2, 6), (6, 6)]
    for i in range(N):
        for j in range(N):
            d = [abs(i - a) + abs(j - b) + rng.integers(0, 2) for a, b in seeds]
            o[i, j] = int(np.argmin(d))
    return o


def mapping_array():
    rng = np.random.default_rng(7)
    return rng.integers(0, 4, size=(N, N))


def owned_ghost():
    o, ghost = graph_partition(), np.zeros((N, N), bool)
    g = np.full((N, N), -1)
    for i in range(N):
        for j in range(N):
            if o[i, j] == 0:
                g[i, j] = 0
    for i in range(N):
        for j in range(N):
            if g[i, j] == 0:
                for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if 0 <= a < N and 0 <= b < N and o[a, b] != 0:
                        g[a, b] = o[a, b]
                        ghost[a, b] = True
    return g, ghost


def import_export(ax):
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor("#888")
    ax.add_patch(Rectangle((0.4, 1.2), 3, 5.6, facecolor=PAL[0], alpha=0.25, edgecolor=PAL[0]))
    ax.add_patch(Rectangle((4.6, 1.2), 3, 5.6, facecolor=PAL[1], alpha=0.25, edgecolor=PAL[1]))
    ax.text(1.9, 7.1, "place P", ha="center", fontsize=6.5)
    ax.text(6.1, 7.1, "place Q", ha="center", fontsize=6.5)
    for k, y in enumerate((5.6, 4.4, 3.2)):
        ax.annotate("", xy=(4.6, y), xytext=(3.4, y), arrowprops=dict(arrowstyle="->", color="#333", lw=0.8))
    ax.text(4.0, 0.35, "export(P) = import(Q)", ha="center", fontsize=6)
    ax.text(1.9, 2.0, "owned", ha="center", fontsize=6.5)
    ax.text(6.1, 2.0, "needed", ha="center", fontsize=6.5)
    ax.set_title("import/export\nschedule", fontsize=7, pad=2)


fig, axes = plt.subplots(3, 5, figsize=(7.0, 5.4))
fig.subplots_adjust(hspace=0.75, wspace=0.3, left=0.04, right=0.99, top=0.9, bottom=0.02)
for ax in axes.ravel():
    ax.axis("off")

row = axes[0]
for ax in row:
    ax.axis("on")
grid(row[0], rect_block_1d(), "1-D block")
grid(row[1], rect_block_2d(), "2-D block")
grid(row[2], uneven_block(), "uneven block")
grid(row[3], tiled(), "tiled /\nhierarchical", subtile=True)
grid(row[4], replicated(), "replicated")

row = axes[1]
for ax in row[:4]:
    ax.axis("on")
h, hg = halo()
grid(row[0], h, "halo / overlap\n(owned by place 0)", ghost=hg)
grid(row[1], cyclic(), "cyclic")
grid(row[2], block_cyclic(), "block-cyclic")
grid(row[3], skewed(), "affine / skewed\nowner map")

row = axes[2]
for ax in row[:4]:
    ax.axis("on")
grid(row[0], graph_partition(), "graph / mesh\npartition")
grid(row[1], mapping_array(), "mapping array\n(INDIRECT)")
og, ogg = owned_ghost()
grid(row[2], og, "owned + ghost sets\n(place 0)", ghost=ogg)
import_export(row[3])

for r, label in enumerate(("A. Rectilinear", "B. Structured, non-rectilinear (and halo)", "C. Irregular")):
    top = axes[r, 0].get_position().y1
    fig.text(0.04, top + 0.075, label, fontsize=8.5, weight="bold", va="bottom")
save_fig(fig, "decomposition-taxonomy")
