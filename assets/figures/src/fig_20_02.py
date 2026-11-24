#!/usr/bin/env python3
"""Figures for chapter 20-02 (two-stage op-amp design).

Run from anywhere:  python assets/figures/src/fig_20_02.py
Outputs
  assets/figures/20-02/current-vs-cc.svg    first-stage, second-stage and total current of Example 20-02.3's op-amp
                                            against the compensation capacitor (p2 held at 2 omega_u)
  assets/figures/20-02/loop-gain-rz.svg     Bode magnitude and phase of the loop gain with R_z = 0, 1/g_m6 and the
                                            cancelling value
  assets/figures/20-02/boost-settling.svg   step-response error of the gain-boosted example with a slow (20 MHz) and a
                                            fast (300 MHz) booster, against an ideal single-pole amplifier
  assets/figures/20-02/settling-vs-pm.svg   0.1 % settling time of a two-pole unity-gain loop against phase margin
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import opamp as o  # noqa: E402

OUT = "assets/figures/20-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
spec, ch = o.Spec(), o.Choices()
d = o.design_two_stage(spec, ch)

# ---------------------------------------------------------------- figure 3: current against C_c
ccs = np.linspace(0.35e-12, 1.6e-12, 300)
wu = 2 * math.pi * spec.gbw
i_ss = 2 * wu * ccs / ch.gmid1
i_tot = np.array([o.total_current(c, spec, ch) for c in ccs])
i_6 = i_tot - i_ss
c_opt = o.optimum_cc(spec, ch)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(ccs * 1e12, i_tot * 1e6, color=PALETTE[0], label="total $I_{SS} + I_6$")
ax.plot(ccs * 1e12, i_6 * 1e6, color=PALETTE[1], ls="--", label="second stage $I_6$")
ax.plot(ccs * 1e12, i_ss * 1e6, color=PALETTE[2], ls=":", label="first stage $I_{SS}$")
ax.axvline(c_opt * 1e12, color="0.5", lw=0.8)
ax.annotate(f"optimum {c_opt * 1e12:.2f} pF", (c_opt * 1e12, o.total_current(c_opt, spec, ch) * 1e6),
            xytext=(c_opt * 1e12 + 0.15, 230), arrowprops=dict(arrowstyle="->", color="0.4"), fontsize=9)
ax.axvline(0.6, color=PALETTE[3], lw=0.8, ls="-.")
ax.text(0.61, 270, "design: 0.6 pF", color=PALETTE[3], fontsize=9)
ax.set_xlabel("compensation capacitor $C_c$ (pF)")
ax.set_ylabel("supply current (µA)")
ax.set_ylim(0, 300)
ax.legend(loc="upper right")
ax.set_title("Example 20-02.3: GBW 50 MHz, $C_L$ = 2 pF, $p_2 = 2\\omega_u$")
save(fig, f"{OUT}/current-vs-cc.svg")

# ---------------------------------------------------------------- figure 4: loop gain for three R_z
f = np.logspace(3, 10, 3000)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 5.6), sharex=True)
for rz, lab_, col, ls in ((0.0, "$R_z$ = 0", PALETTE[1], "-"), (d["rz"], "$R_z = 1/g_{m6}$", PALETTE[0], "--"),
                          (d["rz_cancel"], "cancelling $R_z$", PALETTE[2], ":")):
    num, den = o.miller_tf(d["gm1"], d["gm6"], d["r1"], d["r2"], d["c1"], spec.cl, ch.cc, rz)
    h = np.polyval(num, 2j * math.pi * f) / np.polyval(den, 2j * math.pi * f)
    m = o.margins(o.poly_tf(num, den))
    ax1.semilogx(f, 20 * np.log10(np.abs(h)), color=col, ls=ls, label=f"{lab_}: PM {m['pm']:.1f}°")
    ax2.semilogx(f, np.degrees(np.unwrap(np.angle(h))), color=col, ls=ls)
ax1.axhline(0, color="0.5", lw=0.8)
ax1.set_ylabel("loop gain (dB)")
ax1.set_ylim(-60, 70)
ax1.legend(loc="lower left")
ax2.axhline(-180, color="0.5", lw=0.8)
ax2.set_ylabel("phase (degrees)")
ax2.set_xlabel("frequency (Hz)")
ax2.set_ylim(-280, 10)
ax1.set_title("Example 20-02.3's op-amp as a unity-gain follower")
save(fig, f"{OUT}/loop-gain-rz.svg")

# ---------------------------------------------------------------- figure 5: gain-boost settling


def boost_error(gm, cl, a_unb, ab0, beta, fub, t):
    r0 = a_unb / gm
    wpb = 2 * math.pi * fub / ab0
    n_r = np.array([r0 / wpb, r0 * (1 + ab0)])
    d_r = np.array([1 / wpb, 1.0])
    d_z = np.polyadd(d_r, np.polymul([cl, 0], n_r))
    num_a = gm * n_r
    den_t = np.polyadd(d_z, beta * num_a)
    final = np.polyval(num_a, 0) / np.polyval(den_t, 0)
    _, y = signal.step((num_a / final, den_t), T=t)
    return np.abs(1 - y)


t = np.linspace(0, 60e-9, 60001)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ideal = np.exp(-0.5 * 1e9 * t)
ax.semilogy(t * 1e9, ideal * 100, color="0.5", ls=":", label="ideal single pole")
ax.semilogy(t * 1e9, boost_error(1e-3, 1e-12, 300, 100, 0.5, 20e6, t) * 100, color=PALETTE[1],
            label="booster $f_{ub}$ = 20 MHz")
ax.semilogy(t * 1e9, boost_error(1e-3, 1e-12, 300, 100, 0.5, 300e6, t) * 100, color=PALETTE[0], ls="--",
            label="booster $f_{ub}$ = 300 MHz")
ax.axhline(0.01, color=PALETTE[3], lw=0.8)
ax.text(1, 0.012, "0.01 %", color=PALETTE[3], fontsize=9)
ax.axhline(100 / (0.5 * 300), color="0.6", lw=0.6, ls="-.")
ax.text(40, 0.8, "$1/(\\beta A_{unb})$", color="0.4", fontsize=9)
ax.set_ylim(1e-4, 200)
ax.set_xlabel("time after the step (ns)")
ax.set_ylabel("settling error (%)")
ax.legend(loc="upper right")
ax.set_title("Gain boosting: $g_{m1}$ = 1 mS, $C_L$ = 1 pF, β = 0.5, $A_{unb}$ = 300")
save(fig, f"{OUT}/boost-settling.svg")

# ---------------------------------------------------------------- figure 6: settling against phase margin
ks = np.concatenate([np.linspace(0.8, 3.0, 111), np.linspace(3.01, 6, 200), np.linspace(6.1, 40, 90)])
tt = np.linspace(0, 40, 40001)
pms, tss = [], []
for k in ks:
    _, y = signal.step(([1.0], [1 / k, 1.0, 1.0]), T=tt)
    bad = np.where(np.abs(y - 1) > 1e-3)[0]
    tss.append(tt[bad[-1] + 1])
    pms.append(o.two_pole_pm(k))
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(pms, tss, color=PALETTE[0])
ax.axhline(math.log(1e3), color="0.5", lw=0.8, ls=":")
ax.text(46, math.log(1e3) + 0.2, "single pole: 6.91", color="0.4", fontsize=9)
i = int(np.argmin(tss))
ax.plot(pms[i], tss[i], "o", color=PALETTE[1])
ax.annotate(f"fastest: PM ≈ {pms[i]:.0f}°", (pms[i], tss[i]), xytext=(pms[i] - 22, 2.2),
            arrowprops=dict(arrowstyle="->", color="0.4"), fontsize=9)
ax.set_xlabel("phase margin (degrees)")
ax.set_ylabel("0.1 % settling time × $\\omega_u$")
ax.set_xlim(45, 90)
ax.set_ylim(0, 16)
ax.set_title("Two-pole unity-gain loop $\\omega_u/[s(1 + s/k\\omega_u)]$")
save(fig, f"{OUT}/settling-vs-pm.svg")
print("figures written to", OUT)
