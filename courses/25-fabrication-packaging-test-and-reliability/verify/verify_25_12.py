#!/usr/bin/env python3
"""Verify every number in chapter 25-12 (post-silicon validation), its problems and lab.

Independent routes (the lab module postsi.py uses closed forms):
- Vmin by bisection on the delay ratio t(V)/t(0.75 V) rather than on Fmax;
- Goel-Okumoto parameters by solving the two-point equations with root-finding;
- Wilson score limits by solving the score-test equation (p_hat - p)^2 = z^2 p(1 - p)/n for p;
- decision trees by enumerating outcome branches with their probabilities.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-12-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-12", ROOT / "chapters" / "25-12-post-silicon-validation.md",
                        ROOT / "solutions" / "25-12-solutions.md", LAB / "README.md")

VTH, ALPHA, V0, F0 = 0.30, 1.3, 0.75, 3.0
Z = stats.norm.ppf(0.975)


def delay(vv):
    return vv / (vv - VTH) ** ALPHA


def f_at(vv):
    return F0 * delay(V0) / delay(vv)


def v_for(f):
    return optimize.bisect(lambda vv: f_at(vv) - f, VTH + 0.01, 1.5, xtol=1e-12)


def go(t1, m1, t2, m2):
    b = optimize.brentq(lambda bb: m2 * (1 - math.exp(-bb * t1)) - m1 * (1 - math.exp(-bb * t2)), 1e-4, 5)
    return m1 / (1 - math.exp(-b * t1)), b


def wilson(k, n):
    ph = k / n
    g = lambda p: (ph - p) ** 2 - Z * Z * p * (1 - p) / n  # noqa: E731
    return optimize.brentq(g, 1e-9, ph), optimize.brentq(g, ph, 1 - 1e-9)


def tree(delay_w, cm=2.0, wm=10.0, p=0.8, cf=25.0, wf=20.0):
    branches_metal = [(p, cm + wm * delay_w), (1 - p, cm + wm * delay_w + cf + wf * delay_w)]
    metal = sum(pr * c for pr, c in branches_metal)
    full = cf + wf * delay_w
    be = optimize.brentq(lambda q: (cm + wm * delay_w + (1 - q) * full) - full, 0, 1)
    return metal, full, be


# ---------------------------------------------------------------- Example 1
v.check("Ex 25-12.1a", 256 * 4096)
v.check("Ex 25-12.1a1", 256 * 4096 / 8 / 1024)
v.check("Ex 25-12.1b", 4096 / 2e9 * 1e6)
v.check("Ex 25-12.1c", 10 / (4096 / 2e9 * 1e6))

# ---------------------------------------------------------------- Example 2
v.check("Ex 25-12.2a", F0 * V0 / (V0 - VTH) ** ALPHA)
v.check("Ex 25-12.2b", f_at(0.70))
v.check("Ex 25-12.2c", f_at(0.80))
vm = v_for(2.5)
v.check("Ex 25-12.2d", vm)
v.check("Ex 25-12.2e", vm + 0.030)
v.check("Ex 25-12.2f", ((vm + 0.030) / 0.75) ** 2)
v.check("Ex 25-12.2f1", 100 * (1 - ((vm + 0.030) / 0.75) ** 2))
v.check("Ex 25-12.2g", f_at(vm + 0.030) - f_at(vm))
v.check("Ex 25-12.2h", 100 * (1 - (vm / (vm + 0.030)) ** 2))

# ---------------------------------------------------------------- Example 3
a3, b3 = go(4, 60, 8, 90)
v.check("Ex 25-12.3a", b3)
v.check("Ex 25-12.3b", a3)
v.check("Ex 25-12.3c", a3 - 90)
v.check("Ex 25-12.3d", optimize.brentq(lambda t: 1 - math.exp(-b3 * t) - 0.95, 0.1, 200))

# ---------------------------------------------------------------- Examples 4-6
m5, f5, be5 = tree(5.0)
v.check("Ex 25-12.4a", m5)
v.check("Ex 25-12.4b", f5)
v.check("Ex 25-12.4c", be5)
n10 = 1 + Z * Z / (2 * 0.10**2)
v.check("Ex 25-12.5a", n10)
v.check("Txt 25-12.a", n10)
lo, hi = wilson(16, 320)
v.check("Ex 25-12.6a", 100 * 16 / 320)
v.check("Ex 25-12.6b", 100 * lo)
v.check("Ex 25-12.6b1", 100 * hi)
v.check("Ex 25-12.6c", 14.4 / 5)

# ---------------------------------------------------------------- Problems
d50 = 50e-6 * 2e9
v.check("25-12.1a", d50)
v.check("25-12.1b", 256 * d50 / 8 / 2**20)
v.check("25-12.2a", v_for(2.0))
v.check("25-12.2b", v_for(3.4))
a3b, b3b = go(3, 40, 6, 70)
v.check("25-12.3a", b3b)
v.check("25-12.3b", a3b)
v.check("25-12.3c", a3b - 70)
v.check("25-12.3d", optimize.brentq(lambda t: 1 - math.exp(-b3b * t) - 0.90, 0.1, 500))
m2, f2, be2 = tree(2.0)
v.check("25-12.4a", m2)
v.check("25-12.4b", f2)
v.check("25-12.4c", be2)
v.check("25-12.5a", 1 + Z * Z / (2 * 0.05**2))
lo46, hi46 = wilson(46, 320)
v.check("25-12.6a", 100 * lo46)
v.check("25-12.6b", 100 * hi46)
v.assert_true("2024 and 2026 intervals do not overlap", lo46 > hi)
v.check("25-12.7a", 100 * 20 / 650)
v.check("25-12.7a1", 100 * 40 / 650)
v.check("25-12.7b", 100 * 20 / 75)
v.check("25-12.7b1", 100 * 40 / 50)
v.check("25-12.8b", math.log(2) / b3)

ent = 256 * 4096 / (256 + 32)
v.check("25-12.9a", ent)
v.check("25-12.9b", ent / 0.05 / 2e9 * 1e6)
v.check("25-12.9c", (ent / 0.05 / 2e9) / (4096 / 2e9))
k_fit = F0 * V0 / (V0 - VTH) ** ALPHA
v_cold = optimize.brentq(lambda vv: k_fit * (vv - 0.33) ** ALPHA / vv - 2.5, 0.34, 1.5)
v.check("25-12.10a", v_cold)
v.check("25-12.10b", 1000 * (v_cold - vm))

# ---------------------------------------------------------------- Lab
v.check("Lab 25-12.a", 256 * d50 / 8 / 2**20)
v.check("Lab 25-12.b", v_for(2.0))
v.check("Lab 25-12.c", be2)
v.check("Lab 25-12.d", 100 * hi)

sys.exit(v.finish())
