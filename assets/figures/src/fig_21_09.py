#!/usr/bin/env python3
"""Figures for chapter 21-09 (the RF front end).

Run from anywhere:  python assets/figures/src/fig_21_09.py
Outputs
  assets/figures/21-09/bvd.svg     impedance magnitude of the AlN resonator of Example 21-09.1 (BVD model), with
                                   the series resonance at 2.000 GHz and the anti-resonance at 2.057 GHz
  assets/figures/21-09/ladder.svg  three-section ladder filter of Example 21-09.2 for Q = 2000 and Q = 500, with
                                   the series and shunt resonances that set the pass band and the notches
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import frontend as fe  # noqa: E402

OUT = "assets/figures/21-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

FS = 2e9
FP = fe.fp_for_k2(FS, 0.066)
R = 1 / ((FP / FS) ** 2 - 1)
LM, CM, RM = fe.bvd(FS, 1e-12, R, 2000)
FSH = FS / fe.fp_over_fs(R)

# ---------------------------------------------------------------- BVD impedance
f = np.linspace(1.9e9, 2.15e9, 5001)
z = fe.z_bvd(f, 1e-12, LM, CM, RM)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.semilogy(f / 1e9, np.abs(z), color=PALETTE[0], lw=1.6, label="BVD resonator")
ax.semilogy(f / 1e9, 1 / (2 * np.pi * f * 1e-12), color="0.5", lw=1, ls="--", label=r"$C_0$ alone (1 pF)")
for x, lab_, col in ((FS, f"$f_s$ = {FS/1e9:.3f} GHz\n|Z| ≈ $R_m$", PALETTE[2]),
                     (FP, f"$f_p$ = {FP/1e9:.3f} GHz", PALETTE[3])):
    ax.axvline(x / 1e9, color=col, lw=1, ls=":")
    ax.text(x / 1e9 + 0.004, 2e3 if x == FP else 0.3, lab_, fontsize=8, color=col, va="bottom")
ax.set_xlim(1.9, 2.15)
ax.set_ylim(0.1, 1e5)
ax.set_xlabel("frequency (GHz)")
ax.set_ylabel("|Z| (Ω)")
ax.set_title("An acoustic resonator: a short and an open 2.8% apart", fontsize=10)
ax.legend(loc="lower left", fontsize=8)
save(fig, f"{OUT}/bvd.svg")

# ---------------------------------------------------------------- ladder filter
f = np.linspace(1.85e9, 2.15e9, 3001)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
for q, col in ((2000, PALETTE[0]), (500, PALETTE[1])):
    s21 = fe.ladder_s21(f, fe.ladder(FS, FSH, 1e-12, 2e-12, R, q, 3))
    ax.plot(f / 1e9, 20 * np.log10(np.abs(s21)), color=col, lw=1.5, label=f"Q = {q}")
for x, lab_, col, dx, ha in ((FSH, "shunt $f_s$\n(notch)", PALETTE[2], -0.003, "right"),
                             (FS, "series $f_s$ =\nshunt $f_p$", "k", 0.003, "left"),
                             (FP, "series $f_p$\n(notch)", PALETTE[3], 0.003, "left")):
    ax.axvline(x / 1e9, color=col, lw=1, ls=":")
    ax.text(x / 1e9 + dx, -68 if x == FS else -18, lab_, fontsize=7.5, color=col, va="bottom", ha=ha)
ax.set_xlim(1.85, 2.15)
ax.set_ylim(-70, 2)
ax.set_xlabel("frequency (GHz)")
ax.set_ylabel(r"$|S_{21}|$ (dB)")
ax.set_title("Three-section ladder: pass band between the notches", fontsize=10)
ax.legend(loc="upper right", fontsize=8)
save(fig, f"{OUT}/ladder.svg")
