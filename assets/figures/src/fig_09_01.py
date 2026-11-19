#!/usr/bin/env python3
"""Figures for chapter 09-01 (crystals, energy bands and the semiconductor).

Run from anywhere:  python assets/figures/src/fig_09_01.py
Outputs SVGs to assets/figures/09-01/:
- crystal-planes.svg: the diamond cubic cell (atoms generated from the FCC lattice plus a two-atom basis,
  bonds drawn between nearest neighbors) and the (100), (110) and (111) planes of a cube;
- kronig-penney.svg: F(x) = P sin x / x + cos x for the delta-function comb with P = 3 (allowed bands where
  |F| <= 1 shaded), and the resulting E-k diagram in the first Brillouin zone against the free-electron parabola,
  for the parameters of Example 09-01.3 (d = 0.5 nm, m = m0);
- si-gaas-bands.svg: schematic E-k diagrams of Si (indirect gap, conduction minimum drawn near X) and
  GaAs (direct gap at Gamma), drawn as parabolas with the effective masses and gaps used in the chapter;
- band-diagrams.svg: real-space band diagrams of n-type silicon, flat (with vacuum level, electron affinity,
  work function and gap marked) and with a uniform field applied.
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

HBAR, M0, Q = 1.054571817e-34, 9.1093837015e-31, 1.602176634e-19


def diamond_atoms():
    fcc = [(0, 0, 0), (0, .5, .5), (.5, 0, .5), (.5, .5, 0)]
    pts = set()
    for i, j, k in product(range(-1, 2), repeat=3):
        for b in fcc:
            for s in ((0, 0, 0), (.25, .25, .25)):
                p = tuple(round(b[n] + s[n] + (i, j, k)[n], 6) for n in range(3))
                if all(-1e-9 <= c <= 1 + 1e-9 for c in p):
                    pts.add(p)
    return np.array(sorted(pts))


def fig_crystal():
    fig = plt.figure(figsize=(8.4, 2.6))
    ax = fig.add_subplot(1, 4, 1, projection="3d")
    at = diamond_atoms()
    nn = np.sqrt(3) / 4
    for i in range(len(at)):
        for j in range(i + 1, len(at)):
            if abs(np.linalg.norm(at[i] - at[j]) - nn) < 1e-6:
                ax.plot(*zip(at[i], at[j]), color="0.55", lw=1)
    basis2 = np.isclose((at * 4) % 2, 1).all(axis=1)
    ax.scatter(*at[~basis2].T, s=22, color=PALETTE[0], depthshade=False, label="FCC sites")
    ax.scatter(*at[basis2].T, s=22, color=PALETTE[1], depthshade=False, label="+ (¼,¼,¼)")
    ax.set_title("diamond (Si)", fontsize=9)
    cube_edges(ax)
    planes = {
        "(100)": [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)],
        "(110)": [(1, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 1)],
        "(111)": [(1, 0, 0), (0, 1, 0), (0, 0, 1)],
    }
    for n, (name, poly) in enumerate(planes.items()):
        a = fig.add_subplot(1, 4, n + 2, projection="3d")
        cube_edges(a)
        a.add_collection3d(Poly3DCollection([poly], alpha=0.45, facecolor=PALETTE[n + 2], edgecolor="k"))
        a.set_title(name, fontsize=9)
    for n, a in enumerate(fig.axes):
        a.set_xticks([])
        a.set_yticks([])
        a.set_zticks([])
        a.set_box_aspect((1, 1, 1))
        a.view_init(elev=22, azim=15 if n == 2 else -40)   # turn the (110) cube so its plane is seen face-on
    fig.legend(*fig.axes[0].get_legend_handles_labels(), fontsize=7, loc="lower left", ncol=2,
               bbox_to_anchor=(0.04, 0.0), frameon=False)
    save(fig, f"{OUT}/crystal-planes.svg")


def cube_edges(ax):
    for s, e in product(product((0, 1), repeat=3), repeat=2):
        if sum(abs(np.array(s) - np.array(e))) == 1 and s < e:
            ax.plot(*zip(s, e), color="k", lw=0.8)


def fig_kp():
    P, d = 3.0, 0.5e-9
    Ed = HBAR**2 / (2 * M0 * d**2) / Q
    x = np.linspace(1e-4, 3 * np.pi, 4000)
    F = P * np.sin(x) / x + np.cos(x)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.6))
    a1.plot(x / np.pi, F, color=PALETTE[0])
    a1.axhline(1, color="0.4", lw=0.8, ls="--")
    a1.axhline(-1, color="0.4", lw=0.8, ls="--")
    allowed = np.abs(F) <= 1
    a1.fill_between(x / np.pi, -4, 4, where=allowed, color=PALETTE[2], alpha=0.18, label="allowed bands")
    a1.set_ylim(-2.2, 4)
    a1.set_xlabel(r"$x = \alpha d$ (units of $\pi$)")
    a1.set_ylabel(r"$F = P\,\sin x/x + \cos x$")
    a1.legend(loc="upper right", fontsize=8)
    kd = np.arccos(np.clip(F, -1, 1))
    E = Ed * x**2
    a2.plot(kd[allowed] / np.pi, E[allowed], ".", ms=1.5, color=PALETTE[0], label="Kronig–Penney")
    a2.plot(-kd[allowed] / np.pi, E[allowed], ".", ms=1.5, color=PALETTE[0])
    kf = np.linspace(-1, 1, 200)
    for n in (0, 1, 2):          # free-electron parabola folded into the zone
        for sgn in (1, -1):
            kk = kf + sgn * 2 * n
            a2.plot(kf, Ed * (np.pi * kk) ** 2, color="0.6", lw=0.8, ls=":")
    a2.set_ylim(0, Ed * (3 * np.pi) ** 2)
    a2.set_xlim(-1, 1)
    a2.set_xlabel(r"$kd/\pi$")
    a2.set_ylabel("E (eV)")
    a2.plot([], [], color="0.6", ls=":", label="free electron (folded)")
    a2.legend(loc="upper center", fontsize=8)
    save(fig, f"{OUT}/kronig-penney.svg")


def fig_bands():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.6), sharey=True)
    k = np.linspace(-1, 1, 400)
    c = 0.05                      # eV per (k in units of the zone)^2 per unit inverse mass: schematic scale
    # silicon: valence top at Gamma (k = 0); conduction minimum drawn near X (schematic position 0.85)
    for kk, lab in ((k, None),):
        a1.plot(kk, -c * 6 * kk**2 / 0.49, color=PALETTE[1], label="heavy holes")
        a1.plot(kk, -c * 6 * kk**2 / 0.16, color=PALETTE[4], label="light holes")
    for k0 in (0.85, -0.85):
        kk = np.linspace(k0 - 0.3, k0 + 0.3, 100)
        a1.plot(kk, 1.12 + 4 * c * 6 * (kk - k0) ** 2 / 0.98, color=PALETTE[0])
    a1.plot([], [], color=PALETTE[0], label="conduction (6 valleys along <100>)")
    a1.annotate("", xy=(0.85, 1.12), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="0.3"))
    a1.text(0.05, 0.7, "indirect\n1.12 eV", fontsize=8)
    a1.set_xticks([-1, 0, 1])
    a1.set_xticklabels(["X", "Γ", "X"])
    a1.set_title("Si (indirect)", fontsize=9)
    a1.set_ylabel("E (eV, valence-band top = 0)")
    a1.legend(fontsize=7, loc="lower left")
    a2.plot(k, -c * 6 * k**2 / 0.5, color=PALETTE[1], label="holes")
    a2.plot(k[np.abs(k) < 0.5], 1.42 + c * 6 * k[np.abs(k) < 0.5] ** 2 / 0.067, color=PALETTE[0],
            label="conduction (0.067 $m_0$)")
    a2.annotate("", xy=(0, 1.42), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="0.3"))
    a2.text(0.05, 0.6, "direct\n1.42 eV", fontsize=8)
    a2.set_xticks([-1, 0, 1])
    a2.set_xticklabels(["", "Γ", ""])
    a2.set_title("GaAs (direct)", fontsize=9)
    a2.legend(fontsize=7, loc="lower left")
    a1.set_ylim(-1.2, 2.6)
    save(fig, f"{OUT}/si-gaas-bands.svg")


def fig_real_space():
    chi, Eg, dEF = 4.05, 1.12, 0.20     # Si electron affinity, gap; n-type, E_C - E_F (Example 09-01.5)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.6))
    x = np.linspace(0, 1, 10)
    Ec = np.zeros_like(x)
    a1.plot(x, Ec + chi, color="0.4", ls="--", label="$E_0$ (vacuum)")
    a1.plot(x, Ec, color=PALETTE[0], label="$E_C$")
    a1.plot(x, Ec - Eg, color=PALETTE[1], label="$E_V$")
    a1.plot(x, Ec - dEF, color=PALETTE[2], ls=":", label="$E_F$")
    a1.annotate("", xy=(0.08, chi), xytext=(0.08, 0), arrowprops=dict(arrowstyle="<->"))
    a1.text(0.1, chi / 2 + 0.3, "χ = 4.05 eV", fontsize=8)
    a1.annotate("", xy=(0.33, chi), xytext=(0.33, -dEF), arrowprops=dict(arrowstyle="<->"))
    a1.text(0.35, chi / 2 - 0.5, "Φ = 4.25 eV", fontsize=8)
    a1.annotate("", xy=(0.85, 0), xytext=(0.85, -Eg), arrowprops=dict(arrowstyle="<->"))
    a1.text(0.7, -Eg / 2, "$E_g$", fontsize=8)
    a1.set_title("n-type Si, equilibrium", fontsize=9)
    a1.set_xlabel("position (arb.)")
    a1.set_ylabel("electron energy (eV)")
    a1.legend(fontsize=7, loc="center right", bbox_to_anchor=(1.0, 0.62))
    xs = np.linspace(0, 1, 50)          # 1 µm bar, 20 kV/cm along +x: bands rise 2 eV
    a2.plot(xs, 2 * xs, color=PALETTE[0], label="$E_C$")
    a2.plot(xs, 2 * xs - Eg, color=PALETTE[1], label="$E_V$")
    a2.plot(0.7, 1.4 + 0.08, "o", color=PALETTE[0], ms=6)
    a2.annotate("", xy=(0.42, 0.95), xytext=(0.68, 1.47), arrowprops=dict(arrowstyle="->"))
    a2.text(0.12, 1.2, "electron rolls down", fontsize=8)
    a2.plot(0.3, 0.6 - Eg - 0.08, "o", mfc="white", mec=PALETTE[1], ms=6)
    a2.annotate("", xy=(0.58, 1.16 - Eg - 0.1), xytext=(0.32, 0.64 - Eg - 0.1), arrowprops=dict(arrowstyle="->"))
    a2.text(0.6, -0.45, "hole floats up", fontsize=8)
    a2.annotate("", xy=(0.95, -1.0), xytext=(0.65, -1.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    a2.text(0.66, -0.9, r"field $\mathcal{E}$", fontsize=8)
    a2.set_title("uniform field along +x (bands rise 2 eV)", fontsize=9)
    a2.set_xlabel("x (µm)")
    a2.legend(fontsize=7, loc="upper left")
    save(fig, f"{OUT}/band-diagrams.svg")


if __name__ == "__main__":
    fig_crystal()
    fig_kp()
    fig_bands()
    fig_real_space()
    print("09-01 figures written to", OUT)
