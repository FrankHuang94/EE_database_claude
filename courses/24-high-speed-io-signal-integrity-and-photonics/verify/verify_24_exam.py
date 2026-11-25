#!/usr/bin/env python3
"""Verify every number in the Course 24 final-exam solutions.

About a third of the values are recomputed by a second route; the rest are closed-form re-evaluations:
- Question 3(a): the FFE taps by solving the zero-forcing linear system with the swing constraint;
- Question 7(c): MZM levels by summing the two arms' fields;
- Question 9(b): the grating steer by finite differences of the phase-matching angle;
- Questions 2(c), 9(d), 11(d) and 12(b): BERs by numerical integration of the noise density, convolving the
  segments' densities for linear chains;
- Question 3(c): the CTLE's gains and corner frequencies from H(s) evaluated numerically and root-found;
- Question 4(d): the net coding gain with Q^-1 found by root finding on the tail integral;
- Question 8(b): the TIA by nodal analysis at each frequency;
- Question 9(c): the driver-bond-modulator response from complex impedances, peak by minimization;
- Questions 10(c), 11(d) and 12(c): failure-rate bounds by root-finding the Poisson probability;
- Question 11(c): coupling by numerical quadrature of the overlap integral.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-exam", ROOT / "exam" / "solutions.md")
# The exam states its constants to four figures; its answers use those values.
C0, H, QE, KB = 2.998e8, 6.626e-34, 1.602e-19, 1.381e-23
YEAR = 8766.0


def db(x):
    return 10 * math.log10(x)


def tail(x):
    """Gaussian tail by direct integration of the density."""
    return integrate.quad(lambda t: math.exp(-t * t / 2) / math.sqrt(2 * math.pi), x, x + 40)[0]


def qinv(p):
    return optimize.brentq(lambda x: math.log(tail(x)) - math.log(p), 0.5, 12)


def linear_ber(qs):
    x = np.linspace(-3, 3, 60001)
    dx = x[1] - x[0]
    pdf = None
    for qi in qs:
        g = norm.pdf(x, scale=1 / qi)
        pdf = g if pdf is None else np.convolve(pdf, g, mode="same") * dx
    sel = x >= 1.0
    return float(integrate.trapezoid(pdf[sel], x[sel]))


def poisson_bound_fit(hours, failures=0):
    lam = optimize.brentq(lambda r: stats.poisson.cdf(failures, r * hours) - 0.05, 1e-15, 1e-3, xtol=1e-19)
    return lam * 1e9


def alpha_d(f, er, tand):
    return math.pi * f * math.sqrt(er) * tand / C0


# ---------------------------------------------------------------- Q1
v.check("X24.1a", 212.5 / 2)
v.check("X24.1a1", 1e12 / 106.25e9)
v.check("X24.1a2", 106.25 / 2)
ad = alpha_d(53.125e9, 3.4, 0.002)
v.check("X24.1b0", ad)
v.check("X24.1b", ad * 8.686 * 0.0254)
ac = 36 * math.sqrt(53.125) / (4 * 50)
v.check("X24.1b1", ac)
v.check("X24.1b2", ad * 8.686 * 0.0254 + ac)
v.check("X24.1b3", 8 * (ad * 8.686 * 0.0254 + ac))
stub = lambda ell: C0 / (4 * ell * math.sqrt(3.4))  # noqa: E731
v.check("X24.1c", stub(0.3e-3) / 1e9)
v.check("X24.1c1", stub(1.0e-3) / 1e9)
v.check("X24.1c2", optimize.brentq(lambda ell: stub(ell) - 2 * 53.125e9, 1e-5, 1e-2) * 1e3)
# S11 of a 92-ohm section's leading edge seen from a 100-ohm reference: (Z - Z0)/(Z + Z0) via the ABCD-free form
s11 = (92 / 100 - 1) / (92 / 100 + 1)
v.check("X24.1d", s11)
v.check("X24.1d1", -20 * math.log10(abs(s11)))
kb = 0.25 * (0.03 + 0.03)
v.check("X24.1e", kb)
v.check("X24.1e1", kb * 0.8 * 1e3)
v.check("X24.1e2", C0 / math.sqrt(3.4) * 15e-12 / 2 * 1e3)
v.check("X24.1e3", (0.03 - 0.03) * 0.8 * 1e3)

# ---------------------------------------------------------------- Q2
cur = {-1: 0.04, 0: 0.60, 1: 0.18, 2: 0.06, 3: 0.02}
isi = sum(abs(x) for k, x in cur.items() if k != 0)
v.check("X24.2a0", isi)
v.check("X24.2a", cur[0] - isi)
v.check("X24.2a1", cur[0] / 3 - isi)
v.check("X24.2b", cur[0] - cur[-1])
v.check("X24.2b1", cur[0] / 3 - cur[-1])
x2 = (cur[0] / 3 - cur[-1]) / (2 * 0.012)
v.check("X24.2c", x2)
v.check("X24.2c1", 0.75 * tail(x2))
ui = 1e12 / 106.25e9
tj = 2 * qinv(1e-12) * 0.15 + 1.2
v.check("X24.2d", tj)
v.check("X24.2d1", ui - tj)
v.check("X24.2d2", (ui - tj) / ui)
nbits = optimize.brentq(lambda n: stats.poisson.pmf(0, n * 1e-12) - 0.05, 1e11, 1e14)
v.check("X24.2d3", nbits)
v.check("X24.2d4", nbits / 212.5e9)

# ---------------------------------------------------------------- Q3
taps = np.linalg.solve(np.array([[0.20, 0.60], [1.0, -1.0]]), np.array([0.0, 1.0]))  # g1 = 0; c0 - c1 = 1 (c1 < 0)
v.check("X24.3a", taps[0])
v.check("X24.3a1", taps[1])
g = np.convolve(taps, [0.60, 0.20])
v.check("X24.3a2", g[0])
v.assert_true("first post-cursor cancelled", abs(g[1]) < 1e-12)
v.check("X24.3a3", g[2])
v.check("X24.3a4", 20 * math.log10(1 / taps.sum()))
v.check("X24.3b", 1.0 / 50 * 1e3)
v.check("X24.3b1", 0.9 * 1.0 / 50 * 1e3)
v.check("X24.3b2", 1.0 ** 2 / 200 * 1e3)
v.check("X24.3b3", (0.9 / 50) / (1.0 / 200))
gm, rs, cs, rd = 25e-3, 320.0, 250e-15, 200.0


def ctle(f):
    zs = (rs / 2) / (1 + 2j * math.pi * f * rs * cs)
    return abs(gm * rd / (1 + gm * zs))


h0, hinf = ctle(1.0), ctle(1e16)
v.check("X24.3c0", hinf / h0)
v.check("X24.3c", 20 * math.log10(hinf / h0))
# the zero and pole from the roots of H(s)'s numerator and denominator polynomials in s
zero = abs(np.roots([rs * cs, 1.0])[0]) / (2 * math.pi)
pole = abs(np.roots([rs * cs, 1 + gm * rs / 2])[0]) / (2 * math.pi)
v.assert_true("|H| at the zero is sqrt(2) above DC to first order", abs(ctle(zero) / h0 - math.sqrt(2) * abs(
    1 / (1 + 1j * zero / pole))) < 1e-9)
v.check("X24.3c1", zero / 1e9)
v.check("X24.3c2", pole / 1e9)
v.check("X24.3c3", h0)
v.check("X24.3c4", hinf)
v.check("X24.3d", 2e-4 * 106.25e9 / (2 * math.pi * 2e7))

# ---------------------------------------------------------------- Q4
snr = -20 * math.log10(2 * math.pi * 53.125e9 * 50e-15)
v.check("X24.4a", snr)
v.check("X24.4a0", snr)
v.check("X24.4a1", (snr - 1.76) / 6.02)
step = 3.0 / 2 ** 6
ramp = np.linspace(-0.5, 0.5, 200001) * step  # uniform rounding error over one step
sq = math.sqrt(np.mean(ramp ** 2))
v.check("X24.4b", step)
v.check("X24.4b1", sq)
v.check("X24.4b2", sq / (1 / 3))
v.check("X24.4c", db(1 + 0.7 ** 2))
v.check("X24.4d", 20 * math.log10(qinv(1e-15) / qinv(2.4e-4)) + db(514 / 544))
v.check("X24.4d1", 544 * 10 / 212.5e9 * 1e9)

# ---------------------------------------------------------------- Q5
b5 = 16 * 32e9 * (128 / 130) / 8
v.check("X24.5a", b5 / 1e9)
v.check("X24.5b", 100 * 128 / (128 + 24))
v.check("X24.5b1", b5 * 128 / 152 / 1e9)
v.check("X24.5c", b5 * 500e-9 / 1e3)
v.check("X24.5d", 200 * 257 / 256 * 544 / 514)
v.check("X24.5d1", 64 ** 2 / 2)
v.check("X24.5d2", 512 ** 2 / 2)

# ---------------------------------------------------------------- Q6
e6 = 150e-15 * 0.4 ** 2 / 4
v.check("X24.6a", e6 * 1e15)
v.check("X24.6a1", e6 * 32e9 * 1e3)
v.check("X24.6b", 0.4 ** 2 / (4 * 50 * 32e9) * 1e15)
bumps = (1 / 0.036) ** 2
v.check("X24.6c", bumps * 0.5 * 32 / 8)
v.check("X24.6c1", bumps * 0.5 * 32 / 8 / 1e3)
ctot = 50e-15 + 200e-15 + 50e-15
elm = 100 * ctot + 50 * (200e-15 / 2 + 50e-15)
v.check("X24.6d", ctot * 1e15)
v.check("X24.6d1", elm * 1e12)
v.check("X24.6d2", 100 * 100 * ctot / elm)

# ---------------------------------------------------------------- Q7
r7 = 0.85 * QE * 1310e-9 / (H * C0)
p7 = 1e-3 * 10 ** (-0.8)
v.check("X24.7a", r7)
v.check("X24.7a1", p7 * 1e6)
v.check("X24.7a2", r7 * p7 * 1e6)
dl = (1.31e-6) ** 2 * 106.25e9 / C0 * 1e9
v.check("X24.7b", dl)
v.check("X24.7b1", 3.5 * 2 * dl)
v.check("X24.7b2", 3.5 * 2 * dl / ui)
mz = lambda dphi: abs(0.5 * (np.exp(0.5j * dphi) + np.exp(-0.5j * dphi))) ** 2  # noqa: E731
hi, lo = mz(math.pi / 2 - 0.3 * math.pi), mz(math.pi / 2 + 0.3 * math.pi)
v.check("X24.7c", hi)
v.check("X24.7c1", lo)
v.check("X24.7c2", hi / lo)
v.check("X24.7c3", db(hi / lo))
v.check("X24.7c4", hi - lo)
sig = 18e-12 * math.sqrt(55e9)
pk = qinv(2.4e-4) * sig / 0.85
pen = db((10 ** 0.4 + 1) / (10 ** 0.4 - 1))
v.check("X24.7d", sig * 1e6)
v.check("X24.7d1", pk * 1e6)
v.check("X24.7d2", db(pk / 1e-3))
v.check("X24.7d3", pen)
p4 = db(pk / 1e-3) + db(3) + pen
v.check("X24.7d4", p4)
v.check("X24.7d5", db(pk / 1e-3))

# ---------------------------------------------------------------- Q8
rx = 3 - 2 * 0.36 - 2 * 0.5 - 2 * 1.8
v.check("X24.8a", rx)
v.check("X24.8a1", rx - p4)


def tia_mag(f, rf=600.0, a=12.0, cin=90e-15):
    y = np.array([[2j * math.pi * f * cin + 1 / rf, -1 / rf], [a, 1.0]])
    return abs(np.linalg.solve(y, np.array([1.0, 0.0]))[1])


z0 = tia_mag(1.0)
bw = optimize.brentq(lambda f: tia_mag(f) - z0 / math.sqrt(2), 1e8, 1e12, xtol=1e2)
v.check("X24.8b", z0)
v.check("X24.8b1", bw / 1e9)
nrf = math.sqrt(4 * KB * 300 / 600)
v.check("X24.8b2", nrf * 1e12)
v.check("X24.8b3", nrf * math.sqrt(bw) * 1e6)
v.check("X24.8c", (1.31e-6) ** 2 * 800e9 / C0 * 1e9)
v.check("X24.8c1", C0 * 4.5e-9 / (1.31e-6) ** 2 / 1e9)
sh = 1310 * 1.8e-4 / 3.9
v.check("X24.8d", sh)
v.check("X24.8d1", 1310 / 7500)
v.check("X24.8d2", 1310 / 7500 / sh)


# ---------------------------------------------------------------- Q9
def overlap(w1, w2, d=0.0):
    lim = 12 * max(w1, w2) + abs(d)
    ox = integrate.quad(lambda x: math.exp(-x ** 2 / w1 ** 2 - (x - d) ** 2 / w2 ** 2), -lim, lim)[0]
    oy = integrate.quad(lambda y: math.exp(-y ** 2 / w1 ** 2 - y ** 2 / w2 ** 2), -lim, lim)[0]
    n1 = integrate.quad(lambda x: math.exp(-2 * x ** 2 / w1 ** 2), -lim, lim)[0] ** 2
    n2 = integrate.quad(lambda x: math.exp(-2 * x ** 2 / w2 ** 2), -lim, lim)[0] ** 2
    return (ox * oy) ** 2 / (n1 * n2)


e9 = overlap(4.6, 2.5)
e9d = overlap(4.6, 2.5, 0.8) / e9
v.check("X24.9a", e9)
v.check("X24.9a1", db(e9))
v.check("X24.9a2", e9d)
v.check("X24.9a3", db(e9d))
v.check("X24.9a4", db(e9 * e9d))
v.check("X24.9a5", db(e9))
per = 1310 / (2.75 - math.sin(math.radians(12)))
ang = lambda lam: math.degrees(math.asin(2.75 - lam / per))  # noqa: E731
v.check("X24.9b", per)
v.check("X24.9b1", (ang(1309.99) - ang(1310.01)) / 0.02)
v.check("X24.9b2", 20 * (ang(1309.99) - ang(1310.01)) / 0.02)
rr, lb, cc = 50.0, 0.2e-9, 30e-15
mag = lambda f: abs(1 / (1 + (rr + 2j * math.pi * f * lb) * 2j * math.pi * f * cc))  # noqa: E731
res = optimize.minimize_scalar(lambda lf: -mag(10 ** lf), bounds=(10, 11.5), method="bounded",
                               options={"xatol": 1e-10})
v.check("X24.9c", 1 / (2 * math.pi * math.sqrt(lb * cc)) / 1e9)
v.check("X24.9c1", rr / 2 * math.sqrt(cc / lb))
v.check("X24.9c2", mag(10 ** res.x))
v.check("X24.9c3", 20 * math.log10(mag(10 ** res.x)))
v.check("X24.9c4", 10 ** res.x / 1e9)
v.check("X24.9c5", optimize.brentq(lambda f: mag(f) - 1 / math.sqrt(2), 10 ** res.x, 1e12) / 1e9)
b9 = linear_ber([8, 7, 8])
v.check("X24.9d", norm.isf(b9))
v.check("X24.9d1", b9)
v.check("X24.9d2", 2 * tail(8) + tail(7))

# ---------------------------------------------------------------- Q10
v.check("X24.10a", 4 / 800e9 * 1e12)
v.check("X24.10a1", 14 / 800e9 * 1e12)
v.check("X24.10a2", 100 * (1 - 4 / 14))
avail = 17 - 2 - 1 - 2.0
v.check("X24.10b", avail)
v.check("X24.10b1", 10 ** (avail / 10))
v.check("X24.10b2", 2 ** int(math.log2(10 ** (avail / 10))))
v.check("X24.10c", poisson_bound_fit(3e6))
v.check("X24.10c1", poisson_bound_fit(3e6, 1))
lost = lambda fit, n, t, units: fit * 1e-9 * YEAR * n * t / units  # noqa: E731
v.check("X24.10d", lost(300, 16, 8, 16) / lost(150, 1, 0.5, 1))

# ---------------------------------------------------------------- Q11
a11 = alpha_d(26.5625e9, 3.0, 0.0015)
v.check("X24.11a0", a11)
v.check("X24.11a", a11 * 8.686 * 0.0254)
gm2, rs2 = 30e-3, 300.0
hz = lambda f: abs(1 / (1 + gm2 * (rs2 / 2) / (1 + 2j * math.pi * f * rs2 * 1e-13)))  # noqa: E731
v.check("X24.11b", hz(1e18) / hz(1.0))
v.check("X24.11b1", 20 * math.log10(hz(1e18) / hz(1.0)))
e11 = overlap(4.6, 3.0)
v.check("X24.11c", e11)
v.check("X24.11c1", db(e11))
b11 = linear_ber([9, 7, 9])
v.check("X24.11d", norm.isf(b11))
v.check("X24.11d1", b11)
v.check("X24.11d2", poisson_bound_fit(5e6))

# ---------------------------------------------------------------- Q12
v.check("X24.12a", 8 / 1.6e12 * 1e12)
v.check("X24.12a1", 25 / 1.6e12 * 1e12)
v.check("X24.12a2", 4e5 * 25 / 1e6)
v.check("X24.12a3", 4e5 * 8 / 1e6)
v.check("X24.12a4", 4e5 * (25 - 8) / 1e6)
b12 = linear_ber([11, 6.5, 11])
q12 = norm.isf(b12)
v.check("X24.12b", q12)
v.check("X24.12b1", b12)
v.check("X24.12b2", 20 * math.log10(q12 / qinv(2.4e-4)))
v.check("X24.12b3", qinv(1e-12))
v.assert_true("the optical segment alone is worse than 1e-12", tail(6.5) > 1e-12)
v.check("X24.12c", poisson_bound_fit(2e6))
v.check("X24.12c1", 2e6 / YEAR)
v.check("X24.12c2", optimize.brentq(lambda t: poisson_bound_fit(t) - 100, 1e6, 1e9) / 1e6)

sys.exit(v.finish())
