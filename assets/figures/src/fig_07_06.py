#!/usr/bin/env python3
"""Figures for chapter 07-06 (AC power and power factor).

Run from anywhere:  python assets/figures/src/fig_07_06.py
Outputs SVGs to assets/figures/07-06/: the waveforms of an RL load, the power triangle before and
after correction, and a rectifier's pulsed input current.
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

OUT = "assets/figures/07-06"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_rl_power():
    w = 2 * math.pi * 60
    Z = 10 + 1j * w * 0.02
    Vm = 120 * math.sqrt(2)
    I = Vm / Z
    t = np.linspace(0, 2 / 60, 4000)
    v = Vm * np.cos(w * t)
    i = abs(I) * np.cos(w * t + cmath.phase(I))
    p = v * i
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 4.4), sharex=True)
    axes[0].plot(t * 1e3, v, color=B, label="$v$ (V)")
    axes[0].plot(t * 1e3, i * 10, color=O, ls="--", label="$i$ ×10 (A)")
    axes[0].legend(fontsize=8, loc="upper right")
    axes[0].set_ylabel("V, A×10")
    axes[1].plot(t * 1e3, p, color=G, label="$p = vi$ (W)")
    axes[1].axhline(np.mean(p[:2000]), color="0.3", ls=":", label=f"average {np.mean(p[:2000]):.0f} W")
    axes[1].fill_between(t * 1e3, p, 0, where=p < 0, color=P, alpha=0.4, label="energy returned")
    axes[1].axhline(0, color="0.6", lw=0.6)
    axes[1].legend(fontsize=8, loc="upper right")
    axes[1].set_ylabel("W")
    axes[1].set_xlabel("time (ms)")
    fig.tight_layout()
    save(fig, f"{OUT}/rl-power.svg")


def fig_pf_correction():
    Pw = 14.0
    Q1 = 10 * math.tan(math.acos(0.75))
    Q2 = Pw * math.tan(math.acos(0.95))
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.annotate("", xy=(Pw, 0), xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": B, "lw": 1.8})
    ax.annotate("", xy=(Pw, Q1), xytext=(Pw, 0), arrowprops={"arrowstyle": "-|>", "color": O, "lw": 1.8})
    ax.annotate("", xy=(Pw, Q1), xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": "0.4", "lw": 1.4})
    ax.annotate("", xy=(Pw, Q2), xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": G, "lw": 1.8})
    ax.annotate("", xy=(Pw + 0.6, Q2), xytext=(Pw + 0.6, Q1), arrowprops={"arrowstyle": "-|>", "color": P, "lw": 1.8})
    ax.text(Pw / 2, -0.9, "P = 14 kW", ha="center", color=B)
    ax.text(Pw - 3.6, Q1 * 0.8, f"Q = {Q1:.2f} kvar", color=O, fontsize=9)
    ax.text(Pw + 0.9, (Q1 + Q2) / 2, f"capacitor\n−{Q1 - Q2:.2f} kvar", color=P, fontsize=9)
    ax.text(3.5, Q1 * 0.45, f"|S| = {math.hypot(Pw, Q1):.2f} kVA\n(PF {Pw / math.hypot(Pw, Q1):.3f})", color="0.3", fontsize=9)
    ax.text(6.5, Q2 * 0.15, f"|S| = {math.hypot(Pw, Q2):.2f} kVA (PF 0.95)", color=G, fontsize=9)
    ax.set_xlim(-0.5, 20)
    ax.set_ylim(-1.8, 10)
    ax.set_xlabel("real power (kW)")
    ax.set_ylabel("reactive power (kvar)")
    fig.tight_layout()
    save(fig, f"{OUT}/pf-correction.svg")


def fig_rectifier():
    f, T = 50.0, 0.02
    t = np.linspace(0, 2 * T, 8000)
    v = 230 * math.sqrt(2) * np.cos(2 * math.pi * f * t)
    W = 2.5e-3
    tm = np.mod(t, T)
    shape = ((np.abs(tm) < W / 2) | (np.abs(tm - T) < W / 2)).astype(float) - (np.abs(tm - T / 2) < W / 2).astype(float)
    Ip = 1.2619
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(t * 1e3, v, color=B, label="line voltage (V)")
    ax2 = ax.twinx()
    ax2.plot(t * 1e3, Ip * shape, color=O, label="input current (A)")
    ax2.plot(t * 1e3, 0.4348 * math.sqrt(2) * np.cos(2 * math.pi * f * t), color=O, ls=":", lw=0.9, label="its fundamental")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("V", color=B)
    ax2.set_ylabel("A", color=O)
    ax.set_ylim(-400, 400)
    ax2.set_ylim(-1.6, 1.6)
    ax2.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/rectifier-current.svg")


if __name__ == "__main__":
    fig_rl_power()
    fig_pf_correction()
    fig_rectifier()
    print("07-06 figures written to", OUT)
