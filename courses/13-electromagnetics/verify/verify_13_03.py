#!/usr/bin/env python3
"""Verify every number in chapter 13-03 (magnetostatics and inductance), its solutions and lab.

Independent routes (not the chapter's closed forms):
- fields of wires and loops by numerical Biot-Savart integration;
- fields inside conductors by Ampere's law with the enclosed current integrated numerically from J;
- inductances per length from numerically integrated flux (the fields of equivalent filament pairs for
  wires over planes and two-wire lines) and from numerically integrated stored energy;
- the finite solenoid from a current-sheet double integral of coaxial-loop mutual inductances (elliptic
  integrals), checked against Nagaoka's closed form;
- straight-wire partial inductances by numerical Neumann double integrals;
- magnetic circuits by nodal solution of the reluctance network, and the gap force by numerical virtual work;
- parallel bond wires by inverting the inductance matrix.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad, quad
from scipy.optimize import brentq
from scipy.special import ellipe, ellipk, ellipkm1

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-03-magnetostatics-and-inductance.md",
         COURSE / "solutions" / "13-03-solutions.md"]
lab = COURSE / "labs" / "13-03-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-03", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 299792458.0
eta0 = math.sqrt(mu0 / e0)
U, N_, M_ = 1e6, 1e9, 1e3  # display scales: micro, nano, milli


# ---------------------------------------------------------------- helpers
def H_wire_biot_savart(I, rho):
    """|H| at distance rho from an infinite straight wire, by integrating dH = I dl x R / (4 pi R^3)."""
    val, _ = quad(lambda z: rho / (rho**2 + z**2) ** 1.5, -np.inf, np.inf)
    return I * val / (4 * math.pi)


def loop_axis_field(I, R, z, n=4000):
    """B_z on the axis of a circular loop by summing Biot-Savart over n discrete elements (vector form)."""
    phi = np.linspace(0, 2 * math.pi, n, endpoint=False)
    dphi = 2 * math.pi / n
    src = np.stack([R * np.cos(phi), R * np.sin(phi), np.zeros(n)], axis=1)
    dl = np.stack([-R * np.sin(phi), R * np.cos(phi), np.zeros(n)], axis=1) * dphi
    rvec = np.array([0.0, 0.0, z]) - src
    rmag = np.linalg.norm(rvec, axis=1)[:, None]
    dB = mu0 * I / (4 * math.pi) * np.cross(dl, rvec) / rmag**3
    return dB.sum(axis=0)[2]


def M_coaxial_loops(r, sep):
    """Mutual inductance of two coaxial circular filaments of radius r a distance sep apart (Maxwell)."""
    p = sep * sep / (4 * r * r + sep * sep)  # complementary parameter 1 - m, kept exact for tiny sep
    m = 1 - p
    k = math.sqrt(m)
    return mu0 * r * ((2 / k - k) * ellipkm1(p) - (2 / k) * ellipe(m))


def solenoid_sheet_L(N, r, ell):
    """Inductance of a uniform current sheet: (N/ell)^2 * integral over both positions of M(z - z')."""
    f = lambda u: (ell - u) * M_coaxial_loops(r, u)  # noqa: E731
    val, _ = quad(f, 0, ell, points=[1e-4 * ell, 1e-2 * ell], limit=400, epsabs=0, epsrel=1e-12)
    return (N / ell) ** 2 * 2 * val


def nagaoka_closed(r, ell):
    m = 4 * r * r / (4 * r * r + ell * ell)
    k, kp = math.sqrt(m), math.sqrt(1 - m)
    return 4 / (3 * math.pi * kp) * ((kp**2 / k**2) * (ellipk(m) - ellipe(m)) + ellipe(m) - k)


def neumann_parallel(ell, d):
    """Partial mutual inductance of two parallel coterminous filaments, by the Neumann double integral."""
    val, _ = dblquad(lambda z2, z1: 1 / math.sqrt((z1 - z2) ** 2 + d * d), 0, ell, 0, ell,
                     epsabs=1e-14, epsrel=1e-11)
    return mu0 / (4 * math.pi) * val


def flux_between_filaments(I, d, x1, x2):
    """Flux per metre through the strip x1..x2 on the line joining filaments +I at x = -d and -I at +d."""
    B = lambda x: mu0 * I / (2 * math.pi) * (1 / (x + d) + 1 / (d - x))  # noqa: E731
    val, _ = quad(B, x1, x2)
    return val


def potential_between_filaments(rho_l, d, x1, x2, eps):
    """Voltage between x1 and x2 on the line joining line charges +rho_l at -d and -rho_l at +d."""
    E = lambda x: rho_l / (2 * math.pi * eps) * (1 / (x + d) + 1 / (d - x))  # noqa: E731
    val, _ = quad(E, x1, x2)
    return val


def wire_over_plane(a, h, eps_r=1.0):
    """L' (flux of the wire and its image, wire surface to plane) and C' (line charge and image)."""
    d = math.sqrt(h * h - a * a)  # equivalent filament offset from the plane
    # put the plane at x = 0, the real filament at x = -d: integrate from the wire surface (x = -(h - a)) to 0
    Lp = flux_between_filaments(1.0, d, -(h - a), 0.0)
    Cp = 1.0 / potential_between_filaments(1.0, d, -(h - a), 0.0, eps_r * e0)
    return Lp, Cp


def two_wire(a, D):
    d = math.sqrt((D / 2) ** 2 - a * a)
    Lp = flux_between_filaments(1.0, d, -(D / 2 - a), D / 2 - a)
    return Lp


# ---------------------------------------------------------------- theory
# T a: refraction from iron (mu_r = 1000) into air with no surface current: solve the two boundary conditions
mur = 1000.0
th_in = math.radians(89.0)
Bn = math.cos(th_in)  # take |B| = 1 inside
Ht = math.sin(th_in) / (mur * mu0)
A = np.array([[1.0, 0.0], [0.0, 1.0 / mu0]])  # unknowns B_air_n, B_air_t: B_n equal, B_t/mu0 = Ht
B_air = np.linalg.solve(A, np.array([Bn, Ht]))
v.check("T 13-03.a", math.degrees(math.atan2(B_air[1], B_air[0])))
# T b: internal inductance by numerical energy integral, for two radii (radius independence)
Lints = []
for a_w in (0.5e-3, 3e-3):
    W, _ = quad(lambda r, a_w=a_w: 0.5 * mu0 * (r / (2 * math.pi * a_w**2)) ** 2 * 2 * math.pi * r, 0, a_w)
    Lints.append(2 * W)
v.check("T 13-03.b", Lints[0] * N_)
v.assert_true("internal inductance independent of radius", abs(Lints[1] / Lints[0] - 1) < 1e-10)
# T c, d: reluctance per metre of core vs gap; energy densities with equal B
Rg_per = 1e-3 / mu0
Rcore_per_m = 1.0 / (2000 * mu0)
v.check("T 13-03.c", Rg_per / Rcore_per_m)
Bx = 0.1
v.check("T 13-03.d", (Bx**2 / (2 * mu0) * 1e-3) / (Bx**2 / (2 * 2000 * mu0) * 0.1))

# ---------------------------------------------------------------- Example 1
H1 = H_wire_biot_savart(10.0, 0.01)
v.check("Ex 13-03.1a", H1)
v.check("Ex 13-03.1b", mu0 * H1 * U)
a, b, c = 0.5e-3, 1.75e-3, 2.0e-3
J_in = 1.0 / (math.pi * a * a)
J_out = -1.0 / (math.pi * (c * c - b * b))


def I_enc(rho):
    inner, _ = quad(lambda r: J_in * 2 * math.pi * r, 0, min(rho, a))
    outer = 0.0
    if rho > b:
        outer, _ = quad(lambda r: J_out * 2 * math.pi * r, b, min(rho, c))
    return inner + outer


def B_coax(rho):
    return mu0 * I_enc(rho) / (2 * math.pi * rho)


v.check("Ex 13-03.1c", B_coax(0.25e-3) * M_)
v.check("Ex 13-03.1d", B_coax(a) * M_)
v.check("Ex 13-03.1e", B_coax(1e-3) * M_)
v.check("Ex 13-03.1f", B_coax(3e-3) * M_, tol=1e-9)

# ---------------------------------------------------------------- Example 2
Lp_coax, _ = quad(B_coax, a, b)  # flux per metre per ampere
eps = 2.25 * e0
Vab, _ = quad(lambda r: 1.0 / (2 * math.pi * eps * r), a, b)  # 1 C/m on the inner conductor
Cp_coax = 1.0 / Vab
v.check("Ex 13-03.2a", Lp_coax * N_)
v.check("Ex 13-03.2b", Lp_coax * Cp_coax)
v.assert_true("coax L'C' = mu eps", abs(Lp_coax * Cp_coax / (mu0 * eps) - 1) < 1e-9)
v.check("Ex 13-03.2c", math.sqrt(Lp_coax / Cp_coax))
v.assert_true("coax velocity 2c/3", abs(1 / math.sqrt(Lp_coax * Cp_coax) / (c0 / 1.5) - 1) < 1e-6)

# ---------------------------------------------------------------- Example 3
Ns, rs, ls = 200, 5e-3, 0.05
B_inside = mu0 * Ns / ls  # Ampere around a rectangle, per ampere
Llong = Ns * B_inside * math.pi * rs**2
Lsheet = solenoid_sheet_L(Ns, rs, ls)
K3 = Lsheet / Llong
v.check("Ex 13-03.3a", Llong * U)
v.check("Ex 13-03.3b", K3)
v.assert_true("sheet integral matches Nagaoka closed form", abs(K3 - nagaoka_closed(rs, ls)) < 1e-6,
              f"{K3} vs {nagaoka_closed(rs, ls)}")
v.check("Ex 13-03.3c", Lsheet * U)
v.check("Ex 13-03.3d", (Llong / Lsheet - 1) * 100)
v.check("Ex 13-03.3e", 0.5 * Lsheet * U)


# ---------------------------------------------------------------- Example 4 (energy route)
def gapped_core(N, I, mur, lc, A, g):
    """Solve Ampere's law around the core with B continuous: (lc/(mur mu0) + g/mu0) B = N I; L = 2W/I^2."""
    Bc = np.linalg.solve(np.array([[lc / (mur * mu0) + g / mu0]]), np.array([N * I]))[0]
    W = Bc**2 / (2 * mur * mu0) * lc * A + Bc**2 / (2 * mu0) * g * A
    return Bc, 2 * W / I**2


Rc4 = 0.1 / (2000 * mu0 * 1e-4)
Rg4 = 1e-3 / (mu0 * 1e-4)
v.check("Ex 13-03.4a", Rc4)
v.check("Ex 13-03.4b", Rg4)
B4, L4 = gapped_core(100, 1.0, 2000, 0.1, 1e-4, 1e-3)
_, L4n = gapped_core(100, 1.0, 2000, 0.1, 1e-4, 0.0)
_, L4h = gapped_core(100, 1.0, 1000, 0.1, 1e-4, 1e-3)
v.check("Ex 13-03.4c", L4 * M_)
v.check("Ex 13-03.4d", L4n * M_)
v.check("Ex 13-03.4e", Rg4 / (Rc4 + Rg4) * 100)
v.check("Ex 13-03.4f", B4)
v.check("Ex 13-03.4g", L4n / L4)
v.check("Ex 13-03.4h", (1 - L4h / L4) * 100)
v.assert_true("energy route matches N^2/R", abs(L4 - 100**2 / (Rc4 + Rg4)) < 1e-12)

# ---------------------------------------------------------------- Example 5
aw = 12.5e-6


def bond_formula(ell):
    return mu0 * ell / (2 * math.pi) * (math.log(2 * ell / aw) - 1)


for ell, key in ((1e-3, "a"), (2e-3, "b"), (3e-3, "c")):
    Lf = bond_formula(ell)
    Ln = neumann_parallel(ell, aw)  # filament on the axis against a filament on the surface: GMD of a tube
    v.assert_true(f"bond {ell * 1e3:.0f} mm formula within 0.5% of Neumann integral", abs(Lf / Ln - 1) < 5e-3,
                  f"{Lf} vs {Ln}")
    v.check(f"Ex 13-03.5{key}", Lf * N_)
v.check("Ex 13-03.5d", bond_formula(2e-3) * N_ / 2)
v.check("Ex 13-03.5e", bond_formula(3e-3) * N_ / 3)
v.check("Ex 13-03.5f", 1e-9 * 20e-3 / 200e-12)

# ---------------------------------------------------------------- Example 6
Lwp, Cwp = wire_over_plane(0.5e-3, 5e-3)
v.check("Ex 13-03.6a", Lwp * N_)
v.check("Ex 13-03.6b", math.sqrt(Lwp / Cwp))
v.assert_true("13-02 capacitance reproduced", abs(Cwp * 1e12 - 18.59) < 0.005)
Ltw = two_wire(0.5e-3, 6e-3)
v.check("Ex 13-03.6c", Ltw * N_)
v.assert_true("two-wire closed form", abs(Ltw - mu0 / math.pi * math.acosh(6)) < 1e-15)

# ---------------------------------------------------------------- practitioner and simulation
v.check("Prac 13-03.a", 50.0 / (0.66 * c0) * N_)
v.check("Sim 13-03.a", 2e-9 * 40e-3 / 400e-12)

# ---------------------------------------------------------------- Problems
# 1: superpose the Biot-Savart fields of the two wires at the midpoint; force = I x B of the other
Bmid = mu0 * (H_wire_biot_savart(10, 0.005) + H_wire_biot_savart(10, 0.005))
v.check("13-03.1a", Bmid * U)
v.check("13-03.1b", 10 * mu0 * H_wire_biot_savart(10, 0.01) * M_)

# 2: boundary conditions as a linear system for B2 = (B2t, B2n)
B1 = np.array([0.3e-3, 1.2e-3])
Asys = np.array([[1 / (500 * mu0), 0.0], [0.0, 1.0]])
B2 = np.linalg.solve(Asys, np.array([B1[0] / mu0, B1[1]]))
v.check("13-03.2a", B1[0] / mu0)
v.check("13-03.2b", np.linalg.norm(B2) * M_)
v.check("13-03.2c", math.degrees(math.atan2(B1[0], B1[1])))
v.check("13-03.2d", math.degrees(math.atan2(B2[0], B2[1])))

# 3: toroid flux by numerical integration over the section
Nt, at, bt, ht = 500, 0.02, 0.03, 0.01
Phi_t, _ = quad(lambda r: mu0 * Nt * 1.0 / (2 * math.pi * r) * ht, at, bt)
Lt = Nt * Phi_t
v.check("13-03.3a", Lt * U)
v.check("13-03.3b", 2000 * Lt * M_)
v.check("13-03.3c", Nt / (2 * math.pi * at))
v.check("13-03.3d", Nt / (2 * math.pi * bt))
Lbar = mu0 * Nt**2 * (ht * (bt - at)) / (2 * math.pi * 0.025)
v.check("13-03.3e", Lbar * U)
v.check("13-03.3f", (1 - Lbar / Lt) * 100)

# 4: curl of A numerically, then flux as the difference of A_z
rho0 = 0.37  # arbitrary reference
Az = lambda r: mu0 / (2 * math.pi) * math.log(rho0 / r)  # noqa: E731
hstep = 1e-7
Bphi_num = -(Az(3e-3 + hstep) - Az(3e-3 - hstep)) / (2 * hstep)
v.assert_true("curl A gives the wire field", abs(Bphi_num / (mu0 / (2 * math.pi * 3e-3)) - 1) < 1e-6)
flux_A = Az(1e-3) - Az(1e-2)
flux_B, _ = quad(lambda r: mu0 / (2 * math.pi * r), 1e-3, 1e-2)
v.assert_true("Stokes: circulation of A equals flux of B", abs(flux_A / flux_B - 1) < 1e-10)
v.check("13-03.4a", flux_B * N_)

# 5: discrete Biot-Savart around the loop
R5 = 0.01
v.check("13-03.5a", loop_axis_field(1.0, R5, 0.0) * U)
v.check("13-03.5b", loop_axis_field(1.0, R5, R5) * U)
v.check("13-03.5c", 2 * loop_axis_field(1.0, R5, R5 / 2) * U)

# 6: long-formula and current-sheet inductances at 2 cm and 20 cm
for ell, k1, k2, k3 in ((0.02, "a", "c", "e"), (0.2, "b", "d", "f")):
    Ll = mu0 * Ns**2 * math.pi * rs**2 / ell
    Ls = solenoid_sheet_L(Ns, rs, ell)
    v.check(f"13-03.6{k1}", Ll * U)
    v.check(f"13-03.6{k2}", Ls * U)
    v.check(f"13-03.6{k3}", (Ll / Ls - 1) * 100)
v.assert_true("given Nagaoka factors", abs(nagaoka_closed(rs, 0.02) - 0.8181) < 5e-5
              and abs(nagaoka_closed(rs, 0.2) - 0.9791) < 5e-5)

# 7: design by root finding on the gap
L7, I7, Bm7, A7, lc7, mur7 = 100e-6, 5.0, 0.3, 1e-4, 0.05, 2000
N7 = next(n for n in range(1, 100) if n * Bm7 * A7 >= L7 * I7)
v.check("13-03.7a", N7)
g7 = brentq(lambda g: gapped_core(N7, 1.0, mur7, lc7, A7, g)[1] - L7, 1e-6, 1e-2, xtol=1e-15)
v.check("13-03.7b", g7 * 1e3)
B7, _ = gapped_core(N7, I7, mur7, lc7, A7, g7)
v.check("13-03.7c", B7)
W7 = 0.5 * L7 * I7**2
v.check("13-03.7d", W7 * 1e3)
Wgap7 = B7**2 / (2 * mu0) * g7 * A7
v.check("13-03.7e", Wgap7 / W7 * 100)

# 8: flux of the wire's field through the loop by a double integral
M8, _ = dblquad(lambda z, r: mu0 / (2 * math.pi * r), 0.005, 0.015, 0, 0.02)
v.check("13-03.8a", M8 * N_)
v.check("13-03.8b", M8 * 1.0 / 1e-9)

# 9: energy integrals inside both conductors
Win, _ = quad(lambda r: 0.5 * mu0 * (r / (2 * math.pi * a * a)) ** 2 * 2 * math.pi * r, 0, a)
Wout, _ = quad(lambda r: 0.5 * mu0 * (I_enc(r) / (2 * math.pi * r)) ** 2 * 2 * math.pi * r, b, c)
v.check("13-03.9a", 2 * Win * N_)
v.check("13-03.9b", 2 * Wout * N_)
v.check("13-03.9c", (Lp_coax + 2 * Win + 2 * Wout) * N_)
v.check("13-03.9d", (2 * Win + 2 * Wout) * N_)

# 10: wire over plane in a dielectric
L10, C10 = wire_over_plane(0.1e-3, 0.3e-3, 4.3)
v.check("13-03.10a", L10 * N_)
v.check("13-03.10b", C10 * 1e12)
v.check("13-03.10c", math.sqrt(L10 / C10))
v.check("13-03.10d", math.sqrt(L10 * C10) * 1e12 / 1e3)

# 11: parallel bonds from the inductance matrix: equal voltage across all, L_eff = 1/(1' L^-1 1)
for Mb, key in ((0.0, "a"), (0.3, "b")):
    Lmat = np.full((4, 4), Mb * 1e-9) + np.eye(4) * (1e-9 - Mb * 1e-9)
    Leff = 1.0 / (np.ones(4) @ np.linalg.solve(Lmat, np.ones(4)))
    v.check(f"13-03.11{key}", Leff * N_)
    v.check(f"13-03.11{'c' if Mb == 0 else 'd'}", Leff * 0.1 / 100e-12)

# 12: E-core by nodal analysis of the reluctance network
mu_c = 2000 * mu0
R1 = 0.04 / (mu_c * 2e-4)
Rg12 = 0.5e-3 / (mu0 * 2e-4)
R2 = 0.08 / (mu_c * 1e-4)
v.check("13-03.12a", R1)
v.check("13-03.12b", Rg12)
v.check("13-03.12c", R2)
# nodes: top yoke (magnetic potential u), bottom yoke at 0. Centre branch: MMF NI in series with R1 + Rg,
# driving flux up into the top node; the outer branches return it. KCL for flux at the top node:
NI = 50 * 1.0
G = np.array([[1 / (R1 + Rg12) + 2 / R2]])
u = np.linalg.solve(G, np.array([NI / (R1 + Rg12)]))[0]
Phi_c = (NI - u) / (R1 + Rg12)
Phi_o = u / R2
v.check("13-03.12d", NI / Phi_c)
v.check("13-03.12e", 50 * Phi_c / 1.0 * M_)
v.check("13-03.12f", Rg12 / (NI / Phi_c) * 100)
v.check("13-03.12g", Phi_c / 2e-4)
v.check("13-03.12h", Phi_o / 1e-4)
v.assert_true("flux conservation at the yoke", abs(Phi_c - 2 * Phi_o) < 1e-15)

# 13: square loop from Neumann integrals
s13, a13 = 0.01, 1e-4
Lp13 = neumann_parallel(s13, a13)
Mp13 = neumann_parallel(s13, s13)
v.check("13-03.13a", Lp13 * N_)
v.check("13-03.13b", Mp13 * N_)
v.check("13-03.13c", (4 * Lp13 - 4 * Mp13) * N_)
v.check("13-03.13d", 2 * mu0 * s13 / math.pi * (math.log(s13 / a13) - 0.774) * N_)

# 14: virtual work at fixed flux, numerically
Phi14 = 100 * 1.0 / (Rc4 + Rg4)


def W_fixed_flux(g):
    return 0.5 * Phi14**2 * (Rc4 + g / (mu0 * 1e-4))


dg = 1e-8
F14 = -(W_fixed_flux(1e-3 + dg) - W_fixed_flux(1e-3 - dg)) / (2 * dg)
v.check("13-03.14a", abs(F14))
v.check("13-03.14b", 0.3**2 * 1e-4 / (2 * mu0))

# ---------------------------------------------------------------- Lab
if lab.exists():
    v.check("Lab 13-03.a", loop_axis_field(1.0, 0.01, 0.02) * U)
    l5 = brentq(lambda ell: solenoid_sheet_L(200, 5e-3, ell) / (mu0 * 200**2 * math.pi * 25e-6 / ell) - 1 / 1.05,
                0.02, 0.5, xtol=1e-9)
    v.check("Lab 13-03.b", l5 * 100)
    v.check("Lab 13-03.c", bond_formula(5e-3) * N_ / 5)
    v.assert_true("5 mm bond formula within 0.5% of Neumann", abs(bond_formula(5e-3) / neumann_parallel(5e-3, aw) - 1)
                  < 5e-3)
    Bs, Bt = 0.4, 0.3

    def current_for_B(Btarget, g):
        # tanh B-H curve in the core: B = Bs tanh(mur mu0 H / Bs); solve for H_core with root finding
        Hc = brentq(lambda H: Bs * math.tanh(2000 * mu0 * H / Bs) - Btarget, 0, 1e5, xtol=1e-12)
        return (Hc * 0.1 + Btarget * g / mu0) / 100

    Ig, Iu = current_for_B(Bt, 1e-3), current_for_B(Bt, 0.0)
    v.check("Lab 13-03.d", Ig)
    v.check("Lab 13-03.e", Iu * M_)
    v.check("Lab 13-03.f", Ig / Iu)
    # pulse area: integrate v = L di/dt over the PWL ramp numerically
    t = np.linspace(0, 3e-9, 30001)
    i_t = np.interp(t, [0, 100e-12, 500e-12, 3e-9], [0, 0, 40e-3, 40e-3])
    v_t = 2e-9 * np.gradient(i_t, t)
    v.check("Lab 13-03.g", np.sum((v_t[1:] + v_t[:-1]) / 2 * np.diff(t)) * 1e12)

sys.exit(v.finish())
