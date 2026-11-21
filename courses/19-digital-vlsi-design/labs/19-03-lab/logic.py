"""Logic-family models for Lab 19-03.

Static CMOS sizing and input capacitance in unit-width terms; the Elmore delay of RC ladders and of series
transistor stacks; the exact step response of an RC ladder by the matrix exponential; pseudo-NMOS output level and
static power; an NMOS pass transistor's high level with body effect; transmission-gate chains with buffers; and
charge sharing and leakage in dynamic gates. Units: volts, amperes, farads, ohms, seconds; k in A/V^2.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

LN2 = math.log(2)


# ---------------------------------------------------------------- static CMOS sizing (unit inverter: Wn = 1, Wp = mu)
def nand_sizes(n: int, mu: float = 2.0) -> tuple[float, float]:
    """Widths (Wn, Wp) of an n-input NAND whose worst-case pull-down and pull-up match a unit inverter."""
    return float(n), mu


def nor_sizes(n: int, mu: float = 2.0) -> tuple[float, float]:
    """Widths (Wn, Wp) of an n-input NOR matched to a unit inverter: series PMOS n times wider."""
    return 1.0, mu * n


def input_cap_ratio(wn: float, wp: float, mu: float = 2.0) -> float:
    """Input capacitance of one input relative to the unit inverter's, (Wn + Wp)/(1 + mu)."""
    return (wn + wp) / (1 + mu)


# ---------------------------------------------------------------- Elmore delay and RC ladders
def elmore_ladder(r: list[float], c: list[float]) -> float:
    """Elmore time constant at the far end of a ladder: resistor r[i] feeds node i, which has capacitance c[i].
    tau = sum_i c[i] * (r[0] + ... + r[i])."""
    return float(sum(ci * sum(r[: i + 1]) for i, ci in enumerate(c)))


def ladder_step_50(r: list[float], c: list[float]) -> float:
    """Exact 50% delay at the far end of an RC ladder driven by a unit step at its input (all nodes start at 0),
    from the matrix exponential of the nodal equations C dv/dt = -G v + b."""
    n = len(c)
    g = np.zeros((n, n))
    b = np.zeros(n)
    for i in range(n):
        gi = 1 / r[i]
        g[i, i] += gi
        if i == 0:
            b[0] += gi
        else:
            g[i - 1, i - 1] += gi
            g[i - 1, i] -= gi
            g[i, i - 1] -= gi
    a = -np.diag(1 / np.array(c)) @ g
    bb = np.diag(1 / np.array(c)) @ b
    vinf = np.linalg.solve(g, b)

    def v_end(t):
        return float((vinf - expm(a * t) @ vinf)[-1]) if t > 0 else 0.0

    tau = elmore_ladder(r, c)
    _ = bb
    return brentq(lambda t: v_end(t) - 0.5, 1e-6 * tau, 10 * tau, xtol=1e-6 * tau * 1e-6)


def nand_stack_elmore(n: int, r_unit: float, c_unit: float, c_ext: float, mu: float = 2.0) -> float:
    """Elmore time constant of an n-input NAND's pull-down (n series NMOS of width n, resistance r_unit/n each),
    with c_unit of diffusion per unit width at each internal node (width n) and at the output (NMOS drain of width
    n plus n PMOS drains of width mu), plus c_ext. All internal nodes start charged (worst case)."""
    r = [r_unit / n] * n
    c = [c_unit * n] * (n - 1) + [c_unit * n + c_unit * mu * n + c_ext]
    return elmore_ladder(r, c)


# ---------------------------------------------------------------- ratioed (pseudo-NMOS) logic
def pseudo_nmos_vol(kn: float, kp: float, vdd: float, vtn: float, vtp: float) -> float:
    """Low output level of a pseudo-NMOS gate: saturated PMOS load (gate grounded) against a linear NMOS (gate at
    VDD): kp/2 (VDD - |VTP|)^2 = kn ((VDD - VTN) V - V^2/2), smaller root."""
    a = vdd - vtn
    i_load = 0.5 * kp * (vdd - vtp) ** 2
    return a - math.sqrt(a * a - 2 * i_load / kn)


def pseudo_nmos_static_current(kp: float, vdd: float, vtp: float) -> float:
    return 0.5 * kp * (vdd - vtp) ** 2


def pseudo_nmos_ratio_for_vol(vol: float, vdd: float, vtn: float, vtp: float) -> float:
    """kn/kp needed for a given V_OL."""
    return 0.5 * (vdd - vtp) ** 2 / ((vdd - vtn) * vol - vol * vol / 2)


# ---------------------------------------------------------------- pass transistors
def vt_body(vt0: float, gamma: float, phi2: float, vsb: float) -> float:
    """Threshold with body effect: VT0 + gamma (sqrt(2phiF + VSB) - sqrt(2phiF))."""
    return vt0 + gamma * (math.sqrt(phi2 + vsb) - math.sqrt(phi2))


def nmos_pass_high(vdd: float, vt0: float, gamma: float, phi2: float) -> float:
    """Final level an NMOS pass transistor (gate at VDD) passes for a logic 1: V = VDD - VT(V)."""
    return brentq(lambda v: vdd - vt_body(vt0, gamma, phi2, v) - v, 0.0, vdd)


def inverter_static_current(vin: float, vdd: float, vtn: float, vtp: float, kn: float, kp: float) -> tuple[float, float]:
    """Output voltage and supply current of a square-law inverter at a static input (lambda = 0)."""
    def i_n(vo):
        vov = vin - vtn
        if vov <= 0:
            return 0.0
        return kn * (vov * vo - vo * vo / 2) if vo < vov else 0.5 * kn * vov * vov

    def i_p(vo):
        vov = vdd - vin - vtp
        vsd = vdd - vo
        if vov <= 0:
            return 0.0
        return kp * (vov * vsd - vsd * vsd / 2) if vsd < vov else 0.5 * kp * vov * vov

    vo = brentq(lambda x: i_p(x) - i_n(x), 0.0, vdd, xtol=1e-15)
    return vo, i_n(vo)


# ---------------------------------------------------------------- transmission-gate chains
def tg_chain_delay(n: int, r: float, c: float) -> float:
    """0.69 x Elmore delay of n identical TG sections (r, c): 0.69 r c n(n + 1)/2."""
    return LN2 * r * c * n * (n + 1) / 2


def tg_chain_buffered(n: int, m: int, r: float, c: float, t_buf: float) -> float:
    """n sections split into n/m segments of m, with a buffer of delay t_buf between segments."""
    seg = n // m
    return seg * tg_chain_delay(m, r, c) + (seg - 1) * t_buf


def tg_optimal_m(r: float, c: float, t_buf: float) -> float:
    """Continuous optimum of the segment length: sqrt(2 t_buf / (0.69 r c))."""
    return math.sqrt(2 * t_buf / (LN2 * r * c))


# ---------------------------------------------------------------- dynamic logic
def charge_sharing(vdd: float, vt: float, cl: float, ca: float) -> float:
    """Output after charge sharing between a precharged output cl and an internal node ca that starts at 0 V, through
    an NMOS with its gate at VDD (no body effect). If the shared level would exceed VDD - VT, the NMOS cuts off with
    the internal node at VDD - VT."""
    v_eq = vdd * cl / (cl + ca)
    if v_eq >= vdd - vt:
        return vdd - ca / cl * (vdd - vt)
    return v_eq


def hold_time(c: float, dv: float, i_leak: float) -> float:
    """Time for a leakage current to droop a dynamic node by dv: C dV / I."""
    return c * dv / i_leak
