#!/usr/bin/env python3
"""Figures for chapter 09-14 (optoelectronic devices).

Run from anywhere:  python assets/figures/src/fig_09_14.py
Outputs to assets/figures/09-14/:
- solar-cell-iv.svg: J-V and P-V curves of an ideal cell with J_sc = 40 mA/cm^2 and J_0 = 1e-13 A/cm^2 at 300 K,
  with the maximum-power point marked;
- spad-tof-histogram.svg: a seeded simulation of a SPAD time-of-flight histogram for a target at 5 m: 2000 pulses,
  0.1 detected signal photons per pulse with 100 ps rms jitter, 0.2 ambient detections per pulse uniform over
  100 ns, 20 ps bins.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-14"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

Q = 1.602176634e-19
VT = 1.380649e-23 * 300 / Q
JSC, J0 = 40e-3, 1e-13
voc = VT * math.log(JSC / J0 + 1)
J = lambda v: JSC - J0 * (np.exp(v / VT) - 1)
r = minimize_scalar(lambda v: -v * J(v), bounds=(0, voc), method="bounded", options={"xatol": 1e-12})
vmp = r.x

fig, ax = plt.subplots(figsize=(6.0, 4.0))
v = np.linspace(0, voc * 1.005, 400)
ax.plot(v, J(v) * 1e3, color=PALETTE[0], label="J (mA/cm²)")
ax.plot(v, v * J(v) * 1e3, color=PALETTE[1], label="P (mW/cm²)")
ax.plot([vmp], [J(vmp) * 1e3], "o", color=PALETTE[0], ms=5)
ax.plot([vmp], [vmp * J(vmp) * 1e3], "o", color=PALETTE[1], ms=5)
ax.axvline(vmp, color="k", ls=":", lw=0.8)
ax.annotate(f"maximum power\n$V_{{mp}}$ = {vmp:.3f} V", (vmp, vmp * J(vmp) * 1e3), xytext=(0.25, 15), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.6))
ax.text(voc - 0.02, 2, f"$V_{{oc}}$ = {voc:.3f} V", ha="right", fontsize=8)
ax.set_xlim(0, 0.72)
ax.set_ylim(0, 45)
ax.set_xlabel("V (V)")
ax.set_title("Ideal solar cell, $J_{sc}$ = 40 mA/cm², $J_0$ = 10⁻¹³ A/cm², 300 K", fontsize=9)
ax.legend(fontsize=8, loc="center left")
fig.tight_layout()
save(fig, f"{OUT}/solar-cell-iv.svg")
plt.close(fig)

rng = np.random.default_rng(914)
c = 2.99792458e8
t_true = 2 * 5.0 / c
pulses = 2000
times = np.concatenate([rng.normal(t_true, 100e-12, rng.poisson(0.1 * pulses)),
                        rng.uniform(0, 100e-9, rng.poisson(0.2 * pulses))])
counts, edges = np.histogram(times, bins=np.arange(0, 100e-9 + 20e-12, 20e-12))
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.6))
axs[0].plot(edges[:-1] * 1e9, counts, color=PALETTE[0], lw=0.6)
axs[0].set_xlabel("arrival time (ns)")
axs[0].set_ylabel("counts per 20 ps bin")
axs[0].set_title("(a) full histogram, 2000 pulses", fontsize=9)
sel = (edges[:-1] > 32e-9) & (edges[:-1] < 35e-9)
axs[1].bar(edges[:-1][sel] * 1e9, counts[sel], width=0.02, color=PALETTE[1])
axs[1].axvline(t_true * 1e9, color="k", ls=":", lw=0.8)
axs[1].set_xlabel("arrival time (ns)")
axs[1].set_title("(b) zoom on the target: 33.4 ns = 5.00 m", fontsize=9)
fig.tight_layout()
save(fig, f"{OUT}/spad-tof-histogram.svg")
plt.close(fig)
print("figures written to", OUT)
