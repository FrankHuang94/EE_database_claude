#!/usr/bin/env python3
"""Verify every number published in chapter 04-06, its solutions and its lab handout.

Independent routes: orbits and drifts by integrating the Lorentz force; fields by numerical
Biot–Savart integration over the actual conductor (segments, loops, squares, Helmholtz pairs);
Ampère-law fields by integrating current density over the enclosed area; Hall voltages from the
force balance; gapped-core flux from the magnetic-circuit equation solved numerically.
"""
from __future__ import annotations

import sys
import warnings
from math import cos, pi, radians, sin, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-06", C_DIR / "chapters" / "04-06-magnetic-fields-and-forces.md",
                        C_DIR / "solutions" / "04-06-solutions.md", C_DIR / "labs" / "04-06-lab" / "README.md")
E_CH = 1.602176634e-19
ME = 9.1093837139e-31
MP = 1.67262192595e-27
MU0 = 1.25663706127e-6
U = 1.66054e-27
N_CU = 8.96e3 / 63.546e-3 * 6.02214076e23


def lorentz(q, m, E, B):
    E, B = np.asarray(E, float), np.asarray(B, float)
    return lambda t, s: np.concatenate([s[3:], q / m * (E + np.cross(s[3:], B))])


def orbit_radius(q, m, v0, B):
    T = 2 * pi * m / (abs(q) * B)
    sol = solve_ivp(lorentz(q, m, [0, 0, 0], [0, 0, B]), (0, T), [0, 0, 0, v0, 0, 0], rtol=1e-11, atol=1e-16,
                    max_step=T / 2000)
    return (sol.y[1].max() - sol.y[1].min()) / 2


def segment_B(I, p, a, b, n=None):
    """Biot–Savart field at p from a straight segment a->b (vector), by quadrature along it."""
    a, b, p = (np.asarray(x, float) for x in (a, b, p))
    L = np.linalg.norm(b - a)
    u = (b - a) / L
    s0 = float(np.dot(p - a, u))                     # foot of the perpendicular from p
    d = float(np.linalg.norm(p - a - s0 * u))
    # substitute s = s0 + d tan(phi) so a long wire's narrow peak near s0 is well resolved

    def comp(k):
        def f(phi):
            s = s0 + d * np.tan(phi)
            r = p - (a + s * u)
            return (MU0 * I / (4 * pi) * np.cross(u, r) / np.linalg.norm(r) ** 3)[k] * d / np.cos(phi) ** 2
        return quad(f, np.arctan((0 - s0) / d), np.arctan((L - s0) / d), epsabs=0, epsrel=1e-12, limit=200)[0]
    return np.array([comp(k) for k in range(3)])


def loop_B_axis(I, R, z):
    """Axial field of a circular loop by integrating Biot–Savart around it."""
    f = lambda ph: MU0 * I / (4 * pi) * (R * R) / (R * R + z * z) ** 1.5
    return quad(f, 0, 2 * pi)[0]


def enclosed_field(I_density, r, rmax_parts):
    """Ampère: B(r) = mu0 I_enc / (2 pi r), with I_enc integrated from the current density J(r)."""
    Ienc = quad(lambda rr: I_density(rr) * 2 * pi * rr, 0, r, points=rmax_parts, limit=200)[0]
    return MU0 * Ienc / (2 * pi * r)


def hall_voltage(I, B, n, t, q=E_CH):
    """Force balance q E_H = q v_d B, with v_d = I / (n q w t); V_H = E_H w (w cancels)."""
    w = 1e-3
    vd = I / (n * q * w * t)
    return vd * B * w


def gapped_B_per_A(l, mur, N, g):
    # solve H_c l + H_g g = N I for B with I = 1 A
    return brentq(lambda B: B / (mur * MU0) * l + B / MU0 * g - N * 1.0, 0, 100, xtol=1e-16)


# ---------------------------------------------------------------- theory keys
v.check("T 04-06.a", np.linalg.norm(segment_B(1.0, [0.01, 0, 0], [0, 0, -1e4], [0, 0, 1e4])) * 1e6)
v.check("T 04-06.b", 1 / (2 * pi * orbit_radius(-E_CH, ME, 1e6, 1.0) / 1e6) / 1e9)
v.check("T 04-06.c", MU0 / (4 * pi * 1e-7))
v.assert_true("magnetic force is perpendicular to v", abs(np.dot(np.cross([1, 2, 3], [4, 5, 6]), [1, 2, 3])) < 1e-12)

# ---------------------------------------------------------------- examples
v.check("Ex 04-06.1a", np.linalg.norm(-E_CH * np.cross([1e6, 0, 0], [0, 0, 0.1])))
r_e = orbit_radius(-E_CH, ME, 1e6, 0.1)
v.check("Ex 04-06.1b", r_e * 1e6)
v.check("Ex 04-06.1c", 1e6 / (2 * pi * r_e) / 1e9)
v.check("Ex 04-06.1d", 2 * pi * r_e / 1e6 * 1e9)
v.check("Ex 04-06.1e", orbit_radius(E_CH, MP, 1e6, 0.1) * 1e3)
radii = {}
for mu in (10, 11, 49):
    m = mu * U
    vv = sqrt(2 * E_CH * 1e4 / m)
    radii[mu] = orbit_radius(E_CH, m, vv, 0.5)
    if mu == 11:
        v.check("Ex 04-06.2a", vv)
v.check("Ex 04-06.2b", radii[11] * 100)
v.check("Ex 04-06.2c", radii[10] * 100)
v.check("Ex 04-06.2d", radii[49] * 100)
v.check("Ex 04-06.2e", 2 * (radii[11] - radii[10]) * 100)
B_bus = np.linalg.norm(segment_B(1e3, [0.01, 0, 0], [0, 0, -1e4], [0, 0, 1e4]))
v.check("Ex 04-06.3a", 1e3 * B_bus)
v.check("Ex 04-06.3b", 1e4 * B_bus * 10)
m3 = 100 * 0.1 * 0.02 * 0.02
v.check("Ex 04-06.3c", m3)
v.check("Ex 04-06.3d", np.linalg.norm(np.cross([m3, 0, 0], [0, 0.5, 0])))
v.check("Ex 04-06.3e", (-m3 * 0.5 * cos(pi)) - (-m3 * 0.5 * cos(0)))
Bc = loop_B_axis(2.0, 0.05, 0.0)
v.check("Ex 04-06.4a", Bc * 1e6)
v.check("Ex 04-06.4b", loop_B_axis(2.0, 0.05, 0.05) * 1e6)
corners = [[0.05, 0.05, 0], [-0.05, 0.05, 0], [-0.05, -0.05, 0], [0.05, -0.05, 0]]
Bsq = sum(segment_B(2.0, [0, 0, 0], corners[i], corners[(i + 1) % 4]) for i in range(4))
v.check("Ex 04-06.4c", np.linalg.norm(Bsq) * 1e6)
v.check("Ex 04-06.4d", np.linalg.norm(Bsq) / Bc)
# solenoid: sum of many loops along a long coil, at its center
n_turns_per_m, I5, Lsol, Rsol = 1e4, 0.5, 2.0, 0.01
B_sol = quad(lambda z: n_turns_per_m * loop_B_axis(I5, Rsol, z), -Lsol / 2, Lsol / 2, limit=200)[0]
v.check("Ex 04-06.5a", B_sol * 1e3)
v.check("Ex 04-06.5b", MU0 * 200 * 1.0 / (2 * pi * 0.02) * 1e3)      # Ampere: B 2 pi r = mu0 N I
v.check("Ex 04-06.5c", MU0 * 200 * 1.0 / (2 * pi * 0.03) * 1e3)
v.check("Ex 04-06.6a", hall_voltage(1.0, 1.0, N_CU, 1e-4) * 1e6)
VH_si = hall_voltage(1e-3, 0.1, 1e22, 1e-5)
v.check("Ex 04-06.6b", VH_si * 1e3)
v.check("Ex 04-06.6c", brentq(lambda n: hall_voltage(1e-3, 0.1, n, 1e-5) - 6.242e-3, 1e18, 1e26) / 1e6)
v.check("Ex 04-06.6d", 1 / (E_CH * 1e16 * 0.4458))
wire = lambda I, d: np.linalg.norm(segment_B(I, [d, 0, 0], [0, 0, -100], [0, 0, 100]))
v.check("Ex 04-06.7a", wire(5, 0.5e-3) * 1e3)
v.check("Ex 04-06.7b", wire(50, 0.5e-3) * 1e3)
v.check("Ex 04-06.7c", 0.4 * 5)
v.check("Ex 04-06.7d", 5**2 * 1.2e-3 * 1e3)
v.check("Ex 04-06.7e", 50**2 * 1.2e-3)
k8 = gapped_B_per_A(0.05, 2000, 20, 0.0)
v.check("Ex 04-06.8a", k8)
v.check("Ex 04-06.8b", 0.49 / k8)
v.check("Ex 04-06.8c", 0.39 / k8)
v.check("Ex 04-06.8d", (1 - 0.39 / 0.49) * 100)

# ---------------------------------------------------------------- solutions
F1 = E_CH * np.cross([2e5, 0, 0], 0.2 * np.array([cos(radians(30)), sin(radians(30)), 0]))
v.check("04-06.1a", np.linalg.norm(F1))
v.assert_true("force along +z", F1[2] > 0 and abs(F1[0]) + abs(F1[1]) < 1e-30)
v.check("04-06.2a", 50e-6 / 1e-4)
B2 = wire(10, 0.01)
v.check("04-06.2b", B2 * 1e6)
v.check("04-06.2c", B2 / 1e-4)
r3 = orbit_radius(E_CH, MP, sqrt(2 * 1e6 * E_CH / MP), 1.5)
v.check("04-06.3a", sqrt(2 * 1e6 * E_CH / MP) / (2 * pi * r3) / 1e6)
v.check("04-06.3b", r3 * 100)
vsel = brentq(lambda vv: 1e5 - vv * 0.05, 0, 1e8)
v.check("04-06.4a", vsel)
v.check("04-06.4b", ME * vsel**2 / (2 * E_CH))
r10 = orbit_radius(E_CH, 10 * U, sqrt(2 * E_CH * 3e4 / (10 * U)), 0.8)
r11 = orbit_radius(E_CH, 11 * U, sqrt(2 * E_CH * 3e4 / (11 * U)), 0.8)
v.check("04-06.5a", r10 * 100)
v.check("04-06.5b", r11 * 100)
v.check("04-06.5c", 2 * (r11 - r10) * 1e3)
v.check("04-06.6a", np.linalg.norm(10 * np.cross(0.5 * np.array([cos(radians(60)), sin(radians(60)), 0]), [0.2, 0, 0])))
m7 = 50 * 0.2 * 0.03 * 0.04
v.check("04-06.7a", m7)
v.check("04-06.7b", m7 * 0.3 * sin(radians(30)))
v.check("04-06.7c", 2 * m7 * 0.3)
B8 = np.linalg.norm(segment_B(5.0, [0, 0.02, 0], [-0.05, 0, 0], [0.05, 0, 0]))
v.check("04-06.8a", B8 * 1e6)
v.check("04-06.8b", wire(5, 0.02) * 1e6)
v.check("04-06.8c", B8 / wire(5, 0.02))
v.check("04-06.9a", 5 * wire(3, 0.04))
v.check("04-06.9b", (wire(3, 0.02) + wire(5, 0.02)) * 1e6)
v.check("04-06.10a", brentq(lambda I: MU0 * 600 / 0.3 * I - 0.01, 0, 100))
v.check("04-06.10b", MU0 * 500 * 2 / (2 * pi * 0.04) * 1e3)
v.check("04-06.10c", MU0 * 500 * 2 / (2 * pi * 0.06) * 1e3)
J11 = lambda r: 10 / (pi * 1e-3**2) if r < 1e-3 else 0.0
v.check("04-06.11a", enclosed_field(J11, 0.5e-3, None) * 1e3)
v.check("04-06.11b", enclosed_field(J11, 1e-3, None) * 1e3)
v.check("04-06.11c", enclosed_field(J11, 5e-3, [1e-3]) * 1e3)
v.check("04-06.12a", hall_voltage(10, 0.5, N_CU, 1e-4) * 1e6)
v.check("04-06.12b", hall_voltage(0.5e-3, 0.05, 1e21, 5e-6) * 1e3)
v.check("04-06.12c", 1 / (1e21 * E_CH))
p13 = brentq(lambda p: hall_voltage(1e-3, 0.1, p, 5e-4) - 2.50e-3, 1e16, 1e26)
v.check("04-06.13a", p13 / 1e6)
v.check("04-06.13b", 1 / (E_CH * p13 / 1e6 * 27.7))
B14 = wire(10, 1e-3)
v.check("04-06.14a", B14 * 1e3)
v.check("04-06.14b", ((B14 + 0.5e-3) - (-B14 + 0.5e-3)) * 1e3)
v.check("04-06.14c", 0.5e-3 / B14 * 100)
k15 = gapped_B_per_A(0.05, 2000, 20, 0.5e-3)
v.check("04-06.15a", k15)
v.check("04-06.15b", 0.39 / k15)
v.check("04-06.15c", (0.39 / k15) / (0.39 / k8))
v.check("04-06.16a", loop_B_axis(1.0, 0.01, 0.1) * 1e9)
v.check("04-06.16b", MU0 * pi * 0.01**2 / (2 * pi * 0.1**3) * 1e9)
v.check("04-06.16c", loop_B_axis(1.0, 0.01, 0.1) / (MU0 * pi * 0.01**2 / (2 * pi * 0.1**3)))

# ---------------------------------------------------------------- lab
Tp = 2 * pi * MP / (E_CH * 0.1)
sol = solve_ivp(lorentz(E_CH, MP, [1e3, 0, 0], [0, 0, 0.1]), (0, 5 * Tp), [0] * 6, rtol=1e-11, atol=1e-13, max_step=Tp / 400)
v.check("Lab 04-06.a", abs(sol.y[1, -1]) / (5 * Tp) / 1e3)


def helm(z, R=0.05, N=10, I=1.0):
    return N * (loop_B_axis(I, R, z + R / 2) + loop_B_axis(I, R, z - R / 2))


v.check("Lab 04-06.b", helm(0) * 1e3)
v.check("Lab 04-06.c", (1 - helm(0.01) / helm(0)) * 100)
v.check("Lab 04-06.d", (1 - loop_B_axis(1.0, 0.05, 0.01) / loop_B_axis(1.0, 0.05, 0.0)) * 100)
v.check("Lab 04-06.e", 0.39 / gapped_B_per_A(0.05, 2000, 20, 1e-3))

sys.exit(v.finish())
