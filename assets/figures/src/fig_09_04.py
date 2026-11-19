#!/usr/bin/env python3
"""Figures for chapter 09-04 (generation, recombination and the continuity equation).

Run from anywhere:  python assets/figures/src/fig_09_04.py
Outputs SVGs to assets/figures/09-04/:
- recombination-paths.svg: schematic band diagram with the three recombination paths: band-to-band
  (radiative, photon emitted), trap-assisted via a mid-gap level (Shockley-Read-Hall, energy to phonons) and
  Auger (energy handed to a third carrier);
- minority-profiles.svg: (left) steady excess-hole profiles for injection into a long region
  (exp(-x/L_p), L_p = 33.5 um) and into a short region ending at an ohmic contact at W = 5 um, solved as a
  boundary-value problem; (right) decay of the excess after a light pulse, exp(-t/tau) with tau = 10 us.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_paths():
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    Ec, Ev = 1.0, 0.0
    for y, lab in ((Ec, "$E_C$"), (Ev, "$E_V$")):
        ax.plot([0, 9], [y, y], color="k", lw=1.2)
        ax.text(9.1, y - 0.02, lab, fontsize=9)
    arrow = dict(arrowstyle="->", lw=1.3)
    # radiative
    ax.plot(1, Ec + 0.05, "o", color=PALETTE[0], ms=7)
    ax.plot(1, Ev - 0.05, "o", mfc="white", mec=PALETTE[1], ms=7)
    ax.annotate("", xy=(1, Ev + 0.03), xytext=(1, Ec - 0.03), arrowprops=arrow)
    ax.annotate("photon", xy=(2.4, 0.78), xytext=(1.2, 0.42), fontsize=8, color=PALETTE[4],
                arrowprops=dict(arrowstyle="->", color=PALETTE[4], lw=1.3, connectionstyle="arc3,rad=-0.3"))
    ax.text(0.2, -0.32, "band-to-band\n(radiative)", fontsize=8)
    # SRH
    ax.plot([3.8, 5.0], [0.5, 0.5], color=PALETTE[2], lw=3)
    ax.text(5.1, 0.47, "$E_t$", fontsize=9)
    ax.plot(4.0, Ec + 0.05, "o", color=PALETTE[0], ms=7)
    ax.annotate("", xy=(4.0, 0.53), xytext=(4.0, Ec - 0.03), arrowprops=arrow)
    ax.plot(4.8, Ev - 0.05, "o", mfc="white", mec=PALETTE[1], ms=7)
    ax.annotate("", xy=(4.8, Ev + 0.03), xytext=(4.8, 0.47), arrowprops=arrow)
    ax.text(3.4, -0.32, "trap-assisted (SRH)\nenergy to phonons", fontsize=8)
    # Auger
    ax.plot(7.0, Ec + 0.05, "o", color=PALETTE[0], ms=7)
    ax.plot(7.6, Ec + 0.05, "o", color=PALETTE[0], ms=7)
    ax.plot(7.0, Ev - 0.05, "o", mfc="white", mec=PALETTE[1], ms=7)
    ax.annotate("", xy=(7.0, Ev + 0.03), xytext=(7.0, Ec - 0.03), arrowprops=arrow)
    ax.annotate("", xy=(7.6, Ec + 0.45), xytext=(7.6, Ec + 0.08), arrowprops=arrow)
    ax.text(7.75, Ec + 0.3, "third carrier\nkicked up", fontsize=8)
    ax.text(6.4, -0.32, "Auger", fontsize=8)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.45, 1.6)
    ax.axis("off")
    save(fig, f"{OUT}/recombination-paths.svg")


def bvp(L, W, n=2001):
    """Solve D p'' = p/tau on [0, W] with p(0) = 1, p(W) = 0 by finite differences (lengths in units of um)."""
    x = np.linspace(0, W, n)
    h = x[1] - x[0]
    A = np.zeros((n, n))
    b = np.zeros(n)
    A[0, 0] = A[-1, -1] = 1.0
    b[0] = 1.0
    for i in range(1, n - 1):
        A[i, i - 1] = A[i, i + 1] = 1 / h**2
        A[i, i] = -2 / h**2 - 1 / L**2
    return x, np.linalg.solve(A, b)


def fig_profiles():
    L = 33.5
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.4))
    xl, pl = bvp(L, 8 * L)
    a1.plot(xl, pl, color=PALETTE[0], label=f"long region, $L_p$ = {L} µm")
    xs, ps = bvp(L, 5.0, 501)
    a1.plot(xs, ps, color=PALETTE[1], label="short region, contact at 5 µm")
    a1.axvline(L, color="0.6", ls=":", lw=0.8)
    a1.set_xlim(0, 120)
    a1.set_xlabel("x (µm)")
    a1.set_ylabel("Δp(x)/Δp(0)")
    a1.legend(fontsize=8)
    t = np.linspace(0, 60, 400)
    a2.plot(t, np.exp(-t / 10), color=PALETTE[2])
    a2.axhline(0.01, color="0.6", ls=":", lw=0.8)
    a2.set_xlabel("time after the light pulse (µs)")
    a2.set_ylabel("Δp(t)/Δp(0)")
    a2.set_title("photoconductive decay, τ = 10 µs", fontsize=9)
    save(fig, f"{OUT}/minority-profiles.svg")


if __name__ == "__main__":
    fig_paths()
    fig_profiles()
    print("09-04 figures written to", OUT)
