#!/usr/bin/env python3
"""Figures for chapter 22-02 (the buck converter in steady state).

Run from anywhere:  python assets/figures/src/fig_22_02.py
Outputs
  assets/figures/22-02/buck-ccm-waveforms.svg  inductor voltage, inductor current and capacitor current over two
                                              periods of Example 22-02.1's converter (12 V to 1.2 V, 10 A,
                                              600 kHz, 0.6 uH), small-ripple waveforms with the balanced areas shaded
  assets/figures/22-02/conversion-ratio.svg    the buck's conversion ratio against K = 2L/(R T_s) for D = 0.2,
                                              0.5 and 0.8, with the CCM-DCM boundary K = 1 - M
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import buck as bk  # noqa: E402

OUT = "assets/figures/22-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_ccm():
    vin, v, i, fs, ind = 12.0, 1.2, 10.0, 600e3, 0.6e-6
    d = v / vin
    ts = 1 / fs
    di = bk.ripple_current(v, d, fs, ind)
    t = np.linspace(0, 2 * ts, 4001)
    tau = np.mod(t, ts)
    on = tau < d * ts
    vl = np.where(on, vin - v, -v)
    il = np.where(on, i - di / 2 + (vin - v) / ind * tau, i + di / 2 - v / ind * (tau - d * ts))
    ic = il - i
    tus = t * 1e6
    fig, ax = plt.subplots(3, 1, figsize=(5.8, 5.6), sharex=True)
    ax[0].plot(tus, vl, color=PALETTE[0], lw=1.5)
    ax[0].fill_between(tus, 0, vl, where=on, color=PALETTE[0], alpha=0.25, step="pre")
    ax[0].fill_between(tus, 0, vl, where=~on, color=PALETTE[1], alpha=0.25, step="pre")
    ax[0].axhline(0, color="0.4", lw=0.8)
    ax[0].set_ylabel("v_L (V)")
    ax[0].text(0.35, 5.5, "(V_in − V)·D·T_s", fontsize=8, color=PALETTE[0])
    ax[0].text(0.75, 1.2, "−V·D'·T_s: equal area", fontsize=8, color=PALETTE[1])
    ax[1].plot(tus, il, color=PALETTE[2], lw=1.5)
    ax[1].axhline(i, color="0.5", ls=":", lw=1)
    ax[1].set_ylabel("i_L (A)")
    ax[1].text(0.25, i + 0.05, "I = 10 A", fontsize=8, color="0.35")
    ax[2].plot(tus, ic, color=PALETTE[3], lw=1.5)
    ax[2].fill_between(tus, 0, ic, where=ic > 0, color=PALETTE[3], alpha=0.25)
    ax[2].fill_between(tus, 0, ic, where=ic < 0, color="0.6", alpha=0.25)
    ax[2].axhline(0, color="0.4", lw=0.8)
    ax[2].set_ylabel("i_C (A)")
    ax[2].set_xlabel("time (µs), two periods")
    ax[0].set_title("Volt-second balance on L, charge balance on C", fontsize=10)
    save(fig, f"{OUT}/buck-ccm-waveforms.svg")


def fig_ratio():
    k = np.logspace(-3, 1, 800)
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    for d, col in ((0.2, PALETTE[0]), (0.5, PALETTE[1]), (0.8, PALETTE[2])):
        ax.semilogx(k, [bk.buck_ratio(d, kk) for kk in k], color=col, lw=1.6, label=f"D = {d}")
    m = np.linspace(0.01, 0.99, 200)
    ax.semilogx(1 - m, m, color="0.4", ls="--", lw=1, label="CCM–DCM boundary, K = 1 − M")
    ax.set_xlabel("K = 2L/(R·T_s)   (light load ←  → heavy load)")
    ax.set_ylabel("conversion ratio M = V/V_in")
    ax.set_ylim(0, 1.02)
    ax.set_title("In DCM the ratio depends on the load", fontsize=10)
    ax.legend(loc="lower left", fontsize=8)
    save(fig, f"{OUT}/conversion-ratio.svg")


if __name__ == "__main__":
    fig_ccm()
    fig_ratio()
