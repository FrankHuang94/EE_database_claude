"""First-principles checks of performance, efficiency, benchmark and schedule claims
(chapter 28-02).

Units: operations per second (ops/s), joules, watts, bytes, weeks. A multiply-accumulate
(MAC) counts as two operations. All inputs are the caller's assumptions or cited data.
"""
from __future__ import annotations

import math

# --- Throughput --------------------------------------------------------------------


def peak_ops(n_mac, f_hz, sparsity=1.0, precision_factor=1.0):
    """Peak ops/s: 2 x MACs x clock, times a sparsity factor (2 for 2:4 structured
    sparsity) and a precision factor (2 if each unit does two half-width MACs)."""
    return 2 * n_mac * f_hz * sparsity * precision_factor


def tpp(mac_tops, bit_length):
    """US export-control 'total processing performance': 2 x MacTOPS x bit length."""
    return 2 * mac_tops * bit_length


def roofline_ops(peak, bandwidth_bytes_s, intensity_ops_per_byte):
    """Attainable ops/s: min(peak, intensity x bandwidth)."""
    return min(peak, intensity_ops_per_byte * bandwidth_bytes_s)


# --- Energy ------------------------------------------------------------------------


def energy_per_op_j(tops_per_watt):
    """Energy per operation (J) from an efficiency in TOPS/W."""
    return 1.0 / (tops_per_watt * 1e12)


def energy_floor_j(e_arith_per_op, levels):
    """Energy per op = arithmetic + sum over memory levels of (energy per byte /
    ops per byte). levels: [(joules_per_byte, ops_per_byte), ...]."""
    return e_arith_per_op + sum(e_b / ops_b for e_b, ops_b in levels)


def min_intensity(e_per_byte, budget_per_op):
    """Ops per byte needed for a memory level to stay within an energy budget per op."""
    return e_per_byte / budget_per_op


def scale_dynamic_power(p0, v0, f0, v1, f1):
    """Dynamic power scaled as V^2 f from (v0, f0) to (v1, f1)."""
    return p0 * (v1 / v0) ** 2 * (f1 / f0)


def boundary_power(p_core, p_mem, p_io, eta_conv, overhead=1.0, pue=1.0):
    """Power at successive boundaries: chip loads through conversion, then a system
    overhead factor, then the facility's PUE. Returns (card, system, facility)."""
    card = (p_core + p_mem + p_io) / eta_conv
    system = card * overhead
    return card, system, system * pue


# --- Benchmarks --------------------------------------------------------------------


def arith_mean(xs):
    return sum(xs) / len(xs)


def geo_mean(xs):
    return math.exp(sum(math.log(x) for x in xs) / len(xs))


def expected_max_std_normal(n, steps=20000):
    """E[max of n independent standard normals] by numerical integration of
    x * n * phi(x) * Phi(x)^(n-1)."""
    lo, hi = -10.0, 10.0
    h = (hi - lo) / steps
    total = 0.0
    for k in range(steps + 1):
        x = lo + k * h
        phi = math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
        cdf = 0.5 * math.erfc(-x / math.sqrt(2))
        g = x * n * phi * cdf ** (n - 1)
        total += g * (0.5 if k in (0, steps) else 1.0)
    return total * h


def best_of_n(median, sigma_log, n):
    """Expected best speedup reported from n workloads whose log speedups are normal
    with the given median and spread (first-order: exp of the expected maximum)."""
    return median * math.exp(sigma_log * expected_max_std_normal(n))


# --- Schedules ---------------------------------------------------------------------

HOURS_PER_WEEK = 168.0
DAYS_PER_MONTH = 365.25 / 12


def weeks_to_months(weeks):
    return weeks * 7 / DAYS_PER_MONTH


def tapeout_to_production(mask_wk, fab_wk, pkg_test_wk, bringup_wk, respins, respin_mask_wk,
                          respin_fab_wk, qual_hours, qual_report_wk):
    """Weeks from tape-out to production: first silicon and bring-up, then each respin
    (masks, fab, packaging and test), then qualification and its report."""
    first = mask_wk + fab_wk + pkg_test_wk + bringup_wk
    per_respin = respin_mask_wk + respin_fab_wk + pkg_test_wk
    return first + respins * per_respin + qual_hours / HOURS_PER_WEEK + qual_report_wk


# --- The chapter's cases -----------------------------------------------------------

NPU_MACS = 32768
NPU_CLOCK = 1.2e9
NPU_BW = 64e9            # bytes/s, assumed LPDDR-class bandwidth for the lab
HOROWITZ_8B_MULT = 0.2e-12   # J, 45 nm, 0.9 V [R-208]
HOROWITZ_8B_ADD = 0.03e-12   # J
HOROWITZ_DRAM_32B = 640e-12  # J per 32-bit DRAM read [R-458]
HBM2_PER_BIT = 3.9e-12       # J/bit [R-459]
