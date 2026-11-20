"""Baseband PAM, ISI and equalization: helpers for the 17-04 lab.

- PAM level mapping with Gray coding, and level statistics;
- pulses: rectangular (NRZ), Manchester, sinc, raised cosine and root-raised cosine (closed forms);
- oversampled waveforms and a one-pole (RC) channel, exact for piecewise-constant inputs;
- sampled pulse responses (cursors), worst-case eye and pattern-averaged (statistical) BER;
- eye-diagram folding; zero-forcing FFE design and a DFE;
- binary error-rate simulation.

Conventions: symbol period T = 1 unless stated; cursors h[k] are indexed from -pre to +post with h[pre] the main
cursor; sinc x = sin(pi x)/(pi x).
"""
from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.stats import norm


# ------------------------------------------------------------------ PAM levels
def pam_levels(m):
    """Levels -(M-1), ..., -1, +1, ..., M-1 (spacing 2)."""
    return np.arange(-(m - 1), m, 2, dtype=float)


def gray_map(bits, m):
    """Map groups of log2(M) bits to PAM levels with Gray coding (adjacent levels differ in one bit)."""
    k = int(math.log2(m))
    bits = np.asarray(bits, dtype=int).reshape(-1, k)
    idx = np.zeros(len(bits), dtype=int)
    for j in range(k):
        idx = (idx << 1) | bits[:, j]
    gray_to_index = np.zeros(m, dtype=int)
    for i in range(m):
        gray_to_index[i ^ (i >> 1)] = i
    return pam_levels(m)[gray_to_index[idx]]


def mean_energy(m):
    """E[a^2] for equiprobable M-PAM with spacing 2: (M^2 - 1)/3."""
    return float(np.mean(pam_levels(m) ** 2))


# ------------------------------------------------------------------ pulses
def raised_cosine(t, alpha):
    """Raised-cosine pulse sinc(t) cos(pi a t)/(1 - (2 a t)^2), T = 1, with the removable singularities filled."""
    t = np.asarray(t, dtype=float)
    if alpha == 0:
        return np.sinc(t)
    x = 2 * alpha * t
    out = np.empty_like(t)
    sing = np.isclose(np.abs(x), 1.0)
    out[~sing] = np.sinc(t[~sing]) * np.cos(np.pi * alpha * t[~sing]) / (1 - x[~sing] ** 2)
    out[sing] = (np.pi / 4) * np.sinc(1 / (2 * alpha))
    return out


def raised_cosine_spectrum(f, alpha):
    """H_RC(f)/T for T = 1."""
    f = np.abs(np.asarray(f, dtype=float))
    lo, hi = (1 - alpha) / 2, (1 + alpha) / 2
    h = np.where(f <= lo, 1.0, 0.0)
    if alpha > 0:
        mid = (f > lo) & (f <= hi)
        h = np.where(mid, 0.5 * (1 + np.cos(np.pi / alpha * (f - lo))), h)
    return h


def root_raised_cosine(t, alpha):
    """Root-raised-cosine pulse (T = 1), unit energy; the cascade of two is a raised cosine."""
    t = np.asarray(t, dtype=float)
    a = alpha
    out = np.empty_like(t)
    z = np.isclose(t, 0)
    s = np.isclose(np.abs(4 * a * t), 1) if a > 0 else np.zeros_like(z)
    gen = ~(z | s)
    tg = t[gen]
    out[gen] = (np.sin(np.pi * tg * (1 - a)) + 4 * a * tg * np.cos(np.pi * tg * (1 + a))) / (np.pi * tg * (1 - (4 * a * tg) ** 2))
    out[z] = 1 - a + 4 * a / np.pi
    if a > 0:
        out[s] = a / np.sqrt(2) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * a)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * a)))
    return out


def manchester_psd(f, a2=1.0, t=1.0):
    """PSD of polar Manchester with independent equiprobable bits: A^2 T sinc^2(fT/2) sin^2(pi f T/2)."""
    f = np.asarray(f, dtype=float)
    return a2 * t * np.sinc(f * t / 2) ** 2 * np.sin(np.pi * f * t / 2) ** 2


def folded_spectrum(hfun, f, terms=5):
    """sum_m H(f - m) for T = 1: equals 1 for every f exactly when the pulse has zero ISI."""
    return sum(hfun(np.asarray(f) - m) for m in range(-terms, terms + 1))


# ------------------------------------------------------------------ waveforms and the RC channel
def waveform(symbols, sps, pulse="nrz"):
    """Oversampled baseband waveform with NRZ or Manchester pulses (sps even for Manchester)."""
    if pulse == "nrz":
        p = np.ones(sps)
    elif pulse == "manchester":
        p = np.concatenate([np.ones(sps // 2), -np.ones(sps // 2)])
    else:
        raise ValueError(pulse)
    return np.kron(np.asarray(symbols, dtype=float), p)


def rc_channel(x, tau_over_dt):
    """Exact one-pole RC response to a piecewise-constant input sampled every dt (zero-order hold)."""
    a = math.exp(-1 / tau_over_dt)
    y = np.empty(len(x))
    s = 0.0
    for i, xi in enumerate(x):
        s = a * s + (1 - a) * xi
        y[i] = s
    return y


def rc_cursors(r, n_post):
    """Cursors of NRZ through a one-pole channel sampled at bit ends: h0 = 1 - r, h_k = (1 - r) r^k."""
    return np.array([(1 - r) * r ** k for k in range(n_post + 1)])


# ------------------------------------------------------------------ eyes and error rates
def worst_case_eye(h, main):
    """Binary +-1: h[main] - sum of |h[k]| over k != main."""
    h = np.asarray(h, dtype=float)
    return float(h[main] - (np.sum(np.abs(h)) - abs(h[main])))


def pattern_samples(h, main, levels=(-1.0, 1.0), a0=1.0):
    """All noiseless sample values for symbol a0 over every pattern of the other cursors' symbols."""
    h = np.asarray(h, dtype=float)
    others = [k for k in range(len(h)) if k != main]
    vals = []
    for pat in itertools.product(levels, repeat=len(others)):
        vals.append(a0 * h[main] + sum(a * h[k] for a, k in zip(pat, others)))
    return np.array(vals)


def statistical_ber(h, main, sigma):
    """Exact binary BER with ISI and Gaussian noise: mean over patterns of Q(v / sigma) (threshold 0)."""
    v = pattern_samples(h, main)
    return float(np.mean(norm.sf(v / sigma)))


def fold_eye(y, sps, offset=0, span=2):
    """Cut a waveform into traces of `span` symbols for an eye diagram (rows = traces)."""
    n = (len(y) - offset) // (sps * span)
    return y[offset: offset + n * sps * span].reshape(n, sps * span)


# ------------------------------------------------------------------ equalizers
def zf_equalizer(h, main, ntaps):
    """Zero-forcing FFE with ntaps (odd) centred on the main cursor: forces q_k = delta_k for |k| <= ntaps//2."""
    h = np.asarray(h, dtype=float)
    n = ntaps // 2
    hk = lambda k: h[main + k] if 0 <= main + k < len(h) else 0.0  # noqa: E731
    A = np.array([[hk(i - j) for j in range(-n, n + 1)] for i in range(-n, n + 1)])
    b = np.zeros(ntaps)
    b[n] = 1.0
    return np.linalg.solve(A, b)


def apply_ffe(h, c):
    """Combined response q = h * c (full convolution)."""
    return np.convolve(np.asarray(h, dtype=float), np.asarray(c, dtype=float))


def simulate_binary(h, main, sigma, nsym, rng, ffe=None, dfe=None):
    """Binary +-1 symbols through cursors h with Gaussian noise; optional FFE taps (centred) and DFE taps
    (subtracting decided symbols times dfe[k-1] for postcursor k). Returns the bit-error rate."""
    a = rng.choice([-1.0, 1.0], nsym)
    y = np.convolve(a, h)[main: main + nsym] + sigma * rng.standard_normal(nsym)
    if ffe is not None:
        n = len(ffe) // 2
        y = np.convolve(y, ffe)[n: n + nsym]
    if dfe is None:
        d = np.sign(y)
    else:
        d = np.empty(nsym)
        for i in range(nsym):
            fb = sum(dfe[k] * d[i - k - 1] for k in range(len(dfe)) if i - k - 1 >= 0)
            d[i] = 1.0 if y[i] - fb >= 0 else -1.0
    return float(np.mean(d != a))
