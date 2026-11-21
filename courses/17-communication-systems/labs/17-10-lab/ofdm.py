"""OFDM toolkit for the 17-10 lab.

- OFDM modulation and demodulation with an IFFT/FFT and a cyclic prefix;
- multipath channels, the per-subcarrier response, zero-forcing and MMSE one-tap equalizers;
- end-to-end QPSK/16-QAM OFDM link simulation, with or without a sufficient cyclic prefix;
- carrier-frequency offset, inter-carrier interference (exact and small-offset forms) and Doppler ICI;
- peak-to-average power ratio of oversampled OFDM symbols, its CCDF, and DFT-spread OFDM for comparison;
- NR numerology: useful symbol and cyclic-prefix durations from TS 38.211, and the TS 38.101 guard-band formula.

Conventions: X[k] are frequency-domain symbols on N subcarriers; x[n] = IFFT(X) * sqrt(N) has the same
average power per sample as per subcarrier.
"""
from __future__ import annotations

import math

import numpy as np


# ------------------------------------------------------------------ constellations
def qam(m):
    """Gray-free square QAM with unit average energy (the lab only needs symbol decisions)."""
    k = int(round(math.sqrt(m)))
    lv = np.arange(-(k - 1), k, 2, dtype=float)
    pts = (lv[:, None] + 1j * lv[None, :]).ravel()
    return pts / math.sqrt(np.mean(np.abs(pts) ** 2))


def nearest(y, pts):
    return pts[np.argmin(np.abs(y[..., None] - pts), axis=-1)]


# ------------------------------------------------------------------ modulator and demodulator
def ofdm_mod(X, ncp):
    """Rows of X are OFDM symbols (N subcarriers each); returns the serial time signal with CPs."""
    X = np.atleast_2d(X)
    n = X.shape[1]
    x = np.fft.ifft(X, axis=1) * math.sqrt(n)
    return np.hstack([x[:, n - ncp :], x]).ravel()


def ofdm_demod(y, n, ncp, nsym):
    """Strip the cyclic prefixes and FFT each symbol."""
    blocks = np.asarray(y)[: nsym * (n + ncp)].reshape(nsym, n + ncp)[:, ncp:]
    return np.fft.fft(blocks, axis=1) / math.sqrt(n)


def channel_response(h, n):
    """Per-subcarrier gains H[k] of a tapped-delay channel h on an N-point FFT."""
    return np.fft.fft(np.asarray(h), n)


def apply_channel(x, h, snr_db, rng):
    """Linear convolution with h, then complex AWGN at the given per-sample SNR (signal power 1)."""
    y = np.convolve(x, h)[: len(x)]
    sigma = math.sqrt(10 ** (-snr_db / 10) / 2)
    return y + sigma * (rng.standard_normal(len(y)) + 1j * rng.standard_normal(len(y)))


def equalize(Y, H, snr_db=None):
    """One-tap zero-forcing (snr_db None) or MMSE equalizer per subcarrier."""
    if snr_db is None:
        return Y / H
    n0 = 10 ** (-snr_db / 10)
    return Y * np.conj(H) / (np.abs(H) ** 2 + n0)


def simulate_link(n, ncp, h, m, snr_db, nsym, rng, mmse=False):
    """Symbol-error rate of M-QAM OFDM over channel h (perfect channel knowledge)."""
    pts = qam(m)
    X = pts[rng.integers(0, m, (nsym, n))]
    y = apply_channel(ofdm_mod(X, ncp), h, snr_db, rng)
    Y = ofdm_demod(y, n, ncp, nsym)
    H = channel_response(h, n)
    Xh = equalize(Y, H, snr_db if mmse else None)
    return float(np.mean(nearest(Xh, pts) != X))


# ------------------------------------------------------------------ frequency offset and Doppler
def cfo_attenuation(eps, n):
    """|sin(pi eps) / (N sin(pi eps / N))|^2: power left on the wanted subcarrier for offset eps (in spacings)."""
    if eps == 0:
        return 1.0
    return (math.sin(math.pi * eps) / (n * math.sin(math.pi * eps / n))) ** 2


def cfo_ici_power(eps, n):
    """Total ICI power on a subcarrier for unit-power independent data on all N subcarriers."""
    return 1.0 - cfo_attenuation(eps, n)


def ici_small_offset(eps):
    """Leading-order ICI for small eps: (pi eps)^2 / 3."""
    return (math.pi * eps) ** 2 / 3


def ici_doppler(fd, delta_f):
    """Leading-order ICI for a Jakes Doppler spectrum: average (pi fd cos(a) T)^2/3 over a = (pi fd/df)^2/6."""
    return (math.pi * fd / delta_f) ** 2 / 6


def measure_ici(eps, n, nsym, rng):
    """Simulated ICI power: apply a frequency offset eps (in subcarrier spacings) and compare with ideal."""
    pts = qam(4)
    X = pts[rng.integers(0, 4, (nsym, n))]
    x = np.fft.ifft(X, axis=1) * math.sqrt(n)
    rot = np.exp(2j * np.pi * eps * np.arange(n) / n)
    Y = np.fft.fft(x * rot, axis=1) / math.sqrt(n)
    gain = np.mean(Y * np.conj(X)) / np.mean(np.abs(X) ** 2)
    return float(np.mean(np.abs(Y - gain * X) ** 2) / np.mean(np.abs(X) ** 2))


# ------------------------------------------------------------------ PAPR
def papr_db(x):
    p = np.abs(x) ** 2
    return 10 * np.log10(p.max(axis=-1) / p.mean(axis=-1))


def ofdm_papr(nsc, nsym, rng, m=4, oversample=4, nfft=None):
    """PAPR of OFDM symbols with nsc active subcarriers, oversampled by zero padding."""
    pts = qam(m)
    nfft = nfft or nsc
    L = nfft * oversample
    X = np.zeros((nsym, L), complex)
    data = pts[rng.integers(0, m, (nsym, nsc))]
    half = nsc // 2
    X[:, 1 : half + 1] = data[:, :half]
    X[:, L - (nsc - half) :] = data[:, half:]
    return papr_db(np.fft.ifft(X, axis=1))


def dfts_papr(nsc, nsym, rng, m=4, oversample=4, nfft=None):
    """PAPR of DFT-spread OFDM (single-carrier-like): DFT-precode nsc symbols, map contiguously, IFFT."""
    pts = qam(m)
    nfft = nfft or 4 * nsc
    L = nfft * oversample
    data = pts[rng.integers(0, m, (nsym, nsc))]
    S = np.fft.fft(data, axis=1)
    X = np.zeros((nsym, L), complex)
    X[:, :nsc] = S
    return papr_db(np.fft.ifft(X, axis=1))


def papr_ccdf_theory(gamma_db, n):
    """Nyquist-sampled approximation P(PAPR > gamma) = 1 - (1 - e^-gamma)^N for N independent Gaussian samples."""
    g = 10 ** (np.asarray(gamma_db) / 10)
    return 1 - (1 - np.exp(-g)) ** n


def papr_at(prob, n):
    """PAPR (dB) exceeded with probability prob under the same approximation."""
    return 10 * math.log10(-math.log(1 - (1 - prob) ** (1 / n)))


# ------------------------------------------------------------------ NR numerology
TC = 1 / (480e3 * 4096)  # TS 38.211 basic time unit
KAPPA = 64


def nr_symbol(mu, extended_first=False):
    """Useful symbol and normal-CP durations (s) for numerology mu (TS 38.211 clause 5.3.1)."""
    tu = 2048 * KAPPA * 2.0**-mu * TC
    tcp = 144 * KAPPA * 2.0**-mu * TC + (16 * KAPPA * TC if extended_first else 0.0)
    return tu, tcp


def nr_slot_duration(mu):
    """Sum of 14 symbols; symbols l = 0 and l = 7 * 2^mu of each subframe carry 16 kappa extra."""
    total = 0.0
    for sym in range(14 * 2**mu):  # one subframe
        tu, tcp = nr_symbol(mu, extended_first=(sym % (7 * 2**mu) == 0))
        total += tu + tcp
    return total / 2**mu


def nr_guardband_khz(bw_mhz, nrb, scs_khz):
    """TS 38.101-1 Table 5.3.3-1 note: (BW x 1000 - NRB x SCS x 12)/2 - SCS/2 (kHz)."""
    return (bw_mhz * 1000 - nrb * scs_khz * 12) / 2 - scs_khz / 2
