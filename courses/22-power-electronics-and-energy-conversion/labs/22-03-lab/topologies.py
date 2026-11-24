"""Lab 22-03 helpers: conversion ratios, currents, ripples and stresses of the boost, buck-boost, Cuk and SEPIC;
the boost with winding resistance; boost DCM; the averaged SEPIC with winding resistances.
"""
from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------- CCM ratios
def ratio(topology, d):
    dp = 1 - d
    return {"buck": d, "boost": 1 / dp, "buck-boost": -d / dp, "cuk": -d / dp, "sepic": d / dp}[topology]


def boost_duty(v_in, v_out):
    return 1 - v_in / v_out


def buck_boost_duty(v_in, v_out_mag):
    return v_out_mag / (v_in + v_out_mag)


# ---------------------------------------------------------------- boost currents and ripples
def boost_inductor_current(i_out, d):
    return i_out / (1 - d)


def boost_ripple_current(v_in, d, fs, ind):
    return v_in * d / (fs * ind)


def boost_output_ripple(i_out, d, fs, cap):
    return i_out * d / (fs * cap)


def boost_cout_rms(i_out, d):
    return i_out * math.sqrt(d / (1 - d))


def boost_rhp_zero_hz(d, r_load, ind):
    return (1 - d) ** 2 * r_load / (2 * math.pi * ind)


# ---------------------------------------------------------------- boost with resistance
def boost_ratio_with_rl(d, r_l, r_load):
    dp = 1 - d
    return (1 / dp) / (1 + r_l / (dp * dp * r_load))


def boost_efficiency_with_rl(d, r_l, r_load):
    dp = 1 - d
    return 1 / (1 + r_l / (dp * dp * r_load))


def boost_max_gain(r_l, r_load):
    return 0.5 * math.sqrt(r_load / r_l), 1 - math.sqrt(r_l / r_load)


# ---------------------------------------------------------------- boost DCM
def boost_k_crit(d):
    return d * (1 - d) ** 2


def boost_dcm_ratio(d, k):
    return (1 + math.sqrt(1 + 4 * d * d / k)) / 2


def boost_ratio_any(d, k):
    return 1 / (1 - d) if k >= boost_k_crit(d) else boost_dcm_ratio(d, k)


# ---------------------------------------------------------------- SEPIC averaged model with winding resistances
def sepic_dc(v_in, d, r_load, r1, r2):
    """Solve the four averaged equations for (V_out, V_C1, I_L1, I_L2) with winding resistances r1, r2."""
    dp = 1 - d
    # unknowns x = [V, Vc1, I1, I2]
    a = np.array([
        [dp, dp, r1, 0.0],          # Vin - I1 r1 - D'(V + Vc1) = 0
        [dp, -d, 0.0, r2],          # -D Vc1 + D' V + I2 r2 = 0
        [0.0, 0.0, dp, -d],         # I1 D' = I2 D
        [-1.0 / r_load, 0.0, dp, dp],  # D'(I1 + I2) = V / R
    ])
    b = np.array([v_in, 0.0, 0.0, 0.0])
    return np.linalg.solve(a, b)


def switch_stress(topology, v_in, v_out, d):
    """Active-switch V_pk * I_pk / P_out with small ripple (I in units of the load current)."""
    dp = 1 - d
    vo = abs(v_out)
    if topology == "buck":
        return v_in / vo
    if topology == "boost":
        return 1 / dp
    return (v_in + vo) / (vo * dp)
