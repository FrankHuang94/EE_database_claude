"""Business <-> engineering conversions (chapter 28-09): die cost and its elasticity,
area budgets, delay and respin cost, lifetime energy cost, field failures and a margin
tornado.

Areas in mm^2, defect density per mm^2, money in $ unless noted, power in W, time in hours.
"""
from __future__ import annotations

import math

from scipy import optimize

HOURS_PER_YEAR = 8766.0


def dies_per_wafer(area_mm2, diameter_mm=300.0, whole=True):
    """Dies per wafer, pi d^2/(4A) - pi d/sqrt(2A), rounded down if whole."""
    n = math.pi * diameter_mm ** 2 / (4 * area_mm2) - math.pi * diameter_mm / math.sqrt(2 * area_mm2)
    return math.floor(n) if whole else n


def poisson_yield(area_mm2, d0_per_mm2):
    return math.exp(-area_mm2 * d0_per_mm2)


def die_cost(area_mm2, wafer_price, d0_per_mm2=0.001, whole=True):
    """Cost per good die."""
    return wafer_price / (dies_per_wafer(area_mm2, whole=whole) * poisson_yield(area_mm2, d0_per_mm2))


def elasticity(area_mm2, wafer_price=18500.0, d0_per_mm2=0.001, h=1e-4):
    """d ln(cost) / d ln(area) with unrounded dies per wafer (includes the edge term)."""
    up = die_cost(area_mm2 * (1 + h), wafer_price, d0_per_mm2, whole=False)
    dn = die_cost(area_mm2 * (1 - h), wafer_price, d0_per_mm2, whole=False)
    return (math.log(up) - math.log(dn)) / (math.log(1 + h) - math.log(1 - h))


def gross_margin(asp, die, pkg_test):
    return 1 - (die + pkg_test) / asp


def area_budget(asp, pkg_test, gm_target, wafer_price, d0_per_mm2=0.001):
    """Largest die area whose cost meets the margin target (unrounded dies per wafer)."""
    budget = asp * (1 - gm_target) - pkg_test
    return optimize.brentq(lambda a: die_cost(a, wafer_price, d0_per_mm2, whole=False) - budget, 1, 800)


def delay_cost(revenue_per_year, months, gross_margin_fraction=1.0):
    return revenue_per_year * months / 12 * gross_margin_fraction


def energy_cost(power_w, pue, years, price_per_kwh):
    return power_w / 1000 * pue * years * HOURS_PER_YEAR * price_per_kwh


def field_failures(fit, units, hours):
    return fit * 1e-9 * units * hours


def tornado(base, step=0.10):
    """base: dict(asp, area, wafer, d0, pkg). Returns {knob: margin change in points} for
    a rise of `step` in each knob."""
    def gm(p):
        return gross_margin(p["asp"], die_cost(p["area"], p["wafer"], p["d0"]), p["pkg"])
    b = gm(base)
    out = {}
    for k in base:
        p = dict(base)
        p[k] = base[k] * (1 + step)
        out[k] = 100 * (gm(p) - b)
    return b, out
