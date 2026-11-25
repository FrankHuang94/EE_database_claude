"""Silicon-photonics and transceiver models for chapter 24-08.

Cutoff wavelengths, waveguide critical angles and single-mode conditions, Gaussian mode coupling
(closed form and a numerical overlap integral), grating-coupler phase matching and spectrum, transmitter
budgets, the driver-bond-modulator RLC response, retimed against linear error accumulation, and yield.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import special

HC_EV_NM = 6.62607015e-34 * 299792458.0 / 1.602176634e-19 * 1e9  # 1239.84 nm·eV


def cutoff_nm(eg_ev: float) -> float:
    return HC_EV_NM / eg_ev


def critical_angle_deg(n1: float, n2: float) -> float:
    return math.degrees(math.asin(n2 / n1))


def slab_single_mode_um(lam_um: float, n1: float, n2: float) -> float:
    return lam_um / (2 * math.sqrt(n1 ** 2 - n2 ** 2))


def fiber_single_mode_core_um(lam_um: float, n1: float, n2: float) -> float:
    return 2.405 * lam_um / (math.pi * math.sqrt(n1 ** 2 - n2 ** 2))


def coupling(w1: float, w2: float, d: float = 0.0) -> float:
    """Power coupling between circular Gaussian modes of 1/e field radii w1, w2 offset laterally by d."""
    return (2 * w1 * w2 / (w1 ** 2 + w2 ** 2)) ** 2 * math.exp(-2 * d ** 2 / (w1 ** 2 + w2 ** 2))


def overlap_numeric(w1: float, w2: float, d: float = 0.0, n: int = 801, span: float = 6.0) -> float:
    """The same coupling by direct numerical overlap of the fields on a square grid."""
    half = span * max(w1, w2) + abs(d)
    x = np.linspace(-half, half, n)
    xx, yy = np.meshgrid(x, x)
    e1 = np.exp(-(xx ** 2 + yy ** 2) / w1 ** 2)
    e2 = np.exp(-((xx - d) ** 2 + yy ** 2) / w2 ** 2)
    num = np.sum(e1 * e2) ** 2
    return float(num / (np.sum(e1 ** 2) * np.sum(e2 ** 2)))


def grating_period_nm(lam_nm: float, n_eff: float, theta_deg: float) -> float:
    return lam_nm / (n_eff - math.sin(math.radians(theta_deg)))


def grating_angle_deg(lam_nm, period_nm: float, n_eff: float):
    return np.degrees(np.arcsin(n_eff - np.asarray(lam_nm, dtype=float) / period_nm))


def divergence_deg(lam_um: float, w_um: float) -> float:
    return math.degrees(lam_um / (math.pi * w_um))


def grating_spectrum(lam_nm, lam0_nm: float, n_eff: float, theta_deg: float, w_um: float):
    """Tilt-limited coupling against wavelength for a grating designed for lam0 at theta into a fiber of radius w."""
    period = grating_period_nm(lam0_nm, n_eff, theta_deg)
    dth = grating_angle_deg(lam_nm, period, n_eff) - theta_deg
    return np.exp(-(dth / divergence_deg(lam0_nm / 1e3, w_um)) ** 2)


def laser_dbm(p_rx_dbm: float, margin_db: float, losses_db) -> float:
    return p_rx_dbm + margin_db + sum(losses_db)


def rlc(r: float, l: float, c: float):
    """Driver R, bond L, lumped modulator C: (f0, zeta, f3dB, peak gain, peak frequency)."""
    w0 = 1 / math.sqrt(l * c)
    z = r / 2 * math.sqrt(c / l)
    f0 = w0 / (2 * math.pi)
    a = 1 - 2 * z * z
    f3 = f0 * math.sqrt(a + math.sqrt(a * a + 1))
    if z < 1 / math.sqrt(2):
        return f0, z, f3, 1 / (2 * z * math.sqrt(1 - z * z)), f0 * math.sqrt(a)
    return f0, z, f3, 1.0, 0.0


def rlc_mag(f, r: float, l: float, c: float):
    s = 2j * math.pi * np.asarray(f, dtype=float)
    return np.abs(1 / (l * c * s ** 2 + r * c * s + 1))


def qfunc(x):
    return 0.5 * special.erfc(np.asarray(x, dtype=float) / math.sqrt(2))


def linear_q(qs) -> float:
    return 1 / math.sqrt(sum(1 / q ** 2 for q in qs))


def retimed_ber(qs) -> float:
    return float(sum(qfunc(q) for q in qs))


def yield_cost(y_lane: float, lanes: int, c_pic: float, c_asm: float):
    y = y_lane ** lanes
    return y, (c_pic + c_asm) / y, c_pic / y + c_asm
