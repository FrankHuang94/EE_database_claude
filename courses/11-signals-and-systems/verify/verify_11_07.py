#!/usr/bin/env python3
"""Verify every number in chapter 11-07 (the discrete-time Fourier transform), its solutions and lab.

Independent routes:
- DTFTs by direct summation of x[n] e^{-j w n} at each frequency (never from the closed forms), and by
  zero-padded FFTs;
- Parseval by numerical integration over one period;
- peaks, bandwidths, transition widths and stopband levels by dense grids, optimization and root finding on
  computed magnitudes;
- frequency responses also by driving the filters with long sinusoids and measuring steady-state amplitudes;
- windowed designs by building the taps and evaluating their responses; resolution by evaluating windowed
  DTFTs; downsampling by generating the sequences;
- library and data-sheet facts (R-186, R-187) quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-07", COURSE / "chapters" / "11-07-discrete-time-fourier-transform.md",
                        COURSE / "solutions" / "11-07-solutions.md",
                        COURSE / "labs" / "11-07-lab" / "README.md")


def dtft(x, w, n0=0):
    n = n0 + np.arange(len(x))
    return complex(np.sum(np.asarray(x) * np.exp(-1j * w * n)))


db = lambda r: 20 * math.log10(r)
exp08 = 0.8 ** np.arange(400)
X08 = lambda w: dtft(exp08, w)


def design(L, window, wgrid=np.linspace(0, np.pi, 30001)):
    M = (L - 1) // 2
    m = np.arange(-M, M + 1)
    h = np.where(m == 0, 0.25, np.sin(np.pi * m / 4) / (np.pi * np.where(m == 0, 1, m)))
    if window == "hamming":
        h = h * np.hamming(L)
    H = np.cos(np.outer(wgrid, m)) @ h
    i9 = np.where(H >= 0.9)[0]
    i9 = i9[wgrid[i9] <= np.pi / 4 + 0.3].max()
    i1 = int(np.argmax((wgrid > np.pi / 4) & (H <= 0.1)))
    return h, H, wgrid, wgrid[i1] - wgrid[i9]


# ============================================================ theory / practitioner
v.check("T 11-07.a", 12 / 48e3 * 1e3)
v.check("T 11-07.b", (25 - 1) / 2)
v.check("T 11-07.c", (math.pi / 2) * 1000 / (2 * math.pi))
v.check("T 11-07.d", math.pi * 1000 / (2 * math.pi))
v.check("T 11-07.e", 1 / 0.1)
h21, H21, wg, tw21 = design(21, "rect")
v.check("T 11-07.f", 100 * (H21[wg <= np.pi / 4].max() - 1))
v.check("T 11-07.g", -db(np.abs(H21[wg >= 0.5 * np.pi]).max()))
h21h, H21h, _, _ = design(21, "hamming")
v.check("T 11-07.h", -db(np.abs(H21h[wg >= 0.5 * np.pi]).max()))
v.check("T 11-07.i", abs(X08(0)) ** 2)
v.check("T 11-07.j", abs(X08(math.pi)) ** 2)
h81, H81, _, tw81 = design(81, "rect")
v.check("T 11-07.k", tw21 / tw81)
v.check("T 11-07.l", 100 * (H81[wg <= np.pi / 4].max() - 1))
v.assert_true("periodicity of the DTFT", abs(X08(0.3) - X08(0.3 + 2 * math.pi)) < 1e-12)

# ============================================================ Example 1
v.check("Ex 11-07.1a", abs(X08(0)))
v.check("Ex 11-07.1b", abs(X08(math.pi)))
v.check("Ex 11-07.1c", abs(X08(math.pi / 2)))
v.check("Ex 11-07.1d", math.degrees(np.angle(X08(math.pi / 2))))

# ============================================================ Example 2: five-point average at 500 SPS
h5 = np.ones(5) / 5
H5 = lambda w: dtft(h5, w)
nulls = [brentq(lambda w: (H5(w) * np.exp(2j * w)).real, a_, b_, xtol=1e-14) for a_, b_ in ((1.0, 1.5), (2.3, 2.7))]
v.check("Ex 11-07.2a", nulls[0] * 500 / (2 * math.pi))
v.check("Ex 11-07.2b", nulls[1] * 500 / (2 * math.pi))
v.check("Ex 11-07.2c", abs(H5(0.2 * math.pi)))
wq = np.linspace(0.1, 1.0, 50)
ph = np.unwrap([np.angle(H5(w)) for w in wq])
gd = -np.polyfit(wq, ph, 1)[0]
v.check("Ex 11-07.2d", gd)
v.check("Ex 11-07.2e", gd / 500 * 1e3)
n = np.arange(3000)
y50 = np.convolve(np.cos(0.2 * math.pi * n), h5)[100:3000]
v.assert_true("measured gain at 50 Hz matches", abs(np.max(np.abs(y50)) - abs(H5(0.2 * math.pi))) < 1e-3)

# ============================================================ Example 3
v.check("Ex 11-07.3a", abs(dtft([0.5, -0.5], math.pi)))
halt = h5 * (-1.0) ** np.arange(5)
v.check("Ex 11-07.3b", abs(dtft(halt, 0.0)))
v.check("Ex 11-07.3c", abs(dtft(halt, math.pi)))

# ============================================================ Example 4
v.check("Ex 11-07.4a", h21[10])
v.check("Ex 11-07.4b", h21[11])
v.check("Ex 11-07.4c", H21[wg <= np.pi / 4].max())
v.check("Ex 11-07.4d", db(np.abs(H21[wg >= 0.5 * np.pi]).max()))
v.check("Ex 11-07.4e", H21h[wg <= np.pi / 4].max())
v.check("Ex 11-07.4f", db(np.abs(H21h[wg >= 0.5 * np.pi]).max()))
v.check("Ex 11-07.4g", np.interp(np.pi / 4, wg, H21))
v.assert_true("Hamming also about 0.5 at the cutoff", abs(np.interp(np.pi / 4, wg, H21h) - 0.5) < 0.01)

# ============================================================ Example 5
E_f = quad(lambda w: abs(X08(w)) ** 2, -math.pi, math.pi, limit=200)[0] / (2 * math.pi)
v.check("Ex 11-07.5a", E_f)
v.assert_true("time-domain energy agrees", abs(np.sum(exp08 ** 2) - E_f) < 1e-9)

# ============================================================ Example 6: resonator
c = 2 * 0.9 * math.cos(math.pi / 4)
hr = np.zeros(800)
for k in range(800):
    hr[k] = (1.0 if k == 0 else 0.0) + c * (hr[k - 1] if k >= 1 else 0) - 0.81 * (hr[k - 2] if k >= 2 else 0)
Hr = lambda w: abs(dtft(hr, w))
v.check("Ex 11-07.6a", Hr(0.0))
res = minimize_scalar(lambda w: -Hr(w), bounds=(0.5, 1.0), method="bounded", options={"xatol": 1e-10})
wp, Hp = res.x, Hr(res.x)
v.check("Ex 11-07.6b", Hp)
v.check("Ex 11-07.6c", wp)
lo = brentq(lambda w: Hr(w) - Hp / math.sqrt(2), 0.4, wp)
hi = brentq(lambda w: Hr(w) - Hp / math.sqrt(2), wp, 1.3)
v.check("Ex 11-07.6d", hi - lo)
v.check("Ex 11-07.6e", wp / (hi - lo))

# ============================================================ Example 7
fs = 8000.0
v.check("Ex 11-07.7a", 2 * 1000 / fs)
v.check("Ex 11-07.7b", fs / 64)
v.check("Ex 11-07.7c", fs / 512)
v.check("Ex 11-07.7d", 1 / 50 * 1e3)
v.check("Ex 11-07.7e", fs / 50)


def tones_mag(N, f):
    m = np.arange(N)
    x = np.cos(2 * np.pi * 1000 * m / fs) + np.cos(2 * np.pi * 1050 * m / fs)
    return abs(np.sum(x * np.exp(-2j * np.pi * f * m / fs))) / N


ratio = lambda N: tones_mag(N, 1025) / max(tones_mag(N, 1000), tones_mag(N, 1050))
v.assert_true("64 samples merge the tones, 512 resolve them", ratio(64) > 0.9 and ratio(512) < 0.3)

# ============================================================ solutions
x3 = [1.0, 2.0, 1.0]
v.check("11-07.1a", abs(dtft(x3, 0)))
v.check("11-07.1b", abs(dtft(x3, math.pi / 2)))
v.check("11-07.1c", abs(dtft(x3, math.pi)))
v.check("11-07.2a", 2 * 1e3 / 48e3)
v.check("11-07.2b", 48e3 / 2 / 1e3)
m = np.arange(200)
s30 = np.cos(2 * np.pi * 30e3 / 48e3 * m)
s18 = np.cos(2 * np.pi * 18e3 / 48e3 * m)
v.assert_true("30 kHz and 18 kHz give the same samples at 48 kHz", np.allclose(s30, s18))
v.check("11-07.2c", abs(30e3 - 48e3 * round(30e3 / 48e3)) / 1e3)  # fold into [0, fs/2]
xr = np.random.default_rng(7).normal(size=12)
Xp = dtft(xr, 0.3 * math.pi)
Xm = dtft(xr, -0.3 * math.pi)
v.assert_true("conjugate symmetry and 2pi periodicity",
              abs(Xm - np.conj(Xp)) < 1e-12 and abs(dtft(xr, 1.7 * math.pi) - Xm) < 1e-12
              and abs(dtft(xr, 2.3 * math.pi) - Xp) < 1e-12)
X03 = 2 * np.exp(-1j * math.radians(40))           # the given value at +0.3*pi
v.check("11-07.3a", abs(np.conj(X03)))
v.check("11-07.3b", math.degrees(np.angle(np.conj(X03))))
xm5 = (-0.5) ** np.arange(400)
v.check("11-07.4a", abs(dtft(xm5, 0)))
v.check("11-07.4b", abs(dtft(xm5, math.pi)))
x2s = 0.5 ** np.abs(np.arange(-300, 301))
v.check("11-07.5a", dtft(x2s, 0.0, n0=-300).real)
v.check("11-07.5b", dtft(x2s, math.pi, n0=-300).real)
v.assert_true("two-sided exponential's DTFT is real", abs(dtft(x2s, 1.1, n0=-300).imag) < 1e-12)
bp = lambda k: quad(lambda w: math.cos(w * k), math.pi / 4, math.pi / 2)[0] / math.pi
v.check("11-07.6a", bp(0))
v.check("11-07.6b", bp(1))
hb = np.array([1, 3, 3, 1]) / 8
wq = np.linspace(0.1, 2.0, 50)
phb = np.unwrap([np.angle(dtft(hb, w)) for w in wq])
v.check("11-07.7a", -np.polyfit(wq, phb, 1)[0])
v.check("11-07.7b", abs(dtft(hb, 0)))
v.check("11-07.7c", abs(dtft(hb, math.pi / 2)))
v.check("11-07.7d", abs(dtft(hb, math.pi)))
w0 = 2 * math.pi * 60 / 500
hn = np.array([1, -2 * math.cos(w0), 1])
v.check("11-07.8a", -hn[1] / 2)
v.check("11-07.8b", abs(dtft(hn, 0)))
hnn = hn / abs(dtft(hn, 0))
v.check("11-07.8c", abs(dtft(hnn, 2 * math.pi * 50 / 500)))
v.check("11-07.8d", abs(dtft(hnn, 2 * math.pi * 120 / 500)))
v.assert_true("the notch nulls 60 Hz", abs(dtft(hnn, w0)) < 1e-12)
noise = np.random.default_rng(11).normal(size=400000)
yv = np.convolve(noise, h5, mode="valid")
v.assert_true("measured variance factor near 0.2", abs(np.var(yv) - 0.2) < 0.005)
v.check("11-07.9a", np.sum(h5 ** 2))
v.check("11-07.10a", 1 / (60 - 50))
v.check("11-07.10b", 2 / (60 - 50))
L = next(L for L in range(41, 301, 2) if design(L, "hamming")[3] <= 0.05 * np.pi)
_, HL, wgL, twL = design(L, "hamming")
v.check("11-07.11a", L)
v.check("11-07.11b", twL / np.pi)
v.check("11-07.11c", db(np.abs(HL[wgL >= np.pi / 4 + 0.05 * np.pi]).max()))
yd = np.cos(0.6 * np.pi * 2 * np.arange(100))
v.assert_true("downsampled sequence is cos(0.8 pi n)", np.allclose(yd, np.cos(0.8 * np.pi * np.arange(100))))
v.check("11-07.12a", 0.8)

# ============================================================ lab
nl = np.arange(2000)
yl = np.convolve(np.cos(2 * np.pi * 150 / 500 * nl), h5)[100:2000]
v.check("Lab 11-07.a", np.max(np.abs(yl)))
v.check("Lab 11-07.b", H81[wg <= np.pi / 4].max())
_, H201, _, _ = design(201, "rect")
v.check("Lab 11-07.c", H201[wg <= np.pi / 4].max())
_, H81h, _, tw81h = design(81, "hamming")
v.check("Lab 11-07.d", tw81h / np.pi)
v.check("Lab 11-07.e", db(np.abs(H81h[wg >= 0.5 * np.pi]).max()))
v.check("Lab 11-07.f", ratio(64))
v.check("Lab 11-07.g", ratio(160))
v.check("Lab 11-07.h", ratio(512))
_, H201h, _, _ = design(201, "hamming")
v.check("Lab 11-07.i", db(np.abs(H201h[wg >= 0.5 * np.pi]).max()))
v.check("Lab 11-07.j", db(np.abs(H21h[wg >= 0.5 * np.pi]).max()))

# ============================================================ DTFS (3.7) and Problems 13-14, by FFT
x4 = np.array([1.0, 1.0, 0.0, 0.0])
a4 = np.fft.fft(x4) / 4
v.check("T 11-07.m", a4[0].real)
v.check("T 11-07.n", abs(a4[1]))
v.check("T 11-07.o", np.mean(x4 ** 2))
v.assert_true("DTFS Parseval, period 4", abs(np.mean(x4 ** 2) - np.sum(abs(a4) ** 2)) < 1e-12)
x6 = np.array([3.0, 2, 1, 0, 1, 2])
a6 = np.fft.fft(x6) / 6
v.assert_true("DTFS of a real even period is real", np.allclose(a6.imag, 0))
v.check("11-07.13a", a6[0].real)
v.check("11-07.13b", a6[1].real)
v.check("11-07.13c", a6[2].real)
v.check("11-07.13d", a6[3].real)
v.check("11-07.13e", np.mean(x6 ** 2))
v.assert_true("Parseval, period 6", abs(np.mean(x6 ** 2) - np.sum(abs(a6) ** 2)) < 1e-12)
v.assert_true("synthesis recovers the period", np.allclose(np.fft.ifft(a6 * 6).real, x6))
X4 = np.fft.fft(np.ones(4))
X8 = np.fft.fft(np.ones(4), 8)
v.check("11-07.14a", X4[0].real)
v.assert_true("other 4-point bins are zero", np.allclose(X4[1:], 0))
v.check("11-07.14b", abs(X8[1]))
v.check("11-07.14c", abs(X8[2]))
v.check("11-07.14d", abs(X8[3]))
w8 = np.pi * np.arange(8) / 4
dtft = np.array([np.sum(np.exp(-1j * w * np.arange(4))) for w in w8])
v.assert_true("8-point DFT samples the DTFT", np.allclose(X8, dtft))

sys.exit(v.finish())
