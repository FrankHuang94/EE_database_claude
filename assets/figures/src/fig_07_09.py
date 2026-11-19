#!/usr/bin/env python3
"""Figures for chapter 07-09 (mutual inductance and transformers).

Run from anywhere:  python assets/figures/src/fig_07_09.py
Outputs SVGs to assets/figures/07-09/: the practical transformer's equivalent circuit, and efficiency
against load for the two 50 kVA designs of Examples 07-09.4 and 07-09.5.
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

OUT = "assets/figures/07-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_equivalent_circuit():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += elm.Dot(open=True).label("$v_1$", loc="left")
    d += elm.Resistor().right().label("$R_1$")
    d += elm.Inductor().right().label("$L_{\\ell 1}$")
    d += (n := elm.Dot())
    d += elm.Line().right().length(3)
    d += (t := elm.Transformer(t1=4, t2=4).anchor("p1").label("$N_1 : N_2$\nideal", loc="top"))
    d += elm.Inductor().right().at(t.s1).label("$L_{\\ell 2}$")
    d += elm.Resistor().right().label("$R_2$")
    d += elm.Dot(open=True).label("$v_2$", loc="right")
    d += elm.Resistor().down().at(n.center).toy(t.p2).label("$R_c$", loc="bottom")
    d += elm.Line().right().length(1.5).at(n.center)
    d += elm.Inductor().down().toy(t.p2).label("$L_m$", loc="bottom")
    d += elm.Line().left().length(1.5)
    d += elm.Line().right().length(1.5)
    d += elm.Line().right().tox(t.p2)
    d.save(str(ROOT / OUT / "equivalent-circuit.svg"))


def fig_efficiency():
    x = np.linspace(0.02, 1.2, 500)
    S = 50e3
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for core, cu, c, lab in ((90, 497, PALETTE[0], "design G: core 90 W, copper 497 W"),
                             (30, 560, PALETTE[1], "design A: core 30 W, copper 560 W")):
        eta = x * S / (x * S + core + x**2 * cu) * 100
        ax.plot(x * 100, eta, color=c, label=lab)
        xs = np.sqrt(core / cu)
        ax.plot(xs * 100, xs * S / (xs * S + 2 * core) * 100, "o", color=c, ms=5)
    ax.set_xlabel("load (% of rating, unity power factor)")
    ax.set_ylabel("efficiency (%)")
    ax.set_ylim(97.5, 99.6)
    ax.legend(fontsize=8, loc="lower right")
    ax.text(40, 98.15, "dots: maximum efficiency,\nwhere copper loss = core loss", fontsize=8, color="0.3")
    fig.tight_layout()
    save(fig, f"{OUT}/efficiency-vs-load.svg")


if __name__ == "__main__":
    fig_equivalent_circuit()
    fig_efficiency()
