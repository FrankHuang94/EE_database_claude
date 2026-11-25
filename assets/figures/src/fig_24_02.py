#!/usr/bin/env python3
"""Figures for chapter 24-02 (eye diagrams, jitter and BER).

Run from anywhere:  python assets/figures/src/fig_24_02.py
Outputs
  assets/figures/24-02/eye-anatomy.svg  an annotated NRZ eye of the two-pole channel (tau = 0.4 UI) built from
                                      random bits with a little Gaussian timing jitter: height, width, crossings
  assets/figures/24-02/bathtub.svg    dual-Dirac bathtub (RJ 0.4 ps, DJ(dd) 3 ps, 32 GBd) on a log-BER scale and
                                      on a Q scale, with the 1e-12 eye width marked
  assets/figures/24-02/stat-eye.svg   statistical NRZ eye of the two-pole channel (tau = 0.4 UI, 400 mV swing,
                                      8 mV rms noise) as BER contours, with the noiseless peak-distortion eye
                                      and the same eye less 7.03 sigma on each side marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import eye  # noqa: E402

OUT = "assets/figures/24-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
UI, RJ, DJ = 31.25, 0.4, 3.0


def eye_anatomy() -> None:
    """Overlay two-UI slices of a random NRZ waveform through the two-pole channel and label the eye."""
    rng = np.random.default_rng(3)
    nbits, spb = 400, 64
    bits = rng.integers(0, 2, nbits) * 2 - 1
    t = np.arange(nbits * spb) / spb  # time in UI
    step = eye.two_pole_step
    wave = sum(b * (step(t - k, 0.4) - step(t - k - 1, 0.4)) for k, b in enumerate(bits))
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    phase, _ = eye.cursors(0.4)
    for k in range(20, nbits - 3):
        j = rng.normal(0, 0.02)
        i0 = int(round((k + phase - 1 + j) * spb))
        seg = wave[i0:i0 + 2 * spb + 1]
        ax.plot(np.linspace(-1, 1, len(seg)), seg, color=PALETTE[0], lw=0.4, alpha=0.35)
    h = eye.cursors(0.4)[1]
    e = eye.peak_distortion_eye(h)
    ax.annotate("", xy=(0, e), xytext=(0, -e), arrowprops=dict(arrowstyle="<->", color=PALETTE[1], lw=1.4))
    ax.text(0.04, 0.25, "eye height\n(worst case)", color=PALETTE[1], fontsize=8, va="center",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1))
    ax.annotate("", xy=(-0.42, 0.0), xytext=(0.42, 0.0), arrowprops=dict(arrowstyle="<->", color=PALETTE[2], lw=1.2))
    ax.text(-0.38, -0.16, "eye width at the threshold", color=PALETTE[2], fontsize=8,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1))
    for xc in (-0.5, 0.5):
        ax.axvline(xc, color="0.6", ls=":", lw=0.8)
    ax.text(-0.98, 1.08, "crossings spread by ISI and jitter", fontsize=8, color="0.3")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xlabel("time relative to the sampling instant (UI)")
    ax.set_ylabel("received signal (fraction of the ±1 swing)")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/eye-anatomy.svg")


def bathtub() -> None:
    x = np.linspace(0, UI, 2000)
    ber = eye.bathtub(x, UI, RJ, DJ)
    tj = eye.total_jitter(RJ, DJ, 1e-12)
    xl, xr = tj / 2, UI - tj / 2
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.4))
    a1.semilogy(x, np.maximum(ber, 1e-18), color=PALETTE[0])
    a1.axhline(1e-12, color="0.5", ls=":", lw=1)
    a1.annotate("", xy=(xl, 1e-12), xytext=(xr, 1e-12), arrowprops=dict(arrowstyle="<->", color=PALETTE[3]))
    a1.text(UI / 2, 3e-12, f"{UI - tj:.2f} ps at 1e-12", ha="center", fontsize=8, color=PALETTE[3])
    a1.set_ylim(1e-16, 1)
    a1.set_xlabel("sampling position (ps)")
    a1.set_ylabel("BER")
    a1.set_title("log scale", fontsize=9)
    a1.grid(True, alpha=0.3)
    left = x[x < UI / 2]
    qv = (left - DJ / 2) / RJ
    a2.plot(left, eye.q_inv(np.maximum(eye.bathtub(left, UI, RJ, DJ), 1e-300)), color=PALETTE[0], label="bathtub wall")
    a2.plot(left, qv, "--", color=PALETTE[1], label="line: slope 1/RJ, intercept DJ/2")
    for b in (1e-6, 1e-9, 1e-12):
        a2.axhline(float(eye.q_inv(b)), color="0.6", ls=":", lw=0.8)
        a2.text(0.3, float(eye.q_inv(b)) + 0.1, f"{b:.0e}", fontsize=7, color="0.4")
    a2.set_xlim(0, 7)
    a2.set_ylim(0, 9)
    a2.set_xlabel("sampling position (ps)")
    a2.set_ylabel("Q⁻¹(BER)")
    a2.set_title("Q scale (left wall)", fontsize=9)
    a2.legend(fontsize=7, loc="upper left")
    a2.grid(True, alpha=0.3)
    save(fig, f"{OUT}/bathtub.svg")


def stat_eye() -> None:
    tp, _ = eye.cursors(0.4)
    phases = tp + np.linspace(-0.5, 0.5, 61)
    vth = np.linspace(-0.85, 0.85, 171)  # half-swing units
    sig = 8 / 200
    dv = 5e-4
    logb = np.empty((vth.size, phases.size))
    for j, ph in enumerate(phases):
        _, h = eye.cursors(0.4, n_pre=2, n_post=8, phase=float(ph))
        span = sum(abs(x) for k, x in h.items() if k) + 20 * dv
        grid = np.arange(-span, span + dv / 2, dv)
        grid -= grid[np.argmin(np.abs(grid))]
        pmf = eye.isi_pdf(h, grid)
        one = np.array([np.sum(pmf * eye.q((h[0] + grid - v) / sig)) for v in vth])
        zero = np.array([np.sum(pmf * eye.q((h[0] - grid + v) / sig)) for v in vth])
        logb[:, j] = np.log10(np.maximum(0.5 * (one + zero), 1e-40))
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    t_ps = (phases - tp) * UI
    cs = ax.contour(t_ps, vth * 200, logb, levels=[-12, -9, -6, -3], colors=[PALETTE[k] for k in (3, 2, 1, 0)])
    ax.clabel(cs, fmt=lambda z: f"1e{int(z)}", fontsize=7)
    _, h0 = eye.cursors(0.4)
    half = (h0[0] - sum(abs(x) for k, x in h0.items() if k)) * 200
    ax.plot([0, 0], [-half, half], color="0.3", lw=2, label=f"noiseless peak-distortion eye, ±{half:.1f} mV")
    wn = half - float(eye.q_inv(1e-12)) * 8
    ax.plot([0.4, 0.4], [-wn, wn], color="0.3", lw=2, ls="--", label=f"peak-distortion eye less 7.03σ, ±{wn:.1f} mV")
    ax.set_xlabel("sampling time relative to the pulse peak (ps)")
    ax.set_ylabel("decision threshold (mV)")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/stat-eye.svg")


if __name__ == "__main__":
    eye_anatomy()
    bathtub()
    stat_eye()
