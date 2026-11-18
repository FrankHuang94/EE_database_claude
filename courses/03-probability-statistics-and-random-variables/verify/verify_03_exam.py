#!/usr/bin/env python3
"""Verify every number in the Course 03 final-exam solutions.

Each value is recomputed independently (enumeration, exact binomial and Poisson sums, numerical
integration and root finding), not copied from the solutions. The exam's table of distribution
values is checked too.
"""
from __future__ import annotations

import itertools
import math
import re
import sys
from math import comb, exp, log, log10, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import binom, chi2, norm, poisson
from scipy.stats import t as tdist

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("03-exam", HERE.parent / "exam" / "solutions.md")
Q, Qinv = norm.sf, norm.isf
K_J, K_EV, QE = 1.380649e-23, 8.617333262e-5, 1.602176634e-19
HPY = 8766.0

# ---------------------------------------------------------------- the exam's table of values
table = (HERE.parent / "exam" / "README.md").read_text()
for arg, val in (("2.0512", 0.02012), ("3.5009", 2.319e-4), ("4.5016", 3.372e-6), ("7.1667", 3.842e-13),
                 ("7.5", 3.191e-14), ("7.8333", 2.376e-15)):
    v.assert_true(f"table Q({arg})", abs(Q(float(arg)) / val - 1) < 6e-4)
v.assert_true("table inverse Q and multipliers", round(Qinv(0.05), 3) == 1.645 and round(Qinv(0.01), 3) == 2.326
              and round(Qinv(1e-12), 3) == 7.034 and round(2 * Qinv(1e-12), 3) == 14.069 and round(2 * Qinv(1e-15), 3) == 15.883)
v.assert_true("table t and Poisson bounds", round(tdist.ppf(0.975, 7), 3) == 2.365
              and round(chi2.ppf(0.6, 4) / 2, 3) == 2.022 and round(chi2.ppf(0.9, 4) / 2, 3) == 3.890)
v.assert_true("table rows present", all(s in table for s in ("Q(2.0512)", "Q(4.5016)", "t_{0.025,7}")))

# ---------------------------------------------------------------- 1 · enumeration over the 8 block outcomes
pf = (0.02, 0.05, 0.01)
probs = {o: math.prod(p if f else 1 - p for p, f in zip(pf, o)) for o in itertools.product((0, 1), repeat=3)}
v.check("X03.1a", probs[(0, 0, 0)])
v.check("X03.1b", sum(pr for o, pr in probs.items() if sum(o) == 1))
v.check("X03.1c", sum(pr for o, pr in probs.items() if sum(o) >= 1))
v.check("X03.1d", sum(pf))
v.check("X03.1e", (sum(pf) / (1 - probs[(0, 0, 0)]) - 1) * 100)

# ---------------------------------------------------------------- 2 · Bayes with two tests
prior, det, fr = 0.02, 0.97, 0.03
joint = {(d, r): (prior if d else 1 - prior) * ((det if r else 1 - det) if d else (fr if r else 1 - fr))
         for d in (0, 1) for r in (0, 1)}
rej = joint[(1, 1)] + joint[(0, 1)]
dl1 = joint[(1, 0)] / (joint[(1, 0)] + joint[(0, 0)])
v.check("X03.2a", rej)
v.check("X03.2b", dl1 * 1e6)
v.check("X03.2c", joint[(0, 1)] / rej)
v.check("X03.2d", joint[(1, 1)] / rej)
both_def = prior * det * (1 - det)              # defective: rejected, then passes retest
both_good = (1 - prior) * fr * (1 - fr)          # good: rejected, then passes retest
dl2 = both_def / (both_def + both_good)
v.check("X03.2e", dl2 * 1e6)
v.check("X03.2f", dl2 / dl1)

# ---------------------------------------------------------------- 3 · frames
lam3 = 1e4 * 2e-5
v.check("X03.3a", lam3)
v.check("X03.3b", poisson.pmf(0, lam3))
v.check("X03.3c", (1 - 2e-5) ** 10_000)
f3 = binom.sf(1, 10_000, 2e-5)
v.check("X03.3d", f3)
v.check("X03.3e", sum(kk * f3 ** (kk - 1) * (1 - f3) for kk in range(1, 50)))

# ---------------------------------------------------------------- 4 · reliability
fit4 = 8 * 50 + 400 + 1200
r4 = fit4 * 1e-9
p4 = -math.expm1(-r4 * HPY)
v.check("X03.4a", fit4)
v.check("X03.4j", r4 * HPY)
v.check("X03.4b", p4)
v.check("X03.4c", quad(lambda u: exp(-u), 0, 60)[0] / r4 / HPY)
v.check("X03.4d", exp(-r4 * 7 * HPY))
v.check("X03.4e", (exp(-r4 * 3 * HPY) - exp(-r4 * 4 * HPY)) / exp(-r4 * 3 * HPY))
N4 = 50_000
mu4, sd4 = N4 * p4, sqrt(N4 * p4 * (1 - p4))
v.check("X03.4f", mu4)
v.check("X03.4g", sd4)
v.check("X03.4h", Q((1000.5 - mu4) / sd4))
v.check("X03.4i", binom.sf(1000, N4, p4))

# ---------------------------------------------------------------- 5 · Gaussian decisions (by integration)
A, s5 = 90.0, 12.0
ber = lambda th: 0.5 * quad(lambda x: norm.pdf(x, A, s5), -np.inf, th)[0] + 0.5 * quad(lambda x: norm.pdf(x, -A, s5), th, np.inf)[0]  # noqa: E731
b0, b4 = Q(A / s5), 0.5 * (Q((A - 4) / s5) + Q((A + 4) / s5))
v.assert_true("BER formulas match integration", abs(ber(0) / b0 - 1) < 1e-4 and abs(ber(4) / b4 - 1) < 1e-4)
v.check("X03.5a", A / s5)
v.check("X03.5b", b0)
v.check("X03.5c", A / Qinv(1e-12))
v.check("X03.5d", b4)
v.check("X03.5e", b4 / b0)

# ---------------------------------------------------------------- 6 · jitter
ui = 1e12 / 25e9
rj = sqrt(1.2**2 + 0.9**2)
m12, m15 = 2 * Qinv(1e-12), 2 * Qinv(1e-15)
v.check("X03.6a", ui)
v.check("X03.6b", rj)
v.check("X03.6c", 12 + m12 * rj)
v.check("X03.6d", ui - 12 - m12 * rj)
v.check("X03.6e", (ui - 12 - m12 * rj) / ui)
v.check("X03.6f", 12 + m15 * rj)
rjmax = (ui - 8 - 12) / m12
v.check("X03.6g", rjmax)
v.check("X03.6h", sqrt(rjmax**2 - 0.9**2))

# ---------------------------------------------------------------- 7 · power (time average of the deterministic part)
ms_det = quad(lambda t: (0.5 + 0.2 * math.cos(2 * math.pi * t)) ** 2, 0, 1)[0]
ms = ms_det + 0.03**2
v.check("X03.7a", quad(lambda t: 0.5 + 0.2 * math.cos(2 * math.pi * t), 0, 1)[0])
v.check("X03.7b", ms)
v.check("X03.7c", sqrt(ms))
v.check("X03.7d", sqrt(ms - 0.25))
v.check("X03.7e", ms / 50 * 1e3)
v.check("X03.7f", 10 * log10(ms / 50 / 1e-3))
v.check("X03.7g", 10 * log10((ms_det - 0.25) / 0.03**2))
v.check("X03.7h", 3 * 30)

# ---------------------------------------------------------------- 8 · log-normal leakage
VT = K_J * 300 / QE
s8 = 0.018 / (1.3 * VT)
mean8 = quad(lambda x: exp(x) * norm.pdf(x, 0, s8), -12, 12)[0]
v.check("X03.8a", VT * 1e3)
v.check("X03.8b", s8)
v.check("X03.8c", mean8)
v.check("X03.8d", norm.sf(log(3), 0, s8))
v.check("X03.8e", exp(norm.isf(0.01, 0, s8)))
v.check("X03.8f", 2e7 * 0.2e-9 * mean8 * 1e3)
v.check("X03.8g", (1 - 1 / mean8) * 100)

# ---------------------------------------------------------------- 9 · combining sensors
S9 = np.array([[9.0, 0.6 * 12], [0.6 * 12, 16.0]])
v.check("X03.9a", sqrt(np.array([1, -1]) @ S9 @ np.array([1, -1])))
v.check("X03.9b", sqrt(np.array([0.5, 0.5]) @ S9 @ np.array([0.5, 0.5])))
opt = minimize_scalar(lambda w: np.array([w, 1 - w]) @ S9 @ np.array([w, 1 - w]), bounds=(-2, 3), method="bounded", options={"xatol": 1e-12})
v.check("X03.9c", opt.x)
v.check("X03.9d", sqrt(opt.fun))
S0 = np.diag([9.0, 16.0])
opt0 = minimize_scalar(lambda w: np.array([w, 1 - w]) @ S0 @ np.array([w, 1 - w]), bounds=(-2, 3), method="bounded", options={"xatol": 1e-12})
v.check("X03.9e", opt0.x)
v.check("X03.9f", sqrt(opt0.fun))

# ---------------------------------------------------------------- 10 · block code
n10, p10 = 2000, 5e-4
exact10 = sum(comb(n10, i) * p10**i * (1 - p10) ** (n10 - i) for i in range(5, 60))
sd10 = sqrt(n10 * p10 * (1 - p10))
z10 = (4.5 - n10 * p10) / sd10
v.check("X03.10a", exact10)
v.check("X03.10b", 1 - sum(exp(-1) / math.factorial(i) for i in range(5)))
v.check("X03.10c", sd10)
v.check("X03.10d", z10)
v.check("X03.10e", Q(z10))
v.check("X03.10f", exact10 / Q(z10))
pairs = 1 - sum(exp(-0.5) * 0.5**i / math.factorial(i) for i in range(3))
v.check("X03.10g", pairs)
v.check("X03.10h", pairs / poisson.sf(4, 1.0))
v.check("X03.10i", 1e6 * exact10)
v.check("X03.10j", sqrt(1e6 * exact10 * (1 - exact10)))

# ---------------------------------------------------------------- 11 · estimation and capability
d11 = np.array([1199.2, 1201.5, 1200.8, 1198.9, 1200.3, 1201.9, 1199.6, 1200.6])
m11, s11 = d11.mean(), d11.std(ddof=1)
se11 = s11 / sqrt(8)
tq = tdist.ppf(0.975, 7)
cpk11 = min(1206 - m11, m11 - 1194) / (3 * s11)
sek = sqrt(1 / 72 + cpk11**2 / 14)
v.check("X03.11a", m11)
v.check("X03.11b", s11)
v.check("X03.11j", se11)
v.check("X03.11c", m11 - tq * se11)
v.check("X03.11d", m11 + tq * se11)
v.check("X03.11e", 12 / (6 * s11))
v.check("X03.11f", cpk11)
v.check("X03.11g", sek)
v.check("X03.11h", cpk11 - Qinv(0.05) * sek)
v.check("X03.11i", math.ceil(brentq(lambda n: cpk11 - Qinv(0.05) * sqrt(1 / (9 * n) + cpk11**2 / (2 * (n - 1))) - 1.33, 3, 5000)))

# ---------------------------------------------------------------- 12 · HTOL to field
af12 = exp(0.6 / K_EV * (1 / 343.15 - 1 / 398.15))
D12 = 300 * 1000 * af12
lu = lambda conf: brentq(lambda lam: poisson.cdf(1, lam) - (1 - conf), 1e-6, 50)  # noqa: E731
v.check("X03.12a", af12)
v.check("X03.12b", D12)
v.check("X03.12c", 1 / D12 * 1e9)
v.check("X03.12d", lu(0.6) / D12 * 1e9)
v.check("X03.12e", lu(0.9) / D12 * 1e9)
b1 = brentq(lambda t: exp(-((t / 2500) ** 3)) - 0.99, 1, 2500)
v.check("X03.12f", b1)
v.check("X03.12g", b1 * af12)
v.check("X03.12h", b1 * af12 / HPY)

# ---------------------------------------------------------------- 13 · noise budget
es = sqrt(4 * K_J * 290 * 200)
tot = sqrt(es**2 + (1.5e-9) ** 2 + (1e-12 * 200) ** 2)
F = tot**2 / es**2
v.check("X03.13a", es * 1e9)
v.check("X03.13b", tot * 1e9)
v.check("X03.13c", F)
v.check("X03.13d", 10 * log10(F))
v.check("X03.13e", tot * sqrt(2e7) * 1e6)
v.check("X03.13f", 10 * log10(K_J * 290 / 1e-3) + 10 * log10(2e7) + 10 * log10(F))
v.check("X03.13g", sqrt(K_J * 300 / 2e-12) * 1e6)

v.assert_true("solutions cite every question", all(re.search(rf"\*\*{i}\.\*\*", (HERE.parent / "exam" / "solutions.md").read_text()) for i in range(1, 15)))
sys.exit(v.finish())
