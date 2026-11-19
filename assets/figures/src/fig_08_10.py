#!/usr/bin/env python3
"""Figures for chapter 08-10 (timing, metastability and clock-domain crossing).

Run from anywhere:  python assets/figures/src/fig_08_10.py
Outputs SVGs to assets/figures/08-10/:
- mtbf.svg: synchronizer MTBF against resolution time S for tau = 20 ps and 40 ps (the parameters of
  Examples 08-10.4 and 08-10.5), with the one-, two- and three-flip-flop operating points marked;
- resolution.svg: a Monte Carlo simulation of metastability resolution (data arrivals uniform over the
  clock period, initial imbalance proportional to the arrival offset, exponential growth with time
  constant tau): the fraction still unresolved after time t, against the exponential law.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
YEAR = 365.25 * 24 * 3600
TW, FC, FD = 20e-12, 1e9, 200e6


def mtbf(S, tau):
    return np.exp(S / tau) / (TW * FC * FD)


def fig_mtbf():
    S = np.linspace(0, 2000e-12, 400)
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for k, tau in enumerate((20e-12, 40e-12)):
        ax.semilogy(S * 1e12, mtbf(S, tau) / YEAR, color=PALETTE[k], label=f"τ = {tau * 1e12:.0f} ps")
    pts = [(520e-12, "1 flip-flop + 400 ps logic"), (920e-12, "2 flip-flops"), (1840e-12, "3 flip-flops")]
    for s, lab in pts:
        y = mtbf(s, 20e-12) / YEAR
        ax.plot(s * 1e12, y, "o", color=PALETTE[0])
        ax.annotate(lab, (s * 1e12, y), textcoords="offset points", xytext=(-8, 8), ha="right", fontsize=8.5)
    y2 = mtbf(920e-12, 40e-12) / YEAR
    ax.plot(920, y2, "o", color=PALETTE[1])
    ax.annotate("2 flip-flops at τ = 40 ps:\n41 minutes", (920, y2), textcoords="offset points", xytext=(10, -22),
                fontsize=8.5, color=PALETTE[1])
    for yrs, lab in ((1 / (365.25 * 24), "1 hour"), (1, "1 year"), (1e9, "10⁹ years")):
        ax.axhline(yrs, color="0.6", lw=0.8, ls=":")
        ax.text(1990, yrs * 1.6, lab, ha="right", fontsize=8, color="0.4")
    ax.set_xlim(0, 2000)
    ax.set_ylim(1e-9, 1e28)
    ax.set_xlabel("resolution time S (ps)")
    ax.set_ylabel("MTBF (years)")
    ax.set_title("Synchronizer MTBF: 1 GHz clock, 200 MHz data, $T_W$ = 20 ps", fontsize=10.5)
    ax.legend(loc="upper left")
    save(fig, f"{OUT}/mtbf.svg")


def fig_resolution():
    rng = np.random.default_rng(810)
    tau, tw, tc, n = 20e-12, 20e-12, 1e-9, 10_000_000
    dt = rng.uniform(-tc / 2, tc / 2, n)                  # data arrival relative to the balance instant
    v_ratio = np.abs(dt) / (tw / 2)                        # initial imbalance / resolved level = |dt| / (T_W / 2)
    t_res = np.where(v_ratio >= 1, 0.0, tau * np.log(1 / np.maximum(v_ratio, 1e-300)))
    t = np.linspace(0, 260e-12, 27)
    measured = np.array([(t_res > x).mean() for x in t])
    theory = tw / tc * np.exp(-t / tau)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.semilogy(t * 1e12, theory, color=PALETTE[0], label=r"theory $(T_W/T_c)\,e^{-t/\tau}$")
    ok = measured > 0
    ax.semilogy(t[ok] * 1e12, measured[ok], "o", color=PALETTE[1], ms=4, label=f"simulation, {n:.0e} samples")
    ax.set_xlabel("time after the clock edge, t (ps)")
    ax.set_ylabel("fraction of samples still unresolved")
    ax.set_title("Metastability resolves exponentially (τ = 20 ps, $T_W$ = 20 ps, 1 GHz)", fontsize=10.5)
    ax.legend()
    save(fig, f"{OUT}/resolution.svg")


if __name__ == "__main__":
    fig_mtbf()
    fig_resolution()
    print("figures written to", OUT)
