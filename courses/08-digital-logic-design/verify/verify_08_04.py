#!/usr/bin/env python3
"""Verify every number in chapter 08-04 (combinational building blocks), its solutions and its lab handout.

Independent routes:
- blocks (multiplexers, decoders, priority encoders, adders, comparators, an ALU) are simulated bit by bit
  and compared with their specifications on every input;
- delays come from static timing analysis of explicit gate netlists (arrival time = 1 + latest input);
- hazards and glitch statistics come from a unit-delay simulation in which every gate output at time t is
  its function of the gate inputs at time t - 1, run on all input transitions at once with NumPy.
"""
from __future__ import annotations

import functools
import itertools
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-04", COURSE / "chapters" / "08-04-combinational-building-blocks.md",
                        COURSE / "solutions" / "08-04-solutions.md",
                        COURSE / "labs" / "08-04-lab" / "README.md")

OPS = {"and": lambda *x: int(all(x)), "or": lambda *x: int(any(x)), "xor": lambda a, b: a ^ b,
       "not": lambda a: 1 - a, "nand": lambda *x: 1 - int(all(x)), "nor": lambda *x: 1 - int(any(x)),
       "buf": lambda a: a}


def arrival(net, inputs, delays=None, start=None):
    """Static timing: arrival time of every signal. delays maps gate type to delay (default 1)."""
    t = dict(start or {}) or {x: 0 for x in inputs}
    for x in inputs:
        t.setdefault(x, 0)
    for out, op, ins in net:
        t[out] = (delays or {}).get(op, 1) + max(t[i] for i in ins)
    return t


def evaluate(net, vals):
    v_ = dict(vals)
    for out, op, ins in net:
        v_[out] = OPS[op](*(v_[i] for i in ins))
    return v_


def rca_net(n, cin="c0"):
    net = []
    carry = cin
    for i in range(n):
        net += [(f"p{i}", "xor", [f"a{i}", f"b{i}"]), (f"g{i}", "and", [f"a{i}", f"b{i}"]),
                (f"s{i}", "xor", [f"p{i}", carry]), (f"q{i}", "and", [f"p{i}", carry]),
                (f"c{i + 1}", "or", [f"g{i}", f"q{i}"])]
        carry = f"c{i + 1}"
    return net


def rca_inputs(n, cin="c0"):
    return [f"a{i}" for i in range(n)] + [f"b{i}" for i in range(n)] + [cin]


v.assert_true("ripple adder netlist adds correctly (4 bits, exhaustive)", all(
    sum(evaluate(rca_net(4), {**{f"a{i}": (a >> i) & 1 for i in range(4)}, **{f"b{i}": (b >> i) & 1 for i in range(4)},
                              "c0": c})[f"s{i}"] << i for i in range(4))
    + 16 * evaluate(rca_net(4), {**{f"a{i}": (a >> i) & 1 for i in range(4)},
                                 **{f"b{i}": (b >> i) & 1 for i in range(4)}, "c0": c})["c4"] == a + b + c
    for a in range(16) for b in range(16) for c in (0, 1)))


def rca_delay(n):
    t = arrival(rca_net(n), rca_inputs(n))
    return max(t[f"s{i}"] for i in range(n)), t[f"c{n}"]


def mux_tree_count(k):
    return 0 if k == 0 else 2 ** (k - 1) + mux_tree_count(k - 1)


def addsub(a, b, sub, n):
    """Bit-level add/subtract unit: returns (unsigned result, signed result, carry out, overflow, N)."""
    m = (1 << n) - 1
    bb = (b ^ (m if sub else 0)) & m
    c, cs, s = sub, [sub], 0
    for i in range(n):
        ai, bi = (a >> i) & 1, (bb >> i) & 1
        s |= (ai ^ bi ^ c) << i
        c = (ai & bi) | (c & (ai ^ bi))
        cs.append(c)
    sv = s - (1 << n) if s >> (n - 1) else s
    return s, sv, cs[n], cs[n] ^ cs[n - 1], s >> (n - 1)


def unit_delay_trace(net, inputs, before, after, steps=12):
    """Unit-delay simulation: settle on `before`, switch to `after` at t = 0; return {signal: [values t=0..]}"""
    state = evaluate(net, before)
    for _ in range(len(net)):
        state = evaluate(net, {**state, **{k: before[k] for k in inputs}})
    cur = {**state, **after}
    hist = {k: [cur[k]] for k in cur}
    for _ in range(steps):
        nxt = dict(cur)
        for out, op, ins in net:
            nxt[out] = OPS[op](*(cur[i] for i in ins))
        cur = nxt
        for k in cur:
            hist[k].append(cur[k])
    return hist


def glitch(hist, sig, steady):
    """(start time, width) of the first excursion of `sig` away from `steady`, or None."""
    h = hist[sig]
    bad = [t for t, x in enumerate(h) if x != steady]
    if not bad:
        return None
    return bad[0], len(bad)


# ================================================================= chapter
def mux_eval(sel, data):
    return data[sel]


F1 = {1, 2, 6, 7}
dat = []
for ab in range(4):
    lo, hi = (2 * ab) in F1, (2 * ab + 1) in F1
    dat.append({(0, 0): "0", (1, 1): "1", (0, 1): "C", (1, 0): "C'"}[(lo, hi)])
v.assert_true("Ex1 data inputs C, C', 0, 1", dat == ["C", "C'", "0", "1"])
v.check("Ex 08-04.1a", mux_tree_count(3))
v.check("Ex 08-04.1b", 4 * 2 * 3 + 2 * 4 + 2 * 2)
S_on = [m for m in range(8) if bin(m).count("1") % 2 == 1]
C_on = [m for m in range(8) if bin(m).count("1") >= 2]
v.check("Ex 08-04.2a", len(S_on))
v.check("Ex 08-04.2b", len(set(S_on) & set(C_on)))


def prio(d, n):
    for k in range(n - 1, -1, -1):
        if (d >> k) & 1:
            return k
    return None


counts = {k: sum(1 for d in range(16) if prio(d, 4) == k) for k in (3, 2, 1, 0, None)}
for key, k in (("Ex 08-04.3a", 3), ("Ex 08-04.3b", 2), ("Ex 08-04.3c", 1), ("Ex 08-04.3d", 0), ("Ex 08-04.3e", None)):
    v.check(key, counts[k])
d = 0b0110
Y1 = ((d >> 3) & 1) | ((d >> 2) & 1)
Y0 = ((d >> 3) & 1) | ((1 - ((d >> 2) & 1)) & ((d >> 1) & 1))
v.assert_true("Ex3 equations equal the priority definition on all inputs", all(
    (((x >> 3) & 1) | ((x >> 2) & 1)) * 2 + (((x >> 3) & 1) | ((1 - ((x >> 2) & 1)) & ((x >> 1) & 1)))
    == (prio(x, 4) or 0) for x in range(16)))
v.check("Ex 08-04.3f", 2 * Y1 + Y0)
v.check("Ex 08-04.4a", rca_delay(4)[0])
v.check("Ex 08-04.4b", rca_delay(32)[0])
v.check("Ex 08-04.4c", rca_delay(64)[0])
v.check("Ex 08-04.4d", rca_delay(32)[1])
v.check("Ex 08-04.4e", 15 * rca_delay(64)[0])
v.check("Ex 08-04.4f", 15 * rca_delay(64)[0] / 500)
v.assert_true("RCA delays follow 2n and 2n + 1", all(rca_delay(n) == (2 * n, 2 * n + 1) for n in range(1, 40)))
r = addsub(5, 7, 1, 4)
v.check("Ex 08-04.5a", r[1])
v.check("Ex 08-04.5b", r[2])
v.check("Ex 08-04.5c", r[3])
r = addsub(6, (-3) & 15, 1, 4)
v.check("Ex 08-04.5d", r[1])
v.check("Ex 08-04.5e", r[3])
r = addsub(0b1011, 0b1101, 1, 4)
v.check("Ex 08-04.6a", r[2])
v.check("Ex 08-04.6b", r[4] ^ r[3])
v.assert_true("signed less-than is N xor V for all 4-bit pairs", all(
    (addsub(a & 15, b & 15, 1, 4)[4] ^ addsub(a & 15, b & 15, 1, 4)[3]) == int(a < b)
    for a in range(-8, 8) for b in range(-8, 8)))
v.assert_true("unsigned less-than is NOT carry for all 4-bit pairs", all(
    (1 - addsub(a, b, 1, 4)[2]) == int(a < b) for a in range(16) for b in range(16)))
v.check("Ex 08-04.6c", 32)
v.check("Ex 08-04.6d", math.ceil(math.log2(32)))

mux_net = [("sn", "not", ["s"]), ("t0", "and", ["sn", "d0"]), ("t1", "and", ["s", "d1"]), ("y", "or", ["t0", "t1"])]
fix_net = mux_net[:-1] + [("t2", "and", ["d0", "d1"]), ("y", "or", ["t0", "t1", "t2"])]
ins = ["s", "d0", "d1"]
h = unit_delay_trace(mux_net, ins, {"s": 1, "d0": 1, "d1": 1}, {"s": 0, "d0": 1, "d1": 1})
g = glitch(h, "y", 1)
v.check("Ex 08-04.7a", g[0])
v.check("Ex 08-04.7b", g[1])
v.assert_true("Ex7 no glitch when S rises", glitch(unit_delay_trace(mux_net, ins, {"s": 0, "d0": 1, "d1": 1},
                                                                       {"s": 1, "d0": 1, "d1": 1}), "y", 1) is None)
v.assert_true("Ex7 consensus term removes the glitch", all(
    glitch(unit_delay_trace(fix_net, ins, {"s": a, "d0": 1, "d1": 1}, {"s": 1 - a, "d0": 1, "d1": 1}), "y", 1) is None
    for a in (0, 1)))
v.check("Ex 08-04.7c", 6)
v.check("Th 08-04.a", mux_tree_count(6))
v.check("Th 08-04.b", 2 ** 6)
v.check("N 08-04.a", 50 / 30)
v.check("N 08-04.b", 63 / 30)

# ================================================================= solutions
v.check("08-04.1a", 0b101)
v.check("08-04.1b", 8)
v.check("08-04.1c", 3 + 1)
v.check("08-04.1d", mux_tree_count(3))
F2 = {0, 3, 5, 6}
dat2 = [{(0, 0): "0", (1, 1): "1", (0, 1): "C", (1, 0): "C'"}[((2 * ab) in F2, (2 * ab + 1) in F2)] for ab in range(4)]
v.assert_true("P2 data inputs C', C, C, C'", dat2 == ["C'", "C", "C", "C'"])
v.check("08-04.2a", dat2.count("C'"))


def dec24(e, a1, a0):
    return [e & (1 - a1) & (1 - a0), e & (1 - a1) & a0, e & a1 & (1 - a0), e & a1 & a0]


v.assert_true("P3 decoder is one-hot when enabled and all-zero when not", all(
    sum(dec24(1, a1, a0)) == 1 and dec24(1, a1, a0)[2 * a1 + a0] == 1 and sum(dec24(0, a1, a0)) == 0
    for a1 in (0, 1) for a0 in (0, 1)))
v.check("08-04.3a", dec24(1, 1, 0).index(1))
v.check("08-04.3b", 4 * (6 + 2) + 2 * 2)
v.check("08-04.4a", 4 * 4)
v.check("08-04.4b", 1 + 4)
pre = [("n3", "not", ["a3"]), ("n2", "not", ["a2"]), ("n1", "not", ["a1"]), ("n0", "not", ["a0"]),
       ("h", "and", ["a3", "n2"]), ("l", "and", ["n1", "a0"]), ("y9", "and", ["h", "l"])]
tree = [("n3", "not", ["a3"]), ("n2", "not", ["a2"]), ("n1", "not", ["a1"]), ("n0", "not", ["a0"]),
        ("e2", "and", ["one", "a3", "n2"]), ("y9", "and", ["e2", "n1", "a0"])]
v.check("08-04.4c", arrival(pre, ["a3", "a2", "a1", "a0"])["y9"])
v.check("08-04.4d", arrival(tree, ["a3", "a2", "a1", "a0", "one"])["y9"])


def y8(d):
    D = [(d >> k) & 1 for k in range(8)]
    N_ = lambda x: 1 - x
    y2 = D[7] | D[6] | D[5] | D[4]
    y1 = D[7] | D[6] | (N_(D[5]) & N_(D[4]) & (D[3] | D[2]))
    y0 = D[7] | (N_(D[6]) & D[5]) | (N_(D[6]) & N_(D[4]) & D[3]) | (N_(D[6]) & N_(D[4]) & N_(D[2]) & D[1])
    return 4 * y2 + 2 * y1 + y0


v.assert_true("P5 equations equal the priority definition on all 256 inputs",
              all(y8(d) == (prio(d, 8) or 0) for d in range(256)))
v.check("08-04.5a", y8(0b01010010))
v.check("08-04.5b", sum(1 for d in range(256) if prio(d, 8) == 5))


def min_sop_literals(on, n):
    rows_ = [tuple((i >> (n - 1 - k)) & 1 for k in range(n)) for i in range(2 ** n)]
    imps = []
    for c in itertools.product((0, 1, None), repeat=n):
        m = frozenset(i for i, r in enumerate(rows_) if all(ci is None or ci == ri for ci, ri in zip(c, r)))
        if m and m <= on:
            imps.append((m, sum(x is not None for x in c)))
    primes = [p for p in imps if not any(q[0] > p[0] for q in imps)]
    best = math.inf
    for k in range(1, len(primes) + 1):
        for combo in itertools.combinations(primes, k):
            if frozenset().union(*(m for m, _ in combo)) == on:
                best = min(best, sum(l for _, l in combo))
    return best


v.check("08-04.6a", min_sop_literals(frozenset(C_on), 3))
v.check("08-04.6b", min_sop_literals(frozenset(S_on), 3))
v.check("08-04.6c", len(rca_net(1)))
dl = {"xor": 40, "and": 25, "or": 25}
t8 = arrival(rca_net(8), rca_inputs(8), delays=dl)
v.check("08-04.7a", t8["s7"])
v.check("08-04.7b", t8["c8"])
v.check("08-04.7c", 1e3 / (t8["c8"] + 60))
for keys, (a, b) in ((("08-04.8a", "08-04.8b", "08-04.8c"), (100, 27)), (("08-04.8d", "08-04.8e", "08-04.8f"), (-100, 50)),
                     (("08-04.8g", "08-04.8h", "08-04.8i"), (50, 100))):
    r = addsub(a & 255, b & 255, 1, 8)
    v.check(keys[0], r[1])
    v.check(keys[1], r[2])
    v.check(keys[2], r[3])
gt_on = frozenset(i for i in range(16) if (i >> 2) > (i & 3))
v.check("08-04.9a", min_sop_literals(gt_on, 4))
v.assert_true("P9 published GT expression", all(
    ((((i >> 3) & 1) & (1 - ((i >> 1) & 1))) | (((i >> 3) & 1) & ((i >> 2) & 1) & (1 - (i & 1)))
     | (((i >> 2) & 1) & (1 - ((i >> 1) & 1)) & (1 - (i & 1)))) == int(i in gt_on) for i in range(16)))
r = addsub(0b1001, 0b0111, 0, 4)
v.check("08-04.10a", r[0])
v.check("08-04.10b", int(r[0] == 0))
v.check("08-04.10c", r[2])
v.check("08-04.10d", r[3])
ov = 0
for key, (a, b) in (("08-04.11a", (3, -2)), ("08-04.11b", (-8, 7)), ("08-04.11c", (7, -8))):
    r = addsub(a & 15, b & 15, 1, 4)
    v.check(key, r[4] ^ r[3])
    ov += r[3]
v.check("08-04.11d", ov)
f12 = [("an", "not", ["a"]), ("t0", "and", ["an", "b"]), ("t1", "and", ["a", "c"]), ("y", "or", ["t0", "t1"])]
g12 = glitch(unit_delay_trace(f12, ["a", "b", "c"], {"a": 1, "b": 1, "c": 1}, {"a": 0, "b": 1, "c": 1}), "y", 1)
v.assert_true("P12 no glitch when A rises",
              glitch(unit_delay_trace(f12, ["a", "b", "c"], {"a": 0, "b": 1, "c": 1}, {"a": 1, "b": 1, "c": 1}), "y", 1) is None)
v.check("08-04.12a", g12[0])
v.check("08-04.12b", g12[1])
v.check("08-04.12c", 6)
f13 = [("an", "not", ["a"]), ("u0", "or", ["a", "b"]), ("u1", "or", ["an", "c"]), ("y", "and", ["u0", "u1"])]
g13 = glitch(unit_delay_trace(f13, ["a", "b", "c"], {"a": 0, "b": 0, "c": 0}, {"a": 1, "b": 0, "c": 0}), "y", 0)
v.assert_true("P13 no glitch when A falls",
              glitch(unit_delay_trace(f13, ["a", "b", "c"], {"a": 1, "b": 0, "c": 0}, {"a": 0, "b": 0, "c": 0}), "y", 0) is None)
f13fix = f13[:-1] + [("u2", "or", ["b", "c"]), ("y", "and", ["u0", "u1", "u2"])]
v.assert_true("P13 consensus sum removes the glitch", all(glitch(unit_delay_trace(
    f13fix, ["a", "b", "c"], {"a": x, "b": 0, "c": 0}, {"a": 1 - x, "b": 0, "c": 0}), "y", 0) is None for x in (0, 1)))
v.check("08-04.13a", g13[1])
v.check("08-04.13b", 6)
# carry-select adder: low RCA4 from c0; two high RCA4 with constant carry ins; muxes as 1-unit gates
low = arrival(rca_net(4), rca_inputs(4))
hi = arrival(rca_net(4, "k"), rca_inputs(4, "k"))
v.check("08-04.14a", low["c4"])
v.check("08-04.14b", max(max(hi[f"s{i}"] for i in range(4)), hi["c4"]))
t_cs = 1 + max(low["c4"], max(hi[f"s{i}"] for i in range(4)), hi["c4"])
v.check("08-04.14c", t_cs)
v.check("08-04.14d", rca_delay(8)[1])
v.check("08-04.14e", 3 * 4)
v.check("08-04.14f", 4 + 1)
v.check("08-04.14g", rca_delay(8)[1] / t_cs)

# ================================================================= glitch census (lab and Problem 15)
n = 4
gates = [(o, op, ins_) for o, op, ins_ in rca_net(n)]
inputs = rca_inputs(n)
outs = [f"s{i}" for i in range(n)] + [f"c{n}"]
NPAT = 2 ** (2 * n + 1)
old = np.repeat(np.arange(NPAT), NPAT)
new = np.tile(np.arange(NPAT), NPAT)
NPF = {"xor": np.bitwise_xor, "and": np.bitwise_and, "or": np.bitwise_or}


def vec_settle(vals):
    st = dict(vals)
    for _ in range(len(gates)):
        for o, op, (x, y) in gates:
            st[o] = NPF[op](st[x], st[y])
    return st


oldv = {name: ((old >> k) & 1).astype(np.uint8) for k, name in enumerate(inputs)}
newv = {name: ((new >> k) & 1).astype(np.uint8) for k, name in enumerate(inputs)}
start = vec_settle(oldv)
cur = {**start, **newv}
trans = {o: np.zeros(NPAT * NPAT, dtype=np.int32) for o in outs}
last = {o: np.zeros(NPAT * NPAT, dtype=np.int32) for o in outs}
for step in range(1, 4 * n + 4):
    nxt = dict(cur)
    for o, op, (x, y) in gates:
        nxt[o] = NPF[op](cur[x], cur[y])
    for o in outs:
        ch = nxt[o] != cur[o]
        trans[o] += ch
        last[o] = np.where(ch, step, last[o])
    cur = nxt
final_ok = np.all(sum(cur[f"s{i}"].astype(int) << i for i in range(n)) + (cur[f"c{n}"].astype(int) << n)
                  == (new & 15) + ((new >> 4) & 15) + ((new >> 8) & 1))
v.assert_true("glitch census: every transition settles to the right sum", bool(final_ok))
need = {o: (start[o] != cur[o]).astype(np.int32) for o in outs}
total = sum(trans[o] for o in outs)
needed = sum(need[o] for o in outs)
v.check("Lab 08-04.a", NPAT * NPAT)
v.check("Lab 08-04.b", max(int(last[o].max()) for o in outs[:-1]))
v.check("Lab 08-04.c", int(last[outs[-1]].max()))
v.check("Lab 08-04.d", 100 * float(np.mean(np.any(np.stack([trans[o] > need[o] for o in outs]), axis=0))))
v.check("Lab 08-04.e", float(np.mean(total)))
v.check("Lab 08-04.f", float(np.mean(total - needed)))
v.check("Lab 08-04.g", 100 * (1 - float(needed.sum()) / float(total.sum())))
v.check("08-04.15a", float(np.mean(needed)))
v.check("08-04.15b", 100 * (1 - 2.5 / float(np.mean(total))))
v.check("Lab 08-04.h", 16 * 16 * 6)

v.finish()
