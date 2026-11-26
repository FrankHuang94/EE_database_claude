#!/usr/bin/env python3
"""Verify every number in chapter 26-04 (engineering economics II), its problems and its lab.

Independent routes:
- present values by stepping a balance backward year by year (not the closed sums used in the lab);
- licence/build break-evens and thresholds by root-finding on the cost difference (brentq);
- the effective density gain by shrinking each block's area and adding areas, not by the harmonic formula;
- dies per wafer from the formula coded here, and good-die and package costs by lot accounting (money spent
  divided by good units out);
- TCO by integrating power over the service life in joules and converting to kWh;
- the decision tree by enumerating every second-generation policy and taking the cheapest.
The lab module's functions are checked against these routes with assert_true.
"""
from __future__ import annotations

import math
import sys
from itertools import product
from pathlib import Path

from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sourcing  # noqa: E402

v = Verifier.from_files("26-04", ROOT / "chapters" / "26-04-engineering-economics-2.md",
                        ROOT / "solutions" / "26-04-solutions.md", LAB / "README.md")
M = 1e6


def pv_backward(flows_by_year: dict[int, float], rate: float) -> float:
    """Discount by carrying a balance back one year at a time from the last year to year 0."""
    last = max(flows_by_year)
    bal = 0.0
    for t in range(last, -1, -1):
        bal = bal + flows_by_year.get(t, 0.0)
        if t > 0:
            bal /= 1 + rate
    return bal


def dpw(area: float, d: float = 300.0) -> tuple[float, int]:
    raw = math.pi * d * d / (4 * area) - math.pi * d / math.sqrt(2 * area)
    return raw, math.floor(raw)


def good_die_by_lot(wafer: float, area: float, d0: float, test: float = 0.0, wafers: int = 1000):
    """Buy `wafers` wafers, test every die, keep the good ones: money spent / good dies."""
    n = dpw(area)[1]
    y = math.exp(-area / 100 * d0)
    dies = wafers * n
    spent = wafers * wafer + dies * test
    return n, y, spent / (dies * y)


def package_by_lot(die_costs: list[float], pkg: float, attach: float, lot: int = 1_000_000) -> float:
    """Assemble `lot` packages from good dies; each attach succeeds with probability `attach`."""
    spent = lot * (sum(die_costs) + pkg)
    good = lot * attach ** len(die_costs)
    return spent / good


def slot_tco_joules(price, kw, years, pue, usd_kwh, overhead):
    joules = kw * 1e3 * pue * years * 365 * 24 * 3600
    return price + overhead + joules / 3.6e6 * usd_kwh


# ---------------------------------------------------------------- Example 1
asp = [40 * 0.88**k for k in range(4)]
vol = [3, 5, 5, 3]
for key, a in zip(("Ex 26-04.1a", "Ex 26-04.1a1", "Ex 26-04.1a2"), asp[1:]):
    v.check(key, a)
roy = [0.02 * a for a in asp]
for key, r in zip(("Ex 26-04.1a3", "Ex 26-04.1a4", "Ex 26-04.1a5", "Ex 26-04.1a6"), roy):
    v.check(key, r)
fixed_tot = 0.80 * sum(vol)
pct_tot = sum(r * u for r, u in zip(roy, vol))
v.check("Ex 26-04.1b", fixed_tot)
v.check("Ex 26-04.1b1", pct_tot)
v.check("Ex 26-04.1b2", fixed_tot - pct_tot)
v.check("Ex 26-04.1b3", 100 * pct_tot / fixed_tot)
v.check("Ex 26-04.1c", roy[3] / roy[0])
v.assert_true("Ex 1 lab royalties match", all(abs(a - b) < 1e-12 for a, b in
              zip(roy, sourcing.royalty_per_unit(sourcing.eroding_prices(40, 0.12, 4), 0.02))))

# ---------------------------------------------------------------- Example 2
U = pv_backward({t + 1: u for t, u in enumerate(vol)}, 0.12)
v.assert_true("Ex 2 discounted units match lab", abs(U - sourcing.discounted_units(vol, 0.12)) < 1e-12)
v.check("Ex 26-04.2a", (24 - 6) / 0.80)
v.check("Ex 26-04.2a1", sum(vol))
v.check("Ex 26-04.2b", U)
for key, t in zip(("Ex 26-04.2b0", "Ex 26-04.2b01", "Ex 26-04.2b02", "Ex 26-04.2b03"), range(4)):
    v.check(key, vol[t] / 1.12 ** (t + 1))
lic = pv_backward({0: 6.0, **{t + 1: 0.80 * u for t, u in enumerate(vol)}}, 0.12)
build = 24 + 0.25 * 15
v.check("Ex 26-04.2b1", lic)
v.check("Ex 26-04.2b2", lic - 6.0)
v.check("Ex 26-04.2b3", build)
v.check("Ex 26-04.2b4", build - lic)
ustar = optimize.brentq(lambda u: 6.0 + 0.80 * u - build, 0, 1000)
v.assert_true("Ex 2 U* matches lab", abs(ustar - sourcing.breakeven_discounted_units(build, 6.0, 0.80)) < 1e-9)
v.check("Ex 26-04.2c", ustar)
v.check("Ex 26-04.2c1", ustar / U)
v.check("Ex 26-04.2c2", 0.25 * 15)
v.check("Ex 26-04.2d", 0.80 * sum(vol))

# ---------------------------------------------------------------- Example 3
frac, gain = [0.5, 0.3, 0.2], [1.7, 1.2, 1.1]
blocks = [100 * f for f in frac]                       # mm2 of each block at N5
new_area = sum(b / g for b, g in zip(blocks, gain))
seff = 100 / new_area
v.assert_true("Ex 3 area-sum gain equals harmonic formula",
              abs(seff - sourcing.effective_density_gain(frac, gain)) < 1e-12)
v.check("Ex 26-04.3a", seff)
for key, f, g in zip(("Ex 26-04.3a0", "Ex 26-04.3a01", "Ex 26-04.3a02"), frac, gain):
    v.check(key, f / g)
v.check("Ex 26-04.3a1", new_area)
v.check("Ex 26-04.3a2", 100 / 1.7)
v.check("Ex 26-04.3b", 100 / (blocks[1] / 1.2 + blocks[2] / 1.1))
raw5, n5 = dpw(100)
_, y5, c5 = good_die_by_lot(17000, 100, 0.10)
raw3, n3 = dpw(new_area)
_, y3, c3 = good_die_by_lot(20000, new_area, 0.10)
v.check("Ex 26-04.3c", n5)
v.check("Ex 26-04.3c0", raw5)
v.check("Ex 26-04.3c1", y5)
v.check("Ex 26-04.3c2", c5)
v.check("Ex 26-04.3c3", n3)
v.check("Ex 26-04.3c4", raw3)
v.check("Ex 26-04.3c5", y3)
v.check("Ex 26-04.3c6", c3)
v.check("Ex 26-04.3c7", c5 - c3)
v.check("Ex 26-04.3c8", new_area / 100 * 0.10)
v.assert_true("Ex 3 lab die costs match lot accounting",
              abs(sourcing.good_die_cost(17000, 100, 0.10)[2] - c5) < 1e-9 and
              abs(sourcing.good_die_cost(20000, new_area, 0.10)[2] - c3) < 1e-9)
vstar = optimize.brentq(lambda V: V * (c5 - c3) - 30, 0, 1000)
v.check("Ex 26-04.3d", vstar)
cpf = (20000 / 17000) * new_area / 100
v.check("Ex 26-04.3e", cpf)
_, y3b, c3b = good_die_by_lot(20000, new_area, 0.20)
v.check("Ex 26-04.3e1", y3b)
v.check("Ex 26-04.3e2", c3b)
v.check("Ex 26-04.3e3", c5 - c3b)
v.check("Ex 26-04.3e4", 30 / (c5 - c3b))
v.check("Ex 26-04.3e5", 100 * (1 - new_area / 100))
v.check("Ex 26-04.3e6", 100 * (1 - cpf))

# ---------------------------------------------------------------- Example 4
dS = good_die_by_lot(20000, 200, 0.10, 2)
dL = good_die_by_lot(20000, 350, 0.10, 2)
dC = good_die_by_lot(20000, 165, 0.10, 2)
dI = good_die_by_lot(10000, 55, 0.08, 2)
for keys, d in ((("Ex 26-04.4a", "Ex 26-04.4a1", "Ex 26-04.4a2"), dS),
                (("Ex 26-04.4a3", "Ex 26-04.4a4", "Ex 26-04.4a5"), dL),
                (("Ex 26-04.4a6", "Ex 26-04.4a7", "Ex 26-04.4a8"), dC),
                (("Ex 26-04.4a9", "Ex 26-04.4a10", "Ex 26-04.4a11"), dI)):
    for k, x in zip(keys, d):
        v.check(k, x)
Sm = package_by_lot([dS[2]], 15, 0.99)
Sc = package_by_lot([dC[2], dI[2]], 25, 0.99)
Lm = package_by_lot([dL[2]], 15, 0.99)
Lc = package_by_lot([dC[2], dC[2], dI[2]], 35, 0.99)
v.assert_true("Ex 4 lab package cost matches lot accounting",
              abs(sourcing.package_cost([dC[2], dC[2], dI[2]], 35, 0.99) - Lc) < 1e-9)
v.check("Ex 26-04.4b", Sm)
v.check("Ex 26-04.4b1", Sc)
v.check("Ex 26-04.4b2", Sc - Sm)
v.check("Ex 26-04.4b3", Lm)
v.check("Ex 26-04.4b4", Lc)
v.check("Ex 26-04.4b5", Lm - Lc)
tot_m = 90 + 100 + 4 * Sm + 1 * Lm
nre_c = 80 + 30 + 2 * 8
tot_c = nre_c + 4 * Sc + 1 * Lc
v.check("Ex 26-04.4c", tot_m)
v.check("Ex 26-04.4c1", nre_c)
v.check("Ex 26-04.4c2", tot_c)
v.check("Ex 26-04.4c3", tot_m - tot_c)
v.check("Ex 26-04.4c4", 190 - nre_c)
v.check("Ex 26-04.4c5", 4 * (Sc - Sm) - (Lm - Lc))
v.assert_true("Ex 4 saving decomposes", abs((tot_m - tot_c) - ((190 - nre_c) - (4 * (Sc - Sm) - (Lm - Lc)))) < 1e-9)
v.check("Ex 26-04.4d", 90 + 4 * Sm)
v.check("Ex 26-04.4d1", 118 + 4 * Sc)
v.check("Ex 26-04.4d2", 118 + 4 * Sc - 90 - 4 * Sm)
flip = optimize.brentq(lambda V: (190 + V * Sm + Lm) - (126 + V * Sc + Lc), 0, 1000)
v.check("Ex 26-04.4e", flip)
v.check("Ex 26-04.4f", 100 * dS[1])
v.check("Ex 26-04.4f1", 100 * dL[1])

# ---------------------------------------------------------------- Example 5
Em = slot_tco_joules(0, 1.0, 4, 1.3, 0.08, 0)
Ec = slot_tco_joules(0, 0.7, 4, 1.3, 0.08, 0)
Tm = slot_tco_joules(30000, 1.0, 4, 1.3, 0.08, 12000)
Tc = slot_tco_joules(9000, 0.7, 4, 1.3, 0.08, 12000)
v.assert_true("Ex 5 lab TCO matches joule integration",
              abs(sourcing.slot_tco(9000, 0.7, 4, 1.3, 0.08, 12000) - Tc) < 1e-6)
v.check("Ex 26-04.5a", Em)
v.check("Ex 26-04.5a1", Ec)
v.check("Ex 26-04.5a2", Tm)
v.check("Ex 26-04.5a3", Tc)
tm, tc = Tm / 1.0, Tc / 0.8
v.check("Ex 26-04.5b", tc)
v.check("Ex 26-04.5b1", tm - tc)
be = optimize.brentq(lambda n: n * (tm - tc) - 800 * M, 1, 1e9)
v.check("Ex 26-04.5b2", be)
v.check("Ex 26-04.5b3", be / 0.8)
tm2 = slot_tco_joules(20000, 1.0, 4, 1.3, 0.08, 12000)
v.check("Ex 26-04.5c", tm2)
v.check("Ex 26-04.5c1", tm2 - tc)
be2 = 800 * M / (tm2 - tc)
v.check("Ex 26-04.5c2", be2)
v.check("Ex 26-04.5c3", be2 / 0.8)
v.check("Ex 26-04.5c4", be2 / be)
neq = 200000 * 0.8
v.check("Ex 26-04.5d1", neq)
ceil = optimize.brentq(lambda p: slot_tco_joules(p, 1.0, 4, 1.3, 0.08, 12000) - (tc + 800 * M / neq), 0, 1e6)
v.assert_true("Ex 5 lab ceiling matches root",
              abs(sourcing.merchant_price_ceiling(tc, 800 * M, neq, 1.0, 4, 1.3, 0.08, 12000) - ceil) < 1e-6)
v.check("Ex 26-04.5d", ceil)
v.check("Ex 26-04.5e", 30000 * (1 - 0.75))
v.check("Ex 26-04.5e1", 100 * (1 - 7500 / ceil))


# ---------------------------------------------------------------- Example 6 (policy enumeration)
def best_tree(gen1_lic, gen1_build, port, up2, r, u2, probs, build2):
    """Expected cost of every strategy: commit to build now, or license now with a gen-2 policy per outcome."""
    costs = {"build_now": gen1_build + port}
    for policy in product(("renew", "build"), repeat=len(u2)):
        c = gen1_lic + sum(p * (up2 + r * u if act == "renew" else build2)
                           for p, u, act in zip(probs, u2, policy))
        costs["license:" + ",".join(policy)] = c
    return costs


costs = best_tree(lic, build, 3, 5, 0.80, [25, 6], [0.3, 0.7], 22)
flex = min(c for k, c in costs.items() if k.startswith("license:"))
both = costs["license:renew,renew"]
lab = sourcing.two_generation_costs(lic, build, 3, 5, 0.80, [25, 6], [0.3, 0.7], 22)
v.assert_true("Ex 6 lab tree matches enumeration",
              abs(lab["license_then_choose"] - flex) < 1e-9 and abs(lab["license_both"] - both) < 1e-9)
v.assert_true("Ex 6 best licence policy is build-if-high, renew-if-low", costs["license:build,renew"] == flex)
v.check("Ex 26-04.6a", costs["build_now"])
v.check("Ex 26-04.6b", 5 + 0.80 * 25)
v.check("Ex 26-04.6b1", 5 + 0.80 * 6)
v.check("Ex 26-04.6b2", flex)
v.check("Ex 26-04.6c", 0.3 * 25 + 0.7 * 6)
v.check("Ex 26-04.6c1", both)
v.check("Ex 26-04.6d", both - flex)
v.check("Ex 26-04.6d1", costs["build_now"] - flex)
pstar = optimize.brentq(lambda p: min(c for k, c in best_tree(lic, build, 3, 5, 0.80, [25, 6], [p, 1 - p], 22).items()
                                      if k.startswith("license:")) - (build + 3), 0.01, 0.99)
v.check("Ex 26-04.6e", pstar)

# ---------------------------------------------------------------- text and concept checks
v.check("Txt 26-04.1", 2 / (1 / 1.7 + 1 / 1.1))
v.check("Txt 26-04.2", (1.7 + 1.1) / 2)
v.check("Txt 26-04.3", 100 * 0.04 / 0.50)
v.check("Txt 26-04.4", 100 * (1 / 0.8 - 1))
v.check("Txt 26-04.5", 1 / 0.5)
v.check("Txt 26-04.6", 100 * 2.61 / 4.92)
v.check("Txt 26-04.7", 100 * 670 / (773 + 670))
v.check("Txt 26-04.8", 1751.8 / 1000)
v.check("Txt 26-04.9", 1906.3 / 1000)
v.check("Txt 26-04.10", 100 * (1 - 1751.8 / 1906.3))
v.check("Txt 26-04.11", (10 - 2) / 0.50)
v.check("Txt 26-04.12", 2 + 0.50 * 10)
g_cc = 1 / (0.4 / 2 + 0.4 / 1.1 + 0.2 / 1)
v.check("Txt 26-04.13", g_cc)
v.check("Txt 26-04.14", 100 * (1 - 1 / g_cc))
v.check("Txt 26-04.15", 1.20 / 1.15)
v.check("Txt 26-04.16", 100 * (1.20 / 1.15 - 1))
e_year = 1.0 * 1.3 * 8760 * 0.08  # Example 26-04.5 merchant energy per year
v.check("Txt 26-04.17", sum(e_year / 1.10**t for t in range(1, 5)))

# ---------------------------------------------------------------- Problem 1
v.check("26-04.1a", 100 * 0.45 / 18)
v.check("26-04.1b", 0.015 * 22)
v.check("26-04.1c", 0.005 * 300)
v.check("26-04.1c1", 100 * 0.005 * 300 / 15)
v.check("26-04.1d", 100 * (0.55 * 15 - 1.50) / 15)

# ---------------------------------------------------------------- Problem 3
v.check("26-04.3a", optimize.brentq(lambda V: 1.5 + 0.25 * V - 9, 0, 1000))
v.check("26-04.3b", 1.5 + 0.25 * 20)
v.check("26-04.3b1", 9 - (1.5 + 0.25 * 20))
v.check("26-04.3c", 9 + 0.2 * 6)
v.check("26-04.3c1", optimize.brentq(lambda V: 1.5 + 0.25 * V - 10.2, 0, 1000))

# ---------------------------------------------------------------- Problem 4
vol4 = {2: 2, 3: 6, 4: 8, 5: 6, 6: 3}
U4 = pv_backward(vol4, 0.10)
v.assert_true("P4 matches lab with a two-year delay",
              abs(U4 - sourcing.discounted_units(list(vol4.values()), 0.10, first_year=2)) < 1e-12)
v.check("26-04.4a", U4)
for key, t in zip(("26-04.4a1", "26-04.4a2", "26-04.4a3", "26-04.4a4", "26-04.4a5"), range(2, 7)):
    v.check(key, vol4[t] / 1.1**t)
b4 = pv_backward({0: 10, 1: 10}, 0.10)
l4 = pv_backward({0: 4, **{t: 0.60 * u for t, u in vol4.items()}}, 0.10)
v.check("26-04.4b", b4)
v.check("26-04.4b1", l4)
v.check("26-04.4b2", l4 - 4)
v.check("26-04.4b3", b4 - l4)
u4s = optimize.brentq(lambda u: 4 + 0.60 * u - b4, 0, 1000)
v.check("26-04.4c", u4s)
v.check("26-04.4c1", u4s / U4)
v.check("26-04.4c2", 100 * (l4 - 4) / b4)
v.check("26-04.4c3", 100 * (lic - 6.0) / build)

# ---------------------------------------------------------------- Problem 5
asp5 = [25 * 0.8**k for k in range(4)]
for key, a in zip(("26-04.5a", "26-04.5a1", "26-04.5a2", "26-04.5a3"), asp5):
    v.check(key, 0.016 * a)
U5 = pv_backward({t: 10 for t in range(1, 5)}, 0.10)
v.check("26-04.5b", U5)
v.check("26-04.5b0", U5 / 10)
fix5 = 0.40 * U5
pct5 = pv_backward({t + 1: 0.016 * a * 10 for t, a in enumerate(asp5)}, 0.10)
v.assert_true("P5 matches lab", abs(pct5 - sourcing.percent_license_pv(0, 0.016, asp5, [10] * 4, 0.10)) < 1e-12)
v.check("26-04.5b1", fix5)
v.check("26-04.5b2", pct5)
v.check("26-04.5c", pct5 / U5)
pct10 = pv_backward({t + 1: 0.016 * 25 * 0.9**t * 10 for t in range(4)}, 0.10)
v.check("26-04.5d", pct10)
v.check("26-04.5d1", pct10 / U5)
lo = optimize.brentq(lambda rho: rho / 0.016 * pct10 - fix5, 1e-4, 0.2)
hi = optimize.brentq(lambda rho: rho / 0.016 * pct5 - fix5, 1e-4, 0.2)
v.check("26-04.5d2", 100 * lo)
v.check("26-04.5d3", 100 * hi)

# ---------------------------------------------------------------- Problem 6
R6 = 0.015 * 30 + 0.20 + 0.05 + 0.30 + 0.25
v.check("26-04.6a", R6)
v.check("26-04.6a1", 0.015 * 30)
v.check("26-04.6a2", 0.20 + 0.05 + 0.30 + 0.25)
v.check("26-04.6b", 100 * R6 / 30)
v.check("26-04.6c", 100 * (30 - 14) / 30)
v.check("26-04.6c1", 100 * (30 - 14 - R6) / 30)
v.check("26-04.6d", 100 * R6 / (30 - 14))

# ---------------------------------------------------------------- Problem 7
for key, f in (("26-04.7a", [0.60, 0.35, 0.05]), ("26-04.7b", [0.20, 0.50, 0.30])):
    v.check(key, 100 / sum(100 * x / g for x, g in zip(f, gain)))
v.check("26-04.7c", sum(400 * x / g for x, g in zip([0.60, 0.35, 0.05], gain)))

# ---------------------------------------------------------------- Problem 8
for keys, s_sram in ((("26-04.8a1", "26-04.8a2"), 1.0), (("26-04.8b", "26-04.8b1"), 1.1)):
    sl = optimize.brentq(lambda x: sourcing.effective_density_gain([0.5, 0.3, 0.2], [x, s_sram, 1.1]) - 1.3, 1.01, 20)
    v.check(keys[0], 0.5 / sl)
    v.check(keys[1], sl)
v.check("26-04.8a", 1 / 1.3)

# ---------------------------------------------------------------- Problem 9
v.check("26-04.9a", optimize.brentq(lambda w: (w / 17000) / seff - 1, 1000, 1e6))
v.check("26-04.9b", (30000 / 20000) / 1.15)
v.check("26-04.9c", 30000 / 20000)

# ---------------------------------------------------------------- Problem 10
d0s = optimize.brentq(lambda d: good_die_by_lot(20000, new_area, d)[2] - c5, 0.01, 2)
v.check("26-04.10a", math.exp(new_area / 100 * d0s))
v.check("26-04.10a1", d0s)
rows = [good_die_by_lot(20000, new_area, d) for d in (0.25, 0.15, 0.10)]
v.check("26-04.10b", rows[0][1])
v.check("26-04.10b1", rows[0][2])
v.check("26-04.10b2", c5 - rows[0][2])
v.check("26-04.10b3", rows[1][1])
v.check("26-04.10b4", rows[1][2])
v.check("26-04.10b5", c5 - rows[1][2])
tot10 = sum(u * (c5 - r[2]) for u, r in zip((1, 2, 3), rows))
v.check("26-04.10b6", tot10)
v.check("26-04.10b7", 6 * (c5 - c3))
v.check("26-04.10b8", new_area / 100 * 0.25)
v.check("26-04.10b9", new_area / 100 * 0.15)
v.assert_true("P10 the ramp makes N3 miss its NRE", tot10 < 30 < 6 * (c5 - c3))

# ---------------------------------------------------------------- Problem 11
dX = good_die_by_lot(20000, 650, 0.10, 2)
v.assert_true("P11 650 mm2 fits the 858 mm2 reticle", 650 < 26 * 33)
for k, x in zip(("26-04.11a", "26-04.11a1", "26-04.11a2"), dX):
    v.check(k, x)
Xm = package_by_lot([dX[2]], 15, 0.99)
Xc = package_by_lot([dC[2]] * 4 + [dI[2]], 50, 0.99)
v.check("26-04.11b", Xm)
v.check("26-04.11b1", Xc)
v.check("26-04.11b2", Xm - Xc)
inc_m, inc_c = 110 + 0.5 * Xm, 8 + 0.5 * Xc
v.check("26-04.11c", inc_m)
v.check("26-04.11c1", inc_c)
v.check("26-04.11c2", inc_m - inc_c)
v.check("26-04.11d", tot_m + inc_m)
v.check("26-04.11d1", tot_c + inc_c)
v.check("26-04.11d2", tot_m + inc_m - tot_c - inc_c)

# ---------------------------------------------------------------- Problem 12
dI3 = good_die_by_lot(20000, 55, 0.10, 2)
for k, x in zip(("26-04.12a", "26-04.12a1", "26-04.12a2"), dI3):
    v.check(k, x)
v.check("26-04.12a3", dI3[2] - dI[2])
Sc3 = package_by_lot([dC[2], dI3[2]], 25, 0.99)
v.check("26-04.12b", Sc3)
v.check("26-04.12c", Sc3 - Sc)

# ---------------------------------------------------------------- Problem 13
v.check("26-04.13a", slot_tco_joules(0, 1.0, 5, 1.3, 0.12, 0))
v.check("26-04.13a1", slot_tco_joules(0, 0.7, 5, 1.3, 0.12, 0))
tm13 = slot_tco_joules(30000, 1.0, 5, 1.3, 0.12, 12000)
tc13 = slot_tco_joules(9000, 0.7, 5, 1.3, 0.12, 12000) / 0.8
v.check("26-04.13b", tm13)
v.check("26-04.13b1", tc13)
v.check("26-04.13c", tm13 - tc13)
v.check("26-04.13d", 800 * M / (tm13 - tc13))
v.check("26-04.13d1", 800 * M / (tm13 - tc13) / 0.8)
v.check("26-04.13e", 0.7 / 0.8)
v.assert_true("P13 break-even falls", 800 * M / (tm13 - tc13) < be)

# ---------------------------------------------------------------- Problem 14
cost14 = 30000 * 0.30
v.check("26-04.14a", cost14)
ceil14 = optimize.brentq(lambda p: slot_tco_joules(p, 1.0, 4, 1.3, 0.08, 12000) - (tc + 800 * M / 80000), 0, 1e6)
v.check("26-04.14b", ceil14)
v.check("26-04.14b1", 100 * (1 - cost14 / ceil14))
at_cost = slot_tco_joules(cost14, 1.0, 4, 1.3, 0.08, 12000)
v.check("26-04.14c", at_cost)
v.check("26-04.14c1", tc)
floor14 = optimize.brentq(lambda p: slot_tco_joules(p, 1.0, 4, 1.3, 0.08, 12000) - tc, 0, 1e6)
v.check("26-04.14c2", floor14)
v.assert_true("P14 custom never pays against a merchant at cost", at_cost < tc and floor14 > cost14)

# ---------------------------------------------------------------- Problem 15
port_tie = optimize.brentq(lambda c: (build + c) - flex, -50, 50)
v.check("26-04.15a", port_tie)
p15 = optimize.brentq(lambda p: min(c for k, c in best_tree(lic, build, 1, 5, 0.80, [25, 6], [p, 1 - p], 22).items()
                                    if k.startswith("license:")) - (build + 1), 0.01, 0.99)
v.check("26-04.15b", p15)
c06 = best_tree(lic, build, 3, 5, 0.80, [25, 6], [0.6, 0.4], 22)
flex06 = min(c for k, c in c06.items() if k.startswith("license:"))
v.check("26-04.15c", c06["build_now"])
v.check("26-04.15c1", flex06)
v.check("26-04.15c2", 0.6 * 25 + 0.4 * 6)
v.check("26-04.15c3", c06["license:renew,renew"])
v.check("26-04.15c4", c06["license:renew,renew"] - flex06)
v.assert_true("P15 build now is best at p = 0.6", c06["build_now"] == min(c06.values()))

# ---------------------------------------------------------------- Problem 16
v.check("26-04.16a", 6000 / (1 - 0.40))
v.check("26-04.16a1", 6000 / (1 - 0.60))
tc16 = slot_tco_joules(15000, 0.7, 4, 1.3, 0.08, 12000) / 0.8
v.check("26-04.16b", tc16)
v.check("26-04.16b1", tm - tc16)
v.check("26-04.16b2", 800 * M / (tm - tc16))
v.check("26-04.16c", 30000 - 6000)
v.check("26-04.16c1", 10000 - 6000)
v.check("26-04.16c2", (30000 - 6000) - (10000 - 6000))

# ---------------------------------------------------------------- lab
v.check("Lab 26-04.a", optimize.brentq(lambda n: n + 0.25 * 15 - lic, 0, 100))
rest = blocks[1] / 1.2 / 100 + blocks[2] / 1.1 / 100
v.check("Lab 26-04.b", optimize.brentq(lambda x: 1 / (0.5 / x + rest) - 1.5, 1.01, 50))
v.check("Lab 26-04.b1", rest)
v.check("Lab 26-04.b2", 1 / (0.5 / 3 + rest))
v.check("Lab 26-04.b3", 1 / (0.5 / 10 + rest))
v.check("Lab 26-04.c", flip)
v.check("Lab 26-04.d", floor14)

sys.exit(v.finish())
