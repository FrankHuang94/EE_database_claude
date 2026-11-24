#!/usr/bin/env python3
"""Verify every number in the Course 19 final-exam solutions.

Answers with a non-trivial route are recomputed independently (below); closed-form arithmetic is re-evaluated:
- the inverter by solving the square-law current balance numerically (with lambda in both regions), unity-gain
  points from the computed transfer curve, and threshold sensitivity by finite differences;
- the step delay by integrating the discharge ODE; Elmore constants by explicit path-resistance sums over the
  RC network; pseudo-NMOS V_OL and charge sharing by root finding on current balance and charge conservation;
- logical-effort sizing and stage count by numerical minimization of path delay over the gate sizes;
- the wire's 50 % delay from its Fourier-series step response; the repeater optimum by numerical minimization;
- DVFS and the turbo supply by root finding; pipelining by enumerating the stage count;
- SRAM read disturbance with the 19-08 lab's transistor model; yield by Poisson sums;
- strip lengths by laying out the strip feature by feature; Euler orderings by brute force over all 24
  orderings with the 19-09 lab's graph tools;
- the timing graph by a separate topological pass; path sigma from the covariance matrix;
- strap IR drop by solving a discretized resistor ladder; the zero-skew tap by equating Elmore delays
  numerically; wirelengths with the 19-11 lab and a brute-force Hanan-grid search;
- coverage closure by a dynamic program over covered bins; BMC by state-graph search.
"""
from __future__ import annotations

import itertools
import math
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize
from scipy.stats import norm, poisson

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("19-08-lab", "19-09-lab", "19-11-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import layout  # noqa: E402
import pnr  # noqa: E402
import sram  # noqa: E402

v = Verifier.from_files("19-exam", ROOT / "exam" / "solutions.md")


# ---------------------------------------------------------------- Q1 inverter statics
def i_sq(k, vov, vds, lam=0.0):
    if vov <= 0:
        return 0.0
    if vds < vov:
        return k * (vov * vds - 0.5 * vds * vds) * (1 + lam * vds)
    return 0.5 * k * vov * vov * (1 + lam * vds)


def vout(vin, kn, kp, vdd, vtn, vtp, lam=0.0):
    f = lambda vo: i_sq(kn, vin - vtn, vo, lam) - i_sq(kp, vdd - vin - vtp, vdd - vo, lam)
    return brentq(f, 0.0, vdd, xtol=1e-14)


def vm_numeric(kn, kp, vdd, vtn, vtp, lam=0.0):
    return brentq(lambda x: vout(x, kn, kp, vdd, vtn, vtp, lam) - x, vtn + 1e-6, vdd - vtp - 1e-6, xtol=1e-13)


kp0 = 100e-6
vm_eq = vm_numeric(2.4 * kp0, kp0, 1.0, 0.30, 0.35)
v.check("X19.1a", vm_eq)
ratio = brentq(lambda rr: vm_numeric(rr * kp0, kp0, 1.0, 0.30, 0.35) - 0.5, 0.1, 2.0, xtol=1e-12)
v.check("X19.1b", ratio)
v.check("X19.1c", 2.4 / ratio)
# unity-gain points of the symmetric inverter from the computed transfer curve
k = 200e-6
slope = lambda x: (vout(x + 1e-6, k, k, 1.0, 0.3, 0.3) - vout(x - 1e-6, k, k, 1.0, 0.3, 0.3)) / 2e-6
vil = brentq(lambda x: slope(x) + 1, 0.31, 0.499, xtol=1e-12)
vih = brentq(lambda x: slope(x) + 1, 0.501, 0.69, xtol=1e-12)
v.check("X19.1d", vil)
v.check("X19.1e", vih)
# gain at V_M with lambda = 0.08 in both regions: solve the small-signal slope by implicit differentiation
lam = 0.08
x0 = vm_numeric(k, k, 1.0, 0.3, 0.3, lam)
h = 1e-7
gain = (vout(x0 + h, k, k, 1.0, 0.3, 0.3, lam) - vout(x0 - h, k, k, 1.0, 0.3, 0.3, lam)) / (2 * h)
v.check("X19.1f", abs(gain))
v.check("X19.1g", 2 / (lam * (x0 - 0.3)))
v.check("X19.1h", 1e3 * 1.0 / abs(gain))
d = 1e-5
dn = (vm_numeric(k, k, 1.0, 0.3 + d, 0.3) - vm_numeric(k, k, 1.0, 0.3 - d, 0.3)) / (2 * d)
dp = (vm_numeric(k, k, 1.0, 0.3, 0.3 + d) - vm_numeric(k, k, 1.0, 0.3, 0.3 - d)) / (2 * d)
v.check("X19.1i", 1e3 * 0.020 * math.hypot(dn, dp))

# ---------------------------------------------------------------- Q2 delay
cin, cint = 1.1 * 1.5, 0.9 * 1.5
v.check("X19.2a", cin)
v.check("X19.2b", cint)
v.check("X19.2c", 3 * cin + 3)
v.check("X19.2d", cint + 3 * cin + 3)
v.check("X19.2e", cint / cin)
kn, cl = 250e-6, 12e-15
ev = lambda t, y: y[0] - 0.5
ev.terminal = True
sol = solve_ivp(lambda t, y: [-i_sq(kn, 0.7, y[0]) / cl], [0, 1e-9], [1.0], events=ev, rtol=1e-11, atol=1e-14,
                max_step=1e-13)
v.check("X19.2f", sol.t_events[0][0] * 1e12)
isat = 0.5 * kn * 0.7 ** 2
v.check("X19.2g", isat * 1e6)
req = 0.75 / isat
v.check("X19.2h", req / 1e3)
v.check("X19.2i", math.log(2) * req * cl * 1e12)
v.check("X19.2j", 1e12 / (2 * 41 * 320e6))

# ---------------------------------------------------------------- Q3 logic families
mu = 2
v.check("X19.3a", 4)
v.check("X19.3b", (4 + mu) / (1 + mu))
v.check("X19.3c", 4 * mu)
v.check("X19.3d", (1 + 4 * mu) / (1 + mu))
# NAND3 pull-down: each NMOS has width 3, so resistance R/3; nodes counted from ground up
R, c, cext = 8e3, 0.6e-15, 15e-15
res = [R / 3] * 3                       # bottom, middle, top transistors
caps = [c * 3, c * 3, (1 + mu) * c * 3 + cext]   # node above bottom, node above middle, output
tau_e = sum(cap * sum(res[: i + 1]) for i, cap in enumerate(caps))
v.check("X19.3e", tau_e * 1e12)
v.check("X19.3f", 0.69 * tau_e * 1e12)
kn3, kp3 = 300e-6, 60e-6
iload = 0.5 * kp3 * 0.7 ** 2
v.check("X19.3g", iload * 1e6)
vol = brentq(lambda vo: i_sq(kn3, 0.7, vo) - i_sq(kp3, 0.7, 1.0 - vo), 0.0, 0.5, xtol=1e-14)
v.check("X19.3h", vol)
v.check("X19.3i", 1.0 * iload * 1e6)


def share(cl_, ca, vdd=1.0, vt=0.3):
    """Charge conservation with the internal node limited to vdd - vt."""
    return brentq(lambda vo: cl_ * vdd - cl_ * vo - ca * min(vo, vdd - vt), 0.0, vdd, xtol=1e-14)


v.check("X19.3j", brentq(lambda ca: 12 * 1.0 / (12 + ca) - 0.7, 0.1, 20) / 12)
v.check("X19.3k", share(12, 4))
v.check("X19.3l", share(12, 6))
v.check("X19.3m", 1.0 - share(12, 4))
v.check("X19.3n", 1.0 - vol)

# ---------------------------------------------------------------- Q4 logical effort by numerical minimization
g = [5 / 3, 1, 5 / 3, 1]
p = [2, 1, 3, 1]
branch = [1, 3, 1, 1]


def path_delay(cins, gs, ps, br, load):
    """cins: input capacitances of stages 2..N (stage 1 fixed at 6)."""
    c_all = [6.0] + list(cins) + [load]
    return sum(gs[i] * br[i] * c_all[i + 1] / c_all[i] + ps[i] for i in range(len(gs)))


res4 = minimize(lambda x: path_delay(np.exp(x), g, p, branch, 180.0), np.log([12, 20, 40]), method="Nelder-Mead",
                options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 20000})
G = math.prod(g)
v.check("X19.4a", G)
v.check("X19.4b", math.prod(branch))
v.check("X19.4c", 180 / 6)
v.check("X19.4d", G * 3 * 30)
v.check("X19.4e", sum(p))
v.check("X19.4g", res4.fun)
v.check("X19.4f", (res4.fun - sum(p)) / 4)
cins = np.exp(res4.x)
v.check("X19.4h", cins[2])
v.check("X19.4i", cins[1])
v.check("X19.4j", cins[0])
v.check("X19.4k", (5 / 3) * cins[0] / ((res4.fun - sum(p)) / 4))   # NOR2 input recovered from the optimum
v.check("X19.4l", math.log(250) / math.log(3.59))
res5 = minimize(lambda x: path_delay(np.exp(x), g + [1], p + [1], branch + [1], 180.0), np.log([10, 20, 40, 90]),
                method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 40000})
v.check("X19.4m", res5.fun)
v.check("X19.4n", res4.fun * 12)

# ---------------------------------------------------------------- Q5 wires
Rw, Cw = 8 * 2000, 0.2e-15 * 2000
v.check("X19.5a", Rw / 1e3)
v.check("X19.5b", Cw * 1e15)


def line_far_end(t_over_rc, terms=400):
    n = np.arange(terms)
    return 1 - 4 / math.pi * np.sum((-1.0) ** n / (2 * n + 1) * np.exp(-((2 * n + 1) ** 2) * math.pi ** 2 / 4 * t_over_rc))


t50 = brentq(lambda x: line_far_end(x) - 0.5, 0.1, 1.0, xtol=1e-12)
v.assert_true("distributed 50 % point is 0.379 RC", abs(t50 - 0.3790) < 5e-4, f"{t50:.4f}")
v.check("X19.5c", 0.38 * Rw * Cw * 1e9)
v.check("X19.5d", 0.69 * Rw * Cw * 1e9)
Rd, CL = 2e3, 20e-15
wire_term = Rw * (0.38 * Cw + 0.69 * CL)
t5 = 0.69 * Rd * (Cw + CL) + wire_term
v.check("X19.5e", t5 * 1e9)
v.check("X19.5f", 100 * wire_term / t5)
R0, C0 = 10e3, 0.2e-15
T = lambda kh: 0.69 * R0 * Cw / kh[1] + 0.69 * kh[0] * R0 * C0 + 0.38 * Rw * Cw / kh[0] + 0.69 * Rw * kh[1] * C0
opt = minimize(lambda x: T(x) * 1e12, [20.0, 20.0], method="Nelder-Mead",
               options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 20000})
v.check("X19.5g", opt.x[0])
v.check("X19.5h", opt.x[1])
v.check("X19.5i", opt.fun)
v.check("X19.5j", t5 / (opt.fun * 1e-12))
v.check("X19.5o", round(opt.x[0]))
v.check("X19.5p", 2000 / round(opt.x[0]))
v.check("X19.5k", 1.0 * 30 / (30 + 30 + 40))
for ident, mcf in (("X19.5l", 0), ("X19.5m", 1), ("X19.5n", 2)):
    v.check(ident, 40 + mcf * 60)

# ---------------------------------------------------------------- Q6 power
v.check("X19.6a", 1e3 * 0.12 * 400e-12 * 0.75 ** 2 * 1.5e9)
v.check("X19.6b", 1e3 * 150e-12 * 0.75 ** 2 * 1.5e9)
v.check("X19.6c", 1e3 * 0.6 * 150e-12 * 0.75 ** 2 * 1.5e9)
S = 1.35 * 25.85e-3 * math.log(10)          # the exam fixes kT/q = 25.85 mV at 300 K
v.check("X19.6d", S * 1e3)
v.check("X19.6e", 10 ** (0.060 / S))
speed = lambda vv: (vv - 0.3) ** 1.3 / vv
vh = brentq(lambda vv: speed(vv) / speed(0.9) - 0.5, 0.35, 0.9, xtol=1e-13)
v.check("X19.6f", vh)
v.check("X19.6g", (vh / 0.9) ** 2 * 0.5)
v.check("X19.6h", (vh / 0.9) ** 2)
v.check("X19.6i", 1e9 * (800e-12 * 0.75 ** 2 + 0.05e-9) / 3e-3)
v.check("X19.6j", 1e9 * 800e-12 * 0.75 ** 2)
v.check("X19.6k", 1e9 * (800e-12 * 0.75 ** 2 + 0.05e-9))

# ---------------------------------------------------------------- Q7 sequential timing
tmin = 45 + 380 + 25 - 20 + 12
v.check("X19.7a", tmin)
v.check("X19.7b", 1e3 / tmin)
v.check("X19.7c", 25 + 10 - (20 + 20))
nst = next(nn for nn in range(1, 50) if 1800 / nn + 70 <= 400)
v.check("X19.7d", nst)
tc = 1800 / nst + 70
v.check("X19.7e", 1e3 / tc)
v.check("X19.7f", nst * tc)
v.check("X19.7g", 100 * 70 / tc)
mtbf = math.exp(600 / 18) / (15e-12 * 1.5e9 * 80e6)
v.check("X19.7h", mtbf)
v.check("X19.7i", mtbf / (365.25 * 86400))
v.check("X19.7j", math.exp((1e12 / 1.5e9) / 18))

# ---------------------------------------------------------------- Q8 SRAM
dv = sram.read_disturb(100e-6, 180e-6, 0.9, 0.3)
v.check("X19.8a", dv)
v.check("X19.8b", 0.3 - dv)
cbl = 512 * 0.07e-15 + 12e-15
v.check("X19.8c", 1e12 * cbl * 0.09 / 18e-6)
v.check("X19.8d", 1e12 * 12e-12 * math.log(0.9 / 0.09))
q55 = norm.sf(5.5)
v.check("X19.8e", q55)
lam8 = 2 ** 28 * q55
v.check("X19.8f", lam8)
v.check("X19.8g", 100 * poisson.pmf(0, lam8))
spares = next(sp for sp in range(100) if poisson.cdf(sp, lam8) >= 0.99)
v.check("X19.8h", spares)
v.check("X19.8m", 100 * poisson.cdf(spares, lam8))
v.check("X19.8n", -math.log(0.99) / 2 ** 28)
v.check("X19.8i", brentq(lambda z: math.exp(-(2 ** 28) * norm.sf(z)) - 0.99, 5, 8))
v.check("X19.8o", 1e15 * cbl)
cells = 64 * 2 ** 20 * 0.0175e-6
v.check("X19.8j", cells)
v.check("X19.8k", cells / 0.72)
v.check("X19.8l", 64 * 2 ** 20 / 1e6 / (cells / 0.72))

# ---------------------------------------------------------------- Q9 layout
rules = dict(poly_width=2, poly_space=3, contact=2, contact_to_poly=2, enclose=1)


def strip(n_gates, contact_internal):
    """Lay the strip out feature by feature: enclosure, contact, spacing, gate, (spacing or contact gap), ..."""
    x = rules["enclose"] + rules["contact"] + rules["contact_to_poly"]
    for gi in range(n_gates):
        x += rules["poly_width"]
        if gi < n_gates - 1:
            x += (rules["contact_to_poly"] * 2 + rules["contact"]) if contact_internal else rules["poly_space"]
    return x + rules["contact_to_poly"] + rules["contact"] + rules["enclose"]


v.check("X19.9a", rules["poly_width"] + 2 * rules["contact_to_poly"] + rules["contact"])
v.check("X19.9b", rules["poly_width"] + rules["poly_space"])
v.check("X19.9c", strip(4, False))
v.check("X19.9d", strip(4, False) * 0.09)
v.check("X19.9e", strip(4, True))
v.check("X19.9f", strip(4, True) * 0.09)
pdn = ("s", [("p", [("t", "A"), ("t", "B")]), ("t", "C"), ("t", "D")])
valid = 0
pd_edges = layout.to_edges(pdn, "gnd", "out", itertools.count())
pu_edges = layout.to_edges(layout.dual(pdn), "vdd", "out", itertools.count(100))
for order in itertools.permutations("ABCD"):
    if layout.is_euler_path(pd_edges, list(order)) and layout.is_euler_path(pu_edges, list(order)):
        valid += 1
v.check("X19.9g", valid)
free = set()
for variant in layout.stack_variants(pdn):
    for order in itertools.permutations("ABCD"):
        e1 = layout.to_edges(variant, "gnd", "out", itertools.count())
        e2 = layout.to_edges(layout.dual(variant), "vdd", "out", itertools.count(100))
        if layout.is_euler_path(e1, list(order)) and layout.is_euler_path(e2, list(order)):
            free.add(order)
v.check("X19.9j", len(free))
v.assert_true("lab's common orderings agree", len(layout.common_euler_orders(pdn)) == valid, "")
v.check("X19.9k", 350 / 150)
v.check("X19.9l", 20000 * 25e-6 / 0.65)
v.check("X19.9h", 350 / 150 + 20000 * 25e-6 / 0.65)
v.check("X19.9i", 250 * 0.3 * 1.0 / 0.25)

# ---------------------------------------------------------------- Q10 timing graph
edges = {"G1": [("a", 0.20), ("b", 0.20)], "G2": [("b", 0.35)], "G3": [("G1", 0.15), ("G2", 0.15)]}
at = {"a": 0.0, "b": 0.10}
for node in ("G1", "G2", "G3"):
    at[node] = max(at[u] + dd for u, dd in edges[node])
rt = {"G3": 0.70}
for node in ("G2", "G1", "b", "a"):
    outs = [(w, dd) for w, ins in edges.items() for u, dd in ins if u == node]
    rt[node] = min(rt[w] - dd for w, dd in outs)
slack = {n_: rt[n_] - at[n_] for n_ in rt}
v.check("X19.10a", at["G1"])
v.check("X19.10b", at["G2"])
v.check("X19.10c", at["G3"])
v.check("X19.10d", slack["a"])
v.check("X19.10e", slack["b"])
v.check("X19.10f", slack["G1"])
v.assert_true("critical path b-G2-G3", abs(slack["G2"] - slack["b"]) < 1e-12 and abs(slack["G3"] - slack["b"]) < 1e-12, "")
setup = lambda l2: (1.20 + l2 - 0.06 - 0.05) - (0.35 + 0.12 + 0.62)
v.check("X19.10g", setup(0.28))
tcmin = brentq(lambda tc_: (tc_ + 0.28 - 0.06 - 0.05) - 1.09, 0.1, 2.0)
v.check("X19.10h", tcmin)
v.check("X19.10i", 1 / tcmin)
hold = lambda l2: (0.35 + 0.09 + 0.04) - (l2 + 0.03 + 0.02)
v.check("X19.10j", hold(0.28))
v.check("X19.10k", setup(0.60))
v.check("X19.10l", hold(0.60))
cov = 64.0 * (0.2 * np.ones((12, 12)) + 0.8 * np.eye(12))
sig = math.sqrt(np.ones(12) @ cov @ np.ones(12))
v.check("X19.10m", sig)
v.check("X19.10n", 3 * sig)
v.check("X19.10p", setup(0.60) - 0.17)
v.check("X19.10q", slack["G2"])
v.check("X19.10r", slack["G3"])
v.check("X19.10o", 3 * math.sqrt(np.ones(12) @ (64.0 * np.eye(12)) @ np.ones(12)))

# ---------------------------------------------------------------- Q11 place and route
v.check("X19.11a", 1.20 / 0.70)
v.check("X19.11b", math.sqrt(1.20 / 0.70))
rlen = 0.047 / 1.6
Rs = rlen * 400
v.check("X19.11c", Rs)


def ladder_drop(both_ends, n=2000):
    """Strap as n equal resistor segments with the 3 mA drawn equally at the n + 1 nodes (half at each end node),
    solved as a resistive network with the fed end(s) held at 0 V drop; returns the largest drop."""
    g = n / Rs
    loads = np.full(n + 1, 3e-3 / n)
    loads[0] = loads[-1] = 1.5e-3 / n
    fixed = [0, n] if both_ends else [0]
    free = [j for j in range(n + 1) if j not in fixed]
    idx = {j: m for m, j in enumerate(free)}
    A = np.zeros((len(free), len(free)))
    for j in free:
        for nb in (j - 1, j + 1):
            if 0 <= nb <= n:
                A[idx[j], idx[j]] += g
                if nb in idx:
                    A[idx[j], idx[nb]] -= g
    drop = np.linalg.solve(A, loads[free])     # drop below the supply at each free node
    return float(drop.max())


v.check("X19.11d", 1e3 * ladder_drop(True))
v.check("X19.11e", 1e3 * ladder_drop(False))
i_len = 3e-3 / 400
spacing = brentq(lambda L_: rlen * i_len * L_ ** 2 / 8 - 0.010, 1, 5000)
v.check("X19.11f", spacing)
r_, c_, L_ = 0.5, 0.2e-15, 300.0
d1 = lambda x: r_ * x * (c_ * x / 2 + 20e-15) + 50e-12
d2 = lambda x: r_ * (L_ - x) * (c_ * (L_ - x) / 2 + 30e-15) + 55e-12
x_tap = brentq(lambda x: d1(x) - d2(x), 0, L_, xtol=1e-12)
v.check("X19.11g", x_tap)
v.check("X19.11h", d1(x_tap) * 1e12)
pts = [(0, 0), (40, 10), (10, 50), (30, 30)]
v.check("X19.11i", (max(x for x, _ in pts) - min(x for x, _ in pts)) + (max(y for _, y in pts) - min(y for _, y in pts)))
v.check("X19.11j", pnr.rmst_length(pts))
hanan = [(x, y) for x in {p_[0] for p_ in pts} for y in {p_[1] for p_ in pts}]
best = min(pnr.rmst_length(pts + list(extra)) for k_ in range(0, 3) for extra in itertools.combinations(hanan, k_))
v.check("X19.11k", best)
v.assert_true("lab RSMT agrees with the Hanan search", pnr.rsmt_length(pts) == best, "")

# ---------------------------------------------------------------- Q12 test and verification
v.check("X19.12a", 1e6 * (1 - 0.85 ** 0.02))
v.check("X19.12b", 100 * brentq(lambda tt: 1 - 0.85 ** (1 - tt) - 2e-4, 0.9, 1.0, xtol=1e-14))
Lc = math.ceil(200_000 / 100)
cycles = 0
for _ in range(3000):
    cycles += Lc + 1                      # shift in (overlapping the previous unload) and capture
cycles += Lc                              # final unload
v.check("X19.12c", cycles)
v.check("X19.12d", 1e3 * cycles / 50e6)
v.check("X19.12e", 2 * 200_000 * 3000 / 8 / 1e6)
probs = [0.6, 0.3, 0.1]


@lru_cache(maxsize=None)
def e_cover(mask):
    need = [i for i in range(3) if not mask >> i & 1]
    if not need:
        return 0.0
    q = sum(probs[i] for i in need)
    return (1 + sum(probs[i] * e_cover(mask | 1 << i) for i in need)) / q


v.check("X19.12f", e_cover(0))
v.check("X19.12g", 1 / 0.1)
succ6 = lambda x: (0 if x == 5 else (x + 1) % 8)
reach6, x = {0}, 0
while succ6(x) not in reach6:
    x = succ6(x)
    reach6.add(x)
v.check("X19.12h", len(reach6))
cti = [st for st in range(8) if st != 7 and succ6(st) == 7]
v.check("X19.12i", cti[0])


def k_ok(k):
    """Every sequence of k+1 states following the transitions with x != 7 on the first k ends with x != 7."""
    for seq in itertools.product(range(8), repeat=k + 1):
        if all(succ6(seq[i]) == seq[i + 1] for i in range(k)) and all(q != 7 for q in seq[:-1]) and seq[-1] == 7:
            return False
    return True


v.check("X19.12j", next(k for k in range(1, 6) if k_ok(k)))

# ---------------------------------------------------------------- Q13 derivations
dd = 1e-6
sens = (vm_numeric(2.4 * kp0, kp0, 1.0, 0.30 + dd, 0.35) - vm_numeric(2.4 * kp0, kp0, 1.0, 0.30 - dd, 0.35)) / (2 * dd)
v.check("X19.13a", sens)
seg_k = opt.x[0]
v.assert_true("segment wire delay equals repeater intrinsic delay at the optimum",
              abs(0.38 * Rw * Cw / seg_k ** 2 - 0.69 * R0 * C0) / (0.69 * R0 * C0) < 1e-3, "")
v.check("X19.13b", 0.69 * R0 * C0 * 1e12)
v.check("X19.13c", brentq(lambda rho: rho * (math.log(rho) - 1) - 1.5, 2.8, 10))

# ---------------------------------------------------------------- Q14 diligence
pdyn = 0.25 * 1.6e-6 * 0.75 ** 2 * 1.2e9
v.check("X19.14a", pdyn)
v.check("X19.14b", 450 - pdyn)
v.check("X19.14c", 450 / 600)
fr = speed(0.85) / speed(0.75)
v.check("X19.14d", fr)
v.check("X19.14e", 1.2 * fr)
v.check("X19.14f", (0.85 / 0.75) ** 2 * fr)
v.check("X19.14g", pdyn * (0.85 / 0.75) ** 2 * fr)
v.check("X19.14h", 1e6 * (1 - 0.55 ** 0.03))
v.check("X19.14n", 100 * (1 - 0.55 ** 0.03))
v.check("X19.14i", 100 * brentq(lambda tt: 1 - 0.55 ** (1 - tt) - 5e-5, 0.9, 1.0, xtol=1e-15))
bits = 512 * 2 ** 20 * 8
v.check("X19.14j", bits * 0.021e-6)
v.check("X19.14k", bits * 0.021e-6 / 0.7)
v.check("X19.14l", 100 * bits * 0.021e-6 / 0.7 / 600)
v.check("X19.14m", brentq(lambda vv: speed(vv) / speed(0.75) - 2.0 / 1.2, 0.76, 3.0))

sys.exit(v.finish())
