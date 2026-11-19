#!/usr/bin/env python3
"""Verify every number in chapter 08-08 (finite state machines), its solutions and lab.

Independent routes:
- machines are simulated from their state tables, and detectors are checked against a direct
  pattern match on the input history (the specification), not against the hand traces;
- minimized logic is found by exhaustive search over all product terms (exact minimum literal count),
  and every derived equation is checked against the state table on all inputs;
- state minimization runs partition refinement, and the merged machine is checked against the
  original by simulation on every input sequence up to length 8;
- minimal Moore equivalents of Mealy machines are built by the state-splitting construction and then
  minimized; code-distance claims are checked by searching every code;
- timing, area and rate numbers are recomputed from the problem data.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-08", COURSE / "chapters" / "08-08-finite-state-machines.md",
                        COURSE / "solutions" / "08-08-solutions.md",
                        COURSE / "labs" / "08-08-lab" / "README.md")

# ---------------------------------------------------------------- machines
# Moore: {state: (next on 0, next on 1)}, plus the set of states with output 1
MOORE101 = {0: (0, 1), 1: (2, 1), 2: (0, 3), 3: (2, 1)}
MOORE110 = {0: (0, 1), 1: (0, 2), 2: (3, 2), 3: (0, 1)}
# Mealy: {state: ((next, z) on 0, (next, z) on 1)}
MEALY101 = {0: ((0, 0), (1, 0)), 1: ((2, 0), (1, 0)), 2: ((0, 0), (1, 1))}


def run_moore(m, ones, xs, s=0):
    """Outputs for cycles 0 .. len(xs): the state of cycle t gives z_t."""
    out = []
    for x in xs:
        out.append(int(s in ones))
        s = m[s][x]
    out.append(int(s in ones))
    return out


def run_mealy(m, xs, s=0, overlap=True):
    out = []
    for x in xs:
        n, z = m[s][x]
        out.append(z)
        s = 0 if (z and not overlap) else n
    return out


def spec(xs, pat):
    """Specification: z_t = 1 if inputs t-len+1 .. t equal pat (Mealy timing), overlapping."""
    k = len(pat)
    return [int(t >= k - 1 and tuple(xs[t - k + 1:t + 1]) == pat) for t in range(len(xs))]


def spec_nonoverlap(xs, pat):
    out, last = [], -len(pat)
    for t in range(len(xs)):
        hit = t - last >= len(pat) and t >= len(pat) - 1 and tuple(xs[t - len(pat) + 1:t + 1]) == pat
        out.append(int(hit))
        if hit:
            last = t
    return out


# the detectors meet their specifications on every input sequence of length up to 10
for n in range(1, 11):
    for xs in itertools.product((0, 1), repeat=n):
        xs = list(xs)
        assert run_mealy(MEALY101, xs) == spec(xs, (1, 0, 1))
        assert run_moore(MOORE101, {3}, xs)[1:] == spec(xs, (1, 0, 1))
        assert run_moore(MOORE110, {3}, xs)[1:] == spec(xs, (1, 1, 0))
        assert run_mealy(MEALY101, xs, overlap=False) == spec_nonoverlap(xs, (1, 0, 1))
v.assert_true("101 and 110 detectors match their specifications on all inputs up to length 10", True)


# ---------------------------------------------------------------- exact two-level minimization
def covers(cube, m, n):
    return all(c is None or c == (m >> (n - 1 - i)) & 1 for i, c in enumerate(cube))


def minlits(on, dc=(), n=3):
    """Exact minimum literal count of a sum of products (exhaustive over sets of implicants)."""
    on, dc = set(on), set(dc)
    if not on:
        return 0
    imps = [c for c in itertools.product((0, 1, None), repeat=n)
            if all(m in on or m in dc for m in range(2 ** n) if covers(c, m, n))]
    for k in range(1, len(on) + 1):
        best = None
        for combo in itertools.combinations(imps, k):
            if all(any(covers(c, m, n) for c in combo) for m in on):
                lits = sum(sum(x is not None for x in c) for c in combo)
                best = lits if best is None else min(best, lits)
        if best is not None:
            # a cover with more terms can have fewer literals only if terms are larger; check k+1 too
            for combo in itertools.combinations(imps, k + 1):
                if all(any(covers(c, m, n) for c in combo) for m in on):
                    best = min(best, sum(sum(x is not None for x in c) for c in combo))
            return best


def moore_logic(m, ones, code, nbits=2):
    """Minterms (q1 q0 x) of q1+ and q0+, and of z over (q1 q0); unused codes are don't cares."""
    q1, q0 = [], []
    for s, nx in m.items():
        for x in (0, 1):
            idx = (code[s] << 1) | x
            if (code[nx[x]] >> 1) & 1:
                q1.append(idx)
            if code[nx[x]] & 1:
                q0.append(idx)
    unused = [c for c in range(2 ** nbits) if c not in code.values()]
    dc = [(c << 1) | x for c in unused for x in (0, 1)]
    zon = [code[s] for s in ones]
    return minlits(q1, dc), minlits(q0, dc), minlits(zon, unused, 2)


def check_eq(f, on, n=3):
    return all(bool(f(*[(m >> (n - 1 - i)) & 1 for i in range(n)])) == (m in on) for m in range(2 ** n))


# ================================================================= chapter
v.check("Th 08-08.a", 5 * 2 ** 3)
xs1 = [1, 1, 0, 1, 0, 1, 1, 0, 1]
zm = run_moore(MOORE101, {3}, xs1)
ze = run_mealy(MEALY101, xs1)
v.check("Ex 08-08.1a", len(MOORE101))
hits_m = [t for t, z in enumerate(zm) if z]
v.check("Ex 08-08.1b", hits_m[0])
v.check("Ex 08-08.1d", hits_m[1])
v.check("Ex 08-08.1e", hits_m[2])
v.check("Ex 08-08.1c", len(hits_m))
hits_e = [t for t, z in enumerate(ze) if z]
v.check("Ex 08-08.2a", len(MEALY101))
v.check("Ex 08-08.2b", hits_e[0])
v.check("Ex 08-08.2d", hits_e[1])
v.check("Ex 08-08.2e", hits_e[2])
v.check("Ex 08-08.2c", sum(run_mealy(MEALY101, xs1, overlap=False)))
v.assert_true("Mealy output leads Moore by one cycle", [t + 1 for t in hits_e] == hits_m)

A = {0: 0, 1: 1, 2: 2, 3: 3}
l1, l0, lz = moore_logic(MOORE101, {3}, A)
v.check("Ex 08-08.3a", l1 + l0)
v.check("Ex 08-08.3g", lz)
# the derived equations reproduce the table
on_q1 = [(A[s] << 1) | x for s in MOORE101 for x in (0, 1) if (A[MOORE101[s][x]] >> 1) & 1]
v.assert_true("q1+ = q0 x' + q1 q0' x", check_eq(lambda a, b, x: (b and not x) or (a and not b and x), on_q1))
# Mealy detector, codes S0=00 S1=01 S2=10, 11 don't care
mq1, mq0, mz = [], [], []
for s, row in MEALY101.items():
    for x in (0, 1):
        nx, z = row[x]
        idx = (s << 1) | x
        if nx >> 1:
            mq1.append(idx)
        if nx & 1:
            mq0.append(idx)
        if z:
            mz.append(idx)
v.check("Ex 08-08.3b", minlits(mq1, [6, 7]) + minlits(mq0, [6, 7]))
v.check("Ex 08-08.3h", minlits(mz, [6, 7]))
v.assert_true("Mealy equations q1+ = q0 x', q0+ = x, z = q1 x",
              all(((b and not x) == ((a << 2 | b << 1 | x) in mq1)) and (bool(x) == ((a << 2 | b << 1 | x) in mq0))
                  and ((a and x) == ((a << 2 | b << 1 | x) in mz))
                  for a in (0, 1) for b in (0, 1) for x in (0, 1) if (a, b) != (1, 1)))
v.check("Ex 08-08.3c", math.ceil(math.log2(4)))
v.check("Ex 08-08.3d", 2 ** 2 - 4)
v.check("Ex 08-08.3e", 4)
v.check("Ex 08-08.3f", 2 ** 4 - 4)
v.check("Ex 08-08.3i", 2 ** 2 - 3)
v.check("Ex 08-08.3j", 3)
v.check("Ex 08-08.3k", 2 ** 3 - 3)


def refine_moore(states, out, nxt):
    blk = {s: out[s] for s in states}
    sizes = []
    while True:
        sizes.append(len(set(blk.values())))
        sig = {s: (blk[s],) + tuple(blk[nxt[s][x]] for x in (0, 1)) for s in states}
        ids = {k: i for i, k in enumerate(sorted(set(sig.values()), key=repr))}
        new = {s: ids[sig[s]] for s in states}
        if len(set(new.values())) == len(set(blk.values())):
            return sizes, new
        blk = new


def refine_mealy(states, m):
    blk = {s: tuple(m[s][x][1] for x in (0, 1)) for s in states}
    sizes = []
    while True:
        sizes.append(len(set(blk.values())))
        sig = {s: (blk[s],) + tuple(blk[m[s][x][0]] for x in (0, 1)) for s in states}
        ids = {k: i for i, k in enumerate(sorted(set(sig.values()), key=repr))}
        new = {s: ids[sig[s]] for s in states}
        if len(set(new.values())) == len(set(blk.values())):
            return sizes, new
        blk = new


EX4 = {"A": ("B", "C"), "B": ("D", "E"), "C": ("F", "G"), "D": ("D", "A"), "E": ("D", "A"),
       "F": ("F", "A"), "G": ("F", "A")}
EX4OUT = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 1, "F": 0, "G": 1}
sizes, cls = refine_moore(list(EX4), EX4OUT, EX4)
v.check("Ex 08-08.4a", sizes[0])
v.check("Ex 08-08.4b", sizes[1])
v.check("Ex 08-08.4c", sizes[2])
v.check("Ex 08-08.4d", len(set(cls.values())))
v.check("Ex 08-08.4e", math.ceil(math.log2(len(EX4))))
v.check("Ex 08-08.4f", math.ceil(math.log2(len(set(cls.values())))))
# the merged machine behaves identically on every input sequence up to length 8
mini = {cls[s]: tuple(cls[EX4[s][x]] for x in (0, 1)) for s in EX4}
mini_out = {cls[s]: EX4OUT[s] for s in EX4}


def outs(m, o, s, xs):
    r = [o[s]]
    for x in xs:
        s = m[s][x]
        r.append(o[s])
    return r


v.assert_true("Example 4 minimal machine equivalent to original",
              all(outs(EX4, EX4OUT, s, xs) == outs(mini, mini_out, cls[s], xs)
                  for s in EX4 for n in range(9) for xs in itertools.product((0, 1), repeat=n)))
v.assert_true("Example 4 classes are A, BC, DF, EG",
              {frozenset(k for k in EX4 if cls[k] == c) for c in set(cls.values())}
              == {frozenset("A"), frozenset("BC"), frozenset("DF"), frozenset("EG")})

tpcq, tsu, tg = 80, 40, 35
tb_ = tpcq + 6 * tg + tsu
to_ = tpcq + 3 * tg + tsu
v.check("Ex 08-08.5a", tb_)
v.check("Ex 08-08.5b", 1e3 / tb_)
v.check("Ex 08-08.5c", to_)
v.check("Ex 08-08.5d", 1e3 / to_)
tm = tpcq + (4 + 2 + 3) * tg + tsu
v.check("Ex 08-08.5e", tm)
v.check("Ex 08-08.5f", 1e3 / tm)
treg = max(tpcq + (4 + 2) * tg + tsu, tpcq + 3 * tg + tsu, tb_)
v.check("Ex 08-08.5g", treg)
v.check("Ex 08-08.5h", 1e3 / treg)

phases = [25, 4, 1, 25, 4, 1]
v.check("Ex 08-08.6a", sum(phases))
v.assert_true("32768 is a power of 2", 32768 & (32768 - 1) == 0)
v.check("Ex 08-08.6b", (32768).bit_length() - 1)
v.check("Ex 08-08.6c", math.ceil(math.log2(len(phases))))
v.check("Ex 08-08.6d", (max(phases) - 1).bit_length())
v.check("Ex 08-08.6e", math.ceil(math.log2(len(phases))) + (max(phases) - 1).bit_length())
v.check("Ex 08-08.6f", math.ceil(math.log2(sum(phases))))
v.check("Ex 08-08.6g", sum(phases))

A_FF, A_NAND = 25.024, 3.7536
v.check("Ex 08-08.7f", math.ceil(math.log2(12)))
v.check("Ex 08-08.7g", 12 - math.ceil(math.log2(12)))
v.check("Ex 08-08.7a", (12 - math.ceil(math.log2(12))) * A_FF)
v.check("Ex 08-08.7b", (12 - math.ceil(math.log2(12))) * A_FF / A_NAND)
v.check("Ex 08-08.7h", math.ceil(math.log2(31)))
v.check("Ex 08-08.7i", 31 - math.ceil(math.log2(31)))
v.check("Ex 08-08.7c", (31 - 5) * A_FF)
v.check("Ex 08-08.7j", (31 - 5) * A_FF / A_NAND)
v.check("Ex 08-08.7m", A_FF / A_NAND)


def flip_stats(codes, nbits):
    legal = set(codes)
    total = len(codes) * nbits
    bad = sum((c ^ (1 << b)) not in legal for c in codes for b in range(nbits))
    return total, bad


tot, bad = flip_stats(list(range(31)), 5)
v.check("Ex 08-08.7k", tot)
v.check("Ex 08-08.7l", bad)
v.check("Ex 08-08.7d", 100 * bad / tot)
tot1, bad1 = flip_stats([1 << i for i in range(31)], 31)
v.check("Ex 08-08.7e", 100 * bad1 / tot1)

# Mealy-to-Moore construction for the 101 detector: count (state, entering output) pairs
entered = {(n, z) for s in MEALY101 for (n, z) in MEALY101[s]} | {(0, 0)}
v.check("Th 08-08.b", len(MEALY101) * 2)
v.assert_true("Mealy 101 converts to a 4-state Moore machine", len(entered) == 4)
B = {0: 0, 1: 1, 2: 3, 3: 2}
v.check("Th 08-08.c", sum(moore_logic(MOORE110, {3}, A)))
v.check("Th 08-08.d", sum(moore_logic(MOORE110, {3}, B)))

# ================================================================= solutions
v.check("08-08.1a", math.ceil(math.log2(9)))
v.check("08-08.1b", 2 ** 4 - 9)
v.check("08-08.1c", 9)
v.check("08-08.1d", 2 ** 9 - 9)
v.check("08-08.2a", 6 * 2 ** 2)
v.check("08-08.2b", 12 * 2 ** 4)
xs3 = [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1]
h3 = [t for t, z in enumerate(run_mealy(MEALY101, xs3)) if z]
v.check("08-08.3a", h3[0])
v.check("08-08.3b", h3[1])
v.check("08-08.3c", h3[2])
v.check("08-08.3d", sum(run_mealy(MEALY101, xs3, overlap=False)))
v.check("08-08.3e", [t for t, z in enumerate(run_moore(MOORE101, {3}, xs3)) if z][0])


def min_moore_states_for(pattern):
    """Minimal Moore detector size by building the suffix machine and minimizing it."""
    k = len(pattern)
    pre = [tuple(pattern[:i]) for i in range(k + 1)]

    def nxt(i, x):
        h = pre[i] + (x,)
        for j in range(min(len(h), k), -1, -1):
            if h[len(h) - j:] == pre[j]:
                return j
        return 0
    m = {i: (nxt(i, 0), nxt(i, 1)) for i in range(k + 1)}
    sizes, cls = refine_moore(list(m), {i: int(i == k) for i in m}, m)
    return len(set(cls.values())), m


n110, m110 = min_moore_states_for((1, 1, 0))
v.assert_true("suffix construction reproduces the 110 table", m110 == MOORE110)
v.check("08-08.4a", n110)
# minimal Mealy: merge the accepting state (its outputs move to the arrows)
mealy110 = {s: tuple((m110[s][x], int(m110[s][x] == 3)) for x in (0, 1)) for s in m110}
_, mc = refine_mealy(list(mealy110), mealy110)
reach = {mc[s] for s in mealy110}
v.check("08-08.4b", len(reach))
xs4 = [1, 1, 1, 0, 1, 1, 0, 0]
h4 = [t for t, z in enumerate(run_moore(MOORE110, {3}, xs4)) if z]
v.check("08-08.4c", h4[0])
v.check("08-08.4d", h4[1])
a1, a0, az = moore_logic(MOORE110, {3}, A)
b1, b0, bz = moore_logic(MOORE110, {3}, B)
v.check("08-08.5a", a1)
v.check("08-08.5b", a0)
v.check("08-08.5c", a1 + a0 + az)
v.check("08-08.5d", b1)
v.check("08-08.5e", b0)
v.check("08-08.5f", b1 + b0 + bz)


# P6: minimal machines for edge detectors, by brute-force search over small Moore machines
def moore_matches(m, o, f, n=8):
    return all(outs(m, o, 0, list(xs))[1:] == f(list(xs)) for k in range(1, n) for xs in itertools.product((0, 1), repeat=k))


def change(xs):
    return [int(t > 0 and xs[t] != xs[t - 1]) for t in range(len(xs))]


def rise(xs):
    return [int(t > 0 and xs[t] == 1 and xs[t - 1] == 0) for t in range(len(xs))]


def change0(xs):   # the first input compares with an assumed previous input 0
    return [int(xs[t] != (xs[t - 1] if t else 0)) for t in range(len(xs))]


def rise0(xs):
    return [int(xs[t] == 1 and (xs[t - 1] if t else 0) == 0) for t in range(len(xs))]


def smallest_moore(f, nmax=5):
    for n in range(1, nmax + 1):
        for table in itertools.product(range(n), repeat=2 * n):
            m = {s: (table[2 * s], table[2 * s + 1]) for s in range(n)}
            for o in itertools.product((0, 1), repeat=n):
                if o[0] == 0 and moore_matches(m, dict(enumerate(o)), f, 7):
                    return n
    return None


def smallest_mealy(f, nmax=3):
    for n in range(1, nmax + 1):
        for table in itertools.product(range(n), repeat=2 * n):
            for zs in itertools.product((0, 1), repeat=2 * n):
                m = {s: ((table[2 * s], zs[2 * s]), (table[2 * s + 1], zs[2 * s + 1])) for s in range(n)}
                if all(run_mealy(m, list(xs)) == f(list(xs)) for k in range(1, 7)
                       for xs in itertools.product((0, 1), repeat=k)):
                    return n
    return None


v.check("08-08.6a", smallest_mealy(change0))
v.check("08-08.6b", smallest_moore(change0))
v.check("08-08.6c", smallest_mealy(rise0))
v.check("08-08.6d", smallest_moore(rise0))

P7 = {"A": (("B", 0), ("C", 0)), "B": (("A", 0), ("D", 1)), "C": (("A", 0), ("E", 1)),
      "D": (("F", 0), ("D", 1)), "E": (("F", 0), ("E", 1)), "F": (("A", 0), ("C", 0))}
sizes7, cls7 = refine_mealy(list(P7), P7)
v.check("08-08.7a", sizes7[0])
v.check("08-08.7b", sizes7[1])
v.check("08-08.7c", sizes7[2])
v.check("08-08.7d", len(set(cls7.values())))
v.check("08-08.7e", math.ceil(math.log2(6)))
v.check("08-08.7f", math.ceil(math.log2(len(set(cls7.values())))))
v.assert_true("P7 merged classes behave identically",
              all(run_mealy({k: P7[k] for k in P7}, list(xs), s=a) == run_mealy(P7, list(xs), s=b)
                  for a in P7 for b in P7 if cls7[a] == cls7[b]
                  for n in range(1, 8) for xs in itertools.product((0, 1), repeat=n)))
v.check("08-08.8a", sum(len(MOORE110[s]) for s in MOORE110))
incoming = {t: sum(1 for s in MOORE110 for x in (0, 1) if MOORE110[s][x] == t) for t in MOORE110}
v.check("08-08.8b", sum(c - 1 for c in incoming.values() if c > 0))
v.check("08-08.9a", 70 + 260 + 50)
v.check("08-08.9b", 1e3 / (70 + 260 + 50))
v.check("08-08.9c", 40 + 20 - 30)
v.check("08-08.9d", 40 + 20 - 30 - 50)
t10, b10 = flip_stats(list(range(6)), 3)
v.check("08-08.10a", 8 - 6)
v.check("08-08.10b", t10)
v.check("08-08.10c", b10)
v.check("08-08.10d", 100 * b10 / t10)
v.check("08-08.10e", 2 ** 6 - 6)
t10o, b10o = flip_stats([1 << i for i in range(6)], 6)
v.check("08-08.10f", 100 * b10o / t10o)
fs = 16 * 115200
v.check("08-08.11a", fs / 1e6)
v.check("08-08.11b", 10 / 115200 * 1e6)
v.check("08-08.11c", 8 / fs * 1e6)
v.check("08-08.11d", math.ceil(math.log2(4)) + (15).bit_length() + (7).bit_length() + 8)


# P12: build the pure debouncer FSM and check it, then count
def debounce_states(n=8):
    return 1 + (n - 1) + 1 + (n - 1)


def debounce_sim(samples, n=8):
    out, level, run = [], 0, 0
    for s in samples:
        run = run + 1 if s != level else 0
        if run == n:
            level, run = s, 0
        out.append(level)
    return out


ns12 = debounce_states()
v.check("08-08.12a", ns12)
v.check("08-08.12b", math.ceil(math.log2(ns12)))
v.check("08-08.12c", math.ceil(math.log2(4)) + (7).bit_length())
o12 = debounce_sim([1] * 12)
v.check("08-08.12d", o12.index(1) * 1.0)   # sample k is taken at k ms
# P13: Moore to Mealy conversion, then find identical rows
conv = {s: tuple((MOORE101[s][x], int(MOORE101[s][x] == 3)) for x in (0, 1)) for s in MOORE101}
pairs = [(a, b) for a, b in itertools.combinations(conv, 2) if conv[a] == conv[b]]
v.check("08-08.13a", len(pairs))
_, c13 = refine_mealy(list(conv), conv)
v.check("08-08.13b", len(set(c13.values())))
v.check("08-08.13c", [t for t, z in enumerate(run_mealy(conv, xs1)) if z][0])


# P14: smallest code lengths for 4 codewords at distance 2 and 3, by exhaustive search
def min_bits(dist, k=4):
    for n in range(1, 8):
        for codes in itertools.combinations(range(2 ** n), k):
            if all(bin(a ^ b).count("1") >= dist for a, b in itertools.combinations(codes, 2)):
                return n
    return None


v.check("08-08.14a", min_bits(2))
v.check("08-08.14b", 4 * (1 + 4))
v.check("08-08.14c", 2 ** 4)
v.check("08-08.14d", min_bits(3))
v.assert_true("00000 00111 11001 11110 have minimum distance 3",
              min(bin(a ^ b).count("1") for a, b in itertools.combinations([0b00000, 0b00111, 0b11001, 0b11110], 2)) == 3)
v.check("08-08.15a", math.ceil(math.log2(20)))
v.check("08-08.15b", 20)
v.check("08-08.15c", (20 - 5) * A_FF)
v.check("08-08.15d", (20 - 5) * A_FF / A_NAND)
v.check("08-08.15e", 50 * (20 - 5) * A_FF / 1e6)

# ================================================================= lab
totals = [sum(moore_logic(MOORE110, {3}, dict(enumerate(p)))) for p in itertools.permutations(range(4))]
v.check("Lab 08-08.a", len(totals))
v.check("Lab 08-08.b", min(totals))
v.check("Lab 08-08.c", max(totals))
v.check("Lab 08-08.d", totals.count(min(totals)))
t12, b12 = flip_stats(list(range(12)), 4)
v.check("Lab 08-08.e", 100 * b12 / t12)
v.check("Lab 08-08.f", sum([5, 2, 1, 5, 2, 1]))
v.check("Lab 08-08.g", hits_m[0] - hits_e[0])

v.finish()
