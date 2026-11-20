#!/usr/bin/env python3
"""Figures for chapter 17-05 (matched filters and optimal detection).

Run from anywhere:  python assets/figures/src/fig_17_05.py
Outputs
  assets/figures/17-05/matched-filter.svg  left: a noisy antipodal rectangular-pulse stream and its matched-filter
                                           (integrate-and-dump) output, sampled at the symbol ends; right: a 10 us,
                                           10 MHz chirp echo buried in noise and its compressed output
  assets/figures/17-05/ber-curves.svg      bit-error rate against Eb/N0 for antipodal, orthogonal (and on-off) and
                                           Gray-coded PAM4, with Monte Carlo points from the lab's detectors
Uses labs/17-05-lab/detection.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import detection as dd  # noqa: E402

OUT = "assets/figures/17-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(5)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.3))
sps, nsym = 50, 12
bits = rng.choice([-1.0, 1.0], nsym)
x = np.repeat(bits, sps)
dt = 1.0 / sps
n0 = 0.25  # 2E/N0 = 8 (9 dB) per symbol of energy 1
r = x + dd.white_noise(len(x), n0, dt, rng)
y = np.array([np.sum(r[k - (k % sps): k + 1]) * dt for k in range(len(r))])  # integrate and dump
t = np.arange(len(x)) / sps
a1.plot(t, r, color="0.75", lw=0.5, label="received r(t)")
a1.plot(t, x, color=PALETTE[0], lw=1.2, label="sent ±1")
a1.plot(t, y, color=PALETTE[1], lw=1.2, label="integrate-and-dump")
ends = np.arange(sps - 1, len(x), sps)
a1.plot(t[ends], y[ends], "o", color=PALETTE[1], ms=4)
a1.set_xlabel("time (symbols)")
a1.set_title("Matched filter: noise averages out by the symbol's end", fontsize=9)
a1.legend(fontsize=7, loc="lower left")
fs = 50e6
ref = dd.chirp(10e-6, 10e6, fs)
rx = np.zeros(2000, dtype=complex)
rx[700:700 + len(ref)] = 0.5 * ref
rx += (rng.standard_normal(len(rx)) + 1j * rng.standard_normal(len(rx))) * math.sqrt(0.5)
comp = dd.compress(rx, ref)
tc = np.arange(len(comp)) / fs * 1e6
a2.plot(np.arange(len(rx)) / fs * 1e6, np.abs(rx), color="0.7", lw=0.5, label="|received| (echo at 14 µs)")
a2.plot(tc - len(ref) / fs * 1e6, np.abs(comp) / np.abs(comp).max() * 2.4, color=PALETTE[2], lw=1, label="compressed (normalized)")
a2.set_xlim(0, 40)
a2.set_xlabel("time (µs)")
a2.set_title("Pulse compression: TB = 100", fontsize=9)
a2.legend(fontsize=7, loc="upper right")
fig.tight_layout()
save(fig, f"{OUT}/matched-filter.svg")

eb = np.linspace(0, 14, 200)
lin = 10 ** (eb / 10)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.semilogy(eb, [dd.ber_bpsk(x) for x in lin], color=PALETTE[0], label="antipodal (BPSK)")
ax.semilogy(eb, [dd.ber_orthogonal(x) for x in lin], color=PALETTE[1], label="orthogonal or on-off")
ax.semilogy(eb, [dd.ser_pam(4, 2 * x) / 2 for x in lin], color=PALETTE[2], label="PAM4, Gray (≈ SER/2)")
for db_ in (2, 4, 6, 8):
    l = 10 ** (db_ / 10)
    sim = dd.simulate_ser(np.array([[1.0], [-1.0]]), 1 / l, 400_000, rng)
    ax.semilogy(db_, sim, "o", color=PALETTE[0], ms=4)
    sim = dd.simulate_ser(np.array([[1.0, 0.0], [0.0, 1.0]]), 1 / l, 400_000, rng)
    ax.semilogy(db_, sim, "s", color=PALETTE[1], ms=4)
ax.set_ylim(1e-7, 0.5)
ax.set_xlabel("Eb/N0 (dB)")
ax.set_ylabel("bit-error rate")
ax.set_title("Distance over noise: antipodal is 3 dB ahead of orthogonal")
ax.legend(fontsize=8, loc="lower left")
save(fig, f"{OUT}/ber-curves.svg")
