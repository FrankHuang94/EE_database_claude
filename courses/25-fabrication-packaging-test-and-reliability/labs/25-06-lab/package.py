"""Packaging models for lab 25-06.

I/O counts and the perimeter/area crossover, substrate escape routing, power-bump budgets, solder-joint
shear strain over a bump array, and the package's weakest-link fatigue life (Weibull) by formula and by
Monte Carlo. Lengths in mm unless stated (escape routing in micrometres).
"""
from __future__ import annotations

import math

import numpy as np


def io_perimeter(d_mm: float, pitch_mm: float) -> float:
    return 4 * d_mm / pitch_mm


def io_area(d_mm: float, pitch_mm: float) -> float:
    return (d_mm / pitch_mm) ** 2


def crossover(p_area: float, p_wire: float) -> float:
    return 4 * p_area**2 / p_wire


def traces_between(pitch_um: float, pad_um: float, w_um: float, s_um: float) -> int:
    return math.floor((pitch_um - pad_um - s_um) / (w_um + s_um))


def layers_needed(rows: int, pitch_um: float, pad_um: float, w_um: float, s_um: float) -> int:
    return math.ceil(rows / (traces_between(pitch_um, pad_um, w_um, s_um) + 1))


def power_bumps(power_w: float, vdd: float, amps_per_bump: float) -> float:
    return power_w / vdd / amps_per_bump


def bump_grid(die_mm: float, pitch_mm: float) -> np.ndarray:
    """Bump coordinates (x, y) relative to the die centre."""
    n = int(round(die_mm / pitch_mm))
    c = (np.arange(n) - (n - 1) / 2) * pitch_mm
    x, y = np.meshgrid(c, c)
    return np.column_stack([x.ravel(), y.ravel()])


def shear_strain(dalpha_ppm: float, dt: float, dnp_mm: np.ndarray, h_mm: float) -> np.ndarray:
    return dalpha_ppm * 1e-6 * dt * dnp_mm / h_mm


def package_scale(strains: np.ndarray, beta: float, n_exp: float = 2.0) -> float:
    """Weakest-link Weibull scale of the package relative to a joint at the largest strain."""
    rel = (strains / strains.max()) ** n_exp          # eta_max / eta_i = (gamma_i / gamma_max)^n
    return float(np.sum(rel**beta) ** (-1 / beta))


def simulate_package_life(strains: np.ndarray, beta: float, n_exp: float = 2.0, trials: int = 2000,
                          seed: int = 1) -> np.ndarray:
    """First-failure lives in units of the most-strained joint's Weibull scale."""
    rng = np.random.default_rng(seed)
    with np.errstate(divide="ignore"):
        eta = (strains.max() / strains) ** n_exp       # a joint at the exact centre never fails (inf)
    lives = eta[None, :] * rng.weibull(beta, size=(trials, len(strains)))
    return lives.min(axis=1)
