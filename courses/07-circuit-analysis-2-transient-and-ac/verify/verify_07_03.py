#!/usr/bin/env python3
"""Verify every published number in chapter 07-03 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter derives closed-form results (α, ω0, ζ, the master formulas, peak
formulas). Here each circuit is instead written as state equations dx/dt = A x + g u straight from
KCL/KVL, natural frequencies are taken as numerical eigenvalues of A, and waveforms, peaks, zero
crossings and settling times come from integrating the state equations with scipy's solve_ivp.
The ngspice netlists in labs/07-03-lab are run separately by tools/run_spice.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-03",
    COURSE / "chapters" / "07-03-second-order-rlc-transients.md",
    COURSE / "solutions" / "07-03-solutions.md",
    COURSE / "labs" / "07-03-lab" / "README.md",
)
pi, sqrt, exp, ln = math.pi, math.sqrt, math.exp, math.log


# ----------------------------------------------------------------------------------- helpers
def simulate(A, g, x0, t_end, n_steps=400):
    """Integrate dx/dt = A x + g (constant input already folded into g) and return a dense solution.

    DOP853 with tight tolerances; its 7th-order dense output is accurate between steps, so the step
    is only capped (at t_end/n_steps) to make sure no fast feature is stepped over."""
    A = np.asarray(A, float)
    g = np.asarray(g, float)
    scale = max(1.0, float(np.max(np.abs(x0))), float(np.max(np.abs(np.linalg.solve(A, g)))) if np.linalg.det(A) else 1.0)
    return solve_ivp(lambda t, x: A @ x + g, (0.0, t_end), np.asarray(x0, float), method="DOP853",
                     rtol=1e-11, atol=1e-13 * scale, dense_output=True, max_step=t_end / n_steps)


def extreme(f, t0, t1, kind="max", n=20001):
    """Global extreme of a scalar function on [t0, t1]: dense grid, then a tight bounded refinement."""
    t = np.linspace(t0, t1, n)
    y = np.asarray(f(t), float)
    k = int(np.argmax(y) if kind == "max" else np.argmin(y))
    lo, hi = t[max(k - 1, 0)], t[min(k + 1, n - 1)]
    sgn = -1.0 if kind == "max" else 1.0
    r = minimize_scalar(lambda tt: sgn * float(f(tt)), bounds=(lo, hi), method="bounded",
                        options={"xatol": (hi - lo) * 1e-9})
    return r.x, float(f(r.x))


def settle_time(f, final, band, t_end, n=100001):
    """Last time |f - final| exceeds band, refined between grid points by brentq."""
    t = np.linspace(0.0, t_end, n)
    y = f(t)
    out = np.where(np.abs(y - final) > band)[0]
    k = out[-1]
    h = lambda tt: abs(float(f(tt)) - final) - band  # noqa: E731
    return brentq(h, t[k], t[k + 1], xtol=1e-18)


def os_formula(z):
    return exp(-pi * z / sqrt(1 - z * z))


def damping_from_eigs(A):
    """α, ω0 and ζ of the complex (or real) pair of a 2x2 state matrix, from its eigenvalues."""
    ev = np.linalg.eigvals(np.asarray(A, float))
    w0 = sqrt(abs(np.prod(ev)))
    a = -float(np.sum(ev).real) / 2
    return a, w0, a / w0, ev


def series_A(R, L, C):
    """States (i, vC): L di/dt = u - R i - vC ; C dvC/dt = i."""
    return np.array([[-R / L, -1 / L], [1 / C, 0.0]])


def parallel_A(R, L, C):
    """States (v, iL): C dv/dt = -v/R - iL ; L diL/dt = v."""
    return np.array([[-1 / (R * C), -1 / C], [1 / L, 0.0]])


# ================================================================================ Example 1
L1, C1, R1 = 100e-6, 1e-6, 5.0
v.check("Ex 07-03.1a", sqrt(L1 / C1))
a_s, w0_s, z_s, ev_s = damping_from_eigs(series_A(R1, L1, C1))
v.check("Ex 07-03.1b", w0_s / 1e3)
v.check("Ex 07-03.1c", w0_s / (2 * pi) / 1e3)
v.check("Ex 07-03.1d", a_s / 1e3)
v.check("Ex 07-03.1e", z_s)
v.check("Ex 07-03.1f", 1 / (2 * z_s))
v.check("Ex 07-03.1g", abs(ev_s[0].imag) / 1e3)
a_p, w0_p, z_p, ev_p = damping_from_eigs(parallel_A(R1, L1, C1))
v.check("Ex 07-03.1h", a_p / 1e3)
v.check("Ex 07-03.1i", z_p)
v.check("Ex 07-03.1j", 1 / (2 * z_p))
v.assert_true("Ex1 parallel roots coincide (critical damping)", abs(ev_p[0] - ev_p[1]) < 1e-3 * abs(ev_p[0]))
Rcrit = brentq(lambda R: damping_from_eigs(series_A(R, L1, C1))[2] - 1.0, 1, 100)
v.check("Ex 07-03.1k", Rcrit)
Rpar = brentq(lambda R: damping_from_eigs(parallel_A(R, L1, C1))[2] - 0.25, 1, 1000)
v.check("Ex 07-03.1l", Rpar)

# ================================================================================ Example 2
# Before t = 0: 10 V through R1 = 10 ohm into node a with L, C, R2 to ground. DC: solve the nodal
# equation with the inductor as a 1e-9 ohm resistor (a short) and C open, then KCL for the inductor.
Vs2, Rs2, L2, C2, R2b = 10.0, 10.0, 10e-3, 1e-6, 25.0
va = Vs2 / Rs2 / (1 / Rs2 + 1 / R2b + 1 / 1e-9)
iL0 = (Vs2 - va) / Rs2 - va / R2b
v.check("Ex 07-03.2a", iL0)
A2 = parallel_A(R2b, L2, C2)
x0_2 = np.array([0.0, iL0])
dvdt0 = (A2 @ x0_2)[0]
v.check("Ex 07-03.2b", dvdt0 / 1e6)
a2, w02, z2, ev2 = damping_from_eigs(A2)
v.check("Ex 07-03.2c", a2 / 1e3)
v.check("Ex 07-03.2d", w02 / 1e3)
v.check("Ex 07-03.2e", z2)
s1, s2 = sorted(ev2.real, reverse=True)
v.check("Ex 07-03.2f", s1 / 1e3)
v.check("Ex 07-03.2g", s2 / 1e3)
sol2 = simulate(A2, [0, 0], x0_2, 3e-3)
v2 = lambda t: sol2.sol(t)[0]  # noqa: E731
# A1 from a least-squares fit of the simulated waveform to A1 e^{s1 t} + A2 e^{s2 t}
tt = np.linspace(0, 2e-3, 2001)
M = np.column_stack([np.exp(s1 * tt), np.exp(s2 * tt)])
coef = np.linalg.lstsq(M, v2(tt), rcond=None)[0]
v.check("Ex 07-03.2h", coef[0])
tmin, vmin = extreme(v2, 0, 1e-3, "min")
v.check("Ex 07-03.2i", tmin * 1e6)
v.check("Ex 07-03.2j", vmin)
# energy dissipated in R2 = ∫ v²/R2 dt
Ediss = np.trapezoid(v2(np.linspace(0, 3e-3, 300001)) ** 2 / R2b, np.linspace(0, 3e-3, 300001))
v.check("Ex 07-03.2k", Ediss * 1e3, tol=5e-4)
v.check("Ex 07-03.2l", -iL0 * R2b)

# ================================================================================ Example 3
V3, L3, R3, C3 = 12.0, 1e-6, 0.05, 10e-6
v.check("Ex 07-03.3a", sqrt(L3 / C3))
A3 = series_A(R3, L3, C3)
a3, w03, z3, ev3 = damping_from_eigs(A3)
v.check("Ex 07-03.3b", w03 / (2 * pi) / 1e3)
v.check("Ex 07-03.3c", z3)
sol3 = simulate(A3, [V3 / L3, 0], [0, 0], 400e-6)
tpk3, vpk3 = extreme(lambda t: sol3.sol(t)[1], 0, 30e-6)
v.check("Ex 07-03.3d", (vpk3 / V3 - 1) * 100)
v.check("Ex 07-03.3e", vpk3)
v.check("Ex 07-03.3f", tpk3 * 1e6)
ti3, ipk3 = extreme(lambda t: sol3.sol(t)[0], 0, 15e-6)
v.check("Ex 07-03.3g", ipk3)
v.check("Ex 07-03.3h", ti3 * 1e6)
v.check("Ex 07-03.3i", L3 * (A3 @ np.zeros(2) + np.array([V3 / L3, 0]))[0])   # vL = L di/dt at 0+
v.check("Ex 07-03.3j", ln(50) / a3 * 1e6)
v.assert_true("Ex3 KVL vR + vL + vC = V along the simulated waveform",
              np.allclose(R3 * sol3.sol(tt * 0.1)[0] + L3 * (A3 @ sol3.sol(tt * 0.1) + np.array([[V3 / L3], [0]]))[0]
                          + sol3.sol(tt * 0.1)[1], V3, atol=1e-6))

# ================================================================================ Example 4
VS4, Rs4, L4, C4 = 5.0, 0.03, 4.7e-6, 22e-6


def lc_filter(RL):
    """States (iL, v): L diL/dt = VS - Rs iL - v ; C dv/dt = iL - v/RL."""
    return np.array([[-Rs4 / L4, -1 / L4], [1 / C4, -1 / (RL * C4)]])


A4 = lc_filter(10.0)
a4, w04, z4, _ = damping_from_eigs(A4)
v.check("Ex 07-03.4a", a4)
v.check("Ex 07-03.4b", w04 / 1e3)
v.check("Ex 07-03.4c", w04 / (2 * pi) / 1e3)
v.check("Ex 07-03.4d", z4)
Z04 = sqrt(L4 / C4)
v.check("Ex 07-03.4e", Rs4 / (2 * Z04))
v.check("Ex 07-03.4f", Z04 / (2 * 10.0))
v.assert_true("Ex4 damping adds to within 0.2 %", abs((Rs4 / (2 * Z04) + Z04 / 20) / z4 - 1) < 2e-3)
xinf4 = -np.linalg.solve(A4, np.array([VS4 / L4, 0]))
v.check("Ex 07-03.4g", xinf4[1])
sol4 = simulate(A4, [VS4 / L4, 0], [0, 0], 1e-3)
_, vpk4 = extreme(lambda t: sol4.sol(t)[1], 0, 60e-6)
v.check("Ex 07-03.4h", (vpk4 / xinf4[1] - 1) * 100)
v.check("Ex 07-03.4i", vpk4)
A4b = lc_filter(100.0)
v.check("Ex 07-03.4j", damping_from_eigs(A4b)[2])
sol4b = simulate(A4b, [VS4 / L4, 0], [0, 0], 1e-3)
v.check("Ex 07-03.4k", extreme(lambda t: sol4b.sol(t)[1], 0, 60e-6)[1])

# ================================================================================ Example 5
V5, L5, C5, R5 = 48.0, 2e-9, 250e-12, 0.1
Z05 = sqrt(L5 / C5)
v.check("Ex 07-03.5a", Z05)
A5 = series_A(R5, L5, C5)
a5, w05, z5, _ = damping_from_eigs(A5)
v.check("Ex 07-03.5b", w05 / (2 * pi) / 1e6)
v.check("Ex 07-03.5c", z5)
sol5 = simulate(A5, [V5 / L5, 0], [0, 0], 200e-9)
v.check("Ex 07-03.5d", extreme(lambda t: sol5.sol(t)[1], 0, 20e-9)[1])
v.check("Ex 07-03.5e", ln(20) / a5 * 1e9)
v.assert_true("Ex5 unsnubbed ringing really lasts about 120 ns (last exit from ±5 % between 100 and 125 ns)",
              100e-9 < settle_time(lambda t: sol5.sol(t)[1], V5, 0.05 * V5, 200e-9) < 125e-9)


def snubbed(k, Rd=Z05):
    """States (iL, vC, vCd)."""
    Cd = k * C5
    A = np.array([[-R5 / L5, -1 / L5, 0], [1 / C5, -1 / (Rd * C5), 1 / (Rd * C5)], [0, 1 / (Rd * Cd), -1 / (Rd * Cd)]])
    return A, simulate(A, [V5 / L5, 0, 0], [0, 0, 0], 80e-9, n_steps=2000)


for k, idp, ids in ((1, "f", "j"), (2, "g", "k"), (4, "h", "l"), (10, "i", "m")):
    A, sol = snubbed(k)
    vc = lambda t, sol=sol: sol.sol(t)[1]  # noqa: E731
    v.check(f"Ex 07-03.5{idp}", extreme(vc, 0, 40e-9)[1])
    v.check(f"Ex 07-03.5{ids}", settle_time(vc, V5, 0.05 * V5, 80e-9) * 1e9)
    if k == 4:
        pair = [e for e in np.linalg.eigvals(A) if abs(e.imag) > 1]
        v.check("Ex 07-03.5p", -pair[0].real / abs(pair[0]))
        v.check("Ex 07-03.5q", abs(pair[0].imag) / (2 * pi) / 1e6)
        # energy check: during the charging transient the resistors dissipate ½(C + Cd)V², of which
        # the snubber's share of the extra loss per cycle is ½CdV² here plus ½CdV² at discharge.
        t = np.linspace(0, 80e-9, 400001)
        x = sol.sol(t)
        P = R5 * x[0] ** 2 + (x[1] - x[2]) ** 2 / Z05
        v.assert_true("Ex5 charging transient dissipates ½(C + Cd)V² in total",
                      abs(np.trapezoid(P, t) / (0.5 * 5 * C5 * V5**2) - 1) < 2e-3)
v.check("Ex 07-03.5n", C5 * V5**2 * 500e3)
v.check("Ex 07-03.5o", 4 * C5 * V5**2 * 500e3)

# ================================================================================ Example 6
A6 = np.array([[-(1 / 1e3 + 1 / 1e3) / 1e-6, 1 / (1e3 * 1e-6)], [1 / (1e3 * 1e-6), -1 / (1e3 * 1e-6)]])
a6, w06, z6, ev6 = damping_from_eigs(A6)
v.check("Ex 07-03.6a", z6)
e6 = sorted(ev6.real, reverse=True)
v.check("Ex 07-03.6b", e6[0])
v.check("Ex 07-03.6c", e6[1])
v.check("Ex 07-03.6d", (-1 / e6[0] - 1 / e6[1]) * 1e3)
v.assert_true("Ex6 time constants sum to the Elmore delay", abs((-1 / e6[0] - 1 / e6[1]) - 3e-3) < 1e-12)
sol6 = simulate(A6, [1 / (1e3 * 1e-6), 0], [0, 0], 20e-3)
v.check("Ex 07-03.6e", brentq(lambda t: sol6.sol(t)[1] - 0.5, 1e-4, 10e-3, xtol=1e-15) * 1e3)
# buffered: two independent first-order sections (the second driven by the first's voltage)
Ab = np.array([[-1e3, 0], [1e3, -1e3]])
solb = simulate(Ab, [1e3, 0], [0, 0], 20e-3)
v.check("Ex 07-03.6f", brentq(lambda t: solb.sol(t)[1] - 0.5, 1e-4, 10e-3, xtol=1e-15) * 1e3)
v.check("Ex 07-03.6g", ln(2) * 3.0)
v.assert_true("Ex6 ladder never overshoots", sol6.sol(np.linspace(0, 20e-3, 20001))[1].max() <= 1.0 + 1e-9)

# ============================================================================== Numbers to know
for zz, key in ((0.1, "a"), (0.25, "b"), (0.5, "c"), (0.707, "d")):
    sol = simulate(series_A(2 * zz, 1.0, 1.0), [1.0, 0], [0, 0], 60.0)
    pk = extreme(lambda t, sol=sol: sol.sol(t)[1], 0, 10.0)[1]
    v.check(f"N 07-03.{key}", (pk - 1) * 100)
v.check("N 07-03.e", 1 / (2 * pi * sqrt(150e-9 * 10.8e-12)) / 1e6)

# ============================================================================== Practitioner lens
v.check("PL 07-03.a", sqrt(1e-6 / 22e-6))
v.check("PL 07-03.a2", sqrt(10e-6 / 22e-6))
for (R, L, C, idZ, idz, idv, idi) in ((0.1, 0.5e-6, 1e-6, "b", "c", "d", "e"), (0.1, 5e-6, 1e-6, None, None, "f", "g")):
    A = series_A(R, L, C)
    sol = simulate(A, [30 / L, 0], [0, 0], 4 * pi * sqrt(L * C), n_steps=400)
    if idZ:
        v.check(f"PL 07-03.{idZ}", sqrt(L / C))
        v.check(f"PL 07-03.{idz}", damping_from_eigs(A)[2])
    T = 2 * pi * sqrt(L * C)
    v.check(f"PL 07-03.{idv}", extreme(lambda t, sol=sol: sol.sol(t)[1], 0, T)[1])
    v.check(f"PL 07-03.{idi}", extreme(lambda t, sol=sol: sol.sol(t)[0], 0, T)[1])
v.assert_true("onsemi case 12 (0.3 ohm, 0.5 uH, 100 uF) is overdamped: no surge",
              damping_from_eigs(series_A(0.3, 0.5e-6, 1e-4))[2] > 1)
v.check("PL 07-03.h", 1 / (2 * pi * sqrt(2.5e-9 * 170e-12)) / 1e6, tol=0.5)
v.check("PL 07-03.i", sqrt(2e-6 / 330e-12))
v.check("PL 07-03.j", 1000e-12 * 400**2 * 100e3)

# ================================================================================ Problems
# P1
A = series_A(150, 2e-3, 50e-9)
a, w0, z, ev = damping_from_eigs(A)
v.check("07-03.1a", w0 / 1e3)
v.check("07-03.1b", w0 / (2 * pi) / 1e3)
v.check("07-03.1c", sqrt(2e-3 / 50e-9))
v.check("07-03.1d", a / 1e3)
v.check("07-03.1e", z)
v.check("07-03.1f", 1 / (2 * z))
v.check("07-03.1g", abs(ev[0].imag) / 1e3)
v.check("07-03.1h", brentq(lambda R: damping_from_eigs(series_A(R, 2e-3, 50e-9))[2] - 1, 1, 2000))
# P2
v.check("07-03.2a", sqrt(50e-6 / 200e-9))
v.check("07-03.2b", brentq(lambda R: damping_from_eigs(parallel_A(R, 50e-6, 200e-9))[2] - 1, 0.5, 100))
a, w0, z, _ = damping_from_eigs(parallel_A(50, 50e-6, 200e-9))
v.check("07-03.2c", z)
v.check("07-03.2d", 1 / (2 * z))
v.check("07-03.2e", a / 1e3)
v.check("07-03.2f", w0 / 1e3)
# P3: series loop, states (i, vC), source 10 V, vC(0) = 4 V
A = series_A(20, 5e-3, 2e-6)
x0 = np.array([0.0, 4.0])
dx = A @ x0 + np.array([10 / 5e-3, 0])
v.check("07-03.3a", x0[1])
v.check("07-03.3b", 5e-3 * dx[0])
v.check("07-03.3c", dx[0])
v.check("07-03.3d", 20 * dx[0])
v.check("07-03.3e", -np.linalg.solve(A, np.array([10 / 5e-3, 0]))[1])
# P4: discharge; states (i, vC) with the source term zero and vC(0) = 100 V
A = series_A(2, 1e-3, 10e-6)
a, w0, z, ev = damping_from_eigs(A)
wd = abs(ev[0].imag)
v.check("07-03.4a", a)
v.check("07-03.4b", z)
v.check("07-03.4c", wd)
v.check("07-03.4d", sqrt(1e-3 / 10e-6))
sol = simulate(A, [0, 0], [0, 100.0], 2e-3)
cur = lambda t: -sol.sol(t)[0]  # noqa: E731  (current out of the capacitor's + terminal)
tpk, ipk = extreme(cur, 0, 300e-6)
v.check("07-03.4e", tpk * 1e6)
v.check("07-03.4f", ipk)
tz = brentq(cur, 200e-6, 400e-6, xtol=1e-16)
v.check("07-03.4g", tz * 1e6)
v.check("07-03.4h", sol.sol(tz)[1])
v.check("07-03.4i", (sol.sol(tz)[1] / 100) ** 2 * 100)
# P5
Rc = brentq(lambda R: damping_from_eigs(series_A(R, 10e-6, 1e-6))[2] - 1, 0.1, 100)
v.check("07-03.5a", Rc)
solc = simulate(series_A(Rc, 10e-6, 1e-6), [1 / 10e-6, 0], [0, 0], 200e-6)
t90c = brentq(lambda t: solc.sol(t)[1] - 0.9, 1e-7, 100e-6, xtol=1e-16)
v.check("07-03.5b", t90c * 1e6)
sol2z = simulate(series_A(2 * Rc, 10e-6, 1e-6), [1 / 10e-6, 0], [0, 0], 400e-6)
t90z = brentq(lambda t: sol2z.sol(t)[1] - 0.9, 1e-7, 200e-6, xtol=1e-16)
v.check("07-03.5c", t90z * 1e6)
v.check("07-03.5d", t90z / t90c)
# P6: current step into parallel RLC; states (v, iL)
A = parallel_A(2e3, 10e-3, 10e-9)
a, w0, z, _ = damping_from_eigs(A)
v.check("07-03.6a", w0 / 1e3)
v.check("07-03.6b", sqrt(10e-3 / 10e-9))
v.check("07-03.6c", z)
v.check("07-03.6d", a / 1e3)
sol = simulate(A, [2e-3 / 10e-9, 0], [0, 0], 400e-6)
t_il, il_pk = extreme(lambda t: sol.sol(t)[1], 0, 60e-6)
v.check("07-03.6e", il_pk * 1e3)
v.check("07-03.6f", t_il * 1e6)
t_v, v_pk = extreme(lambda t: sol.sol(t)[0], 0, 30e-6)
v.check("07-03.6g", t_v * 1e6)
v.check("07-03.6h", v_pk)
# P7: before: DC with L short, C open; after: series RLC (R1 = 2, L = 0.5 mH, C = 50 uF), 12 V
Gm = np.array([[1 / 2 + 1 / 4]])
va7 = np.linalg.solve(Gm, np.array([12 / 2]))[0]   # node a with the inductor shorted
iL7 = (12 - va7) / 2
v.check("07-03.7a", iL7)
v.check("07-03.7b", va7)
A = series_A(2, 0.5e-3, 50e-6)
a, w0, z, ev = damping_from_eigs(A)
v.check("07-03.7c", a)
v.check("07-03.7d", w0)
v.check("07-03.7e", z)
v.check("07-03.7f", abs(ev[0].imag))
x0 = np.array([iL7, va7])
v.check("07-03.7g", (A @ x0 + np.array([12 / 0.5e-3, 0]))[1])
v.check("07-03.7h", -np.linalg.solve(A, np.array([12 / 0.5e-3, 0]))[1])
sol = simulate(A, [12 / 0.5e-3, 0], x0, 3e-3)
v.check("07-03.7i", sol.sol(0.5e-3)[1])
t7, v7 = extreme(lambda t: sol.sol(t)[1], 0, 1e-3)
v.check("07-03.7j", t7 * 1e6)
v.check("07-03.7k", v7)
# P8: states (v, iL)
A = np.array([[-1 / (100 * 1e-6), -1 / 1e-6], [1 / 10e-3, -10 / 10e-3]])
g = np.array([11 / (100 * 1e-6), 0])
a, w0, z, ev = damping_from_eigs(A)
v.check("07-03.8a", a)
v.check("07-03.8b", w0 / 1e3)
v.check("07-03.8c", z)
v.check("07-03.8d", abs(ev[0].imag))
xinf = -np.linalg.solve(A, g)
v.check("07-03.8e", xinf[0])
v.check("07-03.8f", xinf[1])
v.check("07-03.8g", g[0] / 1e5)
sol = simulate(A, g, [0, 0], 3e-3)
t8, v8 = extreme(lambda t: sol.sol(t)[0], 0, 1e-3)
v.check("07-03.8h", t8 * 1e6)
v.check("07-03.8i", v8)
v.check("07-03.8j", xinf[0] * (1 + os_formula(z)))
# P9
A = np.array([[-(1 / 1e3 + 1 / 2e3) / 2e-6, 1 / (2e3 * 2e-6)], [1 / (2e3 * 0.5e-6), -1 / (2e3 * 0.5e-6)]])
a, w0, z, ev = damping_from_eigs(A)
v.check("07-03.9a", z)
e9 = sorted(ev.real, reverse=True)
v.check("07-03.9b", e9[0])
v.check("07-03.9c", e9[1])
v.check("07-03.9d", (-1 / e9[0] - 1 / e9[1]) * 1e3)
rng = np.random.default_rng(1)
ok = True
for _ in range(2000):
    r1, r2 = 10 ** rng.uniform(0, 6, 2)
    c1, c2 = 10 ** rng.uniform(-12, -3, 2)
    Ar = np.array([[-(1 / r1 + 1 / r2) / c1, 1 / (r2 * c1)], [1 / (r2 * c2), -1 / (r2 * c2)]])
    ok &= bool(np.all(np.abs(np.linalg.eigvals(Ar).imag) == 0) and np.all(np.linalg.eigvals(Ar).real < 0))
v.assert_true("P9 random RC ladders always have real negative roots", ok)
# P10
Cp = 470e-12 / ((120 / 60) ** 2 - 1)
Lp = 1 / ((2 * pi * 120e6) ** 2 * Cp)
v.check("07-03.10a", Cp * 1e12)
v.check("07-03.10b", Lp * 1e9)
v.check("07-03.10c", sqrt(Lp / Cp))
v.assert_true("P10 added 470 pF really halves the ring", abs(1 / (2 * pi * sqrt(Lp * (Cp + 470e-12))) - 60e6) < 1)
v.check("07-03.10d", 680e-12 * 400**2 * 100e3)
# P11: 12 V, 1 uH, 50 mohm, 10 uF ceramic, 47 uF bulk with ESR Rb


def hotplug(Rb):
    A = np.array([[-0.05 / 1e-6, -1 / 1e-6, 0], [1 / 10e-6, -1 / (Rb * 10e-6), 1 / (Rb * 10e-6)],
                  [0, 1 / (Rb * 47e-6), -1 / (Rb * 47e-6)]])
    return simulate(A, [12 / 1e-6, 0, 0], [0, 0, 0], 400e-6, n_steps=4000)


v.check("07-03.11a", sqrt(1e-6 / 10e-6))
peak11 = {}
for Rb, key in ((0.1, "b"), (0.3, "c"), (1.0, "d"), (0.2, None), (0.25, None)):
    sol = hotplug(Rb)
    peak11[Rb] = extreme(lambda t, sol=sol: sol.sol(t)[1], 0, 60e-6)[1]
    if key:
        v.check(f"07-03.11{key}", peak11[Rb])
    if Rb == 0.3:
        v.check("07-03.11e", settle_time(lambda t, sol=sol: sol.sol(t)[1], 12.0, 0.24, 400e-6) * 1e6)
        v.check("07-03.11i", extreme(lambda t, sol=sol: sol.sol(t)[0], 0, 30e-6)[1])
v.assert_true("P11 the best ESR lies between 0.2 and 0.3 ohm (0.25 beats both ends)",
              peak11[0.25] < peak11[0.2] and peak11[0.25] < peak11[0.3])
sol = simulate(series_A(0.35, 1e-6, 10e-6), [12 / 1e-6, 0], [0, 0], 200e-6)
v.check("07-03.11f", extreme(lambda t: sol.sol(t)[1], 0, 20e-6)[1])
v.check("07-03.11g", 0.3 * 2)
v.check("07-03.11h", 0.3 * 2**2)
# P12
v.check("07-03.12a", sqrt(8e-9 / 2e-9))
A = series_A(1.0, 8e-9, 2e-9)
v.check("07-03.12b", damping_from_eigs(A)[2])
sol = simulate(A, [12 / 8e-9, 0], [0, 0], 1e-6)
v.check("07-03.12c", extreme(lambda t: sol.sol(t)[1], 0, 40e-9)[1])
Rc12 = brentq(lambda R: damping_from_eigs(series_A(R, 8e-9, 2e-9))[2] - 1, 0.1, 50)
v.check("07-03.12d", Rc12)
sol = simulate(series_A(Rc12, 8e-9, 2e-9), [12 / 8e-9, 0], [0, 0], 1e-6)
t10 = brentq(lambda t: sol.sol(t)[1] - 1.2, 1e-12, 50e-9, xtol=1e-20)
t90 = brentq(lambda t: sol.sol(t)[1] - 10.8, 1e-12, 100e-9, xtol=1e-20)
v.check("07-03.12e", (t90 - t10) * 1e9)
# P13: lossless series LC, diode stops the current at its first zero
for v0, kv, ki in ((0.0, "b", "c"), (-200.0, "d", "e")):
    A = series_A(0.0, 10e-3, 1e-6)
    sol = simulate(A, [400 / 10e-3, 0], [0, v0], 1e-3)
    tz = brentq(lambda t: sol.sol(t)[0], 100e-6, 500e-6, xtol=1e-16)
    if v0 == 0.0:
        v.check("07-03.13a", tz * 1e6)
    v.check(f"07-03.13{kv}", sol.sol(tz)[1])
    v.check(f"07-03.13{ki}", extreme(lambda t, sol=sol: sol.sol(t)[0], 0, tz)[1])
# P14
A = series_A(10, 1e-3, 1e-6)
a, w0, z, ev = damping_from_eigs(A)
v.check("07-03.14a", sqrt(1e-3 / 1e-6))
v.check("07-03.14b", z)
v.check("07-03.14c", a)
v.check("07-03.14d", abs(ev[0].imag) / 1e3)
sol = simulate(A, [5 / 1e-3, 0], [0, 0], 2e-3)
vL = lambda t: 5 - 10 * sol.sol(t)[0] - sol.sol(t)[1]  # noqa: E731
dx0 = A @ np.zeros(2) + np.array([5 / 1e-3, 0])        # state derivatives at 0+
v.check("07-03.14e", -10 * dx0[0] - dx0[1])              # vL = 5 - R i - vC
h = 1e-10
v.assert_true("P14 vL slope agrees with a one-sided second-order difference",
              abs((-3 * vL(0) + 4 * vL(h) - vL(2 * h)) / (2 * h) - (-50000)) < 5)
v.check("07-03.14f", extreme(lambda t: sol.sol(t)[0], 0, 100e-6)[1] * 1e3)
t14, v14 = extreme(vL, 0, 150e-6, "min")
v.check("07-03.14g", t14 * 1e6)
v.check("07-03.14h", v14)
v.check("07-03.14i", extreme(lambda t: sol.sol(t)[0], 0, 100e-6)[0] * 1e6)
v.check("07-03.14j", 1e6 * brentq(lambda t: sol.sol(t)[1] - 5.0, 1e-6, 80e-6))
# P15: parallel tank with net conductance 1/R - g
Gnet = 1 / 10e3 - 0.2e-3
A = np.array([[-Gnet / 1e-9, -1 / 1e-9], [1 / 1e-6, 0]])
a, w0, z, ev = damping_from_eigs(A)
v.check("07-03.15a", w0 / (2 * pi) / 1e6)
v.check("07-03.15b", a / 1e3)
v.check("07-03.15c", 1 / abs(a) * 1e6)
v.check("07-03.15d", ln(1000) / abs(a) * 1e6)
v.check("07-03.15e", ln(1000) / abs(a) * abs(ev[0].imag) / (2 * pi), tol=0.5)
v.check("07-03.15f", brentq(lambda g: damping_from_eigs(np.array([[-(1 / 10e3 - g) / 1e-9, -1e9], [1e6, 0]]))[0],
                             0, 1e-3) * 1e3)
# P16: probe
for Lg, kf, kz0, kz, ko in ((150e-9, "a", "b", "c", "d"), (15e-9, "e", "f", "g", "h")):
    A = series_A(50.0, Lg, 10.8e-12)
    a, w0, z, _ = damping_from_eigs(A)
    v.check(f"07-03.16{kf}", w0 / (2 * pi) / 1e6)
    v.check(f"07-03.16{kz0}", sqrt(Lg / 10.8e-12))
    v.check(f"07-03.16{kz}", z)
    sol = simulate(A, [1 / Lg, 0], [0, 0], 30e-9, n_steps=600)
    v.check(f"07-03.16{ko}", (extreme(lambda t, sol=sol: sol.sol(t)[1], 0, 20e-9)[1] - 1) * 100)

# ================================================================================ Lab handout
A = series_A(0.1, 2e-6, 10e-6)
v.check("Lab 07-03.a", sqrt(2e-6 / 10e-6))
v.check("Lab 07-03.b", damping_from_eigs(A)[2])
sol = simulate(A, [12 / 2e-6, 0], [0, 0], 400e-6)
v.check("Lab 07-03.c", extreme(lambda t: sol.sol(t)[1], 0, 40e-6)[1])
v.check("Lab 07-03.d", extreme(lambda t: sol.sol(t)[0], 0, 20e-6)[1])

# P17: three-op-amp two-integrator loop, simulated from the op-amp KCL equations
R17, C17 = 10e3, 10e-9


def a17(RQ):
    # states (v1, v2): C dv1/dt = -(vin + v3)/R - v1/RQ with v3 = -v2;  C dv2/dt = -v1/R
    return np.array([[-1 / (RQ * C17), 1 / (R17 * C17)], [-1 / (R17 * C17), 0.0]])


ev17 = np.linalg.eigvals(a17(50e3))
v.check("07-03.17a", abs(ev17[0]))
v.check("07-03.17b", -ev17[0].real / abs(ev17[0]))
v.check("07-03.17c", abs(ev17[0]) / (-2 * ev17[0].real))


def step17(RQ):
    A = a17(RQ)
    return solve_ivp(lambda t, x: A @ x + np.array([-1.0 / (R17 * C17), 0.0]), (0, 0.02), [0.0, 0.0],
                     rtol=1e-11, atol=1e-14, dense_output=True)


s17 = step17(50e3)
v.check("07-03.17d", s17.y[1, -1])
t17, p17 = extreme(lambda t: s17.sol(t)[1], 0, 1e-3)
v.check("07-03.17e", 100 * (p17 - 1))
v.check("07-03.17f", p17)
v.check("07-03.17g", 1e6 * t17)
RQb = brentq(lambda RQ: -np.linalg.eigvals(a17(RQ))[0].real / abs(np.linalg.eigvals(a17(RQ))[0]) - 1 / math.sqrt(2),
             1e3, 50e3)
v.check("07-03.17h", RQb / 1e3)
sb17 = step17(RQb)
v.check("07-03.17i", 100 * (extreme(lambda t: sb17.sol(t)[1], 0, 2e-3)[1] - 1))

v.finish()
