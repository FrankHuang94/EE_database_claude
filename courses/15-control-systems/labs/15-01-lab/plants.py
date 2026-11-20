"""Plant models for Lab 15-01: the chapter's systems as state-space matrices and nonlinear right-hand sides.

- `msd(m, b, k)`: mass-spring-damper, states (x, v), input force. `analogs(m, b, k)` gives the force-voltage
  and force-current circuit values.
- `motor(R, L, K, J, B)`: DC motor, states (i, omega), input voltage; `motor_first_order` drops L.
- `thermal_two_node(Rjc, Rca, Cj, Ch)`: junction and heat-sink nodes, states are rises above ambient, input power.
- `leakage_rhs(...)`: the nonlinear one-node thermal model with temperature-dependent leakage.
- `pendulum_rhs(g, L)`: the nonlinear pendulum, angle measured from straight down.
- `step(A, B, u, t)`: the exact response x(t) = (e^{At} - I) A^{-1} B u from rest, via the matrix exponential.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm


def msd(m: float, b: float, k: float):
    A = np.array([[0.0, 1.0], [-k / m, -b / m]])
    B = np.array([0.0, 1.0 / m])
    return A, B


def analogs(m: float, b: float, k: float) -> dict:
    return {"force-voltage": {"L": m, "R": b, "C": 1 / k}, "force-current": {"C": m, "R": 1 / b, "L": 1 / k}}


def motor(R: float, L: float, K: float, J: float, B: float):
    A = np.array([[-R / L, -K / L], [K / J, -B / J]])
    Bv = np.array([1 / L, 0.0])
    return A, Bv


def motor_first_order(R: float, K: float, J: float, B: float) -> tuple[float, float]:
    """Gain (rad/s per volt) and time constant of the model with L = 0."""
    return K / (R * B + K * K), R * J / (R * B + K * K)


def thermal_two_node(Rjc: float, Rca: float, Cj: float, Ch: float):
    A = np.array([[-1 / (Rjc * Cj), 1 / (Rjc * Cj)], [1 / (Rjc * Ch), -(1 / Rjc + 1 / Rca) / Ch]])
    Bv = np.array([1 / Cj, 0.0])
    return A, Bv


def leakage_rhs(Pd: float, PL0: float, Tx: float, R: float, C: float, Ta: float, T0: float = 25.0):
    """dT/dt for C dT/dt = Pd + PL0 exp((T - T0)/Tx) - (T - Ta)/R."""
    return lambda t, T: [(Pd + PL0 * math.exp((T[0] - T0) / Tx) - (T[0] - Ta) / R) / C]


def pendulum_rhs(g: float, L: float):
    return lambda t, y: [y[1], -(g / L) * math.sin(y[0])]


def step(A, B, u: float, t: float):
    A = np.asarray(A, dtype=float)
    return (expm(A * t) - np.eye(len(A))) @ np.linalg.solve(A, np.asarray(B, dtype=float) * u)
