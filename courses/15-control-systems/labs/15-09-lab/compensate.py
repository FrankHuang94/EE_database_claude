"""Lab 15-09 helpers: lead and lag compensators, designed on the Bode plot and realized with RC networks.

A lead compensator is C(s) = (1 + alpha T s)/(1 + T s) with alpha > 1 (zero at 1/(alpha T), pole at 1/T).
A lag compensator is C(s) = (1 + s/z)/(1 + s/p) with z > p (it attenuates high frequencies by z/p).
Both have unity DC gain here, so the static gain K is chosen separately (for an error constant).

    lead_phase(alpha)                 maximum phase lead (deg), at w_m = 1/(T sqrt(alpha))
    lead_alpha(phi_deg)               alpha that gives a maximum lead of phi_deg
    design_lead(num, den, pm, extra)  lead for a phase-margin target (frequency-domain recipe of section 3.3)
    design_lag(num, den, pm, allowance, ratio)  lag for a phase-margin target (recipe of section 3.4)
    lead_rc(alpha, w_m, R2)           R1, C1 of the passive lead network R1||C1 in series, R2 to ground
    with_comp(num, den, cnum, cden)   series connection of plant and compensator polynomials
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "15-07-lab"))
from freqdomain import freq_resp, margins  # noqa: E402


def lead_phase(alpha):
    return math.degrees(math.asin((alpha - 1) / (alpha + 1)))


def lead_alpha(phi_deg):
    s = math.sin(math.radians(phi_deg))
    return (1 + s) / (1 - s)


def with_comp(num, den, cnum, cden):
    return np.polymul(num, cnum), np.polymul(den, cden)


def design_lead(num, den, pm, extra=10.0, w_lo=1e-3, w_hi=1e6):
    """Return dict(alpha, T, zero, pole, wm, phi) for a lead that lifts the loop to the target phase margin.

    Recipe: phi = pm - PM_uncompensated + extra; alpha from phi; put the lead's peak at the frequency where the
    uncompensated |L| = 1/sqrt(alpha), which becomes the new crossover.
    """
    m0 = margins(num, den, w_lo=w_lo, w_hi=w_hi)
    phi = pm - m0["pm"] + extra
    alpha = lead_alpha(phi)
    wm = brentq(lambda w: abs(freq_resp(num, den, w)) - 1 / math.sqrt(alpha), w_lo * 10, w_hi / 10)
    T = 1 / (wm * math.sqrt(alpha))
    return dict(alpha=alpha, T=T, zero=1 / (alpha * T), pole=1 / T, wm=wm, phi=phi,
                cnum=np.array([alpha * T, 1.0]), cden=np.array([T, 1.0]))


def design_lag(num, den, pm, allowance=5.0, ratio=10.0, w_lo=1e-4, w_hi=1e6):
    """Return dict(beta, zero, pole, wc) for a lag giving the target phase margin.

    Recipe: find the frequency where the uncompensated phase is -180 + pm + allowance; that becomes the new
    crossover; attenuate by beta = |L| there; put the zero 'ratio' times below the new crossover, the pole at zero/beta.
    """
    w = np.logspace(math.log10(w_lo), math.log10(w_hi), 200001)
    target = -180 + pm + allowance
    from freqdomain import _unwrapped_phase
    ph = np.degrees(_unwrapped_phase(np.asarray(num, float), np.asarray(den, float), w, 0.0))
    i = np.flatnonzero((ph[:-1] - target) * (ph[1:] - target) < 0)[0]
    wc = brentq(lambda x: float(np.degrees(_unwrapped_phase(np.asarray(num, float), np.asarray(den, float),
                                                            np.array([x]), 0.0))[0]) - target, w[i], w[i + 1])
    beta = abs(freq_resp(num, den, wc))
    z = wc / ratio
    p = z / beta
    return dict(beta=beta, zero=z, pole=p, wc=wc, cnum=np.array([1 / z, 1.0]), cden=np.array([1 / p, 1.0]))


def lead_rc(alpha, w_m, R2):
    """Passive lead: R1 || C1 in series, R2 to ground. alpha = (R1 + R2)/R2; zero 1/(R1 C1); w_m = zero * sqrt(alpha)."""
    R1 = (alpha - 1) * R2
    zero = w_m / math.sqrt(alpha)
    C1 = 1 / (R1 * zero)
    return R1, C1
