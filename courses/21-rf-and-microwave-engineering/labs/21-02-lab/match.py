"""Lab 21-02: matching networks.

- l_match: element reactances of a two-element L-network between real resistances (low-pass form).
- l_match_complex: L-network values for a complex load (absorbing its reactance).
- pi_match: pi network of chosen loaded Q between two resistances (two back-to-back L-networks via a virtual R).
- cascade_l: n-section L-network with geometric-mean intermediate resistances, per-section Q.
- binomial_transformer: characteristic impedances of an N-section binomial quarter-wave transformer (small-reflection
  theory with the logarithmic rule), and its fractional bandwidth for a maximum reflection.
- zin_network: input impedance of a ladder of series/shunt reactances (or lossy elements) terminated in a load, at
  any frequency, from lists of element types.
- bode_fano_bw: the Bode-Fano bandwidth limit for a parallel RC load and a constant in-band reflection.
"""
from __future__ import annotations

import math

import numpy as np


def l_match(r_low, r_high):
    """Series reactance (on the low side) and shunt susceptance (on the high side) magnitudes, and Q."""
    q = math.sqrt(r_high / r_low - 1)
    return q * r_low, q / r_high, q


def pi_match(r1, r2, q):
    """Pi network between r1 and r2 with loaded Q set by the larger resistance: returns (B1, X, B2) magnitudes and the
    virtual resistance. Both halves are L-networks down to r_v = max(r1, r2)/(q^2 + 1)."""
    rh = max(r1, r2)
    rv = rh / (q * q + 1)
    q1 = math.sqrt(r1 / rv - 1)
    q2 = math.sqrt(r2 / rv - 1)
    return q1 / r1, (q1 + q2) * rv, q2 / r2, rv


def cascade_l(r_low, r_high, n):
    ratio = (r_high / r_low) ** (1 / n)
    rs = [r_low * ratio ** k for k in range(n + 1)]
    return rs, math.sqrt(ratio - 1)


def binomial_transformer(z0, zl, n):
    """Binomial N-section quarter-wave transformer by the logarithmic rule ln(Z_{k+1}/Z_k) = 2^-N C(N,k) ln(ZL/Z0)."""
    zs = [z0]
    for k in range(n + 1):          # n sections have n + 1 junctions
        zs.append(zs[-1] * math.exp(2.0 ** -n * math.comb(n, k) * math.log(zl / z0)))
    return zs[1:-1], zs


def binomial_bandwidth(z0, zl, n, gamma_max):
    """Fractional bandwidth (Delta f / f0) of an N-section binomial transformer for |Gamma| <= gamma_max:
    |Gamma(theta)| = |A| 2^N |cos theta|^N with A = 2^-N (ZL - Z0)/(ZL + Z0)."""
    a = abs((zl - z0) / (zl + z0)) / 2 ** n
    theta_m = math.acos(0.5 * (gamma_max / a) ** (1 / n))
    return 2 - 4 * theta_m / math.pi


def gamma_of(zin, z0=50.0):
    return (zin - z0) / (zin + z0)


def zin_ladder(elements, zl, f):
    """elements: list from the load side outward of (kind, value[, q]) with kind in
    'sL' series inductor, 'sC' series capacitor, 'pL' shunt inductor, 'pC' shunt capacitor, 'line' (z, theta at f0, f0).
    An optional third entry is the element's unloaded Q (series resistance for L, shunt conductance for C)."""
    w = 2 * math.pi * f
    z = complex(zl)
    for el in elements:
        kind, val = el[0], el[1]
        q = el[2] if len(el) > 2 else None
        if kind in ("sL", "pL"):
            ze = 1j * w * val
            if q:
                ze += w * val / q
        elif kind in ("sC", "pC"):
            ze = 1 / (1j * w * val)
            if q:
                ze = 1 / (1j * w * val + w * val / q)
        if kind == "line":
            zc, theta0, f0 = val, el[2], el[3]
            th = theta0 * f / f0
            z = zc * (z + 1j * zc * math.tan(th)) / (zc + 1j * z * math.tan(th))
            continue
        z = z + ze if kind.startswith("s") else 1 / (1 / z + 1 / ze)
    return z


def bode_fano_bw(r, c, gamma_max):
    """Largest bandwidth (Hz) over which a parallel RC load can be matched with |Gamma| <= gamma_max."""
    return 1 / (2 * r * c * math.log(1 / gamma_max))
