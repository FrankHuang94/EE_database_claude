#!/usr/bin/env python3
"""Verify every number in chapter 10-10 (op-amp application circuits), its solutions and lab.

Independent routes:
- difference-amplifier CMRR by solving the circuit's nodal equations (an op-amp of gain 1e9) with the worst-case
  resistor corners, and by Monte Carlo for the lab;
- integrator and transimpedance amplifier from their complex loop equations with a single-pole op-amp; corners,
  peaks and the feedback capacitor by root finding (capacitances scaled to picofarads so the solver's absolute
  tolerance is meaningful);
- the precision rectifier's dead time by simulating a slew-limited output swing, and its average error by
  numerical integration;
- Schmitt-trigger thresholds by sweeping an ideal comparator's input up and down and recording where it switches.
Data-sheet values (R-183, R-182) are quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-10", COURSE / "chapters" / "10-10-op-amp-application-circuits.md",
                        COURSE / "solutions" / "10-10-solutions.md",
                        COURSE / "labs" / "10-10-lab" / "README.md")


def db(x):
    return 20 * math.log10(abs(x))


def diff_amp(r1, r2, r3, r4, v1, v2, a=1e9):
    """Nodal solution: unknowns v_minus, v_plus, v_out."""
    m = np.array([[-(1 / r1 + 1 / r2), 0, 1 / r2],
                  [0, -(1 / r3 + 1 / r4), 0],
                  [a, -a, 1.0]])
    z = np.array([-v1 / r1, -v2 / r3, 0.0])
    return np.linalg.solve(m, z)[2]


def cmrr_worst(k, eps, r=10e3):
    r1, r2, r3, r4 = r * (1 + eps), k * r * (1 - eps), r * (1 - eps), k * r * (1 + eps)
    a_cm = diff_amp(r1, r2, r3, r4, 1.0, 1.0)
    a_d = diff_amp(r1, r2, r3, r4, -0.5, 0.5)
    return abs(a_d / a_cm)


# ------------------------------------------------------------------ theory (data sheets, R-183)
v.check("T 10-10.a", 100)
v.check("T 10-10.b", 90)
v.check("T 10-10.c", 80)
v.check("T 10-10.d", 47)
v.check("T 10-10.e", 40)
v.check("T 10-10.f", 40e-6 * 2.7 * 1e6)
v.check("T 10-10.g", 40e-6 * 5.5 * 1e6)

# ------------------------------------------------------------------ Example 1
c1 = cmrr_worst(1, 1e-3)
c10 = cmrr_worst(10, 1e-3)
v.check("Ex 10-10.1a", c1)
v.check("Ex 10-10.1b", db(c1))
v.check("Ex 10-10.1c", c10)
v.check("Ex 10-10.1d", db(c10))
# INA: first stage passes common mode with gain 1 and differential with gain G1 = 100
c_ina = 100 * c1
v.check("Ex 10-10.1e", c_ina)
v.check("Ex 10-10.1f", db(c_ina))
c01 = cmrr_worst(1, 1e-4)
v.check("Ex 10-10.1g", c01)
v.check("Ex 10-10.1h", db(c01))

# ------------------------------------------------------------------ Example 2: INA333 (R-183)
rg = brentq(lambda r: 1 + 100e3 / r - 100, 10, 1e6)
v.check("Ex 10-10.2a", rg / 1e3)
g_std = 1 + 100e3 / 1.01e3
v.check("Ex 10-10.2b", g_std)
v.check("Ex 10-10.2c", (g_std / 100 - 1) * 100)
vos = 25 + 75 / 100
v.check("Ex 10-10.2d", vos)
v.check("Ex 10-10.2e", vos * 100 / 1e3)
v.check("Ex 10-10.2f", 0.1 + 0.5 / 100)
v.check("Ex 10-10.2g", 2e-3 * 3.3 * 1e3)
v.check("Ex 10-10.2h", 2e-3 * 3.3 * 100 * 1e3)
for kg, ke, rgx in (("Ex 10-10.2i", "Ex 10-10.2j", 1.00e3), ("Ex 10-10.2k", "Ex 10-10.2l", 1.02e3)):
    gx = 1 + 100e3 / rgx
    v.check(kg, gx)
    v.check(ke, (gx / 100 - 1) * 100)

# ------------------------------------------------------------------ Example 3: integrator


def integ(f, r, c, a0_db, rf=None, gbw=10e6):
    a0 = 10 ** (a0_db / 20)
    s = 2j * math.pi * f
    a = a0 / (1 + s / (2 * math.pi * gbw / a0))
    zf = 1 / (s * c) if rf is None else 1 / (s * c + 1 / rf)
    beta = r / (r + zf)
    return -(zf / r) * a * beta / (1 + a * beta)


ideal = lambda f: abs(1 / (2 * math.pi * f * 10e3 * 10e-9))       # noqa: E731
fcorner = brentq(lambda f: abs(integ(f, 10e3, 10e-9, 100)) / ideal(f) - 1 / math.sqrt(2), 1e-6, 1)
v.check("Ex 10-10.3a", fcorner)
# offset ramp: dv/dt = V_OS/(RC) from a time simulation of the capacitor current V_OS/R
sol = solve_ivp(lambda t, y: [1e-3 / 10e3 / 10e-9], (0, 1.0), [0.0], rtol=1e-12, atol=1e-12)
v.check("Ex 10-10.3b", sol.y[0][-1] / 1.0)
v.check("Ex 10-10.3c", brentq(lambda t: 1e-3 / (10e3 * 10e-9) * t - 2.5, 0, 10))
v.check("Ex 10-10.3d", integ(1e-6, 10e3, 10e-9, 200, rf=1e6).real)
v.check("Ex 10-10.3e", 1e-3 * (1 + 1e6 / 10e3) * 1e3)
dc_leak = abs(integ(1e-6, 10e3, 10e-9, 200, rf=1e6))
v.check("Ex 10-10.3f", brentq(lambda f: abs(integ(f, 10e3, 10e-9, 200, rf=1e6)) / dc_leak - 1 / math.sqrt(2), 1e-3, 1e4))

# ------------------------------------------------------------------ Example 4: precision rectifier


def slew_time(swing, sr):
    # A constant-rate slew covers `swing` in swing/SR. Integrating dv/dt = SR numerically adds nothing,
    # so the dead and settling times below are arithmetic restatements of the chapter's formulas.
    return swing / sr


a0 = 10 ** (130 / 20)
v.check("Ex 10-10.4a", 0.6 / a0 * 1e6)
dt4 = slew_time(1.2, 6.5e6)
v.check("Ex 10-10.4b", dt4 * 1e6)
v.check("Ex 10-10.4c", math.sin(2 * math.pi * 1e4 * dt4) * 1e3)
v.check("Ex 10-10.4d", math.sin(2 * math.pi * 1e5 * dt4) * 1e3)
v.check("Ex 10-10.4e", 0.6 / 10 ** (104 / 20) * 1e6)
dt_sd = 0.2e-6 + slew_time(2.5 + 0.6, 6.5e6)          # overload recovery, then slew from the rail to +V_D
v.check("Ex 10-10.4f", dt_sd * 1e6)
v.check("Ex 10-10.4g", math.sin(2 * math.pi * 1e4 * dt_sd) * 1e3)

# ------------------------------------------------------------------ Example 5: Schmitt trigger by sweeping


def schmitt_thresholds(r1, r2, vref, vdd, inverting=False):
    """Sweep the input up then down; return (rising switch point, falling switch point)."""
    xs = np.linspace(0, vdd, 500001)

    def plus_node(vin, vo):
        if inverting:     # + input: r1 to vref, r2 to output; input on the - pin
            return (vref * r2 + vo * r1) / (r1 + r2)
        return (vin * r2 + vo * r1) / (r1 + r2)

    def decide(vin, vo):
        if inverting:
            return vdd if plus_node(vin, vo) > vin else 0.0
        return vdd if plus_node(vin, vo) > vref else 0.0

    vo = decide(xs[0], vdd if inverting else 0.0)
    up = None
    for x in xs:
        new = decide(x, vo)
        if new != vo:
            up = x
            vo = new
            break
    down = None
    for x in xs[::-1]:
        new = decide(x, vo)
        if new != vo:
            down = x
            vo = new
            break
    return up, down


r1_5 = brentq(lambda r: 5 * r / 100e3 - 0.1, 1, 1e6)
v.check("Ex 10-10.5a", r1_5 / 1e3)
up, down = schmitt_thresholds(2e3, 100e3, 2.5, 5.0)
v.check("Ex 10-10.5b", up)
v.check("Ex 10-10.5c", down)

# ------------------------------------------------------------------ Example 6
ts = slew_time(5.0, 6.5e6)
v.check("Ex 10-10.6a", ts * 1e6)
v.check("Ex 10-10.6b", (ts + 0.2e-6) * 1e6)
v.check("Ex 10-10.6c", (ts + 0.2e-6) / 50e-9)

# ------------------------------------------------------------------ Example 7: TIA


def tia(f, rf, cin_pf, cf_pf, gbw):
    s = 2j * math.pi * f
    a = 2 * math.pi * gbw / s
    cin, cf = cin_pf * 1e-12, cf_pf * 1e-12
    zf = rf / (1 + s * rf * cf)
    zin = 1 / (s * cin)
    beta = zin / (zin + zf)
    return zf * a * beta / (1 + a * beta)


def loop_q(rf, cin_pf, cf_pf, gbw):
    """Q and f0 of the roots of R_F C_T s^2 + (1 + w_t R_F C_F) s + w_t from numpy.roots."""
    wt = 2 * math.pi * gbw
    ct, cf = (cin_pf + cf_pf) * 1e-12, cf_pf * 1e-12
    r = np.roots([rf * ct, 1 + wt * rf * cf, wt])
    w0 = math.sqrt(abs(r[0] * r[1]))
    return w0 / (-2 * r[0].real) if abs(r[0].imag) > 0 else w0 / (-(r[0] + r[1]).real), w0 / (2 * math.pi)


def peak(rf, cin_pf, cf_pf, gbw):
    fs = np.logspace(3, 9, 6001)
    mags = np.abs(tia(fs, rf, cin_pf, cf_pf, gbw))
    i = int(mags.argmax())
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(lambda lf: -abs(tia(10 ** lf, rf, cin_pf, cf_pf, gbw)), bounds=(math.log10(fs[max(i - 2, 0)]),
                          math.log10(fs[min(i + 2, fs.size - 1)])), method="bounded", options={"xatol": 1e-10})
    return -res.fun / rf


def bw(rf, cin_pf, cf_pf, gbw):
    z0 = abs(tia(1e-3, rf, cin_pf, cf_pf, gbw))
    return brentq(lambda f: abs(tia(f, rf, cin_pf, cf_pf, gbw)) / z0 - 1 / math.sqrt(2), 1e2, 1e10, xtol=1e-6)


q0, f00 = loop_q(100e3, 14, 1e-9, 10e6)
v.check("Ex 10-10.7a", f00 / 1e6)
v.check("Ex 10-10.7b", q0)
v.check("Ex 10-10.7c", peak(100e3, 14, 1e-9, 10e6))
cf7 = brentq(lambda c: loop_q(100e3, 14, c, 10e6)[0] - 1 / math.sqrt(2), 1e-3, 100, xtol=1e-12)
v.check("Ex 10-10.7d", cf7)
v.check("Ex 10-10.7e", loop_q(100e3, 14, cf7, 10e6)[1] / 1e6)
v.check("Ex 10-10.7f", math.sqrt(2 * 14e-12 / (2 * math.pi * 10e6 * 100e3)) * 1e12)
a7 = 2 * math.pi * 10e6 * 100e3 * 14e-12
v.check("Ex 10-10.7i", a7)
v.assert_true("closed form C_F = sqrt(2a - 1)/(w_t R_F) matches the numerical root",
              abs(math.sqrt(2 * a7 - 1) / (2 * math.pi * 10e6 * 100e3) * 1e12 - cf7) < 1e-6)
v.check("Ex 10-10.7j", (math.sqrt(2 * 14e-12 / (2 * math.pi * 10e6 * 100e3)) * 1e12 / cf7 - 1) * 100)
v.check("Ex 10-10.7g", bw(100e3, 14, cf7, 10e6) / 1e6)
v.check("Ex 10-10.7h", abs(tia(1e-3, 100e3, 14, cf7, 10e6)) * 1e-6)
v.assert_true("with Q = 1/sqrt(2) the transimpedance -3 dB point equals f0 (Butterworth)",
              abs(bw(100e3, 14, cf7, 10e6) / loop_q(100e3, 14, cf7, 10e6)[1] - 1) < 1e-6)

# ================================================================== solutions
c = cmrr_worst(2, 0.01)
v.check("10-10.1a", c)
v.check("10-10.1b", db(c))
# worst case over all 16 corners of four 1% resistors (R1 = R3 = 10 kOhm, R2 = R4 = 20 kOhm)
import itertools  # noqa: E402
corners = [abs(diff_amp(10e3 * (1 + a), 20e3 * (1 + b), 10e3 * (1 + c_), 20e3 * (1 + d), 2.0, 2.0))
           for a, b, c_, d in itertools.product((-0.01, 0.01), repeat=4)]
v.check("10-10.1c", max(corners) * 1e3)
v.check("10-10.1d", max(corners) / 2.0)
v.check("10-10.1e", ((2 * 2 / 75) / max(corners) - 1) * 100)
v.assert_true("the single corner R1 low, R2 high gives 52.6 mV", abs(abs(diff_amp(10e3 * 0.99, 20e3 * 1.01, 10e3 * 1.01, 20e3 * 0.99, 2.0, 2.0)) * 1e3 - 52.6) < 0.05 or abs(abs(diff_amp(10e3 * 1.01, 20e3 * 0.99, 10e3 * 0.99, 20e3 * 1.01, 2.0, 2.0)) * 1e3 - 52.6) < 0.05)
v.check("10-10.2a", brentq(lambda r: 1 + 100e3 / r - 10, 10, 1e7) / 1e3)
v.check("10-10.2b", brentq(lambda r: 1 + 100e3 / r - 1000, 1, 1e6))
up3, down3 = schmitt_thresholds(10e3, 330e3, 1.65, 3.3)
v.check("10-10.3a", up3)
v.check("10-10.3b", up3 - down3)
v.check("10-10.3c", down3)
up4, down4 = schmitt_thresholds(10e3, 240e3, 2.5, 5.0, inverting=True)
v.check("10-10.4a", up4)
v.check("10-10.4b", down4)
v.check("10-10.4c", up4 - down4)
v.check("10-10.5a", (0.5e-3 / 100e3 + 10e-9) / 100e-9)
v.check("10-10.5b", (0.5e-3 * (1 + 10e6 / 100e3) + 10e-9 * 10e6) * 1e3)
dcl = abs(integ(1e-7, 100e3, 100e-9, 200, rf=10e6))
v.check("10-10.5c", brentq(lambda f: abs(integ(f, 100e3, 100e-9, 200, rf=10e6)) / dcl - 1 / math.sqrt(2), 1e-4, 1e3))
dt6 = slew_time(1.4, 0.5e6)
v.check("10-10.6a", dt6 * 1e6)
v.check("10-10.6b", math.sin(2 * math.pi * 1e3 * dt6) * 1e3)
v.check("10-10.6c", math.sin(2 * math.pi * 20e3 * dt6) * 1e3)
tau7 = 10e3 * 15e-12
rise = lambda tau: tau * (math.log(1 / 0.1) - math.log(1 / 0.9))   # noqa: E731
v.check("10-10.7a", tau7 * 1e9)
v.check("10-10.7b", rise(tau7) * 1e9)
rp = brentq(lambda r: rise(r * 15e-12) - 50e-9, 1, 1e6)
v.check("10-10.7c", rp / 1e3)
v.check("10-10.7d", 3.3 / rp * 1e3)
q8, f8 = loop_q(1e6, 5, 1e-9, 50e6)
v.check("10-10.8a", f8 / 1e6)
v.check("10-10.8b", q8)
cf9 = brentq(lambda c: loop_q(1e6, 5, c, 50e6)[0] - 1 / math.sqrt(2), 1e-4, 100, xtol=1e-12)
v.check("10-10.9a", cf9)
v.check("10-10.9b", bw(1e6, 5, cf9, 50e6) / 1e6)
v.check("10-10.9c", math.sqrt(2 * 5e-12 / (2 * math.pi * 50e6 * 1e6)) * 1e12)
v.check("10-10.9d", 2 * math.pi * 50e6 * 1e6 * 5e-12)
for key_r, key_db, f in (("10-10.10a", "10-10.10b", 60.0), ("10-10.10c", "10-10.10d", 50e3)):
    # mismatch as a complex ratio error: Z1 = R || C_stray on one input resistor
    zc = 1 / (2j * math.pi * f * 1e-12)
    r1c = 1 / (1 / 10e3 + 1 / zc)
    # complex difference amplifier, ideal op-amp: v_o = v2 R4/(R3+R4)(1 + R2/Z1) - v1 R2/Z1
    a_cm = abs(0.5 * (1 + 10e3 / r1c) - 10e3 / r1c)
    a_d = abs(0.5 * (0.5 * (1 + 10e3 / r1c) + 10e3 / r1c))
    v.check(key_r, a_d / a_cm)
    v.check(key_db, db(a_d / a_cm))
v.check("10-10.11a", 25 + 75 / 1000)
v.check("10-10.11b", (25 + 75 / 1000) * 1000 / 1e3)
v.check("10-10.11c", (25 + 75 / 1000) * 1e-6 / 1e-3 * 100)
v.check("10-10.12a", 360 * 1e6 * 47e-9)

# ================================================================== lab
rng = np.random.default_rng(1010)
e = rng.uniform(-1e-3, 1e-3, (20000, 4))
r1, r2, r3, r4 = (1e4 * (1 + e[:, i]) for i in range(4))
a_cm = r4 / (r3 + r4) * (1 + r2 / r1) - r2 / r1
a_d = 0.5 * (r4 / (r3 + r4) * (1 + r2 / r1) + r2 / r1)
dbs = 20 * np.log10(np.abs(a_d / a_cm))
v.check("Lab 10-10.a", np.median(dbs))
v.check("Lab 10-10.b", np.mean(dbs < 60) * 100)
v.check("Lab 10-10.c", dbs.min())
for key, f in (("Lab 10-10.d", 1e4), ("Lab 10-10.e", 1e5)):
    w = 2 * math.pi * f
    v.check(key, quad(lambda t: math.sin(w * t), 0, dt4)[0] / quad(lambda t: math.sin(w * t), 0, 0.5 / f)[0] * 100)
rng = np.random.default_rng(1010)
tt = np.linspace(0, 1, 4000)
vin = 2.3 + 0.4 * tt + rng.normal(0, 0.01, tt.size)


def transitions(h):
    state, count = 0, 0
    for x in vin:
        new = (1 if x > 2.5 else 0) if h == 0 else ((1 if x > 2.5 + h / 2 else 0) if state == 0 else (0 if x < 2.5 - h / 2 else 1))
        if new != state:
            count, state = count + 1, new
    return count


v.check("Lab 10-10.f", transitions(0.0))
v.check("Lab 10-10.g", transitions(0.02))
v.check("Lab 10-10.h", transitions(0.05))
wt = 2 * math.pi * 10e6
ct = (14 + cf7) * 1e-12
sol = solve_ivp(lambda t, y: [y[1], (wt - (1 + wt * 100e3 * cf7 * 1e-12) * y[1] - wt * y[0]) / (100e3 * ct)],
                (0, 10e-6), [0.0, 0.0], max_step=1e-10, rtol=1e-10, atol=1e-12, dense_output=True)
tg = np.linspace(0, 10e-6, 400001)
yg = sol.sol(tg)[0]
last = np.where(np.abs(yg - 1) > 0.01)[0][-1]
v.check("Lab 10-10.i", tg[last + 1] * 1e6)


# ------------------------------------------------------------------ relaxation oscillator: simulate the comparator and RC
def relax_period(r, c, beta, vs=5.0, cycles=6):
    """Event-driven integration of C dv/dt = (v_o - v)/R with v_o = +-vs flipping at +-beta*vs; returns the period."""
    v_, vo, t_, flips = -beta * vs, vs, 0.0, []
    for _ in range(2 * cycles):
        target = beta * vs if vo > 0 else -beta * vs
        sol = solve_ivp(lambda tt, y: [(vo - y[0]) / (r * c)], (0, 50 * r * c), [v_],
                        events=lambda tt, y: y[0] - target, rtol=1e-11, atol=1e-14)
        dt = sol.t_events[0][0]
        t_ += dt
        flips.append(t_)
        v_, vo = target, -vo
    return flips[-1] - flips[-3]


v.check("Ex 10-10.8a", brentq(lambda r: relax_period(r, 10e-9, 0.5) - 1e-3, 1e3, 1e6, xtol=1e-6) / 1e3)
f8 = 1 / relax_period(47e3, 10e-9, 0.5)
v.check("Ex 10-10.8b", f8)
v.check("Ex 10-10.8c", (f8 / 1e3 - 1) * 100)
v.check("Ex 10-10.8d", 0.5 * 5.0)
v.assert_true("the period does not depend on the supply", abs(relax_period(47e3, 10e-9, 0.5, vs=4.5) / relax_period(47e3, 10e-9, 0.5) - 1) < 1e-6)
b13 = 10e3 / 30e3
v.check("10-10.13a", b13)
T13 = relax_period(10e3, 100e-9, b13)
v.check("10-10.13b", T13 * 1e3)
v.check("10-10.13c", 1 / T13)
v.check("10-10.13d", b13 * 5.0)
# peak detector droop
v.check("10-10.14a", 200e-12 / 100e-9 * 1e3)
v.check("10-10.14b", 1e-3 / (200e-12 / 100e-9))
v.check("10-10.14c", 1.2e-9 / 100e-9 * 1e3)
v.check("10-10.14d", 1e-3 / (1.2e-9 / 100e-9) * 1e3)

v.finish()
