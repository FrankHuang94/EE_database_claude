"""Lab 15-07 helpers: loop-gain frequency responses, margins, Nyquist encirclements and Bode's integral.

Loop gains are given as polynomials (num, den), highest power first, optionally with a time delay T:
L(s) = num(s)/den(s) * exp(-s T).

    freq_resp(num, den, w, T=0)     complex L(jw) on an array of frequencies
    margins(num, den, T=0, ...)     crossover, phase margin, phase-crossover frequency, gain margin, delay margin
    nyquist_encirclements(...)      clockwise encirclements of -1 by L along the Nyquist contour
    closed_loop_rhp(...)            Z = N + P, the number of unstable closed-loop poles (rational loops)
    sensitivity_peak(...)           Ms = max |1/(1 + L(jw))|, and its frequency
    bode_integral(...)              integral of ln|S(jw)| from 0 to infinity
    pm_from_zeta(zeta)              phase margin of the standard loop wn^2/(s(s + 2 zeta wn))

The margins are found by root finding on |L| - 1 and on the unwrapped phase + 180 degrees, starting from a dense
logarithmic grid, so they do not depend on the grid spacing.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def freq_resp(num, den, w, T=0.0):
    s = 1j * np.asarray(w, dtype=float)
    return np.polyval(num, s) / np.polyval(den, s) * np.exp(-s * T)


def _unwrapped_phase(num, den, w, T):
    """Phase of L(jw) in radians, built as a sum of factor phases so that it is continuous in w."""
    s = 1j * np.asarray(w, dtype=float)
    ph = np.zeros_like(np.asarray(w, dtype=float))
    lead = np.sign(num[0] if abs(num[0]) > 0 else 1.0) * np.sign(den[0])
    for z in (np.roots(num) if len(num) > 1 else []):
        ph = ph + np.angle(s - z) if abs(z) > 1e-300 else ph + np.pi / 2
    for p in np.roots(den):
        ph = ph - (np.angle(s - p) if abs(p) > 1e-12 else np.pi / 2)
    if lead < 0:
        ph = ph - np.pi
    return ph - np.asarray(w, dtype=float) * T


def margins(num, den, T=0.0, w_lo=1e-6, w_hi=1e12, n=200001):
    """Return a dict with wc, pm (deg), w180, gm (ratio), gm_db and delay_margin (s) where they exist.

    wc is the first gain crossover (|L| = 1) above w_lo; w180 the first phase crossover (phase = -180 deg).
    """
    num, den = np.atleast_1d(np.asarray(num, float)), np.atleast_1d(np.asarray(den, float))
    w = np.logspace(math.log10(w_lo), math.log10(w_hi), n)
    mag = np.abs(freq_resp(num, den, w, T))
    ph = _unwrapped_phase(num, den, w, T)
    out = {}
    i = np.flatnonzero((mag[:-1] - 1) * (mag[1:] - 1) < 0)
    if i.size:
        wc = brentq(lambda x: abs(freq_resp(num, den, x, T)) - 1, w[i[0]], w[i[0] + 1], xtol=1e-14 * w[i[0]])
        phc = float(_unwrapped_phase(num, den, np.array([wc]), T)[0])
        out["wc"] = wc
        out["pm"] = 180.0 + math.degrees(phc)
        if T >= 0 and out["pm"] > 0:
            out["delay_margin"] = math.radians(out["pm"]) / wc
    j = np.flatnonzero((ph[:-1] + math.pi) * (ph[1:] + math.pi) < 0)
    if j.size:
        f = lambda x: float(_unwrapped_phase(num, den, np.array([x]), T)[0]) + math.pi  # noqa: E731
        w180 = brentq(f, w[j[0]], w[j[0] + 1], xtol=1e-14 * w[j[0]])
        out["w180"] = w180
        out["gm"] = 1.0 / abs(freq_resp(num, den, w180, T))
        out["gm_db"] = 20 * math.log10(out["gm"])
    return out


def nyquist_encirclements(num, den, K=1.0, eps=1e-6, R=1e6, n=400001):
    """Clockwise encirclements of -1 by K L(s) as s traverses the Nyquist contour (clockwise).

    The contour runs up the imaginary axis, around a large semicircle on the right, and is indented by small
    semicircles of radius eps to the right of any imaginary-axis poles of L.
    """
    num, den = np.atleast_1d(np.asarray(num, float)), np.atleast_1d(np.asarray(den, float))
    axis_poles = sorted(p.imag for p in np.roots(den) if abs(p.real) < 1e-9)
    pts = []
    # build the path from -jR up to +jR with indentations, then the big arc back to -jR
    ys = np.linspace(-R, R, n)
    ys = np.sinh(np.linspace(-math.asinh(R / eps), math.asinh(R / eps), n)) * eps   # dense near the origin
    for y in ys:
        near = [q for q in axis_poles if abs(y - q) < eps]
        if near:
            continue
        pts.append(1j * y)
    path = []
    k = 0
    for q in axis_poles:
        while k < len(pts) and pts[k].imag < q - eps:
            path.append(pts[k])
            k += 1
        th = np.linspace(-math.pi / 2, math.pi / 2, 4001)
        path.extend(1j * q + eps * np.exp(1j * th))
        while k < len(pts) and pts[k].imag <= q + eps:
            k += 1
    path.extend(pts[k:])
    th = np.linspace(math.pi / 2, -math.pi / 2, 4001)
    path.extend(R * np.exp(1j * th))
    s = np.array(path)
    F = 1 + K * np.polyval(num, s) / np.polyval(den, s)
    ang = np.unwrap(np.angle(F))
    turns = (ang[-1] - ang[0]) / (2 * math.pi)
    return int(round(-turns))           # counterclockwise winding counts negative


def closed_loop_rhp(num, den, K=1.0, **kw):
    """Z = N + P: clockwise encirclements plus open-loop right-half-plane poles."""
    P = int(np.sum(np.roots(den).real > 1e-9))
    return nyquist_encirclements(num, den, K, **kw) + P


def sensitivity_peak(num, den, T=0.0, w_lo=1e-6, w_hi=1e12, n=400001):
    w = np.logspace(math.log10(w_lo), math.log10(w_hi), n)
    S = np.abs(1 / (1 + freq_resp(num, den, w, T)))
    k = int(np.argmax(S))
    return float(S[k]), float(w[k])


def bode_integral(num, den, w_max=np.inf):
    """Integral of ln|S(jw)| over (0, w_max), split at decades for accuracy."""
    f = lambda w: math.log(abs(1 / (1 + freq_resp(num, den, w))))  # noqa: E731
    edges = [0.0] + [10.0**k for k in range(-6, 13)] + [np.inf]
    total = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        if a >= w_max:
            break
        val, _ = quad(f, a, min(b, w_max), limit=400)
        total += val
    return total


def pm_from_zeta(zeta):
    """Exact phase margin (deg) of L = wn^2/(s(s + 2 zeta wn)) with unity feedback."""
    x = math.sqrt(math.sqrt(1 + 4 * zeta**4) - 2 * zeta**2)
    return math.degrees(math.atan(2 * zeta / x))
