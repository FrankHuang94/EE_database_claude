#!/usr/bin/env python3
"""Verify every number in chapter 26-06 (team structures and sizing), its problems and its lab.

Independent routes:
- channel counts by math.comb and, for small teams, by enumerating pairs;
- best team sizes by brute force over integers and by bounded scalar optimization;
- finishing times with added staff by stepping the work down in small time steps (the lab uses the
  closed form);
- management layers by integer ceiling division in a loop written here;
- staffing bases by trying every integer base (the lab uses the newsvendor rule).
"""
from __future__ import annotations

import math
import sys
from itertools import combinations
from pathlib import Path

from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import team  # noqa: E402

v = Verifier.from_files("26-06", ROOT / "chapters" / "26-06-team-structures-and-sizing.md",
                        ROOT / "solutions" / "26-06-solutions.md", LAB / "README.md")


def ch(n):
    return math.comb(n, 2)


def flat(n, c):
    return n * (1 - c * (n - 1))


def best_int(c):
    return max(range(1, 200), key=lambda n: flat(n, c))


def hier(k, m, c, cx):
    return k * m * (1 - c * (m - 1)) * (1 - cx * (k - 1))


def finish_stepped(work, n, c, add=0, ramp=0.0, mentor=0.0, dt=1e-4):
    total = n + add
    e = 1 - c * (total - 1)
    t, left = 0.0, work
    while left > 0:
        rate = (n - mentor * add) * e if (add and t < ramp) else total * e
        step = min(dt, left / rate)
        left -= rate * step
        t += step
    return t


def layers(n, s):
    out = []
    while n > 1:
        n = -(-n // s)
        out.append(n)
    return out


def cost(load, base, ce, cc):
    return sum(base * ce + max(0, l - base) * cc for l in load)


def best_base(load, ce, cc):
    return min(range(0, max(load) + 1), key=lambda b: (cost(load, b, ce, cc), b))


# ---------------------------------------------------------------- Example 1
for key, n in zip(("Ex 26-06.1a", "Ex 26-06.1a1", "Ex 26-06.1a2", "Ex 26-06.1a3"), (5, 10, 50, 100)):
    v.check(key, ch(n))
v.assert_true("Ex 1 pair enumeration", sum(1 for _ in combinations(range(10), 2)) == 45)
h1 = 10 * ch(10) + ch(10)
v.assert_true("Ex 1 lab hierarchy channels", team.channels_hierarchy(10, 9) == h1)
v.check("Ex 26-06.1b", h1)
v.check("Ex 26-06.1b1", 100 * h1 / ch(100))

# ---------------------------------------------------------------- Example 2
c = 0.03
nstar = optimize.minimize_scalar(lambda n: -flat(n, c), bounds=(1, 40), method="bounded", options={"xatol": 1e-10}).x
v.check("Ex 26-06.2a", nstar)
v.assert_true("Ex 2 integer optimum is 17", best_int(c) == 17)
v.check("Ex 26-06.2a1", flat(17, c))
v.check("Ex 26-06.2a2", 600 / flat(17, c))
v.check("Ex 26-06.2b", 1 - c * 7)
v.check("Ex 26-06.2b1", 8 * (1 - c * 7))
v.check("Ex 26-06.2b2", 1 - 0.02 * 9)
O2 = hier(10, 8, c, 0.02)
v.assert_true("Ex 2 lab hierarchy output", abs(team.hierarchy_output(10, 8, c, 0.02) - O2) < 1e-12)
v.check("Ex 26-06.2b3", O2)
v.check("Ex 26-06.2b4", 600 / O2)
v.check("Ex 26-06.2c", O2 / 90)
v.check("Ex 26-06.2c1", flat(17, c) / 17)

# ---------------------------------------------------------------- Example 3
e3 = 1 - 0.02 * 14
v.check("Ex 26-06.3a", e3)
v.check("Ex 26-06.3a1", (10 - 2.5) * e3)
v.check("Ex 26-06.3a2", 15 * e3)
for keys, W in ((("Ex 26-06.3b", "Ex 26-06.3b1"), 120), (("Ex 26-06.3c", "Ex 26-06.3c1"), 30)):
    t0, t1 = finish_stepped(W, 10, 0.02), finish_stepped(W, 10, 0.02, 5, 3, 0.5)
    v.assert_true(f"Ex 3 lab matches stepping at W={W}",
                  abs(team.finish_time(W, 10, 0.02, 5, 3, 0.5) - t1) < 1e-3)
    v.check(keys[0], t0)
    v.check(keys[1], t1)
v.check("Ex 26-06.3b2", finish_stepped(120, 10, 0.02) - finish_stepped(120, 10, 0.02, 5, 3, 0.5))
v.check("Ex 26-06.3d", 3 * (10 * (1 - 0.02 * 9) - (10 - 2.5) * e3))
v.check("Ex 26-06.3d1", 3 * (10 - 2.5) * e3)
v.check("Ex 26-06.3d2", 15 * e3 - 10 * (1 - 0.02 * 9))

# ---------------------------------------------------------------- Example 4
L8, L12 = layers(600, 8), layers(600, 12)
v.assert_true("Ex 4 lab layers", team.management_layers(600, 8) == L8)
for key, x in zip(("Ex 26-06.4a", "Ex 26-06.4a1", "Ex 26-06.4a2"), L8):
    v.check(key, x)
v.check("Ex 26-06.4a3", sum(L8))
for key, x in zip(("Ex 26-06.4b", "Ex 26-06.4b1"), L12):
    v.check(key, x)
v.check("Ex 26-06.4b2", sum(L12))
v.check("Ex 26-06.4c", 600 / 7)
v.check("Ex 26-06.4c1", 600 / 11)

# ---------------------------------------------------------------- Example 5
load5 = [10, 15, 25, 40, 40, 25, 10, 10]
ce, cc = 75e3, 112.5e3
v.check("Ex 26-06.5a", cost(load5, 40, ce, cc) / 1e6)
v.check("Ex 26-06.5b", sum(load5))
v.check("Ex 26-06.5b1", cost(load5, 0, ce, cc) / 1e6)
v.check("Ex 26-06.5c", ce / cc)
v.check("Ex 26-06.5c1", sum(1 for l in load5 if l > 10) / len(load5))
b5 = best_base(load5, ce, cc)
v.assert_true("Ex 5 newsvendor equals brute force", team.newsvendor_base(load5, ce, cc) == b5)
v.check("Ex 26-06.5c2", b5)
v.check("Ex 26-06.5c3", cost(load5, b5, ce, cc) / 1e6)
v.check("Ex 26-06.5c4", sum(max(0, l - b5) for l in load5))
v.check("Ex 26-06.5c5", b5 * len(load5) * ce / 1e6)
v.check("Ex 26-06.5c6", sum(max(0, l - b5) for l in load5) * cc / 1e6)
v.check("Ex 26-06.5d", cost(load5, 15, ce, cc) / 1e6)

# ---------------------------------------------------------------- Example 6
ey = 0.8 * 249e6 / 300e3
v.check("Ex 26-06.6a", ey)
v.check("Ex 26-06.6a1", ey / 2.5)
v.check("Ex 26-06.6b", 249 / 1.66)
v.check("Ex 26-06.6b1", 249 / 1.5)
v.check("Ex 26-06.6b2", ey / 1.66 / 2.5)
v.check("Ex 26-06.6b3", ey / 1.5 / 2.5)

# ---------------------------------------------------------------- text and concept checks
v.check("Txt 26-06.1", 1 + 1 / c)
v.check("Txt 26-06.2", 100 * 31000 / 42000)
v.check("Txt 26-06.3", ch(20))
v.check("Txt 26-06.4", ch(21) - ch(20))
v.check("Txt 26-06.5", ch(21))
v.check("Txt 26-06.6", (1 + 1 / 0.05) / 2)
v.assert_true("Concept check: 10 and 11 tie", abs(flat(10, 0.05) - flat(11, 0.05)) < 1e-12)
v.check("Txt 26-06.7", flat(10, 0.05))
v.check("Txt 26-06.8", sum(layers(1000, 10)))
v.check("Txt 26-06.9", 1 / 1.5)
v.check("Txt 26-06.10", 100 * 38325 / 200834)
v.check("Txt 26-06.11", 34141 / 1000)
v.check("Txt 26-06.12", 38325 / 1000)
v.check("Txt 26-06.13", 200834 / 1000)
v.check("Txt 26-06.14", 991857 / 1000)
v.check("Txt 26-06.15", 1618354 / 1e6)

# ---------------------------------------------------------------- Problems
for key, n in zip(("26-06.1a", "26-06.1a1", "26-06.1a2"), (8, 25, 200)):
    v.check(key, ch(n))
h_p1 = 8 * ch(25) + ch(8)
v.check("26-06.1b", h_p1)
v.check("26-06.1b1", ch(200) / h_p1)

v.assert_true("P3 integer optimum 13", best_int(0.04) == 13)
v.check("26-06.3a", (1 + 1 / 0.04) / 2)
v.check("26-06.3a1", flat(13, 0.04))
v.check("26-06.3b", optimize.brentq(lambda n: flat(n, 0.04), 2, 100))
v.check("26-06.3c", flat(20, 0.04))

v.check("26-06.4a", 1 - 0.03 * 5)
v.check("26-06.4b", 6 * (1 - 0.03 * 5))
v.check("26-06.4c", 1 - 0.015 * 11)
O4 = hier(12, 6, 0.03, 0.015)
v.check("26-06.4d", O4)
v.check("26-06.4d1", O4 / 84)
v.check("26-06.4d2", 1 - 0.03 * (8 - 1))  # Example 26-06.2: teams of 8 engineers
O4x = 12 * 6 * (1 - 0.03 * 5) * (1 - 0.02 * 11)
v.check("26-06.4d3", 1 - 0.02 * 11)
v.check("26-06.4d4", O4x)
v.check("26-06.4d5", O4x / 84)
v.check("26-06.4d6", 51.8 / 90)

v.check("26-06.5a", finish_stepped(60, 8, 0.02))
e5 = 1 - 0.02 * 11
v.check("26-06.5b", e5)
v.check("26-06.5b1", 6 * e5)
v.check("26-06.5b2", 2 * 6 * e5)
v.check("26-06.5b3", 12 * e5)
v.check("26-06.5b4", finish_stepped(60, 8, 0.02, 4, 2, 0.5))
w5 = optimize.brentq(lambda W: team.finish_time(W, 8, 0.02) - team.finish_time(W, 8, 0.02, 4, 2, 0.5), 2, 60)
v.assert_true("P5 break-even agrees with stepping",
              abs(finish_stepped(w5, 8, 0.02) - finish_stepped(w5, 8, 0.02, 4, 2, 0.5)) < 1e-3)
v.check("26-06.5c", w5)
v.check("26-06.5c1", w5 / (8 * (1 - 0.02 * 7)))

L7, L10 = layers(1500, 7), layers(1500, 10)
for key, x in zip(("26-06.6a", "26-06.6a1", "26-06.6a2"), L7):
    v.check(key, x)
v.check("26-06.6a3", sum(L7))
v.check("26-06.6a4", 1500 / 6)
for key, x in zip(("26-06.6b", "26-06.6b1", "26-06.6b2"), L10):
    v.check(key, x)
v.check("26-06.6b3", sum(L10))
v.check("26-06.6b4", 1500 / 9)
v.assert_true("P6 both spans give four layers", len(L7) == len(L10) == 4)

load7 = [20, 30, 50, 60, 60, 50, 30, 20]
ce7, cc7 = 80e3, 100e3
b7 = best_base(load7, ce7, cc7)
v.assert_true("P7 newsvendor equals brute force", team.newsvendor_base(load7, ce7, cc7) == b7)
v.check("26-06.7a", ce7 / cc7)
v.check("26-06.7a1", sum(1 for l in load7 if l > 20) / len(load7))
v.check("26-06.7a2", b7)
v.check("26-06.7b", cost(load7, b7, ce7, cc7) / 1e6)
v.check("26-06.7b1", sum(max(0, l - b7) for l in load7))
v.check("26-06.7c0", 30 * len(load7) * ce7 / 1e6)
v.check("26-06.7c1", sum(max(0, l - 30) for l in load7) * cc7 / 1e6)
v.check("26-06.7c2", sum(max(0, l - 30) for l in load7))
v.check("26-06.7c", cost(load7, 30, ce7, cc7) / 1e6)
v.check("26-06.7d", cost(load7, 60, ce7, cc7) / 1e6)
v.check("26-06.7e", cost(load7, 0, ce7, cc7) / 1e6)

v.check("26-06.8a", 18 * 150e3 / 1e6)
v.check("26-06.8a1", 14 * 200e3 / 1e6)
v.check("26-06.8b", 150 / 200)
v.check("26-06.8b1", optimize.brentq(lambda m: m * 200e3 - 18 * 150e3, 1, 18))

ey10 = 0.75 * 725e6 / 350e3
v.check("26-06.10", ey10)
v.check("26-06.10a", ey10 / 3)

peak = optimize.brentq(lambda P: 0.5 * 30 * P - 600, 1, 1000)
v.check("26-06.11a", peak)
v.check("26-06.11b", peak / 18)

# ---------------------------------------------------------------- lab
v.check("Lab 26-06.a", optimize.brentq(lambda n: flat(n, c), 2, 100))
splits = {k: hier(k, 96 // k, c, 0.02) for k in range(1, 97) if 96 % k == 0}
kbest = max(splits, key=splits.get)
v.check("Lab 26-06.b", kbest)
v.check("Lab 26-06.b1", splits[kbest])
wbe = optimize.brentq(lambda W: finish_stepped(W, 10, 0.02, dt=1e-3) - finish_stepped(W, 10, 0.02, 5, 3, 0.5, dt=1e-3),
                      20, 120, xtol=1e-6)
v.check("Lab 26-06.c", wbe)
v.check("Lab 26-06.c1", wbe / (10 * (1 - 0.02 * 9)))
bd = best_base(load5, 75e3, 187.5e3)
v.check("Lab 26-06.d", bd)
v.check("Lab 26-06.d1", cost(load5, bd, 75e3, 187.5e3) / 1e6)
v.check("Lab 26-06.d2", 1 / 2.5)

sys.exit(v.finish())
