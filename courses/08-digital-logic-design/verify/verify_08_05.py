#!/usr/bin/env python3
"""Verify every number in chapter 08-05 (Verilog and testbenches), its solutions and its lab handout.

The checks model the relevant parts of the Verilog standard in Python, independently of the text:
- values are (width, bits, signed) triples with explicit masking, extension and reinterpretation;
- four-valued logic uses the IEEE 1364 truth tables (0 dominates AND, 1 dominates OR, Z acts as X);
- blocking and non-blocking assignment are modelled as immediate versus deferred updates, with every
  statement order (and every process order, for races) enumerated;
- coverage figures come from exact probability formulas and harmonic sums.
The same chapter examples are also checked in Icarus Verilog by labs/08-05-lab/semantics_tb.v.
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
v = Verifier.from_files("08-05", COURSE / "chapters" / "08-05-verilog-and-testbenches.md",
                        COURSE / "solutions" / "08-05-solutions.md",
                        COURSE / "labs" / "08-05-lab" / "README.md")


def mask(w):
    return (1 << w) - 1


def as_signed(bits, w):
    bits &= mask(w)
    return bits - (1 << w) if bits >> (w - 1) else bits


def extend(bits, w_from, w_to, signed):
    bits &= mask(w_from)
    if signed and bits >> (w_from - 1):
        bits |= mask(w_to) & ~mask(w_from)
    return bits


def ashr(bits, w, k):
    """Arithmetic shift right of a signed w-bit pattern."""
    return (as_signed(bits, w) >> k) & mask(w)


def reduce_and(bits, w):
    return int(bits & mask(w) == mask(w))


def reduce_xor(bits, w):
    return bin(bits & mask(w)).count("1") % 2


# four-valued logic: values '0', '1', 'x', 'z'
def norm(a):
    return "x" if a == "z" else a


def f_and(a, b):
    a, b = norm(a), norm(b)
    if a == "0" or b == "0":
        return "0"
    if a == "1" and b == "1":
        return "1"
    return "x"


def f_or(a, b):
    a, b = norm(a), norm(b)
    if a == "1" or b == "1":
        return "1"
    if a == "0" and b == "0":
        return "0"
    return "x"


def f_not(a):
    a = norm(a)
    return {"0": "1", "1": "0"}.get(a, "x")


def f_xor(a, b):
    a, b = norm(a), norm(b)
    if "x" in (a, b):
        return "x"
    return str(int(a) ^ int(b))


VALS = "01xz"


def definite(fn):
    return sum(1 for a in VALS for b in VALS if fn(a, b) in "01")


def run_block(stmts, regs, blocking):
    """Execute assignments [(lhs, rhs)] once; blocking updates immediately, non-blocking at the end."""
    r = dict(regs)
    pending = {}
    for lhs, rhs in stmts:
        if blocking:
            r[lhs] = r[rhs] if isinstance(rhs, str) else rhs
        else:
            pending[lhs] = r[rhs] if isinstance(rhs, str) else rhs
    r.update(pending)
    return r


def edges_to_reach(stmts, target, blocking, n_edges=8):
    regs = {k: 0 for k, _ in stmts}
    regs["d"] = 1
    for e in range(1, n_edges + 1):
        regs = run_block(stmts, regs, blocking)
        regs["d"] = 0
        if regs[target] == 1:
            return e
    return None


def H(m):
    return sum(1.0 / j for j in range(1, m + 1))


def coverage(n, m):
    return 1 - (1 - 1 / m) ** n


# ================================================================= chapter examples
a4, b4 = 0b1100, 0b0101
v.check("Ex 08-05.1a", (a4 + b4) & mask(5))
v.check("Ex 08-05.1b", (a4 + b4) & mask(4))
v.check("Ex 08-05.1c", (a4 << 4) | b4)
v.check("Ex 08-05.1d", reduce_and(a4, 4))
v.check("Ex 08-05.1e", int(a4 != 0))
v.check("Ex 08-05.1f", reduce_xor(a4, 4))
v.check("Ex 08-05.1g", a4 >> 2)
x8 = (-5) & mask(8)
v.check("Ex 08-05.2a", x8)
v.check("Ex 08-05.2b", as_signed(ashr(x8, 8, 1), 8))
v.check("Ex 08-05.2c", x8 >> 1)
v.check("Ex 08-05.2d", int(x8 < 0))                                   # unsigned compare: 251 < 0
v.check("Ex 08-05.2e", int(as_signed(extend(x8, 8, 32, True), 32) < 0))  # both signed, 32 bits
v.check("Ex 08-05.3a", int(f_and("x", "0")))
v.check("Ex 08-05.3b", int(f_or("x", "1")))
v.assert_true("Ex3 x & 1 is x and x | 0 is x", f_and("x", "1") == "x" and f_or("x", "0") == "x")
v.check("Ex 08-05.3c", definite(f_and))
v.check("Ex 08-05.3d", definite(f_xor))
v.check("Ex 08-05.3e", int("x" == "x"))                               # === compares literally
shift3 = [("q1", "d"), ("q2", "q1"), ("q3", "q2")]
v.check("Ex 08-05.4a", edges_to_reach(shift3, "q3", blocking=False))
v.check("Ex 08-05.4b", edges_to_reach(shift3, "q3", blocking=True))
nb = run_block([("a", "b"), ("b", "a")], {"a": 3, "b": 5}, blocking=False)
bl = run_block([("a", "b"), ("b", "a")], {"a": 3, "b": 5}, blocking=True)
v.check("Ex 08-05.4c", nb["a"])
v.check("Ex 08-05.4d", nb["b"])
v.check("Ex 08-05.4e", bl["a"])
v.check("Ex 08-05.4f", bl["b"])
v.check("Ex 08-05.5a", sum(1 for sel in range(4) if sel not in (0, 1, 2)))
M17 = 2 ** 17
v.check("Ex 08-05.6a", M17)
v.check("Ex 08-05.6b", coverage(M17, M17))
v.check("Ex 08-05.6c", M17 * H(M17))
v.check("Ex 08-05.6d", H(M17))
v.assert_true("coupon-collector asymptote", abs(H(M17) - (math.log(M17) + 0.5772156649)) < 1e-4)


def sens_mismatches(steps, start, sens, func):
    """Simulate an always block with an explicit sensitivity list against the true function."""
    vals = dict(start)
    y = func(vals)
    bad = 0
    for name, val in steps:
        changed = vals[name] != val
        vals[name] = val
        if changed and name in sens:
            y = func(vals)
        bad += int(y != func(vals))
    return bad


v.check("Ex 08-05.7a", sens_mismatches([("a", 1), ("b", 1), ("a", 0), ("a", 1), ("b", 0)], {"a": 0, "b": 0},
                                       {"a"}, lambda s: s["a"] & s["b"]))
v.check("Th 08-05.a", 100 * (1 - math.exp(-1)))
v.check("Th 08-05.b", 2 ** 20)

# ================================================================= solutions
A8, B8 = 200, 100
v.check("08-05.1a", (A8 + B8) & mask(8))
v.check("08-05.1b", (A8 + B8) & mask(9))
v.check("08-05.1c", (A8 - B8) & mask(8))
v.check("08-05.1d", (B8 - A8) & mask(8))
v.check("08-05.1e", as_signed((B8 - A8) & mask(8), 8))
v.check("08-05.2a", int("A", 16))
v.check("08-05.2b", int("101011", 2))
v.check("08-05.2c", int("0F0", 16))
v.check("08-05.2d", 32)
a8 = 0b10100110
v.check("08-05.3a", reduce_and(a8, 8))
v.check("08-05.3b", int(a8 != 0))
v.check("08-05.3c", reduce_xor(a8, 8))
v.check("08-05.3d", ((a8 & 15) << 4) | (a8 & 15))
v.check("08-05.3e", a8 >> 4)
v.check("08-05.3f", (a8 << 3) & mask(8))
p4 = 0b1010
v.check("08-05.4a", as_signed(p4, 4))
v.check("08-05.4b", as_signed(ashr(p4, 4, 2), 4))
v.check("08-05.4c", p4 >> 2)
v.check("08-05.4d", as_signed((p4 + 7) & mask(4), 4))
v.check("08-05.4e", extend(p4, 4, 8, True))
v.check("08-05.4f", int(p4 < 0))
v.check("08-05.4g", int(as_signed(p4, 4) < 0))
v.assert_true("P5 x|0 is x, ~z is x", f_or("x", "0") == "x" and f_not("z") == "x")
v.check("08-05.5a", int(f_and("z", "0")))
v.check("08-05.5b", 1)                      # === of identical four-valued patterns
v.assert_true("P5 == with an x bit is x", any(c == "x" for c in "10x1"))
v.check("08-05.5c", definite(f_or))
v.check("08-05.5d", definite(lambda a, b: f_not(f_and(a, b))))
v.check("08-05.5e", definite(lambda a, b: f_not(f_xor(a, b))))


def latched(block_paths, outputs):
    """Outputs not assigned on every path through a combinational block."""
    return [o for o in outputs if not all(o in path for path in block_paths)]


b1 = [{"y1"}, {"y1"}]
b2 = [{"y2"}, {"y2"}, {"y2"}, set()]            # sel = 0, 1, 2, 3
b3 = [{"y3", "y4"}, {"y3"}]                      # en = 1, en = 0 (y3 has a default)
v.check("08-05.6a", len(latched(b1, ["y1"])) + len(latched(b2, ["y2"])) + len(latched(b3, ["y3", "y4"])))
rev = [("q4", "q3"), ("q3", "q2"), ("q2", "q1"), ("q1", "d")]
fwd = [("q1", "d"), ("q2", "q1"), ("q3", "q2"), ("q4", "q3")]
v.check("08-05.7a", edges_to_reach(rev, "q4", blocking=True))
v.check("08-05.7b", edges_to_reach(fwd, "q4", blocking=True))
v.assert_true("P7 non-blocking gives 4 edges in either order",
              edges_to_reach(rev, "q4", False) == edges_to_reach(fwd, "q4", False) == 4)
rot = [("a", "b"), ("b", "c"), ("c", "a")]
r1 = run_block(rot, {"a": 1, "b": 2, "c": 3}, blocking=False)
r3 = run_block(rot, run_block(rot, r1, False), False)
rb = run_block(rot, {"a": 1, "b": 2, "c": 3}, blocking=True)
v.assert_true("P8 three rotations restore 1, 2, 3", (r3["a"], r3["b"], r3["c"]) == (1, 2, 3))
v.check("08-05.8a", r1["a"])
v.check("08-05.8b", r1["b"])
v.check("08-05.8c", r1["c"])
v.check("08-05.8d", rb["c"])
period_ns = 2 * 5
v.check("08-05.9a", 1e3 / period_ns)
rises = [t for t in range(0, 1000) if t % period_ns == 5]
v.check("08-05.9b", len(rises))
v.check("08-05.9c", 1000 % 256)
v.check("08-05.10a", sens_mismatches([("c", 1), ("a", 1), ("c", 0), ("b", 1)], {"a": 0, "b": 0, "c": 0},
                                     {"a", "b"}, lambda s: (s["a"] & s["b"]) | s["c"]))
M11 = 2 ** 11
v.check("08-05.11a", M11)
v.check("08-05.11b", 100 * coverage(M11, M11))
n99 = math.ceil(math.log(0.01) / math.log(1 - 1 / M11))
v.assert_true("P11 the found N is the smallest", coverage(n99, M11) >= 0.99 > coverage(n99 - 1, M11))
v.check("08-05.11c", n99)
v.check("08-05.11d", M11 * math.log(100))
v.check("08-05.12a", 1024 * H(1024))
v.check("08-05.12b", H(1024))
v.check("08-05.12c", 1024 * (H(1024) - H(512)))
v.check("08-05.12d", 1024 * H(512))
outcomes = set()
for order in itertools.permutations([("x", "y"), ("y", "x")]):
    r = {"x": 0, "y": 1}
    for lhs, rhs in order:
        r[lhs] = r[rhs]
    outcomes.add((r["x"], r["y"]))
v.check("08-05.13a", len(outcomes))
v.assert_true("P13 non-blocking always swaps", run_block([("x", "y"), ("y", "x")], {"x": 0, "y": 1}, False) == {"x": 1, "y": 0})
v.check("08-05.14a", 32)
v.check("08-05.14b", 32 * 5)
req, ack = {1, 4, 7}, {3, 8}
passes = sum(1 for r in req if any(r + k in ack for k in (1, 2, 3)))
v.check("08-05.15a", passes)
v.check("08-05.15b", len(req) - passes)

# ================================================================= lab handout
M16 = 2 ** 16
q1, q2 = (1 - 1 / M16) ** M16, (1 - 2 / M16) ** M16
mean = M16 * (1 - q1)
var = M16 * q1 * (1 - q1) + M16 * (M16 - 1) * (q2 - q1 * q1)
v.check("Lab 08-05.a", M16)
v.check("Lab 08-05.b", 5 + 2 * M16)
v.check("Lab 08-05.c", mean)
v.check("Lab 08-05.d", math.sqrt(var))
v.check("Lab 08-05.e", 0.01 * mean / math.sqrt(var))

v.finish()
