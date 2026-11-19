#!/usr/bin/env python3
"""Figures for chapter 09-08 (the MOS capacitor).

Run from anywhere:  python assets/figures/src/fig_09_08.py
Outputs SVGs to assets/figures/09-08/. The capacitor is the chapter's: p-type N_A = 1e17 cm^-3, 10 nm SiO2,
n+ poly gate (V_FB = -0.9858 V), 300 K, exact Poisson-Boltzmann surface charge.
- mos-surface-potential-charge.svg: (a) surface potential against gate voltage; (b) depletion (bulk) and
  inversion charge magnitudes against gate voltage, with the sheet-charge approximation;
- mos-cv.svg: quasi-static, high-frequency and deep-depletion C-V curves.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

Q = 1.602176634e-19
VT = 1.380649e-23 * 300 / Q
NI = 1e10
EPS = 11.7 * 8.8541878128e-14
EOX = 3.9 * 8.8541878128e-14
NA, TOX = 1e17, 10e-7
COX = EOX / TOX
N0 = NI ** 2 / NA
VFB = 4.05 - (4.05 + 1.12 - VT * math.log(1.8e19 / NA))
PB = VT * math.log(NA / NI)


def Qs(phi):
    if abs(phi) < 1e-12:
        return 0.0
    F2 = (math.exp(-phi / VT) + phi / VT - 1) + (N0 / NA) * (math.exp(phi / VT) - phi / VT - 1)
    return -math.copysign(1, phi) * math.sqrt(2 * Q * NA * EPS * VT * F2)


def vg_of(phi):
    return VFB + phi - Qs(phi) / COX


phis = np.linspace(-0.25, 1.06, 3000)
vgs = np.array([vg_of(p) for p in phis])
qb = np.array([math.sqrt(2 * Q * EPS * NA * max(p - VT, 0)) if p > VT else 0 for p in phis])
qtot = np.array([abs(Qs(p)) for p in phis])
qinv = np.where(phis > VT, qtot - qb, 0)
VT0 = VFB + 2 * PB + math.sqrt(2 * Q * NA * EPS * 2 * PB) / COX

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.8))
ax1.plot(vgs, phis, color="k")
ax1.axhline(2 * PB, color=PALETTE[1], ls=":", lw=1)
ax1.axvline(VFB, color="0.6", ls="--", lw=0.8)
ax1.axvline(VT0, color="0.6", ls="--", lw=0.8)
ax1.text(VFB + 0.03, -0.2, "$V_{FB}$", fontsize=8)
ax1.text(VT0 + 0.03, -0.2, "$V_{TH}$", fontsize=8)
ax1.text(-2.4, 2 * PB + 0.03, r"$2\phi_B$", color=PALETTE[1], fontsize=8)
ax1.text(-2.4, 0.15, "accumulation", fontsize=8)
ax1.text(-0.85, 0.45, "depletion", fontsize=8)
ax1.text(0.9, 0.7, "inversion", fontsize=8)
ax1.set_xlim(-2.5, 2.5)
ax1.set_xlabel("gate voltage $V_g$ (V)")
ax1.set_ylabel(r"surface potential $\phi_s$ (V)")
ax1.set_title("(a) surface potential")
m = phis > 3 * VT
ax2.semilogy(vgs[m], qb[m] / Q, color=PALETTE[0], label="depletion (acceptor) charge")
ax2.semilogy(vgs[m & (qinv > 0)], qinv[m & (qinv > 0)] / Q, color=PALETTE[2], label="inversion (electron) charge")
vv = np.linspace(VT0 + 0.01, 2.5, 100)
ax2.semilogy(vv, COX * (vv - VT0) / Q, color=PALETTE[2], ls="--", lw=1, label=r"sheet model $C_{ox}(V_g - V_{TH})$")
ax2.axvline(VT0, color="0.6", ls="--", lw=0.8)
ax2.set_xlim(-1.0, 2.5)
ax2.set_ylim(1e8, 1e13)
ax2.set_xlabel("gate voltage $V_g$ (V)")
ax2.set_ylabel("charge / q (cm$^{-2}$)")
ax2.set_title("(b) charges in the silicon")
ax2.legend(loc="lower right", fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/mos-surface-potential-charge.svg")
plt.close(fig)

# ---------------------------------------------------------------- C-V
dp = 1e-6
cs = np.array([-(Qs(p + dp) - Qs(p - dp)) / (2 * dp) for p in phis])
c_lf = 1 / (1 / COX + 1 / cs)
# high frequency: electrons cannot follow, so below 2 phi_B use the hole-and-acceptor charge only, and at
# or above 2 phi_B freeze the depletion edge at W_dmax (C_min)


def Qs_noinv(phi):
    if abs(phi) < 1e-12:
        return 0.0
    F2 = math.exp(-phi / VT) + phi / VT - 1
    return -math.copysign(1, phi) * math.sqrt(2 * Q * NA * EPS * VT * F2)


WDM = math.sqrt(2 * EPS * 2 * PB / (Q * NA))
c_hf = []
for p_ in phis:
    if p_ < 2 * PB:
        csn = -(Qs_noinv(p_ + dp) - Qs_noinv(p_ - dp)) / (2 * dp)
        c_hf.append(1 / (1 / COX + 1 / csn))
    else:
        c_hf.append(1 / (1 / COX + WDM / EPS))
c_hf = np.array(c_hf)
vdd = np.linspace(VT0, 3.0, 300)
Wdd = np.array([brentq(lambda W: VFB + Q * NA * W ** 2 / (2 * EPS) + Q * NA * W / COX - vg, 0, 1e-3) for vg in vdd])
c_dd = 1 / (1 / COX + Wdd / EPS)
cfb = 1 / (1 / COX + math.sqrt(EPS * VT / (Q * NA)) / EPS)

fig, ax = plt.subplots(figsize=(6.6, 3.9))
ax.plot(vgs, c_lf / COX, color=PALETTE[0], label="quasi-static (low frequency, or a transistor)")
ax.plot(vgs, c_hf / COX, color=PALETTE[1], label="high frequency (capacitor)")
ax.plot(vdd, c_dd / COX, color=PALETTE[3], ls="-.", label="deep depletion (fast sweep)")
ax.axhline(cfb / COX, color="0.5", ls="--", lw=0.8)
ax.text(-2.4, cfb / COX + 0.02, "$C_{FB}$", fontsize=8)
ax.set_xlim(-2.5, 3.0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("gate voltage $V_g$ (V)")
ax.set_ylabel("$C/C_{ox}$")
ax.set_title("MOS C–V: $N_A$ = 10$^{17}$ cm$^{-3}$, 10 nm oxide, n$^+$ gate")
ax.legend(loc="center right", fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/mos-cv.svg")
plt.close(fig)
print("figures written to", OUT)
