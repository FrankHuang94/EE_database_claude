"""DSP SerDes and FEC models for chapter 24-04.

ADC quantization and jitter limits; PAM symbol mapping and a channel; MMSE FFE design from cursors; slicers;
an ideal-feedback DFE and a Viterbi (MLSD) detector for short responses; exhaustive error-event search;
RS(544,514) failure and output BER for random errors; FEC rates, net coding gain and latency.
"""
from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import special, stats


def q(x):
    return 0.5 * special.erfc(np.asarray(x, dtype=float) / math.sqrt(2))


def q_inv(p):
    return math.sqrt(2) * special.erfcinv(2 * np.asarray(p, dtype=float))


# ---------------------------------------------------------------- ADC
def quantize(x, bits: int, full_scale: float):
    """Mid-rise uniform quantizer over +/- full_scale/2 with clipping."""
    step = full_scale / 2 ** bits
    xc = np.clip(x, -full_scale / 2 + step / 2, full_scale / 2 - step / 2)
    return (np.floor(xc / step) + 0.5) * step


def sqnr_db(bits: int, full_scale: float, signal_rms: float = math.sqrt(5 / 9)) -> float:
    return 20 * math.log10(signal_rms / (full_scale / 2 ** bits / math.sqrt(12)))


def jitter_snr_db(f: float, sigma_t: float) -> float:
    return -20 * math.log10(2 * math.pi * f * sigma_t)


def combine_snr_db(*snrs: float) -> float:
    return -10 * math.log10(sum(10 ** (-s / 10) for s in snrs))


# ---------------------------------------------------------------- link
def pam_symbols(n: int, levels: int = 4, seed: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pts = np.linspace(-1, 1, levels)
    return pts[rng.integers(0, levels, size=n)]


def channel(a: np.ndarray, h: dict, sigma: float, seed: int = 2) -> np.ndarray:
    """y_n = sum_k h_k a_{n-k} + noise, for cursors h indexed by lag (pre-cursors at negative lags)."""
    y = np.zeros(len(a))
    for k, hk in h.items():
        y += hk * np.roll(a, k)
    return y + np.random.default_rng(seed).normal(0.0, sigma, len(a))


def mmse_ffe(h: dict, sigma: float, pre: int, post: int, signal_var: float) -> dict:
    """MMSE FFE taps -pre..post (applied as z_n = sum_j c_j y_{n-j}) for unit-delay target a_n."""
    lags = list(range(-pre, post + 1))
    kmin, kmax = min(h), max(h)
    r = np.zeros((len(lags), len(lags)))
    p = np.zeros(len(lags))
    for i, ji in enumerate(lags):
        p[i] = signal_var * h.get(-ji, 0.0)
        for m, jm in enumerate(lags):
            acc = sum(h.get(k, 0.0) * h.get(k + jm - ji, 0.0) for k in range(kmin - 50, kmax + 50))
            r[i, m] = signal_var * acc + (sigma ** 2 if ji == jm else 0.0)
    c = np.linalg.solve(r, p)
    return dict(zip(lags, c))


def apply_ffe(y: np.ndarray, c: dict) -> np.ndarray:
    z = np.zeros(len(y))
    for j, cj in c.items():
        z += cj * np.roll(y, j)
    return z


def slice_pam(z: np.ndarray, levels: int = 4) -> np.ndarray:
    pts = np.linspace(-1, 1, levels)
    return pts[np.argmin(np.abs(z[:, None] - pts[None, :]), axis=1)]


# ---------------------------------------------------------------- DFE and MLSD on h = (h0, h1, ..., hL)
def dfe_ideal(y: np.ndarray, a: np.ndarray, h: list) -> np.ndarray:
    """Slicer with the post-cursors removed using the true past symbols (no error propagation): NRZ."""
    z = y.copy()
    for k in range(1, len(h)):
        z -= h[k] * np.roll(a, k)
    return np.where(z >= 0, 1.0, -1.0)


def viterbi(y: np.ndarray, h: list, levels=(-1.0, 1.0)) -> np.ndarray:
    """Maximum-likelihood sequence detection for y_n = sum_k h_k a_{n-k} + white noise."""
    L = len(h) - 1
    states = list(itertools.product(levels, repeat=L))  # (a_{n-1}, ..., a_{n-L})
    idx = {s: i for i, s in enumerate(states)}
    ns = len(states)
    cost = np.zeros(ns)
    back = np.zeros((len(y), ns), dtype=np.int32)
    sym = np.zeros((len(y), ns))
    for n, yn in enumerate(y):
        new = np.full(ns, np.inf)
        for i, s in enumerate(states):
            for a in levels:
                out = h[0] * a + sum(h[k] * s[k - 1] for k in range(1, L + 1))
                t = (a,) + s[:-1] if L > 0 else ()
                j = idx[t]
                c = cost[i] + (yn - out) ** 2
                if c < new[j]:
                    new[j] = c
                    back[n, j] = i
                    sym[n, j] = a
        cost = new
    j = int(np.argmin(cost))
    out = np.zeros(len(y))
    for n in range(len(y) - 1, -1, -1):
        out[n] = sym[n, j]
        j = back[n, j]
    return out


def min_error_distance(h, max_len: int = 7, step: float = 2.0):
    """Smallest ||e * h||^2 over NRZ error events e in {-2, 0, 2}^n starting and ending non-zero."""
    h = np.asarray(h, dtype=float)
    best, arg = math.inf, None
    for n in range(1, max_len + 1):
        for e in itertools.product((-step, 0.0, step), repeat=n):
            if e[0] == 0 or e[-1] == 0:
                continue
            d = np.convolve(e, h)
            dd = float(d @ d)
            if dd < best:
                best, arg = dd, e
    return best, arg


# ---------------------------------------------------------------- FEC
def rs_ucr(ber: float, n: int = 544, t: int = 15, m: int = 10) -> float:
    """Uncorrectable codeword ratio for independent bit errors."""
    ps = 1 - (1 - ber) ** m
    return float(stats.binom.sf(t, n, ps))


def rs_ber_out(ber: float, n: int = 544, t: int = 15, m: int = 10) -> float:
    return (t + 1) / (n * m) * rs_ucr(ber, n, t, m)


def ncg_db(p_in: float, p_out: float, rate: float) -> float:
    return 20 * math.log10(float(q_inv(p_out)) / float(q_inv(p_in))) + 10 * math.log10(rate)


def codeword_time(bits: int, rate: float) -> float:
    return bits / rate


def burst_corrected(t: int = 15, m: int = 10, interleave: int = 1) -> int:
    """Longest bit burst always corrected with symbols interleaved round-robin over `interleave` codewords."""
    return (interleave * t - 1) * m + 1
