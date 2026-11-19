#!/usr/bin/env python3
"""Verify every number in chapter 09-01 (crystals, energy bands and the semiconductor), its solutions and lab.

Independent routes:
- lattice quantities come from generating the diamond (and zinc-blende) lattice from its FCC lattice and
  two-atom basis and counting atoms: per cell, per neighbor shell, and per plane inside an in-plane
  parallelogram that tiles the plane;
- plane spacings are point-to-plane distances for the plane through the three intercept points, and angles
  between planes use normals built by cross products of in-plane vectors (not the Miller-index shortcut);
- Kronig-Penney bands come from the 2 x 2 transfer matrix of one period, multiplied numerically, with band
  edges found in energy by a root finder; derivatives are taken numerically; effective masses are fitted
  to the computed E(k) near the band bottom;
- conductivity and density-of-states masses come from per-valley inverse-mass tensors, and effective
  densities of states by integrating g(E) exp(-E/kT) numerically;
- alloy compositions are solved with a root finder; temperature derivatives are finite differences.
"""
from __future__ import annotations

import math
import sys
from itertools import product
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-01", COURSE / "chapters" / "09-01-crystals-and-energy-bands.md",
                        COURSE / "solutions" / "09-01-solutions.md",
                        COURSE / "labs" / "09-01-lab" / "README.md")

HBAR, M0, Q, NA, KB = C.hbar, C.m_e, C.e, C.N_A, C.k
HC = C.h * C.c / Q * 1e9            # nm eV
EV = Q

# ---------------------------------------------------------------- lattice tools (units of a)
FCC = np.array([(0, 0, 0), (0, .5, .5), (.5, 0, .5), (.5, .5, 0)])
BASIS = np.array([(0, 0, 0), (.25, .25, .25)])


def lattice(n, basis=BASIS):
    cells = np.array(list(product(range(-n, n), repeat=3)))
    pts = cells[:, None, None, :] + FCC[None, :, None, :] + basis[None, None, :, :]
    return pts.reshape(-1, 3), pts.shape[2]


def atoms_per_cell():
    pts, _ = lattice(2)
    inside = np.all((pts >= -1e-9) & (pts < 1 - 1e-9), axis=1)
    return int(inside.sum())


def shells(nshell=2):
    pts, _ = lattice(3)
    d = np.linalg.norm(pts, axis=1)
    radii = np.unique(np.round(d[d > 1e-9], 9))[:nshell]
    return [(r, int(np.sum(np.isclose(d, r)))) for r in radii]


def planar_count(normal, u, v_, which=None):
    """Atoms in the plane n.r = 0 inside the half-open parallelogram spanned by u, v (units of a)."""
    pts, nb = lattice(5)
    if which is not None:                  # one sublattice only (zinc blende)
        pts = pts.reshape(-1, nb, 3)[:, which, :]
    normal, u, v_ = map(np.asarray, (normal, u, v_))
    on = pts[np.isclose(pts @ normal, 0.0)]
    coeffs = np.linalg.lstsq(np.stack([u, v_], axis=1), on.T, rcond=None)[0].T
    inside = np.all((coeffs > -1e-9) & (coeffs < 1 - 1e-9), axis=1)
    return int(inside.sum()), float(np.linalg.norm(np.cross(u, v_)))


def plane_normal(intercepts):
    p = [np.array([x if i == k else 0.0 for k in range(3)]) for i, x in enumerate(intercepts) if np.isfinite(x)]
    fin = [i for i, x in enumerate(intercepts) if np.isfinite(x)]
    inf = [i for i, x in enumerate(intercepts) if not np.isfinite(x)]
    vecs = [p[j] - p[0] for j in range(1, len(p))] + [np.eye(3)[i] for i in inf]
    n = np.cross(vecs[0], vecs[1])
    return n, p[0], fin


def spacing(intercepts):
    n, p0, _ = plane_normal(intercepts)
    return abs(n @ p0) / np.linalg.norm(n)


def angle(n1, n2):
    n1, n2 = np.asarray(n1, float), np.asarray(n2, float)
    return math.degrees(math.acos(abs(n1 @ n2) / np.linalg.norm(n1) / np.linalg.norm(n2)))


def angle_signed(n1, n2):
    n1, n2 = np.asarray(n1, float), np.asarray(n2, float)
    return math.degrees(math.acos(n1 @ n2 / np.linalg.norm(n1) / np.linalg.norm(n2)))


# ---------------------------------------------------------------- Kronig-Penney by transfer matrix
def half_trace(E_eV, P, d, m=M0):
    alpha = math.sqrt(2 * m * E_eV * EV) / HBAR
    c, s = math.cos(alpha * d), math.sin(alpha * d)
    free = np.array([[c, s / alpha], [-alpha * s, c]])
    kick = np.array([[1.0, 0.0], [2 * P / d, 1.0]])
    return 0.5 * np.trace(kick @ free)


def e_scale(d, m=M0):
    return HBAR**2 / (2 * m * d**2) / EV


def kp_edges(P, d):
    """Band-1 bottom, band-1 top, band-2 bottom, band-2 top (eV), found in energy from the transfer matrix."""
    Ed = e_scale(d)
    grid = np.linspace(1e-6, 4.2 * math.pi**2 * Ed, 40001)
    f = np.array([half_trace(e, P, d) for e in grid])
    edges = []
    for target in (1.0, -1.0):
        g = f - target
        for i in np.nonzero(np.sign(g[:-1]) != np.sign(g[1:]))[0]:
            edges.append(brentq(lambda e: half_trace(e, P, d) - target, grid[i], grid[i + 1], xtol=1e-14))
    edges.sort()
    return edges[:4]


def kp_mass(P, d, Eb):
    dE = np.linspace(1e-7, 2e-5, 40) * e_scale(d)
    ks = np.array([math.acos(min(1.0, half_trace(Eb + x, P, d))) / d for x in dE])
    slope = np.polyfit(ks**2, dE * EV, 1)[0]
    return HBAR**2 / (2 * slope) / M0


def F_of_x(x, P, d):
    """Half-trace as a function of x = alpha d (energy expressed through x)."""
    return half_trace(e_scale(d) * x**2, P, d)


def dF_dx(x, P, d, h=1e-6):
    return (F_of_x(x + h, P, d) - F_of_x(x - h, P, d)) / (2 * h)


# ---------------------------------------------------------------- masses and densities of states
def valley_tensors(ml, mt, axes):
    out = []
    for ax in axes:
        ax = np.asarray(ax, float) / np.linalg.norm(ax)
        proj = np.outer(ax, ax)
        inv = proj / ml + (np.eye(3) - proj) / mt          # inverse-mass tensor of one valley
        out.append(inv)
    return out


def conductivity_mass(tensors, direction=(1, 0, 0)):
    u = np.asarray(direction, float)
    return 1 / np.mean([u @ t @ u for t in tensors])


def dos_mass(tensors):
    return sum(math.sqrt(1 / np.linalg.det(t)) for t in tensors) ** (2 / 3)


def N_eff(m_rel, T=300.0):
    kT = KB * T
    g = lambda E: (1 / (2 * math.pi**2)) * (2 * m_rel * M0 / HBAR**2) ** 1.5 * math.sqrt(E)
    return quad(lambda x: g(x * kT) * math.exp(-x) * kT, 0, 80, limit=200)[0] / 1e6


def varshni(T, E0, a, b):
    return E0 - a * T**2 / (T + b)


def dvarshni(T, E0, a, b, h=1e-3):
    return (varshni(T + h, E0, a, b) - varshni(T - h, E0, a, b)) / (2 * h)


A_SI, A_GE, A_GAAS, A_ALAS, A_INAS, A_INP = 5.431, 5.658, 5.65325, 5.6611, 6.0583, 5.8697   # Å
SI_VALLEYS = valley_tensors(0.98, 0.19, [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
GE_VALLEYS = valley_tensors(1.6, 0.08, [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)])
SI = (1.17, 4.73e-4, 636.0)
GAAS = (1.519, 5.405e-4, 204.0)
INAS = (0.417, 2.76e-4, 93.0)
B_GAINAS = 0.477

# ================================================================= chapter
n_cell = atoms_per_cell()
v.assert_true(n_cell == 8, "diamond cell holds 8 atoms")
(r1, c1), (r2, c2) = shells(2)
v.assert_true(c1 == 4 and c2 == 12, "4 nearest and 12 second-nearest neighbors")
a_cm = A_SI * 1e-8
N_si = n_cell / a_cm**3
v.check("Ex 09-01.1a", N_si)
v.check("Ex 09-01.1b", r1 * A_SI)
v.check("Ex 09-01.1c", N_si * 28.0855 / NA)
for key, (normal, u, w) in {"Ex 09-01.1d": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                            "Ex 09-01.1e": ((1, 1, 0), (1, -1, 0), (0, 0, 1)),
                            "Ex 09-01.1f": ((1, 1, 1), (1, -1, 0), (0, 1, -1))}.items():
    cnt, area = planar_count(normal, u, w)
    v.check(key, cnt / (area * a_cm**2))
v.check("Ex 09-01.1g", N_si / 1e16)

inf = math.inf
v.check("Ex 09-01.2a", A_SI * spacing((1, inf, inf)))
v.check("Ex 09-01.2b", A_SI * spacing((1, 1, inf)))
v.check("Ex 09-01.2c", A_SI * spacing((1, 1, 1)))
v.check("Ex 09-01.2d", A_SI * spacing((0.5, 1, inf)))
n100 = plane_normal((1, inf, inf))[0]
n110 = plane_normal((1, 1, inf))[0]
n111 = plane_normal((1, 1, 1))[0]
v.check("Ex 09-01.2e", angle(n100, n111))
v.check("Ex 09-01.2f", angle(n100, n110))
n320 = plane_normal((2, 3, inf))[0]
v.assert_true(np.allclose(n320 / np.abs(n320).max() * 3, (3, 2, 0)), "intercepts 2, 3, inf give (320)")
v.assert_true(abs(np.dot((1, 1, 0), (0, 0, 1))) < 1e-12 and abs(np.dot((-1, 1, 0), (0, 0, 1))) < 1e-12
              and np.dot((1, 1, 1), (0, 0, 1)) != 0, "[110] and [-110] lie in (001); [111] does not")

# Example 3: P = 3, d = 0.5 nm
P3, d3 = 3.0, 0.5e-9
Ed3 = e_scale(d3)
e3 = kp_edges(P3, d3)
xb3, x23 = math.sqrt(e3[0] / Ed3), math.sqrt(e3[2] / Ed3)
v.check("Ex 09-01.3a", Ed3)
v.check("Ex 09-01.3b", xb3)
v.check("Ex 09-01.3c", e3[0])
v.check("Ex 09-01.3d", e3[1])
v.check("Ex 09-01.3e", x23)
v.check("Ex 09-01.3f", e3[2])
v.check("Ex 09-01.3g", e3[2] - e3[1])
v.check("Ex 09-01.3h", e3[3])
Fp3 = dF_dx(xb3, P3, d3)
v.check("Ex 09-01.3i", Fp3)
v.check("Ex 09-01.3j", kp_mass(P3, d3, e3[0]))
v.assert_true(abs(-Fp3 / xb3 - kp_mass(P3, d3, e3[0])) < 2e-3, "m*/m0 = -F'(x_b)/x_b agrees with the fitted band")
x = 2.0
newton = []
for _ in range(3):
    x = x - (F_of_x(x, P3, d3) - 1) / dF_dx(x, P3, d3)
    newton.append(x)
v.check("Ex 09-01.3k", newton[0])
v.check("Ex 09-01.3l", newton[1])
v.assert_true(abs(e3[1] - Ed3 * math.pi**2) < 1e-9, "band 1 top at x = pi for any P")

# Example 4: silicon masses
mc_si = conductivity_mass(SI_VALLEYS)
mdn_si = dos_mass(SI_VALLEYS)
mdp_si = (0.49**1.5 + 0.16**1.5) ** (2 / 3)
v.check("Ex 09-01.4a", mc_si)
v.check("Ex 09-01.4b", mdn_si)
v.check("Ex 09-01.4c", mdp_si)
NC, NV = N_eff(mdn_si), N_eff(mdp_si)
v.check("Ex 09-01.4d", NC)
v.check("Ex 09-01.4e", NV)
v.check("Ex 09-01.4f", abs(NC - 2.8e19) / 2.8e19 * 100)
v.check("Ex 09-01.4g", abs(NV - 1.04e19) / 1.04e19 * 100)
v.check("Ex 09-01.4h", N_eff(1.0))
v.check("Ex 09-01.4i", N_eff(1.18))
v.check("Ex 09-01.4j", N_eff(0.81))
v.check("Ex 09-01.4k", 2.8e19 / 4.7e17)
v.check("Ex 09-01.4l", (3.2e19 - 2.8e19) / 2.8e19 * 100)
v.check("Ex 09-01.4m", (1.8e19 - 1.04e19) / 1.04e19 * 100)

# Example 5: band diagram, energies measured from the vacuum level
E0 = 0.0
chi, Eg = 4.05, 1.12
Ec = E0 - chi
Ev = Ec - Eg
v.check("Ex 09-01.5a", E0 - (Ec - 0.20))
v.check("Ex 09-01.5e", Ec - (Ev + 0.15))
v.check("Ex 09-01.5b", E0 - (Ev + 0.15))
field, L = 2e4 * 100, 1e-6          # V/m, m
drop = Q * field * L / EV           # eV of potential-energy rise along +x
v.check("Ex 09-01.5c", drop)
v.check("Ex 09-01.5d", drop)
v.check("Ex 09-01.5f", 1400e-4 * 0.26 * M0 / Q * 1e12)

# Example 6
v.check("Ex 09-01.6a", varshni(77, *SI))
v.check("Ex 09-01.6b", varshni(300, *SI))
v.check("Ex 09-01.6c", varshni(400, *SI))
v.check("Ex 09-01.6d", dvarshni(300, *SI) * 1e3)
Eg_gaas300 = varshni(300, *GAAS)
v.check("Ex 09-01.6e", Eg_gaas300)
v.check("Ex 09-01.6f", HC / Eg_gaas300)
v.check("Ex 09-01.6g", HC / varshni(300, *SI))
y_match = brentq(lambda y: (1 - y) * A_GAAS + y * A_INAS - A_INP, 0, 1)
v.check("Ex 09-01.6h", y_match)


def gainas(y, T):
    return (1 - y) * varshni(T, *GAAS) + y * varshni(T, *INAS) - B_GAINAS * y * (1 - y)


v.check("Ex 09-01.6i", gainas(0.53, 0.0))
v.check("Ex 09-01.6j", varshni(300, *INAS))
v.check("Ex 09-01.6k", B_GAINAS * 0.53 * 0.47)
v.check("Ex 09-01.6l", gainas(0.53, 300))
v.check("Ex 09-01.6m", HC / gainas(0.53, 300))
v.check("Ex 09-01.6n", (A_GE - A_SI) / A_SI * 100)
v.check("Ex 09-01.6o", (A_ALAS - A_GAAS) / A_GAAS * 100)
shrink = varshni(300, *SI) - varshni(400, *SI)
kT400 = KB * 400 / EV
v.check("Ex 09-01.6p", shrink * 1e3)
v.check("Ex 09-01.6q", kT400 * 1e3)
v.check("Ex 09-01.6r", math.exp(shrink / kT400))

# T rows: packing fractions from sphere volumes in the cell
r_touch = r1 / 2
v.check("T 09-01.a", n_cell * 4 / 3 * math.pi * r_touch**3)
r_fcc = math.sqrt(2) / 4                    # FCC spheres touch along the face diagonal
v.check("T 09-01.b", 4 * 4 / 3 * math.pi * r_fcc**3 * 100)

# Concept check 7: 0.5 eV over 100 nm
v.check("C 09-01.a", 0.5 / 100e-7)

# Practitioner rows
v.check("P 09-01.a", (300 / 200) ** 2)
v.check("P 09-01.b", 8500 / 1400)

# ================================================================= solutions
# 1: germanium
a_ge = A_GE * 1e-8
N_ge = n_cell / a_ge**3
v.check("09-01.1a", N_ge)
v.check("09-01.1b", r1 * A_GE)
v.check("09-01.1c", r2 * A_GE)
M_ge = 5.3234 * NA / N_ge
v.check("09-01.1d", M_ge)
v.check("09-01.1e", (r1 * A_GE - r1 * A_SI) / (r1 * A_SI) * 100)
v.check("09-01.1f", M_ge / 28.0855)
v.check("09-01.1g", 5.3234 / (N_si * 28.0855 / NA))
v.check("09-01.1h", 28.0855)

# 2: (231) spacing from intercepts 3, 2, 6
n231 = plane_normal((3, 2, 6))[0]
v.assert_true(np.allclose(n231 / np.abs(n231).min(), (2, 3, 1)), "intercepts 3, 2, 6 give (231)")
nb = plane_normal((0.5, inf, 1))[0]
v.assert_true(np.allclose(np.abs(nb) / np.abs(nb).max() * 2, (2, 0, 1)), "intercepts 1/2, inf, 1 give (201)")
v.check("09-01.2a", A_SI * spacing((1 / 2, 1 / 3, 1)))      # the (231) plane nearest the origin

# 3: angles
v.check("09-01.3a", angle((1, 1, 0), plane_normal((1, 1, 1))[0]))
v.check("09-01.3b", angle(plane_normal((1, 1, 1))[0], plane_normal((-1, 1, 1))[0]))
v.assert_true(abs(np.dot((1, -1, 0), plane_normal((1, 1, 1))[0])) < 1e-12, "[1-10] lies in (111)")
v.check("09-01.3c", angle_signed((1, 1, 1), (1, -1, -1)))

# 4: GaAs, counting one sublattice
a_g = A_GAAS * 1e-8
v.check("09-01.4a", n_cell / a_g**3)
cnt_ga, area = planar_count((0, 0, 1), (1, 0, 0), (0, 1, 0), which=0)
cnt_as, _ = planar_count((0, 0, 1), (1, 0, 0), (0, 1, 0), which=1)
v.assert_true(cnt_ga == 2 and cnt_as == 0, "the z = 0 (100) plane of GaAs holds Ga only")
v.check("09-01.4b", cnt_ga / (area * a_g**2))
cnt111, area111 = planar_count((1, 1, 1), (1, -1, 0), (0, 1, -1), which=0)
v.check("09-01.4c", cnt111 / (area111 * a_g**2))

# 5: wafer geometry
side = np.cross((0, 0, 1), (1, 1, 0))
v.assert_true(np.allclose(side, (-1, 1, 0)), "fin along [110] on (001) has (-110) sidewalls")
v.assert_true(np.allclose(np.cross((0, 0, 1), (1, 0, 0)), (0, 1, 0)), "fin along [100] has (010) sidewalls")
th = angle((0, 0, 1), (1, 1, 1))
v.check("09-01.5a", th)
half = 10.0 / 2
v.check("09-01.5b", half * math.tan(math.radians(th)))
v.check("09-01.5c", math.hypot(half, half * math.tan(math.radians(th))))

# 6: P = 1.5, d = 0.4 nm
P6, d6 = 1.5, 0.4e-9
Ed6 = e_scale(d6)
e6 = kp_edges(P6, d6)
xb6, x26 = math.sqrt(e6[0] / Ed6), math.sqrt(e6[2] / Ed6)
v.check("09-01.6a", Ed6)
v.check("09-01.6o", Ed6 * EV)
v.check("09-01.6b", xb6)
v.check("09-01.6c", e6[0])
v.check("09-01.6d", e6[1])
v.check("09-01.6e", e6[1] - e6[0])
v.check("09-01.6f", x26)
v.check("09-01.6g", e6[2])
v.check("09-01.6h", e6[2] - e6[1])
v.check("09-01.6i", dF_dx(xb6, P6, d6))
v.check("09-01.6j", kp_mass(P6, d6, e6[0]))
v.check("09-01.6k", (e6[1] - e6[0]) / Ed6)
v.check("09-01.6l", (e3[1] - e3[0]) / Ed3)
v.check("09-01.6m", (e6[2] - e6[1]) / Ed6)
v.check("09-01.6n", (e3[2] - e3[1]) / Ed3)

# 7: strong barriers (in units of E_d; d is arbitrary)
for P, ids in ((20, "abcde"), (50, "fghij")):
    e = kp_edges(P, d3)
    xb = math.sqrt(e[0] / Ed3)
    width = (e[1] - e[0]) / Ed3
    approx = 4 * math.pi**2 / P
    v.check(f"09-01.7{ids[0]}", xb)
    v.check(f"09-01.7{ids[1]}", math.pi * (1 - 2 / P))
    v.check(f"09-01.7{ids[2]}", width)
    v.check(f"09-01.7{ids[3]}", approx)
    v.check(f"09-01.7{ids[4]}", (approx - width) / width * 100)

# 8: tight-binding band, derivatives taken numerically
t, dd = 0.5, 0.3e-9
Ek = lambda k: (-2 * t * math.cos(k * dd)) * EV          # J, E0 = 0
ks = np.linspace(0, math.pi / dd, 20001)
Es = np.array([Ek(k) for k in ks])
v.check("09-01.8a", (Es.max() - Es.min()) / EV)
h = 1e5
curv = lambda k: (Ek(k + h) - 2 * Ek(k) + Ek(k - h)) / h**2
v.check("09-01.8b", HBAR**2 / curv(0.0) / M0)
v.check("09-01.8c", HBAR**2 / curv(math.pi / dd) / M0)
vg = np.gradient(Es, ks) / HBAR
i = int(np.argmax(vg))
v.check("09-01.8d", ks[i])
v.check("09-01.8e", vg[i])

# 9: germanium masses
mc_ge = conductivity_mass(GE_VALLEYS)
v.assert_true(abs(conductivity_mass(GE_VALLEYS, (0, 1, 1)) - mc_ge) < 1e-12, "Ge conductivity mass is isotropic")
v.check("09-01.9a", mc_ge)
v.check("09-01.9i", 1 / 1.6 + 2 / 0.08)
v.check("09-01.9b", dos_mass(GE_VALLEYS[:1]))
mdn_ge = dos_mass(GE_VALLEYS)
v.check("09-01.9c", mdn_ge)
NC_ge = N_eff(mdn_ge)
v.check("09-01.9d", NC_ge)
v.check("09-01.9e", (1.04e19 - NC_ge) / 1.04e19 * 100)
mdp_ge = (0.33**1.5 + 0.043**1.5) ** (2 / 3)
v.check("09-01.9f", mdp_ge)
NV_ge = N_eff(mdp_ge)
v.check("09-01.9g", NV_ge)
v.check("09-01.9h", (6.0e18 - NV_ge) / 6.0e18 * 100)

# 10: band diagram
Ec = -4.05
EF = Ec - 0.25
v.check("09-01.10a", 0.0 - EF)
v.check("09-01.10b", 4.50 - (0.0 - EF))
v.check("09-01.10c", 0.30 / 50e-7)
v.check("09-01.10d", 0.30)

# 11: GaAs laser
v.check("09-01.11a", varshni(77, *GAAS))
v.check("09-01.11b", varshni(300, *GAAS))
v.check("09-01.11c", varshni(400, *GAAS))
v.check("09-01.11d", dvarshni(300, *GAAS) * 1e3)
lam = lambda T: HC / varshni(T, *GAAS)
v.check("09-01.11e", lam(300))
v.check("09-01.11f", (lam(300.001) - lam(299.999)) / 0.002)
v.check("09-01.11g", varshni(350, *GAAS))
v.check("09-01.11h", lam(350))
v.check("09-01.11i", lam(350) - lam(300))
v.check("09-01.11j", (lam(300.001) - lam(299.999)) / 0.002 * 50)

# 12: strain from mismatch
a_sige = 0.75 * A_SI + 0.25 * A_GE
v.check("09-01.12a", a_sige)
v.check("09-01.12b", (a_sige - A_SI) / A_SI * 100)
v.check("09-01.12c", (A_SI - a_sige) / a_sige * 100)
a_gi = 0.40 * A_GAAS + 0.60 * A_INAS
v.check("09-01.12d", a_gi)
v.check("09-01.12e", (a_gi - A_INP) / A_INP * 100)

# 13: extended-wavelength detector
Et = HC / 2000
v.check("09-01.13a", Et)
y2 = brentq(lambda y: gainas(y, 300) - Et, 0, 1)
v.check("09-01.13b", y2)
a2 = (1 - y2) * A_GAAS + y2 * A_INAS
v.check("09-01.13c", a2)
v.check("09-01.13d", (a2 - A_INP) / A_INP * 100)
v.check("09-01.13e", HC / varshni(300, *INAS))
v.check("09-01.13f", (A_INAS - A_INP) / A_INP * 100)
poly = np.polyfit(np.linspace(0, 1, 11), [gainas(y, 300) for y in np.linspace(0, 1, 11)], 2)
v.check("09-01.13g", poly[1])
v.check("09-01.13h", poly[2] - Et)

# 14: valley splitting, populations from Boltzmann factors summed over all six valleys
kT300 = KB * 300 / EV


def low_fraction(dE):
    w = np.array([math.exp(dE / kT300)] * 2 + [1.0] * 4)
    return w[:2].sum() / w.sum()


v.check("09-01.14a", low_fraction(0.0))
v.check("09-01.14b", brentq(lambda dE: low_fraction(dE) - 0.8, 0, 0.5) * 1e3)
v.check("09-01.14c", low_fraction(0.10))

# 15: conductivity mass along x with repopulated valleys, from the tensors
def mc_strained(f):
    inv_xx = [t[0, 0] for t in SI_VALLEYS]          # order: +x, -x, +y, -y, +z, -z
    weights = [(1 - f) / 4] * 4 + [f / 2] * 2
    return 1 / sum(w * i for w, i in zip(weights, inv_xx))


v.assert_true(abs(mc_strained(1 / 3) - mc_si) < 1e-12, "f = 1/3 reproduces the unstrained conductivity mass")
v.check("09-01.15a", mc_strained(0.8))
v.check("09-01.15f", 1 / mc_strained(0.8))
v.check("09-01.15b", mc_si / mc_strained(0.8))
v.check("09-01.15c", mc_si / mc_strained(1.0))
v.check("09-01.15d", 1.5 / (mc_si / mc_strained(1.0)))
v.check("09-01.15e", 2.0 / (mc_si / mc_strained(1.0)))

# ================================================================= lab
widths = {}
for P in (3, 6, 12):
    e = kp_edges(P, d3)
    widths[P] = (e[1] - e[0], e[2] - e[1], kp_mass(P, d3, e[0]))
v.check("Lab 09-01.a", widths[3][0])
v.check("Lab 09-01.b", widths[6][0])
v.check("Lab 09-01.c", widths[6][1])
v.check("Lab 09-01.d", widths[6][2])
v.check("Lab 09-01.e", widths[12][0])
v.check("Lab 09-01.f", widths[12][1])
v.check("Lab 09-01.g", widths[12][2])
v.check("Lab 09-01.h", (widths[6][0] - widths[3][0]) / widths[3][0] * 100)
v.check("Lab 09-01.i", (widths[6][2] - widths[3][2]) / widths[3][2] * 100)
v.check("Lab 09-01.j", r2 * A_SI)

v.finish()
