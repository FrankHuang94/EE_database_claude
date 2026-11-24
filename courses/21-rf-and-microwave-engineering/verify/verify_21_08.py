#!/usr/bin/env python3
"""Verify every number in chapter 21-08 (transceiver architectures), its problems and its lab.

Independent routes (the lab module trx.py uses the closed forms):
- preselector attenuation is computed from the ladder network itself (complex nodal analysis of the
  shunt-series-shunt band-pass with 50 ohm terminations) instead of the Butterworth formula;
- spurious responses are found by brute-force search over (m, n);
- I/Q-mismatch EVM is simulated with OFDM and compared with the closed-form IRR;
- complex-filter selectivity is evaluated from the state equation's transfer function at -f_IF;
- Nyquist folding is computed by explicit modular arithmetic; jitter SNR by a seeded sampling simulation;
- ngspice confirms the preselector and the complex filter (preselect.cir, complexfilter.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import trx as lab  # noqa: E402

v = Verifier.from_files("21-08", ROOT / "chapters" / "21-08-transceiver-architectures.md",
                        ROOT / "solutions" / "21-08-solutions.md", LAB / "README.md")
lg = math.log10
db10 = lambda x: 10 * lg(x)  # noqa: E731
db20 = lambda x: 20 * lg(x)  # noqa: E731


def ladder_atten_db(f, f0, bw, order=3, z0=50.0):
    """Insertion loss of an order-n (1..3 shown; general n alternating shunt/series) Butterworth band-pass ladder,
    computed by ABCD matrices of its resonators."""
    w0 = 2 * math.pi * f0
    d = bw / f0
    g = [2 * math.sin((2 * k - 1) * math.pi / (2 * order)) for k in range(1, order + 1)]
    s = 2j * math.pi * f
    M = np.eye(2, dtype=complex)
    for k, gk in enumerate(g):
        if k % 2 == 0:   # shunt parallel LC
            C = gk / (z0 * w0 * d)
            L = z0 * d / (w0 * gk)
            Y = s * C + 1 / (s * L)
            M = M @ np.array([[1, 0], [Y, 1]])
        else:            # series LC
            L = gk * z0 / (w0 * d)
            C = d / (w0 * gk * z0)
            Z = s * L + 1 / (s * C)
            M = M @ np.array([[1, Z], [0, 1]])
    A, B, C_, D = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    s21 = 2 / (A + B / z0 + C_ * z0 + D)
    return -db20(abs(s21))


def order_needed(f, f0, bw, req):
    return next(n for n in range(1, 40) if ladder_atten_db(f, f0, bw, n) >= req)


# ================================================================ Example 21-08.1
F0, BW = 2.45e9, 100e6
LO1 = 2.45e9 + 300e6
IM1 = 2 * LO1 - 2.45e9
v.check("Ex 21-08.1a", LO1 / 1e9)
v.check("Ex 21-08.1b", IM1 / 1e9)
for key, n in zip("cde", (1, 2, 3)):
    v.check(f"Ex 21-08.1{key}", ladder_atten_db(IM1, F0, BW, n))
v.check("Ex 21-08.1f", order_needed(IM1, F0, BW, 60))
IM40 = 2.45e9 + 80e6
v.check("Ex 21-08.1g", IM40 / 1e9)
v.check("Ex 21-08.1h", order_needed(IM40, F0, BW, 60))
v.check("Ex 21-08.1i", 300e6 / 1e6)
v.check("Ex 21-08.1j", 40e6 / 1e6)


# ================================================================ Example 21-08.2
def brute_spurs(flo, fif, lo, hi, mmax=4, nmax=4, step=1e6):
    found = set()
    for m in range(0, mmax + 1):
        for n in range(1, nmax + 1):
            for f in np.arange(lo, hi + step / 2, step):
                if abs(abs(m * flo - n * f) - fif) < step / 4:
                    found.add((m, n, round(f / 1e6, 3)))
    return found


sp = brute_spurs(LO1, 300e6, 1.0e9, 3.0e9, step=1e6)
half = sorted(f for m, n, f in sp if (m, n) == (2, 2))
v.check("Ex 21-08.2a", half[0] / 1e3)
v.check("Ex 21-08.2b", half[1] / 1e3)
v.check("Ex 21-08.2c", ladder_atten_db(half[0] * 1e6, F0, BW, 3))
v.check("Ex 21-08.2d", ladder_atten_db(half[1] * 1e6, F0, BW, 3))
one_two = sorted(f for m, n, f in sp if (m, n) == (1, 2))
v.check("Ex 21-08.2e", one_two[0] / 1e3)
v.check("Ex 21-08.2f", one_two[1] / 1e3)

# ================================================================ Example 21-08.3
v.check("Ex 21-08.3a", db20(0.035))
v.check("Ex 21-08.3b", -db20(0.01))
for (ke, kt), irr in ((("c", "d"), 40.0), (("f", "g"), 45.0)):
    e = math.sqrt(2 * 10 ** (-irr / 10))                     # equal share, small-error formula as in the text
    v.check(f"Ex 21-08.3{ke}", e * 100)
    v.check(f"Ex 21-08.3{kt}", math.degrees(e))
    ex = optimize.brentq(lambda x: lab.irr_db(x, math.degrees(x)) - irr, 1e-5, 0.2)
    v.assert_true(f"exact formula within 0.5% of the small-error share at {irr} dB", abs(ex / e - 1) < 5e-3)
v.check("Ex 21-08.3e", 45)

# ================================================================ Example 21-08.4
v.check("Ex 21-08.4a", 23 - 50)
NF4 = -174 + db10(20e6) + 5
v.check("Ex 21-08.4b", NF4)
v.check("Ex 21-08.4c", 2 * (23 - 50) - (NF4 - 10))

# ================================================================ Example 21-08.5
v.check("Ex 21-08.5a", 25)
e5 = math.sqrt(2 * 10 ** -2.5)
v.check("Ex 21-08.5b", e5 * 100)
v.check("Ex 21-08.5c", math.degrees(e5))
wif, wp = 2 * math.pi * 1e6, 2 * math.pi * 0.5e6
Himg = wp / (wp + 1j * (-wif - wif))      # state-equation transfer function at -f_IF
v.check("Ex 21-08.5d", -db20(abs(Himg)))
v.check("Ex 21-08.5e", -lab.complex_filter_db(-1e6, 1e6, 0.5e6, 3))


# ================================================================ Example 21-08.6
def fold(f, fs):
    r = math.fmod(f, fs)
    return min(r, fs - r), int(f // (fs / 2)) + 1


FS = 2949.12e6
al, zone = fold(3.5e9, FS)
v.check("Ex 21-08.6a", zone)
v.check("Ex 21-08.6b", al / 1e6)
v.check("Ex 21-08.6c", -db20(2 * math.pi * 3.5e9 * 50e-15))
floor = -154.1 + 2.6
v.check("Ex 21-08.6d", floor)
NFA = floor + 174
v.check("Ex 21-08.6e", NFA)
G6 = optimize.brentq(lambda g: 10 ** 0.15 + (10 ** (NFA / 10) - 1) / g - 10 ** 0.3, 1, 1e5)
v.check("Ex 21-08.6f", db10(G6))
v.check("Ex 21-08.6g", -15 + db10(G6))
v.check("Ex 21-08.6h", db10(FS / (2 * 100e6)))

# ================================================================ Example 21-08.7
v.check("Ex 21-08.7a", lab.irr_db(0.01, 1.0))
v.check("Ex 21-08.7b", db20(0.5e-3 / 0.5))
v.check("Ex 21-08.7c", -174 + 5 - 10 + 50)
v.check("Ex 21-08.7d", -174 + 5 - 10 + 50 - 23)

# ================================================================ Example 21-08.8
PHI = 2 * math.pi * 7.115e9 * 57.9e-15
v.check("Ex 21-08.8a", PHI * 1e3)
v.check("Ex 21-08.8b", db20(PHI))
TOT = db10(PHI ** 2 + 10 ** -4.8 + 10 ** -4.0)
v.check("Ex 21-08.8c", TOT)
v.check("Ex 21-08.8d", -38 - TOT)

# ================================================================ text values
v.check("Txt 21-08.a", db10(4 / math.radians(0.3) ** 2))
v.check("Txt 21-08.b", 10513.0 / 10 / 1e3)
v.check("Txt 21-08.c", -155.6 + 158.1)
v.check("Txt 21-08.d", db10(2))
v.check("Txt 21-08.e", -db20(2 * math.pi * 6e9 * 50e-15))
v.check("Txt 21-08.f", 191 / 266 * 100)
v.check("Txt 21-08.g", 5 * 4)
v.check("Txt 21-08.h", (39 - 1.76) / 6.02)
v.check("Txt 21-08.i", -db20(2 * math.pi * 2.4e9 * 50e-15))

# ================================================================ problems
LO_P1 = 1.9e9 - 200e6
v.check("21-08.1a", LO_P1 / 1e9)
v.check("21-08.1b", (LO_P1 - 200e6) / 1e9)
for key, n in zip("abc", (1, 2, 3)):
    v.check(f"21-08.2{key}", ladder_atten_db(1.5e9, 1.9e9, 60e6, n))
v.check("21-08.2d", order_needed(1.5e9, 1.9e9, 60e6, 50))
v.check("21-08.3a", 7.0)
v.check("21-08.3b", 8.2)
v.check("21-08.3c", 1.19)
v.check("21-08.3d", 1.18)
v.check("21-08.3e", ladder_atten_db(1.18e9, 1.2e9, 20e6, 2))
v.check("21-08.3f", order_needed(1.18e9, 1.2e9, 20e6, 60))
sp4 = brute_spurs(LO_P1, 200e6, 1.0e9, 5.5e9, mmax=3, nmax=2, step=10e6)
h3 = sorted(f for m, n, f in sp4 if (m, n) == (3, 1))
v.check("21-08.4a", h3[0] / 1e3)
v.check("21-08.4b", h3[1] / 1e3)
hh = sorted(f for m, n, f in sp4 if (m, n) == (2, 2))
v.check("21-08.4c", hh[1] / 1e3)
v.check("21-08.4d", hh[0] / 1e3)
v.check("21-08.4e", ladder_atten_db(1.8e9, 1.9e9, 60e6, 3))
v.check("21-08.4f", ladder_atten_db(1.6e9, 1.9e9, 60e6, 3))
v.check("21-08.5a", 10 ** (-35 / 20) * 100)
v.check("21-08.5b", (10 ** (-35 / 20) / 0.025) ** 2 * 100)
for key, B in (("a", 1e6), ("b", 100e6)):
    f = np.geomspace(1e4, B, 200001)
    tot = np.trapezoid(1 + 0.2e6 / f, f)
    v.check(f"21-08.6{key}", db10(tot / (B - 1e4)))
v.check("21-08.7", 2 * (-30) + 106)
v.check("21-08.8a", 37)
e8 = math.sqrt(2 * 10 ** -3.7)
v.check("21-08.8b", e8 * 100)
v.check("21-08.8c", math.degrees(e8))
v.check("21-08.8d", -lab.complex_filter_db(-2e6, 2e6, 1e6, 4))
for (kz, ka), f in ((("a", "b"), 2.45e9), (("c", "d"), 5.8e9)):
    al9, z9 = fold(f, 3e9)
    v.check(f"21-08.9{kz}", z9)
    v.check(f"21-08.9{ka}", al9 / 1e9)
v.check("21-08.10a", 10 ** (-3) / (2 * math.pi * 6e9) * 1e15)
v.check("21-08.10b", -60 - db10(1.5e9))
G11 = (10 ** 2.5 - 1) / (10 ** 0.25 - 10 ** 0.1)
v.check("21-08.11a", db10(G11))
v.check("21-08.11b", 2 - 6 - db10(G11))
v.check("21-08.11c", db10(10 ** 0.15 * (10 ** 0.1 + (10 ** 2.5 - 1) / G11)))
th = math.radians(0.5)
e12 = math.sqrt(4e-4 - th * th)
v.check("21-08.12a", e12 * 100)
v.check("21-08.12b", lab.irr_db(e12, 0.5))
v.check("21-08.13a", -174 + 4 - 6 + 45)
v.check("21-08.13b", -174 + 4 - 6 + 45 - 26)
v.check("21-08.13c", -135 + 176)
v.check("21-08.14", 4 * 4 + 1)

# ================================================================ lab
evm = lab.ofdm_iq_evm_db(0.01, 1.0)
v.check("Lab 21-08.a", evm)
v.assert_true("OFDM I/Q EVM equals -IRR", abs(evm + lab.irr_db(0.01, 1.0)) < 1e-6)
js = lab.jitter_snr_sim(3.5e9, FS, 50e-15)
v.check("Lab 21-08.b", js)
v.assert_true("jitter simulation within 0.5 dB of the formula", abs(js - lab.jitter_snr_db(3.5e9, 50e-15)) < 0.5)
taps = 1023
k = np.arange(taps) - (taps - 1) / 2
fc = 10e6 / 3e9
h = 2 * fc * np.sinc(2 * fc * k) * np.blackman(taps)
ENBW = 3e9 * np.sum(h ** 2) / np.sum(h) ** 2
v.check("Lab 21-08.c", ENBW / 1e6)
PRED = 60 + db10(3e9 / (2 * ENBW))
v.check("Lab 21-08.d", PRED)
_, _, snr_in = lab.ddc_snr()
v.check("Lab 21-08.e", snr_in)
v.assert_true("DDC simulation within 0.5 dB of the ENBW prediction", abs(snr_in - PRED) < 0.5)

sys.exit(v.finish())
