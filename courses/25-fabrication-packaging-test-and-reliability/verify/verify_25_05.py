#!/usr/bin/env python3
"""Verify every number in chapter 25-05 (foundries, PDKs and specialty processes), its problems and lab.

Independent routes (the lab module foundry.py uses the series-capacitor formula and a dense linear solve):
- FD-SOI coupling by a charge-balance solve of the four-node capacitor network (front gate, front surface,
  back surface, back gate) with numpy, and by a sparse finite-difference Laplace solve on a different grid;
- corner ratios from the alpha-power law; Monte Carlo for the local-variation fraction;
- market, shuttle and shrink figures by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-05", ROOT / "chapters" / "25-05-foundries-pdks-specialty-processes.md",
                        ROOT / "solutions" / "25-05-solutions.md", LAB / "README.md")


def delay(vv, vt, a=1.3):
    return vv / (vv - vt) ** a


def coupling_network(t_ox, t_si, t_box):
    """Charge balance with the front surface held fixed: unknowns (dV_G, d_phi_back) for dV_BG = 1."""
    c_ox, c_si, c_box = 3.9 / t_ox, 11.7 / t_si, 3.9 / t_box
    # front surface (fixed, 0): C_ox*(dVg - 0) + C_si*(phib - 0) = 0   (no change in surface charge)
    # back surface: C_si*(0 - phib) + C_box*(1 - phib) = 0
    a = np.array([[c_ox, c_si], [0.0, -(c_si + c_box)]])
    b = np.array([0.0, -c_box])
    dvg, _ = np.linalg.solve(a, b)
    return -dvg


def coupling_fd(t_ox, t_si, t_box, h=0.01):
    """Laplace solve on a uniform grid of step h nm; ratio of front-surface sensitivities."""
    edges = [0, t_ox, t_ox + t_si, t_ox + t_si + t_box]
    x = np.arange(0, edges[-1] + h / 2, h)
    n = len(x)
    mids = (x[:-1] + x[1:]) / 2
    eps = np.where(mids < edges[1], 3.9, np.where(mids < edges[2], 11.7, 3.9))
    k = int(round(t_ox / h))
    from scipy.sparse import diags
    from scipy.sparse.linalg import spsolve
    main = np.zeros(n)
    lo = np.zeros(n - 1)
    up = np.zeros(n - 1)
    main[1:-1] = -(eps[:-1] + eps[1:])
    lo[:-1] = eps[:-1]
    up[1:] = eps[1:]
    main[0] = main[-1] = 1.0
    a = diags([lo, main, up], [-1, 0, 1], format="csc")

    def surf(vg, vbg):
        b = np.zeros(n)
        b[0], b[-1] = vg, vbg
        return spsolve(a, b)[k]
    return surf(0, 1) / surf(1, 0)


# ---------------------------------------------------------------- Examples 1-3, text
base = 40.2 / 0.725
v.check("Ex 25-05.1a", base)
v.check("Ex 25-05.1b", 100 * 53.49 / base)
v.check("Ex 25-05.1c", 100 * 40.2 / 53.49)
v.check("Ex 25-05.1d", 100 * 3.26 / base)
v.check("Ex 25-05.2a", 3 + 30 + 33 + 11)
v.check("Ex 25-05.2a1", 8 + 33 + 28 + 10)
v.check("Ex 25-05.2b", 8 / 3)
v.check("Ex 25-05.3a", 4 * 17820)
v.check("Ex 25-05.3b", 10 * 17820)
v.check("Ex 25-05.3c", optimize.brentq(lambda a: a * 17820 - 1.5e6, 1, 1e4))

# ---------------------------------------------------------------- Example 4, text
tt = delay(0.75, 0.30)
ss = delay(0.675, 0.345) / tt
ff = delay(0.825, 0.255) / tt
v.check("Ex 25-05.4a", ss)
v.check("Ex 25-05.4b", ff)
v.check("Ex 25-05.4c", ss / ff)
v.check("Ex 25-05.4d", 1.00 / ss)
v.check("Txt 25-05.a", 100 * (ss - 1))

# ---------------------------------------------------------------- Example 5
v.check("Ex 25-05.5a0", 3.9 / 1.2)
v.check("Ex 25-05.5a1", 11.7 / 7)
v.check("Ex 25-05.5a2", 3.9 / 20)
k20 = coupling_network(1.2, 7, 20)
v.check("Ex 25-05.5a", k20)
v.check("Ex 25-05.5a3", 1000 * k20)
v.check("Ex 25-05.5c0", 1000 * k20)
v.check("Ex 25-05.5b0", 3.9 / 10)
k10 = coupling_network(1.2, 7, 10)
v.check("Ex 25-05.5b", 1000 * k10)
v.check("Ex 25-05.5c1", 1000 * k10)
v.check("Ex 25-05.5c", 10 ** (1000 * k20 / 70))
v.check("Ex 25-05.5c2", 10 ** (1000 * k10 / 70))
v.assert_true("finite-difference Laplace solve matches the network coupling",
              abs(coupling_fd(1.2, 7, 20) / k20 - 1) < 1e-3)

# ---------------------------------------------------------------- Example 6
a6 = 4 / 3 + 2 / 2.5 + 4 / 1.2
v.check("Ex 25-05.6a", a6)
v.check("Ex 25-05.6b", 1.8 * a6 / 10)

# ---------------------------------------------------------------- Problems
v.check("25-05.1a", 5.9 - 5.4)
v.check("25-05.1b", 0.054 * base)
v.check("25-05.2a", 3 + 30 + 33 + 11)
v.check("25-05.2b", 100 - 77)
v.check("25-05.3a", max(2, 6) * 913)
v.check("25-05.3b", max(2, 6) * 913 / 2)
v.check("25-05.4a", 2.5e6 / 17820)
tt2 = delay(0.75, 0.30, 2.0)
s2, f2 = delay(0.675, 0.345, 2.0) / tt2, delay(0.825, 0.255, 2.0) / tt2
v.check("25-05.5a", s2)
v.check("25-05.5b", f2)
v.check("25-05.5c", s2 / f2)
v.check("25-05.6a0", ss)
v.check("25-05.6a", 2.0 * ss)
v.check("25-05.7a", 0.080 / k20)
v.check("25-05.7b", 10 ** (80 / 70))
v.check("25-05.8a", 3.9 / 1.0)
v.check("25-05.8a1", 11.7 / 6)
v.check("25-05.8a2", 3.9 / 25)
k8 = coupling_network(1.0, 6, 25)
v.check("25-05.8b", k8)
v.check("25-05.8b1", 1000 * k8)
v.check("25-05.8c", optimize.brentq(lambda tb: coupling_network(1.0, 6, tb) - 2 * k8, 1, 25))
a9 = 6 / 3 + 1 / 2.5 + 3 / 1.2
v.check("25-05.9a", a9)
v.check("25-05.9b", 1.8 * a9 / 10)
v.check("25-05.9c", 100 * (1 - 1.8 * a9 / 10))
v.check("25-05.10a", 4 * 16200)
v.check("25-05.10b", 4 * 16200 / 40)
v.check("25-05.11a", (80 / 20) ** 2)
v.check("25-05.11b", math.exp(2.5 * math.log(80 / 20)))
v.check("25-05.12a", norm.sf(3))
v.check("25-05.12b", norm.sf(3) * 1e6)
v.check("25-05.13a", 0.30 * 20)
v.check("25-05.13b", 0.30 * 20 / 6)

# ---------------------------------------------------------------- Lab
frac = norm.sf(0.045 / math.hypot(0.015, 0.010))
v.check("Lab 25-05.a", frac)
rng = np.random.default_rng(21)
sim = np.mean(rng.normal(0, 0.015, 400_000) + rng.normal(0, 0.010, 400_000) > 0.045)
v.assert_true("Monte Carlo fraction within 10% of the analytical value", abs(sim / frac - 1) < 0.10)
v.check("Lab 25-05.b", 1000 * coupling_fd(1.2, 5, 20))
v.check("Lab 25-05.c", 3e6 / 17820)
ad = (4 * 2 / 3) / 3 + (4 / 3) / 2.5 + 6 / 1.2
v.check("Lab 25-05.d", ad)
v.check("Lab 25-05.d1", 1.8 * ad / 10)
# break-even analog fraction: the migrated-area cost ratio is linear in x; solve 1.8 * area(x) / 10 = 1 by root-finding
area_x = lambda x: (1 - x) * 10 * (2 / 3) / 3.0 + (1 - x) * 10 * (1 / 3) / 2.5 + x * 10 / 1.2  # noqa: E731
v.check("Lab 25-05.e", optimize.brentq(lambda x: 1.8 * area_x(x) / 10 - 1, 0.01, 0.99))

sys.exit(v.finish())
