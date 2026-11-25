"""Signal-integrity models for chapter 24-01.

Closed forms from the chapter (first-order conductor and dielectric loss, roughness, budgets,
mismatch, via stubs, weak-coupling crosstalk, ground bounce, target impedance) plus an exact
lossy-line two-port (ABCD) with frequency-dependent R' and G', used for S21 and pulse responses.
"""
from __future__ import annotations

import math

import numpy as np

MU0 = 4e-7 * math.pi
SIGMA_CU = 5.8e7
C0 = 2.998e8
NP_TO_DB = 20 / math.log(10)
INCH = 0.0254
MIL = 25.4e-6


def nyquist(bit_rate: float, bits_per_symbol: int = 1) -> tuple[float, float, float]:
    """Symbol rate (Bd), Nyquist frequency (Hz) and unit interval (s)."""
    baud = bit_rate / bits_per_symbol
    return baud, baud / 2, 1 / baud


def skin_depth(f: float, sigma: float = SIGMA_CU) -> float:
    return 1 / math.sqrt(math.pi * f * MU0 * sigma)


def surface_resistance(f: float, sigma: float = SIGMA_CU) -> float:
    return math.sqrt(math.pi * f * MU0 / sigma)


def roughness_factor(f: float, rms: float) -> float:
    """Hammerstad-Jensen multiplier on smooth-copper loss."""
    return 1 + 2 / math.pi * math.atan(1.4 * (rms / skin_depth(f)) ** 2)


def conductor_loss_db_per_in(f: float, width: float, z0: float, rms: float = 0.0) -> float:
    """First-order R' = Rs/w model, in dB per inch."""
    alpha = surface_resistance(f) / width / (2 * z0)
    k = roughness_factor(f, rms) if rms > 0 else 1.0
    return alpha * NP_TO_DB * INCH * k


def dielectric_loss_db_per_in(f: float, eps_r: float, tan_d: float) -> float:
    return math.pi * f * math.sqrt(eps_r) * tan_d / C0 * NP_TO_DB * INCH


def reach_in(budget_db: float, loss_db_per_in: float) -> float:
    return budget_db / loss_db_per_in


def gamma(z_load: float, z_ref: float) -> float:
    return (z_load - z_ref) / (z_load + z_ref)


def return_loss_db(g: float) -> float:
    return -20 * math.log10(abs(g))


def mismatch_loss_db(g: float) -> float:
    return -10 * math.log10(1 - g * g)


def ripple_db(g: float) -> float:
    """Peak-to-peak |S21| ripple from two identical discontinuities."""
    return 20 * math.log10((1 + g * g) / (1 - g * g))


def stub_notch(length: float, eps_r: float) -> float:
    return C0 / (4 * length * math.sqrt(eps_r))


def crosstalk(cm_c: float, lm_l: float, length: float, v: float, v_a: float, t_r: float) -> dict:
    """Weak-coupling NEXT plateau, FEXT peak (linear ramp) and FEXT area."""
    td = length / v
    kb = 0.25 * (cm_c + lm_l)
    fext = 0.5 * td * (cm_c - lm_l) * v_a / t_r
    return {"td": td, "kb": kb, "next": kb * v_a, "next_duration": 2 * td,
            "l_sat": v * t_r / 2, "fext": fext, "fext_area": 0.5 * td * (cm_c - lm_l) * v_a}


def ground_bounce(l_ret: float, n: int, d_i: float, t_r: float) -> float:
    return l_ret * n * d_i / t_r


def target_impedance(v_dd: float, ripple: float, step: float) -> float:
    return v_dd * ripple / step


# ---------------------------------------------------------------- exact lossy line
def line_abcd(f: np.ndarray, length: float, z0: float, eps_r: float, tan_d: float,
              width: float, rms: float = 0.0) -> np.ndarray:
    """ABCD matrices (shape (n, 2, 2)) of a uniform line with R'(f) = K_r Rs/w and G' = w C' tan_d."""
    f = np.asarray(f, dtype=float)
    w = 2 * np.pi * f
    lp = z0 * math.sqrt(eps_r) / C0
    cp = math.sqrt(eps_r) / (C0 * z0)
    rs = np.sqrt(np.pi * f * MU0 / SIGMA_CU)
    k = 1 + 2 / np.pi * np.arctan(1.4 * (rms * np.sqrt(np.pi * f * MU0 * SIGMA_CU)) ** 2) if rms > 0 else 1.0
    rp = k * rs / width
    gp = w * cp * tan_d
    zser = rp + 1j * w * lp
    ysh = gp + 1j * w * cp
    gam = np.sqrt(zser * ysh)
    zc = np.sqrt(zser / ysh)
    gl = gam * length
    m = np.empty((f.size, 2, 2), dtype=complex)
    m[:, 0, 0] = np.cosh(gl)
    m[:, 0, 1] = zc * np.sinh(gl)
    m[:, 1, 0] = np.sinh(gl) / zc
    m[:, 1, 1] = np.cosh(gl)
    return m


def stub_abcd(f: np.ndarray, length: float, z0: float, eps_r: float) -> np.ndarray:
    """Shunt admittance of a lossless open stub, as an ABCD matrix."""
    beta = 2 * np.pi * np.asarray(f, dtype=float) * math.sqrt(eps_r) / C0
    y = 1j * np.tan(beta * length) / z0
    m = np.zeros((np.size(f), 2, 2), dtype=complex)
    m[:, 0, 0] = 1
    m[:, 1, 0] = y
    m[:, 1, 1] = 1
    return m


def s21(abcd: np.ndarray, z_ref: float = 50.0) -> np.ndarray:
    a, b, c, d = abcd[:, 0, 0], abcd[:, 0, 1], abcd[:, 1, 0], abcd[:, 1, 1]
    return 2 / (a + b / z_ref + c * z_ref + d)


def pulse_response(h_of_f, ui: float, n_fft: int = 2 ** 14, fs: float = 2e12):
    """Response to a one-UI rectangular pulse: inverse FFT of H(f) times the pulse spectrum."""
    f = np.fft.rfftfreq(n_fft, 1 / fs)
    f[0] = 1e3
    pulse = ui * np.sinc(f * ui) * np.exp(-1j * np.pi * f * ui)
    y = np.fft.irfft(h_of_f(f) * pulse, n=n_fft) * fs
    t = np.arange(n_fft) / fs
    return t, y
