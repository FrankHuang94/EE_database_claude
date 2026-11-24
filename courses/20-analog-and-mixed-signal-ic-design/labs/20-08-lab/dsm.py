"""Lab 20-08: behavioral models of oversampling and delta-sigma converters.

Conventions: the output levels span [-1, 1] (a 1-bit quantizer outputs +-1, so its step is 2); 0 dBFS is a sine of
amplitude 1. Every modulator starts from zero states unless stated.

- mod1: first-order loop with a delaying integrator, u[n+1] = u[n] + x[n] - y[n], y[n] = sign(u[n]) (NTF 1 - z^-1).
- mod2: second-order loop, u1[n+1] = u1[n] + x[n] - y[n], u2[n+1] = u2[n] + u1[n] - 2 y[n], y[n] = Q(u2[n])
  (STF z^-2, NTF (1 - z^-1)^2).
- ef_mod: any NTF B(z)/A(z) (both monic) in error-feedback form, with an M-level quantizer.
- lee_ntf: an L-th-order NTF with zeros at z = 1 and Butterworth high-pass poles scaled to a chosen out-of-band gain.
- mash11: two first-order stages, the first optionally leaky (integrator pole 1 - eps), digitally recombined.
- ct1: the sampled equivalent of a continuous-time first-order loop with NRZ feedback and excess loop delay d (in
  clock periods, 0 <= d < 1).
- inband_sqnr, cic_gain, jitter_noise: measurement helpers.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, signal


def mod1(x, u0=0.0):
    """First-order delta-sigma modulator; returns (y, u) with u[n] the integrator value at sample n."""
    x = np.asarray(x, float)
    y = np.empty_like(x)
    u = np.empty_like(x)
    s = u0
    for n in range(x.size):
        u[n] = s
        y[n] = 1.0 if s >= 0 else -1.0
        s = s + x[n] - y[n]
    return y, u


def mod2(x, levels=2):
    """Second-order loop (CIFB, feedback coefficients 1 and 2) with an M-level quantizer; returns (y, u1, u2)."""
    x = np.asarray(x, float)
    y, s1, s2 = np.empty_like(x), np.empty_like(x), np.empty_like(x)
    u1 = u2 = 0.0
    for n in range(x.size):
        s1[n], s2[n] = u1, u2
        y[n] = quantize(u2, levels)
        u1, u2 = u1 + x[n] - y[n], u2 + u1 - 2 * y[n]
    return y, s1, s2


def quantize(w, levels):
    """Uniform quantizer with `levels` outputs spanning [-1, 1] (mid-rise for even counts); 1 bit is the sign."""
    if levels == 2:
        return 1.0 if w >= 0 else -1.0
    d = 2.0 / (levels - 1)
    return float(np.clip(np.round((w + 1) / d) * d - 1, -1, 1))


def ef_mod(x, b, a=(1.0,), levels=2):
    """Error-feedback modulator with NTF = B(z)/A(z) (coefficients in powers of z^-1, b[0] = a[0] = 1) and STF = 1.
    Returns (y, max |quantizer input|). An unstable loop shows a quantizer input that grows without bound."""
    x = np.asarray(x, float)
    b = np.asarray(b, float)
    a = np.asarray(a, float)
    order = max(b.size, a.size) - 1
    b = np.pad(b, (0, order + 1 - b.size))
    a = np.pad(a, (0, order + 1 - a.size))
    c = b - a                          # (NTF - 1) A = B - A has no z^0 term
    e_hist = np.zeros(order)
    g_hist = np.zeros(order)
    y = np.empty_like(x)
    wmax = 0.0
    for n in range(x.size):
        g = c[1:] @ e_hist - a[1:] @ g_hist
        w = x[n] + g
        wmax = max(wmax, abs(w))
        if not math.isfinite(w) or wmax > 1e9:
            y[n:] = np.nan
            return y, math.inf
        y[n] = quantize(w, levels)
        e_hist = np.roll(e_hist, 1)
        e_hist[0] = y[n] - w
        g_hist = np.roll(g_hist, 1)
        g_hist[0] = g
    return y, wmax


def lee_ntf(order, hinf=1.5):
    """NTF (1 - z^-1)^L / A(z), A from a Butterworth high-pass whose cutoff is chosen so that max |NTF| = hinf."""
    b = np.poly(np.ones(order))

    def excess(wc):
        _, aa = signal.butter(order, wc, "high")
        return 2.0 ** order / abs(np.polyval(aa / aa[0], -1.0)) - hinf
    wc = optimize.brentq(excess, 1e-4, 0.999)
    _, aa = signal.butter(order, wc, "high")
    return b, aa / aa[0]


def mash11(x, eps=0.0):
    """1-1 MASH: stage 2 quantizes -e1; output y = z^-1 y1 + (1 - z^-1) y2. Stage 1's integrator has pole 1 - eps."""
    x = np.asarray(x, float)
    y1, y2 = np.empty_like(x), np.empty_like(x)
    u1 = u2 = 0.0
    for n in range(x.size):
        y1[n] = 1.0 if u1 >= 0 else -1.0
        e1 = y1[n] - u1
        y2[n] = 1.0 if u2 >= 0 else -1.0
        u1 = (1 - eps) * u1 + x[n] - y1[n]
        u2 = u2 - e1 - y2[n]
    d1 = np.concatenate([[0.0], y1[:-1]])
    d2 = np.concatenate([[0.0], y2[:-1]])
    return d1 + y2 - d2


def ct1(x, d=0.0, u0=0.0, y_prev=1.0):
    """Sampled continuous-time first-order loop with NRZ DAC delayed by d periods: over each period the integrator
    sees y[n-1] for a fraction d and y[n] for 1 - d. x is the input averaged over each period. Returns (y, u)."""
    x = np.asarray(x, float)
    y, u = np.empty_like(x), np.empty_like(x)
    s, yp = u0, y_prev
    for n in range(x.size):
        u[n] = s
        y[n] = 1.0 if s >= 0 else -1.0
        s = s + x[n] - (1 - d) * y[n] - d * yp
        yp = y[n]
    return y, u


def inband_sqnr(y, m, osr):
    """SQNR (dB) of a coherent sine at bin m: Hann window, signal = bins m-2..m+2, noise = bins 3..N/(2 OSR)."""
    n = y.size
    s = np.abs(np.fft.rfft(y * np.hanning(n))) ** 2
    sig = s[m - 2:m + 3].sum()
    noise = s[3:n // (2 * osr) + 1].sum() - sig
    return 10 * math.log10(sig / noise)


def sqnr_formula(order, osr, amp=1.0, step=2.0):
    """Linear-model peak SQNR (dB): sine of amplitude amp, white quantization error of variance step^2/12."""
    pe = step ** 2 / 12 * math.pi ** (2 * order) / ((2 * order + 1) * osr ** (2 * order + 1))
    return 10 * math.log10(amp ** 2 / 2 / pe)


def cic_gain(f_over_fs, m, k):
    """|H| of a K-stage CIC decimator by M: [sin(pi f M / fs) / (M sin(pi f / fs))]^K."""
    f = np.asarray(f_over_fs, float)
    return np.abs(np.sin(np.pi * f * m) / (m * np.sin(np.pi * f))) ** k


def jitter_noise(y, sigma_t, fs, osr):
    """In-band noise power of NRZ-DAC clock jitter: E[(y[n] - y[n-1])^2] (sigma_t fs)^2 / OSR."""
    return np.mean(np.diff(y) ** 2) * (sigma_t * fs) ** 2 / osr
