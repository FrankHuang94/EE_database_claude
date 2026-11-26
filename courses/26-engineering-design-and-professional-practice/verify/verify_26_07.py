#!/usr/bin/env python3
"""Verify every number in chapter 26-07 (engineering ethics), its problems and its lab.

Independent routes:
- fleet probabilities from the binomial distribution (scipy.stats) rather than the closed form in the lab;
- FIT arithmetic through explicit unit conversion (failures per hour);
- the beta-factor model by enumerating the independent and common-cause events;
- upper confidence bounds from the gamma distribution (equivalent to the chi-square form in the lab);
- TPP through MacTOPS, as the rule defines it, and the 3A090 criteria coded from the published text;
- protection-term dates with datetime arithmetic, checked by assert_true.
"""
from __future__ import annotations

import datetime as dt
import math
import sys
from itertools import product
from pathlib import Path

from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import safety  # noqa: E402

v = Verifier.from_files("26-07", ROOT / "chapters" / "26-07-engineering-ethics.md",
                        ROOT / "solutions" / "26-07-solutions.md", LAB / "README.md")


def p_any_binom(p, n):
    return 1 - stats.binom.pmf(0, int(n), p)


def per_hour(fit):
    return fit / 1e9


def p_both_enum(p, beta):
    """Common cause C with probability beta*p; independent faults A, B each with (1 - beta)*p."""
    pc, pi = beta * p, (1 - beta) * p
    total = 0.0
    for c, a, b in product((0, 1), repeat=3):
        pr = (pc if c else 1 - pc) * (pi if a else 1 - pi) * (pi if b else 1 - pi)
        if c or (a and b):
            total += pr
    return total


def upper_gamma(hours, k, conf=0.95):
    return stats.gamma.ppf(conf, k + 1) / hours


def tpp_mactops(tops, bits):
    mactops = tops / 2
    return 2 * mactops * bits


def classify(tpp, density):
    if tpp >= 4800:
        return "a.1"
    if tpp >= 1600 and density >= 5.92:
        return "a.2"
    if 2400 <= tpp < 4800 and 1.6 <= density < 5.92:
        return "b.1"
    if tpp >= 1600 and 3.2 <= density < 5.92:
        return "b.2"
    return None


def mask_work_end(registered, first_sale):
    start = min(registered, first_sale)
    return dt.date(start.year + 10, 12, 31)


# ---------------------------------------------------------------- Example 1
v.check("Ex 26-07.1a", 1e-6 * 5e7)
v.check("Ex 26-07.1b", 1 - math.exp(-50))
v.assert_true("Ex 1 binomial agrees with the lab", abs(p_any_binom(1e-9, 5e7) - safety.p_any(1e-9, 5e7)) < 1e-9)
v.check("Ex 26-07.1c", p_any_binom(1e-9, 5e7))

# ---------------------------------------------------------------- Example 2
h2 = 365 * 12 * 1
v.check("Ex 26-07.2a", h2)
v.check("Ex 26-07.2b", per_hour(10) * 1e7 * h2)
v.check("Ex 26-07.2c", per_hour(100) * 1e7 * h2)
p2 = -math.expm1(-per_hour(10) * h2)
v.check("Ex 26-07.2d", p2)
v.check("Ex 26-07.2d1", 1 / p2)
v.assert_true("Ex 2 lab fleet failures", abs(safety.fleet_failures(10, 1e7, h2) - 438) < 1e-9)

# ---------------------------------------------------------------- Example 3
v.check("Ex 26-07.3a", p_both_enum(1e-3, 0.0))
pb = p_both_enum(1e-3, 0.05)
v.assert_true("Ex 3 enumeration agrees with the lab", abs(pb - safety.p_both_fail(1e-3, 0.05)) < 1e-15)
v.check("Ex 26-07.3b", pb)
v.check("Ex 26-07.3b1", 0.05 * 1e-3)
v.check("Ex 26-07.3b2", (0.95e-3) ** 2)
v.check("Ex 26-07.3c", pb / 1e-6)
v.check("Ex 26-07.3d", 0.05e-3 / 1e-6)

# ---------------------------------------------------------------- Example 4
v.check("Ex 26-07.4a", upper_gamma(3e6, 0) / 1e-9)
t4 = optimize.brentq(lambda T: upper_gamma(T, 0) - 10e-9, 1e6, 1e12)
v.check("Ex 26-07.4b", t4)
v.check("Ex 26-07.4b1", t4 / 8760)
v.check("Ex 26-07.4c", -math.log(0.05))

# ---------------------------------------------------------------- Example 5
chips = {"a": (1000, 8, 800), "b": (250, 16, 600), "c": (200, 8, 800), "d": (50, 8, 100)}
expect = {"a": "a.1", "b": "a.2", "c": None, "d": None}
for name, (tops, bits, area) in chips.items():
    t = tpp_mactops(tops, bits)
    v.assert_true(f"Ex 5 chip {name.upper()} lab TPP", abs(safety.tpp(tops, bits) - t) < 1e-12)
    v.assert_true(f"Ex 5 chip {name.upper()} classification", classify(t, t / area) == expect[name])
v.check("Ex 26-07.5a", tpp_mactops(1000, 8))
v.check("Ex 26-07.5a1", tpp_mactops(1000, 8) / 800)
v.check("Ex 26-07.5b", tpp_mactops(250, 16))
v.check("Ex 26-07.5b1", tpp_mactops(250, 16) / 600)
v.check("Ex 26-07.5c", tpp_mactops(200, 8))
v.check("Ex 26-07.5c1", tpp_mactops(200, 8) / 800)
v.check("Ex 26-07.5d", tpp_mactops(50, 8))

# ---------------------------------------------------------------- Example 6 (dates)
v.assert_true("Ex 6 patent term ends 15 March 2046", safety.add_years(dt.date(2026, 3, 15), 20) == dt.date(2046, 3, 15))
v.assert_true("Ex 6 mask work ends 31 December 2036",
              mask_work_end(dt.date(2026, 9, 1), dt.date(2026, 6, 10)) == dt.date(2036, 12, 31))

# ---------------------------------------------------------------- text
v.check("Txt 26-07.1", 1 / 1e-7)
v.check("Txt 26-07.2", upper_gamma(1e8, 0) / 1e-9)
v.check("Txt 26-07.3", tpp_mactops(300, 16))

# ---------------------------------------------------------------- Problems
v.check("26-07.3a", 2e-7 * 3e7 * 4)
v.check("26-07.3b", p_any_binom(2e-7, 1.2e8))
v.check("26-07.3c", optimize.brentq(lambda p: p * 1.2e8 - 1, 1e-12, 1e-6))
h4 = 2 * 365 * 10
v.check("26-07.4a", h4)
v.check("26-07.4b", per_hour(100) * 2e6 * h4)
p4 = -math.expm1(-per_hour(100) * h4)
v.check("26-07.4c", p4)
v.check("26-07.4c1", 1 / p4)
v.check("26-07.5a", p_both_enum(1e-4, 0))
v.check("26-07.5a1", p_both_enum(1e-4, 0.02))
v.check("26-07.5b", p_both_enum(1e-4, 0.02) / p_both_enum(1e-4, 0))
v.check("26-07.5c", optimize.brentq(lambda b: p_both_enum(1e-4, b) - 1e-7, 0, 0.5))
T6 = 500_000 * 2000
v.check("26-07.6", T6)
v.check("26-07.6a", upper_gamma(T6, 0) / 1e-9)
v.check("26-07.6b", upper_gamma(T6, 2) / 1e-9)
v.assert_true("P6 gamma bound equals the chi-square form", abs(upper_gamma(T6, 2) - safety.rate_upper_bound(T6, 2)) < 1e-15)
t7 = optimize.brentq(lambda T: upper_gamma(T, 0, 0.90) - 100e-9, 1e3, 1e12)
v.check("26-07.7", t7)
v.check("26-07.7a", t7 / 1000)
v.check("26-07.7a1", t7 / 1000 / 8760)
v.check("26-07.7b", t7 / 1000 / 50)
for key, keyd, (tops, bits, area), crit in (("26-07.8a", "26-07.8a1", (400, 16, 800), "a.1"),
                                            ("26-07.8b", "26-07.8b1", (180, 16, 450), "a.2"),
                                            ("26-07.8c", "26-07.8c1", (300, 8, 1500), "b.1")):
    t = tpp_mactops(tops, bits)
    v.assert_true(f"P8 {key} classification {crit}", classify(t, t / area) == crit)
    v.check(key, t)
    v.check(keyd, t / area)
v.check("26-07.8d", optimize.brentq(lambda x: tpp_mactops(x, 8) - 4800, 1, 1e4))
v.check("26-07.8d1", optimize.brentq(lambda x: tpp_mactops(x, 16) - 4800, 1, 1e4))
v.assert_true("P10 patent ends 2 October 2045", safety.add_years(dt.date(2025, 10, 2), 20) == dt.date(2045, 10, 2))
v.assert_true("P10 mask work ends 31 December 2036",
              mask_work_end(dt.date(2026, 1, 20), dt.date(2026, 5, 5)) == dt.date(2036, 12, 31))

# ---------------------------------------------------------------- lab
v.check("Lab 26-07.a", optimize.brentq(lambda n: p_any_binom(1e-6, n) - 0.5, 1e5, 1e7, xtol=1e-3))
beq = optimize.brentq(lambda b: b * 1e-3 - ((1 - b) * 1e-3) ** 2, 1e-6, 0.1)
v.check("Lab 26-07.b", beq)
v.check("Lab 26-07.b1", p_both_enum(1e-3, 0.001) / 1e-6)
v.check("Lab 26-07.c", optimize.brentq(lambda T: upper_gamma(T, 0) - 1e-9, 1e6, 1e13))
bounds = [upper_gamma(1e9, k) / 1e-9 for k in range(4)]
for key, b in zip(("Lab 26-07.d", "Lab 26-07.d1", "Lab 26-07.d2", "Lab 26-07.d3"), bounds):
    v.check(key, b)
steps = [b - a for a, b in zip(bounds, bounds[1:])]
v.check("Lab 26-07.d4", min(steps))
v.check("Lab 26-07.d5", max(steps))

# ---------------------------------------------------------------- Problem 13(c) (17 U.S.C. 908(a): register within two years)
first_sale = dt.date(2026, 3, 1)
deadline = first_sale.replace(year=first_sale.year + 2)
v.assert_true("P13c registration deadline is 1 March 2028", deadline == dt.date(2028, 3, 1))
v.assert_true("P13c if registered in time, protection runs to 31 Dec 2036",
              dt.date(first_sale.year + 10, 12, 31) == dt.date(2036, 12, 31))

sys.exit(v.finish())
