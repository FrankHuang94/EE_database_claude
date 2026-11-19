#!/usr/bin/env python3
"""Figures for chapter 10-06 (MOS single-stage amplifiers).

Run from anywhere:  python assets/figures/src/fig_10_06.py
Outputs SVGs to assets/figures/10-06/:
- three-configurations.svg: common source (with optional R_S), common gate and common drain (source
  follower), each showing where the signal enters and leaves and which terminal is at signal ground;
- gain-limits.svg: (a) common-source gain magnitude against R_D for g_m = 2 mS, with and without r_o = 40 kOhm,
  approaching the intrinsic gain g_m r_o = 80; (b) source-follower gain against R_S for g_m = 2 mS, with and
  without body effect (chi = 0.2) and r_o = 40 kOhm, approaching 1/(1 + chi).
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

OUT = "assets/figures/10-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_configs():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # (a) common source with optional degeneration
    d += elm.Label().at((1.8, 6.0)).label("(a) common source", fontsize=13)
    d += (m := elm.NFet(bulk=False).right().reverse().at((2, 1.5)).anchor("gate"))
    d += elm.Line().at(m.gate).left().length(0.8)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Resistor().at(m.drain).up().length(1.6).label("$R_D$", loc="bottom")
    d += elm.Vdd().label("$V_{DD}$")
    d += elm.Line().at(m.drain).right().length(1.2)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Resistor().at(m.source).down().length(1.4).label("$R_S$ (optional)", loc="bottom")
    d += elm.Ground()
    # (b) common gate
    x0 = 7.5
    d += elm.Label().at((x0 + 1.5, 6.0)).label("(b) common gate", fontsize=13)
    d += (m2 := elm.NFet(bulk=False).right().reverse().at((x0 + 1.5, 1.5)).anchor("gate"))
    d += elm.Line().at(m2.gate).left().length(0.6)
    d += elm.Label().label("$V_B$ (signal ground)", loc="left", fontsize=10)
    d += elm.Resistor().at(m2.drain).up().length(1.6).label("$R_D$", loc="bottom")
    d += elm.Vdd().label("$V_{DD}$")
    d += elm.Line().at(m2.drain).right().length(1.2)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Line().at(m2.source).down().length(0.6)
    d += (n2 := elm.Dot())
    d += elm.SourceI().down().length(1.4).label("$I_{bias}$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(n2.center).right().length(1.4)
    d += elm.Dot(open=True).label("$v_{in}$", loc="right")
    # (c) common drain
    x1 = 15.5
    d += elm.Label().at((x1 + 1.8, 6.0)).label("(c) common drain (source follower)", fontsize=13)
    d += (m3 := elm.NFet(bulk=False).right().reverse().at((x1 + 1.5, 1.5)).anchor("gate"))
    d += elm.Line().at(m3.gate).left().length(0.8)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Line().at(m3.drain).up().length(1.6)
    d += elm.Vdd().label("$V_{DD}$ (signal ground)")
    d += elm.Line().at(m3.source).down().length(0.6)
    d += (n3 := elm.Dot())
    d += elm.SourceI().down().length(1.4).label("$I_{bias}$ or $R_S$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(n3.center).right().length(1.4)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d.save(str(ROOT / OUT / "three-configurations.svg"))


def fig_limits():
    gm, ro, chi = 2e-3, 40e3, 0.2
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.5))
    rd = np.logspace(2, 7, 400)
    a.loglog(rd, gm * rd, color=PALETTE[1], ls="--", label="$g_mR_D$ (no $r_o$)")
    a.loglog(rd, gm * rd * ro / (rd + ro), color=PALETTE[0], label="$g_m(R_D \\parallel r_o)$")
    a.axhline(gm * ro, color="0.6", ls=":")
    a.text(150, gm * ro * 1.3, "intrinsic gain $g_mr_o$ = 80", fontsize=8, color="0.3")
    a.set_ylim(0.1, 1e3)
    a.set_xlabel("$R_D$ ($\\Omega$)")
    a.set_ylabel("$|A_v|$")
    a.set_title("(a) common source", fontsize=10)
    a.legend(fontsize=8, loc="lower right")
    rs = np.logspace(1, 6, 400)

    def follower(rs_, with_body, with_ro):
        g = 1 / rs_
        if with_ro:
            g = g + 1 / ro
        if with_body:
            g = g + chi * gm
        req = 1 / g
        return gm * req / (1 + gm * req)

    b.semilogx(rs, follower(rs, False, False), color=PALETTE[1], ls="--", label="ideal: $g_mR_S/(1 + g_mR_S)$")
    b.semilogx(rs, follower(rs, True, True), color=PALETTE[0], label="with body effect and $r_o$")
    b.axhline(1 / (1 + chi), color="0.6", ls=":")
    b.text(12, 1 / (1 + chi) + 0.03, "$1/(1 + \\chi)$ = 0.833", fontsize=8, color="0.3")
    b.set_ylim(0, 1.05)
    b.set_xlabel("$R_S$ ($\\Omega$)")
    b.set_ylabel("$v_{out}/v_{in}$")
    b.set_title("(b) source follower", fontsize=10)
    b.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/gain-limits.svg")


if __name__ == "__main__":
    fig_configs()
    fig_limits()
