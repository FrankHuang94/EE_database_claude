#!/usr/bin/env python3
"""Figures for chapter 07-04 (Laplace-domain circuit analysis).

Run from anywhere:  python assets/figures/src/fig_07_04.py
Outputs SVGs to assets/figures/07-04/: schematics with schemdraw, the Wien-bridge pole locus with
matplotlib (poles as eigenvalues of the circuit's state matrix).
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

OUT = "assets/figures/07-04"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


def sch_element_models(d):
    # 1. inductor, series form: sL in series with a voltage source L i(0-)
    x = 0.0
    d += elm.Dot(open=True).at((x, 4)).label("+", loc="left")
    d += elm.Inductor().down().at((x, 4)).label("$sL$", loc="bottom")
    d += elm.SourceV().down().label("$L\\,i(0^-)$", loc="bottom")
    d += elm.Dot(open=True).label("−", loc="left")
    d += elm.Label().at((x, 4.9)).label("inductor, series")
    # 2. inductor, parallel form: 1/sL in parallel with a current source i(0-)/s
    x = 4.0
    d += elm.Line().right().at((x, 4)).length(2)
    d += elm.Inductor().down().at((x, 4)).length(4).label("$sL$", loc="bottom")
    d += elm.SourceI().down().at((x + 2, 4)).length(4).label("$i(0^-)/s$", loc="bottom")
    d += elm.Line().right().at((x, 0)).length(2)
    d += elm.Dot(open=True).at((x, 4))
    d += elm.Dot(open=True).at((x, 0))
    d += elm.Label().at((x + 1, 4.9)).label("inductor, parallel")
    # 3. capacitor, series form: 1/sC in series with a voltage source v(0-)/s
    x = 10.0
    d += elm.Dot(open=True).at((x, 4)).label("+", loc="left")
    d += elm.Capacitor().down().at((x, 4)).label("$1/sC$", loc="bottom")
    d += elm.SourceV().down().label("$v(0^-)/s$", loc="bottom").reverse()
    d += elm.Dot(open=True).label("−", loc="left")
    d += elm.Label().at((x, 4.9)).label("capacitor, series")
    # 4. capacitor, parallel form: sC in parallel with a current source C v(0-)
    x = 14.0
    d += elm.Line().right().at((x, 4)).length(2)
    d += elm.Capacitor().down().at((x, 4)).length(4).label("$1/sC$", loc="bottom")
    d += elm.SourceI().up().at((x + 2, 0)).length(4).label("$C\\,v(0^-)$", loc="bottom")
    d += elm.Line().right().at((x, 0)).length(2)
    d += elm.Dot(open=True).at((x, 4))
    d += elm.Dot(open=True).at((x, 0))
    d += elm.Label().at((x + 1, 4.9)).label("capacitor, parallel")


def sch_butterworth(d):
    d += (vs := elm.SourceV().up().label("$V_S$"))
    d += elm.Resistor().right().label("50 Ω")
    d += (n1 := elm.Dot().label("1", loc="top"))
    d += elm.Inductor().right().length(4.5).label("L = 15.92 µH")
    d += (n2 := elm.Dot().label("2", loc="top"))
    d += elm.Line().right().length(4.5)
    d += elm.Resistor().down().label("50 Ω", loc="bottom")
    d += (gnd := elm.Line().left().tox(vs.start))
    d += elm.Ground()
    d += elm.Capacitor().down().at(n1.center).toy(vs.start).label("$C_1$ = 3.183 nF", loc="bottom")
    d += elm.Capacitor().down().at(n2.center).toy(vs.start).label("$C_2$ = 3.183 nF", loc="bottom")


def fig_wien_poles():
    R, C = 10e3, 10e-9
    Ks = np.linspace(0.0, 3.5, 351)
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    pts = []
    for K in Ks:
        A = np.array([[-1, K - 1], [-1, K - 2]]) / (R * C)
        pts.append(np.linalg.eigvals(A))
    pts = np.array(pts) / 1e3
    sc = ax.scatter(pts.real.ravel(), pts.imag.ravel(), c=np.repeat(Ks, 2), cmap="viridis", s=6)
    for K, mk in ((2.9, "o"), (3.0, "s"), (3.1, "^")):
        A = np.array([[-1, K - 1], [-1, K - 2]]) / (R * C)
        e = np.linalg.eigvals(A) / 1e3
        ax.plot(e.real, e.imag, mk, color=O, ms=7, label=f"K = {K}")
    ax.axvline(0, color="0.3", lw=0.8)
    ax.set_xlabel("Re s (10³ s⁻¹)")
    ax.set_ylabel("Im s (10³ s⁻¹)")
    ax.set_xlim(-30, 3)
    fig.colorbar(sc, ax=ax, label="amplifier gain K")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/wien-poles.svg")


if __name__ == "__main__":
    schematic("element-models.svg", sch_element_models)
    schematic("butterworth-schematic.svg", sch_butterworth)
    fig_wien_poles()
    print("07-04 figures written to", OUT)
