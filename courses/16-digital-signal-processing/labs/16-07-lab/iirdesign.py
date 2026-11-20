"""IIR filter-design toolkit for Lab 16-07: analog prototypes, the bilinear transform and biquad sections.

Conventions. Digital frequencies w are in rad/sample (0 to pi); analog frequencies W in rad/s. The bilinear transform
is s = 2 fs (z - 1)/(z + 1), so a digital frequency w corresponds to the analog frequency W = 2 fs tan(w/2).
Filters are kept as zeros, poles and gain (z, p, k) and converted to second-order sections (SOS) at the end.

Functions
- prewarp(f, fs)                    analog frequency (rad/s) that the bilinear transform maps to f (Hz)
- unwarp(W, fs)                     digital frequency (Hz) that an analog frequency W (rad/s) lands on
- discrimination(Ap, As)            D = (10^(As/10) - 1)/(10^(Ap/10) - 1)
- order_butter(Ap, As, Wp, Ws)      real-valued order bound for Butterworth (round up)
- order_cheb(Ap, As, Wp, Ws)        real-valued order bound for Chebyshev type I or II
- order_ellip(Ap, As, Wp, Ws)       real-valued order bound for elliptic, from complete elliptic integrals
- butter_analog(N, Ap, Wp)          (z, p, k) of an analog Butterworth low-pass meeting Ap exactly at Wp
- cheb1_analog(N, Ap, Wp)           (z, p, k) of an analog Chebyshev type I low-pass with ripple Ap up to Wp
- bilinear(z, p, k, fs)             map an analog (z, p, k) to digital: each root r -> (2fs + r)/(2fs - r),
                                    zeros at infinity -> z = -1, gain k * prod(2fs - z)/prod(2fs - p)
- response(z, p, k, w)              complex frequency response of a digital (z, p, k) at w (rad/sample)
- group_delay(z, p, w)              group delay in samples, summed root by root (16-02)
- impulse_invariant_first_order(fc, fs)   (b, a) of a first-order low-pass by impulse invariance
- bilinear_first_order(fc, fs, prewarped) (b, a) of a first-order low-pass by the bilinear transform
- butter2_biquad(fc, fs)            (b, a) of the prewarped second-order Butterworth low-pass, by the closed form
- mults_sos(sos)                    multiplications per output of a cascade of sections (zero and power-of-two
                                    coefficients are shifts, so free)
"""
from __future__ import annotations

import math

import numpy as np
from scipy.special import ellipk


def prewarp(f, fs):
    return 2 * fs * math.tan(math.pi * f / fs)


def unwarp(W, fs):
    return fs / math.pi * math.atan(W / (2 * fs))


def discrimination(Ap, As):
    return (10 ** (As / 10) - 1) / (10 ** (Ap / 10) - 1)


def order_butter(Ap, As, Wp, Ws):
    return math.log10(discrimination(Ap, As)) / (2 * math.log10(Ws / Wp))


def order_cheb(Ap, As, Wp, Ws):
    return math.acosh(math.sqrt(discrimination(Ap, As))) / math.acosh(Ws / Wp)


def order_ellip(Ap, As, Wp, Ws):
    k = Wp / Ws
    k1 = 1 / math.sqrt(discrimination(Ap, As))
    # scipy's ellipk takes the parameter m = k^2
    return ellipk(k**2) * ellipk(1 - k1**2) / (ellipk(k1**2) * ellipk(1 - k**2))


def butter_analog(N, Ap, Wp):
    Wc = Wp / (10 ** (Ap / 10) - 1) ** (1 / (2 * N))
    kk = np.arange(1, N + 1)
    p = Wc * np.exp(1j * np.pi * (2 * kk + N - 1) / (2 * N))
    return np.array([]), p, float(np.real(np.prod(-p)))


def cheb1_analog(N, Ap, Wp):
    eps = math.sqrt(10 ** (Ap / 10) - 1)
    a = math.asinh(1 / eps) / N
    th = (2 * np.arange(1, N + 1) - 1) * np.pi / (2 * N)
    p = Wp * (-math.sinh(a) * np.sin(th) + 1j * math.cosh(a) * np.cos(th))
    k = float(np.real(np.prod(-p)))
    if N % 2 == 0:
        k /= math.sqrt(1 + eps**2)
    return np.array([]), p, k


def bilinear(z, p, k, fs):
    z = np.asarray(z, dtype=complex)
    p = np.asarray(p, dtype=complex)
    c = 2 * fs
    zd = (c + z) / (c - z)
    pd = (c + p) / (c - p)
    zd = np.concatenate([zd, -np.ones(len(p) - len(z))])
    kd = k * np.real(np.prod(c - z) / np.prod(c - p))
    return zd, pd, float(kd)


def response(z, p, k, w):
    e = np.exp(1j * np.atleast_1d(np.asarray(w, dtype=float)))
    num = np.ones_like(e) * k
    for r in z:
        num = num * (1 - r / e)
    den = np.ones_like(e)
    for r in p:
        den = den * (1 - r / e)
    return num / den


def _root_delay(r, w):
    """Group delay (samples) of a factor (1 - r e^{-jw}); a root on the unit circle contributes exactly 1/2."""
    rho, th = abs(r), np.angle(r)
    if abs(rho - 1) < 1e-12:
        return 0.5 * np.ones_like(w)
    return (rho**2 - rho * np.cos(w - th)) / (1 - 2 * rho * np.cos(w - th) + rho**2)


def group_delay(z, p, w):
    """Group delay in samples of a digital (z, p, k): zeros add their factor's delay, poles subtract theirs."""
    w = np.atleast_1d(np.asarray(w, dtype=float))
    tau = np.zeros_like(w)
    for r in z:
        tau += _root_delay(r, w)
    for r in p:
        tau -= _root_delay(r, w)
    return tau


def impulse_invariant_first_order(fc, fs):
    a = 2 * math.pi * fc / fs
    return np.array([a]), np.array([1.0, -math.exp(-a)])


def bilinear_first_order(fc, fs, prewarped=True):
    K = math.tan(math.pi * fc / fs) if prewarped else math.pi * fc / fs
    return np.array([K, K]) / (1 + K), np.array([1.0, (K - 1) / (1 + K)])


def butter2_biquad(fc, fs):
    K = math.tan(math.pi * fc / fs)
    a0 = 1 + math.sqrt(2) * K + K**2
    b = np.array([K**2, 2 * K**2, K**2]) / a0
    a = np.array([1.0, 2 * (K**2 - 1) / a0, (1 - math.sqrt(2) * K + K**2) / a0])
    return b, a


def _free(c, tol=1e-9):
    """True for coefficients that cost no multiplier: exactly 0, or a signed power of two (1, 2, 0.5, ...): a shift."""
    if c == 0:
        return True
    e = math.log2(abs(c))
    return abs(e - round(e)) < tol


def mults_sos(sos):
    """Multiplications per output of a cascade of sections; zero and power-of-two coefficients are free."""
    return sum(0 if _free(c) else 1 for sec in np.atleast_2d(sos) for c in list(sec[:3]) + list(sec[4:]))
