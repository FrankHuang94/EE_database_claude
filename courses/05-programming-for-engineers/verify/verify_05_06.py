#!/usr/bin/env python3
"""Verify chapter 05-06: compile and run every C block, and recompute every published number in Python.

C blocks are compiled with the course's strict flags and sanitizers (eeverify.run_c_blocks); blocks that
demonstrate a bug must be caught by the sanitizer or warned about by the compiler. Answer-key values are
recomputed independently: sizes and struct layouts from Python's ctypes and struct modules (which apply
the platform's C ABI rules without our C code), strings from Python formatting, and growth policies,
statistics and budgets from straightforward simulations and exact arithmetic.
"""
from __future__ import annotations

import ctypes
import struct
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_c_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-06-c-pointers-and-memory.md"
SOL = C_DIR / "solutions" / "05-06-solutions.md"
LAB = C_DIR / "labs" / "05-06-lab" / "README.md"
v = Verifier.from_files("05-06", CH, SOL, LAB)
run_c_blocks(v, CH, "chapter")
run_c_blocks(v, SOL, "solutions")

POINTER = struct.calcsize("P")
v.assert_true("this verification runs on a 64-bit platform (8-byte pointers), as the key assumes", POINTER == 8)


def layout(fields):
    """sizeof and field offsets of a C struct, computed by ctypes with native alignment."""
    cls = type("S", (ctypes.Structure,), {"_fields_": fields})
    return ctypes.sizeof(cls), {name: getattr(cls, name).offset for name, _ in fields}


def grow(start, factor_num, factor_den, target, step=None):
    """Simulate a growable buffer; return (reallocations, worst-case copies, final capacity)."""
    cap, reallocs, copies = start, 0, 0
    while cap < target:
        copies += cap
        cap = cap + step if step else cap * factor_num // factor_den
        reallocs += 1
    return reallocs, copies, cap


# ---------------------------------------------------------------- theory and examples
v.check("T 05-06.a", POINTER)
v.check("T 05-06.b", len(b"ADC") + 1)
samples = [2040, 2052, 2047, 2061, 2035, 2049]
v.check("Ex 05-06.1a", min(samples))
v.check("Ex 05-06.1b", max(samples))
v.check("Ex 05-06.1c", sum(samples) // len(samples))
v.check("Ex 05-06.2a", struct.calcsize("=8i"))
v.check("Ex 05-06.2b", POINTER)
v.check("Ex 05-06.2c", 3 * struct.calcsize("=i"))
status = "T=%.1fC RH=%d%%" % (23.5, 41)
v.check("Ex 05-06.3a", len(status))
v.check("Ex 05-06.3b", len(status) + 1)
v.check("Ex 05-06.3c", 10 - 1)
loose, loose_off = layout([("id", ctypes.c_uint8), ("value", ctypes.c_uint32), ("flags", ctypes.c_uint16)])
tight, _ = layout([("value", ctypes.c_uint32), ("flags", ctypes.c_uint16), ("id", ctypes.c_uint8)])
v.check("Ex 05-06.4a", loose)
v.check("Ex 05-06.4b", tight)
v.assert_true("loose layout offsets are 0, 4, 8", list(loose_off.values()) == [0, 4, 8])
v.check("Ex 05-06.4c", 1000 * (loose - tight))
r, c, cap = grow(4, 2, 1, 1000)
v.check("Ex 05-06.5a", r)
v.check("Ex 05-06.5b", c)
v.assert_true("doubling from 4 ends at capacity 1024", cap == 1024)
v.check("Ex 05-06.5c", grow(4, 1, 1, 1000, step=4)[1])

# ---------------------------------------------------------------- solutions
a, b = 5, 7                                                     # 05-06.1, traced with names for the pointers
a = b + 1                                                       # *p = *q + 1 with p -> a, q -> b
b = 0                                                           # p = q; *p = 0
v.check("05-06.1a", a)
v.check("05-06.1b", b)
arr = [10, 20, 30, 40, 50, 60]
v.check("05-06.2a", arr[2])
v.check("05-06.2b", arr[2 + 3])
v.check("05-06.2c", 5 - 2)
v.check("05-06.2d", (5 - 2) * struct.calcsize("=h"))
v.check("05-06.3a", len("VDD=1.8V"))
v.check("05-06.3b", len("VDD=1.8V") + 1)
v.check("05-06.3c", len("ok") + 1)
v.check("05-06.3d", POINTER)
data = [3, 9, 4, 12, 7, 15]
above = [i for i, x in enumerate(data) if x > 8]
v.check("05-06.4a", len(above))
v.check("05-06.4b", above[0])
s_size, s_off = layout([("a", ctypes.c_uint8), ("b", ctypes.c_uint16), ("c", ctypes.c_uint8), ("d", ctypes.c_uint32)])
v.check("05-06.5a", s_size)
v.check("05-06.5b", s_off["d"])
v.check("05-06.5c", min(layout(f)[0] for f in (
    [("d", ctypes.c_uint32), ("b", ctypes.c_uint16), ("a", ctypes.c_uint8), ("c", ctypes.c_uint8)],
    [("d", ctypes.c_uint32), ("a", ctypes.c_uint8), ("c", ctypes.c_uint8), ("b", ctypes.c_uint16)],
    [("a", ctypes.c_uint8), ("c", ctypes.c_uint8), ("b", ctypes.c_uint16), ("d", ctypes.c_uint32)])))
v.assert_true("8 bytes is the minimum possible: the fields alone occupy 1 + 2 + 1 + 4 bytes", 1 + 2 + 1 + 4 == 8)
v.check("05-06.7a", 10 - 1)
v.check("05-06.7b", len(status))
v.check("05-06.8a", 1000 * 64)
v.check("05-06.9a", sum(10 * r + c for r in range(3) for c in range(4)))
r2, c2, cap2 = grow(16, 2, 1, 10**6)
r15, c15, cap15 = grow(16, 3, 2, 10**6)                         # cap + cap // 2 equals 3 * cap // 2 for these integers
v.assert_true("cap + cap//2 and 3*cap//2 agree along the 1.5x sequence", all(
    (x + x // 2) == (3 * x) // 2 for x in range(16, 2 * 10**6)))
v.check("05-06.10a", r2)
v.check("05-06.10b", c2)
v.check("05-06.10c", r15)
v.check("05-06.10d", c15)
free_ram = 16 * 1024 - (3 * 512 * 2 + 4096 + 3 * 1024)
v.check("05-06.12a", free_ram // loose)
v.check("05-06.12b", free_ram // tight)

# ---------------------------------------------------------------- lab
lab_r, _, lab_cap = grow(8, 2, 1, 1000)
v.check("Lab 05-06.a", lab_r)
v.check("Lab 05-06.b", lab_cap)
lab_samples = [(37 * i) % 101 - 50 for i in range(1000)]
v.check("Lab 05-06.c", Fraction(sum(lab_samples), len(lab_samples)))
v.assert_true("the samples span -50 to 50", (min(lab_samples), max(lab_samples)) == (-50, 50))
v.check("Lab 05-06.d", len("n=%d min=%d max=%d mean=%.2f" % (1000, -50, 50, sum(lab_samples) / 1000)))
v.check("Lab 05-06.e", lab_cap * struct.calcsize("=h"))
v.check("Lab 05-06.f", 100 * 16 * ctypes.sizeof(ctypes.c_int))

sys.exit(v.finish())
