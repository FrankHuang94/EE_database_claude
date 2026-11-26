"""Unit-process models for lab 25-03.

CVD regimes, ALD and plating arithmetic, etch with wafer non-uniformity, a Preston-law CMP
step-height model, implant profiles with a finite-difference diffusion solver (zero-flux surface),
and a gauge-noise simulation. Units are stated per function.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize

K_EV = 8.617333262e-5
Q = 1.602176634e-19
FARADAY = 96485.33212


def arrhenius(k_ref: float, t_ref_c: float, ea_ev: float, t_c: float) -> float:
    """Rate constant at t_c given its value at t_ref_c and an activation energy."""
    return k_ref * math.exp(-(ea_ev / K_EV) * (1 / (t_c + 273.15) - 1 / (t_ref_c + 273.15)))


def cvd_rate_nm_min(ks: float, hg: float, cg: float, n_film: float) -> float:
    """Growth rate for supply and reaction in series (cm/s constants, cm^-3 concentrations)."""
    return ks * hg / (ks + hg) * cg / n_film * 1e7 * 60


def crossover_temperature(k_ref: float, t_ref_c: float, ea_ev: float, hg: float) -> float:
    """Temperature (C) at which ks equals hg."""
    return optimize.brentq(lambda t: arrhenius(k_ref, t_ref_c, ea_ev, t) - hg, 200, 2000)


def ald_cycles(thickness_nm: float, gpc_nm: float) -> int:
    return math.ceil(thickness_nm / gpc_nm - 1e-12)


def plating_rate_nm_s(j_a_cm2: float, molar_mass: float = 63.546, density: float = 8.96, n: int = 2) -> float:
    return j_a_cm2 * molar_mass / (n * FARADAY * density) * 1e7


def stop_layer_loss(thick_nm: float, rate: float, nonunif: float, overetch: float, selectivity: float) -> float:
    """Worst-case stop-layer loss (nm) where the film clears first."""
    t_total = (1 + overetch) * thick_nm / rate
    fast = rate * (1 + nonunif)
    return (t_total - thick_nm / fast) * fast / selectivity


def wafer_map_clear_times(thick_nm: float, rate: float, nonunif: float, n: int = 201) -> np.ndarray:
    """Clearing times on a radial rate profile varying linearly by +-nonunif from centre to edge."""
    r = np.linspace(-1, 1, n)
    x, y = np.meshgrid(r, r)
    rho = np.sqrt(x**2 + y**2)
    rates = rate * (1 + nonunif * (2 * np.clip(rho, 0, 1) - 1))
    return np.where(rho <= 1, thick_nm / rates, np.nan)


def preston_rate_nm_min(kp: float, pressure_pa: float, velocity: float) -> float:
    return kp * pressure_pa * velocity * 1e9 * 60


def cmp_step_time_min(step_nm: float, blanket_rate: float, density: float) -> float:
    """Time to remove a step if only raised features (area fraction density) contact the pad."""
    return step_nm / (blanket_rate / density)


def gaussian_profile(x_nm: np.ndarray, dose: float, rp: float, drp: float) -> np.ndarray:
    return dose / (math.sqrt(2 * math.pi) * drp * 1e-7) * np.exp(-(x_nm - rp) ** 2 / (2 * drp**2))


def junction_depth(dose: float, rp: float, drp: float, nb: float) -> float:
    np_ = dose / (math.sqrt(2 * math.pi) * drp * 1e-7)
    return rp + drp * math.sqrt(2 * math.log(np_ / nb))


def boron_d(t_c: float) -> float:
    return 0.76 * math.exp(-3.46 / (K_EV * (t_c + 273.15)))


def diffuse_fd(profile: np.ndarray, dx_nm: float, d_cm2_s: float, t_s: float) -> np.ndarray:
    """Explicit finite-difference diffusion with a zero-flux surface at index 0 and a far deep boundary."""
    d_nm2_s = d_cm2_s * 1e14
    dt = 0.4 * dx_nm**2 / d_nm2_s
    steps = max(1, int(math.ceil(t_s / dt)))
    dt = t_s / steps
    a = d_nm2_s * dt / dx_nm**2
    n = profile.copy()
    for _ in range(steps):
        lap = np.empty_like(n)
        lap[1:-1] = n[2:] - 2 * n[1:-1] + n[:-2]
        lap[0] = 2 * (n[1] - n[0])          # mirror: zero flux at the surface
        lap[-1] = n[-2] - n[-1]
        n = n + a * lap
    return n


def image_solution(x_nm: np.ndarray, dose: float, rp: float, drp: float, d_cm2_s: float, t_s: float) -> np.ndarray:
    """Gaussian broadened by 2Dt plus its mirror image about the surface (zero flux)."""
    s = math.sqrt(drp**2 + 2 * d_cm2_s * t_s * 1e14)
    return gaussian_profile(x_nm, dose, rp, s) + gaussian_profile(x_nm, dose, -rp, s)


def apparent_cpk(mean: float, lsl: float, usl: float, sigma_p: float, sigma_m: float) -> float:
    s = math.sqrt(sigma_p**2 + sigma_m**2)
    return min(usl - mean, mean - lsl) / (3 * s)


def simulate_measurements(mean: float, sigma_p: float, sigma_m: float, n: int = 10_000, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return mean + rng.normal(0, sigma_p, n) + rng.normal(0, sigma_m, n)
