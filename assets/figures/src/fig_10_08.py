#!/usr/bin/env python3
"""Figures for chapter 10-08 (current sources and current mirrors).

Run from anywhere:  python assets/figures/src/fig_10_08.py
Outputs SVGs to assets/figures/10-08/:
- mirror-characteristics.svg: output current against output voltage for a basic NMOS mirror and a cascode
  mirror with the same reference (k_n = 4 mA/V^2, V_TN = 0.5 V, lambda = 0.1 1/V, I_ref = 0.2463 mA as in
  Example 10-02.5), solved with the large-signal square law (triode and saturation, channel-length modulation;
  body effect ignored), showing compliance voltage and output resistance;
- mismatch.svg: standard deviation of the current ratio of two mirror transistors against gate area for three
  overdrives, from sigma(dI/I) = (2/V_ov) sigma(dV_TH) with sigma(dV_TH) = A_VT/sqrt(WL), using an illustrative
  A_VT = 3.5 mV um (a process parameter; foundries publish their own).
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

OUT = "assets/figures/10-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
K, VTN, LAM = 4e-3, 0.5, 0.1


def ids(vgs, vds):
    vov = vgs - VTN
    if vov <= 0:
        return 0.0
    if vds < vov:
        return K * (vov - vds / 2) * vds * (1 + LAM * vds)
    return 0.5 * K * vov * vov * (1 + LAM * vds)


VGS1 = brentq(lambda v: (3.3 - v) / 10e3 - ids(v, v), 0.5, 3.3)
IREF = (3.3 - VGS1) / 10e3
# cascode reference: M3 (diode) sits on M1 and carries I_ref with its source at V_GS1
VG3 = VGS1 + brentq(lambda v: IREF - ids(v, v), 0.5, 3.3)


def basic(vout):
    return ids(VGS1, vout)


def cascode(vout):
    # find the middle node V_X where M2's current equals M4's
    def f(vx):
        return ids(VGS1, vx) - ids(VG3 - vx, vout - vx)
    if vout <= 1e-9:
        return 0.0
    vx = brentq(f, 0.0, vout)
    return ids(VGS1, vx)


def fig_characteristics():
    v = np.linspace(0, 3.0, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(v, [basic(x) * 1e3 for x in v], color=PALETTE[0], label="basic mirror")
    ax.plot(v, [cascode(x) * 1e3 for x in v], color=PALETTE[1], label="cascode mirror")
    ax.axhline(IREF * 1e3, color="0.6", ls=":")
    ax.text(2.05, IREF * 1e3 - 0.022, "$I_{ref}$ = 0.246 mA", fontsize=8, color="0.3")
    ax.axvline(VGS1 - VTN, color=PALETTE[0], ls="--", lw=0.8)
    ax.axvline(VTN + 2 * (VGS1 - VTN), color=PALETTE[1], ls="--", lw=0.8)
    ax.text(VGS1 - VTN + 0.03, 0.03, "$V_{ov}$", fontsize=8, color=PALETTE[0])
    ax.text(VTN + 2 * (VGS1 - VTN) + 0.03, 0.03, "$V_{TN} + 2V_{ov}$", fontsize=8, color=PALETTE[1])
    ax.set_xlabel("output voltage $V_{out}$ (V)")
    ax.set_ylabel("output current (mA)")
    ax.set_ylim(0, 0.32)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/mirror-characteristics.svg")


def fig_mismatch():
    area = np.logspace(0, 4, 200)          # um^2
    avt = 3.5                               # mV um, illustrative
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for vov, col in ((0.1, PALETTE[0]), (0.2, PALETTE[1]), (0.4, PALETTE[2])):
        ax.loglog(area, 2 / vov * avt / np.sqrt(area) * 1e-3 * 100, color=col, label=f"$V_{{ov}}$ = {vov} V")
    ax.axhline(0.1, color="0.6", ls=":")
    ax.text(1.2, 0.115, "0.1%", fontsize=8, color="0.3")
    ax.set_xlabel("gate area $WL$ ($\\mu$m²)")
    ax.set_ylabel("$\\sigma(\\Delta I/I)$ (%)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/mismatch.svg")


if __name__ == "__main__":
    fig_characteristics()
    fig_mismatch()
