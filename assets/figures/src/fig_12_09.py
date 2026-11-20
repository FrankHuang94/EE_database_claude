#!/usr/bin/env python3
"""Figures for chapter 12-09 (oscillators).

Run from anywhere:  python assets/figures/src/fig_12_09.py
Outputs SVGs to assets/figures/12-09/:
- wien-startup.svg: a Wien-bridge oscillator (R = 10 kohm, C = 10 nF, amplifier tanh(3.3 v)) starting from
  1 mV on the parallel capacitor, from its two state equations integrated with an adaptive Runge-Kutta
  method; the envelope grows exponentially and settles at the describing-function amplitude.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
R, C, G = 10e3, 10e-9, 3.3


def fig_startup():
    def rhs(t, x):
        vc1, vp = x
        i = (math.tanh(G * vp) - vc1 - vp) / R
        return [i / C, (i - vp / R) / C]

    sol = solve_ivp(rhs, (0, 0.015), [0.0, 1e-3], max_step=2e-6, rtol=1e-9, atol=1e-12)
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.plot(sol.t * 1e3, sol.y[1], color=PALETTE[0], lw=0.8)
    ax.axhline(0.1949, color=PALETTE[1], lw=0.9, ls="--")
    ax.axhline(-0.1949, color=PALETTE[1], lw=0.9, ls="--")
    ax.text(0.3, 0.21, "describing-function amplitude, 0.195 V", fontsize=8, color=PALETTE[1])
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("bridge output v_p (V)")
    ax.set_ylim(-0.26, 0.26)
    fig.tight_layout()
    save(fig, f"{OUT}/wien-startup.svg")


if __name__ == "__main__":
    fig_startup()
