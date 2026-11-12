#!/usr/bin/env python3
"""Figures for chapter 00-02 (the abstraction stack).

Run:  python assets/figures/src/fig_00_02.py   -> assets/figures/00-02/*.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/00-02"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
C0 = 299_792_458.0


def fig_lumped_regime():
    f = np.logspace(1, 12, 500)
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    for v, lab, col in [(C0, "free space (v = c)", B), (C0 / 2, "circuit board (v ≈ c/2)", O)]:
        ax.loglog(f, v / f / 10, color=col, label=f"λ/10 in {lab}")
    sizes = [(1e5, "100 km power line"), (1.0, "1 m cable"), (0.15, "15 cm board trace"),
             (0.02, "2 cm chip"), (2e-3, "2 mm on-chip wire")]
    for L, lab in sizes:
        ax.axhline(L, color="0.75", lw=0.8, ls=":")
        ax.text(1.3e1, L * 1.15, lab, fontsize=8, color="0.3")
    ax.set_xlabel("signal frequency (Hz)")
    ax.set_ylabel("largest size treatable as lumped (m)")
    ax.set_title("The lumped-circuit abstraction holds below the line\n(rule of thumb: size < λ/10)")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_ylim(1e-4, 1e7)
    save(fig, f"{OUT}/lumped-regime.svg")


def fig_regeneration():
    rng = np.random.default_rng(7)
    n_stages, n_sig, sigma = 30, 400, 0.12
    bits = rng.integers(0, 2, n_sig).astype(float)
    analog = bits.copy()
    digital = bits.copy()
    a_hist, d_err = [], []
    for _ in range(n_stages):
        analog = analog + rng.normal(0, sigma, n_sig)
        noisy = digital + rng.normal(0, sigma, n_sig)
        digital = (noisy > 0.5).astype(float)
        a_hist.append(analog.copy())
        d_err.append(np.mean(digital != bits))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))
    for k, col in [(0, B), (9, O), (29, P)]:
        ax1.hist(a_hist[k], bins=60, alpha=0.55, color=col, label=f"after {k + 1} stage{'s' if k else ''}")
    ax1.set_xlabel("analog value received (V) for sent 0 V or 1 V")
    ax1.set_ylabel("count")
    ax1.set_title("Analog chain: noise accumulates (σ grows as √N)")
    ax1.legend(fontsize=8)
    ax2.plot(range(1, n_stages + 1), np.array(d_err) * 100, "o-", color=G, ms=3)
    ax2.set_xlabel("number of stages N")
    ax2.set_ylabel("bit errors (%)")
    ax2.set_ylim(-0.5, 5)
    ax2.set_title("Digital chain: each stage re-decides 0 or 1\n(errors stay ~0 while σ ≪ distance to threshold)")
    fig.tight_layout()
    save(fig, f"{OUT}/regeneration.svg")


def far_end(t, rs, z0=50.0, td=1e-9, t_rise=10e-12, n=200):
    """Far-end voltage of an open-ended lossless line driven by a ramped 1 V step (lattice sum)."""
    gs, tau_s = (rs - z0) / (rs + z0), z0 / (rs + z0)
    x = lambda tt: np.clip(tt / t_rise, 0, 1)  # noqa: E731
    return sum(2 * tau_s * gs**k * x(t - (2 * k + 1) * td) for k in range(n))


def fig_tline():
    t = np.linspace(0, 20e-9, 4000)
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.plot(t * 1e9, np.clip(t / 10e-12, 0, 1), color="0.6", lw=1, label="source step (10 ps edge)")
    ax.plot(t * 1e9, far_end(t, 10.0), color=O, lw=2, label="far end, fast edge (line ≫ edge): rings")
    t2 = np.linspace(0, 120e-9, 4000)
    ax.plot(t2 * 1e9, far_end(t2, 10.0, t_rise=50e-9), color=B, lw=2, label="far end, 50 ns edge: looks lumped")
    ax.set_xlim(0, 60)
    ax.set_xlabel("t (ns)")
    ax.set_ylabel("V")
    ax.set_title("A 1 ns transmission line, open at the far end, driven through 10 Ω")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, f"{OUT}/tline-bounce.svg")


if __name__ == "__main__":
    fig_lumped_regime()
    fig_regeneration()
    fig_tline()
    print("00-02 figures written to", OUT)
