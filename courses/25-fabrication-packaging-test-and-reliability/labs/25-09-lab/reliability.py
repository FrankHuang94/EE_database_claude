"""Reliability-physics models for lab 25-09.

Arrhenius and Black's-equation acceleration, the local current exponent of a two-phase (nucleation +
growth) electromigration model, the Blech product, three TDDB extrapolation models fitted to the same two
stress points, Weibull area and percentile scaling, BTI power-law extrapolation, the human-body-model ESD
discharge into a clamp, the chi-square FIT bound for a zero-failure HTOL test, and summing mechanisms with
different activation energies. Temperatures in degrees C unless stated.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats

K_EV = 8.617333262e-5


def arrhenius_af(ea_ev: float, t_use_c: float, t_stress_c: float, k: float = K_EV, offset: float = 273.15) -> float:
    """Acceleration factor of the stress condition over the use condition."""
    return math.exp(ea_ev / k * (1 / (t_use_c + offset) - 1 / (t_stress_c + offset)))


def black_af(ea_ev: float, t_use: float, t_stress: float, j_use: float, j_stress: float, n: float) -> float:
    return arrhenius_af(ea_ev, t_use, t_stress) * (j_stress / j_use) ** n


def two_phase_mttf(x: float) -> float:
    """MTTF of B j^-2 + C j^-1 in units where j* = B/C = 1 and C = 1."""
    return 1 / x**2 + 1 / x


def local_exponent(x: float) -> float:
    return (2 + x) / (1 + x)


def blech_max_length(jl_crit_a_per_cm: float, j_a_per_cm2: float) -> float:
    """Longest immune wire (cm)."""
    return jl_crit_a_per_cm / j_a_per_cm2


def tddb_fit(e1: float, t1: float, e2: float, t2: float) -> dict:
    """Fit E, 1/E and power-law models through two (field, time) points; returns extrapolation functions."""
    gamma = math.log(t2 / t1) / (e1 - e2)
    g = math.log(t2 / t1) / (1 / e2 - 1 / e1)
    m = math.log(t2 / t1) / math.log(e1 / e2)
    return {
        "E": lambda e: t1 * math.exp(gamma * (e1 - e)),
        "1/E": lambda e: t1 * math.exp(g * (1 / e - 1 / e1)),
        "power": lambda e: t1 * (e1 / e) ** m,
        "params": (gamma, g, m),
    }


def weibull_scale(area_ratio: float, fraction: float, beta: float) -> float:
    """Time to reach `fraction` failures on a part `area_ratio` times the test area, relative to the test t63."""
    return area_ratio ** (-1 / beta) * (-math.log(1 - fraction)) ** (1 / beta)


def bti_shift(dv_test: float, t_test: float, t_use: float, n: float) -> float:
    return dv_test * (t_use / t_test) ** n


def alpha_delay(vdd: float, vth: float, alpha: float = 1.3) -> float:
    return vdd / (vdd - vth) ** alpha


def hbm(v0: float, vhold: float, ron: float, r: float = 1500.0, c: float = 100e-12) -> dict:
    i0 = (v0 - vhold) / (r + ron)
    tau = (r + ron) * c
    return {"i_peak": i0, "tau": tau, "v_pad": vhold + i0 * ron, "energy": 0.5 * c * v0**2}


def fit_zero_fail(units: int, hours: float, af: float, cl: float = 0.6, failures: int = 0) -> float:
    chi = stats.chi2.ppf(cl, 2 * failures + 2)
    return chi / (2 * units * hours * af) * 1e9


def sum_fit(fits_at_ref: list[float], eas: list[float], t_ref: float, t_new: float) -> float:
    return float(sum(f * arrhenius_af(ea, t_ref, t_new) for f, ea in zip(fits_at_ref, eas)))


def simulate_htol(units: int, hours: float, af: float, fit_true: float, trials: int = 200_000, seed: int = 3) -> float:
    """Fraction of zero-failure HTOL outcomes for a true use-condition FIT (constant rate)."""
    rng = np.random.default_rng(seed)
    lam = fit_true * 1e-9 * af * hours * units
    return float(np.mean(rng.poisson(lam, size=trials) == 0))
