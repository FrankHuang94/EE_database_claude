#!/usr/bin/env python3
"""Verify every number in the Course 15 final-exam solutions.

Independent routes:
- thermal and leakage results from the one-node model in closed form, checked against the leakage-modified node equation;
- closed-loop parameters, overshoot, peak and settling times from exact step responses (labs/15-03-lab/specs.py)
  and their closed forms;
- Routh arrays built here, checked against numpy roots; root-locus points by the angle condition, checked
  against the roots of the closed-loop polynomial;
- margins by root finding (labs/15-07-lab/freqdomain.py), checked against the closed forms of the solutions;
- the lead design re-derived step by step and confirmed by the compensated loop's margin;
- state feedback and observer gains by coefficient matching, checked by eigenvalues;
- discretization and the PLL design from closed forms, confirmed with scipy and with the PLL loop's margin;
- the derivations' identities checked numerically (final value, lead phase maximum, ZOH frequency response).
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("15-03-lab", "15-04-lab", "15-07-lab", "15-11-lab", "15-12-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
from specs import step_specs  # noqa: E402
from freqdomain import margins  # noqa: E402
import digital as dg  # noqa: E402
import loops as lp  # noqa: E402

v = Verifier.from_files("15-exam", ROOT / "exam" / "solutions.md")
TWO_PI = 2 * math.pi


def routh_first_column(coeffs):
    n = len(coeffs)
    rows = [list(coeffs[0::2]), list(coeffs[1::2])]
    width = len(rows[0])
    rows = [r + [0.0] * (width - len(r)) for r in rows]
    for _ in range(n - 2):
        a, b = rows[-2], rows[-1]
        new = [(b[0] * a[i + 1] - a[0] * b[i + 1]) / b[0] for i in range(width - 1)] + [0.0]
        rows.append(new)
    return [r[0] for r in rows], rows


# 1 Modeling
v.check("X15.1a", 25 + 20 * 2.5)
v.check("X15.1b", 2.5 * 4)
v.check("X15.1c", 25 + 50 * (1 - math.exp(-10 / 10)))
v.check("X15.1d", 2.5 * 0.1)
v.check("X15.1e", 10 / (1 - 0.25))
# the leakage-modified node: C dT/dt = P + 0.1 dT - dT/R -> time constant C/(1/R - 0.1)
v.assert_true("Q1d: C/(1/R - dP/dT) equals tau/(1 - G)", abs(4 / (1 / 2.5 - 0.1) - 10 / 0.75) < 1e-12)

# 2 Loop
K = 1.0
num_T, den_T = [10 * K], [1, 2, 10 * K]
wn, zeta = math.sqrt(10), 1 / math.sqrt(10)
v.check("X15.2a", wn)
v.check("X15.2b", zeta)
v.assert_true("Q2: poles match wn, zeta", np.allclose(sorted(np.roots(den_T), key=lambda z: z.imag),
                                                        sorted([complex(-zeta * wn, -wn * math.sqrt(1 - zeta**2)),
                                                                complex(-zeta * wn, wn * math.sqrt(1 - zeta**2))], key=lambda z: z.imag)))
t = np.linspace(0, 40, 400001)
_, yd = signal.step(([10], [1, 2, 10 * K]), T=t)
v.check("X15.2c", yd[-1])
S1 = abs((1j) * (1j + 2) / ((1j) ** 2 + 2j + 10))
v.check("X15.2d", S1)
v.assert_true("Q2d: sqrt(5)/sqrt(85)", abs(S1 - math.sqrt(5 / 85)) < 1e-12)

# 3 Time response
sp = step_specs(num_T, den_T, 20, n=400001)
v.check("X15.3a", 100 * sp["overshoot"])
v.check("X15.3b", sp["tpeak"])
v.assert_true("Q3: closed forms e^(-pi/3) and pi/3", abs(sp["overshoot"] - math.exp(-math.pi / 3)) < 1e-9 and abs(sp["tpeak"] - math.pi / 3) < 1e-9)
v.check("X15.3c", 4 / (zeta * wn))
v.check("X15.3d", sp["settle"])
z10 = -math.log(0.1) / math.sqrt(math.pi**2 + math.log(0.1) ** 2)
v.check("X15.3e", z10)
K10 = (1 / z10) ** 2 / 10
v.check("X15.3f", K10)
v.check("X15.3g", 1 / z10)
v.assert_true("Q3d: 10% overshoot at that gain", abs(step_specs([10 * K10], [1, 2, 10 * K10], 30, n=200001)["overshoot"] - 0.1) < 1e-6)

# 4 Steady-state error
numL4 = np.polymul([20], [1, 2])
denL4 = np.polymul(np.polymul([1, 0], [1, 4]), [1, 10])
Kv4 = 20 * 2 / (4 * 10)
v.check("X15.4a", Kv4)
import steady  # noqa: E402  (labs/15-04-lab)
ec4 = steady.error_constants(numL4, denL4)
v.check("X15.4b", ec4[2])
char4 = np.polyadd(denL4, numL4)
v.assert_true("Q4: characteristic polynomial s^3 + 14s^2 + 60s + 40", np.allclose(char4, [1, 14, 60, 40]))
col4, _ = routh_first_column([1.0, 14.0, 60.0, 40.0])
v.check("X15.4d", col4[2])
v.assert_true("Q4: stable (first column positive, roots in LHP)", all(c > 0 for c in col4) and np.all(np.roots(char4).real < 0))
# ramp error by simulation of E = R/(1 + L) with R = 1/s^2: e(t) -> 1/Kv
tt = np.linspace(0, 80, 160001)
_, e_r, _ = signal.lsim((denL4, char4), U=tt, T=tt)
v.check("X15.4c", e_r[-1])
v.check("X15.13a", 1 / Kv4)
v.assert_true("Q13a: simulated ramp error equals 1/Kv", abs(e_r[-1] - 1 / Kv4) < 1e-6)
# disturbance at plant input: Y/D = (s + 10)/[s(s+4)(s+10) + 20(s+2)]
_, ydist = signal.step(([1, 10], char4), T=tt)
v.check("X15.4e", ydist[-1])

# 5 Routh
for Kt in (1.0, 1.99, 2.01, 3.0):
    colK, _ = routh_first_column([1.0, 2.0, 3.0, 2.0, Kt])
    stable = np.all(np.roots([1, 2, 3, 2, Kt]).real < 0)
    v.assert_true(f"Q5: Routh verdict matches roots at K={Kt}", (all(c > 0 for c in colK)) == stable)
v.check("X15.5a", brentq(lambda k: max(np.roots([1, 2, 3, 2, k]).real), 1.0, 3.0, xtol=1e-14))
v.assert_true("Q5: s1 row 2 - K", abs(routh_first_column([1.0, 2.0, 3.0, 2.0, 1.5])[0][3] - 0.5) < 1e-12)
r2 = np.roots([1, 2, 3, 2, 2.0])
v.check("X15.5b", max(abs(r.imag) for r in r2 if abs(r.real) < 1e-9))
col3, _ = routh_first_column([1.0, 2.0, 3.0, 2.0, 3.0])
changes = sum(1 for a, b in zip(col3, col3[1:]) if a * b < 0)
v.check("X15.5c", changes)
v.assert_true("Q5d: two RHP roots at K = 3", sum(np.roots([1, 2, 3, 2, 3]).real > 0) == 2)

# 6 Root locus
v.check("X15.6a", (0 - 2 - 4) / 3)
v.check("X15.6b", 180 / 3)
sb = -2 + 2 / math.sqrt(3)
v.check("X15.6c", sb)
v.check("X15.6d", abs(sb * (sb + 2) * (sb + 4)))
v.assert_true("Q6b: double root at breakaway", np.min(np.abs(np.roots([1, 6, 8, abs(sb * (sb + 2) * (sb + 4))]) - sb)) < 1e-6)
k6e = brentq(lambda k: max(np.roots([1, 6, 8, k]).real), 10, 100, xtol=1e-12)
v.check("X15.6e", k6e)
r6e = np.roots([1, 6, 8, 48.0])
v.check("X15.6f", float(np.max(r6e.imag)))
v.assert_true("Q6c: pure imaginary pair at K = 48, bracketing gains stable/unstable",
              abs(r6e[np.argmax(r6e.imag)].real) < 1e-9 and max(np.roots([1, 6, 8, 47.9]).real) < 0 < max(np.roots([1, 6, 8, 48.1]).real))
ray = complex(-0.5, math.sqrt(3) / 2)
r6 = brentq(lambda r: (math.degrees(cmath.phase(r * ray)) + math.degrees(cmath.phase(r * ray + 2))
                       + math.degrees(cmath.phase(r * ray + 4))) - 180, 0.5, 3)
s6 = r6 * ray
K6 = abs(s6 * (s6 + 2) * (s6 + 4))
v.check("X15.6g", s6)
v.check("X15.6h", K6)
v.assert_true("Q6d: r = 4/3 and K = 224/27", abs(r6 - 4 / 3) < 1e-10 and abs(K6 - 224 / 27) < 1e-9)
rts = np.roots([1, 6, 8, K6])
v.check("X15.6i", float(rts[np.argmin(np.abs(rts.imag))].real))

# 7 Frequency response
m7 = margins([40], [1, 12, 20, 0], w_lo=1e-3, w_hi=1e3)
v.check("X15.7a", m7["wc"])
v.check("X15.7b", m7["pm"])
v.check("X15.7c", m7["w180"])
v.check("X15.7d", m7["gm"])
v.check("X15.7e", m7["gm_db"])
v.check("X15.7f", m7["delay_margin"])
from freqdomain import nyquist_encirclements, closed_loop_rhp  # noqa: E402
v.check("X15.7g", closed_loop_rhp([40], [1, 12, 20, 0]))
v.check("X15.7h", nyquist_encirclements([320], [1, 12, 20, 0]))
v.check("X15.7i", int(sum(np.roots(np.polyadd([1, 12, 20, 0], [320])).real > 0)))
v.check("X15.7j", math.radians(m7["pm"]))
xk = 2.0
for _ in range(6):
    xk -= (xk**3 + 104 * xk**2 + 400 * xk - 1600) / (3 * xk**2 + 208 * xk + 400)
v.check("X15.7k", xk)
v.assert_true("Q7a: Newton iterate and crossover agree", abs(math.sqrt(xk) - m7["wc"]) < 1e-9)
v.assert_true("Q7: w180 = sqrt(20), GM = 6 exactly", abs(m7["w180"] - math.sqrt(20)) < 1e-9 and abs(m7["gm"] - 6) < 1e-9)
v.assert_true("Q7d: Routh limit 12*20/40 = 6", all(c > 0 for c in routh_first_column([1, 12, 20, 40 * 5.999])[0])
              and any(c < 0 for c in routh_first_column([1, 12, 20, 40 * 6.001])[0]))
v.assert_true("Q7a: PM closed form", abs(m7["pm"] - (90 - math.degrees(math.atan(m7["wc"] / 2) + math.atan(m7["wc"] / 10)))) < 1e-9)

# 8 PID tuning
col8 = [routh_first_column([1, 3, 3, 1 + k])[0] for k in (7.99, 8.01)]
v.assert_true("Q8: Ku = 8 by Routh", all(c > 0 for c in col8[0]) and any(c < 0 for c in col8[1]))
v.check("X15.8a", 8)
Pu = TWO_PI / math.sqrt(3)
v.assert_true("Q8: oscillation at sqrt(3)", np.min(np.abs(np.roots([1, 3, 3, 9]) - 1j * math.sqrt(3))) < 1e-9)
v.check("X15.8b", Pu)
Kp8, Ti8, Td8 = 0.6 * 8, Pu / 2, Pu / 8
v.check("X15.8c", Kp8)
v.check("X15.8d", Ti8)
v.check("X15.8e", Td8)
v.check("X15.8f", Kp8 / Ti8)
v.check("X15.8g", Kp8 * Td8)

# 9 Lead design
K9 = 20 / 2
v.check("X15.9a", K9)
m9 = margins([4 * K9], [1, 2, 0], w_lo=1e-3, w_hi=1e4)
v.check("X15.9b", m9["wc"])
v.check("X15.9c", m9["pm"])
phi9 = 50 - m9["pm"] + 10
v.check("X15.9d", phi9)
a9 = (1 + math.sin(math.radians(phi9))) / (1 - math.sin(math.radians(phi9)))
v.check("X15.9e", a9)
wm9 = brentq(lambda w: 40 / (w * math.sqrt(w * w + 4)) - 1 / math.sqrt(a9), 1, 100)
v.check("X15.9f", wm9)
T9 = 1 / (wm9 * math.sqrt(a9))
v.check("X15.9g", T9)
v.check("X15.9h", 1 / (a9 * T9))
v.check("X15.9i", 1 / T9)
mc9 = margins([40 * a9 * T9, 40], np.polymul([T9, 1], [1, 2, 0]), w_lo=1e-3, w_hi=1e4)
v.check("X15.9j", mc9["pm"])
v.assert_true("Q9: compensated crossover at wm and Kv unchanged", abs(mc9["wc"] - wm9) < 1e-6 and abs(40 / 2 - 20) < 1e-12)

# 10 State space
A = np.array([[0.0, 1.0], [-2.0, -3.0]])
B = np.array([[0.0], [1.0]])
Cm = np.array([[1.0, 0.0]])
eig = np.sort(np.linalg.eigvals(A).real)
v.check("X15.10a", eig[1])
v.check("X15.10b", eig[0])
v.assert_true("Q10b: controllable", np.linalg.matrix_rank(np.hstack([B, A @ B])) == 2 and abs(np.linalg.det(np.hstack([B, A @ B])) + 1) < 1e-12)
k1, k2 = 32 - 2, 8 - 3
v.check("X15.10c", k1)
v.check("X15.10d", k2)
Acl = A - B @ np.array([[k1, k2]])
v.assert_true("Q10c: poles at -4 +- j4", np.allclose(sorted(np.linalg.eigvals(Acl), key=lambda z: z.imag), [-4 - 4j, -4 + 4j]))
N10 = -1 / (Cm @ np.linalg.solve(Acl, B))[0, 0]
v.check("X15.10e", N10)
l1 = 20 - 3
l2 = 100 - 2 - 3 * l1
v.check("X15.10f", l1)
v.check("X15.10g", l2)
v.assert_true("Q10d: observer poles at -10, -10", np.allclose(np.linalg.eigvals(A - np.array([[l1], [l2]]) @ Cm), [-10, -10], atol=1e-5))

# 11 Digital
z11 = cmath.exp(complex(-1, 2) * 0.1)
v.check("X15.11a", abs(z11))
v.check("X15.11b", math.degrees(cmath.phase(z11)))
nz, dz = dg.zoh([3], [1, 3], 0.1)
v.check("X15.11c", nz[-1] / dz[0])
v.check("X15.11d", -dz[-1] / dz[0])
v.assert_true("Q11b: closed form 1 - e^-0.3", abs(nz[-1] - (1 - math.exp(-0.3))) < 1e-12)
tn11, td11 = dg.tustin([2, 4], [1, 0], 0.05)
b0, b1 = np.asarray(tn11) / td11[0]
v.assert_true("Q11c: denominator z - 1", np.allclose(np.asarray(td11) / td11[0], [1, -1]))
v.check("X15.11e", b0)
v.check("X15.11f", b1)
Hz11 = (1 - cmath.exp(-1j * 10 * 0.02)) / (1j * 10 * 0.02)
v.check("X15.11g", -math.degrees(cmath.phase(Hz11)))

# 12 PLL
x12 = math.tan(math.radians(50)) + 1 / math.cos(math.radians(50))
wc12 = TWO_PI * 500e3
tz12, tp12, K12 = x12 / wc12, 1 / (x12 * wc12), wc12**2 / x12
Ct12 = 200e-6 * TWO_PI * 400e6 / (TWO_PI * 40 * K12)
C2_12 = Ct12 / x12**2
C12 = Ct12 - C2_12
v.check("X15.12a", x12)
v.check("X15.12b", x12**2)
v.check("X15.12c", tz12 * 1e6)
v.check("X15.12d", tp12 * 1e6)
v.check("X15.12e", K12)
v.check("X15.12f", Ct12 * 1e12)
v.check("X15.12g", C2_12 * 1e12)
v.check("X15.12h", C12 * 1e12)
v.check("X15.12i", tz12 / C12 / 1e3)
v.check("X15.12j", 180 * 500e3 / 20e6)
v.check("X15.12k", wc12)
num12, den12 = lp.pll_loop(200e-6, TWO_PI * 400e6, 40, tz12 / C12, C12, C2_12)
m12 = margins(num12, den12, w_lo=1e2, w_hi=1e10)
v.assert_true("Q12: the components give 500 kHz and 50 deg", abs(m12["wc"] / wc12 - 1) < 1e-9 and abs(m12["pm"] - 50) < 1e-9)
v.assert_true("Q12a: tan 50 = 1.192, sec 50 = 1.556", round(math.tan(math.radians(50)), 3) == 1.192 and round(1 / math.cos(math.radians(50)), 3) == 1.556)

# 13 Derivations
a13, T13 = 4.0, 0.05
ph = lambda w: math.atan(a13 * w * T13) - math.atan(w * T13)  # noqa: E731
r13 = minimize_scalar(lambda lw: -ph(10**lw), bounds=(-1, 4), method="bounded", options={"xatol": 1e-12})
v.check("X15.13b", math.degrees(ph(10**r13.x)))
v.check("X15.13c", 10**r13.x)
v.assert_true("Q13b: closed forms asin((a-1)/(a+1)) and 1/(T sqrt a)", abs(math.degrees(math.asin(3 / 5)) - math.degrees(ph(10**r13.x))) < 1e-9
              and abs(10**r13.x - 1 / (T13 * 2)) < 1e-6)
w13, Th = 50.0, 0.01
H = (1 - cmath.exp(-1j * w13 * Th)) / (1j * w13 * Th)
v.check("X15.13d", math.degrees(cmath.phase(H)))
v.check("X15.13e", abs(H))
v.assert_true("Q13c: phase exactly -wT/2 below the sampling frequency",
              all(abs(cmath.phase((1 - cmath.exp(-1j * w * Th)) / (1j * w * Th)) + w * Th / 2) < 1e-12 for w in (1, 100, 300, 600)))

# 14 Diligence
delay = 1.5 / 2e6
v.check("X15.14a", 360 * 1e6 * delay)
v.check("X15.14b", 30 / (360 * delay) / 1e3)
dI, C14, fc14 = 5.0, 200e-6, 50e3
dv_ll = dI / (TWO_PI * fc14 * C14)
v.check("X15.14c", dv_ll * 1e3)
u14 = math.sqrt((1 + math.sqrt(5) / 2) / 2)          # PI crossover / w0 for wz = w0/4
w0_14 = 2 * math.pi * fc14 / u14
v.check("X15.14d", (2 / math.e) * dI / (w0_14 * C14) * 1e3)
v.check("X15.14i", delay * 1e6)
v.check("X15.14e", dI / (TWO_PI * C14 * 0.02) / 1e3)
v.check("X15.14f", u14 * (2 / math.e) * dI / (TWO_PI * C14 * 0.02) / 1e3)
v.assert_true("Q14b: 4.0 and 3.0 times the stated crossover; both above 111 kHz",
              round(dI / (TWO_PI * C14 * 0.02) / fc14, 1) == 4.0 and round(u14 * (2 / math.e) * dI / (TWO_PI * C14 * 0.02) / fc14, 1) == 3.0
              and u14 * (2 / math.e) * dI / (TWO_PI * C14 * 0.02) > 30 / (360 * delay))
tq = np.linspace(0, 40e-6, 40001)
v.assert_true("Q14b: PI peak from the simulated droop", abs(-min(lp.droop(dI, C14, w0_14, w0_14 / 4, tq)) - (2 / math.e) * dI / (w0_14 * C14)) < 1e-6)
v.check("X15.14g", (95 - 35) / 12)
v.check("X15.14h", 12 / ((95 - 35) / 12))

sys.exit(v.finish())
