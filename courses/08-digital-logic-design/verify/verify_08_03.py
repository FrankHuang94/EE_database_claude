#!/usr/bin/env python3
"""Verify every number in chapter 08-03 (logic minimization), its solutions and its lab handout.

Independent routes, not the chapter's map-reading:
- prime implicants are found by enumerating all 3^n product terms and keeping the maximal ones inside
  the on-set plus don't-care set (no tabulation, no maps);
- minimum covers are found exactly by dynamic programming over subsets of the on-set, minimizing
  (terms, literals) lexicographically, and every minimum cover is enumerated to count ties;
- every expression published in the text is parsed into a Python function and compared row by row.
"""
from __future__ import annotations

import functools
import itertools
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-03", COURSE / "chapters" / "08-03-logic-minimization.md",
                        COURSE / "solutions" / "08-03-solutions.md",
                        COURSE / "labs" / "08-03-lab" / "README.md")


def rows(n):
    return [tuple((i >> (n - 1 - k)) & 1 for k in range(n)) for i in range(2 ** n)]


@functools.lru_cache(None)
def cubes(n):
    """(mask of covered rows, literal count, cube) for every product term in n variables."""
    out = []
    for c in itertools.product((0, 1, None), repeat=n):
        m = sum(1 << i for i, r in enumerate(rows(n)) if all(ci is None or ci == ri for ci, ri in zip(c, r)))
        out.append((m, sum(x is not None for x in c), c))
    return tuple(out)


def mask(idx):
    return sum(1 << i for i in idx)


def primes(on, dc, n):
    care = on | dc
    imps = [(m, lit, c) for m, lit, c in cubes(n) if m & ~care == 0 and m & on]
    return [p for p in imps if not any(q[0] != p[0] and q[0] & p[0] == p[0] for q in imps)]


def essentials(on, P):
    ess = []
    for p in P:
        for i in range(64):
            if (on >> i) & 1 and (p[0] >> i) & 1 and sum(1 for q in P if (q[0] >> i) & 1) == 1:
                ess.append(p)
                break
    return ess


def min_covers(on, dc, n, key=lambda t, l: (t, l)):
    """All minimum covers of the on-set by primes, cost = key(terms, literals)."""
    P = primes(on, dc, n)

    @functools.lru_cache(None)
    def best(rem):
        if rem == 0:
            return (0, 0)
        low = rem & -rem
        cands = []
        for m, lit, _ in P:
            if m & low:
                t, l = best(rem & ~m)
                cands.append((t + 1, l + lit))
        return min(cands, key=lambda tl: key(*tl))

    target = best(on)
    sols = set()

    def walk(rem, chosen):
        if rem == 0:
            sols.add(frozenset(chosen))
            return
        low = rem & -rem
        t0, l0 = best(rem)
        for m, lit, c in P:
            if m & low:
                t, l = best(rem & ~m)
                if (t + 1, l + lit) == (t0, l0):
                    walk(rem & ~m, chosen + [c])
    walk(on, [])
    # walk may revisit the same cover via different orders; also a cover may contain a redundant prime
    # chosen for a low bit already covered elsewhere — keep only covers whose cost equals the optimum
    sols = {s for s in sols if (len(s), sum(sum(x is not None for x in c) for c in s)) == target}
    return target, sols, P


def table_of(expr, n):
    return sum(int(bool(expr(*r))) << i for i, r in enumerate(rows(n)))


N = lambda x: 1 - x


def lits_of_cover(sol):
    return sum(sum(x is not None for x in c) for c in sol)


# ================================================================= chapter
on1 = mask([1, 3, 4, 5, 7])
(t, l), s, P = min_covers(on1, 0, 3)
v.assert_true("Ex1 C + AB' equals the function", table_of(lambda a, b, c: c | (a & N(b)), 3) == on1)
v.check("Ex 08-03.1a", t)
v.check("Ex 08-03.1b", l)
v.check("Ex 08-03.1c", 3 * bin(on1).count("1"))

on2 = mask([0, 2, 5, 7, 8, 10, 13, 15])
(t, l), s, P = min_covers(on2, 0, 4)
v.assert_true("Ex2 is XNOR(B, D)", table_of(lambda a, b, c, d: 1 - (b ^ d), 4) == on2)
v.check("Ex 08-03.2a", t)
v.check("Ex 08-03.2b", l)

on3 = mask([0, 1, 2, 5, 6, 7])
(t, l), s, P = min_covers(on3, 0, 3)
v.check("Ex 08-03.3a", len(P))
v.check("Ex 08-03.3b", len(essentials(on3, P)))
v.check("Ex 08-03.3c", l)
v.check("Ex 08-03.3d", len(s))
v.assert_true("Ex3 both published covers equal the function",
              table_of(lambda a, b, c: (N(a) & N(b)) | (b & N(c)) | (a & c), 3) == on3
              and table_of(lambda a, b, c: (N(a) & N(c)) | (N(b) & c) | (a & b), 3) == on3)

on4, dc4 = mask([5, 6, 7, 8, 9]), mask(range(10, 16))
(_, l_nodc), _, _ = min_covers(on4, 0, 4)
(_, l_dc), _, _ = min_covers(on4, dc4, 4)
v.check("Ex 08-03.4a", l_nodc)
v.check("Ex 08-03.4b", l_dc)
f4 = table_of(lambda a, b, c, d: a | (b & d) | (b & c), 4)
v.assert_true("Ex4 A + BD + BC is correct on the legal codes", f4 & mask(range(10)) == on4)
v.check("Ex 08-03.4c", bin(f4 & dc4).count("1"))

on5 = table_of(lambda a, b, c, d: (a | b) & (c | d), 4)
v.assert_true("Ex5 minterm list", on5 == mask([5, 6, 7, 9, 10, 11, 13, 14, 15]))
(_, l5), _, _ = min_covers(on5, 0, 4)
(_, l5p), _, _ = min_covers(0xFFFF & ~on5, 0, 4)       # minimal POS = minimal SOP of the complement
v.check("Ex 08-03.5a", l5)
v.check("Ex 08-03.5b", l5p)

on6 = mask([0, 4, 5, 7, 8, 9, 13, 15])
(t, l), s, P = min_covers(on6, 0, 4)
v.check("Ex 08-03.6a", len(P))
v.check("Ex 08-03.6b", len(essentials(on6, P)))
v.check("Ex 08-03.6c", l)
v.check("Ex 08-03.6d", len(s))
v.assert_true("Ex6 published cover", table_of(lambda a, b, c, d: (b & d) | (N(a) & N(c) & N(d)) | (a & N(b) & N(c)), 4) == on6)

f7 = lambda a, b, c, d, e: (a & d) | (a & e) | (b & d) | (b & e) | (c & d) | (c & e)
on7 = table_of(f7, 5)
v.assert_true("Ex7 factored form equals the SOP", table_of(lambda a, b, c, d, e: (a | b | c) & (d | e), 5) == on7)
(t7, l7), _, _ = min_covers(on7, 0, 5)
v.assert_true("Ex7 the six-term SOP is minimal", (t7, l7) == (6, 12))
v.check("Ex 08-03.7a", l7)


def stack(net):
    if net[0] == "T":
        return 1
    sub = [stack(x) for x in net[1]]
    return sum(sub) if net[0] == "S" else max(sub)


def dual(net):
    return net if net[0] == "T" else ("P" if net[0] == "S" else "S", [dual(x) for x in net[1]])


T = lambda x: ("T", x)
oai32_pdn = ("S", [("P", [T("A"), T("B"), T("C")]), ("P", [T("D"), T("E")])])
v.check("Ex 08-03.7e", max(stack(oai32_pdn), stack(dual(oai32_pdn))))


def leaves(net):
    return 1 if net[0] == "T" else sum(leaves(x) for x in net[1])


def gate_transistors(pdn):
    """A static CMOS gate: one nMOS per leaf in the pull-down, one pMOS per leaf in its dual."""
    return leaves(pdn) + leaves(dual(pdn))


def nand(k):
    return ("S", [T(f"x{i}") for i in range(k)])


inv = T("a")
_, sols7, _ = min_covers(on7, 0, 5)
terms7 = [sum(x is not None for x in c) for c in next(iter(sols7))]          # literals per product of the minimal SOP
v.check("Ex 08-03.7b", leaves(oai32_pdn))                         # literals of (A + B + C)(D + E)
v.check("Ex 08-03.7c", sum(gate_transistors(nand(k)) for k in terms7) + gate_transistors(nand(len(terms7))))
v.check("Ex 08-03.7d", gate_transistors(oai32_pdn) + gate_transistors(inv))
v.check("Ex 08-03.7f", stack(nand(len(terms7))))
v.check("Ex 08-03.7g", stack(oai32_pdn))
v.check("Th 08-03.a", len(cubes(4)))
v.check("Th 08-03.b", 2 ** (4 - 2))

# ================================================================= section 9
SNPS25, SNPS24, CDNS25, CDNS24, ANSYS = 7.054, 6.127, 5.297, 4.641, 0.7566
v.check("PL 08-03.a", SNPS25 + CDNS25)
v.check("PL 08-03.b", 100 * (SNPS25 / SNPS24 - 1))
v.check("PL 08-03.c", 100 * (CDNS25 / CDNS24 - 1))
v.check("PL 08-03.d", SNPS25 - ANSYS)
v.check("PL 08-03.e", 4 * 5.7108)
v.check("PL 08-03.f", 100 * ((SNPS25 - ANSYS) / SNPS24 - 1))

# ================================================================= solutions
for key, idx in (("08-03.1a", [0, 2, 4, 6]), ("08-03.1b", [2, 3, 6, 7])):
    v.check(key, min_covers(mask(idx), 0, 3)[0][1])
for key, idx in (("08-03.2a", [1, 3, 9, 11]), ("08-03.2b", [4, 6, 12, 14]),
                 ("08-03.2c", [0, 1, 2, 3, 8, 9, 10, 11]), ("08-03.2d", [8, 10])):
    m = mask(idx)
    cube = [c for cm, lit, c in cubes(4) if cm == m]
    v.assert_true(f"{key} group is a single product term", len(cube) == 1)
    v.check(key, sum(x is not None for x in cube[0]))
v.check("08-03.3a", min_covers(mask([0, 1, 3, 4, 5, 7]), 0, 3)[0][1])
on = mask([1, 3, 4, 5, 9, 11, 12, 13])
(t, l), s, P = min_covers(on, 0, 4)
v.check("08-03.4a", len(P))
v.check("08-03.4b", len(essentials(on, P)))
v.check("08-03.4c", l)
v.assert_true("P4 published cover", table_of(lambda a, b, c, d: (N(b) & d) | (b & N(c)), 4) == on)
on = mask([0, 1, 2, 3, 4, 6, 8, 9, 10, 11])
v.check("08-03.5a", min_covers(on, 0, 4)[0][1])
v.assert_true("P5 published cover", table_of(lambda a, b, c, d: N(b) | (N(a) & N(d)), 4) == on)
on = mask([0, 1, 2, 3, 4, 5, 6, 8, 10, 12])
v.check("08-03.6a", min_covers(on, 0, 4)[0][1])
v.check("08-03.6b", min_covers(0xFFFF & ~on, 0, 4)[0][1])
_, sols6, _ = min_covers(0xFFFF & ~on, 0, 4)
cover6 = next(iter(sols6))                                    # minimal SOP of F', i.e. F = NOT(sum of these)
v.assert_true("08-03.6: every literal of F' is uncomplemented, so F is one AOI gate on the true inputs",
              all(x in (None, 1) for c in cover6 for x in c))
aoi6 = ("P", [("S", [T(f"v{i}") for i, x in enumerate(c) if x is not None]) for c in cover6])
v.check("08-03.6c", gate_transistors(aoi6))
v.assert_true("P6 published POS", table_of(lambda a, b, c, d: (N(a) | N(d)) & (N(a) | N(b) | N(c)) & (N(b) | N(c) | N(d)), 4) == on)
seg = mask([0, 2, 3, 5, 6, 7, 8, 9])
v.check("08-03.7a", min_covers(seg, mask(range(10, 16)), 4)[0][1])
(t, l), s, _ = min_covers(seg, 0, 4)
v.check("08-03.7b", l)
v.check("08-03.7c", len(s))
fa = table_of(lambda a, b, c, d: a | c | (b & d) | (N(b) & N(d)), 4)
v.assert_true("P7 published segment-a logic is right on 0..9", fa & mask(range(10)) == seg)
v.check("08-03.7d", bin(fa & mask(range(10, 16))).count("1"))
on = mask([1, 3, 4, 5, 10, 11, 12, 13, 14, 15])
(t, l), s, P = min_covers(on, 0, 4)
v.check("08-03.8a", len(P))
v.check("08-03.8b", len(essentials(on, P)))
v.check("08-03.8c", l)
on = mask([0, 2, 3, 5, 7, 8, 10, 11, 13, 15])
(t, l), s, P = min_covers(on, 0, 4)
v.check("08-03.9a", len(P))
v.check("08-03.9b", len(essentials(on, P)))
v.check("08-03.9c", l)
v.check("08-03.9d", len(s))
f1, f2 = mask([2, 6, 7]), mask([2, 3, 6])
_, s1, _ = min_covers(f1, 0, 3)
_, s2, _ = min_covers(f2, 0, 3)
shared = min(len(a | b) for a in s1 for b in s2)
v.check("08-03.10a", shared)
v.check("08-03.10b", min(len(a) for a in s1) + min(len(b) for b in s2) - shared)
on, dc = mask([1, 3, 7, 11, 15]), mask([0, 2, 5])
(t, l), s, _ = min_covers(on, dc, 4)
v.check("08-03.11a", l)
v.check("08-03.11b", len(s))
v.check("08-03.11c", min_covers(on, 0, 4)[0][1])
g1 = table_of(lambda a, b, c, d: (c & d) | (N(a) & N(b)), 4)
g2 = table_of(lambda a, b, c, d: (c & d) | (N(a) & d), 4)
v.assert_true("P11 the two covers agree on the care set and differ on don't cares",
              (g1 ^ g2) & ~dc == 0 and (g1 ^ g2) != 0)
on12 = mask([0, 2, 5, 8, 10, 16, 18, 21, 24, 26])
v.check("08-03.12a", min_covers(on12, 0, 5)[0][1])
v.assert_true("P12 published cover", table_of(lambda a, b, c, d, e: (N(c) & N(e)) | (N(b) & c & N(d) & e), 5) == on12)
on = mask([0, 1, 5, 7, 8, 10, 14, 15])
(t, l), s, P = min_covers(on, 0, 4)
v.assert_true("P13 every prime covers exactly two minterms", all(bin(m).count("1") == 2 for m, _, _ in P))
v.check("08-03.13a", len(P))
v.check("08-03.13b", len(essentials(on, P)))
v.check("08-03.13c", len(s))
v.check("08-03.13d", l)
f14 = lambda a, b, c, d, e, f: (a | b) & (c | d) & (e | f)
on14 = table_of(f14, 6)
(t14, l14), _, _ = min_covers(on14, 0, 6)
v.check("08-03.14a", l14)
oai222_pdn = ("S", [("P", [T("A"), T("B")]), ("P", [T("C"), T("D")]), ("P", [T("E"), T("F")])])
_, sols14, _ = min_covers(on14, 0, 6)
terms14 = [sum(x is not None for x in c) for c in next(iter(sols14))]
v.check("08-03.14b", leaves(oai222_pdn))
v.check("08-03.14c", sum(gate_transistors(nand(k)) for k in terms14) + gate_transistors(nand(len(terms14))))
v.check("08-03.14d", gate_transistors(oai222_pdn) + gate_transistors(inv))
v.check("08-03.14e", 8)
oai222 = ("S", [("P", [T("A"), T("B")]), ("P", [T("C"), T("D")]), ("P", [T("E"), T("F")])])
v.check("08-03.14f", max(stack(oai222), stack(dual(oai222))))
v.check("08-03.15a", 3 ** 10)
v.check("08-03.15b", float(3 ** 20))
par = table_of(lambda a, b, c, d: a ^ b ^ c ^ d, 4)
two = table_of(lambda a, b, c, d: int(a + b + c + d == 2), 4)
v.check("08-03.15c", len(primes(par, 0, 4)))
v.check("08-03.15d", min_covers(par, 0, 4)[0][1])
v.check("08-03.15e", len(primes(two, 0, 4)))
v.check("08-03.15f", min_covers(two, 0, 4)[0][1])
v.check("08-03.15g", float(2 ** 40))
v.check("08-03.15h", 2 ** 40 / 1e9)
v.check("08-03.15i", 2 ** 60 / 1e9 / (365.25 * 86400))
v.assert_true("P15 product-term count formula matches enumeration for n = 4", len(cubes(4)) == 3 ** 4)

# ================================================================= lab handout
lit0 = lit1 = 0
for vals in itertools.product((0, 1, 2), repeat=8):
    on = sum(1 << i for i, x in enumerate(vals) if x == 1)
    dc = sum(1 << i for i, x in enumerate(vals) if x == 2)
    lit0 += min_covers(on, 0, 3, key=lambda t, l: (l, t))[0][1]
    lit1 += min_covers(on, dc, 3, key=lambda t, l: (l, t))[0][1]
NF = 3 ** 8
v.check("Lab 08-03.a", NF)
v.check("Lab 08-03.b", lit0 / NF)
v.check("Lab 08-03.c", lit1 / NF)
v.check("Lab 08-03.d", 100 * (1 - lit1 / lit0))
canon = table_of(lambda a, b, c, d: int(8 * a + 4 * b + 2 * c + d in (5, 6, 7, 8, 9)), 4)
nodc = table_of(lambda a, b, c, d: (N(a) & b & d) | (N(a) & b & c) | (a & N(b) & N(c)), 4)
wdc = table_of(lambda a, b, c, d: a | (b & d) | (b & c), 4)
v.assert_true("Lab: the three BCD circuits agree on 0..9", len({x & mask(range(10)) for x in (canon, nodc, wdc)}) == 1)
v.check("Lab 08-03.e", bin(canon & mask(range(10, 16))).count("1"))
v.check("Lab 08-03.f", bin(nodc & mask(range(10, 16))).count("1"))
v.check("Lab 08-03.g", bin(wdc & mask(range(10, 16))).count("1"))

v.finish()
