#!/usr/bin/env python3
"""Verify every number in chapter 08-11 (memories and programmable logic), its solutions and lab.

Independent routes:
- memory organizations by choosing the array shape and splitting the address, checked by mapping every
  word address to a (row, column) pair and back for the chapter's 64K x 16 example;
- LUT counts by building the LUT networks (AND and parity trees, Shannon expansion with and without
  sharing) and evaluating them against the function on every input;
- PLA sizes from an exact minimum sum of products (exhaustive search) for the full adder;
- multiplexer, decoder, resource and cost figures from the problem data;
- Dadda counts reused from the 08-09 construction (rebuilt here bit by bit).
"""
from __future__ import annotations

import itertools
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-11", COURSE / "chapters" / "08-11-memories-and-programmable-logic.md",
                        COURSE / "solutions" / "08-11-solutions.md",
                        COURSE / "labs" / "08-11-lab" / "README.md")


def organize(words, width, col_to_row=1):
    bits = words * width
    rows = int(math.isqrt(bits // col_to_row))
    assert rows * rows * col_to_row == bits
    cols = rows * col_to_row
    per_row = cols // width
    return dict(bits=bits, addr=int(math.log2(words)), rows=rows, cols=cols, per_row=per_row,
                row_bits=int(math.log2(rows)), col_bits=int(math.log2(per_row)))


# ================================================================= chapter
o = organize(64 * 1024, 16)
v.check("Ex 08-11.1a", o["bits"])
v.check("Ex 08-11.1b", o["addr"])
v.check("Ex 08-11.1c", o["rows"])
v.check("Ex 08-11.1d", o["per_row"])
v.check("Ex 08-11.1e", o["row_bits"])
v.check("Ex 08-11.1f", o["col_bits"])
# every word maps to a distinct (row, column group) and back
seen = set()
for a in range(64 * 1024):
    row, col = a >> o["col_bits"], a & (o["per_row"] - 1)
    seen.add((row, col))
v.assert_true("address split covers every word exactly once", len(seen) == 64 * 1024 and max(r for r, _ in seen) == 1023)



def rom_bits(n_in, f):
    """Size of a ROM tabulating f over every n_in-bit address: entries times the width of the largest output."""
    table = [f(a) for a in range(2 ** n_in)]
    return len(table) * max(table).bit_length()


v.check("Ex 08-11.2a", rom_bits(8, lambda a: (a >> 4) * (a & 15)))
v.check("Ex 08-11.2b", rom_bits(16, lambda a: (a >> 8) * (a & 255)))


def dadda_counts(n):
    d = [2]
    while d[-1] < n:
        d.append(d[-1] * 3 // 2)
    targets = [t for t in reversed(d) if t < n]
    cols = [sum(1 for i in range(n) for j in range(n) if i + j == c) for c in range(2 * n)]
    fa = 0
    for t in targets:
        new = [0] * (2 * n + 1)
        for c in range(2 * n):
            h, bits = cols[c] + new[c], cols[c]
            while h > t:
                if h - t >= 2 and bits >= 3:
                    bits -= 3; new[c] += 1; new[c + 1] += 1; fa += 1; h -= 2
                else:
                    bits -= 2; new[c] += 1; new[c + 1] += 1; h -= 1
            new[c] += bits
        cols = new[:2 * n]
    return fa


v.check("Ex 08-11.2c", 8 * 8)
v.check("Ex 08-11.2d", dadda_counts(8))


def read_muxes(ports, nregs, width):
    return ports * width * (nregs - 1)


v.check("Ex 08-11.3a", 32 * 32)
v.check("Ex 08-11.3b", read_muxes(2, 32, 32))
v.check("Ex 08-11.3c", read_muxes(8, 32, 32))
v.check("Ex 08-11.3d", ((8 + 4) / (2 + 1)) ** 2)
v.check("Ex 08-11.4a", 2 ** 2 ** 4)
v.check("Ex 08-11.4b", 2.0 ** 2 ** 6)


def and_tree(n, k):
    """Fewest k-LUTs (and, among those, fewest levels) that AND n inputs, found by searching tree shapes.

    A tree is described level by level: a LUT may take primary inputs and outputs of LUTs on lower levels.
    best(m) is the cheapest way to reduce m signals to one, trying every number j of LUTs on the current
    level and every number of signals they absorb (the others pass up unchanged); the result is checked against the counting bound
    ceil((n - 1)/(k - 1)) and evaluated on random inputs below.
    """
    import functools

    @functools.lru_cache(None)
    def best(m):
        if m == 1:
            return (0, 0)
        if m <= k:
            return (1, 1)
        options = []
        for j in range(1, m):                  # j LUTs on this level absorb `used` signals; the rest pass up
            for used in range(j + 1, min(m, j * k) + 1):
                luts, lev = best(m - used + j)
                options.append((luts + j, lev + 1))
        return min(options)
    return best(n)


def and_tree_eval(n, k, x):
    """Evaluate the greedy-packed tree that meets the bound: fill LUTs to k inputs, carrying leftovers up."""
    vals = [(x >> i) & 1 for i in range(n)]
    count = 0
    while len(vals) > 1:
        take = vals[:k]
        vals = vals[k:] + [int(all(take))]
        count += 1
    return vals[0], count


for n, k in ((8, 4), (16, 4), (16, 6), (32, 4), (32, 6)):
    rng = random.Random(n * 10 + k)
    samples = [rng.getrandbits(n) for _ in range(2000)] + [2 ** n - 1, 2 ** n - 2]
    assert all(and_tree_eval(n, k, x)[0] == int(x == 2 ** n - 1) for x in samples)
    assert and_tree_eval(n, k, 0)[1] == math.ceil((n - 1) / (k - 1)) == and_tree(n, k)[0]
v.assert_true("AND trees of LUTs compute the AND and meet the counting bound ceil((n-1)/(k-1))", True)
l16, lv16 = and_tree(16, 4)
v.check("Ex 08-11.4c", l16)
v.check("Ex 08-11.4d", lv16)
v.check("Ex 08-11.4e", and_tree(16, 6)[0])


def shannon(tt, n, k=4, share=True):
    built = {}
    count = [0]

    def build(t, m):
        if share and t in built:
            return built[t]
        if m <= k:
            node = ("lut", t)
        else:
            h = len(t) // 2
            node = ("mux", m - 1, build(t[:h], m - 1), build(t[h:], m - 1))
        count[0] += 1
        if share:
            built[t] = node
        return node

    root = build(tuple(tt), n)

    def ev(node, x):
        if node[0] == "lut":
            return node[1][x % len(node[1])]
        return ev(node[3] if (x >> node[1]) & 1 else node[2], x)

    return count[0], (lambda x: ev(root, x))


rng = random.Random(6)
tt6 = tuple(rng.getrandbits(1) for _ in range(64))
c6, f6 = shannon(tt6, 6, share=False)
v.assert_true("Shannon network of a 6-input function is correct on all inputs", all(f6(x) == tt6[x] for x in range(64)))
v.check("Ex 08-11.4f", c6)
v.assert_true("worst case formula 2^(n-k+1)-1 matches the unshared construction (n = 5..8)",
              all(shannon(tuple(rng.getrandbits(1) for _ in range(2 ** n)), n, share=False)[0] == 2 ** (n - 3) - 1
                  for n in range(5, 9)))


# PLA for the full adder: exact minimum SOP (products) of S and Cout
def covers(c, m, n):
    return all(x is None or x == (m >> (n - 1 - i)) & 1 for i, x in enumerate(c))


def min_products(on, n=3):
    imps = [c for c in itertools.product((0, 1, None), repeat=n)
            if all(m in on for m in range(2 ** n) if covers(c, m, n))]
    for k in range(1, len(on) + 1):
        for combo in itertools.combinations(imps, k):
            if all(any(covers(c, m, n) for c in combo) for m in on):
                return list(combo)


S_on = [m for m in range(8) if bin(m).count("1") % 2]
C_on = [m for m in range(8) if bin(m).count("1") >= 2]
pS, pC = min_products(S_on), min_products(C_on)
products = len(set(pS) | set(pC))
v.check("Ex 08-11.5a", 2 ** 3 * 2)
v.check("Ex 08-11.5b", products)
v.check("Ex 08-11.5c", 2 * 3 * products + products * 2)
v.check("Ex 08-11.5d", 2 * 20 * 30 + 30 * 1)

buf = 4096 * 16
v.check("Ex 08-11.6a", buf)
v.check("Ex 08-11.6b", math.ceil(buf / 4096))
v.check("Ex 08-11.6c", 100 * math.ceil(buf / 4096) / 30)
v.check("Ex 08-11.6d", 8)
v.check("Ex 08-11.6e", 100 * 8 / 8)
v.check("Ex 08-11.6f", 8 * 48000)
v.check("Ex 08-11.7a", 5e6 / (50 - 5))
v.check("Ex 08-11.7b", 5 + 5e6 / 50000)
v.check("Ex 08-11.7c", 4086e3 / 5280)

# ================================================================= solutions
o1 = organize(256 * 1024, 32, col_to_row=2)
v.check("08-11.1a", o1["bits"])
v.check("08-11.1b", o1["addr"])
v.check("08-11.1c", o1["rows"])
v.check("08-11.1d", o1["cols"])
v.check("08-11.1e", o1["per_row"])
v.check("08-11.1f", o1["row_bits"])
v.check("08-11.1g", o1["col_bits"])
SEG = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71]
v.check("08-11.2a", rom_bits(4, lambda a: SEG[a]))
v.check("08-11.2b", rom_bits(8, lambda b: b ^ (b >> 1)))
v.assert_true("Gray code g = b xor (b >> 1) uses one XOR per bit except the top",
              all((b ^ (b >> 1)) >> 7 == b >> 7 for b in range(256)))
gray_xors = sum(1 for i in range(8) if any(((b ^ (b >> 1)) >> i & 1) != (b >> i & 1) for b in range(256)))
v.check("08-11.2c", gray_xors)                 # output bits that differ from their input bit need an XOR
v.check("08-11.3a", 2 ** 2 ** 2)
v.check("08-11.3b", 2 ** 2 ** 5)
v.check("08-11.4a", 16 * 64)
v.check("08-11.4b", read_muxes(3, 16, 64))
v.check("08-11.4c", 2 * len({r for r in range(16)}))    # two write ports, each decoding one of 16 registers
v.check("08-11.4d", (5 / 3) ** 2)
for (n, k), (ka, kb) in (((8, 4), ("08-11.5a", "08-11.5b")), ((32, 4), ("08-11.5c", "08-11.5d")),
                         ((32, 6), ("08-11.5e", "08-11.5f"))):
    luts, levels = and_tree(n, k)
    v.check(ka, luts)
    v.check(kb, levels)


def shannon_wide(tt, n, k):
    """Shannon network whose multiplexer LUTs select among 2^m cofactors, with m + 2^m <= k."""
    m_max = max(m for m in range(1, k) if m + 2 ** m <= k)
    count = [0]

    def build(t, nv):
        count[0] += 1
        if nv <= k:
            return ("lut", t)
        m = min(m_max, nv - k)                  # split on m variables (never below k inputs per cofactor)
        size = len(t) // 2 ** m
        return ("mux", nv - m, m, [build(t[i * size:(i + 1) * size], nv - m) for i in range(2 ** m)])

    root = build(tuple(tt), n)

    def ev(node, x):
        if node[0] == "lut":
            return node[1][x % len(node[1])]
        _, low, m, kids = node
        return ev(kids[(x >> low) & (2 ** m - 1)], x)

    return count[0], (lambda x: ev(root, x))


tt8 = tuple(rng.getrandbits(1) for _ in range(256))
c84, f84 = shannon_wide(tt8, 8, 4)
c86, f86 = shannon_wide(tt8, 8, 6)
v.assert_true("8-input Shannon networks (2:1 muxes in 4-LUTs, 4:1 muxes in 6-LUTs) are correct on all inputs",
              all(f84(x) == tt8[x] and f86(x) == tt8[x] for x in range(256)))
v.check("08-11.6a", c84)
v.check("08-11.6b", c86)


def parity_tree_luts(n, k):
    luts, width = 0, n
    while width > 1:
        width = math.ceil(width / k)
        luts += width
    return luts


v.check("08-11.6c", parity_tree_luts(8, 4))
v.check("08-11.7a", 2 * 4 * 9 + 9 * 3)
v.check("08-11.7b", 2 ** 4 * 3)
v.check("08-11.7c", 2 * 16 * 40 + 40 * 4)
v.check("08-11.7d", 2 ** 16 * 4)
v.check("08-11.8a", 100 * 8192 * 50e-9 / 64e-3)
disp = 320 * 240
v.check("08-11.9a", math.ceil(disp / 4096))
v.check("08-11.9b", 100 * math.ceil(disp / 4096) / 30)
v.check("08-11.9c", math.ceil(128 * 1024 * 8 / (256 * 1024)))
EBR_MODES = {(256, 16), (512, 8), (1024, 4), (2048, 2)}    # iCE40 UltraPlus data sheet (R-159)
v.check("08-11.9d", math.ceil(disp / max(depth for depth, width in EBR_MODES)))
v.check("08-11.10a", 64 * 16000)
v.check("08-11.10b", 100 * 64 * 16000 / 12e6)
v.check("08-11.10c", 12e6 / 16000)
v.check("08-11.11a", 5280 * 2 ** 4)
v.check("08-11.12a", 20e6 / (35 - 8))
units = 300_000 * 3
fpga_total, asic_total = 35 * units, 20e6 + 8 * units
v.check("08-11.12b", fpga_total / 1e6)
v.check("08-11.12c", asic_total / 1e6)
v.check("08-11.12d", (fpga_total - asic_total) / 1e6)
v.check("08-11.13a", 100 * 16 / 1024)
v.check("08-11.13b", 100 * 16 / 256)
v.check("08-11.14a", 3840 / 8)

# ================================================================= lab
gb = organize(2 ** 30 // 32, 32)
v.check("Lab 08-11.a", gb["rows"])
v.check("Lab 08-11.b", gb["row_bits"])
v.check("Lab 08-11.c", gb["col_bits"])
rng = random.Random(811)
counts = []
for trial in range(1000):
    tt = tuple(rng.getrandbits(1) for _ in range(256))
    counts.append(shannon(tt, 8)[0])
v.check("Lab 08-11.d", sum(counts) / len(counts))
parity = tuple(bin(x).count("1") % 2 for x in range(256))
cp, fp = shannon(parity, 8)
v.assert_true("shared Shannon network computes 8-input parity", all(fp(x) == parity[x] for x in range(256)))
v.check("Lab 08-11.e", cp)
v.check("Lab 08-11.f", parity_tree_luts(8, 4))
v.check("Lab 08-11.g", math.ceil(4096 * 16 / 4096) + math.ceil(320 * 240 / 4096))
v.check("Lab 08-11.h", 2000)
v.check("Lab 08-11.i", 2 ** 6)

v.finish()
