"""Bandpass digital modulation in complex baseband: helpers for the 17-06 lab.

- Gray-labelled PSK and square-QAM constellations, mapping bits to symbols and back;
- an AWGN channel calibrated to Es/N0 (complex noise, variance N0/2 per dimension);
- ML (nearest-point) detection, SER and BER simulation;
- closed forms: Craig's exact PSK integral, square-QAM SER, DPSK and FSK;
- EVM measurement and transmitter impairments (phase noise, I/Q imbalance, soft-clipping amplifier);
- DPSK and binary FSK receivers.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate
from scipy.stats import norm

Q = norm.sf


# ------------------------------------------------------------------ constellations
def gray(n):
    return n ^ (n >> 1)


def psk(m):
    """M-PSK with unit average energy; point i carries the Gray label gray(i)."""
    pts = np.exp(2j * np.pi * np.arange(m) / m)
    labels = np.array([gray(i) for i in range(m)])
    return pts, labels


def qam(m):
    """Square M-QAM with levels +-1, +-3, ... (unit spacing 2) and Gray labels per dimension; Es = 2(M-1)/3."""
    L = int(round(math.sqrt(m)))
    k = int(math.log2(L))
    lv = np.arange(-(L - 1), L, 2, dtype=float)
    pts, labels = [], []
    for i in range(L):
        for q in range(L):
            pts.append(lv[i] + 1j * lv[q])
            labels.append((gray(i) << k) | gray(q))
    return np.array(pts), np.array(labels)


def natural_qam(m):
    """Square QAM with natural-binary labels (for comparison with Gray)."""
    pts, _ = qam(m)
    L = int(round(math.sqrt(m)))
    k = int(math.log2(L))
    labels = np.array([(i << k) | q for i in range(L) for q in range(L)])
    return pts, labels


def es(pts):
    return float(np.mean(np.abs(pts) ** 2))


def dmin(pts):
    d = np.abs(pts[:, None] - pts[None, :])
    np.fill_diagonal(d, np.inf)
    return float(d.min())


def papr_db(pts):
    return 10 * math.log10(np.max(np.abs(pts) ** 2) / es(pts))


# ------------------------------------------------------------------ channel and detection
def awgn(sym, esn0_db, es_val, rng):
    """Complex AWGN with N0 = Es / (Es/N0): variance N0/2 per real dimension."""
    n0 = es_val / 10 ** (esn0_db / 10)
    return sym + math.sqrt(n0 / 2) * (rng.standard_normal(sym.shape) + 1j * rng.standard_normal(sym.shape))


def detect(r, pts):
    return np.argmin(np.abs(r[:, None] - pts[None, :]), axis=1)


def simulate(pts, labels, esn0_db, nsym, rng):
    """Return (SER, BER) for uniformly random symbols."""
    m = len(pts)
    k = int(math.log2(m))
    idx = rng.integers(0, m, nsym)
    r = awgn(pts[idx], esn0_db, es(pts), rng)
    d = detect(r, pts)
    ser = float(np.mean(d != idx))
    xor = labels[d] ^ labels[idx]
    bits = sum(((xor >> b) & 1).sum() for b in range(k))
    return ser, float(bits / (nsym * k))


# ------------------------------------------------------------------ closed forms
def ser_psk_craig(m, esn0):
    """Exact M-PSK SER (Craig): (1/pi) int_0^{(M-1)pi/M} exp(-Es/N0 sin^2(pi/M)/sin^2 t) dt."""
    s2 = math.sin(math.pi / m) ** 2
    v, _ = integrate.quad(lambda t: math.exp(-esn0 * s2 / math.sin(t) ** 2), 0, (m - 1) * math.pi / m, limit=200)
    return v / math.pi


def ser_psk_nn(m, esn0):
    return float(2 * Q(math.sqrt(2 * esn0) * math.sin(math.pi / m)))


def ser_qam(m, esn0):
    p = 2 * (1 - 1 / math.sqrt(m)) * Q(math.sqrt(3 * esn0 / (m - 1)))
    return float(1 - (1 - p) ** 2)


def ber_dpsk(ebn0):
    return 0.5 * math.exp(-ebn0)


def ber_fsk_coherent(ebn0):
    return float(Q(math.sqrt(ebn0)))


def ber_fsk_noncoherent(ebn0):
    return 0.5 * math.exp(-ebn0 / 2)


# ------------------------------------------------------------------ EVM and impairments
def evm(measured, ideal):
    return float(math.sqrt(np.mean(np.abs(measured - ideal) ** 2) / np.mean(np.abs(ideal) ** 2)))


def phase_noise(sym, rms_deg, rng):
    return sym * np.exp(1j * np.radians(rms_deg) * rng.standard_normal(sym.shape))


def iq_imbalance(sym, gain, phase_deg):
    """Q path scaled by `gain` and rotated by phase error: s = I + j*g*(Q cos e + I sin e) (one common model)."""
    e = np.radians(phase_deg)
    i, q = sym.real, sym.imag
    return i + 1j * gain * (q * np.cos(e) + i * np.sin(e))


def soft_clip(sym, sat):
    """Rapp-like soft limiter with smoothness 2 on the amplitude: A / (1 + (A/sat)^4)^(1/4)."""
    a = np.abs(sym)
    return sym / (1 + (a / sat) ** 4) ** 0.25


# ------------------------------------------------------------------ DPSK and FSK receivers
def simulate_dpsk(ebn0_db, nbits, rng):
    """Binary DPSK with differential detection (sign of Re{r_k r_(k-1)*})."""
    d = rng.integers(0, 2, nbits)
    ph = np.cumsum(np.pi * d) % (2 * np.pi)
    s = np.exp(1j * np.concatenate([[0.0], ph]))
    r = awgn(s, ebn0_db, 1.0, rng)
    dec = (np.real(r[1:] * np.conj(r[:-1])) < 0).astype(int)
    return float(np.mean(dec != d))


def simulate_bfsk(ebn0_db, nbits, rng, coherent=True):
    """Binary orthogonal FSK in its 2-D signal space; noncoherent uses energy per tone with random phases."""
    d = rng.integers(0, 2, nbits)
    n0 = 1 / 10 ** (ebn0_db / 10)
    if coherent:
        r = np.zeros((nbits, 2))
        r[np.arange(nbits), d] = 1.0
        r += rng.standard_normal((nbits, 2)) * math.sqrt(n0 / 2)
        dec = np.argmax(r, axis=1)
    else:
        th = rng.uniform(0, 2 * np.pi, nbits)
        r = np.zeros((nbits, 2), dtype=complex)
        r[np.arange(nbits), d] = np.exp(1j * th)
        r += (rng.standard_normal((nbits, 2)) + 1j * rng.standard_normal((nbits, 2))) * math.sqrt(n0 / 2)
        dec = np.argmax(np.abs(r), axis=1)
    return float(np.mean(dec != d))
