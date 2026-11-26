"""Thermal models for lab 25-08.

Slab resistances, hotspot spreading on a half-space, spreading through a disk-shaped spreader by an
axisymmetric finite-difference solve and by the 45-degree estimate, fin efficiency (closed form and a
numerical ODE solve), coolant flow and temperature rise, a cold-plate junction budget, and the
Arrhenius-equivalent temperature of a mission profile. SI units unless stated.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import integrate, sparse
from scipy.sparse import linalg as spla

K_B_EV = 8.617333262e-5  # Boltzmann constant, eV/K


def slab_r(t_m: float, k: float, area_m2: float) -> float:
    return t_m / (k * area_m2)


def hotspot_center_rise(q_w: float, a_m: float, k: float) -> float:
    """Centre temperature rise of a uniform-flux disk on a half-space: q a / k."""
    return q_w / (math.pi * a_m**2) * a_m / k


def hotspot_r_avg(a_m: float, k: float) -> float:
    """Average-temperature spreading resistance of a uniform-flux disk on a half-space."""
    return 8 / (3 * math.pi**2 * k * a_m)


def r45_disk(a_m: float, t_m: float, k: float, b_m: float | None = None) -> float:
    """Spreading at 45 degrees from a disk of radius a through thickness t (capped at radius b)."""
    if b_m is None or a_m + t_m <= b_m:
        return t_m / (k * math.pi * a_m * (a_m + t_m))
    z1 = b_m - a_m
    return z1 / (k * math.pi * a_m * b_m) + (t_m - z1) / (k * math.pi * b_m**2)


def spreader_fd(a_m: float, b_m: float, t_m: float, k: float, nr: int = 160, nz: int = 48) -> float:
    """Average source temperature / power for a uniform-flux disk (radius a) on top of a cylinder
    (radius b, thickness t, conductivity k) with an isothermal bottom at 0 and adiabatic sides,
    by a cell-centred axisymmetric finite-volume solve."""
    dr, dz = b_m / nr, t_m / nz
    rc = (np.arange(nr) + 0.5) * dr
    n = nr * nz
    rows, cols, vals = [], [], []
    rhs = np.zeros(n)
    q = 1.0 / (math.pi * a_m**2)  # 1 W in total

    def idx(i, j):
        return j * nr + i

    for j in range(nz):
        for i in range(nr):
            p = idx(i, j)
            vol = rc[i] * dr * dz
            diag = 0.0
            if i > 0:  # inner radial face
                g = k * (rc[i] - dr / 2) * dz / dr
                rows.append(p); cols.append(idx(i - 1, j)); vals.append(-g); diag += g
            if i < nr - 1:  # outer radial face
                g = k * (rc[i] + dr / 2) * dz / dr
                rows.append(p); cols.append(idx(i + 1, j)); vals.append(-g); diag += g
            if j > 0:  # face toward the top
                g = k * rc[i] * dr / dz
                rows.append(p); cols.append(idx(i, j - 1)); vals.append(-g); diag += g
            if j < nz - 1:
                g = k * rc[i] * dr / dz
                rows.append(p); cols.append(idx(i, j + 1)); vals.append(-g); diag += g
            else:  # bottom face held at 0 through a half cell
                diag += k * rc[i] * dr / (dz / 2)
            if j == 0:  # top face: flux in over the source
                r_in, r_out = rc[i] - dr / 2, rc[i] + dr / 2
                overlap = max(0.0, min(r_out, a_m) ** 2 - r_in**2) / 2
                rhs[p] += q * overlap
            rows.append(p); cols.append(p); vals.append(diag)
            del vol
    a = sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))
    temp = spla.spsolve(a, rhs).reshape(nz, nr)
    # top-surface temperature by extrapolating half a cell up with the known flux
    top = temp[0] + np.where(rc < a_m, q * dz / 2 / k, 0.0)
    w = np.clip(np.minimum(rc + dr / 2, a_m) ** 2 - (rc - dr / 2) ** 2, 0, None)
    return float(np.sum(top * w) / np.sum(w))


def fin_efficiency(h: float, k: float, t_m: float, length_m: float) -> float:
    m = math.sqrt(2 * h / (k * t_m))
    return math.tanh(m * length_m) / (m * length_m)


def fin_efficiency_ode(h: float, k: float, t_m: float, length_m: float) -> float:
    """Solve theta'' = m^2 theta, theta(0) = 1, theta'(L) = 0 and integrate the convected heat."""
    m2 = 2 * h / (k * t_m)
    x = np.linspace(0, length_m, 201)
    sol = integrate.solve_bvp(lambda s, y: np.vstack([y[1], m2 * y[0]]),
                              lambda ya, yb: np.array([ya[0] - 1, yb[1]]), x, np.vstack([np.ones_like(x), np.zeros_like(x)]))
    xs = np.linspace(0, length_m, 2001)
    return float(integrate.trapezoid(sol.sol(xs)[0], xs) / length_m)


def heatsink_r(n_fins: int, height_m: float, depth_m: float, h: float, eta: float) -> float:
    area = n_fins * 2 * height_m * depth_m
    return 1 / (h * eta * area)


def flow_for(power_w: float, dt_k: float, rho: float, cp: float) -> float:
    """Volumetric flow (m^3/s) that carries power_w with a temperature rise dt_k."""
    return power_w / (rho * cp * dt_k)


def junction(power_w: float, t_in: float, flow_m3s: float, r_total: float, rho: float = 1000.0,
             cp: float = 4180.0) -> float:
    rise = power_w / (rho * cp * flow_m3s)
    return t_in + rise / 2 + power_w * r_total


def arrhenius_equivalent(temps_c: list[float], weights: list[float], ea_ev: float) -> float:
    tk = np.array(temps_c) + 273.15
    rate = np.sum(np.array(weights) * np.exp(-ea_ev / (K_B_EV * tk)))
    return float(-ea_ev / (K_B_EV * math.log(rate)) - 273.15)
