#!/usr/bin/env python3
"""Verify every number in the Course 26 final exam solutions, mostly by second routes.

Routes: a simulated day of mode switching (1a); numerical integration of the normal density (1d); a Markov
chain for defect escalation (2a); trying every reviewer count (3b); lot accounting for the cost stack (4);
explicit summation of interest factors and Brent's method for the IRR (5); backward-stepped present values
(6); shrunk block areas (7); energy in joules (8); root-finding for the 90% date and the tape-out
distribution (9); enumeration of mitigation sets and direct minimization of the expected cost (10); brute
force, the piecewise work integral inverted with Brent's method, and a search over every base (11); unit conversion, event enumeration,
the gamma distribution and TPP through MacTOPS (12).
"""
from __future__ import annotations

import math
import sys
from itertools import product
from pathlib import Path

from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("26-exam", ROOT / "exam" / "solutions.md")


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ---------------------------------------------------------------- Q1
day = 24 * 3600
modes = [(0.02, 12.0), (0.05, 4.0), (0.93, 0.015)]
charge_mAs = sum(frac * day * i for frac, i in modes)          # one simulated day
I_avg = charge_mAs / day
v.check("X26.1a", I_avg)
life_h = 0.8 * 200 / I_avg
v.check("X26.1a1", life_h)
v.check("X26.1a2", life_h / 24)
v.check("X26.1a3", 100 * 0.93 * 0.015 / I_avg)
sig = [0.5, 0.3, 0.4]
v.check("X26.1b", sum(3 * s for s in sig))
sE = math.sqrt(sum(s * s for s in sig))
v.check("X26.1b1", 3 * sE)
sc = math.sqrt(sum(s * s for s in sig) + 2 * 0.6 * 0.5 * 0.3)
v.check("X26.1c", sc)
v.check("X26.1c1", 3 * sc)
v.check("X26.1d", 2 / sE)
inside, _ = integrate.quad(lambda x: stats.norm.pdf(x, 0, sE), -2, 2)
v.check("X26.1d1", (1 - inside) * 1e6)

# ---------------------------------------------------------------- Q2 (Markov chain over stages)
stages = [(0.5, 10), (0.6, 100), (1.0, 1000)]
alive, cdown = 1.0, 0.0
for p, c in stages:
    cdown += alive * p * c
    alive *= 1 - p
v.check("X26.2a", cdown)
C = 50 * (0.4 * 1 + 0.6 * cdown)
v.check("X26.2a1", C)
v.check("X26.2a2", 100 * 0.5 * 0.4 * 1000 / cdown)
dC = (50 * (0.41 * 1 + 0.59 * cdown) - C) / 0.01
v.check("X26.2b", dC)
v.check("X26.2b1", -dC * 0.01)
w = optimize.brentq(lambda w: (w * 9 + (1 - w) * 6.0) - (w * 5 + (1 - w) * 7.5), 0, 1)
v.check("X26.2c", w)
v.check("X26.2d", 200 * 0.08)
v.check("X26.2d1", 200 * 0.08 * 0.25 * 150)

# ---------------------------------------------------------------- Q3
v.check("X26.3a", 1 - 0.6**3)
v.check("X26.3b", 1 + math.log(6000 / (20000 * 25 * 0.4)) / math.log(0.6))
cost = {k: k * 6000 + 20000 * 25 * 0.6**k for k in range(1, 30)}
kbest = min(cost, key=cost.get)
v.check("X26.3b1", kbest)
for key, k in zip(("X26.3b2", "X26.3b3", "X26.3b4"), (6, 7, 8)):
    v.check(key, cost[k])
v.check("X26.3c", 18 * 15 / 10)
v.check("X26.3c1", 19 * 16 / 11 - 1)
v.check("X26.3c2", 18 + 15 - 10)
v.check("X26.3c3", 18 * 15 / 10 - 23)
v.check("X26.3d", 100 * 140 / 180)
v.check("X26.3d1", 100 * 98 / 120)
v.check("X26.3d2", 100 * 20 / 140)
v.assert_true("Q3d ballot passes", 140 / 180 >= 0.75 and 98 / 120 >= 0.75 and 20 / 140 < 0.30)

# ---------------------------------------------------------------- Q4 (lot accounting)
raw = math.pi * 300**2 / 480 - math.pi * 300 / math.sqrt(240)
n = math.floor(raw)
Y = math.exp(-1.2 * 0.12)
v.check("X26.4a", raw)
v.check("X26.4a1", n)
v.check("X26.4a2", Y)
wafers = 1000
good_dies = wafers * n * Y
spent = wafers * 15000
v.check("X26.4a3", spent / good_dies)
spent += good_dies * 5.0
assembled = good_dies * 0.985
v.check("X26.4b", spent / assembled)
spent += assembled * 1.50
shipped = assembled * 0.97
cogs = spent / shipped
v.check("X26.4b1", cogs)
v.check("X26.4c", 100 * (75 - cogs) / 75)
v.check("X26.4c1", 100 * (75 - cogs) / cogs)
v.check("X26.4c2", 75 - cogs)
v.check("X26.4d", 90e6 / (75 - cogs) / 1e6)

# ---------------------------------------------------------------- Q5
pa = sum(1.08**-t for t in range(1, 7))
v.check("X26.5a", pa)
v.check("X26.5a1", 1 / pa)
v.check("X26.5a2", 250e3 / pa)
flows = [-40, -40, 35, 35, 35, 35]
npv = lambda r, f: sum(cf / (1 + r) ** t for t, cf in enumerate(f))  # noqa: E731
v.check("X26.5b", npv(0.12, flows))
v.check("X26.5b1", 100 * optimize.brentq(lambda r: npv(r, flows), 0.01, 1))
cum, t_pay = 0.0, None
for t, cf in enumerate(flows):
    if cum + cf >= 0 and t_pay is None:
        t_pay = (t - 1) + (-cum) / cf
    cum += cf
v.check("X26.5c", t_pay)
slipped = [-40, -40, 0, 35, 35, 35]
v.check("X26.5d", npv(0.12, slipped))
v.check("X26.5d1", npv(0.12, flows) - npv(0.12, slipped))


# ---------------------------------------------------------------- Q6 (backward stepping)
def pv_back(flows_by_year, r):
    bal = 0.0
    for t in range(max(flows_by_year), -1, -1):
        bal += flows_by_year.get(t, 0.0)
        if t:
            bal /= 1 + r
    return bal


vol = [4, 6, 6, 4]
U = pv_back({t + 1: u for t, u in enumerate(vol)}, 0.10)
v.check("X26.6a", U)
lic = pv_back({0: 8.0, **{t + 1: 1.0 * u for t, u in enumerate(vol)}}, 0.10)
build = 30 + 0.2 * 20
v.check("X26.6b", lic)
v.check("X26.6b1", build)
v.check("X26.6b2", build - lic)
ustar = optimize.brentq(lambda u: 8 + u - build, 0, 100)
v.check("X26.6c", ustar)
v.check("X26.6c1", ustar / U)
roy = [0.025 * 40 * 0.9**k for k in range(4)]
for key, r in zip(("X26.6d", "X26.6d1", "X26.6d2"), roy[1:]):
    v.check(key, r)
pct = pv_back({t + 1: r * u for t, (r, u) in enumerate(zip(roy, vol))}, 0.10)
v.check("X26.6d3", pct)
v.check("X26.6d4", pct / U)
v.check("X26.6d5", U * 1.0 - pct)

# ---------------------------------------------------------------- Q7
blocks = [150 * f for f in (0.60, 0.25, 0.15)]
area = sum(b / g for b, g in zip(blocks, (1.6, 1.15, 1.05)))
v.check("X26.7a", 150 / area)
v.check("X26.7a1", area)


def good_die(w, a, d0):
    nn = math.floor(math.pi * 300**2 / (4 * a) - math.pi * 300 / math.sqrt(2 * a))
    yy = math.exp(-a / 100 * d0)
    return nn, yy, w / (nn * yy)


o, nw = good_die(15000, 150, 0.10), good_die(19000, area, 0.12)
for key, x in zip(("X26.7b", "X26.7b1", "X26.7b2"), o):
    v.check(key, x)
for key, x in zip(("X26.7b3", "X26.7b4", "X26.7b5"), nw):
    v.check(key, x)
v.check("X26.7b6", o[2] - nw[2])
v.check("X26.7c", 40 / (o[2] - nw[2]))
ratio = (19000 / 15000) * area / 150
v.check("X26.7d", ratio)
v.check("X26.7d1", 100 * (19000 / 15000 - 1))
v.check("X26.7d2", 100 * (1 - ratio))


# ---------------------------------------------------------------- Q8 (joules)
def energy_cost(kw, years=4, pue=1.25, price=0.07):
    joules = kw * 1e3 * pue * years * 8760 * 3600
    return joules / 3.6e6 * price


Em, Ec = energy_cost(0.9), energy_cost(0.6)
v.check("X26.8a", Em)
v.check("X26.8a1", Ec)
Tm, Tc = 25000 + 10000 + Em, 8000 + 10000 + Ec
v.check("X26.8a2", Tm)
v.check("X26.8a3", Tc)
tc = Tc / 0.75
v.check("X26.8b", tc)
v.check("X26.8b1", Tm - tc)
be = optimize.brentq(lambda n_: n_ * (Tm - tc) - 500e6, 1, 1e8)
v.check("X26.8c", be)
v.check("X26.8c1", be / 0.75)
neq = 150000 * 0.75
v.check("X26.8d1", neq)
v.check("X26.8d", optimize.brentq(lambda pm: (pm + 10000 + Em) - (tc + 500e6 / neq), 0, 1e6))

# ---------------------------------------------------------------- Q9
pm = lambda a, m, b: (a + 4 * m + b) / 6  # noqa: E731
ps = lambda a, m, b: (b - a) / 6  # noqa: E731
A9, B9 = [(6, 8, 14), (2, 3, 5)], [(5, 7, 11), (3, 4, 7)]
muA, muB = sum(pm(*t) for t in A9), sum(pm(*t) for t in B9)
sA, sB = math.sqrt(sum(ps(*t) ** 2 for t in A9)), math.sqrt(sum(ps(*t) ** 2 for t in B9))
v.check("X26.9a", muA)
v.check("X26.9a1", sA)
v.check("X26.9a2", muB)
v.check("X26.9a3", sB)
for key, t in zip(("X26.9a4", "X26.9a5", "X26.9a6", "X26.9a7"), A9 + B9):
    v.check(key, pm(*t))
v.check("X26.9b4", (14 - muA) / sA)
v.check("X26.9b5", (14 - muB) / sB)
v.check("X26.9b", Phi((14 - muA) / sA))
v.check("X26.9b1", Phi((14 - muB) / sB))
v.check("X26.9b2", Phi((14 - muA) / sA) * Phi((14 - muB) / sB))
v.check("X26.9b3", optimize.brentq(lambda T: Phi((T - muA) / sA) * Phi((T - muB) / sB) - 0.9, 10, 30))
q = [0.3, 0.8, 1.0]
dist, alive = [], 1.0
for qk in q:
    dist.append(alive * qk)
    alive *= 1 - qk
EN = sum((k + 1) * d for k, d in enumerate(dist))
v.check("X26.9c", EN)
for key, d in zip(("X26.9c1", "X26.9c2", "X26.9c3"), dist):
    v.check(key, d)
v.check("X26.9c4", (EN - 1) * 16)
v.check("X26.9d", 85 * 1.3)
v.check("X26.9d1", 85 * 1.3 / 7)
v.check("X26.9d2", 28 * 1.3)
v.check("X26.9d3", 28 * 1.3 / 7)

# ---------------------------------------------------------------- Q10
risks = [(0.2, 25), (0.3, 10), (0.1, 40)]
mits = [(2.0, 0.05), (1.0, 0.15), (1.5, 0.03)]
v.check("X26.10a", sum(p * c for p, c in risks))
nets = [(r[0] - m[1]) * r[1] - m[0] for r, m in zip(risks, mits)]
for key, x in zip(("X26.10a1", "X26.10a2", "X26.10a3"), nets):
    v.check(key, x)
best = max((sum(nn for nn, on in zip(nets, pat) if on), pat) for pat in product((0, 1), repeat=3)
           if sum(m[0] for m, on in zip(mits, pat) if on) <= 3.0 + 1e-12)
v.assert_true("Q10a best set is R1 and R2", best[1] == (1, 1, 0))
v.check("X26.10a4", best[0])
v.check("X26.10a5", nets[1] + nets[2])


def f_cost(t, tau, fixed=0.0):
    return fixed + 1.2 * t + 30 * (1 - math.exp(-0.3 * 30 * math.exp(-t / tau)))


def argmin(tau):
    return optimize.minimize_scalar(lambda t: f_cost(t, tau), bounds=(4, 40), method="bounded",
                                    options={"xatol": 1e-10}).x


t10 = argmin(3)
lam = 9 * math.exp(-t10 / 3)
v.check("X26.10b", 1.2 * 3 / 30)
v.check("X26.10b1", lam)
v.check("X26.10b2", t10)
v.check("X26.10b3", 1 - math.exp(-lam))
v.check("X26.10c", f_cost(t10, 3))
v.check("X26.10c1", f_cost(0, 3))
t10d = argmin(2)
v.check("X26.10d", t10d)
v.check("X26.10d1", 1 - math.exp(-9 * math.exp(-t10d / 2)))
v.check("X26.10d2", f_cost(t10d, 2, 2.0))
v.check("X26.10d3", f_cost(t10, 3) - f_cost(t10d, 2, 2.0))
v.check("X26.10d4", t10 - t10d)
v.check("X26.10d5", 1.2 * 2 / 30)

# ---------------------------------------------------------------- Q11
c = 0.035
flat = lambda nn: nn * (1 - c * (nn - 1))  # noqa: E731
v.check("X26.11a", optimize.minimize_scalar(lambda x: -flat(x), bounds=(1, 30), method="bounded",
                                            options={"xatol": 1e-10}).x)
v.assert_true("Q11a best integer is 15", max(range(1, 40), key=flat) == 15)
v.check("X26.11a1", flat(14))
v.check("X26.11a2", flat(15))
v.check("X26.11b", 1 - 0.035 * 6)
v.check("X26.11b1", 7 * (1 - 0.035 * 6))
v.check("X26.11b2", 1 - 0.02 * 7)
H = 8 * 7 * (1 - 0.035 * 6) * (1 - 0.02 * 7)
v.check("X26.11b3", H)
v.check("X26.11b4", H / 64)


def finish(W, n0, add=0, ramp=0.0, mentor=0.0):
    """Invert the work done by time t (piecewise linear) for the finishing time."""
    e = 1 - 0.02 * (n0 + add - 1)
    r1 = (n0 - mentor * add) * e if add else (n0 + add) * e
    r2 = (n0 + add) * e

    def work(t):
        return r1 * min(t, ramp) + r2 * max(0.0, t - ramp) if add else r2 * t

    return optimize.brentq(lambda t: work(t) - W, 0, 1e4, xtol=1e-12)


v.check("X26.11c", 12 * (1 - 0.02 * 11))
v.check("X26.11c1", (12 - 3) * (1 - 0.02 * 17))
v.check("X26.11c2", 18 * (1 - 0.02 * 17))
v.check("X26.11c5", 2.5 * (12 - 3) * (1 - 0.02 * 17))
wbe = optimize.brentq(lambda W: finish(W, 12) - finish(W, 12, 6, 2.5, 0.5), 20, 150, xtol=1e-10)
v.check("X26.11c3", wbe)
v.check("X26.11c4", wbe / (12 * (1 - 0.02 * 11)))
load = [12, 18, 30, 45, 45, 30, 18, 12]
cst = lambda b: sum(b * 80e3 + max(0, l - b) * 120e3 for l in load)  # noqa: E731
b11 = min(range(0, 46), key=lambda b: (cst(b), b))
v.check("X26.11d", 80 / 120)
v.check("X26.11d1", b11)
v.check("X26.11d2", cst(b11) / 1e6)
v.check("X26.11d3", cst(12) / 1e6)
v.check("X26.11d4", cst(30) / 1e6)
v.check("X26.11d5", sum(max(0, l - b11) for l in load))

# ---------------------------------------------------------------- Q12
hrs = 1.5 * 365 * 15
v.check("X26.12a", hrs)
v.check("X26.12a1", 100 / 1e9 * 5e6 * hrs)
v.check("X26.12a2", -math.expm1(-100 / 1e9 * hrs))
p, beta = 5e-4, 0.03
pc, pi_ = beta * p, (1 - beta) * p
both = sum((pc if cc else 1 - pc) * (pi_ if a else 1 - pi_) * (pi_ if b else 1 - pi_)
           for cc, a, b in product((0, 1), repeat=3) if cc or (a and b))
v.check("X26.12b", both)
v.check("X26.12b1", both / p**2)
bound = stats.gamma.ppf(0.95, 1) / 2e8
v.check("X26.12c", bound / 1e-9)
need = optimize.brentq(lambda T: stats.gamma.ppf(0.95, 1) / T - 10e-9, 1e6, 1e12)
v.check("X26.12c2", need)
v.check("X26.12c1", need / 2e8)
tpp = 2 * (220 / 2) * 16
v.check("X26.12d", tpp)
v.check("X26.12d1", tpp / 520)
v.assert_true("Q12d meets 3A090.a.2 but not a.1", tpp < 4800 and tpp >= 1600 and tpp / 520 >= 5.92)

sys.exit(v.finish())
