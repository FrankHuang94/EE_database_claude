#!/usr/bin/env python3
"""Figures for chapter 22-05 (magnetics design).

Run from anywhere:  python assets/figures/src/fig_22_05.py
Outputs
  assets/figures/22-05/gapped-core.svg     (a) a gapped C-core with an N-turn winding, the flux path and the fringing
                                           field at the gap; (b) its magnetic circuit, MMF N·I driving flux through
                                           the core and gap reluctances in series
  assets/figures/22-05/loss-tradeoffs.svg  (a) Dowell's AC-resistance factor F_R against layer thickness Δ = h/δ for
                                           1, 2, 3 and 5 layers; (b) core, copper and total transformer loss against
                                           flux swing with core loss ∝ ΔB^2.253 and copper loss ∝ 1/ΔB², normalized to
                                           the optimum, where P_core/P_cu = 2/β
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import magnetics as mg  # noqa: E402

OUT = "assets/figures/22-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_core():
    fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.6), gridspec_kw={"width_ratios": [1.1, 1]})
    a = ax[0]
    core = dict(facecolor="0.80", edgecolor="0.3", lw=1)
    # C-core: outer 0..4 x 0..3, window 1..3 x 1..2, gap in the right leg at y 1.35..1.65
    a.add_patch(Rectangle((0, 0), 4, 1, **core))
    a.add_patch(Rectangle((0, 2), 4, 1, **core))
    a.add_patch(Rectangle((0, 1), 1, 1, **core))
    a.add_patch(Rectangle((3, 1), 1, 0.35, **core))
    a.add_patch(Rectangle((3, 1.65), 1, 0.35, **core))
    # winding on the left leg
    for y in np.linspace(1.05, 1.95, 7):
        a.plot([-0.15, 1.15], [y, y + 0.06], color=PALETTE[1], lw=2.2, solid_capstyle="round")
    a.text(-0.35, 1.5, "N turns\ncurrent I", ha="right", va="center", fontsize=8, color=PALETTE[1])
    # flux path
    xs = [0.5, 0.5, 3.5, 3.5, 0.5]
    ys = [0.5, 2.5, 2.5, 0.5, 0.5]
    a.plot(xs, ys, color=PALETTE[0], ls="--", lw=1.2)
    a.add_patch(FancyArrowPatch((2.0, 2.5), (2.4, 2.5), arrowstyle="-|>", mutation_scale=12, color=PALETTE[0]))
    a.text(2.0, 2.62, r"flux $\Phi$, path $\ell_e$, area $A_e$", ha="center", fontsize=8, color=PALETTE[0])
    # fringing at the gap: flux crosses the slot vertically and bulges out on both sides
    for x0 in (3.2, 3.5, 3.8):
        a.plot([x0, x0], [1.35, 1.65], color=PALETTE[2], lw=0.9)
    yy = np.linspace(1.35, 1.65, 30)
    for amp in (0.12, 0.22):
        bulge = amp * np.sin(np.pi * (yy - 1.35) / 0.3)
        a.plot(3.0 - bulge, yy, color=PALETTE[2], lw=0.9)
        a.plot(4.0 + bulge, yy, color=PALETTE[2], lw=0.9)
    a.annotate("gap g\n(fringing)", (4.25, 1.5), (4.75, 1.5), fontsize=8, va="center",
               arrowprops=dict(arrowstyle="->", color="0.3"))
    a.set_xlim(-1.6, 5.9)
    a.set_ylim(-0.3, 3.2)
    a.set_aspect("equal")
    a.axis("off")
    a.set_title("(a) gapped core", fontsize=10)
    # (b) magnetic circuit
    b = ax[1]
    b.plot([0, 0, 3, 3, 0], [0, 2, 2, 0, 0], color="0.2", lw=1.2)
    b.add_patch(plt.Circle((0, 1), 0.3, fill=False, lw=1.2, color=PALETTE[1]))
    b.text(0, 1, "+\n−", ha="center", va="center", fontsize=8)
    b.text(-0.45, 1, r"$\mathcal{F} = NI$", ha="right", va="center", fontsize=9, color=PALETTE[1])
    for (x0, y0, lab) in ((1.0, 2, r"$\mathcal{R}_c = \ell_e/(\mu_r\mu_0 A_e)$"), (3, 1.0, r"$\mathcal{R}_g = g/(\mu_0 A_e)$")):
        if y0 == 2:
            b.add_patch(Rectangle((x0, 1.85), 1.0, 0.3, facecolor="white", edgecolor="0.2"))
            b.text(x0 + 0.5, 2.3, lab, ha="center", fontsize=8)
        else:
            b.add_patch(Rectangle((2.85, 0.5), 0.3, 1.0, facecolor="white", edgecolor="0.2"))
            b.text(3.3, 1.0, lab, va="center", fontsize=8)
    b.add_patch(FancyArrowPatch((1.0, 0), (2.0, 0), arrowstyle="-|>", mutation_scale=12, color=PALETTE[0]))
    b.text(1.5, -0.3, r"$\Phi = \mathcal{F}/(\mathcal{R}_c + \mathcal{R}_g)$", ha="center", fontsize=8, color=PALETTE[0])
    b.text(1.5, -0.75, r"$L = N^2/(\mathcal{R}_c + \mathcal{R}_g)$", ha="center", fontsize=9)
    b.set_xlim(-1.6, 5.6)
    b.set_ylim(-1.1, 2.7)
    b.set_aspect("equal")
    b.axis("off")
    b.set_title("(b) magnetic circuit", fontsize=10)
    save(fig, f"{OUT}/gapped-core.svg")


def fig_losses():
    fig, ax = plt.subplots(1, 2, figsize=(8.0, 3.4))
    d = np.linspace(0.05, 3, 400)
    for k, m in enumerate((1, 2, 3, 5)):
        ax[0].semilogy(d, [mg.dowell_fr(x, m) for x in d], color=PALETTE[k], label=f"M = {m}")
    ax[0].set_xlabel("Δ = h/δ")
    ax[0].set_ylabel("F_R = R_ac/R_dc")
    ax[0].set_ylim(0.9, 100)
    ax[0].legend(fontsize=8)
    ax[0].set_title("(a) Dowell: AC resistance of M layers", fontsize=10)
    beta = 2.253
    x = np.linspace(0.4, 2.0, 400)          # ΔB relative to the optimum
    a_core = 2 / beta                       # normalization: at x = 1, P_core = 2/β, P_cu = 1
    pc, pcu = a_core * x ** beta, 1 / x ** 2
    ax[1].plot(x, pc, color=PALETTE[0], label="core ∝ ΔB^β")
    ax[1].plot(x, pcu, color=PALETTE[1], label="copper ∝ 1/ΔB²")
    ax[1].plot(x, pc + pcu, color="0.2", lw=1.8, label="total")
    ax[1].axvline(1, color="0.5", ls=":")
    ax[1].text(1.03, 4.2, "optimum:\nP_core/P_cu = 2/β", fontsize=8)
    ax[1].set_xlabel("flux swing ΔB / ΔB_opt")
    ax[1].set_ylabel("loss / P_cu at optimum")
    ax[1].set_ylim(0, 6)
    ax[1].legend(fontsize=8)
    ax[1].set_title("(b) transformer loss against flux swing (β = 2.253)", fontsize=10)
    save(fig, f"{OUT}/loss-tradeoffs.svg")


if __name__ == "__main__":
    fig_core()
    fig_losses()
