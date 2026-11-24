"""Lab 20-10: phase-domain models of charge-pump, fractional-N and all-digital PLLs.

Phase-domain conventions: phases in radians; the charge pump's gain is I_cp / (2 pi) (A/rad); the VCO's gain K_vco is in
rad/s per volt, so its phase transfer is K_vco / s; the divider divides phase by N. The loop filter is the standard
third-order passive network: R in series with C1, both in parallel with C2.

- loop_filter_z, open_loop, closed_loop: transfer functions at s = j omega.
- design_third_order: R, C1, C2 for a chosen crossover frequency and pole/zero spread b (phase margin
  atan((b - 1) / (2 sqrt b))).
- crossover_and_pm: numerical crossover and phase margin.
- step_settle: settling time of the closed-loop phase step response (linear model, via scipy).
- integrate_jitter: rms jitter of a piecewise-linear (in log-log) single-sideband phase-noise profile.
- mash_sequence, divider_phase_psd: a MASH 1-1-1 divider-control sequence (integer accumulators) and the phase
  noise it produces.
- fom_jitter, fom_oscillator, tdc_floor: figures of merit and the TDC-limited in-band floor of an ADPLL.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, signal


def loop_filter_z(w, r, c1, c2):
    s = 1j * np.asarray(w, float)
    return (1 + s * r * c1) / (s * (c1 + c2) * (1 + s * r * c1 * c2 / (c1 + c2)))


def open_loop(w, icp, kvco, n, r, c1, c2):
    s = 1j * np.asarray(w, float)
    return icp / (2 * np.pi) * loop_filter_z(w, r, c1, c2) * kvco / s / n


def closed_loop(w, icp, kvco, n, r, c1, c2):
    """Reference-to-output phase transfer N G / (1 + G) and VCO-to-output 1 / (1 + G)."""
    g = open_loop(w, icp, kvco, n, r, c1, c2)
    return n * g / (1 + g), 1 / (1 + g)


def design_third_order(fc, b, icp, kvco, n):
    """Return R, C1, C2 placing the maximum phase lead (zero at fc/sqrt b, pole at fc sqrt b) at crossover fc."""
    wc = 2 * np.pi * fc
    wz, wp = wc / math.sqrt(b), wc * math.sqrt(b)
    k = icp * kvco / (2 * np.pi * n)
    ctot = k / wc ** 2 * math.sqrt(1 + (wc / wz) ** 2) / math.sqrt(1 + (wc / wp) ** 2)
    c1 = ctot * (b - 1) / b
    c2 = ctot - c1
    r = 1 / (wz * c1)
    return r, c1, c2


def crossover_and_pm(icp, kvco, n, r, c1, c2, lo=1e2, hi=1e10):
    f = optimize.brentq(lambda f: abs(open_loop(2 * np.pi * f, icp, kvco, n, r, c1, c2)) - 1, lo, hi)
    return f, 180 + math.degrees(np.angle(open_loop(2 * np.pi * f, icp, kvco, n, r, c1, c2)))


def step_settle(icp, kvco, n, r, c1, c2, tol=1e-3, tmax=None):
    """Time for the output phase (normalized) to stay within tol of its final value after a reference phase step."""
    k = icp * kvco / (2 * np.pi * n)
    # G(s) = k (1 + s R C1) / (s^2 (C1 + C2) (1 + s tau2)), tau2 = R C1 C2 / (C1 + C2)
    tau2 = r * c1 * c2 / (c1 + c2)
    num = np.array([k * r * c1, k])
    den = np.polyadd(np.array([(c1 + c2) * tau2, (c1 + c2), 0, 0]), np.array([0, 0, k * r * c1, k]))
    sys_ = signal.TransferFunction(num, den)
    tmax = tmax or 40 / (k * r * c1 / (c1 + c2))
    t = np.linspace(0, tmax, 200001)
    _, y = signal.step(sys_, T=t)
    out = np.abs(y - 1) > tol
    return t[np.nonzero(out)[0][-1] + 1] if out.any() else 0.0


def integrate_jitter(freqs, l_dbc, f1, f2, f0):
    """rms jitter (s) of an SSB phase-noise profile L(f) (dBc/Hz) given at points `freqs`, interpolated linearly in
    log-log, integrated from f1 to f2: sigma_phi^2 = 2 * integral L(f) df, sigma_t = sigma_phi / (2 pi f0)."""
    lf, ll = np.log10(freqs), np.asarray(l_dbc, float) / 10
    grid = np.logspace(math.log10(f1), math.log10(f2), 200001)
    lin = 10 ** np.interp(np.log10(grid), lf, ll)
    var = 2 * np.trapezoid(lin, grid)
    return math.sqrt(var) / (2 * np.pi * f0)


def mash_sequence(k, modulus, n, order=3):
    """Integer offsets c[i] (added to the integer divide ratio) from a MASH 1-1-...-1 modulator built, as in hardware,
    from integer accumulators of size `modulus` with input k: the average of c is exactly k / modulus."""
    acc = [0] * order
    carries = np.zeros((n, order))
    for i in range(n):
        x = k
        for j in range(order):
            acc[j] += x
            if acc[j] >= modulus:
                acc[j] -= modulus
                carries[i, j] = 1.0
            x = acc[j]
    out = carries[:, 0].copy()
    for j in range(1, order):
        d = carries[:, j].copy()
        for _ in range(j):
            d = np.diff(np.concatenate([[0.0], d]))
        out += d
    return out


def divider_phase_psd(f, f_ref, order):
    """Single-sideband phase noise L(f) (as a ratio per hertz, equal to the two-sided phase PSD in rad^2/Hz) at the
    output from an order-m MASH divider whose quantization error is white: (2 pi)^2 / (12 f_ref) times
    (2 sin(pi f / f_ref))^(2(m - 1)), before the loop's low-pass filtering. Rational fractions with small denominators
    make the sequence periodic, and the noise becomes spurs instead."""
    return (2 * np.pi) ** 2 / (12 * f_ref) * (2 * np.sin(np.pi * np.asarray(f) / f_ref)) ** (2 * (order - 1))


def fom_jitter(sigma_t, power_w):
    return 20 * math.log10(sigma_t / 1.0) + 10 * math.log10(power_w / 1e-3)


def fom_oscillator(l_dbc, f0, df, power_w):
    return -l_dbc + 20 * math.log10(f0 / df) - 10 * math.log10(power_w / 1e-3)


def tdc_floor(t_res, f0, f_ref):
    """In-band SSB phase-noise floor (dBc/Hz) of an ADPLL limited by TDC quantization of resolution t_res."""
    return 10 * math.log10((2 * np.pi) ** 2 / 12 * (t_res * f0) ** 2 / f_ref)
