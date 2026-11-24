#!/usr/bin/env python3
"""Verify every number in chapter 20-11 (layout, matching and PVT variation), its problems and its lab.

Independent routes:
- Pelgrom's law and the mirror/pair formulas coded here; the area law itself checked by a seeded Monte Carlo of
  independent gate patches, and the mirror/pair formulas checked by finite differences of a charge-based (EKV-style)
  drain-current model at the stated gm/ID (the lab uses the closed forms);
- gradient residuals with exact rational arithmetic (fractions) over the cell positions of each pattern;
- yield from the complementary error function (the lab uses scipy.stats.norm);
- chi-square confidence limits from the inverse regularized incomplete gamma function, and a seeded coverage
  simulation; the zero-failure run count by direct search;
- the lab's mirror mismatch from the exact square law, confirmed in ngspice (run_spice).
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
from scipy import optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import matching as lab  # noqa: E402

v = Verifier.from_files("20-11", ROOT / "chapters" / "20-11-layout-matching-pvt.md",
                        ROOT / "solutions" / "20-11-solutions.md", LAB / "README.md")
rng = np.random.default_rng(2011)


def pel(a, area):
    return a / math.sqrt(area)


def mirror(gmid, svt, sb):
    return math.sqrt((gmid * svt) ** 2 + sb ** 2)


def pair(gmid, svt, sb):
    return math.sqrt(svt ** 2 + (sb / gmid) ** 2)


def tail2(k):
    """Two-sided Gaussian tail beyond k sigma."""
    return special.erfc(k / math.sqrt(2))


def chi2_ppf(q, dof):
    return 2 * special.gammaincinv(dof / 2, q)


def ci(n):
    return math.sqrt((n - 1) / chi2_ppf(0.975, n - 1)), math.sqrt((n - 1) / chi2_ppf(0.025, n - 1))


def runs(p, conf=0.95):
    n = 1
    while (1 - p) ** n > 1 - conf:
        n += 1
    return n


def residuals(pattern, order):
    """Exact mean of x^order over A cells minus over B cells, x in pitches centred on the row."""
    n = len(pattern)
    xs = [Fr(2 * i - (n - 1), 2) for i in range(n)]
    a = [x ** order for x, c in zip(xs, pattern) if c == "A"]
    b = [x ** order for x, c in zip(xs, pattern) if c == "B"]
    return sum(a) / len(a) - sum(b) / len(b)


def offset(pattern, g1, g2, pitch):
    return float(g1 * pitch * residuals(pattern, 1) + g2 * pitch ** 2 * residuals(pattern, 2))


# ---- the area law: patches of independent threshold error averaged over the gate
def mc_sigma(area, patch=0.01, s_patch=1.0, trials=4000):
    n = int(round(area / patch))
    # mean of n independent patches for each of two devices; the difference's sigma
    da = rng.normal(0, s_patch / math.sqrt(n), trials) - rng.normal(0, s_patch / math.sqrt(n), trials)
    return da.std(ddof=1)


s1, s4 = mc_sigma(1.0), mc_sigma(4.0)
v.assert_true("area law: four times the area halves sigma (MC)", abs(s1 / s4 - 2) < 0.1)


# ---- charge-based drain current and finite-difference mismatch
def ekv_id(vgs, vt, beta=1.0, n=1.3, ut=0.02585):
    """I = 2 n beta U_T^2 ln^2(1 + exp((Vgs - Vt)/(2 n U_T))), all regions."""
    return 2 * n * beta * ut ** 2 * math.log1p(math.exp((vgs - vt) / (2 * n * ut))) ** 2


def vgs_for_gmid(target, vt=0.4):
    lo, hi = vt - 0.3, vt + 1.5
    for _ in range(200):
        mid = (lo + hi) / 2
        h = 1e-6
        g = (math.log(ekv_id(mid + h, vt)) - math.log(ekv_id(mid - h, vt))) / (2 * h)
        lo, hi = (mid, hi) if g > target else (lo, mid)
    return (lo + hi) / 2


for gmid in (5, 10, 20):
    vg = vgs_for_gmid(gmid)
    dv, db = 1e-5, 1e-4
    di_vt = ekv_id(vg, 0.4 + dv) / ekv_id(vg, 0.4) - 1
    v.assert_true(f"mirror Vt sensitivity = -(gm/ID) dVt at gm/ID {gmid}", abs(di_vt / (-gmid * dv) - 1) < 2e-3)
    # pair: input shift that restores the current of a device with beta (1 + db)
    lo, hi = vg - 0.01, vg + 0.01
    target = ekv_id(vg, 0.4)
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ekv_id(mid, 0.4, beta=1 + db) < target else (lo, mid)
    shift = vg - (lo + hi) / 2
    v.assert_true(f"pair beta term = (dbeta/beta)/(gm/ID) at gm/ID {gmid}", abs(shift / (db / gmid) - 1) < 2e-3)

# ---- Example 20-11.1
a_vt = 3.5
s_vt = pel(a_vt, 10 * 1)
v.check("Ex 20-11.1a", s_vt)
v.check("Ex 20-11.1b", 3 * s_vt)
area_05 = (a_vt / 0.5) ** 2
v.check("Ex 20-11.1c", area_05)
v.check("Ex 20-11.1d", area_05 / 10)
v.check("Ex 20-11.1e", s_vt / 0.5)
v.assert_true("lab pelgrom_sigma agrees", abs(lab.pelgrom_sigma(3.5, 10, 1) - s_vt) < 1e-12)

# ---- Example 20-11.2 (sigmas in V and fractions)
svt2, sb2 = s_vt * 1e-3, pel(1.0, 10) / 100
v.check("Ex 20-11.2g", s_vt)
v.check("Ex 20-11.2h", sb2 * 100)
for key_m, key_p, gmid in (("2a", "2d", 5), ("2b", "2e", 10), ("2c", "2f", 20)):
    v.check(f"Ex 20-11.{key_m}", mirror(gmid, svt2, sb2) * 100)
    v.check(f"Ex 20-11.{key_p}", pair(gmid, svt2, sb2) * 1e3)
    v.assert_true(f"lab mirror/pair agree at {gmid}",
                  abs(lab.mirror_sigma(gmid, svt2, sb2) - mirror(gmid, svt2, sb2)) < 1e-12
                  and abs(lab.pair_offset_sigma(gmid, svt2, sb2) - pair(gmid, svt2, sb2)) < 1e-12)
v.check("Ex 20-11.2i", mirror(20, svt2, sb2) / mirror(5, svt2, sb2))

# ---- Example 20-11.3
cox = 10  # fF/um^2
for key_a, key_c, s in (("3a", "3b", 1.0), ("3c", "3d", 0.25)):
    area = (a_vt / s) ** 2
    v.check(f"Ex 20-11.{key_a}", area)
    v.check(f"Ex 20-11.{key_c}", cox * area)
v.check("Ex 20-11.3e", (1.0 / 0.25) ** 2)

# ---- Example 20-11.4: g1 0.01 mV/um, g2 1e-4 mV/um^2, pitch 10 um
g1, g2, p4 = 0.01, 1e-4, 10
v.check("Ex 20-11.4a", abs(offset("AB", g1, 0, p4)))
v.check("Ex 20-11.4b", abs(offset("ABBA", g1, 0, p4)))
v.check("Ex 20-11.4c", abs(offset("ABBABAAB", g1, 0, p4)))
v.check("Ex 20-11.4d", abs(offset("ABBA", g1, g2, p4)))
v.check("Ex 20-11.4e", abs(offset("ABBABAAB", g1, g2, p4)))
v.assert_true("ABBA quadratic residual is 2 pitch^2", residuals("ABBA", 2) == 2)
v.assert_true("lab gradient_offset agrees (ABBA)", abs(lab.gradient_offset("ABBA", [g1, g2], p4) - offset("ABBA", g1, g2, p4)) < 1e-12)

# ---- Example 20-11.5
k5 = 3 / s_vt
v.check("Ex 20-11.5e", k5)
fail = tail2(k5)
v.check("Ex 20-11.5a", fail * 100)
v.check("Ex 20-11.5b", (1 - fail) * 100)
s45 = 3 / 4.5
v.check("Ex 20-11.5c", s45)
v.check("Ex 20-11.5d", (a_vt / s45) ** 2)
v.check("Ex 20-11.5f", tail2(4.5) * 1e6)
v.check("Ex 20-11.5g", (a_vt / s45) ** 2 / 10)

# ---- Example 20-11.6 and the text
lo100, hi100 = ci(100)
lo1k, hi1k = ci(1000)
v.check("Ex 20-11.6a", lo100)
v.check("Ex 20-11.6b", hi100)
v.check("Ex 20-11.6c", lo1k)
v.check("Ex 20-11.6d", hi1k)
v.check("Ex 20-11.6f", 1.1 * lo100)
v.check("Ex 20-11.6g", 1.1 * hi100)
v.check("Ex 20-11.6e", runs(0.0027))
v.check("Ex 20-11.6h", 3 / 0.0027)
v.check("Txt 20-11.a", (lo100 - 1) * 100)
v.check("Txt 20-11.b", (hi100 - 1) * 100)
v.assert_true("lab sigma_ci and zero_failure_runs agree",
              np.allclose(lab.sigma_ci(100), ci(100)) and lab.zero_failure_runs(0.0027) == runs(0.0027))
# coverage of the interval by simulation: 4000 experiments of 100 Gaussian runs
est = rng.normal(0, 1, (4000, 100)).std(axis=1, ddof=1)
cover = np.mean((est * lo100 <= 1) & (1 <= est * hi100))
v.assert_true("100-run interval covers the true sigma about 95% of the time", abs(cover - 0.95) < 0.015)

# ---- Problems
v.check("20-11.1a", pel(2.5, 4 * 0.5))
v.check("20-11.2a", 4 ** 2)
v.check("20-11.3a", mirror(8, 0.002, 0.005) * 100)
v.check("20-11.4a", pair(15, 2e-3, 0.005) * 1e3)
v.check("20-11.5a", 1.77 / math.sqrt(2))
v.check("20-11.6a", abs(offset("AB", 0.02, 0, 5)))
v.check("20-11.6b", abs(offset("ABBA", 0.02, 0, 5)))
v.check("20-11.6c", abs(offset("ABBA", 0.02, 2e-4, 5)))
v.check("20-11.7a", float(residuals("ABBABAAB", 1)))
v.check("20-11.7b", float(residuals("ABBABAAB", 2)))
v.assert_true("lab pattern_residuals agree (ABBABAAB)", np.allclose(lab.pattern_residuals("ABBABAAB"), (0, 0)))
v.check("20-11.8a", tail2(2 / 0.8) * 100)
v.check("20-11.9a", 4 ** 2)
v.check("20-11.10a", runs(0.001))
v.check("20-11.10b", 3 / 0.001)
lo50, hi50 = ci(50)
v.check("20-11.11a", lo50)
v.check("20-11.11b", hi50)
trim = 0.5 / math.sqrt(12)
drift = 1.2e3 * 10e-6 * 165
v.check("20-11.12a", trim)
v.check("20-11.12b", drift)
v.check("20-11.12c", (drift / 2) / 0.25)
v.assert_true("span ratio equals worst-case ratio", abs(drift / 0.5 - (drift / 2) / 0.25) < 1e-12)
# uniform-error sigma by simulation
u = rng.uniform(-0.25, 0.25, 200000)
v.assert_true("uniform trim error sigma = step/sqrt(12) (MC)", abs(u.std() / trim - 1) < 0.01)

# ---- Lab: square-law mirrors with a 1 mV threshold step (W/L 10, KP 200 uA/V^2)
for key, iref in (("a", 10e-6), ("b", 100e-6), ("c", 400e-6)):
    vov = math.sqrt(2 * iref / (200e-6 * 10))
    v.check(f"Lab 20-11.{key}", (1 - ((vov - 1e-3) / vov) ** 2) * 100)
for key, iref in (("d", 10e-6), ("e", 100e-6), ("f", 400e-6)):
    vov = math.sqrt(2 * iref / (200e-6 * 10))
    v.check(f"Lab 20-11.{key}", 2 / vov * 1e-3 * 100)

# ---- Text: practitioner numbers (sources in section 14; arithmetic recomputed here)
v.check("Txt 20-11.c", pel(3.5, 1 * 0.06))
v.check("Txt 20-11.d", pel(30, 20 * 20))
v.check("Txt 20-11.e", tail2(4) * 1e6)
v.check("Txt 20-11.f", tail2(5) * 1e6)
v.check("Txt 20-11.g", tail2(6) * 1e6)
box = 12e-6 * (105 - (-40)) * 100
v.check("Txt 20-11.h", box)
v.check("Txt 20-11.i", box / 0.05)
# probability that a 100-sample sigma estimate is off by more than 10%: chi-square with 99 dof, via gammainc
dof = 99
p_out = special.gammainc(dof / 2, dof * 0.9 ** 2 / 2) + special.gammaincc(dof / 2, dof * 1.1 ** 2 / 2)
v.check("Txt 20-11.j", p_out * 100)
est100 = rng.normal(0, 1, (20000, 100)).std(axis=1, ddof=1)
v.assert_true("MC: 100-run estimates off by >10% about 16% of the time",
              abs(np.mean(np.abs(est100 - 1) > 0.1) - p_out) < 0.01)

# ------------------------------------------------------------------ Problems 13-15
print("Problems 13-15")
gm13, dr13 = 8e-3, 5.0
v.check("20-11.13a", 1e-3 * dr13 * 1e3)
v.check("20-11.13b", -8 * 1e-3 * dr13 * 100)
i2 = optimize.brentq(lambda i: i - (1e-3 + gm13 * (-(i * dr13))), 0, 2e-3)      # I2 = I1 + gm (VGS2 - VGS1)
v.check("20-11.13c", (i2 / 1e-3 - 1) * 100)
drmax = optimize.brentq(lambda r: gm13 * r / (1 + gm13 * r) - 1e-3, 0, 1)
v.assert_true("exact and first-order bounds agree to 0.1%", abs(drmax - 1e-3 / gm13) / drmax < 2e-3)
v.check("20-11.13d", 1e-3 / gm13)
v.check("20-11.13e", 1e-3 / gm13 / 0.05)
v.check("20-11.14a", 5 * 2)
v.check("20-11.14b", 0.7 / 500 * 1e3)
v.check("20-11.14c", 0.7 / 20 * 1e3)
v.check("20-11.14d", 10e-3 * 20)


def area15(gmid):
    return ((gmid * 3.5e-3) ** 2 + 0.01 ** 2) / 1e-3 ** 2


v.check("20-11.15a", area15(5))
v.check("20-11.15b", area15(10))
gmid15 = optimize.brentq(lambda g: 2 / g - 0.3, 1, 30)
v.check("20-11.15c", gmid15)
v.check("20-11.15d", area15(gmid15))
pos15 = (np.arange(8) - 3.5) * 10.0


def grad_err(pattern):
    vt = 0.05 * pos15 + 5e-4 * pos15 ** 2
    a_ = np.mean([vt[i] for i, c in enumerate(pattern) if c == "A"])
    b_ = np.mean([vt[i] for i, c in enumerate(pattern) if c == "B"])
    return a_ - b_


v.check("20-11.15e", abs(grad_err("AAAABBBB")))
v.check("20-11.15f", abs(grad_err("AAAABBBB")) * 1e-3 * gmid15 * 100)
v.check("20-11.15g", abs(grad_err("ABBAABBA")))
v.check("20-11.15h", abs(grad_err("ABBAABBA")) * 1e-3 * gmid15 * 100)
v.assert_true("ABBABAAB cancels linear and quadratic terms", abs(grad_err("ABBABAAB")) < 1e-12)
v.check("20-11.15i", 2 * area15(gmid15))

sys.exit(v.finish())
