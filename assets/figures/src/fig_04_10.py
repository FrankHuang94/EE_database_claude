#!/usr/bin/env python3
"""Figures for chapter 04-10 (introduction to quantum mechanics).

Run from anywhere:  python assets/figures/src/fig_04_10.py
Outputs SVGs to assets/figures/04-10/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-10"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
H = 6.62607015e-34
C = 299792458.0
E_CH = 1.602176634e-19
ME = 9.1093837139e-31
HBAR = H / (2 * math.pi)
HC_EV_NM = H * C / E_CH * 1e9


def fig_photons():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    lam = np.logspace(0, 9, 400)          # nm
    ax.loglog(lam, HC_EV_NM / lam, color=B, lw=2)
    marks = [(6e7, "5 GHz radio", 1.5, 1.4), (1550, "1550 nm", 1.5, 1.0), (850, "850 nm", 0.06, 0.25),
             (193, "193 nm DUV", 1.5, 1.4), (13.5, "13.5 nm EUV", 1.5, 1.4)]
    for l, name, fx, fy in marks:
        ax.plot(l, HC_EV_NM / l, "o", color=O)
        ax.text(l * fx, HC_EV_NM / l * fy, name, fontsize=7.5)
    for e, name, col in ((0.02585, "kT at 300 K", "0.5"), (1.12, "silicon band gap", G), (13.6, "hydrogen ionization", P)):
        ax.axhline(e, color=col, ls=":", lw=1)
        ax.text(1e5, e * 1.25, name, fontsize=7.5, color=col)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("photon energy (eV)")
    ax.set_title("E = hc/λ = 1239.8 eV·nm / λ", fontsize=10)
    ax = axes[1]
    f = np.linspace(0, 2.5e15, 300)
    for phi, color, name in ((2.3, O, "work function 2.3 eV"), (4.5, B, "work function 4.5 eV")):
        K = H * f / E_CH - phi
        ax.plot(f / 1e15, np.where(K > 0, K, np.nan), color=color, lw=2, label=name)
        ax.axvline(phi * E_CH / H / 1e15, color=color, ls=":", lw=1)
    ax.set_xlabel("light frequency (10¹⁵ Hz)")
    ax.set_ylabel("maximum kinetic energy of ejected electrons (eV)")
    ax.set_title("Photoelectric effect: slope h/e, threshold set by the work function", fontsize=9.5)
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/photons.svg")


def fig_box():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    L = 1.0
    x = np.linspace(0, L, 400)
    for n, color in ((1, B), (2, O), (3, G)):
        En = n**2
        psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
        axes[0].plot(x, En + 0.6 * psi, color=color, lw=2)
        axes[0].text(1.04, En, f"n = {n}: E = {n*n}E₁", color=color, fontsize=8, va="center")
        axes[0].axhline(En, color=color, ls=":", lw=0.8)
        axes[1].plot(x, psi**2, color=color, lw=2, label=f"n = {n}")
    for ax in axes:
        ax.axvline(0, color="0.2", lw=3)
        ax.axvline(L, color="0.2", lw=3)
        ax.set_xlabel("position x / L")
    axes[0].set_ylabel("energy (units of E₁) and ψ (offset)")
    axes[0].set_title("Infinite well: E_n = n²h²/(8mL²); ψ_n ∝ sin(nπx/L)", fontsize=10)
    axes[0].set_xlim(-0.05, 1.4)
    axes[1].set_ylabel("probability density |ψ|² (1/L)")
    axes[1].set_title("Where the electron is likely to be found", fontsize=10)
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/particle-in-a-box.svg")


def t_exact(E, V0, d, m=ME):
    k = math.sqrt(2 * m * (V0 - E) * E_CH) / HBAR
    return 1 / (1 + V0**2 * math.sinh(k * d) ** 2 / (4 * E * (V0 - E)))


def fig_tunneling():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    E, V0, d = 1.0, 3.1, 1.2e-9
    k1 = math.sqrt(2 * ME * E * E_CH) / HBAR
    kap = math.sqrt(2 * ME * (V0 - E) * E_CH) / HBAR
    # solve the 4 boundary conditions for incident amplitude 1
    A = np.array([[1, -1, -1, 0], [1j * k1 * -1, -kap, kap, 0],
                  [0, np.exp(kap * d), np.exp(-kap * d), -np.exp(1j * k1 * d)],
                  [0, kap * np.exp(kap * d), -kap * np.exp(-kap * d), -1j * k1 * np.exp(1j * k1 * d)]], dtype=complex)
    rhs = np.array([-1, -1j * k1, 0, 0], dtype=complex)
    r, cc, dd, t = np.linalg.solve(A, rhs)
    x1 = np.linspace(-2e-9, 0, 300)
    x2 = np.linspace(0, d, 200)
    x3 = np.linspace(d, d + 2e-9, 300)
    psi1 = np.exp(1j * k1 * x1) + r * np.exp(-1j * k1 * x1)
    psi2 = cc * np.exp(kap * x2) + dd * np.exp(-kap * x2)
    psi3 = t * np.exp(1j * k1 * x3)
    for xx, ps in ((x1, psi1), (x2, psi2), (x3, psi3)):
        ax.semilogy(xx * 1e9, np.abs(ps) ** 2, color=B, lw=2)
    ax.axvspan(0, d * 1e9, color="0.88")
    ax.text(1.4, 1e-3, "1.2 nm barrier,\n3.1 eV high (shaded)", fontsize=8)
    ax.set_xlabel("position (nm)")
    ax.set_ylabel("|ψ|² (incident wave = 1)")
    ax.set_title("A 1 eV electron decays exponentially inside the barrier", fontsize=10)
    ax.set_ylim(1e-9, 10)
    ax = axes[1]
    dd_ = np.linspace(0.5e-9, 3e-9, 200)
    for m, color, name in ((ME, B, "free-electron mass"), (0.5 * ME, O, "effective mass 0.5 m₀")):
        ax.semilogy(dd_ * 1e9, [t_exact(1.0, 3.1, x, m) for x in dd_], color=color, lw=2, label=name)
    for x in (1.2e-9, 2.0e-9):
        ax.plot(x * 1e9, t_exact(1.0, 3.1, x), "o", color=G)
    ax.set_xlabel("barrier (oxide) thickness (nm)")
    ax.set_ylabel("transmission probability")
    ax.set_title("Tunneling falls about 4× per 0.1 nm of oxide", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/tunneling.svg")


if __name__ == "__main__":
    fig_photons()
    fig_box()
    fig_tunneling()
