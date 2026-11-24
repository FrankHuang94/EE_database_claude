#!/usr/bin/env python3
"""Figures for chapter 20-03 (bandgap and voltage references).

Run from anywhere:  python assets/figures/src/fig_20_03.py
Outputs
  assets/figures/20-03/curvature.svg   first-order bandgap output against temperature for zero-TC temperatures of
                                       27, 38.9 (centered for -40 to 125 C) and 60 C (T130 PNP, eta = 3)
  assets/figures/20-03/trim.svg        Example 20-03.2's output with an I_S error and with an op-amp offset, before
                                       and after a one-temperature trim at 300 K
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import bandgap as b  # noqa: E402

OUT = "assets/figures/20-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
p = b.PNP()
temps = np.arange(-40, 125.001, 0.5) + 273.15

# ---------------------------------------------------------------- figure 2: curvature
tc_mid = brentq(lambda tc: b.vref_closed_form(233.15, p.vg0, p.eta, 1, tc) -
                b.vref_closed_form(398.15, p.vg0, p.eta, 1, tc), 250, 380)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for tc, col, ls in ((300.15, PALETTE[1], "--"), (tc_mid, PALETTE[0], "-"), (333.15, PALETTE[2], ":")):
    vals = [b.vref_closed_form(t, p.vg0, p.eta, 1, tc) for t in temps]
    ax.plot(temps - 273.15, vals, color=col, ls=ls,
            label=f"zero TC at {tc - 273.15:.0f} °C: {(max(vals) - min(vals)) * 1e3:.2f} mV p-p")
ax.set_xlabel("temperature (°C)")
ax.set_ylabel("$V_{REF}$ (V)")
ax.legend(loc="lower center")
ax.set_title("First-order bandgap, T130 PNP ($\\eta$ = 3, $V_{g0}$ = 1.2009 V)")
save(fig, f"{OUT}/curvature.svg")

# ---------------------------------------------------------------- figure 4: trimming
i0, n = 5e-6, 8.0
r1 = b.vt(300) * math.log(n) / i0
r2 = b.k_zero_tc(p.vbe(i0, 300), n, p.vg0, p.eta, 1, tc_mid) * r1
vn = b.opamp_bandgap(300, r1, r2)["vref"]
p13 = b.PNP(is0=1.3 * p.is0)


def curve(r2x, **kw):
    return np.array([b.opamp_bandgap(t, r1, r2x, **kw)["vref"] for t in temps])


r2_is = brentq(lambda x: b.opamp_bandgap(300, r1, x, pnp=p13)["vref"] - vn, 0.9 * r2, 1.1 * r2)
r2_os = brentq(lambda x: b.opamp_bandgap(300, r1, x, vos=1e-3)["vref"] - vn, 0.9 * r2, 1.3 * r2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0), sharey=True)
nom = curve(r2)
for ax, title, before, after in ((ax1, "$I_S$ 30 % high (a PTAT error)", curve(r2, pnp=p13), curve(r2_is, pnp=p13)),
                                 (ax2, "1 mV op-amp offset (a constant error)", curve(r2, vos=1e-3),
                                  curve(r2_os, vos=1e-3))):
    ax.plot(temps - 273.15, (nom - vn) * 1e3, color="0.5", lw=1, label="nominal")
    ax.plot(temps - 273.15, (before - vn) * 1e3, color=PALETTE[1], ls="--", label="untrimmed")
    ax.plot(temps - 273.15, (after - vn) * 1e3, color=PALETTE[0], label="trimmed at 27 °C")
    ax.axvline(26.85, color="0.7", lw=0.8)
    ax.set_title(title)
    ax.set_xlabel("temperature (°C)")
ax1.set_ylabel("$V_{REF} - V_{REF,nom}(27\\,°C)$ (mV)")
ax1.legend(loc="lower right")
save(fig, f"{OUT}/trim.svg")
print("figures written to", OUT)
