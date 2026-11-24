"""Lab 21-08 helpers: frequency planning, image filtering, spurious responses, I/Q imbalance, direct RF sampling.

Frequencies in hertz unless a name says otherwise.
"""
from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------- superheterodyne frequency planning
def image(f_rf, f_if, high_side=True):
    """Image frequency for a given RF and IF: 2 f_LO - f_RF."""
    f_lo = f_rf + f_if if high_side else f_rf - f_if
    return 2 * f_lo - f_rf, f_lo


def butterworth_bp_atten_db(f, f0, bw, order):
    """Attenuation of an order-n Butterworth band-pass (3 dB bandwidth bw centred on f0) at frequency f, using the
    low-pass to band-pass mapping x = (f/f0 - f0/f) f0 / bw."""
    x = (f / f0 - f0 / f) * f0 / bw
    return 10 * math.log10(1 + x ** (2 * order))


def order_for_rejection(f_img, f0, bw, rejection_db, nmax=20):
    for n in range(1, nmax + 1):
        if butterworth_bp_atten_db(f_img, f0, bw, n) >= rejection_db:
            return n
    return None


def spurs(f_lo, f_if, if_bw, rf_lo, rf_hi, mmax=5, nmax=5):
    """Input frequencies f_rf in [rf_lo, rf_hi] for which |m f_LO - n f_RF| lands in the IF band (m, n >= 0),
    other than the wanted (m, n) = (1, 1) and the image. Returns a list of (m, n, f_rf)."""
    out = []
    for m in range(0, mmax + 1):
        for n in range(1, nmax + 1):
            for sgn in (+1, -1):
                # m f_LO - n f_RF = sgn f_IF  ->  f_RF = (m f_LO - sgn f_IF) / n
                f = (m * f_lo - sgn * f_if) / n
                if rf_lo <= f <= rf_hi and not (m == 1 and n == 1):
                    out.append((m, n, f))
    return sorted(set(out), key=lambda t: t[2])


# ---------------------------------------------------------------- I/Q imbalance (zero-IF self-image)
def irr_db(eps, theta_deg):
    a = 1 + eps
    th = math.radians(theta_deg)
    return 10 * math.log10((1 + 2 * a * math.cos(th) + a * a) / (1 - 2 * a * math.cos(th) + a * a))


# ---------------------------------------------------------------- direct RF sampling
def nyquist_alias(f, fs):
    """Frequency (0..fs/2) at which an input at f appears after sampling at fs, and its Nyquist zone (1-based)."""
    zone = int(f // (fs / 2)) + 1
    r = f % fs
    return (r if r <= fs / 2 else fs - r), zone


def jitter_snr_db(f_in, sigma_t):
    """SNR limit set by rms aperture/clock jitter for a full-scale sinusoid at f_in."""
    return -20 * math.log10(2 * math.pi * f_in * sigma_t)


def nsd_dbfs_hz(snr_db, fs):
    """Noise spectral density in dBFS/Hz for an ADC with full-band SNR snr_db (noise spread over fs/2)."""
    return -snr_db - 10 * math.log10(fs / 2)


def processing_gain_db(fs, bw):
    return 10 * math.log10(fs / (2 * bw))


def ideal_snr_db(bits):
    return 6.02 * bits + 1.76


def ddc_snr(seed=2108, fs=3.0e9, f_in=2.45e9, bw=20e6, snr_adc_db=60.0, n=1 << 16, decim=64):
    """Sample a tone plus white ADC noise (full-band SNR snr_adc_db), mix to DC with an NCO, low-pass with a
    windowed-sinc FIR of passband bw/2 and decimate; return (alias frequency, full-band SNR, in-band SNR)."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / fs
    a = 1.0
    sig = a * np.cos(2 * np.pi * f_in * t)
    p_sig = a * a / 2
    noise = rng.normal(0, math.sqrt(p_sig / 10 ** (snr_adc_db / 10)), n)
    x = sig + noise
    f_alias, _ = nyquist_alias(f_in, fs)
    # NCO to the alias (the sampled tone appears at f_alias, possibly spectrally inverted)
    lo = np.exp(-2j * np.pi * f_alias * t)
    z = x * lo
    taps = 1023
    k = np.arange(taps) - (taps - 1) / 2
    fc = (bw / 2) / fs
    h = 2 * fc * np.sinc(2 * fc * k) * np.blackman(taps)
    y = np.convolve(z, h, mode="valid")[::decim]
    # the tone lands at DC with amplitude a/2; noise is what remains after removing the mean
    tone = np.mean(y)
    resid = y - tone
    snr_in = 10 * math.log10(abs(tone) ** 2 / np.mean(np.abs(resid) ** 2))
    return f_alias, snr_adc_db, snr_in


# ---------------------------------------------------------------- simulations
def iq_mismatch(x, eps, theta_deg):
    """Receive I/Q imbalance: the Q branch has gain (1 + eps) and phase error theta, so y = mu x + nu conj(x)."""
    a = 1 + eps
    th = math.radians(theta_deg)
    mu = (1 + a * np.exp(-1j * th)) / 2
    nu = (1 - a * np.exp(1j * th)) / 2
    return mu * x + nu * np.conj(x), mu, nu


def ofdm_iq_evm_db(eps, theta_deg, n_fft=256, n_used=200, n_sym=200, seed=2108):
    """EVM (dB) of 16-QAM OFDM, with subcarriers symmetric about DC, after I/Q imbalance and ideal gain correction."""
    rng = np.random.default_rng(seed)
    lv = np.array([-3, -1, 1, 3])
    k = np.r_[1:n_used // 2 + 1, n_fft - n_used // 2:n_fft]
    err = ref = 0.0
    for _ in range(n_sym):
        X = np.zeros(n_fft, complex)
        X[k] = rng.choice(lv, k.size) + 1j * rng.choice(lv, k.size)
        y, mu, _ = iq_mismatch(np.fft.ifft(X), eps, theta_deg)
        Y = np.fft.fft(y) / mu
        err += np.sum(np.abs(Y[k] - X[k]) ** 2)
        ref += np.sum(np.abs(X[k]) ** 2)
    return 10 * math.log10(err / ref)


def jitter_snr_sim(f_in, fs, sigma_t, n=1 << 16, seed=2108):
    """Sample a unit sinusoid at instants with Gaussian timing error; SNR (dB) from a least-squares sine fit."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / fs
    x = np.sin(2 * np.pi * f_in * (t + rng.normal(0, sigma_t, n)))
    A = np.column_stack([np.sin(2 * np.pi * f_in * t), np.cos(2 * np.pi * f_in * t)])
    c, *_ = np.linalg.lstsq(A, x, rcond=None)
    e = x - A @ c
    return 10 * math.log10(np.sum((A @ c) ** 2) / np.sum(e ** 2))


def complex_filter_db(f, f_if, f_p, order=1):
    """Magnitude (dB) of an order-n Butterworth low-pass of corner f_p shifted to +f_if, at frequency f."""
    x = (f - f_if) / f_p
    return -10 * math.log10(1 + x ** (2 * order))
