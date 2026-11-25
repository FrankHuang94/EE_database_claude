#!/usr/bin/env python3
"""Figures for chapter 24-08 (silicon photonics and optical transceivers).

Run from anywhere:  python assets/figures/src/fig_24_08.py
Outputs
  assets/figures/24-08/coupling.svg  left: coupling from a 4.6 um fiber mode into a chip mode of radius w2;
                                     right: loss against lateral offset for matched modes of 1.5, 3.0 and 4.6 um
  assets/figures/24-08/bond.svg      |H| of a 50 ohm driver into a 20 fF ring through a 1 nH wire bond and a
                                     10 pH hybrid bond, with the 56.7 GHz Nyquist frequency of 113.4375 GBd
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import siph  # noqa: E402

OUT = "assets/figures/24-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def coupling() -> None:
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.4))
    w2 = np.logspace(-1, 1.2, 300)
    eta = np.array([siph.coupling(4.6, w) for w in w2])
    a1.semilogx(w2, 10 * np.log10(eta), color=PALETTE[0])
    for w, lab in ((0.5, "bare Si wire"), (1.5, "spot-size converter"), (4.6, "matched")):
        a1.plot([w], [10 * math.log10(siph.coupling(4.6, w))], "o", color=PALETTE[1])
        a1.annotate(lab, (w, 10 * math.log10(siph.coupling(4.6, w))), textcoords="offset points",
                    xytext=(6, -10), fontsize=7)
    a1.set_xlabel("chip mode radius w2 (µm)")
    a1.set_ylabel("coupling from fiber (dB)")
    a1.set_ylim(-25, 1)
    a1.grid(True, which="both", alpha=0.3)
    d = np.linspace(0, 3, 200)
    for i, w in enumerate((1.5, 3.0, 4.6)):
        a2.plot(d, [-10 * math.log10(siph.coupling(w, w, x)) for x in d], color=PALETTE[i + 2],
                label=f"matched w = {w} µm")
    a2.axhline(0.5, color="0.6", ls=":", lw=1)
    a2.set_xlabel("lateral offset (µm)")
    a2.set_ylabel("loss (dB)")
    a2.set_ylim(0, 6)
    a2.legend(fontsize=7)
    a2.grid(True, alpha=0.3)
    save(fig, f"{OUT}/coupling.svg")


def bond() -> None:
    f = np.logspace(9, 12, 2000)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for i, (lab, l) in enumerate((("1 nH wire bond", 1e-9), ("10 pH hybrid bond", 10e-12))):
        ax.semilogx(f / 1e9, 20 * np.log10(siph.rlc_mag(f, 50, l, 20e-15)), color=PALETTE[i], label=lab)
    ax.axvline(113.4375 / 2, color="0.5", ls="--", lw=1, label="Nyquist of 113.4375 GBd")
    ax.axhline(-3, color="0.7", ls=":", lw=1)
    ax.set_ylim(-20, 15)
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("|V_mod / V_drive| (dB)")
    ax.legend(fontsize=7, loc="lower left")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/bond.svg")


if __name__ == "__main__":
    coupling()
    bond()
