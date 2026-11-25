"""Lab 22-09 helpers: cell fundamentals, the equivalent-circuit (OCV + R0 + R1||C1) model, usable capacity, CC/CV
charging, charger losses, fuel-gauge errors, aging and battery life. SI units unless a name says otherwise
(capacities in coulombs, times in seconds)."""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate

F = 96485.33212          # C/mol
K_B_EV = 8.617333262e-5  # eV/K


# ---------------------------------------------------------------- fundamentals
def cell_voltage(delta_g_j_per_mol, n=1):
    """E = −ΔG/(nF)."""
    return -delta_g_j_per_mol / (n * F)


def theoretical_capacity_mah_per_g(molar_mass_g, n=1):
    """q = nF/(3.6 M) in mAh/g."""
    return n * F / (3.6 * molar_mass_g)


# ---------------------------------------------------------------- OCV curves
def ocv_linear(z, v0=3.30, k=0.90):
    """The chapter's teaching cell: a straight line from 3.30 V (empty) to 4.20 V (full)."""
    return v0 + k * np.asarray(z)


def ocv_curved(z):
    """An illustrative S-shaped OCV (not a real cell): steep near empty and full, flatter in the middle;
    3.00 V at z = 0 and 4.20 V at z = 1."""
    z = np.asarray(z)
    return 3.0 + 0.6 * z + 0.35 * (1 - np.exp(-12 * z)) + 0.25 * z ** 6


# ---------------------------------------------------------------- equivalent circuit
def step_voltage(t, ocv, i, r0, r1, c1):
    """Terminal voltage for a constant discharge current i applied at t = 0 from rest (SOC change neglected)."""
    return ocv - i * r0 - i * r1 * (1 - np.exp(-np.asarray(t) / (r1 * c1)))


def simulate_cell(i_of_t, t_end, q, z0, ocv=ocv_linear, r0=0.20, r1=0.10, c1=200.0, n=2001):
    """Integrate the model for a discharge current i(t) (negative = charge). Returns t, z, v1, terminal voltage."""
    def f(t, y):
        i = i_of_t(t)
        return [-i / q, i / c1 - y[1] / (r1 * c1)]
    t = np.linspace(0, t_end, n)
    sol = integrate.solve_ivp(f, (0, t_end), [z0, 0.0], t_eval=t, rtol=1e-9, atol=1e-12, max_step=t_end / 500)
    z, v1 = sol.y
    i = np.array([i_of_t(x) for x in sol.t])
    return sol.t, z, v1, ocv(z) - i * r0 - v1


def max_current(ocv, v_cut, r):
    return (ocv - v_cut) / r


def usable_fraction_linear(i, r, k=0.90):
    """Usable fraction to a cutoff equal to the empty OCV, for a straight-line OCV of slope k."""
    return 1 - i * r / k


# ---------------------------------------------------------------- charging
def cccv_linear(q, i_cc, i_term, r, v_max=4.20, v0=3.30, k=0.90, z0=0.0):
    """Closed-form CC/CV for a straight-line OCV and resistive cell.
    Returns (z at end of CC, CC time s, CV time constant s, CV time s, z at termination)."""
    z_cv = (v_max - i_cc * r - v0) / k
    t_cc = (z_cv - z0) * q / i_cc
    tau = r * q / k
    t_cv = tau * math.log(i_cc / i_term)
    return z_cv, t_cc, tau, t_cv, z_cv + (i_cc - i_term) * tau / q


def simulate_cccv(q, i_cc, i_term, r, v_max=4.20, ocv=ocv_linear, z0=0.0, dt=0.5, t_max=20000.0):
    """Time-step a resistive cell under a CC/CV charger: i = min(I_cc, (V_max − OCV)/R). Returns (t_cc, t_end, z_end)."""
    z, t, t_cc = z0, 0.0, None
    while t < t_max:
        i = min(i_cc, (v_max - float(ocv(z))) / r)
        if t_cc is None and i < i_cc:
            t_cc = t
        if i <= i_term:
            return t_cc, t, z
        # midpoint step
        zm = z + 0.5 * dt * i / q
        im = min(i_cc, (v_max - float(ocv(zm))) / r)
        z += dt * im / q
        t += dt
    raise RuntimeError("charge did not terminate")


def simulate_cccv_rc(q, i_cc, i_term, r0=0.20, r1=0.10, c1=200.0, v_max=4.20, ocv=ocv_linear, z0=0.0, dt=0.05,
                     t_max=20000.0):
    """CC/CV with the RC branch: the charger holds the terminal at v_max, i = min(I_cc, (V_max − OCV − v1)/R0).
    Fixed-step Euler (dt small against tau1). Returns (t_cc, t_end, z_end)."""
    z, v1, t, t_cc = z0, 0.0, 0.0, None
    while t < t_max:
        i = min(i_cc, (v_max - float(ocv(z)) - v1) / r0)
        if t_cc is None and i < i_cc:
            t_cc = t
        if i <= i_term:
            return t_cc, t, z
        z += dt * i / q
        v1 += dt * (i / c1 - v1 / (r1 * c1))
        t += dt
    raise RuntimeError("charge did not terminate")


def linear_charger(v_in, v_bat, i):
    """Returns (dissipation W, efficiency)."""
    return (v_in - v_bat) * i, v_bat / v_in


def converter_loss(p_out, eta):
    return p_out / eta - p_out


# ---------------------------------------------------------------- gauging
def voltage_gauge_error(i, r, docv_dz):
    """SOC error from reading a loaded terminal voltage as OCV."""
    return i * r / docv_dz


def coulomb_offset_error(i_os, t):
    return i_os * t


def learned_capacity(dq, z1, z2):
    return dq / (z1 - z2)


# ---------------------------------------------------------------- aging and life
def sqrt_aging(loss_ref, t_ref, t):
    return loss_ref * math.sqrt(t / t_ref)


def arrhenius_factor(ea_ev, t1_c, t2_c):
    return math.exp(ea_ev / K_B_EV * (1 / (t1_c + 273.15) - 1 / (t2_c + 273.15)))


def battery_life_hours(q_mah, i_avg_ma, f_age=1.0, f_temp=1.0, f_cut=1.0):
    return q_mah * f_age * f_temp * f_cut / i_avg_ma
