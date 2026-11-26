#!/usr/bin/env python3
"""Verify every number in chapter 26-05 (schedule and respin risk), its problems and its lab.

Independent routes:
- PERT means checked against the mean of the beta-PERT distribution (scipy); normal probabilities through
  math.erf rather than scipy;
- the exact beta-PERT chance of meeting a date by numerical convolution of the task densities, against the
  lab's Monte Carlo;
- expected tape-outs as the sum of k P(N = k) over the full distribution (the lab sums tail probabilities);
- mitigation sets by enumerating every on/off pattern (the lab enumerates combinations by size);
- optimal tape-out times by direct numerical minimization of the expected cost (the lab solves the
  stationary-point equation), and the cost ridge by maximization.
"""
from __future__ import annotations

import math
import sys
from itertools import product
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import risk  # noqa: E402

v = Verifier.from_files("26-05", ROOT / "chapters" / "26-05-schedule-and-respin-risk.md",
                        ROOT / "solutions" / "26-05-solutions.md", LAB / "README.md")


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def beta_pert(a, m, b):
    al = 1 + 4 * (m - a) / (b - a)
    be = 1 + 4 * (b - m) / (b - a)
    return stats.beta(al, be, loc=a, scale=b - a)


def mean_sd(tasks):
    mu = sum(beta_pert(*t).mean() for t in tasks)
    sd = math.sqrt(sum(((t[2] - t[0]) / 6) ** 2 for t in tasks))
    return mu, sd


def dist_expectation(q):
    alive, e = 1.0, 0.0
    for k, qk in enumerate(q, start=1):
        e += k * alive * qk
        alive *= 1 - qk
    return e


def f_cost(t, n0, tau, phi, cw, cr, fixed=0.0):
    return fixed + cw * t + cr * (1 - math.exp(-phi * n0 * math.exp(-t / tau)))


def argmin_cost(n0, tau, phi, cw, cr, lo, hi):
    res = optimize.minimize_scalar(lambda t: f_cost(t, n0, tau, phi, cw, cr), bounds=(lo, hi), method="bounded",
                                   options={"xatol": 1e-10})
    return res.x


# ---------------------------------------------------------------- text
v.check("Txt 26-05.1", beta_pert(10, 14, 24).mean())
v.check("Txt 26-05.2", 100 * 0.85**2)
v.check("Txt 26-05.3", beta_pert(4, 6, 14).mean())
v.check("Txt 26-05.4", (14 - 4) / 6)
v.check("Txt 26-05.5", 0.9**3)
v.check("Txt 26-05.6", dist_expectation([0.5] * 60 + [1.0]))
v.check("Txt 26-05.7", (0.2 - 0.1) * 6)

# ---------------------------------------------------------------- Example 1
q = [0.25, 0.70, 0.95, 1.0]
dist = risk.spin_distribution(q)
v.assert_true("Ex 1 distribution sums to 1", abs(sum(dist) - 1) < 1e-12)
E = dist_expectation(q)
v.assert_true("Ex 1 lab expectation matches", abs(E - risk.expected_spins(q)) < 1e-12)
v.check("Ex 26-05.1a", 1 - q[0])
v.check("Ex 26-05.1b", dist[1])
v.check("Ex 26-05.1b1", dist[2])
v.check("Ex 26-05.1b2", dist[3])
v.check("Ex 26-05.1c", E)
v.check("Ex 26-05.1c1", 0.75 * 0.30)
v.check("Ex 26-05.1d", E - 1)
v.check("Ex 26-05.1d1", (E - 1) * 18)
v.check("Ex 26-05.1d2", (E - 1) * 21)
geo = dist_expectation([0.25] * 200 + [1.0])
v.check("Ex 26-05.1e", geo)
v.check("Ex 26-05.1f", geo - E)

# ---------------------------------------------------------------- Example 2
A = [(10, 14, 24), (1, 2, 4)]
B = [(8, 11, 18), (4, 5, 9)]
muA, sdA = mean_sd(A)
muB, sdB = mean_sd(B)
v.assert_true("Ex 2 lab path stats match", abs(risk.path_stats(A)[0] - muA) < 1e-9 and abs(risk.path_stats(B)[1] - sdB) < 1e-12)
v.check("Ex 26-05.2a", beta_pert(*A[1]).mean())
v.check("Ex 26-05.2a1", muA)
v.check("Ex 26-05.2a2", (24 - 10) / 6)
v.check("Ex 26-05.2a3", (4 - 1) / 6)
v.check("Ex 26-05.2a4", sdA)
v.check("Ex 26-05.2a5", beta_pert(*B[0]).mean())
v.check("Ex 26-05.2a6", beta_pert(*B[1]).mean())
v.check("Ex 26-05.2a7", muB)
v.check("Ex 26-05.2a8", sdB)
v.check("Ex 26-05.2a9", (18 - 8) / 6)
v.check("Ex 26-05.2a10", (9 - 4) / 6)
pa20, pb20 = Phi((20 - muA) / sdA), Phi((20 - muB) / sdB)
v.check("Ex 26-05.2b", pa20)
v.check("Ex 26-05.2b1", pb20)
v.check("Ex 26-05.2b2", pa20 * pb20)
v.check("Ex 26-05.2b3", 20 - muA)
pa16, pb16 = Phi((16 - muA) / sdA), Phi((16 - muB) / sdB)
v.check("Ex 26-05.2c", pa16)
v.check("Ex 26-05.2c1", pb16)
v.check("Ex 26-05.2c2", pa16 * pb16)
d90 = optimize.brentq(lambda T: Phi((T - muA) / sdA) * Phi((T - muB) / sdB) - 0.9, 15, 40)
v.check("Ex 26-05.2d", d90)
v.check("Ex 26-05.2d1", optimize.brentq(lambda T: Phi((T - muA) / sdA) - 0.9, 15, 40))


def path_cdf(tasks, T):
    d1, d2 = beta_pert(*tasks[0]), beta_pert(*tasks[1])
    return integrate.quad(lambda x: d1.pdf(x) * d2.cdf(T - x), tasks[0][0], tasks[0][2], limit=200)[0]


def joint_exact(T):
    return path_cdf(A, T) * path_cdf(B, T)


p_exact = joint_exact(20)
sim = risk.simulate_tapeout([A, B])
v.assert_true("Ex 2 Monte Carlo agrees with numerical convolution", abs((sim <= 20).mean() - p_exact) < 0.005,
              f"MC {(sim <= 20).mean():.4f} vs exact {p_exact:.4f}")
v.check("Ex 26-05.2e", p_exact)
v.check("Lab 26-05.a", p_exact)
d90b = optimize.brentq(lambda T: joint_exact(T) - 0.9, 18, 30)
v.check("Lab 26-05.a1", d90b)

# ---------------------------------------------------------------- Example 3
full_d, eco_d = 80 * 1.2, 25 * 1.2
v.check("Ex 26-05.3a", full_d)
v.check("Ex 26-05.3a1", full_d / 7)
v.check("Ex 26-05.3a2", eco_d)
v.check("Ex 26-05.3a3", eco_d / 7)
full_w, eco_w = full_d / 7 + 4, eco_d / 7 + 3
full_c, eco_c = 18 + 3 + 1.5 * full_w, 4 + 1 + 1.5 * eco_w
v.assert_true("Ex 3 lab ECO costs match", abs(risk.eco_cost(4, 1, eco_w, 1.5) - eco_c) < 1e-12)
v.check("Ex 26-05.3b", full_w)
v.check("Ex 26-05.3b1", full_c)
v.check("Ex 26-05.3b2", eco_w)
v.check("Ex 26-05.3b3", eco_c)
v.check("Ex 26-05.3c", full_c - eco_c)
v.check("Ex 26-05.3c1", full_w - eco_w)
v.check("Ex 26-05.3d", 24 * 12000)
v.check("Ex 26-05.3e", 100 * 1.5 * full_w / full_c)
v.check("Ex 26-05.3e1", 1.5 * full_w)
v.check("Ex 26-05.3e2", 100 * 1.5 * eco_w / eco_c)

# ---------------------------------------------------------------- Example 4
risks4 = [(0.25, 20), (0.15, 30), (0.30, 8), (0.20, 5)]
mits4 = [(2.0, 0.08), (2.5, 0.05), (1.5, 0.10), (0.8, 0.05)]


def best_by_pattern(risks, mits, budget):
    best = (None, -1e9)
    for pattern in product((0, 1), repeat=len(risks)):
        cost = sum(m[0] for m, on in zip(mits, pattern) if on)
        if cost > budget + 1e-12:
            continue
        net = sum((r[0] - m[1]) * r[1] - m[0] for r, m, on in zip(risks, mits, pattern) if on)
        if net > best[1] + 1e-12:
            best = (pattern, net, cost)
    return best


v.check("Ex 26-05.4a", sum(p * c for p, c in risks4))
nets = [(r[0] - m[1]) * r[1] - m[0] for r, m in zip(risks4, mits4)]
for key, n in zip(("Ex 26-05.4b", "Ex 26-05.4b1", "Ex 26-05.4b2", "Ex 26-05.4b3"), nets):
    v.check(key, n)
v.check("Ex 26-05.4b4", 0.25 - 0.08)
b4 = best_by_pattern(risks4, mits4, 4.0)
b5 = best_by_pattern(risks4, mits4, 5.0)
v.assert_true("Ex 4 $4 M set is R1 and R3", b4[0] == (1, 0, 1, 0))
v.assert_true("Ex 4 $5 M set is R1 and R2", b5[0] == (1, 1, 0, 0))
v.assert_true("Ex 4 lab search agrees", risk.best_mitigations(risks4, mits4, 4.0)[0] == (0, 2))
v.check("Ex 26-05.4c", b4[1])
v.check("Ex 26-05.4c1", b4[2])
v.check("Ex 26-05.4c2", b5[1])
v.check("Ex 26-05.4c3", b5[2])
resid = 0.08 * 20 + 0.15 * 30 + 0.10 * 8 + 0.20 * 5
v.check("Ex 26-05.4d", resid)
v.check("Ex 26-05.4d1", resid + b4[2])
v.check("Ex 26-05.4e", (0.20 - 0.05) * 5)

# ---------------------------------------------------------------- Example 5
N0, TAU, PHI, CW, CR = 40, 4.0, 0.25, 1.5, 40.0
k5 = CW * TAU / CR
t5 = argmin_cost(N0, TAU, PHI, CW, CR, 8, 40)
lam5 = PHI * N0 * math.exp(-t5 / TAU)
v.assert_true("Ex 5 lab optimum matches direct minimization", abs(risk.optimal_tapeout(N0, TAU, PHI, CW, CR)[0] - t5) < 1e-5)
v.check("Ex 26-05.5a", k5)
v.check("Ex 26-05.5a1", lam5)
v.check("Ex 26-05.5b", t5)
v.check("Ex 26-05.5b1", 1 - math.exp(-lam5))
v.check("Ex 26-05.5b2", f_cost(t5, N0, TAU, PHI, CW, CR))
lam8 = PHI * N0 * math.exp(-8 / TAU)
v.check("Ex 26-05.5c", lam8)
v.check("Ex 26-05.5c1", 1 - math.exp(-lam8))
v.check("Ex 26-05.5c2", f_cost(8, N0, TAU, PHI, CW, CR))
v.check("Ex 26-05.5c3", CR * (1 - math.exp(-lam8)))
v.check("Ex 26-05.5c4", f_cost(8, N0, TAU, PHI, CW, CR) - f_cost(t5, N0, TAU, PHI, CW, CR))
v.check("Ex 26-05.5d", f_cost(0, N0, TAU, PHI, CW, CR))
tmax = optimize.minimize_scalar(lambda t: -f_cost(t, N0, TAU, PHI, CW, CR), bounds=(0.5, 12), method="bounded",
                                options={"xatol": 1e-10}).x
v.check("Ex 26-05.5d1", PHI * N0 * math.exp(-tmax / TAU))
v.check("Ex 26-05.5d2", tmax)
v.check("Ex 26-05.5d3", f_cost(tmax, N0, TAU, PHI, CW, CR))
v.check("Ex 26-05.5e", lam5)
v.assert_true("Ex 5 marginal week saving equals its cost", abs(CR / TAU * lam5 * math.exp(-lam5) - CW) < 1e-6)

# ---------------------------------------------------------------- Example 6
t6 = argmin_cost(N0, 2.5, PHI, CW, CR, 5, 40)
lam6 = PHI * N0 * math.exp(-t6 / 2.5)
f6 = 3 + f_cost(t6, N0, 2.5, PHI, CW, CR)
v.check("Ex 26-05.6a", CW * 2.5 / CR)
v.check("Ex 26-05.6a1", lam6)
v.check("Ex 26-05.6a2", t6)
v.check("Ex 26-05.6b", 1 - math.exp(-lam6))
v.check("Ex 26-05.6c", f6)
f5 = f_cost(t5, N0, TAU, PHI, CW, CR)
v.check("Ex 26-05.6d", f5 - f6)
v.check("Ex 26-05.6d1", t5 - t6)
v.check("Ex 26-05.6e", f5 - (f6 - 3))
v.check("Ex 26-05.6e1", 100 * (1 - math.exp(-lam6)))
v.check("Ex 26-05.6e2", 100 * (1 - math.exp(-lam5)))

# ---------------------------------------------------------------- Problems
m1, s1 = beta_pert(6, 8, 16).mean(), 10 / 6
v.check("26-05.1a", m1)
v.check("26-05.1a1", s1)
v.check("26-05.1a2", Phi((10 - m1) / s1))
v.check("26-05.1a3", (10 - m1) / s1)

T3 = [(3, 4, 7), (6, 8, 13), (2, 3, 6)]
for key, t in zip(("26-05.3a", "26-05.3a1", "26-05.3a2"), T3):
    v.check(key, beta_pert(*t).mean())
for key, t in zip(("26-05.3a3", "26-05.3a4", "26-05.3a5"), T3):
    v.check(key, (t[2] - t[0]) / 6)
mu3, sd3 = mean_sd(T3)
v.check("26-05.3b", mu3)
v.check("26-05.3b1", sd3)
v.check("26-05.3c", Phi((17 - mu3) / sd3))
v.check("26-05.3d", optimize.brentq(lambda T: Phi((T - mu3) / sd3) - 0.95, 10, 30))

v.check("26-05.4a", 0.9**4)
req = 0.9**0.25
v.check("26-05.4b", req)
v.check("26-05.4c", stats.norm.ppf(req))
v.check("26-05.4c1", stats.norm.ppf(0.9))
v.check("26-05.4c2", stats.norm.ppf(req) - stats.norm.ppf(0.9))

q5 = [0.4, 0.8, 1.0]
E5 = dist_expectation(q5)
v.check("26-05.5a", E5)
v.check("26-05.5b", risk.spin_distribution(q5)[2])
v.check("26-05.5c", (E5 - 1) * 16)
v.check("26-05.5c1", (E5 - 1) * 15)

for key, q1 in (("26-05.6a", 0.14), ("26-05.6b", 0.05), ("26-05.6c", 0.30)):
    v.check(key, dist_expectation([q1, 0.6, 1.0]))

f7, e7 = 90 * 1.4, 30 * 1.4
v.check("26-05.7a", f7)
v.check("26-05.7a1", f7 / 7)
v.check("26-05.7a2", e7)
v.check("26-05.7a3", e7 / 7)
fw7, ew7 = f7 / 7 + 5, e7 / 7 + 3
fc7, ec7 = 25 + 4 + 2 * fw7, 6 + 1.5 + 2 * ew7
v.check("26-05.7b", fw7)
v.check("26-05.7b1", fc7)
v.check("26-05.7b2", ew7)
v.check("26-05.7b3", ec7)
v.check("26-05.7c", fc7 - ec7)
v.check("26-05.7c1", fw7 - ew7)

risks8 = [(0.3, 12), (0.1, 50), (0.4, 4)]
mits8 = [(1.5, 0.1), (2.5, 0.04), (0.5, 0.2)]
v.check("26-05.8a", sum(p * c for p, c in risks8))
for key, r, m in zip(("26-05.8b", "26-05.8b1", "26-05.8b2"), risks8, mits8):
    v.check(key, (r[0] - m[1]) * r[1] - m[0])
b3, b45 = best_by_pattern(risks8, mits8, 3.0), best_by_pattern(risks8, mits8, 4.5)
v.assert_true("P8 sets", b3[0] == (1, 0, 1) and b45[0] == (1, 1, 1))
v.check("26-05.8c", b3[1])
v.check("26-05.8c1", b3[2])
v.check("26-05.8c2", b45[1])

# Problem 9: exact loss distributions
ind = {0: 0.8**2, 10: 2 * 0.2 * 0.8, 20: 0.2**2}
cor = {0: 0.8, 20: 0.2}


def moments(d):
    m = sum(x * p for x, p in d.items())
    return m, math.sqrt(sum((x - m) ** 2 * p for x, p in d.items()))


v.check("26-05.9a", moments(ind)[0])
v.assert_true("P9 same EMV", abs(moments(ind)[0] - moments(cor)[0]) < 1e-12)
v.check("26-05.9b", ind[20])
v.check("26-05.9b1", moments(ind)[1])
v.check("26-05.9c", cor[20])
v.check("26-05.9c1", moments(cor)[1])


def f10(d):
    return 0.5 * d + 40 * Phi(-d / 4)


for key, keyc, d in (("26-05.10a", "26-05.10a1", 0), ("26-05.10a2", "26-05.10a3", 4), ("26-05.10a4", "26-05.10a5", 8)):
    v.check(key, Phi(-d / 4))
    v.check(keyc, f10(d))
d10 = optimize.minimize_scalar(f10, bounds=(0.1, 20), method="bounded", options={"xatol": 1e-10}).x
v.check("26-05.10b", d10 / 4)
v.check("26-05.10b1", d10)
v.check("26-05.10b2", Phi(-d10 / 4))
v.check("26-05.10b3", f10(d10))

t11 = argmin_cost(60, 5, 0.2, 1, 30, 10, 60)
lam11 = 0.2 * 60 * math.exp(-t11 / 5)
v.check("26-05.11a", 1 * 5 / 30)
v.check("26-05.11a1", lam11)
v.check("26-05.11b", t11)
v.check("26-05.11c", 1 - math.exp(-lam11))
v.check("26-05.11c1", f_cost(t11, 60, 5, 0.2, 1, 30))
v.check("26-05.11d", f_cost(0, 60, 5, 0.2, 1, 30))
v.check("26-05.11d1", f_cost(0, 60, 5, 0.2, 1, 30) - f_cost(t11, 60, 5, 0.2, 1, 30))

t12 = argmin_cost(20, TAU, PHI, CW, CR, 5, 40)
v.check("26-05.12a", t12)
v.check("26-05.12a1", 1 - math.exp(-PHI * 20 * math.exp(-t12 / TAU)))
v.check("26-05.12b", 2 + f_cost(t12, 20, TAU, PHI, CW, CR))
v.check("26-05.12c", t5 - t12)
v.assert_true("P12 time saved is tau ln 2", abs((t5 - t12) - TAU * math.log(2)) < 1e-4)

# ---------------------------------------------------------------- lab
v.check("Lab 26-05.b", dist_expectation([0.50, 0.70, 0.95, 1.0]))
v.check("Lab 26-05.b1", E - dist_expectation([0.50, 0.70, 0.95, 1.0]))
v.check("Lab 26-05.b2", 18 * (E - dist_expectation([0.50, 0.70, 0.95, 1.0])))
v.check("Lab 26-05.c", f_cost(24, N0, TAU, PHI, CW, CR))


def best_cost(tau):
    return f_cost(argmin_cost(N0, tau, PHI, CW, CR, 1, 60), N0, tau, PHI, CW, CR)


tau_be = optimize.brentq(lambda x: best_cost(x) + 3 - f5, 2.0, 3.99, xtol=1e-9)
v.check("Lab 26-05.d", tau_be)
v.check("Lab 26-05.d1", 100 * (1 - tau_be / 4))

sys.exit(v.finish())
