#!/usr/bin/env python3
"""Figures for chapter 11-08 (the Laplace transform and system functions).

Run from anywhere:  python assets/figures/src/fig_11_08.py
Outputs SVGs to assets/figures/11-08/:
- splane.svg: Re{e^{st}} at nine points of the s-plane (decaying, steady, growing; three frequencies);
- tent.svg: |H(s)| in dB over the s-plane for the series RLC of 11-04 (poles -10 +/- j30 krad/s), and its
  profile along the imaginary axis (the frequency response);
- roc.svg: Example 11-08.2, X(s) = 3/((s+1)(s-2)) with its three possible ROCs and the three signals;
- geometric.svg: Example 11-08.4, pole vectors to j*omega_d and the magnitude response;
- minphase.svg: Example 11-08.5, step responses of (s+5)/((s+1)(s+2)) and (5-s)/((s+1)(s+2));
- ctle.svg: Example 11-08.6, the IEEE 802.3ck reference CTLE for g_DC = 0, -6, -12, -20 dB.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_splane():
    sig = (-0.5, 0.0, 0.3)
    om = (6.0, 3.0, 0.0)
    t = np.linspace(0, 6, 600)
    fig, axs = plt.subplots(3, 3, figsize=(7.6, 5.0), sharex=True)
    for i, w in enumerate(om):
        for k, s in enumerate(sig):
            ax = axs[i, k]
            ax.plot(t, np.exp(s * t) * np.cos(w * t), color=PALETTE[0], lw=1.2)
            ax.axhline(0, color="0.6", lw=0.6)
            ax.set_ylim(-6.5, 6.5)
            ax.set_yticks([])
            ax.set_title(f"σ = {s:g}, ω = {w:g}", fontsize=8)
            if i == 2:
                ax.set_xlabel("t (s)", fontsize=8)
    fig.suptitle("Re{e^{st}}: left column decays, middle is steady, right grows; higher rows oscillate faster",
                 fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/splane.svg")


def rlc(s):
    w0sq, a = 1e9, 1e4
    return w0sq / (s * s + 2 * a * s + w0sq)


def fig_tent():
    sg = np.linspace(-40e3, 10e3, 251) + 37.0        # offset so no grid point lands on a pole
    wg = np.linspace(-60e3, 60e3, 301) + 53.0
    S = sg[None, :] + 1j * wg[:, None]
    M = 20 * np.log10(np.abs(rlc(S)))
    fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.6), gridspec_kw={"width_ratios": [1.1, 1]})
    im = axs[0].pcolormesh(sg / 1e3, wg / 1e3, np.clip(M, -30, 30), shading="auto", cmap="viridis",
                           rasterized=True)
    axs[0].axvline(0, color="w", lw=1.2, ls="--")
    axs[0].plot([-10, -10], [30, -30], "x", color="w", ms=8, mew=2)
    axs[0].set_xlabel("σ (krad/s)")
    axs[0].set_ylabel("ω (krad/s)")
    axs[0].set_title("|H(s)| (dB): peaks at the poles; jω axis dashed", fontsize=9)
    fig.colorbar(im, ax=axs[0], fraction=0.05)
    w = np.linspace(0, 60e3, 2000)
    axs[1].plot(w / 1e3, 20 * np.log10(np.abs(rlc(1j * w))), color=PALETTE[0])
    axs[1].axvline(28.284, ls=":", color="0.5", lw=1)
    axs[1].set_xlabel("ω (krad/s)")
    axs[1].set_ylabel("|H(jω)| (dB)")
    axs[1].set_title("the profile along the jω axis: peak at 28.28 krad/s", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/tent.svg")


def fig_roc():
    t = np.linspace(-3, 3, 1201)
    u = (t >= 0).astype(float)
    sig = [(-np.exp(-t) + np.exp(2 * t)) * u,
           -np.exp(-t) * u - np.exp(2 * t) * (1 - u),
           (np.exp(-t) - np.exp(2 * t)) * (1 - u)]
    rocs = [(2, 4, "σ > 2: causal, grows"), (-1, 2, "−1 < σ < 2: two-sided, decays"),
            (-4, -1, "σ < −1: anticausal")]
    fig, axs = plt.subplots(2, 3, figsize=(9.0, 4.6))
    for k in range(3):
        ax = axs[0, k]
        lo, hi, lab = rocs[k]
        ax.axvspan(lo, hi, color=PALETTE[1], alpha=0.25)
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(0, color="0.4", lw=0.8, ls="--")
        ax.plot([-1, 2], [0, 0], "x", color=PALETTE[3], ms=9, mew=2)
        ax.set_xlim(-4, 4)
        ax.set_ylim(-3, 3)
        ax.set_xlabel("σ")
        ax.set_ylabel("jω")
        ax.set_title(lab, fontsize=9)
        ax2 = axs[1, k]
        ax2.plot(t, sig[k], color=PALETTE[0])      # growing parts run off the axes
        ax2.axhline(0, color="0.6", lw=0.6)
        ax2.axvline(0, color="0.6", lw=0.6)
        ax2.set_ylim(-8.5, 8.5)
        ax2.set_xlabel("t (s)")
    axs[1, 0].set_ylabel("x(t)")
    fig.suptitle("X(s) = 3/((s+1)(s−2)): one expression, three ROCs, three signals", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/roc.svg")


def fig_geometric():
    p1, p2 = -10 + 30j, -10 - 30j
    fig, axs = plt.subplots(1, 2, figsize=(8.6, 3.6))
    ax = axs[0]
    ax.axhline(0, color="0.5", lw=0.8)
    ax.axvline(0, color="0.5", lw=0.8)
    ax.plot([p1.real, p2.real], [p1.imag, p2.imag], "x", color=PALETTE[3], ms=9, mew=2)
    pt = 30j
    for p, c in ((p1, PALETTE[0]), (p2, PALETTE[2])):
        ax.annotate("", xy=(pt.real, pt.imag), xytext=(p.real, p.imag),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.6))
    ax.plot([0], [30], "o", color="k", ms=4)
    ax.text(1.5, 31.5, "jω_d", fontsize=9)
    ax.text(-9.5, 33, "10", color=PALETTE[0], fontsize=9)
    ax.text(-3.5, 0, "60.8", color=PALETTE[2], fontsize=9)
    ax.set_xlim(-40, 15)
    ax.set_ylim(-40, 40)
    ax.set_aspect("equal")
    ax.set_xlabel("σ (krad/s)")
    ax.set_ylabel("ω (krad/s)")
    ax.set_title("vectors from the poles to jω", fontsize=9)
    w = np.linspace(0, 60e3, 2000)
    axs[1].plot(w / 1e3, np.abs(rlc(1j * w)), color=PALETTE[0])
    axs[1].plot([30], [1.644], "o", color="k", ms=4)
    axs[1].set_xlabel("ω (krad/s)")
    axs[1].set_ylabel("|H(jω)|")
    axs[1].set_title("|H| = ω₀² / (product of the distances)", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/geometric.svg")


def fig_minphase():
    t = np.linspace(0, 6, 1200)
    y1 = 2.5 - 4 * np.exp(-t) + 1.5 * np.exp(-2 * t)
    y2 = 2.5 - 6 * np.exp(-t) + 3.5 * np.exp(-2 * t)
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    ax.plot(t, y1, color=PALETTE[0], label="(s+5)/((s+1)(s+2)): minimum phase")
    ax.plot(t, y2, color=PALETTE[3], label="(5−s)/((s+1)(s+2)): zero at +5")
    ax.axhline(0, color="0.6", lw=0.6)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("step response")
    ax.legend(fontsize=8)
    ax.set_title("same magnitude response; the right-half-plane zero starts the wrong way", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/minphase.svg")


def fig_ctle():
    fz = fp1 = 21.25e9
    fp2 = 53.125e9
    f = np.logspace(8, 11.2, 800)
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    for g, c in ((0, PALETTE[0]), (-6, PALETTE[1]), (-12, PALETTE[2]), (-20, PALETTE[3])):
        G = 10 ** (g / 20)
        H = (G + 1j * f / fz) / ((1 + 1j * f / fp1) * (1 + 1j * f / fp2))
        ax.semilogx(f / 1e9, 20 * np.log10(np.abs(H)), color=c, label=f"g_DC = {g} dB")
    ax.axvline(26.5625, ls=":", color="0.4", lw=1)
    ax.text(28.5, -17.5, "Nyquist", fontsize=8)
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("|H| (dB)")
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("reference CTLE: lowering g_DC slides the zero down; the poles stay put", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/ctle.svg")


if __name__ == "__main__":
    fig_splane()
    fig_tent()
    fig_roc()
    fig_geometric()
    fig_minphase()
    fig_ctle()
