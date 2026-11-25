#!/usr/bin/env python3
"""Figures for chapter 24-03 (SerDes architecture and equalization).

Run from anywhere:  python assets/figures/src/fig_24_03.py
Outputs
  assets/figures/24-03/ctle.svg               |H| of the source-degenerated CTLE of Example 24-03.4 with its 40 fF
                                              load and without the output pole, with zero, poles and peak marked
  assets/figures/24-03/equalized-cursors.svg  cursors of the 24-02 channel unequalized, after the zero-forcing
                                              three-tap TX FFE, and after a two-tap DFE
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import serdes  # noqa: E402

OUT = "assets/figures/24-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
GM, RD, RS, CL = 20e-3, 200.0, 400.0, 40e-15
CS = 1 / (2 * np.pi * RS * 2e9)
H = {-1: 0.02156, 0: 0.73402, 1: 0.21088, 2: 0.02967, 3: 0.00345, 4: 0.00037}


def ctle() -> None:
    f = np.logspace(8, 11, 1500)
    real = serdes.ctle(f, GM, RD, RS, CS, CL)
    ideal = serdes.ctle(f, GM, RD, RS, CS, 0.0)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.semilogx(f / 1e9, 20 * np.log10(real), color=PALETTE[0], label="with 40 fF load (output pole 19.9 GHz)")
    ax.semilogx(f / 1e9, 20 * np.log10(ideal), "--", color=PALETTE[1], label="without the output pole")
    i = real.argmax()
    ax.plot(f[i] / 1e9, 20 * np.log10(real[i]), "o", color=PALETTE[0])
    ax.annotate(f"peak {20*np.log10(real[i]):.2f} dB at {f[i]/1e9:.1f} GHz", (f[i] / 1e9, 20 * np.log10(real[i])),
                textcoords="offset points", xytext=(-150, 8), fontsize=8)
    for fx, lab in ((2, "zero 2 GHz"), (10, "pole 10 GHz")):
        ax.axvline(fx, color="0.6", ls=":", lw=1)
        ax.text(fx * 1.05, -8, lab, fontsize=7, color="0.4")
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("gain (dB)")
    ax.set_ylim(-10, 15)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/ctle.svg")


def cursors() -> None:
    c = serdes.zf_ffe(H, 1, 1)
    g = serdes.convolve_cursors(c, H)
    dfe = {k: (0.0 if k in (1, 2) else x) for k, x in H.items()}
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.0), sharey=True)
    for ax, data, title in ((axes[0], H, f"unequalized (NRZ eye {serdes.eye(H):.3f})"),
                            (axes[1], g, f"3-tap TX FFE ({serdes.eye(g):.3f})"),
                            (axes[2], dfe, f"2-tap DFE ({serdes.eye(H, skip=(0, 1, 2)):.3f})")):
        ks = np.arange(-2, 5)
        vals = [data.get(int(k), 0.0) for k in ks]
        ax.bar(ks, vals, color=[PALETTE[0] if k == 0 else PALETTE[1] for k in ks], width=0.6)
        ax.axhline(0, color="0.3", lw=0.8)
        ax.set_title(title, fontsize=8)
        ax.set_xlabel("cursor k")
        ax.grid(True, axis="y", alpha=0.3)
    axes[0].set_ylabel("amplitude (fraction of swing)")
    save(fig, f"{OUT}/equalized-cursors.svg")


if __name__ == "__main__":
    ctle()
    cursors()
