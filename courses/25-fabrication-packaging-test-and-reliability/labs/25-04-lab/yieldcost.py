"""Yield and die-cost models for lab 25-04.

Exact die counting on an optimized grid, the dies-per-wafer formula, Poisson, Murphy and
negative-binomial yields, a wafer-map Monte Carlo with random or clustered defects, cost per good
die, harvesting and yield learning. Lengths in mm, areas in mm2 unless stated; defect density in cm^-2.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize


def dpw_formula(diameter_mm: float, area_mm2: float) -> float:
    return math.pi * diameter_mm**2 / (4 * area_mm2) - math.pi * diameter_mm / math.sqrt(2 * area_mm2)


def die_sites(diameter_mm: float, pitch_x: float, pitch_y: float, ox: float, oy: float) -> np.ndarray:
    """Lower-left corners of whole dies inside a circle for a grid offset (ox, oy)."""
    r = diameter_mm / 2
    xs = np.arange(-r - pitch_x + ox, r + pitch_x, pitch_x)
    ys = np.arange(-r - pitch_y + oy, r + pitch_y, pitch_y)
    x, y = np.meshgrid(xs, ys)
    far = np.maximum(np.abs(x), np.abs(x + pitch_x)) ** 2 + np.maximum(np.abs(y), np.abs(y + pitch_y)) ** 2
    ok = far <= r**2
    return np.column_stack([x[ok], y[ok]])


def dpw_exact(diameter_mm: float, pitch_x: float, pitch_y: float, steps: int = 40) -> tuple[int, float, float]:
    """Best whole-die count over grid offsets; returns (count, ox, oy)."""
    best = (0, 0.0, 0.0)
    for ox in np.linspace(0, pitch_x, steps, endpoint=False):
        for oy in np.linspace(0, pitch_y, steps, endpoint=False):
            n = len(die_sites(diameter_mm, pitch_x, pitch_y, ox, oy))
            if n > best[0]:
                best = (n, float(ox), float(oy))
    return best


def y_poisson(ad0: float) -> float:
    return math.exp(-ad0)


def y_murphy(ad0: float) -> float:
    return ((1 - math.exp(-ad0)) / ad0) ** 2


def y_negbin(ad0: float, alpha: float) -> float:
    return (1 + ad0 / alpha) ** (-alpha)


def simulate_yield(area_cm2: float, d0: float, alpha: float | None, dies: int = 600, wafers: int = 2000,
                   seed: int = 1) -> float:
    """Fraction of defect-free dies. alpha=None: Poisson; otherwise each die's density is gamma(alpha, d0/alpha)."""
    rng = np.random.default_rng(seed)
    if alpha is None:
        dens = np.full((wafers, dies), d0)
    else:
        dens = rng.gamma(alpha, d0 / alpha, size=(wafers, dies))
    counts = rng.poisson(dens * area_cm2)
    return float(np.mean(counts == 0))


def cost_per_good_die(wafer_cost: float, diameter_mm: float, area_mm2: float, d0: float, alpha: float) -> float:
    return wafer_cost / (dpw_formula(diameter_mm, area_mm2) * y_negbin(area_mm2 / 100 * d0, alpha))


def cost_per_good_mm2(wafer_cost: float, diameter_mm: float, area_mm2: float, d0: float, alpha: float) -> float:
    return cost_per_good_die(wafer_cost, diameter_mm, area_mm2, d0, alpha) / area_mm2


def harvest_yield(n: int, y_core: float, y_uncore: float, max_bad: int = 1) -> float:
    return y_uncore * sum(math.comb(n, k) * y_core ** (n - k) * (1 - y_core) ** k for k in range(max_bad + 1))


def learning_month(target_yield: float, area_cm2: float, alpha: float, d_inf: float, d_start: float, tau: float) -> float:
    d_target = optimize.brentq(lambda d: y_negbin(area_cm2 * d, alpha) - target_yield, 1e-6, 10)
    return -tau * math.log((d_target - d_inf) / (d_start - d_inf))
