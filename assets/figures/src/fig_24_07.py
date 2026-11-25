#!/usr/bin/env python3
"""Figures for chapter 24-07 (photonics fundamentals).

Run from anywhere:  python assets/figures/src/fig_24_07.py
Outputs
  assets/figures/24-07/modulators.svg   left: MZM cos^2 transfer against V/Vpi with quadrature bias and a half-Vpi drive;
                                        right: a Q = 10,000 ring notch at 1310 nm at 0, 1 and 2.3 K of heating
  assets/figures/24-07/sensitivity.svg  BER against average received power for OOK and PAM4 (0.9 A/W, 20 pA/rtHz, 30 GHz)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import optics  # noqa: E402

OUT = "assets/figures/24-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def modulators() -> None:
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.4))
    v = np.linspace(-1, 1, 400)  # V/Vpi relative to quadrature
    a1.plot(v, optics.mzm(math.pi / 2 + math.pi * v), color=PALETTE[0])
    a1.axvspan(-0.25, 0.25, color=PALETTE[1], alpha=0.15, label="drive: Vπ/2 peak to peak")
    a1.plot([0], [0.5], "o", color=PALETTE[1], label="quadrature bias")
    a1.set_xlabel("drive voltage relative to bias (units of Vπ)")
    a1.set_ylabel("Pout / Pin")
    a1.legend(fontsize=7, loc="upper right")
    a1.grid(True, alpha=0.3)
    lam = np.linspace(1309.7, 1310.45, 600)
    shift = 1310 * 1.8e-4 / 4.2
    for i, dt in enumerate((0, 1, 2.3)):
        a2.plot(lam, optics.ring_transmission(lam, 1310 + shift * dt, 1e4), color=PALETTE[i + 2], label=f"+{dt} K")
    a2.axvline(1310, color="0.5", ls=":", lw=1)
    a2.ticklabel_format(axis="x", useOffset=False)
    a2.set_xlabel("wavelength (nm)")
    a2.set_ylabel("transmission")
    a2.legend(fontsize=7, loc="lower left")
    a2.grid(True, alpha=0.3)
    save(fig, f"{OUT}/modulators.svg")


def sensitivity() -> None:
    r, sigma = 0.9, 20e-12 * math.sqrt(30e9)
    pdbm = np.linspace(-24, -6, 300)
    pw = 1e-3 * 10 ** (pdbm / 10)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.semilogy(pdbm, optics.ber_ook(pw, r, sigma), color=PALETTE[0], label="OOK")
    ax.semilogy(pdbm, optics.ber_pam4(pw, r, sigma), color=PALETTE[1], label="PAM4")
    for target, lab in ((1e-12, "1e-12"), (2.4e-4, "KP4 threshold 2.4e-4")):
        ax.axhline(target, color="0.6", ls=":", lw=1)
        ax.text(-23.5, target * 2, lab, fontsize=7, color="0.4")
    ax.set_ylim(1e-15, 1)
    ax.set_xlabel("average received power (dBm)")
    ax.set_ylabel("BER")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/sensitivity.svg")


if __name__ == "__main__":
    modulators()
    sensitivity()
