#!/usr/bin/env python3
"""Verify chapter 05-02: run every code block and recompute every published number independently.

The chapter's and solutions' code blocks are executed and their printed outputs compared exactly.
Answer-key values are then recomputed by other routes: exact or pure-Python arithmetic instead of
NumPy where possible, closed forms, the statistics module, and explicit bit-level reasoning for
the integer and floating-point questions.
"""
from __future__ import annotations

import math
import random
import statistics
import struct
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-02-numpy-and-vectorization.md"
SOL = C_DIR / "solutions" / "05-02-solutions.md"
LAB = C_DIR / "labs" / "05-02-lab" / "README.md"
v = Verifier.from_files("05-02", CH, SOL, LAB)
run_python_blocks(v, CH, "chapter")
run_python_blocks(v, SOL, "solutions")

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
Q = lambda z: 0.5 * math.erfc(z / math.sqrt(2))                      # noqa: E731


def wrap(value, bits, signed):
    """Two's-complement wrap-around of an integer to `bits` bits."""
    value %= 2**bits
    return value - 2**bits if signed and value >= 2 ** (bits - 1) else value


def to_f32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


# ---------------------------------------------------------------- examples
n1 = 480
v.check("Ex 05-02.1a", n1)
v.check("Ex 05-02.1b", math.sqrt(sum(math.sin(2 * math.pi * k / 48) ** 2 for k in range(n1)) / n1))
pairs = [(a * 1e4, b * 1e4) for a in E12 for b in E12]
vouts = [3.3 * rb / (rt + rb) for rt, rb in pairs]
errs = [abs(x - 1.2) / 1.2 for x in vouts]
best = min(range(len(errs)), key=errs.__getitem__)
v.check("Ex 05-02.2a", sum(e < 0.01 for e in errs))
v.check("Ex 05-02.2b", vouts[best])
v.check("Ex 05-02.2c", 100 * errs[best])
rng = np.random.default_rng(2026)
vref = rng.normal(1.0, 0.02, 10_000)                      # the seeded data must be reproduced exactly
fails = [x < 0.97 or x > 1.03 for x in vref.tolist()]
v.check("Ex 05-02.3a", sum(fails))
v.check("Ex 05-02.3b", sum(fails) / 10_000)
v.check("Ex 05-02.3c", 2 * Q(1.5))
v.check("Ex 05-02.4a", wrap(200 + 100, 8, False))
v.check("Ex 05-02.4b", wrap(250 + 100, 8, False))
v.check("Ex 05-02.4c", to_f32(16_777_217.0))
naive = lambda x: (1 - math.cos(x)) / x**2                              # noqa: E731
v.check("Ex 05-02.6a", naive(1e-6))
v.check("Ex 05-02.6b", naive(1e-8))
v.check("Ex 05-02.6c", 2 * math.sin(0.5e-8) ** 2 / 1e-16)
ref = [0, 10, 20, 30, 40, 50]
reading = [0.52, 10.31, 20.18, 30.47, 40.29, 50.62]
slope, intercept = statistics.linear_regression(ref, reading)
v.check("Ex 05-02.7a", slope)
v.check("Ex 05-02.7b", intercept)
v.check("Ex 05-02.7c", max(abs(y - (slope * x + intercept)) for x, y in zip(ref, reading)))

# ---------------------------------------------------------------- solutions
v.check("05-02.1a", (1 - 0) / (11 - 1))
v.check("05-02.1b", math.ceil((1 - 0) / 0.1))
v.check("05-02.1c", 3 * 4)
v.check("05-02.2a", 4 * 3)
v.check("05-02.3a", wrap(250 + 10, 8, False))
v.check("05-02.3b", wrap(127 + 1, 8, True))
v.check("05-02.4a", 1 / math.sqrt(3))                      # exact RMS of a triangle wave
v.check("05-02.4b", math.sqrt(3))
leak = np.random.default_rng(7).normal(10.0, 2.0, 5_000).tolist()
v.check("05-02.5a", sum(x > 14.0 for x in leak))
v.check("05-02.5b", Q(2.0))
v.check("05-02.5c", 5_000 * Q(2.0))
v.check("05-02.6a", sum([0, 1 * 2, 2 * 2, 3 * 2, 4, 5]))
f32_tenth = to_f32(0.1)
acc = 0.0
for _ in range(1_000_000):
    acc = to_f32(acc + f32_tenth)                          # a float32 running sum, rounded at every step
v.check("05-02.7a", acc)
v.check("05-02.7b", float(np.full(1_000_000, 0.1, dtype=np.float32).sum()))   # NumPy's pairwise result
v.check("05-02.7c", float(Fraction(f32_tenth) * 1_000_000))
v.check("05-02.8a", statistics.mean([1, 2, 4]))
v.check("05-02.8b", 3)
h = [1 / complex(1, r) for r in (1.0, 10.0)]
v.check("05-02.9a", abs(h[0]))
v.check("05-02.9b", abs(h[1]))
v.check("05-02.9c", math.degrees(math.atan2(h[0].imag, h[0].real)))
v.check("05-02.9d", math.degrees(math.atan2(h[1].imag, h[1].real)))
d = [1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]
def plain_sum(xs):
    """Left-to-right float64 accumulation (what NumPy does for short arrays). Python's built-in sum()
    uses compensated summation since 3.12, which would hide the cancellation being demonstrated."""
    acc = 0.0
    for x in xs:
        acc += x
    return acc


v.check("05-02.10a", plain_sum([x * x for x in d]) / 4 - (plain_sum(d) / 4) ** 2)
v.check("05-02.10b", float(statistics.pvariance([Fraction(4), Fraction(7), Fraction(13), Fraction(16)])))
disc = math.sqrt(1e16 - 4)
v.check("05-02.11a", (1e8 - disc) / 2)
v.check("05-02.11b", 1 / ((1e8 + disc) / 2))
v.check("05-02.12a", 2.0)                                  # exact data: ln v is exactly linear
v.assert_true("log-linear fit recovers tau", abs(-1 / statistics.linear_regression(
    list(range(6)), [math.log(5 * math.exp(-t / 2)) for t in range(6)]).slope - 2.0) < 1e-9)
v.check("05-02.12b", 5.0)
e6 = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]
fcs = [1 / (2 * math.pi * a * 1e3 * b * 1e-8) for a in e6 for b in e6]
good = [f for f in fcs if abs(f - 1000) / 1000 < 0.05]
v.check("05-02.13a", len(good))
v.check("05-02.13b", good[0])

# ---------------------------------------------------------------- lab
samples = np.random.default_rng(2026).normal(0.0, 1.0, 1_000_000)
v.check("Lab 05-02.a", math.sqrt(math.fsum(x * x for x in samples.tolist()) / 1_000_000))
taus = [a * 1e3 * b * 1e-7 for a in E12 for b in E12]
v.check("Lab 05-02.b", sum(abs(t - 1e-3) / 1e-3 < 0.02 for t in taus))
v.check("Lab 05-02.c", 2.0**-10)                           # binary16: 10 stored fraction bits
v.check("Lab 05-02.d", (2 - 2**-10) * 2**15)               # largest binary16 value
v.check("Lab 05-02.e", acc)
v.check("Lab 05-02.f", float(np.random.default_rng(42).normal(size=1)[0]))
v.assert_true("Python's random module is independent of NumPy's stream", random.Random(42).random() != 0.304717)

sys.exit(v.finish())
