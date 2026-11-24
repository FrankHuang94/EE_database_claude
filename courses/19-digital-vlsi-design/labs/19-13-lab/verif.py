"""Verification models for Lab 19-13: coverage closure, BDD-based equivalence checking, and explicit-state model
checking (reachability, invariants, bounded model checking and k-induction) of small state machines.
"""
from __future__ import annotations

import itertools
import math
import random
from collections import deque


# ---------------------------------------------------------------- coverage closure
def harmonic(n):
    return sum(1.0 / k for k in range(1, n + 1))


def expected_to_cover(n):
    """Coupon collector: expected number of uniformly random samples to hit all n equally likely bins, n H_n."""
    return n * harmonic(n)


def expected_to_cover_unequal(probs, t_max=None, steps=200_000):
    """Expected samples to cover bins with unequal probabilities, by the Poissonization integral
    E[T] = integral_0^inf (1 - prod_i (1 - exp(-p_i t))) dt (exact for Poisson arrivals, very close for samples)."""
    t_max = t_max or 50.0 / min(probs)
    dt = t_max / steps
    total = 0.0
    for k in range(steps):
        t = (k + 0.5) * dt
        total += 1.0 - math.prod(1.0 - math.exp(-p * t) for p in probs)
    return total * dt


def expected_to_cover_exact(probs):
    """Exact expected samples by inclusion-exclusion over subsets of bins: sum over nonempty S of
    (-1)^(|S|+1) / P(S). Small bin counts only."""
    total = 0.0
    for r in range(1, len(probs) + 1):
        for subset in itertools.combinations(probs, r):
            total += (-1) ** (r + 1) / sum(subset)
    return total


def simulate_cover(probs, trials=2000, seed=1):
    rng = random.Random(seed)
    bins = list(range(len(probs)))
    counts = []
    for _ in range(trials):
        seen, n = set(), 0
        while len(seen) < len(probs):
            seen.add(rng.choices(bins, probs)[0])
            n += 1
        counts.append(n)
    return sum(counts) / trials


# ---------------------------------------------------------------- a small reduced ordered BDD package
class BDD:
    """Reduced ordered binary decision diagrams over variables 0..n-1 (the index is the order).
    Node 0 is FALSE, node 1 is TRUE; other nodes are (var, low, high) in a unique table, so equal functions
    are the same node."""

    def __init__(self, n_vars):
        self.n = n_vars
        self.nodes = [(n_vars, 0, 0), (n_vars, 1, 1)]
        self.unique = {}
        self.cache = {}

    def mk(self, var, low, high):
        if low == high:
            return low
        key = (var, low, high)
        if key not in self.unique:
            self.unique[key] = len(self.nodes)
            self.nodes.append(key)
        return self.unique[key]

    def var(self, i):
        return self.mk(i, 0, 1)

    def apply(self, op, u, v):
        key = (op, u, v)
        if key in self.cache:
            return self.cache[key]
        if u <= 1 and v <= 1:
            r = int(op(u, v))
        else:
            vu, lu, hu = self.nodes[u]
            vv, lv, hv = self.nodes[v]
            top = min(vu, vv)
            l1, h1 = (lu, hu) if vu == top else (u, u)
            l2, h2 = (lv, hv) if vv == top else (v, v)
            r = self.mk(top, self.apply(op, l1, l2), self.apply(op, h1, h2))
        self.cache[key] = r
        return r

    def AND(self, u, v):
        return self.apply(lambda a, b: a & b, u, v)

    def OR(self, u, v):
        return self.apply(lambda a, b: a | b, u, v)

    def XOR(self, u, v):
        return self.apply(lambda a, b: a ^ b, u, v)

    def NOT(self, u):
        return self.XOR(u, 1)

    def size(self, u):
        """Number of internal (non-terminal) nodes reachable from u."""
        seen, stack = set(), [u]
        while stack:
            x = stack.pop()
            if x <= 1 or x in seen:
                continue
            seen.add(x)
            _, l, h = self.nodes[x]
            stack += [l, h]
        return len(seen)

    def satisfy_one(self, u):
        """One assignment {var: value} that makes u true (a counterexample for a miter), or None."""
        if u == 0:
            return None
        out = {}
        while u > 1:
            var, l, h = self.nodes[u]
            if h != 0:
                out[var], u = 1, h
            else:
                out[var], u = 0, l
        return out


def ripple_adder(bdd, a, b):
    """Sum bits (and carry out) of a ripple-carry adder over BDD variables a[i], b[i] (LSB first)."""
    carry, out = 0, []
    for x, y in zip(a, b):
        p = bdd.XOR(x, y)
        out.append(bdd.XOR(p, carry))
        carry = bdd.OR(bdd.AND(x, y), bdd.AND(p, carry))
    return out + [carry]


def lookahead_adder(bdd, a, b, bug_bit=None):
    """Carry-lookahead form: c_{i+1} = g_i + p_i c_i expanded as an OR of generate terms gated by propagates.
    bug_bit = k drops the carry-in contribution to carry k (an injected design error)."""
    n = len(a)
    g = [bdd.AND(x, y) for x, y in zip(a, b)]
    p = [bdd.XOR(x, y) for x, y in zip(a, b)]
    carries = [0]
    for i in range(1, n + 1):
        c = 0
        for j in range(i):
            term = g[j]
            for k in range(j + 1, i):
                term = bdd.AND(term, p[k])
            if not (bug_bit == i and j == 0):
                c = bdd.OR(c, term)
        carries.append(c)
    return [bdd.XOR(p[i], carries[i]) for i in range(n)] + [carries[n]]


def equivalent(bdd, outs1, outs2):
    """Miter: OR of XORs of corresponding outputs; the circuits are equivalent iff it is the FALSE node.
    Returns (equivalent, counterexample or None)."""
    miter = 0
    for x, y in zip(outs1, outs2):
        miter = bdd.OR(miter, bdd.XOR(x, y))
    return miter == 0, bdd.satisfy_one(miter)


# ---------------------------------------------------------------- explicit-state model checking
def reachable(init, successors):
    """Breadth-first reachability; returns {state: (depth, parent)}."""
    seen = {s: (0, None) for s in init}
    q = deque(init)
    while q:
        s = q.popleft()
        for t in successors(s):
            if t not in seen:
                seen[t] = (seen[s][0] + 1, s)
                q.append(t)
    return seen


def check_invariant(init, successors, prop):
    """Return (holds, shortest counterexample trace or None)."""
    seen = reachable(init, successors)
    bad = [s for s in seen if not prop(s)]
    if not bad:
        return True, None
    s = min(bad, key=lambda x: seen[x][0])
    trace = [s]
    while seen[trace[-1]][1] is not None:
        trace.append(seen[trace[-1]][1])
    return False, trace[::-1]


def bmc(init, successors, prop, k):
    """Bounded model checking by explicit unrolling: the smallest depth <= k at which a bad state is reachable,
    or None if no violation within k steps."""
    frontier, seen = set(init), set(init)
    for depth in range(k + 1):
        if any(not prop(s) for s in frontier):
            return depth
        frontier = {t for s in frontier for t in successors(s)} - seen
        seen |= frontier
    return None


def k_inductive(states, successors, prop, k):
    """Is prop k-inductive over the full state space? True if every path of k+1 states that satisfies prop in its
    first k states also satisfies it in the last."""
    for s in states:
        paths = [[s]]
        for _ in range(k):
            paths = [p + [t] for p in paths if prop(p[-1]) for t in successors(p[-1])]
        if any(not prop(p[-1]) for p in paths if len(p) == k + 1):
            return False
    return True


# ---------------------------------------------------------------- example designs for the lab
def fifo_counter(depth=4, bits=3, buggy=False):
    """Occupancy counter of a FIFO: inputs push/pop each cycle. Returns (init, successors). The buggy version
    forgets to block a push when full, so the counter can pass the depth (and wrap at 2^bits)."""
    def succ(c):
        out = set()
        for push, pop in itertools.product((0, 1), repeat=2):
            full, empty = c == depth, c == 0
            n = c
            if push and (buggy or not full):
                n += 1
            if pop and not empty:
                n -= 1
            out.add(n % (1 << bits))
        return out
    return [0], succ


def step_by_two(bits=3):
    """A counter that adds 2 each cycle: reachable states are the even values."""
    return [0], (lambda x: {(x + 2) % (1 << bits)})


def bcd_counter():
    """A 4-bit counter that counts 0..9 and returns to 0 (values 10..15 are unreachable)."""
    return [0], (lambda x: {0 if x == 9 else (x + 1) % 16})


def mutex(buggy=False):
    """Two processes, each idle 'I', requesting 'R' or critical 'C', plus a turn bit; all moves are simultaneous.
    A requester enters if the other is not in C and, when the other also requests, only if turn names it.
    The buggy version ignores the other's request (it checks only that the other is not in C)."""
    def moves(i, s):
        me, other, turn = s[i], s[1 - i], s[2]
        if me == "I":
            return ["I", "R"]
        if me == "R":
            ok = other != "C" and (buggy or other != "R" or turn == i)
            return ["C"] if ok else ["R"]
        return ["C", "I"]

    def succ(s):
        out = set()
        for m0 in moves(0, s):
            for m1 in moves(1, s):
                turn = s[2]
                if s[0] == "C" and m0 == "I":
                    turn = 1
                if s[1] == "C" and m1 == "I":
                    turn = 0
                out.add((m0, m1, turn))
        return out
    states = [(a, b, t) for a in "IRC" for b in "IRC" for t in (0, 1)]
    return [("I", "I", 0)], succ, states


def rr_grant(last, req, n, fixed=False):
    """Index granted by a round-robin (or fixed-priority) arbiter, or None."""
    for k in range(1, n + 1):
        i = (k - 1) if fixed else (last + k) % n
        if req >> i & 1:
            return i
    return None


def arbiter_worst_wait(n, fixed=False, cap=None):
    """Exhaustive search over every request pattern (each idle requester may raise a request each cycle; a request is
    held until granted). Returns the largest number of grants to others that a pending requester ever sees, capped at
    `cap` (default 3n) so that unbounded starvation terminates."""
    cap = cap or 3 * n
    start = (n - 1, 0, (0,) * n)
    seen, q, worst = {start}, deque([start]), 0
    while q:
        last, pend, wait = q.popleft()
        idle = [i for i in range(n) if not pend >> i & 1]
        for m in range(1 << len(idle)):
            req = pend
            for b, i in enumerate(idle):
                if m >> b & 1:
                    req |= 1 << i
            g = rr_grant(last, req, n, fixed)
            nw = list(wait)
            for i in range(n):
                if g == i:
                    nw[i] = 0
                elif req >> i & 1 and g is not None:
                    nw[i] = min(nw[i] + 1, cap)
            worst = max(worst, max(nw))
            nxt = (g if g is not None else last, req & ~(1 << g) if g is not None else req, tuple(nw))
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return worst
