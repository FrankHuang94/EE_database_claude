"""Lab 15-04 helpers: system type, static error constants and simulated steady-state errors.

    system_type(num, den)            number of poles of L(s) at the origin
    error_constants(num, den)        (Kp, Kv, Ka) of a unity-feedback loop gain L = num/den
    ss_errors(num, den)              predicted steady-state errors to unit step, ramp and parabola
    simulate_error(num, den, kind)   the error e = r - y of the closed loop, simulated (an independent check)
    loop_from(C, P)                  polynomial product of controller and plant (num, den) pairs

Polynomials are coefficient lists, highest power first (numpy convention).
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal


def _trim(p):
    p = np.atleast_1d(np.asarray(p, dtype=float))
    nz = np.flatnonzero(np.abs(p) > 0)
    return p[nz[0]:] if nz.size else np.array([0.0])


def system_type(num, den):
    """Number of integrators (poles at s = 0) in L(s), after cancelling any zeros at the origin."""
    num, den = _trim(num), _trim(den)
    zn = 0
    while len(num) > 1 and num[-1] == 0:
        num, zn = num[:-1], zn + 1
    pd = 0
    while len(den) > 1 and den[-1] == 0:
        den, pd = den[:-1], pd + 1
    return pd - zn


def _limit_sk(num, den, k):
    """lim_{s->0} s^k L(s), returned as math.inf when it diverges."""
    num, den = _trim(num), _trim(den)
    n = system_type(num, den)
    if k < n:
        return math.inf
    if k > n:
        return 0.0
    num_r = np.trim_zeros(num, "b")
    den_r = np.trim_zeros(den, "b")
    return float(num_r[-1] / den_r[-1])


def error_constants(num, den):
    """Static error constants Kp = lim L, Kv = lim sL, Ka = lim s^2 L."""
    return tuple(_limit_sk(num, den, k) for k in range(3))


def ss_errors(num, den):
    """Steady-state errors to a unit step, unit ramp and unit parabola (t^2/2), for a stable unity loop."""
    Kp, Kv, Ka = error_constants(num, den)
    step = 0.0 if math.isinf(Kp) else 1 / (1 + Kp)
    ramp = 0.0 if math.isinf(Kv) else (math.inf if Kv == 0 else 1 / Kv)
    para = 0.0 if math.isinf(Ka) else (math.inf if Ka == 0 else 1 / Ka)
    return step, ramp, para


def closed_loop_error_tf(num, den):
    """E/R = 1/(1 + L) = den / (den + num)."""
    num, den = _trim(num), _trim(den)
    return den, np.polyadd(den, num)


def simulate_error(num, den, kind, t_end, n=200001):
    """Simulated error e(t) = r(t) - y(t) of the unity-feedback loop for a unit step, ramp or parabola."""
    en, ed = closed_loop_error_tf(num, den)
    t = np.linspace(0, t_end, n)
    r = {"step": np.ones_like(t), "ramp": t, "parabola": t**2 / 2}[kind]
    _, e, _ = signal.lsim(signal.TransferFunction(en, ed), r, t)
    return t, e


def loop_from(C, P):
    """Series connection of two (num, den) pairs."""
    return np.polymul(C[0], P[0]), np.polymul(C[1], P[1])


def is_stable(num, den):
    """True if every closed-loop pole of the unity loop lies in the open left half-plane."""
    return bool(np.all(np.roots(np.polyadd(_trim(den), _trim(num))).real < 0))
