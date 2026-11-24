"""Lab 20-12: why analog does not scale like digital.

- constant_field: how delay, switching energy, area and power density change when a process is scaled by S
  at constant field (09-11).
- ktc_capacitance, thermal_power: the capacitance a kT/C-limited circuit needs for a given SNR and swing, and the
  power to drive it at a given closed-loop bandwidth with a given gm/ID.
- intrinsic_gain, stack_swing: one transistor's gain (gm/ID) V_A and the swing left after stacking devices.
- level1_id, cascode_current: square-law drain current with channel-length modulation and a cascoded current sink
  solved for its internal node (compare with stack.cir).
- two_step_adc, sndr: a 4-bit coarse + 8-bit fine two-step converter whose residue amplifier has a gain error, with
  optional digital correction, and its SNDR for a coherent sine.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize

K_B = 1.380649e-23


def constant_field(s):
    """Factors for delay, energy per switching, area and power density after scaling dimensions and voltages by 1/s."""
    return {"delay": 1 / s, "energy": 1 / s ** 3, "area": 1 / s ** 2, "power_density": 1.0}


def ktc_capacitance(snr_db, amplitude, temp=300.0):
    """Capacitance for SNR = (A^2/2) / (kT/C) with a sine of peak amplitude A (V)."""
    return 2 * K_B * temp * 10 ** (snr_db / 10) / amplitude ** 2


def thermal_power(snr_db, bandwidth, vdd, eta=0.8, gm_over_id=15.0, beta=1.0, temp=300.0):
    """Supply power of a class-A stage that drives the kT/C-sized capacitor at a closed-loop bandwidth
    beta gm / (2 pi C); the peak amplitude is eta * vdd / 2. Returns (C, gm, I, P)."""
    c = ktc_capacitance(snr_db, eta * vdd / 2, temp)
    gm = 2 * math.pi * bandwidth * c / beta
    i = gm / gm_over_id
    return c, gm, i, vdd * i


def intrinsic_gain(gm_over_id, v_a):
    return gm_over_id * v_a


def stack_swing(vdd, n_stack, vdsat):
    """Voltage left for signal after n stacked devices each need vdsat."""
    return vdd - n_stack * vdsat


def level1_id(vgs, vds, kp=300e-6, w_over_l=20.0, vt=0.4, lam=0.2):
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    if vds >= vov:
        return kp * w_over_l / 2 * vov ** 2 * (1 + lam * vds)
    return kp * w_over_l * (vov * vds - vds ** 2 / 2) * (1 + lam * vds)


def cascode_current(vout, vb1=0.55, vb2=0.75, **kw):
    """Current of a cascoded sink (bottom gate vb1, cascode gate vb2) at output voltage vout; returns (I, V_x)."""
    hi = min(vout, vb2 - kw.get("vt", 0.4))
    x = optimize.brentq(lambda v: level1_id(vb1, v, **kw) - level1_id(vb2 - v, vout - v, **kw), 0.0, hi)
    return level1_id(vb1, x, **kw), x


def two_step_adc(x, eps, eps_hat=0.0):
    """Two-step ADC on [0, 1): 4-bit coarse code, residue amplified by 16 (1 - eps), 8-bit fine quantizer.
    The digital output divides the fine code by (1 - eps_hat) before combining."""
    d1 = np.floor(16 * x)
    r = (16 * x - d1) * (1 - eps)
    d2 = (np.floor(np.clip(r, 0, 1 - 1e-12) * 256) + 0.5) / 256
    return (d1 + d2 / (1 - eps_hat)) / 16


def sndr(y, x):
    """SNDR (dB) of output y against the ideal input x (both arrays), removing any gain and offset by least squares."""
    a = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(a, y, rcond=None)
    err = y - a @ coef
    sig = coef[0] ** 2 * np.var(x)
    return 10 * math.log10(sig / np.mean(err ** 2))
