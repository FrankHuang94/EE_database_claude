#!/usr/bin/env python3
"""Verify chapter 15-01 (modeling dynamic systems): examples, problems and lab answers.

Every value is recomputed by a route other than the hand formula where one exists:
- peaks, periods and settling values by integrating the original differential equations (solve_ivp);
- time constants as eigenvalues of the state matrices, and temperatures by the matrix exponential;
- equilibria by root finding, and linearizations by finite-difference Jacobians of the nonlinear models;
- the nonlinear pendulum's period by integration, cross-checked with the elliptic-integral formula.
The ngspice netlists in labs/15-01-lab confirm Examples 15-01.1 and 15-01.3 independently (tools/run_spice.py).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.special import ellipk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "15-01-lab"))
from eeverify import Verifier  # noqa: E402
import plants  # noqa: E402

CH = ROOT / "chapters" / "15-01-modeling-dynamic-systems.md"
v = Verifier.from_files("15-01", CH, ROOT / "solutions" / "15-01-solutions.md", ROOT / "labs" / "15-01-lab" / "README.md")
TIGHT = dict(rtol=1e-10, atol=1e-12)


def jac(f, x0, h=1e-6):
    """Central-difference Jacobian of f: R^n -> R^n at x0."""
    x0 = np.asarray(x0, dtype=float)
    cols = []
    for i in range(len(x0)):
        d = np.zeros_like(x0)
        d[i] = h * max(1.0, abs(x0[i]))
        cols.append((np.asarray(f(x0 + d)) - np.asarray(f(x0 - d))) / (2 * d[i]))
    return np.array(cols).T


def peak(rhs, y0, t_end, idx=0):
    """Largest value of state idx and its time, from a dense integration."""
    sol = solve_ivp(rhs, (0, t_end), y0, dense_output=True, **TIGHT)
    t = np.linspace(0, t_end, 400001)
    y = sol.sol(t)[idx]
    k = int(np.argmax(y))
    return y[k], t[k], sol


# ---------------------------------------------------------------------------------------- Example 1
m, b, k, F0 = 0.5, 4.0, 200.0, 10.0
A1, B1 = plants.msd(m, b, k)
ev1 = np.linalg.eigvals(A1)
wn1 = abs(ev1[0])
v.check("Ex 15-01.1a", wn1)
v.check("Ex 15-01.1b", -ev1[0].real / wn1)
xpk, tpk, sol1 = peak(lambda t, y: A1 @ y + B1 * F0, [0.0, 0.0], 3.0)
v.check("Ex 15-01.1c", sol1.sol(3.0)[0])
an = plants.analogs(m, b, k)
v.check("Ex 15-01.1d", an["force-voltage"]["C"] * 1e3)
v.check("Ex 15-01.1e", an["force-current"]["R"])
v.check("Ex 15-01.1f", an["force-current"]["L"] * 1e3)
v.check("Ex 15-01.1g", xpk)
v.check("Ex 15-01.1h", tpk)
# the force-voltage circuit (L i' = v - R i - q/C, q' = i) gives the same charge trajectory as the displacement
cfv = an["force-voltage"]
qsol = solve_ivp(lambda t, y: [(F0 - cfv["R"] * y[0] - y[1] / cfv["C"]) / cfv["L"], y[0]], (0, 3), [0, 0], dense_output=True, **TIGHT)
tt = np.linspace(0, 3, 3001)
v.assert_true("force-voltage circuit: charge equals displacement at every instant", np.max(np.abs(qsol.sol(tt)[1] - sol1.sol(tt)[0])) < 1e-8)

# ---------------------------------------------------------------------------------------- Example 2
R, L, K, J, B, V = 2.0, 1e-3, 0.05, 2e-5, 1e-5, 12.0
A2, B2 = plants.motor(R, L, K, J, B)
sol2 = solve_ivp(lambda t, y: A2 @ y + B2 * V, (0, 0.5), [0, 0], **TIGHT)
w_ss, i_ss = sol2.y[1, -1], sol2.y[0, -1]
v.check("Ex 15-01.2a", w_ss)
v.check("Ex 15-01.2b", w_ss * 60 / (2 * math.pi))
v.check("Ex 15-01.2c", i_ss)
i_stall = brentq(lambda i: L * 0 - (V - R * i), 0, 100)          # omega = 0: V = R i
v.check("Ex 15-01.2d", i_stall)
v.check("Ex 15-01.2e", K * i_stall)
v.check("Ex 15-01.2f", L / R * 1e3)
gain1, tau1 = plants.motor_first_order(R, K, J, B)
v.check("Ex 15-01.2g", tau1 * 1e3)
taus2 = sorted(-1 / np.linalg.eigvals(A2).real)
v.check("Ex 15-01.2h", taus2[1] * 1e3)
v.check("Ex 15-01.2i", taus2[0] * 1e3)
v.check("Ex 15-01.2j", 100 * (tau1 / taus2[1] - 1))
v.check("Ex 15-01.2k", (taus2[0] + taus2[1]) * 1e3)
v.check("Ex 15-01.2l", taus2[1] / taus2[0])
v.check("Ex 15-01.2m", i_stall / i_ss)
v.check("Ex 15-01.2n", K * K / R)
v.check("Ex 15-01.2o", K * K / R / B)
v.check("Ex 15-01.2p", R * J / K**2 * 1e3)
v.assert_true("first-order model: gain K/(RB + K^2) equals the simulated speed per volt", abs(gain1 * V - w_ss) < 1e-6)

# ---------------------------------------------------------------------------------------- Example 3
P, Rjc, Rca, Cj, Ch, Ta = 100.0, 0.15, 0.35, 5.0, 300.0, 30.0
A3, B3 = plants.thermal_two_node(Rjc, Rca, Cj, Ch)
sol3 = solve_ivp(lambda t, y: A3 @ y + B3 * P, (0, 5000), [0, 0], dense_output=True, method="Radau", rtol=1e-10, atol=1e-10)
v.check("Ex 15-01.3a", Ta + sol3.sol(5000)[0])
v.check("Ex 15-01.3b", Ta + sol3.sol(5000)[1])
taus3 = sorted(-1 / np.linalg.eigvals(A3).real)
v.check("Ex 15-01.3c", taus3[0])
v.check("Ex 15-01.3d", taus3[1])
for key, t in zip("efgh", (1, 5, 60, 300)):
    v.check(f"Ex 15-01.3{key}", Ta + sol3.sol(t)[0])
    v.assert_true(f"matrix exponential agrees with integration at {t} s", abs(plants.step(A3, B3, P, t)[0] - sol3.sol(t)[0]) < 1e-6)
v.check("Ex 15-01.3i", Rjc * Cj)
v.check("Ex 15-01.3j", Rca * Ch)
R1, C1 = Rjc + Rca, 107.0 / (Rjc + Rca)                         # a one-node model with tau = 107 s
one_node = solve_ivp(lambda t, y: [(P - y[0] / R1) / C1], (0, 1), [0.0], **TIGHT)
v.check("Ex 15-01.3k", Ta + one_node.y[0, -1])
v.check("Txt 15-01.a", 1.0 * 1.0 * 0.075 * 2.329 * 0.7)          # cm x cm x cm, g/cm^3, J/(g K)

# ---------------------------------------------------------------------------------------- Example 4
Pd, PL0, Tx, R4, C4, T0 = 60.0, 5.0, 30.0, 0.5, 50.0, 25.0
PL = lambda T: PL0 * math.exp((T - T0) / Tx)  # noqa: E731
f4 = lambda T: Pd + PL(T) - (T - T0) / R4     # noqa: E731
Tmin = T0 + Tx * math.log(Tx / (R4 * PL0))      # where the net heating is smallest
Ts = brentq(f4, T0, Tmin)
Tu = brentq(f4, Tmin, 400)
v.check("Ex 15-01.4a", Ts)
v.check("Ex 15-01.4b", PL(Ts))
G = R4 * jac(lambda x: [PL(x[0])], [Ts])[0, 0]
v.check("Ex 15-01.4c", G)
lin = jac(lambda x: [f4(x[0]) / C4], [Ts])[0, 0]                  # d(dT/dt)/dT at the equilibrium
v.check("Ex 15-01.4d", -1 / lin)
v.check("Ex 15-01.4e", Tu)
v.assert_true("the upper equilibrium is unstable (positive Jacobian)", jac(lambda x: [f4(x[0])], [Tu])[0, 0] > 0)
v.check("Ex 15-01.4h", Pd + PL(Ts))
v.check("Ex 15-01.4i", T0 + R4 * (Pd + PL0))
v.check("Ex 15-01.4j", Ts - (T0 + R4 * (Pd + PL0)))


def has_equilibrium(Rr):
    Tm = T0 + Tx * math.log(Tx / (Rr * PL0))
    return Pd + PL(Tm) - (Tm - T0) / Rr <= 0


lo_r, hi_r = 0.5, 1.0                                               # bisection on "an equilibrium exists"
for _ in range(80):
    mid = (lo_r + hi_r) / 2
    lo_r, hi_r = (mid, hi_r) if has_equilibrium(mid) else (lo_r, mid)
v.check("Ex 15-01.4f", lo_r)
v.check("Ex 15-01.4g", T0 + Tx * math.log(Tx / (lo_r * PL0)))
v.check("Ex 15-01.4k", 100 * (lo_r / R4 - 1))
run = solve_ivp(plants.leakage_rhs(Pd, PL0, Tx, 0.65, C4, T0), (0, 2000), [25.0], events=lambda t, y: y[0] - 150, **TIGHT)
v.assert_true("with R = 0.65 K/W the nonlinear model passes 150 °C in finite time", len(run.t_events[0]) == 1)
settle = solve_ivp(plants.leakage_rhs(Pd, PL0, Tx, R4, C4, T0), (0, 2000), [25.0], **TIGHT)
v.assert_true("with R = 0.5 K/W the nonlinear model settles at the lower equilibrium", abs(settle.y[0, -1] - Ts) < 1e-6)

# ---------------------------------------------------------------------------------------- Example 5
g, Lp = 9.81, 0.5
w0 = math.sqrt(-jac(lambda y: plants.pendulum_rhs(g, Lp)(0, y), [0.0, 0.0])[1, 0])
v.check("Ex 15-01.5a", w0)
v.check("Ex 15-01.5b", 2 * math.pi / w0)


def period(theta0):
    """Integrate from rest at theta0 and time the first return to rest (half a period), doubled."""
    ev = lambda t, y: y[1]  # noqa: E731
    ev.direction = 1
    sol = solve_ivp(plants.pendulum_rhs(g, Lp), (0, 5), [theta0, 0.0], events=ev, rtol=1e-12, atol=1e-12)
    return 2 * sol.t_events[0][0]


for (key_t, key_e), deg in ((("c", "d"), 30), (("e", "f"), 90)):
    th = math.radians(deg)
    T = period(th)
    v.assert_true(f"integration and elliptic integral agree at {deg}°", abs(T - 4 * math.sqrt(Lp / g) * ellipk(math.sin(th / 2) ** 2)) < 1e-8)
    v.check(f"Ex 15-01.5{key_t}", T)
    v.check(f"Ex 15-01.5{key_e}", 100 * (T * w0 / (2 * math.pi) - 1))
Jinv = jac(lambda y: plants.pendulum_rhs(g, Lp)(0, y), [math.pi, 0.0])
p_unst = max(np.linalg.eigvals(Jinv).real)
v.check("Ex 15-01.5g", math.log(2) / p_unst)
for key, deg in (("h", 30), ("i", 90)):
    th = math.radians(deg)
    v.check(f"Ex 15-01.5{key}", 100 * th**2 / 6)
for key, deg in (("j", 30), ("k", 90)):
    th = math.radians(deg)
    v.check(f"Ex 15-01.5{key}", 100 * (th - math.sin(th)) / th)
v.check("Txt 15-01.b", 100 * math.radians(17) ** 2 / 6)
v.check("Txt 15-01.c", 700 * 0.01)

# ---------------------------------------------------------------------------------------- problems
v.check("15-01.1a", 3)
v.check("15-01.1b", 4)
A, Bp = plants.msd(2.0, 10.0, 800.0)
e = np.linalg.eigvals(A)
v.check("15-01.2a", abs(e[0]))
v.check("15-01.2b", -e[0].real / abs(e[0]))
v.check("15-01.2c", plants.analogs(2.0, 10.0, 800.0)["force-voltage"]["C"] * 1e3)
A, Bp = plants.msd(0.01, 0.02, 4.0)                               # rotational: same form with J, B, K
e = np.linalg.eigvals(A)
v.check("15-01.3a", abs(e[0]))
v.check("15-01.3b", -e[0].real / abs(e[0]))
twist = solve_ivp(lambda t, y: A @ y + Bp * 0.2, (0, 200), [0, 0], **TIGHT).y[0, -1]
v.check("15-01.3c", twist)
v.check("15-01.3d", math.degrees(twist))
v.check("15-01.4a", -1 / (-1 / (4 * 2)))
v.check("15-01.4b", 40 + 15 * 4)
s4 = solve_ivp(lambda t, y: [(15 - (y[0] - 40) / 4) / 2], (0, 100), [40.0], events=lambda t, y: y[0] - 90, **TIGHT)
v.check("15-01.4c", s4.t_events[0][0])
A5 = 8e-3 ** 2
R_si, R_tim = 0.5e-3 / (140 * A5), 50e-6 / (5 * A5)
v.check("15-01.5a", R_si)
v.check("15-01.5b", 50 * R_si)
v.check("15-01.5c", R_tim)
v.check("15-01.5d", 50 * R_tim)
v.check("15-01.5e", R_tim / R_si)
v.check("15-01.5f", 140 / 5)
R6, K6, J6, V6 = 1.0, 0.02, 1e-5, 6.0
s6 = solve_ivp(lambda t, y: [(K6 * (V6 - K6 * y[0]) / R6) / J6], (0, 1), [0.0], **TIGHT)
v.check("15-01.6a", s6.y[0, -1])
v.check("15-01.6b", V6 / R6)
v.check("15-01.6c", K6 * V6 / R6)
v.check("15-01.6d", -1000 / jac(lambda w: [(K6 * (V6 - K6 * w[0]) / R6) / J6], [100.0])[0, 0])
w_load = brentq(lambda w: K6 * (V6 - K6 * w) / R6 - 0.03, 0, 300)
v.check("15-01.6e", (V6 - K6 * w_load) / R6)
v.check("15-01.6f", w_load)
v.check("15-01.6g", 100 * (1 - w_load / s6.y[0, -1]))
A7, _ = plants.motor(R6, 2e-3, K6, J6, 0.0)
t7 = sorted(-1 / np.linalg.eigvals(A7).real)
v.check("15-01.7a", t7[1] * 1e3)
v.check("15-01.7b", t7[0] * 1e3)
v.check("15-01.7c", 100 * (0.025 / t7[1] - 1))
v.check("15-01.7d", 0.025 / 0.002)
Ks = np.array([[200.0, -100.0], [-100.0, 100.0]])
ev8 = np.sort(np.linalg.eigvals(Ks).real)
v.check("15-01.8a", math.sqrt(ev8[0]))
v.check("15-01.8b", math.sqrt(ev8[1]))
v.check("15-01.8c", ev8[0])
v.check("15-01.8d", ev8[1])
x9, m9, k9 = 0.01, 0.05, 1e-4
i9 = x9 * math.sqrt(m9 * g / k9)
J9 = jac(lambda y: [y[1], g - (k9 / m9) * i9**2 / y[0] ** 2], [x9, 0.0])
p9 = max(np.linalg.eigvals(J9).real)
v.assert_true("maglev pole independent of m and k: sqrt(2g/x)", abs(p9 - math.sqrt(2 * g / x9)) < 1e-4)
v.check("15-01.9a", p9)
v.check("15-01.9b", math.log(2) / p9 * 1e3)
Pd10, PL010, Tx10, Ta10, R10, C10 = 40.0, 2.0, 25.0, 35.0, 0.8, 20.0
PL10 = lambda T: PL010 * math.exp((T - 25) / Tx10)  # noqa: E731
f10 = lambda T: Pd10 + PL10(T) - (T - Ta10) / R10   # noqa: E731
Tm10 = 25 + Tx10 * math.log(Tx10 / (R10 * PL010))
T10 = brentq(f10, Ta10, Tm10)
v.check("15-01.10a", T10)
v.check("15-01.10b", PL10(T10))
G10 = R10 * jac(lambda x: [PL10(x[0])], [T10])[0, 0]
v.check("15-01.10c", G10)
v.check("15-01.10d", -1 / jac(lambda x: [f10(x[0]) / C10], [T10])[0, 0])


def has_eq10(Rr):
    Tm = 25 + Tx10 * math.log(Tx10 / (Rr * PL010))
    return Pd10 + PL10(Tm) - (Tm - Ta10) / Rr <= 0


lo_r, hi_r = 0.5, 1.5
for _ in range(80):
    mid = (lo_r + hi_r) / 2
    lo_r, hi_r = (mid, hi_r) if has_eq10(mid) else (lo_r, mid)
v.check("15-01.10e", lo_r)
v.check("15-01.10f", 25 + Tx10 * math.log(Tx10 / (lo_r * PL010)))
v.check("15-01.10g", 100 * (lo_r / R10 - 1))
A11, B11 = plants.thermal_two_node(2.0, 8.0, 0.5, 30.0)
x_idle = -np.linalg.solve(A11, B11 * 2.0)
sol11 = solve_ivp(lambda t, y: A11 @ y + B11 * 15.0, (0, 20000), x_idle, method="Radau", rtol=1e-10, atol=1e-10,
                  events=lambda t, y: 25 + y[0] - 95, dense_output=True)
v.check("15-01.11a", 25 + (-np.linalg.solve(A11, B11 * 15.0))[0])
t11 = sorted(-1 / np.linalg.eigvals(A11).real)
v.check("15-01.11b", t11[0])
v.check("15-01.11c", t11[1])
v.check("15-01.11d", sol11.t_events[0][0])
v.check("15-01.11e", (15 - 2) * 2.0)
v.check("15-01.11f", 25 + sol11.sol(5.0)[0])
c12 = 2e-7
f12 = lambda w: (K6 * (V6 - K6 * w) / R6 - c12 * w * w) / J6  # noqa: E731
s12 = solve_ivp(lambda t, y: [f12(y[0])], (0, 2), [0.0], **TIGHT)
w12 = s12.y[0, -1]
v.check("15-01.12a", w12)
a12 = jac(lambda w: [f12(w[0])], [w12])[0, 0]
b12 = jac(lambda u: [(K6 * (u[0] - K6 * w12) / R6 - c12 * w12**2) / J6], [V6])[0, 0]
v.check("15-01.12b", -b12 / a12)
v.check("15-01.12c", -1000 / a12)
v.check("15-01.12d", w12 * 60 / (2 * math.pi))
v.check("15-01.12e", 2 * c12 * w12)
v.check("15-01.12f", K6**2 / R6 + 2 * c12 * w12)
A13 = np.array([[-10 / 1e-3, -1 / 1e-3], [1 / 1e-6, 0.0]])
e13 = np.linalg.eigvals(A13)
v.check("15-01.13a", abs(e13[0]))
v.check("15-01.13b", -e13[0].real / abs(e13[0]))
v.check("15-01.13c", e13[0].real)
v.check("15-01.13d", abs(e13[0].imag))
v.check("15-01.14a", 85 + 2 * 40)
v.check("15-01.14b", 120 + 2 * 2)

# ---------------------------------------------------------------------------------------- lab answers
v.check("Lab 15-01.a", Ta + one_node.y[0, -1])
v.check("Lab 15-01.b", Ta + sol3.sol(1)[0])
sol_m = solve_ivp(lambda t, y: A2 @ y + B2 * V, (0, 0.06), [0, 0], dense_output=True, **TIGHT)
fo = solve_ivp(lambda t, y: [(K * (V - K * y[0]) / R - B * y[0]) / J], (0, 0.06), [0.0], dense_output=True, **TIGHT)
v.check("Lab 15-01.c", sol_m.sol(0.005)[1])
v.check("Lab 15-01.d", fo.sol(0.005)[0])
v.check("Lab 15-01.e", sol_m.sol(0.05)[1])
v.check("Lab 15-01.f", fo.sol(0.05)[0])
v.check("Lab 15-01.g", 100 * (1 - fo.sol(0.05)[0] / sol_m.sol(0.05)[1]))
f06 = lambda T: Pd + PL(T) - (T - T0) / 0.6  # noqa: E731
T06 = brentq(f06, T0, T0 + Tx * math.log(Tx / (0.6 * PL0)))
v.check("Lab 15-01.h", T06)
v.check("Lab 15-01.i", 0.6 * jac(lambda x: [PL(x[0])], [T06])[0, 0])
v.check("Lab 15-01.j", -1 / jac(lambda x: [f06(x[0]) / C4], [T06])[0, 0])
v.check("Lab 15-01.k", 0.6 * C4)
s06 = solve_ivp(plants.leakage_rhs(Pd, PL0, Tx, 0.6, C4, T0), (0, 3000), [25.0], **TIGHT)
v.assert_true("R = 0.6 K/W settles at its lower equilibrium", abs(s06.y[0, -1] - T06) < 1e-6)

sys.exit(v.finish())
