"""Multirate toolkit for Lab 16-09: decimation, interpolation, polyphase structures, half-band and CIC filters.

Conventions. Rates change by integer factors M (down) and L (up). Filters are FIR tap arrays. The polyphase
components of h for factor M are E_k[n] = h[nM + k], k = 0..M-1, so H(z) = sum_k z^-k E_k(z^M).

Functions
- downsample(x, M), upsample(x, L)          keep every M-th sample; insert L - 1 zeros after each sample
- decimate_direct(x, h, M)                  filter at the high rate, then keep every M-th output (wasteful reference)
- polyphase(h, M)                           the M polyphase components (zero-padded to equal length)
- decimate_polyphase(x, h, M)               the same outputs, computing only kept samples: each branch filter runs at
                                            the low rate on its own decimated input stream (a commutator)
- interpolate_direct(x, h, L)               upsample, then filter at the high rate
- interpolate_polyphase(x, h, L)            the same outputs from L branch filters running at the low rate
- resample_rational(x, h, L, M)             upsample by L, filter, downsample by M (reference; h designed at L*fs)
- resample_polyphase(x, h, L, M)            the same outputs computing only the phase each output needs:
                                            y[m] = sum_j h[k + jL] x[q - j] with mM = qL + k
- mults_per_second(taps, rate)              taps * rate
- halfband_taps_nonzero(n)                  nonzero taps of an n-tap half-band filter (n = 4K + 3)
- cic_response(f, R, N, fs_in)              |H(f)| of an N-stage CIC decimator by R (differential delay 1), DC gain 1
- cic_decimate_int(x, R, N, width)          bit-true CIC decimator: N integrators at the input rate, decimate by R, N
                                            combs at the output rate, all registers `width` bits with two's-complement
                                            wrap-around (the arithmetic of cic_decim.v); output not normalized (gain R^N)
- wrap(v, width)                            reduce an integer to a signed `width`-bit two's-complement value
"""
from __future__ import annotations

import numpy as np


def downsample(x, M):
    return np.asarray(x)[::M]


def upsample(x, L):
    x = np.asarray(x)
    y = np.zeros(len(x) * L, dtype=np.result_type(x, float))
    y[::L] = x
    return y


def decimate_direct(x, h, M):
    return np.convolve(x, h)[: len(x)][::M]


def polyphase(h, M):
    h = np.asarray(h, dtype=float)
    K = -(-len(h) // M)
    hp = np.r_[h, np.zeros(K * M - len(h))]
    return hp.reshape(K, M).T  # row k is E_k


def decimate_polyphase(x, h, M):
    """y[m] = sum_k sum_n E_k[n] x[(m - n)M - k]; branch k sees the input delayed by k and decimated by M."""
    x = np.asarray(x, dtype=float)
    E = polyphase(h, M)
    nout = -(-len(x) // M)
    y = np.zeros(nout)
    for k in range(M):
        xk = np.r_[np.zeros(k), x][: len(x)][::M]  # x[mM - k]
        y += np.convolve(xk, E[k])[:nout]
    return y


def interpolate_direct(x, h, L):
    xu = upsample(x, L)
    return np.convolve(xu, h)[: len(xu)]


def interpolate_polyphase(x, h, L):
    """Output phase k at low-rate time m is sum_n E_k[n] x[m - n]: L short filters, then interleave."""
    x = np.asarray(x, dtype=float)
    E = polyphase(h, L)
    y = np.zeros(len(x) * L)
    for k in range(L):
        y[k::L] = np.convolve(x, E[k])[: len(x)]
    return y


def resample_rational(x, h, L, M):
    return interpolate_direct(x, h, L)[::M]


def resample_polyphase(x, h, L, M):
    x = np.asarray(x, dtype=float)
    h = np.asarray(h, dtype=float)
    E = polyphase(h, L)  # E[k][j] = h[jL + k]
    nout = -(-len(x) * L // M)
    y = np.zeros(nout)
    xp = np.r_[np.zeros(E.shape[1]), x]
    off = E.shape[1]
    for m in range(nout):
        q, k = divmod(m * M, L)
        seg = xp[off + q - E.shape[1] + 1: off + q + 1][::-1]
        y[m] = E[k] @ seg
    return y


def mults_per_second(taps, rate):
    return taps * rate


def halfband_taps_nonzero(n):
    assert n % 4 == 3
    c = (n - 1) // 2
    return 1 + 2 * ((c + 1) // 2)


def cic_response(f, R, N, fs_in):
    f = np.atleast_1d(np.asarray(f, dtype=float))
    num = np.sin(np.pi * f * R / fs_in)
    den = R * np.sin(np.pi * f / fs_in)
    out = np.ones_like(f)
    nz = np.abs(den) > 1e-300
    out[nz] = np.abs(num[nz] / den[nz]) ** N
    return out


def wrap(v, width):
    m = 1 << width
    v &= m - 1
    return v - m if v >= (m >> 1) else v


def cic_decimate_int(x, R, N, width):
    integ = [0] * N
    combs = [0] * N
    y = []
    for n, xn in enumerate(x):
        acc = int(xn)
        for i in range(N):
            integ[i] = wrap(integ[i] + acc, width)
            acc = integ[i]
        if n % R == R - 1:
            v = acc
            for i in range(N):
                v, combs[i] = wrap(v - combs[i], width), v
            y.append(v)
    return y
