"""Lab 15-03 helpers: exact step responses and time-domain specifications.

    step_at(num, den, t)      exact unit-step response at time t (matrix exponential; any pole pattern)
    impulse_at(num, den, t)   exact impulse response at t (its zeros are the step response's extrema)
    step_curve(num, den, t)   the step response sampled on an array t (for plots)
    step_specs(num, den, ...) final value, 10-90% rise time, peak, overshoot, peak time, settling time
    second_order(zeta, wn)    the standard second-order specs from the closed-form formulas

Crossing times are found on a dense grid and then refined with brentq on the exact response, so the specs
are accurate to the root finder's tolerance, not to the grid spacing.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal
from scipy.linalg import expm
from scipy.optimize import brentq


def _ss(num, den):
    A, B, C, D = signal.tf2ss(num, den)
    return A, B, C, D


def step_at(num, den, t):
    """y(t) for a unit step: x(t) = integral_0^t e^{A tau} d tau B, from expm([[A, B], [0, 0]] t)."""
    A, B, C, D = _ss(num, den)
    n = A.shape[0]
    if n == 0:
        return float(D.item())
    M = np.zeros((n + 1, n + 1))
    M[:n, :n] = A
    M[:n, n:] = B
    x = expm(M * t)[:n, n:]
    return float((C @ x + D).item())


def impulse_at(num, den, t):
    """h(t) = C e^{At} B for t > 0 (the D*delta term is omitted)."""
    A, B, C, _ = _ss(num, den)
    return float((C @ expm(A * t) @ B).item())


def step_curve(num, den, t):
    _, y = signal.step(signal.TransferFunction(num, den), T=t)
    return y


def _refine(f, a, b):
    return brentq(f, a, b, xtol=1e-15 * max(1.0, abs(b)) + 1e-300, rtol=1e-14, maxiter=500)


def step_specs(num, den, t_end, band=0.02, n=200001, rise=(0.1, 0.9)):
    """Specs of the unit-step response of num/den (all poles must be in the left half-plane).

    Returns a dict: final, rise (10-90% by default), peak, overshoot (fraction of the final value),
    tpeak, settle (last exit from the +/- band around the final value), undershoot (most negative
    excursion relative to zero, as a fraction of the final value; 0 if none) and tmin.
    """
    final = float(np.polyval(num, 0) / np.polyval(den, 0))
    t = np.linspace(0, t_end, n)
    y = step_curve(num, den, t)
    f = lambda tt: step_at(num, den, tt)  # noqa: E731
    out = {"final": final}

    # rise time: first crossings of the two levels
    times = []
    for lev in rise:
        target = lev * final
        k = int(np.flatnonzero((y - target) * np.sign(final) >= 0)[0])
        times.append(_refine(lambda tt: f(tt) - target, t[k - 1], t[k]))
    out["rise"] = times[1] - times[0]

    # peak: largest value, refined as a zero of the impulse response
    k = int(np.argmax(y * np.sign(final)))
    h = lambda tt: impulse_at(num, den, tt)  # noqa: E731
    if 0 < k < n - 1 and abs(y[k]) > abs(final) * (1 + 1e-9) and h(t[k - 1]) * h(t[k + 1]) < 0:
        tp = _refine(h, t[k - 1], t[k + 1])
        pk = f(tp)
    else:                                   # monotonic: no interior peak
        tp, pk = float("nan"), final
    out["peak"], out["tpeak"] = pk, tp
    out["overshoot"] = max(0.0, pk / final - 1)

    # undershoot (non-minimum-phase responses start the wrong way)
    k = int(np.argmin(y * np.sign(final)))
    if 0 < k < n - 1 and y[k] * np.sign(final) < -1e-12 * abs(final) and h(t[k - 1]) * h(t[k + 1]) < 0:
        tm = _refine(h, t[k - 1], t[k + 1])
        out["undershoot"], out["tmin"] = -f(tm) / final, tm
    else:
        out["undershoot"], out["tmin"] = 0.0, 0.0

    # settling: the last time the response is outside the band
    tol = band * abs(final)
    outside = np.flatnonzero(np.abs(y - final) > tol)
    if outside.size == 0:
        out["settle"] = 0.0
    else:
        k = int(outside[-1])
        if k == n - 1:
            raise ValueError("not settled by t_end: increase t_end")
        lev = final + tol if y[k] > final else final - tol
        out["settle"] = _refine(lambda tt: f(tt) - lev, t[k], t[k + 1])
    return out


def second_order(zeta, wn, band=0.02):
    """Closed-form specs of wn^2/(s^2 + 2 zeta wn s + wn^2) for 0 < zeta < 1."""
    wd = wn * math.sqrt(1 - zeta**2)
    sigma = zeta * wn
    return {
        "overshoot": math.exp(-math.pi * zeta / math.sqrt(1 - zeta**2)),
        "tpeak": math.pi / wd,
        "settle_envelope": math.log(1 / (band * math.sqrt(1 - zeta**2))) / sigma,
        "settle_4": 4 / sigma,
        "wd": wd,
        "sigma": sigma,
    }


def zeta_from_overshoot(mp):
    """Damping ratio that gives fractional overshoot mp (0 < mp < 1)."""
    lm = math.log(mp)
    return -lm / math.sqrt(math.pi**2 + lm**2)
