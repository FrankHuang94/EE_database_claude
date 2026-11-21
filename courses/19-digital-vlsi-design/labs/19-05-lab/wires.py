"""Interconnect models for Lab 19-05.

Wire resistance and capacitance from geometry; the distributed RC line's step response (Fourier series) and its 50%
delay; Elmore delays of driver-wire-load paths; optimal repeater insertion; capacitive crosstalk and the Miller
factor; and scaling arithmetic. Units: SI (ohms, farads, metres, seconds) unless a name says otherwise.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

EPS0 = 8.8541878128e-12
LN2 = math.log(2)
K_LINE = 0.379  # 50% delay of a distributed RC line in units of R C (line_t50() = 0.3787), rounded


# ---------------------------------------------------------------- resistance and capacitance
def wire_resistance(rho: float, length: float, width: float, thickness: float) -> float:
    """R = rho L / (W t)."""
    return rho * length / (width * thickness)


def sheet_resistance(rho: float, thickness: float) -> float:
    return rho / thickness


def plate_cap_per_length(eps_r: float, width: float, height: float) -> float:
    """Parallel-plate capacitance per unit length to a plane a distance `height` below: eps W / h (F/m)."""
    return eps_r * EPS0 * width / height


def coupling_cap_per_length(eps_r: float, thickness: float, spacing: float) -> float:
    """Sidewall capacitance per unit length to one neighbour: eps t / s (F/m), no fringing."""
    return eps_r * EPS0 * thickness / spacing


# ---------------------------------------------------------------- distributed RC line
def line_step_response(theta: float, n_terms: int = 400) -> float:
    """Far-end voltage of an open-ended distributed RC line (total R, C) after a unit step at the near end, at
    normalized time theta = t / (R C): v = 1 - (4/pi) sum_n (-1)^n/(2n+1) exp(-(2n+1)^2 pi^2 theta / 4)."""
    n = np.arange(n_terms)
    return float(1 - 4 / math.pi * np.sum((-1.0) ** n / (2 * n + 1) * np.exp(-((2 * n + 1) ** 2) * math.pi ** 2
                                                                                 * theta / 4)))


def line_t50() -> float:
    """50% delay of the distributed line in units of R C (about K_LINE)."""
    return brentq(lambda th: line_step_response(th) - 0.5, 0.05, 2.0, xtol=1e-14)


def ladder_t50(n: int, r_total: float, c_total: float, r_drive: float = 0.0, c_load: float = 0.0) -> float:
    """Exact 50% delay at the far end of an n-section RC ladder (optionally with a driver resistance and a load
    capacitance) after a unit step, by the matrix exponential."""
    rs = [r_drive + r_total / n] + [r_total / n] * (n - 1)
    cs = [c_total / n] * (n - 1) + [c_total / n + c_load]
    m = len(cs)
    g = np.zeros((m, m))
    b = np.zeros(m)
    for i in range(m):
        gi = 1 / rs[i]
        g[i, i] += gi
        if i == 0:
            b[0] = gi
        else:
            g[i - 1, i - 1] += gi
            g[i - 1, i] -= gi
            g[i, i - 1] -= gi
    a = -g / np.array(cs)[:, None]
    vinf = np.linalg.solve(g, b)
    tau = sum(c * sum(rs[: i + 1]) for i, c in enumerate(cs))
    return brentq(lambda t: float((vinf - expm(a * t) @ vinf)[-1]) - 0.5, 1e-4 * tau, 5 * tau, xtol=1e-9 * tau)


def driver_wire_load_delay(r_d: float, r_w: float, c_w: float, c_l: float) -> float:
    """Standard estimate: 0.69 R_d (C_w + C_L) + R_w (0.379 C_w + 0.69 C_L)."""
    return LN2 * r_d * (c_w + c_l) + r_w * (K_LINE * c_w + LN2 * c_l)


# ---------------------------------------------------------------- repeaters
def repeater_optimum(r0: float, c0: float, r_w: float, c_w: float) -> tuple[float, float, float]:
    """Optimal number of segments k, repeater size h and minimum delay T for a wire (total R_w, C_w) driven by
    repeaters of size h (resistance r0/h, input capacitance h c0), using 0.69 for lumped and 0.38 for distributed
    terms and ignoring repeater self-loading:
    T(k, h) = 0.69 r0 c_w / h + 0.69 k r0 c0 + 0.38 r_w c_w / k + 0.69 r_w h c0."""
    k = math.sqrt(K_LINE * r_w * c_w / (LN2 * r0 * c0))
    h = math.sqrt(r0 * c_w / (r_w * c0))
    return k, h, repeated_delay(k, h, r0, c0, r_w, c_w)


def repeated_delay(k: float, h: float, r0: float, c0: float, r_w: float, c_w: float) -> float:
    return LN2 * r0 * c_w / h + LN2 * k * r0 * c0 + K_LINE * r_w * c_w / k + LN2 * r_w * h * c0


# ---------------------------------------------------------------- crosstalk
def floating_victim_noise(v_agg: float, c_c: float, c_g: float) -> float:
    """Step on a floating victim: dV = V_agg C_c / (C_c + C_g)."""
    return v_agg * c_c / (c_c + c_g)


def effective_cap(c_g: float, c_c_each: float, miller: list[float]) -> float:
    """Ground capacitance plus coupling capacitances, each multiplied by its Miller factor (0, 1 or 2)."""
    return c_g + sum(c_c_each * m for m in miller)
