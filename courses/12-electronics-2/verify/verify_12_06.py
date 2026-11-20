#!/usr/bin/env python3
"""Verify every number in chapter 12-06 (stability and frequency compensation), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- crossovers by root finding on |T(jf)| = 1 with T evaluated as a complex product or from a solved circuit;
- phases unwrapped numerically along a dense frequency grid (never summed from arctangent formulas);
- the two-stage amplifier by complex nodal analysis of the full two- or three-node circuit;
- the closed-loop Q from the roots of 1 + T(s) = 0, overshoot from a simulated step response, and peaking
  by bounded optimization of the closed-loop magnitude.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.linalg import eigvals
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-06-stability-and-compensation.md", COURSE / "solutions" / "12-06-solutions.md"]
lab = COURSE / "labs" / "12-06-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-06", *files)
TP = 2 * math.pi
deg = math.degrees


# ============================================================ loop-gain tools
def poles_T(T0, fps):
    """Loop gain with real poles at the listed frequencies (Hz), as a function of frequency."""
    return lambda f: T0 / np.prod([1 + 1j * f / p for p in fps])


def phase(Tf, f, f_lo=1e-3, n=3000):
    """Unwrapped phase (degrees) of T at f, following T continuously from f_lo."""
    fs = np.geomspace(f_lo, f, n)
    return float(deg(np.unwrap(np.angle([Tf(x) for x in fs]))[-1]))


def crossover(Tf, lo=1e-3, hi=1e12):
    return brentq(lambda f: abs(Tf(f)) - 1, lo, hi, xtol=1e-9, rtol=1e-14)


def margins(Tf, lo=1e-3, hi=1e12):
    fc = crossover(Tf, lo, hi)
    return fc, 180 + phase(Tf, fc, lo)


def f180(Tf, lo, hi, f_lo=1e-3):
    return brentq(lambda f: phase(Tf, f, f_lo) + 180, lo, hi, xtol=1e-6, rtol=1e-12)


def closed_bw(Tf, f_lo):
    H = lambda f: abs(Tf(f) / (1 + Tf(f)))  # noqa: E731
    h0 = H(f_lo)
    return brentq(lambda f: H(f) - h0 / math.sqrt(2), f_lo * 10, 1e11, xtol=1e-6, rtol=1e-12)


def two_pole(r):
    """Normalized two-pole loop wu/(s(1 + s/w2)) with wu = 1 rad/s, w2 = r: PM, Q, overshoot (%), peaking (dB)."""
    Tf = lambda w: 1 / (1j * w * (1 + 1j * w / r))  # noqa: E731
    wc = brentq(lambda w: abs(Tf(w)) - 1, 1e-6, 1e3, xtol=1e-15)
    pm = 180 + deg(np.angle(Tf(wc)))                 # phase stays in (-180, -90): no unwrapping needed
    # closed loop: T/(1 + T) = 1/(1 + s + s^2/r); its poles give Q
    p = np.roots([1 / r, 1, 1])
    Q = abs(p[0]) / abs(2 * p[0].real)
    sysc = signal.lti([1], [1 / r, 1, 1])
    t = np.linspace(0, 60 / math.sqrt(r), 400001)
    _, y = signal.step(sysc, T=t)
    os_ = 100 * max(float(np.max(y)) - 1, 0.0)
    H = lambda w: abs(1 / (1 + 1j * w - w * w / r))  # noqa: E731
    res = minimize_scalar(lambda w: -H(w), bounds=(1e-6, 10 * math.sqrt(r)), method="bounded",
                          options={"xatol": 1e-12})
    pk = 20 * math.log10(max(-res.fun, 1.0))
    return dict(wc=wc, pm=pm, Q=Q, os=os_, pk=pk, pkr=max(-res.fun, 1.0))


# ============================================================ complex nodal analysis (two-stage amplifier)
def solve_ac(nodes, elems, fixed, f):
    idx = {n: i for i, n in enumerate(nodes)}
    N = len(nodes)
    Y = np.zeros((N, N), complex)
    b = np.zeros(N, complex)
    fx = dict(fixed)
    fx.setdefault("0", 0.0)
    s = 1j * TP * f

    def add(i, j, val):
        if i not in idx:
            return
        if j in idx:
            Y[idx[i], idx[j]] += val
        else:
            b[idx[i]] -= val * fx[j]

    for e in elems:
        if e[0] in ("R", "C"):
            a, c = e[1], e[2]
            y = 1 / e[3] if e[0] == "R" else s * e[3]
            add(a, a, y); add(a, c, -y); add(c, c, y); add(c, a, -y)
        elif e[0] == "G":                        # gm*(v(cp) - v(cn)) leaves d, enters s
            d, sn, cp, cn, gm = e[1:]
            add(d, cp, gm); add(d, cn, -gm); add(sn, cp, -gm); add(sn, cn, gm)
    x = np.linalg.solve(Y, b)
    return {n: x[idx[n]] for n in nodes}


def stage_elems(gm1, R1, C1, gm2, R2, CL, Cc, Rz=0.0):
    el = [("G", "n1", "0", "in", "0", gm1), ("R", "n1", "0", R1), ("C", "n1", "0", C1),
          ("G", "n2", "0", "n1", "0", gm2), ("R", "n2", "0", R2), ("C", "n2", "0", CL)]
    if Rz > 0:
        return el + [("R", "n1", "m", Rz), ("C", "m", "n2", Cc)], ["n1", "n2", "m"]
    return el + [("C", "n1", "n2", Cc)], ["n1", "n2"]


def two_stage(*args, **kw):
    el, nodes = stage_elems(*args, **kw)
    return lambda f: solve_ac(nodes, el, {"in": 1.0}, f)["n2"]


def stage_poles(*args, **kw):
    """Natural frequencies (Hz) of the amplifier with its input grounded, from the generalized eigenproblem."""
    el, nodes = stage_elems(*args, **kw)
    idx = {n: i for i, n in enumerate(nodes)}
    N = len(nodes)
    G, C = np.zeros((N, N)), np.zeros((N, N))

    def add(M, i, j, val):
        if i in idx and j in idx:
            M[idx[i], idx[j]] += val

    for e in el:
        if e[0] in ("R", "C"):
            M, val = (G, 1 / e[3]) if e[0] == "R" else (C, e[3])
            add(M, e[1], e[1], val); add(M, e[2], e[2], val); add(M, e[1], e[2], -val); add(M, e[2], e[1], -val)
        elif e[0] == "G":
            d, sn, cp, cn, gm = e[1:]
            add(G, d, cp, gm); add(G, d, cn, -gm); add(G, sn, cp, -gm); add(G, sn, cn, gm)
    lam = eigvals(G, -C)
    return np.sort(np.abs(lam[np.isfinite(lam)])) / TP


# ============================================================ §3.3 table and §3.5 rules
t1, t15, t2, t3 = two_pole(1.0), two_pole(1.5), two_pole(2.0), two_pole(3.0)
v.check("T 12-06.a", t1["pm"])
v.check("T 12-06.b", t1["os"])
v.check("T 12-06.c", t1["pk"])
v.check("T 12-06.d", t15["Q"])
v.check("T 12-06.e", t2["pm"])
v.check("T 12-06.f", t2["Q"])
v.check("T 12-06.g", t2["os"])
v.check("T 12-06.h", t3["pm"])
v.check("T 12-06.i", t3["Q"])
v.check("T 12-06.j", t3["os"])
v.assert_true("no peaking at r = 2 and r = 3", t2["pk"] < 1e-6 and t3["pk"] < 1e-6)
r45 = brentq(lambda r: two_pole(r)["pm"] - 45, 0.2, 3, xtol=1e-12)
t45 = two_pole(r45)
v.check("T 12-06.k", t45["os"])
ratio = 0.1                                          # g_m1/g_m2
v.check("T 12-06.l", deg(math.atan(ratio)))
v.check("T 12-06.m", 2.2 * ratio)
v.check("T 12-06.n", deg(math.atan(1 / 2.2)))
v.check("T 12-06.o", 90 - deg(math.atan(1 / 2.2)) - deg(math.atan(ratio)))
v.assert_true("r = 1.5 gives a crossover of sqrt(3)/2 times f_u", abs(t15["wc"] - math.sqrt(3) / 2) < 1e-9)

# ============================================================ Example 1
T1 = poles_T(1000, [1e3, 2e6])
v.check("Ex 12-06.1a", 1000 * 1e3 / 1e6)
v.check("Ex 12-06.1b", 90 + phase(poles_T(1, [2e6]), 1e6))   # dominant pole's 90 deg less the second pole's lag
fc1, pm1 = margins(T1)
v.check("Ex 12-06.1c", fc1 / 1e6)
v.check("Ex 12-06.1d", pm1)
v.check("Ex 12-06.1e", -phase(poles_T(1, [1e3]), fc1))
v.check("Ex 12-06.1f", -phase(poles_T(1, [2e6]), fc1))
v.check("Ex 12-06.1g", -phase(poles_T(1, [2e6]), 1e6))

# ============================================================ Example 2
v.check("Ex 12-06.2a", t15["pm"])
v.check("Ex 12-06.2b", t15["Q"])
v.check("Ex 12-06.2c", 1 / (2 * t15["Q"]))
v.check("Ex 12-06.2d", t15["os"])
v.check("Ex 12-06.2e", t15["pk"])
v.check("Ex 12-06.2f", t15["pkr"])

# ============================================================ Example 3: uncompensated three-pole amplifier
A0, fps = 1e4, [1e6, 10e6, 100e6]
T3 = poles_T(A0, fps)
f3 = f180(T3, 5e6, 1e9)
v.check("Ex 12-06.3a", f3 / 1e6)
v.assert_true("phase crossover at sqrt(f1 f2 + f1 f3 + f2 f3)", abs(f3 / 1e6 / math.sqrt(1110) - 1) < 1e-8)
v.check("Ex 12-06.3b", abs(T3(f3)))
v.check("Ex 12-06.3c", -20 * math.log10(abs(T3(f3))))
fc3, pm3 = margins(T3)
v.check("Ex 12-06.3d", fc3 / 1e6)
v.check("Ex 12-06.3e", pm3)
# the closed loop really has right-half-plane poles
den = np.poly1d([1.0])
for p in fps:
    den = den * np.poly1d([1 / (TP * p), 1])
v.assert_true("closed-loop poles of the buffer lie in the right half-plane",
              np.max((den + np.poly1d([A0])).roots.real) > 0)

# ============================================================ Example 4: add a pole or move one
fd = brentq(lambda x: margins(poles_T(A0, [x] + fps))[1] - 60, 1, 1e4, xtol=1e-10)
v.check("Ex 12-06.4a", fd)
fc4a = crossover(poles_T(A0, [fd] + fps))
v.check("Ex 12-06.4b", fc4a / 1e6)
bw_a = closed_bw(poles_T(A0, [fd] + fps), 1e-3)
v.check("Ex 12-06.4c", bw_a / 1e6)
f1p = brentq(lambda x: margins(poles_T(A0, [x] + fps[1:]))[1] - 60, 1, 1e5, xtol=1e-10)
v.check("Ex 12-06.4d", f1p)
fc4b = crossover(poles_T(A0, [f1p] + fps[1:]))
v.check("Ex 12-06.4e", fc4b / 1e6)
bw_b = closed_bw(poles_T(A0, [f1p] + fps[1:]), 1e-3)
v.check("Ex 12-06.4f", bw_b / 1e6)
v.check("Ex 12-06.4g", bw_b / bw_a)

# ============================================================ Example 5: Miller compensation
gm1, R1, C1, gm2, R2, CL = 1e-3, 200e3, 0.2e-12, 10e-3, 50e3, 5e-12
Cc = 0.22 * CL
A5 = two_stage(gm1, R1, C1, gm2, R2, CL, Cc)
v.check("Ex 12-06.5a", abs(A5(1e-4)))
v.check("Ex 12-06.5b", Cc * 1e12)
v.check("Ex 12-06.5c", gm1 / (TP * Cc) / 1e6)
v.check("Ex 12-06.5d", gm2 / (TP * CL) / 1e6)
v.check("Ex 12-06.5e", gm2 / (TP * Cc) / 1e6)
v.check("Ex 12-06.5f", 90 - deg(math.atan(gm1 / Cc / (gm2 / CL))) - deg(math.atan(gm1 / gm2)))
p2b = gm2 * Cc / (C1 * CL + Cc * (C1 + CL)) / TP
v.check("Ex 12-06.5g", p2b / 1e6)
pz5 = stage_poles(gm1, R1, C1, gm2, R2, CL, Cc)
v.assert_true("improved p2 estimate within 1% of the circuit's upper pole", abs(pz5[-1] / p2b - 1) < 0.01)
v.assert_true("zero of the full circuit at g_m2/C_c (|A| -> 0 there along the real axis)",
              abs(solve_ac(["n1", "n2"], stage_elems(gm1, R1, C1, gm2, R2, CL, Cc)[0], {"in": 1.0},
                           gm2 / Cc / (1j * TP))["n2"]) < 1e-9)
fc5, pm5 = margins(A5)
v.check("Ex 12-06.5h", fc5 / 1e6)
v.check("Ex 12-06.5i", pm5)
Cc60 = brentq(lambda c: margins(two_stage(gm1, R1, C1, gm2, R2, CL, c * 1e-12))[1] - 60, 0.6, 3.0, xtol=1e-10)
v.check("Ex 12-06.5j", Cc60)
v.check("Ex 12-06.5k", gm1 / (TP * Cc60 * 1e-12) / 1e6)
v.check("Ex 12-06.5l", pz5[0] / 1e3)                 # the circuit's lowest natural frequency
v.check("Ex 12-06.5m", 1 / (TP * gm2 * R1 * R2 * Cc) / 1e3)

# ============================================================ Example 6: nulling resistor
Rz0 = 1 / gm2
v.check("Ex 12-06.6a", Rz0)
v.check("Ex 12-06.6b", margins(two_stage(gm1, R1, C1, gm2, R2, CL, Cc, Rz=Rz0))[1])
Rzc = (1 + CL / Cc) / gm2
v.check("Ex 12-06.6c", Rzc)
fc6, pm6 = margins(two_stage(gm1, R1, C1, gm2, R2, CL, Cc, Rz=Rzc))
v.check("Ex 12-06.6d", fc6 / 1e6)
v.check("Ex 12-06.6e", pm6)
v.check("Ex 12-06.6f", 1 / (TP * Rzc * C1) / 1e6)
v.check("Ex 12-06.6g", CL / Cc)
pz6 = stage_poles(gm1, R1, C1, gm2, R2, CL, Cc, Rz=Rzc)
v.assert_true("third pole of the circuit within 15% of 1/(2 pi R_z C_1)",
              abs(pz6[-1] / (1 / (TP * Rzc * C1)) - 1) < 0.15)

# ============================================================ practitioner and guided exercise
r55 = brentq(lambda r: two_pole(r)["pm"] - 55, 0.5, 3, xtol=1e-12)
t55 = two_pole(r55)
v.check("Prac 12-06.a", r55)
v.check("Prac 12-06.b", t55["Q"])
v.check("Prac 12-06.c", t55["os"])
v.check("Sim 12-06.a", gm1 / (TP * 0.55e-12) / 1e6)
fch, pmh = margins(two_stage(gm1, R1, C1, gm2, R2, CL, 0.55e-12))
v.check("Sim 12-06.b", fch / 1e6)
v.check("Sim 12-06.c", pmh)

# ============================================================ solutions
# 1
v.check("12-06.1a", 180 - 125)
v.check("12-06.1b", -20 * math.log10(0.2))
# 2
T2 = poles_T(1e4, [100])
fc2, pm2 = margins(T2)
v.check("12-06.2a", fc2 / 1e6)
v.check("12-06.2b", pm2)
v.check("12-06.2d", phase(T2, fc2))
clp = np.roots([1 / (TP * 100), 1 + 1e4])
v.check("12-06.2c", abs(clp[0]) / TP / 1e6)
# 3
v.check("12-06.3a", t1["pm"])
v.check("12-06.3b", t1["Q"])
v.check("12-06.3c", t1["os"])
v.check("12-06.3d", t1["wc"])
# 4
v.check("12-06.4a", r45)
v.check("12-06.4b", t45["Q"])
v.check("12-06.4c", 1 / (2 * t45["Q"]))
v.check("12-06.4d", t45["os"])
# 5
bmax = brentq(lambda b: -20 * math.log10(abs(poles_T(A0 * b, fps)(f3))), 1e-4, 1.0, xtol=1e-15)
v.check("12-06.5a", bmax)
v.check("12-06.5b", 1 / bmax)
v.check("12-06.5c", 20 * math.log10(1 / bmax))
# 6
A6, fp6 = 1e5, [2e6, 20e6]
T6r = poles_T(A6, [20.0] + fp6)
v.check("12-06.6a", 2e6 / A6)
fc6r, pm6r = margins(T6r)
v.check("12-06.6b", pm6r)
v.check("12-06.6e", fc6r / 1e6)
v.check("12-06.6f", -phase(poles_T(1, [2e6]), fc6r))
v.check("12-06.6g", -phase(poles_T(1, [20e6]), fc6r))
v.check("12-06.6h", -phase(poles_T(1, [20.0]), fc6r))
fd6 = brentq(lambda x: margins(poles_T(A6, [x] + fp6))[1] - 45, 1, 1e3, xtol=1e-10)
v.check("12-06.6c", fd6)
v.check("12-06.6d", crossover(poles_T(A6, [fd6] + fp6)) / 1e6)
# 7
g1, g2, CL7 = 0.5e-3, 5e-3, 2e-12
Cc7 = 2.2 * (g1 / g2) * CL7
v.check("12-06.7a", Cc7 * 1e12)
v.check("12-06.7b", g1 / (TP * Cc7) / 1e6)
v.check("12-06.7c", g2 / (TP * CL7) / 1e6)
v.check("12-06.7d", g2 / (TP * Cc7) / 1e6)
v.check("12-06.7e", 90 - deg(math.atan((g1 / Cc7) / (g2 / CL7))) - deg(math.atan(g1 / g2)))
# 8
v.check("12-06.8a", 90 - deg(math.atan(1 / 2.2)) - deg(math.atan(1.0)))
# 9
v.check("12-06.9a", 1 / g2)
v.check("12-06.9b", (1 + CL7 / Cc7) / g2)
v.check("12-06.9c", 1 / (TP * (1 + CL7 / Cc7) / g2 * 0.1e-12) / 1e6)
v.check("12-06.9d", CL7 / Cc7)
# 10
v.check("12-06.10a", gm2 / (TP * 10e-12) / 1e6)
pm10e = 90 - deg(math.atan((gm1 / Cc) / (gm2 / 10e-12))) - deg(math.atan(gm1 / gm2))
v.check("12-06.10b", pm10e)
fc10, pm10 = margins(two_stage(gm1, R1, C1, gm2, R2, 10e-12, Cc))
v.check("12-06.10c", pm10)
v.check("12-06.10d", fc10 / 1e6)
v.check("12-06.10e", pm5 - pm10)
v.check("12-06.10f", (90 - deg(math.atan(gm1 / Cc / (gm2 / CL))) - deg(math.atan(gm1 / gm2))) - pm10e)


# 11: solve the estimate numerically (not by the quadratic)
def pm_est(c):
    wu, p2, z = gm1 / c, gm2 * c / (C1 * CL + c * (C1 + CL)), gm2 / c
    return 90 - deg(math.atan(wu / p2)) - deg(math.atan(wu / z))


c11 = brentq(lambda c: pm_est(c * 1e-12) - 60, 0.5, 5, xtol=1e-12)
v.check("12-06.11a", math.tan(math.radians(90 - 60 - deg(math.atan(gm1 / gm2)))))
v.check("12-06.11b", c11)
v.check("12-06.11c", margins(two_stage(gm1, R1, C1, gm2, R2, CL, c11 * 1e-12))[1])
v.check("12-06.11d", Cc60)
v.check("12-06.11e", deg(math.atan(gm1 / gm2)))
v.check("12-06.11f", 90 - 60 - deg(math.atan(gm1 / gm2)))
v.check("12-06.11g", 1 / c11)
# 12: find r whose simulated overshoot is 20%
r12 = brentq(lambda r: two_pole(r)["os"] - 20, 0.3, 3, xtol=1e-10)
t12 = two_pole(r12)
v.check("12-06.12a", 1 / (2 * t12["Q"]))
v.check("12-06.12b", t12["Q"])
v.check("12-06.12c", r12)
v.check("12-06.12d", t12["pm"])

# ============================================================ lab README
if lab.exists():
    T_l = poles_T(A0 * 0.005, fps)
    v.check("Lab 12-06.a", -20 * math.log10(abs(T_l(f3))))
    v.check("Lab 12-06.b", margins(T_l)[1])
    pms = [margins(two_stage(gm1, R1, C1, gm2, R2, CL, Cc, Rz=x))[1] for x in (1.0, 250.0, 500.0, 750.0, 1000.0)]
    v.assert_true("phase margin rises monotonically with R_z up to 1 kOhm", all(np.diff(pms) > 0))
    fcl, pml = margins(two_stage(gm1, R1, C1, gm2, R2, CL, Cc, Rz=1000.0))
    v.check("Lab 12-06.c", pml)
    v.check("Lab 12-06.d", fcl / 1e6)

sys.exit(v.finish())
