#!/usr/bin/env python3
"""Verify every number in chapter 19-04 (transistor sizing and logical effort), its problems and its lab.

Independent routes:
- paths are sized by numerically minimizing the RC-model delay over every gate's drive (stage delay
  p_i + b_i C_next / s_i with C_in = g_i s_i), not by the equal-effort formula, and the minimum is compared with
  N F^(1/N) + P;
- the best number of stages by scanning integer N, and the best stage effort by minimizing the continuous chain
  delay numerically;
- logical efforts and parasitic delays from transistor widths (unit-drive sizing) rather than the table;
- the buffer chains by a separately written square-law transistor ODE (Radau), against the lab's simulate_chain;
  ngspice confirms the same chains in chain.cir (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import effort as ef  # noqa: E402

v = Verifier.from_files("19-04", ROOT / "chapters" / "19-04-sizing-and-logical-effort.md",
                        ROOT / "solutions" / "19-04-solutions.md", LAB / "README.md")
TAU = 0.6931471805599453 * 12.57e3 * 2e-15  # 19-02's inverter: tau = 0.69 R C_inv
v.check("Txt 19-04.a", TAU * 1e12)


# ---------------------------------------------------------------- gate parameters from transistor widths
def gate(kind, n=1, mu=2.0):
    """(g, p) from unit-drive widths: input capacitance per input and output diffusion, over the inverter's 1 + mu."""
    if kind == "inv":
        wn, wp, out = 1.0, mu, 1.0 + mu
    elif kind == "nand":
        wn, wp, out = float(n), mu, n * mu + n      # n parallel PMOS of width mu, top NMOS of width n
    else:
        wn, wp, out = 1.0, n * mu, n * mu + n       # top PMOS of width n mu, n parallel NMOS of width 1
    return (wn + wp) / (1 + mu), out / (1 + mu)


INV, NAND2, NOR2 = gate("inv"), gate("nand", 2), gate("nor", 2)
NAND3, NOR3, NAND4, NAND8 = gate("nand", 3), gate("nor", 3), gate("nand", 4), gate("nand", 8)
for (k, n), (g, p) in (((("nand", 3)), NAND3), (("nor", 3), NOR3), (("nand", 8), NAND8)):
    v.assert_true(f"lab efforts {k}{n}", abs(ef.logical_effort(k, n) - g) < 1e-12 and abs(ef.parasitic_delay(k, n) - p) < 1e-12,
                  "")


# ---------------------------------------------------------------- numerical path sizing
def path_rc(stages, branches, c_in, c_out):
    """Minimize sum_i [p_i + b_i * C_next_i / s_i] over the drives s_2..s_N, with s_1 = c_in / g_1."""
    n = len(stages)
    s1 = c_in / stages[0][0]

    def total(logs):
        s = [s1] + list(np.exp(logs))
        d = 0.0
        for i, (g, p) in enumerate(stages):
            nxt = stages[i + 1][0] * s[i + 1] if i + 1 < n else c_out
            d += p + branches[i] * nxt / s[i]
        return d
    if n == 1:
        return total([]), [s1]
    x0 = np.log([s1 * (c_out / c_in) ** ((i + 1) / n) for i in range(n - 1)])
    res = minimize(total, x0, method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 40000,
                                                              "maxfev": 40000})
    res = minimize(total, res.x, method="BFGS", options={"gtol": 1e-12})
    return float(res.fun), [s1] + list(np.exp(res.x))


def le_delay(stages, branches, h):
    gs = [g for g, _ in stages]
    n = len(stages)
    return n * (math.prod(gs) * math.prod(branches) * h) ** (1 / n) + sum(p for _, p in stages)


# Example 1 and Problem 1
for key, (g, p), h in (("1a", INV, 4), ("1c", NAND2, 4), ("1e", NOR2, 4)):
    v.check(f"Ex 19-04.{key}", g * h + p)
    v.check(f"Ex 19-04.{key[0]}{chr(ord(key[1]) + 1)}", (g * h + p) * TAU * 1e12)
v.check("Ex 19-04.1g", (NOR2[0] * 4 + NOR2[1]) / 5)
v.check("19-04.1a", NAND3[0] * 3 + NAND3[1])
v.check("19-04.1b", NOR3[0] * 3 + NOR3[1])
v.check("19-04.1c", NAND4[0] * 3 + NAND4[1])

# Example 2: chains for H = 64, numerically sized
chains = {n: path_rc([INV] * n, [1] * n, 1.0, 64.0)[0] for n in (1, 2, 3, 4)}
v.check("Ex 19-04.2a", chains[1])
v.check("Ex 19-04.2b", chains[2])
v.check("Ex 19-04.2c", chains[3])
v.check("Ex 19-04.2d", chains[4])
nc = minimize_scalar(lambda x: x * 64 ** (1 / x) + x, bounds=(1, 10), method="bounded", options={"xatol": 1e-10}).x
v.check("Ex 19-04.2e", nc)
v.check("Ex 19-04.2f", chains[1] / chains[3])
v.check("Ex 19-04.2g", chains[3] * TAU * 1e12)
v.check("Ex 19-04.2h", chains[1] * TAU * 1e9)
sizes3 = path_rc([INV] * 3, [1] * 3, 1.0, 64.0)[1]
v.assert_true("three-stage sizes 1, 4, 16", np.allclose(sizes3, [1, 4, 16], rtol=1e-5), str(sizes3))

# Example 3: branching path
stages3 = [NAND2, NOR2, INV]
d3, s3 = path_rc(stages3, [2, 1, 1], 10.0, 200.0)
v.check("Ex 19-04.3a", NAND2[0] * NOR2[0] * INV[0])
v.check("Ex 19-04.3b", 2)
v.check("Ex 19-04.3c", 200 / 10)
v.check("Ex 19-04.3d", NAND2[0] * NOR2[0] * 2 * 20)
v.check("Ex 19-04.3e", (NAND2[0] * NOR2[0] * 2 * 20) ** (1 / 3))
v.check("Ex 19-04.3f", d3)
v.check("Ex 19-04.3g", d3 * TAU * 1e12)
v.check("Ex 19-04.3h", INV[0] * s3[2])
v.check("Ex 19-04.3i", NOR2[0] * s3[1])
v.check("Ex 19-04.3j", 2 * NOR2[0] * s3[1])
v.check("Ex 19-04.3k", NAND2[0] * s3[0])
v.assert_true("numerical optimum equals N F^(1/N) + P", abs(d3 - le_delay(stages3, [2, 1, 1], 20)) < 1e-8, f"{d3}")
v.assert_true("lab stage_input_caps matches",
              np.allclose(ef.stage_input_caps([4 / 3, 5 / 3, 1], [2, 1, 1], 10, 200),
                          [NAND2[0] * s3[0], NOR2[0] * s3[1], s3[2]], rtol=1e-6), "")
d3nb = path_rc(stages3, [1, 1, 1], 10.0, 200.0)[0]
v.check("Ex 19-04.3l", NAND2[0] * NOR2[0] * 20)
v.check("Ex 19-04.3m", d3 - d3nb)
v.check("Lab 19-04.h", brentq(lambda h: le_delay([NAND2, NOR2, NAND2, INV], [1] * 4, h)
                              - le_delay([NAND4, NOR2], [1, 1], h), 1, 100, xtol=1e-12))

# Example 4: pad driver
H4 = 10e-12 / 2e-15
d4 = {n: path_rc([INV] * n, [1] * n, 1.0, H4)[0] for n in (5, 6, 7, 8)}
v.check("Ex 19-04.4a", H4)
v.check("Ex 19-04.4b", math.log(H4) / math.log(ef.best_stage_effort(1.0)))
v.check("Ex 19-04.4c", d4[6])
v.check("Ex 19-04.4d", d4[7])
v.check("Ex 19-04.4e", d4[8])
v.assert_true("seven stages best among 5-8", min(d4, key=d4.get) == 7, str(d4))
v.check("Ex 19-04.4f", d4[7] * TAU * 1e12)
v.check("Ex 19-04.4g", (H4 + 1) * TAU * 1e9)
v.check("Ex 19-04.4h", H4 ** (1 / 7))
v.check("Ex 19-04.4i", 100 * (d4[6] / d4[7] - 1))


# Example 5: best stage effort by minimizing the continuous chain delay per ln F
def rho_num(pinv):
    return minimize_scalar(lambda f: (f + pinv) / math.log(f), bounds=(1.5, 20), method="bounded",
                           options={"xatol": 1e-12}).x


v.check("Ex 19-04.5a", rho_num(0.0))
v.check("Ex 19-04.5b", rho_num(1.0))
v.check("Ex 19-04.5c", rho_num(2.0))
r1 = (rho_num(1.0) + 1) / math.log(rho_num(1.0))
v.check("Ex 19-04.5d", 3.4 / math.log(2.4))
v.check("Ex 19-04.5e", 7 / math.log(6))
v.check("Ex 19-04.5f", 100 * (3.4 / math.log(2.4) / r1 - 1))
v.check("Ex 19-04.5g", 100 * (7 / math.log(6) / r1 - 1))
v.assert_true("value per ln F equals rho at the optimum", abs(r1 - rho_num(1.0)) < 1e-6, "")
v.check("Lab 19-04.g", rho_num(3.0))
v.check("19-04.10a", rho_num(0.5))
v.assert_true("lab best_stage_effort matches", abs(ef.best_stage_effort(1.0) - rho_num(1.0)) < 1e-6, "")

# Example 6 and Problem 12: topologies for AND8
topo = {"a": ([NAND8, INV], [1, 1]), "b": ([NAND4, NOR2], [1, 1]), "c": ([NAND2, NOR2, NAND2, INV], [1] * 4)}
v.check("Ex 19-04.6a", path_rc(*topo["a"], 1.0, 10.0)[0])
v.check("Ex 19-04.6b", path_rc(*topo["b"], 1.0, 10.0)[0])
v.check("Ex 19-04.6c", NAND2[0] * NOR2[0] * NAND2[0])
v.check("Ex 19-04.6d", path_rc(*topo["c"], 1.0, 10.0)[0])
for h, keys in ((1.0, ("12a", "12b", "12c")), (100.0, ("12d", "12e", "12f"))):
    for t_, k in zip("abc", keys):
        v.check(f"19-04.{k}", path_rc(*topo[t_], 1.0, h)[0])

# Practitioner arithmetic
v.check("Txt 19-04.d", 13 * 5)
v.check("Txt 19-04.e", 65 / d3)
v.check("Txt 19-04.f", (1 + 2) / (1 + 2) * 2)  # equal-width NAND2: inverter's input capacitance, twice the pull-down R

# ---------------------------------------------------------------- Problems 2-9, 11
v.check("19-04.2a", NAND2[0])
v.check("19-04.2b", NAND2[0] * 12)
v.check("19-04.2c", (NAND2[0] * 12) ** (1 / 3))
v.check("19-04.2d", path_rc([INV, NAND2, INV], [1, 1, 1], 1.0, 12.0)[0])
v.check("19-04.3a", (1 + 2) / 1)
v.check("19-04.3b", (1 + 2 + 1) / 1)
d4p, s4p = path_rc([NAND3, NOR2, INV], [1, 1, 1], 6.0, 120.0)
v.check("19-04.4a", NAND3[0] * NOR2[0])
v.check("19-04.4b", NAND3[0] * NOR2[0] * 20)
v.check("19-04.4c", (NAND3[0] * NOR2[0] * 20) ** (1 / 3))
v.check("19-04.4d", d4p)
v.check("19-04.4e", s4p[2])
v.check("19-04.4f", NOR2[0] * s4p[1])
v.check("19-04.4g", NAND3[0] * s4p[0])
H5 = 2000 / 3
d5 = {n: path_rc([INV] * n, [1] * n, 1.0, H5)[0] for n in (4, 5, 6)}
v.check("19-04.5a", H5)
v.check("19-04.5b", math.log(H5) / math.log(rho_num(1.0)))
v.check("19-04.5c", d5[4])
v.check("19-04.5d", d5[5])
v.check("19-04.5e", d5[6])
v.check("19-04.5f", d5[5] * 15)
v.check("19-04.5g", 100 * (d5[4] / d5[5] - 1))
v.check("19-04.5h", 100 * (d5[6] / d5[5] - 1))
v.check("19-04.6a", NAND2[0] * 50 + NAND2[1])
v.check("19-04.6b", path_rc([NAND2, INV], [1, 1], 1.0, 50.0)[0])
d6c = path_rc([NAND2, INV, INV], [1, 1, 1], 1.0, 50.0)[0]
v.check("19-04.6c", d6c)
v.check("19-04.6d", (NAND2[0] * 50) ** (1 / 3))
v.check("19-04.7a", (1 + 1) + (1 + 1) + (64 + 1))
v.check("19-04.7b", 69 / chains[3])
tau8 = 22 / (4 + 1)
v.check("19-04.8a", tau8)
v.check("19-04.8b", (NAND2[0] * 4 + NAND2[1]) * tau8)
v.check("19-04.8c", d3 * tau8)
v.check("19-04.9a", path_rc([NOR2, INV], [1, 1], 1.0, 10.0)[0])
v.check("19-04.9b", path_rc([INV, NAND2], [1, 1], 1.0, 10.0)[0])
for n, kd, kc in ((2, "11a", "11b"), (3, "11c", "11d"), (4, "11e", "11f")):
    d_, s_ = path_rc([INV] * n, [1] * n, 1.0, 64.0)
    v.check(f"19-04.{kd}", d_)
    v.check(f"19-04.{kc}", sum(s_))
v.check("19-04.11g", 100 * (chains[2] / chains[3] - 1))
v.check("19-04.11h", 100 * (1 - 9 / 21))


# ---------------------------------------------------------------- transistor-level chains (independent ODE)
def chain_ode(sizes, c_load, k=200e-6, vdd=1.2, vt=0.35, cg=2e-15, cp=2e-15, trise=10e-12):
    n = len(sizes)
    caps = np.array([cp * sizes[i] + (cg * sizes[i + 1] if i + 1 < n else c_load) for i in range(n)])

    def ids(kk, vgs, vds):
        ov = vgs - vt
        if ov <= 0 or vds <= 0:
            return 0.0
        return kk * (ov * vds - vds * vds / 2) if vds < ov else kk * ov * ov / 2

    def f(t, x):
        out = np.zeros(n)
        for i in range(n):
            vin = vdd * min(1.0, t / trise) if i == 0 else x[i - 1]
            kk = k * sizes[i]
            out[i] = (ids(kk, vdd - vin, vdd - x[i]) - ids(kk, vin, x[i])) / caps[i]
        return out
    x0 = np.array([vdd * ((i + 1) % 2) for i in range(n)])
    t_end = 5e-9
    sol = solve_ivp(f, (0, t_end), x0, method="Radau", rtol=1e-9, atol=1e-13, dense_output=True,
                    max_step=trise / 2)
    tt = np.linspace(0, t_end, 500001)
    y = sol.sol(tt)[-1] - vdd / 2
    idx = np.nonzero(np.sign(y[:-1]) != np.sign(y[1:]))[0][0]
    tc = tt[idx] - y[idx] * (tt[idx + 1] - tt[idx]) / (y[idx + 1] - y[idx])
    return tc - trise / 2


t1 = chain_ode([1], 128e-15)
t2 = chain_ode([1, 8], 128e-15)
t3 = chain_ode([1, 4, 16], 128e-15)
t4 = chain_ode([1, 64 ** 0.25, 8, 64 ** 0.75], 128e-15)
v.check("Lab 19-04.a", t1 * 1e12)
v.check("Lab 19-04.b", t3 * 1e12)
v.check("Lab 19-04.c", t1 / t3)
v.check("Lab 19-04.d", t2 * 1e12)
v.check("Lab 19-04.e", t4 * 1e12)
v.check("Lab 19-04.f", t3 / TAU / 15)
v.check("Txt 19-04.b", t3 / TAU)
v.check("Txt 19-04.c", t1 / TAU)
v.assert_true("three stages best at transistor level", t3 < min(t1, t2, t4), "")
v.assert_true("lab simulate_chain matches", abs(ef.simulate_chain([1, 4, 16], 128e-15) - t3) < 1e-3 * t3, "")


# ---------------------------------------------------------------- complex and skewed gates, P/N ratio
def cap_units(nmos_w, pmos_w):
    return nmos_w + pmos_w


def unit_gate_efforts(mu):
    """Unit-drive widths for AOI21 / AOI22 (two-deep stacks get doubled widths) and the inverter reference."""
    inv = 1 + mu
    aoi21 = {"A": cap_units(2, 2 * mu), "C": cap_units(1, 2 * mu), "p": (2 + 1 + 2 * mu)}
    aoi22 = {"A": cap_units(2, 2 * mu), "p": (2 + 2 + 2 * mu + 2 * mu)}
    return ({k: v_ / inv for k, v_ in aoi21.items()}, {k: v_ / inv for k, v_ in aoi22.items()})


a21, a22 = unit_gate_efforts(2.0)
v.check("Txt 19-04.i", a21["A"])
v.check("Txt 19-04.j", a21["C"])
v.check("Txt 19-04.k", a21["p"])
v.check("19-04.13a", a22["A"])
v.check("19-04.13b", a22["p"])
b21, b22 = unit_gate_efforts(2.5)
v.check("19-04.13c", b21["A"])
v.check("19-04.13d", b21["C"])
v.check("19-04.13e", b21["p"])
v.check("19-04.13f", b22["A"])
v.check("19-04.13g", b22["p"])


def skew_efforts(n_w, p_w, n_stack=1, p_stack=1, mu=2.0):
    """Rising/falling logical effort: input capacitance over that of an inverter with the same edge strength."""
    cin = n_w + p_w
    up_strength = p_w / (p_stack * mu)      # pull-up strength relative to a unit inverter
    dn_strength = n_w / n_stack             # pull-down strength relative to a unit inverter
    gu = cin / (up_strength * (1 + mu))
    gd = cin / (dn_strength * (1 + mu))
    return gu, gd, (gu + gd) / 2


gu, gd, ga = skew_efforts(0.5, 2.0)
v.check("Txt 19-04.l", gu)
v.check("Txt 19-04.m", gd)
v.check("Txt 19-04.n", ga)
gu, gd, ga = skew_efforts(1.0, 1.0)
v.check("19-04.14a", gd)
v.check("19-04.14b", gu)
v.check("19-04.14c", ga)
gu, gd, ga = skew_efforts(1.0, 2.0, n_stack=2, p_stack=1)
v.check("19-04.14d", gu)
v.check("19-04.14e", gd)
v.check("19-04.14f", ga)


def pn_delay(beta, mu):
    return (1 + beta) * (1 + mu / beta)


for mu, kb, kg in ((2.0, "Txt 19-04.o", "Txt 19-04.p"), (2.5, "Txt 19-04.q", "Txt 19-04.r")):
    bopt = minimize_scalar(lambda b: pn_delay(b, mu), bounds=(0.5, 5), method="bounded", options={"xatol": 1e-12}).x
    v.check(kb, bopt)
    v.check(kg, 100 * (1 - pn_delay(bopt, mu) / pn_delay(mu, mu)))
v.check("Txt 19-04.g", 4 + 0.5)
v.check("Txt 19-04.h", 100 * (5 / 4.5 - 1))
v.check("19-04.8d", 22 / 4.5)
v.check("19-04.8e", 100 * (22 / 4.5 / tau8 - 1))

sys.exit(v.finish())
