#!/usr/bin/env python3
"""Verify every published number in chapter 00-03, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from itertools import accumulate
from pathlib import Path

from sympy import sqrt
from sympy.physics import units as u

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "00-03",
    COURSE / "chapters" / "00-03-how-to-study-this-curriculum.md",
    COURSE / "solutions" / "00-03-solutions.md",
    COURSE / "labs" / "00-03-lab" / "README.md",
)


def same_units(expr, target):
    return u.convert_to(expr, target) == target


# dimensional statements in Example 00-03.1 and Problems 3 and 9
v.assert_true("RC is a time", same_units(u.ohm * u.farad, u.second))
v.assert_true("L/R is a time", same_units(u.henry / u.ohm, u.second))
v.assert_true("1/sqrt(LC) is a frequency", same_units(1 / sqrt(u.henry * u.farad), 1 / u.second))
v.assert_true("V^2/R is a power", same_units(u.volt**2 / u.ohm, u.watt))
v.assert_true("sqrt(L/C) is an impedance", same_units(sqrt(u.henry / u.farad), u.ohm))
v.assert_true("L I^2 is an energy", same_units(u.henry * u.ampere**2, u.joule))
v.assert_true("R/C is NOT a time", not same_units(u.ohm / u.farad, u.second))
v.assert_true("C V is NOT an energy", not same_units(u.farad * u.volt, u.joule))

# Example 2
I = 9 / 46.5
v.check("Ex 00-03.2a", I)
v.check("Ex 00-03.2b", I**2 * 45)
v.check("Ex 00-03.2c", 9 / 45)
v.check("Ex 00-03.2d", 100 * (1 - 45 / 46.5))
# Example 3
P = 2e10 * 0.1 * 3e9 * 0.5e-15
v.check("Ex 00-03.3a", P)
v.check("Ex 00-03.3b", 250 / (2e10 * 3e9 * 0.5e-15))
# Example 4
iv = [2.5**k for k in range(7)]
cum = list(accumulate(iv))
v.check("Ex 00-03.4a", iv[6])
v.check("Ex 00-03.4b", cum[6])
v.assert_true("6 reviews fall within 365 days, the 7th (day 406) passes a year", cum[5] < 365 < cum[6])
v.check("Ex 00-03.4c", 3 * 7 * 8 / 60)
# Example 5
v.check("Ex 00-03.5a", 63 / 20)
v.check("Ex 00-03.5b", 89 / 60)

# Problems
I4 = 12 / 6
v.check("00-03.4a", I4)
v.check("00-03.4b", I4 * 5.5)
v.check("00-03.4c", I4**2 * 5.5)
v.check("00-03.4d", 100 * (I4**2 * 5.5) / (12 * I4))
v.check("00-03.4e", 12 / 5.5)
P5 = 5e10 * 0.01 * 2e9 * 0.3e-15
v.check("00-03.5a", P5)
v.check("00-03.5b", P5 / 5e10 * 1e9)


def reviews_to_cover(ease, horizon=365):
    total, n = 0.0, 0
    while total < horizon:
        total += ease**n
        n += 1
    return n


v.check("00-03.6a", reviews_to_cover(2.0))
v.check("00-03.6b", reviews_to_cover(3.0))
v.check("00-03.7a", 116 / 11)
v.check("00-03.7b", 116 / 8)
v.check("00-03.8a", 61 - 40)
v.check("00-03.8b", 100 * (61 - 40) / 40)
S = 5.0
v.check("00-03.10a", 100 * math.exp(-7 / S))
v.check("00-03.10b", S * math.log(1 / 0.9))
v.check("00-03.10c", 2.5 * S * math.log(1 / 0.9))

# Lab: toy forgetting model. R = exp(-t/S); a review at recall R multiplies S by (1 + 3(1 - R)),
# so reviewing something you still remember perfectly adds little ("desirable difficulty").
def recall_at(day, review_days, s0=1.0, k=3.0):
    S, last = s0, 0.0
    for d in sorted(review_days):
        if d > day:
            break
        R = math.exp(-(d - last) / S)
        S, last = S * (1 + k * (1 - R)), d
    return math.exp(-(day - last) / S), S


cram = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
spaced = [1, 3, 7, 14, 30, 50]
r_c, s_c = recall_at(60, cram)
r_s, s_s = recall_at(60, spaced)
v.check("Lab 00-03.1", 100 * r_c)
v.check("Lab 00-03.2", 100 * r_s)
v.check("Lab 00-03.3", s_c)
v.check("Lab 00-03.4", s_s)

v.finish()
