#!/usr/bin/env python3
"""Figures for chapter 11-01 (signals: classification and operations).

Run from anywhere:  python assets/figures/src/fig_11_01.py
Outputs SVGs to assets/figures/11-01/:
- signal-types.svg: a synthetic ECG-like waveform (a sum of Gaussian bumps, one beat per second) as (a) a
  continuous-time signal, (b) samples every 20 ms, (c) samples rounded to 3-bit levels over [-0.5, 1.25];
- time-ops.svg: Example 11-01.4, x(t) = r(t) - r(t-1) - u(t-2), then x(t+4), y(t) = x(4-2t) and the wrong-order
  result x(8-2t);
- impulse-limit.svg: unit-area pulses of width 1, 0.5, 0.25 and their running integrals approaching u(t);
- dt-sinusoids.svg: (a) cos(wn) for w = pi/8, pi/2, pi, 15pi/8; (b) 3 kHz and 7 kHz cosines sampled at 10 kHz.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def ecg(t):
    """A smooth, ECG-like beat once per second: P, Q, R, S and T bumps (arbitrary units)."""
    ph = np.mod(t, 1.0)
    bumps = [(0.2, 0.15, 0.025), (0.36, -0.12, 0.010), (0.40, 1.0, 0.012), (0.44, -0.25, 0.012),
             (0.68, 0.30, 0.040)]
    return sum(a * np.exp(-0.5 * ((ph - c) / w) ** 2) for c, a, w in bumps)


def step(t):
    return (t > 0).astype(float)


def ramp(t):
    return np.where(t > 0, t, 0.0)


def x_ex4(t):
    return ramp(t) - ramp(t - 1) - step(t - 2)


def fig_signal_types():
    t = np.linspace(0, 2, 4001)
    ts = np.arange(0, 2.0001, 0.02)
    xs = ecg(ts)
    lo, hi, levels = -0.5, 1.25, 8
    q = (hi - lo) / (levels - 1)
    xq = lo + np.round((xs - lo) / q) * q
    fig, axs = plt.subplots(3, 1, figsize=(7.0, 6.2), sharex=True)
    axs[0].plot(t, ecg(t), color=PALETTE[0])
    axs[0].set_title("(a) continuous time: x(t) defined at every instant")
    axs[1].stem(ts, xs, linefmt="C1-", markerfmt="C1o", basefmt=" ")
    axs[1].set_title("(b) discrete time: x[n] = x(nT$_s$), T$_s$ = 20 ms")
    axs[2].stem(ts, xq, linefmt="C2-", markerfmt="C2s", basefmt=" ")
    for k in range(levels):
        axs[2].axhline(lo + k * q, color="0.85", lw=0.6, zorder=0)
    axs[2].set_title("(c) digital: samples rounded to 8 levels (3 bits)")
    axs[2].set_xlabel("time (s)")
    for ax in axs:
        ax.set_ylabel("amplitude")
        ax.set_ylim(-0.6, 1.35)
    fig.tight_layout()
    save(fig, f"{OUT}/signal-types.svg")


def fig_time_ops():
    t = np.linspace(-5, 5, 10001)
    panels = [
        ("(a) x(t)", x_ex4(t)),
        ("(b) shift first: x(t + 4)", x_ex4(t + 4)),
        ("(c) then compress and reverse: y(t) = x(4 − 2t)", x_ex4(4 - 2 * t)),
        ("(d) wrong order: x(8 − 2t)", x_ex4(8 - 2 * t)),
    ]
    fig, axs = plt.subplots(4, 1, figsize=(7.0, 7.0), sharex=True)
    for ax, (title, y), c in zip(axs, panels, [PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]]):
        ax.plot(t, y, color=c)
        ax.set_title(title)
        ax.set_ylim(-0.2, 1.3)
        ax.axvline(0, color="0.6", lw=0.6)
        ax.set_yticks([0, 0.5, 1])
    axs[-1].set_xlabel("t (s)")
    fig.tight_layout()
    save(fig, f"{OUT}/time-ops.svg")


def fig_impulse_limit():
    t = np.linspace(-1.5, 1.5, 6001)
    fig, axs = plt.subplots(1, 2, figsize=(8.0, 3.4))
    for k, d in enumerate([1.0, 0.5, 0.25]):
        p = (step(t + d / 2) - step(t - d / 2)) / d
        run = np.clip((t + d / 2) / d, 0, 1)
        axs[0].plot(t, p, color=PALETTE[k], label=f"Δ = {d:g}")
        axs[1].plot(t, run, color=PALETTE[k], label=f"Δ = {d:g}")
    axs[1].plot(t, step(t), color="0.3", ls="--", label="u(t)")
    axs[0].set_title("(a) unit-area pulses p$_Δ$(t)")
    axs[1].set_title("(b) running integrals → u(t)")
    for ax in axs:
        ax.set_xlabel("t")
        ax.legend(loc="upper left", fontsize=8)
    axs[0].set_ylim(0, 4.5)
    axs[1].set_ylim(-0.1, 1.2)
    fig.tight_layout()
    save(fig, f"{OUT}/impulse-limit.svg")


def fig_dt_sinusoids():
    n = np.arange(0, 17)
    fig = plt.figure(figsize=(8.0, 6.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.25])
    ws = [(np.pi / 8, "π/8"), (np.pi / 2, "π/2"), (np.pi, "π"), (15 * np.pi / 8, "15π/8")]
    for k, (w, lab) in enumerate(ws):
        ax = fig.add_subplot(gs[k // 2, k % 2])
        ax.stem(n, np.cos(w * n), linefmt=f"C{k}-", markerfmt=f"C{k}o", basefmt=" ")
        ax.set_title(f"(a{k + 1}) cos({lab} · n)")
        ax.set_ylim(-1.2, 1.2)
        ax.set_xlabel("n")
    ax = fig.add_subplot(gs[2, :])
    fs = 10e3
    t = np.linspace(0, 1e-3, 4001)
    ns = np.arange(0, 11)
    ax.plot(t * 1e3, np.cos(2 * np.pi * 3e3 * t), color=PALETTE[0], label="3 kHz")
    ax.plot(t * 1e3, np.cos(2 * np.pi * 7e3 * t), color=PALETTE[1], lw=0.9, label="7 kHz")
    ax.plot(ns / fs * 1e3, np.cos(2 * np.pi * 3e3 * ns / fs), "ko", label="samples at 10 kHz")
    ax.set_title("(b) two CT cosines, one set of samples")
    ax.set_xlabel("time (ms)")
    ax.set_ylim(-1.3, 1.9)
    ax.legend(loc="upper center", fontsize=8, ncol=3)
    fig.tight_layout()
    save(fig, f"{OUT}/dt-sinusoids.svg")


if __name__ == "__main__":
    fig_signal_types()
    fig_time_ops()
    fig_impulse_limit()
    fig_dt_sinusoids()
