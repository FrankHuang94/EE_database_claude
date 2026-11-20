"""FIR filter-design toolkit for Lab 16-06: linear phase, windows, Kaiser, frequency sampling and equiripple.

Conventions. A filter of order M has M + 1 taps h[0..M]. Frequencies are in radians per sample (0 to pi) unless a
function takes fs. A linear-phase filter is written H(e^{jw}) = e^{-jwM/2} A(w) for symmetric taps (types I and II)
and e^{-jwM/2} j A(w) for antisymmetric taps (types III and IV), with A(w) real: the "amplitude response".

Functions
- deltas(Ap_db, As_db)              passband ripple delta_p from a peak-to-peak ripple in dB; delta_s from an attenuation
- ideal_lowpass(M, wc)              the ideal low-pass impulse response delayed by M/2: sin(wc(n - M/2)) / (pi(n - M/2))
- i0(x)                             modified Bessel function I0 by its power series
- window(name, M, beta=None)        symmetric windows of length M + 1: 'rect', 'hann', 'hamming', 'blackman', 'kaiser'
- window_lowpass(M, wp, ws, name)   window-method low-pass, cutoff midway between the band edges
- kaiser_beta(A), kaiser_order(A, dw)   Kaiser's empirical design formulas (A in dB, dw the transition width)
- fir_type(h)                       1 to 4 by length parity and symmetry, or 0 if not linear phase
- amplitude(h, w)                   the real amplitude response A(w)
- measure(h, wp, ws)                (delta_p, delta_s, ripple_db, atten_db) on dense band grids
- freq_sampling_lowpass(N, kp, T)   type I frequency-sampling design: amplitude samples 1 (k <= kp), T at kp + 1, 0 above
- remez_lowpass(ntaps, wp, ws, dp, ds)   equiripple (Parks-McClellan) design, stopband weight dp/ds, dense grid
- min_taps(design, wp, ws, dp, ds, start, stop)   smallest tap count in [start, stop) whose design meets the spec
- order_kaiser_pm(dp, ds, dw), length_bellanger(dp, ds, dw)   empirical order estimates for equiripple designs
- alternations(h, wp, ws, dp, ds)   number of alternating extrema of the weighted error (the alternation theorem)
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal


def deltas(Ap_db, As_db):
    g = 10 ** (Ap_db / 20)
    return (g - 1) / (g + 1), 10 ** (-As_db / 20)


def ideal_lowpass(M, wc):
    n = np.arange(M + 1) - M / 2
    return wc / np.pi * np.sinc(wc * n / np.pi)


def i0(x, terms=60):
    x = np.asarray(x, dtype=float)
    s = np.ones_like(x)
    t = np.ones_like(x)
    for k in range(1, terms):
        t = t * (x / (2 * k)) ** 2
        s = s + t
    return s


def window(name, M, beta=None):
    n = np.arange(M + 1)
    if name == "rect":
        return np.ones(M + 1)
    if name == "hann":
        return 0.5 - 0.5 * np.cos(2 * np.pi * n / M)
    if name == "hamming":
        return 0.54 - 0.46 * np.cos(2 * np.pi * n / M)
    if name == "blackman":
        return 0.42 - 0.5 * np.cos(2 * np.pi * n / M) + 0.08 * np.cos(4 * np.pi * n / M)
    if name == "kaiser":
        r = (n - M / 2) / (M / 2)
        return i0(beta * np.sqrt(np.clip(1 - r**2, 0, None))) / i0(beta)
    raise ValueError(name)


def window_lowpass(M, wp, ws, name, beta=None):
    return ideal_lowpass(M, (wp + ws) / 2) * window(name, M, beta)


def kaiser_beta(A):
    if A > 50:
        return 0.1102 * (A - 8.7)
    if A >= 21:
        return 0.5842 * (A - 21) ** 0.4 + 0.07886 * (A - 21)
    return 0.0


def kaiser_order(A, dw):
    return (A - 8) / (2.285 * dw)


def fir_type(h, tol=1e-12):
    h = np.asarray(h, dtype=float)
    odd_len = len(h) % 2 == 1
    if np.allclose(h, h[::-1], atol=tol):
        return 1 if odd_len else 2
    if np.allclose(h, -h[::-1], atol=tol):
        return 3 if odd_len else 4
    return 0


def amplitude(h, w):
    """A(w) with H = e^{-jwM/2} A (symmetric) or e^{-jwM/2} j A (antisymmetric)."""
    h = np.asarray(h, dtype=float)
    M = len(h) - 1
    w = np.atleast_1d(np.asarray(w, dtype=float))
    n = np.arange(M + 1)
    H = np.exp(-1j * np.outer(w, n)) @ h
    rot = H * np.exp(1j * w * M / 2)
    t = fir_type(h)
    return rot.imag if t in (3, 4) else rot.real


def measure(h, wp, ws, ngrid=20000):
    wpass = np.linspace(0, wp, ngrid)
    wstop = np.linspace(ws, np.pi, ngrid)
    Ap = amplitude(h, wpass)
    As = amplitude(h, wstop)
    dp = float(np.max(np.abs(Ap - 1)))
    ds = float(np.max(np.abs(As)))
    ripple_db = 20 * math.log10(np.max(np.abs(Ap)) / np.min(np.abs(Ap)))
    atten_db = -20 * math.log10(ds)
    return dp, ds, ripple_db, atten_db


def freq_sampling_lowpass(N, kp, T):
    """Type I (N odd) design whose amplitude response equals 1 at w_k = 2 pi k / N for k <= kp, T at kp + 1, else 0."""
    assert N % 2 == 1
    A = np.zeros((N - 1) // 2 + 1)
    A[: kp + 1] = 1.0
    A[kp + 1] = T
    n = np.arange(N) - (N - 1) / 2
    h = A[0] * np.ones(N)
    for k in range(1, len(A)):
        h = h + 2 * A[k] * np.cos(2 * np.pi * k * n / N)
    return h / N


def remez_lowpass(ntaps, wp, ws, dp, ds):
    return signal.remez(ntaps, [0, wp, ws, np.pi], [1, 0], weight=[1, dp / ds], fs=2 * np.pi, grid_density=64)


def min_taps(design, wp, ws, dp, ds, start, stop):
    for n in range(start, stop):
        try:
            h = design(n)
        except Exception:  # remez can fail to converge for some lengths
            continue
        mdp, mds, _, _ = measure(h, wp, ws)
        if mdp <= dp and mds <= ds:
            return n, h
    return None, None


def order_kaiser_pm(dp, ds, dw):
    return (-10 * math.log10(dp * ds) - 13) / (2.324 * dw)


def length_bellanger(dp, ds, dw):
    return (2 / 3) * math.log10(1 / (10 * dp * ds)) * (2 * np.pi / dw)


def alternations(h, wp, ws, dp, ds, ngrid=20000, tol=0.99):
    """Length of the longest sign-alternating run of weighted-error extrema reaching tol * max|E|.

    E(w) = W(w)(A(w) - D(w)) with D = 1, W = 1 in the passband and D = 0, W = dp/ds in the stopband. Local extrema
    of |E| on dense band grids, and the four band edges, are kept if they reach tol * max|E|; the count is one plus the
    number of sign changes along frequency, which is what the alternation theorem counts.
    """
    ext = []
    for band, D, W in ((np.linspace(0, wp, ngrid), 1.0, 1.0), (np.linspace(ws, np.pi, ngrid), 0.0, dp / ds)):
        E = W * (amplitude(h, band) - D)
        a = np.abs(E)
        idx = [0] + list(np.where((a[1:-1] >= a[:-2]) & (a[1:-1] >= a[2:]))[0] + 1) + [len(a) - 1]
        ext += [E[i] for i in idx]
    delta = max(abs(e) for e in ext)
    signs = [np.sign(e) for e in ext if abs(e) >= tol * delta]
    return 1 + sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])
