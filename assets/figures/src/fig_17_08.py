#!/usr/bin/env python3
"""Figures for chapter 17-08 (channel coding).

Run from anywhere:  python assets/figures/src/fig_17_08.py
Outputs
  assets/figures/17-08/ber-curves.svg  BER against Eb/N0: uncoded BPSK; the (7,4) Hamming code with hard decisions
                                       (exact, by enumerating all 128 error patterns); the K = 3 (7,5) and K = 7
                                       (171,133) codes with soft Viterbi decoding (union bounds and Monte Carlo);
                                       the K = 7 code with hard decisions (Monte Carlo); a length-504 rate-1/2
                                       LDPC code with min-sum decoding (Monte Carlo, coded-bit BER); and the
                                       rate-1/2 BPSK-input limit (0.19 dB)
  assets/figures/17-08/trellis.svg     the (7,5) trellis for Example 17-08.4 with the decoded survivor path and the
                                       two channel errors marked
Uses labs/17-08-lab/coding.py.
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
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import coding as cd  # noqa: E402

OUT = "assets/figures/17-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1708)

# ------------------------------------------------------------------ BER curves
eb_db = np.linspace(0, 11, 221)
eb = 10 ** (eb_db / 10)
G74, H74 = cd.hamming74()
patterns = ((np.arange(128)[:, None] >> np.arange(6, -1, -1)) & 1).astype(np.uint8)
info_err = np.array([cd.syndrome_decode(e, H74)[:4].sum() for e in patterns])  # all-zero codeword sent
wts = patterns.sum(axis=1)


def hamming_hard_ber(x):
    p = norm.sf(math.sqrt(2 * 4 / 7 * x))
    return float(np.sum(p**wts * (1 - p) ** (7 - wts) * info_err) / 4)


spec3 = cd.distance_spectrum(("7", "5"), 3, 60)
spec7 = cd.distance_spectrum(("171", "133"), 7, 50)


def sim_conv(gens, K, points, nbits, soft=True):
    out = []
    for x in points:
        u = rng.integers(0, 2, nbits).astype(np.uint8)
        c = cd.conv_encode(u, gens, K)
        y, _ = cd.bpsk_awgn(c, x, 0.5, rng)
        rx = y if soft else (y < 0).astype(np.uint8)
        out.append(np.mean(cd.viterbi(rx, gens, K, soft=soft) != u))
    return np.array(out)


H = cd.gallager_ldpc(504, 3, 6, np.random.default_rng(3))
Gl = cd.gf2_nullspace(H)


def sim_ldpc(points, frames):
    out = []
    for x in points:
        errs = 0
        for _ in range(frames):
            c = cd.encode_block(rng.integers(0, 2, Gl.shape[0]), Gl)[0]
            _, llr = cd.bpsk_awgn(c, x, Gl.shape[0] / 504, rng)
            hard, _, _ = cd.min_sum_decode(llr, H)
            errs += np.sum(hard != c)
        out.append(errs / (frames * 504))
    return np.array(out)


fig, ax = plt.subplots(figsize=(6.8, 4.4))
ax.semilogy(eb_db, norm.sf(np.sqrt(2 * eb)), color="0.3", label="uncoded BPSK")
ax.semilogy(eb_db, [hamming_hard_ber(x) for x in eb], color=PALETTE[4], label="Hamming (7,4), hard (exact)")
ax.semilogy(eb_db, [cd.union_bound_ber(spec3, 0.5, x) for x in eb], color=PALETTE[1], ls="--", label="K = 3 (7,5), soft: union bound")
ax.semilogy(eb_db, [cd.union_bound_ber(spec7, 0.5, x) for x in eb], color=PALETTE[0], ls="--", label="K = 7 (171,133), soft: union bound")
p3 = np.array([3.0, 4.0, 5.0])
ax.semilogy(p3, sim_conv(("7", "5"), 3, p3, 200_000), "o", color=PALETTE[1], ms=4, label="K = 3 soft, simulated")
p7 = np.array([2.0, 2.5, 3.0, 3.5])
ax.semilogy(p7, sim_conv(("171", "133"), 7, p7, 150_000), "s", color=PALETTE[0], ms=4, label="K = 7 soft, simulated")
p7h = np.array([4.0, 4.5, 5.0, 5.5])
ax.semilogy(p7h, sim_conv(("171", "133"), 7, p7h, 150_000, soft=False), "^", color=PALETTE[0], mfc="none", ms=5, label="K = 7 hard, simulated")
pl = np.array([1.5, 1.75, 2.0, 2.25, 2.5])
ax.semilogy(pl, sim_ldpc(pl, 150), "D", color=PALETTE[2], ms=4, label="LDPC n = 504, R ≈ 1/2, min-sum")
ax.axvline(0.19, color=PALETTE[2], ls=":", lw=1)
ax.text(0.3, 2e-7, "rate-1/2\nBPSK limit\n0.19 dB", fontsize=7, color=PALETTE[2])
ax.set_ylim(1e-7, 0.5)
ax.set_xlim(0, 11)
ax.set_xlabel("Eb/N0 (dB)")
ax.set_ylabel("bit-error rate")
ax.set_title("Coding gain: about 5.4 dB for K = 7 at 1e-5; iterative codes move closer to the limit")
ax.legend(fontsize=7, loc="upper right")
save(fig, f"{OUT}/ber-curves.svg")

# ------------------------------------------------------------------ trellis for Example 17-08.4
states = [0b00, 0b10, 0b01, 0b11]  # rows top to bottom, labelled u_{t-1} u_{t-2}
row = {s: i for i, s in enumerate(states)}
rx = [1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1]
tx = cd.conv_encode([1, 0, 1, 1], ("7", "5"), 3)
path_inputs = [1, 0, 1, 1, 0, 0]
fig, ax = plt.subplots(figsize=(7.4, 3.4))
T = 6
for t in range(T):
    for s in states:
        for u in (0, 1):
            if t >= T - 2 and u == 1:
                continue
            reg = (u << 2) | s
            ns = reg >> 1
            ax.plot([t, t + 1], [-row[s], -row[ns]], color="0.8", lw=0.8, ls="-" if u == 0 else "--", zorder=1)
s = 0
for t, u in enumerate(path_inputs):
    reg = (u << 2) | s
    ns = reg >> 1
    out = format(int(tx[2 * t]) * 2 + int(tx[2 * t + 1]), "02b")
    ax.plot([t, t + 1], [-row[s], -row[ns]], color=PALETTE[0], lw=2.4, zorder=2)
    ax.text(t + 0.5, -(row[s] + row[ns]) / 2 + 0.12, out, fontsize=8, ha="center", color=PALETTE[0])
    s = ns
for t in range(T + 1):
    for st in states:
        ax.plot(t, -row[st], "o", color="0.25", ms=4, zorder=3)
for t in range(T):
    pair = rx[2 * t : 2 * t + 2]
    bad = [pair[i] != tx[2 * t + i] for i in range(2)]
    label = "".join(str(b) for b in pair)
    ax.text(t + 0.5, 0.55, label, ha="center", fontsize=9, color=PALETTE[3] if any(bad) else "0.2", fontweight="bold" if any(bad) else "normal")
ax.text(-0.15, 0.55, "received:", ha="right", fontsize=8)
ax.set_yticks([-row[s] for s in states])
ax.set_yticklabels([format(s, "02b") for s in states])
ax.set_xticks(range(T + 1))
ax.set_xlabel("time step (last two are tail bits)")
ax.set_ylabel("state  u(t−1) u(t−2)")
ax.set_ylim(-3.5, 0.9)
ax.set_title("Viterbi survivor (blue) for 1011 + 00: both channel errors (red) corrected, metric 2")
ax.grid(False)
save(fig, f"{OUT}/trellis.svg")
