"""SerDes models for chapter 24-03.

Cursor convolution and zero-forcing transmitter FFE design under a peak-swing constraint; peak-distortion
eyes; the source-degenerated CTLE; DFE residuals, error propagation (analytic and simulated) and sign-sign
LMS adaptation; bang-bang phase-detector gain and a bang-bang CDR with proportional and integral paths;
driver power; NRZ/PAM4 break-even loss.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import special


def q(x):
    return 0.5 * special.erfc(np.asarray(x, dtype=float) / math.sqrt(2))


# ---------------------------------------------------------------- FFE and eyes
def convolve_cursors(c: dict, h: dict) -> dict:
    """g_k = sum_j c_j h_{k-j} for tap and cursor dictionaries indexed by lag."""
    g: dict = {}
    for j, cj in c.items():
        for k, hk in h.items():
            g[k + j] = g.get(k + j, 0.0) + cj * hk
    return g


def zf_ffe(h: dict, pre: int, post: int) -> dict:
    """Zero-forcing TX FFE with taps -pre..post, forcing g_j = 0 for the other lags in that span and
    sum|c_j| = 1, assuming the main tap is positive and all others negative."""
    lags = list(range(-pre, post + 1))
    n = len(lags)
    a = np.zeros((n, n))
    b = np.zeros(n)
    row = 0
    for k in lags:
        if k == 0:
            continue
        for col, j in enumerate(lags):
            a[row, col] = h.get(k - j, 0.0)
        row += 1
    a[row, :] = [1.0 if j == 0 else -1.0 for j in lags]
    b[row] = 1.0
    c = np.linalg.solve(a, b)
    return dict(zip(lags, c))


def isi(g: dict, skip=(0,)) -> float:
    return sum(abs(v) for k, v in g.items() if k not in skip)


def eye(g: dict, levels: int = 2, skip=(0,)) -> float:
    """Peak-distortion eye as a fraction of the swing, ignoring the lags in skip (e.g. those a DFE cancels)."""
    return g[0] / (levels - 1) - isi(g, skip)


# ---------------------------------------------------------------- CTLE
def ctle(f, gm: float, rd: float, rs: float, cs: float, cl: float):
    """Magnitude of the source-degenerated CTLE, zero 1/(Rs Cs), poles (1 + gm Rs/2)/(Rs Cs) and 1/(Rd Cl)."""
    s = 2j * np.pi * np.asarray(f, dtype=float)
    return np.abs(gm * rd * (1 + s * rs * cs) / ((1 + gm * rs / 2 + s * rs * cs) * (1 + s * rd * cl)))


# ---------------------------------------------------------------- DFE
def p_continue(h0: float, h1: float, sigma: float) -> float:
    """Probability that a one-tap NRZ DFE error is followed by another."""
    return float(0.5 * q((h0 - 2 * h1) / sigma) + 0.5 * q((h0 + 2 * h1) / sigma))


def simulate_dfe(h0: float, h1: float, sigma: float, n: int, seed: int = 1):
    """NRZ through y_n = h0 a_n + h1 a_{n-1} + noise with a one-tap DFE (b1 = h1).

    Returns (error rate, probability of an error given an error on the previous symbol)."""
    rng = np.random.default_rng(seed)
    a = rng.choice((-1.0, 1.0), size=n)
    noise = rng.normal(0.0, sigma, size=n)
    err = np.zeros(n, dtype=bool)
    prev_dec = 1.0
    prev_a = 1.0
    for i in range(n):
        y = h0 * a[i] + h1 * prev_a + noise[i] - h1 * prev_dec
        dec = 1.0 if y >= 0 else -1.0
        err[i] = dec != a[i]
        prev_dec, prev_a = dec, a[i]
    pairs = np.sum(err[1:] & err[:-1])
    return float(err.mean()), float(pairs / max(1, np.sum(err[:-1])))


def lms_dfe(h: dict, sigma: float, ntaps: int, mu: float, n: int, seed: int = 2):
    """Sign-sign LMS adaptation of ntaps DFE taps and the data level h0, on NRZ through cursors h.

    Returns the tap history (n x ntaps) and the data-level history."""
    rng = np.random.default_rng(seed)
    lags = sorted(h)
    pad = max(lags) + 1
    a = rng.choice((-1.0, 1.0), size=n + pad)
    b = np.zeros(ntaps)
    lev = 0.5
    taps = np.empty((n, ntaps))
    levs = np.empty(n)
    dec_hist = np.ones(ntaps)
    for i in range(pad, n + pad):
        y = sum(h[k] * a[i - k] for k in lags if 0 <= i - k < n + pad) + rng.normal(0.0, sigma)
        z = y - np.dot(b, dec_hist)
        d = 1.0 if z >= 0 else -1.0
        e = z - lev * d
        b += mu * np.sign(e) * dec_hist
        lev += mu * np.sign(e) * d
        dec_hist = np.roll(dec_hist, 1)
        dec_hist[0] = d
        taps[i - pad] = b
        levs[i - pad] = lev
    return taps, levs


# ---------------------------------------------------------------- CDR
def bb_gain(sigma: float) -> float:
    """Linearized bang-bang detector gain sqrt(2/pi)/sigma, per UI of phase error."""
    return math.sqrt(2 / math.pi) / sigma


def bb_bandwidth(step: float, rho: float, sigma: float, f_baud: float) -> float:
    return step * rho * bb_gain(sigma) * f_baud / (2 * math.pi)


def bb_cdr(offset_ppm: float, step: float, ki: float, sigma: float, n: int, rho: float = 0.5, seed: int = 3):
    """Bang-bang CDR, one vote per transition: phase += step*vote + integrator; integrator += ki*vote.

    Returns (phase-error history in UI, integrator history in UI per UI)."""
    rng = np.random.default_rng(seed)
    drift = offset_ppm * 1e-6
    phi_d = 0.0
    phi_c = 0.0
    integ = 0.0
    errs = np.empty(n)
    ints = np.empty(n)
    for i in range(n):
        phi_d += drift
        phi_c += integ
        if rng.random() < rho:
            vote = 1.0 if (phi_d - phi_c + rng.normal(0.0, sigma)) >= 0 else -1.0
            phi_c += step * vote
            integ += ki * vote
        errs[i] = phi_d - phi_c
        ints[i] = integ
    return errs, ints


# ---------------------------------------------------------------- drivers and modulation
def cml_power(v_pp: float, v_dd: float) -> float:
    return v_dd * v_pp / 50.0


def sst_power(v_pp: float, v_dd: float | None = None) -> float:
    """Voltage-mode driver power: V_pp^2/200 from an ideal supply, or V_dd V_pp/200 through a regulator."""
    return v_pp * v_pp / 200.0 if v_dd is None else v_dd * v_pp / 200.0


def pam4_break_even(alpha: float) -> float:
    """Loss at the PAM4 Nyquist frequency above which PAM4 beats NRZ (alpha = conductor fraction)."""
    return 20 * math.log10(3) / (alpha * (math.sqrt(2) - 1) + 1 - alpha)
