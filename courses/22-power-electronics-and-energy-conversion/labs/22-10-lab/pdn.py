"""Lab 22-10 helpers: distribution current and conductor loss, busbars with distributed loads, AC/DC conductor
capacity, conversion-chain efficiency and PUE, multiphase ripple cancellation, load lines, PDN target impedance
and the package–die resonance, plane resistance, and energy storage. SI units."""
from __future__ import annotations

import math

import numpy as np

RHO_CU = 1.72e-8      # Ω·m at 20 °C
DENSITY_CU = 8960.0   # kg/m³


# ---------------------------------------------------------------- distribution
def bar_resistance(length, area, rho=RHO_CU):
    return rho * length / area


def busbar_loss(i, r_loop, load="uniform"):
    """Loss in a busbar loop for a load at the far end ('end'), spread uniformly ('uniform') or at the midpoint."""
    factor = {"end": 1.0, "uniform": 1 / 3, "mid": 0.5}[load]
    return i * i * r_loop * factor


def per_conductor_ratio(v_dc, v_ll, n_ac=3, pf=1.0):
    """Power per conductor of 2-wire DC over n_ac-wire three-phase AC at the same current rating."""
    return n_ac * v_dc / (2 * math.sqrt(3) * v_ll * pf)


def chain_efficiency(etas):
    return float(np.prod(etas))


def facility_power(p_chip, etas, pue):
    return pue * p_chip / chain_efficiency(etas)


# ---------------------------------------------------------------- multiphase VRM
def phase_ripple(v_in, d, l, fs):
    return v_in * d * (1 - d) / (l * fs)


def summed_ripple(n, v_in, d, l, fs):
    """Peak-to-peak ripple of the sum of n interleaved buck inductor currents:
    (V_in T/L)(nD − m)(m + 1 − nD)/n, m = floor(nD)."""
    nd = n * d
    m = math.floor(nd + 1e-12)
    return v_in / (l * fs) * (nd - m) * (m + 1 - nd) / n


def max_slew(n, v_in, v_out, l):
    return n * (v_in - v_out) / l


def load_line(v_max, v_min, i_max):
    """Returns R_LL for AVP spanning the whole window."""
    return (v_max - v_min) / i_max


# ---------------------------------------------------------------- PDN
def target_impedance(dv, di):
    return dv / di


def resonance(l, c):
    """Returns (f0 Hz, Z0 Ω)."""
    return 1 / (2 * math.pi * math.sqrt(l * c)), math.sqrt(l / c)


def first_droop_undamped(di, l, c):
    return di * math.sqrt(l / c)


def sheet_resistance(t, rho=RHO_CU):
    return rho / t


def plane_path_loop(length, width, t, n_planes):
    """Loop resistance of a supply-and-return lateral path using n_planes in parallel each way."""
    return 2 * sheet_resistance(t) * (length / width) / n_planes


def storage_capacitance(energy, v1, v2):
    return 2 * energy / (v1 * v1 - v2 * v2)
