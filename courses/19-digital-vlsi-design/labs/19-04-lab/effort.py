"""Logical-effort models for Lab 19-04.

Delays are in units of tau = 0.69 R C_inv, the delay of an ideal unit inverter driving its own input capacitance with
no self-loading; with self-loading ratio gamma = 1 the inverter's parasitic delay is p_inv = 1 and tau equals the
intrinsic delay t_p0 of 19-02. A stage's delay is d = g h + p. Also: path effort and optimal sizing, the best stage
effort and number of stages, and a square-law transistor simulation of inverter chains.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


# ---------------------------------------------------------------- gate parameters (unit inverter Wn = 1, Wp = mu)
def logical_effort(kind: str, n: int = 1, mu: float = 2.0) -> float:
    """Logical effort g: input capacitance per input relative to an inverter of the same drive."""
    if kind == "inv":
        return 1.0
    if kind == "nand":
        return (n + mu) / (1 + mu)
    if kind == "nor":
        return (1 + n * mu) / (1 + mu)
    raise ValueError(kind)


def parasitic_delay(kind: str, n: int = 1, p_inv: float = 1.0) -> float:
    """Parasitic delay p in units of tau: an n-input NAND or NOR sized for unit drive has n times the inverter's
    output diffusion capacitance (to first order, ignoring internal nodes)."""
    return p_inv if kind == "inv" else n * p_inv


def stage_delay(g: float, h: float, p: float) -> float:
    return g * h + p


# ---------------------------------------------------------------- paths
def path_effort(gs: list[float], bs: list[float], h_path: float) -> float:
    """F = G B H."""
    return math.prod(gs) * math.prod(bs) * h_path


def min_path_delay(gs: list[float], ps: list[float], bs: list[float], h_path: float) -> float:
    """D = N F^(1/N) + P, with every stage bearing the same effort."""
    n = len(gs)
    return n * path_effort(gs, bs, h_path) ** (1 / n) + sum(ps)


def stage_input_caps(gs: list[float], bs: list[float], c_in: float, c_out: float) -> list[float]:
    """Input capacitance of each stage for equal stage efforts, working backward from the load:
    C_in,i = g_i C_out,i / f, with C_out,i = b_i C_in,i+1 (and C_out of the last stage = c_out)."""
    n = len(gs)
    f = path_effort(gs, bs, c_out / c_in) ** (1 / n)
    caps = [0.0] * n
    load = c_out
    for i in reversed(range(n)):
        caps[i] = gs[i] * load / f
        load = bs[i - 1] * caps[i] if i > 0 else load
    return caps


def best_stage_effort(p_inv: float = 1.0) -> float:
    """rho solving rho (ln rho - 1) = p_inv (the stage effort that minimizes the delay of a long inverter chain)."""
    if p_inv == 0:
        return math.e
    return brentq(lambda r: r * (math.log(r) - 1) - p_inv, math.e, 100.0, xtol=1e-14)


def chain_delay(f_path: float, n: int, p_inv: float = 1.0) -> float:
    """Delay of an n-inverter chain with path effort F: n F^(1/n) + n p_inv."""
    return n * f_path ** (1 / n) + n * p_inv


def best_stage_count(f_path: float, p_inv: float = 1.0) -> tuple[float, int]:
    """Continuous optimum log_rho F and the best integer number of stages."""
    rho = best_stage_effort(p_inv)
    n_cont = math.log(f_path) / math.log(rho)
    cands = [max(1, math.floor(n_cont)), math.ceil(n_cont)]
    return n_cont, min(cands, key=lambda n: chain_delay(f_path, n, p_inv))


# ---------------------------------------------------------------- transistor-level check: inverter chains
def i_sq(k: float, vov: float, vds: float) -> float:
    if vov <= 0 or vds <= 0:
        return 0.0
    return k * (vov * vds - vds * vds / 2) if vds < vov else 0.5 * k * vov * vov


def simulate_chain(sizes: list[float], c_load: float, k_unit: float = 200e-6, vdd: float = 1.2, vt: float = 0.35,
                   c_gate: float = 2e-15, c_par: float = 2e-15, t_rise: float = 10e-12) -> float:
    """50%-to-50% delay of a chain of symmetric square-law inverters (stage i has kn = kp = k_unit * sizes[i]) driving
    c_load; node i carries the stage's own c_par * size plus the next stage's c_gate * size. The input is a ramp from
    0 to vdd of duration t_rise. Returns the delay from the input's 50% point to the last output's 50% crossing."""
    n = len(sizes)
    caps = [c_par * sizes[i] + (c_gate * sizes[i + 1] if i + 1 < n else c_load) for i in range(n)]

    def vin(t):
        return min(max(t / t_rise, 0.0), 1.0) * vdd

    def rhs(t, v):
        dv = np.empty(n)
        for i in range(n):
            x = vin(t) if i == 0 else v[i - 1]
            k = k_unit * sizes[i]
            dv[i] = (i_sq(k, vdd - x - vt, vdd - v[i]) - i_sq(k, x - vt, v[i])) / caps[i]
        return dv
    v0 = np.array([vdd if i % 2 == 0 else 0.0 for i in range(n)])
    final_high = n % 2 == 0
    ev = lambda _t, v: v[-1] - vdd / 2  # noqa: E731
    ev.terminal = True
    ev.direction = 1 if final_high else -1
    tau = c_load / (k_unit * (vdd - vt))
    sol = solve_ivp(rhs, (0, 200 * tau + 1e-9), v0, events=ev, method="LSODA", rtol=1e-10, atol=1e-14,
                    max_step=t_rise / 4)
    return float(sol.t_events[0][0]) - t_rise / 2
