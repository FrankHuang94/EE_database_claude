#!/usr/bin/env python3
"""Figures for chapter 09-06 (PN junction I-V, capacitance and breakdown).

Run from anywhere:  python assets/figures/src/fig_09_06.py
Outputs SVGs to assets/figures/09-06/:
- diode-carriers-currents.svg: (a) excess-hole profiles of a forward-biased P+N diode, long (exponential) and
  short (W_n = 0.5 L_p, nearly linear); (b) hole and electron current components in the long diode;
- real-diode-iv.svg: the diode of Example 09-06.1 with depletion-region recombination (tau_0 = 1 us),
  high-level injection and R_s = 50 ohm: (a) semilog I-V with the ideal components, (b) local ideality factor;
- reverse-recovery.svg: numerical solution of the diffusion equation for a long diode switched from I_F to
  -I_R = -I_F: (a) edge density and stored charge against time with the charge-control charge,
  (b) profiles at several times;
- avalanche-breakdown.svg: (a) silicon impact-ionization coefficients (handbook fits), (b) breakdown voltage
  and peak field at breakdown of a one-sided junction against doping, with Hu's rule and the
  fixed-critical-field estimate.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid, trapezoid
from scipy.linalg import solve_banded
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

Q = 1.602176634e-19
VT = 1.380649e-23 * 300 / Q
NI = 1e10
EPS = 11.7 * 8.8541878128e-14
NA, ND, TP, AREA = 1e19, 1e16, 1e-6, 1e-4
MUP = 48 + 402 / (1 + (ND / 6.3e16) ** 0.76)
DP = VT * MUP
LP = math.sqrt(DP * TP)

# ---------------------------------------------------------------- figure 1
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.6))
x = np.linspace(0, 4, 400)
ax1.plot(x, np.exp(-x), color=PALETTE[0], label="long diode: $e^{-x'/L_p}$")
ws = 0.5
xs = np.linspace(0, ws, 100)
ax1.plot(xs, np.sinh(ws - xs) / np.sinh(ws), color=PALETTE[1], label="short diode, $W_n = 0.5L_p$")
ax1.axvline(ws, color=PALETTE[1], lw=0.8, ls=":")
ax1.text(ws + 0.05, 0.85, "ohmic\ncontact", color=PALETTE[1], fontsize=8)
ax1.set_xlabel("distance from depletion edge $x'/L_p$")
ax1.set_ylabel(r"$\Delta p(x')/\Delta p(0)$")
ax1.set_title("(a) excess holes on the n side")
ax1.legend(loc="upper right")
ax1.set_xlim(0, 4)
ax1.set_ylim(0, 1.05)
jp = np.exp(-x)
ax2.plot(x, jp, color=PALETTE[0], label="hole (minority) current, diffusion")
ax2.plot(x, 1 - jp, color=PALETTE[2], label="electron (majority) current")
ax2.plot(x, np.ones_like(x), color="k", ls="--", lw=1, label="total current")
ax2.set_xlabel("distance from depletion edge $x'/L_p$")
ax2.set_ylabel("current / total current")
ax2.set_title("(b) current components, long P$^+$N diode")
ax2.legend(loc="center right")
ax2.set_xlim(0, 4)
ax2.set_ylim(0, 1.1)
fig.tight_layout()
save(fig, f"{OUT}/diode-carriers-currents.svg")
plt.close(fig)

# ---------------------------------------------------------------- figure 2
VBI = VT * math.log(NA * ND / NI ** 2)
W04 = math.sqrt(2 * EPS * (VBI - 0.4) * (1 / NA + 1 / ND) / Q)
TAU0, RS = 1e-6, 50.0
JN0 = 1.519e-14                 # electron term from Example 09-06.1 (A/cm^2)
JP0 = Q * NI ** 2 * DP / (LP * ND)


def i_junction(vj):
    """Diffusion current with high-level injection (edge density from p(N_D + p) = n_i^2 e^{V/V_T}),
    plus depletion-region recombination with W fixed at its 0.4 V value."""
    pe = (-ND + np.sqrt(ND ** 2 + 4 * NI ** 2 * np.exp(vj / VT))) / 2
    pe0 = NI ** 2 / ND
    idiff = AREA * Q * DP / LP * (pe - pe0) * (1 + JN0 / JP0)
    irec = AREA * Q * NI * W04 / (2 * TAU0) * (np.exp(vj / (2 * VT)) - 1)
    return idiff, irec


vj = np.linspace(0.05, 0.95, 2000)
idiff, irec = i_junction(vj)
itot = idiff + irec
vterm = vj + itot * RS
Is = AREA * (JP0 + JN0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
ax1.semilogy(vterm, itot, color="k", lw=2, label=r"total (with $R_s$ = 50 $\Omega$)")
vv = np.linspace(0.05, 0.9, 300)
ax1.semilogy(vv, Is * np.exp(vv / VT), color=PALETTE[0], ls="--", label=r"ideal diffusion, $\eta$ = 1")
ax1.semilogy(vv, AREA * Q * NI * W04 / (2 * TAU0) * np.exp(vv / (2 * VT)), color=PALETTE[1], ls="--",
             label=r"recombination, $\eta$ = 2")
ax1.set_xlim(0, 0.9)
ax1.set_ylim(1e-13, 1e-1)
ax1.set_xlabel("terminal voltage (V)")
ax1.set_ylabel("current (A)")
ax1.set_title("(a) forward I–V, 100 µm × 100 µm P$^+$N diode")
ax1.legend(loc="lower right", fontsize=8)
eta = np.gradient(vterm, np.log(itot), edge_order=2) / VT
ax2.plot(vterm, eta, color="k")
ax2.axhline(1, color=PALETTE[0], ls=":", lw=1)
ax2.axhline(2, color=PALETTE[1], ls=":", lw=1)
ax2.set_xlim(0, 0.9)
ax2.set_ylim(0.8, 3.0)
ax2.set_xlabel("terminal voltage (V)")
ax2.set_ylabel(r"local ideality factor $\eta$")
ax2.set_title("(b) ideality factor")
ax2.text(0.08, 2.1, "recombination", fontsize=8, color=PALETTE[1])
ax2.text(0.48, 1.07, "diffusion", fontsize=8, color=PALETTE[0])
ax2.text(0.62, 2.5, "high injection\n+ series resistance", fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/real-diode-iv.svg")
plt.close(fig)


# ---------------------------------------------------------------- figure 3
def recovery(ratio, L=12.0, n=2401, dt=1e-4, tmax=1.0, snaps=(0.0, 0.05, 0.1, 0.2275)):
    xg = np.linspace(0, L, n)
    h = xg[1] - xg[0]
    N = n - 1
    main = np.full(N, -2.0 / h ** 2 - 1.0)
    up = np.full(N - 1, 1.0 / h ** 2)
    up[0] = 2.0 / h ** 2
    lo = np.full(N - 1, 1.0 / h ** 2)
    b = np.zeros(N)
    b[0] = -2 * ratio / h
    A1 = np.zeros((3, N))
    A1[0, 1:] = -0.5 * dt * up
    A1[1, :] = 1 - 0.5 * dt * main
    A1[2, :-1] = -0.5 * dt * lo
    u = np.exp(-xg[:N])
    ts, u0, qs, prof = [0.0], [1.0], [trapezoid(u, xg[:N])], {0.0: u.copy()}
    t = 0.0
    want = sorted(s for s in snaps if s > 0)
    while t < tmax:
        rhs = u + 0.5 * dt * (main * u + np.concatenate([up * u[1:], [0]]) + np.concatenate([[0], lo * u[:-1]])) + dt * b
        u = solve_banded((1, 1), A1, rhs)
        t += dt
        ts.append(t)
        u0.append(u[0])
        qs.append(trapezoid(u, xg[:N]))
        if want and t >= want[0] - 1e-12:
            prof[want.pop(0)] = u.copy()
        if u[0] < -0.5:
            break
    return xg[:N], np.array(ts), np.array(u0), np.array(qs), prof


xg, ts, u0, qs, prof = recovery(1.0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
ax1.plot(ts, u0, color=PALETTE[0], label=r"edge excess $\Delta p(0,t)/\Delta p(0,0)$")
ax1.plot(ts, qs, color=PALETTE[2], label="stored charge (diffusion solution)")
tcc = np.linspace(0, 1, 200)
ax1.plot(tcc, -1 + 2 * np.exp(-tcc), color=PALETTE[1], ls="--", label="stored charge (charge control)")
ax1.axhline(0, color="k", lw=0.6)
ax1.axvline(0.2275, color=PALETTE[0], ls=":", lw=1)
ax1.axvline(math.log(2), color=PALETTE[1], ls=":", lw=1)
ax1.text(0.235, 0.85, "$t_s$ = 0.2275$\\tau_p$\n(exact)", fontsize=8, color=PALETTE[0])
ax1.text(0.70, 0.55, "0.693$\\tau_p$\n(charge\ncontrol)", fontsize=8, color=PALETTE[1])
ax1.set_xlim(0, 1)
ax1.set_ylim(-0.4, 1.05)
ax1.set_xlabel(r"time after switching $t/\tau_p$")
ax1.set_ylabel("normalized value")
ax1.set_title(r"(a) turn-off with $I_R = I_F$")
ax1.legend(loc="lower left", fontsize=8)
for i, (tt, uu) in enumerate(sorted(prof.items())):
    ax2.plot(xg, uu, color=PALETTE[i], label=f"$t$ = {tt:g}$\\tau_p$")
ax2.axhline(0, color="k", lw=0.6)
ax2.set_xlim(0, 3)
ax2.set_ylim(-0.05, 1.05)
ax2.set_xlabel(r"distance from depletion edge $x'/L_p$")
ax2.set_ylabel(r"$\Delta p/\Delta p(0,0)$")
ax2.set_title("(b) the edge empties first")
ax2.legend(loc="upper right", fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/reverse-recovery.svg")
plt.close(fig)


# ---------------------------------------------------------------- figure 4
def an(F):
    return 3.318e5 * np.exp(-1.174e6 / F)


def ap(F):
    return np.where(F < 5.3e5, 2e6 * np.exp(-1.97e6 / F), 5.6e5 * np.exp(-1.32e6 / F))


def ion_integral(Em, N, n=6001):
    W = EPS * Em / (Q * N)
    xx = np.linspace(0, W, n)
    F = np.maximum(Em * (1 - xx / W), 1e3)
    a, b = an(F), ap(F)
    return trapezoid(a * np.exp(-cumulative_trapezoid(a - b, xx, initial=0)), xx)


def breakdown(N):
    Es = np.geomspace(1.5e5, 1.2e6, 80)
    f = np.array([ion_integral(E, N) - 1 for E in Es])
    i = int(np.argmax(f > 0))
    Em = brentq(lambda E: ion_integral(E, N) - 1, Es[i - 1], Es[i], xtol=10)
    W = EPS * Em / (Q * N)
    return Em, Em * W / 2 - VT * math.log(1e19 * N / NI ** 2)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
F = np.linspace(1.5e5, 1e6, 400)
ax1.semilogy(F / 1e5, an(F), color=PALETTE[0], label=r"electrons $\alpha_n$ (Maes 1990)")
ax1.semilogy(F / 1e5, ap(F), color=PALETTE[1], label=r"holes $\alpha_p$ (Grant 1973)")
ax1.axvline(4.43, color="k", ls=":", lw=1)
ax1.text(4.55, 2e1, "fits cross\n(see text)", fontsize=8)
ax1.set_xlabel(r"electric field ($10^5$ V/cm)")
ax1.set_ylabel(r"ionization coefficient (cm$^{-1}$)")
ax1.set_title("(a) impact ionization in silicon, 300 K")
ax1.legend(loc="lower right", fontsize=8)
Ns = np.geomspace(1e15, 1e17, 17)
res = np.array([breakdown(N) for N in Ns])
ax2.loglog(Ns, res[:, 1], color="k", lw=2, label="ionization integral (this chapter)")
ax2.loglog(Ns, 15 * (1e17 / Ns) ** 0.6, color=PALETTE[2], ls="--", label="Hu's rule $15(10^{17}/N)^{0.6}$ V")
vfix = EPS * 9e10 / (2 * Q * Ns) - VT * np.log(1e19 * Ns / NI ** 2)
ax2.loglog(Ns, vfix, color=PALETTE[4], ls="-.", label=r"fixed $\mathcal{E}_c$ = 3×10$^5$ V/cm")
ax2.set_xlabel(r"doping of lightly doped side (cm$^{-3}$)")
ax2.set_ylabel("breakdown voltage (V)")
ax2.set_title("(b) one-sided step junction")
ax2.set_ylim(1, 500)
ax2.legend(loc="lower left", fontsize=8)
ax3 = ax2.twinx()
ax3.semilogx(Ns, res[:, 0] / 1e5, color=PALETTE[0], lw=1)
ax3.set_ylabel(r"peak field at breakdown ($10^5$ V/cm)", color=PALETTE[0])
ax3.tick_params(axis="y", colors=PALETTE[0])
ax3.set_ylim(0, 8)
fig.tight_layout()
save(fig, f"{OUT}/avalanche-breakdown.svg")
plt.close(fig)
print("figures written to", OUT)
