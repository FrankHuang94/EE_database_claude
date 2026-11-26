"""Schedule and respin-risk models for Lab 26-05.

- PERT three-point estimates, path statistics, the normal approximation to the chance of meeting a date,
  merge bias where parallel paths join, and a Monte Carlo schedule with beta-PERT task durations
  (Example 26-05.2);
- expected tape-outs, delay and cost when each spin succeeds with its own probability (Example 26-05.1);
- metal-only ECO against a full respin (Example 26-05.3);
- a risk register with expected monetary value and mitigation chosen under a budget (Example 26-05.4);
- when to tape out: exponential bug discovery, Poisson escapes and the cost-minimizing verification time,
  with and without emulation (Examples 26-05.5 and 26-05.6).
Times in weeks unless stated; money in $ M.
"""
from __future__ import annotations

import math
from itertools import combinations
from typing import Sequence

import numpy as np
from scipy import optimize, stats


# ---------------------------------------------------------------- PERT schedules
def pert_mean(a: float, m: float, b: float) -> float:
    return (a + 4 * m + b) / 6


def pert_sd(a: float, m: float, b: float) -> float:
    return (b - a) / 6


def path_stats(tasks: Sequence[tuple[float, float, float]]) -> tuple[float, float]:
    """Mean and standard deviation of a chain of independent tasks."""
    mu = sum(pert_mean(*t) for t in tasks)
    var = sum(pert_sd(*t) ** 2 for t in tasks)
    return mu, math.sqrt(var)


def p_by(T: float, mu: float, sd: float) -> float:
    return float(stats.norm.cdf((T - mu) / sd))


def p_all_by(T: float, paths: Sequence[tuple[float, float]]) -> float:
    """Chance that every independent parallel path is done by T (merge bias)."""
    return float(np.prod([p_by(T, mu, sd) for mu, sd in paths]))


def date_for(conf: float, paths: Sequence[tuple[float, float]]) -> float:
    lo = max(mu for mu, _ in paths)
    return optimize.brentq(lambda T: p_all_by(T, paths) - conf, lo - 50, lo + 200)


def beta_pert_sample(a, m, b, n, rng):
    """Beta-PERT with shape 4: alpha = 1 + 4(m - a)/(b - a), beta = 1 + 4(b - m)/(b - a)."""
    al = 1 + 4 * (m - a) / (b - a)
    be = 1 + 4 * (b - m) / (b - a)
    return a + (b - a) * rng.beta(al, be, n)


def simulate_tapeout(paths: Sequence[Sequence[tuple[float, float, float]]], n: int = 200_000, seed: int = 7):
    rng = np.random.default_rng(seed)
    ends = [sum(beta_pert_sample(*t, n, rng) for t in p) for p in paths]
    return np.max(np.vstack(ends), axis=0)


# ---------------------------------------------------------------- respins
def expected_spins(q: Sequence[float]) -> float:
    """E[number of tape-outs] when spin k succeeds with probability q[k] (last q must be 1)."""
    e, alive = 0.0, 1.0
    for qk in q:
        e += alive
        alive *= 1 - qk
    return e


def spin_distribution(q: Sequence[float]) -> list[float]:
    """P(exactly k tape-outs) for k = 1, 2, ..."""
    out, alive = [], 1.0
    for qk in q:
        out.append(alive * qk)
        alive *= 1 - qk
    return out


def eco_cost(masks: float, engineering: float, weeks: float, slip_per_week: float) -> float:
    return masks + engineering + weeks * slip_per_week


# ---------------------------------------------------------------- risk register
def emv(risks: Sequence[tuple[float, float]]) -> float:
    """Expected monetary value: sum of probability x impact."""
    return sum(p * c for p, c in risks)


def best_mitigations(risks, mitigations, budget):
    """risks: [(p, impact)]; mitigations: [(cost, p_after)] per risk. Exhaustive search under a budget;
    returns (chosen indices, net benefit)."""
    best = ((), 0.0)
    n = len(risks)
    for k in range(1, n + 1):
        for combo in combinations(range(n), k):
            cost = sum(mitigations[i][0] for i in combo)
            if cost > budget + 1e-12:
                continue
            gain = sum((risks[i][0] - mitigations[i][1]) * risks[i][1] for i in combo) - cost
            if gain > best[1] + 1e-12:
                best = (combo, gain)
    return best


# ---------------------------------------------------------------- when to tape out
def escapes(t: float, n0: float, tau: float, phi: float = 1.0) -> float:
    """Expected respin-class bugs still in the design after t weeks of verification."""
    return phi * n0 * math.exp(-t / tau)


def p_respin(t: float, n0: float, tau: float, phi: float = 1.0) -> float:
    """Poisson escapes: P(at least one respin-class bug escapes)."""
    return 1 - math.exp(-escapes(t, n0, tau, phi))


def total_cost(t, n0, tau, phi, c_week, c_respin, fixed=0.0):
    return fixed + c_week * t + c_respin * p_respin(t, n0, tau, phi)


def optimal_tapeout(n0, tau, phi, c_week, c_respin):
    """Stationary point: lambda exp(-lambda) = c_week tau / c_respin, the smaller root (a minimum)."""
    k = c_week * tau / c_respin
    lam = optimize.brentq(lambda x: x * math.exp(-x) - k, 1e-12, 1.0)
    t = tau * math.log(phi * n0 / lam)
    return max(t, 0.0), lam
