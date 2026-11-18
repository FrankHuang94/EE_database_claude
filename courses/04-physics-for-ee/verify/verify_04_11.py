#!/usr/bin/env python3
"""Verify every number published in chapter 04-11, its solutions and its lab handout.

Independent routes: atoms counted by generating the diamond lattice explicitly; Fermi energies by
solving the integrated density of states for the electron count; averages by quadrature; band
widths, curvatures and velocities from diagonalized tight-binding matrices and finite differences;
gaps by diagonalizing the plane-wave Hamiltonian; Sommerfeld's heat capacity by numerically
differentiating the Fermi-gas energy; temperatures by root-finding.
"""
from __future__ import annotations

import sys
import warnings
from itertools import product
from math import exp, log, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-11", C_DIR / "chapters" / "04-11-intro-solid-state-physics.md",
                        C_DIR / "solutions" / "04-11-solutions.md", C_DIR / "labs" / "04-11-lab" / "README.md")
H = 6.62607015e-34
E_CH = 1.602176634e-19
KB = 1.380649e-23
ME = 9.1093837139e-31
NA = 6.02214076e23
R = KB * NA
HBAR = H / (2 * pi)
HC_EV_NM = H * 299792458.0 / E_CH * 1e9
A_SI = 0.543102e-9
KT300 = KB * 300 / E_CH


def diamond_sites(a, cells=2):
    """All diamond-lattice sites in a block of cells×cells×cells cubic cells."""
    fcc = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]])
    basis = np.vstack([fcc, fcc + 0.25])
    pts = [basis + np.array(c) for c in product(range(cells), repeat=3)]
    return np.vstack(pts) * a


def atoms_per_cell(a):
    pts = diamond_sites(a, 3) / a
    inside = np.all((pts >= 1 - 1e-9) & (pts < 2 - 1e-9), axis=1)     # the middle cell, half-open
    return int(inside.sum())


def nearest_neighbor(a):
    pts = diamond_sites(a, 3)
    centre = pts[np.argmin(np.linalg.norm(pts - 1.5 * a, axis=1))]
    d = np.linalg.norm(pts - centre, axis=1)
    return d[d > 1e-15].min()


def fermi_energy(n, m=ME):
    """Solve integral of g(E)/V from 0 to E_F = n for the free-electron gas (J)."""
    count = lambda E: (1 / (3 * pi**2)) * (2 * m * E / HBAR**2) ** 1.5
    return brentq(lambda E: count(E) - n, 1e-22, 1e-16, xtol=1e-35, rtol=1e-14)


def sommerfeld_c(t):
    """Heat capacity per electron (units of k) for g ∝ √E, E_F = 1, at kT = t, by numerical derivative."""
    def mu_of(tt):
        num = lambda mu: quad(lambda E: np.sqrt(E) / (1 + np.exp((E - mu) / tt)), 0, mu + 40 * tt,
                              limit=400, epsabs=1e-13)[0] - 2 / 3
        return brentq(num, 0.5, 1.5, xtol=1e-14)

    def energy(tt):
        mu = mu_of(tt)
        return quad(lambda E: E**1.5 / (1 + np.exp((E - mu) / tt)), 0, mu + 40 * tt, limit=400,
                    epsabs=1e-13)[0] / (2 / 3)
    dt = 1e-3 * t
    return (energy(t + dt) - energy(t - dt)) / (2 * dt)


def chain_levels(n_atoms, t, ring=False):
    hm = -t * (np.eye(n_atoms, k=1) + np.eye(n_atoms, k=-1))
    if ring:
        hm[0, -1] = hm[-1, 0] = -t
    return np.linalg.eigvalsh(hm)


def tb_band(k, t, a):
    """Tight-binding band from a single-site Bloch sum, evaluated numerically (E0 = 0)."""
    return float(np.real(-t * (np.exp(1j * k * a) + np.exp(-1j * k * a))))


def curvature_mass(band, k0, h):
    d2 = (band(k0 + h) - 2 * band(k0) + band(k0 - h)) / h**2
    return HBAR**2 / d2


def pw_bands(k, a, u, n_g=41):
    g = 2 * pi / a * np.arange(-(n_g // 2), n_g // 2 + 1)
    hm = np.diag(HBAR**2 * (k + g) ** 2 / (2 * ME) / E_CH) + u * (np.eye(n_g, k=1) + np.eye(n_g, k=-1))
    return np.linalg.eigvalsh(hm)


def first_order_edges(a, u):
    """Standing-wave energies by averaging V over |psi±|² numerically."""
    e0 = HBAR**2 * (pi / a) ** 2 / (2 * ME) / E_CH
    avg = lambda sgn: quad(lambda x: (1 + sgn * np.cos(2 * pi * x / a)) * 2 * u * np.cos(2 * pi * x / a), 0, a)[0] / a
    return e0, e0 + avg(-1), e0 + avg(+1)


fd = lambda dE_eV, T=300: 1 / (1 + exp(dE_eV / (KB * T / E_CH)))
ni_fit = lambda T: 5.29e19 * (T / 300) ** 2.54 * exp(-6726 / T)

# ---------------------------------------------------------------- theory
v.check("T 04-11.a", KT300 * 1e3)
v.check("T 04-11.b", brentq(lambda x: 1 / (1 + exp(x)) - 0.1, 0, 10) - brentq(lambda x: 1 / (1 + exp(x)) - 0.9, -10, 0))
v.assert_true("diamond cell counted as 8 atoms", atoms_per_cell(1.0) == 8)

# ---------------------------------------------------------------- examples
n_si = atoms_per_cell(A_SI) / (A_SI * 100) ** 3
v.check("Ex 04-11.1a", atoms_per_cell(A_SI))
v.check("Ex 04-11.1b", n_si)
v.check("Ex 04-11.1c", nearest_neighbor(A_SI) * 1e9)
v.check("Ex 04-11.1d", n_si * 28.0855 / NA)
v.check("Ex 04-11.1e", 4 * n_si)
n_cu = 8.49e28
ef_cu = fermi_energy(n_cu)
kf_cu = sqrt(2 * ME * ef_cu) / HBAR
v.check("Ex 04-11.2a", kf_cu)
v.check("Ex 04-11.2b", ef_cu / E_CH)
v.check("Ex 04-11.2c", sqrt(2 * ef_cu / ME))
v.check("Ex 04-11.2d", ef_cu / KB)
v.check("Ex 04-11.2e", quad(lambda E: E**1.5, 0, ef_cu)[0] / quad(lambda E: E**0.5, 0, ef_cu)[0] / E_CH)
v.check("Ex 04-11.2f", 1.5 * KT300 * 1e3)
v.check("Ex 04-11.2g", 2 * pi / kf_cu * 1e9)
count = lambda E: (1 / (3 * pi**2)) * (2 * ME * E / HBAR**2) ** 1.5
g_ef = (count(ef_cu * (1 + 1e-6)) - count(ef_cu * (1 - 1e-6))) / (2e-6 * ef_cu)
v.check("Ex 04-11.3a", g_ef * KB * 300 / n_cu)
tf_cu = ef_cu / KB
c_num = sommerfeld_c(300 / tf_cu)
v.assert_true("numerical Sommerfeld heat capacity matches (pi^2/2)T/T_F within 0.1%",
              abs(c_num / (pi**2 / 2 * 300 / tf_cu) - 1) < 1e-3)
v.check("Ex 04-11.3b", pi**2 / 3 * 300 / tf_cu)
v.check("Ex 04-11.3c", c_num * R)
v.check("Ex 04-11.3d", 3 * R)
tau = ME / (n_cu * E_CH**2 * 1.68e-8)
v.check("Ex 04-11.3e", tau)
v.check("Ex 04-11.3f", sqrt(2 * ef_cu / ME) * tau * 1e9)
t4, a4 = 1.0 * E_CH, 0.25e-9
lv = chain_levels(4000, 1.0, ring=True)
v.check("Ex 04-11.4a", lv[-1] - lv[0])
band4 = lambda k: tb_band(k, t4, a4)
v.check("Ex 04-11.4b", curvature_mass(band4, 0.0, 1e7) / ME)
ks = np.linspace(0, pi / a4, 20001)
v.check("Ex 04-11.4c", np.max(np.gradient([band4(k) for k in ks], ks)) / HBAR)
v.check("Ex 04-11.4d", curvature_mass(band4, pi / a4, 1e7) / ME)
a5, u5 = 0.5e-9, 0.2
e0, lo, hi = first_order_edges(a5, u5)
v.check("Ex 04-11.5a", pi / a5)
v.check("Ex 04-11.5b", e0)
v.check("Ex 04-11.5c", lo)
v.check("Ex 04-11.5d", hi)
ev = pw_bands(pi / a5, a5, u5)
v.check("Ex 04-11.5e", ev[1] - ev[0])
v.assert_true("21-wave and 41-wave bases agree on the gap", abs((pw_bands(pi / a5, a5, u5, 21)[1] - pw_bands(pi / a5, a5, u5, 21)[0]) - (ev[1] - ev[0])) < 1e-6)
v.check("Ex 04-11.6a", exp(-1.12 / (2 * KT300)))
v.check("Ex 04-11.6b", sqrt(3e19 * 1e19) * exp(-1.12 / (2 * KT300)))
ni_model = lambda T: T**1.5 * exp(-1.12 * E_CH / (2 * KB * T))
v.check("Ex 04-11.6c", ni_model(400) / ni_model(300))
v.check("Ex 04-11.6d", ni_fit(400) / ni_fit(300))
v.check("Ex 04-11.6e", exp(-3.26 / (2 * KT300)) / exp(-1.12 / (2 * KT300)))
v.check("Ex 04-11.6f", brentq(lambda T: 3.26 * E_CH / (2 * KB * T) - 1.12 / (2 * KT300), 300, 2000))

# ---------------------------------------------------------------- solutions
a_ge = 0.5658e-9
v.check("04-11.1a", atoms_per_cell(a_ge) / (a_ge * 100) ** 3)
v.check("04-11.1b", nearest_neighbor(a_ge) * 1e9)
v.check("04-11.2a", fd(3 * KT300))
v.check("04-11.2b", fd(-3 * KT300))
v.check("04-11.2c", brentq(lambda x: fd(x) - 0.01, 0, 1))
ef_al = fermi_energy(1.81e29)
v.check("04-11.3a", ef_al / E_CH)
v.check("04-11.3b", sqrt(2 * ef_al / ME))
v.check("04-11.3c", ef_al / KB)
ef_na = fermi_energy(2.65e28)
v.check("04-11.4a", ef_na / E_CH)
g_na = (count(ef_na * (1 + 1e-6)) - count(ef_na * (1 - 1e-6))) / (2e-6 * ef_na) * E_CH * 1e-6   # per eV per cm³
v.check("04-11.4b", g_na)
v.check("04-11.4c", g_na * KT300)
two = chain_levels(2, 1.5)
v.check("04-11.5a", 2 * (0 - two[0]))
six = chain_levels(6, 1.5)
v.check("04-11.5b", six[0])
v.check("04-11.5c", six[-1])
long_chain = chain_levels(4000, 1.5, ring=True)
v.check("04-11.5d", long_chain[-1] - long_chain[0])
m6 = brentq(lambda m: HBAR**2 * (2e8) ** 2 / (2 * m) - 0.010 * E_CH, 1e-33, 1e-29, xtol=1e-45)
v.check("04-11.6a", m6 / ME)
v.check("04-11.6b", E_CH * 1e5 / m6)
t7, a7 = 0.5 * E_CH, 0.3e-9
ks7 = np.linspace(0, pi / a7, 20001)
v.check("04-11.7a", np.max(np.gradient([tb_band(k, t7, a7) for k in ks7], ks7)) / HBAR)
t_edge = brentq(lambda tt: E_CH * 1e5 * tt / HBAR - pi / a7, 0, 1e-9, xtol=1e-25)
v.check("04-11.7b", t_edge * 1e12)
v.check("04-11.7c", t_edge / 0.1e-12)
v.check("04-11.8a", (2 * 4) // 2)
v.check("04-11.8b", 1 / 2)
v.check("04-11.8c", 2 * n_si / 2)
v.check("04-11.9a", ni_fit(300))
v.check("04-11.9b", ni_fit(350))
v.check("04-11.9c", ni_fit(400))
v.check("04-11.9d", brentq(lambda T: log(ni_fit(T)) - log(1e14), 300, 800))
v.check("04-11.10a", HC_EV_NM / 450)
v.check("04-11.10b", HC_EV_NM / 4.9)
v.check("04-11.10c", HC_EV_NM / 1310)
v.assert_true("only Ge absorbs 1310 nm", [g < HC_EV_NM / 1310 for g in (0.67, 1.12, 1.42)] == [True, False, False])
k_ph = 2 * pi / (HC_EV_NM / 1.12 * 1e-9)
v.check("04-11.10d", k_ph)
v.check("04-11.10e", k_ph / (pi / A_SI))
mh = 0.5 * ME
vband = lambda k: -HBAR**2 * k**2 / (2 * mh)        # J, relative to E_v
k11 = 1e9
vel = (vband(k11 + 1e3) - vband(k11 - 1e3)) / (2e3) / HBAR
v.check("04-11.11a", vel)
v.check("04-11.11b", vel)
v.check("04-11.11c", -vband(k11) / E_CH)
tf_al = ef_al / KB
c_al = sommerfeld_c(300 / tf_al)
v.check("04-11.12a", 3 * c_al * R)
v.check("04-11.12b", 3 * c_al * R / (3 * R))
e0, lo, hi = first_order_edges(0.4e-9, 0.3)
v.check("04-11.13a", e0)
v.check("04-11.13b", lo)
v.check("04-11.13c", hi)
v.check("04-11.13d", 2 * pi / (pi / 0.4e-9) * 1e9)
v.check("04-11.14a", 1e16 / n_si)
v.check("04-11.14b", 1e19 / n_si)
v.check("04-11.15a", brentq(lambda x: x * 1.2**6 - 11, 0, 11))
v.check("04-11.15b", brentq(lambda x: x * 1.35**6 - 3.5, 0, 3.5))

# ---------------------------------------------------------------- lab
nmax = 40
r = np.arange(-nmax, nmax + 1)
n2 = np.sort((r[:, None, None] ** 2 + r[None, :, None] ** 2 + r[None, None, :] ** 2).ravel())
v.check("Lab 04-11.a", n2[100_000 // 2 - 1] / (3 * 100_000 / (8 * pi)) ** (2 / 3))
v.check("Lab 04-11.b", sommerfeld_c(0.01))
c100 = chain_levels(100, 1.0)
v.check("Lab 04-11.c", c100[-1] - c100[0])
ev = pw_bands(pi / 0.5e-9, 0.5e-9, 0.5)
v.check("Lab 04-11.d", ev[1] - ev[0])
ni_sic = lambda T: 1.732e19 * (T / 300) ** 1.5 * exp(-3.26 * E_CH / (2 * KB * T))
v.check("Lab 04-11.e", brentq(lambda T: log(ni_sic(T)) - log(1e14), 300, 3000))

sys.exit(v.finish())
