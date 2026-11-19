#!/usr/bin/env python3
"""Verify chapter 05-04: run every code block and recompute every published number independently.

Code blocks in the chapter and solutions are executed (including real git and pytest runs) and their
outputs compared exactly. Answer-key values are recomputed by other routes: exact fractions, the
normal tail from math.erfc and its inverse from mpmath instead of scipy, pure-Python re-implementations
of the tests in place of pytest, and a pure-Python bisection in place of git bisect.
"""
from __future__ import annotations

import hashlib
import math
import subprocess
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-04-reproducible-workflows.md"
SOL = C_DIR / "solutions" / "05-04-solutions.md"
LAB = C_DIR / "labs" / "05-04-lab" / "README.md"
v = Verifier.from_files("05-04", CH, SOL, LAB)
run_python_blocks(v, CH, "chapter")
run_python_blocks(v, SOL, "solutions")
mp.mp.dps = 30


def normal_two_sided_tail(k):
    """P(|Z| > k) for a standard normal, from the complementary error function."""
    return math.erfc(k / math.sqrt(2))


def normal_two_sided_limit(p):
    """k with P(|Z| > k) = p, by inverting erfc with mpmath."""
    return float(mp.sqrt(2) * mp.erfinv(1 - mp.mpf(p)))


def half_ulp(published: str) -> float:
    return float(Fraction(1, 2) * Fraction(10) ** Decimal(published).as_tuple().exponent)


def failures(impl, tests):
    """Count the tests (callables taking the implementation) that fail, as pytest would."""
    n = 0
    for t in tests:
        try:
            if not t(impl):
                n += 1
        except Exception:                                   # an unexpected exception is a failure too
            n += 1
    return n


def raises_value_error(call):
    try:
        call()
    except ValueError:
        return True
    except Exception:
        return False
    return False


# ---------------------------------------------------------------- theory
v.check("T 05-04.a", half_ulp("0.6925"))
v.check("T 05-04.b", half_ulp("0.693"))

# ---------------------------------------------------------------- Example 1: kernel order
v.check("Ex 05-04.1a", float(Fraction(1000) * Fraction(1, 10**6) * 1000))      # r = 1000 when tau is first computed
v.check("Ex 05-04.1b", float(Fraction(2000) * Fraction(1, 10**6) * 1000))      # r = 2000 when cell 3 is re-run

# ---------------------------------------------------------------- Example 2: tests re-implemented without pytest
v.check("Ex 05-04.2a", float(Fraction(33, 10) * Fraction(47, 147)))


def buggy(vin, rt, rb):
    return vin * rt / (rt + rb)


def fixed(vin, rt, rb):
    if rt < 0 or rb < 0 or rt + rb == 0:
        raise ValueError
    return vin * rb / (rt + rb)


div_tests = [lambda f: abs(f(5.0, 10e3, 10e3) - 2.5) <= 2.5e-6,
             lambda f: abs(f(3.3, 10e3, 4.7e3) - 1.0551) <= 5e-5]
div_tests += [lambda f, a=a, b=b: 0.0 < f(5.0, a, b) < 5.0 for a, b in ((1.0, 1e6), (1e6, 1.0), (4.7e3, 22e3))]
div_tests += [lambda f: raises_value_error(lambda: f(5.0, -10e3, 10e3))]
v.check("Ex 05-04.2b", failures(buggy, div_tests))
v.check("Ex 05-04.2c", len(div_tests))
v.assert_true("corrected divider passes all six re-implemented tests", failures(fixed, div_tests) == 0)

# ---------------------------------------------------------------- Example 3: KCL near zero
net = (0.1 + 0.2) - 0.3
v.check("Ex 05-04.3a", net)
v.assert_true("the KCL residual is exactly one ulp of 0.3 (2^-54)", net == 2.0**-54 == math.ulp(0.3))
v.assert_true("exact rational KCL residual of the decimal currents is zero",
              Fraction("0.1") + Fraction("0.2") - Fraction("0.3") == 0)
v.check("Ex 05-04.3b", 1e-9 * 0.3)

# ---------------------------------------------------------------- Example 4: hashes and the birthday bound
v1 = b"tau = 1e3 * 1e-6\n"
v.check("Ex 05-04.4a", len(v1))
git_hash = subprocess.run(["git", "hash-object", "--stdin"], input=v1, capture_output=True).stdout.decode().strip()
v.assert_true("git hash-object agrees with the hand-built blob hash and the diff's a62fe87",
              git_hash.startswith("a62fe87") and git_hash == hashlib.sha1(b"blob 17\0" + v1).hexdigest())
v.check("Ex 05-04.4b", float(Fraction(40 * 15, 16)))
v.check("Ex 05-04.4c", float(mp.mpf(10) ** 14 / (2 * mp.mpf(2) ** 160)))
v.assert_true("exact birthday product for 10^7 objects matches n^2/2N to 1e-6",
              abs(float(-mp.expm1(-mp.mpf(10**7) * (10**7 - 1) / (2 * mp.mpf(2) ** 160))) /
                  float(mp.mpf(10) ** 14 / (2 * mp.mpf(2) ** 160)) - 1) < 1e-6)

# ---------------------------------------------------------------- Example 5: testing random code
v.check("Ex 05-04.5a", float(Fraction(1, 2)))
sigma_g = math.sqrt(2) * 0.01 / 4
v.check("Ex 05-04.5b", sigma_g)
v.check("Ex 05-04.5c", sigma_g / math.sqrt(10_000))
rng = np.random.default_rng(99)                                       # a different seed: check the first-order sigma
rt, rb = rng.normal(10e3, 100.0, (2, 400_000))
v.assert_true("Monte Carlo sigma of the ratio agrees with the first-order value to 1%",
              abs(float(np.std(rb / (rt + rb))) / sigma_g - 1) < 0.01)
p4 = normal_two_sided_tail(4)
v.check("Ex 05-04.5d", p4)
v.check("Ex 05-04.5e", 100 * (1 - (1 - p4) ** 1000))

# ---------------------------------------------------------------- solutions
v.check("05-04.1a", 3.3 / 1e3 * 1e3)                                  # B ran after C set v = 3.3
v.check("05-04.1b", 5.0 / 1e3 * 1e3)
v.check("05-04.3a", len(b"R = 4.7e3\n"))
v.check("05-04.4a", max(1e-6 * 2.0e-12, 1e-12))
v.check("05-04.4b", 100 * 1e-12 / 2.0e-12)
v.check("05-04.5a", float(1 / (3 * Fraction(1, 3000))))
v.check("05-04.6a", 10 * math.log10(10))
v.check("05-04.6b", 20 * math.log10(10))
v.check("05-04.7a", float(mp.sqrt(2 * mp.mpf(2) ** 160 * mp.mpf("1e-9"))))
v.check("05-04.7b", float(mp.sqrt(2 * mp.mpf(2) ** 28 * mp.log(2))))
v.check("05-04.7c", float(Fraction(10**10, 2 * 2**28)))
v.assert_true("exact expected pairs C(n,2)/N differs from n^2/2N by < 0.01%",
              abs(Fraction(10**5 * (10**5 - 1), 2 * 2**28) / Fraction(10**10, 2 * 2**28) - 1) < Fraction(1, 10**4))
se8 = math.sqrt(float(Fraction(9, 100) / 2500))
k8 = normal_two_sided_limit(1e-6)
v.check("05-04.8a", se8)
v.check("05-04.8b", k8)
v.check("05-04.8c", k8 * se8)
v.check("05-04.9a", half_ulp("2.20"))
v.check("05-04.9b", half_ulp("6.32e-3"))
gains = [20.0 if step >= 11 else 2.0 for step in range(1, 17)]      # pure-Python bisection over the same history
lo, hi = 0, len(gains) - 1                                            # gains[lo] good, gains[hi] bad
while hi - lo > 1:
    mid = (lo + hi) // 2
    lo, hi = (mid, hi) if gains[mid] == 2.0 else (lo, mid)
v.check("05-04.10a", hi + 1)
v.check("05-04.10b", next(k for k in range(64) if 2**k >= 1000))
p3 = normal_two_sided_tail(3)
v.check("05-04.11a", 1 - (1 - p3) ** 400)
p_test = -math.expm1(math.log(0.99) / 400)
v.check("05-04.11b", p_test)
v.check("05-04.11c", normal_two_sided_limit(p_test))

# ---------------------------------------------------------------- lab: decoder tests re-implemented without pytest
DIGITS = {c: d for d, c in enumerate(["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white"])}


def strict(c):
    if c not in DIGITS:
        raise ValueError(c)
    return DIGITS[c]


versions = {
    "correct": lambda a, b, m: (10 * strict(a) + strict(b)) * 10 ** strict(m),
    "multiplier": lambda a, b, m: (10 * strict(a) + strict(b)) * 10 ** (strict(m) + 1),
    "swapped": lambda a, b, m: (10 * strict(b) + strict(a)) * 10 ** strict(m),
    "unchecked": lambda a, b, m: (10 * DIGITS.get(a, 0) + DIGITS.get(b, 0)) * 10 ** DIGITS.get(m, 0),
}
decoder_tests = [lambda f: f("brown", "black", "red") == 1_000,
                 lambda f: f("yellow", "violet", "orange") == 47_000,
                 lambda f: f("red", "red", "black") == 22,
                 lambda f: raises_value_error(lambda: f("pink", "black", "red"))]
v.check("Lab 05-04.a", float(Fraction(1000) * Fraction(1, 10**6) * 1000))
v.assert_true("correct decoder passes all four tests", failures(versions["correct"], decoder_tests) == 0)
v.check("Lab 05-04.b", failures(versions["multiplier"], decoder_tests))
v.check("Lab 05-04.c", failures(versions["swapped"], decoder_tests))
v.check("Lab 05-04.d", failures(versions["unchecked"], decoder_tests))
v.check("Lab 05-04.e", half_ulp("3.197") * 1e3)
v.assert_true("3.198 kΩ is outside the half-unit window of 10 kΩ ∥ 4.7 kΩ while 3.197 is inside",
              abs(Fraction(470, 147) - Fraction("3.198")) > Fraction(5, 10**4) >= abs(Fraction(470, 147) - Fraction("3.197")))

sys.exit(v.finish())
