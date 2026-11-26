"""Smartphone SoC models for chapter 27-02: memory bandwidth, heterogeneous cores and DVFS,
on-device language-model decode, die cost and BOM shifts.

All parameter values used in the chapter are assumed for teaching unless a source is cited there.
"""
from __future__ import annotations

import math

from scipy import optimize


def lpddr_bandwidth_gbs(data_rate_mts: float, bus_bits: int = 64) -> float:
    """Peak bandwidth in GB/s = transfers per second x bus width in bytes."""
    return data_rate_mts * 1e6 * bus_bits / 8 / 1e9


def dram_traffic(demands: dict[str, float], slc_hit: dict[str, float]) -> float:
    """DRAM traffic after a system-level cache: each client's demand times its miss rate."""
    return sum(d * (1 - slc_hit.get(k, 0.0)) for k, d in demands.items())


def voltage(f_ghz: float, v0: float, k: float) -> float:
    """Linear voltage-frequency curve above threshold, V = V0 + k f."""
    return v0 + k * f_ghz


def epi_nj(f_ghz: float, c_nf: float, v0: float, k: float, ipc: float, p_static_w: float) -> float:
    """Energy per instruction (nJ) at frequency f: dynamic c V^2 per cycle over IPC, plus static power x time."""
    v = voltage(f_ghz, v0, k)
    dynamic = c_nf * v * v / ipc               # nF x V^2 = nJ per cycle, divided by instructions per cycle
    static = p_static_w / (ipc * f_ghz)        # W / (instructions per ns) = nJ per instruction
    return dynamic + static


def core_power_w(f_ghz: float, c_nf: float, v0: float, k: float, p_static_w: float) -> float:
    v = voltage(f_ghz, v0, k)
    return c_nf * v * v * f_ghz + p_static_w   # nJ x GHz = W


def epi_at_perf(gips: float, core: dict) -> float:
    """Energy per instruction for a core delivering `gips` billion instructions/s (inf if beyond f_max)."""
    f = gips / core["ipc"]
    if f > core["f_max"]:
        return math.inf
    return epi_nj(f, core["c"], core["v0"], core["k"], core["ipc"], core["ps"])


def crossover_gips(big: dict, little: dict) -> float:
    """Performance at which the big core becomes as efficient as the little core."""
    hi = little["ipc"] * little["f_max"]
    return optimize.brentq(lambda s: epi_at_perf(s, big) - epi_at_perf(s, little), 0.2, hi - 1e-9)


def f_min_energy(core: dict) -> float:
    """Frequency (GHz) that minimizes energy per instruction: 2 c k V(f) / IPC = P_s / (IPC f^2)."""
    res = optimize.minimize_scalar(lambda f: epi_nj(f, core["c"], core["v0"], core["k"], core["ipc"], core["ps"]),
                                   bounds=(0.05, core["f_max"]), method="bounded", options={"xatol": 1e-10})
    return res.x


def decode_tokens_per_s(bandwidth_gbs: float, params_b: float, bits: float) -> float:
    """Bandwidth bound on decode: each token reads every weight once."""
    return bandwidth_gbs / (params_b * bits / 8)


def decode_energy_mj(params_b: float, bits: float, pj_per_bit: float) -> float:
    """DRAM energy per token (mJ) to read the weights once."""
    return params_b * 1e9 * bits * pj_per_bit * 1e-12 * 1e3


def dies_per_wafer(area_mm2: float, d_mm: float = 300) -> int:
    return int(math.pi * d_mm ** 2 / (4 * area_mm2) - math.pi * d_mm / math.sqrt(2 * area_mm2))


def die_cost(wafer_usd: float, area_mm2: float, d0_per_cm2: float) -> tuple[int, float, float]:
    dpw = dies_per_wafer(area_mm2)
    y = math.exp(-area_mm2 / 100 * d0_per_cm2)
    return dpw, y, wafer_usd / (dpw * y)


def memory_share_shift(share_before: float, share_after: float) -> tuple[float, float]:
    """If only memory's cost changes, return (memory cost multiple, BOM multiple)."""
    other = 1 - share_before
    mem_after = share_after * other / (1 - share_after)
    return mem_after / share_before, other + mem_after
