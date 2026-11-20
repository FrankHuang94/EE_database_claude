#!/usr/bin/env python3
"""Figures for chapter 15-12 (applications: PLLs, regulators, thermal management).

Run from anywhere:  python assets/figures/src/fig_15_12.py
Outputs
  assets/figures/15-12/pll_noise.svg  left: output phase noise of Example 15-12.5's PLL at the optimal crossover,
                                      with the reference and VCO contributions; right: rms jitter against crossover.
  assets/figures/15-12/throttle.svg   Example 15-12.7: junction temperature and permitted power under the
                                      sampled velocity-form PI limiter, with the exponential of section 3.6.
Uses labs/15-12-lab/loops.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import loops as lp  # noqa: E402

OUT = "assets/figures/15-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_pll_noise():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
    fc = 10 ** 5.5
    d = lp.pll_design(fc, 60, 1.0, 1.0, 1.0)
    num, den = [d["K"] * d["tz"], d["K"]], [d["tp"], 1.0, 0.0, 0.0]
    f = np.logspace(4, 8, 2000)
    L = lp.freq_resp(num, den, 2 * math.pi * f)
    T, S = L / (1 + L), 1 / (1 + L)
    ref = -110 + 20 * np.log10(np.abs(T))
    vco_free = -120 + 20 * np.log10(1e6 / f)
    vco = vco_free + 20 * np.log10(np.abs(S))
    tot = 10 * np.log10(10 ** (ref / 10) + 10 ** (vco / 10))
    a1.semilogx(f, np.full_like(f, -110), color=PALETTE[0], ls=":", lw=0.9, label="reference path, unshaped")
    a1.semilogx(f, vco_free, color=PALETTE[1], ls=":", lw=0.9, label="free-running VCO")
    a1.semilogx(f, ref, color=PALETTE[0], label="reference × |T|²")
    a1.semilogx(f, vco, color=PALETTE[1], label="VCO × |S|²")
    a1.semilogx(f, tot, color="k", lw=1.6, label="total")
    a1.axvline(fc, color="gray", lw=0.6)
    a1.text(fc * 1.1, -152, "fc = 316 kHz", fontsize=7, color="gray")
    a1.set_ylim(-160, -85)
    a1.set_xlabel("offset frequency (Hz)")
    a1.set_ylabel("phase noise (dBc/Hz)")
    a1.set_title("Example 15-12.5: noise shaping at the optimal bandwidth", fontsize=9)
    a1.legend(fontsize=6.5, loc="lower left")

    fcs = np.logspace(4.3, 6.7, 41)
    jit = [lp.jitter(x)[1] * 1e15 for x in fcs]
    a2.semilogx(fcs, jit, color=PALETTE[2])
    for x in (1e5, fc, 1e6):
        a2.plot(x, lp.jitter(x)[1] * 1e15, "o", color=PALETTE[2], ms=4)
    a2.set_xlabel("crossover fc (Hz)")
    a2.set_ylabel("rms jitter, 10 kHz–100 MHz (fs)")
    a2.set_title("Integrated jitter against loop bandwidth", fontsize=9)
    a2.set_ylim(0, 1200)
    fig.tight_layout()
    save(fig, f"{OUT}/pll_noise.svg")


def fig_throttle():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True)
    t, TJ, P, t_thr = lp.throttle(10.0, 10.0 / 0.75)
    a1.plot(t, TJ, color=PALETTE[3])
    a1.axhline(95, color="gray", lw=0.6, ls="--")
    a1.text(5, 96.5, "limit 95 °C", fontsize=7, color="gray")
    a1.set_ylabel("junction (°C)")
    a1.set_ylim(25, 105)
    a1.set_title("Example 15-12.7: turbo, then throttle (200 W demand)", fontsize=9)
    a2.plot(t, P, color=PALETTE[0], label="permitted power (sampled PI limiter)")
    tt = np.linspace(75.5, 400, 400)
    a2.plot(tt, 130 + 70 * np.exp(-(tt - 75.5) / 31.5), color=PALETTE[1], ls="--", lw=1,
            label="130 + 70 exp(−t′/31.5 s)")
    a2.axhline(130, color="gray", lw=0.6, ls=":")
    a2.text(300, 122, "sustained 130 W", fontsize=7, color="gray")
    a2.set_ylabel("power (W)")
    a2.set_xlabel("time (s)")
    a2.set_ylim(100, 210)
    a2.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/throttle.svg")


if __name__ == "__main__":
    fig_pll_noise()
    fig_throttle()
