#!/usr/bin/env python3
"""Figures for chapter 01-01 (functions, models and units).

Run:  python assets/figures/src/fig_01_01.py  -> assets/figures/01-01/*.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/01-01"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_families():
    x = np.linspace(0.05, 4, 400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
    for y, lab, col in [(2 * x, "linear: 2x", B), (x**2, "power law: x²", O), (np.exp(x), "exponential: eˣ", G),
                        (np.log(x), "logarithm: ln x", P)]:
        a1.plot(x, y, color=col, label=lab)
    a1.set_ylim(-3, 20)
    a1.set_title("Linear axes")
    a1.legend(fontsize=8)
    a1.set_xlabel("x")
    t = np.linspace(0, 5, 200)
    a2.semilogy(t, np.exp(-t), color=G, label="e^(−t/τ) on semilog axes: a straight line")
    a2.set_xlabel("t / τ")
    a2.set_title("Semilog axes turn exponentials into lines")
    a2.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/function-families.svg")


def fig_diode():
    vt, i_s = 0.025852, 1e-14
    v = np.linspace(0, 0.75, 400)
    i = i_s * np.expm1(v / vt)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
    a1.plot(v, i * 1e3, color=B)
    a1.set_xlabel("V (V)")
    a1.set_ylabel("I (mA)")
    a1.set_ylim(0, 10)
    a1.set_title("Diode current, linear axes: looks like a 'turn-on' at ~0.6 V")
    a2.semilogy(v[1:], i[1:], color=B)
    for k in range(-12, -1, 2):
        a2.axhline(10.0**k, color="0.85", lw=0.6)
    a2.set_xlabel("V (V)")
    a2.set_ylabel("I (A)")
    a2.set_title("Semilog axes: a straight line, one decade per 59.5 mV")
    fig.tight_layout()
    save(fig, f"{OUT}/diode-semilog.svg")


def fig_powerlaw():
    v = np.array([0.6, 0.7, 0.8, 0.9, 1.0])
    p = np.array([0.130, 0.206, 0.307, 0.437, 0.600])
    n, lnk = np.polyfit(np.log(v), np.log(p), 1)
    vv = np.linspace(0.55, 1.05, 100)
    fig, ax = plt.subplots(figsize=(6.4, 4))
    ax.loglog(v, p, "o", color=O, label="synthetic measurements")
    ax.loglog(vv, np.exp(lnk) * vv**n, color=B, label=f"fit: P = {np.exp(lnk):.3f}·V^{n:.2f}")
    ax.set_xlabel("supply voltage V (V)")
    ax.set_ylabel("power P (W)")
    ax.set_title("A power law is a straight line on log–log axes\n(slope = exponent)")
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/power-law-fit.svg")


if __name__ == "__main__":
    fig_families()
    fig_diode()
    fig_powerlaw()
    print("01-01 figures written")
