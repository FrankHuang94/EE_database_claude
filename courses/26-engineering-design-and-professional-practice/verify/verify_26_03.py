#!/usr/bin/env python3
"""Verify every number in chapter 26-03 (engineering economics I), its problems and its lab.

Independent routes:
- interest factors by explicit summation of discounted payments (not the closed forms), and effective rates
  by simulating compounding;
- the cost stack by simulating a lot of units through the yield gates (expected cost per shipped unit);
- IRR by Brent's method against the lab's bisection; payback by stepping through cumulative cash;
- slips by building the cash flows directly with shifted times;
- the tornado by re-running the program model with perturbed inputs.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import econ  # noqa: E402

v = Verifier.from_files("26-03", ROOT / "chapters" / "26-03-engineering-economics-1.md",
                        ROOT / "solutions" / "26-03-solutions.md", LAB / "README.md")


def pa_sum(i, n):
    return sum((1 + i) ** -t for t in range(1, n + 1))


def fa_sum(i, n):
    return sum((1 + i) ** (n - t) for t in range(1, n + 1))


def npv_direct(rate, flows, times=None):
    times = range(len(flows)) if times is None else times
    return sum(cf * math.exp(-t * math.log1p(rate)) for cf, t in zip(flows, times))


def payback_by_interpolation(flows):
    """Second route for simple payback: walk the cumulative sum and interpolate inside the crossing year."""
    cum = 0.0
    for t, cf in enumerate(flows):
        if cum < 0 <= cum + cf and t > 0:
            return (t - 1) + (-cum) / cf
        cum += cf
    return float("nan")


def cascade_by_accounting(wafer, dpw, y_die, pkg, y_asm, test, y_test, royalty, lot=1_000_000):
    """Track a lot of good dies through assembly and test: total money spent / units shipped."""
    good_dies = lot
    spent = wafer * good_dies / (dpw * y_die)          # wafers bought to yield `lot` good dies
    spent += pkg * good_dies
    assembled = good_dies * y_asm
    spent += test * assembled
    shipped = assembled * y_test
    return spent / shipped + royalty


# ---------------------------------------------------------------- Example 1
v.check("Ex 26-03.1a", 100 * (25 - 10) / 25)
v.check("Ex 26-03.1a1", 100 * 15 / 10)
p65 = optimize.brentq(lambda p: (p - 10) / p - 0.65, 10.01, 1000)
v.check("Ex 26-03.1b", p65)
v.check("Ex 26-03.1c", 100 * (p65 / 25 - 1))

# ---------------------------------------------------------------- Example 2
dpw_raw = math.pi * 300**2 / 400 - math.pi * 300 / math.sqrt(200)
dpw = econ.dies_per_wafer(300, 100)
v.check("Ex 26-03.2a0", dpw_raw)
v.check("Ex 26-03.2a", dpw)
y = math.exp(-0.1)
v.check("Ex 26-03.2a1", y)
cs = econ.cost_stack(17000, dpw, y, 4.0, 0.99, 1.20, 0.98, 0.02 * 60)
cogs_acct = cascade_by_accounting(17000, dpw, y, 4.0, 0.99, 1.20, 0.98, 0.02 * 60)
v.assert_true("Ex 2 cost stack equals lot accounting", abs(cs["cogs"] - cogs_acct) < 1e-9)
v.check("Ex 26-03.2a2", cs["die"])
v.check("Ex 26-03.2b", cs["after_asm"])
v.check("Ex 26-03.2b1", cs["after_test"])
v.check("Ex 26-03.2c0", 0.02 * 60)
cogs = cs["cogs"]
v.check("Ex 26-03.2c", cogs)
v.check("Ex 26-03.2d", 100 * econ.gross_margin(60, cogs))
v.check("Ex 26-03.2d1", 100 * (60 - cogs) / cogs)
adder = cs["after_test"] - (cs["die"] + 4.0 + 1.20)
v.check("Ex 26-03.2e", adder)
v.check("Ex 26-03.2e1", 100 * cs["die"] / cogs)
v.check("Ex 26-03.2e2", 100 * adder / cogs)

# ---------------------------------------------------------------- Example 3
contrib = 60 - cogs
v.check("Ex 26-03.3a", contrib)
v.check("Ex 26-03.3a1", econ.breakeven_volume(60e6, 60, cogs) / 1e6)
v.check("Ex 26-03.3b", 60e6 / 1e7)
v.check("Ex 26-03.3b1", cogs + 6)
v.check("Ex 26-03.3b2", 100 * (60 - cogs - 6) / 60)
v.check("Ex 26-03.3b3", 100 * econ.gross_margin(60, cogs) - 100 * (60 - cogs - 6) / 60)
v.check("Ex 26-03.3c", 60e6 / 3e6)

# ---------------------------------------------------------------- Example 4
ap8 = 1 / pa_sum(0.08, 5)
af8 = 1 / fa_sum(0.08, 5)
v.assert_true("Ex 4 factors match closed forms", abs(ap8 - econ.a_p(0.08, 5)) < 1e-12 and abs(af8 - econ.a_f(0.08, 5)) < 1e-12)
v.assert_true("Ex 4 A/P - A/F = i", abs(ap8 - af8 - 0.08) < 1e-12)
v.check("Ex 26-03.4a", ap8)
v.check("Ex 26-03.4a1", af8)
v.check("Ex 26-03.4b0", 2.0 * ap8)
v.check("Ex 26-03.4b1", 0.3 * af8)
cr = 2.0e6 * ap8 - 0.3e6 * af8
# check: the annual payment CR repays 2.0 M less the PV of salvage
v.assert_true("Ex 4 CR annuity repays the net present cost", abs(cr * pa_sum(0.08, 5) - (2.0e6 - 0.3e6 * 1.08**-5)) < 1e-6)
v.check("Ex 26-03.4b", cr)
v.check("Ex 26-03.4c", (2.0e6 - 0.3e6) / 5)
v.check("Ex 26-03.4c1", 2.0 - 3 * 0.34)
v.check("Ex 26-03.4d", pa_sum(0.10, 5))

# ---------------------------------------------------------------- Example 5
units = [1e6, 3e6, 4e6, 2e6]
flows, times = econ.program_flows([30e6, 30e6], units, contrib)
for key, cf in zip(("Ex 26-03.5a", "Ex 26-03.5a1", "Ex 26-03.5a2", "Ex 26-03.5a3"), flows[2:]):
    v.check(key, cf / 1e6)
npv0 = npv_direct(0.12, flows, times)
v.check("Ex 26-03.5a4", npv0 / 1e6)
irr_b = optimize.brentq(lambda r: npv_direct(r, flows, times), 0.0, 5.0)
v.assert_true("Ex 5 IRR: Brent equals the lab's bisection", abs(irr_b - econ.irr(flows)) < 1e-9)
v.check("Ex 26-03.5a5", 100 * irr_b)
cum = np.cumsum(flows)
v.check("Ex 26-03.5a6", cum[2] / 1e6)
v.assert_true("Ex 5 payback: lab routine equals interpolation", abs(econ.payback(flows) - payback_by_interpolation(flows)) < 1e-9)
v.check("Ex 26-03.5a7", payback_by_interpolation(flows))
slipped = [-30e6, -30e6, 0.0] + [u * contrib for u in units[:3]]
npv1 = npv_direct(0.12, slipped)
f1, t1 = econ.program_flows([30e6, 30e6], units, contrib, slip=1.0, window_end=5.0)
v.assert_true("Ex 5 slipped flows equal the lab model", abs(econ.npv(0.12, f1, t1) - npv1) < 1e-3)
v.check("Ex 26-03.5b", npv1 / 1e6)
v.check("Ex 26-03.5c", (npv0 - npv1) / 1e6)
v.check("Ex 26-03.5c1", 100 * (npv0 - npv1) / npv0)
pvu = sum(u / 1.12**t for u, t in zip(units, (2, 3, 4, 5))) / 1e6
v.check("Ex 26-03.5d0", pvu)
c54 = 54.0 - cs["after_test"] - 0.02 * 54.0  # price cut 10%; the 2% royalty falls with it
v.check("Ex 26-03.5d3", contrib - c54)
d_asp = npv0 - npv_direct(0.12, econ.program_flows([30e6, 30e6], units, c54)[0])
d_nre = npv0 - npv_direct(0.12, econ.program_flows([33e6, 33e6], units, contrib)[0])
v.check("Ex 26-03.5d", d_asp / 1e6)
v.check("Ex 26-03.5d1", d_nre / 1e6)
v.check("Ex 26-03.5d2", d_asp / d_nre)

# ---------------------------------------------------------------- Example 6
ap10 = 1 / pa_sum(0.10, 5)
af10 = 1 / fa_sum(0.10, 5)
v.check("Ex 26-03.6a", ap10)
v.check("Ex 26-03.6a1", af10)
euac = 3.0 * ap10 + 0.4 - 0.5 * af10
# second route: NPV of buying over 5 years, annualized
npv_buy = 3.0 + sum(0.4 / 1.1**t for t in range(1, 6)) - 0.5 / 1.1**5
v.assert_true("Ex 6 EUAC equals annualized NPV", abs(euac - npv_buy * ap10) < 1e-12)
v.check("Ex 26-03.6b", euac)
v.check("Ex 26-03.6b1", (1.2 - euac) * 1e6)
v.check("Ex 26-03.6c", euac)
v.check("Ex 26-03.6d", 100 * (1.2 - euac) / 1.2)

# ---------------------------------------------------------------- Problems 1-5
v.check("26-03.1a", 10000 * econ.f_p(0.06, 8))
v.check("26-03.1b", 50000 * econ.p_f(0.07, 5))
bal = 1.0
for _ in range(12):
    bal *= 1 + 0.12 / 12
v.check("26-03.2a", 100 * (bal - 1))
v.check("26-03.2b", 100 * econ.effective_rate(0.12, None))
v.assert_true("P2 monthly compounding at 1e6 periods approaches continuous",
              abs(econ.effective_rate(0.12, 1e6) - (math.exp(0.12) - 1)) < 1e-6)
v.check("26-03.2c", 100 * (econ.effective_rate(0.12, None) - (bal - 1)))
v.check("26-03.3b", fa_sum(0.05, 10))
v.check("26-03.3c", 1e6 / fa_sum(0.05, 10))
v.check("26-03.4", 1 / pa_sum(0.09, 3))
v.check("26-03.4a", 12 / pa_sum(0.09, 3))
cf5 = [-10, 4, 4, 4, 2]
v.check("26-03.5a0", pa_sum(0.10, 3))
v.check("26-03.5a1", 1.1**-4)
v.check("26-03.5a", npv_direct(0.10, cf5))
v.check("26-03.5b", 100 * optimize.brentq(lambda r: npv_direct(r, cf5), 0, 1))
v.assert_true("P5 payback: lab routine equals interpolation", abs(econ.payback(cf5) - payback_by_interpolation(cf5)) < 1e-9)
v.check("26-03.5c", payback_by_interpolation(cf5))

# ---------------------------------------------------------------- Problems 6-9
dpw6_raw = math.pi * 300**2 / 800 - math.pi * 300 / math.sqrt(400)
dpw6 = econ.dies_per_wafer(300, 200)
y6 = math.exp(-0.3)
c6 = econ.cost_stack(12000, dpw6, y6, 6.0, 0.985, 2.50, 0.96, 0.50)
v.assert_true("P6 cost stack equals lot accounting",
              abs(c6["cogs"] - cascade_by_accounting(12000, dpw6, y6, 6.0, 0.985, 2.50, 0.96, 0.50)) < 1e-9)
v.check("26-03.6a0", dpw6_raw)
v.check("26-03.6a", dpw6)
v.check("26-03.6a1", y6)
v.check("26-03.6a2", c6["die"])
v.check("26-03.6b", c6["after_asm"])
v.check("26-03.6b1", c6["after_test"])
v.check("26-03.6c", c6["cogs"])
v.check("26-03.6d", 100 * econ.gross_margin(95, c6["cogs"]))
v.check("26-03.6d1", 100 * (95 - c6["cogs"]) / c6["cogs"])
ca = econ.cost_stack(17000, dpw, y, 4.0, 0.97, 1.20, 0.98, 1.20)["cogs"]
ct = econ.cost_stack(17000, dpw, y, 4.0, 0.99, 1.20, 0.96, 1.20)["cogs"]
v.check("26-03.7a", ca)
v.check("26-03.7a1", ca - cogs)
v.check("26-03.7b", ct)
v.check("26-03.7b1", ct - cogs)
v.check("26-03.8a", 25e6 / 8 / 1e6)
v.check("26-03.8b", 25e6 / 6 / 1e6)
v.check("26-03.8b1", 100 * (8 / 6 - 1))
v.check("26-03.8c", 25e6 / 5e6)
v.check("26-03.8c1", (20 - 8) + 25e6 / 5e6)
v.check("26-03.8c2", 100 * (20 - ((20 - 8) + 25e6 / 5e6)) / 20)
v.check("26-03.9", optimize.brentq(lambda a: (a - 30 - 0.03 * a) / a - 0.55, 31, 1000))

# ---------------------------------------------------------------- Problem 10
u10 = [2, 5, 6, 4]


def prog10(erosion):
    asp = [40 * (1 - erosion) ** k for k in range(4)]
    con = [a - 22 for a in asp]
    return asp, con, [-40, -40] + [u * c for u, c in zip(u10, con)]


asp10, con10, cf10 = prog10(0.10)
for i, a in enumerate(asp10):
    v.check(f"26-03.10a{i}" if i else "26-03.10a", a)
for i, c in enumerate(con10):
    v.check(f"26-03.10a{i + 4}", c)
for i, c in enumerate(cf10[2:]):
    v.check(f"26-03.10a{i + 8}", c)
v.check("26-03.10b", npv_direct(0.12, cf10))
v.check("26-03.10c", 100 * optimize.brentq(lambda e: npv_direct(0.12, prog10(e)[2]), 0, 0.9))

# ---------------------------------------------------------------- Problem 11
pv_sales = sum(u * contrib / 1.12**t for u, t in zip(units, (2, 3, 4, 5))) / 1e6
pv_nre = 30 + 30 / 1.12
v.check("26-03.11a", pv_sales)
h = npv_direct(0.12, [-30e6, -30e6] + [u * contrib for u in units], [0, 1, 2.5, 3.5, 4.5, 5.5]) / 1e6
v.assert_true("P11 half-year delay equals discounting the sales by 1.12^0.5",
              abs(h - (pv_sales / 1.12**0.5 - pv_nre)) < 1e-9)
v.check("26-03.11b", h)
v.check("26-03.11b1", npv0 / 1e6 - h)
full = pv_sales / 1.12 - pv_nre
v.check("26-03.11c", full)
v.check("26-03.11c1", npv0 / 1e6 - full)
window = (npv0 - npv1) / 1e6 - (npv0 / 1e6 - full)
v.check("26-03.11d", window)
v.check("26-03.11d1", 100 * window / ((npv0 - npv1) / 1e6))

# ---------------------------------------------------------------- Problems 12-14
a4, a6 = 1 / pa_sum(0.10, 4), 1 / pa_sum(0.10, 6)
v.check("26-03.12a", a4)
v.check("26-03.12a1", a6)
ea, eb = 2.0 * a4 + 0.3, 3.0 * a6 + 0.2
v.check("26-03.12b", ea)
v.check("26-03.12b1", eb)
v.check("26-03.12c", (ea - eb) * 1e6)
v.check("26-03.13a", (5.0 - 0.5) / 5)
v.check("26-03.13a1", 5.0 - 2 * 0.9)
v.check("26-03.13b", 0.21 * 0.9)
v.check("26-03.13b1", 0.21 * 0.9 * pa_sum(0.10, 5))


def model(p):
    con = p["asp"] * (1 - 0.02) - p["cogs"]  # "cogs" here is the manufacturing cost; the royalty is 2% of ASP
    f, t = econ.program_flows([p["nre"] / 2, p["nre"] / 2], [p["vol"] * u for u in (1, 3, 4, 2)], con)
    return econ.npv(0.12, f, t) / 1e6


base = {"asp": 60.0, "cogs": cs["after_test"], "vol": 1e6, "nre": 60e6}
tor = {k: abs(hi - lo) / 2 for k, lo, hi in econ.tornado(base, model)}
v.assert_true("P14 tornado order ASP, COGS, volume, NRE",
              [k for k, *_ in econ.tornado(base, model)] == ["asp", "cogs", "vol", "nre"])
v.check("26-03.14a", tor["asp"])
v.check("26-03.14b", tor["vol"])
v.check("26-03.14c", tor["cogs"])
v.check("26-03.14d", tor["nre"])
v.check("26-03.14e", 0.1 * cs["after_test"])
v.check("26-03.14e1", 0.1 * contrib)

# ---------------------------------------------------------------- Lab
c90 = econ.cost_stack(17000, dpw, y, 4.0, 0.99, 1.20, 0.90, 1.20)["cogs"]
v.check("Lab 26-03.a", c90)
v.check("Lab 26-03.a1", c90 - cogs)
v.check("Lab 26-03.a2", 100 * econ.gross_margin(60, c90))
v.check("Lab 26-03.b", optimize.brentq(lambda vol: 60e6 / vol - 2.0, 1e5, 1e9) / 1e6)
f_h, t_h = econ.program_flows([30e6, 30e6], units, contrib, slip=0.5, window_end=5.0)
# second route: half of year-5 units lost, all sales half a year later
direct = npv_direct(0.12, [-30e6, -30e6] + [u * contrib for u in units[:3]] + [0.5 * units[3] * contrib],
                    [0, 1, 2.5, 3.5, 4.5, 5.5])
v.assert_true("Lab six-month slip: model equals direct construction", abs(econ.npv(0.12, f_h, t_h) - direct) < 1e-3)
v.check("Lab 26-03.c", direct / 1e6)
v.check("Lab 26-03.c1", (npv0 - direct) / 1e6)
v.check("Lab 26-03.c2", 100 * (1 - 1.12**-0.5))
v.check("Lab 26-03.c3", 100 * (1 - 1 / 1.12))

# ---------------------------------------------------------------- Problem 16 (gradient by explicit summation)
g_flows = [50_000 + 10_000 * (t - 1) for t in range(1, 6)]
pw16 = sum(c / 1.08**t for t, c in enumerate(g_flows, 1))
pg16 = sum((t - 1) / 1.08**t for t in range(1, 6))
v.check("26-03.16a", pg16)
v.check("26-03.16a1", pg16 / pa_sum(0.08, 5))
v.assert_true("P16 closed forms equal the sums",
              abs(pg16 - (1.08**5 - 1 - 5 * 0.08) / (0.08**2 * 1.08**5)) < 1e-12
              and abs(pg16 / pa_sum(0.08, 5) - (1 / 0.08 - 5 / (1.08**5 - 1))) < 1e-12)
v.check("26-03.16b", pw16)
v.check("26-03.16c", pw16 / pa_sum(0.08, 5))

# ---------------------------------------------------------------- Problem 17 (perpetuity by a long sum; B/C by direct PVs)
v.check("26-03.17a", sum(0.3 / 1.06**t for t in range(1, 5001)))
pv = lambda flows: sum(c / 1.10**t for t, c in enumerate(flows))  # noqa: E731
cost_b, ben_b = pv([4.0, 1.0, 1.0, 1.0, 1.0]), pv([0, 3.0, 3.0, 3.0, 3.0])
cost_x, ben_x = pv([6.0, 1.2, 1.2, 1.2, 1.2]), pv([0, 3.8, 3.8, 3.8, 3.8])
v.check("26-03.17b", ben_b / cost_b)
v.check("26-03.17b1", ben_b - cost_b)
v.check("26-03.17b2", ben_x / cost_x)
v.check("26-03.17b3", ben_x - cost_x)
v.check("26-03.17c", (ben_x - ben_b) / (cost_x - cost_b))
v.assert_true("P17 the incremental test agrees with NPV", ((ben_x - ben_b) / (cost_x - cost_b) < 1) == (ben_b - cost_b > ben_x - cost_x))

# ---------------------------------------------------------------- Txt (margin and markup)
markup = lambda gm: gm / (1 - gm)  # noqa: E731
v.check("Txt 26-03.a", 100 * markup(0.60))
v.check("Txt 26-03.b", 100 * markup(0.90))
v.check("Txt 26-03.c", 100 * 0.5 / 1.5)
v.check("Txt 26-03.d", 100 * 0.40 / 0.60)
v.check("Txt 26-03.e", 100 * 0.40 / 1.40)

sys.exit(v.finish())
