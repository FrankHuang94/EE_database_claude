"""Lab 20-11: mismatch, gradients and statistical design.

- pelgrom_sigma: sigma of a pair difference, A / sqrt(W L).
- mirror_sigma, pair_offset_sigma: current-mirror and differential-pair mismatch from threshold and beta terms.
- pattern_residuals: the linear and quadratic gradient residuals of a one-dimensional placement pattern (e.g. "ABBA").
- gradient_offset: the systematic mismatch of two devices split into unit cells placed in a pattern, for a
  polynomial gradient of a parameter along the row.
- mc_pair: a seeded Monte Carlo of pair offsets from independent unit-cell threshold errors (area law check).
- zero_failure_runs, sigma_ci: how many Monte Carlo runs a yield claim needs, and the confidence interval of an
  estimated standard deviation.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats


def pelgrom_sigma(a, w, l):
    """Standard deviation of the difference of a parameter between two devices of area W L (A in unit*um)."""
    return a / math.sqrt(w * l)


def mirror_sigma(gm_over_id, s_vt, s_beta):
    """Relative current mismatch of a mirror: sqrt((gm/ID * s_vt)^2 + s_beta^2)."""
    return math.hypot(gm_over_id * s_vt, s_beta)


def pair_offset_sigma(gm_over_id, s_vt, s_beta):
    """Input offset of a differential pair: sqrt(s_vt^2 + (s_beta / (gm/ID))^2)."""
    return math.hypot(s_vt, s_beta / gm_over_id)


def pattern_residuals(pattern):
    """Mean position (order 1) and mean squared position (order 2) of A cells minus those of B cells, positions in
    unit pitches centred on the row."""
    n = len(pattern)
    pos = np.arange(n) - (n - 1) / 2
    a = np.array([p for p, c in zip(pos, pattern) if c == "A"])
    b = np.array([p for p, c in zip(pos, pattern) if c == "B"])
    return float(a.mean() - b.mean()), float((a ** 2).mean() - (b ** 2).mean())


def gradient_offset(pattern, coeffs, pitch):
    """Systematic difference (A minus B) of a parameter p(x) = c1 x + c2 x^2 + ... averaged over each device's cells,
    with x in micrometres from the row centre and unit cells `pitch` apart."""
    n = len(pattern)
    pos = (np.arange(n) - (n - 1) / 2) * pitch
    p = sum(c * pos ** (k + 1) for k, c in enumerate(coeffs))
    a = np.array([v for v, ch in zip(p, pattern) if ch == "A"])
    b = np.array([v for v, ch in zip(p, pattern) if ch == "B"])
    return float(a.mean() - b.mean())


def mc_pair(a_vt, w, l, n_cells, trials, rng):
    """Monte Carlo: each device is n_cells unit cells of area W L / n_cells whose threshold errors are independent with
    single-device sigma a_vt / sqrt(2 * cell area); returns the pair offsets (difference of mean thresholds)."""
    cell_area = w * l / n_cells
    s_cell = a_vt / math.sqrt(2 * cell_area)
    va = rng.normal(0, s_cell, (trials, n_cells)).mean(axis=1)
    vb = rng.normal(0, s_cell, (trials, n_cells)).mean(axis=1)
    return va - vb


def zero_failure_runs(p_fail, confidence=0.95):
    """Smallest n with (1 - p_fail)^n <= 1 - confidence: runs with no failure needed to claim failure rate < p_fail."""
    return math.ceil(math.log(1 - confidence) / math.log(1 - p_fail))


def sigma_ci(n, confidence=0.95):
    """Multipliers (low, high) on an estimated standard deviation from n Gaussian samples (chi-square interval)."""
    a = (1 - confidence) / 2
    return math.sqrt((n - 1) / stats.chi2.ppf(1 - a, n - 1)), math.sqrt((n - 1) / stats.chi2.ppf(a, n - 1))
