#!/usr/bin/env python3
"""Verify every number published in chapter 06-02, its solutions and its lab handout.

Independent routes: resistances by integrating rho/A along the conductor and by counting squares
on a sampled strip; source models solved as linear systems (all node voltages and branch currents
at once) rather than with the text's one-node KCL; diode quantities by root-finding on the
diode law and numerical differentiation; worst cases by brute-force enumeration of every
tolerance corner; the E-series exceptions by direct comparison with the standard table.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-02", C_DIR / "chapters" / "06-02-circuit-elements-and-ohms-law.md",
                        C_DIR / "solutions" / "06-02-solutions.md", C_DIR / "labs" / "06-02-lab" / "README.md")
RHO20, ALPHA = 1.7241e-8, 0.00393
I_S, V_T = 1e-14, 0.025852


def wire_r(rho, length, area):
    """Resistance by integrating rho dx / A along the conductor."""
    return quad(lambda x: rho / area, 0, length)[0]


def diode_v(i):
    return brentq(lambda vd: I_S * math.expm1(vd / V_T) - i, 0.0, 1.5, xtol=1e-15)


def parallel_sources(sources, loads=()):
    """Sources (emf, internal R) and load resistors all across one pair of terminals.
    Returns the terminal voltage and each source's current out of its + terminal (linear solve)."""
    n = len(sources)
    # unknowns: v, i_1..i_n ; equations: v = E_k - R_k i_k ; sum i_k = v * sum(1/R_load)
    A = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)
    for k, (emf, r) in enumerate(sources):
        A[k, 0], A[k, k + 1], b[k] = 1.0, r, emf
    A[n, 0] = -sum(1.0 / r for r in loads)
    A[n, 1:] = 1.0
    x = np.linalg.solve(A, b)
    return x[0], x[1:]


# ---------------------------------------------------------------- theory
v.check("T 06-02.a", wire_r(RHO20, 1.0, 1e-6) * 1e3)
vd1 = diode_v(1e-3)
v.check("T 06-02.b", vd1 / 1e-3)
h = 1e-9
v.check("T 06-02.c", (diode_v(1e-3 + h) - diode_v(1e-3 - h)) / (2 * h))
v.check("T 06-02.d", parallel_sources([(3.90, 0.40)], [1.0])[0])

# ---------------------------------------------------------------- examples
v.check("Ex 06-02.1a", 12 / 4.7e3 * 1e3)
v.check("Ex 06-02.1b", 1 / 4.7e3 * 1e6)
v.check("Ex 06-02.1c", (12 / 4.7e3) ** 2 * 4.7e3 * 1e3)
t_cu = 35e-6
rs = RHO20 / t_cu
v.check("Ex 06-02.2a", rs * 1e3)
squares = sum(1 for _ in np.arange(0, 50e-3, 0.25e-3))                   # count 0.25 mm squares along 50 mm
v.check("Ex 06-02.2b", squares)
r20 = wire_r(RHO20, 50e-3, 0.25e-3 * t_cu)
v.check("Ex 06-02.2c", r20 * 1e3)
r85 = wire_r(RHO20 * (1 + ALPHA * 65), 50e-3, 0.25e-3 * t_cu)
v.check("Ex 06-02.2d", r85 * 1e3)
v.check("Ex 06-02.2e", 2 * r85 * 1e3)
v.check("Ex 06-02.2f", 4 * r85)
rint = np.polyfit([0.0, 3.75 / 10], [3.90, 3.75], 1)[0] * -1              # slope of the terminal line
v.check("Ex 06-02.3a", rint)
v.check("Ex 06-02.3b", 3.90 / rint)
vt10, _ = parallel_sources([(3.90, rint)], [10.0])
v.check("Ex 06-02.3c", vt10 ** 2 / 10)
v.check("Ex 06-02.3d", ((3.90 - vt10) / rint) ** 2 * rint)
v.check("Ex 06-02.3e", 100 * (vt10 ** 2 / 10) / (3.90 * (3.90 - vt10) / rint))
v.check("Ex 06-02.3f", 3.90 - 2 * rint)
v.check("Ex 06-02.4a", (5.0 - 2.1) / 300 * 1e3)
corners = [((vs - 2.1) / r) for vs, r in itertools.product((4.75, 5.0, 5.25), (285.0, 300.0, 315.0))]
v.check("Ex 06-02.4b", max(corners) * 1e3)
v.check("Ex 06-02.4c", min(corners) * 1e3)
pmax = max((vs - 2.1) ** 2 / r for vs, r in itertools.product((4.75, 5.25), (285.0, 315.0)))
v.check("Ex 06-02.4d", pmax * 1e3)
v.check("Ex 06-02.4e", 2 * pmax * 1e3)
vt5, i5 = parallel_sources([(4.20, 0.05), (3.60, 0.05)])
v.check("Ex 06-02.5a", i5[0])
v.check("Ex 06-02.5b", vt5)
v.check("Ex 06-02.5c", 4.20 * i5[0])
v.check("Ex 06-02.5d", -3.60 * i5[1])
v.check("Ex 06-02.5e", sum(ik ** 2 * 0.05 for ik in i5))
v.assert_true("Example 06-02.5 power balance", abs(-4.20 * i5[0] - 3.60 * i5[1] + sum(ik ** 2 * 0.05 for ik in i5)) < 1e-12)
vt5l, i5l = parallel_sources([(4.20, 0.05), (3.60, 0.05)], [1.0])
v.check("Ex 06-02.5f", vt5l)
v.check("Ex 06-02.5g", i5l[0])
v.check("Ex 06-02.5h", i5l[1])

# ---------------------------------------------------------------- solutions
v.check("06-02.1a", 3.3 / 2.2e3 * 1e3)
v.check("06-02.1b", 3.3 ** 2 / 2.2e3 * 1e3)
v.check("06-02.1c", 50e-3 / 10e-3)
v.check("06-02.1d", 50e-3 * 50e-3 / 10e-3)
v.check("06-02.2a", 1 / 2e-3)
v.check("06-02.2b", 8)
v.check("06-02.2c", 4)
v.check("06-02.2d", 8 / 4e-3 / 1e3)
v.check("06-02.4a", 10 ** (1 / 12))
v.check("06-02.4b", 10 ** (1 / 96))
r_cord = wire_r(RHO20, 40.0, 2.08e-6)
v.check("06-02.5a", r_cord)
v.check("06-02.5b", 10 * r_cord)
v.check("06-02.5c", 100 * r_cord)
v.check("06-02.5d", 1e4 * r_cord)
v.check("06-02.6a", brentq(lambda T: 2.000 * (1 + ALPHA * (T - 20)) - 2.400, 0, 200))
slope7, icpt7 = np.polyfit([2.0, 5.0], [11.6, 11.0], 1)
v.check("06-02.7a", -slope7)
v.check("06-02.7b", icpt7)
v.check("06-02.7c", icpt7 / -slope7)
v.check("06-02.7d", icpt7 + slope7 * 8.0)
powers8 = [vs ** 2 / r for vs, r in itertools.product((10.8, 13.2), (950.0, 1050.0))]
v.check("06-02.8a", max(powers8))
v.check("06-02.8b", min(powers8))
v.check("06-02.9a", 10.0 * (1 + 100e-6 * 100))                          # linear TCR model
v.check("06-02.9b", 10.0 * (1 + 25e-6 * 100))
v.check("06-02.9c", 100 * ((1 + 0.01) / (1 - 0.01) - 1))
v.check("06-02.10a", 10e3 / 200 * 1.00)
v.check("06-02.10b", 200 * 50 / 0.95 / 1e3)
v.check("06-02.10c", 200 * 50 / 1.05 / 1e3)
v.check("06-02.11a", 0.1 / 20 * 1e3)
v.check("06-02.11b", 20 ** 2 * 5e-3)
v.check("06-02.11c", 100 * (0.01 + 35e-6 * 60))
v.check("06-02.11d", 20 * 0.5e-3 * 1e3)
v.check("06-02.11e", 20 ** 2 * 0.5e-3)
v.check("06-02.11f", 100 * (0.01 + 350e-6 * 60))
vt12, i12 = parallel_sources([(4.0, 0.06), (4.0, 0.06), (3.7, 0.06)])
v.check("06-02.12a", vt12)
v.check("06-02.12b", i12[0])
v.check("06-02.12c", -i12[2])
v.check("06-02.12d", sum(ik ** 2 * 0.06 for ik in i12))
for key_v, key_s, key_r, cur in (("a", "b", "c", 1e-3), ("d", "e", "f", 10e-3)):
    vd = diode_v(cur)
    v.check(f"06-02.13{key_v}", vd)
    v.check(f"06-02.13{key_s}", vd / cur)
    v.check(f"06-02.13{key_r}", (diode_v(cur * (1 + 1e-6)) - diode_v(cur * (1 - 1e-6))) / (2e-6 * cur))
v.check("06-02.13g", (I_S * math.expm1((vd1 + 1e-3) / V_T) - 1e-3) * 1e6 * 0.5
        + (1e-3 - I_S * math.expm1((vd1 - 1e-3) / V_T)) * 1e6 * 0.5)              # centred difference
v.check("06-02.14a", 0.050 + 0.100 + 0.050)
v.check("06-02.14b", 0.100)
v.check("06-02.15a", 12 / 0.1)
v.check("06-02.15b", 12 ** 2 / 0.1)

# ---------------------------------------------------------------- lab
v.check("Lab 06-02.a", parallel_sources([(4.0, 0.05), (3.9, 0.05)])[1][0])
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
v.check("Lab 06-02.b", sum(1 for k, x in enumerate(E12) if f"{10 ** (k / 12):.1f}" != f"{x:.1f}"))
v.check("Lab 06-02.c", sum(1 for k, x in enumerate(E24) if f"{10 ** (k / 24):.1f}" != f"{x:.1f}"))
v.check("Lab 06-02.d", max(b / a for a, b in zip(E24, E24[1:] + [10.0])))
v.check("Lab 06-02.e", -np.polyfit(np.linspace(0, 5, 501), 3.90 - 0.40 * np.linspace(0, 5, 501), 1)[0])

sys.exit(v.finish())
