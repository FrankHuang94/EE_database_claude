"""Random processes and power spectral density: helpers for the 17-01 lab.

Everything here is built from the chapter's definitions so the notebook can compare
simulation with theory:

- autocorrelation estimates from one long record (time averages) and from an ensemble;
- PSD estimates (averaged periodograms, the Welch method of 16-05) in physical units;
- exact discrete-time models: white noise of a given density, the sampled RC-filtered
  (exponentially correlated) process as an AR(1) recursion;
- the PSD of random PAM (digital) signals, simulated and in closed form;
- bandpass noise and its in-phase and quadrature components;
- the noise spectrum of a resistor driving a series RLC circuit.

Conventions: S(f) is a two-sided density (V^2/Hz into 1 ohm); G(f) = 2 S(f) is one-sided.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, signal

K_B = 1.380649e-23  # J/K (exact, SI 2019)


# ------------------------------------------------------------------ estimates from data
def autocorr_time(x, maxlag):
    """Biased time-average estimate R[k] = (1/N) sum x[n+k] x[n], k = 0..maxlag (real x)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    return np.array([np.dot(x[k:], x[: n - k]) / n for k in range(maxlag + 1)])


def autocorr_ensemble(X, n0, maxlag):
    """Ensemble estimate E[X(n0 + k) X(n0)] over the rows of X (realizations), k = 0..maxlag."""
    X = np.asarray(X, dtype=float)
    return np.array([np.mean(X[:, n0 + k] * X[:, n0]) for k in range(maxlag + 1)])


def psd_welch(x, fs, nperseg=1024, twosided=False):
    """Averaged-periodogram PSD in V^2/Hz (Hann window, 50% overlap).

    Returns (f, density); one-sided G(f) by default, two-sided S(f) (fftshifted) if twosided.
    """
    if twosided:
        f, p = signal.welch(x, fs=fs, nperseg=nperseg, return_onesided=False, detrend=False)
        return np.fft.fftshift(f), np.fft.fftshift(p)
    return signal.welch(x, fs=fs, nperseg=nperseg, detrend=False)


# ------------------------------------------------------------------ models
def white_noise(n, s0, fs, rng):
    """Samples of white noise whose two-sided density is s0 (V^2/Hz) over |f| < fs/2: variance s0*fs."""
    return rng.standard_normal(n) * math.sqrt(s0 * fs)


def ou_samples(n, sigma2, tau_c, T, rng):
    """Exact samples, every T, of a Gaussian process with R(tau) = sigma2 exp(-|tau|/tau_c).

    The samples form the AR(1) sequence x[n] = a x[n-1] + w[n], a = exp(-T/tau_c),
    Var(w) = sigma2 (1 - a^2), started in its stationary distribution.
    """
    a = math.exp(-T / tau_c)
    w = rng.standard_normal(n) * math.sqrt(sigma2 * (1 - a * a))
    x = np.empty(n)
    x[0] = rng.standard_normal() * math.sqrt(sigma2)
    for i in range(1, n):
        x[i] = a * x[i - 1] + w[i]
    return x


def ar1_psd(a, var_w, w):
    """PSD (per rad/sample) of x[n] = a x[n-1] + w[n]: var_w / |1 - a e^{-jw}|^2."""
    w = np.asarray(w, dtype=float)
    return var_w / (1 - 2 * a * np.cos(w) + a * a)


def lorentzian_two_sided(f, sigma2, tau_c):
    """Two-sided PSD of R(tau) = sigma2 exp(-|tau|/tau_c): 2 sigma2 tau_c / (1 + (2 pi f tau_c)^2)."""
    f = np.asarray(f, dtype=float)
    return 2 * sigma2 * tau_c / (1 + (2 * math.pi * f * tau_c) ** 2)


def aliased_density(f, sigma2, tau_c, fs, terms=2000):
    """Two-sided density seen after sampling at fs: sum over m of S(f - m fs), for |f| < fs/2."""
    f = np.atleast_1d(np.asarray(f, dtype=float))
    m = np.arange(-terms, terms + 1)
    return np.array([np.sum(lorentzian_two_sided(fi - m * fs, sigma2, tau_c)) for fi in f])


# ------------------------------------------------------------------ PAM signals
def pam_waveform(symbols, sps, pulse="nrz"):
    """Baseband PAM sampled at sps samples per symbol with a rectangular (NRZ) or half-sine pulse."""
    if pulse == "nrz":
        p = np.ones(sps)
    elif pulse == "halfsine":
        p = np.sin(np.pi * (np.arange(sps) + 0.5) / sps)
    else:
        raise ValueError(pulse)
    up = np.zeros(len(symbols) * sps)
    up[::sps] = symbols
    return np.convolve(up, p)[: len(up)]


def nrz_psd(f, A2, T):
    """Two-sided PSD of polar NRZ with symbol power A2 and symbol period T: A2 T sinc^2(fT)."""
    return A2 * T * np.sinc(np.asarray(f, dtype=float) * T) ** 2


def nrz_power_fraction(k):
    """Fraction of a polar NRZ signal's power within |f| < k/T: integral of sinc^2 over |x| < k."""
    val, _ = integrate.quad(lambda x: np.sinc(x) ** 2, -k, k, limit=400, points=list(range(-int(k), int(k) + 1)))
    return val


def pam_line_power(mean, var):
    """Unipolar NRZ with symbols of mean mu and variance s2: power in the DC line over the total power."""
    return mean * mean / (mean * mean + var)


# ------------------------------------------------------------------ bandpass noise
def bandpass_noise(n, fs, fc, B, s0, rng, ntaps=801):
    """Bandpass Gaussian noise of two-sided density s0 over |f -/+ fc| < B/2 (FIR-filtered white noise)."""
    x = white_noise(n + ntaps, s0, fs, rng)
    h = signal.firwin(ntaps, [fc - B / 2, fc + B / 2], pass_zero=False, fs=fs)
    return signal.lfilter(h, 1, x)[ntaps:]


def iq_components(x, fs, fc, B, ntaps=801):
    """n_I = LPF{2 x cos(2 pi fc t)}, n_Q = LPF{-2 x sin(2 pi fc t)}, so x = n_I cos - n_Q sin."""
    t = np.arange(len(x)) / fs
    h = signal.firwin(ntaps, B / 2 * 1.2, fs=fs)
    d = (ntaps - 1) // 2
    i = signal.lfilter(h, 1, 2 * x * np.cos(2 * np.pi * fc * t))
    q = signal.lfilter(h, 1, -2 * x * np.sin(2 * np.pi * fc * t))
    return i[d:], q[d:]


# ------------------------------------------------------------------ circuits
def rlc_vc_density(f, R, L, C, T=300.0):
    """One-sided PSD (V^2/Hz) of the voltage across C when resistor R's thermal noise drives series R-L-C."""
    w = 2 * np.pi * np.asarray(f, dtype=float)
    H = 1 / (1 - w * w * L * C + 1j * w * R * C)
    return 4 * K_B * T * R * np.abs(H) ** 2


def is_valid_autocorrelation(R, tau_max, n=1 << 16):
    """Numerically test Bochner's condition: the transform of R(tau) on [-tau_max, tau_max] must be >= 0.

    Returns the minimum of the transform divided by its value at f = 0.
    """
    tau = np.linspace(-tau_max, tau_max, n, endpoint=False)
    dt = tau[1] - tau[0]
    S = np.real(np.fft.fft(np.fft.ifftshift(R(tau)))) * dt
    return S.min() / S[0]
