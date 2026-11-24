"""Lab 20-07: behavioral models of Nyquist-rate ADC architectures.

- Flash: thermometer code from 2^N - 1 comparators and a ones-counting encoder (bubble tolerant).
- SAR: charge-redistribution DAC switching energy, conventional (trial and revert, chapter section 3.3) and monotonic
  (Liu et al., 2010), by explicit charge bookkeeping on the top plates; a SAR with arbitrary (e.g. redundant) bit
  weights and a DAC settling error on the early decisions.
- Pipeline: 1.5-bit stages (thresholds +-V_REF/4, residue g (2 v - D V_REF)) with comparator offsets and stage gain
  errors, plus an ideal backend flash.
- Time interleaving: M channels with offset, gain and timing-skew mismatch.
All voltages in volts; energies in units of C_u V_REF^2 where stated.
"""
from __future__ import annotations

import math

import numpy as np


# ------------------------------------------------------------------ flash
def flash_thermometer(v, thresholds):
    """Comparator outputs (1 if v > threshold) for inputs v (array) against sorted thresholds."""
    return (np.asarray(v, float)[..., None] > np.asarray(thresholds)[None, :]).astype(int)


def ones_count(thermo):
    """Ones-counting encoder: the output code is the number of comparators that fired (tolerates bubbles)."""
    return thermo.sum(axis=-1)


def first_transition(thermo):
    """Naive encoder: the code is the position of the first 1->0 transition (a bubble makes it wrong)."""
    out = []
    for row in np.atleast_2d(thermo):
        k = 0
        while k < row.size and row[k] == 1:
            k += 1
        out.append(k)
    return np.array(out)


# ------------------------------------------------------------------ SAR switching energy
def _from_vref(caps, st0, st1, vx0, vx1, vref):
    """Energy drawn from V_REF in one transition: V_REF times the charge into bottom plates held at V_REF."""
    return vref * sum(caps[i] * ((st1[i] - vx1) - (st0[i] - vx0)) for i in range(len(caps)) if st1[i] == vref)


def conventional_energy(n, vin, vref=1.0):
    """Single-ended conventional SAR (bit caps 2^i plus a unit dummy, top plate at -vin after sampling): energy of the
    N trial transitions (each trial switches the new bit up and, if the previous trial failed, that bit down)."""
    caps = np.array([2.0 ** i for i in range(n)] + [1.0])
    ct = caps.sum()
    q = -ct * vin

    def vx(st):
        return (q + (caps * st).sum()) / ct
    st = np.zeros(n + 1)
    x = vx(st)
    kept = np.zeros(n + 1)
    e = 0.0
    for b in range(n - 1, -1, -1):
        new = kept.copy()
        new[b] = vref
        xn = vx(new)
        e += _from_vref(caps, st, new, x, xn, vref)
        st, x = new, xn
        if x <= 0:
            kept[b] = vref
    return e


def conventional_energy_avg(n):
    """Differential average over all codes: twice the single-ended average (closed form for checking)."""
    return 2 * np.mean([conventional_energy(n, (c + 0.5) / 2 ** n) for c in range(2 ** n)])


def monotonic_energy(n, vin_diff, vref=1.0):
    """Monotonic switching: each side has caps 2^(n-2)..1 plus a unit dummy, bottoms start at V_REF, inputs are
    sampled on the top plates, and after each comparison the higher side's next cap drops from V_REF to 0."""
    caps = np.array([2.0 ** i for i in range(n - 1)][::-1] + [1.0])
    ct = caps.sum()
    out = 0.0
    sides = []
    for vtop in (vref / 2 + vin_diff / 2, vref / 2 - vin_diff / 2):
        sides.append({"q": ct * vtop - (caps * vref).sum(), "st": np.full(caps.size, vref)})
    for s in sides:
        s["x"] = (s["q"] + (caps * s["st"]).sum()) / ct
    for k in range(n - 1):
        s = sides[0] if sides[0]["x"] > sides[1]["x"] else sides[1]
        new = s["st"].copy()
        new[k] = 0.0
        xn = (s["q"] + (caps * new).sum()) / ct
        out += _from_vref(caps, s["st"], new, s["x"], xn, vref)
        s["st"], s["x"] = new, xn
    return out


# ------------------------------------------------------------------ SAR with arbitrary weights
def sar_convert(v, weights, vref=1.0, settle_err=None):
    """SAR with bit weights (in units of vref/sum, largest first) on input v in [0, vref). Each trial compares v with
    the DAC value of the trial code; settle_err[k] adds an error (volts) to the DAC value at decision k (incomplete
    settling). Returns the reconstructed value sum(kept weights) / sum(weights) * vref."""
    w = np.asarray(weights, float)
    full = w.sum() + 1.0           # +1 LSB-sized unit so codes span [0, full)
    v = np.asarray(v, float)
    acc = np.zeros(v.shape)
    for k, wk in enumerate(w):
        trial = acc + wk
        err = 0.0 if settle_err is None else settle_err[k]
        keep = v >= trial / full * vref + err
        acc = np.where(keep, trial, acc)
    return acc / full * vref


# ------------------------------------------------------------------ pipeline
def pipeline(v, n_stages=8, vref=1.0, offsets=None, gains=None, backend_bits=2):
    """1.5-bit-per-stage pipeline on v in [-vref, vref]; returns output codes (ideal digital weights)."""
    v = np.asarray(v, float)
    offsets = np.zeros((n_stages, 2)) if offsets is None else np.asarray(offsets)
    gains = np.ones(n_stages) if gains is None else np.asarray(gains)
    out = np.zeros(v.shape)
    r = v.copy()
    for i in range(n_stages):
        d = np.where(r > vref / 4 + offsets[i, 1], 1, np.where(r < -vref / 4 + offsets[i, 0], -1, 0))
        out += d * 2.0 ** (n_stages - 1 - i) * 2 ** backend_bits / 2
        r = gains[i] * (2 * r - d * vref)
    nb = 2 ** backend_bits
    out += np.clip(np.floor((r + vref) / (2 * vref) * nb), 0, nb - 1) - nb / 2 + 0.5
    return out


def mdac_residue(vin, d_vref, cs, cf, cp, a):
    """Flip-around MDAC hold-phase output with finite op-amp gain a and summing-node parasitic cp."""
    return ((cs + cf) * vin - cs * d_vref) / (cf + (cs + cf + cp) / a)


# ------------------------------------------------------------------ time interleaving
def ti_capture(m_ch, fs, n, m_bin, amp, offs, gains, skews):
    """Samples of a coherent sine taken round-robin by m_ch channels with offset, gain and timing-skew mismatch."""
    t = np.arange(n) / fs
    ch = np.arange(n) % m_ch
    f = m_bin * fs / n
    return gains[ch] * amp * np.sin(2 * np.pi * f * (t + skews[ch])) + offs[ch], f


def power_spectrum(x):
    """One-sided power per bin (signal power A^2/2 for a sine); DC and Nyquist bins counted once."""
    n = x.size
    s = np.abs(np.fft.rfft(x)) ** 2 / n ** 2 * 2
    s[0] /= 2
    if n % 2 == 0:
        s[-1] /= 2
    return s


def spur_dbc(s, m_sig, b):
    return 10 * math.log10(s[b] / s[m_sig])
