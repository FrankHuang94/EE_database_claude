"""Physical-design models for Lab 19-11: floorplan, power grid, placement, routing and clock trees.

Units are SI unless a name says otherwise (lengths in um where marked, resistances in ohms, capacitances in farads,
times in seconds).
"""
from __future__ import annotations

import heapq
import itertools
import math
from collections import deque

import numpy as np


# ---------------------------------------------------------------- floorplan
def core_dimensions(cell_area_um2, utilization, aspect=1.0, row_height_um=2.72):
    """Core width and height (um) and the number of rows for a target utilization and aspect ratio (height/width)."""
    core = cell_area_um2 / utilization
    width = math.sqrt(core / aspect)
    rows = math.ceil(width * aspect / row_height_um)
    return width, rows * row_height_um, rows


# ---------------------------------------------------------------- IR drop on a power strap
def strap_drop_continuous(i_total, r_total, both_ends=True):
    """Worst IR drop on a uniform strap drawing a uniformly distributed current i_total: I R / 8 when fed from both
    ends (worst at the middle), I R / 2 when fed from one end (worst at the far end)."""
    return i_total * r_total / (8.0 if both_ends else 2.0)


def strap_drop_ladder(i_total, r_total, n, both_ends=True):
    """Voltage drops at the nodes of a strap discretized into n equal segments. Each interior node draws i_total / n
    (the trapezoidal share of a uniform load); a fed end's half-share flows straight into the supply, and with a
    one-end feed the far end draws i_total / (2n). Solved by nodal analysis; at the nodes this matches the continuous
    strap exactly."""
    g = n / r_total
    if both_ends:
        m = n - 1                      # interior nodes; both ends held at the supply
        taps = np.full(m, i_total / n)
        G = np.zeros((m, m))
        for k in range(m):
            G[k, k] = 2 * g
            if k > 0:
                G[k, k - 1] = -g
            if k < m - 1:
                G[k, k + 1] = -g
        return np.linalg.solve(G, taps)
    m = n                              # nodes 1..n; node 0 at the supply
    taps = np.full(m, i_total / n)
    taps[-1] = i_total / (2 * n)
    G = np.zeros((m, m))
    for k in range(m):
        G[k, k] = 2 * g if k < m - 1 else g
        if k > 0:
            G[k, k - 1] = -g
        if k < m - 1:
            G[k, k + 1] = -g
    return np.linalg.solve(G, taps)


def max_strap_spacing(dv_max, r_per_length, i_per_length):
    """Largest length between supply feeds (both ends) that keeps the drop below dv_max: r i L^2 / 8 = dv_max."""
    return math.sqrt(8 * dv_max / (r_per_length * i_per_length))


# ---------------------------------------------------------------- quadratic placement
def quadratic_place(n_cells, nets, fixed):
    """Minimize sum w (x_i - x_j)^2 + (y_i - y_j)^2 over two-pin connections.
    nets: list of (a, b, w) where a, b are cell indices (int) or fixed-pin names (str); fixed: {name: (x, y)}.
    Returns an (n_cells, 2) array of positions. Setting the gradient to zero gives Q x = b in each axis."""
    Q = np.zeros((n_cells, n_cells))
    bx = np.zeros(n_cells)
    by = np.zeros(n_cells)
    for a, b, w in nets:
        for p, q in ((a, b), (b, a)):
            if isinstance(p, int):
                Q[p, p] += w
                if isinstance(q, int):
                    Q[p, q] -= w
                else:
                    bx[p] += w * fixed[q][0]
                    by[p] += w * fixed[q][1]
    return np.column_stack([np.linalg.solve(Q, bx), np.linalg.solve(Q, by)])


def hpwl(points):
    """Half-perimeter wirelength of a set of pins."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (max(xs) - min(xs)) + (max(ys) - min(ys))


# ---------------------------------------------------------------- routing
def lee_route(grid, src, dst):
    """Lee's maze router: breadth-first wave expansion on a grid (True = blocked), then backtrace.
    Returns the list of cells on a shortest path (inclusive), or None. Path length in steps = len - 1."""
    rows, cols = len(grid), len(grid[0])
    dist = {src: 0}
    prev = {}
    q = deque([src])
    while q:
        cur = q.popleft()
        if cur == dst:
            break
        r, c = cur
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and not grid[nr][nc] and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[cur] + 1
                prev[(nr, nc)] = cur
                q.append((nr, nc))
    if dst not in dist:
        return None
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    return path[::-1]


def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def rmst_length(points):
    """Rectilinear minimum spanning tree length (Prim's algorithm)."""
    pts = list(points)
    in_tree = {0}
    best = {k: manhattan(pts[0], pts[k]) for k in range(1, len(pts))}
    total = 0
    while best:
        k = min(best, key=best.get)
        total += best.pop(k)
        in_tree.add(k)
        for j in best:
            best[j] = min(best[j], manhattan(pts[k], pts[j]))
    return total


def rmst_edges(points):
    """Edges (i, j) of a rectilinear minimum spanning tree (Prim)."""
    pts = list(points)
    best = {k: (manhattan(pts[0], pts[k]), 0) for k in range(1, len(pts))}
    edges = []
    while best:
        k = min(best, key=lambda j: best[j][0])
        edges.append((best.pop(k)[1], k))
        for j in best:
            d = manhattan(pts[k], pts[j])
            if d < best[j][0]:
                best[j] = (d, k)
    return edges


def rsmt_points(points):
    """Pins plus the Hanan Steiner points of a minimum tree (exhaustive; small nets only)."""
    pts = [tuple(p) for p in points]
    xs = sorted({p[0] for p in pts})
    ys = sorted({p[1] for p in pts})
    hanan = [(x, y) for x in xs for y in ys if (x, y) not in pts]
    best, best_pts = rmst_length(pts), pts
    for k in range(1, len(pts) - 1):
        for extra in itertools.combinations(hanan, k):
            length = rmst_length(pts + list(extra))
            if length < best - 1e-12:
                best, best_pts = length, pts + list(extra)
    return best_pts


def rsmt_length(points):
    """Rectilinear Steiner minimum tree length by exhaustive search over Hanan-grid Steiner points (Hanan's theorem:
    some optimal tree uses only Hanan points; at most n - 2 Steiner points are needed). Small nets only."""
    pts = [tuple(p) for p in points]
    xs = sorted({p[0] for p in pts})
    ys = sorted({p[1] for p in pts})
    hanan = [(x, y) for x in xs for y in ys if (x, y) not in pts]
    best = rmst_length(pts)
    for k in range(1, len(pts) - 1):
        for extra in itertools.combinations(hanan, k):
            best = min(best, rmst_length(pts + list(extra)))
    return best


# ---------------------------------------------------------------- clock trees: Elmore constant and zero-skew merging
def zero_skew_tap(t1, c1, t2, c2, length, r, c):
    """Tapping point x (distance from subtree 1 along a wire of the given length) at which the Elmore constants to the
    two subtrees are equal. t: subtree delay from its root (s), C: subtree capacitance (F), r, c per unit length.
    Returns x; x outside [0, length] means the wire must be lengthened (snaked) on one side."""
    return (t2 - t1 + r * length * (c2 + c * length / 2)) / (r * (c1 + c2 + c * length))


def merged(t1, c1, t2, c2, length, r, c):
    """Delay from the tapping point to the sinks, and the merged subtree's capacitance, for a zero-skew merge
    (when 0 <= x <= length)."""
    x = zero_skew_tap(t1, c1, t2, c2, length, r, c)
    t = t1 + r * x * (c * x / 2 + c1)
    return x, t, c1 + c2 + c * length


def snake_length(t_fast, c_fast, t_slow, r, c):
    """Wire length that, tapped at the slow subtree's root, adds exactly (t_slow - t_fast) of Elmore constant to the fast
    subtree: r l (c l / 2 + C_fast) = t_slow - t_fast, the positive root of a quadratic."""
    a = r * c / 2
    b = r * c_fast
    d = t_slow - t_fast
    return (-b + math.sqrt(b * b + 4 * a * d)) / (2 * a)


def elmore_tree(edges, root, caps):
    """Elmore constant from the root to every node of an RC tree. edges: {child: (parent, R)}; caps: {node: C}.
    Delay(n) = sum over resistors on the root-to-n path of R times the capacitance downstream of that resistor."""
    children = {}
    for ch, (par, _) in edges.items():
        children.setdefault(par, []).append(ch)

    def down(n):
        return caps.get(n, 0.0) + sum(down(k) for k in children.get(n, []))
    delay = {root: 0.0}

    def walk(n):
        for k in children.get(n, []):
            delay[k] = delay[n] + edges[k][1] * down(k)
            walk(k)
    walk(root)
    return delay


def wire_delay50(r_eff, r_wire, c_wire, c_load):
    """50 % delay estimate of a driver into a distributed wire and a load (19-05): r_eff (C_w + C_L) +
    R_w (0.38 C_w + 0.69 C_L), where r_eff is a Liberty delay-versus-load slope (it already contains ln 2)."""
    return r_eff * (c_wire + c_load) + r_wire * (0.38 * c_wire + 0.69 * c_load)


def wire_elmore(r_drv, r_wire, c_wire, c_load):
    """Elmore constant of a driver resistance into a distributed wire (lumped as half its capacitance at each end in
    the Elmore sense) and a load: R_d (C_w + C_L) + R_w (C_w / 2 + C_L)."""
    return r_drv * (c_wire + c_load) + r_wire * (c_wire / 2 + c_load)
