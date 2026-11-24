"""Lab 22-06 helpers: switch loss mechanisms, device sizing, electrothermal operating point and ZVS conditions.

SI units (V, A, s, Hz, Ω, C, F, J, W, K).
"""
from __future__ import annotations

import math


# ---------------------------------------------------------------- loss mechanisms
def conduction(i_rms, r_on):
    return i_rms ** 2 * r_on


def overlap(v, i, t_on, t_off, fs):
    """Clamped-inductive hard switching with linear ramps: ½ V I (t_on + t_off) f_s."""
    return 0.5 * v * i * (t_on + t_off) * fs


def coss_hard_turn_on(q_oss, v, fs):
    """Half-bridge hard turn-on: Q_oss V per transition."""
    return q_oss * v * fs


def recovery(q_rr, v, fs):
    return q_rr * v * fs


def gate_drive(q_g, v_drv, fs):
    return q_g * v_drv * fs


def dead_time(v_sd, i, t_d, fs, edges=2):
    return edges * v_sd * i * t_d * fs


# ---------------------------------------------------------------- nonlinear output capacitance C0/(1 + v/V0)^m
def coss_junction(c0, v0, m, v):
    return c0 / (1 + v / v0) ** m


def qoss_junction(c0, v0, m, v):
    """∫0^V C dv for C = C0/(1 + v/V0)^m (m ≠ 1)."""
    return c0 * v0 / (1 - m) * ((1 + v / v0) ** (1 - m) - 1)


def eoss_junction(c0, v0, m, v):
    """∫0^V v C dv for C = C0/(1 + v/V0)^m (m ≠ 1, m ≠ 2), by parts on u = 1 + v/V0."""
    u = 1 + v / v0
    return c0 * v0 ** 2 * ((u ** (2 - m) - 1) / (2 - m) - (u ** (1 - m) - 1) / (1 - m))


# ---------------------------------------------------------------- sizing and FOM
def optimal_resistance(fom, v, fs, i_rms):
    """Minimize I²R + FOM·V·f/R: R* = √(FOM V f)/I."""
    return math.sqrt(fom * v * fs) / i_rms


def minimum_loss(fom, v, fs, i_rms):
    return 2 * i_rms * math.sqrt(fom * v * fs)


def baliga_relative(eps_r, mu, ec, eps_ref=11.9, mu_ref=1240.0, ec_ref=0.3):
    return eps_r * mu * ec ** 3 / (eps_ref * mu_ref * ec_ref ** 3)


# ---------------------------------------------------------------- electrothermal
def junction_temperature(t_amb, r_th, i_rms, r25, slope):
    """R(T) = r25 + slope (T − 25 °C); T = T_a + R_th I² R(T). slope in Ω/K. Returns inf at runaway."""
    a = r_th * i_rms ** 2
    den = 1 - a * slope
    if den <= 0:
        return math.inf
    return (t_amb + a * (r25 - 25 * slope)) / den


def runaway_current(r_th, slope):
    return 1 / math.sqrt(r_th * slope)


# ---------------------------------------------------------------- soft switching
def zvs_transition_time(q_oss, i):
    return 2 * q_oss / i


def zvs_min_current(q_oss, t_dead):
    return 2 * q_oss / t_dead


def llc_magnetizing_peak(v_bus, l_m, fs, bridge="half"):
    """Half bridge: the primary sees ±V/2, so I_pk = V/(8 L_m f). Full bridge: V/(4 L_m f)."""
    return v_bus / ((8 if bridge == "half" else 4) * l_m * fs)
