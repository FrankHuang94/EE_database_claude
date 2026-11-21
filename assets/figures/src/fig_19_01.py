#!/usr/bin/env python3
"""Figures for chapter 19-01 (the CMOS inverter: static characteristics).

Run from anywhere:  python assets/figures/src/fig_19_01.py
Outputs
  assets/figures/19-01/vtc-regions.svg   transfer curve of the symmetric inverter of Example 19-01.1 (VDD = 1.2 V,
                                         VTN = |VTP| = 0.35 V, kn = kp, lambda = 0.05 1/V) with the five operating
                                         regions shaded, the switching threshold, the unity-gain points and the
                                         noise margins marked
  assets/figures/19-01/vm-sizing.svg     switching threshold against the width ratio Wp/Wn for long-channel
                                         transistors with a mobility ratio of 2.5 (alpha = 2) and for velocity-
                                         saturated ones with a drive ratio of 1.6 at equal widths (alpha = 1.3)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import inverter as iv  # noqa: E402

OUT = "assets/figures/19-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 1: VTC and regions
inv = iv.Inverter(1.2, 0.35, 0.35, 200e-6, 200e-6, 0.05, 0.05)
vin = np.linspace(0, 1.2, 1201)
vout = inv.vtc(vin)
vm = inv.vm()
vil, vih = inv.unity_gain_points()
fig, ax = plt.subplots(figsize=(6.4, 4.6))
bounds = [0, 0.35, None, None, None, 0.85, 1.2]
# region boundaries: NMOS saturated while Vout > Vin - VTN; PMOS saturated while Vout < Vin + |VTP|
b_lo = vin[np.argmax(vout < vin + 0.35)]          # PMOS enters saturation (Vout falls below Vin + |VTP|)
b_hi = vin[np.argmax(vout < vin - 0.35)]          # NMOS enters the linear region
edges = [0, 0.35, b_lo, b_hi, 0.85, 1.2]
labels = ["A\nN off\nP lin", "B\nN sat\nP lin", "C\nboth\nsat", "D\nN lin\nP sat", "E\nN lin\nP off"]
for k in range(5):
    ax.axvspan(edges[k], edges[k + 1], color=PALETTE[k % len(PALETTE)], alpha=0.08 + 0.04 * (k % 2), lw=0)
    ax.text(0.5 * (edges[k] + edges[k + 1]), 1.30, labels[k], ha="center", va="top", fontsize=7)
ax.plot(vin, vout, color=PALETTE[0], lw=2, label="$V_{out}(V_{in})$")
ax.plot([0, 1.2], [0, 1.2], color="gray", lw=0.8, ls=":", label="$V_{out} = V_{in}$")
for x, name in ((vil, "$V_{IL}$"), (vih, "$V_{IH}$")):
    y = inv.vout(x)
    ax.plot([x - 0.08, x + 0.08], [y + 0.08, y - 0.08], color=PALETTE[3], lw=1.2)
    ax.plot(x, y, "o", color=PALETTE[3], ms=4)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(-30, -14) if x < vm else (8, 6), fontsize=8)
ax.plot(vm, vm, "s", color=PALETTE[1], ms=5)
ax.annotate(f"$V_M$ = {vm:.2f} V", (vm, vm), textcoords="offset points", xytext=(8, -4), fontsize=8)
ax.annotate("", xy=(vil, -0.07), xytext=(0, -0.07), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(vil / 2, -0.12, "$NM_L$", ha="center", fontsize=8)
ax.annotate("", xy=(1.2, -0.07), xytext=(vih, -0.07), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text((vih + 1.2) / 2, -0.12, "$NM_H$", ha="center", fontsize=8)
ax.set_xlim(0, 1.2)
ax.set_ylim(-0.18, 1.32)
ax.set_xlabel("input $V_{in}$ (V)")
ax.set_ylabel("output $V_{out}$ (V)")
ax.set_title("Symmetric CMOS inverter: transfer curve and operating regions")
ax.legend(loc="center left", fontsize=7)
save(fig, f"{OUT}/vtc-regions.svg")
plt.close(fig)

# ---------------------------------------------------------------- figure 2: VM against sizing
ratio = np.logspace(np.log10(0.25), np.log10(10), 200)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
for alpha, drive, col, lab in ((2.0, 2.5, PALETTE[0], "long channel ($\\alpha$ = 2), $\\mu_n/\\mu_p$ = 2.5"),
                               (1.3, 1.6, PALETTE[1], "velocity-saturated ($\\alpha$ = 1.3), drive ratio 1.6")):
    vms = [iv.vm_closed_form(1.2, 0.35, 0.35, drive / w, alpha) for w in ratio]
    ax.semilogx(ratio, vms, color=col, lw=1.8, label=lab)
    w_sym = drive
    ax.plot(w_sym, 0.6, "o", color=col, ms=4)
ax.axhline(0.6, color="gray", lw=0.8, ls=":")
ax.set_xlabel("width ratio $W_p/W_n$")
ax.set_ylabel("switching threshold $V_M$ (V)")
ax.set_title("$V_M$ moves slowly with sizing: a factor of 2 shifts it by tens of mV")
ax.legend(fontsize=7)
save(fig, f"{OUT}/vm-sizing.svg")
plt.close(fig)
print("figures written")
