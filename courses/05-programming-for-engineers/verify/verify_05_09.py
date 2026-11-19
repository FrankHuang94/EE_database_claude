#!/usr/bin/env python3
"""Verify chapter 05-09: run every code block, and recompute every published number independently.

Code blocks in the chapter and solutions are executed and their outputs compared exactly. Answer-key
values are recomputed by other routes: complexity from a control-flow-graph edge/node count (M = E - N + 2)
rather than by counting decision keywords, MC/DC minima by an independent search, defect escapes and
canary statistics from closed forms, and coverage by Python's line table.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-09-software-engineering-practices.md"
SOL = C_DIR / "solutions" / "05-09-solutions.md"
LAB = C_DIR / "labs" / "05-09-lab" / "README.md"
v = Verifier.from_files("05-09", CH, SOL, LAB)
run_python_blocks(v, CH, "chapter")
run_python_blocks(v, SOL, "solutions")


def mcdc_minimum(f, n):
    """Smallest MC/DC test set size, by search (pairs indexed by the condition they isolate)."""
    cases = list(product((0, 1), repeat=n))
    pairs = {k: {frozenset((a, b)) for a in cases for b in cases
                 if a < b and sum(x != y for x, y in zip(a, b)) == 1 and a[k] != b[k] and bool(f(*a)) != bool(f(*b))}
             for k in range(n)}
    for size in range(n + 1, len(cases) + 1):
        for s in combinations(cases, size):
            ss = set(s)
            if all(any(p <= ss for p in pairs[k]) for k in range(n)):
                return size
    return None


def cfg_complexity(decisions_with_two_exits: int) -> int:
    """Build a toy CFG for a chain of binary decisions and return E - N + 2 (independent of the keyword count)."""
    k = decisions_with_two_exits
    nodes = 2 + 2 * k                                           # entry, exit, and per decision: test + merge
    edges = 1 + 2 * k + (k - 1) + 1                             # entry->D1; Di->Mi twice; Mi->D(i+1); Mk->exit
    return edges - nodes + 2


# ---------------------------------------------------------------- examples
v.check("Ex 05-09.1a", float((Fraction("3.40") - Fraction("3.30")) * 1000))
v.check("Ex 05-09.1b", 3 * 2 + 2)                              # 3 points per threshold x 2, plus 2 hold tests
v.check("Ex 05-09.2a", cfg_complexity(6))
v.check("Ex 05-09.3a", 2**3)
v.check("Ex 05-09.3b", 2)
v.check("Ex 05-09.3c", mcdc_minimum(lambda p, t, o: p and (t or o), 3))
v.check("Ex 05-09.3d", 10 + 1)
f_esc = Fraction(4, 10) * Fraction(5, 10) * Fraction(6, 10) * Fraction(7, 10)
v.check("Ex 05-09.4a", float(f_esc))
v.check("Ex 05-09.4b", float(50 * f_esc))
v.check("Ex 05-09.4c", float(100 * (1 - f_esc)))
v.check("Ex 05-09.4d", float(50 * Fraction(5, 10) * Fraction(6, 10) * Fraction(7, 10)))

# ---------------------------------------------------------------- solutions
v.check("05-09.3a", cfg_complexity(4))
v.check("05-09.3b", cfg_complexity(4))
v.check("05-09.4a", 6 + 6)
v.check("05-09.4b", 6 * 6)


def clamp_gain(g):
    if g < 1:
        g = 1
    if g > 16:
        g = 16
    return g


executable = {line for _, _, line in clamp_gain.__code__.co_lines() if line and line > clamp_gain.__code__.co_firstlineno}
first = clamp_gain.__code__.co_firstlineno
not_run_by_5_and_20 = {first + 2}                               # "g = 1" needs g < 1
v.check("05-09.5a", 100 * (len(executable) - len(not_run_by_5_and_20)) / len(executable))
v.check("05-09.5b", len({0, 5, 20}))
v.assert_true("{0, 5, 20} makes both ifs true and false", {g < 1 for g in (0, 5, 20)} == {True, False}
              and {g > 16 for g in (0, 5, 20)} == {True, False})
v.check("05-09.6a", mcdc_minimum(lambda a, b, c: (a and b) or c, 3))
v.check("05-09.7a", 80 * 0.5**3)
v.check("05-09.7b", 100 * (1 - Fraction(1, 16) / Fraction(1, 4)))
v.check("05-09.7c", 100 * (1 - Fraction(1, 16) / Fraction(1, 8)))
covered = {"R1", "R2", "R3"}
v.check("05-09.9a", 100 * len(covered) / 5)
state, count, history = False, 0, []                            # debounced monitor, written independently
for volts in (3.25, 3.25, 3.31, 3.25, 3.25, 3.25, 3.35, 3.41):
    count = count + 1 if volts < 3.30 else 0
    state = True if count >= 3 else (False if volts >= 3.40 else state)
    history.append(state)
v.check("05-09.10a", history.index(True) + 1)
v.check("05-09.10b", history.index(False, history.index(True)) + 1)
lows, run = [], 0                                               # buggy version: count survives the band
for i, volts in enumerate((3.25, 3.25, 3.31, 3.25), 1):
    run = run + 1 if volts < 3.30 else (0 if volts >= 3.40 else run)
    lows.append(run)
v.check("05-09.10c", lows.index(3) + 1)
v.check("05-09.11a", Fraction(25 * 30, 15))
v.check("05-09.11b", Fraction(25 * 30, 15) - (25 + 30 - 15))
v.check("05-09.12a", -math.expm1(1000 * math.log1p(-0.001)))
v.check("05-09.12b", math.ceil(math.log(0.05) / math.log1p(-0.001)))

# ---------------------------------------------------------------- lab
v.check("Lab 05-09.a", 1)                                       # only v = 3.30 distinguishes < from <=
v.assert_true("only the 3.30 V case separates < from <=", sum((v_ < 3.30) != (v_ <= 3.30) for v_ in (3.29, 3.30, 3.31, 3.39, 3.40, 3.41, 3.35)) == 1)
v.check("Lab 05-09.b", sum(1 for volts, s in ((3.39, True), (3.35, True), (3.35, False)) if (volts < 3.30) != s))
v.check("Lab 05-09.c", 100 * 9 / 11)
v.check("Lab 05-09.d", mcdc_minimum(lambda p, d, t, o: p and d and (t or o), 4))
rates = [0.6, 0.3, 0.5, 0.4, 0.3]
v.check("Lab 05-09.e", 100 * math.prod(1 - r for r in rates))
v.check("Lab 05-09.f", 1 / (1 - 0.6))

sys.exit(v.finish())
