#!/usr/bin/env python3
"""Figures for chapter 20-06 (data converter fundamentals).

Run from anywhere:  python assets/figures/src/fig_20_06.py
Outputs
  assets/figures/20-06/dnl_inl.svg    DNL and INL of the lab's seeded 12-bit SAR (0.5 % unit mismatch), with the INL
                                      recovered by a sine histogram test with coherent and with random phases
  assets/figures/20-06/spectrum.svg   16,384-point spectrum of the lab's full model near 49 MHz (mismatch, thermal
                                      noise, cubic distortion), annotated with SNR, SINAD, SFDR
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import adc  # noqa: E402

OUT = "assets/figures/20-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
N, VFS = 12, 1.6
LSB = VFS / 2 ** N
w = adc.sar_weights(N, 0.005, np.random.default_rng(2006))
T = adc.sar_transitions(w, VFS)
dnl, inl = adc.dnl_inl(T)

# ---------------------------------------------------------------- figure 2: DNL and INL
ns, A = 2 ** 22, 1.02 * 0.8
inl_h = {}
for name, ph in (("coherent", 2 * np.pi * (np.arange(ns) * 1048573 / ns + 0.123)),
                 ("random", np.random.default_rng(2007).uniform(0, 2 * np.pi, ns))):
    th = adc.histogram_transitions(adc.sar_code(0.8 + A * np.sin(ph), w, VFS), 2 ** N, A, 0.8)
    inl_h[name] = adc.dnl_inl(th)[1]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.2), sharex=True)
a1.plot(np.arange(1, 4095), dnl, color=PALETTE[0], lw=0.5)
a1.set_ylabel("DNL (LSB)")
a1.set_title("12-bit SAR, 0.5 % unit-capacitor mismatch (seeded)")
a2.plot(np.arange(1, 4096), inl_h["random"], color=PALETTE[1], lw=0.8, label="histogram, random phases")
a2.plot(np.arange(1, 4096), inl, color=PALETTE[0], lw=1.6, label="true")
a2.plot(np.arange(1, 4096), inl_h["coherent"], color=PALETTE[2], lw=0.8, ls="--", label="histogram, coherent phases")
a2.set_ylabel("INL (LSB)")
a2.set_xlabel("code")
a2.legend(loc="lower left", fontsize=8)
save(fig, f"{OUT}/dnl_inl.svg")

# ---------------------------------------------------------------- figure 3: spectrum
n = 16384
f, m = adc.coherent_frequency(100e6, n, 49e6)
sig_th = math.sqrt(206.2791136341102e-6 ** 2 - (LSB / math.sqrt(12)) ** 2)
a3 = 4 * 10 ** (-64.40878967245925 / 20) / 0.8 ** 2
vd = 0.8 * (1 - 1e-6) * 0.999 * np.sin(2 * np.pi * m * np.arange(n) / n)
vin = 0.8 + vd - a3 * vd ** 3 + np.random.default_rng(2008).normal(0, sig_th, n)
x = adc.sar_code(vin, w, VFS) * LSB
r = adc.spectrum_metrics(x, m, full_scale_amp=0.8)
s = np.abs(np.fft.rfft(x - x.mean())) ** 2 / n ** 2 * 2
s[-1] /= 2
freq = np.arange(s.size) * 100e6 / n / 1e6
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.plot(freq, 10 * np.log10(s / (0.8 ** 2 / 2) + 1e-30), color=PALETTE[0], lw=0.5)
b3 = (3 * m) % n
b3 = n - b3 if b3 > n // 2 else b3
ax.annotate(f"HD3 (aliased) {10 * np.log10(s[b3] / s[m]):.1f} dBc", xy=(freq[b3], 10 * np.log10(s[b3] / 0.32)),
            xytext=(22, -50), arrowprops=dict(arrowstyle="->", lw=0.7), fontsize=8)
ax.text(2, -20, f"SNR {r['snr']:.1f} dB, SINAD {r['sinad']:.1f} dB\nSFDR {r['sfdr']:.1f} dBc, ENOB {r['enob_fs']:.2f}",
        fontsize=8)
ax.axhline(-r["snr"] - 10 * math.log10(n / 2), color="0.5", lw=0.8, ls=":")
ax.text(2, -143, "dotted: average noise per bin, SNR + 10 log10(N/2) below the signal",
        fontsize=7, color="0.2", bbox=dict(facecolor="white", edgecolor="none", pad=1))
ax.set_ylim(-150, 5)
ax.set_xlabel("frequency (MHz)")
ax.set_ylabel("power (dBFS)")
ax.set_title(f"FFT test, 16,384 points, $f_{{in}}$ = {f / 1e6:.2f} MHz, $f_s$ = 100 MS/s")
save(fig, f"{OUT}/spectrum.svg")
print("figures written to", OUT)
