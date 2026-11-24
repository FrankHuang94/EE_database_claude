"""Technology mapping by tree covering for Lab 19-10.

A Boolean function is first written as a subject tree of two-input NANDs and inverters (the base functions). Each
library cell is also written as one or more pattern trees in the same base functions. A cover chooses, at each
node, a cell whose pattern matches the tree rooted there; the cell's inputs are the subtrees at the pattern's
leaves. Dynamic programming over the tree, from the leaves up, finds the cover of minimum total area, or of
minimum arrival time under a load-independent delay per cell, and is optimal for trees (Keutzer's DAGON method).

Trees are nested tuples: ("in", "A"), ("inv", t), ("nand", t1, t2). Pattern leaves are ("x", k).
"""
from __future__ import annotations

import itertools


def IN(name):
    return ("in", name)


def INV(t):
    return ("inv", t)


def NAND(a, b):
    return ("nand", a, b)


def X(k):
    return ("x", k)


# Pattern trees for SKY130 hd cells (inputs x0, x1, ... in the cell's pin order).
PATTERNS = {
    "inv_1": [INV(X(0))],
    "nand2_1": [NAND(X(0), X(1))],
    "and2_1": [INV(NAND(X(0), X(1)))],
    "nor2_1": [INV(NAND(INV(X(0)), INV(X(1))))],
    "nand3_1": [NAND(INV(NAND(X(0), X(1))), X(2))],
    "nand4_1": [NAND(INV(NAND(X(0), X(1))), INV(NAND(X(2), X(3))))],
    "a21oi_1": [INV(NAND(NAND(X(0), X(1)), INV(X(2))))],
    "a22oi_1": [INV(NAND(NAND(X(0), X(1)), NAND(X(2), X(3))))],
    "o21ai_1": [NAND(NAND(INV(X(0)), INV(X(1))), X(2))],
}


def match(pattern, tree):
    """All bindings {leaf index: subtree} under which the pattern matches the tree (NAND inputs commute)."""
    if pattern[0] == "x":
        return [{pattern[1]: tree}]
    if pattern[0] != tree[0]:
        return []
    if pattern[0] == "inv":
        return match(pattern[1], tree[1])
    out = []
    for a, b in ((tree[1], tree[2]), (tree[2], tree[1])):
        for m1 in match(pattern[1], a):
            for m2 in match(pattern[2], b):
                if not set(m1) & set(m2):
                    out.append({**m1, **m2})
    return out


def matches(tree, patterns=PATTERNS):
    """(cell, leaves) for every cell pattern that matches at the root of the tree; duplicates removed."""
    seen, out = set(), []
    for cell, pats in patterns.items():
        for p in pats:
            for m in match(p, tree):
                leaves = tuple(m[k] for k in sorted(m))
                key = (cell, tuple(sorted(map(repr, leaves))))
                if key not in seen:
                    seen.add(key)
                    out.append((cell, leaves))
    return out


def best_cover(tree, cost, combine, patterns=PATTERNS, memo=None):
    """Dynamic programming: (value, cells) minimizing combine(cell value, [leaf values]) over all covers."""
    memo = {} if memo is None else memo
    if tree[0] == "in":
        return 0.0, []
    if tree in memo:
        return memo[tree]
    best = None
    for cell, leaves in matches(tree, patterns):
        sub = [best_cover(t, cost, combine, patterns, memo) for t in leaves]
        value = combine(cost[cell], [s[0] for s in sub])
        cells = [cell] + [c for s in sub for c in s[1]]
        if best is None or value < best[0] - 1e-12:
            best = (value, cells)
    memo[tree] = best
    return best


def min_area(tree, area, patterns=PATTERNS):
    return best_cover(tree, area, lambda a, subs: a + sum(subs), patterns)


def min_delay(tree, delay, patterns=PATTERNS):
    return best_cover(tree, delay, lambda d, subs: d + max(subs, default=0.0), patterns)


def evaluate(tree, env):
    """Logic value of a subject tree for an input assignment."""
    if tree[0] == "in":
        return env[tree[1]]
    if tree[0] == "inv":
        return 1 - evaluate(tree[1], env)
    return 1 - (evaluate(tree[1], env) & evaluate(tree[2], env))


def truth_table(tree, names):
    return tuple(evaluate(tree, dict(zip(names, bits))) for bits in itertools.product((0, 1), repeat=len(names)))
