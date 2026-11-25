"""IM-DD photonics models for chapter 24-07.

Responsivity, dBm conversions, fiber latency and loss, dispersion (spectral width, spread and an FFT
propagation of a Gaussian pulse), Mach-Zehnder and ring-modulator transfer functions, receiver sensitivity
and BER against received power for OOK and PAM4, extinction-ratio penalty, link budgets, WDM spacing,
and the shunt-feedback TIA.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import special

H = 6.62607015e-34
Q_E = 1.602176634e-19
C0 = 299792458.0
K_B = 1.380649e-23


def responsivity(lam_m: float, eta: float = 1.0) -> float:
    return eta * Q_E * lam_m / (H * C0)


def dbm_to_w(dbm: float) -> float:
    return 1e-3 * 10 ** (dbm / 10)


def w_to_dbm(w: float) -> float:
    return 10 * math.log10(w / 1e-3)


def fiber_delay_s_per_m(n_g: float = 1.468) -> float:
    return n_g / C0


def spectral_width_nm(lam_m: float, df_hz: float) -> float:
    return lam_m ** 2 * df_hz / C0 * 1e9


def dispersion_spread_ps(d_ps_nm_km: float, length_km: float, dlam_nm: float) -> float:
    return d_ps_nm_km * length_km * dlam_nm


def propagate_gaussian(t0_ps: float, d_ps_nm_km: float, length_km: float, lam_m: float, n: int = 2 ** 14,
                       span_ps: float = 2000.0):
    """Propagate an unchirped Gaussian field of 1/e intensity half-width t0 through fiber with dispersion D,
    using beta2 = -D lambda^2/(2 pi c). Returns (t, |E|^2 in, |E|^2 out) with t in ps."""
    t = np.linspace(-span_ps / 2, span_ps / 2, n, endpoint=False)
    e0 = np.exp(-t ** 2 / (2 * t0_ps ** 2))
    beta2 = -d_ps_nm_km * (lam_m * 1e9) ** 2 / (2 * math.pi * C0 * 1e-3)  # ps^2/km (c in nm/ps)
    w = 2 * math.pi * np.fft.fftfreq(n, d=t[1] - t[0])  # rad/ps
    e1 = np.fft.ifft(np.fft.fft(e0) * np.exp(0.5j * beta2 * length_km * w ** 2))
    return t, np.abs(e0) ** 2, np.abs(e1) ** 2


def rms_width(t, p):
    m = np.sum(t * p) / np.sum(p)
    return math.sqrt(np.sum((t - m) ** 2 * p) / np.sum(p))


def mzm(dphi):
    return np.cos(np.asarray(dphi, dtype=float) / 2) ** 2


def ring_transmission(lam_nm, lam0_nm: float, q_factor: float, depth: float = 0.95):
    """Lorentzian notch of full width lam0/Q and fractional depth `depth`."""
    hw = lam0_nm / q_factor / 2
    x = (np.asarray(lam_nm, dtype=float) - lam0_nm) / hw
    return 1 - depth / (1 + x * x)


def qfunc(x):
    return 0.5 * special.erfc(np.asarray(x, dtype=float) / math.sqrt(2))


def ber_ook(p_avg_w, r: float, sigma_a: float, er: float = math.inf):
    """BER of OOK at average power p_avg (mid threshold, equal Gaussian noise on both levels)."""
    eye = 2 * r * np.asarray(p_avg_w, dtype=float) * (1.0 if math.isinf(er) else (er - 1) / (er + 1))
    return qfunc(eye / (2 * sigma_a))


def ber_pam4(p_avg_w, r: float, sigma_a: float, er: float = math.inf):
    """Gray-coded PAM4: each eye a third of OOK's; SER = 1.5 Q, BER = SER/2."""
    eye = 2 * r * np.asarray(p_avg_w, dtype=float) / 3 * (1.0 if math.isinf(er) else (er - 1) / (er + 1))
    return 0.75 * qfunc(eye / (2 * sigma_a))


def er_penalty_db(er: float) -> float:
    return 10 * math.log10((er + 1) / (er - 1))


def wdm_df_hz(lam_m: float, dlam_m: float) -> float:
    return C0 * dlam_m / lam_m ** 2


def tia(r_f: float, gain: float, c_in: float):
    """Low-frequency transimpedance (ohm) and -3 dB bandwidth (Hz) of a shunt-feedback TIA."""
    return r_f * gain / (1 + gain), (1 + gain) / (2 * math.pi * r_f * c_in)


def resistor_noise_a_rthz(r: float, t_k: float = 300.0) -> float:
    return math.sqrt(4 * K_B * t_k / r)
