#!/usr/bin/env python3
"""Figures for chapter 19-05 (interconnect).

Run from anywhere:  python assets/figures/src/fig_19_05.py
Outputs
  assets/figures/19-05/line-step.svg      far-end step response of a distributed RC line (Fourier series) against a
                                          lumped RC with the same total R and C and a single pole with the Elmore
                                          time constant RC/2, with the 50% crossings marked
  assets/figures/19-05/repeaters.svg      delay against wire length for Example 19-05.3's wire (13.3 Ohm/um,
                                          0.198 fF/um): unrepeated (driven by one repeater of the optimal size) and
                                          optimally repeated (R0 = 10 kOhm, C0 = 0.1 fF), on log-log axes, from 30 um (about one optimal segment)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import wires as wr  # noqa: E402

OUT = "assets/figures/19-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 1: step responses
th = np.linspace(0, 2.0, 801)
dist = [wr.line_step_response(x) if x > 0 else 0.0 for x in th]
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(th, dist, color=PALETTE[0], label="distributed line (exact)")
ax.plot(th, 1 - np.exp(-th), color=PALETTE[1], ls="--", label="lumped RC")
ax.plot(th, 1 - np.exp(-2 * th), color=PALETTE[2], ls=":", label="single pole at Elmore RC/2")
ax.axhline(0.5, color="0.6", lw=0.8)
for x, c, dx, y in ((wr.line_t50(), PALETTE[0], 0.03, 0.40), (math.log(2), PALETTE[1], 0.03, 0.40),
                     (math.log(2) / 2, PALETTE[2], -0.22, 0.58)):
    ax.plot([x], [0.5], "o", color=c, ms=4)
    ax.annotate(f"{x:.3f}", (x, 0.5), (x + dx, y), fontsize=8, color=c)
ax.set_xlabel("time / (R C)")
ax.set_ylabel("far-end voltage (normalized)")
ax.set_xlim(0, 2)
ax.set_ylim(0, 1.02)
ax.legend(loc="lower right")
save(fig, f"{OUT}/line-step.svg")

# ---------------------------------------------------------------- figure 2: repeated vs unrepeated
r, c, r0, c0 = 13.3, 0.198e-15, 10e3, 0.1e-15
lengths = np.logspace(np.log10(30), 4, 200)  # um, from about one optimal segment
rep, unrep = [], []
for L in lengths:
    rw, cw = r * L, c * L
    k, h, t = wr.repeater_optimum(r0, c0, rw, cw)
    rep.append(t * 1e12)
    unrep.append(wr.driver_wire_load_delay(r0 / h, rw, cw, h * c0) * 1e12)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.loglog(lengths / 1000, unrep, color=PALETTE[1], label="unrepeated (∝ L²)")
ax.loglog(lengths / 1000, rep, color=PALETTE[0], label="optimally repeated (∝ L)")
ax.plot([1, 5], [123.7, 618.7], "o", color=PALETTE[0], ms=4)
ax.plot([1, 5], [1069.9, 25307.9], "o", color=PALETTE[1], ms=4)
ax.set_xlabel("wire length (mm)")
ax.set_ylabel("delay (ps)")
ax.legend(loc="upper left")
ax.set_title("Example 19-05.4: 13.3 Ω/µm, 0.198 fF/µm, R0C0 = 1 ps", fontsize=9)
save(fig, f"{OUT}/repeaters.svg")
