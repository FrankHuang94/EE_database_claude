#!/usr/bin/env python3
"""Verify every number in chapter 21-12 (modem baseband and standards), its problems and its lab.

Independent routes (the lab module modem.py uses closed forms):
- NR rates are rebuilt from resource elements per second (RBs x 12 x symbols per second) and the overhead, written
  out separately from the 38.306 expression;
- FFT costs are counted by running a radix-2 recursion that tallies butterflies;
- Wi-Fi rates come from bits per OFDM symbol divided by the symbol duration;
- two-way ranging is simulated event by event with explicit clock models; the double-sided estimate is evaluated
  with exact rational arithmetic;
- phase-based ranging distances come from a two-tone phase difference and from a least-squares fit written here;
- the ionosphere-free coefficients are solved as a 2x2 linear system (unit geometry, zero 1/f^2 term);
- Doppler comes from differentiating the satellite-user range numerically over an orbit.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-12-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("21-12", ROOT / "chapters" / "21-12-modem-baseband-and-standards.md",
                        ROOT / "solutions" / "21-12-solutions.md", LAB / "README.md")
C = 299_792_458.0
GM, RE = 3.986004418e14, 6_371_000.0


def nr_rate(layers, qm, rbs, scs_khz, oh=0.14):
    """Resource elements per second times bits per RE at the top code rate, less overhead (Mb/s)."""
    symbols_per_s = 14 * 1000 * scs_khz / 15
    re_per_s = rbs * 12 * symbols_per_s
    return layers * qm * (948 / 1024) * re_per_s * (1 - oh) / 1e6


def fft_count(n):
    """Count butterflies (one complex multiply each) of a radix-2 decimation-in-time FFT by recursion."""
    if n == 1:
        return 0
    return 2 * fft_count(n // 2) + n // 2


def wifi(n_sd, bits, rc, gi, streams):
    return streams * n_sd * bits * rc / (12.8e-6 + gi)


def twr(tau, treply1, treply2, ea, eb):
    """Event times on a true clock; each device converts intervals with its own clock rate."""
    t0 = Fraction(0)
    tau, treply1, treply2 = Fraction(tau), Fraction(treply1), Fraction(treply2)
    ea, eb = Fraction(ea), Fraction(eb)
    t_b_rx = t0 + tau
    t_b_tx = t_b_rx + treply1
    t_a_rx = t_b_tx + tau
    t_a_tx = t_a_rx + treply2
    t_b_rx2 = t_a_tx + tau
    r1, d1 = (t_a_rx - t0) * (1 + ea), (t_b_tx - t_b_rx) * (1 + eb)
    r2, d2 = (t_b_rx2 - t_b_tx) * (1 + eb), (t_a_tx - t_a_rx) * (1 + ea)
    return float((r1 - d1) / 2), float((r1 * r2 - d1 * d2) / (r1 + r2 + d1 + d2))


def iono_coeffs(f1, f2):
    """Solve a + b = 1 (geometry preserved) and a/f1^2 + b/f2^2 = 0 (ionosphere removed)."""
    sol = np.linalg.solve(np.array([[1.0, 1.0], [1 / f1 ** 2, 1 / f2 ** 2]]), np.array([1.0, 0.0]))
    return sol[0], sol[1]


def doppler_max(f, h):
    """Largest Doppler for a user under the ground track: differentiate the range over the orbit numerically."""
    w = math.sqrt(GM / (RE + h)) / (RE + h)
    t = np.linspace(-600, 600, 200001)
    x, y = (RE + h) * np.sin(w * t), (RE + h) * np.cos(w * t)
    rng = np.hypot(x, y - RE)
    vis = y - RE > 0
    rr = np.gradient(rng, t)
    return f * np.max(-rr[vis]) / C


def doppler_at_elev(f, h, el):
    w = math.sqrt(GM / (RE + h)) / (RE + h)
    t = np.linspace(-600, 0, 400001)
    x, y = (RE + h) * np.sin(w * t), (RE + h) * np.cos(w * t)
    elev = np.degrees(np.arctan2(y - RE, np.abs(x)))
    rr = np.gradient(np.hypot(x, y - RE), t)
    i = np.argmin(np.abs(elev - el))
    return -f * rr[i] / C


# ================================================================ chapter
print("Example 21-12.1")
r100, r40 = nr_rate(4, 10, 273, 30), nr_rate(4, 10, 106, 30)
v.check("Ex 21-12.1a", r100)
v.check("Ex 21-12.1b", r40)
tot = 3 * r100 + 2 * r40
v.check("Ex 21-12.1c", tot)
v.check("Ex 21-12.1d", (11200 / tot - 1) * 100)
v.check("Ex 21-12.1e", nr_rate(4, 8, 273, 30))

print("Example 21-12.2")
v.check("Ex 21-12.2a", 150752 / 1e3)
l2 = (10e9 + 3.5e9) * 0.040 / 8
v.check("Ex 21-12.2b", l2 / 1e6)
v.check("Ex 21-12.2c", l2 / 1.9e6)

print("Example 21-12.3")
tb = r100 * 1e6 * 0.5e-3
v.check("Ex 21-12.3a", tb / 1e6)
v.check("Ex 21-12.3b", tb * 1.5 / 1e6)
v.check("Ex 21-12.3c", 16 * tb * 1.5 * 6 / 8 / 1e6)

print("Example 21-12.4")
v.check("Ex 21-12.4a", 10e9 * 5.14e-12 * 1e3)
v.check("Ex 21-12.4b", 10e9 * 58.6e-12 * 1e3)
v.check("Ex 21-12.4c", 118.3e9 * 5.14e-12)
v.check("Ex 21-12.4d", 118.3 / 2.35)
v.check("Ex 21-12.4e", 10 / (118.3 / 2.35))

print("Example 21-12.5")
nfft = fft_count(4096)
v.check("Ex 21-12.5a", nfft)
v.check("Ex 21-12.5b", nfft * 28000 / 1e6)
v.check("Ex 21-12.5c", nfft * 28000 * 4 / 1e9)

print("Example 21-12.6")
s1 = wifi(3920, 12, 5 / 6, 0.8e-6, 1)
v.check("Ex 21-12.6a", s1 / 1e6)
v.check("Ex 21-12.6b", 8 * s1 / 1e9)
v.check("Ex 21-12.6c", 16 * s1 / 1e9)
v.check("Ex 21-12.6d", wifi(1960, 12, 5 / 6, 0.8e-6, 2) / 1e6)
v.check("Ex 21-12.6e", wifi(3920, 12, 5 / 6, 0.8e-6, 2) / 1e6)
v.check("Ex 21-12.6f", (12 / 10 - 1) * 100)

print("Example 21-12.7")
v.check("Ex 21-12.7a", 1 / 499.2e6 * 1e9)
v.check("Ex 21-12.7b", C / 499.2e6)
ss, ds = twr(10 / C, 1e-3, 1e-3, 20e-6, 0.0)
v.check("Ex 21-12.7c", (ss - 10 / C) * 1e9)
v.check("Ex 21-12.7d", (ss - 10 / C) * C)
v.check("Ex 21-12.7e", 2 * 0.1 / (C * 1e-3) * 1e6)
v.assert_true("double-sided residual equals range x mean clock offset (0.1 mm at 10 m, 20 ppm)", abs((ds - 10 / C) * C - 10 * 20e-6 / 2) < 1e-7)
import sympy as sp  # noqa: E402
_a, _b, _tau, _d1, _d2 = sp.symbols("a b tau D1 D2", positive=True)
_tr1, _td1, _tr2, _td2 = _a * (2 * _tau + _d1), _b * _d1, _b * (2 * _tau + _d2), _a * _d2
_est = (_tr1 * _tr2 - _td1 * _td2) / (_tr1 + _tr2 + _td1 + _td2)
v.assert_true("§3.5: DS-TWR estimate is exactly 2ab tau/(a+b), independent of D1 and D2",
              sp.simplify(_est - 2 * _a * _b * _tau / (_a + _b)) == 0)

print("Example 21-12.8")
v.check("Ex 21-12.8a", C * math.radians(30) / (4 * math.pi * 1e6))
v.check("Ex 21-12.8b", C / (2 * 1e6))
v.check("Ex 21-12.8c", C / (2 * 72e6))
fr = 2402e6 + np.arange(2) * 1e6
ph = -4 * np.pi * fr * 12.49135 / C
v.assert_true("two-tone phase difference of a 12.49 m path is 30 degrees (mod 360)",
              abs(((math.degrees(ph[0] - ph[1]) + 180) % 360) - 180 - 30) < 0.01)

print("Example 21-12.9")
f1, f5, f2 = 1575.42e6, 1176.45e6, 1227.60e6
v.check("Ex 21-12.9a", C / 1.023e6)
v.check("Ex 21-12.9b", C / 10.23e6)
v.check("Ex 21-12.9c", f1 / 10.23e6)
v.check("Ex 21-12.9d", f5 / 10.23e6)
v.check("Ex 21-12.9e", 5.0 * (f1 / f5) ** 2)
a15, b15 = iono_coeffs(f1, f5)
v.check("Ex 21-12.9f", a15)
v.check("Ex 21-12.9g", b15)
v.check("Ex 21-12.9h", math.hypot(a15, b15))

print("Example 21-12.10")
vorb = math.sqrt(GM / (RE + 600e3))
v.check("Ex 21-12.10a", vorb / 1e3)
v.check("Ex 21-12.10b", doppler_max(1.0, 600e3) * C / 1e3)
v.check("Ex 21-12.10c", doppler_max(2e9, 600e3) / 1e3)
v.check("Ex 21-12.10d", 2 * 1075.088e3 / C * 1e3)
rtt_geo = 4 * 35786e3 / C
v.check("Ex 21-12.10e", rtt_geo * 1e3)
v.check("Ex 21-12.10f", math.ceil(rtt_geo / 1e-3))

print("Text")
v.check("Txt 21-12.a", 20e9 / 100e6)
v.check("Txt 21-12.b", nfft * 28000 / 1e9)
v.check("Txt 21-12.c", 16 * s1 / 1e9)
v.check("Txt 21-12.d", C / 2e6)
v.check("Txt 21-12.e", C / (2 * 72e6))
v.check("Txt 21-12.f", 10e3 / 314.38)
v.check("Txt 21-12.g", 12.5e3 / 314.38)
v.check("Txt 21-12.h", 24072 / 37208 * 100)
v.check("Txt 21-12.i", (24072 / 27793 - 1) * 100)
v.check("Txt 21-12.j", 118.3 / 2.35)
v.check("Txt 21-12.k", 314.38 / 12.5e3 * 100)
v.check("Txt 21-12.l", 314.38 / 10e3 * 100)
v.check("Txt 21-12.m", 2 * math.pi * 6378.137 / 86164.0905)  # WGS-84 equatorial radius, sidereal day

# ================================================================ problems
print("Problems")
p100, p20 = nr_rate(4, 8, 273, 30), nr_rate(2, 6, 106, 15)
v.check("21-12.1a", p100)
v.check("21-12.1b", p20)
v.check("21-12.1c", 2 * p100 + p20)
v.check("21-12.2a", 2019360 / 1e6)
v.check("21-12.2b", 3531888 / 1e6)
v.check("21-12.3a", 16.2e9 * 0.020 / 8 / 1e6)
v.check("21-12.3b", 16.2e9 * 0.050 / 8 / 1e6)
tb40 = r40 * 1e6 * 0.5e-3
v.check("21-12.4a", tb40 / 1e6)
v.check("21-12.4b", tb40 * 1.5 / 1e6)
v.check("21-12.4c", 32 * tb40 * 1.5 * 5 / 8 / 1e6)
v.check("21-12.5a", 12.5e9 * 5.14e-12 * 1e3)
v.check("21-12.5b", 12.5e9 * 58.6e-12 * 1e3)
v.check("21-12.5c", math.ceil(12.5 / 2.38))
v.check("21-12.6", nfft * 14 * 8000 / 1e9)
assert 4 * 980 == 3920 and 2 * 980 == 1960  # 80 MHz is a quarter of the 320 MHz tone plan
v.check("21-12.7a", wifi(980, 12, 5 / 6, 0.8e-6, 2) / 1e6)
v.check("21-12.7b", wifi(980, 12, 5 / 6, 3.2e-6, 2) / 1e6)
tau8 = 10 / C
s8, d8 = twr(tau8, 1e-3, 0.5e-3, 10e-6, -10e-6)
v.check("21-12.8a", tau8 * 1e9)
v.check("21-12.8b", (s8 - tau8) * C)
v.check("21-12.8c", (d8 - tau8) * C * 1e3)
v.check("21-12.9a", C * (2 * math.pi / 5) / (4 * math.pi * 2e6))
v.check("21-12.9b", C / (2 * 2e6))
a12, b12 = iono_coeffs(f1, f2)
v.check("21-12.10a", a12)
v.check("21-12.10b", b12)
v.check("21-12.10c", math.hypot(a12, b12))
v.check("21-12.10d", f2 / 10.23e6)
v.check("21-12.11a", doppler_max(1.54e9, 600e3) / 1e3)
rtt11 = 4 * 1075.088e3 / C
v.check("21-12.11b", rtt11 * 1e3)
v.check("21-12.11c", math.ceil(rtt11 / 1e-3))
# 10 degree elevation: slant range by solving the Earth-centred triangle numerically (law of cosines root).
_re, _rs = 6371e3, 6371e3 + 600e3
d10 = optimize.brentq(lambda d: _rs**2 - (_re**2 + d**2 + 2 * _re * d * math.sin(math.radians(10))), 1e3, 5e6)
v.check("21-12.11d", d10 / 1e3)
v.check("21-12.11e", 4 * d10 / C * 1e3)
v.check("21-12.11f", math.ceil(4 * d10 / C / 1e-3))
v.check("21-12.12a", 50e9 / 500e6)
v.check("21-12.12b", 200e9 / 300e6)
v.check("21-12.13a", (6004 / 3957 - 1) * 100)
v.check("21-12.13b", (7132 / 6617 - 1) * 100)
v.check("21-12.13c", 27793 / 38367 * 100)
v.check("21-12.14", 7.5e-3 / 375e-6)

# ================================================================ lab
print("Lab")
v.check("Lab 21-12.a", 2 * p100 + p20)
v.check("Lab 21-12.b", tot / (2 * p100 + p20))
# e_A - e_B with independent uniforms on +-20 ppm is triangular on +-40 ppm: variance 2 (40e-6)^2 / 12
rms = math.sqrt(2 * (40e-6) ** 2 / 12) * 1e-3 / 2 * C
v.check("Lab 21-12.c", rms)
v.check("Lab 21-12.d", 40e-6 * 1e-3 / 2 * C)
fr72 = 2402e6 + np.arange(72) * 1e6
h = np.exp(-1j * 4 * np.pi * fr72 * 12 / C) + 0.5 * np.exp(-1j * 4 * np.pi * fr72 * 20 / C)
ph = np.unwrap(np.angle(h))
A = np.vstack([fr72, np.ones_like(fr72)]).T
slope = np.linalg.lstsq(A, ph, rcond=None)[0][0]
v.check("Lab 21-12.e", -slope * C / (4 * math.pi))
n = 72 * 16
prof = np.abs(np.fft.ifft(h, n))
v.check("Lab 21-12.f", int(np.argmax(prof)) / (n * 1e6) * C / 2)
for key, el in (("g", 10), ("h", 30), ("i", 60)):
    v.check(f"Lab 21-12.{key}", doppler_at_elev(2e9, 600e3, el) / 1e3)
rng = np.random.default_rng(99)
errs = []
for _ in range(4000):
    ea, eb = rng.uniform(-20e-6, 20e-6, 2)
    errs.append((ea - eb) * 1e-3 / 2 * C)
v.assert_true("simulated single-sided rms within 3% of the triangular-distribution value",
              abs(math.sqrt(np.mean(np.square(errs))) / rms - 1) < 0.03)

# Problem 21-12.15: maximum range rate over a pass, found by scanning the orbit geometry (800 km).
_r15 = 6371e3 + 800e3
_v15 = math.sqrt(3.986e14 / _r15)
_ang = np.linspace(-math.acos(6371e3 / _r15), math.acos(6371e3 / _r15), 400001)
_pos = np.stack([_r15 * np.sin(_ang), _r15 * np.cos(_ang) - 6371e3], axis=1)
_vel = _v15 * np.stack([np.cos(_ang), -np.sin(_ang)], axis=1)
_rr = np.abs(np.sum(_pos * _vel, axis=1) / np.linalg.norm(_pos, axis=1)).max()
v.check("21-12.15a", _v15)
v.check("21-12.15b", _rr)
v.check("21-12.15c", _rr * 2e9 / 299792458 / 1e3)
v.finish()
