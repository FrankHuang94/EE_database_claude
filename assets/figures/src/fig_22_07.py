#!/usr/bin/env python3
"""Figures for chapter 22-07 (converter dynamics and control).

Run from anywhere:  python assets/figures/src/fig_22_07.py
Outputs
  assets/figures/22-07/loop-bode.svg  Bode plots of Example 22-07.3's buck plant G_vd, type-III compensator G_c and
                                      loop gain T, with the 60 kHz crossover and 60° phase margin marked
  assets/figures/22-07/boost-rhp.svg  Bode plot of Example 22-07.2's boost G_vd against an otherwise identical plant
                                      with the RHP zero mirrored into the left half plane, showing the extra phase lag
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import control as ct  # noqa: E402

OUT = "assets/figures/22-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_loop():
    f = np.logspace(2, 6, 600)
    l, c, r, vg = 0.6e-6, 62.5e-6, 0.12, 12.0
    _, ph_p = 0, np.degrees(np.angle(ct.buck_gvd(60e3, vg, l, c, r)))
    b, k = ct.kfactor(60, ph_p)
    fz, fp = 60e3 / k, 60e3 * k
    gc0 = ct.type3(60e3, 1.0, fz, fp)
    wi = 1 / abs(gc0 * ct.buck_gvd(60e3, vg, l, c, r))
    g = ct.buck_gvd(f, vg, l, c, r)
    gc = ct.type3(f, wi, fz, fp)
    t = g * gc
    fig, ax = plt.subplots(2, 1, figsize=(6.0, 5.2), sharex=True)
    for y, lab, col in ((g, "plant G_vd", PALETTE[0]), (gc, "compensator G_c", PALETTE[1]), (t, "loop gain T", "0.15")):
        ax[0].semilogx(f, 20 * np.log10(np.abs(y)), color=col, label=lab, lw=1.8 if lab.startswith("loop") else 1.2)
        ax[1].semilogx(f, np.degrees(np.unwrap(np.angle(y))), color=col, lw=1.8 if lab.startswith("loop") else 1.2)
    ax[0].axhline(0, color="0.5", lw=0.8)
    ax[0].axvline(60e3, color="0.5", ls=":")
    ax[1].axvline(60e3, color="0.5", ls=":")
    ax[1].axhline(-180, color="0.5", lw=0.8)
    ax[1].annotate("phase margin 60°", (60e3, -120), (2.5e3, -150), fontsize=8, arrowprops=dict(arrowstyle="->", color="0.3"))
    ax[0].set_ylabel("magnitude (dB)")
    ax[1].set_ylabel("phase (°)")
    ax[1].set_xlabel("frequency (Hz)")
    ax[0].legend(fontsize=8)
    ax[0].set_title("Voltage-mode buck with a type-III compensator (crossover 60 kHz)", fontsize=10)
    save(fig, f"{OUT}/loop-bode.svg")


def fig_rhp():
    f = np.logspace(2, 6.5, 600)
    v, d, l, c, r = 5.0, 0.28, 1e-6, 22e-6, 10 / 3
    g = ct.boost_gvd(f, v, d, l, c, r)
    s = 2j * np.pi * f
    dp = 1 - d
    g_lhp = (v / dp) * (1 + s * l / (dp * dp * r)) / (1 + s * l / (dp * dp * r) + s * s * l * c / (dp * dp))
    fz = ct.boost_rhp_zero_hz(d, l, r)
    fig, ax = plt.subplots(2, 1, figsize=(6.0, 4.8), sharex=True)
    ax[0].semilogx(f, 20 * np.log10(np.abs(g)), color=PALETTE[0], label="boost (RHP zero)")
    ax[0].semilogx(f, 20 * np.log10(np.abs(g_lhp)), color=PALETTE[1], ls="--", label="same zero in the left half plane")
    ax[1].semilogx(f, np.degrees(np.unwrap(np.angle(g))), color=PALETTE[0])
    ax[1].semilogx(f, np.degrees(np.unwrap(np.angle(g_lhp))), color=PALETTE[1], ls="--")
    for a in ax:
        a.axvline(fz, color="0.5", ls=":")
    ax[1].text(fz * 1.1, -60, "f_RHP = 275 kHz", fontsize=8)
    ax[0].set_ylabel("|G_vd| (dB)")
    ax[1].set_ylabel("phase (°)")
    ax[1].set_xlabel("frequency (Hz)")
    ax[0].legend(fontsize=8)
    ax[0].set_title("Boost control-to-output: same magnitude, 180° more lag", fontsize=10)
    save(fig, f"{OUT}/boost-rhp.svg")


if __name__ == "__main__":
    fig_loop()
    fig_rhp()
