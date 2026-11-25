"""Linear-drive and co-packaged optics models for chapter 24-09.

Energy per bit from watts per port, dB conversions, linear and retimed link budgets, external-laser sharing,
zero-failure and few-failure confidence bounds on failure rate, and blast-radius unavailability.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats

KP4_BER = 2.4e-4
HOURS_PER_YEAR = 8766.0


def pj_per_bit(watts: float, gbps: float) -> float:
    return watts / (gbps * 1e9) * 1e12


def db_to_power_ratio(db: float) -> float:
    return 10 ** (db / 10)


def db_to_amplitude_ratio(db: float) -> float:
    return 10 ** (db / 20)


def linear_q(qs) -> float:
    return 1 / math.sqrt(sum(1 / q ** 2 for q in qs))


def ber(q: float) -> float:
    return float(stats.norm.sf(q))


def margin_db(q: float, target_ber: float = KP4_BER) -> float:
    return 20 * math.log10(q / stats.norm.isf(target_ber))


def lanes_per_laser(source_dbm: float, path_db: float, excess_db: float, need_dbm: float):
    """Split factor available and the largest power-of-two split that still meets the per-lane need."""
    avail = source_dbm - path_db - excess_db - need_dbm
    n = 10 ** (avail / 10)
    return avail, n, 2 ** int(math.floor(math.log2(n)))


def fit_bound(device_hours: float, failures: int = 0, conf: float = 0.95) -> float:
    """Upper confidence bound on a constant failure rate, in FIT, from the chi-square distribution."""
    return stats.chi2.ppf(conf, 2 * failures + 2) / (2 * device_hours) * 1e9


def port_hours_lost(fit: float, ports_lost: int, mttr_h: float, ports_per_unit: int) -> float:
    """Expected port-hours lost per port per year."""
    return fit * 1e-9 * HOURS_PER_YEAR * ports_lost * mttr_h / ports_per_unit


def zero_failure_fraction(rate_per_h: float, device_hours: float, trials: int = 100_000, seed: int = 1) -> float:
    """Monte Carlo: fraction of tests of the given exposure that see no failures."""
    rng = np.random.default_rng(seed)
    return float(np.mean(rng.poisson(rate_per_h * device_hours, trials) == 0))
