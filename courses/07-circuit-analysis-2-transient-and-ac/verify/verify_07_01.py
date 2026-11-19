#!/usr/bin/env python3
"""Verify every number published in chapter 07-01, its solutions and its lab handout.

Independent routes. The text applies i = C dv/dt and v = L di/dt to straight-line waveforms by inspection,
and uses closed forms for energies, combinations, resonance and the decoupling budget. This script instead
differentiates and integrates sampled waveforms numerically, integrates p = vi to get energies, solves the
charge-redistribution and inductor-saturation problems as ODEs, obtains series/parallel combinations and the
capacitive divider from charge conservation with a linear solve, finds self-resonance by minimizing the
complex impedance numerically, and solves DC steady states as resistive circuits (C open, L short) with a
sparse-tableau solver.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("07-01", C_DIR / "chapters" / "07-01-capacitors-and-inductors.md",
                        C_DIR / "solutions" / "07-01-solutions.md", C_DIR / "labs" / "07-01-lab" / "README.md")


def tableau(elements):
    """Sparse tableau with dependent sources. Each element is (name, kind, a, b, value) where
    branch current flows a -> b through the element and branch voltage is v_a - v_b:
      R: v = value * i;  I: i = value;  V: v = value;
      G: i = g * (v_c - v_d) with value = (c, d, g);   E: v = mu * (v_c - v_d) with value = (c, d, mu);
      F: i = beta * i_ctrl with value = (ctrl, beta);  H: v = r * i_ctrl with value = (ctrl, r)."""
    nodes = sorted({n for _, _, a, b, _ in elements for n in (a, b) if n != "0"})
    nn, nb = len(nodes), len(elements)
    idx = {n: k for k, n in enumerate(nodes)}
    bidx = {el[0]: k for k, el in enumerate(elements)}
    A = np.zeros((nn, nb))
    for k, (_, _, a, b, _) in enumerate(elements):
        if a != "0":
            A[idx[a], k] += 1.0
        if b != "0":
            A[idx[b], k] -= 1.0
    size = nn + 2 * nb
    M, z = np.zeros((size, size)), np.zeros(size)
    M[:nn, nn:nn + nb] = A
    M[nn:nn + nb, :nn] = -A.T
    M[nn:nn + nb, nn + nb:] = np.eye(nb)

    def node_col(n):
        return None if n == "0" else idx[n]

    for k, (_, kind, _, _, val) in enumerate(elements):
        r = nn + nb + k
        ci, cv = nn + k, nn + nb + k
        if kind == "R":
            M[r, cv], M[r, ci] = 1.0, -val
        elif kind == "I":
            M[r, ci], z[r] = 1.0, val
        elif kind == "V":
            M[r, cv], z[r] = 1.0, val
        elif kind in "GE":
            c, d, gain = val
            M[r, ci if kind == "G" else cv] = 1.0
            for node, sgn in ((c, -1.0), (d, 1.0)):
                if node_col(node) is not None:
                    M[r, node_col(node)] += sgn * gain
        elif kind in "FH":
            ctrl, gain = val
            M[r, ci if kind == "F" else cv] = 1.0
            M[r, nn + bidx[ctrl]] -= gain
        else:
            raise ValueError(kind)
    x = np.linalg.solve(M, z)
    e = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    cur = {el[0]: x[nn + k] for k, el in enumerate(elements)}
    vol = {el[0]: x[nn + nb + k] for k, el in enumerate(elements)}
    return e, cur, vol


def slope(t, y, at):
    """Numerical derivative of a sampled waveform at time `at` (central difference on a fine grid)."""
    d = np.gradient(y, t)
    return float(np.interp(at, t, d))


def zmag(f, C, L, R, n=1):
    w = 2 * math.pi * f
    return abs(R / n + 1j * w * L / n + 1 / (1j * w * C * n))


# ================================================================ examples
# ---- Example 07-01.1
t = np.linspace(0, 3e-3, 300001)
vc = np.interp(t, [0, 1e-3, 2e-3, 2.5e-3, 3e-3], [0, 5, 5, 0, 0])
C1 = 10e-6
v.check("Ex 07-01.1a", 1e3 * C1 * slope(t, vc, 0.5e-3))
v.check("Ex 07-01.1b", 1e3 * C1 * slope(t, vc, 2.25e-3))
ic = C1 * np.gradient(vc, t)
w_t = np.concatenate([[0], np.cumsum(0.5 * (vc[1:] * ic[1:] + vc[:-1] * ic[:-1]) * np.diff(t))])   # ∫ p dt
v.check("Ex 07-01.1c", 1e6 * w_t.max(), tol=0.05)
v.check("Ex 07-01.1d", 1e3 * np.max(vc * ic), tol=0.05)

# ---- Example 07-01.2
L2 = 4.7e-6
tl = np.linspace(0, 5e-6, 500001)
il = np.interp(tl, [0, 2e-6, 5e-6], [1, 3, 1])
v.check("Ex 07-01.2a", L2 * slope(tl, il, 1e-6))
v.check("Ex 07-01.2b", L2 * slope(tl, il, 3.5e-6))
energy_L = lambda i: quad(lambda x: L2 * x, 0, i)[0]          # ∫ L i di  # noqa: E731
v.check("Ex 07-01.2c", 1e6 * energy_L(3.0))
v.check("Ex 07-01.2d", 1e6 * energy_L(1.0))
v.check("Ex 07-01.2e", 1e6 * (energy_L(3.0) - energy_L(1.0)))
vl = L2 * np.gradient(il, tl)
up = np.trapezoid(np.where(vl > 0, vl, 0), tl)
dn = -np.trapezoid(np.where(vl < 0, vl, 0), tl)
v.assert_true("Ex 2: volt-second balance over the period", abs(up - dn) < 1e-9)
v.check("Ex 07-01.2f", 1e6 * up, tol=0.01)


# ---- Example 07-01.3: charge conservation. Unknowns: q (on the 4 uF), v4, vp (pair voltage).
# Equations: v4 + vp = 12; q = 4 v4; q = (2 + 6) vp   (µF, V, µC)
A = np.array([[0, 1, 1], [1, -4, 0], [1, 0, -8]], float)
q3, v4, vp = np.linalg.solve(A, [12, 0, 0])
v.check("Ex 07-01.3a", q3 / 12)
v.check("Ex 07-01.3b", q3)
v.check("Ex 07-01.3c", v4)
v.check("Ex 07-01.3d", vp)
v.check("Ex 07-01.3e", 2 * vp)
v.check("Ex 07-01.3f", 6 * vp)
v.check("Ex 07-01.3g", 0.5 * 4 * v4 ** 2 + 0.5 * 2 * vp ** 2 + 0.5 * 6 * vp ** 2)

# ---- Example 07-01.4
tk = np.linspace(0, 1e-6, 1001)
ik = 0.05 * (1 - tk / 1e-6)
v.check("Ex 07-01.4a", abs(0.1 * slope(tk, ik, 0.5e-6)))
v.check("Ex 07-01.4b", 1e6 * quad(lambda x: 0.1 * x, 0, 0.05)[0])
v.check("Ex 07-01.4c", 12 + 0.7)                              # supply plus one (nominal) diode drop
v.check("Ex 07-01.4d", 12 / 0.05)

# ---- Example 07-01.5
v.check("Ex 07-01.5a", 1e6 * brentq(lambda C: 1.0 * 10e-9 / C - 0.05, 1e-9, 1e-3))
v.check("Ex 07-01.5b", 0.40 * 10)
v.check("Ex 07-01.5c", 0.5e-9 * 1.0 / 1e-9)
v.check("Ex 07-01.5d", next(n for n in range(1, 1000) if 0.5e-9 / n * 1.0 / 1e-9 <= 0.025 + 1e-15))
res = minimize_scalar(lambda lf: zmag(10 ** lf, 10e-6, 0.5e-9, 5e-3), bounds=(5, 8), method="bounded",
                      options={"xatol": 1e-12})
v.check("Ex 07-01.5e", 10 ** res.x / 1e6)
v.check("Ex 07-01.5f", zmag(1e5, 10e-6, 0.5e-9, 5e-3))
v.check("Ex 07-01.5g", zmag(1e8, 10e-6, 0.5e-9, 5e-3))
res4 = minimize_scalar(lambda lf: zmag(10 ** lf, 4e-6, 0.5e-9, 5e-3), bounds=(5, 8), method="bounded",
                       options={"xatol": 1e-12})
v.check("Ex 07-01.5h", 10 ** res4.x / 1e6)
v.check("Ex 07-01.5i", zmag(1e5, 4e-6, 0.5e-9, 5e-3))


# ---- Example 07-01.6: integrate the integrator's ODE; differentiate the triangle numerically
def integrator(vin, R, C, t_end):
    sol = solve_ivp(lambda tt, y: [-vin(tt) / (R * C)], (0, t_end), [0.0], rtol=1e-10, atol=1e-12, dense_output=True)
    return sol


s6 = integrator(lambda tt: 1.0, 10e3, 10e-9, 2e-3)
v.check("Ex 07-01.6a", (s6.sol(0.5e-3)[0] - s6.sol(0.25e-3)[0]) / 0.25)        # V per ms
v.check("Ex 07-01.6b", 1e3 * brentq(lambda tt: s6.sol(tt)[0] + 10, 1e-6, 2e-3))
ttri = np.linspace(0, 1e-3, 100001)
tri = np.interp(ttri, [0, 0.5e-3, 1e-3], [-1, 1, -1])
v.check("Ex 07-01.6c", slope(ttri, tri, 0.25e-3))
v.check("Ex 07-01.6d", abs(-10e3 * 10e-9 * slope(ttri, tri, 0.25e-3)))

# ================================================================ solutions
tt = np.linspace(0, 0.02, 200001)
vs = 5 * np.sin(2 * math.pi * 50 * tt)
v.check("07-01.1a", 1e3 * np.max(np.abs(47e-6 * np.gradient(vs, tt))), tol=0.005)
v.check("07-01.1b", 1e6 * 0.5 * 47e-6 * vs.max() ** 2, tol=0.05)

i2 = lambda x: 2 * (1 - math.exp(-x / 1e-3))                  # noqa: E731
d = 1e-9
v.check("07-01.2a", 10e-3 * (i2(d) - i2(0)) / d, tol=0.001)
v.check("07-01.2b", 10e-3 * (i2(1e-3 + d) - i2(1e-3 - d)) / (2 * d), tol=0.0005)
v.check("07-01.2c", 1e3 * quad(lambda x: 10e-3 * x, 0, 2)[0])

s3 = solve_ivp(lambda x, y: [(10e-3 if x < 30e-3 else -5e-3) / 100e-6], (0, 50e-3), [2.0], max_step=1e-5,
               rtol=1e-10, atol=1e-12, dense_output=True)
v.check("07-01.3a", s3.sol(30e-3)[0], tol=0.002)
v.check("07-01.3b", s3.sol(50e-3)[0], tol=0.002)

v.check("07-01.4a", 2 + 1 / (1 / 3 + 1 / 6))
v.check("07-01.4b", 3 + 1 / (1 / 6 + 1 / 3))

A5 = np.array([[1, 1], [1.0, -2.0]])                          # v1 + v2 = 9; 1*v1 = 2*v2 (equal charge)
v1_5, v2_5 = np.linalg.solve(A5, [9, 0])
v.check("07-01.5a", v1_5)
v.check("07-01.5b", v2_5)
v.check("07-01.5c", tableau([("V", "V", "s", "0", 9.0), ("R1", "R", "s", "m", 10.0), ("R2", "R", "m", "0", 10.0)])[0]["m"])


def share(C1, C2, V0, R):
    tau = R * C1 * C2 / (C1 + C2)
    sol = solve_ivp(lambda x, y: [-(y[0] - y[1]) / R / C1, (y[0] - y[1]) / R / C2, (y[0] - y[1]) ** 2 / R],
                    (0, 30 * tau), [V0, 0, 0], rtol=1e-11, atol=1e-15)
    return sol.y[:, -1]


v1f, v2f, wl = share(4.7e-6, 2.2e-6, 12.0, 1.0)
v.check("07-01.6a", v1f)
v.check("07-01.6b", 1e6 * 0.5 * 4.7e-6 * 144)
v.check("07-01.6c", 1e6 * (0.5 * 4.7e-6 * v1f ** 2 + 0.5 * 2.2e-6 * v2f ** 2))
v.check("07-01.6d", 1e6 * wl)
v.assert_true("07-01.6: the loss is the same with a 100x smaller resistor",
              abs(share(4.7e-6, 2.2e-6, 12.0, 0.01)[2] - wl) < 1e-10)

D = brentq(lambda dd: 8.7 * dd - 3.3 * (1 - dd), 0, 1)
v.check("07-01.7a", D)
v.check("07-01.7b", 1e6 * D * 2e-6)
v.check("07-01.7c", 8.7 * D * 2e-6 / 10e-6)

v.check("07-01.8a", 0.05 * 0.5 / 10e-6)
v.check("07-01.8b", 1e3 * quad(lambda x: 0.05 * x, 0, 0.5)[0])
s8 = solve_ivp(lambda x, y: [-30 / 0.05], (0, 2e-3), [0.5], events=lambda x, y: y[0], rtol=1e-12, atol=1e-14)
v.check("07-01.8c", 1e3 * s8.t_events[0][0])

Cneed = 5 * 50e-9 / 0.03
v.check("07-01.9a", 1e6 * Cneed)
v.check("07-01.9b", math.ceil(Cneed / (0.35 * 22e-6)))
Lmax = 0.02 / (5 / 2e-9)
v.check("07-01.9c", 1e12 * Lmax)
v.check("07-01.9d", math.ceil(0.3e-9 / Lmax - 1e-9))

r10 = minimize_scalar(lambda lf: zmag(10 ** lf, 100e-9, 0.4e-9, 1e-9), bounds=(6, 9), method="bounded",
                      options={"xatol": 1e-12})
v.check("07-01.10a", 10 ** r10.x / 1e6)
v.check("07-01.10b", zmag(1e9, 100e-9, 0.4e-9, 0.0))

s11 = integrator(lambda x: 0.5 if x <= 2 else 0.0, 100e3, 1e-6, 2.0)
v.check("07-01.11a", s11.sol(2.0)[0])
s11b = integrator(lambda x: 1e-3, 100e3, 1e-6, 2000.0)
v.check("07-01.11b", s11b.sol(10.0)[0])
v.check("07-01.11c", brentq(lambda x: s11b.sol(x)[0] + 12, 1, 2000))

w = 2 * math.pi * 1e3
t12 = np.linspace(0, 1e-3, 100001)
i12 = 2 * np.sin(w * t12)
v12 = 1e-3 * np.gradient(i12, t12)
p12 = v12 * i12
v.check("07-01.12a", v12.max(), tol=0.005)
v.check("07-01.12b", p12.max(), tol=0.005)
v.assert_true("07-01.12: average power over a period is zero", abs(np.trapezoid(p12, t12)) < 1e-6)
spec = np.abs(np.fft.rfft(p12[:-1]))
v.check("07-01.12c", np.argmax(spec[1:]) + 1)                 # cycles per 1 ms window = kHz
v.check("07-01.12d", 1e3 * 0.5 * 1e-3 * 2 ** 2)


def sat(L_of_i, i0, vv, t_end):
    sol = solve_ivp(lambda x, y: [vv / L_of_i(y[0])], (0, t_end), [i0], max_step=1e-10, rtol=1e-10, atol=1e-12,
                    dense_output=True)
    return sol


v.check("07-01.13a", sat(lambda i: 10e-6, 2.5, 8.7, 1e-6).y[0, -1])
s13 = sat(lambda i: 10e-6 if i < 3 else 2e-6, 2.5, 8.7, 1e-6)
v.check("07-01.13b", 1e6 * brentq(lambda x: s13.sol(x)[0] - 3, 0, 1e-6, xtol=1e-15))
v.check("07-01.13c", s13.y[0, -1])

e14, c14, _ = tableau([("V", "V", "s", "0", 12.0), ("R1", "R", "s", "a", 2.0), ("RL", "R", "a", "b", 1e-9),
                       ("R2", "R", "b", "0", 4.0)])       # C open, L short (kΩ, mA)
v.check("07-01.14a", c14["R2"])
v.check("07-01.14b", e14["a"])
v.check("07-01.14c", 1e6 * 0.5 * 1e-6 * e14["a"] ** 2)
v.check("07-01.14d", 1e9 * 0.5 * 10e-3 * (c14["R2"] * 1e-3) ** 2)

# ================================================================ lab
_, _, w_lab = share(10e-6, 10e-6, 10.0, 1.0)
v.check("Lab 07-01.a", 1e6 * w_lab)
v.check("Lab 07-01.b", 10.0 / 1.0)
v.check("Lab 07-01.c", 10.0 / 0.01)
r1 = minimize_scalar(lambda lf: zmag(10 ** lf, 10e-6, 0.5e-9, 5e-3, n=20), bounds=(5, 8), method="bounded",
                     options={"xatol": 1e-12})
v.check("Lab 07-01.d", 10 ** r1.x / 1e6)
v.check("Lab 07-01.e", 1e3 * zmag(10 ** res.x, 10e-6, 0.5e-9, 5e-3))
v.check("Lab 07-01.f", 1e3 * zmag(10 ** r1.x, 10e-6, 0.5e-9, 5e-3, n=20))
v.check("Lab 07-01.g", 1e6 * 3 * 0.5 * 10e-6 * (100e-6 / 30e-6) ** 2, tol=0.5)
rh = minimize_scalar(lambda lf: zmag(10 ** lf, 1e-6, 0.5e-9, 5e-3), bounds=(5, 9), method="bounded",
                     options={"xatol": 1e-12})
v.check("Lab 07-01.h", 10 ** rh.x / 1e6)
v.check("Lab 07-01.i", brentq(lambda Lp: 1 / (2 * math.pi * math.sqrt(Lp * 1e-12 * 10e-6)) - 10e6, 0.1, 1000, xtol=1e-12))

# P15: pre-charged series capacitors discharged through 10 k (simulated)
C1p, C2p, Rp = 2e-6, 3e-6, 10e3
s15 = solve_ivp(lambda t, x: [-(x[0] + x[1]) / Rp / C1p, -(x[0] + x[1]) / Rp / C2p], (0, 0.3), [5.0, 2.0],
                rtol=1e-11, atol=1e-14, dense_output=True)
v15f = s15.y[:, -1]
v.check("07-01.15b", 5.0 + 2.0)
tc = brentq(lambda t: s15.sol(t).sum() - 7.0 / math.e, 1e-4, 0.1)
v.check("07-01.15e", 1e3 * tc)
v.check("07-01.15a", 1e6 * tc / Rp)
v.check("07-01.15c", 1e6 * (0.5 * C1p * 25 + 0.5 * C2p * 4))
v.check("07-01.15d", 1e6 * 0.5 * (tc / Rp) * 49)
v.check("07-01.15f", v15f[0])
v.check("07-01.15g", v15f[1])
tt15 = np.linspace(0, 0.3, 300001)
v.check("07-01.15h", 1e6 * np.trapezoid(s15.sol(tt15).sum(axis=0) ** 2 / Rp, tt15))
v.check("07-01.15i", 1e6 * (0.5 * C1p * v15f[0] ** 2 + 0.5 * C2p * v15f[1] ** 2))

v.finish()
