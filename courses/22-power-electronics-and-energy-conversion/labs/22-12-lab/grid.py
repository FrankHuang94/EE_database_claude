"""Lab 22-12 helpers: per-unit bases and base changes, line parameters and SIL, two-bus power flow and voltage drop,
fault currents, RoCoF and droop, and a swing-equation frequency-response model. SI units unless stated."""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate

MU0 = 4e-7 * math.pi
EPS0 = 8.854187817e-12


def bases(s_b, v_b):
    """Returns (Z_base Ω, I_base A) for a three-phase MVA/kV base given in VA and V."""
    return v_b ** 2 / s_b, s_b / (math.sqrt(3) * v_b)


def change_base(z_pu, s_old, s_new, v_old, v_new):
    return z_pu * (v_old / v_new) ** 2 * s_new / s_old


def line_parameters(d, gmr, r_eq, f=60.0):
    """Per-metre L, C and characteristic impedance, and the wave speed, for spacing d and radii in metres."""
    l = MU0 / (2 * math.pi) * math.log(d / gmr)
    c = 2 * math.pi * EPS0 / math.log(d / r_eq)
    return l, c, math.sqrt(l / c), 1 / math.sqrt(l * c)


def sil(v_ll, z_c):
    return v_ll ** 2 / z_c


def two_bus(v1, v2, x, delta_deg):
    """Returns (P, Q leaving bus 1, Q arriving at bus 2) in per unit."""
    d = math.radians(delta_deg)
    return v1 * v2 * math.sin(d) / x, (v1 ** 2 - v1 * v2 * math.cos(d)) / x, (v1 * v2 * math.cos(d) - v2 ** 2) / x


def voltage_drop(r, x, p, q, v):
    return (r * p + x * q) / v


def fault_3ph(z_th_pu, v_f=1.0):
    return v_f / z_th_pu


def fault_slg(z1, z2, z0, v_f=1.0):
    return 3 * v_f / (z1 + z2 + z0)


def rocof(dp, h, s, f0=60.0):
    return dp * f0 / (2 * h * s)


def droop_df(dp, units, f0=60.0, d_load=0.0):
    """units: list of (S MW, droop R). Returns the steady frequency change in Hz for a load increase dp (MW)."""
    beta = sum(s / (r * f0) for s, r in units) + d_load
    return -dp / beta


def frequency_response(dp, h, s, r=0.05, t_gov=5.0, d_load=1000.0, f0=60.0, t_end=60.0, n=6001):
    """Swing equation with one aggregate first-order governor: returns time and frequency deviation (Hz)."""
    ek = h * s
    def f(t, y):
        df, pg = y
        return [(pg - dp - d_load * df) * f0 / (2 * ek), (-(s / (r * f0)) * df - pg) / t_gov]
    t = np.linspace(0, t_end, n)
    sol = integrate.solve_ivp(f, (0, t_end), [0.0, 0.0], t_eval=t, max_step=0.01, rtol=1e-9, atol=1e-12)
    return sol.t, sol.y[0]
