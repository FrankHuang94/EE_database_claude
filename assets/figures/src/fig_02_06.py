#!/usr/bin/env python3
"""Figures for chapter 02-06 (vectors, matrices and linear systems).

Run:  python assets/figures/src/fig_02_06.py  -> assets/figures/02-06/*.svg
Plots use matplotlib; the circuit schematic uses schemdraw.
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
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/02-06"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def arrow(ax, start, end, color, label=None, lw=2.0, ls="-"):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=14))


def fig_projection():
    """Example 02-06.1 drawn in the plane of u and v (orthonormal coordinates of that plane)."""
    u = np.array([2.0, -1.0, 2.0])
    v = np.array([3.0, 0.0, 4.0])
    e1 = u / np.linalg.norm(u)
    w = v - (v @ e1) * e1
    e2 = w / np.linalg.norm(w)
    U = np.array([u @ e1, u @ e2])
    V = np.array([v @ e1, v @ e2])
    Pp = np.array([(v @ e1), 0.0])
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.plot([-0.3, 5.6], [0, 0], color="0.75", lw=1, ls=":")
    arrow(ax, (0, 0), tuple(Pp), G, lw=5.0)
    arrow(ax, (0, 0), tuple(U), B, lw=2.0)
    arrow(ax, (0, 0), tuple(V), "k")
    arrow(ax, tuple(Pp), tuple(V), O, ls="--")
    s = 0.18
    ax.plot([Pp[0] - s, Pp[0] - s, Pp[0]], [0, s, s], color="0.4", lw=1)
    ax.text(U[0] / 2, -0.32, "u = (2, −1, 2), length 3", color=B, ha="center", fontsize=9)
    ax.text(V[0] / 2 - 0.65, V[1] / 2 + 0.25, "v = (3, 0, 4)\nlength 5", color="k", ha="center", fontsize=9)
    ax.text(Pp[0] - 0.2, -0.32, "p = (14/9) u", color=G, ha="right", fontsize=9)
    ax.text(Pp[0] + 0.12, Pp[1] + V[1] / 2, "e = v − p\n(length 1.795)", color=O, ha="left", fontsize=9)
    ax.text(0.75, 0.12, "θ = 21.04°", fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-0.4, 6.2)
    ax.set_ylim(-0.6, 2.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Projection onto a line: the error is perpendicular to u")
    fig.tight_layout()
    save(fig, f"{OUT}/projection.svg")


def fig_row_column():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 4.0))
    x = np.linspace(-0.5, 4.5, 50)
    a1.plot(x, 2 * x - 1, color=B, label="2x₁ − x₂ = 1")
    a1.plot(x, 5 - x, color=O, label="x₁ + x₂ = 5")
    a1.plot([2], [3], "o", color="k")
    a1.annotate("solution (2, 3)", (2, 3), xytext=(2.4, 1.6), fontsize=9,
                arrowprops=dict(arrowstyle="-", color="0.5"))
    a1.set_xlabel("x₁")
    a1.set_ylabel("x₂")
    a1.set_xlim(-0.5, 4.5)
    a1.set_ylim(-1, 6)
    a1.legend(fontsize=8, loc="upper left")
    a1.set_title("Row picture: lines cross at the solution")
    c1, c2, b = np.array([2.0, 1.0]), np.array([-1.0, 1.0]), np.array([1.0, 5.0])
    arrow(a2, (0, 0), tuple(c1), B)
    arrow(a2, (0, 0), tuple(c2), O)
    arrow(a2, (0, 0), tuple(2 * c1), B, lw=1.2, ls="--")
    arrow(a2, tuple(2 * c1), tuple(2 * c1 + 3 * c2), O, lw=1.2, ls="--")
    arrow(a2, (0, 0), tuple(b), "k", lw=2.4)
    a2.text(1.15, 0.35, "column 1 = (2, 1)", color=B, fontsize=9)
    a2.text(-1.9, 1.15, "column 2\n= (−1, 1)", color=O, fontsize=9)
    a2.text(3.1, 1.7, "2 × column 1", color=B, fontsize=9)
    a2.text(2.6, 4.0, "+ 3 × column 2", color=O, fontsize=9)
    a2.text(-0.15, 5.25, "b = (1, 5)", color="k", fontsize=9)
    a2.set_aspect("equal")
    a2.set_xlim(-2.2, 4.8)
    a2.set_ylim(-0.6, 5.9)
    a2.set_title("Column picture: 2·(2, 1) + 3·(−1, 1) = b")
    fig.tight_layout()
    save(fig, f"{OUT}/row-column-pictures.svg")


def solve2(a11, a12, a21, a22, b1, b2):
    """Elimination without row exchanges, in IEEE double precision."""
    m = a21 / a11
    u22 = a22 - m * a12
    c2 = b2 - m * b1
    x2 = c2 / u22
    return (b1 - a12 * x2) / a11, x2


def fig_pivoting():
    eps = np.logspace(-2, -18, 161)
    naive, piv = [], []
    for e in eps:
        true1 = 1.0 / (1.0 - e)
        x1n, _ = solve2(e, 1.0, 1.0, 1.0, 1.0, 2.0)
        x1p, _ = solve2(1.0, 1.0, e, 1.0, 2.0, 1.0)
        naive.append(max(abs(x1n - true1) / true1, 1e-17))
        piv.append(max(abs(x1p - true1) / true1, 1e-17))
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.loglog(eps, naive, ".", color=O, ms=4, label="no pivoting (pivot = ε)")
    ax.loglog(eps, piv, ".", color=B, ms=4, label="partial pivoting (rows exchanged)")
    ax.loglog(eps, np.minimum(2.2e-16 / eps, 1.0), color="0.5", lw=1, ls="--",
              label="machine epsilon / ε")
    ax.invert_xaxis()
    ax.set_xlabel("pivot size ε (smaller to the right)")
    ax.set_ylabel("relative error in computed x₁")
    ax.set_ylim(5e-18, 3)
    ax.set_title("[ε 1; 1 1] x = [1; 2] in double precision")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/pivoting-error.svg")


def fig_nodal_circuit():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += (src := elm.SourceI().up().label("10 mA", loc="top"))
    d += (n1 := elm.Dot().label("1", loc="left"))
    d += elm.Resistor().right().label("$R_a$ = 1 kΩ", loc="bottom")
    d += (n2 := elm.Dot().label("2", loc="bottom", ofst=(0.25, -0.1)))
    d += elm.Resistor().right().label("$R_d$ = 2 kΩ", loc="bottom")
    d += (n3 := elm.Dot().label("3", loc="right"))
    d += elm.Resistor().down().label("$R_e$ = 500 Ω", loc="bottom")
    d += (br := elm.Line().left().tox(src.start))
    d += elm.Resistor().at(n2.center).down().label("$R_c$ = 1 kΩ", loc="bottom")
    d += elm.Line().at(n1.center).up().length(1.5)
    d += elm.Resistor().right().tox(n3.center).label("$R_b$ = 2 kΩ", loc="top")
    d += elm.Line().down().toy(n3.center)
    d += elm.Ground().at(src.start)
    return save_schem(d, f"{OUT}/nodal-circuit.svg")


def save_schem(d, rel):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(path))
    print(f"wrote {rel}")


if __name__ == "__main__":
    fig_projection()
    fig_row_column()
    fig_pivoting()
    fig_nodal_circuit()
