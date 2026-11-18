#!/usr/bin/env python3
"""Verify every published number in chapter 02-10, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-10",
    COURSE / "chapters" / "02-10-numerical-methods.md",
    COURSE / "solutions" / "02-10-solutions.md",
    COURSE / "labs" / "02-10-lab" / "README.md",
)

# ---------------------------------------------------------------- shared models
K_B, Q_E = 1.380649e-23, 1.602176634e-19
VT = K_B * 300.15 / Q_E                  # ngspice default temperature (R-053)
IS, RR, VS = 1e-14, 1e3, 5.0
fd = lambda vv: (VS - vv) / RR - IS * (math.exp(vv / VT) - 1)  # noqa: E731
fdp = lambda vv: -1 / RR - IS / VT * math.exp(vv / VT)  # noqa: E731
VCRIT = VT * math.log(VT / (math.sqrt(2) * IS))


def pnjlim(vnew, vold):
    """ngspice DEVpnjlim (src/spicelib/devices/devsup.c), positive-step branch and first-step branch."""
    if vnew > VCRIT and abs(vnew - vold) > 2 * VT:
        if vold > 0:
            arg = (vnew - vold) / VT
            return vold + VT * (2 + math.log(arg - 2)) if arg > 0 else vold - VT * (2 + math.log(2 - arg))
        return VT * math.log(vnew / VT)
    return vnew


def newton(v0, limit=False, tol=1e-12, maxit=500):
    vv, seq = v0, [v0]
    for k in range(1, maxit + 1):
        vn = vv - fd(vv) / fdp(vv)
        if limit:
            vn = pnjlim(vn, vv)
        seq.append(vn)
        if abs(vn - vv) < tol:
            return k, seq
        vv = vn
    return None, seq


def integrate(step, h, T=1.0, y=1.0):
    for _ in range(round(T / h)):
        y = step(y, h)
    return y


euler = lambda y, h: y - h * y  # noqa: E731
heun = lambda y, h: y + h / 2 * (-y - (y - h * y))  # noqa: E731


def rk4(y, h):
    k1 = -y; k2 = -(y + h / 2 * k1); k3 = -(y + h / 2 * k2); k4 = -(y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# ---------------------------------------------------------------- theory identities
v.assert_true("machine epsilon 2^-52 and unit roundoff 2^-53", np.finfo(float).eps == 2.0**-52 and 1.0 + 2.0**-53 == 1.0)
v.assert_true("0.1 is not exact; 0.375 is", (0.1).as_integer_ratio()[1] != 10 and (0.375).as_integer_ratio() == (3, 8))
z = np.linspace(-5, 0, 200001)
rk4R = 1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24
edge = z[np.where(np.abs(rk4R) <= 1)[0].min()]
v.assert_true("RK4 real-axis stability limit about -2.785", abs(edge + 2.785) < 1e-3)
v.assert_true("trapezoidal factor -> -1 as h lambda -> -inf", abs((1 - 1e9 / 2) / (1 + 1e9 / 2) + 1) < 1e-8)
A_ = np.random.default_rng(4).standard_normal((5, 5))
v.assert_true("kappa = sigma_max/sigma_min", np.isclose(np.linalg.cond(A_), np.divide(*np.linalg.svd(A_, compute_uv=False)[[0, -1]])))
e_seq = [abs(x - math.sqrt(2)) for x in (1.5, 17 / 12, 577 / 408)]
v.assert_true("Newton error ~ e^2/(2 sqrt2) for sqrt(2)", abs(e_seq[2] - e_seq[1] ** 2 / (2 * math.sqrt(2))) < 1e-7)

# ---------------------------------------------------------------- Example 1
v.check("Ex 02-10.1a", 0.1 + 0.2 - 0.3)
v.check("Ex 02-10.1b", 1 - math.cos(1e-8))
v.check("Ex 02-10.1c", 2 * math.sin(0.5e-8) ** 2)
d = math.sqrt(1e16 - 4)
v.check("Ex 02-10.1d", (-1e8 + d) / 2)
v.check("Ex 02-10.1e", 1 / ((-1e8 - d) / 2))
v.assert_true("Ex 1: 0.1 + 0.2 - 0.3 = 2^-54", 0.1 + 0.2 - 0.3 == 2.0**-54)

# ---------------------------------------------------------------- Example 2 (diode Newton)
vstar = brentq(fd, 0, 1, xtol=1e-15)
v.check("Ex 02-10.2a", vstar)
v.check("Ex 02-10.2b", (VS - vstar) / RR * 1e3)
n07, s07 = newton(0.7)
v.check("Ex 02-10.2c", n07)
errs = [abs(x - vstar) for x in s07]
v.assert_true("Ex 2: quadratic convergence (e_{k+1}/e_k^2 roughly constant)",
              0.5 < (errs[3] / errs[2] ** 2) / (errs[2] / errs[1] ** 2) < 2)
n06, s06 = newton(0.6)
v.check("Ex 02-10.2d", s06[1])
v.check("Ex 02-10.2e", n06)
v.check("Ex 02-10.2f", VCRIT)
nl, sl = newton(0.6, limit=True)
v.check("Ex 02-10.2g", nl)
v.assert_true("Ex 2: 173 plain and 9 limited iterations from 0 V", newton(0.0)[0] == 173 and newton(0.0, True)[0] == 9)
v.check("Ex 02-10.2h", IS * math.exp(vstar / VT) / VT * 1e3)

# ---------------------------------------------------------------- Example 3 (companion model)
v0 = 0.7
G0 = IS * math.exp(v0 / VT) / VT
i0 = IS * (math.exp(v0 / VT) - 1)
Ieq = i0 - G0 * v0
v1 = (VS / RR - Ieq) / (1 / RR + G0)
v.check("Ex 02-10.3a", i0 * 1e3); v.check("Ex 02-10.3b", G0); v.check("Ex 02-10.3c", Ieq); v.check("Ex 02-10.3d", v1)
v.assert_true("Ex 3: companion iterate equals Newton iterate", abs(v1 - (v0 - fd(v0) / fdp(v0))) < 1e-14)

# ---------------------------------------------------------------- Example 4 (order)
ex = math.exp(-1)
for st, ka, kb in ((euler, "Ex 02-10.4a", "Ex 02-10.4b"), (heun, "Ex 02-10.4c", "Ex 02-10.4d"), (rk4, "Ex 02-10.4e", "Ex 02-10.4f")):
    e1, e2 = abs(integrate(st, 0.1) - ex), abs(integrate(st, 0.05) - ex)
    v.check(ka, e1); v.check(kb, e1 / e2)
v.assert_true("Ex 4: Euler y(1) = 0.9^10", abs(integrate(euler, 0.1) - 0.9**10) < 1e-15)

# ---------------------------------------------------------------- Example 5 (stiffness)
lf, ls_, h5 = -1e6, -1e3, 50e-6
v.check("Ex 02-10.5a", 2 / abs(lf) * 1e6)
v.check("Ex 02-10.5b", 5e-3 / (2 / abs(lf)))
v.check("Ex 02-10.5c", 5e-3 / h5)
v.check("Ex 02-10.5d", 1 / (1 - h5 * lf)); v.check("Ex 02-10.5e", 1 / (1 - h5 * ls_))
v.check("Ex 02-10.5f", (1 + h5 * ls_ / 2) / (1 - h5 * ls_ / 2)); v.check("Ex 02-10.5g", (1 + h5 * lf / 2) / (1 - h5 * lf / 2))
v.assert_true("Ex 5: trapezoidal slow factor within 1e-5 of exact", abs((1 + h5 * ls_ / 2) / (1 - h5 * ls_ / 2) - math.exp(h5 * ls_)) < 1e-5)

# ---------------------------------------------------------------- Example 6 (conditioning)
A6 = np.array([[1, 1], [1, 1.0001]])
k6 = np.linalg.cond(A6)
v.check("Ex 02-10.6a", k6)
x1 = np.linalg.solve(A6, [2, 2.0001]); x2 = np.linalg.solve(A6, [2, 2.0002])
v.assert_true("Ex 6: solutions (1, 1) and (0, 2)", np.allclose(x1, [1, 1]) and np.allclose(x2, [0, 2], atol=1e-8))
v.check("Ex 02-10.6b", np.linalg.norm(x2 - x1) / np.linalg.norm(x1) * 100)
v.check("Ex 02-10.6c", math.log10(k6))
v.assert_true("Ex 6: bound kappa * rel(db) >= rel(dx)",
              k6 * np.linalg.norm([0, 1e-4]) / np.linalg.norm([2, 2.0001]) >= np.linalg.norm(x2 - x1) / np.linalg.norm(x1))

# ---------------------------------------------------------------- numbers to know
v.check("N 02-10.a", np.finfo(float).eps)
v.check("N 02-10.b", 1 / math.log10(2))
v.check("N 02-10.c", float(np.finfo(np.float16).max))
v.check("N 02-10.d", 1.75 * 2**8)       # E4M3: S.1111.110 = 1.75 x 2^(15-7)
v.check("N 02-10.e", 1.75 * 2**15)      # E5M2: S.11110.11 = 1.75 x 2^(30-15)
mxp, hpl = 16.680, 1.8090             # HPL-MxP Nov 2026 (R-055)
v.check("N 02-10.f", mxp); v.check("N 02-10.g", hpl); v.check("N 02-10.h", mxp / hpl)
tick_err = 0.1 * 2.0**-20             # Skeel: 0.1 chopped to 23 binary places (R-057)
v.check("N 02-10.i", tick_err * 100 * 3600 * 10)
v.check("N 02-10.j", 687)              # GAO's tabulated range-gate shift (sourced constant)

# ---------------------------------------------------------------- Problems 1-6
for key, p in (("02-10.1a", 52), ("02-10.1b", 23), ("02-10.1c", 10)):
    v.check(key, 2.0**-p)
for key, p in (("02-10.1d", 52), ("02-10.1e", 23), ("02-10.1f", 10)):
    v.check(key, -math.log10(2.0 ** -(p + 1)))
s32 = np.float32(0)
for _ in range(10):
    s32 = np.float32(s32 + np.float32(0.1))
v.check("02-10.2a", float(s32), tol=5e-8)
v.check("02-10.2b", float(s32) - 1.0)
v.check("02-10.3a", math.ceil(math.log2(1e6)))
x = 1.0; xs = []
for _ in range(3):
    x = 0.5 * (x + 2 / x); xs.append(x)
v.check("02-10.4a", xs[0]); v.check("02-10.4b", xs[1]); v.check("02-10.4c", xs[2])
direct = math.exp(1e-10) - 1
v.check("02-10.5a", abs(direct - math.expm1(1e-10)) / math.expm1(1e-10))
data = np.array([1e8 + 1, 1e8 + 2, 1e8 + 3])
v.check("02-10.5b", float(np.mean(data**2) - np.mean(data) ** 2))
v.check("02-10.5c", float(np.mean((data - data.mean()) ** 2)))
x = 1.0; nn = 0
while True:
    xn = x - (x - math.cos(x)) / (1 + math.sin(x)); nn += 1
    if abs(xn - x) < 1e-14:
        x = xn
        break
    x = xn
v.check("02-10.6a", x); v.check("02-10.6b", nn); v.check("02-10.6c", math.sin(x))
y = 1.0; nf = 0
while abs(y - x) > 1e-10:
    y = math.cos(y); nf += 1
v.check("02-10.6d", nf)

# ---------------------------------------------------------------- Problems 7-12
X = np.array([2.0, 0.5])
F = lambda X: np.array([X[0]**2 + X[1]**2 - 4, X[0] * X[1] - 1])  # noqa: E731
J = lambda X: np.array([[2 * X[0], 2 * X[1]], [X[1], X[0]]])  # noqa: E731
X1 = X - np.linalg.solve(J(X), F(X))
v.check("02-10.7a", X1[0]); v.check("02-10.7b", X1[1])
for _ in range(8):
    X = X - np.linalg.solve(J(X), F(X))
v.check("02-10.7c", X[0]); v.check("02-10.7d", X[1])
v.assert_true("P7: exact root x = sqrt(2 + sqrt3)", abs(X[0] - math.sqrt(2 + math.sqrt(3))) < 1e-12)
f8 = lambda y: -2 * y  # noqa: E731
h = 0.1
k1 = f8(1); k2 = f8(1 + h * k1)
v.check("02-10.8a", 1 + h * f8(1)); v.check("02-10.8b", 1 + h / 2 * (k1 + k2))
k1 = f8(1); k2 = f8(1 + h / 2 * k1); k3 = f8(1 + h / 2 * k2); k4 = f8(1 + h * k3)
v.check("02-10.8c", 1 + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)); v.check("02-10.8d", math.exp(-0.2))
tau9 = 10e-6; z9 = -30e-6 / tau9
v.check("02-10.9a", 2 * tau9 * 1e6); v.check("02-10.9b", 1 + z9); v.check("02-10.9c", 1 / (1 - z9))
v.check("02-10.9d", (1 + z9 / 2) / (1 - z9 / 2))
C10, h10, R10, vn = 1e-6, 10e-6, 100, 2.0
G10 = C10 / h10
v.check("02-10.10a", G10); v.check("02-10.10b", G10 * vn)
v.check("02-10.10c", G10 * vn / (G10 + 1 / R10)); v.check("02-10.10d", vn * math.exp(-h10 / (R10 * C10)))
A11 = np.array([[1, 1], [1, 1.01], [1, 1.02]])
v.check("02-10.11a", np.linalg.cond(A11)); v.check("02-10.11b", np.linalg.cond(A11.T @ A11))
v.check("02-10.12a", float(np.spacing(np.float32(1e8))))
v.assert_true("P12: float32 1e8 + 1 == 1e8; counter stalls at 2^24",
              np.float32(1e8) + np.float32(1) == np.float32(1e8) and np.float32(2**24) + np.float32(1) == np.float32(2**24))

# ---------------------------------------------------------------- Problems 13-15
x = 2.0; n13 = 0
while abs(x - 1) > 1e-6:
    x = x - (x - 1) ** 2 / (2 * (x - 1)); n13 += 1
v.check("02-10.13a", n13)
v.assert_true("P13: modified Newton converges in one step", 2.0 - 2 * (2.0 - 1) ** 2 / (2 * (2.0 - 1)) == 1.0)
v.check("02-10.14a", 10e-6 / 2e-12); v.check("02-10.14b", 10e-6 / 10e-9); v.check("02-10.14c", (10e-6 / 2e-12) / (10e-6 / 10e-9))
kap, uh, us = 1e3, 2.0**-11, 2.0**-24
v.check("02-10.15a", kap * uh); v.check("02-10.15b", kap * us)
v.check("02-10.15c", math.log(1e-16 / (kap * uh)) / math.log(kap * uh))
v.check("02-10.15d", math.log(1e-16 / (kap * us)) / math.log(kap * us))
v.check("02-10.15e", 1 / uh)

# ---------------------------------------------------------------- lab handout
s16 = np.float16(0)
for _ in range(20000):
    s16 = np.float16(s16 + np.float16(0.1))
v.check("Lab 02-10.a", float(s16))
v.check("Lab 02-10.b", float(np.spacing(np.float16(256))))
s32 = np.float32(0)
for _ in range(20000):
    s32 = np.float32(s32 + np.float32(0.1))
v.check("Lab 02-10.c", float(s32))
v.check("Lab 02-10.d", float(np.spacing(np.float32(1e8))))

v.finish()
