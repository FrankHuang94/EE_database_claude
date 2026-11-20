#!/usr/bin/env python3
"""Write the test vectors for cordic_tb.v from the bit-exact model hwarch.cordic_fixed.

vectors.hex holds, for each of 64 angles, the 16-bit binary angle (2^15 = pi) and the expected cos and sin in Q2.14,
as 16-bit two's-complement hex words. Angles: the convergence-range edges +-pi/2 and the codes just beyond them (the
quadrant stage's boundary), the axes and -pi, +-30, +-45, 120, 135 and 150 degrees, values next to zero, code 155
(the worst case of an exhaustive sweep), and seeded random angles over the whole circle.
Run from this directory:  python make_vectors.py
"""
from __future__ import annotations

import numpy as np

from hwarch import cordic_fixed

angles = [-16384, 16384, 0, 1, -1, 5461, -5461, 8192, -8192, 16383, -16383, 2, -2, 10923,
          16385, -16385, 21845, -21845, 24576, -24576, 27307, 32767, -32768, 155]
rng = np.random.default_rng(1611)
angles += list(map(int, rng.integers(-32768, 32768, 64 - len(angles))))


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
