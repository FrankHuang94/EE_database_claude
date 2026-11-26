"""Quantitative checks behind the analog, RF, power, packaging and embedded question banks
(chapter 28-05).

Units: watts, hertz, seconds and kelvin unless a name says otherwise; SNR, SNDR and
figures of merit in dB; currents in µA and capacities in mAh for battery life.
"""
from __future__ import annotations

import math

from scipy import stats

K_B = 1.380649e-23  # J/K
HOURS_PER_YEAR = 8766.0

# --- Data converters and clocks --------------------------------------------------------


def enob(sndr_db):
    """Effective number of bits from SNDR in dB."""
    return (sndr_db - 1.76) / 6.02


def fom_walden(power_w, fs_hz, sndr_db):
    """Walden figure of merit in J per conversion step."""
    return power_w / (fs_hz * 2 ** enob(sndr_db))


def fom_schreier(sndr_db, bw_hz, power_w):
    """Schreier figure of merit in dB (bandwidth = fs/2 for a Nyquist converter)."""
    return sndr_db + 10 * math.log10(bw_hz / power_w)


def thermal_floor_w(snr_db, fs_hz, temp_k=300.0):
    """Power on the survey's 8kT*SNR line at sample rate fs."""
    return 8 * K_B * temp_k * 10 ** (snr_db / 10) * fs_hz


def schreier_ceiling(temp_k=300.0):
    """Ceiling on the Schreier figure set by the 8kT*SNR line: 10 log10(1/16kT)."""
    return 10 * math.log10(1 / (16 * K_B * temp_k))


def snr_jitter(f_in_hz, sigma_s):
    """Jitter-limited SNR in dB for a full-scale sine."""
    return -20 * math.log10(2 * math.pi * f_in_hz * sigma_s)


def jitter_for_snr(snr_db, f_in_hz):
    """RMS jitter that alone limits SNR to snr_db at f_in."""
    return 10 ** (-snr_db / 20) / (2 * math.pi * f_in_hz)


def snr_combine(*snrs_db):
    """Total SNR of independent noise sources, each given as an SNR in dB."""
    return -10 * math.log10(sum(10 ** (-s / 10) for s in snrs_db))


# --- Power amplifiers ------------------------------------------------------------------


def eff_class_b(backoff_db):
    """Ideal class-B drain efficiency at an output back-off in dB."""
    return math.pi / 4 * 10 ** (-backoff_db / 20)


def eff_doherty(backoff_db):
    """Ideal symmetric Doherty efficiency: (pi/2)a below half amplitude a,
    (pi/2)a^2/(3a - 1) above it."""
    a = 10 ** (-backoff_db / 20)
    if a <= 0.5:
        return math.pi / 2 * a
    return math.pi / 2 * a * a / (3 * a - 1)


def evm_db(evm_fraction):
    """EVM as a fraction converted to dB."""
    return 20 * math.log10(evm_fraction)


# --- Power conversion --------------------------------------------------------------------


def loss_w(p_out_w, eta):
    """Loss of a converter delivering p_out at efficiency eta."""
    return p_out_w * (1 / eta - 1)


def chain(p_out_w, etas):
    """Efficiencies listed from source to load. Returns (chain efficiency, input power,
    losses per stage in the same order)."""
    p = p_out_w
    losses = []
    for eta in reversed(etas):
        p_in = p / eta
        losses.append(p_in - p)
        p = p_in
    return p_out_w / p, p, list(reversed(losses))


# --- Packaging -----------------------------------------------------------------------------


def density_per_mm2(pitch_um):
    """Connections per mm^2 for an area array at pitch_um."""
    return 1e6 / pitch_um ** 2


def package_yield(die, stack, n_stacks, assembly):
    """End-to-end yield: die survival x stack survival^n x assembly."""
    return die * stack ** n_stacks * assembly


def junction_temp(t_ref_c, power_w, theta_k_per_w):
    """Junction temperature from a reference temperature and a thermal resistance."""
    return t_ref_c + power_w * theta_k_per_w


# --- Embedded --------------------------------------------------------------------------------


def avg_current_ua(sleep_ua, events):
    """events: [(active current in µA above sleep, active time s, period s), ...]."""
    return sleep_ua + sum(i * t / period for i, t, period in events)


def battery_years(capacity_mah, i_avg_ua):
    """Battery life in years (8,766 h each) before derating."""
    return capacity_mah / (i_avg_ua / 1000) / HOURS_PER_YEAR


# --- Typical and guaranteed ---------------------------------------------------------------


def cpk_upper(usl, mean, sigma):
    """One-sided capability index against an upper limit."""
    return (usl - mean) / (3 * sigma)


def ppm_beyond(cpk):
    """Parts per million beyond a one-sided limit for a normal parameter."""
    return stats.norm.sf(3 * cpk) * 1e6


def sigma_upper(s, n, confidence=0.95):
    """Upper confidence bound on sigma from n parts with sample std s."""
    return s * math.sqrt((n - 1) / stats.chi2.ppf(1 - confidence, n - 1))
