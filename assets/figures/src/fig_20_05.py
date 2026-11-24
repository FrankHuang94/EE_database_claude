#!/usr/bin/env python3
"""Figures for chapter 20-05 (comparators and sample-and-hold circuits).

Run from anywhere:  python assets/figures/src/fig_20_05.py
Outputs
  assets/figures/20-05/ron.svg      on-resistance against input for the running design's switch: gate at V_DD,
                                    bootstrapped with the body grounded, bootstrapped with the body tied to the source,
                                    and a transmission gate (Problem 20-05.5)
  assets/figures/20-05/jitter.svg   SNR of the running design against input frequency for 0.1, 0.3 and 1 ps of jitter,
                                    with the quantization + kT/C floor
  assets/figures/20-05/regen.svg    latch output against time for three inputs: the current-limited simulation and the
                                    exponential estimate
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sh  # noqa: E402

OUT = "assets/figures/20-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
C = sh.ktc_cap(12, 1.6)
TAU = 0.5 / 100e6 / math.log(2 ** 13)
W = sh.L_MIN / (sh.MU_N * sh.COX * (TAU / C) * (sh.VDD - sh.vth(1.0)))

# ---------------------------------------------------------------- figure 3: on-resistance
vin = np.linspace(0.05, 1.15, 441)


def g(w, vov, mu=sh.MU_N):
    return mu * sh.COX * (w / sh.L_MIN) * vov if vov > 0 else 0.0


def vthp(v):
    return sh.VTH0 + sh.GAMMA_B * (math.sqrt(sh.PHI2 + sh.VDD - v) - math.sqrt(sh.PHI2))


curves = {
    "gate at $V_{DD}$": [g(W, sh.VDD - x - sh.vth(x)) for x in vin],
    "transmission gate (PMOS 3× wider)": [g(W, sh.VDD - x - sh.vth(x)) + g(3 * W, x - vthp(x), 100e-4) for x in vin],
    "bootstrapped, body grounded": [g(W, sh.VDD - sh.vth(x)) for x in vin],
    "bootstrapped, body tied to source": [g(W, sh.VDD - sh.VTH0) for x in vin],
}
fig, ax = plt.subplots(figsize=(6.6, 4.2))
for (lab, gs), col, ls in zip(curves.items(), PALETTE, ("-", "-.", "-", "--")):
    r = np.array([1 / x if x > 0 else np.nan for x in gs])
    ax.semilogy(vin, r, color=col, ls=ls, label=lab)
ax.axhline(TAU / C, color="0.4", lw=0.8)
ax.text(0.06, TAU / C * 1.12, f"settling target {TAU / C:.0f} Ω", fontsize=8, color="0.3")
ax.axvspan(0.2, 1.0, color="0.92", zorder=0)
ax.set_xlabel("input voltage (V)")
ax.set_ylabel("$R_{on}$ (Ω)")
ax.set_ylim(300, 3e4)
ax.legend(loc="upper left", fontsize=8)
ax.set_title("Sampling switch, $W$ = 0.888 µm, $V_{DD}$ = 1.2 V (shaded: input range)")
save(fig, f"{OUT}/ron.svg")

# ---------------------------------------------------------------- figure 4: jitter
f = np.logspace(6, 9.3, 400)
fig, ax = plt.subplots(figsize=(6.6, 4.2))
floor = sh.snr_db(12, 1.6, C)
for sig, col in zip((0.1e-12, 0.3e-12, 1e-12), PALETTE):
    ax.semilogx(f, [sh.snr_db(12, 1.6, C, sig, x) for x in f], color=col, label=f"σ = {sig * 1e12:g} ps")
    ax.semilogx(f, [sh.jitter_snr_db(x, sig) for x in f], color=col, ls=":", lw=0.9)
ax.axhline(floor, color="0.4", lw=0.8)
ax.text(1.2e6, floor + 1, f"quantization + kT/C floor, {floor:.1f} dB", fontsize=8, color="0.3")
ax.set_ylim(30, 80)
ax.set_xlabel("input frequency (Hz)")
ax.set_ylabel("SNR (dB)")
ax.legend(loc="lower left")
ax.set_title("Running design: total SNR (solid) and jitter-only limit (dotted)")
save(fig, f"{OUT}/jitter.svg")

# ---------------------------------------------------------------- figure 5: regeneration
fig, ax = plt.subplots(figsize=(6.6, 4.2))
tau_l = 60e-15 / 3e-3
lsb = 1.6 / 4096
for vi, col, lab in zip((lsb / 2, 1e-3, 10e-3), PALETTE, ("half an LSB", "1 mV", "10 mV")):
    v0 = 6.75 * vi
    sol = solve_ivp(lambda t, y: [0.3e-3 * math.tanh(3e-3 * y[0] / 0.3e-3) / 60e-15], (0, 200e-12), [v0 / 2],
                    max_step=0.2e-12, rtol=1e-9, atol=1e-15)
    ax.semilogy(sol.t * 1e12, 2 * sol.y[0], color=col, label=f"$v_{{in}}$ = {lab}")
    tt = np.linspace(0, 200e-12, 200)
    ax.semilogy(tt * 1e12, v0 * np.exp(tt / tau_l), color=col, ls=":", lw=0.9)
ax.axhline(0.6, color="0.4", lw=0.8)
ax.text(2, 0.68, "$V_L$ = 0.6 V", fontsize=8, color="0.3")
ax.set_ylim(1e-3, 3)
ax.set_xlabel("time (ps)")
ax.set_ylabel("differential output (V)")
ax.legend(loc="lower right")
ax.set_title("Latch regeneration, τ = 20 ps: simulation (solid), $v_0e^{t/τ}$ (dotted)")
save(fig, f"{OUT}/regen.svg")
print("figures written to", OUT)
