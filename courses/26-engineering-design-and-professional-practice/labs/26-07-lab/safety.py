"""Quantitative tools behind the safety and compliance arguments of Lab 26-07.

- fleet risk: the chance that at least one of N units fails, and expected events (Example 26-07.1);
- FIT budgets: expected dangerous failures across a fleet's operating hours (Example 26-07.2);
- redundancy with common-cause failures: the beta-factor model (Example 26-07.3);
- what zero observed failures proves: the exponential (Poisson) upper confidence bound and the operating
  hours needed to demonstrate a rate (Example 26-07.4);
- export-control arithmetic: total processing performance (TPP) and performance density (Example 26-07.5);
- protection terms: dates a fixed number of years after a start date (Example 26-07.6).
"""
from __future__ import annotations

import datetime as dt
import math

FIT = 1e-9  # failures per device-hour


# ---------------------------------------------------------------- fleets
def p_any(p: float, n: float) -> float:
    """Chance that at least one of n independent units fails, each with probability p."""
    return -math.expm1(n * math.log1p(-p))


def expected_events(p: float, n: float) -> float:
    return p * n


def fleet_failures(fit: float, units: float, hours_per_unit: float) -> float:
    return fit * FIT * units * hours_per_unit


def p_unit_lifetime(fit: float, hours: float) -> float:
    return -math.expm1(-fit * FIT * hours)


# ---------------------------------------------------------------- redundancy
def p_both_fail(p: float, beta: float = 0.0) -> float:
    """Beta-factor model: a fraction beta of each channel's failures are common to both channels."""
    common = beta * p
    independent = (1 - beta) * p
    return common + independent**2 - common * independent**2


# ---------------------------------------------------------------- zero-failure evidence
def rate_upper_bound(hours: float, failures: int = 0, conf: float = 0.95) -> float:
    """Upper confidence bound on a constant failure rate after `failures` events in `hours` (chi-square)."""
    from scipy import stats
    return stats.chi2.ppf(conf, 2 * (failures + 1)) / (2 * hours)


def hours_to_demonstrate(rate: float, conf: float = 0.95) -> float:
    """Failure-free hours needed so that the upper bound with zero failures equals `rate`."""
    return -math.log(1 - conf) / rate


# ---------------------------------------------------------------- export-control arithmetic
def tpp(dense_tops: float, bit_length: int) -> float:
    """Total processing performance: 2 x MacTOPS x bit length, with MacTOPS = TOPS/2 for a MAC counted as
    two operations, so TPP = TOPS x bit length."""
    return dense_tops * bit_length


def performance_density(tpp_value: float, die_area_mm2: float) -> float:
    return tpp_value / die_area_mm2


# ---------------------------------------------------------------- terms
def add_years(start: dt.date, years: int) -> dt.date:
    try:
        return start.replace(year=start.year + years)
    except ValueError:  # 29 February
        return start.replace(year=start.year + years, day=28)
