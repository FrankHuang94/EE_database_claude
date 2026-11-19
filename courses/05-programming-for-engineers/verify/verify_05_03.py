#!/usr/bin/env python3
"""Verify chapter 05-03: run every code block and recompute every published number independently.

Code blocks in the chapter and solutions are executed and their outputs compared exactly. Answer-key
values are recomputed by different routes: closed forms where they exist, mpmath's high-precision
root-finder and integrator, hand-coded least squares (Gauss-Newton) instead of curve_fit, and
counting function calls in our own implementations.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-03-scipy-sympy-matplotlib.md"
SOL = C_DIR / "solutions" / "05-03-solutions.md"
LAB = C_DIR / "labs" / "05-03-lab" / "README.md"
v = Verifier.from_files("05-03", CH, SOL, LAB)
run_python_blocks(v, CH, "chapter")
run_python_blocks(v, SOL, "solutions")
mp.mp.dps = 30


def gauss_newton(model, jac, t, y, p, iters=60):
    """Least squares by Gauss-Newton; returns parameters and their standard errors."""
    p = np.array(p, float)
    for _ in range(iters):
        r = y - model(t, *p)
        J = jac(t, *p)
        p = p + np.linalg.lstsq(J, r, rcond=None)[0]
    r = y - model(t, *p)
    J = jac(t, *p)
    s2 = r @ r / (len(t) - len(p))
    return p, np.sqrt(np.diag(s2 * np.linalg.inv(J.T @ J))), r


charge = lambda t, vs, tau: vs * (1 - np.exp(-t / tau))                         # noqa: E731
charge_jac = lambda t, vs, tau: np.column_stack([1 - np.exp(-t / tau), -vs * t / tau**2 * np.exp(-t / tau)])  # noqa: E731
decay = lambda t, v0, tau: v0 * np.exp(-t / tau)                                # noqa: E731
decay_jac = lambda t, v0, tau: np.column_stack([np.exp(-t / tau), v0 * t / tau**2 * np.exp(-t / tau)])       # noqa: E731
diode = lambda vs, r: float(mp.findroot(lambda x: (vs - x) / r - mp.mpf("1e-14") * (mp.e ** (x / mp.mpf("0.025852")) - 1), 0.7))  # noqa: E731

# ---------------------------------------------------------------- theory and examples
v.check("T 05-03.a", float(mp.findroot(lambda x: x**3 - 2 * x - 5, 2)))
temp = lambda r: 1 / (1 / 298.15 + math.log(r / 10e3) / 3950) - 273.15          # noqa: E731
table_t = [0.0, 25.0, 50.0, 75.0, 100.0]
table_r = [10e3 * math.exp(3950 * (1 / (t + 273.15) - 1 / 298.15)) for t in table_t]
v.check("T 05-03.b", temp(6000))
k = next(i for i in range(4) if table_r[i] >= 6000 >= table_r[i + 1])
lin = lambda xa, xb, ya, yb, x: ya + (yb - ya) * (x - xa) / (xb - xa)            # noqa: E731
v.check("T 05-03.c", lin(table_r[k], table_r[k + 1], table_t[k], table_t[k + 1], 6000))
v.check("T 05-03.d", lin(math.log(table_r[k]), math.log(table_r[k + 1]), table_t[k], table_t[k + 1], math.log(6000)))
from scipy.interpolate import CubicSpline  # noqa: E402  (natural-vs-not-a-knot check below)
spline = CubicSpline(np.log(table_r[::-1]), table_t[::-1])
v.check("T 05-03.e", float(spline(math.log(6000))))
v.assert_true("spline agrees with the exact curve to 0.01 C", abs(float(spline(math.log(6000))) - temp(6000)) < 0.01)
vd = diode(5.0, 1e3)
v.check("Ex 05-03.1a", vd)
v.check("Ex 05-03.1b", (5.0 - vd) / 1e3 * 1e3)
rng = np.random.default_rng(2026)
t2 = np.linspace(0, 5e-3, 26)
y2 = 3.3 * (1 - np.exp(-t2 / 1e-3)) + rng.normal(0, 0.02, t2.size)
p2, se2, r2 = gauss_newton(charge, charge_jac, t2, y2, (3.0, 0.8e-3))
v.check("Ex 05-03.2a", p2[0])
v.check("Ex 05-03.2b", se2[0])
v.check("Ex 05-03.2c", p2[1] * 1e3)
v.check("Ex 05-03.2d", se2[1] * 1e3)
s2 = math.sqrt(float(r2 @ r2) / (t2.size - 2))
v.check("Ex 05-03.2e", s2 * 1e3)
v.check("Ex 05-03.2f", se2[0] * 0.02 / s2)                                     # covariance scales with sigma^2
v.check("Ex 05-03.2g", se2[1] * 0.02 / s2 * 1e3)
v.check("Ex 05-03.3a", 1e-6 / (2 * 50.0))                                       # exact: mean of sin^2 is 1/2
v.check("Ex 05-03.4a", 5 * (1 - math.exp(-1)))
v.check("Ex 05-03.4b", 100 * (1 - math.exp(-1)))
v.check("Ex 05-03.5a", 50.0)                                                    # R_L = R_s
v.check("Ex 05-03.5b", 1.0**2 / (4 * 50) * 1e3)
for key, target in (("Ex 05-03.6a", "0.5"), ("Ex 05-03.6b", "1.0"), ("Ex 05-03.6c", "1.2"), ("Ex 05-03.6d", "1.8")):
    vo = Fraction(target)
    v.check(key, float(10_000 * vo / (Fraction("3.3") - vo)))

# ---------------------------------------------------------------- solutions
v.check("05-03.1a", float(mp.findroot(lambda x: mp.cos(x) - x, 0.7)))
v.check("05-03.2a", 2.0)                                                        # (x - 2)^2 + 3
v.check("05-03.2b", 3.0)
vd3 = diode(3.3, 330.0)
v.check("05-03.3a", vd3)
v.check("05-03.3b", (3.3 - vd3) / 330 * 1e3)
v.check("05-03.3c", (vd3 - vd) * 1e3)
rng = np.random.default_rng(11)
t4 = np.linspace(0, 10e-3, 21)
y4 = 5.0 * np.exp(-t4 / 2e-3) + rng.normal(0, 0.05, t4.size)
p4, se4, _ = gauss_newton(decay, decay_jac, t4, y4, (4.0, 1.5e-3))
v.check("05-03.4a", p4[0])
v.check("05-03.4b", se4[0])
v.check("05-03.4c", p4[1] * 1e3)
v.check("05-03.4d", se4[1] * 1e3)
v.check("05-03.5a", 2e-3 * 1e-3 * 1e6)                                          # peak current × time constant
v.check("05-03.5b", 2e-3 * 1e-3 * (1 - math.exp(-1)) * 1e6)
v.check("05-03.6a", 2 * (1 - math.exp(-1)))
v.check("05-03.7a", float(Fraction(4700 * 10000, 10000 - 4700)))
par = lambda a, b: a * b / (a + b)                                              # noqa: E731
v.check("05-03.7b", par(10, 8.2))
v.check("05-03.7c", par(10, 9.1))
v.check("05-03.9a", (8.7 + 7.5) / 2)
v.check("05-03.9b", float(CubicSpline([0, 1, 2, 3, 4, 5.0], [10, 9.6, 8.7, 7.5, 6.3, 5.2])(2.5)))
rng = np.random.default_rng(5)
t10 = np.linspace(0, 25e-3, 51)
y10 = 5 * (1 - np.exp(-t10 / 1e-3)) + 0.5 * (1 - np.exp(-t10 / 5e-3)) + rng.normal(0, 0.01, t10.size)
p10, _, r10 = gauss_newton(charge, charge_jac, t10, y10, (5.0, 1e-3))
v.check("05-03.10a", p10[0])
v.check("05-03.10b", p10[1] * 1e3)
v.check("05-03.10c", math.sqrt(float(np.mean(r10**2))) * 1e3)
runs10 = sum(1 for k in range(len(r10)) if k == 0 or (r10[k] > 0) != (r10[k - 1] > 0))
n1, n0 = int(np.sum(r10 > 0)), int(np.sum(r10 < 0))
v.check("05-03.10d", runs10)
v.check("05-03.10e", 2 * n1 * n0 / (n1 + n0) + 1)
v.check("05-03.10f", math.sqrt(2 * n1 * n0 * (2 * n1 * n0 - n1 - n0) / ((n1 + n0) ** 2 * (n1 + n0 - 1))))   # Wald-Wolfowitz variance
v.check("05-03.11a", 1e3 * math.sqrt(99))
v.check("05-03.13a", -math.degrees(math.atan(1.0)))
v.check("05-03.13b", -10 * math.log10(101))
v.check("05-03.13c", -10 * math.log10(10001))
v.check("05-03.13d", -10 * math.log10(10001) + 10 * math.log10(101))
v.check("05-03.12a", len({round(float(mp.findroot(lambda x: x**3 - 6 * x**2 + 11 * x - 6, g)), 9) for g in (0.8, 2.1, 3.3)}))

# ---------------------------------------------------------------- lab: count evaluations with our own instrumented copies
i_s, v_t = 1e-14, 0.025852
count = {"n": 0}


def f_d(x):
    count["n"] += 1
    return (5.0 - x) / 1e3 - i_s * (math.exp(x / v_t) - 1)


lo, hi = 0.0, 1.0
count["n"] = 0
f_lo = f_d(lo)
while hi - lo > 1e-12:
    mid = (lo + hi) / 2
    f_mid = f_d(mid)
    if f_lo * f_mid <= 0:
        hi = mid
    else:
        lo, f_lo = mid, f_mid
v.check("Lab 05-03.a", count["n"])
from scipy.optimize import brentq, newton  # noqa: E402  (the lab's own tools, run here only to count their calls)
count["n"] = 0
brentq(f_d, 0.0, 1.0, xtol=1e-12)
v.check("Lab 05-03.b", count["n"])
count["n"] = 0
newton(f_d, 0.7, tol=1e-12)
v.check("Lab 05-03.c", count["n"])
two = lambda t, a1, t1, a2, t2: a1 * (1 - np.exp(-t / t1)) + a2 * (1 - np.exp(-t / t2))  # noqa: E731
def two_jac(t, a1, t1, a2, t2):
    e1, e2 = np.exp(-t / t1), np.exp(-t / t2)
    return np.column_stack([1 - e1, -a1 * t / t1**2 * e1, 1 - e2, -a2 * t / t2**2 * e2])


p2e, _, _ = gauss_newton(two, two_jac, t10, y10, (5, 1e-3, 0.5, 5e-3))
v.assert_true("two-exponential fit recovers the true time constants within 10%", abs(p2e[1] / 1e-3 - 1) < 0.1 and abs(p2e[3] / 5e-3 - 1) < 0.1)
v.check("Lab 05-03.d", math.sqrt(float(np.mean((y10 - two(t10, *p2e)) ** 2))) * 1e3)
v.check("Lab 05-03.e", p2e[3] * 1e3)
n_r = 256                                                                         # closed-form geometric sums of e^(k/n)
left_sum = (math.e - 1) / (n_r * (math.exp(1 / n_r) - 1))
v.check("Lab 05-03.f", abs(left_sum - (math.e - 1)))
v.check("Lab 05-03.g", abs(left_sum + (math.e - 1) / (2 * n_r) - (math.e - 1)))   # trapezoid = left + (g(1) - g(0)) h / 2

sys.exit(v.finish())
