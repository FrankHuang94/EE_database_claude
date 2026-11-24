"""Lab 21-12 helpers: 3GPP peak-rate arithmetic, modem memory and compute sizing, Wi-Fi rates, and the three
ranging methods (UWB two-way ranging, Bluetooth phase-based ranging, dual-frequency GNSS), plus satellite Doppler."""
from __future__ import annotations

import math

import numpy as np

C0 = 299_792_458.0
GM = 3.986004418e14
R_E = 6_371_000.0


# ---------------------------------------------------------------- capability arithmetic
def nr_rate_mbps(layers, qm, n_prb, mu, oh, f=1.0, rmax=948 / 1024):
    """TS 38.306 approximate maximum data rate of one carrier, Mb/s."""
    ts = 1e-3 / (14 * 2 ** mu)
    return 1e-6 * layers * qm * f * rmax * n_prb * 12 / ts * (1 - oh)


def l2_buffer_bytes(dl_bps, ul_bps, rlc_rtt_s):
    return (dl_bps + ul_bps) * rlc_rtt_s / 8


def soft_buffer_bytes(rate_bps, slot_s, processes, llr_bits, r_lbrm=2 / 3):
    return processes * rate_bps * slot_s / r_lbrm * llr_bits / 8


def fft_cmults(n):
    return n / 2 * math.log2(n)


def wifi_rate_bps(n_sd, bits, code_rate, gi_s=0.8e-6, streams=1):
    return streams * n_sd * bits * code_rate / (12.8e-6 + gi_s)


# ---------------------------------------------------------------- UWB two-way ranging
def twr_simulate(tau, t_reply1, t_reply2, e_a, e_b):
    """Single- and double-sided two-way ranging with clock errors e_a, e_b (fractional). Device A starts; B replies
    after t_reply1 of true time; A replies again after t_reply2. Each device measures intervals with its own clock.
    Returns (single-sided estimate, double-sided estimate) of the flight time."""
    t_round1 = 2 * tau + t_reply1            # true durations
    t_round2 = 2 * tau + t_reply2
    r1, d1 = t_round1 * (1 + e_a), t_reply1 * (1 + e_b)   # as measured
    r2, d2 = t_round2 * (1 + e_b), t_reply2 * (1 + e_a)
    single = (r1 - d1) / 2
    double = (r1 * r2 - d1 * d2) / (r1 + r2 + d1 + d2)
    return single, double


# ---------------------------------------------------------------- Bluetooth phase-based ranging
def pbr_phases(freqs, paths, rng=None, noise_rad=0.0):
    """Round-trip phase of each tone for multipath 'paths' = [(distance, amplitude), ...]."""
    h = np.zeros(len(freqs), complex)
    for d, a in paths:
        h += a * np.exp(-1j * 4 * np.pi * np.asarray(freqs) * d / C0)
    phase = np.angle(h)
    if rng is not None and noise_rad:
        phase = phase + rng.normal(0, noise_rad, len(freqs))
    return phase


def pbr_slope_distance(freqs, phase):
    """Distance from the least-squares slope of the unwrapped phase against frequency."""
    slope = np.polyfit(np.asarray(freqs), np.unwrap(phase), 1)[0]
    return -slope * C0 / (4 * np.pi)


def pbr_ifft_distance(freqs, h, oversample=16):
    """Distance of the strongest peak of the inverse FFT of the channel samples (time-of-flight profile)."""
    n = len(freqs) * oversample
    df = freqs[1] - freqs[0]
    prof = np.abs(np.fft.ifft(h, n))
    k = int(np.argmax(prof))
    return k / (n * df) * C0 / 2


# ---------------------------------------------------------------- GNSS and satellites
def iono_free_coeffs(f1, f2):
    a = f1 ** 2 / (f1 ** 2 - f2 ** 2)
    return a, 1 - a


def leo_doppler_hz(f, h, elev_deg):
    """Doppler for a user directly under the ground track, satellite at elevation elev_deg (approaching)."""
    v = math.sqrt(GM / (R_E + h))
    e = math.radians(elev_deg)
    # angle between the velocity (horizontal at the satellite) and the line of sight
    nadir = math.asin(R_E * math.cos(e) / (R_E + h))
    return f * v * math.sin(nadir) / C0
