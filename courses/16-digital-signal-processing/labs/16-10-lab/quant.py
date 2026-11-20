"""Quantization and fixed-point toolkit for Lab 16-10.

Conventions. A signed fixed-point number with I integer bits (including the sign) and F fractional bits has step
(LSB) 2^-F and range [-2^(I-1), 2^(I-1) - 2^-F]; Q1.15 is I = 1, F = 15. Integer-domain helpers work in LSB units.

Functions
- quantize(x, F, mode='round', I=None, overflow='saturate')   round ('round' = nearest, ties up; 'floor' = two's-
                                    complement truncation; 'zero' = magnitude truncation) to F fractional bits, then
                                    saturate or wrap to I integer bits if I is given
- sqnr_db(x, xq)                    10 log10(power(x) / power(x - xq))
- sine_sqnr(B, N=65536, amp=1.0)    simulated SQNR of a B-bit (full scale ±1) quantized sine of amplitude amp
- gaussian_sqnr(B, load=4.0, N)     simulated SQNR of a Gaussian signal with sigma = full scale / load, clipped
- noise_gain(b, a, n=200000)        sum of h[n]^2 of B/A (the factor by which a white error's variance grows)
- l1_norm(b, a, n)                  sum of |h[n]| (worst-case gain for bounded inputs)
- limit_cycle_first_order(a, y0, mode, n)   zero-input y[n] = Q(a y[n-1]) in LSB units ('round' = ties up,
                                    'zero' = magnitude truncation); returns the sequence
- second_order_zero_input(a1, a2, y1, y2, overflow, n)   zero-input Q1.15 recursion with Q2.14 coefficients,
                                    rounding, and 'wrap' or 'saturate' overflow; returns the sequence (LSB units)
- tpdf_dither(n, rng)               triangular dither in LSB units (sum of two independent uniforms on [-1/2, 1/2])
- harmonic_levels_db(y, k0, nh)     levels (dB re the fundamental) of harmonics 2..nh of a coherent tone in bin k0
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal


def quantize(x, F, mode="round", I=None, overflow="saturate"):
    x = np.asarray(x, dtype=float)
    s = x * 2.0**F
    if mode == "round":
        q = np.floor(s + 0.5)
    elif mode == "floor":
        q = np.floor(s)
    elif mode == "zero":
        q = np.trunc(s)
    else:
        raise ValueError(mode)
    if I is not None:
        lo, hi = -(2 ** (I - 1 + F)), 2 ** (I - 1 + F) - 1
        if overflow == "saturate":
            q = np.clip(q, lo, hi)
        else:
            m = 2 ** (I + F)
            q = (q - lo) % m + lo
    return q / 2.0**F


def sqnr_db(x, xq):
    x, xq = np.asarray(x, float), np.asarray(xq, float)
    return 10 * math.log10(np.mean(x**2) / np.mean((x - xq) ** 2))


def sine_sqnr(B, N=65536, amp=1.0, cycles=4093):
    n = np.arange(N)
    x = amp * np.sin(2 * np.pi * cycles * n / N + 0.1)
    F = B - 1
    return sqnr_db(x, quantize(x, F, I=1))


def gaussian_sqnr(B, load=4.0, N=1_000_000, seed=10):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(N) / load
    F = B - 1
    return sqnr_db(x, quantize(x, F, I=1))


def _impulse(b, a, n):
    return signal.lfilter(b, a, np.r_[1.0, np.zeros(n - 1)])


def noise_gain(b, a, n=200000):
    h = _impulse(b, a, n)
    return float(np.sum(h * h))


def l1_norm(b, a, n=200000):
    return float(np.sum(np.abs(_impulse(b, a, n))))


def limit_cycle_first_order(a, y0, mode="round", n=80):
    y, out = int(y0), []
    for _ in range(n):
        v = a * y
        y = math.floor(v + 0.5) if mode == "round" else int(v)
        out.append(y)
    return out


def second_order_zero_input(a1, a2, y1, y2, overflow="saturate", n=300):
    q = 2**15
    Y1, Y2 = round(y1 * q), round(y2 * q)
    A1, A2 = round(a1 * 2**14), round(a2 * 2**14)
    out = []
    for _ in range(n):
        y = (-A1 * Y1 - A2 * Y2 + (1 << 13)) >> 14
        if overflow == "wrap":
            y = (y + q) % (2 * q) - q
        else:
            y = max(-q, min(q - 1, y))
        Y2, Y1 = Y1, y
        out.append(y)
    return out


def tpdf_dither(n, rng):
    return rng.uniform(-0.5, 0.5, n) + rng.uniform(-0.5, 0.5, n)


def harmonic_levels_db(y, k0, nh=5):
    Y = np.abs(np.fft.rfft(y))
    N = len(y)
    out = []
    for h in range(2, nh + 1):
        k = (h * k0) % N
        if k > N // 2:
            k = N - k
        out.append(20 * math.log10(max(Y[k], 1e-300) / Y[k0]))
    return out
