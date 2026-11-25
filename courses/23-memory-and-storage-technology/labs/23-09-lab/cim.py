"""Models for chapter 23-09: compute-in-memory and near-memory computing.

Closed forms for the chapter's examples: the analog crossbar's matrix-vector product with differential conductance
pairs, the compute SNR and effective bits of an array with conductance variation, ADC resolution and its energy per
multiply-accumulate, bank-level processing-in-memory throughput and bandwidth, the decode-rate roofline and Amdahl's
law, and TOPS/W at different measurement boundaries. The verify script recomputes the published numbers by other
routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------- analog crossbar
def conductance_pairs(weights, g_unit: float, g_min: float = 0.0):
    """Map signed integer weights to (G+, G-) arrays; both carry g_min, which cancels in the difference."""
    w = np.asarray(weights, dtype=float)
    return g_unit * np.clip(w, 0, None) + g_min, g_unit * np.clip(-w, 0, None) + g_min


def column_currents(v_rows, g):
    """Kirchhoff current summing with ideal virtual-ground columns: I_j = sum_i V_i G_ij."""
    return np.asarray(v_rows, dtype=float) @ np.asarray(g, dtype=float)


def snr_from_sigma(sigma_rel: float) -> float:
    """Compute SNR (power ratio) of a dot product of zero-mean terms with independent relative errors sigma."""
    return 1 / sigma_rel ** 2


def enob(snr_db: float) -> float:
    return (snr_db - 1.76) / 6.02


# ---------------------------------------------------------------- ADC cost
def adc_bits_exact(rows: int, x_bits: int = 1, w_bits: int = 1) -> float:
    """Bits needed to represent every possible column sum exactly."""
    max_sum = rows * (2 ** x_bits - 1) * (2 ** w_bits - 1)
    return math.log2(max_sum + 1)


def adc_energy_walden(fom: float, bits: float) -> float:
    return fom * 2 ** bits


def adc_energy_per_mac(fom: float, bits: float, rows: int, x_bits: int, w_bits: int) -> float:
    """ADC energy per multi-bit MAC with bit-serial inputs and bit-sliced weights (one conversion per bit pair)."""
    return adc_energy_walden(fom, bits) * x_bits * w_bits / rows


def tops_per_watt(energy_per_mac: float) -> float:
    """TOPS/W counting a multiply-accumulate as two operations."""
    return 2 / energy_per_mac / 1e12


# ---------------------------------------------------------------- PIM
def simd_throughput(units: int, lanes: int, f: float, ops_per_lane: int = 2) -> float:
    return units * lanes * ops_per_lane * f


def bus_bandwidth(rate: float, width_bits: int) -> float:
    return rate * width_bits / 8


def amdahl(fraction: float, speedup: float) -> float:
    return 1 / ((1 - fraction) + fraction / speedup)


def fraction_for(overall: float, speedup: float) -> float:
    """Fraction of time that must be accelerated by `speedup` to reach `overall` (inverse Amdahl)."""
    return (1 - 1 / overall) / (1 - 1 / speedup)
