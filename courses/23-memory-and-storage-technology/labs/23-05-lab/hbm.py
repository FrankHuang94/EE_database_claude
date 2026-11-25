"""Models for chapter 23-05: HBM in depth.

Closed forms for the chapter's examples: stack bandwidth and capacity, interface energy of short unterminated links,
the TSV's resistance, capacitance and area cost, the stack-height budget, a one-dimensional thermal model of a
stack, stack yield and wafer consumption, and interposer packages per wafer. The verify script recomputes the
published numbers by other routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math

EPS0 = 8.8541878128e-12  # F/m


# ---------------------------------------------------------------- bandwidth and capacity
def stack_bandwidth(io_bits: int, pin_rate: float) -> float:
    """Bytes per second of one stack."""
    return io_bits * pin_rate / 8


def pin_rate_for(bandwidth: float, io_bits: int) -> float:
    return bandwidth * 8 / io_bits


def stack_capacity_gb(layers: int, die_gbit: float) -> float:
    """Stack capacity in gigabytes (die density in gigabits, 8 bits per byte)."""
    return layers * die_gbit / 8


# ---------------------------------------------------------------- interface energy
def cv2_energy_per_bit(c: float, v: float, p01: float = 0.25) -> float:
    """Supply energy per bit of an unterminated line: C V^2 per 0-to-1 transition, p01 of them per bit."""
    return p01 * c * v * v


# ---------------------------------------------------------------- TSV
def tsv_capacitance(length: float, r_cu: float, liner: float, eps_r: float = 3.9) -> float:
    """Oxide capacitance of a TSV, a coaxial capacitor of inner radius r_cu and liner thickness `liner`."""
    return 2 * math.pi * eps_r * EPS0 * length / math.log((r_cu + liner) / r_cu)


def tsv_resistance(length: float, r_cu: float, rho: float = 1.72e-8) -> float:
    return rho * length / (math.pi * r_cu * r_cu)


def tsv_area_fraction(n: int, pitch_keepout: float, die_area: float) -> float:
    """Fraction of a die taken by n TSVs, each blocking a square of side pitch_keepout."""
    return n * pitch_keepout ** 2 / die_area


# ---------------------------------------------------------------- stack height
def layer_pitch(total_height: float, overhead: float, layers: int) -> float:
    """Height available per core layer (die plus bond gap) once fixed overhead is removed."""
    return (total_height - overhead) / layers


# ---------------------------------------------------------------- thermal
def layer_resistance(area: float, t_si: float, k_si: float, t_gap: float, k_gap: float) -> float:
    """Thermal resistance (K/W) of one die plus its bond gap, heat flowing through the full area."""
    return t_si / (k_si * area) + t_gap / (k_gap * area)


def base_rise(n_layers: int, r_layer: float, p_base: float, p_core: float) -> float:
    """Temperature rise of the base die above the stack's top when heat leaves through the top.

    The j-th layer from the bottom carries the base die's power plus that of the j - 1 core dies below it:
    sum_j r (p_base + (j - 1) p_core) = r [n p_base + p_core n (n - 1) / 2].
    """
    return r_layer * (n_layers * p_base + p_core * n_layers * (n_layers - 1) / 2)


# ---------------------------------------------------------------- yield and wafers
def stack_yield(layers: int, y_bond: float, y_die: float = 1.0) -> float:
    return (y_bond * y_die) ** layers


def wafer_per_bit_ratio(wafer_share: float, bit_share: float) -> float:
    """Wafers per bit of HBM relative to conventional DRAM, from HBM's shares of wafers and bits."""
    return (wafer_share / bit_share) / ((1 - wafer_share) / (1 - bit_share))


def gross_dies_per_wafer(diameter: float, area: float) -> float:
    """Classic estimate of whole dies (or interposers) per round wafer: pi d^2/(4A) - pi d / sqrt(2A)."""
    return math.pi * diameter ** 2 / (4 * area) - math.pi * diameter / math.sqrt(2 * area)
