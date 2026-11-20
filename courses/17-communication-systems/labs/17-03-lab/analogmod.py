"""Analog modulation in discrete time: helpers for the 17-03 lab.

- the Hilbert transform (FFT-based) and single-sideband generation by the phasing method;
- coherent demodulation with phase and frequency errors;
- AM with an ideal envelope detector;
- FM and PM in complex baseband, the quadrature (arctangent-difference) discriminator, de-emphasis;
- tone-FM spectra from Bessel functions, Carson's rule and power fractions;
- output-SNR measurement for any scheme by projecting the output onto the known message.

Conventions: signals are sampled at fs; m(t) is the message with |m| <= 1; N0 is the one-sided noise density.
Bandpass simulations use complex baseband z(t), with s(t) = Re{z(t) e^{j 2 pi fc t}}; a bandpass noise of
one-sided density N0 is complex baseband noise with N0 in each of I and Q (17-01 section 3.9) when z is
normalized so that the bandpass power is |z|^2 / 2.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal
from scipy.special import jv


# ------------------------------------------------------------------ Hilbert transform and SSB
def hilbert(x):
    """Hilbert transform by FFT: multiply the spectrum by -j sgn(f)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    X = np.fft.fft(x)
    f = np.fft.fftfreq(n)
    H = -1j * np.sign(f)
    return np.real(np.fft.ifft(X * H))


def ssb(m, fc, fs, upper=True, amp=1.0):
    """Phasing-method SSB: (A/2)[m cos(wc t) -/+ m_hat sin(wc t)]; minus gives the upper sideband."""
    t = np.arange(len(m)) / fs
    mh = hilbert(m)
    sgn = -1.0 if upper else 1.0
    return amp / 2 * (m * np.cos(2 * np.pi * fc * t) + sgn * mh * np.sin(2 * np.pi * fc * t))


def dsb_sc(m, fc, fs, amp=1.0):
    """DSB-SC: A m(t) cos(wc t)."""
    t = np.arange(len(m)) / fs
    return amp * m * np.cos(2 * np.pi * fc * t)


def lowpass(x, cutoff, fs, ntaps=1001):
    """Linear-phase FIR low-pass with its delay removed (zero-phase via filtfilt-free alignment)."""
    h = signal.firwin(ntaps, cutoff, fs=fs)
    y = np.convolve(x, h, mode="same")
    return y


def coherent_demod(s, fc, fs, cutoff, phase=0.0, freq_offset=0.0):
    """Multiply by 2 cos((wc + dw) t + phase) and low-pass."""
    t = np.arange(len(s)) / fs
    return lowpass(2 * s * np.cos(2 * np.pi * (fc + freq_offset) * t + phase), cutoff, fs)


# ------------------------------------------------------------------ AM
def am(m, fc, fs, ka, amp=1.0):
    """Conventional AM: A [1 + ka m(t)] cos(wc t)."""
    t = np.arange(len(m)) / fs
    return amp * (1 + ka * m) * np.cos(2 * np.pi * fc * t)


def envelope(s):
    """Ideal envelope detector: magnitude of the analytic signal."""
    return np.abs(s + 1j * hilbert(s))


# ------------------------------------------------------------------ angle modulation (complex baseband)
def fm_baseband(m, fs, kf, amp=1.0):
    """Complex envelope of FM: A exp(j 2 pi kf * integral of m); kf in Hz per unit of m."""
    phase = 2 * np.pi * kf * np.cumsum(m) / fs
    return amp * np.exp(1j * phase)


def pm_baseband(m, kp, amp=1.0):
    """Complex envelope of PM: A exp(j kp m)."""
    return amp * np.exp(1j * kp * np.asarray(m))


def fm_discriminator(z, fs):
    """Instantaneous frequency (Hz) of a complex baseband signal: angle(z[n] conj(z[n-1])) fs / 2 pi."""
    d = np.angle(z[1:] * np.conj(z[:-1])) * fs / (2 * np.pi)
    return np.concatenate([[d[0]], d])


def deemphasis(x, tau, fs):
    """First-order de-emphasis 1/(1 + j 2 pi f tau) (impulse-invariant one-pole)."""
    a = math.exp(-1 / (fs * tau))
    return signal.lfilter([1 - a], [1, -a], x)


def preemphasis(x, tau, fs):
    """Inverse of `deemphasis` (exactly, sample by sample)."""
    a = math.exp(-1 / (fs * tau))
    return signal.lfilter([1, -a], [1 - a], x)


# ------------------------------------------------------------------ tone FM spectra
def bessel_lines(beta, nmax):
    """Amplitudes J_n(beta) of the carrier (n = 0) and sidebands n = -nmax..nmax of tone FM."""
    n = np.arange(-nmax, nmax + 1)
    return n, jv(n, beta)


def power_fraction(beta, nmax):
    """Fraction of tone-FM power in the carrier and the first nmax sideband pairs."""
    _, a = bessel_lines(beta, nmax)
    return float(np.sum(a ** 2))


def carson(deviation, w):
    """Carson's rule bandwidth 2 (deviation + W)."""
    return 2 * (deviation + w)


# ------------------------------------------------------------------ output SNR
def snr_theory_db(scheme, gamma_db, pm=0.5, ka=1.0, d=5.0, peak=1.0):
    """Above-threshold output SNR (dB) against the baseband reference gamma = S_R/(N0 W).

    DSB-SC and SSB: gamma. AM (envelope, ka): ka^2 Pm / (1 + ka^2 Pm) gamma.
    FM with deviation ratio d = Delta f / W: 3 d^2 (Pm / peak^2) gamma.
    """
    g = 10 ** (gamma_db / 10)
    if scheme in ("dsb", "ssb"):
        r = g
    elif scheme == "am":
        r = ka * ka * pm / (1 + ka * ka * pm) * g
    elif scheme == "fm":
        r = 3 * d * d * pm / peak ** 2 * g
    else:
        raise ValueError(scheme)
    return 10 * math.log10(r)


def measured_snr_db(y, m):
    """SNR of an output y that should be proportional to m: project onto m, the rest is noise."""
    y = np.asarray(y, dtype=float) - np.mean(y)
    m = np.asarray(m, dtype=float) - np.mean(m)
    g = np.dot(y, m) / np.dot(m, m)
    e = y - g * m
    return 10 * math.log10(g * g * np.dot(m, m) / np.dot(e, e))


def simulate_fm_snr(gamma_db, d=5.0, w=15e3, fs=1.2e6, n=1 << 20, fm_tone=None, rng=None, if_factor=1.0):
    """Monte Carlo FM link in complex baseband: tone (or given) message, deviation d*W, received power 1/2
    (|z| = 1), complex noise of one-sided bandpass density N0 set from gamma, IF filter at Carson's
    bandwidth times if_factor, discriminator, ideal low-pass to W. Returns the measured output SNR in dB."""
    rng = np.random.default_rng() if rng is None else rng
    t = np.arange(n) / fs
    f_tone = w * 0.3 if fm_tone is None else fm_tone
    m = np.cos(2 * np.pi * f_tone * t)
    z = fm_baseband(m, fs, d * w)
    s_r = 0.5  # bandpass power of |z| = 1
    n0 = s_r / (10 ** (gamma_db / 10) * w)
    # bandpass noise of one-sided density N0 -> n_I and n_Q each with two-sided PSD N0 (17-01 section 3.9),
    # so over the sampled band of width fs each has variance N0 * fs.
    sigma = math.sqrt(n0 * fs)
    r = z + sigma * (rng.standard_normal(n) + 1j * rng.standard_normal(n))
    bt = carson(d * w, w) * if_factor
    h = signal.firwin(801, bt / 2, fs=fs)
    r = np.convolve(r, h, mode="same")
    f_inst = fm_discriminator(r, fs)
    H = np.fft.rfft(f_inst)
    fr = np.fft.rfftfreq(n, 1 / fs)
    y = np.fft.irfft(np.where(fr <= w, H, 0), n)
    k = 2000
    return measured_snr_db(y[k:-k], m[k:-k])


def _brickwall(x, fs, lo, hi):
    """Ideal band-pass by FFT: keep lo <= |f| <= hi."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / fs)
    return np.fft.irfft(np.where((f >= lo) & (f <= hi), X, 0), len(x))


def simulate_linear_snr(scheme, gamma_db, w=4e3, fc=50e3, fs=400e3, n=1 << 20, ka=0.9, rng=None):
    """Monte Carlo of DSB-SC, SSB (upper) or AM (envelope detector) on a real passband signal.

    The message is a three-tone signal below W, scaled to a peak of exactly 1 (ka < 1 avoids overmodulation). Real white noise of one-sided
    density N0 (per-sample variance N0 fs / 2) is set from gamma = S_R/(N0 W), filtered by an ideal pre-detection
    band-pass matched to the scheme's band, demodulated and low-passed to W. Returns the measured output SNR (dB).
    """
    rng = np.random.default_rng() if rng is None else rng
    t = np.arange(n) / fs
    # three tones whose frequencies are multiples of fs/n (periodic in the record), peak about 1
    fr = [round(f * n / fs) * fs / n for f in (0.11 * w, 0.37 * w, 0.83 * w)]
    m = sum(np.cos(2 * np.pi * f * t + p) for f, p in zip(fr, (0.0, 1.0, 2.0)))
    m = m / np.max(np.abs(m))  # peak exactly 1, so ka < 1 avoids overmodulation
    if scheme == "dsb":
        s, lo, hi = dsb_sc(m, fc, fs), fc - w, fc + w
    elif scheme == "ssb":
        s, lo, hi = ssb(m, fc, fs, upper=True), fc, fc + w
    elif scheme == "am":
        s, lo, hi = am(m, fc, fs, ka), fc - w, fc + w
    else:
        raise ValueError(scheme)
    s_r = np.mean(s ** 2)
    n0 = s_r / (10 ** (gamma_db / 10) * w)
    noise = _brickwall(math.sqrt(n0 * fs / 2) * rng.standard_normal(n), fs, lo, hi)
    r = s + noise
    if scheme == "am":
        y = envelope(r)
    else:
        y = 2 * r * np.cos(2 * np.pi * fc * t)
    y = _brickwall(y, fs, 0, w)
    return measured_snr_db(y, m), float(np.mean(m ** 2))
