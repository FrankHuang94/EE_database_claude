"""CMOS inverter delay models for Lab 19-02.

Square-law transistors (lambda = 0) driving a lumped load capacitance: the exact step-input delay, the equivalent-
resistance model, intrinsic delay and fan-out, a ring oscillator simulated as coupled ODEs, and alpha-power supply
scaling. Units: volts, amperes, farads, seconds; k in A/V^2.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad, solve_ivp


def i_nmos(k: float, vov: float, vds: float) -> float:
    """Square-law NMOS current (lambda = 0) for overdrive vov and drain-source voltage vds."""
    if vov <= 0 or vds <= 0:
        return 0.0
    if vds < vov:
        return k * (vov * vds - 0.5 * vds * vds)
    return 0.5 * k * vov * vov


def tp_step_exact(c: float, k: float, vdd: float, vt: float) -> float:
    """50% delay of a step-driven inverter discharging c through a square-law transistor (valid for vt < vdd/2):
    t = C/(k Vov) [2 Vt/Vov + ln(4 Vov/VDD - 1)], Vov = VDD - Vt."""
    vov = vdd - vt
    return c / (k * vov) * (2 * vt / vov + math.log(4 * vov / vdd - 1))


def tp_step_ode(c: float, k: float, vdd: float, vt: float) -> float:
    """The same delay by integrating C dV/dt = -I(V) numerically to V = VDD/2."""
    vov = vdd - vt

    def f(_t, y):
        return [-i_nmos(k, vov, y[0]) / c]

    def half(_t, y):
        return y[0] - vdd / 2
    half.terminal = True
    tmax = 50 * c * vdd / (0.5 * k * vov * vov)
    sol = solve_ivp(f, (0, tmax), [vdd], events=half, rtol=1e-11, atol=1e-16, max_step=tmax / 2e4)
    return float(sol.t_events[0][0])


def r_eq(k: float, vdd: float, vt: float) -> float:
    """Equivalent resistance: the average of V/I(V) as the output falls from VDD to VDD/2."""
    vov = vdd - vt
    return quad(lambda v: v / i_nmos(k, vov, v), vdd / 2, vdd, points=[vov] if vov < vdd else None)[0] / (vdd / 2)


def r_eq_approx(k: float, vdd: float, vt: float) -> float:
    """The usual approximation 3 VDD / (4 I_sat), from averaging the resistance at the two end points."""
    return 3 * vdd / (4 * 0.5 * k * (vdd - vt) ** 2)


def tp_rc(r: float, c: float) -> float:
    """Delay of an RC step response to its 50% point: ln 2 R C."""
    return math.log(2) * r * c


def tp_with_fanout(tp0: float, c_ext: float, c_int: float, size: float = 1.0) -> float:
    """t_p = t_p0 (1 + C_ext / (S C_int)): intrinsic delay plus the load's share, for an inverter scaled by S."""
    return tp0 * (1 + c_ext / (size * c_int))


def ring_frequency(n_stages: int, tp: float) -> float:
    return 1.0 / (2 * n_stages * tp)


def simulate_ring(n_stages: int, kn: float, kp: float, vdd: float, vtn: float, vtp: float, c: float,
                  periods: float = 6.0) -> float:
    """Period of a ring oscillator of square-law inverters, each loading its node with c, from coupled ODEs.
    Returns the average period measured from rising crossings of VDD/2 at node 0 after the start-up transient."""
    def deriv(_t, v):
        dv = np.empty(n_stages)
        for i in range(n_stages):
            vin = v[i - 1]
            ip = i_nmos(kp, vdd - vin - vtp, vdd - v[i])
            inn = i_nmos(kn, vin - vtn, v[i])
            dv[i] = (ip - inn) / c
        return dv
    tp_guess = tp_step_exact(c, min(kn, kp), vdd, max(vtn, vtp))
    t_end = periods * 2 * n_stages * tp_guess * 3
    v0 = np.array([vdd if i % 2 else 0.0 for i in range(n_stages)])
    v0[0] = vdd / 2 + 0.01
    sol = solve_ivp(deriv, (0, t_end), v0, rtol=1e-9, atol=1e-12, max_step=tp_guess / 20, dense_output=True)
    t = np.linspace(0, t_end, 200001)
    x = sol.sol(t)[0] - vdd / 2
    ups = t[1:][(x[:-1] < 0) & (x[1:] >= 0)]
    ups = ups[len(ups) // 3:]
    return float(np.mean(np.diff(ups)))


def delay_vs_supply(vdd: float, vt: float, alpha: float) -> float:
    """Relative delay of the alpha-power model, proportional to VDD / (VDD - Vt)^alpha."""
    return vdd / (vdd - vt) ** alpha


def edp_optimal_vdd(vt: float, alpha: float) -> float:
    """Supply that minimizes the energy-delay product C VDD^2 x VDD/(VDD - Vt)^alpha: VDD = 3 Vt / (3 - alpha)."""
    return 3 * vt / (3 - alpha)
