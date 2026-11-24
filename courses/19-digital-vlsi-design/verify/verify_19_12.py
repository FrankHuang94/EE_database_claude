#!/usr/bin/env python3
"""Verify every number in chapter 19-12 (design for test), its problems and its lab.

Independent routes:
- fault simulation by bit-parallel evaluation (each signal is an integer whose bits are its values over all input
  vectors), not the lab's vector-by-vector simulator; equivalence classes and minimal test sets from the resulting
  detection masks by exhaustive search;
- LFSR periods as the multiplicative order of x modulo the feedback polynomial over GF(2);
- MISR aliasing from the rank over GF(2) of the linear map from error streams to signatures;
- memory tests with a separately written cell model and March interpreter;
- scan cycles by stepping through the shift and capture phases; arithmetic quantities directly.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-12-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import dft  # noqa: E402

v = Verifier.from_files("19-12", ROOT / "chapters" / "19-12-design-for-test.md",
                        ROOT / "solutions" / "19-12-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- bit-parallel fault simulation
def bitpar(inputs, gates, outputs):
    """Return (fault list, {fault: detection mask}) with every signal as a 2^n-bit integer."""
    n = len(inputs)
    width = 1 << n
    full = (1 << width) - 1
    base = {}
    for k, name in enumerate(inputs):
        # bit j of the mask is input k's value in vector j (vector j = binary digits, first input most significant)
        m = 0
        for j in range(width):
            if (j >> (n - 1 - k)) & 1:
                m |= 1 << j
        base[name] = m
    fanout = {}
    for g, _, ins in gates:
        for pin, src in enumerate(ins):
            fanout.setdefault(src, []).append((g, pin))

    def run(fault=None):
        val = dict(base)
        if fault and fault[0] in val:
            val[fault[0]] = full if fault[1] else 0
        for g, typ, ins in gates:
            args = []
            for pin, src in enumerate(ins):
                x = val[src]
                if fault and fault[0] == (g, pin):
                    x = full if fault[1] else 0
                args.append(x)
            if typ in ("AND", "NAND"):
                r = full
                for a in args:
                    r &= a
            elif typ in ("OR", "NOR"):
                r = 0
                for a in args:
                    r |= a
            elif typ in ("XOR", "XNOR"):
                r = 0
                for a in args:
                    r ^= a
            else:
                r = args[0]
            if typ in ("NAND", "NOR", "XNOR", "NOT"):
                r ^= full
            val[g] = (full if fault[1] else 0) if fault and fault[0] == g else r
        return [val[o] for o in outputs]

    good = run()
    faults = []
    for s in list(inputs) + [g for g, _, _ in gates]:
        faults += [(s, 0), (s, 1)]
        if len(fanout.get(s, [])) > 1:
            for br in fanout[s]:
                faults += [(br, 0), (br, 1)]
    masks = {}
    for f in faults:
        bad = run(f)
        d = 0
        for a, b in zip(good, bad):
            d |= a ^ b
        masks[f] = d
    return faults, masks, width


def min_tests(masks, width):
    need = [m for m in masks.values() if m]
    for k in range(1, 10):
        for combo in itertools.combinations(range(width), k):
            sel = 0
            for j in combo:
                sel |= 1 << j
            if all(m & sel for m in need):
                return k
    return None


# Example 2: AB + CD from three NAND2 gates
f2, m2, w2 = bitpar(list("ABCD"), [("x", "NAND", ["A", "B"]), ("y", "NAND", ["C", "D"]), ("F", "NAND", ["x", "y"])], ["F"])
v.check("Ex 19-12.2a", len(f2))
v.check("Ex 19-12.2b", len(set(m2.values())))
v.check("Ex 19-12.2c", min_tests(m2, w2))
v.check("Ex 19-12.2d", 100 * len(set(m2.values())) / len(f2))
# Example 3: the consensus circuit
g3 = [("nA", "NOT", ["A"]), ("g1", "AND", ["A", "B"]), ("g2", "AND", ["nA", "C"]), ("g3", "AND", ["B", "C"]),
      ("F", "OR", ["g1", "g2", "g3"])]
f3, m3, w3 = bitpar(list("ABC"), g3, ["F"])
und = [f for f in f3 if m3[f] == 0]
v.check("Ex 19-12.3a", len(f3))
v.check("Ex 19-12.3b", len(und))
v.check("Ex 19-12.3c", 100 * (len(f3) - len(und)) / len(f3))
v.check("Ex 19-12.3d", len(f3) // 2)
v.assert_true("the undetectable faults are on the consensus gate", all("g3" in str(f[0]) for f in und), str(und))
v.assert_true("110 detects g1 stuck-at-0", bool(m3[("g1", 0)] >> 0b110 & 1), "")
v.assert_true("lab agrees on the consensus circuit", len(dft.Circuit(list("ABC"), g3, ["F"]).faults()) == len(f3), "")
# NAND3 (Problem 2) and AND-n tests
f_n3, m_n3, w_n3 = bitpar(list("ABC"), [("Y", "NAND", list("ABC"))], ["Y"])
v.check("19-12.2a", len(f_n3))
v.check("19-12.2b", len(set(m_n3.values())))
v.check("19-12.2c", min_tests(m_n3, w_n3))
for n_in in (2, 3, 4, 5):
    ins = [f"i{k}" for k in range(n_in)]
    fa, ma, wa = bitpar(ins, [("o", "AND", ins)], ["o"])
    v.assert_true(f"{n_in}-input AND needs n + 1 tests", min_tests(ma, wa) == n_in + 1, "")
v.check("Ex 19-12.4d", 16 + 1)
# c17 (Problem 4)
c17g = [("N10", "NAND", ["N1", "N3"]), ("N11", "NAND", ["N3", "N6"]), ("N16", "NAND", ["N2", "N11"]),
        ("N19", "NAND", ["N11", "N7"]), ("N22", "NAND", ["N10", "N16"]), ("N23", "NAND", ["N16", "N19"])]
f17, m17, w17 = bitpar(["N1", "N2", "N3", "N6", "N7"], c17g, ["N22", "N23"])
v.check("19-12.4a", len(f17))
v.check("19-12.4b", len(set(m17.values())))
v.check("19-12.4c", sum(1 for m in m17.values() if m == 0))
v.check("19-12.4d", min_tests(m17, w17))
v.assert_true("lab agrees on c17", len(dft.equivalence_classes(dft.Circuit(["N1", "N2", "N3", "N6", "N7"], c17g,
                                                                         ["N22", "N23"]))) == len(set(m17.values())), "")
# Problem 5: NAND(OR(A, B), C)
f5, m5, w5 = bitpar(list("ABC"), [("o", "OR", ["A", "B"]), ("F", "NAND", ["o", "C"])], ["F"])
v.check("19-12.5a", bin(m5[("A", 1)]).count("1"))
v.check("19-12.5b", bin(m5[("o", 0)]).count("1"))
# wide circuit of the lab (Part 2)
names = [f"a{k}" for k in range(10)] + ["b0", "b1"]
fw, mw, ww = bitpar(names, [("w", "AND", names[:10]), ("x", "XOR", ["b0", "b1"]), ("out", "OR", ["w", "x"])], ["out"])
hard = [f for f in fw if bin(mw[f]).count("1") * 2 ** 11 == ww * 1]
v.check("Lab 19-12.f", len(hard))
v.check("Lab 19-12.g", len(fw) - len(hard))

# ---------------------------------------------------------------- defect level and random patterns
dl = lambda y, t: 1 - math.exp((1 - t) * math.log(y))
v.check("Ex 19-12.1a", 1e6 * dl(0.8, 0.99))
v.check("Ex 19-12.1b", 1e6 * dl(0.8, 0.999))
from scipy.optimize import brentq  # noqa: E402
v.check("Ex 19-12.1c", 100 * brentq(lambda t: dl(0.8, t) - 1e-4, 0.9, 1.0, xtol=1e-12))
v.check("Ex 19-12.1d", 1e6 * 0.01 * -math.log(0.8))
v.check("19-12.1a", 1e6 * dl(0.9, 0.95))
v.check("19-12.1b", 100 * brentq(lambda t: dl(0.9, t) - 1e-5, 0.9, 1.0, xtol=1e-13))
v.check("19-12.11a", dl(0.5, 0.9))
v.check("19-12.11b", 0.1 * math.log(2))
v.check("19-12.11c", 100 * (0.1 * math.log(2) / dl(0.5, 0.9) - 1))
v.assert_true("lab defect level agrees", abs(dft.defect_level(0.8, 0.99) - dl(0.8, 0.99)) < 1e-15, "")


def n_patterns(p, conf):
    """Smallest N with 1 - (1 - p)^N >= conf, by search."""
    lo = math.log(1 - conf) / math.log(1 - p)
    return lo


v.check("Ex 19-12.4a", n_patterns(2 ** -16, 0.95))
v.check("Ex 19-12.4b", 3 / 2 ** -16)
v.check("Ex 19-12.4c", math.ceil(n_patterns(1 / 16, 0.95)))
v.assert_true("47 random patterns reach 95 % for p = 1/16", 1 - (15 / 16) ** 47 >= 0.95 > 1 - (15 / 16) ** 46, "")
v.check("19-12.6a", math.ceil(n_patterns(2 ** -8, 0.99)))
v.check("19-12.6b", 1 - 2 ** -8)


# ---------------------------------------------------------------- scan by stepping through phases
def step_scan(n_flops, chains, patterns):
    L = -(-n_flops // chains)
    cycles = 0
    for p in range(patterns + 1):
        cycles += L                     # shift in pattern p while shifting out response p - 1 (or final unload)
        if p < patterns:
            cycles += 1                 # capture
    return L, cycles


L5, c5 = step_scan(2_000_000, 8, 20_000)
v.check("Ex 19-12.5a", L5)
v.check("Ex 19-12.5b", c5 / 50e6)
L5c, c5c = step_scan(2_000_000, 800, 20_000)
v.check("Ex 19-12.5c", L5c)
v.check("Ex 19-12.5d", c5c / 50e6)
v.check("Ex 19-12.5e", c5 / c5c)
v.check("Ex 19-12.5f", 2 * 2_000_000 * 20_000 / 8 / 1e9)
v.check("Ex 19-12.5g", 16 * c5c / 8 / 1e6)
_, c7 = step_scan(500_000, 16, 5000)
_, c7c = step_scan(500_000, 1600, 5000)
v.check("19-12.7a", c7)
v.check("19-12.7b", c7 / 25e6)
v.check("19-12.7c", c7c)
v.check("19-12.7d", 1e3 * c7c / 25e6)
v.check("19-12.7e", c7 / c7c)
v.check("Lab 19-12.a", step_scan(8, 1, 4)[1])
v.assert_true("lab scan formula agrees", dft.scan_cycles(2_000_000, 800, 20_000) == c5c, "")
v.check("Lab 19-12.b", sum(1 for p in (0x00, 0x5A, 0xFF, 0x80) if (((p + 3) & 0xFF) >> 2) & 1))


# ---------------------------------------------------------------- LFSR periods as polynomial orders over GF(2)
def poly_order(poly_bits):
    """Multiplicative order of x modulo the polynomial (bit k = coefficient of x^k)."""
    deg = poly_bits.bit_length() - 1
    x, r, k = 0b10, 0b10, 1
    while r != 1:
        r <<= 1
        if r >> deg & 1:
            r ^= poly_bits
        k += 1
        if k > 1 << deg:
            return None
    return k


v.check("Ex 19-12.6a", poly_order(0b11001))     # x^4 + x^3 + 1
v.check("Ex 19-12.6b", poly_order(0b10101))     # x^4 + x^2 + 1
v.check("19-12.8a", poly_order(0b1101))         # x^3 + x^2 + 1
v.check("19-12.8b", poly_order(0b10101))
v.assert_true("lab LFSR periods agree", len(dft.lfsr_sequence([4, 3], 4)) == 15 and len(dft.lfsr_sequence([4, 2], 4)) == 6
              and len(dft.lfsr_sequence([3, 2], 3)) == 7, "")
v.check("Ex 19-12.6c", 2 ** -16)


# ---------------------------------------------------------------- MISR aliasing from the rank of its linear map
def my_misr(words, n=4):
    s = 0
    for w in words:
        fb = ((s >> 3) ^ (s >> 2)) & 1         # taps 4 and 3
        s = (((s << 1) | fb) ^ w) & ((1 << n) - 1)
    return s


def gf2_rank(vectors):
    rank, rows = 0, list(vectors)
    for bit in range(64):
        pivot = next((r for r in rows if r >> bit & 1), None)
        if pivot is None:
            continue
        rows.remove(pivot)
        rows = [r ^ pivot if r >> bit & 1 else r for r in rows]
        rank += 1
    return rank


n, m = 4, 3
images = []
for k in range(m):
    for b in range(n):
        words = [0] * m
        words[k] = 1 << b
        images.append(my_misr(words))
rank = gf2_rank(images)
aliasing = 2 ** (n * m - rank) - 1
v.check("19-12.12a", aliasing / (2 ** (n * m) - 1))
v.check("19-12.12b", aliasing)
v.assert_true("lab enumeration agrees", sum(1 for e in itertools.product(range(16), repeat=3)
                                            if any(e) and dft.misr_signature(list(e), [4, 3], 4) == 0) == aliasing, "")
v.assert_true("single-bit errors never alias", all(img != 0 for img in images), "")


# ---------------------------------------------------------------- March tests with an independent memory model
def march_detects(alg, fault, n=8):
    mem = [0] * n
    kind = fault[0]

    def write(a, val):
        old = mem[a]
        new = val
        if kind == "tf" and fault[1] == a and old != val and (val == 1) == fault[2]:
            new = old
        mem[a] = new
        if kind == "cf" and fault[1] == a and old != new and (new == 1) == fault[3]:
            mem[fault[2]] = fault[4]

    def read(a):
        return fault[2] if kind == "saf" and fault[1] == a else mem[a]
    for order, ops in alg:
        seq = range(n) if order != "down" else range(n - 1, -1, -1)
        for a in seq:
            for op in ops:
                if op.startswith("w"):
                    write(a, int(op[1]))
                elif read(a) != int(op[1]):
                    return True
    return False


C_MINUS = [("up", ["w0"]), ("up", ["r0", "w1"]), ("up", ["r1", "w0"]), ("down", ["r0", "w1"]), ("down", ["r1", "w0"]),
           ("up", ["r0"])]
MATS = [("up", ["w0"]), ("up", ["r0", "w1"]), ("down", ["r1", "w0"])]
simple = [("saf", a, val) for a in range(8) for val in (0, 1)] + [("tf", a, r) for a in range(8) for r in (True, False)]
cfs = [("cf", g, w, r, val) for g in range(8) for w in range(8) if g != w for r in (True, False) for val in (0, 1)]
v.assert_true("March C- detects every fault", all(march_detects(C_MINUS, f) for f in simple + cfs), "")
missed_simple = [f for f in simple if not march_detects(MATS, f)]
v.check("Lab 19-12.c", len(missed_simple))
v.check("Lab 19-12.d", sum(1 for f in cfs if not march_detects(MATS, f)))
v.check("Lab 19-12.e", len(cfs))
v.assert_true("MATS+ misses exactly the falling transition faults", all(f[0] == "tf" and f[2] is False for f in missed_simple), "")
v.check("Ex 19-12.6d", sum(len(ops) for _, ops in C_MINUS) * 8192)
v.check("Ex 19-12.6e", 1e6 * 10 * 8192 / 200e6)
v.check("19-12.9a", 10 * 131_072)
v.check("19-12.9b", 1e3 * 10 * 131_072 / 100e6)
v.check("19-12.10a", 1e6 * 256 / 10e6)
v.check("19-12.10b", 1e6 * 259 / 10e6)
v.check("19-12.10c", 32)

# scan gate overhead, classic estimate: scan FF 14 gate equivalents, plain FF 10
ng, nsff = 100_000, 2_000
v.check("Txt 19-12.a", 100 * (14 - 10) * nsff / (ng + 10 * nsff))

sys.exit(v.finish())
