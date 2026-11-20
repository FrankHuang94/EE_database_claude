#!/usr/bin/env python3
"""Figures for chapter 12-07 (output stages and power amplifiers).

Run from anywhere:  python assets/figures/src/fig_12_07.py
Outputs SVGs to assets/figures/12-07/:
- efficiency.svg: efficiency and transistor dissipation against output amplitude for a +/-15 V, 8 ohm stage:
  class A biased for full swing, ideal class B, and a class D model (two 85 mohm switches, 2.5 W fixed loss),
  by averaging the instantaneous powers over a sampled cycle.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VCC, RL = 15.0, 8.0
SIN = np.sin(2 * math.pi * (np.arange(4096) + 0.5) / 4096)


def powers(vop):
    vo = vop * SIN
    pl = np.mean(vo ** 2 / RL)
    return pl, 2 * VCC * VCC / RL, VCC * np.mean(np.abs(vo) / RL), pl + np.mean((vo / RL) ** 2) * 0.17 + 2.5


def fig_efficiency():
    a = np.linspace(0.05, VCC, 400)
    r = np.array([powers(x) for x in a])
    fig, (ae, ad) = plt.subplots(1, 2, figsize=(8.6, 3.4))
    for k, lab, col in ((1, "class A", PALETTE[3]), (2, "class B", PALETTE[0]), (3, "class D model", PALETTE[2])):
        ae.plot(a, 100 * r[:, 0] / r[:, k], color=col, lw=1.8, label=lab)
        ad.plot(a, r[:, k] - r[:, 0], color=col, lw=1.8, label=lab)
    xw = 2 * VCC / math.pi
    ad.axvline(xw, color="0.6", lw=0.8, ls="--")
    ad.text(xw * 1.02, 15, "class B worst\n2V_CC/π", fontsize=7.5, color="0.35")
    ae.axhline(100 * math.pi / 4, color="0.7", lw=0.8)
    ae.set_xlabel("output amplitude (V)")
    ae.set_ylabel("efficiency (%)")
    ae.set_ylim(0, 100)
    ae.legend(fontsize=8, loc="upper left")
    ad.set_xlabel("output amplitude (V)")
    ad.set_ylabel("dissipation (W)")
    ad.set_yscale("log")
    ad.set_ylim(0.1, 100)
    fig.tight_layout()
    save(fig, f"{OUT}/efficiency.svg")


if __name__ == "__main__":
    fig_efficiency()
