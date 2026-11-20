"""Filter-structure toolkit for Lab 16-08: one transfer function, many implementations.

Every structure below computes y[n] for the same H(z) = B(z)/A(z) (a[0] = 1) sample by sample, exposing its internal
state so that headroom, round-off and sensitivity can be studied. All arithmetic is float unless stated.

Functions
- fir_direct(h, x)                 tapped-delay-line FIR (adder chain after the multipliers)
- fir_transposed(h, x)             transposed FIR (each multiplier feeds an adder in a chain of delays)
- df1(b, a, x)                     Direct Form I: feed-forward on x, then feedback on y; states are past x and y
- df2(b, a, x)                     Direct Form II: w = x/A first, then y = B w; returns (y, w) so w can be inspected
- df2t(b, a, x)                    transposed Direct Form II; returns (y, states)
- sos_filter(sos, x)               cascade of second-order sections, each in Direct Form I
- counts(structure, N)             (multipliers, two-input adders, delays) for an order-N filter
- critical_path(taps, t_mul, t_add, transposed)   longest register-to-register path of an FIR (direct form uses
                                   a linear adder chain)
- poly_to_lattice(a)               reflection coefficients k_1..k_N of A(z) by the step-down recursion
- lattice_to_poly(k)               A(z) from reflection coefficients by the step-up recursion
- biquad_df1_fixed(x, coef, frac=14, width=16)   bit-exact model of biquad_df1.v: integer coefficients in Q2.frac,
                                   products summed exactly, rounded (add 2^(frac-1), arithmetic shift), saturated to
                                   `width` bits; the saturated output is what is fed back. Returns (y, saturation count)
"""
from __future__ import annotations

import numpy as np


def fir_direct(h, x):
    h = np.asarray(h, dtype=float)
    d = np.zeros(len(h))
    y = np.zeros(len(x))
    for n, xn in enumerate(x):
        d = np.roll(d, 1)
        d[0] = xn
        acc = 0.0
        for k in range(len(h)):  # the adder chain
            acc = acc + h[k] * d[k]
        y[n] = acc
    return y


def fir_transposed(h, x):
    h = np.asarray(h, dtype=float)
    M = len(h) - 1
    s = np.zeros(M + 1)  # s[k] is the register after adder k; s[M] is unused
    y = np.zeros(len(x))
    for n, xn in enumerate(x):
        y[n] = h[0] * xn + s[0]
        for k in range(M - 1):
            s[k] = h[k + 1] * xn + s[k + 1]
        if M >= 1:
            s[M - 1] = h[M] * xn
    return y


def df1(b, a, x):
    b, a = np.asarray(b, float), np.asarray(a, float)
    xs = np.zeros(len(b))
    ys = np.zeros(len(a) - 1)
    y = np.zeros(len(x))
    for n, xn in enumerate(x):
        xs = np.roll(xs, 1)
        xs[0] = xn
        yn = b @ xs - a[1:] @ ys
        ys = np.roll(ys, 1)
        if len(ys):
            ys[0] = yn
        y[n] = yn
    return y


def df2(b, a, x):
    b, a = np.asarray(b, float), np.asarray(a, float)
    N = max(len(a), len(b)) - 1
    b = np.r_[b, np.zeros(N + 1 - len(b))]
    a = np.r_[a, np.zeros(N + 1 - len(a))]
    w = np.zeros(N + 1)
    y = np.zeros(len(x))
    wt = np.zeros(len(x))
    for n, xn in enumerate(x):
        w = np.roll(w, 1)
        w[0] = xn - a[1:] @ w[1:]
        wt[n] = w[0]
        y[n] = b @ w
    return y, wt


def df2t(b, a, x):
    b, a = np.asarray(b, float), np.asarray(a, float)
    N = max(len(a), len(b)) - 1
    b = np.r_[b, np.zeros(N + 1 - len(b))]
    a = np.r_[a, np.zeros(N + 1 - len(a))]
    s = np.zeros(N + 1)
    y = np.zeros(len(x))
    st = np.zeros((len(x), N))
    for n, xn in enumerate(x):
        yn = b[0] * xn + s[0]
        for k in range(N - 1):
            s[k] = b[k + 1] * xn - a[k + 1] * yn + s[k + 1]
        s[N - 1] = b[N] * xn - a[N] * yn
        y[n] = yn
        st[n] = s[:N]
    return y, st


def sos_filter(sos, x):
    y = np.asarray(x, float)
    for sec in np.atleast_2d(sos):
        y = df1(sec[:3], sec[3:], y)
    return y


def counts(structure, N):
    """(multipliers, two-input adders, delays) for an order-N IIR filter with N + 1 numerator and N denominator
    coefficients; 'cascade' assumes N even and N/2 biquads with 5 multipliers each."""
    if structure == "df1":
        return 2 * N + 1, 2 * N, 2 * N
    if structure in ("df2", "df2t"):
        return 2 * N + 1, 2 * N, N
    if structure == "cascade":
        return 5 * (N // 2), 4 * (N // 2), 2 * (N // 2)
    raise ValueError(structure)


def critical_path(taps, t_mul, t_add, transposed):
    return t_mul + t_add if transposed else t_mul + (taps - 1) * t_add


def poly_to_lattice(a):
    """Reflection coefficients of A(z) = 1 + a1 z^-1 + ... + aN z^-N (step-down; A_m = A_{m-1} + k_m z^-m A_{m-1}(1/z))."""
    a = np.asarray(a, float)
    assert abs(a[0] - 1) < 1e-12
    cur = a[1:].copy()
    k = np.zeros(len(cur))
    for m in range(len(cur), 0, -1):
        km = cur[m - 1]
        k[m - 1] = km
        if m == 1:
            break
        prev = (cur[: m - 1] - km * cur[m - 2::-1]) / (1 - km * km)
        cur = prev
    return k


def lattice_to_poly(k):
    a = np.array([1.0])
    for km in k:
        ext = np.r_[a, 0.0]
        a = ext + km * ext[::-1]
    return a


def biquad_df1_fixed(x, coef, frac=14, width=16):
    b0, b1, b2, a1, a2 = (int(c) for c in coef)
    lo, hi = -(1 << (width - 1)), (1 << (width - 1)) - 1
    x1 = x2 = y1 = y2 = 0
    y, sat = [], 0
    for xn in x:
        xn = int(xn)
        acc = b0 * xn + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        yn = (acc + (1 << (frac - 1))) >> frac
        if yn > hi or yn < lo:
            sat += 1
            yn = hi if yn > hi else lo
        x2, x1 = x1, xn
        y2, y1 = y1, yn
        y.append(yn)
    return y, sat
