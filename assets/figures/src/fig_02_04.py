#!/usr/bin/env python3
"""Figures for chapter 02-04 (forced response and resonance).

Run:  python assets/figures/src/fig_02_04.py  -> assets/figures/02-04/*.svg
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
OUT = "assets/figures/02-04"
B, O, G, P, Y = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4]


def fig_bode():
    r = np.logspace(-1, 1, 800)
    fig, axes = plt.subplots(2, 1, figsize=(7.0, 6.0), sharex=True)
    for z, c in [(0.05, B), (0.25, O), (0.5, G), (0.707, P), (1.0, "k")]:
        h = 1 / (1 - r**2 + 2j * z * r)
        axes[0].semilogx(r, 20 * np.log10(abs(h)), color=c, lw=1.8, label=f"ζ = {z}")
        axes[1].semilogx(r, np.degrees(np.angle(h)), color=c, lw=1.8)
    axes[0].semilogx(r, np.where(r < 1, 0, -40 * np.log10(r)), color="0.6", ls="--", lw=1, label="asymptotes (0, −40 dB/dec)")
    axes[0].set_ylabel("|H| (dB)")
    axes[0].set_ylim(-40, 25)
    axes[0].legend(fontsize=8, ncol=2)
    axes[0].set_title("Second-order low-pass: capacitor voltage of a series RLC")
    axes[1].set_ylabel("phase (°)")
    axes[1].set_xlabel("ω / ω₀")
    axes[1].set_yticks([0, -45, -90, -135, -180])
    fig.tight_layout()
    save(fig, f"{OUT}/bode-second-order.svg")


def fig_bandpass():
    r = np.linspace(0.5, 1.6, 2000)
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    for Q, c in [(2, B), (10, O), (50, G)]:
        h = 1 / np.sqrt(1 + Q**2 * (r - 1 / r) ** 2)
        ax.plot(r, h, color=c, lw=1.8, label=f"Q = {Q}: bandwidth ω₀/{Q}")
    ax.axhline(1 / math.sqrt(2), color="0.5", ls="--", lw=1)
    ax.text(1.42, 0.73, "half power (1/√2)", fontsize=8, color="0.4")
    Q = 10
    r1 = math.sqrt(1 + 1 / (4 * Q * Q)) - 1 / (2 * Q)
    r2 = math.sqrt(1 + 1 / (4 * Q * Q)) + 1 / (2 * Q)
    ax.annotate("", xy=(r1, 0.69), xytext=(r2, 0.69), arrowprops=dict(arrowstyle="<->", color=O))
    ax.text((r1 + r2) / 2, 0.64, "ω₂ − ω₁ = ω₀/Q", color=O, ha="center", fontsize=8)
    ax.set_xlabel("ω / ω₀")
    ax.set_ylabel("|H| (current or resistor voltage)")
    ax.set_title("Band-pass response of a series RLC: Q sets the bandwidth")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/bandpass-q.svg")


def fig_buildup():
    w0 = 1.0
    t = np.linspace(0, 120, 6000)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    Q = 10
    z = 1 / (2 * Q)
    a = z * w0
    wd = w0 * math.sqrt(1 - z * z)
    # driven at w0 from rest: x'' + 2 a x' + w0^2 x = cos(w0 t); steady state = sin(w0 t)/(2 a w0)
    A = 1 / (2 * a * w0)
    xs = A * np.sin(w0 * t)
    xh = np.exp(-a * t) * (0 * np.cos(wd * t) - A * w0 / wd * np.sin(wd * t))
    ax.plot(t, xs + xh, color=B, lw=1.2, label="Q = 10, driven at ω₀ from rest")
    ax.plot(t, A * (1 - np.exp(-a * t)), color=B, ls="--", lw=1.2, label="envelope Q(1 − e^(−αt))")
    ax.plot(t, 0.5 * t * np.sin(w0 * t) / w0, color=O, lw=0.8, alpha=0.8, label="undamped (ζ = 0): (t/2ω₀) sin ω₀t")
    ax.set_ylim(-14, 14)
    ax.set_xlabel("ω₀t")
    ax.set_ylabel("response / static response")
    ax.set_title("Resonant build-up: amplitude grows to Q over about 2Q/ω₀ seconds")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/resonance-buildup.svg")


def fig_beats():
    w0, w = 10.0, 9.5
    t = np.linspace(0, 25, 8000)
    x = (np.cos(w * t) - np.cos(w0 * t)) / (w0**2 - w**2)
    env = 2 / (w0**2 - w**2) * np.abs(np.sin((w0 - w) * t / 2))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(t, x, color=B, lw=0.9, label="x(t), forced at 9.5 rad/s, ω₀ = 10 rad/s")
    ax.plot(t, env, color=O, ls="--", lw=1.4, label="envelope ±(2/(ω₀² − ω²)) sin((ω₀ − ω)t/2)")
    ax.plot(t, -env, color=O, ls="--", lw=1.4)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("x (m)")
    ax.set_title("Beats: forcing near an undamped resonance")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/beats.svg")


def fig_nfc():
    f0 = 13.56e6
    f = np.linspace(11.5e6, 15.6e6, 3000)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for Q, c, lab in [(28.4, B, "Q = 28.4 (R = 3 Ω)"), (8.0, G, "Q = 8 (R = 10.65 Ω)")]:
        h = 1 / np.sqrt(1 + Q**2 * (f / f0 - f0 / f) ** 2)
        ax.plot(f / 1e6, h, color=c, lw=1.8, label=lab)
    for fs in (f0 - 847.5e3, f0 + 847.5e3):
        ax.axvline(fs / 1e6, color=O, ls=":", lw=1.4)
    ax.text((f0 + 847.5e3) / 1e6 + 0.05, 0.9, "subcarrier\nsidebands\n±847.5 kHz", color=O, fontsize=8)
    ax.axhline(1 / math.sqrt(2), color="0.5", ls="--", lw=1)
    ax.set_xlabel("frequency (MHz)")
    ax.set_ylabel("relative response")
    ax.set_title("A 13.56 MHz antenna: high Q boosts the signal but cuts the data sidebands")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/nfc-tuning.svg")


if __name__ == "__main__":
    fig_bode()
    fig_bandpass()
    fig_buildup()
    fig_beats()
    fig_nfc()
