#!/usr/bin/env python3
"""Verify chapter 15-06 (root locus): examples, problems and lab answers.

Routes:
- the sketching rules from labs/15-06-lab/rlocus.py (closed forms);
- every rule's prediction checked against closed-loop roots from numpy (breakpoints are double roots, design points
  are roots at the computed gain, crossings are roots on the axis);
- gains at points from the magnitude condition, cross-checked by substituting into the characteristic polynomial;
- step-response numbers from labs/15-03-lab/specs.py; the PD servo is confirmed in ngspice (pd_servo.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "15-06-lab"))
sys.path.insert(0, str(ROOT / "labs" / "15-03-lab"))
from eeverify import Verifier  # noqa: E402
import rlocus as rl  # noqa: E402
from specs import step_specs  # noqa: E402

CH = ROOT / "chapters" / "15-06-root-locus.md"
v = Verifier.from_files("15-06", CH, ROOT / "solutions" / "15-06-solutions.md", ROOT / "labs" / "15-06-lab" / "README.md")


def roots_at(N, D, K):
    return np.roots(rl.char_poly(N, D, K))


def is_root(N, D, K, s0, tol=1e-6):
    return abs(np.polyval(rl.char_poly(N, D, K), s0)) < tol * max(1.0, abs(np.polyval(D, s0)))


def double_root(N, D, K, x, tol=1e-5):
    r = roots_at(N, D, K)
    return np.sum(np.abs(r - x) < tol * max(1.0, abs(x))) >= 2


def crossing(N, D, lo, hi):
    K = brentq(lambda k: np.max(roots_at(N, D, k).real), lo, hi, xtol=1e-12)
    r = roots_at(N, D, K)
    return K, float(np.max(np.abs(r[np.argsort(np.abs(r.real))[:2]].imag)))


# ---------------------------------------------------------------------------------------- Example 1
N1, D1 = [1], [1, 4, 0]
(bx, bk), = rl.breakpoints(N1, D1)
v.check("Ex 15-06.1a", bx)
v.check("Ex 15-06.1b", bk)
v.assert_true("Ex 1: double root at the breakaway", double_root(N1, D1, bk, bx))
s0 = complex(-2, 2)
v.check("Ex 15-06.1c", rl.gain_at(N1, D1, s0))
v.assert_true("Ex 1: -2+j2 is a root at K = 8", is_root(N1, D1, 8, s0))

# ---------------------------------------------------------------------------------------- Example 2
N2, D2 = [1], [1, 6, 8, 0]
v.check("Ex 15-06.2a", rl.asymptotes(N2, D2)[1])
(bx, bk), = rl.breakpoints(N2, D2)
v.check("Ex 15-06.2b", bx)
v.check("Ex 15-06.2c", bk)
v.assert_true("Ex 2: double root at the breakaway", double_root(N2, D2, bk, bx))
Kc, wc = crossing(N2, D2, 10, 100)
v.check("Ex 15-06.2d", wc)
v.assert_true("Ex 2: crossing gain 48", abs(Kc - 48) < 1e-8)
(sz, Kz), = rl.zeta_point(N2, D2, 0.5, 5)
v.check("Ex 15-06.2e", sz)
v.check("Ex 15-06.2f", Kz)
v.assert_true("Ex 2: K = 224/27 exactly", abs(Kz - 224 / 27) < 1e-9)
r = roots_at(N2, D2, Kz)
third = float(r[np.argmin(abs(r.imag))].real)
v.check("Ex 15-06.2g", third)
v.assert_true("Ex 2: constant sum", abs(2 * sz.real + third + 6) < 1e-9)
v.check("Ex 15-06.2h", 100 * step_specs([Kz], rl.char_poly(N2, D2, Kz), 20)["overshoot"])

# ---------------------------------------------------------------------------------------- Example 3
N3, D3 = [1, 1], [1, 6, 8, 0]
v.check("Ex 15-06.3a", rl.asymptotes(N3, D3)[1])
(bx, bk), = rl.breakpoints(N3, D3)
v.check("Ex 15-06.3b", bx)
v.check("Ex 15-06.3c", bk)
v.assert_true("Ex 3: double root at the breakaway", double_root(N3, D3, bk, bx))
(sz, Kz), = rl.zeta_point(N3, D3, 0.5, 10)
v.check("Ex 15-06.3d", sz)
v.check("Ex 15-06.3e", Kz)
v.assert_true("Ex 3: stable from K = 0.01 to 1e5",
              all(np.max(roots_at(N3, D3, k).real) < 0 for k in np.logspace(-2, 5, 300)))

# ---------------------------------------------------------------------------------------- Example 4
N4, D4 = [1, 2], [1, 2, 5]
v.check("Ex 15-06.4a", rl.departure_angle(N4, D4, complex(-1, 2)))
(bx, bk), = rl.breakpoints(N4, D4)
v.check("Ex 15-06.4b", bx)
v.check("Ex 15-06.4c", bk)
rad = abs(complex(-1, 2) - (-2))
v.check("Ex 15-06.4d", rad)
v.assert_true("Ex 4: complex branch points lie on the circle about -2",
              all(abs(abs(c - (-2)) - rad) < 1e-9 for k in np.linspace(0.1, 6.4, 50)
                  for c in roots_at(N4, D4, k) if abs(c.imag) > 1e-6))
# numerical departure: direction of the branch for a tiny K
eps = 1e-6
rr = roots_at(N4, D4, eps)
c = rr[np.argmax(rr.imag)]
v.assert_true("Ex 4: numerical departure direction matches",
              abs(math.degrees(np.angle(c - complex(-1, 2))) - rl.departure_angle(N4, D4, complex(-1, 2))) < 0.01)

# ---------------------------------------------------------------------------------------- Example 5
tz, tp = 5e-6, 5e-6 / 11
N5, D5 = [tz, 1], [tp, 1, 0, 0]
bps = rl.breakpoints(N5, D5)
(x1, k1), (x2, k2) = sorted(bps, reverse=True)
v.check("Ex 15-06.5a", x1)
v.check("Ex 15-06.5b", k1)
v.check("Ex 15-06.5c", x2)
v.check("Ex 15-06.5d", k2)
v.assert_true("Ex 5: all three poles real between the two gains",
              np.all(np.abs(roots_at(N5, D5, 0.5 * (k1 + k2)).imag) < 1e-6))
r = roots_at(N5, D5, 1e11 / 1.1)
c = r[np.argmax(r.imag)]
v.check("Ex 15-06.5e", -c.real / abs(c))
rr_ = sp.symbols("r", positive=True)
v.assert_true("Ex 5: real meeting points need tau_z/tau_p > 9",
              sp.solve(sp.Eq((3 + rr_) ** 2 - 16 * rr_, 0), rr_) == [1, 9])

# ---------------------------------------------------------------------------------------- Example 6
v.check("Ex 15-06.6a", step_specs([8], [1, 4, 8], 10)["settle"])
N6, D6 = [1, 8], [1, 4, 0]
v.check("Ex 15-06.6b", math.sqrt(8 * 4))
def min_zeta(N, D, k_lo, k_hi):
    """Brute-force search over K for the complex pair's smallest damping; returns (zeta, K, root)."""
    def z_of(k):
        r = roots_at(N, D, k)
        c = r[np.argmax(r.imag)]
        return -c.real / abs(c) if c.imag > 1e-9 else 1.0
    ks = np.linspace(k_lo, k_hi, 4001)
    zs = [z_of(k) for k in ks]
    i = int(np.argmin(zs))
    res = minimize_scalar(z_of, bounds=(ks[max(i - 1, 0)], ks[min(i + 1, len(ks) - 1)]), method="bounded",
                          options={"xatol": 1e-12})
    r = roots_at(N, D, res.x)
    return res.fun, res.x, r[np.argmax(r.imag)]


z6, k6min, s6 = min_zeta([1, 8], [1, 4, 0], 0.5, 60)
v.assert_true("Ex 6: brute-force minimum damping is 0.707 at K = 4", abs(z6 - 1 / math.sqrt(2)) < 1e-6 and abs(k6min - 4) < 1e-4)
v.check("Ex 15-06.6c", s6.real)
s6 = complex(round(s6.real, 6), round(s6.imag, 6))
K6 = rl.gain_at(N6, D6, s6)
v.check("Ex 15-06.6d", K6)
v.assert_true("Ex 6: double root of zeta(K) at K = 4 (tangency)",
              abs(sp.solve(sp.Eq((4 + sp.Symbol("k")) ** 2, 16 * sp.Symbol("k")), sp.Symbol("k"))[0] - 4) < 1e-12)
v.assert_true("Ex 6: -4+j4 is a closed-loop root", is_root(N6, D6, K6, s6))
r6 = step_specs([4, 32], [1, 8, 32], 5)
v.check("Ex 15-06.6e", 100 * r6["overshoot"])
v.check("Ex 15-06.6f", r6["settle"])
zmin = min(-c.real / abs(c) for k in np.linspace(0.7, 23, 4000) for c in roots_at(N6, D6, k) if c.imag > 1e-9)
v.assert_true("Ex 6: smallest damping on the circle is 0.707", abs(zmin - 1 / math.sqrt(2)) < 1e-4)

# ---------------------------------------------------------------------------------------- Problem 1
N, D = [1, 3], np.polymul([1, 0], np.polymul([1, 1], np.polymul([1, 5], [1, 6])))
v.check("15-06.1a", rl.asymptotes(N, D)[1])
v.assert_true("P1: segments [-1,0], [-5,-3], (-inf,-6]",
              [tuple(round(x, 9) for x in sgm) for sgm in rl.real_axis_segments(N, D, lo=-1e6)] == [(-1.0, 0.0), (-5.0, -3.0), (-1e6, -6.0)])

# ---------------------------------------------------------------------------------------- Problem 2
D = np.polymul([1, 0], np.polymul([1, 4], [1, 6]))
v.check("15-06.2a", math.degrees(np.angle(1 / np.polyval(D, complex(-2, 2)))))
Kc, wc = crossing([1], D, 50, 500)
v.check("15-06.2b", Kc)
v.check("15-06.2c", wc)

# ---------------------------------------------------------------------------------------- Problem 3
(bx, bk), = rl.breakpoints([1], [1, 4, 3])
v.check("15-06.3a", bx)
v.check("15-06.3b", bk)

# ---------------------------------------------------------------------------------------- Problem 4
D = np.polymul([1, 0], np.polymul([1, 1], [1, 5]))
v.check("15-06.4a", rl.asymptotes([1], D)[1])
(bx, bk), = rl.breakpoints([1], D)
v.check("15-06.4b", bx)
v.check("15-06.4c", bk)
Kc, wc = crossing([1], D, 5, 100)
v.check("15-06.4d", Kc)
v.check("15-06.4e", wc)

# ---------------------------------------------------------------------------------------- Problem 5
D = np.polymul([1, 3], [1, 2, 2])
dep = rl.departure_angle([1, 2], D, complex(-1, 1))
v.check("15-06.5a", dep)
rr = roots_at([1, 2], D, 1e-7)
c = rr[np.argmin(abs(rr - complex(-1, 1)))]
v.assert_true("P5: numerical departure direction", abs(math.degrees(np.angle(c - complex(-1, 1))) - dep) < 0.01)

# ---------------------------------------------------------------------------------------- Problem 6
D = np.polymul([1, 0], np.polymul([1, 2], [1, 10]))
(sz, Kz), = rl.zeta_point([1], D, 0.6, 10)
v.check("15-06.6a", sz)
v.check("15-06.6b", Kz)
r = roots_at([1], D, Kz)
v.check("15-06.6c", float(r[np.argmin(abs(r.imag))].real))

# ---------------------------------------------------------------------------------------- Problem 7
D = np.polymul([1, 0], np.polymul([1, 4], [1, 10]))
Kc, wc = crossing([1], D, 100, 2000)
v.check("15-06.7a", Kc)
v.check("15-06.7b", wc)
v.assert_true("P7: two-pole loop stable for all K", all(np.max(roots_at([1], [1, 4, 0], k).real) < 0 for k in np.logspace(-2, 6, 50)))

# ---------------------------------------------------------------------------------------- Problem 8
K8 = brentq(lambda k: max(c.real for c in roots_at([1], [1, 6, 8, 0], k) if abs(c.imag) > 1e-9) + 0.5, 4, 40)
r = roots_at([1], [1, 6, 8, 0], K8)
v.check("15-06.8a", float(r[np.argmin(abs(r.imag))].real))
v.check("15-06.8b", K8)

# ---------------------------------------------------------------------------------------- Problem 9
N9, D9 = [1, 6], [1, 2, 0]
rho = math.sqrt(24)
v.check("15-06.9a", rho)
v.assert_true("P9: angle condition holds around the circle",
              all(rl.on_locus(N9, D9, -6 + rho * complex(math.cos(ph), math.sin(ph))) for ph in np.linspace(0.3, 2.8, 12)))
z9, k9, s9 = min_zeta(N9, D9, 0.3, 40)
v.check("15-06.9b", z9)
v.assert_true("P9: tangent-ray construction agrees", abs(z9 - math.cos(math.asin(rho / 6))) < 1e-6)
v.check("15-06.9d", abs(s9))
v.check("15-06.9c", k9)

# ---------------------------------------------------------------------------------------- Problem 10
Kneg = brentq(lambda k: np.max(np.roots([1, 3, 2 - k]).real), 0.1, 5)
v.check("15-06.10a", Kneg)

# ---------------------------------------------------------------------------------------- Problem 11
den = np.poly1d([1e-4, 1]) * np.poly1d([1e-6, 1]) * np.poly1d([1e-7, 1])
bmax = brentq(lambda b: np.max(np.roots((den + 1e4 * b).coeffs).real), 1e-3, 1.0, xtol=1e-14)
v.check("15-06.11a", bmax)
v.check("15-06.11b", 1 / bmax)
r = np.roots((den + 1e4 * bmax).coeffs)
v.check("15-06.11c", float(np.max(r.imag)))

# ---------------------------------------------------------------------------------------- Problem 12
K12 = 1e11 / 1.1
tzc = brentq(lambda t: np.max(np.roots([tp, 1, K12 * t, K12]).real), 0.1e-6, 2e-6, xtol=1e-18)
v.check("15-06.12a", tzc * 1e6)
r = np.roots([tp, 1, K12 * tzc, K12])
v.check("15-06.12b", float(np.max(r.imag)))

# ---------------------------------------------------------------------------------------- Problem 13
N13, D13 = [1, 2, 5], [1, 4, 0]
zk = complex(-1, 2)
arr = 180 + math.degrees(np.angle(zk - 0)) + math.degrees(np.angle(zk + 4)) - math.degrees(np.angle(zk - zk.conjugate()))
arr = (arr + 180) % 360 - 180
v.check("15-06.13a", arr)
rr = roots_at(N13, D13, 1e7)
c = rr[np.argmin(abs(rr - zk))]
v.assert_true("P13: numerical arrival direction (a high-gain root sits at angle arr from the zero)",
              abs(math.degrees(np.angle(c - zk)) - arr) < 0.01)
v.assert_true("P13: the branch arrives from below and to the left", (c - zk).real < 0 and (c - zk).imag < 0)

# ---------------------------------------------------------------------------------------- Problem 14
s14 = complex(-2, 2 * math.tan(math.radians(60)))
K14 = rl.gain_at([1], [1, 4, 3], s14)
v.check("15-06.14a", K14)
v.check("15-06.14b", 1 / (1 + K14 / 3))

# ---------------------------------------------------------------------------------------- Lab
ang8, cen8 = rl.asymptotes([1, 8], [1, 6, 8, 0])
v.assert_true("Lab a: lab asymptotes() agrees with (sum p - sum z)/(n - m)", abs(cen8 - (-6 + 8) / 2) < 1e-12 and ang8 == [90.0, 270.0])
# independent: the high-gain complex roots of s^3 + 6s^2 + (8 + K)s + 8K approach Re s = centroid
rK = np.roots([1, 6, 8 + 1e8, 8e8])
v.check("Lab 15-06.a", float(np.mean([c.real for c in rK if abs(c.imag) > 1])))
Kc, wc = crossing([1, 8], [1, 6, 8, 0], 5, 100)
v.check("Lab 15-06.b", Kc)
v.check("Lab 15-06.c", wc)
for K, key in ((2e11, "d"), (5e10, "e")):
    r = roots_at(N5, D5, K)
    c = r[np.argmax(r.imag)]
    v.check(f"Lab 15-06.{key}", -c.real / abs(c))

sys.exit(v.finish())
