#!/usr/bin/env python3
"""Figures for chapter 15-09 (lead and lag compensation).

Run from anywhere:  python assets/figures/src/fig_15_09.py
Outputs
  assets/figures/15-09/lead-lag-bode.svg   Bode plots of a lead (1 + 10Ts)/(1 + Ts) and a lag (1 + s/z)/(1 + s/p) with
                                           z/p = 10, on a normalized frequency axis, with the lead's 54.9 deg peak at
                                           the geometric mean of its corners
  assets/figures/15-09/lead-network.svg    the passive lead network of section 3.6 and the lab (9 kOhm || 10 nF in
                                           series, 1 kOhm to ground)
  assets/figures/15-09/type3.svg           the op-amp Type III compensator of section 3.6, with Example 15-09.6's values
The schematics use schemdraw.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/15-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_bode():
    x = np.logspace(-3, 2, 2000)   # omega T for the lead; omega / p for the lag
    lead = (1 + 1j * 10 * x) / (1 + 1j * x)
    lag = (1 + 1j * x / 10) / (1 + 1j * x)   # lag pole at x = 1, zero at x = 10
    fig, (am, ap) = plt.subplots(2, 1, figsize=(6.4, 4.6), sharex=True)
    for H, col, lab in ((lead, PALETTE[0], "lead, α = 10: (1 + 10Ts)/(1 + Ts), x = ωT"),
                        (lag, PALETTE[3], "lag, z/p = 10: (1 + s/z)/(1 + s/p), x = ω/p")):
        am.semilogx(x, 20 * np.log10(np.abs(H)), color=col, label=lab)
        ap.semilogx(x, np.degrees(np.angle(H)), color=col)
    xm = 1 / math.sqrt(10)
    ap.axvline(xm, color=PALETTE[0], ls=":", lw=0.8)
    ap.annotate("lead peak 54.9° at x = 1/√10", (xm, 54.9), textcoords="offset points", xytext=(8, -4), fontsize=7)
    ap.annotate("lag dip −54.9° at x = √10", (math.sqrt(10), -54.9), textcoords="offset points", xytext=(8, 0),
                fontsize=7)
    am.axhline(0, color="gray", lw=0.5)
    ap.axhline(0, color="gray", lw=0.5)
    am.set_ylabel("gain (dB)")
    ap.set_ylabel("phase (deg)")
    ap.set_xlabel("normalized frequency x")
    am.legend(fontsize=7, loc="lower left")
    am.set_title("Lead adds phase where it adds gain; lag removes gain (and some phase) where it sits", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/lead-lag-bode.svg")


def save_schem(d, rel):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(path))


def fig_lead_network():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += (vin := elm.Dot().label("$v_{in}$", loc="left"))
    d += elm.Line().right().length(1.0)
    d += (a := elm.Dot())
    d += elm.Resistor().right().length(3.0).label("$R_1$ = 9 kΩ", loc="bottom")
    d += (b := elm.Dot())
    d += elm.Line().at(a.center).up().length(1.5)
    d += elm.Capacitor().right().length(3.0).label("$C_1$ = 10 nF", loc="top")
    d += elm.Line().down().toy(b.center)
    d += elm.Line().at(b.center).right().length(1.5)
    d += (o := elm.Dot().label("$v_{out}$", loc="right"))
    d += elm.Resistor().at(b.center).down().length(2.5).label("$R_2$ = 1 kΩ", loc="bottom")
    d += elm.Ground()
    d += elm.Label().at((3.0, -3.6)).label("zero 1/(R₁C₁) = 1.77 kHz, pole 1/((R₁∥R₂)C₁) = 17.7 kHz, α = (R₁ + R₂)/R₂ = 10")
    save_schem(d, f"{OUT}/lead-network.svg")


def fig_type3():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += (op := elm.Opamp(leads=True))
    d += elm.Line().at(op.in1).left().length(1.0)
    d += (n := elm.Dot())
    d += elm.Resistor().left().length(4.0).label("$R_1$ = 10 kΩ", loc="bottom")
    d += (vs := elm.Dot().label("$v_{out}$\n(sensed)", loc="left"))
    d += elm.Line().at(vs.center).up().length(1.5)
    d += elm.Resistor().right().length(2.0).label("$R_3$ = 272 Ω", loc="top")
    d += elm.Capacitor().right().length(2.0).label("$C_3$ = 1.95 nF", loc="bottom")
    d += elm.Dot()
    d += elm.Line().down().toy(n.center)
    span = op.out[0] - n.center[0]
    d += elm.Line().at(n.center).up().length(3.0)
    d += (ft := elm.Dot())
    d += elm.Resistor().right().length(0.4 * span).label("$R_2$ = 3.68 kΩ", loc="top")
    d += elm.Capacitor().right().length(0.4 * span).label("$C_1$ = 5.43 nF", loc="bottom")
    d += elm.Line().right().tox(op.out)
    d += (fo := elm.Dot())
    d += elm.Line().down().toy(op.out)
    d += elm.Line().at(ft.center).up().length(1.5)
    d += elm.Capacitor().right().tox(fo.center).label("$C_2$ = 148 pF", loc="top")
    d += elm.Line().down().toy(fo.center)
    d += elm.Line().at(op.out).right().length(1.5)
    d += elm.Dot().label("$v_c$ → PWM\n(gain 1/$V_M$)", loc="right")
    d += elm.Line().at(op.in2).left().length(0.75)
    d += elm.Dot().label("$V_{ref}$", loc="left")
    save_schem(d, f"{OUT}/type3.svg")


if __name__ == "__main__":
    fig_bode()
    fig_lead_network()
    fig_type3()
