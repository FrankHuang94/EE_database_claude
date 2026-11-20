"""Matched filtering and optimal detection: helpers for the 17-05 lab.

- calibrated continuous-time white noise on a sample grid (two-sided PSD N0/2 -> variance N0/(2 dt));
- matched filtering and correlation, with energy and inner products as numerical integrals;
- numerical Gram-Schmidt for sampled waveforms;
- ML and MAP decisions in signal space; Monte Carlo error rates for constellations;
- closed-form error probabilities (binary, M-PAM), union and nearest-neighbour bounds;
- a linear chirp and its pulse compression.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.stats import norm

Q = norm.sf
Qinv = norm.isf


# ------------------------------------------------------------------ continuous-time helpers on a grid
def white_noise(n, n0, dt, rng):
    """Samples of white noise with two-sided PSD N0/2 seen through a grid of spacing dt: variance N0/(2 dt)."""
    return rng.standard_normal(n) * math.sqrt(n0 / (2 * dt))


def energy(s, dt):
    return float(np.sum(np.asarray(s) ** 2) * dt)


def inner(a, b, dt):
    return float(np.dot(a, b) * dt)


def matched_filter_output(r, s, dt):
    """Output of the filter h(t) = s(T - t) for all times (full convolution), in continuous-time units."""
    return np.convolve(r, s[::-1]) * dt


def correlate(r, s, dt):
    """Correlator output int r s dt (the matched filter sampled at T)."""
    return inner(r, s, dt)


def mf_peak_snr_mc(s, n0, dt, trials, rng):
    """Monte Carlo: mean^2 / variance of the correlator output with the pulse present, against 2E/N0."""
    e = energy(s, dt)
    y = np.array([correlate(s + white_noise(len(s), n0, dt, rng), s, dt) for _ in range(trials)])
    return float(np.mean(y) ** 2 / np.var(y)), 2 * e / n0


def one_pole_ratio(x):
    """SNR of a one-pole filter (time constant tau, x = T/tau) on a rectangular pulse, relative to 2E/N0."""
    return 2 * (1 - math.exp(-x)) ** 2 / x


# ------------------------------------------------------------------ signal space
def gram_schmidt(signals, dt, tol=1e-9):
    """Orthonormal basis (rows) for sampled waveforms; signals already in the span are skipped."""
    basis = []
    for s in signals:
        v = np.array(s, dtype=float)
        for b in basis:
            v = v - inner(v, b, dt) * b
        e = energy(v, dt)
        if e > tol:
            basis.append(v / math.sqrt(e))
    return np.array(basis)


def coordinates(signals, basis, dt):
    return np.array([[inner(s, b, dt) for b in basis] for s in signals])


def ml_decide(r, points):
    """Index of the nearest constellation point for each received vector (rows of r)."""
    d2 = ((r[:, None, :] - points[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(d2, axis=1)


def map_decide(r, points, priors, n0):
    """MAP: minimize |r - s_i|^2 - N0 ln P_i."""
    d2 = ((r[:, None, :] - points[None, :, :]) ** 2).sum(axis=2) - n0 * np.log(np.asarray(priors))[None, :]
    return np.argmin(d2, axis=1)


def simulate_ser(points, n0, nsym, rng, priors=None, rule="ml"):
    """Monte Carlo symbol-error rate of a constellation (rows of points) in AWGN with variance N0/2 per dimension."""
    points = np.asarray(points, dtype=float)
    m, dim = points.shape
    p = np.full(m, 1 / m) if priors is None else np.asarray(priors, dtype=float)
    idx = rng.choice(m, nsym, p=p)
    r = points[idx] + rng.standard_normal((nsym, dim)) * math.sqrt(n0 / 2)
    dec = ml_decide(r, points) if rule == "ml" else map_decide(r, points, p, n0)
    return float(np.mean(dec != idx))


# ------------------------------------------------------------------ closed forms
def pe_pair(d, n0):
    """Error probability between two points at distance d: Q(d / sqrt(2 N0))."""
    return float(Q(d / math.sqrt(2 * n0)))


def ber_bpsk(ebn0):
    return float(Q(math.sqrt(2 * ebn0)))


def ber_orthogonal(ebn0):
    return float(Q(math.sqrt(ebn0)))


def ser_pam(m, esn0):
    return float(2 * (m - 1) / m * Q(math.sqrt(6 * esn0 / (m * m - 1))))


def union_bound(points, n0):
    """Average over points of the sum of pairwise Q(d/sqrt(2N0))."""
    points = np.asarray(points, dtype=float)
    m = len(points)
    tot = 0.0
    for i in range(m):
        for k in range(m):
            if k != i:
                tot += pe_pair(float(np.linalg.norm(points[i] - points[k])), n0)
    return tot / m


def nearest_neighbour(points, n0):
    points = np.asarray(points, dtype=float)
    d = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    dmin = d.min()
    nmin = np.mean(np.sum(np.isclose(d, dmin), axis=1))
    return float(nmin * Q(dmin / math.sqrt(2 * n0)))


# ------------------------------------------------------------------ pulse compression
def chirp(duration, bandwidth, fs):
    """Complex baseband linear chirp sweeping -B/2..+B/2 over the duration."""
    t = np.arange(int(round(duration * fs))) / fs
    k = bandwidth / duration
    return np.exp(1j * np.pi * k * (t - duration / 2) ** 2)


def compress(r, ref):
    """Matched-filter (correlate) a complex signal with a reference pulse."""
    return np.convolve(r, np.conj(ref[::-1]))


def mainlobe_width(y, fs, level=0.5):
    """Width of the main lobe of |y| at `level` of its peak (in seconds)."""
    a = np.abs(y) / np.abs(y).max()
    k = int(np.argmax(a))
    lo = k
    while lo > 0 and a[lo] >= level:
        lo -= 1
    hi = k
    while hi < len(a) - 1 and a[hi] >= level:
        hi += 1
    return (hi - lo - 1) / fs
