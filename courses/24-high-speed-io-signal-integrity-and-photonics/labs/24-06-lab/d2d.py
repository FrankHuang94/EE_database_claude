"""Short-reach link models for chapter 24-06.

Wire energy (unterminated CV^2/4 and terminated V^2/(4 R f_b)), an RC-ladder step response solved exactly by
eigen-decomposition, Elmore delay, bump density and bandwidth density, and fabric bandwidth arithmetic.
"""
from __future__ import annotations

import numpy as np
from scipy import optimize


def unterminated_energy(c: float, v: float) -> float:
    """Energy per bit for random data: C V^2 / 4 (joules)."""
    return c * v * v / 4


def terminated_energy(v: float, r: float, f_b: float) -> float:
    """Energy per bit of a doubly terminated wire high half the time: V^2/(4 R f_b)."""
    return v * v / (4 * r * f_b)


def ladder(ron: float, rw: float, cw: float, cpad: float, n: int = 40):
    """Conductance matrix G and node capacitances C of a driver plus an n-section RC wire with end pads."""
    m = n + 1
    c = np.full(m, cw / n)
    c[0] = c[-1] = cw / n / 2 + cpad
    g = np.zeros((m, m))
    r = rw / n
    for i in range(n):
        g[i, i] += 1 / r
        g[i + 1, i + 1] += 1 / r
        g[i, i + 1] -= 1 / r
        g[i + 1, i] -= 1 / r
    g[0, 0] += 1 / ron
    return g, c


def step_response(g: np.ndarray, c: np.ndarray, v: float):
    """Exact node voltages x(t) after a step of v at the driver, via the symmetric form C^-1/2 G C^-1/2."""
    d = np.sqrt(c)
    lam, q = np.linalg.eigh(g / np.outer(d, d))
    xss = np.full(len(c), v)
    y0 = q.T @ (d * xss)
    return lambda t: xss - (q @ (np.exp(-lam * t) * y0)) / d


def crossing(x_of_t, node: int, level: float, t_max: float = 1e-9) -> float:
    return optimize.brentq(lambda t: x_of_t(t)[node] - level, 1e-18, t_max, xtol=1e-18)


def elmore(ron: float, rw: float, cw: float, cpad_near: float, cpad_far: float) -> float:
    ctot = cw + cpad_near + cpad_far
    return ron * ctot + rw * (cw / 2 + cpad_far)


def bumps_per_mm2(pitch_um: float) -> float:
    return (1000 / pitch_um) ** 2


def areal_density_gbps_mm2(pitch_um: float, rate_gbps: float, data_fraction: float = 0.5) -> float:
    """GB/s per mm^2."""
    return bumps_per_mm2(pitch_um) * data_fraction * rate_gbps / 8


def power_w(bandwidth_bytes_per_s: float, pj_per_bit: float) -> float:
    return bandwidth_bytes_per_s * 8 * pj_per_bit * 1e-12
