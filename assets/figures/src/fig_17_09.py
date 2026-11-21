#!/usr/bin/env python3
"""Figures for chapter 17-09 (wireless channels).

Run from anywhere:  python assets/figures/src/fig_17_09.py
Outputs
  assets/figures/17-09/path-loss.svg   path loss against distance at 3.5 GHz: free space, the exact two-ray model
                                       (10 m and 1.5 m antennas), TR 38.901 UMi-Street Canyon LOS and NLOS (R-283)
                                       with +/- one shadowing standard deviation
  assets/figures/17-09/fading.svg      20 ms of Rayleigh fading at fD = 389 Hz (3.5 GHz, 120 km/h) by a sum of
                                       sinusoids, a Rician envelope (K = 10 dB) for comparison, and the -10 dB level
  assets/figures/17-09/ber-fading.svg  average BPSK BER against average Eb/N0: AWGN, Rayleigh, and Rayleigh with 2-
                                       and 4-branch MRC, with Monte Carlo points
Uses labs/17-09-lab/channels.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import channels as ch  # noqa: E402

OUT = "assets/figures/17-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1709)

# ------------------------------------------------------------------ path loss
d = np.logspace(1, 4, 600)
f = 3.5e9
fsl = np.array([ch.fspl_db(f, x) for x in d])
tr = np.array([ch.two_ray_loss_db(x, 10, 1.5, f) for x in d])
los = np.array([ch.umi_los_db(x, 3.5) for x in d])
nlos = np.array([ch.umi_nlos_db(x, 3.5) for x in d])
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.semilogx(d, fsl, color="0.3", label="free space (n = 2)")
ax.semilogx(d, tr, color=PALETTE[4], lw=0.8, label="two-ray, 10 m / 1.5 m")
ax.semilogx(d, los, color=PALETTE[0], label="UMi LOS (σ = 4 dB)")
ax.fill_between(d, los - 4, los + 4, color=PALETTE[0], alpha=0.12)
ax.semilogx(d, nlos, color=PALETTE[1], label="UMi NLOS (σ = 7.82 dB)")
ax.fill_between(d, nlos - 7.82, nlos + 7.82, color=PALETTE[1], alpha=0.12)
bp = ch.two_ray_breakpoint(10, 1.5, f)
ax.axvline(bp, color=PALETTE[4], ls=":", lw=1)
ax.text(bp * 1.08, 150, "two-ray\nbreakpoint\n700 m", fontsize=7, color=PALETTE[4])
ax.axvline(ch.umi_breakpoint(fc_ghz=3.5), color=PALETTE[0], ls=":", lw=1)
ax.text(ch.umi_breakpoint(fc_ghz=3.5) / 2.3, 160, "UMi d'BP\n210 m", fontsize=7, color=PALETTE[0])
ax.set_xlim(10, 1e4)
ax.set_ylim(55, 180)
ax.set_xlabel("distance (m)")
ax.set_ylabel("path loss at 3.5 GHz (dB)")
ax.set_title("Free space loses 20 dB/decade; blocked urban paths about 35 dB/decade")
ax.legend(fontsize=8, loc="lower right")
save(fig, f"{OUT}/path-loss.svg")

# ------------------------------------------------------------------ fading envelopes
fd = ch.doppler_hz(120 / 3.6, 3.5e9)
fs_rate = 50_000.0
n = int(0.02 * fs_rate)
t = np.arange(n) / fs_rate * 1e3
h = ch.rayleigh_sos(n, fd, fs_rate, rng, m=64)
hr = ch.rayleigh_sos(n, fd, fs_rate, rng, m=64, k_factor=10.0)
fig, ax = plt.subplots(figsize=(6.8, 3.4))
ax.plot(t, 20 * np.log10(np.abs(h)), color=PALETTE[0], lw=1, label="Rayleigh (no line of sight)")
ax.plot(t, 20 * np.log10(np.abs(hr)), color=PALETTE[2], lw=1, label="Rician, K = 10 dB")
ax.axhline(-10, color=PALETTE[3], ls=":", lw=1)
ax.text(0.3, -8.5, "−10 dB", fontsize=8, color=PALETTE[3])
ax.set_ylim(-35, 10)
ax.set_xlabel("time (ms)")
ax.set_ylabel("envelope relative to rms (dB)")
ax.set_title(f"3.5 GHz at 120 km/h: fD = {fd:.0f} Hz, a deep fade every few ms")
ax.legend(fontsize=8, loc="lower right")
save(fig, f"{OUT}/fading.svg")

# ------------------------------------------------------------------ BER in fading
g_db = np.linspace(0, 45, 451)
g = 10 ** (g_db / 10)
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.semilogy(g_db, norm.sf(np.sqrt(2 * g)), color="0.3", label="AWGN")
for L, col in ((1, PALETTE[1]), (2, PALETTE[0]), (4, PALETTE[2])):
    ax.semilogy(g_db, [ch.ber_bpsk_mrc(x, L) for x in g], color=col, label="Rayleigh" if L == 1 else f"Rayleigh, {L}-branch MRC")
    pts = np.array([0, 5, 10, 15, 20]) if L > 1 else np.array([0, 10, 20, 30])
    sim = []
    for x in pts:
        nb = 200_000
        bits = rng.integers(0, 2, nb)
        gains = (rng.standard_normal((L, nb)) + 1j * rng.standard_normal((L, nb))) / math.sqrt(2)
        sig = math.sqrt(1 / (2 * 10 ** (x / 10)))
        y = gains * (1 - 2 * bits) + sig * (rng.standard_normal((L, nb)) + 1j * rng.standard_normal((L, nb)))
        sim.append(np.mean((np.real(np.sum(np.conj(gains) * y, axis=0)) < 0) != bits))
    sim = np.array(sim)
    keep = np.array([ch.ber_bpsk_mrc(10 ** (x / 10), L) * 200_000 >= 50 for x in pts])  # plot only points with ~50+ expected errors
    ax.semilogy(pts[keep], sim[keep], "o", color=col, ms=4)
ax.set_ylim(1e-6, 0.5)
ax.set_xlim(0, 45)
ax.set_xlabel("average Eb/N0 per branch (dB)")
ax.set_ylabel("bit-error rate (BPSK)")
ax.set_title("Fading turns an exponential waterfall into 1/SNR; diversity restores the slope")
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/ber-fading.svg")
