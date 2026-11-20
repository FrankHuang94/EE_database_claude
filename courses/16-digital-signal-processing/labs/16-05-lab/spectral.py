"""Spectral-analysis toolkit for Lab 16-05: windows and their figures of merit, periodograms, and ADC testing.

Windows are "DFT-even" (periodic): w[n] for n = 0..N-1 taken from a length-(N+1) symmetric window with the last
sample dropped, the form appropriate for spectral analysis with an N-point DFT.

Functions
- window(name, N)                 'rect', 'hann', 'hamming', 'blackman', 'bh4' (4-term Blackman-Harris), 'flattop'
- coherent_gain(w)                sum(w)/N
- enbw_bins(w)                    N sum(w^2) / (sum w)^2
- scalloping_db(w)                gain loss for a tone halfway between bins, in dB (negative)
- highest_sidelobe_db(w)          largest sidelobe relative to the main-lobe peak, in dB
- periodogram(x, w=None)          |X[k]|^2 / sum(w^2) for k = 0..N-1 (a power-spectral estimate per bin)
- welch(x, N, overlap=0.5, name)  averaged windowed periodograms of segments of length N
- coherent_bin(f_target, fs, N)   the odd bin M nearest f_target*N/fs that is relatively prime to N
- adc_metrics(x, M, nharm=5)      SNR, SINAD, THD, SFDR (dB) and ENOB from a coherently sampled record whose tone
                                  sits exactly in bin M (rectangular window, DC excluded, harmonics aliased)
- sine_fit3(x, f_over_fs)         least-squares fit of A cos + B sin + C at a known frequency; returns the residual rms
"""
from __future__ import annotations

import math

import numpy as np

_COEF = {
    "rect": [1.0],
    "hann": [0.5, 0.5],
    "hamming": [0.54, 0.46],
    "blackman": [0.42, 0.5, 0.08],
    "bh4": [0.35875, 0.48829, 0.14128, 0.01168],
    # flat-top window as defined in scipy.signal.windows.flattop (from D'Antona and Ferrero)
    "flattop": [0.21557895, 0.41663158, 0.277263158, 0.083578947, 0.006947368],
}


def window(name, N):
    a = _COEF[name]
    n = np.arange(N)
    w = np.zeros(N)
    for k, ak in enumerate(a):
        w += (-1) ** k * ak * np.cos(2 * np.pi * k * n / N)
    return w


def coherent_gain(w):
    return float(np.sum(w) / len(w))


def enbw_bins(w):
    return float(len(w) * np.sum(w**2) / np.sum(w) ** 2)


def _w_dtft(w, nu):
    """|W| at frequency nu in bins (nu = 1 is one DFT bin)."""
    N = len(w)
    n = np.arange(N)
    nu = np.atleast_1d(nu)
    return np.abs(np.exp(-2j * np.pi * np.outer(nu, n) / N) @ w)


def scalloping_db(w):
    return float(20 * math.log10(_w_dtft(w, 0.5)[0] / _w_dtft(w, 0.0)[0]))


def highest_sidelobe_db(w, search=20, pts_per_bin=200):
    nu = np.linspace(0, search, search * pts_per_bin + 1)
    mag = _w_dtft(w, nu)
    mag = mag / mag[0]
    # first local minimum ends the main lobe
    i = 1
    while i < len(mag) - 1 and not (mag[i] <= mag[i - 1] and mag[i] <= mag[i + 1]):
        i += 1
    return float(20 * math.log10(np.max(mag[i:])))


def periodogram(x, w=None):
    x = np.asarray(x, float)
    if w is None:
        w = np.ones(len(x))
    X = np.fft.fft(x * w)
    return np.abs(X) ** 2 / np.sum(w**2)


def welch(x, N, overlap=0.5, name="hann"):
    w = window(name, N)
    step = int(N * (1 - overlap))
    segs = [x[s:s + N] for s in range(0, len(x) - N + 1, step)]
    return np.mean([periodogram(s, w) for s in segs], axis=0), len(segs)


def coherent_bin(f_target, fs, N):
    m0 = int(round(f_target * N / fs))
    for d in range(0, N):
        for m in (m0 - d, m0 + d):
            if 0 < m < N // 2 and m % 2 == 1 and math.gcd(m, N) == 1:
                return m
    raise ValueError("no coherent bin found")


def adc_metrics(x, M, nharm=5):
    x = np.asarray(x, float)
    N = len(x)
    P = np.abs(np.fft.fft(x)) ** 2
    half = P[:N // 2 + 1].copy()
    half[1:N // 2] *= 2                      # one-sided power
    half[0] = 0.0                            # exclude DC
    sig = half[M]
    harm_bins = []
    for h in range(2, nharm + 1):
        b = (h * M) % N
        if b > N // 2:
            b = N - b
        harm_bins.append(b)
    harm = sum(half[b] for b in harm_bins)
    other = half.copy()
    other[M] = 0.0
    nad = float(np.sum(other))              # noise and distortion
    noise = nad - harm
    spur = float(np.max(other))
    sinad = 10 * math.log10(sig / nad)
    return {
        "snr": 10 * math.log10(sig / noise),
        "sinad": sinad,
        "thd": 10 * math.log10(harm / sig),
        "sfdr": 10 * math.log10(sig / spur),
        "enob": (sinad - 1.76) / 6.02,
        "harm_bins": harm_bins,
    }


def sine_fit3(x, f_over_fs):
    x = np.asarray(x, float)
    n = np.arange(len(x))
    A = np.c_[np.cos(2 * np.pi * f_over_fs * n), np.sin(2 * np.pi * f_over_fs * n), np.ones(len(x))]
    coef, *_ = np.linalg.lstsq(A, x, rcond=None)
    resid = x - A @ coef
    amp = math.hypot(coef[0], coef[1])
    return amp, float(np.sqrt(np.mean(resid**2)))


def adc_metrics_window(x, name, cycles, nharm=5, guard=None):
    """SNR, SINAD, THD and ENOB from a non-coherent record: window it, sum the power within +-guard bins of the
    fundamental (at 'cycles' cycles per record, not necessarily an integer) and of each aliased harmonic, and
    treat the rest (DC region excluded) as noise. guard defaults to the window's main-lobe half-width plus 2 bins."""
    x = np.asarray(x, float)
    N = len(x)
    w = window(name, N)
    P = np.abs(np.fft.fft(x * w)) ** 2
    half = P[:N // 2 + 1].copy()
    half[1:N // 2] *= 2
    if guard is None:
        guard = {"rect": 3, "hann": 4, "hamming": 4, "blackman": 5, "bh4": 6, "flattop": 7}[name]
    mask = np.zeros(len(half), bool)
    mask[:guard + 1] = True                                      # DC and its skirt

    def band(f):
        f = f % N
        if f > N / 2:
            f = N - f
        c = int(round(f))
        return slice(max(c - guard, 0), min(c + guard + 1, len(half)))

    s = band(cycles)
    sig = half[s].sum()
    mask[s] = True
    harm = 0.0
    for h in range(2, nharm + 1):
        b = band(h * cycles)
        harm += half[b][~mask[b]].sum()
        mask[b] = True
    noise = half[~mask].sum() * len(half) / max(np.count_nonzero(~mask), 1)  # rescale for the bins removed
    sinad = 10 * math.log10(sig / (noise + harm))
    return {"snr": 10 * math.log10(sig / noise), "sinad": sinad, "thd": 10 * math.log10(harm / sig),
            "enob": (sinad - 1.76) / 6.02}
