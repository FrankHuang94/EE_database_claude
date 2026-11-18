#!/usr/bin/env python3
"""Verify every published number in chapter 02-04, its solutions and its lab handout."""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-04",
    COURSE / "chapters" / "02-04-forced-response-and-resonance.md",
    COURSE / "solutions" / "02-04-solutions.md",
    COURSE / "labs" / "02-04-lab" / "README.md",
)
t = sp.symbols("t", real=True)
y = sp.Function("y")
S, W = sp.symbols("s omega")


def lowpass(r, z):
    return 1 / complex(1 - r * r, 2 * z * r)


def bandpass(r, Q):
    return 1 / math.sqrt(1 + Q * Q * (r - 1 / r) ** 2)


def ivp(lhs_coeffs, rhs, y0, dy0):
    a1, a0 = lhs_coeffs
    eq = sp.Eq(y(t).diff(t, 2) + a1 * y(t).diff(t) + a0 * y(t), rhs)
    return sp.dsolve(eq, y(t), ics={y(0): y0, y(t).diff(t).subs(t, 0): dy0}).rhs


# ---------------------------------------------------------------- theory identities
p = S**2 + 2 * sp.Symbol("alpha") * S + sp.Symbol("w0") ** 2
D = lambda f: sp.diff(f, t)  # noqa: E731
pD = lambda f: D(D(f)) + 2 * sp.Symbol("alpha") * D(f) + sp.Symbol("w0") ** 2 * f  # noqa: E731
v.assert_true("ERF: p(D) e^{st} = p(s) e^{st}", sp.simplify(pD(sp.exp(S * t)) - p * sp.exp(S * t)) == 0)
v.assert_true("p(D)(t e^{st}) = p'(s) e^{st} + p(s) t e^{st}",
              sp.simplify(pD(t * sp.exp(S * t)) - (sp.diff(p, S) * sp.exp(S * t) + p * t * sp.exp(S * t))) == 0)
w0s, Fs = sp.symbols("omega_0 F", positive=True)
v.assert_true("undamped resonance (F/2w0) t sin w0 t", sp.simplify(sp.diff(Fs / (2 * w0s) * t * sp.sin(w0s * t), t, 2)
                                                                   + w0s**2 * Fs / (2 * w0s) * t * sp.sin(w0s * t) - Fs * sp.cos(w0s * t)) == 0)
zz, uu = sp.symbols("zeta u", positive=True)
Du = (1 - uu) ** 2 + 4 * zz**2 * uu
v.assert_true("peak at u = 1 - 2 zeta^2 with D_min = 4 zeta^2 (1 - zeta^2)",
              sp.solve(sp.diff(Du, uu), uu) == [1 - 2 * zz**2] and sp.simplify(Du.subs(uu, 1 - 2 * zz**2) - 4 * zz**2 * (1 - zz**2)) == 0)
Qs, r = sp.symbols("Q r", positive=True)
rr = sp.solve(sp.Eq(Qs * (r - 1 / r), 1), r) + sp.solve(sp.Eq(Qs * (r - 1 / r), -1), r)
rr = [x for x in rr if x.subs(Qs, 5) > 0]
v.assert_true("half-power: r2 - r1 = 1/Q and r1 r2 = 1",
              sp.simplify(abs(rr[0] - rr[1]) - 1 / Qs).subs(Qs, 7) == 0 and sp.simplify(rr[0] * rr[1]) == 1)
v.assert_true("butterworth: |H(jw0)| = 1/(2 zeta) = 0.7071 at zeta = 1/sqrt2", math.isclose(abs(lowpass(1, 1 / math.sqrt(2))), 1 / math.sqrt(2)))
yvp = sp.cos(t) * sp.log(sp.cos(t)) + t * sp.sin(t)
v.assert_true("variation of parameters: y'' + y = sec t", sp.simplify(sp.diff(yvp, t, 2) + yvp - 1 / sp.cos(t)) == 0)

# ---------------------------------------------------------------- Example 1
y1 = ivp((3, 2), 4 * t + sp.exp(-3 * t), 0, 0)
v.check("Ex 02-04.1a", float(y1.coeff(sp.exp(-t))))
v.check("Ex 02-04.1b", float(y1.coeff(sp.exp(-2 * t))))
v.check("Ex 02-04.1c", float(y1.subs(t, 1)))

# ---------------------------------------------------------------- Example 2
L2, C2, R2 = 10e-3, 1e-6, 50.0
w02 = 1 / math.sqrt(L2 * C2)
z2 = R2 / 2 * math.sqrt(C2 / L2)
v.check("Ex 02-04.2a", abs(lowpass(0.5, z2)))
v.check("Ex 02-04.2b", math.degrees(cmath.phase(lowpass(0.5, z2))))
v.check("Ex 02-04.2c", abs(lowpass(1, z2)))
v.check("Ex 02-04.2d", abs(lowpass(2, z2)))
v.check("Ex 02-04.2e", math.degrees(cmath.phase(lowpass(2, z2))))
pk = minimize_scalar(lambda rr_: -abs(lowpass(rr_, z2)), bounds=(0.5, 1.2), method="bounded", options={"xatol": 1e-12})
v.check("Ex 02-04.2f", pk.x * w02)
v.check("Ex 02-04.2g", -pk.fun)
v.check("Ex 02-04.2h", 20 * math.log10(-pk.fun))

# ---------------------------------------------------------------- Example 3 (numerical integration as the independent check)
def undamped(w, T):
    sol = solve_ivp(lambda tt, s: [s[1], math.cos(w * tt) - 100 * s[0]], (0, T), [0.0, 0.0],
                    rtol=1e-11, atol=1e-13, dense_output=True, max_step=0.01)
    return sol


v.check("Ex 02-04.3a", 1 / (2 * 10) * 5)
sol3 = undamped(10.0, 5.2)
tt3 = np.linspace(4.6, 5.2, 20001)
v.assert_true("tuned response equals 0.05 t sin 10t (numerical check)", np.max(abs(sol3.sol(tt3)[0] - 0.05 * tt3 * np.sin(10 * tt3))) < 1e-6)
v.check("Ex 02-04.3b", 100 - 9.5**2)
solb = undamped(9.5, 13.0)
tt3b = np.linspace(0, 13.0, 260001)
xb = solb.sol(tt3b)[0]
v.check("Ex 02-04.3c", abs(xb).max(), tol=5e-4)
v.check("Ex 02-04.3d", math.pi / 0.5)
v.check("Ex 02-04.3e", 2 * math.pi / 0.5)
v.check("Ex 02-04.3f", 0.05 * math.pi / 0.5)

# ---------------------------------------------------------------- Example 4 (NFC)
f0 = 13.56e6
L4, R4 = 1e-6, 3.0
w04 = 2 * math.pi * f0
C4 = 1 / (w04**2 * L4)
Q4 = w04 * L4 / R4
v.check("Ex 02-04.4a", C4 * 1e12)
v.check("Ex 02-04.4b", w04 * L4)
v.check("Ex 02-04.4c", Q4)
v.check("Ex 02-04.4d", f0 / Q4 / 1e3)
v.check("Ex 02-04.4e", f0 * (math.sqrt(1 + 1 / (4 * Q4**2)) - 1 / (2 * Q4)) / 1e6)
v.check("Ex 02-04.4f", f0 * (math.sqrt(1 + 1 / (4 * Q4**2)) + 1 / (2 * Q4)) / 1e6)
fu, fl = f0 + 847.5e3, f0 - 847.5e3
# exact series-RLC current response, as an independent check of the band-pass formula
Hser = lambda f, R=R4: abs(R / complex(R, 2 * math.pi * f * L4 - 1 / (2 * math.pi * f * C4)))  # noqa: E731
v.check("Ex 02-04.4g", Hser(fu))
v.check("Ex 02-04.4h", 20 * math.log10(Hser(fu)))
v.check("Ex 02-04.4i", Hser(fl))
Q8 = f0 / (2 * 847.5e3)
v.check("Ex 02-04.4j", Q8)
R8 = w04 * L4 / Q8
v.check("Ex 02-04.4k", R8)
v.check("Ex 02-04.4l", R8 - R4)
v.check("Ex 02-04.4m", Hser(fu, R8))
v.check("Ex 02-04.4n", Hser(fl, R8))
from scipy.optimize import brentq as _bq  # noqa: E402
R_edge = _bq(lambda R: Hser(fl, R) - 1 / math.sqrt(2), 5, 20, xtol=1e-12)
v.check("Ex 02-04.4p", w04 * L4 / R_edge)
v.check("Ex 02-04.4q", R_edge)
_H2 = lambda r, z=0.25: 1 / complex(1 - r**2, 2 * z * r)  # noqa: E731
v.check("Ex 02-04.2i", math.degrees(cmath.phase(_H2(1.0))))
v.check("Ex 02-04.2j", abs(_H2(2.0, 0.0)))
v.check("Fig 02-04.a", 2 * math.pi / 0.5)
v.check("Ex 02-04.5j", 20e-6 * 30 * 86400)
v.check("Ex 02-04.4o", 1 / math.sqrt(2))
v.check("T 02-04.a", 50 * 1)
v.check("T 02-04.b", 1 / Hser(fu))
v.check("T 02-04.c", 1 / Hser(fl))

# ---------------------------------------------------------------- Example 5 (watch crystal)
f5, Q5 = 32768.0, 5e4
w05 = 2 * math.pi * f5
a5 = w05 / (2 * Q5)
v.check("Ex 02-04.5a", w05)
v.check("Ex 02-04.5b", 1 / a5)
v.check("Ex 02-04.5c", math.log(100))
v.check("Ex 02-04.5d", math.log(100) / a5)
v.check("Ex 02-04.5e", math.log(100) / a5 * f5, tol=50)
v.check("Ex 02-04.5f", f5 / Q5)
v.check("Ex 02-04.5g", 2 * Q5 * 1 / f5)
v.check("Ex 02-04.5h", bandpass((f5 + 1) / f5, Q5))
v.check("Ex 02-04.5i", 1 / f5 * 1e6)
v.assert_true("narrow-band approximation agrees with exact band-pass to 0.1 %",
              abs(bandpass((f5 + 1) / f5, Q5) - 1 / math.sqrt(1 + (2 * Q5 / f5) ** 2)) < 1e-3)

# ---------------------------------------------------------------- numbers to know
v.check("N 02-04.a", 1 / math.sqrt(2))
v.check("N 02-04.b", 20 * math.log10(abs(lowpass(1, 1 / math.sqrt(2)))))
v.check("N 02-04.c", 13.56e6 / 16 / 1e3)

# ---------------------------------------------------------------- problems
y2 = ivp((0, 4), 8, 0, 0)
v.check("02-04.2a", max(float(y2.subs(t, x)) for x in np.linspace(0, 2, 20001)))
v.check("02-04.2b", math.pi / 2)
v.check("02-04.3a", 10 / complex(sp.N((S**2 + 2 * S + 5).subs(S, -3))).real)
p4 = complex(sp.N((S**2 + 2 * S + 5).subs(S, sp.I)))
v.check("02-04.4a", 1 / abs(p4))
v.check("02-04.4b", -math.degrees(cmath.phase(p4)))
yp5 = t * sp.sin(3 * t)
v.assert_true("5(a): t sin 3t solves y'' + 9y = 6 cos 3t", sp.simplify(sp.diff(yp5, t, 2) + 9 * yp5 - 6 * sp.cos(3 * t)) == 0)
v.check("02-04.5a", 4)
v.check("02-04.5b", float(sp.diff(S**2 - S - 2, S).subs(S, 2)))
y6 = ivp((3, 2), 10 * sp.cos(t), 0, 0)
v.check("02-04.6a", math.sqrt(10))
v.check("02-04.6b", float(y6.coeff(sp.exp(-t))))
v.check("02-04.6c", float(y6.coeff(sp.exp(-2 * t))))
v.check("02-04.6d", float(y6.subs(t, 1)))
z7 = 0.1
rg = np.linspace(0.9, 1.05, 1500001)
g7 = 1 / np.abs(1 - rg**2 + 2j * z7 * rg)
v.check("02-04.7a", rg[np.argmax(g7)])
v.check("02-04.7b", g7.max())
v.check("02-04.7c", 20 * math.log10(g7.max()))
v.check("02-04.7d", abs(lowpass(1, z7)))
v.check("02-04.7e", abs(lowpass(10, z7)))
v.check("02-04.7f", 20 * math.log10(abs(lowpass(10, z7))))
L8, C8, R8b = 1e-3, 10e-9, 10.0
w08 = 1 / math.sqrt(L8 * C8)
f08 = w08 / (2 * math.pi)
Q8b = w08 * L8 / R8b
f1 = f08 * (math.sqrt(1 + 1 / (4 * Q8b**2)) - 1 / (2 * Q8b))
f2 = f08 * (math.sqrt(1 + 1 / (4 * Q8b**2)) + 1 / (2 * Q8b))
v.check("02-04.8a", w08 / 1e3)
v.check("02-04.8b", f08 / 1e3)
v.check("02-04.8c", Q8b)
v.check("02-04.8d", (f2 - f1) / 1e3)
v.check("02-04.8e", f1 / 1e3)
v.check("02-04.8f", f2 / 1e3)
v.check("02-04.8g", f1 * f2 / 1e6)
R9, L9, C9 = 1e4, 100e-6, 1e-9
w09 = 1 / math.sqrt(L9 * C9)
v.check("02-04.9a", w09 / 1e6)
v.check("02-04.9b", w09 / (2 * math.pi) / 1e3)
v.check("02-04.9c", R9 * math.sqrt(C9 / L9))
Z9 = 1 / (1 / R9 + 1 / (1j * w09 * L9) + 1j * w09 * C9)
v.check("02-04.9d", abs(Z9) * 1e-3)
v.check("02-04.9e", w09 * C9 * abs(Z9) * 1e-3 * 1e3)
v.check("02-04.10a", (440 + 442) / 2)
v.check("02-04.10b", 442 - 440)
v.check("02-04.11a", float(yvp.subs(t, sp.pi / 4)))
yp11 = -sp.cos(t) * sp.log(1 / sp.cos(t) + sp.tan(t))
v.assert_true("11(b): y'' + y = tan t", sp.simplify(sp.diff(yp11, t, 2) + yp11 - sp.tan(t)) == 0)
v.check("02-04.11b", float(yp11.subs(t, sp.pi / 4)))
R12, L12, C12 = 5.0, 1e-3, 1e-6
w012 = 1 / math.sqrt(L12 * C12)
v.check("02-04.12a", w012 / (2 * math.pi) / 1e3)
v.check("02-04.12b", w012 * L12 / R12)
v.check("02-04.12c", 10 / R12)
v.check("02-04.12d", (10 / R12) ** 2 * R12)
vc = (10 / R12) / (w012 * C12)
v.check("02-04.12e", vc)
v.check("02-04.12f", vc * math.sqrt(2))
f13, Q13 = 25e3, 1e4
a13 = 2 * math.pi * f13 / (2 * Q13)
v.check("02-04.13a", f13 / Q13)
v.check("02-04.13b", 1 / a13)
v.check("02-04.13c", math.log(100) / a13)
v.check("02-04.13d", bandpass((f13 + 1) / f13, Q13), tol=2e-4)
out = {n: 4 / (n * math.pi) * bandpass(n / 3, 10) for n in (1, 3, 5, 7)}
v.check("02-04.14a", out[1])
v.check("02-04.14b", out[3])
v.check("02-04.14c", out[5])
v.check("02-04.14d", out[7])
v.check("02-04.14e", bandpass(1 / 3, 10))
v.check("02-04.14f", bandpass(5 / 3, 10))
v.check("02-04.14g", bandpass(7 / 3, 10))
v.check("02-04.14h", 100 * out[1] / out[3])
v.check("02-04.14i", 20 * math.log10(out[1] / out[3]))
v.check("02-04.14j", 4 / math.pi)
v.check("02-04.14k", 4 / (5 * math.pi))
v.check("02-04.14l", 4 / (7 * math.pi))
L15, C15, R15 = 25e-12, 100e-9, 1e-3
w015 = 1 / math.sqrt(L15 * C15)
Z15 = lambda w: 1 / (1 / complex(R15, w * L15) + 1j * w * C15)  # noqa: E731
v.check("02-04.15a", w015 / (2 * math.pi) / 1e6)
v.check("02-04.15b", abs(Z15(w015)) * 1e3)
v.check("02-04.15c", L15 / (R15 * C15) * 1e3)
v.check("02-04.15d", abs(Z15(2 * math.pi * 50e6)) * 1e3)
v.check("02-04.15e", abs(Z15(0.0)) * 1e3)
v.check("02-04.15f", abs(Z15(w015)) * 1 * 1e3)
v.check("02-04.15g", abs(Z15(2 * math.pi * 50e6)) * 1e3)
v.check("02-04.15h", abs(Z15(0.0)) * 1e3)

# ---------------------------------------------------------------- lab handout
v.check("Lab 02-04.a", math.log(100) * 20 / math.pi)
v.check("Lab 02-04.b", 1 / (2 * 0.5 * math.sqrt(1 - 0.25)))
v.check("Lab 02-04.c", pk.x * w02 / (2 * math.pi))
v.check("Lab 02-04.d", w02 / (2 * math.pi))
v.check("Lab 02-04.e", Hser(fu, R8))
v.check("Lab 02-04.f", fu / 1e6)

# 16 · variation of parameters, non-constant Wronskian
t16 = sp.symbols("t16", real=True)
yp16 = (sp.exp(t16) + sp.exp(2 * t16)) * sp.log(1 + sp.exp(-t16)) - sp.exp(t16)
v.assert_true("P16 y_p solves y'' - 3y' + 2y = 1/(1 + e^-t)",
              sp.simplify(sp.diff(yp16, t16, 2) - 3 * sp.diff(yp16, t16) + 2 * yp16 - 1 / (1 + sp.exp(-t16))) == 0)
v.check("02-04.16a", float(yp16.subs(t16, 0)))
# 17 · product input
yp17 = -sp.Rational(2, 9) * sp.cos(t16) + t16 / 3 * sp.sin(t16)
v.assert_true("P17 y_p solves y'' + 4y = t sin t", sp.simplify(sp.diff(yp17, t16, 2) + 4 * yp17 - t16 * sp.sin(t16)) == 0)
v.check("02-04.17a", float(yp17.subs(t16, sp.pi / 2)))

v.finish()
