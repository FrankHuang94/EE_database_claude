#!/usr/bin/env python3
"""Verify every number in chapter 08-02 (Boolean algebra and logic gates), its solutions and its lab handout.

Independent routes, not the chapter's hand algebra:
- functions are evaluated row by row as Python callables and compared as truth-table integers;
- minimal SOP/POS literal counts come from an exhaustive search over all cubes (product terms) of the
  variables, choosing the cheapest set that covers the function exactly;
- minimal NAND/NOR gate counts come from an exhaustive search over straight-line gate programs;
- functional completeness is decided by computing the closure of the projections under composition;
- CMOS gates are simulated as series-parallel switch networks; transistor counts and stages are read
  from explicit gate-level netlists.
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
v = Verifier.from_files("08-02", COURSE / "chapters" / "08-02-boolean-algebra-and-gates.md",
                        COURSE / "solutions" / "08-02-solutions.md",
                        COURSE / "labs" / "08-02-lab" / "README.md")


# ---------------------------------------------------------------- truth-table helpers
def rows(n):
    """All input rows as tuples, row i = binary of i with the first variable most significant."""
    return [tuple((i >> (n - 1 - k)) & 1 for k in range(n)) for i in range(2 ** n)]


def lut(f, n):
    return sum(int(bool(f(*r))) << i for i, r in enumerate(rows(n)))


def ones(f, n):
    return sum(1 for r in rows(n) if f(*r))


def NOT(x):
    return 1 - x


# ---------------------------------------------------------------- exhaustive minimal SOP
def cubes(n):
    """Every product term: a tuple of 0 (complemented literal), 1 (true literal) or None (absent)."""
    return list(itertools.product((0, 1, None), repeat=n))


def cube_rows(c, n):
    return {i for i, r in enumerate(rows(n)) if all(ci is None or ci == ri for ci, ri in zip(c, r))}


def min_sop_literals(onset, n):
    """Fewest literals in any sum of products equal to the function with the given on-set.
    Only prime implicants need be considered: replacing a term by a prime that contains it covers at
    least as many rows with no more literals."""
    if not onset:
        return 0
    imps = [(c, cube_rows(c, n), sum(x is not None for x in c)) for c in cubes(n) if cube_rows(c, n) <= onset]
    primes = [m for m in imps if not any(o[1] > m[1] for o in imps)]
    best = math.inf
    for k in range(1, len(primes) + 1):
        for combo in itertools.combinations(primes, k):
            if set().union(*(rs for _, rs, _ in combo)) == onset:
                best = min(best, sum(lit for _, _, lit in combo))
    return best


def onset(f, n):
    return {i for i, r in enumerate(rows(n)) if f(*r)}


# ---------------------------------------------------------------- straight-line gate programs
def min_gates(op, inputs, target, nbits, max_gates=5):
    """Fewest 2-input gates `op` (on truth-table integers) computing target from the input tables."""
    mask = (1 << nbits) - 1
    if target in inputs:
        return 0
    frontier = [tuple(inputs)]
    for depth in range(1, max_gates + 1):
        nxt = set()
        for sigs in frontier:
            for i in range(len(sigs)):
                for j in range(i, len(sigs)):
                    g = op(sigs[i], sigs[j]) & mask
                    if g == target:
                        return depth
                    if g not in sigs:
                        nxt.add(tuple(sorted(sigs + (g,))))
        frontier = list(nxt)
    return None


def var_table(k, n):
    return lut(lambda *r: r[k], n)


nand = lambda a, b: ~(a & b)
nor = lambda a, b: ~(a | b)


# ---------------------------------------------------------------- gate-level netlists
TRANSISTORS = {"INV": 2, "NAND2": 4, "NOR2": 4, "NAND3": 6, "NOR3": 6, "AOI22": 8, "OAI21": 6, "AOI21": 6,
               "XOR2": 12}


def check_counts():
    # the table above follows the 2k rule: k input literals in the pull-down expression -> 2k transistors
    lits = {"INV": 1, "NAND2": 2, "NOR2": 2, "NAND3": 3, "NOR3": 3, "AOI22": 4, "OAI21": 3, "AOI21": 3}
    return all(TRANSISTORS[g] == 2 * k for g, k in lits.items())


v.assert_true("Gate transistor counts follow the 2k rule", check_counts())

EVAL = {"INV": lambda a: 1 - a, "NAND2": lambda a, b: 1 - (a & b), "NOR2": lambda a, b: 1 - (a | b),
        "NAND3": lambda a, b, c: 1 - (a & b & c), "NOR3": lambda a, b, c: 1 - (a | b | c),
        "AOI22": lambda a, b, c, d: 1 - ((a & b) | (c & d)), "XOR2": lambda a, b: a ^ b}


def run_netlist(net, inputs, out, n):
    """net: list of (name, gate, [input names]); returns (lookup integer, transistors, stages)."""
    tbl = 0
    for i, r in enumerate(rows(n)):
        val = dict(zip(inputs, r))
        for name, g, ins in net:
            val[name] = EVAL[g](*(val[x] for x in ins))
        tbl |= val[out] << i
    depth = {x: 0 for x in inputs}
    for name, g, ins in net:
        depth[name] = 1 + max(depth[x] for x in ins)
    return tbl, sum(TRANSISTORS[g] for _, g, _ in net), depth[out]


# ---------------------------------------------------------------- CMOS switch networks
def conducts(net, val, kind):
    """net: ('T', var) | ('S', [..]) series | ('P', [..]) parallel. nMOS ON at 1, pMOS ON at 0."""
    if net[0] == "T":
        return val[net[1]] == (1 if kind == "n" else 0)
    sub = [conducts(x, val, kind) for x in net[1]]
    return all(sub) if net[0] == "S" else any(sub)


def count_t(net):
    return 1 if net[0] == "T" else sum(count_t(x) for x in net[1])


def stack(net):
    if net[0] == "T":
        return 1
    sub = [stack(x) for x in net[1]]
    return sum(sub) if net[0] == "S" else max(sub)


def dual(net):
    if net[0] == "T":
        return net
    return ("P" if net[0] == "S" else "S", [dual(x) for x in net[1]])


def cmos_gate(pdn, names):
    """Returns (truth-table integer, transistor count, PDN stack, PUN stack, rows Y=1); checks complementarity."""
    pun = dual(pdn)
    n = len(names)
    tbl, up_rows = 0, 0
    for i, r in enumerate(rows(n)):
        val = dict(zip(names, r))
        down, up = conducts(pdn, val, "n"), conducts(pun, val, "p")
        assert down != up, f"networks not complementary at row {r}"
        tbl |= int(up) << i
        up_rows += up
    return tbl, count_t(pdn) + count_t(pun), stack(pdn), stack(pun), up_rows


# ---------------------------------------------------------------- closure (functional completeness)
def closure(ops, n=2, consts=()):
    """All n-input truth tables buildable from the projections (and constants) with the given ops."""
    mask = (1 << 2 ** n) - 1
    have = {var_table(k, n) for k in range(n)} | set(consts)
    while True:
        new = set()
        for op, arity in ops:
            for args in itertools.product(have, repeat=arity):
                t = op(*args) & mask
                if t not in have:
                    new.add(t)
        if not new:
            return have
        have |= new


# ================================================================= chapter: worked examples
A, B, C = (lambda a, b, c: a), (lambda a, b, c: b), (lambda a, b, c: c)
lhs = lambda a, b, c: (a & b) | (NOT(a) & c) | (b & c)
rhs = lambda a, b, c: (a & b) | (NOT(a) & c)
v.assert_true("Ex1 consensus holds on every row", lut(lhs, 3) == lut(rhs, 3))
v.check("Ex 08-02.1a", len(rows(3)))
v.check("Ex 08-02.1b", ones(lambda a, b, c: b & c, 3))

maj = lambda a, b, c: int(a + b + c >= 2)
v.check("Ex 08-02.2a", ones(maj, 3))
v.check("Ex 08-02.2b", 3 * ones(maj, 3))
v.check("Ex 08-02.2c", min_sop_literals(onset(maj, 3), 3))
v.check("Ex 08-02.2d", lut(maj, 3))
offset = set(range(8)) - onset(maj, 3)
v.check("Ex 08-02.2e", min_sop_literals(offset, 3))   # minimal POS of F = minimal SOP of its complement
v.assert_true("Ex2 majority is self-dual", all(maj(*r) == 1 - maj(*(1 - x for x in r)) for r in rows(3)))

F3 = lambda a, b, c, d: (NOT(a) & b) | (c & NOT(d))
v.check("Ex 08-02.3a", ones(F3, 4))
v.check("Ex 08-02.3b", 16 - ones(F3, 4))
pos3 = lambda a, b, c, d: (a | NOT(b)) & (NOT(c) | d)
v.assert_true("Ex3 De Morgan complement", lut(pos3, 4) == lut(lambda *r: 1 - F3(*r), 4))
v.check("Ex 08-02.3c", 4)   # literal count of (A + B')(C' + D), read off the expression checked above
sop3 = lambda a, b, c, d: (a & NOT(c)) | (a & d) | (NOT(b) & NOT(c)) | (NOT(b) & d)
v.assert_true("Ex3 expanded SOP equals the complement", lut(sop3, 4) == lut(pos3, 4))
v.assert_true("Ex3 the expanded SOP is minimal", min_sop_literals(onset(pos3, 4), 4) == 8)
v.check("Ex 08-02.3d", min_sop_literals(onset(pos3, 4), 4))

ab_cd = lambda a, b, c, d: (a & b) | (c & d)
I4 = ["A", "B", "C", "D"]
and_or = [("n1", "NAND2", ["A", "B"]), ("x1", "INV", ["n1"]), ("n2", "NAND2", ["C", "D"]), ("x2", "INV", ["n2"]),
          ("o", "NOR2", ["x1", "x2"]), ("Y", "INV", ["o"])]
nand_nand = [("n1", "NAND2", ["A", "B"]), ("n2", "NAND2", ["C", "D"]), ("Y", "NAND2", ["n1", "n2"])]
aoi = [("z", "AOI22", ["A", "B", "C", "D"]), ("Y", "INV", ["z"])]
res = {k: run_netlist(net, I4, "Y", 4) for k, net in (("ao", and_or), ("nn", nand_nand), ("aoi", aoi))}
v.assert_true("Ex4 all three circuits compute AB + CD", all(t == lut(ab_cd, 4) for t, _, _ in res.values()))
v.check("Ex 08-02.4a", res["ao"][1])
v.check("Ex 08-02.4b", res["nn"][1])
v.check("Ex 08-02.4c", res["aoi"][1])
v.check("Ex 08-02.4d", res["ao"][2])
v.check("Ex 08-02.4e", res["nn"][2])
v.check("Ex 08-02.4f", res["aoi"][2])

xor_net = [("M", "NAND2", ["A", "B"]), ("P", "NAND2", ["A", "M"]), ("Q", "NAND2", ["B", "M"]),
           ("Y", "NAND2", ["P", "Q"])]
t5, tr5, st5 = run_netlist(xor_net, ["A", "B"], "Y", 2)
v.assert_true("Ex5 four NANDs make XOR", t5 == lut(lambda a, b: a ^ b, 2))
v.check("Ex 08-02.5a", min_gates(nand, [var_table(0, 2), var_table(1, 2)], lut(lambda a, b: a ^ b, 2), 4))
v.check("Ex 08-02.5b", tr5)
v.check("Ex 08-02.5c", st5)
xor_aoi = [("na", "INV", ["A"]), ("nb", "INV", ["B"]), ("Y", "AOI22", ["A", "B", "na", "nb"])]
t5d, tr5d, _ = run_netlist(xor_aoi, ["A", "B"], "Y", 2)
v.assert_true("Ex5d AOI22 with inverted inputs is XOR", t5d == lut(lambda a, b: a ^ b, 2))
v.check("Ex 08-02.5d", tr5d)

oai = cmos_gate(("S", [("T", "A"), ("P", [("T", "B"), ("T", "C")])]), ["A", "B", "C"])
v.assert_true("Ex6 gate computes NOT(A(B+C))", oai[0] == lut(lambda a, b, c: 1 - (a & (b | c)), 3))
v.check("Ex 08-02.6a", oai[1])
v.check("Ex 08-02.6b", 8 - oai[4])
v.check("Ex 08-02.6c", oai[4])
v.check("Ex 08-02.6d", max(oai[2], oai[3]))

all2 = list(range(16))
v.check("Ex 08-02.7a", len(all2))


def depends_on(tbl, k, n):
    return any(((tbl >> i) & 1) != ((tbl >> (i ^ (1 << (n - 1 - k)))) & 1) for i in range(2 ** n))


v.check("Ex 08-02.7b", sum(1 for t in all2 if depends_on(t, 0, 2) and depends_on(t, 1, 2)))
v.check("Ex 08-02.7c", 2 ** (2 ** 4))
v.check("Ex 08-02.7d", float(2 ** (2 ** 6)))
v.check("Ex 08-02.7e", 2 ** 6)
cof0 = lambda b, c: maj(0, b, c)
cof1 = lambda b, c: maj(1, b, c)
v.assert_true("Ex7 cofactors are BC and B + C",
              lut(cof0, 2) == lut(lambda b, c: b & c, 2) and lut(cof1, 2) == lut(lambda b, c: b | c, 2))

v.check("Th 08-02.a", 2 ** (2 ** 3))
v.check("Th 08-02.b", 2 ** 20)
v.check("Th 08-02.c", 2.0 ** 64 / 1e9 / (365.25 * 86400))
v.check("Th 08-02.d", cmos_gate(("P", [("S", [("T", "A"), ("T", "B")]), ("S", [("T", "C"), ("T", "D")])]),
                                ["A", "B", "C", "D"])[1])
v.check("N 08-02.a", 2.0 ** 20 / 1e9 * 1e3)
v.check("N 08-02.b", 2.0 ** 40 / 1e9 / 60)
v.check("PL 08-02.a", 1.0 / 0.65)
v.check("PL 08-02.b", 24 / 4)
v.check("PL 08-02.c", 208 / 2)
v.check("PL 08-02.d", 208 / 28)
v.check("PL 08-02.e", 208 / 4)

# ================================================================= solutions
f1 = lambda a, b, c: (NOT(a) & b) | (a & NOT(c))
v.check("08-02.1a", lut(f1, 3))
v.check("08-02.1b", ones(f1, 3))
v.check("08-02.2a", len(rows(2)))
v.assert_true("P2 A + A'B = A + B on every row", lut(lambda a, b: a | (NOT(a) & b), 2) == lut(lambda a, b: a | b, 2))
v.assert_true("P2 (A + B)(A + C) = A + BC", lut(lambda a, b, c: (a | b) & (a | c), 3) == lut(lambda a, b, c: a | (b & c), 3))
F2 = lambda a, b, c, d: a & (b | (NOT(c) & d))
v.assert_true("P3 complement of F2", lut(lambda a, b, c, d: NOT(a) | (NOT(b) & (c | NOT(d))), 4)
              == lut(lambda *r: 1 - F2(*r), 4))
v.assert_true("P3 complement of F1", lut(lambda a, b, c: (NOT(a) & b) | NOT(c), 3)
              == lut(lambda a, b, c: 1 - ((a | NOT(b)) & c), 3))
v.check("08-02.3a", ones(F2, 4))
v.check("08-02.3b", 16 - ones(F2, 4))
p4 = {"a": (lambda a, b: (a & b) | (a & NOT(b)) | (NOT(a) & b), 2),
      "b": (lambda a, b: (a | b) & (a | NOT(b)), 2),
      "c": (lambda a, b, c: (NOT(a) & NOT(b) & NOT(c)) | (NOT(a) & b & NOT(c)) | (a & NOT(b) & NOT(c))
            | (a & b & NOT(c)), 3),
      "d": (lambda a, b, c: (a & b) | (b & NOT(c)) | (a & c), 3),
      "e": (lambda a, b, c: (NOT(a) & b & c) | (a & NOT(b) & c) | (a & b & NOT(c)) | (a & b & c), 3)}
for k, (f, n) in p4.items():
    v.check(f"08-02.4{k}", min_sop_literals(onset(f, n), n))
F5 = {0, 2, 3, 7}
v.check("08-02.5a", sum(1 << i for i in F5))
v.check("08-02.5b", sum(1 << i for i in set(range(8)) - F5))
v.check("08-02.5c", min_sop_literals(F5, 3))
v.check("08-02.5d", min_sop_literals(set(range(8)) - F5, 3))


def apply2(t):
    """The two-input function with 4-bit table t (bit index 2A + B), lifted to 4-bit tables of A and B."""
    return lambda x, y: sum((((t >> ((((x >> i) & 1) << 1) | ((y >> i) & 1))) & 1) << i) for i in range(4))


v.check("08-02.6a", sum(1 for t in range(16) if ((t >> 1) & 1) == ((t >> 2) & 1)))
v.check("08-02.6b", sum(1 for t in range(16) if depends_on(t, 0, 2) and depends_on(t, 1, 2)))
complete = [t for t in range(16) if len(closure([(apply2(t), 2)])) == 16]
v.assert_true("P6 the complete functions are NOR (0001) and NAND (0111)", complete == [1, 7])
v.check("08-02.6c", len(complete))

S3, D03, D13 = var_table(0, 3), var_table(1, 3), var_table(2, 3)
muxt = lut(lambda s, d0, d1: (NOT(s) & d0) | (s & d1), 3)
net7 = [("N1", "NAND2", ["S", "S"]), ("N2", "NAND2", ["N1", "D0"]), ("N3", "NAND2", ["S", "D1"]),
        ("Y", "NAND2", ["N2", "N3"])]
t7, tr7, st7 = run_netlist(net7, ["S", "D0", "D1"], "Y", 3)
v.assert_true("P7 NAND multiplexer is correct", t7 == muxt)
v.check("08-02.7a", min_gates(nand, [S3, D03, D13], muxt, 8))
v.check("08-02.7b", tr7)
v.check("08-02.7c", st7)
depth_d = {"S": -math.inf, "D0": 0, "D1": 0}     # longest path counted from the data inputs only
for name, g, ins in net7:
    depth_d[name] = 1 + max(depth_d[x] for x in ins)
v.check("08-02.7d", depth_d["Y"])
net8a = [("P", "NOR2", ["A", "B"]), ("Q", "NOR2", ["C", "D"]), ("Y", "NOR2", ["P", "Q"])]
t8a, tr8a, _ = run_netlist(net8a, I4, "Y", 4)
v.assert_true("P8a NOR-NOR computes (A+B)(C+D)", t8a == lut(lambda a, b, c, d: (a | b) & (c | d), 4))
v.check("08-02.8a", len(net8a))
v.check("08-02.8b", tr8a)
net8c = [("na", "NOR2", ["A", "A"]), ("nb", "NOR2", ["B", "B"]), ("nc", "NOR2", ["C", "C"]),
         ("nd", "NOR2", ["D", "D"]), ("ab", "NOR2", ["na", "nb"]), ("cd", "NOR2", ["nc", "nd"]),
         ("o", "NOR2", ["ab", "cd"]), ("Y", "NOR2", ["o", "o"])]
t8c, tr8c, st8c = run_netlist(net8c, I4, "Y", 4)
v.assert_true("P8c NOR-only circuit computes AB + CD", t8c == lut(ab_cd, 4))
v.check("08-02.8c", len(net8c))
v.check("08-02.8d", tr8c)
v.check("08-02.8e", st8c)
net9 = [("G1", "NAND2", ["A", "B"]), ("G2", "INV", ["C"]), ("Y", "NAND2", ["G1", "G2"])]
t9, _, _ = run_netlist(net9, ["A", "B", "C"], "Y", 3)
v.assert_true("P9 circuit is AB + C", t9 == lut(lambda a, b, c: (a & b) | c, 3))
v.check("08-02.9a", t9)
v.check("08-02.9b", bin(t9).count("1"))


def mux_tree(table, n):
    """Build a function from 2:1 muxes by Shannon expansion; returns (evaluator, mux count)."""
    if n == 0:
        return (lambda *r: table & 1), 0
    lo_t = sum(((table >> i) & 1) << i for i in range(2 ** (n - 1)))
    hi_t = sum(((table >> (i + 2 ** (n - 1))) & 1) << i for i in range(2 ** (n - 1)))
    lo, c0 = mux_tree(lo_t, n - 1)
    hi, c1 = mux_tree(hi_t, n - 1)
    return (lambda s, *r: hi(*r) if s else lo(*r)), c0 + c1 + 1


for n_in, key in ((3, "08-02.10a"), (6, "08-02.10b")):
    tbl = lut(lambda *r: sum(r) % 3 == 1, n_in)        # an arbitrary test function
    ev, cnt = mux_tree(tbl, n_in)
    v.assert_true(f"P10 mux tree reproduces a {n_in}-input function", lut(ev, n_in) == tbl)
    v.check(key, cnt)
ea, _ = mux_tree(lut(lambda a, b, c: a ^ b ^ c, 3), 3)
v.assert_true("P10 Shannon expansion of XOR3", all(
    (a ^ b ^ c) == ((NOT(a) & (b ^ c)) | (a & NOT(b ^ c))) for a, b, c in rows(3)))
v.assert_true("P10 expansion of the consensus function", lut(lambda a, b, c: (NOT(a) & c) | (a & b), 3) == lut(lhs, 3))

aoi21 = cmos_gate(("P", [("S", [("T", "A"), ("T", "B")]), ("T", "C")]), ["A", "B", "C"])
v.assert_true("P11 gate computes NOT(AB + C)", aoi21[0] == lut(lambda a, b, c: 1 - ((a & b) | c), 3))
v.assert_true("P11 input 110 gives Y = 0", not (aoi21[0] >> 6) & 1)
v.check("08-02.11a", aoi21[1])
v.check("08-02.11b", aoi21[4])
v.check("08-02.11c", max(aoi21[2], aoi21[3]))
n12 = {"a": [("n", "NAND3", ["A", "B", "C"]), ("Y", "INV", ["n"])],
       "b": [("n1", "NAND2", ["A", "B"]), ("x1", "INV", ["n1"]), ("n2", "NAND2", ["x1", "C"]), ("Y", "INV", ["n2"])],
       "c": [("na", "INV", ["A"]), ("nb", "INV", ["B"]), ("nc", "INV", ["C"]), ("Y", "NOR3", ["na", "nb", "nc"])]}
r12 = {k: run_netlist(net, ["A", "B", "C"], "Y", 3) for k, net in n12.items()}
v.assert_true("P12 all three compute ABC", all(t == 128 for t, _, _ in r12.values()))
for k, idt, ids in (("a", "08-02.12a", "08-02.12d"), ("b", "08-02.12b", "08-02.12e"), ("c", "08-02.12c", "08-02.12f")):
    v.check(idt, r12[k][1])
    v.check(ids, r12[k][2])
v.assert_true("P13 XOR is associative",
              lut(lambda a, b, c: (a ^ b) ^ c, 3) == lut(lambda a, b, c: a ^ (b ^ c), 3))
par_net = [("x1", "XOR2", ["A", "B"]), ("x2", "XOR2", ["C", "D"]), ("Y", "XOR2", ["x1", "x2"])]
t13, tr13, st13 = run_netlist(par_net, I4, "Y", 4)
v.assert_true("P13 XOR tree is 4-input parity", t13 == lut(lambda a, b, c, d: a ^ b ^ c ^ d, 4))
v.check("08-02.13a", len(par_net))
v.check("08-02.13b", st13)
v.check("08-02.13c", min_sop_literals(onset(lambda a, b, c, d: a ^ b ^ c ^ d, 4), 4))
v.check("08-02.13d", tr13)
L14 = lambda a, b, c: (NOT(a) & b) | (b & c) | (a & NOT(b) & NOT(c))
R14 = lambda a, b, c: (NOT(a) & b) | (b & c) | (a & NOT(c))
diff = [i for i, r in enumerate(rows(3)) if L14(*r) != R14(*r)]
v.assert_true("P14 exactly one differing row", len(diff) == 1)
v.check("08-02.14a", diff[0])
v.check("08-02.14b", lut(L14, 3))
v.check("08-02.14c", lut(R14, 3))
v.check("08-02.14d", 2.0 ** 50 / 1e9 / 86400)
v.check("08-02.14e", 2.0 ** 50 / 1e9)
v.check("08-02.14f", 2.0 ** 60 / 1e9 / (365.25 * 86400))
andor = closure([(lambda x, y: x & y, 2), (lambda x, y: x | y, 2)])
v.check("08-02.15a", len(andor))
v.assert_true("P15 XOR, AND and 1 are complete",
              len(closure([(lambda x, y: x ^ y, 2), (lambda x, y: x & y, 2)], consts=(15,))) == 16)
A2, B2 = var_table(0, 2), var_table(1, 2)
v.check("08-02.15c", min_gates(nand, [A2, B2], lut(lambda a, b: 1 - (a | b), 2), 4))
v.check("08-02.15d", min_gates(nor, [A2, B2], lut(lambda a, b: 1 - (a & b), 2), 4))

# ================================================================= lab handout
VDD = 1.8
nand_sw = cmos_gate(("S", [("T", "A"), ("T", "B")]), ["A", "B"])   # complementarity asserted inside
for i, key in enumerate(("Lab 08-02.a", "Lab 08-02.b", "Lab 08-02.c", "Lab 08-02.d")):
    v.check(key, VDD * ((nand_sw[0] >> i) & 1))
# settled current: a path from VDD to ground needs both networks on at once, which cmos_gate proved never happens
v.check("Lab 08-02.e", 0.0)
tables3 = range(256)


def tbit(t, r):
    return (t >> (4 * r[0] + 2 * r[1] + r[2])) & 1


sym = sum(1 for t in tables3 if all(tbit(t, r) == tbit(t, p) for r in rows(3)
                                     for p in itertools.permutations(r)))
selfdual = sum(1 for t in tables3 if all(tbit(t, r) == 1 - tbit(t, tuple(1 - x for x in r)) for r in rows(3)))
mono = sum(1 for t in tables3 if all(tbit(t, r) <= tbit(t, s) for r in rows(3) for s in rows(3)
                                     if all(x <= y for x, y in zip(r, s))))
v.check("Lab 08-02.f", sym)
v.check("Lab 08-02.g", selfdual)
v.check("Lab 08-02.h", mono)
v.assert_true("Lab: monotone functions are exactly those built from AND, OR and constants",
              mono == len(closure([(lambda x, y: x & y, 2), (lambda x, y: x | y, 2)], n=3, consts=(0, 255))))

v.finish()
