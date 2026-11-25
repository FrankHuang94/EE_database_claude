#!/usr/bin/env python3
"""Verify every number in chapter 22-06 (converter losses and wide-bandgap switches), its problems and its lab.

Independent routes (the lab module losses.py uses closed forms):
- overlap energy integrates v(t)·i(t) over piecewise-linear switching waveforms (with arbitrary splits of each
  transition into its current and voltage ramps);
- the hard turn-on loss is found by simulating the half-bridge charge transfer (an RC discharge/charge through the
  channel resistance with a nonlinear capacitance) and integrating i²R, and by an energy balance;
- Q_oss and E_oss of the junction model come from numerical quadrature;
- the device-size optimum and the transformer-style optima come from numerical minimization;
- junction temperatures come from fixed-point iteration of T = T_a + R_th I² R(T);
- ZVS times come from integrating dt = 2C dv/I over the swing, and the LLC magnetizing peak from integrating the
  magnetizing current over a half period;
- Baliga ratios come from the material constants; text values from the stated data-sheet numbers.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-06", ROOT / "chapters" / "22-06-converter-losses-and-wide-bandgap.md",
                        ROOT / "solutions" / "22-06-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- independent helpers
def transition_energy(V, I, t_total, split=0.3, n=20001):
    """One clamped-inductive transition of total length t_total: the current ramps at full voltage for a fraction
    `split` of it, then the voltage ramps at full current (piecewise linear). The result must not depend on split."""
    t1 = np.linspace(0, split * t_total, n)
    t2 = np.linspace(0, (1 - split) * t_total, n)
    return (integrate.simpson(V * I * t1 / t1[-1], x=t1)
            + integrate.simpson(I * V * (1 - t2 / t2[-1]), x=t2))


def overlap_power(V, I, t_on, t_off, fs):
    return (transition_energy(V, I, t_on, 0.3) + transition_energy(V, I, t_off, 0.6)) * fs


def hard_turn_on_sim(cfun, V, R=0.5):
    """Half bridge: HS channel R closes onto C_hs (charged to V) and C_ls (at 0). State: switch-node voltage x.
    Charge balance at the node: i_R = C_hs(V−x) dx/dt + C_ls(x) dx/dt, with i_R = (V − x)/R."""
    def rhs(t, x):
        return [(V - x[0]) / R / (cfun(V - x[0]) + cfun(x[0]))]
    tau = R * (cfun(0) * 2)
    sol = integrate.solve_ivp(rhs, (0, 60 * tau), [0.0], rtol=1e-11, atol=1e-12, dense_output=True)
    t = np.linspace(0, sol.t[-1], 400001)
    x = sol.sol(t)[0]
    return integrate.simpson((V - x) ** 2 / R, x=t), x[-1]


def junction_c(v_, c0=2e-9, v0=2.0, m=0.9):
    return c0 / (1 + max(v_, -1.0) / v0) ** m


def fixed_point_T(ta, rth, i, r25, slope, n=2000):
    T = ta
    for _ in range(n):
        T = ta + rth * i * i * (r25 + slope * (T - 25))
    return T


def zvs_time(C, V, I):
    """Time for a current I to swing a node holding two capacitances C (one charging, one discharging) by V:
    dt = 2 C(v) dv / I, integrated over the swing (C may be a function of v)."""
    cf = C if callable(C) else (lambda x: C)
    return integrate.quad(lambda x: 2 * cf(x) / I, 0, V, limit=200)[0]


def llc_peak(V_primary, lm, fs, n=20001):
    t = np.linspace(0, 1 / (2 * fs), n)
    di = integrate.simpson(np.full_like(t, V_primary / lm), x=t)       # rise over a half period
    return di / 2                                                      # symmetric triangle: peak = Δi/2


# ---------------------------------------------------------------- Example 22-06.1
print("Example 22-06.1")
v.check("Ex 22-06.1a", overlap_power(400, 10, 5e-9, 5e-9, 100e3))
v.check("Ex 22-06.1b", overlap_power(400, 10, 20e-9, 20e-9, 100e3))
v.check("Ex 22-06.1c", overlap_power(400, 10, 5e-9, 5e-9, 500e3))
v.check("Ex 22-06.1d", overlap_power(400, 10, 20e-9, 20e-9, 500e3))

# ---------------------------------------------------------------- Example 22-06.2
print("Example 22-06.2")
for keys, q, e in (("abcd", 1212e-12 * 400, 9.4e-6), ("efg", 47e-9, 6.3e-6), ("hij", 35e-9, 5.2e-6)):
    vals = ([q * 1e9] if len(keys) == 4 else []) + [q * 400 * 1e6, q * 400 * 100e3, q * 400 / e]
    for k, val in zip(keys, vals):
        v.check(f"Ex 22-06.2{k}", val)

# ---------------------------------------------------------------- Example 22-06.3
print("Example 22-06.3")
for keys, q in (("ab", 3.6e-6), ("cd", 0.88e-6), ("ef", 49e-9), ("gh", 35e-9)):
    v.check(f"Ex 22-06.3{keys[0]}", q * 400 * 1e6)
    v.check(f"Ex 22-06.3{keys[1]}", q * 400 * 100e3)

# ---------------------------------------------------------------- Example 22-06.4
print("Example 22-06.4")
FS4, I4 = 1e6, 20 * math.sqrt(0.75)
v.check("Ex 22-06.4a", 73e-9 * 10 * FS4)
v.check("Ex 22-06.4b", 11e-9 * 5 * FS4)
for keys, fom, vd in (("cef", 1.8e-3 * 73e-9, 10), ("dgh", 2.4e-3 * 11e-9, 5)):
    loss = lambda r, fom=fom, vd=vd: I4 ** 2 * r + fom * vd * FS4 / r
    opt = optimize.minimize_scalar(loss, bounds=(1e-5, 1e-1), method="bounded", options={"xatol": 1e-12})
    v.check(f"Ex 22-06.4{keys[0]}", fom * 1e12)
    v.check(f"Ex 22-06.4{keys[1]}", opt.x * 1e3)
    v.check(f"Ex 22-06.4{keys[2]}", opt.fun)
    v.assert_true(f"conduction equals gate loss at the optimum ({keys})",
                  abs(I4 ** 2 * opt.x / (fom * vd * FS4 / opt.x) - 1) < 1e-6)
opt4 = {}
for tag, fom, vd in (("si", 1.8e-3 * 73e-9, 10), ("gan", 2.4e-3 * 11e-9, 5)):
    opt4[tag] = optimize.minimize_scalar(lambda r, fom=fom, vd=vd: I4 ** 2 * r + fom * vd * FS4 / r,
                                         bounds=(1e-5, 1e-1), method="bounded", options={"xatol": 1e-12})
v.check("Ex 22-06.4i", opt4["gan"].fun / opt4["si"].fun)
v.check("Ex 22-06.4j", 2.4e-3 / opt4["gan"].x)

# ---------------------------------------------------------------- Example 22-06.5
print("Example 22-06.5")
k5 = (0.120 - 0.055) / 125
v.check("Ex 22-06.5a", k5 * 1e3)
T5 = fixed_point_T(60, 20, 6, 0.055, k5)
v.check("Ex 22-06.5b", T5)
R5 = 0.055 + k5 * (T5 - 25)
v.check("Ex 22-06.5c", R5 * 1e3)
v.check("Ex 22-06.5d", 36 * R5)
T5c = 60 + 20 * 36 * 0.055
v.check("Ex 22-06.5e", T5c)
icrit = optimize.brentq(lambda i: 20 * i * i * k5 - 1, 1, 100)
v.check("Ex 22-06.5f", icrit)
v.check("Ex 22-06.5g", 36 * 0.055)
v.check("Ex 22-06.5h", (icrit / 6 - 1) * 100)
v.check("Ex 22-06.5i", T5 - T5c)
v.assert_true("fixed point diverges above the runaway current",
              fixed_point_T(60, 20, 1.01 * icrit, 0.055, k5, n=400) > 1e4)

# ---------------------------------------------------------------- Example 22-06.6
print("Example 22-06.6")
VIN, IO, FS, D, TD = 48.0, 20.0, 500e3, 0.25, 20e-9
ihs = rms = math.sqrt(integrate.quad(lambda t: IO ** 2 * (t < D), 0, 1, points=[D])[0])
ils = math.sqrt(integrate.quad(lambda t: IO ** 2 * (t >= D), 0, 1, points=[D])[0])
budget = {}
for name, r, qg, vd, qoss, qrr, t, vsd in (("Si", 1.8e-3, 73e-9, 10, 135e-9, 70e-9, 8e-9, 0.8),
                                          ("GaN", 2.4e-3, 11e-9, 5, 43e-9, 0.0, 3e-9, 2.5)):
    parts = [(ihs ** 2 + ils ** 2) * r, 2 * qg * vd * FS, qoss * VIN * FS, qrr * VIN * FS,
             overlap_power(VIN, IO, t, t, FS), 2 * vsd * IO * TD * FS]
    budget[name] = parts
si, gan = budget["Si"], budget["GaN"]
for k, val in zip("abcdef", si):
    v.check(f"Ex 22-06.6{k}", val)
v.check("Ex 22-06.6g", sum(si))
v.check("Ex 22-06.6h", 240 / (240 + sum(si)) * 100)
for k, val in zip("ijklm", [gan[0], gan[1], gan[2], gan[4], gan[5]]):
    v.check(f"Ex 22-06.6{k}", val)
v.assert_true("GaN recovery loss is zero", gan[3] == 0.0)
v.check("Ex 22-06.6n", sum(gan))
v.check("Ex 22-06.6o", 240 / (240 + sum(gan)) * 100)
v.check("Ex 22-06.6p", sum(si) - si[0])
# figure: frequency at which each device's total switch loss reaches 2% of 240 W (switching terms scale with f)
for key, losses in (("Txt 22-06.l", si), ("Txt 22-06.m", gan)):
    v.check(key, optimize.brentq(lambda f: losses[0] + (sum(losses) - losses[0]) * f / 500e3 - 0.02 * 240, 1e3, 5e6) / 1e3)

# ---------------------------------------------------------------- Example 22-06.7
print("Example 22-06.7")
v.check("Ex 22-06.7a", zvs_time(88e-12, 400, 2) * 1e9)
v.check("Ex 22-06.7b", zvs_time(1212e-12, 400, 2) * 1e9)
for keys, C in (("cdg", 88e-12), ("ef", 1212e-12)):
    imin = optimize.brentq(lambda i: zvs_time(C, 400, i) - 50e-9, 0.01, 1000)
    lm = optimize.brentq(lambda L: llc_peak(200, L, 300e3) - imin, 1e-7, 1e-2)
    v.check(f"Ex 22-06.7{keys[0]}", imin)
    v.check(f"Ex 22-06.7{keys[1]}", lm * 1e6)
    if len(keys) == 3:
        t = np.linspace(0, 1, 200001)
        tri = imin * (1 - 4 * np.abs(t - 0.5))                         # triangle of peak imin over a period
        v.check(f"Ex 22-06.7{keys[2]}", math.sqrt(integrate.simpson(tri ** 2, x=t)))

# ---------------------------------------------------------------- text numbers
print("Text")
v.check("Txt 22-06.a", 120 / 55)
v.check("Txt 22-06.b", 2e-9 * 20 / 2e-9)
v.check("Txt 22-06.c", 1212 / 117)
v.check("Txt 22-06.d", 6270 / 8.8, rtol=0.03)                          # "about 700"
v.check("Txt 22-06.e", 27900 / 8.8, rtol=0.03)                         # "about 3200"
v.check("Txt 22-06.f", 55 * 4.7)
v.check("Txt 22-06.g", 50 * 22)
v.check("Txt 22-06.h", 38 * 90)
v.check("Txt 22-06.i", 1212e-12 * 400 * 1e9)
v.check("Txt 22-06.j", 100e-9 * 400 * 1e6)
v.check("Txt 22-06.k", (100e-9 * 400 - 10e-6) * 1e6)

# §3.7 energy condition for a small swinging inductance: integrate the swing with a nonlinear
# C(v) = C0/sqrt(1 + v/V0) per switch, the inductor's far end at the rail the node leaves, and find
# the smallest starting current that still reaches 0 V. Compare 1/2 L I^2 with Q_oss V and 2 E_oss.
C0Z, V0Z, VZ, LZ = 2e-9, 5.0, 400.0, 2e-6


def czv(x):
    return C0Z / math.sqrt(1 + max(x, 0.0) / V0Z)


def swing_margin(i0):
    def rhs(_t, y):
        vn, i = y
        return [-i / (czv(vn) + czv(VZ - vn)), (vn - VZ) / LZ]
    hit0 = lambda _t, y: y[0]
    hit0.terminal, hit0.direction = True, -1
    stall = lambda _t, y: y[1]
    stall.terminal, stall.direction = True, -1
    sol = integrate.solve_ivp(rhs, (0, 1e-5), [VZ, i0], events=(hit0, stall), rtol=1e-10, atol=[1e-9, 1e-12],
                              max_step=1e-9)
    return sol.y[1, -1] if sol.t_events[0].size else -sol.y[0, -1]


i_crit = optimize.brentq(swing_margin, 0.5, 20, xtol=1e-9)
qz = integrate.quad(czv, 0, VZ)[0]
ez = integrate.quad(lambda x: x * czv(x), 0, VZ)[0]
v.assert_true("§3.7: ZVS energy boundary 1/2 L I^2 equals Q_oss V for nonlinear C_oss",
              abs(0.5 * LZ * i_crit ** 2 / (qz * VZ) - 1) < 1e-4)
v.assert_true("§3.7: a 2 E_oss condition would understate it for nonlinear C_oss", 2 * ez < 0.9 * qz * VZ)

# ---------------------------------------------------------------- problems
print("Problems")
v.check("22-06.1a", 22e-9 * 18 * 100e3 * 1e3)
v.check("22-06.1b", 22e-9 * 18 * 500e3)
v.check("22-06.2", overlap_power(48, 15, 4e-9, 6e-9, 1e6))
e_lin, _ = hard_turn_on_sim(lambda x: 100e-12, 400)
v.check("22-06.3a", 100e-12 * 400 * 1e9)
v.check("22-06.3b", integrate.quad(lambda x: x * 100e-12, 0, 400)[0] * 1e6)
v.check("22-06.3c", e_lin * 1e6)
v.check("22-06.4a", 1.5e-9 * 30 / 3e-9)
v.check("22-06.4b", 48 + 1.5e-9 * 30 / 3e-9)
v.check("22-06.4c", 100 - 48 - 1.5e-9 * 30 / 3e-9)
v.check("22-06.4d", optimize.brentq(lambda L: L * 30 / 1.5e-9 - 20, 1e-12, 1e-6) * 1e9)
v.check("22-06.5a", 2 * 4.3 * 20 * 100e-9 * 100e3)
v.check("22-06.5b", 2 * 4.3 * 20 * 30e-9 * 100e3)
rq6 = 2.4e-3 * 43e-9
opt6 = optimize.minimize_scalar(lambda r: 100 * r + rq6 * 48 * 1e6 / r, bounds=(1e-5, 1e-1), method="bounded",
                                options={"xatol": 1e-12})
v.check("22-06.6a", rq6 * 1e12)
v.check("22-06.6b", opt6.x * 1e3)
v.check("22-06.6c", opt6.fun)
k7 = (0.082 - 0.050) / 150
v.check("22-06.7a", k7 * 1e3)
T7 = fixed_point_T(50, 15, 10, 0.050, k7)
v.check("22-06.7b", T7)
v.check("22-06.7c", (0.050 + k7 * (T7 - 25)) * 1e3)
v.check("22-06.7d", 100 * (0.050 + k7 * (T7 - 25)))
v.check("22-06.7e", optimize.brentq(lambda i: 15 * i * i * k7 - 1, 1, 100))
v.check("22-06.8a", 3.6e-6 * 400 * 65e3)
v.check("22-06.8b", 30e-9 * 400 * 65e3)
EPS0 = 8.8541878128e-12
bf = lambda er, mu, ec: er * EPS0 * mu * 1e-4 * (ec * 1e8) ** 3      # SI: F/m · m²/V·s · (V/m)³
si_b, sic_b, gan_b = bf(11.9, 1240, 0.3), bf(9.7, 980, 3.1), bf(10.4, 1000, 4.9)
v.check("22-06.9f", 11.9 * 1240 * 0.3 ** 3)
v.check("22-06.9g", 9.7 * 980 * 3.1 ** 3 / 1e5)
v.check("22-06.9h", 10.4 * 1000 * 4.9 ** 3 / 1e6)
v.assert_true("22-06.9: SI Baliga products have the same ratios", abs(sic_b / si_b - (9.7 * 980 * 3.1 ** 3) / (11.9 * 1240 * 0.3 ** 3)) < 1e-9)
v.check("22-06.9a", sic_b / si_b)
v.check("22-06.9b", gan_b / si_b)
VB = 1200.0
ron = lambda b: 4 * VB ** 2 / b
v.check("22-06.9c", ron(si_b) / ron(sic_b))
v.check("22-06.9d", 6270 / 8.8)
v.check("22-06.9e", 27900 / 8.8)
for k, td in zip("abc", (5e-9, 10e-9, 20e-9)):
    v.check(f"22-06.10{k}", optimize.brentq(lambda i: (2 * 43e-9) / i - td, 1e-3, 1e4))
imin11 = optimize.brentq(lambda i: zvs_time(88e-12, 400, i) - 30e-9, 0.01, 1000)
v.check("22-06.11a", imin11)
lm11 = optimize.brentq(lambda L: llc_peak(400, L, 500e3) - imin11, 1e-7, 1e-2)
v.check("22-06.11b", lm11 * 1e6)
t = np.linspace(0, 1, 200001)
v.check("22-06.11c", math.sqrt(integrate.simpson((imin11 * (1 - 4 * np.abs(t - 0.5))) ** 2, x=t)))
slope_si = (sum(si) - si[0]) / 0.5
slope_gan = (sum(gan) - gan[0]) / 0.5
v.check("22-06.12a", slope_si)
v.check("22-06.12b", slope_gan)
f_si = optimize.brentq(lambda f: si[0] + slope_si * f - 4.8, 0, 10)
f_gan = optimize.brentq(lambda f: gan[0] + slope_gan * f - 4.8, 0, 10)
v.check("22-06.12c", f_si)
v.check("22-06.12d", f_gan)
v.check("22-06.12e", f_gan / f_si)

# Problem 22-06.13: (a) the energy identity for a general far-end potential, by integrating the swing
# with the nonlinear C(v) of the §3.7 check; (c-h) the minimum currents.
def swing_end(i0, vx):
    def rhs(_t, y):
        return [-y[1] / (czv(y[0]) + czv(VZ - y[0])), (y[0] - vx) / LZ]
    hit0 = lambda _t, y: y[0]
    hit0.terminal, hit0.direction = True, -1
    s = integrate.solve_ivp(rhs, (0, 1e-5), [VZ, i0], events=hit0, rtol=1e-10, atol=[1e-9, 1e-12], max_step=1e-9)
    return s.y[1, -1], s.y[1].min()


for vx in (0.8 * VZ, 0.3 * VZ):
    i1, imin = swing_end(8.0, vx)
    v.assert_true(f"22-06.13a: 1/2 L (I0^2 - I1^2) = Q_oss (2Vx - V) at Vx = {vx:.0f} V",
                  abs(0.5 * LZ * (8.0 ** 2 - i1 ** 2) - qz * (2 * vx - VZ)) < 1e-6 * 0.5 * LZ * 64)
    v.assert_true(f"22-06.13b: smallest current is at an end of the swing (Vx = {vx:.0f} V)",
                  imin >= min(8.0, i1) - 1e-6)
L13 = 4e-6
q13g, q13s = integrate.quad(lambda x: 88e-12, 0, 400)[0], integrate.quad(lambda x: 1212e-12, 0, 400)[0]
v.check("22-06.13c", q13g * 1e9)
v.check("22-06.13d", optimize.brentq(lambda i: 0.5 * L13 * i ** 2 - q13g * 400, 0, 100))
v.check("22-06.13e", q13s * 1e9)
i13f = optimize.brentq(lambda i: 0.5 * L13 * i ** 2 - q13s * 400, 0, 100)
v.check("22-06.13f", i13f)
i13g = optimize.brentq(lambda i: 0.5 * L13 * i ** 2 - 117e-12 * 400 ** 2, 0, 100)
v.check("22-06.13g", i13g)
v.check("22-06.13h", i13f / i13g)

# ---------------------------------------------------------------- lab
print("Lab")
import mpmath as mp  # noqa: E402

mp.mp.dps = 30
q_j = float(mp.quad(lambda x: 2e-9 / (1 + x / 2) ** mp.mpf("0.9"), [0, 1, 10, 100, 400]))
e_j = float(mp.quad(lambda x: x * 2e-9 / (1 + x / 2) ** mp.mpf("0.9"), [0, 1, 10, 100, 400]))
v.check("Lab 22-06.a", q_j * 1e9)
v.check("Lab 22-06.b", e_j * 1e6)
e_sim, xend = hard_turn_on_sim(junction_c, 400)
v.check("Lab 22-06.c", e_sim * 1e6)
v.assert_true("simulated hard turn-on equals Q_oss·V", abs(e_sim / (q_j * 400) - 1) < 1e-4)
v.assert_true("switch node reaches the rail", abs(xend - 400) < 1e-3)
v.check("Lab 22-06.d", 2 * e_j * 1e6)
v.check("Lab 22-06.e", q_j * 400 / e_j)
v.check("Lab 22-06.f", q_j / 400 * 1e12)

sys.path.insert(0, str(LAB))
import losses as ls  # noqa: E402

v.assert_true("lab qoss_junction matches quadrature", abs(ls.qoss_junction(2e-9, 2, 0.9, 400) / q_j - 1) < 1e-8)
v.assert_true("lab eoss_junction matches quadrature", abs(ls.eoss_junction(2e-9, 2, 0.9, 400) / e_j - 1) < 1e-8)
v.assert_true("lab overlap formula matches the waveform integral",
              abs(ls.overlap(400, 10, 5e-9, 7e-9, 1e5) - overlap_power(400, 10, 5e-9, 7e-9, 1e5)) < 1e-9)
v.assert_true("transition energy is independent of how the transition splits",
              abs(transition_energy(400, 10, 10e-9, 0.1) - transition_energy(400, 10, 10e-9, 0.8)) < 1e-12)
v.assert_true("lab junction_temperature matches fixed-point iteration",
              abs(ls.junction_temperature(60, 20, 6, 0.055, k5) - T5) < 1e-9)
v.assert_true("lab llc_magnetizing_peak matches the integrated current",
              abs(ls.llc_magnetizing_peak(400, 100e-6, 300e3) - llc_peak(200, 100e-6, 300e3)) < 1e-9)
v.assert_true("lab minimum_loss matches numerical minimization",
              abs(ls.minimum_loss(2.4e-3 * 11e-9, 5, 1e6, I4) - 2 * I4 * math.sqrt(2.4e-3 * 11e-9 * 5e6)) < 1e-12)

v.finish()
