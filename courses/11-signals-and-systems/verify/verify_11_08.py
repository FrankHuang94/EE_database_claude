#!/usr/bin/env python3
"""Verify every number in chapter 11-08 (the Laplace transform and system functions), its solutions and lab.

Independent routes:
- transforms by numerical integration of x(t) e^{-st} (never from the table), and inverse transforms checked by
  transforming the candidate signals back at test points inside each ROC;
- residues as numerical limits (s - p) X(s); poles with numpy.roots and scipy.signal.butter;
- step responses by integrating state-space models (scipy.signal.tf2ss + solve_ivp), with overshoots,
  undershoots and zero crossings found by optimization and root finding on the dense solutions;
- peaks, edges and bandwidths by optimization and root finding on computed magnitudes; group delays by
  differentiating the computed phase;
- the CTLE from the formula in the IEEE 802.3ck COM code (R-189); data-sheet facts (R-117) quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-08", COURSE / "chapters" / "11-08-laplace-transform-and-system-functions.md",
                        COURSE / "solutions" / "11-08-solutions.md",
                        COURSE / "labs" / "11-08-lab" / "README.md")
deg = math.degrees
db = lambda r: 20 * math.log10(r)
INF = np.inf


def laplace(x, s, lo=-INF, hi=INF):
    """Bilateral transform at complex s by quadrature (real and imaginary parts separately)."""
    re = quad(lambda t: (x(t) * np.exp(-s * t)).real, lo, hi, limit=400)[0]
    im = quad(lambda t: (x(t) * np.exp(-s * t)).imag, lo, hi, limit=400)[0]
    return re + 1j * im


def lap_terms(terms, s, lo, hi):
    """Transform of a sum of exponentials sum A e^{a t} on (lo, hi), by quadrature of the combined exponent
    sum A e^{(a - s) t}, so that neither factor overflows on its own."""
    f = lambda t: sum(A * np.exp((a - s) * t) for A, a in terms)
    return quad(lambda t: f(t).real, lo, hi, limit=400)[0] + 1j * quad(lambda t: f(t).imag, lo, hi, limit=400)[0]


def two_sided(pos, neg, s):
    """pos and neg are lists of (A, a) terms for t > 0 and t < 0."""
    return lap_terms(pos, s, 0, INF) + lap_terms(neg, s, -INF, 0)


def step_response(num, den, tmax, n=20001):
    A, B, C, D = signal.tf2ss(num, den)
    sol = solve_ivp(lambda t, z: A @ z + B[:, 0], (0, tmax), np.zeros(A.shape[0]), dense_output=True,
                    rtol=1e-11, atol=1e-13, method="DOP853")
    y = lambda t: float((C @ sol.sol(t))[0] + D[0, 0])
    return y


def extremum(y, a, b, sign=+1):
    r = minimize_scalar(lambda t: -sign * y(t), bounds=(a, b), method="bounded", options={"xatol": 1e-10})
    return r.x, y(r.x)


def residue(X, p, eps=1e-7):
    return ((eps) * X(p + eps) + (-eps) * X(p - eps)) / 2


def gdelay(H, w, h=1e-6):
    return -(np.angle(H(1j * (w + h)) / H(1j * (w - h)))) / (2 * h)


# ============================================================ theory / practitioner
fb = 53.125e9
v.check("T 11-08.a", fb / 2 / 1e9)
v.check("T 11-08.b", fb / 80 / 1e6)
v.check("T 11-08.c", 1 / (2 * math.pi * 0.1 * 2.2e-6) / 1e3)
fz = fp1 = 21.25e9
fp2 = 53.125e9


def ctle(f, g):
    G = 10 ** (g / 20)
    return (G + 1j * f / fz) / ((1 + 1j * f / fp1) * (1 + 1j * f / fp2))


# the zero's corner: where the numerator's magnitude has risen by sqrt(2) above its DC value
zero_f = lambda g: brentq(lambda f: abs(10 ** (g / 20) + 1j * f / fz) - math.sqrt(2) * 10 ** (g / 20), 1e6, 1e12,
                          xtol=1e-3)
v.check("T 11-08.d", zero_f(-20) / 1e9)
boost = lambda g: db(abs(ctle(fb / 2, g))) - db(abs(ctle(0.0, g)))
v.check("T 11-08.e", boost(-20))
fhp = fb / 80
ctle2 = lambda f, g, ghp: ctle(f, g) * (10 ** (ghp / 20) + 1j * f / fhp) / (1 + 1j * f / fhp)
v.check("T 11-08.i", brentq(lambda f: abs(10 ** (-6 / 20) + 1j * f / fhp) - math.sqrt(2) * 10 ** (-6 / 20), 1e3, 1e12,
                            xtol=1e-6) / 1e6)
v.check("T 11-08.j", db(abs(ctle2(fb / 2, -20, -6))) - db(abs(ctle2(0.0, -20, -6))))
poles2 = np.roots(np.polymul([1, 1], [1, -2]))
v.check("T 11-08.f", len(set(np.round(poles2.real, 9))) + 1)
pc = complex(-2, 6)
v.check("T 11-08.g", abs(pc))
v.check("T 11-08.h", -pc.real / abs(pc))

# ============================================================ Example 1
x1 = lambda t: np.exp(-2 * t) + np.exp(-3 * t)
X1 = lambda s: laplace(x1, s, 0, INF)
num1 = np.polyadd(np.poly([-3]), np.poly([-2]))           # (s+3) + (s+2)
v.check("Ex 11-08.1a", np.roots(num1)[0].real)
v.check("Ex 11-08.1b", max(-2, -3))
v.check("Ex 11-08.1c", X1(1.0).real)
v.check("Ex 11-08.1d", X1(0.0).real)
v.assert_true("integral diverges just left of -2 (grows with the window)",
              quad(lambda t: x1(t) * np.exp(2.1 * t), 0, 60)[0] > 10 * quad(lambda t: x1(t) * np.exp(2.1 * t), 0, 30)[0])

# ============================================================ Example 2
X2 = lambda s: 3 / ((s + 1) * (s - 2))
v.check("Ex 11-08.2a", residue(X2, -1).real)
v.check("Ex 11-08.2b", residue(X2, 2).real)
xc = lambda t: -np.exp(-t) + np.exp(2 * t)
xs_pos, xs_neg = (lambda t: -np.exp(-t)), (lambda t: -np.exp(2 * t))
TS_POS, TS_NEG = [(-1, -1)], [(-1, 2)]
xa = lambda t: np.exp(-t) - np.exp(2 * t)
v.assert_true("causal signal transforms back to X at s = 3",
              abs(laplace(xc, 3.0, 0, 200) - X2(3.0)) < 1e-8)
v.assert_true("two-sided signal transforms back to X at s = 0.5 and s = -0.5 + 1j",
              abs(two_sided(TS_POS, TS_NEG, 0.5) - X2(0.5)) < 1e-8
              and abs(two_sided(TS_POS, TS_NEG, -0.5 + 1j) - X2(-0.5 + 1j)) < 1e-8)
v.assert_true("anticausal signal transforms back to X at s = -2",
              abs(laplace(xa, -2.0, -200, 0) - X2(-2.0)) < 1e-8)
v.check("Ex 11-08.2c", xs_pos(1.0))
v.check("Ex 11-08.2d", xs_neg(-1.0))
v.check("Ex 11-08.2e", quad(xs_pos, 0, INF)[0] + quad(xs_neg, -INF, 0)[0])
v.check("Ex 11-08.2f", quad(lambda t: xs_pos(t) ** 2, 0, INF)[0] + quad(lambda t: xs_neg(t) ** 2, -INF, 0)[0])
v.check("Ex 11-08.2g", xc(1.0))
v.check("Ex 11-08.2h", xa(-1.0))

# ============================================================ Example 3: feedback
K = 5
pK = np.roots([1, 2, K])
p_up = pK[np.argmax(pK.imag)]
v.check("Ex 11-08.3a", p_up.real)
v.check("Ex 11-08.3b", p_up.imag)
v.check("Ex 11-08.3c", abs(p_up))
v.check("Ex 11-08.3d", -p_up.real / abs(p_up))
y3 = step_response([K], [1, 2, K], 12)
_, ymax = extremum(y3, 0.5, 3.0)
v.check("Ex 11-08.3e", 100 * (ymax - 1))
Kz = brentq(lambda k: -np.roots([1, 2, k])[0].real / abs(np.roots([1, 2, k])[0]) - 1 / math.sqrt(2), 1.01, 10)
v.check("Ex 11-08.3f", Kz)
v.check("Ex 11-08.3g", brentq(lambda k: 4 - 4 * k, 0, 3))
v.assert_true("for K > 1 the real part stays at -1",
              all(abs(np.roots([1, 2, k])[0].real + 1) < 1e-12 for k in (2, 5, 25)))

# ============================================================ Example 4: RLC
L, C, R = 1e-3, 1e-6, 20.0
pR = np.roots([L * C, R * C, 1])
p4 = pR[np.argmax(pR.imag)]
w0 = abs(p4)
al = -p4.real
wd = p4.imag
v.check("Ex 11-08.4a", w0 / 1e3)
v.check("Ex 11-08.4b", p4.real / 1e3)
v.check("Ex 11-08.4c", wd / 1e3)
v.check("Ex 11-08.4d", al / w0)
v.check("Ex 11-08.4e", w0 / (2 * al))
HC = lambda s: 1 / (L * C * s * s + R * C * s + 1)
HR = lambda s: R * C * s / (L * C * s * s + R * C * s + 1)
dists = [abs(1j * wd - p) for p in pR]
v.check("Ex 11-08.4f", w0 ** 2 / np.prod(dists))
v.check("Ex 11-08.4m", max(dists) / 1e3)
v.assert_true("geometric value equals direct evaluation", abs(w0 ** 2 / np.prod(dists) - abs(HC(1j * wd))) < 1e-12)
r = minimize_scalar(lambda w: -abs(HC(1j * w)), bounds=(1e4, 4e4), method="bounded", options={"xatol": 1e-6})
v.check("Ex 11-08.4g", r.x / (2 * math.pi) / 1e3)
v.check("Ex 11-08.4n", r.x / 1e3)
v.check("Ex 11-08.4h", abs(HC(1j * r.x)))
v.check("Ex 11-08.4o", db(abs(HC(1j * r.x))))
v.check("Ex 11-08.4i", abs(HC(1j * w0)))
v.assert_true("phase at w0 is -90 degrees", abs(deg(np.angle(HC(1j * w0))) + 90) < 1e-9)
g3 = lambda w: abs(HR(1j * w)) - 1 / math.sqrt(2)
lo = brentq(g3, 1e3, w0)
hi = brentq(g3, w0, 1e6)
v.check("Ex 11-08.4j", lo / (2 * math.pi) / 1e3)
v.check("Ex 11-08.4k", hi / (2 * math.pi) / 1e3)
v.check("Ex 11-08.4l", (hi - lo) / (2 * math.pi) / 1e3)
v.check("Ex 11-08.4p", lo / 1e3)
v.check("Ex 11-08.4q", hi / 1e3)
v.check("Ex 11-08.4r", (lo - (wd - al)) / 1e3)
v.check("Ex 11-08.4s", math.sqrt(lo * hi) / (2 * math.pi) / 1e3)
v.check("Ex 11-08.4t", (lo + hi) / 2 / 1e3)
v.check("Ex 11-08.4u", (wd - al) / (2 * math.pi) / 1e3)
v.check("Ex 11-08.4v", (wd + al) / (2 * math.pi) / 1e3)

# ============================================================ Example 5
H1 = lambda s: (s + 5) / ((s + 1) * (s + 2))
H2 = lambda s: (5 - s) / ((s + 1) * (s + 2))
v.check("Ex 11-08.5a", abs(H1(2j)))
v.assert_true("equal magnitudes on a grid", all(abs(abs(H1(1j * w)) - abs(H2(1j * w))) < 1e-14
                                                for w in np.linspace(0, 50, 101)))
v.check("Ex 11-08.5b", deg(np.angle(H1(2j))))
v.check("Ex 11-08.5c", deg(np.angle(H2(2j))))
v.check("Ex 11-08.5d", gdelay(H1, 0.0))
v.check("Ex 11-08.5e", gdelay(H2, 0.0))
v.check("Ex 11-08.5i", deg(np.angle(2j + 5)))
v.check("Ex 11-08.5j", deg(np.angle(1 / ((2j + 1) * (2j + 2)))))
v.check("Ex 11-08.5k", gdelay(lambda s: (5 - s) / (5 + s), 0.0))
y5 = step_response([-1, 5], [1, 3, 2], 20)
tmin, ymin = extremum(y5, 0.01, 1.0, sign=-1)
v.check("Ex 11-08.5f", tmin)
v.check("Ex 11-08.5g", ymin)
v.check("Ex 11-08.5h", y5(20.0))
y51 = step_response([1, 5], [1, 3, 2], 20)
v.assert_true("minimum-phase step response never goes negative", min(y51(t) for t in np.linspace(0, 3, 301)) >= -1e-12)

# ============================================================ Example 6: CTLE (R-189)
G12 = 10 ** (-12 / 20)
v.check("Ex 11-08.6a", G12)
v.check("Ex 11-08.6b", zero_f(-12) / 1e9)
v.check("Ex 11-08.6c", db(abs(ctle(fb / 2, -12))))
v.check("Ex 11-08.6d", boost(-12))
pk = minimize_scalar(lambda lf: -abs(ctle(10 ** lf, -12)), bounds=(9.5, 11), method="bounded",
                     options={"xatol": 1e-12})
v.check("Ex 11-08.6e", 10 ** pk.x / 1e9)
v.check("Ex 11-08.6f", db(abs(ctle(10 ** pk.x, -12))) + 12)
v.check("Ex 11-08.6g", db(abs(ctle(fb / 2, 0))))
v.check("Ex 11-08.6h", abs(ctle(fb / 2, -12)))
v.check("Ex 11-08.6i", math.log10(fz / zero_f(-12)))
v.check("Ex 11-08.6j", abs(G12 + 1j * (fb / 2) / fz))
v.check("Ex 11-08.6k", abs(1 + 1j * (fb / 2) / fp1))
v.check("Ex 11-08.6l", abs(1 + 1j * (fb / 2) / fp2))
v.assert_true("at 0 dB the zero cancels the first pole", abs(ctle(7e9, 0) - 1 / (1 + 1j * 7e9 / fp2)) < 1e-14)

# ============================================================ Example 7: Butterworth
z2, p2, k2 = signal.butter(2, 1.0, analog=True, output="zpk")
v.check("Ex 11-08.7a", -p2[0].real / abs(p2[0]))
mag = lambda n, w: abs(signal.freqs_zpk(*signal.butter(n, 1.0, analog=True, output="zpk"), worN=[w])[1][0])
v.check("Ex 11-08.7b", db(mag(2, 2.0)))
v.check("Ex 11-08.7c", db(mag(3, 3.0)))
v.check("Ex 11-08.7d", db(mag(2, 3.0)))
v.check("Ex 11-08.7e", db(mag(2, 1.0)))
v.assert_true("product of squared distances equals w^4 + 1",
              all(abs(np.prod([abs(1j * w - p) ** 2 for p in p2]) - (w ** 4 + 1)) < 1e-12 for w in (0.3, 1.7, 4.0)))

# ============================================================ solutions
v.check("11-08.1a", np.roots([1, 4])[0])          # pole of 1/(s + 4) bounds the ROC
v.check("11-08.1b", laplace(lambda t: np.exp(-4 * t), 1.0, 0, INF).real)
v.check("11-08.1c", lap_terms([(-1, -4)], -5.0, -INF, 0).real)
pulse = lambda s: laplace(lambda t: 1.0, s, 0, 2)
v.check("11-08.2a", pulse(0.0).real)
v.check("11-08.2b", pulse(1.0).real)
nul = minimize_scalar(lambda w: abs(pulse(1j * w)), bounds=(2.0, 4.0), method="bounded", options={"xatol": 1e-9})
v.check("11-08.2c", nul.x)
v.check("11-08.2d", nul.x / (2 * math.pi))
p3 = np.roots([1, 6, 25])
v.check("11-08.3a", np.roots([1, 1])[0])
v.check("11-08.3b", abs(p3[0]))
v.check("11-08.3c", -p3[0].real / abs(p3[0]))
v.check("11-08.3d", abs(p3[0]) / (-2 * p3[0].real))
v.check("11-08.3e", 1 / 25)
h5 = lambda t: np.exp(-(t + 1)) * (t >= -1)
v.check("11-08.4a", h5(-0.5))
v.assert_true("system (v) transforms back to e^s/(s+1) at s = 0.3",
              abs(laplace(lambda t: np.exp(-(t + 1)), 0.3, -1, INF) - np.exp(0.3) / 1.3) < 1e-9)
X5 = lambda s: (s + 5) / ((s + 1) * (s + 3))
v.check("11-08.5a", residue(X5, -1).real)
v.check("11-08.5b", residue(X5, -3).real)
x5p, x5n = (lambda t: -np.exp(-3 * t)), (lambda t: -2 * np.exp(-t))
v.assert_true("strip signal transforms back at s = -2 + 0.5j",
              abs(two_sided([(-1, -3)], [(-2, -1)], -2 + 0.5j) - X5(-2 + 0.5j)) < 1e-8)
v.check("11-08.5c", x5p(1.0))
v.check("11-08.5d", x5n(-1.0))
E2P, E2N = [(1, -2)], [(1, 2)]
v.check("11-08.6a", two_sided(E2P, E2N, 0.0).real)
v.check("11-08.6b", two_sided(E2P, E2N, 2j).real)
v.check("11-08.6c", two_sided(E2P, E2N, 1.0).real)
p7 = np.roots([1, 4, 13])
w07 = abs(p7[0])
H7 = lambda s: 13 / (s * s + 4 * s + 13)
v.check("11-08.7a", w07)
v.check("11-08.7b", -p7[0].real / w07)
v.check("11-08.7c", w07 / (-2 * p7[0].real))
r7 = minimize_scalar(lambda w: -abs(H7(1j * w)), bounds=(0.5, 3.5), method="bounded", options={"xatol": 1e-10})
v.check("11-08.7d", r7.x)
v.check("11-08.7e", abs(H7(1j * r7.x)))
v.check("11-08.7f", db(abs(H7(1j * r7.x))))
A0, wa, beta = 1e5, 2 * math.pi * 10, 0.1
num8 = [A0]
den8 = np.polyadd([1 / wa, 1], [beta * A0])
v.check("11-08.8a", num8[0] / np.polyval(den8, 0))
pole8 = np.roots(den8)[0]
v.check("11-08.8b", -pole8 / (2 * math.pi) / 1e3)
v.check("11-08.8d", -pole8 / (2 * math.pi) / 1e3)
v.check("11-08.8c", num8[0] / np.polyval(den8, 0) * (-pole8 / (2 * math.pi)) / 1e6)
v.assert_true("open-loop GBW is also 1 MHz", abs(A0 * 10 - 1e6) < 1e-6)
H9 = lambda s: 1000 / ((s + 10) * (s + 100))
v.check("11-08.9a", abs(10j + 10))
v.check("11-08.9b", abs(10j + 100))
v.check("11-08.9c", deg(np.angle(10j + 100)))
v.check("11-08.9d", abs(H9(10j)))
v.check("11-08.9e", deg(np.angle(H9(10j))))
v.check("11-08.9f", abs(100j + 100))
v.check("11-08.9g", deg(np.angle(100j + 10)))
v.check("11-08.9h", abs(H9(100j)))
v.check("11-08.9i", deg(np.angle(H9(100j))))
H10 = lambda s: (2 - s) / (2 + s)
v.check("11-08.10a", deg(np.angle(H10(2j))))
v.check("11-08.10b", gdelay(H10, 0.0))
v.check("11-08.10c", gdelay(H10, 2.0))
y10 = step_response([-1, 2], [1, 2], 10)
v.check("11-08.10d", y10(1e-12))
v.check("11-08.10e", brentq(y10, 0.01, 2.0, xtol=1e-13))
z3, p3b, k3 = signal.butter(3, 1.0, analog=True, output="zpk")
pc3 = p3b[np.argmax(p3b.imag)]
v.check("11-08.11a", pc3.real)
v.check("11-08.11b", -pc3.real / abs(pc3))
v.check("11-08.11c", db(mag(3, 2.0)))
n40 = next(n for n in range(1, 20) if -db(mag(n, 2.0)) >= 40)
v.check("11-08.11d", n40)
v.check("11-08.11e", -db(mag(7, 2.0)))
v.check("11-08.11f", -db(mag(6, 2.0)))
v.check("11-08.11g", brentq(lambda n: 10 * math.log10(1 + 4 ** n) - 40, 1, 10))
H12 = lambda s: (s - 3) / ((s + 1) * (s + 6))
H12m = lambda s: -(s + 3) / ((s + 1) * (s + 6))
H12a = lambda s: (3 - s) / (3 + s)
v.check("11-08.12a", H12(0.0))
v.assert_true("H = Hmin * Hap at test points", all(abs(H12(s) - H12m(s) * H12a(s)) < 1e-14
                                                     for s in (0.7j, 2 + 1j, -0.4 + 5j)))
v.check("11-08.12b", gdelay(H12a, 0.0))
v.check("11-08.12c", deg(np.angle(H12(3j) / H12m(3j))))
v.check("11-08.13g", 10 ** (-6 / 20))
v.check("11-08.13a", zero_f(-6) / 1e9)
v.check("11-08.13b", db(abs(ctle(fb / 2, -6))))
v.check("11-08.13c", boost(-6))
g10 = next(g for g in range(0, -21, -1) if boost(g) >= 10)
v.check("11-08.13d", g10)
v.check("11-08.13e", boost(g10))
v.check("11-08.13f", db(abs(ctle(fb / 2, -400))))
f0, B = 100e6, 4e6
alpha = brentq(lambda a: (lambda lo_, hi_: hi_ - lo_)(
    *[brentq(lambda w: abs(2 * a * 1j * w / ((1j * w) ** 2 + 2 * a * 1j * w + (2 * math.pi * f0) ** 2))
             - 1 / math.sqrt(2), x0, x1) for x0, x1 in ((1e6, 2 * math.pi * f0), (2 * math.pi * f0, 1e10))])
    - 2 * math.pi * B, 1e5, 1e9)
v.check("11-08.14a", f0 / B)
v.check("11-08.14b", -alpha / 1e6)
v.check("11-08.14c", 1 / alpha * 1e9)
v.check("11-08.14d", f0 / alpha)
# damped frequency from the actual poles of s^2 + (w0/Q)s + w0^2
pr = np.roots([1, 2 * math.pi * f0 / 25, (2 * math.pi * f0) ** 2])
v.check("11-08.14e", abs(pr[0].imag) / (2 * math.pi) / (-pr[0].real))

# ============================================================ lab
v.check("Lab 11-08.a", two_sided(TS_POS, TS_NEG, 0.5).real)
v.check("Lab 11-08.b", 100 * (ymax - 1))
y25 = step_response([25], [1, 2, 25], 12)
_, ymax25 = extremum(y25, 0.2, 1.5)
v.check("Lab 11-08.c", 100 * (ymax25 - 1))
zc = [brentq(lambda t: y25(t) - 1, a_, a_ + 0.6) for a_ in (0.2, 0.85)]
v.check("Lab 11-08.d", math.pi / (zc[1] - zc[0]))
v.check("Lab 11-08.e", ymin)
v.check("Lab 11-08.f", boost(-20))
v.check("Lab 11-08.g", boost(-1))
v.check("Lab 11-08.h", next(g for g in range(0, -21, -1) if boost(g) > 0))

sys.exit(v.finish())
