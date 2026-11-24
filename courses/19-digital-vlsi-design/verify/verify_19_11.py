#!/usr/bin/env python3
"""Verify every number in chapter 19-11 (floorplan, place and route, signoff), its problems and its lab.

Independent routes:
- strap IR drop by solving the boundary-value problem V'' = r i(x) with scipy's solve_bvp (uniform load) and by
  superposition of point-load solutions, not by the lab's ladder;
- quadratic placement by minimizing the spring energy numerically (scipy.optimize.minimize);
- spanning trees with scipy.sparse.csgraph, Steiner trees by exhaustive search written here, maze routes by
  csgraph shortest paths on the grid graph;
- zero-skew merging by root-finding on the skew of an explicitly computed Elmore delay, with pi-ladder Elmore delays
  from a resistance-sharing matrix; the H-tree by constructing its segments recursively;
- arithmetic quantities directly; the lab module is checked against these results; ngspice confirms the strap and
  the merge (strap.cir, merge.cir).
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import brentq, minimize
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, shortest_path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import pnr  # noqa: E402

v = Verifier.from_files("19-11", ROOT / "chapters" / "19-11-place-route-signoff.md",
                        ROOT / "solutions" / "19-11-solutions.md", LAB / "README.md")
ROW, SITE = 2.72, 0.46


# ---------------------------------------------------------------- floorplans
def floorplan(cells, util, aspect):
    core = cells / util
    width = math.sqrt(core / aspect)
    rows = math.ceil(round(width * aspect / ROW, 9))
    return core, width, rows, rows * ROW


core, w, rows, h = floorplan(300_000, 0.60, 1.0)
v.check("Ex 19-11.1a", core)
v.check("Ex 19-11.1b", w)
v.check("Ex 19-11.1c", rows)
v.check("Ex 19-11.1d", h)
v.check("Ex 19-11.1e", math.floor(w / SITE))
v.check("Ex 19-11.1f", 100 * 300_000 / (w * h))
v.check("Ex 19-11.1g", (w + 80) * (h + 80) / 1e6)
v.check("Ex 19-11.1h", 100 * ((w + 80) * (h + 80) / 1e6 / 0.5 - 1))
core, w, rows, h = floorplan(120_000, 0.70, 2.0)
v.check("19-11.1a", core)
v.check("19-11.1b", w)
v.check("19-11.1c", rows)
v.check("19-11.1d", h)
v.check("19-11.1e", math.floor(w / SITE))
v.check("19-11.1f", 100 * 120_000 / (w * h))
v.assert_true("lab floorplan agrees", abs(pnr.core_dimensions(120_000, 0.70, 2.0)[1] - h) < 1e-9, "")


# ---------------------------------------------------------------- straps by boundary-value problems
def strap_bvp(r, i, L, both_ends=True):
    """Max drop on a strap with uniform load: dV/dx = -r I(x), dI/dx = -i (I = current flowing toward +x)."""
    x = np.linspace(0, L, 201)

    def f(x, y):
        return np.vstack([r * y[1], -i * np.ones_like(x)])     # y0 = drop, y1 = current away from x = 0

    if both_ends:
        bc = lambda a, b: np.array([a[0], b[0]])                 # zero drop at both ends
    else:
        bc = lambda a, b: np.array([a[0], b[1]])                 # zero drop at x = 0, no current past the far end
    sol = solve_bvp(f, bc, x, np.zeros((2, x.size)), tol=1e-10)
    return float(np.max(sol.sol(np.linspace(0, L, 4001))[0]))


v.check("19-11.2a", 1e3 * strap_bvp(2.0, 0.020, 1.0))
v.check("19-11.2b", 1e3 * strap_bvp(2.0, 0.020, 1.0, both_ends=False))
v.check("19-11.2c", 1e3 * strap_bvp(1.0 / 0.5, 0.010 / 0.5, 0.5))   # half length: 1 ohm and 10 mA over 0.5 units
v.assert_true("lab ladder matches the continuous strap", abs(pnr.strap_drop_ladder(0.02, 2.0, 50).max() - 0.005) < 1e-12
              and abs(pnr.strap_drop_ladder(0.02, 2.0, 50, both_ends=False).max() - 0.020) < 1e-12, "")


def point_drop(x, ip, r, a, L):
    return ip * r * x * (L - a) / L if x <= a else ip * r * a * (L - x) / L


def uniform_drop(x, r, i, L):
    return r * i * x * (L - x) / 2


L12, r12, i12 = 200.0, 0.5, 1e-3 / 200.0
xs = np.linspace(0, L12, 200_001)
tot = np.array([uniform_drop(x, r12, i12, L12) + point_drop(x, 2e-3, r12, 50, L12) for x in xs])
v.check("19-11.12a", 1e3 * point_drop(50, 2e-3, r12, 50, L12))
v.check("19-11.12b", 1e3 * tot.max())
v.check("19-11.12c", xs[tot.argmax()])
v.check("19-11.12d", 1e3 * strap_bvp(r12, i12, L12))
v.check("19-11.12e", 1e3 * max(uniform_drop(x, r12, i12, L12) + point_drop(x, 2e-3, r12, 100, L12) for x in xs[::100]))
v.check("Lab 19-11.a", 1e3 * (uniform_drop(100, r12, i12, L12) + point_drop(100, 2e-3, r12, 50, L12)))


# ---------------------------------------------------------------- placement by numerical minimization
def place_min(n, nets, fixed, dims=2):
    def pos(z, p):
        return np.array(fixed[p]) if isinstance(p, str) else z.reshape(n, dims)[p]

    def energy(z):
        return sum(w * np.sum((pos(z, a) - pos(z, b)) ** 2) for a, b, w in nets)
    res = minimize(energy, np.ones(n * dims), method="BFGS", options={"gtol": 1e-12})
    return res.x.reshape(n, dims)


ex3 = place_min(4, [("P0", 0, 1), (0, 1, 1), (1, 2, 1), (2, "P1", 1), (1, 3, 1), (3, "P2", 2)],
                {"P0": (0, 0), "P1": (10, 0), "P2": (5, 6)})
for key, val in zip(("Ex 19-11.3a", "Ex 19-11.3b", "Ex 19-11.3c", "Ex 19-11.3d", "Ex 19-11.3e", "Ex 19-11.3f",
                     "Ex 19-11.3g", "Ex 19-11.3h"), ex3.flatten()):
    v.check(key, val)
segs = [((0, 0), ex3[0]), (ex3[0], ex3[1]), (ex3[1], ex3[2]), (ex3[2], (10, 0)), (ex3[1], ex3[3]), (ex3[3], (5, 6))]
v.check("Ex 19-11.3i", sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in segs))
v.assert_true("lab quadratic placement agrees", np.allclose(pnr.quadratic_place(
    4, [("P0", 0, 1), (0, 1, 1), (1, 2, 1), (2, "P1", 1), (1, 3, 1), (3, "P2", 2)],
    {"P0": (0, 0), "P1": (10, 0), "P2": (5, 6)}), ex3, atol=1e-6), "")
p4 = place_min(2, [("P0", 0, 1), (0, 1, 2), (1, "P1", 1), (0, "P1", 1)], {"P0": (0,), "P1": (12,)}, dims=1)
v.check("19-11.4a", p4[1, 0])
v.check("19-11.4b", p4[0, 0])
p4s = place_min(2, [("P0", 0, 1), (0, 1, 2), (1, "P1", 1), (0, "P1", 1)], {"P0": (3,), "P1": (15,)}, dims=1)
v.check("19-11.4c", p4s[0, 0] - p4[0, 0])
v.assert_true("uniform shift moves both cells equally", abs((p4s[1, 0] - p4[1, 0]) - 3) < 1e-6, "")


# ---------------------------------------------------------------- wirelength, trees and mazes
def hpwl(pts):
    xs, ys = zip(*pts)
    return max(xs) - min(xs) + max(ys) - min(ys)


def mst(pts):
    n = len(pts)
    d = np.array([[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in pts] for p in pts], dtype=float)
    return float(minimum_spanning_tree(csr_matrix(d)).sum())


def smt(pts):
    pts = [tuple(p) for p in pts]
    grid = {(x, y) for x in {p[0] for p in pts} for y in {p[1] for p in pts}} - set(pts)
    best = mst(pts)
    for k in range(1, len(pts) - 1):
        for extra in itertools.combinations(sorted(grid), k):
            best = min(best, mst(pts + list(extra)))
    return best


ex5 = [(0, 0), (4, 6), (6, 2), (2, 8)]
v.check("Ex 19-11.5a", hpwl(ex5))
v.check("Ex 19-11.5b", mst(ex5))
v.check("Ex 19-11.5c", smt(ex5))
v.check("Ex 19-11.5d", mst(ex5) / smt(ex5))
v.assert_true("lab trees agree", pnr.rmst_length(ex5) == mst(ex5) and pnr.rsmt_length(ex5) == smt(ex5)
              and pnr.hpwl(ex5) == hpwl(ex5), "")
p3 = [(2, 3), (10, 5), (6, 11)]
v.check("19-11.3a", hpwl(p3))
v.check("19-11.3b", smt(p3))
plus = [(0, 2), (2, 0), (2, 4), (4, 2)]
v.check("19-11.6a", hpwl(plus))
v.check("19-11.6b", mst(plus))
v.check("19-11.6c", smt(plus))
v.check("19-11.6d", mst(plus) / smt(plus))

rng = np.random.default_rng(1)
ratios = []
for _ in range(200):
    pts = [tuple(int(c) for c in p) for p in rng.integers(0, 10, size=(5, 2))]
    pts = list(dict.fromkeys(pts))
    if len(pts) < 2:
        continue
    ratios.append(mst(pts) / smt(pts))
v.check("Lab 19-11.b", float(np.mean(ratios)))
v.check("Lab 19-11.c", float(np.max(ratios)))
v.assert_true("Hwang's bound holds on every random net", max(ratios) <= 1.5 + 1e-12, "")


def maze_len(nrows, ncols, blocked, src, dst):
    idx = lambda r, c: r * ncols + c
    rows_, cols_ = [], []
    for r in range(nrows):
        for c in range(ncols):
            if (r, c) in blocked:
                continue
            for dr, dc in ((0, 1), (1, 0)):
                rr, cc = r + dr, c + dc
                if rr < nrows and cc < ncols and (rr, cc) not in blocked:
                    rows_ += [idx(r, c), idx(rr, cc)]
                    cols_ += [idx(rr, cc), idx(r, c)]
    g = csr_matrix((np.ones(len(rows_)), (rows_, cols_)), shape=(nrows * ncols, nrows * ncols))
    return shortest_path(g, unweighted=True, indices=idx(*src))[idx(*dst)]


wall = {(r, 3) for r in range(6)}
v.check("19-11.5a", abs(6 - 0) + abs(3 - 3))
v.check("19-11.5b", maze_len(7, 7, wall, (3, 0), (3, 6)))
grid = [[(r, c) in wall for c in range(7)] for r in range(7)]
v.assert_true("lab Lee router agrees", len(pnr.lee_route(grid, (3, 0), (3, 6))) - 1 == maze_len(7, 7, wall, (3, 0), (3, 6)), "")


# ---------------------------------------------------------------- clock trees
def elmore_side(x, r, c, t, C):
    """Elmore delay through x of distributed wire into a subtree of delay t and capacitance C."""
    return t + r * x * (c * x / 2 + C)


def tap_by_root(t1, c1, t2, c2, L, r, c):
    return brentq(lambda x: elmore_side(x, r, c, t1, c1) - elmore_side(L - x, r, c, t2, c2), -10 * L, 10 * L, xtol=1e-12)


def pi_ladder_elmore(length, r, c, n, load):
    """Elmore delay of an n-section pi ladder into a load, from the matrix of shared path resistances."""
    R = r * length / n
    C = c * length / n
    caps = np.full(n + 1, C)
    caps[0] = caps[-1] = C / 2
    caps[-1] += load
    shared = np.array([[R * min(i, j) for j in range(n + 1)] for i in range(n + 1)])
    return float((shared @ caps)[-1])


r4, c4 = 0.2, 0.2e-15
x4 = tap_by_root(15e-12, 30e-15, 15e-12, 50e-15, 400, r4, c4)
v.check("Ex 19-11.4a", x4)
v.check("Ex 19-11.4b", 1e12 * elmore_side(x4, r4, c4, 15e-12, 30e-15))
v.check("Ex 19-11.4c", 1e15 * (30e-15 + 50e-15 + c4 * 400))
v.check("Ex 19-11.4d", tap_by_root(15e-12, 30e-15, 15e-12, 30e-15, 400, r4, c4))
v.assert_true("pi ladders reproduce the continuous Elmore delay",
              abs(15e-12 + pi_ladder_elmore(x4, r4, c4, 40, 30e-15) - elmore_side(x4, r4, c4, 15e-12, 30e-15)) < 1e-20, "")
r7, c7 = 0.30, 0.20e-15
x7 = tap_by_root(10e-12, 40e-15, 12e-12, 60e-15, 500, r7, c7)
v.check("19-11.7a", x7)
v.check("19-11.7b", 1e12 * elmore_side(x7, r7, c7, 10e-12, 40e-15))
v.check("19-11.7c", 1e15 * (40e-15 + 60e-15 + c7 * 500))
x7c = tap_by_root(10e-12, 40e-15, 80e-12, 60e-15, 500, r7, c7)
v.check("19-11.7d", x7c)
snake = brentq(lambda l: elmore_side(l, r7, c7, 10e-12, 40e-15) - 80e-12, 0, 1e5)
v.check("19-11.7e", snake)
v.check("19-11.7f", snake - 500)
v.assert_true("lab merge and snake agree", abs(pnr.zero_skew_tap(10e-12, 40e-15, 12e-12, 60e-15, 500, r7, c7) - x7) < 1e-6
              and abs(pnr.snake_length(10e-12, 40e-15, 80e-12, r7, c7) - snake) < 1e-6, "")


def h_segments(cx, cy, size, levels):
    """Segments (length) of an H-tree, built recursively, and the source-to-sink path length."""
    half = size / 2
    segs = [2 * half, 2 * half, 2 * half]           # horizontal bar and two vertical bars
    path = half + half
    if levels == 1:
        return segs, path
    sub_segs, sub_path = h_segments(0, 0, size / 2, levels - 1)
    return segs + 4 * sub_segs, path + sub_path


segs, path = h_segments(0, 0, 1000.0, 3)        # first H is D/2 = 1 mm wide in a 2 mm core
v.check("19-11.8a", 4 ** 3)
v.check("19-11.8b", path / 1000)
v.check("19-11.8c", sum(segs) / 1000)
v.check("19-11.8d", sum(segs) * 0.2e-15 / 1e-12)
cclk = 20_000 * 1.794e-15 + 4.0e-12 + 2.0e-12
v.check("19-11.9a", cclk / 1e-12)
v.check("19-11.9b", 1e3 * cclk * 1.8 ** 2 * 100e6)
v.check("19-11.9c", 100 * 20_000 * 1.794e-15 / cclk)

# ---------------------------------------------------------------- SKY130 layers (R-319): rail IR drop and EM
r2 = 0.125 / 0.48
v.check("Ex 19-11.2a", r2)
v.check("Ex 19-11.2b", 1e3 * strap_bvp(r2, 2e-6, 200.0))
v.check("Ex 19-11.2c", 1e3 * strap_bvp(r2, 2e-6, 200.0, both_ends=False))
v.check("Ex 19-11.2d", brentq(lambda L: strap_bvp(r2, 2e-6, L) - 0.018, 100, 2000, xtol=1e-6))
v.check("Ex 19-11.2e", 1e3 * 2e-6 * 100)
v.check("Ex 19-11.2f", 2.8 * 0.48)
v.check("Ex 19-11.2g", 2.8 * 0.48 / (1e3 * 2e-6 * 100))
v.check("19-11.10a", 0.125 / 0.14)
v.check("19-11.10b", 0.047 / 0.30)
v.check("19-11.10c", 0.0285 / 1.6)
v.check("19-11.10d", 1.20565 / (0.125 / 0.14))
v.check("19-11.10e", 2000 * 0.047 / 0.30)
v.check("19-11.10f", 2.8 * 0.14)
v.check("19-11.10g", 6.8 * 0.30)
v.check("19-11.10h", 1.5 / 2.8)

# ---------------------------------------------------------------- routed-net delay with explicit RC ladders
LAYER = {"met1": (1.20565, 0.172375e-15), "met3": (0.166281, 0.214962e-15)}
CL6, RD6 = 2.302e-15, 5640.0


def ladder_elmore(length, layer, rd, n=40):
    r, c = LAYER[layer]
    return rd * (c * length + CL6) + pi_ladder_elmore(length, r, c, n, CL6)


def est50(length, layer, r_eff):
    """19-05's 50 % estimate with a Liberty slope r_eff: r_eff (C_w + C_L) + R_w (0.379 or 0.38 C_w + 0.69 C_L)."""
    r, c = LAYER[layer]
    return r_eff * (c * length + CL6) + r * length * (0.38 * c * length + 0.69 * CL6)


REQ6 = RD6 / math.log(2)
for key, (L, rd, layer) in {"Ex 19-11.6a": (1000, RD6, "met1"), "Ex 19-11.6b": (1000, RD6, "met3"),
                            "Ex 19-11.6c": (1000, RD6 / 8, "met1"), "Ex 19-11.6d": (1000, RD6 / 8, "met3"),
                            "Ex 19-11.6e": (3000, RD6 / 8, "met1"), "Ex 19-11.6f": (3000, RD6 / 8, "met3")}.items():
    v.check(key, 1e12 * est50(L, layer, rd))
v.check("Ex 19-11.6g", 1e12 * LAYER["met1"][0] * 3000 * (0.38 * LAYER["met1"][1] * 3000 + 0.69 * CL6))
v.check("Ex 19-11.6h", 100 * (1 - est50(1000, "met3", RD6 / 8) / est50(1000, "met1", RD6 / 8)))
v.check("Ex 19-11.6i", 1e12 * RD6 * (LAYER["met1"][1] * 1000 + CL6))
v.check("Ex 19-11.6j", 1e12 * LAYER["met1"][0] * 1000 * (0.38 * LAYER["met1"][1] * 1000 + 0.69 * CL6))
v.check("Ex 19-11.6k", REQ6 / 1e3)
v.assert_true("lab wire_delay50 agrees", abs(pnr.wire_delay50(RD6, 1205.65, 172.375e-15, CL6) - est50(1000, "met1", RD6)) < 1e-18, "")
v.assert_true("lab wire_elmore agrees with the ladder", abs(pnr.wire_elmore(REQ6, 1205.65, 172.375e-15, CL6) - ladder_elmore(1000, "met1", REQ6)) < 1e-18, "")
for key, rd in (("Lab 19-11.d", RD6), ("Lab 19-11.e", RD6 / 8)):
    v.check(key, brentq(lambda L: est50(L, "met1", rd) - est50(L, "met3", rd), 10, 1e5, xtol=1e-6))


def step_t50(length, layer, rd, n=40):
    """50 % crossing of the ladder's step response, from the matrix exponential of its state equations."""
    from scipy.linalg import expm
    r, c = LAYER[layer]
    R, C = r * length / n, c * length / n
    caps = np.array([C / 2] + [C] * (n - 1) + [C / 2])
    caps[-1] += CL6
    G = np.zeros((n + 1, n + 1))
    G[0, 0] += 1 / rd
    for k in range(n):
        G[k, k] += 1 / R
        G[k + 1, k + 1] += 1 / R
        G[k, k + 1] -= 1 / R
        G[k + 1, k] -= 1 / R
    A = -G / caps[:, None]
    ones = np.ones(n + 1)
    return brentq(lambda t: (ones - expm(A * t) @ ones)[-1] - 0.5, 1e-13, 1e-8, xtol=1e-17)


t50 = step_t50(1000, "met1", REQ6)
v.check("Lab 19-11.f", 1e12 * t50)
v.check("Lab 19-11.g", 1e12 * ladder_elmore(1000, "met1", REQ6))
v.assert_true("Elmore constant bounds the 50 % delay", t50 < ladder_elmore(1000, "met1", REQ6), "")
v.assert_true("estimate within 0.5 % of the ladder's 50 % delay", abs(est50(1000, "met1", RD6) / t50 - 1) < 0.005, "")
v.check("Txt 19-11.a", 100 * (1 - 0.5 / 0.7))

sys.exit(v.finish())
