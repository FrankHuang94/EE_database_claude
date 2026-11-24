"""Lab 22-07 helpers: averaged small-signal models, compensator design, current-mode slope compensation,
load-step and delay estimates. SI units; transfer functions are evaluated at a frequency f in Hz."""
from __future__ import annotations

import cmath
import math


def _s(f):
    return 2j * math.pi * f


# ---------------------------------------------------------------- plants
def buck_gvd(f, vg, l, c, r):
    s = _s(f)
    return vg / (1 + s * l / r + s * s * l * c)


def buck_zout(f, l, c, r):
    s = _s(f)
    return s * l / (1 + s * l / r + s * s * l * c)


def buck_f0_q(l, c, r):
    return 1 / (2 * math.pi * math.sqrt(l * c)), r * math.sqrt(c / l)


def boost_gvd(f, v, d, l, c, r):
    s, dp = _s(f), 1 - d
    return (v / dp) * (1 - s * l / (dp * dp * r)) / (1 + s * l / (dp * dp * r) + s * s * l * c / (dp * dp))


def boost_rhp_zero_hz(d, l, r):
    return (1 - d) ** 2 * r / (2 * math.pi * l)


# ---------------------------------------------------------------- compensation
def kfactor(pm_deg, plant_phase_deg, kind="III"):
    """Type III: boost B = 2(2 atan k − 90°); type II: B = 2 atan k − 90°. Returns (boost, k)."""
    b = pm_deg - 90 - plant_phase_deg
    half = b / 2 if kind == "III" else b
    return b, math.tan(math.radians((half + 90) / 2))


def type3(f, w_i, fz, fp):
    s = _s(f)
    return w_i / s * (1 + s / (2 * math.pi * fz)) ** 2 / (1 + s / (2 * math.pi * fp)) ** 2


def type3_components(r1, w_i, k, fz, fp):
    """Returns C1, C2, R2, R3, C3 for the classic op-amp type-III network."""
    c12 = 1 / (w_i * r1)
    c2 = c12 / k ** 2
    c1 = c12 - c2
    r2 = 1 / (2 * math.pi * fz * c1)
    r3 = r1 / (k ** 2 - 1)
    c3 = 1 / (2 * math.pi * fp * r3)
    return c1, c2, r2, r3, c3


def crossover_and_pm(loop, f_lo=10.0, f_hi=1e7, n=4000):
    """Find |T| = 1 by bisection on a log grid, return (f_c, phase margin in degrees)."""
    import numpy as np
    fs = np.logspace(math.log10(f_lo), math.log10(f_hi), n)
    mags = np.array([abs(loop(f)) for f in fs])
    idx = int(np.where(mags < 1)[0][0])
    lo, hi = fs[idx - 1], fs[idx]
    for _ in range(100):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if abs(loop(mid)) > 1 else (lo, mid)
    fc = math.sqrt(lo * hi)
    return fc, 180 + math.degrees(cmath.phase(loop(fc)))


# ---------------------------------------------------------------- current mode
def perturbation_ratio(m1, m2, ma=0.0):
    return -(m2 - ma) / (m1 + ma)


# ---------------------------------------------------------------- transients and delay
def droop(delta_i, fc, c):
    return delta_i / (2 * math.pi * fc * c)


def delay_phase_deg(fc, td):
    return 360 * fc * td
