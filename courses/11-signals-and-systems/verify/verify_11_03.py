#!/usr/bin/env python3
"""Verify every number in chapter 11-03 (convolution), its solutions and lab.

Independent routes (none uses the chapter's closed forms):
- DT convolutions by an explicit double loop over the definition, cross-checked by a Toeplitz matrix product;
- CT convolutions by adaptive quadrature of x(tau) h(t - tau) at each requested t, and by discretized
  convolution on a fine grid;
- peaks, crossing times and rise times by root finding on numerically convolved responses;
- the sinc^3 filter by convolving three boxcars; stability sums by direct accumulation;
- the RC responses also by integrating the circuit's ODE;
- data-sheet and paper values (R-039, R-185, R-186) quoted; MAC counts by multiplication.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import toeplitz
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-03", COURSE / "chapters" / "11-03-convolution.md",
                        COURSE / "solutions" / "11-03-solutions.md",
                        COURSE / "labs" / "11-03-lab" / "README.md")
rng = np.random.default_rng(31103)


def conv_loop(x, h):
    y = [0.0] * (len(x) + len(h) - 1)
    for n in range(len(y)):
        for k in range(len(x)):
            if 0 <= n - k < len(h):
                y[n] += x[k] * h[n - k]
    return np.array(y)


def conv_toeplitz(x, h):
    L = len(x) + len(h) - 1
    return toeplitz(np.r_[h, np.zeros(L - len(h))], np.r_[h[0], np.zeros(len(x) - 1)]) @ np.asarray(x, float)


def digits(seq, most_significant_first):
    s = list(seq) if most_significant_first else list(seq)[::-1]
    return int("".join(str(int(round(d))) for d in s))


def ct_conv(x, h, t, pts):
    """(x*h)(t) by quadrature over tau, with breakpoints supplied."""
    br = sorted(set(pts + [t - p for p in pts]))
    return quad(lambda tau: x(tau) * h(t - tau), min(br) - 1, max(br) + 1, points=br, limit=400)[0]


# ============================================================ theory
y_digits = conv_loop([1, 2, 3], [1, 1, 2])
v.assert_true("[1,2,3]*[1,1,2] = [1,3,7,7,6]", list(y_digits) == [1, 3, 7, 7, 6])
v.check("T 11-03.a", digits(y_digits, most_significant_first=False))
v.assert_true("321 x 211 = 67731", 321 * 211 == digits(y_digits, False))

# ============================================================ Example 1
x1, h1 = [1, 2, 3], [1, -1, 2]
y1 = conv_loop(x1, h1)
v.assert_true("Toeplitz form agrees", np.allclose(conv_toeplitz(x1, h1), y1))
for i, key in enumerate("abcde"):
    v.check(f"Ex 11-03.1{key}", y1[i])
v.check("Ex 11-03.1f", len(y1))
v.check("Ex 11-03.1g", y1.sum())
v.assert_true("area rule", y1.sum() == sum(x1) * sum(h1))
v.check("Ex 11-03.1h", digits(y_digits, most_significant_first=True))
v.assert_true("123 x 112 = 13776", 123 * 112 == digits(y_digits, True))

# ============================================================ Example 2
n = np.arange(60)
y2 = conv_loop(np.ones(60), 0.5 ** n)[:60]
v.check("Ex 11-03.2a", y2[3])
v.check("Ex 11-03.2b", y2[-1])
v.check("Ex 11-03.2c", conv_loop(0.5 ** n[:10], 0.25 ** n[:10])[2])

# ============================================================ Example 3
xp = lambda t: 1.0 if 0 <= t < 2 else 0.0
hp = lambda t: 3.0 if 0 <= t < 1 else 0.0
for key, tt in (("a", 0.5), ("b", 1.5), ("c", 2.5)):
    v.check(f"Ex 11-03.3{key}", ct_conv(xp, hp, tt, [0, 1, 2]))
tg = np.linspace(-1, 5, 6001)
yg = np.array([ct_conv(xp, hp, t, [0, 1, 2]) for t in tg[::10]])
v.check("Ex 11-03.3d", tg[::10][np.nonzero(yg > 1e-9)[0][-1]], tol=0.02)
v.check("Ex 11-03.3e", quad(lambda t: ct_conv(xp, hp, t, [0, 1, 2]), 0, 3, points=[1, 2], limit=200)[0])

# ============================================================ Example 4 (also by the ODE)
tau = 1e-3
x4 = lambda t: 5.0 if 0 <= t < 2e-3 else 0.0
h4 = lambda t: math.exp(-t / tau) / tau if t >= 0 else 0.0
for key, tt in (("a", 1e-3), ("b", 2e-3), ("c", 3e-3)):
    val = ct_conv(x4, h4, tt, [0, 2e-3])
    v.check(f"Ex 11-03.4{key}", val)
ode = solve_ivp(lambda t, y: [(x4(t) - y[0]) / tau], (0, 3e-3), [0.0], max_step=1e-6, rtol=1e-10, atol=1e-12,
                dense_output=True)
v.assert_true("ODE agrees at 3 ms", abs(ode.sol(3e-3)[0] - ct_conv(x4, h4, 3e-3, [0, 2e-3])) < 1e-4)
area4 = quad(lambda t: ct_conv(x4, h4, t, [0, 2e-3]), 0, 40e-3, points=[2e-3], limit=200)[0]
v.check("Ex 11-03.4d", area4 * 1e3)

# ============================================================ Example 5
hh = lambda t: ct_conv(h4, h4, t, [0])
tpk = brentq(lambda t: (hh(t + 1e-7) - hh(t - 1e-7)) / 2e-7, 0.2e-3, 3e-3, xtol=1e-12)
v.check("Ex 11-03.5a", tpk * 1e3)
v.check("Ex 11-03.5b", hh(tpk))
s2 = lambda t: quad(hh, 0, t, limit=200)[0]
s1 = lambda t: quad(h4, 0, t)[0]
v.check("Ex 11-03.5c", s2(1e-3))
v.check("Ex 11-03.5d", s1(1e-3))
r1 = brentq(lambda t: s1(t) - 0.9, 1e-6, 10e-3, xtol=1e-12) - brentq(lambda t: s1(t) - 0.1, 1e-7, 10e-3, xtol=1e-12)
t10 = brentq(lambda t: s2(t) - 0.1, 1e-6, 10e-3, xtol=1e-12)
t90 = brentq(lambda t: s2(t) - 0.9, 1e-6, 20e-3, xtol=1e-12)
v.check("Ex 11-03.5e", r1 * 1e3)
v.check("Ex 11-03.5f", (t90 - t10) * 1e3)
v.check("Ex 11-03.5g", t10 / tau)
v.check("Ex 11-03.5h", t90 / tau)
v.check("Ex 11-03.5i", (t90 - t10) / r1)

# ============================================================ Example 6: sinc^3 from boxcars
N = 256
box = np.ones(N)
h3 = np.convolve(np.convolve(box, box), box)
v.check("Ex 11-03.6a", len(h3))
v.check("Ex 11-03.6b", len(h3) / 128e3 * 1e3)
v.check("Ex 11-03.6c", h3.sum())
v.assert_true("sinc^3 DC gain is 2^24", h3.sum() == 2 ** 24)
v.assert_true("500 SPS is f_MOD/256 with f_MOD = 512 kHz/4", 512e3 / 4 / 256 == 500)

# ============================================================ Example 7
nn = np.arange(2000)
hA = (-0.8) ** nn
v.check("Ex 11-03.7a", np.sum(np.abs(hA)))
v.check("Ex 11-03.7b", np.sum(hA))
hB = 1.0 / (nn[:1000] + 1)
v.check("Ex 11-03.7c", np.cumsum(hB)[999])
hC = np.array([1, -2, 3, -2, 1], dtype=float)
v.check("Ex 11-03.7d", hC.sum())
worst_in = np.sign(hC[::-1])
v.check("Ex 11-03.7e", conv_loop(worst_in, hC)[4])
v.check("Ex 11-03.7f", math.log2(np.sum(np.abs(hC))))
v.check("Ex 11-03.7g", math.ceil(math.log2(np.sum(np.abs(hC)))))

# ============================================================ Example 8
v.check("Ex 11-03.8a", 101 * 48e3 * 2 / 1e6)
v.check("Ex 11-03.8b", 25 * 48e3 / 1e6)                          # 25-tap FIR in the ADC path [R-186]
macs = 56 * 56 * 64 * 64 * 9
v.check("Ex 11-03.8c", macs / 1e6)
v.check("Ex 11-03.8d", 256 * 256)                                  # 256 x 256 MAC array [R-039]
rate = 256 * 256 * 700e6
v.check("Ex 11-03.8e", rate / 1e12)
v.check("Ex 11-03.8f", 2 * rate / 1e12)
v.check("Ex 11-03.8g", macs / rate * 1e6)

# ============================================================ solutions
y11 = conv_loop([2, -1, 1], [1, 3])
for i, key in enumerate("abcd"):
    v.check(f"11-03.{1}{key}", y11[i])
v.check("11-03.1e", y11.sum())
# 2: supports
xs = {-2: 1, -1: 1, 0: 1, 1: 1}
hs = {3: 1, 4: -1}
ys = {}
for kx, vx in xs.items():
    for kh, vh in hs.items():
        ys[kx + kh] = ys.get(kx + kh, 0) + vx * vh
nz = sorted(k for k, val in ys.items())
v.check("11-03.2a", nz[0])
v.check("11-03.2b", nz[-1])
v.check("11-03.2c", ys[1])
v.check("11-03.2d", ys[5])
v.assert_true("interior samples cancel", all(ys[k] == 0 for k in (2, 3, 4)))
v.check("11-03.3a", sum([2, -1]))
y14 = conv_loop([1, 2], [3, -1, 1])
for i, key in enumerate("abcd"):
    v.check(f"11-03.4{key}", y14[i])
v.check("11-03.4e", digits(conv_loop([1, 2], [3, 1, 1]), most_significant_first=True))
v.assert_true("12 x 311", 12 * 311 == 3732)
y15 = conv_loop(0.5 ** n[:20], 0.5 ** n[:20])
for i, key in enumerate("abcd"):
    v.check(f"11-03.5{key}", y15[i])
y15b = conv_loop([1, 1, 1, 1], 0.5 ** n[:30])
v.check("11-03.5e", y15b[2])
v.check("11-03.5f", y15b[3])
v.check("11-03.5g", y15b[4])
h6 = lambda t: math.exp(-2 * t) if t >= 0 else 0.0
u6 = lambda t: 1.0 if t >= 0 else 0.0
v.check("11-03.6a", ct_conv(u6, h6, 0.5, [0]))
v.check("11-03.6b", ct_conv(u6, h6, 40.0, [0]))
r1f = lambda t: 1.0 if 0 <= t < 1 else 0.0
for key, tt in (("a", 0.5), ("b", 1.0), ("c", 1.5)):
    v.check(f"11-03.7{key}", ct_conv(r1f, r1f, tt, [0, 1]))
ramp = lambda t: t if 0 <= t < 2 else 0.0
for key, tt in (("d", 0.5), ("e", 1.5), ("f", 2.5)):
    v.check(f"11-03.7{key}", ct_conv(r1f, ramp, tt, [0, 1, 2]))
v.check("11-03.7g", quad(lambda t: ct_conv(r1f, ramp, t, [0, 1, 2]), 0, 3, points=[1, 2], limit=200)[0])
x8 = lambda t: 5 * math.exp(-t / 2e-3) if t >= 0 else 0.0
y8 = lambda t: ct_conv(x8, h4, t, [0])
t8 = brentq(lambda t: (y8(t + 1e-8) - y8(t - 1e-8)) / 2e-8, 0.3e-3, 4e-3, xtol=1e-12)
v.check("11-03.8a", t8 * 1e3)
v.check("11-03.8b", y8(t8))
v.check("11-03.8c", quad(y8, 0, 60e-3, limit=400)[0] * 1e3)
s9 = lambda k: 1 - 0.5 ** (k + 1) if k >= 0 else 0.0
h9 = [s9(k) - s9(k - 1) for k in range(60)]
v.check("11-03.9a", h9[0])
v.check("11-03.9b", sum(h9))
v.assert_true("h[n] = 0.5^(n+1)", all(abs(h9[k] - 0.5 ** (k + 1)) < 1e-15 for k in range(60)))
v.assert_true("cascade and parallel of [1,1] and [1,-1]",
              list(conv_loop([1, 1], [1, -1])) == [1, 0, -1] and list(conv_loop([1, -1], [1, 1])) == [1, 0, -1])
v.assert_true("cascade step response 1, 1, 0, 0, ...", list(np.cumsum([1, 0, -1, 0, 0])) == [1, 1, 0, 0, 0])
k = np.arange(5000)
v.check("11-03.11a", np.sum(0.9 ** k))
v.assert_true("(a) actual sum below its bound", np.sum(np.abs(0.9 ** k * np.cos(np.pi * k / 4))) < 10)
v.check("11-03.11b", np.sum(np.abs(np.ones(100))))
v.check("11-03.11c", np.sum(k * 0.5 ** k))
h12 = np.array([0.25, -0.5, 1, -0.5, 0.25])
v.check("11-03.12a", h12.sum())
v.check("11-03.12b", np.abs(h12).sum())
alt = (-1.0) ** np.arange(40)
v.check("11-03.12c", np.max(np.abs(conv_loop(alt, h12)[4:40])))
v.check("11-03.12d", math.log2(np.abs(h12).sum()))
v.check("11-03.12e", math.ceil(math.log2(np.abs(h12).sum())))
mf = conv_loop([1, 1, -1], [-1, 1, 1])
v.check("11-03.13a", mf.max())
v.check("11-03.13b", np.max(np.abs(np.delete(mf, np.argmax(mf)))))
m14 = 28 * 28 * 128 * 128 * 9
v.check("11-03.14a", m14 / 1e6)
v.check("11-03.14b", m14 / (4096 * 1e9) * 1e6)
v.check("11-03.14c", 100 * (m14 / (4096 * 1e9)) / 25e-6)

# ============================================================ lab
xr, hr = rng.normal(size=50), rng.normal(size=12)
ref = conv_loop(xr, hr)
agree = 1 + sum(np.allclose(f(xr, hr), ref, atol=1e-12) for f in
                (np.convolve, conv_toeplitz, lambda a, b: np.polynomial.polynomial.polymul(a, b)))
v.check("Lab 11-03.a", agree)
dt = 1e-3
tl = np.arange(0, 4, dt)
xpl = ((tl >= 0) & (tl < 2)).astype(float)
hpl = 3.0 * ((tl >= 0) & (tl < 1))
ypl = np.convolve(xpl, hpl)[: len(tl)] * dt
v.check("Lab 11-03.b", ypl[int(round(1.5 / dt))])
v.check("Lab 11-03.c", ypl.sum() * dt)
v.check("Lab 11-03.k", abs(ypl[int(round(0.5 / dt))] - 1.5))
exact = ct_conv(x4, h4, 2e-3 - 1e-15, [0, 2e-3])


def y_at(dlt, rule):
    lam = np.arange(0, 2e-3 + dlt / 2, dlt)
    f = 5.0 * np.exp(-(2e-3 - lam) / tau) / tau
    if rule == "rectangle":
        return np.sum(f[:-1]) * dlt
    return (np.sum(f) - 0.5 * (f[0] + f[-1])) * dlt


v.check("Lab 11-03.d", abs(y_at(2e-5, "rectangle") - exact) / abs(y_at(1e-5, "rectangle") - exact))
v.check("Lab 11-03.e", abs(y_at(2e-5, "trapezoid") - exact) / abs(y_at(1e-5, "trapezoid") - exact))
v.check("Lab 11-03.f", ode.sol(2e-3)[0])
s3 = np.cumsum(h3 / N ** 3)
v.check("Lab 11-03.g", s3[N - 1])
v.check("Lab 11-03.h", (len(h3) - 1) / 2 / 128e3 * 1e3)
v.assert_true("sinc^3 step response is 0.5 at the midpoint", abs(s3[382] - 0.5) < 2e-3)
# matched filter with the lab's seed and construction
rng_lab = np.random.default_rng(1103)
_ = rng_lab.normal(size=50), rng_lab.normal(size=12)                # Part 1 draws come first in the notebook
p = np.array([1.0, 1.0, -1.0])
code_ = np.kron([1, 1, 1, -1, -1, 1, -1], p)
r = rng_lab.normal(0, 0.8, size=400)
r[137:137 + len(code_)] += code_
v.check("Lab 11-03.i", int(np.argmax(np.convolve(r, code_[::-1]))) - (len(code_) - 1))
v.check("Lab 11-03.j", math.sqrt(len(code_)))

sys.exit(v.finish())
