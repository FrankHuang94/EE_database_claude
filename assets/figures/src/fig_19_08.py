#!/usr/bin/env python3
"""Figures for chapter 19-08 (SRAM design).

Run from anywhere:  python assets/figures/src/fig_19_08.py
Outputs
  assets/figures/19-08/butterfly.svg   butterfly plots of a 6T cell (VDD = 1.0 V, VT = 0.3 V, kN = 200, kP = 100,
                                       kA = 100 uA/V^2): hold (no access transistor) and read (access transistors to
                                       bitlines at VDD), each inverter's transfer curve and its mirror, with the
                                       static noise margins
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sram as sr  # noqa: E402

OUT = "assets/figures/19-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

x = np.linspace(0, 1.0, 801)
fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2), sharey=True)
for ax, kacc, title in ((axes[0], 0.0, "hold"), (axes[1], 100e-6, "read (CR = 2)")):
    y = sr.inverter_vtc(x, 1.0, 0.3, 200e-6, 100e-6, kacc)
    snm = sr.static_noise_margin(1.0, 0.3, 200e-6, 100e-6, kacc)
    ax.plot(x, y, color=PALETTE[0], label="inverter 1")
    ax.plot(y, x, color=PALETTE[1], ls="--", label="inverter 2 (mirrored)")
    ax.set_title(f"{title}: SNM = {snm:.3f} V", fontsize=10)
    ax.set_xlabel("V_Q (V)")
    ax.set_aspect("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
axes[0].set_ylabel("V_QB (V)")
axes[0].legend(loc="upper right", fontsize=8)
save(fig, f"{OUT}/butterfly.svg")
