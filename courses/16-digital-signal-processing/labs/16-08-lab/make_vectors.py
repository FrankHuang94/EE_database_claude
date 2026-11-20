#!/usr/bin/env python3
"""Write the test vectors for biquad_df1_tb.v from the bit-exact model structures.biquad_df1_fixed.

vectors.hex holds, for each of 15 tests, 64 input samples then the 64 expected outputs, as 16-bit two's complement
hex words. Tests: an impulse; steps of +32000 and -32000, which drive the output into positive and negative
saturation through the filter's 5.5% step overshoot; an alternating (Nyquist) input; a 250 Hz sine; and ten seeded
random sequences.
Run from this directory:  python make_vectors.py
"""
from __future__ import annotations

import math

import numpy as np

from structures import biquad_df1_fixed

COEF = (1600, 3199, 1600, -15447, 5461)   # Example 16-07.3 in Q2.14
L = 64
tests = [
    [16384] + [0] * (L - 1),
    [32000] * L,
    [-32000] * L,
    [20000 * (-1) ** n for n in range(L)],
    [round(20000 * math.sin(2 * math.pi * 250 * n / 8000)) for n in range(L)],
]
rng = np.random.default_rng(1608)
for _ in range(10):
    tests.append(list(map(int, rng.integers(-20000, 20001, L))))


def build():
    """The vector file's lines, and the number of saturation events, computed from the bit-exact model."""
    lines, sat = [], 0
    for x in tests:
        y, s = biquad_df1_fixed(x, COEF)
        sat += s
        lines += [f"{v & 0xFFFF:04x}" for v in [*x, *y]]
    return lines, sat


if __name__ == "__main__":
    lines, sat = build()
    with open("vectors.hex", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote vectors.hex: {len(tests)} tests, {sat} saturating outputs")
