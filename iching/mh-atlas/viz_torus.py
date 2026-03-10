#!/usr/bin/env python3
"""
Torus visualization for meihua atlas.
Z5 x Z5 grid showing population, well-definedness, relations, and a sample reading trajectory.
"""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

HERE = Path(__file__).resolve().parent
CJK = FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
CJK_B = FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc")

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
E_ZH = {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}
E_IDX = {e: i for i, e in enumerate(ELEMENTS)}

REL_ZH = {
    (0,): "比和",
    (1,): "生体",
    (4,): "体生用",
    (2,): "克体",
    (3,): "体克用",
}


def load_data():
    with open(HERE / "mh_torus_flow.json") as f:
        flow = json.load(f)
    with open(HERE / "mh_states.json") as f:
        states = json.load(f)
    return flow, states


def cjk(ax, x, y, text, fontsize=9, ha="center", va="center", color="black",
         bold=False, **kw):
    """Place CJK text."""
    fp = CJK_B if bold else CJK
    fp_copy = fp.copy()
    fp_copy.set_size(fontsize)
    ax.text(x, y, text, ha=ha, va=va, color=color, fontproperties=fp_copy, **kw)


def label_axes(ax, xlabel, ylabel):
    """Label axes with CJK font."""
    fp = CJK.copy()
    fp.set_size(10)
    ax.set_xlabel(xlabel, fontproperties=fp)
    ax.set_ylabel(ylabel, fontproperties=fp)


def set_element_ticks(ax):
    """Set element ticks with CJK labels."""
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    fp = CJK.copy()
    fp.set_size(9)
    ax.set_xticklabels([E_ZH[e] for e in ELEMENTS], fontproperties=fp)
    ax.set_yticklabels([E_ZH[e] for e in ELEMENTS], fontproperties=fp)


def plot_population_heatmap(flow, ax):
    """5x5 heatmap of cell populations."""
    grid = np.zeros((5, 5))
    for key, data in flow.items():
        ti, yong = data["cell"]
        grid[E_IDX[ti]][E_IDX[yong]] = data["population"]

    ax.imshow(grid, cmap="YlOrRd", interpolation="nearest", vmin=0, vmax=26)
    set_element_ticks(ax)
    label_axes(ax, "用", "体")
    cjk(ax, 2, -1.0, "体用分布 (384態)", fontsize=11, bold=True)

    for i in range(5):
        for j in range(5):
            v = int(grid[i][j])
            color = "white" if v > 15 else "black"
            ax.text(j, i, str(v), ha="center", va="center", fontsize=12,
                    fontweight="bold", color=color)

    # Mark bihe diagonal
    for i in range(5):
        rect = mpatches.Rectangle((i - 0.5, i - 0.5), 1, 1,
                                   linewidth=2.5, edgecolor="gold", facecolor="none")
        ax.add_patch(rect)


def plot_well_defined(flow, ax):
    """5x5 grid: well-defined vs turbulent cells for hu."""
    grid = np.zeros((5, 5))
    for key, data in flow.items():
        ti, yong = data["cell"]
        grid[E_IDX[ti]][E_IDX[yong]] = 1 if data["well_defined"] else 0

    colors = ["#e74c3c", "#2ecc71"]
    cmap = LinearSegmentedColormap.from_list("wd", colors, N=2)
    ax.imshow(grid, cmap=cmap, interpolation="nearest", vmin=0, vmax=1)
    set_element_ticks(ax)
    label_axes(ax, "用", "体")
    cjk(ax, 2, -1.0, "互 定義域", fontsize=11, bold=True)

    for key, data in flow.items():
        ti, yong = data["cell"]
        i, j = E_IDX[ti], E_IDX[yong]
        n_targets = data["hu_target_count"]
        sym = "✓" if data["well_defined"] else "✗"
        color = "black" if data["well_defined"] else "white"
        ax.text(j, i, f"{sym}\n{n_targets}", ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)


def plot_relations(ax):
    """5x5 grid colored by Z5 relation type."""
    grid = np.ones((5, 5)) * 0.97
    ax.imshow(grid, cmap="Greys", interpolation="nearest", vmin=0, vmax=1)
    set_element_ticks(ax)
    label_axes(ax, "用", "体")
    cjk(ax, 2, -1.0, "Z₅ 生克関係", fontsize=11, bold=True)

    rel_colors = {
        0: ("#dddddd", "比和"),
        1: ("#d5f5e3", "生体"),
        4: ("#fdebd0", "体生用"),
        2: ("#fadbd8", "克体"),
        3: ("#d6eaf8", "体克用"),
    }

    for i in range(5):
        for j in range(5):
            diff = (j - i) % 5
            color, label = rel_colors[diff]
            rect = mpatches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                       facecolor=color, edgecolor="#aaaaaa", linewidth=0.5)
            ax.add_patch(rect)
            cjk(ax, j, i, label, fontsize=8, bold=True)

    # Legend
    handles = [mpatches.Patch(facecolor=c, label=f"{l} ({'+' if d in (1,3) else ''}{[0,2,-1,-2,1][d]})",
               edgecolor="gray")
               for d, (c, l) in rel_colors.items()]
    ax.legend(handles=handles, loc="upper left", fontsize=7,
              bbox_to_anchor=(-0.02, 1.0), framealpha=0.9, prop=CJK.copy())


def plot_reading(ax):
    """Guanmei zhan trajectory on the torus."""
    grid = np.ones((5, 5)) * 0.95
    ax.imshow(grid, cmap="Greys", interpolation="nearest", vmin=0, vmax=1)
    set_element_ticks(ax)
    label_axes(ax, "用", "体")
    cjk(ax, 2, -1.0, "觀梅占 軌跡 (rescued arc)", fontsize=11, bold=True)

    for i in range(6):
        ax.axhline(i - 0.5, color="#cccccc", linewidth=0.5)
        ax.axvline(i - 0.5, color="#cccccc", linewidth=0.5)

    # Light cell labels
    for i in range(5):
        for j in range(5):
            cjk(ax, j, i, f"{E_ZH[ELEMENTS[i]]},{E_ZH[ELEMENTS[j]]}",
                fontsize=7, color="#cccccc")

    # Trajectory points: (row=ti_idx, col=yong_idx, label, color, valence)
    # Ti=Metal(3), the entire trajectory stays on row 3
    points = [
        (3, 1, "本卦\n克体", "#e74c3c"),     # Metal,Fire → ke ti
        (3, 3, "体互\n比和", "#888888"),       # Metal,Metal → bihe
        (3, 0, "用互\n体克用", "#3498db"),     # Metal,Wood → ti ke yong
        (3, 2, "変卦\n生体", "#2ecc71"),       # Metal,Earth → sheng ti
    ]

    # Arrows: ben→tihu, ben→yonghu, tihu→bian, yonghu→bian
    arrows = [(0, 1), (0, 2), (1, 3), (2, 3)]
    for src, dst in arrows:
        sy, sx = points[src][0], points[src][1]
        dy, dx = points[dst][0], points[dst][1]
        rad = 0.2 if src == 0 else -0.15
        ax.annotate("", xy=(dx, dy), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.8,
                                   connectionstyle=f"arc3,rad={rad}"))

    for i, (y, x, label, color) in enumerate(points):
        size = 700 if i in (0, 3) else 450
        ax.scatter(x, y, s=size, c=color, zorder=5, edgecolors="black", linewidth=1.5)
        offset_y = 0.42 if i % 2 == 0 else -0.42
        cjk(ax, x, y + offset_y, label, fontsize=8, bold=True, color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor=color, alpha=0.9))

    # Valence narrative
    cjk(ax, 2, 4.6, "弧: -2 → 0/+1 → +2  (rescued)", fontsize=9, color="#333333")


def main():
    flow, states = load_data()

    fig, axes = plt.subplots(2, 2, figsize=(14, 13))
    fig.text(0.5, 0.98, "Meihua Torus  Z₅ × Z₅  —  384 Reading States",
             ha="center", fontsize=14, fontweight="bold", fontproperties=CJK_B.copy())

    plot_population_heatmap(flow, axes[0, 0])
    plot_well_defined(flow, axes[0, 1])
    plot_relations(axes[1, 0])
    plot_reading(axes[1, 1])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out = HERE / "torus_visualization.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close()


if __name__ == "__main__":
    main()
