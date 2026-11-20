"""DFT toolkit for Lab 16-03: the DFT written out from its definition, circular convolution, block convolution.

numpy.fft is used only to cross-check. Index conventions: x[0..N-1], X[0..N-1], W_N = exp(-j 2 pi / N).

Functions
- dft_matrix(N)              the N x N matrix F with F[k, n] = W_N^(k n)
- dft(x), idft(X)            O(N^2) transforms from the definition
- dtft(x, w)                 DTFT of a finite sequence at frequencies w (rad/sample)
- bin_freq(k, N, fs)         frequency of bin k in Hz, with bins above N/2 mapped to negative frequencies
- circ_shift(x, m)           x[((n - m)) mod N]
- circ_conv(x, h, N)         N-point circular convolution, computed directly (no DFT)
- overlap_add(x, h, N)       linear convolution in blocks with N-point DFTs
- overlap_save(x, h, N)      the same, keeping the valid part of each circular convolution
- fft_conv_cost(M, N)        real multiplies per output sample of FFT block convolution (radix-2 model of 16-04)
"""
from __future__ import annotations

import math

import numpy as np


def dft_matrix(N):
    n = np.arange(N)
    return np.exp(-2j * np.pi * np.outer(n, n) / N)


def dft(x):
    x = np.asarray(x, complex)
    return dft_matrix(len(x)) @ x


def idft(X):
    X = np.asarray(X, complex)
    N = len(X)
    return np.conj(dft_matrix(N)) @ X / N


def dtft(x, w):
    x = np.asarray(x, complex)
    w = np.atleast_1d(np.asarray(w, float))
    return np.exp(-1j * np.outer(w, np.arange(len(x)))) @ x


def bin_freq(k, N, fs):
    k = np.asarray(k)
    return np.where(k < N / 2, k, k - N) * fs / N


def circ_shift(x, m):
    x = np.asarray(x)
    N = len(x)
    return np.array([x[(n - m) % N] for n in range(N)])


def circ_conv(x, h, N):
    xp = np.zeros(N, complex)
    hp = np.zeros(N, complex)
    xp[:len(x)] = x
    hp[:len(h)] = h
    y = np.array([sum(hp[k] * xp[(n - k) % N] for k in range(N)) for n in range(N)])
    return np.real_if_close(y, tol=1e6)


def overlap_add(x, h, N):
    """Blocks of L = N - M + 1 inputs, each zero-padded to N and multiplied by H in the DFT domain."""
    x, h = np.asarray(x, float), np.asarray(h, float)
    M = len(h)
    L = N - M + 1
    if L < 1:
        raise ValueError("N must be at least the filter length")
    H = np.fft.fft(h, N)
    y = np.zeros(len(x) + M - 1)
    for start in range(0, len(x), L):
        blk = x[start:start + L]
        yb = np.real(np.fft.ifft(np.fft.fft(blk, N) * H))
        end = min(start + N, len(y))
        y[start:end] += yb[:end - start]
    return y


def overlap_save(x, h, N):
    """Overlapping input blocks of length N; the first M - 1 outputs of each circular convolution are discarded."""
    x, h = np.asarray(x, float), np.asarray(h, float)
    M = len(h)
    L = N - M + 1
    H = np.fft.fft(h, N)
    xpad = np.concatenate([np.zeros(M - 1), x, np.zeros(N)])
    out = []
    for start in range(0, len(x) + M - 1, L):
        blk = xpad[start:start + N]
        yb = np.real(np.fft.ifft(np.fft.fft(blk, N) * H))
        out.append(yb[M - 1:])
    return np.concatenate(out)[:len(x) + M - 1]


def fft_conv_cost(M, N):
    """Real multiplies per output sample: per block, a forward FFT and an inverse FFT of (N/2) log2 N complex
    multiplies each, plus N complex multiplies for the spectrum product (the filter's FFT is precomputed);
    4 real multiplies per complex one; L = N - M + 1 new outputs per block."""
    L = N - M + 1
    complex_mults = 2 * (N / 2) * math.log2(N) + N
    return 4 * complex_mults / L
