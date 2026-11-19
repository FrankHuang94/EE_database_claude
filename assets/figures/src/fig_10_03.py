#!/usr/bin/env python3
"""Figures for chapter 10-03 (BJT DC operation and biasing).

Run from anywhere:  python assets/figures/src/fig_10_03.py
Outputs SVGs to assets/figures/10-03/:
- bjt-output-loadline.svg: idealized output characteristics (I_C = beta I_B, saturation below about 0.2 V)
  for beta = 100, with the 2 kOhm load line of Example 10-03.1 and its operating points for beta = 100
  and 300;
- bias-vs-beta.svg: collector current against beta for fixed base-current bias, four-resistor bias and
  collector-to-base feedback bias (Examples 10-03.1, 10-03.3 and Problem 10-03.6).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def ic_curve(vce, ib, beta=100.0, vsat=0.2):
    """A smooth idealized output curve: active current beta*I_B, collapsing below about V_CE,sat."""
    return beta * ib * (1 - np.exp(-vce / (vsat / 3)))


def fig_output():
    vce = np.linspace(0, 5, 500)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    for i, ib in enumerate((5e-6, 13e-6, 20e-6, 26e-6)):
        ax.plot(vce, ic_curve(vce, ib) * 1e3, color=PALETTE[i % len(PALETTE)], label=f"$I_B$ = {ib*1e6:.0f} µA")
    ax.plot(vce, (5 - vce) / 2e3 * 1e3, color="k", ls="--", lw=1, label="load line, $R_C$ = 2 kΩ")
    ax.plot(2.4, 1.3, "o", color="k", ms=5)
    ax.annotate("β = 100: active, $V_{CE}$ = 2.4 V", (2.4, 1.3), (2.6, 1.9), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="0.4"))
    ax.plot(0.2, 2.4, "s", color="k", ms=5)
    ax.annotate("β = 300: saturated, $V_{CE}$ ≈ 0.2 V", (0.2, 2.4), (0.6, 2.8), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="0.4"))
    ax.axvspan(0, 0.3, color="0.9", zorder=0)
    ax.text(0.03, 0.15, "saturation", fontsize=8, color="0.3", rotation=90)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 3.2)
    ax.set_xlabel("$V_{CE}$ (V)")
    ax.set_ylabel("$I_C$ (mA)")
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/bjt-output-loadline.svg")


def fig_beta():
    beta = np.linspace(50, 300, 200)
    fixed = beta * 13e-6
    fixed = np.minimum(fixed, (5 - 0.2) / 2e3)
    vth, rth = 12 * 10 / 57, 47e3 * 10e3 / 57e3
    four = (vth - 0.7) / (1e3 + rth / (beta + 1)) * beta / (beta + 1)
    fb = (5 - 0.7) / (2e3 + 200e3 / (beta + 1)) * beta / (beta + 1)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(beta, fixed / fixed[np.argmin(abs(beta - 100))], color=PALETTE[0], label="fixed base current (Ex. 1)")
    ax.plot(beta, four / four[np.argmin(abs(beta - 100))], color=PALETTE[1], label="four-resistor (Ex. 3)")
    ax.plot(beta, fb / fb[np.argmin(abs(beta - 100))], color=PALETTE[2], label="collector feedback (Prob. 6)")
    ax.axvline(100, color="0.7", lw=0.8)
    ax.set_xlabel("β")
    ax.set_ylabel("$I_C$ relative to β = 100")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/bias-vs-beta.svg")


if __name__ == "__main__":
    fig_output()
    fig_beta()
