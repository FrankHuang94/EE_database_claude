"""Advanced-packaging and chiplet models for lab 25-07.

Reticle multiples and interposer counts per wafer, shoreline wiring capacity, hybrid-bond density, the
overlay budget and die-level bond yield (analytic and Monte Carlo), the anneal needed to close a copper
recess, known-good-die escapes and package yield, and a monolithic-against-chiplet cost model.
Lengths in mm unless stated; defect density in cm^-2; money in dollars.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special

RETICLE_MM2 = 26 * 33  # full scanner field, 858 mm2


# ---------------------------------------------------------------- interposers
def interposer_area(multiple: float, reticle_mm2: float = RETICLE_MM2) -> float:
    return multiple * reticle_mm2


def sites_on_wafer(w: float, h: float, diameter: float = 300.0, steps: int = 30) -> int:
    """Most whole w x h rectangles on a circular wafer over grid offsets (no edge exclusion, no street)."""
    r = diameter / 2
    best = 0
    for ox in np.linspace(0, w, steps, endpoint=False):
        for oy in np.linspace(0, h, steps, endpoint=False):
            xs = np.arange(-r - w + ox, r + w, w)
            ys = np.arange(-r - h + oy, r + h, h)
            x, y = np.meshgrid(xs, ys)
            far = np.maximum(np.abs(x), np.abs(x + w)) ** 2 + np.maximum(np.abs(y), np.abs(y + h)) ** 2
            best = max(best, int(np.count_nonzero(far <= r**2)))
    return best


def packages_per_month(wafers: float, per_wafer: int, yield_pkg: float) -> float:
    return wafers * per_wafer * yield_pkg


def shoreline_wires(layers: int, line_um: float, space_um: float) -> float:
    """Wires per mm of die edge: routing layers divided by wire pitch."""
    return layers / ((line_um + space_um) * 1e-3)


# ---------------------------------------------------------------- hybrid bonding
def bond_density(pitch_um: float) -> float:
    """Connections per mm2 on a square grid."""
    return (1000 / pitch_um) ** 2


def die_bond_yield(pitch_um: float, sigma_um: float) -> float:
    """Pad width p/2; a die passes if |error| <= p/4 on both axes (Gaussian placement error per axis)."""
    return special.erf(pitch_um / 4 / (sigma_um * math.sqrt(2))) ** 2


def sigma_for_yield(pitch_um: float, target: float) -> float:
    z = math.sqrt(2) * special.erfinv(math.sqrt(target))
    return pitch_um / 4 / z


def simulate_bond_yield(pitch_um: float, sigma_um: float, dies: int = 200_000, seed: int = 1) -> float:
    rng = np.random.default_rng(seed)
    e = rng.normal(0, sigma_um, size=(dies, 2))
    return float(np.mean(np.all(np.abs(e) <= pitch_um / 4, axis=1)))


def anneal_rise(recess_nm: float, pad_um: float, alpha_cu: float = 17.0, alpha_d: float = 0.5) -> float:
    """Temperature rise (K) for free differential expansion of a copper pad to close its recess."""
    return recess_nm * 1e-9 / ((alpha_cu - alpha_d) * 1e-6 * pad_um * 1e-6)


# ---------------------------------------------------------------- known-good die and cost
def escape_fraction(die_yield: float, coverage: float) -> float:
    """Fraction of dies passing test that are bad (Bayes)."""
    bad_pass = (1 - die_yield) * (1 - coverage)
    return bad_pass / (die_yield + bad_pass)


def package_yield(escapes: list[float], attach_yield: float) -> float:
    return float(np.prod([1 - e for e in escapes])) * attach_yield ** len(escapes)


def y_poisson(area_mm2: float, d0: float) -> float:
    return math.exp(-area_mm2 / 100 * d0)


def y_negbin(area_mm2: float, d0: float, alpha: float) -> float:
    return (1 + area_mm2 / 100 * d0 / alpha) ** (-alpha)


def good_package_cost(areas: list[float], d0: float, c_mm2: float, test: float, pkg: float, attach: float,
                      alpha: float | None = None) -> float:
    """[sum over dies of (c*A + test)/Y + package] / attach^n; Poisson yield unless alpha is given."""
    s = 0.0
    for a in areas:
        y = y_poisson(a, d0) if alpha is None else y_negbin(a, d0, alpha)
        s += (c_mm2 * a + test) / y
    return (s + pkg) / attach ** len(areas)


def breakeven_d0(total_mm2: float, n: int, overhead: float, c_mm2: float, test: float, pkg_mono: float,
                 pkg_chiplet: float, attach: float, alpha: float | None = None) -> float:
    def diff(d0):
        mono = good_package_cost([total_mm2], d0, c_mm2, test, pkg_mono, attach, alpha)
        chip = good_package_cost([total_mm2 / n * (1 + overhead)] * n, d0, c_mm2, test, pkg_chiplet, attach, alpha)
        return mono - chip
    return optimize.brentq(diff, 1e-4, 5)
