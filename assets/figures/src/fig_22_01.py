#!/usr/bin/env python3
"""Figures for chapter 22-01 (power conversion principles).

Run from anywhere:  python assets/figures/src/fig_22_01.py
Outputs
  assets/figures/22-01/linear-vs-switching.svg  a linear regulator (pass PMOS, error amplifier, 1.8 V reference)
                                                beside a synchronous buck (two switches, switch node, L, C, load)
  assets/figures/22-01/switch-node.svg          one period of the switch-node voltage, inductor current and output
                                                of Example 22-01.4's buck, from its exact periodic steady state
  assets/figures/22-01/efficiency-vs-load.svg   efficiency against load for Example 22-01.5's loss model: fixed
                                                frequency, a PFM mode with a tenth of the fixed loss, and two phases
The schematic uses schemdraw.
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
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import power as pw  # noqa: E402

OUT = "assets/figures/22-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_schematics():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # ---- (a) linear regulator: a series pass device steered by an error amplifier
    d += elm.Label().at((2.2, 5.4)).label("(a) linear regulator")
    d += elm.Dot().at((0, 3.5)).label("$V_{in}$ = 12 V", loc="left")
    d += elm.ResistorVar().right().length(3.0).label("pass device", loc="bottom", ofst=0.5)
    d += elm.Line().right().length(1.4)
    d += elm.Dot().label("$V_{out}$ = 3.3 V", loc="top")
    d += elm.Resistor().down().length(2.5).label("load\n1 A", loc="bottom")
    d += elm.Ground()
    d += (ea := elm.Opamp(leads=True).at((1.5, 0.4)).up().anchor("out").scale(0.7))
    d += elm.Line().at(ea.out).toy(3.5 - 0.35)
    d += elm.Label().at((0.1, 0.6)).label("error\namplifier")
    d += elm.Label().at((1.5, -2.7)).label("inputs: $V_{ref}$ and $v_{out}$")
    d += elm.Label().at((2.2, -3.5)).label("drops 8.7 V at the full 1 A: 8.7 W of heat")
    # ---- (b) synchronous buck
    x0 = 8.6
    d += elm.Label().at((x0 + 2.8, 5.4)).label("(b) synchronous buck")
    d += elm.Dot().at((x0, 3.5)).label("$V_{in}$", loc="left")
    d += elm.Line().right().length(1.0)
    d += elm.Switch().down().length(2.0).label("$S_1$", loc="bottom")
    d += (sw := elm.Dot())
    d += elm.Switch().down().length(2.0).label("$S_2$", loc="bottom")
    d += elm.Ground()
    d += elm.Label().at((x0 + 2.4, 1.0)).label("switch node")
    d += elm.Inductor().at(sw.center).right().length(2.6).label("$L$", loc="top")
    d += (bo := elm.Dot())
    d += elm.Capacitor().down().length(2.0).label("$C$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(bo.center).right().length(1.8)
    d += elm.Dot().label("$V_{out} = DV_{in}$", loc="top")
    d += elm.Resistor().down().length(2.0).label("load", loc="bottom")
    d += elm.Ground()
    d += elm.Label().at((x0 + 2.8, -2.4)).label("$S_1$ on for $DT_s$, $S_2$ for the rest;\nideal parts dissipate nothing")
    path = ROOT / OUT / "linear-vs-switching.svg"
    d.save(str(path))


def fig_switch_node():
    d = 3.3 / 12
    t, il, vo = pw.buck_pss(12.0, d, 500e3, 10e-6, 1e-6, 3.3)
    tus = t * 1e6
    vsw = np.where(t <= d * t[-1], 12.0, 0.0)
    fig, ax = plt.subplots(3, 1, figsize=(5.8, 5.2), sharex=True)
    ax[0].plot(tus, vsw, color=PALETTE[0], lw=1.5)
    ax[0].axhline(d * 12, color="0.5", ls=":", lw=1)
    ax[0].text(1.25, d * 12 + 0.6, "average D·V_in = 3.3 V", fontsize=8, color="0.35")
    ax[0].set_ylabel("v_sw (V)")
    ax[1].plot(tus, il, color=PALETTE[1], lw=1.5)
    ax[1].set_ylabel("i_L (A)")
    ax[2].plot(tus, vo, color=PALETTE[2], lw=1.5)
    ax[2].set_ylabel("v_out (V)")
    ax[2].set_xlabel("time within one 2 µs period (µs)")
    ax[0].set_title("Ideal buck, 12 V to 3.3 V at 500 kHz: chop, then filter", fontsize=10)
    save(fig, f"{OUT}/switch-node.svg")


def fig_efficiency():
    p0, a, r, v = 0.150, 0.030, 0.003, 1.0
    i = np.logspace(-2, np.log10(30), 600)
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.semilogx(i, pw.model_efficiency(i, v, p0, a, r) * 100, color=PALETTE[0], lw=1.6,
                label="one phase, fixed frequency")
    ax.semilogx(i, pw.model_efficiency(i, v, p0 / 10, a, r) * 100, color=PALETTE[2], lw=1.6, ls="--",
                label="one phase, PFM (fixed loss ÷ 10)")
    ax.semilogx(i, v * i / (v * i + pw.phased_loss(i, 2, p0, a, r)) * 100, color=PALETTE[1], lw=1.6, ls="-.",
                label="two phases")
    ip = pw.peak_efficiency_current(p0, r)
    ax.plot([ip], [pw.model_efficiency(ip, v, p0, a, r) * 100], "o", color=PALETTE[0])
    ax.annotate("peak where P₀ = RI²", (ip, pw.model_efficiency(ip, v, p0, a, r) * 100), xytext=(0.6, 72),
                fontsize=8, arrowprops={"arrowstyle": "->", "color": "0.4"})
    ax.set_ylim(0, 100)
    ax.set_xlabel("load current (A)")
    ax.set_ylabel("efficiency (%)")
    ax.set_title("A converter's efficiency curve has a peak", fontsize=10)
    ax.legend(loc="lower right", fontsize=8)
    save(fig, f"{OUT}/efficiency-vs-load.svg")


if __name__ == "__main__":
    fig_schematics()
    fig_switch_node()
    fig_efficiency()
