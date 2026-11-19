#!/usr/bin/env python3
"""Verify chapter 05-05: compile and run every C block, and recompute every published number in Python.

C blocks in the chapter and solutions are compiled with the course's strict flags and sanitizers
(eeverify.run_c_blocks) and their printed output compared exactly. Answer-key values are recomputed
independently: C's truncating division and fixed-width wrap-around are modeled with exact Python
integers and fractions, and the filter and accumulator limits come from closed forms.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_c_blocks, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-05-c-fundamentals.md"
SOL = C_DIR / "solutions" / "05-05-solutions.md"
LAB = C_DIR / "labs" / "05-05-lab" / "README.md"
v = Verifier.from_files("05-05", CH, SOL, LAB)
run_c_blocks(v, CH, "chapter")
run_python_blocks(v, CH, "chapter")
run_c_blocks(v, SOL, "solutions")


def c_div(a: int, b: int) -> int:
    """C99 integer division: the exact quotient truncated toward zero."""
    q = Fraction(a, b)
    return math.floor(q) if q >= 0 else math.ceil(q)


def c_mod(a: int, b: int) -> int:
    return a - b * c_div(a, b)


def wrap(x: int, bits: int, signed: bool) -> int:
    """Reduce x modulo 2^bits, as two's-complement hardware does."""
    x %= 2**bits
    return x - 2**bits if signed and x >= 2**(bits - 1) else x


INT_MAX, UINT32_MAX = 2**31 - 1, 2**32 - 1

# ---------------------------------------------------------------- theory
v.check("T 05-05.a", float(Fraction(4700) * Fraction(100, 10**9) * 1000))
v.check("T 05-05.b", INT_MAX)
v.check("T 05-05.c", UINT32_MAX)
v.check("T 05-05.d", 1 + 2 * 1 + 2)                                   # x * x with x -> 1 + 2, textually

# ---------------------------------------------------------------- examples
k = 1000
v.check("Ex 05-05.1a", c_div(k, 4096) * 3300)
v.check("Ex 05-05.1b", c_div(k * 3300, 4096))
v.check("Ex 05-05.1c", c_div(k * 3300 + 2048, 4096))
v.assert_true("rounded value equals round-half-up of the exact 805.66 mV",
              c_div(k * 3300 + 2048, 4096) == math.floor(Fraction(k * 3300, 4096) + Fraction(1, 2)))
v.check("Ex 05-05.1d", 4095 * 3300 + 2048)
v.check("Ex 05-05.2a", c_div(-7, 2))
v.check("Ex 05-05.2b", c_mod(-7, 2))
v.check("Ex 05-05.2c", math.floor(Fraction(-7, 2)))
v.check("Ex 05-05.2d", -7 - 2 * math.floor(Fraction(-7, 2)))
v.check("Ex 05-05.2e", c_mod(c_mod(0 - 1, 8) + 8, 8))
v.check("Ex 05-05.3a", wrap(-1, 32, signed=False))
alpha = -math.expm1(-0.1)
v.check("Ex 05-05.4a", alpha)
v.check("Ex 05-05.4b", -math.expm1(-1.0))
v.check("Ex 05-05.4c", math.ceil(math.log(0.01) / math.log1p(-alpha)))
sq16 = max(s * s for s in (-(2**15), 2**15 - 1))                    # worst case over the int16 range
v.check("Ex 05-05.5a", INT_MAX // sq16)
v.check("Ex 05-05.5b", (2**63 - 1) // sq16)
v.check("Ex 05-05.5c", (2**63 - 1) // sq16 / 48_000 / 3600)
v.check("Ex 05-05.5d", next(b for b in range(2, 129) if 48_000 * sq16 <= 2 ** (b - 1) - 1))   # smallest signed width that holds the sum
v.assert_true("one worst-case 16-bit square fits in int32 and two do not", sq16 <= INT_MAX < 2 * sq16)

# ---------------------------------------------------------------- solutions
v.check("05-05.2a", c_div(17, 5))
v.check("05-05.2b", c_mod(17, 5))
v.check("05-05.2c", c_div(-17, 5))
v.check("05-05.2d", c_mod(-17, 5))
v.check("05-05.2e", 17 / 5.0)
v.check("05-05.2f", c_div(-37, 10))                                  # truncation of -3.7 toward zero
v.check("05-05.2g", c_div(1, 2) * 4.0)
v.check("05-05.3a", Fraction(2**32, 10**6 * 60))
v.check("05-05.4b", wrap(300, 8, signed=False))
v.check("05-05.4c", 200 + 100)                                       # promoted to int: no wrap
v.check("05-05.5a", float(Fraction(700 * 5000, 1024)))
v.check("05-05.5b", c_div(700 * 5000, 1024))
v.check("05-05.5c", c_div(700 * 5000 + 512, 1024))
v.check("05-05.5d", 1023 * 5000 + 512)
v.check("05-05.6a", min(max(500, 0), 255))
v.check("05-05.7a", 2 + 1 * 2 + 1 * 2 + 1)
v.check("05-05.7b", 10 + c_div(4, 2))
v.check("05-05.7c", (2 + 1) ** 3)
v.check("05-05.8a", float(Fraction(3 + 5 + 10, 3)))
alpha9 = -math.expm1(-0.25)
v.check("05-05.9a", alpha9)
v.check("05-05.9b", math.ceil(math.log(1e-3) / math.log1p(-alpha9)))
sq24 = max(s * s for s in (-(2**23), 2**23 - 1))
v.check("05-05.10a", float(sq24))
v.assert_true("one full-scale 24-bit square exceeds INT32_MAX", sq24 > INT_MAX)
v.check("05-05.10b", (2**63 - 1) // sq24)
v.check("05-05.10c", ((2**63 - 1) // sq24) / 48_000)
v.check("05-05.11a", wrap(704 - 4294967000, 32, signed=False))
v.check("05-05.11b", float(Fraction(2**31, 100) / 86400))
v.check("05-05.12a", c_div(-7 + 2, 2))
v.check("05-05.12b", -7 + c_div(2 - (-7), 2))

# ---------------------------------------------------------------- lab: the adc_test.c checks, re-implemented


def adc_to_mv(code, bits, vref, rounding=True):
    if not 1 <= bits <= 16 or vref <= 0 or not 0 <= code < 2**bits:
        return -1
    return c_div(code * vref + (2**bits // 2 if rounding else 0), 2**bits)


conversion_checks = [((0, 12, 3300), 0), ((2048, 12, 3300), 1650), ((1000, 12, 3300), 806),
                     ((4095, 12, 3300), 3299), ((700, 10, 5000), 3418), ((4096, 12, 3300), -1), ((-1, 12, 3300), -1)]
v.assert_true("all seven conversion checks hold for the rounded formula",
              all(adc_to_mv(*args) == want for args, want in conversion_checks))
v.check("Lab 05-05.a", adc_to_mv(4095, 12, 3300))
v.check("Lab 05-05.b", adc_to_mv(1000, 12, 3300))
v.check("Lab 05-05.c", math.ceil(math.log(0.01) / math.log1p(-alpha)))
v.check("Lab 05-05.d", sum(adc_to_mv(*args, rounding=False) != want for args, want in conversion_checks))
v.check("Lab 05-05.e", wrap(INT_MAX + 1, 32, signed=True))

sys.exit(v.finish())
