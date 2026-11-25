#!/usr/bin/env python3
"""Verify every number in chapter 23-04 (DRAM interfaces), its problems and its lab.

Independent routes (the lab module ddrio.py uses closed forms):
- termination levels by solving the driver-termination node with a linear (nodal) solve;
- DBI by enumerating all bytes (the module's route) against the binomial-sum formula used here;
- reflections by a Bergeron (method-of-characteristics) time-stepping simulation of the line;
- delay per millimetre from scipy's speed of light;
- channel cursors by integrating the first-order channel's ODE for a one-UI pulse and sampling it;
- worst-case eyes by brute force over all symbol patterns on the integrated cursors;
- PAM break-even slopes by root finding on the eye amplitudes.
"""
from __future__ import annotations

import math
import sys
from itertools import product
from math import comb
from pathlib import Path

import numpy as np
from scipy import constants, integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-04", ROOT / "chapters" / "23-04-dram-interfaces.md",
                        ROOT / "solutions" / "23-04-solutions.md", LAB / "README.md")
C = constants.c


# ---------------------------------------------------------------- independent helpers
def node_voltage(v_top, r_top, v_bot, r_bot):
    """Voltage of a node between a source v_top through r_top and v_bot through r_bot (nodal equation)."""
    g = np.array([[1 / r_top + 1 / r_bot]])
    i = np.array([v_top / r_top + v_bot / r_bot])
    return float(np.linalg.solve(g, i)[0])


def dbi_lows(p0, dbi=True):
    """Expected low wires per byte by the binomial sum, bits 0 with probability p0."""
    tot = 0.0
    for k in range(9):
        w = comb(8, k) * p0 ** k * (1 - p0) ** (8 - k)
        tot += w * ((9 - k) if (dbi and k > 4) else k)
    return tot


def bergeron(v_s, r_s, z0, r_l, n_trips):
    """Far-end voltage after each arrival, by stepping the method of characteristics one delay at a time."""
    # forward wave a and backward wave b; at the source: v = a + b, i = (a - b)/z0, v_s = v + r_s i
    b_src = 0.0
    out = []
    for _ in range(n_trips):
        a = (v_s - b_src * (1 - r_s / z0)) / (1 + r_s / z0)  # source boundary
        # far end: incident a; v = a + b_l, i = (a - b_l)/z0 = v/r_l
        if math.isinf(r_l):
            b_l = a
        else:
            b_l = a * (r_l / z0 - 1) / (r_l / z0 + 1)  # from v = a + b_l and (a - b_l)/z0 = v/r_l
        out.append(a + b_l)
        b_src = b_l
    return out


def pulse_cursors(ui, tau, n):
    """Integrate dv/dt = (u - v)/tau for a one-UI unit pulse and sample at the ends of n UIs."""
    def f(t, y):
        u = 1.0 if t < ui else 0.0
        return [(u - y[0]) / tau]
    s1 = integrate.solve_ivp(f, (0, ui), [0.0], rtol=1e-11, atol=1e-14)
    y1 = s1.y[0, -1]
    s2 = integrate.solve_ivp(lambda t, y: [-y[0] / tau], (ui, n * ui), [y1], rtol=1e-11, atol=1e-16,
                             t_eval=[ui * k for k in range(2, n + 1)])
    return [y1] + list(s2.y[0])


def brute_eye(h, levels, taps_removed=0):
    """Worst-case eye (fraction of swing) by trying every pattern of the earlier symbols."""
    lv = np.linspace(-1, 1, levels)
    post = h[1 + taps_removed:]
    worst_isi = sum(abs(x) for x in post)  # the extreme pattern; confirm with explicit enumeration below
    pats = list(product(lv[[0, -1]], repeat=min(len(post), 6)))
    isi = max(abs(sum(c * p for c, p in zip(post[:6], pat))) for pat in pats) + sum(abs(x) for x in post[6:])
    assert abs(isi - worst_isi) < 1e-12
    return (h[0] * (lv[1] - lv[0]) - 2 * isi) / 2


def pam_eye_rc(bit_rate, tau, levels, bits):
    h = pulse_cursors(bits / bit_rate, tau, 40)
    return brute_eye(h, levels)


# ---------------------------------------------------------------- Example 23-04.1
v.check("Ex 23-04.1a", 1 / (8 * (1 / 3200e6)) / 1e6)
v.check("Ex 23-04.1b", 1 / (16 * (1 / 6400e6)) / 1e6)
v.check("Ex 23-04.1c", 1 / (32 * (1 / 9600e6)) / 1e6)
v.check("Ex 23-04.1d", 1 / (16 * (1 / 9600e6)) / 1e6)
for key, (w, bl) in {"Ex 23-04.1e": (64, 8), "Ex 23-04.1f": (32, 16), "Ex 23-04.1g": (64, 16),
                     "Ex 23-04.1h": (16, 32), "Ex 23-04.1i": (16, 16)}.items():
    v.check(key, sum(w for _ in range(bl)) / 8)

# ---------------------------------------------------------------- Example 23-04.2
v.check("Ex 23-04.2a", 64 * 6.4e9 / 8 / 1e9)
v.check("Ex 23-04.2b", 12 * 64 * 6.4e9 / 8 / 1e9)
v.check("Ex 23-04.2c", 16 * 9.6e9 / 8 / 1e9)
bw5090, bw4090 = 512 * 28e9 / 8, 384 * 21e9 / 8
v.check("Ex 23-04.2d", bw5090 / 1e9)
v.check("Ex 23-04.2e", bw4090 / 1e9)
v.check("Ex 23-04.2f", bw5090 / bw4090)
pins = bw5090 * 8 / 6.4e9
v.check("Ex 23-04.2g", pins)
v.check("Ex 23-04.2g1", pins / 512)
v.check("Ex 23-04.2h", 192e9 * 8 / 32 / 1e9)
v.check("Ex 23-04.2i", 8800 / 2)

# ---------------------------------------------------------------- Example 23-04.3 (POD)
vl = node_voltage(1.1, 40, 0.0, 34)
i_pod = (1.1 - vl) / 40
p_pod = 1.1 * i_pod
v.check("Ex 23-04.3a", vl)
v.check("Ex 23-04.3b", 1.1 - vl)
v.check("Ex 23-04.3c", i_pod * 1e3)
v.check("Ex 23-04.3c1", i_pod * 1e3)
v.check("Ex 23-04.3d", p_pod * 1e3)
v.check("Ex 23-04.3d1", p_pod * 1e3)
ui64 = 1 / 6.4e9
v.check("Ex 23-04.3e", ui64 * 1e12)
e0 = integrate.quad(lambda t: p_pod, 0, ui64)[0]
v.check("Ex 23-04.3f", e0 * 1e12)
v.check("Ex 23-04.3f1", e0 * 1e12)
v.check("Ex 23-04.3g", e0 * 0.5 * 1e12)
v.check("Ex 23-04.4g0", e0 * 0.5 * 1e12)
lows = dbi_lows(0.5)
enum = np.mean([(b.count(0) if b.count(0) <= 4 else 9 - b.count(0)) for b in product((0, 1), repeat=8)])
v.assert_true("DBI binomial sum equals enumeration of all 256 bytes", abs(lows - enum) < 1e-12)
v.check("Ex 23-04.3h", lows)
v.check("Ex 23-04.3i", e0 * lows / 8 * 1e12)
v.check("Ex 23-04.3j", 100 * (1 - lows / 4))
v.check("Txt 23-04.a", lows * 256)
v.check("Txt 23-04.b", sum(k * comb(8, k) for k in range(5)))
v.check("Txt 23-04.c", sum((9 - k) * comb(8, k) for k in range(5, 9)))
v.check("Lab 23-04.d", max((b.count(0) if b.count(0) <= 4 else 9 - b.count(0)) for b in product((0, 1), repeat=8)))
v.check("Lab 23-04.e", max(b.count(0) for b in product((0, 1), repeat=8)))

# ---------------------------------------------------------------- Example 23-04.4 (LVSTL)
vh = node_voltage(0.5, 40, 0.0, 40)
p_lv = 0.5 * vh / 40
v.check("Ex 23-04.4a", vh)
v.check("Ex 23-04.4b", vh / 40 * 1e3)
v.check("Ex 23-04.4c", p_lv * 1e3)
ui96 = 1 / 9.6e9
v.check("Ex 23-04.4d", ui96 * 1e12)
v.check("Ex 23-04.4d1", ui96 * 1e12)
v.check("Ex 23-04.4e", p_lv * ui96 * 1e12)
v.check("Ex 23-04.4f", p_lv * ui96 * 0.5 * 1e12)
v.check("Ex 23-04.4f1", p_lv * ui96 * 0.5 * 1e12)
v.check("Ex 23-04.4g", (e0 * 0.5) / (p_lv * ui96 * 0.5))
v.check("Txt 23-04.d", (1.1 / 0.5) ** 2)
v.check("Txt 23-04.g", ui64 / ui96)

# ---------------------------------------------------------------- Example 23-04.5 (reflections)
m40 = bergeron(1.0, 34, 40, 40, 3)
m120 = bergeron(1.0, 34, 40, 120, 40)
mopen = bergeron(1.0, 34, 40, math.inf, 3)
vp = m40[0]
v.check("Ex 23-04.5a", vp)
v.check("Ex 23-04.5a1", vp)
v.assert_true("a matched far end holds the launched wave", abs(m40[2] - m40[0]) < 1e-12)
v.check("Ex 23-04.5b", (34 - 40) / (34 + 40))
v.check("Ex 23-04.5c", m120[0] / vp - 1)
v.check("Ex 23-04.5d", m120[0])
v.check("Ex 23-04.5e1", m120[0] - vp)
v.check("Ex 23-04.5e2", (m120[0] - vp) * (34 - 40) / 74)
v.check("Ex 23-04.5e3", m120[1] - m120[0])
v.check("Ex 23-04.5e", m120[1])
v.check("Ex 23-04.5f", m120[-1])
v.check("Ex 23-04.5g", mopen[0])
v.check("Ex 23-04.5h", mopen[1])
v.check("Txt 23-04.h", 100 * (mopen[0] - 1.0))

# ---------------------------------------------------------------- Example 23-04.6 (fly-by)
d = math.sqrt(4) / C * 1e-3  # s/mm
v.check("Ex 23-04.6a1", C, tol=0.005e8)
v.check("Ex 23-04.6a", d * 1e12)
v.check("Ex 23-04.6b0", 7 * 15)
v.check("Ex 23-04.6b", 105 * d * 1e12, tol=0.5)
v.check("Ex 23-04.6c", 105 * d / ui64)
v.check("Ex 23-04.6d", 105 * d / (2 * ui64))
v.check("Ex 23-04.6e", 0.05 * ui64 / d)
v.check("Txt 23-04.e", 50 * d * 1e12)

# ---------------------------------------------------------------- Example 23-04.7 (ISI, DFE)
ui88 = 1 / 8.8e9
h = pulse_cursors(ui88, 80e-12, 60)
a = sum(h[1:])
v.check("Ex 23-04.7a0", ui88 * 1e12)
v.check("Ex 23-04.7a", a)
v.check("Ex 23-04.7b", h[0])
v.check("Ex 23-04.7c", h[1])
v.check("Ex 23-04.7d", h[2])
v.check("Ex 23-04.7e", brute_eye(h, 2))
v.check("Ex 23-04.7f", brute_eye(h, 2, taps_removed=1))
v.check("Ex 23-04.7g", h[0])
t_close = optimize.brentq(lambda t: brute_eye(pulse_cursors(t, 80e-12, 60), 2), 20e-12, 200e-12, xtol=1e-18)
v.check("Ex 23-04.7h", 1 / t_close / 1e9)
v.check("Txt 23-04.i", h[1])
v.check("Txt 23-04.j", h[1] / a)

# ---------------------------------------------------------------- Example 23-04.8 (PAM)
for k, b in (("1", 1), ("2", 1.5), ("3", 2)):
    v.check(f"Ex 23-04.8a{k}", 48 / b)
    v.check(f"Ex 23-04.8b{k}", 48 / b / 2)
v.check("Ex 23-04.8c1", 20 * math.log10(2))
v.check("Ex 23-04.8c2", 20 * math.log10(3))
v.check("Ex 23-04.8d", (2 / (3 - 1)) / (2 / (4 - 1)))


def eye_amp(alpha, f_nyq, levels):
    return 10 ** (-alpha * f_nyq / 20) / (levels - 1)


v.check("Ex 23-04.8e", eye_amp(1.0, 24, 2))
v.check("Ex 23-04.8f", eye_amp(1.0, 16, 3))
v.check("Ex 23-04.8g", eye_amp(1.0, 12, 4))
v.check("Ex 23-04.8h", optimize.brentq(lambda al: eye_amp(al, 24, 2) - eye_amp(al, 16, 3), 0.01, 5))
v.check("Ex 23-04.8i", optimize.brentq(lambda al: eye_amp(al, 24, 2) - eye_amp(al, 12, 4), 0.01, 5))
v.check("Ex 23-04.8j", optimize.brentq(lambda al: eye_amp(al, 16, 3) - eye_amp(al, 12, 4), 0.01, 5))
v.check("Txt 23-04.f", 100 * (eye_amp(1.0, 12, 4) / eye_amp(1.0, 16, 3) - 1))

# ---------------------------------------------------------------- practitioner arithmetic
v.check("Txt 23-04.k", 14400e6 * 24 / 8 / 1e9)
v.check("Txt 23-04.l", 16 / (500e9 * 8) * 1e12)

# ---------------------------------------------------------------- lab: PAM through an RC channel
v.check("Lab 23-04.a", pam_eye_rc(48e9, 15e-12, 2, 1))
v.check("Lab 23-04.b", pam_eye_rc(48e9, 15e-12, 3, 1.5))
v.check("Lab 23-04.c", pam_eye_rc(48e9, 15e-12, 4, 2))

# ---------------------------------------------------------------- problems
v.check("23-04.1a", 8800 / 16)
v.check("23-04.1b", 2400 / 8)
v.check("23-04.1c", (32 + 8) * 16 / 8)
v.check("23-04.1d", 100 * 8 / 32)
v.check("23-04.1x", 100 * (550 / 400 - 1))
v.check("23-04.2a", 8 * 64 * 5.6e9 / 8 / 1e9)
v.check("23-04.2b", 512 * 8.533e9 / 8 / 1e9)
v.check("23-04.2c", 384 * 32e9 / 8 / 1e9)
d4 = math.sqrt(4) / C * 1e-3
v.check("23-04.3a", 1e12 / 8.8e9)
v.check("23-04.3b0", 28 / 1.5)
v.check("23-04.3b", 1e12 / (28e9 / 1.5))
v.check("23-04.3b1", 1e12 / 28e9)
v.check("23-04.3d0", 1e12 / (28e9 / 1.5))
v.check("23-04.3c", (1 / 8.8e9) / 6.67e-12)
v.check("23-04.3d", (1.5 / 28e9) / 6.67e-12)
vl4 = node_voltage(1.2, 60, 0.0, 48)
i4 = (1.2 - vl4) / 60
v.check("23-04.4a", vl4)
v.check("23-04.4b", 1.2 - vl4)
v.check("23-04.4c", i4 * 1e3)
v.check("23-04.4c1", i4 * 1e3)
v.check("23-04.4d", 1.2 * i4 * 1e3)
v.check("23-04.4d1", 1.2 * i4 * 1e3)
v.check("23-04.4e", 1.2 * i4 / 3.2e9 * 1e12)
v.check("23-04.4f", 1.2 * i4 / 3.2e9 * 0.5 * 1e12)
v.check("23-04.5a", dbi_lows(0.7, dbi=False))
lows7 = np.sum([0.7 ** bb.count(0) * 0.3 ** bb.count(1) * (bb.count(0) if bb.count(0) <= 4 else 9 - bb.count(0))
                for bb in product((0, 1), repeat=8)])
v.check("23-04.5b", lows7)
v.check("23-04.5c", 100 * (1 - lows7 / 5.6))
v.check("23-04.6a", (0.45 / 0.5) ** 2)
v.check("23-04.6b", 100 * (1 - (0.45 / 0.5) ** 2))
v.check("23-04.6c", 0.45 * node_voltage(0.45, 40, 0.0, 40) / 40 * 1e3)
m7 = bergeron(1.0, 40, 45, 60, 40)
vp7 = bergeron(1.0, 40, 45, 45, 1)[0]
v.check("23-04.7a", vp7)
v.check("23-04.7a1", vp7)
v.check("23-04.7b", (40 - 45) / 85)
v.check("23-04.7c", m7[0] / vp7 - 1)
v.check("23-04.7d", m7[0])
v.check("23-04.7e1", m7[0] - vp7)
v.check("23-04.7e2", (m7[0] - vp7) * (40 - 45) / 85)
v.check("23-04.7e3", m7[1] - m7[0])
v.check("23-04.7e", m7[1])
v.check("23-04.7f", m7[-1])
v.check("23-04.7x", 100 * (m7[0] / m7[-1] - 1))
d42 = math.sqrt(4.2) / 3.00e8 * 1e-3  # the problems state c = 3.00e8 m/s
v.check("23-04.8a", d42 * 1e12)
v.check("23-04.8b0", 8 * 14)
v.check("23-04.8b", 112 * d42 * 1e12)
v.check("23-04.8b1", 112 * d42 * 1e12)
v.check("23-04.8c", 112 * d42 * 8.8e9)
ui128 = 1 / 12.8e9
h9 = pulse_cursors(ui128, 60e-12, 60)
v.check("23-04.9a", ui128 * 1e12)
v.check("23-04.9b", sum(h9[1:]))
v.check("23-04.9c", h9[0])
v.check("23-04.9d", h9[1])
v.check("23-04.9e", brute_eye(h9, 2))
v.check("23-04.9f", brute_eye(h9, 2, taps_removed=1))
v.check("23-04.9g", h9[0])
v.check("23-04.9h", 1 / optimize.brentq(lambda t: brute_eye(pulse_cursors(t, 60e-12, 60), 2), 10e-12, 200e-12,
                                        xtol=1e-18) / 1e9)
v.check("23-04.10a", 32 / 1.5)
v.check("23-04.10b", 32 / 1.5 / 2)
v.check("23-04.10c", optimize.brentq(lambda al: eye_amp(al, 16, 2) - eye_amp(al, 32 / 3, 3), 0.01, 5))
v.check("23-04.10d", 28 / 1.5 / 2)
units = {"a": (64 * 6.4e9 / 8, 64), "b": (16 * 9.6e9 / 8, 16), "c": (32 * 32e9 / 8, 32)}
pins_k = {"a": "d", "b": "e", "c": "f"}
n_units = {}
for k, (bw, w) in units.items():
    v.check(f"23-04.11{k}0", 1e12 / bw)
    n = math.ceil(1e12 / bw)
    n_units[k] = n
    v.check(f"23-04.11{k}", n)
    v.check(f"23-04.11{pins_k[k]}", n * w)
v.check("23-04.11c1", 32 * 32e9 / 8 / 1e9)
v.check("23-04.11g", n_units["c"] * 32 / 8)
v.check("23-04.11h", n_units["a"] * 64)
v.check("23-04.11x", (n_units["a"] * 64) / (n_units["c"] * 32 / 8))
v.check("23-04.11y", (n_units["a"] * 64) / (n_units["c"] * 32))
e_act = 8192 * 40e-15 * 1.0 ** 2 / 2
e_pod = e0 * 0.5
e_lv = p_lv * ui96 * 0.5
v.check("23-04.12a", e_act / 128 * 1e12)
v.check("23-04.12b", (e_act / 128 + e_pod) * 1e12)
v.check("23-04.12c", (e_act / 8192 + e_pod) * 1e12)
v.check("23-04.12d", (e_act / 128 + e_lv) * 1e12)
v.check("23-04.12e", (e_act / 8192 + e_lv) * 1e12)
v.check("23-04.12f", 100 * (e_act / 128) / (e_act / 128 + e_pod))
v.check("23-04.12x", (e_act / 8192 + e_pod) / (e_act / 8192 + e_lv))
v.check("23-04.13a0", 2 * ui64 * 1e12)
v.check("23-04.13a", 2 * ui64 / 128 * 1e12)
v.check("23-04.13b", (2 * ui64 / 128) / 6.67e-12)
v.check("23-04.14a", pam_eye_rc(48e9, 20e-12, 2, 1))
v.check("23-04.14b", pam_eye_rc(48e9, 20e-12, 3, 1.5))
v.check("23-04.14c", pam_eye_rc(48e9, 20e-12, 4, 2))
x_close = {m: optimize.brentq(lambda x, m=m, b=b: (1 - math.exp(-b * x)) / (m - 1) - math.exp(-b * x), 0.1, 3)
           for m, b in ((2, 1), (3, 1.5), (4, 2))}
v.check("23-04.14d", x_close[2])
v.check("23-04.14e", x_close[3])
v.check("23-04.14f", x_close[4])
v.check("23-04.14g", 0.5 - 2 * 0.5 + 1.5 * 0.5 ** 1.5)
v.check("23-04.14g1", 0.5 ** 1.5)
v.check("23-04.14h", (8 / 9) ** 2)
v.check("23-04.14i", 3 ** (-2 / 3))
v.check("23-04.14j", 1e12 / 48e9)
xs = np.linspace(0.05, 6, 600)
nrz = 1 - 2 * np.exp(-xs)
pam3 = (1 - np.exp(-1.5 * xs)) / 2 - np.exp(-1.5 * xs)
pam4 = (1 - np.exp(-2 * xs)) / 3 - np.exp(-2 * xs)
open_any = (nrz > 0) | (pam3 > 0) | (pam4 > 0)
v.assert_true("NRZ eye >= PAM3 and PAM4 eyes wherever any eye is open (first-order channel)",
              bool(np.all((nrz[open_any] >= pam3[open_any] - 1e-12) & (nrz[open_any] >= pam4[open_any] - 1e-12))))

# ---------------------------------------------------------------- audit additions
v.check("Txt 23-04.m", (1.1 / 0.5) ** 2)
v.check("Txt 23-04.n", 80 / 74)
v.check("Txt 23-04.n1", 80 / 74)
v.assert_true("4.84 x 80/74 x 1.5 reproduces the 7.85 ratio", abs((1.1 / 0.5) ** 2 * 80 / 74 * 1.5 - 7.85) < 0.01)
v.check("Txt 23-04.o", 700 / 6.67)
v.check("Txt 23-04.o1", 700 / 6.67 / 10)
v.check("Txt 23-04.p", 240 / 7)
v.check("Txt 23-04.q", 240 / 5)
v.check("Txt 23-04.r", 240)

sys.exit(v.finish())
