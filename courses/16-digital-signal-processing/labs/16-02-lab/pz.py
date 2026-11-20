"""Pole-zero design helpers for Lab 16-02.

Conventions: b and a are coefficient lists in powers of z^-1, H(z) = (b0 + b1 z^-1 + ...)/(a0 + a1 z^-1 + ...).
Frequencies w are in rad/sample.

Functions
- freq_resp(b, a, w)              H(e^jw) evaluated directly from the coefficients
- zpk(b, a)                       zeros, poles and gain k such that H(z) = k * prod(1 - z_i z^-1) / prod(1 - p_i z^-1)
- geometric(zeros, poles, k, w)   the same H(e^jw) from vectors e^jw - z_i and e^jw - p_i (section 3.2)
- group_delay(b, a, w)            -d(phase)/dw, as a sum of the closed-form delays of each zero and pole
- group_delay_numeric(b, a, w)    the same by differentiating the unwrapped phase on a fine grid
- notch(w0, r), resonator(w0, r), dc_blocker(a), allpass1(a)
- minimum_phase_fir(b)            reflect every zero outside the unit circle inside, keeping |H|
- partial_energy(h)               cumulative energy sum_{k<=n} h[k]^2
- anticausal_inverse(c0, c1, K)   K-tap delayed FIR inverse of the max-phase channel c0 + c1 z^-1 (|c0| < |c1|)
"""
from __future__ import annotations

import numpy as np


def freq_resp(b, a, w):
    w = np.atleast_1d(np.asarray(w, float))
    zi = np.exp(-1j * w)
    num = sum(bk * zi**k for k, bk in enumerate(b))
    den = sum(ak * zi**k for k, ak in enumerate(a))
    return num / den


def zpk(b, a):
    """Zeros and poles from the coefficient lists (in z^-1), and the gain b0/a0."""
    b, a = np.trim_zeros(np.asarray(b, complex), "b"), np.trim_zeros(np.asarray(a, complex), "b")
    return np.roots(b), np.roots(a), (b[0] / a[0]).real if abs((b[0] / a[0]).imag) < 1e-15 else b[0] / a[0]


def geometric(zeros, poles, k, w):
    """H(e^jw) = k * prod(e^jw - z_i) / prod(e^jw - p_i) * e^{-jw(nz - np)}, the vector form of section 3.2."""
    w = np.atleast_1d(np.asarray(w, float))
    e = np.exp(1j * w)
    num = np.prod([e - z for z in zeros], axis=0) if len(zeros) else np.ones_like(e)
    den = np.prod([e - p for p in poles], axis=0) if len(poles) else np.ones_like(e)
    return k * num / den * np.exp(-1j * w * (len(zeros) - len(poles)))


def _root_delay(c, w):
    """Group delay of the factor (1 - c e^{-jw}): (|c|^2 - Re(c e^{-jw})) / |1 - c e^{-jw}|^2."""
    q = c * np.exp(-1j * w)
    return (abs(c) ** 2 - q.real) / np.abs(1 - q) ** 2


def group_delay(b, a, w):
    w = np.atleast_1d(np.asarray(w, float))
    zeros, poles, _ = zpk(b, a)
    tau = np.zeros_like(w)
    for z in zeros:
        tau += _root_delay(z, w)
    for p in poles:
        tau -= _root_delay(p, w)
    return tau


def group_delay_numeric(b, a, w, dw=1e-6):
    w = np.atleast_1d(np.asarray(w, float))
    p1 = np.angle(freq_resp(b, a, w + dw) / freq_resp(b, a, w - dw))
    return -p1 / (2 * dw)


def notch(w0, r):
    """Zeros on the unit circle at +-w0, poles at r e^{+-jw0}; scaled to unit gain at DC."""
    b = np.array([1.0, -2 * np.cos(w0), 1.0])
    a = np.array([1.0, -2 * r * np.cos(w0), r * r])
    g = abs(freq_resp(b, a, 0.0)[0])
    return b / g, a


def resonator(w0, r):
    """Poles at r e^{+-jw0}, zeros at z = +1 and -1 (no response at DC or at Nyquist)."""
    return np.array([1.0, 0.0, -1.0]), np.array([1.0, -2 * r * np.cos(w0), r * r])


def dc_blocker(a):
    return np.array([1.0, -1.0]), np.array([1.0, -a])


def allpass1(a):
    """First-order all-pass (z^-1 - a)/(1 - a z^-1) for real |a| < 1."""
    return np.array([-a, 1.0]), np.array([1.0, -a])


def minimum_phase_fir(b):
    """FIR with every zero outside the unit circle reflected to 1/z*, scaled so |H| is unchanged."""
    zeros, _, k = zpk(b, [1.0])
    gain = k
    new = []
    for z in zeros:
        if abs(z) > 1:
            new.append(1 / np.conj(z))
            gain = gain * (-z)   # (1 - z q) = -z (q - 1/z): magnitude |z| |1 - q / z| ... kept as a complex factor
        else:
            new.append(z)
    h = np.poly(new) * gain
    if np.allclose(np.imag(h), 0):
        h = np.real(h)
        if h[0] < 0:          # a constant sign does not change |H|; present h[0] > 0
            h = -h
    return h


def partial_energy(h):
    return np.cumsum(np.abs(np.asarray(h)) ** 2)


def anticausal_inverse(c0, c1, K):
    """Taps e[0..K-1] of the delayed, truncated inverse of c0 + c1 z^-1 with |c0| < |c1| (zero outside the circle).

    1/(c0 + c1 z^-1) = (z/c1) / (1 + (c0/c1) z) = (1/c1) sum_k (-c0/c1)^k z^(k+1): future samples. Delaying by K
    makes it causal: e[n] = (1/c1) (-c0/c1)^(K-1-n) for n = 0..K-1, and channel * e has its main tap at n = K."""
    rho = -c0 / c1
    return np.array([(1 / c1) * rho ** (K - 1 - n) for n in range(K)])
