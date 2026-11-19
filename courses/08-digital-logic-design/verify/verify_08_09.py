#!/usr/bin/env python3
"""Verify every number in chapter 08-09 (arithmetic circuits), its solutions and lab.

Independent routes:
- adders are built as prefix networks of (G, P) operators, checked on random additions against
  Python integers, and timed by an arrival-time simulation in the unit-delay model (carry-in folded
  into bit 0's generate); carry-select adders are timed by composing ripple blocks and multiplexers;
- operator counts and levels are counted on the constructed networks, then compared with formulas;
- Dadda multipliers are built bit by bit, checked against Python multiplication, and their adders
  counted; Booth digits are recomputed and checked by summation;
- fixed-point results use integer arithmetic; rounding biases are computed by enumerating every
  value of the dropped bits; SQNR from the formula and from a measured quantized sine;
- energies come from Horowitz's 45 nm table (R-157), as published.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-09", COURSE / "chapters" / "08-09-arithmetic-circuits.md",
                        COURSE / "solutions" / "08-09-solutions.md",
                        COURSE / "labs" / "08-09-lab" / "README.md")
rng = random.Random(9)


# ---------------------------------------------------------------- prefix networks
def ripple(n):
    return [[(i, i - 1)] for i in range(1, n)]


def kogge_stone(n):
    out, d = [], 1
    while d < n:
        out.append([(i, i - d) for i in range(d, n)])
        d *= 2
    return out


def sklansky(n):
    out, d = [], 1
    while d < n:
        out.append([(i, (i // d) * d - 1) for i in range(n) if (i // d) % 2 == 1])
        d *= 2
    return out


def brent_kung(n):
    out, d = [], 1
    while d < n:
        out.append([(i, i - d) for i in range(2 * d - 1, n, 2 * d)])
        d *= 2
    d //= 4
    while d >= 1:
        lv = [(i, i - d) for i in range(3 * d - 1, n, 2 * d)]
        if lv:
            out.append(lv)
        d //= 2
    return out


def run(levels, n, a, b, cin, t_bit0=3):
    A = [(a >> i) & 1 for i in range(n)]
    B = [(b >> i) & 1 for i in range(n)]
    P = [x ^ y for x, y in zip(A, B)]
    g = [x & y for x, y in zip(A, B)]
    g[0] |= P[0] & cin
    p, lo = P[:], list(range(n))
    tg, tp = [1] * n, [1] * n
    tg[0] = t_bit0
    for lv in levels:
        ng, np_, ntg, ntp, nlo = g[:], p[:], tg[:], tp[:], lo[:]
        for i, j in lv:
            assert lo[i] == j + 1
            ng[i] = g[i] | (p[i] & g[j])
            np_[i] = p[i] & p[j]
            ntg[i] = max(tg[i], max(tp[i], tg[j]) + 1) + 1
            ntp[i] = max(tp[i], tp[j]) + 1
            nlo[i] = lo[j]
        g, p, tg, tp, lo = ng, np_, ntg, ntp, nlo
    assert all(x == 0 for x in lo)
    s = sum((P[i] ^ (g[i - 1] if i else cin)) << i for i in range(n)) | (g[n - 1] << n)
    t_sum = max(max(1, tg[i - 1] if i else 0) + 1 for i in range(n))
    return s, t_sum, tg[n - 1]


NETS = {"ripple": ripple, "KS": kogge_stone, "Sk": sklansky, "BK": brent_kung}
INFO = {}
for name, f in NETS.items():
    for n in (4, 8, 16, 32, 64):
        L = f(n)
        for _ in range(200):
            a, b, c = rng.getrandbits(n), rng.getrandbits(n), rng.getrandbits(1)
            assert run(L, n, a, b, c)[0] == a + b + c
        fan = max(sum(1 for i, j in lv if j == k) for lv in L for k in range(n))
        _, ts, tc = run(L, n, 0, 0, 0)
        INFO[name, n] = dict(ops=sum(map(len, L)), levels=len(L), fan=fan, t_sum=ts, t_cout=tc)
v.assert_true("all four networks add correctly at 4 to 64 bits (random tests)", True)
lg = {n: int(math.log2(n)) for n in (16, 32, 64)}
v.assert_true("operator-count formulas match the constructed networks",
              all(INFO["KS", n]["ops"] == n * lg[n] - n + 1 and INFO["Sk", n]["ops"] == n // 2 * lg[n]
                  and INFO["BK", n]["ops"] == 2 * n - 2 - lg[n] and INFO["BK", n]["levels"] == 2 * lg[n] - 1
                  for n in (16, 32, 64)))
v.assert_true("ripple sum delay is 2n (matches 08-04)", all(INFO["ripple", n]["t_sum"] == 2 * n for n in (4, 8, 16, 32, 64)))

# ================================================================= chapter, theory keys
E = {"add8": 0.03, "add32": 0.1, "fadd16": 0.4, "fadd32": 0.9, "mul8": 0.2, "mul32": 3.1, "fmul16": 1.1,
     "fmul32": 3.7, "cache32k": 20.0}                        # Horowitz 2014, Fig. 1.1.9 (pJ)
v.check("Th 08-09.a", E["mul32"] / E["mul8"])
v.check("Th 08-09.b", E["add32"] / E["add8"])
v.check("Th 08-09.c", 10 * math.log10(1.5 * 2 ** 32))
v.check("Th 08-09.d", 10 * math.log10(1.5 * 2 ** 24))
v.check("Th 08-09.e", 2 ** -15)


def barrel_muxes(n):
    return n * int(math.log2(n))


v.check("Th 08-09.f", barrel_muxes(32))
v.check("Th 08-09.g", 32 + math.ceil(math.log2(64)))

# ================================================================= chapter, examples
A1, B1 = 0b10110110, 0b01011101
G1, P1 = A1 & B1, A1 ^ B1
v.check("Ex 08-09.1a", G1)
v.check("Ex 08-09.1b", P1)


def carries(a, b, n, cin=0):
    c = [cin]
    for i in range(n):
        gi, pi = (a >> i) & (b >> i) & 1, ((a ^ b) >> i) & 1
        c.append(gi | (pi & c[-1]))
    return c


def longest_propagate(a, b, n):
    """Longest run of consecutive bits through which an actual carry passes (P = 1 and carry in = 1)."""
    c = carries(a, b, n)
    best = cur = 0
    for i in range(n):
        if ((a ^ b) >> i) & 1 and c[i]:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


c1 = carries(A1, B1, 8)
v.check("Ex 08-09.1c", (A1 + B1) & 0xFF)
v.check("Ex 08-09.1d", c1[8])
v.assert_true("sum bits equal P xor C", all((((A1 + B1) >> i) & 1) == (((P1 >> i) & 1) ^ c1[i]) for i in range(8)))
v.check("Ex 08-09.1e", longest_propagate(A1, B1, 8))


def lookahead_terms(k):
    """Terms of the flat C_k: G_{k-1}, P_{k-1}G_{k-2}, ..., P_{k-1}..P_0 C_0; returns literal lists."""
    terms = []
    for j in range(k - 1, -2, -1):
        lits = [f"P{m}" for m in range(k - 1, j, -1)] + ([f"G{j}"] if j >= 0 else ["C0"])
        terms.append(lits)
    return terms


def check_lookahead(k):
    for _ in range(500):
        a, b, c0 = rng.getrandbits(k), rng.getrandbits(k), rng.getrandbits(1)
        env = {"C0": c0}
        for i in range(k):
            env[f"G{i}"] = (a >> i) & (b >> i) & 1
            env[f"P{i}"] = ((a ^ b) >> i) & 1
        val = int(any(all(env[l] for l in t) for t in lookahead_terms(k)))
        if val != carries(a, b, k, c0)[k]:
            return False
    return True


v.assert_true("flat lookahead equations equal the ripple recurrence (k = 3, 4, 8, 16)",
              all(check_lookahead(k) for k in (3, 4, 8, 16)))
t4 = lookahead_terms(4)
v.check("Ex 08-09.2a", len(t4))
v.check("Ex 08-09.2b", max(map(len, t4)))
v.check("Ex 08-09.2c", sum(sum(1 for t in lookahead_terms(k) if len(t) >= 2) for k in range(1, 5)))
t16 = lookahead_terms(16)
v.check("Ex 08-09.2d", len(t16))
v.check("Ex 08-09.2e", max(map(len, t16)))

v.check("Ex 08-09.3a", INFO["KS", 16]["ops"])
v.check("Ex 08-09.3b", INFO["KS", 16]["levels"])
v.check("Ex 08-09.3c", INFO["Sk", 16]["ops"])
v.check("Ex 08-09.3d", INFO["BK", 16]["ops"])
v.check("Ex 08-09.3e", INFO["BK", 16]["levels"])
v.check("Ex 08-09.3f", INFO["ripple", 16]["t_sum"])
v.check("Ex 08-09.3g", INFO["KS", 16]["t_sum"])
v.check("Ex 08-09.3h", INFO["Sk", 16]["t_sum"])
v.check("Ex 08-09.3i", INFO["BK", 16]["t_sum"])
v.check("Ex 08-09.3j", INFO["ripple", 16]["t_sum"] / INFO["KS", 16]["t_sum"])
v.check("Ex 08-09.3k", INFO["ripple", 16]["t_sum"] / INFO["Sk", 16]["t_sum"])
v.check("Ex 08-09.3l", INFO["ripple", 16]["t_sum"] / INFO["BK", 16]["t_sum"])
v.check("Ex 08-09.3m", INFO["KS", 64]["t_sum"])
v.check("Ex 08-09.3n", INFO["Sk", 64]["t_sum"])
v.check("Ex 08-09.3o", INFO["BK", 64]["t_sum"])
v.check("Ex 08-09.3p", INFO["ripple", 64]["t_sum"])
v.assert_true("per-level fan-out: KS 1, BK 1, Sklansky n/2",
              INFO["KS", 16]["fan"] == 1 and INFO["BK", 16]["fan"] == 1 and INFO["Sk", 16]["fan"] == 8)


# carry-select: timing by composing ripple blocks (with constant or real carry-in) and 2-unit muxes
MUX = 2


def carry_select(block, nblocks):
    L = ripple(block)
    _, ts0, tc0 = run(L, block, 0, 0, 0, t_bit0=3)          # real carry-in: bit-0 generate at 3
    _, tsk, tck = run(L, block, 0, 0, 0, t_bit0=1)          # constant carry-in: bit-0 generate at 1
    t_carry, t_sum = tc0, ts0
    for _ in range(1, nblocks):
        t_sum = max(t_sum, max(tsk, t_carry) + MUX)
        t_carry = max(tck, t_carry) + MUX
    fas = block + (nblocks - 1) * 2 * block
    muxes = (nblocks - 1) * (block + 1)
    return max(t_sum, t_carry), fas, muxes, tc0, tsk, tck


cs2 = carry_select(16, 2)
v.check("Ex 08-09.4a", cs2[3])
v.check("Ex 08-09.4b", cs2[4])
v.check("Ex 08-09.4c", cs2[5])
v.check("Ex 08-09.4d", cs2[0])
v.check("Ex 08-09.4e", INFO["ripple", 32]["t_sum"])
v.check("Ex 08-09.4f", cs2[1])
v.check("Ex 08-09.4g", cs2[2])


# Dadda multiplier, bit by bit
def dadda_targets(n):
    d = [2]
    while d[-1] < n:
        d.append(d[-1] * 3 // 2)
    return [t for t in reversed(d) if t < n]


def dadda(a, b, n):
    cols = [[((a >> i) & 1) & ((b >> j) & 1) for i in range(n) for j in range(n) if i + j == c]
            for c in range(2 * n)]
    heights0 = [len(c) for c in cols]
    fa = ha = 0
    for t in dadda_targets(n):
        new = [[] for _ in range(2 * n + 1)]
        for c in range(2 * n):
            bits = cols[c]
            h = len(bits) + len(new[c])
            while h > t:
                if h - t >= 2 and len(bits) >= 3:
                    x, y, z = bits.pop(), bits.pop(), bits.pop()
                    new[c].append(x ^ y ^ z)
                    new[c + 1].append((x & y) | (x & z) | (y & z))
                    fa, h = fa + 1, h - 2
                else:
                    x, y = bits.pop(), bits.pop()
                    new[c].append(x ^ y)
                    new[c + 1].append(x & y)
                    ha, h = ha + 1, h - 1
            new[c].extend(bits)
        cols = new[:2 * n]
        assert all(len(col) <= t for col in cols)
    final = sum(1 for col in cols if len(col) == 2)
    return sum(sum(col) << c for c, col in enumerate(cols)), fa, ha, final, heights0


for n in (8, 12, 16, 24, 32):
    for _ in range(100):
        a, b = rng.getrandbits(n), rng.getrandbits(n)
        assert dadda(a, b, n)[0] == a * b
v.assert_true("Dadda multipliers (8 to 32 bits) multiply correctly, bit by bit", True)
_, fa8, ha8, fin8, h8 = dadda(1, 1, 8)
v.check("Ex 08-09.5a", sum(h8))
v.check("Ex 08-09.5b", max(h8))
v.check("Ex 08-09.5c", len(dadda_targets(8)))
v.check("Ex 08-09.5d", fa8)
v.check("Ex 08-09.5e", ha8)
v.check("Ex 08-09.5f", fin8)
v.check("Ex 08-09.5g", len(dadda_targets(24)))
v.assert_true("FA count equals n^2 - 4n + 3 and HA count n - 1 (8 to 32 bits)",
              all(dadda(1, 1, n)[1] == n * n - 4 * n + 3 and dadda(1, 1, n)[2] == n - 1 for n in (8, 12, 16, 24, 32)))


def booth(B, n=8):
    bits = [(B >> i) & 1 for i in range(n)]
    padded = [0] + bits
    return [-2 * padded[2 * k + 2] + padded[2 * k + 1] + padded[2 * k] for k in range(n // 2)]


d122 = booth(122)
v.assert_true("Booth digits of 122 are -2, -1, 0, +2", d122 == [-2, -1, 0, 2])
v.check("Ex 08-09.6a", sum(d * 4 ** k for k, d in enumerate(d122)))
v.check("Ex 08-09.6b", sum(d * 45 * 4 ** k for k, d in enumerate(d122)))
v.check("Ex 08-09.6c", sum(d != 0 for d in d122))
v.check("Ex 08-09.6d", bin(122).count("1"))

v.check("Ex 08-09.7a", 16 + 16)
v.check("Ex 08-09.7b", 32 + math.ceil(math.log2(64)))
v.check("Ex 08-09.7c", 48 - 32)
v.check("Ex 08-09.7d", 2 ** (48 - 32))
q = (24576 * -16384 + 2 ** 14) >> 15
v.check("Ex 08-09.7e", q)
v.check("Ex 08-09.7f", q / 2 ** 15)
v.check("Ex 08-09.7g", 10 * math.log10(1.5 * 2 ** 32))

# ================================================================= solutions
A, B = 92, 59
v.check("08-09.1a", A & B)
v.check("08-09.1b", A ^ B)
v.check("08-09.1c", (A + B) & 0xFF)
v.check("08-09.1d", (A + B) >> 8)
v.check("08-09.1e", longest_propagate(A, B, 8))


def op(hi, lo):
    return (hi[0] | (hi[1] & lo[0]), hi[1] & lo[1])


b3, b2, b1, b0 = (0, 1), (0, 1), (1, 0), (0, 0)
r1 = op(op(b3, b2), op(b1, b0))
r2 = op(b3, op(b2, op(b1, b0)))
v.assert_true("both groupings agree", r1 == r2)
v.check("08-09.2a", r1[0])
v.check("08-09.2b", r1[1])
v.check("08-09.2c", op((0, 0), (1, 0))[0])
v.check("08-09.2d", op((1, 0), (0, 0))[0])
v.check("08-09.3a", INFO["KS", 32]["ops"])
v.check("08-09.3b", INFO["KS", 32]["levels"])
v.check("08-09.3c", INFO["Sk", 32]["ops"])
v.check("08-09.3d", INFO["BK", 32]["ops"])
v.check("08-09.3e", INFO["BK", 32]["levels"])
v.check("08-09.4a", INFO["ripple", 64]["t_sum"] * 15e-3)
v.check("08-09.4b", INFO["KS", 64]["t_sum"] * 15e-3)
v.check("08-09.4c", INFO["BK", 64]["t_sum"] * 15e-3)
v.check("08-09.4d", INFO["KS", 64]["ops"])
cs4 = carry_select(8, 4)
v.check("08-09.5a", cs4[0])
v.check("08-09.5b", cs4[1])
v.check("08-09.5c", cs4[2])
v.check("08-09.6a", len(lookahead_terms(3)))
t8 = lookahead_terms(8)
v.check("08-09.6b", len(t8))
v.check("08-09.6c", max(map(len, t8)))
v.check("08-09.6d", 16 // 4)
_, fa12, ha12, fin12, h12 = dadda(1, 1, 12)
v.check("08-09.7a", sum(h12))
v.check("08-09.7b", len(dadda_targets(12)))
v.check("08-09.7c", fa12)
v.check("08-09.7d", ha12)
v.check("08-09.7e", fin12)
dm99 = booth(-99 & 0xFF)
v.assert_true("Booth digits of -99 are +1, -1, +2, -2", dm99 == [1, -1, 2, -2])
v.check("08-09.8a", sum(d * 4 ** k for k, d in enumerate(dm99)))
v.check("08-09.8b", sum(d * 7 * 4 ** k for k, d in enumerate(dm99)))
v.check("08-09.8c", sum(d != 0 for d in dm99))
v.check("08-09.9a", int(math.log2(64)))
v.check("08-09.9b", barrel_muxes(64))
v.check("08-09.9c", 64 * 63)
pat = -40 & 0xFF
v.check("08-09.9d", pat >> 3)
v.check("08-09.9e", (pat - 256) >> 3)                       # Python >> on negative ints is arithmetic
v.check("08-09.10a", 8 - 2 ** -12)
v.check("08-09.10b", 2 ** -12)
code = round(math.e * 4096)
v.check("08-09.10c", code)
v.check("08-09.10d", code / 4096 - math.e)
v.check("08-09.11a", 12 + 16)
v.assert_true("(-2^11)(-2^15) needs 28 signed bits", (-2 ** 11) * (-2 ** 15) == 2 ** 26 and 2 ** 26 > 2 ** 26 - 1)
v.check("08-09.11b", 28 + math.ceil(math.log2(256)))
v.check("08-09.12a", 10 * math.log10(1.5 * 2 ** 24))
v.check("08-09.12b", next(b for b in range(1, 40) if 10 * math.log10(1.5 * 2 ** (2 * b)) >= 90))
v.check("08-09.12c", 10 * math.log10(1.5 * 2 ** 48))
# P13: enumerate all 2^15 values of the dropped bits
r = np.arange(2 ** 15)
trunc_err = (-r) / 2 ** 15
round_err = np.where(r < 2 ** 14, -r, 2 ** 15 - r) / 2 ** 15
v.check("08-09.13a", trunc_err.mean())
v.check("08-09.13b", round_err.mean())
v.check("08-09.13c", 1000 * trunc_err.mean())
v.check("08-09.13d", 1000 * round_err.mean())
v.check("08-09.14a", 27 + 18)
v.check("08-09.14b", 48 - 45)
v.check("08-09.14c", 2 ** 3)
v.check("08-09.14d", 18 + 18)
v.check("08-09.14e", 48 - 36)
v.check("08-09.14f", 2 ** 12)
mac8 = E["mul8"] + E["add32"]
mac32 = E["fmul32"] + E["fadd32"]
v.check("08-09.15a", mac8)
v.check("08-09.15b", mac32)
v.check("08-09.15c", mac32 / mac8)
v.check("08-09.15d", E["cache32k"] / mac8)
v.check("08-09.15e", 100 * mac8 / (mac8 + E["cache32k"]))

# ================================================================= lab
v.check("Lab 08-09.a", INFO["KS", 64]["t_sum"] / INFO["KS", 16]["t_sum"])
v.check("Lab 08-09.b", INFO["KS", 64]["ops"] / INFO["KS", 16]["ops"])
v.check("Lab 08-09.c", INFO["Sk", 64]["fan"])
_, fa32, _, _, _ = dadda(1, 1, 32)
v.check("Lab 08-09.d", fa32)
v.check("Lab 08-09.e", len(dadda_targets(32)))
nz = [sum(d != 0 for d in booth(x & 0xFF)) for x in range(-128, 128)]
v.assert_true("every signed 8-bit Booth recoding sums to its value",
              all(sum(d * 4 ** k for k, d in enumerate(booth(x & 0xFF))) == x for x in range(-128, 128)))
v.check("Lab 08-09.f", sum(nz) / 256)
nrng = np.random.default_rng(809)
qa = nrng.integers(-32768, 32768, 200_000)
qb = nrng.integers(-32768, 32768, 200_000)
prod = qa * qb
v.check("Lab 08-09.g", float(np.mean((prod >> 15) - prod / 2 ** 15)), tol=0.005)
t = np.arange(2 ** 16)
x = np.sin(2 * np.pi * 1031 / 2 ** 16 * t + 0.3)
qx = np.round(x * (2 ** 15 - 1)) / (2 ** 15 - 1)
v.check("Lab 08-09.h", 10 * math.log10(np.mean(x ** 2) / np.mean((x - qx) ** 2)))
v.check("Lab 08-09.i", 2 ** 16)

v.finish()
