"""Lab 21-09 helpers: acoustic resonators (BVD model), ladder filters, temperature drift, RF switches, antenna
mismatch. Frequencies in hertz, impedances in ohms."""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------- Butterworth-Van Dyke resonator
def bvd(fs, c0, ratio, q):
    """Motional elements for series resonance fs, static capacitance c0, capacitance ratio r = C0/Cm and
    unloaded Q at fs. Returns (Lm, Cm, Rm)."""
    cm = c0 / ratio
    lm = 1 / ((2 * math.pi * fs) ** 2 * cm)
    rm = 2 * math.pi * fs * lm / q
    return lm, cm, rm


def z_bvd(f, c0, lm, cm, rm):
    s = 2j * math.pi * np.asarray(f, dtype=float)
    zm = rm + s * lm + 1 / (s * cm)
    return 1 / (s * c0 + 1 / zm)


def fp_over_fs(ratio):
    """Parallel (anti-)resonance over series resonance: sqrt(1 + Cm/C0)."""
    return math.sqrt(1 + 1 / ratio)


def k2_eff(fs, fp):
    """Thickness-mode effective coupling: (pi/2)(fs/fp) / tan((pi/2)(fs/fp))."""
    x = (math.pi / 2) * fs / fp
    return x / math.tan(x)


def k2_approx(fs, fp):
    return (math.pi ** 2 / 4) * (fp - fs) / fp


def fp_for_k2(fs, k2):
    """Inverse of k2_eff: the anti-resonance that gives coupling k2."""
    return brentq(lambda fp: k2_eff(fs, fp) - k2, fs * (1 + 1e-9), fs * 1.5)


# ---------------------------------------------------------------- ladder filter (ABCD)
def ladder_s21(f, stages, z0=50.0):
    """stages: list of ('series'|'shunt', impedance function of f). Returns complex S21 between z0 terminations."""
    f = np.atleast_1d(np.asarray(f, dtype=float))
    out = np.empty(f.size, complex)
    for i, fi in enumerate(f):
        M = np.eye(2, dtype=complex)
        for kind, zfun in stages:
            z = zfun(fi)
            M = M @ (np.array([[1, z], [0, 1]]) if kind == "series" else np.array([[1, 0], [1 / z, 1]]))
        a, b, c, d = M.ravel()
        out[i] = 2 / (a + b / z0 + c * z0 + d)
    return out


def ladder(fs_series, fs_shunt, c0_series, c0_shunt, ratio, q, n_sections=2):
    """An n-section ladder: each section a series resonator then a shunt resonator."""
    ls, cs, rs = bvd(fs_series, c0_series, ratio, q)
    lp, cp, rp = bvd(fs_shunt, c0_shunt, ratio, q)
    ser = ("series", lambda f: complex(z_bvd(f, c0_series, ls, cs, rs)))
    sh = ("shunt", lambda f: complex(z_bvd(f, c0_shunt, lp, cp, rp)))
    return [ser, sh] * n_sections


# ---------------------------------------------------------------- temperature drift
def tcf_drift(f, tcf_ppm, dT):
    return f * tcf_ppm * 1e-6 * dT


# ---------------------------------------------------------------- switches and mismatch
def series_switch_on_db(ron, z0=50.0):
    """Insertion loss of a series resistance between z0 terminations: 20 log(1 + R/(2 z0))."""
    return 20 * math.log10(1 + ron / (2 * z0))


def series_switch_off_db(f, coff, z0=50.0):
    """Isolation of a series capacitance between z0 terminations."""
    x = 2 * z0 * 2 * math.pi * f * coff
    return -20 * math.log10(x / math.sqrt(1 + x * x))


def fom_fs(ron, coff):
    return ron * coff * 1e15


def cutoff_hz(ron, coff):
    return 1 / (2 * math.pi * ron * coff)


def mismatch_loss_db(vswr):
    g = (vswr - 1) / (vswr + 1)
    return -10 * math.log10(1 - g * g)


def peak_voltage(p_dbm, z0=50.0, vswr=1.0):
    """Peak RF voltage on a line carrying p_dbm into z0, worst case under a mismatch: (1 + |Gamma|) times."""
    v = math.sqrt(2 * z0 * 10 ** (p_dbm / 10) * 1e-3)
    g = (vswr - 1) / (vswr + 1)
    return v * (1 + g)


# ---------------------------------------------------------------- lab conveniences
def insertion_loss_db(f, stages, z0=50.0):
    return -20 * np.log10(np.abs(ladder_s21(f, stages, z0)))


def band_edges(stages, fc, span, drop_db=3.0):
    """Frequencies where the loss is drop_db above its value at fc, searched within fc*(1 -/+ span)."""
    ref = float(insertion_loss_db(fc, stages)[0])
    g = lambda f: float(insertion_loss_db(f, stages)[0]) - ref - drop_db  # noqa: E731
    return brentq(g, fc * (1 - span), fc), brentq(g, fc, fc * (1 + span))


def loss_at_temperature(f, stages, tcf_ppm, t_c, t_ref=25.0):
    """Loss at a fixed frequency f when every resonance has moved by tcf_ppm*(t_c - t_ref) ppm: equivalent to
    evaluating the room-temperature filter at f / (1 + alpha)."""
    alpha = tcf_ppm * 1e-6 * (t_c - t_ref)
    return float(insertion_loss_db(f / (1 + alpha), stages)[0])


def stack_count(p_dbm, vswr, v_per_fet, z0=50.0):
    return math.ceil(peak_voltage(p_dbm, z0, vswr) / v_per_fet)
