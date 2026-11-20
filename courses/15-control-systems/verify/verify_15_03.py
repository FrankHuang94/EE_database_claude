#!/usr/bin/env python3
"""Verify chapter 15-03 (time response and specifications): examples, problems and lab answers.

Two independent routes are used wherever possible:
- exact step responses from labs/15-03-lab/specs.py (matrix exponential of an augmented state matrix, crossings
  and peaks refined by brentq on the exact response);
- closed-form formulas (first-order logarithms, the second-order overshoot, peak-time and envelope formulas, the
  doublet residue), each checked against the exact responses with assert_true;
- for the RLC lab circuit and for Example 15-03.2, an independent solve_ivp integration of the state equations.
The ngspice netlist labs/15-03-lab/rlc_step.cir confirms the lab's RLC values (tools/run_spice.py).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "15-03-lab"))
from eeverify import Verifier  # noqa: E402
from specs import step_specs, step_at, second_order, zeta_from_overshoot  # noqa: E402

CH = ROOT / "chapters" / "15-03-time-response.md"
v = Verifier.from_files("15-03", CH, ROOT / "solutions" / "15-03-solutions.md", ROOT / "labs" / "15-03-lab" / "README.md")
s = sp.symbols("s")


def std(z, wn=1.0):
    return [wn**2], [1, 2 * z * wn, wn**2]


def ivp_specs(A, B, C, t_end, final, band=0.02):
    """Rise, peak, peak time and settling time from a solve_ivp integration (independent of specs.py)."""
    A, B, C = map(np.asarray, (A, B, C))
    sol = solve_ivp(lambda t, x: A @ x + B, (0, t_end), np.zeros(len(B)), dense_output=True, rtol=1e-11, atol=1e-13)
    y = lambda t: float(C @ sol.sol(t))  # noqa: E731
    tt = np.linspace(0, t_end, 200001)
    yy = np.array([C @ col for col in sol.sol(tt).T])
    k10 = np.flatnonzero(yy >= 0.1 * final)[0]
    k90 = np.flatnonzero(yy >= 0.9 * final)[0]
    t10 = brentq(lambda t: y(t) - 0.1 * final, tt[k10 - 1], tt[k10], xtol=1e-14)
    t90 = brentq(lambda t: y(t) - 0.9 * final, tt[k90 - 1], tt[k90], xtol=1e-14)
    kp = int(np.argmax(yy))
    dy = lambda t: float(C @ (A @ sol.sol(t) + B))  # noqa: E731
    tp = brentq(dy, tt[kp - 1], tt[kp + 1], xtol=1e-14)
    out = np.flatnonzero(np.abs(yy - final) > band * final)[-1]
    lev = final * (1 + band) if yy[out] > final else final * (1 - band)
    ts = brentq(lambda t: y(t) - lev, tt[out], tt[out + 1], xtol=1e-14)
    return t90 - t10, y(tp), tp, ts


# ---------------------------------------------------------------------------------------- text table
for z, (ko, kr, kt) in ((0.3, ("a", "e", "j")), (0.5, ("b", "f", "k")), (1 / math.sqrt(2), ("c", "g", "l")),
                        (0.8, ("d", "h", "m"))):
    r = step_specs(*std(z), 60)
    v.check(f"Txt 15-03.{ko}", 100 * r["overshoot"])
    v.check(f"Txt 15-03.{kr}", r["rise"])
    v.check(f"Txt 15-03.{kt}", r["settle"])
    v.assert_true(f"overshoot formula at zeta={z:.3f}", abs(second_order(z, 1)["overshoot"] - r["overshoot"]) < 1e-9)
r1 = step_specs(*std(1.0), 60)
v.check("Txt 15-03.i", r1["rise"])
v.check("Txt 15-03.n", r1["settle"])
# critically damped: y = 1 - (1 + t) e^-t, so the 10-90 rise time solves that closed form
y_crit = lambda t: 1 - (1 + t) * math.exp(-t)  # noqa: E731
tr_crit = brentq(lambda t: y_crit(t) - 0.9, 0.1, 10) - brentq(lambda t: y_crit(t) - 0.1, 0.01, 5)
v.assert_true("critically damped rise time from the closed form", abs(tr_crit - r1["rise"]) < 1e-9)
v.check("Txt 15-03.o", 13 * math.log(2))
v.check("Txt 15-03.p", 17 * math.log(2))
v.assert_true("zeta 0.8 settles sooner than zeta 0.707 and zeta 1",
              step_specs(*std(0.8), 60)["settle"] < min(step_specs(*std(0.7071), 60)["settle"], r1["settle"]))

# ---------------------------------------------------------------------------------------- Example 1
tau = 1e-3
r = step_specs([1], [tau, 1], 0.02)
v.check("Ex 15-03.1a", r["rise"] * 1e3)
v.check("Ex 15-03.1b", r["settle"] * 1e3)
v.check("Ex 15-03.1c", step_specs([1], [tau, 1], 0.02, band=1e-3)["settle"] * 1e3)
fB = 1 / (2 * math.pi * tau)
v.check("Ex 15-03.1d", fB)
v.check("Ex 15-03.1e", r["rise"] * fB)
v.assert_true("first order: tr = tau ln 9", abs(r["rise"] - tau * math.log(9)) < 1e-12)

# ---------------------------------------------------------------------------------------- Example 2
num2, den2 = [10], [1, 3, 12]
p2 = np.roots(den2)
sig2, wd2 = -p2[0].real, abs(p2[0].imag)
v.check("Ex 15-03.2a", sig2)
v.check("Ex 15-03.2b", wd2)
r = step_specs(num2, den2, 10)
v.check("Ex 15-03.2c", r["tpeak"])
v.check("Ex 15-03.2d", 100 * r["overshoot"])
v.check("Ex 15-03.2e", 4 / sig2)
z2 = sig2 / math.sqrt(12)
v.check("Ex 15-03.2f", math.log(1 / (0.02 * math.sqrt(1 - z2**2))) / sig2)
v.check("Ex 15-03.2g", r["rise"])
v.check("Ex 15-03.2h", r["settle"])
tr_i, pk_i, tp_i, ts_i = ivp_specs([[0, 1], [-12, -3]], [0, 1], [10, 0], 10, 10 / 12)
v.assert_true("Ex 2: solve_ivp agrees with specs.py",
              max(abs(tr_i - r["rise"]), abs(tp_i - r["tpeak"]), abs(ts_i - r["settle"])) < 1e-7)

# ---------------------------------------------------------------------------------------- Example 3
p = 25.0
v.check("Ex 15-03.3a", 4 / (p / 2))
zmin = zeta_from_overshoot(0.10)
v.check("Ex 15-03.3b", zmin)
Kmax = (p / 2 / zmin) ** 2
v.check("Ex 15-03.3c", Kmax)
v.assert_true("Ex 3: overshoot at Kmax is 10%", abs(step_specs([Kmax], [1, p, Kmax], 2)["overshoot"] - 0.10) < 1e-9)
K3 = (p / 2 / 0.6) ** 2
v.check("Ex 15-03.3d", K3)
r = step_specs([K3], [1, p, K3], 2)
v.check("Ex 15-03.3e", 100 * r["overshoot"])
v.check("Ex 15-03.3f", r["tpeak"])
v.check("Ex 15-03.3g", r["rise"])
v.check("Ex 15-03.3h", r["settle"])
tr_3, pk_3, tp_3, ts_3 = ivp_specs([[0, 1], [-K3, -25]], [0, 1], [K3, 0], 1.0, 1.0)
v.assert_true("Ex 3: solve_ivp cross-check of rise, peak time and settling",
              abs(tr_3 - r["rise"]) < 1e-7 and abs(tp_3 - r["tpeak"]) < 1e-7 and abs(ts_3 - r["settle"]) < 1e-7)

# ---------------------------------------------------------------------------------------- Example 4
ids4 = {None: ("a", "e", "i"), 10: ("b", "f", "j"), 3: ("c", "g", "k"), 1: ("d", "h", "l")}
for pp, (ko, kr, ks) in ids4.items():
    num, den = ([1], [1, 1, 1]) if pp is None else ([pp], np.polymul([1, 1, 1], [1, pp]))
    r = step_specs(num, den, 40)
    v.check(f"Ex 15-03.4{ko}", 100 * r["overshoot"])
    v.check(f"Ex 15-03.4{kr}", r["rise"])
    v.check(f"Ex 15-03.4{ks}", r["settle"])

# ---------------------------------------------------------------------------------------- Example 5
r = step_specs([1 / 2, 1], [1, 1, 1], 40)
v.check("Ex 15-03.5a", 100 * r["overshoot"])
v.check("Ex 15-03.5b", r["rise"])
r = step_specs([1 / 0.5, 1], [1, 1, 1], 40)
v.check("Ex 15-03.5c", 100 * r["overshoot"])
v.check("Ex 15-03.5d", r["rise"])
r = step_specs([-1 / 2, 1], [1, 1, 1], 40)
v.check("Ex 15-03.5e", 100 * r["undershoot"])
v.check("Ex 15-03.5f", r["tmin"])
v.check("Ex 15-03.5g", 100 * r["overshoot"])
v.check("Ex 15-03.5h", float(sp.limit(s * (1 - s / 2) / (s**2 + s + 1), s, sp.oo)))
# y_z = y + ydot/z: check at a few times against the exact zero response
ok = True
for tt in (0.3, 1.0, 2.5, 5.0):
    h = 1 / math.sqrt(0.75) * math.exp(-0.5 * tt) * math.sin(math.sqrt(0.75) * tt)
    ok &= abs(step_at([0.5, 1], [1, 1, 1], tt) - (step_at([1], [1, 1, 1], tt) + h / 2)) < 1e-10
v.assert_true("Ex 5: a zero adds ydot/z (closed-form impulse response)", ok)

# ---------------------------------------------------------------------------------------- Example 6
wc, pd, zd = 2 * math.pi * 100e6, 2 * math.pi * 1e6, 2 * math.pi * 1.05e6
v.check("Ex 15-03.6a", step_specs([wc], [1, wc], 1e-7, band=1e-3)["settle"] * 1e9)
num6 = np.polymul([wc], [1, zd]) * pd / zd
den6 = np.polymul([1, wc], [1, pd])
# residue of T(s)/s at s = -p, by sympy
res = sp.residue(sp.Rational(1) * wc * (s + zd) * pd / zd / ((s + wc) * (s + pd) * s), s, -pd)
v.check("Ex 15-03.6b", -100 * float(res))
v.check("Ex 15-03.6c", 1 / pd * 1e9)
r6 = step_specs(num6, den6, 2e-6, band=1e-3, n=400001)
v.check("Ex 15-03.6d", r6["settle"] * 1e9)
v.assert_true("Ex 6: tail formula ln(A/0.001)/p matches the exact settling time",
              abs(math.log(-float(res) / 1e-3) / pd - r6["settle"]) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 1
tau = 4e-3
v.check("15-03.1a", 5.0)
v.check("15-03.1b", brentq(lambda t: 5 * (1 - math.exp(-t / tau)) - 5 * (1 - math.exp(-1)), 1e-4, 1e-2) * 1e3)
v.check("15-03.1c", -1 / tau)
r = step_specs([5], [tau, 1], 0.1)
v.check("15-03.1d", r["rise"] * 1e3)
v.check("15-03.1e", r["settle"] * 1e3)
v.check("15-03.1f", 1 / (2 * math.pi * tau))

# ---------------------------------------------------------------------------------------- Problem 2
z = zeta_from_overshoot(0.25)
wd = math.pi / 2e-3
wn = wd / math.sqrt(1 - z**2)
v.check("15-03.2a", z)
v.check("15-03.2b", wd)
v.check("15-03.2c", wn)
v.check("15-03.2d", z * wn)
v.check("15-03.2e", 4 / (z * wn) * 1e3)
r = step_specs([wn**2], [1, 2 * z * wn, wn**2], 0.03)
v.assert_true("P2: the model reproduces 25% at 2 ms", abs(r["overshoot"] - 0.25) < 1e-9 and abs(r["tpeak"] - 2e-3) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 3
for (b, c), (kw, kz) in (((4, 20), "ab"), ((6, 9), "cd"), ((5, 4), "ef"), ((0, 16), "gh"), ((-2, 5), "ij")):
    wn = math.sqrt(c)
    v.check(f"15-03.3{kw}", wn)
    v.check(f"15-03.3{kz}", b / (2 * wn))
v.assert_true("P3(e) has right-half-plane poles", all(np.roots([1, -2, 5]).real > 0))

# ---------------------------------------------------------------------------------------- Problem 4
r = step_specs(*std(0.3, 10), 5)
so = second_order(0.3, 10)
v.check("15-03.4a", 100 * r["overshoot"])
v.check("15-03.4b", r["tpeak"])
v.check("15-03.4c", so["settle_4"])
v.check("15-03.4d", so["settle_envelope"])
v.check("15-03.4e", r["settle"])
v.check("15-03.4f", so["wd"])
# the derived closed form against the exact response
t_ = sp.symbols("t", positive=True)
sig, wdd = 3, sp.sqrt(91)
y_cf = 1 - sp.exp(-sig * t_) * (sp.cos(wdd * t_) + sig / wdd * sp.sin(wdd * t_))
v.assert_true("P4: derived y(t) matches the exact response",
              all(abs(float(y_cf.subs(t_, tt)) - step_at(*std(0.3, 10), tt)) < 1e-10 for tt in (0.05, 0.2, 0.6, 1.5)))

# ---------------------------------------------------------------------------------------- Problem 5
zmin5 = zeta_from_overshoot(0.05)
v.check("15-03.5a", zmin5)
v.check("15-03.5b", 4 / 2)
v.check("15-03.5c", 1.8 / 0.6)
results = {}
for name, pole in (("A", -2 + 2j), ("B", -3 + 2j), ("C", -1 + 1j), ("D", -4 + 5j), ("E", -4 + 3j)):
    wn, sg = abs(pole), -pole.real
    rules = (sg / wn >= zmin5) and (sg >= 2) and (wn >= 3)
    rr = step_specs([wn**2], [1, 2 * sg, wn**2], 20)
    exact = rr["overshoot"] <= 0.05 and rr["settle"] <= 2 and rr["rise"] <= 0.6
    results[name] = (rules, exact, rr)
v.assert_true("P5: rules pass exactly B and E", [k for k, x in results.items() if x[0]] == ["B", "E"])
v.assert_true("P5: exact responses pass only E", [k for k, x in results.items() if x[1]] == ["E"])
v.check("15-03.5d", results["B"][2]["rise"])
v.check("15-03.5h", 100 * results["B"][2]["overshoot"])
v.check("15-03.5i", results["B"][2]["settle"])
v.check("15-03.5e", 100 * results["E"][2]["overshoot"])
v.check("15-03.5f", results["E"][2]["settle"])
v.check("15-03.5g", results["E"][2]["rise"])

# ---------------------------------------------------------------------------------------- Problem 6
wn = 20 / 0.7
K6 = wn**2
r = step_specs([K6], [1, 40, K6], 2)
v.check("15-03.6a", wn)
v.check("15-03.6b", K6)
v.check("15-03.6c", 100 * r["overshoot"])
v.check("15-03.6d", r["tpeak"])
v.check("15-03.6e", 4 / 20)
v.check("15-03.6f", r["settle"])
v.check("15-03.6g", wn * math.sqrt(1 - 0.49))

# ---------------------------------------------------------------------------------------- Problem 7
for eps, (kt, kf) in ((1e-3, "ab"), (2.0**-17, "cd")):
    tmax = brentq(lambda tc: step_specs([1], [tc, 1], 20 * tc, band=eps)["settle"] - 10e-6, 1e-7, 5e-6, xtol=1e-16)
    v.check(f"15-03.7{kt}", tmax * 1e6)
    v.check(f"15-03.7{kf}", 1 / (2 * math.pi * tmax) / 1e3)

# ---------------------------------------------------------------------------------------- Problem 8
for z, (ko, kr, ks) in ((1.0, "abc"), (1 / math.sqrt(2), "def")):
    r = step_specs(*std(z, 100), 1)
    v.check(f"15-03.8{ko}", 100 * r["overshoot"])
    v.check(f"15-03.8{kr}", r["rise"] * 1e3)
    v.check(f"15-03.8{ks}", r["settle"] * 1e3)
v.check("15-03.8g", step_specs(*std(0.8, 100), 1)["settle"] * 1e3)

# ---------------------------------------------------------------------------------------- Problem 9
v.check("15-03.9a", 2 / (2 * math.sqrt(10)))
ra = step_specs([10], [1, 2, 10], 20)
re_ = step_specs([100], np.polymul([1, 10], [1, 2, 10]), 20)
v.check("15-03.9b", 100 * ra["overshoot"])
v.check("15-03.9c", 100 * re_["overshoot"])
v.check("15-03.9d", ra["tpeak"])
v.check("15-03.9e", re_["tpeak"])
v.check("15-03.9f", ra["settle"])
v.check("15-03.9g", re_["settle"])

# ---------------------------------------------------------------------------------------- Problem 10
base10 = step_specs([4], [1, 2, 4], 20)
v.check("15-03.10a", 100 * base10["overshoot"])
v.check("15-03.10e", base10["rise"])
r = step_specs([4 / 3, 4], [1, 2, 4], 20)
v.check("15-03.10b", 100 * r["overshoot"])
v.check("15-03.10c", r["rise"])
z25 = brentq(lambda zz: step_specs([4 / zz, 4], [1, 2, 4], 20)["overshoot"] - 0.25, 1.0, 10.0, xtol=1e-12)
v.check("15-03.10d", z25)
os_z = [step_specs([4 / zz, 4], [1, 2, 4], 20)["overshoot"] for zz in (1, 2, 3, 5, 10)]
v.assert_true("P10: overshoot falls as the zero moves left", all(a > b for a, b in zip(os_z, os_z[1:])))

# ---------------------------------------------------------------------------------------- Problem 11
for zz, (ks, ku, kt) in ((8, ("a", "c", "d")), (1, ("b", "e", "f"))):
    v.check(f"15-03.11{ks}", float(sp.limit(s * 4 * (1 - s / zz) / (s**2 + 2 * s + 4), s, sp.oo)))
    r = step_specs([-4 / zz, 4], [1, 2, 4], 20)
    v.check(f"15-03.11{ku}", 100 * r["undershoot"])
    v.check(f"15-03.11{kt}", r["tmin"])

# ---------------------------------------------------------------------------------------- Problem 12
SR, GBW, beta, Vs = 55e6, 16e6, 0.5, 10.0
tau12 = 1 / (2 * math.pi * beta * GBW)
v.check("15-03.12a", tau12 * 1e9)
v.check("15-03.12e", Vs / SR * 1e9)
v.check("15-03.12f", tau12 * math.log(1e4) * 1e9)
v.check("15-03.12b", (Vs / SR + tau12 * math.log(1e4)) * 1e9)
VL = SR * tau12
v.check("15-03.12c", VL)
v.check("15-03.12g", (Vs - VL) / SR * 1e9)
v.check("15-03.12h", tau12 * math.log(VL / (1e-4 * Vs)) * 1e9)
v.check("15-03.12d", ((Vs - VL) / SR + tau12 * math.log(VL / (1e-4 * Vs))) * 1e9)


# simulate the slew-limited single-pole model: dv/dt = clip((Vs - v)/tau, SR); its 0.01% settling time
def slew_settle():
    sol = solve_ivp(lambda t, x: [min((Vs - x[0]) / tau12, SR)], (0, 1e-6), [0.0], dense_output=True,
                    rtol=1e-12, atol=1e-15, max_step=1e-10)
    return brentq(lambda t: Vs - sol.sol(t)[0] - 1e-4 * Vs, 1e-7, 1e-6, xtol=1e-16)


v.assert_true("P12: refined estimate equals the simulated slew-limited model",
              abs(slew_settle() - ((Vs - VL) / SR + tau12 * math.log(VL / (1e-4 * Vs)))) < 1e-10)

# ---------------------------------------------------------------------------------------- Problem 13
wc, p13 = 2 * math.pi * 100e6, 2 * math.pi * 1e6


def settle13(delta):
    zz = p13 * (1 + delta)
    return step_specs(np.polymul([wc], [1, zz]) * p13 / zz, np.polymul([1, wc], [1, p13]), 3e-6,
                      band=1e-3, n=300001)["settle"]


for d, k in ((0.05, "a"), (0.01, "b"), (0.002, "c")):
    v.check(f"15-03.13{k}", settle13(d) * 1e9)


def tail(delta, t):
    return wc / (wc - p13) * delta / (1 + delta) * math.exp(-p13 * t)


dstar = brentq(lambda d: tail(d, 50e-9) - 1e-3, 1e-6, 0.1, xtol=1e-16)
v.check("15-03.13d", dstar)
v.check("15-03.13e", settle13(dstar * 0.999) * 1e9)
v.check("15-03.13f", settle13(dstar * 1.001) * 1e9)

# ---------------------------------------------------------------------------------------- Problem 14
z = zeta_from_overshoot(0.2)
wn = (math.pi / 0.5) / math.sqrt(1 - z**2)
v.check("15-03.14a", 2.0)
v.check("15-03.14b", z)
v.check("15-03.14c", wn)
v.check("15-03.14d", 2 * wn**2)
v.check("15-03.14e", 2 * z * wn)
v.check("15-03.14f", wn**2)
r = step_specs([2 * wn**2], [1, 2 * z * wn, wn**2], 5)
v.check("15-03.14g", r["peak"])
v.check("15-03.14h", r["tpeak"])

# ---------------------------------------------------------------------------------------- Lab (RLC)
R, L, C = 31.6228, 1e-3, 1e-6
A = [[-R / L, -1 / L], [1 / C, 0]]          # states i, v_C
tr_i, pk_i, tp_i, ts_i = ivp_specs(A, [1 / L, 0], [0, 1], 2e-3, 1.0)
v.check("Lab 15-03.a", tr_i * 1e6)
v.check("Lab 15-03.b", tp_i * 1e6)
v.check("Lab 15-03.c", 100 * (pk_i - 1))
v.check("Lab 15-03.d", ts_i * 1e6)
r = step_specs([1], [L * C, R * C, 1], 2e-3)
v.assert_true("Lab: specs.py agrees with solve_ivp on the RLC circuit",
              max(abs(r["rise"] - tr_i), abs(r["tpeak"] - tp_i), abs(r["settle"] - ts_i)) < 1e-9)

# ---------------------------------------------------------------------------------------- audit additions (Ex 3)
ts3 = lambda k: step_specs([k], [1, 25, k], 3, n=200001)["settle"]  # noqa: E731
k_th = brentq(lambda k: ts3(k) - 0.4, 160, 200, xtol=1e-6)
v.assert_true("Ex 3: exact settling exceeds 0.4 s below K = 173 (zeta 0.95)", round(k_th) == 173 and round(12.5 / math.sqrt(k_th), 2) == 0.95)
tvals = [ts3(k) for k in (156.25, 200, 250, 300, 434, 1000)]
v.assert_true("Ex 3: exact settling spans about 0.23 to 0.47 s", round(min(tvals), 2) == 0.23 and round(max(tvals), 2) == 0.47)

def _rule_dev(z):
    return 100 * (1.8 / step_specs([1], [1, 2 * z, 1], 40, n=400001)["rise"] - 1)


v.assert_true("3.3: rise rule 23% high at zeta 0.4, 15% low at 0.7, 19% high at 0.43",
              round(_rule_dev(0.4)) == 23 and round(_rule_dev(0.7)) == -15 and round(_rule_dev(0.43)) == 19)
v.assert_true("Common mistakes: rule 27% below exact at 0.8 (exact 37% longer); 30% below at 0.83 (44% longer)",
              round(_rule_dev(0.8)) == -27 and round(100 * (1 / (1 + _rule_dev(0.8) / 100) - 1)) == 37
              and round(_rule_dev(0.83)) == -30 and round(100 * (1 / (1 + _rule_dev(0.83) / 100) - 1)) == 44)

# ---------------------------------------------------------------------------------------- prose numbers (audit)
base = step_specs([1], [1, 1, 1], 40, n=400001)
p6 = step_specs([3], np.polymul([1, 3], [1, 1, 1]), 40, n=400001)
p2 = step_specs([1], np.polymul([1, 1], [1, 1, 1]), 40, n=400001)
v.assert_true("Ex 4: at 6 sigma +7% rise and about 1 point less overshoot; at 2 sigma +40% rise and overshoot halves",
              round(100 * (p6["rise"] / base["rise"] - 1)) == 7 and round(100 * (base["overshoot"] - p6["overshoot"])) == 1
              and round(100 * (p2["rise"] / base["rise"] - 1)) == 40 and 0.45 < p2["overshoot"] / base["overshoot"] < 0.55)
wn3 = 12.5 / 0.6
v.assert_true("Ex 3: wn = 20.83, wd = 16.67", round(wn3, 2) == 20.83 and round(wn3 * 0.8, 2) == 16.67)
wc6, pp6, zz6 = 2 * math.pi * 1e8, 2 * math.pi * 1e6, 2 * math.pi * 1.05e6
t6 = math.log(48.1) / pp6
w6 = np.logspace(4, 10, 200001)
Hdb = 20 * np.log10(np.abs((1 + 1j * w6 / zz6) / (1 + 1j * w6 / pp6)))
v.assert_true("Ex 6: 56 times longer; doublet changes |T| by 0.42 dB (< 0.5 dB)",
              round(t6 / (math.log(1000) / wc6)) == 56 and round(float(np.max(np.abs(Hdb))), 2) == 0.42)
v.assert_true("P5(b): D overshoot 8.1% at zeta 0.625", round(100 * math.exp(-math.pi * 0.625 / math.sqrt(1 - 0.625**2)), 1) == 8.1)
v.assert_true("P5(b): table zeta and wn", all(round(abs(complex(a_, b_)), 2) == wn_ and round(a_ / abs(complex(a_, b_)), 3) == z_
                                             for a_, b_, wn_, z_ in ((2, 2, 2.83, 0.707), (3, 2, 3.61, 0.832), (1, 1, 1.41, 0.707), (4, 5, 6.40, 0.625), (4, 3, 5, 0.8))))
v.assert_true("P13(b): e^{-pt} = 0.730 at 50 ns; 0.14%", round(math.exp(-pp6 * 50e-9), 3) == 0.730)

sg, wd_ = 0.5, math.sqrt(0.75)
y_b = lambda tt: 1 - math.exp(-sg * tt) * (math.cos(wd_ * tt) + sg / wd_ * math.sin(wd_ * tt))  # noqa: E731
yd_b = lambda tt: (1 / wd_) * math.exp(-sg * tt) * math.sin(wd_ * tt)  # noqa: E731
tp2 = (math.pi - math.atan(wd_ / (2 - sg))) / wd_
tp05 = (math.pi / 2) / wd_
tu = math.atan(wd_ / (2 + sg)) / wd_
v.assert_true("Ex 5 by hand: tp 3.023 s and 19.1%; 1.814 s and 69.9%; undershoot at 0.385 s (9.12%)",
              round(tp2, 3) == 3.023 and round(100 * (y_b(tp2) + yd_b(tp2) / 2 - 1), 1) == 19.1
              and round(tp05, 3) == 1.814 and round(100 * (y_b(tp05) + yd_b(tp05) / 0.5 - 1), 1) == 69.9
              and round(tu, 3) == 0.385 and round(-100 * (y_b(tu) - yd_b(tu) / 2), 2) == 9.12)

sys.exit(v.finish())
