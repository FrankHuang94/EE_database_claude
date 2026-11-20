#!/usr/bin/env python3
"""Write the test vectors for cordic_tb.v from the bit-exact model hwarch.cordic_fixed.

vectors.hex holds, for each of 64 angles, the 16-bit binary angle (2^15 = pi) and the expected cos and sin in Q2.14,
as 16-bit two's-complement hex words. Angles: the convergence-range edges +-pi/2, the axes, +-30 and +-45 degrees,
values next to zero, and seeded random angles in [-pi/2, pi/2].
Run from this directory:  python make_vectors.py
"""
from __future__ import annotations

import numpy as np

from hwarch import cordic_fixed

angles = [-16384, 16384, 0, 1, -1, 5461, -5461, 8192, -8192, 16383, -16383, 2, -2, 10923]
rng = np.random.default_rng(1611)
angles += list(map(int, rng.integers(-16384, 16385, 64 - len(angles))))


def build():
    lines = []
    for th in angles:
        x, y, _ = cordic_fixed(th, 14)
        lines += [f"{v & 0xFFFF:04x}" for v in (th, x, y)]
    return lines


if __name__ == "__main__":
    with open("vectors.hex", "w") as f:
        f.write("\n".join(build()) + "\n")
    print(f"wrote vectors.hex: {len(angles)} angles")
