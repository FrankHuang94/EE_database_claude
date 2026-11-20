#!/usr/bin/env python3
"""Verify chapter 15-02 (transfer functions and block diagrams): examples, problems and lab answers.

Each value is recomputed by a route other than the hand formula where one exists:
- block diagrams are written as the raw signal equations and solved with sympy (no reduction rules used);
- transfer functions of state-space models come from sympy's C (sI - A)^-1 B, poles from eigenvalues;
- Mason's formula (labs/15-02-lab/blocks.py) is checked against a direct linear solve of the node equations,
  on the chapter's graphs and on random graphs;
- overshoots and peak times come from simulated step responses (scipy.signal / solve_ivp), not formulas.
The ngspice netlist labs/15-02-lab/two_loop.cir confirms Example 15-02.3 independently (tools/run_spice.py).
"""
from __future__ import annotations

import math
import random
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
sys.path.insert(0, str(ROOT / "labs" / "15-02-lab"))
from eeverify import Verifier  # noqa: E402
import blocks  # noqa: E402

CH = ROOT / "chapters" / "15-02-transfer-functions-and-block-diagrams.md"
v = Verifier.from_files("15-02", CH, ROOT / "solutions" / "15-02-solutions.md", ROOT / "labs" / "15-02-lab" / "README.md")
s, t = sp.symbols("s t")


def solve_signals(eqs, unknowns, out):
    """Solve linear signal equations (each an Eq) for the unknown signals and return out, simplified."""
    sol = sp.solve(eqs, unknowns, dict=True)[0]
    return sp.factor(sp.simplify(out.subs(sol)))


def num_den(expr):
    n, d = sp.fraction(sp.together(expr))
    return [float(c) for c in sp.Poly(n, s).all_coeffs()], [float(c) for c in sp.Poly(d, s).all_coeffs()]


def step_peak(num, den, t_end, n=400001):
    """Peak value, its time and the final sample of the unit-step response (simulated)."""
    tt = np.linspace(0, t_end, n)
    _, y = signal.step(signal.TransferFunction(num, den), T=tt)
    k = int(np.argmax(y))
    return y[k], tt[k], y[-1], tt, y


def exact_peak_time(num, den, t_guess, width):
    """Refine the peak time as the zero of the impulse response near t_guess (brentq, tight xtol)."""
    sysd = signal.TransferFunction(num, den)

    def h(tt):
        _, yy = signal.impulse(sysd, T=[0.0, tt])
        return yy[-1]

    return brentq(h, t_guess - width, t_guess + width, xtol=1e-15 * max(1.0, t_guess) + 1e-18)


# ---------------------------------------------------------------------------------------- Example 1
G = (s + 4) / (s**2 + 3 * s + 2)
p1 = sorted(float(r) for r in sp.solve(sp.denom(G), s))
v.check("Ex 15-02.1a", p1[1])
v.check("Ex 15-02.1b", p1[0])
v.check("Ex 15-02.1c", float(sp.solve(sp.numer(G), s)[0]))
v.check("Ex 15-02.1d", float(G.subs(s, 0)))
# the ODE in steady state: 2y = 4u
v.assert_true("Ex 1: steady state of the ODE equals G(0)", abs(4 / 2 - float(G.subs(s, 0))) < 1e-15)

# ---------------------------------------------------------------------------------------- Example 2
R, L, K, J, B = 2.0, 1e-3, 0.05, 2e-5, 1e-5
A2 = sp.Matrix([[-R / L, -K / L], [K / J, -B / J]])
B2 = sp.Matrix([1 / L, 0])
G2 = sp.simplify((sp.Matrix([[0, 1]]) * (s * sp.eye(2) - A2).inv() * B2)[0])
n2, d2 = num_den(G2)
n2 = [c / d2[0] for c in n2]
d2 = [c / d2[0] for c in d2]
v.check("Ex 15-02.2d", n2[-1])
v.check("Ex 15-02.2e", d2[1])
v.check("Ex 15-02.2f", d2[2])
v.check("Ex 15-02.2a", n2[-1] / d2[-1])
ev2 = sorted(np.linalg.eigvals(np.array(A2, dtype=float)).real)
v.check("Ex 15-02.2b", ev2[1])
v.check("Ex 15-02.2c", ev2[0])
G2_formula = sp.lambdify(s, K / ((L * s + R) * (J * s + B) + K**2))
G2_ss = sp.lambdify(s, G2)
v.assert_true("Ex 2: 15-01 formula K/[(Ls+R)(Js+B)+K^2] equals C(sI-A)^-1 B at test frequencies",
              all(abs(G2_formula(z) - G2_ss(z)) < 1e-9 * abs(G2_ss(z)) for z in (0.3, 1j * 50, -10 + 400j, 1e4j)))
v.assert_true("Ex 2: 12 V gives 238.1 rad/s", abs(12 * n2[-1] / d2[-1] - 238.1) < 0.05)
v.assert_true("Ex 2: blocks.tf_from_ss reproduces the denominator",
              np.allclose(blocks.tf_from_ss(np.array(A2, dtype=float), [1 / L, 0], [0, 1]).den, d2, rtol=1e-12))

# ---------------------------------------------------------------------------------------- Example 3
r, e, u, y = sp.symbols("r e u y")
eqs = [sp.Eq(e, r - y), sp.Eq(u, 10 / (s + 1) * e), sp.Eq(y, (u - 2 * y) / s)]
T3 = solve_signals(eqs, [e, u, y], y) / r
T3 = sp.simplify(T3)
v.assert_true("Ex 3: T = 10/(s^2+3s+12)", sp.simplify(T3 - 10 / (s**2 + 3 * s + 12)) == 0, str(T3))
n3, d3 = num_den(T3)
wn3 = math.sqrt(d3[2] / d3[0])
z3 = d3[1] / d3[0] / (2 * wn3)
v.check("Ex 15-02.3a", wn3)
v.check("Ex 15-02.3b", z3)
v.check("Ex 15-02.3c", float(T3.subs(s, 0)))
ypk, tpk, _, _, _ = step_peak(n3, d3, 10)
yfin = float(T3.subs(s, 0))
v.check("Ex 15-02.3d", 100 * (ypk / yfin - 1))
v.check("Ex 15-02.3e", exact_peak_time(n3, d3, tpk, 0.05))
# without velocity feedback: y = u/s
T3b = sp.simplify(solve_signals([sp.Eq(e, r - y), sp.Eq(u, 10 / (s + 1) * e), sp.Eq(y, u / s)], [e, u, y], y) / r)
n3b, d3b = num_den(T3b)
wn3b = math.sqrt(d3b[2] / d3b[0])
v.check("Ex 15-02.3f", d3b[1] / d3b[0] / (2 * wn3b))
ypk_b, _, _, _, _ = step_peak(n3b, d3b, 15)
v.check("Ex 15-02.3g", 100 * (ypk_b / float(T3b.subs(s, 0)) - 1))

# ---------------------------------------------------------------------------------------- Example 4
d_ = sp.symbols("d")
for Kp, ids in ((9, "acegi"), (99, "bdfhj")):
    eqs = [sp.Eq(e, r - y), sp.Eq(u, Kp * e), sp.Eq(y, (u + d_) / (s + 1))]
    sol = sp.solve(eqs, [e, u, y], dict=True)[0]
    Ty = sp.simplify(sol[y].diff(r))
    Dy = sp.simplify(sol[y].diff(d_))
    Se = sp.simplify(sol[e].diff(r))
    v.check(f"Ex 15-02.4{ids[0]}", float(Ty.subs(s, 0)))
    v.check(f"Ex 15-02.4{ids[1]}", float(Se.subs(s, 0)))
    v.check(f"Ex 15-02.4{ids[2]}", float(Dy.subs(s, 0)))
    v.check(f"Ex 15-02.4{ids[3]}", float(sp.solve(sp.denom(sp.together(Ty)), s)[0]))
    # controller output at t = 0+: initial value theorem on U = K S R with R = 1/s
    v.check(f"Ex 15-02.4{ids[4]}", float(sp.limit(s * sol[u].diff(r) / s, s, sp.oo)))
    v.assert_true(f"Ex 4 (K={Kp}): S + T = 1", sp.simplify(Se + Ty - 1) == 0)

# ---------------------------------------------------------------------------------------- Example 5
vals = dict(G1=2, G2=5, G3=4, G4=1, G5=3, H1=0.5, H2=0.25, H3=0.1)


def ex5_edges(g):
    return [("R", "x1", 1), ("x1", "x2", g["G1"]), ("x2", "x1", -g["H1"]), ("x2", "x3", g["G2"]),
            ("x3", "x4", g["G3"]), ("x4", "x3", -g["H2"]), ("x4", "x5", g["G4"]), ("x5", "x2", -g["H3"]),
            ("x2", "x4", g["G5"])]


E5 = ex5_edges(vals)
T5, info5 = blocks.mason(E5, "R", "x5", detail=True)
direct5 = blocks.solve_graph(E5, "R", "x5")
v.check("Ex 15-02.5a", info5["delta"])
v.check("Ex 15-02.5b", direct5)
v.assert_true("Ex 5: Mason equals the direct linear solve", abs(T5 - direct5) < 1e-12)
loops5 = info5["loops"]
gsum = sum(gain for _, gain in loops5)
v.check("Ex 15-02.5c", (40 + 6) / (1 - gsum))
v.assert_true("Ex 5: forward-path gains are 40 and 6",
              sorted(round(gn, 12) for _, gn in info5["paths"]) == [6, 40])
nontouch = [(a, b) for i, (a, _) in enumerate(loops5) for (b, _) in loops5[i + 1:] if set(a).isdisjoint(b)]
v.check("Lab 15-02.f", len(loops5))
v.check("Lab 15-02.g", len(nontouch))
# symbolic Mason against the symbolic node-equation solve
gs = {k: sp.Symbol(k) for k in vals}
Ts = sp.simplify(blocks.mason(ex5_edges(gs), "R", "x5"))
X = sp.symbols("x1:6")
node_eqs = [sp.Eq(X[0], 1 - gs["H1"] * X[1]), sp.Eq(X[1], gs["G1"] * X[0] - gs["H3"] * X[4]),
            sp.Eq(X[2], gs["G2"] * X[1] - gs["H2"] * X[3]), sp.Eq(X[3], gs["G3"] * X[2] + gs["G5"] * X[1]),
            sp.Eq(X[4], gs["G4"] * X[3])]
Tsol = sp.solve(node_eqs, X, dict=True)[0][X[4]]
v.assert_true("Ex 5: symbolic Mason equals symbolic node solve", sp.simplify(Ts - Tsol) == 0)

# random graphs: Mason against the linear solve
rng = random.Random(15)
ok = True
for trial in range(60):
    n = rng.randint(4, 7)
    nodes = [f"n{i}" for i in range(n)]
    edges = [(nodes[i], nodes[i + 1], rng.uniform(0.2, 2.0)) for i in range(n - 1)]  # guarantees a path
    for _ in range(rng.randint(2, 7)):
        a, b = rng.sample(range(1, n), 2)
        edges.append((nodes[a], nodes[b], rng.uniform(-0.6, 0.6)))
    try:
        direct = blocks.solve_graph(edges, nodes[0], nodes[-1])
    except np.linalg.LinAlgError:
        continue
    ok &= abs(blocks.mason(edges, nodes[0], nodes[-1]) - direct) < 1e-9 * max(1.0, abs(direct))
v.assert_true("Mason's formula equals the linear solve on 60 random graphs", ok)

# ---------------------------------------------------------------------------------------- Example 6
Icp, Kv, N, Rf, Cf = 100e-6, 2 * math.pi * 100e6, 100, 5e3, 1e-9
# loop gain L = Kpd * Z(s) * Kv / (N s); closed loop from the raw equations
th_r, th_d, i_cp, vc, th_o = sp.symbols("th_r th_d i_cp vc th_o")
eqs6 = [sp.Eq(i_cp, Icp / (2 * sp.pi) * (th_r - th_d)), sp.Eq(vc, (Rf + 1 / (s * Cf)) * i_cp),
        sp.Eq(th_o, Kv / s * vc), sp.Eq(th_d, th_o / N)]
sol6 = sp.solve(eqs6, [th_d, i_cp, vc, th_o], dict=True)[0]
T6 = sp.simplify(sol6[th_d] / th_r)
n6, d6 = num_den(T6)
wn6 = math.sqrt(d6[2] / d6[0])
v.check("Ex 15-02.6a", wn6)
v.check("Ex 15-02.6b", wn6 / (2 * math.pi) / 1e3)
v.check("Ex 15-02.6c", d6[1] / d6[0] / (2 * wn6))
v.check("Ex 15-02.6d", float(sp.limit(sol6[th_o] / th_r, s, 0)))
eqs6_R0 = [sp.Eq(i_cp, Icp / (2 * sp.pi) * (th_r - th_d)), sp.Eq(vc, (1 / (s * Cf)) * i_cp),
           sp.Eq(th_o, Kv / s * vc), sp.Eq(th_d, th_o / N)]
T6_R0 = sp.simplify(sp.solve(eqs6_R0, [th_d, i_cp, vc, th_o], dict=True)[0][th_d] / th_r)
poles_R0 = [complex(pp_) for pp_ in sp.solve(sp.denom(sp.together(T6_R0)), s)]
v.assert_true("Ex 6: R = 0 in the derived loop puts the closed-loop poles on the imaginary axis",
              len(poles_R0) == 2 and all(abs(pp_.real) < 1e-6 and abs(abs(pp_.imag) - wn6) < 1e-3 * wn6 for pp_ in poles_R0))

# ---------------------------------------------------------------------------------------- Problem 1
G = 5 / (s**2 + 7 * s + 10)
pp = sorted(float(x) for x in sp.solve(sp.denom(G), s))
v.check("15-02.1a", pp[1])
v.check("15-02.1b", pp[0])
v.check("15-02.1c", float(G.subs(s, 0)))
v.check("15-02.1d", sp.degree(sp.denom(G), s) - sp.degree(sp.numer(G), s))

# ---------------------------------------------------------------------------------------- Problem 2
Ga, Gb = 1 / (s + 1), 2 / (s + 3)
v.check("15-02.2a", float((Ga * Gb).subs(s, 0)))
Gp = sp.together(Ga + Gb)
v.check("15-02.2b", float(Gp.subs(s, 0)))
v.check("15-02.2c", float(sp.solve(sp.numer(Gp), s)[0]))
v.assert_true("P2: the two branches cancel at the zero",
              abs(float(Ga.subs(s, sp.Rational(-5, 3)) + Gb.subs(s, sp.Rational(-5, 3)))) < 1e-15)

# ---------------------------------------------------------------------------------------- Problem 3
x_ = sp.symbols("x_")
neg = sp.solve(sp.Eq(x_, 4 * (1 - 0.2 * x_)), x_)[0]
pos = sp.solve(sp.Eq(x_, 4 * (1 + 0.2 * x_)), x_)[0]
v.check("15-02.3a", float(neg))
v.check("15-02.3b", float(pos))
Hs = sp.symbols("Hs")
v.check("15-02.3c", float(sp.solve(1 - 4 * Hs, Hs)[0]))

# ---------------------------------------------------------------------------------------- Problem 4
T41 = 1e5 / (1 + 1e5 * 0.01)
T42 = 8e4 / (1 + 8e4 * 0.01)
v.check("15-02.4a", T41)
v.check("15-02.4b", T42)
v.check("15-02.4c", 100 * (T42 / T41 - 1))
v.check("15-02.4d", 100 * (-0.2) / (1 + 1e5 * 0.01))

# ---------------------------------------------------------------------------------------- Problem 5
Rr, Lr, Cr = 10.0, 1e-3, 1e-6
A5 = sp.Matrix([[-Rr / Lr, -1 / Lr], [1 / Cr, 0]])
B5 = sp.Matrix([1 / Lr, 0])
res = (s * sp.eye(2) - A5).inv() * B5
Gvc = sp.simplify(res[1])
Gi = sp.simplify(res[0])
ev5 = np.linalg.eigvals(np.array(A5, dtype=float))
evu = ev5[np.argmax(ev5.imag)]
v.check("15-02.5a", evu.real)
v.check("15-02.5b", evu.imag)
v.check("15-02.5c", abs(evu))
v.check("15-02.5d", -evu.real / abs(evu))
v.check("15-02.5e", float(Gvc.subs(s, 0)))
v.check("15-02.5f", float(Gi.subs(s, 0)))
v.assert_true("P5: both outputs share the denominator s^2 + 1e4 s + 1e9",
              sp.simplify(sp.denom(sp.together(Gvc)) / sp.denom(sp.together(Gi))).is_number)
v.assert_true("P5: I/Vs = 1000 s/(s^2+1e4 s+1e9)", sp.simplify(Gi - 1000 * s / (s**2 + 1e4 * s + 1e9)) == 0)

# ---------------------------------------------------------------------------------------- Problem 6
G1_, G2_, G3_, H1_, H2_ = 5, 1 / (s + 1), 1 / s, sp.Rational(2, 5), 2
r_, e1, e2, a_, y_ = sp.symbols("r_ e1 e2 a_ y_")
eqs6p = [sp.Eq(e1, r_ - H1_ * a_), sp.Eq(e2, G1_ * e1 - H2_ * y_), sp.Eq(a_, G2_ * e2), sp.Eq(y_, G3_ * a_)]
T6p = sp.simplify(sp.solve(eqs6p, [e1, e2, a_, y_], dict=True)[0][y_] / r_)
v.assert_true("P6: Y/R = 5/((s+1)(s+2))", sp.simplify(T6p - 5 / ((s + 1) * (s + 2))) == 0, str(T6p))
pp6 = sorted(float(x) for x in sp.solve(sp.denom(sp.together(T6p)), s))
v.check("15-02.6a", pp6[1])
v.check("15-02.6b", pp6[0])
v.check("15-02.6c", float(T6p.subs(s, 0)))
# Mason on the same graph, symbolically
E6 = [("R", "e1", 1), ("e1", "e2", G1_), ("e2", "a", G2_), ("a", "Y", G3_), ("a", "e1", -H1_), ("Y", "e2", -H2_)]
v.assert_true("P6: Mason equals the node solve", sp.simplify(blocks.mason(E6, "R", "Y") - T6p) == 0)

# ---------------------------------------------------------------------------------------- Problem 7
L7 = 8 / (s * (s + 2))
T7 = sp.simplify(L7 / (1 + L7))
n7, d7 = num_den(T7)
wn7 = math.sqrt(d7[2])
v.check("15-02.7a", wn7)
v.check("15-02.7b", d7[1] / (2 * wn7))
Lf = sp.lambdify(s, L7)
mags = {}
for w, ids in ((0.5, "cdg"), (10.0, "efh")):
    Lj = complex(Lf(1j * w))
    S_, T_ = 1 / (1 + Lj), Lj / (1 + Lj)
    v.check(f"15-02.7{ids[0]}", abs(S_))
    v.check(f"15-02.7{ids[1]}", abs(T_))
    v.check(f"15-02.7{ids[2]}", abs(S_) + abs(T_))
    v.assert_true(f"P7: S + T = 1 as complex numbers at {w} rad/s", abs(S_ + T_ - 1) < 1e-14)

# ---------------------------------------------------------------------------------------- Problem 8
Rm, Km, Jm, Kp8 = 1.0, 0.02, 1e-5, 0.2
taum = Rm * Jm / Km**2
TL = 0.01


def motor_rhs(_t, x, wref, tl, kp):
    w = x[0]
    vin = kp * (wref - w)
    i = (vin - Km * w) / Rm
    return [(Km * i - tl) / Jm]


# closed loop with only a load torque (wref = 0) from the original torque balance, integrated to steady state
sol = solve_ivp(motor_rhs, (0, 0.2), [0.0], args=(0.0, TL, Kp8), rtol=1e-11, atol=1e-13, dense_output=True)
droop_cl = -sol.y[0, -1]
sol_ol = solve_ivp(motor_rhs, (0, 1.0), [0.0], args=(0.0, TL, 0.0), rtol=1e-11, atol=1e-13)
droop_ol = -sol_ol.y[0, -1]
v.check("15-02.8a", Kp8 / Km)
sol_tr = solve_ivp(motor_rhs, (0, 0.2), [0.0], args=(1.0, 0.0, Kp8), rtol=1e-11, atol=1e-13)
v.check("15-02.8b", sol_tr.y[0, -1])
v.check("15-02.8c", droop_ol)
v.check("15-02.8d", droop_cl)
# time constant: the time to reach 1 - 1/e of the final droop
tau_cl = brentq(lambda tt: -sol.sol(tt)[0] - (1 - math.exp(-1)) * droop_cl, 1e-5, 0.05, xtol=1e-14)
v.check("15-02.8e", tau_cl * 1e3)
v.assert_true("P8: tau_cl = tau_m/(1 + L0)", abs(tau_cl - taum / (1 + Kp8 / Km)) < 1e-8)

# ---------------------------------------------------------------------------------------- Problem 9
E9 = [("R", "x1", 1), ("x1", "x2", 4), ("x2", "x1", -0.5), ("x2", "Y", 1),
      ("R", "x3", 1), ("x3", "x4", 10), ("x4", "x3", -0.1), ("x4", "Y", 2)]
T9, info9 = blocks.mason(E9, "R", "Y", detail=True)
paths9 = {round(gn, 9): dk for (_, gn), dk in zip(info9["paths"], info9["cofactors"])}
v.check("15-02.9a", info9["delta"])
v.check("15-02.9b", paths9[4])
v.check("15-02.9c", paths9[20])
v.check("15-02.9d", blocks.solve_graph(E9, "R", "Y"))
v.assert_true("P9: Mason equals the parallel-blocks result", abs(T9 - (4 / 3 + 10)) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 10
E10 = [("R", "e", 2), ("e", "x", 1 / (s + 1)), ("x", "e", -3), ("x", "Y", 1), ("R", "Y", sp.Rational(1, 2))]
T10 = sp.factor(sp.simplify(blocks.mason(E10, "R", "Y")))
e10, x10, y10 = sp.symbols("e10 x10 y10")
T10b = sp.solve([sp.Eq(e10, 2 - 3 * x10), sp.Eq(x10, e10 / (s + 1)), sp.Eq(y10, x10 + sp.Rational(1, 2))],
                [e10, x10, y10], dict=True)[0][y10]
v.assert_true("P10: Mason equals the node solve", sp.simplify(T10 - T10b) == 0, str(T10))
v.check("15-02.10a", float(sp.solve(sp.denom(sp.together(T10)), s)[0]))
v.check("15-02.10b", float(sp.solve(sp.numer(sp.together(T10)), s)[0]))
v.check("15-02.10c", float(T10.subs(s, 0)))
v.check("15-02.10d", float(sp.limit(T10, s, sp.oo)))

# ---------------------------------------------------------------------------------------- Problem 11
P11 = 1 / (s - 1)
C11 = (s - 1) / (s + 2)
dd, ee, uu, yy = sp.symbols("dd ee uu yy")
sol11 = sp.solve([sp.Eq(ee, r - yy), sp.Eq(uu, C11 * ee), sp.Eq(yy, P11 * (uu + dd))], [ee, uu, yy], dict=True)[0]
T11 = sp.simplify(sol11[yy].diff(r))
YD = sp.factor(sp.simplify(sol11[yy].diff(dd)))
v.check("15-02.11a", float(sp.solve(sp.denom(sp.together(T11)), s)[0]))
v.assert_true("P11: Y/D keeps the pole at +1", sp.simplify(sp.denom(sp.together(YD)).subs(s, 1)) == 0, str(YD))
# time response by integrating a state-space realization of Y/D (not by partial fractions)
nYD, dYD = num_den(YD)
tt11 = np.linspace(0, 5, 50001)
_, y11 = signal.step(signal.TransferFunction(nYD, dYD), T=tt11)
v.check("15-02.11b", y11[-1])
yt = sp.inverse_laplace_transform(YD / s, s, t)
v.assert_true("P11: closed form 3/4 e^t - 2/3 - e^(-3t)/12",
              abs(float(yt.subs(t, 5)) - (0.75 * math.exp(5) - 2 / 3 - math.exp(-15) / 12)) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 12
A0, wa, gm, RL, CL, beta, Vref = 1000.0, 2 * math.pi * 1e4, 0.5, 10.0, 1e-6, 0.5, 1.2
vo, il, vg = sp.symbols("vo il vg")
ZL = RL / (1 + s * RL * CL)
eq12 = [sp.Eq(vg, A0 / (1 + s / wa) * (sp.Symbol("vr") - beta * vo)), sp.Eq(vo, ZL * (gm * vg - il))]
sol12 = sp.solve(eq12, [vg, vo], dict=True)[0]
H_ref = sp.simplify(sol12[vo].diff(sp.Symbol("vr")))
Z_out = sp.simplify(-sol12[vo].diff(il))
L0 = A0 * gm * RL * beta
v.check("15-02.12a", L0)
v.check("15-02.12b", Vref * float(H_ref.subs(s, 0)))
v.check("15-02.12c", 100 * (1 - beta * float(H_ref.subs(s, 0))))
v.check("15-02.12d", 0.1 * RL)
v.check("15-02.12e", float(Z_out.subs(s, 0)) * 1e3)
v.check("15-02.12f", 0.1 * float(Z_out.subs(s, 0)) * 1e3)
n12, d12 = num_den(H_ref)
poles12 = np.roots(d12)
wn12 = abs(poles12[0])
z12 = -poles12[0].real / wn12
v.check("15-02.12g", wn12)
v.check("15-02.12h", wn12 / (2 * math.pi) / 1e3)
v.check("15-02.12i", z12)
pk12, _, fin12, _, _ = step_peak(n12, d12, 2e-4, n=800001)
v.check("15-02.12j", 100 * (pk12 / float(H_ref.subs(s, 0)) - 1))  # simulated peak, sampled every 0.25 ns

# ---------------------------------------------------------------------------------------- Problem 13
Icp, Kv, N, C13 = 200e-6, 2 * math.pi * 50e6, 50, 4e-9
wn13 = math.sqrt(Icp * Kv / (2 * math.pi * N * C13))
R13 = brentq(lambda Rx: Rx * C13 * wn13 / 2 - 1 / math.sqrt(2), 1, 1e6, xtol=1e-12)
v.check("15-02.13a", wn13)
v.check("15-02.13b", wn13 / (2 * math.pi) / 1e3)
v.check("15-02.13c", R13)
v.check("15-02.13d", -1 / (R13 * C13))
n13 = [wn13**2 * R13 * C13, wn13**2]
d13 = [1, wn13**2 * R13 * C13, wn13**2]
pk13, tp13, _, _, _ = step_peak(n13, d13, 1e-4)
v.check("15-02.13e", 100 * (pk13 - 1))
v.check("15-02.13f", exact_peak_time(n13, d13, tp13, 1e-6) * 1e6)
v.assert_true("P13: no-zero second order at zeta 0.707 overshoots 4.3%",
              abs(100 * math.exp(-math.pi / math.sqrt(2) / math.sqrt(0.5)) - 4.3) < 0.05)

# ---------------------------------------------------------------------------------------- Problem 14
KI = sp.symbols("KI", positive=True)
T14 = sp.simplify((2 * KI / (s * (s + 4))) / (1 + 2 * KI / (s * (s + 4))))
den14 = sp.Poly(sp.denom(sp.together(T14)), s).all_coeffs()
KI_val = sp.solve(sp.Eq(den14[1] / (2 * sp.sqrt(den14[2] / den14[0])), 1 / sp.sqrt(2)), KI)[0]
v.check("15-02.14a", float(sp.sqrt(den14[2].subs(KI, KI_val))))
v.check("15-02.14b", float(KI_val))
v.check("15-02.14c", float(1 - T14.subs(KI, KI_val).subs(s, 0)))

# ---------------------------------------------------------------------------------------- Lab
GI = blocks.tf_from_ss(np.array(A2, dtype=float), [1 / L, 0], [1, 0])
v.check("Lab 15-02.a", GI.zeros()[0].real)
v.check("Lab 15-02.b", GI.dcgain() * 1e3)
v.assert_true("Lab: I/V = (Js+B)/[(Ls+R)(Js+B)+K^2]",
              abs(GI.dcgain() - B / (R * B + K**2)) < 1e-15)
_, _, _, tt3, y3 = step_peak(n3, d3, 15, n=150001)
v.check("Lab 15-02.c", y3.max())
outside = np.flatnonzero(np.abs(y3 - yfin) > 0.02 * yfin)
v.check("Lab 15-02.d", tt3[outside[-1] + 1])
v.check("Lab 15-02.e", float(T3b.subs(s, 0)))
for Rx, kz, ko in ((2.5e3, "h", "j"), (5e3, None, "k"), (10e3, "i", "l")):
    wn = math.sqrt(1e11)
    if kz:
        v.check(f"Lab 15-02.{kz}", Rx * 1e-9 * wn / 2)
    pk, _, _, _, _ = step_peak([wn**2 * Rx * 1e-9, wn**2], [1, wn**2 * Rx * 1e-9, wn**2], 1e-4)
    v.check(f"Lab 15-02.{ko}", 100 * (pk - 1))

# ---------------------------------------------------------------------------------------- prose numbers (audit)
wa_, wL_ = 2 * math.pi * 1e4, 1e5
pl = np.roots([1, wa_ + wL_, 2501 * wa_ * wL_])
c_ = pl[np.argmax(pl.imag)]
v.assert_true("Sol 11(c): LDO poles -8.14e4 +- j3.963e6", round(c_.real / 1e4, 2) == -8.14 and round(c_.imag / 1e6, 3) == 3.963)

# ---------------------------------------------------------------------------------------- Problem 15 (op-amp impedances)
R1, R2, Cop = 1e4, 1e5, 1e-9
Zf_a = R2 / (1 + s * R2 * Cop)
Ha = sp.simplify(-Zf_a / R1)
v.check("15-02.15a", float(Ha.subs(s, 0)))
pa = [complex(x) for x in sp.solve(sp.denom(sp.together(Ha)), s)][0]
v.check("15-02.15b", -pa.real)
v.check("15-02.15c", -pa.real / (2 * math.pi) / 1e3)
Hb = sp.simplify(-(R2 + 1 / (s * Cop)) / R1)
Ki_b = float(sp.limit(-s * Hb, s, 0))
v.check("15-02.15d", Ki_b)
zb = [complex(x) for x in sp.solve(sp.numer(sp.together(Hb)), s)][0]
v.check("15-02.15e", zb.real)

sys.exit(v.finish())
