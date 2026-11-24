"""Lab 22-01 helpers: efficiency and loss arithmetic, linear regulators, capacitor charging, the ideal buck's
periodic steady state, the P0 + aI + RI^2 loss model, power density and hold-up energy.

Everything here is closed-form or a matrix exponential; the verify script recomputes the published numbers by
other routes (ODE integration, Fourier sums, numerical minimization).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm

IN3 = 16.387064e-6  # m^3 per cubic inch


# ---------------------------------------------------------------- efficiency and loss
def loss_from_efficiency(p_out, eta):
    """Loss for a delivered power p_out at efficiency eta: P_out (1/eta - 1)."""
    return p_out * (1.0 / eta - 1.0)


def chain_efficiency(etas):
    return float(np.prod(etas))


def chain_losses(p_load, etas):
    """Loss in each stage of a chain (listed source to load) delivering p_load; returns (losses, p_in)."""
    losses = []
    p = p_load
    for eta in reversed(list(etas)):
        p_in = p / eta
        losses.append(p_in - p)
        p = p_in
    return losses[::-1], p


# ---------------------------------------------------------------- linear regulators
def ldo_efficiency(v_in, v_out, i_out, i_q):
    """Series regulator: input current = load current + quiescent (ground) current."""
    return v_out * i_out / (v_in * (i_out + i_q))


def buck_input_current(v_in, v_out, i_out, eta):
    return v_out * i_out / (eta * v_in)


# ---------------------------------------------------------------- capacitor charging and charge sharing
def charge_loss(c, v, steps=1):
    """Energy lost charging c from 0 to v through any resistance in `steps` equal voltage steps."""
    return 0.5 * c * v ** 2 / steps


def share_loss(c1, v1, c2, v2):
    """Energy lost when c1 at v1 is connected to c2 at v2."""
    return 0.5 * c1 * c2 / (c1 + c2) * (v1 - v2) ** 2


# ---------------------------------------------------------------- the ideal synchronous buck
def buck_pss(v_in, d, fs, ind, cap, r_load, npts=4001):
    """Exact periodic steady state of an ideal synchronous buck (ideal switches, L, C, resistive load).

    Returns (t, i_L, v_out) over one period, t from the start of the on-time.
    """
    t_s = 1.0 / fs
    a = np.array([[0.0, -1.0 / ind], [1.0 / cap, -1.0 / (r_load * cap)]])

    def aug(vs):
        m = np.zeros((3, 3))
        m[:2, :2] = a
        m[0, 2] = vs / ind
        return m

    p1 = expm(aug(v_in) * d * t_s)
    p2 = expm(aug(0.0) * (1 - d) * t_s)
    p = p2 @ p1
    x0 = np.linalg.solve(np.eye(2) - p[:2, :2], p[:2, 2])
    t = np.linspace(0.0, t_s, npts)
    il = np.empty_like(t)
    vo = np.empty_like(t)
    for k, tk in enumerate(t):
        m = expm(aug(v_in) * tk) if tk <= d * t_s else expm(aug(0.0) * (tk - d * t_s)) @ p1
        x = m[:2, :2] @ x0 + m[:2, 2]
        il[k], vo[k] = x
    return t, il, vo


def switch_node_harmonic(v_in, d, n):
    """Amplitude of the n-th harmonic of a 0/v_in rectangular wave with duty d."""
    return 2 * v_in / (n * math.pi) * abs(math.sin(n * math.pi * d))


# ---------------------------------------------------------------- the loss model
def model_loss(i, p0, a, r):
    return p0 + a * i + r * i ** 2


def model_efficiency(i, v_out, p0, a, r):
    return v_out * i / (v_out * i + model_loss(i, p0, a, r))


def peak_efficiency_current(p0, r):
    return math.sqrt(p0 / r)


def shed_current(n, p0, r):
    """Load at which n + 1 phases start to beat n phases (each phase: fixed loss p0, resistance r)."""
    return math.sqrt(n * (n + 1) * p0 / r)


def phased_loss(i, n, p0, a, r):
    return n * p0 + a * i + r * i ** 2 / n


# ---------------------------------------------------------------- density and hold-up
def density_w_per_in3(p, dims_mm):
    vol = dims_mm[0] * dims_mm[1] * dims_mm[2] * 1e-9 / IN3
    return p / vol, vol


def thermal_density_limit(q_w_per_in3, eta):
    """Largest power density a box can reach if it can reject q W/in^3 of heat."""
    return q_w_per_in3 * eta / (1 - eta)


def holdup_capacitance(p_bus, t_hold, v1, v2):
    return 2 * p_bus * t_hold / (v1 ** 2 - v2 ** 2)
