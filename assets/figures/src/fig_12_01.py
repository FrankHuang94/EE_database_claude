#!/usr/bin/env python3
"""Figures for chapter 12-01 (differential pairs).

Run from anywhere:  python assets/figures/src/fig_12_01.py
Outputs SVGs to assets/figures/12-01/:
- transfer.svg: normalized current difference against differential input for a BJT pair (tanh) and a MOS
  pair with V_ov = 0.316 V (k_n = 2 mA/V^2, I_SS = 200 uA), each solved from its device equations with
  the tail constraint, with the small-signal (linear) slopes for comparison.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VT = 1.380649e-23 * 300 / 1.602176634e-19


def bjt_diff(vid):
    f = lambda ve: math.exp((vid / 2 - ve) / VT) + math.exp((-vid / 2 - ve) / VT) - 1.0
    ve = brentq(f, -2.0, 2.0, xtol=1e-15)
    return math.exp((vid / 2 - ve) / VT) - math.exp((-vid / 2 - ve) / VT)


def mos_diff(vid, kn=2e-3, iss=200e-6, vtn=0.5):
    sq = lambda vov: 0.5 * kn * max(vov, 0.0) ** 2
    f = lambda vs: sq(1.0 + vid / 2 - vs - vtn) + sq(1.0 - vid / 2 - vs - vtn) - iss
    vs = brentq(f, -5.0, 3.0, xtol=1e-15)
    return (sq(1.0 + vid / 2 - vs - vtn) - sq(1.0 - vid / 2 - vs - vtn)) / iss


def fig_transfer():
    x = np.linspace(-0.6, 0.6, 1201)
    b = np.array([bjt_diff(xi) for xi in x])
    m = np.array([mos_diff(xi) for xi in x])
    vov = math.sqrt(200e-6 / 2e-3)
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.plot(x * 1e3, b, color=PALETTE[0], lw=2, label="BJT pair: tanh(v_id / 2V_T)")
    ax.plot(x * 1e3, m, color=PALETTE[3], lw=2, label="MOS pair, V_ov = 0.316 V")
    ax.plot(x * 1e3, np.clip(x / (2 * VT), -1.2, 1.2), ":", color=PALETTE[0], lw=1, label="BJT small-signal slope")
    ax.plot(x * 1e3, np.clip(x / vov, -1.2, 1.2), ":", color=PALETTE[3], lw=1, label="MOS small-signal slope")
    for s in (-1, 1):
        ax.axvline(s * math.sqrt(2) * vov * 1e3, ls="--", color="0.5", lw=0.8)
    ax.text(math.sqrt(2) * vov * 1e3 + 8, 0.55, "±√2 V_ov", fontsize=8, color="0.3")
    ax.set_xlim(-600, 600)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlabel("differential input v_id (mV)")
    ax.set_ylabel("(i₁ − i₂) / tail current")
    ax.legend(fontsize=7.5, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/transfer.svg")


if __name__ == "__main__":
    fig_transfer()
