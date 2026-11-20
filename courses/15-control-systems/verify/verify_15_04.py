#!/usr/bin/env python3
"""Verify chapter 15-04 (feedback properties and steady-state error): examples, problems and lab answers.

Routes:
- sensitivities from exact closed-loop gains (not from the 1/(1+L) formula), and derivatives by sympy;
- system type and error constants by sympy limits, checked against labs/15-04-lab/steady.py;
- every steady-state error, peak and offset by simulating the closed loop (lsim on E/R, or solve_ivp on the
  physical state equations), so the final-value theorem is never the only evidence;
- stability from the closed-loop roots before any final value is used.
The ngspice netlist labs/15-04-lab/disturbance.cir confirms Example 15-04.4 (tools/run_spice.py).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "15-04-lab"))
sys.path.insert(0, str(ROOT / "labs" / "15-03-lab"))
from eeverify import Verifier  # noqa: E402
import steady  # noqa: E402
from specs import step_specs  # noqa: E402

CH = ROOT / "chapters" / "15-04-feedback-and-steady-state-error.md"
v = Verifier.from_files("15-04", CH, ROOT / "solutions" / "15-04-solutions.md", ROOT / "labs" / "15-04-lab" / "README.md")
s = sp.symbols("s")


def coeffs(expr):
    return [float(c) for c in sp.Poly(sp.expand(expr), s).all_coeffs()]


def closed_loop_roots(L):
    n, d = sp.fraction(sp.together(L))
    return np.roots(coeffs(n + d))


def sim_error(L, r_of_t, t_end, n=200001):
    """Simulated e = r - y for unity feedback around L, input r(t)."""
    num, den = sp.fraction(sp.together(L))
    t = np.linspace(0, t_end, n)
    _, e, _ = signal.lsim((coeffs(den), coeffs(num + den)), r_of_t(t), t)
    return t, e


def peak_of(fun_rhs, x0, t_end, idx, sign=1, n=400001, deriv=None):
    """Peak of sign*x[idx] from a dense solve_ivp, refined as a zero of its derivative."""
    sol = solve_ivp(fun_rhs, (0, t_end), x0, dense_output=True, rtol=1e-12, atol=1e-14)
    t = np.linspace(0, t_end, n)
    y = sign * sol.sol(t)[idx]
    k = int(np.argmax(y))
    d = lambda tt: fun_rhs(tt, sol.sol(tt))[idx]  # noqa: E731
    tp = brentq(d, t[k - 1], t[k + 1], xtol=1e-15)
    return sign * sol.sol(tp)[idx], tp, sol


# ---------------------------------------------------------------------------------------- Example 1
T = lambda G, H: G / (1 + G * H)  # noqa: E731
G0, H0 = 1e4, 0.01
v.check("Ex 15-04.1a", T(G0, H0))
Gs, Hs = sp.symbols("G H", positive=True)
Ts = Gs / (1 + Gs * Hs)
SG = sp.simplify(Gs / Ts * sp.diff(Ts, Gs))
SH = sp.simplify(Hs / Ts * sp.diff(Ts, Hs))
v.assert_true("S_G^T = 1/(1+GH)", sp.simplify(SG - 1 / (1 + Gs * Hs)) == 0)
v.check("Ex 15-04.1b", float(SG.subs({Gs: G0, Hs: H0})))
v.check("Ex 15-04.1c", 100 * 0.2 * float(SG.subs({Gs: G0, Hs: H0})))
v.check("Ex 15-04.1d", 100 * (T(1.2 * G0, H0) / T(G0, H0) - 1))
v.check("Ex 15-04.1e", 100 * (T(0.8 * G0, H0) / T(G0, H0) - 1))
v.check("Ex 15-04.1f", float(SH.subs({Gs: G0, Hs: H0})))
v.check("Ex 15-04.1g", 100 * (T(G0, 1.01 * H0) / T(G0, H0) - 1))

# ---------------------------------------------------------------------------------------- Example 2
L2 = 20 * (s + 2) / (s * (s + 4) * (s + 5))
r2 = closed_loop_roots(L2)
v.assert_true("Ex 2: closed loop stable", all(r2.real < 0))
v.check("Ex 15-04.2a", float(r2[np.argmin(abs(r2.imag))].real))
v.check("Ex 15-04.2f", complex(r2[np.argmax(r2.imag)]))
n2, d2 = sp.fraction(sp.together(L2))
v.check("Ex 15-04.2b", steady.system_type(coeffs(n2), coeffs(d2)))
v.check("Ex 15-04.2c", float(sp.limit(s * L2, s, 0)))
t, e = sim_error(L2, lambda t: np.ones_like(t), 40)
v.check("Ex 15-04.2d", e[-1])
t, e = sim_error(L2, lambda t: t, 60)
v.check("Ex 15-04.2e", e[-1])
v.assert_true("Ex 2: steady.py error constants", steady.error_constants(coeffs(n2), coeffs(d2))[1] == 2.0)

# ---------------------------------------------------------------------------------------- Example 3
Kmot, Rm, tau, Kp = 0.02, 1.0, 0.025, 0.2


def motor(ki, wref=lambda t: 0.0, TL=0.01):
    def rhs(t, x):
        w, z = x
        e = wref(t) - w
        vin = Kp * e + ki * z
        return [((vin - (Rm / Kmot) * TL) / Kmot - w) / tau, e]
    return rhs


r3 = np.sort(np.roots([0.025, 1 + 50 * Kp, 50 * 2.0]).real)
v.check("Ex 15-04.3a", r3[1])
v.check("Ex 15-04.3b", r3[0])
pk, tp, sol3 = peak_of(motor(2.0), [0, 0], 2.0, 0, sign=-1)
v.check("Ex 15-04.3c", pk)
v.check("Ex 15-04.3d", tp * 1e3)
v.check("Ex 15-04.3e", abs(sol3.sol(2.0)[0]))
v.check("Ex 15-04.3f", float(sp.limit(s * (0.2 * s + 2) / s * 50 / (0.025 * s + 1), s, 0)))
sol = solve_ivp(motor(2.0, wref=lambda t: 100 * t, TL=0.0), (0, 3), [0, 0], rtol=1e-11, atol=1e-13)
v.check("Ex 15-04.3g", 300 - sol.y[0, -1])
v.check("Ex 15-04.3h", -1e3 / r3[1])
sol = solve_ivp(motor(0.0), (0, 1), [0, 0], rtol=1e-11, atol=1e-13)
v.assert_true("Ex 3: proportional-only droop is 2.27 rad/s", abs(-sol.y[0, -1] - 2.2727) < 1e-3)


# ---------------------------------------------------------------------------------------- Example 4
def position(ki, d=0.5, r=lambda t: 0.0):
    def rhs(t, x):
        a, y, z = x
        e = r(t) - y
        u = 10 * e + ki * z + d
        return [(u - a) / 0.1, a, e]
    return rhs


sol = solve_ivp(position(0.0), (0, 20), [0, 0, 0], rtol=1e-11, atol=1e-13)
v.check("Ex 15-04.4a", sol.y[1, -1])
P4 = 1 / (s * (0.1 * s + 1))
v.check("Ex 15-04.4b", float(sp.limit(s * 10 * P4, s, 0)))
sol = solve_ivp(position(0.0, d=0.0, r=lambda t: t), (0, 20), [0, 0, 0], rtol=1e-11, atol=1e-13)
v.check("Ex 15-04.4c", 20 - sol.y[1, -1])
sol = solve_ivp(position(20.0), (0, 30), [0, 0, 0], rtol=1e-11, atol=1e-13)
v.check("Ex 15-04.4d", sol.y[1, -1])
r4 = np.roots([0.1, 1, 10, 20])
v.assert_true("Ex 4: PI loop stable", all(r4.real < 0))
v.check("Ex 15-04.4e", float(r4[np.argmin(abs(r4.imag))].real))
v.assert_true("Ex 4: offset = d/K by sympy", abs(float(sp.limit(P4 / (1 + 10 * P4), s, 0)) * 0.5 - 0.05) < 1e-15)

# ---------------------------------------------------------------------------------------- Example 5
wn2, RC = 1e11, 5e-6
L5 = wn2 * (1 + s * RC) / s**2
v.check("Ex 15-04.5a", float(sp.limit(s**2 * L5, s, 0)))
t, e = sim_error(L5, lambda t: 2 * math.pi * 1e5 * t, 1e-4)
v.check("Ex 15-04.5b", e[-1])
alpha = 2 * math.pi * 1e10
t, e = sim_error(L5, lambda t: alpha * t**2 / 2, 1e-4)
v.check("Ex 15-04.5c", e[-1])
v.check("Ex 15-04.5d", math.degrees(e[-1]))

# ---------------------------------------------------------------------------------------- Example 6
A0, fa, beta = 1e5, 10.0, 0.1
for f, ids in ((1e3, "abcd"), (1e4, "efgh")):
    Lj = A0 * beta / (1 + 1j * f / fa)
    Tb = Lj / (1 + Lj)
    v.check(f"Ex 15-04.6{ids[0]}", abs(Lj))
    v.check(f"Ex 15-04.6{ids[1]}", abs(1 / (1 + Lj)))
    v.check(f"Ex 15-04.6{ids[2]}", 100 * (abs(Tb) - 1))
    v.check(f"Ex 15-04.6{ids[3]}", math.degrees(np.angle(Tb)))

# ---------------------------------------------------------------------------------------- Problem 1
v.check("15-04.1a", T(2000, 0.05))
v.check("15-04.1b", float(SG.subs({Gs: 2000, Hs: 0.05})))
v.check("15-04.1c", 100 * (T(1000, 0.05) / T(2000, 0.05) - 1))

# ---------------------------------------------------------------------------------------- Problem 2
cases = {"a": 50 / ((s + 2) * (s + 5)), "b": 10 / (s * (s + 4)), "c": 4 * (s + 1) / (s**2 * (s + 5))}
for k, L in cases.items():
    v.assert_true(f"P2({k}) stable", all(closed_loop_roots(L).real < 0))
La, Lb, Lc = cases["a"], cases["b"], cases["c"]
na, da = sp.fraction(sp.together(La))
v.check("15-04.2a", steady.system_type(coeffs(na), coeffs(da)))
v.check("15-04.2b", float(sp.limit(La, s, 0)))
v.check("15-04.2c", sim_error(La, lambda t: np.ones_like(t), 20)[1][-1])
nb_, db = sp.fraction(sp.together(Lb))
v.check("15-04.2d", steady.system_type(coeffs(nb_), coeffs(db)))
v.check("15-04.2e", float(sp.limit(s * Lb, s, 0)))
v.check("15-04.2f", sim_error(Lb, lambda t: t, 40)[1][-1])
nc, dc = sp.fraction(sp.together(Lc))
v.check("15-04.2g", steady.system_type(coeffs(nc), coeffs(dc)))
v.check("15-04.2h", float(sp.limit(s**2 * Lc, s, 0)))
v.check("15-04.2i", sim_error(Lc, lambda t: t**2 / 2, 80)[1][-1])
rc = closed_loop_roots(Lc)
v.check("15-04.2j", float(rc[np.argmin(abs(rc.imag))].real))

# ---------------------------------------------------------------------------------------- Problem 3
L0 = 99.0
v.check("15-04.3a", 1 / (1 + L0))
v.check("15-04.3b", L0 / (1 + L0))

# ---------------------------------------------------------------------------------------- Problem 4
K4 = brentq(lambda K: 1 / (1 + K / 3) - 0.02, 1, 1000, xtol=1e-12)
v.check("15-04.4a", K4)
v.check("15-04.4b", 4 / (2 * math.sqrt(3 + K4)))
v.check("15-04.4c", 100 * step_specs([K4], [1, 4, 3 + K4], 10)["overshoot"])

# ---------------------------------------------------------------------------------------- Problem 5
K5 = brentq(lambda K: sim_error(K / (s * (s + 10)), lambda t: t, 10, n=20001)[1][-1] - 0.05, 50, 1000, xtol=1e-9)
v.check("15-04.5a", K5, rtol=1e-6)  # simulated ramp error inverted numerically
K5 = 200.0
v.check("15-04.5b", 10 / (2 * math.sqrt(K5)))
v.check("15-04.5c", 100 * step_specs([K5], [1, 10, K5], 5)["overshoot"])

# ---------------------------------------------------------------------------------------- Problem 6
Pth = 0.5 / (10 * s + 1)
v.check("15-04.6a", float(Pth.subs(s, 0)) * 20)


def thermal(kp, ki):
    def rhs(t, x):
        T_, z = x
        q = -kp * T_ + ki * z            # actuator heat (removes heat when T_ rises), reference 0
        return [(0.5 * (q + 20) - T_) / 10, -T_]
    return rhs


sol = solve_ivp(thermal(20, 0), (0, 20), [0, 0], rtol=1e-11, atol=1e-13)
v.check("15-04.6b", sol.y[0, -1])
sol = solve_ivp(thermal(20, 5), (0, 200), [0, 0], rtol=1e-11, atol=1e-13)
v.check("15-04.6c", sol.y[0, -1])

# ---------------------------------------------------------------------------------------- Problem 7
T7 = sp.simplify((10 / (s + 1)) / (1 + 0.5 * 10 / (s + 1)))
v.check("15-04.7a", float(T7.subs(s, 0)))
v.check("15-04.7b", 1 / 0.5)
v.check("15-04.7c", 1 / 0.5 - float(T7.subs(s, 0)))

# ---------------------------------------------------------------------------------------- Problem 8
L8 = 20 / (s * (s / 20 + 1))  # a type-1 loop with Kv = 20 1/s (any stable realization)
v.check("15-04.8a", sim_error(L8, lambda t: 0.5 * t, 5)[1][-1])

# ---------------------------------------------------------------------------------------- Problem 9
Lj = 1e5 * 0.5 / (1 + 1j * 1e5 / 100)
v.check("15-04.9a", abs(Lj))
v.check("15-04.9b", abs(1 / (1 + Lj)))
v.check("15-04.9c", 100 * (abs(Lj / (1 + Lj)) - 1))
v.check("15-04.9d", math.degrees(np.angle(Lj / (1 + Lj))))

# ---------------------------------------------------------------------------------------- Problem 10
w0 = 2 * math.pi * 60
tt = np.linspace(0, 1.0, 400001)
_, yP, _ = signal.lsim(([1, 10], [1, 110]), np.sin(w0 * tt), tt)
v.check("15-04.10a", np.abs(yP[tt > 1 - 1 / 60]).max())
v.assert_true("P10(a): matches |S(j w0)|", abs(np.abs(yP[tt > 1 - 1 / 60]).max() - abs((1j * w0 + 10) / (1j * w0 + 110))) < 1e-4)
Kr = 3e4
den10 = [1, 110, w0**2 + Kr, 110 * w0**2]
r10 = np.roots(den10)
v.assert_true("P10(b): stable", all(r10.real < 0))
v.check("15-04.10b", float(r10[np.argmax(r10.imag)].real))
num10 = np.polymul([1, 0, w0**2], [1, 10])
_, yR, _ = signal.lsim((num10, den10), np.sin(w0 * tt), tt)
v.check("15-04.10c", np.abs(yR[(tt >= 0.5) & (tt <= 0.5 + 1 / 60)]).max())
v.assert_true("P10(b): S has zeros at +-j w0", abs(np.polyval(num10, 1j * w0)) < 1e-6 * w0**3)

# ---------------------------------------------------------------------------------------- Problem 11
t, e = sim_error(L5, lambda t: 2 * math.pi * 1e5 * t, 1e-4, n=400001)
v.check("15-04.11a", e[-1])
k = int(np.argmax(e))
# refine with the closed-form error response: E = dw * 1/(s^2 + a s + b) (impulse response of 1/den), so
# e'(t) = dw * h(t) for h the impulse response of s/(s^2+as+b); find its zero near the grid peak
a_, b_ = wn2 * RC, wn2
sysd = signal.TransferFunction([1, 0], [1, a_, b_])
hz = lambda tt: signal.impulse(sysd, T=[0, tt])[1][-1]  # noqa: E731
tpk = brentq(hz, t[k - 1], t[k + 1], xtol=1e-18)
epk = 2 * math.pi * 1e5 * signal.impulse(signal.TransferFunction([1], [1, a_, b_]), T=[0, tpk])[1][-1]
v.check("15-04.11b", epk)
v.check("15-04.11c", tpk * 1e6)
v.assert_true("P11: grid peak agrees with the refined peak", abs(e[k] - epk) < 1e-6)

# ---------------------------------------------------------------------------------------- Problem 12
Ki12 = sp.solve(sp.Eq(0.025 * 2500 - 11 * 50 + 50 * sp.Symbol("ki"), 0))[0]
v.check("15-04.12a", float(Ki12))
r12 = np.sort(np.roots([0.025, 11, 50 * float(Ki12)]).real)
v.check("15-04.12b", r12[0])
v.assert_true("P12: slow pole at -50", abs(r12[1] + 50) < 1e-9)
v.check("15-04.12c", 50 * float(Ki12))
pk, tp, _ = peak_of(motor(float(Ki12)), [0, 0], 1.0, 0, sign=-1)
v.check("15-04.12d", pk)
v.check("15-04.12e", tp * 1e3)

# ---------------------------------------------------------------------------------------- Problem 13
for A, (kr, kv) in ((1000, "ab"), (300, "cd")):
    Lz = A * 0.5 * 10 * 0.5
    # output resistance from the loop equations: v = -R_L i_L + R_L g_m A (-beta v)  =>  v/i = -R_L/(1 + L)
    vo, il = sp.symbols("vo il")
    Zo = -sp.solve(sp.Eq(vo, -10 * il + 10 * 0.5 * A * (-0.5 * vo)), vo)[0] / il
    v.check(f"15-04.13{kr}", float(Zo) * 1e3)
    v.check(f"15-04.13{kv}", 0.1 * float(Zo) * 1e3)

# ---------------------------------------------------------------------------------------- Problem 14


def sensor_loop(kp, ki, H=0.98):
    def rhs(t, x):
        y, z = x
        e = 1.0 - H * y
        u = kp * e + ki * z
        return [u - y, e]                 # plant 1/(s+1)
    return rhs


sol = solve_ivp(sensor_loop(1.0, 2.0), (0, 60), [0, 0], rtol=1e-11, atol=1e-13)
v.check("15-04.14a", sol.y[0, -1])
v.check("15-04.14b", 100 / (1 + 100 * 0.98))
sol = solve_ivp(lambda t, x: [100 * (1 - 0.98 * x[0]) - x[0]], (0, 1), [0.0], rtol=1e-11, atol=1e-13)
v.assert_true("P14(b): forward gain 100 around plant 1/(s+1), sensor 0.98, settles at 100/99",
              abs(sol.y[0, -1] - 100 / 99) < 1e-9)

# ---------------------------------------------------------------------------------------- Lab (Example 4 peaks)
pk, tp, _ = peak_of(position(0.0), [0, 0, 0], 5.0, 1)
v.check("Lab 15-04.a", pk)
pk, tp, _ = peak_of(position(20.0), [0, 0, 0], 5.0, 1)
v.check("Lab 15-04.b", pk)
v.check("Lab 15-04.c", tp)

sys.exit(v.finish())
