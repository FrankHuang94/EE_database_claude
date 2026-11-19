#!/usr/bin/env python3
"""Verify every number in chapter 08-07 (registers, counters, shift registers, LFSRs), solutions and lab.

Independent routes:
- registers, counters and shift registers are simulated cycle by cycle from their next-state definitions;
- ripple counters are simulated as events with clock-to-Q delays;
- LFSR periods come from stepping the register; primitivity of the PRBS polynomials is proved with
  polynomial arithmetic over GF(2) (Rabin's irreducibility test and the order test), since stepping a
  31-bit register through its period is impractical;
- m-sequence statistics are measured on generated sequences.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-07", COURSE / "chapters" / "08-07-registers-counters-shift-registers.md",
                        COURSE / "solutions" / "08-07-solutions.md",
                        COURSE / "labs" / "08-07-lab" / "README.md")
PRINT = "--print" in sys.argv


# ---------------------------------------------------------------- GF(2) polynomials as integers
def pmulmod(a, b, m):
    r, dm = 0, m.bit_length() - 1
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if (a >> dm) & 1:
            a ^= m
    return r


def ppowmod(a, e, m):
    r = 1
    while e:
        if e & 1:
            r = pmulmod(r, a, m)
        a = pmulmod(a, a, m)
        e >>= 1
    return r


def pgcd(a, b):
    while b:
        while a and a.bit_length() >= b.bit_length():
            a ^= b << (a.bit_length() - b.bit_length())
        a, b = b, a
    return a


def prime_factors(n):
    f, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            f.add(d)
            n //= d
        d += 1
    if n > 1:
        f.add(n)
    return sorted(f)


def poly(n, k):
    return (1 << n) | (1 << k) | 1


def is_primitive(n, k):
    p, x = poly(n, k), 2
    if ppowmod(x, 2 ** n, p) != x:
        return False
    if any(pgcd(ppowmod(x, 2 ** (n // q), p) ^ x, p) != 1 for q in prime_factors(n)):
        return False
    return all(ppowmod(x, (2 ** n - 1) // q, p) != 1 for q in prime_factors(2 ** n - 1))


# ---------------------------------------------------------------- LFSR simulation (Fibonacci)
def lfsr_step(state, n, k):
    """state bit i-1 holds Q_i; Q1 <- Q_n xor Q_k, others shift toward Q_n."""
    fb = ((state >> (n - 1)) ^ (state >> (k - 1))) & 1
    return ((state << 1) | fb) & ((1 << n) - 1)


def lfsr_cycles(n, k):
    seen, cycles = set(), []
    for start in range(1, 2 ** n):
        if start in seen:
            continue
        s, length = start, 0
        while True:
            s = lfsr_step(s, n, k)
            seen.add(s)
            length += 1
            if s == start:
                break
        cycles.append(length)
    return sorted(cycles)


def lfsr_bits(n, k, count, state=1):
    out = []
    for _ in range(count):
        out.append((state >> (n - 1)) & 1)
        state = lfsr_step(state, n, k)
    return out


def runs(bits):
    """Runs of a periodic sequence: rotate so it starts at a run boundary."""
    i = next(j for j in range(len(bits)) if bits[j] != bits[j - 1])
    b = bits[i:] + bits[:i]
    out, cur, ln = [], b[0], 0
    for x in b:
        if x == cur:
            ln += 1
        else:
            out.append((cur, ln))
            cur, ln = x, 1
    out.append((cur, ln))
    return out


# ================================================================= chapter
def usr(q, mode, sin=0, d=0, w=4):
    m = (1 << w) - 1
    if mode == "hold":
        return q
    if mode == "right":
        return ((sin << (w - 1)) | (q >> 1)) & m
    if mode == "left":
        return ((q << 1) | sin) & m
    return d & m


q = 0b1011
seq = []
for mode, sin, d in (("right", 0, 0), ("left", 1, 0), ("left", 0, 0), ("load", 0, 0b1100), ("hold", 0, 0)):
    q = usr(q, mode, sin, d)
    seq.append(q)
v.check("Ex 08-07.1a", seq[0])
v.check("Ex 08-07.1b", seq[1])
v.check("Ex 08-07.1c", seq[2])
v.check("Ex 08-07.1d", seq[4])
v.check("Ex 08-07.2a", 32 * 500e6 / 1e9)
v.check("Ex 08-07.2b", 32)
v.check("Ex 08-07.2c", 16 * 64 / 66)
v.check("Ex 08-07.2d", 100 * 2 / 66)


def sync_count(q, n=4, up=True):
    """Next state from toggle conditions, not from +1."""
    nq = 0
    for i in range(n):
        lower = [(q >> j) & 1 for j in range(i)]
        t = all(lower) if up else all(b == 0 for b in lower)
        nq |= (((q >> i) & 1) ^ int(t)) << i
    return nq


q = 0b0110
for _ in range(5):
    q = sync_count(q)
v.check("Ex 08-07.3a", q)
v.check("Ex 08-07.3b", bin(0b0111 ^ sync_count(0b0111)).count("1"))
tog = sum(bin(c ^ sync_count(c)).count("1") for c in range(16))
v.check("Ex 08-07.3c", tog)
v.check("Ex 08-07.3d", tog / 16)


def bcd_next(q):
    return 0 if ((q >> 3) & 1) and (q & 1) else sync_count(q)


visited, q = set(), 0
for _ in range(20):
    visited.add(q)
    q = bcd_next(q)
v.assert_true("BCD counter cycles 0..9", visited == set(range(10)))
v.check("Ex 08-07.3e", 16 - len(visited))


def ripple_events(start, n, tcq):
    """Toggle stage 0; each stage that falls 1 -> 0 toggles the next after tcq. Returns state trace."""
    q, t, trace, stage = start, 0.0, [], 0
    while stage < n:
        t += tcq
        old = (q >> stage) & 1
        q ^= 1 << stage
        trace.append((t, q))
        if old == 1:          # it fell: the next stage toggles
            stage += 1
        else:
            break
    return trace


tr = ripple_events(0b0111, 4, 2.0)
v.check("Ex 08-07.4a", max(t for t, _ in ripple_events(0b0111, 4, 2.0)) if tr[-1][1] == 0b1000 else 0)
v.check("Ex 08-07.4b", 1e3 / (4 * 2.0 + 2.0))
v.check("Ex 08-07.4c", len([s for _, s in tr if s != 0b1000]))


def ring_next(q, n=4):
    return ((q >> 1) | ((q & 1) << (n - 1))) & ((1 << n) - 1)


def johnson_next(q, n=4):
    return ((q >> 1) | ((1 - (q & 1)) << (n - 1))) & ((1 << n) - 1)


def orbit(f, start):
    s, out = start, []
    while True:
        out.append(s)
        s = f(s)
        if s == start:
            return out


ring = orbit(ring_next, 0b1000)
john = orbit(johnson_next, 0b0000)
v.check("Ex 08-07.5a", len(ring))
v.check("Ex 08-07.5b", 16 - len(ring))
v.check("Ex 08-07.5c", len(john))
v.check("Ex 08-07.5d", 16 - len(john))
v.check("Ex 08-07.5e", math.ceil(math.log2(len(john))))
v.assert_true("Johnson sequence from 0000 is 0000 1000 1100 1110 1111 0111 0011 0001",
              john == [0, 8, 12, 14, 15, 7, 3, 1])
v.check("Ex 08-07.6a", lfsr_cycles(4, 3)[0] if len(lfsr_cycles(4, 3)) == 1 else 0)
v.check("Ex 08-07.6b", sum(lfsr_bits(4, 3, 15)))
c42 = lfsr_cycles(4, 2)
v.assert_true("x^4+x^2+1 cycles are 3, 6, 6", c42 == [3, 6, 6])
v.check("Ex 08-07.6c", max(c42))
v.check("Ex 08-07.6d", min(c42))
v.assert_true("x^4+x^3+1 is primitive and x^4+x^2+1 is not", is_primitive(4, 3) and not is_primitive(4, 2))
PRBS = {7: 6, 15: 14, 23: 18, 31: 28}
v.assert_true("PRBS7/15/23/31 polynomials are primitive", all(is_primitive(n, k) for n, k in PRBS.items()))
v.assert_true("PRBS7 and PRBS15 periods by stepping", lfsr_cycles(7, 6) == [127]
              and len(set(orbit(lambda s: lfsr_step(s, 15, 14), 1))) == 32767)
v.check("Ex 08-07.7a", 2 ** 31 - 1)
v.check("Ex 08-07.7b", (2 ** 31 - 1) / 106.25e9 * 1e3)
v.check("Ex 08-07.7c", 2 ** 30)
v.check("Ex 08-07.7d", (2 ** 7 - 1) / 106.25e9 * 1e9)
v.check("N 08-07.a", 2 ** 7 - 1)
v.check("N 08-07.b", 2 ** 15 - 1)
v.check("N 08-07.c", 2 ** 23 - 1)
# longest runs in an m-sequence: n ones and n - 1 zeros, checked on n = 7 and 15, applied to 31
for n, k in ((7, 6), (15, 14)):
    r = runs(lfsr_bits(n, k, 2 ** n - 1))
    v.assert_true(f"longest runs for n = {n}", max(l for b, l in r if b == 1) == n and max(l for b, l in r if b == 0) == n - 1)
v.check("PL 08-07.a", 31)
v.check("PL 08-07.b", 30)


# ================================================================= solutions
def clmul(a, b):
    """Carry-less (GF(2)) polynomial product."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def pmod(a, m):
    while a and a.bit_length() >= m.bit_length():
        a ^= m << (a.bit_length() - m.bit_length())
    return a


# P1: SIPO shifting left, MSB first
q = 0
for b in (1, 0, 1, 1, 0, 0, 1, 0):
    q = ((q << 1) | b) & 0xFF
v.check("08-07.1a", q)
# P2: PISO, LSB first
bits = [(0x5A >> i) & 1 for i in range(8)]
v.assert_true("0x5A LSB first is 0,1,0,1,1,0,1,0", bits == [0, 1, 0, 1, 1, 0, 1, 0])
v.check("08-07.2a", sum(bits))
v.check("08-07.2b", sum(a != b for a, b in zip(bits, bits[1:])))
# P3: smallest n with 2^n >= N
for N, ida, idb in ((60, "08-07.3a", "08-07.3b"), (24, "08-07.3c", "08-07.3d")):
    n = next(n for n in range(1, 10) if 2 ** n >= N)
    v.check(ida, n)
    v.check(idb, 2 ** n - N)
# P4: down counter from toggle conditions
q = 0b0010
for _ in range(5):
    q = sync_count(q, 4, up=False)
v.check("08-07.4a", q)
v.assert_true("down count from 1000 gives 0111", sync_count(0b1000, 4, up=False) == 0b0111)
v.check("08-07.4b", bin(0b1000 ^ sync_count(0b1000, 4, up=False)).count("1"))
# P5: chain T_i = T_(i-1) AND Q_(i-1) with T_1 = Q_0, so T_7 has 6 ANDs; tree of 7 inputs
ands = [0, 0] + [i - 1 for i in range(2, 8)]          # ANDs on the path to T_i
tpcq, tand, txor, tsu = 60, 25, 30, 40
v.check("08-07.5a", ands[7])
t_chain = tpcq + ands[7] * tand + txor + tsu
v.check("08-07.5b", t_chain)
v.check("08-07.5c", 1e3 / t_chain)
levels, width = 0, 7
while width > 1:
    width, levels = math.ceil(width / 2), levels + 1
v.check("08-07.5d", levels)
t_tree = tpcq + levels * tand + txor + tsu
v.check("08-07.5e", t_tree)
v.check("08-07.5f", 1e3 / t_tree)
# P6: ripple divider, simulated
ev = ripple_events(2 ** 10 - 1, 10, 0.5)
v.check("08-07.6a", 100e6 / 2 ** 10 / 1e3)
v.check("08-07.6b", ev[-1][0])
v.assert_true("ripple from all ones ends at 0", ev[-1][1] == 0)


# P7: 5-bit Johnson counter
def johnson5(q):
    return johnson_next(q, 5)


j5 = orbit(johnson5, 0)
v.check("08-07.7a", 5 if len(j5) == 10 else 0)
v.check("08-07.7b", 2 ** 5 - len(j5))
v.check("08-07.7c", 100 * sum(s & 1 for s in j5) / len(j5))
# each state is decoded by one two-input AND of two literals: find one that matches only that state
def decodable(s, states, n=5):
    for i in range(n):
        for j in range(i + 1, n):
            lit = ((s >> i) & 1, (s >> j) & 1)
            if [t for t in states if ((t >> i) & 1, (t >> j) & 1) == lit] == [s]:
                return True
    return False


v.check("08-07.7d", sum(decodable(s, j5) for s in j5))
# P8: ring counter loaded with 1100; rotation cycles of 4 bits
v.check("08-07.8a", len(orbit(ring_next, 0b1100)))
seen, cyc = set(), 0
for s0 in range(16):
    if s0 not in seen:
        seen.update(orbit(ring_next, s0))
        cyc += 1
v.check("08-07.8b", cyc)
# P9, P10: LFSR cycles
v.check("08-07.9a", lfsr_cycles(3, 2)[0] if lfsr_cycles(3, 2) == [7] else 0)
v.check("08-07.9b", sum(lfsr_bits(3, 2, 7)))
v.check("08-07.9c", lfsr_cycles(3, 1)[0] if lfsr_cycles(3, 1) == [7] else 0)
v.check("08-07.10a", lfsr_cycles(5, 3)[0] if lfsr_cycles(5, 3) == [31] else 0)
c54 = lfsr_cycles(5, 4)
v.check("08-07.10b", c54[0])
v.check("08-07.10c", c54[1])
v.check("08-07.10d", c54[2])
v.assert_true("(x^2+x+1)(x^3+x+1) = x^5+x^4+1", clmul(0b111, 0b1011) == poly(5, 4))
# P11: 5-bit m-sequence statistics
b5 = lfsr_bits(5, 3, 31)
r5 = runs(b5)
v.check("08-07.11a", sum(b5))
v.check("08-07.11b", 31 - sum(b5))
v.check("08-07.11c", len(r5))
v.check("08-07.11d", sum(1 for _, ln in r5 if ln == 1))
v.check("08-07.11e", max(ln for b, ln in r5 if b == 1))
agree = {sum(b5[i] == b5[(i + s) % 31] for i in range(31)) for s in range(1, 31)}
v.assert_true("agreements identical for every nonzero shift", len(agree) == 1)
v.check("08-07.11f", agree.pop())
# P12: rule of three
nbits = 25.78125e9 * 600
v.check("08-07.12a", nbits)
v.check("08-07.12b", 3 / nbits)
v.check("08-07.12c", 3 / 1e-15 / 25.78125e9 / 3600)
# P13: CRC register for generator x^3 + x + 1
reg, clocks = 0, 0
for b in (1, 1, 0, 1, 0, 0, 0):
    top = (reg >> 2) & 1
    reg = ((reg << 1) | b) & 0b111
    if top:
        reg ^= 0b011
    clocks += 1
v.assert_true("CRC register agrees with long division", reg == pmod(0b1101000, 0b1011))
v.check("08-07.13a", clocks)
v.check("08-07.13b", reg)
# P14: toggles per count, 16 bits, simulated over a full cycle
M = 2 ** 16
cnt = np.arange(M, dtype=np.int64)
nxt = (cnt + 1) % M
bin_tog = np.unpackbits((cnt ^ nxt).astype(">u2").view(np.uint8)).sum() / M
gray_tog = np.unpackbits(((cnt ^ (cnt >> 1)) ^ (nxt ^ (nxt >> 1))).astype(">u2").view(np.uint8)).sum() / M
v.check("08-07.14a", bin_tog)
v.assert_true("Gray counter toggles exactly 1 per count", gray_tog == 1.0)
v.check("08-07.14b", bin_tog * 5e-15 * 100e6 * 1e6)
v.check("08-07.14c", gray_tog * 5e-15 * 100e6 * 1e6)
# P15
v.check("08-07.15a", 36 + 24)
v.check("08-07.15b", 32 * (36 + 24))
v.check("08-07.15c", 100 * 36 / (36 + 24))


# ================================================================= lab
def toggles_per_step(seq):
    return sum(bin(a ^ b).count("1") for a, b in zip(seq, seq[1:] + seq[:1])) / len(seq)


v.check("Lab 08-07.a", toggles_per_step(list(range(16))))
v.check("Lab 08-07.b", toggles_per_step([g ^ (g >> 1) for g in range(16)]))
v.check("Lab 08-07.c", toggles_per_step(ring))
v.check("Lab 08-07.d", toggles_per_step(john))
tested = maximal = 0
for n in range(4, 9):
    for k in range(1, n):
        is_max = lfsr_cycles(n, k) == [2 ** n - 1]
        v.assert_true(f"stepping agrees with primitivity for n={n}, k={k}", is_max == is_primitive(n, k))
        tested += 1
        maximal += is_max
v.check("Lab 08-07.e", tested)
v.check("Lab 08-07.f", maximal)


def is_irreducible(p):
    n, x = p.bit_length() - 1, 2
    return ppowmod(x, 2 ** n, p) == x and all(pgcd(ppowmod(x, 2 ** (n // q), p) ^ x, p) == 1
                                              for q in prime_factors(n))


v.check("Lab 08-07.g", sum(is_irreducible(poly(8, k)) for k in range(1, 8)))
# brute-force cross-check: no trinomial of degree 8 is irreducible (trial division by all lower-degree polys)
v.assert_true("degree-8 trinomials all have a factor of degree 1 to 4",
              all(any(pmod(poly(8, k), d) == 0 for d in range(2, 32)) for k in range(1, 8)))
s, per = 1, 0
while True:
    fb = ((s >> 7) ^ (s >> 5) ^ (s >> 4) ^ (s >> 3)) & 1   # taps Q8, Q6, Q5, Q4
    s = ((s << 1) | fb) & 0xFF
    per += 1
    if s == 1:
        break
v.check("Lab 08-07.h", per)
b7 = lfsr_bits(7, 6, 127)
v.check("Lab 08-07.i", lfsr_cycles(7, 6)[0])
v.check("Lab 08-07.j", sum(b7))
v.check("Lab 08-07.k", len(runs(b7)))
pm = np.array(b7) * 2 - 1
acf = [float(np.dot(pm, np.roll(pm, sh))) / 127 for sh in range(1, 127)]
v.assert_true("PRBS7 autocorrelation constant at nonzero shifts", max(acf) - min(acf) < 1e-12)
v.check("Lab 08-07.l", acf[0])
b15 = lfsr_bits(15, 14, 32767)
v.check("Lab 08-07.m", len(set(orbit(lambda st: lfsr_step(st, 15, 14), 1))))
v.check("Lab 08-07.n", sum(b15))
trans, worst = 0, 0.0
for c in range(16):
    tr = ripple_events(c, 4, 2.0)
    v.assert_true(f"ripple {c} ends at {c + 1}", tr[-1][1] == (c + 1) % 16)
    trans += len(tr) - 1
    worst = max(worst, tr[-1][0])
v.check("Lab 08-07.o", trans)
v.check("Lab 08-07.p", worst)

v.finish()
