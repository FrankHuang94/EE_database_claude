#!/usr/bin/env python3
"""Figures for chapter 19-03 (combinational logic families).

Run from anywhere:  python assets/figures/src/fig_19_03.py
Outputs
  assets/figures/19-03/fanin-elmore.svg     Elmore constant of an N-input NAND pull-down sized for unit drive
                                            (R = 10 kOhm, 0.5 fF per unit width of diffusion, 10 fF external load),
                                            split into the internal-node term R c N(N-1)/2 and the output term
                                            R[(1 + mu) c N + C_ext], for N = 1 to 8
  assets/figures/19-03/charge-sharing.svg   output of a dynamic gate (10 fF, precharged to 1.2 V, VTN0 = 0.35 V)
                                            after charge sharing with an internal node of 0 to 20 fF, without body
                                            effect and with gamma_B = 0.4 V^0.5, against a 0.6 V switching threshold
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import logic as lg  # noqa: E402

OUT = "assets/figures/19-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 1: fan-in and the Elmore constant
R, C, CEXT = 10e3, 0.5e-15, 10e-15
n = np.arange(1, 9)
quad = R * C * n * (n - 1) / 2 * 1e12
lin = R * (3 * C * n + CEXT) * 1e12
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.bar(n, lin, color=PALETTE[0], label="output node: $R[(1+\\mu)cN + C_{ext}]$")
ax.bar(n, quad, bottom=lin, color=PALETTE[1], label="internal nodes: $Rc\\,N(N-1)/2$")
for ni, tot in zip(n, lin + quad):
    ax.text(ni, tot + 4, f"{lg.LN2 * tot:.0f}", ha="center", fontsize=8)
ax.set_xlabel("fan-in N (NAND-N sized for unit drive)")
ax.set_ylabel("Elmore constant (ps)")
ax.set_title("labels: estimated fall delay 0.69 τ (ps)", fontsize=9)
ax.legend(loc="upper left")
save(fig, f"{OUT}/fanin-elmore.svg")

# ---------------------------------------------------------------- figure 2: charge sharing
ca = np.linspace(0, 20e-15, 401)
plain = [lg.charge_sharing(1.2, 0.35, 10e-15, x) for x in ca]
vx = lg.nmos_pass_high(1.2, 0.35, 0.4, 0.8)
body = [1.2 - x / 10e-15 * vx if 1.2 * 10 / (10 + x * 1e15) >= vx else 1.2 * 10 / (10 + x * 1e15) for x in ca]
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(ca * 1e15, plain, color=PALETTE[0], label="no body effect")
ax.plot(ca * 1e15, body, color=PALETTE[2], ls="--", label="$\\gamma_B$ = 0.4 V$^{1/2}$")
ax.axhline(0.6, color=PALETTE[1], lw=1)
ax.text(19.5, 0.62, "next stage switches (0.6 V)", ha="right", fontsize=8, color=PALETTE[1])
ax.axvline(0.35 / 0.85 * 10, color="0.6", ls=":", lw=1)
ax.text(0.35 / 0.85 * 10 + 0.3, 1.12, "cut-off ends\n($C_a/C_L$ = 0.412)", fontsize=8, color="0.4")
ax.plot([3, 12], [0.945, 0.545], "o", color=PALETTE[0], ms=4)
ax.set_xlabel("internal-node capacitance $C_a$ (fF), with $C_L$ = 10 fF")
ax.set_ylabel("output after charge sharing (V)")
ax.set_ylim(0.3, 1.25)
ax.set_xlim(0, 20)
ax.legend(loc="lower left")
save(fig, f"{OUT}/charge-sharing.svg")
