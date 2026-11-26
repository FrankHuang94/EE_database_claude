#!/usr/bin/env python3
"""Verify every number in chapter 25-03 (deposition, etch, CMP, implant, metrology), its problems and lab.

Independent routes (the lab module units.py uses closed forms and an explicit finite-difference solver):
- CVD growth from solving the steady-state flux balance numerically for the surface concentration;
- plating thickness from integrating charge (mol of electrons to grams to volume);
- implant profiles by numerical integration (dose check) and root-finding for junction depths;
- anneal broadening by convolving profiles numerically, and a Crank-Nicolson solver with a reflecting
  surface for the lab's junction depth;
- out-of-spec fractions from the normal distribution; gauge noise by simulation.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, linalg, optimize
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-03", ROOT / "chapters" / "25-03-deposition-etch-cmp-implant-metrology.md",
                        ROOT / "solutions" / "25-03-solutions.md", LAB / "README.md")

K = 8.617333262e-5
Q_E = 1.602176634e-19
F = 96485.33212
PSI = 6895.0


def kt(tc):
    return K * (tc + 273.15)


def ks_at(tc, ks_ref=0.05, t_ref=650, ea=1.5):
    return ks_ref * math.exp(-(ea / K) * (1 / (tc + 273.15) - 1 / (t_ref + 273.15)))


def eff_constant(ks, hg):
    """Solve hg*(Cg - Cs) = ks*Cs for Cs numerically (Cg = 1) and return the flux."""
    cs = optimize.brentq(lambda c: hg * (1 - c) - ks * c, 0, 1)
    return ks * cs


def plating_rate_cm_s(j, m=63.55, rho=8.96, n=2):
    mol_e = j / F                 # mol electrons per cm2 per s
    grams = mol_e / n * m
    return grams / rho


def boron_d(tc):
    return 0.76 * math.exp(-3.46 / kt(tc))


# ---------------------------------------------------------------- Example 1, text
e650 = eff_constant(0.05, 2.0)
v.check("Ex 25-03.1a", e650)
v.check("Ex 25-03.1a1", e650 * 3e16 / 5e22 * 1e7 * 60)
v.check("Ex 25-03.1b0", ks_at(660))
v.check("Ex 25-03.1b1", eff_constant(ks_at(660), 2.0))
v.check("Ex 25-03.1b", 100 * (eff_constant(ks_at(660), 2.0) / e650 - 1))
v.check("Ex 25-03.1c0", ks_at(950))
e950 = eff_constant(ks_at(950), 2.0)
v.check("Ex 25-03.1c1", e950)
v.check("Ex 25-03.1c2", e950 * 3e16 / 5e22 * 1e7 * 60)
v.check("Ex 25-03.1c", 100 * (eff_constant(ks_at(960), 2.0) / e950 - 1))
v.check("Txt 25-03.a", 100 * ((eff_constant(ks_at(660), 2.0) / e650) ** 0.1 - 1))

# ---------------------------------------------------------------- Example 2
v.check("Ex 25-03.2a", 2.0 / 0.10)
v.check("Ex 25-03.2a1", 2.0 / 0.10 * 4.0)
v.check("Ex 25-03.2b", 20 / 0.10)
v.check("Ex 25-03.2b1", 20 / 0.10 * 4.0 / 60)

# ---------------------------------------------------------------- Example 3
r3 = plating_rate_cm_s(0.010)
v.check("Ex 25-03.3a", r3)
v.check("Ex 25-03.3a1", r3 * 1e7)
v.check("Ex 25-03.3a2", r3 * 1e4 * 60)
v.check("Ex 25-03.3b", optimize.brentq(lambda t: r3 * t - 1.0e-4, 1, 1e4))

# ---------------------------------------------------------------- Example 4
v.check("Ex 25-03.4a", 100 / 50)
v.check("Ex 25-03.4a1", 100 / (50 * 0.95))
t_fast = 100 / (50 * 1.05)
v.check("Ex 25-03.4a2", t_fast)
v.check("Ex 25-03.4b0", t_fast)
v.check("Ex 25-03.4a3", 1.2 * 2.0)
v.check("Ex 25-03.4b", 2.4 - t_fast)
v.check("Ex 25-03.4c", (2.4 - t_fast) * 52.5 / 20)
v.assert_true("total etch time clears the slowest region", 2.4 > 100 / 47.5)

# ---------------------------------------------------------------- Example 5
p2 = 2.0 * PSI
rr = 2.4e-13 * p2 * 1.0
v.check("Ex 25-03.5a0", p2)
v.check("Ex 25-03.5a", rr)
v.check("Ex 25-03.5a1", rr * 1e9 * 60)
v.check("Ex 25-03.5b", 500 / (rr * 1e9 * 60))
v.check("Ex 25-03.5c", rr * 1e9 * 60 / 0.25)

# ---------------------------------------------------------------- Example 6, text


def peak(dose, drp_nm):
    return dose / (math.sqrt(2 * math.pi) * drp_nm * 1e-7)


v.check("Ex 25-03.6a", 1e15 * Q_E * 707 / 0.010)
np6 = peak(1e15, 12)
v.check("Ex 25-03.6b", np6)
xs = np.linspace(-200, 300, 200001)
prof = np6 * np.exp(-(xs - 30) ** 2 / (2 * 12**2))
v.assert_true("Gaussian profile integrates to the dose", abs(integrate.trapezoid(prof, xs * 1e-7) / 1e15 - 1) < 1e-6)
v.check("Ex 25-03.6c0", math.sqrt(2 * math.log(np6 / 1e18)))
v.check("Ex 25-03.6c", optimize.brentq(lambda x: np6 * math.exp(-(x - 30) ** 2 / 288) - 1e18, 30, 200))
v.check("Txt 25-03.d", np6 / 1e18)

# ---------------------------------------------------------------- Example 7, text
v.check("Ex 25-03.7a0", kt(1000))
d1000, d1050 = boron_d(1000), boron_d(1050)
v.check("Ex 25-03.7a", d1000)
add_f = math.sqrt(2 * d1000 * 1800) * 1e7
v.check("Ex 25-03.7a1", add_f)
v.check("Ex 25-03.7a2", add_f)
# second route: numerically convolve the 12 nm Gaussian with the diffusion kernel and measure the new std
grid = np.linspace(-600, 600, 24001)
g1 = np.exp(-grid**2 / (2 * 12**2))
g2 = np.exp(-grid**2 / (2 * add_f**2))
conv = np.convolve(g1, g2, mode="same")
std_new = math.sqrt(integrate.trapezoid(conv * grid**2, grid) / integrate.trapezoid(conv, grid))
v.check("Ex 25-03.7a3", std_new)
v.check("Ex 25-03.7a4", 12 / std_new)
v.check("Ex 25-03.7b", d1050)
add_s = math.sqrt(2 * d1050 * 1.0) * 1e7
v.check("Ex 25-03.7b1", add_s)
s_new = math.hypot(12, add_s)
v.check("Ex 25-03.7b2", s_new)
v.check("Ex 25-03.7b3", 12 / s_new)
v.check("Txt 25-03.b", d1050 / d1000)
v.check("Txt 25-03.c", 1800 / 1.0)

# ---------------------------------------------------------------- Example 8
v.check("Ex 25-03.8a", min(21.5 - 20.3, 20.3 - 18.5) / (3 * 0.40))
v.check("Ex 25-03.8a1", norm.sf(21.5, 20.3, 0.40) + norm.cdf(18.5, 20.3, 0.40))
so = math.hypot(0.40, 0.15)
v.check("Ex 25-03.8b", so)
v.check("Ex 25-03.8b1", 1.2 / (3 * so))
v.check("Ex 25-03.8c", 6 * 0.15 / 3.0)

# ---------------------------------------------------------------- Example 9, text
v.check("Ex 25-03.9a", 100 * (143.9 / 116.9 - 1))
v.check("Ex 25-03.9b", 100 * 78.0 / 143.9)
v.check("Ex 25-03.9b1", 100 * 38.8 / 143.9)
v.check("Ex 25-03.9b2", 100 * 13.9 / 143.9)
v.check("Ex 25-03.9c", 165.9 / 1.232)
v.check("Ex 25-03.9c1", 100 * (136.2 / (165.9 / 1.232) - 1))
v.check("Txt 25-03.e", 116.9)

# ---------------------------------------------------------------- Problems 1-7
v.check("25-03.1a", eff_constant(20, 1.0))
v.check("25-03.2c", optimize.brentq(lambda t: ks_at(t) - 2.0, 600, 1200))
v.check("25-03.3a0", 3.0 / 0.09)
v.check("25-03.3a", math.ceil(3.0 / 0.09))
v.check("25-03.3b", math.ceil(3.0 / 0.09) * 3.0)
r4 = plating_rate_cm_s(0.020)
v.check("25-03.4a", r4 * 1e7)
t4 = 1.5e-4 / r4
v.check("25-03.4b", t4)
v.check("25-03.4c", 0.020 * 707 * t4)
tn = 80 / 60
v.check("25-03.5a0", tn)
v.check("25-03.5a", 1.3 * tn)
fast = 60 * 1.08
v.check("25-03.5b0", fast)
v.check("25-03.5b", 80 / fast)
expo = 1.3 * tn - 80 / fast
v.check("25-03.5b1", expo)
v.check("25-03.5c", optimize.brentq(lambda s: expo * fast / s - 1.0, 1, 1000))
v.check("25-03.6a", 300 * 1.1)
v.check("25-03.6b", 1000 - 2 * 300 * 1.1)
r7 = 2.4e-13 * 3.0 * PSI * 1.5 * 1e9 * 60
v.check("25-03.7a", r7)
v.check("25-03.7b", 400 / r7)

# ---------------------------------------------------------------- Problems 8-14
r8 = rr * 1e9 * 60 / 0.50
v.check("25-03.8a", r8)
v.check("25-03.8b", 300 / r8)
v.check("25-03.9a", 5e15 * Q_E * 707 / 0.0050)
np9 = peak(5e15, 20)
v.check("25-03.9b", np9)
v.check("25-03.10a", math.sqrt(2 * math.log(np9 / 1e17)))
v.check("25-03.10b", optimize.brentq(lambda x: np9 * math.exp(-(x - 50) ** 2 / 800) - 1e17, 50, 400))
v.check("25-03.11a0", kt(950))
v.check("25-03.11a", boron_d(950))
v.check("25-03.11b", 30 * d1000 / boron_d(950))
v.check("25-03.12a", 0.10 * 3.0 / 6)
v.check("25-03.12b", math.hypot(0.40, 0.050))
v.check("25-03.13a", 38.8 / 1.390)
v.check("25-03.13a1", 78.0 / 1.189)
v.check("25-03.13b", 143.9 - 116.9)
a_sige = 0.5431 + 0.30 * (0.5658 - 0.5431)
v.check("25-03.14a", a_sige)
v.check("25-03.14b", 100 * (a_sige - 0.5431) / 0.5431)

# ---------------------------------------------------------------- Lab
v.check("Lab 25-03.a", optimize.brentq(lambda t: ks_at(t) - 2.0, 600, 1200))


def crank_nicolson(x_nm, n0, d_cm2_s, t_s, steps=400):
    """Crank-Nicolson diffusion with zero flux at x = 0 and at the deep end."""
    dx = x_nm[1] - x_nm[0]
    dt = t_s / steps
    r = d_cm2_s * 1e14 * dt / dx**2
    n = len(x_nm)
    lap = np.zeros((3, n))
    main = np.full(n, -2.0)
    up = np.ones(n - 1)
    lo = np.ones(n - 1)
    up[0] = 2.0     # mirror at the surface
    lo[-1] = 2.0    # mirror at the deep end
    a_band = np.zeros((3, n))
    a_band[0, 1:] = -r / 2 * up
    a_band[1, :] = 1 - r / 2 * main
    a_band[2, :-1] = -r / 2 * lo
    u = n0.copy()
    for _ in range(steps):
        rhs = u * (1 + r / 2 * main)
        rhs[:-1] += r / 2 * up * u[1:]
        rhs[1:] += r / 2 * lo * u[:-1]
        u = linalg.solve_banded((1, 1), a_band, rhs)
    del lap
    return u


xg = np.linspace(0, 800, 3201)
n0 = np6 * (np.exp(-(xg - 30) ** 2 / 288) + np.exp(-(xg + 30) ** 2 / 288))
n_f = crank_nicolson(xg, n0, d1000, 1800)
xj_cn = optimize.brentq(lambda z: np.interp(z, xg, n_f) - 1e18, 30, 790)
v.check("Lab 25-03.b", xj_cn)
v.check("Lab 25-03.b1", n_f[0])
v.check("Lab 25-03.c", 300 / (rr * 1e9 * 60 / 0.25))
v.check("Lab 25-03.d", 1.2 / (3 * math.hypot(0.40, 0.05)))
rng = np.random.default_rng(5)
meas = 20.3 + rng.normal(0, 0.40, 200_000) + rng.normal(0, 0.05, 200_000)
cpk_sim = min(21.5 - meas.mean(), meas.mean() - 18.5) / (3 * meas.std())
v.assert_true("simulated apparent Cpk within 2% of formula", abs(cpk_sim / (1.2 / (3 * math.hypot(0.40, 0.05))) - 1) < 0.02)

# Problem 15: two-step diffusion. Independent routes: numerical quadrature for the dose, root-finding
# for the junctions, and an image-method convolution for the drive-in from the true erfc profile.
from scipy.special import erfc as _erfc  # noqa: E402

c_s, n_b = 2.5e20, 1.0e16
d950 = 0.76 * math.exp(-3.46 / kt(950))
t_pre = 20 * 60
l_pre = math.sqrt(d950 * t_pre)
v.check("25-03.15b", d950)
v.check("25-03.15b1", l_pre * 1e7)
q_num, _ = integrate.quad(lambda x: c_s * _erfc(x / (2 * l_pre)), 0, 60 * l_pre)
v.assert_true("25-03.15 dose closed form equals quadrature",
              abs(q_num - 2 * c_s * l_pre / math.sqrt(math.pi)) / q_num < 1e-8)
v.check("25-03.15b2", q_num)
eta_j = optimize.brentq(lambda e: _erfc(e) - n_b / c_s, 0.5, 6)
v.check("25-03.15b3", eta_j)
v.check("25-03.15b4", 2 * l_pre * eta_j * 1e7)
# the PDE residual of the erfc solution, by finite differences at a few points
for xx, tt in ((2e-6, 600.0), (5e-6, 1200.0)):
    f = lambda x, t: c_s * _erfc(x / (2 * math.sqrt(d950 * t)))  # noqa: E731
    hx, ht = 1e-8, 1e-2
    dct = (f(xx, tt + ht) - f(xx, tt - ht)) / (2 * ht)
    dcxx = (f(xx + hx, tt) - 2 * f(xx, tt) + f(xx - hx, tt)) / hx**2
    v.assert_true(f"25-03.15 erfc satisfies diffusion eq at x={xx}", abs(dct - d950 * dcxx) / abs(dct) < 1e-3)
d1100 = 0.76 * math.exp(-3.46 / kt(1100))
dt_drive = d1100 * 3600
v.check("25-03.15c", d1100)
v.check("25-03.15c1", dt_drive / (d950 * t_pre))
v.check("25-03.15c2", math.sqrt(dt_drive / (d950 * t_pre)))
c_surf = q_num / math.sqrt(math.pi * dt_drive)
v.check("25-03.15d", c_surf)
xj_sheet = optimize.brentq(lambda x: c_surf * math.exp(-x * x / (4 * dt_drive)) - n_b, 1e-6, 1e-3)
v.check("25-03.15d1", xj_sheet * 1e4)
v.check("25-03.15d2", c_s / c_surf)
v.check("25-03.15d3", xj_sheet / (2 * l_pre * eta_j))
_eta = 3.0
for _ in range(20):
    _eta = math.sqrt(-math.log(n_b / c_s * math.sqrt(math.pi) * _eta))
v.assert_true("25-03.15 asymptotic erfc iteration within 1% of exact root", abs(_eta - eta_j) / eta_j < 0.01)


def drive_in_exact(x):
    """Reflecting-surface drive-in of the erfc predeposition profile (method of images)."""
    g = lambda xi: c_s * _erfc(xi / (2 * l_pre)) * (  # noqa: E731
        math.exp(-(x - xi) ** 2 / (4 * dt_drive)) + math.exp(-(x + xi) ** 2 / (4 * dt_drive))) \
        / math.sqrt(4 * math.pi * dt_drive)
    return integrate.quad(g, 0, 40 * l_pre, limit=200)[0]


xj_exact = optimize.brentq(lambda x: drive_in_exact(x) - n_b, 1e-5, 5e-4)
v.assert_true("25-03.15 sheet approximation within 1% of exact drive-in junction",
              abs(xj_exact - xj_sheet) / xj_exact < 0.01, f"{xj_exact*1e4:.4f} vs {xj_sheet*1e4:.4f} um")

# Problem 16: four-point probe and activation. Rs from superposed point-source potentials.
def rs_from_probe(v_meas, i_force, s=1.0):
    # potential difference between probes 2 and 3 per unit Rs, from +I at 0 and -I at 3s
    pot = lambda r: -math.log(r) / (2 * math.pi)  # noqa: E731
    dv_per_rs = i_force * ((pot(s) - pot(2 * s)) - (pot(2 * s) - pot(s)))
    return v_meas / dv_per_rs


rs_lo = rs_from_probe(41.7e-3, 1.0e-3)
rs_hi = rs_from_probe(16.2e-3, 1.0e-3)
v.check("25-03.16a", rs_lo)
v.check("25-03.16a1", rs_hi)
qa_lo = 1 / (Q_E * 50 * rs_lo)
qa_hi = 1 / (Q_E * 50 * rs_hi)
v.check("25-03.16b", qa_lo)
v.check("25-03.16b1", 100 * qa_lo / 2.0e15)
v.check("25-03.16b2", qa_hi)
v.check("25-03.16b3", 100 * qa_hi / 2.0e15)
v.check("25-03.16c", 20 * rs_hi / 1e3)

sys.exit(v.finish())
