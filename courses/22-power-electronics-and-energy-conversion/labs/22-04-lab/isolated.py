"""Lab 22-04 helpers: flyback and forward converters, leakage-clamp loss, core flux, and insulation arithmetic."""
from __future__ import annotations

import math


# ---------------------------------------------------------------- flyback
def flyback_duty(v_in, v_out, n):
    """CCM (and boundary) duty cycle: D/D' = n V / V_in."""
    return n * v_out / (v_in + n * v_out)


def flyback_switch_voltage(v_in, v_out, n):
    return v_in + n * v_out


def flyback_dcm_power(v_in, d, fs, lm):
    ipk = v_in * d / (fs * lm)
    return ipk, 0.5 * lm * ipk * ipk * fs


def flyback_boundary_design(p_in, v_in_min, v_out, n, fs):
    """Boundary conduction at the lowest input: returns (D, I_pk, L_m)."""
    d = flyback_duty(v_in_min, v_out, n)
    ipk = 2 * p_in / (v_in_min * d)
    return d, ipk, v_in_min * d / (fs * ipk)


def flyback_dcm_boundary_current(v_in, v_out, n, fs, lm):
    d = flyback_duty(v_in, v_out, n)
    dim = v_in * d / (fs * lm)
    return n * (1 - d) * dim / 2


def clamp_energy(l_lk, i_pk, v_clamp, v_reflected):
    """Energy absorbed per cycle by an RCD clamp held at v_clamp above the bus."""
    return 0.5 * l_lk * i_pk * i_pk * v_clamp / (v_clamp - v_reflected)


# ---------------------------------------------------------------- forward and bridges
def forward_duty(v_in, v_out, n):
    return n * v_out / v_in


def forward_max_duty(n3_over_n1):
    return 1 / (1 + n3_over_n1)


def forward_switch_voltage(v_in, n3_over_n1):
    return v_in * (1 + 1 / n3_over_n1)


def flux_swing(v, t_on, turns, area_m2):
    return v * t_on / (turns * area_m2)


# ---------------------------------------------------------------- insulation
def y_cap_current(c, v_rms, f):
    return 2 * math.pi * f * c * v_rms


def y_cap_limit(i_max, v_rms, f):
    return i_max / (2 * math.pi * f * v_rms)
