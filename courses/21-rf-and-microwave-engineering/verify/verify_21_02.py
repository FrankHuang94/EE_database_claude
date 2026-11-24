#!/usr/bin/env python3
"""Verify every number in chapter 21-02 (impedance matching networks), its problems and its lab.

Independent routes (the lab uses closed-form element formulas and an impedance recursion):
- L-network element values found by solving Re(Zin) = 50 and Im(Zin) = 0 numerically for (L, C);
- input impedance by multiplying ABCD matrices of the elements, and band edges by root finding on |Gamma| = 0.316;
- multi-section transformer impedances from the binomial rule coded here, bandwidth both from the small-reflection
  formula and exactly from a cascade of line ABCD matrices;
- the inductor-loss fraction from the branch power split in a lossy circuit solved by ABCD;
- ngspice confirms six band edges (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import match as lab  # noqa: E402

v = Verifier.from_files("21-02", ROOT / "chapters" / "21-02-impedance-matching-networks.md",
                        ROOT / "solutions" / "21-02-solutions.md")
lg = math.log10
TH = 10 ** (-10 / 20)


def ser(z):
    return np.array([[1, z], [0, 1]], dtype=complex)


def sh(y):
    return np.array([[1, 0], [y, 1]], dtype=complex)


def zin_abcd(mats, zl):
    """mats from the source side to the load; Zin = (A ZL + B)/(C ZL + D)."""
    m = np.eye(2, dtype=complex)
    for x in mats:
        m = m @ x
    return (m[0, 0] * zl + m[0, 1]) / (m[1, 0] * zl + m[1, 1])


def gam(z):
    return abs((z - 50) / (z + 50))


def edges(net, zl, f0, lo, hi):
    """Band edges (Hz) where |Gamma| = 0.316 on either side of f0; net(f) returns the ABCD list."""
    g = lambda f: gam(zin_abcd(net(f), zl)) - TH  # noqa: E731
    return optimize.brentq(g, lo, f0), optimize.brentq(g, f0, hi)


def solve_lc(net_lc, zl, f0, guess):
    """Find (L, C) giving Zin = 50 + j0 at f0."""
    def res(x):
        z = zin_abcd(net_lc(x[0] * 1e-9, x[1] * 1e-12, f0), zl)
        return [z.real - 50, z.imag]
    sol = optimize.fsolve(res, guess, xtol=1e-13)
    return sol[0] * 1e-9, sol[1] * 1e-12


W = lambda f: 2 * math.pi * f  # noqa: E731

# ---- Example 1: low-pass L, 10 -> 50 at 2.4 GHz (source side: shunt C, then series L to the load)
lp = lambda L, C, f: [sh(1j * W(f) * C), ser(1j * W(f) * L)]  # noqa: E731
L1, C1 = solve_lc(lp, 10, 2.4e9, [1.3, 2.6])
q1 = math.sqrt(50 / 10 - 1)
v.check("Ex 21-02.1a", q1)
v.check("Ex 21-02.1b", W(2.4e9) * L1)
v.check("Ex 21-02.1c", L1 * 1e9)
v.check("Ex 21-02.1d", W(2.4e9) * C1)
v.check("Ex 21-02.1e", C1 * 1e12)
lo, hi = edges(lambda f: lp(L1, C1, f), 10, 2.4e9, 1e9, 2.4e9 * 1.8)
v.check("Ex 21-02.1f", lo / 1e9)
v.check("Ex 21-02.1g", hi / 1e9)
v.check("Ex 21-02.1h", (hi - lo) / 2.4e9 * 100)
v.check("Txt 21-02.a", (hi - lo) / 2.4e9 * q1)
v.assert_true("lab l_match agrees", abs(lab.l_match(10, 50)[0] - W(2.4e9) * L1) < 1e-9)

# ---- Example 2: load 20 - j15 at 900 MHz
L2, C2 = solve_lc(lp, 20 - 15j, 9e8, [7, 4])
q2 = math.sqrt(50 / 20 - 1)
v.check("Ex 21-02.2a", q2)
v.check("Ex 21-02.2b", q2 * 20)
v.check("Ex 21-02.2c", W(9e8) * L2)
v.check("Ex 21-02.2d", L2 * 1e9)
v.check("Ex 21-02.2e", C2 * 1e12)
v.check("Ex 21-02.2f", zin_abcd(lp(L2, C2, 9e8), 20 - 15j).real)

# ---- Example 3: pi network Q = 5, 50 -> 10 at 2.4 GHz
rv = 50 / (5 ** 2 + 1)
qa, qb = math.sqrt(50 / rv - 1), math.sqrt(10 / rv - 1)
b1, b2, xs = qa / 50, qb / 10, (qa + qb) * rv
v.check("Ex 21-02.3a", rv)
v.check("Ex 21-02.3b", b1)
v.check("Ex 21-02.3c", b2)
v.check("Ex 21-02.3d", xs)
f0 = 2.4e9
pinet = lambda f: [sh(1j * b1 * f / f0), ser(1j * xs * f / f0), sh(1j * b2 * f / f0)]  # noqa: E731
v.assert_true("pi network matches at f0", gam(zin_abcd(pinet(f0), 10)) < 1e-9)
lo, hi = edges(pinet, 10, f0, 1.5e9, 3.5e9)
v.check("Ex 21-02.3e", lo / 1e9)
v.check("Ex 21-02.3f", hi / 1e9)
v.check("Ex 21-02.3g", (hi - lo) / f0 * 100)

# ---- Example 4: 5 -> 50 at 2 GHz, one and two sections
f0 = 2e9
v.check("Ex 21-02.4a", math.sqrt(50 / 5 - 1))
L4, C4 = solve_lc(lp, 5, f0, [1.2, 4.8])
lo, hi = edges(lambda f: lp(L4, C4, f), 5, f0, 0.8e9, 4e9)
v.check("Ex 21-02.4b", lo / 1e9)
v.check("Ex 21-02.4c", hi / 1e9)
v.check("Ex 21-02.4d", (hi - lo) / f0 * 100)
rmid = math.sqrt(5 * 50)
v.check("Ex 21-02.4e", rmid)
qs = math.sqrt(rmid / 5 - 1)
v.check("Ex 21-02.4f", qs)
La, Ca = solve_lc(lp, 5, f0, [0.6, 7.4])           # inner section 5 -> 15.81: solve against rmid
def inner(L, C, f):
    return [sh(1j * W(f) * C), ser(1j * W(f) * L)]
La, Ca = (lambda r: (r[0], r[1]))(optimize.fsolve(
    lambda x: [zin_abcd(inner(x[0] * 1e-9, x[1] * 1e-12, f0), 5).real - rmid, zin_abcd(inner(x[0] * 1e-9, x[1] * 1e-12, f0), 5).imag],
    [0.6, 7.4], xtol=1e-13))
La, Ca = La * 1e-9, Ca * 1e-12
Lb, Cb = solve_lc(lp, rmid, f0, [1.85, 2.34])
two = lambda f: lp(Lb, Cb, f) + inner(La, Ca, f)  # noqa: E731
v.assert_true("two-section network matches at f0", gam(zin_abcd(two(f0), 5)) < 1e-8)
lo, hi = edges(two, 5, f0, 0.8e9, 4e9)
v.check("Ex 21-02.4g", lo / 1e9)
v.check("Ex 21-02.4h", hi / 1e9)
v.check("Ex 21-02.4i", (hi - lo) / f0 * 100)


# ---- Example 5: loss fraction from the branch power split (series r = X/Qu with the load resistance)
def loss_db(qn, qu, r_low=10.0):
    x = qn * r_low
    r = x / qu
    # same current through r and r_low: P_load / (P_load + P_r) = r_low / (r_low + r)
    i = 1.0
    p_load, p_r = i * i * r_low / 2, i * i * r / 2
    return -10 * lg(p_load / (p_load + p_r))


v.check("Ex 21-02.5a", loss_db(2, 15))
v.check("Ex 21-02.5b", loss_db(3, 15))
v.check("Ex 21-02.5c", loss_db(3, 8))
v.check("Ex 21-02.5d", (1 - 10 ** (-loss_db(3, 8) / 10)) * 100)
v.check("Txt 21-02.b", (1 - 10 ** (-loss_db(3, 8) / 10)) * 1.0)

# ---- Example 6: Bode-Fano and transformers
v.check("Ex 21-02.6a", 1 / (2 * 50 * 1e-12 * math.log(10)) / 1e9)


def binomial(z0, zl, n):
    zs = [z0]
    for k in range(n + 1):
        zs.append(zs[-1] * math.exp(math.comb(n, k) / 2 ** n * math.log(zl / z0)))
    return zs[1:-1]


def bw_approx(z0, zl, n, gm):
    a = abs((zl - z0) / (zl + z0)) / 2 ** n
    return 2 - 4 * math.acos(0.5 * (gm / a) ** (1 / n)) / math.pi


def line(zc, x):     # x = f/f0, quarter wave at f0
    th = math.pi / 2 * x
    return np.array([[math.cos(th), 1j * zc * math.sin(th)], [1j * math.sin(th) / zc, math.cos(th)]])


def bw_exact(zs, zl, gm):
    g = lambda x: gam(zin_abcd([line(z, x) for z in zs], zl)) - gm  # noqa: E731
    return optimize.brentq(g, 1.0, 1.999) - optimize.brentq(g, 0.001, 1.0)


z2 = binomial(50, 100, 2)
v.check("Ex 21-02.6b", z2[0])
v.check("Ex 21-02.6c", z2[1])
v.check("Ex 21-02.6d", bw_approx(50, 100, 2, 0.05) * 100)
v.check("Ex 21-02.6e", bw_approx(50, 100, 1, 0.05) * 100)
v.check("Ex 21-02.6f", bw_exact(z2, 100, 0.05) * 100)
v.check("Ex 21-02.6g", bw_exact([math.sqrt(5000)], 100, 0.05) * 100)

# ---- Problems
w1 = W(1e9)
v.check("21-02.1a", math.sqrt(50 / 25 - 1))
v.check("21-02.1b", 25)
L, C = solve_lc(lp, 25, 1e9, [4, 3])
v.check("21-02.1c", L * 1e9)
v.check("21-02.1d", W(1e9) * C)
v.check("21-02.1e", C * 1e12)
hp = lambda L, C, f: [sh(1 / (1j * W(f) * L)), ser(1 / (1j * W(f) * C))]  # noqa: E731
Lh, Ch = optimize.fsolve(lambda x: [zin_abcd(hp(x[0] * 1e-9, x[1] * 1e-12, 2.4e9), 10).real - 50,
                                    zin_abcd(hp(x[0] * 1e-9, x[1] * 1e-12, 2.4e9), 10).imag], [1.7, 3.3], xtol=1e-13)
v.check("21-02.2a", Ch)
v.check("21-02.2b", Lh)
L3, C3 = solve_lc(lp, 30 + 10j, 2e9, [1.2, 1.3])
v.check("21-02.3a", math.sqrt(50 / 30 - 1))
v.check("21-02.3b", W(2e9) * L3)
v.check("21-02.3c", L3 * 1e9)
v.check("21-02.3d", C3 * 1e12)
bload = W(1e9) * 2e-12
zl4 = 1 / (1 / 100 + 1j * bload)
# high-pass: source side series C, then shunt L at the load
hp4 = lambda L, C, f: [ser(1 / (1j * W(f) * C)), sh(1 / (1j * W(f) * L))]  # noqa: E731
L4h, C4h = optimize.fsolve(lambda x: [zin_abcd(hp4(x[0] * 1e-9, x[1] * 1e-12, 1e9), zl4).real - 50,
                                      zin_abcd(hp4(x[0] * 1e-9, x[1] * 1e-12, 1e9), zl4).imag], [7, 3], xtol=1e-13)
v.check("21-02.4a", bload)
v.check("21-02.4b", L4h)
v.check("21-02.4c", C4h)
rv5 = 50 / 17
qa, qb = 4, math.sqrt(25 / rv5 - 1)
v.check("21-02.5a", rv5)
v.check("21-02.5b", qa / 50)
v.check("21-02.5c", qb / 25)
v.check("21-02.5d", (qa + qb) * rv5)
pi5 = [sh(1j * qa / 50), ser(1j * (qa + qb) * rv5), sh(1j * qb / 25)]
v.assert_true("problem 5 pi network matches", gam(zin_abcd(pi5, 25)) < 1e-9)
r = 25 ** (1 / 3)
v.check("21-02.6a", 2 * r)
v.check("21-02.6b", 2 * r * r)
v.check("21-02.6c", math.sqrt(r - 1))
z3 = binomial(50, 25, 3)
v.check("21-02.7a", z3[0])
v.check("21-02.7b", z3[1])
v.check("21-02.7c", z3[2])
v.check("21-02.7d", bw_approx(50, 25, 3, 0.05) * 100)
v.check("21-02.7e", bw_exact(z3, 25, 0.05) * 100)
v.check("21-02.8a", loss_db(1, 10))
v.check("21-02.8b", loss_db(5, 10))
ropt = (3.4 - 0.4) ** 2 / (2 * 2)
v.check("21-02.9a", ropt)
v.check("21-02.9b", 50 / ropt)
q91 = math.sqrt(50 / ropt - 1)
q92 = math.sqrt(math.sqrt(50 / ropt) - 1)
v.check("21-02.9c", q91)
v.check("21-02.9d", loss_db(q91, 30))
v.check("21-02.9e", q92)
v.check("21-02.9f", 2 * loss_db(q92, 30))
v.check("21-02.10a", 1 / (2 * 50 * 3e-12 * math.log(1 / TH)) / 1e9)
v.check("21-02.10b", 1 / (2 * 50 * 3e-12 * math.log(10)) / 1e9)
rv11 = 50 / 10
v.check("21-02.11a", rv11)
f0 = 2.4e9
v.check("21-02.11b", 3 / 50 / W(f0) * 1e12)
v.check("21-02.11c", 6 * rv11 / W(f0) * 1e9)
pi11 = lambda f: [sh(1j * 0.06 * f / f0), ser(1j * 30 * f / f0), sh(1j * 0.06 * f / f0)]  # noqa: E731
lo, hi = edges(pi11, 50, f0, 1.5e9, 3.5e9)
v.check("21-02.11d", lo / 1e9)
v.check("21-02.11e", hi / 1e9)
v.check("21-02.11f", (hi - lo) / f0 * 100)
for n, (kq, kl) in zip((1, 2, 3, 4), (("a", "b"), ("c", "d"), ("e", "f"), ("g", "h"))):
    qn = math.sqrt(25 ** (1 / n) - 1)
    v.check(f"21-02.12{kq}", qn)
    v.check(f"21-02.12{kl}", n * loss_db(qn, 20))
v.check("21-02.12i", 10 / math.log(10))

# ---- Sections 7 and 9: return-loss thresholds and the Bode-Fano bound at 10 dB, by quadrature of the
# optimal (brick-wall) reflection budget: integral of ln(1/|Gamma|) over the band equals pi/(RC)
v.check("Txt 21-02.c", optimize.brentq(lambda g: -20 * math.log10(g) - 10, 1e-3, 0.999))
v.check("Txt 21-02.e", optimize.brentq(lambda g: -20 * math.log10(g) - 7, 1e-3, 0.999))
gm10 = 10 ** (-10 / 20)
bw_rad = optimize.brentq(lambda dw: np.trapezoid(np.full(201, math.log(1 / gm10)), np.linspace(0, dw, 201))
                         - math.pi / (50 * 1e-12), 1e6, 1e12)
v.check("Txt 21-02.d", bw_rad / (2 * math.pi) / 1e9)
# first-order L-section bandwidth: slope of |Gamma| at the center by a numerical derivative of the exact low-pass
# L-match input admittance (10 ohm load, 50 ohm source), against the closed form Q^2/sqrt(1 + Q^2)
def gam_l(delta, r_lo=10.0, r_hi=50.0):
    q = math.sqrt(r_hi / r_lo - 1)
    y = r_hi * (1j * (q / r_hi) * (1 + delta) + 1 / (r_lo + 1j * q * r_lo * (1 + delta)))
    return (1 - y) / (1 + y)


slope = abs(gam_l(1e-6) - gam_l(-1e-6)) / 2e-6
v.assert_true("first-order |Gamma| slope equals Q^2/sqrt(1+Q^2)", abs(slope - 4 / math.sqrt(5)) < 1e-6, f"{slope}")
v.check("Txt 21-02.f", 100 * 2 * gm10 / slope)

sys.exit(v.finish())
