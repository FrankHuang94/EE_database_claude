"""Post-silicon validation models for lab 25-12.

Trace-buffer sizing, an alpha-power shmoo (synthetic pass/fail grid with measurement noise, and a fit of its
boundary), Vmin solving, Goel-Okumoto bug-discovery fitting by least squares, fix decision trees, Wilson
score intervals and characterization sample sizes.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats


def trace(signals: int, depth: int, f_hz: float) -> tuple[int, float]:
    return signals * depth, depth / f_hz


def fmax(v: float, k: float, vth: float = 0.30, alpha: float = 1.3) -> float:
    return k * (v - vth) ** alpha / v


def fit_k(f_ghz: float, v: float, vth: float = 0.30, alpha: float = 1.3) -> float:
    return f_ghz * v / (v - vth) ** alpha


def vmin(f_target: float, k: float, vth: float = 0.30, alpha: float = 1.3) -> float:
    return optimize.brentq(lambda v: fmax(v, k, vth, alpha) - f_target, vth + 1e-3, 2.0)


def shmoo(k: float, volts: np.ndarray, freqs: np.ndarray, noise_ghz: float = 0.03, seed: int = 1) -> np.ndarray:
    """Pass (True) / fail grid: a point passes if f <= Fmax(V) + measurement noise."""
    rng = np.random.default_rng(seed)
    f_lim = np.array([fmax(v, k) for v in volts])[None, :] + rng.normal(0, noise_ghz, (len(freqs), len(volts)))
    return freqs[:, None] <= f_lim


def fit_shmoo_k(grid: np.ndarray, volts: np.ndarray, freqs: np.ndarray) -> float:
    """Least-squares fit of K to the highest passing frequency in each voltage column."""
    top = np.array([freqs[grid[:, j]].max() if grid[:, j].any() else np.nan for j in range(len(volts))])
    ok = ~np.isnan(top)
    shape = np.array([(v - 0.30) ** 1.3 / v for v in volts])[ok]
    return float(np.sum(shape * top[ok]) / np.sum(shape * shape))


def go_fit(weeks: np.ndarray, bugs: np.ndarray) -> tuple[float, float]:
    popt, _ = optimize.curve_fit(lambda t, a, b: a * (1 - np.exp(-b * t)), weeks, bugs, p0=[bugs.max() * 1.5, 0.1])
    return float(popt[0]), float(popt[1])


def go_two_points(t1: float, m1: float, t2: float, m2: float) -> tuple[float, float]:
    """Exact fit when t2 = 2 t1."""
    x = m2 / m1 - 1
    b = -math.log(x) / t1
    return m1 / (1 - x), b


def decision(delay_per_week: float, metal=(2.0, 10.0, 0.8), full=(25.0, 20.0)) -> tuple[float, float, float]:
    cm, wm, p = metal
    cf, wf = full
    full_cost = cf + wf * delay_per_week
    metal_cost = cm + wm * delay_per_week + (1 - p) * full_cost
    breakeven = 1 - (full_cost - (cm + wm * delay_per_week)) / full_cost
    return metal_cost, full_cost, breakeven


def wilson(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    z = stats.norm.ppf(0.5 + conf / 2)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def sigma_sample(rel_err: float, conf: float = 0.95) -> float:
    z = stats.norm.ppf(0.5 + conf / 2)
    return 1 + z * z / (2 * rel_err**2)
