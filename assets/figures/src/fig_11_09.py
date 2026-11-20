#!/usr/bin/env python3
"""Figures for chapter 11-09 (the z-transform).

Run from anywhere:  python assets/figures/src/fig_11_09.py
Outputs SVGs to assets/figures/11-09/:
- zplane.svg: Re{z^n} at nine points of the z-plane (radius 0.85, 1, 1.1; angle 0, pi/4, pi);
- roc.svg: Example 11-09.2, poles at 0.5 and 2, the three possible ROCs and the three sequences;
- geometric.svg: Example 11-09.3, the resonator's pole vectors to a point on the unit circle and |H|;
- notch.svg: Example 11-09.4, the three-tap FIR notch of 11-07 against the IIR notch with r = 0.98;
- triangle.svg: Example 11-09.5, the biquad stability triangle with the complex-pole parabola;
- bilinear.svg: Example 11-09.6, the reference CTLE (g_DC = -12 dB) analog and bilinear-digitized at M = 32, 2.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def unit_circle(ax):
    ax.add_patch(Circle((0, 0), 1, fill=False, ls="--", color="0.4", lw=1))
    ax.axhline(0, color="0.6", lw=0.6)
    ax.axvline(0, color="0.6", lw=0.6)
    ax.set_aspect("equal")


def fig_zplane():
    radii = (0.85, 1.0, 1.1)
    angles = ((math.pi, "π"), (math.pi / 4, "π/4"), (0.0, "0"))
    n = np.arange(0, 25)
    fig, axs = plt.subplots(3, 3, figsize=(7.6, 5.0), sharex=True)
    for i, (w, wl) in enumerate(angles):
        for k, r in enumerate(radii):
            ax = axs[i, k]
            y = (r ** n) * np.cos(w * n)
            ax.vlines(n, 0, y, color=PALETTE[0], lw=1)
            ax.plot(n, y, "o", color=PALETTE[0], ms=2.5)
            ax.axhline(0, color="0.6", lw=0.6)
            ax.set_ylim(-11, 11)
            ax.set_yticks([])
            ax.set_title(f"r = {r:g}, ω = {wl}", fontsize=8)
            if i == 2:
                ax.set_xlabel("n", fontsize=8)
    fig.suptitle("Re{zⁿ}: inside the unit circle decays, on it steady, outside grows; the angle sets the frequency",
                 fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/zplane.svg")


def fig_roc():
    rings = [(2, 3.0, "|z| > 2: causal, grows"), (0.5, 2, "0.5 < |z| < 2: two-sided, decays"),
             (0, 0.5, "|z| < 0.5: anticausal")]
    n = np.arange(-8, 9)
    u = (n >= 0).astype(float)
    seqs = [(-(1 / 3) * 0.5 ** n + (4 / 3) * 2.0 ** n) * u,
            -(1 / 3) * 0.5 ** n * u - (4 / 3) * 2.0 ** n * (1 - u),
            ((1 / 3) * 0.5 ** n - (4 / 3) * 2.0 ** n) * (1 - u)]
    fig, axs = plt.subplots(2, 3, figsize=(9.0, 5.0))
    for k in range(3):
        ax = axs[0, k]
        lo, hi, lab = rings[k]
        ax.add_patch(Wedge((0, 0), hi, 0, 360, width=hi - lo, color=PALETTE[1], alpha=0.3))
        unit_circle(ax)
        ax.plot([0.5, 2], [0, 0], "x", color=PALETTE[3], ms=8, mew=2)
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_title(lab, fontsize=9)
        ax2 = axs[1, k]
        ax2.vlines(n, 0, seqs[k], color=PALETTE[0], lw=1)
        ax2.plot(n, seqs[k], "o", color=PALETTE[0], ms=3)
        ax2.axhline(0, color="0.6", lw=0.6)
        ax2.set_ylim(-6, 6)
        ax2.set_xlabel("n")
    axs[1, 0].set_ylabel("x[n]")
    fig.suptitle("X(z) = 1/((1 − 0.5z⁻¹)(1 − 2z⁻¹)): one expression, three ROCs, three sequences", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/roc.svg")


def fig_geometric():
    r, th = 0.9, math.pi / 4
    p1, p2 = r * np.exp(1j * th), r * np.exp(-1j * th)
    w0 = 0.6
    pt = np.exp(1j * w0)
    fig, axs = plt.subplots(1, 2, figsize=(8.6, 3.8))
    ax = axs[0]
    unit_circle(ax)
    ax.plot([p1.real, p2.real], [p1.imag, p2.imag], "x", color=PALETTE[3], ms=9, mew=2)
    ax.plot([0], [0], "o", mfc="none", color=PALETTE[3], ms=8)
    ax.text(0.05, 0.08, "2", fontsize=8, color=PALETTE[3])
    for p, c in ((p1, PALETTE[0]), (p2, PALETTE[2])):
        ax.annotate("", xy=(pt.real, pt.imag), xytext=(p.real, p.imag),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.5))
    ax.plot([pt.real], [pt.imag], "o", color="k", ms=4)
    ax.text(pt.real + 0.05, pt.imag + 0.05, "e^{jω}", fontsize=9)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_title("poles at 0.9e^{±jπ/4}; vectors to e^{jω}", fontsize=9)
    w = np.linspace(0, math.pi, 2000)
    a = np.array([1, -2 * r * math.cos(th), r * r])
    H = 1 / np.abs(a[0] + a[1] * np.exp(-1j * w) + a[2] * np.exp(-2j * w))
    axs[1].plot(w / math.pi, H, color=PALETTE[0])
    axs[1].axvline(0.25, ls=":", color="0.5", lw=1)
    axs[1].set_xlabel("ω / π")
    axs[1].set_ylabel("|H(e^{jω})|")
    axs[1].set_title("peak ≈ 1/((1 − r)·1.345) near ω = π/4", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/geometric.svg")


def fig_notch():
    fs = 500.0
    w0 = 2 * math.pi * 60 / fs
    f = np.linspace(0, 250, 5000)
    e = np.exp(-1j * 2 * math.pi * f / fs)
    bF = np.array([1, -2 * math.cos(w0), 1])
    HF = np.abs(np.polyval(bF[::-1], e)) / abs(bF.sum())
    rr = 0.98
    aN = np.array([1, -2 * rr * math.cos(w0), rr * rr])
    K = aN.sum() / bF.sum()
    HN = np.abs(K * np.polyval(bF[::-1], e) / np.polyval(aN[::-1], e))
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.plot(f, HF, color=PALETTE[3], label="3-tap FIR notch (11-07)")
    ax.plot(f, HN, color=PALETTE[0], label="IIR notch, r = 0.98")
    for fx in (50, 120):
        ax.axvline(fx, ls=":", color="0.6", lw=1)
    ax.set_xlabel("frequency (Hz), fs = 500 SPS")
    ax.set_ylabel("|H|")
    ax.set_ylim(0, 3.6)
    ax.legend(fontsize=8)
    ax.set_title("both null 60 Hz; only the IIR notch leaves 50 and 120 Hz alone", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/notch.svg")


def fig_triangle():
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    tri = np.array([[-2, 1], [2, 1], [0, -1], [-2, 1]])
    ax.fill(tri[:, 0], tri[:, 1], color=PALETTE[1], alpha=0.2)
    ax.plot(tri[:, 0], tri[:, 1], color=PALETTE[1])
    a1 = np.linspace(-2, 2, 400)
    ax.plot(a1, a1 ** 2 / 4, color="0.4", ls="--", lw=1, label="a₁² = 4a₂ (complex poles above)")
    pts = [(-1.5, 0.56, "Ex 5 (stable, margin 0.06)", PALETTE[2]),
           (1.5, -0.56, "sign-flipped (unstable)", PALETTE[3]),
           (-1.273, 0.81, "resonator", PALETTE[0])]
    for x, y, lab, c in pts:
        ax.plot([x], [y], "o", color=c, ms=7, label=lab)
    ax.set_xlabel("a₁")
    ax.set_ylabel("a₂")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-1.3, 1.3)
    ax.legend(fontsize=7, loc="lower left")
    ax.set_title("biquad 1 + a₁z⁻¹ + a₂z⁻² is stable inside the triangle", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/triangle.svg")


def fig_bilinear():
    fb = 53.125e9
    fz = fp1 = 21.25e9
    fp2 = 53.125e9
    G = 10 ** (-12 / 20)
    f = np.linspace(1e8, fb, 1500)
    Ha = (G + 1j * f / fz) / ((1 + 1j * f / fp1) * (1 + 1j * f / fp2))
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.plot(f / 1e9, 20 * np.log10(np.abs(Ha)), color="k", lw=2.2, label="analog")
    k = (2 * math.pi * fp1) * (2 * math.pi * fp2) / (2 * math.pi * fz)
    for M, c in ((32, PALETTE[0]), (2, PALETTE[3])):
        fs = fb * M
        zd, pd, kd = signal.bilinear_zpk([-2 * math.pi * fz * G], [-2 * math.pi * fp1, -2 * math.pi * fp2], k, fs)
        w = np.linspace(1e-4, min(math.pi, 2 * math.pi * fb / fs), 1500)
        _, hd = signal.freqz_zpk(zd, pd, kd, worN=w)
        ax.plot(w * fs / (2 * math.pi) / 1e9, 20 * np.log10(np.abs(hd)), color=c, ls="--", label=f"bilinear, M = {M}")
    ax.axvline(26.5625, ls=":", color="0.5", lw=1)
    ax.set_ylim(-16, 1)
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("|H| (dB)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("bilinear transform: exact with oversampling, warped at 2 samples per UI", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/bilinear.svg")


if __name__ == "__main__":
    fig_zplane()
    fig_roc()
    fig_geometric()
    fig_notch()
    fig_triangle()
    fig_bilinear()
