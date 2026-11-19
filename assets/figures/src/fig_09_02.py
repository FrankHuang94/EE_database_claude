#!/usr/bin/env python3
"""Figures for chapter 09-02 (carriers, doping and the Fermi level).

Run from anywhere:  python assets/figures/src/fig_09_02.py
Outputs SVGs to assets/figures/09-02/:
- dos-fermi-carriers.svg: density of states, Fermi-Dirac occupation and the resulting electron and hole
  distributions for intrinsic and n-type (N_D = 1e16 cm^-3) silicon at 300 K; the carrier distributions
  are drawn on a log scale so that both carrier types are visible;
- fermi-level-vs-doping.svg: E_F - E_i against donor and acceptor concentration at 300 K (course values
  N_C = 3.2e19, N_V = 1.8e19 cm^-3, n_i = 1e10 cm^-3), solved with full Fermi-Dirac statistics, with the band
  edges and the degenerate ranges (E_F within 3 kT of a band edge) shaded;
- n-vs-temperature.svg: electron concentration against temperature for N_D = 1e15 cm^-3 phosphorus
  (E_C - E_D = 45 meV), from charge neutrality with donor ionization and the course n_i(T) model, with n_i(T).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

K = 8.617333262e-5          # eV/K
NC0, NV0, EG, NI0 = 3.2e19, 1.8e19, 1.12, 1.0e10


def F12(eta):
    upper = max(eta, 0.0) + 60.0
    return 2 / math.sqrt(math.pi) * quad(lambda x: math.sqrt(x) / (1 + math.exp(min(x - eta, 700))), 0, upper,
                                         epsabs=0, epsrel=1e-11)[0]


def fig_dos():
    kT = K * 300
    E = np.linspace(-0.85, 0.85, 1200)            # energy from mid-gap, eV
    Ec, Ev = EG / 2, -EG / 2
    gC = np.where(E > Ec, np.sqrt(np.clip(E - Ec, 0, None)), 0.0)
    gV = np.where(E < Ev, np.sqrt(np.clip(Ev - E, 0, None)), 0.0)
    Ei = 0.0
    EF_n = Ei + kT * math.log(1e16 / NI0)
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.6), sharey=True)
    a1, a2, a3 = axes
    a1.plot(gC, E, color=PALETTE[0], label="$g_C(E)$")
    a1.plot(gV, E, color=PALETTE[1], label="$g_V(E)$")
    a1.set_xlabel("density of states (arb.)")
    a1.set_ylabel("E − mid-gap (eV)")
    a1.legend(fontsize=7, loc="center right")
    for EF, lab, col in ((Ei, "intrinsic", "0.4"), (EF_n, "n-type, $10^{16}$ cm$^{-3}$", PALETTE[2])):
        f = 1 / (1 + np.exp((E - EF) / kT))
        a2.plot(f, E, color=col, label=lab)
        a2.axhline(EF, color=col, ls=":", lw=0.8)
    a2.set_xlabel("occupation $f(E)$")
    a2.legend(fontsize=7, loc="lower right")
    for EF, col in ((Ei, "0.4"), (EF_n, PALETTE[2])):
        f = 1 / (1 + np.exp((E - EF) / kT))
        n_E = gC * f
        p_E = gV * (1 - f)
        a3.semilogx(np.where(n_E > 0, n_E, np.nan), E, color=col)
        a3.semilogx(np.where(p_E > 0, p_E, np.nan), E, color=col, ls="--")
    a3.set_xlim(1e-22, 1)
    a3.set_xlabel("$g_Cf$ (solid), $g_V(1-f)$ (dashed)")
    for a in axes:
        a.axhline(Ec, color="0.6", lw=0.6)
        a.axhline(Ev, color="0.6", lw=0.6)
    a1.text(0.02, Ec + 0.02, "$E_C$", fontsize=8)
    a1.text(0.02, Ev - 0.08, "$E_V$", fontsize=8)
    a1.set_ylim(-0.85, 0.85)
    save(fig, f"{OUT}/dos-fermi-carriers.svg")


def ef_from_net(net, T=300.0):
    """E_F - E_i (eV) for net doping N_D - N_A (cm^-3), full ionization, Fermi-Dirac statistics."""
    kT = K * T
    Ec = kT * math.log(NC0 / NI0)            # E_C - E_i with the course constants
    Ev = -kT * math.log(NV0 / NI0)
    def charge(x):
        n = NC0 * F12((x - Ec) / kT)
        p = NV0 * F12((Ev - x) / kT)
        return p - n + net
    return brentq(charge, Ev - 0.3, Ec + 0.3), Ec, Ev


def fig_fermi():
    kT = K * 300
    N = np.logspace(13, 20, 120)
    efn = [ef_from_net(x)[0] for x in N]
    efp = [ef_from_net(-x)[0] for x in N]
    _, Ec, Ev = ef_from_net(1e16)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogx(N, efn, color=PALETTE[0], label="n-type ($N_D$)")
    ax.semilogx(N, efp, color=PALETTE[1], label="p-type ($N_A$)")
    ax.axhline(Ec, color="0.3", lw=1)
    ax.axhline(Ev, color="0.3", lw=1)
    ax.axhline(0, color="0.5", lw=0.8, ls=":")
    ax.axhspan(Ec - 3 * kT, Ec + 0.1, color=PALETTE[0], alpha=0.1)
    ax.axhspan(Ev - 0.1, Ev + 3 * kT, color=PALETTE[1], alpha=0.1)
    ax.text(1.5e13, Ec + 0.015, "$E_C$", fontsize=8)
    ax.text(1.5e13, Ev - 0.05, "$E_V$", fontsize=8)
    ax.text(1.5e13, 0.015, "$E_i$", fontsize=8)
    ax.text(2e19, Ec - 0.07, "degenerate", fontsize=7, ha="center")
    ax.text(2e19, Ev + 0.04, "degenerate", fontsize=7, ha="center")
    ax.set_xlabel("doping (cm$^{-3}$)")
    ax.set_ylabel("$E_F - E_i$ (eV)")
    ax.set_ylim(Ev - 0.1, Ec + 0.1)
    ax.legend(fontsize=8, loc="center right")
    save(fig, f"{OUT}/fermi-level-vs-doping.svg")


def eg(T):
    return 1.17 - 4.73e-4 * T**2 / (T + 636)


def ni(T):
    return NI0 * (T / 300) ** 1.5 * math.exp(eg(300) / (2 * K * 300) - eg(T) / (2 * K * T))


def n_of_T(T, ND=1e15, dE=0.045):
    kT = K * T
    NC = NC0 * (T / 300) ** 1.5
    NV = NV0 * (T / 300) ** 1.5
    nI = ni(T)
    # solve neutrality for u = E_F - E_C (eV): p + N_D+ = n, Boltzmann carriers with n p = n_i^2
    def charge(u):
        n = NC * math.exp(u / kT)
        p = nI**2 / max(n, 1e-300)
        ndp = ND / (1 + 2 * math.exp((u + dE) / kT))
        return p + ndp - n
    u = brentq(charge, -1.5, 0.2)
    return NC * math.exp(u / kT)


def fig_temperature():
    T = np.linspace(20, 700, 400)
    n = np.array([n_of_T(t) for t in T])
    nI = np.array([ni(t) for t in T])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogy(T, n, color=PALETTE[0], label="$n$ ($N_D = 10^{15}$ cm$^{-3}$)")
    ax.semilogy(T, nI, color="0.5", ls="--", label="$n_i(T)$")
    ax.axhline(1e15, color="0.7", lw=0.8, ls=":")
    ax.set_ylim(1e12, 1e17)
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("concentration (cm$^{-3}$)")
    for x, lab in ((40, "freeze-out"), (300, "extrinsic"), (600, "intrinsic")):
        ax.text(x, 3e16, lab, fontsize=8, ha="center")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, f"{OUT}/n-vs-temperature.svg")


if __name__ == "__main__":
    fig_dos()
    fig_fermi()
    fig_temperature()
    print("09-02 figures written to", OUT)
