#!/usr/bin/env python3
"""Verify every number in chapter 19-13 (verification), its problems and its lab.

Independent routes (none reuses the lab's formulas for the quantity being checked):
- coverage closure: exact rational harmonic numbers; unequal bins by a dynamic program over covered subsets (not
  inclusion-exclusion); closure probabilities from a Markov chain on the number of covered bins (matrix powers);
- arbiter fairness: a separately coded exhaustive search that tracks one requester's wait, plus a cycle-by-cycle
  evaluation of the SVA windows;
- ROBDD sizes: counting distinct cofactors that depend on the next variable, directly from truth tables (numpy);
- adder miter: brute force over all inputs with integer models of the ripple and the buggy lookahead adder;
- model checking: reachability and BMC depths from Boolean adjacency matrices, k-induction by enumerating every
  state sequence of length k + 1, the protocol re-encoded with integers.
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-13-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import verif  # noqa: E402

v = Verifier.from_files("19-13", ROOT / "chapters" / "19-13-verification-methods.md",
                        ROOT / "solutions" / "19-13-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- coverage closure
def harmonic(n):
    return sum(Fraction(1, k) for k in range(1, n + 1))


def expected_cover_dp(probs):
    """E[samples to cover every bin] by a DP over the set of covered bins:
    E[S] = (1 + sum_{i not in S} p_i E[S + i]) / sum_{i not in S} p_i, with E[all] = 0."""
    n = len(probs)
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def e(mask):
        if mask == full:
            return 0.0
        new = [i for i in range(n) if not mask >> i & 1]
        q = sum(probs[i] for i in new)
        return (1 + sum(probs[i] * e(mask | 1 << i) for i in new)) / q
    return e(0)


def p_all_markov(n, t):
    """P(all n equal bins covered after t samples) from the Markov chain on the number of covered bins."""
    m = np.zeros((n + 1, n + 1))
    for k in range(n + 1):
        m[k, k] = k / n
        if k < n:
            m[k, k + 1] = (n - k) / n
    state = np.zeros(n + 1)
    state[0] = 1.0
    return float((state @ np.linalg.matrix_power(m, t))[n])


e16 = 16 * harmonic(16)
v.check("Ex 19-13.1a", float(e16))
v.check("Lab 19-13.i", float(e16))
v.check("Ex 19-13.1b", 16 * math.log(16) + 0.5772156649 * 16 + 0.5)
t95 = next(t for t in range(1, 500) if p_all_markov(16, t) >= 0.95)
v.check("Ex 19-13.1c", t95)
v.assert_true("t = 89 is below 95 %", p_all_markov(16, 89) < 0.95, f"{p_all_markov(16, 89):.4f}")
rare = [0.99 / 7] * 7 + [0.01]
e_rare = expected_cover_dp(rare)
v.check("Ex 19-13.1d", e_rare)
v.check("Lab 19-13.j", e_rare)
v.assert_true("rare-bin mean exceeds 1/p_min", e_rare >= 100, f"{e_rare:.3f}")
v.assert_true("inclusion-exclusion (lab) agrees with the DP", abs(verif.expected_to_cover_exact(rare) - e_rare) < 1e-9, "")
# seven common bins after a directed test has covered the corner: the corner still takes 1 % of the samples


@lru_cache(maxsize=None)
def e_seven(mask):
    need = [i for i in range(7) if not mask >> i & 1]
    if not need:
        return 0.0
    q = sum(rare[i] for i in need)
    return (1 + sum(rare[i] * e_seven(mask | 1 << i) for i in need)) / q


v.check("Ex 19-13.1e", e_seven(0))

v.check("19-13.2a", float(32 * harmonic(32)))
v.check("19-13.2b", float(64 * harmonic(64)))
v.check("19-13.2c", 64 * float(Fraction(63, 64) ** 64))
v.check("19-13.3a", p_all_markov(8, 30))
t99 = next(t for t in range(1, 500) if p_all_markov(8, t) >= 0.99)
v.check("19-13.3b", t99)
e4 = expected_cover_dp([0.5, 0.3, 0.15, 0.05])
v.check("19-13.4a", e4)
v.check("19-13.4b", 1 / 0.05)
v.check("19-13.4c", float(4 * harmonic(4)))
v.check("Txt 19-13.a", 4 + 5)          # four one-hot grant bins and five active-request counts (0..4)
v.check("Lab 19-13.b", 4 + 5)
v.check("Lab 19-13.h", (1 / 16) ** 4)


# ---------------------------------------------------------------- arbiter fairness
def worst_wait_tracked(n, cap=50):
    """Exhaustive search that tracks requester 0 only (by symmetry the worst case is the same for every requester).
    State: (pointer, pending set, requester 0's wait). Each idle requester may raise a request; requests are held."""
    start = (n - 1, 0, 0)
    seen, stack, worst = {start}, [start], 0
    while stack:
        last, pend, w = stack.pop()
        idle = [i for i in range(n) if not pend >> i & 1]
        for raised in itertools.product((0, 1), repeat=len(idle)):
            req = pend | sum(1 << i for i, r in zip(idle, raised) if r)
            order = [(last + k) % n for k in range(1, n + 1)]
            g = next((i for i in order if req >> i & 1), None)
            nw = 0 if g == 0 else (min(w + 1, cap) if (req & 1 and g is not None) else w)
            worst = max(worst, nw)
            nxt = (last if g is None else g, req if g is None else req & ~(1 << g), nw)
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return worst


v.check("Lab 19-13.a", worst_wait_tracked(4))
v.check("19-13.5a", worst_wait_tracked(6))
v.assert_true("worst wait is N - 1 for N = 2..5", all(worst_wait_tracked(n) == n - 1 for n in range(2, 6)), "")
v.assert_true("the lab's search agrees", verif.arbiter_worst_wait(4) == 3, "")
v.check("19-13.5b", 7 * 16)


def first_failure_fixed_priority(window=3, cycles=20):
    """Requesters 0 and 1 request every cycle from cycle 1; fixed priority grants 0. Evaluate req[1] |-> ##[0:w] gnt[1]."""
    gnt1 = {c: False for c in range(1, cycles + 1)}
    for start in range(1, cycles + 1):
        end = start + window
        if end > cycles:
            break
        if not any(gnt1[c] for c in range(start, end + 1)):
            return end
    return None


v.check("19-13.5c", first_failure_fixed_priority())


def sva_window(req_cycles, ack_cycles, lo, hi, cycles=10):
    """Attempts of req |-> ##[lo:hi] ack on cycles 1..cycles: returns (failure cycles, vacuous count, passes)."""
    fails, vac, passes = [], 0, []
    for c in range(1, cycles + 1):
        if c not in req_cycles:
            vac += 1
            continue
        if any(a in ack_cycles for a in range(c + lo, c + hi + 1)):
            passes.append(c)
        else:
            fails.append(c + hi)
    return fails, vac, passes


fails, vac, passes = sva_window({2, 6}, {4, 9}, 1, 2)
v.assert_true("attempt from cycle 2 passes", 2 in passes, str(passes))
v.check("19-13.6a", fails[0])
fails2, _, _ = sva_window({2, 6}, {4, 9}, 2, 3)
v.check("19-13.6b", len(fails2))
v.check("19-13.6c", vac)


# ---------------------------------------------------------------- ROBDD sizes from truth tables
def robdd_size(tt, nvars):
    """Nodes of the ROBDD of a function given as a truth table indexed with variable 0 as the most significant bit
    (variable order 0, 1, ..., nvars-1): at each level, count the distinct subfunctions that depend on that variable."""
    total = 0
    subs = {tt.tobytes(): tt}
    for _ in range(nvars):
        nxt, count = {}, 0
        for f in subs.values():
            half = f.size // 2
            lo, hi = f[:half], f[half:]
            if not np.array_equal(lo, hi):
                count += 1
            for g in (lo, hi):
                nxt[g.tobytes()] = g
        total += count
        subs = nxt
    return total


def table(fn, order):
    """Truth table of fn(assignment dict) with variables tested in `order` (list of names)."""
    n = len(order)
    out = np.zeros(1 << n, dtype=np.uint8)
    for idx in range(1 << n):
        a = {name: (idx >> (n - 1 - k)) & 1 for k, name in enumerate(order)}
        out[idx] = fn(a)
    return out


def sum_xy(n):
    return lambda a: int(any(a[f"x{i}"] and a[f"y{i}"] for i in range(n)))


def inter(n):
    return [nm for i in range(n) for nm in (f"x{i}", f"y{i}")]


def sep(n):
    return [f"x{i}" for i in range(n)] + [f"y{i}" for i in range(n)]


for n, ida, idb in ((3, "Ex 19-13.2a", "Ex 19-13.2b"), (8, "Ex 19-13.2c", "Ex 19-13.2d")):
    v.check(ida, robdd_size(table(sum_xy(n), inter(n)), 2 * n))
    v.check(idb, robdd_size(table(sum_xy(n), sep(n)), 2 * n))
v.assert_true("separated size is 2^(n+1) - 2 for n = 2..7",
              all(robdd_size(table(sum_xy(n), sep(n)), 2 * n) == 2 ** (n + 1) - 2 for n in range(2, 8)), "")
v.check("Ex 19-13.2e", 2 ** 33 - 2)


def eq_ab(n):
    return lambda a: int(all(a[f"x{i}"] == a[f"y{i}"] for i in range(n)))


v.check("19-13.8a", robdd_size(table(eq_ab(4), inter(4)), 8))
v.check("19-13.8b", robdd_size(table(eq_ab(4), sep(4)), 8))
v.check("Lab 19-13.d", robdd_size(table(eq_ab(8), inter(8)), 16))
v.check("Lab 19-13.c", robdd_size(table(eq_ab(8), sep(8)), 16))
v.assert_true("comparator sizes follow 3n and 3*2^n - 3 for n = 2..6",
              all(robdd_size(table(eq_ab(n), inter(n)), 2 * n) == 3 * n
                  and robdd_size(table(eq_ab(n), sep(n)), 2 * n) == 3 * 2 ** n - 3 for n in range(2, 7)), "")
v.check("19-13.8c", 3 * 16)
v.check("19-13.8d", 3 * 2 ** 16 - 3)
v.check("19-13.7a", robdd_size(table(lambda a: int(a["a"] + a["b"] + a["c"] >= 2), ["a", "b", "c"]), 3))
par5 = [f"p{i}" for i in range(5)]
v.check("19-13.7b", robdd_size(table(lambda a: sum(a.values()) % 2, par5), 5))
v.assert_true("parity size is order independent (reversed order)",
              robdd_size(table(lambda a: sum(a.values()) % 2, par5[::-1]), 5) == 9, "")


# sum bits of an 8-bit adder, interleaved order a0 b0 a1 b1 ... (least significant bits first)
def adder_bit(i):
    def f(a):
        x = sum(a[f"x{k}"] << k for k in range(8))
        y = sum(a[f"y{k}"] << k for k in range(8))
        return ((x + y) >> i) & 1
    return f


sizes = [robdd_size(table(adder_bit(i), inter(8)), 16) for i in range(8)]
v.assert_true("sum bit i has 3i + 3 nodes (8-bit adder)", sizes == [3 * i + 3 for i in range(8)], str(sizes))
v.check("Lab 19-13.e", sizes[7])
v.check("Txt 19-13.e", 3 * 31 + 3)
v.check("Txt 19-13.f", -math.log(0.01))


# ---------------------------------------------------------------- adder miter by brute force
def lookahead_buggy(x, y, n=4, bug_carry=3):
    a = [(x >> i) & 1 for i in range(n)]
    b = [(y >> i) & 1 for i in range(n)]
    g = [ai & bi for ai, bi in zip(a, b)]
    p = [ai ^ bi for ai, bi in zip(a, b)]
    c = [0]
    for i in range(1, n + 1):
        terms = []
        for j in range(i):
            if i == bug_carry and j == 0:
                continue
            t = g[j]
            for k in range(j + 1, i):
                t &= p[k]
            terms.append(t)
        c.append(int(any(terms)))
    return sum((p[i] ^ c[i]) << i for i in range(n)) | (c[n] << n)


bad = [(x, y) for x in range(16) for y in range(16) if lookahead_buggy(x, y) != x + y]
v.check("Ex 19-13.3a", len(bad))
v.assert_true("correct lookahead equals ripple on all inputs",
              all(lookahead_buggy(x, y, bug_carry=99) == x + y for x in range(16) for y in range(16)), "")
v.assert_true("(7, 1) is a counterexample", (7, 1) in bad, "")
v.check("Ex 19-13.3b", 7)
v.check("Ex 19-13.3c", 1)
v.check("Ex 19-13.3d", 7 + 1)
v.check("Ex 19-13.3e", lookahead_buggy(7, 1))
v.assert_true("the lab's BDD miter returns the same counterexample",
              (lambda b: (lambda A, B: verif.equivalent(b, verif.ripple_adder(b, A, B),
                                                       verif.lookahead_adder(b, A, B, bug_bit=3))[1])(
                  [b.var(2 * i) for i in range(4)], [b.var(2 * i + 1) for i in range(4)]))(verif.BDD(8))
              == {0: 1, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0}, "")
v.check("Ex 19-13.3f", 2.0 ** -32)
v.check("Ex 19-13.3g", math.log(0.01) / math.log1p(-2.0 ** -32))
# problem 9: the per-vector probability 2^-(k+1) checked by brute force on an 8-bit adder for k = 3..6
for k in range(3, 7):
    cnt = sum(1 for x in range(256) for y in range(256)
              if lookahead_buggy(x, y, n=8, bug_carry=k) != x + y)
    v.assert_true(f"8-bit adder, bug at carry {k}: fraction 2^-(k+1)", cnt == 65536 >> (k + 1), str(cnt))
n15 = math.log(0.01) / math.log1p(-2.0 ** -16)
v.check("19-13.9a", n15)
v.check("19-13.9b", n15 / 1e6)
n63 = math.log(0.01) / math.log1p(-2.0 ** -64)
v.check("19-13.9c", n63)
v.check("19-13.9d", n63 / 1e6 / (365.25 * 86400))


# ---------------------------------------------------------------- model checking with adjacency matrices
def adjacency(nstates, succ):
    m = np.zeros((nstates, nstates), dtype=bool)
    for s in range(nstates):
        for t in succ(s):
            m[s, t] = True
    return m


def reach_layers(m, init):
    """Breadth-first layers by Boolean matrix-vector products; returns the depth of every reachable state."""
    depth = {s: 0 for s in init}
    frontier = np.zeros(m.shape[0], dtype=bool)
    frontier[list(init)] = True
    d = 0
    while frontier.any():
        d += 1
        nxt = (frontier.astype(int) @ m.astype(int)) > 0
        new = [s for s in np.flatnonzero(nxt) if s not in depth]
        for s in new:
            depth[s] = d
        frontier = np.zeros_like(frontier)
        frontier[new] = True
    return depth


def fifo_succ(buggy):
    def succ(c):
        out = set()
        for push in (0, 1):
            for pop in (0, 1):
                n = c + (1 if push and (buggy or c < 4) else 0) - (1 if pop and c > 0 else 0)
                out.add(n % 8)
        return out
    return succ


good = reach_layers(adjacency(8, fifo_succ(False)), [0])
badr = reach_layers(adjacency(8, fifo_succ(True)), [0])
v.check("Ex 19-13.4a", len(good))
v.check("Ex 19-13.4b", len(badr))
first_bad = min(d for s, d in badr.items() if s > 4)
v.check("Ex 19-13.4c", first_bad)
v.check("Ex 19-13.4d", first_bad)
v.check("Ex 19-13.4e", 3 * (first_bad + 1) + 2 * first_bad)
v.check("Ex 19-13.4f", max(good.values()))
v.assert_true("c <= 4 is 1-inductive for the correct counter",
              all(t <= 4 for c in range(5) for t in fifo_succ(False)(c)), "")


def k_step_holds(states, succ, prop, k):
    """Enumerate every sequence of k + 1 states; the step holds if no T-path with P on its first k states fails P last."""
    for seq in itertools.product(states, repeat=k + 1):
        if all(seq[i + 1] in succ(seq[i]) for i in range(k)) and all(prop(s) for s in seq[:-1]) and not prop(seq[-1]):
            return False
    return True


def by_two(x):
    return {(x + 2) % 8}


v.check("Ex 19-13.5a", len(reach_layers(adjacency(8, by_two), [0])))
v.assert_true("1-induction fails only through 5 -> 7",
              [s for s in range(8) if s != 7 and 7 in by_two(s)] == [5], "")
v.check("Ex 19-13.5b", 5)
kmin = next(k for k in range(1, 8) if k_step_holds(range(8), by_two, lambda x: x != 7, k))
v.check("Ex 19-13.5c", kmin)
v.check("Lab 19-13.f", kmin)
v.assert_true("'x even' is 1-inductive", all(t % 2 == 0 for x in range(0, 8, 2) for t in by_two(x)), "")


def bcd(x):
    return {0 if x == 9 else (x + 1) % 16}


v.check("19-13.11a", len(reach_layers(adjacency(16, bcd), [0])))
v.check("19-13.11b", next(s for s in range(16) if s != 12 and 12 in bcd(s)))
k_bcd = next(k for k in range(1, 6) if k_step_holds(range(16), bcd, lambda x: x != 12, k))
v.check("19-13.11c", k_bcd)
v.assert_true("x <= 9 is 1-inductive", all(t <= 9 for x in range(10) for t in bcd(x)), "")


# two-process protocol, re-encoded: state = 3*3*2 integers; 0 idle, 1 requesting, 2 critical
def proto_succ(buggy):
    def succ(code):
        s0, s1, turn = code // 6, (code // 2) % 3, code % 2

        def moves(me, other, i):
            if me == 0:
                return (0, 1)
            if me == 1:
                enter = other != 2 and (buggy or other != 1 or turn == i)
                return (2,) if enter else (1,)
            return (2, 0)
        out = set()
        for m0 in moves(s0, s1, 0):
            for m1 in moves(s1, s0, 1):
                t = turn
                if s0 == 2 and m0 == 0:
                    t = 1
                if s1 == 2 and m1 == 0:
                    t = 0
                out.add(m0 * 6 + m1 * 2 + t)
        return out
    return succ


v.check("19-13.10a", 3 * 3 * 2)
pg = reach_layers(adjacency(18, proto_succ(False)), [0])
v.check("19-13.10b", len(pg))
v.check("Lab 19-13.g", len(pg))
v.assert_true("mutual exclusion holds", all(not (c // 6 == 2 and (c // 2) % 3 == 2) for c in pg), "")
pb = reach_layers(adjacency(18, proto_succ(True)), [0])
v.check("19-13.10c", min(d for c, d in pb.items() if c // 6 == 2 and (c // 2) % 3 == 2))


# ---------------------------------------------------------------- speed ladder (illustrative speeds)
boot = 2e9
v.check("Txt 19-13.b", boot / 100 / 86400)
v.check("Txt 19-13.c", boot / 1e6 / 60)
v.check("Txt 19-13.d", boot / 20e6)
test = 5e8
v.check("19-13.12a", test / 1e6)
v.check("19-13.12b", 200 * test / 1e6 / 3600)
v.check("19-13.12c", 200 * test / 1e6 / 3600 / 4)
v.check("19-13.12d", 200 * test / 25e6 / 60)
v.check("19-13.12e", test / 100 / 86400)

sys.exit(v.finish())
