#!/usr/bin/env python3
"""Figures for chapter 12-06 (stability and frequency compensation).

Run from anywhere:  python assets/figures/src/fig_12_06.py
Outputs SVGs to assets/figures/12-06/:
- miller-loop-gain.svg: magnitude and unwrapped phase of Example 12-06.5's two-stage amplifier
  (g_m1 = 1 mA/V, R1 = 200 kohm, C1 = 0.2 pF, g_m2 = 10 mA/V, R2 = 50 kohm, C_L = 5 pF, C_c = 1.1 pF) used as a
  unity-gain buffer, with C_c alone and with the cancelling nulling resistor R_z = (1 + C_L/C_c)/g_m2, from
  complex nodal analysis of the two- and three-node circuits; the crossovers and phase margins are marked.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
GM1, R1, C1, GM2, R2, CL, CC = 1e-3, 200e3, 0.2e-12, 10e-3, 50e3, 5e-12, 1.1e-12
TP = 2 * math.pi


def gain(f, rz=0.0):
    s = 1j * TP * f
    yc = s * CC if rz == 0 else 1 / (rz + 1 / (s * CC))
    Y = np.array([[1 / R1 + s * C1 + yc, -yc], [GM2 - yc, 1 / R2 + s * CL + yc]])
    return np.linalg.solve(Y, np.array([-GM1, 0]))[1]


def fig_loop_gain():
    f = np.logspace(0, 10, 2000)
    fig, (am, ap) = plt.subplots(2, 1, figsize=(6.6, 5.0), sharex=True)
    for k, (rz, lab) in enumerate(((0.0, "C_c only"), ((1 + CL / CC) / GM2, "with R_z = 554.5 Ω"))):
        A = np.array([gain(x, rz) for x in f])
        ph = np.degrees(np.unwrap(np.angle(A)))
        fc = brentq(lambda x: abs(gain(x, rz)) - 1, 1e6, 1e10)
        pc = np.interp(math.log10(fc), np.log10(f), ph)
        col = PALETTE[0] if k == 0 else PALETTE[1]
        am.semilogx(f, 20 * np.log10(np.abs(A)), color=col, lw=1.8, label=lab)
        ap.semilogx(f, ph, color=col, lw=1.8)
        ap.plot([fc, fc], [-180, pc], color=col, lw=1.2, ls=":")
        ap.text(fc * 0.7, -205 - 25 * k, f"{lab}: PM = {180 + pc:.1f}° at {fc / 1e6:.1f} MHz", color=col,
                fontsize=8, ha="right")
        am.plot(fc, 0, "o", color=col, ms=4)
    am.axhline(0, color="0.5", lw=0.8)
    ap.axhline(-180, color="0.5", lw=0.8)
    am.set_ylabel("loop gain (dB)")
    am.set_ylim(-60, 110)
    am.legend(fontsize=8, loc="upper right")
    ap.set_ylabel("phase (°)")
    ap.set_ylim(-280, 10)
    ap.set_yticks([-270, -180, -90, 0])
    ap.set_xlabel("frequency (Hz)")
    fig.tight_layout()
    save(fig, f"{OUT}/miller-loop-gain.svg")


if __name__ == "__main__":
    fig_loop_gain()
