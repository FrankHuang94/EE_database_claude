"""Lab 21-05 helpers: switching mixers, harmonic responses, image rejection and harmonic-reject mixing.

A commutating (double-balanced) mixer multiplies the input by a square wave s(t) = sign(cos w_LO t), whose
Fourier series is (4/pi) [cos x - cos 3x / 3 + cos 5x / 5 - ...]; each LO harmonic n mixes the input at
n f_LO +/- f_IF down to f_IF with voltage conversion gain 2/(n pi) (odd n only).
"""
from __future__ import annotations

import math

import numpy as np


def conversion_gain_square(n=1):
    """Voltage conversion gain of an ideal commutating mixer for the n-th LO harmonic (odd n): 2/(n pi)."""
    return 0.0 if n % 2 == 0 else 2 / (n * math.pi)


def conversion_gain_db(n=1):
    g = conversion_gain_square(n)
    return 20 * math.log10(g) if g else -math.inf


def irr_db(eps, theta_deg):
    """Image-rejection ratio of a Hartley/quadrature receiver with relative gain error eps and phase error theta:
    IRR = (1 + 2(1+eps)cos(theta) + (1+eps)^2) / (1 - 2(1+eps)cos(theta) + (1+eps)^2)."""
    a = 1 + eps
    th = math.radians(theta_deg)
    return 10 * math.log10((1 + 2 * a * math.cos(th) + a * a) / (1 - 2 * a * math.cos(th) + a * a))


def irr_small_db(eps, theta_deg):
    """Small-error approximation IRR = 4 / (eps^2 + theta^2)."""
    th = math.radians(theta_deg)
    return 10 * math.log10(4 / (eps * eps + th * th))


def hr_weights():
    """Harmonic-reject mixer with three square-wave LO phases at -45, 0 and +45 degrees weighted 1 : sqrt(2) : 1;
    the composite LO has no 3rd or 5th harmonic."""
    return [(-45.0, 1.0), (0.0, math.sqrt(2)), (45.0, 1.0)]


def composite_lo_harmonics(weights, nmax=9, npts=1 << 14):
    """Harmonic amplitudes (relative to the fundamental) of a weighted sum of phase-shifted square waves, by FFT."""
    t = np.arange(npts) / npts
    lo = sum(w * np.sign(np.cos(2 * np.pi * t - math.radians(ph))) for ph, w in weights)
    spec = np.abs(np.fft.rfft(lo)) / npts * 2
    return {n: spec[n] / spec[1] for n in range(1, nmax + 1)}


def ssb_nf_from_dsb(nf_dsb_db):
    """A mixer measured with noise at both the signal and image bands (DSB) looks 3 dB better than when only one
    band carries signal (SSB): NF_SSB ~ NF_DSB + 3 dB for equal responses."""
    return nf_dsb_db + 10 * math.log10(2)
