#!/usr/bin/env python3
"""Figures for chapter 07-11 (three-phase circuits).

Run from anywhere:  python assets/figures/src/fig_07_11.py
Outputs SVGs to assets/figures/07-11/: the Y phasor diagram with phase and line voltages, and the
instantaneous power of a single-phase load against a balanced three-phase load of the same power.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/07-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_phasors():
    fig, ax = plt.subplots(figsize=(5.0, 5.0))
    Vp = 1.0
    ph = {"a": Vp, "b": Vp * cmath.exp(-2j * math.pi / 3), "c": Vp * cmath.exp(2j * math.pi / 3)}
    for name, z in ph.items():
        ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": PALETTE[0], "lw": 1.8})
        ax.text(z.real * 1.12, z.imag * 1.12, f"$V_{{{name}n}}$", color=PALETTE[0], ha="center", va="center", fontsize=11)
    for (p, q) in (("a", "b"), ("b", "c"), ("c", "a")):
        z = ph[p] - ph[q]
        ax.annotate("", xy=(z.real, z.imag), xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": PALETTE[1], "lw": 1.4})
        ax.text(z.real * 1.08, z.imag * 1.08, f"$V_{{{p}{q}}}$", color=PALETTE[1], ha="center", va="center", fontsize=11)
    ax.text(0.95, 0.25, "30°", fontsize=9, color="0.3")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axhline(0, color="0.85", lw=0.6)
    ax.axvline(0, color="0.85", lw=0.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("phase voltages (blue) and line voltages (orange, ×√3)", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/y-phasors.svg")


def fig_power():
    t = np.linspace(0, 0.04, 2000)
    w = 2 * math.pi * 50
    P, pf = 12.8, 0.8
    S = P / pf
    th = math.acos(pf)
    single = P + S * np.cos(2 * w * t - th)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(t * 1e3, single, color=PALETTE[1], label="single phase, 12.8 kW at PF 0.8")
    for k in range(3):
        pk = P / 3 + S / 3 * np.cos(2 * w * t - th - 2 * k * 2 * math.pi / 3)
        ax.plot(t * 1e3, pk, color=PALETTE[0], lw=0.9, alpha=0.5, label="each of three phases" if k == 0 else None)
    ax.axhline(P, color=PALETTE[2], lw=2, label="three-phase total (constant)")
    ax.axhline(0, color="0.6", lw=0.6)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("instantaneous power (kW)")
    ax.set_ylim(-5, 42)
    ax.legend(fontsize=8, loc="upper center", ncol=3)
    fig.tight_layout()
    save(fig, f"{OUT}/instantaneous-power.svg")


if __name__ == "__main__":
    fig_phasors()
    fig_power()
