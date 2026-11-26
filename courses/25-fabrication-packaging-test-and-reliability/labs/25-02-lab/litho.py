"""Lithography models for lab 25-02.

Aerial images of line-space gratings built from the diffraction orders that pass the pupil
(scalar, thin-mask model), with on-axis or dipole illumination and defocus; photon counting;
scanner throughput and cost per pass. Lengths in nm unless stated.
"""
from __future__ import annotations

import math

import numpy as np

HC_EV_NM = 1239.84193
Q = 1.602176634e-19


def fourier_amp(m: int, f: float) -> float:
    """Fourier amplitude of order m for a grating open (transmission 1) over a fraction f of each period."""
    return f if m == 0 else math.sin(math.pi * m * f) / (math.pi * m)


def passing_orders(p: float, lam: float, na: float, s0: float = 0.0, mmax: int = 10) -> list[tuple[int, float]]:
    """Orders (m, s) with |s0 + m*lam/p| <= NA."""
    out = []
    for m in range(-mmax, mmax + 1):
        s = s0 + m * lam / p
        if abs(s) <= na + 1e-12:
            out.append((m, s))
    return out


def aerial_image(x: np.ndarray, p: float, lam: float, na: float, n: float = 1.0, f: float = 0.5,
                 poles: tuple[float, ...] = (0.0,), defocus: float = 0.0) -> np.ndarray:
    """Intensity at positions x: coherent sum over passing orders for each illumination pole,
    incoherent sum over poles. Defocus adds phase 2*pi*n*z*cos(theta)/lam to each order."""
    total = np.zeros_like(x, dtype=float)
    for s0 in poles:
        field = np.zeros_like(x, dtype=complex)
        for m, s in passing_orders(p, lam, na, s0):
            cos_t = math.sqrt(max(0.0, 1 - (s / n) ** 2))
            phase = 2 * math.pi * n * defocus * cos_t / lam
            field += fourier_amp(m, f) * np.exp(1j * (2 * math.pi * m * x / p + phase))
        total += np.abs(field) ** 2
    return total / len(poles)


def contrast(intensity: np.ndarray) -> float:
    imax, imin = float(intensity.max()), float(intensity.min())
    return 0.0 if imax + imin == 0 else (imax - imin) / (imax + imin)


def image_contrast(p: float, lam: float, na: float, n: float = 1.0, f: float = 0.5,
                   poles: tuple[float, ...] = (0.0,), defocus: float = 0.0, npts: int = 2001) -> float:
    x = np.linspace(0, 2 * p, npts)
    return contrast(aerial_image(x, p, lam, na, n, f, poles, defocus))


def dipole_for(p: float, lam: float) -> tuple[float, float]:
    """Symmetric dipole placing orders 0 and -1 (and 0 and +1) at +-lam/2p."""
    s0 = lam / (2 * p)
    return (s0, -s0)


def dof_quarter_wave(lam: float, na: float, n: float = 1.0) -> float:
    """Depth of focus (total) from the quarter-wave criterion with one order at the pupil edge."""
    return 2 * lam / (4 * n * (1 - math.sqrt(1 - (na / n) ** 2)))


def photon_energy_j(lam_nm: float) -> float:
    return HC_EV_NM / lam_nm * Q


def photons_per_nm2(dose_mj_cm2: float, lam_nm: float) -> float:
    return dose_mj_cm2 * 1e-3 / photon_energy_j(lam_nm) * 1e-14


def simulate_absorbed(dose_mj_cm2: float, lam_nm: float, area_nm2: float, absorb: float,
                      trials: int = 100_000, seed: int = 1) -> np.ndarray:
    """Absorbed photons per feature: Poisson arrivals thinned by absorption probability."""
    rng = np.random.default_rng(seed)
    incident = rng.poisson(photons_per_nm2(dose_mj_cm2, lam_nm) * area_nm2, trials)
    return rng.binomial(incident, absorb)


def throughput_wph(wph_ref: float, dose_ref: float, overhead_s: float, dose: float, power_ratio: float = 1.0) -> float:
    """Wafers per hour when exposure time scales as dose / power from a reference point."""
    t_exp_ref = 3600 / wph_ref - overhead_s
    return 3600 / (overhead_s + t_exp_ref * (dose / dose_ref) / power_ratio)


def cost_per_pass(price: float, wph: float, years: float = 5, availability: float = 0.8) -> float:
    return price / (years * 8766 * availability * wph)
