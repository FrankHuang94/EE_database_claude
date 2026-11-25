#!/usr/bin/env python3
"""Figures for chapter 22-10 (datacenter power delivery).

Run from anywhere:  python assets/figures/src/fig_22_10.py
Outputs
  assets/figures/22-10/pdn.svg           Example 22-10.6's die-side impedance (2 pH package inductance, 20 µF die
                                         capacitance) against frequency for three ESR values, with the 250 µΩ target
                                         impedance (top), and the die-voltage deviation for a 100 A step (bottom)
  assets/figures/22-10/interleaving.svg  peak-to-peak ripple of the summed inductor currents, relative to one phase,
                                         against phase count N for D = 1/15 (12 V to 0.8 V) and D = 1/3; the ripple
                                         vanishes whenever N·D is an integer
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pdn  # noqa: E402

OUT = "assets/figures/22-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
L, C, DI = 2e-12, 20e-6, 100.0


def _z(f, r):
    s = 2j * np.pi * f
    zl, zc = s * L, r + 1 / (s * C)
    return zl * zc / (zl + zc)


def _droop(r, t):
    def f(_t, y):
        il, vc = y
        return [-(vc + r * (il - DI)) / L, (il - DI) / C]
    sol = integrate.solve_ivp(f, (0, t[-1]), [0, 0], t_eval=t, max_step=2e-12, rtol=1e-9, atol=1e-14)
    il, vc = sol.y
    return vc + r * (il - DI)


def fig_pdn():
    f = np.logspace(6, 9, 1500)
    t = np.linspace(0, 60e-9, 1500)
    fig, ax = plt.subplots(2, 1, figsize=(6.0, 5.6))
    for r, col in ((0.05e-3, PALETTE[0]), (0.17e-3, PALETTE[1]), (0.5e-3, PALETTE[2])):
        lab = f"ESR {r * 1e3:.2f} mΩ"
        ax[0].loglog(f, np.abs(_z(f, r)) * 1e6, color=col, label=lab)
        ax[1].plot(t * 1e9, _droop(r, t) * 1e3, color=col, label=lab)
    ax[0].axhline(250, color="0.4", ls="--", lw=1)
    ax[0].text(1.2e6, 280, "target 250 µΩ", fontsize=8)
    ax[0].set_xlabel("frequency (Hz)")
    ax[0].set_ylabel("|Z| seen from die (µΩ)")
    ax[0].legend(fontsize=8)
    ax[0].set_title("2 pH package, 20 µF die: resonance near 25 MHz", fontsize=10)
    ax[1].axhline(-25, color="0.4", ls="--", lw=1)
    ax[1].set_xlabel("time after a 100 A step (ns)")
    ax[1].set_ylabel("die voltage change (mV)")
    fig.tight_layout()
    save(fig, f"{OUT}/pdn.svg")


def fig_interleave():
    n = np.arange(1, 25)
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    for d, col, lab in ((1 / 15, PALETTE[0], "D = 1/15 (12 V → 0.8 V)"), (1 / 3, PALETTE[1], "D = 1/3")):
        one = pdn.phase_ripple(12, d, 100e-9, 1e6)
        rel = [pdn.summed_ripple(k, 12, d, 100e-9, 1e6) / one for k in n]
        ax.plot(n, rel, "o-", color=col, ms=3, label=lab)
    ax.set_xlabel("number of interleaved phases N")
    ax.set_ylabel("summed ripple / one phase")
    ax.legend(fontsize=8)
    ax.set_title("Interleaving cancels ripple fully only where N·D is an integer", fontsize=10)
    save(fig, f"{OUT}/interleaving.svg")


if __name__ == "__main__":
    fig_pdn()
    fig_interleave()
