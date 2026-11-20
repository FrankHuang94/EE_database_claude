"""Lab 15-02 helpers: polynomial transfer functions, block-diagram algebra and Mason's gain formula.

Everything is plain numpy/scipy (and sympy for symbolic gains in `mason`), so each step can be read.

    TF(num, den)            transfer function from coefficient lists, highest power first
    G1 * G2, G1 + G2        series and parallel connection
    feedback(G, H, sign=-1) closed loop G / (1 - sign*G*H); sign=-1 is negative feedback
    tf_from_ss(A, B, C, D)  SISO transfer function of a state-space model
    mason(edges, src, dst)  Mason's gain formula on a signal-flow graph
    solve_graph(...)        the same transfer function by solving the node equations directly
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
from scipy import signal


def _trim(p):
    p = np.atleast_1d(np.asarray(p, dtype=float))
    nz = np.flatnonzero(np.abs(p) > 1e-14 * max(1.0, np.max(np.abs(p))))
    return p[nz[0]:] if nz.size else np.array([0.0])


@dataclass
class TF:
    """A SISO rational transfer function num(s)/den(s); coefficients highest power first."""

    num: np.ndarray
    den: np.ndarray

    def __post_init__(self):
        self.num = _trim(self.num)
        self.den = _trim(self.den)
        lead = self.den[0]
        self.num = self.num / lead      # make the denominator monic
        self.den = self.den / lead

    # -- connections -----------------------------------------------------------------------------
    def __mul__(self, other):
        other = _as_tf(other)
        return TF(np.polymul(self.num, other.num), np.polymul(self.den, other.den))

    __rmul__ = __mul__

    def __add__(self, other):
        other = _as_tf(other)
        num = np.polyadd(np.polymul(self.num, other.den), np.polymul(other.num, self.den))
        return TF(num, np.polymul(self.den, other.den))

    __radd__ = __add__

    def __neg__(self):
        return TF(-self.num, self.den)

    def __sub__(self, other):
        return self + (-_as_tf(other))

    # -- properties ------------------------------------------------------------------------------
    def __call__(self, s):
        return np.polyval(self.num, s) / np.polyval(self.den, s)

    def poles(self):
        return np.roots(self.den)

    def zeros(self):
        return np.roots(self.num) if len(self.num) > 1 else np.array([])

    def dcgain(self):
        return self(0.0)

    def minreal(self, tol=1e-6):
        """Cancel (numerically) coincident pole-zero pairs. Use with care: see chapter section 3.2."""
        z, p = list(self.zeros()), list(self.poles())
        k = self.num[0]
        for zi in list(z):
            for pi in p:
                if abs(zi - pi) < tol * max(1.0, abs(pi)):
                    z.remove(zi)
                    p.remove(pi)
                    break
        return TF(np.real(k * np.poly(z)) if z else [k], np.real(np.poly(p)) if p else [1.0])

    def step(self, t):
        """Unit-step response sampled at the times t."""
        _, y = signal.step(signal.TransferFunction(self.num, self.den), T=t)
        return y

    def __repr__(self):
        return f"TF(num={np.round(self.num, 6).tolist()}, den={np.round(self.den, 6).tolist()})"


def _as_tf(x):
    return x if isinstance(x, TF) else TF([float(x)], [1.0])


def feedback(G, H=1.0, sign=-1):
    """Closed-loop transfer function of forward path G with feedback H; sign=-1 for negative feedback.

    Y = G E, E = R + sign*H Y  =>  Y/R = G / (1 - sign*G*H), formed over a common denominator so that no
    pole-zero pair is cancelled silently.
    """
    G, H = _as_tf(G), _as_tf(H)
    num = np.polymul(G.num, H.den)
    den = np.polyadd(np.polymul(G.den, H.den), -sign * np.polymul(G.num, H.num))
    return TF(num, den)


def tf_from_ss(A, B, C, D=0.0):
    """Transfer function C (sI - A)^-1 B + D of a single-input single-output state-space model.

    Uses the matrix determinant lemma: det(sI - A + B C) = det(sI - A) * (1 + C (sI - A)^-1 B), so the
    numerator of C (sI - A)^-1 B is det(sI - A + BC) - det(sI - A). The denominator is det(sI - A), whose
    roots are the eigenvalues of A.
    """
    A = np.atleast_2d(np.asarray(A, dtype=float))
    B = np.asarray(B, dtype=float).reshape(-1, 1)
    C = np.asarray(C, dtype=float).reshape(1, -1)
    den = np.poly(A)                       # det(sI - A), monic
    num = np.polysub(np.poly(A - B @ C), den)
    num = np.polyadd(num, float(D) * den)
    return TF(num, den)


# ---------------------------------------------------------------------------------- signal-flow graphs
def _adjacency(edges):
    adj: dict = {}
    for u, v, g in edges:
        adj.setdefault(u, []).append((v, g))
        adj.setdefault(v, [])
    return adj


def forward_paths(edges, src, dst):
    """All paths src -> dst that visit no node twice, as (node list, gain)."""
    adj = _adjacency(edges)
    out = []

    def dfs(node, nodes, gain):
        if node == dst:
            out.append((nodes, gain))
            return
        for nxt, g in adj[node]:
            if nxt not in nodes:
                dfs(nxt, nodes + [nxt], gain * g)

    dfs(src, [src], 1)
    return out


def loops(edges):
    """All simple cycles, each reported once (starting from its smallest node in a fixed order)."""
    adj = _adjacency(edges)
    order = {n: i for i, n in enumerate(adj)}
    out = []
    for start in adj:
        def dfs(node, nodes, gain):
            for nxt, g in adj[node]:
                if nxt == start:
                    out.append((nodes, gain * g))
                elif order[nxt] > order[start] and nxt not in nodes:
                    dfs(nxt, nodes + [nxt], gain * g)

        dfs(start, [start], 1)
    return out


def graph_determinant(loop_list):
    """Mason's Delta = 1 - sum(L) + sum(pairs of non-touching L) - sum(triples) + ..."""
    sets = [set(n) for n, _ in loop_list]
    gains = [g for _, g in loop_list]
    delta = 1
    k = 1
    while True:
        term = 0
        found = False
        for combo in combinations(range(len(loop_list)), k):
            nodes = [sets[i] for i in combo]
            if all(nodes[a].isdisjoint(nodes[b]) for a in range(k) for b in range(a + 1, k)):
                found = True
                prod = 1
                for i in combo:
                    prod = prod * gains[i]
                term = term + prod
        if not found:
            return delta
        delta = delta + (-1) ** k * term
        k += 1


def mason(edges, src, dst, detail=False):
    """Transfer function src -> dst of the signal-flow graph `edges` = [(u, v, gain), ...].

    Gains may be numbers or sympy expressions. With detail=True also returns the paths, loops, Delta and
    the cofactors Delta_k.
    """
    paths = forward_paths(edges, src, dst)
    lps = loops(edges)
    delta = graph_determinant(lps)
    num = 0
    cof = []
    for nodes, gain in paths:
        untouched = [lp for lp in lps if set(lp[0]).isdisjoint(nodes)]
        dk = graph_determinant(untouched)
        cof.append(dk)
        num = num + gain * dk
    T = num / delta
    if detail:
        return T, dict(paths=paths, loops=lps, delta=delta, cofactors=cof)
    return T


def solve_graph(edges, src, dst):
    """The same transfer function by solving x = M x + b r for numeric gains (an independent check)."""
    nodes = list(_adjacency(edges))
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    M = np.zeros((n, n), dtype=complex)
    for u, v, g in edges:
        M[idx[v], idx[u]] += complex(g)
    # the source node is driven externally: its own equation is x_src = r
    A = np.eye(n, dtype=complex) - M
    A[idx[src], :] = 0
    A[idx[src], idx[src]] = 1
    b = np.zeros(n, dtype=complex)
    b[idx[src]] = 1
    x = np.linalg.solve(A, b)
    val = x[idx[dst]]
    return val.real if abs(val.imag) < 1e-12 * max(1.0, abs(val)) else val


def second_order_specs(zeta, wn):
    """Overshoot (fraction) and peak time of the standard underdamped second-order step response."""
    wd = wn * np.sqrt(1 - zeta**2)
    return np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2)), np.pi / wd
