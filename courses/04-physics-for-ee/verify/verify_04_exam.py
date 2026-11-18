#!/usr/bin/env python3
"""Verify every number in the Course 04 final-exam solutions.

Each value is recomputed independently rather than copied: fields by summing Coulomb vectors and by
integrating the charge distribution, potentials by integrating fields, charge sharing by solving the
circuit ODE, delays from a discretized RC line, orbits by integrating the Lorentz force, inductance
and energies from the field, the fiber angles by root-finding on Snell's law, quantum-well levels by
root-finding on sin kL = 0, the Fermi energy by solving the integrated density of states, and the
HBM pulse by integrating its ODE.
"""
from __future__ import annotations

import sys
from math import asin, degrees, exp, log, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("04-exam", HERE.parent / "exam" / "solutions.md")
H, E_CH, C, KB = 6.62607015e-34, 1.602176634e-19, 299792458.0, 1.380649e-23
ME, EPS0, MU0 = 9.1093837139e-31, 8.8541878188e-12, 1.25663706127e-6
KE, U, G, R = 8.98755e9, 1.66054e-27, 9.80665, 8.314462618
HBAR = H / (2 * pi)
HC_EV_NM = H * C / E_CH * 1e9
KT300 = KB * 300 / E_CH


def coulomb_field(charges, point):
    f = np.zeros(3)
    for q, pos in charges:
        r = np.asarray(point, float) - np.asarray(pos, float)
        f += KE * q * r / np.linalg.norm(r) ** 3
    return f


# ---------------------------------------------------------------- 1
m1, k1 = 1.0e-9, 2.0
w0 = brentq(lambda w: k1 - m1 * w**2, 1, 1e7)          # resonance where the spring and inertia balance
v.check("X04.1a", w0 / (2 * pi))
v.check("X04.1b", m1 * G / k1 * 1e9)
v.check("X04.1c", 1 / (2 * 0.7))

# ---------------------------------------------------------------- 2
qs = [(2e-9, (0, 0, 0)), (-2e-9, (0.04, 0, 0))]
e_mid = coulomb_field(qs, (0.02, 0, 0))
v.assert_true("midpoint field points along +x", e_mid[0] > 0 and abs(e_mid[1]) < 1e-9)
v.check("X04.2a", e_mid[0])
v.check("X04.2b", E_CH * np.linalg.norm(e_mid))
v.check("X04.2c", 2e-9 * 0.04)
# far-field limit: the exact on-axis field times r³ approaches 2 k_e p; evaluate at 1 km and scale to 1 m
far = coulomb_field([(2e-9, (-0.02, 0, 0)), (-2e-9, (0.02, 0, 0))], (-1000.0, 0, 0))
v.check("X04.2d", np.linalg.norm(far) * 1000.0**3)
near = coulomb_field([(2e-9, (-0.02, 0, 0)), (-2e-9, (0.02, 0, 0))], (-1.0, 0, 0))
v.assert_true("exact field at 1 m within 0.1% of the dipole formula", abs(np.linalg.norm(near) / (np.linalg.norm(far) * 1e9) - 1) < 1e-3)

# ---------------------------------------------------------------- 3
Q3, R3 = 1e-8, 0.01
rho3 = Q3 / (4 / 3 * pi * R3**3)
enc = lambda r: quad(lambda s: rho3 * 4 * pi * s**2, 0, min(r, R3))[0]
v.check("X04.3a", KE * enc(0.005) / 0.005**2)
v.check("X04.3b", KE * enc(0.02) / 0.02**2)
eps_si = 11.7 * EPS0
field_p = lambda x: E_CH * 1e23 * x / eps_si           # field grows linearly from the depletion edge
v.check("X04.3c", field_p(50e-9))
v.check("X04.3d", quad(field_p, 0, 50e-9)[0])

# ---------------------------------------------------------------- 4
c_ox, c_hk = 3.9 * EPS0 / 0.6e-9, 25 * EPS0 / 1.5e-9
c_stack = 1 / (1 / c_ox + 1 / c_hk)
v.check("X04.4a", 3.9 * EPS0 / c_stack * 1e9)
v.check("X04.4b", c_stack * 1e2)                     # F/m² → µF/cm²
cs, cb, rsw = 10e-15, 60e-15, 1e3
sol = solve_ivp(lambda t, y: [-(y[0] - y[1]) / (rsw * cs), (y[0] - y[1]) / (rsw * cb)], (0, 2e-10), [1.0, 0.5],
                rtol=1e-11, atol=1e-14, dense_output=True)
vf = sol.y[1, -1]
v.check("X04.4c", vf)
v.check("X04.4d", (vf - 0.5) * 1e3)
p_sw = lambda t: (sol.sol(t)[0] - sol.sol(t)[1]) ** 2 / rsw
v.check("X04.4e", quad(p_sw, 0, 2e-10, limit=200)[0] * 1e15)

# ---------------------------------------------------------------- 5
rw = 5.0e-8 * 1e-4 / (20e-9 * 40e-9)
cw = 0.20e-15 * 100
v.check("X04.5a", rw)
v.check("X04.5b", cw * 1e15)


def ladder_t50(r_tot, c_tot, n=200):
    """50% delay of an n-section RC ladder (driven by an ideal step, open far end)."""
    r, c = r_tot / n, c_tot / n
    a = np.zeros((n, n))
    for i in range(n):
        a[i, i] = -2 / (r * c) if i < n - 1 else -1 / (r * c)
        if i > 0:
            a[i, i - 1] = 1 / (r * c)
        if i < n - 1:
            a[i, i + 1] = 1 / (r * c)
    b = np.zeros(n)
    b[0] = 1 / (r * c)
    out = solve_ivp(lambda t, y: a @ y + b, (0, 3 * r_tot * c_tot), np.zeros(n), method="BDF", rtol=1e-8,
                    atol=1e-11, dense_output=True)
    return brentq(lambda t: out.sol(t)[-1] - 0.5, 1e-6 * r_tot * c_tot, 3 * r_tot * c_tot, xtol=1e-9 * r_tot * c_tot)


t_full = ladder_t50(rw, cw)
v.assert_true("ladder 50% delay is 0.38 RC to 1%", abs(t_full / (rw * cw) / 0.38 - 1) < 0.01)
v.check("X04.5c", 0.38 * rw * cw * 1e12)
v.assert_true("half-length ladder delay is a quarter", abs(ladder_t50(rw / 2, cw / 2) / t_full - 0.25) < 1e-3)
v.check("X04.5d", 0.38 * (rw / 2) * (cw / 2) * 1e12)
v.check("X04.5e", 20e-6 / (20e-9 * 40e-9) / 1e10)


# ---------------------------------------------------------------- 6
def orbit_radius(mass_u, volts, b):
    m = mass_u * U
    speed = sqrt(2 * E_CH * volts / m)
    # integrate the Lorentz force for a half turn and take half the maximum excursion
    rhs = lambda t, y: [y[2], y[3], E_CH * y[3] * b / m, -E_CH * y[2] * b / m]
    period = 2 * pi * m / (E_CH * b)
    s = solve_ivp(rhs, (0, period / 2), [0, 0, speed, 0], rtol=1e-11, atol=1e-14, max_step=period / 2000)
    return np.max(np.abs(s.y[1])) / 2


r11, r49, r10 = orbit_radius(11, 4e4, 0.8), orbit_radius(49, 4e4, 0.8), orbit_radius(10, 4e4, 0.8)
v.check("X04.6a", r11 * 100)
v.check("X04.6b", r49 * 100)
v.check("X04.6c", (r11 - r10) * 1e3)

# ---------------------------------------------------------------- 7
b_wire = quad(lambda s: MU0 * 10 / (4 * pi) * 0.01 / (s**2 + 0.01**2) ** 1.5, -np.inf, np.inf)[0]   # Biot-Savart
v.check("X04.7a", b_wire)
sens = 1e-3 / (1e22 * E_CH * 1e-6)
v.check("X04.7b", sens)
v.check("X04.7c", sens * b_wire * 1e3)
v.check("X04.7d", sens * 0.05 * 1e3)

# ---------------------------------------------------------------- 8
n_turns, area, length = 200, 1e-4, 0.02
b_per_amp = MU0 * n_turns / length
l_sol = n_turns * b_per_amp * area                 # flux linkage per ampere
v.check("X04.8a", l_sol * 1e6)
w_field = (b_per_amp * 0.5) ** 2 / (2 * MU0) * area * length
v.check("X04.8b", w_field * 1e6)
v.check("X04.8c", l_sol * 0.5 / 10e-6)
v.check("X04.8d", sqrt(2 * 1.68e-8 / (2 * pi * 2e5 * MU0)) * 1e6)

# ---------------------------------------------------------------- 9
v_board = 1 / sqrt(MU0 * 4.0 * EPS0)
v.check("X04.9a", v_board)
v.check("X04.9b", 0.1 / v_board * 1e9)
eta0 = sqrt(MU0 / EPS0)
v.check("X04.9c", eta0)
v.check("X04.9d", sqrt(MU0 / (4.0 * EPS0)))
v.check("X04.9e", v_board / 10e9 * 100)
t_grid = np.linspace(0, 1, 100001)
v.check("X04.9f", np.mean((10 * np.cos(2 * pi * t_grid)) ** 2) / eta0)

# ---------------------------------------------------------------- 10
n1, n2 = 1.4500, 1.4447
crit = brentq(lambda th: n1 * np.sin(th) - n2, 0, pi / 2)
theta_core = pi / 2 - crit                          # largest ray angle to the axis inside the core
na = n1 * np.sin(theta_core)
v.check("X04.10a", na)
v.check("X04.10b", degrees(asin(na)))
v.check("X04.10c", degrees(crit))
v.check("X04.10d", 0.32 * 13.5 / 0.33)
v.check("X04.10e", 0.32 * 13.5 / 0.55)

# ---------------------------------------------------------------- 11
e_ph = HC_EV_NM / 1550
v.check("X04.11a", e_ph)
v.check("X04.11b", 0.80 * E_CH / (e_ph * E_CH))


def well_level(n, width, m):
    k = brentq(lambda kk: np.sin(kk * width), (n - 0.5) * pi / width, (n + 0.5) * pi / width)
    return HBAR**2 * k**2 / (2 * m) / E_CH


e1, e2 = well_level(1, 8e-9, 0.067 * ME), well_level(2, 8e-9, 0.067 * ME)
v.check("X04.11c", e1 * 1e3)
v.check("X04.11d", (e2 - e1) * 1e3)
v.check("X04.11e", HC_EV_NM / (e2 - e1) / 1e3)
kappa = sqrt(2 * ME * 2.1 * E_CH) / HBAR
v.check("X04.11f", exp(-2 * kappa * 1.5e-9) / exp(-2 * kappa * 2.0e-9))

# ---------------------------------------------------------------- 12
n_ag = 5.86e28
count = lambda e_j: (1 / (3 * pi**2)) * (2 * ME * e_j / HBAR**2) ** 1.5
ef = brentq(lambda e_j: count(e_j) - n_ag, 1e-20, 1e-17, xtol=1e-35, rtol=1e-14)
v.check("X04.12a", ef / E_CH)
v.check("X04.12b", sqrt(2 * ef / ME))
v.check("X04.12c", pi**2 / 3 * KB * 300 / ef)
ni = lambda t: 5.29e19 * (t / 300) ** 2.54 * exp(-6726 / t)
v.check("X04.12d", ni(398.15))
v.check("X04.12e", ni(398.15) / ni(300))
v.check("X04.12f", brentq(lambda t: 3.26 / t - 1.12 / 398.15, 300, 3000))

# ---------------------------------------------------------------- 13
l13, k13, f13, i13 = 24e-6, 0.4, 128e3, 2.0
m13 = k13 * sqrt(l13 * l13)
w13 = 2 * pi * f13
v.check("X04.13a", m13 * 1e6)
z = np.array([[1j * w13 * l13, 1j * w13 * m13], [1j * w13 * m13, 1j * w13 * l13 + 1e9]])   # receiver loaded by 1 GΩ
# drive the primary with a current: v1 = Z11 i1 + Z12 i2, 0 = Z21 i1 + Z22 i2
i2 = -z[1, 0] * i13 / z[1, 1]
v.check("X04.13b", abs(i2 * 1e9))
v.check("X04.13c", abs(z[0, 0] * i13 + z[0, 1] * i2))
v.check("X04.13d", brentq(lambda c: w13 * l13 - 1 / (w13 * c), 1e-12, 1e-5, xtol=1e-20) * 1e9)
v.check("X04.13e", 0.5 * l13 * i13**2 * 1e6)
v.check("X04.13f", w13 * 0.2 * l13 * i13)

# ---------------------------------------------------------------- 14
c14, v14, r14 = 100e-12, 2000.0, 1500.0
hbm = solve_ivp(lambda t, y: [-y[0] / (r14 * c14)], (0, 2e-6), [v14], rtol=1e-11, atol=1e-9, dense_output=True)
cur = lambda t: hbm.sol(t)[0] / r14
v.check("X04.14a", cur(0))
v.check("X04.14b", r14 * c14 * 1e9)
v.check("X04.14c", quad(lambda t: cur(t) ** 2 * r14, 0, 2e-6, limit=200)[0] * 1e6)
v.check("X04.14d", quad(cur, 0, 2e-6, limit=200)[0] * 1e9)
v.check("X04.14e", brentq(lambda t: cur(t) - 0.1 * cur(0), 1e-9, 1e-6, xtol=1e-15) * 1e9)

sys.exit(v.finish())
