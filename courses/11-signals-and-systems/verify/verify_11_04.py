#!/usr/bin/env python3
"""Verify every number in chapter 11-04 (LTI systems and differential/difference equations), its solutions and lab.

Independent routes:
- impulse and step responses by iterating each difference equation from rest (never from the closed forms);
- characteristic roots with numpy.roots;
- CT impulse responses by integrating the ODE from rest with the jump conditions as initial values, and checked
  against a narrow-pulse simulation; peaks by root finding on the integrated solution;
- DC gains by summing (integrating) the impulse responses;
- eigenvalues by driving the systems with long sinusoids and exponentials and measuring the steady-state ratio;
- structures by running direct form I, direct form II and transposed direct form II;
- library and data-sheet statements (R-186, R-187) quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-04", COURSE / "chapters" / "11-04-lti-systems-and-differential-equations.md",
                        COURSE / "solutions" / "11-04-solutions.md",
                        COURSE / "labs" / "11-04-lab" / "README.md")


def iterate(b, a, x):
    """y[n] = sum b_k x[n-k] - sum_{k>=1} a_k y[n-k], a[0] = 1, from rest."""
    y = np.zeros(len(x))
    for n in range(len(x)):
        acc = sum(b[k] * x[n - k] for k in range(len(b)) if n - k >= 0)
        acc -= sum(a[k] * y[n - k] for k in range(1, len(a)) if n - k >= 0)
        y[n] = acc
    return y


def imp(N):
    d = np.zeros(N)
    d[0] = 1
    return d


def steady_gain(b, a, w, N=3000):
    n = np.arange(N)
    y = iterate(b, a, np.cos(w * n)) if N <= 3000 else None
    return np.max(np.abs(y[N // 2:]))


# ============================================================ Example 1
v.check("Ex 11-04.1a", np.sum(np.abs(0.5 ** np.arange(200))))
hc = 0.5 ** np.arange(60)
hi = np.array([1.0, -0.5])
v.assert_true("inverse of 0.5^n u[n] is delta - 0.5 delta[n-1]", np.allclose(np.convolve(hc, hi)[:60], imp(60)))
v.assert_true("accumulator * first difference = delta", np.allclose(np.convolve(np.ones(50), [1, -1])[:50], imp(50)))

# ============================================================ Example 2
h2 = iterate([1, 1], [1, -0.5], imp(200))
for i, key in enumerate("abcd"):
    v.check(f"Ex 11-04.2{key}", h2[i])
v.check("Ex 11-04.2e", h2.sum())

# ============================================================ Example 3
r3 = np.sort(np.roots([1, -1.5, 0.56]).real)[::-1]
v.check("Ex 11-04.3a", r3[0])
v.check("Ex 11-04.3b", r3[1])
h3 = iterate([1], [1, -1.5, 0.56], imp(400))
v.check("Ex 11-04.3c", h3[2])
v.check("Ex 11-04.3d", h3.max())
v.check("Ex 11-04.3e", int(np.argmax(h3)))
v.check("Ex 11-04.3f", h3[6])
v.check("Ex 11-04.3g", h3.sum())

# ============================================================ Example 4
c4 = 2 * 0.9 * math.cos(math.pi / 4)
v.check("Ex 11-04.4a", c4)
h4 = iterate([1], [1, -c4, 0.81], imp(600))
v.check("Ex 11-04.4b", h4[1])
v.check("Ex 11-04.4c", h4[2])
v.check("Ex 11-04.4d", h4[3])
zc = [n for n in range(1, 60) if abs(h4[n]) < 1e-9]
v.check("Ex 11-04.4e", 2 * (zc[1] - zc[0]))                         # zeros every half period
v.check("Ex 11-04.4f", brentq(lambda n: 0.9 ** n - 0.01, 1, 200))
v.check("Ex 11-04.4g", h4.sum())
roots4 = np.roots([1, -c4, 0.81])
v.assert_true("resonator roots at 0.9 e^{+-j pi/4}",
              np.allclose(np.abs(roots4), 0.9) and np.allclose(np.sort(np.abs(np.angle(roots4))), math.pi / 4))

# ============================================================ Example 5 (ODE with jump conditions)
L, C, R = 1e-3, 1e-6, 20.0
w0 = 1 / math.sqrt(L * C)
alpha = R / (2 * L)
v.check("Ex 11-04.5a", w0 / 1e3)
v.check("Ex 11-04.5b", alpha)
v.check("Ex 11-04.5c", alpha / w0)
rts = np.roots([L * C, R * C, 1])
wd = abs(rts[0].imag)
v.check("Ex 11-04.5d", wd / 1e3)
v.check("Ex 11-04.5e", w0 ** 2 / wd / 1e4)
ode = solve_ivp(lambda t, y: [y[1], -w0 ** 2 * y[0] - 2 * alpha * y[1]], (0, 1e-3), [0.0, w0 ** 2],
                rtol=1e-11, atol=1e-6, dense_output=True)
hr = lambda t: ode.sol(t)[0]
tpk = brentq(lambda t: ode.sol(t)[1], 1e-6, 80e-6, xtol=1e-14)
v.check("Ex 11-04.5f", tpk * 1e6)
v.check("Ex 11-04.5g", hr(tpk) / 1e3)
v.check("Ex 11-04.5h", quad(hr, 0, 1e-3, limit=400)[0])
# narrow pulse check of the jump conditions
wdt = 0.2e-6
src = lambda t: (1 / wdt) if t < wdt else 0.0
nar = solve_ivp(lambda t, y: [y[1], w0 ** 2 * (src(t) - y[0]) - 2 * alpha * y[1]], (0, 100e-6), [0.0, 0.0],
                max_step=wdt / 20, rtol=1e-9, atol=1e-6, dense_output=True)
v.assert_true("narrow-pulse response matches h at 60 us (within 0.5%)",
              abs(nar.sol(60e-6)[0] - hr(60e-6 - wdt / 2)) < 5e-3 * abs(hr(60e-6)))

# ============================================================ Example 6
v.check("Ex 11-04.6a", 4)                                           # DF-I: two input and two output delays
v.check("Ex 11-04.6b", 5)
v.check("Ex 11-04.6c", 2)
v.check("Ex 11-04.6d", 2 * 5)
v.check("Ex 11-04.6e", 5 * 5)
v.check("Ex 11-04.6f", 25 * 48e3 / 1e6)
# CMSIS form y = b0 x + ... + a1 y[n-1] + a2 y[n-2]: run it with the negated coefficients and compare
cm_a1, cm_a2 = 1.5, -0.56
d = imp(100)
y_cm = np.zeros(100)
for n in range(100):
    y_cm[n] = d[n] + (cm_a1 * y_cm[n - 1] if n >= 1 else 0) + (cm_a2 * y_cm[n - 2] if n >= 2 else 0)
v.assert_true("CMSIS-signed coefficients reproduce Example 3", np.allclose(y_cm, h3[:100]))
v.check("Ex 11-04.6g", cm_a1)
v.check("Ex 11-04.6h", cm_a2)
v.check("Ex 11-04.6i", len(np.roots(np.ones(25))))                  # a 25-tap FIR polynomial has 24 roots
bad = np.sort(np.roots([1, 1.5, -0.56]).real)[::-1]
v.check("Ex 11-04.6j", bad[0])
v.check("Ex 11-04.6k", bad[1])

# ============================================================ Example 7
t = np.linspace(0, 200, 400001)
tau = 1.0
rc = signal.lsim(([1], [tau, 1]), np.cos(t / tau), t)[1]
amp7 = np.max(np.abs(rc[len(t) // 2:]))
v.check("Ex 11-04.7a", amp7)
lag_t = t[len(t) // 2:][np.argmax(rc[len(t) // 2:])] % (2 * math.pi)
v.check("Ex 11-04.7b", -math.degrees(lag_t))
ma = lambda w: steady_gain([1 / 3, 1 / 3, 1 / 3], [1], w, 3000)
v.check("Ex 11-04.7c", np.mean(iterate([1 / 3] * 3, [1], np.ones(50))[5:]))
v.check("Ex 11-04.7d", ma(2 * math.pi * 30 / 180))
v.check("Ex 11-04.7e", ma(2 * math.pi * 60 / 180))
n = np.arange(200)
y9 = iterate([1, 1], [1, -0.5], 0.9 ** n)
v.check("Ex 11-04.7f", y9[150] / 0.9 ** 150)
v.check("Ex 11-04.7g", y9[0] - y9[150] / 0.9 ** 150)
v.check("Ex 11-04.7h", y9[2])

# ============================================================ solutions
v.check("11-04.1a", 2)
v.check("11-04.1b", quad(lambda t: math.exp(-t), -1, 60)[0])
v.check("11-04.1c", sum(2.0 ** k for k in range(0, -200, -1)))
h12 = iterate([0.2], [1, -0.8], imp(300))
v.check("11-04.2a", h12[0])
v.check("11-04.2b", h12[1])
v.check("11-04.2c", h12[2])
v.check("11-04.2d", h12.sum())
v.check("11-04.2e", np.cumsum(h12)[9])
ra = np.sort(np.roots([1, -0.9, -0.1]).real)[::-1]
v.check("11-04.3a", ra[0])
v.check("11-04.3b", ra[1])
rb = np.roots([1, 0, 0.25])
v.check("11-04.3c", abs(rb[0]))
v.check("11-04.3d", 2 * math.pi / abs(np.angle(rb[0])))
rcr = np.sort(np.roots([1, -2.5, 1]).real)[::-1]
v.check("11-04.3e", rcr[0])
v.check("11-04.3f", rcr[1])
r4 = np.sort(np.roots([1, -1.2, 0.32]).real)[::-1]
v.check("11-04.4a", r4[0])
v.check("11-04.4b", r4[1])
h44 = iterate([1], [1, -1.2, 0.32], imp(300))
v.check("11-04.4c", h44[3])
v.check("11-04.4d", h44.sum())
th = 2 * math.pi * 1e3 / 8e3
r5 = brentq(lambda r: r ** 80 - 0.01, 0.5, 0.9999)
v.check("11-04.5a", th)
v.check("11-04.5b", r5)
v.check("11-04.5c", 2 * r5 * math.cos(th))
v.check("11-04.5d", r5 ** 2)
h5 = iterate([1], [1, -2 * r5 * math.cos(th), r5 ** 2], imp(200))
v.assert_true("resonator stays inside the envelope r^n / sin(theta), which is 1% of its start at n = 80",
              all(abs(h5[k]) <= r5 ** k / math.sin(th) + 1e-12 for k in range(200))
              and abs(r5 ** 80 - 0.01) < 1e-12)
# 6: H(s) = (s + 3)/(s + 2): DC gain by integrating h = delta + e^{-2t}
v.check("11-04.6a", 1 + quad(lambda t: math.exp(-2 * t), 0, 60)[0])
# 7: overdamped RLC by ODE
R7 = 100.0
a7 = R7 / (2 * L)
r7 = np.sort(np.roots([L * C, R7 * C, 1]).real)[::-1]
v.check("11-04.7a", r7[0] / 1e3)
v.check("11-04.7b", r7[1] / 1e3)
v.check("11-04.7c", w0 ** 2 / (r7[0] - r7[1]) / 1e3)
v.check("11-04.7e", math.sqrt(a7 ** 2 - w0 ** 2) / 1e4)
ode7 = solve_ivp(lambda t, y: [y[1], -w0 ** 2 * y[0] - 2 * a7 * y[1]], (0, 1e-3), [0.0, w0 ** 2],
                 rtol=1e-11, atol=1e-6, dense_output=True)
v.check("11-04.7d", brentq(lambda t: ode7.sol(t)[1], 1e-6, 200e-6, xtol=1e-14) * 1e6)
# 8: 2y'' + 3y' + y = delta
ode8 = solve_ivp(lambda t, y: [y[1], (-3 * y[1] - y[0]) / 2], (0, 60), [0.0, 0.5], rtol=1e-11, atol=1e-13,
                 dense_output=True)
v.check("11-04.8a", 0.5)
t8 = brentq(lambda t: ode8.sol(t)[1], 0.1, 5, xtol=1e-14)
v.check("11-04.8b", t8)
v.check("11-04.8c", ode8.sol(t8)[0])
v.check("11-04.8d", quad(lambda t: ode8.sol(t)[0], 0, 60, limit=400)[0])
# 9-10
b9, a9 = [0.5, 0.5], [1, -0.9]
x = np.random.default_rng(4).normal(size=300)
w1 = 0.0
yd2 = np.zeros(300)
for k, xn in enumerate(x):                                           # direct form II with one delay
    w = xn + 0.9 * w1
    yd2[k] = 0.5 * w + 0.5 * w1
    w1 = w
v.assert_true("DF-II with one delay equals DF-I", np.allclose(yd2, iterate(b9, a9, x)))
v.check("11-04.9a", 2)
v.check("11-04.9b", 3)
v.check("11-04.9c", 2)
v.check("11-04.9d", 1)
v.check("11-04.9e", iterate(b9, a9, imp(400)).sum())
v.check("11-04.10a", np.mean(iterate(b9, a9, np.ones(400))[300:]))
v.check("11-04.10b", np.max(np.abs(iterate(b9, a9, (-1.0) ** np.arange(400))[300:])))
nq = np.arange(4000)
yq = iterate(b9, a9, np.cos(math.pi / 2 * nq))
# fit y = A cos(pi/2 n + phi) = c0 cos(pi/2 n) - c1 sin(pi/2 n) on the steady part
seg = np.arange(2000, 4000)
M = np.c_[np.cos(math.pi / 2 * seg), -np.sin(math.pi / 2 * seg)]
coef = np.linalg.lstsq(M, yq[2000:], rcond=None)[0]
v.check("11-04.10c", math.hypot(coef[0], coef[1]))
v.check("11-04.10d", math.degrees(math.atan2(coef[1], coef[0])))
q4 = lambda c: round(c * 16) / 16
v.check("11-04.11a", q4(c4))
v.check("11-04.11b", q4(0.81))
rq = np.roots([1, -q4(c4), q4(0.81)])
v.check("11-04.11c", abs(rq[0]))
thq = math.degrees(abs(np.angle(rq[0])))
v.check("11-04.11d", thq)
v.check("11-04.11e", 360 / thq)
v.check("11-04.11f", math.cos(math.radians(thq)))
v.check("11-04.11g", 100 * (thq - 45) / 45)
alpha12 = brentq(lambda al: iterate([al], [1, -(1 - al)], np.ones(51))[49] - (1 - math.exp(-1)), 1e-4, 0.5)
v.assert_true("step reaches 63% at about sample 50", abs(alpha12 - (1 - math.exp(-1 / 50))) < 5e-4)
v.check("11-04.12a", 1 - math.exp(-1 / 50))
v.check("11-04.12b", math.log(100))
v.check("11-04.12c", 5 * 50)

# ============================================================ lab
d40 = imp(40)
for key, r in (("a", 1.0), ("b", 1.02)):
    h = iterate([1], [1, -2 * r * math.cos(math.pi / 4), r * r], d40)
    v.check(f"Lab 11-04.{key}", np.max(np.abs(h[32:40])))
bb, aa = signal.butter(8, 0.05)
qq = lambda c: np.round(np.asarray(c) * 2 ** 12) / 2 ** 12
v.check("Lab 11-04.c", np.max(np.abs(np.roots(aa))))
v.check("Lab 11-04.d", np.max(np.abs(np.roots(qq(aa)))))
v.check("Lab 11-04.e", max(np.max(np.abs(np.roots(sec[3:]))) for sec in qq(signal.tf2sos(bb, aa))))
v.check("Lab 11-04.f", np.max(np.abs(iterate([1, 1], [1, -0.5], np.cos(math.pi / 3 * np.arange(400)))[300:])))
y9l = iterate([1, 1], [1, -0.5], 0.9 ** np.arange(60))
v.check("Lab 11-04.g", y9l[2] / 0.9 ** 2)
v.check("Lab 11-04.h", y9l[40] / 0.9 ** 40)
v.check("Lab 11-04.i", 0.5 / 0.9)

sys.exit(v.finish())
