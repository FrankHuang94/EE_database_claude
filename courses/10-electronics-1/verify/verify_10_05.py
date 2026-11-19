#!/usr/bin/env python3
"""Verify every number in chapter 10-05 (amplifier fundamentals), its solutions and lab.

Independent routes:
- every cascade is solved by nodal analysis (numpy.linalg.solve) with each stage's output written as a
  voltage-controlled current source A/R_o in parallel with R_o, not by multiplying divider ratios;
- resistance measurements are inverted by root finding on a simulated Thevenin source;
- swing from the exponential transistor's transfer characteristic and the AC load line; class-A and
  class-B limits by numerical optimization and integration;
- the bilateral two-port by solving its y-parameter equations with source and load attached;
- corners by root finding on the magnitude of the complex response.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.special import iv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-05", COURSE / "chapters" / "10-05-amplifier-fundamentals.md",
                        COURSE / "solutions" / "10-05-solutions.md",
                        COURSE / "labs" / "10-05-lab" / "README.md")

VT = 1.380649e-23 * 300 / 1.602176634e-19


def db(x):
    return 20 * math.log10(abs(x))


def chain(stages, r_sig, r_load):
    """Nodal solution of source -> stages -> load; returns v_out / v_sig.

    Node k (k = 0..n) is the input of stage k (node n is the output). Stage k injects (A_k/R_ok) v_k into
    node k+1 through its Norton form, with R_ok from node k+1 to ground.
    """
    n = len(stages)
    G = np.zeros((n + 1, n + 1))
    I = np.zeros(n + 1)
    G[0, 0] += 1 / r_sig
    I[0] = 1 / r_sig                                   # Norton form of a 1 V source behind r_sig
    for k, (r_i, a, r_o) in enumerate(stages):
        G[k, k] += 1 / r_i
        G[k + 1, k + 1] += 1 / r_o
        G[k + 1, k] -= a / r_o                         # injected current a v_k / r_o moved to the left side
    G[n, n] += 1 / r_load
    return np.linalg.solve(G, I)


# ------------------------------------------------------------------ theory
v.check("T 10-05.a", math.sqrt(1e-3 * 50))
v.check("T 10-05.b", 10 * math.log10(2))
v.check("T 10-05.c", db(2))
v.check("T 10-05.d", db(1 / math.sqrt(2)))


def class_a_eff(vq_frac, vcc=10.0, r=1e3):
    """Resistive class A: bias V_C = vq_frac*V_CC; swing limited by saturation (0 V) and cutoff (V_CC)."""
    vc = vq_frac * vcc
    iq = (vcc - vc) / r
    swing = min(vc, vcc - vc)
    return (swing ** 2 / (2 * r)) / (vcc * iq)


best = minimize_scalar(lambda q: -class_a_eff(q), bounds=(0.05, 0.95), method="bounded", options={"xatol": 1e-10})
v.check("T 10-05.e", -best.fun * 100)
v.check("T 10-05.f", -best.fun * 100 * 0.1)          # P_L/10 at fixed P_DC
# transformer/inductor coupled: collector swings about V_CC, from 0 to 2V_CC; I_Q = V_CC/R sets the downward swing
eta_l = minimize_scalar(lambda iq: -(min(10.0, iq * 1e3) ** 2 / (2 * 1e3)) / (10.0 * iq),
                        bounds=(1e-4, 0.1), method="bounded", options={"xatol": 1e-12})
v.check("T 10-05.g", -eta_l.fun * 100)
p_load = quad(lambda t: (math.sin(t)) ** 2, 0, 2 * math.pi)[0] / (2 * math.pi)    # V^2/R units with V = V_CC
p_supply = quad(lambda t: abs(math.sin(t)), 0, 2 * math.pi)[0] / (2 * math.pi)
v.check("T 10-05.h", p_load / p_supply * 100)
v.check("T 10-05.i", 1e-3 * 10 ** (30 / 10))

# ------------------------------------------------------------------ Example 1
vi, vo, ri, rl = 10e-3, 1.0, 10e3, 1e3
ap = (vo * vo / rl) / (vi * vi / ri)
v.check("Ex 10-05.1a", db(vo / vi))
v.check("Ex 10-05.1b", db((vo / rl) / (vi / ri)))
v.check("Ex 10-05.1c", ap)
v.check("Ex 10-05.1d", 10 * math.log10(ap))
v.check("Ex 10-05.1e", 10 * math.log10((vi * vi / ri) / 1e-3))
v.check("Ex 10-05.1f", 10 * math.log10((vo * vo / rl) / 1e-3))

# ------------------------------------------------------------------ Example 2
x = chain([(10e3, 200, 2e3)], 5e3, 3e3)
v.check("Ex 10-05.2a", x[0])
v.check("Ex 10-05.2b", x[1] / (200 * x[0]))
v.check("Ex 10-05.2c", x[1])
v.check("Ex 10-05.2d", db(x[1]))
v.check("Ex 10-05.2e", db(x[1] / 200))

# ------------------------------------------------------------------ Example 3
gm = 1e-3 / VT
rpi = 100 / gm
ro_dev = 50e3
Ro = 1 / (1 / 5e3 + 1 / ro_dev)
# G_m: short-circuit output current with v_i = 1: the device sinks gm from the output node
gm_sc = -gm
v.check("Ex 10-05.3a", rpi / 1e3)
v.check("Ex 10-05.3b", Ro / 1e3)
v.check("Ex 10-05.3c", gm_sc * 1e3)
v.check("Ex 10-05.3d", gm_sc * Ro)
v.check("Ex 10-05.3e", gm_sc * Ro * rpi / 1e3)
v.check("Ex 10-05.3f", gm_sc * rpi)
x = chain([(rpi, gm_sc * Ro, Ro)], 1e3, 10e3)
v.check("Ex 10-05.3g", x[0])
v.check("Ex 10-05.3h", x[1] / (gm_sc * Ro * x[0]))
v.check("Ex 10-05.3i", x[1])

# ------------------------------------------------------------------ Example 4
ro_from = lambda voc, vl, rl: brentq(lambda r: voc * rl / (rl + r) - vl, 1e-6, 1e9)   # noqa: E731
ri_from = lambda vs, vin, rs: brentq(lambda r: vs * r / (r + rs) - vin, 1e-6, 1e12)   # noqa: E731
v.check("Ex 10-05.4a", ro_from(2.00, 1.60, 1e3))
v.check("Ex 10-05.4b", ri_from(100e-3, 80e-3, 10e3) / 1e3)
r1 = ro_from(2.00, 1.616, 1e3)
r2 = ro_from(2.00, 1.01, 250)
v.check("Ex 10-05.4c", r1)
v.check("Ex 10-05.4d", (r1 / 250 - 1) * 100)
v.check("Ex 10-05.4e", r2)
v.check("Ex 10-05.4f", (r2 / 250 - 1) * 100)
v.assert_true("the 250 ohm test load reads 1.00 V when correct", abs(2 * 250 / 500 - 1.0) < 1e-12)

# ------------------------------------------------------------------ Example 5
g_stage, buf = (10e3, -50, 5e3), (100e3, 1, 50)
x = chain([g_stage, g_stage, buf], 10e3, 100)
v.check("Ex 10-05.5a", x[-1])
v.check("Ex 10-05.5b", db(x[-1]))
x = chain([g_stage, g_stage], 10e3, 100)
v.check("Ex 10-05.5c", x[-1])
v.check("Ex 10-05.5d", db(x[-1]))
v.check("Ex 10-05.5e", db(50 * 50))

# ------------------------------------------------------------------ Example 6: swing from the exponential transfer curve
i_s = 1e-3 / math.exp(0.7 / VT)
vcc, rc, vsat = 10.0, 5e3, 0.2
vbe_q = 0.7
vc_of = lambda vb: vcc - rc * i_s * math.exp(vb / VT)                 # noqa: E731
vq = vc_of(vbe_q)
vb_sat = brentq(lambda vb: vc_of(vb) - vsat, 0.6, 0.9)
down = vq - vc_of(vb_sat)
up = vcc - vq                                                         # cutoff: i_C -> 0, v_C -> V_CC
swing = min(down, up)
v.check("Ex 10-05.6a", swing)
v.check("Ex 10-05.6b", swing ** 2 / (2 * rc) * 1e3)
v.check("Ex 10-05.6c", swing ** 2 / (2 * rc) / (vcc * 1e-3) * 100)
v.check("Ex 10-05.6d", class_a_eff(0.5) * 100)                            # ideal: V_CE,sat = 0, half-supply bias
r_ac = 1 / (1 / rc + 1 / 5e3)
up_ac = 1e-3 * r_ac                                                   # current can fall by at most I_C
swing_ac = min(down, up_ac)
v.check("Ex 10-05.6e", swing_ac)
v.check("Ex 10-05.6f", swing_ac ** 2 / (2 * 5e3) * 1e3)                 # the load sees the collector swing
v.check("Ex 10-05.6g", swing_ac ** 2 / (2 * 5e3) / (vcc * 1e-3) * 100)
v.assert_true("the coupled load limits the upward swing", up_ac < down)

# ------------------------------------------------------------------ Example 7
buf7, g7 = (10e6, 1, 100), (10e3, 40, 1e3)
x = chain([buf7, g7, g7], 100e3, 10e3)
v.check("Ex 10-05.7a", x[1])                                              # buffer output per volt of source
v.check("Ex 10-05.7b", x[2] / x[1])
v.check("Ex 10-05.7c", x[3])
v.check("Ex 10-05.7d", db(x[3]))
y = chain([g7, g7], 100e3, 10e3)
v.check("Ex 10-05.7e", y[-1])
v.check("Ex 10-05.7f", db(y[-1]))


def h_in(f, c, rs=100e3, ri=10e6):
    return abs(ri / (rs + ri + 1 / (1j * 2 * math.pi * f * c)))


mid = 10e6 / 10.1e6
c7 = brentq(lambda c: h_in(0.05, c) - mid / math.sqrt(2), 1e-9, 1e-4)
v.check("Ex 10-05.7g", c7 * 1e9)
v.check("Ex 10-05.7h", brentq(lambda f: h_in(f, 330e-9) - mid / math.sqrt(2), 1e-4, 10) * 1e3)

# ================================================================== solutions
v.check("10-05.1a", 10 * math.log10(2))
v.check("10-05.1b", db(2))
v.check("10-05.1c", 10 * math.log10(1000))
v.check("10-05.1d", db(1 / math.sqrt(2)))
v.check("10-05.1e", brentq(lambda a: db(a) - 26, 1, 100))
v.check("10-05.1f", brentq(lambda p: 10 * math.log10(p / 1e-3) - 10, 1e-6, 1) * 1e3)
v.check("10-05.1g", brentq(lambda u: 10 * math.log10(u * u / 50 / 1e-3), 0.01, 10))

x = chain([(20e3, 50, 500)], 2e3, 1e3)
v.check("10-05.3a", x[-1])
v.check("10-05.3b", db(x[-1]))

gm4, ri4, ro4 = 20e-3, 5e3, 25e3
v.check("10-05.4a", gm4 * ro4)
v.check("10-05.4b", gm4 * ro4 * ri4 / 1e6)
v.check("10-05.4c", gm4 * ri4)
# Norton output directly: node equations with G_m v_i into R_o || R_L
vi4 = ri4 / (ri4 + 1e3)
v.check("10-05.4d", np.linalg.solve([[1 / ro4 + 1 / 25e3]], [gm4 * vi4])[0])

v.check("10-05.5a", ro_from(1.20, 0.90, 600))
v.check("10-05.5b", ri_from(50e-3, 30e-3, 47e3) / 1e3)

X, Y = (1e6, 10, 10e3), (2e3, 100, 100)
v.check("10-05.6a", chain([X, Y], 50e3, 1e3)[-1])
v.check("10-05.6b", chain([Y, X], 50e3, 1e3)[-1])

vdd, rd, vmin = 12.0, 2e3, 1.0
vd = vdd - 3e-3 * rd
sw = min(vd - vmin, 3e-3 * rd)
v.check("10-05.7a", sw)
v.check("10-05.7b", sw ** 2 / (2 * rd) * 1e3)
v.check("10-05.7c", sw ** 2 / (2 * rd) / (vdd * 3e-3) * 100)
i_best = minimize_scalar(lambda i: -min(vdd - i * rd - vmin, i * rd), bounds=(1e-4, 5.5e-3), method="bounded",
                         options={"xatol": 1e-12}).x
sw_b = min(vdd - i_best * rd - vmin, i_best * rd)
v.check("10-05.7d", i_best * 1e3)
v.check("10-05.7e", sw_b)
v.check("10-05.7f", sw_b ** 2 / (2 * rd) * 1e3)
v.check("10-05.7g", sw_b ** 2 / (2 * rd) / (vdd * i_best) * 100)

corner = lambda r, c: brentq(lambda f: abs(r / (r + 1 / (1j * 2 * math.pi * f * c))) - 1 / math.sqrt(2), 1e-3, 1e3)  # noqa: E731
v.check("10-05.8a", corner(30e3, 3.3e-6))
v.check("10-05.8b", corner(24e3, 3.3e-6))
v.check("10-05.8c", brentq(lambda c: corner(24e3, c) - 2.0, 1e-7, 1e-4) * 1e6)

a9 = 10 ** (26 / 20)
vpk = brentq(lambda u: u * u / (2 * 4) - 50, 1, 100)
v.check("10-05.9a", a9)
v.check("10-05.9b", vpk)
v.check("10-05.9c", vpk / math.sqrt(2))
v.check("10-05.9d", vpk / math.sqrt(2) / a9)
v.check("10-05.9e", 50 / 0.9 - 50)
v.check("10-05.9f", 50 / 0.25 - 50)

Y2 = np.array([[0.1e-3, -0.01e-3], [40e-3, 0.05e-3]])
yl = 1 / 10e3


def two_port(rs, gl):
    """Solve [y]{v1, v2} = {i1, i2} with a 1 V source behind rs (rs = 0: driven directly) and load gl."""
    if rs == 0:
        a = np.array([[1, 0], [Y2[1, 0], Y2[1, 1] + gl]])
        b = np.array([1.0, 0.0])
    else:
        a = np.array([[Y2[0, 0] + 1 / rs, Y2[0, 1]], [Y2[1, 0], Y2[1, 1] + gl]])
        b = np.array([1 / rs, 0.0])
    return np.linalg.solve(a, b)


v1, v2 = two_port(0, yl)
v.check("10-05.10a", v2 / v1)
v.check("10-05.10b", 1 / Y2[0, 0] / 1e3)
i1 = Y2[0, 0] * v1 + Y2[0, 1] * v2
v.check("10-05.10c", v1 / i1)
v1o, v2o = two_port(0, 0.0)
v.check("10-05.10d", v1o / (Y2[0, 0] * v1o + Y2[0, 1] * v2o))
v.check("10-05.10e", (1 / Y2[0, 0]) / (1 / Y2[0, 0] + 1e3) * (v2 / v1))
v.check("10-05.10f", two_port(1e3, yl)[1])

B11, G11 = (1e6, 0.95, 200), (5e3, 30, 3e3)
gain = lambda s: chain([B11 if c == "B" else G11 for c in s], 50e3, 2e3)[-1]   # noqa: E731
v.check("10-05.11a", gain("GGG"))
v.check("10-05.11b", db(gain("GGG")))
v.check("10-05.11c", gain("BGGB"))
v.check("10-05.11d", db(gain("BGGB")))
v.check("10-05.11e", gain("GGGB"))
v.check("10-05.11f", db(gain("GGGB")))
v.check("10-05.11g", gain("BGGG"))
v.check("10-05.11h", db(gain("BGGG")))
v.check("10-05.11i", gain("BGBGB"))
best_two = max(gain("".join(p)) for n in range(2, 7) for p in itertools.product("BG", repeat=n) if "".join(p).count("G") == 2)
v.assert_true("no chain with two gain stages (up to 6 stages) reaches 1000", best_two < 1000, f"best {best_two:.1f}")

v.check("10-05.12a", 25 * 0.1)
loss = lambda p: 0.24 + p / 9                         # noqa: E731
v.check("10-05.12b", 1 / (1 + loss(1)) * 100)
v.check("10-05.12c", 10 / (10 + loss(10)) * 100)
v.check("10-05.12d", 1 / (1 + 0.24) * 100)

# ================================================================== lab
r_l = minimize_scalar(lambda r: -(chain([(10e3, 200, 2e3)], 5e3, r)[-1] * 0.01) ** 2 / r, bounds=(10, 1e6),
                      method="bounded", options={"xatol": 1e-6}).x
v.check("Lab 10-05.a", r_l / 1e3)
v.check("Lab 10-05.b", (chain([(10e3, 200, 2e3)], 5e3, r_l)[-1] * 0.01) ** 2 / r_l * 1e3)
v.check("Lab 10-05.c", chain([(10e3, 200, 2e3)], 5e3, r_l)[-1])
st = {"X": X, "Y": Y, "Z": (100e3, 1, 50)}
orders = {"".join(p): chain([st[c] for c in p], 50e3, 1e3)[-1] for p in itertools.permutations("XYZ")}
v.check("Lab 10-05.d", orders["XZY"])
v.check("Lab 10-05.e", orders["YZX"])
v.assert_true("XZY is the best order and YZX the worst",
              max(orders, key=orders.get) == "XZY" and min(orders, key=orders.get) == "YZX")
# Part 3 by direct FFT of the exponential (independent of the Bessel route in the notebook)
N = 8192
th = 2 * np.pi * np.arange(N) / N
ic = 1e-3 * np.exp(10e-3 / VT * np.cos(th))
c = np.fft.rfft(ic) / N
fund = 2 * abs(c[1]) * rc
v.check("Lab 10-05.f", fund)
v.check("Lab 10-05.g", fund ** 2 / (2 * rc) * 1e3)
v.check("Lab 10-05.h", vcc * abs(c[0]) * 1e3)
v.check("Lab 10-05.i", fund ** 2 / (2 * rc) / (vcc * abs(c[0])) * 100)
v.assert_true("FFT agrees with the Bessel series", abs(abs(c[0]) / 1e-3 - iv(0, 10e-3 / VT)) < 1e-12)
a_sat = brentq(lambda a: vcc - rc * 1e-3 * math.exp(a / VT) - vsat, 1e-4, 0.05)
v.check("Lab 10-05.j", a_sat * 1e3)
v.check("Lab 10-05.k", vcc - rc * 1e-3 * math.exp(-a_sat / VT))
mid_gain = chain([buf7, g7, g7], 100e3, 10e3)[-1]
v.check("Lab 10-05.l", mid_gain * h_in(0.1, 330e-9) / mid)
v.check("Lab 10-05.m", mid_gain * h_in(1.0, 330e-9) / mid)

v.finish()
