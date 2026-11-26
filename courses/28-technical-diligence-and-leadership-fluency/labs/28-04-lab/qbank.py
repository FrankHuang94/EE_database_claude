"""Quantitative checks behind the diligence question banks (chapter 28-04): iso-power CPU
claims, decode on the roofline, memory and link power, optics ports and interview scoring.

Units: FLOP/s and bytes/s for the roofline, GB/s (1e9 bytes/s) for memory interfaces,
joules per bit (pJ/bit = 1e-12 J/bit) for link and memory energy, watts for power.
"""
from __future__ import annotations

import math

# --- Digital and CPU claims --------------------------------------------------------


def iso_power(perf_ratio, ipc_ratio, cap_ratio=1.0):
    """Requirement behind a claim of perf_ratio more performance at the same power.

    Performance is IPC x f and dynamic power rises as C f^3 along the voltage-frequency
    line. Returns (frequency ratio, power factor at fixed energy per op, required
    fractional reduction in energy per operation)."""
    f_ratio = perf_ratio / ipc_ratio
    power_factor = cap_ratio * f_ratio ** 3
    return f_ratio, power_factor, 1 - 1 / power_factor


def ddr_channel_gbs(mt_per_s, data_bits=64):
    """Peak bandwidth of a DRAM channel in GB/s from its transfer rate in MT/s."""
    return mt_per_s * 1e6 * data_bits / 8 / 1e9


# --- AI accelerators -----------------------------------------------------------------


def ridge_point(peak_flops, mem_bw):
    """Arithmetic intensity (FLOP/byte) at which compute and memory limits meet."""
    return peak_flops / mem_bw


def decode_intensity(batch, bytes_per_weight):
    """FLOP per byte of weights in decode: 2 FLOP per weight per sequence, each weight read
    once per step (KV-cache traffic ignored)."""
    return 2 * batch / bytes_per_weight


def attainable(intensity, peak_flops, mem_bw):
    """Roofline: the lesser of the compute peak and intensity x bandwidth (FLOP/s)."""
    return min(peak_flops, intensity * mem_bw)


def batch_at_ridge(peak_flops, mem_bw, bytes_per_weight):
    """Batch at which decode intensity reaches the ridge point."""
    return bytes_per_weight * ridge_point(peak_flops, mem_bw) / 2


def devices_for(total_bytes, bytes_per_device):
    """Smallest number of devices whose memory holds total_bytes."""
    return math.ceil(total_bytes / bytes_per_device - 1e-12)


# --- Memory, links and optics ----------------------------------------------------------


def stack_gbs(interface_bits, gbps_per_pin):
    """Bandwidth of a memory stack or interface in GB/s."""
    return interface_bits * gbps_per_pin / 8


def link_power_w(bytes_per_s, pj_per_bit):
    """Power of moving bytes_per_s at pj_per_bit."""
    return bytes_per_s * 8 * pj_per_bit * 1e-12


def bits_power_w(bits_per_s, pj_per_bit):
    """Power of moving bits_per_s at pj_per_bit."""
    return bits_per_s * pj_per_bit * 1e-12


def shoreline_mm(gb_per_s, gb_per_s_per_mm):
    """Die edge needed for a bandwidth at a shoreline density."""
    return gb_per_s / gb_per_s_per_mm


def port_pj_per_bit(port_watts, port_bits_per_s):
    """Energy per bit of a port from its power and rate."""
    return port_watts / port_bits_per_s * 1e12


def dbm_to_mw(dbm):
    """Optical or electrical power in mW from dBm."""
    return 10 ** (dbm / 10)


def db_to_ratio(db):
    """Power ratio from decibels."""
    return 10 ** (db / 10)


# --- Scoring answers ---------------------------------------------------------------------


def posterior(prior, ratios):
    """Posterior (odds, probability) from a prior probability and the likelihood ratios of
    conditionally independent answers."""
    odds = prior / (1 - prior)
    for r in ratios:
        odds *= r
    return odds, odds / (1 + odds)


def strong_needed(prior, recorded, ratio_strong, target):
    """Fewest further answers of ratio_strong that lift the posterior to at least target,
    given answers already recorded."""
    odds, _ = posterior(prior, recorded)
    goal = target / (1 - target)
    n = 0
    while odds < goal:
        odds *= ratio_strong
        n += 1
    return n


def trajectory(prior, ratios):
    """Posterior probability after each answer, starting with the prior."""
    out = [prior]
    for k in range(len(ratios)):
        out.append(posterior(prior, ratios[: k + 1])[1])
    return out
