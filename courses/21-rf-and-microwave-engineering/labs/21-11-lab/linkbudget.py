"""Lab 21-11 helpers: link-budget arithmetic, sensitivity, path-loss inversion, fade and shadowing margins,
coverage probability, noise rise and satellite links. Powers in dBm, gains in dB unless a name says otherwise."""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize, special

C0 = 299_792_458.0
K_DBM_HZ = -174.0   # 10 log10(k T0 / 1 mW), T0 = 290 K


# ---------------------------------------------------------------- the budget
def noise_floor_dbm(bw_hz, nf_db):
    return K_DBM_HZ + 10 * math.log10(bw_hz) + nf_db


def sensitivity_dbm(bw_hz, nf_db, snr_db, im_db=0.0):
    return noise_floor_dbm(bw_hz, nf_db) + snr_db + im_db


def sensitivity_from_rate(rate_bps, ebn0_db, nf_db, im_db=0.0):
    """Sensitivity written with the bit rate and Eb/N0: S = -174 + 10 log R + Eb/N0 + NF + IM."""
    return K_DBM_HZ + 10 * math.log10(rate_bps) + ebn0_db + nf_db + im_db


def shannon_ebn0_min_db(spectral_eff):
    """Minimum Eb/N0 for spectral efficiency eta (b/s/Hz): (2^eta - 1)/eta."""
    return 10 * math.log10((2 ** spectral_eff - 1) / spectral_eff)


def mapl_db(eirp_dbm, rx_gain_dbi, rx_losses_db, sens_dbm, margins_db):
    """Maximum allowable path loss: what the link can lose between the antennas and still close."""
    return eirp_dbm + rx_gain_dbi - rx_losses_db - sens_dbm - margins_db


def fspl_db(f_hz, d_m):
    return 20 * math.log10(4 * math.pi * d_m * f_hz / C0)


def range_log_distance(mapl, pl_d0, n, d0=1.0):
    """Distance at which PL(d) = PL(d0) + 10 n log10(d/d0) reaches the MAPL."""
    return d0 * 10 ** ((mapl - pl_d0) / (10 * n))


# ---------------------------------------------------------------- margins
def rayleigh_margin_db(p_out):
    """Margin above the mean for Rayleigh outage p_out: P(|h|^2 < x) = 1 - exp(-x)."""
    return -10 * math.log10(-math.log(1 - p_out))


def lognormal_margin_db(sigma_db, p_out):
    return sigma_db * special.ndtri(1 - p_out)


def outage_shadow_rayleigh(margin_db, sigma_db):
    """Outage when the local mean is lognormal (sigma dB) about the margin and the instantaneous power is
    Rayleigh about the local mean (the Suzuki model)."""
    def integrand(x):
        local = margin_db + x                           # local-mean margin in dB
        return (1 - math.exp(-10 ** (-local / 10))) * math.exp(-0.5 * (x / sigma_db) ** 2) / (sigma_db * math.sqrt(2 * math.pi))
    val, _ = integrate.quad(integrand, -10 * sigma_db, 10 * sigma_db, limit=200)
    return val


def combined_margin_db(sigma_db, p_out):
    return optimize.brentq(lambda m: outage_shadow_rayleigh(m, sigma_db) - p_out, -20, 80)


def edge_to_area_coverage(p_edge, sigma_db, n):
    """Jakes's formula: the fraction of a circular cell's area above threshold, given the probability p_edge
    at its edge, lognormal shadowing sigma (dB) and path-loss exponent n."""
    a = special.ndtri(p_edge) * sigma_db / (sigma_db * math.sqrt(2))   # = margin/(sigma sqrt2)
    b = 10 * n * math.log10(math.e) / (sigma_db * math.sqrt(2))
    return 0.5 * (1 + special.erf(a)) + 0.5 * math.exp((1 + 2 * a * b) / b ** 2) * (1 - special.erf((1 + a * b) / b))


def noise_rise_db(load):
    """Uplink interference margin of a loaded CDMA/OFDMA cell: 10 log10(1/(1 - load))."""
    return -10 * math.log10(1 - load)


# ---------------------------------------------------------------- satellites and GNSS
def cn0_dbhz(eirp_dbw, path_loss_db, g_over_t_dbk, other_losses_db=0.0):
    """Carrier-to-noise-density ratio of a satellite link: EIRP - L + G/T - k (k = -228.6 dBW/K/Hz)."""
    return eirp_dbw - path_loss_db - other_losses_db + g_over_t_dbk + 228.6


def slant_range_m(alt_m, elev_deg, re_m=6_371_000.0):
    """Distance from a ground terminal to a satellite at altitude alt_m seen at elevation elev_deg."""
    e = math.radians(elev_deg)
    return math.sqrt((re_m + alt_m) ** 2 - (re_m * math.cos(e)) ** 2) - re_m * math.sin(e)


# ---------------------------------------------------------------- Monte Carlo checks for the lab
def mc_outage(margin_db, sigma_db, n=1_000_000, seed=1):
    """Fraction of samples with shadowing (lognormal) plus Rayleigh fading below the threshold."""
    rng = np.random.default_rng(seed)
    shadow = rng.normal(0.0, sigma_db, n)
    fade = 10 * np.log10(rng.exponential(1.0, n))
    return float(np.mean(margin_db + shadow + fade < 0))


def mc_area_coverage(p_edge, sigma_db, n_exp, n=1_000_000, seed=2):
    """Users uniform over a unit disc; mean margin at radius r is M_edge - 10 n log10(r); count coverage."""
    rng = np.random.default_rng(seed)
    r = np.sqrt(rng.uniform(0, 1, n))
    m_edge = sigma_db * special.ndtri(p_edge)
    margin = m_edge - 10 * n_exp * np.log10(r) + rng.normal(0.0, sigma_db, n)
    return float(np.mean(margin > 0))


def mc_repetition_gain_db(reps, snr_db=-10.0, n=200_000, seed=3):
    """BPSK symbols repeated reps times in AWGN and combined coherently: measured SNR gain in dB."""
    rng = np.random.default_rng(seed)
    a = 10 ** (snr_db / 20)
    bits = rng.choice([-1.0, 1.0], n)
    y = a * bits[:, None] + rng.normal(0.0, 1.0, (n, reps))
    comb = y.sum(axis=1) / reps
    noise = comb - a * bits
    return 10 * math.log10(a ** 2 / np.var(noise)) - snr_db
