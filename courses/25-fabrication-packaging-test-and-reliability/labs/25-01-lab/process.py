"""Process-flow models for lab 25-01.

Deal-Grove thermal oxidation, silicon consumption, the replacement-gate trench budget,
contact degeneration, wire tiers and fab-flow arithmetic (step yield, days per mask layer,
Little's law). Units are stated in each docstring.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize

K_EV = 8.617333262e-5          # Boltzmann constant, eV/K
T50 = 0.3787478382714433       # 50% delay of an open-ended distributed RC line, in units of RC (19-05)
C_LIGHT = 2.99792458e8          # m/s
DAYS_PER_MONTH = 365.25 / 12
WEEKS_PER_YEAR = 365.25 / 7

# Deal-Grove coefficients for (111) silicon: (C1 um^2/h, E1 eV, C2 um/h, E2 eV)
DG = {"dry": (772.0, 1.23, 6.23e6, 2.0), "wet": (386.0, 0.78, 1.63e8, 2.05)}
ORIENT_100 = 1.68               # divide C2 (B/A) by this for (100) silicon


def kt(t_c: float) -> float:
    """Thermal energy in eV at a temperature in degrees Celsius."""
    return K_EV * (t_c + 273.15)


def dg_coeffs(t_c: float, ambient: str = "wet", orientation: int = 100) -> tuple[float, float, float]:
    """Return (B um^2/h, B/A um/h, A um) at t_c in Celsius."""
    c1, e1, c2, e2 = DG[ambient]
    b = c1 * math.exp(-e1 / kt(t_c))
    ba = c2 * math.exp(-e2 / kt(t_c)) / (ORIENT_100 if orientation == 100 else 1.0)
    return b, ba, b / ba


def oxide_thickness(t_h: float, t_c: float, ambient: str = "wet", xi_um: float = 0.0, orientation: int = 100) -> float:
    """Oxide thickness in um after t_h hours, starting from xi_um (closed-form Deal-Grove)."""
    b, ba, a = dg_coeffs(t_c, ambient, orientation)
    tau = (xi_um**2 + a * xi_um) / b
    return (a / 2) * (math.sqrt(1 + 4 * b * (t_h + tau) / a**2) - 1)


def oxidation_time(x_um: float, t_c: float, ambient: str = "wet", xi_um: float = 0.0, orientation: int = 100) -> float:
    """Hours to grow from xi_um to x_um."""
    b, ba, a = dg_coeffs(t_c, ambient, orientation)
    return (x_um**2 - xi_um**2 + a * (x_um - xi_um)) / b


def oxide_ode(t_h: float, t_c: float, ambient: str = "wet", xi_um: float = 0.0, orientation: int = 100) -> float:
    """Oxide thickness from integrating dx/dt = B/(A + 2x) numerically (checks the closed form)."""
    b, ba, a = dg_coeffs(t_c, ambient, orientation)
    sol = integrate.solve_ivp(lambda t, x: b / (a + 2 * x), (0, t_h), [xi_um], rtol=1e-10, atol=1e-13)
    return float(sol.y[0, -1])


def temperature_for(x_um: float, t_h: float, ambient: str = "wet", orientation: int = 100) -> float:
    """Temperature in Celsius at which x_um grows from bare silicon in t_h hours."""
    return optimize.brentq(lambda tc: oxidation_time(x_um, tc, ambient, 0.0, orientation) - t_h, 600, 1300)


def si_consumed_ratio(density_ox: float = 2.20, molar_ox: float = 60.08, a_si_nm: float = 0.5431) -> float:
    """Silicon thickness consumed per unit oxide thickness, from densities."""
    n_ox = density_ox * 6.02214076e23 / molar_ox
    n_si = 8 / (a_si_nm * 1e-7) ** 3
    return n_ox / n_si


def fill_width(trench_nm: float, t_hk_nm: float, t_wf_nm: float) -> float:
    """Fill-metal width left in a conformally lined gate trench, nm."""
    return trench_nm - 2 * (t_hk_nm + t_wf_nm)


def contact_r(rho_c_ohm_cm2: float, w_nm: float, l_nm: float) -> float:
    """Contact resistance in ohms."""
    return rho_c_ohm_cm2 / (w_nm * 1e-7 * l_nm * 1e-7)


def drive_loss(gm_s: float, rs_ohm: float) -> float:
    """Fractional drive-current loss from a source resistance (first order)."""
    return 1 - 1 / (1 + gm_s * rs_ohm)


def wire_r_per_um(w_nm: float, h_nm: float, t_barrier_nm: float, rho_uohm_cm: float) -> float:
    """Resistance per um of a wire with a non-conducting barrier on its sides and bottom."""
    area_m2 = (w_nm - 2 * t_barrier_nm) * (h_nm - t_barrier_nm) * 1e-18
    return rho_uohm_cm * 1e-8 / area_m2 * 1e-6


def rc_delay(r_per_um: float, c_per_um_f: float, length_um: float) -> float:
    """50% delay in seconds of an open-ended distributed RC wire."""
    return T50 * r_per_um * length_um * c_per_um_f * length_um


def time_of_flight(length_um: float, eps_r: float) -> float:
    """Seconds for light to travel length_um in a dielectric."""
    return length_um * 1e-6 * math.sqrt(eps_r) / C_LIGHT


def rc_equals_tof_length_um(r_per_um: float, c_per_um_f: float, eps_r: float) -> float:
    """Length at which the RC delay equals the time of flight."""
    return math.sqrt(eps_r) / C_LIGHT * 1e-6 / (T50 * r_per_um * c_per_um_f)


def step_survival(per_step: float, steps: int) -> float:
    return per_step**steps


def cycle_time_days(masks: int, dpml: float) -> float:
    return masks * dpml


def little_wip(starts_per_month: float, cycle_weeks: float) -> float:
    """Work in process (wafers) = start rate x cycle time."""
    return starts_per_month * cycle_weeks * 7 / DAYS_PER_MONTH


def simulate_wip(starts_per_day: float, mean_cycle_days: float, days: int = 3000, seed: int = 1) -> float:
    """Average WIP of a fab with Poisson starts and gamma-distributed cycle times (shape 20), after warm-up."""
    rng = np.random.default_rng(seed)
    n = rng.poisson(starts_per_day, days)
    start = np.repeat(np.arange(days), n) + rng.random(n.sum())
    finish = start + rng.gamma(20.0, mean_cycle_days / 20.0, start.size)
    t = np.arange(int(3 * mean_cycle_days), days - int(3 * mean_cycle_days))
    s, f = np.sort(start), np.sort(finish)
    wip = np.searchsorted(s, t) - np.searchsorted(f, t)
    return float(wip.mean())


def mixed_density_gain(fractions: list[float], gains: list[float]) -> float:
    """Chip density gain for area fractions shrinking by the given factors (harmonic mean)."""
    return 1 / sum(f / g for f, g in zip(fractions, gains))
