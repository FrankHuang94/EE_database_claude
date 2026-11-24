"""Design-for-test models for Lab 19-12: stuck-at faults, fault simulation and test generation, random-pattern
coverage, LFSRs and MISRs, memory March tests, scan test time and defect level.

A combinational netlist is an ordered list of gates (name, type, [inputs]) over named primary inputs; every gate
output is a net with the gate's name. Supported types: AND, NAND, OR, NOR, XOR, XNOR, NOT, BUF.
"""
from __future__ import annotations

import itertools
import math
import random

OPS = {
    "AND": lambda v: int(all(v)),
    "NAND": lambda v: int(not all(v)),
    "OR": lambda v: int(any(v)),
    "NOR": lambda v: int(not any(v)),
    "XOR": lambda v: sum(v) % 2,
    "XNOR": lambda v: 1 - sum(v) % 2,
    "NOT": lambda v: 1 - v[0],
    "BUF": lambda v: v[0],
}


class Circuit:
    def __init__(self, inputs, gates, outputs):
        self.inputs, self.gates, self.outputs = list(inputs), list(gates), list(outputs)

    def eval(self, vector, fault=None):
        """Evaluate with an optional stuck-at fault (net, value) or a branch fault ((gate, pin), value)."""
        val = dict(zip(self.inputs, vector))
        if fault and isinstance(fault[0], str) and fault[0] in val:
            val[fault[0]] = fault[1]
        for name, typ, ins in self.gates:
            args = []
            for k, n in enumerate(ins):
                x = val[n]
                if fault and fault[0] == (name, k):
                    x = fault[1]
                args.append(x)
            val[name] = OPS[typ](args)
            if fault and fault[0] == name:
                val[name] = fault[1]
        return tuple(val[o] for o in self.outputs)

    def fanout(self):
        fo = {n: [] for n in self.inputs + [g[0] for g in self.gates]}
        for name, _, ins in self.gates:
            for k, n in enumerate(ins):
                fo[n].append((name, k))
        return fo

    def faults(self):
        """The uncollapsed single stuck-at fault list: both values on every stem, and on every branch of a net with
        fanout greater than one."""
        out = []
        fo = self.fanout()
        for n in self.inputs + [g[0] for g in self.gates]:
            out += [(n, 0), (n, 1)]
            if len(fo[n]) > 1:
                for br in fo[n]:
                    out += [(br, 0), (br, 1)]
        return out

    def detects(self, vector, fault):
        return self.eval(vector) != self.eval(vector, fault)

    def all_vectors(self):
        return list(itertools.product((0, 1), repeat=len(self.inputs)))

    def test_sets(self, faults=None):
        """For each fault, the set of input vectors that detect it (exhaustive; small circuits only)."""
        faults = self.faults() if faults is None else faults
        vecs = self.all_vectors()
        return {f: {v for v in vecs if self.detects(v, f)} for f in faults}


def equivalence_classes(circuit):
    """Group faults with identical test sets (functional equivalence, found exhaustively). Undetectable faults
    form their own group (empty test set)."""
    ts = circuit.test_sets()
    groups = {}
    for f, s in ts.items():
        groups.setdefault(frozenset(s), []).append(f)
    return list(groups.values())


def greedy_test_set(circuit):
    """A small test set covering every detectable fault, by repeatedly taking the vector that detects the most
    still-undetected faults."""
    ts = {f: s for f, s in circuit.test_sets().items() if s}
    remaining = set(ts)
    chosen = []
    while remaining:
        best = max(circuit.all_vectors(), key=lambda v: sum(1 for f in remaining if v in ts[f]))
        chosen.append(best)
        remaining = {f for f in remaining if best not in ts[f]}
    return chosen


def random_coverage(circuit, n_patterns, seed=0):
    """Fault coverage (detectable faults only) after each of n random patterns."""
    rng = random.Random(seed)
    ts = {f: s for f, s in circuit.test_sets().items() if s}
    detected, curve = set(), []
    for _ in range(n_patterns):
        v = tuple(rng.randint(0, 1) for _ in circuit.inputs)
        detected |= {f for f, s in ts.items() if v in s}
        curve.append(len(detected) / len(ts))
    return curve


def patterns_for_detection(p_detect, confidence):
    """Random patterns needed to detect a fault of per-pattern detection probability p with the given confidence."""
    return math.log(1 - confidence) / math.log(1 - p_detect)


# ---------------------------------------------------------------- defect level
def defect_level(yield_, coverage):
    """Williams-Brown: fraction of shipped (test-passing) parts that are defective, DL = 1 - Y^(1 - T)."""
    return 1 - yield_ ** (1 - coverage)


def coverage_for_dl(yield_, dl):
    return 1 - math.log(1 - dl) / math.log(yield_)


# ---------------------------------------------------------------- scan test time and data
def scan_cycles(n_flops, n_chains, n_patterns):
    """Shift-in of pattern k overlaps shift-out of pattern k-1: patterns x (L + 1) + L cycles for chain length L."""
    L = math.ceil(n_flops / n_chains)
    return n_patterns * (L + 1) + L


def test_data_bits(n_flops, n_patterns):
    """Stimulus plus expected response, one bit each per scan cell per pattern."""
    return 2 * n_flops * n_patterns


# ---------------------------------------------------------------- LFSR and MISR
def lfsr_sequence(taps, n_bits, seed=1, steps=None):
    """Fibonacci LFSR: taps are bit positions (1 = least significant ... n) XORed into the new MSB-side bit.
    Returns the list of states until the seed repeats (or steps states)."""
    state, out = seed, []
    mask = (1 << n_bits) - 1
    while True:
        out.append(state)
        fb = 0
        for t in taps:
            fb ^= (state >> (t - 1)) & 1
        state = ((state << 1) | fb) & mask
        if state == seed or (steps and len(out) >= steps):
            return out


def misr_signature(words, taps, n_bits, seed=0):
    """Multiple-input signature register: shift like the LFSR and XOR each response word into the state."""
    state = seed
    mask = (1 << n_bits) - 1
    for w in words:
        fb = 0
        for t in taps:
            fb ^= (state >> (t - 1)) & 1
        state = (((state << 1) | fb) ^ w) & mask
    return state


# ---------------------------------------------------------------- memory March tests
MARCH_C_MINUS = [("any", ["w0"]), ("up", ["r0", "w1"]), ("up", ["r1", "w0"]),
                 ("down", ["r0", "w1"]), ("down", ["r1", "w0"]), ("any", ["r0"])]


def march_ops(algorithm=MARCH_C_MINUS):
    """Operations per cell (10 for March C-)."""
    return sum(len(ops) for _, ops in algorithm)


class FaultyMemory:
    """A bit memory with optional faults: ('saf', cell, v) stuck-at, ('tf', cell, rising) transition fault,
    ('cfid', aggressor, victim, rising, v) idempotent coupling fault (an aggressor transition forces the victim)."""

    def __init__(self, n, faults=()):
        self.n, self.cells, self.faults = n, [0] * n, list(faults)

    def write(self, a, v):
        old = self.cells[a]
        for f in self.faults:
            if f[0] == "tf" and f[1] == a and old != v and (v == 1) == f[2]:
                v = old                                     # the transition fails
        self.cells[a] = v
        for f in self.faults:
            if f[0] == "cfid" and f[1] == a and old != v and (v == 1) == f[3]:
                self.cells[f[2]] = f[4]
        for f in self.faults:
            if f[0] == "saf":
                self.cells[f[1]] = f[2]

    def read(self, a):
        for f in self.faults:
            if f[0] == "saf" and f[1] == a:
                return f[2]
        return self.cells[a]


def run_march(memory, algorithm=MARCH_C_MINUS):
    """Apply a March test; return True if any read mismatches (fault detected)."""
    for order, ops in algorithm:
        addrs = range(memory.n) if order in ("up", "any") else range(memory.n - 1, -1, -1)
        for a in addrs:
            for op in ops:
                if op[0] == "w":
                    memory.write(a, int(op[1]))
                elif memory.read(a) != int(op[1]):
                    return True
    return False
