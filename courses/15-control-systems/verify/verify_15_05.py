#!/usr/bin/env python3
"""Verify chapter 15-05 (stability and the Routh-Hurwitz criterion): examples, problems and lab answers.

Routes:
- Routh arrays from labs/15-05-lab/routh.py, and every count checked against numpy roots;
- gain limits by sympy (the symbolic first column) and checked by locating the root crossing numerically;
- the ring oscillator simulated in Python (solve_ivp with root-refined zero crossings); ngspice confirms it
  through labs/15-05-lab/ring3.cir (tools/run_spice.py);
- the marginal-stability response and the Pade limit by sympy, the time-delay limit by solving the phase condition.
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
sys.path.insert(0, str(ROOT / "labs" / "15-05-lab"))
from eeverify import Verifier  # noqa: E402
from routh import routh, first_column, rhp_count, jw_roots  # noqa: E402

CH = ROOT / "chapters" / "15-05-stability-routh-hurwitz.md"
v = Verifier.from_files("15-05", CH, ROOT / "solutions" / "15-05-solutions.md", ROOT / "labs" / "15-05-lab" / "README.md")
s, K = sp.symbols("s K", real=True)


def n_rhp(c):
    return int(np.sum(np.roots(c).real > 1e-9))


def crossing_gain(char_of_K, lo, hi):
    """Gain at which the largest real part of the roots crosses zero (numerical, independent of Routh)."""
    return brentq(lambda k: np.max(np.roots(char_of_K(k)).real), lo, hi, xtol=1e-12)


def check_count(label, c):
    v.assert_true(f"{label}: Routh count equals the root count", rhp_count(c) == n_rhp(c))


# ---------------------------------------------------------------------------------------- Example 1
c1 = [1, 2, 3, 10]
v.check("Ex 15-05.1a", first_column(c1)[2])
v.check("Ex 15-05.1b", rhp_count(c1))
check_count("Ex 1", c1)
v.check("Ex 15-05.1c", float(np.max(np.roots(c1).real)))

# ---------------------------------------------------------------------------------------- Example 2
col = [sp.Integer(1), sp.Integer(6), (6 * 8 - K) / 6, K]
Kmax2 = sp.solve(sp.Eq(col[2], 0), K)[0]
v.check("Ex 15-05.2a", float(Kmax2))
v.assert_true("Ex 2: numerical crossing at 48", abs(crossing_gain(lambda k: [1, 6, 8, k], 10, 100) - 48) < 1e-8)
w2 = jw_roots([1, 6, 8, 48])
v.check("Ex 15-05.2b", float(np.max(w2.imag)))

# ---------------------------------------------------------------------------------------- Example 3
x = sp.symbols("x")
cub = sp.Poly(sp.expand((x + 1) ** 3 + K), x).all_coeffs()
Kmax3 = sp.solve(sp.Eq(cub[1] * cub[2] - cub[0] * cub[3], 0), K)[0]
v.check("Ex 15-05.3a", float(Kmax3))
v.check("Ex 15-05.3b", float(np.max(jw_roots([1, 3, 3, 9]).imag)))
v.check("Ex 15-05.3c", float(Kmax3) ** (1 / 3))
# ring of three identical stages with pole at w0 = 2 pi x 1 GHz: crossing frequency of (s/w0 + 1)^3 + 8, in GHz
w0r = 2 * math.pi * 1e9
v.check("Ex 15-05.3d", float(np.max(np.roots([1 / w0r**3, 3 / w0r**2, 3 / w0r, 9]).imag)) / (2 * math.pi) / 1e9)
v.assert_true("Ex 3: numerical crossing of (x+1)^3 + K at K = 8",
              abs(crossing_gain(lambda k: [1, 3, 3, 1 + k], 1, 20) - 8) < 1e-8)

# ---------------------------------------------------------------------------------------- Example 4
c4a = [1, 1, 2, 2, 3]
v.check("Ex 15-05.4a", rhp_count(c4a))
check_count("Ex 4a", c4a)
c4b = [1, 2, 6, 8, 8]
v.check("Ex 15-05.4b", rhp_count(c4b))
v.check("Ex 15-05.4c", float(np.max(jw_roots(c4b).imag)))
v.assert_true("Ex 4b: factors as (s^2+4)(s^2+2s+2)", np.allclose(np.polymul([1, 0, 4], [1, 2, 2]), c4b))
_, notes_a, _ = routh(c4a)
_, notes_b, _ = routh(c4b)
v.assert_true("Ex 4: the special cases are the ones the text names",
              "zero first element" in notes_a[0] and "all zero" in notes_b[0])

# ---------------------------------------------------------------------------------------- Example 5
C, C2, R = 1e-9, 1e-10, 5e3
K5 = 1e11 * C / (C + C2)
tz, tp = R * C, R * C * C2 / (C + C2)
v.check("Ex 15-05.5a", K5)
v.check("Ex 15-05.5b", tz * 1e6)
v.check("Ex 15-05.5c", tp * 1e6)
v.check("Ex 15-05.5d", tz / tp)
r5 = np.roots([tp, 1, K5 * tz, K5])
v.check("Ex 15-05.5e", float(r5[np.argmin(abs(r5.imag))].real))
v.check("Ex 15-05.5f", complex(r5[np.argmax(r5.imag)]))
tzs, tps, Ks = sp.symbols("tau_z tau_p K_s", positive=True)
cub5 = [tps, 1, Ks * tzs, Ks]
v.assert_true("Ex 5: cubic test reduces to K (tau_z - tau_p) > 0",
              sp.simplify(cub5[1] * cub5[2] - cub5[0] * cub5[3] - Ks * (tzs - tps)) == 0)
v.assert_true("Ex 5: stable for K from 1e6 to 1e16", all(np.all(np.roots([tp, 1, k * tz, k]).real < 0)
                                                        for k in np.logspace(6, 16, 41)))

# ---------------------------------------------------------------------------------------- Example 6
z = sp.symbols("z")
sh = sp.Poly(sp.expand((z - sp.Rational(1, 2)) ** 3 + 6 * (z - sp.Rational(1, 2)) ** 2 + 8 * (z - sp.Rational(1, 2)) + K), z).all_coeffs()
Khi = sp.solve(sp.Eq(sh[1] * sh[2] - sh[0] * sh[3], 0), K)[0]
Klo = sp.solve(sp.Eq(sh[3], 0), K)[0]
v.check("Ex 15-05.6a", float(Khi))
v.check("Ex 15-05.6b", float(Klo))
for k, good in ((2.0, False), (2.7, True), (14.9, True), (15.1, False)):
    v.assert_true(f"Ex 6: K = {k} {'meets' if good else 'misses'} the -0.5 line",
                  (np.max(np.roots([1, 6, 8, k]).real) < -0.5) == good)
r6 = np.roots([1, 6, 8, 10])
v.check("Ex 15-05.6c", float(r6[np.argmax(r6.imag)].real))

# ---------------------------------------------------------------------------------------- Problem 1
c1d = [1, 1, 1, 2]
v.check("15-05.1a", rhp_count(c1d))
check_count("P1d", c1d)
v.assert_true("P1(a),(b) have RHP or axis roots", n_rhp([1, 2, 0, 5]) > 0 and n_rhp([1, 3, -1, 2, 1]) > 0)
v.assert_true("P1(c) stable", n_rhp([1, 3, 2]) == 0)

# ---------------------------------------------------------------------------------------- Problem 2
for c, (kf, kr) in (([1, 4, 5, 2], "ab"), ([1, 1, 2, 8], "cd")):
    v.check(f"15-05.2{kf}", first_column(c)[2])
    v.check(f"15-05.2{kr}", rhp_count(c))
    check_count(f"P2 {c}", c)

# ---------------------------------------------------------------------------------------- Problem 4
col4 = (5 * (K - 6) - K) / 5
Kmin4 = sp.solve(sp.Eq(col4, 0), K)[0]
v.check("15-05.4a", float(Kmin4))
v.assert_true("P4: numerical crossing at 7.5", abs(crossing_gain(lambda k: [1, 5, k - 6, k], 6.5, 20) - 7.5) < 1e-8)
v.check("15-05.4b", float(np.max(jw_roots([1, 5, 1.5, 7.5]).imag)))

# ---------------------------------------------------------------------------------------- Problem 5
c5 = [1, 1, 6, 6, 8, 8]
v.check("15-05.5a", rhp_count(c5))
ax = jw_roots(c5)
v.check("15-05.5b", len(ax))
freqs = sorted(set(np.round(np.abs(ax.imag), 9)))
v.check("15-05.5c", freqs[0])
v.check("15-05.5d", freqs[1])
v.assert_true("P5: remaining root is -1", np.allclose(np.polydiv(c5, np.real(np.poly(ax)))[0], [1, 1]))

# ---------------------------------------------------------------------------------------- Problem 6
c6 = [1, 2, 4, 8, 5]
v.check("15-05.6a", rhp_count(c6))
check_count("P6", c6)

# ---------------------------------------------------------------------------------------- Problem 7
Amin = brentq(lambda A: np.max(np.roots((np.poly1d([1, 1]) ** 5 + A**5).coeffs).real), 1.0, 2.0, xtol=1e-14)
r7 = np.roots((np.poly1d([1, 1]) ** 5 + Amin**5).coeffs)
w7 = float(np.max(np.abs(r7[np.argsort(np.abs(r7.real))[:2]].imag)))
v.check("15-05.7a", w7)
v.check("15-05.7b", Amin)
v.check("15-05.7c", w7 * 1e3)
v.assert_true("P7: matches tan 36 deg and 1/cos 36 deg",
              abs(w7 - math.tan(math.pi / 5)) < 1e-9 and abs(Amin - 1 / math.cos(math.pi / 5)) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 8
sh8 = sp.Poly(sp.expand((z - 1) ** 3 + 6 * (z - 1) ** 2 + 8 * (z - 1) + K), z).all_coeffs()
v.check("15-05.8a", float(sh8[2]))
bk = np.roots([3, 12, 8])
bk = float(bk[np.argmax(bk)])
sig = sp.symbols("sigma", positive=True)
zcoef = sp.Poly(sp.expand((z - sig) ** 3 + 6 * (z - sig) ** 2 + 8 * (z - sig) + K), z).all_coeffs()[2]
v.assert_true("P8b: shifted z-coefficient is 3 sigma^2 - 12 sigma + 8 (independent of K)", sp.simplify(zcoef - (3 * sig**2 - 12 * sig + 8)) == 0)
sig_max = min(float(r) for r in sp.solve(sp.Eq(zcoef, 0), sig))
v.assert_true("P8b: Routh bound equals the breakaway", abs(sig_max + bk) < 1e-12)
v.check("15-05.8b", sig_max)
v.check("15-05.8c", -bk * (bk + 2) * (bk + 4))
# the best guaranteed decay rate over K, found by brute force
Kgrid = np.linspace(0.5, 47, 46501)
worst = [np.max(np.roots([1, 6, 8, k]).real) for k in Kgrid]
v.assert_true("P8: brute-force optimum matches the breakaway point",
              abs(min(worst) - bk) < 1e-3 and abs(Kgrid[int(np.argmin(worst))] - (-bk * (bk + 2) * (bk + 4))) < 0.01)

# ---------------------------------------------------------------------------------------- Problem 9
a, b, c = 2 * math.pi * 1e4, 1e5, 2 * math.pi * 1e6
den9 = np.poly1d([1 / a, 1]) * np.poly1d([1 / b, 1]) * np.poly1d([1 / c, 1])
L0max = crossing_gain(lambda k: (den9 + k).coeffs, 10, 1000)
v.check("15-05.9a", L0max)
v.assert_true("P9: matches the cubic formula", abs(L0max - ((a + b + c) * (a * b + b * c + c * a) / (a * b * c) - 1)) < 1e-6)
r9 = np.roots((den9 + L0max).coeffs)
v.check("15-05.9b", float(np.max(r9.imag)) / (2 * math.pi) / 1e3)
v.assert_true("P9: L0 = 2500 is unstable", rhp_count((den9 + 2500).coeffs) == 2)

# ---------------------------------------------------------------------------------------- Problem 10
t3 = 1e-6
char10 = lambda k: np.polyadd(np.polymul([1, 0, 0], np.polymul([tp, 1], [t3, 1])), [0, 0, 0, k * tz, k])  # noqa: E731
K10 = crossing_gain(char10, 1e11, 1e12)
v.check("15-05.10a", K10)
v.check("15-05.10b", K10 / K5)
v.check("15-05.10c", 20 * math.log10(K10 / K5))
r10 = np.roots(char10(K10))
v.check("15-05.10d", float(np.max(r10.imag)) / (2 * math.pi) / 1e3)
v.assert_true("P10: stable at the design gain", rhp_count(char10(K5)) == 0)

# ---------------------------------------------------------------------------------------- Problem 11
Rth, Cth, G, ts = 0.8, 20.0, 1.2, 0.1
char11 = lambda kc: [Rth * Cth * ts, Rth * Cth + ts * (1 - G), 1 - G + Rth * kc]  # noqa: E731
v.check("15-05.11a", crossing_gain(char11, 0.01, 2.0))


def throttle(kc):
    def rhs(t, xv):
        T_, Ts_ = xv
        return [(-(1 - G) * T_ + Rth * (-kc * Ts_)) / (Rth * Cth), (T_ - Ts_) / ts]
    return solve_ivp(rhs, (0, 600), [1.0, 1.0], rtol=1e-10, atol=1e-12).y[0, -1]


v.assert_true("P11: Kc = 0.2 runs away, Kc = 0.5 settles", throttle(0.2) > 1.0 and abs(throttle(0.5)) < 0.01)

# ---------------------------------------------------------------------------------------- Problem 12
v.check("15-05.12a", float(np.max(jw_roots([1, 3, 4, 12]).imag)))
v.assert_true("P12: boundary frequency independent of a",
              all(abs(np.max(jw_roots([1, aa, 4, 4 * aa]).imag) - 2) < 1e-9 for aa in (0.5, 3, 10)))

# ---------------------------------------------------------------------------------------- Problem 13
Kp13 = crossing_gain(lambda k: [0.5, 1 - k / 2, k], 0.5, 3.9)
v.check("15-05.13a", Kp13)
# exact: phase of e^{-jw}/(jw) is -pi/2 - w = -pi at w = pi/2; |L| = K/w = 1 there
w_exact = brentq(lambda w: -math.pi / 2 - w + math.pi, 0.1, 3)
Kexact = w_exact
v.check("15-05.13b", Kexact)
v.check("15-05.13c", 100 * (Kp13 / Kexact - 1))

# ---------------------------------------------------------------------------------------- Problem 14
t_ = sp.symbols("t", positive=True)
y14 = sp.inverse_laplace_transform(2 / (s**2 + 4) ** 2, s, t_)
v.assert_true("P14: y(t) = (sin 2t - 2t cos 2t)/8",
              all(abs(float(y14.subs(t_, tt)) - (math.sin(2 * tt) - 2 * tt * math.cos(2 * tt)) / 8) < 1e-12
                  for tt in (0.5, 3.0, 10.0)))
sol14 = solve_ivp(lambda t, xv: [xv[1], math.sin(2 * t) - 4 * xv[0]], (0, 10), [0, 0], rtol=1e-12, atol=1e-14)
v.check("15-05.14a", sol14.y[0, -1])
# envelope: amplitude of the growing term found from the simulated peaks near t = 10 s (local maxima of |y| grow as t/4)
tt14 = np.linspace(9.0, 11.0, 200001)
yy14 = np.abs(solve_ivp(lambda t, xv: [xv[1], math.sin(2 * t) - 4 * xv[0]], (0, 11), [0, 0], dense_output=True,
                        rtol=1e-12, atol=1e-14).sol(tt14)[0])
pk_i = [i for i in range(1, len(tt14) - 1) if yy14[i] > yy14[i - 1] and yy14[i] >= yy14[i + 1]]
slope = np.polyfit(tt14[pk_i], yy14[pk_i], 1)
v.check("15-05.14b", float(np.polyval(slope, 10.0)))

# ---------------------------------------------------------------------------------------- Lab (ring oscillator)
Rr, Cc, gm, Vs = 1e3, 1e-9, 2.2e-3, 0.1


def ring(t, vv):
    f = lambda xx: -gm * Vs * np.tanh(xx / Vs)  # noqa: E731
    return [(-vv[0] / Rr + f(vv[2])) / Cc, (-vv[1] / Rr + f(vv[0])) / Cc, (-vv[2] / Rr + f(vv[1])) / Cc]


sol = solve_ivp(ring, (0, 200e-6), [1e-3, 0, 0], dense_output=True, rtol=1e-11, atol=1e-14)
tt = np.linspace(0, 200e-6, 2000001)
v1 = sol.sol(tt)[0]
idx = np.flatnonzero((v1[:-1] < 0) & (v1[1:] >= 0))
ups = [brentq(lambda q: sol.sol(q)[0], tt[i], tt[i + 1], xtol=1e-18) for i in idx]
v.check("Lab 15-05.a", 10 / (ups[49] - ups[39]) / 1e3)
A_, w0 = gm * Rr, 1 / (Rr * Cc)
lin = np.roots((np.poly1d([1 / w0, 1]) ** 3 + A_**3).coeffs)
pl = lin[np.argmax(lin.imag)]
v.check("Lab 15-05.b", pl.real)
v.check("Lab 15-05.c", pl.imag / (2 * math.pi) / 1e3)
v.check("Lab 15-05.d", math.sqrt(3) * w0 / (2 * math.pi) / 1e3)

# ---------------------------------------------------------------------------------------- Lab optional hardware
# Three hard-switching inverters, each driving an RC (RC = 1): an inverter's output is the rail opposite to its
# input's side of mid-rail. Event-driven exact solution: between switching events every node relaxes exponentially.
def hard_ring_period():
    vn = np.array([0.0, 0.6, 0.2])
    t_now, crossings = 0.0, []
    for _ in range(400):
        outs = np.array([1.0 if vn[(i - 1) % 3] < 0.5 else 0.0 for i in range(3)])
        # time for each node to reach 0.5 while heading to its target, if it is heading across mid-rail
        dts = []
        for i in range(3):
            if (vn[i] - 0.5) * (outs[i] - 0.5) < 0:
                dts.append(math.log((outs[i] - vn[i]) / (outs[i] - 0.5)))
            else:
                dts.append(math.inf)
        k = int(np.argmin(dts))
        dt = dts[k]
        vn = outs + (vn - outs) * math.exp(-dt)
        vn[k] = 0.5 + (1e-12 if outs[k] > 0.5 else -1e-12)
        t_now += dt
        if k == 0 and outs[0] > 0.5:
            crossings.append(t_now)
    return float(np.mean(np.diff(crossings[-20:])))


Th = hard_ring_period()
v.assert_true("Lab hardware note: hard-switching ring oscillates near 1/(2.9 RC), stage delay about 0.48 RC",
              round(Th, 1) == 2.9 and round(Th / 6, 2) == 0.48 and abs(1 / Th - math.sqrt(3) / (2 * math.pi)) > 0.06)
v.assert_true("Lab hardware note: small-signal value is 1/(3.6 RC)", round(2 * math.pi / math.sqrt(3), 1) == 3.6)

sys.exit(v.finish())
