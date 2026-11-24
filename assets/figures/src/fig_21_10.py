#!/usr/bin/env python3
"""Figures for chapter 21-10 (antennas, arrays, beamforming and mmWave).

Run from anywhere:  python assets/figures/src/fig_21_10.py
Outputs
  assets/figures/21-10/squint.svg   array factor of the 16-element lambda/2 array of Example 21-10.4 steered to 60 degrees
                                    with phase shifters, at 26, 28 and 30 GHz (the beam squints), and with true-time delay
  assets/figures/21-10/chu.svg      Chu-McLean bound on radiation Q and the VSWR-2 bandwidth it allows against ka, with the
                                    10 mm and 5 mm Bluetooth antennas of Example 21-10.2
  assets/figures/21-10/dcpower.svg  DC power of a 60 dBm EIRP transmit array against element count (Example 21-10.6)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import antenna as ant  # noqa: E402

OUT = "assets/figures/21-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- squint
th = np.linspace(20, 90, 3501)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
for fr, col, lab_ in ((26 / 28, PALETTE[3], "26 GHz"), (1.0, "k", "28 GHz"), (30 / 28, PALETTE[0], "30 GHz")):
    af = ant.array_factor(th, 16, 0.5, 60, fr)
    ax.plot(th, 20 * np.log10(np.maximum(af, 1e-6)), color=col, lw=1.5, label=f"phase shifters, {lab_}")
af = ant.array_factor(th, 16, 0.5, 60, 26 / 28, "ttd")
ax.plot(th, 20 * np.log10(np.maximum(af, 1e-6)), color=PALETTE[2], lw=1.2, ls="--", label="true-time delay, 26 GHz")
ax.axvline(60, color="0.5", lw=0.8, ls=":")
ax.text(60.5, -27, "steered\nto 60°", fontsize=7.5, color="0.4")
ax.set_xlim(20, 90)
ax.set_ylim(-30, 2)
ax.set_xlabel("angle from broadside (degrees)")
ax.set_ylabel("|AF| (dB)")
ax.set_title("A phase-shifter beam squints with frequency; TTD does not", fontsize=10)
ax.legend(loc="upper left", fontsize=7.5)
save(fig, f"{OUT}/squint.svg")

# ---------------------------------------------------------------- Chu limit
ka = np.geomspace(0.1, 1.5, 400)
q = ant.chu_q(ka)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.loglog(ka, q, color=PALETTE[0], lw=1.6, label=r"$Q_{min} = 1/(ka)^3 + 1/ka$")
for r, lab_ in ((0.010, "10 mm sphere"), (0.005, "5 mm sphere")):
    k = 2 * math.pi * 2.44175e9 * r / ant.C0
    ax.plot(k, ant.chu_q(k), "o", color=PALETTE[3], ms=5)
    ax.annotate(f"{lab_}\nQ ≥ {ant.chu_q(k):.1f}", (k, ant.chu_q(k)), textcoords="offset points", xytext=(8, 4),
                fontsize=7.5)
qband = 1 / (83.5 / 2441.75 * math.sqrt(2))
ax.axhline(qband, color=PALETTE[2], lw=1, ls="--")
ax.text(0.105, qband * 1.12, "largest Q that covers 2400–2483.5 MHz", fontsize=7.5, color=PALETTE[2])
ax.set_xlabel("ka (sphere radius × 2π/λ)")
ax.set_ylabel("minimum radiation Q")
ax.set_xlim(0.1, 1.5)
ax.text(0.105, 1.3, "VSWR-2 bandwidth at 100 % efficiency = 0.707/Q", fontsize=7.5, color="0.3")
ax.set_title("The Chu limit: small antennas are narrow-band or lossy", fontsize=10)
ax.legend(loc="upper right", fontsize=8)
save(fig, f"{OUT}/chu.svg")

# ---------------------------------------------------------------- DC power vs N
n = np.arange(16, 513)
e_w, ge, eta, poh = 1000.0, 10 ** 0.5, 0.15, 0.1
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.plot(n, [ant.dc_power_w(x, e_w, ge, eta, poh) for x in n], color=PALETTE[0], lw=1.6, label="total DC power")
ax.plot(n, e_w / (n * ge * eta), color=PALETTE[3], lw=1, ls="--", label="PAs: E/(N G_e η_PA)")
ax.plot(n, n * poh, color=PALETTE[2], lw=1, ls="--", label="overhead: N P_oh")
nopt = ant.optimal_elements(e_w, ge, eta, poh)
ax.plot(nopt, ant.dc_power_w(nopt, e_w, ge, eta, poh), "o", color="k", ms=5)
ax.annotate(f"N* = {nopt:.0f}, {ant.dc_power_w(nopt, e_w, ge, eta, poh):.1f} W", (nopt, 29.0),
            textcoords="offset points", xytext=(10, 18), fontsize=8)
ax.set_xscale("log", base=2)
ax.set_xlim(16, 512)
ax.set_ylim(0, 100)
ax.set_xlabel("number of elements N")
ax.set_ylabel("DC power (W)")
ax.set_title("60 dBm EIRP: PA power falls as 1/N, overhead rises as N", fontsize=10)
ax.legend(loc="upper center", fontsize=8)
save(fig, f"{OUT}/dcpower.svg")
