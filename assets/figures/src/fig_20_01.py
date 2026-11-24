#!/usr/bin/env python3
"""Figures for chapter 20-01 (analog design fundamentals, the g_m/I_D method).

Run from anywhere:  python assets/figures/src/fig_20_01.py
Outputs
  assets/figures/20-01/gmid-vs-ic.svg      g_m/I_D against the inversion coefficient: the charge-based model (long
                                           channel and with velocity saturation at 0.15 um), the square law's 2/V_ov,
                                           and the weak-inversion limit 1/(n V_T), with the three regions shaded
  assets/figures/20-01/design-chart.svg    current density, f_T and intrinsic gain against g_m/I_D for L = 0.15, 0.5
                                           and 1 um in the illustrative T130 process
  assets/figures/20-01/sweet-spot.svg      the product (g_m/I_D) f_T against IC for the three lengths, peaks marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import gmid as g  # noqa: E402

OUT = "assets/figures/20-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
p = g.Process()
LENGTHS = (0.15e-6, 0.5e-6, 1e-6)

# ---------------------------------------------------------------- figure 2: g_m/I_D against IC
ics = np.logspace(-3, 3, 400)
long_ = [g.gm_over_id(ic, p.n, p.vt) for ic in ics]
short = [g.gm_over_id(ic, p.n, p.vt, p.lam(0.15e-6)) for ic in ics]
vov = np.array([g.vov_of_ic(ic, p.n, p.vt) for ic in ics])
sq = np.where(vov > 0, 2 / np.where(vov > 0, vov, 1), np.nan)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.axvspan(1e-3, 0.1, color=PALETTE[0], alpha=0.08)
ax.axvspan(0.1, 10, color=PALETTE[2], alpha=0.08)
ax.axvspan(10, 1e3, color=PALETTE[3], alpha=0.08)
ax.text(0.01, 1.2, "weak", ha="center", fontsize=9)
ax.text(1, 1.2, "moderate", ha="center", fontsize=9)
ax.text(100, 1.2, "strong", ha="center", fontsize=9)
ax.loglog(ics, long_, color=PALETTE[0], label="charge-based model, long channel")
ax.loglog(ics, short, color=PALETTE[1], label="with velocity saturation, L = 0.15 µm")
ax.loglog(ics, sq, "--", color=PALETTE[3], label="square law, 2/V_ov")
ax.axhline(1 / (p.n * p.vt), color="k", lw=0.8, ls=":")
ax.text(2e-3, 1 / (p.n * p.vt) * 1.12, "1/(nV_T)", fontsize=9)
ax.set_ylim(1, 300)
ax.set_xlabel("inversion coefficient IC = I_D / I_spec")
ax.set_ylabel("g_m / I_D (S/A)")
ax.legend(loc="upper right", fontsize=8)
save(fig, f"{OUT}/gmid-vs-ic.svg")

# ---------------------------------------------------------------- figure 3: the design chart
targets = np.linspace(3, 28, 101)
fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.6))
for k, L in enumerate(LENGTHS):
    rows = []
    for t in targets:
        ic = g.ic_for_gm_over_id(t, p, L)
        rows.append((g.id_per_w(ic, p, L), g.ft(ic, p, L) / 1e9, g.intrinsic_gain(ic, p, L)))
    rows = np.array(rows)
    lab = f"L = {L * 1e6:.2f} µm"
    axs[0].semilogy(targets, rows[:, 0], color=PALETTE[k], label=lab)
    axs[1].semilogy(targets, rows[:, 1], color=PALETTE[k], label=lab)
    axs[2].plot(targets, rows[:, 2], color=PALETTE[k], label=lab)
axs[0].set_ylabel("current density I_D/W (µA/µm)")
axs[1].set_ylabel("transit frequency f_T (GHz)")
axs[2].set_ylabel("intrinsic gain g_m r_o")
for a in axs:
    a.set_xlabel("g_m / I_D (S/A)")
axs[2].legend(fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/design-chart.svg")

# ---------------------------------------------------------------- figure 4: the sweet spot
fig, ax = plt.subplots(figsize=(6.4, 4.0))
for k, L in enumerate(LENGTHS):
    prod = [g.gm_over_id(ic, p.n, p.vt, p.lam(L)) * g.ft(ic, p, L) / 1e9 for ic in ics]
    ax.loglog(ics, prod, color=PALETTE[k], label=f"L = {L * 1e6:.2f} µm")
    r = minimize_scalar(lambda x: -g.gm_over_id(10 ** x, p.n, p.vt, p.lam(L)) * g.ft(10 ** x, p, L),
                        bounds=(-3, 3), method="bounded")
    icp = 10 ** r.x
    ax.plot([icp], [g.gm_over_id(icp, p.n, p.vt, p.lam(L)) * g.ft(icp, p, L) / 1e9], "o", color=PALETTE[k])
ax.set_xlabel("inversion coefficient IC")
ax.set_ylabel("(g_m / I_D) · f_T (GHz/V)")
ax.legend(fontsize=8)
save(fig, f"{OUT}/sweet-spot.svg")
