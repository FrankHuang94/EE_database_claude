#!/usr/bin/env python3
"""Verify every number in chapter 25-10 (qualification and functional safety), its problems and lab.

Independent routes (the lab module qual.py uses closed forms and a sampling Monte Carlo):
- Coffin-Manson equivalence and its required exponent by root-finding;
- mission-profile stress hours by numerically integrating the Arrhenius damage rate over the profile
  treated as a step function of time;
- FMEDA metrics from an explicit table of fault classes;
- the dual-point rate in the lab by exact integration over the latent-fault arrival time;
- vehicle and sampling probabilities from scipy's binomial distribution.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-10", ROOT / "chapters" / "25-10-qualification-and-functional-safety.md",
                        ROOT / "solutions" / "25-10-solutions.md", LAB / "README.md")

K = 8.617333262e-5
PROFILE = [(-40, 0.05), (70, 0.65), (110, 0.20), (125, 0.10)]


def rate(ea, t_c):
    return math.exp(-ea / (K * (t_c + 273.15)))


def stress_hours(ea, t_stress, life=20000.0):
    # damage = integral of rate over the profile laid out in time; divide by the stress rate
    edges = [0.0]
    for _, w in PROFILE:
        edges.append(edges[-1] + w * life)
    dmg = 0.0
    for (t_c, _), a, b in zip(PROFILE, edges[:-1], edges[1:]):
        dmg += integrate.quad(lambda _t, tc=t_c: rate(ea, tc), a, b)[0]
    return dmg / rate(ea, t_stress)


def fmeda(rows):
    """rows: (lambda, class) with classes 'S' safe, 'RF' residual, 'MPF_D' detected, 'MPF_L' latent."""
    total = sum(r for r, _ in rows)
    rf = sum(r for r, c in rows if c == "RF")
    lat = sum(r for r, c in rows if c == "MPF_L")
    return total, rf, lat, 1 - rf / total, 1 - lat / (total - rf)


def dual_exact(lam_l, lam_d, t_test, life):
    def f(t):
        found = min(math.ceil(t / t_test) * t_test, life)
        return lam_l * math.exp(-lam_l * t) * (1 - math.exp(-lam_d * (found - t)))
    n = int(math.ceil(life / t_test))
    return sum(integrate.quad(f, i * t_test, min((i + 1) * t_test, life))[0] for i in range(n)) / life


def tc_years(cycles, ds, df, n):
    return cycles * (ds / df) ** n / 365.25


# ---------------------------------------------------------------- Example 1
v.check("Ex 25-10.1a", 150 - (-55))
v.check("Ex 25-10.1b", (205 / 60) ** 2)
v.check("Ex 25-10.1b1", tc_years(1000, 205, 60, 2))
v.check("Ex 25-10.1c", (205 / 60) ** 4)
v.check("Ex 25-10.1c1", tc_years(1000, 205, 60, 4))
v.check("Ex 25-10.1d", tc_years(1500, 205, 60, 2))
v.check("Txt 25-10.b", 1000 * (205 / 60) ** 2)

# ---------------------------------------------------------------- Example 2
h125, h150 = stress_hours(0.7, 125), stress_hours(0.7, 150)
seg = 0.10 * 20000 * rate(0.7, 125) / rate(0.7, 150)
v.check("Ex 25-10.2a", h125)
v.check("Ex 25-10.2b", h150)
v.check("Ex 25-10.2c0", seg)
v.check("Ex 25-10.2c", 100 * seg / h150)
v.check("Ex 25-10.2d", 100 * 1000 / h125)

# ---------------------------------------------------------------- Example 3
v.check("Ex 25-10.3a", 1e-8 * 1e9)
v.check("Ex 25-10.3a1", 1e-7 * 1e9)
v.check("Ex 25-10.3b", 1 - math.exp(-1e-8 * 15000))
v.check("Ex 25-10.3c", 1e6 * (1 - math.exp(-1e-8 * 15000)))

# ---------------------------------------------------------------- Examples 4-5
rows = [(80, "S"), (120 * 0.99, "MPF_D"), (120 * 0.01, "RF"), (20 * 0.9, "MPF_D"), (20 * 0.1, "MPF_L")]
total, rf, lat, spfm, lfm = fmeda(rows)
v.check("Ex 25-10.4a", 200 - 80)
v.check("Ex 25-10.4a1", rf)
v.check("Ex 25-10.4a2", total)
v.check("Ex 25-10.4b", 100 * spfm)
v.check("Ex 25-10.4c", lat)
v.check("Ex 25-10.4c1", 100 * lfm)
rows_nb = [(80, "S"), (118.8, "MPF_D"), (1.2, "RF"), (20, "MPF_L")]
v.check("Ex 25-10.4d", 100 * fmeda(rows_nb)[4])
v.check("Ex 25-10.4e", 100 * fmeda(rows_nb)[4] - 90)
lam_d = 118.8e-9
# dual-point rates from the exact integral (latent arrival, exposure until the next test or end of life)
v.check("Ex 25-10.5a", dual_exact(20e-9, lam_d, 15000, 15000) * 1e9)
v.check("Ex 25-10.5b", dual_exact(2e-9, lam_d, 15000, 15000) * 1e9)
v.check("Ex 25-10.5c", rf + dual_exact(2e-9, lam_d, 15000, 15000) * 1e9)

# ---------------------------------------------------------------- Example 6
v.check("Ex 25-10.6a", 100 * stats.binom.sf(0, 10_000, 1e-6))
v.check("Ex 25-10.6b", stats.binom.sf(0, 10_000, 1e-9))
v.check("Ex 25-10.6c", 1e-5 / 1e4)
v.check("Ex 25-10.6d", 3 / (365.25 * 86400) * 1e6)
v.check("Txt 25-10.a", 100 * (1 - 0.1 ** (1 / 231)))

# ---------------------------------------------------------------- Problems
v.check("25-10.1a", 125 - (-55))
v.check("25-10.1a1", (180 / 60) ** 2)
v.check("25-10.1a2", tc_years(1000, 180, 60, 2))
v.check("25-10.1b", tc_years(2000, 205, 60, 2))
v.check("25-10.2a", 15 * 365.25)
v.check("25-10.2b", optimize.brentq(lambda n: 1000 * (205 / 60) ** n - 15 * 365.25, 0.1, 10))
h05 = stress_hours(0.5, 150)
v.check("25-10.3a", h05)
v.check("25-10.3b", 100 * 1000 / h05)


def spfm_dc(dc):
    return fmeda([(80, "S"), (120 * dc, "MPF_D"), (120 * (1 - dc), "RF"), (20, "MPF_D")])[3]


v.check("25-10.4a", 100 * optimize.brentq(lambda d: spfm_dc(d) - 0.99, 0.5, 1))
v.check("25-10.4b", 100 * optimize.brentq(lambda d: spfm_dc(d) - 0.97, 0.5, 1))
v.check("25-10.5a", 100 * fmeda([(80, "S"), (118.8, "MPF_D"), (1.2, "RF"), (30, "MPF_L")])[4])
v.check("25-10.5b", 100 * optimize.brentq(
    lambda x: fmeda([(80, "S"), (118.8, "MPF_D"), (1.2, "RF"), (30 * x, "MPF_D"), (30 * (1 - x), "MPF_L")])[4] - 0.90,
    0, 1))
v.check("25-10.6a", dual_exact(20e-9, lam_d, 1000, 15000) * 1e9)
v.check("25-10.6b", 7500 / 500)
v.check("25-10.7a", 0.10 * 10)
v.assert_true("1.20 FIT exceeds the 1.0 FIT allocation", rf + 2e-9 * lam_d * 7500 * 1e9 > 1.0)
v.check("25-10.8a", 100 * stats.binom.sf(0, 20_000, 1e-7))
v.check("25-10.9a", 100e-9 * 1e4)
n100 = math.log(0.1) / math.log(1 - 1e-4)
v.assert_true("binomial: zero failures in n units has probability 0.10 at 100 ppm",
              abs(stats.binom.pmf(0, round(n100), 1e-4) - 0.1) < 1e-3)
v.check("25-10.10a", n100)
v.check("25-10.10b", n100 / 231)
v.check("25-10.11a", 4 * 1000)
v.check("25-10.11b", 0.001 * 4 * 1000)
v.check("25-10.11c", 4 * 1000 / 10)

# ---------------------------------------------------------------- Lab
v.check("Lab 25-10.a", 100 * optimize.brentq(lambda d: spfm_dc(d) - 0.99, 0.5, 1))
v.check("Lab 25-10.b", h05)
v.check("Lab 25-10.c", dual_exact(2e-6, 2e-5, 1000, 15000) / (2e-6 * 2e-5 * 500))
v.check("Lab 25-10.d", 100 * stats.binom.sf(0, 20_000, 1e-7))

# per-segment acceleration factors and stress hours (Example 2 and Problem 3)
def af_to(ea, tc, ts):
    return rate(ea, ts) / rate(ea, tc)


for key, ea, tc, ts, val in (("s1", 0.7, -40, 125, "af"), ("s2", 0.7, 70, 125, "af"), ("s3", 0.7, 70, 125, "h"), ("s4", 0.7, 110, 125, "af"),
                             ("s5", 0.7, 110, 125, "h"), ("s6", 0.7, 125, 125, "h"), ("s7", 0.7, -40, 150, "af"), ("s8", 0.7, 70, 150, "af"),
                             ("s9", 0.7, 70, 150, "h"), ("s10", 0.7, 110, 150, "af"), ("s11", 0.7, 110, 150, "h"), ("s12", 0.7, 125, 150, "af")):
    w = dict(PROFILE)[tc]
    v.check(f"Ex 25-10.2{key}", af_to(ea, tc, ts) if val == "af" else w * 20000 / af_to(ea, tc, ts))
for i, tc in enumerate((-40, 70, 110, 125), start=1):
    v.check(f"25-10.3s{i}", af_to(0.5, tc, 150))
    v.check(f"25-10.3s{i + 4}", dict(PROFILE)[tc] * 20000 / af_to(0.5, tc, 150))
v.check("25-10.13b", 20e-9 * lam_d * 720 / 2 * 1e9)
v.assert_true("Problem 13: the exact integral over whole test intervals agrees with lambda_L lambda_DD T/2 within 0.5%",
              abs(dual_exact(20e-9, lam_d, 720, 720 * 20) / (20e-9 * lam_d * 360) - 1) < 5e-3)
v.check("25-10.13c", 7500 / 360)

sys.exit(v.finish())
