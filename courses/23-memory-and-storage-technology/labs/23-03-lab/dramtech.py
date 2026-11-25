"""Models for chapter 23-03: DRAM cells, arrays and refresh.

Closed forms for the chapter's examples: charge-sharing signal and bitline length, writing through an access
transistor with and without a boosted wordline, latch regeneration, device organization, access latency, refresh
overhead and energy, retention against temperature, and row-hammer arithmetic including probabilistic mitigation.
The verify script recomputes the published numbers by other routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math

from scipy import stats

Q_E = 1.602176634e-19  # elementary charge (C)
EPS0 = 8.8541878128e-12  # vacuum permittivity (F/m)


# ---------------------------------------------------------------- sensing
def charge_sharing_dv(c_s: float, c_bl: float, v_cell: float, v_pre: float) -> float:
    """Bitline voltage change when a cell at v_cell shares charge with a bitline precharged to v_pre."""
    return (v_cell - v_pre) * c_s / (c_s + c_bl)


def max_bitline_cap(c_s: float, v_signal: float, dv_min: float) -> float:
    """Largest bitline capacitance that still gives dv_min from a cell whose signal (v_cell - v_pre) is v_signal."""
    return c_s * (v_signal / dv_min - 1.0)


def max_cells_per_bitline(c_s: float, v_signal: float, dv_min: float, c_per_cell: float, c_fixed: float) -> float:
    """Cells per bitline at which the signal falls to dv_min (not rounded)."""
    return (max_bitline_cap(c_s, v_signal, dv_min) - c_fixed) / c_per_cell


def area_per_bit(a_cell: float, a_sa_per_bitline: float, cells_per_bitline: int) -> float:
    """Array area per bit: the cell plus its share of the sense amplifier serving its bitline."""
    return a_cell + a_sa_per_bitline / cells_per_bitline


def latch_time(tau: float, v_final: float, dv: float) -> float:
    """Time for a regenerative latch with time constant tau to grow a difference dv to v_final (linear model)."""
    return tau * math.log(v_final / dv)


# ---------------------------------------------------------------- writing through the access transistor
def write_saturated(t: float, k: float, c_s: float, v_wl: float, v_th: float) -> float:
    """Cell voltage at time t when charged from 0 through a saturated access transistor (bitline >= v_wl - v_th).

    dV/dt = (k / 2C) (a - V)^2 with a = v_wl - v_th, so V = a - 1 / (1/a + k t / 2C).
    """
    a = v_wl - v_th
    return a - 1.0 / (1.0 / a + k * t / (2 * c_s))


def write_linear_deficit(t: float, k: float, c_s: float, v_wl: float, v_th: float, v_bl: float) -> float:
    """Shortfall v_bl - V at time t when the access transistor stays linear (v_wl - v_th > v_bl), cell starting at 0.

    With u = v_bl - V and b = v_wl - v_th - v_bl: du/dt = -(k/C)(b u + u^2/2), solved by partial fractions.
    """
    b = v_wl - v_th - v_bl
    u0 = v_bl
    r = u0 / (b + 0.5 * u0) * math.exp(-b * k * t / c_s)
    return r * b / (1.0 - 0.5 * r)


# ---------------------------------------------------------------- organization
def device_bits(banks: int, rows: int, page_bits: int) -> int:
    return banks * rows * page_bits


def page_bits(col_bits: int, dq: int) -> int:
    """Bits in one bank's open row: 2^col_bits columns, each dq bits wide."""
    return (2 ** col_bits) * dq


def cell_area_nm2(f_nm: float, factor: float = 6.0) -> float:
    """Cell area in nm² for a cell of `factor` F² (6F² for today's DRAM)."""
    return factor * f_nm * f_nm


# ---------------------------------------------------------------- latency and bandwidth
def latencies(t_cl: float, t_rcd: float, t_rp: float) -> tuple[float, float, float]:
    """Row hit, closed bank (row miss) and row conflict latencies to the first data."""
    return t_cl, t_rcd + t_cl, t_rp + t_rcd + t_cl


def bank_random_bw(line_bytes: float, t_rc: float) -> float:
    """Bytes per second one bank delivers when every access opens a new row."""
    return line_bytes / t_rc


# ---------------------------------------------------------------- refresh, energy and retention
def refresh_overhead(t_rfc: float, t_refi: float) -> float:
    """Fraction of time a device is busy refreshing."""
    return t_rfc / t_refi


def activation_energy(n_bitlines: int, c_bl: float, v: float) -> float:
    """Supply energy to sense and restore one row: each bitline pair takes C V/2 of charge from the supply at V."""
    return n_bitlines * c_bl * v * v / 2.0


def retention_time(c_s: float, dv_allowed: float, i_leak: float) -> float:
    return c_s * dv_allowed / i_leak


def retention_at(t_ref: float, temp_ref: float, temp: float, doubling_c: float = 10.0) -> float:
    """Retention time at temp if leakage doubles every doubling_c degrees."""
    return t_ref * 2.0 ** (-(temp - temp_ref) / doubling_c)


def weak_cells(n_bits: float, t_window: float, median: float, sigma_ln: float) -> float:
    """Expected cells with retention below t_window for a lognormal retention distribution."""
    return n_bits * float(stats.norm.cdf((math.log(t_window) - math.log(median)) / sigma_ln))


# ---------------------------------------------------------------- row hammer
def activations_in(window: float, t_rc: float) -> float:
    return window / t_rc


def para_miss_probability(p: float, n_th: int) -> float:
    """Probability that PARA never refreshes a given neighbour in n_th closes (each close refreshes it with p/2)."""
    return (1.0 - p / 2.0) ** n_th


def para_p_for(target: float, n_th: int) -> float:
    """PARA probability p that gives a miss probability `target` at threshold n_th."""
    return 2.0 * (1.0 - target ** (1.0 / n_th))


# ---------------------------------------------------------------- capacitor geometry
def plate_area_needed(c: float, eps_r: float, t_ox: float) -> float:
    """Electrode area (m²) a thin-film capacitor of thickness t_ox needs for capacitance c."""
    return c * t_ox / (EPS0 * eps_r)


def pillar_height(c: float, eps_r: float, t_ox: float, diameter: float, sides: int = 1) -> float:
    """Height of a cylindrical electrode of the given diameter whose wall area (one or both sides) gives c."""
    return plate_area_needed(c, eps_r, t_ox) / (sides * math.pi * diameter)
