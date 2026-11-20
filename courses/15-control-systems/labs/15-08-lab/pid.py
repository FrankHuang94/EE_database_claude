"""Lab 15-08 helpers: a PID controller with the features real loops need, and classic tuning rules.

    simulate(plant, Kp, Ki, Kd, ...)   closed-loop time response with actuator limits, anti-windup, a filtered
                                       derivative, setpoint weighting and an input disturbance (fixed-step RK4)
    zn_ultimate(Ku, Pu)                Ziegler-Nichols ultimate-gain PID rule  -> (Kp, Ti, Td)
    tyreus_luyben(Ku, Pu)              Tyreus-Luyben PID rule                  -> (Kp, Ti, Td)
    simc_pi(K, tau, theta, tau_c)      Skogestad's SIMC PI rule for a first-order-plus-delay plant -> (Kp, Ti)
    pid_tf(Kp, Ti, Td, N)              standard-form PID with derivative filter as (num, den)

The controller is u = Kp (b r - y) + Ki * integral(r - y) + D, where the derivative term D acts on (c r - y) through
the filter Kd s / (1 + s Td / N). Anti-windup modes: 'none', 'clamp' (stop integrating while saturated in the
direction that would deepen saturation) and 'back' (back-calculation with tracking time constant Tt).

A fixed-step integrator is used on purpose: saturation and clamping switch the dynamics abruptly, which slows
variable-step solvers. The verify script checks convergence by halving the step.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import signal


def simulate(plant, Kp, Ki=0.0, Kd=0.0, N=10.0, umin=-math.inf, umax=math.inf, aw="none", Tt=None,
             r=lambda t: 1.0, d=lambda t: 0.0, b=1.0, c=1.0, t_end=10.0, dt=1e-3, noise=None):
    """Return t, y, u (saturated) and u_raw arrays. plant = (num, den) of the plant transfer function.

    noise(t), if given, is added to the measured output that the controller sees (sensor noise).
    """
    A, B, C, D = signal.tf2ss(*plant)
    A, B, C = np.asarray(A), np.asarray(B).ravel(), np.asarray(C).ravel()
    Dp = float(np.asarray(D).ravel()[0]) if np.size(D) else 0.0
    n = A.shape[0]
    Td = Kd / Kp if (Kp and Kd) else 0.0
    Tf = Td / N if Td > 0 else None
    if Tt is None:
        Tt = Kp / Ki if Ki else 1.0

    def outputs(t, s):
        x, z, xf = s[:n], s[n], s[n + 1]
        y = float(C @ x)                       # strictly proper plants: Dp = 0
        ym = y + (noise(t) if noise else 0.0)  # what the sensor reports
        e = r(t) - ym
        v = c * r(t) - ym
        Dterm = Kd * (v - xf) / Tf if Tf else 0.0
        ur = Kp * (b * r(t) - ym) + Ki * z + Dterm
        u = min(umax, max(umin, ur))
        return x, y, e, v, ur, u

    def f(t, s):
        x, y, e, v, ur, u = outputs(t, s)
        xf = s[n + 1]
        dx = A @ x + B * (u + d(t))
        if aw == "none":
            dz = e
        elif aw == "clamp":
            dz = 0.0 if (ur != u and e * ur > 0) else e
        elif aw == "back":
            dz = e + (u - ur) / (Ki * Tt) if Ki else 0.0
        else:
            raise ValueError(aw)
        dxf = (v - xf) / Tf if Tf else 0.0
        return np.concatenate([dx, [dz, dxf]])

    steps = int(round(t_end / dt))
    t = np.linspace(0.0, steps * dt, steps + 1)
    s = np.zeros(n + 2)                        # plant, integrator and derivative filter all at rest before t = 0
    ys, us, urs = np.empty(steps + 1), np.empty(steps + 1), np.empty(steps + 1)
    for k in range(steps + 1):
        _, y, _, _, ur, u = outputs(t[k], s)
        ys[k], us[k], urs[k] = y, u, ur
        if k == steps:
            break
        h = dt
        k1 = f(t[k], s)
        k2 = f(t[k] + h / 2, s + h / 2 * k1)
        k3 = f(t[k] + h / 2, s + h / 2 * k2)
        k4 = f(t[k] + h, s + h * k3)
        s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return t, ys, us, urs


def zn_ultimate(Ku, Pu):
    """Ziegler-Nichols closed-loop (ultimate-gain) PID rule."""
    return 0.6 * Ku, Pu / 2, Pu / 8


def tyreus_luyben(Ku, Pu):
    """Tyreus-Luyben PID rule: a more conservative ultimate-gain rule."""
    return Ku / 2.2, 2.2 * Pu, Pu / 6.3


def simc_pi(K, tau, theta, tau_c=None):
    """SIMC PI rule for K e^{-theta s}/(tau s + 1): Kp = tau/(K(tau_c + theta)), Ti = min(tau, 4(tau_c + theta))."""
    tau_c = theta if tau_c is None else tau_c
    return tau / (K * (tau_c + theta)), min(tau, 4 * (tau_c + theta))


def pid_tf(Kp, Ti, Td=0.0, N=None):
    """Standard-form PID Kp (1 + 1/(Ti s) + Td s / (1 + Td s / N)) as (num, den); N=None for an ideal derivative."""
    if Td == 0:
        return Kp * np.array([Ti, 1.0]), np.array([Ti, 0.0])
    if N is None:
        return Kp * np.array([Td * Ti, Ti, 1.0]), np.array([Ti, 0.0])
    Tf = Td / N
    # Kp[(Ti s)(1 + Tf s) + (1 + Tf s) + Td Ti s^2] / [Ti s (1 + Tf s)]
    num = Kp * np.polyadd(np.polyadd(np.polymul([Ti, 0], [Tf, 1]), [Tf, 1]), [Td * Ti, 0, 0])
    den = np.polymul([Ti, 0], [Tf, 1])
    return num, den
