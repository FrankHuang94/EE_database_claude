#!/usr/bin/env python3
"""Figures for chapter 12-04 (high-frequency analysis methods).

Run from anywhere:  python assets/figures/src/fig_12_04.py
Outputs SVGs to assets/figures/12-04/:
- pole-splitting.svg: the two poles of Example 12-04.4's two-stage amplifier (R1 = 50 kohm, C1 = 50 fF,
  g_m2 = 4 mA/V, R2 = 12.5 kohm, C2 = 1 pF) against the compensation capacitance, from the generalized
  eigenvalues of the two-node circuit, with the right-half-plane zero g_m2/(2 pi C_c) for reference.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigvals

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
R1, C1, GM2, R2, C2 = 50e3, 50e-15, 4e-3, 12.5e3, 1e-12


def poles(cc):
    G = np.array([[1 / R1, 0.0], [GM2, 1 / R2]])
    C = np.array([[C1 + cc, -cc], [-cc, C2 + cc]])
    lam = eigvals(G, -C)
    return np.sort(np.abs(lam.real)) / (2 * math.pi)


def fig_pole_splitting():
    cc = np.logspace(-16, -11, 300)
    p = np.array([poles(c) for c in cc])
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.loglog(cc * 1e12, p[:, 0], color=PALETTE[0], lw=2, label="lower pole")
    ax.loglog(cc * 1e12, p[:, 1], color=PALETTE[3], lw=2, label="upper pole")
    ax.loglog(cc * 1e12, GM2 / (2 * math.pi * cc), ":", color="0.4", lw=1.2, label="RHP zero g_m2/(2πC_c)")
    for f0, lab in ((1 / (2 * math.pi * R1 * C1), "node 1 alone"), (1 / (2 * math.pi * R2 * C2), "node 2 alone")):
        ax.axhline(f0, color="0.7", lw=0.8)
        ax.text(1.4, f0 * 1.15, lab, fontsize=7.5, color="0.4")
    ax.axvline(1.0, color="0.6", lw=0.8, ls="--")
    ax.set_xlim(1e-4, 10)
    ax.set_ylim(5e3, 1e11)
    ax.set_xlabel("compensation capacitance C_c (pF)")
    ax.set_ylabel("frequency (Hz)")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/pole-splitting.svg")


if __name__ == "__main__":
    fig_pole_splitting()
