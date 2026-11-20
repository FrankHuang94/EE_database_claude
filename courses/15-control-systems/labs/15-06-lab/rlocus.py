"""Lab 15-06 helpers: root loci computed numerically and the sketching rules computed exactly.

The loop is 1 + K N(s)/D(s) = 0 with polynomials N (zeros) and D (poles), highest power first, K >= 0.

    locus(N, D, Ks)                closed-loop roots for each K, ordered so that branches are continuous
    asymptotes(N, D)               (angles in degrees, centroid) for the n - m branches that go to infinity
    real_axis_segments(N, D)       intervals of the real axis on the locus (odd count of poles+zeros to the right)
    breakpoints(N, D)              real break-away / break-in points with their K (> 0) from N D' - D N' = 0
    departure_angle(N, D, p)       angle (degrees) at which the branch leaves the complex pole p
    gain_at(N, D, s0)              K that places a closed-loop pole at s0 (magnitude condition)
    on_locus(N, D, s0)             True if s0 satisfies the angle condition
    zeta_point(N, D, zeta, r_max)  points of the locus on the ray of constant damping ratio zeta
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq, linear_sum_assignment


def _p(c):
    return np.atleast_1d(np.asarray(c, dtype=float))


def char_poly(N, D, K):
    return np.polyadd(_p(D), K * _p(N))


def locus(N, D, Ks):
    """Roots of D + K N for each K, matched to the previous step's roots (minimum total movement)."""
    out = []
    prev = None
    for K in Ks:
        r = np.roots(char_poly(N, D, K))
        if prev is not None and len(r) == len(prev):
            cost = np.abs(prev[:, None] - r[None, :])
            _, j = linear_sum_assignment(cost)
            r = r[j]
        out.append(r)
        prev = r
    return np.array(out)


def asymptotes(N, D):
    n, m = len(_p(D)) - 1, len(_p(N)) - 1
    q = n - m
    if q <= 0:
        return [], None
    angles = [(2 * k + 1) * 180.0 / q for k in range(q)]
    centroid = (np.sum(np.roots(D)).real - (np.sum(np.roots(N)).real if m > 0 else 0.0)) / q
    return angles, centroid


def on_real_axis(N, D, x):
    crit = np.concatenate([np.roots(D), np.roots(N) if len(_p(N)) > 1 else []])
    real = [c.real for c in crit if abs(c.imag) < 1e-9]
    return sum(1 for c in real if c > x) % 2 == 1


def real_axis_segments(N, D, lo=-1e6):
    crit = np.concatenate([np.roots(D), np.roots(N) if len(_p(N)) > 1 else []])
    pts = sorted({round(c.real, 12) for c in crit if abs(c.imag) < 1e-9}, reverse=True)
    edges = pts + [lo]
    segs = []
    hi = pts[0]
    for a, b in zip(edges[:-1], edges[1:]):
        mid = (a + b) / 2
        if on_real_axis(N, D, mid):
            segs.append((b, a))
    return segs


def breakpoints(N, D):
    """Real roots of N D' - D N' that lie on the locus with K > 0, and their gains."""
    N, D = _p(N), _p(D)
    q = np.polysub(np.polymul(N, np.polyder(D)), np.polymul(D, np.polyder(N)))
    out = []
    for r in np.roots(q):
        if abs(r.imag) < 1e-9:
            x = r.real
            K = -np.polyval(D, x) / np.polyval(N, x)
            if K > 0:
                out.append((x, K))
    return sorted(out)


def departure_angle(N, D, p):
    """180 - sum(angles from other poles) + sum(angles from zeros), in degrees, wrapped to (-180, 180]."""
    poles = [q for q in np.roots(D) if abs(q - p) > 1e-9]
    zeros = np.roots(N) if len(_p(N)) > 1 else []
    ang = 180.0 - sum(math.degrees(np.angle(p - q)) for q in poles) + sum(math.degrees(np.angle(p - z)) for z in zeros)
    return (ang + 180.0) % 360.0 - 180.0


def gain_at(N, D, s0):
    return abs(np.polyval(D, s0)) / abs(np.polyval(N, s0))


def on_locus(N, D, s0, tol=1e-6):
    g = np.polyval(N, s0) / np.polyval(D, s0)
    return abs(abs(np.angle(g)) - math.pi) < tol


def zeta_point(N, D, zeta, r_max, n=200001):
    """Points s = r(-zeta + j sqrt(1 - zeta^2)) on the locus (angle condition), 0 < r < r_max, with their K."""
    u = complex(-zeta, math.sqrt(1 - zeta**2))
    f = lambda r: np.imag(np.polyval(N, r * u) / np.polyval(D, r * u))  # noqa: E731
    rs = np.linspace(r_max / n, r_max, n)
    vals = np.array([f(r) for r in rs])
    out = []
    for i in np.flatnonzero(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0):
        r = brentq(f, rs[i], rs[i + 1], xtol=1e-14)
        s0 = r * u
        if on_locus(N, D, s0):
            out.append((s0, gain_at(N, D, s0)))
    return out
