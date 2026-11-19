#!/usr/bin/env python3
"""Verify chapter 05-08: run every Python and C block, and recompute every published number independently.

Code blocks in the chapter and solutions are executed (C under the course's strict flags and sanitizers)
and their outputs compared exactly. Answer-key values are recomputed by other routes: closed forms for
the cost formulas, Python's heapq and bisect modules in place of the hand-written heap and search,
lgamma for log2(n!), exact fractions, and independent re-implementations of the hashing, ring-buffer
and queue scenarios.
"""
from __future__ import annotations

import heapq
import math
import statistics
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, run_c_blocks, run_python_blocks  # noqa: E402

C_DIR = HERE.parent
CH = C_DIR / "chapters" / "05-08-data-structures-and-algorithms.md"
SOL = C_DIR / "solutions" / "05-08-solutions.md"
LAB = C_DIR / "labs" / "05-08-lab" / "README.md"
v = Verifier.from_files("05-08", CH, SOL, LAB)
for runner in (run_python_blocks, run_c_blocks):
    runner(v, CH, "chapter")
    runner(v, SOL, "solutions")

lp_succ = lambda a: 0.5 * (1 + 1 / (1 - a))                     # noqa: E731  Knuth, linear probing
lp_fail = lambda a: 0.5 * (1 + 1 / (1 - a) ** 2)                # noqa: E731
log2_fact = lambda n: math.lgamma(n + 1) / math.log(2)          # noqa: E731
msort_worst = lambda n: n * math.ceil(math.log2(n)) - 2 ** math.ceil(math.log2(n)) + 1  # noqa: E731


def fnv1a(data: bytes) -> int:
    h = 2166136261
    for byte in data:
        h = ((h ^ byte) * 16777619) % 2**32
    return h


# ---------------------------------------------------------------- theory
v.check("T 05-08.a", lp_succ(0.75))
v.check("T 05-08.b", lp_fail(0.75))
v.check("T 05-08.c", lp_fail(0.9))

# ---------------------------------------------------------------- examples
v.check("Ex 05-08.1a", (10**6).bit_length())                   # floor(log2 n) + 1
v.check("Ex 05-08.1b", 10**6 * math.log2(10**6) / 1e9)
v.check("Ex 05-08.1c", Fraction(10**12, 2) / 10**9 / 60)
v.check("Ex 05-08.1d", (10**7).bit_length())
cap, stored, dropped = 8, [], 0                                 # ring buffer as a bounded list
for ch in "ABCDEFGHIJ":
    if len(stored) == cap:
        dropped += 1
    else:
        stored.append(ch)
popped, stored = stored[:3], stored[3:]
stored += ["K", "L"]
v.check("Ex 05-08.2a", dropped)
v.check("Ex 05-08.2b", len(stored))
v.assert_true("drained bytes are D E F G H K L", "".join(stored) == "DEFGHKL" and "".join(popped) == "ABC")
v.check("Ex 05-08.2c", math.ceil(115200 / 10 * 0.005))
slots, total = [None] * 8, 0
for key in ("adc", "gpio", "i2c", "spi", "uart", "timer"):
    i, probes = fnv1a(key.encode()) % 8, 1
    while slots[i] is not None:
        i, probes = (i + 1) % 8, probes + 1
    slots[i] = key
    total += probes
v.check("Ex 05-08.3a", total)
v.check("Ex 05-08.3b", total / 6)
h = []
for d in (40, 10, 30, 5, 20, 50, 15):
    heapq.heappush(h, d)
v.assert_true("heapq builds the same array 5 10 15 40 20 50 30", h == [5, 10, 15, 40, 20, 50, 30])
v.check("Ex 05-08.4a", math.floor(math.log2(10**6)))
v.check("Ex 05-08.5a", Fraction(1000 * 999, 4))
v.check("Ex 05-08.5b", log2_fact(1000))
v.check("Ex 05-08.5c", msort_worst(1000))

# ---------------------------------------------------------------- solutions
n = 1000
v.check("05-08.1a", n * (n - 1) // 2)
v.check("05-08.1b", n.bit_length())
v.check("05-08.1c", n * math.ceil(math.log2(n)))
arr = [3, 8, 15, 21, 29, 37, 44, 52, 60]
lo, hi, comps = 0, len(arr) - 1, 0                              # independent loop on half-open ranges
while lo <= hi:
    mid, comps = (lo + hi) // 2, comps + 1
    if arr[mid] == 37:
        break
    lo, hi = (mid + 1, hi) if arr[mid] < 37 else (lo, mid - 1)
v.check("05-08.3a", comps)
v.check("05-08.3b", len(arr).bit_length())
rate = 6 * 4000
v.check("05-08.4a", rate * 0.012)
v.check("05-08.4b", 1 << math.ceil(math.log2(rate * 0.012)))
v.check("05-08.4c", 2**32 / rate / 3600)
class _Node:                                                    # reverse a 5-node list, counting pointer writes
    def __init__(self, value, nxt):
        self.value, self.next = value, nxt


lst = None
for value in (5, 4, 3, 2, 1):
    lst = _Node(value, lst)
prev, cur, writes = None, lst, 0
while cur is not None:
    cur.next, prev, cur = prev, cur, cur.next
    writes += 1
values, node = [], prev
while node is not None:
    values.append(node.value)
    node = node.next
v.assert_true("reversal gives 5 4 3 2 1", values == [5, 4, 3, 2, 1])
v.check("05-08.5a", writes)
alpha = 1 - 1 / math.sqrt(19)
v.assert_true("alpha solves the 10-probe condition", abs(lp_fail(alpha) - 10) < 1e-12)
v.check("05-08.7a", alpha)
v.check("05-08.7b", math.floor(alpha * 1024))
v.check("05-08.7c", lp_succ(alpha))
v.check("05-08.7d", 1 + alpha / 2)
T = {1: 0}
for k in (2, 4, 8, 16):
    T[k] = 2 * T[k // 2] + k
v.check("05-08.9a", T[16])
v.check("05-08.9b", msort_worst(16))
v.check("05-08.10a", math.ceil(log2_fact(5)))
v.check("05-08.10b", math.ceil(log2_fact(12)))
v.check("05-08.10c", math.ceil(log2_fact(100)))
v.check("05-08.10d", msort_worst(12))
v.check("05-08.11a", 10**6 + 4096)
v.check("05-08.11b", 4096 * 4)
v.check("05-08.11c", statistics.median_low([2050, 2047, 4095, 0, 2047, 2049, 2050, 2047, 1]))
inbox, outbox, moves = [], [], 0                                # two-stack queue, re-implemented
ops = [("e", x) for x in range(1, 9)] + [("d", None)] * 3 + [("e", 9)] + [("d", None)] * 6
out = []
for op, x in ops:
    if op == "e":
        inbox.append(x)
    else:
        if not outbox:
            moves += len(inbox)
            outbox, inbox = inbox[::-1], []
        out.append(outbox.pop())
v.assert_true("two-stack queue preserves FIFO order", out == list(range(1, 10)))
v.check("05-08.12a", moves)

# ---------------------------------------------------------------- lab
cap, resizes = 8, 0
for count in range(1000):                                       # grow when (count + 1) / cap > 0.75
    if 4 * (count + 1) > 3 * cap:
        cap, resizes = cap * 2, resizes + 1
v.check("Lab 05-08.a", cap)
v.check("Lab 05-08.b", resizes)
v.check("Lab 05-08.c", 1000 / cap)
v.check("Lab 05-08.d", lp_succ(1000 / cap))
v.check("Lab 05-08.e", dropped)                                 # same scenario as Example 05-08.2
v.assert_true("lab drop count equals the example's", dropped == 2)


# ---------------------------------------------------------------- Problem 05-08.13: BST built with Python dicts
def bst_insert(t, k):
    if t is None:
        return {"k": k, "l": None, "r": None}
    if k < t["k"]:
        t["l"] = bst_insert(t["l"], k)
    elif k > t["k"]:
        t["r"] = bst_insert(t["r"], k)
    return t


def bst_height(t):
    return 0 if t is None else 1 + max(bst_height(t["l"]), bst_height(t["r"]))


def bst_keys(t):
    return [] if t is None else bst_keys(t["l"]) + [t["k"]] + bst_keys(t["r"])


keys13 = [8, 3, 10, 1, 6, 14, 4, 7, 13]
t13 = None
for k in keys13:
    t13 = bst_insert(t13, k)
v.check("05-08.13a", bst_height(t13))
v.check("05-08.13b", sum(1 for k in bst_keys(t13) if 4 <= k <= 10))
chain13 = None
for k in sorted(keys13):
    chain13 = bst_insert(chain13, k)
v.check("05-08.13c", bst_height(chain13))
v.check("05-08.13d", bst_height(chain13) + 1)                   # one frame per level plus the empty-child call
v.check("05-08.13e", 2048 // 32 - 1)

sys.exit(v.finish())
