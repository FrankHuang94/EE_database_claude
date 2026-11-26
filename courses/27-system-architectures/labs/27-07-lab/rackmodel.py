"""Models for Chapter 27-07 (The AI datacenter server and rack).

Each function is a first-order engineering model from the chapter. Units are in
every docstring. Parameter values used in the chapter are illustrative
assumptions unless a source is cited there.
"""
import math

SECONDS_PER_DAY = 86400.0
HOURS_PER_YEAR = 8760.0


# --- Reading a rack ------------------------------------------------------------

def per_device(rack_total, n_devices):
    """Share of a rack-level figure per device (same units as rack_total)."""
    return rack_total / n_devices


def machine_balance(flops, bytes_per_s):
    """Peak compute over memory bandwidth (FLOP per byte): the roofline ridge point."""
    return flops / bytes_per_s


# --- Power ---------------------------------------------------------------------

def rack_power_kw(n_gpu, p_gpu_kw, n_cpu, p_cpu_kw, n_tray, p_tray_other_kw,
                  n_switch, p_switch_kw, p_fans_kw, eta_conv):
    """Rack input power (kW): the sum of the IT loads at the busbar divided by the
    power-shelf efficiency eta_conv. Returns (busbar load kW, input kW)."""
    load = (n_gpu * p_gpu_kw + n_cpu * p_cpu_kw + n_tray * p_tray_other_kw
            + n_switch * p_switch_kw + p_fans_kw)
    return load, load / eta_conv


def facility_power_kw(p_it_kw, pue):
    """Facility power (kW) for an IT load at a given power usage effectiveness."""
    return p_it_kw * pue


# --- Training compute ------------------------------------------------------------

def training_flops(n_params, n_tokens):
    """Training compute (FLOP) for a dense transformer: 6 N D (2 forward, 4 backward
    FLOPs per parameter per token; attention's context-dependent FLOPs neglected)."""
    return 6.0 * n_params * n_tokens


def training_days(flops, n_gpu, achieved_flops_per_gpu):
    """Wall-clock days of pure compute at an achieved per-GPU rate (FLOP/s)."""
    return flops / (n_gpu * achieved_flops_per_gpu) / SECONDS_PER_DAY


def gpus_for_deadline(flops, achieved_flops_per_gpu, days, effective_fraction=1.0):
    """GPUs needed to finish `flops` in `days` with a fraction of elapsed time useful."""
    return flops / (achieved_flops_per_gpu * effective_fraction * days * SECONDS_PER_DAY)


def energy_gwh(power_w, seconds):
    """Energy (GWh) of a constant power (W) over a time (s)."""
    return power_w * seconds / 3.6e12


# --- Collectives -------------------------------------------------------------------

def ring_allreduce_s(size_bytes, p, bw_bytes_per_s, alpha_s=0.0):
    """Ring all-reduce time (s): reduce-scatter then all-gather, 2(p-1) steps of
    size/p each, T = 2(p-1)/p * S/B + 2(p-1) alpha."""
    if p <= 1:
        return 0.0
    return 2.0 * (p - 1) / p * size_bytes / bw_bytes_per_s + 2.0 * (p - 1) * alpha_s


def hierarchical_allreduce_s(size_bytes, p_in, bw_in, p_out, bw_out):
    """Two-level all-reduce (s): reduce-scatter and all-gather inside each scale-up
    domain of p_in GPUs at bw_in, plus a ring all-reduce of each 1/p_in shard across
    p_out domains at bw_out (every GPU's own NIC works in parallel). Bandwidth terms
    only. Returns (inside, across, total)."""
    inside = ring_allreduce_s(size_bytes, p_in, bw_in)
    across = ring_allreduce_s(size_bytes / p_in, p_out, bw_out)
    return inside, across, inside + across


# --- Reliability -------------------------------------------------------------------

def mean_time_between(period_s, n_events):
    """Mean time between events (s) observed over a period."""
    return period_s / n_events


def young_interval_s(delta_s, mtbf_s):
    """Young's first-order optimal checkpoint interval sqrt(2 delta M) (s)."""
    return math.sqrt(2.0 * delta_s * mtbf_s)


def lost_fraction(tau_s, delta_s, mtbf_s, restart_s):
    """First-order fraction of elapsed time lost: checkpoint writing delta/tau, rework
    of half an interval and a restart per failure (tau/2 + R)/M."""
    return delta_s / tau_s + (tau_s / 2.0 + restart_s) / mtbf_s


def max_restart_s(target_lost, delta_s, mtbf_s):
    """Largest restart time (s) that keeps the lost fraction at target_lost when
    checkpoints are taken at Young's interval."""
    return (target_lost - math.sqrt(2.0 * delta_s / mtbf_s)) * mtbf_s


# --- Inference serving ---------------------------------------------------------------

def decode_step_s(batch, weight_bytes, kv_bytes_per_seq, bw_bytes_per_s, eta_bw,
                  active_params, flops_peak):
    """Decode step time (s) for one token per sequence: the larger of the memory time
    (weights once plus every sequence's KV cache, at eta_bw of peak bandwidth) and
    the compute time (2 FLOPs per active parameter per token). Returns
    (step, memory time, compute time)."""
    t_mem = (weight_bytes + batch * kv_bytes_per_seq) / (eta_bw * bw_bytes_per_s)
    t_cmp = 2.0 * active_params * batch / flops_peak
    return max(t_mem, t_cmp), t_mem, t_cmp


def max_batch(hbm_bytes, weight_bytes, kv_bytes_per_seq):
    """Largest batch whose KV caches fit beside the weights (activations neglected)."""
    return math.floor((hbm_bytes - weight_bytes) / kv_bytes_per_seq)


def cost_per_million_tokens(capex_usd, years, p_it_kw, pue, usd_per_kwh,
                            tokens_per_s, utilization):
    """Cost (USD) per million tokens: straight-line capital cost plus energy, over the
    tokens served at a utilization. Returns (cost, annual capex, annual energy cost,
    tokens per year)."""
    capex_yr = capex_usd / years
    energy_yr = p_it_kw * pue * HOURS_PER_YEAR * usd_per_kwh
    tokens_yr = tokens_per_s * utilization * HOURS_PER_YEAR * 3600.0
    return (capex_yr + energy_yr) / (tokens_yr / 1e6), capex_yr, energy_yr, tokens_yr
