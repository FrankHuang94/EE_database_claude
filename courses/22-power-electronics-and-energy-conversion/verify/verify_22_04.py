#!/usr/bin/env python3
"""Verify every number in chapter 22-04 (isolated converters), its problems and its lab helpers.

Independent routes (the lab module isolated.py uses closed forms):
- the flyback's ratio comes from its switched steady state (magnetizing current referred to the primary,
  output capacitor on the secondary), found by Newton iteration on the one-period map;
- boundary-conduction sizing solves for L_m so that the integrated triangle of input current carries P_in;
- the RCD clamp energy integrates the clamp interval's current and the power delivered to the clamp;
- the forward converter's magnetizing current and reset come from integrating L_m di/dt over on and reset;
- duty cycles come from root finding on volt-second balance; insulation numbers from 2 pi f C V.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-04", ROOT / "chapters" / "22-04-isolated-converters.md",
                        ROOT / "solutions" / "22-04-solutions.md", LAB / "README.md")
TOL = dict(rtol=1e-11, atol=1e-13)


def vsb_flyback_duty(v_in, v_out, n):
    return optimize.brentq(lambda d: v_in * d - n * v_out * (1 - d), 1e-9, 1 - 1e-9, xtol=1e-14)


def flyback_pss_vout(v_in, d, fs, lm, n, cout, r):
    """CCM flyback steady state: state (i_m on primary, v_out); returns the average output voltage."""
    t_s = 1 / fs
    on = lambda t, y: [v_in / lm, -y[1] / (r * cout)]  # noqa: E731
    off = lambda t, y: [-n * y[1] / lm, (n * y[0] - y[1] / r) / cout]  # noqa: E731

    def period(x):
        a = integrate.solve_ivp(on, (0, d * t_s), x, **TOL)
        b = integrate.solve_ivp(off, (0, (1 - d) * t_s), a.y[:, -1], **TOL)
        return b.y[:, -1]

    vg = v_in * d / ((1 - d) * n)
    x0 = optimize.fsolve(lambda x: period(x) - x, [vg / r / (n * (1 - d)), vg], xtol=1e-13)
    t1 = np.linspace(0, d * t_s, 1000)
    t2 = np.linspace(0, (1 - d) * t_s, 1000)
    a = integrate.solve_ivp(on, (0, d * t_s), x0, t_eval=t1, **TOL)
    b = integrate.solve_ivp(off, (0, (1 - d) * t_s), a.y[:, -1], t_eval=t2, **TOL)
    vo = np.concatenate([a.y[1], b.y[1]])
    tt = np.concatenate([t1, d * t_s + t2])
    return np.trapezoid(vo, tt) / t_s, x0


def boundary_lm(p_in, v_in, d, fs):
    """L_m such that the input-current triangle (0 -> V_in D T / L_m over D T) averages P_in / V_in."""
    t_s = 1 / fs

    def avg_in(lm):
        s = integrate.solve_ivp(lambda t, y: [v_in / lm, 0.0], (0, d * t_s), [0.0, 0.0], dense_output=True, **TOL)
        tt = np.linspace(0, d * t_s, 2001)
        return np.trapezoid(s.sol(tt)[0], tt) / t_s

    return optimize.brentq(lambda lm: avg_in(lm) - p_in / v_in, 1e-6, 1e-1, xtol=1e-14)


def clamp_energy_ode(l_lk, i_pk, v_c, v_r):
    """Integrate the clamp interval: di/dt = -(V_c - V_R)/L_lk until i = 0; energy = integral of V_c i dt."""
    ev = lambda t, y: y[0]  # noqa: E731
    ev.terminal = True
    s = integrate.solve_ivp(lambda t, y: [-(v_c - v_r) / l_lk, v_c * y[0]], (0, 1e-3), [i_pk, 0.0],
                            events=ev, rtol=1e-12, atol=1e-18)
    return s.y[1, -1]


def magnetizing(v_in, t_on, lm):
    s = integrate.solve_ivp(lambda t, y: [v_in / lm], (0, t_on), [0.0], **TOL)
    return s.y[0, -1]


# ---------------------------------------------------------------- Example 22-04.1
print("Example 22-04.1")
n = 32 / 5
d1 = vsb_flyback_duty(150.0, 20.0, n)
v.check("Ex 22-04.1a", n)
v.check("Ex 22-04.1b", d1)
vo_sim, _ = flyback_pss_vout(150.0, d1, 100e3, 500e-6, n, 0.1, 6.1538)
v.assert_true("switched flyback steady state gives 20 V at the volt-second duty", abs(vo_sim - 20.0) < 2e-3)
v.check("Ex 22-04.1c", n * 20)
v.check("Ex 22-04.1d", 150 + n * 20)
v.check("Ex 22-04.1e", 264 * math.sqrt(2) + n * 20)

# ---------------------------------------------------------------- Example 22-04.2
print("Example 22-04.2")
pin = 65 / 0.92
d2 = vsb_flyback_duty(100.0, 20.0, n)
lm2 = boundary_lm(pin, 100.0, d2, 100e3)
ipk2 = magnetizing(100.0, d2 / 100e3, lm2)
v.check("Ex 22-04.2a", d2)
v.check("Ex 22-04.2b", ipk2)
v.check("Ex 22-04.2c", lm2 * 1e6)
v.check("Ex 22-04.2d", 0.5 * lm2 * ipk2 ** 2 * 1e3)
v.assert_true("energy per cycle times f_s equals P_in", abs(0.5 * lm2 * ipk2 ** 2 * 100e3 - pin) < 1e-6)

# ---------------------------------------------------------------- Example 22-04.3
print("Example 22-04.3")
for key, nn, vin in (("a", 4, 48.0), ("b", 4, 36.0), ("c", 3, 36.0), ("d", 3, 75.0)):
    v.check(f"Ex 22-04.3{key}", optimize.brentq(lambda d, nn=nn, vin=vin: d * vin / nn - 5.0, 0, 2))
# reset: primary sees -V_in N1/N3 during reset; the switch blocks V_in + V_in N1/N3
v.check("Ex 22-04.3e", 75 + 75 * 1)

# ---------------------------------------------------------------- Example 22-04.4
print("Example 22-04.4")
im4 = magnetizing(48.0, 0.4 / 250e3, 500e-6)
v.check("Ex 22-04.4a", im4)
v.check("Ex 22-04.4b", 0.5 * 500e-6 * im4 ** 2 * 1e6)
v.check("Ex 22-04.4c", 0.5 * 500e-6 * im4 ** 2 * 250e3)
# reset through a 1:1 tertiary takes exactly the on-time
tr = optimize.brentq(lambda t: im4 - 48.0 * t / 500e-6, 0, 1e-5)
v.assert_true("1:1 tertiary reset time equals the on-time", abs(tr - 0.4 / 250e3) < 1e-12)

# ---------------------------------------------------------------- Example 22-04.5
print("Example 22-04.5")
llk = 0.02 * lm2
e0 = 0.5 * llk * ipk2 ** 2
ec = clamp_energy_ode(llk, ipk2, 200.0, n * 20)
v.check("Ex 22-04.5a", llk * 1e6)
v.check("Ex 22-04.5b", e0 * 1e6)
v.check("Ex 22-04.5c", ec / e0)
v.check("Ex 22-04.5d", ec * 100e3)
v.check("Ex 22-04.5e", ec * 100e3 / pin * 100)

# ---------------------------------------------------------------- Example 22-04.6
print("Example 22-04.6")
v.check("Ex 22-04.6a", 3.8 * 1.48)
for key, basic in (("b", 2.0), ("c", 2.8), ("d", 4.0)):
    v.check(f"Ex 22-04.6{key}", 2 * basic)
v.check("Ex 22-04.6e", 2 * math.pi * 60 * 2.2e-9 * 264 * 1e3)
v.check("Ex 22-04.6f", optimize.brentq(lambda c: 2 * math.pi * 60 * c * 264 - 0.5e-3, 1e-12, 1e-6) * 1e9)

# ---------------------------------------------------------------- Example 22-04.7
print("Example 22-04.7")
v.check("Ex 22-04.7a", 6 * 50 / 400)
v.check("Ex 22-04.7b", 400)
v.check("Ex 22-04.7c", (1000 / 50) / 6)
v.check("Ex 22-04.7d", 400 + 400)
# the peak current at the DCM boundary does not depend on the frequency; evaluate at 100 kHz
lm7 = boundary_lm(1000.0, 400.0, 0.5, 100e3)
ipk7 = magnetizing(400.0, 0.5 / 100e3, lm7)
v.check("Ex 22-04.7e", ipk7)
v.check("Ex 22-04.7f", 400 * (1000 / 50) / 6)
v.check("Ex 22-04.7g", 800 * ipk7)
v.check("Ex 22-04.7h", 4 * 400 * (1000 / 50) / 6 / 1e3)

# ---------------------------------------------------------------- problems
print("Problems")
v.check("22-04.1a", vsb_flyback_duty(48.0, 12.0, 2.0))
v.check("22-04.1b", 48 + 2 * 12)
ip2 = magnetizing(300.0, 0.3 / 65e3, 1e-3)
v.check("22-04.2a", ip2)
v.check("22-04.2b", 0.5 * 1e-3 * ip2 ** 2 * 65e3)
v.check("22-04.3a", 16 * 12 / 400)
v.check("22-04.3b", 2 * 400)
vd = 264 * math.sqrt(2) + 180
v.check("22-04.4a", vd)
v.check("22-04.4b", 650 - vd)
v.check("22-04.4c", (650 - vd) / 650 * 100)
d5 = vsb_flyback_duty(150.0, 20.0, n)
dim5 = magnetizing(150.0, d5 / 100e3, 500e-6)
v.check("22-04.5a", dim5)
# DCM boundary: find the output current at which the simulated valley magnetizing current reaches zero
def valley(i_out):
    _, x0 = flyback_pss_vout(150.0, d5, 100e3, 500e-6, n, 0.1, 20.0 / i_out)
    return x0[0]


v.check("22-04.5b", optimize.brentq(valley, 1.0, 4.0, xtol=1e-9))
e6 = 0.5 * 3e-6 * 4
v.check("22-04.6a", e6 * 1e6)
v.check("22-04.6b", e6 * 1e5)
for key, vc in (("c", 150.0), ("d", 200.0), ("e", 300.0)):
    v.check(f"22-04.6{key}", clamp_energy_ode(3e-6, 2.0, vc, 100.0) * 1e5)
v.check("22-04.7a", 1 / (1 + 0.5))
v.check("22-04.7b", 1 + 1 / 0.5)
v.check("22-04.8a", 48 * 0.4 * 4e-6 / (6 * 40e-6))
v.check("22-04.8b", optimize.brentq(lambda nn: 48 * 0.4 * 4e-6 / (nn * 40e-6) - 0.2, 1, 100))
v.check("22-04.9a", 0.8 * 340 / 12)
v.check("22-04.9b", 12 * 22 / 380)
v.check("22-04.9c", 100 / 22)
v.check("22-04.10a", 2 * math.pi * 50 * 4.7e-9 * 264 * 1e3)
v.check("22-04.10b", 2 * math.pi * 60 * 4.7e-9 * 264 * 1e3)
v.check("22-04.11a", 3.0 * 1.48)
v.check("22-04.11b", 3.8 * 1.48)
n12 = 100 / 12
d12a = vsb_flyback_duty(100.0, 12.0, n12)
v.check("22-04.12a", n12)
v.check("22-04.12b", d12a)
v.check("22-04.12d", 373 + 100)
p12 = 24 / 0.88
v.check("22-04.12e", p12)
lm12 = boundary_lm(p12, 100.0, d12a, 65e3)
v.check("22-04.12f", magnetizing(100.0, d12a / 65e3, lm12))
v.check("22-04.12g", lm12 * 1e6)
# (c) at 373 V and fixed 65 kHz: DCM; find D whose stored energy per cycle delivers P_in
d12c = optimize.brentq(lambda d: 0.5 * lm12 * (373 * d / 65e3 / lm12) ** 2 * 65e3 - p12, 0.01, 0.5)
v.check("22-04.12c", d12c)
v.assert_true("22-04.12c is discontinuous (D + D2 < 1)", d12c + 373 * d12c / 100 < 1)
v.check("22-04.13a", 2 * 4.0)
v.check("22-04.13b", 2 * 4.0 - 2 * 2.0)
v.assert_true("22-04.13c: groups I and II fit a 6 mm path, III does not", 2 * 2.0 <= 6 and 2 * 2.8 <= 6 and 2 * 4.0 > 6)
# 22-04.14: D from per-cycle energy balance; DCM confirmed by simulating the reset interval
ts14, lm14, r14 = 1 / 150e3, 30e-6, 5 / 2
d14 = optimize.brentq(lambda d: 0.5 * lm14 * (48 * d * ts14 / lm14) ** 2 / ts14 - 5 * 2, 0.01, 0.9)
v.check("22-04.14a", d14)
v.check("22-04.14b", 2 * lm14 / (16 * r14 * ts14))
ipk14 = 48 * d14 * ts14 / lm14
v.check("22-04.14c", ipk14)
t_reset14 = ipk14 * lm14 / (4 * 5)            # magnetizing current falls at nV/Lm
v.assert_true("22-04.14 resets within the period", d14 * ts14 + t_reset14 < ts14)
d14c = optimize.brentq(lambda d: 48 / 4 * d / (1 - d) - 5, 0.01, 0.9)
v.check("22-04.14d", 1e6 * optimize.brentq(lambda lm: 2 * lm / (16 * r14 * ts14) - (1 - d14c) ** 2, 1e-6, 1e-3))
# 22-04.15: output stage as a buck fed by Vin/n; ripple from the sampled inductor waveform
v.check("22-04.15a", 4.5 * 3.3 / 36)
d15b = 4.5 * 3.3 / 72
v.check("22-04.15b", d15b)
l15 = optimize.brentq(lambda l: (72 / 4.5 - 3.3) * d15b / 300e3 / l - 4.5, 1e-7, 1e-5)
tt15 = np.linspace(0, 1 / 300e3, 300001)
vl15 = np.where(tt15 < d15b / 300e3, 72 / 4.5 - 3.3, -3.3)
il15 = np.concatenate([[0], np.cumsum((vl15[1:] + vl15[:-1]) / 2 * np.diff(tt15))]) / l15
v.assert_true("22-04.15: sampled ripple is 4.5 A", abs(np.ptp(il15) - 4.5) < 1e-3)
v.check("22-04.15c", 1e6 * l15)
ic15 = il15 - il15.mean()
q15 = np.concatenate([[0], np.cumsum((ic15[1:] + ic15[:-1]) / 2 * np.diff(tt15))])
v.check("22-04.15d", 1e6 * optimize.brentq(lambda c: np.ptp(q15 / c) - 0.02, 1e-6, 1e-3))
v.check("22-04.15e", 36 * (4.5 * 3.3 / 36) / 300e3 / (9 * 60e-6))

# ---------------------------------------------------------------- lab helpers
print("Lab")
sys.path.insert(0, str(LAB))
import isolated as iso  # noqa: E402

v.assert_true("lab clamp_energy equals the integrated clamp interval",
              abs(iso.clamp_energy(llk, ipk2, 200.0, n * 20) - ec) < 1e-12)
v.assert_true("lab boundary design equals the energy-balance route",
              abs(iso.flyback_boundary_design(pin, 100.0, 20.0, n, 100e3)[2] - lm2) < 1e-12)
v.assert_true("lab DCM boundary current equals the simulated valley route",
              abs(iso.flyback_dcm_boundary_current(150.0, 20.0, n, 100e3, 500e-6)
                  - optimize.brentq(valley, 1.0, 4.0, xtol=1e-9)) < 1e-4)


# README keys: each recomputed through the lab module and cross-checked against an independent route
v.check("Lab 22-04.a", 48.0 * iso.forward_switch_voltage(1.0, 1.0))       # 3:1:3 windings, N3/N1 = 1
v.assert_true("forward reset voltage is twice the input by the tertiary's volt-second balance",
              abs(iso.forward_switch_voltage(48.0, 1.0) - (48.0 + 48.0 * 3 / 3)) < 1e-12)
for key, frac in (("Lab 22-04.b", 0.01), ("Lab 22-04.c", 0.05)):
    v.check(key, iso.clamp_energy(frac * lm2, ipk2, 200.0, n * 20) * 100e3)
    v.assert_true(f"clamp power at {frac:.0%} leakage scales linearly from the 2% example",
                  abs(iso.clamp_energy(frac * lm2, ipk2, 200.0, n * 20) * 100e3 - ec * 100e3 * frac / 0.02) < 1e-9)
v.check("Lab 22-04.d", iso.y_cap_limit(0.5e-3, 264.0, 50.0) * 1e9)

sys.exit(v.finish())
