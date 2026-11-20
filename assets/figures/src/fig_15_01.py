#!/usr/bin/env python3
"""Figure for chapter 15-01 (modeling dynamic systems).

Run from anywhere:  python assets/figures/src/fig_15_01.py
Outputs assets/figures/15-01/thermal.svg: left, Example 15-01.3's two-node junction and case temperatures after a
100 W step, on a logarithmic time axis; right, Example 15-01.4's heat balance, the leakage-dependent heat
generated against the heat removed for R = 0.5 K/W and the critical 0.628 K/W. Uses labs/15-01-lab/plants.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import plants  # noqa: E402

OUT = "assets/figures/15-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_thermal():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
    A, B = plants.thermal_two_node(0.15, 0.35, 5.0, 300.0)
    ts = np.logspace(-2, 3.2, 400)
    xs = np.array([plants.step(A, B, 100.0, t) for t in ts])
    a1.semilogx(ts, 30 + xs[:, 0], color=PALETTE[0], label="junction $T_J$")
    a1.semilogx(ts, 30 + xs[:, 1], color=PALETTE[1], label="case / heat sink $T_C$")
    a1.axhline(80, color="gray", lw=0.6, ls=":")
    a1.annotate("fast: τ ≈ 0.74 s (≈ $R_{JC}C_J$)", (0.8, 42), fontsize=7)
    a1.annotate("slow: τ ≈ 107 s (≈ $R_{CA}C_H$)", (60, 52), fontsize=7)
    a1.set_xlabel("time after the 100 W step (s)")
    a1.set_ylabel("temperature (°C)")
    a1.set_title("Two thermal time scales", fontsize=9)
    a1.legend(fontsize=7, loc="upper left")

    T = np.linspace(25, 140, 400)
    gen = 60 + 5 * np.exp((T - 25) / 30)
    a2.plot(T, gen, color=PALETTE[2], label="heat generated $P_d + P_L(T)$")
    for Rth, ls in ((0.5, "-"), (0.628, "--")):
        a2.plot(T, (T - 25) / Rth, color=PALETTE[0], ls=ls, label=f"heat removed, R = {Rth} K/W")
    for Teq, mk in ((64.25, "o"), (124.9, "s")):
        a2.plot(Teq, (Teq - 25) / 0.5, marker=mk, color="black", ms=5, ls="none")
    a2.annotate("stable", (64.25, (64.25 - 25) / 0.5), textcoords="offset points", xytext=(6, -12), fontsize=7)
    a2.annotate("unstable", (124.9, (124.9 - 25) / 0.5), textcoords="offset points", xytext=(-48, 6), fontsize=7)
    a2.set_xlabel("chip temperature T (°C)")
    a2.set_ylabel("heat flow (W)")
    a2.set_ylim(0, 250)
    a2.set_title("Leakage feedback: equilibria and runaway", fontsize=9)
    a2.legend(fontsize=7, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/thermal.svg")


if __name__ == "__main__":
    fig_thermal()
