#!/usr/bin/env python3
"""Figures for chapter 09-11 (CMOS and scaling).

Run from anywhere:  python assets/figures/src/fig_09_11.py
Outputs to assets/figures/09-11/:
- cmos-inverter-vtc.svg: square-law inverter transfer curves at V_DD = 1.0 V, V_TN = |V_TP| = 0.3 V,
  mu_n/mu_p = 2, for W_p = W_n and W_p = 2 W_n, with the V_out = V_in line;
- scaling-power-density.svg: relative power density over five 0.7x nodes for constant-field scaling,
  constant voltage at fixed frequency and constant voltage with frequency rising as 1/delay;
- cpu-clock-power-trend.svg: microprocessor clock frequency and typical power by year from K. Rupp's
  Microprocessor Trend Data (CC-BY 4.0), as copied into the 09-11 lab's data folder.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VDD, VT = 1.0, 0.3


def i_sq(vgs, vds, k):
    vov = vgs - VT
    if vov <= 0:
        return 0.0
    return k * (vov * vds - vds ** 2 / 2) if vds < vov else k * vov ** 2 / 2


def vout(vin, r):
    if vin <= VT:
        return VDD
    if vin >= VDD - VT:
        return 0.0
    return brentq(lambda vo: r * i_sq(vin, vo, 1) - i_sq(VDD - vin, VDD - vo, 1), 0, VDD, xtol=1e-12)


# ------------------------------------------------------------------ figure 1
fig, ax = plt.subplots(figsize=(5.2, 4.2))
vin = np.linspace(0, 1, 801)
for i, (r, lab) in enumerate(((2.0, "$W_p = W_n$ ($k_n/k_p$ = 2)"), (1.0, "$W_p = 2W_n$ ($k_n/k_p$ = 1)"))):
    vo = [vout(x, r) for x in vin]
    ax.plot(vin, vo, color=PALETTE[i], label=lab)
    vm = brentq(lambda x: vout(x, r) - x, VT + 1e-9, VDD - VT - 1e-9)
    ax.plot([vm], [vm], "o", color=PALETTE[i], ms=5)
    ax.annotate(f"$V_M$ = {vm:.3f} V", (vm, vm), xytext=(vm + 0.1, vm + 0.15 - 0.2 * i), fontsize=8,
                color=PALETTE[i])
ax.plot([0, 1], [0, 1], color="k", ls=":", lw=0.8)
ax.set_xlabel("$V_{in}$ (V)")
ax.set_ylabel("$V_{out}$ (V)")
ax.set_title("CMOS inverter, $V_{DD}$ = 1.0 V, $V_{TH}$ = 0.3 V, $\\mu_n/\\mu_p$ = 2", fontsize=9)
ax.legend(fontsize=8, loc="lower left")
fig.tight_layout()
save(fig, f"{OUT}/cmos-inverter-vtc.svg")
plt.close(fig)

# ------------------------------------------------------------------ figure 2
k = 1 / 0.7
n = np.arange(0, 6)
fig, ax = plt.subplots(figsize=(5.6, 4.0))
ax.semilogy(n, np.ones_like(n, dtype=float), marker="o", color=PALETTE[0], label="constant field (Dennard)")
ax.semilogy(n, k ** n, marker="s", color=PALETTE[1], label="constant voltage, fixed frequency")
ax.semilogy(n, k ** (2 * n), marker="^", color=PALETTE[2], label="constant voltage, frequency ∝ 1/delay")
ax.set_xlabel("nodes (0.7× linear shrink each)")
ax.set_ylabel("relative power density")
ax.set_title("Power density under three scaling rules", fontsize=9)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
save(fig, f"{OUT}/scaling-power-density.svg")
plt.close(fig)

# ------------------------------------------------------------------ figure 3
DATA = ROOT / "courses/09-semiconductor-devices/labs/09-11-lab/data"
f = np.loadtxt(DATA / "rupp_frequency_mhz.dat", comments="#")
w = np.loadtxt(DATA / "rupp_power_w.dat", comments="#")
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.semilogy(f[:, 0], f[:, 1], "o", ms=3.5, color=PALETTE[0], label="clock frequency (MHz)")
ax.semilogy(w[:, 0], w[:, 1], "s", ms=3.5, color=PALETTE[1], label="typical power (W)")
ax.axvline(2004, color="k", ls=":", lw=1)
ax.text(2004.5, 0.5, "2004", fontsize=8)
ax.set_xlabel("year of introduction")
ax.set_title("Microprocessors 1971–2021 (data: K. Rupp, CC-BY 4.0)", fontsize=9)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
save(fig, f"{OUT}/cpu-clock-power-trend.svg")
plt.close(fig)
print("figures written to", OUT)
