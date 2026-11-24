#!/usr/bin/env python3
"""Verify every number in chapter 21-01 (S-parameters and network analysis), its problems and its lab.

Independent routes (the lab uses closed-form S and ABCD formulas):
- two-port S-parameters from a nodal solution of the circuit driven by a matched source and terminated in Z0, with
  the waves formed from the solved port voltages and currents;
- the mismatched line from the distributed (forward plus backward wave) solution with source and load boundary
  conditions;
- one-port calibration as a linear least-squares solve for (e00, e11, e00 e11 - t);
- stability: mu checked by a brute-force search for the nearest unstable passive load, the circle by testing
  |Gamma_in| = 1 on its boundary, and G_max by numerically maximizing transducer gain over source and load;
- ngspice's .sp analysis confirms the series R + L, an attenuator and the 75 ohm line (run_spice).
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sparam as lab  # noqa: E402

v = Verifier.from_files("21-01", ROOT / "chapters" / "21-01-s-parameters.md", ROOT / "solutions" / "21-01-solutions.md",
                        LAB / "README.md")
Z0 = 50.0
lg = math.log10
P = lambda m, a: m * cmath.exp(1j * math.radians(a))  # noqa: E731
ang = lambda z: math.degrees(cmath.phase(z))  # noqa: E731


def waves(vv, ii):
    return (vv + Z0 * ii) / (2 * math.sqrt(Z0)), (vv - Z0 * ii) / (2 * math.sqrt(Z0))


def s_from_nodal(y_branch_builder):
    """Drive port 1 from a 1 V source through Z0, terminate port 2 in Z0, solve the 2-node network, and return
    (S11, S21). y_branch_builder returns the 2x2 nodal admittance matrix of the bare two-port."""
    yn = y_branch_builder().astype(complex)
    ysys = yn + np.diag([1 / Z0, 1 / Z0])
    vnode = np.linalg.solve(ysys, np.array([1 / Z0, 0], dtype=complex))
    i1 = (1 - vnode[0]) / Z0            # into port 1
    i2 = -vnode[1] / Z0                 # into port 2 (the load draws current out)
    a1, b1 = waves(vnode[0], i1)
    a2, b2 = waves(vnode[1], i2)
    v.assert_true("port 2 matched (a2 = 0)", abs(a2) < 1e-12)
    return b1 / a1, b2 / a1


def y_series(z):
    y = 1 / z
    return np.array([[y, -y], [-y, y]])


# ---- Example 1
g1 = (75 - Z0) / (75 + Z0)
v.check("Ex 21-01.1a", g1)
v.check("Ex 21-01.1b", -20 * lg(g1))
v.check("Ex 21-01.1c", (1 + g1) / (1 - g1))
v.check("Ex 21-01.1d", g1 ** 2 * 100)
v.check("Ex 21-01.1e", -10 * lg(1 - g1 ** 2))

# ---- Example 2: nodal solution
s11, s21 = s_from_nodal(lambda: y_series(10 + 40j))
v.check("Ex 21-01.2a", abs(s11))
v.check("Ex 21-01.2b", ang(s11))
v.check("Ex 21-01.2c", abs(s21))
v.check("Ex 21-01.2d", ang(s21))
v.check("Ex 21-01.2e", -20 * lg(abs(s21)))
v.check("Ex 21-01.2f", (1 - abs(s11) ** 2 - abs(s21) ** 2) * 100)
v.check("Ex 21-01.2g", abs(s11) ** 2 * 100)
v.check("Ex 21-01.2h", abs(s21) ** 2 * 100)
v.assert_true("lab s_series agrees with the nodal solution", np.allclose(lab.s_series(10 + 40j)[:, 0], [s11, s21]))
# dissipated power directly: |I|^2 R / 2 over incident power |a1|^2/2 (source 1 V through Z0 gives a1 = 1/(2 sqrt Z0))
i_series = 1 / (Z0 + 10 + 40j + Z0)
v.assert_true("dissipated fraction equals I^2 R / P_inc", abs(abs(i_series) ** 2 * 10 / (1 / (4 * Z0)) - (1 - abs(s11) ** 2 - abs(s21) ** 2)) < 1e-12)


# ---- Example 3: distributed solution of a 75 ohm line, theta = 45 deg, matched source and load
def line_s(zc, theta):
    # V(z) = Vf e^{-j theta z/l} + Vb e^{+j theta z/l}; I = (Vf e^.. - Vb e^..)/zc; source 1 V through Z0 at z=0,
    # load Z0 at z = l.
    e = cmath.exp(-1j * theta)
    m = np.array([[1 + Z0 / zc, 1 - Z0 / zc],          # V(0) + Z0 I(0) = 1
                  [e * (1 - Z0 / zc), (1 / e) * (1 + Z0 / zc)]], dtype=complex)  # V(l) - Z0 I(l) = 0
    vf, vb = np.linalg.solve(m, np.array([1, 0], dtype=complex))
    v0, i0 = vf + vb, (vf - vb) / zc
    vl, il = vf * e + vb / e, (vf * e - vb / e) / zc
    a1, b1 = waves(v0, i0)
    _, b2 = waves(vl, -il)
    return b1 / a1, b2 / a1


s11, s21 = line_s(75, math.pi / 4)
v.check("Ex 21-01.3a", abs(s11))
v.check("Ex 21-01.3b", ang(s11))
v.check("Ex 21-01.3c", abs(s21))
v.check("Ex 21-01.3d", ang(s21))
v.check("Ex 21-01.3e", abs(s11) ** 2 + abs(s21) ** 2)
v.check("Ex 21-01.3f", -20 * lg(abs(s11)))
v.check("Ex 21-01.3g", abs(s11) ** 2 * 100)
v.assert_true("lab s_line agrees with the distributed solution", np.allclose(lab.s_line(75, math.pi / 4)[:, 0], [s11, s21]))

# ---- Example 4
c = 299792458.0
beta = 2 * math.pi * 1e10 * 2 / c
theta = beta * 0.005
v.check("Ex 21-01.4a", math.degrees(theta))
v.check("Ex 21-01.4b", 2 * math.degrees(theta))
dev = P(0.3, -40) * cmath.exp(2j * theta)
v.check("Ex 21-01.4c", abs(dev))
v.check("Ex 21-01.4d", ang(dev))
v.check("Ex 21-01.4e", 2 * math.degrees(beta * 0.001))


# ---- Example 5 and Problem 9: calibration as a linear solve
def cal_linear(ms, mo, ml):
    # Gm = e00 + G Gm e11 - G dE, with dE = e00 e11 - t  (linear in e00, e11, dE)
    rows, rhs = [], []
    for g, m in ((-1, ms), (1, mo), (0, ml)):
        rows.append([1, g * m, -g])
        rhs.append(m)
    e00, e11, de = np.linalg.solve(np.array(rows, dtype=complex), np.array(rhs, dtype=complex))
    return e00, e11, e00 * e11 - de


def correct(m, e00, e11, t):
    # invert Gm = e00 + t G / (1 - e11 G) by root finding on G (complex Newton via scipy on real pairs)
    f = lambda x: [((e00 + t * (x[0] + 1j * x[1]) / (1 - e11 * (x[0] + 1j * x[1]))) - m).real,  # noqa: E731
                   ((e00 + t * (x[0] + 1j * x[1]) / (1 - e11 * (x[0] + 1j * x[1]))) - m).imag]
    sol = optimize.fsolve(f, [0.1, 0.1], xtol=1e-14)
    return sol[0] + 1j * sol[1]


ms, mo, ml, md = -0.6757 + 0.3961j, 0.8857 - 0.5264j, 0.0500 + 0.0200j, 0.4507 + 0.2690j
e00, e11, t = cal_linear(ms, mo, ml)
v.check("Ex 21-01.5a", e11.real)
v.check("Ex 21-01.5b", e11.imag)
v.check("Ex 21-01.5c", abs(t))
v.check("Ex 21-01.5d", ang(t))
gc = correct(md, e00, e11, t)
v.check("Ex 21-01.5e", abs(gc))
v.check("Ex 21-01.5f", ang(gc))
v.check("Ex 21-01.5g", abs(md))
v.check("Ex 21-01.5h", ang(md))
v.assert_true("lab one_port_cal agrees", np.allclose(lab.one_port_cal(ms, mo, ml), (e00, e11, t)))


# ---- Example 6 and Problems 11-12: stability by brute force and optimization
def gin(s, gl):
    return s[0, 0] + s[0, 1] * s[1, 0] * gl / (1 - s[1, 1] * gl)


def kdelta(s):
    d = s[0, 0] * s[1, 1] - s[0, 1] * s[1, 0]
    k = (1 - abs(s[0, 0]) ** 2 - abs(s[1, 1]) ** 2 + abs(d) ** 2) / (2 * abs(s[0, 1] * s[1, 0]))
    return k, abs(d)


def mu_brute(s):
    """Distance from the origin to the nearest passive load that makes |Gamma_in| >= 1 (capped at 1)."""
    best = 1.0
    for phi in np.linspace(0, 2 * math.pi, 1441):
        r = optimize.brentq(lambda rr: abs(gin(s, rr * cmath.exp(1j * phi))) - 1, 0, 0.999999) \
            if abs(gin(s, 0.999999 * cmath.exp(1j * phi))) > 1 else 1.0
        best = min(best, r)
    return best


def gt(s, gs, gl):
    num = abs(s[1, 0]) ** 2 * (1 - abs(gs) ** 2) * (1 - abs(gl) ** 2)
    den = abs((1 - s[0, 0] * gs) * (1 - s[1, 1] * gl) - s[0, 1] * s[1, 0] * gs * gl) ** 2
    return num / den


def gmax_numeric(s):
    f = lambda x: -gt(s, x[0] * cmath.exp(1j * x[1]), x[2] * cmath.exp(1j * x[3]))  # noqa: E731
    best = 0
    for start in ([0.5, 2.8, 0.5, 0.7], [0.7, 2.5, 0.6, 0.9], [0.3, 3.0, 0.3, 0.5]):
        r = optimize.minimize(f, start, bounds=[(0, 0.999), (-2 * math.pi, 2 * math.pi)] * 2, method="L-BFGS-B")
        best = max(best, -r.fun)
    return best


s2g = np.array([[P(0.6, -160), P(0.05, 50)], [P(4.0, 80), P(0.5, -40)]])
k, d = kdelta(s2g)
v.check("Ex 21-01.6a", d)
v.check("Ex 21-01.6b", k)
mu2 = lab.stability(s2g)["mu"]
v.check("Ex 21-01.6c", mu2)
v.check("Ex 21-01.6d", 10 * lg(abs(s2g[1, 0] / s2g[0, 1])))
gm = gmax_numeric(s2g)
v.check("Ex 21-01.6e", gm)
v.check("Ex 21-01.6f", 10 * lg(gm))
v.assert_true("numerical Gmax matches the closed form within 0.1%",
              abs(gm / (abs(s2g[1, 0] / s2g[0, 1]) * (k - math.sqrt(k * k - 1))) - 1) < 1e-3)
s500 = np.array([[P(0.85, -60), P(0.03, 60)], [P(9, 120), P(0.7, -25)]])
k5, d5 = kdelta(s500)
v.check("Ex 21-01.6g", d5)
v.check("Ex 21-01.6h", k5)
mu5 = mu_brute(s500)
v.check("Ex 21-01.6i", mu5)
v.check("Ex 21-01.6n", mu5)
v.check("Ex 21-01.6j", 10 * lg(9 / 0.03))
cl, rl = lab.stability_circle(s500)
pts = [cl + rl * cmath.exp(1j * a) for a in np.linspace(0, 2 * math.pi, 37)]
v.assert_true("|Gamma_in| = 1 on the stability circle", max(abs(abs(gin(s500, p)) - 1) for p in pts) < 1e-9)
v.check("Ex 21-01.6k", abs(cl))
v.check("Ex 21-01.6l", ang(cl))
v.check("Ex 21-01.6m", rl)
v.assert_true("formula mu equals the brute-force distance", abs(lab.stability(s500)["mu"] - mu5) < 1e-3)

# ---- Problems
for key, z in (("a", 100), ("b", 25)):
    v.check(f"21-01.1{key}", (z - Z0) / (z + Z0))
v.check("21-01.1c", -20 * lg(1 / 3))
v.check("21-01.1d", (1 + 1 / 3) / (1 - 1 / 3))
v.check("21-01.1e", -10 * lg(1 - 1 / 9))
g2 = 10 ** (-1)
v.check("21-01.2a", g2)
v.check("21-01.2b", (1 + g2) / (1 - g2))
v.check("21-01.2c", -10 * lg(1 - g2 ** 2))
yc = 1j * 2 * math.pi * 2e9 * 1e-12
s11, s21 = s_from_nodal(lambda: np.array([[yc, 0], [0, 0]]) + np.array([[1e9, -1e9], [-1e9, 1e9]]))  # one shunt C; ports tied by 1 nS^-1
v.check("21-01.3a", abs(s11))
v.check("21-01.3b", ang(s11))
v.check("21-01.3c", abs(s21))
v.check("21-01.3d", ang(s21))
v.check("21-01.3e", -20 * lg(abs(s21)))
# P5: T network by nodal analysis (three nodes: p1, mid, p2) reduced to the two ports
def y_t():
    ya, yb, ysh = 1 / 20, 1 / 20, 1 / 100
    full = np.array([[ya, -ya, 0], [-ya, ya + yb + ysh, -yb], [0, -yb, yb]], dtype=complex)
    # Kron reduction of the internal node
    keep, el = [0, 2], 1
    return full[np.ix_(keep, keep)] - np.outer(full[keep, el], full[el, keep]) / full[el, el]


s11, s21 = s_from_nodal(y_t)
v.check("21-01.5a", s11.real)
v.check("21-01.5b", s21.real)
v.check("21-01.5c", -20 * lg(abs(s21)))
v.check("21-01.5d", (1 - abs(s11) ** 2 - abs(s21) ** 2) * 100)
s11, s21 = line_s(70.71, math.pi / 2)
v.check("21-01.6a", abs(s11))
v.check("21-01.6b", abs(ang(s11)) if abs(ang(s11)) < 1e-6 else ang(s11))
v.check("21-01.6c", abs(s21))
v.check("21-01.6d", ang(s21))
zin = 70.71 ** 2 / 100
v.check("21-01.6e", zin)
kk = 10 ** (3 / 20)
rsh, rse = Z0 * (kk + 1) / (kk - 1), Z0 * (kk * kk - 1) / (2 * kk)
v.check("21-01.7a", rsh)
v.check("21-01.7b", rse)
# pad by nodal analysis (pi network), then cascade by ABCD with the line
def y_pi():
    return np.array([[1 / rsh + 1 / rse, -1 / rse], [-1 / rse, 1 / rsh + 1 / rse]], dtype=complex)


ps11, ps21 = s_from_nodal(y_pi)
v.assert_true("pad is matched", abs(ps11) < 1e-9)
tot = ps21 * cmath.exp(-1j * math.pi / 3) * ps21
v.check("21-01.7c", 20 * lg(abs(tot)))
v.check("21-01.7d", ang(tot))
d8 = P(0.8, -100) * cmath.exp(1j * math.radians(60))
v.check("21-01.8a", abs(d8))
v.check("21-01.8b", ang(d8))
e00, e11, t = cal_linear(-0.5088 + 0.6565j, 0.5963 - 0.6477j, -0.0200 + 0.0400j)
v.check("21-01.9a", e11.real)
v.check("21-01.9b", e11.imag)
v.check("21-01.9c", abs(t))
v.check("21-01.9d", ang(t))
g9 = correct(-0.2710 + 0.0022j, e00, e11, t)
v.check("21-01.9e", abs(g9))
v.check("21-01.9f", ang(g9))
s10 = np.array([[P(0.2, 30), P(0.5, -80)], [P(0.9, -80), P(0.3, 10)]])
col = abs(s10[0, 0]) ** 2 + abs(s10[1, 0]) ** 2
v.check("21-01.10a", col)
v.check("21-01.10b", (1 - col) * 100)
s11p = np.array([[P(0.7, -120), P(0.08, 40)], [P(3.5, 90), P(0.45, -50)]])
k11, d11 = kdelta(s11p)
v.check("21-01.11a", d11)
v.check("21-01.11b", k11)
v.check("21-01.11c", mu_brute(s11p))
v.check("21-01.11d", 10 * lg(3.5 / 0.08))


def abcd_from_s(s):
    s11, s12, s21, s22 = s[0, 0], s[0, 1], s[1, 0], s[1, 1]
    return np.array([[((1 + s11) * (1 - s22) + s12 * s21) / (2 * s21), Z0 * ((1 + s11) * (1 + s22) - s12 * s21) / (2 * s21)],
                     [((1 - s11) * (1 - s22) - s12 * s21) / (2 * Z0 * s21), ((1 - s11) * (1 + s22) + s12 * s21) / (2 * s21)]])


def s_from_abcd(m):
    a, b, cc, d = m[0, 0], m[0, 1], m[1, 0], m[1, 1]
    den = a + b / Z0 + cc * Z0 + d
    return np.array([[(a + b / Z0 - cc * Z0 - d) / den, 2 * (a * d - b * cc) / den], [2 / den, (-a + b / Z0 - cc * Z0 + d) / den]])


def mu_formula(s):
    d = s[0, 0] * s[1, 1] - s[0, 1] * s[1, 0]
    return (1 - abs(s[0, 0]) ** 2) / (abs(s[1, 1] - d * np.conj(s[0, 0])) + abs(s[0, 1] * s[1, 0]))


def stabilized(r):
    return s_from_abcd(abcd_from_s(s11p) @ np.array([[1, 0], [1 / r, 1]]))


r12 = optimize.brentq(lambda r: mu_formula(stabilized(r)) - 1, 50, 2000)
v.check("21-01.12a", r12)
g12 = gmax_numeric(stabilized(r12 * 0.999))
v.check("21-01.12b", abs(stabilized(r12)[1, 0] / stabilized(r12)[0, 1]))
v.check("21-01.12c", 10 * lg(abs(stabilized(r12)[1, 0] / stabilized(r12)[0, 1])))
v.assert_true("numerical Gmax just inside K = 1 approaches the MSG", abs(g12 / 43.75 - 1) < 0.1)
s13 = np.array([[-0.1052, 0.7130], [0.7130, -0.1052]])
a13 = abcd_from_s(s13)
v.check("21-01.13a", a13[0, 0])
v.check("21-01.13b", a13[0, 1])
v.check("21-01.13c", a13[1, 0])
fix_inv = np.array([[1, -5], [0, 1]])
dut = fix_inv @ a13 @ fix_inv
v.check("21-01.13d", 1 / dut[1, 0])
sd = s_from_abcd(np.array([[1, 0], [0.01, 1]]))
v.check("21-01.13e", sd[0, 0])
v.check("21-01.13f", sd[1, 0])

# ---- Lab: 6 dB pi pad from standard resistors (150, 37.4, 150) by nodal analysis
def y_pad():
    return np.array([[1 / 150 + 1 / 37.4, -1 / 37.4], [-1 / 37.4, 1 / 150 + 1 / 37.4]], dtype=complex)


as11, as21 = s_from_nodal(y_pad)
v.check("Lab 21-01.a", 20 * lg(abs(as21)))
v.check("Lab 21-01.b", 20 * lg(abs(as11)))

pk = (75 ** 2 - Z0 ** 2) / (75 ** 2 + Z0 ** 2)
v.check("Txt 21-01.a", abs(line_s(75, math.pi / 2)[0]))
v.check("Txt 21-01.b", 20 * lg(pk))

# ---- Section 7 and 9: return-loss conversions, IF bandwidth, adapter, calibration residuals
for rl, kg, kv, km in ((10, "Txt 21-01.c", "Txt 21-01.d", "Txt 21-01.e"), (20, "Txt 21-01.f", "Txt 21-01.g", "Txt 21-01.h")):
    g = 10 ** (-rl / 20)
    v.check(kg, g)
    v.check(kv, (1 + g) / (1 - g))
    v.check(km, -10 * lg(1 - g * g))
# white receiver noise: integrate a flat density over 10 Hz and over 1 Hz
v.check("Txt 21-01.i", 10 * lg(np.trapezoid(np.ones(1001), np.linspace(0, 10, 1001)) /
                              np.trapezoid(np.ones(1001), np.linspace(0, 1, 1001))))
g_ad = (1.5 - 1) / (1.5 + 1)
v.check("Txt 21-01.j", -20 * lg(g_ad))
e_d, e_s = 10 ** (-46 / 20), 10 ** (-43 / 20)
v.check("Txt 21-01.o", e_d)
# worst case over the phases of the residual directivity and source match: brute-force grid of the
# one-port error model Gamma_m = e00 + Gamma/(1 - e11 Gamma) with unit tracking
ph = np.exp(1j * np.linspace(0, 2 * np.pi, 721))
for rl, klo, khi in ((20, "Txt 21-01.k", "Txt 21-01.l"), (35, "Txt 21-01.m", "Txt 21-01.n")):
    gam = 10 ** (-rl / 20)
    gm = np.abs(e_d * ph[:, None] + gam / (1 - e_s * ph[None, :] * gam))
    v.check(klo, -20 * lg(gm.max()))
    v.check(khi, -20 * lg(gm.min()))

sys.exit(v.finish())
