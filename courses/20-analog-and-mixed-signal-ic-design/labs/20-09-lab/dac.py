"""Lab 20-09: behavioral models of digital-to-analog converters.

- r2r_output: a voltage-mode R-2R ladder solved by nodal analysis, with optional resistor mismatch and switch resistance.
- string_dac: a resistor-string DAC's tap voltages with optional mismatch.
- cs_levels: output levels of a current-steering DAC built from unary (thermometer) and binary cells with random
  unit-current mismatch; segmented designs use unary cells of 2^B units for the MSBs and binary cells for B LSBs.
- inl_dnl: endpoint INL and DNL (in LSB) of a level list.
- zout_levels: single-ended and differential outputs of a current-steering DAC whose unit cells have finite output
  impedance (normalized x = R_L / Z_unit).
- harmonics: harmonic levels of a static nonlinearity driven by a full-scale sine (FFT of one period).
- zoh_gain: the sinc response of an NRZ (zero-order-hold) output, and of RZ and mixed-mode (RF) outputs.
- dwa_select: data-weighted averaging element selection.
"""
from __future__ import annotations

import math

import numpy as np


def r2r_output(code, nbits, vref=1.0, r=1.0, mism_r=None, mism_2r=None, r_sw=0.0):
    """Voltage-mode R-2R ladder: bit k (k = 0 is the LSB) drives a 2R leg from V_REF (bit 1) or ground (bit 0) through a
    switch of resistance r_sw; series R between nodes; the LSB end is terminated by 2R to ground; the output is the MSB
    node (unloaded). Returns the output voltage."""
    n = nbits
    rr = r * (1 + (np.zeros(n - 1) if mism_r is None else np.asarray(mism_r)))     # series R between node k and k+1
    r2 = 2 * r * (1 + (np.zeros(n + 1) if mism_2r is None else np.asarray(mism_2r)))  # n legs + LSB termination
    g = np.zeros((n, n))
    b = np.zeros(n)
    for k in range(n):
        gl = 1.0 / (r2[k] + r_sw)
        g[k, k] += gl
        b[k] += gl * (vref if (code >> k) & 1 else 0.0)
        if k == 0:
            g[0, 0] += 1.0 / r2[n]
        if k < n - 1:
            gs = 1.0 / rr[k]
            g[k, k] += gs
            g[k + 1, k + 1] += gs
            g[k, k + 1] -= gs
            g[k + 1, k] -= gs
    return float(np.linalg.solve(g, b)[n - 1])


def string_dac(nbits, vref=1.0, mism=None):
    """Tap voltages of a 2^N-resistor string between ground and V_REF (taps 0 .. 2^N - 1)."""
    r = 1 + (np.zeros(2 ** nbits) if mism is None else np.asarray(mism))
    return vref * np.concatenate([[0.0], np.cumsum(r)[:-1]]) / r.sum()


def cs_levels(nbits, n_unary_bits, sigma, rng):
    """Levels (in units of the nominal LSB current) for all 2^N codes of a segmented current-steering DAC: the top
    n_unary_bits are thermometer-decoded into 2^M - 1 cells of 2^B units, the B = N - M LSBs are binary cells of 2^k
    units. Every unit has an independent relative error N(0, sigma); a cell of w units has error sigma * sqrt(w)."""
    m = n_unary_bits
    b = nbits - m
    unary = 2 ** b * (1 + rng.normal(0, sigma / math.sqrt(2 ** b), 2 ** m - 1))
    binary = np.array([2 ** k * (1 + rng.normal(0, sigma / math.sqrt(2 ** k))) for k in range(b)])
    codes = np.arange(2 ** nbits)
    hi, lo = codes >> b, codes & (2 ** b - 1)
    cum_u = np.concatenate([[0.0], np.cumsum(unary)])
    lo_val = np.array([sum(binary[k] for k in range(b) if (c >> k) & 1) for c in range(2 ** b)]) if b else np.zeros(1)
    return cum_u[hi] + lo_val[lo]


def inl_dnl(levels):
    """Endpoint INL (per code) and DNL (per transition) in LSB."""
    levels = np.asarray(levels, float)
    lsb = (levels[-1] - levels[0]) / (levels.size - 1)
    inl = (levels - levels[0]) / lsb - np.arange(levels.size)
    dnl = np.diff(levels) / lsb - 1
    return inl, dnl


def zout_levels(nt, x, differential=False):
    """Output (in units of I_unit * R_L) for n = 0..nt on cells, each with output impedance Z = R_L / x, into R_L.
    Single-ended: n / (1 + n x). Differential: the complementary side carries nt - n cells."""
    n = np.arange(nt + 1, dtype=float)
    se = n / (1 + n * x)
    if not differential:
        return se
    return se - (nt - n) / (1 + (nt - n) * x)


def harmonics(f, npts=4096, kmax=5):
    """Apply a static function f(s) to a full-scale sine s in [-1, 1]; return amplitudes of harmonics 1..kmax relative
    to the fundamental (dBc for k >= 2)."""
    s = np.sin(2 * np.pi * np.arange(npts) / npts)
    spec = np.abs(np.fft.rfft(f(s))) / (npts / 2)
    return {k: 20 * math.log10(spec[k] / spec[1]) if k > 1 else spec[1] for k in range(1, kmax + 1)}


def zoh_gain(f_over_fs, mode="nrz"):
    """Magnitude response of a DAC output pulse: NRZ (full-period hold), RZ (half-period pulse, half amplitude of the
    area), or mixed-mode (+1 for the first half period, -1 for the second), normalized so NRZ has unit DC gain."""
    f = np.asarray(f_over_fs, float)
    if mode == "nrz":
        return np.abs(np.sinc(f))
    if mode == "rz":
        return 0.5 * np.abs(np.sinc(f / 2))
    if mode == "mix":
        return np.abs(np.sinc(f / 2) * np.sin(np.pi * f / 2))
    raise ValueError(mode)


def dwa_select(codes, n_units):
    """Data-weighted averaging: each sample uses the next `code` elements in rotation. Returns a (samples x n_units)
    0/1 selection matrix."""
    sel = np.zeros((len(codes), n_units), dtype=int)
    ptr = 0
    for i, c in enumerate(codes):
        idx = (ptr + np.arange(c)) % n_units
        sel[i, idx] = 1
        ptr = (ptr + c) % n_units
    return sel
