"""Maturity models for chip programmes (chapter 28-03): stage chains, qualification
failure-rate bounds and a software defect-discovery model.

Units: months for stage durations, hours for life tests, failures per 1e9 device-hours
(FIT) for failure rates, weeks for software testing time.
"""
from __future__ import annotations

import math

from scipy import stats

K_BOLTZMANN_EV = 8.617333262e-5  # eV/K

# --- Stage chains ------------------------------------------------------------------


def remaining(stages):
    """stages: [(probability, months), ...] from the current level to production.
    Returns (probability of reaching production, months if every stage succeeds)."""
    p, t = 1.0, 0.0
    for q, m in stages:
        p *= q
        t += m
    return p, t


def value_multiplier(stages, annual_rate):
    """Risk-adjusted, time-discounted fraction of a production-ready programme's value."""
    p, t = remaining(stages)
    return p / (1 + annual_rate) ** (t / 12)


# --- Qualification -----------------------------------------------------------------


def arrhenius_af(ea_ev, t_use_c, t_stress_c):
    """Arrhenius acceleration factor between a use and a stress junction temperature."""
    tu, ts = t_use_c + 273.15, t_stress_c + 273.15
    return math.exp(ea_ev / K_BOLTZMANN_EV * (1 / tu - 1 / ts))


def fit_upper(n_devices, hours, failures, af, confidence):
    """Upper confidence bound on the use-condition failure rate in FIT:
    chi2(confidence; 2r + 2) / (2 n t AF) x 1e9."""
    chi2 = stats.chi2.ppf(confidence, 2 * failures + 2)
    return chi2 / (2 * n_devices * hours * af) * 1e9


def devices_needed(fit_target, hours, failures, af, confidence):
    """Smallest sample size whose life test, with the given failures, bounds the failure
    rate at or below the target."""
    chi2 = stats.chi2.ppf(confidence, 2 * failures + 2)
    return math.ceil(chi2 * 1e9 / (2 * fit_target * hours * af))


# --- Software defect discovery (Goel-Okumoto) --------------------------------------


def go_fit_two_points(t1, m1, t2, m2):
    """Fit m(t) = a(1 - exp(-b t)) through two cumulative counts with t2 = 2 t1.
    Returns (a, b)."""
    if abs(t2 - 2 * t1) > 1e-12:
        raise ValueError("the closed form needs t2 = 2 t1")
    x = m2 / m1 - 1          # = exp(-b t1)
    b = -math.log(x) / t1
    a = m1 / (1 - x)
    return a, b


def go_cumulative(a, b, t):
    return a * (1 - math.exp(-b * t))


def go_rate(a, b, t):
    """Discovery rate (defects per unit time) at time t."""
    return a * b * math.exp(-b * t)


def go_remaining(a, b, t):
    """Expected defects not yet found at time t."""
    return a * math.exp(-b * t)


def go_time_to_rate(a, b, rate):
    """Time at which the discovery rate falls to the given level."""
    return math.log(a * b / rate) / b
