#!/usr/bin/env python3
"""Verify every published number in chapter 07-02 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Values are recomputed from circuit laws. Key results are additionally cross-checked by integrating
the governing ODEs numerically (scipy solve_ivp), independently of the closed-form solutions.
The ngspice netlists in labs/07-02-lab are run separately by tools/run_spice.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-02",
    COURSE / "chapters" / "07-02-first-order-rc-rl-transients.md",
    COURSE / "solutions" / "07-02-solutions.md",
    COURSE / "labs" / "07-02-lab" / "README.md",
)
exp, ln = math.exp, math.log
k_B, T = 1.380649e-23, 300.0


def ode(f, t_end, y0, **kw):
    """Integrate y' = f(t, y) tightly and return a dense solution."""
    return solve_ivp(f, (0, t_end), np.atleast_1d(y0), rtol=1e-10, atol=1e-13, dense_output=True,
                     max_step=t_end / 2000, **kw)


def par(*rs):
    return 1 / sum(1 / r for r in rs)


# =============================================================================== Example 1
R, C, V0 = 4.7e3, 10e-6, 12.0
tau = R * C
v.check("Ex 07-02.1a", tau * 1e3)
v.check("Ex 07-02.1b", V0 * exp(-0.1 / tau))
v.check("Ex 07-02.1c", tau * ln(V0 / 1.0) * 1e3)
v.check("Ex 07-02.1d", 0.5 * C * V0**2 * 1e3)
v.check("Ex 07-02.1e", 0.5 * C * (V0**2 - 1) * 1e3)
s = ode(lambda t, y: -y / tau, 0.2, V0)
v.assert_true("Ex1 numerical discharge at 100 ms", abs(s.sol(0.1)[0] - V0 * exp(-0.1 / tau)) < 1e-6)

# =============================================================================== Examples 2-3 (nodal ODE, no Thevenin)
VS, R1, R2, C = 24.0, 6e3, 3e3, 2e-6
VTh, RTh = VS * R2 / (R1 + R2), par(R1, R2)
tau1 = RTh * C
v.check("Ex 07-02.2a", VTh)
v.check("Ex 07-02.2b", RTh / 1e3)
v.check("Ex 07-02.2c", tau1 * 1e3)
v.check("Ex 07-02.2d", (VS - 0) / R1 * 1e3)
v.check("Ex 07-02.2e", VTh * (1 - exp(-1)))
v.check("Ex 07-02.2f", tau1 * ln(VTh / (VTh - 7)) * 1e3)
v.check("Ex 07-02.2g", VS / (R1 + R2) * 1e3)
# independent: KCL at node A with the switch closed for 0 <= t < 10 ms, open afterwards
def kcl(t, y):
    vc = y[0]
    i_in = (VS - vc) / R1 if t < 10e-3 else 0.0
    return [(i_in - vc / R2) / C]
s = solve_ivp(kcl, (0, 25e-3), [0.0], rtol=1e-11, atol=1e-13, dense_output=True, max_step=2e-6)
v.assert_true("Ex2 nodal ODE agrees at t = tau", abs(s.sol(4e-3)[0] - VTh * (1 - exp(-1))) < 1e-6)
v10 = VTh * (1 - exp(-10e-3 / tau1))
tau2 = R2 * C
v.check("Ex 07-02.3a", v10)
v.check("Ex 07-02.3b", tau2 * 1e3)
v.check("Ex 07-02.3c", v10 * exp(-10e-3 / tau2))
v.check("Ex 07-02.3d", ((VS - v10) / R1 - v10 / R2) * 1e3)
v.check("Ex 07-02.3e", (0 - v10 / R2) * 1e3)
v.assert_true("Ex3 nodal ODE agrees at 20 ms", abs(s.sol(20e-3)[0] - v10 * exp(-10e-3 / tau2)) < 1e-5)
v.assert_true("Ex3 i_C(10ms-) equals C dv/dt from the exponential",
              abs(((VS - v10) / R1 - v10 / R2) - C * VTh / tau1 * exp(-10e-3 / tau1)) < 1e-12)

# =============================================================================== Example 4
L, R1b, R2b, VSb = 0.2, 4.0, 20.0, 12.0
I0 = VSb / R1b
v.check("Ex 07-02.4a", I0)
v.check("Ex 07-02.4b", L / R2b * 1e3)
v.check("Ex 07-02.4c", -I0 * R2b)
v.check("Ex 07-02.4d", VSb - (-I0 * R2b))
v.check("Ex 07-02.4e", 0.5 * L * I0**2)
v.check("Ex 07-02.4f", I0 * exp(-10e-3 / (L / R2b)))
v.check("Ex 07-02.4g", L / 200 * 1e3)
v.check("Ex 07-02.4h", -I0 * 200)
v.check("Ex 07-02.4i", I0**2 * R2b)
E_diss, _ = quad(lambda t: (I0 * exp(-t / (L / R2b)))**2 * R2b, 0, 1.0)
v.assert_true("Ex4 integral of i^2 R equals 1/2 L I0^2", abs(E_diss - 0.5 * L * I0**2) < 1e-9)

# =============================================================================== Example 5
Rs, Cs, Nbits = 100.0, 20e-12, 16
tau5 = Rs * Cs
Nt = (Nbits + 1) * ln(2)
v.check("Ex 07-02.5a", tau5 * 1e9)
v.check("Ex 07-02.5b", Nt)
v.check("Ex 07-02.5c", Nt * tau5 * 1e9)
v.check("Ex 07-02.5d", 300e-9 / Nt / Cs / 1e3)
vn = math.sqrt(k_B * T / Cs)
lsb = 5 / 2**16
v.check("Ex 07-02.5e", vn * 1e6)
v.check("Ex 07-02.5f", lsb * 1e6)
v.check("Ex 07-02.5g", vn / lsb)
v.assert_true("Ex5 settling: error after Nt taus equals exactly half an LSB of full scale",
              math.isclose(exp(-Nt), 0.5 / 2**16, rel_tol=1e-12))

# =============================================================================== numbers to know / practitioner
v.check("N 07-02.a", ln(1000))
v.check("N 07-02.b", 9 * ln(2))
v.check("N 07-02.c", 13 * ln(2))
v.check("N 07-02.d", 21 * ln(2))
v.check("N 07-02.e", math.sqrt(k_B * T / 1e-12) * 1e6)
v.check("N 07-02.f", ln(9) / (2 * math.pi))
v.check("PL 07-02.a", 656 * 10 / 1e3)
v.check("PL 07-02.b", 0.2 * 10)
v.check("PL 07-02.c", (656 * 10) * (0.2e-15 * 10) * 1e12)
v.check("PL 07-02.d", (656 * 20) * (0.2e-15 * 20) * 1e12)
v.check("PL 07-02.e", 1 / (2 * math.pi * 300e-9 / Nt) / 1e6)
v.check("PL 07-02.f", 0.38 * (656 * 10) * (0.2e-15 * 10) * 1e12)
# distributed RC line: 50 % delay ≈ 0.38 RC, checked by simulating a 200-segment RC ladder
nseg = 200
Rseg, Cseg = 1.0 / nseg, 1.0 / nseg  # total R = C = 1 (normalized)
def ladder(t, y):
    vin = 1.0
    dv = np.empty_like(y)
    for i in range(nseg):
        left = vin if i == 0 else y[i - 1]
        right = y[i + 1] if i < nseg - 1 else None
        i_in = (left - y[i]) / Rseg
        i_out = (y[i] - right) / Rseg if right is not None else 0.0
        dv[i] = (i_in - i_out) / Cseg
    return dv
sl = solve_ivp(ladder, (0, 3), np.zeros(nseg), method="LSODA", rtol=1e-8, atol=1e-10, dense_output=True)
tg = np.linspace(0, 3, 30001)
t50 = tg[np.argmax(sl.sol(tg)[-1] >= 0.5)]
v.assert_true("distributed RC line 50 % delay ≈ 0.38 RC", abs(t50 - 0.38) < 0.01, f"t50 = {t50:.4f} RC")
# the landmark table in §3.7: rise time derivation and fraction table
t = np.linspace(0, 10, 1_000_001)
y = 1 - np.exp(-t)
t10, t90 = t[np.argmax(y >= 0.1)], t[np.argmax(y >= 0.9)]
v.assert_true("10-90 % rise time = ln 9 tau (numerical)", abs((t90 - t10) - ln(9)) < 1e-4)
v.assert_true("landmark table 63.2/86.5/95.0/98.2/99.3 %",
              [round(100 * (1 - exp(-n)), 1) for n in range(1, 6)] == [63.2, 86.5, 95.0, 98.2, 99.3])

# =============================================================================== problems
v.check("07-02.1a", 2.2e3 * 47e-6 * 1e3)
v.check("07-02.1b", 5e-3 / 50 * 1e6)
v.check("07-02.1c", 10e3 * 10e-12 * 1e9)
v.check("07-02.2a", 100 * exp(-3))
v.check("07-02.2b", ln(1000))
v.check("07-02.2c", ln(2))

Rth3 = par(1e3, 4e3)
v.check("07-02.3a", 10 / 1e3 * 1e3)
v.check("07-02.3b", 10 * 4 / 5)
v.check("07-02.3c", Rth3)
v.check("07-02.3d", Rth3 * 1e-6 * 1e3)
v.check("07-02.4a", 9 / 3)
v.check("07-02.4b", 0.5 * 2e-3 * 3**2 * 1e3)

RC5 = 0.05 / ln(3.3 / 3.0)
v.check("07-02.5a", RC5)
v.check("07-02.5b", RC5 / 10e-6 / 1e3)

tau6 = 10e3 * 1e-6
v5 = 5 * (1 - exp(-5e-3 / tau6))
v.check("07-02.6a", v5)
v.check("07-02.6b", v5 * exp(-10e-3 / tau6))
v.check("07-02.6c", 5 / 10e3 * 1e3)
v.check("07-02.6d", (0 - v5) / 10e3 * 1e3)
v.check("07-02.6e", v5 * exp(-20e-3 / tau6))
s = ode(lambda t, y: ((5.0 if t < 5e-3 else 0.0) - y) / tau6, 30e-3, 0.0)
v.assert_true("P6 pulse response by ODE", abs(s.sol(15e-3)[0] - v5 * exp(-1)) < 1e-6)

Rth7 = 10 + 15
v.check("07-02.7a", Rth7)
v.check("07-02.7b", 0.05 / Rth7 * 1e3)
iinf7 = 2 * 10 / (10 + 15)
v.check("07-02.7c", iinf7)
v.check("07-02.7d", 2 * 10)
v.check("07-02.7e", iinf7 * (1 - exp(-3e-3 / (0.05 / Rth7))))
# independent: current source 2 A into R1 || (R2 + L): node voltage vn = (2 - iL) R1, L diL/dt = vn - R2 iL
s = ode(lambda t, y: [((2 - y[0]) * 10 - 15 * y[0]) / 0.05], 10e-3, 0.0)
v.assert_true("P7 RL by ODE at 3 ms", abs(s.sol(3e-3)[0] - iinf7 * (1 - exp(-1.5))) < 1e-7)

v.check("07-02.8a", 12)
v.check("07-02.8b", 12 * 2 / 4)
v.check("07-02.8c", par(2e3, 2e3) * 5e-6 * 1e3)
v.check("07-02.8d", 12 / 2e3 * 1e3)
v.check("07-02.8e", ((12 - 12) / 2e3 - 12 / 2e3) * 1e3)
v.check("07-02.8f", 6 / 2e3 * 1e3)

v.check("07-02.9a", 0.35 / 3.5e-9 / 1e6)
v.check("07-02.9b", ln(9) / (2 * math.pi * 3.5e-9) / 1e6)
tau9 = 1e3 * 10e-9
v.check("07-02.9c", 1 / (2 * math.pi * tau9) / 1e3)
v.check("07-02.9d", tau9 * ln(9) * 1e6)
v.check("07-02.9e", tau9 * ln(2) * 1e6)

k10, tau10 = 2.0, 1.0  # V/ms, ms
v.check("07-02.10a", k10 * (5 - tau10) + k10 * tau10 * exp(-5 / tau10))
v.check("07-02.10b", tau10)
v.check("07-02.10c", k10 * tau10)
s = ode(lambda t, y: (k10 * t - y) / tau10, 10.0, 0.0)
v.assert_true("P10 ramp response by ODE", abs(s.sol(5.0)[0] - (k10 * 4 + k10 * exp(-5))) < 1e-8)

RC11 = 10e3 * 100e-9
v.check("07-02.11a", 1 / RC11 * 5e-3)
v.check("07-02.11b", 12 * RC11 * 1e3)
tau11 = 100e3 * 100e-9
v.check("07-02.11c", 10 * (1 - exp(-10e-3 / tau11)))
v.check("07-02.11d", (100e3 / 10e3) * 1.0)
v.check("07-02.11e", tau11 * 1e3)
# KCL at virtual ground: vin/R + vout/Rf + C dvout/dt = 0 with vin = -1
s = ode(lambda t, y: (-(-1.0) / 10e3 - y / 100e3) / 100e-9, 20e-3, 0.0)
v.assert_true("P11 leaky integrator by ODE", abs(s.sol(10e-3)[0] - 10 * (1 - exp(-1))) < 1e-6)

def square_ss(tau, T=1e-3, V=1.0):
    k = exp(-T / (2 * tau))
    return V / (1 + k), V * k / (1 + k)
vmax1, vmin1 = square_ss(0.5e-3)
vmax2, vmin2 = square_ss(5e-3)
v.check("07-02.12a", vmax1)
v.check("07-02.12b", vmin1)
v.check("07-02.12c", vmax1 - vmin1)
v.check("07-02.12d", vmax2)
v.check("07-02.12e", vmin2)
v.check("07-02.12f", vmax2 - vmin2)
v.check("07-02.12g", 1.0 * 1e-3 / (4 * 5e-3))
sq = lambda t: 1.0 if (t % 1e-3) < 0.5e-3 else 0.0  # noqa: E731
s = solve_ivp(lambda t, y: (sq(t) - y) / 0.5e-3, (0, 30e-3), [0.0], rtol=1e-10, atol=1e-13, max_step=1e-6,
              dense_output=True)
tt = np.linspace(29e-3, 30e-3, 20001)
yy = s.sol(tt)[0]
v.assert_true("P12 square-wave steady state by brute-force ODE",
              abs(yy.max() - vmax1) < 1e-4 and abs(yy.min() - vmin1) < 1e-4)

C13, V13, a13, f13 = 2e-15, 0.75, 0.15, 3e9
P13 = a13 * C13 * V13**2 * f13
v.check("07-02.13a", C13 * V13**2 * 1e15)
v.check("07-02.13b", P13 * 1e6)
v.check("07-02.13c", 50 / P13 / 1e6)
v.check("07-02.13d", 100 * (1 - (0.65 / 0.75) ** 2))
# P13(a)/(b): the R-independence of the loss and the stepwise result, by numerical integration
for Rt in (10.0, 1e3, 1e5):
    Eloss, _ = quad(lambda t: (1.0 / Rt) ** 2 * exp(-2 * t / (Rt * 1e-6)) * Rt, 0, 50 * Rt * 1e-6)
    v.assert_true(f"P13a charging loss is CV^2/2 for R = {Rt:g}", abs(Eloss - 0.5e-6) < 1e-12)
N = 8
step_loss = sum(0.5 * 1e-6 * (1.0 / N) ** 2 for _ in range(N))
v.assert_true("P13b N-step loss = CV^2/(2N)", math.isclose(step_loss, 1e-6 / (2 * N)))

L14, Rc, I0_14 = 0.1, 200.0, 12 / 200
Rf = (30 - 12) / I0_14
v.check("07-02.14a", I0_14 * 1e3)
v.check("07-02.14b", Rf)
v.check("07-02.14c", L14 / (Rc + Rf) * 1e3)
v.check("07-02.14d", L14 / (Rc + Rf) * ln(10) * 1e3)
tauD = L14 / Rc
v.check("07-02.14e", tauD * 1e3)
VD = 0.7
v.check("07-02.14f", tauD * ln((I0_14 + VD / Rc) / (0.1 * I0_14 + VD / Rc)) * 1e3)
v.check("07-02.14g", 12 + VD)
v.check("07-02.14h", 0.5 * L14 * I0_14**2 * 1e3)
v.check("07-02.14i", 12**2 / Rf)
v.check("07-02.14j", (I0_14 + 12 / Rf) * 1e3)
v.check("07-02.14k", (30 - 12 - 0.7) / I0_14)
# diode case by ODE with an exponential diode (Is = 1e-14 A, n = 1): shows the constant-drop model is close
VT = k_B * T / 1.602176634e-19
Is = 1e-14
s = solve_ivp(lambda t, y: [-(Rc * y[0] + 1.0 * VT * math.log1p(max(y[0], 0) / Is)) / L14], (0, 3e-3), [I0_14],
              rtol=1e-10, atol=1e-14, dense_output=True, max_step=1e-6,
              events=lambda t, y: y[0] - 0.1 * I0_14)
t_exp = s.t_events[0][0]
v.assert_true("P14f exponential-diode model within 10 % of constant-drop answer",
              abs(t_exp - tauD * ln((I0_14 + VD / Rc) / (0.1 * I0_14 + VD / Rc))) / t_exp < 0.10,
              f"t_exp = {t_exp * 1e3:.4f} ms")

N15 = 13 * ln(2)
t15 = 100e-9 / N15
vn15 = math.sqrt(k_B * T / 10e-12)
v.check("07-02.15a", N15)
v.check("07-02.15b", t15 * 1e9)
v.check("07-02.15c", t15 / 10e-12 / 1e3)
v.check("07-02.15d", vn15 * 1e6)
v.check("07-02.15e", vn15 / (3.3 / 4096))
v.check("07-02.15f", vn15 / (3.3 / 65536))
qn = 1 / math.sqrt(12)
tot = math.hypot(qn, vn15 / (3.3 / 65536))
v.check("07-02.15i", tot)
v.check("07-02.15j", math.log2(tot / qn))
Cmin = k_B * T / (0.1 * 3.3 / 65536) ** 2
v.check("07-02.15g", Cmin * 1e12)
v.check("07-02.15h", (100e-9 / (17 * ln(2))) / Cmin)

C16, V16, R16 = 1e-6, 10.0, 1e3
v.check("07-02.16a", C16 * V16 / (2 * C16))
v.check("07-02.16b", R16 * (C16 / 2) * 1e3)
v.check("07-02.16c", 0.5 * C16 * V16**2 * 1e6)
v.check("07-02.16d", 2 * 0.5 * C16 * (V16 / 2) ** 2 * 1e6)
v.check("07-02.16e", (0.5 * C16 * V16**2 - 2 * 0.5 * C16 * (V16 / 2) ** 2) * 1e6)
# two-capacitor ODE: i = (v1 - v2)/R, C dv1/dt = -i, C dv2/dt = i ; dissipation = ∫ i^2 R
s = ode(lambda t, y: [-(y[0] - y[1]) / R16 / C16, (y[0] - y[1]) / R16 / C16, (y[0] - y[1]) ** 2 / R16],
        10e-3, [V16, 0.0, 0.0])
v.assert_true("P16 two-capacitor ODE: final voltages and dissipated energy",
              abs(s.sol(10e-3)[0] - 5) < 1e-6 and abs(s.sol(10e-3)[2] - 25e-6) < 1e-10)

# Problem 17: dependent source (test-source method), stable and unstable cases
R1_17, C17 = 2e3, 10e-6
for g, ids in [(0.25e-3, ("07-02.17a", "07-02.17b", "07-02.17c")), (1e-3, ("07-02.17d", "07-02.17e", None))]:
    Rth = 1 / (1 / R1_17 - g)
    v.check(ids[0], Rth / 1e3)
    v.check(ids[1], Rth * C17 * 1e3)
    sk = ode(lambda t, y: [(-y[0] / R1_17 + g * y[0]) / C17], 0.1, 1.0)  # KCL at node A
    if ids[2]:
        v.check(ids[2], sk.sol(0.04)[0], tol=5e-5)
    else:
        v.check("07-02.17f", sk.sol(0.02)[0], tol=5e-4)
        v.check("07-02.17g", sk.sol(0.1)[0], tol=0.05)
v.check("07-02.17h", 1 / R1_17 * 1e3)
vt = 1.0  # test-source check of R_Th formula
v.assert_true("P17 test-source current gives R_Th", math.isclose(vt / (vt / R1_17 - 0.25e-3 * vt), 4000.0))

# Problem 18: two-position switch
tau18 = 4e3 * 1e-6
v.check("07-02.18a", 5)
v.check("07-02.18b", tau18 * 1e3)
v.check("07-02.18c", -10)
v.check("07-02.18d", (-10 - 5) / 4e3 * 1e3)
v.check("07-02.18e", tau18 * ln(15 / 10) * 1e3)
s18 = ode(lambda t, y: [(-10 - y[0]) / tau18], 0.02, 5.0)
v.check("07-02.18f", s18.sol(8e-3)[0], tol=5e-4)
v.check("07-02.18g", (5 - (-10)) / (1e3 + 4e3) * 1e3)
ustep = lambda t: np.where(t > 0, 1.0, 0.0)  # noqa: E731
tt18 = np.linspace(-5e-3, 20e-3, 2501)
unified = 5 + (15 * np.exp(-np.clip(tt18, 0, None) / tau18) - 15) * ustep(tt18)
piecewise = np.where(tt18 > 0, -10 + 15 * np.exp(-np.clip(tt18, 0, None) / tau18), 5.0)
v.assert_true("P18 unit-step expression equals the piecewise answer", np.allclose(unified, piecewise))

# =============================================================================== lab expected results
tau_l = par(6e3, 6e3) * 2e-6
VTh_l = 24 * 6 / 12
v.check("Lab 07-02.1", VTh_l)
v.check("Lab 07-02.2", par(6e3, 6e3) / 1e3)
v.check("Lab 07-02.3", tau_l * 1e3)
v.check("Lab 07-02.4", tau_l * ln(VTh_l / (VTh_l - 7)) * 1e3)
v.check("Lab 07-02.5", 0.5 * 1e-6 * 5**2 * 1e6)
v.check("Lab 07-02.6", 0.5 * 1e-6 * 5**2 / 10 * 1e6)
v.check("Lab 07-02.7", VTh_l * (1 - exp(-10e-3 / tau_l)))
v.check("Lab 07-02.8", 12 + 0.06 * 1000)
v.check("Lab 07-02.9", 0.1 / (200 + 1000) * 1e6)

v.finish()
