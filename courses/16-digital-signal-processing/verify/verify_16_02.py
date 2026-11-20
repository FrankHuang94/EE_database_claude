#!/usr/bin/env python3
"""Verify chapter 16-02 (DTFT and z-transform for DSP): examples, concept checks, problems and lab answers.

Routes:
- frequency responses directly from the coefficients (labs/16-02-lab/pz.py) and, independently, from
  scipy.signal.freqz and from the pole-zero vector formula;
- group delay in closed form (sum over roots) against numerical differentiation of the phase and scipy.signal.group_delay;
- notch and resonator band edges by root finding on |H|, peaks by a fine search refined with a bounded optimizer;
- impulse responses by scipy.signal.lfilter; the anticausal inverse by direct convolution with the channel;
- partial-fraction impulse responses by evaluating the series numerically against the z-transform.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "16-02-lab"))
from eeverify import Verifier  # noqa: E402
import pz  # noqa: E402

CH = ROOT / "chapters" / "16-02-dtft-and-z-transform-for-dsp.md"
v = Verifier.from_files("16-02", CH, ROOT / "solutions" / "16-02-solutions.md", ROOT / "labs" / "16-02-lab" / "README.md")


def H(b, a, w):
    return complex(pz.freq_resp(b, a, w)[0])


def scipy_H(b, a, w):
    return complex(signal.freqz(b, a, worN=[w])[1][0])


def band_edges(b, a, w_peak_or_null, level, lo, hi):
    f = lambda w: abs(H(b, a, w)) - level  # noqa: E731
    return brentq(f, lo, w_peak_or_null, xtol=1e-14), brentq(f, w_peak_or_null, hi, xtol=1e-14)


def find_peak(b, a, lo, hi):
    W = np.linspace(lo, hi, 200001)
    k = int(np.argmax(np.abs(pz.freq_resp(b, a, W))))
    r = minimize_scalar(lambda w: -abs(H(b, a, w)), bounds=(W[max(k - 1, 0)], W[min(k + 1, len(W) - 1)]),
                        method="bounded", options={"xatol": 1e-13})
    return -r.fun, r.x


# self-test of the helpers against scipy
wt = np.linspace(0.01, 3.1, 50)
for b, a in (([1, 1], [1, -0.5]), ([1, -2.5, 1], [1]), ([0.3, 0.1], [1, -1.2, 0.5])):
    v.assert_true(f"helpers: freq_resp matches scipy.freqz for {b}/{a}",
                  np.allclose(pz.freq_resp(b, a, wt), signal.freqz(b, a, worN=wt)[1]))
    z, p, k = pz.zpk(b, a)
    v.assert_true(f"helpers: geometric form matches for {b}/{a}", np.allclose(pz.freq_resp(b, a, wt), pz.geometric(z, p, k, wt)))
    v.assert_true(f"helpers: closed-form group delay matches numeric for {b}/{a}",
                  np.allclose(pz.group_delay(b, a, wt), pz.group_delay_numeric(b, a, wt), atol=1e-5))
    v.assert_true(f"helpers: group delay matches scipy for {b}/{a}",
                  np.allclose(pz.group_delay(b, a, wt), signal.group_delay((b, a), w=wt)[1], atol=1e-6))

# ---------------------------------------------------------------------------------------- Example 1
b1, a1 = [1, 1], [1, -0.5]
v.check("Ex 16-02.1a", abs(H(b1, a1, 0)))
h = scipy_H(b1, a1, math.pi / 2)
v.check("Ex 16-02.1b", abs(h))
v.check("Ex 16-02.1c", math.degrees(np.angle(h)))
v.check("Ex 16-02.1d", abs(H(b1, a1, math.pi)))
v.check("Ex 16-02.1e", math.degrees(np.angle(1j - 0.5)))

# ---------------------------------------------------------------------------------------- Example 2
fs = 1000.0
w0 = 2 * math.pi * 50 / fs
v.check("Ex 16-02.2a", 2 * math.cos(w0))
r = 0.98
a2 = [1, -2 * r * math.cos(w0), r * r]
v.check("Ex 16-02.2b", -a2[1])
v.check("Ex 16-02.2c", a2[2])
v.check("Ex 16-02.2d", abs(H([1, -2 * math.cos(w0), 1], a2, 0)))
v.check("Ex 16-02.2e", 2 * (1 - r) * fs / (2 * math.pi))
bn, an = pz.notch(w0, r)
v.assert_true("Ex 2: scaled notch has unit DC gain and an exact null", abs(abs(H(bn, an, 0)) - 1) < 1e-12 and abs(H(bn, an, w0)) < 1e-12)
lo, hi = band_edges(bn, an, w0, 1 / math.sqrt(2), 1e-4, 1.0)
v.check("Ex 16-02.2f", (hi - lo) * fs / (2 * math.pi))
v.check("Ex 16-02.2g", abs(H(bn, an, 2 * math.pi * 10 / fs)))
v.check("Ex 16-02.2h", abs(H(bn, an, 2 * math.pi * 60 / fs)))
tau = -1 / math.log(r)
v.check("Ex 16-02.2i", tau)
# the transient decays as r^n: check the impulse response envelope
hn = signal.lfilter(bn, an, np.r_[1.0, np.zeros(999)])
v.assert_true("Ex 2: |h[n]| decays no slower than r^n (times a constant)", np.max(np.abs(hn[200:]) / r ** np.arange(200, 1000)) < 1.0)
bn9, an9 = pz.notch(w0, 0.9)
lo9, hi9 = band_edges(bn9, an9, w0, 1 / math.sqrt(2), 1e-4, 1.5)
v.check("Ex 16-02.2j", (hi9 - lo9) * fs / (2 * math.pi))
v.check("Ex 16-02.2k", -1 / math.log(0.9) / fs * 1e3)
v.check("Ex 16-02.2l", (hi - lo) * tau)

# ---------------------------------------------------------------------------------------- Example 3
br, ar = pz.resonator(math.pi / 4, 0.99)
e = np.exp(1j * math.pi / 4)
v.check("Ex 16-02.3a", abs(e - 0.99 * e))
v.check("Ex 16-02.3b", abs(e - 0.99 * np.conj(e)))
g0 = abs(H(br, ar, math.pi / 4))
v.check("Ex 16-02.3c", g0)
v.assert_true("Ex 3: geometric gain equals direct gain",
              abs(abs(e - 1) * abs(e + 1) / (abs(e - 0.99 * e) * abs(e - 0.99 * np.conj(e))) - g0) < 1e-9)
pk, wpk = find_peak(br, ar, 0.5, 1.1)
v.assert_true("Ex 3: peak equals the gain at w0 to 4 significant figures", abs(pk / g0 - 1) < 5e-5)
v.check("Txt 16-02.e", wpk)
lo, hi = band_edges(br, ar, wpk, pk / math.sqrt(2), 0.5, 1.1)
v.check("Ex 16-02.3d", hi - lo)
v.check("Ex 16-02.3e", wpk / (hi - lo))
v.check("Ex 16-02.3f", (math.pi / 4) / (2 * 0.01))

# ---------------------------------------------------------------------------------------- Example 4
hmin, hmax = [1, -0.5], [-0.5, 1]
v.assert_true("Ex 4: equal magnitudes", np.allclose(np.abs(pz.freq_resp(hmin, [1], wt)), np.abs(pz.freq_resp(hmax, [1], wt))))
v.check("Ex 16-02.4i", abs(H(hmin, [1], 0)))
v.check("Ex 16-02.4j", abs(H(hmin, [1], math.pi)))
v.check("Ex 16-02.4a", pz.partial_energy(hmin)[0] / pz.partial_energy(hmin)[-1])
v.check("Ex 16-02.4b", pz.partial_energy(hmax)[0] / pz.partial_energy(hmax)[-1])
gmin = pz.group_delay(hmin, [1], [0.0, math.pi])
gmax = pz.group_delay(hmax, [1], [0.0, math.pi])
v.check("Ex 16-02.4c", gmin[0])
v.check("Ex 16-02.4d", gmin[1])
v.check("Ex 16-02.4e", gmax[0])
v.check("Ex 16-02.4f", gmax[1])
bap, aap = pz.allpass1(0.5)
gap = pz.group_delay(bap, aap, [0.0, math.pi])
v.check("Ex 16-02.4g", gap[0])
v.check("Ex 16-02.4h", gap[1])
v.assert_true("Ex 4: H_max = H_min * H_ap", np.allclose(pz.freq_resp(hmax, [1], wt), pz.freq_resp(hmin, [1], wt) * pz.freq_resp(bap, aap, wt)))
v.assert_true("Ex 4: delays add", np.allclose(gmin + gap, gmax))
v.assert_true("Ex 4: all-pass has unit magnitude", np.allclose(np.abs(pz.freq_resp(bap, aap, wt)), 1))
v.assert_true("Ex 4: all-pass delay formula", np.allclose(pz.group_delay(bap, aap, wt), (1 - 0.25) / (1 - 2 * 0.5 * np.cos(wt) + 0.25)))

# ---------------------------------------------------------------------------------------- Example 5
v.check("Ex 16-02.5a", float(np.roots([0.8, 1.0])[0].real))
for K, key in ((5, "b"), (10, "c"), (20, "d")):
    eq = pz.anticausal_inverse(0.8, 1.0, K)
    tot = np.convolve([0.8, 1.0], eq)
    v.assert_true(f"Ex 5: main tap 1 at delay {K}", abs(tot[K] - 1) < 1e-12)
    v.assert_true(f"Ex 5: only one residual tap for K = {K}", np.allclose(np.delete(tot, [0, K]), 0, atol=1e-12))
    v.check(f"Ex 16-02.5{key}", abs(tot[0]))
Kmin = next(K for K in range(1, 100) if 0.8**K < 0.01)
v.check("Ex 16-02.5e", Kmin)
v.check("Ex 16-02.5f", int(np.argmax(np.abs(np.convolve([0.8, 1.0], pz.anticausal_inverse(0.8, 1.0, Kmin))))) - int(np.argmax([0.8, 1.0])))
v.assert_true("Ex 5: K = 1 gives the channel itself (residual 0.8)", abs(abs(np.convolve([0.8, 1.0], pz.anticausal_inverse(0.8, 1.0, 1))[0]) - 0.8) < 1e-12)
tot_m = np.convolve([1.0, 0.8], [(-0.8) ** k for k in range(Kmin)])
v.assert_true("Ex 5d: the minimum-phase mirror leaves the residual after the main tap", abs(tot_m[0] - 1) < 1e-12 and abs(abs(tot_m[Kmin]) - 0.8**Kmin) < 1e-12)

# ---------------------------------------------------------------------------------------- Concept checks
v.check("Txt 16-02.a", 0.01 * 8000 / math.pi)
v.check("Txt 16-02.b", -1 / math.log(0.99))
v.check("Txt 16-02.c", -1 / math.log(0.99) / 8000 * 1e3)
bq, aq = pz.allpass1(0.6)
v.check("Txt 16-02.d", pz.group_delay(bq, aq, 0.0)[0])
v.check("Txt 16-02.f", -1 / math.log(0.995))
v.check("Txt 16-02.g", -1 / math.log(0.9))
v.assert_true("Q1: poles at 0.9 e^{+-j pi/3} stable; zero response at 2 pi/3",
              abs(H(np.poly(np.exp(1j * np.array([2, -2]) * math.pi / 3)).real, np.poly(0.9 * np.exp(1j * np.array([1, -1]) * math.pi / 3)).real, 2 * math.pi / 3)) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 1
b, a = pz.dc_blocker(0.8)
v.check("16-02.1a", abs(H(b, a, 0)))
v.check("16-02.1b", abs(H(b, a, math.pi)))

# ---------------------------------------------------------------------------------------- Problem 2
b, a = [1, 0, -1], [1, 0, 0.81]
v.assert_true("P2: poles at +-j0.9", np.allclose(sorted(np.roots(a), key=lambda c: c.imag), [-0.9j, 0.9j]))
v.check("16-02.2a", abs(H(b, a, math.pi / 2)))
v.check("16-02.2b", abs(H(b, a, 0)))

# ---------------------------------------------------------------------------------------- Problem 3
A, B = 1 / (1 - 2 / 0.5), 1 / (1 - 0.5 / 2)
n = np.arange(-200, 201)
h3 = np.where(n >= 0, A * 0.5 ** np.maximum(n, 0), 0.0) + np.where(n <= -1, -B * 2.0 ** np.minimum(n, 0), 0.0)
for zt in (0.9 * np.exp(0.4j), 1.0 * np.exp(1.3j), 1.5 * np.exp(-0.7j)):   # points inside the ROC 0.5 < |z| < 2
    Hz = np.sum(h3 * zt ** (-n.astype(float)))
    v.assert_true(f"P3: series equals H(z) at |z| = {abs(zt):.1f}", abs(Hz - 1 / ((1 - 0.5 / zt) * (1 - 2 / zt))) < 1e-9)
v.check("16-02.3a", h3[n == 0][0])
v.check("16-02.3b", h3[n == -1][0])

# ---------------------------------------------------------------------------------------- Problem 4
fs4 = 48000.0


def f3(a):
    bb, aa = pz.dc_blocker(a)
    hf = 2 / (1 + a)
    return brentq(lambda w: abs(H(bb, aa, w)) - hf / math.sqrt(2), 1e-7, 1.0, xtol=1e-15) * fs4 / (2 * math.pi)


a_est = 1 - 2 * math.pi * 20 / fs4
v.check("16-02.4a", a_est)
v.check("16-02.4b", f3(a_est))
v.check("16-02.4c", brentq(lambda a: f3(a) - 20, 0.99, 0.99999, xtol=1e-14))

# ---------------------------------------------------------------------------------------- Problem 5
r5 = 1 - (2 * math.pi * 2 / 1000) / 2
w5 = 2 * math.pi * 60 / 1000
b5, a5 = pz.notch(w5, r5)
v.check("16-02.5a", r5)
v.check("16-02.5b", -a5[1])
v.check("16-02.5c", a5[2])
v.check("16-02.5d", b5[0])
v.assert_true("P5: symmetric numerator", abs(b5[0] - b5[2]) < 1e-15)
v.check("16-02.5e", -b5[1])
lo, hi = band_edges(b5, a5, w5, 1 / math.sqrt(2), 0.2, 0.6)
v.check("16-02.5f", (hi - lo) * 1000 / (2 * math.pi))
v.check("16-02.5g", -1 / math.log(r5))

# ---------------------------------------------------------------------------------------- Problem 6
b6, a6 = pz.resonator(math.pi / 3, 0.95)
v.check("16-02.6a", (math.pi / 3) / (2 * 0.05))
v.check("16-02.6b", abs(H(b6, a6, math.pi / 3)))
pk6, wpk6 = find_peak(b6, a6, 0.6, 1.5)
v.check("16-02.6c", pk6)
v.check("16-02.6d", wpk6)
lo, hi = band_edges(b6, a6, wpk6, pk6 / math.sqrt(2), 0.6, 1.5)
v.check("16-02.6e", hi - lo)
v.check("16-02.6f", wpk6 / (hi - lo))
e6 = np.exp(1j * math.pi / 3)
v.assert_true("P6: far-pole distance 1.6889 and zero product 2 sin(pi/3)",
              abs(abs(e6 - 0.95 * np.conj(e6)) - 1.6889) < 5e-5 and abs(abs(e6 - 1) * abs(e6 + 1) - 2 * math.sin(math.pi / 3)) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 7
g7 = pz.group_delay([1], [1, -0.9], [0.0, math.pi])
v.check("16-02.7a", g7[0])
v.check("16-02.7b", g7[1])

# ---------------------------------------------------------------------------------------- Problem 8
h8 = [1, -2.5, 1]
v.check("16-02.8a", float(np.mean(pz.group_delay(h8, [1], wt))))
v.assert_true("P8: constant group delay (away from the sign flips)", np.allclose(pz.group_delay_numeric(h8, [1], np.array([0.3, 1.0, 2.0])), 1, atol=1e-6))
v.assert_true("P8: zeros 2 and 0.5", np.allclose(sorted(np.roots(h8).real), [0.5, 2]))
v.check("16-02.8b", abs(H(h8, [1], 0)))
v.check("16-02.8c", abs(H(h8, [1], math.pi)))

# ---------------------------------------------------------------------------------------- Problem 9
hm = pz.minimum_phase_fir(h8)
v.assert_true("P9: minimum-phase FIR is (2, -2, 0.5)", np.allclose(hm, [2, -2, 0.5]))
hM = hm[::-1]
for hh, key in ((hm, "a"), (h8, "b"), (hM, "c")):
    v.assert_true(f"P9: same magnitude ({key})", np.allclose(np.abs(pz.freq_resp(hh, [1], wt)), np.abs(pz.freq_resp(h8, [1], wt))))
    pe = pz.partial_energy(hh)
    v.check(f"16-02.9{key}", pe[0] / pe[-1])
v.check("16-02.9d", pz.group_delay(hm, [1], 0.0)[0])
v.check("16-02.9e", pz.group_delay(hM, [1], 0.0)[0])
v.assert_true("P9: partial energy ordered min >= lin >= max at every n",
              all(pz.partial_energy(hm)[k] >= pz.partial_energy(h8)[k] - 1e-12 >= pz.partial_energy(hM)[k] - 2e-12 for k in range(3)))

# ---------------------------------------------------------------------------------------- Problem 10
a10 = brentq(lambda a: pz.group_delay(*pz.allpass1(a), 0.0)[0] - 0.5, -0.9, 0.9, xtol=1e-15)
v.check("16-02.10a", a10)
b10, a10c = pz.allpass1(a10)
v.check("16-02.10b", pz.group_delay(b10, a10c, math.pi)[0])
ph = math.degrees(np.angle(H(b10, a10c, math.pi / 4)))
v.check("16-02.10c", ph)
v.check("16-02.10d", ph - (-0.5 * 45))

# ---------------------------------------------------------------------------------------- Problem 11
v.assert_true("P11: zero at -1/0.6 outside the circle", abs(np.roots([0.6, 1.0])[0]) > 1)
v.check("16-02.11a", abs(np.convolve([0.6, 1.0], pz.anticausal_inverse(0.6, 1.0, 10))[0]))
K11 = next(K for K in range(1, 100) if 0.6**K < 0.01)
v.check("16-02.11b", K11)
v.check("16-02.11c", int(np.argmax(np.abs(np.convolve([0.6, 1.0], pz.anticausal_inverse(0.6, 1.0, K11))))) - 1)
tot11 = np.convolve([1.0, 0.6], [(-0.6) ** k for k in range(10)])
v.assert_true("P11c: mirror channel, residual 0.6^10 after the main tap, no delay", abs(tot11[0] - 1) < 1e-12 and abs(abs(tot11[10]) - 0.6**10) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 12
b12, a12 = [1, -3], [1, -0.5]
bmin, amin = [3, -1], [1, -0.5]
bap12, aap12 = pz.allpass1(1 / 3)
v.assert_true("P12: H = H_min * (-H_ap)", np.allclose(pz.freq_resp(b12, a12, wt), -pz.freq_resp(bmin, amin, wt) * pz.freq_resp(bap12, aap12, wt)))
gA, gM, gH = (pz.group_delay(b_, a_, [0.0, math.pi]) for b_, a_ in ((bap12, aap12), (bmin, amin), (b12, a12)))
v.check("16-02.12a", gA[0])
v.check("16-02.12b", gA[1])
v.check("16-02.12c", gM[0])
v.check("16-02.12d", gM[1])
v.check("16-02.12e", gH[0])
v.check("16-02.12f", gH[1])
v.assert_true("P12: delays add", np.allclose(gA + gM, gH))

# ---------------------------------------------------------------------------------------- Lab
bn, an = pz.notch(2 * math.pi * 50 / 1000, 0.9)
v.check("Lab 16-02.a", abs(H(bn, an, 2 * math.pi * 10 / 1000)))
w50 = 2 * math.pi * 50 / 1000
bn, an = pz.notch(w50, 0.995)
lo, hi = band_edges(bn, an, w50, 1 / math.sqrt(2), 0.2, 0.5)
v.check("Lab 16-02.b", (hi - lo) * 1000 / (2 * math.pi))
v.check("Lab 16-02.c", -1 / math.log(0.995))   # samples at 1 kHz = ms
v.check("Lab 16-02.d", 0.8**21)
v.check("Lab 16-02.e", 1 - 0.8**5)
v.check("Lab 16-02.f", math.sqrt(np.sum(pz.anticausal_inverse(0.8, 1.0, 21) ** 2)))
v.assert_true("Lab: noise gain tends to 1/sqrt(1 - 0.64)", abs(math.sqrt(np.sum(pz.anticausal_inverse(0.8, 1.0, 60) ** 2)) - 1 / math.sqrt(0.36)) < 1e-6)
rng = np.random.default_rng(42)
Ns = 200_000
sym = rng.choice([-1.0, 1.0], Ns)
nz = rng.normal(size=Ns)
for sigma, key in ((0.1, "g"), (0.3, "h")):
    rx = np.convolve(sym, [0.8, 1.0])[:Ns] + sigma * nz
    v.check(f"Lab 16-02.{key}", 100 * np.mean(np.sign(rx[1:]) != sym[:-1]))
rx = np.convolve(sym, [0.8, 1.0])[:Ns] + 0.3 * nz
for K, key in ((5, "i"), (10, "j"), (21, "k")):
    y = np.convolve(rx, pz.anticausal_inverse(0.8, 1.0, K))[:Ns]
    v.check(f"Lab 16-02.{key}", 100 * np.mean(np.sign(y[K:]) != sym[:Ns - K]))

# Figure 1 caption and §9: the 20-point moving average at 1 kHz is 3 dB down near 22 Hz
from scipy.optimize import brentq as _brentq  # noqa: E402
_ma = lambda f: abs(np.sum(np.exp(-2j * np.pi * f / 1000 * np.arange(20)))) / 20 - 2 ** -0.5  # noqa: E731
v.assert_true("20-point moving average -3 dB near 22 Hz", abs(_brentq(_ma, 1, 40) - 22.1) < 0.5)

# Problem 13: group delay of the r = 0.98 notch, by scipy on the transfer function
from scipy import signal as _sig  # noqa: E402
_w0 = 0.1 * np.pi
_b13, _a13 = [1, -2 * np.cos(_w0), 1], [1, -2 * 0.98 * np.cos(_w0), 0.98**2]
v.check("16-02.13a", _sig.group_delay((_b13, [1.0]), w=[0.05])[1][0])
v.check("16-02.13b", _sig.group_delay(([1.0], _a13), w=[_w0])[1][0])
v.check("16-02.13c", _sig.group_delay((_b13, _a13), w=[1e-7])[1][0])
v.check("16-02.13d", _sig.group_delay((_b13, _a13), w=[0.3])[1][0])

sys.exit(v.finish())
