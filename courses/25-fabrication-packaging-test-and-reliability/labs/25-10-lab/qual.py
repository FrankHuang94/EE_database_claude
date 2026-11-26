"""Qualification and functional-safety models for lab 25-10.

Coffin-Manson temperature-cycling equivalence, mission-profile HTOL hours (Arrhenius), FMEDA metrics
(SPFM, LFM), a first-order PMHF with the dual-point term, a Monte Carlo of latent faults with periodic
self-test, and vehicle-level defect rates. Rates in FIT unless stated; temperatures in degrees C.
"""
from __future__ import annotations

import math

import numpy as np

K_EV = 8.617333262e-5


def tc_af(dt_stress: float, dt_field: float, n: float) -> float:
    return (dt_stress / dt_field) ** n


def tc_field_years(cycles: float, dt_stress: float, dt_field: float, n: float, per_day: float = 1.0) -> float:
    return cycles * tc_af(dt_stress, dt_field, n) / (per_day * 365.25)


def arrhenius(ea: float, t_use: float, t_stress: float) -> float:
    return math.exp(ea / K_EV * (1 / (t_use + 273.15) - 1 / (t_stress + 273.15)))


def profile_stress_hours(profile: list[tuple[float, float]], life_h: float, ea: float, t_stress: float) -> float:
    return sum(w * life_h / arrhenius(ea, t, t_stress) for t, w in profile)


def fmeda(lam: float, safe: float, dc: float, lam_sm: float, sm_test_cov: float) -> dict:
    """One element plus its safety mechanism: returns rates (FIT) and metrics."""
    lam_d = lam - safe
    lam_rf = (1 - dc) * lam_d
    total = lam + lam_sm
    lam_lat = (1 - sm_test_cov) * lam_sm
    return {"lam_d": lam_d, "lam_rf": lam_rf, "total": total, "lam_lat": lam_lat,
            "spfm": 1 - lam_rf / total, "lfm": 1 - lam_lat / (total - lam_rf)}


def dual_point_fit(lam_l_fit: float, lam_d_fit: float, tau_h: float) -> float:
    return lam_l_fit * 1e-9 * lam_d_fit * 1e-9 * tau_h * 1e9


def simulate_dual(lam_l: float, lam_d: float, t_test: float, life: float, vehicles: int = 1_000_000,
                  seed: int = 5) -> float:
    """Average dual-point violation rate (per hour): a latent fault at t_L is found at the next periodic
    test; a dangerous fault in the window between causes a violation."""
    rng = np.random.default_rng(seed)
    t_l = rng.exponential(1 / lam_l, size=vehicles)
    has = t_l < life
    found = np.ceil(t_l / t_test) * t_test
    window = np.clip(np.minimum(found, life) - t_l, 0, None)
    p_violate = np.where(has, 1 - np.exp(-lam_d * window), 0.0)
    return float(p_violate.mean() / life)


def vehicle_defect_fraction(components: int, p: float) -> float:
    return 1 - (1 - p) ** components


def zero_fail_sample(fraction: float, confidence: float) -> float:
    return math.log(1 - confidence) / math.log(1 - fraction)
