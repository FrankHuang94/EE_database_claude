#!/usr/bin/env python3
"""Figures for chapter 06-05 (mesh analysis).

Run from anywhere:  python assets/figures/src/fig_06_05.py
Outputs SVGs to assets/figures/06-05/. Schematics use schemdraw; the nonplanar graph uses matplotlib.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/06-05"
use_style()
B, O = PALETTE[0], PALETTE[1]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


def loop(d, center, label, w=1.6, h=1.6, color=B):
    d += elm.LoopArrow(direction="cw", width=w, height=h).at(center).color(color)
    d += elm.Label().at(center).label(label, fontsize=13, color=color)


def sch_two_mesh(d):
    """Example 06-05.1: 20 V, R1 = 2 (top left), R2 = 4 (shared), R3 = 4 (top right), 8 V opposing i2."""
    d += (v1 := elm.SourceV().up().length(4).label("20 V"))
    d += elm.Resistor().right().length(3.5).label("$R_1$ = 2 Ω")
    d += (m := elm.Dot())
    d += elm.Resistor().down().length(4).label("$R_2$\n4 Ω", loc="bottom")
    d += (mb := elm.Dot())
    d += elm.Line().left().tox(v1.start)
    d += elm.Resistor().right().at(m.center).length(3.5).label("$R_3$ = 4 Ω")
    d += elm.Line().at(mb.center).right().length(3.5)
    d += elm.SourceV().up().length(4).label("8 V", loc="bottom")   # + at the top: i2 enters its + terminal
    loop(d, (1.75, 2.0), "$i_1$")
    loop(d, (5.25, 2.0), "$i_2$")


def sch_bridge_meshes(d):
    """Example 06-05.2: the bridge of 06-03.5 with three clockwise mesh currents."""
    d += (v := elm.SourceV().up().length(5).label("10 V"))
    d += elm.Line().right().length(2.0)
    d += (tl := elm.Dot())
    d += elm.Line().right().length(4.5)
    d += (tr := elm.Dot())
    d += elm.Label().at(((tl.center[0] + tr.center[0]) / 2, tl.center[1] + 0.35)).label("a", fontsize=12)
    d += elm.Resistor().down().at(tl.center).length(2.5).label("10 Ω", loc="bottom")
    d += (c := elm.Dot().label("c", loc="left"))
    d += elm.Resistor().down().length(2.5).label("40 Ω", loc="bottom")
    d += (bl := elm.Dot())
    d += elm.Resistor().down().at(tr.center).length(2.5).label("20 Ω", loc="bottom")
    d += (dd := elm.Dot().label("d", loc="right"))
    d += elm.Resistor().down().length(2.5).label("50 Ω", loc="bottom")
    d += (br := elm.Dot())
    d += elm.Resistor().at(c.center).to(dd.center).label("30 Ω", loc="top")
    d += elm.Line().at(br.center).to(bl.center)
    d += elm.Line().left().at(bl.center).tox(v.start)
    d += elm.Label().at(((bl.center[0] + br.center[0]) / 2, bl.center[1] - 0.35)).label("b", fontsize=12)
    xm = (tl.center[0] + tr.center[0]) / 2 + 0.2
    loop(d, (1.0, 2.5), "$i_1$", w=1.2, h=2.8)
    loop(d, (xm, 3.85), "$i_2$", w=1.4, h=1.0)
    loop(d, (xm, 1.25), "$i_3$", w=1.4, h=1.0)


def sch_supermesh(d):
    """Example 06-05.3: 36 V, R1 = 4, a 3 A source in the shared branch (pointing up), R2 = 2, R3 = 6."""
    d += (v := elm.SourceV().up().length(4).label("36 V"))
    d += elm.Resistor().right().length(3.5).label("$R_1$ = 4 Ω")
    d += (m := elm.Dot())
    d += elm.Resistor().right().length(3.5).label("$R_2$ = 2 Ω")
    d += elm.Resistor().down().length(4).label("$R_3$\n6 Ω", loc="bottom")
    d += elm.Line().left().tox(v.start)
    d += elm.SourceI().up().at((m.center[0], m.center[1] - 4)).length(4).label("3 A", loc="bottom")
    loop(d, (1.75, 2.0), "$i_1$")
    loop(d, (5.45, 2.0), "$i_2$", w=1.4)
    d += elm.Label().at((3.5, -0.75)).label("supermesh: KVL around the outer loop, plus $i_2 - i_1$ = 3 A",
                                              fontsize=11, color=O)


def fig_k33():
    """Example 06-05.5: K3,3 resistor network (nonplanar); the 1-4 branch holds the source."""
    pos = {1: (0, 1), 2: (1.5, 1), 3: (3, 1), 4: (0, 0), 5: (1.5, 0), 6: (3, 0)}
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    for a in (1, 2, 3):
        for b in (4, 5, 6):
            (x1, y1), (x2, y2) = pos[a], pos[b]
            src = (a, b) == (1, 4)
            ax.plot([x1, x2], [y1, y2], color=O if src else B, lw=2.6 if src else 1.4, zorder=1)
    for k, (x, y) in pos.items():
        ax.scatter([x], [y], s=260, color="white", edgecolor="black", zorder=3)
        ax.text(x, y, str(k), ha="center", va="center", fontsize=10, zorder=4)
    ax.text(-0.12, 0.5, "10 V + 1 Ω", rotation=90, ha="right", va="center", color=O, fontsize=10)
    ax.text(3.15, 0.5, "all other branches 1 Ω", rotation=90, ha="left", va="center", color=B, fontsize=9)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(-0.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Every node in the top row joins every node in the bottom row:\n"
                 "no way to draw it without crossings", fontsize=9)
    save(fig, f"{OUT}/nonplanar-k33.svg")


if __name__ == "__main__":
    schematic("two-mesh.svg", sch_two_mesh)
    schematic("bridge-meshes.svg", sch_bridge_meshes)
    schematic("supermesh.svg", sch_supermesh)
    fig_k33()
    print("06-05 figures written to", OUT)
