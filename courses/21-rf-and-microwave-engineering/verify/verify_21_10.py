#!/usr/bin/env python3
"""Verify every number in chapter 21-10 (antennas, arrays, beamforming and mmWave), its problems and its lab.

Independent routes (the lab module antenna.py sums complex exponentials and uses closed forms):
- array factors use the closed form sin(N psi/2)/(N sin(psi/2)); beam directions under squint are found by
  maximizing the pattern numerically instead of from arcsin((f0/f) sin theta0);
- the squint bandwidth is found by root-finding on the gain toward theta0, not from 0.886/(N d sin theta0);
- small-antenna bandwidth is found by solving |Gamma(delta)| for a series RLC numerically, not from (s-1)/(Q sqrt s);
- the DC-optimal element count is found with a numerical minimizer;
- phase quantization is checked by a seeded Monte Carlo (different seed and implementation from the lab);
- the radar virtual array is built as a set of TX+RX position sums and its first null located numerically;
- ngspice confirms the squint and true-time-delay arrays separately (squint.cir via run_spice.py).
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("21-10", ROOT / "chapters" / "21-10-antennas-arrays-mmwave.md",
                        ROOT / "solutions" / "21-10-solutions.md", LAB / "README.md")
lg = math.log10
db10 = lambda x: 10 * lg(x)  # noqa: E731
db20 = lambda x: 20 * lg(x)  # noqa: E731
C = 299_792_458.0
rad, deg = math.radians, math.degrees


# ---------------------------------------------------------------- independent helpers
def patch(f0, er, h):
    w = C / (2 * f0) * (2 / (er + 1)) ** 0.5
    ee = 0.5 * (er + 1) + 0.5 * (er - 1) * (1 + 12 * h / w) ** -0.5
    dl = 0.412 * h * (ee + 0.3) * (w / h + 0.264) / ((ee - 0.258) * (w / h + 0.8))
    length = C / (2 * f0 * ee ** 0.5) - 2 * dl
    return w, ee, dl, length


def q_chu(ka):
    return ka ** -3 + ka ** -1


def bw_numeric(q, vswr):
    """Fractional bandwidth of Z = R(1 + j 2 Q delta) within the VSWR limit, by root-finding on |Gamma|."""
    gmax = (vswr - 1) / (vswr + 1)
    g = lambda d: abs((1j * 2 * q * d) / (2 + 1j * 2 * q * d)) - gmax  # noqa: E731
    return 2 * optimize.brentq(g, 1e-9, 1.0)


def af_closed(theta, n, d, theta0, fr=1.0, ttd=False):
    """Closed-form |AF| (spacing d in design wavelengths, evaluated at f = fr f0)."""
    s0 = math.sin(rad(theta0))
    psi = 2 * math.pi * d * (fr * math.sin(rad(theta)) - (fr if ttd else 1.0) * s0)
    if abs(math.sin(psi / 2)) < 1e-12:
        return 1.0
    return abs(math.sin(n * psi / 2) / (n * math.sin(psi / 2)))


def beam_peak(n, d, theta0, fr):
    res = optimize.minimize_scalar(lambda t: -af_closed(t, n, d, theta0, fr), bounds=(theta0 - 25, min(theta0 + 25, 89.9)),
                                   method="bounded", options={"xatol": 1e-9})
    return res.x


def hpbw(n, d, theta0):
    f = lambda t: af_closed(t, n, d, theta0) - 2 ** -0.5  # noqa: E731
    step = 0.886 / (n * d) * 180 / math.pi / math.cos(rad(theta0))
    lo = optimize.brentq(f, theta0 - 1.5 * step, theta0 - 1e-6)
    hi = optimize.brentq(f, theta0 + 1e-6, min(theta0 + 1.5 * step, 89.99))
    return hi - lo


def squint_bw(n, d, theta0):
    g = lambda fr: af_closed(theta0, n, d, theta0, fr) - 2 ** -0.5  # noqa: E731
    return optimize.brentq(g, 1.0 + 1e-9, 1.5) - optimize.brentq(g, 0.5, 1.0 - 1e-9)


def fspl(f, r):
    return db20(4 * math.pi * r * f / C)


def floor_dbm(bw, nf):
    return -174 + db10(bw) + nf


# ================================================================ chapter text
print("Text")
v.check("Txt 21-10.a", -db20(1 / 3))
v.check("Txt 21-10.b", -db10(0.5))
v.check("Txt 21-10.c", bw_numeric(1.0, 2.0))
v.check("Txt 21-10.d", -db10(math.cos(rad(45))))
v.check("Txt 21-10.e", -db10(math.cos(rad(60))))
x = 2.0
v.check("Txt 21-10.f", ((1 / x + x) / 2 - 1) * 100)
v.check("Txt 21-10.g", 400e6 / 28e9 * 100)
v.check("Txt 21-10.h", 22.4 - 11.5)
v.check("Txt 21-10.i", 20.6 - 8)
v.check("Txt 21-10.j", 10 ** (43 / 10) / 1000)
v.check("Txt 21-10.k", len([4, 8, 16, 20]) * len([0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18]))
v.check("Txt 21-10.l", db20(64))
v.check("Txt 21-10.m", 5 * 0.3)
v.check("Txt 21-10.n", 0.4215 * 25 ** 0.8743)
v.check("Txt 21-10.o", 0.8606 * 25 ** 0.7656)
v.check("Txt 21-10.p", 24 / 392 * 100)

print("Example 21-10.1")
w, ee, dl, L = patch(28e9, 3.0, 0.25e-3)
v.check("Ex 21-10.1a", w * 1e3)
v.check("Ex 21-10.1b", ee)
v.check("Ex 21-10.1c", dl * 1e3)
v.check("Ex 21-10.1d", L * 1e3)
v.check("Ex 21-10.1e", C / 28e9 / 2 * 1e3)
v.check("Ex 21-10.1f", C / 28e9 / 2 / 3 ** 0.5 * 1e3)
v.assert_true("patch resonates at 28 GHz with the fringing extension",
              abs(C / (2 * (L + 2 * dl) * ee ** 0.5) - 28e9) < 1)

print("Example 21-10.2")
lam = C / 2.44175e9
q10, q5 = q_chu(2 * math.pi * 0.010 / lam), q_chu(2 * math.pi * 0.005 / lam)
v.check("Ex 21-10.2a", 2 * math.pi * 0.010 / lam)
v.check("Ex 21-10.2b", q10)
v.check("Ex 21-10.2c", bw_numeric(q10, 2) * 100)
v.check("Ex 21-10.2d", 2 * math.pi * 0.005 / lam)
v.check("Ex 21-10.2e", q5)
v.check("Ex 21-10.2f", bw_numeric(q5, 2) * 100)
need = 83.5 / 2441.75
v.check("Ex 21-10.2g", need * 100)
qmax = optimize.brentq(lambda q: bw_numeric(q, 2) - need, 1, 1000)
v.check("Ex 21-10.2h", qmax)
v.check("Ex 21-10.2i", qmax / q5 * 100)
v.check("Ex 21-10.2j", db10(qmax / q5))
v.check("Ex 21-10.2k", q5 / q10)

print("Example 21-10.3")
tgt = 22.4 + 3
pe = tgt - 5 - db20(4)
v.check("Ex 21-10.3a", tgt)
v.check("Ex 21-10.3b", pe)
v.check("Ex 21-10.3c", pe + 5 * 0.3)
v.check("Ex 21-10.3d", db10(4 * 10 ** (pe / 10)))
v.check("Ex 21-10.3e", tgt + db10(math.cos(rad(45))))
v.check("Ex 21-10.3f", 43 - tgt)
v.check("Ex 21-10.3g", tgt - 5 - db20(8) + 1.5)
v.check("Ex 21-10.3h", 43 - 23)
v.check("Ex 21-10.3i", 10 ** ((43 - 23 - 5) / 10))

print("Example 21-10.4")
v.check("Ex 21-10.4a", beam_peak(16, 0.5, 60, 26 / 28))
v.check("Ex 21-10.4b", beam_peak(16, 0.5, 60, 30 / 28))
v.check("Ex 21-10.4c", hpbw(16, 0.5, 60))
bw = squint_bw(16, 0.5, 60)
v.check("Ex 21-10.4d", bw * 28)
v.check("Ex 21-10.4h", bw * 100)
v.check("Ex 21-10.4e", db20(af_closed(60, 16, 0.5, 60, 26 / 28)))
v.assert_true("squint loss is symmetric at 26 and 30 GHz",
              abs(af_closed(60, 16, 0.5, 60, 26 / 28) - af_closed(60, 16, 0.5, 60, 30 / 28)) < 1e-12)
tspan = 15 * (C / 28e9 / 2) * math.sin(rad(60)) / C
v.check("Ex 21-10.4f", tspan * 1e12)
v.check("Ex 21-10.4i", tspan * 28e9)
v.check("Ex 21-10.4g", db20(16))
v.check("Ex 21-10.4j", db10(16))
v.check("Ex 21-10.4k", beam_peak(16, 0.5, 60, 26 / 28) - 60)
v.check("Ex 21-10.4l", 60 - beam_peak(16, 0.5, 60, 30 / 28))

# §3.6 mean-power identity: E|AF|^2 = S|AF0|^2 + (1-S)/N, checked by brute-force expectation over
# all 2-bit error patterns for a random 3-element weight set (errors uniform on 4 discrete points
# so the expectation is an exact finite sum; S = |E e^{j eps}|^2 for that distribution).
_rng = np.random.default_rng(10)
_a = np.exp(1j * _rng.uniform(0, 2 * np.pi, 3))
_pts = np.array([-0.3, -0.1, 0.1, 0.3])
_mean = np.mean([abs(np.sum(_a * np.exp(1j * np.array(e))) / 3) ** 2
                 for e in itertools.product(_pts, repeat=3)])
_S = abs(np.mean(np.exp(1j * _pts))) ** 2
v.assert_true("quantization mean-power identity", abs(_mean - (_S * abs(np.sum(_a) / 3) ** 2 + (1 - _S) / 3)) < 1e-12)
v.assert_true("TTD array has no loss toward 60 deg at 26 GHz", abs(af_closed(60, 16, 0.5, 60, 26 / 28, ttd=True) - 1) < 1e-12)

print("Example 21-10.5")
for (a, b, c), bits in ((("a", "b", "c"), 3), (("d", "e", "f"), 4)):
    xq = math.pi / 2 ** bits
    S = (math.sin(xq) / xq) ** 2
    v.check(f"Ex 21-10.5{a}", -db10(S))
    v.check(f"Ex 21-10.5{b}", math.degrees(math.sqrt(xq ** 2 / 3)))      # rms of uniform(-x, x)
    v.check(f"Ex 21-10.5{c}", db10((1 - S) / 64))

print("Example 21-10.6")
E, GE, ETA, POH = 1000.0, 10 ** 0.5, 0.15, 0.1
pdc = lambda n: n * (E / (n ** 2 * GE) / ETA + POH)  # noqa: E731
res = optimize.minimize_scalar(pdc, bounds=(1, 2000), method="bounded", options={"xatol": 1e-9})
v.check("Ex 21-10.6a", res.x)
v.check("Ex 21-10.6b", res.fun)
v.check("Ex 21-10.6c", E / (res.x ** 2 * GE) * 1e3)
v.check("Ex 21-10.6g", db10(E / (res.x ** 2 * GE) * 1e3))
v.check("Ex 21-10.6d", pdc(64))
v.check("Ex 21-10.6e", E / (64 ** 2 * GE) * 1e3)
v.check("Ex 21-10.6h", db10(E / (64 ** 2 * GE) * 1e3))
v.check("Ex 21-10.6f", pdc(256))
v.check("Ex 21-10.6i", res.x * POH)

print("Example 21-10.7")
padc = 20e-15 * 2 ** 8 * 1e9
chain = 2 * padc + 0.040
dig, hyb, ana = 64 * chain, 4 * chain + 64 * 0.015, chain + 64 * 0.015
v.check("Ex 21-10.7a", padc * 1e3)
v.check("Ex 21-10.7b", dig)
v.check("Ex 21-10.7c", hyb)
v.check("Ex 21-10.7d", ana)
v.check("Ex 21-10.7e", (hyb / ana - 1) * 100)
v.check("Ex 21-10.7f", dig / ana)

print("Example 21-10.8")
g_ue = 5 + db10(4)
nf = floor_dbm(100e6, 10)
pl_los = lambda d: 32.4 + 21 * lg(d) + 20 * lg(28)  # noqa: E731
pl_nl = lambda d: max(pl_los(d), 35.3 * lg(d) + 22.4 + 21.3 * lg(28) - 0.3 * (1.5 - 1.5))  # noqa: E731
v.check("Ex 21-10.8a", g_ue)
v.check("Ex 21-10.8b", nf)
v.check("Ex 21-10.8c", pl_los(100))
pr1 = 60 - pl_los(100) + g_ue
v.check("Ex 21-10.8d", pr1)
v.check("Ex 21-10.8e", pr1 - nf)
v.check("Ex 21-10.8f", pl_nl(200))
v.check("Ex 21-10.8l", pl_los(200))
gam = 0.2051 * 25 ** 0.9679
v.check("Ex 21-10.8g", gam)
v.check("Ex 21-10.8k", gam * 0.2)
pr2 = 60 - pl_nl(200) - gam * 0.2 - 0.02 + g_ue
v.check("Ex 21-10.8h", pr2)
v.check("Ex 21-10.8i", pr2 - nf)
v.check("Ex 21-10.8j", pr2 - 30 - nf)
v.check("Ex 21-10.8m", pl_nl(200) - pl_los(100))

print("Example 21-10.9")
lam77 = C / 77e9
rx = [k * 0.5 for k in range(4)]
tx = [k * 2.0 for k in range(3)]
virt = sorted({a + b for a in tx for b in rx})
v.assert_true("virtual positions form a filled lambda/2 line", np.allclose(np.diff(virt), 0.5))
v.check("Ex 21-10.9a", lam77 * 1e3)
v.check("Ex 21-10.9b", len(virt))
v.check("Ex 21-10.9c", (virt[-1] - virt[0]) * lam77 * 1e3)
null = optimize.brentq(lambda s: math.sin(len(virt) * math.pi * s / 2), 1e-3, 3.0 / len(virt))
v.check("Ex 21-10.9d", math.degrees(null))          # first null sin(theta) = 2/N, i.e. the Rayleigh resolution
v.check("Ex 21-10.9e", len(tx) + len(rx))

# ================================================================ problems
print("Problems")
w, ee, dl, L = patch(39e9, 3.5, 0.2e-3)
v.check("21-10.1a", w * 1e3)
v.check("21-10.1b", ee)
v.check("21-10.1c", dl * 1e3)
v.check("21-10.1d", L * 1e3)
v.check("21-10.1e", C / 39e9 / 2 * 1e3)

gm = 1.5 / 3.5
v.check("21-10.2a", 0.7 * (1 - gm ** 2) * 100)
v.check("21-10.2b", db10(0.7 * (1 - gm ** 2)))
v.check("21-10.2c", -db10(math.cos(rad(30)) ** 2))

ka = 2 * math.pi * 0.020 / (C / 868e6)
v.check("21-10.3a", ka)
v.check("21-10.3b", q_chu(ka))
v.check("21-10.3c", bw_numeric(q_chu(ka), 2) * 100)
v.check("21-10.3d", 7 / 866.5 * 100)
v.assert_true("Problem 21-10.3: the antenna covers the band", bw_numeric(q_chu(ka), 2) > 7 / 866.5)

v.check("21-10.4a", bw_numeric(20, 3) * 100)
v.check("21-10.4b", bw_numeric(20, 2) * 100)
v.check("21-10.4c", (bw_numeric(20, 3) / bw_numeric(20, 2) - 1) * 100)

v.check("21-10.5a", 8 * C / 39e9 / 2 * 1e3)
v.check("21-10.5b", 5 + db10(64))
v.check("21-10.5c", 5 + db10(64) + db10(math.cos(rad(50))))

for key, d in (("a", 0.6), ("b", 0.8)):
    v.check(f"21-10.6{key}", deg(math.asin(1 / d - 1)))
th = np.linspace(-89.99, -1, 89000)
afv = np.array([af_closed(t, 16, 0.8, 30) for t in th])
v.check("21-10.6c", th[np.argmax(afv)])

v.check("21-10.7a", squint_bw(64, 0.5, 45) * 100)
v.check("21-10.7b", squint_bw(64, 0.5, 45) * 39e3)
v.check("21-10.7c", 63 * (C / 39e9 / 2) * math.sin(rad(45)) / C * 1e12)
v.check("21-10.7d", hpbw(64, 0.5, 0))

for key, bits in (("a", 5), ("c", 6)):
    xq = math.pi / 2 ** bits
    v.check(f"21-10.8{key}", -db20(math.sin(xq) / xq))
v.check("21-10.8b", deg(math.pi / 32 / 3 ** 0.5))

v.check("21-10.9", 8 - 1 + 5 + db20(8))

E2, ETA2, POH2 = 100.0, 0.2, 0.05
p2 = lambda n, poh=POH2: n * (E2 / (n ** 2 * GE) / ETA2 + poh)  # noqa: E731
r2 = optimize.minimize_scalar(p2, bounds=(1, 2000), method="bounded", options={"xatol": 1e-9})
v.check("21-10.10a", r2.x)
v.check("21-10.10b", r2.fun)
v.check("21-10.10c", optimize.minimize_scalar(lambda n: p2(n, POH2 / 2), bounds=(1, 2000), method="bounded",
                                              options={"xatol": 1e-9}).x)

pa6 = 20e-15 * 2 ** 6 * 2e9
ch6 = 2 * pa6 + 0.040
v.check("21-10.11a", pa6 * 1e3)
v.check("21-10.11b", 64 * ch6)
v.check("21-10.11c", 8 * ch6 + 64 * 0.015)

nf60 = floor_dbm(2.16e9, 10)
v.check("21-10.12a", nf60)
for (k_pl, k_ab, k_snr, k_pr), dist in ((("b", "c", "e", "d"), 50), (("f", "g", "h", None), 500)):
    pl, ab = fspl(60e9, dist), 14.7 * dist / 1000
    pr = 40 - pl - ab + 15
    v.check(f"21-10.12{k_pl}", pl)
    v.check(f"21-10.12{k_ab}", ab)
    v.check(f"21-10.12{k_snr}", pr - nf60)
    if k_pr:
        v.check(f"21-10.12{k_pr}", pr)

nv = math.ceil(2 / rad(2))
v.check("21-10.13a", nv)
side = next(k for k in range(1, 20) if k * k >= nv)
v.check("21-10.13b", side)
v.check("21-10.13c", 2 * side)
v.check("21-10.13d", deg(2 / side ** 2))

nb = round(16 * math.sin(rad(60)))
v.check("21-10.14a", nb)
v.check("21-10.14b", nb * 0.125)
v.check("21-10.14c", nb ** 2 * 0.125)

v.check("21-10.15a", 4 * 4)
v.check("21-10.15b", lam77 / 2 * 1e3)
v.check("21-10.15c", 15 * lam77 / 2 * 1e3)
v.check("21-10.15d", deg(2 / 16))
v.check("21-10.15e", 13.5 + db10(4))
v.check("21-10.15f", db20(4))

# ================================================================ lab
print("Lab")
v.check("Lab 21-10.a", bw_numeric(q_chu(2 * math.pi * 0.0075 / lam), 2) * 100)
v.check("Lab 21-10.b", deg(math.asin(0.5 - 1 / 0.8)))
v.check("Lab 21-10.c", deg(math.asin(1 / 0.8 - 1)))
v.check("Lab 21-10.d", -db10(math.cos(rad(30))))
v.check("Lab 21-10.e", hpbw(16, 0.5, 30))
xq = math.pi / 8
S3 = (math.sin(xq) / xq) ** 2
v.check("Lab 21-10.f", -db10(S3 + (1 - S3) / 64))
v.check("Lab 21-10.g", db10((1 - S3) / 64))
rng = np.random.default_rng(2026)
k = np.arange(64)
eps = rng.uniform(-xq, xq, (20000, 64))
peak = np.mean(np.abs(np.exp(1j * eps).sum(axis=1)) ** 2) / 64 ** 2
v.assert_true("Monte Carlo (independent seed) gain loss within 0.01 dB of the formula",
              abs(-db10(peak) - (-db10(S3 + (1 - S3) / 64))) < 0.01, f"{-db10(peak):.4f}")

# Problem 21-10.16: Monte Carlo of the mean pattern at an ideal null, 16 elements, 3-bit (uniform +-pi/8) errors.
_rng16 = np.random.default_rng(1016)
_u = 2 / 16  # first null of a 16-element lambda/2 array: N pi u / 2 = pi
_acc = 0.0
for _ in range(20000):
    _w = np.exp(1j * _rng16.uniform(-math.pi / 8, math.pi / 8, 16)) / 16
    _acc += abs(np.sum(_w * np.exp(1j * math.pi * np.arange(16) * _u))) ** 2
v.check("21-10.16", 10 * math.log10(_acc / 20000), tol=0.1)  # Monte Carlo: +-0.1 dB at 20,000 trials
v.finish()
