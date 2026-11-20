"""Discrete-time systems toolkit for Lab 16-01 (and later Course 16 labs).

Everything here is written out sample by sample, the way a DSP core or a hardware datapath computes it, so
that the operation counts are visible. numpy/scipy are used only to cross-check.

Functions
- digital_freq(f, fs)          analog frequency (Hz) -> digital frequency (rad/sample)
- apparent_freq(f, fs)         the frequency (0 .. fs/2) at which a sampled tone appears after aliasing
- dt_period(num, den)          fundamental period of cos(2*pi*(num/den)*n), or None if not periodic
- conv_mac(x, h)               direct convolution sum with a multiply-accumulate counter
- df1(b, a, x)                 direct-form-I difference equation y[n] = sum b_k x[n-k] - sum_{k>=1} a_k y[n-k]
- impulse(b, a, n), step(b, a, n)
- poles(a), is_stable(a)       roots of the denominator; BIBO stability of a causal recursion
- ma_gain(N, w)                magnitude response of the N-point moving average at w (rad/sample)
- ema(alpha, x)                exponential moving average y[n] = y[n-1] + alpha (x[n] - y[n-1])
- running_sum(x, N, bits=None) recursive moving sum; with bits, two's-complement wraparound at every step
- wrap(v, bits)                reduce an integer to a signed two's-complement value of the given width
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np


def digital_freq(f, fs):
    """Digital frequency in rad/sample of an analog tone at f Hz sampled at fs Hz."""
    return 2 * math.pi * f / fs


def apparent_freq(f, fs):
    """Frequency in [0, fs/2] that a real tone at f Hz appears at after sampling at fs Hz."""
    r = math.fmod(f, fs)
    if r < 0:
        r += fs
    return fs - r if r > fs / 2 else r


def dt_period(num, den):
    """Fundamental period N of cos(2*pi*(num/den)*n) for integers num, den; None if the frequency is irrational.

    The sequence repeats when (num/den)*N is an integer, so N = den / gcd(num, den).
    """
    fr = Fraction(num, den)
    return fr.denominator


def conv_mac(x, h):
    """Convolution sum y[n] = sum_k h[k] x[n-k] for finite x and h, counting multiply-accumulates.

    Returns (y, macs). Only products of samples that exist are counted (no zero padding)."""
    x, h = list(x), list(h)
    y = [0.0] * (len(x) + len(h) - 1)
    macs = 0
    for n in range(len(y)):
        acc = 0.0
        for k in range(len(h)):
            if 0 <= n - k < len(x):
                acc += h[k] * x[n - k]
                macs += 1
        y[n] = acc
    return np.array(y), macs


def df1(b, a, x):
    """Direct-form-I recursion with a[0] normalized to 1, from rest (all past values zero)."""
    b = np.asarray(b, float) / a[0]
    a = np.asarray(a, float) / a[0]
    y = np.zeros(len(x))
    for n in range(len(x)):
        acc = 0.0
        for k in range(len(b)):
            if n - k >= 0:
                acc += b[k] * x[n - k]
        for k in range(1, len(a)):
            if n - k >= 0:
                acc -= a[k] * y[n - k]
        y[n] = acc
    return y


def impulse(b, a, n):
    """First n samples of the impulse response."""
    d = np.zeros(n)
    d[0] = 1.0
    return df1(b, a, d)


def step(b, a, n):
    """First n samples of the step response."""
    return df1(b, a, np.ones(n))


def poles(a):
    """Roots of a[0] z^M + a[1] z^(M-1) + ... + a[M], the poles of a causal recursion with denominator a."""
    return np.roots(a) if len(a) > 1 else np.array([])


def is_stable(a, tol=1e-12):
    """A causal LTI recursion is BIBO stable iff every pole lies strictly inside the unit circle
    (assuming no pole-zero cancellation)."""
    p = poles(a)
    return bool(np.all(np.abs(p) < 1 - tol)) if p.size else True


def ma_gain(N, w):
    """|H(e^jw)| of the N-point moving average (1/N) sum_{k<N} x[n-k], from the closed form."""
    w = np.asarray(w, float)
    with np.errstate(invalid="ignore", divide="ignore"):
        g = np.abs(np.sin(N * w / 2) / (N * np.sin(w / 2)))
    return np.where(np.abs(np.sin(w / 2)) < 1e-15, 1.0, g)


def ema(alpha, x, y0=0.0):
    """Exponential moving average y[n] = y[n-1] + alpha (x[n] - y[n-1]), starting from y[-1] = y0."""
    y = np.zeros(len(x))
    prev = y0
    for n, xn in enumerate(x):
        prev = prev + alpha * (xn - prev)
        y[n] = prev
    return y


def wrap(v, bits):
    """Signed two's-complement value of the integer v reduced to the given width."""
    m = 1 << bits
    v = int(v) % m
    return v - m if v >= m // 2 else v


def running_sum(x, N, bits=None):
    """Recursive moving sum s[n] = s[n-1] + x[n] - x[n-N] (from rest).

    With bits given, x must be integers and every addition and subtraction wraps to a signed accumulator of that
    width, as two's-complement hardware does. The intermediate s[n-1] + x[n] is wrapped before x[n-N] is
    subtracted. Returns (s, intermediates)."""
    s_prev = 0
    out, mids = [], []
    for n in range(len(x)):
        xo = x[n - N] if n - N >= 0 else 0
        mid = s_prev + x[n]
        if bits is not None:
            mid = wrap(mid, bits)
        s = mid - xo
        if bits is not None:
            s = wrap(s, bits)
        mids.append(mid)
        out.append(s)
        s_prev = s
    return np.array(out), np.array(mids)
