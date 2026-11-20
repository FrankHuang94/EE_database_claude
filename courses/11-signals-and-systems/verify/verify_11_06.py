#!/usr/bin/env python3
"""Verify every number in chapter 11-06 (the continuous-time Fourier transform), its solutions and lab.

Independent routes:
- transforms by numerical integration of x(t) e^{-j w t} (scipy quad) at each needed frequency, and by FFTs of
  finely sampled signals; inverse-transform statements by integrating X back;
- energies in both domains (time integrals and Parseval frequency integrals);
- bandwidths and crossing frequencies by root finding on numerically computed magnitudes or energy fractions;
- rise times from numerically integrated step responses and numerically convolved cascades;
- the ADS1292R sinc^3 response both in its exact digital form and its continuous-time limit;
- data-sheet and standards values (R-141, R-184, R-185) quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erf, erfinv, gammaincinv, sici

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-06", COURSE / "chapters" / "11-06-continuous-time-fourier-transform.md",
                        COURSE / "solutions" / "11-06-solutions.md",
                        COURSE / "labs" / "11-06-lab" / "README.md")


def ft(x, w, lo, hi, pts=None):
    re = quad(lambda t: x(t) * math.cos(w * t), lo, hi, points=pts, limit=800)[0]
    im = quad(lambda t: -x(t) * math.sin(w * t), lo, hi, points=pts, limit=800)[0]
    return complex(re, im)


db = lambda r: 20 * math.log10(r)


def frac_sinc2(W):
    return quad(lambda u: np.sinc(u) ** 2, -W, W, limit=800)[0]


def rise(step, t):
    return t[np.argmax(step >= 0.9)] - t[np.argmax(step >= 0.1)]


# ============================================================ theory and practitioner
W = 1.0
lp = lambda t: 0.5 + sici(W * t)[0] / math.pi
tpk = brentq(lambda t: math.sin(W * t) / (math.pi * t), 2.5, 3.5)        # derivative of the step = h(t) = 0
v.check("T 11-06.a", lp(tpk))
sig = 1.0
g_step = lambda t: 0.5 * (1 + erf(t / (math.sqrt(2) * sig)))
t10 = brentq(lambda t: g_step(t) - 0.1, -5, 5)
t90 = brentq(lambda t: g_step(t) - 0.9, -5, 5)
v.check("T 11-06.b", t90 - t10)
G = lambda f: math.exp(-2 * math.pi ** 2 * sig ** 2 * f ** 2)
f3g = brentq(lambda f: G(f) - 1 / math.sqrt(2), 1e-4, 1)
v.check("T 11-06.c", f3g * sig)
v.check("T 11-06.d", 10 ** (-32 / 20))                                    # 32 dB at 16 GHz [R-141]
v.check("T 11-06.e", 53.125 / 2)                                         # half of 53.125 GBd [R-141]
v.check("T 11-06.f", math.sqrt(500 ** 2 + 350 ** 2))
v.check("T 11-06.g", 100 * (math.sqrt(500 ** 2 + 350 ** 2) / 500 - 1))
v.check("T 11-06.h", 10 ** (32 / 20))
# cascades of single-pole stages, each with a 1 ns rise time, by numerical convolution
t = np.linspace(0, 20e-9, 400001)
dt = t[1] - t[0]
tau = 1e-9 / math.log(9)
h1 = np.exp(-t / tau) / tau
h2 = np.convolve(h1, h1)[: len(t)] * dt
s2 = np.cumsum(h2) * dt
tr2 = rise(s2, t)
v.check("T 11-06.i", math.sqrt(2))
v.check("T 11-06.j", tr2 * 1e9)
v.check("T 11-06.k", 100 * (tr2 * 1e9 / math.sqrt(2) - 1))
v.check("T 11-06.l", 100 * ((t90 - t10) / math.log(9) - 1))
v.check("Lab 11-06.e", tr2 * 1e9)
h4 = h2.copy()
for _ in range(2):
    h4 = np.convolve(h4, h1)[: len(t)] * dt
v.check("Lab 11-06.f", (gammaincinv(4, 0.9) - gammaincinv(4, 0.1)) * tau * 1e9)  # Erlang-4, exact
v.assert_true("numerical 4-stage convolution agrees within 0.1%", abs(rise(np.cumsum(h4) * dt, t) / ((gammaincinv(4, 0.9) - gammaincinv(4, 0.1)) * tau) - 1) < 1e-3)
sg = 1e-9 / (t90 - t10)
gg = 0.5 * (1 + erf((t - 10e-9) / (math.sqrt(2 * 2) * sg)))
v.check("Lab 11-06.g", rise(gg, t) * 1e9)
v.check("Lab 11-06.h", 0.35 / 20e6 * 1e9)

# ============================================================ Example 1
a = 1000.0
xe = lambda tt: math.exp(-a * tt)
X0 = ft(xe, 0.0, 0, 0.05)
Xa = ft(xe, a, 0, 0.05)
v.check("Ex 11-06.1a", abs(X0) * 1e3)
v.check("Ex 11-06.1b", abs(Xa) * 1e3)
v.check("Ex 11-06.1c", math.degrees(math.atan2(Xa.imag, Xa.real)))
E1 = quad(lambda tt: xe(tt) ** 2, 0, 0.05)[0]
v.check("Ex 11-06.1d", E1 * 1e3)
E1f = quad(lambda w: 1 / (a * a + w * w), -np.inf, np.inf)[0] / (2 * math.pi)
v.assert_true("Parseval for the exponential", abs(E1f - E1) < 1e-12)

# ============================================================ Example 2
T = 1e-6
rect = lambda tt: 1.0 if 0 <= tt < T else 0.0
v.check("Ex 11-06.2a", abs(ft(rect, 2 * math.pi * 0.5e6, 0, T)) * 1e6)
nul = brentq(lambda f: abs(ft(rect, 2 * math.pi * f, 0, T)) / T, 0.6e6, 1.4e6) if False else None
fz = np.linspace(0.8e6, 1.2e6, 4001)
mags = np.array([abs(ft(rect, 2 * math.pi * f, 0, T)) for f in fz[::40]])
v.check("Ex 11-06.2b", fz[::40][np.argmin(mags)] / 1e6)
v.check("Ex 11-06.2c", 100 * frac_sinc2(1.0))
v.check("Ex 11-06.2d", 100 * frac_sinc2(0.5))

# ============================================================ Example 3
rect2 = lambda tt: 1.0 if -T / 4 <= tt < T / 4 else 0.0                   # p(2t)
fz2 = np.linspace(1.5e6, 2.5e6, 201)
m2 = [abs(ft(rect2, 2 * math.pi * f, -T / 4, T / 4)) for f in fz2]
v.check("Ex 11-06.3a", fz2[int(np.argmin(m2))] / 1e6)
v.check("Ex 11-06.3b", quad(lambda tt: rect2(tt) ** 2, -T, T, points=[-T / 4, T / 4])[0] / T)
fc = 10e6
modp = lambda tt: (1.0 if -T / 2 <= tt < T / 2 else 0.0) * math.cos(2 * math.pi * fc * tt)
v.check("Ex 11-06.3c", abs(ft(modp, 2 * math.pi * fc, -T / 2, T / 2)) * 1e6)

# ============================================================ Example 4: sinc^3, exact digital form and limit
N, fmod = 256, 128e3
fdr = fmod / N
Hx = lambda f: abs(math.sin(math.pi * f * N / fmod) / (N * math.sin(math.pi * f / fmod))) ** 3
Hl = lambda f: abs(np.sinc(f / fdr)) ** 3
f3x = brentq(lambda f: Hx(f) - 1 / math.sqrt(2), 1, 400)
f3l = brentq(lambda f: Hl(f) - 1 / math.sqrt(2), 1, 400)
v.check("Ex 11-06.4a", f3l / fdr)
v.check("Ex 11-06.4b", f3x)
v.assert_true("data sheet's 0.262 f_DR matches", abs(f3x / fdr - 0.262) < 5e-4)
v.check("Ex 11-06.4c", db(Hx(60)))
v.check("Ex 11-06.4d", db(Hx(250)))
v.check("Lab 11-06.d", f3x)
# also: build the filter from three boxcars and take its FFT
box = np.ones(N) / N
h3 = np.convolve(np.convolve(box, box), box)
Hfft = lambda f: abs(np.sum(h3 * np.exp(-2j * math.pi * f / fmod * np.arange(len(h3)))))
v.assert_true("boxcar cascade's response equals the closed form at 131 Hz", abs(Hfft(131.0) - Hx(131.0)) < 1e-9)

# ============================================================ Example 5: energies in both domains
tau = 1e-3
def y5(tt):
    return 5 * (1 - math.exp(-tt / tau)) if tt < 2e-3 else 5 * (1 - math.exp(-2)) * math.exp(-(tt - 2e-3) / tau)
v.check("Ex 11-06.5a", 25 * 2e-3 * 1e3)
Ey = 2 * quad(lambda f: (10e-3 * np.sinc(f * 2e-3)) ** 2 / (1 + (2 * math.pi * f * tau) ** 2), 0, 50000, limit=4000)[0]
Ey_t = quad(lambda tt: y5(tt) ** 2, 0, 2e-3)[0] + quad(lambda tt: y5(tt) ** 2, 2e-3, 0.05, limit=400)[0]
v.check("Ex 11-06.5b", Ey * 1e3)
v.assert_true("time and frequency energies agree", abs(Ey - Ey_t) < 1e-6)
v.check("Ex 11-06.5c", 100 * Ey_t / 50e-3)

# ============================================================ Example 6
fracE = lambda Wn: quad(lambda w: 1 / (1 + w * w), -Wn, Wn, limit=500)[0] / math.pi
v.check("Ex 11-06.6a", brentq(lambda Wn: fracE(Wn) - 0.99, 1, 1000))
gfrac = lambda z: quad(lambda w: math.exp(-w * w), -z, z)[0] / math.sqrt(math.pi)
v.check("Ex 11-06.6b", brentq(lambda z: gfrac(z) - 0.99, 0.1, 5) / math.sqrt(math.log(2)))

# ============================================================ Example 7
f3 = 100e6
tt7 = np.linspace(0, 40e-9, 400001)
sp = 1 - np.exp(-tt7 * 2 * math.pi * f3)
tr7 = rise(sp, tt7)
v.check("Ex 11-06.7a", tr7 * 1e9)
v.check("Ex 11-06.7b", tr7 * f3)
v.check("Ex 11-06.7c", (t90 - t10) * f3g)
v.check("Ex 11-06.7d", math.sqrt(1 + 0.35 ** 2))

# ============================================================ Example 8
Ts = 1 / 32e9
v.check("Ex 11-06.8a", 1 / (2 * Ts) / 1e9)
v.check("Ex 11-06.8b", 1 / Ts / 1e9)
v.check("Ex 11-06.8c", 100 * frac_sinc2(0.5))
v.check("Ex 11-06.8d", 100 * frac_sinc2(1.0))

# ============================================================ solutions
xa = lambda tt: math.exp(-3 * tt)
v.check("11-06.1a", abs(ft(xa, 0.0, 2, 30)))
xb = lambda tt: math.exp(-2 * abs(tt))
v.check("11-06.1b", ft(xb, 0.0, -30, 30, pts=[0]).real)
xc = lambda tt: math.cos(2 * math.pi * 1000 * tt) if abs(tt) < 0.005 else 0.0
v.check("11-06.1c", abs(ft(xc, 2 * math.pi * 1000, -0.005, 0.005)))
# 2(a): inverse transform of 1/(2 + jw)^2 by numerical inverse integral at a few t, then peak
inv = lambda tt: quad(lambda w: (np.real(np.exp(1j * w * tt) / (2 + 1j * w) ** 2)), -400, 400, limit=4000)[0] / (2 * math.pi)
v.assert_true("inverse of 1/(2+jw)^2 is t e^{-2t} at t = 0.7",
              abs(inv(0.7) - 0.7 * math.exp(-1.4)) < 2e-3)
tp = np.linspace(0.01, 3, 30000)
yp = tp * np.exp(-2 * tp)
v.check("11-06.2a", tp[np.argmax(yp)])
v.check("11-06.2b", yp.max())
Wc = 2 * math.pi * 1000
v.check("11-06.3a", quad(lambda w: 1.0, -Wc, Wc)[0] / (2 * math.pi))
v.check("11-06.4a", 1 / 10e-9 / 1e6)
v.check("11-06.4b", 1 / 1e-9 / 1e9)
v.check("11-06.4c", quad(lambda tt: 1.0 ** 2, 0, 10e-9)[0] * 1e9)    # energy of a 1 V, 10 ns pulse in V²·ns
v.check("11-06.4d", quad(lambda tt: 1.0 ** 2, 0, 1e-9)[0] * 1e9)
v.check("11-06.4e", abs(ft(lambda tt: 1.0, 0.0, 0, 10e-9)) / abs(ft(lambda tt: 1.0, 0.0, 0, 1e-9)))
tri = lambda tt: max(0.0, 1 - abs(tt))
v.check("11-06.5a", ft(tri, 0.0, -1, 1, pts=[0]).real)
v.check("11-06.5b", ft(tri, 2 * math.pi * 0.5, -1, 1, pts=[0]).real)
v.check("11-06.6a", quad(lambda tt: (math.exp(-tt / 1e-3) / 1e-3) ** 2, 0, 0.05)[0])
tau7 = 1e-6
ph = lambda w: np.unwrap([np.angle((1 - 1j * ww * tau7) / (1 + 1j * ww * tau7)) for ww in w])
wg = np.array([-1e2, 1e2])
v.check("11-06.7a", -(ph(wg)[1] - ph(wg)[0]) / (wg[1] - wg[0]) * 1e6)
w1 = 1 / tau7
wg = np.array([w1 * (1 - 1e-5), w1 * (1 + 1e-5)])
v.check("11-06.7b", -(ph(wg)[1] - ph(wg)[0]) / (wg[1] - wg[0]) * 1e6)
v.assert_true("all-pass magnitude is 1", abs(abs((1 - 1j * 3.7) / (1 + 1j * 3.7)) - 1) < 1e-15)
v.check("11-06.8a", Wc / math.pi)
v.check("11-06.8b", brentq(lambda tt: math.sin(Wc * tt), 0.3e-3, 0.7e-3) * 1e3)
v.check("11-06.8c", 0.5 + sici(math.pi)[0] / math.pi)
v.check("11-06.9a", brentq(lambda Wn: frac_sinc2(Wn) - 0.9, 0.3, 1.0))
v.check("11-06.9b", brentq(lambda Wn: frac_sinc2(Wn) - 0.99, 1, 30))
v.check("11-06.10a", 0.35 / 2e9 * 1e12)
v.check("11-06.10b", math.sqrt(175 ** 2 + 300 ** 2))
v.check("11-06.10c", 100 * (math.sqrt(175 ** 2 + 300 ** 2) / 300 - 1))
st = math.sqrt(quad(lambda tt: tt * tt * math.exp(-2 * abs(tt)), -40, 40, points=[0])[0]
               / quad(lambda tt: math.exp(-2 * abs(tt)), -40, 40, points=[0])[0])
sw = math.sqrt(quad(lambda w: w * w * (2 / (1 + w * w)) ** 2, -np.inf, np.inf)[0]
               / quad(lambda w: (2 / (1 + w * w)) ** 2, -np.inf, np.inf)[0])
v.check("11-06.11a", st * sw)
v.check("11-06.12a", 1000 - 5)
v.check("11-06.12b", 1000 + 5)
v.check("11-06.12c", 2 * 5)
v.check("11-06.13a", 10 ** (-32 / 20))
v.check("11-06.13b", 15.5 / 1.0)
v.check("11-06.13c", 15.5 / 2.0)
v.check("11-06.14a", brentq(lambda f: abs(np.sinc(f / 2000)) ** 3 - 1 / math.sqrt(2), 1, 1000))
v.check("11-06.14b", db(abs(np.sinc(60 / 2000)) ** 3))
gcd_rate = math.gcd(50, 60)
v.check("11-06.14c", gcd_rate)
v.assert_true("10 SPS sinc notches 50, 60, 100, 120 Hz",
              all(abs(np.sinc(f / gcd_rate)) < 1e-12 for f in (50, 60, 100, 120)))

# ============================================================ lab
def ft_by_fft(x, t0, dtt, Nn):
    tt = t0 + dtt * np.arange(Nn)
    f = np.fft.fftfreq(Nn, dtt)
    X = dtt * np.fft.fft(x(tt)) * np.exp(-2j * np.pi * f * t0)
    return np.fft.fftshift(f), np.fft.fftshift(X)


f, X = ft_by_fft(lambda tt: ((tt >= -T / 2) & (tt < T / 2)).astype(float), -4e-6, 1e-9, 2 ** 15)
i = int(np.argmin(np.abs(f - 0.5e6)))
v.check("Lab 11-06.a", abs(X[i]) * 1e6)
v.assert_true("the bin is at 0.4883 MHz", abs(f[i] / 1e6 - 0.4883) < 5e-5)
f, X = ft_by_fft(lambda tt: np.exp(-tt ** 2 / 2), -40, 0.01, 2 ** 14)
i = int(np.argmin(np.abs(f - 0.2)))
v.check("Lab 11-06.b", abs(X[i]))
dtl = 1e-6
tl = np.arange(0, 0.05, dtl)
xl = 5.0 * (tl < 2e-3)
hl = np.exp(-tl / 1e-3) / 1e-3
yl = np.real(np.fft.ifft(np.fft.fft(xl, 2 * len(tl)) * np.fft.fft(hl, 2 * len(tl))))[: len(tl)] * dtl
v.check("Lab 11-06.c", np.sum(yl ** 2) * dtl * 1e3)

sys.exit(v.finish())
