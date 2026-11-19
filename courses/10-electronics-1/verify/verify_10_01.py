#!/usr/bin/env python3
"""Verify every number in chapter 10-01 (diodes and diode circuits), its solutions and lab.

Independent routes:
- diode circuits by root finding on the full exponential, cross-checked with the Lambert W closed form;
  the hand iterations (fixed point and Newton) replayed step by step;
- diode sharing in the ORing example by solving the bus voltage with both exponential diodes conducting;
- small-signal resistance by numerically differentiating the exponential at the bias point;
- rectifiers by integrating the circuit's differential equation through several cycles with a stiff
  diode (on-resistance extrapolated to zero) until periodic, then measuring ripple, conduction angle and
  diode currents from the waveforms, not from the closed-form approximations, which are checked separately;
- the Zener regulator by root finding on its nodal equation at each corner, with the derivatives that
  define line and load regulation taken numerically;
- the limiter by root finding; clamp and doubler by simulating the circuits until they settle.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import lambertw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-01", COURSE / "chapters" / "10-01-diodes-and-diode-circuits.md",
                        COURSE / "solutions" / "10-01-solutions.md",
                        COURSE / "labs" / "10-01-lab" / "README.md")

K = 1.380649e-23
QE = 1.602176634e-19
VT = K * 300 / QE                      # 25.852 mV
IS = 1e-15


def diode_i(vd, Is=IS, n=1.0):
    return Is * math.expm1(vd / (n * VT))


def solve_series(Vdd, R, Is=IS, n=1.0):
    """Operating point of a diode in series with R across Vdd, by root finding."""
    vd = brentq(lambda x: diode_i(x, Is, n) - (Vdd - x) / R, -1, min(Vdd, 2.0), xtol=1e-15)
    return vd, (Vdd - vd) / R


def ddx(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


# ------------------------------------------------------------------ theory values
v1 = brentq(lambda x: diode_i(x) - 1e-4, 0, 1, xtol=1e-15)
v2 = brentq(lambda x: diode_i(x) - 1e-3, 0, 1, xtol=1e-15)
v.check("T 10-01.a", v1)
v.check("T 10-01.b", v2)
rD = (v2 - v1) / 0.9e-3
VD0 = v2 - rD * 1e-3
v.check("T 10-01.c", rD)
v.check("T 10-01.d", VD0)
# 10% small-signal limit: amplitude where the quadratic term is 10% of the linear one
v.check("T 10-01.e", brentq(lambda a: (a / VT) ** 2 / 2 / (a / VT) - 0.1, 1e-6, 0.1) * 1e3)
v.check("T 10-01.f", 5.1 - 0.049 * 7)
v.check("T 10-01.g", brentq(lambda dv: math.exp(dv / VT) - 2, 0, 0.1) * 1e3)
v.check("T 10-01.h", 7 / 0.2)

# ------------------------------------------------------------------ Example 1
V1, R1 = 5.0, 4.3e3
v.check("Ex 10-01.1a", (V1 - 0.7) / R1 * 1e3)
vd1, id1 = solve_series(V1, R1)
v.check("Ex 10-01.1b", vd1)
v.check("Ex 10-01.1c", id1 * 1e3)
idw = VT / R1 * lambertw(R1 * IS / VT * math.exp((V1 + R1 * IS) / VT)).real - IS
v.assert_true("Lambert W reproduces the root-finding current", abs(idw / id1 - 1) < 1e-10)
v.check("Ex 10-01.1d", ((V1 - 0.7) / R1 / id1 - 1) * 100)
x = 0.7
fp = []
for _ in range(2):
    x = VT * math.log((V1 - x) / R1 / IS + 1)
    fp.append(x)
v.check("Ex 10-01.1e", fp[0])
v.check("Ex 10-01.1f", fp[1])
x = 0.7
nt = []
for _ in range(3):
    f = diode_i(x) - (V1 - x) / R1
    x -= f / ddx(lambda y: diode_i(y) - (V1 - y) / R1, x)
    nt.append(x)
v.check("Ex 10-01.1g", nt[0])
v.check("Ex 10-01.1h", nt[1])
v.check("Ex 10-01.1i", nt[2])
ipwl = brentq(lambda i: VD0 + rD * i - (V1 - R1 * i), 0, 1)
v.check("Ex 10-01.1j", ipwl * 1e3)
v.check("Ex 10-01.1k", VD0 + rD * ipwl)

# ------------------------------------------------------------------ Example 2 (ORing)
v.check("Ex 10-01.2a", 12.0 - 0.7)
v.check("Ex 10-01.2b", 11.5 - (12.0 - 0.7))
# both exponential diodes into a 5 A load: solve the bus voltage
Ip = IS                                                           # the ratio does not depend on I_S once both exponentials dominate
bus = brentq(lambda vb: diode_i(12.0 - vb, Ip) + diode_i(11.5 - vb, Ip) - 5.0, 9, 12)
ratio = diode_i(11.5 - bus, Ip) / diode_i(12.0 - bus, Ip)
v.check("Ex 10-01.2c", ratio)
v.check("Ex 10-01.2d", diode_i(11.5 - bus, Ip) * 1e9)
v.check("Ex 10-01.2e", 5 * 0.7)
v.check("Ex 10-01.2f", 5 * 0.45)
v.check("Ex 10-01.2g", 5 * 5e-3 * 1e3)
v.check("Ex 10-01.2h", 5**2 * 5e-3)
v.check("Ex 10-01.2i", 11.5 - 0.7)
v.check("Ex 10-01.2j", 20e-3 / 5 * 1e3)
v.check("Ex 10-01.2k", 50e-3 / 5 * 1e3)

# ------------------------------------------------------------------ Example 3 (small signal)
for k_, I0 in (("a", 1e-4), ("b", 1e-3)):
    Vq = brentq(lambda x: diode_i(x) - I0, 0, 1, xtol=1e-15)
    rd = 1 / ddx(diode_i, Vq, 1e-7)
    v.check(f"Ex 10-01.3{k_}", rd)
rd_a, rd_b = VT / 1e-4, VT / 1e-3
ga, gb = rd_a / (1e3 + rd_a), rd_b / (1e3 + rd_b)
v.check("Ex 10-01.3c", ga)
v.check("Ex 10-01.3d", 20 * math.log10(ga))
v.check("Ex 10-01.3e", gb)
v.check("Ex 10-01.3f", 20 * math.log10(gb))
v.check("Ex 10-01.3g", 20 * math.log10(ga / gb))
v.check("Ex 10-01.3h", 10 * ga)
v.assert_true("second-order error near 4% at 2.05 mV", abs((10 * ga * 1e-3) / (2 * VT) - 0.04) < 0.003)


# ------------------------------------------------------------------ rectifier simulator
def rectifier(vs, VD, C, R=None, IL=None, f=60.0, full=False, cycles=4):
    """Integrate dv/dt = (i_D - i_load)/C with a stiff constant-drop diode; extrapolate R_on -> 0.

    Returns peak-to-peak ripple, mean output, minimum output, peak diode current, conduction angle (degrees
    of the 60 Hz cycle per conduction interval), turn-off angle after the source peak, and the average
    diode current during conduction."""
    w, T = 2 * math.pi * f, 1 / f
    src = (lambda t: abs(vs * math.cos(w * t))) if full else (lambda t: vs * math.cos(w * t))
    out = []
    for Ron in (2e-4, 1e-4):
        def iD(t, y, Ron=Ron):
            return max(0.0, (src(t) - VD - y) / Ron)

        def rhs(t, y, Ron=Ron):
            il = y[0] / R if R else IL
            return [(iD(t, y[0]) - il) / C]

        sol = solve_ivp(rhs, (0, cycles * T), [vs - VD], method="Radau", max_step=T / 4000,
                        rtol=1e-10, atol=1e-12, dense_output=True)
        half = T / 2 if full else T
        tt = np.linspace((cycles - 1) * T, (cycles - 1) * T + half, 200001)
        vv = sol.sol(tt)[0]
        ii = np.array([iD(t, y) for t, y in zip(tt, vv)])
        on = ii > 1e-9
        # conduction interval: the on-region surrounding the source peak at t = (cycles - 1) T
        ph = (tt - (cycles - 1) * T) * w                        # phase in radians from the peak
        ph = np.where(ph > (math.pi / 2 if full else math.pi), ph - (math.pi if full else 2 * math.pi), ph)
        cond = on.mean() * (180 if full else 360)
        toff = ph[on & (ph > 0)].max() if np.any(on & (ph > 0)) else 0.0
        iav = (ii[on].mean())
        out.append(np.array([vv.max() - vv.min(), vv.mean(), vv.min(), ii.max(), cond, math.degrees(toff), iav]))
    return 2 * out[1] - out[0]                                  # linear extrapolation to R_on = 0


# ------------------------------------------------------------------ Example 4 (half-wave)
Vs4, f4, R4, C4 = 12.0, 60.0, 1e3, 470e-6
Vp4 = Vs4 - 0.7
IL4 = Vp4 / R4
Vr4 = IL4 / (f4 * C4)
v.check("Ex 10-01.4a", Vp4)
v.check("Ex 10-01.4b", IL4 * 1e3)
v.check("Ex 10-01.4c", Vr4)
v.check("Ex 10-01.4d", Vp4 - Vr4 / 2)
wdt4 = brentq(lambda th: Vp4 * (1 - th**2 / 2) - (Vp4 - Vr4), 0, 1)       # small-angle crossing
v.check("Ex 10-01.4e", wdt4)
v.check("Ex 10-01.4f", math.degrees(wdt4))
v.check("Ex 10-01.4g", wdt4 / (2 * math.pi) * 100)
v.check("Ex 10-01.4h", IL4 * (1 / f4) / (wdt4 / (2 * math.pi * f4)) * 1e3)
v.check("Ex 10-01.4i", (IL4 + C4 * 2 * math.pi * f4 * Vp4 * wdt4) * 1e3)          # small-angle sin, as in §3.6
r4 = rectifier(Vs4, 0.7, C4, R=R4)
v.check("Ex 10-01.4j", r4[5])
v.check("Ex 10-01.4k", r4[0])
v.check("Ex 10-01.4l", r4[4])
v.check("Ex 10-01.4m", r4[3] * 1e3)
v.check("Ex 10-01.4n", r4[1])
v.check("Ex 10-01.4o", (Vr4 / r4[0] - 1) * 100)
r4b = rectifier(Vs4, 0.7, C4, R=500.0)
v.check("T 10-01.i", r4b[0] / r4[0])
v.check("T 10-01.j", r4b[3] / r4[3])

# ------------------------------------------------------------------ Example 5 (bridge)
Vs5 = 9 * math.sqrt(2)
Vp5 = Vs5 - 1.4
IL5, C5, f5 = 0.5, 4700e-6, 60.0
v.check("Ex 10-01.5a", Vs5)
v.check("Ex 10-01.5b", Vp5)
v.check("Ex 10-01.5c", IL5 / (2 * f5 * 1.0) * 1e6)
Vr5 = IL5 / (2 * f5 * C5)
v.check("Ex 10-01.5d", Vr5)
v.check("Ex 10-01.5e", Vp5 - Vr5)
wdt5 = math.sqrt(2 * Vr5 / Vp5)
v.check("Ex 10-01.5f", math.degrees(wdt5))
v.check("Ex 10-01.5g", IL5 * (1 / (2 * f5)) / (wdt5 / (2 * math.pi * f5)))
v.check("Ex 10-01.5h", IL5 * (1 + math.pi * math.sqrt(2 * Vp5 / Vr5)))
v.check("Ex 10-01.5i", Vs5 - 0.7)
v.check("Ex 10-01.5j", IL5 / 2)
r5 = rectifier(Vs5, 1.4, C5, IL=IL5, full=True)
v.check("Ex 10-01.5k", r5[5])
v.check("Ex 10-01.5l", r5[0])
v.check("Ex 10-01.5m", r5[2])
v.check("Ex 10-01.5n", r5[4])
v.check("Ex 10-01.5o", r5[3])
v.check("Ex 10-01.5p", r5[6])
v.check("Ex 10-01.5q", (Vr5 / r5[0] - 1) * 100)


# ------------------------------------------------------------------ Example 6 (Zener)
def zener_vo(VS, IL, R, VZ0=5.1 - 0.049 * 7, rz=7.0):
    return brentq(lambda vo: (VS - vo) / R - IL - (vo - VZ0) / rz, 0, VS)


VZ0 = 5.1 - 0.049 * 7
v.check("Ex 10-01.6a", VZ0 + 7 * 5e-3)
v.check("Ex 10-01.6b", brentq(lambda R: zener_vo(8.0, 0.05, R) - (VZ0 + 7 * 5e-3), 1, 200))
vo = zener_vo(8.0, 0.05, 56)
v.check("Ex 10-01.6c", vo)
v.check("Ex 10-01.6d", (vo - VZ0) / 7 * 1e3)
vo = zener_vo(10.0, 0.0, 56)
v.check("Ex 10-01.6e", (vo - VZ0) / 7 * 1e3)
v.check("Ex 10-01.6f", vo)
v.check("Ex 10-01.6g", vo * (vo - VZ0) / 7 * 1e3)
v.check("Ex 10-01.6h", max((10.0 - zener_vo(10.0, il, 56)) ** 2 / 56 for il in np.linspace(0, 0.05, 51)) * 1e3)
v.check("Ex 10-01.6i", ddx(lambda s: zener_vo(s, 0.025, 56), 9.0, 1e-3) * 1e3)
v.check("Ex 10-01.6j", ddx(lambda i: zener_vo(9.0, i, 56), 0.025, 1e-4))
v.check("Ex 10-01.6k", (zener_vo(10.0, 0.05, 56) - zener_vo(8.0, 0.05, 56)) * 1e3)
v.check("Ex 10-01.6l", (zener_vo(9.0, 0.05, 56) - zener_vo(9.0, 0.0, 56)) * 1e3)
vo = zener_vo(9.0, 0.025, 56)
v.check("Ex 10-01.6m", vo)
v.check("Ex 10-01.6n", vo * 0.025 / (9.0 * (9.0 - vo) / 56) * 100)
v.check("Ex 10-01.6o", (zener_vo(9.0, 0.0, 56, VZ0=2.495, rz=0.2) - zener_vo(9.0, 0.05, 56, VZ0=2.495, rz=0.2)) * 1e3)

# ------------------------------------------------------------------ Example 7 (limiter, clamp, doubler)
for k_, vin in (("a", 0.5), ("b", 2.0), ("c", 5.0)):
    v.check(f"Ex 10-01.7{k_}", brentq(lambda vo: 2 * IS * math.sinh(vo / VT) - (vin - vo) / 1e3, 0, vin, xtol=1e-14))
# clamp and doubler with constant-drop diodes (stiff switch), simulated until settled
fq, Vp7, Cc = 1e3, 5.0, 1e-6


def clamp_doubler(cycles=60, Ron=1.0):
    w = 2 * math.pi * fq

    def rhs(t, y):
        vc1, vc2 = y                                    # clamp capacitor voltage (input side minus node x), doubler output
        vin = Vp7 * math.sin(w * t)
        vx = vin - vc1                                  # clamped node
        i1 = max(0.0, (-0.7 - vx) / Ron)                # clamp diode: anode at ground, cathode at node x
        i2 = max(0.0, (vx - 0.7 - vc2) / Ron)           # doubler diode into the output capacitor
        return [(i2 - i1) / Cc, i2 / Cc]

    sol = solve_ivp(rhs, (0, cycles / fq), [0.0, 0.0], method="Radau", max_step=1 / fq / 2000, rtol=1e-8,
                    atol=1e-10, dense_output=True)
    tt = np.linspace((cycles - 1) / fq, cycles / fq, 20001)
    y = sol.sol(tt)
    vx = Vp7 * np.sin(2 * math.pi * fq * tt) - y[0]
    return y[0][-1], vx.min(), vx.max(), y[1][-1]


vc1, vmin, vmax, vdbl = clamp_doubler()
v.check("Ex 10-01.7d", -vc1)        # the capacitor holds 4.3 V, input side negative
v.check("Ex 10-01.7e", vmin)
v.check("Ex 10-01.7f", vmax)
v.check("Ex 10-01.7g", vdbl)

# ------------------------------------------------------------------ solutions
for (ka, kb, kc, kd), Vdd in ((("a", "b", "c", "d"), 3.0), (("e", "f", "g", "h"), 1.0)):
    vd_, id_ = solve_series(Vdd, 1e3, 1e-14)
    v.check(f"10-01.1{ka}", (Vdd - 0.7) / 1e3 * 1e3)
    v.check(f"10-01.1{kb}", vd_)
    v.check(f"10-01.1{kc}", id_ * 1e3)
    v.check(f"10-01.1{kd}", ((Vdd - 0.7) / 1e3 / id_ - 1) * 100)
v.check("10-01.2a", 3.3 - 0.7)
v.check("10-01.2b", 0.0 - (3.3 - 0.7))
v.check("10-01.2c", 3.0 - (3.3 - 0.7))
busq = brentq(lambda vb: diode_i(3.3 - vb) + diode_i(3.0 - vb) - vb / 1e4, 0, 3.3, xtol=1e-15)
v.check("10-01.2d", diode_i(3.0 - busq) / diode_i(3.3 - busq))
for k_, n_ in (("a", 1), ("b", 2)):
    Vq = brentq(lambda x: diode_i(x, IS, n_) - 0.5e-3, 0, 2, xtol=1e-15)
    v.check(f"10-01.3{k_}", 1 / ddx(lambda x: diode_i(x, IS, n_), Vq, 1e-7))
v.check("10-01.3c", 1e-3 / (VT / 0.5e-3) * 1e6)
v.check("10-01.3d", 1e-3 / (2 * VT / 0.5e-3) * 1e6)
v.check("10-01.4a", 0.650 - 0.002 * 60)
v.check("10-01.4b", 0.650 + 0.002 * 65)
VT85 = K * 358.15 / QE
v.check("10-01.4c", VT85 * math.log(10) * 1e3)
v.check("10-01.4d", math.exp(0.120 / VT85))
Vs_, IL_ = 10.0, 0.1
v.check("10-01.5a", Vs_ - 0.7)
v.check("10-01.5b", IL_ / 60 * 1e6)
Vr_ = IL_ / (60 * 2200e-6)
v.check("10-01.5c", Vr_)
v.check("10-01.5d", 9.3 - Vr_)
w5 = brentq(lambda th: 9.3 * (1 - th**2 / 2) - (9.3 - Vr_), 0, 1)
v.check("10-01.5e", math.degrees(w5))
v.check("10-01.5f", IL_ + 2200e-6 * 2 * math.pi * 60 * 9.3 * w5)
v.check("10-01.5g", 2 * Vs_ - 0.7)
v.check("10-01.6a", 1.0 / (2 * 60 * 0.5) * 1e6)
v.check("10-01.6b", 12 + 0.8)
v.check("10-01.6c", 2 * 12.8 - 0.8)
v.check("10-01.6d", 12 + 1.6)
v.check("10-01.6e", 13.6 - 0.8)
rz7, VZ07 = 9.0, 12 - 0.021 * 9
v.check("10-01.7a", VZ07)
v.check("10-01.7b", VZ07 + rz7 * 5e-3)
v.check("10-01.7c", brentq(lambda R: zener_vo(16.0, 0.030, R, VZ07, rz7) - (VZ07 + rz7 * 5e-3), 10, 500))
vo7 = zener_vo(16.0, 0.030, 110, VZ07, rz7)
v.check("10-01.7d", vo7)
v.check("10-01.7e", (vo7 - VZ07) / rz7 * 1e3)
vo7 = zener_vo(20.0, 0.0, 110, VZ07, rz7)
v.check("10-01.7f", (vo7 - VZ07) / rz7 * 1e3)
v.check("10-01.7g", vo7 * (vo7 - VZ07) / rz7)
v.check("10-01.7h", max((20.0 - zener_vo(20.0, il, 110, VZ07, rz7)) ** 2 / 110 for il in np.linspace(0, 0.03, 31)))
v.check("10-01.8a", ddx(lambda vs: zener_vo(vs, 0.03, 110, VZ07, rz7), 18.0, 1e-3) * 1e3)
v.check("10-01.8b", ddx(lambda il: zener_vo(18.0, il, 110, VZ07, rz7), 0.015, 1e-4))
v.check("10-01.8c", (zener_vo(20.0, 0.03, 110, VZ07, rz7) - zener_vo(16.0, 0.03, 110, VZ07, rz7)) * 1e3)
v.check("10-01.8d", (zener_vo(18.0, 0.03, 110, VZ07, rz7) - zener_vo(18.0, 0.0, 110, VZ07, rz7)) * 1e3)
v.check("10-01.9a", 2.0 + 0.7)
v.check("10-01.9b", brentq(lambda x: diode_i(x - 2.0) - (5 - x) / 1e3, 2.0, 5.0, xtol=1e-14))
v.check("10-01.10a", -0.7)
v.check("10-01.10b", 3 + (3 - 0.7))
v.check("10-01.10c", 3 + (3 - 0.7) - 0.7)
v.check("10-01.10d", 3 + (3 - 0.3) - 0.3)
iw = VT / 1e3 * lambertw(1e3 * 1e-14 / VT * math.exp((1.0 + 1e3 * 1e-14) / VT)).real - 1e-14
v.check("10-01.11a", iw * 1e3)
v.check("10-01.11b", VT / (1e3 * solve_series(3.0, 1e3, 1e-14)[1]))
v.check("10-01.11c", VT / (1e3 * solve_series(1.0, 1e3, 1e-14)[1]))
r12 = rectifier(10.0, 0.7, 2200e-6, IL=0.1)
v.check("10-01.12a", r12[5])
v.check("10-01.12b", r12[0])
v.check("10-01.12c", r12[4])
v.check("10-01.12d", r12[3])
v.check("10-01.12e", r12[6])
v.check("10-01.12f", (Vr_ / r12[0] - 1) * 100)
v.check("10-01.13a", 20e-3 / 3 * 1e3)
v.check("10-01.13b", 50e-3 / 3 * 1e3)
v.check("10-01.13c", 3**2 * 0.010)
v.check("10-01.13d", 3 * 0.5)
v.check("10-01.13e", 3 * 0.8)
v.check("10-01.13f", 6 * 0.010 * 1e3)
v.check("10-01.13g", 6**2 * 0.010)
tau14 = 50 * 12e-12
v.check("10-01.14a", tau14 * 1e9)
v.check("10-01.14b", brentq(lambda fr: abs(1 / (1 + 2j * math.pi * fr * tau14)) - 1 / math.sqrt(2), 1e6, 1e10) / 1e6)
tr = brentq(lambda t: 1 - math.exp(-t / tau14) - 0.9, 0, 1e-8) - brentq(lambda t: 1 - math.exp(-t / tau14) - 0.1, 0, 1e-8)
v.check("10-01.14c", tr * 1e9)
v.check("10-01.14d", tr / 2.5e-9)

# ------------------------------------------------------------------ lab
IS_R, N_R = 10e-9, 1.9                                           # the lab's course rectifier diode


def rect_exp(R=1e3, C=470e-6, f=60.0, cycles=4):
    w, T = 2 * math.pi * f, 1 / f
    src = lambda t: 12.0 * math.cos(w * t)
    iD = lambda t, y: IS_R * math.expm1((src(t) - y) / (N_R * VT))
    rhs = lambda t, y: [(iD(t, y[0]) - y[0] / R) / C]
    jac = lambda t, y: [[(-IS_R / (N_R * VT) * math.exp((src(t) - y[0]) / (N_R * VT)) - 1 / R) / C]]
    sol = solve_ivp(rhs, (0, cycles * T), [11.15], method="Radau", jac=jac, max_step=T / 4000, rtol=1e-10,
                    atol=1e-12, dense_output=True)
    tt = np.linspace((cycles - 1) * T, cycles * T, 200001)
    vv = sol.sol(tt)[0]
    ii = np.array([iD(t, y) for t, y in zip(tt, vv)])
    return vv.max() - vv.min(), vv.mean(), ii.max()


rl = rect_exp()
v.check("Lab 10-01.a", rl[0])
v.check("Lab 10-01.b", rl[1])
v.check("Lab 10-01.c", rl[2] * 1e3)
v.check("Lab 10-01.d", r4b[0])
v.check("Lab 10-01.e", r4b[3] * 1e3)
v.check("Lab 10-01.f", zener_vo(10.0, 0.05, 56))
v.check("Lab 10-01.g", (1 - rl[2] / r4[3]) * 100)
v.check("Lab 10-01.h", brentq(lambda vs: (vs - zener_vo(vs, 0.06, 56)) / 56 - 0.06 - 1e-12, 5, 12))
v.check("Lab 10-01.i", N_R * VT * math.log(rl[2] / IS_R + 1))

# ------------------------------------------------------------------ practitioner values (quoted data sheets, R-176)
for k_, val in (("P 10-01.a", 4), ("P 10-01.b", 4), ("P 10-01.c", 15), ("P 10-01.d", 0.45), ("P 10-01.e", 1),
                ("P 10-01.f", 5), ("P 10-01.g", 2.495), ("P 10-01.h", 0.2), ("P 10-01.i", 20), ("P 10-01.j", 0.75),
                ("P 10-01.k", 12), ("P 10-01.l", 30), ("P 10-01.m", 10), ("P 10-01.n", 100)):
    v.check(k_, val)

v.finish()
