#!/usr/bin/env python3
"""Verify the Term 1 checkpoint: recompute every answer and check every numerical multiple-choice letter.

Each key value is recomputed independently (closed forms, numpy/scipy, exact fractions). For numerical
multiple-choice questions, the option text is parsed from README.md and the script checks that the letter
given in solutions.md is the only option matching the computed value to the option's printed precision.
"""
from __future__ import annotations

import cmath
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-1", SOL)

EPS0, MU0, KE, Q, HC = 8.854e-12, 4 * math.pi * 1e-7, 8.988e9, 1.602e-19, 1239.84   # constants as stated in the exam

# ---------------------------------------------------------------- computed answers
ans = {
    1: (2 * 1 - 1**2) * math.exp(-1),
    2: float(np.trapezoid(np.sin(np.linspace(0, math.pi, 200001)) ** 2, np.linspace(0, math.pi, 200001))),
    3: 0.5,
    4: math.exp(0.1) - (1 + 0.1 + 0.1**2 / 2),
    5: 10**2 / (4 * 50),
    6: math.hypot(2 * 1 * 2, 1**2 + 3),
    7: 5 * -math.expm1(-0.02 / (1e4 * 10e-6)),
    8: 4 / (2 * math.sqrt(13)),
    9: 5 / 2,
    10: 3 * -math.expm1(-2),
    11: round(np.linalg.det(np.array([[2, 1, 0], [1, 3, 1], [0, 1, 2]], float))),
    12: np.linalg.solve(np.array([[2.0, 1.0], [1.0, -1.0]]), np.array([5.0, 1.0]))[0],
    13: max(np.linalg.eigvals(np.array([[4.0, 1.0], [2.0, 3.0]])).real),
    14: np.linalg.inv(np.array([[3.0, 1.0], [2.0, 1.0]]))[1, 1],
    15: abs((3 + 4j) * (1 - 2j)),
    16: abs(cmath.rect(10, math.radians(30)) + cmath.rect(10, math.radians(-30))),
    17: (5 * cmath.exp(1j * math.radians(60))).real,
    18: abs(cmath.rect(2, 0) - cmath.rect(2, 2 * math.pi / 3)),
    19: stats.binom.pmf(0, 10, 0.05),
    20: stats.poisson.sf(0, 2),
    21: stats.norm.cdf(1020, 1000, 10) - stats.norm.cdf(980, 1000, 10),
    22: stats.expon.sf(2000, scale=10_000),
    23: float(Fraction(99, 100) * Fraction(1, 100) / (Fraction(99, 100) * Fraction(1, 100) + Fraction(2, 100) * Fraction(99, 100))),
    24: math.sqrt(10**2 + 10**2),
    25: stats.norm.ppf(0.975) * 4 / math.sqrt(25),
    26: math.sqrt(stats.uniform(loc=-0.5, scale=1.0).var()),
    27: float(np.average(np.array([0, 1, 2]) ** 2, weights=[0.5, 0.3, 0.2]) - np.average([0, 1, 2], weights=[0.5, 0.3, 0.2]) ** 2),
    28: 2 * stats.norm.sf(3),
    29: KE * 1e-6 * 1e-6 / 0.1**2,
    30: 4 * EPS0 * 1e-4 / 10e-6 * 1e12,
    31: 0.5 * 10e-6 * 5**2 * 1e6,
    32: 1.72e-8 * 10 / (math.pi * (0.5e-3) ** 2),
    33: float(100 * (1 + Fraction("0.00393") * 50)),
    34: MU0 * 10 / (2 * math.pi * 0.01) * 1e6,
    35: MU0 * 500**2 * 1e-4 / 0.1 * 1e6,
    36: 50 * 0.5e-3 / 1e-3,
    37: HC / 1550,
    39: 1 / (Q * 1e16 * 1350),
    40: math.sqrt(1.72e-8 / (math.pi * 1e6 * MU0)) * 1e6,
    41: (-45) % 256,
    42: int("3FF", 16),
    44: (10**6).bit_length(),
    46: -17 % 5,
    47: (7 // 2) * 2.0,
    48: sum(2 * k for k in range(1, 6)),
    50: 4 + 1,
}
for qn, value in ans.items():
    v.check(f"T1.{qn:02d}", value)

# ---------------------------------------------------------------- multiple-choice letters
readme = README.read_text(encoding="utf-8")
sol = SOL.read_text(encoding="utf-8")
letters = {int(n): l for n, l in re.findall(r"^\*\*(\d+)\. Answer: \(([A-D])\)", sol, re.M)}
options = {}
for block in re.split(r"^\*\*(?=\d+\.\*\*)", readme, flags=re.M)[1:]:
    n = int(block.split(".", 1)[0])
    opt_line = next((l for l in block.splitlines() if l.startswith("(A)")), None)
    if opt_line:
        options[n] = dict(re.findall(r"\(([A-D])\)\s*([^·]+?)\s*(?:·|$)", opt_line))


def option_value(text):
    token = text.split()[0]
    if token.startswith("0x"):
        return float(int(token, 16)), 0.5
    try:
        pub = parse_value(token)
    except Exception:  # noqa: BLE001 - non-numeric option such as "∞" or a name
        return None
    part = pub.parts[0]
    return part.value, part.halfulp


numeric_mc = [1, 3, 4, 6, 8, 9, 12, 15, 16, 19, 21, 23, 25, 27, 29, 31, 34, 36, 40, 41, 47]
for qn in numeric_mc:
    target = ans[qn]
    scored = sorted((abs(parsed[0] - target), letter, parsed[1]) for letter, text in options[qn].items()
                    if (parsed := option_value(text)) is not None)
    (best_err, best, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  best == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best} (error {best_err:.3g}), options {options[qn]}")
v.assert_true("Q13: option (B) lists the eigenvalues 2 and 5", letters[13] == "B" and options[13]["B"] == "2 and 5"
              and sorted(np.round(np.linalg.eigvals(np.array([[4.0, 1.0], [2.0, 3.0]])).real, 9)) == [2.0, 5.0])
v.assert_true("Q38: only Ge's band gap is below the 1550 nm photon energy",
              [name for name, eg in (("Si", 1.12), ("GaAs", 1.42), ("Ge", 0.66), ("GaN", 3.4)) if eg < HC / 1550] == ["Ge"]
              and letters[38] == "C")
v.assert_true("Q43: the nested loop runs n(n-1)/2 times (quadratic)", sum(i for i in range(100)) == 100 * 99 // 2 and letters[43] == "C")
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))

sys.exit(v.finish())
