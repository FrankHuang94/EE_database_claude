"""Lab 15-11 helpers: sampled-data control with a zero-order hold.

    zoh(num, den, T)                 exact ZOH-equivalent discrete transfer function (numz, denz)
    tustin(num, den, T, w_p=None)    bilinear (Tustin) discretization, optionally prewarped at w_p rad/s
    pi_tustin(Kp, Ki, T)             difference-equation coefficients of a Tustin PI controller
    sampled_loop(plant, ctrl, T, ...) closed-loop step response of a continuous plant under a discrete
                                     controller and ZOH, exact at and between samples
    dmargins(numz, denz, T)          crossover, phase and gain margins of a discrete loop gain on the unit circle
    jury2(a1, a0)                    stability of z^2 + a1 z + a0 by the second-order Jury conditions

Polynomials are highest power first; discrete transfer functions are in powers of z.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal
from scipy.linalg import expm
from scipy.optimize import brentq


def zoh(num, den, T):
    nz, dz, _ = signal.cont2discrete((num, den), T, method="zoh")
    nz = np.trim_zeros(np.atleast_1d(np.squeeze(nz)), "f")
    return nz, np.asarray(dz)


def tustin(num, den, T, w_p=None):
    alpha = T / 2 if w_p is None else math.tan(w_p * T / 2) / w_p
    nz, dz, _ = signal.cont2discrete((num, den), 2 * alpha, method="bilinear")
    # cont2discrete's bilinear uses s = (2/dt)(z-1)/(z+1); dt = 2 alpha gives s = (1/alpha)(z-1)/(z+1)
    return np.trim_zeros(np.atleast_1d(np.squeeze(nz)), "f"), np.asarray(dz)


def pi_tustin(Kp, Ki, T):
    """u[k] = u[k-1] + b0 e[k] + b1 e[k-1] for C(z) = Kp + Ki (T/2)(z + 1)/(z - 1)."""
    return Kp + Ki * T / 2, -Kp + Ki * T / 2


def _ss(num, den):
    A, B, C, D = signal.tf2ss(num, den)
    return np.asarray(A), np.asarray(B).ravel(), np.asarray(C).ravel(), float(np.asarray(D).ravel()[0])


def sampled_loop(plant, ctrl_step, T, t_end, r=1.0, n_sub=50, u_limits=None):
    """Simulate a continuous plant (num, den) under a discrete controller with ZOH.

    ctrl_step(e, state) -> (u, state) is called once per sample with the sampled error e = r - y(kT).
    Returns (t, y, uk) with n_sub points per sample interval (exact matrix-exponential propagation).
    """
    A, B, C, _ = _ss(*plant)
    n = len(A)
    M = np.zeros((n + 1, n + 1))
    M[:n, :n] = A
    M[:n, n] = B
    h = T / n_sub
    Eh = expm(M * h)
    x = np.zeros(n)
    state = None
    ts, ys, us = [], [], []
    steps = int(round(t_end / T))
    for k in range(steps):
        y = float(C @ x)
        u, state = ctrl_step(r - y, state)
        if u_limits is not None:
            u = min(u_limits[1], max(u_limits[0], u))
        us.append(u)
        for j in range(n_sub):
            ts.append(k * T + j * h)
            ys.append(float(C @ x))
            z = Eh @ np.concatenate([x, [u]])
            x = z[:n]
    ts.append(steps * T)
    ys.append(float(C @ x))
    return np.array(ts), np.array(ys), np.array(us)


def dfreq(numz, denz, w, T):
    z = np.exp(1j * np.asarray(w) * T)
    return np.polyval(numz, z) / np.polyval(denz, z)


def dmargins(numz, denz, T, w_lo=None, n=200001):
    """Margins of a discrete loop gain evaluated on the unit circle up to the Nyquist frequency pi/T."""
    w_hi = math.pi / T * (1 - 1e-9)
    w_lo = w_hi * 1e-6 if w_lo is None else w_lo
    w = np.logspace(math.log10(w_lo), math.log10(w_hi), n)
    L = dfreq(numz, denz, w, T)
    mag = np.abs(L)
    ph = np.unwrap(np.angle(L))
    out = {}
    i = np.flatnonzero((mag[:-1] - 1) * (mag[1:] - 1) < 0)
    if i.size:
        wc = brentq(lambda x: abs(dfreq(numz, denz, x, T)) - 1, w[i[0]], w[i[0] + 1], xtol=1e-14 * w[i[0]])
        phc = ph[i[0]] + (np.angle(dfreq(numz, denz, wc, T) / L[i[0]]))
        out["wc"], out["pm"] = wc, 180 + math.degrees(phc)
    j = np.flatnonzero((ph[:-1] + math.pi) * (ph[1:] + math.pi) < 0)
    if j.size:
        f = lambda x: math.degrees(ph[j[0]] + np.angle(dfreq(numz, denz, x, T) / L[j[0]])) + 180  # noqa: E731
        w180 = brentq(f, w[j[0]], w[j[0] + 1], xtol=1e-14 * w[j[0]])
        out["w180"], out["gm"] = w180, 1 / abs(dfreq(numz, denz, w180, T))
    return out


def jury2(a1, a0):
    """True if both roots of z^2 + a1 z + a0 lie strictly inside the unit circle."""
    return abs(a0) < 1 and 1 + a1 + a0 > 0 and 1 - a1 + a0 > 0
