#!/usr/bin/env python3
"""Figures for chapter 10-07 (BJT single-stage amplifiers).

Run from anywhere:  python assets/figures/src/fig_10_07.py
Outputs SVGs to assets/figures/10-07/:
- three-configurations.svg: common emitter (with optional R_E), common base and common collector
  (emitter follower), with the signal-ground terminal of each;
- rout-degeneration.svg: output resistance looking into the collector (BJT: g_m = 38.68 mS, beta = 100,
  r_o = 50 kOhm) and into the drain (MOSFET: g_m = 2 mS, r_o = 40 kOhm) against the degeneration
  resistance; the BJT saturates at (beta + 1) r_o + r_pi because base current bypasses the feedback.
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

OUT = "assets/figures/10-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VT = 1.380649e-23 * 300 / 1.602176634e-19


def fig_configs():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # (a) common emitter
    d += elm.Label().at((1.5, 5.5)).label("(a) common emitter", fontsize=13)
    d += (q := elm.BjtNpn(circle=True).right().at((1.0, 1.5)).anchor("base"))
    d += elm.Line().at(q.base).left().length(0.8)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Resistor().at(q.collector).up().length(1.4).label("$R_C$", loc="bottom")
    d += elm.Vdd().label("$V_{CC}$")
    d += elm.Line().at(q.collector).right().length(1.2)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Resistor().at(q.emitter).down().length(1.4).label("$R_E$ (optional)", loc="bottom")
    d += elm.Ground()
    # (b) common base
    x0 = 7.5
    d += elm.Label().at((x0 + 0.8, 5.5)).label("(b) common base", fontsize=13)
    d += (q2 := elm.BjtNpn(circle=True).right().at((x0, 1.5)).anchor("base"))
    d += elm.Line().at(q2.base).left().length(0.6)
    d += elm.Label().label("$V_B$ (signal ground)", loc="left", fontsize=10)
    d += elm.Resistor().at(q2.collector).up().length(1.4).label("$R_C$", loc="bottom")
    d += elm.Vdd().label("$V_{CC}$")
    d += elm.Line().at(q2.collector).right().length(1.2)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Line().at(q2.emitter).down().length(0.6)
    d += (n2 := elm.Dot())
    d += elm.SourceI().down().length(1.4).label("$I_{bias}$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(n2.center).right().length(1.4)
    d += elm.Dot(open=True).label("$v_{in}$", loc="right")
    # (c) common collector
    x1 = 15.0
    d += elm.Label().at((x1 + 1.2, 5.5)).label("(c) common collector (emitter follower)", fontsize=13)
    d += (q3 := elm.BjtNpn(circle=True).right().at((x1, 1.5)).anchor("base"))
    d += elm.Line().at(q3.base).left().length(0.8)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Line().at(q3.collector).up().length(1.4)
    d += elm.Vdd().label("$V_{CC}$ (signal ground)")
    d += elm.Line().at(q3.emitter).down().length(0.6)
    d += (n3 := elm.Dot())
    d += elm.Resistor().down().length(1.4).label("$R_E$ or $I_{bias}$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(n3.center).right().length(1.4)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d.save(str(ROOT / OUT / "three-configurations.svg"))


def fig_rout():
    r = np.logspace(1, 7, 400)
    gm_b, beta, ro_b = 1e-3 / VT, 100, 50e3
    rpi = beta / gm_b
    re_par = r * rpi / (r + rpi)
    rout_b = ro_b * (1 + gm_b * re_par) + re_par
    gm_m, ro_m = 2e-3, 40e3
    rout_m = ro_m + r + gm_m * ro_m * r
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.loglog(r, rout_b, color=PALETTE[0], label="BJT: $r_o[1 + g_m(R_E \\parallel r_\\pi)] + R_E \\parallel r_\\pi$")
    ax.loglog(r, rout_m, color=PALETTE[1], ls="--", label="MOSFET: $r_o + R_S + g_mr_oR_S$")
    ax.axhline((beta + 1) * ro_b + rpi, color="0.6", ls=":")
    ax.text(12, (beta + 1) * ro_b * 1.25, "BJT ceiling $(\\beta + 1)r_o + r_\\pi$ ≈ 5.05 MΩ", fontsize=8, color="0.3")
    ax.set_xlabel("degeneration resistance $R_E$ or $R_S$ ($\\Omega$)")
    ax.set_ylabel("output resistance ($\\Omega$)")
    ax.set_ylim(1e4, 1e10)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/rout-degeneration.svg")


if __name__ == "__main__":
    fig_configs()
    fig_rout()
