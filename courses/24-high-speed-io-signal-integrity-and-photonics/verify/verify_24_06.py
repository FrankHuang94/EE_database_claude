#!/usr/bin/env python3
"""Verify every number in chapter 24-06 (die-to-die links, memory PHYs, scale-up fabrics), its problems and lab.

Independent routes (the lab module d2d.py uses closed forms and its own eigen solution):
- the supply energy of an edge by numerically integrating V * i_supply(t) from an exact ladder solution, checked
  against C V^2;
- ladder rise and delay from an independent eigen-decomposition (assembled here from branch lists) and, as a
  cross-check of the method, an implicit-Euler time march;
- densities from bumps per unit area on a square grid;
- fabric and power figures by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-06", ROOT / "chapters" / "24-06-d2d-memory-phys-scale-up.md",
                        ROOT / "solutions" / "24-06-solutions.md", LAB / "README.md")


def build(ron, rw, cw, cpad, n=40):
    branches = [(i, i + 1, rw / n) for i in range(n)]
    m = n + 1
    g = np.zeros((m, m))
    for a, b, r in branches:
        g[a, a] += 1 / r
        g[b, b] += 1 / r
        g[a, b] -= 1 / r
        g[b, a] -= 1 / r
    g[0, 0] += 1 / ron
    c = np.array([cw / n] * m)
    c[0] += -cw / n / 2 + cpad
    c[-1] += -cw / n / 2 + cpad
    return g, c


def solution(g, c, vs):
    d = np.sqrt(c)
    lam, q = np.linalg.eigh(g / np.outer(d, d))
    y0 = q.T @ (d * vs)
    return (lambda t: vs - (q @ (np.exp(-lam * t) * y0)) / d), lam


def times(ron, v=0.5):
    g, c = build(ron, 50.0, 200e-15, 50e-15)
    x, lam = solution(g, c, np.full(len(c), v))
    f = lambda lvl: optimize.brentq(lambda t: x(t)[-1] - lvl * v, 1e-18, 1e-9, xtol=1e-19)  # noqa: E731
    return f(0.1), f(0.5), f(0.9), x, c


t10, t50, t90, x50, c50 = times(50.0)
# supply energy: integral of V * (V - x0)/Ron
esup, _ = integrate.quad(lambda t: 0.5 * (0.5 - x50(t)[0]) / 50.0, 0, 2e-9, limit=500, epsabs=1e-22)
v.assert_true("integrated supply energy equals C V^2", abs(esup - c50.sum() * 0.25) / (c50.sum() * 0.25) < 1e-6)


def implicit_euler_t50(ron, v=0.5, dt=2e-15, t_end=6e-11):
    g, c = build(ron, 50.0, 200e-15, 50e-15)
    b = np.zeros(len(c))
    b[0] = v / ron
    a = np.diag(c / dt) + g
    xk = np.zeros(len(c))
    t = 0.0
    prev = 0.0
    while t < t_end:
        xn = np.linalg.solve(a, c / dt * xk + b)
        t += dt
        if prev < 0.5 * v <= xn[-1]:
            return t - dt * (xn[-1] - 0.5 * v) / (xn[-1] - prev)
        prev, xk = xn[-1], xn
    return float("nan")


v.assert_true("eigen and implicit-Euler 50% delays agree", abs(implicit_euler_t50(50.0) - t50) < 0.05e-12)

# ================================================================ chapter
v.check("Ex 24-06.1a0", c50.sum() * 1e15)
v.check("Ex 24-06.1a", esup * 1e15)
v.check("Ex 24-06.1b", esup / 4 * 1e15)
v.check("Ex 24-06.1b1", esup / 4 * 1e12)
eh = 20e-15 * 0.4 ** 2 / 4
v.check("Ex 24-06.1c", eh * 1e15)
v.check("Ex 24-06.1c1", eh * 1e12)
pterm = 0.4 ** 2 / (2 * 50) * 0.5  # current V/2R while high, high half the time
v.check("Ex 24-06.1d", pterm / 32e9 * 1e12)
v.check("Ex 24-06.1d1", pterm * 1e3)


n45 = (1000 / 45) ** 2
v.check("Ex 24-06.2a", n45)
v.check("Ex 24-06.2a0", n45 / 2)
v.check("Ex 24-06.2a1", n45 / 2 * 32 / 8)
v.check("Txt 24-06.f", n45 / 2 * 32 / 8)
n9 = (1000 / 9) ** 2
v.check("Ex 24-06.2b", n9)
v.check("Ex 24-06.2b0", n9 / 2)
v.check("Ex 24-06.2b1", n9 / 2 * 4 / 8)
v.check("Ex 24-06.2c", 4000 * 8 / (4 * n9))
v.check("Ex 24-06.2d", n45 / 2 * 32 / 8 * 0.5)

mod32, mod64 = 64 * 32 / 8, 64 * 64 / 8
v.check("Ex 24-06.3a", mod32)
v.check("Ex 24-06.3a1", mod64)
v.check("Ex 24-06.3b0", 10_000 / (2 * mod32))
v.check("Ex 24-06.3b", math.ceil(10_000 / (2 * mod32)))
v.check("Ex 24-06.3c", 10e12 * 8 * 0.25e-12)
v.check("Ex 24-06.3d", 10e12 * 8 * 3e-12)

v.check("Ex 24-06.4a", 16 * 16)
v.check("Ex 24-06.4a1", 16 * 32)
v.check("Ex 24-06.4b0", 1000 / 256)
v.check("Ex 24-06.4b", math.ceil(1000 / 256))

link = 2 * 200 / 8
v.check("Ex 24-06.5a", link)
v.check("Ex 24-06.5a1", 2 * link)
v.check("Ex 24-06.5b", 18 * 2 * link)
v.check("Ex 24-06.5c", 72 * 18 * 2 * link / 1000)
v.check("Txt 24-06.g", 72 * 18 * 2 * link / 1000)
v.check("Ex 24-06.5d", 18 * 2 * link / (2 * 800 / 8))

v.check("Ex 24-06.6a", 3600 / 36)
v.check("Ex 24-06.6a1", 3000 / 36)
v.check("Ex 24-06.6b", 3.6 / 1.8)
v.check("Ex 24-06.6b1", 3.0 / 1.8)
v.check("Ex 24-06.6c", 72 * 3.6)
v.check("Ex 24-06.6c1", 72 * 3.0)

ladder_pj = {"a": 0.05, "b": 0.25, "c": 0.5, "d": 1.3, "e": 3.0}
pw = {k: 1e12 * 8 * e * 1e-12 for k, e in ladder_pj.items()}
for k, p in pw.items():
    v.check(f"Ex 24-06.7{k}", p)
v.check("Ex 24-06.7f", pw["e"] / pw["a"])
v.check("Ex 24-06.7g", pw["e"] - pw["b"])
steps = [0.25 / 0.05, 0.5 / 0.25, 1.3 / 0.5, 3.0 / 1.3]
v.check("Txt 24-06.h", min(steps))
v.check("Txt 24-06.i", max(steps))

hbm = 2048 * 8 / 8
v.check("Ex 24-06.8a", hbm)
v.check("Ex 24-06.8b0", 2048 * 8 / 224)
v.check("Ex 24-06.8b", math.ceil(2048 * 8 / 224))
v.check("Ex 24-06.8c", 2048 * 8e9 * 3e-12)
v.check("Ex 24-06.8d", 2048 * 8e9 * 0.052e-12)
v.check("Ex 24-06.8e", 3 / 0.052)
v.check("Txt 24-06.e", 1.3e-12 * 0.4 ** 2 / 4 * 1e12)

v.check("Txt 24-06.a", (t90 - t10) * 1e12)
v.check("Txt 24-06.b", t50 * 1e12)
elmore = 50 * c50.sum() + 50 * (200e-15 / 2 + 50e-15)
v.check("Txt 24-06.c", elmore * 1e12)
v.check("Txt 24-06.d", 1e12 / 32e9)
t10b, _, t90b, _, _ = times(25.0)
v.check("Txt 24-06.j", (t90b - t10b) * 1e12)

# ================================================================ solutions
e1 = 500e-15 * 0.6 ** 2
v.check("24-06.1a", e1 * 1e15)
v.check("24-06.1b", e1 / 4 * 1e15)
v.check("24-06.1c", e1 / 4 * 16e9 * 1e3)
v.check("24-06.1d", 1024 * e1 / 4 * 16e9)
v.check("24-06.2a", 0.3 ** 2 / (4 * 50 * 16e9) * 1e12)
v.check("24-06.2b", 300e-15 * 0.09 / 4 * 1e15)
v.check("24-06.2b1", 300e-15 * 0.09 / 4 * 1e12)
f_eq = optimize.brentq(lambda f: 0.09 / (4 * 50 * f) - 300e-15 * 0.09 / 4, 1e9, 1e12)
v.check("24-06.2c", f_eq / 1e9)
for p, a0, a in ((25, "3a0", "3a"), (55, "3b0", "3b")):
    n = (1000 / p) ** 2
    v.check(f"24-06.{a0}", n)
    v.check(f"24-06.{a}", n / 2 * 32 / 8)
v.check("24-06.3c", 55 / 25)
v.check("24-06.3c1", (1000 / 25) ** 2 / (1000 / 55) ** 2)
v.check("24-06.4a", 10_000 / 25)
v.assert_true("P4 inside the UCIe-A range", 165 <= 10_000 / 25 <= 1317)
v.check("24-06.4c", 10_000 / 224)
v.check("24-06.5a", 2 * mod64)
v.check("24-06.5b0", 10_000 / (2 * mod64))
v.check("24-06.5b", math.ceil(10_000 / (2 * mod64)))
v.check("24-06.5c", 10e12 * 8 * 0.25e-12)
ct = 50e-15 + 100e-15 + 50e-15
el6 = 100 * ct + 25 * (100e-15 / 2 + 50e-15)
v.check("24-06.6a", ct * 1e15)
v.check("24-06.6b", el6 * 1e12)
v.check("24-06.6c", 2.2 * el6 * 1e12)
v.check("24-06.6d", 1 / (2.2 * el6) / 1e9)
v.check("24-06.7a", 4 * 512)
v.check("24-06.7b", 4 * 512 / 8)
l4 = 2 * 100 / 8
v.check("24-06.8a", l4)
v.check("24-06.8a1", 2 * l4)
v.check("24-06.8b", 18 * 2 * l4)
v.check("24-06.8c", 8 * 18 * 2 * l4 / 1000)
v.check("24-06.9a", 4 * 200 / 8)
v.check("24-06.9b", 1800 / (2 * 4 * 200 / 8))
v.check("24-06.9c", 100 * (212.5 / 200 - 1))
p10 = [2e12 * 8 * 0.25e-12, 1.8e12 * 8 * 1.3e-12, 0.2e12 * 8 * 3e-12]
v.check("24-06.10a", p10[0])
v.check("24-06.10b", p10[1])
v.check("24-06.10c", p10[2])
v.check("24-06.10d", sum(p10))
base = 8 * 2048 * 8 / 8
v.check("24-06.11a", base)
v.check("24-06.11a1", base / 1000)
v.check("24-06.11b", 22e12 * 8 / (8 * 2048) / 1e9)
v.check("24-06.11b1", 19.2e12 * 8 / (8 * 2048) / 1e9)
v.check("24-06.12a", 1e6 * 0.5 * 1 / 8 / 1000)
v.check("24-06.12b", 10e12 * 8 * 0.01e-12)

# ================================================================ lab
v.check("Lab 24-06.a", esup * 1e15)
v.check("Lab 24-06.b", (t90 - t10) * 1e12)
v.check("Lab 24-06.c", t50 * 1e12)
v.check("Lab 24-06.d", elmore * 1e12)
v.check("Lab 24-06.e", (t90b - t10b) * 1e12)
v.check("Lab 24-06.f", (1000 / 25) ** 2 / 2 * 32 / 8)
v.check("Lab 24-06.g", 72 * 18 * 2 * link / 1000)

sys.exit(v.finish())
