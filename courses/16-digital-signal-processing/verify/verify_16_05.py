#!/usr/bin/env python3
"""Verify chapter 16-05 (spectral analysis and windowing): examples, concept checks, problems and lab answers.

Routes:
- window figures of merit from their definitions (labs/16-05-lab/spectral.py), the windows themselves checked
  against scipy.signal.windows, sidelobes and scalloping from a dense evaluation of each window's DTFT;
- floor depths and SNRs by quantizing sines and measuring the spectra;
- the ADC test of Example 16-05.5 by simulation, with SINAD checked by an independent time-domain sine fit;
- periodogram scatter and Welch averaging by Monte Carlo.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.signal import windows

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import spectral as sp  # noqa: E402

CH = ROOT / "chapters" / "16-05-spectral-analysis-and-windowing.md"
v = Verifier.from_files("16-05", CH, ROOT / "solutions" / "16-05-solutions.md", LAB / "README.md")

ref = {"hann": windows.hann, "hamming": windows.hamming, "blackman": windows.blackman,
       "bh4": windows.blackmanharris, "flattop": windows.flattop}
for name, fn in ref.items():
    v.assert_true(f"window {name} equals scipy's periodic window", np.allclose(sp.window(name, 256), fn(256, sym=False)))

# ---------------------------------------------------------------------------------------- the table of 3.2
N = 4096
keys = {"rect": "agm", "hann": "bhn", "hamming": "cio", "blackman": "djp", "bh4": "ekq", "flattop": "flr"}
for name, (ke, ks, kl) in keys.items():
    w = sp.window(name, N)
    v.check(f"Txt 16-05.{ke}", sp.enbw_bins(w))
    v.check(f"Txt 16-05.{ks}", sp.scalloping_db(w))
    v.check(f"Txt 16-05.{kl}", sp.highest_sidelobe_db(w))
v.check("Txt 16-05.s", sp.coherent_gain(sp.window("bh4", N)))
v.check("Txt 16-05.t", sp.coherent_gain(sp.window("flattop", N)))
for name in ("rect", "hann"):
    w = sp.window(name, N)
    width = 2 * brentq(lambda nu: sp._w_dtft(w, nu)[0] / sp._w_dtft(w, 0)[0] - 0.5, 0.01, 3, xtol=1e-12)
    v.check("Txt 16-05.u" if name == "rect" else "Txt 16-05.v", width)
v.assert_true("ENBW >= 1 for every window (Cauchy-Schwarz)", all(sp.enbw_bins(sp.window(n_, 512)) >= 1 - 1e-12 for n_ in keys))

# ---------------------------------------------------------------------------------------- Example 1
v.check("Ex 16-05.1a", 1e6 / 4096)
v.check("Ex 16-05.1b", 1e6 / 4096 * sp.enbw_bins(sp.window("hann", 4096)))
v.check("Ex 16-05.1c", 10 * math.log10(sp.enbw_bins(sp.window("hann", 4096))))
wh = sp.window("hann", 4096)
v.check("Ex 16-05.1d", -20 * math.log10(sp.coherent_gain(wh)))
v.check("Ex 16-05.1e", float(np.mean(wh**2)))
v.check("Ex 16-05.1f", -10 * math.log10(np.mean(wh**2)))

# ---------------------------------------------------------------------------------------- Example 2
n = np.arange(1024)
X = np.abs(np.fft.fft(np.cos(2 * np.pi * 100 * n / 1024) * sp.window("hann", 1024)))
v.check("Ex 16-05.2a", X[100])
for name, key in (("rect", "b"), ("hann", "c"), ("flattop", "d")):
    v.check(f"Ex 16-05.2{key}", sp.scalloping_db(sp.window(name, 1024)))
v.check("Ex 16-05.2e", 100 * (1 - 10 ** (sp.scalloping_db(sp.window("rect", 1024)) / 20)))

# ---------------------------------------------------------------------------------------- Example 3
Nn = 1024
n = np.arange(Nn)
xs = np.cos(2 * np.pi * 100.5 * n / Nn)
xw = 1e-3 * np.cos(2 * np.pi * 110 * n / Nn)
for name, kl, kw in (("rect", "a", "d"), ("hann", "b", "e"), ("bh4", "c", "f")):
    w = sp.window(name, Nn)
    S = np.abs(np.fft.fft(xs * w))
    pk = S.max()
    v.check(f"Ex 16-05.3{kl}", 20 * math.log10(S[110] / pk))
    v.check(f"Ex 16-05.3{kw}", 20 * math.log10(np.abs(np.fft.fft(xw * w))[110] / pk))
v.check("Ex 16-05.3g", 20 * math.log10(1 / (math.pi * 9.5)))

# ---------------------------------------------------------------------------------------- Example 4
snr_ideal = 6.02 * 12 + 1.76
v.check("Ex 16-05.4a", snr_ideal)
v.check("Ex 16-05.4b", snr_ideal + 10 * math.log10(8192 / 2))
v.check("Ex 16-05.4c", snr_ideal + 10 * math.log10(8192 / (2 * sp.enbw_bins(sp.window("hann", 8192)))))
v.check("Ex 16-05.4f", snr_ideal + 10 * math.log10(8192 / 2) - snr_ideal)
N4 = 8192
M4 = sp.coherent_bin(1e6, 8.192e6, N4)
v.assert_true("Ex 4: the coherent bin near N/8 is 999", M4 == 999)
x4 = (1 - 1e-9) * np.sin(2 * np.pi * M4 * np.arange(N4) / N4 + 0.3)
q = 2 / 2**12
xq = np.clip(np.round(x4 / q) * q, -1, 1 - q)
m4 = sp.adc_metrics(xq, M4)
v.check("Ex 16-05.4d", m4["snr"])
P = np.abs(np.fft.fft(xq)) ** 2
v.check("Ex 16-05.4e", 10 * math.log10(P[M4] / np.mean(np.delete(P[1:N4 // 2], [M4 - 1]))))

# ---------------------------------------------------------------------------------------- Example 5
fs, N5 = 100e6, 16384
M5 = sp.coherent_bin(10e6, fs, N5)
v.check("Ex 16-05.5a", M5)
v.assert_true("Ex 5: M odd and relatively prime to N", M5 % 2 == 1 and math.gcd(M5, N5) == 1)
v.check("Ex 16-05.5b", M5 * fs / N5 / 1e6)
A = 10 ** (-1 / 20)
a3 = 4e-4 / A**2
a2 = 2 * 10 ** (-90 / 20) / A
v.assert_true("Ex 5: nonlinearity designed for HD3 -80 dBc and HD2 -90 dBc",
              abs(20 * math.log10(a3 * A**2 / 4) + 80) < 1e-9 and abs(20 * math.log10(a2 * A / 2) + 90) < 1e-9)
rng = np.random.default_rng(1605)
n5 = np.arange(N5)
x5 = A * np.sin(2 * np.pi * M5 * n5 / N5 + 0.7)
y5 = x5 + a2 * x5**2 + a3 * x5**3 + rng.normal(scale=2.0e-4, size=N5)
q = 2 / 2**12
yq = np.clip(np.round(y5 / q) * q, -1, 1 - q)
m5 = sp.adc_metrics(yq, M5)
v.assert_true("Ex 5: harmonic bins 3274, 4911, 6548, 8185", m5["harm_bins"] == [3274, 4911, 6548, 8185])
v.check("Ex 16-05.5c", m5["snr"])
v.check("Ex 16-05.5d", m5["sinad"])
v.check("Ex 16-05.5e", m5["thd"])
v.check("Ex 16-05.5f", m5["sfdr"])
v.check("Ex 16-05.5g", m5["enob"])
v.check("Ex 16-05.5h", 20 * math.log10((A / math.sqrt(2)) / math.sqrt(2e-4**2 + q**2 / 12)))
amp, res = sp.sine_fit3(yq, M5 / N5)
sinad_fit = 20 * math.log10(amp / math.sqrt(2) / res)
v.check("Ex 16-05.5i", sinad_fit)
v.assert_true("Ex 5: FFT and sine-fit SINAD agree to 0.01 dB", abs(sinad_fit - m5["sinad"]) < 0.01)
v.check("Ex 16-05.5j", (m5["sinad"] + 1 - 1.76) / 6.02)
v.check("Ex 16-05.5k", 2e-4 / q)
v.check("Ex 16-05.5l", 1 / 6.02)
v.check("Ex 16-05.5m", m5["snr"] - m5["sinad"])
v.check("Ex 16-05.5n", -m5["thd"] - m5["snr"])

# ---------------------------------------------------------------------------------------- concept checks
v.check("Txt 16-05.w", 512 / (2048 * 0.5 / 2))
v.check("Txt 16-05.x", 6.02 * 16 + 1.76)
v.check("Txt 16-05.y", 10 * math.log10(65536 / 2))
v.check("Txt 16-05.z", 6.02 * 16 + 1.76 + 10 * math.log10(65536 / 2))
v.check("Txt 16-05.aa", sp.coherent_bin(100e3, 1e6, 4096))
v.check("Txt 16-05.ab", sp.coherent_bin(100e3, 1e6, 4096) * 1e6 / 4096 / 1e3)
v.check("Txt 16-05.ac", (54.5 - 1.76) / 6.02)   # R-237: SINAD 54.5 dBFS from the data sheet

# ---------------------------------------------------------------------------------------- Problems
v.check("16-05.1a", 48000 / 2048)
v.check("16-05.1b", 48000 / 2048 * sp.enbw_bins(sp.window("blackman", 2048)))
wh4 = sp.window("hann", 4096)
v.check("16-05.1c", 20 * math.log10(sp._w_dtft(wh4, 15.5)[0] / sp._w_dtft(wh4, 0.5)[0]))
v.check("16-05.2a", 367.4 / (4096 * sp.coherent_gain(sp.window("bh4", 4096)) / 2))
v.check("16-05.3a", 6.02 * 14 + 1.76)
v.check("16-05.3b", 6.02 * 14 + 1.76 + 10 * math.log10(16384 / 2))
for Nh in (64, 1000, 4096):
    w = sp.window("hann", Nh)
    v.assert_true(f"P4: Hann sums N/2 and 3N/8 for N = {Nh}", abs(w.sum() - Nh / 2) < 1e-9 and abs((w**2).sum() - 3 * Nh / 8) < 1e-9)
v.check("16-05.4a", sp.enbw_bins(sp.window("hann", 4096)))
snr5 = 120 - 10 * math.log10(65536 / 2)
v.check("16-05.5a", snr5)
v.check("16-05.5b", (snr5 - 1.76) / 6.02)
wr = 2 * brentq(lambda nu: sp._w_dtft(sp.window("rect", 4096), nu)[0] / 4096 - 0.5, 0.01, 3, xtol=1e-12)
v.check("16-05.6a", wr * 48000 / 150)
v.check("16-05.6b", 1 << math.ceil(math.log2(wr * 48000 / 150)))
v.check("16-05.6c", 2.0 * 48000 / 150)
v.check("16-05.6d", 1 << math.ceil(math.log2(2.0 * 48000 / 150)))
K = math.ceil(1 / 0.1**2)
v.check("16-05.7a", K)
v.check("16-05.7b", K * 1024)
v.check("16-05.7c", K * 1024 / 48000)
# Monte Carlo: single periodogram scatter ~ 1; averages of K segments ~ 1/sqrt(K)
rngm = np.random.default_rng(57)
noise = rngm.normal(size=1024 * 100)
single = sp.periodogram(noise[:1024], sp.window("hann", 1024))[10:500]
avg, nseg = sp.welch(noise, 1024, overlap=0.0, name="hann")
v.assert_true("P7: one periodogram scatters about as much as its mean", 0.8 < single.std() / single.mean() < 1.2)
v.assert_true("P7: 100 averages bring the scatter near 0.1", nseg == 100 and 0.08 < avg[10:500].std() / avg[10:500].mean() < 0.12)
M8 = sp.coherent_bin(70e6, 250e6, 32768)
v.check("16-05.8a", M8)
v.check("16-05.8b", M8 * 250e6 / 32768 / 1e6)
fold = lambda b, N: (N - b % N) if b % N > N // 2 else b % N  # noqa: E731
v.check("16-05.8c", fold(2 * M8, 32768))
v.check("16-05.8d", fold(3 * M8, 32768))
v.check("16-05.9a", (70.0 - 1.76) / 6.02)
v.check("16-05.9b", (71.0 - 1.76) / 6.02)
thd = 10 * math.log10(sum(10 ** (x / 10) for x in (-85, -78, -95, -90)))
v.check("16-05.10a", thd)
v.check("16-05.10b", -10 * math.log10(10 ** (-72.0 / 10) + 10 ** (thd / 10)))
v.check("16-05.10c", -max(-85, -78, -95, -90))
for name, key in (("rect", "a"), ("bh4", "b")):
    w = sp.window(name, 8192)
    v.check(f"16-05.11{key}", 20 * math.log10(sp._w_dtft(w, 20.5)[0] / sp._w_dtft(w, 0.5)[0]))
fl_r = 80 + 10 * math.log10(8192 / (2 * sp.enbw_bins(sp.window("rect", 8192))))
fl_b = 80 + 10 * math.log10(8192 / (2 * sp.enbw_bins(sp.window("bh4", 8192))))
v.check("16-05.12a", fl_r)
v.check("16-05.12b", fl_b)
v.check("16-05.12c", fl_b - 100)

# ---------------------------------------------------------------------------------------- Lab
v.check("Lab 16-05.a", 6.02 * 12 + 1.76 + 10 * math.log10(65536 / 2))
N6 = 65536
M6 = sp.coherent_bin(N6 / 8.2, N6, N6)
x6 = (1 - 1e-9) * np.sin(2 * np.pi * M6 * np.arange(N6) / N6 + 0.3)
x6q = np.clip(np.round(x6 / q) * q, -1, 1 - q)
P6 = np.abs(np.fft.fft(x6q)) ** 2
sim_floor = 10 * math.log10(P6[M6] / np.mean(np.delete(P6[1:N6 // 2], [M6 - 1])))
v.assert_true("Lab: the simulated 65,536-point floor is within 0.3 dB of the theory", abs(sim_floor - (6.02 * 12 + 1.76 + 10 * math.log10(N6 / 2))) < 0.3)


def adc_record(cycles, seed=1605):
    rg = np.random.default_rng(seed)
    nn = np.arange(N5)
    xx = A * np.sin(2 * np.pi * cycles * nn / N5 + 0.7)
    yy = xx + a2 * xx**2 + a3 * xx**3 + rg.normal(scale=2.0e-4, size=N5)
    return np.clip(np.round(yy / q) * q, -1, 1 - q)


v.assert_true("Lab: the coherent record equals Example 5's", np.array_equal(adc_record(M5), yq))
yn = adc_record(M5 + 0.3)
v.check("Lab 16-05.b", sp.adc_metrics(yn, M5)["sinad"])
v.check("Lab 16-05.c", sp.adc_metrics_window(yn, "hann", M5 + 0.3)["sinad"])
bh = sp.adc_metrics_window(yn, "bh4", M5 + 0.3)["sinad"]
v.check("Lab 16-05.d", bh)
v.assert_true("Lab: Blackman-Harris recovers the coherent SINAD within 0.05 dB", abs(bh - m5["sinad"]) < 0.05)

sys.exit(v.finish())
