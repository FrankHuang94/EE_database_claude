#!/usr/bin/env python3
"""Figures for chapter 07-01 (capacitors and inductors).

Run from anywhere:  python assets/figures/src/fig_07_01.py
Outputs SVGs to assets/figures/07-01/: a matplotlib plot of the two element laws applied to the chapter's
example waveforms, and a schemdraw schematic of the practical capacitor model.
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

OUT = "assets/figures/07-01"
use_style()
B, O = PALETTE[0], PALETTE[1]


def fig_waveforms():
    """Left: Example 07-01.1 (capacitor v and i). Right: Example 07-01.2 (inductor i and v)."""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))
    # capacitor: 10 uF, 0 -> 5 V in 1 ms, hold 1 ms, 5 -> 0 in 0.5 ms
    t = np.array([0, 1, 2, 2.5, 3.0])
    v = np.array([0, 5, 5, 0, 0])
    ax = axes[0]
    ax.plot(t, v, color=B, label="$v_C$ (V)")
    ti = np.array([0, 1, 1, 2, 2, 2.5, 2.5, 3.0])
    ii = np.array([50, 50, 0, 0, -100, -100, 0, 0])
    ax2 = ax.twinx()
    ax2.plot(ti, ii, color=O, ls="--", label="$i_C$ (mA)")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("$v_C$ (V)", color=B)
    ax2.set_ylabel("$i_C = C\\,dv_C/dt$ (mA)", color=O)
    ax.set_ylim(-6, 6)
    ax2.set_ylim(-120, 120)
    ax.set_title("capacitor, 10 µF", fontsize=9)
    # inductor: 4.7 uH, 1 -> 3 A in 2 us, 3 -> 1 A in 3 us, two cycles
    ax = axes[1]
    tl = np.array([0, 2, 5, 7, 10])
    il = np.array([1, 3, 1, 3, 1])
    ax.plot(tl, il, color=B)
    tv = np.array([0, 2, 2, 5, 5, 7, 7, 10])
    vv = np.array([4.7, 4.7, -3.133, -3.133, 4.7, 4.7, -3.133, -3.133])
    ax3 = ax.twinx()
    ax3.plot(tv, vv, color=O, ls="--")
    ax.set_xlabel("time (µs)")
    ax.set_ylabel("$i_L$ (A)", color=B)
    ax3.set_ylabel("$v_L = L\\,di_L/dt$ (V)", color=O)
    ax.set_ylim(0, 4)
    ax3.set_ylim(-6, 6)
    ax.set_title("inductor, 4.7 µH", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/element-laws.svg")


def fig_real_capacitor():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += elm.Dot(open=True).label("a", loc="left")
    d += elm.Resistor().right().label("ESR")
    d += elm.Inductor().right().label("ESL")
    d += (n := elm.Dot())
    d += elm.Line().up().length(1.2)
    d += elm.Capacitor().right().label("$C$")
    d += elm.Line().down().length(1.2)
    d += (m := elm.Dot())
    d += elm.Line().down().at(n.center).length(1.2)
    d += elm.Resistor().right().label("$R_{leak}$", loc="bottom")
    d += elm.Line().up().length(1.2)
    d += elm.Line().right().at(m.center).length(1.0)
    d += elm.Dot(open=True).label("b", loc="right")
    d.save(str(ROOT / OUT / "real-capacitor.svg"))


if __name__ == "__main__":
    (ROOT / OUT).mkdir(parents=True, exist_ok=True)
    fig_waveforms()
    fig_real_capacitor()
    print("07-01 figures written to", OUT)
