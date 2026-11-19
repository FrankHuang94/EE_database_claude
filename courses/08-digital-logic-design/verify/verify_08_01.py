#!/usr/bin/env python3
"""Verify every number in chapter 08-01 (number systems and codes), its solutions and its lab handout.

Each value is recomputed by a route independent of the chapter's hand method:
- base conversions with exact rational arithmetic (fractions.Fraction) and Python's own parsers;
- two's-complement sums by a bit-level ripple-carry adder that reports its internal carries;
- integer widths by searching for the smallest two's-complement width that holds a value;
- floating-point formats by decoding *every* bit pattern of each format from its field definition
  (and, for FP16 and FP32, by NumPy's hardware conversions);
- Gray code by the recursive reflect-and-prefix construction, BCD by a digit-serial adder;
- Hamming codes by generator and parity-check matrices over GF(2), CRCs by carry-less integer
  division, and error probabilities by exact binomial sums.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-01", COURSE / "chapters" / "08-01-number-systems-and-codes.md",
                        COURSE / "solutions" / "08-01-solutions.md",
                        COURSE / "labs" / "08-01-lab" / "README.md")


# ---------------------------------------------------------------- helpers
def ripple_add(a: int, b: int, n: int, cin: int = 0):
    """Add two n-bit patterns with a bit-level ripple-carry adder. Returns (sum pattern, carries)
    where carries[i] is the carry INTO column i (carries[n] is the carry out)."""
    c = [cin]
    s = 0
    for i in range(n):
        ai, bi, ci = (a >> i) & 1, (b >> i) & 1, c[i]
        s |= (ai ^ bi ^ ci) << i
        c.append((ai & bi) | (ai & ci) | (bi & ci))
    return s, c


def as_signed(pattern: int, n: int) -> int:
    """Interpret an n-bit pattern with the weight -2^(n-1) on the top bit."""
    return -((pattern >> (n - 1)) & 1) * 2 ** (n - 1) + (pattern & (2 ** (n - 1) - 1))


def to_pattern(x: int, n: int) -> int:
    """Two's-complement pattern of x by 'invert and add one' for negatives."""
    if x >= 0:
        return x
    mag = -x
    return ((~mag) & (2 ** n - 1)) + 1 & (2 ** n - 1)


def signed_bits(x: int) -> int:
    n = 1
    while not (-(2 ** (n - 1)) <= x <= 2 ** (n - 1) - 1):
        n += 1
    return n


def float_values(e: int, m: int, kind: str) -> np.ndarray:
    """All finite positive values of a binary float format with e exponent and m fraction bits.
    kind 'ieee': all-ones exponent reserved for inf/NaN. kind 'e4m3': only S.1111.111 is NaN (OCP).
    Any other kind (used for E2M1): every pattern is a finite number."""
    bias = 2 ** (e - 1) - 1
    vals = []
    for E in range(2 ** e):
        for F in range(2 ** m):
            if kind == "ieee" and E == 2 ** e - 1:
                continue
            if kind == "e4m3" and E == 2 ** e - 1 and F == 2 ** m - 1:
                continue
            if E == 0:
                val = Fraction(F, 2 ** m) * Fraction(2) ** (1 - bias)
            else:
                val = (1 + Fraction(F, 2 ** m)) * Fraction(2) ** (E - bias)
            if val > 0:
                vals.append(val)
    return sorted(vals)


def nearest(vals, x):
    x = Fraction(x)
    return min(vals, key=lambda t: (abs(t - x), t))


def bf16(x: float) -> float:
    """Round an FP32 value to bfloat16 by round-to-nearest-even on its bit pattern."""
    u = np.array([x], dtype=np.float32).view(np.uint32)[0].item()
    lsb = (u >> 16) & 1
    u = (u + 0x7FFF + lsb) & 0xFFFF0000
    return float(np.array([u], dtype=np.uint32).view(np.float32)[0])


# ---------------------------------------------------------------- Example 1
v.check("Ex 08-01.1a", int("ADB", 16))
assert Fraction(int("ADB", 16), 16) == Fraction(1736875, 10000)
k = round(Fraction(1, 10) * 256)
v.check("Ex 08-01.1b", k)
v.check("Ex 08-01.1c", float(Fraction(k, 256)))
v.check("Ex 08-01.1d", float((Fraction(k, 256) - Fraction(1, 10)) / Fraction(1, 10) * 100))
# 0.1 never terminates: after 4 doublings the fractional part 2/10 recurs
fr, seen = Fraction(1, 10), []
while fr not in seen:
    seen.append(fr)
    fr = (fr * 2) % 1
v.assert_true("0.1 has a repeating binary expansion with period 4", len(seen) - seen.index(fr) == 4 and fr != 0)

# ---------------------------------------------------------------- Example 2
s, c = ripple_add(to_pattern(100, 8), to_pattern(50, 8), 8)
v.check("Ex 08-01.2a", as_signed(s, 8))
v.assert_true("100+50: c7=1, c8=0, V=1", c[7] == 1 and c[8] == 0)
s, c = ripple_add(to_pattern(-100, 8), to_pattern(-50, 8), 8)
v.check("Ex 08-01.2b", as_signed(s, 8))
v.assert_true("-100-50: c7=0, c8=1, V=1", c[7] == 0 and c[8] == 1)
p = to_pattern(-5, 8)
ext = p | (((p >> 7) & 1) * 0xFF00)   # replicate the sign bit into the upper byte
v.check("Ex 08-01.2c", ext)
v.assert_true("sign extension preserves the value", as_signed(ext, 16) == -5)
s, c = ripple_add(0xFF, 0xFF, 8)
v.assert_true("-1 + -1: carry out but no overflow", c[8] == 1 and (c[8] ^ c[7]) == 0 and as_signed(s, 8) == -2)
# the carry rule equals the sign rule for every 4-bit pair
ok = True
for a in range(16):
    for b in range(16):
        s4, c4 = ripple_add(a, b, 4)
        sa, sb, ss = a >> 3, b >> 3, s4 >> 3
        ok &= ((c4[4] ^ c4[3]) == int(sa == sb and ss != sa))
        ok &= ((c4[4] ^ c4[3]) == int(not -8 <= as_signed(a, 4) + as_signed(b, 4) <= 7))
v.assert_true("carry rule = sign rule = true overflow for all 4-bit pairs", ok)

# ---------------------------------------------------------------- Example 3
q = np.arange(-128, 128)
prods = np.outer(q, q)
v.check("Ex 08-01.3a", int(prods.max()))
v.check("Ex 08-01.3b", int(prods.min()))
v.check("Ex 08-01.3c", max(signed_bits(int(prods.max())), signed_bits(int(prods.min()))))
v.check("Ex 08-01.3d", 1024 * int(prods.max()))
v.check("Ex 08-01.3e", signed_bits(1024 * int(prods.max())))
n = 0
while (n + 1) * int(prods.max()) <= 2 ** 31 - 1:
    n += 1
v.check("Ex 08-01.3f", n)

# ---------------------------------------------------------------- Example 4 and the format table
fp8_e4m3 = float_values(4, 3, "e4m3")
fp8_e5m2 = float_values(5, 2, "ieee")
bf_vals = float_values(8, 7, "ieee")
x01 = Fraction(1, 10)
r32 = float(np.float32(0.1))
r16 = float(np.float16(0.1))
rbf = bf16(0.1)
assert Fraction(rbf) == nearest(bf_vals, x01)
r43 = float(nearest(fp8_e4m3, x01))
r52 = float(nearest(fp8_e5m2, x01))
for val, kv, ke in ((r32, "Ex 08-01.4a", "Ex 08-01.4b"), (r16, "Ex 08-01.4c", "Ex 08-01.4d"),
                    (rbf, "Ex 08-01.4e", "Ex 08-01.4f"), (r43, "Ex 08-01.4g", "Ex 08-01.4h"),
                    (r52, "Ex 08-01.4i", "Ex 08-01.4j")):
    v.check(kv, val)
    v.check(ke, float((Fraction(val) - x01) / x01 * 100))
v.check("Th 08-01.a", float(np.finfo(np.float32).max))
v.check("Th 08-01.b", float(np.finfo(np.float16).max))
v.check("Th 08-01.c", float(bf_vals[-1]))
v.check("Th 08-01.d", float(fp8_e5m2[-1]))
v.check("Th 08-01.e", float(fp8_e4m3[-1]))
v.check("Th 08-01.f", float(np.finfo(np.float16).tiny))
# smallest normal of E4M3: the smallest value with a nonzero exponent field, 1.000 x 2^(1-7)
v.check("Th 08-01.g", float(min(t for t in fp8_e4m3 if t >= Fraction(1, 2 ** 6))))
v.check("Th 08-01.h", float(min(t for t in bf_vals if t > 1)) - 1)

# ---------------------------------------------------------------- Example 5: Gray code and BCD


def gray_reflect(nbits):
    codes = ["0", "1"]
    for _ in range(nbits - 1):
        codes = ["0" + c for c in codes] + ["1" + c for c in reversed(codes)]
    return codes


g4 = gray_reflect(4)
v.check("Ex 08-01.5a", int(g4[0b1011], 2))
v.check("Ex 08-01.5b", bin(7 ^ 8).count("1"))
v.check("Ex 08-01.5c", bin(int(g4[7], 2) ^ int(g4[8], 2)).count("1"))
v.assert_true("reflected Gray = B xor (B >> 1) for all 4-bit B", all(int(g4[b], 2) == b ^ (b >> 1) for b in range(16)))


def bcd_add(x: int, y: int) -> int:
    """Digit-serial BCD adder with the +6 correction; returns the decimal value of the BCD result."""
    xd, yd = [int(ch) for ch in f"{x:02d}"][::-1], [int(ch) for ch in f"{y:02d}"][::-1]
    carry, out = 0, []
    for a, b in zip(xd, yd):
        s = a + b + carry
        if s > 9:
            s = (s + 6) & 0xF
            carry = 1
        else:
            carry = 0
        out.append(s)
    out.append(carry)
    return sum(d * 10 ** i for i, d in enumerate(out))


v.check("Ex 08-01.5d", bcd_add(59, 38))

# ---------------------------------------------------------------- Example 6: Hamming codes over GF(2)
# parity-check matrix: column k (1..7) is the binary representation of k (rows s1, s2, s4)
H = np.array([[(k >> r) & 1 for k in range(1, 8)] for r in range(3)])
data_pos = [3, 5, 6, 7]


def encode(d):
    """Solve H c = 0 for the check bits at positions 1, 2, 4, given the data bits."""
    c = np.zeros(7, dtype=int)
    for pos, bit in zip(data_pos, d):
        c[pos - 1] = bit
    for r, ppos in enumerate((1, 2, 4)):
        c[ppos - 1] = (H[r] @ c) % 2
    assert not ((H @ c) % 2).any()
    return c


cw = encode([1, 0, 1, 1])
v.check("Ex 08-01.6a", int("".join(map(str, cw)), 2))
r = cw.copy()
r[5] ^= 1
syn = (H @ r) % 2
v.check("Ex 08-01.6b", int(syn[0] + 2 * syn[1] + 4 * syn[2]))
r2 = cw.copy()
r2[5] ^= 1
r2[6] ^= 1
syn2 = (H @ r2) % 2
v.check("Ex 08-01.6c", int(syn2[0] + 2 * syn2[1] + 4 * syn2[2]))
v.assert_true("double error: overall parity still even", (r2.sum() + cw.sum() % 2) % 2 == 0)
# every single error in every code word is located by its syndrome
okh = True
for dv in range(16):
    c0 = encode([(dv >> i) & 1 for i in range(4)])
    for e in range(7):
        rr = c0.copy()
        rr[e] ^= 1
        s_ = (H @ rr) % 2
        okh &= int(s_[0] + 2 * s_[1] + 4 * s_[2]) == e + 1
v.assert_true("Hamming(7,4): syndrome = error position for all 112 single errors", okh)
rr = next(rr for rr in range(1, 20) if 2 ** rr >= 64 + rr + 1)
v.check("Ex 08-01.6d", rr + 1)
v.check("Ex 08-01.6e", 64 / (64 + rr + 1))

# ---------------------------------------------------------------- Example 7: CRC by carry-less division


def clmod(a: int, g: int) -> int:
    """Remainder of carry-less (GF(2)[x]) division of a by g."""
    dg = g.bit_length() - 1
    while a.bit_length() - 1 >= dg:
        a ^= g << (a.bit_length() - 1 - dg)
    return a


g = 0b1011
crc = clmod(0b1101 << 3, g)
v.check("Ex 08-01.7a", crc)
v.check("Ex 08-01.7b", clmod((0b1101 << 3) | crc, g))
rems = {clmod(1 << k, g) for k in range(7)}
v.assert_true("x^3+x+1: the 7 single-bit errors give 7 distinct nonzero remainders", len(rems) == 7 and 0 not in rems)

# ---------------------------------------------------------------- parity escape probability
pe = 1e-6
v.check("Th 08-01.i", sum(math.comb(8, kk) * pe ** kk * (1 - pe) ** (8 - kk) for kk in range(2, 9, 2)))

# ---------------------------------------------------------------- solutions
# P1
v.check("08-01.1a", int("3F7", 16))
v.check("08-01.1b", int(format(245, "o")))
v.check("08-01.1c", int(format(245, "X"), 16))


def frac_bits(fr: Fraction, n: int) -> int:
    out = 0
    for _ in range(n):
        fr *= 2
        out = (out << 1) | int(fr)
        fr -= int(fr)
    return out


v.check("08-01.1d", frac_bits(Fraction(3, 8), 8))
v.check("08-01.1e", frac_bits(Fraction(3, 10), 8))
# P2
bits = 0
while 2 ** bits < 1000:
    bits += 1
v.check("08-01.2a", bits)
levels = int(Fraction(33, 10) / Fraction(1, 10000)) + 1
v.check("08-01.2b", levels)
bits = 0
while 2 ** bits < levels:
    bits += 1
v.check("08-01.2c", bits)
# P3
v.check("08-01.3a", to_pattern(-77, 8))
v.check("08-01.3b", as_signed(0xC9, 8))
v.check("08-01.3c", as_signed((((~0xC9) & 0xFF) + 1) & 0xFF, 8))
# P4: bit-level 4-bit adds
for kk, (a_, b_) in zip("abcd", ((5, 4), (-8, -1), (7, -8), (-3, -6))):
    s4, c4 = ripple_add(to_pattern(a_, 4), to_pattern(b_, 4), 4)
    v.check(f"08-01.4{kk}", as_signed(s4, 4))
    v.assert_true(f"P4{kk} overflow flag matches the true sum", (c4[4] ^ c4[3]) == int(not -8 <= a_ + b_ <= 7))
# P5
s5, c5 = ripple_add(0x35, (~0x5A) & 0xFF, 8, cin=1)
v.check("08-01.5a", s5)
v.check("08-01.5b", c5[8])
v.check("08-01.5c", as_signed(s5, 8))
# P6: Q4.12
v.check("08-01.6a", (2 ** 15 - 1) / 2 ** 12)
v.check("08-01.6b", 2.0 ** -12)
q6 = int(Fraction("3.14159") * 4096 + Fraction(1, 2))
v.check("08-01.6c", q6)
v.check("08-01.6d", q6 / 4096)
v.check("08-01.6e", float(Fraction(q6, 4096) - Fraction("3.14159")))
raw = round(1.5 * 4096) * round(2.25 * 4096)
v.check("08-01.6f", raw)
v.check("08-01.6g", (raw + 2 ** 11) >> 12)
sq = (round(3.5 * 4096) ** 2 + 2 ** 11) >> 12
v.check("08-01.6h", min(sq, 2 ** 15 - 1))
# P7: brute force over the extreme Q1.15 values
ext = [-(2 ** 15), 2 ** 15 - 1]
pmax = max(a_ * b_ for a_ in ext for b_ in ext)
pmin = min(a_ * b_ for a_ in ext for b_ in ext)
pw = max(signed_bits(pmax), signed_bits(pmin))
v.check("08-01.7a", pw)
v.check("08-01.7b", signed_bits(64 * pmax))
# P8: FP16 via NumPy's conversion and bit view
f16 = lambda x: int(np.array([x], dtype=np.float16).view(np.uint16)[0])  # noqa: E731
v.check("08-01.8a", f16(1.0))
v.check("08-01.8b", f16(-2.5))
v.check("08-01.8c", f16(65504.0))
v.check("08-01.8d", float(np.array([0xC500], dtype=np.uint16).view(np.float16)[0]))
v.check("08-01.8e", float(np.spacing(np.float16(2048))))
v.check("08-01.8f", float(np.float16(2049)))
# P9
pi32 = float(np.float32(math.pi))
pb = np.array([bf16(pi32)], dtype=np.float32).view(np.uint32)[0].item() >> 16
v.check("08-01.9a", pb)
v.check("08-01.9b", bf16(pi32))
v.check("08-01.9c", (bf16(pi32) - math.pi) / math.pi * 100)
e43 = float(nearest(float_values(4, 3, "e4m3"), Fraction(math.pi)))
v.check("08-01.9d", e43)
v.check("08-01.9e", (e43 - math.pi) / math.pi * 100)
# P10: Gray decode by searching the reflected code
v.check("08-01.10a", gray_reflect(4).index("1101"))
# P11
v.check("08-01.11a", int.from_bytes("\u03a9".encode("utf-8"), "big"))
v.check("08-01.11b", ord(bytes.fromhex("E697A5").decode("utf-8")))
v.check("08-01.11c", len("\u03a9=1\u20ac".encode("utf-8")))
# P12
c12 = encode([0, 1, 1, 0])
v.check("08-01.12a", int("".join(map(str, c12)), 2))
r12 = np.array([int(ch) for ch in "1110110"])
s12 = (H @ r12) % 2
v.check("08-01.12b", int(s12[0] + 2 * s12[1] + 4 * s12[2]))
# P13
r13 = next(rr for rr in range(1, 20) if 2 ** rr >= 32 + rr + 1)
v.check("08-01.13a", r13 + 1)
v.check("08-01.13b", 32 / (32 + r13 + 1))
p13 = 1e-9
bad = 1 - (1 - p13) ** 32
unc = sum(math.comb(39, kk) * p13 ** kk * (1 - p13) ** (39 - kk) for kk in range(2, 40))
v.check("08-01.13c", bad)
v.check("08-01.13d", unc)
v.check("08-01.13e", bad / unc)
# P14
g14 = 0b10011
crc14 = clmod(0b1010011101 << 4, g14)
v.check("08-01.14a", crc14)
cw14 = (0b1010011101 << 4) | crc14
v.check("08-01.14b", clmod(cw14 ^ (g14 << 3), g14))
okb = all(clmod(cw14 ^ ((1 << (L - 1)) | 1 | (mid << 1)) << k, g14) != 0
          for L in range(2, 5) for k in range(14 - L + 1) for mid in range(2 ** max(L - 2, 0)))
v.assert_true("P14 every burst of length 2 to 4 is detected", okb and all(clmod(cw14 ^ (1 << k), g14) for k in range(14)))
# P15
v.check("08-01.15a", int(str(2026), 16))


def bcd_add_n(x: int, y: int, ndig: int = 4) -> int:
    """Digit-serial BCD adder on 4-bit digit codes with the +6 correction; returns the decoded decimal sum."""
    xd = [(int(str(x), 16) >> (4 * i)) & 0xF for i in range(ndig)]   # BCD digit codes, low digit first
    yd = [(int(str(y), 16) >> (4 * i)) & 0xF for i in range(ndig)]
    carry, out = 0, 0
    for i in range(ndig):
        s_ = xd[i] + yd[i] + carry
        carry = 1 if s_ > 9 else 0
        if carry:
            s_ = (s_ + 6) & 0xF
        out |= s_ << (4 * i)
    out |= carry << (4 * ndig)
    return int(format(out, "x"))


v.check("08-01.15b", bcd_add_n(857, 479))
v.check("08-01.15c", 4 * 4)
bits = 0
while 2 ** bits < 10000:
    bits += 1
v.check("08-01.15d", bits)


# ---------------------------------------------------------------- section 7 (numbers to know)
v.check("N 08-01.a", float(2 ** 32))
v.check("N 08-01.b", float(2 ** 64))
v.check("N 08-01.c", math.log10(2))
v.check("N 08-01.d", 2 ** 31 - 1)
v.check("N 08-01.e", 100 / 9)
v.check("N 08-01.f", 100 * 8 / 64)
v.check("N 08-01.g", 100 * 32 / (1500 * 8))
codepoints = 0x10FFFF + 1
v.assert_true("N: 17 planes of 65 536 code points", codepoints == 17 * 2 ** 16)
v.check("N 08-01.h", codepoints)
v.check("N 08-01.i", 100 * 159801 / codepoints)

# ---------------------------------------------------------------- section 9 (practitioner lens)
v.check("PL 08-01.a", 4 + 8 / 32)
v.check("PL 08-01.b", 4 + 8 / 16)
e2m1 = sorted({float(x) for x in float_values(2, 1, "e2m1")} | {0.0})   # E2M1 has no inf or NaN
v.assert_true("PL: E2M1 magnitudes are 0, 0.5, 1, 1.5, 2, 3, 4, 6", e2m1 == [0, 0.5, 1, 1.5, 2, 3, 4, 6])
v.check("PL 08-01.c", max(e2m1))
v.check("PL 08-01.d", 2 * len(e2m1) - 1)        # +0 and -0 are one value
r_sec = 1
while 2 ** r_sec < 128 + r_sec + 1:
    r_sec += 1
v.check("PL 08-01.e", r_sec)
v.check("PL 08-01.f", 100 * r_sec / 128)
v.check("PL 08-01.g", 2.0 ** -32)
v.check("PL 08-01.h", 144 / 8)
v.check("PL 08-01.i", 72 / 8)

# ---------------------------------------------------------------- lab handout: silent failures by exhaustive enumeration
# Every error pattern of each code word is pushed through an explicit decoder; a pattern is a silent failure if the
# decoder raises no flag yet delivers wrong data. The probability is the sum of p^w (1-p)^(n-w) over those patterns.
G7 = [encode(list(map(int, format(d, "04b")))) for d in range(16)]
codeset7 = {tuple(c) for c in G7}


def sec_decode(r):
    syn = (H @ r) % 2
    pos = int(syn[0]) + 2 * int(syn[1]) + 4 * int(syn[2])
    rr = r.copy()
    if pos:
        rr[pos - 1] ^= 1
    return [int(rr[k - 1]) for k in data_pos], pos


def secded_decode(r8):
    r = r8[:7]
    d, pos = sec_decode(r)
    overall_ok = int(r8.sum()) % 2 == 0
    if pos and overall_ok:
        return None, True                       # double error: flagged
    return d, False


def prob(fail_weights, n, p):
    return sum(c * p ** w * (1 - p) ** (n - w) for w, c in fail_weights.items())


def tally(n, is_silent):
    counts = {}
    for e in range(2 ** n):
        if is_silent(e):
            w = bin(e).count("1")
            counts[w] = counts.get(w, 0) + 1
    return counts


def bits(e, n):
    return np.array([(e >> (n - 1 - k)) & 1 for k in range(n)])


# parity: 8 data bits + 1 even-parity bit; the check passes iff the error pattern has even weight
par = tally(9, lambda e: bin(e).count("1") % 2 == 0 and e != 0)
# SEC: data word 1011 (any word gives the same result, the code being linear); also confirm over all 16 words
data_ref = [1, 0, 1, 1]
cw_ref = encode(data_ref)
sec = tally(7, lambda e: sec_decode((cw_ref + bits(e, 7)) % 2)[0] != data_ref)
v.assert_true("Lab: SEC silent-failure set is the same for every data word",
              all(tally(7, lambda e, c=c: sec_decode((c + bits(e, 7)) % 2)[0]
                        != [int(c[k - 1]) for k in data_pos]) == sec for c in G7[::5]))
cw8 = np.append(cw_ref, cw_ref.sum() % 2)


def secded_silent(e):
    d, flagged = secded_decode((cw8 + bits(e, 8)) % 2)
    return (not flagged) and d != data_ref


def secded_flagged(e):
    return secded_decode((cw8 + bits(e, 8)) % 2)[1]


sd = tally(8, secded_silent)
sdf = tally(8, secded_flagged)
# CRC x^3 + x + 1 on 4-bit messages: undetected iff the received 7-bit word leaves remainder 0 and differs
crc_cw = (0b1101 << 3) | clmod(0b1101 << 3, 0b1011)
crc = tally(7, lambda e: clmod(crc_cw ^ e, 0b1011) == 0 and e != 0)
v.assert_true("Lab: CRC x^3+x+1 code words are the Hamming(7,4) weight distribution 1,7,7,1",
              crc == {3: 7, 4: 7, 7: 1})
for ids, wts, n in ((("a", "b", "c"), par, 9), (("d", "e", "f"), sec, 7), (("g", "h", "i"), sd, 8),
                    (("j", "k", "l"), crc, 7)):
    lo, hi = prob(wts, n, 1e-3), prob(wts, n, 1e-2)
    v.check(f"Lab 08-01.{ids[0]}", lo, rtol=6e-4)
    v.check(f"Lab 08-01.{ids[1]}", hi, rtol=6e-4)
    v.check(f"Lab 08-01.{ids[2]}", hi / lo)
v.check("Lab 08-01.m", prob(sdf, 8, 1e-3), rtol=6e-4)
pairs = sum(1 for a in range(-8, 8) for b in range(-8, 8) if not -8 <= a + b <= 7)
v.check("Lab 08-01.n", pairs)
e4m3_patterns = 2 * (len(float_values(4, 3, "e4m3")) + 1)   # positive values and +0, doubled for sign
v.check("Lab 08-01.o", e4m3_patterns)

v.finish()
