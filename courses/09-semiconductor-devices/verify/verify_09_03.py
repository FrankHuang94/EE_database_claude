#!/usr/bin/env python3
"""Verify every number in chapter 09-03 (carrier transport: drift and diffusion), its solutions and lab.

Independent routes:
- the drift relation mu = q tau/m* is confirmed by a Monte Carlo ensemble of electrons with Poisson
  collisions; the thermal velocity by integrating the Maxwell-Boltzmann distribution;
- mobility models are evaluated as published and inverted with a root finder; model spreads by scanning;
- sheet resistances by integrating slice conductances; the four-point-probe constant by superposing the
  potentials of point sources on a sheet numerically;
- velocities from the velocity-field fits, with transit times by integrating dx/v;
- the Einstein relation and built-in fields by imposing a flat Fermi level on a doping profile and
  differentiating the band edge numerically (not from the closed-form field);
- diffusion by a simulated random walk; temperature coefficients by numerical differentiation.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-03", COURSE / "chapters" / "09-03-drift-and-diffusion.md",
                        COURSE / "solutions" / "09-03-solutions.md",
                        COURSE / "labs" / "09-03-lab" / "README.md")

Q, M0, KB = C.e, C.m_e, C.k
VT = KB * 300 / Q                     # kT/q at 300 K, volts
NC = 3.2e19


def mun(N):
    return 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def mup(N):
    return 48 + 402 / (1 + (N / 6.3e16) ** 0.76)


def mun_hu(N):
    return 92 + 1318 / (1 + (N / 1e17) ** 0.85)


def mup_hu(N):
    return 50 + 420 / (1 + (N / 1.6e17) ** 0.7)


def mu_L(T, a=1430.0):
    return a * (300 / T) ** 2.2


def vfit(F, vs, Fc, beta):
    return vs * (F / Fc) / (1 + (F / Fc) ** beta) ** (1 / beta)


def e_params(T=300.0):
    return 1.53e9 * T**-0.87, 1.01 * T**1.55, 2.57e-2 * T**0.66


def h_params(T=300.0):
    return 1.62e8 * T**-0.52, 1.24 * T**1.68, 0.46 * T**0.17


def ve(F):
    return vfit(F, *e_params())


def vh(F):
    return vfit(F, *h_params())


def tau_of(mu_cm2, m_rel):
    return mu_cm2 * 1e-4 * m_rel * M0 / Q


def vth_numeric(m_rel, T=300.0):
    """sqrt(<v^2>) from the Maxwell-Boltzmann speed distribution, integrated numerically (cm/s)."""
    m = m_rel * M0
    a = m / (2 * KB * T)
    f = lambda v_: 4 * math.pi * (a / math.pi) ** 1.5 * v_**2 * math.exp(-a * v_**2)
    scale = math.sqrt(1 / a)
    v2 = quad(lambda v_: v_**2 * f(v_), 0, 20 * scale)[0]
    return math.sqrt(v2) * 100


def mc_drift(tau, m_rel, field_V_per_m, n=200_000, seed=1):
    """Monte Carlo: time-average velocity of electrons with exponential free flights (m/s)."""
    rng = np.random.default_rng(seed)
    t = rng.exponential(tau, n)                       # free-flight durations
    a = -Q * field_V_per_m / (m_rel * M0)
    # average velocity over a flight of length t, starting from zero: a t / 2; weight flights by duration
    return np.sum(a * t * t / 2) / np.sum(t)


def equilibrium_field(Nfun, x, majority="n"):
    """Field (V/cm) from a flat Fermi level: E_C(x) - E_F = kT ln(N_C/n(x)), E = (1/q) dE_C/dx."""
    if majority == "n":
        Ec = VT * np.log(NC / Nfun(x))                # eV relative to E_F, numerically per point
        return np.gradient(Ec, x, edge_order=2)
    Ev = -VT * np.log(1.8e19 / Nfun(x))               # E_V - E_F for p-type
    return np.gradient(Ev, x, edge_order=2)


# ================================================================= chapter
# Example 1
N1 = 1e15
x91 = (N1 / 1.3e17) ** 0.91
v.check("Ex 09-03.1a", x91)
mu1 = mun(N1)
v.check("Ex 09-03.1b", mu1)
tau1 = tau_of(mu1, 0.26)
v.check("Ex 09-03.1c", tau1 * 1e12)
vd_mc = mc_drift(tau1, 0.26, 1e5)                      # 1 kV/cm = 1e5 V/m
v.assert_true(abs(-vd_mc * 100 / (mu1 * 1e3) - 1) < 0.01, "Monte Carlo drift velocity matches q tau/m* times the field")
vth1 = vth_numeric(0.26)
v.check("Ex 09-03.1d", vth1)
lam1 = vth1 * tau1 * 1e7                              # nm
v.check("Ex 09-03.1e", lam1)
v.check("Ex 09-03.1f", mu1 * 1e3)
v.check("Ex 09-03.1g", mu1 * 1e3 / vth1)
v.check("Ex 09-03.1h", KB * 300)
v.check("Ex 09-03.1i", 0.26 * M0)
v.check("Ex 09-03.1j", lam1 / 0.5431)

# Example 2
for N, (ka, kb, kc, kd) in ((1e15, "abcd"), (1e17, "efgh"), (1e19, "ijkl")):
    v.check(f"Ex 09-03.2{ka}", mun(N))
    v.check(f"Ex 09-03.2{kb}", mun_hu(N))
    v.check(f"Ex 09-03.2{kc}", (mun_hu(N) - mun(N)) / mun(N) * 100)
    v.check(f"Ex 09-03.2{kd}", 1 / (Q * N * mun(N)))
v.check("Ex 09-03.2m", mup(1e16))
v.check("Ex 09-03.2n", mup_hu(1e16))
v.check("Ex 09-03.2o", 1 / (Q * 1e16 * mup(1e16)))
v.check("Ex 09-03.2p", (1 / (Q * 1e15 * mun(1e15))) / (1 / (Q * 1e19 * mun(1e19))))
v.check("Ex 09-03.2q", mun(1e15) / mun(1e19))

# Example 3: sheet resistance by integrating slices; 4PP constant by superposition
t3 = 0.5e-4
Rs3 = 1 / quad(lambda x: Q * mun(1e18) * 1e18, 0, t3)[0]
v.check("Ex 09-03.3a", mun(1e18))
v.check("Ex 09-03.3b", 1 / (Q * 1e18 * mun(1e18)))
v.check("Ex 09-03.3c", Rs3)


def four_point_V(Rs, I, s=1.0):
    pot = lambda r: -(Rs * I / (2 * math.pi)) * math.log(r)       # point source on a sheet
    probes = [0.0, s, 2 * s, 3 * s]
    V = lambda x: pot(abs(x - probes[0])) - pot(abs(x - probes[3]))
    return V(probes[1]) - V(probes[2])


k4 = 1 / four_point_V(1.0, 1.0)
v.check("Ex 09-03.3f", k4)
v.check("Ex 09-03.3e", 1 / k4)
v.check("Ex 09-03.3d", four_point_V(Rs3, 1e-3))
v.check("Ex 09-03.3g", 1e4 / Rs3)
v.check("Ex 09-03.3h", 1e4 / Rs3 * 1.0)

# Example 4: temperature
v.check("Ex 09-03.4a", mu_L(250))
v.check("Ex 09-03.4b", mu_L(300))
v.check("Ex 09-03.4c", mu_L(400))
v.check("Ex 09-03.4d", mu_L(300) / mu_L(400))
muI300 = brentq(lambda m: 1 / (1 / mu_L(300) + 1 / m) - mun(1e17), 100, 1e5)
v.check("Ex 09-03.4e", muI300)
muI400 = muI300 * (400 / 300) ** 1.5
v.check("Ex 09-03.4f", muI400)
mu400 = 1 / (1 / mu_L(400) + 1 / muI400)
v.check("Ex 09-03.4g", mu400)
v.check("Ex 09-03.4h", mun(1e17) / mu400)

# Example 5: velocity saturation
vs, Fc, beta = e_params()
v.check("Ex 09-03.5a", vs)
v.check("Ex 09-03.5b", Fc)
v.check("Ex 09-03.5c", beta)
mu0 = (ve(1e-3) / 1e-3)                                # low-field limit, numerically
v.check("Ex 09-03.5d", mu0)
for F, (kv, kr) in ((1e3, "ef"), (1e4, "gh"), (3e4, "ij"), (1e5, "kl")):
    v.check(f"Ex 09-03.5{kv}", ve(F))
    v.check(f"Ex 09-03.5{kr}", ve(F) / (mu0 * F))
v.check("Ex 09-03.5m", ve(5e4))
v.check("Ex 09-03.5n", quad(lambda x: 1 / ve(5e4), 0, 1e-4)[0] * 1e12)
v.check("Ex 09-03.5o", 1e-4 / (1400 * 5e4) * 1e12)
v.check("Ex 09-03.5p", 1400 * 5e4)
v.check("Ex 09-03.5q", ve(1e5) / vs * 100)

# Example 6: Einstein relation by solving zero current in a graded sample
xg = np.linspace(0, 1e-4, 20001)
Nfun = lambda x: 1e15 * np.exp(-x / 2e-5)
E_eq = equilibrium_field(Nfun, xg)                      # V/cm
dndx = np.gradient(Nfun(xg), xg)
D_from_zero_current = -(mu1 * Nfun(xg) * E_eq) / dndx    # J = q n mu E + q D dn/dx = 0
D6 = float(np.median(D_from_zero_current))
v.check("Ex 09-03.6a", D6)
v.assert_true(abs(D6 / (mu1 * VT) - 1) < 1e-4, "D/mu = kT/q from the zero-current condition")
v.check("Ex 09-03.6b", mup(1e15))
v.check("Ex 09-03.6c", VT * mup(1e15))
v.check("Ex 09-03.6d", math.sqrt(D6 * 1e-6) * 1e4)
v.check("Ex 09-03.6e", (1e16 - 1e14) / 1e-4)
v.check("Ex 09-03.6f", Q * D6 * (-(1e16 - 1e14) / 1e-4))

# Example 7: graded base, p-type, field from a flat Fermi level
W = 0.2e-4
NA = lambda x: 1e18 * np.exp(-x * math.log(100) / W)
xb = np.linspace(0, W, 20001)
Eb = equilibrium_field(NA, xb, majority="p")
v.check("Ex 09-03.7a", abs(float(np.median(Eb))))
vel = mun(1e17) * abs(float(np.median(Eb)))
v.check("Ex 09-03.7b", vel)
v.check("Ex 09-03.7c", W / vel * 1e12)
D7 = VT * mun(1e17)
v.check("Ex 09-03.7d", D7)
v.check("Ex 09-03.7e", W**2 / (2 * D7) * 1e12)

# Theory rows
v.check("T 09-03.a", vth_numeric(0.26) / 100 / 1e3 * 1e3)       # m/s, handbook value 2.3e5
v.check("T 09-03.b", 1e19 / 1e15)
v.check("T 09-03.c", math.sqrt(2 * 0.063 * Q / (0.26 * M0)) * 100)
vsh, Fch, bh = h_params()
v.check("T 09-03.d", vsh)
v.check("T 09-03.e", Fch)
v.check("T 09-03.f", bh)
v.check("T 09-03.g", mu0)
v.check("T 09-03.h", 1.0 / 100e-7)
v.check("T 09-03.i", (mu0 * 1e5) / ve(1e5))
v.check("T 09-03.j", abs(float(np.median(equilibrium_field(lambda x: 1e18 * np.exp(-x * math.log(100) / 0.2e-4), xb)))) / 1e3)
Ns = np.logspace(15, 19, 4001)
dn = np.abs((mun_hu(Ns) - mun(Ns)) / mun(Ns)) * 100
dp = np.abs((mup_hu(Ns) - mup(Ns)) / mup(Ns)) * 100
v.check("T 09-03.k", dn.max())
v.check("T 09-03.l", dp.max())
v.check("T 09-03.m", Ns[dp.argmax()])

# ================================================================= solutions
mu = mup(1e16)
v.check("09-03.1a", mu)
tp = tau_of(mu, 0.39)
v.check("09-03.1b", tp * 1e12)
v.check("09-03.1c", mu * 500)
vthp = vth_numeric(0.39)
v.check("09-03.1d", vthp)
v.check("09-03.1e", vthp * tp * 1e7)

v.check("09-03.2a", 1 / (1 / 1430 + 1 / 3000))
v.check("09-03.2b", brentq(lambda m: 1 / (1 / 1430 + 1 / m) - 1000, 1000, 1e5))

Nn = brentq(lambda N: 1 / (Q * N * mun(N)) - 10, 1e12, 1e18)
Np = brentq(lambda N: 1 / (Q * N * mup(N)) - 10, 1e12, 1e18)
v.check("09-03.3a", Nn)
v.check("09-03.3b", mun(Nn))
v.check("09-03.3c", Np)
v.check("09-03.3d", mup(Np))

v.check("09-03.4a", mun(3e17))
r_c = 1 / (Q * 1e17 * mun(3e17))
r_u = 1 / (Q * 1e17 * mun(1e17))
v.check("09-03.4b", r_c)
v.check("09-03.4c", r_u)
v.check("09-03.4d", r_c / r_u)

v.check("09-03.5a", 50e3 / 200)
v.check("09-03.5b", 50e3 / 200 * 2)
v.check("09-03.5c", four_point_V(200, 1e-3) * 1e3)

g_top = quad(lambda x: Q * mun(1e19) * 1e19, 0, 0.2e-4)[0]
g_bot = quad(lambda x: Q * mun(1e17) * 1e17, 0.2e-4, 1.0e-4)[0]
v.check("09-03.6a", g_top)
v.check("09-03.6b", g_bot)
v.check("09-03.6c", 1 / (g_top + g_bot))
v.check("09-03.6d", g_top / (g_top + g_bot) * 100)
v.check("09-03.6e", 1 / g_top)
v.check("09-03.6f", 1 / g_bot)

v.check("09-03.7a", vh(1e4))
v.check("09-03.7b", vh(1e5))
v.check("09-03.7c", vh(2e5))
v.check("09-03.7d", quad(lambda x: 1 / vh(2e5), 0, 50e-7)[0] * 1e12)
v.check("09-03.7e", ve(2e5))
v.check("09-03.7f", quad(lambda x: 1 / ve(2e5), 0, 50e-7)[0] * 1e12)
v.check("09-03.7g", (ve(2e5) / vh(2e5) - 1) * 100)

v.check("09-03.8a", mup(1e17))
Dp8 = VT * mup(1e17)
v.check("09-03.8b", Dp8)
v.check("09-03.8c", math.sqrt(Dp8 * 1e-7) * 1e4)
v.check("09-03.8d", KB * 400 / Q * 1e3)

L9 = 10e-4
x9 = np.linspace(0, 3 * L9, 30001)
n9 = 1e15 * np.exp(-x9 / L9)
J9 = Q * D6 * np.gradient(n9, x9)
v.check("09-03.9a", float(J9[0]))
v.check("09-03.9b", float(np.interp(2 * L9, x9, J9)))

x10 = np.linspace(0, 1e-4, 100001)
N10 = lambda x: 1e17 + (1e16 - 1e17) * x / 1e-4
E10 = equilibrium_field(N10, x10)
v.check("09-03.10a", (1e16 - 1e17) / 1e-4)
v.check("09-03.10b", float(E10[0]))
v.check("09-03.10c", float(np.interp(0.5e-4, x10, E10)))
v.check("09-03.10d", float(E10[-1]))
v.check("09-03.10e", np.trapezoid(E10, x10) * 1e3)

h = 0.01
lnR = lambda T: math.log(1 / mu_L(T))
v.check("09-03.11a", (lnR(300 + h) - lnR(300 - h)) / (2 * h) * 1e6)
mu17 = lambda T: 1 / (1 / mu_L(T) + 1 / (muI300 * (T / 300) ** 1.5))
v.check("09-03.11b", (math.log(1 / mu17(300 + h)) - math.log(1 / mu17(300 - h))) / (2 * h) * 1e6)

ratio = brentq(lambda r: (lambda T: 1 / (1 / mu_L(T) + 1 / (r * mu_L(300) * (T / 300) ** 1.5)))(300 + h)
               - (lambda T: 1 / (1 / mu_L(T) + 1 / (r * mu_L(300) * (T / 300) ** 1.5)))(300 - h), 0.1, 5)
v.check("09-03.12a", ratio)
v.check("09-03.12b", ratio * mu_L(300))
mu12 = 1 / (1 / mu_L(300) + 1 / (ratio * mu_L(300)))
v.check("09-03.12c", mu12)
v.check("09-03.12d", brentq(lambda N: mun(N) - mu12, 1e15, 1e19))

v.check("09-03.13a", vth1 * (lam1 * 1e-7) / 3)
rng = np.random.default_rng(11)
steps = rng.choice([-1.0, 1.0], size=(4000, 400))
spread = np.var(steps.sum(axis=1)) / 400 / 2            # D in units of lambda^2/tau
v.assert_true(abs(spread - 0.5) < 0.03, "simulated 1-D random walk gives D = lambda^2/(2 tau)")

I, B, t, VH, rho = 1e-3, 0.5, 0.5e-3, 6.24e-3, 4.7
n14 = I * B / (Q * t * VH) / 1e6
v.check("09-03.14a", n14)
RH = VH * t / (I * B) * 1e6
v.check("09-03.14b", RH)
v.check("09-03.14c", RH / rho)
v.check("09-03.14d", mun(n14))
v.check("09-03.14e", (RH / rho) / mun(n14))

Fe = brentq(lambda F: ve(F) - 5e6, 10, 1e6)
Fh = brentq(lambda F: vh(F) - 5e6, 10, 1e6)
v.check("09-03.15a", Fe)
v.check("09-03.15b", Fe * 5e-4)
v.check("09-03.15c", Fh)
v.check("09-03.15d", Fh * 5e-4)
v.check("09-03.15e", 5e-4 / vs * 1e12)
v.check("09-03.15f", 5e-4 / vsh * 1e12)

# ================================================================= lab
def sheet_gauss(sigma, dose=1e14):
    N0 = 2 * dose / (sigma * math.sqrt(2 * math.pi))
    g = quad(lambda x: Q * mun(N0 * math.exp(-x * x / (2 * sigma * sigma))) * N0 * math.exp(-x * x / (2 * sigma * sigma)),
             0, 12 * sigma, limit=200)[0]
    return 1 / g, N0


R50, N50 = sheet_gauss(50e-7)
R100, N100 = sheet_gauss(100e-7)
v.assert_true(abs(quad(lambda x: N50 * math.exp(-x * x / (2 * (50e-7) ** 2)), 0, 1e-4)[0] / 1e14 - 1) < 1e-6, "half-Gaussian holds the stated dose")
v.check("Lab 09-03.a", N50)
v.check("Lab 09-03.b", R50)
v.check("Lab 09-03.c", N100)
v.check("Lab 09-03.d", R100)
v.check("Lab 09-03.e", R50 / R100)
v.check("Lab 09-03.f", ve(1e5) / vs * 100)
xl = np.linspace(0, 1e-4, 20001)
v.check("Lab 09-03.g", float(np.median(equilibrium_field(lambda x: 1e17 * np.exp(-x / 0.5e-4), xl))))
v.finish()
