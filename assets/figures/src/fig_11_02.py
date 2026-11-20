#!/usr/bin/env python3
"""Figures for chapter 11-02 (systems and their properties).

Run from anywhere:  python assets/figures/src/fig_11_02.py
Outputs SVGs to assets/figures/11-02/:
- decimator.svg: the time-invariance test applied to the decimator y[n] = x[2n] with the pulse
  x = [1, 2, 3, 2, 1] at n = 0..4: shifting the input by one sample and then decimating does not give the
  decimated output shifted by one sample;
- stability.svg: Example 11-02.4, y[n] = a y[n-1] + x[n] from rest with |x| <= 1: a = 0.9 with a step,
  a = -0.9 with the alternating input (-1)^n, both approaching the bound 1/(1 - |a|) = 10, and a = 1 with a
  step (unbounded);
- distortion.svg: Example 11-02.5, the output spectrum of y = 10x + 0.5x^2 - 0.2x^3 for (a) one 0.1 V tone
  at 1 kHz and (b) two 0.1 V tones at 1.0 and 1.1 kHz, in dB relative to 1 V;
- inverse.svg: Example 11-02.7, a 1 mV error injected into the causal inverse of y[n] = x[n] + b x[n-1]
  for b = 0.5 (decays as 0.5^n) and b = 2 (grows as 2^n).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_decimator():
    n = np.arange(-2, 11)
    pulse = {0: 1, 1: 2, 2: 3, 3: 2, 4: 1}

    def x(k, shift=0):
        return np.array([pulse.get(int(i) - shift, 0) for i in k], dtype=float)

    def decimate(sig_fn, k):
        return sig_fn(2 * k)

    m = np.arange(-2, 7)
    y_then_shift = decimate(lambda k: x(k), m - 1)     # y[m - 1]
    shift_then_y = decimate(lambda k: x(k, 1), m)      # x[2m - 1]
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 4.8), sharey=True)
    axs[0, 0].stem(n, x(n), linefmt="C0-", markerfmt="C0o", basefmt=" ")
    axs[0, 0].set_title("(a) input x[n]")
    axs[0, 1].stem(n, x(n, 1), linefmt="C0-", markerfmt="C0o", basefmt=" ")
    axs[0, 1].set_title("(b) shifted input x[n - 1]")
    axs[1, 0].stem(m, y_then_shift, linefmt="C1-", markerfmt="C1o", basefmt=" ")
    axs[1, 0].set_title("(c) decimate, then shift: y[n - 1]")
    axs[1, 1].stem(m, shift_then_y, linefmt="C3-", markerfmt="C3o", basefmt=" ")
    axs[1, 1].set_title("(d) shift, then decimate: x[2n - 1]")
    for ax in axs.flat:
        ax.set_xlabel("n")
        ax.set_ylim(-0.3, 3.5)
    fig.tight_layout()
    save(fig, f"{OUT}/decimator.svg")


def recursion(a, x):
    y = np.zeros(len(x))
    prev = 0.0
    for i, xi in enumerate(x):
        prev = a * prev + xi
        y[i] = prev
    return y


def fig_stability():
    n = np.arange(40)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.plot(n, recursion(0.9, np.ones(40)), "o-", ms=3, color=PALETTE[0], label="a = 0.9, step input")
    ax.plot(n, np.abs(recursion(-0.9, (-1.0) ** n)), "s", ms=6, mfc="none", color=PALETTE[1],
            label="a = −0.9, input (−1)ⁿ (magnitude; same values)")
    ax.plot(n, recursion(1.0, np.ones(40)), "^-", ms=3, color=PALETTE[3], label="a = 1, step input")
    ax.axhline(10, color="0.4", ls="--", lw=1)
    ax.text(30, 10.6, "bound 1/(1 − |a|) = 10", color="0.3", fontsize=9)
    ax.set_xlabel("n")
    ax.set_ylabel("|y[n]|")
    ax.set_ylim(0, 25)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/stability.svg")


def amp(x):
    return 10 * x + 0.5 * x ** 2 - 0.2 * x ** 3


def spectrum(x_fn, n_samp=4000):
    """One second at 100 Hz resolution units: frequencies in multiples of 100 Hz."""
    t = np.arange(n_samp) / n_samp
    y = amp(x_fn(t))
    f = np.fft.rfft(y) / n_samp * 2
    f[0] /= 2
    return np.abs(f)


def fig_distortion():
    one = spectrum(lambda t: 0.1 * np.cos(2 * np.pi * 10 * t))
    two = spectrum(lambda t: 0.1 * np.cos(2 * np.pi * 10 * t) + 0.1 * np.cos(2 * np.pi * 11 * t))
    fig, axs = plt.subplots(1, 2, figsize=(7.6, 3.4), sharey=True)
    for ax, s, title in ((axs[0], one, "(a) one tone, 0.1 V at 1 kHz"),
                         (axs[1], two, "(b) two tones, 0.1 V at 1.0 and 1.1 kHz")):
        k = np.nonzero(s > 1e-9)[0]
        k = k[k <= 40]
        db = 20 * np.log10(s[k])
        ax.vlines(k * 0.1, -120, db, color=PALETTE[0])
        ax.plot(k * 0.1, db, "o", ms=4, color=PALETTE[0])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("frequency (kHz)")
        ax.set_xlim(-0.1, 3.6)
        ax.set_ylim(-100, 10)
    axs[0].set_ylabel("amplitude (dB re 1 V)")
    axs[0].annotate("HD2 −52 dB", (2.0, -52), (2.2, -35), fontsize=9, arrowprops={"arrowstyle": "->"})
    axs[0].annotate("HD3 −86 dB", (3.0, -86), (2.2, -70), fontsize=9, arrowprops={"arrowstyle": "->"})
    axs[1].annotate("IM2 at 0.1 and 2.1 kHz", (0.1, -46), (0.5, -25), fontsize=9,
                    arrowprops={"arrowstyle": "->"})
    axs[1].annotate("IM3 at 0.9 and 1.2 kHz", (1.2, -76.5), (1.6, -62), fontsize=9,
                    arrowprops={"arrowstyle": "->"})
    fig.tight_layout()
    save(fig, f"{OUT}/distortion.svg")


def fig_inverse():
    n = np.arange(21)
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    for b, c, mk in ((0.5, PALETTE[0], "o"), (2.0, PALETTE[3], "s")):
        e = 1e-3 * (-b) ** n
        ax.semilogy(n, np.abs(e), mk + "-", ms=3, color=c, label=f"b = {b:g}: error × (−{b:g})ⁿ")
    ax.set_xlabel("n (samples after the error)")
    ax.set_ylabel("|error| (V)")
    ax.axhline(1e-3, color="0.5", ls=":", lw=1)
    ax.legend(fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/inverse.svg")


if __name__ == "__main__":
    fig_decimator()
    fig_stability()
    fig_distortion()
    fig_inverse()
