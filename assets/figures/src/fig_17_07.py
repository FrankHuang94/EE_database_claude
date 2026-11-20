#!/usr/bin/env python3
"""Figures for chapter 17-07 (information theory and Shannon capacity).

Run from anywhere:  python assets/figures/src/fig_17_07.py
Outputs
  assets/figures/17-07/shannon-limit.svg  spectral efficiency against Eb/N0: the Shannon boundary (2^eta - 1)/eta,
                                          the -1.59 dB asymptote, uncoded QPSK/16-QAM/64-QAM at BER 1e-5 and two
                                          DVB-S2 operating points (QEF thresholds from EN 302 307-1, R-276)
  assets/figures/17-07/capacity.svg       capacity per real channel use against Es/N0: Gaussian input, BPSK with
                                          soft decisions and BPSK with hard decisions, with the rate-1/2 points
Uses labs/17-07-lab/infotheory.py and labs/17-06-lab/modulation.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[3]
LABS = ROOT / "courses" / "17-communication-systems" / "labs"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(LABS / "17-07-lab"))
sys.path.insert(0, str(LABS / "17-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import infotheory as it  # noqa: E402
import modulation as md  # noqa: E402

OUT = "assets/figures/17-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ Shannon limit plane
eta = np.linspace(0.01, 8, 400)
ebn0 = 10 * np.log10((2**eta - 1) / eta)
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.plot(ebn0, eta, color=PALETTE[0], label="Shannon boundary, R = C")
ax.fill_betweenx(eta, -3, ebn0, color=PALETTE[0], alpha=0.08)
ax.axvline(10 * math.log10(math.log(2)), color=PALETTE[0], ls=":", lw=1)
ax.text(-1.45, 7.3, "−1.59 dB", fontsize=8, color=PALETTE[0])
ax.text(-2.6, 5.0, "no reliable\ncommunication", fontsize=8, color=PALETTE[0])


def uncoded_db(m):
    k = math.log2(m)
    if m == 4:
        return 20 * math.log10(norm.isf(1e-5) / math.sqrt(2))
    return optimize.brentq(lambda x: md.ser_qam(m, k * 10 ** (x / 10)) / k - 1e-5, 0, 40, xtol=1e-12)


pts = [(uncoded_db(m), math.log2(m), name) for m, name in ((4, "QPSK"), (16, "16-QAM"), (64, "64-QAM"))]
ax.plot([p[0] for p in pts], [p[1] for p in pts], "s", color=PALETTE[1], label="uncoded, BER 1e-5")
for x, y, name in pts:
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, -10), fontsize=8)
# DVB-S2 QEF thresholds (EN 302 307-1 Table 13, R-276), converted to Eb/N0 in 17-06 Example 5
dvb = [(1.05, 0.988858, "QPSK 1/2"), (9.56, 4.453027, "32APSK 9/10")]
ax.plot([d[0] for d in dvb], [d[1] for d in dvb], "o", color=PALETTE[2], label="DVB-S2 LDPC (QEF)")
for x, y, name in dvb:
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.text(3.0, 0.25, "power-limited (low η)", fontsize=8, color="0.35")
ax.text(14.5, 7.2, "bandwidth-limited\n(high η)", fontsize=8, color="0.35")
ax.set_xlim(-3, 20)
ax.set_ylim(0, 8)
ax.set_xlabel("Eb/N0 (dB)")
ax.set_ylabel("spectral efficiency η (b/s/Hz)")
ax.set_title("Uncoded modulation sits 7–8 dB from the bound; modern codes close most of the gap")
ax.legend(fontsize=8, loc="lower right")
save(fig, f"{OUT}/shannon-limit.svg")

# ------------------------------------------------------------------ constrained-input capacity
es_db = np.linspace(-10, 15, 251)
lin = 10 ** (es_db / 10)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
ax.plot(es_db, [it.gaussian_real_capacity(x) for x in lin], color=PALETTE[0], label="Gaussian input (unconstrained)")
ax.plot(es_db, [it.bpsk_soft_capacity(x) for x in lin], color=PALETTE[1], label="BPSK, soft decisions")
ax.plot(es_db, [it.bpsk_hard_capacity(x) for x in lin], color=PALETTE[2], label="BPSK, hard decisions (BSC)")
for fn, col in ((it.gaussian_real_capacity, PALETTE[0]), (it.bpsk_soft_capacity, PALETTE[1]), (it.bpsk_hard_capacity, PALETTE[2])):
    x = it.required_es_n0_db(fn, 0.5)
    ax.plot([x], [0.5], "o", color=col, ms=4)
ax.axhline(0.5, color="0.6", ls=":", lw=1)
ax.text(8, 0.53, "rate 1/2", fontsize=8, color="0.35")
ax.set_xlim(-10, 15)
ax.set_ylim(0, 2.6)
ax.set_xlabel("Es/N0 (dB)")
ax.set_ylabel("capacity (bits per real channel use)")
ax.set_title("Binary inputs saturate at 1 bit; slicing to hard bits costs about 1.6 dB at rate 1/2")
ax.legend(fontsize=8, loc="upper left")
save(fig, f"{OUT}/capacity.svg")
