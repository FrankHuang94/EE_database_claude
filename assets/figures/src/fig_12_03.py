#!/usr/bin/env python3
"""Figures for chapter 12-03 (frequency response: capacitances, Miller effect, poles and zeros).

Run from anywhere:  python assets/figures/src/fig_12_03.py
Outputs SVGs to assets/figures/12-03/:
- cs-bode.svg: Example 12-03.2's common-source stage (g_m = 1 mA/V, C_gs = 72.67 fF, C_gd = 6 fF,
  R_S = 10 kohm, R_L = 20 kohm, C_L = 100 fF): the exact magnitude response from the two-node nodal
  equations, against single-pole responses at the Miller input pole and at 1/(2 pi b1).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
GM, CGS, CGD, RS, RL, CL = 1e-3, 2 / 3 * 20 * 0.5 * 10e-15 + 6e-15, 6e-15, 10e3, 20e3, 100e-15


def h_exact(f):
    """Solve the gate and drain node equations at each frequency."""
    s = 2j * math.pi * f
    Y = np.array([[1 / RS + s * (CGS + CGD), -s * CGD], [GM - s * CGD, 1 / RL + s * (CGD + CL)]])
    return np.linalg.solve(Y, np.array([1 / RS, 0]))[1]


def fig_cs_bode():
    f = np.logspace(6, 11.3, 800)
    a0 = abs(h_exact(1.0))
    ex = np.array([abs(h_exact(x)) for x in f])
    cm = CGS + CGD * (1 + GM * RL)
    fm = 1 / (2 * math.pi * RS * cm)
    b1 = RS * cm + RL * (CGD + CL)
    fb = 1 / (2 * math.pi * b1)
    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    ax.semilogx(f, 20 * np.log10(ex), color=PALETTE[0], lw=2, label="exact (two nodes)")
    ax.semilogx(f, 20 * np.log10(a0 / np.abs(1 + 1j * f / fm)), "--", color=PALETTE[3], lw=1.3,
                label=f"Miller input pole only ({fm / 1e6:.1f} MHz)")
    ax.semilogx(f, 20 * np.log10(a0 / np.abs(1 + 1j * f / fb)), ":", color=PALETTE[2], lw=1.6,
                label=f"dominant pole 1/(2πb₁) ({fb / 1e6:.2f} MHz)")
    ax.axhline(20 * math.log10(a0 / math.sqrt(2)), color="0.6", lw=0.8)
    fz = GM / (2 * math.pi * CGD)
    for x, lab in ((350.0e6, "second pole\n350 MHz"), (fz, "RHP zero\n26.5 GHz")):
        ax.axvline(x, color="0.5", lw=0.8, ls="-.")
        ax.text(x * 1.12, 8, lab, fontsize=7.5, color="0.3")
    ax.set_xlim(1e6, 2e11)
    ax.set_ylim(-45, 32)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|V_o / V_s| (dB)")
    ax.legend(fontsize=7.5, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/cs-bode.svg")


if __name__ == "__main__":
    fig_cs_bode()
