#!/usr/bin/env python3
"""Figures for chapter 01-07 (applications of integration).

Run:  python assets/figures/src/fig_01_07.py  -> assets/figures/01-07/*.svg
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

use_style()
OUT = "assets/figures/01-07"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_waveforms():
    t = np.linspace(0, 2, 2000)
    waves = [  # (name, samples, exact RMS, exact average)
        ("sine", np.sin(2 * np.pi * t), 1 / math.sqrt(2), 0.0),
        ("square", np.sign(np.sin(2 * np.pi * t)), 1.0, 0.0),
        ("triangle", 2 / np.pi * np.arcsin(np.sin(2 * np.pi * t)), 1 / math.sqrt(3), 0.0),
        ("PWM, D = 25 %", np.where((t % 1) < 0.25, 1.0, 0.0), 0.5, 0.25),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.0), sharey=True)
    for ax, (name, y, rms, avg) in zip(axes, waves):
        ax.plot(t, y, color=B)
        ax.axhline(rms, color=O, ls="--", label=f"RMS {rms:.3f}")
        ax.axhline(avg, color=G, ls=":", label=f"average {avg:.3f}")
        ax.set_title(name)
        ax.set_xlabel("t / T")
        ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/waveform-rms.svg")


def fig_ac_power():
    t = np.linspace(0, 2 / 60, 1000)
    w = 377.0
    v = 170 * np.cos(w * t)
    i = 10 * np.cos(w * t - np.pi / 6)
    p = v * i
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 4.6), sharex=True)
    a1.plot(t * 1e3, v, color=B, label="v (V)")
    a1.plot(t * 1e3, i * 10, color=O, label="i × 10 (A)")
    a1.legend(fontsize=8, loc="upper right", ncol=2)
    a1.set_ylim(-200, 290)
    a1.axhline(0, color="0.6", lw=0.8)
    a2.plot(t * 1e3, p, color="k", label="p = v·i (W)")
    a2.axhline(p.mean(), color=G, ls="--", label=f"average P = {0.5 * 1700 * math.cos(math.pi / 6):.1f} W")
    a2.axhline(0, color="0.6", lw=0.8)
    a2.set_ylim(-300, 2300)
    a2.legend(fontsize=8, loc="upper right", ncol=2)
    a2.set_xlabel("t (ms)")
    a1.set_title("Current lagging by 30°: power oscillates at 2ω around its average")
    fig.tight_layout()
    save(fig, f"{OUT}/ac-power.svg")


def fig_supercap():
    C = 10.0
    V = np.linspace(0, 2.7, 300)
    E = 0.5 * C * V**2
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(V, E, color=B)
    m = V >= 1.35
    ax.fill_between(V[m], E[m], 0.5 * C * 1.35**2, color=G, alpha=0.3, label="usable from 2.7 V to 1.35 V: 75 %")
    ax.axvline(1.35, color="0.5", ls=":")
    ax.set_xlabel("capacitor voltage (V)")
    ax.set_ylabel("stored energy ½CV² (J)")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("A 10 F supercapacitor: half the voltage leaves a quarter of the energy")
    fig.tight_layout()
    save(fig, f"{OUT}/supercap-energy.svg")


def fig_quantization():
    x = np.linspace(-0.5, 4.5, 1000)
    q = np.round(x)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(x, x, color="0.6", ls="--", label="ideal")
    a1.plot(x, q, color=B, label="quantized")
    a1.set_xlabel("input (LSB)")
    a1.set_ylabel("output code")
    a1.legend(fontsize=8)
    a1.set_title("A uniform quantizer")
    e = np.linspace(-0.5, 0.5, 2)
    a2.fill_between(e, [1, 1], color=O, alpha=0.4)
    a2.set_xlim(-1, 1)
    a2.set_ylim(0, 1.4)
    a2.set_xlabel("error (LSB)")
    a2.set_ylabel("probability density")
    a2.set_title("Error uniform on ±½ LSB: variance Δ²/12")
    fig.tight_layout()
    save(fig, f"{OUT}/quantization-noise.svg")


def fig_gaussian():
    x = np.linspace(-4, 4, 800)
    f = np.exp(-x**2 / 2) / math.sqrt(2 * math.pi)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(x, f, color=B)
    m = np.abs(x) <= 2
    ax.fill_between(x[m], f[m], color=G, alpha=0.3, label="within ±2σ: 95.45 %")
    ax.set_xlabel("(R − μ) / σ")
    ax.set_ylabel("probability density")
    ax.legend(fontsize=8)
    ax.set_title("Yield is an integral of the probability density")
    fig.tight_layout()
    save(fig, f"{OUT}/gaussian-yield.svg")


if __name__ == "__main__":
    fig_waveforms()
    fig_ac_power()
    fig_supercap()
    fig_quantization()
    fig_gaussian()
    print("01-07 figures written")
