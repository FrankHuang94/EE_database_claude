"""Lab 15-12 helpers: the three loops in every chip (clock, power, thermal).

PLL (phase-domain linear model, charge pump with loop filter R + C in series, C2 across them):
    pll_design(fc, pm_deg, Icp, Kv, N)   components for crossover fc (Hz) at the maximum phase margin pm_deg
    pll_loop(Icp, Kv, N, R, C, C2)       loop gain L(s) = K(1 + s tz)/[s^2 (1 + s tp)] as (num, den)
    closed(num, den)                     T = L/(1 + L) as (num, den)
    peaking(numT, denT)                  peak of |T(jw)| in dB and its frequency (Hz)
    bw3db(numT, denT)                    -3 dB frequency of T (Hz)
    phase_error_peak(num, den, dw, t_end) largest PFD phase error (rad) after a reference frequency step dw (rad/s)
    jitter(fc, ...)                      rms phase (rad) and jitter (s) from reference and VCO noise, max-PM loop at fc

Regulators:
    ldo_loop(Re, ...)                    LDO loop gain with error-amplifier, gate and output poles and the ESR zero
    esr_window(pm_min, ...)              ESR range (ohm) giving at least pm_min degrees of phase margin
    droop(dI, C, wc, wz, t)              output deviation after a load step dI for a transconductance regulator
                                         with PI gain g(1 + wz/s) and crossover wc = g/C (wz = 0: proportional)

Thermal:
    two_node(CJ, RJC, CH, RCA)           state matrices (A, B) of the junction / heat-sink model of 15-01
    throttle(...)                        sampled velocity-form PI power limiter (the ACPI passive-cooling form)

Polynomials are highest power first. The margins come from labs/15-07-lab/freqdomain.py and the step
specifications from labs/15-03-lab/specs.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar

_HERE = Path(__file__).resolve().parent
for _lab in ("15-07-lab", "15-03-lab"):
    sys.path.insert(0, str(_HERE.parent / _lab))
from freqdomain import freq_resp, margins  # noqa: E402
from specs import impulse_at, step_at  # noqa: E402


# ---------------------------------------------------------------- PLL
def pll_design(fc, pm_deg, Icp, Kv, N):
    """Place crossover at the peak of the phase curve: wc = 1/sqrt(tz tp), PM = atan((b - 1)/(2 sqrt b))."""
    wc = 2 * math.pi * fc
    t = math.tan(math.radians(pm_deg))
    x = t + math.sqrt(t * t + 1)              # x = sqrt(b) solves x^2 - 2 t x - 1 = 0
    b = x * x
    tz, tp = x / wc, 1 / (wc * x)
    K = wc**2 / x                             # |L(j wc)| = (K / wc^2) sqrt(b) = 1
    Ctot = Icp * Kv / (2 * math.pi * N * K)
    C2 = Ctot / b                             # tp / tz = C2 / (C + C2)
    C = Ctot - C2
    return {"b": b, "x": x, "tz": tz, "tp": tp, "K": K, "Ctot": Ctot, "C": C, "C2": C2, "R": tz / C}


def pll_loop(Icp, Kv, N, R, C, C2=0.0):
    K = Icp * Kv / (2 * math.pi * N * (C + C2))
    tz = R * C
    if C2 == 0:
        return np.array([K * tz, K]), np.array([1.0, 0.0, 0.0])
    tp = R * C * C2 / (C + C2)
    return np.array([K * tz, K]), np.array([tp, 1.0, 0.0, 0.0])


def closed(num, den):
    num, den = np.asarray(num, float), np.asarray(den, float)
    return num, np.polyadd(den, num)


def peaking(numT, denT, f_lo=1.0, f_hi=1e10):
    g = lambda lf: -abs(freq_resp(numT, denT, 2 * math.pi * 10**lf))  # noqa: E731
    lf = np.linspace(math.log10(f_lo), math.log10(f_hi), 20001)
    mag = np.abs(freq_resp(numT, denT, 2 * math.pi * 10**lf))
    k = int(np.argmax(mag))
    r = minimize_scalar(g, bounds=(lf[max(k - 1, 0)], lf[min(k + 1, lf.size - 1)]), method="bounded",
                        options={"xatol": 1e-12})
    return 20 * math.log10(-r.fun), 10**r.x


def bw3db(numT, denT, f_lo=1.0, f_hi=1e10):
    dc = abs(np.polyval(numT, 0) / np.polyval(denT, 0))
    lf = np.linspace(math.log10(f_lo), math.log10(f_hi), 20001)
    mag = np.abs(freq_resp(numT, denT, 2 * math.pi * 10**lf)) / dc
    k = int(np.flatnonzero(mag < 1 / math.sqrt(2))[0])
    h = lambda f: abs(freq_resp(numT, denT, 2 * math.pi * f)) / dc - 1 / math.sqrt(2)  # noqa: E731
    return brentq(h, 10 ** lf[k - 1], 10 ** lf[k], xtol=1e-12, rtol=1e-14)


def phase_error_peak(num, den, dw, t_end, n=200001):
    """PFD phase error after a reference frequency step dw: E(s) = (dw/s^2) S(s), S = den/(den + num).

    Because S has a double zero at s = 0 (type 2), E(s) = dw * den'(s)/(den + num) with den = s^2 den'(s):
    the error is dw times the impulse response of den'/(den + num).
    """
    num, den = np.asarray(num, float), np.asarray(den, float)
    dprime = den[:-2]                         # remove the s^2 factor
    dcl = np.polyadd(den, num)
    t = np.linspace(0, t_end, n)
    e = dw * np.array([impulse_at(dprime, dcl, tt) for tt in t])
    k = int(np.argmax(np.abs(e)))
    r = minimize_scalar(lambda tt: -abs(dw * impulse_at(dprime, dcl, tt)), bounds=(t[max(k - 1, 0)], t[min(k + 1, n - 1)]),
                        method="bounded", options={"xatol": 1e-15})
    return -r.fun, r.x


def jitter(fc, L_ref=-110.0, L_vco_1M=-120.0, f1=1e4, f2=1e8, f_out=2e9, pm_deg=60.0):
    """Integrated rms phase and jitter of a max-PM third-order loop with crossover fc.

    Reference-path noise L_ref (dBc/Hz, flat, already referred to the output) passes through |T|^2;
    VCO noise L_vco_1M at 1 MHz offset falling 20 dB/decade passes through |S|^2. The rms phase is
    sqrt(2 * integral of L(f) df) from f1 to f2 (single-sideband L), and jitter = phase/(2 pi f_out).
    """
    d = pll_design(fc, pm_deg, 1.0, 1.0, 1.0)
    num, den = np.array([d["K"] * d["tz"], d["K"]]), np.array([d["tp"], 1.0, 0.0, 0.0])

    def density(lf):
        f = 10**lf
        L = complex(freq_resp(num, den, 2 * math.pi * f))
        T, S = L / (1 + L), 1 / (1 + L)
        p = 10 ** (L_ref / 10) * abs(T) ** 2 + 10 ** ((L_vco_1M + 20 * math.log10(1e6 / f)) / 10) * abs(S) ** 2
        return p * f * math.log(10)

    val, _ = quad(density, math.log10(f1), math.log10(f2), limit=500, epsabs=0, epsrel=1e-11)
    phi = math.sqrt(2 * val)
    return phi, phi / (2 * math.pi * f_out)


# ---------------------------------------------------------------- regulators
def ldo_loop(Re, A0=1000.0, wa=2 * math.pi * 1e4, gm=0.5, RL=10.0, beta=0.5, wg=2 * math.pi * 1e6, CL=10e-6):
    """L(s) = A0 beta gm Z(s) / [(1 + s/wa)(1 + s/wg)], Z = RL || (Re + 1/(s CL))."""
    num = A0 * beta * gm * RL * np.array([Re * CL, 1.0])
    den = np.polymul(np.polymul([1 / wa, 1.0], [1 / wg, 1.0]), [(RL + Re) * CL, 1.0])
    return num, den


def ldo_pm(Re, **kw):
    return margins(*ldo_loop(Re, **kw), w_lo=1.0, w_hi=1e10)["pm"]


def esr_window(pm_min=45.0, lo=1e-3, hi=10.0, **kw):
    lr = np.linspace(math.log10(lo), math.log10(hi), 161)
    pms = np.array([ldo_pm(10**x, **kw) for x in lr])
    k = int(np.argmax(pms))
    best = minimize_scalar(lambda x: -ldo_pm(10**x, **kw), bounds=(lr[max(k - 1, 0)], lr[min(k + 1, lr.size - 1)]),
                           method="bounded", options={"xatol": 1e-10})
    rb = 10**best.x
    f = lambda r: ldo_pm(r, **kw) - pm_min  # noqa: E731
    return brentq(f, lo, rb, xtol=1e-14, rtol=1e-12), brentq(f, rb, hi, xtol=1e-14, rtol=1e-12), rb, -best.fun


def droop(dI, C, wc, wz, t):
    """v(t) for a load-current step dI: V(s) = -(dI/s) * s / [C (s^2 + wc s + wc wz)] (wz = 0: proportional)."""
    t = np.asarray(t, float)
    num, den = np.array([-dI / C]), np.array([1.0, wc, wc * wz])
    return np.array([impulse_at(num, den, tt) for tt in np.atleast_1d(t)])


# ---------------------------------------------------------------- thermal
def two_node(CJ=5.0, RJC=0.15, CH=300.0, RCA=0.35):
    A = np.array([[-1 / (CJ * RJC), 1 / (CJ * RJC)],
                  [1 / (CH * RJC), -1 / (CH * RJC) - 1 / (CH * RCA)]])
    B = np.array([1 / CJ, 0.0])
    return A, B


def throttle(Kp, Ki, Ts=0.1, T_lim=95.0, T_amb=30.0, P_max=200.0, P_min=0.0, t_end=400.0, model=None):
    """Sampled power limiter in velocity form (ACPI passive cooling, Equations 1 and 2):

        dP_k = Kp (T_k - T_{k-1}) + Ki Ts (T_k - T_lim),   P_k = clamp(P_{k-1} - dP_k, P_min, P_max)

    applied through a zero-order hold to the two-node model. Returns (t, T_J, P) at the sample instants and
    the time of the first sample at which P falls below P_max.
    """
    A, B = two_node(**(model or {}))
    M = np.zeros((3, 3))
    M[:2, :2] = A
    M[:2, 2] = B
    E = expm(M * Ts)
    x = np.zeros(2)
    P, T_prev = P_max, T_amb
    ts, TJ, Ps, t_thr = [], [], [], None
    for k in range(int(round(t_end / Ts))):
        Tn = T_amb + x[0]
        dP = Kp * (Tn - T_prev) + Ki * Ts * (Tn - T_lim)
        P = min(P_max, max(P_min, P - dP))
        T_prev = Tn
        if t_thr is None and P < P_max - 1e-12:
            t_thr = k * Ts
        ts.append(k * Ts)
        TJ.append(Tn)
        Ps.append(P)
        x = (E @ np.append(x, P))[:2]
    return np.array(ts), np.array(TJ), np.array(Ps), t_thr


__all__ = ["pll_design", "pll_loop", "closed", "peaking", "bw3db", "phase_error_peak", "jitter", "ldo_loop",
           "ldo_pm", "esr_window", "droop", "two_node", "throttle", "margins", "freq_resp", "step_at"]
