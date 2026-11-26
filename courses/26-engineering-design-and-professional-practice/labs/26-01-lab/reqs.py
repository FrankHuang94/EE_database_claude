"""Requirements arithmetic for Lab 26-01: flow-down, budgets, traceability value and decisions.

Every function is short and self-contained so it can be read next to the chapter:

- duty-cycle averages and battery life (Example 26-01.2);
- worst-case, RSS and correlated stacking of error contributions, the two-sided Gaussian
  out-of-spec fraction and a Monte Carlo of the same budget (Example 26-01.3);
- expected escape cost of untested requirements (Example 26-01.4);
- the phase-by-phase defect-escalation model (Example 26-01.5);
- weighted decision matrices and the weight at which a ranking flips (Example 26-01.6).
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np
from scipy.stats import norm


# ---------------------------------------------------------------- flow-down
def duty_average(profile: Iterable[tuple[float, float]]) -> float:
    """Average of a quantity over a duty-cycle profile [(fraction of time, value), ...]."""
    profile = list(profile)
    total = sum(d for d, _ in profile)
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"duty fractions sum to {total}, not 1")
    return sum(d * x for d, x in profile)


def battery_life_h(capacity_mah: float, usable: float, i_avg_ma: float) -> float:
    """Hours of operation from a battery's usable charge at an average current."""
    return capacity_mah * usable / i_avg_ma


# ---------------------------------------------------------------- budgets
def stack_worst(bounds: Sequence[float]) -> float:
    """Worst-case stack: every contribution at its bound, same sign."""
    return float(sum(abs(b) for b in bounds))


def stack_rss(bounds: Sequence[float]) -> float:
    """Root-sum-square stack of independent contributions given at a common k-sigma level."""
    return float(math.sqrt(sum(b * b for b in bounds)))


def stack_corr(sigmas: Sequence[float], rho: np.ndarray) -> float:
    """Standard deviation of a sum of contributions with correlation matrix rho."""
    s = np.asarray(sigmas, dtype=float)
    return float(math.sqrt(s @ np.asarray(rho, dtype=float) @ s))


def p_outside(sigma: float, limit: float, mean: float = 0.0) -> float:
    """Probability that a Gaussian total N(mean, sigma) falls outside +/- limit."""
    return float(norm.sf((limit - mean) / sigma) + norm.cdf((-limit - mean) / sigma))


def mc_budget(bounds: Sequence[float], k: float = 3.0, n: int = 1_000_000, dist: str = "normal",
              groups: Sequence[Sequence[int]] | None = None, seed: int = 26) -> np.ndarray:
    """Monte Carlo samples of a summed error budget.

    bounds: each contribution's +/- bound; for 'normal' the bound is k sigma, for 'uniform' it is the
    half-width of a uniform distribution. groups: lists of indices that share one random draw
    (perfect correlation, same sign); contributions not in any group are independent.
    """
    rng = np.random.default_rng(seed)
    b = np.asarray(bounds, dtype=float)
    groups = [list(g) for g in (groups or [])]
    owner = {i: gi for gi, g in enumerate(groups) for i in g}
    draws = {}
    total = np.zeros(n)
    for i, bi in enumerate(b):
        key = ("g", owner[i]) if i in owner else ("i", i)
        if key not in draws:
            if dist == "normal":
                draws[key] = rng.standard_normal(n)
            elif dist == "uniform":
                draws[key] = rng.uniform(-1.0, 1.0, n)
            else:
                raise ValueError(dist)
        unit = draws[key]
        total += bi / k * unit if dist == "normal" else bi * unit
    return total


# ---------------------------------------------------------------- traceability and escalation
def escape_cost(untested: Sequence[tuple[int, float]], cost_per_escape: float) -> float:
    """Expected cost of untested requirements [(count, probability a defect escapes), ...]."""
    return sum(nr * p for nr, p in untested) * cost_per_escape


def defect_flow(n: float, p_detect: Sequence[float], factors: Sequence[float]) -> tuple[list[float], float]:
    """Defects found in each phase and the total relative cost.

    p_detect: the fraction of the defects still present that each phase catches (the last phase,
    operations, catches whatever remains, so it is not listed). factors: relative cost to fix in each
    phase, one more entry than p_detect (the last is operations).
    """
    if len(factors) != len(p_detect) + 1:
        raise ValueError("need one cost factor per phase including operations")
    found, left = [], float(n)
    for p in p_detect:
        f = p * left
        found.append(f)
        left -= f
    found.append(left)
    return found, float(sum(f * c for f, c in zip(found, factors)))


# ---------------------------------------------------------------- decisions
def weighted_scores(weights: Sequence[float], scores: np.ndarray) -> np.ndarray:
    """Weighted-sum score of each option (rows) over criteria (columns)."""
    w = np.asarray(weights, dtype=float)
    if abs(w.sum() - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1")
    return np.asarray(scores, dtype=float) @ w


def scores_vs_weight(weights: Sequence[float], scores: np.ndarray, j: int, wj: np.ndarray) -> np.ndarray:
    """Scores as criterion j's weight sweeps over wj, the others rescaled in their base proportions."""
    w0 = np.asarray(weights, dtype=float)
    rest = np.delete(np.arange(len(w0)), j)
    out = []
    for x in np.atleast_1d(wj):
        w = np.empty_like(w0)
        w[j] = x
        w[rest] = w0[rest] / w0[rest].sum() * (1.0 - x)
        out.append(np.asarray(scores, dtype=float) @ w)
    return np.array(out)


def flip_weight(weights: Sequence[float], scores: np.ndarray, j: int, a: int, b: int) -> float:
    """Weight on criterion j at which options a and b tie (closed form for the linear sweep)."""
    w0 = np.asarray(weights, dtype=float)
    s = np.asarray(scores, dtype=float)
    rest = np.delete(np.arange(len(w0)), j)
    r = s[:, rest] @ (w0[rest] / w0[rest].sum())
    d_rest, d_j = r[a] - r[b], s[a, j] - s[b, j]
    return float(d_rest / (d_rest - d_j))
