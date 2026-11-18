#!/usr/bin/env python3
"""Verify every number published in chapter 04-05, its solutions and its lab handout.

Independent routes: carrier density from density, molar mass and Avogadro's number; drift and
mobility by integrating the Drude ODE to steady state; resistances by integrating rho dx / A;
temperatures by root-finding on R(T); the distributed-RC delay from the series solution of the
diffusion equation (the netlist and notebook use lumped ladders); optimum repeater count by
numerical minimization.
"""
from __future__ import annotations

import sys
import warnings
from math import log, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-05", C_DIR / "chapters" / "04-05-current-resistance-and-conduction.md",
                        C_DIR / "solutions" / "04-05-solutions.md", C_DIR / "labs" / "04-05-lab" / "README.md")
E_CH = 1.602176634e-19
ME = 9.1093837139e-31
EPS0 = 8.8541878188e-12
KB = 1.380649e-23
N_A = 6.02214076e23
RHO_CU = 1.68e-8
ALPHA = 0.00393
VF = 1.57e6
N_CU = 8.96e3 / 63.546e-3 * N_A          # one conduction electron per atom


def tau_from_rho(rho, n=N_CU):
    return brentq(lambda t: n * E_CH**2 * t / ME - 1 / rho, 1e-18, 1e-10, xtol=1e-30, rtol=1e-14)


def drude_mobility(tau):
    """Integrate m dv/dt = -eE - m v / tau to steady state and return |v|/E."""
    E = 1.0
    sol = solve_ivp(lambda t, vv: [-E_CH * E / ME - vv[0] / tau], (0, 40 * tau), [0.0], rtol=1e-12, atol=1e-20)
    return abs(sol.y[0, -1]) / E


def resistance(rho, L, area):
    return quad(lambda x: rho / area(x), 0, L, epsabs=0, epsrel=1e-12)[0]


def temp_from_R(R_hot, R_20):
    return brentq(lambda T: R_20 * (1 + ALPHA * (T - 20)) - R_hot, -100, 1000)


def rc_line_t50():
    """50% delay of a distributed RC line (step at one end, open at the other) from its series solution, in units of RC."""
    k = np.arange(0, 400)

    def v_end(t):
        return 1 - np.sum(4 / pi * (-1) ** k / (2 * k + 1) * np.exp(-(2 * k + 1) ** 2 * pi**2 * t / 4))
    return brentq(lambda t: v_end(t) - 0.5, 0.01, 2, xtol=1e-14)


T50 = rc_line_t50()

# ---------------------------------------------------------------- theory keys
v.check("T 04-05.a", N_CU)
v.check("T 04-05.b", T50)
v.check("T 04-05.c", ALPHA * (100 - 20) * 100)

# ---------------------------------------------------------------- examples
v.check("Ex 04-05.1a", 1 / E_CH)
J1 = 1.0 / 1e-6
v.check("Ex 04-05.1b", J1)
v.check("Ex 04-05.1c", J1 / 1e4)
vd1 = J1 / (N_CU * E_CH)
v.check("Ex 04-05.1d", vd1 * 1e6)
v.check("Ex 04-05.1e", 1 / vd1 / 3600)
tau_cu = tau_from_rho(RHO_CU)
v.check("Ex 04-05.2a", 1 / RHO_CU)
v.check("Ex 04-05.2b", tau_cu * 1e15)
mu_cu = drude_mobility(tau_cu)
v.check("Ex 04-05.2c", mu_cu * 1e4)
v.check("Ex 04-05.2d", VF * tau_cu * 1e9)
vth = sqrt(3 * KB * 300 / ME)
v.check("Ex 04-05.2e", vth)
v.check("Ex 04-05.2f", vth * tau_cu * 1e9)
# silicon (cm units for densities and mobilities)
rho_i = 1 / (E_CH * 1e10 * (1400 + 470))
v.check("Ex 04-05.3a", rho_i)
v.check("Ex 04-05.3b", 1 / (E_CH * 1e15 * 1400))
v.check("Ex 04-05.3c", rho_i / (RHO_CU * 100))
t_oz = 28.3495 / (929.03 * 8.96) * 1e-2           # cm -> m
v.check("Ex 04-05.4a", t_oz * 1e6)
Rs = RHO_CU / t_oz
v.check("Ex 04-05.4b", Rs * 1e3)
R_tr = resistance(RHO_CU, 0.05, lambda x: 0.25e-3 * t_oz)
v.check("Ex 04-05.4c", R_tr / Rs)
v.check("Ex 04-05.4d", R_tr * 1e3)
v.check("Ex 04-05.4e", 2 * R_tr)
v.check("Ex 04-05.4f", 2**2 * R_tr)
v.check("Ex 04-05.5a", (1 + ALPHA * (100 - 20)) / 1.0)
v.check("Ex 04-05.5b", temp_from_R(12.5, 10.0))
w, h, b = 20e-9, 40e-9, 2.5e-9
A_cu = (w - 2 * b) * (h - b)
v.check("Ex 04-05.6a", A_cu * 1e18)
v.check("Ex 04-05.6b", A_cu / (w * h))
r_wire = resistance(RHO_CU, 1e-6, lambda x: A_cu)
v.check("Ex 04-05.6c", r_wire)
v.check("Ex 04-05.6d", resistance(RHO_CU, 1e-6, lambda x: w * h))
eps = 2.8 * EPS0
c_wire = quad(lambda y: eps / w, 0, h)[0] * 2 + quad(lambda x: eps / h, 0, w)[0] * 2      # F/m: plates summed
v.check("Ex 04-05.6e", c_wire * 1e15 * 1e-6)
R100, C100 = r_wire * 100, c_wire * 100e-6
R1m, C1m = r_wire * 1000, c_wire * 1e-3
v.check("Ex 04-05.6f", R100 * C100 * 1e12)
v.check("Ex 04-05.6g", R1m * C1m * 1e9)
v.check("Ex 04-05.6h", T50 * R100 * C100 * 1e12)
v.check("Ex 04-05.6i", T50 * R1m * C1m * 1e9)
v.check("Ex 04-05.6j", R100)
v.check("Ex 04-05.6k", C100 * 1e15)
v.check("Ex 04-05.6l", R1m / 1e3)
v.check("Ex 04-05.6m", C1m * 1e15)
A_cm2 = A_cu * 1e4
v.check("Ex 04-05.7a", 50e-6 / A_cm2 / 1e6)
v.check("Ex 04-05.7b", 0.3e6 * A_cm2 * 1e6)
v.check("Ex 04-05.7c", (50e-6 / A_cm2) / 0.3e6)
v.check("Ex 04-05.7d", RHO_CU * (0.3e6 * 1e4) ** 2)

# ---------------------------------------------------------------- solutions
v.check("04-05.1a", 3 / 2)
v.check("04-05.1b", 1.5 / E_CH)
v.check("04-05.1c", quad(lambda t: 3.0, 0, 3600)[0])
v.check("04-05.2a", 10 / 2.5)
v.check("04-05.2b", (10 / 2.5e-6) / (N_CU * E_CH) * 1e6)
v.check("04-05.3a", resistance(RHO_CU, 100, lambda x: 1.5e-6))
v.check("04-05.3b", resistance(1.10e-6, 1, lambda x: pi * 0.25e-3**2))
rho100 = RHO_CU * (1 + ALPHA * 80)
tau100 = tau_from_rho(rho100)
v.check("04-05.4a", rho100 * 1e8)
v.check("04-05.4b", tau100 * 1e15)
v.check("04-05.4c", VF * tau100 * 1e9)
rho_n = 1 / (E_CH * 1e15 * 1400)
v.check("04-05.5a", rho_n)
v.check("04-05.5b", rho_n / 2e-4)
v.check("04-05.5c", rho_n / 2e-4 * 10 / 1e3)
v.check("04-05.5d", 1 / (E_CH * 1e15 * 470))
v.check("04-05.6a", 100 * 50 / 1)
v.check("04-05.6b", 1e4 / 100 * 2)
v.check("04-05.7a", temp_from_R(4.80, 4.00))
v.check("04-05.8a", sqrt(0.25 / 10))
v.check("04-05.8b", sqrt(0.25 * 10))
p8 = RHO_CU * (4e6) ** 2
v.check("04-05.8c", p8)
v.check("04-05.8d", p8 * 2.5e-6)
v.check("04-05.9a", 3 - 1 - 1.5)
v.check("04-05.9b", 0.5e-3 / 10e-12 / 1e6)
v.check("04-05.10a", 100 * 0.2e-3 * 1e3)
v.check("04-05.10b", 100**2 * 0.2e-3)
v.check("04-05.10c", brentq(lambda R: 100 * R - 0.01, 0, 1) * 1e3)
t11 = 34.06e-6
v.check("04-05.11a", resistance(RHO_CU, 0.05, lambda x: t11 * (0.5e-3 + (0.25e-3 - 0.5e-3) * x / 0.05)) * 1e3)
v.check("04-05.11b", resistance(RHO_CU, 0.05, lambda x: t11 * 0.375e-3) * 1e3)
a12, b12, L12 = 0.45e-3, 1.475e-3, 1.5
R12 = quad(lambda r: 1e13 / (2 * pi * r * L12), a12, b12)[0]
V_per_lam = quad(lambda r: 1 / (2 * pi * 2.25 * EPS0 * r), a12, b12)[0]
C12 = L12 / V_per_lam
v.check("04-05.12a", R12)
v.check("04-05.12b", C12 * 1e12)
v.check("04-05.12c", R12 * C12)
v.assert_true("RC equals rho eps", abs(R12 * C12 / (1e13 * 2.25 * EPS0) - 1) < 1e-10)
v.check("04-05.13a", RHO_CU / A_cu * 1e-6)
v.check("04-05.13b", 5.3e-8 / (w * h) * 1e-6)
v.check("04-05.13c", 6.0e-8 / A_cu * 1e-6)
v.check("04-05.13d", 9.0e-8 / (w * h) * 1e-6)
v.check("04-05.13e", brentq(lambda rc: rc / A_cu - 9.0e-8 / (w * h), 1e-9, 1e-6, xtol=1e-20) * 1e8)
w14 = 2e-3 / (1e6 * 1e4 * 100e-9)
v.check("04-05.14a", w14 * 1e6)
R14 = resistance(RHO_CU, 100e-6, lambda x: w14 * 100e-9)
v.check("04-05.14b", R14)
v.check("04-05.14c", R14 * 2e-3 * 1e3)
v.check("04-05.15a", brentq(lambda f: -np.angle(1 / (1 + 1j * 2 * pi * f * tau_cu), deg=True) - 45, 1e9, 1e15) / 1e12)
RC1 = R1m * C1m
opt = minimize_scalar(lambda k: k * 10e-12 + 0.38 * RC1 / k, bounds=(1, 100), method="bounded", options={"xatol": 1e-10})
v.check("04-05.16a", opt.x)
v.check("04-05.16b", (12 * 10e-12 + 0.38 * RC1 / 12) * 1e12)
v.check("04-05.16c", 0.38 * RC1 * 1e12)

# ---------------------------------------------------------------- lab
tl = 34.06e-6
v.check("Lab 04-05.a", resistance(RHO_CU, 0.1, lambda x: tl * (1e-3 + (0.2e-3 - 1e-3) * x / 0.1)) * 1e3)
v.check("Lab 04-05.b", resistance(RHO_CU, 0.1, lambda x: tl * 0.6e-3) * 1e3)
T_ss = brentq(lambda T: 25 + 30 * 1.0**2 * 1.0 * (1 + ALPHA * (T - 20)) - T, 0, 500)
v.check("Lab 04-05.c", T_ss)
v.check("Lab 04-05.d", brentq(lambda I: 30 * I**2 * 1.0 * ALPHA - 1, 0.1, 10))
v.check("Lab 04-05.e", brentq(lambda t: 1 - np.exp(-t / 0.5) - 0.5, 0.01, 2))      # one section: R with C/2 at the far end
v.check("Lab 04-05.f", T50)

sys.exit(v.finish())
