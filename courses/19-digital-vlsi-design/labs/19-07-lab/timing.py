"""Sequential timing models for Lab 19-07.

Setup and hold checks with skew and jitter, pipelining and sequencing overhead, two-phase latch time borrowing,
metastability (a cross-coupled inverter pair simulated as square-law ODEs, its resolution time constant, and
synchronizer MTBF). Units: SI unless a name says otherwise.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------- flip-flop timing
def min_period(t_pcq: float, t_pd: float, t_setup: float, skew: float = 0.0, jitter: float = 0.0) -> float:
    """Setup constraint: T_c >= t_pcq + t_pd + t_setup + t_jitter - skew, skew = capture clock - launch clock."""
    return t_pcq + t_pd + t_setup + jitter - skew


def hold_slack(t_ccq: float, t_cd: float, t_hold: float, skew: float = 0.0) -> float:
    """Hold constraint: t_ccq + t_cd >= t_hold + skew; returns the slack (negative = violation)."""
    return t_ccq + t_cd - (t_hold + skew)


def pipeline_period(t_logic: float, n_stages: int, t_overhead: float) -> float:
    return t_logic / n_stages + t_overhead


# ---------------------------------------------------------------- latches
def max_borrow(t_c: float, t_setup: float) -> float:
    """Two-phase, 50% duty clock: a latch-based path can borrow up to T_c/2 - t_setup into the next half-cycle."""
    return t_c / 2 - t_setup


def two_phase_min_period(t_logic_total: float, t_dq: float) -> float:
    """Two latches per cycle in the critical loop: T_c >= t_logic + 2 t_DQ (when every latch is transparent)."""
    return t_logic_total + 2 * t_dq


# ---------------------------------------------------------------- metastability
def i_sq(k: float, vov: float, vds: float) -> float:
    if vov <= 0 or vds <= 0:
        return 0.0
    return k * (vov * vds - vds * vds / 2) if vds < vov else 0.5 * k * vov * vov


def resolve_time(dv0: float, k: float = 200e-6, vdd: float = 1.2, vt: float = 0.35, c: float = 10e-15,
                 v_target: float = 0.9) -> float:
    """Cross-coupled symmetric inverters, each node loaded by c, starting at VDD/2 +/- dv0/2; time for the higher node
    to reach v_target."""
    def rhs(_t, v):
        v1, v2 = v
        d1 = (i_sq(k, vdd - v2 - vt, vdd - v1) - i_sq(k, v2 - vt, v1)) / c
        d2 = (i_sq(k, vdd - v1 - vt, vdd - v2) - i_sq(k, v1 - vt, v2)) / c
        return [d1, d2]
    ev = lambda _t, v: v[0] - v_target  # noqa: E731
    ev.terminal = True
    sol = solve_ivp(rhs, (0, 1e-7), [vdd / 2 + dv0 / 2, vdd / 2 - dv0 / 2], events=ev, method="LSODA", rtol=1e-12,
                    atol=1e-18)
    return float(sol.t_events[0][0])


def tau_small_signal(k: float = 200e-6, vdd: float = 1.2, vt: float = 0.35, c: float = 10e-15) -> float:
    """tau = C / (g_mn + g_mp) at the metastable point, g_m = k V_ov for each square-law device."""
    vov = vdd / 2 - vt
    return c / (2 * k * vov)


def mtbf(t_resolve: float, tau: float, t0: float, f_clk: float, f_data: float) -> float:
    """MTBF = exp(t_r / tau) / (T_0 f_clk f_data)."""
    return math.exp(t_resolve / tau) / (t0 * f_clk * f_data)
