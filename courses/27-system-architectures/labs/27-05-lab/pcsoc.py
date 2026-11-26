"""Models for Chapter 27-05 (The PC SoC).

Each function is a first-order engineering model from the chapter. Units are in
every docstring. Parameter values used in the chapter are illustrative
assumptions unless a source is cited there.
"""
import math


# --- Power states and battery life ---------------------------------------------

def residency_power_w(states):
    """Average power (W) from [(residency fraction, power W), ...]; fractions sum to 1."""
    return sum(f * p for f, p in states)


def battery_hours(wh, p_w):
    """Hours a battery of wh watt-hours lasts at an average power p_w."""
    return wh / p_w


# --- Turbo under an averaged power limit -----------------------------------------

def turbo_seconds(pl1_w, pl2_w, tau_s, p_start_w):
    """Time (s) a package can run at pl2 before the exponentially weighted moving
    average of its power (time constant tau), starting from p_start, reaches pl1:
    t = tau * ln((PL2 - P0) / (PL2 - PL1))."""
    if p_start_w >= pl1_w:
        return 0.0
    return tau_s * math.log((pl2_w - p_start_w) / (pl2_w - pl1_w))


def ewma_trace(powers_w, dt_s, tau_s, y0_w):
    """Exponentially weighted moving average of a power trace (W), step dt."""
    a = 1.0 - math.exp(-dt_s / tau_s)
    y, out = y0_w, []
    for p in powers_w:
        y = y + a * (p - y)
        out.append(y)
    return out


# --- Memory, bandwidth and local AI ----------------------------------------------

def bandwidth_gbs(bus_bits, mtps):
    """Peak DRAM bandwidth (GB/s) of a bus bus_bits wide at mtps mega-transfers/s."""
    return bus_bits / 8.0 * mtps * 1e6 / 1e9


def model_gb(params_b, bits):
    """Weight footprint (GB) of params_b billion parameters at bits per weight."""
    return params_b * 1e9 * bits / 8.0 / 1e9


def decode_tokens_s(bw_gbs, params_b, bits):
    """Bandwidth-bound decode speed: every token reads all weights once."""
    return bw_gbs / model_gb(params_b, bits)


def prefill_seconds(params_b, tokens, tops, utilization):
    """Compute-bound prefill time: 2 * params * tokens operations at tops * util."""
    return 2.0 * params_b * 1e9 * tokens / (tops * 1e12 * utilization)


def accel_power_w(ops_per_s, tops_per_w):
    """Power (W) of an accelerator sustaining ops_per_s at an efficiency in TOPS/W."""
    return ops_per_s / (tops_per_w * 1e12)


# --- Die cost: monolithic vs chiplets ---------------------------------------------

def dies_per_wafer(area_mm2, wafer_mm=300.0):
    """Gross dies per wafer (25-04): pi d^2/(4A) - pi d/sqrt(2A), rounded down."""
    d = wafer_mm
    return math.floor(math.pi * d * d / (4 * area_mm2) - math.pi * d / math.sqrt(2 * area_mm2))


def poisson_yield(area_mm2, d0_per_cm2):
    """Zero-defect probability exp(-A D0) with A in cm^2."""
    return math.exp(-area_mm2 / 100.0 * d0_per_cm2)


def die_cost(area_mm2, wafer_cost, d0_per_cm2):
    """Cost ($) per good die."""
    return wafer_cost / (dies_per_wafer(area_mm2) * poisson_yield(area_mm2, d0_per_cm2))


def chiplet_cost(tiles, package_cost, assembly_yield):
    """Cost ($) of a good multi-tile package: (sum of good-tile costs + package) / yield.
    tiles = [(area_mm2, wafer_cost, d0), ...]."""
    return (sum(die_cost(a, w, d) for a, w, d in tiles) + package_cost) / assembly_yield


def link_power_w(bw_gbs, pj_per_bit):
    """Power (W) to move bw_gbs across a link costing pj_per_bit."""
    return bw_gbs * 1e9 * 8 * pj_per_bit * 1e-12
