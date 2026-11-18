#!/usr/bin/env python3
"""Figures for chapter 03-01 (probability in EE language).

Run:  python assets/figures/src/fig_03_01.py  -> assets/figures/03-01/*.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/03-01"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_packet_error():
    n = 12_000
    p = np.logspace(-13, -2, 400)
    exact = -np.expm1(n * np.log1p(-p))          # 1 - (1 - p)^n without cancellation
    union = n * p
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(p, union, "--", color=O, label="union bound np")
    ax.loglog(p, exact, color=B, lw=2, label="exact 1 − (1 − p)ⁿ")
    ax.axhline(1, color="0.5", lw=0.8)
    for pp, lab in ((1e-12, "PCIe NRZ target"), (1e-6, "PCIe 6.0 FBER"), (1e-4, "")):
        ax.plot([pp], [-np.expm1(n * np.log1p(-pp))], "o", color="k", ms=4)
        if lab:
            ax.annotate(lab, (pp, -np.expm1(n * np.log1p(-pp))), xytext=(6, -14), textcoords="offset points", fontsize=8)
    ax.set_xlabel("bit error rate p")
    ax.set_ylabel("probability a 12,000-bit packet has an error")
    ax.set_ylim(1e-10, 3)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Rare errors add up linearly until np approaches 1 (Example 03-01.1)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/packet-error.svg")


def fig_defect_level():
    u = np.logspace(-6, -1, 400)                       # untested fraction 1 - T
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for Y, col in ((0.5, P), (0.8, B), (0.95, G)):
        dl = -np.expm1(u * np.log(Y)) * 1e6            # 1 - Y^(1-T), in ppm
        ax.loglog(u, dl, color=col, label=f"yield {Y:.0%}")
    for lvl in (100, 10):
        ax.axhline(lvl, color="0.5", lw=0.8, ls=":")
        ax.text(7e-2, lvl * 1.15, f"{lvl} ppm", fontsize=8, color="0.4", ha="left")
    ax.invert_xaxis()
    ax.set_xticks([1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6])
    ax.set_xticklabels(["90%", "99%", "99.9%", "99.99%", "99.999%", "99.9999%"])
    ax.set_xlabel("fault coverage T (each step right is ten times fewer untested faults)")
    ax.set_ylabel("defect level of shipped parts (ppm)")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("Williams–Brown: DL = 1 − Y^(1−T) ≈ (1 − T)·ln(1/Y) (Example 03-01.7)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/defect-level.svg")


def fig_tmr():
    R = np.linspace(0, 1, 501)
    tmr = 3 * R**2 - 2 * R**3
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(R, R, "--", color="0.5", label="single module")
    ax.plot(R, tmr, color=B, lw=2, label="TMR, perfect voter: 3R² − 2R³")
    ax.plot([0.5], [0.5], "o", color="k", ms=4)
    ax.annotate("break-even at R = 0.5", (0.5, 0.5), xytext=(0.55, 0.3), fontsize=8,
                arrowprops=dict(arrowstyle="-", color="0.5"))
    ax.set_xlabel("module reliability R over the mission")
    ax.set_ylabel("system reliability")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Majority voting helps only when each module is already good (Example 03-01.6)", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/tmr.svg")


if __name__ == "__main__":
    fig_packet_error()
    fig_defect_level()
    fig_tmr()
