#!/usr/bin/env python3
"""Figures for chapter 10-04 (small-signal models).

Run from anywhere:  python assets/figures/src/fig_10_04.py
Outputs SVGs to assets/figures/10-04/:
- linearization.svg: the BJT's exponential I_C(V_BE) around 1 mA with its tangent (the small-signal model),
  and the relative error of the tangent against signal amplitude;
- gm-over-id.svg: transconductance efficiency g_m/I_D against overdrive for a MOSFET (strong-inversion
  square law 2/V_ov, the weak-inversion limit 1/(n V_T), n = 1.3, and the smooth EKV interpolation of the lab),
  with the bipolar value 1/V_T.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VT = 1.380649e-23 * 300 / 1.602176634e-19


def fig_linear():
    vbe0 = VT * math.log(1e-3 / 1e-15)
    v = np.linspace(vbe0 - 0.06, vbe0 + 0.04, 400)
    ic = 1e-15 * np.exp(v / VT)
    tangent = 1e-3 + (1e-3 / VT) * (v - vbe0)
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.5))
    a.plot(v, ic * 1e3, color=PALETTE[0], label="$I_C = I_Se^{V_{BE}/V_T}$")
    a.plot(v, tangent * 1e3, color=PALETTE[1], ls="--", label="tangent: $g_m = I_C/V_T$")
    a.plot(vbe0, 1, "o", color="k", ms=5)
    a.set_ylim(0, 4)
    a.set_xlabel("$V_{BE}$ (V)")
    a.set_ylabel("$I_C$ (mA)")
    a.legend(fontsize=8, loc="upper left")
    a.set_title("(a) the small-signal model is the tangent", fontsize=10)
    amp = np.linspace(0.1e-3, 30e-3, 300)
    err = (np.exp(amp / VT) - 1 - amp / VT) / (amp / VT) * 100
    b.plot(amp * 1e3, err, color=PALETTE[0], label="BJT ($2V_T$ scale)")
    vov = 0.2
    b.plot(amp * 1e3, (amp / (2 * vov)) * 100, color=PALETTE[2], label="MOSFET, $V_{ov}$ = 0.2 V")
    b.axhline(10, color="0.6", ls=":")
    b.set_xlabel("signal amplitude (mV)")
    b.set_ylabel("nonlinear part / linear part (%)")
    b.set_ylim(0, 60)
    b.legend(fontsize=8)
    b.set_title("(b) how small is small", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/linearization.svg")


def ekv_gmid(vov, n=1.3):
    """g_m/I_D of the EKV interpolation I_D ~ ln(1 + exp(V_ov/2nV_T))^2, by numerical differentiation."""
    h = 1e-6
    f = lambda x: np.log(np.log1p(np.exp(x / (2 * n * VT))) ** 2)  # noqa: E731
    return (f(vov + h) - f(vov - h)) / (2 * h)


def fig_gmid():
    vov = np.linspace(0.02, 0.6, 300)
    n = 1.3
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ve = np.linspace(-0.2, 0.6, 400)
    ax.plot(ve * 1e3, ekv_gmid(ve, n), color="k", lw=1.6, label="MOSFET, EKV interpolation (smooth)")
    ax.plot(vov * 1e3, 2 / vov, color=PALETTE[0], label="MOSFET, strong inversion: $2/V_{ov}$")
    ax.axhline(1 / (n * VT), color=PALETTE[1], ls="--", label="MOSFET, weak-inversion limit: $1/nV_T$ ($n$ = 1.3)")
    ax.axhline(1 / VT, color=PALETTE[2], ls="-.", label="BJT: $1/V_T$")
    ax.axvline(2 * n * VT * 1e3, color="0.6", ls=":")
    ax.text(2 * n * VT * 1e3 + 5, 70, "$V_{ov} = 2nV_T$", fontsize=8, color="0.3")
    ax.set_ylim(0, 80)
    ax.set_xlabel("overdrive $V_{ov}$ (mV)")
    ax.set_ylabel("$g_m/I_D$ (1/V)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/gm-over-id.svg")


if __name__ == "__main__":
    fig_linear()
    fig_gmid()
