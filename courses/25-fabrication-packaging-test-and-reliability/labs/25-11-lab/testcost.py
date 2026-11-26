"""Production-test models for lab 25-11.

Multisite test time and cost, a weak-subpopulation burn-in model (closed form and Monte Carlo), speed-bin
fractions and revenue, and escapes and overkill at a guard-banded limit (integration and Monte Carlo).
Times in seconds or hours as labelled; frequencies in GHz.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, stats


def multisite_time(t1: float, n: int, eta: float) -> float:
    return t1 * (1 + (n - 1) * (1 - eta))


def multisite_eta(t1: float, tn: float, n: int) -> float:
    return 1 - (tn - t1) / ((n - 1) * t1)


def cost_per_die(rate_per_h: float, t1: float, n: int, eta: float, index_s: float) -> float:
    return rate_per_h / 3600 * (multisite_time(t1, n, eta) + index_s) / n


def weak_fail(t_h: float, eta_h: float, beta: float) -> float:
    return 1 - math.exp(-((t_h / eta_h) ** beta))


def burn_in_for(p_weak: float, target: float, eta_h: float, beta: float) -> float:
    """Use-equivalent burn-in hours that leave `target` weak fraction shipped."""
    return eta_h * math.log(p_weak / target) ** (1 / beta)


def simulate_burn_in(p_weak: float, eta_h: float, beta: float, t_eq: float, n: int = 2_000_000,
                     seed: int = 2) -> float:
    """Fraction of the weak population removed by a burn-in of t_eq use hours (Monte Carlo)."""
    rng = np.random.default_rng(seed)
    n_weak = rng.binomial(n, p_weak)
    lives = eta_h * rng.weibull(beta, size=n_weak)
    return float(np.mean(lives < t_eq))


def bin_fractions(mu: float, sigma: float, thresholds: list[float]) -> list[float]:
    """Fractions above the first threshold, then between successive thresholds, then below the last."""
    cdf = [stats.norm.cdf(t, mu, sigma) for t in thresholds]
    out = [1 - cdf[0]] + [cdf[i] - cdf[i + 1] for i in range(len(cdf) - 1)] + [cdf[-1]]
    return out


def bin_revenue(mu: float, sigma: float, thresholds: list[float], prices: list[float], guard: float = 0.0) -> float:
    fr = bin_fractions(mu, sigma, [t + guard for t in thresholds])
    return float(sum(f * p for f, p in zip(fr, prices)))


def escapes_overkill(limit: float, guard: float, mu: float, sigma: float, sigma_m: float) -> tuple[float, float]:
    esc = integrate.quad(lambda x: stats.norm.pdf(x, mu, sigma) * stats.norm.sf(limit + guard, x, sigma_m),
                         mu - 10 * sigma, limit)[0]
    ovk = integrate.quad(lambda x: stats.norm.pdf(x, mu, sigma) * stats.norm.cdf(limit + guard, x, sigma_m),
                         limit, mu + 10 * sigma)[0]
    return esc, ovk


def simulate_escapes(limit: float, guard: float, mu: float, sigma: float, sigma_m: float, n: int = 4_000_000,
                     seed: int = 4) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    f = rng.normal(mu, sigma, n)
    m = f + rng.normal(0, sigma_m, n)
    ship = m >= limit + guard
    return float(np.mean(ship & (f < limit))), float(np.mean(~ship & (f >= limit)))
