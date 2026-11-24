"""Lab 21-03 helpers: noise figure, noise parameters, Y-factor, nonlinearity, cascades and dynamic range.

Conventions: powers in dBm are available powers referred to 50 ohm; a peak voltage amplitude A across 50 ohm
carries A^2/(2 * 50) watts. Polynomial models are y = a1 x + a2 x^2 + a3 x^3 (memoryless).
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, optimize, special

K_B = 1.380649e-23
Q_E = 1.602176634e-19
T0 = 290.0
KT0_DBM_HZ = 10 * math.log10(K_B * T0 * 1e3)   # -173.98 dBm/Hz


def db(x):
    return 10 * math.log10(x)


def undb(x_db):
    return 10 ** (x_db / 10)


def dbm_from_amp(a, r=50.0):
    """Peak voltage amplitude across r -> power in dBm."""
    return db(a * a / (2 * r) / 1e-3)


def amp_from_dbm(p_dbm, r=50.0):
    return math.sqrt(2 * r * 1e-3 * undb(p_dbm))


# ---------------------------------------------------------------- noise figure
def friis(stages):
    """stages: list of (gain_dB, NF_dB) from the input. Returns the cascade noise figure in dB."""
    f_tot, g_run = 0.0, 1.0
    for k, (g_db, nf_db) in enumerate(stages):
        f = undb(nf_db)
        f_tot = f if k == 0 else f_tot + (f - 1) / g_run
        g_run *= undb(g_db)
    return db(f_tot)


def noise_factor_gamma(gs, fmin_db, rn, gopt, z0=50.0):
    """Noise factor for source reflection gs from (Fmin, Rn, Gamma_opt): Fmin + 4 rn |gs - gopt|^2 /
    ((1 - |gs|^2) |1 + gopt|^2)."""
    rn_n = rn / z0
    return undb(fmin_db) + 4 * rn_n * abs(gs - gopt) ** 2 / ((1 - abs(gs) ** 2) * abs(1 + gopt) ** 2)


def noise_circle(nf_db, fmin_db, rn, gopt, z0=50.0):
    """Centre and radius (in the source-reflection plane) of the constant-noise-figure circle."""
    n = (undb(nf_db) - undb(fmin_db)) * abs(1 + gopt) ** 2 / (4 * rn / z0)
    c = gopt / (n + 1)
    r = math.sqrt(n * (n + 1 - abs(gopt) ** 2)) / (n + 1)
    return c, r


def noise_params_from_en_in(en, in_u, ycor, t=T0):
    """Two-port noise parameters from an input noise voltage density en (V/sqrt(Hz)), the part of the input noise
    current density uncorrelated with it, in_u (A/sqrt(Hz)), and the correlation admittance ycor (S):
    returns Rn, Gu, Yopt, Fmin."""
    rn = en ** 2 / (4 * K_B * t)
    gu = in_u ** 2 / (4 * K_B * t)
    gopt = math.sqrt(gu / rn + ycor.real ** 2)
    yopt = complex(gopt, -ycor.imag)
    fmin = 1 + 2 * rn * (gopt + ycor.real)
    return rn, gu, yopt, fmin


def y_factor_nf(enr_db, y_db, tc=T0):
    """Noise figure (dB) from the Y-factor, with the cold temperature correction."""
    enr, y = undb(enr_db), undb(y_db)
    return db((enr - y * (tc / T0 - 1)) / (y - 1))


def second_stage_correct(f12_db, f2_db, g1_db):
    return db(undb(f12_db) - (undb(f2_db) - 1) / undb(g1_db))


def sensitivity_dbm(nf_db, bw_hz, snr_db, im_db=0.0, div_db=0.0):
    """-174 dBm/Hz + 10 log B + NF + SNR + implementation margin - diversity gain (3GPP TR 38.817-01 form)."""
    return KT0_DBM_HZ + db(bw_hz) + nf_db + snr_db + im_db - div_db


# ---------------------------------------------------------------- nonlinearity
def a_1db(a1, a3):
    """Input amplitude of 1 dB gain compression from the cubic model (a3 of opposite sign to a1)."""
    return math.sqrt((1 - 10 ** (-1 / 20)) * 4 / 3 * abs(a1 / a3))


def a_iip3(a1, a3):
    return math.sqrt(4 / 3 * abs(a1 / a3))


def a_iip2(a1, a2):
    return abs(a1 / a2)


def cascade_iip3(stages):
    """stages: list of (gain_dB, IIP3_dBm) from the input. Worst-case (in-phase) cascade, in dBm."""
    inv, g_run = 0.0, 1.0
    for g_db, iip3 in stages:
        inv += g_run / undb(iip3)
        g_run *= undb(g_db)
    return -db(inv)


def sfdr_db(iip3_dbm, nf_db, bw_hz):
    floor = KT0_DBM_HZ + db(bw_hz) + nf_db
    return 2 / 3 * (iip3_dbm - floor)


def tones(func, amps, freqs, fs, n):
    """Apply a memoryless func to a sum of cosines sampled at fs (n samples, whole periods); return the one-sided
    amplitude spectrum and its frequency axis."""
    t = np.arange(n) / fs
    x = sum(a * np.cos(2 * np.pi * f * t) for a, f in zip(amps, freqs))
    y = func(x)
    spec = np.abs(np.fft.rfft(y)) / n * 2
    spec[0] /= 2
    return np.fft.rfftfreq(n, 1 / fs), spec


def bjt_harmonics(x, nmax=3):
    """Collector-current harmonics of exp(x cos wt) relative to the fundamental: I_n(x)/I_1(x)."""
    return [special.iv(k, x) / special.iv(1, x) for k in range(2, nmax + 1)]


def tanh_fundamental(x):
    """Fundamental amplitude of tanh(x cos theta), by quadrature."""
    return 2 / math.pi * integrate.quad(lambda th: math.tanh(x * math.cos(th)) * math.cos(th), 0, math.pi)[0]


def tanh_x1db():
    """Peak input (in units of the tanh argument) at which the fundamental is 1 dB below linear."""
    return optimize.brentq(lambda x: tanh_fundamental(x) / x - 10 ** (-1 / 20), 0.05, 3.0, xtol=1e-12)
