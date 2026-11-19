#!/usr/bin/env python3
"""Verify every number in the Course 08 final-exam solutions.

Each value is recomputed independently of the hand method in the solutions, by brute force where possible:
- Number formats by bit-level arithmetic: a simulated ripple adder for the sums and flags, exact
  fractions for fixed point, and a Hamming syndrome computed from the parity-check rules.
- Boolean functions from full truth tables. Prime implicants, minimal covers and hazards come from an
  exhaustive search over all cubes and covers, and minimal POS forms by minimizing the complement.
- Adder and multiplexer delays from an arrival-time simulation of gate-level netlists, the prefix
  networks built and tested on random additions, and the Dadda counts by running Dadda's reduction.
- Latch, flip-flop, counter, LFSR and FSM behavior by cycle simulation. The detector's state counts come
  from building the pattern automaton and minimizing it by partition refinement, its equations from
  exhaustive minimization of the encoded table.
- Timing, memory, FPGA, energy and MTBF answers from the formulas, with the skew optimum found by
  scanning and the FIFO occupancy checked by a discrete-time simulation.
The Verilog answers (Questions 5 and 8) are also checked under Icarus Verilog by exam/exam_tb.v.
"""
from __future__ import annotations

import itertools
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("08-exam", HERE.parent / "exam" / "solutions.md")
rng = random.Random(8)
YEAR = 365.25 * 86400


def signed(x, n):
    x &= (1 << n) - 1
    return x - (1 << n) if x >> (n - 1) else x


def ripple_add(a, b, cin, n):
    """Bit-level ripple adder: returns (sum, list of carries C_0..C_n)."""
    c, s, carries = cin, 0, [cin]
    for i in range(n):
        x, y = (a >> i) & 1, (b >> i) & 1
        s |= (x ^ y ^ c) << i
        c = (x & y) | (c & (x ^ y))
        carries.append(c)
    return s, carries


# ================================================================= Q1 numbers and codes
v.check("X08.1a", int("B6", 16))
v.check("X08.1b", signed(int("B6", 16), 8))
s, cy = ripple_add(0x5A, 0x3C, 0, 8)
v.check("X08.1c", s)
v.check("X08.1d", signed(s, 8))
v.assert_true("5A + 3C overflows: V = C8 xor C7 = 1, with C8 = 0 and C7 = 1",
              cy[8] ^ cy[7] == 1 and cy[8] == 0 and cy[7] == 1 and s == 0x96)
q = Fraction(-40625, 100000) * 2 ** 7
v.assert_true("-0.40625 is exactly representable in Q1.7", q.denominator == 1)
v.check("X08.1e", int(q))
v.check("X08.1f", int(q) & 0xFF)
v.assert_true("CC hex is 1100 1100", int(q) & 0xFF == 0xCC)
v.check("X08.1g", float(Fraction(1, 2 ** 7)))
v.check("X08.1h", float(1 - Fraction(1, 2 ** 7)))
recv = [int(ch) for ch in "1100010"]                 # positions 1..7


def syndrome(word):
    return sum(p for p in (1, 2, 4) if sum(word[i - 1] for i in range(1, 8) if i & p) % 2)


syn = syndrome(recv)
v.check("X08.1i", syn)
fixed = recv[:]
fixed[syn - 1] ^= 1
v.assert_true("the corrected word has zero syndrome", syndrome(fixed) == 0)
v.check("X08.1j", int("".join(map(str, fixed)), 2))
data = [fixed[i - 1] for i in (3, 5, 6, 7)]
v.check("X08.1k", int("".join(map(str, data)), 2))
v.assert_true("re-encoding the data gives the corrected word", all(
    fixed[p - 1] == sum(fixed[i - 1] for i in range(1, 8) if i & p and i != p) % 2 for p in (1, 2, 4)))

# ================================================================= Q2 Boolean algebra
rows3 = list(itertools.product((0, 1), repeat=3))
v.assert_true("AB + A'C + BC = AB + A'C, and (A+B)(A+C) = A + BC, on all rows",
              all(((a & b) | ((1 - a) & c) | (b & c)) == ((a & b) | ((1 - a) & c)) for a, b, c in rows3)
              and all(((a | b) & (a | c)) == (a | (b & c)) for a, b, c in rows3))
v.assert_true("complement of A + B'C is A'(B + C')",
              all(1 - (a | ((1 - b) & c)) == ((1 - a) & (b | (1 - c))) for a, b, c in rows3))
v.assert_true("NAND-NAND and AOI22 + inverter both equal AB + CD", all(
    (1 - ((1 - (a & b)) & (1 - (c & d)))) == ((a & b) | (c & d)) == (1 - (1 - ((a & b) | (c & d))))
    for a, b, c, d in itertools.product((0, 1), repeat=4)))
T_NAND = lambda k: 2 * k      # noqa: E731  static CMOS counts of the exam's conventions
T_INV = 2
v.check("X08.2a", 3 * (T_NAND(2) + T_INV))
v.check("X08.2b", 3 * T_NAND(2))
v.check("X08.2c", T_NAND(4) + T_INV)
v.check("X08.2d", sum(((a ^ b ^ c) << (4 * a + 2 * b + c)) for a, b, c in rows3))
v.check("X08.2e", sum(((a + b + c >= 2) << (4 * a + 2 * b + c)) for a, b, c in rows3))


# ================================================================= Q3 minimization (exhaustive)
def covers(cube, m, n):
    return all(val is None or val == (m >> (n - 1 - i)) & 1 for i, val in enumerate(cube))


def cube_minterms(cube, n):
    return frozenset(m for m in range(2 ** n) if covers(cube, m, n))


def primes_of(on, dc, n=4):
    allowed = set(on) | set(dc)
    imps = [c for c in itertools.product((0, 1, None), repeat=n)
            if cube_minterms(c, n) <= allowed and cube_minterms(c, n) & set(on)]
    return [c for c in imps if not any(d != c and cube_minterms(c, n) < cube_minterms(d, n) for d in imps)]


def literals(cubes):
    return sum(sum(x is not None for x in c) for c in cubes)


def minimal_covers(on, dc, n=4):
    P = primes_of(on, dc, n)
    for k in range(1, len(P) + 1):
        sols = [combo for combo in itertools.combinations(P, k)
                if all(any(covers(c, m, n) for c in combo) for m in on)]
        if sols:
            best = min(map(literals, sols))
            return P, [s_ for s_ in sols if literals(s_) == best]
    return P, []


ON3 = [1, 5, 6, 7, 11, 12, 13, 15]
OFF3 = [m for m in range(16) if m not in ON3]
P3, sop = minimal_covers(ON3, [])
ess = [p for p in P3 if any(covers(p, m, 4) and sum(covers(q_, m, 4) for q_ in P3) == 1 for m in ON3)]
BD = (None, 1, None, 1)
v.check("X08.3a", len(P3))
v.check("X08.3b", len(ess))
v.assert_true("the minimal SOP is unique and is the four essential primes, without BD",
              len(sop) == 1 and set(sop[0]) == set(ess) and BD in P3 and BD not in sop[0])
v.check("X08.3c", len(sop[0]))
v.check("X08.3d", literals(sop[0]))
_, pos = minimal_covers(OFF3, [])
v.assert_true("the minimal POS is unique with 4 sum terms", len(pos) == 1 and len(pos[0]) == 4)
v.check("X08.3e", literals(pos[0]))
hazards = []
for m in ON3:
    for bit in range(4):
        m2 = m ^ (1 << bit)
        if m < m2 and m2 in ON3 and not any(covers(c, m, 4) and covers(c, m2, 4) for c in sop[0]):
            hazards.append((m, m2))
v.assert_true("the hazardous pairs are 5-7, 5-13, 7-15 and 13-15, all inside BD",
              sorted(hazards) == [(5, 7), (5, 13), (7, 15), (13, 15)]
              and all(covers(BD, a, 4) and covers(BD, b, 4) for a, b in hazards))
v.check("X08.3f", len(hazards))
v.check("X08.3g", literals(sop[0]) + literals([BD]))
_, sop_dc = minimal_covers(ON3, [3, 9])
v.assert_true("with don't cares 3 and 9 the minimal SOP is unique: D + A'BC + ABC'",
              len(sop_dc) == 1 and set(sop_dc[0]) == {(None, None, None, 1), (0, 1, 1, None), (1, 1, 0, None)})
v.check("X08.3h", len(sop_dc[0]))
v.check("X08.3i", literals(sop_dc[0]))

# ================================================================= Q4 combinational blocks
G = {1, 2, 6, 7}
mux_data = {0: lambda c: c, 1: lambda c: 1 - c, 2: lambda c: 0, 3: lambda c: 1}
v.assert_true("4:1 mux with data C, C', 0, 1 implements G; decoder outputs 1, 2, 6, 7 too",
              all(mux_data[2 * a + b](c) == (4 * a + 2 * b + c in G) for a, b, c in rows3))
for key, a, b in (("X08.4a", 0b0101, 0b0111), ("X08.4b", 0b0110, 0b1101)):
    r, cy = ripple_add(a, (~b) & 0xF, 1, 4)
    v.check(key, signed(r, 4))
    want_v = not (-8 <= signed(a, 4) - signed(b, 4) <= 7)
    v.assert_true(f"{key}: V = C4 xor C3 flags overflow exactly when the true difference is out of range",
                  (cy[4] ^ cy[3]) == want_v and cy[4] == 0)


def rca_arrival(n):
    """Gate-level arrival times (unit delay) of a ripple adder: S = A^B^C, Cout = AB + C(A^B)."""
    c, t_sum = 0.0, []
    t_c = 0                                   # carry-in available at 0
    for _ in range(n):
        t_x = 1                               # A xor B
        t_and1 = 1                            # A and B
        t_and2 = max(t_x, t_c) + 1            # C and (A xor B)
        t_sum.append(max(t_x, t_c) + 1)       # second XOR
        t_c = max(t_and1, t_and2) + 1         # OR
    return max(t_sum), t_c


ts16, tc16 = rca_arrival(16)
v.check("X08.4c", ts16)
v.check("X08.4d", tc16)
v.check("X08.4e", ts16 * 20)
v.check("X08.4f", tc16 * 20)


# ================================================================= Q5 Verilog semantics (emulated)
a5, b5, s5 = 9, 12, signed(0b1010, 4)
v.check("X08.5a", (a5 + b5) & 0xF)
v.check("X08.5b", (a5 + b5) & 0xFF)
v.check("X08.5c", (a5 << 4) | b5)
v.check("X08.5d", signed(s5 & 0xFF, 8))
v.check("X08.5e", signed(((s5 & 0xF) + a5) & 0xFF, 8))        # unsigned context: s zero-extended
v.check("X08.5f", signed((s5 & 0xFF) >> 1 | 0x80, 8))         # arithmetic shift of the sign-extended s
x_, y_, u_, w_ = 1, 0, 1, 0
for _ in range(2):
    x_, y_ = y_, x_                                            # nonblocking: both sides read first
    u_ = w_
    w_ = u_                                                    # blocking: in order
v.assert_true("after two edges x, y = 1, 0 and u, v = 0, 0", (x_, y_, u_, w_) == (1, 0, 0, 0))
combos = 2 ** (16 + 16 + 1)
v.check("X08.5g", combos)
v.check("X08.5h", combos / 1e6)
v.check("X08.5i", combos / 1e6 / 3600)
v.check("X08.5j", 2 ** 65 / 1e6 / YEAR)

# ================================================================= Q6 latch, flip-flop, timing
CLK = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
D6 = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
ql, qf, lat, ff, prev = 0, 0, [], [], 0
for c_, d_ in zip(CLK, D6):
    if c_:
        ql = d_
    if c_ and not prev:
        qf = d_
    prev = c_
    lat.append(ql)
    ff.append(qf)
v.assert_true("latch and flip-flop outputs as published",
              lat == [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1] and ff == [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
changes = lambda seq: sum(1 for i in range(len(seq)) if seq[i] != (seq[i - 1] if i else 0))  # noqa: E731
v.check("X08.6a", changes(lat))
v.check("X08.6b", changes(ff))
tpcq, tccq, tsu, th, tpd, tcd = 70, 45, 55, 60, 615, 5
v.check("X08.6c", tpcq + tpd + tsu)
v.check("X08.6d", 1000 / (tpcq + tpd + tsu))
v.check("X08.6e", tccq + tcd - th)
nbuf = next(k for k in range(10) if tccq + tcd + 8 * k - th >= 0)
v.check("X08.6f", nbuf)
v.check("X08.6g", tccq + tcd + 8 * nbuf - th)
t3 = tpcq + tpd / 3 + tsu
v.check("X08.6h", t3)
v.check("X08.6i", 1000 / t3)
v.check("X08.6j", (tpcq + tpd + tsu) / t3)
v.check("X08.6k", 3 * t3)

# ================================================================= Q7 counters and LFSRs
st, seen = (0, 0, 0, 0), []
while st not in seen:
    seen.append(st)
    st = (1 - st[3],) + st[:3]                      # shift right, complement feedback
v.assert_true("Johnson sequence from 0000 as published", ["".join(map(str, s_)) for s_ in seen] ==
              ["0000", "1000", "1100", "1110", "1111", "0111", "0011", "0001"])
v.check("X08.7a", len(seen))
v.check("X08.7b", 16 - len(seen))
st, states, out = (1, 0, 0, 0), [], []
while st not in states:
    states.append(st)
    out.append(st[3])
    st = (st[3] ^ st[2],) + st[:3]
v.check("X08.7c", len(states))
v.check("X08.7d", int("".join(map(str, out[:15])), 2))
v.check("X08.7e", sum(out))


v.check("X08.7f", 2 ** 8)
v.check("X08.7g", 8)
v.check("X08.7h", 2 * 8)
s_, k8 = 1, 0
while True:                                         # Fibonacci form of x^8 + x^6 + x^5 + x^4 + 1
    bit = ((s_ >> 7) ^ (s_ >> 5) ^ (s_ >> 4) ^ (s_ >> 3)) & 1
    s_ = ((s_ << 1) | bit) & 0xFF
    k8 += 1
    if s_ == 1:
        break
v.assert_true("x^8 + x^6 + x^5 + x^4 + 1 gives a period-255 LFSR", k8 == 255)
v.check("X08.7i", k8)
cnt, trans = [1, 1, 1, 0], []                       # bits Q0..Q3 of 0111 (Q0 first)
i = 0
while True:                                         # ripple: each falling output toggles the next stage
    cnt[i] ^= 1
    trans.append(int("".join(map(str, cnt[::-1])), 2))
    if cnt[i] == 1 or i == 3:
        break
    i += 1
v.assert_true("the ripple counter passes through 6, 4, 0 to reach 8", trans == [6, 4, 0, 8])

# ================================================================= Q8 sequence detector
PAT = [1, 1, 0, 1]


def next_prefix_full(k, x):
    s_ = PAT[:k] + [x]
    for L in range(min(len(s_), 4), -1, -1):
        if s_[len(s_) - L:] == PAT[:L]:
            return L
    return 0


moore = {k: {x: next_prefix_full(k, x) for x in (0, 1)} for k in range(5)}


def minimize_states(states, delta, out):
    """Partition refinement; out(state) or out(state, x) for Mealy."""
    part = {s_: out(s_) for s_ in states}
    while True:
        sig = {s_: (part[s_],) + tuple(part[delta(s_, x)] for x in (0, 1)) for s_ in states}
        new = {s_: sorted(set(sig.values())).index(sig[s_]) for s_ in states}
        if len(set(new.values())) == len(set(part.values())):
            return len(set(new.values()))
        part = new


n_moore = minimize_states(range(5), lambda s_, x: moore[s_][x], lambda s_: int(s_ == 4))
FAIL4 = max(L for L in range(4) if PAT[4 - L:] == PAT[:L])     # longest proper suffix that is a prefix
v.assert_true("after 1101 the Mealy machine keeps the suffix '1'", FAIL4 == 1)
mealy_t = {k: {x: (next_prefix_full(k, x) if next_prefix_full(k, x) < 4 else FAIL4) for x in (0, 1)}
           for k in range(4)}
n_mealy = minimize_states(range(4), lambda s_, x: mealy_t[s_][x],
                          lambda s_: tuple(int(s_ == 3 and x == 1) for x in (0, 1)))
v.check("X08.8a", n_moore)
v.check("X08.8b", n_mealy)
CODE = {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}           # A, B, C, D as q1q0
DEC = {cd: k for k, cd in CODE.items()}
f_q1, f_q0, f_z = [], [], []
for q1, q0, x in itertools.product((0, 1), repeat=3):
    k = DEC[(q1, q0)]
    nq1, nq0 = CODE[mealy_t[k][x]]
    idx = 4 * q1 + 2 * q0 + x
    (f_q1 if nq1 else []).append(idx)
    (f_q0 if nq0 else []).append(idx)
    (f_z if (k == 3 and x == 1) else []).append(idx)
lit8 = 0
for f in (f_q1, f_q0, f_z):
    _, sols = minimal_covers(f, [], 3)
    lit8 += literals(sols[0])
v.assert_true("q0+ = x, q1+ = q0 x + q1 q0, z = q1 q0' x",
              minimal_covers(f_q0, [], 3)[1][0] == ((None, None, 1),)
              and set(minimal_covers(f_q1, [], 3)[1][0]) == {(None, 1, 1), (1, 1, None)}
              and minimal_covers(f_z, [], 3)[1][0] == ((1, 0, 1),))
v.check("X08.8c", lit8)
XS = [1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
k, mealy_hits = 0, []
for t, x in enumerate(XS):
    if k == 3 and x == 1:
        mealy_hits.append(t)
    k = mealy_t[k][x]
k, moore_hits = 0, []
for t, x in enumerate(XS + [0]):
    if k == 4:
        moore_hits.append(t)
    k = moore[k][x]
v.assert_true("Mealy detects in cycles 3, 6, 11 and Moore in 4, 7, 12",
              mealy_hits == [3, 6, 11] and moore_hits == [4, 7, 12])
v.check("X08.8d", len(mealy_hits))
v.check("X08.8e", moore_hits[0])
v.check("X08.8f", math.ceil(math.log2(n_moore)))
v.check("X08.8g", n_moore)
v.check("X08.8h", math.ceil(math.log2(n_mealy)))
v.check("X08.8i", n_mealy)


# ================================================================= Q9 arithmetic
def prefix_net(kind, n):
    lv, d = [], 1
    if kind == "BK":
        while d < n:
            lv.append([(i, i - d) for i in range(2 * d - 1, n, 2 * d)])
            d *= 2
        d //= 4
        while d >= 1:
            row = [(i, i - d) for i in range(3 * d - 1, n, 2 * d)]
            if row:
                lv.append(row)
            d //= 2
        return lv
    while d < n:
        if kind == "KS":
            lv.append([(i, i - d) for i in range(d, n)])
        else:  # Sklansky
            lv.append([(i, (i // d) * d - 1) for i in range(n) if (i // d) % 2])
        d *= 2
    return lv


def prefix_add(levels, n, a, b, cin):
    """Gate-level evaluation with arrival times: G = g_hi + p_hi g_lo (AND then OR), P = p_hi p_lo."""
    A = [(a >> i) & 1 for i in range(n)]
    B = [(b >> i) & 1 for i in range(n)]
    p = [x ^ y for x, y in zip(A, B)]
    g = [x & y for x, y in zip(A, B)]
    tg, tp = [1] * n, [1] * n
    g[0] = g[0] | (p[0] & cin)
    tg[0] = 3                                   # AND then OR after the bit-0 propagate
    P0 = p[:]
    span = list(range(n))
    for row in levels:
        G2, P2, TG2, TP2, S2 = g[:], p[:], tg[:], tp[:], span[:]
        for i, j in row:
            assert span[i] == j + 1
            t_and = max(tp[i], tg[j]) + 1
            G2[i] = g[i] | (p[i] & g[j])
            TG2[i] = max(tg[i], t_and) + 1
            P2[i] = p[i] & p[j]
            TP2[i] = max(tp[i], tp[j]) + 1
            S2[i] = span[j]
        g, p, tg, tp, span = G2, P2, TG2, TP2, S2
    s_ = sum((P0[i] ^ (g[i - 1] if i else cin)) << i for i in range(n)) | (g[n - 1] << n)
    t_sum = max(max(1, tg[i - 1] if i else 0) + 1 for i in range(n))
    return s_, t_sum


n9 = 64
ripple_levels = [[(i, i - 1)] for i in range(1, n9)]
delay = {}
for kind, lv in (("ripple", ripple_levels), ("KS", prefix_net("KS", n9)), ("Sk", prefix_net("Sk", n9)),
                 ("BK", prefix_net("BK", n9))):
    for _ in range(300):
        a, b, c = rng.getrandbits(n9), rng.getrandbits(n9), rng.getrandbits(1)
        assert prefix_add(lv, n9, a, b, c)[0] == a + b + c
    delay[kind] = (prefix_add(lv, n9, 0, 0, 0)[1], sum(map(len, lv)), len(lv))
v.assert_true("all 64-bit networks add correctly on random inputs", True)
v.assert_true("the simulated delays are 14, 16 and 24 units, as the question states",
              (delay["KS"][0], delay["Sk"][0], delay["BK"][0]) == (14, 16, 24))
v.check("X08.9a", delay["ripple"][0])
v.check("X08.9b", delay["KS"][1])
v.check("X08.9c", delay["Sk"][1])
v.check("X08.9d", delay["BK"][1])
v.assert_true("Kogge-Stone and Sklansky have the same number of levels", delay["KS"][2] == delay["Sk"][2])
v.check("X08.9e", delay["KS"][2])
v.check("X08.9f", delay["BK"][2])
v.check("X08.9g", delay["ripple"][0] / delay["KS"][0])
v.check("X08.9h", delay["ripple"][0] / delay["Sk"][0])
v.check("X08.9i", delay["ripple"][0] / delay["BK"][0])
v.assert_true("Sklansky's last level has fan-out 32", max(
    sum(1 for i, j in prefix_net("Sk", 64)[-1] if j == k_) for k_ in range(64)) == 32)


def dadda_counts(n):
    heights = [min(i + 1, 2 * n - 1 - i) for i in range(2 * n - 1)] + [0]
    targets = [2]
    while targets[-1] < n:
        targets.append(targets[-1] * 3 // 2)
    fa = ha = 0
    for d in reversed(targets[:-1]):
        carry_in = 0
        new = heights[:]
        for col in range(len(heights)):
            h = heights[col] + carry_in
            carry_in = 0
            while h > d:
                if h == d + 1:
                    ha += 1
                    h -= 1
                else:
                    fa += 1
                    h -= 2
                carry_in += 1
            new[col] = h
        heights = new
    width = sum(1 for h in heights if h == 2)
    return fa, ha, heights


fa8, ha8, _ = dadda_counts(8)
fa16, ha16, h16 = dadda_counts(16)
v.assert_true("Dadda 8 x 8 gives 35 full and 7 half adders (08-09 Example 5)", (fa8, ha8) == (35, 7))
v.check("X08.9j", fa16)
v.check("X08.9k", ha16)
v.check("X08.9l", len([h for h in h16 if h > 0]) - 1)
qa, qb = int(0.75 * 2 ** 15), int(-0.5 * 2 ** 15)
v.check("X08.9m", qa)
v.check("X08.9n", qb)
v.check("X08.9o", qa * qb)
v.check("X08.9p", (qa * qb) >> 15)
v.assert_true("the result is -0.375 exactly", Fraction((qa * qb) >> 15, 2 ** 15) == Fraction(-3, 8))
v.assert_true("(-1)(-1) overflows Q1.15 and only it does",
              ((-32768) ** 2 >> 15) == 32768 and (-32768 * -32767) >> 15 <= 32767)
worst = 64 * (-32768) ** 2
need = next(k for k in range(32, 64) if worst <= 2 ** (k - 1) - 1)
v.assert_true("64 worst-case products need 38 signed bits", need == 38 == 32 + 6)
v.check("X08.9q", need)
v.check("X08.9r", 32 * int(math.log2(32)))
v.check("X08.9s", int(math.log2(32)))

# ================================================================= Q10 skew and jitter
pcq, su, ccq, hold, pd12, cd12, pd23 = 50, 40, 30, 35, 560, 30, 520


def periods(delta, jitter=0):
    return (pcq + pd12 + su - delta + jitter, pcq + pd23 + su + delta + jitter)


v.check("X08.10a", max(periods(0)))
v.check("X08.10b", 1000 / max(periods(0)))
v.check("X08.10c", ccq + cd12 - hold)
p1, p2 = periods(60)
v.check("X08.10d", p1)
v.check("X08.10e", p2)
v.check("X08.10f", 1000 / max(p1, p2))
v.check("X08.10g", ccq + cd12 - hold - 60)
best = min(range(0, 101), key=lambda d: max(periods(d)))
v.check("X08.10h", best)
v.check("X08.10i", max(periods(best)))
v.check("X08.10j", 1000 / max(periods(best)))
v.check("X08.10k", ccq + cd12 - hold - best)
v.check("X08.10l", max(periods(best, 25)))
v.check("X08.10m", 1000 / max(periods(best, 25)))

# ================================================================= Q11 memories and LUTs
bits = 128 * 1024 * 32
side = math.isqrt(bits)
v.assert_true("the array is exactly square", side * side == bits)
v.check("X08.11a", bits)
v.check("X08.11b", int(math.log2(128 * 1024)))
v.check("X08.11c", side)
v.check("X08.11d", side // 32)
v.check("X08.11e", int(math.log2(side)))
v.check("X08.11f", int(math.log2(side // 32)))
v.check("X08.11g", 2 ** 8 * 8)
v.check("X08.11h", 2 ** 16 * 16)


def and_tree(n, k):
    luts = levels = 0
    while n > 1:
        m = math.ceil(n / k)
        luts += m
        levels += 1
        n = m
    return luts, levels


v.check("X08.11i", and_tree(12, 4)[0])
v.check("X08.11j", and_tree(12, 6)[0])
v.assert_true("both trees have 2 levels", and_tree(12, 4)[1] == and_tree(12, 6)[1] == 2)
v.check("X08.11k", and_tree(12, 4)[1])
v.check("X08.11l", 4 * 64 * (32 - 1))

# ================================================================= Q12 FPGA report
v.check("X08.12a", 100 * 1584 / 5280)
v.check("X08.12b", 100 * 6 / 30)
v.check("X08.12c", 100 * 2 / 8)
v.check("X08.12d", 100 * 21 / 39)
seg = dict(cq=1.39, logic=8.62, route=13.47, setup=0.82)
tot = sum(seg.values())
v.check("X08.12e", tot)
v.check("X08.12f", 1000 / tot)
v.check("X08.12g", 1000 / 48 - tot)
v.check("X08.12h", 100 * seg["route"] / tot)
v.check("X08.12i", 1.03 * 1000 / tot)
v.assert_true("a 3% gain does not reach 48 MHz", 1.03 * 1000 / tot < 48)
t_pipe = (seg["logic"] + seg["route"]) / 2 + seg["cq"] + seg["setup"]
v.check("X08.12j", 1000 / t_pipe)
v.check("X08.12k", 1000 / 48 - t_pipe)

# ================================================================= Q13 MAC unit
prods = [x * y for x in range(-128, 128) for y in range(-128, 128)]
pmax, pmin = max(prods), min(prods)
v.assert_true("products span -16256 to +16384 and need 16 signed bits",
              (pmin, pmax) == (-16256, 16384) and -2 ** 15 <= pmin and pmax <= 2 ** 15 - 1 and pmax > 2 ** 14 - 1)
v.check("X08.13a", 16)
v.check("X08.13b", 256 * pmax)
v.check("X08.13c", 256 * pmin)
acc = next(k for k in range(16, 40) if -2 ** (k - 1) <= 256 * pmin and 256 * pmax <= 2 ** (k - 1) - 1)
v.check("X08.13d", acc)
E_MUL8, E_ADD32, E_SRAM, E_DRAM = 0.2, 0.1, 20.0, 1300.0      # pJ, Horowitz ISSCC 2014 (R-157)
macs, rate = 2.5e6, 10
e_mac = E_MUL8 + E_ADD32
v.check("X08.13e", e_mac)
v.check("X08.13f", macs * e_mac * 1e-12 * 1e6)
v.check("X08.13g", macs * e_mac * 1e-12 * rate * 1e6)
v.check("X08.13h", E_SRAM / 8)
v.check("X08.13i", macs * E_SRAM / 8 * 1e-12 * 1e6)
v.check("X08.13j", macs * E_SRAM / 8 * 1e-12 * rate * 1e6)
v.check("X08.13k", (E_SRAM / 8) / e_mac)
v.check("X08.13l", E_DRAM / 8)
v.check("X08.13m", macs * E_DRAM / 8 * 1e-12 * 1e6)
v.check("X08.13n", macs * E_DRAM / 8 * 1e-12 * rate * 1e3)
v.check("X08.13o", (E_DRAM / 8) / e_mac)
v.check("X08.13p", 1000 / (1.1 + 0.6 + 0.1))
v.check("X08.13q", 1000 / (max(1.1, 0.6) + 0.1))
v.check("X08.13r", macs * rate / 1e6)

# ================================================================= Q14 clock-domain crossing
gray = lambda b: b ^ (b >> 1)  # noqa: E731
v.check("X08.14a", bin(7 ^ 8).count("1"))
v.check("X08.14b", bin(gray(7) ^ gray(8)).count("1"))
v.check("X08.14c", gray(7))
v.check("X08.14d", gray(8))
v.assert_true("successive Gray codes differ in one bit, including the wrap of a 128-entry 8-bit pointer",
              all(bin(gray(i) ^ gray((i + 1) % 256)).count("1") == 1 for i in range(256)))
f_w, f_r, burst, lag = 100e6, 75e6, 256, 3
t_burst = burst / f_w
v.check("X08.14e", t_burst * 1e6)
reads = (t_burst - lag / f_r) * f_r
v.check("X08.14f", reads)
v.check("X08.14g", burst - reads)
# discrete check: writes at k/f_w, reads at each read edge from lag/f_r on (if data present)
events = sorted([(k / f_w, 0) for k in range(burst)] + [(lag / f_r + j / f_r, 1) for j in range(400)])
occ = peak = 0
for _, kind in events:
    if kind == 0:
        occ += 1
    elif occ:
        occ -= 1
    peak = max(peak, occ)
v.assert_true(f"discrete simulation peak occupancy ({peak}) agrees with the fluid estimate within 2",
              abs(peak - (burst - reads)) <= 2)
depth = 2 ** math.ceil(math.log2(burst - reads))
v.check("X08.14h", depth)
v.check("X08.14i", burst / f_r * 1e6)
v.check("X08.14j", int(math.log2(depth)) + 1)
v.check("X08.14k", 2 * (int(math.log2(depth)) + 1) * 2)
tau, tw, fc, fd = 25e-12, 20e-12, 1.25e9, 1e8
S1 = 1 / fc - 50e-12 - 30e-12
m2 = math.exp(2 * S1 / tau / 2) / (tw * fc * fd)            # two stages: S = S1
m3 = math.exp(2 * S1 / tau) / (tw * fc * fd)                # three stages: S = 2 S1
v.check("X08.14l", m2)
v.check("X08.14m", m2 / 86400)
v.check("X08.14n", m3)
v.check("X08.14o", m3 / YEAR)
S75 = 1 / 75e6 - 80e-12
v.assert_true("at 75 MHz two stages give an exponent above 500 (astronomically safe)", S75 / tau > 500)

v.finish()
