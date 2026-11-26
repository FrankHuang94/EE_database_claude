#!/usr/bin/env python3
"""Figures for chapter 25-03 (deposition, etch, CMP, implant, metrology).

Run from anywhere:  python assets/figures/src/fig_25_03.py
Outputs
  assets/figures/25-03/cvd-regimes.svg     CVD growth rate against 1000/T for Example 25-03.1's constants
                                           (ks = 0.05 cm/s at 650 C, Ea = 1.5 eV, hg = 2.0 cm/s), with both limits
  assets/figures/25-03/implant-anneal.svg  boron profile as implanted (1e15 cm^-2, Rp 30 nm, dRp 12 nm), after a 1 s spike at
                                           1050 C and after 30 min at 1000 C, with a reflecting surface; background 1e18
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import units as u  # noqa: E402

OUT = "assets/figures/25-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def cvd_regimes() -> None:
    tc = np.linspace(500, 1150, 400)
    ks = np.array([u.arrhenius(0.05, 650, 1.5, t) for t in tc])
    v = [u.cvd_rate_nm_min(k, 2.0, 3e16, 5e22) for k in ks]
    v_rx = [u.cvd_rate_nm_min(k, 1e9, 3e16, 5e22) for k in ks]
    v_tr = [u.cvd_rate_nm_min(1e9, 2.0, 3e16, 5e22) for _ in ks]
    x = 1000 / (tc + 273.15)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.semilogy(x, v, color=PALETTE[0], lw=2, label="growth rate")
    ax.semilogy(x, v_rx, color=PALETTE[1], ls="--", label="reaction limit (ks)")
    ax.semilogy(x, v_tr, color=PALETTE[2], ls=":", label="transport limit (hg)")
    for t in (650, 950):
        k = u.arrhenius(0.05, 650, 1.5, t)
        ax.plot(1000 / (t + 273.15), u.cvd_rate_nm_min(k, 2.0, 3e16, 5e22), "ko", ms=5)
        ax.annotate(f"{t} °C", (1000 / (t + 273.15), u.cvd_rate_nm_min(k, 2.0, 3e16, 5e22)),
                    textcoords="offset points", xytext=(6, -12), fontsize=8)
    ax.set_xlabel("1000/T (1/K)")
    ax.set_ylabel("growth rate (nm/min)")
    ax.set_ylim(1, 3000)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/cvd-regimes.svg")


def implant_anneal() -> None:
    x = np.arange(0, 600.25, 0.25)
    p0 = u.image_solution(x, 1e15, 30, 12, 0, 0)
    spike = u.image_solution(x, 1e15, 30, 12, u.boron_d(1050), 1.0)
    furn = u.image_solution(x, 1e15, 30, 12, u.boron_d(1000), 1800)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.semilogy(x, p0, color=PALETTE[0], label="as implanted")
    ax.semilogy(x, spike, color=PALETTE[2], ls="--", label="spike, 1050 °C, 1 s")
    ax.semilogy(x, furn, color=PALETTE[1], label="furnace, 1000 °C, 30 min")
    ax.axhline(1e18, color="0.5", ls=":")
    ax.text(300, 1.3e18, "background 10¹⁸ cm⁻³", fontsize=8)
    ax.set_xlim(0, 400)
    ax.set_ylim(1e16, 1e21)
    ax.set_xlabel("depth (nm)")
    ax.set_ylabel("boron concentration (cm⁻³)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/implant-anneal.svg")


if __name__ == "__main__":
    cvd_regimes()
    implant_anneal()
