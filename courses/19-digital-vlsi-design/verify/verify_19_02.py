#!/usr/bin/env python3
"""Verify every number in chapter 19-02 (the CMOS inverter, dynamic behavior and delay), its problems and its lab.

Independent routes:
- step delays by integrating C dV/dt = -I(V) with a current function written here (not the lab's), against the
  closed form, and the closed form re-derived symbolically with sympy;
- R_eq by quadrature of V/I, against Problem 10's closed form;
- the ring oscillator as coupled ODEs written here, with the period from zero crossings of a dense solution;
- the delay-optimal PMOS width and the E D^n optima by numerical minimization, against the closed forms;
- the lab's module is checked against these results; ngspice confirms the step delays, the RC delay and the ring
  in delay.cir and ring.cir (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import delay as dl  # noqa: E402

v = Verifier.from_files("19-02", ROOT / "chapters" / "19-02-cmos-inverter-dynamic.md",
                        ROOT / "solutions" / "19-02-solutions.md", LAB / "README.md")
LN2 = math.log(2)
P, F, KO = 1e-12, 1e-15, 1e3


# ---------------------------------------------------------------- independent device and delay routines
def cur(k, vt, vg, vd):
    """Square-law NMOS (lambda = 0) with gate voltage vg and drain voltage vd, source at ground."""
    vov = vg - vt
    if vov <= 0 or vd <= 0:
        return 0.0
    return k * (vov * vd - vd * vd / 2) if vd < vov else k * vov * vov / 2


def step_delay(c, k, vdd, vt):
    """50% fall time by direct numerical integration of the discharge."""
    ev = lambda _t, y: y[0] - vdd / 2  # noqa: E731
    ev.terminal = True
    tscale = c * vdd / (k * (vdd - vt) ** 2)
    sol = solve_ivp(lambda _t, y: [-cur(k, vt, vdd, y[0]) / c], (0, 100 * tscale), [vdd], events=ev,
                    method="LSODA", rtol=1e-12, atol=1e-18, max_step=tscale / 500)
    return float(sol.t_events[0][0])


def time_in_saturation(c, k, vdd, vt):
    ev = lambda _t, y: y[0] - (vdd - vt)  # noqa: E731
    ev.terminal = True
    tscale = c * vdd / (k * (vdd - vt) ** 2)
    sol = solve_ivp(lambda _t, y: [-cur(k, vt, vdd, y[0]) / c], (0, 100 * tscale), [vdd], events=ev,
                    rtol=1e-12, atol=1e-18, max_step=tscale / 500)
    return float(sol.t_events[0][0])


def req(k, vdd, vt):
    vov = vdd - vt
    return quad(lambda x: x / cur(k, vt, vdd, x), vdd / 2, vdd, points=[vov], epsabs=0, epsrel=1e-13)[0] / (vdd / 2)


def req_closed(k, vdd, vt):
    vov = vdd - vt
    return 2 / vdd * ((vdd ** 2 - vov ** 2) / (k * vov ** 2) + 2 / k * math.log((4 * vov - vdd) / (2 * vov)))


def ring_period(n, k, vdd, vt, c):
    """Ring of n identical symmetric inverters (kn = kp = k, VTN = |VTP| = vt)."""
    def rhs(_t, x):
        out = np.empty(n)
        for i in range(n):
            vin = x[i - 1]
            ipull = cur(k, vt, vdd - vin, vdd - x[i])  # PMOS as an NMOS mirrored about VDD
            idown = cur(k, vt, vin, x[i])
            out[i] = (ipull - idown) / c
        return out
    td = step_delay(c, k, vdd, vt)
    x0 = np.array([0.0 if i % 2 == 0 else vdd for i in range(n)])
    x0[0] = vdd / 2 + 0.02
    t_end = 80 * n * td
    sol = solve_ivp(rhs, (0, t_end), x0, method="LSODA", rtol=1e-10, atol=1e-13, dense_output=True,
                    max_step=td / 25)
    t = np.linspace(0, t_end, 400001)
    y = sol.sol(t)[0] - vdd / 2
    idx = np.nonzero((y[:-1] < 0) & (y[1:] >= 0))[0]
    cross = t[idx] - y[idx] * (t[idx + 1] - t[idx]) / (y[idx + 1] - y[idx])
    cross = cross[len(cross) // 2:]
    return float((cross[-1] - cross[0]) / (len(cross) - 1))


# ---------------------------------------------------------------- symbolic check of the closed form (§3.3)
Cs, ks, Vd, Vt, V = sp.symbols("C k V_DD V_t V", positive=True)
Vo = Vd - Vt
t1s = Cs * Vt / (ks * Vo ** 2 / 2)
t2s = sp.integrate(Cs / (ks * (Vo * V - V ** 2 / 2)), (V, Vd / 2, Vo))
closed = Cs / (ks * Vo) * (2 * Vt / Vo + sp.log(4 * Vo / Vd - 1))
num = {Cs: 20e-15, ks: 200e-6, Vd: 1.2, Vt: 0.35}
v.assert_true("closed-form step delay matches the symbolic integral",
              abs(float((t1s + t2s - closed).subs(num))) < 1e-22, "sympy")

# ---------------------------------------------------------------- Example 1
cg = 1.0 * (0.4 + 0.8)
cint = 0.8 * 1.2
cext = 4 * cg + 2
v.check("Ex 19-02.1a", cg)
v.check("Ex 19-02.1b", cint)
v.check("Ex 19-02.1c", cext)
v.check("Ex 19-02.1d", cint + cext)
v.check("Ex 19-02.1e", cint / cg)

# ---------------------------------------------------------------- Example 2 and the text
c, k, vdd, vt = 20 * F, 200e-6, 1.2, 0.35
tsat = time_in_saturation(c, k, vdd, vt)
thl = step_delay(c, k, vdd, vt)
tlh = step_delay(c, 100e-6, vdd, vt)  # mirror image: the PMOS charging with half the strength
v.check("Ex 19-02.2a", tsat / P)
v.check("Ex 19-02.2b", thl / P)
v.check("Ex 19-02.2c", tlh / P)
v.check("Ex 19-02.2d", (thl + tlh) / 2 / P)
v.check("Txt 19-02.a", (thl - tsat) / P)
v.assert_true("closed form equals the ODE delay", abs(dl.tp_step_exact(c, k, vdd, vt) - thl) < 1e-16,
              f"{dl.tp_step_exact(c, k, vdd, vt):.6e} vs {thl:.6e}")
v.assert_true("lab ODE matches", abs(dl.tp_step_ode(c, k, vdd, vt) - thl) < 1e-15, "tp_step_ode")

# ---------------------------------------------------------------- Example 3
r = req(k, vdd, vt)
v.check("Ex 19-02.3a", r / KO)
v.check("Ex 19-02.3b", 3 * vdd / (4 * 0.5 * k * (vdd - vt) ** 2) / KO)
trc = LN2 * 12.57e3 * c
v.check("Ex 19-02.3c", trc / P)
v.check("Ex 19-02.3d", 100 * (trc / thl - 1))
v.check("Txt 19-02.f", 12.57e3 * c / P)
v.assert_true("lab r_eq matches", abs(dl.r_eq(k, vdd, vt) - r) < 1e-6 * r, "r_eq")
# the RC curve starts faster but crosses the exact one before the 50% point (Figure 1 and the sanity check)
v.assert_true("RC initial current exceeds I_sat", vdd / r > 0.5 * k * (vdd - vt) ** 2, "1.2 V/R_eq > I_sat")

# ---------------------------------------------------------------- Example 4
tp0 = LN2 * 12.57e3 * 2 * F
v.check("Ex 19-02.4a", tp0 / P)
v.check("Ex 19-02.4b", tp0 * (1 + 4 * 2 / 2) / P)
v.check("Ex 19-02.4c", tp0 * (1 + 50 / 2) / P)
v.check("Ex 19-02.4d", tp0 * (1 + 50 / 8) / P)
v.check("Ex 19-02.4e", (1 + 50 / 2) / (1 + 50 / 8))
v.check("Lab 19-02.b", tp0 * (1 + 50 / 4) / P)
v.assert_true("lab tp_with_fanout matches", abs(dl.tp_with_fanout(tp0, 50 * F, 2 * F, 4) - tp0 * 7.25) < 1e-18, "")

# ---------------------------------------------------------------- Example 5 and Lab Part 5
t10 = step_delay(10 * F, k, vdd, vt)
v.check("Ex 19-02.5a", t10 / P)
v.check("Ex 19-02.5b", 1 / (10 * t10) / 1e9)
per5 = ring_period(5, k, vdd, vt, 10 * F)
v.check("Ex 19-02.5c", per5 / 10 / P)
v.check("Ex 19-02.5d", per5 / 10 / t10)
v.check("Ex 19-02.5e", 1 / per5 / 1e6)
per7 = ring_period(7, k, vdd, vt, 10 * F)
v.check("Lab 19-02.c", per7 * 1e9)
v.check("Lab 19-02.d", per7 / 14 / P)
v.assert_true("lab simulate_ring matches (5 stages)",
              abs(dl.simulate_ring(5, k, k, vdd, vt, vt, 10 * F) - per5) < 2e-4 * per5, "")

# ---------------------------------------------------------------- Example 6 and §3.7
def drat(a, lo=0.6, hi=1.2, vtx=0.35):
    return (lo / (lo - vtx) ** a) / (hi / (hi - vtx) ** a)


def edp_opt(a, vtx):
    return minimize_scalar(lambda x: math.log(x ** 3 / (x - vtx) ** a), bounds=(vtx * 1.0001, 20 * vtx),
                           method="bounded", options={"xatol": 1e-12}).x


v.check("Ex 19-02.6a", (0.6 / 1.2) ** 2)
v.check("Ex 19-02.6b", drat(1.3))
v.check("Ex 19-02.6c", drat(2.0))
v.check("Ex 19-02.6d", edp_opt(1.3, 0.35))
v.check("Ex 19-02.6e", edp_opt(2.0, 0.35))
v.check("Txt 19-02.b", edp_opt(1.0, 1.0))
v.check("Txt 19-02.c", edp_opt(1.3, 1.0))
edp = lambda x: x ** 3 / (x - 0.35) ** 1.3  # noqa: E731
emin = edp(edp_opt(1.3, 0.35))
v.check("Txt 19-02.n", brentq(lambda x: edp(x) - 1.1 * emin, 0.36, edp_opt(1.3, 0.35), xtol=1e-14))
v.check("Txt 19-02.o", brentq(lambda x: edp(x) - 1.1 * emin, edp_opt(1.3, 0.35), 3.0, xtol=1e-14))
v.assert_true("lab edp_optimal_vdd matches", abs(dl.edp_optimal_vdd(0.35, 1.3) - edp_opt(1.3, 0.35)) < 1e-8, "")

# ---------------------------------------------------------------- FO4, rings and practitioner arithmetic
g_ho = sp.solve(sp.Eq(1 + 4 / sp.Symbol("g"), 3 * (1 + 1 / sp.Symbol("g"))), sp.Symbol("g"))[0]
v.check("Txt 19-02.d", float(g_ho))
v.check("Txt 19-02.g", 1 + 4 / float(g_ho))
v.check("Txt 19-02.e", 1 / (2 * 11 * 1e9) / P)
v.check("Txt 19-02.h", 360 * 0.18)
v.check("Txt 19-02.i", 77.2 / 2.47)
v.check("Txt 19-02.j", 1.8 / 0.8)
v.check("Txt 19-02.k", 44.1 / 24.7)
v.check("Txt 19-02.l", 1.0611080997 / 0.6240911176)  # IRDS 2024 MM01 "CV/I (ps) - FO3 load, HP"
v.check("Txt 19-02.m", 77.2 / 34.7)

# ---------------------------------------------------------------- Problems 1-3
cg1 = 1.2 * 0.9
v.check("19-02.1a", cg1)
v.check("19-02.1b", 1.0 * 0.9)
v.check("19-02.1c", 3 * cg1 + 1.5)
v.check("19-02.1d", 0.9 + 3 * cg1 + 1.5)
v.check("19-02.1e", 0.9 / cg1)
v.check("19-02.2a", 0.3 + 0.3 + 2 * (0.1 + 0.1))
v.check("19-02.2b", 0.3 + 0.3 + 0.1 + 0.1)
tp3 = 1 / (2 * 31 * 450e6)
v.check("19-02.3a", tp3 / P)
v.check("19-02.3b", 1 / (2 * 51 * tp3) / 1e6)

# ---------------------------------------------------------------- Problems 4, 5, 10
c4, k4, vdd4, vt4 = 15 * F, 300e-6, 1.0, 0.3
ts4 = time_in_saturation(c4, k4, vdd4, vt4)
t4 = step_delay(c4, k4, vdd4, vt4)
v.check("19-02.4a", ts4 / P)
v.check("19-02.4b", (t4 - ts4) / P)
v.check("19-02.4c", t4 / P)
r4 = req(k4, vdd4, vt4)
ra4 = 3 * vdd4 / (4 * 0.5 * k4 * 0.49)
v.check("19-02.5a", r4 / KO)
v.check("19-02.5b", ra4 / KO)
v.check("19-02.5c", LN2 * r4 * c4 / P)
v.check("19-02.5d", 100 * (LN2 * r4 * c4 / t4 - 1))
v.check("19-02.5e", LN2 * ra4 * c4 / P)
v.check("19-02.5f", 100 * (LN2 * ra4 * c4 / t4 - 1))
v.check("19-02.10a", req_closed(200e-6, 1.2, 0.35) / KO)
v.assert_true("closed-form R_eq equals quadrature", abs(req_closed(k4, vdd4, vt4) - r4) < 1e-8 * r4, "")


def rc_ratio(x):
    return LN2 * req(1e-4, 1.0, x) * 1e-14 / step_delay(1e-14, 1e-4, 1.0, x)


v.check("19-02.10b", rc_ratio(0.2))
v.check("19-02.10c", rc_ratio(0.4))
v.check("Lab 19-02.a", rc_ratio(0.45))
v.assert_true("RC ratio independent of C and k",
              abs(LN2 * req(7e-4, 2.0, 0.8) * 3e-15 / step_delay(3e-15, 7e-4, 2.0, 0.8) - rc_ratio(0.4)) < 1e-9, "")

# ---------------------------------------------------------------- Problems 6-9
v.check("19-02.6a", (40 + 100) / 2)
v.check("19-02.6b", 100 / 2.5)
v.check("19-02.6c", (40 + 100 / 2.5) / 2)
v.check("19-02.6d", (1 + 2.5) / 2)
tp07 = LN2 * 10e3 * 1.5 * F
v.check("19-02.7a", tp07 / P)
v.check("19-02.7b", 1.5 / 2)
v.check("19-02.7c", tp07 * (1 + 4 / 0.75) / P)
v.check("19-02.7d", tp07 * (1 + 100 / 1.5) / P)
v.check("19-02.7e", tp07 * (1 + 100 / 15) / P)
v.check("19-02.7f", 10 * 2)
fo1 = 1 / (2 * 101 * 150e6)
v.check("19-02.8a", fo1 / P)
v.check("19-02.8b", 5 * fo1 / 2 / P)
v.check("19-02.8c", 3 * fo1 / P)
v.check("19-02.8d", float(g_ho))
d9 = drat(1.4, 0.5, 0.9, 0.3)
v.check("19-02.9a", d9)
v.check("19-02.9b", (0.5 / 0.9) ** 2)
v.check("19-02.9e", (0.9 / 0.5) ** 2)
v.check("19-02.9c", (0.5 / 0.9) ** 2 * d9)
v.check("19-02.9d", edp_opt(1.4, 0.3))

# ---------------------------------------------------------------- Problem 11: minimize the full delay numerically
def tp_beta(beta, rr=2.5, gamma=0.8, n=4):
    rn = 1.0
    load = (gamma + n) * (1 + beta)
    return 0.5 * LN2 * (rn * load + rr * rn / beta * load)


bopt = minimize_scalar(tp_beta, bounds=(0.2, 10), method="bounded", options={"xatol": 1e-12}).x
v.check("19-02.11a", bopt)
v.check("19-02.11b", 100 * (1 - tp_beta(bopt) / tp_beta(2.5)))
v.check("19-02.11c", (1 + bopt) * (1 + 2.5 / bopt))
v.assert_true("beta = 1 and beta = r give the same delay", abs(tp_beta(1.0) - tp_beta(2.5)) < 1e-12, "")
v.assert_true("optimum independent of gamma and N",
              abs(minimize_scalar(lambda b: tp_beta(b, 2.5, 0.3, 1), bounds=(0.2, 10), method="bounded",
                                  options={"xatol": 1e-12}).x - bopt) < 1e-6, "")


# ---------------------------------------------------------------- Problem 12
def edn_opt(n, a=1.3, vtx=0.35):
    return minimize_scalar(lambda x: (2 + n) * math.log(x) - n * a * math.log(x - vtx),
                           bounds=(vtx * 1.0001, 50 * vtx), method="bounded", options={"xatol": 1e-12}).x


v.check("19-02.12a", edn_opt(1))
v.check("19-02.12b", edn_opt(2))
v.check("19-02.12c", edn_opt(3))
xs = np.linspace(0.4, 10, 500)
ed2 = (xs / (xs - 0.35)) ** 4
v.assert_true("square-law E D^2 decreases monotonically", bool(np.all(np.diff(ed2) < 0)), "")


# ---------------------------------------------------------------- Problem 13: capacitances from device data
WN, WP, L13, COX, COV, CJ, CJSW, LD, KB, KS = 0.5, 1.0, 0.15, 8.5, 0.3, 1.0, 0.25, 0.5, 0.62, 0.75


def c_int_dev(w):
    return w * LD * CJ * KB + (2 * LD + w) * CJSW * KS + 2 * COV * w


cg13 = (COX * L13 + 2 * COV) * (WN + WP)
v.check("19-02.13a", cg13)
v.check("19-02.13b", c_int_dev(WN))
v.check("19-02.13c", c_int_dev(WP))
v.check("19-02.13d", c_int_dev(WN) + c_int_dev(WP))
v.check("19-02.13e", (c_int_dev(WN) + c_int_dev(WP)) / cg13)
v.check("19-02.13f", c_int_dev(WN) + c_int_dev(WP) + 4 * cg13)


# ---------------------------------------------------------------- Problem 14: fall time by integrating the discharge ODE
def discharge_times(c, k, vdd, vt, levels):
    from scipy.integrate import solve_ivp

    def ids_n(vo):
        vov = vdd - vt
        return k * (vov * vo - vo * vo / 2) if vo < vov else k * vov * vov / 2

    out = {}
    for lev in levels:
        ev = lambda t, y, lev=lev: y[0] - lev
        ev.terminal, ev.direction = True, -1
        sol = solve_ivp(lambda t, y: [-ids_n(y[0]) / c], (0, 5e-9), [vdd], events=ev, rtol=1e-11, atol=1e-15, max_step=1e-13)
        out[lev] = sol.t_events[0][0]
    return out


tt = discharge_times(20e-15, 200e-6, 1.2, 0.35, (1.08, 0.6, 0.12))
v.check("19-02.14a", tt[1.08] / P)
v.check("19-02.14b", tt[0.12] / P)
v.check("19-02.14c", (tt[0.12] - tt[1.08]) / P)
v.check("19-02.14d", (tt[0.12] - tt[1.08]) / tt[0.6])
v.check("19-02.14e", math.log(9) * 12.5728e3 * 20e-15 / P)
v.check("19-02.14f", 100 * (math.log(9) * 12.5728e3 * 20e-15 / (tt[0.12] - tt[1.08]) - 1))

sys.exit(v.finish())
