"""Lab 21-07 helpers: power-amplifier classes, efficiency under back-off, Doherty, envelope tracking, ACLR and DPD.

Conventions. Drain-current waveforms are idealized; the drain voltage swings sinusoidally (or as stated) about
V_DD. Complex baseband signals use envelope power: a signal x has average power E|x|^2.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate


# ---------------------------------------------------------------- load line
def r_opt(vdd, pout, vknee=0.0):
    """Optimum load for a sinusoidal swing from the knee to 2 V_DD - V_knee: (V_DD - V_k)^2 / (2 P)."""
    return (vdd - vknee) ** 2 / (2 * pout)


# ---------------------------------------------------------------- reduced conduction angle
def conduction(alpha):
    """Truncated-cosine drain current with conduction angle alpha (rad) and peak I_max = 1.
    Returns (I_dc, I_1, efficiency at full voltage swing)."""
    c = math.cos(alpha / 2)
    idc = (2 * math.sin(alpha / 2) - alpha * c) / (2 * math.pi * (1 - c))
    i1 = (alpha - math.sin(alpha)) / (2 * math.pi * (1 - c))
    return idc, i1, 0.5 * i1 / idc


def eta_backoff(cls, x):
    """Drain efficiency at normalized output amplitude x (0..1) for ideal tuned class A or class B."""
    return {"A": 0.5 * x * x, "B": math.pi / 4 * x}[cls]


def eta_doherty(x):
    """Ideal symmetric Doherty (class-B main and auxiliary, auxiliary turning on at x = 1/2)."""
    return (math.pi / 2) * x * x / (x + max(0.0, 2 * x - 1))


def class_f3_eta():
    """Class-B current with a maximally flat voltage using the 3rd harmonic: V1 = (9/8) V_DD."""
    return math.pi / 4 * 9 / 8


# ---------------------------------------------------------------- class E (50 % duty, infinite choke, high-Q load)
def class_e():
    """Normalized design values: P R / V_DD^2, w C R, X / R, I_m / I_DC, phase (deg), peak v / V_DD, peak i / I_DC."""
    k = 8 / (math.pi ** 2 + 4)
    phi = math.atan2(1, -math.pi / 2)
    im = math.sqrt(1 + math.pi ** 2 / 4)
    th = np.linspace(0, 2 * np.pi, 400001)[:-1]
    wc = 1 / math.pi                      # I_DC = V_DD = 1
    v = np.where(th >= np.pi, ((th - np.pi) + im * (np.cos(th + phi) - np.cos(np.pi + phi))) / wc, 0.0)
    x_over_r = 2 * np.mean(v * np.cos(th + phi)) / im / k
    return {"PR_V2": k, "wCR": 8 / (math.pi * (math.pi ** 2 + 4)), "X_R": x_over_r, "Im_Idc": im,
            "phi_deg": math.degrees(phi), "vpk": float(v.max()), "ipk": 1 + im}


# ---------------------------------------------------------------- OFDM statistics
def average_efficiency(eta_fun, papr_db):
    """Average efficiency for a complex-Gaussian (Rayleigh-envelope) signal whose peak, at papr_db above the
    average power, is set to full output (x = 1). Output power ~ x^2; DC power = output / eta(x)."""
    xmax2 = 10 ** (papr_db / 10)          # (peak / average) power ratio
    # envelope power P/Pavg = u, exponential; x = sqrt(u / xmax2), clipped at 1
    def x_of(u):
        return min(1.0, math.sqrt(u / xmax2))
    pout = integrate.quad(lambda u: x_of(u) ** 2 * math.exp(-u), 0, 60, points=[xmax2], limit=200)[0]
    pdc = integrate.quad(lambda u: (x_of(u) ** 2 / eta_fun(x_of(u)) if u > 0 else 0.0) * math.exp(-u), 0, 60,
                         points=[xmax2], limit=200)[0]
    return pout / pdc


# ---------------------------------------------------------------- signals, PA models, ACLR, DPD
def ofdm(n_sym=64, n_fft=1024, n_used=128, seed=2107):
    """Complex baseband OFDM, 16-QAM on n_used central subcarriers, oversampled n_fft/n_used times; unit power."""
    rng = np.random.default_rng(seed)
    levels = np.array([-3, -1, 1, 3])
    out = []
    for _ in range(n_sym):
        X = np.zeros(n_fft, complex)
        k = np.r_[1:n_used // 2 + 1, n_fft - n_used // 2:n_fft]
        X[k] = rng.choice(levels, n_used) + 1j * rng.choice(levels, n_used)
        out.append(np.fft.ifft(X))
    x = np.concatenate(out)
    return x / np.sqrt(np.mean(np.abs(x) ** 2))


def rapp(x, gain=1.0, asat=1.0, p=2.0):
    """Rapp AM-AM model (no AM-PM): |y| = g|x| / (1 + (g|x|/A_sat)^(2p))^(1/2p)."""
    a = np.abs(x)
    return gain * x / (1 + (gain * a / asat) ** (2 * p)) ** (1 / (2 * p))


def cubic(x, a1=1.0, a3=-0.05):
    return a1 * x + a3 * x * np.abs(x) ** 2


def aclr_db(y, n_fft=1024, n_used=128):
    """Adjacent-channel leakage ratio (upper adjacent channel of the same width, centred one channel away)."""
    seg = y.reshape(-1, n_fft)
    S = np.mean(np.abs(np.fft.fft(seg, axis=1)) ** 2, axis=0)
    f = np.fft.fftfreq(n_fft) * n_fft            # bin index, signed
    main = S[np.abs(f) <= n_used // 2].sum()
    adj = S[(f > n_used // 2) & (f <= 3 * n_used // 2)].sum()
    return 10 * math.log10(adj / main)


def evm_pct(y, x):
    g = np.vdot(x, y) / np.vdot(x, x)
    return 100 * math.sqrt(np.mean(np.abs(y - g * x) ** 2) / np.mean(np.abs(g * x) ** 2))


def fit_postinverse(y, x, orders=(1, 3, 5, 7)):
    """Indirect learning: fit x ~ sum c_k y |y|^(k-1); the same polynomial is then used as the predistorter."""
    A = np.column_stack([y * np.abs(y) ** (k - 1) for k in orders])
    c, *_ = np.linalg.lstsq(A, x, rcond=None)
    return c


def apply_poly(u, c, orders=(1, 3, 5, 7)):
    return sum(ck * u * np.abs(u) ** (k - 1) for ck, k in zip(c, orders))


def dpd_loop(x, pa, iterations=3, orders=(1, 3, 5, 7)):
    """Iterated indirect learning with the PA's small-signal gain normalized to 1."""
    u = x.copy()
    for _ in range(iterations):
        y = pa(u)
        c = fit_postinverse(y, u, orders)
        u = apply_poly(x, c, orders)
    return u
