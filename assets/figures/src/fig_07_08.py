#!/usr/bin/env python3
"""Figures for chapter 07-08 (filters and resonance).

Run from anywhere:  python assets/figures/src/fig_07_08.py
Outputs SVGs to assets/figures/07-08/: series-resonance current for three Q values, the Butterworth
magnitude family for orders 1 to 5, and the Sallen-Key low-pass schematic.
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

OUT = "assets/figures/07-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_resonance():
    r = np.logspace(-0.5, 0.5, 2000)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for Q, c in ((2, PALETTE[0]), (10, PALETTE[1]), (100, PALETTE[2])):
        # series RLC current relative to its peak: 1/(1 + jQ(r - 1/r))
        H = 1 / (1 + 1j * Q * (r - 1 / r))
        ax.semilogx(r, np.abs(H), color=c, label=f"Q = {Q}")
    ax.axhline(1 / np.sqrt(2), color="0.6", ls=":", lw=0.8)
    ax.text(0.33, 0.73, "half power (0.707)", fontsize=8, color="0.3")
    ax.set_xlabel(r"$\omega/\omega_0$")
    ax.set_ylabel(r"$|I|\,/\,I_{peak}$")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/series-resonance.svg")


def fig_butterworth():
    x = np.logspace(-1, 1, 1500)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for n in range(1, 6):
        mag = -10 * np.log10(1 + x ** (2 * n))
        ax.semilogx(x, mag, color=PALETTE[n - 1], label=f"n = {n}")
    ax.axhline(-3.01, color="0.6", ls=":", lw=0.8)
    ax.text(0.11, -6.5, "−3.01 dB at the cutoff for every order", fontsize=8, color="0.3")
    ax.set_xlabel(r"$\omega/\omega_c$")
    ax.set_ylabel("magnitude (dB)")
    ax.set_ylim(-60, 3)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/butterworth-family.svg")


def fig_sallen_key():
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Resistor().right().label("$R_1$")
    d += (a := elm.Dot().label("A", loc="bottom"))
    d += elm.Resistor().right().label("$R_2$")
    d += (b := elm.Dot().label("B", loc="top"))
    d += elm.Line().right().length(0.8)
    d += (op := elm.Opamp(leads=True).anchor("in2").right())
    d += elm.Capacitor().down().at(b.center).label("$C_2$", loc="bottom")
    d += elm.Ground()
    d += (w := elm.Line().right().at(op.out).length(0.6))
    d += elm.Line().right().length(1.0)
    d += (o := elm.Dot().label("$v_{out}$", loc="right"))
    # follower feedback: output to inverting input
    d += elm.Line().up().at(op.in1).length(1.0)
    d += elm.Line().right().tox(w.end)
    d += elm.Line().down().toy(w.end)
    d += elm.Dot().at(w.end)
    # C1 from node A, over the top, down to the output node
    d += elm.Line().up().at(a.center).length(3.0)
    d += elm.Capacitor().right().tox(o.center).label("$C_1$")
    d += elm.Line().down().toy(o.center)
    d.save(str(ROOT / OUT / "sallen-key.svg"))


if __name__ == "__main__":
    fig_resonance()
    fig_butterworth()
    fig_sallen_key()
