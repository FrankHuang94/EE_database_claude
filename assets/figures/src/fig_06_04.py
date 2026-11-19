#!/usr/bin/env python3
"""Figures for chapter 06-04 (nodal analysis).

Run from anywhere:  python assets/figures/src/fig_06_04.py
Outputs SVGs to assets/figures/06-04/. Schematics use schemdraw; the IR-drop map uses matplotlib.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import save, use_style  # noqa: E402

OUT = "assets/figures/06-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


def sch_two_node(d):
    """Example 06-04.1: 4 A into node 1, 1 A into node 2; R1 = 2 (1-gnd), R2 = 2 (1-2), R3 = 4 (2-gnd)."""
    d += (i1 := elm.SourceI().up().label("4 A"))
    d += elm.Line().right().length(2.0)
    d += (n1 := elm.Dot().label("$v_1$", loc="top"))
    d += elm.Resistor().down().label("$R_1$\n2 Ω", loc="bottom")
    d += (g1 := elm.Dot())
    d += elm.Line().left().tox(i1.start)
    d += elm.Resistor().right().at(n1.center).length(3.5).label("$R_2$ = 2 Ω")
    d += (n2 := elm.Dot().label("$v_2$", loc="top"))
    d += elm.Resistor().down().label("$R_3$\n4 Ω", loc="bottom")
    d += (g2 := elm.Dot())
    d += elm.Line().left().tox(g1.center)
    d += elm.Line().right().at(n2.center).length(2.0)
    d += (i2 := elm.SourceI().down().reverse().label("1 A", loc="bottom"))
    d += elm.Line().left().tox(g2.center)
    d += elm.Ground().at(g1.center)


def sch_supernode(d):
    """Example 06-04.3: 12 V at node 1; 5 V floating, + at node 2, - at node 3."""
    d += (vs := elm.SourceV().up().length(4).label("12 V"))
    d += elm.Line().right().length(2.0)
    d += (n1 := elm.Dot().label("1", loc="bottom"))
    d += elm.Resistor().right().length(3.5).label("2 Ω")
    d += (n2 := elm.Dot().label("2", loc="top"))
    d += (r4 := elm.Resistor().down().length(4).label("4 Ω", loc="bottom"))
    # floating 5 V source, + at node 2 (left), - at node 3 (right)
    # (a plain source circle with + and - drawn upright; SourceV would rotate its minus sign)
    d += (v5 := elm.Source().at((n2.center[0] + 4.0, n2.center[1])).left().length(4.0)
          .label("5 V", loc="bottom"))
    cx, cy = n2.center[0] + 2.0, n2.center[1]
    d += elm.Label().at((cx - 0.22, cy)).label("+", fontsize=14)
    d += elm.Label().at((cx + 0.22, cy)).label("−", fontsize=14)
    d += (n3 := elm.Dot().at(v5.start).label("3", loc="top"))
    d += (r6 := elm.Resistor().down().at(n3.center).length(4).label("6 Ω", loc="bottom"))
    d += elm.Line().at(r6.end).tox(vs.start)
    # 3 Ω from node 1 to node 3 over the top
    d += elm.Line().up().at(n1.center).length(2.0)
    d += elm.Resistor().right().tox(n3.center).label("3 Ω")
    d += elm.Line().down().toy(n3.center)
    d += elm.Ground().at((n1.center[0], vs.start[1]))
    d += elm.EncircleBox([n2, v5, n3], padx=0.6, pady=0.6, includelabels=False).linestyle("--").color("#D55E00")
    d += elm.Label().at((n2.center[0] + 2.0, n2.center[1] - 1.75)).label("supernode", fontsize=11, color="#D55E00")
    del r4


def grid_voltages(n=5, r_edge=0.010, i_load=0.5, vdd=0.80):
    """Solve Example 06-04.5's grid (corners fixed at vdd) and return an n x n array of node voltages."""
    idx = lambda r, c: r * n + c  # noqa: E731
    corners = {idx(0, 0), idx(0, n - 1), idx(n - 1, 0), idx(n - 1, n - 1)}
    unknown = [k for k in range(n * n) if k not in corners]
    pos = {k: i for i, k in enumerate(unknown)}
    G = np.zeros((len(unknown), len(unknown)))
    b = np.full(len(unknown), -i_load)
    g = 1.0 / r_edge
    for r in range(n):
        for c in range(n):
            for rr, cc in ((r, c + 1), (r + 1, c)):
                if rr < n and cc < n:
                    k, m = idx(r, c), idx(rr, cc)
                    for p, q in ((k, m), (m, k)):
                        if p in pos:
                            G[pos[p], pos[p]] += g
                            if q in pos:
                                G[pos[p], pos[q]] -= g
                            else:
                                b[pos[p]] += g * vdd
    v = np.full(n * n, vdd)
    v[unknown] = np.linalg.solve(G, b)
    return v.reshape(n, n)


def fig_ir_drop():
    v = grid_voltages()
    drop = (0.80 - v) * 1e3
    fig, ax = plt.subplots(figsize=(4.8, 4.0))
    im = ax.imshow(drop, cmap="viridis_r", origin="upper")
    for r in range(5):
        for c in range(5):
            ax.text(c, r, f"{drop[r, c]:.1f}", ha="center", va="center", fontsize=8,
                    color="white" if drop[r, c] > 12 else "black")
    for r, c in ((0, 0), (0, 4), (4, 0), (4, 4)):
        ax.add_patch(plt.Rectangle((c - 0.45, r - 0.45), 0.9, 0.9, fill=False, ec="#D55E00", lw=2))
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xlabel("column")
    ax.set_ylabel("row")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.set_label("IR drop below 0.80 V (mV)")
    ax.set_title("5 × 5 grid, 10 mΩ per edge, 0.5 A per node;\nbumps (outlined) at the corners", fontsize=9)
    save(fig, f"{OUT}/ir-drop-map.svg")


if __name__ == "__main__":
    schematic("two-node.svg", sch_two_node)
    schematic("supernode.svg", sch_supernode)
    fig_ir_drop()
    print("06-04 figures written to", OUT)
