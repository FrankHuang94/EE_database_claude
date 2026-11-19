#!/usr/bin/env python3
"""Figures for chapter 09-03 (carrier transport: drift and diffusion).

Run from anywhere:  python assets/figures/src/fig_09_03.py
Outputs SVGs to assets/figures/09-03/:
- drift-diffusion.svg: (left) 2-D random walks of electrons with exponentially distributed free times,
  without and with a field (the field adds a small steady displacement; seeded, illustrative units);
  (right) diffusion from a narrow source: Gaussian profiles of width sqrt(2Dt) at three times;
- mobility-vs-doping.svg: electron and hole mobility of Si at 300 K against total impurity concentration,
  course model (handbook fit, Baccarani and Ostoja) and Hu's fit;
- velocity-field.svg: electron and hole drift velocity at 300 K against field from the Jacoboni et al. fits
  in the handbook, with the low-field lines v = mu0 * E.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def mun(N):
    return 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def mup(N):
    return 48 + 402 / (1 + (N / 6.3e16) ** 0.76)


def mun_hu(N):
    return 92 + 1318 / (1 + (N / 1e17) ** 0.85)


def mup_hu(N):
    return 50 + 420 / (1 + (N / 1.6e17) ** 0.7)


def vfit(F, vs, Fc, beta):
    return vs * (F / Fc) / (1 + (F / Fc) ** beta) ** (1 / beta)


def walk(rng, steps, push):
    pos = np.zeros((steps + 1, 2))
    for i in range(steps):
        t = rng.exponential(1.0)
        ang = rng.uniform(0, 2 * np.pi)
        pos[i + 1] = pos[i] + t * np.array([np.cos(ang), np.sin(ang)]) + np.array([push * t * t / 2, 0])
    return pos


def fig_drift_diffusion():
    rng = np.random.default_rng(3)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.6))
    for push, col, lab in ((0.0, "0.5", "no field"), (0.35, PALETTE[0], "with a field (net drift to the right)")):
        p = walk(rng, 60, push)
        a1.plot(p[:, 0], p[:, 1], color=col, lw=1, label=lab)
        a1.plot(p[-1, 0], p[-1, 1], "o", color=col, ms=4)
    a1.plot(0, 0, "k+", ms=8)
    a1.set_aspect("equal")
    a1.set_xticks([])
    a1.set_yticks([])
    a1.set_title("random thermal motion, with and without a field", fontsize=9)
    a1.legend(fontsize=7, loc="lower left")
    x = np.linspace(-6, 6, 400)
    for t, col in ((0.25, PALETTE[1]), (1.0, PALETTE[2]), (4.0, PALETTE[4])):
        sig = np.sqrt(2 * 1.0 * t)
        a2.plot(x, np.exp(-x**2 / (2 * sig**2)) / (sig * np.sqrt(2 * np.pi)), color=col, label=f"t = {t:g} (width √(2Dt) = {sig:.2f})")
    a2.set_xlabel("position (arb.)")
    a2.set_ylabel("concentration (arb.)")
    a2.set_title("diffusion from a narrow source (D = 1)", fontsize=9)
    a2.legend(fontsize=7)
    save(fig, f"{OUT}/drift-diffusion.svg")


def fig_mobility():
    N = np.logspace(14, 20, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogx(N, mun(N), color=PALETTE[0], label="electrons (course model)")
    ax.semilogx(N, mun_hu(N), color=PALETTE[0], ls="--", label="electrons (Hu)")
    ax.semilogx(N, mup(N), color=PALETTE[1], label="holes (course model)")
    ax.semilogx(N, mup_hu(N), color=PALETTE[1], ls="--", label="holes (Hu)")
    ax.set_xlabel("total impurity concentration $N_A + N_D$ (cm$^{-3}$)")
    ax.set_ylabel("mobility (cm$^2$/V·s)")
    ax.set_ylim(0, 1500)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/mobility-vs-doping.svg")


def fig_velocity():
    T = 300.0
    F = np.logspace(2, 5.5, 300)
    ve = vfit(F, 1.53e9 * T**-0.87, 1.01 * T**1.55, 2.57e-2 * T**0.66)
    vh = vfit(F, 1.62e8 * T**-0.52, 1.24 * T**1.68, 0.46 * T**0.17)
    mu0e = 1.53e9 * T**-0.87 / (1.01 * T**1.55)
    mu0h = 1.62e8 * T**-0.52 / (1.24 * T**1.68)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.loglog(F, ve, color=PALETTE[0], label="electrons")
    ax.loglog(F, vh, color=PALETTE[1], label="holes")
    ax.loglog(F, mu0e * F, color=PALETTE[0], ls=":", lw=0.9, label="constant mobility")
    ax.loglog(F, mu0h * F, color=PALETTE[1], ls=":", lw=0.9)
    ax.set_ylim(1e4, 3e7)
    ax.set_xlabel("electric field (V/cm)")
    ax.set_ylabel("drift velocity (cm/s)")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, f"{OUT}/velocity-field.svg")


if __name__ == "__main__":
    fig_drift_diffusion()
    fig_mobility()
    fig_velocity()
    print("09-03 figures written to", OUT)
