#!/usr/bin/env python3
"""Verify chapter 05-07: compile and run every C block, and recompute every published number in Python.

C blocks are compiled with the course's strict flags and sanitizers (eeverify.run_c_blocks) and their
output compared exactly. Answer-key values are recomputed independently with Python's unbounded
integers (masking to model fixed widths), exact fractions for the Patriot constant, and closed forms
for the quantization statistics.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_c_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-07-bit-manipulation.md"
SOL = C_DIR / "solutions" / "05-07-solutions.md"
LAB = C_DIR / "labs" / "05-07-lab" / "README.md"
v = Verifier.from_files("05-07", CH, SOL, LAB)
run_c_blocks(v, CH, "chapter")
run_c_blocks(v, SOL, "solutions")


def signed(x: int, bits: int) -> int:
    """Interpret the low `bits` bits of x as two's complement, by the definition (negative top weight)."""
    x &= (1 << bits) - 1
    return x - (1 << bits) if x >> (bits - 1) else x


def field_set(reg: int, width: int, pos: int, value: int) -> int:
    mask = ((1 << width) - 1) << pos
    return (reg & ~mask & 0xFFFFFFFF) | ((value << pos) & mask)


def q15_round(x: float) -> int:
    return max(-32768, min(32767, round(x * 32768)))


def q15_mul(a: int, b: int, rounding: bool = True) -> int:
    p = a * b + ((1 << 14) if rounding else 0)
    return min(32767, p >> 15)                       # Python >> on ints is an arithmetic (floor) shift


def chopped_tenth(bits: int) -> Fraction:
    return Fraction(math.floor(Fraction(1, 10) * 2**bits), 2**bits)


def ones_complement_sum(words) -> int:
    s = sum(words)
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return s


# ---------------------------------------------------------------- theory and examples
v.check("T 05-07.a", 2.0**-15)
v.check("T 05-07.b", float(1 - chopped_tenth(23) / Fraction(1, 10)))
v.assert_true("the chopped 0.1 is exactly 0.1 (1 - 2^-20)", chopped_tenth(23) == Fraction(1, 10) * (1 - Fraction(1, 2**20)))
v.check("T 05-07.c", float(3_600_000 * (Fraction(1, 10) - chopped_tenth(23))))
v.check("Ex 05-07.1a", (-100) % 256)
v.check("Ex 05-07.1b", 0xF380 >> 4)
v.check("Ex 05-07.1c", signed(0xF380 >> 4, 12))
v.assert_true("XOR identity agrees with the definition for every 12-bit value",
              all(((x ^ 0x800) - 0x800) == signed(x, 12) for x in range(4096)))
v.check("Ex 05-07.1d", signed(0xF380 >> 4, 12) * 0.0625)
ctrl = field_set(field_set(1, 3, 1, 5), 4, 8, 9)
v.check("Ex 05-07.2a", ctrl)
v.check("Ex 05-07.2b", ctrl & ~1)
v.check("Ex 05-07.2c", (0x80000D35 >> 1) & 0b111)
v.check("Ex 05-07.2d", (0x80000D35 >> 8) & 0xF)
pkt = bytes([0xA5, 0x01, 0xF4, 0xFF, 0x38])
v.check("Ex 05-07.3a", int.from_bytes(pkt[1:3], "big"))
v.check("Ex 05-07.3b", int.from_bytes(pkt[1:3], "little"))
v.check("Ex 05-07.3c", int.from_bytes(pkt[3:5], "big", signed=True))
v.check("Ex 05-07.4a", q15_mul(q15_round(0.5), q15_round(-0.75)))
v.check("Ex 05-07.4b", q15_round(0.7))
v.check("Ex 05-07.4c", q15_mul(q15_round(0.7), q15_round(0.7)))
v.check("Ex 05-07.4d", q15_mul(-32768, -32768))
alpha_q = round(-math.expm1(-0.1) * 32768)
v.check("Ex 05-07.5a", alpha_q)
for key, rounding in (("Ex 05-07.5b", False), ("Ex 05-07.5c", True)):
    y = 0
    while True:                                     # same recurrence, Python integers (floor shift)
        delta = (alpha_q * (10000 - y) + ((1 << 14) if rounding else 0)) >> 15
        if delta == 0:
            break
        y += delta
    v.check(key, 10000 - y)
v.assert_true("the truncating dead band is below 32768/alpha_q", 10000 - y < 32768 / alpha_q)

# ---------------------------------------------------------------- solutions
v.check("05-07.1a", (-1) % 256)
v.check("05-07.1b", signed(0x80, 8))
v.check("05-07.1c", (-12) % 256)
v.check("05-07.2a", 0xA5 & 0x0F)
v.check("05-07.2b", 0xA5 ^ 0xFF)
v.check("05-07.2c", (0xA5 << 2) & 0xFF)
v.check("05-07.2d", 0xA5 >> 3)
v.check("05-07.3a", 2.0**-15)
v.check("05-07.3b", 2.0**-8)
v.check("05-07.3c", float(Fraction(32767, 256)))
v.check("05-07.4a", signed(0x13, 5))
v.check("05-07.5a", (0xFFFF00F0 >> 4) & 0b111)
v.check("05-07.5b", field_set(0xFFFF00F0, 3, 4, 3))
v.check("05-07.6a", int.from_bytes(bytes([0x10, 0x27, 0x00, 0x00]), "little"))
v.check("05-07.7a", q15_round(-0.3))
v.check("05-07.7b", q15_round(-0.3) / 32768 + 0.3)
v.check("05-07.7c", round(3.3 * 256))
v.check("05-07.7d", q15_mul(8192, 16384))
v.check("05-07.8a", 1234 % 256)
v.check("05-07.8b", 1 << (1000 - 1).bit_length())
v.check("05-07.9a", bin(0xF0F0).count("1"))
v.check("05-07.9b", bin(0x5A).count("1") % 2)
v.check("05-07.10a", float(3_600_000 * (Fraction(1, 10) - chopped_tenth(23))))
v.check("05-07.10b", float(3_600_000 * (Fraction(1, 10) - chopped_tenth(24))))
v.check("05-07.10c", next(b for b in range(1, 64) if 3_600_000 * (Fraction(1, 10) - chopped_tenth(b)) < Fraction(1, 1000)))
v.check("05-07.11a", 2.0**-15 / math.sqrt(12))
v.check("05-07.11b", 2.0**-15 / math.sqrt(3))
hdr = [0x4500, 0x0073, 0x0000, 0x4000, 0x4011, 0x0000, 0xC0A8, 0x0001, 0xC0A8, 0x00C7]
csum = ~ones_complement_sum(hdr) & 0xFFFF
v.check("05-07.12a", csum)
v.check("05-07.12b", ones_complement_sum(hdr[:5] + [csum] + hdr[6:]))


def w1c_write(reg, value, w1c=0b110, rw=0x300):
    """Peripheral semantics: 1s clear W1C bits, R/W bits load the value, other bits ignore writes."""
    kept = reg & ~(value & w1c)
    return (kept & ~rw) | (value & rw)


reg0 = 0x107
v.check("05-07.13a", w1c_write(reg0, reg0 | 0b10))
v.check("05-07.13b", w1c_write(reg0, 0b10))
v.check("05-07.13c", w1c_write(reg0, (reg0 & 0x300) | 0b10))

# ---------------------------------------------------------------- lab
pending = 0b11
pending &= ~(pending | 0b01)                         # write back what was read, OR bit 0: each 1 clears
v.check("Lab 05-07.a", pending)
v.check("Lab 05-07.b", 0b11 & ~0b01)
v.check("Lab 05-07.c", q15_mul(22938, 22938, rounding=False))
v.check("Lab 05-07.d", sum(1 for x in range(1, 1 << 16) if x & (x - 1) == 0))
v.check("Lab 05-07.e", sum(bin(x).count("1") for x in range(1 << 16)))
v.check("Lab 05-07.f", max(-32768, min(32767, 30000 + 10000)))

sys.exit(v.finish())
