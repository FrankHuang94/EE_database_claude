#!/usr/bin/env python3
"""Verify the Course 05 final exam: run every code block in the solutions and recompute every key value.

The solutions' Python and C blocks are executed (C under the course's strict flags and sanitizers) and
their output compared exactly. The answer key is recomputed here by independent routes: exact integer
and fraction arithmetic modeling C's rules, closed forms, and fresh implementations of the searches.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_c_blocks, run_python_blocks  # noqa: E402

SOL = HERE.parent / "exam" / "solutions.md"
v = Verifier.from_files("05-exam", SOL)
run_python_blocks(v, SOL, "exam solutions")
run_c_blocks(v, SOL, "exam solutions")


def c_div(a, b):
    q = Fraction(a, b)
    return math.floor(q) if q >= 0 else math.ceil(q)


def mcdc_min(f, n):
    cases = list(product((0, 1), repeat=n))
    def ok(s):
        return all(any(sum(x != y for x, y in zip(a, b)) == 1 and a[k] != b[k] and bool(f(*a)) != bool(f(*b))
                       for a, b in combinations(s, 2)) for k in range(n))
    return next(size for size in range(1, len(cases) + 1) if any(ok(s) for s in combinations(cases, size)))


# Q1-Q4
v.check("X05.1a", len([1, 2, 3] + [4]))
v.check("X05.1b", math.floor(Fraction(7, 2)))
v.check("X05.1c", math.floor(Fraction(-7, 2)))
v.check("X05.2a", 3 * 4)
v.check("X05.2b", (200 + 100) % 256)
v.check("X05.2c", (100 + 50 + 128) % 256 - 128)
v.check("X05.2d", 2.0**-23)
v.check("X05.3a", next(n for n in range(64) if Fraction(1, 2**n) < Fraction(1, 10**6)))
x1 = Fraction(3, 2)
x2 = x1 - (x1 * x1 - 2) / (2 * x1)
x3 = x2 - (x2 * x2 - 2) / (2 * x2)
v.check("X05.3b", float(x2))
v.check("X05.3c", float(x3))
v.assert_true("x3 agrees with sqrt(2) to 5 decimals", abs(float(x3) - math.sqrt(2)) < 5e-6)
xs, ys = [0, 1, 2, 3], [Fraction(10, 10), Fraction(29, 10), Fraction(51, 10), Fraction(70, 10)]
n = 4
m = (n * sum(a * b for a, b in zip(xs, ys)) - sum(xs) * sum(ys)) / (n * sum(a * a for a in xs) - sum(xs) ** 2)
v.check("X05.3d", float(m))
v.check("X05.3e", float((sum(ys) - m * sum(xs)) / n))
v.check("X05.4a", 0.005)
p3 = math.erfc(3 / math.sqrt(2))
v.check("X05.4b", p3)
v.check("X05.4c", -math.expm1(200 * math.log1p(-p3)))
v.check("X05.4d", math.sqrt(2 * 2**28 * math.log(2)))

# Q5-Q9: C semantics modeled with Python integers
v.check("X05.5a", c_div(-17, 4))
v.check("X05.5b", -17 - 4 * c_div(-17, 4))
v.check("X05.5c", (-2) % 2**32)
v.check("X05.5d", 250 + 10)
v.check("X05.5e", (250 + 10) % 256)
v.check("X05.5f", c_div(700 * 3300, 1024))
v.check("X05.5g", c_div(700 * 3300 + 512, 1024))
a = [10, 20, 30, 40, 50]
p = 1
a[p] += 5
a[p + 2] = a[p - 1] + 1
p += 1
v.check("X05.6a", a[1])
v.check("X05.6b", a[3])
v.check("X05.6c", a[p])
v.check("X05.6d", 5 * 4)
v.check("X05.6e", 4 - p)
import ctypes  # noqa: E402

Rec = type("Rec", (ctypes.Structure,), {"_fields_": [("a", ctypes.c_uint16), ("b", ctypes.c_uint32), ("c", ctypes.c_uint8)]})
Tight = type("Tight", (ctypes.Structure,), {"_fields_": [("b", ctypes.c_uint32), ("a", ctypes.c_uint16), ("c", ctypes.c_uint8)]})
v.check("X05.7a", ctypes.sizeof(Rec))
v.check("X05.7b", Rec.b.offset)
v.check("X05.7c", ctypes.sizeof(Tight))
v.check("X05.7d", 2000 * (ctypes.sizeof(Rec) - ctypes.sizeof(Tight)))
v.check("X05.7e", len("V=%.3fV" % 3.3))
reg = 0x3A5C
v.check("X05.8a", (reg >> 8) & 0xF)
v.check("X05.8b", (reg & ~0xF0) | (3 << 4))
signed12 = 0xE70 - 4096 if 0xE70 & 0x800 else 0xE70
v.check("X05.8c", signed12)
v.check("X05.8d", signed12 * Fraction(1, 16))
v.assert_true("little-endian bytes of 0x11223344 are 44 33 22 11", (0x11223344).to_bytes(4, "little") == bytes([0x44, 0x33, 0x22, 0x11]))
qa, qb = round(Fraction(6, 10) * 32768), round(Fraction(-4, 10) * 32768)
q = (qa * qb + 2**14) // 2**15                                  # floor division models the arithmetic shift
v.check("X05.9a", qa)
v.check("X05.9b", q)
v.check("X05.9c", float(Fraction(q, 32768) + Fraction(24, 100)))
v.check("X05.9d", 2.0**-15 / math.sqrt(12))
v.check("X05.9e", 4 * 20 * math.log10(2))

# Q10-Q12
v.check("X05.10a", (5000).bit_length())
T = {1: 0}
for k in (2, 4, 8, 16, 32, 64):
    T[k] = 2 * T[k // 2] + k
v.check("X05.10b", T[64])
v.check("X05.10c", math.ceil(math.log2(math.factorial(8))))
v.check("X05.10d", (5 - 4294967294) % 2**32)
slots, probes = {}, 0
for key, home in enumerate([3, 5, 3, 4, 7, 7]):
    i = home
    probes += 1
    while i in slots:
        i, probes = (i + 1) % 8, probes + 1
    slots[i] = key
v.check("X05.11a", probes)
v.check("X05.11b", probes / 6)
v.check("X05.11c", 0.5 * (1 + 1 / (1 - 0.75) ** 2))
import heapq  # noqa: E402

h = []
for x in (9, 4, 7, 1):
    heapq.heappush(h, x)
v.assert_true("heapq gives the array [1, 4, 7, 9]", h == [1, 4, 7, 9])
import re  # noqa: E402

exam_text = (HERE.parent / "exam" / "README.md").read_text(encoding="utf-8")
count_bad_src = re.search(r"int count_bad\(.*?\n\}", exam_text, re.S).group(0)
count_bad_src = re.sub(r"/\*.*?\*/", "", count_bad_src, flags=re.S)
tokens = re.findall(r"\bif\b|\bfor\b|\bwhile\b|&&|\|\|", count_bad_src)   # decisions in the C source itself
v.assert_true("count_bad has an else-if counted once as an if", "else if" in count_bad_src)
v.check("X05.12a", len(tokens) + 1)
v.check("X05.12b", mcdc_min(lambda a_, b_, c_, d_: a_ and (b_ or c_) and d_, 4))
v.check("X05.12c", 40 * Fraction(5, 10) * Fraction(6, 10) * Fraction(4, 10))

# Q13-Q15
data = [5, 12, 13, 4, 15, 16, 17, 3, 11, 2, 14, 15]
runs, length = [], 0
for x in data + [-10**9]:                                       # a sentinel closes the final run
    if x > 10:
        length += 1
    else:
        if length:
            runs.append(length)
        length = 0
v.check("X05.13a", sum(1 for r in runs if r >= 2))
v.check("X05.13b", sum(1 for r in runs[:-1] if r >= 2) if data[-1] > 10 else sum(1 for r in runs if r >= 2))
v.check("X05.14a", float(Fraction(1, 1000) * (Fraction(0, 2) + 2 + 3 + 2 + 1 + Fraction(0, 2))) * 1000)
v.check("X05.14b", ((5 - 0.70) / 1000 - 1e-14 * math.expm1(0.70 / 0.025852)) * 1e3)
dfdv = (lambda h: ((5 - (0.70 + h)) / 1000 - 1e-14 * math.expm1((0.70 + h) / 0.025852)
                   - ((5 - (0.70 - h)) / 1000 - 1e-14 * math.expm1((0.70 - h) / 0.025852))) / (2 * h))(1e-7)   # central difference
v.check("X05.14c", dfdv)
v.check("X05.14d", 0.70 - ((5 - 0.70) / 1000 - 1e-14 * math.expm1(0.70 / 0.025852)) / dfdv)
v.check("X05.15a", -math.expm1(500 * math.log1p(-0.002)))

sys.exit(v.finish())
