#!/usr/bin/env python3
"""Figures for chapter 19-06 (power and low-power design).

Run from anywhere:  python assets/figures/src/fig_19_06.py
Outputs
  assets/figures/19-06/short-circuit.svg   supply current of an unloaded symmetric inverter (beta = 200 uA/V^2,
                                           VT = 0.35 V, VDD = 1.2 V) during a 50 ps input ramp, from its static
                                           transfer curve, with the shaded area equal to Veendrick's charge
  assets/figures/19-06/min-energy.svg      energy per operation against supply for subthreshold logic
                                           (alpha = 0.1, logic depth 20, n = 1.3, 300 K), split into switching and
                                           leakage, with the minimum-energy point marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import power as pw  # noqa: E402

OUT = "assets/figures/19-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 1: short-circuit current
beta, vt, vdd, tau = 200e-6, 0.35, 1.2, 50e-12
t = np.linspace(0, tau, 1001)
vin = vdd * t / tau
i = np.minimum(0.5 * beta * np.clip(vin - vt, 0, None) ** 2, 0.5 * beta * np.clip(vdd - vin - vt, 0, None) ** 2)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.fill_between(t * 1e12, i * 1e6, color=PALETTE[0], alpha=0.3)
ax.plot(t * 1e12, i * 1e6, color=PALETTE[0], label="supply current")
ax2 = ax.twinx()
ax2.plot(t * 1e12, vin, color=PALETTE[1], ls="--", label="input")
ax2.set_ylabel("input voltage (V)", color=PALETTE[1])
ax.set_xlabel("time during the input ramp (ps)")
ax.set_ylabel("current (µA)")
q = pw.short_circuit_charge_numeric(beta, vdd, vt, tau)
ax.text(40, 4.5, f"shaded area = {q * 1e15:.4f} fC", ha="center", fontsize=9, color=PALETTE[0])
ax.set_title("both transistors conduct while VT < v_in < VDD − VT", fontsize=9)
save(fig, f"{OUT}/short-circuit.svg")

# ---------------------------------------------------------------- figure 2: minimum energy
v = np.linspace(0.08, 0.5, 400)
nvt = 1.3 * pw.VT_300K
sw = 0.1 * v ** 2
lk = 20 * v ** 2 * np.exp(-v / nvt)
vm = pw.minimum_energy_supply(0.1, 20, 1.3)
emin = pw.energy_per_op(vm, 0.1, 20, 1.3)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(v * 1e3, (sw + lk) / emin, color=PALETTE[0], lw=2, label="total")
ax.plot(v * 1e3, sw / emin, color=PALETTE[2], ls="--", label="switching α V²")
ax.plot(v * 1e3, lk / emin, color=PALETTE[1], ls=":", label="leakage over the cycle")
ax.plot([vm * 1e3], [1.0], "o", color=PALETTE[0])
ax.annotate(f"minimum at {vm * 1e3:.0f} mV", (vm * 1e3, 1.0), (vm * 1e3 + 40, 0.5), fontsize=9,
            arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("supply (mV)")
ax.set_ylabel("energy per operation (relative to the minimum)")
ax.set_ylim(0, 4)
ax.legend(loc="upper left")
save(fig, f"{OUT}/min-energy.svg")
