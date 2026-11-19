#!/usr/bin/env python3
"""Figures for chapter 09-07 (the bipolar junction transistor).

Run from anywhere:  python assets/figures/src/fig_09_07.py
Outputs SVGs to assets/figures/09-07/. The device is the chapter's NPN: A_E = 10 um^2, W_B = 0.1 um,
N_E = 1e20 (W_E = 0.2 um, Hu's 95 meV band-gap narrowing), N_B = 1e18, N_C = 1e17 cm^-3, 300 K.
- bjt-operation.svg: (a) band diagram (depletion approximation) at V_BE = 0.8 V, V_CB = 2 V;
  (b) excess minority-carrier profiles in emitter and base;
- gummel-beta.svg: (a) Gummel plot with high-level injection in the base and emitter-base depletion
  recombination (tau_0 = 0.1 us over a 30 nm depletion width, an assumed value); (b) beta_F against I_C;
- output-characteristics.svg: I_C against V_CE from Ebers-Moll with base-width modulation
  (beta_F = 100, beta_R = 2, V_A = 31.4 V), with the Early extrapolation;
- ft-vs-ic.svg: f_T against I_C for uniform and graded (0.1 eV) bases, with an illustrative Kirk model
  in which the base pushes out by W_dC (1 - J_K/J) above J_K = q N_C v_sat.
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

OUT = "assets/figures/09-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

Q = 1.602176634e-19
VT = 1.380649e-23 * 300 / Q
NI = 1e10
EPS = 11.7 * 8.8541878128e-14
AE, WB, WE = 1e-7, 1e-5, 2e-5
NE, NB, NC = 1e20, 1e18, 1e17
mun = lambda N: 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)
mup = lambda N: 48 + 402 / (1 + (N / 6.3e16) ** 0.76)
DB, DE = VT * mun(NB), VT * mup(NE)
BGN = math.exp(0.095 / VT)
IS = Q * AE * DB * NI ** 2 / (WB * NB)
BETA0 = (DB * WE * NE) / (DE * WB * NB) / BGN


def junction(NA_, ND_, VA):
    vbi = VT * math.log(NA_ * ND_ / NI ** 2)
    W = math.sqrt(2 * EPS * (vbi - VA) * (1 / NA_ + 1 / ND_) / Q)
    return vbi, W * ND_ / (NA_ + ND_), W * NA_ / (NA_ + ND_)    # vbi, x_p (p side), x_n (n side)


# ---------------------------------------------------------------- figure 1
VBE, VCB = 0.8, 2.0
vbe_bi, xpE, xnE = junction(NB, NE, VBE)       # emitter-base: p = base, n = emitter
vbc_bi, xpC, xnC = junction(NB, NC, -VCB)      # base-collector
# positions (um): emitter neutral [-0.2 - xnE, -xnE], EB depletion [-xnE, xpE], base [xpE, xpE + WB], ...
x0 = 0.0
xs = {"e0": -(WE + xnE), "e1": -xnE, "b0": xpE, "b1": xpE + WB, "c1": xpE + WB + xpC + xnC}
xc_end = xs["c1"] + 0.15e-4


def potential(x):
    """Electrostatic potential (V), zero in the neutral base; depletion approximation."""
    if x <= xs["e1"]:
        return (vbe_bi - VBE)
    if x <= 0:
        return (vbe_bi - VBE) - Q * NE * (x + xnE) ** 2 / (2 * EPS)
    if x <= xs["b0"]:
        return Q * NB * (xs["b0"] - x) ** 2 / (2 * EPS)
    if x <= xs["b1"]:
        return 0.0
    xj = xs["b1"] + xpC
    if x <= xj:
        return Q * NB * (x - xs["b1"]) ** 2 / (2 * EPS)
    if x <= xs["c1"]:
        return (vbc_bi + VCB) - Q * NC * (xs["c1"] - x) ** 2 / (2 * EPS)
    return vbc_bi + VCB


x = np.linspace(xs["e0"], xc_end, 3000)
psi = np.array([potential(t) for t in x])
EG = 1.12
ef_base = -VT * math.log(NB / NI) + EG / 2          # E_F - E_v in the base, roughly (eV, Boltzmann)
Ec = EG - psi                                        # base E_c reference: E_c(base) = E_g with E_v(base) = 0
Ev = -psi
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.8))
ax1.plot(x * 1e4, Ec, color=PALETTE[0], label="$E_C$")
ax1.plot(x * 1e4, Ev, color=PALETTE[1], label="$E_V$")
efp = EG / 2 - VT * math.log(NB / NI)
ax1.hlines(efp, xs["b0"] * 1e4, xs["b1"] * 1e4, color="k", ls="--", lw=1)
ax1.hlines(efp + VBE, xs["e0"] * 1e4, xs["e1"] * 1e4, color="k", ls="--", lw=1)
ax1.hlines(efp - VCB, (xs["c1"]) * 1e4, xc_end * 1e4, color="k", ls="--", lw=1)
ax1.text(xs["e0"] * 1e4 + 0.01, efp + VBE + 0.08, "$E_{Fn}$", fontsize=8)
ax1.text(xs["b0"] * 1e4 + 0.005, efp - 0.2, "$E_{Fp}$", fontsize=8)
ax1.text(xs["c1"] * 1e4 + 0.01, efp - VCB + 0.08, "$E_{Fn}$", fontsize=8)
for lab, a, b in (("emitter", xs["e0"], xs["e1"]), ("base", xs["b0"], xs["b1"]), ("collector", xs["c1"], xc_end)):
    ax1.text((a + b) / 2 * 1e4, 1.75, lab, ha="center", fontsize=8)
ax1.annotate("", xy=(xs["b1"] * 1e4 + 0.05, EG - 0.9), xytext=(xs["b0"] * 1e4 - 0.02, EG - 0.1),
             arrowprops=dict(arrowstyle="->", color=PALETTE[2]))
ax1.text(xs["b0"] * 1e4 + 0.01, EG + 0.1, "electrons", color=PALETTE[2], fontsize=8)
ax1.set_xlabel("position (µm)")
ax1.set_ylabel("energy (eV)")
ax1.set_title(r"(a) bands, $V_{BE}$ = 0.8 V, $V_{CB}$ = 2 V")
ax1.set_ylim(-2.4, 2.0)
ax1.legend(loc="lower left", fontsize=8)
n0 = NI ** 2 / NB * math.exp(VBE / VT)
p0 = NI ** 2 * BGN / NE * math.exp(VBE / VT)
xb = np.linspace(0, WB, 50)
xe = np.linspace(-WE, 0, 50)
ax2.plot((xs["b0"] + xb) * 1e4, n0 * (1 - xb / WB) / n0, color=PALETTE[2], label="electrons in base, $n'(x)$")
ax2.plot((xs["e1"] + xe) * 1e4, p0 * (1 + xe / WE) / n0, color=PALETTE[1], label="holes in emitter, $p'(x)$")
ax2.axvspan(xs["e1"] * 1e4, xs["b0"] * 1e4, color="0.9")
ax2.axvspan(xs["b1"] * 1e4, xs["c1"] * 1e4, color="0.9")
ax2.text((xs["b1"] + xs["c1"]) / 2 * 1e4, 0.6, "B–C\ndepletion", ha="center", fontsize=8)
ax2.set_xlabel("position (µm)")
ax2.set_ylabel(r"excess density / $n'(0)$")
ax2.set_title("(b) minority carriers (band-gap narrowing included)")
ax2.set_xlim(xs["e0"] * 1e4, xc_end * 1e4)
ax2.set_ylim(0, 1.1)
ax2.legend(loc="upper right", fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/bjt-operation.svg")
plt.close(fig)

# ---------------------------------------------------------------- figure 2
TAU0, WEB = 1e-7, 3e-6
IR0 = Q * NI * WEB * AE / (2 * TAU0)
v = np.linspace(0.3, 1.05, 600)
nprime = (-NB + np.sqrt(NB ** 2 + 4 * NI ** 2 * np.exp(v / VT))) / 2   # n'(N_B + n') = n_i^2 e^{V/V_T}
ic = Q * AE * DB * nprime / WB
ib = IS / BETA0 * np.exp(v / VT) + IR0 * (np.exp(v / (2 * VT)) - 1)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.8))
ax1.semilogy(v, ic, color=PALETTE[0], label="$I_C$")
ax1.semilogy(v, ib, color=PALETTE[1], label="$I_B$")
ax1.semilogy(v, IS * np.exp(v / VT), color=PALETTE[0], ls=":", lw=1, label="ideal $I_Se^{V_{BE}/V_T}$")
ax1.set_xlabel("$V_{BE}$ (V)")
ax1.set_ylabel("current (A)")
ax1.set_title("(a) Gummel plot")
ax1.set_ylim(1e-14, 1e-1)
ax1.legend(loc="lower right", fontsize=8)
ax2.semilogx(ic, ic / ib, color="k")
ax2.set_xlabel("$I_C$ (A)")
ax2.set_ylabel(r"$\beta_F = I_C/I_B$")
ax2.set_title("(b) current gain against collector current")
ax2.set_xlim(1e-12, 1e-1)
ax2.text(3e-12, 3, "depletion-region\nrecombination", fontsize=8)
ax2.text(1e-5, 8, "high-level\ninjection", fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/gummel-beta.svg")
plt.close(fig)

# ---------------------------------------------------------------- figure 3
BF, BR, VA = 100.0, 2.0, 31.4
IS3 = IS


def ic_ib(vbe, vce):
    vbc = vbe - vce
    x_, y_ = math.exp(vbe / VT), math.exp(vbc / VT)
    ic_ = IS3 * (x_ - y_) * (1 + vce / VA) - IS3 / BR * (y_ - 1)
    ib_ = IS3 / BF * (x_ - 1) + IS3 / BR * (y_ - 1)
    return ic_, ib_


fig, (axa, axb) = plt.subplots(1, 2, figsize=(9.8, 3.9))
vce = np.linspace(0.0, 3.0, 400)
for i, IB in enumerate((2e-6, 4e-6, 6e-6, 8e-6, 10e-6)):
    icv = []
    for vc in vce:
        vb = brentq(lambda vv: ic_ib(vv, vc)[1] - IB, 0.3, 1.2, xtol=1e-12)
        icv.append(ic_ib(vb, vc)[0])
    icv = np.array(icv)
    for ax in (axa, axb):
        ax.plot(vce, icv * 1e3, color=PALETTE[i % 7], label=f"$I_B$ = {IB*1e6:.0f} µA")
    slope = (icv[-1] - icv[-60]) / (vce[-1] - vce[-60])
    xx = np.linspace(-VA, 3, 10)
    axb.plot(xx, (icv[-1] + slope * (xx - vce[-1])) * 1e3, color=PALETTE[i % 7], ls=":", lw=0.8)
axa.set_xlim(0, 3)
axa.set_ylim(0, 1.15)
axa.set_xlabel("$V_{CE}$ (V)")
axa.set_ylabel("$I_C$ (mA)")
axa.set_title("(a) saturation and forward-active regions")
axa.text(0.05, 1.08, "saturation", fontsize=8)
axb.legend(loc="upper left", fontsize=8)
axb.set_xlim(-35, 3)
axb.set_ylim(0, 1.15)
axb.axvline(0, color="k", lw=0.6)
axb.text(-33, 0.05, r"$-V_A$ = −31.4 V", fontsize=8)
axb.set_xlabel("$V_{CE}$ (V)")
axb.set_title("(b) Early extrapolation (dotted)")
fig.tight_layout()
save(fig, f"{OUT}/output-characteristics.svg")
plt.close(fig)

# ---------------------------------------------------------------- figure 4
vbc_bi2, xp2, xn2 = junction(NB, NC, -2.0)
WDC = xn2
VSAT = 1.53e9 * 300 ** -0.87
JK = Q * NC * VSAT
CJE = 20e-15
CJC = EPS / (xp2 + xn2) * 2 * AE
ic = np.geomspace(1e-5, 1e-1, 400)
eta = 0.1 / VT


def tau_b(w, graded):
    if not graded:
        return w ** 2 / (2 * DB)
    e = eta * w / WB                                    # same field, longer path when pushed out
    return w ** 2 / DB / e * (1 - (1 - math.exp(-e)) / e)


fig, ax = plt.subplots(figsize=(6.6, 3.9))
for graded, col, lab in ((False, PALETTE[0], "uniform base"), (True, PALETTE[2], "graded SiGe base (0.1 eV)")):
    ft = []
    for i_ in ic:
        J = i_ / AE
        push = WDC * (1 - JK / J) if J > JK else 0.0
        tb = tau_b(WB + push, graded)
        tc = (WDC - push) / (2 * VSAT)
        ft.append(1 / (2 * math.pi * (tb + tc + (CJE + CJC) * VT / i_)))
    ax.semilogx(ic * 1e3, np.array(ft) / 1e9, color=col, label=lab)
ax.axvline(JK * AE * 1e3, color="k", ls=":", lw=1)
ax.text(JK * AE * 1e3 * 1.1, 3, "Kirk onset\n$J_K = qN_Cv_{sat}$", fontsize=8)
ax.set_xlabel("$I_C$ (mA)")
ax.set_ylabel("$f_T$ (GHz)")
ax.set_title(r"Cutoff frequency against current ($A_E$ = 10 µm², $V_{CB}$ = 2 V)")
ax.legend(loc="upper left", fontsize=8)
ax.set_ylim(0, 50)
fig.tight_layout()
save(fig, f"{OUT}/ft-vs-ic.svg")
plt.close(fig)
print("figures written to", OUT)
