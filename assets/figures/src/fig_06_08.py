#!/usr/bin/env python3
"""Figures for chapter 06-08 (Thevenin and Norton equivalents).

Run from anywhere:  python assets/figures/src/fig_06_08.py
Outputs SVGs to assets/figures/06-08/. Schematics use schemdraw; the two-load plot uses matplotlib.
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

OUT = "assets/figures/06-08"
use_style()
B, O = PALETTE[0], PALETTE[1]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


def sch_equivalents(d):
    """A linear network at a port, its Thevenin equivalent and its Norton equivalent."""
    # network box
    d += elm.Rect(corner1=(0, 0), corner2=(2.6, 3)).linestyle("--")
    d += elm.Label().at((1.3, 1.5)).label("linear\nnetwork\n(R, sources,\ndependent\nsources)", fontsize=10)
    d += elm.Line().at((2.6, 2.5)).right().length(1.0)
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.Line().at((2.6, 0.5)).right().length(1.0)
    d += elm.Dot(open=True).label("b", loc="right")
    d += elm.Label().at((4.5, 1.5)).label("≡", fontsize=22)
    # Thevenin
    x = 6.2
    d += (v := elm.SourceV().up().at((x, 0.5)).length(2.0).label("$V_{th}$"))
    d += elm.Resistor().right().length(2.0).label("$R_{th}$")
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.Line().at(v.start).right().length(2.0)
    d += elm.Dot(open=True).label("b", loc="right")
    d += elm.Label().at((9.7, 1.5)).label("≡", fontsize=22)
    # Norton
    x = 11.4
    d += (i := elm.SourceI().up().at((x, 0.5)).length(2.0).label("$I_N$"))
    d += elm.Line().right().length(1.4)
    d += (t := elm.Dot())
    d += elm.Resistor().down().length(2.0).label("$R_{th}$", loc="bottom")
    d += elm.Line().at(i.start).right().length(1.4)
    d += elm.Line().at(t.center).right().length(1.0)
    d += elm.Dot(open=True).label("a", loc="right")
    d += elm.Line().at((x + 1.4, 0.5)).right().length(1.0)
    d += elm.Dot(open=True).label("b", loc="right")
    d += elm.Label().at((13.4, -0.6)).label("$V_{th} = R_{th} I_N$", fontsize=12)


def sch_poe(d):
    """Example 06-08.4: a PoE port as a Thevenin source driving a powered device."""
    d += (v := elm.SourceV().up().length(3).label("$V_{PSE}$\n52 V"))
    d += elm.Resistor().right().length(3.0).label("$R_{chan}$ = 6.25 Ω\n(100 m, 4 pairs)")
    d += (p := elm.Dot().label("PD input", loc="bottom"))
    x0 = p.center[0] + 0.8
    d += elm.Rect(corner1=(x0, -0.3), corner2=(x0 + 2.0, 3.3)).at((0, 0)).color(O)
    d += elm.Label().at((x0 + 1.0, 1.5)).label("powered\ndevice\n71.3 W", fontsize=10, color=O)
    d += elm.Line().at(p.center).right().length(0.8)
    d += elm.Line().at(v.start).right().length(3.8)
    d += elm.Label().at((1.5, -0.7)).label("PSE (power sourcing equipment)", fontsize=10)


def fig_two_load():
    """Example 06-08.5: 1/v against 1/R_L is a straight line; intercept 1/V_th, slope R_th/V_th."""
    Vth, Rth = 0.300, 200.0                      # V, MOhm
    RL = np.logspace(0.5, 4.5, 200)               # MOhm
    v = Vth * RL / (Rth + RL)
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.2))
    ax = axes[0]
    ax.semilogx(RL, v * 1e3, color=B)
    for r, lab in ((10.0, "10 MΩ meter"), (1e4, "10 GΩ mode")):
        vv = Vth * r / (Rth + r)
        ax.plot([r], [vv * 1e3], "o", color=O)
        ax.annotate(f"{lab}\n{vv * 1e3:.1f} mV", (r, vv * 1e3), textcoords="offset points", xytext=(8, 14) if r < 100 else (6, -40), fontsize=8)
    ax.axhline(300, color="0.5", ls="--", lw=0.8)
    ax.set_xlabel("load resistance (MΩ)")
    ax.set_ylabel("reading (mV)")
    ax.set_title("A 200 MΩ, 300 mV source", fontsize=10)
    ax = axes[1]
    x = 1 / RL
    ax.plot(x, 1 / v, color=B)
    for r in (10.0, 1e4):
        ax.plot([1 / r], [(Rth + r) / (Vth * r)], "o", color=O)
    ax.set_xlabel("1 / load (1/MΩ)")
    ax.set_ylabel("1 / reading (1/V)")
    ax.set_title("straight line: intercept 1/V_th, slope R_th/V_th", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/two-load-method.svg")


if __name__ == "__main__":
    schematic("thevenin-norton.svg", sch_equivalents)
    schematic("poe-thevenin.svg", sch_poe)
    fig_two_load()
    print("06-08 figures written to", OUT)
