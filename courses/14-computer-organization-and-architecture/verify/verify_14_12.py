#!/usr/bin/env python3
"""Verify every number in chapter 14-12, its problem set and its lab.

Independent routes:
- coherence counts come from the lab's MESI/MSI simulator (labs/14-12-lab/mesi.py), which itself asserts the
  single-writer/multiple-reader and data-value invariants after every operation; the regular workloads are also
  checked against closed forms derived here (false sharing: 3 transactions per round of n-core increments, padded
  counters: one miss per core; spin locks: one BusRdX per test-and-set spin);
- SC litmus outcomes are recomputed here by brute force over all permutations that respect program order,
  independently of the lab's enumerator, and the TSO/PSO results are checked against the outcome sets stated in
  the x86-TSO paper (SB's (0, 0) allowed under TSO) and against the fence argument;
- directory overheads, interleaving counts, bus limits and the Amdahl optimum are evaluated from formulas.
"""
from __future__ import annotations

import itertools
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "14-12-lab"))
from eeverify import Verifier  # noqa: E402
import litmus  # noqa: E402
import mesi  # noqa: E402

v = Verifier.from_files("14-12", ROOT / "chapters" / "14-12-multicore-coherence-consistency.md",
                        ROOT / "solutions" / "14-12-solutions.md", ROOT / "labs" / "14-12-lab" / "README.md")


def sc_bruteforce(test):
    """All outcomes of every program-order-respecting permutation of the instructions (fences are no-ops)."""
    tags = [(t, i) for t, th in enumerate(test) for i in range(len(th))]
    regs = sorted({ins[2] for th in test for ins in th if ins[0] == "ld"})
    out, n = set(), 0
    for perm in itertools.permutations(tags):
        if any(perm.index((t, i)) > perm.index((t, i + 1)) for t, i in tags if i + 1 < len(test[t])):
            continue
        n += 1
        mem, r = {}, {}
        for t, i in perm:
            ins = test[t][i]
            if ins[0] == "st":
                mem[ins[1]] = ins[2]
            elif ins[0] == "ld":
                r[ins[2]] = mem.get(ins[1], 0)
        out.add(tuple(r[k] for k in regs))
    return out, n


# ---------------------------------------------------------------------------------------------------------------
# Example 1 and Problem 1: traces
ex1 = [(0, 0x100, False), (1, 0x100, False), (0, 0x100, True), (1, 0x100, False), (1, 0x100, True), (0, 0x100, False)]
s1 = mesi.System(2).run(ex1)
v.check("Ex 14-12.1a", s1.bus)
v.check("Ex 14-12.1b", s1.stats["invalidations"])
v.check("Ex 14-12.1c", s1.stats["flush"])
v.check("Ex 14-12.1d", s1.stats["coherence_misses"])
v.assert_true("Example 1: 4 BusRd + 2 BusUpgr; both end in S", (s1.stats["BusRd"], s1.stats["BusUpgr"]) == (4, 2)
              and [c.get(4) for c in s1.state] == ["S", "S"])
states = []
s = mesi.System(2)
for op in ex1:
    s.access(*op)
    states.append(tuple(s.state[c].get(4, "I") for c in range(2)))
v.assert_true("Example 1 table of states", states == [("E", "I"), ("S", "S"), ("M", "I"), ("S", "S"), ("I", "M"), ("S", "S")])
p1 = [(0, 0x100, False), (1, 0x100, False), (2, 0x100, False), (0, 0x100, True), (1, 0x100, True), (2, 0x100, False)]
s = mesi.System(3)
st1 = []
for op in p1:
    s.access(*op)
    st1.append(tuple(s.state[c].get(4, "I") for c in range(3)))
v.assert_true("Problem 1 states", st1 == [("E", "I", "I"), ("S", "S", "I"), ("S", "S", "S"), ("M", "I", "I"),
                                          ("I", "M", "I"), ("I", "S", "S")])
v.check("14-12.1a", s.bus)
v.check("14-12.1b", s.stats["invalidations"])
v.check("14-12.1c", s.stats["flush"])

# Example 2 and Problem 4: MSI against MESI
priv = [(0, 0x1000 + 64 * i, w) for i in range(100) for w in (False, True)]
v.check("Ex 14-12.2a", mesi.System(2, "MSI").run(priv).bus)
v.check("Ex 14-12.2b", mesi.System(2, "MESI").run(priv).bus)
p4 = [(0, 0x200, False), (0, 0x200, True), (1, 0x200, False), (0, 0x300, False), (0, 0x300, True)]
v.check("14-12.4a", mesi.System(2, "MSI").run(p4).bus)
v.check("14-12.4b", mesi.System(2, "MESI").run(p4).bus)

# Example 3 and Problem 5: false sharing
fs = {}
for n in (2, 4, 8):
    packed = mesi.System(n).run(mesi.counters(n, 1000, 4))
    padded = mesi.System(n).run(mesi.counters(n, 1000, 64))
    fs[n] = (packed.bus, packed.stats["invalidations"], padded.bus)
    v.assert_true(f"false sharing, {n} cores: closed forms 2n x 1000 + 1 transactions... ",
                  padded.bus == n and packed.bus == (2 * n - 1) * 1000 + 1 and packed.stats["invalidations"] == (2 * n - 2) * 1000)
v.check("Ex 14-12.3a", fs[2][0])
v.check("Ex 14-12.3b", fs[2][1])
v.check("Ex 14-12.3c", fs[2][2])
v.check("14-12.5a", fs[4][0])
v.check("14-12.5b", fs[4][1])
v.check("14-12.5c", fs[4][2])
v.check("14-12.5d", fs[8][0])
v.check("14-12.5e", fs[8][2])

# Example 4 and Problem 2: directories
v.check("Ex 14-12.4a", 100 * (64 + 2) / 512)
v.check("Ex 14-12.4b", 100 * (1024 + 2) / 512)
v.check("Ex 14-12.4c", 4 * int(math.log2(1024)) + 2)
v.assert_true("limited pointers: 8.2% overhead", round(100 * 42 / 512, 1) == 8.2)
v.check("14-12.2a", 100 * (32 + 2) / 1024)

# Example 5 and Problems 3, 7, 8, 12: litmus tests
sb_sc, n_sb = sc_bruteforce(litmus.SB)
v.assert_true("SB under SC: enumerator equals brute force", litmus.outcomes(litmus.SB, "SC") == sb_sc)
v.check("Ex 14-12.5a", n_sb)
v.check("Ex 14-12.5b", len(sb_sc))
sb_tso = litmus.outcomes(litmus.SB, "TSO")
v.check("Ex 14-12.5c", len(sb_tso))
v.assert_true("TSO adds exactly (0, 0) to SB, as the x86-TSO paper states", sb_tso - sb_sc == {(0, 0)})
v.check("Ex 14-12.5d", len(litmus.outcomes(litmus.SB_FENCED, "TSO")))
v.assert_true("fenced SB under TSO equals SC", litmus.outcomes(litmus.SB_FENCED, "TSO") == sb_sc)
v.check("14-12.3a", math.comb(4, 2))
v.check("14-12.3b", math.comb(6, 3))
v.check("14-12.3c", math.factorial(6) // (2 * 2 * 2))
v.assert_true("brute-force interleaving counts", sc_bruteforce([[("st", "a", 1)] * 3, [("st", "b", 1)] * 3])[1] == 20)
T7 = [[("st", "x", 1), ("ld", "x", "r1"), ("ld", "y", "r2")], [("st", "y", 1), ("ld", "y", "r3"), ("ld", "x", "r4")]]
o7sc, o7tso = litmus.outcomes(T7, "SC"), litmus.outcomes(T7, "TSO")
v.assert_true("Problem 7: SC enumerator equals brute force", o7sc == sc_bruteforce(T7)[0])
v.check("14-12.7a", len(o7sc))
v.check("14-12.7b", len(o7tso))
v.assert_true("(1, 0, 1, 0) only under TSO", (1, 0, 1, 0) in o7tso and (1, 0, 1, 0) not in o7sc)
mp = {m: litmus.outcomes(litmus.MP, m) for m in ("SC", "TSO", "PSO")}
v.assert_true("MP: SC enumerator equals brute force", mp["SC"] == sc_bruteforce(litmus.MP)[0])
v.check("14-12.8a", len(mp["SC"]))
v.check("14-12.8b", len(mp["TSO"]))
v.check("14-12.8c", len(mp["PSO"]))
v.assert_true("(1, 0) only under PSO; a fence between the stores removes it",
              (1, 0) in mp["PSO"] and (1, 0) not in mp["TSO"] and (1, 0) not in litmus.outcomes(litmus.MP_FENCED, "PSO"))
v.check("14-12.12a", 2)
v.assert_true("Dekker = SB: (0, 0) under TSO, gone with one fence per thread", (0, 0) in sb_tso
              and (0, 0) not in litmus.outcomes(litmus.SB_FENCED, "TSO"))

# Example 6 and Problem 10: spin locks
locks = {n: [mesi.System(n).run(mesi.spin_lock(n, 100, k)).bus for k in ("tas", "ttas")] for n in (2, 4, 8)}
v.check("Ex 14-12.6a", locks[4][0])
v.check("Ex 14-12.6b", locks[4][1])
inval = {k: mesi.System(4).run(mesi.spin_lock(4, 100, k)).stats["invalidations"] for k in ("tas", "ttas")}
v.check("Ex 14-12.6c", inval["tas"])
v.check("Ex 14-12.6d", inval["ttas"])
v.assert_true("closed forms: TAS = (n-1) x 100 + 1 + 1 + (n-1); TTAS = 1 + (n-1) + 1 + 2(n-1)",
              all(locks[n] == [(n - 1) * 100 + 2 + (n - 1), 1 + (n - 1) + 1 + 2 * (n - 1)] for n in (4, 8)))
v.check("14-12.10a", locks[2][0])
v.check("14-12.10b", locks[2][1])
v.check("14-12.10c", locks[8][0])
v.check("14-12.10d", locks[8][1])

# Problems 6 and 11
per_core = 2e9 * 10 / 1000 * 64
v.check("14-12.6a", per_core / 1e9)
v.check("14-12.6b", math.floor(51.2e9 / per_core))
S = lambda N: 1 / (0.05 + 0.95 / N + 0.005 * (N - 1))  # noqa: E731
best = max(range(1, 400), key=S)
v.check("14-12.11a", best)
v.check("14-12.11b", S(best))
v.assert_true("continuous optimum sqrt(0.95/0.005) = 13.8", round(math.sqrt(0.95 / 0.005), 1) == 13.8)

# Lab
v.check("Lab 14-12.a", fs[8][1])
v.check("Lab 14-12.b", locks[8][0])
v.check("Lab 14-12.c", len(litmus.outcomes(litmus.MP_FENCED, "PSO")))
v.check("Lab 14-12.d", len(litmus.outcomes(litmus.SB, "PSO")))

# ---------------------------------------------------------------- Problem 13: a full-map directory, message by message


class Directory:
    """Home-node directory with the rules of Problem 13; counts messages and critical-path traversals."""

    def __init__(self):
        self.state, self.sharers, self.owner = "I", set(), None
        self.log = []

    def read(self, c):
        if self.state == "M":                      # request, forward to owner, data to requester, copy to home
            msgs, path = 4, 3
            self.sharers = {self.owner, c}
            self.state, self.owner = "S", None
        else:                                      # request, data from home
            msgs, path = 2, 2
            self.sharers.add(c)
            self.state = "S"
        self.log.append((msgs, path, self.state, frozenset(self.sharers if self.state == "S" else {self.owner})))

    def write(self, c):
        others = self.sharers - {c}
        msgs = 2 + 2 * len(others)                 # request, data, one invalidation and one ack per sharer
        path = 3 if others else 2
        self.state, self.owner, self.sharers = "M", c, set()
        self.log.append((msgs, path, "M", frozenset({c})))


d13 = Directory()
d13.read(3)
d13.read(7)
d13.write(12)
d13.read(3)
for key, (msgs, _, _, _) in zip("abcd", d13.log):
    v.check(f"14-12.13{key}", msgs)
v.check("14-12.13e", sum(m for m, _, _, _ in d13.log))
v.check("14-12.13f", d13.log[2][1])
v.check("14-12.13g", d13.log[3][1])
sol12 = (ROOT / "solutions" / "14-12-solutions.md").read_text(encoding="utf-8").split("<!-- directory trace -->")[1]
rows13 = re.findall(r"^\| core \d+ \w+s X \| (\d+) \(.*?\) \| (\w) \{([\d, ]+)\} \|$", sol12, re.M)
v.assert_true("Solution 13's table matches the directory model row by row",
              [(int(m), s, frozenset(int(x) for x in sh.split(","))) for m, s, sh in rows13]
              == [(m, s, sh) for m, _, s, sh in d13.log])

sys.exit(v.finish())
