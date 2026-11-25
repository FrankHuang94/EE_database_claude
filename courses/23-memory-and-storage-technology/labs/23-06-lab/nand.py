"""Models for chapter 23-06: NAND flash and 3D NAND.

Closed forms for the chapter's examples: the floating-gate (or charge-trap) cell's threshold shift and coupling,
Fowler-Nordheim tunneling and incremental-step programming, multi-level margins and raw bit error rate, 3D density
and channel-hole aspect ratio, Arrhenius retention acceleration, endurance budgets and die throughput. The verify
script recomputes the published numbers by other routes. SI units unless a name says otherwise.
"""
from __future__ import annotations

import math

from scipy import stats

Q_E = 1.602176634e-19
EPS0 = 8.8541878128e-12
K_B_EV = 8.617333262e-5  # Boltzmann constant (eV/K)


# ---------------------------------------------------------------- the cell
def vt_shift_per_electron(c_cg: float) -> float:
    """Threshold shift seen at the control gate per stored electron (V)."""
    return Q_E / c_cg


def coupling_ratio(c_cg: float, c_other: float) -> float:
    return c_cg / (c_cg + c_other)


def plate_cap(eps_r: float, area: float, t: float) -> float:
    return eps_r * EPS0 * area / t


def fn_current_density(e_field: float, a_fn: float = 1.25e-6, b_fn: float = 2.33e10) -> float:
    """Fowler-Nordheim current density (A/m^2) at oxide field e_field (V/m); representative SiO2 constants."""
    if e_field <= 0:
        return 0.0
    return a_fn * e_field ** 2 * math.exp(-b_fn / e_field)


def ispp_pulses(v_start: float, v_target: float, step: float) -> int:
    """Program pulses for incremental-step programming, which raises V_T by one step per pulse in steady state."""
    return math.ceil((v_target - v_start) / step - 1e-12)


# ---------------------------------------------------------------- multi-level cells
def level_gap(window: float, bits: int) -> float:
    """Spacing between adjacent threshold-level centres when 2^bits levels share a window."""
    return window / (2 ** bits - 1)


def rber(window: float, bits: int, sigma: float) -> float:
    """Raw bit error rate with Gaussian levels, Gray coding and equiprobable data.

    A level is misread into a neighbour with probability Q(gap / 2 sigma) per side; interior levels have two
    neighbours, the outer two have one, so the average is 2 (L - 1)/L Q(gap/2 sigma); each such error costs 1 of
    `bits` bits.
    """
    levels = 2 ** bits
    q = float(stats.norm.sf(level_gap(window, bits) / (2 * sigma)))
    return 2 * (levels - 1) / levels * q / bits


# ---------------------------------------------------------------- 3D structure
def density_per_layer_bit(density_gb_mm2: float, layers: int, bits: int) -> float:
    return density_gb_mm2 / (layers * bits)


def aspect_ratio(layers: int, layer_pitch: float, hole_diameter: float, decks: int = 1) -> float:
    """Height-to-diameter ratio of the channel hole each deck must etch."""
    return layers * layer_pitch / decks / hole_diameter


# ---------------------------------------------------------------- reliability
def arrhenius_af(ea_ev: float, t_use_c: float, t_stress_c: float) -> float:
    """Acceleration factor of a stress at t_stress over use at t_use for activation energy ea (eV)."""
    t1, t2 = t_use_c + 273.15, t_stress_c + 273.15
    return math.exp(ea_ev / K_B_EV * (1 / t1 - 1 / t2))


def tbw(capacity_tb: float, pe_cycles: float, waf: float) -> float:
    """Terabytes the host can write over the drive's life."""
    return capacity_tb * pe_cycles / waf


def dwpd(tbw_tb: float, capacity_tb: float, years: float) -> float:
    return tbw_tb / (capacity_tb * 365 * years)


# ---------------------------------------------------------------- throughput
def die_throughput(page_bytes: float, planes: int, t_op: float) -> float:
    """Bytes per second one die sustains when all planes operate in parallel."""
    return page_bytes * planes / t_op


# ---------------------------------------------------------------- ISPP transient (the netlist's cell, in Python)
def ispp_shifts(c_cg: float = 16e-18, c_tox: float = 12.332618739e-18, tox: float = 7e-9, area: float = 2.5e-15,
                v0: float = 15.0, step: float = 0.25, pulses: int = 30, t_pulse: float = 10e-6) -> list[float]:
    """Threshold shift -Q/C_CG after each pulse of an ISPP train, holding each pulse flat for t_pulse.

    Integrates dQ/dt = -I_FN(V_FG) with V_FG = (C_CG V_CG + Q)/(C_CG + C_TOX); charge in attocoulombs.
    """
    from scipy import integrate

    ct = c_cg + c_tox
    q = 0.0
    out = []
    for k in range(pulses):
        vcg = v0 + step * k

        def rhs(t, y, vcg=vcg):
            e = (c_cg * vcg + y[0] * 1e-18) / ct / tox
            return [-fn_current_density(e) * area * 1e18]

        sol = integrate.solve_ivp(rhs, (0.0, t_pulse), [q * 1e18], method="Radau", rtol=1e-8, atol=1e-8)
        q = sol.y[0, -1] * 1e-18
        out.append(-q / c_cg)
    return out
