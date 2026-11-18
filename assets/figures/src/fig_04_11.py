#!/usr/bin/env python3
"""Figures for chapter 04-11 (introduction to solid-state physics).

Run from anywhere:  python assets/figures/src/fig_04_11.py
Outputs SVGs to assets/figures/04-11/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-11"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
H = 6.62607015e-34
E_CH = 1.602176634e-19
ME = 9.1093837139e-31
KB = 1.380649e-23
HBAR = H / (2 * math.pi)


def chain_levels(n_atoms, e0=0.0, t=1.0):
    """Eigenvalues of an open tight-binding chain: E0 on the diagonal, -t between neighbors."""
    if n_atoms == 1:
        return np.array([e0])
    h = np.diag(np.full(n_atoms, e0)) - t * (np.eye(n_atoms, k=1) + np.eye(n_atoms, k=-1))
    return np.linalg.eigvalsh(h)


def fig_bands_from_atoms():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9), gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axes[0]
    sizes = [1, 2, 3, 4, 6, 10, 30, 100]
    for i, n in enumerate(sizes):
        for e in chain_levels(n):
            ax.plot([i - 0.32, i + 0.32], [e, e], color=B, lw=1.2 if n < 30 else 0.5)
        # a second atomic level 6 eV higher, with weaker coupling (t = 0.6 eV)
        for e in chain_levels(n, e0=6.0, t=0.6):
            ax.plot([i - 0.32, i + 0.32], [e, e], color=O, lw=1.2 if n < 30 else 0.5)
    ax.axhspan(2.0, 6.0 - 1.2, color=G, alpha=0.12)
    ax.text(len(sizes) - 1.5, 3.4, "band gap", ha="center", fontsize=8.5, color=G)
    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels([str(n) for n in sizes])
    ax.set_xlabel("number of atoms in the chain")
    ax.set_ylabel("electron energy (eV, relative to the lower atomic level)")
    ax.set_title("Each atomic level splits into N levels that fill a band", fontsize=9.5)
    ax = axes[1]
    a = 1.0
    k = np.linspace(-math.pi / a, math.pi / a, 400)
    ax.plot(k * a / math.pi, -2 * np.cos(k * a), color=B, lw=2, label="band E₀ − 2t cos ka (t = 1 eV)")
    ax.plot(k * a / math.pi, -2 + (k * a) ** 2, color=O, ls="--", lw=1.5, label="parabola near k = 0 (effective mass)")
    kr = 2 * math.pi * np.arange(-6, 6) / (12 * a)
    ax.plot(kr * a / math.pi, -2 * np.cos(kr * a), "o", color=B, ms=4, label="allowed k for a 12-atom ring")
    ax.set_ylim(-2.4, 2.6)
    ax.set_xlabel("wavenumber k (units of π/a)")
    ax.set_ylabel("energy (eV)")
    ax.set_title("Tight-binding band: width 4t, curvature sets m*", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper center")
    fig.tight_layout()
    save(fig, f"{OUT}/bands-from-atoms.svg")


def fig_fermi_dirac():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    x = np.linspace(-0.6, 0.6, 600)
    ax.plot(x, np.where(x < 0, 1.0, 0.0), color="0.3", lw=1.5, label="0 K")
    for T, col in ((300, B), (1000, O), (3000, G)):
        kt = KB * T / E_CH
        ax.plot(x, 1 / (1 + np.exp(x / kt)), color=col, lw=2, label=f"{T} K (kT = {kt * 1000:.0f} meV)")
    ax.set_xlabel("E − E_F (eV)")
    ax.set_ylabel("occupation probability f(E)")
    ax.set_title("Fermi–Dirac distribution: the edge blurs over a few kT", fontsize=9.5)
    ax.legend(fontsize=8)
    ax = axes[1]
    ef = 7.04
    e = np.linspace(0, 9, 900)
    g = np.sqrt(e)
    t_show = 3000.0
    f = 1 / (1 + np.exp((e - ef) / (KB * t_show / E_CH)))
    ax.plot(e, g, color="0.4", lw=1.2, label="density of states g(E) ∝ √E")
    ax.fill_between(e, 0, g * np.where(e < ef, 1, 0), color=B, alpha=0.25, label="filled at 0 K")
    ax.plot(e, g * f, color=O, lw=2, label=f"filled at {t_show:.0f} K (exaggerated)")
    ax.axvline(ef, color="0.3", ls=":", lw=1)
    ax.text(ef + 0.1, 0.3, "E_F = 7.04 eV (copper)", fontsize=8)
    ax.annotate("only electrons within a few kT\nof E_F can gain thermal energy", xy=(ef - 0.25, 2.5), xytext=(3.9, 3.3),
                fontsize=8, arrowprops={"arrowstyle": "->", "color": "0.3"})
    ax.set_ylim(0, 3.9)
    ax.set_xlabel("electron energy E (eV)")
    ax.set_ylabel("electrons per unit energy (arb. units)")
    ax.set_title("Free-electron gas in copper (Sommerfeld)", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/fermi-dirac.svg")


def nfe_bands(k, a, u, u2=0.0, n_g=15):
    """Plane-wave bands for V(x) = 2u cos(2πx/a) + 2u2 cos(4πx/a), in eV."""
    g = 2 * math.pi / a
    gs = g * np.arange(-(n_g // 2), n_g // 2 + 1)
    h = np.diag(HBAR**2 * (k + gs) ** 2 / (2 * ME) / E_CH)
    h += u * (np.eye(n_g, k=1) + np.eye(n_g, k=-1)) + u2 * (np.eye(n_g, k=2) + np.eye(n_g, k=-2))
    return np.linalg.eigvalsh(h)


def fig_bands_and_gaps():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axes[0]
    a, u, u2 = 0.5e-9, 0.35, 0.25
    ks = np.linspace(-2 * math.pi / a, 2 * math.pi / a, 801)
    free = HBAR**2 * ks**2 / (2 * ME) / E_CH
    ax.plot(ks * a / math.pi, free, color="0.5", ls="--", lw=1.2, label="free electron ħ²k²/2m")
    # extended-zone scheme: band n occupies n·π/a < |k| < (n+1)·π/a
    e_ext = []
    for kk in ks:
        n_band = min(int(abs(kk) * a / math.pi), 2)
        e_ext.append(nfe_bands(kk, a, u, u2)[n_band])
    e_ext = np.array(e_ext)
    for lo, hi in ((0, 1), (1, 2), (2, 2.001)):
        m = (np.abs(ks) * a / math.pi >= lo) & (np.abs(ks) * a / math.pi < hi)
        for sgn in (1, -1):
            mm = m & (np.sign(ks) == sgn)
            ax.plot(ks[mm] * a / math.pi, e_ext[mm], color=B, lw=2)
    for n_band, (lo, hi) in enumerate(((0, 1), (1, 2))):
        el = nfe_bands(math.pi / a * (n_band + 1), a, u, u2)
        ax.axhspan(el[n_band], el[n_band + 1], color=G, alpha=0.15)
    ax.text(-1.9, 1.5, "gap at k = ±π/a", fontsize=8, color=G)
    ax.text(-1.9, 6.35, "gap at k = ±2π/a", fontsize=8, color=G)
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 7.5)
    ax.set_xlabel("wavenumber k (units of π/a)")
    ax.set_ylabel("energy (eV)")
    ax.set_title("Weak periodic potential: gaps open where Bragg reflection occurs", fontsize=9.5)
    ax.legend(fontsize=8, loc="upper center")
    ax = axes[1]
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 10)
    ax.axis("off")
    specs = [("metal\n(copper)", [(1.0, 6.5, 0.55)], None),
             ("semiconductor\n(silicon, 1.12 eV)", [(1.0, 4.0, 1.0), (5.12, 8.3, 0.0)], 0.06),
             ("insulator\n(diamond 5.5 eV,\nSiO₂ ≈ 9 eV)", [(0.5, 2.5, 1.0), (8.0, 9.0, 0.0)], None)]
    for i, (name, bands, thermal) in enumerate(specs):
        x0 = 0.15 + i
        for lo, hi, fill in bands:
            ax.add_patch(Rectangle((x0, lo), 0.7, hi - lo, fill=False, ec="0.3", lw=1.2))
            if fill > 0:
                ax.add_patch(Rectangle((x0, lo), 0.7, (hi - lo) * fill, color=B, alpha=0.55, lw=0))
        if thermal:
            ax.add_patch(Rectangle((x0, 5.12), 0.7, 0.25, color=O, alpha=0.7, lw=0))
            ax.add_patch(Rectangle((x0, 3.75), 0.7, 0.25, color="white", lw=0))
            ax.add_patch(Rectangle((x0, 3.75), 0.7, 0.25, fill=False, ec=O, lw=1, hatch="///"))
        ax.text(x0 + 0.35, -0.3, name, ha="center", va="top", fontsize=8)
    ax.text(1.5, 9.9, "filled states shaded; thermally excited electrons (orange)\nand the holes they leave (hatched)",
            ha="center", va="top", fontsize=7.5)
    ax.set_title("Band filling decides metal, semiconductor or insulator", fontsize=9.5)
    fig.tight_layout()
    save(fig, f"{OUT}/bands-and-gaps.svg")


if __name__ == "__main__":
    fig_bands_from_atoms()
    fig_fermi_dirac()
    fig_bands_and_gaps()
