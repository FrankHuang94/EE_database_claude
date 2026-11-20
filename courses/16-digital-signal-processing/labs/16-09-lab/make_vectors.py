#!/usr/bin/env python3
"""Write the test vectors for cic_decim_tb.v from the bit-true model multirate.cic_decimate_int.

vectors.hex holds, for each of 12 tests, 64 input samples (12-bit) then the 8 expected outputs (24-bit), each as a
32-bit two's-complement hex word. Tests: positive and negative full-scale DC (the integrators wrap around many times,
and the output reaches the full gain R^N = 4096 times the input), an alternating full-scale input at Nyquist, a slow
ramp, and eight seeded random sequences.
Run from this directory:  python make_vectors.py
"""
from __future__ import annotations

import numpy as np

from multirate import cic_decimate_int

N, R, BIN, W = 4, 8, 12, 24
L = 64
tests = [
    [2047] * L,
    [-2048] * L,
    [2047 if n % 2 == 0 else -2048 for n in range(L)],
    [n * 32 - 1024 for n in range(L)],
]
rng = np.random.default_rng(1609)
for _ in range(8):
    tests.append(list(map(int, rng.integers(-2048, 2048, L))))


def integrator_wraps(x):
    """How many times the last integrator's unbounded sum crosses a 24-bit boundary (evidence of wrap-around)."""
    acc = [0] * N
    wraps = 0
    for xn in x:
        v = xn
        for i in range(N):
            acc[i] += v
            v = acc[i]
        wraps = max(wraps, abs(acc[-1]) >> (W - 1))
    return wraps


def build():
    lines = []
    for x in tests:
        y = cic_decimate_int(x, R, N, W)
        lines += [f"{v & 0xFFFFFFFF:08x}" for v in [*x, *y]]
    return lines


if __name__ == "__main__":
    lines = build()
    with open("vectors.hex", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote vectors.hex: {len(tests)} tests; the DC test's last integrator spans {integrator_wraps(tests[0])}"
          " multiples of 2^23 before wrapping")
