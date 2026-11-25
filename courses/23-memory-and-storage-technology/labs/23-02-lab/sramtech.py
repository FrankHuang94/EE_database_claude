"""Models for chapter 23-02: SRAM technology.

Closed forms and small solvers for the chapter's examples: bitcell and macro density, the die-area effect of a
stalled SRAM shrink, array sigma and Vmin, square-law read and write assists, bitline length, and leakage.
The verify script recomputes the published numbers by other routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math

from scipy import optimize, stats


# ---------------------------------------------------------------- density
def raw_density_mb_per_mm2(cell_um2: float) -> float:
    """Bits per mm² if the whole area were bitcells, in units of 10^6 bits per mm²."""
    return 1.0 / cell_um2  # 1 / µm² = 10^6 / mm²


def array_efficiency(macro_mb_per_mm2: float, cell_um2: float) -> float:
    """Fraction of a macro's area that is bitcells."""
    return macro_mb_per_mm2 / raw_density_mb_per_mm2(cell_um2)


def area_per_bit(cell_um2: float, col_overhead_um2: float, cells_per_bitline: int, other_um2: float) -> float:
    """Macro area per bit (µm²): the cell, the column periphery shared by a bitline, and other overhead."""
    return cell_um2 + col_overhead_um2 / cells_per_bitline + other_um2


def bitline_time(cells: int, c_per_cell: float, c_fixed: float, dv: float, i_cell: float) -> float:
    """Time for the cell current to develop dv on a bitline of `cells` cells (s)."""
    return (cells * c_per_cell + c_fixed) * dv / i_cell


def shrunk_die_fraction(sram_fraction: float, logic_shrink: float, sram_shrink: float = 1.0) -> float:
    """New die area as a fraction of the old when logic and SRAM shrink by different factors."""
    return sram_fraction / sram_shrink + (1 - sram_fraction) / logic_shrink


# ---------------------------------------------------------------- variation and Vmin
def sigma_needed(n_bits: float, yield_target: float = 0.99) -> float:
    """Margin in standard deviations for an array of n_bits to work with probability yield_target (no repair)."""
    return float(stats.norm.isf(-math.log(yield_target) / n_bits))


def pelgrom_sigma_mv(a_vt_mv_um: float, w_um: float, l_um: float) -> float:
    """Threshold-voltage standard deviation (mV) from Pelgrom's law."""
    return a_vt_mv_um / math.sqrt(w_um * l_um)


def vmin(k: float, sigma_vt_mv: float, slope: float = 0.2, v0: float = 0.25, sens: float = 0.6) -> float:
    """Lowest supply at which a linear margin slope·(V - v0) still exceeds k standard deviations.

    The margin's standard deviation is sens × σ_VT.
    """
    return v0 + k * sens * sigma_vt_mv * 1e-3 / slope


# ---------------------------------------------------------------- square-law cell
def ids(k: float, vgs: float, vds: float, vt: float) -> float:
    """Level-1 drain current magnitude (A) for an n-type device (use magnitudes for p-type)."""
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    if vds >= vov:
        return 0.5 * k * vov * vov
    return k * (vov * vds - 0.5 * vds * vds)


def switching_threshold(vdd: float, kn: float, kp: float, vtn: float, vtp: float) -> float:
    """Inverter switching threshold with both devices saturated."""
    r = math.sqrt(kn / kp)
    return (vdd - vtp + r * vtn) / (1 + r)


def write_node(vdd: float, k_pg: float, k_pu: float, vt_pg: float, vt_pu: float, v_bl: float = 0.0) -> float:
    """Voltage of the node being written to 0: pass gate (gate at vdd, source at the bitline) against the pull-up."""
    def f(v):
        return ids(k_pg, vdd - v_bl, v - v_bl, vt_pg) - ids(k_pu, vdd, vdd - v, vt_pu)
    return optimize.brentq(f, v_bl, vdd)


def read_node(vdd: float, k_pg: float, k_pd: float, vt_pg: float, vt_pd: float, v_wl: float) -> float:
    """Voltage of the 0 node during a read: pass gate from a vdd bitline against the pull-down."""
    def f(v):
        return ids(k_pg, v_wl - v, vdd - v, vt_pg) - ids(k_pd, vdd, v, vt_pd)
    return optimize.brentq(f, 0.0, v_wl - vt_pg)


def read_current(vdd: float, k_pg: float, k_pd: float, vt_pg: float, vt_pd: float, v_wl: float) -> float:
    v = read_node(vdd, k_pg, k_pd, vt_pg, vt_pd, v_wl)
    return ids(k_pg, v_wl - v, vdd - v, vt_pg)


def nbl_needed(vdd: float, k_pg: float, k_pu: float, vt_pg: float, vt_pu: float, v_trip: float) -> float:
    """Negative bitline voltage that pulls the written node down to the opposite inverter's trip point."""
    return optimize.brentq(lambda vb: write_node(vdd, k_pg, k_pu, vt_pg, vt_pu, vb) - v_trip, -vdd, 0.0)


# ---------------------------------------------------------------- leakage
def array_leakage(bits: float, i_bit: float, v: float) -> tuple[float, float]:
    """Leakage current (A) and power (W) of an array."""
    return bits * i_bit, bits * i_bit * v


def retention_leakage_factor(dv: float, halving_mv: float = 100.0) -> float:
    """Leakage multiplier when the supply drops by dv volts, if leakage halves every halving_mv."""
    return 2.0 ** (-dv * 1e3 / halving_mv)
