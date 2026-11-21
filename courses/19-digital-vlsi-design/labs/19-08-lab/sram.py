"""6T SRAM models for Lab 19-08.

Read disturb (access transistor against pull-down), write margin (access against pull-up), butterfly curves and the
static noise margin, bitline development and sense-amplifier regeneration, array area, and the yield arithmetic of
rare cell failures. Square-law transistors with lambda = 0. Units: SI.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm


def i_sq(k: float, vov: float, vds: float) -> float:
    if vov <= 0 or vds <= 0:
        return 0.0
    return k * (vov * vds - vds * vds / 2) if vds < vov else 0.5 * k * vov * vov


# ---------------------------------------------------------------- read and write
def read_disturb(k_access: float, k_pulldown: float, vdd: float, vt: float) -> float:
    """Voltage of the '0' node during a read with the bitline held at VDD: the saturated access transistor
    (gate VDD, source = node) against the linear pull-down (gate VDD)."""
    return brentq(lambda v: i_sq(k_access, vdd - v - vt, vdd - v) - i_sq(k_pulldown, vdd - vt, v), 0.0, vdd / 2,
                  xtol=1e-15)


def write_level(k_access: float, k_pullup: float, vdd: float, vt: float) -> float:
    """Voltage of the '1' node when the access transistor pulls it toward a 0 V bitline against the pull-up PMOS
    (gate at the other node, still 0 V)."""
    return brentq(lambda v: i_sq(k_access, vdd - vt, v) - i_sq(k_pullup, vdd - vt, vdd - v), 0.0, vdd, xtol=1e-15)


# ---------------------------------------------------------------- butterfly and SNM
def inverter_vtc(vin: np.ndarray, vdd: float, vt: float, kn: float, kp: float, k_access: float = 0.0) -> np.ndarray:
    """Output of a cell inverter; with k_access > 0 the access transistor connects the output to a bitline at VDD
    (read condition)."""
    out = np.empty_like(vin)
    for i, x in enumerate(vin):
        def f(v):
            return (i_sq(kp, vdd - x - vt, vdd - v) + i_sq(k_access, vdd - v - vt, vdd - v)
                    - i_sq(kn, x - vt, v))
        out[i] = brentq(f, 0.0, vdd, xtol=1e-13)
    return out


def static_noise_margin(vdd: float, vt: float, kn: float, kp: float, k_access: float = 0.0, n: int = 4001) -> float:
    """Side of the largest square that fits in a lobe of the butterfly plot (Seevinck's method: rotate by 45 degrees
    and take the largest vertical separation of the two curves, divided by sqrt 2), the smaller of the two lobes."""
    x = np.linspace(0, vdd, n)
    y = inverter_vtc(x, vdd, vt, kn, kp, k_access)
    # curve 1: (x, y); curve 2, its mirror: (y, x). In rotated coordinates u = (x - y)/sqrt2 (monotonic along both
    # curves) and v = (x + y)/sqrt2, the separation in v at fixed u is the diagonal of an inscribed square.
    u1, v1 = (x - y) / math.sqrt(2), (x + y) / math.sqrt(2)
    u2, v2 = (y - x) / math.sqrt(2), (y + x) / math.sqrt(2)
    o1, o2 = np.argsort(u1), np.argsort(u2)
    uu = np.linspace(max(u1.min(), u2.min()), min(u1.max(), u2.max()), 8001)
    d = np.interp(uu, u1[o1], v1[o1]) - np.interp(uu, u2[o2], v2[o2])
    return min(d.max(), -d.min()) / math.sqrt(2)


# ---------------------------------------------------------------- bitlines and sense amplifiers
def bitline_time(c_bl: float, dv: float, i_cell: float) -> float:
    return c_bl * dv / i_cell


def sense_time(tau: float, dv: float, v_full: float) -> float:
    """Regenerative latch: time to grow dv to v_full, tau ln(v_full/dv)."""
    return tau * math.log(v_full / dv)


# ---------------------------------------------------------------- area and yield
def array_area_mm2(bits: float, cell_um2: float, efficiency: float = 1.0) -> float:
    return bits * cell_um2 / efficiency * 1e-6


def cell_fail_probability(margin_sigmas: float) -> float:
    return float(norm.sf(margin_sigmas))


def array_yield(bits: float, p_fail: float, spares: int = 0) -> float:
    """Probability of at most `spares` failing cells (Poisson)."""
    lam = bits * p_fail
    return float(sum(math.exp(-lam) * lam ** j / math.factorial(j) for j in range(spares + 1)))
