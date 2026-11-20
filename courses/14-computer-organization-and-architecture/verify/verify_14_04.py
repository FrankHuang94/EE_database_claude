#!/usr/bin/env python3
"""Verify every number in chapter 14-04, its problem set and its lab.

Independent routes:
- integer results by executing RV32IM instructions on the course simulator (_rv32.py), compared with
  Python's exact integers;
- division by constants by the excess condition d*M - 2^(32+k) <= 2^k, by brute-force tests on ten million
  random inputs plus boundary values, and by compiling x / d with clang and reading the constants back;
- floating-point results twice: in NumPy FP32 arithmetic, and by exact rational arithmetic (fractions)
  followed by a round-to-nearest-even FP32 rounding function written here from the definition;
- an integer-only FP32 adder with guard, round and sticky bits, compared with NumPy on random pairs;
- summations performed element by element in FP32 and compared with the exact rational sum;
- quantization by direct computation, with SQNR from the data.
"""
from __future__ import annotations

import math
import random
import re
import struct
import subprocess
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(HERE))
from eeverify import Verifier  # noqa: E402
from _rv32 import M32, run_function, sx, tool  # noqa: E402

ROOT = HERE.parent
v = Verifier.from_files("14-04", ROOT / "chapters" / "14-04-computer-arithmetic-and-number-formats.md",
                        ROOT / "solutions" / "14-04-solutions.md", ROOT / "labs" / "14-04-lab" / "README.md")
f32 = np.float32


def bits(x) -> int:
    return struct.unpack("<I", struct.pack("<f", float(x)))[0]


def from_bits(b: int) -> float:
    return struct.unpack("<f", struct.pack("<I", b))[0]


def round_f32(q: Fr) -> Fr:
    """Round an exact rational to the nearest FP32 value, ties to even (normal range only)."""
    if q == 0:
        return Fr(0)
    sgn, a = (1, q) if q > 0 else (-1, -q)
    e = math.floor(math.log2(a))
    while Fr(2) ** e > a:
        e -= 1
    while Fr(2) ** (e + 1) <= a:
        e += 1
    ulp = Fr(2) ** (e - 23)
    n, rem = divmod(a, ulp)
    n = int(n)
    if rem > ulp / 2 or (rem == ulp / 2 and n % 2 == 1):
        n += 1
    return sgn * n * ulp


# --------------------------------------------------------------------------- RV32IM execution helper
OPS = """    .text
    .globl t
t:  add   a2, a0, a1
    slt   a3, a2, zero
    sltu  a4, a2, zero
    slt   a5, a0, a1
    sltu  a6, a0, a1
    mul   a7, a0, a1
    mulh  t3, a0, a1
    mulhu t4, a0, a1
    div   t5, a0, a1
    rem   t6, a0, a1
    divu  s2, a0, a1
    remu  s3, a0, a1
    ret
"""
# t uses s2/s3 without saving them; the stub does not depend on them.


def ops(a: int, b: int) -> dict:
    x = run_function({"t.s": OPS}, "t", [a, b], m=True)["sim"].x
    names = ["add", "slt0", "sltu0", "slt", "sltu", "mul", "mulh", "mulhu", "div", "rem", "divu", "remu"]
    regs = [12, 13, 14, 15, 16, 17, 28, 29, 30, 31, 18, 19]
    return dict(zip(names, (x[r] for r in regs)))


# =========================================================================== Examples
r = ops(0x7FFFFFFF, 1)
v.check("Ex 14-04.1a", r["add"])
v.check("Ex 14-04.1b", r["slt0"])
v.assert_true("sltu (result < 0) is 0", r["sltu0"] == 0)
a_, b_, s_ = 0x7FFFFFFF, 1, r["add"]
v.check("Ex 14-04.1c", (((a_ ^ s_) & (b_ ^ s_)) >> 31) & 1)
r = ops(-1, 1)
v.check("Ex 14-04.1d", r["slt"])
v.check("Ex 14-04.1e", r["sltu"])

r = ops(-3, 5)
v.check("Ex 14-04.2a", r["mul"])
v.check("Ex 14-04.2b", r["mulh"])
v.check("Ex 14-04.2c", r["mulhu"])
v.assert_true("MUL/MULH/MULHU agree with exact products", r["mul"] == (-15) & M32 and r["mulh"] == ((-15) >> 32) & M32
              and r["mulhu"] == (((2**32 - 3) * 5) >> 32))
r0, r1, r2 = ops(7, 0), ops(-2**31, -1), ops(-7, 2)
v.check("Ex 14-04.2d", sx(r0["div"], 32))
v.assert_true("REM 7 / 0 = 7", r0["rem"] == 7)
v.check("Ex 14-04.2e", sx(r1["div"], 32))
v.assert_true("REM of the overflow case is 0", r1["rem"] == 0)
v.check("Ex 14-04.2f", sx(r2["div"], 32))
v.check("Ex 14-04.2g", sx(r2["rem"], 32))


def magic(d: int) -> tuple[int, int]:
    """Smallest k with d*M - 2^(32+k) <= 2^k, and its M (may exceed 32 bits)."""
    k = 0
    while True:
        M = -(-(2 ** (32 + k)) // d)
        if d * M - 2 ** (32 + k) <= 2 ** k:
            return M, 32 + k
        k += 1


def mulshift_ok(d: int, M: int, sh: int, n: int = 10**7, seed: int = 1404) -> bool:
    rng = np.random.default_rng(seed)
    xs = np.concatenate([rng.integers(0, 2**32, n, dtype=np.uint64),
                         np.array([0, 1, d - 1, d, 2**32 - 1, 2**32 - d, 2**31, 2**31 - 1], dtype=np.uint64)])
    hi = (xs * np.uint64(M & 0xFFFFFFFF)) >> np.uint64(32)  # x*M fits in 64 bits only for 32-bit M
    if M < 2**32:
        q = (xs * np.uint64(M)) >> np.uint64(sh)
    else:
        q = (((xs - hi) >> np.uint64(1)) + hi) >> np.uint64(sh - 33)
    return bool(np.all(q == xs // np.uint64(d)))


def clang_magic(d: int) -> tuple[int, list[int], list[str]]:
    src = f"unsigned f(unsigned x) {{ return x / {d}; }}\n"
    out = subprocess.run([tool("clang"), "--target=riscv32", "-march=rv32im", "-mabi=ilp32", "-O2", "-S", "-x", "c", "-", "-o", "-"],
                         input=src, capture_output=True, text=True, check=True).stdout
    lui = int(re.search(r"lui\s+a1, (\d+)", out).group(1))
    addi = int(re.search(r"addi\s+a1, a1, (-?\d+)", out).group(1))
    shifts = [int(s) for s in re.findall(r"srli\s+a0, a0, (\d+)", out)]
    insns = re.findall(r"^\s+(lui|addi|mulhu|sub|srli|add)\b", out, re.M)
    return ((lui << 12) + addi) & M32, shifts, insns


M10, sh10 = magic(10)
v.assert_true("M = ceil(2^35/10) = (2^35 + 2)/10, shift 35", (M10, sh10) == ((2**35 + 2) // 10, 35))
v.assert_true("division by 10: identity holds on 10^7 random and boundary inputs", mulshift_ok(10, M10, sh10))
cm, csh, cins = clang_magic(10)
v.assert_true("clang 18 emits lui/addi/mulhu/srli with 0xCCCCCCCD and shift 3", cm == M10 and csh == [3] and cins == ["lui", "addi", "mulhu", "srli"])
v.check("Ex 14-04.3a", len(cins))
v.check("Ex 14-04.3b", M10)
v.check("Ex 14-04.3c", sh10 - 32)
v.assert_true("error term bound 2x/(10*2^35) < 1/40 and M/2^35 = 0.100000000005821", 2 * 2**32 / (10 * 2**35) <= 1 / 40
              and abs(M10 / 2**35 - 0.100000000005821) < 5e-16)
v.assert_true("lui 0xCCCCD + addi -819 builds the constant", (0xCCCCD << 12) - 819 == M10)

one = f32(1)
for ID, a, b in (("Ex 14-04.4a", 1.0, 2**-24), ("Ex 14-04.4b", 1.0, 1.5 * 2**-24), ("Ex 14-04.4c", 1 + 2**-23, 2**-24)):
    hw = bits(f32(a) + f32(b))
    v.assert_true(f"{ID}: NumPy FP32 agrees with exact rounding", from_bits(hw) == float(round_f32(Fr(a) + Fr(b))))
    v.check(ID, hw)

N = 10**6
x01 = f32(0.1)
exact = Fr(float(x01)) * N
seq = f32(0)
for _ in range(N):
    seq = f32(seq + x01)


def pairwise(n):  # sum of n copies of x01, recursive halving, every addition in FP32
    if n == 1:
        return x01
    h = n // 2
    return f32(pairwise(h) + pairwise(n - h))


pw = pairwise(N)
s, c = f32(0), f32(0)
for _ in range(N):
    y = f32(x01 - c)
    t = f32(s + y)
    c = f32(f32(t - s) - y)
    s = t
rel = lambda val: float((Fr(float(val)) - exact) / exact)  # noqa: E731
v.check("Ex 14-04.5a", float(seq))
v.check("Ex 14-04.5b", 100 * rel(seq))
v.check("Ex 14-04.5c", float(pw))
v.check("Ex 14-04.5d", float(s))
v.assert_true("pairwise relative error about -9.3e-8", abs(rel(pw) + 9.3e-8) < 5e-10)
v.assert_true("Kahan relative error about -1.5e-8 and Kahan = nearest FP32 to the exact sum", abs(rel(s) + 1.5e-8) < 1e-9 and Fr(float(s)) == round_f32(exact))
v.assert_true("pairwise is one ulp below Kahan at 1e5", float(s) - float(pw) == 2**-7)
v.assert_true("pairwise about 1e5 times more accurate than sequential", 5e4 < rel(seq) / abs(rel(pw)) < 2e5)
v.assert_true("sequential error is inside the (n-1)u bound", abs(rel(seq)) < (N - 1) * 2**-24)
v.assert_true("13 ulps of 2^-7 per addition in [2^16, 2^17): 0.1015625", round(0.1 / 2**-7) * 2**-7 == 0.1015625)
v.assert_true("(1e8 + 1) - 1e8 = 0 in FP32 and the spacing at 1e8 is 8", f32(f32(1e8) + one) - f32(1e8) == 0 and np.spacing(f32(1e8)) == 8)

w = np.array([0.43, -1.31, 0.027, 0.88, -0.555, 1.12, -0.094, 0.705])
sc = np.max(np.abs(w)) / 127
q = np.round(w / sc).astype(int)
deq = q * sc
v.check("Ex 14-04.6a", sc)
v.assert_true("INT8 codes", list(q) == [42, -127, 3, 85, -54, 109, -9, 68])
v.check("Ex 14-04.6b", q[5])
v.check("Ex 14-04.6c", np.max(np.abs(deq - w)))
v.assert_true("largest error within s/2", np.max(np.abs(deq - w)) <= sc / 2)
v.check("Ex 14-04.6d", 20 * np.log10(np.sqrt(np.mean(w**2)) / np.sqrt(np.mean((deq - w) ** 2))))
v.check("Ex 14-04.6e", (2**31 - 1) // 127**2)
v.assert_true("133144 products fit and 133145 might not", 133144 * 127**2 <= 2**31 - 1 < 133145 * 127**2)

E2M1 = [0, 0.5, 1, 1.5, 2, 3, 4, 6]


def to_e2m1(x: float) -> float:
    """Round to the E2M1 grid, ties to even (the encoding with mantissa bit 0), clamping above 6."""
    a = min(abs(x), 6.0)
    best = min(E2M1, key=lambda g: (abs(g - a), E2M1.index(g) % 2))
    return math.copysign(best, x) if best else 0.0


def mx_block(vals, emax_pow2=4):
    X = 2.0 ** math.floor(math.log2(max(abs(x) for x in vals))) / emax_pow2
    return X, [to_e2m1(x / X) for x in vals]


vv = [0.9, -2.7, 0.15, 5.3, -1.2, 0.04, 3.9, -0.6]
X, P = mx_block(vv)
v.check("Ex 14-04.6f", X)
v.assert_true("FP4 elements", P == [1.0, -3.0, 0.0, 6.0, -1.0, 0.0, 4.0, -0.5])
v.check("Ex 14-04.6g", P[3])
v.check("Ex 14-04.6h", max(abs(p * X - x) for p, x in zip(P, vv)))
v.assert_true("E2M1 has 15 distinct values with sign", len({s * g for g in E2M1 for s in (1, -1)}) == 15)

# §3.6 area model and the Google comparison
p2 = {k: p * p for k, p in (("fp32", 24), ("fp16", 11), ("bf16", 8), ("e4m3", 4))}
v.assert_true("p^2 table: 576, 121, 64, 16; ratios 0.21, 0.11, 0.028; bf16/fp16 about half", (p2["fp32"], p2["fp16"], p2["bf16"], p2["e4m3"]) == (576, 121, 64, 16)
              and round(121 / 576, 2) == 0.21 and round(64 / 576, 2) == 0.11 and round(16 / 576, 3) == 0.028 and 0.45 < 64 / 121 < 0.6)
v.assert_true("MX FP4 block: 8 + 32*4 = 136 bits, 4.25 per element", 8 + 32 * 4 == 136 and 136 / 32 == 4.25)

# =========================================================================== Problems
r = ops(0xFFFFFF9C - 2**32, 0)
SH = """    .text
    .globl t
t:  srai a2, a0, 2
    srli a3, a0, 2
    ret
"""
x = run_function({"sh.s": SH}, "t", [-100])["sim"].x
v.check("14-04.1a", 0xFFFFFF9C)
v.check("14-04.1b", 0xFFFFFF9C - 2**32)
v.check("14-04.1c", sx(x[12], 32))
v.check("14-04.1d", x[13])

for ID, a, b, kind in (("14-04.2a", 0x40000000, 0x40000000, "signed"), ("14-04.2b", 0xFFFFFFFF, 2, "carry"), ("14-04.2c", 0xFFFFFFFF, 2, "signed")):
    s_ = (a + b) & M32
    v.check(ID, ((((a ^ s_) & (b ^ s_)) >> 31) & 1) if kind == "signed" else int(s_ < a))
v.assert_true("0x40000000 + 0x40000000 has no unsigned carry", (0x80000000 >= 0x40000000))

LB = """    .text
    .globl t
t:  lb   a2, 0(a0)
    lbu  a3, 0(a0)
    ret
"""
x = run_function({"lb.s": LB}, "t", [0x20000], data={0x20000: 0xF0})["sim"].x
v.check("14-04.3a", sx(x[12], 32))
v.check("14-04.3b", x[13])

r = ops(0x89ABCDEF - 2**32, 0x12345678)
v.check("14-04.4a", r["mul"])
v.check("14-04.4b", r["mulhu"])
v.check("14-04.4c", r["mulh"])
v.assert_true("MULH = MULHU - b (mod 2^32)", r["mulh"] == (r["mulhu"] - 0x12345678) & M32)

ra, rb = ops(-7, -2), ops(7, -2)
v.check("14-04.5a", sx(ra["div"], 32))
v.check("14-04.5b", sx(ra["rem"], 32))
v.check("14-04.5c", sx(rb["div"], 32))
v.check("14-04.5d", sx(rb["rem"], 32))
v.check("14-04.5e", ops(0xFFFFFFFE - 2**32, 2)["divu"])
v.check("14-04.5f", ops(5, 0)["remu"])

M3, sh3 = magic(3)
cm3, csh3, _ = clang_magic(3)
v.assert_true("division by 3: identity holds; clang agrees", mulshift_ok(3, M3, sh3) and cm3 == M3 and csh3 == [sh3 - 32])
v.check("14-04.6a", M3)
v.check("14-04.6b", sh3)
v.assert_true("M3 = (2^33 + 1)/3", M3 * 3 == 2**33 + 1)

rows7 = [(k, -(-(2 ** (32 + k)) // 7)) for k in range(4)]
v.assert_true("excesses 3, 6, 5 exceed 2^k for k <= 2; k = 3 qualifies with a 33-bit M",
              [7 * M - 2 ** (32 + k) for k, M in rows7] == [3, 6, 5, 3] and all(7 * M - 2 ** (32 + k) > 2**k for k, M in rows7[:3])
              and rows7[3][1] >= 2**32 and magic(7) == (rows7[3][1], 35))
M2 = rows7[2][1]
first = next(x for x in range(-(-(2**34) // 5), 2**32) if x % 7 == 6)
v.assert_true("the first candidate fails and the analytic argument holds", (first * M2) >> 34 != first // 7)
lo = first - 2_000_000
xs = np.arange(lo, first, dtype=np.uint64)
v.assert_true("no failure in the 2 million inputs below it", bool(np.all((xs * np.uint64(M2)) >> np.uint64(34) == xs // np.uint64(7))))
v.check("14-04.7a", first)
cm7, csh7, cins7 = clang_magic(7)
v.check("14-04.7b", rows7[3][1] - 2**32)
v.assert_true("clang's x/7 uses 0x24924925 with the sub/srli/add/srli fix-up", cm7 == rows7[3][1] - 2**32 and cins7 == ["lui", "addi", "mulhu", "sub", "srli", "add", "srli"] and csh7 == [1, 2])
v.assert_true("fix-up sequence exact on 10^7 random and boundary inputs", mulshift_ok(7, rows7[3][1], 35))

v.check("14-04.8a", float(np.spacing(f32(1000))))
v.assert_true("ulp at 1000 = 2^-14", float(np.spacing(f32(1000))) == 2**-14)
v.check("14-04.8b", 2**24 + 1)
v.check("14-04.8c", float(f32(2**24 + 1)))
v.assert_true("all integers up to 2^24 are exact", all(float(f32(n)) == n for n in (2**24 - 1, 2**24, 2**24 - 12345)))

for ID, a, b in (("14-04.9a", 1.75, 2**-24 + 2**-30), ("14-04.9b", 1.75, 2**-25), ("14-04.9c", 16777215.0, 1.5)):
    hw = bits(f32(a) + f32(b))
    v.assert_true(f"{ID}: FP32 agrees with exact rounding", from_bits(hw) == float(round_f32(Fr(a) + Fr(b))))
    v.check(ID, hw)

a, b, c = f32(1 + 2**-13), f32(1 - 2**-13), f32(-1)
v.assert_true("a, b, c are exact in FP32", float(a) == 1 + 2**-13 and float(b) == 1 - 2**-13)
sep = f32(f32(a * b) + c)
fma = round_f32(Fr(float(a)) * Fr(float(b)) + Fr(float(c)))
v.check("14-04.10a", float(sep))
v.check("14-04.10b", float(fma))
v.assert_true("FMA result is exactly -2^-26", fma == -Fr(1, 2**26))

v.check("14-04.11a", 4095 * 2**-8)
v.check("14-04.11b", 4095 * 2**-24)
v.check("14-04.11c", next(p for p in range(1, 40) if 4095 * 2.0**-p < 0.01))

X, P = mx_block([7.5, 1.0, -2.0])
v.check("14-04.12a", X)
v.check("14-04.12b", P[0])
v.check("14-04.12c", 7.5 - P[0] * X)
v.check("14-04.12d", abs(to_e2m1(7.5 / 2) * 2 - 7.5))
worst = max((m - 6) / m for m in np.linspace(4, 8 - 1e-9, 100001))
v.check("14-04.12e", 100 * 2 / 8)
v.assert_true("relative clamping error approaches but never reaches 25%", 0.2499 < worst < 0.25)

s13 = 7 / 255
z = round(1 / s13)
q13 = round(2.5 / s13) + z
v.check("14-04.13a", s13)
v.check("14-04.13b", z)
v.check("14-04.13c", q13)
v.check("14-04.13d", s13 * (q13 - z))
v.assert_true("-1 maps near code 0 and 6 near code 255", round(-1 / s13) + z == 0 and round(6 / s13) + z == 255)

m14 = 4096 * 127**2
v.check("14-04.14a", math.ceil(math.log2(m14 + 1)) + 1)
v.check("14-04.14b", math.ceil(math.log2(32 * 36 * 4 + 1)) + 1)
v.assert_true("E2M1 products are multiples of 0.25 with magnitude <= 36", all((Fr(p) * Fr(q)) % Fr(1, 4) == 0 for p in E2M1 for q in E2M1)
              and max(p * q for p in E2M1 for q in E2M1) == 36)

# =========================================================================== Lab
M1000, sh1000 = magic(1000)
cm1000, csh1000, _ = clang_magic(1000)
v.assert_true("÷1000: identity holds and clang agrees", mulshift_ok(1000, M1000, sh1000) and cm1000 == M1000 and csh1000 == [sh1000 - 32])
v.check("Lab 14-04.a", M1000)
v.check("Lab 14-04.b", sh1000)


def add_f32_bits(x: int, y: int, sticky: bool = True) -> int:
    """Add two positive normal FP32 numbers given as bit patterns, using integers only (round to nearest even)."""
    ex, ey = x >> 23 & 0xFF, y >> 23 & 0xFF
    mx, my = (x & 0x7FFFFF) | 0x800000, (y & 0x7FFFFF) | 0x800000
    if (ex, mx) < (ey, my):
        ex, ey, mx, my = ey, ex, my, mx
    d = ex - ey
    my3 = my << 3  # three extra bits: guard, round, sticky
    if d:
        shifted = my3 >> d if d < 27 else 0
        lost = my3 & ((1 << d) - 1) if d < 27 else my3
        if sticky and lost:
            shifted |= 1
        my3 = shifted
    m = (mx << 3) + my3
    e = ex
    if m >> 27:  # carry out: renormalize, folding the dropped bit into sticky
        m = (m >> 1) | (m & 1 if sticky else 0)
        e += 1
    keep, low = m >> 3, m & 7
    if low > 4 or (low == 4 and keep & 1):
        keep += 1
        if keep >> 24:
            keep >>= 1
            e += 1
    return (e << 23) | (keep & 0x7FFFFF)


rnd = random.Random(14041)
mism = mism_ns = 0
for i in range(100_000):
    ea, eb = rnd.randint(100, 150), rnd.randint(100, 150)
    if i % 4 == 0:
        eb = ea - rnd.randint(0, 3)  # many close exponents, where rounding is busiest
    xa = (ea << 23) | rnd.getrandbits(23)
    xb = (max(eb, 1) << 23) | rnd.getrandbits(23)
    hw = bits(f32(from_bits(xa)) + f32(from_bits(xb)))
    mism += add_f32_bits(xa, xb) != hw
    mism_ns += add_f32_bits(xa, xb, sticky=False) != hw
v.check("Lab 14-04.c", mism)
v.assert_true("without the sticky bit the adder disagrees on some pairs", mism_ns > 0)

N5 = 10**5
s5 = f32(0)
for _ in range(N5):
    s5 = f32(s5 + x01)
v.check("Lab 14-04.d", 100 * float((Fr(float(s5)) - Fr(float(x01)) * N5) / (Fr(float(x01)) * N5)))
v.assert_true("pairwise error stays at or below about 1e-7 for n = 10 .. 1e6",
              all(abs(float((Fr(float(pairwise(n))) - Fr(float(x01)) * n) / (Fr(float(x01)) * n))) < 1.5e-7 for n in (10, 100, 1000, 10**4, 10**5, 10**6)))

# Part 4 claims on Gaussian data (Box-Muller from random.random(), stable across Python versions)
g = random.Random(7)
data = []
while len(data) < 4096:
    u1, u2 = g.random(), g.random()
    if u1 > 0:
        r_ = math.sqrt(-2 * math.log(u1))
        data += [r_ * math.cos(2 * math.pi * u2), r_ * math.sin(2 * math.pi * u2)]
data = np.array(data[:4096])


def sqnr(xq):
    return 20 * math.log10(np.sqrt(np.mean(data**2)) / np.sqrt(np.mean((xq - data) ** 2)))


def int_q(bits_):
    L = 2 ** (bits_ - 1) - 1
    s_ = np.max(np.abs(data)) / L
    return np.clip(np.round(data / s_), -L, L) * s_


mx = np.concatenate([np.array(mx_block(list(blk))[1]) * mx_block(list(blk))[0] for blk in data.reshape(-1, 32)])
s8, s4, smx = sqnr(int_q(8)), sqnr(int_q(4)), sqnr(mx)
v.assert_true(f"INT8 - INT4 SQNR about 6 dB per bit ({s8 - s4:.1f} dB for 4 bits)", 21 < s8 - s4 < 27)
v.assert_true(f"MX FP4 ({smx:.1f} dB) beats per-tensor INT4 ({s4:.1f} dB)", smx > s4)

sys.exit(v.finish())
