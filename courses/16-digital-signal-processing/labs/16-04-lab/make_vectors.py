#!/usr/bin/env python3
"""Write the test vectors for fft8_tb.v from fft.py's bit-exact model (fft8_fixed).

vectors.hex holds, for each test, 32 four-digit hex words: xr[0..7], xi[0..7], then the expected Xr[0..7], Xi[0..7],
all as 16-bit two's complement. Tests: an impulse, full-scale DC, the alternating sequence, an on-bin complex tone,
a full-scale alternating input, a full-scale input found by a seeded search that drives a butterfly into
saturation, and 60 seeded random vectors.
Run from this directory:  python make_vectors.py
"""
from __future__ import annotations

import math

import numpy as np

import fft

tests = [
    ([20000] + [0] * 7, [0] * 8),
    ([32767] * 8, [0] * 8),
    ([16384 * (-1) ** n for n in range(8)], [0] * 8),
    ([round(16000 * math.cos(2 * math.pi * n / 8)) for n in range(8)], [round(16000 * math.sin(2 * math.pi * n / 8)) for n in range(8)]),
    ([32767, -32768] * 4, [-32768, 32767] * 4),
]
rng = np.random.default_rng(1604)
# a full-scale vector that drives the saturation of Example 16-04.5: the first, in a seeded search, for which some
# butterfly output saturates
while True:
    xr = list(map(int, rng.choice([-32768, 32767], 8)))
    xi = list(map(int, rng.choice([-32768, 32767], 8)))
    before = fft.SAT_EVENTS[0]
    fft.fft8_fixed(xr, xi)
    if fft.SAT_EVENTS[0] > before:
        tests.append((xr, xi))
        break
for _ in range(60):
    tests.append((list(map(int, rng.integers(-30000, 30001, 8))), list(map(int, rng.integers(-30000, 30001, 8)))))



def build():
    """The vector file's lines, computed from the bit-exact model."""
    lines = []
    for xr, xi in tests:
        Xr, Xi = fft.fft8_fixed(xr, xi)
        lines += [f"{v & 0xFFFF:04x}" for v in [*xr, *xi, *Xr, *Xi]]
    return lines


if __name__ == "__main__":
    with open("vectors.hex", "w") as f:
        f.write("\n".join(build()) + "\n")
    print(f"wrote {len(tests)} vectors")
