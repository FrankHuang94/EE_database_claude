"""Lab 22-08 helpers: rail allocation, PFM/PWM crossover, usage-profile battery life, DVS ramps and loop tracking,
AVS savings, soft start, sequencing and power-gating break-even. SI units throughout."""
from __future__ import annotations

import math


# ---------------------------------------------------------------- rail allocation
def ldo_efficiency(v_out, i_load, v_in, i_q=0.0):
    """Efficiency of an LDO: the load current plus its quiescent current flow from v_in."""
    return v_out * i_load / (v_in * (i_load + i_q))


def chain_efficiency(eta_buck, v_out, v_mid):
    """A buck to v_mid followed by an LDO to v_out (LDO quiescent current neglected)."""
    return eta_buck * v_out / v_mid


# ---------------------------------------------------------------- light load
def pwm_loss(i, p_fixed, r):
    return p_fixed + r * i * i


def pfm_loss(i, v_in, i_q, alpha, r_p):
    return v_in * i_q + alpha * i + r_p * i * i


def pfm_pwm_crossover(p_fixed, r, v_in, i_q, alpha, r_p):
    """Load current at which the PFM and PWM loss models are equal (requires r_p > r)."""
    a, b, c = r_p - r, alpha, v_in * i_q - p_fixed
    return (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)


def efficiency(p_out, p_loss):
    return p_out / (p_out + p_loss)


# ---------------------------------------------------------------- usage profile
def daily_energy(states, v_bat, i_q, t_day=86400.0):
    """states: iterable of (output power W, duration s, efficiency). Returns (per-state energies J, PMIC J, total J)."""
    e = [p * t / eta for p, t, eta in states]
    e_q = v_bat * i_q * t_day
    return e, e_q, sum(e) + e_q


def battery_energy(q_mah, v_bat):
    return q_mah * 1e-3 * 3600 * v_bat


# ---------------------------------------------------------------- DVS
def dvs_ramp(c, v1, v2, slew):
    """Returns (ramp time s, capacitor current A, stored energy J) for a ramp from v1 to v2 at slew V/s."""
    return abs(v2 - v1) / slew, c * slew, 0.5 * c * (v2 * v2 - v1 * v1)


def pfm_down_time(c, dv, i_load):
    """Time for the load alone to discharge c by dv (a PFM converter cannot sink current)."""
    return c * dv / i_load


def ramp_lead(slew, w_i, v_m, v_g):
    """Steady lead of the output over a ramping reference for the op-amp type-III loop with the reference on the
    non-inverting input: e = (S / w_I)(1 − V_M / V_g)."""
    return slew / w_i * (1 - v_m / v_g)


# ---------------------------------------------------------------- AVS, soft start, sequencing, gating
def avs_ratio(v_old, v_new):
    """Ratio of dynamic power at the same frequency."""
    return (v_new / v_old) ** 2


def soft_start(c, v, i_ss):
    """Returns (ramp time s, energy dissipated in the switch J); the energy does not depend on i_ss."""
    return c * v / i_ss, 0.5 * c * v * v


def sequence_time(n_rails, slot, groups=None):
    """Power-up time with each rail taking `slot` seconds; `groups` rails come up together (default: one at a time)."""
    groups = n_rails if groups is None else groups
    return groups * slot


def leakage_at(p_ref, t, t_ref=25.0, t_double=25.0):
    return p_ref * 2 ** ((t - t_ref) / t_double)


def gating_breakeven(c, v, e_state, p_leak):
    """Idle time beyond which gating a domain saves energy: (C V² + E_state) / P_leak."""
    return (c * v * v + e_state) / p_leak
