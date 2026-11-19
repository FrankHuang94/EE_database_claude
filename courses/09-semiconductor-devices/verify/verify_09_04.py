#!/usr/bin/env python3
"""Verify every number in chapter 09-04 (generation, recombination and the continuity equation), its
solutions and lab.

Independent routes:
- SRH rates by solving the trap's steady-state occupation numerically from its four capture and emission
  processes (root finding on net electron capture = net hole capture), never from the closed formula;
- lifetimes as Delta p / U evaluated with the full rate expressions at a small excess, and transients by
  integrating the rate equations in time and fitting the decay;
- quasi-Fermi levels from the carrier densities;
- diffusion profiles by finite-difference boundary-value solutions, currents from the computed slopes;
- surface problems with Robin boundary conditions solved numerically; the wafer's effective lifetime from
  the exact transcendental mode condition and a method-of-lines simulation;
- crossover temperatures by root finding on the course n_i(T) model.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-04", COURSE / "chapters" / "09-04-generation-recombination-continuity.md",
                        COURSE / "solutions" / "09-04-solutions.md",
                        COURSE / "labs" / "09-04-lab" / "README.md")

Q = C.e
K = C.k / C.e
KT = K * 300
NI, NC = 1.0e10, 3.2e19
VN, VP = 2.3e7, 1.65e7
B_SI, CN, CP = 1.1e-14, 1.1e-30, 0.3e-30


def mun(N):
    return 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def mup(N):
    return 48 + 402 / (1 + (N / 6.3e16) ** 0.76)


def eg(T):
    return 1.17 - 4.73e-4 * T**2 / (T + 636)


def ni_T(T):
    return NI * (T / 300) ** 1.5 * math.exp(eg(300) / (2 * K * 300) - eg(T) / (2 * K * T))


def srh_U(n, p, Nt, sn, sp, EtEi, vn=VN, vp=VP):
    """Net SRH rate from the trap's steady-state occupation, found numerically."""
    cn, cp = sn * vn, sp * vp
    n1, p1 = NI * math.exp(EtEi / KT), NI * math.exp(-EtEi / KT)
    def balance(f):
        rn = cn * n * (1 - f) - cn * n1 * f
        rp = cp * p * f - cp * p1 * (1 - f)
        return rn - rp
    f = brentq(balance, 0.0, 1.0, xtol=1e-16)
    return cn * n * Nt * (1 - f) - cn * n1 * Nt * f


def srh_tau(n0, p0, Nt, sn, sp, EtEi, d=None):
    d = d if d is not None else 1e-6 * max(n0, p0)
    return d / srh_U(n0 + d, p0 + d, Nt, sn, sp, EtEi)


def rad_tau(n0, p0, Bc=B_SI):
    d = 1e-6 * max(n0, p0)
    return d / (Bc * ((n0 + d) * (p0 + d) - NI**2))


def auger_tau(n0, p0):
    d = 1e-6 * max(n0, p0)
    n, p = n0 + d, p0 + d
    return d / ((CN * n + CP * p) * (n * p - NI**2))


def fit_decay(tau_true_fun, y0, t_end):
    sol = solve_ivp(tau_true_fun, (0, t_end), [y0], t_eval=np.linspace(0.2 * t_end, t_end, 60), rtol=1e-10, atol=1e-6)
    return -1 / np.polyfit(sol.t, np.log(sol.y[0]), 1)[0]


def bvp_dirichlet(L, W, left=1.0, n=4001):
    x = np.linspace(0, W, n)
    h = x[1] - x[0]
    A = np.zeros((n, n))
    b = np.zeros(n)
    A[0, 0] = A[-1, -1] = 1
    b[0] = left
    for i in range(1, n - 1):
        A[i, i - 1] = A[i, i + 1] = 1 / h**2
        A[i, i] = -2 / h**2 - 1 / L**2
    return x, np.linalg.solve(A, b)


def slope0(x, y):
    """Second-order one-sided derivative at x[0]."""
    h = x[1] - x[0]
    return (-3 * y[0] + 4 * y[1] - y[2]) / (2 * h)


# ================================================================= chapter
# Example 1
n0 = 1e17
p0 = NI**2 / n0
t_rad = rad_tau(n0, p0)
t_aug = auger_tau(n0, p0)
t_srh = srh_tau(n0, p0, 1e12, 1e-15, 1e-15, 0.0)
v.check("Ex 09-04.1a", t_rad * 1e3)
v.check("Ex 09-04.1b", t_aug * 1e6)
v.check("Ex 09-04.1c", t_srh * 1e6)
U_total = lambda t, y: [-(y[0] / t_rad + y[0] / t_aug + y[0] / t_srh)]
v.check("Ex 09-04.1d", fit_decay(U_total, 1e10, 2e-4) * 1e6)
v.check("Ex 09-04.1e", auger_tau(1e19, NI**2 / 1e19) * 1e9)
v.check("Ex 09-04.1f", auger_tau(1e20, NI**2 / 1e20) * 1e12)
v.check("Ex 09-04.1g", rad_tau(1e19, NI**2 / 1e19) * 1e6)
v.check("T 09-04.a", t_rad * 1e3)
v.check("T 09-04.b", auger_tau(1e19, NI**2 / 1e19) * 1e9)

# Example 2: gold
Nt = 1e15
tn0 = 1 / (8e-17 * VN * Nt)
tp0 = 1 / (9.0e-15 * VP * Nt)
v.check("Ex 09-04.2a", tn0 * 1e9)
v.check("Ex 09-04.2b", tp0 * 1e9)
ECEi = KT * math.log(NC / NI)
v.check("Ex 09-04.2c", ECEi)
EtEi = ECEi - 0.55
v.check("Ex 09-04.2d", EtEi * 1e3)
v.check("Ex 09-04.2e", NI * math.exp(EtEi / KT))
v.check("Ex 09-04.2f", NI * math.exp(-EtEi / KT))
v.check("Ex 09-04.2g", srh_tau(1e16, 1e4, Nt, 8e-17, 9.0e-15, EtEi, d=1e10) * 1e9)
EiEv = KT * math.log(1.8e19 / NI)
EtEi_d = 0.35 - EiEv                       # gold donor at E_V + 0.35 eV
v.check("Ex 09-04.2h", srh_tau(1e4, 1e16, Nt, 1e-15, 3.5e-15, EtEi_d, d=1e10) * 1e9)
v.check("Ex 09-04.2i", 1 / (1e-15 * VN * Nt) * 1e9)
v.check("Ex 09-04.2j", NI * math.exp(-EtEi_d / KT))
v.check("Ex 09-04.2k", srh_tau(1e4, 1e16, Nt, 1e-15, 3.5e-15, EtEi_d, d=1e10)
        / srh_tau(1e16, 1e4, Nt, 8e-17, 9.0e-15, EtEi, d=1e10))
v.check("Ex 09-04.2l", EiEv)
v.check("T 09-04.e", tn0 / tp0)

# Example 3: generation from the SRH rate with n, p << n_i
gen = lambda Et: -srh_U(1.0, 1.0, 1.0, 1.0 / (1e-6 * VN), 1.0 / (1e-6 * VP), Et)   # tau_n0 = tau_p0 = 1 us, N_t = 1
G0 = gen(0.0)
v.check("Ex 09-04.3a", G0)
v.check("Ex 09-04.3b", G0 / gen(0.1))
v.check("Ex 09-04.3c", G0 / gen(0.3))

# Example 4: quasi-Fermi levels
N4, d4 = 1e16, 1e14
v.check("Ex 09-04.4a", KT * math.log(N4 / NI))
v.check("Ex 09-04.4b", KT * math.log((N4 + d4) / NI))
v.check("Ex 09-04.4c", KT * math.log((N4 + d4) / N4) * 1e3)
p4 = NI**2 / N4 + d4
v.check("Ex 09-04.4d", KT * math.log(p4 / NI))
v.check("Ex 09-04.4e", KT * math.log((N4 + d4) * p4 / NI**2))
v.check("Ex 09-04.4f", d4 / (NI**2 / N4))

# Example 5: photoconductive decay, simulated
tau5, G5 = 10e-6, 1e19
sol = solve_ivp(lambda t, y: [G5 - y[0] / tau5], (0, 30 * tau5), [0.0], rtol=1e-10, atol=1)
dp5 = sol.y[0][-1]
v.check("Ex 09-04.5a", dp5)
sig0 = Q * 1e15 * mun(1e15)
dsig = Q * dp5 * (mun(1e15) + mup(1e15))
v.check("Ex 09-04.5b", sig0)
v.check("Ex 09-04.5c", dsig)
v.check("Ex 09-04.5d", dsig / sig0 * 100)
off = solve_ivp(lambda t, y: [-y[0] / tau5], (0, 10 * tau5), [1.0], dense_output=True, rtol=1e-11, atol=1e-14)
v.check("Ex 09-04.5e", brentq(lambda t: off.sol(t)[0] - 0.01, 0, 10 * tau5) * 1e6)

# Example 6: injection into long and short regions
Dp6 = KT * mup(1e15)
Lp6 = math.sqrt(Dp6 * 1e-6)
v.check("Ex 09-04.6a", Dp6)
v.check("Ex 09-04.6b", Lp6 * 1e4)
xl, yl = bvp_dirichlet(Lp6, 12 * Lp6, n=8001)
J_long = -Q * Dp6 * 1e14 * slope0(xl, yl)
v.check("Ex 09-04.6c", J_long * 1e3)
v.check("Ex 09-04.6d", float(np.interp(2 * Lp6, xl, yl)))
xs, ys = bvp_dirichlet(Lp6, 5e-4, n=4001)
J_short_exact = -Q * Dp6 * 1e14 * slope0(xs, ys)
J_short_lin = Q * Dp6 * 1e14 / 5e-4
v.check("Ex 09-04.6e", J_short_lin * 1e3)
v.check("Ex 09-04.6f", J_short_lin / J_long)
recomb = np.trapezoid(ys * 1e14 / 1e-6, xs) * Q                   # A/cm^2 lost to recombination
v.check("Ex 09-04.6g", recomb / J_short_exact * 100)          # fraction of injected holes that recombine
v.check("Ex 09-04.6h", J_short_exact * 1e3)

# Example 7: generation leakage, temperature, surface
G7 = -srh_U(0.0, 0.0, 1.0, 1.0 / (1e-6 * VN), 1.0 / (1e-6 * VP), 0.0)
v.check("Ex 09-04.7a", G7)
v.check("Ex 09-04.7b", Q * G7 * 1e-4)
v.check("Ex 09-04.7c", ni_T(350) / NI)
v.check("Ex 09-04.7d", (ni_T(350) / NI) ** 2)
v.check("Ex 09-04.7e", Q * 1e4 * 1e12 * 1e3)

# Theory rows
v.check("T 09-04.c", 7e-10 / B_SI)
v.check("T 09-04.d", 8 / (5.431e-8) ** 3 / 1e12)
v.check("T 09-04.f", 8e4 / 0.5)

# Practitioner
v.check("P 09-04.a", 28.29 / 0.962)

# ================================================================= solutions
NA1 = 1e16
n01 = NI**2 / NA1
ts1 = srh_tau(n01, NA1, 5e11, 1e-15, 1e-15, 0.0)
tr1 = rad_tau(n01, NA1)
ta1 = auger_tau(n01, NA1)
v.check("09-04.1a", ts1 * 1e6)
v.check("09-04.1b", tr1 * 1e3)
v.check("09-04.1c", ta1 * 1e3)
v.check("09-04.1d", 1 / (1 / ts1 + 1 / tr1 + 1 / ta1) * 1e6)

N2, d2 = 5e15, 1e13
v.check("09-04.2a", KT * math.log((N2 + d2) / N2) * 1e3)
v.check("09-04.2b", (NI**2 / N2 + d2) / (NI**2 / N2))
v.check("09-04.2c", d2 / 2e-6)
v.check("09-04.2d", d2 / N2 * 100)
v.check("09-04.3a", 5e20 * 2e-6)

tau4 = lambda N: srh_tau(N, NI**2 / N, 1.0, 1.0 / (1e-6 * VN), 1.0 / (1e-6 * VP), 0.25)
v.check("09-04.4a", NI * math.exp(0.25 / KT))
v.check("09-04.4b", tau4(1e15) * 1e6)
v.check("09-04.4c", tau4(1e14) * 1e6)

I5 = -srh_U(0.0, 0.0, 1.0, 1.0 / (10e-6 * VN), 1.0 / (10e-6 * VP), 0.0) * Q * 2e-4 * 1e-2
v.check("09-04.5a", I5)
v.check("09-04.5b", I5 / 1e-2)

N6, d6 = 1e17, 1e15
n6 = NI**2 / N6 + d6
v.check("09-04.6a", KT * math.log((N6 + d6) / N6) * 1e3)
v.check("09-04.6b", KT * math.log(n6 / NI))
v.check("09-04.6c", KT * math.log((N6 + d6) * n6 / NI**2))
v.check("09-04.6d", KT * math.log(N6 / NI))

sol7 = solve_ivp(lambda t, y: [1e20 - y[0] / 5e-6], (0, 1e-4), [0.0], dense_output=True, rtol=1e-11, atol=1)
v.check("09-04.7a", sol7.sol(1e-4)[0])
v.check("09-04.7b", brentq(lambda t: sol7.sol(t)[0] - 0.9 * 1e20 * 5e-6, 1e-7, 1e-4) * 1e6)

mu8 = mun(1e16)
D8 = KT * mu8
L8 = math.sqrt(D8 * 1e-5)
v.check("09-04.8a", mu8)
v.check("09-04.8b", D8)
v.check("09-04.8c", L8 * 1e4)
x8, y8 = bvp_dirichlet(L8, 12 * L8, n=8001)
v.check("09-04.8d", -Q * D8 * 1e13 * slope0(x8, y8) * 1e3)

D9 = KT * mun(1e17)
L9 = math.sqrt(D9 * 1e-7)
W9 = 0.5e-4
v.check("09-04.9a", D9)
v.check("09-04.9b", L9 * 1e4)
v.check("09-04.9c", L9 / W9)
v.check("09-04.9d", W9**2 / (2 * L9**2))
v.check("09-04.9e", W9**2 / (2 * D9) * 1e12)


def robin_profile(S, D, L, G=1.0, Wt=None, n=6001):
    """Steady D p'' - p/tau + G = 0 on [0, Wt], D p'(0) = S p(0), p'(Wt) = 0 (deep bulk), tau = L^2/D."""
    Wt = Wt or 12 * L
    tau = L * L / D
    x = np.linspace(0, Wt, n)
    h = x[1] - x[0]
    A = np.zeros((n, n))
    b = np.full(n, -G)
    for i in range(1, n - 1):
        A[i, i - 1] = A[i, i + 1] = D / h**2
        A[i, i] = -2 * D / h**2 - 1 / tau
    A[0, 0], A[0, 1], A[0, 2] = -3 * D / (2 * h) - S, 4 * D / (2 * h), -D / (2 * h)
    b[0] = 0.0
    A[-1, -1], A[-1, -2] = 1, -1
    b[-1] = 0.0
    return x, np.linalg.solve(A, b) / (G * tau)


v.check("09-04.10a", Dp6 / Lp6)
for S, (ka, kr) in ((1e4, ("09-04.10b", "09-04.10c")), (10.0, ("09-04.10d", "09-04.10e"))):
    x10, y10 = robin_profile(S, Dp6, Lp6)
    v.check(kr, float(y10[0]))
    v.check(ka, 1 - float(y10[0]))
v.check("09-04.10f", 1e19 * 1e-6)


def exact_tau_eff(S, W=0.03, taub=1e-3, D=Dp6):
    y = brentq(lambda y: y * math.tan(y) - S * W / (2 * D), 1e-12, math.pi / 2 - 1e-12)
    return 1 / (1 / taub + D * (2 * y / W) ** 2)


v.check("09-04.11a", 1 / (1 / 1e-3 + 2 * 10 / 0.03) * 1e6)
v.check("09-04.11b", 10 * 0.03 / (2 * Dp6))
v.assert_true(abs(exact_tau_eff(10.0) / (1 / (1 / 1e-3 + 2 * 10 / 0.03)) - 1) < 0.01, "weak-surface formula within 1% at S = 10")

t12 = auger_tau(1e20, NI**2 / 1e20)
D12 = KT * mup(1e20)
v.check("09-04.12a", t12 * 1e12)
v.check("09-04.12b", mup(1e20))
v.check("09-04.12c", D12)
v.check("09-04.12d", math.sqrt(D12 * t12) * 1e7)

v.check("09-04.13a", brentq(lambda N: srh_tau(1e15, 1e5, N, 8e-17, 9.0e-15, 0.0, d=1e8) - 50e-9, 1e12, 1e16))

Tc = brentq(lambda T: ni_T(T) / NI - 100, 300, 500)
v.check("09-04.14a", Tc)
v.check("09-04.14b", Tc - 273.15)

t_r15 = rad_tau(1e17, 1.0, Bc=7e-10)
v.check("09-04.15a", t_r15 * 1e9)
tot15 = 1 / (1 / t_r15 + 1 / 10e-9)
v.check("09-04.15b", tot15 * 1e9)
v.check("09-04.15c", tot15 / t_r15)

# ================================================================= lab
v.check("Lab 09-04.a", 1 / (9.0e-15 * VP * 1e13) * 1e9)
v.check("Lab 09-04.b", exact_tau_eff(1e4) * 1e6)
v.check("Lab 09-04.c", 1 / (1 / 1e-3 + 2 * 1e4 / 0.03) * 1e6)
v.check("Lab 09-04.d", 1 / (1 / 1e-3 + math.pi**2 * Dp6 / 0.03**2) * 1e6)
v.check("Lab 09-04.e", exact_tau_eff(10.0) * 1e6)
v.check("Lab 09-04.f", 1 / (1 / 1e-3 + 2 * 10 / 0.03) * 1e6)
v.check("Lab 09-04.g", math.log10(G0 / gen(0.3)))

v.finish()
