"""Sourcing and partitioning economics for Lab 26-04.

- licensing against building an IP block: the discounted unit stream, per-unit and percentage royalties,
  expected slip cost and the discounted break-even volume (Examples 26-04.1 and 26-04.2);
- node selection: the mix-weighted (harmonic) density gain, cost per good die and the NRE break-even
  (Example 26-04.3);
- monolithic dies against reusable chiplets for a product family (Example 26-04.4);
- custom accelerators against merchant parts by total cost of ownership per unit of throughput
  (Example 26-04.5);
- a two-generation decision tree with the option to build later (Example 26-04.6).

Money in dollars unless a function says otherwise; areas in mm2; defect density in cm^-2. The time-value
helpers come from Lab 26-03's `econ.py`.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "26-03-lab"))
import econ  # noqa: E402

HOURS_PER_YEAR = 8760


# ---------------------------------------------------------------- licensing and building
def discounted_units(units: Sequence[float], rate: float, first_year: int = 1) -> float:
    """U = sum of V_t / (1 + i)^t, with the first year's units booked at the end of `first_year`."""
    return sum(u * (1 + rate) ** -(first_year + k) for k, u in enumerate(units))


def eroding_prices(asp0: float, erosion: float, years: int) -> list[float]:
    return [asp0 * (1 - erosion) ** k for k in range(years)]


def royalty_per_unit(asps: Sequence[float], percent: float) -> list[float]:
    return [percent * p for p in asps]


def license_pv(upfront: float, royalty: float, units: Sequence[float], rate: float) -> float:
    """Upfront fee at year 0 plus a fixed per-unit royalty on each year's units."""
    return upfront + royalty * discounted_units(units, rate)


def percent_license_pv(upfront: float, percent: float, asps: Sequence[float], units: Sequence[float],
                       rate: float) -> float:
    return upfront + sum(percent * p * u * (1 + rate) ** -(k + 1) for k, (p, u) in enumerate(zip(asps, units)))


def build_pv(nre: float, p_slip: float = 0.0, slip_cost: float = 0.0) -> float:
    """NRE at year 0 plus the expected cost of a slip."""
    return nre + p_slip * slip_cost


def breakeven_discounted_units(build_cost: float, upfront: float, royalty: float) -> float:
    return (build_cost - upfront) / royalty


# ---------------------------------------------------------------- node selection
def effective_density_gain(fractions: Sequence[float], gains: Sequence[float]) -> float:
    """Area fractions at the old node and per-block density gains; the new area is sum(f/s)."""
    return 1 / sum(f / s for f, s in zip(fractions, gains))


def good_die_cost(wafer: float, area_mm2: float, d0: float, diameter: float = 300.0, test: float = 0.0):
    """(dies per wafer, Poisson yield, cost per good die); a per-die test cost is paid on every die tested."""
    n = econ.dies_per_wafer(diameter, area_mm2)
    y = math.exp(-area_mm2 / 100 * d0)
    return n, y, (wafer / n + test) / y


def node_breakeven(delta_nre: float, cost_old: float, cost_new: float, value_gain: float = 0.0) -> float:
    """Lifetime units at which the new node's unit saving (plus any extra value per unit) repays its extra NRE."""
    return delta_nre / (cost_old - cost_new + value_gain)


# ---------------------------------------------------------------- chiplets and reuse
def package_cost(die_costs: Sequence[float], package: float, attach: float) -> float:
    """[sum of good-die costs + package] / attach^n: each die attach must succeed."""
    return (sum(die_costs) + package) / attach ** len(die_costs)


def family_total(nre: float, unit_costs: Sequence[float], volumes: Sequence[float]) -> float:
    return nre + sum(c * v for c, v in zip(unit_costs, volumes))


# ---------------------------------------------------------------- custom against merchant
def slot_tco(price: float, kw: float, years: float, pue: float, usd_per_kwh: float, overhead: float) -> float:
    """Accelerator price + per-slot infrastructure + facility energy over the service life (undiscounted)."""
    return price + overhead + kw * pue * HOURS_PER_YEAR * years * usd_per_kwh


def tco_per_throughput(price, kw, throughput, years, pue, usd_per_kwh, overhead) -> float:
    return slot_tco(price, kw, years, pue, usd_per_kwh, overhead) / throughput


def merchant_price_ceiling(custom_per_eq: float, nre: float, merchant_eq: float, kw: float, years: float,
                           pue: float, usd_per_kwh: float, overhead: float, throughput: float = 1.0) -> float:
    """Merchant price at which a custom program of `merchant_eq` merchant-equivalents exactly breaks even."""
    energy = kw * pue * HOURS_PER_YEAR * years * usd_per_kwh
    return throughput * (custom_per_eq + nre / merchant_eq) - overhead - energy


# ---------------------------------------------------------------- the option to build later
def two_generation_costs(gen1_license: float, gen1_build: float, port: float, gen2_upfront: float,
                         royalty: float, u2: Sequence[float], probs: Sequence[float], gen2_build: float) -> dict:
    """Expected present cost of three strategies: build now (and port), license now and choose later, or
    license both generations."""
    exp_u2 = sum(p * u for p, u in zip(probs, u2))
    choose = sum(p * min(gen2_upfront + royalty * u, gen2_build) for p, u in zip(probs, u2))
    return {"build_now": gen1_build + port,
            "license_then_choose": gen1_license + choose,
            "license_both": gen1_license + gen2_upfront + royalty * exp_u2}
