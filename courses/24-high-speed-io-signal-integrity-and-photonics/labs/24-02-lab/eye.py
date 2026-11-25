"""Eye, jitter and BER models for chapter 24-02.

Closed forms from the chapter (Q function, dual-Dirac total jitter, bathtub, Q-scale fit, first-order
CDR jitter tolerance, zero-error test length, phase-noise jitter) plus numerical models: the pulse
response of a two-equal-pole channel, its cursors, peak-distortion eyes, a statistical NRZ eye built by
convolving the ISI distribution, and the tail of sinusoidal plus random jitter.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import special


# ---------------------------------------------------------------- Gaussian tails
def q(x):
    """Gaussian tail probability Q(x)."""
    return 0.5 * special.erfc(np.asarray(x, dtype=float) / math.sqrt(2))


def q_inv(p):
    """Inverse of Q: the x for which Q(x) = p."""
    return math.sqrt(2) * special.erfcinv(2 * np.asarray(p, dtype=float))


# ---------------------------------------------------------------- channel and eyes
def two_pole_step(t, tau):
    """Unit step response of two equal real poles: 1 - (1 + t/tau) exp(-t/tau) for t > 0."""
    t = np.asarray(t, dtype=float)
    return np.where(t > 0, 1 - (1 + t / tau) * np.exp(-np.clip(t, 0, None) / tau), 0.0)


def pulse(t, tau, ui=1.0):
    """Response to a rectangular pulse of width ui starting at t = 0."""
    return two_pole_step(t, tau) - two_pole_step(np.asarray(t, dtype=float) - ui, tau)


def cursors(tau_ui: float, n_pre: int = 1, n_post: int = 6, phase: float | None = None):
    """Cursors h_k of the two-pole channel (time in UI). Sampled at the pulse peak unless phase is given."""
    if phase is None:
        t = np.linspace(0, 4, 400001)
        phase = float(t[np.argmax(pulse(t, tau_ui))])
    ks = range(-n_pre, n_post + 1)
    return phase, {k: float(pulse(phase + k, tau_ui)) for k in ks}


def peak_distortion_eye(h: dict, levels: int = 2) -> float:
    """Worst-case eye as a fraction of the full swing: h0/(M-1) - sum |h_k|, k != 0."""
    isi = sum(abs(v) for k, v in h.items() if k != 0)
    return h[0] / (levels - 1) - isi


def isi_pdf(h: dict, grid: np.ndarray) -> np.ndarray:
    """Probability mass of the NRZ ISI sum on a uniform grid (random +/-1 data)."""
    dv = grid[1] - grid[0]
    pmf = np.zeros_like(grid)
    pmf[np.argmin(np.abs(grid))] = 1.0
    for k, hk in h.items():
        if k == 0 or hk == 0:
            continue
        shift = int(round(hk / dv))
        pmf = 0.5 * (np.roll(pmf, shift) + np.roll(pmf, -shift))
    return pmf


def stat_ber_nrz(h: dict, sigma: float, threshold: float = 0.0, dv: float = 1e-5) -> float:
    """BER of NRZ at a decision threshold, averaging over the ISI distribution (units of half the swing)."""
    span = sum(abs(v) for k, v in h.items() if k != 0) + 10 * dv
    grid = np.arange(-span, span + dv / 2, dv)
    grid -= grid[np.argmin(np.abs(grid))]
    pmf = isi_pdf(h, grid)
    one = np.sum(pmf * q((h[0] + grid - threshold) / sigma))
    zero = np.sum(pmf * q((h[0] - grid + threshold) / sigma))
    return float(0.5 * (one + zero))


# ---------------------------------------------------------------- jitter
def total_jitter(rj: float, dj: float, ber: float) -> float:
    """Dual-Dirac total jitter: 2 Q^-1(BER) RJ + DJ(dd)."""
    return 2 * float(q_inv(ber)) * rj + dj


def bathtub(x, ui: float, rj: float, dj: float):
    """Dual-Dirac bathtub: BER at sampling position x measured from the left crossing."""
    x = np.asarray(x, dtype=float)
    return q((x - dj / 2) / rj) + q((ui - x - dj / 2) / rj)


def qscale_fit(x1: float, ber1: float, x2: float, ber2: float) -> tuple[float, float]:
    """Fit a Q-scale line to two points on one bathtub wall: returns (sigma, DJ(dd))."""
    q1, q2 = float(q_inv(ber1)), float(q_inv(ber2))
    sigma = (x2 - x1) / (q2 - q1)
    return sigma, 2 * (x1 - q1 * sigma)


def sj_rj_tail(x, pj_pp: float, rj: float, n: int = 4001):
    """Probability that an edge lies beyond x for sinusoidal PJ (peak-to-peak pj_pp) plus Gaussian RJ."""
    phase = (np.arange(n) + 0.5) / n * 2 * np.pi
    u = 0.5 * pj_pp * np.sin(phase)
    x = np.atleast_1d(np.asarray(x, dtype=float))
    return np.array([np.mean(q((xi - u) / rj)) for xi in x])


def jitter_tolerance(f, fc: float, margin_ui: float):
    """First-order CDR: tolerable sinusoidal jitter amplitude M sqrt(1 + (fc/f)^2)."""
    f = np.asarray(f, dtype=float)
    return margin_ui * np.sqrt(1 + (fc / f) ** 2)


def tracking_error_ratio(f, fc: float):
    """|1 - H(f)| for a first-order CDR."""
    r = np.asarray(f, dtype=float) / fc
    return r / np.sqrt(1 + r * r)


def cdr_tracking_sim(f_jit: float, fc: float, amp: float = 1.0, cycles: int = 40, steps: int = 4000):
    """Integrate a first-order loop d(phi_c)/dt = 2 pi fc (phi_d - phi_c) under sinusoidal input.

    Returns the peak tracking error over the last quarter of the run, relative to amp.
    """
    t_end = cycles / f_jit
    t_end = max(t_end, 20 / fc)
    n = int(steps * t_end * f_jit) + steps
    dt = t_end / n
    phi_c = 0.0
    err = np.empty(n)
    w, k = 2 * np.pi * f_jit, 2 * np.pi * fc
    for i in range(n):
        t = i * dt
        # midpoint (RK2) step
        e1 = amp * math.sin(w * t) - phi_c
        mid = phi_c + 0.5 * dt * k * e1
        e2 = amp * math.sin(w * (t + 0.5 * dt)) - mid
        phi_c += dt * k * e2
        err[i] = e1
    return float(np.max(np.abs(err[3 * n // 4:])) / amp)


# ---------------------------------------------------------------- testing and clocks
def zero_error_bits(ber: float, confidence: float = 0.95) -> float:
    return -math.log(1 - confidence) / ber


def phase_noise_jitter(l_dbc: float, f1: float, f2: float, f0: float) -> float:
    """RMS jitter (s) of a flat phase-noise level l_dbc (dBc/Hz) from f1 to f2, both sidebands."""
    return math.sqrt(2 * 10 ** (l_dbc / 10) * (f2 - f1)) / (2 * math.pi * f0)


def com_db(a_s: float, a_ni: float) -> float:
    return 20 * math.log10(a_s / a_ni)
