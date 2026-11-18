#!/usr/bin/env python3
"""Verify chapter 05-01: run every code block and recompute every published number independently.

Every ```python block in the chapter and the solutions is executed in order, and each one followed
by a ```text block must print exactly that text (eeverify.run_python_blocks). The answer-key values
are then recomputed by different routes: exact rational arithmetic for float questions, NumPy for
complex numbers, closed forms for loops, and SciPy's brentq for roots.
"""
from __future__ import annotations

import math
import statistics
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-01-python-fundamentals.md"
SOL = C_DIR / "solutions" / "05-01-solutions.md"
LAB = C_DIR / "labs" / "05-01-lab" / "README.md"
v = Verifier.from_files("05-01", CH, SOL, LAB)

# ---------------------------------------------------------------- the code in the text runs and prints what is shown
run_python_blocks(v, CH, "chapter")
run_python_blocks(v, SOL, "solutions")


def floor_div(a, b):
    return math.floor(Fraction(a, b))


def floor_mod(a, b):
    return a - b * floor_div(a, b)


# ---------------------------------------------------------------- examples
v.check("Ex 05-01.1a", float(Fraction(33, 10) * Fraction(47, 147)))     # 3.3 V × 4.7k / 14.7k, exactly
v.check("Ex 05-01.1b", 10 * np.log10(2.0))
v.check("Ex 05-01.1c", floor_div(1000, 7))
v.check("Ex 05-01.1d", floor_mod(1000, 7))
v.check("Ex 05-01.1e", floor_div(-7, 2))
v.check("Ex 05-01.1f", floor_mod(-7, 2))
f01, f02, f03 = Fraction(0.1), Fraction(0.2), Fraction(0.3)
sum_rounded = Fraction(float(f01 + f02))                  # IEEE addition = exact sum rounded to nearest float
v.check("Ex 05-01.2a", float(sum_rounded - f03))
v.check("Ex 05-01.2b", float(np.finfo(np.float64).eps))
z = np.complex128(50.0) + 1j * 2 * np.pi * 1e9 * 10e-9
v.check("Ex 05-01.3a", z.imag)
v.check("Ex 05-01.3b", np.abs(z))
v.check("Ex 05-01.3c", np.degrees(np.angle(z)))
v.check("Ex 05-01.4a", statistics.harmonic_mean([100, 220, 330]) / 3)
e12 = "1.0 1.2 1.5 1.8 2.2 2.7 3.3 3.9 4.7 5.6 6.8 8.2".split()
v.check("Ex 05-01.4b", len({int(Fraction(x) * 1000) for x in e12}))     # distinct values in one decade
years = math.ceil(math.log(2) / math.log(1.07))
v.check("Ex 05-01.5a", years)
v.check("Ex 05-01.5b", 1.07 ** years)
v.check("Ex 05-01.5c", brentq(lambda t: 1.07 ** t - 2, 1, 50))
v.check("Ex 05-01.5d", 72 / 7)
errors = {ref: 100 * (meas - nom) / nom for ref, nom, meas in
          [("R1", 1000, 1012.0), ("R2", 1000, 993.0), ("R3", 4700, 4790.0), ("R4", 4700, 4680.0)]}
v.check("Ex 05-01.6a", sum(abs(e) > 1 for e in errors.values()))
v.check("Ex 05-01.6b", errors["R1"])
v.check("Ex 05-01.6c", errors["R3"])
flows = [-1000, 300, 400, 500]
npv = lambda r: sum(c / (1 + r) ** t for t, c in enumerate(flows))  # noqa: E731
v.check("Ex 05-01.7a", 100 * brentq(npv, 0.0, 1.0, xtol=1e-14))
v.check("Ex 05-01.7b", math.ceil(math.log2(1 / 1e-10)))
v.check("Ex 05-01.7c", npv(0.10))

# ---------------------------------------------------------------- solutions
v.check("05-01.1a", float(Fraction(7, 2)))
v.check("05-01.1b", floor_div(7, 2))
v.check("05-01.1c", floor_mod(7, 3))
v.check("05-01.1d", math.prod([2] * 10))
v.check("05-01.1e", 42 + 1)
v.check("05-01.1f", len(list("VDD_core")))
v.check("05-01.2a", floor_div(-17, 5))
v.check("05-01.2b", floor_mod(-17, 5))
v.check("05-01.2c", floor_div(17, -5))
v.check("05-01.2d", floor_mod(17, -5))
times3 = Fraction(float(3 * f01))                         # 0.1 * 3 rounded once
v.check("05-01.3a", float(times3 - f03))
v.assert_true("2.675 is stored below 2.675", Fraction(2.675) < Fraction(2675, 1000))
v.check("05-01.3b", math.floor(float(Fraction(2.675) * 100)) / 100)
v.check("05-01.4a", 20 * np.log10(1000))
v.check("05-01.4b", 10 * np.log10(0.5))
v.check("05-01.4c", 10 * np.log10(1 / 1e-3))
v.check("05-01.4d", 10 * np.log10(1e-6 / 1e-3))
samples = np.arange(0, 100, 7)
v.check("05-01.5a", samples.size)
v.check("05-01.5b", samples[-1])
v.check("05-01.5c", samples[::4].sum())
def ones_after_set(grid):
    grid[0][0] = 1
    return sum(row.count(1) for row in grid)


v.check("05-01.6a", ones_after_set([[0] * 3] * 3))             # one inner list referenced three times
v.check("05-01.6b", ones_after_set([[0] * 3 for _ in range(3)]))


def shared_default(msg, acc=[]):                                # noqa: B006 - the bug being measured
    acc.append(msg)
    return acc


def fresh_default(msg, acc=None):
    acc = [] if acc is None else acc
    acc.append(msg)
    return acc


v.check("05-01.7a", len([shared_default(m) for m in "abc"][-1]))
v.check("05-01.7b", len([fresh_default(m) for m in "abc"][-1]))
vals = [100, 220, 4700, 1000, 47000, 330, 2200, 10000, 68]
decades = [len(str(x)) - 1 for x in vals]                 # integer digit count, avoiding floating log10
v.check("05-01.8a", len(set(decades)))
v.check("05-01.8b", decades.count(3))
v.check("05-01.9a", 1000 * Fraction(106, 100) ** 10)
v.check("05-01.9b", float(1000 * (1 + Fraction(6, 1200)) ** 120))
v.check("05-01.9c", float(1000 * (1 + Fraction(6, 1200)) ** 120 - 1000 * Fraction(106, 100) ** 10))
v.check("05-01.9d", 1000 * math.exp(0.6))
v.check("05-01.10a", 4700 + 220 + 1_000_000 + 68)
v.check("05-01.11a", 2e-3 * math.log(3.3 / 1.8) * 1e3)
v.check("05-01.11b", math.ceil(math.log2(10e-3 / 1e-9)))
temps = [20 + h % 12 for h in range(24)]
v.check("05-01.12a", statistics.mean(temps))
v.check("05-01.12b", max(temps))
v.check("05-01.12c", sum(t > 28 for t in temps))
v.check("05-01.13a", 8 * 2**7)
v.check("05-01.13b", math.comb(8, 4))
rule_err = {p: abs(math.log(2) / math.log1p(p / 100) - 72 / p) for p in range(1, 21)}
v.check("05-01.14a", min(rule_err, key=rule_err.get))
v.check("05-01.14b", brentq(lambda p: math.log(2) / math.log1p(p / 100) - 72 / p, 1, 20, xtol=1e-12))

# ---------------------------------------------------------------- lab
total = 0.0
for _ in range(1_000_000):
    total += 0.1
v.check("Lab 05-01.a", float(Fraction(total) - 100000))
v.check("Lab 05-01.b", math.ulp(1.0))
v.check("Lab 05-01.c", float(f01 - Fraction(1, 10)))
v.check("Lab 05-01.d", 47 * 10**2)
v.check("Lab 05-01.e", 10 * 10**3)

sys.exit(v.finish())
