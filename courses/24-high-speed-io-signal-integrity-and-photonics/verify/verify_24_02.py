#!/usr/bin/env python3
"""Verify every number in chapter 24-02 (eye diagrams, jitter and BER), its problems and its lab.

Independent routes (the lab module eye.py uses erfcinv, grid convolution and a time-stepped loop):
- Q and its inverse from scipy.stats.norm and root-finding on the tail;
- the two-pole pulse peak from its closed form t = UI/(1 - exp(-UI/tau)), checked against p'(t) = 0;
- statistical BERs by exact enumeration of ISI patterns (itertools and the binomial distribution);
- sinusoidal-jitter tails by quadrature over the sinusoid's phase;
- zero-error and one-error test lengths from the chi-square quantiles of the Poisson bound;
- phase-noise jitter by numerical integration of the phase-noise density.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-02", ROOT / "chapters" / "24-02-eye-diagrams-jitter-ber.md",
                        ROOT / "solutions" / "24-02-solutions.md", LAB / "README.md")


def Q(x):
    return stats.norm.sf(x)


def Qi(p):
    """Inverse tail by root-finding on norm.sf (independent of erfcinv)."""
    return optimize.brentq(lambda x: stats.norm.logsf(x) - math.log(p), 0, 40, xtol=1e-14)


# ---------------------------------------------------------------- two-pole channel
def step2(t, tau):
    return 0.0 if t <= 0 else 1 - (1 + t / tau) * math.exp(-t / tau)


def pulse2(t, tau):
    return step2(t, tau) - step2(t - 1, tau)


def peak2(tau):
    t = 1 / (1 - math.exp(-1 / tau))
    # p'(t) = s'(t) - s'(t-1), with s'(t) = t exp(-t/tau)/tau^2
    resid = t * math.exp(-t / tau) - (t - 1) * math.exp(-(t - 1) / tau)
    v.assert_true(f"pulse peak is a stationary point (tau={tau})", abs(resid) < 1e-12)
    return t


def cursors2(tau, phase=None):
    tp = peak2(tau) if phase is None else phase
    return tp, {k: pulse2(tp + k, tau) for k in range(-1, 9)}


def isi_sum(h):
    return sum(abs(x) for k, x in h.items() if k != 0)


# ================================================================ chapter
for b, a, b1 in ((1e-6, "1a", "1a1"), (1e-9, "1b", "1b1"), (1e-12, "1c", "1c1"), (1e-15, "1d", "1d1")):
    v.check(f"Ex 24-02.{a}", Qi(b))
    v.check(f"Ex 24-02.{b1}", 2 * Qi(b))
v.check("Ex 24-02.1e", 2 * Qi(2e-12))
v.check("Ex 24-02.1f", 2 * Qi(5e-13))
q6, q9, q12, q15 = Qi(1e-6), Qi(1e-9), Qi(1e-12), Qi(1e-15)

tp, h = cursors2(0.4)
v.check("Ex 24-02.2a", tp)
v.check("Ex 24-02.2b", h[-1])
v.check("Ex 24-02.2b1", h[0])
v.check("Ex 24-02.2b2", h[1])
v.check("Ex 24-02.2b3", h[2])
v.check("Ex 24-02.2b4", h[3])
isi = isi_sum(h)
v.check("Ex 24-02.2c", isi)
nrz = h[0] - isi
v.check("Ex 24-02.2d", nrz)
v.check("Ex 24-02.2d1", nrz)
v.check("Ex 24-02.2e", h[0] / 3 - isi)
_, h2p = cursors2(0.2)
isi2 = isi_sum(h2p)
v.check("Ex 24-02.2f0", h2p[0])
v.check("Ex 24-02.2f1", isi2)
pam = h2p[0] / 3 - isi2
v.check("Ex 24-02.2f", pam)
v.check("Ex 24-02.2f2", pam)

eye_mv = nrz * 400
half = eye_mv / 2
v.check("Ex 24-02.3a", eye_mv)
v.check("Ex 24-02.3a1", half)
v.check("Ex 24-02.3a2", half / q12)
v.check("Ex 24-02.3b0", half / 8)
ber_nrz = Q(half / 8)
v.check("Ex 24-02.3b", ber_nrz)
pam_mv = pam * 400
v.check("Ex 24-02.3c", pam_mv)
v.check("Ex 24-02.3c0", pam_mv / 2)
ser = 1.5 * Q(pam_mv / 2 / 8)
v.check("Ex 24-02.3c1", ser)
v.check("Ex 24-02.3c2", ser / 2)
v.check("Ex 24-02.3d", 100 * (1 - (pam_mv / 2) / half))
v.check("Ex 24-02.3e", math.log10((ser / 2) / ber_nrz))

UI32 = 31.25
tj12 = 2 * q12 * 0.4 + 3.0
tj15 = 2 * q15 * 0.4 + 3.0
v.check("Ex 24-02.4a", tj12)
v.check("Ex 24-02.4a1", tj12)
v.check("Ex 24-02.4b", UI32 - tj12)
v.check("Ex 24-02.4b1", 1 - tj12 / UI32)
v.check("Ex 24-02.4c", tj15)
tjd = 2 * q12 * 0.8 + 3.0
v.check("Ex 24-02.4d", tjd)
v.check("Ex 24-02.4e", tj15 - tj12)
v.check("Ex 24-02.4f", tjd - tj12)

# Ex 5: least squares through two points on the Q scale
A = np.array([[q6, 1.0], [q9, 1.0]])
sig5, dj2 = np.linalg.solve(A, [3.40, 3.90])
v.check("Ex 24-02.5a", sig5)
v.check("Ex 24-02.5a1", sig5)
v.check("Ex 24-02.5b0", dj2)
v.check("Ex 24-02.5b", 2 * dj2)
x12 = dj2 + q12 * sig5
v.check("Ex 24-02.5c", x12)
v.check("Ex 24-02.5c1", x12)
v.check("Ex 24-02.5d", UI32 - 2 * x12)
v.assert_true("Ex 5 bathtub point lies at 1e-12", abs(Q((x12 - dj2) / sig5) / 1e-12 - 1) < 1e-9)

rj6 = float(np.linalg.norm([0.15, 0.25, 0.20]))
tj6 = 2 * q12 * rj6 + 6.5
v.check("Ex 24-02.6a", rj6)
v.check("Ex 24-02.6a1", rj6)
v.check("Ex 24-02.6b", 1.0 + 4.0 + 1.5)
v.check("Ex 24-02.6c", tj6)
v.check("Ex 24-02.6d", tj6 / UI32)


def jtol(f, fc, m):
    # amplitude at which |1 - H| * A = m, with H = 1/(1 + j f/fc)
    return m / abs(1 - 1 / (1 + 1j * f / fc))


v.check("Ex 24-02.7a", 106.25e9 / 26562.5 / 1e6)
v.check("Ex 24-02.7b", jtol(1e5, 4e6, 0.3))
v.check("Ex 24-02.7c", jtol(4e6, 4e6, 0.3))
v.check("Ex 24-02.7d", jtol(4e7, 4e6, 0.3))

n95 = stats.chi2.ppf(0.95, 2) / 2 / 1e-12
v.check("Ex 24-02.8a", n95)
v.check("Ex 24-02.8a1", n95 / 32e9)
v.check("Ex 24-02.8b", n95 * 1000 / 32e9 / 3600)
v.check("Ex 24-02.8c", 0.1 / 31.25)
v.check("Ex 24-02.8d", 0.067 / 15.625)


def pn_jitter(l_dbc, f1, f2, f0):
    val, _ = integrate.quad(lambda f: 2 * 10 ** (l_dbc / 10), f1, f2)
    return math.sqrt(val) / (2 * math.pi * f0)


pn = pn_jitter(-150, 1e4, 2e7, 1e8) * 1e15
v.check("Ex 24-02.8e", pn)
v.check("Ex 24-02.8f", pn / 67)

# text values
v.check("Txt 24-02.a", q12)
v.check("Txt 24-02.b", q6)
v.check("Txt 24-02.c", 2.0 ** -10)
v.check("Txt 24-02.d", (1 / math.log2(4)) * 2 * (1 - 1 / 4))
v.check("Txt 24-02.e", h[0])
v.check("Txt 24-02.f", h[1])
v.check("Txt 24-02.g", h[-1])
v.check("Txt 24-02.h", q12 / q6)
v.check("Txt 24-02.i", 0.67e-5 + 2e-5)
ui_by_gen = {"1.1": (86, 400), "2.1": (3.1, 200), "3.1": (1.0, 125), "4.0": (0.5, 62.5),
             "5.0": (0.15, 31.25), "6.0": (0.1, 31.25), "7.0": (0.067, 15.625)}
frac = {g: a / b for g, (a, b) in ui_by_gen.items()}
v.check("Txt 24-02.j", frac["1.1"])
later = [frac[g] for g in ("3.1", "4.0", "5.0", "6.0", "7.0")]
v.check("Txt 24-02.k", min(later))
v.check("Txt 24-02.l", max(later))
v.check("Txt 24-02.m", 20 * math.log10(q12 / q6))
v.check("Txt 24-02.n", n95 / 32e9)
v.check("Txt 24-02.o", q9)
v.check("Txt 24-02.p", q15)

# ================================================================ solutions
for b, a, a1 in ((1e-4, "1a", "1a1"), (1e-10, "1b", "1b1"), (1e-14, "1c", "1c1")):
    v.check(f"24-02.{a}", Qi(b))
    v.check(f"24-02.{a1}", 2 * Qi(b))


# P3: single pole, tau = 0.5 UI, by direct evaluation of the pulse
def p1(t, tau=0.5):
    s = lambda x: 0.0 if x <= 0 else 1 - math.exp(-x / tau)  # noqa: E731
    return s(t) - s(t - 1)


tt = np.linspace(0.5, 1.5, 200001)
tpk1 = tt[np.argmax([p1(x) for x in tt])]
v.assert_true("P3 single-pole pulse peaks at 1 UI", abs(tpk1 - 1) < 1e-4)
c3 = [p1(1 + k) for k in range(0, 40)]
v.check("24-02.3b", c3[0])
v.check("24-02.3b1", c3[1])
v.check("24-02.3b2", c3[2])
isi3 = sum(c3[1:])
v.check("24-02.3c", isi3)
v.check("24-02.3d", c3[0] - isi3)
v.check("24-02.3d1", c3[0] / 3 - isi3)
v.check("24-02.3e", 100 * (1 - (c3[0] - isi3)))
v.assert_true("P3 NRZ eye loss is 2e^-2 of the swing", abs((1 - (c3[0] - isi3)) - 2 * math.exp(-2)) < 1e-12)
v.check("24-02.3e1", 100 * (c3[0] / 3 - isi3))

h4 = {-1: 0.05, 0: 0.60, 1: 0.25, 2: 0.05}
v.check("24-02.4a", h4[0] - isi_sum(h4))
v.check("24-02.4a1", h4[0] / 3 - isi_sum(h4))
h4d = {k: x for k, x in h4.items() if k != 1}
v.check("24-02.4b", h4d[0] - isi_sum(h4d))
v.check("24-02.4b1", h4d[0] / 3 - isi_sum(h4d))

v.check("24-02.5a", Q(30 / 4))
s12, s15 = 30 / q12, 30 / q15
v.check("24-02.5b", s12)
v.check("24-02.5c", s15)
v.check("24-02.5d", 100 * (1 - s15 / s12))

v.check("24-02.6a0", 20 / 3)
v.check("24-02.6a", 1.5 * Q(20 / 3))
v.check("24-02.6a1", 0.75 * Q(20 / 3))
v.check("24-02.6b", Q(60 / 3))
v.check("24-02.6c", 20 * math.log10(120 / 40))
v.check("24-02.6c1", 20 * math.log10(3))

ui53 = 1e12 / 53.125e9
v.check("24-02.7a0", ui53)
for b, a in ((1e-12, "7a"), (1e-15, "7b")):
    tj = 2 * Qi(b) * 0.25 + 2.0
    v.check(f"24-02.{a}", tj)
    v.check(f"24-02.{a}1", ui53 - tj)
    v.check(f"24-02.{a}2", (ui53 - tj) / ui53)

q5, q8 = Qi(1e-5), Qi(1e-8)
v.check("24-02.8a0", q5)
v.check("24-02.8a00", q8)
s8, d8 = np.linalg.solve(np.array([[q5, 1.0], [q8, 1.0]]), [2.10, 2.55])
v.check("24-02.8a", s8)
v.check("24-02.8a1", s8)
v.check("24-02.8a2", d8)
v.check("24-02.8a3", 2 * d8)
w8 = d8 + q12 * s8
v.check("24-02.8b", w8)
v.check("24-02.8b1", w8)
v.check("24-02.8c", ui53 - 2 * w8)
v.check("24-02.8c1", (ui53 - 2 * w8) / ui53)

tjmax = 0.40 * ui53
dj9 = 0.8 + 2.0 + 0.7
rjmax = (tjmax - dj9) / (2 * q12)
v.check("24-02.9a", tjmax)
v.check("24-02.9a1", dj9)
v.check("24-02.9b0", tjmax - dj9)
v.check("24-02.9b", rjmax)
v.check("24-02.9b1", rjmax)
v.check("24-02.9c", math.sqrt(rjmax ** 2 - 0.15 ** 2 - 0.12 ** 2))

rate = 106.25e9
lam0_95 = stats.chi2.ppf(0.95, 2) / 2
lam0_99 = stats.chi2.ppf(0.99, 2) / 2
lam1_95 = stats.chi2.ppf(0.95, 4) / 2
v.assert_true("one-error Poisson bound", abs(stats.poisson.cdf(1, lam1_95) - 0.05) < 1e-12)
v.check("24-02.10a0", lam0_95)
v.check("24-02.10a", lam0_95 / 1e-12)
v.check("24-02.10a1", lam0_95 / 1e-12 / rate)
v.check("24-02.10b0", lam0_99)
v.check("24-02.10b", lam0_99 / 1e-12)
v.check("24-02.10b1", lam0_99 / 1e-12 / rate)
v.check("24-02.10c", lam1_95)
v.check("24-02.10c1", lam1_95 / 1e-12)
v.check("24-02.10c2", lam1_95 / 1e-12 / rate)
v.check("24-02.10d", 100 * (lam1_95 / lam0_95 - 1))

fc11 = 53.125e9 / 26562.5
v.check("24-02.11a", fc11 / 1e6)
v.check("24-02.11b", jtol(1e5, fc11, 0.25))
v.check("24-02.11c0", math.sqrt(15))
f1ui = optimize.brentq(lambda f: jtol(f, fc11, 0.25) - 1.0, 1e3, 1e8)
v.check("24-02.11c", f1ui / 1e3)
te200 = abs(1 - 1 / (1 + 1j * 2e5 / fc11))
te_c = abs(1 - 1 / (1 + 1j))
v.check("24-02.11d", te200)
v.check("24-02.11d1", te_c)
v.check("24-02.11e", 100 * (1 - te200))
v.check("24-02.11e1", 100 * (1 - te_c))


# P12: exact enumeration of patterns
def ber_patterns(h0, taps, sigma):
    tot = 0.0
    for signs in itertools.product((1, -1), repeat=len(taps)):
        tot += Q((h0 + sum(s * t for s, t in zip(signs, taps))) / sigma)
    return tot / 2 ** len(taps)


b12 = ber_patterns(0.7, [0.2, 0.1], 0.05)
bnd = Q(0.4 / 0.05)
v.check("24-02.12a", b12)
v.check("24-02.12a1", bnd)
v.check("24-02.12a2", bnd / b12)
sw = 0.4 / q12
sx = optimize.brentq(lambda s: math.log(ber_patterns(0.7, [0.2, 0.1], s)) + 12 * math.log(10), 0.02, 0.2,
                     xtol=1e-12)
v.check("24-02.12b", sw)
v.check("24-02.12b1", sx)
v.check("24-02.12b2", 100 * (sx / sw - 1))
j = np.arange(21)
w20 = stats.binom.pmf(j, 20, 0.5)
marg = 0.7 - 0.015 * (20 - 2 * j)


def ber20(s):
    return float(np.sum(w20 * Q(marg / s)))


v.check("24-02.12c", ber20(0.05))
s20 = optimize.brentq(lambda s: math.log(ber20(s)) + 12 * math.log(10), 0.02, 0.2, xtol=1e-12)
v.check("24-02.12c1", s20)
v.check("24-02.12c2", 100 * (s20 / sw - 1))

j13 = pn_jitter(-140, 1.2e4, 2e7, 1e8)
v.check("24-02.13a", j13 * 1e12)
v.check("24-02.13b", j13 * 1e12 / 0.15)
v.check("24-02.13c1", j13 * 1e12 / 0.15)
v.check("24-02.13c0", 20 * math.log10(j13 * 1e12 / 0.15))
lreq = optimize.brentq(lambda L: pn_jitter(L, 1.2e4, 2e7, 1e8) - 0.15e-12, -180, -120)
v.check("24-02.13c", lreq)

a14, b14 = Qi(1e-12 / 0.75), Qi(1e-6 / 0.75)
v.check("24-02.14a", a14)
v.check("24-02.14b", b14)
v.check("24-02.14c", 20 * math.log10(a14 / b14))
v.check("24-02.14c1", 20 * math.log10(a14 / b14))
v.check("24-02.14d", lam0_95 / 1e-6)
v.check("24-02.14d1", lam0_95 / 1e-6 / 128e9 * 1e6)

com = 20 * math.log10(30 / 20)
v.check("24-02.15a", com)
v.assert_true("P15 passes 3 dB", com >= 3)
v.check("24-02.15b", com - 3)
v.check("24-02.15c", 30 / 10 ** (3 / 20))
v.check("24-02.15c1", 100 * (30 / 10 ** (3 / 20) / 20 - 1))

# ================================================================ lab
v.check("Lab 24-02.a", h[0])
v.check("Lab 24-02.b", h[1])

# statistical eye by pattern enumeration over h_-1 .. h_8 (the remainder is below 1e-7)
taps = [h[k] for k in sorted(h) if k != 0]
sig_lab = 8 / 200
levels = np.array([h[0] + sum(s * t for s, t in zip(signs, taps))
                   for signs in itertools.product((1, -1), repeat=len(taps))])


def cond_err(vth):
    # probability that a 1 falls below vth
    return float(np.mean(stats.norm.cdf((vth - levels) / sig_lab)))


v1 = optimize.brentq(lambda x: math.log(cond_err(x)) + 12 * math.log(10), 0.0, h[0], xtol=1e-12)
stat_h = 2 * v1 * 200
worst_h = (2 * (h[0] - isi_sum(h)) - 2 * q12 * sig_lab) * 200
v.check("Lab 24-02.c", stat_h)
v.check("Lab 24-02.d", worst_h)
v.check("Txt 24-02.q", stat_h)
v.check("Txt 24-02.r", worst_h)
ber_c = cond_err(0.0)
v.check("Lab 24-02.e", ber_c)
v.check("Lab 24-02.l", 100 * (stat_h / worst_h - 1))
v.check("Lab 24-02.m", Q((h[0] - isi_sum(h)) / sig_lab) / ber_c)
v.check("Lab 24-02.n", 100 * h[1] / isi_sum(h))


def sj_tail(x, pp=3.0, rj=0.4):
    val, _ = integrate.quad(lambda th: Q((x - 0.5 * pp * math.sin(th)) / rj), -math.pi / 2, math.pi / 2,
                            epsabs=0, epsrel=1e-11, limit=200)
    return val / math.pi


def wall(b):
    return optimize.brentq(lambda x: math.log(sj_tail(x)) - math.log(b), 0.0, 10.0, xtol=1e-12)


xa, xb, xc = wall(1e-6), wall(1e-9), wall(1e-12)
sA, dA = np.linalg.solve(np.array([[q9, 1.0], [q12, 1.0]]), [xb, xc])
sB, dB = np.linalg.solve(np.array([[q6, 1.0], [q9, 1.0]]), [xa, xb])
v.check("Lab 24-02.f", 2 * dA)
v.check("Lab 24-02.g", sA)
v.check("Lab 24-02.h", 2 * dB)
v.assert_true("fitted DJ(dd) below the 3 ps peak-to-peak", 2 * dA < 3.0 and 2 * dB < 3.0)

for key, f in (("Lab 24-02.i", 1e5), ("Lab 24-02.j", 4e6), ("Lab 24-02.k", 4e7)):
    v.check(key, abs(1 - 1 / (1 + 1j * f / 4e6)))

sys.exit(v.finish())
