"""Lab 22-02 helpers: buck converter steady state in CCM and DCM, ripples, RMS currents, conduction losses,
PFM pulses and design limits.

`pss` solves the exact periodic steady state of a buck with switch and winding resistances by matrix
exponentials of the two switched linear circuits; the other functions are the chapter's closed forms.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm


# ---------------------------------------------------------------- CCM closed forms
def ripple_current(v_out, d, fs, ind):
    return v_out * (1 - d) / (fs * ind)


def inductance_for_ratio(v_out, d, fs, r, i_out):
    return v_out * (1 - d) / (fs * r * i_out)


def ripple_voltage(di, fs, cap, esr=0.0):
    """Capacitive ripple plus (conservatively) the ESR ripple."""
    return di / (8 * fs * cap) + esr * di


def rms_currents(i_out, d, di):
    """(inductor, high side, low side, input capacitor, output capacitor) RMS currents for a triangular ripple
    (the output-capacitor value assumes all the ripple flows in the capacitor)."""
    r = di / i_out
    il = i_out * math.sqrt(1 + r * r / 12)
    cin = math.sqrt(d * il * il - (d * i_out) ** 2)
    return il, math.sqrt(d) * il, math.sqrt(1 - d) * il, cin, di / (2 * math.sqrt(3))


def duty_with_resistances(v_in, v_out, i_out, r_hs, r_ls, r_l):
    """Duty cycle that gives v_out at i_out with conduction drops: V = D Vin - I (D Rhs + D' Rls + RL)."""
    return (v_out + i_out * (r_ls + r_l)) / (v_in - i_out * (r_hs - r_ls))


def duty_with_diode(v_in, v_out, i_out, v_f, r_hs, r_l):
    return (v_out + v_f + i_out * r_l) / (v_in + v_f - i_out * r_hs)


# ---------------------------------------------------------------- exact periodic steady state
def pss(v_in, d, fs, ind, cap, r_load, r_hs=0.0, r_ls=0.0, r_l=0.0, npts=20001):
    """Exact CCM-or-negative-current periodic steady state (synchronous, forced PWM).

    Returns t, i_L, v_out over one period and the average input and output powers.
    """
    t_s = 1.0 / fs

    def aug(vs, rs):
        m = np.zeros((3, 3))
        m[0, 0] = -(rs + r_l) / ind
        m[0, 1] = -1.0 / ind
        m[1, 0] = 1.0 / cap
        m[1, 1] = -1.0 / (r_load * cap)
        m[0, 2] = vs / ind
        return m

    def charge_on(x0):
        """Exact input charge during the on-time: integrate i_L with a fourth (integrator) state."""
        m = np.zeros((4, 4))
        m[:3, :3] = aug(v_in, r_hs)
        m[3, 0] = 1.0
        return (expm(m * d * t_s) @ np.array([x0[0], x0[1], 1.0, 0.0]))[3]

    p1 = expm(aug(v_in, r_hs) * d * t_s)
    p2 = expm(aug(0.0, r_ls) * (1 - d) * t_s)
    p = p2 @ p1
    x0 = np.linalg.solve(np.eye(2) - p[:2, :2], p[:2, 2])
    t = np.linspace(0.0, t_s, npts)
    il = np.empty_like(t)
    vo = np.empty_like(t)
    for k, tk in enumerate(t):
        m = expm(aug(v_in, r_hs) * tk) if tk <= d * t_s else expm(aug(0.0, r_ls) * (tk - d * t_s)) @ p1
        il[k], vo[k] = m[:2, :2] @ x0 + m[:2, 2]
    p_in = v_in * charge_on(x0) / t_s
    p_out = np.trapezoid(vo ** 2 / r_load, t) / t_s
    return t, il, vo, p_in, p_out


# ---------------------------------------------------------------- DCM
def k_param(ind, r_load, fs):
    return 2 * ind * fs / r_load


def critical_current(v_out, d, fs, ind):
    return ripple_current(v_out, d, fs, ind) / 2


def dcm_ratio(d1, k):
    return 2 / (1 + math.sqrt(1 + 4 * k / d1 ** 2))


def dcm_duty_for_ratio(m, k):
    return math.sqrt(4 * k / ((2 / m - 1) ** 2 - 1))


def buck_ratio(d, k):
    """Conversion ratio of a diode buck: D in CCM, the DCM formula below the boundary."""
    return d if k >= 1 - d else dcm_ratio(d, k)


# ---------------------------------------------------------------- PFM and limits
def pfm_pulse(v_in, v_out, t_on, ind):
    """Peak current, off-time and charge of one fixed-on-time DCM pulse."""
    ipk = (v_in - v_out) * t_on / ind
    t_off = t_on * (v_in - v_out) / v_out
    return ipk, t_off, 0.5 * ipk * (t_on + t_off)


def max_frequency(v_in, v_out, t_on_min):
    return (v_out / v_in) / t_on_min
