#!/usr/bin/env python3
"""Figures for chapter 10-02 (MOSFET DC operation and biasing).

Run from anywhere:  python assets/figures/src/fig_10_02.py
Outputs SVGs to assets/figures/10-02/:
- mosfet-iv-loadlines.svg: square-law output characteristics of Example 10-02.1's NMOS (k = 2 mA/V^2,
  V_TN = 0.5 V) with the triode/saturation boundary and the load lines for R_D = 2 kOhm and 12 kOhm;
- bias-stability.svg: drain current against threshold shift for fixed-V_GS, source-degenerated and
  current-source bias (Examples 10-02.3 to 10-02.5).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def i_nmos(vgs, vds, k=2e-3, vt=0.5):
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    if vds < vov:
        return k * (vov * vds - vds**2 / 2)
    return 0.5 * k * vov**2


def fig_iv():
    vds = np.linspace(0, 3.3, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    for i, vgs in enumerate((0.8, 1.0, 1.2, 1.4)):
        ax.plot(vds, [i_nmos(vgs, x) * 1e3 for x in vds], color=PALETTE[i % len(PALETTE)],
                label=f"$V_{{GS}}$ = {vgs:.1f} V")
    vb = np.linspace(0, 0.95, 100)
    ax.plot(vb, 0.5 * 2e-3 * vb**2 * 1e3, color="0.4", ls=":", label="$V_{DS} = V_{ov}$ (region boundary)")
    for rd, ls in ((2e3, "--"), (12e3, "-.")):
        ax.plot(vds, (3.3 - vds) / rd * 1e3, color="k", ls=ls, lw=1, label=f"load line, $R_D$ = {rd/1e3:.0f} kΩ")
    for rd in (2e3, 12e3):
        x = brentq(lambda v: i_nmos(1.0, v) - (3.3 - v) / rd, 1e-6, 3.3)
        ax.plot(x, (3.3 - x) / rd * 1e3, "o", color="k", ms=5)
    ax.text(2.0, 0.30, "saturation", fontsize=8, color="0.3")
    ax.text(0.05, 0.85, "triode", fontsize=8, color="0.3")
    ax.set_xlim(0, 3.3)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("$V_{DS}$ (V)")
    ax.set_ylabel("$I_D$ (mA)")
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/mosfet-iv-loadlines.svg")


def fig_bias():
    dvt = np.linspace(-0.1, 0.1, 81)
    k, vt0, vg, rs = 4e-3, 0.5, 2.0, 1e3
    vgs_nom = brentq(lambda x: x + rs * 0.5 * k * (x - vt0) ** 2 - vg, vt0, vg)
    i_nom = 0.5 * k * (vgs_nom - vt0) ** 2
    fixed = [0.5 * k * (vgs_nom - vt0 - d) ** 2 / i_nom for d in dvt]
    deg = []
    for d in dvt:
        x = brentq(lambda v: v + rs * 0.5 * k * (v - vt0 - d) ** 2 - vg, vt0 + d, vg)
        deg.append(0.5 * k * (x - vt0 - d) ** 2 / i_nom)
    src = []
    i_ref0 = (3.3 - 0.85) / 10e3
    for d in dvt:
        x = brentq(lambda v: (3.3 - v) / 10e3 - 0.5 * 4e-3 * (v - vt0 - d) ** 2, vt0 + d, 3.3)
        src.append((3.3 - x) / 10e3 / i_ref0)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(dvt * 1e3, (np.array(fixed) - 1) * 100, color=PALETTE[0], label="fixed $V_{GS}$")
    ax.plot(dvt * 1e3, (np.array(deg) - 1) * 100, color=PALETTE[1], label="divider + $R_S$ = 1 kΩ")
    ax.plot(dvt * 1e3, (np.array(src) - 1) * 100, color=PALETTE[2], label="current-source reference (10 kΩ)")
    ax.axhline(0, color="0.6", lw=0.8)
    ax.set_xlabel("threshold shift $\\Delta V_{TN}$ (mV)")
    ax.set_ylabel("change in $I_D$ (%)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/bias-stability.svg")


if __name__ == "__main__":
    fig_iv()
    fig_bias()
