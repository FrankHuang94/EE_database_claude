"""System budgets for chapter 27-01: power trees, thermal RC limits, roofline, pipelines and BOMs.

Every function is a closed form from the chapter; the verify script checks them by independent routes
(time-stepped thermal simulation, explicit pipelines, numerical derivatives).
"""
from __future__ import annotations

import math


def power_tree(loads: list[tuple[str, float, float]]) -> dict:
    """loads: (name, load power W, converter efficiency). Returns battery-side powers and totals."""
    rows = [(name, p, eta, p / eta, p / eta - p) for name, p, eta in loads]
    p_load = sum(r[1] for r in rows)
    p_batt = sum(r[3] for r in rows)
    return {"rows": rows, "p_load": p_load, "p_batt": p_batt, "eta": p_load / p_batt, "loss": p_batt - p_load}


def ldo_efficiency(v_out: float, v_in: float) -> float:
    """A linear regulator passes the load current, so its efficiency is at most V_out / V_in."""
    return v_out / v_in


def runtime_h(usable_wh: float, p_batt: float) -> float:
    return usable_wh / p_batt


def duty_average(modes: list[tuple[float, float]]) -> float:
    """modes: (duty fraction, power W). Duty fractions must sum to 1."""
    assert abs(sum(d for d, _ in modes) - 1) < 1e-9
    return sum(d * p for d, p in modes)


def sustained_power(t_limit: float, t_amb: float, theta: float) -> float:
    """Largest constant power that keeps T = T_amb + P*theta at or below the limit."""
    return (t_limit - t_amb) / theta


def rc_temperature(t: float, t0: float, t_amb: float, p: float, theta: float, c_th: float) -> float:
    """First-order thermal RC: T(t) = T_inf - (T_inf - T0) exp(-t/tau), T_inf = T_amb + P*theta."""
    t_inf = t_amb + p * theta
    return t_inf - (t_inf - t0) * math.exp(-t / (theta * c_th))


def time_to_limit(t0: float, t_limit: float, t_amb: float, p: float, theta: float, c_th: float) -> float:
    """Time for a burst of power p to heat the node from t0 to t_limit (inf if it never gets there)."""
    t_inf = t_amb + p * theta
    if t_inf <= t_limit:
        return math.inf
    return theta * c_th * math.log((t_inf - t0) / (t_inf - t_limit))


def max_burst_duty(p_burst: float, p_idle: float, p_sustained: float) -> float:
    """Duty cycle of a burst/idle pattern whose average equals the sustained limit (period << tau)."""
    return (p_sustained - p_idle) / (p_burst - p_idle)


def roofline(peak: float, bandwidth: float, intensity: float) -> float:
    """Attainable rate = min(peak, intensity x bandwidth); units follow the inputs."""
    return min(peak, intensity * bandwidth)


def ridge(peak: float, bandwidth: float) -> float:
    return peak / bandwidth


def decode_tokens_per_s(bandwidth_bytes: float, params: float, bytes_per_param: float) -> float:
    """Bandwidth-bound decode: every token step reads all weights once."""
    return bandwidth_bytes / (params * bytes_per_param)


def pipeline_throughput(stage_rates: dict[str, float]) -> tuple[str, float]:
    """The slowest stage sets the throughput of a pipeline; returns (bottleneck, rate)."""
    name = min(stage_rates, key=stage_rates.get)
    return name, stage_rates[name]


def littles_law(rate: float, latency: float) -> float:
    """Items in flight L = lambda * W."""
    return rate * latency


def amdahl(fractions_and_speedups: list[tuple[float, float]]) -> float:
    """Overall speedup when each fraction of the original time is sped up by its factor."""
    assert abs(sum(f for f, _ in fractions_and_speedups) - 1) < 1e-9
    return 1 / sum(f / s for f, s in fractions_and_speedups)


def bom(parts: dict[str, float], other_cogs: float, asp: float) -> dict:
    total = sum(parts.values())
    cogs = total + other_cogs
    return {"bom": total, "cogs": cogs, "gm": (asp - cogs) / asp,
            "share": {k: v / total for k, v in parts.items()}}


def perf_under_cap(p_dyn_budget: float, p_dyn_ref: float, ipc_gain: float = 1.0, power_factor: float = 1.0) -> float:
    """Relative performance under a fixed dynamic-power budget with P_dyn proportional to f^3.

    A change that multiplies IPC by ipc_gain and dynamic power at fixed frequency by power_factor
    runs at f/f0 = (budget / (power_factor * ref))^(1/3), so performance = ipc_gain * that.
    """
    return ipc_gain * (p_dyn_budget / (power_factor * p_dyn_ref)) ** (1 / 3)


def shadow_price_per_watt(p_dyn: float) -> float:
    """d ln(performance) / dP at a power cap with P_dyn ~ f^3: 1 / (3 P_dyn)."""
    return 1 / (3 * p_dyn)
